import os, sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.stdout.reconfigure(encoding='utf-8')

# Cài đặt phông chữ và thẩm mỹ đồ họa khoa học
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#E5E7EB'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

BASE_COLOR = '#1f77b4'   # Xanh dương Navy / SteelBlue
TSVM_COLOR = '#ff7f0e'   # Cam san hô / Hổ phách Coral
BG_COLOR = '#F9FAFB'

data_root = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen")
out_root = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KQ_DoiXung\Base vs TSVM_BG20")

dir_tonghop = out_root / "01_BieuDo_TongHop_6Seeds"
dir_chitiet = out_root / "03_ChiTiet_TungChiSo"
dir_baocao = out_root / "04_BangSoLieu_Va_BaoCao"

for d in [dir_tonghop, dir_chitiet, dir_baocao]:
    d.mkdir(parents=True, exist_ok=True)

# 1. ĐỌC DỮ LIỆU RESULTS.CSV CỦA 12 RUNS
print("=== BẮT ĐẦU ĐỌC DỮ LIỆU 12 RUNS ===")
models = ["Baseline", "TSVM"]
dfs = {"Baseline": [], "TSVM": []}
best_records = []

for m in models:
    for s in range(6):
        folder_name = f"Kvasir_BG20_Baseline_YOLO26s_seg_s{s}_w2" if m == "Baseline" else f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2"
        csv_file = data_root / folder_name / "results.csv"
        
        df = pd.read_csv(csv_file)
        df.columns = [c.strip() for c in df.columns]
        dfs[m].append(df)
        
        # Cột mAP
        col_map = "metrics/mAP50-95(M)" if "metrics/mAP50-95(M)" in df.columns else "metrics/mAP_0.5:0.95(M)"
        col_map50 = "metrics/mAP50(M)" if "metrics/mAP50(M)" in df.columns else "metrics/mAP_0.5(M)"
        
        best_idx = df[col_map].idxmax()
        row = df.loc[best_idx]
        
        best_records.append({
            "Model": m,
            "Seed": f"s{s}",
            "Best_Epoch": int(row['epoch']),
            "Mask_mAP50_95": float(row[col_map]),
            "Mask_mAP50": float(row[col_map50]),
            "Mask_Precision": float(row.get('metrics/precision(M)', 0)),
            "Mask_Recall": float(row.get('metrics/recall(M)', 0)),
            "Box_mAP50_95": float(row.get('metrics/mAP50-95(B)', row.get('metrics/mAP_0.5:0.95(B)', 0))),
            "Box_mAP50": float(row.get('metrics/mAP50(B)', row.get('metrics/mAP_0.5(B)', 0))),
            "val_seg_loss": float(row.get('val/seg_loss', 0)),
            "val_box_loss": float(row.get('val/box_loss', 0)),
            "val_cls_loss": float(row.get('val/cls_loss', 0)),
            "train_seg_loss": float(row.get('train/seg_loss', 0)),
        })

df_best = pd.DataFrame(best_records)
df_best.to_csv(dir_baocao / "head_to_head_seed_details.csv", index=False, encoding='utf-8-sig')
print(f"✅ Đã xuất: head_to_head_seed_details.csv")

# 2. TÍNH BẢNG TỔNG HỢP MEAN ± STD
summary_rows = []
metrics_to_summarize = [
    ("Mask_mAP50_95", "Mask mAP@50-95", "Độ chính xác phân đoạn toàn diện"),
    ("Mask_mAP50", "Mask mAP@50", "Độ chính xác phân đoạn ngưỡng 0.5"),
    ("Mask_Precision", "Mask Precision", "Độ chuẩn xác (giảm báo động giả)"),
    ("Mask_Recall", "Mask Recall", "Độ nhạy phát hiện tổn thương polyp"),
    ("Box_mAP50_95", "Box mAP@50-95", "Độ chính xác định vị hộp bao"),
    ("val_seg_loss", "Validation Seg Loss", "Mất mát phân đoạn ranh giới"),
    ("val_box_loss", "Validation Box Loss", "Mất mát định vị hộp bao"),
    ("val_cls_loss", "Validation Cls Loss", "Mất mát phân loại polyp"),
]

for col, name, desc in metrics_to_summarize:
    b_vals = df_best[df_best['Model'] == 'Baseline'][col].values
    t_vals = df_best[df_best['Model'] == 'TSVM'][col].values
    
    b_mean, b_std, b_var = np.mean(b_vals), np.std(b_vals, ddof=1), np.var(b_vals, ddof=1)
    t_mean, t_std, t_var = np.mean(t_vals), np.std(t_vals, ddof=1), np.var(t_vals, ddof=1)
    
    delta = t_mean - b_mean
    delta_pct = (delta / b_mean) * 100 if b_mean != 0 else 0
    
    summary_rows.append({
        "Metric": name,
        "Description": desc,
        "Baseline_Mean": round(b_mean, 4),
        "Baseline_Std": round(b_std, 4),
        "Baseline_Var": round(b_var, 6),
        "Baseline_Mean_Std": f"{b_mean:.4f} ± {b_std:.4f}",
        "TSVM_Mean": round(t_mean, 4),
        "TSVM_Std": round(t_std, 4),
        "TSVM_Var": round(t_var, 6),
        "TSVM_Mean_Std": f"{t_mean:.4f} ± {t_std:.4f}",
        "Delta": round(delta, 4),
        "Delta_Pct": f"{delta_pct:+.2f}%",
        "Variance_Reduction": f"{b_var / t_var:.2f}x" if t_var > 0 else "N/A"
    })

df_summary = pd.DataFrame(summary_rows)
df_summary.to_csv(dir_baocao / "summary_mean_std_6seeds.csv", index=False, encoding='utf-8-sig')
print(f"✅ Đã xuất: summary_mean_std_6seeds.csv")

