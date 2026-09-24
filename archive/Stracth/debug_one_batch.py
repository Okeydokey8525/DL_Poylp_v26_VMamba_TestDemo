import sys, os
from pathlib import Path

repo_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\ultralytics_Topology-Shape-aware VMamba"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

import torch
from ultralytics.models.yolo.segment import SegmentationValidator
from ultralytics.nn import autobackend
from ultralytics.utils.metrics import box_iou, mask_iou
from ultralytics.data.utils import check_det_dataset

ckpt_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2\weights\best.pt"
data_yaml = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\data_bg20.yaml"

# Patch AutoBackend
orig_init = autobackend.AutoBackend.__init__
def patched_init(self, model="yolo26n.pt", device=None, dnn=False, data=None, fp16=False, fuse=True, verbose=True):
    orig_init(self, model=model, device=device, dnn=dnn, data=data, fp16=fp16, fuse=False, verbose=verbose)
    if hasattr(self.model, "model"):
        self.model.model[-1]._end2end = False
    self.end2end = False
autobackend.AutoBackend.__init__ = patched_init

if __name__ == "__main__":
    validator = SegmentationValidator(args=dict(
        model=ckpt_path,
        data=data_yaml,
        batch=4,
        imgsz=640,
        device="cpu",
        task="segment",
        mode="val",
        plots=False,
        workers=0,
    ))
    validator.data = check_det_dataset(data_yaml)
    validator.device = torch.device("cpu")
    validator.dataloader = validator.get_dataloader(validator.data["val"], batch_size=4)

    model = autobackend.AutoBackend(model=ckpt_path, device=torch.device("cpu"), fuse=False)
    model.model.model[-1]._end2end = False
    model.end2end = False

    validator.init_metrics(model)
    validator.end2end = False

    # Find a batch with polyps!
    for batch_i, batch in enumerate(validator.dataloader):
        if batch["cls"].shape[0] > 0:
            print(f"Found batch {batch_i} with {batch['cls'].shape[0]} ground truth instances!")
            batch = validator.preprocess(batch)
            preds = model(batch["img"])
            preds = validator.postprocess(preds)
            for si, pred in enumerate(preds):
                pbatch = validator._prepare_batch(si, batch)
                predn = validator._prepare_pred(pred)
                print(f"  Sample {si}: gt_cls={pbatch['cls'].shape}, pred_cls={predn['cls'].shape}")
                if pbatch['cls'].shape[0] > 0 and predn['cls'].shape[0] > 0:
                    b_iou = box_iou(pbatch["bboxes"], predn["bboxes"])
                    print("    Box IoU max:", b_iou.max().item() if b_iou.numel() > 0 else "empty")
                    m_iou = mask_iou(pbatch["masks"].flatten(1), predn["masks"].flatten(1).float())
                    print("    Mask IoU max:", m_iou.max().item() if m_iou.numel() > 0 else "empty")
                    print("    GT box:", pbatch["bboxes"][:2])
                    print("    Pred box:", predn["bboxes"][:2])
            break
