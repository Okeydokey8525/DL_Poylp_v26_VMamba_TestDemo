import sys, os
from pathlib import Path

repo_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\ultralytics_Topology-Shape-aware VMamba"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

import torch
import ultralytics
import ultralytics.utils.plotting as p
# make plot_images sync
p.plot_images = p.plot_images.__closure__[0].cell_contents

from ultralytics.models.yolo.segment import SegmentationValidator
from ultralytics.nn import autobackend

import PIL.ImageDraw
from ultralytics.utils.plotting import Annotator

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
test_dir = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\test_val_plots")

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
orig_plot_pred = validator.plot_predictions

def my_plot_pred(batch, preds, ni):
    print(f"Calling plot_predictions for batch {ni} with {len(preds)} images in preds")
    for idx, pr in enumerate(preds):
        bb = pr.get("bboxes", [])
        mk = pr.get("masks", None)
        print(f"  img {idx}: bboxes={bb.shape}, masks={mk.shape if mk is not None else None}")
    try:
        orig_plot_pred(batch, preds, ni)
        print(f"plot_predictions {ni} finished without error!")
    except Exception as e:
        import traceback
        traceback.print_exc()

validator.plot_predictions = my_plot_pred

orig_init_metrics = validator.init_metrics
def patched_init_metrics(m):
    orig_init_metrics(m)
    validator.end2end = False
validator.init_metrics = patched_init_metrics

if __name__ == "__main__":
    validator(model=ckpt_path)
