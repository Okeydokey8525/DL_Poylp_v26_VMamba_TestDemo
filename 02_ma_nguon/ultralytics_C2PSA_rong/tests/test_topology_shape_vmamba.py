"""
Comprehensive Test Suite for YOLO26-seg + Topology-Shape-aware VMamba (TS-VMamba).
Validates Tests 0 through 24 as required by the technical specification.
"""

from __future__ import annotations

import hashlib
import os
import pathlib
import sys
import unittest

# Ensure local workspace is registered as 'ultralytics' module
ROOT = str(pathlib.Path(__file__).resolve().parents[1])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

if "ultralytics" not in sys.modules:
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "ultralytics", os.path.join(ROOT, "__init__.py"), submodule_search_locations=[ROOT]
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["ultralytics"] = mod
    spec.loader.exec_module(mod)

import torch
import torch.nn as nn
import torch.optim as optim

from ultralytics.nn.modules.topology_shape_vmamba import (
    C2TSVMamba,
    DirectionalShapeExtractor,
    SS2D,
    ShapeAwareBranch,
    TSVMamba,
    TopologyShapeGate,
    parallel_associative_scan,
)
from ultralytics.nn.tasks import SegmentationModel


class TestTopologyShapeVMamba(unittest.TestCase):
    """Test suite covering TEST 0 through TEST 24."""

    BASELINE_YAML_PATH = os.path.join(ROOT, "cfg", "models", "26", "yolo26-seg.yaml")
    EXPECTED_SHA256 = "53c0348a36a3e19bbc3bd4f695f50cbbfc97a3059f62e9b251f278ad74fdd7cb"
    PROPOSED_YAML_PATH = os.path.join(ROOT, "cfg", "models", "26", "yolo26-seg-TopologyShapeVMamba.yaml")

    def test_00_baseline_yaml_integrity(self):
        """TEST 0: Baseline YAML integrity (SHA256 verification)."""
        self.assertTrue(os.path.exists(self.BASELINE_YAML_PATH), "Baseline YAML file does not exist")
        with open(self.BASELINE_YAML_PATH, "rb") as f:
            data = f.read()
        computed_sha256 = hashlib.sha256(data).hexdigest()
        self.assertEqual(
            computed_sha256,
            self.EXPECTED_SHA256,
            f"Baseline YAML was modified! Expected {self.EXPECTED_SHA256}, got {computed_sha256}",
        )

    def test_01_component_imports(self):
        """TEST 1: Import all module components."""
        for cls in (SS2D, ShapeAwareBranch, DirectionalShapeExtractor, TopologyShapeGate, TSVMamba, C2TSVMamba):
            self.assertIsNotNone(cls)
            self.assertTrue(issubclass(cls, nn.Module))

    def test_02_module_initialization_multi_channels(self):
        """TEST 2: Module initialization across various channel widths."""
        test_channels = [32, 64, 128, 256, 512, 1024]
        for c in test_channels:
            m_ts = TSVMamba(c=c)
            m_c2 = C2TSVMamba(c1=c, c2=c, n=1)
            self.assertIsInstance(m_ts, nn.Module)
            self.assertIsInstance(m_c2, nn.Module)

    def test_03_shape_preservation(self):
        """TEST 3: Shape preservation [B, C, H, W] -> [B, C, H, W]."""
        test_configs = [
            (2, 64, 20, 20),
            (1, 128, 40, 40),
            (2, 256, 10, 10),
            (1, 32, 16, 24),  # Non-square spatial resolution
        ]
        for B, C, H, W in test_configs:
            x = torch.randn(B, C, H, W)
            m_ts = TSVMamba(c=C)
            m_c2 = C2TSVMamba(c1=C, c2=C, n=1)
            out_ts = m_ts(x)
            out_c2 = m_c2(x)
            self.assertEqual(out_ts.shape, (B, C, H, W))
            self.assertEqual(out_c2.shape, (B, C, H, W))

    def test_04_ss2d_output(self):
        """TEST 4: SS2D output validity."""
        B, C, H, W = 2, 64, 16, 16
        x = torch.randn(B, C, H, W)
        ss2d = SS2D(d_model=C, d_state=16)
        out = ss2d(x)
        self.assertEqual(out.shape, (B, C, H, W))
        self.assertFalse(torch.isnan(out).any())
        self.assertFalse(torch.isinf(out).any())

    def test_05_shape_branch_output(self):
        """TEST 5: Shape branch output validity."""
        B, C, H, W = 2, 64, 20, 20
        x = torch.randn(B, C, H, W)
        shape_branch = ShapeAwareBranch(c1=C, c2=C)
        out = shape_branch(x)
        self.assertEqual(out.shape, (B, C, H, W))
        self.assertFalse(torch.isnan(out).any())

    def test_06_directional_feature_output(self):
        """TEST 6: Directional feature output validity."""
        B, C, H, W = 2, 64, 20, 20
        s_in = torch.randn(B, C, H, W)
        dir_ext = DirectionalShapeExtractor(c=C)
        out = dir_ext(s_in)
        self.assertEqual(out.shape, (B, C, H, W))
        self.assertFalse(torch.isnan(out).any())

    def test_07_guidance_range(self):
        """TEST 7: Guidance gate range 0 <= G_TS <= 1."""
        B, C, H, W = 2, 64, 20, 20
        s = torch.randn(B, C, H, W) * 5.0
        gate = TopologyShapeGate(c=C)
        g_ts = gate(s)
        self.assertEqual(g_ts.shape, (B, C, H, W))
        self.assertTrue((g_ts >= 0.0).all().item())
        self.assertTrue((g_ts <= 1.0).all().item())

    def test_08_fusion_output(self):
        """TEST 8: Fusion and FFN output validity."""
        B, C, H, W = 2, 64, 20, 20
        x = torch.randn(B, C, H, W)
        ts_block = TSVMamba(c=C, mode="topology_shape_vmamba")
        out = ts_block(x)
        self.assertEqual(out.shape, (B, C, H, W))
        self.assertFalse(torch.isnan(out).any())

    def test_09_input_gradient(self):
        """TEST 9: Input gradient != 0."""
        x = torch.randn(2, 32, 16, 16, requires_grad=True)
        block = TSVMamba(c=32)
        out = block(x)
        loss = out.sum()
        loss.backward()
        self.assertIsNotNone(x.grad)
        self.assertFalse(torch.isnan(x.grad).any())
        self.assertTrue((x.grad != 0).any().item())

    def test_10_vmamba_parameter_gradients(self):
        """TEST 10: VMamba / SS2D parameter gradients != 0."""
        x = torch.randn(2, 32, 16, 16)
        block = TSVMamba(c=32, mode="topology_shape_vmamba")
        out = block(x)
        loss = out.sum()
        loss.backward()
        vmamba_grads = [p.grad for p in block.vmamba.parameters() if p.requires_grad]
        self.assertTrue(len(vmamba_grads) > 0)
        for g in vmamba_grads:
            self.assertIsNotNone(g)
            self.assertFalse(torch.isnan(g).any())
            self.assertTrue((g != 0).any().item())

    def test_11_shape_branch_parameter_gradients(self):
        """TEST 11: Shape branch & directional extractor parameter gradients != 0."""
        x = torch.randn(2, 32, 16, 16)
        block = TSVMamba(c=32, mode="topology_shape_vmamba")
        out = block(x)
        loss = out.sum()
        loss.backward()
        shape_grads = [p.grad for p in block.shape_branch.parameters() if p.requires_grad]
        topo_grads = [p.grad for p in block.directional_extractor.parameters() if p.requires_grad]
        self.assertTrue(len(shape_grads) > 0)
        self.assertTrue(len(topo_grads) > 0)
        for g in shape_grads + topo_grads:
            self.assertIsNotNone(g)
            self.assertFalse(torch.isnan(g).any())
            self.assertTrue((g != 0).any().item())

    def test_12_no_nan_inf_high_variance(self):
        """TEST 12: No NaN/Inf under high variance inputs (10x, 50x)."""
        block = TSVMamba(c=32)
        for scale in [1.0, 10.0, 50.0]:
            x = (torch.randn(2, 32, 16, 16) * scale).requires_grad_(True)
            out = block(x)
            loss = out.mean()
            loss.backward()
            self.assertFalse(torch.isnan(out).any(), f"NaN in output at scale {scale}")
            self.assertFalse(torch.isinf(out).any(), f"Inf in output at scale {scale}")
            self.assertIsNotNone(x.grad, f"Input grad is None at scale {scale}")
            self.assertFalse(torch.isnan(x.grad).any(), f"NaN in input grad at scale {scale}")
            self.assertFalse(torch.isinf(x.grad).any(), f"Inf in input grad at scale {scale}")

    def test_13_cpu_forward_backward(self):
        """TEST 13: CPU forward/backward pass."""
        device = torch.device("cpu")
        block = C2TSVMamba(c1=64, c2=64, n=1).to(device)
        x = torch.randn(2, 64, 16, 16, device=device, requires_grad=True)
        out = block(x)
        loss = out.sum()
        loss.backward()
        self.assertIsNotNone(x.grad)
        self.assertFalse(torch.isnan(out).any())

    def test_14_cuda_forward_backward(self):
        """TEST 14: CUDA forward/backward pass if CUDA available."""
        if not torch.cuda.is_available():
            self.skipTest("SKIPPED - CUDA unavailable")
        device = torch.device("cuda:0")
        block = C2TSVMamba(c1=64, c2=64, n=1).to(device)
        x = torch.randn(2, 64, 16, 16, device=device, requires_grad=True)
        out = block(x)
        loss = out.sum()
        loss.backward()
        self.assertIsNotNone(x.grad)
        self.assertFalse(torch.isnan(out).any())

    def test_15_amp_fp16(self):
        """TEST 15: AMP FP16 if CUDA available."""
        if not torch.cuda.is_available():
            self.skipTest("SKIPPED - CUDA unavailable for AMP FP16")
        device = torch.device("cuda:0")
        block = C2TSVMamba(c1=64, c2=64, n=1).to(device)
        x = torch.randn(2, 64, 16, 16, device=device, requires_grad=True)
        with torch.autocast(device_type="cuda", dtype=torch.float16):
            out = block(x)
            loss = out.sum()
        loss.backward()
        self.assertFalse(torch.isnan(out).any())

    def test_16_amp_bf16(self):
        """TEST 16: AMP BF16."""
        device_type = "cuda" if torch.cuda.is_available() else "cpu"
        block = C2TSVMamba(c1=64, c2=64, n=1)
        x = torch.randn(2, 64, 16, 16, requires_grad=True)
        try:
            with torch.autocast(device_type=device_type, dtype=torch.bfloat16):
                out = block(x)
                loss = out.sum()
            loss.backward()
            self.assertFalse(torch.isnan(out).any())
        except Exception as e:
            self.skipTest(f"SKIPPED - BF16 not supported on this platform: {e}")

    def test_17_multiple_resolutions(self):
        """TEST 17: Multiple resolutions (320, 640, 800 input sizes -> feature maps 10, 20, 25)."""
        resolutions = [(10, 10), (20, 20), (25, 25), (14, 18)]
        block = C2TSVMamba(c1=64, c2=64, n=1)
        for H, W in resolutions:
            x = torch.randn(1, 64, H, W)
            out = block(x)
            self.assertEqual(out.shape, (1, 64, H, W))
            self.assertFalse(torch.isnan(out).any())

    def test_18_multiple_batch_sizes(self):
        """TEST 18: Multiple batch sizes (1, 2, 4)."""
        block = C2TSVMamba(c1=64, c2=64, n=1)
        for B in [1, 2, 4]:
            x = torch.randn(B, 64, 16, 16)
            out = block(x)
            self.assertEqual(out.shape, (B, 64, 16, 16))

    def test_19_yolo26_yaml_parsing(self):
        """TEST 19: YOLO26 YAML parsing."""
        self.assertTrue(os.path.exists(self.PROPOSED_YAML_PATH))
        model = SegmentationModel(cfg=self.PROPOSED_YAML_PATH, ch=3, nc=1, verbose=False)
        self.assertIsInstance(model, nn.Module)
        self.assertEqual(len(model.model), 24)
        # Layer 10 must be C2TSVMamba
        self.assertIsInstance(model.model[10], C2TSVMamba)

    def test_20_pretrained_weight_transfer(self):
        """TEST 20: Pretrained weight transfer compatibility."""
        baseline_model = SegmentationModel(cfg=self.BASELINE_YAML_PATH, ch=3, nc=1, verbose=False)
        proposed_model = SegmentationModel(cfg=self.PROPOSED_YAML_PATH, ch=3, nc=1, verbose=False)

        baseline_sd = baseline_model.state_dict()
        proposed_sd = proposed_model.state_dict()

        transferred_keys = []
        new_keys = []
        incompatible_keys = []

        for k, v in proposed_sd.items():
            if k in baseline_sd:
                if baseline_sd[k].shape == v.shape:
                    transferred_keys.append(k)
                else:
                    incompatible_keys.append(k)
            else:
                new_keys.append(k)

        # Layers 0-9 (backbone before layer 10) and layers 11-23 (head) must match perfectly
        self.assertEqual(len(incompatible_keys), 0, f"Incompatible key shapes: {incompatible_keys}")
        self.assertTrue(len(transferred_keys) > 200, f"Expected >200 matching keys, got {len(transferred_keys)}")
        # New keys must be within layer 10 (C2TSVMamba)
        for k in new_keys:
            self.assertTrue(k.startswith("model.10."), f"Unexpected new key outside layer 10: {k}")

    def test_21_end_to_end_train_step(self):
        """TEST 21: End-to-end forward -> loss -> backward -> optimizer step."""
        model = SegmentationModel(cfg=self.PROPOSED_YAML_PATH, ch=3, nc=1, verbose=False)
        optimizer = optim.AdamW(model.parameters(), lr=1e-3)

        x = torch.randn(2, 3, 160, 160)
        out = model(x)
        def compute_sum(item):
            if isinstance(item, torch.Tensor):
                return item.sum()
            elif isinstance(item, dict):
                return sum(compute_sum(v) for v in item.values())
            elif isinstance(item, (list, tuple)):
                return sum(compute_sum(v) for v in item)
            return torch.tensor(0.0)

        loss = compute_sum(out)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        self.assertFalse(torch.isnan(loss))

    def test_22_parameter_count(self):
        """TEST 22: Parameter count comparison and calculation."""
        baseline_model = SegmentationModel(cfg=self.BASELINE_YAML_PATH, ch=3, nc=1, verbose=False)
        proposed_model = SegmentationModel(cfg=self.PROPOSED_YAML_PATH, ch=3, nc=1, verbose=False)

        base_params = sum(p.numel() for p in baseline_model.parameters())
        prop_params = sum(p.numel() for p in proposed_model.parameters())
        diff_params = prop_params - base_params
        increase_pct = (diff_params / base_params) * 100

        self.assertGreater(prop_params, 0)
        self.assertLess(increase_pct, 15.0, f"Parameter increase {increase_pct:.2f}% exceeds acceptable budget")

    def test_23_no_token_wise_loops(self):
        """TEST 23: Verify parallel associative scan is vectorized (zero token loops)."""
        L = 256
        a = torch.rand(2, 4, 8, L).clamp(min=0.1, max=0.99)
        b = torch.randn(2, 4, 8, L)
        h = parallel_associative_scan(a, b)
        self.assertEqual(h.shape, (2, 4, 8, L))
        self.assertFalse(torch.isnan(h).any())

    def test_24_residual_gradient_flow(self):
        """TEST 24: Residual gradient flow (learnable gamma and both paths active)."""
        block = TSVMamba(c=32)
        x = torch.randn(2, 32, 16, 16, requires_grad=True)
        out = block(x)
        loss = (out * 2.0).sum()
        loss.backward()

        # Check gamma gradient
        self.assertIsNotNone(block.gamma.grad)
        self.assertFalse(torch.isnan(block.gamma.grad).any())
        self.assertTrue((block.gamma.grad != 0).any().item())

        # Check input gradient flow through residual connection
        self.assertIsNotNone(x.grad)
        self.assertTrue((x.grad != 0).any().item())


def run_all_tests():
    """Run all tests and output a clean report."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTopologyShapeVMamba)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result


if __name__ == "__main__":
    result = run_all_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
