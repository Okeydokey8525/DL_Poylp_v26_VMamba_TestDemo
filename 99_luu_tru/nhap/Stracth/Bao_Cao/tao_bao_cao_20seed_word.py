"""Ban Word cua bao cao 20 seed, cung noi dung va bo cuc voi tao_bao_cao_20seed_pdf.py (mau formatThang).

    python archive/Stracth/Bao_Cao/tao_bao_cao_20seed_word.py

Lay HTML tu tao_bao_cao_20seed_pdf.py, doi font sang Times New Roman / Arial (DejaVu khong cai tren Windows),
mo bang Word (COM) roi nhung anh, ke bang kieu booktabs, danh so trang va luu .docx.
Ghi archive/Bao_cao/CNTT_KLCN182_BaoCao_20Seed_FP32_formatThang.docx (khong ghi de).
"""
import re
import sys
import tempfile
from pathlib import Path

import win32com.client
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tao_bao_cao_20seed_pdf as rep  # noqa: E402

OUT = rep.ROOT / "Bao_cao" / "CNTT_KLCN182_BaoCao_20Seed_FP32_formatThang.docx"
TEXT_WIDTH_PX = 635  # 168 mm text block at 96 px/in
FONT_SCALE = 1.15  # Times New Roman runs smaller than DejaVu Serif at the same size
WORD_CSS = """
p.figcap, div.cap { font-family: Arial; font-size: 9pt; text-align: left; margin: 0 0 3pt; }
p.figcap { margin: 0 0 7pt; }
table.info td { padding: 0; }
table.info p { margin: 0; }
.sign { margin-top: 10pt; }
div.fig { text-align: center; margin: 8pt 0 2pt; }
"""


def scale_sizes(css):
    return re.sub(r"(font(?:-size)?:\s*(?:bold\s+)?)(\d+(?:\.\d+)?)pt",
                  lambda mt: f"{mt[1]}{float(mt[2]) * FONT_SCALE:.1f}pt", css)


def bold_first_column(html, marker):
    """Bold the first cell of every row in the table that follows each marker (Word ignores :first-child)."""
    parts = html.split(marker)
    for i in range(1, len(parts)):
        end = parts[i].index("</table>")
        head = parts[i][:end].replace('<tr><td class="l">', '<tr><td class="l" style="font-weight:bold">')
        parts[i] = head + parts[i][end:]
    return marker.join(parts)


IMG_SIZES = []  # (width_pt, height_pt) per figure, in document order


def img_tag(mt):
    """Word needs both pixel dimensions, otherwise it keeps the source height and stretches the figure."""
    w, h = Image.open(Path.from_uri(mt[1])).size
    width = TEXT_WIDTH_PX * int(mt[2]) / 100
    IMG_SIZES.append((width * 0.75, width * h / w * 0.75))
    return f'<img src="{mt[1]}" width="{int(width)}" height="{int(width * h / w)}">'


def word_html(doc):
    css_start, css_end = doc.index("<style>") + 7, doc.index("</style>")
    css = doc[css_start:css_end]
    css = re.sub(r"@font-face \{[^}]*\}\s*", "", css)
    css = re.sub(r"@page \{[^}]*\{[^}]*\}\s*\}\s*", "", css)
    css = css.replace('"DVSerif", serif', '"Times New Roman", serif').replace('"DVSerif"', '"Times New Roman"')
    css = css.replace('"DVSans"', "Arial")
    css = re.sub(r"border-(?:top|bottom): 1px solid #333;", "", css)
    css = css.replace("border-bottom: .6px solid #333;", "").replace("border-top: .6px solid #333;", "")
    css = css.replace(".r { color: #d04545; }", ".red { color: #d04545; }")
    html = doc[:css_start] + scale_sizes(css) + WORD_CSS + doc[css_end:]
    html = html.replace('<b class="r">', '<b class="red">')
    html = re.sub(r'<span class="n">([\d.]+)</span>', r'\1&nbsp;&nbsp;', html)  # Word drops span margins

    html = html.replace(' style="break-before:page"', '')  # Word layout is longer; no forced break
    for marker in ('<div class="tbl kq">', '<div class="kq">'):
        html = bold_first_column(html, marker)
    for cls, align in (("l", "left"), ("c", "center"), ("r", "right"), ("j", "justify")):
        for tag in ("td", "th"):
            html = html.replace(f'<{tag} class="{cls}">', f'<{tag} class="{cls}" style="text-align:{align}">')
    # info table: navy sans labels
    s, e = html.index('<table class="info">'), html.index("</table>", html.index('<table class="info">'))
    info = html[s:e].replace("<tr><td>", '<tr><td style="font-family:Arial;font-weight:bold;color:#17325c;'
                                            'font-size:9.4pt;width:24%;vertical-align:bottom">')
    html = html[:s] + info + html[e:]
    # bold "Toan bo" totals row
    html = re.sub(r'<tr class="last">(.*?)</tr>',
                  lambda mt: '<tr class="last">' + mt[1].replace('style="text-align:right"',
                                                                 'style="text-align:right;font-weight:bold"') + "</tr>",
                  html)
    # figures: Word does not know <figure>, and needs pixel widths
    html = html.replace("<figure>", '<div class="fig">').replace("</figure>", "</div>")
    html = html.replace("<figcaption>", '<p class="figcap">').replace("</figcaption>", "</p>")
    html = re.sub(r'<img src="([^"]+)" style="width:(\d+)%">', img_tag, html)
    return rule_tables(html)


