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
    d = OUT / "chung" / lang
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


# --------------------------------------------------------------------------- s01
def s01_kien_truc_ung_dung(st: dict) -> None:
    """Hình 5.2: kiến trúc hệ thống PolypVision (cổng và endpoint lấy từ mã nguồn Ung_Dung/polypweb)."""
    vi = st["lang"] == "vi"
    fs = st["fs"] + (0.8 if vi else 0.0)
    W, H = (16.0 * CM, 6.4 * CM) if vi else (8.9 * CM, 4.6 * CM)
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, 12.6)
    ax.set_ylim(-0.4, 5.0)
    ax.axis("off")
    t = (lambda a, b: a if vi else b)

    br = box(ax, 1.2, 3.0, 2.0, 0.9, t("Trình duyệt\n(Web)", "Browser\n(Web)"), fs=fs)
    sp = box(ax, 4.4, 3.0, 2.8, 0.9, t("Spring Boot Web\n(cổng 8080)", "Spring Boot Web\n(port 8080)"),
             ec=C_BB, fc=F_BB, fs=fs, bold=True)
    mg = box(ax, 3.4, 4.5, 1.8, 0.7, "MongoDB", fs=fs - 0.3)
    st_ = box(ax, 5.5, 4.5, 2.0, 0.7, t("Kho tệp ảnh\n(storage/)", "Image storage\n(storage/)"), fs=fs - 0.3)
    fl = box(ax, 1.2, 0.9, 2.0, 0.9, t("Flutter Mobile", "Flutter Mobile"), fs=fs)
    ai = box(ax, 8.4, 1.95, 2.2, 3.1, t("FastAPI\ndịch vụ suy luận\n(cổng 8000)\n\nvẽ mặt nạ,\nhộp bao,\nđường viền",
                                        "FastAPI\ninference service\n(port 8000)\n\nmask, box,\noutline"),
             ec=C_TS, fc=F_TS, fs=fs, bold=False)
    m1 = box(ax, 11.4, 2.8, 2.1, 0.8, "YOLO26s-seg", ec=C_NK, fc=F_NK, fs=fs - 0.2)
    m2 = box(ax, 11.4, 1.1, 2.1, 0.8, "YOLO26s-seg\n+ TSVM (FP32)", ec=C_TS, fc=F_TS, fs=fs - 0.2)

    hd = 8.0
    arrow(ax, br["r"], sp["l"], head=hd)
    arrow(ax, (sp["t"][0] - 0.6, sp["t"][1]), mg["b"], head=hd)
    arrow(ax, (sp["t"][0] + 0.6, sp["t"][1]), st_["b"], head=hd)
    arrow(ax, sp["r"], (ai["l"][0], sp["r"][1]), head=hd)
    arrow(ax, fl["r"], (ai["l"][0], fl["r"][1]), head=hd)
    arrow(ax, (ai["r"][0], m1["l"][1]), m1["l"], head=hd)
    arrow(ax, (ai["r"][0], m2["l"][1]), m2["l"], head=hd)
    lab = dict(ha="center", va="bottom", fontsize=fs - 1.2, color="#333333")
    ax.text((sp["r"][0] + ai["l"][0]) / 2, sp["r"][1] + 0.08, "POST /predict", **lab)
    ax.text((fl["r"][0] + ai["l"][0]) / 2, fl["r"][1] + 0.08, "POST /api/v1/inference, /comparison", **lab)
    ax.text(1.2, 2.05, t("có tài khoản,\nlưu lịch sử", "accounts,\nhistory"), ha="center", va="center",
            fontsize=fs - 1.2, color="#555555")
    ax.text(1.2, -0.05, t("không tài khoản,\nkhông lưu ảnh", "no account,\nno storage"), ha="center", va="center",
            fontsize=fs - 1.2, color="#555555")
    save(fig, "s01_kien_truc_ung_dung", st["lang"])


# --------------------------------------------------------------------------- a05–a08: hình cho slide (khổ 16:9)
SLIDE = (16.0 * CM, 9.0 * CM)


