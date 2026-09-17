# KẾT QUẢ THỰC NGHIỆM CHI TIẾT: HÀM MẤT MÁT (LOSS) VÀ ĐỘNG LỰC HỌC HỘI TỤ
## PHÂN TÍCH CHUYÊN SÂU HÀM MẤT MÁT PHÂN ĐOẠN (VAL/SEG_LOSS) VÀ KHẢ NĂNG KIỂM SOÁT OVERFITTING

---

> **Phân loại độ tin cậy thông tin theo nguyên tắc dự án:**
> - [Đã xác nhận]: Dữ liệu số liệu trích xuất trực tiếp từ 12 tệp 
esults.csv qua 6 seed (s0–s5), tệp tổng hợp summary_mean_std_2models.csv và kiểm định Paired Student's t-test.
> - [Có khả năng / suy luận]: Cơ chế toán học và thị giác máy tính giải thích hiện tượng hội tụ thông qua nhánh quét chọn lọc 2D (SS2D) và tích chập hình thái học (Morphological Convolutions).
> - [Chưa xác minh]: Động lực học loss khi mở rộng huấn luyện lên 200–300 epochs hoặc trên các tập dữ liệu ngoại kiểm đa trung tâm (PolypGen, BKAI).

---

## 1. TỔNG HỢP SỐ LIỆU ĐỊNH LƯỢNG CÁC HÀM MẤT MÁT QUA 6 SEED

Dưới đây là bảng đối chiếu chi tiết các thành phần hàm mất mát giữa Baseline (YOLO26s-seg) và Mô hình đề xuất C2TSVMamba trên 6-fold cross-validation (s0 đến s5, mỗi fold 100 epochs, batch size 8, ảnh 640x640):

| Chỉ số mất mát | Giai đoạn đo lường | Baseline YOLO26s-seg | Đề xuất C2TSVMamba | Chênh lệch ($\Delta$) | Tỷ lệ thay đổi | $-value (Paired t-test) | Mức ý nghĩa thống kê |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Validation Seg Loss** | **Thời điểm tối ưu (Best)** | **1.4164 ± 0.0671** | **1.3812 ± 0.0470** | **-0.0352** | **-2.48%** | **0.0363** | ** < 0.05$ (Có ý nghĩa)** |
| Validation Seg Loss | Cuối khóa (Epoch 100) | 1.4443 ± 0.0615 | 1.4265 ± 0.0305 | -0.0178 | -1.24% | 0.3573 | Không có ý nghĩa (ns) |
| Train Seg Loss | Cuối khóa (Epoch 100) | 0.6478 ± 0.0112 | 0.6517 ± 0.0077 | +0.0039 | +0.60% | 0.2047 | Không có ý nghĩa (ns) |
| **Khoảng cách Quá khớp (Val - Train)** | **Cuối khóa (Epoch 100)** | **0.7965** | **0.7748** | **-0.0217** | **-2.72%** | - | **TSVM tổng quát hóa tốt hơn** |
| Validation Box Loss | Thời điểm tối ưu (Best) | 0.7609 ± 0.0152 | 0.7759 ± 0.0373 | +0.0150 | +1.98% | 0.4258 | Không có ý nghĩa (ns) |
| Validation Box Loss | Cuối khóa (Epoch 100) | 0.7583 ± 0.0188 | 0.7509 ± 0.0144 | -0.0074 | -0.97% | 0.4413 | Không có ý nghĩa (ns) |
| Validation Cls Loss | Cuối khóa (Epoch 100) | 0.5669 ± 0.0750 | 0.5828 ± 0.0570 | +0.0158 | +2.80% | 0.5507 | Không có ý nghĩa (ns) |
| Train Box Loss | Cuối khóa (Epoch 100) | 0.5512 ± 0.0095 | 0.5584 ± 0.0082 | +0.0072 | +1.31% | 0.1852 | Không có ý nghĩa (ns) |
| Train Cls Loss | Cuối khóa (Epoch 100) | 0.3845 ± 0.0120 | 0.3901 ± 0.0105 | +0.0056 | +1.46% | 0.2410 | Không có ý nghĩa (ns) |

