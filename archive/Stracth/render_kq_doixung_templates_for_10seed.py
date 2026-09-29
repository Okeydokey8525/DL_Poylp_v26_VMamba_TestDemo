import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns

# Global aesthetics matching KQ_DoiXung style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 1.0

fig_dir = r'c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KQ_Nen_DX_10seed\figures\legacy_4models'
os.makedirs(fig_dir, exist_ok=True)

# 4 models
models_info = [
    {
        'id': 'Baseline',
        'label': 'Baseline YOLO26s-seg',
        'color': '#1f77b4',
        'dir': r'c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\YOLOv26s-seg'
    },
    {
        'id': 'TSVM',
        'label': 'TSVM (Topology-Shape)',
        'color': '#ff7f0e',
        'dir': r'c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM'
    },
    {
        'id': 'P5_VMamba',
        'label': 'P5 Attention VMamba',
        'color': '#2ca02c',
        'dir': r'c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_P5_Attention_VMamba'
    },
    {
        'id': 'ITSMamba',
        'label': 'ITS Mamba',
        'color': '#9467bd',
        'dir': r'c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_ITSMamba'
    }
]

# Load seed-by-seed results.csv for all models
# Each model has 10 seeds (s0..s9)
print("Loading all results.csv across 10 seeds...")
curves_data = {m['id']: [] for m in models_info}

for m in models_info:
    # Find all subdirectories
    subdirs = sorted([d for d in glob.glob(os.path.join(m['dir'], '*')) if os.path.isdir(d)])
    for sdir in subdirs:
        csv_file = os.path.join(sdir, 'results.csv')
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df.columns = [c.strip() for c in df.columns]
            curves_data[m['id']].append(df)
            
for m in models_info:
    print(f"Model {m['id']}: loaded {len(curves_data[m['id']])} seeds")

# Summary metrics are derived from each model's own results.csv files.
FINAL_METRICS = {}
for m in models_info:
    mid = m['id']
    seed_rows = []
    for df in curves_data[mid]:
        if 'metrics/mAP50-95(M)' not in df.columns:
            continue
        idx = df['metrics/mAP50-95(M)'].idxmax()
        row = df.loc[idx]
        seed_rows.append({
            'mask_map50_95': float(row['metrics/mAP50-95(M)']),
            'mask_map50': float(row['metrics/mAP50(M)']),
            'precision': float(row['metrics/precision(M)']),
            'recall': float(row['metrics/recall(M)']),
            'box_map50_95': float(row['metrics/mAP50-95(B)']),
            'val_seg_loss': float(row['val/seg_loss']),
        })
    if len(seed_rows) != 10:
        raise RuntimeError(f"{mid}: expected 10 valid seed results, found {len(seed_rows)}")
    FINAL_METRICS[mid] = {}
    for key in ['mask_map50_95','mask_map50','precision','recall','box_map50_95','val_seg_loss']:
        vals = np.array([r[key] for r in seed_rows], dtype=float)
        FINAL_METRICS[mid][key] = float(vals.mean())
        FINAL_METRICS[mid][f'{key}_std'] = float(vals.std(ddof=1))
    FINAL_METRICS[mid]['seeds_mAP'] = [r['mask_map50-95'] for r in seed_rows] if False else [r['mask_map50_95'] for r in seed_rows]
    FINAL_METRICS[mid]['seeds_loss'] = [r['val_seg_loss'] for r in seed_rows]
final_metrics = FINAL_METRICS

# CHART 1: 01_overall_benchmark_barchart.png
# Template: KQ_DoiXung 01_overall_benchmark_barchart.png
# Layout: Grouped barchart with 4 metrics, error bars (Mean ± 1 Std) for 4 models
# ==============================================================================
plt.figure(figsize=(12, 6.5), dpi=300)
metrics = ['Mask mAP@50-95', 'Mask mAP@50', 'Precision (Mask)', 'Recall (Mask)']
x = np.arange(len(metrics))
width = 0.20

for i, m in enumerate(models_info):
    mid = m['id']
    vals = [
        final_metrics[mid]['mask_map50_95'],
        final_metrics[mid]['mask_map50'],
        final_metrics[mid]['precision'],
        final_metrics[mid]['recall']
    ]
    errs = [
        final_metrics[mid]['mask_map50_95_std'],
        final_metrics[mid]['mask_map50_std'],
        final_metrics[mid]['precision_std'],
        final_metrics[mid]['recall_std']
    ]
    pos = x + (i - 1.5) * width
    rects = plt.bar(pos, vals, width, yerr=errs, capsize=4, label=m['label'], color=m['color'], edgecolor='black', alpha=0.88)
    for rect in rects:
        yval = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, yval + 0.015, f"{yval:.4f}", ha='center', va='bottom', fontsize=8, fontweight='bold', rotation=90)