def _luoi(ax, x0, y0, o, n, to, mau, nhan, fs):
    """Lưới n×n ô cạnh o, tô các ô trong `to` (hàng, cột) bằng `mau`; nhãn ở dưới."""
    for i in range(n):
        for j in range(n):
            fc = mau if (i, j) in to else "white"
            ax.add_patch(FancyBboxPatch((x0 + j * o, y0 + (n - 1 - i) * o), o, o, boxstyle="square,pad=0",
                                        linewidth=0.5, edgecolor="#AAAAAA", facecolor=fc, zorder=2))
    ax.text(x0 + n * o / 2, y0 - 0.2, nhan, ha="center", va="top", fontsize=fs)


def a05_nhanh_hinh_dang(st: dict) -> None:
    """Slide: nhân có hướng của nhánh hình dạng, luồng tính S và cổng (1 + G)."""
    vi = st["lang"] == "vi"
    t = (lambda a, b: a if vi else b)
    fs = 8.0
    fig, ax = plt.subplots(figsize=SLIDE)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # hàng 1: các nhân tích chập theo chiều sâu, minh họa trên vùng 5×5
    ax.text(0.2, 8.75, t("① Các nhân tích chập theo chiều sâu (vùng 5×5 quanh một vị trí)",
                         "① Depthwise kernels (5×5 neighbourhood of one position)"),
            fontsize=fs + 0.5, fontweight="bold", va="top")
    o, y0 = 0.32, 5.85
    tam = [(2, j) for j in range(5)]
    _luoi(ax, 0.6, y0, o, 5, {(i, j) for i in range(1, 4) for j in range(1, 4)}, F_GR, "3×3", fs)
    _luoi(ax, 2.9, y0, o, 5, {(i, j) for i in range(5) for j in range(5)}, F_SH, "5×5", fs)
    _luoi(ax, 5.8, y0, o, 5, set(tam), "#F5C77E", t("1×5: ngang", "1×5: horizontal"), fs)
    _luoi(ax, 8.1, y0, o, 5, {(i, 2) for i in range(5)}, "#9CC8E6", t("5×1: dọc", "5×1: vertical"), fs)
    ax.text(1.9, 8.05, "ShapeAware", ha="center", fontsize=fs, color="#9A6A00", fontweight="bold")
    ax.text(7.75, 8.05, "Directional", ha="center", fontsize=fs, color="#9A6A00", fontweight="bold")
    ax.text(10.3, 6.65, t("Ở mức P5 (bước 32), nhân 1×5\nphủ khoảng 160 pixel ảnh gốc:\n"
                          "hình dạng ở mức vùng,\nkhông phải biên từng pixel.",
                          "At P5 (stride 32) a 1×5 kernel\ncovers about 160 input pixels:\n"
                          "region-level shape,\nnot pixel-level boundary."),
            fontsize=fs - 0.5, va="center", color="#444444",
            bbox=dict(boxstyle="round,pad=0.35", fc="#FAFAFA", ec="#BBBBBB", lw=0.6))

    # hàng 2: luồng tính S
    ax.text(0.2, 5.05, t("② Luồng tính đặc trưng hình dạng S", "② Computing the shape feature S"),
            fontsize=fs + 0.5, fontweight="bold", va="top")
    yr, f2 = 4.0, fs - 1.5
    b = box(ax, 0.55, yr, 0.85, 0.8, "b\n256", fs=f2)
    s1 = box(ax, 2.65, yr, 2.9, 1.0, "DW 3×3 ‖ DW 5×5\n→ 1×1 → $S_{shape}$", ec=C_SH, fc=F_SH, fs=f2)
    s2 = box(ax, 6.9, yr, 5.1, 1.0, "$S_h$ (1×5),  $S_v$ (5×1),  $S_{loc}$ (3×3)\n"
             "$S_{grad}=\\sqrt{S_h^2+S_v^2}$", ec=C_SH, fc=F_SH, fs=f2)
    s3 = box(ax, 11.3, yr, 3.2, 1.0, t("ghép 4 → 1×1,\nghép với $S_{shape}$ → 1×1", "concat 4 → 1×1,\n"
                                      "concat $S_{shape}$ → 1×1"), ec=C_SH, fc=F_SH, fs=f2)
    s = box(ax, 13.7, yr, 0.8, 0.8, "S", ec=C_SH, fc="white", fs=fs + 2, bold=True)
    for p, q in ((b, s1), (s1, s2), (s2, s3), (s3, s)):
        arrow(ax, p["r"], q["l"], head=6)

    # hàng 3: cổng (G đặt ngay dưới S)
    ax.text(0.2, 2.95, t("③ Cổng: nhánh hình dạng điều biến đầu ra SS2D (một chiều)",
                         "③ Gate: the shape branch modulates SS2D (one-way)"),
            fontsize=fs + 0.5, fontweight="bold", va="top")
    yg = 1.75
    fm = box(ax, 1.4, yg, 2.2, 0.75, "$F_M$ (SS2D)", ec=C_TS, fc=F_TS, fs=f2)
    mul = box(ax, 5.6, yg, 3.4, 0.8, "$F'_M = F_M\\odot(1+G)$", ec=C_TS, fc="white", fs=fs)
    g = box(ax, 13.7, yg, 4.4, 0.9, "$G=\\sigma(W_g * S + b_g)$\n$G\\in(0,1)$", ec=C_SH, fc=F_SH, fs=f2)
    arrow(ax, s["b"], g["t"], color="#9A6A00", head=6)
    arrow(ax, fm["r"], mul["l"], head=6)
    arrow(ax, g["l"], mul["r"], color="#9A6A00", head=6)
    # trục hệ số 1 + G: nhãn ở trên, vạch số ở dưới
    x1, x2, ya = 5.0, 11.0, 0.55
    ax.plot([x1 - 0.8, x2 + 0.5], [ya, ya], color="#999999", lw=0.8)
    ax.add_patch(FancyBboxPatch((x1, ya - 0.12), x2 - x1, 0.24, boxstyle="round,pad=0,rounding_size=0.11",
                                linewidth=0, facecolor="#F5C77E", zorder=2))
    for xv, lab in ((x1 - 0.8, "0"), (x1, "1"), (x2, "2")):
        ax.plot([xv, xv], [ya - 0.18, ya + 0.18], color="#555555", lw=0.8)
        ax.text(xv, ya - 0.22, lab, ha="center", va="top", fontsize=f2)
    ax.text((x1 + x2) / 2, ya + 0.25, t("1 + G ∈ (1, 2): chỉ khuếch đại, không tắt hẳn vị trí nào",
                                        "1 + G ∈ (1, 2): only amplifies, never switches a position off"),
            ha="center", va="bottom", fontsize=f2, color="#9A6A00", fontweight="bold")
    save(fig, "a05_nhanh_hinh_dang_cong", st["lang"])


