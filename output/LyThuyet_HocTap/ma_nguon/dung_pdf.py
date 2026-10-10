"""Dựng giáo trình PDF từ tệp nội dung văn bản (.txt) theo cấu hình đoạn văn của nhóm.

Cấu hình đoạn văn (theo hộp thoại Paragraph trong Word):
  Times New Roman 13 pt, căn đều hai bên, thụt dòng đầu 1,27 cm,
  cách trước 3 pt, cách sau 3 pt, giãn dòng bội số 1,37.

Cú pháp tệp nội dung (UTF-8):
  @tieu_de <dòng>          dòng tiêu đề trang bìa (có thể lặp)
  @phu_de <dòng>           dòng phụ đề trang bìa (có thể lặp)
  @so_bai <n>              số bài, dùng để đánh số hình "Hình n.k"
  # Chương ...             đề mục cấp 1 (sang trang mới)
  ## ...                   đề mục cấp 2
  ### ...                  đề mục cấp 3
  - ...                    gạch đầu dòng
  $$ ...                   công thức đặt giữa dòng
  >> ...                   hộp "Ghi nhớ" (các dòng >> liền nhau gộp thành một hộp)
  !hinh <đường dẫn> | <chú thích> | <rộng cm>
  | a | b |                bảng (dòng đầu là tiêu đề cột; hạn chế dùng)
  @ngat_trang
  ~ ...                    đoạn nối tiếp công thức, không thụt dòng đầu ("trong đó …")
  Dòng trống ngăn cách đoạn. **đậm**, *nghiêng*, _{chỉ số dưới}, ^{chỉ số trên}.

Chạy từ gốc repo:
  python output/LyThuyet_HocTap/ma_nguon/dung_pdf.py <noi_dung.txt> <dau_ra.pdf>
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[3]
FONTS = Path("C:/Windows/Fonts")

pdfmetrics.registerFont(TTFont("TNR", str(FONTS / "times.ttf")))
pdfmetrics.registerFont(TTFont("TNR-B", str(FONTS / "timesbd.ttf")))
pdfmetrics.registerFont(TTFont("TNR-I", str(FONTS / "timesi.ttf")))
pdfmetrics.registerFont(TTFont("TNR-BI", str(FONTS / "timesbi.ttf")))
pdfmetrics.registerFont(TTFont("SYM", str(FONTS / "seguisym.ttf")))
pdfmetrics.registerFontFamily("TNR", normal="TNR", bold="TNR-B", italic="TNR-I", boldItalic="TNR-BI")
TNR_GLYPHS = set(pdfmetrics.getFont("TNR").face.charToGlyph)

# ---- Cấu hình đoạn văn -------------------------------------------------------
CO_CHU = 13
GIAN_DONG = round(CO_CHU * 1.15 * 1.37, 2)  # "Bội số 1,37" theo cách Word tính dòng đơn của Times New Roman
THUT_DAU = 1.27 * cm
CACH = 3

LE_TREN, LE_DUOI, LE_TRAI, LE_PHAI = 2 * cm, 2 * cm, 3 * cm, 2 * cm
MAU_NHAN = colors.HexColor("#1f3b63")
MAU_HOP = colors.HexColor("#eef3fa")
MAU_VIEN = colors.HexColor("#2a78d6")

st_than = ParagraphStyle("than", fontName="TNR", fontSize=CO_CHU, leading=GIAN_DONG, alignment=TA_JUSTIFY,
                         firstLineIndent=THUT_DAU, spaceBefore=CACH, spaceAfter=CACH)
st_noi_tiep = ParagraphStyle("noitiep", parent=st_than, firstLineIndent=0)  # đoạn "trong đó…" nối sau công thức
st_gach = ParagraphStyle("gach", parent=st_than, firstLineIndent=0, leftIndent=THUT_DAU + 0.5 * cm,
                         bulletIndent=THUT_DAU, bulletFontName="TNR")
st_cong_thuc = ParagraphStyle("ct", parent=st_than, alignment=TA_CENTER, firstLineIndent=0,
                              spaceBefore=CACH + 3, spaceAfter=CACH + 3)
st_hop = ParagraphStyle("hop", parent=st_than, firstLineIndent=0, spaceBefore=1, spaceAfter=1)
st_chu_thich = ParagraphStyle("chuthich", parent=st_than, fontName="TNR-I", fontSize=12, leading=16,
                              alignment=TA_CENTER, firstLineIndent=0, spaceBefore=4, spaceAfter=10)
st_h1 = ParagraphStyle("h1", fontName="TNR-B", fontSize=16, leading=22, alignment=TA_CENTER,
                       spaceBefore=6, spaceAfter=16, textColor=MAU_NHAN)
st_h2 = ParagraphStyle("h2", fontName="TNR-B", fontSize=14, leading=19, alignment=TA_LEFT,
                       spaceBefore=12, spaceAfter=6, keepWithNext=1)
st_h3 = ParagraphStyle("h3", fontName="TNR-BI", fontSize=13, leading=18, alignment=TA_LEFT,
                       spaceBefore=8, spaceAfter=4, keepWithNext=1)
st_bang = ParagraphStyle("bang", fontName="TNR", fontSize=12, leading=15.5, alignment=TA_LEFT)
st_bang_dau = ParagraphStyle("bangdau", parent=st_bang, fontName="TNR-B", alignment=TA_CENTER)
st_toc1 = ParagraphStyle("toc1", fontName="TNR-B", fontSize=13, leading=19, leftIndent=0, firstLineIndent=0)
st_toc2 = ParagraphStyle("toc2", fontName="TNR", fontSize=13, leading=18, leftIndent=0.8 * cm, firstLineIndent=0)


def dinh_dang(text: str) -> str:
    """Chuyển cú pháp nhẹ sang markup của reportlab và thay font cho ký hiệu Times New Roman không có."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
    text = re.sub(r"_\{(.+?)\}", r"<sub>\1</sub>", text)
    text = re.sub(r"\^\{(.+?)\}", r"<super>\1</super>", text)
    out, in_tag = [], False
    for ch in text:
        if ch == "<":
            in_tag = True
        if not in_tag and ord(ch) > 127 and ord(ch) not in TNR_GLYPHS:
            out.append(f'<font name="SYM">{ch}</font>')
        else:
            out.append(ch)
        if ch == ">":
            in_tag = False
    return "".join(out)


