"""Ve ma tran nham lan trung binh 20 seed (Baseline, TSVM FP32, chenh lech) tu raw_20seeds_confusion_matrices.csv.

    python archive/Stracth/Bao_Cao/ve_ma_tran_nham_lan_20seed.py

Ghi archive/Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/figures/12_confusion_matrix_mean_comparison.png (khong ghi de).
Ultralytics khong dem o nen-nen (TN) cho phan doan thuc the, nen o do de trong ("khong xac dinh").
FP la du doan khong khop polyp nao (phan lon nam tren anh co polyp), nen ty le FP chia cho tong du doan:
FP / (TP + FP) = 1 - precision tai nguong conf cua ma tran, khong chia cho 127 nhan hay 40 anh nen.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "Ket_Qua_V2" / "KQ_Nen_DX_20seed_FP32"
OUT = DATA / "figures" / "12_confusion_matrix_mean_comparison.png"
N_POLYP = 127.0
GRAY = "#e6e6e6"

cm = pd.read_csv(DATA / "raw_20seeds_confusion_matrices.csv")
n = cm.seed.nunique()
plt.rcParams["font.sans-serif"] = "DejaVu Sans"


def stats(model):
    part = cm[cm.model == model]
    out = {k: (part[k].mean(), part[k].std(ddof=1)) for k in ("TP", "FN", "FP")}
    out["FP_rate"] = (part["FP"] / (part["TP"] + part["FP"])).mean()  # mean of per-seed rates, same as Bang 5
    return out


def axes_style(ax):
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["polyp", "background"], fontsize=10.5, fontweight="bold")
    ax.set_yticklabels(["polyp", "background"], fontsize=10.5, fontweight="bold")
    ax.set_xlabel("Predicted Label", fontsize=11, fontweight="bold")
    ax.set_ylabel("True Label", fontsize=11, fontweight="bold")
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(1.5, -0.5)


def cell(ax, r, c, face, big, small, color="black"):
    ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, facecolor=face, edgecolor="white", linewidth=2))
    ax.text(c, r - 0.12, big, ha="center", va="center", color=color, fontsize=15, fontweight="bold")
    ax.text(c, r + 0.22, small, ha="center", va="center", color=color, fontsize=9.5)


fig = plt.figure(figsize=(13, 11.5), dpi=300)
axes = [fig.add_axes([0.10, 0.50, 0.34, 0.38]), fig.add_axes([0.55, 0.50, 0.34, 0.38]), fig.add_axes([0.325, 0.04, 0.34, 0.38])]
cax = fig.add_axes([0.92, 0.55, 0.015, 0.28])
blues = plt.get_cmap("Blues")
names = {"Baseline": "Baseline YOLO26s-seg", "TSVM": "TSVM (Topology-Shape) FP32"}
st = {m: stats(m) for m in names}
for ax, model in zip(axes[:2], names):
    s = st[model]
    for c, key in enumerate(("TP", "FN")):  # polyp row: share of the 127 polyp instances
        rate = s[key][0] / N_POLYP
        cell(ax, 0, c, blues(rate), f"{rate:.2f}", f"{key}: {s[key][0]:.1f} ± {s[key][1]:.1f}", "white" if rate > 0.5 else "black")
    fp_rate = s["FP_rate"]  # share of all "polyp" predictions that match no polyp
    cell(ax, 1, 0, blues(fp_rate), f"{fp_rate:.3f}", f"FP: {s['FP'][0]:.1f} ± {s['FP'][1]:.1f}\ntrên tổng dự đoán polyp")
    cell(ax, 1, 1, GRAY, "—", "TN không xác định")
    ax.set_title(names[model], fontsize=12, fontweight="bold", pad=10)
    axes_style(ax)
cbar = fig.colorbar(plt.cm.ScalarMappable(cmap=blues, norm=plt.Normalize(0, 1)), cax=cax)
cbar.set_label("Tỷ lệ (TP, FN: trên 127 nhãn;\nFP: trên tổng dự đoán polyp)", fontsize=8.5)

ax = axes[2]
for c, key in enumerate(("TP", "FN")):
    d = st["TSVM"][key][0] - st["Baseline"][key][0]
    cell(ax, 0, c, "#f4f4f4", f"{d / N_POLYP * 100:+.2f} đ%", f"{key}: {d:+.1f} nhãn")
dfp = st["TSVM"]["FP"][0] - st["Baseline"]["FP"][0]
rate = {m: st[m]["FP_rate"] for m in names}
cell(ax, 1, 0, "#dbe9f6" if dfp < 0 else "#fbe0d6", f"{(rate['TSVM'] - rate['Baseline']) * 100:+.2f} đ%", f"FP: {dfp:+.1f} dự đoán")
cell(ax, 1, 1, GRAY, "—", "TN không xác định")
ax.set_title("Chênh lệch (TSVM − Baseline)", fontsize=12, fontweight="bold", pad=10)
axes_style(ax)

fig.suptitle(f"Ma Trận Nhầm Lẫn Trung Bình {n} Seeds (127 nhãn polyp, 40 ảnh nền)\n"
             "TP, FN chia cho 127 nhãn; FP chia cho tổng dự đoán (TP + FP); ô TN không được Ultralytics đếm",
             fontsize=13, fontweight="bold", y=0.985)
with OUT.open("xb") as f:
    fig.savefig(f, format="png", bbox_inches="tight", pad_inches=0.2)
print("saved", OUT)