def a06_quet_song_song(st: dict) -> None:
    """Slide: ví dụ quét kết hợp song song Hillis–Steele trên chuỗi L = 4 (số liệu như Bảng PL.9)."""
    vi = st["lang"] == "vi"
    t = (lambda a, b: a if vi else b)
    fs = 8.0
    fig, ax = plt.subplots(figsize=SLIDE)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.text(0.2, 8.8, t("Truy hồi  $h_t = a_t\\,h_{t-1} + b_t$   →   ghép hai bước:  "
                        "$(a_1,b_1)\\circ(a_2,b_2) = (a_2a_1,\\ a_2b_1 + b_2)$",
                        "Recurrence  $h_t = a_t\\,h_{t-1} + b_t$   →   combine two steps:  "
                        "$(a_1,b_1)\\circ(a_2,b_2) = (a_2a_1,\\ a_2b_1 + b_2)$"),
            fontsize=fs + 0.5, va="top")
    rows = [
        (t("Ban đầu", "Start"), ["0,5; 1", "0,8; 2", "0,5; 0", "0,9; 1"] if vi else ["0.5; 1", "0.8; 2", "0.5; 0", "0.9; 1"]),
        (t("Vòng 1\nstep = 1", "Round 1\nstep = 1"), ["0,5; 1", "0,4; 2,8", "0,4; 1", "0,45; 1"] if vi else
         ["0.5; 1", "0.4; 2.8", "0.4; 1", "0.45; 1"]),
        (t("Vòng 2\nstep = 2", "Round 2\nstep = 2"), ["0,5; 1", "0,4; 2,8", "0,2; 1,4", "0,18; 2,26"] if vi else
         ["0.5; 1", "0.4; 2.8", "0.2; 1.4", "0.18; 2.26"]),
    ]
    xs = [2.95, 4.85, 6.75, 8.65]
    ys = [6.9, 4.6, 2.3]
    for k, x in enumerate(xs):
        ax.text(x, 7.85, t(f"vị trí {k + 1}", f"position {k + 1}"), ha="center", fontsize=fs, color="#555555")
    bx = {}
    for r, ((lab, vals), y) in enumerate(zip(rows, ys)):
        ax.text(0.15, y, lab, ha="left", va="center", fontsize=fs - 0.5, fontweight="bold")
        for k, (x, v) in enumerate(zip(xs, vals)):
            done = (r == 1 and k == 1) or r == 2
            bx[r, k] = box(ax, x, y, 1.8, 0.75, f"({v})", ec=C_TS if done else C_GR,
                           fc=F_TS if done else F_GR, fs=fs - 1.3)
    # mũi tên: vòng 1 từ t−1, vòng 2 từ t−2; mũi tên thẳng là giữ giá trị của chính nó
    for r, step in ((1, 1), (2, 2)):
        for k in range(4):
            arrow(ax, bx[r - 1, k]["b"], bx[r, k]["t"], color="#AAAAAA", head=5)
            if k - step >= 0:
                arrow(ax, (bx[r - 1, k - step]["b"][0] + 0.3, bx[r - 1, k - step]["b"][1]),
                      (bx[r, k]["t"][0] - 0.3, bx[r, k]["t"][1]), color=C_TS, lw=0.9, head=5)
    ax.text(5.6, 1.3, t("$h$ = (1; 2,8; 1,4; 2,26): trùng với tính tuần tự",
                        "$h$ = (1; 2.8; 1.4; 2.26): same as sequential"),
            ha="center", fontsize=fs - 0.8, color=C_TS, fontweight="bold")
    ax.text(5.8, 0.7, t("mũi tên cam: kết hợp với vị trí t − step\nô cam: đã gom đủ các phần tử đứng trước",
                        "orange arrow: combine with position t − step\norange box: prefix complete"),
            ha="center", va="center", fontsize=fs - 1.0, color="#555555")
    # khung so sánh với chuỗi thật L = 400
    ax.add_patch(FancyBboxPatch((10.3, 1.0), 5.4, 6.9, boxstyle="round,pad=0,rounding_size=0.15",
                                linewidth=0.8, edgecolor="#BBBBBB", facecolor="#FAFAFA", zorder=0))
    ax.text(13.0, 7.45, t("Tầng 10: L = 400\n(đệm lên 512)", "Layer 10: L = 400\n(padded to 512)"),
            ha="center", va="center", fontsize=fs, fontweight="bold")
    big = dict(ha="center", fontsize=fs + 9, fontweight="bold")
    ax.text(11.75, 5.75, "399", color=C_GR, **big)
    ax.text(14.25, 5.75, "9", color=C_TS, **big)
    ax.text(11.75, 5.2, t("bước nối tiếp\n(tuần tự)", "serial steps\n(sequential)"), ha="center", va="top", fontsize=fs)
    ax.text(14.25, 5.2, t("vòng\n(song song)", "rounds\n(parallel)"), ha="center", va="top", fontsize=fs)
    ax.text(11.75, 2.95, "399", color=C_GR, ha="center", fontsize=fs + 5, fontweight="bold")
    ax.text(14.25, 2.95, "4.097" if vi else "4,097", color=C_TS, ha="center", fontsize=fs + 5, fontweight="bold")
    ax.text(13.0, 2.55, t("phép kết hợp mỗi chuỗi\n→ tổng công việc O(L log L),\nkhoảng 67 triệu phép mỗi ảnh",
                          "combines per sequence\n→ total work O(L log L),\nabout 67 million per image"),
            ha="center", va="top", fontsize=fs - 0.3)
    save(fig, "a06_quet_song_song", st["lang"])


