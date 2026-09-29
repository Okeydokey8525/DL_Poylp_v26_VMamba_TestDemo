# QUY CHUẨN THIẾT KẾ BÁO CÁO MICROSOFT WORD VÀ VĂN PHONG HỌC THUẬT
## TÁC GIẢ & CHỦ SỞ HỮU THIẾT KẾ: LÊ ĐỨC LƯƠNG (ĐỀ TÀI: CNTT_KLCN182)
### TÀI LIỆU DÀNH CHO CÁC HỆ THỐNG AI ĐỂ NẮM BẮT VÀ TUÂN THỦ 100% PHONG CÁCH THIẾT KẾ

> **MỤC ĐÍCH CỦA TÀI LIỆU NÀY:**
> Tài liệu này đóng gói toàn bộ **Hệ Thống Thiết Kế (Design System)**, **Quy Chuẩn Định Dạng (Formatting Specifications)** và **Bộ Quy Tắc Ngôn Ngữ Học Thuật (Academic & Clinical Writing Style)** được trích xuất và học trực tiếp từ tệp chuẩn [`CNTT_KLCN182_LeDucLuong.docx`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/CNTT_KLCN182_LeDucLuong.docx). 
> **Mọi AI khi tham gia hỗ trợ, chỉnh sửa hoặc sinh tài liệu Word/Markdown cho dự án này BẮT BUỘC PHẢI TUÂN THỦ TUYỆT ĐỐI các quy tắc dưới đây.**

---

## 1. TRIẾT LÝ THIẾT KẾ CỐT LÕI (CORE DESIGN PHILOSOPHY)

Phong cách thiết kế của Lê Đức Lương được định hình bởi 4 trụ cột:
1. **Tính Chuẩn Mực Học Thuật & Đóng Gáy Luận Văn:** Định dạng lề trang bất đối xứng (Lề trái 3.5 cm) bắt buộc để khi in ấn và đóng bìa gáy luận văn, nội dung không bao giờ bị che khuất hay lẹm chữ.
2. **Khoảng Thở Thanh Thoát (Typographic Breathing Room):** Không dùng phím `Enter` nhiều lần để tạo dòng trống. Khoảng cách giữa các đoạn văn và bảng biểu được kiểm soát chính xác bằng vi thông số `space_before` và `space_after`.
3. **Tính Đồng Nhất Tuyệt Đối (Zero Inconsistency):** Chỉ sử dụng một phông chữ duy nhất `Times New Roman` cho toàn bộ tài liệu (từ trang bìa, đề mục, nội dung, bảng biểu, đến nhãn đồ thị và chú thích ảnh).
4. **Đối Chiếu Hai Trục Song Song Trong Mọi Nhận Xét (Two-Axis Analysis):** Mọi biểu đồ, đồ thị và bảng số liệu đều phải được diễn giải song song trên 2 góc nhìn: **(1) Trục Kỹ thuật Học sâu (Deep Learning)** và **(2) Trục Ý nghĩa Y khoa Lâm sàng (Clinical Gastrointestinal Endoscopy)**.

---

## 2. QUY CHUẨN THIẾT LẬP TRANG (PAGE SETUP & GEOMETRY)

| Thuộc tính | Thông số chuẩn | Đơn vị quy đổi OpenXML / Word | Ý nghĩa thiết kế |
| :--- | :--- | :--- | :--- |
| **Khổ giấy (Paper Size)** | **A4** (21.00 cm × 29.70 cm) | $11.906'' \times 8.268''$ | Chuẩn in ấn học thuật Việt Nam |
| **Lề Trái (Left Margin)** | **3.50 cm** | 1984 twips / 99.2 pt | **BẮT BUỘC:** Chừa gáy đóng bìa luận văn cử nhân |
| **Lề Phải (Right Margin)** | **2.50 cm** | 1417 twips / 70.9 pt | Cân đối thị giác trang in |
| **Lề Trên (Top Margin)** | **2.50 cm** | 1417 twips / 70.9 pt | Khoảng cách an toàn tới mép giấy |
| **Lề Dưới (Bottom Margin)** | **2.50 cm** | 1417 twips / 70.9 pt | Chừa vị trí đánh số trang |
| **Vùng in khả dụng (Printable Width)** | **15.00 cm** | ~8504 twips / 425 pt | Chiều rộng tối đa cho ảnh và bảng (không vượt quá) |
| **Khoảng cách Header / Footer** | **1.27 cm** (0.5 inch) | 720 twips / 36.0 pt | Vị trí tiêu đề đầu trang và chân trang |

