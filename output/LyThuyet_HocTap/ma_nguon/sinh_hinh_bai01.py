"""Sinh hình minh họa cho giáo trình Bài 1 (YOLO26-seg, VMamba, chỉ số đánh giá).

Chạy từ gốc repo:  python output/LyThuyet_HocTap/ma_nguon/sinh_hinh_bai01.py
Hình 1.8 đọc số liệu thật từ raw_10seeds_extracted_metrics.csv (chỉ đọc).
Các hình còn lại là sơ đồ minh họa khái niệm, không phải đầu ra của mô hình.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "output" / "LyThuyet_HocTap" / "hinh"
CSV = ROOT / "archive" / "Ket_Qua_V2" / "KQ_Nen_DX_10seed" / "01_raw_analysis" / "raw_10seeds_extracted_metrics.csv"

plt.rcParams.update({"font.family": "Times New Roman", "font.size": 13, "mathtext.fontset": "stix"})

INK = "#222222"
MUTED = "#6b6b6b"
BLUE = "#2a78d6"  # Baseline / thực thể thứ nhất
ORANGE = "#eb6834"  # TSVM / thực thể thứ hai
FILL_BLUE = "#dbe8f8"
FILL_ORANGE = "#fde3d6"
FILL_GREEN = "#dcefdc"
FILL_GRAY = "#f2f2f2"


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("đã lưu", name)


def box(ax, x, y, w, h, text, fc=FILL_GRAY, ec=INK, fs=12, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.8", fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK, weight=weight, linespacing=1.3)


def arrow(ax, p, q, color=INK, style="-|>", lw=1.3):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=13, color=color, lw=lw, shrinkA=0, shrinkB=0))


def blank_ax(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


# ---------------------------------------------------------------- Hình 1.1
def hinh_tich_chap():
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.6), gridspec_kw={"width_ratios": [5, 3, 3]})
    rng = np.random.default_rng(3)
    x = rng.integers(0, 9, size=(5, 5))
    k = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    y = np.array([[np.sum(x[i : i + 3, j : j + 3] * k) for j in range(3)] for i in range(3)])

    def grid(ax, m, title, hi=None, cell_fc="white"):
        n = m.shape[0]
        for i in range(n):
            for j in range(n):
                fc = cell_fc
                if hi is not None and hi[0] <= i < hi[0] + hi[2] and hi[1] <= j < hi[1] + hi[2]:
                    fc = FILL_ORANGE
                ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, fc=fc, ec=INK, lw=1))
                ax.text(j + 0.5, n - 0.5 - i, str(m[i, j]), ha="center", va="center", fontsize=13)
        ax.set_xlim(-0.1, n + 0.1)
        ax.set_ylim(-0.1, n + 0.1)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=13)

    grid(axes[0], x, "a. Ảnh vào 5×5", hi=(0, 0, 3))
    grid(axes[1], k, "b. Kernel 3×3", cell_fc=FILL_BLUE)
    grid(axes[2], y, "c. Bản đồ đặc trưng 3×3", hi=(0, 0, 1))
    save(fig, "hinh_1_1_tich_chap.png")


# ---------------------------------------------------------------- Hình 1.2
def hinh_kien_truc():
    fig, ax = blank_ax(11.5, 6.2, (0, 120), (0, 60))
    box(ax, 1, 24, 15, 12, "Ảnh vào\n640×640×3", fc=FILL_BLUE)
    ax.text(31, 57.5, "BACKBONE", ha="center", fontsize=13, weight="bold")
    box(ax, 21, 44, 20, 10, "Tầng 0–4\nP3: 80×80")
    box(ax, 21, 30, 20, 10, "Tầng 5–6\nP4: 40×40")
    box(ax, 21, 16, 20, 10, "Tầng 7–9 (SPPF)\nP5: 20×20")
    box(ax, 21, 2, 20, 10, "Tầng 10\nC2TSVMamba", fc=FILL_ORANGE, ec=ORANGE, weight="bold")
    arrow(ax, (16, 30), (21, 49))
    arrow(ax, (31, 44), (31, 40))
    arrow(ax, (31, 30), (31, 26))
    arrow(ax, (31, 16), (31, 12))

    ax.text(57, 57.5, "NECK", ha="center", fontsize=13, weight="bold")
    box(ax, 49, 2, 16, 52, "Trộn đặc trưng\nnhiều tỉ lệ\n(FPN + PAN)\n\nphóng to, ghép,\nthu nhỏ, ghép")
    arrow(ax, (41, 49), (49, 49))
    arrow(ax, (41, 35), (49, 35))
    arrow(ax, (41, 7), (49, 7))

    ax.text(87, 57.5, "HEAD", ha="center", fontsize=13, weight="bold")
    box(ax, 77, 30, 20, 24, "Segment26\n(mỗi vị trí dự đoán)\n• khung: 4 số\n• điểm tin cậy\n• 32 hệ số mặt nạ")
    box(ax, 77, 2, 20, 22, "Proto26\n32 prototype\n160×160\n(dùng chung\ncả ảnh)")
    for yy, lab in ((49, "P3 (tầng 16)"), (40, "P4 (tầng 19)"), (33, "P5 (tầng 22)")):
        arrow(ax, (65, yy), (77, yy))
        ax.text(71, yy + 0.9, lab, ha="center", fontsize=9, color=MUTED)
    arrow(ax, (65, 13), (77, 13))

    box(ax, 103, 18, 16, 20, "Kết quả\nkhung +\nmặt nạ\ntừng polyp", fc=FILL_GREEN)
    arrow(ax, (97, 42), (103, 32))
    arrow(ax, (97, 13), (103, 24))
    save(fig, "hinh_1_2_kien_truc_yolo26seg_tsvm.png")


# ---------------------------------------------------------------- Hình 1.3
def hinh_prototype():
    n = 96
    yy, xx = np.mgrid[0:n, 0:n] / (n - 1)
    protos = [
        np.exp(-(((xx - 0.45) ** 2 + (yy - 0.45) ** 2) / 0.04)) * 2 - 1,  # khối tròn ở giữa
        xx * 2 - 1,  # sáng dần sang phải
        yy * 2 - 1,  # sáng dần xuống dưới
        np.cos(np.sqrt((xx - 0.5) ** 2 + (yy - 0.5) ** 2) * 14),  # vòng đồng tâm
    ]
    coef = [3.0, -1.2, -0.8, 0.6]
    logit = sum(c * p for c, p in zip(coef, protos)) - 0.3
    mask = 1 / (1 + np.exp(-logit))

    fig, axes = plt.subplots(1, 6, figsize=(12, 2.9), gridspec_kw={"width_ratios": [1, 1, 1, 1, 0.35, 1.15]})
    for i, (ax, p, c) in enumerate(zip(axes[:4], protos, coef)):
        ax.imshow(p, cmap="gray", vmin=-1, vmax=1)
        ax.set_title(f"P{i + 1}\nhệ số c{i + 1} = {c:+.1f}", fontsize=12)
        ax.axis("off")
    axes[4].axis("off")
    axes[4].text(0.5, 0.5, "→", ha="center", va="center", fontsize=30)
    axes[5].imshow(mask > 0.5, cmap="gray")
    axes[5].set_title("Mặt nạ = sigmoid(Σ cᵢ·Pᵢ) > 0,5", fontsize=12)
    axes[5].axis("off")
    save(fig, "hinh_1_3_prototype_he_so.png")


# ---------------------------------------------------------------- Hình 1.4
def hinh_quet_4_huong():
    n = 4
    cells = [(r, c) for r in range(n) for c in range(n)]
    orders = {
        "Hướng 1: theo hàng, xuôi": cells,
        "Hướng 2: theo hàng, ngược": cells[::-1],
        "Hướng 3: theo cột, xuôi": [(r, c) for c in range(n) for r in range(n)],
        "Hướng 4: theo cột, ngược": [(r, c) for c in range(n) for r in range(n)][::-1],
    }
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.4))
    for ax, (title, order) in zip(axes, orders.items()):
        for r in range(n):
            for c in range(n):
                ax.add_patch(Rectangle((c, n - 1 - r), 1, 1, fc="white", ec="#bbbbbb", lw=1))
        pts = [(c + 0.5, n - 0.5 - r) for r, c in order]
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=BLUE, lw=1.6)
        for a, b in zip(pts[:-1], pts[1:]):
            ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.4, shrinkA=6, shrinkB=6))
        ax.plot(*pts[0], "o", color=ORANGE, ms=9)
        ax.text(pts[0][0], pts[0][1] + 0.28, "bắt đầu", ha="center", fontsize=9, color=MUTED)
        ax.set_xlim(-0.1, n + 0.1)
        ax.set_ylim(-0.1, n + 0.25)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=12)
    save(fig, "hinh_1_4_quet_4_huong.png")


# ---------------------------------------------------------------- Hình 1.5
def hinh_tsvm():
    fig, ax = blank_ax(10, 7.6, (0, 100), (0, 78))
    box(ax, 38, 70, 24, 7, "Đặc trưng vào x", fc=FILL_BLUE)
    box(ax, 6, 52, 30, 9, "SS2D (VMamba)\nngữ cảnh toàn cục → F_M", fc=FILL_ORANGE, ec=ORANGE)
    box(ax, 60, 58, 34, 8, "ShapeAwareBranch\ntích chập 3×3 và 5×5")
    box(ax, 60, 44, 34, 10, "DirectionalShapeExtractor\nlọc ngang 1×5, dọc 5×1, 3×3\nđộ lớn biên √(h² + v²) → S")
    box(ax, 60, 31, 34, 8, "TopologyShapeGate\n1×1 + sigmoid → G $\\in$ [0, 1]")
    box(ax, 6, 31, 30, 9, "Điều biến\nF_M $\\odot$ (1 + G)", fc=FILL_GREEN)
    box(ax, 22, 16, 56, 8, "Ghép [F_M $\odot$ (1 + G), S] → Conv 1×1 → FFN")
    box(ax, 30, 2, 40, 8, "Đầu ra = x + γ · (…),  γ khởi tạo 0,001", fc=FILL_BLUE)

    arrow(ax, (45, 70), (21, 61))
    arrow(ax, (55, 70), (77, 66))
    arrow(ax, (77, 58), (77, 54))
    arrow(ax, (77, 44), (77, 39))
    arrow(ax, (21, 52), (21, 40))
    arrow(ax, (60, 35), (36, 35))
    arrow(ax, (21, 31), (40, 24))
    arrow(ax, (94, 49), (97, 49), style="-")
    ax.plot([97, 97], [49, 20], color=INK, lw=1.3)
    arrow(ax, (97, 20), (78, 20))
    ax.text(98, 34, "S", fontsize=12, color=MUTED)
    arrow(ax, (50, 16), (50, 10))
    ax.plot([62, 99.5, 99.5], [73.5, 73.5, 6], color=MUTED, lw=1.1, ls="--")
    arrow(ax, (99.5, 6), (70, 6), color=MUTED)
    ax.text(99, 75, "nối tắt (residual)", ha="right", fontsize=10, color=MUTED)
    save(fig, "hinh_1_5_khoi_tsvm.png")


# ---------------------------------------------------------------- Hình 1.6
def hinh_iou():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.9))
    for ax, iou in zip(axes, (0.50, 0.75, 0.95)):
        d = (1 - iou) / (1 + iou)  # hai hình vuông cạnh 1 lệch ngang d có IoU = (1-d)/(1+d)
        ax.add_patch(Rectangle((0, 0), 1, 1, fc=BLUE, alpha=0.18, ec=BLUE, lw=2))
        ax.add_patch(Rectangle((d, 0.06), 1, 1, fc="none", ec=ORANGE, lw=2.2, ls="--"))
        passed = int(np.sum(np.linspace(0.5, 0.95, 10) <= iou + 1e-9))
        ax.set_title(f"IoU = {iou:.2f}\nđạt {passed}/10 ngưỡng của mAP@50-95", fontsize=12)
        ax.set_xlim(-0.15, 1.5)
        ax.set_ylim(-0.15, 1.25)
        ax.set_aspect("equal")
        ax.axis("off")
    axes[0].text(0.03, -0.12, "nhãn thật", color=BLUE, fontsize=11)
    axes[0].text(0.62, 1.1, "dự đoán", color=ORANGE, fontsize=11)
    save(fig, "hinh_1_6_iou_va_nguong.png")


# ---------------------------------------------------------------- Hình 1.7
def hinh_pr():
    r = np.linspace(0, 1, 200)
    p = np.clip(1 - 0.08 * r - 0.85 * r**6, 0, 1)
    ap = np.trapezoid(p, r) if hasattr(np, "trapezoid") else np.trapz(p, r)
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    ax.fill_between(r, 0, p, color=BLUE, alpha=0.15, lw=0)
    ax.plot(r, p, color=BLUE, lw=2)
    ax.text(0.08, 0.3, f"AP = diện tích tô màu ≈ {ap:.2f}", fontsize=13, color=INK)
    for conf, rr, dx, dy in (("ngưỡng tin cậy cao", 0.25, 0.04, 0.07), ("ngưỡng tin cậy thấp", 0.93, -0.42, -0.12)):
        pp = 1 - 0.08 * rr - 0.85 * rr**6
        ax.plot(rr, pp, "o", color=ORANGE, ms=8)
        ax.annotate(conf, (rr, pp), xytext=(rr + dx, pp + dy), fontsize=11, color=MUTED)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.12)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(color="#e6e6e6", lw=0.8)
    save(fig, "hinh_1_7_duong_pr.png")


# ---------------------------------------------------------------- Hình 1.8
def hinh_ket_qua():
    data: dict[str, dict[int, float]] = {"Baseline": {}, "TSVM": {}}
    with CSV.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["model"] in data:
                data[row["model"]][int(row["seed"])] = float(row["mask_map50_95"])
    seeds = sorted(data["Baseline"])
    b = np.array([data["Baseline"][s] for s in seeds])
    t = np.array([data["TSVM"][s] for s in seeds])

    fig, ax = plt.subplots(figsize=(9, 4.6))
    for s, vb, vt in zip(seeds, b, t):
        ax.plot([s, s], [vb, vt], color="#c8c8c8", lw=2, zorder=1)
    ax.scatter(seeds, b, s=70, marker="o", color=BLUE, ec="white", lw=1.5, zorder=3, label="Baseline YOLO26s-seg")
    ax.scatter(seeds, t, s=70, marker="s", color=ORANGE, ec="white", lw=1.5, zorder=3, label="YOLO26s-seg + TSVM")
    ax.axhline(b.mean(), color=BLUE, lw=1.2, ls="--", zorder=2)
    ax.axhline(t.mean(), color=ORANGE, lw=1.2, ls=":", zorder=2)
    ax.text(9.75, b.mean(), f"TB {b.mean():.4f}", va="top", fontsize=11, color=INK)
    ax.text(9.75, t.mean(), f"TB {t.mean():.4f}", va="bottom", fontsize=11, color=INK)
    ax.set_xticks(seeds)
    ax.set_xlim(-0.5, 11.3)
    ax.set_xlabel("Seed")
    ax.set_ylabel("Mask mAP@50-95")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#e6e6e6", lw=0.8)
    ax.legend(loc="lower left", frameon=False, fontsize=11)
    save(fig, "hinh_1_8_ket_qua_10_seed.png")


if __name__ == "__main__":
    hinh_tich_chap()
    hinh_kien_truc()
    hinh_prototype()
    hinh_quet_4_huong()
    hinh_tsvm()
    hinh_iou()
    hinh_pr()
    hinh_ket_qua()