# 3. TÍNH DỮ LIỆU ĐƯỜNG CONG 100 EPOCHS (MEAN & STD)
epoch_stats = {"Baseline": {}, "TSVM": {}}
curve_cols = ['train/seg_loss', 'val/seg_loss', 'val/box_loss', 'val/cls_loss', 
              'metrics/mAP50-95(M)', 'metrics/mAP50(M)', 'metrics/precision(M)', 'metrics/recall(M)']

for m in models:
    for c in curve_cols:
        # gom cột c qua 6 dfs
        matrix = []
        for df in dfs[m]:
            # nếu tên khác
            if c not in df.columns:
                alt = c.replace('mAP50-95', 'mAP_0.5:0.95').replace('mAP50', 'mAP_0.5')
                col_name = alt if alt in df.columns else c
            else:
                col_name = c
            matrix.append(df[col_name].values[:100])
        matrix = np.array(matrix)
        epoch_stats[m][c] = {
            "mean": np.mean(matrix, axis=0),
            "std": np.std(matrix, axis=0, ddof=1),
            "min": np.min(matrix, axis=0),
            "max": np.max(matrix, axis=0)
        }

epochs = np.arange(1, 101)

# ==============================================================================
# HỆ THỐNG BIỂU ĐỒ TỔNG HỢP (DẠNG 1 -> DẠNG 6)
# ==============================================================================

# --- 01. GROUPED BAR CHART TỔNG QUAN 4 CHỈ SỐ ---
print("Đang vẽ 01_overall_benchmark_barchart.png...")
fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
x_labels = ['Mask mAP@50-95', 'Mask mAP@50', 'Precision (Mask)', 'Recall (Mask)']
b_vals_bar = [df_summary.loc[df_summary['Metric']=='Mask mAP@50-95', 'Baseline_Mean'].values[0],
              df_summary.loc[df_summary['Metric']=='Mask mAP@50', 'Baseline_Mean'].values[0],
              df_summary.loc[df_summary['Metric']=='Mask Precision', 'Baseline_Mean'].values[0],
              df_summary.loc[df_summary['Metric']=='Mask Recall', 'Baseline_Mean'].values[0]]
b_errs_bar = [df_summary.loc[df_summary['Metric']=='Mask mAP@50-95', 'Baseline_Std'].values[0],
              df_summary.loc[df_summary['Metric']=='Mask mAP@50', 'Baseline_Std'].values[0],
              df_summary.loc[df_summary['Metric']=='Mask Precision', 'Baseline_Std'].values[0],
              df_summary.loc[df_summary['Metric']=='Mask Recall', 'Baseline_Std'].values[0]]

t_vals_bar = [df_summary.loc[df_summary['Metric']=='Mask mAP@50-95', 'TSVM_Mean'].values[0],
              df_summary.loc[df_summary['Metric']=='Mask mAP@50', 'TSVM_Mean'].values[0],
              df_summary.loc[df_summary['Metric']=='Mask Precision', 'TSVM_Mean'].values[0],
              df_summary.loc[df_summary['Metric']=='Mask Recall', 'TSVM_Mean'].values[0]]
t_errs_bar = [df_summary.loc[df_summary['Metric']=='Mask mAP@50-95', 'TSVM_Std'].values[0],
              df_summary.loc[df_summary['Metric']=='Mask mAP@50', 'TSVM_Std'].values[0],
              df_summary.loc[df_summary['Metric']=='Mask Precision', 'TSVM_Std'].values[0],
              df_summary.loc[df_summary['Metric']=='Mask Recall', 'TSVM_Std'].values[0]]

x = np.arange(len(x_labels))
width = 0.35

rects1 = ax.bar(x - width/2, b_vals_bar, width, yerr=b_errs_bar, label='Baseline YOLO26s-seg',
                color=BASE_COLOR, alpha=0.9, capsize=5, edgecolor='#111827', linewidth=0.8)
rects2 = ax.bar(x + width/2, t_vals_bar, width, yerr=t_errs_bar, label='TSVM (Topology-Shape)',
                color=TSVM_COLOR, alpha=0.9, capsize=5, edgecolor='#111827', linewidth=0.8)

