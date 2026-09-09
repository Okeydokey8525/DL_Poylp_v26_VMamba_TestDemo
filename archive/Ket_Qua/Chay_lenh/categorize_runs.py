import json
import os
import pandas as pd
import numpy as np

with open('all_runs_metrics.json', 'r', encoding='utf-8') as f:
    runs = json.load(f)

print(f"Loaded {len(runs)} runs.")

# Group runs by model category/folder
categories = {}
for r in runs:
    p = r['rel_path']
    top_folder = p.split(os.sep)[0]
    sub_folder = p.split(os.sep)[1] if len(p.split(os.sep)) > 1 else top_folder
    
    # Identify model family
    if "Kvasir_YOLO26s_seg_P5_Attention_VMamba" in p and top_folder == "Kvasir_YOLO26s_seg_P5_Attention_VMamba":
        fam = "Proposed_P5_Attn_VMamba_10Runs"
    elif top_folder == "Kvasir_YOLO26s_seg":
        fam = "Baseline_YOLO26s_seg"
    elif "Attention_VMamba_Fusion" in p or "AVMF" in p:
        fam = "Attention_VMamba_Fusion"
    elif "BoundaryAwareVMamba" in p:
        fam = "BoundaryAwareVMamba"
    elif "C3K2VSS" in p:
        fam = "C3K2VSS"
    elif "P3_CNN_VMamba" in p:
        fam = "P3_CNN_VMamba"
    elif "P5_VMamba" in p and "Attention" not in p:
        fam = "P5_VMamba_NoAttn"
    elif "TSVM" in p:
        fam = "TSVM"
    elif "Cac_Mo_Hinh_Khac" in p and "P5_Attention_VMamba" in p:
        fam = "P5_Attn_VMamba_OtherRuns"
    else:
        fam = f"Other_{top_folder}"
        
    categories.setdefault(fam, []).append(r)

print("\n--- MODEL FAMILIES AND RUN COUNTS ---")
for fam, items in categories.items():
    print(f"{fam}: {len(items)} runs")
    for it in items:
        p_mask = it['peak_metrics']['mask_map5095_max'] * 100 if it['peak_metrics']['mask_map5095_max'] is not None else 0
        p_box = it['peak_metrics']['box_map5095_max'] * 100 if it['peak_metrics']['box_map5095_max'] is not None else 0
        b_ep = it['best_epoch']
        model_name = it['model_arg']
        print(f"  - {it['rel_path']} (Epochs: {it['epochs_run']}, BestEp: {b_ep}) -> Mask mAP50-95: {p_mask:.2f}%, Box mAP50-95: {p_box:.2f}% | Model: {model_name}")

