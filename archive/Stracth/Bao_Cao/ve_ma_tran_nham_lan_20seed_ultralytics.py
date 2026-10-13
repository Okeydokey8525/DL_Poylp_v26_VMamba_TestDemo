"""Ve ma tran nham lan trung binh 20 seed theo bo cuc Ultralytics (hang = Predicted, cot = True) - Hinh 1 bao cao 13-10.

    python archive/Stracth/Bao_Cao/ve_ma_tran_nham_lan_20seed_ultralytics.py

Nguon: raw_20seeds_confusion_matrices.csv (da doi chieu 40/40 voi confusion_matrix.png cua tung seed).
Ghi archive/Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/figures/13_confusion_matrix_mean_ultralytics.png (khong ghi de).
Hai bang canh nhau (Baseline trai, TSVM phai), chi so dem trung binh +- do lech chuan (ddof=1). Khong ve ban chuan hoa:
TN khong duoc dem nen cot background chuan hoa luon = 1.00, khong mang thong tin; do nhay TP/127 da co o Bang 5.
Khong dung cot TN_reconstructed (40 - FP sai khai niem).
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "Ket_Qua_V2" / "KQ_Nen_DX_20seed_FP32"
OUT = DATA / "figures" / "13_confusion_matrix_mean_ultralytics.png"
N_POLYP = 127
GRAY = "#e6e6e6"

cm = pd.read_csv(DATA / "raw_20seeds_confusion_matrices.csv")
assert (cm.TP + cm.FN == N_POLYP).all()
n = cm.seed.nunique()
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
blues = plt.get_cmap("Blues")
names = {"Baseline": "YOLO26-SEG (Baseline)", "TSVM": "YOLO26-SEG - TSVM"}


def axes_style(ax):
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["polyp", "background"], fontsize=10.5, fontweight="bold")
    ax.set_yticklabels(["polyp", "background"], fontsize=10.5, fontweight="bold")
    ax.set_xlabel("Nhãn thực tế (True)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Nhãn dự đoán (Predicted)", fontsize=11, fontweight="bold")
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(1.5, -0.5)


def cell(ax, r, c, face, big, small, color="black"):
    ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, facecolor=face, edgecolor="white", linewidth=2))
    ax.text(c, r - 0.12, big, ha="center", va="center", color=color, fontsize=15, fontweight="bold")
    ax.text(c, r + 0.22, small, ha="center", va="center", color=color, fontsize=9.5)


def ink(v):
    return "white" if v > 0.5 else "black"


fig = plt.figure(figsize=(14, 6.8), dpi=300)
axes = [fig.add_axes([x, 0.08, 0.34, 0.70]) for x in (0.06, 0.55)]
cax = fig.add_axes([0.91, 0.18, 0.012, 0.50])
for ax, model in zip(axes, names):
    part = cm[cm.model == model]
    m, s = part[["TP", "FP", "FN"]].mean(), part[["TP", "FP", "FN"]].std(ddof=1)
    print(model, {k: f"{m[k]:.2f} ± {s[k]:.2f}" for k in m.index}, f"TP/127 = {m.TP / N_POLYP:.4f}")
    # Ultralytics layout: (pred polyp, true polyp)=TP, (pred polyp, true bg)=FP, (pred bg, true polyp)=FN
    for (r, c), k in {(0, 0): "TP", (0, 1): "FP", (1, 0): "FN"}.items():
        v = m[k] / N_POLYP
        cell(ax, r, c, blues(v), f"{m[k]:.2f}", f"{k}: ± {s[k]:.2f}", ink(v))
    cell(ax, 1, 1, GRAY, "—", "TN không được đếm")
    ax.set_title(f"{names[model]}\nSố đếm trung bình ± độ lệch chuẩn", fontsize=11.5, fontweight="bold", pad=10)
    axes_style(ax)

cbar = fig.colorbar(plt.cm.ScalarMappable(cmap=blues, norm=plt.Normalize(0, N_POLYP)), cax=cax)
cbar.set_label("Số đếm trung bình", fontsize=9)

fig.suptitle(f"Ma trận nhầm lẫn trung bình {n} seed", fontsize=14, fontweight="bold", y=0.95)
with OUT.open("xb") as f:
    fig.savefig(f, format="png", bbox_inches="tight", pad_inches=0.2)
print("saved", OUT)
