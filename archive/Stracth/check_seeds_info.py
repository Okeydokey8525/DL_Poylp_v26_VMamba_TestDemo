import os, yaml
from pathlib import Path

base_dir = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen")

for s in range(6):
    f = base_dir / f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2" / "args.yaml"
    if f.exists():
        with open(f, 'r') as fp:
            cfg = yaml.safe_load(fp)
        print(f"Seed {s}: seed={cfg.get('seed')}, end2end={cfg.get('end2end')}, nms={cfg.get('nms')}, batch={cfg.get('batch')}")
