import os
import sys
import gc
import time
import importlib.util
import psutil
import numpy as np
import pandas as pd
import torch
from thop import profile

def load_yolo_from_dir(pkg_dir):
    for k in list(sys.modules.keys()):
        if k == 'ultralytics' or k.startswith('ultralytics.'):
            del sys.modules[k]
    spec = importlib.util.spec_from_file_location(
        'ultralytics',
        os.path.join(pkg_dir, '__init__.py'),
        submodule_search_locations=[pkg_dir]
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules['ultralytics'] = mod
    spec.loader.exec_module(mod)
    from ultralytics import YOLO
    return YOLO

def run_benchmark():
    anti_up = r'c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Anti_Up'
    
    models_config = [
        {
            'model_name': 'YOLOv26s Baseline',
            'pkg_dir': os.path.join(anti_up, 'ultralytics_Topology-Shape-aware VMamba'),
            'ckpt_path': r'KetQua_Nen\YOLOv26s-seg\Kvasir_BG20_Baseline_YOLO26s_seg_s0_w2\weights\best.pt'
        },
        {
            'model_name': 'TSVM',
            'pkg_dir': os.path.join(anti_up, 'ultralytics_Topology-Shape-aware VMamba'),
            'ckpt_path': r'KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM\Kvasir_BG20_YOLO26s_seg_TSVM_s0_w2\weights\best.pt'
        },
        {
            'model_name': 'P5 Attention VMamba',
            'pkg_dir': os.path.join(anti_up, 'ultralytics_Attention_VMamba'),
            'ckpt_path': r'KetQua_Nen\Kvasir_BG20_YOLO26s_seg_P5_Attention_VMamba\Kvasir_BG20_YOLO26s_seg_P5_Attention_VMamba_s0_w2\weights\best.pt'
        },
        {
            'model_name': 'ITS Mamba',
            'pkg_dir': os.path.join(anti_up, 'ultralytics_Interactive_Topology_VMamba'),
            'ckpt_path': r'KetQua_Nen\Kvasir_BG20_YOLO26s_seg_ITSMamba\Kvasir_BG20_YOLO26s_seg_ITSMamba_s0_w2\weights\best.pt'
        }
    ]
    
    device_name = 'CPU'
    if torch.cuda.is_available():
        device = torch.device('cuda:0')
        device_name = torch.cuda.get_device_name(0)
    else:
        device = torch.device('cpu')
        
    print(f"Executing Efficiency Benchmark on {device_name}...")
    
    torch.set_grad_enabled(False)
    
    # Input tensor definition
    input_shape = (1, 3, 640, 640)
    torch.manual_seed(42)
    dummy_input = torch.randn(*input_shape, dtype=torch.float32, device=device)
    
    raw_records = []
    summary_records = []
    
    warmup_iters = 20
    test_iters = 100
    
    for cfg in models_config:
        mname = cfg['model_name']
        pkg = cfg['pkg_dir']
        ckpt = cfg['ckpt_path']
        print(f"\n--- Benchmarking {mname} ---")
        
        # Memory cleanup before model load
        gc.collect()
        process = psutil.Process()
        ram_before_mb = process.memory_info().rss / (1024 * 1024)
        
        # Load model
        YOLO_cls = load_yolo_from_dir(pkg)
        yolo_obj = YOLO_cls(ckpt)
        model = yolo_obj.model.to(device).eval()
        
        # Checkpoint size
        ckpt_size_mb = os.path.getsize(ckpt) / (1024 * 1024)
        
        # Count parameters
        total_params = sum(p.numel() for p in model.parameters())
        mparams = total_params / 1e6
        
        # Profile GFLOPs
        try:
            flops, _ = profile(model, inputs=(dummy_input,), verbose=False)
            gflops = flops / 1e9
        except Exception as e:
            print(f"Warning: GFLOPs profiling error on {mname}: {e}")
            gflops = np.nan
            
        # Warmup
        print(f"Warming up ({warmup_iters} iterations)...")
        for _ in range(warmup_iters):
            if device.type == 'cuda':
                torch.cuda.synchronize()
            _ = model(dummy_input)
            if device.type == 'cuda':
                torch.cuda.synchronize()
                
        # Benchmark timing
        print(f"Measuring latency ({test_iters} iterations)...")
        latencies_ms = []
        ram_peak_mb = ram_before_mb
        
        for it in range(test_iters):
            t0 = time.perf_counter()
            if device.type == 'cuda':
                torch.cuda.synchronize()
            _ = model(dummy_input)
            if device.type == 'cuda':
                torch.cuda.synchronize()
            t1 = time.perf_counter()
            
            dur_ms = (t1 - t0) * 1000.0
            latencies_ms.append(dur_ms)
            
            cur_ram_mb = process.memory_info().rss / (1024 * 1024)
            if cur_ram_mb > ram_peak_mb:
                ram_peak_mb = cur_ram_mb
                
            raw_records.append({
                'model_name': mname,
                'iteration': it + 1,
                'latency_ms': round(dur_ms, 3)
            })
            
        lat_arr = np.array(latencies_ms)
        mean_lat = float(np.mean(lat_arr))
        std_lat = float(np.std(lat_arr))
        p50 = float(np.percentile(lat_arr, 50))
        p95 = float(np.percentile(lat_arr, 95))
        p99 = float(np.percentile(lat_arr, 99))
        min_lat = float(np.min(lat_arr))
        max_lat = float(np.max(lat_arr))
        fps = 1000.0 / mean_lat if mean_lat > 0 else 0.0
        
        # Memory metrics
        ram_delta_mb = ram_peak_mb - ram_before_mb
        vram_peak_mb = 'N/A' if device.type == 'cpu' else round(torch.cuda.max_memory_allocated() / (1024 * 1024), 2)
        
        summary_records.append({
            'Model': mname,
            'Params_M': round(mparams, 3),
            'GFLOPs': round(gflops, 2),
            'Checkpoint_MB': round(ckpt_size_mb, 2),
            'Latency_Mean_ms': round(mean_lat, 2),
            'Latency_Std_ms': round(std_lat, 2),
            'P50_ms': round(p50, 2),
            'P95_ms': round(p95, 2),
            'P99_ms': round(p99, 2),
            'FPS': round(fps, 2),
            'Peak_RAM_MB': round(ram_peak_mb, 2),
            'RAM_Delta_MB': round(ram_delta_mb, 2),
            'Peak_VRAM_MB': vram_peak_mb
        })
        
        print(f"Summary for {mname}: Latency = {mean_lat:.2f} ms, P95 = {p95:.2f} ms, FPS = {fps:.2f}, RAM Peak = {ram_peak_mb:.1f} MB")
        
        # Cleanup
        del model
        del yolo_obj
        gc.collect()
        
    df_raw = pd.DataFrame(raw_records)
    raw_path = r'efficiency_benchmark\raw\efficiency_raw_benchmark.csv'
    df_raw.to_csv(raw_path, index=False)
    print(f"\nRaw iteration latencies saved to {raw_path} ({len(df_raw)} records)")
    
    df_summary = pd.DataFrame(summary_records)
    summary_path = r'efficiency_benchmark\tables\efficiency_summary.csv'
    df_summary.to_csv(summary_path, index=False)
    print(f"Efficiency summary saved to {summary_path}")
    
    # Accuracy from 10-seed
    # Baseline, TSVM, P5 Attention VMamba, ITS Mamba
    acc_data = {
        'YOLOv26s Baseline': {'mAP50-95': 0.7210, 'Std': 0.0129, 'Precision': 0.9023, 'Recall': 0.8584},
        'TSVM': {'mAP50-95': 0.7246, 'Std': 0.0078, 'Precision': 0.9118, 'Recall': 0.8625},
        'P5 Attention VMamba': {'mAP50-95': 0.7165, 'Std': 0.0075, 'Precision': 0.8983, 'Recall': 0.8338},
        'ITS Mamba': {'mAP50-95': 0.7203, 'Std': 0.0101, 'Precision': 0.9205, 'Recall': 0.8485}
    }
    
    joint_records = []
    for r in summary_records:
        m = r['Model']
        acc = acc_data[m]
        joint_records.append({
            'Model': m,
            'mAP50-95': acc['mAP50-95'],
            'Std': acc['Std'],
            'Precision': acc['Precision'],
            'Recall': acc['Recall'],
            'Params': r['Params_M'],
            'GFLOPs': r['GFLOPs'],
            'Latency': r['Latency_Mean_ms'],
            'P95': r['P95_ms'],
            'FPS': r['FPS'],
            'VRAM': r['Peak_VRAM_MB'],
            'Peak_RAM_MB': r['Peak_RAM_MB']
        })
        
    df_joint = pd.DataFrame(joint_records)
    joint_path = r'efficiency_benchmark\tables\accuracy_efficiency_summary.csv'
    df_joint.to_csv(joint_path, index=False)
    print(f"Accuracy-Efficiency summary saved to {joint_path}")

if __name__ == '__main__':
    run_benchmark()
