"""TAM THOI - forensic: crop tung o CM + upscale + OCR (read-only)."""
import sys
from pathlib import Path
from PIL import Image
import numpy as np
from rapidocr_onnxruntime import RapidOCR

sys.stdout.reconfigure(encoding='utf-8')
ocr = RapidOCR()

ROOT = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive"
TSVM = ROOT + r"\Ket_Qua_V2\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM\Kvasir_BG20_YOLO26s_seg_TSVM_s{q}_w2"
BASE = ROOT + r"\Ket_Qua_V2\KetQua_Nen\YOLOv26s-seg\Kvasir_BG20_Baseline_YOLO26s_seg_s{q}_w2"

TARGETS = []
for q in [0, 1, 5, 8]:
    TARGETS.append((TSVM.format(q=q) + r"\confusion_matrix.png", f"TSVM s{q} raw"))
    TARGETS.append((TSVM.format(q=q) + r"\confusion_matrix_normalized.png", f"TSVM s{q} norm"))
TARGETS.append((BASE.format(q=0) + r"\confusion_matrix.png", "BASE s0 raw"))
TARGETS.append((ROOT + r"\Stracth\seed8_re_eval\val_run\confusion_matrix.png", "TSVM s8 seed8_re_eval raw"))

# cell boxes as fractions of (W,H): TL, TR, BL, BR
CELLS = {
    "TP(TL)": (0.22, 0.08, 0.50, 0.40),
    "FP(TR)": (0.50, 0.08, 0.78, 0.40),
    "FN(BL)": (0.22, 0.40, 0.50, 0.74),
    "TN(BR)": (0.50, 0.40, 0.78, 0.74),
}

for path, tag in TARGETS:
    p = Path(path)
    print("=" * 70)
    print(f"[{tag}] exists={p.exists()}")
    if not p.exists():
        continue
    im = Image.open(p).convert("RGB")
    W, H = im.size
    a = np.asarray(im)
    vals = {}
    for name, (x0f, y0f, x1f, y1f) in CELLS.items():
        crop = im.crop((int(x0f * W), int(y0f * H), int(x1f * W), int(y1f * H)))
        crop = crop.resize((crop.width * 3, crop.height * 3), Image.LANCZOS)
        res, _ = ocr(np.asarray(crop))
        txt = " ".join(t[1] for t in res) if res else ""
        vals[name] = txt
    # detect emptiness via pixel variance in the numeric area
    print(f"  size={W}x{H}")
    for k, v in vals.items():
        print(f"    {k:<8} OCR='{v}'")