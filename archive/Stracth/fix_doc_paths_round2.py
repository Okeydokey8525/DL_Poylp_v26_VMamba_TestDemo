"""
fix_doc_paths_round2.py — Sua 21 duong dan hong that trong doc/*.md (v3.1)

Phuong an da duyet:
  * Khac_phuc/            -> da xoa khoi repo, ghi chu ro rang
  * Kvasir_YOLO_SEG      -> ban GOC 1000 anh, KHONG train -> tro sang .rar
  * Kvasir_YOLO_SEG_BG20 -> ban TRAIN
  * Ket_Qua_V1, Ket_Qua_2, KQ_Poylp, KQ_DoiXung -> da doi ten / da chuyen choi khac
  * doc/02_, doc/05_, doc/09_, doc/11_, doc/12_ -> da chuyen vao doc/historical/

Chay XEM TRUOC mac dinh; them --apply de ghi file.
"""
from __future__ import annotations
import re, sys
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
APPLY = "--apply" in sys.argv
HIST = "archive/doc/historical"

# (mau cu, mau moi)
RULES = [
    # --- tep da chuyen vao doc/historical ---
    (r"archive/doc/02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU\.md",
     f"{HIST}/thuc_nghiem_6fold_5mo_hinh/02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md"),
    (r"archive/doc/BAO_CAO_TIEN_DO_TUAN_HOAN_CHINH\.md",
     f"{HIST}/thuc_nghiem_6fold_5mo_hinh/BAO_CAO_TIEN_DO_TUAN_HOAN_CHINH.md"),
    (r"archive/doc/05_KET_QUA_MAP_VA_DO_ON_DINH_SEED\.md",
     f"{HIST}/05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md"),
    (r"archive/doc/01_KIEN_TRUC_C2IAVM_CHAMPION_VA_CAC_BIEN_THE\.md",
     f"{HIST}/mo_hinh_khong_lien_quan/01_KIEN_TRUC_C2IAVM_CHAMPION_VA_CAC_BIEN_THE.md"),
    (r"archive/doc/09_KHAO_SAT_ABLATION_TANG_10_VS_P5\.md",
     f"{HIST}/mo_hinh_khong_lien_quan/09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md"),
    (r"archive/doc/11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA\.md",
     f"{HIST}/mo_hinh_khong_lien_quan/11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md"),
    (r"archive/doc/12_CHI_TIET_KET_QUA_IAVM_INTERACTIVE_ATTENTION_VMAMBA\.md",
     f"{HIST}/mo_hinh_khong_lien_quan/12_CHI_TIET_KET_QUA_IAVM_INTERACTIVE_ATTENTION_VMAMBA.md"),
    (r"archive/doc/14_HUONG_8_INTERACTIVE_TOPOLOGY_VMAMBA\.md",
     f"{HIST}/mo_hinh_khong_lien_quan/14_HUONG_8_INTERACTIVE_TOPOLOGY_VMAMBA.md"),
    # --- thu muc da xoa khoi repo ---
    (r"archive/Khac_phuc/[A-Za-z0-9_\-]+", "`Khac_phuc/…` (đã xóa khỏi repo năm 2026)"),
    (r"archive/Khac_phuc/?", "`Khac_phuc/` (đã xóa khỏi repo năm 2026)"),
    (r"archive/KQ_Poylp/?", "`KQ_Poylp/` (không còn trong repo)"),
    (r"archive/Ket_Qua_V1/?", "`Ket_Qua_V1/` (không còn trong repo)"),
    (r"archive/Ket_Qua_2/?", "`Ket_Qua_2/` (không còn trong repo)"),
    # --- da doi ten ---
    (r"archive/KQ_DoiXung/[A-Za-z0-9_ ]+", "archive/Ket_Qua_V2/KQ_Nen_DX_10seed"),
    (r"archive/KQ_DoiXung", "archive/Ket_Qua_V2/KQ_Nen_DX_10seed"),
    # --- dataset: ban GOC khong train ---
    (r"archive/Kvasir_YOLO_SEG_BG20/report\.txt",
     "archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/dataset_bg20_summary.json"),
    (r"archive/Kvasir_YOLO_SEG_BG20", "archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20"),
    (r"archive/Kvasir_YOLO_SEG", "archive/Kvasir_YOLO_SEG.rar  "
                                 "_(bản gốc 1.000 ảnh — KHÔNG dùng để train)_"),
]

# TẬP TỰ TRÍCH DẪN — không sửa (trích đường dẫn hỏng làm ví dụ)
SKIP = {"24_DANH_SACH_DUONG_DAN_HONG.md", "21_HUONG_DAN_BAN_GIAO_AI_MOI_VA_VIEC_CONG_TAI.md"}
TARGETS = [m for m in sorted(ROOT.glob("doc/*.md")) + sorted(ROOT.glob("*.md"))
           if m.name not in SKIP]

print("=" * 86)
print("SUA DUONG DAN HONG VONG 2" + ("   [CHAY THAT]" if APPLY else "   [XEM TRUOC]"))
print("=" * 86)

n_files = n_rules = 0
for md in TARGETS:
    s = md.read_text(encoding="utf-8", errors="replace")
    orig, applied = s, []
    for pat, new in RULES:
        s2, n = re.subn(pat, new, s)
        if n:
            applied.append((n, pat[:52]))
            s = s2
    if s != orig:
        n_files += 1
        n_rules += sum(n for n, _ in applied)
        print(f"\n[{md.relative_to(ROOT)}]")
        for n, p in applied:
            print(f"   x{n:<3} {p}")
        if APPLY:
            md.write_text(s, encoding="utf-8"); print("   -> DA GHI")

print("\n" + "=" * 86)
print(f"{n_rules} quy tac tren {n_files} tep" + ("  (DA GHI)" if APPLY else ""))
if not APPLY:
    print("Chay:  python .\\Stracth\\fix_doc_paths_round2.py --apply")
print("=" * 86)
