"""Tỉ lệ báo nhầm trên 800 ảnh normal-cecum chưa dùng (phản hồi nhận xét phản biện II.5).

BG20 chỉ lấy 200/1.000 ảnh normal-cecum của Kvasir v2 làm ảnh nền (160 train, 40 val, seed 42).
800 ảnh còn lại không tham gia huấn luyện hay chọn epoch. Chạy 4 mô hình × 20 seed trên 800 ảnh này để
tách hai nguyên nhân báo nhầm trên PolypGen: ảnh chưa thấy (cùng vị trí, cùng nguồn) hay khác miền.

Giao thức giống hệt 00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py (dùng lại hàm của script đó):
- YOLO: imgsz 640, conf 0,25, iou 0,7, retina_masks=True, half=False; best.pt của từng seed.
- PraNet/U-Net: bản `pranet640`/`unet640`, kéo về 640×640, ngưỡng 0,5.
- Một ảnh bị báo nhầm nếu có ít nhất 1 điểm ảnh bị dự đoán là polyp (như bg_fp_image_rate).

Kiểm tra gần trùng: Kvasir v2 có nhiều khung hình liên tiếp từ cùng video, nên với mỗi ảnh trong 800 ảnh,
tính tương quan ảnh xám 64×64 (sau khi cắt viền đen) lớn nhất với 160 ảnh nền huấn luyện; >= 0,95 coi là gần trùng
(cùng ngưỡng với kiem_tra_trung_polypgen.py). Kết quả báo cáo cho cả 800 ảnh và riêng nhóm không gần trùng.

Chỉ đọc 01_du_lieu/, 03_, 05_; ghi từng lượt vào ../bang/nen_cecum/ và bảng tổng hợp vào
00_tai_lieu_tong_quan/bang/pixel_640/nen_cecum/06–07_*.csv (hoặc --out).

Chạy (cần GPU):
    C:\\venv_kl_gpu\\Scripts\\python.exe danh_gia_nen_cecum.py --kiem-tra         # kiểm tra đủ GPU/dữ liệu/checkpoint
    C:\\venv_kl_gpu\\Scripts\\python.exe danh_gia_nen_cecum.py --doi-chieu        # đối chiếu môi trường (40 ảnh nền val)
    C:\\venv_kl_gpu\\Scripts\\python.exe danh_gia_nen_cecum.py --seeds 0          # chạy thử
    C:\\venv_kl_gpu\\Scripts\\python.exe danh_gia_nen_cecum.py                    # 4 mô hình × 20 seed
    C:\\venv_kl_gpu\\Scripts\\python.exe danh_gia_nen_cecum.py --chi-tong-hop
Phần tổng hợp chỉ lấy các mô hình được chọn (mặc định baseline, tsvm, pranet640, unet640).
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent
sys.path.insert(0, str(REPO / "00_tai_lieu_tong_quan" / "scripts"))
sys.path.insert(0, str(HERE))
import danh_gia_pixel as dg  # noqa: E402
from kiem_tra_trung_polypgen import crop_black  # noqa: E402

CECUM = REPO / "01_du_lieu" / "tao_BG20" / "normal-cecum" / "normal-cecum"
BG20 = REPO / "01_du_lieu" / "Kvasir_YOLO_SEG_BG20"
OUT = ROOT / "bang" / "nen_cecum"
LUOT = OUT / "tung_luot"
OUT20 = ROOT / "bang" / "20seed"
CORR_DUP = 0.95


def danh_sach():
    tat_ca = sorted(p.name for p in CECUM.glob("*.jpg"))
    assert len(tat_ca) == 1000, len(tat_ca)
    tr = (BG20 / "selected_normal_cecum_train_160.txt").read_text(encoding="utf-8").split()
    va = (BG20 / "selected_normal_cecum_val_40.txt").read_text(encoding="utf-8").split()
    assert len(tr) == 160 and len(va) == 40 and not set(tr) & set(va)
    assert set(tr) | set(va) <= set(tat_ca)
    # đối chiếu với ảnh thật trong BG20 (tên bg_<tên gốc>)
    for split, names in (("train", tr), ("val", va)):
        have = {p.name[3:] for p in (BG20 / "images" / split).glob("bg_*.jpg")}
        assert have == set(names), split
    con_lai = [n for n in tat_ca if n not in set(tr) | set(va)]
    assert len(con_lai) == 800
    return con_lai, tr


def v64(img):
    g = crop_black(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    s = cv2.resize(g, (64, 64), interpolation=cv2.INTER_AREA).astype(np.float32).flatten()
    return (s - s.mean()) / (s.std() + 1e-6)


def gan_trung(con_lai, tr):
    f = OUT / "00_gan_trung_voi_train.csv"
    if f.exists():
        return pd.read_csv(f, encoding="utf-8-sig")
    T = np.array([v64(cv2.imread(str(CECUM / n))) for n in tr])
    rows = []
    for n in con_lai:
        c = T @ v64(cv2.imread(str(CECUM / n))) / T.shape[1]
        j = int(np.argmax(c))
        rows.append({"image": n, "train_gan_nhat": tr[j], "corr64": float(c[j])})
    df = pd.DataFrame(rows)
    df["gan_trung"] = df.corr64 >= CORR_DUP
    df.to_csv(f, index=False, encoding="utf-8-sig")
    return df


def run(args, con_lai):
    import torch
    assert torch.cuda.is_available(), "Cần GPU (C:\\venv_kl_gpu\\Scripts\\python.exe)"
    dev = "cuda:0"
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    print("GPU:", torch.cuda.get_device_name(0), "| torch", torch.__version__)
    cleanup = dg.import_fork()
    nbc = dg.notebook_classes()
    items = None
    t0 = time.time()
    try:
        for model in args.models:
            for s in args.seeds:
                out = LUOT / f"cecum800_{model}_s{s}.csv"
                if out.exists():
                    continue
                if items is None:
                    items = []
                    for n in con_lai:
                        img = cv2.imread(str(CECUM / n))
                        items.append({"name": n, "bgr": img, "gt": np.zeros(img.shape[:2], bool)})
                    print(f"Đã nạp {len(items)} ảnh")
                w = dg.MODELS[model][1](s)
                t1 = time.time()
                if model in ("baseline", "tsvm"):
                    preds = dg.predict_yolo(w, items, dev)
                else:
                    net = nbc[model]()
                    net.load_state_dict(torch.load(w, map_location="cpu"), strict=True)
                    net = net.to(dev).eval()
                    preds = dg.predict_semantic(net, items, model, dev)
                    del net
                torch.cuda.empty_cache()
                pd.DataFrame([{"model": model, "seed": s, "image": it["name"], "pred_px": int(p.sum())}
                              for it, p in zip(items, preds)]).to_csv(out, index=False, encoding="utf-8-sig")
                print(f"  {model:8s} seed {s:2d}: {time.time() - t1:6.1f}s")
    finally:
        cleanup()
    print(f"Tổng thời gian: {(time.time() - t0) / 60:.1f} phút")


def tong_hop(dup, models, out_root=None):
    """Tổng hợp các mô hình `models`. out_root=None: bộ chính, ghi bang/20seed/06–07; ngược lại ghi vào out_root."""
    files = sorted(LUOT.glob("cecum800_*.csv"))
    assert files, "Chưa có kết quả"
    df = pd.concat([pd.read_csv(f, encoding="utf-8-sig") for f in files], ignore_index=True)
    df = df[df.model.isin(models)]
    assert set(df.model) == set(models), f"Thiếu kết quả của: {sorted(set(models) - set(df.model))}"
    df = df.merge(dup[["image", "gan_trung"]], on="image", how="left")
    assert df.gan_trung.notna().all()
    rows = []
    for (m, s), g in df.groupby(["model", "seed"]):
        k = g[~g.gan_trung]
        rows.append({"model": m, "seed": s, "n_images": len(g), "fp_image_rate": (g.pred_px > 0).mean(),
                     "n_khong_gan_trung": len(k), "fp_image_rate_khong_gan_trung": (k.pred_px > 0).mean(),
                     "fp_area_mean": g.pred_px.mean()})
    sd = pd.DataFrame(rows).sort_values(["model", "seed"])
    have = sd.groupby("model").seed.nunique()
    print("Số seed đã có:", have.to_dict())
    n = int(have.min())
    tag = "20seed" if n >= 20 else f"thu_{n}seed"
    sd = sd[sd.seed < max(n, 1)] if n >= 20 else sd
    metrics = ["fp_image_rate", "fp_image_rate_khong_gan_trung"]
    st = []
    for m in sd.model.unique():
        g = sd[sd.model == m]
        for k in metrics:
            st.append({"model": m, "metric": k, "n_seeds": len(g), "mean": g[k].mean(), "sd": g[k].std(ddof=1),
                       "min": g[k].min(), "max": g[k].max()})
    if "tsvm" in set(sd.model):
        t = sd[sd.model == "tsvm"].set_index("seed")
        for o_name in [x for x in sd.model.unique() if x != "tsvm"]:
            o = sd[sd.model == o_name].set_index("seed")
            c = t.index.intersection(o.index)
            for k in metrics:
                d = t.loc[c, k] - o.loc[c, k]
                ok = len(c) >= 3 and d.std() > 0
                st.append({"model": f"tsvm_vs_{o_name}", "metric": k, "n_seeds": len(c), "mean": d.mean(),
                           "sd": d.std(ddof=1) if len(c) > 1 else np.nan,
                           "paired_t_p": stats.ttest_rel(t.loc[c, k], o.loc[c, k]).pvalue if ok else np.nan,
                           "wilcoxon_p": stats.wilcoxon(t.loc[c, k], o.loc[c, k]).pvalue if ok else np.nan,
                           "tsvm_higher": int((d > 0).sum())})
    st = pd.DataFrame(st)
    if out_root is not None:
        out_root.mkdir(parents=True, exist_ok=True)
        pre = "" if tag == "20seed" else f"{tag}_"
        sd.to_csv(out_root / f"{pre}06_nen_cecum_tung_seed.csv", index=False, encoding="utf-8-sig")
        st.to_csv(out_root / f"{pre}07_nen_cecum_thong_ke.csv", index=False, encoding="utf-8-sig")
        print("Đã ghi:", out_root)
    elif tag == "20seed":
        sd.to_csv(OUT20 / "06_nen_cecum_tung_seed.csv", index=False, encoding="utf-8-sig")
        st.to_csv(OUT20 / "07_nen_cecum_thong_ke.csv", index=False, encoding="utf-8-sig")
    else:
        sd.to_csv(OUT / f"{tag}_tung_seed.csv", index=False, encoding="utf-8-sig")
        st.to_csv(OUT / f"{tag}_thong_ke.csv", index=False, encoding="utf-8-sig")
    print(f"Gần trùng với 160 ảnh nền train (corr64 >= {CORR_DUP}): {int(dup.gan_trung.sum())}/800")
    with pd.option_context("display.float_format", "{:.4f}".format, "display.width", 200):
        print(st.to_string(index=False))


def kiem_tra(args):
    """Kiểm tra đủ GPU, dữ liệu, checkpoint trước khi chạy thật."""
    thieu = []
    try:
        import torch
        if not torch.cuda.is_available():
            thieu.append("GPU (torch.cuda.is_available() = False; dùng C:\\venv_kl_gpu\\Scripts\\python.exe)")
        else:
            print("GPU:", torch.cuda.get_device_name(0))
    except ImportError:
        thieu.append("torch")
    try:
        con_lai, _ = danh_sach()
        print(f"Ảnh cecum chưa dùng: {len(con_lai)}")
    except Exception as e:  # noqa: BLE001
        thieu.append(f"dữ liệu normal-cecum hoặc danh sách BG20 ({e!r})")
    for p in (dg.FORK, dg.NB / "pranet-new.ipynb", dg.NB / "unet-new.ipynb",
              dg.NB_640 / "pranet-new.ipynb", dg.NB_640 / "unet-new.ipynb"):
        if not p.exists():
            thieu.append(str(p))
    n_ck = 0
    for m in args.models:
        for s in args.seeds:
            w = dg.MODELS[m][1](s)
            if w.exists():
                n_ck += 1
            else:
                thieu.append(f"checkpoint {w}")
    print(f"Checkpoint có: {n_ck}/{len(args.models) * len(args.seeds)}")
    for t in thieu:
        print("THIẾU:", t)
    print("KIỂM TRA: ĐỦ, có thể chạy" if not thieu else "KIỂM TRA: CHƯA ĐỦ")


def doi_chieu():
    """Chạy mô hình gốc seed 0 trên 40 ảnh nền kiểm định, so pred_px với bang/pixel_640/10_pixel_tung_anh.csv."""
    import torch
    ref = pd.read_csv(REPO / "00_tai_lieu_tong_quan" / "bang" / "pixel_640" / "10_pixel_tung_anh.csv", encoding="utf-8-sig")
    ref = ref[(ref.model == "baseline") & (ref.seed == 0) & (ref.is_bg.astype(str) == "True")].set_index("image")
    names = sorted(p.name for p in (BG20 / "images" / "val").glob("bg_*.jpg"))
    assert len(names) == 40 and len(ref) == 40
    items = []
    for n in names:
        img = cv2.imread(str(BG20 / "images" / "val" / n))
        items.append({"name": n, "bgr": img, "gt": np.zeros(img.shape[:2], bool)})
    cleanup = dg.import_fork()
    try:
        preds = dg.predict_yolo(dg.MODELS["baseline"][1](0), items, "cuda:0")
    finally:
        cleanup()
    torch.cuda.empty_cache()
    lech = sum((int(p.sum()) > 0) != (int(ref.loc[it["name"], "pred_px"]) > 0) for it, p in zip(items, preds))
    print(f"ĐỐI CHIẾU: {lech}/40 ảnh nền lệch kết luận báo nhầm so với bang/pixel_640/10_pixel_tung_anh.csv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=dg.DEFAULT_MODELS, choices=list(dg.MODELS))
    ap.add_argument("--seeds", nargs="*", type=int, default=list(range(20)))
    ap.add_argument("--chi-tong-hop", action="store_true")
    ap.add_argument("--kiem-tra", action="store_true", help="chỉ kiểm tra GPU, dữ liệu, checkpoint")
    ap.add_argument("--doi-chieu", action="store_true", help="đối chiếu môi trường trên 40 ảnh nền kiểm định")
    ap.add_argument("--out", type=Path,
                    default=REPO / "00_tai_lieu_tong_quan" / "bang" / "pixel_640" / "nen_cecum",
                    help="thư mục ghi bảng 06–07 (mặc định 00_tai_lieu_tong_quan/bang/pixel_640/nen_cecum)")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.kiem_tra:
        kiem_tra(args)
        return
    if args.doi_chieu:
        doi_chieu()
        return
    LUOT.mkdir(parents=True, exist_ok=True)
    con_lai, tr = danh_sach()
    dup = gan_trung(con_lai, tr)
    if not args.chi_tong_hop:
        run(args, con_lai)
    models = list(dict.fromkeys(["baseline", "tsvm", *args.models]))   # luôn kèm baseline, tsvm để so ghép cặp
    tong_hop(dup, models, args.out)


if __name__ == "__main__":
    main()
