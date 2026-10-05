import sys, torch
repo_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\ultralytics_Topology-Shape-aware VMamba"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

from ultralytics.nn import autobackend
from ultralytics.data.utils import check_det_dataset
from ultralytics.models.yolo.segment import SegmentationValidator
from ultralytics.nn.modules.head import Detect

Detect.end2end = property(fget=lambda self: False, fset=lambda self, v: setattr(self, '_end2end', v))

ckpt_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Khac_phuc\Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2\weights\best.pt"
data_yaml = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\data_bg20.yaml"

val = SegmentationValidator(args=dict(model=ckpt_path, data=data_yaml, device="cpu", batch=4, imgsz=640, end2end=False, conf=0.001, workers=0))
val.device = torch.device("cpu")
val.data = check_det_dataset(data_yaml, split="val")
val.dataloader = val.get_dataloader(val.data["val"], batch_size=4)

model = autobackend.AutoBackend(model=ckpt_path, device="cpu", fuse=False)
val.init_metrics(model)
head = model.model.model[-1]
head.end2end = False
model.end2end = False
val.end2end = False

batch = next(iter(val.dataloader))
batch = val.preprocess(batch)
preds = model(batch["img"])
post_preds = val.postprocess(preds)

print("--- KIỂM TRA MATCHING GIỮA PREDICTION VÀ GROUND TRUTH ---")
print("batch cls:", batch["cls"].unique().tolist())
print("val.names:", val.names)
print("model.names:", model.names)
for i in range(len(post_preds)):
    p = post_preds[i]
    gt_c = batch["cls"][batch["batch_idx"] == i].tolist()
    print(f"img {i}: pred cls={p['cls'].unique().tolist()}, num_pred={len(p['cls'])}, gt cls={gt_c}")
    print(f"       pred bboxes[:2]={p['bboxes'][:2].tolist() if len(p['bboxes']) else []}")
    print(f"       gt bboxes={batch['bboxes'][batch['batch_idx'] == i].tolist()}")
