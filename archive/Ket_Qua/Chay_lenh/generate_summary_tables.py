import json
import os
import pandas as pd
import numpy as np

with open('all_runs_metrics.json', 'r', encoding='utf-8') as f:
    runs = json.load(f)

# Structure and classify each run
def get_clean_run_info(r):
    p = r['rel_path']
    parts = p.split(os.sep)
    
    # Classify architecture
    if "Kvasir_YOLO26s_seg_P5_Attention_VMamba" in p and parts[0] == "Kvasir_YOLO26s_seg_P5_Attention_VMamba":
        arch = "YOLO26s + P5 Attention VMamba (Proposed 10-Run Benchmark)"
        short_arch = "P5-Attn-VMamba (10-Runs)"
        tag = parts[-1]
    elif parts[0] == "Kvasir_YOLO26s_seg":
        arch = "YOLO26s-seg (Baseline)"
        short_arch = "Baseline YOLO26s-seg"
        tag = parts[-1]
    elif "Attention_VMamba_Fusion" in p or "AVMF" in p:
        arch = "YOLO26s + Attention VMamba Fusion (AVMF)"
        short_arch = "AVMF"
        tag = parts[-1]
    elif "BoundaryAwareVMamba" in p:
        arch = "YOLO26s + Boundary-Aware VMamba"
        short_arch = "Boundary-Aware VMamba"
        tag = parts[-1]
    elif "C3K2VSS" in p:
        arch = "YOLO26s + C3K2VSS (P3 VMamba Backbone)"
        short_arch = "C3K2VSS"
        tag = parts[-1]
    elif "P3_CNN_VMamba" in p:
        arch = "YOLO26s + P3 CNN VMamba"
        short_arch = "P3-CNN-VMamba"
        tag = parts[-1]
    elif "P5_VMamba" in p and "Attention" not in p:
        arch = "YOLO26s + P5 VMamba (No Attention)"
        short_arch = "P5-VMamba (No Attn)"
        tag = parts[-1]
    elif "TSVM" in p:
        arch = "YOLO26s + Topology Shape VMamba (TSVM)"
        short_arch = "TSVM"
        tag = parts[-1]
    elif "Cac_Mo_Hinh_Khac" in p and "P5_Attention_VMamba" in p:
        arch = "YOLO26s + P5 Attention VMamba (Other Runs)"
        short_arch = "P5-Attn-VMamba (Other)"
        tag = parts[-1]
    else:
        arch = "Other"
        short_arch = "Other"
        tag = parts[-1]
        
    peak = r['peak_metrics']
    pep = r['peak_epochs']
    best_ep = r['best_epoch_metrics']
    fin_ep = r['final_epoch_metrics']
    
    return {
        'path': p,
        'tag': tag,
        'arch': arch,
        'short_arch': short_arch,
        'model_yaml': r['model_arg'],
        'seed': r['seed_arg'],
        'epochs': r['epochs_run'],
        'best_epoch': r['best_epoch'],
        # Peak metrics
        'peak_mask_map5095': peak['mask_map5095_max'] * 100 if peak['mask_map5095_max'] else 0,
        'peak_mask_map50': peak['mask_map50_max'] * 100 if peak['mask_map50_max'] else 0,
        'peak_mask_p': peak['mask_p_max'] * 100 if peak['mask_p_max'] else 0,
        'peak_mask_r': peak['mask_r_max'] * 100 if peak['mask_r_max'] else 0,
        'peak_box_map5095': peak['box_map5095_max'] * 100 if peak['box_map5095_max'] else 0,
        'peak_box_map50': peak['box_map50_max'] * 100 if peak['box_map50_max'] else 0,
        'peak_box_p': peak['box_p_max'] * 100 if peak['box_p_max'] else 0,
        'peak_box_r': peak['box_r_max'] * 100 if peak['box_r_max'] else 0,
        # Best epoch metrics (at max mask mAP50-95)
        'best_mask_map5095': best_ep['mask_map5095'] * 100 if best_ep['mask_map5095'] else 0,
        'best_mask_map50': best_ep['mask_map50'] * 100 if best_ep['mask_map50'] else 0,
        'best_mask_p': best_ep['mask_p'] * 100 if best_ep['mask_p'] else 0,
        'best_mask_r': best_ep['mask_r'] * 100 if best_ep['mask_r'] else 0,
        'best_box_map5095': best_ep['box_map5095'] * 100 if best_ep['box_map5095'] else 0,
        'best_box_map50': best_ep['box_map50'] * 100 if best_ep['box_map50'] else 0,
        'best_box_p': best_ep['box_p'] * 100 if best_ep['box_p'] else 0,
        'best_box_r': best_ep['box_r'] * 100 if best_ep['box_r'] else 0,
        'val_seg_loss_best': best_ep['val_seg_loss'],
        'val_box_loss_best': best_ep['val_box_loss'],
        'val_cls_loss_best': best_ep['val_cls_loss'],
        # Final epoch metrics
        'fin_mask_map5095': fin_ep['mask_map5095'] * 100 if fin_ep['mask_map5095'] else 0,
        'fin_mask_map50': fin_ep['mask_map50'] * 100 if fin_ep['mask_map50'] else 0,
        'fin_mask_p': fin_ep['mask_p'] * 100 if fin_ep['mask_p'] else 0,
        'fin_mask_r': fin_ep['mask_r'] * 100 if fin_ep['mask_r'] else 0,
        'fin_box_map5095': fin_ep['box_map5095'] * 100 if fin_ep['box_map5095'] else 0,
        'fin_box_map50': fin_ep['box_map50'] * 100 if fin_ep['box_map50'] else 0,
        'fin_box_p': fin_ep['box_p'] * 100 if fin_ep['box_p'] else 0,
        'fin_box_r': fin_ep['box_r'] * 100 if fin_ep['box_r'] else 0,
        'val_seg_loss_fin': fin_ep['val_seg_loss'],
        'val_box_loss_fin': fin_ep['val_box_loss'],
        'val_cls_loss_fin': fin_ep['val_cls_loss'],
    }

clean_runs = [get_clean_run_info(r) for r in runs]
df_runs = pd.DataFrame(clean_runs)

print("=== ARCHITECTURE LEADERBOARD (AVERAGED BY ARCHITECTURE) ===")
agg_arch = df_runs.groupby('arch').agg(
    runs_count=('path', 'count'),
    peak_mask_map5095_mean=('peak_mask_map5095', 'mean'),
    peak_mask_map5095_max=('peak_mask_map5095', 'max'),
    peak_mask_map50_mean=('peak_mask_map50', 'mean'),
    peak_box_map5095_mean=('peak_box_map5095', 'mean'),
    peak_box_map5095_max=('peak_box_map5095', 'max'),
    peak_mask_p_mean=('peak_mask_p', 'mean'),
    peak_mask_r_mean=('peak_mask_r', 'mean'),
    best_epoch_mean=('best_epoch', 'mean')
).sort_values(by='peak_mask_map5095_max', ascending=False)
print(agg_arch.to_string())

print("\n=== TOP 10 SINGLE BEST RUNS ACROSS ALL EXPERIMENTS (BY MASK mAP50-95) ===")
top10 = df_runs.sort_values(by='peak_mask_map5095', ascending=False).head(15)
for idx, row in top10.iterrows():
    print(f"{row['peak_mask_map5095']:.2f}% | Mask mAP50: {row['peak_mask_map50']:.2f}% | Box mAP50-95: {row['peak_box_map5095']:.2f}% | Ep: {row['best_epoch']} | {row['short_arch']} | {row['tag']}")

