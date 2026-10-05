# -*- coding: utf-8 -*-
import sys
import re
from docx import Document

sys.stdout.reconfigure(encoding='utf-8')
docx_path = 'Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx'
doc = Document(docx_path)

headings = []
for p in doc.paragraphs:
    xml = p._p.xml
    if 'outlineLvl' in xml:
        m = re.search(r'w:val="([0-9]+)"', xml)
        if m:
            headings.append((m.group(1), p.text.strip()))

print("--- DANH MỤC TOÀN BỘ CÁC ĐỀ MỤC CẤP 1 (OUTLINE LEVEL 0) ---")
for lvl, text in headings:
    if lvl == '0':
        print(f"  * {text}")

print("\n--- KIỂM TRA ĐÁNH SỐ TRANG TRÊN 3 SECTIONS ---")
for i, s in enumerate(doc.sections):
    sectPr = s._sectPr
    pg = sectPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgNumType')
    pg_attr = pg.attrib if pg is not None else "Không có (Không đánh số)"
    print(f"Section {i}: Left={s.left_margin.cm:.1f}cm, Right={s.right_margin.cm:.1f}cm | pgNumType: {pg_attr}")