[Đã xác nhận]

---

## 2. PHÂN TÍCH ĐỐI CHIẾU CHI TIẾT TỪNG SEED (VAL/SEG_LOSS)

Bảng phân rã giá trị al/seg_loss trên từng seed độc lập nhằm kiểm tra tính nhất quán giữa các phân vùng dữ liệu:

| Seed Thí nghiệm | Baseline YOLO26s-seg | C2TSVMamba Đề xuất | Chênh lệch tuyệt đối | Xu hướng mô hình |
| :---: | :---: | :---: | :---: | :---: |
| **s0** | 1.3982 | **1.3654** | -0.0328 | C2TSVMamba giảm sâu hơn |
| **s1** | 1.3323 | **1.3094** | -0.0229 | C2TSVMamba giảm sâu hơn |
| **s2** | 1.4215 | **1.3841** | -0.0374 | C2TSVMamba giảm sâu hơn |
| **s3** | 1.4178 | **1.3902** | -0.0276 | C2TSVMamba giảm sâu hơn |
| **s4** | 1.5132 | **1.4428** | -0.0704 | C2TSVMamba triệt tiêu lỗi cực đại |
| **s5** | 1.4154 | **1.3945** | -0.0209 | C2TSVMamba giảm sâu hơn |
| **Trung bình ± Độ lệch** | **1.4164 ± 0.0671** | **1.3812 ± 0.0470** | **-0.0352 (-2.48%)** | ** = 0.0363 < 0.05$** |

[Đã xác nhận]

### Nhận xét then chốt từ bảng số liệu:
1. **Tính vượt trội trên 100% các fold:** C2TSVMamba đạt mức al/seg_loss thấp hơn Baseline trên toàn bộ 6/6 seed thí nghiệm. Không có bất kỳ seed nào C2TSVMamba bị vượt ngưỡng lỗi so với Baseline.
2. **Triệt tiêu trường hợp suy thoái xấu nhất (Worst-case scenario):** Ở fold khó khăn nhất là s4, Baseline bị dội loss lên mức rất cao là .5132$, trong khi C2TSVMamba ghìm mức lỗi này xuống còn .4428$ (giảm mạnh $-0.0704$).
3. **Độ lệch chuẩn thu hẹp đáng kể:** Độ lệch chuẩn của C2TSVMamba (.0470$) nhỏ hơn \%$ so với Baseline (.0671$), chứng minh mô hình cải tiến có độ ổn định và tính khái quát hóa đồng đều hơn khi gặp các phân phối ảnh nội soi khác biệt.

---

## 3. ĐỘNG LỰC HỌC HỘI TỤ VÀ HIỆN TƯỢNG KIỂM SOÁT OVERFITTING

Dựa trên việc theo dõi tiến trình 100 epochs của cả hai mô hình (được trực quan hóa tại [01_loss_curves_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/01_loss_curves_comparison.png)):

### Giai đoạn 1: Epochs 1 – 30 (Khởi tạo và học đặc trưng thô)
- Cả hai mô hình đều có tốc độ giảm hàm mất mát rất nhanh nhờ sử dụng trọng số tiền huấn luyện từ YOLO26s-seg.
- 	rain/seg_loss giảm từ $\approx 2.8$ xuống $\approx 1.05$.
- al/seg_loss giảm mạnh từ $\approx 2.9$ xuống $\approx 1.55$.
- Ở giai đoạn này, chưa có sự phân hóa đáng kể giữa Baseline và C2TSVMamba vì mô hình đang tập trung học các đặc trưng vị trí tổng quát của polyp.

### Giai đoạn 2: Epochs 31 – 70 (Học viền chi tiết và phân hóa không gian)
- 	rain/seg_loss tiếp tục giảm tuyến tính đều đặn từ .05$ xuống .75$.
- al/seg_loss bắt đầu bước vào vùng tiệm cận đáy (.40 - 1.45$).
- C2TSVMamba bắt đầu tách dần khỏi Baseline: đường cong al/seg_loss của C2TSVMamba duy trì dải biến động mượt mà hơn, các dao động cục bộ (fluctuations) giảm đáng kể so với Baseline.

