import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

fig_dir = r'efficiency_benchmark\figures'
os.makedirs(fig_dir, exist_ok=True)

df_eff = pd.read_csv(r'efficiency_benchmark\tables\efficiency_summary.csv')
df_acc_eff = pd.read_csv(r'efficiency_benchmark\tables\accuracy_efficiency_summary.csv')
df_raw = pd.read_csv(r'efficiency_benchmark\raw\efficiency_raw_benchmark.csv')

colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd']
model_names = list(df_eff['Model'])

# 1. Params
plt.figure(figsize=(7, 4.5), dpi=300)
bars = plt.bar(df_eff['Model'], df_eff['Params_M'], color=colors, width=0.55, edgecolor='black', alpha=0.85)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.15, f"{yval:.3f}M", ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title("Model Parameters (MParams)", fontsize=13, fontweight='bold', pad=12)
plt.ylabel("Parameters (Million)", fontsize=11)
plt.ylim(0, max(df_eff['Params_M']) * 1.2)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=15, ha='right', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig01_params.png'))
plt.close()

# 2. GFLOPs
plt.figure(figsize=(7, 4.5), dpi=300)
bars = plt.bar(df_eff['Model'], df_eff['GFLOPs'], color=colors, width=0.55, edgecolor='black', alpha=0.85)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.2, f"{yval:.2f}", ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title("Computational Complexity (GFLOPs @ 640x640)", fontsize=13, fontweight='bold', pad=12)
plt.ylabel("GFLOPs", fontsize=11)
plt.ylim(0, max(df_eff['GFLOPs']) * 1.2)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=15, ha='right', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig02_gflops.png'))
plt.close()

# 3. Model Size (Checkpoint)
plt.figure(figsize=(7, 4.5), dpi=300)
bars = plt.bar(df_eff['Model'], df_eff['Checkpoint_MB'], color=colors, width=0.55, edgecolor='black', alpha=0.85)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.25, f"{yval:.2f} MB", ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title("Checkpoint Disk Size (best.pt)", fontsize=13, fontweight='bold', pad=12)
plt.ylabel("Size (MB)", fontsize=11)
plt.ylim(0, max(df_eff['Checkpoint_MB']) * 1.2)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=15, ha='right', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig03_model_size.png'))
plt.close()

# 4. Latency Mean (+ Std)
plt.figure(figsize=(7, 4.5), dpi=300)
bars = plt.bar(df_eff['Model'], df_eff['Latency_Mean_ms'], yerr=df_eff['Latency_Std_ms'], capsize=5, color=colors, width=0.55, edgecolor='black', alpha=0.85)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 35, f"{yval:.1f} ms", ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title("Mean Latency per Image (Batch Size = 1)", fontsize=13, fontweight='bold', pad=12)
plt.ylabel("Inference Time (ms)", fontsize=11)
plt.ylim(0, max(df_eff['Latency_Mean_ms']) * 1.25)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=15, ha='right', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig04_latency_mean.png'))
plt.close()

