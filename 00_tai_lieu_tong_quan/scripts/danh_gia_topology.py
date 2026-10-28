"""Chỉ số topology (lỗi Betti) cho 4 mô hình × 20 seed trên 160 ảnh validation BG20.

Dùng lại đúng giao thức suy luận của danh_gia_pixel.py (nhãn polygon ở độ phân giải gốc; YOLO imgsz 640,
conf 0,25, iou 0,7, retina_masks; PraNet/U-Net resize 352, ngưỡng 0,5). Chỉ suy luận, không sửa checkpoint.

Với mỗi ảnh, đếm trên mặt nạ dự đoán và mặt nạ nhãn:
- b0: số thành phần liên thông của vùng polyp (8-liên thông) = số "mảnh";
- b1: số lỗ = số vùng nền (4-liên thông) không chạm biên ảnh.
Chỉ đếm mảnh và lỗ có diện tích >= MIN_AREA pixel. Ngưỡng chính là 20 pixel, trùng ngưỡng loại đốm nhiễu
khi tạo nhãn (Chương 4); ngưỡng 0 (đếm mọi mảnh) ghi kèm để kiểm tra độ nhạy.

Chỉ số theo seed (trên 120 ảnh polyp):
- err_b0, err_b1: trung bình |b_pred − b_gt|;
- topo_ok: tỉ lệ ảnh có b0 và b1 đều khớp nhãn;
- frag_rate: tỉ lệ ảnh dự đoán nhiều mảnh hơn nhãn (vỡ mảnh hoặc thêm vùng thừa);
- hole_rate: tỉ lệ ảnh có ít nhất một lỗ trong mặt nạ dự đoán;
- miss_rate: tỉ lệ ảnh dự đoán ít mảnh hơn nhãn (sót polyp hoặc hai polyp dính thành một).
Trên 40 ảnh nền: bg_b0 = số mảnh thừa trung bình.

Kết quả: ../bang/13_topology_tung_anh.csv, 14_topology_tung_seed.csv, 15_topology_thong_ke.csv
(và bản 10 seed trong ../bang/10seed/ để đối chiếu).

    C:\\venv_kl_gpu\\Scripts\\python.exe danh_gia_topology.py                 # 4 mô hình × 20 seed (cần GPU)
    C:\\venv_kl_gpu\\Scripts\\python.exe danh_gia_topology.py --tu-bang       # chỉ tổng hợp lại từ bảng 13
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

import danh_gia_pixel as dg

MIN_AREAS = (20, 0)          # ngưỡng chính trước, ngưỡng kiểm tra độ nhạy sau
METRICS = ["err_b0", "err_b1", "topo_ok", "frag_rate", "hole_rate", "miss_rate", "bg_b0"]


def betti(mask: np.ndarray, min_area: int) -> tuple[int, int]:
    """(b0, b1) của mặt nạ nhị phân, bỏ mảnh/lỗ nhỏ hơn min_area pixel."""
    m = mask.astype(np.uint8)
    n, _, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
    b0 = int((st[1:, cv2.CC_STAT_AREA] >= max(min_area, 1)).sum())
    # Lỗ: vùng nền 4-liên thông không chạm biên. Đệm 1 pixel nền để mọi vùng chạm biên nối với nhau.
    bg = np.pad(1 - m, 1, constant_values=1)
    n, lab, st, _ = cv2.connectedComponentsWithStats(bg, connectivity=4)
    outer = lab[0, 0]
    b1 = int(sum(1 for i in range(1, n) if i != outer and st[i, cv2.CC_STAT_AREA] >= max(min_area, 1)))
    return b0, b1


def tong_hop(df: pd.DataFrame, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "13_topology_tung_anh.csv", index=False, encoding="utf-8-sig")
    rows = []
    for (key, s, a), g in df.groupby(["model", "seed", "min_area"], sort=False):
        pol, bg = g[~g.is_bg], g[g.is_bg]
        d0, d1 = pol.b0_pred - pol.b0_gt, pol.b1_pred - pol.b1_gt
        rows.append({"model": key, "seed": s, "min_area": a,
                     "err_b0": d0.abs().mean(), "err_b1": d1.abs().mean(),
                     "topo_ok": ((d0 == 0) & (d1 == 0)).mean(),
                     "frag_rate": (d0 > 0).mean(), "hole_rate": (pol.b1_pred > 0).mean(),
                     "miss_rate": (d0 < 0).mean(), "bg_b0": bg.b0_pred.mean()})
    sd = pd.DataFrame(rows)
    sd.to_csv(out / "14_topology_tung_seed.csv", index=False, encoding="utf-8-sig")

    st_rows = []
    for a in sd.min_area.unique():
        sa = sd[sd.min_area == a]
        for key in sa.model.unique():
            g = sa[sa.model == key]
            for m in METRICS:
                st_rows.append({"min_area": a, "model": key, "metric": m, "n_seeds": len(g), "mean": g[m].mean(),
                                "sd": g[m].std(ddof=1), "min": g[m].min(), "max": g[m].max()})
        if "tsvm" not in set(sa.model):
            continue
        t = sa[sa.model == "tsvm"].set_index("seed")
        for other in [k for k in sa.model.unique() if k != "tsvm"]:
            o = sa[sa.model == other].set_index("seed")
            common = t.index.intersection(o.index)
            for m in METRICS:
                d = t.loc[common, m] - o.loc[common, m]
                ok = len(common) >= 3 and d.std() > 0
                st_rows.append({"min_area": a, "model": f"tsvm_vs_{other}", "metric": m, "n_seeds": len(common),
                                "mean": d.mean(), "sd": d.std(ddof=1),
                                "paired_t_p": stats.ttest_rel(t.loc[common, m], o.loc[common, m]).pvalue if ok else np.nan,
                                "wilcoxon_p": stats.wilcoxon(t.loc[common, m], o.loc[common, m]).pvalue if ok else np.nan,
                                "tsvm_lower": int((d < 0).sum()), "tsvm_higher": int((d > 0).sum())})
    stt = pd.DataFrame(st_rows)
    stt.to_csv(out / "15_topology_thong_ke.csv", index=False, encoding="utf-8-sig")
    with pd.option_context("display.float_format", "{:.4f}".format, "display.width", 220, "display.max_rows", 300):
        print(f"== {out}")
        print(stt[stt.min_area == MIN_AREAS[0]].to_string(index=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", nargs="*", type=int, default=list(range(20)))
    ap.add_argument("--models", nargs="*", default=list(dg.MODELS))
    ap.add_argument("--tu-bang", action="store_true", help="không suy luận; tổng hợp lại từ bang/13_topology_tung_anh.csv")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.tu_bang:
        df = pd.read_csv(dg.OUT / "13_topology_tung_anh.csv", encoding="utf-8-sig")
    else:
        assert torch.cuda.is_available(), "Cần GPU (chạy bằng C:\\venv_kl_gpu\\Scripts\\python.exe)"
        dev = "cuda:0"
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True
        items = dg.load_val()
        gt_b = {it["name"]: {a: betti(it["gt"], a) for a in MIN_AREAS} for it in items}
        cleanup = dg.import_fork()
        nbc = dg.notebook_classes()
        rows, t0 = [], time.time()
        try:
            for key in args.models:
                for s in args.seeds:
                    w, t1 = dg.MODELS[key][1](s), time.time()
                    if key in ("baseline", "tsvm"):
                        preds = dg.predict_yolo(w, items, dev)
                    else:
                        net = nbc[key]()
                        net.load_state_dict(torch.load(w, map_location="cpu"), strict=True)
                        preds = dg.predict_semantic(net.to(dev).eval(), items, key, dev)
                        del net
                    torch.cuda.empty_cache()
                    for it, pr in zip(items, preds):
                        for a in MIN_AREAS:
                            b0, b1 = betti(pr, a)
                            g0, g1 = gt_b[it["name"]][a]
                            rows.append({"model": key, "seed": s, "image": it["name"], "is_bg": it["is_bg"], "min_area": a,
                                         "b0_pred": b0, "b1_pred": b1, "b0_gt": g0, "b1_gt": g1, "pred_px": int(pr.sum())})
                    print(f"  {key:8s} seed {s:2d}: {time.time() - t1:5.1f}s", flush=True)
        finally:
            cleanup()
        print(f"Tổng thời gian suy luận: {(time.time() - t0) / 60:.1f} phút")
        df = pd.DataFrame(rows)

    tong_hop(df, dg.OUT)
    tong_hop(df[df.seed < 10], dg.OUT / "10seed")


if __name__ == "__main__":
    main()
