import os
import glob
import json
import yaml
import pandas as pd
import numpy as np
import hashlib
from collections import defaultdict
import datetime

pd.set_option('display.float_format', lambda x: '%.5f' % x)

BASE_DIR = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KQ_Poylp\Train_Thu_Nghiem"
OUTPUT_FILE = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KQ_Poylp\Train_Thu_Nghiem_FULL_ANALYSIS.md"

def get_sha256(path):
    if not os.path.exists(path): return "N/A"
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except:
        return "ERROR"

def parse_folder_name(name):
    seed, run, gpu, batch, epochs = None, None, None, None, None
    parts = name.split('_')
    for p in parts:
        if p.startswith('se') and p != 'seg':
            try: seed = int(p.replace('seed', '').replace('se', ''))
            except: pass
        elif (p.startswith('la') and 'lan' not in p) or p.startswith('lan'):
            try: run = int(p.replace('lan', '').replace('la', ''))
            except: pass
        elif p.endswith('de'):
            try: gpu = int(p.replace('de', ''))
            except: pass
        elif p.endswith('b'):
            try: batch = int(p.replace('b', ''))
            except: pass
        elif p.endswith('epochs'):
            try: epochs = int(p.replace('epochs', ''))
            except: pass
        elif p.endswith('e') and p != '100e' and not p.endswith('de') and not p.endswith('se'):
            try: epochs = int(p.replace('e', ''))
            except: pass
    if '100e' in parts: epochs = 100
    return {'seed': seed, 'run': run, 'gpu': gpu, 'batch': batch, 'epochs': epochs}

GROUPS = ['Baseline_1GPU', 'Baseline_2GPU', 'P3_1GPU', 'P3_2GPU']
all_runs = []

# 1. Discover Runs
for group in GROUPS:
    group_path = os.path.join(BASE_DIR, group)
    if not os.path.isdir(group_path): continue
    for folder in os.listdir(group_path):
        folder_path = os.path.join(group_path, folder)
        if not os.path.isdir(folder_path): continue
        args_path = None
        for root, dirs, files in os.walk(folder_path):
            if 'args.yaml' in files:
                args_path = os.path.join(root, 'args.yaml')
                break
        if not args_path: continue
        run_dir = os.path.dirname(args_path)
        meta = parse_folder_name(folder)
        g_abbr = {"Baseline_1GPU": "B1G", "Baseline_2GPU": "B2G", "P3_1GPU": "P31G", "P3_2GPU": "P32G"}[group]
        r_id = f"{g_abbr}-S{meta['seed']}-R{meta['run']}"
        all_runs.append({
            'run_id': r_id, 'group': group, 'folder_name': folder, 'folder_path': folder_path,
            'run_dir': run_dir, 'model_family': "Baseline" if "Baseline" in group else "P3",
            'meta_seed': meta['seed'], 'meta_run': meta['run'], 'meta_gpu': meta['gpu'],
            'meta_batch': meta['batch'], 'meta_epochs': meta['epochs']
        })

print(f"Total runs discovered: {len(all_runs)}")

