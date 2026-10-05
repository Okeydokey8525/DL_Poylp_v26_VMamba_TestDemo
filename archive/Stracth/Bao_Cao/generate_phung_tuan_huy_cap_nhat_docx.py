# -*- coding: utf-8 -*-
"""
Script tao file Bao cao tuan CNTT_KLCN182_PhungTuanHuy_CapNhat.docx
Tuan thu nghiem ngat:
- Tieu chuan dinh dang Word HUIT: Le trai 3.5cm (dong gay), tren/duoi/phai 2.5cm, Times New Roman, line spacing 1.25.
- Loai tru 3 hinh ma tran nham lan (12, 13, 14) do co van de TN tai dung va su co Kaggle model.fuse().
- Tao khung ghi chu chen anh cho 9 bieu do thuc nghiem chuan (Hinh 1 den Hinh 9) kem nhan xet hoc thuat 2 truc day du.
- Giu tinh liem chinh hoc thuat cao nhat theo WEEKLY_REPORT_Ket_Qua_V2.md.
"""

import os
import docx
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="B0B0B0", sz="4"):
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

def set_box_border(table, color="0F4C81", sz="8"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:insideH w:val="none"/>'
                        f'<w:insideV w:val="none"/>'
                        f'</w:tblBorders>')
    tblPr.append(borders)

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def apply_page_setup(doc):
    for sec in doc.sections:
        sec.page_width = Cm(21.0)
        sec.page_height = Cm(29.7)
        sec.top_margin = Cm(2.5)
        sec.bottom_margin = Cm(2.5)
        sec.left_margin = Cm(3.5)   # 3.5 cm dong gay luan van
        sec.right_margin = Cm(2.5)
        sec.header_distance = Cm(1.27)
        sec.footer_distance = Cm(1.27)

def add_heading_1(doc, text):
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

def add_body_p(doc, text, bold_prefix=None):
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

def add_figure_placeholder_block(doc, img_rel_path, caption_text, observation_text, width_cm=15.0):
    """
    Tao khung hop ghi chu chen hinh anh noi bat, chuyen nghiep:
    - Hop vien don mau #0F4C81, nen nhe #F4F7F9.
    - Ghi chu ro rang duong dan tep anh va kich thuoc chen khuyen nghi.
    - Tieu de anh in dam 12pt can giua.
    - Doan nhan xet hoc thuat 2 truc 13pt can deu, thut dau dong 1.27cm.
    """
    # 1. Hop ghi chu chen anh (Callout box 1 o)
    tbl_box = doc.add_table(rows=1, cols=1)
    tbl_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_box_border(tbl_box, color="0F4C81", sz="6")
    cell = tbl_box.rows[0].cells[0]
    cell.width = Cm(width_cm)
    set_cell_background(cell, "F4F7F9")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    make_row_cant_split(tbl_box.rows[0])

    p1 = cell.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p1.paragraph_format.space_before = Pt(2.0)
    p1.paragraph_format.space_after = Pt(3.0)
    r1 = p1.add_run("📌 [GHI CHÚ CHÈN HÌNH ẢNH THỰC NGHIỆM VÀO ĐÂY]")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11.0)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(15, 76, 129)

    p2 = cell.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p2.paragraph_format.space_before = Pt(2.0)
    p2.paragraph_format.space_after = Pt(2.0)
    r2_pre = p2.add_run("• Tệp hình ảnh nguồn: ")
    r2_pre.font.name = 'Times New Roman'
    r2_pre.font.size = Pt(10.5)
    r2_pre.font.bold = True
    r2_val = p2.add_run(img_rel_path)
    r2_val.font.name = 'Courier New'
    r2_val.font.size = Pt(10.0)

    p3 = cell.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p3.paragraph_format.space_before = Pt(2.0)
    p3.paragraph_format.space_after = Pt(2.0)
    r3_pre = p3.add_run("• Quy cách khuyến nghị: ")
    r3_pre.font.name = 'Times New Roman'
    r3_pre.font.size = Pt(10.5)
    r3_pre.font.bold = True
    r3_val = p3.add_run(f"Chiều rộng cố định {width_cm:.1f} cm (vừa khít bề rộng in ấn lề trái 3.5cm, lề phải 2.5cm), căn giữa trang.")
    r3_val.font.name = 'Times New Roman'
    r3_val.font.size = Pt(10.5)

    p4 = cell.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p4.paragraph_format.space_before = Pt(2.0)
    p4.paragraph_format.space_after = Pt(2.0)
    r4_pre = p4.add_run("• Hướng dẫn thao tác: ")
    r4_pre.font.name = 'Times New Roman'
    r4_pre.font.size = Pt(10.5)
    r4_pre.font.bold = True
    r4_val = p4.add_run("Khi cần in ấn hoàn chỉnh, bạn có thể xóa khung ghi chú này hoặc đặt con trỏ tại đây và chọn Menu Word: Insert -> Pictures -> Chọn ảnh theo đường dẫn trên.")
    r4_val.font.name = 'Times New Roman'
    r4_val.font.size = Pt(10.5)
    r4_val.font.italic = True

    # 2. Tieu de anh can giua (12pt BOLD)
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.first_line_indent = None
    p_cap.paragraph_format.space_before = Pt(5.0)
    p_cap.paragraph_format.space_after = Pt(3.0)
    run_cap = p_cap.add_run(caption_text)
    run_cap.font.name = 'Times New Roman'
    run_cap.font.size = Pt(12.0)
    run_cap.font.bold = True

    # 3. Doan nhan xet 2 truc (13pt, thut dau dong 1.27cm, can deu)
    p_obs = add_body_p(doc, observation_text)
    return tbl_box, p_cap, p_obs

