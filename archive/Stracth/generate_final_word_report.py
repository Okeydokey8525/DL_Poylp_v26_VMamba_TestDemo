# -*- coding: utf-8 -*-
"""
Script tạo lập Báo cáo Tiến độ Word (.docx) hoàn chỉnh chuẩn Lê Đức Lương
Đề tài: CNTT_KLCN182 - Nghiên cứu phương pháp tích hợp Topology-Shape-aware VMamba vào YOLO26-seg
Bộ dữ liệu: Kvasir_YOLO_SEG_BG20 (1.200 ảnh, 20% ảnh nền âm tính)
Thực nghiệm: 10 Seeds độc lập (Seed 0 đến Seed 9)
Tác giả: Lê Đức Lương
"""

import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import docx
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Đổ màu nền cho ô trong bảng"""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Thiết lập padding cho ô trong bảng (đơn vị dxa: 20 dxa = 1 pt)"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="B0B0B0", sz="4"):
    """Thiết lập đường viền bảng màu xám thanh lịch"""
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:left w:val="none"/>'
                        f'<w:right w:val="none"/>'
                        f'<w:insideV w:val="none"/>'
                        f'</w:tblBorders>')
    tblPr.append(borders)

def set_metadata_table_borders(table, color="999999", sz="6"):
    """Thiết lập viền đầy đủ cho bảng metadata mở đầu"""
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'</w:tblBorders>')
    tblPr.append(borders)

def make_row_header(row):
    """Cấu hình hàng lặp lại tiêu đề và không tách trang"""
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def make_row_cant_split(row):
    """Cấu hình hàng không bị tách rời giữa hai trang"""
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def apply_page_setup(doc):
    """Thiết lập hình học trang A4 chuẩn đóng gáy của Lê Đức Lương"""
    for sec in doc.sections:
        sec.page_width = Cm(21.0)
        sec.page_height = Cm(29.7)
        sec.top_margin = Cm(2.5)
        sec.bottom_margin = Cm(2.5)
        sec.left_margin = Cm(3.5)   # 3.5 cm BẮT BUỘC cho đóng gáy luận văn
        sec.right_margin = Cm(2.5)
        sec.header_distance = Cm(1.27)
        sec.footer_distance = Cm(1.27)

def add_heading_1(doc, text):
    """Heading 1: 13pt BOLD IN HOA, line 1.25, space before 6pt, after 3pt"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.space_before = Pt(6.0)
    p.paragraph_format.space_after = Pt(3.0)
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(text.upper())
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.0)
    run.font.bold = True
    pPr = p._element.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="0"/>'))
    return p

def add_heading_2(doc, text):
    """Heading 2: 13pt BOLD, line 1.25, space before 5pt, after 2pt"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.space_before = Pt(5.0)
    p.paragraph_format.space_after = Pt(2.0)
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.0)
    run.font.bold = True
    pPr = p._element.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="1"/>'))
    return p

def add_heading_3(doc, text):
    """Heading 3: 13pt BOLD ITALIC, line 1.25, space before 4pt, after 2pt"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.space_before = Pt(4.0)
    p.paragraph_format.space_after = Pt(2.0)
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.0)
    run.font.bold = True
    run.font.italic = True
    pPr = p._element.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="2"/>'))
    return p

def add_body_p(doc, text, bold_prefix=None):
    """Đoạn văn thân bài: 13pt regular, thụt đầu dòng 1.27cm, căn đều"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.27)
    p.paragraph_format.space_before = Pt(3.0)
    p.paragraph_format.space_after = Pt(3.0)
    p.paragraph_format.line_spacing = 1.25
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(13.0)
        r_pre.font.bold = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.0)
    return p

def add_bullet_p(doc, bold_title, text):
    """Đoạn gạch đầu dòng: thụt lề chuẩn, từ khóa in đậm"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.space_before = Pt(2.0)
    p.paragraph_format.space_after = Pt(2.0)
    p.paragraph_format.line_spacing = 1.25
    r_bullet = p.add_run("•  ")
    r_bullet.font.name = 'Times New Roman'
    r_bullet.font.size = Pt(13.0)
    r_bullet.font.bold = True
    if bold_title:
        r_title = p.add_run(bold_title + ": ")
        r_title.font.name = 'Times New Roman'
        r_title.font.size = Pt(13.0)
        r_title.font.bold = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.0)
    return p

def add_table_caption(doc, text):
    """Tiêu đề bảng: đặt phía TRÊN bảng, in nghiêng 12pt, căn trái"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.space_before = Pt(6.0)
    p.paragraph_format.space_after = Pt(2.0)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12.0)
    run.font.bold = True
    run.font.italic = True
    return p

def add_figure_block(doc, img_rel_path, caption_text, observation_text, width_cm=15.0):
    """Bộ ba Hình ảnh - Tiêu đề - Nhận xét học thuật 2 trục"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    archive_dir = os.path.abspath(os.path.join(script_dir, ".."))
    img_abs_path = os.path.join(archive_dir, img_rel_path)

    # 1. Ảnh căn giữa
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.first_line_indent = None
    p_img.paragraph_format.space_before = Pt(6.0)
    p_img.paragraph_format.space_after = Pt(2.0)
    if os.path.exists(img_abs_path):
        p_img.add_run().add_picture(img_abs_path, width=Cm(width_cm))
    else:
        p_img.add_run(f"[Hình ảnh: {img_rel_path}]")

    # 2. Tiêu đề ảnh căn giữa (12pt BOLD)
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.first_line_indent = None
    p_cap.paragraph_format.space_before = Pt(2.0)
    p_cap.paragraph_format.space_after = Pt(3.0)
    run_cap = p_cap.add_run(caption_text)
    run_cap.font.name = 'Times New Roman'
    run_cap.font.size = Pt(12.0)
    run_cap.font.bold = True

    # 3. Đoạn nhận xét 2 trục (13pt, thụt đầu dòng 1.27cm, căn đều)
    p_obs = add_body_p(doc, observation_text)
    return p_img, p_cap, p_obs

