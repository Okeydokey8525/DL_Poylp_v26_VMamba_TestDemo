import sys, os
from pathlib import Path

# Add custom repo to sys.path
repo_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\ultralytics_Topology-Shape-aware VMamba"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

import torch
from ultralytics import YOLO

ckpt = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2\weights\best.pt"
data_yaml = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\data_bg20.yaml"

print("Loading model...")
model = YOLO(ckpt)

# Check head
head = model.model.model[-1]
print(f"Head type: {type(head)}, end2end: {getattr(head, 'end2end', None)}")
print(f"cv2 exists: {head.cv2 is not None}, one2one_cv2 exists: {getattr(head, 'one2one_cv2', None) is not None}")

# Set end2end = False
head.end2end = False
for m in model.model.modules():
    if hasattr(m, "end2end"):
        m.end2end = False

print("Running quick test val (1 batch)...")
# Run val with half=False, batch=4
try:
    metrics = model.val(
        data=data_yaml,
        batch=4,
        imgsz=640,
        device="cpu",
        plots=False,
        split="val",
        half=False,
        max_det=300,
    )
    print("Val metrics successfully computed!")
    print(f"Mask mAP50: {metrics.seg.map50:.4f}, Box mAP50: {metrics.box.map50:.4f}")
except Exception as e:
    import traceback
    traceback.print_exc()