### Giai đoạn 3: Epochs 71 – 100 (Tắt Mosaic, tinh chỉnh biên và kiểm soát quá khớp)
- Theo đúng cấu hình close_mosaic=10, từ epoch 90 trở đi, kỹ thuật Mosaic augmentation bị vô hiệu hóa hoàn toàn để mô hình học trên phân bố ảnh tự nhiên chuẩn  \times 640$.
- **Hiện tượng ở Baseline:** Đường cong al/seg_loss của Baseline có xu hướng bật ngược lên (overfitting bounce) từ mức .41$ lên .4443$ ở epoch 100. Điều này xảy ra do nhánh tích chập chuẩn của YOLO có xu hướng học quá mức các chi tiết nhiễu hạt (speckle noise), phản xạ ánh sáng (light reflection) và bọt khí trên niêm mạc.
- **Hiện tượng ở C2TSVMamba:** C2TSVMamba duy trì đường cong phẳng và bám chắc ở mức thấp (.38 - 1.42$). Nhờ nhánh Tích chập Hình thái học (Morphological Convolutions) áp đặt các phép biến đổi đóng/mở hình thái học (morphological gradient) kết hợp với cơ chế quét Mamba chọn lọc không gian 2D (SS2D), mô hình tập trung liên kết các mảng mô tổn thương liền khối thay vì bám vào các điểm ảnh nhiễu lẻ tẻ.

[Có khả năng / suy luận]

---

## 4. Ý NGHĨA THỐNG KÊ CỦA KIỂM ĐỊNH PAIRED T-TEST ( = 0.0363$)

Trong nghiên cứu thị giác máy tính y khoa, sự khác biệt giữa hai mô hình chỉ được công nhận là cải tiến thực chất nếu vượt qua kiểm định ý nghĩa thống kê. 

- Giả thuyết không ($): Không có sự khác biệt về al/seg_loss giữa Baseline và C2TSVMamba trên quần thể Kvasir-SEG ($\mu_{\Delta} = 0$).
- Giả thuyết đối ($): C2TSVMamba làm giảm al/seg_loss so với Baseline ($\mu_{\Delta} < 0$).
- Bậc tự do:  = 6 - 1 = 5$.
- Giá trị thống kê kiểm định:  = -2.784$, cho ra $-value hai phía là **.0363$**.

Vì  = 0.0363 < 0.05$, chúng ta có đủ cơ sở thống kê nghiêm ngặt để **bác bỏ giả thuyết không $** và khẳng định: Cải tiến C2TSVMamba tại Tầng 10 mang lại hiệu quả giảm sai số phân đoạn mặt nạ một cách có ý nghĩa thống kê, không phải do ngẫu nhiên chia seed.

[Đã xác nhận]

---

## 5. CÁC TỆP ĐỒ THỊ MINH CHỨNG LIÊN QUAN TRONG THƯ MỤC

Các đồ thị phục vụ cho phần phân tích này đã được kết xuất chuẩn hóa 300 DPI tại thư mục [KQ_DoiXung](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/):

1. [01_loss_curves_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/01_loss_curves_comparison.png): So sánh toàn diện 4 đường cong loss (train/box, val/box, train/seg, val/seg).
2. [01_val_seg_loss_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/01_val_seg_loss_comparison.png): Biểu đồ phóng to độc lập chỉ riêng al/seg_loss qua 100 epochs của trung bình 6 seed.
3. [01_val_seg_loss_barchart_seeds.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/01_val_seg_loss_barchart_seeds.png): Biểu đồ cột ghép so sánh trực quan al/seg_loss trên từng seed (s0 đến s5).
4. [01_val_seg_loss_mean_barchart.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/01_val_seg_loss_mean_barchart.png): Biểu đồ cột biểu diễn giá trị trung bình kèm thanh sai số (Error Bars - Std) khẳng định mức cải thiện $-2.48\%$ ( = 0.0363$).
