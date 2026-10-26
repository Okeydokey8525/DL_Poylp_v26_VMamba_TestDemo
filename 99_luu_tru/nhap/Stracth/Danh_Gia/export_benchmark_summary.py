"""
EXPORT BENCHMARK SUMMARY (CSV)
==============================
Trich xuat du lieu 6-fold cua Baseline va TSVM thanh 2 file CSV sach se:
  1. baseline_vs_tsvm_folds.csv (Chi tiet tung fold s0 den s5)
  2. baseline_vs_tsvm_aggregated.csv (Gia tri thong ke Mean, Std, Delta, p-value)

Luu tai: c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth
"""

import os
import math
import pandas as pd
import numpy as np

BASE_DIR = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Ket_Qua_2"
OUT_DIR = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth"

def t_distribution_p_value_df5(t_val):
    abs_t = abs(t_val)
    def t_pdf(x):
        return (2.0 / (math.sqrt(5 * math.pi) * 1.329340388179137)) * (1 + (x**2)/5.0)**(-3.0)
    xs = np.linspace(abs_t, max(abs_t, 60.0), 20000)
    ys = t_pdf(xs)
    tail = np.trapezoid(ys, xs) if hasattr(np, "trapezoid") else np.trapz(ys, xs)
    return float(min(1.0, 2.0 * tail))

def main():
    splits = [f"s{i}" for i in range(6)]
    models = {
        "Baseline": "Kvasir_Baseline_YOLO26s_seg_{split}_w2",
        "TSVM": "Kvasir_YOLO26s_seg_TSVM_{split}_w2"
    }
    
    fold_rows = []
    for s in splits:
        b_p = os.path.join(BASE_DIR, models["Baseline"].format(split=s), "results.csv")
        t_p = os.path.join(BASE_DIR, models["TSVM"].format(split=s), "results.csv")
        
        b_df = pd.read_csv(b_p)
        t_df = pd.read_csv(t_p)
        b_df.columns = [c.strip() for c in b_df.columns]
        t_df.columns = [c.strip() for c in t_df.columns]
        
        for name, df in [("Baseline", b_df), ("TSVM", t_df)]:
            df["fitness"] = (0.1*df["metrics/mAP50(B)"] + 0.9*df["metrics/mAP50-95(B)"] + 
                             0.1*df["metrics/mAP50(M)"] + 0.9*df["metrics/mAP50-95(M)"])
            best = dict(df.loc[df["fitness"].idxmax()])
            bp, br = best["metrics/precision(B)"], best["metrics/recall(B)"]
            mp, mr = best["metrics/precision(M)"], best["metrics/recall(M)"]
            
            fold_rows.append({
                "model": name,
                "split": s,
                "epoch": int(best["epoch"]),
                "mask_map50": best["metrics/mAP50(M)"],
                "mask_map50_95": best["metrics/mAP50-95(M)"],
                "mask_precision": mp,
                "mask_recall": mr,
                "mask_f1": (2*mp*mr/(mp+mr)) if (mp+mr)>0 else 0,
                "box_map50": best["metrics/mAP50(B)"],
                "box_map50_95": best["metrics/mAP50-95(B)"],
                "box_precision": bp,
                "box_recall": br,
                "box_f1": (2*bp*br/(bp+br)) if (bp+br)>0 else 0,
                "val_seg_loss": best["val/seg_loss"],
                "val_box_loss": best["val/box_loss"],
                "val_cls_loss": best["val/cls_loss"],
                "train_time_sec": df["time"].iloc[-1] if "time" in df else 0
            })
            
    df_folds = pd.DataFrame(fold_rows)
    p_folds = os.path.join(OUT_DIR, "baseline_vs_tsvm_folds.csv")
    df_folds.to_csv(p_folds, index=False)
    print(f"[*] Da xuat: {p_folds}")
    
    # Aggregated
    agg_metrics = [
        ("mask_map50", "Mask mAP@50"),
        ("mask_map50_95", "Mask mAP@50-95"),
        ("mask_precision", "Mask Precision"),
        ("mask_recall", "Mask Recall"),
        ("mask_f1", "Mask F1-Score"),
        ("box_map50", "Box mAP@50"),
        ("box_map50_95", "Box mAP@50-95"),
        ("box_precision", "Box Precision"),
        ("box_recall", "Box Recall"),
        ("box_f1", "Box F1-Score"),
        ("val_seg_loss", "Val Seg Loss"),
        ("val_box_loss", "Val Box Loss"),
        ("val_cls_loss", "Val Cls Loss")
    ]
    
    agg_rows = []
    for col, lbl in agg_metrics:
        b_vals = df_folds[df_folds["model"] == "Baseline"][col].values
        t_vals = df_folds[df_folds["model"] == "TSVM"][col].values
        diff = t_vals - b_vals
        mean_d = np.mean(diff)
        se = np.std(diff, ddof=1) / math.sqrt(6)
        t_stat = mean_d / se if se != 0 else 0
        p_val = t_distribution_p_value_df5(t_stat)
        
        agg_rows.append({
            "metric": lbl,
            "baseline_mean": np.mean(b_vals),
            "baseline_std": np.std(b_vals, ddof=1),
            "tsvm_mean": np.mean(t_vals),
            "tsvm_std": np.std(t_vals, ddof=1),
            "delta": mean_d,
            "pct_change": (mean_d / np.mean(b_vals)) * 100,
            "p_value": p_val,
            "is_significant": p_val < 0.05
        })
        
    df_agg = pd.DataFrame(agg_rows)
    p_agg = os.path.join(OUT_DIR, "baseline_vs_tsvm_aggregated.csv")
    df_agg.to_csv(p_agg, index=False)
    print(f"[*] Da xuat: {p_agg}")

if __name__ == "__main__":
    main()
