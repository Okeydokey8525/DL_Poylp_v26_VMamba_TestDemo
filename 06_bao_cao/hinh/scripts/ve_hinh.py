"""Vẽ bộ hình kết quả cho khóa luận (tiếng Việt) và bài báo IEEE (tiếng Anh).

Đọc trực tiếp các bảng trong 00_tai_lieu_tong_quan/bang/ (đã đối chiếu với results.csv gốc).
Mỗi hình xuất PNG 300 dpi và PDF vector vào <thư mục>/vi/ và <thư mục>/en/:
  - hình không phụ thuộc số seed (a, d, e02, e03, m01, q01) -> ../chung/
  - hình kết quả theo seed (h, r, c, e01, p)                -> ../ket_qua_<N>seed/, đọc bang/ (N = 20) hoặc bang/<N>seed/

    python ve_hinh.py                  # vẽ tất cả, kết quả dùng 20 seed (seed 0–19, bộ dùng trong báo cáo)
    python ve_hinh.py --seeds 10       # kết quả dùng 10 seed (chỉ đối chiếu)
    python ve_hinh.py --chi h01 h03    # chỉ vẽ một số hình
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
REPO = OUT.parents[1]
BANG = REPO / "00_tai_lieu_tong_quan" / "bang"
BANG_SEED = BANG              # bảng cho các hình kết quả; main() đặt lại theo --seeds
N_SEED = 20
DICH = OUT / "chung"          # thư mục ghi của hình đang vẽ; main() đặt lại cho từng hình

# Bảng màu Okabe–Ito (Wong, Nature Methods 2011), an toàn cho người mù màu.
C_BASE = "#0072B2"   # xanh dương
C_TSVM = "#D55E00"   # cam đỏ
C_UP = "#009E73"     # xanh lá: TSVM tốt hơn
C_DOWN = "#999999"   # xám: TSVM kém hơn
C_GRID = "#D9D9D9"

CM = 1 / 2.54
# Bản tiếng Việt cho khóa luận: rộng 16 cm, chữ 10 pt.
# Bản tiếng Anh cho IEEE hai cột: một cột 8,9 cm (3,5 in), chữ 8 pt.
STYLE = {
    "vi": {"width": 16.0 * CM, "font": 10, "lang": "vi"},
    "en": {"width": 8.9 * CM, "font": 8, "lang": "en"},
}

T = {  # nhãn hai ngôn ngữ
    "baseline": {"vi": "YOLO26s-seg (đối chứng)", "en": "YOLO26s-seg"},
    "tsvm": {"vi": "YOLO26s-seg + TSVM (đề xuất)", "en": "YOLO26s-seg + TSVM"},
    "baseline_short": {"vi": "Đối chứng", "en": "Baseline"},
    "tsvm_short": {"vi": "TSVM", "en": "TSVM"},
    "score": {"vi": "Giá trị chỉ số", "en": "Score"},
    "seed": {"vi": "Seed", "en": "Seed"},
    "epoch": {"vi": "Epoch", "en": "Epoch"},
    "mask_map": {"vi": "Mask mAP@50–95", "en": "Mask mAP@50–95"},
    "close_mosaic": {"vi": "tắt mosaic", "en": "mosaic off"},
    "pred": {"vi": "Dự đoán", "en": "Predicted"},
    "true": {"vi": "Thực tế", "en": "Ground truth"},
    "polyp": {"vi": "polyp", "en": "polyp"},
    "background": {"vi": "nền", "en": "background"},
    "na": {"vi": "không xác định", "en": "undefined"},
}
METRIC_LABEL = {
    "mask_map50_95": {"vi": "mAP@50–95", "en": "mAP50–95"},
    "mask_map50": {"vi": "mAP@50", "en": "mAP50"},
    "mask_precision": {"vi": "Precision", "en": "Precision"},
    "mask_recall": {"vi": "Recall", "en": "Recall"},
    "mask_f1": {"vi": "F1", "en": "F1"},
}


def setup(style: dict) -> None:
    plt.rcParams.update({
        "font.size": style["font"],
        "axes.titlesize": style["font"],
        "axes.labelsize": style["font"],
        "xtick.labelsize": style["font"] - 1,
        "ytick.labelsize": style["font"] - 1,
        "legend.fontsize": style["font"] - 1,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "lines.linewidth": 1.2,
        "legend.frameon": False,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,   # nhúng TrueType để tạp chí đọc được chữ
        "ps.fonttype": 42,
    })


def num(v: float, nd: int, lang: str) -> str:
    """Định dạng số: tiếng Việt dùng dấu phẩy thập phân, tiếng Anh dùng dấu chấm."""
    s = f"{v:.{nd}f}"
    return s.replace(".", ",") if lang == "vi" else s


def num_axis(ax, which: str, nd: int, lang: str) -> None:
    from matplotlib.ticker import FuncFormatter
    f = FuncFormatter(lambda v, _p: num(v, nd, lang))
    (ax.yaxis if which == "y" else ax.xaxis).set_major_formatter(f)


def save(fig, name: str, lang: str) -> None:
    d = DICH / lang
    d.mkdir(parents=True, exist_ok=True)
    fig.savefig(d / f"{name}.png")
    fig.savefig(d / f"{name}.pdf")
    plt.close(fig)


def load_seeds() -> pd.DataFrame:
    df = pd.read_csv(BANG_SEED / "02_ket_qua_tung_seed.csv", encoding="utf-8-sig")
    p, r = df["mask_precision"], df["mask_recall"]
    df["mask_f1"] = 2 * p * r / (p + r)   # F1 tính lại từ P và R của cùng dòng epoch
    return df


# --------------------------------------------------------------------------- hình
def h01_cot_kep_chi_so_mask(lang: str, st: dict) -> None:
    """Cột kép mean ± SD (N_SEED seed) cho các chỉ số mặt nạ. Điểm từng seed vẽ riêng ở h01b."""
    df = load_seeds()
    metrics = ["mask_map50_95", "mask_map50", "mask_precision", "mask_recall", "mask_f1"]
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.55))
    x = np.arange(len(metrics))
    w = 0.36
    for k, (model, color, key) in enumerate([("Baseline", C_BASE, "baseline"), ("TSVM_FP32", C_TSVM, "tsvm")]):
        g = df[df.model == model]
        mean = g[metrics].mean().to_numpy()
        sd = g[metrics].std(ddof=1).to_numpy()
        pos = x + (k - 0.5) * w
        ax.bar(pos, mean, w * 0.92, color=color, alpha=0.85, label=T[key][lang], zorder=2)
        ax.errorbar(pos, mean, yerr=sd, fmt="none", ecolor="black", elinewidth=0.8, capsize=2.5, zorder=4)
    ax.set_xticks(x, [METRIC_LABEL[m][lang] for m in metrics])
    ax.set_ylabel(T["score"][lang])
    ax.set_ylim(0, 1.0)
    num_axis(ax, "y", 1, lang)
    ax.yaxis.grid(True, color=C_GRID, linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, handlelength=1.2, columnspacing=1.2)
    save(fig, "h01_cot_kep_chi_so_mask", lang)


def h01b_diem_tung_seed_chi_so_mask(lang: str, st: dict) -> None:
    """Điểm của từng seed (N_SEED seed/mô hình) cho các chỉ số mặt nạ; vạch đen là trung bình."""
    df = load_seeds()
    metrics = ["mask_map50_95", "mask_map50", "mask_precision", "mask_recall", "mask_f1"]
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.55))
    x = np.arange(len(metrics))
    w = 0.36
    rng = np.random.default_rng(0)
    for k, (model, color, key) in enumerate([("Baseline", C_BASE, "baseline"), ("TSVM_FP32", C_TSVM, "tsvm")]):
        g = df[df.model == model]
        pos = x + (k - 0.5) * w
        for i, m in enumerate(metrics):
            jit = rng.uniform(-w * 0.30, w * 0.30, len(g))
            ax.scatter(pos[i] + jit, g[m], s=10 if lang == "vi" else 6, color=color, alpha=0.75,
                       edgecolors="white", linewidths=0.3, zorder=3, label=T[key][lang] if i == 0 else None)
            ax.hlines(g[m].mean(), pos[i] - w * 0.40, pos[i] + w * 0.40, color="black", linewidth=1.2, zorder=4)
    ax.set_xticks(x, [METRIC_LABEL[m][lang] for m in metrics])
    for xi in x[:-1] + 0.5:
        ax.axvline(xi, color=C_GRID, linewidth=0.5, zorder=0)
    ax.set_ylabel(T["score"][lang])
    num_axis(ax, "y", 2, lang)
    ax.yaxis.grid(True, color=C_GRID, linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)
    from matplotlib.lines import Line2D
    handles, labels = ax.get_legend_handles_labels()
    handles.append(Line2D([], [], color="black", lw=1.2))
    labels.append({"vi": f"Trung bình {N_SEED} seed", "en": f"Mean of {N_SEED} seeds"}[lang])
    ax.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3,
              handlelength=1.2, columnspacing=1.0)
    save(fig, "h01b_diem_tung_seed_chi_so_mask", lang)


def h02_ghep_cap_tung_seed(lang: str, st: dict) -> None:
    """Biểu đồ nối cặp: mask mAP@50–95 của hai mô hình tại cùng seed."""
    df = load_seeds()
    b = df[df.model == "Baseline"].set_index("seed")["mask_map50_95"]
    t = df[df.model == "TSVM_FP32"].set_index("seed")["mask_map50_95"]
    fig, ax = plt.subplots(figsize=(st["width"] * (0.62 if lang == "vi" else 1.0), st["width"] * 0.62))
    for s in b.index:
        up = t[s] > b[s]
        ax.plot([0, 1], [b[s], t[s]], color=C_UP if up else C_DOWN, linewidth=0.7, alpha=0.9, zorder=1)
    ax.scatter(np.zeros(len(b)), b, s=12, color=C_BASE, zorder=2)
    ax.scatter(np.ones(len(t)), t, s=12, color=C_TSVM, zorder=2)
    for xpos, ser, color in [(0, b, C_BASE), (1, t, C_TSVM)]:
        ax.errorbar(xpos + (-0.12 if xpos == 0 else 0.12), ser.mean(), yerr=ser.std(ddof=1), fmt="o", color=color,
                    markersize=4, elinewidth=1, capsize=2.5, zorder=3)
    ax.set_xticks([0, 1], [T["baseline_short"][lang], T["tsvm_short"][lang]])
    ax.set_xlim(-0.35, 1.35)
    ax.set_ylabel(T["mask_map"][lang])
    num_axis(ax, "y", 2, lang)
    ax.yaxis.grid(True, color=C_GRID, linewidth=0.5)
    ax.set_axisbelow(True)
    from matplotlib.lines import Line2D
    n_up = int((t > b).sum())
    n = len(b)
    lab_up = {"vi": f"TSVM cao hơn ({n_up}/{n})", "en": f"TSVM higher ({n_up}/{n})"}[lang]
    lab_dn = {"vi": f"TSVM thấp hơn ({n - n_up}/{n})", "en": f"TSVM lower ({n - n_up}/{n})"}[lang]
    ax.legend(handles=[Line2D([], [], color=C_UP, lw=1, label=lab_up), Line2D([], [], color=C_DOWN, lw=1, label=lab_dn)],
              loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=1)
    save(fig, "h02_ghep_cap_tung_seed", lang)


def h03_duong_mien_mask_map_theo_epoch(lang: str, st: dict) -> None:
    """Đường trung bình và miền ±1 SD (N_SEED seed) của mask mAP@50–95 theo epoch."""
    cv = pd.read_csv(BANG_SEED / "05_duong_cong_theo_epoch.csv", encoding="utf-8-sig")
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.55))
    for model, color, key in [("Baseline", C_BASE, "baseline"), ("TSVM_FP32", C_TSVM, "tsvm")]:
        g = cv[cv.model == model]
        ax.plot(g.epoch, g.mask_map_mean, color=color, label=T[key][lang], zorder=3)
        ax.fill_between(g.epoch, g.mask_map_mean - g.mask_map_sd, g.mask_map_mean + g.mask_map_sd,
                        color=color, alpha=0.18, linewidth=0, zorder=2)
    ax.plot([90.5, 90.5], [0.55, 0.78], color="black", linestyle=":", linewidth=0.7)
    ax.text(89.5, 0.555, T["close_mosaic"][lang], ha="right", va="bottom", fontsize=st["font"] - 2)
    ax.set_xlim(1, 100)
    ax.set_ylim(0.15, 0.78)
    ax.set_xlabel(T["epoch"][lang])
    ax.set_ylabel(T["mask_map"][lang])
    num_axis(ax, "y", 1, lang)
    ax.yaxis.grid(True, color=C_GRID, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, handlelength=1.4, columnspacing=1.2)
    # Phóng to giai đoạn cuối (epoch 70–100), đặt ở vùng trống dưới đường cong
    ins = ax.inset_axes([0.50, 0.08, 0.46, 0.42])
    ins.set_zorder(5)
    ins.patch.set_facecolor("white")
    for model, color in [("Baseline", C_BASE), ("TSVM_FP32", C_TSVM)]:
        g = cv[(cv.model == model) & (cv.epoch >= 70)]
        ins.plot(g.epoch, g.mask_map_mean, color=color, linewidth=1)
        ins.fill_between(g.epoch, g.mask_map_mean - g.mask_map_sd, g.mask_map_mean + g.mask_map_sd,
                         color=color, alpha=0.18, linewidth=0)
    ins.set_xlim(70, 100)
    ins.axvline(90.5, color="black", linestyle=":", linewidth=0.6)
    num_axis(ins, "y", 2, lang)
    ins.tick_params(labelsize=st["font"] - 3, length=2)
    for s in ("top", "right"):
        ins.spines[s].set_visible(True)
    save(fig, "h03_duong_mien_mask_map_theo_epoch", lang)


def h04_ma_tran_nham_lan(lang: str, st: dict) -> None:
    """Ma trận nhầm lẫn trung bình N_SEED seed (đơn vị: đối tượng), hai mô hình cạnh nhau."""
    cm = pd.read_csv(BANG_SEED / "06_ma_tran_nham_lan_tung_seed.csv", encoding="utf-8-sig")
    # Giá trị đã in trong ô nên không cần thanh màu; hai ô dùng chung trục dự đoán.
    fig, axes = plt.subplots(1, 2, figsize=(st["width"], st["width"] * 0.50), sharey=True,
                             gridspec_kw={"wspace": 0.08})
    vmax = 127
    big, small = st["font"] + 1, st["font"] - 2
    for i, (ax, (model, key)) in enumerate(zip(axes, [("Baseline", "baseline_short"), ("TSVM_FP32", "tsvm_short")])):
        g = cm[cm.model == model]
        m, s = g[["TP", "FP", "FN"]].mean(), g[["TP", "FP", "FN"]].std(ddof=1)
        # Hàng = dự đoán, cột = thực tế (cùng quy ước với Ultralytics)
        grid = np.array([[m.TP, m.FP], [m.FN, np.nan]])
        ax.imshow(grid, cmap="Blues", vmin=0, vmax=vmax)
        ax.add_patch(plt.Rectangle((0.5, 0.5), 1, 1, color="#EEEEEE", zorder=2))
        cells = {(0, 0): ("TP", m.TP, s.TP), (0, 1): ("FP", m.FP, s.FP), (1, 0): ("FN", m.FN, s.FN)}
        for (r, c), (lab, mu, sd) in cells.items():
            col = "white" if mu > vmax * 0.55 else "black"
            ax.text(c, r - 0.10, num(mu, 2, lang), ha="center", va="center", color=col, fontsize=big, weight="bold")
            ax.text(c, r + 0.22, f"{lab} ± {num(sd, 2, lang)}", ha="center", va="center", color=col, fontsize=small)
        ax.text(1, 1, T["na"][lang], ha="center", va="center", fontsize=small, color="#555555", zorder=3)
        ax.set_xticks([0, 1], [T["polyp"][lang], T["background"][lang]])
        ax.set_yticks([0, 1], [T["polyp"][lang], T["background"][lang]], rotation=90, va="center")
        ax.set_xlabel(T["true"][lang])
        if i == 0:
            ax.set_ylabel(T["pred"][lang])
        ax.set_title(T[key][lang])
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.tick_params(length=0)
    save(fig, "h04_ma_tran_nham_lan", lang)


# =========================================================================== bộ hình đầy đủ
C_PRANET = "#009E73"   # xanh lá (Okabe–Ito)
C_UNET = "#CC79A7"     # tím đỏ (Okabe–Ito)
EFF = REPO / "04_phan_tich_20seed" / "efficiency_benchmark" / "tables" / "efficiency_summary.csv"
DATASET = REPO / "01_du_lieu" / "Kvasir_YOLO_SEG_BG20"
MODELS2 = [("Baseline", C_BASE, "baseline"), ("TSVM_FP32", C_TSVM, "tsvm")]
PIX_MODELS = [("baseline", C_BASE, {"vi": "YOLO26s-seg", "en": "YOLO26s-seg"}),
              ("tsvm", C_TSVM, {"vi": "YOLO26s-seg + TSVM", "en": "YOLO26s-seg + TSVM"}),
              ("pranet", C_PRANET, {"vi": "PraNet (ResNet-50)", "en": "PraNet (ResNet-50)"}),
              ("unet", C_UNET, {"vi": "U-Net", "en": "U-Net"})]


def L(vi: str, en: str, lang: str) -> str:
    return vi if lang == "vi" else en


def grid_y(ax):
    ax.yaxis.grid(True, color=C_GRID, linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)


def legend_top(ax, ncol=2, handles=None, labels=None):
    kw = dict(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=ncol, handlelength=1.2, columnspacing=1.0)
    if handles is not None:
        ax.legend(handles, labels, **kw)
    else:
        ax.legend(**kw)


def dataset_stats():
    """Đọc trực tiếp nhãn YOLO của BG20: số polyp/ảnh, số đỉnh, diện tích tương đối (công thức shoelace)."""
    rows = []
    for split in ("train", "val"):
        for p in sorted((DATASET / "labels" / split).glob("*.txt")):
            lines = [l for l in p.read_text().splitlines() if l.strip()]
            bg = p.stem.startswith("bg_")
            rows.append({"split": split, "bg": bg, "n_obj": len(lines), "kind": "img"})
            for l in lines:
                c = np.array(l.split()[1:], float).reshape(-1, 2)
                x, y = c[:, 0], c[:, 1]
                area = 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
                rows.append({"split": split, "bg": bg, "n_pts": len(c), "area": area, "kind": "obj"})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- Chương 4: dữ liệu
def d01_thanh_phan_bg20(lang, st):
    """Cột chồng: số ảnh polyp và ảnh nền trong tập train và validation."""
    df = dataset_stats()
    img = df[df.kind == "img"]
    fig, ax = plt.subplots(figsize=(st["width"] * (0.6 if lang == "vi" else 1.0), st["width"] * 0.5))
    splits = ["train", "val"]
    pol = [int(((img.split == s) & ~img.bg).sum()) for s in splits]
    bg = [int(((img.split == s) & img.bg).sum()) for s in splits]
    x = np.arange(2)
    ax.bar(x, pol, 0.55, color=C_BASE, label=L("Ảnh có polyp", "Polyp images", lang), zorder=2)
    ax.bar(x, bg, 0.55, bottom=pol, color=C_DOWN, label=L("Ảnh nền (normal-cecum)", "Background (normal-cecum)", lang), zorder=2)
    th = (lambda v: f"{v:,}".replace(",", ".")) if lang == "vi" else (lambda v: f"{v:,}")
    for i in range(2):
        ax.text(x[i], pol[i] / 2, th(pol[i]), ha="center", va="center", color="white", fontsize=st["font"])
        if bg[i] > 100:
            ax.text(x[i], pol[i] + bg[i] / 2, th(bg[i]), ha="center", va="center", color="black", fontsize=st["font"])
        else:   # đoạn quá mỏng: ghi số bên phải cột
            ax.text(x[i] + 0.31, pol[i] + bg[i] / 2, th(bg[i]), ha="left", va="center", color="black", fontsize=st["font"])
        ax.text(x[i], pol[i] + bg[i] + 15, th(pol[i] + bg[i]), ha="center", va="bottom", fontsize=st["font"], weight="bold")
    ax.set_xticks(x, [L("Huấn luyện", "Train", lang), L("Kiểm định", "Validation", lang)])
    ax.set_ylabel(L("Số ảnh", "Images", lang))
    ax.set_ylim(0, 1200)
    grid_y(ax)
    legend_top(ax, ncol=1)
    save(fig, "d01_thanh_phan_bg20", lang)


def d02_so_polyp_moi_anh(lang, st):
    """Cột kép: phân bố số polyp trên mỗi ảnh có polyp (train và validation)."""
    df = dataset_stats()
    img = df[(df.kind == "img") & ~df.bg]
    fig, ax = plt.subplots(figsize=(st["width"] * (0.7 if lang == "vi" else 1.0), st["width"] * 0.5))
    ks = sorted(img.n_obj.unique().astype(int))
    x = np.arange(len(ks))
    w = 0.38
    for k, (split, color, lab) in enumerate([("train", C_BASE, L("Huấn luyện", "Train", lang)),
                                             ("val", C_TSVM, L("Kiểm định", "Validation", lang))]):
        g = img[img.split == split]
        frac = [100 * (g.n_obj == v).mean() for v in ks]
        bars = ax.bar(x + (k - 0.5) * w, frac, w * 0.92, color=color, label=f"{lab} (n = {len(g)})", zorder=2)
        for b, v in zip(bars, [(g.n_obj == v).sum() for v in ks]):
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1, str(int(v)), ha="center", va="bottom",
                    fontsize=st["font"] - 2)
    ax.set_xticks(x, [str(v) for v in ks])
    ax.set_xlabel(L("Số polyp trong một ảnh", "Polyps per image", lang))
    ax.set_ylabel(L("Tỉ lệ ảnh (%)", "Images (%)", lang))
    ax.set_ylim(0, 105)
    grid_y(ax)
    legend_top(ax)
    save(fig, "d02_so_polyp_moi_anh", lang)


def d03_so_dinh_polygon(lang, st):
    """Histogram số đỉnh của polygon nhãn (toàn bộ 1.063 đối tượng)."""
    df = dataset_stats()
    o = df[df.kind == "obj"]
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.45))
    bins = np.arange(o.n_pts.min() - 0.5, o.n_pts.max() + 1.5, 2)
    ax.hist(o.n_pts, bins=bins, color=C_BASE, edgecolor="white", linewidth=0.4, zorder=2)
    med = o.n_pts.median()
    ax.axvline(med, color="black", linestyle="--", linewidth=0.8)
    ax.text(med + 1, ax.get_ylim()[1] * 0.92, L(f"trung vị = {med:.0f}", f"median = {med:.0f}", lang), fontsize=st["font"] - 1)
    ax.set_xlabel(L("Số đỉnh của polygon", "Polygon vertices", lang))
    ax.set_ylabel(L("Số đối tượng", "Objects", lang))
    grid_y(ax)
    save(fig, "d03_so_dinh_polygon", lang)


def d04_dien_tich_polyp(lang, st):
    """Histogram diện tích polyp tương đối so với ảnh (%), trục log."""
    df = dataset_stats()
    o = df[df.kind == "obj"]
    a = 100 * o.area
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.45))
    bins = np.logspace(np.log10(max(a.min(), 0.01)), np.log10(a.max()), 30)
    ax.hist(a, bins=bins, color=C_BASE, edgecolor="white", linewidth=0.4, zorder=2)
    ax.set_xscale("log")
    from matplotlib.ticker import FuncFormatter
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _p: num(v, 0 if v >= 1 else (1 if v >= 0.1 else 2), lang)))
    med = a.median()
    ax.axvline(med, color="black", linestyle="--", linewidth=0.8)
    ax.text(med / 1.08, ax.get_ylim()[1] * 0.95, L(f"trung vị = {num(med, 1, lang)}%", f"median = {med:.1f}%", lang),
            ha="right", va="top", fontsize=st["font"] - 1)
    ax.set_xlabel(L("Diện tích polyp so với ảnh (%, thang log)", "Polyp area relative to image (%, log scale)", lang))
    ax.set_ylabel(L("Số đối tượng", "Objects", lang))
    grid_y(ax)
    save(fig, "d04_dien_tich_polyp", lang)


# ---------------------------------------------------------------- Chương 3: mô hình
def m01_tham_so_tang10(lang, st):
    """Thanh ngang: số tham số của từng thành phần trong tầng 10 (C2TSVMamba) so với C2PSA."""
    a = pd.read_csv(BANG / "08_kien_truc_dung_lai.csv", header=None, index_col=0, encoding="utf-8-sig")
    t = a[2]
    parts = [("p_cv1_cv2", L("cv1 + cv2 (khung C2)", "cv1 + cv2 (C2 wrapper)", lang)),
             ("p_directional_extractor", "DirectionalShapeExtractor"),
             ("p_vmamba", L("SS2D (VMamba)", "SS2D (VMamba)", lang)),
             ("p_ffn", "FFN"),
             ("p_shape_branch", "ShapeAwareBranch"),
             ("p_fuse", L("fuse 1×1", "fuse 1×1", lang)),
             ("p_gate", L("Cổng (Gate)", "Gate", lang))]
    vals = [float(t[k]) / 1e3 for k, _ in parts]
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.5))
    y = np.arange(len(parts))[::-1]
    ax.barh(y, vals, 0.6, color=C_TSVM, zorder=2)
    for yi, v in zip(y, vals):
        ax.text(v + 8, yi, num(v, 1, lang), va="center", fontsize=st["font"] - 1)
    c2psa = float(a.loc["layer10_params", 1]) / 1e3
    total = float(t["layer10_params"]) / 1e3
    ax.set_yticks(y, [lab for _, lab in parts])
    ax.set_xlabel(L("Số tham số (nghìn)", "Parameters (thousands)", lang))
    ax.set_xlim(0, max(vals) * 1.22)
    ax.xaxis.grid(True, color=C_GRID, linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.set_title(L(f"Tổng C2TSVMamba: {num(total, 1, lang)} nghìn  |  C2PSA (đối chứng): {num(c2psa, 1, lang)} nghìn",
                   f"C2TSVMamba total: {total:.1f}k  |  C2PSA (baseline): {c2psa:.1f}k", lang),
                 fontsize=st["font"] - 1)
    save(fig, "m01_tham_so_tang10", lang)


# ---------------------------------------------------------------- Chương 6: độ chính xác
def r01_delta_tung_seed(lang, st):
    """Thanh: Δ mask mAP@50–95 (TSVM − đối chứng) từng seed, sắp xếp."""
    df = load_seeds()
    b = df[df.model == "Baseline"].set_index("seed")["mask_map50_95"]
    t = df[df.model == "TSVM_FP32"].set_index("seed")["mask_map50_95"]
    d = (t - b).sort_values()
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.45))
    x = np.arange(len(d))
    ax.bar(x, d.values * 100, 0.75, color=[C_UP if v > 0 else C_DOWN for v in d.values], zorder=2)
    ax.axhline(0, color="black", linewidth=0.7)
    ax.axhline(d.mean() * 100, color=C_TSVM, linestyle="--", linewidth=0.9)
    sg = "+" if d.mean() >= 0 else ""
    ax.text(-0.4, d.mean() * 100 + 0.08, L(f"trung bình = {sg}{num(d.mean() * 100, 2, lang)}", f"mean = {sg}{d.mean() * 100:.2f}", lang),
            va="bottom", ha="left", fontsize=st["font"] - 1, color=C_TSVM)
    ax.set_xticks(x, [str(s) for s in d.index], fontsize=st["font"] - 2)
    ax.set_xlabel(L("Seed (sắp xếp theo Δ)", "Seed (sorted by Δ)", lang))
    ax.set_ylabel(L("Δ mask mAP@50–95 (điểm %)", "Δ mask mAP50–95 (pp)", lang))
    num_axis(ax, "y", 1, lang)
    grid_y(ax)
    save(fig, "r01_delta_tung_seed", lang)


def r02_hop_phan_bo(lang, st):
    """Hộp: phân bố mask mAP@50–95 của N_SEED seed cho mỗi mô hình."""
    df = load_seeds()
    data = [df[df.model == m]["mask_map50_95"].values for m, _, _ in MODELS2]
    fig, ax = plt.subplots(figsize=(st["width"] * (0.55 if lang == "vi" else 1.0), st["width"] * 0.6))
    bp = ax.boxplot(data, widths=0.5, patch_artist=True, showmeans=True,
                    meanprops=dict(marker="D", markerfacecolor="white", markeredgecolor="black", markersize=4),
                    medianprops=dict(color="black", linewidth=1), flierprops=dict(marker="o", markersize=3))
    for patch, (_, c, _) in zip(bp["boxes"], MODELS2):
        patch.set_facecolor(c)
        patch.set_alpha(0.75)
    ax.set_xticks([1, 2], [T["baseline_short"][lang], T["tsvm_short"][lang]])
    ax.set_ylabel(T["mask_map"][lang])
    num_axis(ax, "y", 3, lang)
    grid_y(ax)
    from matplotlib.lines import Line2D
    legend_top(ax, ncol=2, handles=[Line2D([], [], color="black", lw=1),
                                    Line2D([], [], marker="D", color="white", markeredgecolor="black", lw=0)],
               labels=[L("trung vị", "median", lang), L("trung bình", "mean", lang)])
    save(fig, "r02_hop_phan_bo", lang)


def r03_histogram_delta(lang, st):
    """Histogram của N_SEED hiệu số ghép cặp Δ (TSVM − đối chứng)."""
    df = load_seeds()
    b = df[df.model == "Baseline"].set_index("seed")["mask_map50_95"]
    t = df[df.model == "TSVM_FP32"].set_index("seed")["mask_map50_95"]
    d = (t - b) * 100
    fig, ax = plt.subplots(figsize=(st["width"] * (0.7 if lang == "vi" else 1.0), st["width"] * 0.5))
    ax.hist(d, bins=np.arange(min(-1.5, np.floor(d.min() * 2) / 2), max(3.0, np.ceil(d.max() * 2) / 2) + 0.01, 0.5), color=C_TSVM, alpha=0.85, edgecolor="white", zorder=2)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.axvline(d.mean(), color="black", linestyle="--", linewidth=0.8)
    ax.set_ylim(0, ax.get_ylim()[1] * 1.15)
    ax.text(d.mean() + 0.05, ax.get_ylim()[1] * 0.97, L(f"trung bình = {num(d.mean(), 2, lang)}", f"mean = {d.mean():.2f}", lang),
            va="top", fontsize=st["font"] - 1, bbox=dict(facecolor="white", edgecolor="none", pad=1))
    ax.set_xlabel(L("Δ mask mAP@50–95 (điểm %)", "Δ mask mAP50–95 (pp)", lang))
    ax.set_ylabel(L("Số seed", "Seeds", lang))
    from matplotlib.ticker import MaxNLocator
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))   # số seed là số nguyên
    num_axis(ax, "x", 1, lang)
    grid_y(ax)
    save(fig, "r03_histogram_delta", lang)


def r04_do_nhay_quy_tac_epoch(lang, st):
    """Điểm mean ± SD (N_SEED seed) của mask mAP@50–95 theo ba quy tắc chọn epoch, kèm p ghép cặp."""
    s = pd.read_csv(BANG_SEED / "04b_do_nhay_quy_tac_epoch.csv", encoding="utf-8-sig")
    labels = [L("Cực đại mask mAP\n(endpoint chính)", "Max mask mAP\n(primary)", lang),
              L("Fitness box+mask\n(best.pt)", "Box+mask fitness\n(best.pt)", lang),
              L("Epoch 100", "Epoch 100", lang)]
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.5))
    x = np.arange(3)
    for k, (col, c, key) in enumerate([("baseline", C_BASE, "baseline"), ("tsvm", C_TSVM, "tsvm")]):
        ax.errorbar(x + (k - 0.5) * 0.22, s[f"{col}_mean"], yerr=s[f"{col}_sd"], fmt="o", color=c, markersize=5,
                    elinewidth=1, capsize=3, label=T[key][lang], zorder=3)
    for i, r in s.iterrows():
        top = max(r.baseline_mean + r.baseline_sd, r.tsvm_mean + r.tsvm_sd)
        ax.text(x[i], top + 0.002, f"p = {num(r.paired_t_p, 3, lang)}", ha="center", fontsize=st["font"] - 2)
    ax.set_xticks(x, labels)
    ax.set_xlim(-0.5, 2.5)
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + (hi - lo) * 0.12)
    ax.set_ylabel(T["mask_map"][lang])
    num_axis(ax, "y", 3, lang)
    grid_y(ax)
    legend_top(ax)
    save(fig, "r04_do_nhay_quy_tac_epoch", lang)


def r05_precision_recall(lang, st):
    """Tán xạ: Mask Precision và Recall của từng seed."""
    df = load_seeds()
    fig, ax = plt.subplots(figsize=(st["width"] * (0.62 if lang == "vi" else 1.0), st["width"] * 0.62))
    for m, c, key in MODELS2:
        g = df[df.model == m]
        ax.scatter(g.mask_recall, g.mask_precision, s=14, color=c, alpha=0.8, edgecolors="white", linewidths=0.3,
                   label=T[key][lang], zorder=3)
        ax.errorbar(g.mask_recall.mean(), g.mask_precision.mean(), xerr=g.mask_recall.std(ddof=1),
                    yerr=g.mask_precision.std(ddof=1), fmt="D", color=c, markeredgecolor="black", markersize=5,
                    elinewidth=0.9, capsize=2, zorder=4)
    ax.set_xlabel("Mask Recall")
    ax.set_ylabel("Mask Precision")
    num_axis(ax, "x", 2, lang)
    num_axis(ax, "y", 2, lang)
    ax.grid(True, color=C_GRID, linewidth=0.5)
    ax.set_axisbelow(True)
    legend_top(ax, ncol=1)
    save(fig, "r05_precision_recall", lang)


# ---------------------------------------------------------------- Chương 6: hội tụ
def c01_val_seg_loss(lang, st):
    """Đường và miền ±1 SD: val segmentation loss theo epoch (bỏ 2 epoch đầu để thang đo đọc được)."""
    cv = pd.read_csv(BANG_SEED / "05_duong_cong_theo_epoch.csv", encoding="utf-8-sig")
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.5))
    for m, c, key in MODELS2:
        g = cv[(cv.model == m) & (cv.epoch >= 3)]
        ax.plot(g.epoch, g.val_seg_mean, color=c, label=T[key][lang], zorder=3)
        ax.fill_between(g.epoch, g.val_seg_mean - g.val_seg_sd, g.val_seg_mean + g.val_seg_sd, color=c, alpha=0.18,
                        linewidth=0, zorder=2)
        best = g.loc[g.val_seg_mean.idxmin()]
        ax.plot(best.epoch, best.val_seg_mean, marker="v", color=c, markeredgecolor="black", markersize=5, zorder=4)
    ax.axvline(90.5, color="black", linestyle=":", linewidth=0.7)
    ax.set_xlim(3, 100)
    ax.set_xlabel(T["epoch"][lang])
    ax.set_ylabel(L("Val segmentation loss", "Validation segmentation loss", lang))
    num_axis(ax, "y", 1, lang)
    grid_y(ax)
    legend_top(ax)
    save(fig, "c01_val_seg_loss", lang)


def c02_train_seg_loss(lang, st):
    """Đường: train segmentation loss trung bình N_SEED seed; đánh dấu thời điểm tắt mosaic."""
    cv = pd.read_csv(BANG_SEED / "05_duong_cong_theo_epoch.csv", encoding="utf-8-sig")
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.45))
    for m, c, key in MODELS2:
        g = cv[cv.model == m]
        ax.plot(g.epoch, g.train_seg_mean, color=c, label=T[key][lang], linewidth=1.0 if m == "Baseline" else 1.0,
                linestyle="-" if m == "Baseline" else "--", zorder=3)
    ax.axvline(90.5, color="black", linestyle=":", linewidth=0.7)
    ax.text(89.5, ax.get_ylim()[1] * 0.97, T["close_mosaic"][lang], ha="right", va="top", fontsize=st["font"] - 2)
    ax.set_xlim(1, 100)
    ax.set_xlabel(T["epoch"][lang])
    ax.set_ylabel(L("Train segmentation loss", "Training segmentation loss", lang))
    num_axis(ax, "y", 1, lang)
    grid_y(ax)
    legend_top(ax)
    save(fig, "c02_train_seg_loss", lang)


# ---------------------------------------------------------------- Chương 6: sai số và hiệu năng
def e01_tp_fp_fn(lang, st):
    """Cột kép mean ± SD của TP, FP, FN (đối tượng) trên N_SEED seed."""
    cm = pd.read_csv(BANG_SEED / "06_ma_tran_nham_lan_tung_seed.csv", encoding="utf-8-sig")
    keys = ["TP", "FP", "FN"]
    fig, ax = plt.subplots(figsize=(st["width"] * (0.7 if lang == "vi" else 1.0), st["width"] * 0.5))
    x = np.arange(3)
    w = 0.36
    for k, (m, c, key) in enumerate(MODELS2):
        g = cm[cm.model == m][keys]
        bars = ax.bar(x + (k - 0.5) * w, g.mean(), w * 0.92, color=c, alpha=0.85, label=T[key][lang], zorder=2)
        ax.errorbar(x + (k - 0.5) * w, g.mean(), yerr=g.std(ddof=1), fmt="none", ecolor="black", elinewidth=0.8,
                    capsize=2.5, zorder=3)
        for b, v, sdv in zip(bars, g.mean(), g.std(ddof=1)):
            ax.text(b.get_x() + b.get_width() / 2, v + sdv + 2, num(v, 2, lang), ha="center", fontsize=st["font"] - 2)
    ax.set_xticks(x, keys)
    ax.set_ylabel(L("Số đối tượng (trên 127 polyp)", "Objects (of 127 polyps)", lang))
    ax.set_ylim(0, 135)
    grid_y(ax)
    legend_top(ax)
    save(fig, "e01_tp_fp_fn", lang)


def e02_do_tre_cpu(lang, st):
    """Cột kép mean ± SD độ trễ suy luận trên CPU (seed 0, 100 lượt đo)."""
    e = pd.read_csv(EFF, encoding="utf-8-sig")
    modes = [("forward_only", L("Chỉ forward", "Forward only", lang)),
             ("predict_pipeline", L("Toàn pipeline", "Full pipeline", lang))]
    fig, ax = plt.subplots(figsize=(st["width"] * (0.7 if lang == "vi" else 1.0), st["width"] * 0.5))
    x = np.arange(2)
    w = 0.36
    for k, (name, c, key) in enumerate([("YOLO26s-seg", C_BASE, "baseline"), ("YOLO26s-TSVM-FP32-seg", C_TSVM, "tsvm")]):
        g = e[e.model == name].set_index("mode")
        mu = [g.loc[mo, "mean_ms"] for mo, _ in modes]
        sdv = [g.loc[mo, "sd_ms"] for mo, _ in modes]
        bars = ax.bar(x + (k - 0.5) * w, mu, w * 0.92, color=c, alpha=0.85, label=T[key][lang], zorder=2)
        ax.errorbar(x + (k - 0.5) * w, mu, yerr=sdv, fmt="none", ecolor="black", elinewidth=0.8, capsize=2.5, zorder=3)
        for b, v, s_ in zip(bars, mu, sdv):
            ax.text(b.get_x() + b.get_width() / 2, v + s_ + 10, num(v, 0, lang), ha="center", fontsize=st["font"] - 2)
    ax.set_xticks(x, [lab for _, lab in modes])
    ax.set_ylabel(L("Độ trễ CPU (ms/ảnh)", "CPU latency (ms/image)", lang))
    ax.set_ylim(0, 700)
    grid_y(ax)
    legend_top(ax)
    save(fig, "e02_do_tre_cpu", lang)


def e03_tham_so_dung_luong(lang, st):
    """Hai biểu đồ cột: số tham số (triệu) và bộ nhớ tham số FP32 (MiB); mỗi biểu đồ một đơn vị."""
    e = pd.read_csv(EFF, encoding="utf-8-sig").drop_duplicates("model").set_index("model")
    items = [("params_M", L("Số tham số (triệu)", "Parameters (M)", lang), 2),
             ("fp32_parameter_MiB_unfused", L("Bộ nhớ tham số FP32 (MiB)", "FP32 parameter memory (MiB)", lang), 1)]
    names = [("YOLO26s-seg", C_BASE, "baseline_short"), ("YOLO26s-TSVM-FP32-seg", C_TSVM, "tsvm_short")]
    fig, axes = plt.subplots(1, 2, figsize=(st["width"] * (0.75 if lang == "vi" else 1.0), st["width"] * 0.42),
                             gridspec_kw={"wspace": 0.45})
    for ax, (col, lab, nd) in zip(axes, items):
        vals = [e.loc[n, col] for n, _, _ in names]
        bars = ax.bar([0, 1], vals, 0.6, color=[c for _, c, _ in names], alpha=0.88, zorder=2)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v * 1.02, num(v, nd, lang), ha="center", va="bottom",
                    fontsize=st["font"] - 2)
        ax.set_xticks([0, 1], [T[k][lang] for _, _, k in names])
        ax.set_ylabel(lab)
        ax.set_ylim(0, max(vals) * 1.18)
        grid_y(ax)
    save(fig, "e03_tham_so_dung_luong", lang)


# ---------------------------------------------------------------- Chương 6: so sánh 4 mô hình theo pixel
def _pix():
    return pd.read_csv(BANG_SEED / "11_pixel_tung_seed.csv", encoding="utf-8-sig")


def p01_cot_kep_pixel(lang, st):
    """Cột mean ± SD (N_SEED seed) của Dice, IoU, Precision, Recall theo pixel cho 4 mô hình."""
    sd = _pix()
    metrics = [("dice", "Dice"), ("iou", "IoU"), ("precision", "Precision"), ("recall", "Recall")]
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.55))
    x = np.arange(len(metrics))
    w = 0.2
    for k, (key, c, lab) in enumerate(PIX_MODELS):
        g = sd[sd.model == key]
        mu = [g[m].mean() for m, _ in metrics]
        s_ = [g[m].std(ddof=1) for m, _ in metrics]
        ax.bar(x + (k - 1.5) * w, mu, w * 0.92, color=c, alpha=0.88, label=lab[lang], zorder=2)
        ax.errorbar(x + (k - 1.5) * w, mu, yerr=s_, fmt="none", ecolor="black", elinewidth=0.7, capsize=1.8, zorder=3)
    ax.set_xticks(x, [lab for _, lab in metrics])
    ax.set_ylabel(L("Giá trị theo pixel", "Pixel-level score", lang))
    ax.set_ylim(0, 1.0)
    num_axis(ax, "y", 1, lang)
    grid_y(ax)
    legend_top(ax, ncol=2 if lang == "en" else 4)
    save(fig, "p01_cot_kep_pixel", lang)


def p02_diem_dice_tung_seed(lang, st):
    """Điểm Dice của từng seed cho 4 mô hình; vạch đen là trung bình."""
    sd = _pix()
    fig, ax = plt.subplots(figsize=(st["width"] * (0.75 if lang == "vi" else 1.0), st["width"] * 0.55))
    rng = np.random.default_rng(1)
    for k, (key, c, lab) in enumerate(PIX_MODELS):
        g = sd[sd.model == key]["dice"]
        ax.scatter(k + rng.uniform(-0.18, 0.18, len(g)), g, s=12, color=c, alpha=0.8, edgecolors="white",
                   linewidths=0.3, zorder=3)
        ax.hlines(g.mean(), k - 0.28, k + 0.28, color="black", linewidth=1.2, zorder=4)
    ax.set_xticks(range(4), [lab[lang].replace(" + ", "\n+ ").replace(" (", "\n(") for _, _, lab in PIX_MODELS])
    ax.set_ylabel(L("Dice theo pixel (trung bình 120 ảnh)", "Pixel Dice (mean of 120 images)", lang))
    num_axis(ax, "y", 2, lang)
    grid_y(ax)
    save(fig, "p02_diem_dice_tung_seed", lang)


def p03_bao_nham_anh_nen(lang, st):
    """Cột mean ± SD: tỉ lệ ảnh nền (40 ảnh) có dự đoán polyp."""
    sd = _pix()
    fig, ax = plt.subplots(figsize=(st["width"] * (0.8 if lang == "vi" else 1.0), st["width"] * 0.5))
    for k, (key, c, lab) in enumerate(PIX_MODELS):
        g = 100 * sd[sd.model == key]["bg_fp_image_rate"]
        lo = min(g.std(ddof=1), g.mean())   # tỉ lệ không âm: cắt thanh lỗi dưới tại 0
        ax.bar(k, g.mean(), 0.6, color=c, alpha=0.88, zorder=2)
        ax.errorbar(k, g.mean(), yerr=[[lo], [g.std(ddof=1)]], fmt="none", ecolor="black", elinewidth=0.8,
                    capsize=2.5, zorder=3)
        ax.text(k, g.mean() + g.std(ddof=1) + 0.6, num(g.mean(), 1, lang), ha="center", fontsize=st["font"] - 2)
    ax.set_xticks(range(4), [lab[lang].replace(" + ", "\n+ ").replace(" (", "\n(") for _, _, lab in PIX_MODELS],
                  fontsize=st["font"] - 2)
    ax.set_ylabel(L("Ảnh nền bị báo nhầm (%)", "False-alarm background images (%)", lang))
    ax.set_ylim(0, ax.get_ylim()[1] * 1.08)   # chừa chỗ cho nhãn số trên thanh cao nhất
    grid_y(ax)
    save(fig, "p03_bao_nham_anh_nen", lang)


def q01_minh_hoa_dinh_tinh(lang, st):
    """Ảnh minh họa: ảnh gốc, nhãn và dự đoán seed 0 của 4 mô hình trên 3 ảnh validation."""
    import cv2
    pix = pd.read_csv(BANG / "10_pixel_tung_anh.csv", encoding="utf-8-sig")
    pol = pix[(pix.seed == 0) & ~pix.is_bg]
    dice = pol.assign(d=2 * pol.tp / (2 * pol.tp + pol.fp + pol.fn)).pivot(index="image", columns="model", values="d")
    # chọn ảnh: một ảnh cả 4 đều tốt, một ảnh TSVM tốt hơn đối chứng nhiều nhất, một ảnh khó (trung bình thấp)
    picks = [dice.mean(axis=1).idxmax(), (dice.tsvm - dice.baseline).idxmax(), dice.mean(axis=1).idxmin()]
    Q = REPO / "06_bao_cao" / "hinh" / "du_lieu_dinh_tinh"
    preds = {k: np.load(Q / f"pred_seed0_{k}.npz") for k, _, _ in PIX_MODELS}
    cols = [L("Ảnh gốc", "Image", lang), L("Nhãn", "Ground truth", lang), "YOLO26s-seg",
            "YOLO26s-seg\n+ TSVM", "PraNet\n(ResNet-50)", "U-Net"]
    fig, axes = plt.subplots(len(picks), len(cols), figsize=(st["width"] * (1.0 if lang == "vi" else 2.05),
                                                             st["width"] * (0.5 if lang == "vi" else 1.0)))
    for r, name in enumerate(picks):
        img = cv2.cvtColor(cv2.imread(str(DATASET / "images" / "val" / name)), cv2.COLOR_BGR2RGB)
        h, w = img.shape[:2]
        gt = np.zeros((h, w), np.uint8)
        for line in (DATASET / "labels" / "val" / f"{Path(name).stem}.txt").read_text().splitlines():
            c = np.array(line.split()[1:], np.float32).reshape(-1, 2) * [w, h]
            cv2.fillPoly(gt, [c.astype(np.int32)], 1)
        panels = [img, gt.astype(bool)] + [np.unpackbits(preds[k][name])[: h * w].reshape(h, w).astype(bool)
                                            for k, _, _ in PIX_MODELS]
        for cidx, (ax, pnl) in enumerate(zip(axes[r], panels)):
            if cidx == 0:
                ax.imshow(pnl)
            else:
                over = img.copy().astype(float) / 255
                color = np.array(matplotlib.colors.to_rgb(
                    "#FFFFFF" if cidx == 1 else PIX_MODELS[cidx - 2][1]))
                over[pnl] = 0.45 * over[pnl] + 0.55 * color
                ax.imshow(over)
                ax.contour(gt, levels=[0.5], colors="yellow", linewidths=0.6)
                if cidx >= 2:
                    k = PIX_MODELS[cidx - 2][0]
                    ax.text(0.03, 0.04, f"Dice {num(dice.loc[name, k], 2, lang)}", transform=ax.transAxes,
                            fontsize=st["font"] - 3, color="white",
                            bbox=dict(facecolor="black", alpha=0.55, pad=1, linewidth=0))
            ax.set_xticks([])
            ax.set_yticks([])
            if r == 0:
                ax.set_title(cols[cidx], fontsize=st["font"] - 2)
    fig.subplots_adjust(wspace=0.03, hspace=0.05)
    save(fig, "q01_minh_hoa_dinh_tinh", lang)


# ---------------------------------------------------------------- Chương 2: bốn kiểu đầu ra
ANH_HAI_POLYP = "cju7eea9b2m0z0801ynqv1fqu"   # ảnh val có hai polyp tách rời, kích thước gần nhau


def t01_bon_kieu_dau_ra(lang, st):
    """Hình 2.1: cùng một ảnh, bốn kiểu đầu ra (phân loại, hộp bao, mặt nạ ngữ nghĩa, mặt nạ thực thể), vẽ từ nhãn."""
    import cv2
    img = cv2.cvtColor(cv2.imread(str(DATASET / "images" / "val" / f"{ANH_HAI_POLYP}.jpg")), cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]
    polys = [np.array(l.split()[1:], np.float32).reshape(-1, 2) * [w, h]
             for l in (DATASET / "labels" / "val" / f"{ANH_HAI_POLYP}.txt").read_text().splitlines() if l.strip()]
    inst_colors = [C_TSVM, C_PRANET]
    titles = [L("(a) Phân loại\nảnh", "(a) Image\nclassification", lang),
              L("(b) Phát hiện\nđối tượng", "(b) Object\ndetection", lang),
              L("(c) Phân đoạn\nngữ nghĩa", "(c) Semantic\nsegmentation", lang),
              L("(d) Phân đoạn\nthực thể", "(d) Instance\nsegmentation", lang)]
    fig, axes = plt.subplots(1, 4, figsize=(st["width"] * (1.0 if lang == "vi" else 2.05),
                                            st["width"] * (0.24 if lang == "vi" else 0.5)))
    base = img.astype(float) / 255
    for k, ax in enumerate(axes):
        if k == 0:
            ax.imshow(img)
            ax.text(0.03, 0.05, L("có polyp: 0,97", "polyp: 0.97", lang), transform=ax.transAxes,
                    fontsize=st["font"] - 2, color="white", bbox=dict(facecolor="black", alpha=0.6, pad=1.5, linewidth=0))
        elif k == 1:
            ax.imshow(img)
            for c in polys:
                x0, y0 = c.min(0)
                x1, y1 = c.max(0)
                ax.add_patch(matplotlib.patches.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False,
                                                          edgecolor=C_BASE, linewidth=1.4))
        else:
            over = base.copy()
            for i, c in enumerate(polys):
                m = np.zeros((h, w), np.uint8)
                cv2.fillPoly(m, [c.astype(np.int32)], 1)
                col = np.array(matplotlib.colors.to_rgb(C_BASE if k == 2 else inst_colors[i % 2]))
                over[m.astype(bool)] = 0.35 * over[m.astype(bool)] + 0.65 * col
            ax.imshow(over)
            if k == 3:
                for i, c in enumerate(polys):
                    cx, cy = c.mean(0)
                    ax.text(cx, cy, f"#{i + 1}", ha="center", va="center", fontsize=st["font"] - 2, color="white",
                            fontweight="bold")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(titles[k], fontsize=st["font"] - 2)
    fig.subplots_adjust(wspace=0.04)
    save(fig, "t01_bon_kieu_dau_ra", lang)


# ---------------------------------------------------------------- Chương 6: chỉ số topology
def _topo():
    sd = pd.read_csv(BANG_SEED / "14_topology_tung_seed.csv", encoding="utf-8-sig")
    return sd[sd.min_area == 20]   # ngưỡng chính: bỏ mảnh/lỗ < 20 pixel, như khi tạo nhãn


def o01_anh_dung_topology(lang, st):
    """Tỉ lệ ảnh polyp có số mảnh và số lỗ khớp nhãn, 4 mô hình, mean ± SD qua các seed."""
    sd = _topo()
    fig, ax = plt.subplots(figsize=(st["width"] * (0.8 if lang == "vi" else 1.0), st["width"] * 0.5))
    for k, (key, c, lab) in enumerate(PIX_MODELS):
        g = 100 * sd[sd.model == key]["topo_ok"]
        ax.bar(k, g.mean(), 0.6, color=c, alpha=0.88, zorder=2)
        ax.errorbar(k, g.mean(), yerr=g.std(ddof=1), fmt="none", ecolor="black", elinewidth=0.8, capsize=2.5, zorder=3)
        ax.text(k, g.mean() + g.std(ddof=1) + 1.5, num(g.mean(), 1, lang), ha="center", fontsize=st["font"] - 2)
    ax.set_xticks(range(4), [lab[lang].replace(" + ", "\n+ ").replace(" (", "\n(") for _, _, lab in PIX_MODELS],
                  fontsize=st["font"] - 2)
    ax.set_ylabel(L("Ảnh đúng topology (%)", "Topologically correct images (%)", lang))
    ax.set_ylim(0, 105)
    grid_y(ax)
    save(fig, "o01_anh_dung_topology", lang)


def o02_kieu_loi_topology(lang, st):
    """Ba kiểu lỗi topology (thừa mảnh, có lỗ, thiếu mảnh) theo tỉ lệ ảnh polyp, mean ± SD qua các seed."""
    sd = _topo()
    kinds = [("frag_rate", L("Thừa mảnh", "Extra fragments", lang)), ("hole_rate", L("Có lỗ", "Holes", lang)),
             ("miss_rate", L("Thiếu mảnh", "Missing parts", lang))]
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.5))
    x = np.arange(len(kinds))
    w = 0.2
    for k, (key, c, lab) in enumerate(PIX_MODELS):
        g = sd[sd.model == key]
        mu = [100 * g[m].mean() for m, _ in kinds]
        s_ = [100 * g[m].std(ddof=1) for m, _ in kinds]
        ax.bar(x + (k - 1.5) * w, mu, w * 0.92, color=c, alpha=0.88, label=lab[lang], zorder=2)
        ax.errorbar(x + (k - 1.5) * w, mu, yerr=[np.minimum(s_, mu), s_], fmt="none", ecolor="black",
                    elinewidth=0.7, capsize=1.6, zorder=3)
    ax.set_xticks(x, [lab for _, lab in kinds])
    ax.set_ylabel(L("Tỉ lệ ảnh polyp (%)", "Polyp images (%)", lang))
    grid_y(ax)
    legend_top(ax, ncol=2 if lang == "en" else 4)
    save(fig, "o02_kieu_loi_topology", lang)


# ---------------------------------------------------------------- Chương 6: dữ liệu ngoài
NGOAI = REPO / "08_du_lieu_thuc_te" / "bang"
NGOAI_SETS = [("clinicdb", "CVC-ClinicDB"), ("colondb", "CVC-ColonDB"), ("etis", "ETIS-Larib"),
              ("polypgen", "PolypGen")]


def _ngoai():
    return pd.read_csv(NGOAI / f"{N_SEED}seed" / "01_ngoai_tung_seed.csv", encoding="utf-8-sig")


def _cot_nhom(ax, sd, sets, metric, scale=1.0):
    """Cột nhóm mean ± SD qua các seed: mỗi nhóm là một bộ dữ liệu, mỗi cột một mô hình."""
    x = np.arange(len(sets))
    w = 0.2
    for k, (key, c, lab) in enumerate(PIX_MODELS):
        g = sd[sd.model == key]
        mu = [scale * g[g.dataset == d][metric].mean() for d, _ in sets]
        s_ = [scale * g[g.dataset == d][metric].std(ddof=1) for d, _ in sets]
        ax.bar(x + (k - 1.5) * w, mu, w * 0.92, color=c, alpha=0.88, label=key, zorder=2)
        ax.errorbar(x + (k - 1.5) * w, mu, yerr=s_, fmt="none", ecolor="black", elinewidth=0.7, capsize=1.6, zorder=3)
    ax.set_xticks(x, [lab for _, lab in sets])
    grid_y(ax)


def x01_dice_du_lieu_ngoai(lang, st):
    """Dice theo pixel của 4 mô hình trên 4 bộ dữ liệu ngoài (mean ± SD qua các seed)."""
    sd = _ngoai()
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.5))
    _cot_nhom(ax, sd, NGOAI_SETS, "dice")
    h_, _l = ax.get_legend_handles_labels()
    legend_top(ax, ncol=2 if lang == "en" else 4, handles=h_, labels=[lab[lang] for _, _, lab in PIX_MODELS])
    ax.set_ylabel(L("Dice theo pixel", "Pixel Dice", lang))
    ax.set_ylim(0, 1.0)
    num_axis(ax, "y", 1, lang)
    save(fig, "x01_dice_du_lieu_ngoai", lang)


def x02_dice_polypgen_trung_tam(lang, st):
    """Dice theo pixel của 4 mô hình trên từng trung tâm C1–C6 của PolypGen."""
    sd = _ngoai()
    sets = [(f"pg_c{i}", f"C{i}") for i in range(1, 7)]
    fig, ax = plt.subplots(figsize=(st["width"], st["width"] * 0.5))
    _cot_nhom(ax, sd, sets, "dice")
    h_, _l = ax.get_legend_handles_labels()
    legend_top(ax, ncol=2 if lang == "en" else 4, handles=h_, labels=[lab[lang] for _, _, lab in PIX_MODELS])
    ax.set_xlabel(L("Trung tâm thu ảnh của PolypGen", "PolypGen data centre", lang))
    ax.set_ylabel(L("Dice theo pixel", "Pixel Dice", lang))
    ax.set_ylim(0, 1.0)
    num_axis(ax, "y", 1, lang)
    save(fig, "x02_dice_polypgen_trung_tam", lang)


def x03_bao_nham_polypgen(lang, st):
    """Tỉ lệ ảnh không có polyp của PolypGen (125 ảnh) bị dự đoán có polyp, mean ± SD qua các seed."""
    sd = _ngoai()
    sd = sd[sd.dataset == "polypgen"]
    fig, ax = plt.subplots(figsize=(st["width"] * (0.8 if lang == "vi" else 1.0), st["width"] * 0.5))
    for k, (key, c, lab) in enumerate(PIX_MODELS):
        g = 100 * sd[sd.model == key]["bg_fp_image_rate"]
        lo = min(g.std(ddof=1), g.mean())
        ax.bar(k, g.mean(), 0.6, color=c, alpha=0.88, zorder=2)
        ax.errorbar(k, g.mean(), yerr=[[lo], [g.std(ddof=1)]], fmt="none", ecolor="black", elinewidth=0.8,
                    capsize=2.5, zorder=3)
        ax.text(k, g.mean() + g.std(ddof=1) + 1.5, num(g.mean(), 1, lang), ha="center", fontsize=st["font"] - 2)
    ax.set_xticks(range(4), [lab[lang].replace(" + ", "\n+ ").replace(" (", "\n(") for _, _, lab in PIX_MODELS],
                  fontsize=st["font"] - 2)
    ax.set_ylabel(L("Ảnh không polyp bị báo nhầm (%)", "False-alarm polyp-free images (%)", lang))
    ax.set_ylim(0, ax.get_ylim()[1] * 1.08)
    grid_y(ax)
    save(fig, "x03_bao_nham_polypgen", lang)


FIGS_BO_SUNG = {
    "d01": d01_thanh_phan_bg20, "d02": d02_so_polyp_moi_anh, "d03": d03_so_dinh_polygon, "d04": d04_dien_tich_polyp,
    "m01": m01_tham_so_tang10,
    "r01": r01_delta_tung_seed, "r02": r02_hop_phan_bo, "r03": r03_histogram_delta,
    "r04": r04_do_nhay_quy_tac_epoch, "r05": r05_precision_recall,
    "c01": c01_val_seg_loss, "c02": c02_train_seg_loss,
    "e01": e01_tp_fp_fn, "e02": e02_do_tre_cpu, "e03": e03_tham_so_dung_luong,
    "p01": p01_cot_kep_pixel, "p02": p02_diem_dice_tung_seed, "p03": p03_bao_nham_anh_nen,
    "q01": q01_minh_hoa_dinh_tinh,
    "t01": t01_bon_kieu_dau_ra,
    "o01": o01_anh_dung_topology, "o02": o02_kieu_loi_topology,
    "x01": x01_dice_du_lieu_ngoai, "x02": x02_dice_polypgen_trung_tam, "x03": x03_bao_nham_polypgen,
}



FIGS = {
    "h01": h01_cot_kep_chi_so_mask,
    "h01b": h01b_diem_tung_seed_chi_so_mask,
    "h02": h02_ghep_cap_tung_seed,
    "h03": h03_duong_mien_mask_map_theo_epoch,
    "h04": h04_ma_tran_nham_lan,
    **FIGS_BO_SUNG,
}


# Hình kết quả phụ thuộc nhóm seed; các hình còn lại ghi vào chung/.
THEO_SEED = {"h01", "h01b", "h02", "h03", "h04", "r01", "r02", "r03", "r04", "r05", "c01", "c02", "e01",
             "p01", "p02", "p03", "x01", "x02", "x03", "o01", "o02"}


def main() -> None:
    global BANG_SEED, N_SEED, DICH
    ap = argparse.ArgumentParser()
    ap.add_argument("--chi", nargs="*", help="chỉ vẽ các hình có mã này, ví dụ h01 h03")
    ap.add_argument("--seeds", type=int, default=20, help="số seed (0..N-1) cho hình kết quả; mặc định 20")
    args = ap.parse_args()
    N_SEED = args.seeds
    BANG_SEED = BANG if N_SEED == 20 else BANG / f"{N_SEED}seed"
    assert (BANG_SEED / "02_ket_qua_tung_seed.csv").is_file(), f"Chưa có bảng {BANG_SEED}; chạy tinh_lai_so_lieu.py --seeds {N_SEED}"
    keys = args.chi or list(FIGS)
    for lang, st in STYLE.items():
        setup(st)
        for k in keys:
            DICH = OUT / (f"ket_qua_{N_SEED}seed" if k in THEO_SEED else "chung")
            FIGS[k](lang, st)
            print(f"{lang}: {k} -> {DICH.name}")


if __name__ == "__main__":
    main()
