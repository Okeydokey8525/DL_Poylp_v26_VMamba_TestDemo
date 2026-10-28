"""Kiểm tra ảnh trùng giữa PolypGen2021 (ảnh đơn C1–C6) và Kvasir-SEG (1.000 ảnh dùng huấn luyện/kiểm định).

Ảnh có thể đã bị đổi kích thước, cắt viền hoặc nén lại, nên không chỉ so mã băm tệp. Ba lớp kiểm tra:
1. md5 của tệp (trùng tuyệt đối).
2. pHash 64 bit (DCT trên ảnh xám 32×32) và dHash 64 bit; lấy cặp có khoảng cách Hamming nhỏ.
3. Với mỗi cặp ứng viên: tương quan Pearson giữa hai ảnh xám thu về 64×64 (sau khi cắt viền đen).

Chỉ đọc DeepLearning/Dataset/; ghi bảng vào ../bang/polypgen_trung/ và CHÉP (không di chuyển) ảnh trùng
vào ../polypgen_trung_kvasir/ để xem lại. Ảnh gốc không bị sửa hay xóa.

    python kiem_tra_trung_polypgen.py            # tính đặc trưng, ghi bảng ứng viên
    python kiem_tra_trung_polypgen.py --chep     # thêm bước chép các cặp đã kết luận trùng
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATASET = ROOT.parent.parent / "Dataset"
KVASIR = DATASET / "Kvasir-SEG_data" / "Kvasir-SEG" / "Kvasir-SEG" / "images"
PG = DATASET / "PolypGen2021_MultiCenterData_v3" / "PolypGen2021_MultiCenterData_v3"
OUT = ROOT / "bang" / "polypgen_trung"
COPY = ROOT / "polypgen_trung_kvasir"
HAM_MAX = 12          # ngưỡng Hamming để coi là ứng viên (trên 64 bit)
CORR_DUP = 0.95       # tương quan ảnh 64×64 từ ngưỡng này trở lên: kết luận trùng


def read(p):
    return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_COLOR)


def crop_black(gray):
    """Cắt viền đen (khung nội soi) để ảnh cắt khác nhau vẫn so được."""
    m = gray > 20
    if m.sum() < 100:
        return gray
    ys, xs = np.where(m)
    return gray[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def feats(p):
    img = read(p)
    g = crop_black(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    s32 = cv2.resize(g, (32, 32), interpolation=cv2.INTER_AREA).astype(np.float32)
    d = cv2.dct(s32)[:8, :8].flatten()
    ph = d[1:] > np.median(d[1:])
    s9 = cv2.resize(g, (9, 8), interpolation=cv2.INTER_AREA).astype(np.int16)
    dh = (s9[:, 1:] > s9[:, :-1]).flatten()
    s64 = cv2.resize(g, (64, 64), interpolation=cv2.INTER_AREA).astype(np.float32).flatten()
    s64 = (s64 - s64.mean()) / (s64.std() + 1e-6)
    return {"md5": hashlib.md5(p.read_bytes()).hexdigest(), "ph": ph, "dh": dh, "v64": s64,
            "h": img.shape[0], "w": img.shape[1]}


def collect():
    kv = sorted(KVASIR.glob("*.jpg"))
    assert len(kv) == 1000, len(kv)
    pg = []
    for c in range(1, 7):
        for p in sorted((PG / f"data_C{c}" / f"images_C{c}").glob("*.jpg")):
            pg.append((f"C{c}", p))
    print(f"Kvasir-SEG: {len(kv)} ảnh | PolypGen ảnh đơn: {len(pg)} ảnh")
    return kv, pg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chep", action="store_true", help="chép ảnh trùng (PolypGen và Kvasir) ra thư mục riêng")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    kv, pg = collect()
    K = [feats(p) for p in kv]
    P = [feats(p) for _, p in pg]
    kph = np.array([f["ph"] for f in K]); kdh = np.array([f["dh"] for f in K]); kv64 = np.array([f["v64"] for f in K])
    kmd5 = {f["md5"]: p.name for f, p in zip(K, kv)}

    rows = []
    for (center, p), f in zip(pg, P):
        hp = (kph != f["ph"]).sum(1)
        hd = (kdh != f["dh"]).sum(1)
        corr = kv64 @ f["v64"] / len(f["v64"])
        j = int(np.argmax(corr))
        rows.append({"center": center, "polypgen": p.name, "pg_size": f"{f['w']}x{f['h']}",
                     "kvasir_best": kv[j].name, "kv_size": f"{K[j]['w']}x{K[j]['h']}",
                     "corr64": float(corr[j]), "phash_ham": int(hp[j]), "dhash_ham": int(hd[j]),
                     "min_phash_ham": int(hp.min()), "md5_match": kmd5.get(f["md5"], "")})
    df = pd.DataFrame(rows).sort_values("corr64", ascending=False)
    df.to_csv(OUT / "01_cap_gan_nhat.csv", index=False, encoding="utf-8-sig")
    df["trung"] = (df.md5_match != "") | (df.corr64 >= CORR_DUP)
    dup = df[df.trung]
    dup.to_csv(OUT / "02_danh_sach_trung.csv", index=False, encoding="utf-8-sig")

    print("Trùng md5:", int((df.md5_match != "").sum()))
    print("Phân bố tương quan 64×64 cao nhất của mỗi ảnh PolypGen:")
    for t in (0.99, 0.97, 0.95, 0.90, 0.85, 0.80):
        print(f"  >= {t}: {int((df.corr64 >= t).sum())}")
    print("Ứng viên theo pHash (Hamming <=", HAM_MAX, "):", int((df.min_phash_ham <= HAM_MAX).sum()))
    print("Kết luận trùng theo từng trung tâm:")
    print(dup.groupby("center").size().reindex([f"C{c}" for c in range(1, 7)], fill_value=0).to_string())
    with pd.option_context("display.width", 200, "display.max_rows", 60):
        print(df.head(40).to_string(index=False))

    if args.chep:
        COPY.mkdir(exist_ok=True)
        for r in dup.itertuples():
            d = COPY / r.center
            d.mkdir(exist_ok=True)
            stem = Path(r.polypgen).stem
            shutil.copy2(PG / f"data_{r.center}" / f"images_{r.center}" / r.polypgen, d / f"{stem}__polypgen.jpg")
            shutil.copy2(KVASIR / r.kvasir_best, d / f"{stem}__kvasir_{r.kvasir_best}")
        dup.to_csv(COPY / "danh_sach_trung.csv", index=False, encoding="utf-8-sig")
        print("Đã chép", len(dup), "cặp vào", COPY)


if __name__ == "__main__":
    main()
