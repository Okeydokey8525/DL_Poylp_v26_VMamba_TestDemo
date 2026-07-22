# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""
Weight transfer and verification utilities for YOLO26-VMamba-seg models.
"""

import re
from pathlib import Path
import torch
import torch.nn as nn

from ultralytics.engine.model import Model
from ultralytics.models.yolo.model import YOLO
from ultralytics.utils import DEFAULT_CFG_DICT, ROOT, callbacks
from ultralytics.utils.patches import torch_load
from ultralytics.nn.tasks import yaml_model_load


def build_yolo26_vmamba_seg(
    scale: str,
    pretrained=None,
    nc: int = 1,
) -> tuple[YOLO, dict]:
    """Build a YOLO26-VMamba-seg model for a specific scale and transfer pretrained baseline weights.

    Args:
        scale (str): Model compound scale ('n', 's', 'm', 'l', or 'x').
        pretrained (str | Path | bool | None, optional): Path to pretrained baseline checkpoint or None for auto-selection.
        nc (int): Number of target classes.

    Returns:
        (tuple):
            YOLO: Initialized YOLO instance with transferred weights.
            dict: Detailed transfer report dictionary.
    """
    if scale not in {"n", "s", "m", "l", "x"}:
        raise ValueError(f"Invalid scale '{scale}'. Must be one of 'n', 's', 'm', 'l', 'x'.")

    if pretrained is None:
        pretrained = f"yolo26{scale}-seg.pt"

    yaml_path = ROOT / "cfg" / "models" / "26" / "yolo26-vmamba-seg.yaml"
    cfg_dict = yaml_model_load(yaml_path)
    cfg_dict["scale"] = scale
    cfg_dict["nc"] = nc
    cfg_dict["yaml_file"] = str(yaml_path)

    # Instantiate YOLO model without triggering scale fallback warning
    yolo = YOLO.__new__(YOLO)
    super(Model, yolo).__init__()
    yolo.callbacks = callbacks.get_default_callbacks()
    yolo.predictor = None
    yolo.model = None
    yolo.trainer = None
    yolo.ckpt = {}
    yolo.cfg = str(yaml_path)
    yolo.ckpt_path = None
    yolo.overrides = {}
    yolo.metrics = None
    yolo.session = None
    yolo.task = "segment"
    yolo.model_name = str(yaml_path)

    yolo.model = yolo._smart_load("model")(cfg_dict, verbose=False)
    yolo.overrides["model"] = yolo.cfg
    yolo.overrides["task"] = yolo.task
    yolo.overrides["scale"] = scale
    yolo.model.args = {**DEFAULT_CFG_DICT, **yolo.overrides}
    yolo.model.task = yolo.task

    report = {
        "scale": scale,
        "pretrained": str(pretrained) if pretrained is not False and pretrained is not None else None,
        "direct_loaded": 0,
        "shifted_loaded": 0,
        "vmamba_random": 0,
        "expected_nc_mismatch": 0,
        "unexpected_mismatch": 0,
        "missing_source": 0,
        "total_target_tensors": 0,
        "total_transferred": 0,
        "segment26_transferred": 0,
    }

    target_state_dict = yolo.model.state_dict()
    report["total_target_tensors"] = len(target_state_dict)

    if pretrained and pretrained is not False:
        ckpt = torch_load(pretrained, map_location="cpu")
        if isinstance(ckpt, dict) and "model" in ckpt:
            src_model = ckpt["model"]
            if hasattr(src_model, "state_dict"):
                source_state_dict = src_model.float().state_dict()
            elif isinstance(src_model, dict):
                source_state_dict = {k: v.float() if isinstance(v, torch.Tensor) else v for k, v in src_model.items()}
            else:
                source_state_dict = ckpt.state_dict()
        elif hasattr(ckpt, "state_dict"):
            source_state_dict = ckpt.state_dict()
        elif isinstance(ckpt, dict):
            source_state_dict = ckpt
        else:
            raise ValueError(f"Unsupported checkpoint format in {pretrained}")

        # Verify scale compatibility
        for k in ["model.0.conv.weight", "model.1.conv.weight", "model.2.cv1.conv.weight"]:
            if k in target_state_dict and k in source_state_dict:
                if target_state_dict[k].shape != source_state_dict[k].shape:
                    raise ValueError(
                        f"Checkpoint scale mismatch: expected scale '{scale}' (target tensor {k} shape {target_state_dict[k].shape}), "
                        f"but checkpoint tensor has shape {source_state_dict[k].shape}."
                    )

        new_state_dict = {}
        for target_key, target_tensor in target_state_dict.items():
            match = re.match(r"^model\.(\d+)\.(.+)$", target_key)
            if not match:
                new_state_dict[target_key] = target_tensor
                continue

            layer_idx = int(match.group(1))
            sub_path = match.group(2)

            if layer_idx <= 10:
                source_layer_idx = layer_idx
            elif layer_idx == 11:
                # Target layer 11 is VMambaBlock: retain random initialization
                new_state_dict[target_key] = target_tensor
                report["vmamba_random"] += 1
                continue
            else:
                # Target layer 12-24 mapped from source layer 11-23
                source_layer_idx = layer_idx - 1

            source_key = f"model.{source_layer_idx}.{sub_path}"
            if source_key not in source_state_dict:
                report["missing_source"] += 1
                if layer_idx <= 23:
                    raise ValueError(f"Missing source tensor '{source_key}' for backbone/neck layer '{target_key}'.")
                new_state_dict[target_key] = target_tensor
                continue

            source_tensor = source_state_dict[source_key]
            if source_tensor.shape == target_tensor.shape:
                new_state_dict[target_key] = source_tensor
                if layer_idx <= 10:
                    report["direct_loaded"] += 1
                else:
                    report["shifted_loaded"] += 1
                    if layer_idx == 24:
                        report["segment26_transferred"] += 1
            else:
                if layer_idx == 24:
                    # Output head mismatch due to nc change
                    report["expected_nc_mismatch"] += 1
                    new_state_dict[target_key] = target_tensor
                else:
                    report["unexpected_mismatch"] += 1
                    if layer_idx <= 23:
                        raise ValueError(
                            f"Shape mismatch at backbone/neck layer '{target_key}': "
                            f"target {target_tensor.shape} vs source {source_tensor.shape} ({source_key})."
                        )
                    new_state_dict[target_key] = target_tensor

        report["total_transferred"] = report["direct_loaded"] + report["shifted_loaded"]
        yolo.model.load_state_dict(new_state_dict, strict=True)
    else:
        for target_key in target_state_dict:
            match = re.match(r"^model\.(\d+)\.(.+)$", target_key)
            if match and int(match.group(1)) == 11:
                report["vmamba_random"] += 1

    return yolo, report


def verify_vmamba_fast_path(
    model,
    device="cuda:0",
) -> dict:
    """Verify forward/backward passes of VMambaBlock on specified device and check fast CUDA path usage.

    Args:
        model (YOLO | nn.Module): YOLO model or PyTorch module.
        device (str | torch.device): Device string or torch.device.

    Returns:
        (dict): Verification report dictionary.
    """
    from ultralytics.nn.modules import VMambaBlock

    target_device = torch.device(device if torch.cuda.is_available() and "cuda" in str(device).lower() else "cpu")
    is_cuda_env = target_device.type == "cuda"

    net = model.model if hasattr(model, "model") else model
    if hasattr(net, "model") and isinstance(net.model, nn.Sequential):
        net = net.model

    vmamba_block = None
    block_index = -1
    for idx, m in enumerate(net.modules() if not isinstance(net, nn.Sequential) else net):
        if isinstance(m, VMambaBlock):
            vmamba_block = m
            if isinstance(net, nn.Sequential):
                block_index = idx
            break

    if vmamba_block is None:
        return {
            "block_found": False,
            "block_index": None,
            "channels": None,
            "device": str(target_device),
            "output_shape_match": False,
            "output_finite": False,
            "backward_finite": False,
            "fast_cuda_path_used": False,
            "status": "FAIL (VMambaBlock not found in model)",
        }

    c1 = getattr(vmamba_block, "c1", None)
    if c1 is None:
        c1 = vmamba_block.norm1.weight.shape[0]

    vmamba_block = vmamba_block.to(target_device)
    x = torch.randn(1, c1, 20, 20, device=target_device, dtype=torch.float32, requires_grad=True)

    out = vmamba_block(x)
    shape_match = out.shape == (1, c1, 20, 20)
    out_finite = bool(torch.isfinite(out).all().item())

    loss = out.sum()
    loss.backward()
    grad_finite = x.grad is not None and bool(torch.isfinite(x.grad).all().item())

    fast_path_used = getattr(vmamba_block, "last_forward_used_fast_path", False) and getattr(
        vmamba_block.ss2d, "last_forward_used_fast_path", False
    )

    if is_cuda_env:
        status = "PASS" if (shape_match and out_finite and grad_finite and fast_path_used) else "FAIL"
    else:
        status = "PENDING (Tested on CPU with PyTorch fallback; fast CUDA path unverified on CPU)"

    return {
        "block_found": True,
        "block_index": block_index,
        "channels": c1,
        "device": str(target_device),
        "output_shape_match": shape_match,
        "output_finite": out_finite,
        "backward_finite": grad_finite,
        "fast_cuda_path_used": bool(fast_path_used),
        "status": status,
    }
