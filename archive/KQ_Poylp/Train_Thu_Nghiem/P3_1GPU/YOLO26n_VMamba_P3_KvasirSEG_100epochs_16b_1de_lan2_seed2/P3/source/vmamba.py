# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""Lightweight Visual State-Space modules for YOLO feature refinement."""

from __future__ import annotations

import math
import warnings
from typing import Any

import torch
import torch.nn as nn
import torch.nn.functional as F

from .block import C3k2

__all__ = ("C3k2VSS", "PartialVSSRefine")

try:
    from mamba_ssm.ops.selective_scan_interface import selective_scan_fn as _mamba_selective_scan_fn

    _MAMBA_IMPORT_ERROR = None
except Exception as error:  # mamba-ssm may fail with ImportError, OSError, or a CUDA ABI RuntimeError
    _mamba_selective_scan_fn = None
    _MAMBA_IMPORT_ERROR = f"{type(error).__name__}: {error}"


class DropPath(nn.Module):
    """Per-sample stochastic depth without an external timm dependency."""

    def __init__(self, drop_prob: float = 0.0):
        """Initialize stochastic depth."""
        super().__init__()
        if not 0.0 <= drop_prob < 1.0:
            raise ValueError(f"drop_prob must be in [0, 1), got {drop_prob}")
        self.drop_prob = float(drop_prob)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Apply stochastic depth during training."""
        if self.drop_prob == 0.0 or not self.training:
            return x
        keep_prob = 1.0 - self.drop_prob
        shape = (x.shape[0],) + (1,) * (x.ndim - 1)
        random_tensor = keep_prob + torch.rand(shape, dtype=x.dtype, device=x.device)
        return x * random_tensor.floor_() / keep_prob


class PartialVSSRefine(nn.Module):
    """Refine a channel subset with four-direction 2D selective scan and a near-identity residual."""

    valid_backends = frozenset({"auto", "cuda", "torch"})

    def __init__(
        self,
        channels: int,
        d_state: int = 8,
        d_conv: int = 3,
        expand: float = 2.0,
        scans: int = 4,
        drop_path: float = 0.0,
        gamma_init: float = 1e-3,
        backend: str = "auto",
        dt_rank: int | str = "auto",
        bias: bool = False,
        dt_min: float = 1e-3,
        dt_max: float = 1e-1,
        dt_init_floor: float = 1e-4,
        vss_force_fp32: bool = False,
    ):
        """Initialize a lightweight SS2D refinement branch.

        Args:
            channels: Number of partial channels refined by the branch.
            d_state: Selective state dimension.
            d_conv: Odd depthwise convolution kernel size.
            expand: Inner channel expansion ratio.
            scans: Number of scan directions. Milestone 2A supports the VMamba four-direction scan.
            drop_path: Stochastic depth probability on the new branch.
            gamma_init: Initial per-channel residual coefficient.
            backend: Selective scan backend: ``auto``, ``cuda``, or ``torch``.
            dt_rank: Delta projection rank, or ``auto`` for ceil(d_inner / 16).
            bias: Whether input and output linear projections use bias.
            dt_min: Minimum initialized selective timestep.
            dt_max: Maximum initialized selective timestep.
            dt_init_floor: Numerical lower bound for timestep initialization.
            vss_force_fp32: Run the VSS branch and residual fusion in an explicit FP32 autocast island.
        """
        super().__init__()
        if channels < 1:
            raise ValueError(f"channels must be positive, got {channels}")
        if d_state < 1:
            raise ValueError(f"d_state must be positive, got {d_state}")
        if d_conv < 1 or d_conv % 2 == 0:
            raise ValueError(f"d_conv must be a positive odd number, got {d_conv}")
        if expand <= 0:
            raise ValueError(f"expand must be positive, got {expand}")
        if scans != 4:
            raise ValueError(f"Only four-direction SS2D is supported, got scans={scans}")
        if backend not in self.valid_backends:
            raise ValueError(f"backend must be one of {sorted(self.valid_backends)}, got {backend!r}")
        if not (0 < dt_min < dt_max):
            raise ValueError(f"Expected 0 < dt_min < dt_max, got {dt_min} and {dt_max}")

        self.channels = int(channels)
        self.d_state = int(d_state)
        self.d_conv = int(d_conv)
        self.expand = float(expand)
        self.scans = int(scans)
        self.d_inner = max(int(round(self.channels * self.expand)), 1)
        self.dt_rank = math.ceil(self.d_inner / 16) if dt_rank == "auto" else int(dt_rank)
        self.backend = backend
        self.last_backend: str | None = None
        self.backend_reason: str | None = None
        self._warned_fast_failure = False
        self.vss_force_fp32 = bool(vss_force_fp32)
        self.last_dtype_trace: dict[str, Any] = {}

        self.in_norm = nn.LayerNorm(self.channels)
        self.in_proj = nn.Linear(self.channels, 2 * self.d_inner, bias=bias)
        self.dwconv = nn.Conv2d(
            self.d_inner,
            self.d_inner,
            kernel_size=self.d_conv,
            padding=self.d_conv // 2,
            groups=self.d_inner,
            bias=True,
        )
        self.activation = nn.SiLU()

        projection_dim = self.dt_rank + 2 * self.d_state
        self.x_proj_weight = nn.Parameter(torch.empty(self.scans, projection_dim, self.d_inner))
        self.dt_proj_weight = nn.Parameter(torch.empty(self.scans, self.d_inner, self.dt_rank))
        self.dt_proj_bias = nn.Parameter(torch.empty(self.scans, self.d_inner))

        a = torch.arange(1, self.d_state + 1, dtype=torch.float32)
        a = a.view(1, self.d_state).repeat(self.scans * self.d_inner, 1)
        self.A_logs = nn.Parameter(torch.log(a))
        self.Ds = nn.Parameter(torch.ones(self.scans * self.d_inner, dtype=torch.float32))

        self.out_norm = nn.LayerNorm(self.d_inner)
        self.out_proj = nn.Linear(self.d_inner, self.channels, bias=bias)
        self.drop_path = DropPath(drop_path) if drop_path > 0.0 else nn.Identity()
        self.gamma = nn.Parameter(torch.full((1, self.channels, 1, 1), float(gamma_init)))

        self._initialize_selective_parameters(dt_min, dt_max, dt_init_floor)

    def _initialize_selective_parameters(self, dt_min: float, dt_max: float, dt_init_floor: float) -> None:
        """Initialize input-dependent selective-scan projections and stable SSM timesteps."""
        nn.init.xavier_uniform_(self.x_proj_weight.view(-1, self.d_inner))
        dt_scale = self.dt_rank**-0.5
        nn.init.uniform_(self.dt_proj_weight, -dt_scale, dt_scale)
        dt = torch.exp(
            torch.rand(self.scans, self.d_inner) * (math.log(dt_max) - math.log(dt_min)) + math.log(dt_min)
        ).clamp_min(dt_init_floor)
        inverse_softplus = dt + torch.log(-torch.expm1(-dt))
        with torch.no_grad():
            self.dt_proj_bias.copy_(inverse_softplus)

    @staticmethod
    def _cross_scan(x: torch.Tensor) -> torch.Tensor:
        """Create row, column, reverse-row, and reverse-column scan sequences."""
        b, d, h, w = x.shape
        row = x.flatten(2)
        column = x.transpose(2, 3).contiguous().flatten(2)
        forward = torch.stack((row, column), dim=1)
        return torch.cat((forward, torch.flip(forward, dims=(-1,))), dim=1).view(b, 4, d, h * w)

    @staticmethod
    def _cross_merge(y: torch.Tensor, h: int, w: int) -> torch.Tensor:
        """Invert four scan routes and merge them in the original row-major image layout."""
        b, _, d, length = y.shape
        if length != h * w:
            raise ValueError(f"Scan length {length} does not match H*W={h * w}")
        reverse = torch.flip(y[:, 2:4], dims=(-1,))
        column = y[:, 1].view(b, d, w, h).transpose(2, 3).contiguous().view(b, d, length)
        reverse_column = reverse[:, 1].view(b, d, w, h).transpose(2, 3).contiguous().view(b, d, length)
        return y[:, 0] + reverse[:, 0] + column + reverse_column

    @staticmethod
    def _selective_scan_torch(
        u: torch.Tensor,
        delta: torch.Tensor,
        a: torch.Tensor,
        b_param: torch.Tensor,
        c_param: torch.Tensor,
        d_skip: torch.Tensor,
        delta_bias: torch.Tensor,
    ) -> torch.Tensor:
        """Differentiable FP32 reference selective scan used as a correctness fallback."""
        input_dtype = u.dtype
        u = u.float()
        delta = F.softplus(delta.float() + delta_bias.float().view(1, -1, 1))
        a = a.float()
        b_param = b_param.float()
        c_param = c_param.float()
        d_skip = d_skip.float()

        batch, channels, length = u.shape
        groups, d_state = b_param.shape[1:3]
        if channels % groups:
            raise ValueError(f"Scan channels {channels} must be divisible by B/C groups {groups}")
        channels_per_group = channels // groups
        b_expanded = b_param.repeat_interleave(channels_per_group, dim=1)
        c_expanded = c_param.repeat_interleave(channels_per_group, dim=1)
        state = torch.zeros(batch, channels, d_state, dtype=torch.float32, device=u.device)
        outputs = []
        a = a.unsqueeze(0)
        for index in range(length):
            delta_t = delta[:, :, index]
            u_t = u[:, :, index]
            state = (
                torch.exp(delta_t.unsqueeze(-1) * a) * state
                + delta_t.unsqueeze(-1) * b_expanded[:, :, :, index] * u_t.unsqueeze(-1)
            )
            y_t = (state * c_expanded[:, :, :, index]).sum(-1) + d_skip.view(1, -1) * u_t
            outputs.append(y_t)
        return torch.stack(outputs, dim=-1).to(input_dtype)

    def _run_selective_scan(
        self,
        u: torch.Tensor,
        delta: torch.Tensor,
        a: torch.Tensor,
        b_param: torch.Tensor,
        c_param: torch.Tensor,
        d_skip: torch.Tensor,
        delta_bias: torch.Tensor,
    ) -> torch.Tensor:
        """Dispatch selective scan while making the actually executed backend observable."""
        self.last_dtype_trace.update(
            {
                "selective_scan_u_dtype": str(u.dtype),
                "selective_scan_delta_dtype": str(delta.dtype),
                "selective_scan_a_dtype": str(a.dtype),
                "selective_scan_b_dtype": str(b_param.dtype),
                "selective_scan_c_dtype": str(c_param.dtype),
                "selective_scan_d_dtype": str(d_skip.dtype),
                "selective_scan_delta_bias_dtype": str(delta_bias.dtype),
            }
        )
        use_cuda = self.backend in {"auto", "cuda"} and u.is_cuda
        if self.backend == "cuda" and not u.is_cuda:
            raise RuntimeError("backend='cuda' requires CUDA input tensors")
        if self.backend == "cuda" and _mamba_selective_scan_fn is None:
            raise RuntimeError(f"mamba-ssm selective_scan_fn is unavailable: {_MAMBA_IMPORT_ERROR}")

        if use_cuda and _mamba_selective_scan_fn is not None:
            try:
                output = _mamba_selective_scan_fn(
                    u,
                    delta,
                    a,
                    b_param,
                    c_param,
                    d_skip,
                    z=None,
                    delta_bias=delta_bias,
                    delta_softplus=True,
                    return_last_state=False,
                )
                self.last_backend = "cuda"
                self.backend_reason = None
                output = output[0] if isinstance(output, tuple) else output
                self.last_dtype_trace["selective_scan_output_dtype"] = str(output.dtype)
                return output
            except Exception as error:
                message = f"{type(error).__name__}: {error}"
                if self.backend == "cuda":
                    raise RuntimeError(f"mamba-ssm CUDA selective scan failed: {message}") from error
                self.backend_reason = message
                if not self._warned_fast_failure:
                    warnings.warn(
                        f"mamba-ssm CUDA selective scan failed; using the PyTorch reference fallback. {message}",
                        RuntimeWarning,
                        stacklevel=2,
                    )
                    self._warned_fast_failure = True
        elif self.backend == "auto":
            self.backend_reason = (
                "input is not CUDA" if not u.is_cuda else f"mamba-ssm unavailable: {_MAMBA_IMPORT_ERROR}"
            )
            if u.is_cuda and _mamba_selective_scan_fn is None and not self._warned_fast_failure:
                warnings.warn(
                    f"mamba-ssm is unavailable; using the PyTorch reference fallback. {_MAMBA_IMPORT_ERROR}",
                    RuntimeWarning,
                    stacklevel=2,
                )
                self._warned_fast_failure = True

        self.last_backend = "torch"
        output = self._selective_scan_torch(u, delta, a, b_param, c_param, d_skip, delta_bias)
        self.last_dtype_trace["selective_scan_output_dtype"] = str(output.dtype)
        return output

    def _ss2d(self, x: torch.Tensor) -> torch.Tensor:
        """Apply four-direction selective scan to an NCHW feature map."""
        batch, _, h, w = x.shape
        xs = self._cross_scan(x)
        projected = torch.einsum("bkdl,kcd->bkcl", xs, self.x_proj_weight)
        dts, b_param, c_param = torch.split(projected, (self.dt_rank, self.d_state, self.d_state), dim=2)
        dts = torch.einsum("bkrl,kdr->bkdl", dts, self.dt_proj_weight)

        u = xs.reshape(batch, self.scans * self.d_inner, h * w).contiguous()
        delta = dts.reshape(batch, self.scans * self.d_inner, h * w).contiguous()
        a = -torch.exp(self.A_logs.float())
        d_skip = self.Ds.float()
        delta_bias = self.dt_proj_bias.float().reshape(-1)
        y = self._run_selective_scan(u, delta, a, b_param.contiguous(), c_param.contiguous(), d_skip, delta_bias)
        self.last_dtype_trace.update(
            {
                "ss2d_projected_dtype": str(projected.dtype),
                "ss2d_dt_dtype": str(dts.dtype),
                "ss2d_merged_scan_dtype": str(y.dtype),
            }
        )
        y = y.view(batch, self.scans, self.d_inner, h * w)
        return self._cross_merge(y, h, w).view(batch, self.d_inner, h, w)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Return an identity-preserving partial feature refinement."""
        if x.ndim != 4 or x.shape[1] != self.channels:
            raise ValueError(f"Expected NCHW input with {self.channels} channels, got shape {tuple(x.shape)}")
        try:
            outer_autocast_enabled = bool(torch.is_autocast_enabled(x.device.type))
        except TypeError:
            outer_autocast_enabled = bool(torch.is_autocast_enabled())
        force_fp32 = bool(getattr(self, "vss_force_fp32", False))
        self.last_dtype_trace = {
            "vss_force_fp32": force_fp32,
            "outer_autocast_enabled": outer_autocast_enabled,
            "input_dtype": str(x.dtype),
        }

        residual = x
        if force_fp32:
            non_fp32_parameters = [
                name
                for name, parameter in self.named_parameters()
                if parameter.is_floating_point() and parameter.dtype != torch.float32
            ]
            if non_fp32_parameters:
                raise RuntimeError(
                    "vss_force_fp32 requires FP32 master parameters; non-FP32 parameters: "
                    + ", ".join(non_fp32_parameters)
                )
            with torch.autocast(device_type=x.device.type, enabled=False):
                x = self.in_norm(x.float().permute(0, 2, 3, 1))
                x, gate = self.in_proj(x).chunk(2, dim=-1)
                x = self.activation(self.dwconv(x.permute(0, 3, 1, 2).contiguous()))
                x = self._ss2d(x).permute(0, 2, 3, 1)
                x = self.out_proj(self.out_norm(x) * F.silu(gate)).permute(0, 3, 1, 2).contiguous()
                branch_fp32_dtype = str(x.dtype)
            x = x.to(dtype=residual.dtype)
            branch_cast_dtype = str(x.dtype)
            with torch.autocast(device_type=x.device.type, enabled=False):
                output = residual.float() + self.gamma.float() * self.drop_path(x.float())
            output = output.to(dtype=residual.dtype)
            self.last_dtype_trace.update(
                {
                    "island_compute_dtype": branch_fp32_dtype,
                    "branch_dtype_before_residual": branch_cast_dtype,
                    "residual_fusion_compute_dtype": "torch.float32",
                    "output_dtype": str(output.dtype),
                }
            )
            return output

        x = self.in_norm(x.permute(0, 2, 3, 1))
        x, gate = self.in_proj(x).chunk(2, dim=-1)
        x = self.activation(self.dwconv(x.permute(0, 3, 1, 2).contiguous()))
        x = self._ss2d(x).permute(0, 2, 3, 1)
        x = self.out_proj(self.out_norm(x) * F.silu(gate)).permute(0, 3, 1, 2).contiguous()
        output = residual + self.gamma * self.drop_path(x)
        self.last_dtype_trace.update(
            {
                "island_compute_dtype": None,
                "branch_dtype_before_residual": str(x.dtype),
                "residual_fusion_compute_dtype": str(output.dtype),
                "output_dtype": str(output.dtype),
            }
        )
        return output