def a07_che_do_tach_thanh_phan(st: dict) -> None:
    """Slide: bốn chế độ của khối TSVMamba; thành phần bị bỏ vẽ nét đứt, màu xám."""
    vi = st["lang"] == "vi"
    t = (lambda a, b: a if vi else b)
    fs = 7.6
    fig, axes = plt.subplots(1, 4, figsize=SLIDE)
    modes = [
        (t("Đầy đủ", "Full"), "topology_shape_vmamba", (1, 1, 1), "1.811.201" if vi else "1,811,201"),
        (t("Bỏ cổng", "No gate"), "shape_vmamba_no_guidance", (1, 1, 0), "1.745.409" if vi else "1,745,409"),
        (t("Chỉ SS2D", "SS2D only"), "vmamba_only", (1, 0, 0), "1.071.873" if vi else "1,071,873"),
        (t("Chỉ hình dạng", "Shape only"), "shape_only", (0, 1, 0), "1.331.969" if vi else "1,331,969"),
    ]
    off = dict(ec="#BBBBBB", fc="white", ls="--", color="#AAAAAA")
    for ax, (ten, ma, (ss, sh, cg), ts) in zip(axes, modes):
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 9)
        ax.axis("off")
        ax.text(2, 8.7, ten, ha="center", va="top", fontsize=fs + 2, fontweight="bold")
        ax.text(2, 8.0, ma, ha="center", va="top", fontsize=fs - 1.6, family="monospace", color="#555555")
        b = box(ax, 2, 7.0, 1.0, 0.6, "b", fs=fs)
        kw_ss = dict(ec=C_TS, fc=F_TS) if ss else off
        kw_sh = dict(ec=C_SH, fc=F_SH) if sh else off
        kw_cg = dict(ec=C_SH, fc="white") if cg else off
        bss = box(ax, 1.0, 5.6, 1.6, 0.8, "SS2D", fs=fs, **kw_ss)
        bsh = box(ax, 3.0, 5.6, 1.6, 0.8, t("Hình dạng", "Shape"), fs=fs, **kw_sh)
        bcg = box(ax, 2.0, 4.3, 1.6, 0.7, t("Cổng 1+G", "Gate 1+G"), fs=fs, **kw_cg)
        fuse_on = ss and sh
        bfu = box(ax, 2.0, 3.0, 1.6, 0.7, "fuse 1×1", fs=fs, **(dict() if fuse_on else off))
        bff = box(ax, 2.0, 1.85, 1.6, 0.7, "FFN · γ", fs=fs)
        for p, on in ((bss, ss), (bsh, sh)):
            arrow(ax, b["b"], p["t"], color=C_ARROW if on else "#CCCCCC", ls="-" if on else "--", head=5)
        if cg:
            arrow(ax, bsh["b"], bcg["r"], color="#9A6A00", head=5)
            arrow(ax, (bsh["b"][0] + 0.5, bsh["b"][1]), bfu["r"], cs="arc3,rad=-0.2", color="#9A6A00", head=5)
            arrow(ax, bss["b"], bcg["l"], color=C_TS, head=5)
            arrow(ax, bcg["b"], bfu["t"], head=5)
        elif fuse_on:
            arrow(ax, bss["b"], bfu["l"], cs="arc3,rad=0.25", head=5)
            arrow(ax, bsh["b"], bfu["r"], cs="arc3,rad=-0.25", head=5)
        else:
            src = bss if ss else bsh
            arrow(ax, src["b"], bff["t"], cs="arc3,rad=0.2" if ss else "arc3,rad=-0.2", head=5)
        if fuse_on:
            arrow(ax, bfu["b"], bff["t"], head=5)
        ax.text(2, 0.95, t("Tham số tầng 10", "Layer-10 params"), ha="center", va="center", fontsize=fs - 0.8,
                color="#555555")
        ax.text(2, 0.4, ts, ha="center", va="center", fontsize=fs + 1.5, fontweight="bold",
                color=C_TS if ma == "topology_shape_vmamba" else "#222222")
    fig.subplots_adjust(wspace=0.08, left=0.01, right=0.99)
    save(fig, "a07_che_do_tach_thanh_phan", st["lang"])


