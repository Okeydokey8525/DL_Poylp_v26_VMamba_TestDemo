"""Phan tich 20 seed: Baseline (YOLOv26s-seg) vs TSVM FP32, xuat CSV + 9 hinh cho bao cao.

    python archive/Stracth/Bao_Cao/phan_tich_20seed_fp32.py

Doc results.csv cua seed 0..19 (epoch tot nhat = max Mask mAP50-95, giong ban 10 seed), doc ma tran nham lan
bang OCR tu confusion_matrix.png (giong _forensic_cm_all.py), roi ghi vao archive/Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/.
Thu muc dau ra phai chua ton tai hoac rong.
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]  # archive/
KQ = ROOT / "Ket_Qua_V2" / "KetQua_Nen"
OUT = ROOT / "Ket_Qua_V2" / "KQ_Nen_DX_20seed_FP32"
OLD_CM = ROOT / "Ket_Qua_V2" / "KQ_Nen_DX_10seed" / "01_raw_analysis" / "raw_10seeds_confusion_matrices.csv"
SEEDS = list(range(20))
N = len(SEEDS)
MODELS = {
    "Baseline": lambda s: KQ / "YOLOv26s-seg" / f"Kvasir_BG20_Baseline_YOLO26s_seg_s{s}_w2",
    "TSVM": lambda s: KQ / "Kvasir_BG20_YOLO26s_seg_TSVM_FP32" / f"Kvasir_BG20_YOLO26s_seg_TSVM_FP32_s{s}_w2",
}
LABEL = {"Baseline": "Baseline YOLO26s-seg", "TSVM": "TSVM (Topology-Shape)"}
COLOR = {"Baseline": "#1f77b4", "TSVM": "#ff7f0e"}
TEXT = {"Baseline": "#174a7c", "TSVM": "#b04a00"}
COLS = {
    "mask_map50_95": "metrics/mAP50-95(M)", "mask_map50": "metrics/mAP50(M)",
    "mask_precision": "metrics/precision(M)", "mask_recall": "metrics/recall(M)",
    "box_map50_95": "metrics/mAP50-95(B)", "box_map50": "metrics/mAP50(B)",
    "box_precision": "metrics/precision(B)", "box_recall": "metrics/recall(B)",
    "val_seg_loss": "val/seg_loss",
}

plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#333333"


def load():
    curves, rows = {m: [] for m in MODELS}, []
    for m, path in MODELS.items():
        for s in SEEDS:
            df = pd.read_csv(path(s) / "results.csv")
            df.columns = [c.strip() for c in df.columns]
            if len(df) != 100:
                raise ValueError(f"{m} s{s}: {len(df)} epochs")
            curves[m].append(df)
            best = df.loc[df[COLS["mask_map50_95"]].idxmax()]
            rows.append({"model": m, "seed": s, "best_epoch": int(best["epoch"]),
                         **{k: float(best[c]) for k, c in COLS.items()}, "run_path": str(path(s).relative_to(ROOT))})
    return curves, pd.DataFrame(rows)


def ocr_confusion():
    """Read TP/FP/FN/TN counts from Ultralytics confusion_matrix.png (same crop boxes as _forensic_cm_all.py)."""
    from PIL import Image
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()
    boxes = {"TP": (890, 404, 1330, 644), "FP": (1670, 404, 2110, 644),
             "FN": (890, 1182, 1330, 1422), "TN": (1670, 1182, 2110, 1422)}

    def cell(img, box):
        c = img.crop(box)
        c = c.resize((c.width * 4, c.height * 4), Image.LANCZOS)
        res, _ = ocr(np.asarray(c))
        for t in res or []:
            try:
                return int(round(float(t[1].replace(" ", "").replace(",", ".").replace("O", "0").replace("l", "1"))))
            except ValueError:
                continue
        return None

    rows = []
    for m, path in MODELS.items():
        for s in SEEDS:
            img = Image.open(path(s) / "confusion_matrix.png").convert("RGB")
            if img.size != (3000, 2250):
                raise ValueError(f"{m} s{s}: unexpected confusion_matrix.png size {img.size}")
            v = {k: cell(img, b) for k, b in boxes.items()}
            rows.append({"model": m, "seed": s, **v})
    return pd.DataFrame(rows)


def paired(df, key):
    b = df[df.model == "Baseline"].sort_values("seed")[key].to_numpy()
    t = df[df.model == "TSVM"].sort_values("seed")[key].to_numpy()
    return b, t


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if any(OUT.iterdir()):
        raise SystemExit(f"{OUT} is not empty")
    (OUT / "figures").mkdir()
    curves, df = load()
    df.to_csv(OUT / "raw_20seeds_extracted_metrics.csv", index=False)

    # ------------------------------------------------------------------ statistics
    summary = []
    for key in [*COLS, "best_epoch"]:
        b, t = paired(df, key)
        d = t - b
        tt = stats.ttest_rel(t, b)
        w = stats.wilcoxon(t, b) if np.any(d) else None
        lo, hi = stats.t.interval(0.95, N - 1, loc=d.mean(), scale=d.std(ddof=1) / np.sqrt(N))
        summary.append({"metric": key, "baseline_mean": b.mean(), "baseline_sd": b.std(ddof=1),
                        "tsvm_mean": t.mean(), "tsvm_sd": t.std(ddof=1), "delta": d.mean(),
                        "delta_ci95_low": lo, "delta_ci95_high": hi, "p_ttest": tt.pvalue,
                        "p_wilcoxon": None if w is None else w.pvalue,
                        "levene_p": stats.levene(b, t).pvalue,
                        "tsvm_wins": int((d > 0).sum()), "baseline_wins": int((d < 0).sum())})
    summ = pd.DataFrame(summary)
    summ.to_csv(OUT / "summary_20seeds_paired.csv", index=False)
    b, t = paired(df, "mask_map50_95")
    wins = int((t > b).sum())
    sign_p = stats.binomtest(wins, int((t != b).sum()), 0.5).pvalue

    # ------------------------------------------------------------------ confusion matrices (OCR)
    cm = ocr_confusion()
    if OLD_CM.exists():  # OCR self-check: Baseline seeds 0..9 must reproduce the verified 10-seed CSV
        old = pd.read_csv(OLD_CM)
        ref = old[old.model == "Baseline"].set_index("seed")[["TP", "FN", "FP"]]
        got = cm[(cm.model == "Baseline") & (cm.seed < 10)].set_index("seed")[["TP", "FN", "FP"]]
        cm_check = bool((ref.sort_index() == got.sort_index()).all().all())
    else:
        cm_check = None
    cm["TP+FN"] = cm["TP"] + cm["FN"]
    cm["TN_reconstructed"] = 40 - cm["FP"]
    cm.to_csv(OUT / "raw_20seeds_confusion_matrices.csv", index=False)

    # ------------------------------------------------------------------ envelope width
    def band(m):
        mat = np.array([c[COLS["mask_map50_95"]].to_numpy()[:100] for c in curves[m]])
        return mat.max(0) - mat.min(0)
    wb, wt = band("Baseline"), band("TSVM")

    facts = {"n_seeds": N, "sign_test_p_mask_map50_95": sign_p, "tsvm_wins_mask_map50_95": wins,
             "baseline_wins_mask_map50_95": int((b > t).sum()),
             "median_baseline": float(np.median(b)), "median_tsvm": float(np.median(t)),
             "min_baseline": float(b.min()), "min_baseline_seed": int(np.argmin(b)),
             "max_baseline": float(b.max()), "max_baseline_seed": int(np.argmax(b)),
             "min_tsvm": float(t.min()), "min_tsvm_seed": int(np.argmin(t)),
             "max_tsvm": float(t.max()), "max_tsvm_seed": int(np.argmax(t)),
             "band_narrower_epochs": int((wt < wb).sum()), "band_mean_width_change_pct": float((wt.mean() - wb.mean()) / wb.mean() * 100),
             "ocr_check_baseline_s0_9_matches_10seed_csv": cm_check,
             "cm_mean": {m: {k: [float(cm[cm.model == m][k].mean()), float(cm[cm.model == m][k].std(ddof=1))]
                             for k in ["TP", "FN", "FP", "TN_reconstructed"]} for m in MODELS},
             "cm_missing_cells": int(cm[["TP", "FN", "FP", "TN"]].isna().sum().sum())}
    (OUT / "facts.json").write_text(json.dumps(facts, indent=1, ensure_ascii=False), encoding="utf-8")

    figures(df, curves, summ, wins)
    print(summ[["metric", "baseline_mean", "baseline_sd", "tsvm_mean", "tsvm_sd", "delta", "p_ttest", "p_wilcoxon", "levene_p", "tsvm_wins"]].to_string())
    print(json.dumps(facts, indent=1, ensure_ascii=False))


def figures(df, curves, summ, wins):
    fd = OUT / "figures"
    S = summ.set_index("metric")
    seeds_lbl = f"{N} Seeds"

    # Hinh 1: 4 chi so phan doan
    fig = plt.figure(figsize=(10, 6.2), dpi=300)
    keys = ["mask_map50_95", "mask_map50", "mask_precision", "mask_recall"]
    names = ["Mask mAP@50-95", "Mask mAP@50", "Precision (Mask)", "Recall (Mask)"]
    x, w = np.arange(4), 0.32
    for i, m in enumerate(MODELS):
        pre = "baseline" if m == "Baseline" else "tsvm"
        vals = [S.loc[k, f"{pre}_mean"] for k in keys]
        errs = [S.loc[k, f"{pre}_sd"] for k in keys]
        bars = plt.bar(x + (i - 0.5) * w, vals, w, yerr=errs, capsize=6, label=LABEL[m], color=COLOR[m], edgecolor="black", alpha=0.88)
        for r, e in zip(bars, errs):
            plt.text(r.get_x() + r.get_width() / 2, r.get_height() + e + 0.003, f"{r.get_height():.4f}", ha="center", va="bottom",
                     fontsize=10, fontweight="bold", color=TEXT[m])
    plt.title(f"So Sánh Hiệu Năng Phân Đoạn {seeds_lbl} (Kvasir_YOLO_SEG_BG20)\nMean ± 1 Std (Baseline vs TSVM FP32)", fontsize=13, fontweight="bold", pad=12)
    plt.ylabel("Điểm số đo lường (Score)", fontsize=11, fontweight="bold")
    plt.ylim(0.70, 0.98)
    plt.xticks(x, names, fontsize=11, fontweight="bold")
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.legend(loc="upper right", fontsize=10)
    plt.tight_layout()
    plt.savefig(fd / "01_overall_benchmark_barchart.png")
    plt.close(fig)

    # Hinh 2: val seg loss
    fig = plt.figure(figsize=(6, 5), dpi=300)
    for i, m in enumerate(MODELS):
        pre = "baseline" if m == "Baseline" else "tsvm"
        mu, sd = S.loc["val_seg_loss", f"{pre}_mean"], S.loc["val_seg_loss", f"{pre}_sd"]
        plt.bar(i - 0.5, mu, 1.0, yerr=sd, capsize=8, label=m, color=["#406e9a", "#dc6f1e"][i], edgecolor="black", align="edge")
        plt.text(i, mu + sd + 0.01, f"{mu:.4f}\n±{sd:.4f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    plt.xticks([0.5], ["val/seg_loss"])
    plt.xlim(-0.6, 1.6)
    plt.ylim(1.0, max(S.loc["val_seg_loss", "baseline_mean"] + S.loc["val_seg_loss", "baseline_sd"], S.loc["val_seg_loss", "tsvm_mean"] + S.loc["val_seg_loss", "tsvm_sd"]) + 0.08)
    plt.title(f"Validation Segmentation Loss ({seeds_lbl} Mean ± Std)", fontsize=13)
    plt.ylabel("Validation Segmentation Loss (Lower is better)", fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(fd / "02_val_seg_loss_barchart.png")
    plt.close(fig)

    # Hinh 3: tung seed
    fig = plt.figure(figsize=(16, 6.5), dpi=300)
    x, w = np.arange(N), 0.38
    for i, m in enumerate(MODELS):
        v = df[df.model == m].sort_values("seed")["mask_map50_95"].to_numpy()
        bars = plt.bar(x + (i - 0.5) * w, v, w, label=LABEL[m], color=COLOR[m], edgecolor="black", alpha=0.88)
        for r in bars:
            plt.text(r.get_x() + r.get_width() / 2, r.get_height() + 0.001, f"{r.get_height():.4f}", ha="center", va="bottom",
                     fontsize=6.5, fontweight="bold", color=TEXT[m], rotation=90)
    lo = df["mask_map50_95"].min()
    plt.ylim(np.floor(lo * 100 - 1) / 100, 0.76)
    plt.title(f"Đối Chiếu Hiệu Năng Từng Cặp Seed Độc Lập (Seed 0 - Seed {N - 1})\nMask mAP@50-95 trên tập Kvasir_YOLO_SEG_BG20 (Baseline vs TSVM FP32)", fontsize=14, fontweight="bold", pad=12)
    plt.ylabel("Mask mAP@50-95", fontsize=12, fontweight="bold")
    plt.xticks(x, [f"Seed {s}" for s in SEEDS], fontsize=9.5, fontweight="bold", rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.legend(loc="lower right", fontsize=10)
    plt.tight_layout()
    plt.savefig(fd / "03_seed_by_seed_barchart.png")
    plt.close(fig)

    epochs = np.arange(1, 101)

    def mean_band(ax, col, m):
        mat = np.array([c[col].to_numpy()[:100] for c in curves[m]])
        mu, sd = mat.mean(0), mat.std(0)
        ax.plot(epochs, mu, label=LABEL[m], color=COLOR[m], linewidth=1.8)
        ax.fill_between(epochs, mu - sd, mu + sd, color=COLOR[m], alpha=0.15)

    # Hinh 4: loss curves
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
    for col, title, ax in [("val/seg_loss", "Validation Seg Loss", axes[0, 0]), ("train/seg_loss", "Training Seg Loss", axes[0, 1]),
                           ("val/box_loss", "Validation Box Loss", axes[1, 0]), ("val/cls_loss", "Validation Cls Loss", axes[1, 1])]:
        for m in MODELS:
            mean_band(ax, col, m)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Loss")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(fontsize=9, loc="upper right")
    plt.suptitle(f"Đường Cong Hội Tụ Các Hàm Mất Mát (Loss Convergence Curves)\nTrung Bình ± 1 Std qua {seeds_lbl} (100 Epochs)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(fd / "04_convergence_loss_curves.png")
    plt.close(fig)

    # Hinh 5: mAP curves
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    for col, title, ax in [("metrics/mAP50-95(M)", "Mask mAP@50-95 vs Epoch", axes[0]), ("metrics/mAP50(M)", "Mask mAP@50 vs Epoch", axes[1])]:
        for m in MODELS:
            mean_band(ax, col, m)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Epoch (1 -> 100)")
        ax.set_ylabel("Score")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(fontsize=9.5, loc="lower right")
    plt.suptitle(f"Động Thái Phát Triển Độ Chính Xác Phân Đoạn Theo Epoch ({seeds_lbl})", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(fd / "05_metric_curves_mAP.png")
    plt.close(fig)

    # Hinh 6: win rate donut
    fig = plt.figure(figsize=(7, 6), dpi=300)
    bw = N - wins - int((df[df.model == "TSVM"].sort_values("seed")["mask_map50_95"].to_numpy() == df[df.model == "Baseline"].sort_values("seed")["mask_map50_95"].to_numpy()).sum())
    _, _, autotexts = plt.pie([wins, bw], explode=(0.05, 0), labels=[f"TSVM Thắng ({wins}/{N} Seeds)", f"Baseline Thắng ({bw}/{N} Seeds)"],
                              colors=[COLOR["TSVM"], COLOR["Baseline"]], autopct="%1.1f%%", startangle=140, pctdistance=0.75,
                              wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2), textprops=dict(fontsize=11, fontweight="bold"))
    for a in autotexts:
        a.set_color("white")
        a.set_fontsize(12)
    plt.title(f"Tỷ Lệ Thắng Đối Đầu Trực Diện (Head-to-Head Win Rate)\nTheo Mask mAP@50-95 Qua {N} Seeds Độc Lập", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(fd / "07b_pie_head_to_head_winrate.png")
    plt.close(fig)

    # Hinh 7: stability envelope
    fig = plt.figure(figsize=(10, 5.8), dpi=300)
    for m in MODELS:
        mat = np.array([c["metrics/mAP50-95(M)"].to_numpy()[:100] for c in curves[m]])
        plt.fill_between(epochs, mat.min(0), mat.max(0), color=COLOR[m], alpha=0.22, label=f"Dải phân bổ {LABEL[m]} [Min, Max]")
        plt.plot(epochs, mat.mean(0), color=COLOR[m], linewidth=2.2, label=f"{LABEL[m]} (Mean)")
    plt.title(f"Biểu Đồ Miền Bao Phủ Độ Ổn Định (Stability Envelope Band)\nBiên Độ Dao Động Cực Đại - Cực Tiểu Giữa {seeds_lbl} (Baseline vs TSVM)", fontsize=13, fontweight="bold", pad=15)
    plt.xlabel("Epoch Huấn Luyện (1 -> 100)", fontsize=11, fontweight="bold")
    plt.ylabel("Mask mAP@50-95 Span", fontsize=11, fontweight="bold")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend(loc="lower right", fontsize=10)
    plt.tight_layout()
    plt.savefig(fd / "09_metric_stability_band_area.png")
    plt.close(fig)

    # Hinh 8: radar 8 truc Box + Mask
    axes_names = ["Mask mAP@50-95", "Mask mAP@50", "Mask Precision", "Mask Recall", "Box Recall", "Box Precision", "Box mAP@50", "Box mAP@50-95"]
    axes_keys = ["mask_map50_95", "mask_map50", "mask_precision", "mask_recall", "box_recall", "box_precision", "box_map50", "box_map50_95"]
    ang = np.linspace(0, 2 * np.pi, len(axes_keys), endpoint=False) + np.pi / len(axes_keys)
    ang = np.concatenate([ang, ang[:1]])
    fig, ax = plt.subplots(figsize=(8, 8.2), subplot_kw=dict(polar=True), dpi=300)
    for m in MODELS:
        pre = "baseline" if m == "Baseline" else "tsvm"
        v = [S.loc[k, f"{pre}_mean"] for k in axes_keys]
        v += v[:1]
        ax.plot(ang, v, linewidth=3, color=COLOR[m], label=LABEL[m])
        ax.fill(ang, v, color=COLOR[m], alpha=0.15)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(ang[:-1])
    ax.set_xticklabels(axes_names, fontsize=11, fontweight="bold")
    ax.set_ylim(0.65, 0.95)
    ax.set_yticks([0.70, 0.75, 0.80, 0.85, 0.90, 0.95])
    ax.tick_params(axis="y", labelsize=9, colors="#555555")
    ax.set_title(f"Đối Chiếu Đa Chiều Toàn Diện (Multi-Metric Radar Comparison)\nBox Detection (Bên Trái) vs Mask Segmentation (Bên Phải) qua {seeds_lbl}", fontsize=12.5, fontweight="bold", pad=28)
    fig.text(0.08, 0.5, "BOX METRICS\n(Phát Hiện)", ha="center", va="center", fontsize=11, fontweight="bold", color="#174a7c",
             bbox=dict(boxstyle="round", fc="#eef4fb", ec="#1f77b4"))
    fig.text(0.92, 0.5, "MASK METRICS\n(Phân Đoạn)", ha="center", va="center", fontsize=11, fontweight="bold", color="#b04a00",
             bbox=dict(boxstyle="round", fc="#fff3e6", ec="#ff7f0e"))
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=2, fontsize=10.5)
    plt.tight_layout()
    plt.savefig(fd / "10_radar_multiobjective_tradeoff.png", bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)

    # Hinh 9: boxplot
    fig, ax = plt.subplots(figsize=(8, 6.4), dpi=300)
    data = [df[df.model == m].sort_values("seed")["mask_map50_95"].to_numpy() for m in MODELS]
    bp = ax.boxplot(data, patch_artist=True, tick_labels=[LABEL[m] for m in MODELS], widths=0.45)
    for patch, m in zip(bp["boxes"], MODELS):
        patch.set_facecolor(COLOR[m])
        patch.set_alpha(0.75)
    for med in bp["medians"]:
        med.set(color="black", linewidth=2.2)
    rng = np.random.default_rng(0)
    for i, v in enumerate(data):
        ax.scatter(rng.normal(i + 1, 0.04, len(v)), v, color="#333333", alpha=0.8, s=36, edgecolor="white", zorder=3)
        ax.text(i + 1, 0.04, f"Mean: {v.mean():.4f} ± {v.std(ddof=1):.4f}\nMedian: {np.median(v):.4f}\nMin–Max: [{v.min():.4f}, {v.max():.4f}]",
                transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=10, fontweight="bold",
                bbox=dict(boxstyle="round", fc="#f7f8fa", ec="#cccccc"))
    lo = min(x.min() for x in data)
    ax.set_ylim(lo - 0.012, max(x.max() for x in data) + 0.008)
    ax.set_title(f"Phân Bổ Độ Chính Xác Mask mAP@50-95 Qua {seeds_lbl} Độc Lập\nKiểm Chứng Tính Ổn Định & Phương Sai (Baseline vs TSVM FP32)", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Mask mAP@50-95", fontsize=12, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(fd / "11_boxplot_variance_stability.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
