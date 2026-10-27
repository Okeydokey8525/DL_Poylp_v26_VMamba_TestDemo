"""Vẽ sơ đồ kiến trúc cho Chương 3 (tiếng Việt) và bài báo IEEE (tiếng Anh).

Thông số lấy từ cấu hình yolo26-seg.yaml / yolo26-seg-TopologyShapeVMamba.yaml (scale s)
và mã nn/modules/topology_shape_vmamba.py của fork; kích thước tensor đã đối chiếu với
00_tai_lieu_tong_quan/bang/08_kien_truc_dung_lai.csv.

    python ve_so_do.py              # vẽ tất cả sơ đồ
    python ve_so_do.py --chi a01    # chỉ vẽ một sơ đồ
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
CM = 1 / 2.54

# Okabe–Ito: viền đậm, nền nhạt cùng tông
C_BB, F_BB = "#0072B2", "#E6F0F8"     # backbone
C_NK, F_NK = "#009E73", "#E5F4EE"     # neck
C_HD, F_HD = "#CC79A7", "#F7EAF2"     # head
C_TS, F_TS = "#D55E00", "#FBE4D6"     # khối đề xuất
C_SH, F_SH = "#E69F00", "#FCF0D9"     # nhánh hình dạng
C_GR, F_GR = "#555555", "#F2F2F2"     # khối chung
C_ARROW = "#333333"

STYLE = {
    "vi": {"lang": "vi", "fs": 6.5},
    "en": {"lang": "en", "fs": 6.0},
}


def setup() -> None:
    plt.rcParams.update({
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def box(ax, x, y, w, h, text, ec=C_GR, fc=F_GR, fs=7.0, lw=0.8, bold=False, ls="-", r=0.04, color="#111111"):
    """Hộp có tâm (x, y). Trả về tọa độ biên để nối mũi tên."""
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       linewidth=lw, edgecolor=ec, facecolor=fc, linestyle=ls, zorder=2)
    ax.add_patch(p)
    if text:
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=3, color=color,
                fontweight="bold" if bold else "normal", linespacing=1.15)
    return {"l": (x - w / 2, y), "r": (x + w / 2, y), "t": (x, y + h / 2), "b": (x, y - h / 2), "c": (x, y)}


def arrow(ax, p, q, cs="arc3", lw=0.7, color=C_ARROW, ls="-", head=4.0):
    a = FancyArrowPatch(p, q, arrowstyle=f"-|>,head_length={head / 10},head_width={head / 20}",
                        connectionstyle=cs, linewidth=lw, color=color, linestyle=ls,
                        shrinkA=0, shrinkB=0, zorder=1)
    ax.add_patch(a)


def line(ax, pts, lw=0.7, color=C_ARROW, ls="-"):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=1, solid_capstyle="round")


def poly_arrow(ax, pts, **kw):
    """Đường gấp khúc, mũi tên ở đoạn cuối."""
    if len(pts) > 2:
        line(ax, pts[:-1], lw=kw.get("lw", 0.7), color=kw.get("color", C_ARROW), ls=kw.get("ls", "-"))
    arrow(ax, pts[-2], pts[-1], **kw)


def save(fig, name: str, lang: str) -> None:
    d = OUT / lang
    d.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(d / f"{name}.{ext}")
    plt.close(fig)
    print("  ->", d / f"{name}.png")


# --------------------------------------------------------------------------- a01
def a01_kien_truc_tong_the(st: dict) -> None:
    """Toàn mạng YOLO26s-seg, đánh dấu tầng 10 được thay."""
    vi = st["lang"] == "vi"
    fs = st["fs"]
    W, H = (16.0 * CM, 15.5 * CM) if vi else (18.1 * CM, 15.5 * CM)
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(-0.75, 6.55)
    ax.set_ylim(-1.2, 12.45)
    ax.axis("off")

    bw, bh = 1.45, 0.74
    xb, xn1, xn2, xh = 0.0, 1.95, 3.75, 5.6

    # nền vùng
    def region(x0, x1, y0, y1, fc, label):
        ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0,rounding_size=0.08",
                                    linewidth=0, facecolor=fc, alpha=0.45, zorder=0))
        ax.text((x0 + x1) / 2, y1 - 0.05, label, ha="center", va="top", fontsize=fs + 0.5, fontweight="bold",
                color="#222222")

    region(-0.72, 0.85, -0.55, 12.4, F_BB, "Backbone")
    region(1.15, 4.6, -0.55, 8.05, F_NK, "Neck (FPN + PAN)")
    region(4.78, 6.5, -0.55, 8.05, F_HD, "Head")

    # backbone: y giảm dần từ ảnh vào xuống tầng 10
    bb = [
        ("", "Ảnh vào" if vi else "Input", "3×640×640"),
        ("0", "Conv 3×3, s2", "32×320×320"),
        ("1", "Conv 3×3, s2", "64×160×160"),
        ("2", "C3k2", "128×160×160"),
        ("3", "Conv 3×3, s2", "128×80×80"),
        ("4", "C3k2", "256×80×80"),
        ("5", "Conv 3×3, s2", "256×40×40"),
        ("6", "C3k2", "256×40×40"),
        ("7", "Conv 3×3, s2", "512×20×20"),
        ("8", "C3k2", "512×20×20"),
        ("9", "SPPF", "512×20×20"),
    ]
    P = {}
    y = 11.5
    for idx, name, shp in bb:
        label = f"{idx}  {name}\n{shp}" if idx else f"{name}\n{shp}"
        P[idx or "in"] = box(ax, xb, y, bw, bh, label, ec=C_BB, fc="white", fs=fs)
        y -= 1.02
    y10 = y
    t10 = ("10  C2TSVMamba\n(thay cho C2PSA)\n512×20×20" if vi else "10  C2TSVMamba\n(replaces C2PSA)\n512×20×20")
    P["10"] = box(ax, xb, y10, bw + 0.1, bh + 0.3, t10, ec=C_TS, fc=F_TS, fs=fs, lw=1.4, bold=True)
    keys = ["in"] + [str(i) for i in range(10)]
    for k1, k2 in zip(keys, keys[1:] + ["10"]):
        arrow(ax, P[k1]["b"], P[k2]["t"])

    # neck nhánh từ trên xuống (đi lên trên hình): 11..16
    ytd = [0.2, 1.25, 2.3, 3.6, 4.65, 5.7]
    td = [
        ("11", "Upsample ×2", "512×40×40"),
        ("12", "Concat (+6)", "768×40×40"),
        ("13", "C3k2", "256×40×40"),
        ("14", "Upsample ×2", "256×80×80"),
        ("15", "Concat (+4)", "512×80×80"),
        ("16", "C3k2", "128×80×80"),
    ]
    for (idx, name, shp), yy in zip(td, ytd):
        P[idx] = box(ax, xn1, yy, bw, bh, f"{idx}  {name}\n{shp}", ec=C_NK, fc="white", fs=fs)
    for a_, b_ in zip(["11", "12", "13", "14", "15"], ["12", "13", "14", "15", "16"]):
        arrow(ax, P[a_]["t"], P[b_]["b"])
    # 10 -> 11
    poly_arrow(ax, [P["10"]["r"], (0.98, P["10"]["r"][1]), (0.98, ytd[0]), P["11"]["l"]])
    # skip 6 -> 12, 4 -> 15
    g6, g4 = 1.06, 1.14
    poly_arrow(ax, [P["6"]["r"], (g6, P["6"]["r"][1]), (g6, ytd[1]), P["12"]["l"]], color=C_BB)
    poly_arrow(ax, [P["4"]["r"], (g4, P["4"]["r"][1]), (g4, ytd[4]), P["15"]["l"]], color=C_BB)

    # neck nhánh từ dưới lên (đi xuống trên hình): 17..22
    ybu = [5.7, 4.65, 3.6, 2.3, 1.25, 0.2]
    bu = [
        ("17", "Conv 3×3, s2", "128×40×40"),
        ("18", "Concat (+13)", "384×40×40"),
        ("19", "C3k2", "256×40×40"),
        ("20", "Conv 3×3, s2", "256×20×20"),
        ("21", "Concat (+10)", "768×20×20"),
        ("22", "C3k2 (attn)", "512×20×20"),
    ]
    for (idx, name, shp), yy in zip(bu, ybu):
        P[idx] = box(ax, xn2, yy, bw, bh, f"{idx}  {name}\n{shp}", ec=C_NK, fc="white", fs=fs)
    for a_, b_ in zip(["17", "18", "19", "20", "21"], ["18", "19", "20", "21", "22"]):
        arrow(ax, P[a_]["b"], P[b_]["t"])
    # 16 -> 17
    poly_arrow(ax, [P["16"]["t"], (xn1, 6.45), (xn2, 6.45), P["17"]["t"]])
    # 13 -> 18
    poly_arrow(ax, [P["13"]["r"], (2.85, ytd[2]), (2.85, ybu[1]), P["18"]["l"]], color=C_NK)
    # 10 -> 21 (đường thứ hai của tầng 10)
    poly_arrow(ax, [P["10"]["b"], (xb, -0.75), (2.95, -0.75), (2.95, ybu[4]), P["21"]["l"]], color=C_TS, lw=1.0)
    ax.text(1.5, -0.83, "đầu ra tầng 10 đi tới tầng 11 và tầng 21" if vi else "layer-10 output feeds layers 11 and 21",
            ha="center", va="top", fontsize=fs - 0.8, color=C_TS)

    # head
    hb = box(ax, xh, 3.0, 1.62, 5.9, "", ec=C_HD, fc="white", fs=fs)
    ax.text(xh, 5.6, "23  Segment26", ha="center", va="center", fontsize=fs + 0.3, fontweight="bold")
    head_txt = ("Hai đầu dự đoán:\none-to-many (huấn luyện)\none-to-one (suy luận)\n\n"
                "Mỗi đối tượng:\nhộp, điểm lớp,\n32 hệ số mặt nạ\n\n"
                "Proto26:\n32 prototype 160×160\n\n"
                "Suy luận end-to-end,\nkhông dùng NMS") if vi else (
                "Dual heads:\none-to-many (training)\none-to-one (inference)\n\n"
                "Per object:\nbox, class score,\n32 mask coefficients\n\n"
                "Proto26:\n32 prototypes 160×160\n\n"
                "End-to-end inference,\nno NMS")
    ax.text(xh, 2.95, head_txt, ha="center", va="center", fontsize=fs - 1.0, linespacing=1.2)
    # P3, P4, P5 vào head
    poly_arrow(ax, [P["16"]["r"], (2.8, ytd[5]), (2.8, 7.05), (4.62, 7.05), (4.62, 5.1), (xh - 0.81, 5.1)], color=C_HD)
    ax.text(3.7, 7.1, "P3 (stride 8)", ha="center", va="bottom", fontsize=fs - 0.8, color=C_HD)
    poly_arrow(ax, [P["19"]["r"], (xh - 0.81, ybu[2])], color=C_HD)
    ax.text(4.7, ybu[2] + 0.06, "P4", ha="center", va="bottom", fontsize=fs - 0.8, color=C_HD)
    poly_arrow(ax, [P["22"]["r"], (xh - 0.81, ybu[5])], color=C_HD)
    ax.text(4.7, ybu[5] + 0.06, "P5", ha="center", va="bottom", fontsize=fs - 0.8, color=C_HD)

    # ô so sánh hai mô hình (góc trên bên phải)
    note = ("\n".join([
        "Hai mô hình chỉ khác nhau ở tầng 10:",
        "• Đối chứng: C2PSA (attention), 990.976 tham số",
        "• Đề xuất: C2TSVMamba, 1.811.201 tham số",
        "Các tầng còn lại giống hệt nhau.",
        "Toàn mô hình: 11.434.463 → 12.254.688 tham số"]) if vi else "\n".join([
        "The two models differ only at layer 10:",
        "• Baseline: C2PSA (attention), 990,976 params",
        "• Proposed: C2TSVMamba, 1,811,201 params",
        "All other layers are identical.",
        "Whole model: 11,434,463 → 12,254,688 params"]))
    ax.text(1.25, 11.9, note, ha="left", va="top", fontsize=fs - 0.3, linespacing=1.45,
            bbox=dict(boxstyle="round,pad=0.5", fc=F_TS, ec=C_TS, lw=0.8))
    save(fig, "a01_kien_truc_tong_the", st["lang"])


# --------------------------------------------------------------------------- a02
def a02_khoi_c2tsvmamba(st: dict) -> None:
    """Cấu trúc C2TSVMamba ở mức khối; chi tiết SS2D vẽ riêng ở a04."""
    vi = st["lang"] == "vi"
    fs = st["fs"]
    sub = fs - 0.5
    W, H = (16.0 * CM, 9.6 * CM) if vi else (18.1 * CM, 10.0 * CM)
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(-0.1, 16.5)
    ax.set_ylim(0.0, 9.0)
    ax.axis("off")
    ym = 4.5  # trục chính

    x_in = box(ax, 0.9, ym, 1.8, 0.9, "x\n512×20×20", fs=sub)
    cv1 = box(ax, 2.5, ym, 1.0, 0.9, "cv1\n1×1", ec=C_BB, fc=F_BB, fs=sub)
    arrow(ax, x_in["r"], cv1["l"])
    b = box(ax, 4.15, ym, 0.8, 0.7, "b\n256", fs=sub)
    arrow(ax, cv1["r"], b["l"])
    ax.text(3.4, ym + 0.08, "split", ha="center", va="bottom", fontsize=sub, style="italic")

    # khung TSVMamba
    ax.add_patch(FancyBboxPatch((3.55, 0.15), 11.1, 7.55, boxstyle="round,pad=0,rounding_size=0.15",
                                linewidth=1.1, edgecolor=C_TS, facecolor="none", linestyle="--", zorder=0))
    ax.text(3.7, 7.55, "TSVMamba (1 khối)" if vi else "TSVMamba (1 block)", ha="left", va="top",
            fontsize=fs, fontweight="bold", color=C_TS)

    # nhánh toàn cục
    ss = box(ax, 6.45, 6.55, 2.2, 1.0, "SS2D\n(VMamba)", ec=C_TS, fc=F_TS, fs=fs, bold=True)
    poly_arrow(ax, [b["t"], (4.15, 6.55), ss["l"]])
    mul = box(ax, 9.6, 6.55, 1.9, 0.8, r"$F_M \odot (1 + G)$", ec=C_TS, fc="white", fs=fs)
    arrow(ax, ss["r"], mul["l"])
    ax.text(8.1, 6.62, r"$F_M$", ha="center", va="bottom", fontsize=sub)

    # nhánh hình dạng cục bộ
    yh = 2.0
    sh1 = box(ax, 6.3, yh, 2.75, 1.1, "ShapeAware\nDW 3×3 ‖ DW 5×5\n" + r"→ 1×1 → $S_{shape}$",
              ec=C_SH, fc=F_SH, fs=sub)
    sh2 = box(ax, 9.6, yh, 2.95, 1.1, "Directional\nDW 1×5, 5×1, 3×3\n|∇|, 1×1 → S", ec=C_SH, fc=F_SH, fs=sub)
    poly_arrow(ax, [b["b"], (4.15, yh), sh1["l"]])
    arrow(ax, sh1["r"], sh2["l"])
    ax.text(4.95, 2.7, "Nhánh hình dạng cục bộ" if vi else "Local shape branch", ha="left", va="bottom",
            fontsize=sub, fontweight="bold", color="#9A6A00")
    gate = box(ax, 9.6, 4.3, 2.3, 0.9, "Gate\nG = σ(1×1(S))", ec=C_SH, fc=F_SH, fs=sub)
    arrow(ax, sh2["t"], gate["b"])
    arrow(ax, gate["t"], mul["b"])
    ax.text(9.72, 5.45, "G ∈ (0, 1)", ha="left", va="center", fontsize=sub)

    # hợp nhất, FFN, residual
    fuse = box(ax, 11.85, 6.55, 1.4, 0.9, "Concat S\nfuse 1×1", fs=sub)
    arrow(ax, mul["r"], fuse["l"])
    poly_arrow(ax, [sh2["r"], (11.85, yh), fuse["b"]], color="#9A6A00")
    ax.text(11.97, 3.2, "S", ha="left", va="center", fontsize=fs, color="#9A6A00")
    ffn = box(ax, 13.75, 6.55, 1.95, 0.9, "FFN\n1×1 → 1×1", fs=sub)
    arrow(ax, fuse["r"], ffn["l"])
    gam = box(ax, 13.75, 5.45, 0.75, 0.5, "× γ", ec=C_TS, fc=F_TS, fs=fs, r=0.2)
    arrow(ax, ffn["b"], gam["t"])
    add = box(ax, 13.75, ym, 0.5, 0.5, "+", ec="#111111", fc="white", fs=fs + 2, r=0.25)
    arrow(ax, gam["b"], add["t"])
    poly_arrow(ax, [(4.15, yh), (4.15, 0.55), (13.75, 0.55), add["b"]], color="#777777", ls="--")
    ax.text(9.0, 0.62, "nối tắt: b′ = b + γ·F,  γ vô hướng, khởi tạo 0,001" if vi else
            "residual: b′ = b + γ·F,  scalar γ initialised to 0.001",
            ha="center", va="bottom", fontsize=sub, color="#555555")

    # khung C2: nhánh a, concat, cv2
    cat = box(ax, 15.6, ym, 1.1, 0.9, "Concat\n512", fs=sub)
    arrow(ax, add["r"], cat["l"])
    ax.text(14.75, ym + 0.08, "b′", ha="center", va="bottom", fontsize=fs)
    poly_arrow(ax, [cv1["t"], (2.5, 8.35), (15.6, 8.35), cat["t"]])
    ax.text(9.0, 8.42, "a: 256×20×20, đi thẳng" if vi else "a: 256×20×20, identity path",
            ha="center", va="bottom", fontsize=sub)
    cv2 = box(ax, 15.6, 2.75, 1.1, 0.9, "cv2\n1×1", ec=C_BB, fc=F_BB, fs=sub)
    arrow(ax, cat["b"], cv2["t"])
    y_out = box(ax, 15.5, 1.2, 1.95, 0.8, "y\n512×20×20", fs=sub)
    arrow(ax, cv2["b"], y_out["t"])

    save(fig, "a02_khoi_c2tsvmamba", st["lang"])


# --------------------------------------------------------------------------- a04
def a04_ss2d(st: dict) -> None:
    """Các bước bên trong SS2D như cài đặt trong mã."""
    vi = st["lang"] == "vi"
    fs = st["fs"]
    sub = fs - 0.3
    W, H = (16.0 * CM, 4.6 * CM) if vi else (18.1 * CM, 4.6 * CM)
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(-0.15, 16.2)
    ax.set_ylim(-0.2, 3.75)
    ax.axis("off")
    steps = ([
        "① in_proj 1×1\n→ U, Z",
        "② DWConv 3×3\n+ SiLU",
        "③ Trải phẳng\ntheo 4 hướng",
        "④ Chiếu ra\n" + r"$\Delta_t, B_t, C_t$",
        "⑤ Quét, đọc ra\n" + r"$y_t = C_t h_t$",
        "⑥ Về lưới,\ncộng 4 hướng",
        "⑦ ⊙ SiLU(Z),\n" + r"out_proj → $F_M$",
    ] if vi else [
        "① in_proj 1×1\n→ U, Z",
        "② DWConv 3×3\n+ SiLU",
        "③ Flatten in\n4 directions",
        "④ Project to\n" + r"$\Delta_t, B_t, C_t$",
        "⑤ Scan, read out\n" + r"$y_t = C_t h_t$",
        "⑥ Fold to grid,\nsum 4 dirs",
        "⑦ ⊙ SiLU(Z),\n" + r"out_proj → $F_M$",
    ])
    w, gap, y = 2.12, 0.18, 2.0
    x = 1.0
    prev = None
    bx_list = []
    for k, txt in enumerate(steps):
        ec, fc = (C_TS, F_TS) if k in (2, 3, 4) else (C_GR, F_GR)
        bx = box(ax, x, y, w, 1.0, txt, ec=ec, fc=fc, fs=sub)
        if prev:
            arrow(ax, prev["r"], bx["l"])
        prev = bx
        bx_list.append(bx)
        x += w + gap
    x0 = bx_list[2]["l"][0] - 0.1
    x1 = bx_list[4]["r"][0] + 0.1
    ax.add_patch(FancyBboxPatch((x0, 1.35), x1 - x0, 1.95, boxstyle="round,pad=0,rounding_size=0.1",
                                linewidth=0.8, edgecolor=C_TS, facecolor="none", linestyle=":", zorder=0))
    ax.text((x0 + x1) / 2, 3.35, "lặp cho từng hướng k = 1..4, mỗi hướng có tham số riêng" if vi else
            "repeated for each direction k = 1..4 with separate parameters",
            ha="center", va="bottom", fontsize=sub, color=C_TS)
    poly_arrow(ax, [bx_list[0]["b"], (bx_list[0]["b"][0], 0.85), (bx_list[6]["b"][0], 0.85), bx_list[6]["b"]],
               color="#777777", ls="--")
    ax.text(3.6, 0.9, "Z: nhánh cổng" if vi else "Z: gating branch", ha="center", va="bottom",
            fontsize=sub, color="#555555")
    ax.text(8.0, -0.15, r"$h_t = \bar{A}_t\, h_{t-1} + \Delta_t B_t u_t,\quad "
            r"\bar{A}_t = \exp(\Delta_t A),\quad A = -\exp(A_{\log})$"
            + ("     (D = 256 kênh, N = 16 trạng thái)" if vi else "     (D = 256 channels, N = 16 states)"),
            ha="center", va="bottom", fontsize=sub, color="#333333")
    save(fig, "a04_ss2d", st["lang"])


# --------------------------------------------------------------------------- a03
def a03_quet_bon_huong(st: dict) -> None:
    """Minh họa 4 thứ tự quét của SS2D trên lưới nhỏ."""
    vi = st["lang"] == "vi"
    fs = st["fs"] + 0.5
    n = 4
    W, H = (16.0 * CM, 3.9 * CM) if vi else (8.9 * CM, 2.9 * CM)
    fig, axes = plt.subplots(1, 4, figsize=(W, H))
    titles = (["(1) hàng, xuôi", "(2) hàng, ngược", "(3) cột, xuôi", "(4) cột, ngược"] if vi else
              ["(1) rows, fwd", "(2) rows, bwd", "(3) cols, fwd", "(4) cols, bwd"])
    for k, ax in enumerate(axes):
        order = []
        for i in range(n):
            for j in range(n):
                order.append((i, j) if k < 2 else (j, i))
        if k in (1, 3):
            order = order[::-1]
        for i in range(n + 1):
            ax.plot([0, n], [i, i], color="#CCCCCC", lw=0.5)
            ax.plot([i, i], [0, n], color="#CCCCCC", lw=0.5)
        pts = [(c + 0.5, n - r - 0.5) for r, c in order]
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=C_TS, lw=0.9, zorder=2)
        ax.annotate("", xy=pts[1], xytext=pts[0],
                    arrowprops=dict(arrowstyle="-|>", color=C_TS, lw=0.9, mutation_scale=7))
        ax.scatter([pts[0][0]], [pts[0][1]], s=14, color=C_BB, zorder=3)
        ax.scatter([pts[-1][0]], [pts[-1][1]], s=14, color="#111111", marker="s", zorder=3)
        ax.set_xlim(-0.1, n + 0.1)
        ax.set_ylim(-0.1, n + 0.1)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(titles[k], fontsize=fs - 0.5, pad=3)
    fig.subplots_adjust(wspace=0.25)
    save(fig, "a03_quet_bon_huong", st["lang"])


FIGS = {"a01": a01_kien_truc_tong_the, "a02": a02_khoi_c2tsvmamba, "a03": a03_quet_bon_huong, "a04": a04_ss2d}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chi", nargs="*", default=None)
    args = ap.parse_args()
    setup()
    for key, fn in FIGS.items():
        if args.chi and key not in args.chi:
            continue
        for st in STYLE.values():
            print(key, st["lang"])
            fn(st)


if __name__ == "__main__":
    main()
