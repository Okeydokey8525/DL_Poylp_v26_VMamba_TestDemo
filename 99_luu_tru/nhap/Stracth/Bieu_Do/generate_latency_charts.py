import os, sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding='utf-8')

# Cài đặt phông chữ và thẩm mỹ đồ họa
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

out_root = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KQ_DoiXung\Base vs TSVM_BG20")
dir_tonghop = out_root / "01_BieuDo_TongHop_6Seeds"
dir_baocao = out_root / "04_BangSoLieu_Va_BaoCao"

csv_file = dir_baocao / "latency_breakdown_baseline_tsvm.csv"
df = pd.read_csv(csv_file)
print("Dữ liệu Latency:")
print(df)

# Bảng màu 4 giai đoạn chuẩn y tế đồng nhất
stage_colors = ['#3B82F6', '#8B5CF6', '#EC4899', '#10B981'] # Xanh biển, Tím, Hồng đậm, Xanh lá
stages = ['Preprocessing', 'Backbone/Neck', 'Mask Head/Decode', 'NMS/Postprocessing']

b_row = df[df['Model'] == 'Baseline'].iloc[0]
t_row = df[df['Model'] == 'TSVM'].iloc[0]

b_times = [b_row['Preprocessing_ms'], b_row['Backbone_Neck_ms'], b_row['Mask_Head_ms'], b_row['NMS_Postprocessing_ms']]
t_times = [t_row['Preprocessing_ms'], t_row['Backbone_Neck_ms'], t_row['Mask_Head_ms'], t_row['NMS_Postprocessing_ms']]

b_total = b_row['Total_Latency_ms']
t_total = t_row['Total_Latency_ms']

b_fps = b_row['FPS']
t_fps = t_row['FPS']

# 15A. DONUT CHART BASELINE
print("Đang vẽ 15a_pie_latency_baseline.png...")
fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
wedges, texts, autotexts = ax.pie(b_times, autopct='%1.1f%%', startangle=140, colors=stage_colors,
                                  wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2), pctdistance=0.75)
for at in autotexts:
    at.set_color('white')
    at.set_fontweight('bold')
    at.set_fontsize(10)

labels_legend = [f"{s}: {t:.2f} ms ({t/b_total*100:.1f}%)" for s, t in zip(stages, b_times)]
ax.legend(wedges, labels_legend, title="Các Giai Đoạn Xử Lý", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
ax.set_title(f"Phân Rã Độ Trễ Suy Luận - Baseline YOLO26s-seg\nTổng độ trễ: {b_total:.2f} ms (~{b_fps:.1f} FPS)", fontsize=11, fontweight='bold', pad=14)
plt.savefig(dir_tonghop / "15a_pie_latency_baseline.png", bbox_inches='tight')
plt.close()

# 15B. DONUT CHART TSVM
print("Đang vẽ 15b_pie_latency_tsvm.png...")
fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
wedges, texts, autotexts = ax.pie(t_times, autopct='%1.1f%%', startangle=140, colors=stage_colors,
                                  wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2), pctdistance=0.75)
for at in autotexts:
    at.set_color('white')
    at.set_fontweight('bold')
    at.set_fontsize(10)

labels_legend = [f"{s}: {t:.2f} ms ({t/t_total*100:.1f}%)" for s, t in zip(stages, t_times)]
ax.legend(wedges, labels_legend, title="Các Giai Đoạn Xử Lý", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
ax.set_title(f"Phân Rã Độ Trễ Suy Luận - TSVM (Topology-Shape)\nTổng độ trễ: {t_total:.2f} ms (~{t_fps:.1f} FPS)", fontsize=11, fontweight='bold', pad=14)
plt.savefig(dir_tonghop / "15b_pie_latency_tsvm.png", bbox_inches='tight')
plt.close()

# 15C. STACKED BAR CHART COMPARISON
print("Đang vẽ 15c_latency_stacked_comparison.png...")
fig, ax = plt.subplots(figsize=(7.5, 6), dpi=300)
models_label = ['Baseline YOLO26s-seg', 'TSVM (Topology-Shape)']
x = np.arange(len(models_label))
width = 0.45

bottom_b = 0
bottom_t = 0

for i, (stage, color) in enumerate(zip(stages, stage_colors)):
    val_b = b_times[i]
    val_t = t_times[i]
    
    p1 = ax.bar(0, val_b, width, bottom=bottom_b, color=color, edgecolor='#111827', label=stage if i == 0 or True else "")
    p2 = ax.bar(1, val_t, width, bottom=bottom_t, color=color, edgecolor='#111827')
    
    # Text ở giữa segment nếu đủ lớn
    if val_b > 20:
        ax.text(0, bottom_b + val_b/2, f"{val_b:.1f} ms", ha='center', va='center', color='white', fontweight='bold', fontsize=9)
    if val_t > 20:
        ax.text(1, bottom_t + val_t/2, f"{val_t:.1f} ms", ha='center', va='center', color='white', fontweight='bold', fontsize=9)
        
    bottom_b += val_b
    bottom_t += val_t

# Header text ở đỉnh mỗi cột
ax.annotate(f"Tổng: {b_total:.1f} ms\n({b_fps:.1f} FPS)", xy=(0, b_total), xytext=(0, 6),
            textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1E3A8A')
ax.annotate(f"Tổng: {t_total:.1f} ms\n({t_fps:.1f} FPS)", xy=(1, t_total), xytext=(0, 6),
            textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#9A3412')

ax.set_ylabel('Độ Trễ Xử Lý (Thời Gian ms)', fontsize=10, fontweight='bold')
ax.set_title('So Sánh Phân Rã Độ Trễ Suy Luận Theo 4 Giai Đoạn\n(Preprocessing, Backbone/Neck, Mask Head, NMS Postprocessing)', fontsize=11, fontweight='bold', pad=14)
ax.set_xticks(x)
ax.set_xticklabels(models_label, fontsize=10, fontweight='bold')
ax.set_ylim(0, max(b_total, t_total) * 1.22)
ax.grid(axis='y', linestyle='--', alpha=0.6)
ax.legend(title="Giai Đoạn", loc='upper left', frameon=True, facecolor='white')
plt.savefig(dir_tonghop / "15c_latency_stacked_comparison.png", bbox_inches='tight')
plt.close()

print("🎉 HOÀN THÀNH VẼ DẠNG 7: 15A, 15B, 15C!")
