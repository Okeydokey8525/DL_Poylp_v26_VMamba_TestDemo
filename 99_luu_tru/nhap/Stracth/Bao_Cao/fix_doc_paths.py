"""
fix_doc_paths.py — TU ĐỘNG SỬA ĐƯỜNG DẪN HỎNG trong doc/*.md
Chỉ sửa các quy tắc đổi tên có tính quyết định (deterministic).
Mặc định chạy ở chế độ CHẾ ĐỘ XEM TRƯỚC (dry-run); thêm --apply để ghi file.
"""
from __future__ import annotations
import io, re, sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
APPLY = "--apply" in sys.argv

# (mẫu cũ, mẫu mới) — thứ tự quan trọng: mẫu dài hơn phải đứng trước
RULES = [
    # doc/ mo ta cau truc cu (khong sua - chi thong ke)
    ("archive/KQ_Nen_DX_10seed/", "archive/Ket_Qua_V2/KQ_Nen_DX_10seed/"),
    ("archive/KQ_Nen_DX_10seed`", "archive/Ket_Qua_V2/KQ_Nen_DX_10seed`"),
    ("archive/KQ_Nen_DX_10seed\"", "archive/Ket_Qua_V2/KQ_Nen_DX_10seed\""),
    ("archive/KQ_Nen_DX_10seed)", "archive/Ket_Qua_V2/KQ_Nen_DX_10seed)"),
    ("archive/KQ_Nen_DX_10seed ", "archive/Ket_Qua_V2/KQ_Nen_DX_10seed "),
    ("archive/KQ_Nen_DX_10seed\n", "archive/Ket_Qua_V2/KQ_Nen_DX_10seed\n"),
    ("archive/KQ_Nen_DX_10seed", "archive/Ket_Qua_V2/KQ_Nen_DX_10seed"),
    # KetQua_Nen -> Ket_Qua_V2/KetQua_Nen
    ("archive/KetQua_Nen/", "archive/Ket_Qua_V2/KetQua_Nen/"),
    ("archive/KetQua_Nen`", "archive/Ket_Qua_V2/KetQua_Nen`"),
    ("archive/KetQua_Nen\n", "archive/Ket_Qua_V2/KetQua_Nen\n"),
    ("archive/KetQua_Nen", "archive/Ket_Qua_V2/KetQua_Nen"),
    # efficiency_benchmark nam trong KQ_Nen_DX_10seed
    ("archive/efficiency_benchmark/", "archive/Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/"),
    ("archive/efficiency_benchmark", "archive/Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark"),
    # dataset
    ("archive/Kvasir_YOLO_SEG_BG20/", "archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/"),
    ("archive/Kvasir_YOLO_SEG_BG20", "archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20"),
    ("archive/Kvasir_YOLO_SEG/", "archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/"),
    ("archive/Kvasir_YOLO_SEG", "archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20"),
    # script chuyen sang thu muc Stracth/
    ("archive/convert_kvasir_to_yolo_seg.py", "archive/Stracth/convert_kvasir_to_yolo_seg.py"),
    ("archive/convert_datasets_to_yolo_seg.py", "archive/Stracth/convert_datasets_to_yolo_seg.py"),
    # file o cap archive/
    ("archive/data_bg20.yaml", "archive/data_bg20.yaml"),
]

# cac file .md CHINH (khong sua historical)
TARGETS = sorted(ROOT.glob("doc/*.md")) + sorted(ROOT.glob("*.md"))

print("=" * 92)
print("TU DONG SUA DUONG DAN HONG" + ("  [CHAY THAT]" if APPLY else "  [CHAY THU - them --apply de ghi file]"))
print("=" * 92)

total = 0
for md in TARGETS:
    s = md.read_text(encoding="utf-8", errors="replace")
    orig = s
    counts = []
    for old, new in RULES:
        n = s.count(old)
        if n:
            s = s.replace(old, new)
            counts.append(f"{old!r}->{new!r} x{n}")
    if s != orig:
        total += sum(1 for c in counts)
        rel = md.relative_to(ROOT)
        print(f"\n[{rel}]  {len(counts)} quy tac")
        for c in counts:
            print("   ", c)
        if APPLY:
            md.write_text(s, encoding="utf-8")
            print("    -> DA GHI FILE")

print("\n" + "=" * 92)
print(f"Tong so file thay doi: {sum(1 for md in TARGETS if md.read_text(encoding='utf-8', errors='replace') != md.read_text(encoding='utf-8', errors='replace'))}"
      if not APPLY else f"Da ghi {total} quy tac vao file.")
print("=" * 92)
if not APPLY:
    print("\nChay lai voi:  python .\\Stracth\\fix_doc_paths.py --apply")
