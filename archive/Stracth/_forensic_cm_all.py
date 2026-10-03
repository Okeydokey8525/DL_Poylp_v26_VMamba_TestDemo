"""TAM THOI - forensic: OCR toan bo 20 CM (tight crop) va doi chieu voi CSV (read-only)."""
import sys
import csv
from pathlib import Path
from PIL import Image
import numpy as np
from rapidocr_onnxruntime import RapidOCR

sys.stdout.reconfigure(encoding='utf-8')
ocr = RapidOCR()

ROOT = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive")
KP = ROOT / "Ket_Qua_V2" / "KetQua_Nen"
CM_CSV = ROOT / "Ket_Qua_V2" / "KQ_Nen_DX_10seed" / "01_raw_analysis" / "raw_10seeds_confusion_matrices.csv"

# all images are 3000x2250; number centres approx (x,y)
BOXES = {
    "TP": (890, 404, 1330, 644),    # top-left  (pred polyp , true polyp)
    "FP": (1670, 404, 2110, 644),   # top-right (pred polyp , true background)
    "FN": (890, 1182, 1330, 1422),  # bottom-left (pred bg, true polyp)
    "TN": (1670, 1182, 2110, 1422),  # bottom-right (pred bg, true bg)
}


def cell(img, box):
    c = img.crop(box)
    c = c.resize((c.width * 4, c.height * 4), Image.LANCZOS)
    res, _ = ocr(np.asarray(c))
    if not res:
        return None
    # keep only numeric-ish
    for t in res:
        s = t[1].replace(" ", "").replace(",", ".").replace("O", "0").replace("l", "1")
        try:
            return int(round(float(s)))
        except ValueError:
            continue
    return None


def cells(path):
    im = Image.open(path).convert("RGB")
    return {k: cell(im, b) for k, b in BOXES.items()}


csv_rows = {}
with open(CM_CSV, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        csv_rows[(r["model"], int(r["seed"]))] = r

print(f"{'run':<12}{'img TP':>7}{'csv TP':>7} | {'img FP':>7}{'csv FP':>7} | {'img FN':>7}{'csv FN':>7} | status")
print("-" * 78)
for model, folder in [("Baseline", "YOLOv26s-seg"), ("TSVM", "Kvasir_BG20_YOLO26s_seg_TSVM")]:
    for s in range(10):
        if model == "Baseline":
            d = KP / folder / f"Kvasir_BG20_Baseline_YOLO26s_seg_s{s}_w2"
        else:
            d = KP / folder / f"Kvasir_BG20_TSVM_s{s}_w2" if False else KP / folder / f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2"
        p = d / "confusion_matrix.png"
        g = cells(p) if p.exists() else {}
        c = csv_rows[(model, s)]
        itp, ifp, ifn = g.get("TP"), g.get("FP"), g.get("FN")
        ctp, cfp, cfn = int(c["TP"]), int(c["FP"]), int(c["FN"])
        ok = (itp == ctp) and (ifp == cfp) and (ifn == cfn)
        print(f"{model[:4]+' s'+str(s):<12}{str(itp):>7}{ctp:>7} | {str(ifp):>7}{cfp:>7} | {str(ifn):>7}{cfn:>7} | {'MATCH' if ok else 'MISMATCH'}")