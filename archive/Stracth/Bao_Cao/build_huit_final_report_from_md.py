# -*- coding: utf-8 -*-
"""
Script: build_huit_final_report_from_md.py (Bản nâng cấp hoàn thiện)
Mục đích: Tự động chuyển đổi 11 tệp Markdown trong 'Bao_cao/md viet bao cao/'
thành tệp Word Khóa luận Cử nhân hoàn chỉnh theo đúng Biểu mẫu chuẩn HUIT 2025:
- 3 Sections chuẩn: Bìa (không số) -> Phần đầu (số La Mã i, ii...) -> Thân bài & Phụ lục (số Ả Rập 1, 2, 3...)
- Outline Level chuẩn 3 cấp cho TOC tự động
- Đầy đủ 16 bảng dữ liệu 10 seed và các khung hình ảnh/nhận xét hai trục
"""

import os
import re
import sys
import shutil
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive"
OUTPUT_PATH = os.path.join(WORKSPACE, "Bao_cao", "CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx")
MD_DIR = os.path.join(WORKSPACE, "Bao_cao", "md viet bao cao")

MD_FILES = [
    "00_TRANG_BIA_VA_DANH_MUC.md",
    "01_PHAN_MO_DAU.md",
    "02_CHUONG_1_TONG_QUAN_VA_CO_SO_NGHIEN_CUU.md",
    "03_CHUONG_2_PHAN_TICH_VA_THIET_KE_MO_HINH_DE_XUAT.md",
    "04_CHUONG_3_XAY_DUNG_BO_DU_LIEU_VA_TIEN_XU_LY.md",
    "05_CHUONG_4_CAI_DAT_THUAT_TOAN_VA_UNG_DUNG_MINH_HOA.md",
    "06_CHUONG_5_THU_NGHIEM_VA_DANH_GIA_KET_QUA.md",
    "07_KET_LUAN_VA_HUONG_PHAT_TRIEN.md",
    "08_TAI_LIEU_THAM_KHAO.md",
    "09_PHU_LUC_A_B_C_D_SO_LIEU_THUC_NGHIEM.md",
    "10_PHU_LUC_E_F_G_H_BENCHMARK_NOTEBOOK_UNG_DUNG.md"
]

def apply_section_geometry(sec):
    """Thiết lập lề giấy chuẩn HUIT: Trái 3.5cm, Phải/Trên/Dưới 2.5cm"""
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(3.5)
    sec.right_margin = Cm(2.5)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.header_distance = Cm(1.27)
    sec.footer_distance = Cm(1.27)

def setup_page_numbering(section, fmt="decimal", start=1, show_in_footer=True):
    """Cấu hình định dạng đánh số trang OpenXML"""
    sectPr = section._sectPr
    # Xóa pgNumType cũ nếu có
    for child in list(sectPr):
        if child.tag.endswith('pgNumType'):
            sectPr.remove(child)
            
    if fmt == "none":
        return
        
    xml_pg = f'<w:pgNumType {nsdecls("w")} w:fmt="{fmt}" w:start="{start}"/>' if fmt != "decimal" else f'<w:pgNumType {nsdecls("w")} w:start="{start}"/>'
    sectPr.append(parse_xml(xml_pg))
    
    if show_in_footer:
        footer = section.footer
        p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.text = ""
        run = p.add_run()
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.0)
        # Chèn trường PAGE
        fld = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        p._p.append(fld)

def set_cell_background(cell, color_hex="F2F4F7"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'))

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="B0B0B0", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def add_chapter_title(doc, text):
    """Cấp 1: Tiêu đề chương: 18pt, IN HOA, ĐẬM, CANH GIỮA, outlineLvl = 0"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.space_before = Pt(14.0)
    p.paragraph_format.space_after = Pt(12.0)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(text.upper())
    run.font.name = 'Times New Roman'
    run.font.size = Pt(18.0)
    run.font.bold = True
    pPr = p._element.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="0"/>'))
    return p

def add_front_section_title(doc, text):
    """Tiêu đề phần đầu (Lời cảm ơn, Nhận xét...): 16pt, IN HOA, ĐẬM, CANH GIỮA, outlineLvl = 0"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.space_before = Pt(12.0)
    p.paragraph_format.space_after = Pt(12.0)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(text.upper())
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16.0)
    run.font.bold = True
    pPr = p._element.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="0"/>'))
    return p

