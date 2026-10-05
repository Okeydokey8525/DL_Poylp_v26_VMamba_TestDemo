import os, sys, shutil
from pathlib import Path
import yaml
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

dataset_dir = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Kvasir_YOLO_SEG_BG20")
seed5_dir = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2")
best_pt = seed5_dir / "weights" / "best.pt"
eval_out_dir = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\seed5_re_eval")

# 1. Tạo data.yaml cục bộ
yaml_path = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\data_bg20_val.yaml")
yaml_data = {
    'path': str(dataset_dir),
    'train': 'images/train',
    'val': 'images/val',
    'nc': 1,
    'names': {0: 'polyp'}
}
with open(yaml_path, 'w', encoding='utf-8') as f:
    yaml.safe_dump(yaml_data, f)

print("✅ Đã tạo data.yaml:", yaml_path)
print("🚀 Đang tải mô hình TSVM Seed 5 best.pt...")
model = YOLO(str(best_pt))

print("⚡ Bắt đầu chạy Validation (plots=True, batch=16)...")
metrics = model.val(
    data=str(yaml_path),
    project=str(eval_out_dir),
    name="val_run",
    plots=True,
    batch=16,
    device="cpu",
    workers=2,
    verbose=True
)

print("\n=== KẾT QUẢ VALIDATION MỚI CHO TSVM SEED 5 BEST.PT ===")
print(f"Mask mAP@50-95 : {metrics.seg.map:.4f}")
print(f"Mask mAP@50    : {metrics.seg.map50:.4f}")
print(f"Box mAP@50-95  : {metrics.box.map:.4f}")
print(f"Box mAP@50     : {metrics.box.map50:.4f}")

# 2. Copy các file ảnh đường cong mới sinh vào thư mục run gốc
val_run_dir = eval_out_dir / "val_run"
files_to_copy = [
    "BoxF1_curve.png", "BoxP_curve.png", "BoxPR_curve.png", "BoxR_curve.png",
    "MaskF1_curve.png", "MaskP_curve.png", "MaskPR_curve.png", "MaskR_curve.png",
    "confusion_matrix.png", "confusion_matrix_normalized.png"
]

print("\n--- COPY CÁC FILE ẢNH MỚI VÀO SEED 5 GỐC ---")
for fn in files_to_copy:
    src = val_run_dir / fn
    dst = seed5_dir / fn
    if src.exists():
        shutil.copy2(src, dst)
        print(f"✅ Đã cập nhật: {fn} ({src.stat().st_size} bytes)")
    else:
        print(f"⚠️ Không tìm thấy: {fn}")

print("\n🎉 HOÀN THÀNH TÁI TẠO FILE ẢNH CHO TSVM SEED 5!")
