import cv2
import numpy as np
from pathlib import Path

base_dir = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen")

for s in range(6):
    f_pr = base_dir / f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2" / "BoxPR_curve.png"
    f_f1 = base_dir / f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2" / "BoxF1_curve.png"
    if f_pr.exists():
        img = cv2.imread(str(f_pr))
        print(f"Seed {s}: BoxPR shape={img.shape if img is not None else None}")