def add_heading_2(doc, text):
    """Cấp 2: Mục 1.1, 2.1: 14pt, IN HOA, ĐẬM, CANH TRÁI, outlineLvl = 1"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.space_before = Pt(6.0)
    p.paragraph_format.space_after = Pt(6.0)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(text.upper())
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14.0)
    run.font.bold = True
    pPr = p._element.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="1"/>'))
    return p

def add_heading_3(doc, text):
    """Cấp 3: Mục 1.1.1: 13pt, Thường, ĐẬM, CANH TRÁI, outlineLvl = 2"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.space_before = Pt(6.0)
    p.paragraph_format.space_after = Pt(6.0)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.0)
    run.font.bold = True
    pPr = p._element.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="2"/>'))
    return p

def add_body_paragraph(doc, text):
    """Đoạn văn nội dung: 13pt, regular, thụt đầu dòng 1.0cm, căn đều"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.0)
    p.paragraph_format.space_before = Pt(4.0)
    p.paragraph_format.space_after = Pt(4.0)
    p.paragraph_format.line_spacing = 1.3
    
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = p.add_run(part[2:-2])
            run.font.name = 'Times New Roman'
            run.font.size = Pt(13.0)
            run.font.bold = True
        else:
            run = p.add_run(part)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(13.0)
    return p

def add_bullet_item(doc, text, level=1):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(-0.5)
    p.paragraph_format.left_indent = Cm(0.8 if level == 1 else 1.3)
    p.paragraph_format.space_before = Pt(2.0)
    p.paragraph_format.space_after = Pt(2.0)
    p.paragraph_format.line_spacing = 1.3
    
    prefix = "– " if level == 1 else "+ "
    r_pre = p.add_run(prefix)
    r_pre.font.name = 'Times New Roman'
    r_pre.font.size = Pt(13.0)
    r_pre.font.bold = True
    
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = p.add_run(part[2:-2])
            run.font.name = 'Times New Roman'
            run.font.size = Pt(13.0)
            run.font.bold = True
        else:
            run = p.add_run(part)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(13.0)
    return p

def add_table_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.space_before = Pt(8.0)
    p.paragraph_format.space_after = Pt(3.0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.0)
    run.font.bold = True
    return p

def add_figure_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.space_before = Pt(4.0)
    p.paragraph_format.space_after = Pt(6.0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.0)
    run.font.bold = True
    run.font.italic = True
    return p

def add_observation_box(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.right_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(3.0)
    p.paragraph_format.space_after = Pt(8.0)
    p.paragraph_format.line_spacing = 1.2
    
    parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = p.add_run(part[2:-2])
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12.0)
            run.font.bold = True
        elif part.startswith('*') and part.endswith('*'):
            run = p.add_run(part[1:-1])
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12.0)
            run.font.italic = True
        else:
            run = p.add_run(part)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12.0)
    return p

def parse_markdown_table(lines):
    table_data = []
    for line in lines:
        line_clean = line.strip()
        if not line_clean.startswith('|'):
            continue
        cells = [c.strip() for c in line_clean.split('|')[1:-1]]
        if cells and all(set(c).issubset({'-', ':', ' '}) for c in cells):
            continue
        table_data.append(cells)
    return table_data

def render_table_to_docx(doc, table_data):
    if not table_data or len(table_data) < 1:
        return
    num_rows = len(table_data)
    num_cols = max(len(row) for row in table_data)
    
    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    
    for r_idx, row in enumerate(table_data):
        row_elem = table.rows[r_idx]
        make_row_cant_split(row_elem)
        is_header = (r_idx == 0)
        if is_header:
            make_row_header(row_elem)
            
        for c_idx in range(num_cols):
            cell = row_elem.cells[c_idx]
            val = row[c_idx] if c_idx < len(row) else ""
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (is_header or re.match(r'^[0-9\.\-\+\±\%\$\s]+$', val)) else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2.0)
            p.paragraph_format.space_after = Pt(2.0)
            p.paragraph_format.line_spacing = 1.15
            
            clean_val = val.replace('$', '').replace('**', '')
            run = p.add_run(clean_val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5 if not is_header else 11.0)
            if is_header or '**' in val:
                run.font.bold = True
                
            if is_header:
                set_cell_background(cell, "EAECEF")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F9FAFB")

def render_cover_page(doc, is_outer=True):
    """Vẽ trang bìa chính hoặc bìa phụ chuẩn quy định Khoa CNTT HUIT"""
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2.0)
    r1 = p_inst.add_run("BỘ CÔNG THƯƠNG\nTRƯỜNG ĐẠI HỌC CÔNG THƯƠNG THÀNH PHỐ HỒ CHÍ MINH\nKHOA CÔNG NGHỆ THÔNG TIN")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(13.0)
    r1.font.bold = True
    
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(36.0)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(24.0)
    p_title.paragraph_format.space_after = Pt(12.0)
    r_k = p_title.add_run("KHÓA LUẬN CỬ NHÂN\nNGÀNH CÔNG NGHỆ THÔNG TIN\nMÃ ĐỀ TÀI: CNTT_KLCN182\n\n")
    r_k.font.name = 'Times New Roman'
    r_k.font.size = Pt(16.0)
    r_k.font.bold = True
    
    r_name = p_title.add_run("NGHIÊN CỨU PHƯƠNG PHÁP TÍCH HỢP VMAMBA VÀO MÔ HÌNH\nYOLO26-SEG TRONG PHÂN ĐOẠN POLYP TỪ ẢNH NỘI SOI ĐẠI TRỰC TRÀNG")
    r_name.font.name = 'Times New Roman'
    r_name.font.size = Pt(18.0)
    r_name.font.bold = True
    
    p_space2 = doc.add_paragraph()
    p_space2.paragraph_format.space_before = Pt(48.0)
    
    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_info.paragraph_format.left_indent = Cm(3.0)
    p_info.paragraph_format.space_before = Pt(12.0)
    p_info.paragraph_format.space_after = Pt(48.0)
    p_info.paragraph_format.line_spacing = 1.3
    
    info_text = (
        "Sinh viên thực hiện:\n"
        "  1. LÊ ĐỨC LƯƠNG     - MSSV: 2001230490 - Lớp: 14DHTH09\n"
        "  2. PHÙNG TUẤN HUY   - MSSV: 2001230312 - Lớp: 14DHTH13\n"
        "  3. TRẦN MẠNH TOÀN   - MSSV: 2001230830 - Lớp: 14DHTH09\n\n"
        "Giảng viên hướng dẫn:\n"
        "  TS. PHÙNG THẾ BẢO"
    )
    r_info = p_info.add_run(info_text)
    r_info.font.name = 'Times New Roman'
    r_info.font.size = Pt(13.0)
    r_info.font.bold = True
    
    p_bot = doc.add_paragraph()
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bot.paragraph_format.space_before = Pt(24.0)
    r_bot = p_bot.add_run("TP. HỒ CHÍ MINH, NĂM 2026")
    r_bot.font.name = 'Times New Roman'
    r_bot.font.size = Pt(13.0)
    r_bot.font.bold = True

def process_file_content(doc, file_path, is_front_matter=False):
    """Đọc và nhúng nội dung file markdown"""
    print(f"--> Đang xử lý: {os.path.basename(file_path)}")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    i = 0
    in_table = False
    table_lines = []
    
    while i < len(lines):
        line = lines[i].rstrip('\r\n')
        line_strip = line.strip()
        
        # 1. Bảng Markdown
        if line_strip.startswith('|'):
            in_table = True
            table_lines.append(line_strip)
            i += 1
            continue
        elif in_table:
            data = parse_markdown_table(table_lines)
            render_table_to_docx(doc, data)
            in_table = False
            table_lines = []
            
        if not line_strip:
            i += 1
            continue
            
        # 2. Bỏ qua các khối bìa text thô trong 00_ vì đã có render_cover_page
        if is_front_matter and ("TRANG BÌA CHÍNH" in line_strip or "TRANG BÌA PHỤ" in line_strip or "```text" in line_strip):
            # Bỏ qua code block bìa text
            if line_strip.startswith("```"):
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    i += 1
                i += 1
                continue
            i += 1
            continue
            
        # 3. Khối hình ảnh
        if line_strip.startswith('> **[HÌNH ẢNH MINH HỌA') or line_strip.startswith('![') or ('figures/' in line_strip and line_strip.startswith('>')):
            fig_lines = [line_strip]
            i += 1
            while i < len(lines) and lines[i].strip().startswith('>'):
                fig_lines.append(lines[i].strip())
                i += 1
                
            full_fig_text = "\n".join(fig_lines)
            img_match = re.search(r'[`\(\'\"](.*?\.(?:png|jpg|jpeg))[`\)\'\"]', full_fig_text)
            img_path = img_match.group(1) if img_match else None
            cap_match = re.search(r'\*(Hình \d+\.\d+:.*?)\*', full_fig_text)
            caption = cap_match.group(1) if cap_match else "Hình minh họa"
            
            real_img = None
            if img_path:
                candidates = [
                    os.path.join(WORKSPACE, img_path),
                    os.path.join(WORKSPACE, "doc", img_path),
                    os.path.join(WORKSPACE, "Ket_Qua_V2", "KQ_Nen_DX_10seed", img_path),
                    os.path.join(WORKSPACE, "Ket_Qua_V2", "KQ_Nen_DX_10seed", "05_charts", os.path.basename(img_path))
                ]
                for c in candidates:
                    if os.path.exists(c):
                        real_img = c
                        break
            
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8.0)
            p_img.paragraph_format.space_after = Pt(2.0)
            
            if real_img:
                try:
                    p_img.add_run().add_picture(real_img, width=Inches(5.5))
                except Exception:
                    r_box = p_img.add_run(f"[HỘP MINH HỌA: {os.path.basename(img_path)}]")
                    r_box.font.name = 'Times New Roman'
                    r_box.font.size = Pt(11.0)
                    r_box.font.italic = True
            else:
                r_box = p_img.add_run(f"[KHUNG HÌNH ẢNH: {caption}]")
                r_box.font.name = 'Times New Roman'
                r_box.font.size = Pt(11.0)
                r_box.font.italic = True
                
            add_figure_caption(doc, caption)
            
            if '[PHẦN NHẬN XÉT' in full_fig_text or 'Nhận xét' in full_fig_text:
                obs_idx = full_fig_text.find('[PHẦN NHẬN XÉT')
                if obs_idx != -1:
                    obs_content = full_fig_text[obs_idx:].replace('>', '').strip()
                    add_observation_box(doc, obs_content)
            continue
            
        # 4. Tiêu đề cấp 1
        if line_strip.startswith('# '):
            text = line_strip[2:].strip()
            if "PHẦN ĐẦU:" in text or "HỆ THỐNG PHỤ LỤC" in text:
                i += 1
                continue
            add_chapter_title(doc, text)
            i += 1
            continue
            
        # 5. Tiêu đề cấp 2
        if line_strip.startswith('## '):
            text = line_strip[3:].strip()
            if is_front_matter:
                # Tiêu đề mục phần đầu (Lời cảm ơn, Mục lục...)
                clean_text = re.sub(r'^\d+\.\s*', '', text)
                add_front_section_title(doc, clean_text)
                if "MỤC LỤC" in clean_text.upper():
                    # Chèn trường TOC tự động
                    p_toc = doc.add_paragraph()
                    p_toc.paragraph_format.space_before = Pt(6.0)
                    p_toc.paragraph_format.space_after = Pt(6.0)
                    p_toc._p.append(parse_xml(r'<w:fldSimple %s w:instr="TOC \o &quot;1-3&quot; \h \z \u"/>' % nsdecls('w')))
            else:
                add_heading_2(doc, text)
            i += 1
            continue
            
        # 6. Tiêu đề cấp 3
        if line_strip.startswith('### '):
            text = line_strip[4:].strip()
            add_heading_3(doc, text)
            i += 1
            continue
            
        # 7. Tiêu đề bảng biểu độc lập
        if line_strip.startswith('*Bảng ') or line_strip.startswith('**Bảng '):
            caption = re.sub(r'[\*\`]', '', line_strip)
            add_table_caption(doc, caption)
            i += 1
            continue
            
        # 8. Bullet
        if line_strip.startswith('- ') or line_strip.startswith('* '):
            text = line_strip[2:].strip()
            add_bullet_item(doc, text, level=1)
            i += 1
            continue
        if line_strip.startswith('  - ') or line_strip.startswith('  * ') or line_strip.startswith('    - '):
            text = line_strip.strip()[2:].strip()
            add_bullet_item(doc, text, level=2)
            i += 1
            continue
            
        # 9. Danh mục đánh số
        num_match = re.match(r'^(\d+\.)\s+(.*)$', line_strip)
        if num_match:
            prefix = num_match.group(1)
            text = num_match.group(2)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(-0.5)
            p.paragraph_format.left_indent = Cm(0.8)
            p.paragraph_format.space_before = Pt(3.0)
            p.paragraph_format.space_after = Pt(3.0)
            p.paragraph_format.line_spacing = 1.3
            r_num = p.add_run(f"{prefix} ")
            r_num.font.name = 'Times New Roman'
            r_num.font.size = Pt(13.0)
            r_num.font.bold = True
            
            parts = re.split(r'(\*\*.*?\*\*)', text)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(13.0)
                    run.font.bold = True
                else:
                    run = p.add_run(part)
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(13.0)
            i += 1
            continue
            
        # 10. Code block
        if line_strip.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i].rstrip('\r\n'))
                i += 1
            i += 1
            
            p_code = doc.add_paragraph()
            p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_code.paragraph_format.left_indent = Cm(0.5)
            p_code.paragraph_format.right_indent = Cm(0.5)
            p_code.paragraph_format.space_before = Pt(4.0)
            p_code.paragraph_format.space_after = Pt(4.0)
            p_code.paragraph_format.line_spacing = 1.15
            
            code_text = "\n".join(code_lines)
            run = p_code.add_run(code_text)
            run.font.name = 'Consolas'
            run.font.size = Pt(9.5)
            continue
            
        # 11. Hộp cảnh báo / Note
        if line_strip.startswith('>'):
            note_lines = [line_strip[1:].strip()]
            i += 1
            while i < len(lines) and lines[i].strip().startswith('>'):
                note_lines.append(lines[i].strip()[1:].strip())
                i += 1
            note_text = "\n".join(note_lines)
            add_observation_box(doc, note_text)
            continue
            
        # 12. Đoạn văn thường
        add_body_paragraph(doc, line_strip)
        i += 1
        
    if in_table and table_lines:
        data = parse_markdown_table(table_lines)
        render_table_to_docx(doc, data)

def main():
    print("=" * 65)
    print("BẮT ĐẦU XÂY DỰNG BÁO CÁO KHÓA LUẬN CỬ NHÂN HUIT 2025 HOÀN HẢO")
    print("=" * 65)
    
    # Khởi tạo Document mới
    doc = Document()
    
    # =========================================================================
    # SECTION 0: BÌA CHÍNH VÀ BÌA PHỤ (KHÔNG SỐ TRANG)
    # =========================================================================
    print("1. Xây dựng Section 0: Trang bìa chính và Trang bìa phụ...")
    sec0 = doc.sections[0]
    apply_section_geometry(sec0)
    setup_page_numbering(sec0, fmt="none", show_in_footer=False)
    
    # Bìa chính
    render_cover_page(doc, is_outer=True)
    doc.add_page_break()
    # Bìa phụ
    render_cover_page(doc, is_outer=False)
    
    # =========================================================================
    # SECTION 1: PHẦN ĐẦU (ĐÁNH SỐ LA MÃ: i, ii, iii...)
    # =========================================================================
    print("2. Xây dựng Section 1: Lời cảm ơn, Nhận xét, Mục lục, Danh mục...")
    sec1 = doc.add_section(WD_SECTION.NEW_PAGE)
    apply_section_geometry(sec1)
    setup_page_numbering(sec1, fmt="lowerRoman", start=1, show_in_footer=True)
    
    # Nạp nội dung 00_TRANG_BIA_VA_DANH_MUC.md
    f00 = os.path.join(MD_DIR, "00_TRANG_BIA_VA_DANH_MUC.md")
    process_file_content(doc, f00, is_front_matter=True)
    
    # =========================================================================
    # SECTION 2: PHẦN THÂN VÀ PHỤ LỤC (ĐÁNH SỐ TỰ NHIÊN: 1, 2, 3...)
    # =========================================================================
    print("3. Xây dựng Section 2: Mở đầu, Chương 1-5, Kết luận, TLTK, Phụ lục...")
    sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
    apply_section_geometry(sec2)
    setup_page_numbering(sec2, fmt="decimal", start=1, show_in_footer=True)
    
    # Nạp tuần tự từ 01_PHAN_MO_DAU đến 10_PHU_LUC...
    for md_file in MD_FILES[1:]:
        md_path = os.path.join(MD_DIR, md_file)
        if not os.path.exists(md_path):
            print(f"CẢNH BÁO: Thiếu tệp {md_path}")
            continue
            
        if md_file != MD_FILES[1]:
            doc.add_page_break()
            
        process_file_content(doc, md_path, is_front_matter=False)
        
    # Lưu tài liệu Word hoàn chỉnh
    print(f"\n4. Đang xuất bản tệp Word vào: {OUTPUT_PATH}")
    doc.save(OUTPUT_PATH)
    
    file_size_mb = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print("=" * 65)
    print("HOÀN THÀNH TOÀN DIỆN! TỆP WORD KHÓA LUẬN HUIT ĐÃ XUẤT BẢN THÀNH CÔNG.")
    print(f"- Tệp xuất xưởng: {os.path.basename(OUTPUT_PATH)}")
    print(f"- Dung lượng: {file_size_mb:.2f} MB")
    print("=" * 65)

if __name__ == '__main__':
    main()
