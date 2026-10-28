"""Đánh giá theo pixel trên dữ liệu ngoài (CVC-ClinicDB, CVC-ColonDB, ETIS-LaribPolypDB).

Bốn mô hình (YOLO26s-seg, YOLO26s-seg + TSVM FP32, PraNet, U-Net) đã huấn luyện trên BG20 (Kvasir-SEG + ảnh nền),
được chạy thẳng trên ảnh của ba bộ dữ liệu khác nguồn, không huấn luyện lại, không tinh chỉnh.
Giao thức giống hệt 00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py (dùng lại các hàm của script đó):
- YOLO: imgsz 640, conf 0,25, iou 0,7, retina_masks=True, half=False; gộp mọi mặt nạ của ảnh thành một.
- PraNet/U-Net: resize 352×352, ngưỡng xác suất 0,5, phóng song tuyến về kích thước gốc.
- Nhãn chuẩn: mặt nạ gốc của từng bộ dữ liệu, nhị phân hóa ở ngưỡng > 127. Mọi ảnh đều có polyp.

Chỉ đọc dữ liệu ở DeepLearning/Dataset/ và checkpoint ở 03_, 05_; chỉ ghi vào ../bang/ và ../du_lieu_dinh_tinh/.
Mỗi lượt (bộ dữ liệu, mô hình, seed) ghi một tệp riêng trong ../bang/tung_luot/, chạy lại sẽ bỏ qua lượt đã có.

Chạy (cần GPU):
    C:\\venv_kl_gpu\\Scripts\\python.exe danh_gia_du_lieu_ngoai.py                 # 4 mô hình × seed 0–9 × 3 bộ
    C:\\venv_kl_gpu\\Scripts\\python.exe danh_gia_du_lieu_ngoai.py --seeds 0 --sets etis   # chạy thử
    C:\\venv_kl_gpu\\Scripts\\python.exe danh_gia_du_lieu_ngoai.py --chi-tong-hop          # chỉ tổng hợp lại
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import torch
from scipy import stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent
sys.path.insert(0, str(REPO / "00_tai_lieu_tong_quan" / "scripts"))
import danh_gia_pixel as dg  # noqa: E402  (hàm suy luận và chỉ số dùng chung)

DATASET = REPO.parent / "Dataset"
SETS = {
    "clinicdb": ("CVC-ClinicDB", DATASET / "CVC-ClinicDB" / "PNG" / "Original", DATASET / "CVC-ClinicDB" / "PNG" / "Ground Truth", 612),
    "colondb": ("CVC-ColonDB", DATASET / "CVC-ColonDB_data" / "CVC-ColonDB" / "images", DATASET / "CVC-ColonDB_data" / "CVC-ColonDB" / "masks", 380),
    "etis": ("ETIS-LaribPolypDB", DATASET / "ETIS-Larib PolypDB" / "images", DATASET / "ETIS-Larib PolypDB" / "masks", 196),
}
# PolypGen2021: ảnh đơn của 6 trung tâm, nạp và chạy từng trung tâm (ảnh lớn, tránh tràn RAM);
# khi tổng hợp có thêm dòng gộp "polypgen". Đã kiểm tra không trùng ảnh với Kvasir-SEG (kiem_tra_trung_polypgen.py).
PG = DATASET / "PolypGen2021_MultiCenterData_v3" / "PolypGen2021_MultiCenterData_v3"
for _c, _n in zip(range(1, 7), (256, 301, 457, 227, 208, 88)):
    SETS[f"pg_c{_c}"] = (f"PolypGen C{_c}", PG / f"data_C{_c}" / f"images_C{_c}", PG / f"data_C{_c}" / f"masks_C{_c}", _n)
BANG = ROOT / "bang"
LUOT = BANG / "tung_luot"
QUAL = ROOT / "du_lieu_dinh_tinh"
METRICS = ["dice", "iou", "precision", "recall", "dice_micro", "iou_micro", "no_pred_rate", "bg_fp_image_rate"]


def load_set(key):
    _, img_dir, mask_dir, n = SETS[key]
    items = []
    pg = key.startswith("pg_")
    for p in sorted(img_dir.glob("*.jpg" if pg else "*.png"), key=lambda q: int(q.stem) if q.stem.isdigit() else q.stem):
        img = cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_COLOR)
        # Bộ gốc có 1 lỗi đặt tên: ảnh C3 "C3_EndoCV2021_00489].jpg" thừa "]", còn mặt nạ đúng tên.
        mp = mask_dir / (f"{p.stem.rstrip(']')}_mask.jpg" if pg else p.name)
        m = cv2.imdecode(np.fromfile(mp, np.uint8), cv2.IMREAD_GRAYSCALE)
        assert img is not None and m is not None, p
        assert m.shape == img.shape[:2], (p, img.shape, m.shape)
        items.append({"name": p.name, "path": p, "bgr": img, "gt": m > 127, "raw": None, "is_bg": False})
    assert len(items) == n, (key, len(items))
    n_empty = sum(not it["gt"].any() for it in items)
    if n_empty:
        print(f"  [{key}] {n_empty} ảnh có mặt nạ rỗng")
    return items


def run(args):
    assert torch.cuda.is_available(), "Cần GPU (chạy bằng C:\\venv_kl_gpu\\Scripts\\python.exe)"
    dev = "cuda:0"
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    print("GPU:", torch.cuda.get_device_name(0), "| torch", torch.__version__)
    cleanup = dg.import_fork()
    import ultralytics
    print("ultralytics:", ultralytics.__version__, ultralytics.__file__)
    nbc = dg.notebook_classes()
    LUOT.mkdir(parents=True, exist_ok=True)
    QUAL.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    try:
        for key in args.sets:
            items = None
            for model in args.models:
                for s in args.seeds:
                    out = LUOT / f"{key}_{model}_s{s}.csv"
                    if out.exists():
                        continue
                    if items is None:
                        items = load_set(key)
                        print(f"[{key}] {len(items)} ảnh")
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
                    rows = []
                    for it, pr in zip(items, preds):
                        tp, fp, fn = dg.counts(pr, it["gt"])
                        rows.append({"dataset": key, "model": model, "seed": s, "image": it["name"],
                                     "pred_px": int(pr.sum()), "gt_px": int(it["gt"].sum()), "tp": tp, "fp": fp, "fn": fn})
                    pd.DataFrame(rows).to_csv(out, index=False, encoding="utf-8-sig")
                    if s == 0 and not key.startswith("pg_"):   # lưu mặt nạ seed 0 cho hình minh họa (bỏ PolypGen vì ảnh rất lớn)
                        np.savez_compressed(QUAL / f"pred_seed0_{key}_{model}.npz",
                                            **{it["name"]: np.packbits(pr) for it, pr in zip(items, preds)})
                    print(f"  {key:8s} {model:8s} seed {s}: {time.time() - t1:6.1f}s")
            del items
    finally:
        cleanup()
    print(f"Tổng thời gian: {(time.time() - t0) / 60:.1f} phút")


def summarize(n_seed):
    """Tổng hợp seed 0..n_seed-1 vào bang/<n_seed>seed/ (chỉ khi đã đủ lượt)."""
    files = sorted(LUOT.glob("*.csv"))
    assert files, "Chưa có kết quả trong bang/tung_luot/"
    df = pd.concat([pd.read_csv(f, encoding="utf-8-sig") for f in files], ignore_index=True)
    df = df[df.seed < n_seed]
    pgall = df[df.dataset.str.startswith("pg_")].assign(dataset="polypgen")   # gộp 6 trung tâm
    df = pd.concat([df, pgall], ignore_index=True)
    have = df.groupby(["dataset", "model"]).seed.nunique()
    if (have < n_seed).any():
        print(f"Bỏ qua tổng hợp {n_seed} seed: còn thiếu lượt")
        print(have[have < n_seed])
        return
    out = BANG / f"{n_seed}seed"
    out.mkdir(exist_ok=True)
    rows = []
    for (key, model, s), g_all in df.groupby(["dataset", "model", "seed"], sort=False):
        # Ảnh có mặt nạ rỗng (PolypGen có 125 ảnh không polyp) không tính vào chỉ số phân đoạn;
        # dùng để đo tỉ lệ ảnh không polyp bị báo nhầm, như ảnh nền của BG20.
        g, bg = g_all[g_all.gt_px > 0], g_all[g_all.gt_px == 0]
        m = np.array([dg.per_image_metrics(a, b, c) for a, b, c in zip(g.tp, g.fp, g.fn)])
        r = {"dataset": key, "model": model, "seed": s, "n_images": len(g), "n_no_polyp": len(bg),
             "bg_fp_image_rate": float((bg.pred_px > 0).mean()) if len(bg) else np.nan}
        r["dice"], r["iou"], r["precision"], r["recall"] = np.nanmean(m, 0)
        TP, FP, FN = g.tp.sum(), g.fp.sum(), g.fn.sum()
        r["dice_micro"] = 2 * TP / (2 * TP + FP + FN)
        r["iou_micro"] = TP / (TP + FP + FN)
        r["no_pred_rate"] = float((g.pred_px == 0).mean())
        rows.append(r)
    sd = pd.DataFrame(rows).sort_values(["dataset", "model", "seed"])
    sd.to_csv(out / "01_ngoai_tung_seed.csv", index=False, encoding="utf-8-sig")

    st = []
    for key in sd.dataset.unique():
        d = sd[sd.dataset == key]
        for model in d.model.unique():
            g = d[d.model == model]
            for m in METRICS:
                st.append({"dataset": key, "model": model, "metric": m, "n_seeds": len(g),
                           "mean": g[m].mean(), "sd": g[m].std(ddof=1), "min": g[m].min(), "max": g[m].max()})
        if "tsvm" in set(d.model):
            t = d[d.model == "tsvm"].set_index("seed")
            for other in [x for x in d.model.unique() if x != "tsvm"]:
                o = d[d.model == other].set_index("seed")
                common = t.index.intersection(o.index)
                if len(common) < 3:
                    continue
                for m in METRICS:
                    diff = t.loc[common, m] - o.loc[common, m]
                    ok = diff.std() > 0
                    st.append({"dataset": key, "model": f"tsvm_vs_{other}", "metric": m, "n_seeds": len(common),
                               "mean": diff.mean(), "sd": diff.std(ddof=1),
                               "paired_t_p": stats.ttest_rel(t.loc[common, m], o.loc[common, m]).pvalue if ok else np.nan,
                               "wilcoxon_p": stats.wilcoxon(t.loc[common, m], o.loc[common, m]).pvalue if ok else np.nan,
                               "tsvm_higher": int((diff > 0).sum())})
    stt = pd.DataFrame(st)
    stt.to_csv(out / "02_ngoai_thong_ke.csv", index=False, encoding="utf-8-sig")
    print(f"===== {n_seed} seed -> {out}")
    with pd.option_context("display.float_format", "{:.4f}".format, "display.width", 220, "display.max_rows", 400):
        print(stt[stt.metric.isin(["dice", "iou", "precision", "recall", "no_pred_rate"])].to_string(index=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sets", nargs="*", default=list(SETS), choices=list(SETS))
    ap.add_argument("--models", nargs="*", default=list(dg.MODELS), choices=list(dg.MODELS))
    ap.add_argument("--seeds", nargs="*", type=int, default=list(range(10)))
    ap.add_argument("--chi-tong-hop", action="store_true", help="không suy luận, chỉ tổng hợp bang/tung_luot/")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not args.chi_tong_hop:
        run(args)
    for n in (10, 20):   # bảng tổng hợp ghi riêng vào bang/10seed/ và bang/20seed/
        summarize(n)


if __name__ == "__main__":
    main()
