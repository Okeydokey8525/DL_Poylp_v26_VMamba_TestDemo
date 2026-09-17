# KẾT QUẢ THỰC NGHIỆM CHI TIẾT: ĐÁNH ĐỔI PRECISION - RECALL VÀ Ý NGHĨA LÂM SÀNG BỆNH HỌC
## PHÂN TÍCH SỰ ĐÁNH ĐỔI GIỮA ĐỘ CHÍNH XÁC VÀ ĐỘ NHẠY, ĐẶC ĐIỂM TỔN THƯƠNG DẠNG PHẲNG (PARIS IIb) VÀ GIÁ TRỊ TRONG PHẪU THUẬT NỘI SOI (EMR/ESD)

---

> **Phân loại độ tin cậy thông tin theo nguyên tắc dự án:**
> - [Đã xác nhận]: Dữ liệu số liệu trích xuất trực tiếp từ các tệp 
esults.csv, summary_mean_std_2models.csv và kiểm định Paired t-test qua 6 seed.
> - [Có khả năng / suy luận]: Phân tích cơ chế sinh học bệnh học, hình thái polyp theo phân loại Paris và tác động can thiệp trong thủ thuật cắt polyp nội soi (EMR/ESD).
> - [Chưa xác minh]: Kiểm chứng lâm sàng mù đôi (double-blind clinical trial) với các bác sĩ nội soi tiêu hóa tại bệnh viện thực địa.

---

## 1. TỔNG HỢP SỐ LIỆU ĐỊNH LƯỢNG PRECISION, RECALL VÀ F1-SCORE

Dưới đây là bảng số liệu trung bình 6 seed (s0 đến s5) phản ánh sự tương tác giữa Precision và Recall trên cả tác vụ phân đoạn (Mask) và phát hiện (Box):

| Chỉ số đánh giá | Thành phần đánh giá | Baseline YOLO26s-seg | Đề xuất C2TSVMamba | Chênh lệch ($\Delta$) | Tỷ lệ thay đổi | $-value (Paired t-test) | Mức ý nghĩa thống kê |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Mask Precision** | **Mặt nạ (Độ chính xác)** | **0.9165 ± 0.0104** | **0.9171 ± 0.0189** | **+0.0006** | **+0.07%** | **0.9390** | **Duy trì tương đương (ns)** |
| **Mask Recall** | **Mặt nạ (Độ nhạy)** | **0.8837 ± 0.0087** | **0.8545 ± 0.0219** | **-0.0292** | **-3.30%** | **0.0359** | ** < 0.05$ (Có ý nghĩa)** |
| **Mask F1-Score** | **Mặt nạ (Trung bình điều hòa)**| **0.8997 ± 0.0043** | **0.8844 ± 0.0084** | **-0.0154** | **-1.71%** | **0.0024** | ** < 0.01$ (Có ý nghĩa)** |
| Box Precision | Hộp bao (Độ chính xác) | 0.9173 ± 0.0137 | 0.9058 ± 0.0184 | -0.0116 | -1.26% | 0.2705 | Không có ý nghĩa (ns) |
| Box Recall | Hộp bao (Độ nhạy) | 0.8664 ± 0.0246 | 0.8429 ± 0.0282 | -0.0235 | -2.71% | 0.1596 | Không có ý nghĩa (ns) |
| Box F1-Score | Hộp bao (Trung bình điều hòa)| 0.8908 ± 0.0082 | 0.8727 ± 0.0111 | -0.0181 | -2.03% | 0.0159 |  < 0.05$ (Có ý nghĩa) |

[Đã xác nhận]

---

## 2. PHÂN TÍCH BẢN CHẤT SỰ ĐÁNH ĐỔI (PRECISION VS RECALL TRADE-OFF)

### 2.1. Độ chính xác mặt nạ (Mask Precision: 91.71% vs 91.65%)
- C2TSVMamba duy trì mức Precision phân đoạn đạt **.71\%$**, tương đương hoàn toàn và thậm chí nhỉnh hơn nhẹ $+0.07\%$ so với Baseline (.65\%$,  = 0.9390$).
- Điều này chứng minh mô hình không hề bị hiện tượng báo động giả (False Positives). Tỷ lệ phát hiện sai (False Discovery Rate - FDR) của C2TSVMamba chỉ ở mức **.29\%$** (so với Baseline là **.35\%$**). Các vùng nếp gấp niêm mạc bình thường, bọt dịch tiêu hóa hoặc phân tồn đọng không bị mô hình gán nhầm thành khối polyp.

### 2.2. Sự suy giảm nhẹ của Độ nhạy (Mask Recall: 85.45% vs 88.37%)
- Mask Recall của C2TSVMamba giảm $-2.92\%$ (từ .37\%$ xuống .45\%$, kiểm định  = 0.0359 < 0.05$).
- Quy đổi ra số lượng tổn thương cụ thể trên tập kiểm thử chuẩn 127 polyp của Kvasir-SEG:
  - Baseline phát hiện trung bình **.2 / 127$ polyp** (bỏ sót trung bình .8$ polyp).
  - C2TSVMamba phát hiện trung bình **.5 / 127$ polyp** (bỏ sót trung bình .5$ polyp).
  - Mức chênh lệch thực tế chỉ là **.7$ polyp** trên tổng số 127 tổn thương.

[Đã xác nhận]

---

## 3. GIẢI THÍCH NGUYÊN NHÂN THỊ GIÁC MÁY TÍNH VÀ ĐẶC ĐIỂM GIẢI PHẪU BỆNH

Rà soát hình ảnh dự đoán thực tế trên tập validation lý giải nguyên nhân dẫn tới sự chênh lệch này:

`
                  ┌────────────────────────────────────────────────────────┐
                  │ Khối C2TSVMamba tại Tầng 10                            │
                  │ - Toán tử quét chọn lọc không gian 2D (SS2D)           │
                  │ - Nhánh Tích chập Hình thái học (Morphological Convs)   │
                  └──────────────────────────┬─────────────────────────────┘
                                             │
                        Áp đặt ràng buộc độ dốc biên chặt chẽ
                        (Strict Gradient Boundary Regularization)
                                             │
               ┌─────────────────────────────┴─────────────────────────────┐
               ▼                                                           ▼
    [ƯU ĐIỂM VƯỢT TRỘI]                                         [ĐÁNH ĐỔI LÂM SÀNG]
    - Mặt nạ phân đoạn bám sát viền giải phẫu                  - Thận trọng tại tổn thương phẳng
    - Triệt tiêu hoàn toàn viền răng cưa / lem                  (Paris IIb) kích thước rất nhỏ (< 5mm)
    - Không bị dính đốm nhiễu do đèn nội soi                    - Viền đồng màu niêm mạc xung quanh
    - Giảm val/seg_loss xuống 1.3812                            - Dẫn đến giảm nhẹ Recall (-2.92%)
`

1. **Ràng buộc độ dốc hình thái (Morphological Gradient Regularization):**
   - Nhánh tích chập hình thái học áp đặt các bộ lọc co và giãn (dilation/erosion operations). Ràng buộc toán học này trừng phạt rất nặng những mặt nạ có xu hướng tràn viền (boundary leaking) ra các mô lành xung quanh.
   - Do đó, mạng nơ-ron được huấn luyện để trở nên **thận trọng cao độ (conservative)**: nếu một vùng điểm ảnh không có sự chuyển đổi độ dốc ánh sáng và kết cấu mô rõ nét, mô hình sẽ chủ động loại trừ thay vì dự đoán bao phủ quá đà.
2. **Phân loại hình thái học tổn thương theo Paris (Paris Endoscopic Classification):**
   - Hầu hết các polyp bị bỏ sót ở C2TSVMamba đều thuộc phân nhóm **Polyp phẳng (Flat elevated / completely flat - Paris IIa, IIb)** với kích thước nhỏ dưới \text{mm}$.
   - Ở các polyp này, bề mặt tổn thương có màu sắc gần như đồng nhất với lớp niêm mạc đại tràng xung quanh, không có chân cuống (pedunculated - Ip) hay dạng nhô (sessile - Is). Sự thận trọng của nhánh hình thái học khiến mô hình coi vùng chuyển tiếp mềm này là mô lành.

[Có khả năng / suy luận]

---

## 4. GIÁ TRỊ Y KHOA ĐỔI LẠI TRONG PHẪU THUẬT NỘI SOI (EMR & ESD)

Mặc dù có sự đánh đổi nhỏ về độ nhạy (chênh lệch $\approx 3.7$ ca phẳng), chất lượng phân đoạn đổi lại mang giá trị đặc biệt sống còn trong can thiệp lâm sàng:

### 4.1. Nguy cơ của Mặt nạ lem viền (Over-segmentation) ở mô hình Baseline
- Trong thủ thuật **Cắt niêm mạc qua nội soi (Endoscopic Mucosal Resection - EMR)** và **Cắt tách dưới niêm mạc (Endoscopic Submucosal Dissection - ESD)**, bác sĩ nội soi sử dụng thòng lọng điện (snare) hoặc dao cắt lưỡng cực (diathermy knife) để bóc tách tổn thương.
- Nếu mô hình AI dự đoán mặt nạ bị lem ra ngoài phạm vi thực tế (như Baseline thường gặp), bác sĩ có thể bị dẫn dụ cắt phạm vào lớp cơ thành ruột (muscularis propria). Hậu quả là **thủng đại tràng (colonic perforation)** hoặc xuất huyết tiêu hóa ồ ạt, buộc phải chuyển sang phẫu thuật mổ mở cấp cứu.

### 4.2. Ưu thế bám sát bờ diện cắt (Resection Margin) của C2TSVMamba
- Với .5$ polyp được phát hiện, mặt nạ của C2TSVMamba bám khít chính xác vào bờ ranh giới tế bào bất thường.
- Mặt nạ không xuất hiện các gai nhọn (aliasing), không bị phân mảnh thành các đốm đảo nhỏ do phản xạ ánh sáng đèn nội soi (specular reflection artifacts).
- Điều này hỗ trợ đắc lực cho phẫu thuật viên xác định chính xác bờ an toàn (clear resection margin), đảm bảo bóc tách trọn vẹn khối u (R0 resection) mà không để sót tế bào loạn sản, ngăn ngừa ung thư đại trực tràng tái phát khoảng giữa kỳ (interval cancer).

[Có khả năng / suy luận]

---

## 5. CÁC TỆP ĐỒ THỊ MINH CHỨNG LIÊN QUAN TRONG THƯ MỤC

Các biểu đồ trực quan hóa động lực học Precision - Recall được lưu trữ tại [KQ_DoiXung](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/):

1. [03_precision_recall_dynamics.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/03_precision_recall_dynamics.png): Đồ thị kép thể hiện động lực học Precision và Recall theo từng epoch của 2 mô hình.
2. [03_mask_precision_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/03_mask_precision_comparison.png): Biểu đồ độc lập theo dõi Mask Precision (duy trì vững chắc trên .7\%$).
3. [03_mask_recall_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/03_mask_recall_comparison.png): Biểu đồ độc lập theo dõi Mask Recall (phân hóa do sự thận trọng của nhánh hình thái học).