class C3k2VSS(C3k2):
    """State-dict-compatible C3k2 followed by partial-channel VSS output refinement."""

    def __init__(
        self,
        c1: int,
        c2: int,
        n: int = 1,
        c3k: bool = False,
        e: float = 0.5,
        attn: bool = False,
        g: int = 1,
        shortcut: bool = True,
        vss_cfg: dict[str, Any] | None = None,
    ):
        """Initialize the unchanged C3k2 path and append only a new ``vss`` submodule."""
        super().__init__(c1, c2, n, c3k, e, attn, g, shortcut)
        cfg = dict(vss_cfg or {})
        ratio = float(cfg.pop("ratio", 0.5))
        dim_cap = int(cfg.pop("dim_cap", c2))
        if not 0.0 < ratio < 1.0:
            raise ValueError(f"VSS partial ratio must be in (0, 1), got {ratio}")
        vss_channels = int(math.ceil(min(c2 * ratio, dim_cap) / 8) * 8)
        vss_channels = min(vss_channels, c2 - 8)
        if not 8 <= vss_channels < c2:
            raise ValueError(f"Invalid partial VSS width {vss_channels} for C3k2 output channels {c2}")

        gamma_init = float(cfg.pop("gamma", cfg.pop("gamma_init", 1e-3)))
        self.vss_channels = vss_channels
        self.identity_channels = c2 - vss_channels
        self.vss = PartialVSSRefine(vss_channels, gamma_init=gamma_init, **cfg)

    @property
    def last_backend(self) -> str | None:
        """Return the selective scan backend executed by the latest forward."""
        return self.vss.last_backend

    def _refine_output(self, z: torch.Tensor) -> torch.Tensor:
        """Keep leading channels untouched and refine only the configured trailing channels."""
        identity, vss_part = torch.split(z, (self.identity_channels, self.vss_channels), dim=1)
        return torch.cat((identity, self.vss(vss_part)), dim=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Run the complete pretrained-compatible C3k2 path before partial VSS refinement."""
        return self._refine_output(super().forward(x))

    def forward_split(self, x: torch.Tensor) -> torch.Tensor:
        """Run C2f's split-based path before the same partial VSS refinement."""
        return self._refine_output(super().forward_split(x))
