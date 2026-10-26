# CẨM NANG PHONG CÁCH THIẾT KẾ WORD VÀ NGÔN NGỮ HỌC THUẬT BÁO CÁO KHÓA LUẬN
## ĐỀ TÀI: CNTT_KLCN182 — PHÂN ĐOẠN POLYP NỘI SOI ĐẠI TRÀNG VỚI YOLO26-SEG & VMAMBA

---

## 1. NGUYÊN TẮC THIẾT KẾ TÀI LIỆU MICROSOFT WORD (DESIGN SYSTEM)

Quy chuẩn này được đúc kết từ việc phân tích trực tiếp 2 tài liệu mẫu:
1. `CNTT_KLCN182_LeDucLuong.docx` (Báo cáo tiến độ thực nghiệm tuần của sinh viên Lê Đức Lương).
2. `CNTT_KLCN182-Phung The Bao.docx` (Đề cương chi tiết đề tài của Giảng viên hướng dẫn TS. Phùng Thế Bảo).

### 1.1. Khổ giấy và Căn lề trang (Page Setup & Margins)
* **Khổ giấy chuẩn:** A4 (210 x 297 mm, trong Word tương ứng 595.35 x 842.0 pt).
* **Căn lề trang (Page Margins):**
  * **Lề trên (Top):** 1.50 cm (42.5 pt)
  * **Lề dưới (Bottom):** 1.50 cm (42.5 pt)
  * **Lề trái (Left):** 3.00 cm (85.05 pt) — *Quy chuẩn bắt buộc để phục vụ đóng gáy luận văn*.
  * **Lề phải (Right):** 2.00 cm (56.7 pt)
* **Vùng in khả dụng (Printable Width):** xấp xỉ 16.0 cm (453.6 pt). Mọi hình ảnh và bảng biểu tuyệt đối không vượt quá chiều rộng này để tránh tràn viền.

---

### 1.2. Kiểu chữ và Phân cấp Tiêu đề (Typography & Hierarchy)
* **Phông chữ duy nhất:** `Times New Roman` cho toàn bộ tài liệu (từ văn bản, tiêu đề đến bảng biểu và chú thích).
* **Bảng phân cấp cỡ chữ và định dạng:**
  | Thành phần tài liệu | Cỡ chữ (Size) | Định dạng (Style) | Căn lề (Alignment) | Cấp mục lục (Outline Level) |
  | :--- | :---: | :---: | :---: | :---: |
  | **Tiêu đề Báo cáo (Document Title)** | 13.0 pt | In hoa, Đậm (BOLD UPPERCASE) | Căn giữa (CENTER) | Không (Title) |
  | **Tên Đề tài (Topic Title)** | 15.0 pt | In đậm nghiêng (BOLD ITALIC) | Căn giữa (CENTER) | Không |
  | **Mục Cấp 1 (Heading 1)** | 13.0 pt | In hoa, Đậm (1. MỤC TIÊU...) | Căn đều (JUSTIFY) / Trái | outlineLvl = 0 |
  | **Mục Cấp 2 (Heading 2)** | 13.0 pt | In đậm (2.1. Kiến trúc...) | Căn đều (JUSTIFY) / Trái | outlineLvl = 1 |
  | **Mục Cấp 3 (Heading 3)** | 13.0 pt | In đậm nghiêng (5.10.1. ...) | Căn đều (JUSTIFY) / Trái | outlineLvl = 2 |
  | **Văn bản nội dung (Body Text)** | 13.0 pt | Chữ thường (Normal) | Căn đều hai bên (JUSTIFY) | Body Text |
  | **Tiêu đề Bảng (Table Caption)** | 12.0 pt | In nghiêng (Bảng X: ...) | Căn lề đều / Trái (trên bảng) | Không |
  | **Tiêu đề Hình (Figure Caption)** | 12.0 pt | In đậm nhẹ (Hình X. ...) | Căn giữa (CENTER) (dưới hình) | Không |
  | **Nội dung ô Bảng (Table Cells)** | 11.0 - 12.0 pt | Thường, Đậm ở tiêu đề cột | Số: Giữa, Chữ: Trái | Không |

---

### 1.3. Thụt đầu dòng, Giãn cách dòng và Giãn cách đoạn (Indentation & Spacing)
* **Quy chuẩn Thụt đầu dòng (First-line Indent - BẮT BUỘC):**
  * Mọi đoạn văn thân bài (Body Text / Normal) và các đoạn văn nhận xét học thuật bên dưới hình ảnh **BẮT BUỘC PHẢI THỤT ĐẦU DÒNG CHUẨN 1.27 cm (0.5 inch / 36.0 pt)** bằng mã:
    `p.paragraph_format.first_line_indent = Cm(1.27)`
  * Các tiêu đề (`Heading 1`, `Heading 2`, `Heading 3`), tiêu đề Bảng (`Bảng X:...`), tiêu đề Hình (`Hình X....`) và nội dung trong các ô Bảng giữ nguyên `first_line_indent = None` (không thụt đầu dòng).
