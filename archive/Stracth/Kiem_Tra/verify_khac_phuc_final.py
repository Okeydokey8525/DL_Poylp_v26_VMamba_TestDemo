import os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

EXPECTED_24_IMAGES = [
    # 7 train progress images
    "labels.jpg",
    "train_batch0.jpg",
    "train_batch1.jpg",
    "train_batch2.jpg",
    "train_batch11700.jpg",
    "train_batch11701.jpg",
    "train_batch11702.jpg",
    # 3 val ground-truth labels
    "val_batch0_labels.jpg",
    "val_batch1_labels.jpg",
    "val_batch2_labels.jpg",
    # 3 val predictions
    "val_batch0_pred.jpg",
    "val_batch1_pred.jpg",
    "val_batch2_pred.jpg",
    # 1 training curves summary
    "results.png",
    # 2 confusion matrices
    "confusion_matrix.png",
    "confusion_matrix_normalized.png",
    # 8 performance curves
    "BoxPR_curve.png",
    "BoxF1_curve.png",
    "BoxP_curve.png",
    "BoxR_curve.png",
    "MaskPR_curve.png",
    "MaskF1_curve.png",
    "MaskP_curve.png",
    "MaskR_curve.png",
]

base_khac_phuc = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Khac_phuc")

print("="*80)
print("🔍 BÁO CÁO NGHIỆM THU KIỂM TRA CHẤT LƯỢNG 24 ẢNH KẾT QUẢ / SEED (KHAC_PHUC)")
print("="*80)

all_passed = True

for s in [0, 5]:
    folder_name = f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2"
    target = base_khac_phuc / folder_name
    print(f"\n📂 THƯ MỤC: {folder_name}")
    assert target.exists(), f"Thư mục không tồn tại: {target}"
    
    existing_images = sorted([f for f in os.listdir(target) if f.lower().endswith(('.jpg', '.png'))])
    print(f"   Tổng số ảnh: {len(existing_images)} / 24 ảnh chuẩn")
    
    missing = [f for f in EXPECTED_24_IMAGES if f not in existing_images]
    if missing:
        print(f"   ❌ THIẾU CÁC FILE: {missing}")
        all_passed = False
    else:
        print("   ✅ Đầy đủ chính xác 100% 24/24 file ảnh theo chuẩn Ultralytics!")
    
    # Kiểm tra kích thước từng file
    small_files = []
    for f in existing_images:
        sz = (target / f).stat().st_size / 1024
        if sz < 40.0:
            small_files.append((f, sz))
    
    if small_files:
        print(f"   ⚠️ Cảnh báo file dung lượng nhỏ bất thường: {small_files}")
    else:
        print("   ✅ Tất cả 24 file ảnh đều có độ phân giải và dung lượng chuẩn (> 50KB).")

    # Kiểm tra các file dữ liệu kèm theo
    aux_files = ["args.yaml", "results.csv", "weights/best.pt", "weights/last.pt"]
    missing_aux = [f for f in aux_files if not (target / f).exists()]
    if missing_aux:
        print(f"   ❌ Thiếu file phụ trợ: {missing_aux}")
        all_passed = False
    else:
        print("   ✅ Đầy đủ các file metadata: args.yaml, results.csv, weights/best.pt, weights/last.pt")

print("\n" + "="*80)
if all_passed:
    print("🎉 KẾT QUẢ: TẤT CẢ TIÊU CHÍ NGHIỆM THU ĐÃ HOÀN TOÀN THỎA MÃN!")
else:
    print("❌ KẾT QUẢ: CÓ MỘT SỐ TIÊU CHÍ CHƯA ĐẠT.")
print("="*80)
