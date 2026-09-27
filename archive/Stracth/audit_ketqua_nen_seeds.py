import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

nen_dir = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen"

models = {
    "Baseline (YOLOv26s-seg)": "YOLOv26s-seg",
    "TSVM": "Kvasir_BG20_YOLO26s_seg_TSVM",
    "P5_Attention_VMamba": "Kvasir_BG20_YOLO26s_seg_P5_Attention_VMamba",
    "ITSMamba": "Kvasir_BG20_YOLO26s_seg_ITSMamba",
    "IAVM": "Kvasir_BG20_YOLO26s_seg_IAVM" if os.path.exists(os.path.join(nen_dir, "Kvasir_BG20_YOLO26s_seg_IAVM")) else "Kvasir_BG20_YOLO26s_seg",
}

print("=== THONG KE CHI TIET SO LUONG SEED THEO MO HINH TRONG KetQua_Nen ===\n")
total_seeds_all_models = 0

for model_name, subfolder in models.items():
    p = os.path.join(nen_dir, subfolder)
    if not os.path.exists(p):
        print(f"{model_name}: KHONG TIM THAY THU MUC {subfolder}")
        continue
    runs = [d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d))]
    import re
    def get_seed(folder_name):
        m = re.search(r'_s(\d+)_', folder_name)
        return int(m.group(1)) if m else 999

    runs_sorted = sorted(runs, key=get_seed)
    seeds = [get_seed(x) for x in runs_sorted if re.search(r'_s(\d+)_', x)]
    total_seeds_all_models += len(runs_sorted)
    
    csv_ok = all(os.path.exists(os.path.join(p, r, "results.csv")) for r in runs_sorted)
    weights_ok = all(os.path.exists(os.path.join(p, r, "weights", "best.pt")) for r in runs_sorted)
    
    print(f"Mô hình: {model_name}")
    print(f"  - Thư mục: {subfolder}")
    print(f"  - Tổng số seed: {len(runs_sorted)}")
    print(f"  - Danh sách seed: {seeds} (từ seed {min(seeds)} đến seed {max(seeds)})")
    print(f"  - results.csv: {'Day du' if csv_ok else 'Thieu'}")
    print(f"  - weights/best.pt: {'Day du' if weights_ok else 'Thieu'}")
    print()

print(f"TONG CONG TAT CA MO HINH: {total_seeds_all_models} runs/seeds.")