---

## 3. HỆ THỐNG PHÂN CẤP CHỮ VÀ ĐỊNH DẠNG ĐOẠN VĂN (TYPOGRAPHY & PARAGRAPH SYSTEM)

### 3.1. Bảng phân cấp kiểu chữ (Font Hierarchy)
*Phông chữ duy nhất áp dụng cho toàn bộ văn bản: `Times New Roman`.*

| Thành phần | Cỡ chữ (Size) | Kiểu dáng (Weight & Style) | Căn lề (Alignment) | Thụt đầu dòng (First-Line Indent) | Giãn dòng & Giãn đoạn |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Tiêu đề Báo cáo (Document Title)** | **13.0 pt** | **IN HOA, IN ĐẬM** | Căn giữa (`CENTER`) | `None` (0 cm) | Before: 3pt, After: 3pt, Line: 1.25 |
| **Tên Đề tài (Topic Subtitle)** | **15.0 pt** | **In Đậm, In Nghiêng** | Căn giữa (`CENTER`) | `None` (0 cm) | Before: 3pt, After: 3pt, Line: 1.25 |
| **Đề mục Cấp 1 (Heading 1)** | **13.0 pt** | **IN HOA, IN ĐẬM** (`1. MỤC TIÊU...`) | Căn đều / Trái | `None` (0 cm) | Before: 3pt, After: 3pt, Line: 1.25 |
| **Đề mục Cấp 2 (Heading 2)** | **13.0 pt** | **In Đậm** (`2.1. Vai trò...`) | Căn đều / Trái | `None` (0 cm) | Before: 3pt, After: 3pt, Line: 1.25 |
| **Đề mục Cấp 3 (Heading 3)** | **13.0 pt** | **In Đậm Nghiêng** (`5.1. Đồ thị...`) | Căn đều / Trái | `None` (0 cm) | Before: 3pt, After: 3pt, Line: 1.25 |
| **Đoạn văn Thân bài (Body Text)** | **13.0 pt** | Thường (Regular) | Căn đều (`JUSTIFY`) | **1.27 cm (0.5 inch / 720 twips)** | Before: 3pt, After: 3pt, Line: 1.25 |
| **Ý gạch đầu dòng (Bullet points)** | **13.0 pt** | Thường hoặc Đậm từ khóa đầu | Căn đều (`JUSTIFY`) | `None` (thụt lề trái theo bullet) | Before: 3pt, After: 3pt, Line: 1.25 |
| **Tiêu đề Bảng (Table Caption)** | **12.0 pt** | *In Nghiêng* (`Bảng X: ...`) | Căn lề Trái / Đều (trên bảng) | `None` (0 cm) | Before: 3pt, After: 3pt |
| **Tiêu đề Hình (Figure Caption)** | **12.0 pt** | **In Đậm nhẹ** hoặc Thường (`Hình X. ...`) | Căn giữa (`CENTER`) (dưới ảnh) | `None` (0 cm) | Before: 3pt, After: 3pt |
| **Đoạn nhận xét dưới ảnh (Observation)** | **13.0 pt** | Thường (Regular) | Căn đều (`JUSTIFY`) | **1.27 cm (0.5 inch / 720 twips)** | Before: 3pt, After: 3pt, Line: 1.25 |
| **Ký tên cuối văn bản (Sign-off Block)** | **13.0 pt** | In Nghiêng (ngày) / In Đậm (tên) | Căn phải (`RIGHT`) | `None` (0 cm) | Before: 3pt, After: 3pt |