* **Giãn cách dòng (Line Spacing):** Đặt cố định từ 1.15 đến 1.25 lines (tối ưu tính thoáng đãng và trang nhã).
* **Giãn cách đoạn (Paragraph Spacing):**
  * `Space Before = 3.0 pt`
  * `Space After = 3.0 pt`
  * *Nguyên tắc sống còn:* Không ấn phím Enter nhiều lần để tạo dòng trống. Khoảng đệm giữa các đoạn văn và tiêu đề phải được điều khiển hoàn toàn bằng thuộc tính `Space Before` và `Space After`.

### 1.4. Quy chuẩn Thông tin GVHD và Cấu trúc Báo cáo (BỘ NHỚ QUAN TRỌNG)
* **Học vị Giảng viên Hướng dẫn:** Giảng viên Hướng dẫn chính thức là **TS. Phùng Thế Bảo** (Tiến sĩ, PhD). Tuyệt đối **KHÔNG ĐƯỢC** ghi "ThS.".
* **Tên đề tài chính thức:** **`Nghiên cứu phương pháp tích hợp VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng`**. (Không chèn tên mô hình C2IAVM vào tên đề tài chính).
* **Cấu trúc báo cáo tiến độ:** Báo cáo tuần chuẩn gồm **6 Mục chính** (Mục 1 đến Mục 6). **KHÔNG ĐƯA** Mục 7 checklist kế hoạch tuần vào báo cáo Word.

---

### 1.5. Cơ chế Phân cấp Mục lục Tự động (Automatic TOC & Outline Levels)
Để Microsoft Word tự động tạo cây thư mục tại Navigation Pane (Ctrl + F) và cập nhật số trang tự động qua lệnh F9:
1. Mọi đoạn văn tiêu đề Mục Cấp 1 phải gắn `style='Heading 1'` và XML `<w:outlineLvl w:val="0"/>`.
2. Mọi đoạn văn tiêu đề Mục Cấp 2 phải gắn `style='Heading 2'` và XML `<w:outlineLvl w:val="1"/>`.
3. Mọi đoạn văn tiêu đề Mục Cấp 3 phải gắn `style='Heading 3'` và XML `<w:outlineLvl w:val="2"/>`.
4. Trường mã mục lục tự động (TOC Field): Chèn đoạn mã XML `{ TOC \o "1-3" \h \z \u }`. Khi mở tệp Word, người dùng chỉ cần nhấp chuột phải chọn *Update Field* là toàn bộ cây mục lục và số trang sẽ được liên kết hoàn hảo.

---

### 1.6. Quy chuẩn Thiết kế Bảng biểu (Table Design)
* **Vị trí tiêu đề:** Luôn đặt **phía trên** bảng, ví dụ: *Bảng 1: Bảng so sánh tổng hợp chỉ số định lượng qua 6 seed*.
* **Hàng tiêu đề (Header Row):** Đổ nền xám nhẹ (`#F2F2F2`), in đậm, căn giữa theo cả chiều ngang và chiều dọc. Thiết lập thuộc tính `w:cantSplit` và `w:tblHeader` để tự động lặp lại tiêu đề nếu bảng kéo dài sang trang tiếp theo.
* **Căn chỉnh dữ liệu:**
  * Dữ liệu số (mAP, Recall, Loss, FPS, Tham số): Căn giữa (`CENTER`).
  * Dữ liệu diễn giải (Tên mô hình, Ý nghĩa y khoa, Nhận xét): Căn trái (`LEFT`) hoặc căn đều.
* **Viền kẻ bảng:** Đường viền ngang đơn giản, thanh thoát (`0.5 pt - 0.75 pt`), hạn chế các đường viền dọc quá đậm.

---

### 1.7. Quy chuẩn Chèn Hình ảnh và Nhận xét (Figure & Observation System)
* **Kích thước ảnh:** Chiều rộng chuẩn từ 14.5 cm đến 15.8 cm (độ rộng tối ưu 410 - 450 pt), đảm bảo hình ảnh hiển thị trọn vẹn, không bị tràn ra lề phải hay lệch trang.
* **Căn lề ảnh:** Luôn căn giữa trang (`WD_ALIGN_PARAGRAPH.CENTER`).
* **Tiêu đề hình ảnh:** Đặt ngay **dưới ảnh**, căn giữa (`CENTER`), định dạng Times New Roman 12pt, ví dụ: *Hình 1. Đồ thị đường cong hội tụ 4 hàm mất mát trọng tâm qua 100 epoch*.
* **Đoạn văn nhận xét học thuật (Observation Paragraph):** Đặt ngay dưới tiêu đề hình, căn đều hai bên (`JUSTIFY`), bắt buộc phải phân tích theo **cấu trúc 2 trục đối xứng**:
  1. *Trục Kỹ thuật Học sâu (Deep Learning Technical Axis):* Tốc độ hội tụ, độ phẳng đường cong, biên độ dao động sai số ± 1σ, hiện tượng suy biến gradient, hiện tượng co hẹp phương sai.
  2. *Trục Ý nghĩa Y khoa Lâm sàng (Clinical Impact Axis):* Khả năng bao phủ vùng tổn thương (Recall), kiểm soát âm tính giả (False Negative), khử đốm lóa sáng trên bề mặt niêm mạc đại tràng, đáp ứng tốc độ xử lý thời gian thực (>30 FPS) trong thủ thuật can thiệp nội soi.

