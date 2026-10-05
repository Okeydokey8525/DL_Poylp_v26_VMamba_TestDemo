import os, re, sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

nen_dir = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen"

models = {
    "Baseline": "YOLOv26s-seg",
    "TSVM": "Kvasir_BG20_YOLO26s_seg_TSVM",
    "P5_Attention_VMamba": "Kvasir_BG20_YOLO26s_seg_P5_Attention_VMamba",
    "ITSMamba": "Kvasir_BG20_YOLO26s_seg_ITSMamba",
    "IAVM": "Kvasir_BG20_YOLO26s_seg_IAVM" if os.path.exists(os.path.join(nen_dir, "Kvasir_BG20_YOLO26s_seg_IAVM")) else "Kvasir_BG20_YOLO26s_seg",
}

def get_seed(folder_name):
    m = re.search(r'_s(\d+)_', folder_name)
    return int(m.group(1)) if m else 999

summary_data = []

for model_name, subfolder in models.items():
    p = os.path.join(nen_dir, subfolder)
    runs = [d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d))]
    runs_sorted = sorted(runs, key=get_seed)
    
    for r in runs_sorted:
        s = get_seed(r)
        csv_path = os.path.join(p, r, "results.csv")
        if not os.path.exists(csv_path):
            continue
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()
        
        metric_col = "metrics/mAP50-95(M)"
        if metric_col not in df.columns:
            seg_cols = [c for c in df.columns if "mAP50-95" in c]
            metric_col = seg_cols[-1] if seg_cols else None
        
        if metric_col:
            best_idx = df[metric_col].idxmax()
            best_row = df.loc[best_idx]
            summary_data.append({
                "model": model_name,
                "seed": s,
                "best_epoch": int(best_row["epoch"]),
                "mask_mAP50_95": float(best_row[metric_col]),
                "mask_mAP50": float(best_row["metrics/mAP50(M)"]),
                "mask_precision": float(best_row["metrics/precision(M)"]),
                "mask_recall": float(best_row["metrics/recall(M)"]),
                "box_mAP50_95": float(best_row["metrics/mAP50-95(B)"]),
                "box_mAP50": float(best_row["metrics/mAP50(B)"]),
                "box_precision": float(best_row["metrics/precision(B)"]),
                "box_recall": float(best_row["metrics/recall(B)"]),
                "val_seg_loss": float(best_row["val/seg_loss"]) if "val/seg_loss" in df.columns else None
            })

df_sum = pd.DataFrame(summary_data)

print("="*80)
print("BẢNG TỔNG HỢP CHI TIẾT MASK mAP@50-95 THEO SEED (BG20)")
print("="*80)
pivot_map = df_sum.pivot(index="seed", columns="model", values="mask_mAP50_95")
cols_order = ["Baseline", "TSVM", "P5_Attention_VMamba", "ITSMamba", "IAVM"]
cols_order = [c for c in cols_order if c in pivot_map.columns]
pivot_map = pivot_map[cols_order]
print(pivot_map.to_string(float_format=lambda x: f"{x:.4f}"))

print("\n" + "="*80)
print("BẢNG TỔNG HỢP MASK RECALL THEO SEED (BG20)")
print("="*80)
pivot_rec = df_sum.pivot(index="seed", columns="model", values="mask_recall")
pivot_rec = pivot_rec[cols_order]
print(pivot_rec.to_string(float_format=lambda x: f"{x:.4f}"))

print("\n" + "="*80)
print("THỐNG KÊ TRUNG BÌNH (MEAN ± STD) THEO TỪNG MÔ HÌNH TRÊN BG20")
print("="*80)
for m in cols_order:
    sub = df_sum[df_sum["model"] == m]
    s_list = sub["seed"].tolist()
    m95 = sub["mask_mAP50_95"]
    m50 = sub["mask_mAP50"]
    rec = sub["mask_recall"]
    prec = sub["mask_precision"]
    print(f"Mô hình: {m}")
    print(f"  - Số seed hoàn thành: {len(sub)} (Seeds: {s_list})")
    print(f"  - Mask mAP@50-95: {m95.mean():.4f} ± {m95.std():.4f} (Min: {m95.min():.4f}, Max: {m95.max():.4f})")
    print(f"  - Mask mAP@50   : {m50.mean():.4f} ± {m50.std():.4f} (Min: {m50.min():.4f}, Max: {m50.max():.4f})")
    print(f"  - Mask Recall   : {rec.mean():.4f} ± {rec.std():.4f} (Min: {rec.min():.4f}, Max: {rec.max():.4f})")
    print(f"  - Mask Precision: {prec.mean():.4f} ± {prec.std():.4f} (Min: {prec.min():.4f}, Max: {prec.max():.4f})")
    print()

# Save df_sum to csv
out_csv = os.path.join(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth", "bg20_all_seeds_metrics.csv")
df_sum.to_csv(out_csv, index=False)
print(f"Đã lưu bảng tổng hợp đầy đủ vào: {out_csv}")
