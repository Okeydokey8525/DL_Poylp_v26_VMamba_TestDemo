import os, sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

p = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen")
subdirs = sorted([d for d in p.iterdir() if d.is_dir()])

print(f"Tổng số thư mục giải nén: {len(subdirs)}")
print("-" * 115)
print(f"{'Tên thư mục Run':<50} | {'Epochs':<7} | {'Max Mask mAP':<13} | {'best.pt':<8} | {'CM Norm':<8}")
print("-" * 115)

records = []

for d in subdirs:
    csv_file = d / "results.csv"
    best_pt = d / "weights" / "best.pt"
    cm_norm = d / "confusion_matrix_normalized.png"
    
    epochs = "N/A"
    max_mask_map = "N/A"
    if csv_file.exists():
        try:
            df = pd.read_csv(csv_file)
            df.columns = [c.strip() for c in df.columns]
            epochs = str(len(df))
            col_map = "metrics/mAP50-95(M)" if "metrics/mAP50-95(M)" in df.columns else "metrics/mAP_0.5:0.95(M)"
            if col_map in df.columns:
                best_idx = df[col_map].idxmax()
                best_row = df.loc[best_idx]
                max_mask_map = f"{best_row[col_map]:.4f}"
                
                if "Baseline" in d.name: model = "Baseline"
                elif "IAVM" in d.name: model = "IAVM"
                elif "ITSMamba" in d.name: model = "ITSMamba"
                elif "P5_Attention_VMamba" in d.name: model = "P5_Attn_VMamba"
                elif "TSVM" in d.name: model = "TSVM"
                else: model = "Other"
                
                records.append({
                    "Model": model,
                    "Folder": d.name,
                    "Mask_mAP": best_row[col_map],
                    "Mask_mAP50": best_row['metrics/mAP50(M)'] if 'metrics/mAP50(M)' in df.columns else best_row.get('metrics/mAP_0.5(M)', 0),
                    "Precision": best_row.get('metrics/precision(M)', 0),
                    "Recall": best_row.get('metrics/recall(M)', 0),
                    "seg_loss": best_row.get('val/seg_loss', 0)
                })
        except Exception as e:
            epochs = "ERR"
            
    has_pt = "OK" if best_pt.exists() else "MISSING"
    has_cm = "OK" if cm_norm.exists() else "MISSING"
    print(f"{d.name:<50} | {epochs:<7} | {max_mask_map:<13} | {has_pt:<8} | {has_cm:<8}")

print("-" * 115)

df_all = pd.DataFrame(records)
print("\n" + "=" * 80)
print("=== BẢNG THỐNG KÊ TỔNG HỢP MEAN ± STD THEO TỪNG MÔ HÌNH TRÊN TẬP BG20 ===")
print("=" * 80)

for m, g in df_all.groupby("Model"):
    print(f"\n--- Mô hình: {m} ({len(g)} seeds) ---")
    map_mean = g['Mask_mAP'].mean()
    map_std = g['Mask_mAP'].std()
    map_var = g['Mask_mAP'].var()
    map50_mean = g['Mask_mAP50'].mean()
    p_mean = g['Precision'].mean() * 100
    r_mean = g['Recall'].mean() * 100
    loss_mean = g['seg_loss'].mean()
    loss_std = g['seg_loss'].std()
    
    print(f"  * Mask mAP@50-95 : {map_mean:.4f} ± {map_std:.4f} (Phương sai: {map_var:.6f})")
    print(f"  * Mask mAP@50    : {map50_mean:.4f}")
    print(f"  * Mask Precision : {p_mean:.2f}%")
    print(f"  * Mask Recall    : {r_mean:.2f}%")
    print(f"  * val/seg_loss   : {loss_mean:.4f} ± {loss_std:.4f}")
print("=" * 80)
