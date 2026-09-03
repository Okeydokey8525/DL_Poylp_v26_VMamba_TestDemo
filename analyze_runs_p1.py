import os
import glob
import json
import pandas as pd
import numpy as np
import hashlib
import sys
from collections import defaultdict
import yaml

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

def get_file_size(path):
    if not os.path.exists(path): return "N/A"
    try:
        return os.path.getsize(path)
    except:
        return "ERROR"

def parse_metadata_from_name(name):
    # Try to extract seed, run, gpu, model variant
    seed = None
    run = None
    gpu = None
    batch = None
    epochs = None
    
    parts = name.split('_')
    for p in parts:
        if p.startswith('se') and p != 'seg':
            if p.startswith('seed'):
                try: seed = int(p.replace('seed', ''))
                except: pass
            else:
                try: seed = int(p.replace('se', ''))
                except: pass
        elif p.startswith('la') and 'lan' not in p:
            try: run = int(p.replace('la', ''))
            except: pass
        elif p.startswith('lan'):
            try: run = int(p.replace('lan', ''))
            except: pass
        elif p.endswith('de'):
            try: gpu = int(p.replace('de', ''))
            except: pass
        elif p.endswith('b'):
            try: batch = int(p.replace('b', ''))
            except: pass
        elif p.endswith('e') and p != '100e': # wait 100e is epochs
            try: epochs = int(p.replace('e', ''))
            except: pass
        elif p.endswith('epochs'):
            try: epochs = int(p.replace('epochs', ''))
            except: pass

    # If epochs not caught by 'e' loop safely
    for p in parts:
        if p.endswith('e') and not p.endswith('de') and not p.endswith('se'):
            try: epochs = int(p.replace('e', ''))
            except: pass
            
    return {'seed': seed, 'run': run, 'gpu': gpu, 'batch': batch, 'epochs': epochs}

def load_yaml(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return {}

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

# Define Groups
GROUPS = ['Baseline_1GPU', 'Baseline_2GPU', 'P3_1GPU', 'P3_2GPU']

runs_data = []

# 1. Discover all runs
for group in GROUPS:
    group_path = os.path.join(BASE_DIR, group)
    if not os.path.isdir(group_path): continue
    
    for folder in os.listdir(group_path):
        folder_path = os.path.join(group_path, folder)
        if not os.path.isdir(folder_path): continue
        
        # Find args.yaml
        args_path = None
        for root, dirs, files in os.walk(folder_path):
            if 'args.yaml' in files:
                args_path = os.path.join(root, 'args.yaml')
                break
                
        if not args_path:
            continue
            
        run_dir = os.path.dirname(args_path)
        
        # Meta
        meta = parse_metadata_from_name(folder)
        
        # ID gen
        # B1G-S0-R1
        g_abbr = "B1G" if group == "Baseline_1GPU" else "B2G" if group == "Baseline_2GPU" else "P31G" if group == "P3_1GPU" else "P32G"
        r_id = f"{g_abbr}-S{meta['seed']}-R{meta['run']}"
        
        model_family = "Baseline" if "Baseline" in group else "P3"
        gpu_count = 1 if "1GPU" in group else 2
        
        runs_data.append({
            'run_id': r_id,
            'group': group,
            'folder_name': folder,
            'folder_path': folder_path,
            'run_dir': run_dir,
            'model_family': model_family,
            'meta_seed': meta['seed'],
            'meta_run': meta['run'],
            'meta_gpu': gpu_count,
            'meta_batch': meta['batch'],
            'meta_epochs': meta['epochs']
        })

print(f"Discovered {len(runs_data)} runs")
