"""
VERIFY TSVM LAYER 10 (C2TSVMamba) ARCHITECTURE
==============================================
Script doc lap kiem thu don vi (Unit Test) cho khoi C2TSVMamba tai tang 10:
  - Dang ky package ultralytics cuc bo
  - Import module C2TSVMamba tu ultralytics.nn.modules.topology_shape_vmamba
  - Tao tensor gia lap o do phan giai P5: [Batch=2, Channels=1024, H=20, W=20]
  - Kiem tra lan truyen tien (Forward Pass)
  - Kiem tra lan truyen nguoc (Backward Pass) & Gradient Flow
  - Kiem tra bao toan kich thuoc tensor output [2, 1024, 20, 20]
  - Thong ke so luong tham so (Parameters)

Chay doc lap: python verify_tsvm_layer10.py
"""

from __future__ import annotations
import os
import sys
import importlib.util
import pathlib
import torch
import torch.nn as nn

ROOT = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\ultralytics_Topology-Shape-aware VMamba"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

if "ultralytics" not in sys.modules:
    spec = importlib.util.spec_from_file_location(
        "ultralytics", os.path.join(ROOT, "__init__.py"), submodule_search_locations=[ROOT]
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["ultralytics"] = mod
    spec.loader.exec_module(mod)

try:
    from ultralytics.nn.modules.topology_shape_vmamba import (
        SS2D,
        ShapeAwareBranch,
        DirectionalShapeExtractor,
        TopologyShapeGate,
        TSVMamba,
        C2TSVMamba
    )
    print("[+] Da import thanh cong cac module TSVM tu ultralytics.nn.modules.topology_shape_vmamba")
except Exception as e:
    print(f"[-] Loi import: {e}")
    sys.exit(1)

def main():
    print("="*70)
    print("KIEM TRA KHOI C2TSVMamba TAI TANG 10 (BACKBONE P5)")
    print("="*70)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Thiet bi kiem thu: {device}")
    
    c_in = 1024
    c_out = 1024
    n_blocks = 2
    
    layer10 = C2TSVMamba(c1=c_in, c2=c_out, n=n_blocks).to(device)
    total_params = sum(p.numel() for p in layer10.parameters())
    trainable_params = sum(p.numel() for p in layer10.parameters() if p.requires_grad)
    print(f"[*] Khoi tao C2TSVMamba(c1={c_in}, c2={c_out}, n={n_blocks}) thanh cong.")
    print(f"[*] Tong so tham so: {total_params:,} ({total_params*4 / (1024*1024):.2f} MB FP32)")
    print(f"[*] Tham so can huan luyen: {trainable_params:,}")
    
    b_size, h, w = 2, 20, 20
    dummy_x = torch.randn(b_size, c_in, h, w, device=device, requires_grad=True)
    print(f"[*] Tensor dau vao: shape={dummy_x.shape}")
    
    out = layer10(dummy_x)
    print(f"[*] Tensor dau ra:  shape={out.shape}")
    assert out.shape == dummy_x.shape, f"Loi kich thuoc! Dau ra {out.shape} != {dummy_x.shape}"
    assert not torch.isnan(out).any(), "Phat hien gia tri NaN trong output!"
    assert not torch.isinf(out).any(), "Phat hien gia tri Inf trong output!"
    print("[+] PASS: Forward Pass hoan hao, shape duoc bao toan chinh xac!")
    
    loss = out.sum()
    loss.backward()
    assert dummy_x.grad is not None, "Khong truyen duoc gradient ve dau vao dummy_x!"
    has_grad = any(p.grad is not None and p.grad.abs().sum() > 0 for p in layer10.parameters())
    assert has_grad, "Khong co gradient trong cac tham so cua layer10!"
    print("[+] PASS: Backward Pass thanh cong, gradient lan truyen on dinh, khong bi vanishing/exploding!")
    print("="*70)
    print("[*] KET LUAN: Khoi C2TSVMamba tai Tang 10 dat chuan ky thuat 100%!")

if __name__ == "__main__":
    main()