class GiaoTrinh(BaseDocTemplate):
    def __init__(self, path: str, tieu_de_ngan: str):
        super().__init__(path, pagesize=A4, leftMargin=LE_TRAI, rightMargin=LE_PHAI, topMargin=LE_TREN,
                         bottomMargin=LE_DUOI, title=tieu_de_ngan, author="Nhóm đồ án DL Polyp")
        khung = Frame(LE_TRAI, LE_DUOI, A4[0] - LE_TRAI - LE_PHAI, A4[1] - LE_TREN - LE_DUOI, id="khung",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate("bia", frames=[khung]),
            PageTemplate("noi_dung", frames=[khung], onPage=self._so_trang),
        ])
        self._dem_muc = 0

    def beforeDocument(self):
        self._dem_muc = 0  # multiBuild dựng nhiều lượt; khóa đề mục phải giống nhau giữa các lượt

    @staticmethod
    def _so_trang(canv, doc):
        canv.saveState()
        canv.setFont("TNR", 12)
        canv.drawCentredString(A4[0] / 2 + (LE_TRAI - LE_PHAI) / 2, 1.1 * cm, str(doc.page))
        canv.restoreState()

    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name in ("h1", "h2"):
            muc = 0 if f.style.name == "h1" else 1
            text = f.getPlainText()
            self._dem_muc += 1
            key = f"muc{self._dem_muc}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=muc, closed=muc > 0)
            self.notify("TOCEntry", (muc, text, self.page, key))


def doc_noi_dung(path: Path):
    meta = {"tieu_de": [], "phu_de": [], "so_bai": "1"}
    khoi = []  # (loai, du_lieu)
    doan: list[str] = []
    hop: list[str] = []
    bang: list[list[str]] = []

    def xa():
        nonlocal doan, hop, bang
        if doan:
            text = " ".join(doan)
            khoi.append(("noi_tiep", text[2:]) if text.startswith("~ ") else ("doan", text))
            doan = []
        if hop:
            khoi.append(("hop", hop))
            hop = []
        if bang:
            khoi.append(("bang", bang))
            bang = []

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("@tieu_de "):
            meta["tieu_de"].append(line[9:])
        elif line.startswith("@phu_de "):
            meta["phu_de"].append(line[8:])
        elif line.startswith("@so_bai "):
            meta["so_bai"] = line[8:].strip()
        elif not line:
            xa()
        elif line.startswith(">>"):
            if doan or bang:
                xa()
            hop.append(line[2:].strip())
        elif line.startswith("|"):
            if doan or hop:
                xa()
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                bang.append(cells)
        else:
            if hop or bang:
                xa()
            for pre, loai in (("### ", "h3"), ("## ", "h2"), ("# ", "h1"), ("- ", "gach"), ("$$ ", "ct"),
                              ("!hinh ", "hinh")):
                if line.startswith(pre):
                    xa()
                    khoi.append((loai, line[len(pre):]))
                    break
            else:
                if line == "@ngat_trang":
                    xa()
                    khoi.append(("ngat", None))
                else:
                    doan.append(line)
    xa()
    return meta, khoi