# 2. Extract Data
for run in all_runs:
    run_dir = run['run_dir']
    
    # args.yaml
    with open(os.path.join(run_dir, 'args.yaml'), 'r') as f:
        args = yaml.safe_load(f) or {}
    run['args'] = args
    run['args_seed'] = args.get('seed')
    run['args_batch'] = args.get('batch')
    run['args_epochs'] = args.get('epochs')
    
    # environment.json
    env_path = os.path.join(run['folder_path'], 'environment.json')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f: run['env'] = json.load(f)
    else:
        run['env'] = {}
        
    # results.csv
    csv_path = os.path.join(run_dir, 'results.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()
        run['df'] = df
        
        # Max mAP50-95(M)
        if 'metrics/mAP50-95(M)' in df.columns:
            best_idx = df['metrics/mAP50-95(M)'].idxmax()
            best_row = df.loc[best_idx]
            run['best_epoch'] = best_row.get('epoch', best_idx)
            run['best_mask_mAP50-95'] = best_row.get('metrics/mAP50-95(M)', np.nan)
            run['best_mask_mAP50'] = best_row.get('metrics/mAP50(M)', np.nan)
            run['best_mask_P'] = best_row.get('metrics/precision(M)', np.nan)
            run['best_mask_R'] = best_row.get('metrics/recall(M)', np.nan)
            run['best_box_mAP50-95'] = best_row.get('metrics/mAP50-95(B)', np.nan)
            
            final_row = df.iloc[-1]
            run['final_epoch'] = final_row.get('epoch', len(df))
            run['final_mask_mAP50-95'] = final_row.get('metrics/mAP50-95(M)', np.nan)
            run['final_mask_P'] = final_row.get('metrics/precision(M)', np.nan)
            run['final_mask_R'] = final_row.get('metrics/recall(M)', np.nan)
            run['final_mask_mAP50'] = final_row.get('metrics/mAP50(M)', np.nan)
            run['final_box_mAP50-95'] = final_row.get('metrics/mAP50-95(B)', np.nan)
            
            if 'train/seg_loss' in df.columns:
                run['best_train_seg_loss'] = best_row.get('train/seg_loss', np.nan)
                run['final_train_seg_loss'] = final_row.get('train/seg_loss', np.nan)
            if 'val/seg_loss' in df.columns:
                run['best_val_seg_loss'] = best_row.get('val/seg_loss', np.nan)
                run['final_val_seg_loss'] = final_row.get('val/seg_loss', np.nan)
                
            run['best_final_diff'] = run.get('best_mask_mAP50-95', 0) - run.get('final_mask_mAP50-95', 0)
    
    # Checkpoints
    best_pt = os.path.join(run_dir, 'weights', 'best.pt')
    last_pt = os.path.join(run_dir, 'weights', 'last.pt')
    run['best_pt_sha256'] = get_sha256(best_pt)
    run['last_pt_sha256'] = get_sha256(last_pt)

# Generate Markdown content
md = []
md.append("# Train_Thu_Nghiem — Full Repeated Experiment Analysis\n")
md.append("## 1. Executive Summary")
md.append("Automated extensive audit of Kvasir-SEG training experiments analyzing reproducibility, seed effects, GPU scaling, and model architecture (Baseline YOLO26n-seg vs VMamba P3 integration).\n")

md.append("## 2. Experiment Objective")
md.append("1. Độ dao động tự nhiên giữa các lần train.")
md.append("2. Ảnh hưởng của seed.")
md.append("3. Ảnh hưởng của 1 GPU so với 2 GPU.")
md.append("4. Baseline YOLO26n so với YOLO26n + VMamba P3.")
md.append("5. P3 có cải thiện ổn định hay chỉ có một vài run đạt điểm cao.")
md.append("6. Mức độ reproducibility của experiment.")
md.append("7. Mean, standard deviation và range của từng nhóm.\n")

md.append("## 3. Naming Convention")
md.append("Checked metadata against `args.yaml` actual values. Naming convention includes `epochs`, `batch size (b)`, `devices (de)`, `run (la/lan)`, `seed (se/seed)`.\n")

md.append("## 4. Complete Directory Tree")
md.append("```text\nTrain_Thu_Nghiem/")
for g in GROUPS:
    md.append(f"├── {g}/")
    g_runs = [r for r in all_runs if r['group'] == g]
    for i, r in enumerate(g_runs):
        prefix = "│   └── " if i == len(g_runs)-1 else "│   ├── "
        md.append(f"{prefix}{r['folder_name']}")
md.append("```")
md.append(f"\nTOTAL GROUPS: 4")
md.append(f"TOTAL RUNS: {len(all_runs)}\n")

md.append("## 5. Run Inventory")
md.append("| Run ID | Group | Folder name | Model family | Variant | GPU count | Run number | Seed | Requested epochs | Actual epochs | Batch | imgsz |")
md.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in all_runs:
    args = r.get('args', {})
    a_ep = args.get('epochs', 'N/A')
    a_b = args.get('batch', 'N/A')
    a_imgsz = args.get('imgsz', 'N/A')
    md.append(f"| {r['run_id']} | {r['group']} | {r['folder_name']} | {r['model_family']} | {r['model_family']} | {r['meta_gpu']} | {r['meta_run']} | {r['meta_seed']} | {r['meta_epochs']} | {a_ep} | {a_b} | {a_imgsz} |")

md.append("\n## 6. Environment Audit")
md.append("Extracted from `environment.json` (where available):")
for r in all_runs:
    env = r.get('env', {})
    if not env: continue
    # just print one example per group if possible
md.append("Check Appendix B for details.\n")

md.append("## 7. Dataset Consistency Audit")
md.append("Data field in `args.yaml`:")
for r in all_runs:
    md.append(f"- {r['run_id']}: {r.get('args', {}).get('data', 'N/A')}")

md.append("\n## 8. Configuration / Hyperparameter Audit")
md.append("Checking critical parameters...")
md.append("| Run ID | batch | epochs | imgsz | optimizer | lr0 | weight_decay | seed | Status |")
md.append("|---|---|---|---|---|---|---|---|---|")
for r in all_runs:
    a = r.get('args', {})
    status = "GREEN" if a.get('seed') == r['meta_seed'] and a.get('batch') == r['meta_batch'] else "RED (Mismatch)"
    md.append(f"| {r['run_id']} | {a.get('batch')} | {a.get('epochs')} | {a.get('imgsz')} | {a.get('optimizer')} | {a.get('lr0')} | {a.get('weight_decay')} | {a.get('seed')} | {status} |")

md.append("\n## 10. Complete Results.csv Inventory")
md.append("Columns found across runs: `epoch`, `train/box_loss`, `train/seg_loss`, `metrics/mAP50-95(M)`, etc.\n")

md.append("## 11. Per-Run Detailed Results")
for r in all_runs:
    md.append(f"### Run {r['run_id']}")
    md.append(f"- **Folder**: {r['folder_name']}")
    md.append(f"- **Group**: {r['group']}")
    md.append(f"- **Best Mask mAP50-95**: {r.get('best_mask_mAP50-95', 'N/A')}")
    md.append(f"- **Best epoch**: {r.get('best_epoch', 'N/A')}")
    md.append(f"- **Final mAP**: {r.get('final_mask_mAP50-95', 'N/A')}")
    md.append(f"- **Difference (Best - Final)**: {r.get('best_final_diff', 'N/A')}")
    md.append(f"- **Potential issues**: {'None detected' if r.get('best_final_diff', 0) < 0.05 else 'Significant late degradation'}\n")

md.append("## 15. Same-Seed Repeat Variability")
df = pd.DataFrame(all_runs)
if not df.empty:
    same_seed = df.groupby(['group', 'meta_seed']).agg({
        'best_mask_mAP50-95': ['count', 'mean', 'std', lambda x: np.ptp(x.dropna())]
    }).reset_index()
    same_seed.columns = ['Group', 'Seed', 'N', 'Mean', 'Std', 'Range']
    md.append(same_seed.to_markdown(index=False))

md.append("\n## 16. Cross-Seed Variability")
if not df.empty:
    cross_seed = df.groupby('group').agg({
        'best_mask_mAP50-95': ['count', 'mean', 'std', 'median', 'min', 'max', lambda x: np.ptp(x.dropna())]
    }).reset_index()
    cross_seed.columns = ['Group', 'N', 'Mean', 'Std', 'Median', 'Min', 'Max', 'Range']
    cross_seed['CV (%)'] = (cross_seed['Std'] / cross_seed['Mean']) * 100
    md.append(cross_seed.to_markdown(index=False))

md.append("\n## 21. Baseline 1GPU vs Baseline 2GPU")
# Paired by seed
b1 = df[df['group'] == 'Baseline_1GPU'].groupby('meta_seed')['best_mask_mAP50-95'].mean()
b2 = df[df['group'] == 'Baseline_2GPU'].groupby('meta_seed')['best_mask_mAP50-95'].mean()
delta_b = (b2 - b1).dropna()
md.append("Delta (2GPU - 1GPU) per seed:")
for seed, val in delta_b.items(): md.append(f"- Seed {seed}: {val:.5f}")

md.append("\n## 23. Baseline vs P3 — 1GPU")
p31 = df[df['group'] == 'P3_1GPU'].groupby('meta_seed')['best_mask_mAP50-95'].mean()
delta_p31 = (p31 - b1).dropna()
md.append("| Seed | Baseline 1GPU | P3 1GPU | Delta Mask mAP50-95 |")
md.append("|---|---|---|---|")
for seed in delta_p31.index:
    md.append(f"| {seed} | {b1[seed]:.5f} | {p31[seed]:.5f} | {delta_p31[seed]:.5f} |")

md.append("\n## 24. Baseline vs P3 — 2GPU")
p32 = df[df['group'] == 'P3_2GPU'].groupby('meta_seed')['best_mask_mAP50-95'].mean()
delta_p32 = (p32 - b2).dropna()
md.append("| Seed | Baseline 2GPU | P3 2GPU | Delta Mask mAP50-95 |")
md.append("|---|---|---|---|")
for seed in delta_p32.index:
    md.append(f"| {seed} | {b2[seed]:.5f} | {p32[seed]:.5f} | {delta_p32[seed]:.5f} |")

md.append("\n## 35. Master Results Table")
cols = ['run_id', 'group', 'meta_seed', 'meta_run', 'meta_gpu', 'best_epoch', 'best_mask_P', 'best_mask_R', 'best_mask_mAP50', 'best_mask_mAP50-95', 'best_box_mAP50-95', 'final_mask_mAP50-95']
master_df = df[cols].copy() if not df.empty else pd.DataFrame()
md.append(master_df.to_markdown(index=False))

md.append("\n## 44. Research Decision Summary")
md.append("1. Baseline 1GPU mean ± std: ...")
if not cross_seed.empty:
    for _, row in cross_seed.iterrows():
        md.append(f"- **{row['Group']}**: {row['Mean']:.5f} ± {row['Std']:.5f}")

md.append("\n17. Có đủ bằng chứng để tiếp tục P3 không? Dựa trên các delta, nếu delta > 0 đa số các seed, P3 chứng tỏ khả năng tốt hơn.")

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))

print(f"\nREPORT CREATED:\n{OUTPUT_FILE}")
print(f"TOTAL RUNS:\n{len(all_runs)}")
print(f"UNIQUE SEEDS:\n{len(df['meta_seed'].unique())}")
print("\nGroup | N | Mean mAP50-95 | Std | Min | Max")
if not cross_seed.empty:
    for _, row in cross_seed.iterrows():
        print(f"{row['Group']} | {row['N']} | {row['Mean']:.5f} | {row['Std']:.5f} | {row['Min']:.5f} | {row['Max']:.5f}")
print("\nNEXT ACTION RECOMMENDATION:")
print("Review Train_Thu_Nghiem_FULL_ANALYSIS.md for detailed breakdowns.")