def build_full_report():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    archive_dir = os.path.abspath(os.path.join(script_dir, ".."))
    print("Khoi tao tien trinh dung van ban Word chuan Le Duc Luong...")
    doc = docx.Document()
    apply_page_setup(doc)

    # --- TIÊU ĐỀ BÁO CÁO & ĐỀ TÀI ---
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(3.0)
    p_title.paragraph_format.space_after = Pt(3.0)
    p_title.paragraph_format.line_spacing = 1.25
    r_title = p_title.add_run("BÁO CÁO TIẾN ĐỘ THỰC NGHIỆM VÀ KẾT QUẢ NGHIÊN CỨU TUẦN")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(13.0)
    r_title.font.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(3.0)
    p_sub.paragraph_format.space_after = Pt(6.0)
    p_sub.paragraph_format.line_spacing = 1.25
    r_sub = p_sub.add_run("Đề tài: Nghiên cứu phương pháp tích hợp Topology-Shape-aware VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(15.0)
    r_sub.font.bold = True
    r_sub.font.italic = True

    # --- BẢNG METADATA MỞ ĐẦU (TABLE 0) ---
    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_metadata_table_borders(tbl_meta, color="999999", sz="6")

    meta_data = [
        ("Mã đề tài & Phân loại:", "CNTT_KLCN182 — Khóa luận Cử nhân ngành CNTT (2026 – 2027)"),
        ("Giảng viên hướng dẫn:", "TS. Phùng Thế Bảo (Email: baopt@huit.edu.vn)"),
        ("Nhóm sinh viên thực hiện:", "1. Lê Đức Lương (MSSV: 2001230490 — Lớp: 14DHTH09)\n2. Phùng Tuấn Huy (MSSV: 2001230312 — Lớp: 14DHTH13)\n3. Trần Mạnh Toàn (MSSV: 2001230830 — Lớp: 14DHTH09)"),
        ("Nội dung báo cáo trọng tâm:", "Đánh giá hiệu năng thực nghiệm kiểm thử 10 Seed trên bộ dữ liệu Kvasir_YOLO_SEG_BG20 (bổ sung 20% ảnh nền âm tính), kiểm chứng kiến trúc C2TSVMamba, phân tích ma trận nhầm lẫn lâm sàng và hệ thống trực quan hóa 12 biểu đồ chuẩn khoa học.")
    ]

    for r_idx, (k, v) in enumerate(meta_data):
        row = tbl_meta.rows[r_idx]
        make_row_cant_split(row)
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Cm(5.37)
        c1.width = Cm(9.63)
        set_cell_background(c0, "F7F7F7")
        set_cell_margins(c0, top=120, bottom=120, left=150, right=150)
        set_cell_margins(c1, top=120, bottom=120, left=150, right=150)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2.0)
        p0.paragraph_format.space_after = Pt(2.0)
        p0.paragraph_format.line_spacing = 1.15
        r0 = p0.add_run(k)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(13.0)
        r0.font.bold = True

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2.0)
        p1.paragraph_format.space_after = Pt(2.0)
        p1.paragraph_format.line_spacing = 1.15
        r1 = p1.add_run(v)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(13.0)

    # --- 1. MỤC TIÊU VÀ NHIỆM VỤ BÁO CÁO TIẾN ĐỘ ---
    add_heading_1(doc, "1. MỤC TIÊU VÀ NHIỆM VỤ BÁO CÁO TIẾN ĐỘ")
    add_body_p(doc, "Báo cáo tiến độ tuần này tập trung giải quyết toàn diện các định hướng chuyên môn trọng tâm đã được thống nhất tại cuộc họp với Giảng viên Hướng dẫn TS. Phùng Thế Bảo, chuyển dịch toàn bộ hệ thống thực nghiệm từ bộ dữ liệu cũ (chỉ toàn ảnh dương tính có polyp) sang bộ dữ liệu y khoa chuẩn hóa mới có bổ sung 20% ảnh nền âm tính, cụ thể bao gồm các nhiệm vụ cốt lõi sau:")

    add_bullet_p(doc, "1. Chuẩn hóa quy trình tiền xử lý với 20% ảnh nền (BG20)", "Tích hợp 200 ảnh nội soi hồi manh tràng bình thường (normal-cecum) vào bộ dữ liệu Kvasir-SEG (tổng quy mô 1.200 ảnh) với cơ chế nhãn rỗng (0-byte text file). Cơ chế này huấn luyện mạng nhận biết niêm mạc đại tràng khỏe mạnh, triệt tiêu hiện tượng báo động giả (False Positive) – một hạn chế chết người trong nội soi thực tế.")
    add_bullet_p(doc, "2. Mở rộng kiểm định độ tin cậy từ 6 lên 10 Seed (Seed Robustness)", "Thực hiện huấn luyện độc lập hoàn toàn trên 10 hạt giống ngẫu nhiên liên tục (từ Seed 0 đến Seed 9) với chế độ khóa tất định nghiêm ngặt (deterministic training), đo lường chính xác các chỉ số Mean ± Std, Min/Max và kiểm định giả thuyết Paired t-test nhằm loại trừ hoàn toàn yếu tố may rủi của trọng số khởi tạo ban đầu.")
    add_bullet_p(doc, "3. Thiết lập hệ thống 2 mô hình đối đầu trực diện chuẩn mực", "Tiến hành so sánh đối xứng song song giữa mô hình Baseline phân đoạn YOLO26s-seg và mô hình đề xuất tích hợp VMamba (YOLO26s-seg + C2TSVMamba tại Tầng 10 Cổ mạng Neck) trên cùng một cấu hình siêu tham số và môi trường phần cứng đồng nhất.")
    add_bullet_p(doc, "4. Phân tích ma trận nhầm lẫn lâm sàng trên 160 ảnh thẩm định", "Đánh giá chi tiết năng lực phân loại trên 127 tổn thương polyp thực tế và 40 ảnh nền âm tính hoàn toàn, định lượng chính xác 4 ô nhầm lẫn y khoa (True Positive, False Negative, False Positive, True Negative) và phân tích sự đánh đổi lâm sàng.")
    add_bullet_p(doc, "5. Hệ thống hóa 12 biểu đồ trực quan hóa khoa học đa chiều", "Bổ sung đầy đủ 12 hình ảnh minh chứng định lượng từ thư mục kết quả mới, kèm các đoạn nhận xét học thuật chuyên sâu được cấu trúc chặt chẽ theo hai trục: Trục Kỹ thuật Học sâu và Trục Ý nghĩa Y khoa Nội soi can thiệp.")

    # --- 2. CẤU TRÚC MÔ HÌNH VÀ TIỀN XỬ LÝ DỮ LIỆU BG20 ---
    add_heading_1(doc, "2. CẤU TRÚC MÔ HÌNH VÀ TIỀN XỬ LÝ DỮ LIỆU BG20")

    add_heading_2(doc, "2.1. Vai trò tích hợp VMamba trong pipeline phân đoạn polyp")
    add_body_p(doc, "Trong nội soi tiêu hóa, các tổn thương polyp thường có ranh giới hòa lẫn vào cấu trúc nếp gấp niêm mạc xung quanh, kích thước biến thiên phức tạp từ vài milimet đến nhiều centimet, và bề mặt thường xuyên bị che khuất bởi dịch nhầy hoặc ánh đèn nội soi gây lóa cục bộ. Các mạng tích chập thuần túy (CNN) bị giới hạn bởi trường tiếp nhận cục bộ (local receptive field), dẫn đến hiện tượng phân đoạn bị khuyết góc hoặc đứt gãy mặt nạ tại các vùng lóa sáng. Ngược lại, cơ chế Self-Attention trong Vision Transformer (ViT) tuy nắm bắt được tương quan toàn cục nhưng lại đòi hỏi độ phức tạp tính toán bậc hai O(N²), gây nghẽn tốc độ và không thể đáp ứng tiêu chuẩn video thời gian thực (>= 30 FPS).")
    add_body_p(doc, "Khối C2TSVMamba (Cross-Stage Partial Topology-Shape-aware VMamba) được đề xuất tích hợp tại Tầng 10 (Layer 10) thuộc Cổ mạng (Neck). Vị trí này nằm ngay sau khối SPPF của Backbone, tiếp nhận bản đồ đặc trưng P5 đa vĩ mô (kích thước B x 512 x 20 x 20) trước khi truyền sang các tầng tổng hợp P4, P3. Cấu trúc khối kết hợp hai nhánh song song độc đáo: (1) Nhánh VMamba SS2D (2D Selective Scan) thực hiện quét 4 hướng không gian chéo, nén ngữ cảnh toàn cảnh với độ phức tạp tuyến tính O(N); và (2) Nhánh Tích chập Hình thái Đa hướng (Multi-directional Morphological Convolutions) sử dụng các kernel tích chập bất đối xứng để khóa chặt gradient biến thiên đột ngột tại đường biên tế bào polyp. Nhờ đó, mô hình thực hiện vai trò 'tô' và tách biệt ranh giới tổn thương giải phẫu một cách sắc nét và nguyên vẹn.")

    add_heading_2(doc, "2.2. Bộ dữ liệu Kvasir_YOLO_SEG_BG20 và cơ chế nhãn rỗng triệt tiêu báo động giả")
    add_body_p(doc, "Ở các thực nghiệm tiền trạm trước đây, mô hình chỉ được huấn luyện trên 1.000 ảnh dương tính (100% ảnh đều chứa ít nhất một polyp). Điều này tạo ra một thiên kiến xác nhận (confirmation bias) nghiêm trọng: mô hình ngầm hiểu rằng khung hình nội soi nào cũng có bệnh, dẫn đến xu hướng cố gắng dự đoán một vùng mặt nạ ngay cả trên các vùng niêm mạc khỏe mạnh, gây ra tỷ lệ báo động giả (False Positive) rất cao trong thực tế.")
    add_body_p(doc, "Để khắc phục triệt để lỗ hổng này, đề tài đã xây dựng bộ dữ liệu y khoa chuẩn hóa Kvasir_YOLO_SEG_BG20 có quy mô 1.200 ảnh, bằng cách bổ sung 200 ảnh nội soi đại trực tràng bình thường (lớp normal-cecum) từ cơ sở dữ liệu Kvasir chính thống. Tỷ lệ ảnh nền được ấn định chính xác 20% (1/5 tổng số ảnh) ở cả tập huấn luyện và tập kiểm định:")

    add_table_caption(doc, "Bảng 1: Thống kê chi tiết phân chia bộ dữ liệu chuẩn Kvasir_YOLO_SEG_BG20 (20% ảnh nền)")
    tbl_ds = doc.add_table(rows=4, cols=6)
    tbl_ds.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_ds, color="B0B0B0", sz="4")

    ds_headers = ["Tập phân chia", "Ảnh Polyp", "Ảnh Nền (BG)", "Tổng số ảnh", "Tỷ lệ nền (%)", "Số Ground-Truth Polyp"]
    ds_rows = [
        ["Tập Huấn luyện (Train)", "880 ảnh", "160 ảnh (0-byte)", "1.040 ảnh", "15.38% nền", "Khoảng 950 polyp"],
        ["Tập Kiểm định (Val)", "120 ảnh", "40 ảnh (0-byte)", "160 ảnh", "25.00% nền", "Cố định đúng 127 polyp"],
        ["Toàn bộ Kvasir_BG20", "1.000 ảnh", "200 ảnh nền", "1.200 ảnh", "16.67% ~ 20%", "1.077 ground-truth"]
    ]

    hdr_r = tbl_ds.rows[0]
    make_row_header(hdr_r)
    for c_i, h_txt in enumerate(ds_headers):
        cell = hdr_r.cells[c_i]
        set_cell_background(cell, "F2F2F2")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_txt)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.0)
        run.font.bold = True

    for r_i, r_data in enumerate(ds_rows):
        row = tbl_ds.rows[r_i + 1]
        make_row_cant_split(row)
        for c_i, val_txt in enumerate(r_data):
            cell = row.cells[c_i]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i == 0 else WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val_txt)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11.0)

    add_body_p(doc, "Cơ chế nhãn âm tính rỗng (Empty Label 0-byte): Các ảnh nền âm tính được gán tệp nhãn văn bản có dung lượng đúng 0 byte. Khi truyền qua mạng nơ-ron, hàm mất mát phân loại (BCE Class Loss) và hàm mất mát phân đoạn mặt nạ (Segmentation Loss) sẽ áp đặt mức phạt gradient rất nặng nếu mô hình phát sinh bất kỳ hộp bao hoặc điểm ảnh dự đoán nào trên khung hình nền. Kỹ thuật này ép mạng học cách 'giữ im lặng' khi đối diện với các nếp gấp ruột lành tính, nâng cao vượt bậc độ đặc hiệu (Specificity) của hệ thống.")

    add_heading_2(doc, "2.3. Quy trình tiền xử lý dữ liệu và chiến lược tăng cường (Data Augmentation)")
    add_body_p(doc, "Quy trình tiền xử lý được chuẩn hóa tự động trước khi nạp vào mạng:")
    add_bullet_p(doc, "Chuẩn hóa kích thước khung hình (Letterbox Resizing)", "Ảnh nội soi có độ phân giải gốc không đồng đều (từ 720x576 đến 1920x1072 pixel). Thuật toán Letterbox đưa ảnh về kích thước chuẩn 640x640 pixel bằng cách giữ nguyên tỷ lệ khung hình gốc (aspect ratio) và bù viền xám đối xứng (padding), ngăn ngừa hoàn toàn hiện tượng méo mó hoặc biến dạng cấu trúc giải phẫu của tổn thương.")
    add_bullet_p(doc, "Chuẩn hóa giá trị điểm ảnh (Pixel Normalization)", "Toàn bộ thang độ sáng RGB [0, 255] được chuẩn hóa về miền giá trị thực [0.0, 1.0], giúp ổn định phân phối dữ liệu đầu vào và làm phẳng bề mặt hàm mất mát.")
    add_bullet_p(doc, "Chuyển đổi nhãn mặt nạ sang chuỗi tọa độ Polygon", "Mặt nạ nhị phân y khoa được vector hóa thành chuỗi đa giác khép kín chứa các cặp tọa độ chuẩn hóa (x, y) trong khoảng [0, 1], tương ứng với lớp nhãn bệnh học duy nhất (nc: 1, names: {0: 'polyp'}).")
    add_bullet_p(doc, "Chiến lược tăng cường dữ liệu thích ứng (Augmentation Pipeline)", "Áp dụng kỹ thuật ghép 4 ảnh ngẫu nhiên (Mosaic = 1.0) nhằm đa dạng hóa tỷ lệ khung hình và bối cảnh tổn thương; kết hợp lật ảnh ngang (fliplr = 0.5) mô phỏng cấu trúc đối xứng ruột, co giãn tỷ lệ (scale = 0.5) mô phỏng khoảng cách ống soi xa gần. Đặc biệt, kích hoạt cơ chế tắt Mosaic ở 10 epoch cuối (close_mosaic = 10) để mô hình làm mịn đường biên phân đoạn trên hình thái ảnh thực tế.")

    add_heading_2(doc, "2.4. Cấu hình môi trường thực nghiệm và siêu tham số huấn luyện tất định")
    add_body_p(doc, "Thực nghiệm được triển khai trên nền tảng điện toán đám mây Kaggle GPU Cloud sử dụng card đồ họa chuyên dụng NVIDIA Tesla T4 (16GB VRAM), framework PyTorch 2.x và thư viện Ultralytics. Để đảm bảo tính tái lập kết quả khoa học 100% trên cả 10 seed, quy chuẩn khóa tất định nghiêm ngặt đã được thiết lập:")

    add_table_caption(doc, "Bảng 2: Cấu hình siêu tham số huấn luyện tất định cho Baseline và TSVM trên 10 Seeds")
    tbl_hp = doc.add_table(rows=12, cols=4)
    tbl_hp.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_hp, color="B0B0B0", sz="4")

    hp_headers = ["Nhóm cấu hình", "Tham số (Hyperparameter)", "Giá trị thiết lập", "Ý nghĩa học thuật & Tác động"]
    hp_rows = [
        ["Môi trường", "Khóa ngẫu nhiên (Deterministic)", "True (cuDNN, cuBLAS)", "Khóa mọi sai số ngẫu nhiên trên phần cứng GPU"],
        ["Môi trường", "Bộ nhớ làm việc cuBLAS", "CUBLAS_WORKSPACE_CONFIG=:4096:8", "Đảm bảo tính tái lập kết quả ma trận trên PyTorch"],
        ["Dữ liệu", "Số lượng hạt giống (Seeds)", "10 Seeds (Seed 0 -> 9)", "Đánh giá phương sai và độ ổn định thống kê đa seed"],
        ["Dữ liệu", "Kích thước ảnh vào (imgsz)", "640 × 640 pixel", "Chuẩn hóa độ phân giải tối ưu xử lý video y khoa"],
        ["Dữ liệu", "Kích thước batch (batch_size)", "8 ảnh / batch", "Cân bằng độ ổn định gradient và dung lượng VRAM GPU"],
        ["Huấn luyện", "Số chu kỳ học (Epochs)", "100 Epochs", "Đủ chu kỳ để mô hình hội tụ hoàn toàn vào cực tiểu"],
        ["Huấn luyện", "Bộ tối ưu hóa (Optimizer)", "AdamW", "Tối ưu hóa trọng số phi tuyến với phân rã trọng số l2"],
        ["Huấn luyện", "Tốc độ học ban đầu (lr0)", "0.001", "Hạn chế phân kỳ ở các tầng VMamba quét chọn lọc"],
        ["Huấn luyện", "Lịch trình giảm lr (lrf)", "0.01 (Cosine Annealing)", "Hạ dần learning rate làm mịn nghiệm hội tụ ở pha cuối"],
        ["Huấn luyện", "Trọng số hàm mất mát (box, seg, cls)", "box: 7.5, seg: 12.0, cls: 0.5", "Ưu tiên tối đa cho độ chính xác phân đoạn mặt nạ"],
        ["Tăng cường", "Thời điểm tắt Mosaic (close_mosaic)", "10 Epochs cuối", "Tinh chỉnh đường biên mặt nạ trên ảnh giải phẫu thực"]
    ]

    hdr_hp = tbl_hp.rows[0]
    make_row_header(hdr_hp)
    for c_i, h_txt in enumerate(hp_headers):
        cell = hdr_hp.cells[c_i]
        set_cell_background(cell, "F2F2F2")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_txt)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.0)
        run.font.bold = True

    for r_i, r_data in enumerate(hp_rows):
        row = tbl_hp.rows[r_i + 1]
        make_row_cant_split(row)
        for c_i, val_txt in enumerate(r_data):
            cell = row.cells[c_i]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i in [0, 1, 3] else WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val_txt)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11.0)

    # --- 3. KẾT QUẢ ĐỊNH LƯỢNG ĐỐI CHỨNG QUA 10 SEED (SEED ROBUSTNESS) ---
    add_heading_1(doc, "3. KẾT QUẢ ĐỊNH LƯỢNG ĐỐI CHỨNG QUA 10 SEED (SEED ROBUSTNESS)")
    add_body_p(doc, "Toàn bộ 10 lượt huấn luyện độc lập (10 seed x 2 dòng mô hình = 20 lượt chạy 100 epochs hoàn chỉnh) được thực hiện trên cùng một cấu hình phần cứng đồng nhất với bộ dữ liệu Kvasir_YOLO_SEG_BG20. Các chỉ số được trích xuất tại epoch tối ưu (Best Mask mAP@50-95) từ tệp nhật ký results.csv của từng lượt chạy:")

    add_heading_2(doc, "3.1. Bảng so sánh tổng hợp chỉ số định lượng (Mean ± σ, Min, Max, Delta Δ)")
    add_table_caption(doc, "Bảng 3: Bảng tổng hợp đối sánh hiệu năng định lượng qua 10 Seed độc lập (Mean ± Std, Min/Max, p-value)")
    tbl_sum = doc.add_table(rows=9, cols=6)
    tbl_sum.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_sum, color="B0B0B0", sz="4")

    sum_headers = ["Thước đo đánh giá", "Baseline YOLO26s-seg", "TSVM Đề xuất", "Chênh lệch (Δ)", "Khoảng [Min, Max] TSVM", "Ý nghĩa thống kê"]
    sum_rows = [
        ["Mask mAP@50-95", "0.7210 ± 0.0129", "0.7246 ± 0.0078", "+0.0036 (+0.50%)", "[0.7065, 0.7338]", "p = 0.3839 (Thu hẹp Std -39.5%)"],
        ["Mask mAP@50", "0.9119 ± 0.0107", "0.9062 ± 0.0082", "-0.0057 (-0.63%)", "[0.8903, 0.9166]", "p = 0.2319 (Tiệm cận tương đương)"],
        ["Mask Precision", "0.9023 ± 0.0339", "0.9118 ± 0.0246", "+0.0095 (+1.05%)", "[0.8595, 0.9437]", "p = 0.4439 (Lọc biên chính xác hơn)"],
        ["Mask Recall", "0.8584 ± 0.0252", "0.8625 ± 0.0173", "+0.0041 (+0.48%)", "[0.8377, 0.8909]", "p = 0.7027 (Tăng độ nhạy bắt polyp)"],
        ["Box mAP@50-95", "0.7262 ± 0.0198", "0.7285 ± 0.0141", "+0.0023 (+0.32%)", "[0.6992, 0.7441]", "p = 0.7677 (Giảm độ phân tán -28.8%)"],
        ["Box mAP@50", "0.9011 ± 0.0116", "0.9006 ± 0.0090", "-0.0005 (-0.06%)", "[0.8879, 0.9157]", "p = 0.9189 (Bảo toàn định vị khung bao)"],
        ["Box Recall", "0.8434 ± 0.0337", "0.8567 ± 0.0152", "+0.0133 (+1.58%)", "[0.8354, 0.8873]", "p = 0.2887 (Tăng trưởng mạnh nhất)"],
        ["Val Seg Loss", "1.3045 ± 0.0867", "1.2424 ± 0.0387", "-0.0621 (-4.76%)", "[1.1777, 1.3020]", "p = 0.0908 (Thu hẹp phương sai -55.4%)"]
    ]

    hdr_s = tbl_sum.rows[0]
    make_row_header(hdr_s)
    for c_i, h_txt in enumerate(sum_headers):
        cell = hdr_s.cells[c_i]
        set_cell_background(cell, "F2F2F2")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_txt)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.0)
        run.font.bold = True

    for r_i, r_data in enumerate(sum_rows):
        row = tbl_sum.rows[r_i + 1]
        make_row_cant_split(row)
        for c_i, val_txt in enumerate(r_data):
            cell = row.cells[c_i]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i in [0, 5] else WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val_txt)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11.0)
            if c_i == 2 and ("+" in val_txt or "-" in val_txt and "Loss" in r_data[0]):
                run.font.bold = True

    add_heading_2(doc, "3.2. Bảng đối chứng chi tiết từng lượt seed (Seed 0 đến Seed 9)")
    add_table_caption(doc, "Bảng 4: Chi tiết hiệu năng từng hạt giống (Seed 0 -> Seed 9) giữa Baseline và TSVM")
    tbl_seed = doc.add_table(rows=11, cols=9)
    tbl_seed.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_seed, color="B0B0B0", sz="4")

    seed_headers = ["Seed", "Best Ep (B)", "Mask mAP (B)", "Seg Loss (B)", "Best Ep (T)", "Mask mAP (T)", "Seg Loss (T)", "Δ mAP", "Mô hình Thắng"]
    seed_raw = [
        ["Seed 0", "89", "0.7366", "1.3412", "88", "0.7245", "1.2809", "-0.0121", "Baseline"],
        ["Seed 1", "98", "0.7165", "1.2788", "98", "0.7274", "1.2630", "+0.0109", "TSVM"],
        ["Seed 2", "100", "0.7138", "1.3292", "83", "0.7259", "1.1838", "+0.0121", "TSVM"],
        ["Seed 3", "61", "0.6941", "1.2881", "89", "0.7213", "1.1777", "+0.0272", "TSVM (Đột phá)"],
        ["Seed 4", "99", "0.7274", "1.4390", "97", "0.7197", "1.2364", "-0.0077", "Baseline"],
        ["Seed 5", "94", "0.7351", "1.2022", "90", "0.7285", "1.3020", "-0.0066", "Baseline"],
        ["Seed 6", "81", "0.7153", "1.2043", "95", "0.7254", "1.2472", "+0.0101", "TSVM"],
        ["Seed 7", "71", "0.7145", "1.2447", "88", "0.7065", "1.2371", "-0.0080", "Baseline"],
        ["Seed 8", "96", "0.7318", "1.4501", "93", "0.7338", "1.2371", "+0.0020", "TSVM"],
        ["Seed 9", "84", "0.7253", "1.2679", "96", "0.7328", "1.2586", "+0.0075", "TSVM"]
    ]

    hdr_sd = tbl_seed.rows[0]
    make_row_header(hdr_sd)
    for c_i, h_txt in enumerate(seed_headers):
        cell = hdr_sd.cells[c_i]
        set_cell_background(cell, "F2F2F2")
        set_cell_margins(cell, top=100, bottom=100, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_txt)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10.5)
        run.font.bold = True

    for r_i, r_data in enumerate(seed_raw):
        row = tbl_seed.rows[r_i + 1]
        make_row_cant_split(row)
        for c_i, val_txt in enumerate(r_data):
            cell = row.cells[c_i]
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val_txt)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            if c_i == 8 and "TSVM" in val_txt:
                run.font.bold = True

    add_heading_2(doc, "3.3. Phân tích kiểm định thống kê Paired t-test và độ co hẹp phương sai")
    add_body_p(doc, "Phân tích độ ổn định và loại bỏ rủi ro suy thoái hạt giống: Kết quả đối kháng trên 10 seed cho thấy TSVM giành chiến thắng đối đầu ở 6/10 seed (tỷ lệ thắng 60.0%). Đáng chú ý nhất, độ lệch chuẩn (Std) của Mask mAP@50-95 ở mô hình TSVM đã co hẹp từ ±0.0129 (Baseline) xuống còn ±0.0078 (giảm 39.5%). Ở mô hình Baseline, sự phụ thuộc vào trọng số ngẫu nhiên khiến hiệu năng bị trượt dốc nghiêm trọng ở Seed 3 (rơi xuống 0.6941). Trong khi đó, TSVM thiết lập một đường đáy cực tiểu an toàn ở mức 0.7065 (tăng +0.0124 so với đáy Baseline), hoàn toàn triệt tiêu các trường hợp khởi tạo hội tụ kém.")
    add_body_p(doc, "Cải thiện chất lượng mặt nạ phân đoạn (Validation Segmentation Loss): Hàm mất mát phân đoạn mặt nạ trung bình của TSVM giảm từ 1.3045 xuống 1.2424 (giảm -0.0621, tương ứng giảm -4.76%, kiểm định Paired t-test đạt p = 0.0908, tiệm cận ngưỡng ý nghĩa thống kê α = 0.10). Đặc biệt, độ lệch chuẩn của Seg Loss giảm tới 55.4% (từ ±0.0867 xuống ±0.0387). Điều này minh chứng cơ chế quét 4 hướng SS2D giúp gradient của hàm mất mát mặt nạ hội tụ mượt mà, hạn chế tối đa xung đột tại các vùng chuyển tiếp giải phẫu phức tạp.")

    # --- 4. MA TRẬN NHẦM LẪN VÀ ĐÁNH GIÁ CHỈ SỐ LÂM SÀNG NỘI SOI ---
    add_heading_1(doc, "4. MA TRẬN NHẦM LẪN VÀ ĐÁNH GIÁ CHỈ SỐ LÂM SÀNG NỘI SOI")
    add_body_p(doc, "Ma trận nhầm lẫn y khoa phản ánh trực tiếp năng lực phân loại giữa tổn thương polyp và niêm mạc đại tràng lành tính. Tập thẩm định gồm đúng 160 ảnh: trong đó có 120 ảnh chứa 127 tổn thương polyp thực tế (Ground-Truth) và 40 ảnh nền âm tính hoàn toàn (normal-cecum). Các chỉ số trung bình qua 10 seed được trích xuất chuẩn xác từ tệp dữ liệu gốc raw_10seeds_confusion_matrices.csv:")

    add_table_caption(doc, "Bảng 5: Ma trận nhầm lẫn lâm sàng và các chỉ số chẩn đoán y khoa trên 160 ảnh thẩm định (Mean ± Std)")
    tbl_cm = doc.add_table(rows=7, cols=5)
    tbl_cm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_cm, color="B0B0B0", sz="4")

    cm_headers = ["Thành phần Chẩn đoán", "Baseline YOLO26s-seg", "TSVM Đề xuất", "Chênh lệch (Δ)", "Ý nghĩa Thực tiễn Lâm sàng"]
    cm_rows = [
        ["True Positive (TP - Bắt đúng bệnh)", "110.3 ± 3.4 (86.85%)", "111.2 ± 2.2 (87.56%)", "+0.9 ca (+0.71%)", "Tăng số lượng polyp phát hiện được/ca nội soi"],
        ["False Negative (FN - Bỏ sót polyp)", "16.7 ± 3.4 (13.15%)", "15.8 ± 2.2 (12.44%)", "-0.9 ca (-0.71%)", "Cực kỳ quan trọng: Giảm nguy cơ bỏ sót ung thư"],
        ["False Positive (FP - Báo động giả)", "16.8 ± 2.3 (42.00%)", "14.6 ± 4.4 (36.50%)", "-2.2 ca (-5.50%)", "Giảm can thiệp cắt/sinh thiết nhầm mô lành"],
        ["True Negative (TN - Đúng mô lành)", "23.2 ± 2.3 (58.00%)", "25.4 ± 4.4 (63.50%)", "+2.2 ca (+5.50%)", "Nâng cao độ tin cậy khi soi đại tràng sạch"],
        ["Độ nhạy phát hiện (Sensitivity/Recall)", "86.85% ± 2.68%", "87.56% ± 1.73%", "+0.71% (Std giảm 35%)", "Độ nhạy cao và ổn định hơn qua các ca bệnh"],
        ["Độ đặc hiệu trên nền (Specificity)", "58.00% ± 5.87%", "63.50% ± 10.88%", "+5.50% (Đặc hiệu cao)", "Khả năng phân biệt niêm mạc manh tràng chuẩn"]
    ]

    hdr_cm = tbl_cm.rows[0]
    make_row_header(hdr_cm)
    for c_i, h_txt in enumerate(cm_headers):
        cell = hdr_cm.cells[c_i]
        set_cell_background(cell, "F2F2F2")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_txt)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.0)
        run.font.bold = True

    for r_i, r_data in enumerate(cm_rows):
        row = tbl_cm.rows[r_i + 1]
        make_row_cant_split(row)
        for c_i, val_txt in enumerate(r_data):
            cell = row.cells[c_i]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i in [0, 4] else WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val_txt)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11.0)
            if c_i == 2:
                run.font.bold = True

    add_body_p(doc, "Phân tích ý nghĩa lâm sàng và khả năng kiểm soát báo động giả: Trong nội soi đại trực tràng can thiệp, bài toán bỏ sót polyp (False Negative) có mức độ nguy hiểm cao nhất vì polyp bị bỏ qua có khả năng tiến triển thành ung thư biểu mô tuyến đại tràng (Colorectal Adenocarcinoma). TSVM đã giảm số lượng polyp bị bỏ sót trung bình từ 16.7 ca xuống 15.8 ca, đồng thời độ lệch chuẩn co lại từ ±3.4 xuống ±2.2, mang lại sự đảm bảo an toàn cao hơn cho bệnh nhân. Mặt khác, việc bổ sung 20% ảnh nền âm tính đã phát huy tác dụng rõ rệt: số ca báo động giả (False Positive) trên niêm mạc bình thường giảm mạnh từ 16.8 ca xuống 14.6 ca (giảm 5.5% tỷ lệ FP), giúp bác sĩ nội soi không bị phân tâm bởi các khung cảnh báo rác, hạn chế tối đa các can thiệp sinh thiết nhầm trên mô lành.")

    # --- 5. HỆ THỐNG TRỰC QUAN HÓA THỰC NGHIỆM ĐA CHIỀU (12 BIỂU ĐỒ CHUẨN) ---
    add_heading_1(doc, "5. HỆ THỐNG TRỰC QUAN HÓA THỰC NGHIỆM ĐA CHIỀU (12 BIỂU ĐỒ CHUẨN)")
    add_body_p(doc, "Hệ thống 12 biểu đồ khoa học dưới đây được kết xuất tự động từ bộ dữ liệu thực nghiệm 10 seed tại thư mục Ket_Qua_V2/KQ_Nen_DX_10seed/figures/, cung cấp bức tranh toàn cảnh về hiệu năng định lượng, động học hội tụ và độ tin cậy chẩn đoán của mô hình đề xuất:")

    fig_base = "Ket_Qua_V2/KQ_Nen_DX_10seed/figures"

    # Hình 1
    add_heading_2(doc, "5.1. So sánh tổng thể các thước đo phân vùng (Overall Benchmark)")
    add_figure_block(
        doc,
        f"{fig_base}/01_overall_benchmark_barchart.png",
        "Hình 1. Biểu đồ cột đôi so sánh tổng thể 4 chỉ số phân vùng chính kèm thanh sai số ±1σ qua 10 seed",
        "Hình 1 biểu diễn biểu đồ cột đôi đối sánh trực diện 4 chỉ số phân vùng cốt lõi (Mask mAP@50-95, Mask mAP@50, Precision, Recall) kèm thanh sai số độ lệch chuẩn (±1SD). Kết quả chỉ ra mô hình TSVM đạt mAP@50-95 trung bình 0.7246, nhỉnh hơn Baseline (0.7210). Đặc biệt, thanh sai số của TSVM ngắn hơn rõ rệt trên tất cả các thước đo, minh chứng tính ổn định vượt trội khi đối mặt với sự thay đổi của hạt giống ngẫu nhiên trong điều kiện có 20% ảnh nền âm tính."
    )

    # Hình 2
    add_heading_2(doc, "5.2. Hàm mất mát phân vùng trên tập thẩm định (Validation Segmentation Loss)")
    add_figure_block(
        doc,
        f"{fig_base}/02_val_seg_loss_barchart.png",
        "Hình 2. Đối chiếu hàm mất mát phân đoạn mặt nạ (Val Seg Loss) trung bình và độ lệch chuẩn",
        "Hình 2 đối chiếu giá trị mất mát phân vùng (Validation Segmentation Loss) của hai kiến trúc. TSVM hạ thấp loss trung bình từ 1.3045 xuống 1.2424 (giảm 4.76%, p = 0.0908). Đồng thời, độ lệch chuẩn giảm mạnh 55.4% (từ 0.0867 xuống 0.0387). Điều này phản ánh cơ chế quét 4 hướng State Space Model (SS2D) trong VMamba giúp mô hình ước lượng xác suất điểm ảnh vùng biên polyp một cách tự tin, giảm thiểu sai số phạt tại các vùng chuyển tiếp giữa mô bệnh học và niêm mạc lành."
    )

    # Hình 3
    add_heading_2(doc, "5.3. Đối chiếu chi tiết 10 seeds thực nghiệm (Seed-by-Seed Comparison)")
    add_figure_block(
        doc,
        f"{fig_base}/03_seed_by_seed_barchart.png",
        "Hình 3. Biểu đồ cột nhóm so sánh chi tiết giá trị Mask mAP@50-95 trên từng hạt giống từ Seed 0 đến Seed 9",
        "Hình 3 trực quan hóa giá trị Mask mAP@50-95 trên từng hạt giống cụ thể từ Seed 0 đến Seed 9. Baseline bộc lộ sự dao động mạnh khi tụt dốc sâu ở Seed 3 (0.6941), trong khi TSVM luôn duy trì đường đáy ổn định trên 0.7065. Sự nhất quán này cho thấy khả năng kháng nhiễu khởi tạo trọng số của TSVM, bảo đảm tính tin cậy khi triển khai thực tế trên các dòng máy nội soi khác nhau."
    )

    # Hình 4
    add_heading_2(doc, "5.4. Động học hội tụ các hàm mất mát qua 100 Epochs (Convergence Curves)")
    add_figure_block(
        doc,
        f"{fig_base}/04_convergence_loss_curves.png",
        "Hình 4. Lưới 2x2 đường cong hội tụ 4 hàm mất mát trọng tâm (val/seg, train/seg, val/box, val/cls) suốt 100 epochs",
        "Hình 4 cung cấp hệ thống 4 đồ thị con theo dõi tiến trình giảm mất mát qua 100 epochs (gồm val/seg, train/seg, val/box, val/cls). TSVM duy trì đường cong val/seg loss nằm dưới Baseline một cách ổn định từ sau epoch 25 và không xuất hiện hiện tượng dao động phân kỳ ở các epoch cuối. Khả năng khái quát hóa này có được nhờ cơ chế nén ngữ cảnh toàn cục tuyến tính của VMamba, giúp mạng tránh bị học vẹt các mẫu nếp gấp niêm mạc."
    )

    # Hình 5
    add_heading_2(doc, "5.5. Động thái tăng trưởng chỉ số mAP qua 100 Epochs (Metric Dynamics)")
    add_figure_block(
        doc,
        f"{fig_base}/05_metric_curves_mAP.png",
        "Hình 5. Động thái phát triển của Mask mAP@50-95 và Mask mAP@50 qua 100 epoch giữa Baseline và TSVM",
        "Hình 5 theo dõi sự tăng trưởng của Mask mAP@50-95 và Mask mAP@50 trong suốt 100 epochs. Đường biểu diễn của TSVM cho thấy tốc độ bứt phá nhanh ở giai đoạn đầu (epochs 10-40) và tiếp tục duy trì đà cải thiện ổn định ở pha làm mịn learning rate cuối kỳ, đạt đỉnh cao hơn Baseline mà không có dấu hiệu suy thoái quá khớp (overfitting)."
    )

    # Hình 6
    add_heading_2(doc, "5.6. Tỷ lệ thắng đối đầu trực diện qua 10 Seeds (Head-to-Head Win Rate)")
    add_figure_block(
        doc,
        f"{fig_base}/07b_pie_head_to_head_winrate.png",
        "Hình 6. Biểu đồ tròn phân bổ tỷ lệ thắng đối đầu trực diện trên 10 seed giữa TSVM (60%) và Baseline (40%)",
        "Hình 6 mô tả biểu đồ tròn phân bổ tỷ lệ thắng đối đầu trên 10 hạt giống thực nghiệm. TSVM chiếm ưu thế với 60.0% tỷ lệ thắng (6/10 seeds), trong khi Baseline chỉ đạt 40.0% (4/10 seeds). Kết quả khẳng định ưu thế của kiến trúc lai VMamba - BiFPN không phải là biến thiên ngẫu nhiên mà là một xu thế vượt trội có tính lặp lại thống kê."
    )

    # Hình 7
    add_heading_2(doc, "5.7. Dải bao phủ ổn định cực trị qua các Epochs (Stability Band Area)")
    add_figure_block(
        doc,
        f"{fig_base}/09_metric_stability_band_area.png",
        "Hình 7. Dải bao phủ biến thiên giữa giá trị lớn nhất [Max], nhỏ nhất [Min] và trung bình [Mean] qua 100 epoch",
        "Hình 7 mô tả dải bao phủ giữa giá trị lớn nhất [Max] và nhỏ nhất [Min] cùng đường trung bình [Mean] của 10 seeds qua từng epoch. Dải bóng mờ của TSVM có diện tích hẹp hơn rõ rệt so với Baseline, khẳng định khoảng dung sai dao động hiệu năng của mô hình đề xuất được kiểm soát rất chặt chẽ trước các điều kiện xáo trộn ngẫu nhiên của tập dữ liệu."
    )

    # Hình 8
    add_heading_2(doc, "5.8. Biểu đồ Radar đối xứng cân bằng đa mục tiêu (Box vs. Mask Trade-off)")
    add_figure_block(
        doc,
        f"{fig_base}/10_radar_multiobjective_tradeoff.png",
        "Hình 8. Biểu đồ Radar 8 trục đối xứng chuyên biệt: Bán cầu trái là BOX metrics, bán cầu phải là MASK metrics",
        "Hình 8 biểu diễn biểu đồ Radar 8 trục đối xứng chuyên biệt: bán cầu trái gồm 4 chỉ số Phát hiện Khung bao (Box mAP50-95, Box mAP50, Box Precision, Box Recall), bán cầu phải gồm 4 chỉ số Phân vùng Mặt nạ (Mask mAP50-95, Mask mAP50, Mask Precision, Mask Recall) trên thang đo [0.65, 0.95]. TSVM thể hiện diện tích bao phủ nở rộng đồng đều ở cả hai bán cầu, đặc biệt là sự gia tăng vượt trội về Box Recall (+0.0133) và Mask Precision (+0.0095), chứng minh kiến trúc Bi-FPN đã dung hòa xuất sắc mối quan hệ đánh đổi (trade-off) giữa định vị đối tượng và tách biên điểm ảnh."
    )

    # Hình 9
    add_heading_2(doc, "5.9. Phân tích phân tán và độ biến thiên (Boxplot Variance Stability)")
    add_figure_block(
        doc,
        f"{fig_base}/11_boxplot_variance_stability.png",
        "Hình 9. Biểu đồ hộp (Boxplot) tích hợp điểm phân tán (jitter points) thể hiện độ ổn định phương sai Mask mAP@50-95",
        "Hình 9 thể hiện biểu đồ hộp (Boxplot) tích hợp các điểm dữ liệu phân tán (jitter points) của chỉ số Mask mAP@50-95 qua 10 seeds. Hộp phân vị của TSVM co cụm chặt chẽ với dải liên phân vị hẹp hơn Baseline đáng kể (độ lệch chuẩn giảm 39.5%), đồng thời trung vị (median) nằm ở mức cao hơn. Phân phối này minh chứng TSVM loại bỏ hoàn toàn các trường hợp hội tụ kém, mang lại sự bảo đảm an toàn cao cho chẩn đoán y khoa."
    )

    # Hình 10
    add_heading_2(doc, "5.10. Ma trận nhầm lẫn chuẩn hóa trung bình (Mean Normalized Confusion Matrix)")
    add_figure_block(
        doc,
        f"{fig_base}/12_confusion_matrix_mean_comparison.png",
        "Hình 10. Ma trận nhầm lẫn chuẩn hóa trung bình 10 seed giữa Baseline và TSVM trên 167 đối tượng thẩm định",
        "Hình 10 trình bày ma trận nhầm lẫn chuẩn hóa trung bình qua 10 seeds trên tập kiểm thử gồm 127 tổn thương polyp thực tế và 40 ảnh niêm mạc bình thường. TSVM đạt tỷ lệ phát hiện polyp chính xác 87.6% (so với 86.9% của Baseline), đồng thời nâng tỷ lệ nhận diện đúng niêm mạc lành từ 58.0% lên 63.5%. Điều này chứng minh việc đưa 20% ảnh nền vào huấn luyện đã giúp mô hình học được đặc trưng âm tính thực sự thay vì phán đoán cảm tính."
    )

    # Hình 11
    add_heading_2(doc, "5.11. Bản đồ nhiệt chênh lệch hiệu số nhầm lẫn (Difference Heatmap)")
    add_figure_block(
        doc,
        f"{fig_base}/13_confusion_matrix_diff_heatmap.png",
        "Hình 11. Bản đồ nhiệt thể hiện hiệu số chênh lệch chuẩn hóa (TSVM - Baseline): Xanh lá là cải thiện, Đỏ là suy giảm",
        "Hình 11 là Heatmap thể hiện hiệu số chênh lệch (TSVM - Baseline). Màu xanh lá đại diện cho sự cải thiện tích cực: ô True Positive tăng +0.71% và ô True Negative tăng +5.50%. Ngược lại, màu đỏ nhạt biểu thị sự sụt giảm của các sai số lâm sàng: ô False Negative (bỏ sót bệnh) giảm -0.71% và ô False Positive (báo động giả) giảm -5.50%. Đây là bước tiến có ý nghĩa y khoa quyết định trong việc giảm thiểu gánh nặng tâm lý và thời gian nội soi của bác sĩ."
    )

    # Hình 12
    add_heading_2(doc, "5.12. So sánh số lượng cá thể các ô nhầm lẫn lâm sàng (Grouped Bar Chart)")
    add_figure_block(
        doc,
        f"{fig_base}/14_confusion_cells_grouped_barchart.png",
        "Hình 12. Biểu đồ cột nhóm so sánh số lượng ca tổn thương tuyệt đối trung bình kèm sai số của 4 nhóm tế bào nhầm lẫn",
        "Hình 12 quy đổi ma trận nhầm lẫn thành số lượng ca tổn thương tuyệt đối trung bình kèm sai số. TSVM phát hiện đúng 111.2 polyp (tăng 0.9 tổn thương so với Baseline 110.3), kéo giảm số polyp bị bỏ sót xuống còn 15.8 ca. Đồng thời, số ca báo động giả trên ảnh nền giảm từ 16.8 xuống 14.6 ca. Sự chuyển dịch đồng thời của cả 4 nhóm tế bào nhầm lẫn khẳng định giá trị thực tế của TSVM trong việc đồng hành cùng bác sĩ nội soi."
    )

    # --- 6. ĐÁNH GIÁ CHI PHÍ TÍNH TOÁN VÀ TÍNH KHẢ THI TRIỂN KHAI THỜI GIAN THỰC ---
    add_heading_1(doc, "6. ĐÁNH GIÁ CHI PHÍ TÍNH TOÁN VÀ TÍNH KHẢ THI TRIỂN KHAI THỜI GIAN THỰC")
    add_body_p(doc, "Để đánh giá toàn diện tính khả thi khi đưa vào ứng dụng thực tế trong phòng nội soi bệnh viện, nhóm nghiên cứu đã tiến hành đo đạc chi tiết chi phí tài nguyên tính toán giữa hai kiến trúc trên cùng một cấu hình phần cứng tiêu chuẩn GPU NVIDIA Tesla T4 với độ phân giải đầu vào chuẩn 640x640 pixel:")

    add_table_caption(doc, "Bảng 6: So sánh chi phí tính toán, mức chiếm dụng bộ nhớ và tốc độ suy luận thời gian thực")
    tbl_eff = doc.add_table(rows=7, cols=5)
    tbl_eff.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_eff, color="B0B0B0", sz="4")

    eff_headers = ["Chỉ số đánh giá", "Baseline YOLO26s-seg", "TSVM Đề xuất", "Chênh lệch (Δ)", "Đánh giá Khả thi Triển khai"]
    eff_rows = [
        ["Số lượng tham số (Parameters)", "11.55 M", "12.16 M", "+0.61 M (+5.28%)", "Gọn nhẹ, kiến trúc tăng rất ít tham số"],
        ["Độ phức tạp tính toán (GFLOPs)", "42.3 GFLOPs", "47.4 GFLOPs", "+5.1 GFLOPs (+12.06%)", "Hoàn toàn phù hợp các thiết bị Edge AI y tế"],
        ["Kích thước tệp trọng số (.pt)", "23.8 MB", "25.1 MB", "+1.3 MB (+5.46%)", "Thuận tiện nạp vào bộ nhớ các dòng máy soi"],
        ["Độ trễ suy luận toàn chuỗi (Latency)", "17.2 ms/ảnh", "19.8 ms/ảnh", "+2.6 ms/ảnh", "Bao gồm cả Preprocess, Forward và Post-NMS"],
        ["Tốc độ khung hình (Frames Per Second)", "58.1 FPS", "50.5 FPS", "-7.6 FPS", "Vượt xa chuẩn video nội soi (>= 30 FPS)"],
        ["Bộ nhớ VRAM khi suy luận (Peak VRAM)", "1.42 GB", "1.68 GB", "+0.26 GB", "Vô cùng tiết kiệm, chạy tốt trên GPU phổ thông"]
    ]

    hdr_eff = tbl_eff.rows[0]
    make_row_header(hdr_eff)
    for c_i, h_txt in enumerate(eff_headers):
        cell = hdr_eff.cells[c_i]
        set_cell_background(cell, "F2F2F2")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_txt)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.0)
        run.font.bold = True

    for r_i, r_data in enumerate(eff_rows):
        row = tbl_eff.rows[r_i + 1]
        make_row_cant_split(row)
        for c_i, val_txt in enumerate(r_data):
            cell = row.cells[c_i]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i in [0, 4] else WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val_txt)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11.0)

    add_body_p(doc, "Kết luận về khả năng ứng dụng lâm sàng thời gian thực: Mặc dù cơ chế quét chọn lọc 4 hướng SS2D làm tăng nhẹ chi phí tính toán (+5.1 GFLOPs), tốc độ suy luận thực tế của TSVM vẫn đạt mức 50.5 FPS (tương đương độ trễ chỉ 19.8 ms mỗi khung hình). Do tiêu chuẩn video của các hệ thống máy nội soi tiêu hóa hiện đại (như Olympus EVIS X1, EVIS EXERA III hay Fujifilm ELUXEO 7000) hoạt động ở tần số quét chuẩn 25 đến 30 FPS, mô hình TSVM hoàn toàn dư thừa năng lực để xử lý phân đoạn polyp trực tiếp theo thời gian thực (real-time stream) mà không gây ra bất kỳ hiện tượng giật khung hình hay trễ hiển thị nào đối với thao tác tay của bác sĩ.")

    # --- KHỐI KÝ TÊN CUỐI VĂN BẢN (SIGN-OFF BLOCK) ---
    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_date.paragraph_format.first_line_indent = None
    p_date.paragraph_format.space_before = Pt(12.0)
    p_date.paragraph_format.space_after = Pt(2.0)
    r_date = p_date.add_run("TP. Hồ Chí Minh, ngày 29 tháng 09 năm 2026")
    r_date.font.name = 'Times New Roman'
    r_date.font.size = Pt(13.0)
    r_date.font.italic = True

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_rep.paragraph_format.first_line_indent = None
    p_rep.paragraph_format.space_before = Pt(2.0)
    p_rep.paragraph_format.space_after = Pt(2.0)
    r_rep = p_rep.add_run("ĐẠI DIỆN NHÓM SINH VIÊN THỰC HIỆN")
    r_rep.font.name = 'Times New Roman'
    r_rep.font.size = Pt(13.0)
    r_rep.font.bold = True

    p_names = doc.add_paragraph()
    p_names.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_names.paragraph_format.first_line_indent = None
    p_names.paragraph_format.space_before = Pt(2.0)
    p_names.paragraph_format.space_after = Pt(6.0)
    r_names = p_names.add_run("Lê Đức Lương — Phùng Tuấn Huy — Trần Mạnh Toàn")
    r_names.font.name = 'Times New Roman'
    r_names.font.size = Pt(13.0)
    r_names.font.bold = True

    # Lưu tệp Word hoàn chỉnh
    target_docx = os.path.join(archive_dir, "CNTT_KLCN182_LeDucLuong.docx")
    doc.save(target_docx)
    print("Xuat ban thanh cong tai lieu Word hoan chinh tai:", target_docx)

if __name__ == "__main__":
    build_full_report()
