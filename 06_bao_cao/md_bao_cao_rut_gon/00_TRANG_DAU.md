# CÁC TRANG ĐẦU

> **Ghi chú soạn thảo (xóa khi ghép Word):**
> - Theo Biểu mẫu V3, thứ tự các trang đầu là: bìa chính, bìa phụ, Lời cảm ơn, Mục lục, Danh mục các ký hiệu và chữ viết tắt, Danh mục hình, Danh mục bảng. Sau đó đến Mở đầu.
> - **Bìa chính, bìa phụ:** điền khi ghép Word, theo nội dung ở mục "Thông tin bìa" bên dưới.
> - **Mục lục, Danh mục hình, Danh mục bảng:** Word tạo tự động khi ghép, không viết tay.
> - **Lời cảm ơn:** đây là **bản nháp**, nhóm sửa lại theo ý mình. Lời cảm ơn nên do chính nhóm viết.
> - Danh mục chữ viết tắt lấy từ các chữ thực sự xuất hiện trong Mở đầu, Chương 1–6 và Kết luận (quét ngày 29/10/2026), sắp xếp theo thứ tự chữ cái.

## Thông tin bìa (dùng khi ghép Word)

| Mục trên bìa | Nội dung |
|---|---|
| Cơ quan | BỘ CÔNG THƯƠNG – TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP. HCM – KHOA CÔNG NGHỆ THÔNG TIN |
| Loại đề tài | KHÓA LUẬN TỐT NGHIỆP |
| Tên đề tài | NGHIÊN CỨU PHƯƠNG PHÁP TÍCH HỢP VMAMBA VÀO MÔ HÌNH YOLO26-SEG TRONG PHÂN ĐOẠN POLYP TỪ ẢNH NỘI SOI ĐẠI TRỰC TRÀNG |
| Ngành | Công nghệ thông tin |
| Mã đề tài | CNTT_KLCN182 |
| Giảng viên hướng dẫn (bìa phụ) | Phùng Thế Bảo **[ĐIỀN: học hàm, học vị nếu có]** |
| Sinh viên thực hiện | 1. 2001230490 – Lê Đức Lương – 14DHTH09<br>2. 2001230312 – Phùng Tuấn Huy – 14DHTH13<br>3. 2001230830 – Trần Mạnh Toàn – 14DHTH09 |
| Nơi, thời gian | TP. HỒ CHÍ MINH, tháng 11 năm 2026 |

---

# LỜI CẢM ƠN

> **Bản nháp. Nhóm đọc lại, sửa cho đúng giọng của mình và thêm người cần cảm ơn.**

Nhóm thực hiện xin gửi lời cảm ơn chân thành đến thầy **Phùng Thế Bảo**, giảng viên hướng dẫn. Trong suốt mười hai tuần thực hiện đề tài, thầy đã định hướng nội dung nghiên cứu, góp ý cho từng giai đoạn và nhắc nhóm luôn kiểm chứng kết quả một cách cẩn thận.

Nhóm xin cảm ơn quý thầy cô Khoa Công nghệ Thông tin, Trường Đại học Công Thương TP. Hồ Chí Minh. Những kiến thức thầy cô truyền đạt trong những năm học là nền tảng để nhóm thực hiện khóa luận này.

Nhóm cũng cảm ơn các nhóm tác giả đã công bố miễn phí các bộ dữ liệu Kvasir-SEG, Kvasir, CVC-ClinicDB, CVC-ColonDB, ETIS-Larib và PolypGen cùng các thư viện mã nguồn mở được sử dụng trong đề tài. Nhờ đó nhóm có thể thực nghiệm và đối chiếu kết quả. Nhóm cảm ơn nền tảng Kaggle đã cung cấp tài nguyên GPU cho quá trình huấn luyện.

Cuối cùng, nhóm xin cảm ơn gia đình và bạn bè đã luôn động viên, hỗ trợ trong suốt thời gian học tập và thực hiện đề tài.

Dù đã cố gắng, khóa luận khó tránh khỏi thiếu sót. Nhóm mong nhận được góp ý của quý thầy cô để hoàn thiện hơn.

TP. Hồ Chí Minh, tháng 11 năm 2026
Nhóm sinh viên thực hiện

---

# DANH MỤC CÁC KÝ HIỆU VÀ CHỮ VIẾT TẮT

## Chữ viết tắt

