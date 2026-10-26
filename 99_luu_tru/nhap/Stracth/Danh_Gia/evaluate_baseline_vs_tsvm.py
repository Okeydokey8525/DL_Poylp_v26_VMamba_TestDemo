"""
EVALUATE BASELINE VS TSVM (6-FOLD CROSS VALIDATION)
===================================================
Script thuc thi phan tich, tong hop va kiem dinh thong ke (Paired Student's t-test)
giua 2 mo hinh:
  1. YOLO26s-seg Baseline
  2. YOLO26s-seg-TSVM (Topology-Shape-aware VMamba)
tren bo du lieu Kvasir-SEG (6 splits tu s0 den s5).

Luu y: Chay script nay doc lap de tai lap 100% so lieu duoc ghi trong bao cao.
"""

import os
import math
import pandas as pd
import numpy as np

BASE_DIRS = [
    r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Ket_Qua_2",
    r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Ket_Qua_2"
]

def find_working_dir():
    for d in BASE_DIRS:
        if os.path.exists(d) and os.path.exists(os.path.join(d, "Kvasir_Baseline_YOLO26s_seg_s0_w2")):
            return d
    raise FileNotFoundError("Khong tim thay thu muc ket qua hop le!")

def t_distribution_p_value_df5(t_val):
    abs_t = abs(t_val)
    def t_pdf(x):
        coef = 2.0 / (math.sqrt(5 * math.pi) * 1.329340388179137)
        return coef * (1 + (x**2) / 5.0)**(-3.0)
    xs = np.linspace(abs_t, max(abs_t, 60.0), 20000)
    ys = t_pdf(xs)
    tail = np.trapezoid(ys, xs) if hasattr(np, "trapezoid") else np.trapz(ys, xs)
    return float(min(1.0, 2.0 * tail))

def main():
    target_dir = find_working_dir()
    print(f"[*] Thu muc du lieu ket qua: {target_dir}")
    
    splits = [f"s{i}" for i in range(6)]
    models = {
        "Baseline": "Kvasir_Baseline_YOLO26s_seg_{split}_w2",
        "TSVM": "Kvasir_YOLO26s_seg_TSVM_{split}_w2"
    }
    
    records = {"Baseline": [], "TSVM": []}
    
    for m_name, pat in models.items():
        for s in splits:
            csv_path = os.path.join(target_dir, pat.format(split=s), "results.csv")
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"Thieu file: {csv_path}")
            
            df = pd.read_csv(csv_path)
            df.columns = [c.strip() for c in df.columns]
            
            df["fitness"] = (0.1 * df["metrics/mAP50(B)"] + 0.9 * df["metrics/mAP50-95(B)"] + 
                             0.1 * df["metrics/mAP50(M)"] + 0.9 * df["metrics/mAP50-95(M)"])
            best_row = dict(df.loc[df["fitness"].idxmax()])
            
            bp, br = best_row["metrics/precision(B)"], best_row["metrics/recall(B)"]
            mp, mr = best_row["metrics/precision(M)"], best_row["metrics/recall(M)"]
            best_row["f1_b"] = (2 * bp * br / (bp + br)) if (bp + br) > 0 else 0
            best_row["f1_m"] = (2 * mp * mr / (mp + mr)) if (mp + mr) > 0 else 0
            best_row["split"] = s
            best_row["epoch"] = int(best_row["epoch"])
            best_row["time_sec"] = df["time"].iloc[-1] if "time" in df else 0
            records[m_name].append(best_row)

    metrics_list = [
        ("metrics/mAP50(M)", "Mask mAP@50"),
        ("metrics/mAP50-95(M)", "Mask mAP@50-95"),
        ("metrics/precision(M)", "Mask Precision"),
        ("metrics/recall(M)", "Mask Recall"),
        ("f1_m", "Mask F1-Score"),
        ("metrics/mAP50(B)", "Box mAP@50"),
        ("metrics/mAP50-95(B)", "Box mAP@50-95"),
        ("metrics/precision(B)", "Box Precision"),
        ("metrics/recall(B)", "Box Recall"),
        ("f1_b", "Box F1-Score"),
        ("val/seg_loss", "Val Seg Loss"),
        ("val/box_loss", "Val Box Loss"),
        ("val/cls_loss", "Val Cls Loss")
    ]
    
    print("\n" + "="*85)
    print("BANG SO SANH THONG KE TONG HOP: BASELINE VS TSVM (6 FOLDS)")
    print("="*85)
    header = f"| {'Ten chi so':20s} | {'Baseline (Mean +/- Std)':23s} | {'TSVM (Mean +/- Std)':23s} | {'Delta':9s} | {'p-value':8s} | {'Y nghia (p<0.05)':16s} |"
    print(header)
    print("|" + "-"*22 + "|" + "-"*25 + "|" + "-"*25 + "|" + "-"*11 + "|" + "-"*10 + "|" + "-"*18 + "|")
    
    for k, lbl in metrics_list:
        b_vals = np.array([r[k] for r in records["Baseline"]])
        t_vals = np.array([r[k] for r in records["TSVM"]])
        
        diff = t_vals - b_vals
        mean_d = np.mean(diff)
        
        se_d = np.std(diff, ddof=1) / math.sqrt(6)
        t_stat = mean_d / se_d if se_d != 0 else 0
        p_val = t_distribution_p_value_df5(t_stat)
        
        sig = "Co (p < 0.05)" if p_val < 0.05 else "Khong"
        print(f"| {lbl:20s} | {np.mean(b_vals):.4f} +/- {np.std(b_vals, ddof=1):.4f}        | {np.mean(t_vals):.4f} +/- {np.std(t_vals, ddof=1):.4f}        | {mean_d:+.4f}   | {p_val:.4f}   | {sig:16s} |")
    
    b_time = np.mean([r["time_sec"] for r in records["Baseline"]])
    t_time = np.mean([r["time_sec"] for r in records["TSVM"]])
    print("="*85)
    print(f"[*] Thoi gian train trung binh: Baseline = {b_time/3600:.2f}h | TSVM = {t_time/3600:.2f}h (Tang {t_time/b_time:.2f}x)")
    print("[*] Da hoan tat danh gia thanh cong.")

if __name__ == "__main__":
    main()