### 3.2. Quy tắc Thụt đầu dòng (First-Line Indent Rule)
- **BẮT BUỘC THỤT 1.27 CM (720 twips / 0.5 inch):** Áp dụng cho mọi đoạn văn văn bản thông thường (Body Text), đoạn mở đầu mục con, và đoạn nhận xét học thuật bên dưới các biểu đồ hình ảnh.
- **TUYỆT ĐỐI KHÔNG THỤT ĐẦU DÒNG (0 cm):** 
  + Tiêu đề báo cáo và tên đề tài.
  + Mọi tiêu đề mục (Heading 1, 2, 3).
  + Tiêu đề bảng (`Bảng X: ...`) và Tiêu đề hình (`Hình X. ...`).
  + Các ô trong bảng biểu.
  + Khối ký tên cuối trang.

---

## 4. QUY CHUẨN THIẾT KẾ BẢNG BIỂU (TABLE DESIGN SYSTEM)

Các bảng trong tài liệu của Lê Đức Lương được thiết kế theo chuẩn thanh lịch, hiện đại, không lạm dụng viền đậm:

### 4.1. Bảng Thông Tin Metadata Mở Đầu (Header Info Block)
- **Vị trí:** Ngay dưới Tiêu đề Báo cáo và Tên Đề tài.
- **Cấu trúc:** 2 cột (Cột 1: Thuộc tính ~5.37 cm; Cột 2: Nội dung chi tiết ~9.63 cm).
- **Màu nền Cột 1:** Đổ nền xám nhạt `#F7F7F7`, chữ in đậm `Times New Roman 13pt`.
- **Màu nền Cột 2:** Không đổ nền (Trắng), chữ thường `Times New Roman 13pt`.
- **Đường viền (Borders):** Viền đơn màu xám trung tính `#999999` hoặc `#CCCCCC`, độ dày `0.75 pt` (`sz="6"`).

### 4.2. Bảng Dữ Liệu Thực Nghiệm (Experimental Data Tables)
- **Vị trí Tiêu đề:** Luôn đặt **phía trên** bảng, in nghiêng hoặc in đậm nghiêng: `Bảng X: [Mô tả chi tiết nội dung bảng]`.
- **Hàng tiêu đề cột (Header Row):**
  + Đổ nền xám nhạt (`#F2F2F2` hoặc `#F7F7F7`).
  + Chữ in đậm (`BOLD`), căn giữa cả theo chiều ngang (`CENTER`) và chiều dọc (`CENTER`).
  + Thuộc tính XML bắt buộc: `<w:tblHeader/>` (tự động lặp lại hàng tiêu đề nếu bảng tràn trang) và `<w:cantSplit/>` (không bị vỡ hàng khi chuyển trang).
- **Căn lề nội dung ô:**
  + Dữ liệu số (mAP, Precision, Recall, Loss, FPS, Giá trị $p$): **Căn giữa (`CENTER`)**.
  + Các giá trị đo lường có sai số: Định dạng đồng nhất dạng `Mean ± Std` (ví dụ: $0.7246 \pm 0.0078$).
  + Tên mô hình, mô tả văn bản, tham số: **Căn trái (`LEFT`)**.
- **Đường viền bảng:** Viền ngang thanh lịch màu xám `#B0B0B0` độ dày `0.5 pt` (`sz="4"`), viền dọc tối giản hoặc ẩn để tạo không gian thoáng đãng.

---

## 5. QUY CHUẨN HÌNH ẢNH VÀ NHẬN XÉT HỌC THUẬT (FIGURES & OBSERVATIONS)

Đây là điểm nhấn quan trọng nhất trong phong cách của Lê Đức Lương. Mỗi biểu đồ khoa học không bao giờ đứng đơn lẻ mà luôn đi kèm bộ ba: **(1) Khung ảnh chuẩn kích thước $\to$ (2) Tiêu đề định danh chuẩn $\to$ (3) Đoạn văn nhận xét học thuật chuyên sâu**.