THICK, THIN = "solid windowtext 1.0pt", "solid windowtext .5pt"


def add_style(cell_open, css):
    if 'style="' in cell_open:
        return cell_open.replace('style="', f'style="{css};', 1)
    return cell_open[:-1] + f' style="{css}">'


def style_row(row, css):
    return re.sub(r"<t[dh][^>]*>", lambda mt: add_style(mt[0], css), row)


def booktabs_html(table, has_header):
    """Booktabs rules as cell borders: Word keeps those on HTML import, but rejects border changes over COM."""
    rows = re.findall(r"<tr[^>]*>.*?</tr>", table, flags=re.S)
    first, last = rows[0], rows[-1]
    new_first = style_row(first, f"border-top:{THICK}" + (f";border-bottom:{THIN}" if has_header else ""))
    total = 'class="last"' in last
    new_last = style_row(last, f"border-bottom:{THICK}" + (f";border-top:{THIN}" if total else ""))
    table = table.replace(first, new_first, 1)
    i = table.rindex(last)
    return table[:i] + new_last + table[i + len(last):]


def rule_tables(html):
    out, pos = [], 0
    for mt in re.finditer(r"<table[^>]*>.*?</table>", html, flags=re.S):
        tbl = mt[0]
        tbl = booktabs_html(tbl, has_header='class="info"' not in tbl[:30])
        if 'class="info"' not in tbl[:30]:
            tbl = tbl.replace("<table", '<table align="center"', 1)
        out.append(html[pos:mt.start()] + tbl)
        pos = mt.end()
    return "".join(out) + html[pos:]


def main():
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "bao_cao_20seed_word.html"
            page.write_text(word_html(rep.doc), encoding="utf-8")
            doc = word.Documents.Open(str(page), ConfirmConversions=False, ReadOnly=True, AddToRecentFiles=False)
            doc.ActiveWindow.View.Type = 3  # print layout
            ps = doc.PageSetup
            ps.PageWidth, ps.PageHeight = 595.3, 841.9
            ps.TopMargin, ps.BottomMargin, ps.LeftMargin, ps.RightMargin = 54, 57, 59.5, 59.5
            ps.FooterDistance = 28
            footer = doc.Sections(1).Footers(1)
            footer.PageNumbers.Add(1, True)  # centred, also on page 1
            footer.Range.Font.Name, footer.Range.Font.Size = "Times New Roman", 10
            for shape in list(doc.InlineShapes):
                if shape.LinkFormat is not None:
                    shape.LinkFormat.SavePictureWithDocument = True
                    shape.LinkFormat.BreakLink()
            assert doc.InlineShapes.Count == len(IMG_SIZES)
            for i, (w, h) in enumerate(IMG_SIZES, start=1):
                shape = doc.InlineShapes(i)
                shape.LockAspectRatio = False
                shape.Width, shape.Height = w, h
                # keep heading -> figure -> caption on one page
                para = shape.Range.Paragraphs(1)
                para.KeepWithNext = True
                prev = para.Previous()
                while prev is not None and len(prev.Range.Text.strip()) <= 1:
                    prev.KeepWithNext = True
                    prev = prev.Previous()
                if prev is not None and prev.Range.Font.Name == "Arial":
                    prev.KeepWithNext = True
            for para in doc.Paragraphs:  # headings and captions (Arial) stay with what follows
                rng = para.Range
                if rng.Font.Name == "Arial" and len(rng.Text) < 120 and rng.Information(12) is False:
                    para.KeepWithNext = True
                if rng.Text.startswith("Đo tốc độ toàn chuỗi"):  # "Buoc tiep theo" stays with the signature
                    para.KeepWithNext = True
            for i in range(2, doc.Tables.Count + 1):  # short tables never split across pages
                t = doc.Tables(i)
                if t.Rows.Count <= 12:
                    t.Range.ParagraphFormat.KeepWithNext = True
                    t.Rows(t.Rows.Count).Range.ParagraphFormat.KeepWithNext = False
                    t.Rows.AllowBreakAcrossPages = False
            info = doc.Tables(1)  # HTML import leaves loose spacing in the info block
            info.Range.ParagraphFormat.SpaceBefore = 0
            info.Range.ParagraphFormat.SpaceAfter = 0
            info.Range.ParagraphFormat.LineSpacingRule = 0  # single
            info.Rows.HeightRule = 0  # auto
            info.TopPadding = info.BottomPadding = 1.5
            doc.SaveAs2(str(OUT), FileFormat=16)  # wdFormatDocumentDefault (.docx)
            doc.Close(False)
    finally:
        word.Quit()
    print("saved", OUT)


if __name__ == "__main__":
    if OUT.exists():
        sys.exit(f"{OUT} already exists; delete it first")
    main()
