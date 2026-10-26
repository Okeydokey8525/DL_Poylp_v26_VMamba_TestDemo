from rapidocr_onnxruntime import RapidOCR
from pathlib import Path

ocr = RapidOCR()
for s in [0, 5]:
    dir_p = Path(rf"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Khac_phuc\Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2")
    print(f"\n=== SEED {s} KHAC_PHUC OCR ===")
    for name in ["BoxPR_curve.png", "MaskPR_curve.png", "BoxF1_curve.png", "MaskF1_curve.png"]:
        f = dir_p / name
        res, _ = ocr(str(f))
        texts = [l[1] for l in res if any(k in l[1] for k in ["0.", "mAP", "all classes"])]
        print(f"  {name:<18}: {' | '.join(texts)}")
