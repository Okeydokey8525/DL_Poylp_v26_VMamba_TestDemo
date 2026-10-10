"""Build the preprocessing flow as an editable .drawio file and a matching PNG."""
import sys
from pathlib import Path
from xml.sax.saxutils import escape
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)

# id: (x, y, w, h, text, fill, stroke)  -- draw.io pixel coordinates, y grows downward
SRC, PROC, DATA, MODEL = ("#DAE8FC", "#6C8EBF"), ("#FFFFFF", "#555555"), ("#D5E8D4", "#82B366"), ("#FFE6CC", "#D79B00")
N = {
    "kv":  (40, 50, 300, 50, "Kvasir-SEG\n1.000 ảnh polyp và mặt nạ", *SRC),
    "nc":  (400, 50, 260, 50, "Kvasir, lớp normal-cecum\n1.000 ảnh không có polyp", *SRC),
    "cv":  (40, 140, 300, 70, "Chuyển mặt nạ thành đa giác\nOtsu → phép đóng → đường bao\n→ đơn giản hóa → chuẩn hóa tọa độ", *PROC),
    "bg":  (400, 140, 260, 70, "Chọn ngẫu nhiên 200 ảnh, seed 42\nChia 160 huấn luyện / 40 kiểm định\nTạo tệp nhãn rỗng", *PROC),
    "ds":  (190, 250, 320, 50, "Bộ dữ liệu BG20 định dạng YOLO\nHuấn luyện 1.040 ảnh, kiểm định 160 ảnh", *DATA),
    "tr":  (40, 360, 300, 70, "Nhánh huấn luyện\nĐổi kích thước → tăng cường dữ liệu\n→ định dạng và chuẩn hóa", *PROC),
    "va":  (400, 360, 260, 70, "Nhánh kiểm định\nĐổi kích thước → LetterBox\n→ định dạng và chuẩn hóa", *PROC),
    "md":  (190, 470, 320, 45, "Mô hình YOLO26-seg + TSVM", *MODEL),
}
E = [("kv", "cv"), ("nc", "bg"), ("cv", "ds"), ("bg", "ds"), ("ds", "tr"), ("ds", "va"), ("tr", "md"), ("va", "md")]
GROUPS = [(8, 30, 672, 285, "Chuẩn bị trước huấn luyện"),
          (8, 345, 672, 100, "Khi nạp dữ liệu")]

# ---------- draw.io ----------
cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
for k, (x, y, w, h, t) in enumerate(GROUPS):
    cells.append(f'<mxCell id="g{k}" value="{escape(t)}" style="rounded=1;arcSize=4;dashed=1;fillColor=none;strokeColor=#999999;'
                 f'horizontal=0;verticalAlign=top;align=center;spacingTop=2;fontFamily=Times New Roman;fontSize=12;fontStyle=2;" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
for nid, (x, y, w, h, t, f, s) in N.items():
    v = escape(t).replace("\n", "&#xa;")
    cells.append(f'<mxCell id="{nid}" value="{v}" style="rounded=1;whiteSpace=wrap;html=0;fillColor={f};strokeColor={s};'
                 f'fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
for k, (a, b) in enumerate(E):
    cells.append(f'<mxCell id="e{k}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=block;endFill=1;strokeColor=#333333;" '
                 f'edge="1" parent="1" source="{a}" target="{b}"><mxGeometry relative="1" as="geometry"/></mxCell>')
xml = ('<mxfile host="app.diagrams.net"><diagram name="Tien xu ly BG20"><mxGraphModel dx="800" dy="600" grid="1" gridSize="10" '
       'page="1" pageWidth="720" pageHeight="560"><root>' + "".join(cells) + "</root></mxGraphModel></diagram></mxfile>")
(OUT / "hinh_3_5_quy_trinh.drawio").write_text(xml, encoding="utf-8")

# ---------- PNG ----------
plt.rcParams["font.family"] = "Times New Roman"
W, H = 700, 535
fig = plt.figure(figsize=(W / 88, H / 88)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
for x, y, w, h, t in GROUPS:
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=8", fill=False, ec="#999999", ls="--", lw=1))
    ax.text(x + 14, y + h / 2, t, fontsize=10, style="italic", color="#555555", va="center", ha="center", rotation=90)
for x, y, w, h, t, f, s in N.values():
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=8", fc=f, ec=s, lw=1.2))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=11, linespacing=1.3)


def arrow(p, q):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.2, shrinkA=0, shrinkB=0))


def c(n, side):
    x, y, w, h = N[n][:4]
    return {"b": (x + w / 2, y + h), "t": (x + w / 2, y)}[side]


arrow(c("kv", "b"), c("cv", "t")); arrow(c("nc", "b"), c("bg", "t"))
for src, dst in [("cv", "ds"), ("bg", "ds")]:
    (sx, sy), (dx, dy) = c(src, "b"), c(dst, "t")
    mid = (sy + dy) / 2
    ax.plot([sx, sx, dx], [sy, mid, mid], color="#333333", lw=1.2); arrow((dx, mid), (dx, dy))
for dst in ["tr", "va"]:
    (sx, sy), (dx, dy) = c("ds", "b"), c(dst, "t")
    mid = (sy + dy) / 2 + 8
    ax.plot([sx, sx, dx], [sy, mid, mid], color="#333333", lw=1.2); arrow((dx, mid), (dx, dy))
for src in ["tr", "va"]:
    (sx, sy), (dx, dy) = c(src, "b"), c("md", "t")
    mid = (sy + dy) / 2
    ax.plot([sx, sx, dx], [sy, mid, mid], color="#333333", lw=1.2); arrow((dx, mid), (dx, dy))
fig.savefig(OUT / "hinh_3_5_quy_trinh.png", dpi=200, bbox_inches="tight", pad_inches=0.05)
print("ok")