---

## 2. CẨM NANG NGÔN NGỮ HỌC THUẬT & MẪU CÂU NHẬN XÉT CHUẨN

### 2.1. Mẫu câu phân tích Đồ thị Đường cong Mất mát (Loss Curves)
> *"Quan sát đồ thị đường cong hội tụ qua 100 epoch, cả hai mô hình đều đạt trạng thái ổn định vững chắc sau epoch 75 mà không xuất hiện dấu hiệu quá khớp (overfitting). Mô hình đề xuất C2IAVM đạt được nghiệm cực tiểu của hàm mất mát phân đoạn mặt nạ (Validation Segmentation Loss) ở mức 1.3987 ± 0.0695, giảm sâu -0.0327 so với Baseline (1.4314 ± 0.0540). Việc đường Seg Loss của C2IAVM nằm tách biệt phía dưới đường Baseline minh chứng cơ chế tương tác hai chiều chéo đã giúp mạng học được không gian biểu diễn viền tổn thương tối ưu hơn, giải quyết triệt để sự xung đột gradient."*

### 2.2. Mẫu câu phân tích Động thái Đánh đổi Precision vs Recall
> *"Trong bài toán chẩn đoán polyp nội soi đại trực tràng có hỗ trợ của máy tính (CADe/CADx), việc bỏ sót tổn thương ung thư giai đoạn sớm (False Negative) mang lại rủi ro nguy hiểm hơn rất nhiều so với việc cảnh báo thừa (False Positive). Mô hình đề xuất C2IAVM chủ động thực hiện một sự đánh đổi lâm sàng mang tính chiến lược: chấp nhận mở rộng nhẹ viền điểm ảnh dự đoán (Precision đạt 88.76% so với 91.98% của Baseline) để kéo vọt Độ nhạy phát hiện (Mask Recall) từ 87.60% lên mức đỉnh cao 88.75% (tăng +1.15%, tương ứng phát hiện thêm nhiều tổn thương nguy hiểm). Đây là sự đánh đổi hoàn toàn phù hợp với thực tiễn y khoa can thiệp."*

### 2.3. Mẫu câu phân tích Tính Ổn định và Giảm Phương sai (Seed Robustness)
> *"Thực nghiệm lặp lại độc lập trên 6 seed ngẫu nhiên (s0 đến s5) với cùng bộ siêu tham số trên nền tảng Kaggle GPU T4 cho thấy sự vượt trội áp đảo của C2IAVM khi giành chiến thắng đối đầu trực diện ở 5/6 seed (tỷ lệ thắng 83.33%). Độ lệch chuẩn của Mask mAP@50-95 co hẹp từ ±0.0153 (Baseline) xuống còn ±0.0073, tương ứng hệ số giảm phương sai F = 4.39 lần theo kiểm định Fisher F-test. Điều này khẳng định cơ chế Attention-VMamba giúp mô hình hoàn toàn thoát khỏi sự lệ thuộc vào tính ngẫu nhiên của trọng số khởi tạo ban đầu, đảm bảo tính tái lập kết quả khoa học cao."*

### 2.4. Mẫu câu phân tích Minh chứng Định tính (Qualitative Inspection)
> *"Kết quả trực quan hóa trên các ca bệnh điển hình cho thấy: Đối với polyp có kích thước trung bình và viền mờ, mô hình Baseline tạo ra mặt nạ răng cưa và bị khuyết góc, trong khi C2IAVM tạo ra đường bao tròn mượt, bám khít ranh giới tế bào niêm mạc. Đặc biệt, ở trường hợp ánh đèn nội soi phản chiếu tạo ra các đốm lóa sáng cục bộ (specular highlights), Baseline bị đánh lừa tạo ra các lỗ thủng trên mặt nạ phân đoạn, trong khi C2IAVM nhờ bản đồ liên tục giải phẫu của VMamba đã duy trì cấu trúc mặt nạ nguyên vẹn, xóa sạch hiện tượng phân mảnh giả tạo."*

### 2.5. Mẫu câu phân tích Độ khả thi Triển khai Thời gian thực (Real-time Latency)
> *"Về mặt chi phí tính toán, khối C2IAVM tích hợp lớp vi phân giải tích SelectiveScanAutograd chỉ làm tăng thêm 0.61M tham số (+5.3%) và 5.1 GFLOPs so với Baseline nguyên bản. Tổng thời gian trễ suy luận toàn chuỗi đầu-cuối (bao gồm tiền xử lý Letterbox, suy luận nơ-ron và hậu xử lý NMS) chỉ tiêu tốn 25.0 ms/ảnh trên GPU NVIDIA Tesla T4, tương đương tốc độ khung hình 40.0 FPS. Tốc độ này vượt xa yêu cầu tần số quét chuẩn của các hệ thống máy nội soi tiêu hóa hiện đại (>= 30 FPS), khẳng định tính khả thi tuyệt đối khi triển khai thực tế tại các phòng mổ và trung tâm nội soi."*
