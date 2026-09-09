import json
import os
import pandas as pd
import numpy as np

with open('all_runs_metrics.json', 'r', encoding='utf-8') as f:
    runs = json.load(f)

print(f"Total runs: {len(runs)}")

# Let's inspect all 32 runs and print their details
data_list = []
for r in runs:
    p = r['rel_path']
    parts = p.split(os.sep)
    top_folder = parts[0]
    
    # Categorization
    if top_folder == "Kvasir_YOLO26s_seg":
        category = "1. Baseline YOLOv26s-seg"
        model_name = "YOLOv26s-seg"
    elif top_folder == "Kvasir_YOLO26s_seg_P5_Attention_VMamba":
        category = "2. Proposed: YOLOv26s-seg + P5 Attention VMamba (10 Runs Benchmark)"
        model_name = "YOLOv26s-seg + P5 Attention VMamba"
    elif "P5_Attention_VMamba" in p:
        category = "3. YOLOv26s-seg + P5 Attention VMamba (Ablation / Additional Runs)"
        model_name = "YOLOv26s-seg + P5 Attention VMamba"
    elif "P3_CNN_VMamba" in p:
        category = "4. YOLOv26s-seg + P3 CNN VMamba"
        model_name = "YOLOv26s-seg + P3 CNN VMamba"
    elif "P5_VMamba" in p:
        category = "5. YOLOv26s-seg + P5 VMamba (Without Attention Mechanism)"
        model_name = "YOLOv26s-seg + P5 VMamba (No Attn)"
    elif "Attention_VMamba_Fusion" in p or "AVMF" in p:
        category = "6. YOLOv26s-seg + Interactive Attention VMamba Fusion (AVMF)"
        model_name = "YOLOv26s-seg + AVMF"
    elif "BoundaryAwareVMamba" in p:
        category = "7. YOLOv26s-seg + Boundary-Aware VMamba"
        model_name = "YOLOv26s-seg + Boundary-Aware VMamba"
    elif "C3K2VSS" in p:
        category = "8. YOLOv26s-seg + C3K2VSS (P3 VMamba Backbone)"
        model_name = "YOLOv26s-seg + C3K2VSS"
    elif "TSVM" in p:
        category = "9. YOLOv26s-seg + Topology Shape VMamba (TSVM)"
        model_name = "YOLOv26s-seg + TSVM"
    else:
        category = "10. Other Experiments"
        model_name = "Other"
        
    pk = r['peak_metrics']
    be = r['best_epoch_metrics']
    fe = r['final_epoch_metrics']
    pep = r['peak_epochs']
    
    data_list.append({
        'path': p,
        'folder_name': parts[-1],
        'category': category,
        'model_name': model_name,
        'epochs': r['epochs_run'],
        'best_epoch': r['best_epoch'],
        # Peak metrics (%)
        'peak_mask_map5095': (pk['mask_map5095_max'] or 0) * 100,
        'peak_mask_map50': (pk['mask_map50_max'] or 0) * 100,
        'peak_mask_p': (pk['mask_p_max'] or 0) * 100,
        'peak_mask_r': (pk['mask_r_max'] or 0) * 100,
        'peak_box_map5095': (pk['box_map5095_max'] or 0) * 100,
        'peak_box_map50': (pk['box_map50_max'] or 0) * 100,
        'peak_box_p': (pk['box_p_max'] or 0) * 100,
        'peak_box_r': (pk['box_r_max'] or 0) * 100,
        # Peak epochs
        'ep_mask_map5095': pep['mask_map5095_max_ep'],
        'ep_mask_map50': pep['mask_map50_max_ep'],
        'ep_box_map5095': pep['box_map5095_max_ep'],
        'ep_box_map50': pep['box_map50_max_ep'],
        # Best Epoch metrics (%)
        'be_mask_map5095': (be['mask_map5095'] or 0) * 100,
        'be_mask_map50': (be['mask_map50'] or 0) * 100,
        'be_mask_p': (be['mask_p'] or 0) * 100,
        'be_mask_r': (be['mask_r'] or 0) * 100,
        'be_box_map5095': (be['box_map5095'] or 0) * 100,
        'be_box_map50': (be['box_map50'] or 0) * 100,
        'be_box_p': (be['box_p'] or 0) * 100,
        'be_box_r': (be['box_r'] or 0) * 100,
        'val_seg_loss_be': be['val_seg_loss'],
        'val_box_loss_be': be['val_box_loss'],
        'val_cls_loss_be': be['val_cls_loss'],
        'train_seg_loss_be': be['train_seg_loss'],
        'train_box_loss_be': be['train_box_loss'],
        # Final Epoch metrics (%)
        'fe_mask_map5095': (fe['mask_map5095'] or 0) * 100,
        'fe_mask_map50': (fe['mask_map50'] or 0) * 100,
        'fe_mask_p': (fe['mask_p'] or 0) * 100,
        'fe_mask_r': (fe['mask_r'] or 0) * 100,
        'fe_box_map5095': (fe['box_map5095'] or 0) * 100,
        'fe_box_map50': (fe['box_map50'] or 0) * 100,
        'fe_box_p': (fe['box_p'] or 0) * 100,
        'fe_box_r': (fe['box_r'] or 0) * 100,
        'val_seg_loss_fe': fe['val_seg_loss'],
        'val_box_loss_fe': fe['val_box_loss'],
        'val_cls_loss_fe': fe['val_cls_loss'],
    })

df = pd.DataFrame(data_list)
print("Columns:", df.columns.tolist())
print("\nGroup counts by category:")
print(df['category'].value_counts())

