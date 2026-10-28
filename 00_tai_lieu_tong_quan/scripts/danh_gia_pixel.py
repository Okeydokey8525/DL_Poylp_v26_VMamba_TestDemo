"""Đánh giá theo pixel (Dice, IoU, Precision, Recall) cho 4 mô hình × 20 seed trên 160 ảnh validation BG20.

Mô hình: YOLO26s-seg (đối chứng), YOLO26s-seg + TSVM FP32, PraNet (biến thể ResNet-50), U-Net.
Chỉ suy luận, không huấn luyện, không sửa checkpoint. Kết quả ghi vào ../bang/10–12_*.csv.

Giao thức (đã thống nhất với chủ dự án):
- Nhãn chuẩn chính: mặt nạ vẽ từ polygon YOLO ở độ phân giải gốc (cv2.fillPoly, giống notebook PraNet/U-Net).
  Nhãn chuẩn phụ: mặt nạ gốc của Kvasir-SEG (ngưỡng > 127), chỉ có cho 120 ảnh polyp.
- Mọi dự đoán được đưa về kích thước ảnh gốc trước khi so sánh.
- PraNet/U-Net: tiền xử lý đúng như notebook (resize 352×352, chuẩn hóa ImageNet với PraNet, chia 255 với U-Net),
  lấy nhánh lateral_map_s2 của PraNet, phóng song tuyến về kích thước gốc, ngưỡng xác suất 0,5.
- YOLO: dự đoán imgsz 640, conf 0,25, iou 0,7, retina_masks=True, half=False; gộp mọi mặt nạ của ảnh thành một.
- Chỉ số tính trên 120 ảnh polyp; 40 ảnh nền tính tỉ lệ ảnh có ít nhất một pixel bị dự đoán là polyp.
- Kiến trúc PraNet và U-Net được nạp trực tiếp từ notebook huấn luyện trong 99_luu_tru/log_kaggle_cu/.

Chạy (cần GPU):  C:\\venv_kl_gpu\\Scripts\\python.exe danh_gia_pixel.py [--seeds 0 1] [--models pranet unet]
Chỉ tổng hợp lại từ bang/10_pixel_tung_anh.csv cho một nhóm seed (không suy luận, không cần GPU):
    ... danh_gia_pixel.py --tu-bang --seeds 0 1 2 3 4 5 6 7 8 9 --out ../bang/10seed
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from scipy import stats

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = HERE.parent / "bang"
DATA = REPO / "01_du_lieu" / "Kvasir_YOLO_SEG_BG20"
RAW_MASKS = REPO / "01_du_lieu" / "tao_BG20" / "Kvasir-SEG" / "masks"
FORK = REPO / "02_ma_nguon" / "ultralytics_TSVM_FP32"
RUNS = REPO / "03_ket_qua_huan_luyen"
OTHER = REPO / "05_so_sanh_mo_hinh_khac"
NB = REPO / "99_luu_tru" / "log_kaggle_cu"
QUAL = REPO / "06_bao_cao" / "hinh" / "du_lieu_dinh_tinh"

MODELS = {
    "baseline": ("YOLO26s-seg", lambda s: RUNS / "Baseline_YOLO26s_seg" / f"Kvasir_BG20_Baseline_YOLO26s_seg_s{s}_w2" / "weights" / "best.pt"),
    "tsvm": ("YOLO26s-seg + TSVM", lambda s: RUNS / "TSVM_FP32" / f"Kvasir_BG20_YOLO26s_seg_TSVM_FP32_s{s}_w2" / "weights" / "best.pt"),
    "pranet": ("PraNet (ResNet-50)", lambda s: OTHER / "PraNet" / f"pranet_best_s{s}.pth"),
    "unet": ("U-Net", lambda s: OTHER / "UNet" / f"best_unet_s{s}.pth"),
}
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


# ------------------------------------------------------------------ dữ liệu
def load_val():
    items = []
    for p in sorted((DATA / "images" / "val").glob("*.jpg")):
        img = cv2.imread(str(p))
        h, w = img.shape[:2]
        gt = np.zeros((h, w), np.uint8)
        lbl = DATA / "labels" / "val" / f"{p.stem}.txt"
        if lbl.stat().st_size > 0:
            for line in lbl.read_text().splitlines():
                parts = line.split()
                if len(parts) > 5:
                    c = np.array(parts[1:], np.float32).reshape(-1, 2)
                    c[:, 0] *= w
                    c[:, 1] *= h
                    cv2.fillPoly(gt, [c.astype(np.int32)], 1)
        raw = None
        if not p.stem.startswith("bg_"):
            m = cv2.imread(str(RAW_MASKS / f"{p.stem}.jpg"), cv2.IMREAD_GRAYSCALE)
            raw = (m > 127).astype(np.uint8)
            assert raw.shape == gt.shape, p
        items.append({"name": p.name, "path": p, "bgr": img, "gt": gt.astype(bool),
                      "raw": None if raw is None else raw.astype(bool), "is_bg": p.stem.startswith("bg_")})
    assert len(items) == 160 and sum(i["is_bg"] for i in items) == 40
    return items


# ------------------------------------------------------------------ mô hình
def notebook_classes():
    out = {}
    for key, f, cut in [("pranet", "pranet-new.ipynb", "# 5. HÀM LOSS"), ("unet", "unet-new.ipynb", "# 4. HÀM LOSS")]:
        nb = json.loads((NB / f).read_text(encoding="utf-8"))
        code = "".join(nb["cells"][1]["source"]).split(cut)[0]
        code = re.sub(r"(?s)# 1\. SIÊU THAM SỐ.*?# 3\.", "# 3.", code)  # bỏ phần seed/thiết bị của huấn luyện
        code = code.replace("weights=models.ResNet50_Weights.DEFAULT", "weights=None")  # trọng số nạp từ .pth
        ns: dict = {}
        exec(code, ns)
        out[key] = ns["PraNet"] if key == "pranet" else (lambda ns=ns: ns["UNet"](3, 1))
    return out


def import_fork():
    """Nạp fork TSVM làm gói `ultralytics` qua junction tạm; trả về hàm dọn dẹp."""
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    sys.dont_write_bytecode = True
    tmp = Path(tempfile.mkdtemp(prefix="tsvm_fork_"))
    link = tmp / "ultralytics"
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(FORK)], check=True, capture_output=True)
    else:
        link.symlink_to(FORK, target_is_directory=True)
    sys.path.insert(0, str(tmp))
    import ultralytics  # noqa: F401
    assert Path(ultralytics.__file__).resolve().parent == FORK.resolve(), ultralytics.__file__

    def cleanup():
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "rmdir", str(link)], check=False, capture_output=True)
        else:
            link.unlink()
        os.rmdir(tmp)
    return cleanup


def predict_semantic(net, items, kind, dev):
    preds = []
    with torch.no_grad():
        for it in items:
            h, w = it["gt"].shape
            rgb = cv2.cvtColor(it["bgr"], cv2.COLOR_BGR2RGB)
            x = cv2.resize(rgb, (352, 352), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255.0
            if kind == "pranet":
                x = (x - MEAN) / STD
            t = torch.from_numpy(x).permute(2, 0, 1)[None].to(dev)
            out = net(t)
            logit = out[0] if isinstance(out, (tuple, list)) else out
            logit = F.interpolate(logit, size=(h, w), mode="bilinear", align_corners=False)
            preds.append((torch.sigmoid(logit)[0, 0] > 0.5).cpu().numpy())
    return preds


def predict_yolo(weights, items, dev):
    from ultralytics import YOLO
    model = YOLO(str(weights))
    preds = []
    for it in items:
        h, w = it["gt"].shape
        r = model.predict(it["bgr"], imgsz=640, conf=0.25, iou=0.7, retina_masks=True, half=False,
                          device=dev, verbose=False)[0]
        m = np.zeros((h, w), bool)
        if r.masks is not None and len(r.masks):
            mm = r.masks.data.cpu().numpy() > 0.5
            assert mm.shape[1:] == (h, w), (mm.shape, h, w)
            m = mm.any(0)
        preds.append(m)
    del model
    return preds


# ------------------------------------------------------------------ chỉ số
def counts(pred, gt):
    tp = int(np.logical_and(pred, gt).sum())
    fp = int(np.logical_and(pred, ~gt).sum())
    fn = int(np.logical_and(~pred, gt).sum())
    return tp, fp, fn


def per_image_metrics(tp, fp, fn):
    dice = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else np.nan
    iou = tp / (tp + fp + fn) if (tp + fp + fn) else np.nan
    prec = tp / (tp + fp) if (tp + fp) else 0.0   # không dự đoán gì trên ảnh có polyp → precision 0
    rec = tp / (tp + fn) if (tp + fn) else np.nan
    return dice, iou, prec, rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", nargs="*", type=int, default=list(range(20)))
    ap.add_argument("--models", nargs="*", default=list(MODELS))
    ap.add_argument("--tag", default="", help="hậu tố tên file kết quả (dùng khi chạy thử)")
    ap.add_argument("--tu-bang", action="store_true", help="không suy luận; lọc bang/10_pixel_tung_anh.csv theo --seeds rồi tổng hợp")
    ap.add_argument("--out", type=Path, default=OUT, help="thư mục ghi 10–12_*.csv")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.tu_bang:
        df = pd.read_csv(OUT / "10_pixel_tung_anh.csv", encoding="utf-8-sig")
        df = df[df.seed.isin(args.seeds) & df.model.isin(args.models)]
        tong_hop(df, args.out, args.tag)
        return
    assert torch.cuda.is_available(), "Cần GPU (chạy bằng C:\\venv_kl_gpu\\Scripts\\python.exe)"
    dev = "cuda:0"
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    print("GPU:", torch.cuda.get_device_name(0), "| torch", torch.__version__)

    items = load_val()
    print(f"Validation: {len(items)} ảnh ({sum(not i['is_bg'] for i in items)} polyp, {sum(i['is_bg'] for i in items)} nền)")
    cleanup = import_fork()
    import ultralytics
    print("ultralytics:", ultralytics.__version__, ultralytics.__file__)
    nbc = notebook_classes()
    QUAL.mkdir(parents=True, exist_ok=True)

    rows = []
    t0 = time.time()
    try:
        for key in args.models:
            for s in args.seeds:
                w = MODELS[key][1](s)
                t1 = time.time()
                if key in ("baseline", "tsvm"):
                    preds = predict_yolo(w, items, dev)
                else:
                    net = nbc[key]()
                    net.load_state_dict(torch.load(w, map_location="cpu"), strict=True)
                    net = net.to(dev).eval()
                    preds = predict_semantic(net, items, key, dev)
                    del net
                torch.cuda.empty_cache()
                for it, pr in zip(items, preds):
                    tp, fp, fn = counts(pr, it["gt"])
                    row = {"model": key, "seed": s, "image": it["name"], "is_bg": it["is_bg"],
                           "pred_px": int(pr.sum()), "gt_px": int(it["gt"].sum()), "img_px": it["gt"].size,
                           "tp": tp, "fp": fp, "fn": fn}
                    if it["raw"] is not None:
                        rtp, rfp, rfn = counts(pr, it["raw"])
                        row.update(raw_tp=rtp, raw_fp=rfp, raw_fn=rfn)
                    rows.append(row)
                if s == 0:   # lưu mặt nạ seed 0 cho hình định tính
                    np.savez_compressed(QUAL / f"pred_seed0_{key}.npz",
                                        **{it["name"]: np.packbits(pr) for it, pr in zip(items, preds)},
                                        **{f"__shape__{it['name']}": np.array(pr.shape) for it, pr in zip(items, preds)})
                print(f"  {key:8s} seed {s:2d}: {time.time() - t1:5.1f}s")
    finally:
        cleanup()
    print(f"Tổng thời gian suy luận: {(time.time() - t0) / 60:.1f} phút")

    tong_hop(pd.DataFrame(rows), args.out, args.tag)


def tong_hop(df: pd.DataFrame, out: Path, tag: str) -> None:
    """Ghi 10_ (từng ảnh), 11_ (từng seed), 12_ (thống kê) vào thư mục out."""
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / f"10_pixel_tung_anh{tag}.csv", index=False, encoding="utf-8-sig")

    # --- tổng hợp theo seed
    seed_rows = []
    for (key, s), g in df.groupby(["model", "seed"], sort=False):
        pol, bg = g[~g.is_bg], g[g.is_bg]
        r = {"model": key, "seed": s}
        for pre, (tpc, fpc, fnc) in [("", ("tp", "fp", "fn")), ("raw_", ("raw_tp", "raw_fp", "raw_fn"))]:
            m = np.array([per_image_metrics(a, b, c) for a, b, c in zip(pol[tpc], pol[fpc], pol[fnc])])
            r[f"{pre}dice"], r[f"{pre}iou"], r[f"{pre}precision"], r[f"{pre}recall"] = np.nanmean(m, 0)
            TP, FP, FN = pol[tpc].sum(), pol[fpc].sum(), pol[fnc].sum()
            r[f"{pre}dice_micro"] = 2 * TP / (2 * TP + FP + FN)
            r[f"{pre}iou_micro"] = TP / (TP + FP + FN)
        r["polyp_imgs_no_pred"] = int((pol.pred_px == 0).sum())
        r["bg_fp_image_rate"] = float((bg.pred_px > 0).mean())
        r["bg_fp_area_mean"] = float((bg.pred_px / bg.img_px).mean())
        seed_rows.append(r)
    sd = pd.DataFrame(seed_rows)
    sd.to_csv(out / f"11_pixel_tung_seed{tag}.csv", index=False, encoding="utf-8-sig")

    # --- thống kê: mean ± SD và so sánh ghép cặp TSVM với từng mô hình
    metrics = ["dice", "iou", "precision", "recall", "dice_micro", "iou_micro", "bg_fp_image_rate",
               "raw_dice", "raw_iou", "raw_precision", "raw_recall"]
    st_rows = []
    for key in sd.model.unique():
        g = sd[sd.model == key]
        for m in metrics:
            st_rows.append({"model": key, "label": MODELS[key][0], "metric": m, "n_seeds": len(g),
                            "mean": g[m].mean(), "sd": g[m].std(ddof=1), "min": g[m].min(), "max": g[m].max()})
    if "tsvm" in set(sd.model):
        t = sd[sd.model == "tsvm"].set_index("seed")
        for other in [k for k in sd.model.unique() if k != "tsvm"]:
            o = sd[sd.model == other].set_index("seed")
            common = t.index.intersection(o.index)
            if len(common) < 3:
                continue
            for m in metrics:
                d = t.loc[common, m] - o.loc[common, m]
                ok = d.std() > 0
                st_rows.append({"model": f"tsvm_vs_{other}", "metric": m, "n_seeds": len(common), "mean": d.mean(),
                                "sd": d.std(ddof=1),
                                "paired_t_p": stats.ttest_rel(t.loc[common, m], o.loc[common, m]).pvalue if ok else np.nan,
                                "wilcoxon_p": stats.wilcoxon(t.loc[common, m], o.loc[common, m]).pvalue if ok else np.nan,
                                "tsvm_higher": int((d > 0).sum())})
    stt = pd.DataFrame(st_rows)
    stt.to_csv(out / f"12_pixel_thong_ke{tag}.csv", index=False, encoding="utf-8-sig")
    with pd.option_context("display.float_format", "{:.4f}".format, "display.width", 220, "display.max_rows", 200):
        print(stt[stt.metric.isin(["dice", "iou", "precision", "recall", "bg_fp_image_rate", "raw_dice"])].to_string(index=False))


if __name__ == "__main__":
    main()