```
+-------------------------------------------------------------+
|                                                             |
|                      [ HÌNH ẢNH ]                           |
|       (Căn giữa trang, Chiều rộng 14.50 cm - 15.80 cm)      |
|                                                             |
+-------------------------------------------------------------+
               Hình X. Tiêu đề mô tả khoa học của hình ảnh
                      (Times New Roman 12pt, Căn giữa)

   [Thụt đầu dòng 1.27cm] Đoạn văn phân tích học thuật chuyên sâu 
được cấu trúc theo 2 trục đối xứng: Trục Kỹ thuật Học sâu và Trục 
Ý nghĩa Y khoa Can thiệp Lâm sàng...
```

### 5.1. Quy chuẩn Khung hình (Image Dimensions)
- **Căn lề:** Luôn căn giữa trang (`WD_ALIGN_PARAGRAPH.CENTER`).
- **Chiều rộng tối ưu:** Từ **14.50 cm đến 15.80 cm** (không vượt quá 15.90 cm để bảo đảm nằm trọn trong vùng in khả dụng 15.0 cm - 16.0 cm, không bị tràn lề phải).
- **Tỷ lệ khung hình:** Giữ nguyên tỷ lệ gốc, không co kéo méo ảnh.

### 5.2. Công thức Soạn thảo Nhận xét Học thuật (Academic Commentary Formula)
Mỗi đoạn nhận xét bên dưới biểu đồ bắt buộc phải tuân theo công thức 2 trục:

1. **Trục 1: Cơ chế Kỹ thuật Học sâu (Deep Learning Technical Axis):**
   - Chỉ rõ xu hướng biến thiên: độ phẳng đường cong, tốc độ hội tụ qua 100 epochs, điểm uốn của hàm mất mát.
   - Định lượng chính xác: Trích dẫn con số cụ thể kèm sai số ($\text{Mean} \pm \text{Std}$), tỷ lệ phần trăm cải thiện ($\Delta$).
   - Giải thích căn nguyên kiến trúc: Liên hệ trực tiếp tới cơ chế toán học của mô hình (ví dụ: cơ chế quét chọn lọc 4 hướng SS2D trong VMamba, khả năng nén ngữ cảnh dài hạn tuyến tính $O(N)$, cơ chế dung hòa đặc trưng đa vĩ mô của Bi-FPN).
   - Đánh giá độ co hẹp phương sai: Phân tích độ lệch chuẩn co cụm, loại bỏ sự phụ thuộc vào trọng số khởi tạo ngẫu nhiên.

2. **Trục 2: Ý nghĩa Thực hành Y khoa Lâm sàng (Clinical Impact Axis):**
   - Đánh giá khả năng bảo vệ người bệnh: Nâng cao độ nhạy (Recall), triệt tiêu nguy cơ bỏ sót tổn thương ung thư tiền phát (False Negative).
   - Kiểm soát áp lực bác sĩ can thiệp: Giảm thiểu báo động giả (False Positive) trên bề mặt niêm mạc bình thường (đặc biệt khi có 20% ảnh nền âm tính).
   - Chất lượng phân vùng giải phẫu: Tách biệt ranh giới tổn thương phẳng (flat/sessile), triệt tiêu nhiễu quang học (lóa sáng đèn nội soi, nếp gấp ruột).
   - Khả năng xử lý thời gian thực: Tốc độ khung hình thực tế (>30 FPS) tương thích với các dòng máy nội soi y khoa tiêu chuẩn (Olympus, Fujifilm).

---

## 6. MÃ PYTHON-DOCX THAM CHIẾU CHUẨN (RECIPE ĐÓNG GÓI CHO AI)

Khi bất kỳ AI nào cần xuất báo cáo sang tệp Word `.docx` theo đúng phong cách của Lê Đức Lương, hãy áp dụng trực tiếp mẫu code chuẩn hóa dưới đây:

