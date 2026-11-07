# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""
MambaPSA: khối Mamba thay cho C2PSA ở cuối backbone YOLO26.

TÁI HIỆN THEO MÔ TẢ trong bài: S.-W. Chan et al., "MambaPSA: A Mamba-based replacement for C2PSA in YOLO26",
arXiv:2607.12681v1, 2026. Bài báo chưa công bố mã nguồn, nên đây KHÔNG phải mã gốc của tác giả.

Theo mô tả của bài báo:
- Đặc trưng được chiếu 1×1 rồi tách làm hai nửa.
- Nửa a đi qua một lõi Mamba một chiều (mono-directional); nửa b giữ nguyên (identity).
- Ghép hai nửa rồi qua một tích chập 1×1 thứ hai.

Các chi tiết bài báo không ghi rõ được chọn theo mặc định của Mamba gốc:
- expand = 2, d_state = 16, d_conv = 4 (tích chập 1 chiều nhân quả);
- có thêm nhánh nối tắt D và kết nối dư.

Lõi quét dùng lại phép quét kết hợp song song `parallel_associative_scan` của khối TSVM (cùng fork),
nên chạy được trên GPU Kaggle mà không cần biên dịch `mamba_ssm`.
"""

from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from .conv import Conv
from .topology_shape_vmamba import parallel_associative_scan


class MambaCore1D(nn.Module):
    """Lõi Mamba một chiều (quét theo hàng, từ trái sang phải, trên trên xuống dưới)."""

    def __init__(self, c: int, d_state: int = 16, d_conv: int = 4, expand: float = 2.0):
        super().__init__()
        self.d_inner = int(expand * c)
        self.d_state = d_state
        self.dt_rank = math.ceil(c / 16)
        self.in_proj = nn.Linear(c, self.d_inner * 2, bias=False)
        self.conv1d = nn.Conv1d(self.d_inner, self.d_inner, d_conv, groups=self.d_inner, padding=d_conv - 1)
        self.x_proj = nn.Linear(self.d_inner, self.dt_rank + 2 * d_state, bias=False)
        self.dt_proj = nn.Linear(self.dt_rank, self.d_inner, bias=True)
        A = torch.arange(1, d_state + 1, dtype=torch.float32).repeat(self.d_inner, 1)
        self.A_log = nn.Parameter(torch.log(A))          # (D, N), A = -exp(A_log)
        self.D = nn.Parameter(torch.ones(self.d_inner))  # nối tắt trực tiếp như Mamba gốc
        self.out_proj = nn.Linear(self.d_inner, c, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, C, H, W = x.shape
        L = H * W
        seq = x.flatten(2).transpose(1, 2)                      # (B, L, C)
        u, z = self.in_proj(seq).chunk(2, dim=-1)               # (B, L, D)
        u = self.conv1d(u.transpose(1, 2))[..., :L]             # tích chập nhân quả, (B, D, L)
        u = F.silu(u)
        dt_raw, B_raw, C_raw = torch.split(self.x_proj(u.transpose(1, 2)),
                                           [self.dt_rank, self.d_state, self.d_state], dim=-1)
        dt = F.softplus(self.dt_proj(dt_raw)).transpose(1, 2)  # (B, D, L)
        A = -torch.exp(self.A_log)                              # (D, N)
        a = torch.exp(torch.clamp(dt.unsqueeze(2) * A[None, :, :, None], min=-50.0, max=0.0))  # (B, D, N, L)
        b = dt.unsqueeze(2) * B_raw.transpose(1, 2).unsqueeze(1) * u.unsqueeze(2)              # (B, D, N, L)
        h = parallel_associative_scan(a, b)                                                     # (B, D, N, L)
        y = torch.einsum("bdnl,bnl->bdl", h, C_raw.transpose(1, 2)) + u * self.D[None, :, None]
        y = y.transpose(1, 2) * F.silu(z)                       # (B, L, D)
        return self.out_proj(y).transpose(1, 2).reshape(B, C, H, W)


class MambaPSA(nn.Module):
    """Thay cho C2PSA: cv1 -> tách (a, b) -> a qua lõi Mamba một chiều (có dư), b giữ nguyên -> ghép -> cv2."""

    def __init__(self, c1: int, c2: int, n: int = 1, e: float = 0.5, d_state: int = 16, d_conv: int = 4):
        super().__init__()
        assert c1 == c2, f"MambaPSA yêu cầu c1 == c2, nhận c1={c1}, c2={c2}"
        self.c = int(c1 * e)
        self.cv1 = Conv(c1, 2 * self.c, 1, 1)
        self.cv2 = Conv(2 * self.c, c1, 1)
        self.m = nn.ModuleList(MambaCore1D(self.c, d_state=d_state, d_conv=d_conv) for _ in range(n))
        self.norms = nn.ModuleList(nn.GroupNorm(1, self.c) for _ in range(n))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        a, b = self.cv1(x).split((self.c, self.c), dim=1)
        for norm, core in zip(self.norms, self.m):
            a = a + core(norm(a))
        return self.cv2(torch.cat((a, b), dim=1))