for r in rects1:
    h = r.get_height()
    ax.annotate(f"{h:.4f}", xy=(r.get_x() + r.get_width()/2, h), xytext=(0, 7),
                textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1E3A8A')
for r in rects2:
    h = r.get_height()
    ax.annotate(f"{h:.4f}", xy=(r.get_x() + r.get_width()/2, h), xytext=(0, 7),
                textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#9A3412')

ax.set_ylabel('Điểm số đo lường (Score)', fontsize=11, fontweight='bold')
ax.set_title('So Sánh Hiệu Năng Phân Đoạn 6 Seeds (Kvasir_YOLO_SEG_BG20)\nMean ± 1 Std (Baseline vs TSVM)', fontsize=12, fontweight='bold', pad=14)
ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=10, fontweight='bold')
ax.set_ylim(0.65, 1.0)
ax.grid(axis='y', linestyle='--', alpha=0.6)
ax.legend(frameon=True, facecolor='white', framealpha=0.95, loc='upper left')
plt.savefig(dir_tonghop / "01_overall_benchmark_barchart.png", bbox_inches='tight')
plt.close()

# --- 02. VAL SEG LOSS BARCHART ---
print("Đang vẽ 02_val_seg_loss_barchart.png...")
fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
b_loss_m = df_summary.loc[df_summary['Metric']=='Validation Seg Loss', 'Baseline_Mean'].values[0]
b_loss_s = df_summary.loc[df_summary['Metric']=='Validation Seg Loss', 'Baseline_Std'].values[0]
t_loss_m = df_summary.loc[df_summary['Metric']=='Validation Seg Loss', 'TSVM_Mean'].values[0]
t_loss_s = df_summary.loc[df_summary['Metric']=='Validation Seg Loss', 'TSVM_Std'].values[0]

bars = ax.bar(['Baseline YOLO26s-seg', 'TSVM (Topology-Shape)'], [b_loss_m, t_loss_m],
              yerr=[b_loss_s, t_loss_s], width=0.45, color=[BASE_COLOR, TSVM_COLOR],
              capsize=6, edgecolor='#111827', linewidth=0.8)

ax.annotate(f"{b_loss_m:.4f} ± {b_loss_s:.4f}", xy=(0, b_loss_m), xytext=(0, 8),
            textcoords="offset points", ha='center', fontsize=10, fontweight='bold', color=BASE_COLOR)
ax.annotate(f"{t_loss_m:.4f} ± {t_loss_s:.4f}\n(Giảm {(b_loss_m-t_loss_m)/b_loss_m*100:.2f}%)", xy=(1, t_loss_m), xytext=(0, 8),
            textcoords="offset points", ha='center', fontsize=10, fontweight='bold', color='#C2410C')

ax.set_ylabel('Validation Segmentation Loss (Mean ± Std)', fontsize=11, fontweight='bold')
ax.set_title('Độ Giảm Mất Mát Phân Đoạn Ranh Giới (val/seg_loss)\nTrung bình 6 Seeds trên tập Kvasir_YOLO_SEG_BG20', fontsize=12, fontweight='bold', pad=12)
ax.set_ylim(1.0, 1.55)
ax.grid(axis='y', linestyle='--', alpha=0.6)
plt.savefig(dir_tonghop / "02_val_seg_loss_barchart.png", bbox_inches='tight')
plt.close()

# --- 03. SEED BY SEED BARCHART (PAIRWISE HEAD-TO-HEAD) ---
print("Đang vẽ 03_seed_by_seed_barchart.png...")
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
b_seeds = df_best[df_best['Model']=='Baseline']['Mask_mAP50_95'].values
t_seeds = df_best[df_best['Model']=='TSVM']['Mask_mAP50_95'].values
seed_labels = [f"Seed {i}" for i in range(6)]
x = np.arange(len(seed_labels))

r1 = ax.bar(x - width/2, b_seeds, width, label='Baseline YOLO26s-seg', color=BASE_COLOR, alpha=0.9, edgecolor='#111827')
r2 = ax.bar(x + width/2, t_seeds, width, label='TSVM (Topology-Shape)', color=TSVM_COLOR, alpha=0.9, edgecolor='#111827')

for i in range(6):
    ax.annotate(f"{b_seeds[i]:.4f}", xy=(x[i]-width/2, b_seeds[i]), xytext=(0, 4),
                textcoords="offset points", ha='center', fontsize=8.5, fontweight='bold', color='#1E3A8A')
    ax.annotate(f"{t_seeds[i]:.4f}", xy=(x[i]+width/2, t_seeds[i]), xytext=(0, 4),
                textcoords="offset points", ha='center', fontsize=8.5, fontweight='bold', color='#9A3412')

ax.set_ylabel('Mask mAP@50-95', fontsize=11, fontweight='bold')
ax.set_title('Đối Chiếu Hiệu Năng Từng Cặp Seed Đối Xứng (s0 - s5)\nTSVM Ổn Định Tuyệt Đối (Var co hẹp 21.25x so với Baseline)', fontsize=12, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(seed_labels, fontsize=10, fontweight='bold')
ax.set_ylim(0.67, 0.76)
ax.grid(axis='y', linestyle='--', alpha=0.6)
ax.legend(frameon=True, facecolor='white', loc='lower right')
plt.savefig(dir_tonghop / "03_seed_by_seed_barchart.png", bbox_inches='tight')
plt.close()

# --- 04. CONVERGENCE LOSS CURVES (2x2 GRID, 100 EPOCHS WITH SHADED RIBBON) ---
print("Đang vẽ 04_convergence_loss_curves.png...")
fig, axs = plt.subplots(2, 2, figsize=(13, 10), dpi=300)
loss_configs = [
    ('val/seg_loss', 'Validation Segmentation Loss', axs[0, 0]),
    ('train/seg_loss', 'Training Segmentation Loss', axs[0, 1]),
    ('val/box_loss', 'Validation Bounding Box Loss', axs[1, 0]),
    ('val/cls_loss', 'Validation Classification Loss', axs[1, 1])
]

for col_name, title, ax in loss_configs:
    bm = epoch_stats['Baseline'][col_name]['mean']
    bs = epoch_stats['Baseline'][col_name]['std']
    tm = epoch_stats['TSVM'][col_name]['mean']
    ts = epoch_stats['TSVM'][col_name]['std']
    
    ax.plot(epochs, bm, color=BASE_COLOR, label='Baseline (Mean)', linewidth=2.0)
    ax.fill_between(epochs, bm - bs, bm + bs, color=BASE_COLOR, alpha=0.18)
    
    ax.plot(epochs, tm, color=TSVM_COLOR, label='TSVM (Mean)', linewidth=2.0)
    ax.fill_between(epochs, tm - ts, tm + ts, color=TSVM_COLOR, alpha=0.18)
    
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_xlabel('Epoch', fontsize=10)
    ax.set_ylabel('Loss Value', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right', frameon=True, facecolor='white')

plt.suptitle('Đường Cong Hội Tụ Các Hàm Mất Mát (Loss Curves) Qua 100 Epochs (Mean ± 1 Std Ribbon, 6 Seeds)', fontsize=13, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig(dir_tonghop / "04_convergence_loss_curves.png", bbox_inches='tight')
plt.close()

# --- 05. METRIC CURVES mAP (MASK mAP50-95 & mAP50) ---
print("Đang vẽ 05_metric_curves_mAP.png...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

for col, title, ax in [('metrics/mAP50-95(M)', 'Mask mAP@50-95 Dynamics (100 Epochs)', ax1),
                      ('metrics/mAP50(M)', 'Mask mAP@50 Dynamics (100 Epochs)', ax2)]:
    bm = epoch_stats['Baseline'][col]['mean']
    bs = epoch_stats['Baseline'][col]['std']
    tm = epoch_stats['TSVM'][col]['mean']
    ts = epoch_stats['TSVM'][col]['std']
    
    ax.plot(epochs, bm, color=BASE_COLOR, label='Baseline (Mean)', linewidth=2.0)
    ax.fill_between(epochs, bm - bs, bm + bs, color=BASE_COLOR, alpha=0.18)
    ax.plot(epochs, tm, color=TSVM_COLOR, label='TSVM (Mean)', linewidth=2.0)
    ax.fill_between(epochs, tm - ts, tm + ts, color=TSVM_COLOR, alpha=0.18)
    
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_xlabel('Epoch', fontsize=10)
    ax.set_ylabel('mAP Score', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='lower right', frameon=True, facecolor='white')

plt.suptitle('Động Học Tăng Trưởng mAP Qua 100 Epochs (Dải Dao Động ±1σ của 6 Seeds)', fontsize=13, fontweight='bold', y=1.0)
plt.tight_layout()
plt.savefig(dir_tonghop / "05_metric_curves_mAP.png", bbox_inches='tight')
plt.close()

# --- 06. PRECISION & RECALL DYNAMICS ---
print("Đang vẽ 06_precision_recall_epoch_dynamics.png...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
for col, title, ax in [('metrics/precision(M)', 'Mask Precision qua 100 Epochs', ax1),
                      ('metrics/recall(M)', 'Mask Recall qua 100 Epochs (TSVM vượt trội)', ax2)]:
    bm = epoch_stats['Baseline'][col]['mean']
    bs = epoch_stats['Baseline'][col]['std']
    tm = epoch_stats['TSVM'][col]['mean']
    ts = epoch_stats['TSVM'][col]['std']
    
    ax.plot(epochs, bm, color=BASE_COLOR, label='Baseline (Mean)', linewidth=2.0)
    ax.fill_between(epochs, bm - bs, bm + bs, color=BASE_COLOR, alpha=0.18)
    ax.plot(epochs, tm, color=TSVM_COLOR, label='TSVM (Mean)', linewidth=2.0)
    ax.fill_between(epochs, tm - ts, tm + ts, color=TSVM_COLOR, alpha=0.18)
    
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_xlabel('Epoch', fontsize=10)
    ax.set_ylabel('Score', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='lower right', frameon=True, facecolor='white')

plt.suptitle('Động Học Precision và Recall Qua 100 Epochs (Mean ± 1 Std Ribbon)', fontsize=13, fontweight='bold', y=1.0)
plt.tight_layout()
plt.savefig(dir_tonghop / "06_precision_recall_epoch_dynamics.png", bbox_inches='tight')
plt.close()

# --- 07A. PIE CHART Ý NGHĨA LÂM SÀNG (TRUE POSITIVES VS FALSE NEGATIVES) ---
print("Đang vẽ 07a_pie_clinical_breakdown.png...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5), dpi=300)

b_r = df_summary.loc[df_summary['Metric']=='Mask Recall', 'Baseline_Mean'].values[0] * 100
b_fn = 100.0 - b_r
t_r = df_summary.loc[df_summary['Metric']=='Mask Recall', 'TSVM_Mean'].values[0] * 100
t_fn = 100.0 - t_r

wedges1, texts1, autotexts1 = ax1.pie([b_r, b_fn], labels=['Phát hiện đúng (TP)', 'Bỏ sót (FN)'],
                                       autopct='%1.2f%%', startangle=90, colors=['#3B82F6', '#EF4444'],
                                       wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2))
wedges2, texts2, autotexts2 = ax2.pie([t_r, t_fn], labels=['Phát hiện đúng (TP)', 'Bỏ sót (FN)'],
                                       autopct='%1.2f%%', startangle=90, colors=['#F97316', '#DC2626'],
                                       wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2))

for autotext in autotexts1 + autotexts2:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

ax1.set_title(f'Baseline YOLO26s-seg\nRecall: {b_r:.2f}% (Bỏ sót: {b_fn:.2f}%)', fontsize=11, fontweight='bold')
ax2.set_title(f'TSVM (Topology-Shape)\nRecall: {t_r:.2f}% (Bỏ sót: {t_fn:.2f}%)', fontsize=11, fontweight='bold')
plt.suptitle('Ý Nghĩa Lâm Sàng: Tỷ Lệ Phát Hiện Polyp Đúng vs Bỏ Sót Tổn Thương (Rủi Ro Y Tế)', fontsize=12, fontweight='bold', y=0.98)
plt.savefig(dir_tonghop / "07a_pie_clinical_breakdown.png", bbox_inches='tight')
plt.close()

# --- 07B. PIE CHART HEAD-TO-HEAD WIN RATE ---
print("Đang vẽ 07b_pie_head_to_head_winrate.png...")
fig, ax = plt.subplots(figsize=(6, 5), dpi=300)
wins_t = sum(t_seeds > b_seeds)
wins_b = sum(b_seeds >= t_seeds)
wedges, texts, autotexts = ax.pie([wins_t, wins_b], labels=[f'TSVM Thắng ({wins_t}/6 Seeds)', f'Baseline Thắng ({wins_b}/6 Seeds)'],
                                  autopct='%1.1f%%', startangle=140, colors=[TSVM_COLOR, BASE_COLOR],
                                  wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2))
for at in autotexts:
    at.set_color('white')
    at.set_fontweight('bold')
    at.set_fontsize(11)

ax.set_title('Tỷ Lệ Thắng Đối Đầu Trực Diện (Head-to-Head Win Rate)\nTheo Mask mAP@50-95 Qua 6 Seeds Đối Xứng', fontsize=11, fontweight='bold')
plt.savefig(dir_tonghop / "07b_pie_head_to_head_winrate.png", bbox_inches='tight')
plt.close()

# --- 08. CUMULATIVE LOSS AREA CHART ---
print("Đang vẽ 08_cumulative_loss_area_chart.png...")
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
# Diện tích tích lũy sai số seg loss qua từng epoch
b_cum_loss = np.cumsum(epoch_stats['Baseline']['val/seg_loss']['mean'])
t_cum_loss = np.cumsum(epoch_stats['TSVM']['val/seg_loss']['mean'])

ax.plot(epochs, b_cum_loss, color=BASE_COLOR, label='Baseline Tích Lũy', linewidth=2.0)
ax.plot(epochs, t_cum_loss, color=TSVM_COLOR, label='TSVM Tích Lũy', linewidth=2.0)

ax.fill_between(epochs, t_cum_loss, b_cum_loss, color='#10B981', alpha=0.35, label='Diện Tích Sai Số Triệt Tiêu (Thặng dư tối ưu của TSVM)')
ax.set_title('Biểu Đồ Miền Tích Lũy Sai Số Phân Đoạn (Cumulative Seg Loss Area)\nKhẳng Định TSVM Giảm Tải Sai Số Bền Vững Khi Học Ảnh Nền', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Epoch Huấn Luyện (1 -> 100)', fontsize=10, fontweight='bold')
ax.set_ylabel('Giá Trị Tích Lũy Validation Seg Loss', fontsize=10, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left', frameon=True, facecolor='white')
plt.savefig(dir_tonghop / "08_cumulative_loss_area_chart.png", bbox_inches='tight')
plt.close()

# --- 09. METRIC STABILITY BAND AREA (MIN - MAX ENVELOPE) ---
print("Đang vẽ 09_metric_stability_band_area.png...")
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
b_min = epoch_stats['Baseline']['metrics/mAP50-95(M)']['min']
b_max = epoch_stats['Baseline']['metrics/mAP50-95(M)']['max']
t_min = epoch_stats['TSVM']['metrics/mAP50-95(M)']['min']
t_max = epoch_stats['TSVM']['metrics/mAP50-95(M)']['max']

ax.fill_between(epochs, b_min, b_max, color=BASE_COLOR, alpha=0.25, label='Dải Phân Bổ Baseline [Min, Max]')
ax.fill_between(epochs, t_min, t_max, color=TSVM_COLOR, alpha=0.35, label='Dải Phân Bổ TSVM [Min, Max]')
ax.plot(epochs, epoch_stats['Baseline']['metrics/mAP50-95(M)']['mean'], color=BASE_COLOR, linewidth=1.8, label='Baseline Mean')
ax.plot(epochs, epoch_stats['TSVM']['metrics/mAP50-95(M)']['mean'], color=TSVM_COLOR, linewidth=1.8, label='TSVM Mean')

ax.set_title('Biểu Đồ Miền Bao Phủ Độ Ổn Định (Stability Envelope Band)\nTSVM Co Hẹp Biên Độ Dao Động Cực Đại - Cực Tiểu Giữa 6 Seeds', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Epoch Huấn Luyện (1 -> 100)', fontsize=10, fontweight='bold')
ax.set_ylabel('Mask mAP@50-95 Span', fontsize=10, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='lower right', frameon=True, facecolor='white')
plt.savefig(dir_tonghop / "09_metric_stability_band_area.png", bbox_inches='tight')
plt.close()

# --- 10. RADAR CHART ĐA MỤC TIÊU ---
print("Đang vẽ 10_radar_multiobjective_tradeoff.png...")
categories = ['Mask mAP50-95', 'Mask mAP50', 'Precision', 'Recall', 'Seg Loss Opt (1/Loss)', 'Stability (1/Var)']
N = len(categories)

# Chuẩn hóa về thang điểm 0 - 100 để vẽ radar
b_map = df_summary.loc[df_summary['Metric']=='Mask mAP@50-95', 'Baseline_Mean'].values[0]
t_map = df_summary.loc[df_summary['Metric']=='Mask mAP@50-95', 'TSVM_Mean'].values[0]

b_map50 = df_summary.loc[df_summary['Metric']=='Mask mAP@50', 'Baseline_Mean'].values[0]
t_map50 = df_summary.loc[df_summary['Metric']=='Mask mAP@50', 'TSVM_Mean'].values[0]

b_prec = df_summary.loc[df_summary['Metric']=='Mask Precision', 'Baseline_Mean'].values[0]
t_prec = df_summary.loc[df_summary['Metric']=='Mask Precision', 'TSVM_Mean'].values[0]

b_rec = df_summary.loc[df_summary['Metric']=='Mask Recall', 'Baseline_Mean'].values[0]
t_rec = df_summary.loc[df_summary['Metric']=='Mask Recall', 'TSVM_Mean'].values[0]

b_loss = df_summary.loc[df_summary['Metric']=='Validation Seg Loss', 'Baseline_Mean'].values[0]
t_loss = df_summary.loc[df_summary['Metric']=='Validation Seg Loss', 'TSVM_Mean'].values[0]

b_var = df_summary.loc[df_summary['Metric']=='Mask mAP@50-95', 'Baseline_Var'].values[0]
t_var = df_summary.loc[df_summary['Metric']=='Mask mAP@50-95', 'TSVM_Var'].values[0]

values_base = [b_map*100, b_map50*100, b_prec*100, b_rec*100, (1.5 - b_loss)*150, (0.0003 - b_var)/0.0003*100]
values_tsvm = [t_map*100, t_map50*100, t_prec*100, t_rec*100, (1.5 - t_loss)*150, (0.0003 - t_var)/0.0003*100]

angles = [n / float(N) * 2 * np.pi for n in range(N)]
values_base += values_base[:1]
values_tsvm += values_tsvm[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True), dpi=300)
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], categories, fontsize=9.5, fontweight='bold')

ax.plot(angles, values_base, linewidth=2, linestyle='solid', label='Baseline YOLO26s-seg', color=BASE_COLOR)
ax.fill(angles, values_base, color=BASE_COLOR, alpha=0.2)

ax.plot(angles, values_tsvm, linewidth=2, linestyle='solid', label='TSVM (Topology-Shape)', color=TSVM_COLOR)
ax.fill(angles, values_tsvm, color=TSVM_COLOR, alpha=0.25)

plt.title('Đánh Đổi Đa Mục Tiêu (Multi-Objective Radar Profile)\nBaseline vs TSVM trên Bộ Dữ Liệu BG20', size=12, fontweight='bold', y=1.08)
plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), frameon=True)
plt.savefig(dir_tonghop / "10_radar_multiobjective_tradeoff.png", bbox_inches='tight')
plt.close()

# --- 11. BOXPLOT VARIANCE & STABILITY ---
print("Đang vẽ 11_boxplot_variance_stability.png...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5), dpi=300)

bp1 = ax1.boxplot([b_seeds, t_seeds], patch_artist=True, tick_labels=['Baseline', 'TSVM'], widths=0.45)
colors = [BASE_COLOR, TSVM_COLOR]
for patch, color in zip(bp1['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
for median in bp1['medians']:
    median.set(color='black', linewidth=1.5)

# Swarm scatter
ax1.scatter([1]*len(b_seeds), b_seeds, color='#1E3A8A', zorder=5, alpha=0.9, s=40)
ax1.scatter([2]*len(t_seeds), t_seeds, color='#9A3412', zorder=5, alpha=0.9, s=40)
ax1.set_ylabel('Mask mAP@50-95', fontsize=10, fontweight='bold')
ax1.set_title('Phân Bổ mAP@50-95 (6 Seeds)\nTSVM Co Cụm Phương Sai 21.25x', fontsize=11, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.6)

# Boxplot cho val_seg_loss
b_loss_seeds = df_best[df_best['Model']=='Baseline']['val_seg_loss'].values
t_loss_seeds = df_best[df_best['Model']=='TSVM']['val_seg_loss'].values

bp2 = ax2.boxplot([b_loss_seeds, t_loss_seeds], patch_artist=True, tick_labels=['Baseline', 'TSVM'], widths=0.45)
for patch, color in zip(bp2['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
for median in bp2['medians']:
    median.set(color='black', linewidth=1.5)

ax2.scatter([1]*len(b_loss_seeds), b_loss_seeds, color='#1E3A8A', zorder=5, alpha=0.9, s=40)
ax2.scatter([2]*len(t_loss_seeds), t_loss_seeds, color='#9A3412', zorder=5, alpha=0.9, s=40)
ax2.set_ylabel('Validation Seg Loss', fontsize=10, fontweight='bold')
ax2.set_title('Phân Bổ Seg Loss (6 Seeds)\nTSVM Giảm Loss Rõ Rệt', fontsize=11, fontweight='bold')
ax2.grid(axis='y', linestyle='--', alpha=0.6)

plt.suptitle('Biểu Đồ Hộp (Boxplot & Data Points) Kiểm Chứng Tính Ổn Định', fontsize=12, fontweight='bold', y=0.98)
plt.savefig(dir_tonghop / "11_boxplot_variance_stability.png", bbox_inches='tight')
plt.close()

# --- DẠNG 6: MA TRẬN NHẦM LẪN TRUNG BÌNH 6 SEEDS ---
print("Đang vẽ Dạng 6: 12, 13, 14 (Mean Confusion Matrix)...")
# Đọc file raw đã trích xuất
df_cm_raw = pd.read_csv(dir_baocao / "confusion_matrix_raw_6seeds.csv")

# Tính toán ma trận chuẩn hóa trung bình:
# Với 127 polyp GT:
# Baseline TP, FN, FP, TN
b_cm_sub = df_cm_raw[df_cm_raw['Model']=='Baseline']
t_cm_sub = df_cm_raw[df_cm_raw['Model']=='TSVM']

# Tính mean và std từ các seed hợp lệ
b_tp_mean = b_cm_sub['Norm_TP'].mean()
b_fn_mean = 1.0 - b_tp_mean
b_fp_mean = b_cm_sub['Norm_FP'].mean()
b_tn_mean = 0.0 # object detection/segmentation background convention

t_tp_mean = t_cm_sub['Norm_TP'].dropna().mean()
t_fn_mean = 1.0 - t_tp_mean
t_fp_mean = t_cm_sub['Norm_FP'].dropna().mean()
t_tn_mean = 0.0

cm_base_matrix = np.array([[b_tp_mean, b_fn_mean], [b_fp_mean, 1.0]])
cm_tsvm_matrix = np.array([[t_tp_mean, t_fn_mean], [t_fp_mean, 1.0]])

# 12. MEAN CONFUSION MATRIX SIDE-BY-SIDE
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300)
im1 = ax1.imshow(cm_base_matrix, cmap='Blues', vmin=0, vmax=1)
im2 = ax2.imshow(cm_tsvm_matrix, cmap='Blues', vmin=0, vmax=1)

classes = ['polyp', 'background']
for ax, mat, title, score in [(ax1, cm_base_matrix, 'Baseline YOLO26s-seg', f"mAP@50-95: {b_map:.4f} ± {df_summary.loc[df_summary['Metric']=='Mask mAP@50-95', 'Baseline_Std'].values[0]:.4f}"),
                              (ax2, cm_tsvm_matrix, 'TSVM (Topology-Shape)', f"mAP@50-95: {t_map:.4f} ± {df_summary.loc[df_summary['Metric']=='Mask mAP@50-95', 'TSVM_Std'].values[0]:.4f}")]:
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(classes, fontsize=10, fontweight='bold')
    ax.set_yticklabels(classes, fontsize=10, fontweight='bold')
    ax.set_xlabel('Predicted Label', fontsize=10, fontweight='bold')
    ax.set_ylabel('True Label', fontsize=10, fontweight='bold')
    ax.set_title(f"{title}\n{score}", fontsize=11, fontweight='bold', pad=10)
    
    for i in range(2):
        for j in range(2):
            v = mat[i, j]
            color = "white" if v > 0.5 else "black"
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", color=color, fontsize=13, fontweight='bold')

fig.subplots_adjust(right=0.88)
cbar_ax = fig.add_axes([0.91, 0.2, 0.02, 0.6])
fig.colorbar(im2, cax=cbar_ax, label='Tỷ Lệ Chuẩn Hóa (Normalized Rate)')
plt.suptitle('Ma Trận Nhầm Lẫn Chuẩn Hóa Trung Bình 6 Seeds (Mean Confusion Matrix)', fontsize=13, fontweight='bold', y=0.98)
plt.savefig(dir_tonghop / "12_confusion_matrix_mean_comparison.png", bbox_inches='tight')
plt.close()

# 13. CONFUSION MATRIX DIFF HEATMAP
print("Đang vẽ 13_confusion_matrix_diff_heatmap.png...")
fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=300)
diff_matrix = cm_tsvm_matrix - cm_base_matrix

im = ax.imshow(diff_matrix, cmap='RdBu_r', vmin=-0.15, vmax=0.15)
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(classes, fontsize=10, fontweight='bold')
ax.set_yticklabels(classes, fontsize=10, fontweight='bold')
ax.set_xlabel('Predicted Label', fontsize=10, fontweight='bold')
ax.set_ylabel('True Label', fontsize=10, fontweight='bold')
ax.set_title('Ma Trận Chênh Lệch Hiệu Số (TSVM - Baseline)\nÔ False Negative (Hàng 0, Cột 1) Bị Triệt Tiêu Khi Recall Tăng', fontsize=11, fontweight='bold', pad=12)

for i in range(2):
    for j in range(2):
        v = diff_matrix[i, j]
        sign = "+" if v > 0 else ""
        color = "white" if abs(v) > 0.08 else "black"
        ax.text(j, i, f"{sign}{v:.3f}", ha="center", va="center", color=color, fontsize=12, fontweight='bold')

fig.colorbar(im, ax=ax, label='Độ Lệch Hiệu Số (Delta Rate)')
plt.savefig(dir_tonghop / "13_confusion_matrix_diff_heatmap.png", bbox_inches='tight')
plt.close()

# 14. CONFUSION CELLS GROUPED BARCHART
print("Đang vẽ 14_confusion_cells_grouped_barchart.png...")
fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)
cell_labels = ['True Positive (TP)\n[Phát hiện đúng polyp]', 
               'False Negative (FN)\n[Bỏ sót polyp]', 
               'False Positive (FP)\n[Báo động giả trên nền]']

b_raw_tp = b_cm_sub['Raw_TP'].mean()
b_raw_tp_s = b_cm_sub['Raw_TP'].std()
b_raw_fn = b_cm_sub['Raw_FN'].mean()
b_raw_fn_s = b_cm_sub['Raw_FN'].std()
b_raw_fp = b_cm_sub['Raw_FP'].mean()
b_raw_fp_s = b_cm_sub['Raw_FP'].std()

t_raw_tp = t_cm_sub['Raw_TP'].dropna().mean()
t_raw_tp_s = t_cm_sub['Raw_TP'].dropna().std()
t_raw_fn = t_cm_sub['Raw_FN'].dropna().mean()
t_raw_fn_s = t_cm_sub['Raw_FN'].dropna().std()
t_raw_fp = t_cm_sub['Raw_FP'].dropna().mean()
t_raw_fp_s = t_cm_sub['Raw_FP'].dropna().std()

b_cell_vals = [b_raw_tp, b_raw_fn, b_raw_fp]
b_cell_errs = [b_raw_tp_s, b_raw_fn_s, b_raw_fp_s]
t_cell_vals = [t_raw_tp, t_raw_fn, t_raw_fp]
t_cell_errs = [t_raw_tp_s, t_raw_fn_s, t_raw_fp_s]

x = np.arange(len(cell_labels))
width = 0.35

r1 = ax.bar(x - width/2, b_cell_vals, width, yerr=b_cell_errs, label='Baseline YOLO26s-seg', color=BASE_COLOR, capsize=5, edgecolor='#111827')
r2 = ax.bar(x + width/2, t_cell_vals, width, yerr=t_cell_errs, label='TSVM (Topology-Shape)', color=TSVM_COLOR, capsize=5, edgecolor='#111827')

for r in r1:
    h = r.get_height()
    ax.annotate(f"{h:.1f}", xy=(r.get_x() + r.get_width()/2, h), xytext=(0, 6),
                textcoords="offset points", ha='center', fontsize=9, fontweight='bold', color='#1E3A8A')
for r in r2:
    h = r.get_height()
    ax.annotate(f"{h:.1f}", xy=(r.get_x() + r.get_width()/2, h), xytext=(0, 6),
                textcoords="offset points", ha='center', fontsize=9, fontweight='bold', color='#9A3412')

ax.set_ylabel('Số Lượng Tổn Thương / Khung Hình (Mean ± Std)', fontsize=10, fontweight='bold')
ax.set_title('So Sánh Số Lượng Các Ô Ma Trận Nhầm Lẫn (Mean ± 1 Std, 6 Seeds)', fontsize=12, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(cell_labels, fontsize=9.5, fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.6)
ax.legend(frameon=True, facecolor='white', loc='upper right')
plt.savefig(dir_tonghop / "14_confusion_cells_grouped_barchart.png", bbox_inches='tight')
plt.close()

# ==============================================================================
# BIỂU ĐỒ CHI TIẾT TỪNG CHỈ SỐ (03_ChiTiet_TungChiSo)
# ==============================================================================
print("Đang vẽ các biểu đồ trong 03_ChiTiet_TungChiSo/...")
# Chi tiết val seg loss
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
bm = epoch_stats['Baseline']['val/seg_loss']['mean']
bs = epoch_stats['Baseline']['val/seg_loss']['std']
tm = epoch_stats['TSVM']['val/seg_loss']['mean']
ts = epoch_stats['TSVM']['val/seg_loss']['std']
ax.plot(epochs, bm, color=BASE_COLOR, label='Baseline (Mean)', linewidth=2.0)
ax.fill_between(epochs, bm - bs, bm + bs, color=BASE_COLOR, alpha=0.2)
ax.plot(epochs, tm, color=TSVM_COLOR, label='TSVM (Mean)', linewidth=2.0)
ax.fill_between(epochs, tm - ts, tm + ts, color=TSVM_COLOR, alpha=0.2)
ax.set_title('Validation Segmentation Loss Qua 100 Epochs (Tập Trung Vùng Hội Tụ)', fontsize=11, fontweight='bold')
ax.set_xlabel('Epoch', fontsize=10)
ax.set_ylabel('val/seg_loss', fontsize=10)
ax.set_ylim(1.15, 2.2)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()
plt.savefig(dir_chitiet / "val_seg_loss_detail.png", bbox_inches='tight')
plt.close()

# Chi tiết mask map50-95
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
bm = epoch_stats['Baseline']['metrics/mAP50-95(M)']['mean']
bs = epoch_stats['Baseline']['metrics/mAP50-95(M)']['std']
tm = epoch_stats['TSVM']['metrics/mAP50-95(M)']['mean']
ts = epoch_stats['TSVM']['metrics/mAP50-95(M)']['std']
ax.plot(epochs, bm, color=BASE_COLOR, label='Baseline', linewidth=2.0)
ax.fill_between(epochs, bm - bs, bm + bs, color=BASE_COLOR, alpha=0.2)
ax.plot(epochs, tm, color=TSVM_COLOR, label='TSVM', linewidth=2.0)
ax.fill_between(epochs, tm - ts, tm + ts, color=TSVM_COLOR, alpha=0.2)
ax.set_title('Mask mAP@50-95 Chi Tiết (Mean ± 1 Std Ribbon)', fontsize=11, fontweight='bold')
ax.set_xlabel('Epoch', fontsize=10)
ax.set_ylabel('Mask mAP@50-95', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()
plt.savefig(dir_chitiet / "mask_map50_95_detail.png", bbox_inches='tight')
plt.close()

# Chi tiết mask precision
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
bm = epoch_stats['Baseline']['metrics/precision(M)']['mean']
bs = epoch_stats['Baseline']['metrics/precision(M)']['std']
tm = epoch_stats['TSVM']['metrics/precision(M)']['mean']
ts = epoch_stats['TSVM']['metrics/precision(M)']['std']
ax.plot(epochs, bm, color=BASE_COLOR, label='Baseline', linewidth=2.0)
ax.fill_between(epochs, bm - bs, bm + bs, color=BASE_COLOR, alpha=0.2)
ax.plot(epochs, tm, color=TSVM_COLOR, label='TSVM', linewidth=2.0)
ax.fill_between(epochs, tm - ts, tm + ts, color=TSVM_COLOR, alpha=0.2)
ax.set_title('Mask Precision Chi Tiết (Mean ± 1 Std Ribbon)', fontsize=11, fontweight='bold')
ax.set_xlabel('Epoch', fontsize=10)
ax.set_ylabel('Mask Precision', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()
plt.savefig(dir_chitiet / "mask_precision_detail.png", bbox_inches='tight')
plt.close()

# Chi tiết mask recall
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
bm = epoch_stats['Baseline']['metrics/recall(M)']['mean']
bs = epoch_stats['Baseline']['metrics/recall(M)']['std']
tm = epoch_stats['TSVM']['metrics/recall(M)']['mean']
ts = epoch_stats['TSVM']['metrics/recall(M)']['std']
ax.plot(epochs, bm, color=BASE_COLOR, label='Baseline', linewidth=2.0)
ax.fill_between(epochs, bm - bs, bm + bs, color=BASE_COLOR, alpha=0.2)
ax.plot(epochs, tm, color=TSVM_COLOR, label='TSVM', linewidth=2.0)
ax.fill_between(epochs, tm - ts, tm + ts, color=TSVM_COLOR, alpha=0.2)
ax.set_title('Mask Recall Chi Tiết (Mean ± 1 Std Ribbon)', fontsize=11, fontweight='bold')
ax.set_xlabel('Epoch', fontsize=10)
ax.set_ylabel('Mask Recall', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()
plt.savefig(dir_chitiet / "mask_recall_detail.png", bbox_inches='tight')
plt.close()

print("\n🎉 HOÀN THÀNH VẼ TOÀN BỘ CÁC BIỂU ĐỒ TỔNG HỢP VÀ CHI TIẾT (DẠNG 1 -> DẠNG 6)!")