def a08_uu_nhuoc_diem(st: dict) -> None:
    """Slide: ưu và nhược điểm của mô hình đề xuất (nội dung mục 3.6), dạng thẻ."""
    vi = st["lang"] == "vi"
    t = (lambda a, b: a if vi else b)
    fs = 8.0
    fig, ax = plt.subplots(figsize=SLIDE)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")
    uu = [
        t("Chỉ thay 1 tầng,\ngiao diện 512×20×20 giữ nguyên", "Only one layer changed,\n512×20×20 interface kept"),
        t("Ngữ cảnh toàn cục có chọn lọc:\nquét 4 hướng", "Selective global context:\n4-direction scan"),
        t("Kênh riêng cho thông tin hình dạng\n(nhân 1×5, 5×1 và cổng)", "Dedicated shape path\n(1×5, 5×1 kernels and gate)"),
        t("Khởi đầu ổn định: γ = 0,001,\nkế thừa cv1, cv2, FFN từ C2PSA", "Stable start: γ = 0.001,\ninherits cv1, cv2, FFN"),
        t("Chỉ cần PyTorch:\nchạy CPU/GPU, kết quả tất định", "PyTorch only:\nCPU/GPU, deterministic"),
    ]
    nh = [
        t("Tham số +7,17%;\ncheckpoint FP32 lớn hơn", "Parameters +7.17%;\nlarger FP32 checkpoint"),
        t("Độ trễ CPU khoảng 2,1 lần", "CPU latency about 2.1×"),
        t("Huấn luyện khoảng 2,3 → 4,7 giờ\nmỗi lượt", "Training about 2.3 → 4.7 h\nper run"),
        t("Quét O(L log L),\nnhiều tensor trung gian", "O(L log L) scan,\nmany intermediate tensors"),
        t("Ở P5 (L = 400),\nlợi thế của SSM chưa thể hiện", "At P5 (L = 400),\nthe SSM advantage does not show"),
    ]
    for x0, tieu_de, ds, ec, fc, ky in ((0.3, t("Ưu điểm", "Strengths"), uu, C_NK, F_NK, "✓"),
                                        (8.2, t("Hạn chế", "Limitations"), nh, C_TS, F_TS, "✗")):
        ax.text(x0 + 3.75, 8.6, tieu_de, ha="center", va="top", fontsize=fs + 4, fontweight="bold", color=ec)
        for k, s in enumerate(ds):
            y = 7.0 - k * 1.45
            ax.add_patch(FancyBboxPatch((x0, y - 0.55), 7.5, 1.1, boxstyle="round,pad=0,rounding_size=0.15",
                                        linewidth=0.9, edgecolor=ec, facecolor=fc, zorder=1))
            ax.text(x0 + 0.5, y, ky, ha="center", va="center", fontsize=fs + 6, color=ec, fontweight="bold")
            ax.text(x0 + 1.0, y, s, ha="left", va="center", fontsize=fs)
    save(fig, "a08_uu_nhuoc_diem", st["lang"])


FIGS = {"a01": a01_kien_truc_tong_the, "a02": a02_khoi_c2tsvmamba, "a03": a03_quet_bon_huong, "a04": a04_ss2d,
        "s01": s01_kien_truc_ung_dung, "a05": a05_nhanh_hinh_dang, "a06": a06_quet_song_song,
        "a07": a07_che_do_tach_thanh_phan, "a08": a08_uu_nhuoc_diem}


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
