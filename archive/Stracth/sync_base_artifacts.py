import os, shutil
from pathlib import Path

src_root = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen")
dst_root = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Khac_phuc")

files_to_copy = [
    "labels.jpg",
    "train_batch0.jpg",
    "train_batch1.jpg",
    "train_batch2.jpg",
    "train_batch11700.jpg",
    "train_batch11701.jpg",
    "train_batch11702.jpg",
    "val_batch0_labels.jpg",
    "val_batch1_labels.jpg",
    "val_batch2_labels.jpg",
    "results.png",
    "results.csv",
    "args.yaml",
]

for s in [0, 5]:
    folder_name = f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2"
    src_folder = src_root / folder_name
    dst_folder = dst_root / folder_name
    dst_folder.mkdir(parents=True, exist_ok=True)
    
    # Copy files
    for f in files_to_copy:
        src_file = src_folder / f
        if src_file.exists():
            shutil.copy2(src_file, dst_folder / f)
            print(f"[{folder_name}] Copied {f}")
        else:
            print(f"[{folder_name}] Warning: {f} not found in source!")
            
    # Copy weights
    src_weights = src_folder / "weights"
    dst_weights = dst_folder / "weights"
    if src_weights.exists():
        dst_weights.mkdir(parents=True, exist_ok=True)
        for w in ["best.pt", "last.pt"]:
            if (src_weights / w).exists():
                shutil.copy2(src_weights / w, dst_weights / w)
                print(f"[{folder_name}] Copied weights/{w}")

print("Pre-sync completed successfully!")
