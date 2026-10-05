import os, sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

base_dir = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen")

print("=" * 90)
print(f"{'Seed':<8} | {'Best Ep':<8} | {'Mask mAP50-95':<14} | {'Mask mAP50':<12} | {'Precision':<10} | {'Recall':<10} | {'val/seg_loss':<12}")
print("=" * 90)

records = []
for s in range(6):
    folder = base_dir / f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2"
    csv_file = folder / "results.csv"
    if not csv_file.exists():
        print(f"Seed {s}: Không tìm thấy results.csv!")
        continue
    df = pd.read_csv(csv_file)
    df.columns = [c.strip() for c in df.columns]
    col_m = "metrics/mAP50-95(M)" if "metrics/mAP50-95(M)" in df.columns else "metrics/mAP_0.5:0.95(M)"
    col_m50 = "metrics/mAP50(M)" if "metrics/mAP50(M)" in df.columns else "metrics/mAP_0.5(M)"
    
    best_idx = df[col_m].idxmax()
    row = df.loc[best_idx]
    
    rec = {
        "Seed": f"s{s}",
        "Best_Ep": int(row['epoch']),
        "Mask_mAP50_95": float(row[col_m]),
        "Mask_mAP50": float(row[col_m50]),
        "Precision": float(row.get('metrics/precision(M)', 0)),
        "Recall": float(row.get('metrics/recall(M)', 0)),
        "val_seg_loss": float(row.get('val/seg_loss', 0)),
        "val_box_loss": float(row.get('val/box_loss', 0)),
        "val_cls_loss": float(row.get('val/cls_loss', 0)),
        # last epoch (epoch 100)
        "Last_Mask_mAP50_95": float(df.iloc[-1][col_m]),
        "Last_Recall": float(df.iloc[-1].get('metrics/recall(M)', 0)),
        "Last_Precision": float(df.iloc[-1].get('metrics/precision(M)', 0)),
    }
    records.append(rec)
    print(f"Seed {s:<3} | {rec['Best_Ep']:<8} | {rec['Mask_mAP50_95']:<14.4f} | {rec['Mask_mAP50']:<12.4f} | {rec['Precision']:<10.4f} | {rec['Recall']:<10.4f} | {rec['val_seg_loss']:<12.4f}")

df_res = pd.DataFrame(records)
print("=" * 90)
print(f"TRUNG BÌNH CỘNG (MEAN ± STD) CỦA 6 SEEDS TSVM:")
print(f"  * Mask mAP@50-95 : {df_res['Mask_mAP50_95'].mean():.4f} ± {df_res['Mask_mAP50_95'].std():.4f} (Min: {df_res['Mask_mAP50_95'].min():.4f}, Max: {df_res['Mask_mAP50_95'].max():.4f})")
print(f"  * Mask mAP@50    : {df_res['Mask_mAP50'].mean():.4f} ± {df_res['Mask_mAP50'].std():.4f}")
print(f"  * Mask Precision : {df_res['Precision'].mean()*100:.2f}% ± {df_res['Precision'].std()*100:.2f}%")
print(f"  * Mask Recall    : {df_res['Recall'].mean()*100:.2f}% ± {df_res['Recall'].std()*100:.2f}%")
print(f"  * val/seg_loss   : {df_res['val_seg_loss'].mean():.4f} ± {df_res['val_seg_loss'].std():.4f}")
print("=" * 90)

print("\n--- SO SÁNH GIỮA BEST EPOCH VÀ LAST EPOCH (EPOCH 100) CỦA TSVM ---")
for r in records:
    print(f"{r['Seed']}: Best Ep {r['Best_Ep']:02d} (mAP={r['Mask_mAP50_95']:.4f}, R={r['Recall']:.4f})  vs  Last Ep 100 (mAP={r['Last_Mask_mAP50_95']:.4f}, R={r['Last_Recall']:.4f})")
