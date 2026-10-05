import os, sys
from pathlib import Path
import numpy as np
import pandas as pd
from rapidocr_onnxruntime import RapidOCR

sys.stdout.reconfigure(encoding='utf-8')

ocr = RapidOCR()

base_dir = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen")
out_root = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KQ_DoiXung\Base vs TSVM_BG20")

# 1. Tạo cấu trúc thư mục
subdirs = [
    out_root / "01_BieuDo_TongHop_6Seeds",
    out_root / "02_Ghep_DoiXung_TungSeed" / "Confusion_Matrix",
    out_root / "02_Ghep_DoiXung_TungSeed" / "Mask_PR_Curve",
    out_root / "02_Ghep_DoiXung_TungSeed" / "Val_Predictions",
    out_root / "03_ChiTiet_TungChiSo",
    out_root / "04_BangSoLieu_Va_BaoCao"
]

for d in subdirs:
    d.mkdir(parents=True, exist_ok=True)

print("✅ Đã tạo cấu trúc thư mục KQ_DoiXung/Base vs TSVM_BG20 thành công!")

# 2. Hàm bóc tách Confusion Matrix từ ảnh bằng OCR
def extract_cm_from_image(img_path):
    if not os.path.exists(img_path):
        return None
    res, _ = ocr(str(img_path))
    if not res:
        return None
    
    # Tìm các số thực / nguyên trong vùng ô ma trận
    # Bố cục Ultralytics CM:
    # Hàng 1 (True polyp): TP ở cột 1 (X ~ 1000-1200, Y ~ 500), FN ở cột 2 (X ~ 1800-1950, Y ~ 500)
    # Hàng 2 (True background): FP ở cột 1 (X ~ 1000-1200, Y ~ 1250-1350), TN ở cột 2 (X ~ 1800-1950, Y ~ 1250-1350)
    tp, fn, fp, tn = None, None, None, 0.0
    
    for item in res:
        text = item[1].strip()
        pts = item[0]
        cx = sum(p[0] for p in pts) / 4.0
        cy = sum(p[1] for p in pts) / 4.0
        
        # Lọc các text là số
        clean_text = text.replace(' ', '').replace(',', '.')
        try:
            val = float(clean_text)
        except ValueError:
            continue
            
        # Phân loại vị trí ô
        if 950 <= cx <= 1250 and 450 <= cy <= 600:
            tp = val
        elif 1750 <= cx <= 2000 and 450 <= cy <= 600:
            fn = val
        elif 950 <= cx <= 1250 and 1200 <= cy <= 1400:
            fp = val
        elif 1750 <= cx <= 2000 and 1200 <= cy <= 1400:
            tn = val

    return {"TP": tp, "FN": fn, "FP": fp, "TN": tn}

# 3. Trích xuất cả 6 seed cho Baseline và 6 seed cho TSVM
models = ["Baseline", "TSVM"]
cm_records = []

for m in models:
    for s in range(6):
        if m == "Baseline":
            folder_name = f"Kvasir_BG20_Baseline_YOLO26s_seg_s{s}_w2"
        else:
            folder_name = f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2"
            
        run_path = base_dir / folder_name
        cm_norm_file = run_path / "confusion_matrix_normalized.png"
        cm_raw_file = run_path / "confusion_matrix.png"
        
        raw_vals = extract_cm_from_image(cm_raw_file)
        norm_vals = extract_cm_from_image(cm_norm_file)
        
        print(f"[{m} - Seed {s}]")
        print(f"  Raw count  : TP={raw_vals.get('TP')}, FN={raw_vals.get('FN')}, FP={raw_vals.get('FP')}, TN={raw_vals.get('TN')}")
        print(f"  Normalized : TP={norm_vals.get('TP')}, FN={norm_vals.get('FN')}, FP={norm_vals.get('FP')}, TN={norm_vals.get('TN')}")
        
        cm_records.append({
            "Model": m,
            "Seed": f"s{s}",
            "Raw_TP": raw_vals.get('TP'),
            "Raw_FN": raw_vals.get('FN'),
            "Raw_FP": raw_vals.get('FP'),
            "Raw_TN": raw_vals.get('TN'),
            "Norm_TP": norm_vals.get('TP'),
            "Norm_FN": norm_vals.get('FN'),
            "Norm_FP": norm_vals.get('FP'),
            "Norm_TN": norm_vals.get('TN')
        })

df_cm = pd.DataFrame(cm_records)
out_csv = out_root / "04_BangSoLieu_Va_BaoCao" / "confusion_matrix_raw_6seeds.csv"
df_cm.to_csv(out_csv, index=False, encoding='utf-8-sig')
print(f"\n✅ Đã lưu kết quả trích xuất CM tại: {out_csv}")