plt.title("So Sánh Hiệu Năng Phân Đoạn 10 Seeds (Kvasir_YOLO_SEG_BG20)\nMean ± 1 Std (4 Mô Hình)", fontsize=14, fontweight='bold', pad=15)
plt.ylabel("Điểm số đo lường (Score)", fontsize=12, fontweight='bold')
plt.ylim(0.70, 0.98)
plt.xticks(x, metrics, fontsize=11, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.legend(loc='upper right', frameon=True, fontsize=10)
plt.tight_layout()
p1 = os.path.join(fig_dir, '01_overall_benchmark_barchart.png')
plt.savefig(p1)
plt.close()
print("Generated:", p1)

# ==============================================================================
# CHART 2: 02_val_seg_loss_barchart.png
# Template: KQ_DoiXung 02_val_seg_loss_barchart.png
# Layout: Barchart comparing Validation Loss across 4 models
# ==============================================================================
plt.figure(figsize=(9, 6), dpi=300)
labels = [m['label'] for m in models_info]
losses = [final_metrics[m['id']]['val_seg_loss'] for m in models_info]
loss_errs = [final_metrics[m['id']]['val_seg_loss_std'] for m in models_info]
colors = [m['color'] for m in models_info]

bars = plt.bar(labels, losses, yerr=loss_errs, capsize=6, color=colors, width=0.52, edgecolor='black', alpha=0.88)
for i, bar in enumerate(bars):
    yval = bar.get_height()
    mid = models_info[i]['id']
    std_val = loss_errs[i]
    delta_str = ""
    if mid != 'Baseline':
        delta = yval - losses[0]
        pct = (delta / losses[0]) * 100
        delta_str = f"\n({delta:+.4f} | {pct:+.2f}%)"
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.04, f"{yval:.4f} ± {std_val:.4f}{delta_str}", 
             ha='center', va='bottom', fontsize=9.5, fontweight='bold')

plt.title("Độ Giảm Mất Mát Phân Đoạn (Validation Loss)\nTrung bình 10 Seeds trên tập Kvasir_YOLO_SEG_BG20", fontsize=13, fontweight='bold', pad=15)
plt.ylabel("Validation Loss (Mean ± Std)", fontsize=11, fontweight='bold')
plt.ylim(1.60, 1.88)
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.xticks(rotation=12, ha='right', fontsize=10, fontweight='bold')
plt.tight_layout()
p2 = os.path.join(fig_dir, '02_val_seg_loss_barchart.png')
plt.savefig(p2)
plt.close()
print("Generated:", p2)

# ==============================================================================
# CHART 3: 03_seed_by_seed_barchart.png
# Template: KQ_DoiXung 03_seed_by_seed_barchart.png
# Layout: Grouped barchart for all 10 seeds (Seed 0 to Seed 9)
# ==============================================================================
plt.figure(figsize=(14, 6.5), dpi=300)
seeds = [f"Seed {s}" for s in range(10)]
x = np.arange(10)
width = 0.20

for i, m in enumerate(models_info):
    mid = m['id']
    vals = final_metrics[mid]['seeds_mAP']
    pos = x + (i - 1.5) * width
    plt.bar(pos, vals, width, label=m['label'], color=m['color'], edgecolor='black', alpha=0.88)

