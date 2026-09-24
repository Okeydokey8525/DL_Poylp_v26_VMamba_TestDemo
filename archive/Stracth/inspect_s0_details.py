import os, sys
from pathlib import Path
import pandas as pd
from rapidocr_onnxruntime import RapidOCR

sys.stdout.reconfigure(encoding='utf-8')
ocr = RapidOCR()

p0_dir = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM_s0_w2")
csv_file = p0_dir / "results.csv"

df = pd.read_csv(csv_file)
df.columns = [c.strip() for c in df.columns]

print("=" * 85)
print("1. ĐỐI CHIẾU DỮ LIỆU RESULTS.CSV CỦA SEED 0")
print("=" * 85)

box_cols = ['epoch', 'metrics/precision(B)', 'metrics/recall(B)', 'metrics/mAP50(B)', 'metrics/mAP50-95(B)',
            'metrics/precision(M)', 'metrics/recall(M)', 'metrics/mAP50(M)', 'metrics/mAP50-95(M)']

print("\n--- 5 Epoch cuối cùng (Epoch 96 -> 100) ---")
print(df[box_cols].tail(5).to_string(index=False))

col_m = "metrics/mAP50-95(M)"
best_idx = df[col_m].idxmax()
best_row = df.loc[best_idx]
last_row = df.iloc[-1]

print("\n--- Dòng Best Epoch (Epoch 88) ---")
print(best_row[box_cols])

print("\n--- Dòng Last Epoch (Epoch 100) ---")
print(last_row[box_cols])

print("\n" + "=" * 85)
print("2. ĐỐI CHIẾU VỚI CÁC FILE ẢNH CURVES CỦA SEED 0 (ĐƯỢC VẼ TẠI EPOCH 100)")
print("=" * 85)

for img_name in ['BoxF1_curve.png', 'BoxPR_curve.png', 'BoxR_curve.png', 'BoxP_curve.png',
                'MaskF1_curve.png', 'MaskPR_curve.png', 'MaskR_curve.png', 'MaskP_curve.png']:
    img_p = p0_dir / img_name
    if img_p.exists():
        res, _ = ocr(str(img_p))
        text = ' | '.join([l[1] for l in res if 'all classes' in l[1] or 'mAP' in l[1] or 'polyp' in l[1]])
        print(f"  {img_name:<20}: {text}")
    else:
        print(f"  {img_name:<20}: MISSING")

print("=" * 85)