```python
import docx
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def apply_le_duc_luong_page_setup(doc):
    """Thiết lập lề trang chuẩn đóng gáy luận văn của Lê Đức Lương"""
    for sec in doc.sections:
        sec.page_width = Cm(21.0)   # Khổ A4
        sec.page_height = Cm(29.7)
        sec.top_margin = Cm(2.5)    # Lề trên 2.5 cm
        sec.bottom_margin = Cm(2.5) # Lề dưới 2.5 cm
        sec.left_margin = Cm(3.5)   # Lề trái 3.5 cm (BẮT BUỘC: Đóng gáy luận văn)
        sec.right_margin = Cm(2.5)  # Lề phải 2.5 cm
        sec.header_distance = Cm(1.27)
        sec.footer_distance = Cm(1.27)

def add_le_duc_luong_heading_1(doc, text):
    """Mục cấp 1: 13pt BOLD IN HOA, căn đều/trái, giãn dòng chuẩn"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.space_before = Pt(6.0)
    p.paragraph_format.space_after = Pt(4.0)
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(text.upper())
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.0)
    run.font.bold = True
    return p

def add_le_duc_luong_body_paragraph(doc, text):
    """Đoạn văn thân bài: 13pt thường, căn đều, BẮT BUỘC thụt đầu dòng 1.27cm"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.27)  # BẮT BUỘC: 0.5 inch
    p.paragraph_format.space_before = Pt(3.0)
    p.paragraph_format.space_after = Pt(3.0)
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.0)
    return p

def add_le_duc_luong_figure_block(doc, image_path, caption_text, observation_text, width_cm=15.0):
    """Bộ ba Hình ảnh - Tiêu đề - Nhận xét học thuật chuẩn mực"""
    # 1. Khung hình căn giữa
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.first_line_indent = None
    p_img.paragraph_format.space_before = Pt(6.0)
    p_img.paragraph_format.space_after = Pt(2.0)
    p_img.add_run().add_picture(image_path, width=Cm(width_cm))

    # 2. Tiêu đề hình căn giữa (12pt)
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.first_line_indent = None
    p_cap.paragraph_format.space_before = Pt(2.0)
    p_cap.paragraph_format.space_after = Pt(4.0)
    run_cap = p_cap.add_run(caption_text)
    run_cap.font.name = 'Times New Roman'
    run_cap.font.size = Pt(12.0)
    run_cap.font.bold = True

    # 3. Đoạn nhận xét học thuật 2 trục (13pt, thụt đầu dòng 1.27cm)
    p_obs = add_le_duc_luong_body_paragraph(doc, observation_text)
    return p_img, p_cap, p_obs
```

---

## 7. BẢNG CHECKLIST NGHIỆM THU ĐỊNH DẠNG TRƯỚC KHI BÀN GIAO CHO LÊ ĐỨC LƯƠNG

Mọi AI sau khi tạo hoặc sửa tài liệu Word/Markdown phải tự kiểm tra theo danh mục này:

- [ ] **Lề trang:** Đã đặt đúng Lề Trái = 3.50 cm; Trên = Dưới = Phải = 2.50 cm chưa?
- [ ] **Phông chữ:** Đã kiểm tra 100% văn bản dùng `Times New Roman` chưa? (Không bị lẫn Arial hay Calibri).
- [ ] **Thụt đầu dòng:** Tất cả đoạn văn thân bài và đoạn nhận xét dưới ảnh đã thụt đầu dòng đúng 1.27 cm chưa?
- [ ] **Không thụt đầu dòng:** Các đề mục, tiêu đề bảng, tiêu đề hình và ô bảng có bị thụt nhầm không? (Phải là 0 cm).
- [ ] **Khoảng trống:** Đã loại bỏ các phím Enter thừa (đoạn trống vô nghĩa) chưa?
- [ ] **Độ rộng hình ảnh:** Có ảnh nào vượt quá 15.80 cm gây tràn lề không? (Tất cả phải $\le 15.80$ cm).
- [ ] **Nhận xét học thuật:** Các biểu đồ đã có đủ cả phân tích kỹ thuật học sâu lẫn ý nghĩa y khoa nội soi chưa?
- [ ] **Số liệu thực nghiệm:** Giữ nguyên 100% số liệu gốc từ thư mục kết quả, tuyệt đối không bịa số hay làm tròn sai lệch.

---
*Tài liệu này được biên soạn độc quyền cho đề tài CNTT_KLCN182 và được lưu trữ vĩnh viễn tại thư mục `archive/doc/` để mọi hệ thống AI tái lập chính xác phong cách làm việc của tác giả Lê Đức Lương.*
