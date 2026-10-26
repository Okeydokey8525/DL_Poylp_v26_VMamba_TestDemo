import sys, time, torch
repo_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\ultralytics_Topology-Shape-aware VMamba"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

from ultralytics.nn import autobackend
from ultralytics.data.utils import check_det_dataset
from ultralytics.models.yolo.segment import SegmentationValidator
from ultralytics.nn.modules.head import Detect

# Khóa cứng Detect.end2end
Detect.end2end = property(fget=lambda self: False, fset=lambda self, v: setattr(self, '_end2end', v))

ckpt_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Khac_phuc\Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2\weights\best.pt"
data_yaml = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\data_bg20.yaml"

val = SegmentationValidator(args=dict(model=ckpt_path, data=data_yaml, device="cpu", batch=16, imgsz=640, end2end=False, conf=0.001, workers=0))
val.device = torch.device("cpu")
val.args.workers = 0
val.data = check_det_dataset(data_yaml, split="val")
val.dataloader = val.get_dataloader(val.data["val"], batch_size=16)

# Load model không fuse
model = autobackend.AutoBackend(model=ckpt_path, device="cpu", fuse=False)
head = model.model.model[-1]
head.end2end = False
model.end2end = False
val.init_metrics(model)
val.end2end = False

print("🚀 Đang chạy validation 160 ảnh qua nhánh One-to-Many...")
t0 = time.time()
for b_i, batch in enumerate(val.dataloader):
    batch = val.preprocess(batch)
    preds = model(batch["img"])
    post_preds = val.postprocess(preds)
    val.update_metrics(post_preds, batch)

stats = val.get_stats()
print(f"⏱️ Thời gian: {time.time()-t0:.1f}s")
print(f"✅ KẾT QUẢ TÍNH ĐƯỢC TỪ BEST.PT SEED 5:")
print(f"   - Mask mAP50:    {val.metrics.seg.map50:.4f}")
print(f"   - Mask mAP50-95: {val.metrics.seg.map:.4f}")
print(f"   - Box  mAP50:    {val.metrics.box.map50:.4f}")
print(f"   - Box  mAP50-95: {val.metrics.box.map:.4f}")
