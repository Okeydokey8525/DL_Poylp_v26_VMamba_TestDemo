"""
================================================================================
check_doc_paths.py  —  KIỂM TRA ĐƯỜNG DẪN HỎNG TRONG TÀI LIỆU MARKDOWN
================================================================================
Tác giả : Nhóm nghiên cứu CNTT_KLCN182
Ngày   : 02/10/2026
Mục đích: Quét mọi tệp `.md` trong `doc/` và thư mục gốc `archive/`, phát hiện
          đường dẫn tới thư mục/tệp KHÔNG tồn tại.

CÁCH DÙNG
---------
    python Stracth/check_doc_paths.py            # xuất tóm tắt
    python Stracth/check_doc_paths.py --fix-hint # in gợi ý đường dẫn thay thế

KẾT QUẢ: ghi `doc/historical/../24_...` ? Không — in ra màn hình và
          `Ket_Qua_V2/KQ_Nen_DX_10seed/07_audit/doc_path_report.csv`.
================================================================================
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent          # .../archive
OUT = ROOT / "Ket_Qua_V2" / "KQ_Nen_DX_10seed" / "07_audit"
OUT.mkdir(parents=True, exist_ok=True)

# các thư mục hợp lệ ở cấp archive/
VALID_TOP = {
    "Ket_Qua_V2", "Kvasir-SEG", "Cac_Dataset", "Stracth",
    "ultralytics_Topology-Shape-aware VMamba", "normal-cecum", "doc",
    "Khac_phuc",
}
# tiền tố đường dẫn đã bị đổi theo thời gian -> ánh xạ sang vị trí hiện tại
RENAME_HINTS = {
    "archive/KQ_Nen_DX_10seed": "archive/Ket_Qua_V2/KQ_Nen_DX_10seed",
    "archive/KetQua_Nen":       "archive/Ket_Qua_V2/KetQua_Nen",
    "archive/efficiency_benchmark": "archive/Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark",
    "archive/KQ_DoiXung":       "archive/Ket_Qua_V2/KQ_Nen_DX_10seed",
    "archive/Ket_Qua_V1":       "(không còn trong repo — xem doc/historical/)",
    "archive/Ket_Qua_2":        "(không còn trong repo — xem doc/historical/)",
    "archive/Kvasir_YOLO_SEG":  "archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20",
    "archive/Kvasir_YOLO_SEG_BG20": "archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20",
    "archive/data_bg20.yaml":   "archive/data_bg20.yaml",
    "archive/convert_kvasir_to_yolo_seg.py": "archive/Stracth/convert_kvasir_to_yolo_seg.py",
}

MD_FILES = sorted(ROOT.glob("doc/*.md")) + sorted(ROOT.glob("doc/historical/**/*.md")) \
         + sorted(ROOT.glob("*.md"))

# Tệp báo cáo tự trích dẫn các đường dẫn hỏng làm ví dụ / liệt kê thư mục đã bị xoá
# -> bỏ qua để tránh báo động giả
SELF_REPORT = {
    "24_DANH_SACH_DUONG_DAN_HONG.md",
    "21_HUONG_DAN_BAN_GIAO_AI_MOI_VA_VIEC_CONG_TAI.md",
    "LICHSU_CAP_NHAT.md",
    "23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md",
}
MD_FILES = [m for m in MD_FILES if m.name not in SELF_REPORT]

# nhận diện đường dẫn dạng archive/... hoặc file://.../archive/...
PAT_FILEURL = re.compile(r"file:///([A-Za-z]:[^)\"'\s]*archive/[^\s)\"']+)")
# thư mục có khoảng trắng trong tên -> phải khớp trước
_SPACED_DIR = r"ultralytics_Topology-Shape-aware VMamba"
PAT_PLAIN = re.compile(
    r"\barchive/(?:_SPACED_|[A-Za-z0-9_.\-]+)(?:/[A-Za-z0-9_.\-]+)*".replace("_SPACED_", _SPACED_DIR)
)
# cắt anchor (#L233, #section) và ký tự markdown ở cuối đường dẫn
TRAIL = re.compile(r"[>)\]\"'`#,;:]+$")
ANCHOR = re.compile(r"#.*$")

# các thư mục/tệp KHÔNG được coi là đường dẫn (artifact của regex)
SKIP_TOKENS = {"archive"}


def clean(p: str) -> str:
    """Loại anchor + ký tự markdown thừa, rstrip ký tự phân tách."""
    return ANCHOR.sub("", TRAIL.sub("", p)).rstrip("/.,;: ")


def resolve(rel: str) -> Path | None:
    """Chuyển 'archive/xxx' thành đường dẫn tuyệt đối trên đĩa."""
    if not rel.startswith("archive"):
        return None
    tail = rel.split("/", 1)[1] if "/" in rel else ""
    return (ROOT / tail) if tail else None


def main() -> int:
    print("=" * 96)
    print("KIỂM TRA ĐƯỜNG DẪN HỎNG TRONG TÀI LIỆU MARKDOWN")
    print(f"{datetime.now():%d/%m/%Y %H:%M:%S}   —   quét {len(MD_FILES)} tệp .md")
    print("=" * 96)

    rows: list[dict] = []
    seen: set[tuple[str, str]] = set()

    for md in MD_FILES:
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            cands: list[str] = []
            for m in PAT_FILEURL.finditer(line):
                idx = m.group(1).find("archive/")
                if idx >= 0:
                    raw = clean(m.group(1)[idx:])
                    if raw:
                        cands.append(raw)
            for m in PAT_PLAIN.finditer(line):
                raw = clean(m.group(0))
                if raw and raw not in SKIP_TOKENS:
                    cands.append(raw)
            for rel in cands:
                key = (str(md.relative_to(ROOT)), rel)
                if key in seen:
                    continue
                seen.add(key)
                top = rel.split("/")[1] if len(rel.split("/")) > 1 else ""
                target = resolve(rel)
                ok = target is not None and target.exists()
                if top not in VALID_TOP:
                    if not ok:
                        rows.append({
                            "file": key[0], "line": line_no, "duong_dan": rel,
                            "nguyen_nhan": "tệp ở cấp archive/ không tồn tại",
                            "goi_y": RENAME_HINTS.get(rel.rstrip("/"), ""),
                        })
                    continue
                if not ok:
                    rows.append({
                        "file": key[0], "line": line_no, "duong_dan": rel,
                        "nguyen_nhan": "đường dẫn không tồn tại",
                        "goi_y": RENAME_HINTS.get(rel.rstrip("/"), ""),
                    })

    df_rows = rows
    by_file: dict[str, int] = {}
    for r in df_rows:
        by_file[r["file"]] = by_file.get(r["file"], 0) + 1

    print(f"\nTổng số đường dẫn hỏng: {len(df_rows)}\n")
    print(f"{'tệp .md':<52}{'số đường dẫn hỏng':>18}")
    print("-" * 70)
    for f, n in sorted(by_file.items(), key=lambda x: -x[1]):
        print(f"{f:<52}{n:>18}")

    print("\n--- Gợi ý sửa ---")
    seen_hint: set[str] = set()
    for r in df_rows:
        h = r["goi_y"]
        if h and h not in seen_hint:
            seen_hint.add(h)
            print(f"  {r['duong_dan']}\n      → {h}")

    import csv
    with open(OUT / "doc_path_report.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "line", "duong_dan", "nguyen_nhan", "goi_y"])
        w.writeheader()
        w.writerows(df_rows)
    print(f"\nBáo cáo chi tiết: {OUT / 'doc_path_report.csv'}")
    return 0 if not df_rows else 1


if __name__ == "__main__":
    raise SystemExit(main())
