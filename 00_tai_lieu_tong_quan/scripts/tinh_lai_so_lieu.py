"""Tính lại toàn bộ số liệu dùng trong bộ tài liệu TaiLieu_TongQuan_Base_TSVM_FP32.

Script CHỈ ĐỌC dữ liệu gốc trong các thư mục 01–04 và 99_luu_tru/ và ghi kết quả vào ../bang/.
Không huấn luyện, không suy luận, không sửa file nào ngoài ../bang/.

Chạy:
    python tinh_lai_so_lieu.py            # phần dữ liệu + kết quả huấn luyện (cần numpy, pandas, scipy, pyyaml, pillow)
    python tinh_lai_so_lieu.py --torch    # thêm kiểm tra checkpoint và dựng lại mô hình (cần torch)
    python tinh_lai_so_lieu.py --seeds 10 # chỉ dùng seed 0..9, ghi vào ../bang/10seed/ (bảng 20 seed giữ nguyên)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from PIL import Image
from scipy import stats

HERE = Path(__file__).resolve().parent
DOC = HERE.parent
REPO = DOC.parent
DATA = REPO / "01_du_lieu"
DATASET = DATA / "Kvasir_YOLO_SEG_BG20"
FORK = REPO / "02_ma_nguon" / "ultralytics_TSVM_FP32"
RUNS_DIR = REPO / "03_ket_qua_huan_luyen"
PKG = REPO / "04_phan_tich_20seed"
OLD_TSVM = REPO / "99_luu_tru" / "ket_qua_cu" / "TSVM_cu_checkpoint_FP16_seed0-20"
OUT = DOC / "bang"

SEEDS = range(20)
RUNS = {
    "Baseline": RUNS_DIR / "Baseline_YOLO26s_seg" / "Kvasir_BG20_Baseline_YOLO26s_seg_s{}_w2",
    "TSVM_FP32": RUNS_DIR / "TSVM_FP32" / "Kvasir_BG20_YOLO26s_seg_TSVM_FP32_s{}_w2",
}
METRICS = {  # tên ngắn -> (cột results.csv, chiều tốt hơn)
    "mask_map50_95": ("metrics/mAP50-95(M)", "higher"),
    "mask_map50": ("metrics/mAP50(M)", "higher"),
    "mask_precision": ("metrics/precision(M)", "higher"),
    "mask_recall": ("metrics/recall(M)", "higher"),
    "box_map50_95": ("metrics/mAP50-95(B)", "higher"),
    "box_map50": ("metrics/mAP50(B)", "higher"),
    "box_precision": ("metrics/precision(B)", "higher"),
    "box_recall": ("metrics/recall(B)", "higher"),
    "val_seg_loss": ("val/seg_loss", "lower"),
    "val_box_loss": ("val/box_loss", "lower"),
    "val_cls_loss": ("val/cls_loss", "lower"),
    "val_l1_loss": ("val/l1_loss", "lower"),
    "val_sem_loss": ("val/sem_loss", "lower"),
}
ARGKEYS = ["model", "pretrained", "data", "epochs", "imgsz", "batch", "device", "workers", "optimizer", "lr0",
           "lrf", "momentum", "weight_decay", "warmup_epochs", "cos_lr", "close_mosaic", "amp", "deterministic",
           "patience", "mosaic", "mixup", "fliplr", "flipud", "degrees", "scale", "translate", "hsv_h", "hsv_s",
           "hsv_v", "overlap_mask", "mask_ratio", "iou", "conf", "max_det", "rect", "cache"]


def read_results(run: Path) -> pd.DataFrame:
    df = pd.read_csv(run / "results.csv")
    df.columns = [c.strip() for c in df.columns]
    return df


def section(title: str) -> None:
    print(f"\n{'=' * 8} {title} {'=' * 8}")


# ---------------------------------------------------------------- 1. Dữ liệu
def dataset_audit() -> dict:
    section("1. Dữ liệu BG20")
    res = {}
    hashes = {}
    rows = []
    for split in ("train", "val"):
        imgs = sorted((DATASET / "images" / split).glob("*.jpg"))
        lbls = sorted((DATASET / "labels" / split).glob("*.txt"))
        img_stems = {p.stem for p in imgs}
        lbl_stems = {p.stem for p in lbls}
        n_bg = sum(p.stem.startswith("bg_") for p in imgs)
        empty = [p for p in lbls if p.stat().st_size == 0]
        empty_non_bg = [p.name for p in empty if not p.stem.startswith("bg_")]
        n_inst, n_pts, multi = 0, [], 0
        for p in lbls:
            lines = [l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
            n_inst += len(lines)
            multi += len(lines) > 1
            for l in lines:
                vals = l.split()
                assert vals[0] == "0", f"class khác 0 trong {p}"
                coords = list(map(float, vals[1:]))
                assert len(coords) % 2 == 0 and all(0.0 <= c <= 1.0 for c in coords), p
                n_pts.append(len(coords) // 2)
        sizes = {}
        for p in imgs:
            with Image.open(p) as im:
                sizes[im.size] = sizes.get(im.size, 0) + 1
            hashes.setdefault(split, {})[hashlib.sha256(p.read_bytes()).hexdigest()] = p.name
        r = {
            "split": split, "images": len(imgs), "labels": len(lbls), "background_images": n_bg,
            "polyp_images": len(imgs) - n_bg, "empty_labels": len(empty), "empty_labels_not_bg": len(empty_non_bg),
            "polyp_instances": n_inst, "images_with_multiple_instances": multi,
            "image_label_stem_match": img_stems == lbl_stems,
            "polygon_points_min": min(n_pts), "polygon_points_median": float(np.median(n_pts)),
            "polygon_points_max": max(n_pts), "distinct_image_sizes": len(sizes),
            "most_common_size": "%dx%d" % max(sizes, key=sizes.get),
            "most_common_size_count": max(sizes.values()),
        }
        rows.append(r)
    df = pd.DataFrame(rows)
    dup = set(hashes["train"]) & set(hashes["val"])
    print(df.T.to_string(header=False))
    print("Ảnh trùng byte giữa train và val:", len(dup))
    # Đối chiếu danh sách split với dataset
    train_ids = {l.strip() for l in (DATA / "train.txt").read_text(encoding="utf-8").splitlines() if l.strip()}
    val_ids = {l.strip() for l in (DATA / "val.txt").read_text(encoding="utf-8").splitlines() if l.strip()}
    ds_train = {p.stem for p in (DATASET / "images" / "train").glob("*.jpg") if not p.stem.startswith("bg_")}
    ds_val = {p.stem for p in (DATASET / "images" / "val").glob("*.jpg") if not p.stem.startswith("bg_")}
    bg_train = {l.strip() for l in (DATASET / "selected_normal_cecum_train_160.txt").read_text().splitlines() if l.strip()}
    bg_val = {l.strip() for l in (DATASET / "selected_normal_cecum_val_40.txt").read_text().splitlines() if l.strip()}
    ds_bg_train = {p.name[3:] for p in (DATASET / "images" / "train").glob("bg_*.jpg")}
    ds_bg_val = {p.name[3:] for p in (DATASET / "images" / "val").glob("bg_*.jpg")}
    checks = {
        "train.txt (880) == ảnh polyp train": train_ids == ds_train and len(train_ids) == 880,
        "val.txt (120) == ảnh polyp val": val_ids == ds_val and len(val_ids) == 120,
        "train.txt giao val.txt rỗng": not (train_ids & val_ids),
        "danh sách nền train (160) == ảnh bg train": bg_train == ds_bg_train and len(bg_train) == 160,
        "danh sách nền val (40) == ảnh bg val": bg_val == ds_bg_val and len(bg_val) == 40,
        "nền train giao nền val rỗng": not (bg_train & bg_val),
    }
    for k, v in checks.items():
        print(f"  {'OK ' if v else 'SAI'} {k}")
    df.to_csv(OUT / "01_du_lieu_bg20.csv", index=False, encoding="utf-8-sig")
    res.update(dup_train_val=len(dup), checks=checks)
    return res


# ---------------------------------------------------------------- 2. Kết quả huấn luyện
def training_audit() -> pd.DataFrame:
    section(f"2. {2 * len(SEEDS)} lượt huấn luyện (seed 0–{len(SEEDS) - 1})")
    rows, args_rows, curves = [], [], []
    for model, pat in RUNS.items():
        for s in SEEDS:
            run = Path(str(pat).format(s))
            df = read_results(run)
            i = int(df["metrics/mAP50-95(M)"].values.argmax())  # dòng ĐẦU TIÊN đạt cực đại mask mAP50-95
            fit = (df["metrics/mAP50-95(B)"] + df["metrics/mAP50-95(M)"]).values
            j = int(fit.argmax())
            r = {"model": model, "seed": s, "epochs_logged": len(df),
                 "max_mask_epoch": int(df["epoch"].iloc[i]), "fitness_epoch": int(df["epoch"].iloc[j]),
                 "last_epoch_mask_map50_95": float(df["metrics/mAP50-95(M)"].iloc[-1]),
                 "fitness_epoch_mask_map50_95": float(df["metrics/mAP50-95(M)"].iloc[j]),
                 "train_time_s": float(df["time"].iloc[-1])}
            for k, (c, _) in METRICS.items():
                r[k] = float(df[c].iloc[i])
            r["has_best_pt"] = (run / "weights" / "best.pt").is_file()
            rows.append(r)
            a = yaml.safe_load((run / "args.yaml").read_text(encoding="utf-8"))
            args_rows.append({"group": model, "run_seed": s, "seed": a.get("seed"), **{k: a.get(k) for k in ARGKEYS}})
            c = df[["epoch", "metrics/mAP50-95(M)", "metrics/mAP50-95(B)", "val/seg_loss", "train/seg_loss",
                    "train/sem_loss", "val/sem_loss"]].copy()
            c.insert(0, "seed", s)
            c.insert(0, "model", model)
            curves.append(c)
    per = pd.DataFrame(rows)
    per.to_csv(OUT / "02_ket_qua_tung_seed.csv", index=False, encoding="utf-8-sig")

    # Cấu hình
    A = pd.DataFrame(args_rows)
    print("seed trong args.yaml == seed trong tên thư mục:", bool((A["seed"] == A["run_seed"]).all()))
    print("Số epoch ghi trong results.csv:", sorted(per.epochs_logged.unique()), "| đủ best.pt:", bool(per.has_best_pt.all()))
    cfg_rows = []
    for k in ARGKEYS:
        vals = {g: sorted({str(v) for v in A.loc[A.group == g, k]}) for g in RUNS}
        cfg_rows.append({"tham_so": k, "Baseline": "; ".join(vals["Baseline"]), "TSVM_FP32": "; ".join(vals["TSVM_FP32"]),
                         "giong_nhau": vals["Baseline"] == vals["TSVM_FP32"]})
    cfg = pd.DataFrame(cfg_rows)
    cfg.to_csv(OUT / "03_cau_hinh_args.csv", index=False, encoding="utf-8-sig")
    print(cfg.to_string(index=False))

    # Thống kê ghép cặp
    b = per[per.model == "Baseline"].sort_values("seed")
    t = per[per.model == "TSVM_FP32"].sort_values("seed")
    srows = []
    for k, (_, better) in METRICS.items():
        x, y = b[k].to_numpy(), t[k].to_numpy()
        d = y - x
        r = {"metric": k, "better": better, "baseline_mean": x.mean(), "baseline_sd": x.std(ddof=1),
             "baseline_min": x.min(), "baseline_max": x.max(), "tsvm_mean": y.mean(), "tsvm_sd": y.std(ddof=1),
             "tsvm_min": y.min(), "tsvm_max": y.max(), "delta": d.mean()}
        if d.std() > 0:
            se = d.std(ddof=1) / math.sqrt(len(d))
            q = stats.t.ppf(0.975, len(d) - 1)
            wins = int((d > 0).sum() if better == "higher" else (d < 0).sum())
            r.update(ci95_low=d.mean() - q * se, ci95_high=d.mean() + q * se,
                     paired_t_p=stats.ttest_rel(y, x).pvalue, wilcoxon_p=stats.wilcoxon(y, x).pvalue,
                     cohen_dz=d.mean() / d.std(ddof=1), tsvm_better_seeds=wins,
                     sign_test_p=stats.binomtest(wins, len(d)).pvalue)
        srows.append(r)
    summ = pd.DataFrame(srows)
    summ.to_csv(OUT / "04_thong_ke_ghep_cap.csv", index=False, encoding="utf-8-sig")
    with pd.option_context("display.float_format", "{:.6f}".format, "display.width", 250):
        print(summ.to_string(index=False))

    # Lựa chọn epoch
    per["epoch_khac"] = per.max_mask_epoch != per.fitness_epoch
    print("Số lượt epoch cực đại mask khác epoch fitness (best.pt):", int(per.epoch_khac.sum()),
          per.groupby("model").epoch_khac.sum().to_dict())
    print("Thời gian huấn luyện (giờ) mean theo model:", (per.groupby("model").train_time_s.mean() / 3600).round(3).to_dict())
    for m in RUNS:
        g = per[per.model == m]
        print(f"  {m}: mask AP tại epoch fitness mean={g.fitness_epoch_mask_map50_95.mean():.6f}, "
              f"tại epoch 100 mean={g.last_epoch_mask_map50_95.mean():.6f}, "
              f"epoch cực đại mask: min={g.max_mask_epoch.min()} median={g.max_mask_epoch.median()} max={g.max_mask_epoch.max()}")

    # Power của paired t-test hai phía (alpha 0,05) nếu hiệu ứng thật bằng d_z quan sát được
    dz = float(summ.set_index("metric").loc["mask_map50_95", "cohen_dz"])

    def power(n: int) -> float:
        tc, nc = stats.t.ppf(0.975, n - 1), dz * math.sqrt(n)
        return 1 - stats.nct.cdf(tc, n - 1, nc) + stats.nct.cdf(-tc, n - 1, nc)

    n80 = next(n for n in range(3, 1000) if power(n) >= 0.8)
    print(f"Power với d_z={dz:.3f}: n={len(SEEDS)} -> {power(len(SEEDS)):.3f}; số cặp cần cho power 80%: {n80} ({power(n80):.3f})")

    # Phân tích độ nhạy: cùng phép so sánh nhưng đổi quy tắc chọn epoch
    sens = []
    for col, rule in [("mask_map50_95", "epoch cực đại mask mAP50-95 (endpoint chính)"),
                      ("fitness_epoch_mask_map50_95", "epoch fitness box+mask (epoch của best.pt)"),
                      ("last_epoch_mask_map50_95", "epoch 100 (cuối huấn luyện)")]:
        x, y = b[col].to_numpy(), t[col].to_numpy()
        d = y - x
        sens.append({"quy_tac": rule, "baseline_mean": x.mean(), "baseline_sd": x.std(ddof=1), "tsvm_mean": y.mean(),
                     "tsvm_sd": y.std(ddof=1), "delta": d.mean(), "paired_t_p": stats.ttest_rel(y, x).pvalue,
                     "wilcoxon_p": stats.wilcoxon(y, x).pvalue, "tsvm_better_seeds": int((d > 0).sum())})
    sens = pd.DataFrame(sens)
    sens.to_csv(OUT / "04b_do_nhay_quy_tac_epoch.csv", index=False, encoding="utf-8-sig")
    with pd.option_context("display.float_format", "{:.6f}".format, "display.width", 250):
        print(sens.to_string(index=False))

    # Đường cong theo epoch
    cv = pd.concat(curves)
    agg = cv.groupby(["model", "epoch"]).agg(
        mask_map_mean=("metrics/mAP50-95(M)", "mean"), mask_map_sd=("metrics/mAP50-95(M)", lambda s: s.std(ddof=1)),
        val_seg_mean=("val/seg_loss", "mean"), val_seg_sd=("val/seg_loss", lambda s: s.std(ddof=1)),
        train_seg_mean=("train/seg_loss", "mean"), train_sem_mean=("train/sem_loss", "mean"),
        val_sem_absmax=("val/sem_loss", lambda s: s.abs().max())).reset_index()
    agg.to_csv(OUT / "05_duong_cong_theo_epoch.csv", index=False, encoding="utf-8-sig")
    key = agg[agg.epoch.isin([1, 5, 10, 20, 30, 50, 70, 90, 100])]
    with pd.option_context("display.float_format", "{:.4f}".format, "display.width", 200):
        print(key.to_string(index=False))
    mean_w = agg.pivot(index="epoch", columns="model", values="mask_map_mean")
    sd_w = agg.pivot(index="epoch", columns="model", values="mask_map_sd")
    gap = mean_w["TSVM_FP32"] - mean_w["Baseline"]
    print("Epoch (>=50) có mean mask mAP của TSVM <= Baseline:", [int(e) for e in gap[(gap <= 0) & (gap.index >= 50)].index])
    print("Số epoch SD mask mAP của TSVM > Baseline:", int((sd_w["TSVM_FP32"] > sd_w["Baseline"]).sum()), "/", len(sd_w))
    for m in RUNS:
        g = agg[agg.model == m]
        ep_min_val = int(g.loc[g.val_seg_mean.idxmin(), "epoch"])
        print(f"  {m}: val seg loss trung bình nhỏ nhất tại epoch {ep_min_val} = {g.val_seg_mean.min():.4f}; "
              f"epoch 100 = {g.val_seg_mean.iloc[-1]:.4f}")
    return per


# ---------------------------------------------------------------- 3. Đối chiếu gói phân tích
def compare_package(per: pd.DataFrame) -> None:
    section("3. Đối chiếu với KQ_Nen_DX_20seed_FP32")
    raw = pd.read_csv(PKG / "01_raw_analysis" / "raw_20seeds_extracted_metrics.csv", encoding="utf-8-sig")
    raw["model"] = raw["model"].replace({"TSVM": "TSVM_FP32"})
    m = per.merge(raw, on=["model", "seed"], suffixes=("", "_pkg"))
    bad = sum(int(((m[k] - m[f"{k}_pkg"]).abs() > 1e-9).sum()) for k in METRICS)
    bad += int((m.max_mask_epoch != m.best_epoch).sum())
    print(f"Ghép {len(m)}/40 dòng; số ô lệch so với raw CSV của gói: {bad}")
    summ = pd.read_csv(PKG / "06_reports" / "summary.csv", encoding="utf-8-sig").set_index("metric")
    ours = pd.read_csv(OUT / "04_thong_ke_ghep_cap.csv").set_index("metric")
    pairs = [("baseline_mean", "baseline_mean"), ("tsvm_mean", "tsvm_mean"), ("delta", "delta_tsvm_minus_baseline"),
             ("paired_t_p", "paired_t_p"), ("ci95_low", "delta_ci95_low"), ("ci95_high", "delta_ci95_high")]
    worst = max(abs(ours.loc[k, a] - summ.loc[k, b]) for k in METRICS for a, b in pairs
                if not (pd.isna(ours.loc[k, a]) or pd.isna(summ.loc[k, b])))
    print(f"Sai số lớn nhất so với 06_reports/summary.csv: {worst:.2e}")


def lineage_check() -> None:
    section(f"3b. TSVM cũ (checkpoint FP16) so với TSVM FP32, seed 0-{len(SEEDS) - 1}")
    old = OLD_TSVM / "Kvasir_BG20_YOLO26s_seg_TSVM_s{}_w2"
    same = diff = 0
    cols = set()
    for s in SEEDS:
        a = read_results(Path(str(old).format(s)))
        b = read_results(Path(str(RUNS["TSVM_FP32"]).format(s)))
        for c in a.columns:
            eq = a[c].to_numpy() == b[c].to_numpy()
            same += int(eq.sum())
            diff += int((~eq).sum())
            if not eq.all():
                cols.add(c)
    print(f"Ô giống nhau: {same}; ô khác: {diff}; cột khác: {sorted(cols)}")


# ---------------------------------------------------------------- 4. Ma trận nhầm lẫn
def confusion_audit() -> None:
    section("4. Ma trận nhầm lẫn (TP/FP/FN đối tượng)")
    cm = pd.read_csv(PKG / "01_raw_analysis" / "raw_20seeds_confusion_matrices.csv", encoding="utf-8-sig")
    cm["model"] = cm["model"].replace({"TSVM": "TSVM_FP32"})
    cm = cm[cm.seed.isin(SEEDS)]
    print("TP+FN == 127 ở mọi dòng:", bool(((cm.TP + cm.FN) == 127).all()), "| số dòng:", len(cm))
    g = cm.groupby("model")[["TP", "FP", "FN"]].agg(["mean", "std", "min", "max"])
    print(g.round(2).to_string())
    b = cm[cm.model == "Baseline"].sort_values("seed")
    t = cm[cm.model == "TSVM_FP32"].sort_values("seed")
    for k in ("TP", "FP", "FN"):
        d = t[k].to_numpy() - b[k].to_numpy()
        p = stats.wilcoxon(t[k], b[k]).pvalue if np.any(d != 0) else float("nan")
        print(f"  {k}: Δ mean={d.mean():+.2f}, Wilcoxon p={p:.4f}")
    cm.to_csv(OUT / "06_ma_tran_nham_lan_tung_seed.csv", index=False, encoding="utf-8-sig")


# ---------------------------------------------------------------- 5. Torch: checkpoint + dựng mô hình
def torch_audit() -> None:
    section("5. Checkpoint best.pt và dựng lại kiến trúc")
    import tempfile
    import subprocess

    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    sys.dont_write_bytecode = True
    # Nạp fork làm gói `ultralytics` qua một junction/symlink tạm (không ghi vào fork).
    tmp = Path(tempfile.mkdtemp(prefix="tsvm_fork_"))
    link = tmp / "ultralytics"
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(FORK)], check=True, capture_output=True)
    else:
        link.symlink_to(FORK, target_is_directory=True)
    sys.path.insert(0, str(tmp))
    import torch
    import ultralytics
    from ultralytics.nn.tasks import SegmentationModel

    print("ultralytics nạp từ:", ultralytics.__file__, ultralytics.__version__)
    rows = []
    for model, pat in RUNS.items():
        for s in SEEDS:
            p = Path(str(pat).format(s)) / "weights" / "best.pt"
            ck = torch.load(p, map_location="cpu", weights_only=False)
            net = ck.get("ema") or ck.get("model")
            sd = net.state_dict()
            dtypes = sorted({str(v.dtype) for v in sd.values() if torch.is_tensor(v) and v.is_floating_point()})
            finite = all(torch.isfinite(v).all().item() for v in sd.values() if torch.is_tensor(v) and v.is_floating_point())
            n_par = sum(v.numel() for v in net.parameters())
            rows.append({"model": model, "seed": s, "epoch_saved": ck.get("epoch"), "dtypes": "|".join(dtypes),
                         "all_finite": finite, "params": n_par, "file_MiB": round(p.stat().st_size / 2**20, 2),
                         "ultralytics_version": ck.get("version")})
    ckdf = pd.DataFrame(rows)
    ckdf.to_csv(OUT / "07_checkpoint_best_pt.csv", index=False, encoding="utf-8-sig")
    print(ckdf.groupby("model").agg(dtypes=("dtypes", lambda s: sorted(set(s))), finite=("all_finite", "all"),
                                    params=("params", lambda s: sorted(set(s))), MiB=("file_MiB", "mean"),
                                    version=("ultralytics_version", lambda s: sorted(set(map(str, s))))).to_string())
    # strip_optimizer đặt epoch=-1 cho best.pt cuối cùng nên không dùng trường này để suy ra epoch đã lưu.
    print("Giá trị epoch lưu trong best.pt:", sorted(ckdf.epoch_saved.unique()))

    cfgdir = FORK / "cfg" / "models" / "26"
    arch = []
    for model, fname in [("Baseline", "yolo26-seg.yaml"), ("TSVM_FP32", "yolo26-seg-TopologyShapeVMamba.yaml")]:
        cfg = yaml.safe_load((cfgdir / fname).read_text(encoding="utf-8"))
        cfg["scale"] = "s"
        net = SegmentationModel(cfg, nc=1, verbose=False).eval()
        shapes = {}
        hooks = [net.model[i].register_forward_hook(lambda m, i_, o, k=i: shapes.__setitem__(k, tuple(o.shape)))
                 for i in range(23)]
        with torch.no_grad():
            net(torch.zeros(1, 3, 640, 640))
        for h in hooks:
            h.remove()
        l10 = net.model[10]
        r = {"model": model, "params": sum(p.numel() for p in net.parameters()), "layer10": type(l10).__name__,
             "layer10_params": sum(p.numel() for p in l10.parameters()),
             **{f"out_layer{k}": "x".join(map(str, v[1:])) for k, v in shapes.items()}}
        if model == "TSVM_FP32":
            blk = l10.m[0]
            r.update(hidden_c=l10.c, n_blocks=len(l10.m), mode=blk.mode, gamma_init=round(blk.gamma.item(), 6),
                     **{f"p_{n}": sum(p.numel() for p in getattr(blk, n).parameters())
                        for n in ("vmamba", "shape_branch", "directional_extractor", "gate", "fuse", "ffn")},
                     p_cv1_cv2=sum(p.numel() for p in l10.cv1.parameters()) + sum(p.numel() for p in l10.cv2.parameters()),
                     ss2d_d_inner=blk.vmamba.d_inner, ss2d_d_state=blk.vmamba.d_state, ss2d_dt_rank=blk.vmamba.dt_rank)
        else:
            r.update(hidden_c=l10.c, n_blocks=len(l10.m))
        arch.append(r)
    # Tensor nào của TSVM nhận được trọng số yolo26s-seg.pt khi gọi .load() (cùng tên + cùng kích thước,
    # đúng quy tắc intersect_dicts). yolo26s-seg.pt có kiến trúc yolo26-seg.yaml scale s, nc=80.
    cfg = yaml.safe_load((cfgdir / "yolo26-seg.yaml").read_text(encoding="utf-8"))
    cfg["scale"] = "s"
    src = SegmentationModel(cfg, nc=80, verbose=False).state_dict()
    cfg = yaml.safe_load((cfgdir / "yolo26-seg-TopologyShapeVMamba.yaml").read_text(encoding="utf-8"))
    cfg["scale"] = "s"
    dst_model = SegmentationModel(cfg, nc=1, verbose=False)
    dst = dst_model.state_dict()
    params = dict(dst_model.named_parameters())
    ok = [k for k, v in dst.items() if k in src and src[k].shape == v.shape]
    l10 = [k for k in params if k.startswith("model.10.")]
    l10_ok = [k for k in l10 if k in ok]
    arch[1].update(l10_param_tensors_pretrained=f"{len(l10_ok)}/{len(l10)}",
                   l10_params_pretrained=sum(params[k].numel() for k in l10_ok),
                   l10_pretrained_groups="|".join(sorted({".".join(k.split(".")[2:4]) for k in l10_ok})))
    ar = pd.DataFrame(arch)
    ar.T.to_csv(OUT / "08_kien_truc_dung_lai.csv", header=False, encoding="utf-8-sig")
    print(ar.T.to_string(header=False))
    # Chỉ gỡ liên kết tạm, không bao giờ xóa đệ quy (tránh chạm vào thư mục fork thật).
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "rmdir", str(link)], check=False, capture_output=True)
    else:
        link.unlink()
    os.rmdir(tmp)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--torch", action="store_true", help="kiểm tra best.pt và dựng lại mô hình (cần torch)")
    ap.add_argument("--seeds", type=int, default=20, help="số seed đầu tiên dùng (0..N-1); khác 20 thì ghi vào bang/<N>seed/")
    args = ap.parse_args()
    global SEEDS, OUT
    SEEDS = range(args.seeds)
    if args.seeds != 20:
        OUT = OUT / f"{args.seeds}seed"
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    OUT.mkdir(exist_ok=True)
    ds = dataset_audit()
    per = training_audit()
    if len(SEEDS) == 20:  # gói 04_phan_tich_20seed chỉ có thống kê cho đủ 20 seed
        compare_package(per)
    lineage_check()
    confusion_audit()
    if args.torch:
        torch_audit()
    (OUT / "00_kiem_tra_du_lieu.json").write_text(
        json.dumps({"trung_byte_train_val": ds["dup_train_val"], **{k: bool(v) for k, v in ds["checks"].items()}},
                   ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