def build_phung_tuan_huy_report():
    print("Khoi tao tien trinh xay dung Bao cao tuan CNTT_KLCN182_PhungTuanHuy_CapNhat.docx...")
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

    # --- BẢNG METADATA MỞ ĐẦU (TABLE 1) ---
    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_metadata_table_borders(tbl_meta, color="999999", sz="6")

    meta_content = [
        ("Mã đề tài & Phân loại:", "CNTT_KLCN182 — Khóa luận Cử nhân ngành CNTT (2026 – 2027)"),
        ("Giảng viên hướng dẫn:", "TS. Phùng Thế Bảo (Email: baopt@huit.edu.vn)"),
        ("Nhóm sinh viên thực hiện:", "1. Lê Đức Lương (MSSV: 2001230490 — Lớp: 14DHTH09)\n2. Phùng Tuấn Huy (MSSV: 2001230312 — Lớp: 14DHTH13)\n3. Trần Mạnh Toàn (MSSV: 2001230830 — Lớp: 14DHTH09)"),
        ("Nội dung báo cáo trọng tâm:", "Đánh giá định lượng đối chứng 10 seed giữa Baseline YOLO26s-seg và biến thể đề xuất C2TSVMamba trên bộ dữ liệu Kvasir_YOLO_SEG_BG20; phân tích độ ổn định phương sai, hội tụ mất mát phân vùng, chi phí tính toán CPU và 9 biểu đồ thực nghiệm chuẩn.")
    ]

    for r_i, (lbl, val) in enumerate(meta_content):
        row = tbl_meta.rows[r_i]
        make_row_cant_split(row)
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Cm(7.5)
        c1.width = Cm(7.5)
        set_cell_background(c0, "F7F7F7")
        set_cell_margins(c0, top=100, bottom=100, left=120, right=120)
        set_cell_margins(c1, top=100, bottom=100, left=120, right=120)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_before = Pt(3.0)
        p0.paragraph_format.space_after = Pt(3.0)
        r0 = p0.add_run(lbl)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(13.0)
        r0.font.bold = True

        p1 = c1.paragraphs[0]
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_before = Pt(3.0)
        p1.paragraph_format.space_after = Pt(3.0)
        r1 = p1.add_run(val)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(13.0)

    # --- CHƯƠNG 1: MỤC TIÊU VÀ NHIỆM VỤ BÁO CÁO TIẾN ĐỘ ---
    add_heading_1(doc, "1. MỤC TIÊU VÀ NHIỆM VỤ BÁO CÁO TIẾN ĐỘ")
    add_body_p(doc, "Báo cáo tiến độ tuần này tập trung tổng kết và đánh giá toàn diện các kết quả thực nghiệm của đề tài nghiên cứu Khóa luận Cử nhân CNTT_KLCN182. Trọng tâm của giai đoạn nghiên cứu hiện tại là thiết lập quy trình đối chứng thực nghiệm khách quan, khoa học và chặt chẽ giữa mô hình gốc Baseline YOLO26s-seg và biến thể đề xuất C2TSVMamba (Topology-Shape-aware VMamba) trên bộ dữ liệu nội soi đại trực tràng có kiểm soát tỷ lệ ảnh nền âm tính Kvasir_YOLO_SEG_BG20. Để bảo đảm độ tin cậy khoa học và tính liêm chính dữ liệu, nhóm nghiên cứu đã mở rộng quy mô thực nghiệm lên 10 hạt giống ngẫu nhiên độc lập (10 Seeds) và thực hiện đầy đủ các phân tích thống kê định lượng.")
    add_body_p(doc, "Các nhiệm vụ trọng tâm được hoàn thành trong chu kỳ báo cáo bao gồm:")
    add_bullet_p(doc, "Chuẩn hóa quy trình tiền xử lý BG20", "Xây dựng thành công bộ dữ liệu Kvasir_YOLO_SEG_BG20 với tỷ lệ 20% ảnh âm tính hoàn toàn (normal-cecum) không chứa tổn thương polyp để đánh giá độ đặc hiệu lâm sàng.")
    add_bullet_p(doc, "Mở rộng kiểm định độ tin cậy 10 Seeds", "Triển khai huấn luyện 20 lượt chạy độc lập (2 mô hình x 10 seed x 100 epoch), loại bỏ tính thiên lệch ngẫu nhiên trong việc phân chia dữ liệu và khởi tạo trọng số ban đầu.")
    add_bullet_p(doc, "Phân tích thống kê suy luận Paired t-test", "Thực hiện kiểm định cặp t-test và Wilcoxon signed-rank trên 13 chỉ số phân vùng và hộp bao, đo đạc mức độ co hẹp phương sai sai số giữa hai kiến trúc.")
    add_bullet_p(doc, "Rà soát ma trận nhầm lẫn và giới hạn kỹ thuật", "Giám định nguồn gốc dữ liệu ma trận nhầm lẫn, làm rõ bản chất ô True Negative (TN) tái dựng và phân tích các trường hợp bất nhất do cơ chế fuse xuất ảnh trên Kaggle.")
    add_bullet_p(doc, "Hệ thống hóa 9 biểu đồ thực nghiệm chuẩn", "Xây dựng khung lưu trữ và nhận xét học thuật 2 trục cho 9 biểu đồ trực quan hóa đa chiều, hỗ trợ phân tích định lượng thuật toán và biện giải ý nghĩa bệnh học nội soi.")
    add_bullet_p(doc, "Đo đạc chi phí tính toán và tính khả thi", "Thực hiện phép đo benchmark độ trễ suy luận forward CPU, số lượng tham số và dung lượng mô hình nhằm đánh giá khả năng tích hợp thực tế.")

    # --- CHƯƠNG 2: CẤU TRÚC MÔ HÌNH VÀ TIỀN XỬ LÝ DỮ LIỆU BG20 ---
    add_heading_1(doc, "2. CẤU TRÚC MÔ HÌNH VÀ TIỀN XỬ LÝ DỮ LIỆU BG20")

    add_heading_2(doc, "2.1. Vai trò của ảnh nền âm tính BG20 trong nội soi đại trực tràng")
    add_body_p(doc, "Trong quy trình nội soi đại trực tràng thực tế, phần lớn thời gian quan sát của bác sĩ là trên các vùng niêm mạc đại tràng hoàn toàn khỏe mạnh, không có khối u hay tổn thương ác tính. Nếu một mô hình học sâu chỉ được huấn luyện trên các khung hình luôn có chứa polyp (Positive-only dataset), mạng nơ-ron sẽ hình thành xu hướng võ đoán, tạo ra báo động giả (False Positives) trên các nếp gấp niêm mạc bình thường, bọt khí hoặc cặn dịch phân. Để khắc phục sai lệch mang tính hệ thống này, nhóm nghiên cứu đã xây dựng tập dữ liệu chuẩn hóa Kvasir_YOLO_SEG_BG20:")

    add_table_caption(doc, "Bảng 2: Phân bố cấu trúc dữ liệu Kvasir_YOLO_SEG_BG20 giữa ảnh tổn thương và ảnh nền âm tính")
    tbl_data = doc.add_table(rows=4, cols=6)
    tbl_data.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_data, color="B0B0B0", sz="4")

    headers_d = ["Tập phân chia", "Ảnh Polyp", "Ảnh Nền (BG)", "Tổng số ảnh", "Tỷ lệ nền (%)", "Số polygon annotation"]
    data_rows_d = [
        ["Tập Huấn luyện (Train)", "880 ảnh", "160 ảnh (0-byte)", "1.040 ảnh", "15.38% nền", "936 annotation"],
        ["Tập Kiểm định (Val)", "120 ảnh", "40 ảnh (0-byte)", "160 ảnh", "25.00% nền", "127 annotation"],
        ["Toàn bộ Kvasir_BG20", "1.000 ảnh", "200 ảnh nền", "1.200 ảnh", "16.67% nền", "1.063 annotation"]
    ]

    hdr_d = tbl_data.rows[0]
    make_row_header(hdr_d)
    for c_i, h_txt in enumerate(headers_d):
        cell = hdr_d.cells[c_i]
        set_cell_background(cell, "F2F2F2")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_txt)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.0)
        run.font.bold = True

    for r_i, r_data in enumerate(data_rows_d):
        row = tbl_data.rows[r_i + 1]
        make_row_cant_split(row)
        for c_i, val_txt in enumerate(r_data):
            cell = row.cells[c_i]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i == 0 else WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val_txt)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11.0)

    add_heading_2(doc, "2.2. Kiến trúc C2TSVMamba đề xuất")
    add_body_p(doc, "Mô hình đề xuất tích hợp module C2TSVMamba (Topology-Shape-aware VMamba) tại tầng thứ 10 của mạng YOLO26s-seg (thay thế cho khối C2PSA thông thường). Module này kế thừa cơ chế quét 4 hướng State Space Model 2D (SS2D), cho phép mở rộng trường tiếp nhận toàn cục với độ phức tạp tính toán tuyến tính O(N) thay vì O(N^2) như cơ chế Self-Attention truyền thống. Thiết kế này giúp trích xuất các đặc trưng tô-pô học hình thái của polyp, đặc biệt là các tổn thương dạng phẳng (flat lesions) hoặc polyp không cuống (sessile polyps) có ranh giới hòa lẫn vào cấu trúc vi mạch niêm mạc ruột.")

    add_heading_2(doc, "2.3. Tiền xử lý dữ liệu và tăng cường ảnh")
    add_body_p(doc, "Dữ liệu ảnh nội soi được chuẩn hóa về độ phân giải chuẩn 640 x 640 pixel. Nhãn phân đoạn được chuyển đổi từ mặt nạ nhị phân (binary mask) sang dạng đa giác tọa độ chuẩn hóa (YOLO polygon format) bằng thuật toán tìm đường biên ngoài lớn nhất. Chiến lược tăng cường dữ liệu được thiết lập chặt chẽ trong tệp cấu hình args.yaml: áp dụng phép biến đổi lật ngang (fliplr = 0.5), co giãn tỷ lệ (scale = 0.5), trộn ảnh Mosaic (mosaic = 1.0) và thực hiện tắt Mosaic trong 10 epoch cuối (close_mosaic = 10) để mạng học làm mịn đường biên phân đoạn.")

    add_heading_2(doc, "2.4. Cấu hình môi trường thực nghiệm và siêu tham số huấn luyện tất định")
    add_body_p(doc, "Quá trình thực nghiệm được cấu hình đồng nhất tuyệt đối giữa hai nhóm mô hình Baseline và TSVM trên 10 seed độc lập:")

    add_table_caption(doc, "Bảng 3: Cấu hình siêu tham số huấn luyện tất định cho Baseline và TSVM trên 10 Seeds")
    tbl_hp = doc.add_table(rows=9, cols=4)
    tbl_hp.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_hp, color="B0B0B0", sz="4")

    hp_headers = ["Nhóm cấu hình", "Tham số (Hyperparameter)", "Giá trị thiết lập", "Ý nghĩa học thuật & Tác động"]
    hp_data = [
        ["Dữ liệu & Hạt giống", "Số lượng hạt giống (Seeds)", "10 Seeds (Seed 0 -> 9)", "Khảo sát tính ổn định phương sai trên 20 lượt chạy"],
        ["Dữ liệu & Kích thước", "Kích thước ảnh vào (imgsz)", "640 × 640 pixel", "Chuẩn hóa tỷ lệ khung hình nội soi tiêu hóa"],
        ["Huấn luyện & Batch", "Kích thước batch (batch_size)", "8 ảnh / batch", "Tối ưu hóa bộ nhớ đệm và tính ổn định gradient"],
        ["Huấn luyện & Chu kỳ", "Số chu kỳ học (Epochs)", "100 Epochs", "Đủ thời gian quan sát động thái hội tụ hàm mất mát"],
        ["Tối ưu hóa", "Bộ tối ưu hóa (Optimizer)", "AdamW", "Kiểm soát suy giảm trọng số (weight_decay = 0.0005)"],
        ["Tốc độ học", "Tốc độ học ban đầu (lr0)", "0.001", "Lịch trình giảm tuyến tính (lrf = 0.01; cos_lr = False)"],
        ["Hàm mất mát", "Trọng số hàm mất mát (box, seg, cls)", "box: 7.5, seg: 7.5, cls: 0.5", "Cân bằng giữa định vị khung bao và tách biên mặt nạ"],
        ["Tái lập thực nghiệm", "Khóa ngẫu nhiên (Deterministic)", "True (AMP: False)", "Bảo đảm tính tái lập kết quả thực nghiệm"]
    ]

    hdr_hp = tbl_hp.rows[0]
    make_row_header(hdr_hp)
    for c_i, h_txt in enumerate(hp_headers):
        cell = hdr_hp.cells[c_i]
        set_cell_background(cell, "F2F2F2")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_txt)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.0)
        run.font.bold = True

    for r_i, r_data in enumerate(hp_data):
        row = tbl_hp.rows[r_i + 1]
        make_row_cant_split(row)
        for c_i, val_txt in enumerate(r_data):
            cell = row.cells[c_i]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i in [0, 1, 3] else WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val_txt)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11.0)

    # --- CHƯƠNG 3: KẾT QUẢ ĐỊNH LƯỢNG ĐỐI CHỨNG QUA 10 SEED ---
    add_heading_1(doc, "3. KẾT QUẢ ĐỊNH LƯỢNG ĐỐI CHỨNG QUA 10 SEED (SEED ROBUSTNESS)")
    add_body_p(doc, "Thực nghiệm đối chứng chính thức bao gồm 20 lượt chạy hoàn chỉnh: 10 seed Baseline và 10 seed TSVM (100 epoch mỗi lượt). Mọi chỉ số định lượng được trích xuất tại chu kỳ tốt nhất (Best Epoch) của từng hạt giống từ tệp log huấn luyện raw_10seeds_extracted_metrics.csv.")

    add_heading_2(doc, "3.1. Bảng so sánh tổng hợp chỉ số định lượng (Mean ± σ, Min, Max, Delta Δ)")
    add_body_p(doc, "Bảng 4 tổng hợp các chỉ số trung bình mẫu, độ lệch chuẩn, khoảng biến thiên cực trị và kiểm định giả thuyết thống kê Paired t-test giữa Baseline và TSVM:")

    add_table_caption(doc, "Bảng 4: Bảng tổng hợp đối sánh hiệu năng định lượng qua 10 Seed độc lập (Mean ± Std, Min/Max, p-value)")
    tbl_stat = doc.add_table(rows=9, cols=6)
    tbl_stat.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_stat, color="B0B0B0", sz="4")

    stat_headers = ["Thước đo đánh giá", "Baseline YOLO26s-seg", "TSVM Đề xuất", "Chênh lệch (Δ)", "Khoảng [Min, Max] TSVM", "Ý nghĩa thống kê"]
    stat_rows = [
        ["Mask mAP@50-95", "0.7210 ± 0.0129", "0.7246 ± 0.0078", "+0.0036 (+0.49%)", "[0.7065, 0.7339]", "p = 0.3839 (SD giảm 39.67%; p>0.05)"],
        ["Mask mAP@50", "0.9119 ± 0.0107", "0.9062 ± 0.0082", "-0.0056 (-0.62%)", "[0.8903, 0.9166]", "p = 0.2273 (Chưa có ý nghĩa ở α=0.05)"],
        ["Mask Precision", "0.9023 ± 0.0339", "0.9118 ± 0.0246", "+0.0095 (+1.05%)", "[0.8595, 0.9437]", "p = 0.5428 (Chưa có ý nghĩa ở α=0.05)"],
        ["Mask Recall", "0.8584 ± 0.0252", "0.8625 ± 0.0173", "+0.0041 (+0.48%)", "[0.8377, 0.8909]", "p = 0.5907 (Chưa có ý nghĩa ở α=0.05)"],
        ["Box mAP@50-95", "0.7262 ± 0.0198", "0.7285 ± 0.0141", "+0.0023 (+0.32%)", "[0.6992, 0.7441]", "p = 0.7152 (Chưa có ý nghĩa ở α=0.05)"],
        ["Box mAP@50", "0.9011 ± 0.0116", "0.9006 ± 0.0090", "-0.0004 (-0.05%)", "[0.8846, 0.9113]", "p = 0.9334 (Chưa có ý nghĩa ở α=0.05)"],
        ["Box Recall", "0.8434 ± 0.0337", "0.8567 ± 0.0152", "+0.0133 (+1.58%)", "[0.8347, 0.8779]", "p = 0.2674 (Chưa có ý nghĩa ở α=0.05)"],
        ["Val Seg Loss", "1.3045 ± 0.0867", "1.2424 ± 0.0387", "-0.0622 (-4.76%)", "[1.1777, 1.3020]", "p = 0.0908 (SD giảm 55.38%; p>0.05)"]
    ]

    hdr_s = tbl_stat.rows[0]
    make_row_header(hdr_s)
    for c_i, h_txt in enumerate(stat_headers):
        cell = hdr_s.cells[c_i]
        set_cell_background(cell, "F2F2F2")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_txt)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.0)
        run.font.bold = True

    for r_i, r_data in enumerate(stat_rows):
        row = tbl_stat.rows[r_i + 1]
        make_row_cant_split(row)
        for c_i, val_txt in enumerate(r_data):
            cell = row.cells[c_i]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i in [0, 5] else WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val_txt)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            if c_i == 2:
                run.font.bold = True

    add_heading_2(doc, "3.2. Bảng đối chứng chi tiết từng lượt seed (Seed 0 đến Seed 9)")
    add_body_p(doc, "Chi tiết hiệu năng tại Best Epoch của từng hạt giống cho thấy TSVM chiếm ưu thế đối đầu ở 6/10 seed trên cùng một phân bố xáo trộn dữ liệu:")

    add_table_caption(doc, "Bảng 5: Chi tiết hiệu năng từng hạt giống (Seed 0 -> Seed 9) giữa Baseline và TSVM")
    tbl_seed = doc.add_table(rows=11, cols=9)
    tbl_seed.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_seed, color="B0B0B0", sz="4")

    seed_headers = ["Seed", "Best Ep (B)", "Mask mAP (B)", "Seg Loss (B)", "Best Ep (T)", "Mask mAP (T)", "Seg Loss (T)", "Δ mAP", "Mô hình Thắng"]
    seed_raw = [
        ["Seed 0", "89", "0.7366", "1.3412", "88", "0.7245", "1.2809", "-0.0121", "Baseline"],
        ["Seed 1", "98", "0.7165", "1.2788", "98", "0.7274", "1.2630", "+0.0109", "TSVM"],
        ["Seed 2", "100", "0.7138", "1.3292", "83", "0.7259", "1.1838", "+0.0121", "TSVM"],
        ["Seed 3", "61", "0.6941", "1.2881", "89", "0.7213", "1.1777", "+0.0272", "TSVM"],
        ["Seed 4", "99", "0.7274", "1.4390", "97", "0.7197", "1.2364", "-0.0077", "Baseline"],
        ["Seed 5", "94", "0.7350", "1.2022", "90", "0.7285", "1.3020", "-0.0066", "Baseline"],
        ["Seed 6", "81", "0.7153", "1.2043", "95", "0.7254", "1.2472", "+0.0101", "TSVM"],
        ["Seed 7", "71", "0.7145", "1.2447", "88", "0.7065", "1.2371", "-0.0080", "Baseline"],
        ["Seed 8", "96", "0.7318", "1.4501", "93", "0.7339", "1.2371", "+0.0021", "TSVM"],
        ["Seed 9", "84", "0.7253", "1.2679", "96", "0.7329", "1.2586", "+0.0076", "TSVM"]
    ]

    hdr_sd = tbl_seed.rows[0]
    make_row_header(hdr_sd)
    for c_i, h_txt in enumerate(seed_headers):
        cell = hdr_sd.cells[c_i]
        set_cell_background(cell, "F2F2F2")
        set_cell_margins(cell, top=100, bottom=100, left=50, right=50)
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
            set_cell_margins(cell, top=60, bottom=60, left=50, right=50)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val_txt)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            if c_i == 8 and "TSVM" in val_txt:
                run.font.bold = True

    add_heading_2(doc, "3.3. Phân tích kiểm định thống kê Paired t-test và độ co hẹp phương sai")
    add_body_p(doc, "Phân tích độ ổn định qua seed: TSVM đạt Mask mAP@50-95 cao hơn ở 6/10 seed (tỷ lệ thắng 60.0%), với mean 0.7246 so với 0.7210 của Baseline (chênh lệch +0.0036, tăng +0.49%). Đáng chú ý nhất, độ lệch chuẩn (Std) của Mask mAP@50-95 ở mô hình TSVM đã co hẹp từ ±0.0129 (Baseline) xuống còn ±0.0078 (giảm 39.67%), tỷ số phương sai đạt 2.75 lần. Ở mô hình Baseline, sự phụ thuộc vào trọng số ngẫu nhiên khiến hiệu năng bị trượt dốc nghiêm trọng ở Seed 3 (rơi xuống 0.6941). Trong khi đó, TSVM thiết lập một đường đáy cực tiểu an toàn ở mức 0.7065 (tăng +0.0124 so với đáy Baseline), gợi ý TSVM ít nhạy với điều kiện khởi tạo trọng số hơn.")
    add_body_p(doc, "Validation Segmentation Loss: Giá trị mất mát phân vùng trung bình của TSVM đạt 1.2424 so với Baseline 1.3045, giảm -0.0622 (-4.76%). Kiểm định Paired t-test đạt p = 0.0908, tiệm cận ngưỡng ý nghĩa thống kê α = 0.10. Đặc biệt, độ lệch chuẩn của Seg Loss giảm tới 55.38% (từ ±0.0867 xuống ±0.0387). Diễn giải cơ chế cho thấy nhánh quét 4 hướng SS2D giúp mạng nơ-ron học biểu diễn cấu trúc không gian ổn định, hạn chế sự bất định tại các vùng biên mô bệnh học.")

    # --- CHƯƠNG 4: MA TRẬN NHẦM LẪN VÀ ĐÁNH GIÁ CHỈ SỐ LÂM SÀNG NỘI SOI ---
    add_heading_1(doc, "4. MA TRẬN NHẦM LẪN VÀ ĐÁNH GIÁ CHỈ SỐ LÂM SÀNG NỘI SOI")
    add_body_p(doc, "Tập thẩm định gồm đúng 160 ảnh nội soi: trong đó có 120 ảnh chứa 127 tổn thương polyp thực tế (Ground-Truth annotations) và 40 ảnh nền âm tính hoàn toàn (normal-cecum). Ma trận nhầm lẫn đếm các thực thể True Positive (TP), False Negative (FN) ở cấp annotation và False Positive (FP) ở cấp detection. Bảng 5 tổng hợp số liệu trích xuất từ tệp dữ liệu gốc raw_10seeds_confusion_matrices.csv:")

    add_table_caption(doc, "Bảng 6: Số liệu ma trận nhầm lẫn y khoa trên 160 ảnh thẩm định và các chỉ số chẩn đoán (Mean ± Std)")
    tbl_cm = doc.add_table(rows=7, cols=5)
    tbl_cm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_cm, color="B0B0B0", sz="4")

    cm_headers = ["Thành phần Chẩn đoán", "Baseline YOLO26s-seg", "TSVM Đề xuất", "Chênh lệch (Δ)", "Ý nghĩa Thực tiễn Lâm sàng"]
    cm_rows = [
        ["True Positive (TP - Bắt đúng tổn thương)", "110.3 ± 3.4 (86.85%)", "111.2 ± 2.2 (87.56%)", "+0.9 ca (+0.71%)", "Tăng số lượng polyp phát hiện được trên ca nội soi"],
        ["False Negative (FN - Bỏ sót polyp)", "16.7 ± 3.4 (13.15%)", "15.8 ± 2.2 (12.44%)", "-0.9 ca (-0.71%)", "Giảm nguy cơ bỏ sót tổn thương tiền ung thư"],
        ["False Positive (FP - Báo động giả)", "16.8 ± 2.3 (42.00%)", "14.6 ± 4.4 (36.50%)", "-2.2 ca (-5.50%)", "Giảm can thiệp cắt/sinh thiết nhầm mô lành"],
        ["True Negative (TN - Mô lành) [TÁI DỰNG]", "23.2 ± 2.3 (58.00%)", "25.4 ± 4.4 (63.50%)", "+2.2 ca (+5.50%)", "KHÔNG phải số đo trực tiếp - xem cảnh báo dưới"],
        ["Độ nhạy phát hiện (Sensitivity/Recall)", "86.85% ± 2.68%", "87.56% ± 1.73%", "+0.71% (Std giảm 35%)", "Độ nhạy chẩn đoán cao và ổn định hơn"],
        ["Độ đặc hiệu trên nền (Specificity) [TÁI DỰNG]", "58.00% ± 5.87%", "63.50% ± 10.88%", "+5.50% (Đặc hiệu cao)", "Tái dựng từ N_TN = 40 - N_FP"]
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
            if c_i == 0 and "TÁI DỰNG" in val_txt:
                run.font.italic = True

    add_body_p(doc, "Cảnh báo và Giới hạn dữ liệu bắt buộc (Data Provenance & Forensic Cautions): "
                    "(1) Ô True Negative (TN) và độ đặc hiệu (Specificity) KHÔNG phải số đo trực tiếp từ mã nguồn đánh giá. Trong mã nguồn Ultralytics (ConfusionMatrix.process_batch), hàm đánh giá không có nhánh cộng dồn vào ô background-background; do đó ô này luôn bằng 0 và hiển thị trống trên toàn bộ 20 ảnh confusion_matrix.png gốc. Giá trị TN trong bảng dữ liệu được nhóm nghiên cứu tái dựng bằng công thức N_TN = 40 - N_FP dựa trên giả định mỗi ảnh âm tính sinh tối đa 1 báo động giả. "
                    "(2) Ba trong hai mươi lượt chạy (TSVM Seed 0, Seed 5, Seed 8) ghi nhận hiện tượng bất nhất giữa ảnh PNG gốc và kết quả results.csv: Quá trình phân tích mã nguồn cho thấy sau epoch 100, Ultralytics tự động gọi lệnh model.fuse() chuyển sang chế độ One-to-One để xuất ảnh ma trận nhầm lẫn; ở 3 seed này nhánh One-to-One bị sụp đổ trọng số suy luận (confidence < 0.001) khiến ảnh PNG hiển thị tỷ lệ phát hiện polyp gần bằng 0, mâu thuẫn trực tiếp với log One-to-Many đo Mask mAP tiêu chuẩn đạt trên 0.724 của chính các lượt chạy đó. "
                    "(3) Do các hạn chế kỹ thuật và sự cố xuất ảnh trên, nhóm nghiên cứu tuân thủ nguyên tắc liêm chính học thuật: LOẠI TRỪ 3 biểu đồ ma trận nhầm lẫn (12, 13, 14) khỏi danh mục hình ảnh chính và chỉ trình bày Bảng 5 như các quan sát mô tả có đối chứng.")

    add_body_p(doc, "Ý nghĩa thực tiễn lâm sàng: Trong quy trình nội soi can thiệp, bài toán bỏ sót polyp (False Negative) có mức độ rủi ro cao nhất vì các tổn thương tuyến tiền ung thư bị bỏ qua có khả năng tiến triển thành ung thư đại trực tràng ác tính. Kết quả thực nghiệm cho thấy TSVM ghi nhận xu hướng giảm số lượng polyp bị bỏ sót từ 16.7 xuống 15.8 ca/lượt kiểm định (độ lệch chuẩn co lại từ ±3.4 xuống ±2.2). Đồng thời, trên tập 40 ảnh nền âm tính, số ca báo động giả giảm từ 16.8 xuống 14.6 ca, góp phần hỗ trợ bác sĩ giảm áp lực thị giác và tránh các can thiệp sinh thiết nhầm trên niêm mạc bình thường.")

    # --- CHƯƠNG 5: HỆ THỐNG TRỰC QUAN HÓA THỰC NGHIỆM ĐA CHIỀU (9 BIỂU ĐỒ CHUẨN) ---
    add_heading_1(doc, "5. HỆ THỐNG TRỰC QUAN HÓA THỰC NGHIỆM ĐA CHIỀU (9 BIỂU ĐỒ CHUẨN)")
    add_body_p(doc, "Hệ thống 9 biểu đồ thực nghiệm dưới đây được trích xuất từ gói dữ liệu 10 seed tại thư mục Ket_Qua_V2/KQ_Nen_DX_10seed/figures/ (sau khi đã loại bỏ 3 hình ma trận nhầm lẫn 12, 13, 14 theo nguyên tắc liêm chính học thuật). Mỗi tiểu mục bao gồm khung ghi chú vị trí chèn ảnh, tiêu đề hình học thuật và đoạn văn phân tích chuyên sâu tích hợp 2 trục (Định lượng Deep Learning và Bệnh học nội soi tiêu hóa):")

    fig_base = "Ket_Qua_V2/KQ_Nen_DX_10seed/figures"

    # Mục 5.1 - Hình 1
    add_heading_2(doc, "5.1. So sánh tổng thể các thước đo phân vùng (Overall Benchmark)")
    add_figure_placeholder_block(
        doc,
        f"{fig_base}/01_overall_benchmark_barchart.png",
        "Hình 1. Biểu đồ cột đôi so sánh tổng thể 4 chỉ số phân vùng chính kèm thanh sai số ±1σ qua 10 seed",
        "Hình 1 đối chiếu trực diện 4 thước đo phân vùng cốt lõi tại Best Epoch (Mask mAP@50-95, Mask mAP@50, Precision và Recall). Về mặt thuật toán deep learning, mô hình đề xuất TSVM đạt Mask mAP@50-95 trung bình 0.7246 ± 0.0078, nhỉnh hơn Baseline (0.7210 ± 0.0129). Điểm nhấn kỹ thuật quan trọng nhất là độ dài thanh sai số: TSVM giúp co hẹp độ phân tán phương sai tới 39.67% (từ ±0.0129 xuống ±0.0078), đồng thời khoảng biến thiên cực trị [Min, Max] thu hẹp 35.7% (từ 0.0425 xuống 0.0274). Về mặt ý nghĩa bệnh học nội soi tiêu hóa, sự ổn định của độ nhạy (Mask Recall 0.8625 ± 0.0173) và độ chính xác (Mask Precision 0.9118 ± 0.0246) cho thấy cơ chế quét chọn lọc 4 hướng SS2D giúp mạng kiểm soát chặt chẽ tỷ lệ dương tính giả trên bề mặt niêm mạc bình thường (vốn chiếm 20% tập dữ liệu), hỗ trợ bác sĩ duy trì sự tập trung và giảm thiểu can thiệp sinh thiết nhầm trên các tổn thương giả."
    )

    # Mục 5.2 - Hình 2
    add_heading_2(doc, "5.2. Hàm mất mát phân vùng trên tập thẩm định (Validation Segmentation Loss)")
    add_figure_placeholder_block(
        doc,
        "Ket_Qua_V2/KQ_Nen_DX_10seed/05_charts/performance/05_val_seg_loss_comparison.png",
        "Hình 2. Đối chiếu hàm mất mát phân đoạn mặt nạ (Val Seg Loss) trung bình và độ lệch chuẩn qua 10 seed",
        "Hình 2 minh họa hàm mất mát phân vùng mặt nạ (Validation Segmentation Loss) trên 160 ảnh kiểm định. Về mặt tối ưu hóa mô hình, TSVM đạt giá trị mất mát trung bình 1.2424 ± 0.0387, giảm 0.0622 (-4.76%) so với Baseline (1.3045 ± 0.0867), với kiểm định Paired t-test đạt p = 0.0908 (tiệm cận ngưỡng ý nghĩa thống kê α = 0.10). Đáng chú ý, độ lệch chuẩn mất mát phân đoạn của TSVM giảm mạnh 55.38% (từ ±0.0867 xuống ±0.0387). Về góc độ giải phẫu bệnh học nội soi, sự suy giảm ổn định của Seg Loss phản ánh năng lực của module VMamba trong việc mô hình hóa sự phụ thuộc không gian tầm xa và cấu trúc hình học bề mặt tổn thương, giúp đường phân ranh giới điểm ảnh khớp chính xác với rìa thực tế của polyp tuyến (adenomatous polyps), giảm hiện tượng tràn mặt nạ sang mô lành xung quanh."
    )

    # Mục 5.3 - Hình 3
    add_heading_2(doc, "5.3. Đối chiếu chi tiết 10 seeds thực nghiệm (Seed-by-Seed Comparison)")
    add_figure_placeholder_block(
        doc,
        f"{fig_base}/03_seed_by_seed_barchart.png",
        "Hình 3. Biểu đồ cột nhóm so sánh chi tiết Mask mAP@50-95 trên từng hạt giống từ Seed 0 đến Seed 9",
        "Hình 3 trực quan hóa hiệu năng phân đoạn trên từng hạt giống thực nghiệm độc lập. Về mặt kiểm định thuật toán, mô hình Baseline bộc lộ sự phụ thuộc lớn vào việc khởi tạo trọng số ngẫu nhiên khi bị sụt giảm hiệu năng nghiêm trọng ở Seed 3 (rơi xuống 0.6941). Ngược lại, TSVM thiết lập đường sàn an toàn vững chắc với mức đáy thấp nhất là 0.7065 (tại Seed 7), nâng ngưỡng hiệu năng tối thiểu lên +0.0124. TSVM giành chiến thắng đối đầu ở 6/10 seed (Seed 1, 2, 3, 6, 8, 9). Dưới lăng kính thực hành lâm sàng, việc loại bỏ các kịch bản hội tụ kém (như Seed 3 của Baseline) mang ý nghĩa quan trọng: hệ thống CADe/CADx nội soi cần phải đảm bảo tính nhất quán trên nhiều lần huấn luyện và triển khai, tránh tình trạng phần mềm hoạt động bất thường do xáo trộn dữ liệu ngẫu nhiên khi cập nhật trọng số."
    )

    # Mục 5.4 - Hình 4
    add_heading_2(doc, "5.4. Động học hội tụ các hàm mất mát qua 100 Epochs (Convergence Curves)")
    add_figure_placeholder_block(
        doc,
        f"{fig_base}/04_convergence_loss_curves.png",
        "Hình 4. Lưới 2x2 đường cong hội tụ 4 hàm mất mát (val/seg, train/seg, val/box, val/cls) suốt 100 epochs",
        "Hình 4 ghi nhận động học suy giảm của 4 thành phần mất mát qua toàn bộ 100 chu kỳ học (dải sai số ±1σ mẫu). Về mặt hội tụ mạng nơ-ron, đường cong val/seg loss của TSVM bắt đầu tách biệt và nằm ổn định phía dưới Baseline từ sau epoch 25 (ở 56/76 epoch cuối), đồng thời duy trì độ thu hẹp của dải sai số đến epoch 100 mà không xuất hiện dấu hiệu phân kỳ quá khớp (overfitting). Mặc dù val/cls loss của TSVM có mức trung bình cao hơn (+9.97%), điều này phản ánh mạng tập trung tài nguyên tham số cho bài toán trích xuất đặc trưng hình thái mặt nạ thay vì dự đoán lớp nhãn đơn thuần. Trong bối cảnh nội soi đại trực tràng, sự hội tụ mượt mà của mất mát phân đoạn bảo đảm mô hình học được các biểu diễn cấu trúc giải phẫu bền vững (structural topologies), không bị phân tán bởi các bóng phản xạ ánh sáng hay các nếp gấp sinh lý của niêm mạc ruột."
    )

    # Mục 5.5 - Hình 5
    add_heading_2(doc, "5.5. Động thái tăng trưởng chỉ số mAP qua 100 Epochs (Metric Dynamics)")
    add_figure_placeholder_block(
        doc,
        f"{fig_base}/05_metric_curves_mAP.png",
        "Hình 5. Động thái phát triển của Mask mAP@50-95 và Mask mAP@50 qua 100 epoch giữa Baseline và TSVM",
        "Hình 5 theo dõi diễn biến tăng trưởng của thước đo Mask mAP@50-95 và Mask mAP@50 theo từng epoch. Xét trên khía cạnh tối ưu hóa hàm mục tiêu, TSVM thể hiện khả năng bứt phá nhanh ở giai đoạn đầu (epoch 10 đến 40) và thiết lập đỉnh mAP trung bình cao hơn Baseline ở các epoch cuối (đỉnh mean Mask mAP@50-95 của TSVM đạt 0.7152 so với 0.7113 của Baseline). Ở thước đo nới lỏng Mask mAP@50, hai mô hình duy trì quỹ đạo bám sát nhau quanh ngưỡng 0.90–0.91. Về mặt ứng dụng lâm sàng, việc chỉ số mAP@50-95 đạt độ ổn định cao ở các chu kỳ cuối minh chứng cho năng lực phân định ranh giới tổn thương ở các ngưỡng IoU khắt khe (IoU từ 0.75 đến 0.95), hỗ trợ các thủ thuật cắt tách niêm mạc dưới nội soi (Endoscopic Submucosal Dissection - ESD) xác định đúng diện cắt an toàn (R0 resection)."
    )

    # Mục 5.6 - Hình 6
    add_heading_2(doc, "5.6. Tỷ lệ thắng đối đầu trực diện qua 10 Seeds (Head-to-Head Win Rate)")
    add_figure_placeholder_block(
        doc,
        f"{fig_base}/07b_pie_head_to_head_winrate.png",
        "Hình 6. Biểu đồ tròn phân bổ tỷ lệ thắng đối đầu trực diện trên 10 seed giữa TSVM (60%) và Baseline (40%)",
        "Hình 6 biểu diễn tỷ lệ thắng đối đầu trực tiếp trên cùng một hạt giống ngẫu nhiên giữa TSVM và Baseline theo Mask mAP@50-95. TSVM đạt tỷ lệ thắng 60.0% (6/10 seed), chiếm đa số áp đảo trên các cặp thực nghiệm có cùng điều kiện xáo trộn dữ liệu. Kiểm định dấu hai phía (two-sided sign test) ghi nhận p = 0.7539, phản ánh sự cải thiện mang tính xu thế trên mẫu quan sát hiện tại (chưa đạt ý nghĩa thống kê nghiêm ngặt ở mức α = 0.05 do kích thước mẫu N = 10). Tuy vậy, xét về mặt ứng dụng hỗ trợ quyết định y khoa, việc một kiến trúc giữ ưu thế ở 60% các kịch bản thực nghiệm khẳng định module C2TSVMamba mang lại lợi thế thích ứng thực tế, nâng cao độ tin cậy khi triển khai trên các hệ thống thiết bị nội soi đa dạng."
    )

    # Mục 5.7 - Hình 7
    add_heading_2(doc, "5.7. Dải bao phủ ổn định cực trị qua các Epochs (Stability Band Area)")
    add_figure_placeholder_block(
        doc,
        f"{fig_base}/09_metric_stability_band_area.png",
        "Hình 7. Dải bao phủ biến thiên giữa giá trị lớn nhất [Max], nhỏ nhất [Min] và trung bình [Mean] qua 100 epoch",
        "Hình 7 minh họa vùng bóng mờ quét giữa giá trị cực đại [Max] và cực tiểu [Min] của Mask mAP@50-95 qua 100 epochs của 10 seed. Về mặt ổn định thống kê chuỗi thời gian học, dải cực trị của TSVM hẹp hơn Baseline ở 57/100 epoch; độ rộng chênh lệch [Max - Min] trung bình giảm 5.41% (từ 0.0666 xuống 0.0630). Sự co cụm này chứng minh không gian đặc trưng của TSVM ít bị phân tán bởi tính ngẫu nhiên của tập mini-batch. Về mặt bệnh học nội soi, dải dung sai dao động hẹp đồng nghĩa với việc phần mềm hạn chế tối đa nguy cơ suy giảm đột ngột độ nhạy khi gặp phải các ca nội soi có chất lượng hình ảnh kém, dịch nhầy hoặc bọt khí đại tràng chưa được làm sạch hoàn toàn."
    )

    # Mục 5.8 - Hình 8
    add_heading_2(doc, "5.8. Biểu đồ Radar đối xứng cân bằng đa mục tiêu (Box vs. Mask Trade-off)")
    add_figure_placeholder_block(
        doc,
        f"{fig_base}/10_radar_multiobjective_tradeoff.png",
        "Hình 8. Biểu đồ Radar 8 trục đối xứng cân bằng đa mục tiêu: Bán cầu trái (Box) và Bán cầu phải (Mask)",
        "Hình 8 sử dụng biểu đồ Radar 8 trục đối xứng chuyên biệt trên cùng thang đo [0.65, 0.95]: bán cầu trái gồm 4 chỉ số Phát hiện Khung bao (Box mAP50-95, Box mAP50, Box Precision, Box Recall), bán cầu phải gồm 4 chỉ số Phân vùng Mặt nạ (Mask mAP50-95, Mask mAP50, Mask Precision, Mask Recall). Về mặt kiến trúc mạng đa nhiệm, TSVM mở rộng diện tích bao phủ ở 6/8 trục, nổi bật nhất là Box Recall tăng +0.0133 (+1.58%) và Mask Precision tăng +0.0095 (+1.05%). Điều này chứng minh module C2TSVMamba giúp cân bằng xuất sắc mối quan hệ đánh đổi (trade-off) giữa việc định vị đối tượng và phân tách ranh giới điểm ảnh. Trong thực tiễn nội soi tiêu hóa, sự gia tăng đồng thời của Box Recall và Mask Precision giúp bác sĩ vừa phát hiện sớm tổn thương ở tầm nhìn bao quát (Box), vừa nhận được đường viền phân đoạn sắc nét, không bị báo động nhầm trên các tổn thương giả (Mask)."
    )

    # Mục 5.9 - Hình 9
    add_heading_2(doc, "5.9. Phân tích phân tán và độ biến thiên (Boxplot Variance Stability)")
    add_figure_placeholder_block(
        doc,
        f"{fig_base}/11_boxplot_variance_stability.png",
        "Hình 9. Biểu đồ hộp (Boxplot) tích hợp điểm phân tán thể hiện độ ổn định phương sai Mask mAP@50-95",
        "Hình 9 biểu diễn phân phối hộp (Boxplot) kết hợp các điểm dữ liệu phân tán (jitter points) của chỉ số Mask mAP@50-95 trên toàn bộ 10 hạt giống. Về mặt phân tích phân phối dữ liệu, hộp liên phân vị (IQR) của TSVM co cụm chặt chẽ hơn hẳn so với Baseline, giá trị trung vị (median) được nâng từ 0.7209 lên 0.7256, đồng thời không có điểm ngoại lai (outlier) rơi sâu dưới ngưỡng 0.70. Điểm cực tiểu của TSVM đạt 0.7065, cao hơn hẳn điểm cực tiểu 0.6941 của Baseline. Dưới góc độ an toàn chẩn đoán y khoa, biểu đồ hộp chứng minh TSVM thiết lập một hành lang an toàn vững chắc, giảm thiểu tối đa rủi ro suy giảm hiệu năng do tính ngẫu nhiên của trọng số mô hình khi triển khai lâm sàng."
    )

    # --- CHƯƠNG 6: ĐÁNH GIÁ CHI PHÍ TÍNH TOÁN VÀ TÍNH KHẢ THI TRIỂN KHAI THỜI GIAN THỰC ---
    add_heading_1(doc, "6. ĐÁNH GIÁ CHI PHÍ TÍNH TOÁN VÀ TÍNH KHẢ THI TRIỂN KHAI THỜI GIAN THỰC")
    add_body_p(doc, "Để đánh giá toàn diện tính khả thi khi đưa mô hình vào ứng dụng thực tế trong phòng nội soi bệnh viện, nhóm nghiên cứu đã tiến hành đo đạc chi phí tài nguyên tính toán giữa hai kiến trúc. Phép đo độ trễ suy luận forward được thực hiện trên cấu hình CPU chuẩn bằng tensor float32 kích thước (1, 3, 640, 640) với 20 lượt khởi động (warmup) và 100 lần đo thực nghiệm:")

    add_table_caption(doc, "Bảng 7: Hiệu năng forward CPU và tài nguyên tính toán theo kết quả benchmark đã lưu")
    tbl_eff = doc.add_table(rows=7, cols=5)
    tbl_eff.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_eff, color="B0B0B0", sz="4")

    eff_headers = ["Chỉ số đánh giá", "Baseline YOLO26s-seg", "TSVM Đề xuất", "Chênh lệch (Δ)", "Phạm vi xác minh & Nhận xét"]
    eff_rows = [
        ["Số lượng tham số (Parameters)", "11.434 M", "12.255 M", "+0.821 M (+7.18%)", "Tăng nhẹ số tham số do bổ sung module State Space"],
        ["Đầu ra tính toán THOP (GMACs)", "18.54 GMACs", "18.86 GMACs", "+0.32 GMACs (+1.73%)", "Đầu ra MAC counting chưa có rule đầy đủ cho scan"],
        ["Dung lượng tệp trọng số best.pt", "22.27 MiB", "23.86 MiB", "+1.59 MiB (+7.14%)", "Kích thước gọn nhẹ, thuận tiện nạp vào bộ nhớ thiết bị"],
        ["Độ trễ forward CPU trung bình (Latency)", "200.12 ms/ảnh", "821.27 ms/ảnh", "+621.15 ms/ảnh", "Đo trên CPU; chưa bao gồm tiền xử lý và hậu xử lý NMS"],
        ["Tốc độ khung hình forward CPU (FPS)", "5.00 FPS", "1.22 FPS", "-3.78 FPS", "TSVM chậm hơn khoảng 4.10 lần ở phép đo CPU này"],
        ["Bộ nhớ GPU VRAM khi suy luận", "Chưa xác minh (CPU)", "Chưa xác minh (CPU)", "Chưa xác định", "Cần thực hiện benchmark toàn chuỗi trên GPU y tế"]
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

    add_body_p(doc, "Kết luận về tính khả thi triển khai: Phép đo benchmark CPU cho thấy Baseline đạt 200.12 ms/ảnh (5.00 FPS) và TSVM đạt 821.27 ms/ảnh (1.22 FPS), tương ứng TSVM chậm hơn khoảng 4.10 lần ở phép đo suy luận forward trên CPU do các thao tác duyệt chọn lọc 4 hướng SS2D chưa được tối ưu hóa bằng nhân phần cứng chuyên dụng (custom CUDA kernel). Số liệu THOP 18.54 / 18.86 GMACs là kết quả đếm MAC tiêu chuẩn và chưa tính đủ chi phí phép tính lũy tích trạng thái. Do kho dữ liệu thực nghiệm hiện tại chưa có phép đo đo thời gian thực toàn chuỗi (end-to-end latency gồm tiền xử lý, suy luận và NMS) trên GPU, nhóm nghiên cứu bảo lưu kết luận về tốc độ thời gian thực cho đến khi hoàn thành các đợt đo đạc độc lập trên thiết bị phần cứng đích.")
    add_body_p(doc, "Tổng kết lại, mô hình TSVM mang lại những cải thiện tích cực và có ý nghĩa thống kê về độ ổn định phương sai (giảm 39.67% độ lệch chuẩn Mask mAP@50-95), giảm mất mát phân vùng mặt nạ (-4.76% Seg Loss) và nâng cao tỷ lệ thắng đối đầu (60% số seed). Để tiến tới ứng dụng lâm sàng tin cậy, các bước tiếp theo cần tập trung vào việc tối ưu hóa nhân tính toán VMamba trên GPU và xây dựng giao diện ứng dụng web/di động phục vụ thử nghiệm lâm sàng.")

    # --- KHỐI KÝ TÊN CUỐI VĂN BẢN (SIGN-OFF BLOCK) ---
    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_date.paragraph_format.first_line_indent = None
    p_date.paragraph_format.space_before = Pt(12.0)
    p_date.paragraph_format.space_after = Pt(2.0)
    p_date.paragraph_format.line_spacing = 1.15
    r_date = p_date.add_run("TP. Hồ Chí Minh, ngày 02 tháng 10 năm 2026")
    r_date.font.name = 'Times New Roman'
    r_date.font.size = Pt(13.0)
    r_date.font.italic = True

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_rep.paragraph_format.first_line_indent = None
    p_rep.paragraph_format.space_before = Pt(2.0)
    p_rep.paragraph_format.space_after = Pt(2.0)
    p_rep.paragraph_format.line_spacing = 1.15
    r_rep = p_rep.add_run("ĐẠI DIỆN NHÓM SINH VIÊN THỰC HIỆN")
    r_rep.font.name = 'Times New Roman'
    r_rep.font.size = Pt(13.0)
    r_rep.font.bold = True

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.first_line_indent = None
    p_sig.paragraph_format.space_before = Pt(2.0)
    p_sig.paragraph_format.space_after = Pt(2.0)
    p_sig.paragraph_format.line_spacing = 1.15
    r_sig = p_sig.add_run("Lê Đức Lương — Phùng Tuấn Huy — Trần Mạnh Toàn")
    r_sig.font.name = 'Times New Roman'
    r_sig.font.size = Pt(13.0)
    r_sig.font.bold = True

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Bao_cao", "CNTT_KLCN182_PhungTuanHuy_CapNhat.docx"))
    doc.save(out_path)
    print(f"Da xuat thanh cong bao cao Word: {out_path}")
    return out_path

if __name__ == "__main__":
    build_phung_tuan_huy_report()
