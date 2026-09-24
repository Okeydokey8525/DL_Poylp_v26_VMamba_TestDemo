import os, sys
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

p = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen")
subdirs = sorted([d for d in p.iterdir() if d.is_dir()])

records = []
for d in subdirs:
    csv_file = d / "results.csv"
    if csv_file.exists():
        try:
            df = pd.read_csv(csv_file)
            df.columns = [c.strip() for c in df.columns]
            col_map = "metrics/mAP50-95(M)" if "metrics/mAP50-95(M)" in df.columns else "metrics/mAP_0.5:0.95(M)"
            if col_map in df.columns:
                best_idx = df[col_map].idxmax()
                best_row = df.loc[best_idx]
                
                if "Baseline" in d.name: model = "Baseline"
                elif "IAVM" in d.name: model = "IAVM"
                elif "ITSMamba" in d.name: model = "ITSMamba"
                elif "P5_Attention_VMamba" in d.name: model = "P5_Attn_VMamba"
                elif "TSVM" in d.name: model = "TSVM"
                else: model = "Other"
                
                # Extract seed from name (e.g., s0_w2 -> 0)
                seed = "Unknown"
                for part in d.name.split('_'):
                    if part.startswith('s') and part[1:].isdigit():
                        seed = int(part[1:])
                        break
                
                records.append({
                    "Model": model,
                    "Seed": seed,
                    "Folder": d.name,
                    "Mask_mAP": best_row[col_map],
                    "Mask_mAP50": best_row['metrics/mAP50(M)'] if 'metrics/mAP50(M)' in df.columns else best_row.get('metrics/mAP_0.5(M)', 0),
                    "Precision": best_row.get('metrics/precision(M)', 0) * 100,
                    "Recall": best_row.get('metrics/recall(M)', 0) * 100,
                    "seg_loss": best_row.get('val/seg_loss', 0)
                })
        except Exception as e:
            pass

df_all = pd.DataFrame(records)
print("=== CHI TIẾT TỪNG SEED ===")
print(df_all.to_string(index=False))

print("\n=== BẢNG TỔNG HỢP (MEAN ± STD) ===")
summary = df_all.groupby("Model")[['Mask_mAP', 'Mask_mAP50', 'Precision', 'Recall', 'seg_loss']].agg(['mean', 'std'])
print(summary.to_string())
