"""Kiểm tra bản rút gọn: đánh số hình/bảng/công thức, tham chiếu, trích dẫn, số liệu so với bản đầy đủ."""
import re, sys
from pathlib import Path
BC = Path(sys.argv[1])
FULL, RG = BC / "md_bao_cao", BC / "md_bao_cao_rut_gon"
THAN = ["01_MO_DAU.md", "02_CHUONG_1_TONG_QUAN.md", "03_CHUONG_2_CO_SO_LY_THUYET.md", "04_CHUONG_3_MO_HINH_DE_XUAT.md",
        "05_CHUONG_4_DU_LIEU_TIEN_XU_LY.md", "06_CHUONG_5_CAI_DAT_UNG_DUNG.md", "07_CHUONG_6_THUC_NGHIEM_DANH_GIA.md",
        "09_KET_LUAN.md", "10_PHU_LUC.md"]

def bo_ghi_chu(t):  # bỏ dòng ghi chú '>' và khối code
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    return "\n".join(l for l in t.splitlines() if not l.startswith(">"))

loi = []
cap_bang, cap_hinh, cong_thuc, tt = {}, {}, {}, {}
for f in THAN:
    t = (RG / f).read_text(encoding="utf-8")
    for m in re.finditer(r"^\*Bảng ((?:PL\.)?[\d.]+)\.", t, re.M): cap_bang.setdefault(f, []).append(m.group(1))
    for m in re.finditer(r"^\*Hình ((?:PL\.)?[\d.]+)\.", t, re.M): cap_hinh.setdefault(f, []).append(m.group(1))
    for m in re.finditer(r"[\\]tag\{([\d.]+)\}", t): cong_thuc.setdefault(f, []).append(m.group(1))
    for m in re.finditer(r"^\*Thuật toán ([\d.]+)\.", t, re.M): tt.setdefault(f, []).append(m.group(1))
    # ảnh và chú thích phải khớp số
    for m in re.finditer(r"^!\[Hình ((?:PL\.)?[\d.]+)\]\([^)]*\)(?:\{[^}]*\})?\s*\n+\*Hình ((?:PL\.)?[\d.]+)\.", t, re.M):
        if m.group(1) != m.group(2): loi.append(f"{f}: ảnh {m.group(1)} ≠ chú thích {m.group(2)}")

def lien_tuc(ds, ten):
    nhom = {}
    for f, xs in ds.items():
        for x in xs:
            k, n = x.rsplit(".", 1); nhom.setdefault(k, []).append(int(n))
    for k, ns in nhom.items():
        if ns != list(range(1, len(ns) + 1)): loi.append(f"{ten} {k}.x không liên tục: {ns}")
    return {x for xs in ds.values() for x in xs}
B = lien_tuc(cap_bang, "Bảng"); H = lien_tuc(cap_hinh, "Hình"); C = lien_tuc(cong_thuc, "Công thức"); T = lien_tuc(tt, "Thuật toán")

# tham chiếu trong văn (bỏ ghi chú)
tat_ca = ""
for f in THAN:
    t = bo_ghi_chu((RG / f).read_text(encoding="utf-8"))
    tat_ca += t
    for m in re.finditer(r"Bảng ((?:PL\.)?\d+\.\d+)", t):
        if m.group(1) not in B: loi.append(f"{f}: nhắc Bảng {m.group(1)} không tồn tại")
    for m in re.finditer(r"Hình ((?:PL\.)?\d+\.\d+)", t):
        if m.group(1) not in H: loi.append(f"{f}: nhắc Hình {m.group(1)} không tồn tại")
    for m in re.finditer(r"(?<![\w$])\((\d\.\d+)\)", t):
        if m.group(1) not in C: loi.append(f"{f}: nhắc công thức ({m.group(1)}) không tồn tại")
    for m in re.finditer(r"Thuật toán (\d\.\d+)", t):
        if m.group(1) not in T: loi.append(f"{f}: nhắc Thuật toán {m.group(1)} không tồn tại")
# mục được nhắc phải tồn tại
muc = set()
for f in THAN:
    for m in re.finditer(r"^#{2,4} (\d+(?:\.\d+)+)\.", (RG / f).read_text(encoding="utf-8"), re.M): muc.add(m.group(1))
for m in re.finditer(r"[Mm]ục (\d+\.\d+(?:\.\d+)?)", tat_ca):
    if m.group(1) not in muc and not m.group(1).startswith(("0.",)): loi.append(f"nhắc mục {m.group(1)} không tồn tại")

# trích dẫn: thứ tự lần đầu 1..57 (mở rộng khoảng [a]–[b])
def trich(t):
    out = []
    for m in re.finditer(r"\[(\d+)\](?:–\[(\d+)\])?", t):
        a = int(m.group(1)); b = int(m.group(2) or a); out += list(range(a, b + 1))
    return out
ds = []
for f in THAN:
    ds += [x for x in trich(re.sub(r"`[^`]*`", "", bo_ghi_chu((RG / f).read_text(encoding="utf-8")))) if x <= 57]
dau = list(dict.fromkeys(ds))
print("Trích dẫn khác nhau:", len(dau), "| thứ tự lần đầu đúng 1→N:", dau == list(range(1, len(dau) + 1)))
if dau != list(range(1, len(dau) + 1)): print("  thứ tự:", dau)

# số liệu: mọi số trong bản rút gọn phải có trong bản đầy đủ (toàn bộ thân)
so = lambda t: set(re.findall(r"\d+(?:[.,]\d+)*", t))
day_du = set().union(*[so(bo_ghi_chu((FULL / f).read_text(encoding="utf-8"))) for f in THAN])
moi = {}
for f in THAN:
    x = so(bo_ghi_chu((RG / f).read_text(encoding="utf-8"))) - day_du
    if x: moi[f] = sorted(x)
print("Số không có trong bản đầy đủ:", moi or "không")
print("Bảng:", len(B), "| Hình:", len(H), "| Công thức:", len(C))
print("LỖI:" if loi else "Không lỗi đánh số/tham chiếu.", *loi, sep="\n  ")
