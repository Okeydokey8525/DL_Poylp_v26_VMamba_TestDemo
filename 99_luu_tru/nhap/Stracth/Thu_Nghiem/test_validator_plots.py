import sys, os
from pathlib import Path

repo_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\ultralytics_Topology-Shape-aware VMamba"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

import torch
import ultralytics
from ultralytics.models.yolo.segment import SegmentationValidator
from ultralytics.nn import autobackend

test_dir = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\test_val_plots")
test_dir.mkdir(parents=True, exist_ok=True)

# Patch AutoBackend to NEVER fuse and to disable end2end
orig_init = autobackend.AutoBackend.__init__
def patched_init(self, model="yolo26n.pt", device=None, dnn=False, data=None, fp16=False, fuse=True, verbose=True):
    orig_init(self, model=model, device=device, dnn=dnn, data=data, fp16=fp16, fuse=False, verbose=verbose)
    if hasattr(self.model, "model"):
        head = self.model.model[-1]
        head._end2end = False
    self.end2end = False

autobackend.AutoBackend.__init__ = patched_init

ckpt_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2\weights\best.pt"
data_yaml = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\data_bg20.yaml"

args = dict(
    model=ckpt_path,
    data=data_yaml,
    batch=8,
    imgsz=640,
    device="cpu",
    plots=True,
    split="val",
    half=False,
    conf=0.001,
    iou=0.7,
    max_det=300,
    task="segment",
    mode="val",
    save_dir=test_dir,
    project=str(test_dir.parent),
    name=test_dir.name,
    exist_ok=True,
)

validator = SegmentationValidator(args=args)

# Hook into validator to force validator.end2end = False after model init
orig_init_metrics = validator.init_metrics
def patched_init_metrics(m):
    orig_init_metrics(m)
    validator.end2end = False
validator.init_metrics = patched_init_metrics

metrics = validator(model=ckpt_path)

print("=== Validation Finished Successfully! ===")
print("Mask mAP50:", validator.metrics.seg.map50)
print("Mask mAP50-95:", validator.metrics.seg.map)
print("Box mAP50:", validator.metrics.box.map50)
print("Box mAP50-95:", validator.metrics.box.map)
print("\nGenerated files in test_dir:")
for f in sorted(os.listdir(test_dir)):
    print(" -", f)