def trang_bia(meta) -> list:
    st_nho = ParagraphStyle("bia_nho", fontName="TNR", fontSize=14, leading=20, alignment=TA_CENTER)
    st_lon = ParagraphStyle("bia_lon", fontName="TNR-B", fontSize=22, leading=32, alignment=TA_CENTER,
                            textColor=MAU_NHAN)
    st_phu = ParagraphStyle("bia_phu", fontName="TNR-I", fontSize=14, leading=21, alignment=TA_CENTER)
    out = [Spacer(1, 3 * cm), Paragraph("GIÁO TRÌNH TỰ HỌC", st_nho), Spacer(1, 0.4 * cm),
           Paragraph(f"BÀI {meta['so_bai']}", st_nho), Spacer(1, 1.2 * cm)]
    out += [Paragraph(dinh_dang(t), st_lon) for t in meta["tieu_de"]]
    out.append(Spacer(1, 1.2 * cm))
    out += [Paragraph(dinh_dang(t), st_phu) for t in meta["phu_de"]]
    out += [Spacer(1, 7 * cm), Paragraph("Tháng 10 năm 2026", st_nho), NextPageTemplate("noi_dung"), PageBreak()]
    return out


def muc_luc() -> list:
    toc = TableOfContents()
    toc.levelStyles = [st_toc1, st_toc2]
    toc.dotsMinLevel = 0
    return [Paragraph("MỤC LỤC", ParagraphStyle("ml", parent=st_h1)), toc, PageBreak()]


def dung(nguon: Path, dich: Path):
    meta, khoi = doc_noi_dung(nguon)
    doc = GiaoTrinh(str(dich), " ".join(meta["tieu_de"]))
    story = trang_bia(meta) + muc_luc()
    so_hinh = 0
    chuong_dau = True
    for loai, du_lieu in khoi:
        if loai == "h1":
            if not chuong_dau:
                story.append(PageBreak())
            chuong_dau = False
            story.append(Paragraph(dinh_dang(du_lieu.upper()), st_h1))
        elif loai == "h2":
            story.append(Paragraph(dinh_dang(du_lieu), st_h2))
        elif loai == "h3":
            story.append(Paragraph(dinh_dang(du_lieu), st_h3))
        elif loai == "doan":
            story.append(Paragraph(dinh_dang(du_lieu), st_than))
        elif loai == "noi_tiep":
            story.append(Paragraph(dinh_dang(du_lieu), st_noi_tiep))
        elif loai == "gach":
            story.append(Paragraph(dinh_dang(du_lieu), st_gach, bulletText="–"))
        elif loai == "ct":
            story.append(Paragraph(dinh_dang(du_lieu), st_cong_thuc))
        elif loai == "ngat":
            story.append(PageBreak())
        elif loai == "hop":
            noi_dung = [Paragraph("<b>Ghi nhớ</b>", st_hop)] + [Paragraph(dinh_dang(t), st_hop) for t in du_lieu]
            t = Table([[noi_dung]], colWidths=[A4[0] - LE_TRAI - LE_PHAI])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), MAU_HOP),
                ("LINEBEFORE", (0, 0), (0, -1), 3, MAU_VIEN),
                ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]))
            story += [Spacer(1, 4), t, Spacer(1, 6)]
        elif loai == "bang":
            rong = A4[0] - LE_TRAI - LE_PHAI
            so_cot = len(du_lieu[0])
            rows = [[Paragraph(dinh_dang(c), st_bang_dau if i == 0 else st_bang) for c in r] for i, r in enumerate(du_lieu)]
            t = Table(rows, colWidths=[rong / so_cot] * so_cot, repeatRows=1)
            t.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#8a8a8a")),
                ("BACKGROUND", (0, 0), (-1, 0), MAU_HOP),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story += [Spacer(1, 4), t, Spacer(1, 8)]
        elif loai == "hinh":
            duong_dan, chu_thich, rong_cm = [p.strip() for p in du_lieu.split("|")]
            anh = ROOT / duong_dan
            w, h = PILImage.open(anh).size
            if anh.stat().st_size > 600_000:  # ảnh nội soi: nhúng JPEG chất lượng cao cho nhẹ tệp
                tam = Path(tempfile.gettempdir()) / f"giaotrinh_{anh.stem}.jpg"
                PILImage.open(anh).convert("RGB").save(tam, quality=90)
                anh = tam
            rong = float(rong_cm) * cm
            so_hinh += 1
            story.append(KeepTogether([
                Spacer(1, 6),
                Image(str(anh), width=rong, height=rong * h / w),
                Paragraph(dinh_dang(f"Hình {meta['so_bai']}.{so_hinh}. {chu_thich}"), st_chu_thich),
            ]))
    doc.multiBuild(story)
    print("đã tạo", dich)


if __name__ == "__main__":
    dung(Path(sys.argv[1]), Path(sys.argv[2]))
