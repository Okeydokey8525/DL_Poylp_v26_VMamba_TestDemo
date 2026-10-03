"""TAM THOI - forensic: OCR confusion_matrix.png va in text + toa do (read-only)."""
import sys
from pathlib import Path
from rapidocr_onnxruntime import RapidOCR

sys.stdout.reconfigure(encoding='utf-8')
ocr = RapidOCR()

IMAGES = [
    (r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Ket_Qua_V2\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM\Kvasir_BG20_YOLO26s_seg_TSVM_s0_w2\confusion_matrix.png", "TSVM s0 KetQua_Nen"),
    (r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Ket_Qua_V2\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM\Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2\confusion_matrix.png", "TSVM s5 KetQua_Nen"),
    (r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Ket_Qua_V2\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM\Kvasir_BG20_YOLO26s_seg_TSVM_s8_w2\confusion_matrix.png", "TSVM s8 KetQua_Nen"),
    (r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Ket_Qua_V2\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM\Kvasir_BG20_YOLO26s_seg_TSVM_s1_w2\confusion_matrix.png", "TSVM s1 KetQua_Nen"),
    (r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Ket_Qua_V2\KetQua_Nen\YOLOv26s-seg\Kvasir_BG20_Baseline_YOLO26s_seg_s0_w2\confusion_matrix.png", "BASE s0 KetQua_Nen"),
    (r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\seed5_re_eval\val_run\confusion_matrix.png", "TSVM s5 seed5_re_eval"),
    (r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\seed8_re_eval\val_run\confusion_matrix.png", "TSVM s8 seed8_re_eval"),
    (r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\eval_s5_test\val_test\confusion_matrix.png", "TSVM s5 eval_s5_test"),
    (r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\test_val_plots\confusion_matrix.png", "test_val_plots (unknown ckpt)"),
]

for img, tag in IMAGES:
    p = Path(img)
    print("=" * 80)
    print(f"[{tag}] exists={p.exists()}  {p}")
    if not p.exists():
        continue
    print(f"  size = {p.stat().st_size} bytes")
    res, _ = ocr(str(p))
    if not res:
        print("  OCR: NO TEXT")
        continue
    for item in res:
        pts = item[0]
        cx = sum(q[0] for q in pts) / 4.0
        cy = sum(q[1] for q in pts) / 4.0
        print(f"  text='{item[1]}'  c=({cx:.0f},{cy:.0f})")