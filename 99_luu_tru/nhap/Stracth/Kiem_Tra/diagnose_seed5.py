import os, sys
from pathlib import Path
import pandas as pd
from rapidocr_onnxruntime import RapidOCR

sys.stdout.reconfigure(encoding='utf-8')
ocr = RapidOCR()
p5 = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2")

print("--- 1. KIỂM TRA TẤT CẢ FILE ẢNH CURVE TRONG SEED 5 ---")
curves = ['BoxF1_curve.png', 'BoxP_curve.png', 'BoxPR_curve.png', 'BoxR_curve.png',
          'MaskF1_curve.png', 'MaskP_curve.png', 'MaskPR_curve.png', 'MaskR_curve.png']

for img_name in curves:
    img_p = p5 / img_name
    if img_p.exists():
        res, _ = ocr(str(img_p))
        text = ' | '.join([l[1] for l in res if 'all classes' in l[1] or 'mAP' in l[1] or 'polyp' in l[1]])
        print(f"  {img_name:<20}: {text}")
    else:
        print(f"  {img_name:<20}: MISSING")

print("\n--- 2. KIỂM TRA 10 DÒNG CUỐI CÙNG CỦA RESULTS.CSV SEED 5 ---")
csv_file = p5 / "results.csv"
df = pd.read_csv(csv_file)
df.columns = [c.strip() for c in df.columns]

cols_to_show = ['epoch', 'train/seg_loss', 'val/seg_loss', 
                'metrics/precision(B)', 'metrics/recall(B)', 'metrics/mAP50(B)', 'metrics/mAP50-95(B)',
                'metrics/precision(M)', 'metrics/recall(M)', 'metrics/mAP50(M)', 'metrics/mAP50-95(M)']
existing_cols = [c for c in cols_to_show if c in df.columns]

print(df[existing_cols].tail(10).to_string(index=False))

print("\n--- 3. KIỂM TRA DÒNG BEST EPOCH TRONG RESULTS.CSV SEED 5 ---")
col_map = "metrics/mAP50-95(M)" if "metrics/mAP50-95(M)" in df.columns else "metrics/mAP_0.5:0.95(M)"
best_idx = df[col_map].idxmax()
print(f"Best row index: {best_idx} (Epoch {int(df.loc[best_idx, 'epoch'])})")
print(df.loc[best_idx, existing_cols])
