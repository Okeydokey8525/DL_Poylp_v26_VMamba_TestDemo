"""
# ==============================================================================
# HƯỚNG DẪN & SCRIPT CHẠY VALIDATION TRÊN KAGGLE GPU ĐỂ XUẤT 24 ẢNH KẾT QUẢ CHUẨN
# Áp dụng cho: Kvasir_BG20_YOLO26s_seg_TSVM (Seed 0 & Seed 5)
# ==============================================================================
# Bối cảnh:
# Khi hoàn thành epoch 100, Ultralytics tự động gọi `model.fuse()`.
# Trong kiến trúc YOLO26 (Segment26), hàm `fuse()` sẽ xóa bỏ nhánh One-to-Many
# (`self.cv2 = self.cv3 = self.cv4 = None`) và ép dùng nhánh One-to-One.
# Do nhánh One-to-One ở Seed 5 chưa hội tụ, kết quả final eval bị suy sụp (mAP=0),
# dẫn tới các file PR curve trống và `val_batch2_pred.jpg` bị lỗi kéo giãn cột dọc.
#
# Script này ngăn chặn fuse và tắt cờ end2end để đánh giá trên đúng nhánh
# One-to-Many (nhánh có Mask mAP50 ~ 0.910 thực tế), xuất đủ 24 ảnh chuẩn.
# ==============================================================================
"""

import os, sys, shutil
from pathlib import Path

# 1. Khai báo repo custom và dataset
CUSTOM_REPO_PATH = "/kaggle/input/datasets/luong2005lam/ultralytics-topology-shape-aware-vmamba/ultralytics_Topology-Shape-aware VMamba"
DATASET_ROOT = "/kaggle/input/datasets/luong2005lam/kvasir-yolo-seg-bg20/Kvasir_YOLO_SEG_BG20"

if os.path.exists(CUSTOM_REPO_PATH) and CUSTOM_REPO_PATH not in sys.path:
    sys.path.insert(0, CUSTOM_REPO_PATH)

import torch
import PIL.ImageDraw
from ultralytics.utils.plotting import Annotator
import ultralytics.utils.plotting as p
from ultralytics.models.yolo.segment import SegmentationValidator
from ultralytics.nn import autobackend

# 2. Patch chống crash Pillow 10+ và đồng bộ luồng lưu ảnh
if hasattr(p.plot_images, "__closure__") and p.plot_images.__closure__:
    p.plot_images = p.plot_images.__closure__[0].cell_contents

orig_draw_rectangle = PIL.ImageDraw.ImageDraw.rectangle
def safe_rectangle(self, xy, fill=None, outline=None, width=1):
    try:
        if isinstance(xy, (list, tuple)) and len(xy) == 4:
            x0, y0, x1, y1 = xy
            xy = [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]
    except Exception:
        pass
    return orig_draw_rectangle(self, xy, fill=fill, outline=outline, width=width)
PIL.ImageDraw.ImageDraw.rectangle = safe_rectangle

orig_box_label = Annotator.box_label
def safe_box_label(self, box, label="", color=(128, 128, 128), **kwargs):
    try:
        if hasattr(box, "__len__") and len(box) == 4:
            b0, b1, b2, b3 = box
            box = [min(b0, b2), min(b1, b3), max(b0, b2), max(b1, b3)]
    except Exception:
        pass
    return orig_box_label(self, box, label=label, color=color, **kwargs)
Annotator.box_label = safe_box_label

# 3. Patch AutoBackend không fuse và kích hoạt nhánh One-to-Many
orig_init = autobackend.AutoBackend.__init__
def patched_init(self, model="yolo26n.pt", device=None, dnn=False, data=None, fp16=False, fuse=True, verbose=True):
    orig_init(self, model=model, device=device, dnn=dnn, data=data, fp16=fp16, fuse=False, verbose=verbose)
    if hasattr(self.model, "model"):
        head = self.model.model[-1]
        head._end2end = False
    self.end2end = False
autobackend.AutoBackend.__init__ = patched_init

def run_kaggle_eval(ckpt_path: str, output_dir: str, data_yaml_path: str):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    args = dict(
        model=ckpt_path,
        data=data_yaml_path,
        batch=16,
        imgsz=640,
        device=0 if torch.cuda.is_available() else "cpu",
        plots=True,
        split="val",
        conf=0.001,
        iou=0.7,
        max_det=300,
        task="segment",
        mode="val",
        save_dir=output_path,
        project=str(output_path.parent),
        name=output_path.name,
        exist_ok=True,
    )
    
    validator = SegmentationValidator(args=args)
    orig_init_metrics = validator.init_metrics
    def patched_init_metrics(m):
        orig_init_metrics(m)
        validator.end2end = False
    validator.init_metrics = patched_init_metrics
    
    metrics = validator(model=ckpt_path)
    print(f"Hoàn thành xuất ảnh cho {ckpt_path} vào {output_dir}")
    print(f"Mask mAP50: {validator.metrics.seg.map50:.4f}, Box mAP50: {validator.metrics.box.map50:.4f}")

if __name__ == "__main__":
    print("Script sẵn sàng để import hoặc thực thi trực tiếp trên Kaggle!")