| Viết tắt | Tiếng Anh | Tiếng Việt |
|---|---|---|
| AP | Average Precision | Độ chính xác trung bình |
| API | Application Programming Interface | Giao diện lập trình ứng dụng |
| BG20 | Background 20% | Bộ dữ liệu của đề tài: Kvasir-SEG cộng số ảnh nền bằng 20% số ảnh polyp |
| BN | Batch Normalization | Chuẩn hóa theo lô |
| C2PSA | CSP block with Partial Self-Attention | Khối tự chú ý từng phần của YOLO26 (tầng 10 của mô hình gốc) |
| C2TSVMamba | CSP block with Topology–Shape-aware VMamba | Khối đề xuất thay C2PSA ở tầng 10 |
| CI | Confidence Interval | Khoảng tin cậy |
| CNN | Convolutional Neural Network | Mạng nơ-ron tích chập |
| COCO | Common Objects in Context | Bộ dữ liệu ảnh dùng để tiền huấn luyện YOLO |
| CPU | Central Processing Unit | Bộ xử lý trung tâm |
| CSP | Cross Stage Partial | Cấu trúc tách–ghép kênh qua các tầng |
| CUDA | Compute Unified Device Architecture | Nền tảng tính toán song song trên GPU của NVIDIA |
| CVC | Computer Vision Center | Trung tâm Thị giác máy tính (Barcelona), nơi công bố các bộ CVC-ClinicDB, CVC-ColonDB |
| DFL | Distribution Focal Loss | Hàm mất mát tiêu điểm theo phân phối |
| EMA | Exponential Moving Average | Trung bình trượt hàm mũ |
| FFN | Feed-Forward Network | Mạng truyền thẳng |
| FLOPs | Floating-Point Operations | Số phép tính dấu phẩy động |
| FN | False Negative | Âm tính giả (polyp bị bỏ sót) |
| FP | False Positive | Dương tính giả (báo nhầm) |
| FP16, FP32 | 16-bit / 32-bit Floating Point | Số thực dấu phẩy động 16 bit / 32 bit |
| FPN | Feature Pyramid Network | Mạng kim tự tháp đặc trưng |
| GFLOPs | Giga Floating-Point Operations | Tỉ phép tính dấu phẩy động |
| GPU | Graphics Processing Unit | Bộ xử lý đồ họa |
| HSV | Hue, Saturation, Value | Không gian màu sắc độ – bão hòa – độ sáng |
| IEEE | Institute of Electrical and Electronics Engineers | Viện Kỹ sư Điện và Điện tử (kiểu trích dẫn) |
| IoU | Intersection over Union | Tỉ lệ giao trên hợp |
| MAC | Multiply–Accumulate | Phép nhân–cộng |
| mAP | mean Average Precision | Trung bình độ chính xác trung bình |
| mAP50, mAP50–95 | mAP at IoU 0.5 / averaged over IoU 0.5–0.95 | mAP ở ngưỡng IoU 0,5 / trung bình trên các ngưỡng IoU 0,5–0,95 |
| NMS | Non-Maximum Suppression | Lọc trùng hộp không cực đại |
| P, R | Precision, Recall | Độ chính xác, độ phủ |
| P3, P4, P5 | Pyramid levels 3–5 | Các mức đặc trưng có bước 8, 16, 32 pixel |
| PAN | Path Aggregation Network | Mạng tổng hợp đường dẫn |
| PSA | Partial Self-Attention | Tự chú ý từng phần |
| SPPF | Spatial Pyramid Pooling – Fast | Gộp kim tự tháp không gian, bản nhanh |
| SS2D | 2D Selective Scan | Quét chọn lọc hai chiều (bốn hướng) |
| SSM | State Space Model | Mô hình không gian trạng thái |
| STAL | Small-Target-Aware Label assignment | Gán nhãn có ưu tiên vật nhỏ |
| TN | True Negative | Âm tính đúng |
| TP | True Positive | Dương tính đúng |
| TSVM | Topology–Shape-aware VMamba | Tên gọi tắt của mô hình đề xuất (YOLO26s-seg + C2TSVMamba) |
| VMamba | Visual Mamba (Visual State Space Model) | Mô hình không gian trạng thái thị giác |
| YOLO | You Only Look Once | Họ mô hình phát hiện một giai đoạn |
| ZOH | Zero-Order Hold | Giữ bậc không (cách rời rạc hóa SSM) |

## Ký hiệu

| Ký hiệu | Ý nghĩa | Xuất hiện ở |
|---|---|---|
| $A, B, C, \Delta$ | Ma trận trạng thái, ma trận đầu vào, ma trận đầu ra và bước thời gian của mô hình không gian trạng thái | Mục 2.6, 3.3–3.4 |
| $\bar A, \bar B$ | $A$, $B$ sau rời rạc hóa | Mục 2.6.2 |
| $h_t$ | Trạng thái ẩn tại bước $t$ | Mục 2.6, 3.4 |
| $F$, $G$ | Đặc trưng của nhánh SS2D và tín hiệu cổng; cổng có dạng $F\cdot(1+G)$ | Mục 3.3.4 |
| $b_0$, $b_1$ | Số mảnh và số lỗ của mặt nạ (hai số Betti đầu tiên) | Mục 6.4 |
| $\Delta$ (ở Chương 6) | Hiệu số chỉ số giữa hai mô hình cùng seed | Chương 6 |
| $d_z$ | Cỡ hiệu ứng Cohen cho dữ liệu ghép cặp | Mục 2.8.3, 6.2 |
| $p$ | Giá trị p của kiểm định thống kê | Mục 2.8, Chương 6 |
| SD | Độ lệch chuẩn qua các seed (ddof = 1) | Chương 6 |