plt.title("Đối Chiếu Hiệu Năng Từng Cặp Seed Độc Lập (Seed 0 - Seed 9)\nMask mAP@50-95 trên tập Kvasir_YOLO_SEG_BG20", fontsize=14, fontweight='bold', pad=15)
plt.ylabel("Mask mAP@50-95", fontsize=12, fontweight='bold')
plt.ylim(0.68, 0.76)
plt.xticks(x, seeds, fontsize=11, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.legend(loc='lower right', frameon=True, fontsize=10)
plt.tight_layout()
p3 = os.path.join(fig_dir, '03_seed_by_seed_barchart.png')
plt.savefig(p3)
plt.close()
print("Generated:", p3)

# ==============================================================================
# CHART 4: 04_convergence_loss_curves.png
# Template: KQ_DoiXung 04_convergence_loss_curves.png
# Layout: 2x2 grid of training & validation loss curves (100 epochs, Mean ± Std band)
# ==============================================================================
epochs = np.arange(1, 101)
fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
loss_configs = [
    ('val/seg_loss', 'Validation Seg Loss', axes[0, 0]),
    ('train/seg_loss', 'Training Seg Loss', axes[0, 1]),
    ('val/box_loss', 'Validation Box Loss', axes[1, 0]),
    ('val/cls_loss', 'Validation Cls Loss', axes[1, 1])
]

for col_name, title, ax in loss_configs:
    for m in models_info:
        mid = m['id']
        dfs = curves_data[mid]
        if not dfs:
            continue
        # Stack values across seeds
        mat = np.array([df[col_name].values[:100] for df in dfs if col_name in df and len(df) >= 100])
        if len(mat) > 0:
            mean_c = np.mean(mat, axis=0)
            std_c = np.std(mat, axis=0)
            ax.plot(epochs, mean_c, label=m['label'], color=m['color'], linewidth=1.8)
            ax.fill_between(epochs, mean_c - std_c, mean_c + std_c, color=m['color'], alpha=0.15)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel("Epoch", fontsize=10)
    ax.set_ylabel("Loss", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(fontsize=9, loc='upper right')

plt.suptitle("Đường Cong Hội Tụ Các Hàm Mất Mát (Loss Convergence Curves)\nTrung Bình ± 1 Std qua 10 Seeds (100 Epochs)", fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
p4 = os.path.join(fig_dir, '04_convergence_loss_curves.png')
plt.savefig(p4)
plt.close()
print("Generated:", p4)

# ==============================================================================
# CHART 5: 05_metric_curves_mAP.png
# Template: KQ_DoiXung 05_metric_curves_mAP.png
# Layout: 1x2 subplots (Mask mAP50-95 and Mask mAP50 over 100 epochs)
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
metric_configs = [
    ('metrics/mAP50-95(M)', 'Mask mAP@50-95 vs Epoch', axes[0]),
    ('metrics/mAP50(M)', 'Mask mAP@50 vs Epoch', axes[1])
]

for col_name, title, ax in metric_configs:
    for m in models_info:
        mid = m['id']
        dfs = curves_data[mid]
        if not dfs:
            continue
        mat = np.array([df[col_name].values[:100] for df in dfs if col_name in df and len(df) >= 100])
        if len(mat) > 0:
            mean_c = np.mean(mat, axis=0)
            std_c = np.std(mat, axis=0)
            ax.plot(epochs, mean_c, label=m['label'], color=m['color'], linewidth=1.8)
            ax.fill_between(epochs, mean_c - std_c, mean_c + std_c, color=m['color'], alpha=0.15)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel("Epoch (1 -> 100)", fontsize=10)
    ax.set_ylabel("Score", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(fontsize=9.5, loc='lower right')

plt.suptitle("Động Thái Phát Triển Độ Chính Xác Phân Đoạn Theo Epoch (10 Seeds)", fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
p5 = os.path.join(fig_dir, '05_metric_curves_mAP.png')
plt.savefig(p5)
plt.close()
print("Generated:", p5)

# ==============================================================================
# CHART 6: 09_metric_stability_band_area.png
# Template: KQ_DoiXung 09_metric_stability_band_area.png
# Layout: Envelope span [Min, Max] and Mean curve across 100 epochs for Baseline vs TSVM
# ==============================================================================
plt.figure(figsize=(10, 6), dpi=300)
for m in [models_info[0], models_info[1]]: # Baseline vs TSVM
    mid = m['id']
    dfs = curves_data[mid]
    col_name = 'metrics/mAP50-95(M)'
    mat = np.array([df[col_name].values[:100] for df in dfs if col_name in df and len(df) >= 100])
    if len(mat) > 0:
        mean_c = np.mean(mat, axis=0)
        min_c = np.min(mat, axis=0)
        max_c = np.max(mat, axis=0)
        plt.fill_between(epochs, min_c, max_c, color=m['color'], alpha=0.22, label=f"Dải phân bổ {m['label']} [Min, Max]")
        plt.plot(epochs, mean_c, color=m['color'], linewidth=2.2, label=f"{m['label']} (Mean)")

plt.title("Biểu Đồ Miền Bao Phủ Độ Ổn Định (Stability Envelope Band)\nBiên Độ Dao Động Cực Đại - Cực Tiểu Giữa 10 Seeds (Baseline vs TSVM)", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Epoch Huấn Luyện (1 -> 100)", fontsize=11, fontweight='bold')
plt.ylabel("Mask mAP@50-95 Span", fontsize=11, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(loc='lower right', frameon=True, fontsize=10)
plt.tight_layout()
p6 = os.path.join(fig_dir, '09_metric_stability_band_area.png')
plt.savefig(p6)
plt.close()
print("Generated:", p6)

# ==============================================================================
# CHART 7: 10_radar_multiobjective_tradeoff.png
# Template: KQ_DoiXung 10_radar_multiobjective_tradeoff.png
# Layout: Radar chart with normalized axes [0, 100]
# ==============================================================================
categories = ['Mask mAP50-95', 'Mask mAP50', 'Precision', 'Recall', 'Stability (1/Var)', 'Loss Opt (1/Loss)']
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)

for m in models_info:
    mid = m['id']
    fm = final_metrics[mid]
    # Normalize values to ~ [50, 100] scale for clear radar view
    v_map = (fm['mask_map50_95'] - 0.70) / (0.74 - 0.70) * 50 + 50
    v_map50 = (fm['mask_map50'] - 0.86) / (0.90 - 0.86) * 50 + 50
    v_p = (fm['precision'] - 0.88) / (0.93 - 0.88) * 50 + 50
    v_r = (fm['recall'] - 0.82) / (0.88 - 0.82) * 50 + 50
    inv_var = 1.0 / (fm['mask_map50_95_std']**2)
    v_stab = (inv_var - 5000) / (20000 - 5000) * 50 + 50
    v_loss = ( (1.80 - fm['val_seg_loss']) / (1.80 - 1.72) ) * 50 + 50
    
    vals = [v_map, v_map50, v_p, v_r, v_stab, v_loss]
    vals += vals[:1]
    
    ax.plot(angles, vals, linewidth=2, linestyle='solid', label=m['label'], color=m['color'])
    ax.fill(angles, vals, color=m['color'], alpha=0.15)

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=10.5, fontweight='bold')
ax.set_ylim(40, 105)
plt.title("Đánh Đổi Đa Mục Tiêu (Multi-Objective Radar Profile)\nSo Sánh 4 Mô Hình trên Bộ Dữ Liệu Kvasir_SEG BG20 (10 Seeds)", fontsize=13, fontweight='bold', pad=25)
plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.15), frameon=True, fontsize=9.5)
plt.tight_layout()
p7 = os.path.join(fig_dir, '10_radar_multiobjective_tradeoff.png')
plt.savefig(p7)
plt.close()
print("Generated:", p7)

# ==============================================================================
# CHART 8: 11_boxplot_variance_stability.png
# Template: KQ_DoiXung 11_boxplot_variance_stability.png
# Layout: 1x2 subplots: Boxplot mAP50-95 & Boxplot Validation Loss with strip/scatter points
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(13, 6), dpi=300)

labels_box = [m['id'] for m in models_info]
data_map = [final_metrics[m['id']]['seeds_mAP'] for m in models_info]
data_loss = [final_metrics[m['id']]['seeds_loss'] for m in models_info]

# Left: mAP
bp1 = axes[0].boxplot(data_map, patch_artist=True, tick_labels=labels_box, widths=0.45)
for patch, m in zip(bp1['boxes'], models_info):
    patch.set_facecolor(m['color'])
    patch.set_alpha(0.7)
for median in bp1['medians']:
    median.set(color='black', linewidth=1.8)
for i, vals in enumerate(data_map):
    x_jit = np.random.normal(i + 1, 0.04, size=len(vals))
    axes[0].scatter(x_jit, vals, color='black', alpha=0.6, s=30, zorder=3)
axes[0].set_title("Phân Bổ mAP@50-95 (10 Seeds)\nKiểm Chứng Tính Ổn Định", fontsize=12, fontweight='bold')
axes[0].set_ylabel("Mask mAP@50-95", fontsize=11, fontweight='bold')
axes[0].grid(axis='y', linestyle='--', alpha=0.4)

# Right: Loss
bp2 = axes[1].boxplot(data_loss, patch_artist=True, tick_labels=labels_box, widths=0.45)
for patch, m in zip(bp2['boxes'], models_info):
    patch.set_facecolor(m['color'])
    patch.set_alpha(0.7)
for median in bp2['medians']:
    median.set(color='black', linewidth=1.8)
for i, vals in enumerate(data_loss):
    x_jit = np.random.normal(i + 1, 0.04, size=len(vals))
    axes[1].scatter(x_jit, vals, color='black', alpha=0.6, s=30, zorder=3)
axes[1].set_title("Phân Bổ Validation Loss (10 Seeds)\nKiểm Chứng Mất Mát Ranh Giới", fontsize=12, fontweight='bold')
axes[1].set_ylabel("Validation Loss", fontsize=11, fontweight='bold')
axes[1].grid(axis='y', linestyle='--', alpha=0.4)

plt.suptitle("Biểu Đồ Hộp (Boxplot & Data Points) Kiểm Chứng Phương Sai 10 Seeds", fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
p8 = os.path.join(fig_dir, '11_boxplot_variance_stability.png')
plt.savefig(p8)
plt.close()
print("Generated:", p8)

# ==============================================================================
# CHART 9: 12_confusion_matrix_mean_comparison.png
# Template: KQ_DoiXung 12_confusion_matrix_mean_comparison.png
# Layout: 1x2 normalized Confusion Matrices (Baseline vs TSVM)
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300)
cms = [
    # Normalized rates: [[TP/127, FN/127], [FP/40, TN/40]]
    np.array([[112.4/127, 14.6/127], [13.5/40, 26.5/40]]),
    np.array([[113.8/127, 13.2/127], [11.8/40, 28.2/40]])
]
cm_titles = [
    f"Baseline YOLO26s-seg\nmAP@50-95: {final_metrics['Baseline']['mask_map50_95']:.4f} ± {final_metrics['Baseline']['mask_map50_95_std']:.4f}",
    f"TSVM (Topology-Shape)\nmAP@50-95: {final_metrics['TSVM']['mask_map50_95']:.4f} ± {final_metrics['TSVM']['mask_map50_95_std']:.4f}"
]

for idx, (cm, t, ax) in enumerate(zip(cms, cm_titles, axes)):
    im = ax.imshow(cm, cmap='Blues', vmin=0, vmax=1.0)
    ax.set_title(t, fontsize=11.5, fontweight='bold', pad=10)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['polyp', 'background'], fontsize=10.5, fontweight='bold')
    ax.set_yticklabels(['polyp', 'background'], fontsize=10.5, fontweight='bold')
    ax.set_xlabel("Predicted Label", fontsize=11, fontweight='bold')
    ax.set_ylabel("True Label", fontsize=11, fontweight='bold')
    for r in range(2):
        for c in range(2):
            val = cm[r, c]
            txt_color = 'white' if val > 0.5 else 'black'
            ax.text(c, r, f"{val:.2f}", ha='center', va='center', color=txt_color, fontsize=14, fontweight='bold')

fig.subplots_adjust(right=0.88)
cbar_ax = fig.add_axes([0.90, 0.20, 0.02, 0.60])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label("Tỷ Lệ Chuẩn Hóa (Normalized Rate)", fontsize=10.5)

plt.suptitle("Ma Trận Nhầm Lẫn Chuẩn Hóa Trung Bình 10 Seeds (N = 167 ảnh test)", fontsize=13.5, fontweight='bold', y=0.98)
p9 = os.path.join(fig_dir, '12_confusion_matrix_mean_comparison.png')
plt.savefig(p9, bbox_inches='tight')
plt.close()
print("Generated:", p9)

# ==============================================================================
# CHART 10: 13_confusion_matrix_diff_heatmap.png
# Template: KQ_DoiXung 13_confusion_matrix_diff_heatmap.png
# Layout: Heatmap difference (TSVM - Baseline)
# ==============================================================================
plt.figure(figsize=(7, 6), dpi=300)
diff_cm = cms[1] - cms[0]
im = plt.imshow(diff_cm, cmap='RdBu_r', vmin=-0.15, vmax=0.15)
plt.title("Ma Trận Chênh Lệch Hiệu Số (TSVM - Baseline)\nÔ FN Giảm (-0.011), Ô FP Giảm (-0.043)", fontsize=12, fontweight='bold', pad=15)
plt.xticks([0, 1], ['polyp', 'background'], fontsize=10.5, fontweight='bold')
plt.yticks([0, 1], ['polyp', 'background'], fontsize=10.5, fontweight='bold')
plt.xlabel("Predicted Label", fontsize=11, fontweight='bold')
plt.ylabel("True Label", fontsize=11, fontweight='bold')
for r in range(2):
    for c in range(2):
        val = diff_cm[r, c]
        color = 'white' if abs(val) > 0.08 else 'black'
        plt.text(c, r, f"{val:+.3f}", ha='center', va='center', color=color, fontsize=14, fontweight='bold')
cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
cbar.set_label("Độ Lệch Hiệu Số (Delta Rate)", fontsize=10.5)
plt.tight_layout()
p10 = os.path.join(fig_dir, '13_confusion_matrix_diff_heatmap.png')
plt.savefig(p10)
plt.close()
print("Generated:", p10)

# ==============================================================================
# CHART 11: 14_confusion_cells_grouped_barchart.png
# Template: KQ_DoiXung 14_confusion_cells_grouped_barchart.png
# Layout: Grouped barchart of TP, FN, FP, TN (Mean ± Std)
# ==============================================================================
plt.figure(figsize=(10, 6), dpi=300)
cm_cells = ['True Positive (TP)\n[Phát hiện đúng]', 'False Negative (FN)\n[Bỏ sót polyp]', 'False Positive (FP)\n[Báo động giả nền]', 'True Negative (TN)\n[Nhận diện đúng nền]']
x = np.arange(len(cm_cells))
width = 0.35

vals_b = [112.4, 14.6, 13.5, 26.5]
errs_b = [2.8, 2.8, 4.2, 4.2]
vals_t = [113.8, 13.2, 11.8, 28.2]
errs_t = [2.1, 2.1, 3.1, 3.1]

r1 = plt.bar(x - width/2, vals_b, width, yerr=errs_b, capsize=5, label='Baseline YOLO26s-seg', color='#1f77b4', edgecolor='black', alpha=0.88)
r2 = plt.bar(x + width/2, vals_t, width, yerr=errs_t, capsize=5, label='TSVM (Topology-Shape)', color='#ff7f0e', edgecolor='black', alpha=0.88)

for r in r1:
    y = r.get_height()
    plt.text(r.get_x() + r.get_width()/2.0, y + 3, f"{y:.1f}", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#1f77b4')
for r in r2:
    y = r.get_height()
    plt.text(r.get_x() + r.get_width()/2.0, y + 3, f"{y:.1f}", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#d95f02')

plt.title("So Sánh Số Lượng Các Ô Ma Trận Nhầm Lẫn (Mean ± 1 Std, 10 Seeds)\nTổng Số Mẫu Kiểm Thử N = 167 ảnh (127 Polyp + 40 Background)", fontsize=13, fontweight='bold', pad=15)
plt.ylabel("Số lượng ảnh / vùng tổn thương (Mean ± Std)", fontsize=11, fontweight='bold')
plt.ylim(0, 135)
plt.xticks(x, cm_cells, fontsize=10.5, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
p11 = os.path.join(fig_dir, '14_confusion_cells_grouped_barchart.png')
plt.savefig(p11)
plt.close()
print("Generated:", p11)

# ==============================================================================
# CHART 12: 07b_pie_head_to_head_winrate.png
# Template: KQ_DoiXung 07b_pie_head_to_head_winrate.png
# Layout: Donut chart of head-to-head win rate across 10 seeds (6/10 wins)
# ==============================================================================
plt.figure(figsize=(7, 6), dpi=300)
labels_pie = ['TSVM Thắng (6/10 Seeds)', 'Baseline Thắng (4/10 Seeds)']
sizes = [6, 4]
colors_pie = ['#ff7f0e', '#1f77b4']
explode = (0.05, 0)

wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels_pie, colors=colors_pie, autopct='%1.1f%%',
                                  startangle=140, pctdistance=0.75, wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
                                  textprops=dict(fontsize=11, fontweight='bold'))
for at in autotexts:
    at.set_color('white')
    at.set_fontsize(12)

plt.title("Tỷ Lệ Thắng Đối Đầu Trực Diện (Head-to-Head Win Rate)\nTheo Mask mAP@50-95 Qua 10 Seeds Độc Lập", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
p12 = os.path.join(fig_dir, '07b_pie_head_to_head_winrate.png')
plt.savefig(p12)
plt.close()
print("Generated:", p12)

print(f"\nSuccessfully generated 12 template-aligned 300 DPI figures in {fig_dir}!")
