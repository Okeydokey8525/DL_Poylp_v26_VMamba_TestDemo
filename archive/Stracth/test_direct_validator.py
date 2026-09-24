import sys, os
from pathlib import Path

repo_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\ultralytics_Topology-Shape-aware VMamba"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

import torch
# Make sure we import from custom repo
import ultralytics
print("Imported ultralytics from:", ultralytics.__file__)

from ultralytics.models.yolo.segment import SegmentationValidator
from ultralytics.nn.tasks import load_checkpoint

ckpt_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2\weights\best.pt"
data_yaml = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\data_bg20.yaml"

# 1. Load model WITHOUT fusing
model, _ = load_checkpoint(ckpt_path, device=torch.device('cpu'), fuse=False)
model.eval()

# 2. Disable end2end so it routes to one2many head with NMS
for m in model.modules():
    if hasattr(m, "end2end"):
        m.end2end = False

# 3. Create validator with args
args = dict(
    data=data_yaml,
    batch=4,
    imgsz=640,
    device="cpu",
    plots=False,
    split="val",
    half=False,
    conf=0.001,
    iou=0.7,
    max_det=300,
    task="segment",
    mode="val",
    save_dir=Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\test_val_run")
)
validator = SegmentationValidator(args=args)

# 4. In validator, prevent AutoBackend from fusing
from ultralytics.nn import autobackend
orig_autobackend_init = autobackend.AutoBackend.__init__
def patched_init(self, *a, **kw):
    kw['fuse'] = False
    return orig_autobackend_init(self, *a, **kw)
autobackend.AutoBackend.__init__ = patched_init

metrics = validator(model=model)
print("=== VALIDATION RESULTS (TSVM Seed 5 - ONE-TO-MANY HEAD) ===")
print("Mask mAP50:", validator.metrics.seg.map50)
print("Mask mAP50-95:", validator.metrics.seg.map)
print("Box mAP50:", validator.metrics.box.map50)
print("Box mAP50-95:", validator.metrics.box.map)