# 5. Latency Percentiles (P50, P95, P99)
plt.figure(figsize=(8, 4.5), dpi=300)
x = np.arange(len(model_names))
width = 0.25
plt.bar(x - width, df_eff['P50_ms'], width, label='P50 (Median)', color='#2b5c8f', edgecolor='black')
plt.bar(x, df_eff['P95_ms'], width, label='P95', color='#e67e22', edgecolor='black')
plt.bar(x + width, df_eff['P99_ms'], width, label='P99', color='#c0392b', edgecolor='black')
plt.title("Inference Latency Percentiles (P50, P95, P99)", fontsize=13, fontweight='bold', pad=12)
plt.ylabel("Latency (ms)", fontsize=11)
plt.xticks(x, model_names, rotation=15, ha='right', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig05_latency_percentiles.png'))
plt.close()

# 6. FPS
plt.figure(figsize=(7, 4.5), dpi=300)
bars = plt.bar(df_eff['Model'], df_eff['FPS'], color=colors, width=0.55, edgecolor='black', alpha=0.85)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f"{yval:.2f}", ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title("Inference Throughput (FPS)", fontsize=13, fontweight='bold', pad=12)
plt.ylabel("Frames Per Second (FPS)", fontsize=11)
plt.ylim(0, max(df_eff['FPS']) * 1.25)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=15, ha='right', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig06_fps.png'))
plt.close()

# 7. VRAM (Annotated as N/A CPU environment)
plt.figure(figsize=(7, 4.5), dpi=300)
bars = plt.bar(df_eff['Model'], [0, 0, 0, 0], color='lightgray', width=0.55, edgecolor='black', linestyle='--')
plt.text(1.5, 0.5, "GPU VRAM: N/A\n(Host execution on CPU environment - PyTorch+CPU)\nStrict adherence to no-fabrication rule", 
         ha='center', va='center', fontsize=11, fontweight='bold', bbox=dict(boxstyle='round,pad=0.8', facecolor='#fff2cc', edgecolor='#d6b656'))
plt.title("Peak GPU VRAM Usage", fontsize=13, fontweight='bold', pad=12)
plt.ylabel("Peak VRAM (MB)", fontsize=11)
plt.ylim(0, 1)
plt.xticks(rotation=15, ha='right', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig07_vram_status.png'))
plt.close()

# 8. Peak System RAM
plt.figure(figsize=(7, 4.5), dpi=300)
bars = plt.bar(df_eff['Model'], df_eff['Peak_RAM_MB'], color=colors, width=0.55, edgecolor='black', alpha=0.85)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 5, f"{yval:.1f} MB", ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.title("Peak Process Memory (RAM RSS)", fontsize=13, fontweight='bold', pad=12)
plt.ylabel("RAM (MB)", fontsize=11)
plt.ylim(0, max(df_eff['Peak_RAM_MB']) * 1.2)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=15, ha='right', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig08_ram.png'))
plt.close()

# 9. mAP50-95 vs Latency
plt.figure(figsize=(8, 5), dpi=300)
for idx, row in df_acc_eff.iterrows():
    plt.errorbar(row['Latency'], row['mAP50-95'], yerr=row['Std'], fmt='o', color=colors[idx], markersize=9, capsize=4, label=row['Model'])
    plt.annotate(f"{row['Model']}\n({row['Latency']:.1f}ms, {row['mAP50-95']:.4f})", 
                 (row['Latency'], row['mAP50-95']), textcoords="offset points", xytext=(8, -5), fontsize=9, fontweight='medium')
plt.title("Trade-off: Mask mAP50-95 vs Inference Latency", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Latency Mean (ms, CPU) [Lower is better]", fontsize=11)
plt.ylabel("Mask mAP50-95 (Mean ± Std) [Higher is better]", fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig09_map_vs_latency.png'))
plt.close()

# 10. mAP50-95 vs FPS
plt.figure(figsize=(8, 5), dpi=300)
for idx, row in df_acc_eff.iterrows():
    plt.errorbar(row['FPS'], row['mAP50-95'], yerr=row['Std'], fmt='s', color=colors[idx], markersize=9, capsize=4, label=row['Model'])
    plt.annotate(f"{row['Model']}\n({row['FPS']:.2f} FPS, {row['mAP50-95']:.4f})", 
                 (row['FPS'], row['mAP50-95']), textcoords="offset points", xytext=(8, -5), fontsize=9, fontweight='medium')
plt.title("Trade-off: Mask mAP50-95 vs FPS", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Throughput (FPS) [Higher is better]", fontsize=11)
plt.ylabel("Mask mAP50-95 (Mean ± Std) [Higher is better]", fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig10_map_vs_fps.png'))
plt.close()

# 11. mAP50-95 vs Params
plt.figure(figsize=(8, 5), dpi=300)
for idx, row in df_acc_eff.iterrows():
    plt.errorbar(row['Params'], row['mAP50-95'], yerr=row['Std'], fmt='^', color=colors[idx], markersize=9, capsize=4, label=row['Model'])
    plt.annotate(f"{row['Model']}\n({row['Params']:.2f}M, {row['mAP50-95']:.4f})", 
                 (row['Params'], row['mAP50-95']), textcoords="offset points", xytext=(8, -5), fontsize=9, fontweight='medium')
plt.title("Trade-off: Mask mAP50-95 vs Parameters", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Parameters (MParams) [Lower is lighter]", fontsize=11)
plt.ylabel("Mask mAP50-95 (Mean ± Std) [Higher is better]", fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig11_map_vs_params.png'))
plt.close()

# 12. mAP50-95 vs GFLOPs
plt.figure(figsize=(8, 5), dpi=300)
for idx, row in df_acc_eff.iterrows():
    plt.errorbar(row['GFLOPs'], row['mAP50-95'], yerr=row['Std'], fmt='D', color=colors[idx], markersize=9, capsize=4, label=row['Model'])
    plt.annotate(f"{row['Model']}\n({row['GFLOPs']:.2f}G, {row['mAP50-95']:.4f})", 
                 (row['GFLOPs'], row['mAP50-95']), textcoords="offset points", xytext=(8, -5), fontsize=9, fontweight='medium')
plt.title("Trade-off: Mask mAP50-95 vs GFLOPs", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Computational Complexity (GFLOPs) [Lower is faster]", fontsize=11)
plt.ylabel("Mask mAP50-95 (Mean ± Std) [Higher is better]", fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig12_map_vs_gflops.png'))
plt.close()

# 13. mAP50-95 vs System RAM
plt.figure(figsize=(8, 5), dpi=300)
for idx, row in df_acc_eff.iterrows():
    plt.errorbar(row['Peak_RAM_MB'], row['mAP50-95'], yerr=row['Std'], fmt='p', color=colors[idx], markersize=9, capsize=4, label=row['Model'])
    plt.annotate(f"{row['Model']}\n({row['Peak_RAM_MB']:.1f} MB, {row['mAP50-95']:.4f})", 
                 (row['Peak_RAM_MB'], row['mAP50-95']), textcoords="offset points", xytext=(8, -5), fontsize=9, fontweight='medium')
plt.title("Trade-off: Mask mAP50-95 vs Peak RAM Memory", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Peak Memory Usage (RAM MB) [Lower is better]", fontsize=11)
plt.ylabel("Mask mAP50-95 (Mean ± Std) [Higher is better]", fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig13_map_vs_ram.png'))
plt.close()

# 14. Pareto Frontier: mAP vs Latency
plt.figure(figsize=(8.5, 5.2), dpi=300)
# Sort by latency
df_sorted_lat = df_acc_eff.sort_values(by='Latency').reset_index(drop=True)
pareto_lat_models = []
max_acc = -1
for _, row in df_sorted_lat.iterrows():
    if row['mAP50-95'] > max_acc:
        pareto_lat_models.append(row)
        max_acc = row['mAP50-95']
df_pareto_lat = pd.DataFrame(pareto_lat_models)

# Plot all points
for idx, row in df_acc_eff.iterrows():
    is_pareto = row['Model'] in list(df_pareto_lat['Model'])
    color = '#2ca02c' if is_pareto else '#7f7f7f'
    m_marker = '*' if is_pareto else 'o'
    m_size = 12 if is_pareto else 8
    plt.errorbar(row['Latency'], row['mAP50-95'], yerr=row['Std'], fmt=m_marker, color=color, markersize=m_size, capsize=4, label=f"{row['Model']} (Pareto Optimal)" if is_pareto else row['Model'])
    plt.annotate(f"{row['Model']}\n({row['Latency']:.1f}ms, {row['mAP50-95']:.4f})", 
                 (row['Latency'], row['mAP50-95']), textcoords="offset points", xytext=(10, -5), fontsize=9, fontweight='bold' if is_pareto else 'normal')

# Draw Pareto line
plt.step(df_pareto_lat['Latency'], df_pareto_lat['mAP50-95'], where='post', color='#2ca02c', linestyle='-', linewidth=2, label='Pareto Frontier')
plt.title("Pareto Analysis: Mask mAP50-95 vs Latency", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Latency (ms) [Lower is better]", fontsize=11)
plt.ylabel("Mask mAP50-95 (Mean) [Higher is better]", fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig14_pareto_map_vs_latency.png'))
plt.close()

# 15. Pareto Frontier: mAP vs GFLOPs
plt.figure(figsize=(8.5, 5.2), dpi=300)
df_sorted_flops = df_acc_eff.sort_values(by='GFLOPs').reset_index(drop=True)
pareto_flops_models = []
max_acc = -1
for _, row in df_sorted_flops.iterrows():
    if row['mAP50-95'] > max_acc:
        pareto_flops_models.append(row)
        max_acc = row['mAP50-95']
df_pareto_flops = pd.DataFrame(pareto_flops_models)

for idx, row in df_acc_eff.iterrows():
    is_pareto = row['Model'] in list(df_pareto_flops['Model'])
    color = '#1f77b4' if is_pareto else '#7f7f7f'
    m_marker = '*' if is_pareto else 'o'
    m_size = 12 if is_pareto else 8
    plt.errorbar(row['GFLOPs'], row['mAP50-95'], yerr=row['Std'], fmt=m_marker, color=color, markersize=m_size, capsize=4, label=f"{row['Model']} (Pareto Optimal)" if is_pareto else row['Model'])
    plt.annotate(f"{row['Model']}\n({row['GFLOPs']:.2f}G, {row['mAP50-95']:.4f})", 
                 (row['GFLOPs'], row['mAP50-95']), textcoords="offset points", xytext=(10, -5), fontsize=9, fontweight='bold' if is_pareto else 'normal')

plt.step(df_pareto_flops['GFLOPs'], df_pareto_flops['mAP50-95'], where='post', color='#1f77b4', linestyle='-', linewidth=2, label='Pareto Frontier')
plt.title("Pareto Analysis: Mask mAP50-95 vs GFLOPs", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Complexity (GFLOPs) [Lower is better]", fontsize=11)
plt.ylabel("Mask mAP50-95 (Mean) [Higher is better]", fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig15_pareto_map_vs_gflops.png'))
plt.close()

print(f"Generated 15 publication-grade figures in {fig_dir}!")
