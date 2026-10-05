import sys, os, time
from pathlib import Path

# Add custom repo to sys.path
repo_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\ultralytics_Topology-Shape-aware VMamba"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

import torch
import PIL.ImageDraw
from ultralytics.utils.plotting import Annotator
import ultralytics.utils.plotting as p
from ultralytics.models.yolo.segment import SegmentationValidator
from ultralytics.nn import autobackend

# 1. Patch plot_images to run synchronously (no dropped frames/files on exit)
if hasattr(p.plot_images, "__closure__") and p.plot_images.__closure__:
    p.plot_images = p.plot_images.__closure__[0].cell_contents

# 2. Patch PIL ImageDraw.rectangle to avoid "x1 must be greater than or equal to x0"
orig_draw_rectangle = PIL.ImageDraw.ImageDraw.rectangle
def safe_rectangle(self, xy, fill=None, outline=None, width=1):
    try:
        if isinstance(xy, (list, tuple)) and len(xy) == 4:
            x0, y0, x1, y1 = xy
            xy = [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]
        elif isinstance(xy, (list, tuple)) and len(xy) == 2 and isinstance(xy[0], (list, tuple)):
            (x0, y0), (x1, y1) = xy
            xy = [(min(x0, x1), min(y0, y1)), (max(x0, x1), max(y0, y1))]
    except Exception:
        pass
    return orig_draw_rectangle(self, xy, fill=fill, outline=outline, width=width)
PIL.ImageDraw.ImageDraw.rectangle = safe_rectangle

# 3. Patch Annotator.box_label to clamp / sort coordinates
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

# 4. Patch AutoBackend to NEVER fuse and force One-to-Many head
orig_init = autobackend.AutoBackend.__init__
def patched_init(self, model="yolo26n.pt", device=None, dnn=False, data=None, fp16=False, fuse=True, verbose=True):
    orig_init(self, model=model, device=device, dnn=dnn, data=data, fp16=fp16, fuse=False, verbose=verbose)
    if hasattr(self.model, "model"):
        head = self.model.model[-1]
        head._end2end = False
    self.end2end = False
autobackend.AutoBackend.__init__ = patched_init

def run_seed_validation(seed_num: int):
    print(f"\n{'='*70}")
    print(f"🚀 BẮT ĐẦU TẠO TOÀN BỘ ẢNH KẾT QUẢ CHUẨN CHO SEED {seed_num}")
    print(f"{'='*70}")
    
    ckpt_path = Path(rf"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM_s{seed_num}_w2\weights\best.pt")
    target_dir = Path(rf"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Khac_phuc\Kvasir_BG20_YOLO26s_seg_TSVM_s{seed_num}_w2")
    data_yaml = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\data_bg20.yaml"
    
    assert ckpt_path.exists(), f"Không tìm thấy checkpoint: {ckpt_path}"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    args = dict(
        model=str(ckpt_path),
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
        save_dir=target_dir,
        project=str(target_dir.parent),
        name=target_dir.name,
        exist_ok=True,
    )
    
    validator = SegmentationValidator(args=args)
    
    orig_init_metrics = validator.init_metrics
    def patched_init_metrics(m):
        orig_init_metrics(m)
        validator.end2end = False
    validator.init_metrics = patched_init_metrics
    
    t0 = time.time()
    metrics = validator(model=str(ckpt_path))
    elapsed = time.time() - t0
    
    print(f"\n✅ Hoàn thành Seed {seed_num} trong {elapsed:.1f}s")
    print(f"   - Box  mAP50: {validator.metrics.box.map50:.4f}, mAP50-95: {validator.metrics.box.map:.4f}")
    print(f"   - Mask mAP50: {validator.metrics.seg.map50:.4f}, mAP50-95: {validator.metrics.seg.map:.4f}")
    
    # Liệt kê toàn bộ file ảnh có trong target_dir
    img_files = sorted([f for f in os.listdir(target_dir) if f.lower().endswith(('.jpg', '.png'))])
    print(f"📁 Tổng số file ảnh hiện có trong {target_dir.name}: {len(img_files)}/24")
    for f in img_files:
        size_kb = (target_dir / f).stat().st_size / 1024
        print(f"   [IMG] {f:<32} ({size_kb:6.1f} KB)")

if __name__ == "__main__":
    for s in [0, 5]:
        run_seed_validation(s)
    print("\n🎉 TOÀN BỘ QUÁ TRÌNH TẠO ẢNH KHẮC PHỤC HOÀN TẤT THÀNH CÔNG!")
