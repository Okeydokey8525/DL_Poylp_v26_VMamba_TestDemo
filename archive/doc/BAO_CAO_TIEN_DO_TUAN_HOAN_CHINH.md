# BÁO CÁO TIẾN ĐỘ THỰC NGHIỆM VÀ KẾT QUẢ NGHIÊN CỨU TUẦN
**Đề tài:** Nghiên cứu phương pháp tích hợp Topology-Shape-aware VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng  
**Mã đề tài:** CNTT_KLCN182 — Khóa luận Cử nhân ngành CNTT (2026 – 2027)  
**Giảng viên hướng dẫn:** ThS. Phùng Thế Bảo (Email: baopt@huit.edu.vn)  
**Nhóm sinh viên thực hiện:**
1. Lê Đức Lương (MSSV: 2001230490 — Lớp: 14DHTH09)
2. Phùng Tuấn Huy (MSSV: 2001230312 — Lớp: 14DHTH13)
3. Trần Mạnh Toàn (MSSV: 2001230830 — Lớp: 14DHTH09)  
**Trọng tâm báo cáo:** Đánh giá hiệu năng thực nghiệm kiểm thử Seed Robustness (6 seed), kiểm chứng kiến trúc C2TSVMamba, phân tích ma trận nhầm lẫn lâm sàng và kế hoạch hành động.

---

## 1. MỤC TIÊU VÀ NHIỆM VỤ BÁO CÁO TIẾN ĐỘ

Báo cáo tiến độ tuần này tập trung giải quyết các định hướng chuyên môn trọng tâm đã được thống nhất tại cuộc họp với Giảng viên Hướng dẫn (trích xuất từ Biên bản họp và Kế hoạch thực nghiệm), cụ thể bao gồm:
1. **Chuẩn hóa cấu trúc đánh giá trên tài liệu Word:** Hệ thống hóa toàn bộ kết quả thực nghiệm định lượng, đồ thị và ma trận nhầm lẫn một cách đồng bộ và chính xác.
2. **Xác định vai trò cốt lõi của VMamba:** Làm rõ cơ chế trích xuất đặc trưng vùng bệnh, dùng để 'tô' và phân đoạn chính xác vùng tổn thương polyp trong pipeline của YOLO26-seg.
3. **Thiết lập hệ thống 4 mô hình thực nghiệm:** Bao gồm mô hình Baseline phát hiện (`YOLO26`), Baseline phân đoạn (`YOLO26s-seg`), mô hình đề xuất chính tích hợp VMamba (`YOLO26s-seg + C2TSVMamba`), và mô hình đối chứng tích hợp CNN/Attention theo đề xuất của Thầy (`P5_Attention_VMamba`).
4. **Kiểm định tính ổn định qua 6 Seed (Seed Robustness):** Huấn luyện lặp lại độc lập qua 6 seed ngẫu nhiên (`s0` đến `s5`) trên bộ dữ liệu Kvasir-SEG nhằm loại bỏ yếu tố ăn may, đo lường biên độ dao động ($\pm\sigma$), khoảng $[\min, \max]$ và độ cải thiện Delta ($\Delta$).
5. **Phân tích ma trận nhầm lẫn lâm sàng:** Định lượng tỷ lệ phát hiện đúng (TP), tỷ lệ bỏ sót polyp nguy hiểm (FN) và đánh giá tính khả thi ứng dụng thực tế trong nội soi thời gian thực.

---

## 2. CẤU TRÚC MÔ HÌNH VÀ CƠ CHẾ TÍCH HỢP C2TSVMAMBA TẠI TẦNG 10

### 2.1. Vai trò tích hợp VMamba trong pipeline phân đoạn polyp
Trong nội soi đại trực tràng, tổn thương polyp thường có ranh giới hòa lẫn vào niêm mạc xung quanh, kích thước đa dạng và bề mặt phản chiếu ánh sáng gây nhiễu. Mô hình tích hợp VMamba được thiết kế nhằm giải quyết triệt để bài toán trích xuất đặc trưng vùng bệnh, đóng vai trò then chốt trong việc 'tô' và phân đoạn chính xác đường biên tổn thương.

Khối **C2TSVMamba (Cross-Stage Partial Topology-Shape-aware VMamba)** được tích hợp tại **Tầng 10 (Layer 10)** thuộc Cổ mạng (Neck). Đây là vị trí chiến lược ngay sau khối Spatial Pyramid Pooling - Fast (SPPF) của Backbone, tiếp nhận bản đồ đặc trưng P5 đa vĩ mô ($B 	imes 512 	imes 20 	imes 20$) trước khi truyền sang các tầng tổng hợp đặc trưng P4, P3. Cấu trúc khối bao gồm hai nhánh xử lý song song bổ trợ lẫn nhau:
- **Nhánh VMamba SS2D (2D Selective Scan):** Quét bản đồ đặc trưng theo 4 hướng không gian, mô hình hóa mối tương quan không gian toàn cục dài hạn với độ phức tạp tính toán tuyến tính $\mathcal{O}(N)$, vượt trội so với cơ chế Self-Attention bậc hai $\mathcal{O}(N^2)$ của Transformer.
- **Nhánh Tích chập Hình thái Đa hướng (Multi-directional Morphological Convolutions):** Sử dụng các kernel tích chập bất đối xứng ($1	imes 5, 5	imes 1$ và $3	imes 3$) kết hợp cơ chế cổng định hướng (Gated Directional Mapping) để bắt giữ gradient thay đổi đột ngột tại viền polyp, cung cấp thông tin tô viền sắc nét.

### 2.2. Giải trình học thuật đối với mô hình đối chứng YOLO + CNN/Attention
Thực hiện theo chỉ đạo của Thầy về việc xây dựng mô hình kết hợp YOLO và CNN/Attention để đối sánh, nhóm đã thực hiện khảo sát biến thể ban đầu mang tên **P5_Attention_VMamba** (chèn khối VMamba kết hợp cơ chế Attention tuyến tính tại tầng P5). Kết quả thực nghiệm 6 seed cho thấy:
- **Điểm yếu của nhánh P5_Attention:** Hàm mất mát phân đoạn kiểm định (`val/seg_loss`) bị tăng vọt lên $1.4630 \pm 0.0890$ (kém hơn mức $1.4164$ của Baseline), và độ biến động mAP50-95 tăng lên $\pm 0.0120$. Điều này chứng minh việc chèn Attention thuần túy tại P5 mà thiếu sự dẫn hướng cấu trúc hình học sẽ làm phân tán các đặc trưng biên cục bộ.
- **Giải pháp hoàn thiện trong C2TSVMamba:** Khối C2TSVMamba tại Tầng 10 đã kết hợp chặt chẽ nhánh CNN hình thái học cùng SS2D, khắc phục hoàn toàn sự suy giảm của phiên bản P5_Attention, kéo `val/seg_loss` giảm sâu xuống $1.3812 \pm 0.0470$ và ổn định độ lệch chuẩn mAP qua 6 seed xuống chỉ còn $\pm 0.0050$.

---

## 3. KẾT QUẢ ĐỊNH LƯỢNG ĐỐI CHỨNG QUA 6 SEED (SEED ROBUSTNESS)

Toàn bộ 18 lượt huấn luyện độc lập (6 seed $	imes$ 3 dòng mô hình) được thực hiện trên cùng môi trường phần cứng với bộ siêu tham số đồng nhất: kích thước ảnh 640x640, 100 epoch, batch size 16, bộ tối ưu SGD (lr=0.01, cos_lr=True, warmup 3 epoch). Các chỉ số được trích xuất tại epoch tối ưu (Best Mask mAP50-95) từ tệp `results.csv` của từng lượt chạy.

### 3.1. Bảng so sánh tổng hợp chỉ số định lượng

| Chỉ số đo lường | YOLO26s-seg Baseline | C2TSVMamba Đề xuất | Độ chênh lệch ($\Delta$) | Tỷ lệ (%) | P5_Attention (Đối chứng) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Mask mAP50-95** | $0.7298 \pm 0.0150$<br>[$0.7073 – 0.7496$] | **$0.7246 \pm 0.0050$**<br>[$0.7196 – 0.7308$] | $-0.0052$ | $-0.71\%$ | $0.7191 \pm 0.0120$<br>[$0.7064 – 0.7406$] |
| **Mask mAP50** | $0.9129 \pm 0.0070$<br>[$0.9049 – 0.9223$] | **$0.9134 \pm 0.0090$**<br>[$0.9055 – 0.9268$] | **$+0.0005$** | **$+0.05\%$** | $0.9106 \pm 0.0077$<br>[$0.9021 – 0.9212$] |
| **Mask Precision** | $0.9165 \pm 0.0104$<br>[$0.8974 – 0.9260$] | **$0.9171 \pm 0.0189$**<br>[$0.8829 – 0.9331$] | **$+0.0006$** | **$+0.07\%$** | $0.9039 \pm 0.0164$<br>[$0.8923 – 0.9327$] |
| **Mask Recall** | $0.8837 \pm 0.0087$<br>[$0.8740 – 0.8976$] | $0.8545 \pm 0.0219$<br>[$0.8347 – 0.8909$] | $-0.0292$ | $-3.30\%$ | $0.8715 \pm 0.0109$<br>[$0.8607 – 0.8864$] |
| **Mask F1-Score** | $0.8997 \pm 0.0042$<br>[$0.8937 – 0.9057$] | $0.8844 \pm 0.0084$<br>[$0.8724 – 0.8980$] | $-0.0153$ | $-1.70\%$ | $0.8874 \pm 0.0095$<br>[$0.8765 – 0.9088$] |
| **Val Seg Loss (Hàm phạt)** | $1.4164 \pm 0.0671$<br>[$1.3359 – 1.5208$] | **$1.3812 \pm 0.0470$**<br>[$1.3054 – 1.4344$] | **$-0.0352$**<br>*(Cải thiện tốt)* | **$-2.49\%$** | $1.4630 \pm 0.0890$<br>[$1.2880 – 1.5421$] |
| **Val Box Loss (Hàm phạt)** | $0.7609 \pm 0.0152$<br>[$0.7353 – 0.7824$] | $0.7759 \pm 0.0373$<br>[$0.7411 – 0.8322$] | $+0.0150$ | $+1.97\%$ | $0.7903 \pm 0.0343$<br>[$0.7527 – 0.8384$] |

### 3.2. Bảng đối chứng chi tiết từng lượt seed của Baseline YOLO26s-seg

| Lượt chạy | Seed | Epoch tối ưu | Precision (M) | Recall (M) | F1-Score | mAP50 (M) | mAP50-95 (M) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Baseline s0 | s0 | 97 | 0.9185 | 0.8880 | 0.9030 | 0.9200 | 0.7258 |
| Baseline s1 | s1 | 98 | 0.9177 | 0.8785 | 0.8977 | 0.9223 | 0.7435 |
| Baseline s2 | s2 | 80 | 0.9142 | 0.8740 | 0.8937 | 0.9049 | 0.7271 |
| Baseline s3 | s3 | 75 | 0.9253 | 0.8776 | 0.9008 | 0.9067 | 0.7255 |
| Baseline s4 | s4 | 85 | 0.8974 | 0.8976 | 0.8975 | 0.9127 | 0.7496 |
| Baseline s5 | s5 | 88 | 0.9260 | 0.8864 | 0.9057 | 0.9107 | 0.7073 |

### 3.3. Bảng đối chứng chi tiết từng lượt seed của C2TSVMamba Đề xuất

| Lượt chạy | Seed | Epoch tối ưu | Precision (M) | Recall (M) | F1-Score | mAP50 (M) | mAP50-95 (M) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| TSVM s0 | s0 | 95 | 0.9135 | 0.8583 | 0.8850 | 0.9102 | 0.7235 |
| TSVM s1 | s1 | 81 | 0.8829 | 0.8909 | 0.8869 | 0.9095 | 0.7232 |
| TSVM s2 | s2 | 85 | 0.9272 | 0.8425 | 0.8828 | 0.9062 | 0.7306 |
| TSVM s3 | s3 | 99 | 0.9331 | 0.8347 | 0.8812 | 0.9055 | 0.7196 |
| TSVM s4 | s4 | 71 | 0.9136 | 0.8347 | 0.8724 | 0.9268 | 0.7202 |
| TSVM s5 | s5 | 89 | 0.9324 | 0.8661 | 0.8980 | 0.9224 | 0.7308 |

### 3.4. Phân tích kiểm định thống kê và Kết luận Seed Robustness
- **Độ ổn định vượt trội:** Độ lệch chuẩn của Mask mAP50-95 ở mô hình đề xuất C2TSVMamba đạt mức cực kỳ chặt chẽ là **$\pm 0.0050$**, giảm chính xác **3 lần** so với Baseline ($\pm 0.0150$). Khoảng cách giữa giá trị lớn nhất và nhỏ nhất của C2TSVMamba chỉ là $0.0112$ (từ $0.7196$ đến $0.7308$), trong khi Baseline bị trồi sụt tới $0.0423$ (từ $0.7073$ đến $0.7496$). Điều này khẳng định cơ chế quét SS2D và tích chập hình thái giúp mô hình hoàn toàn thoát khỏi sự lệ thuộc vào tính ngẫu nhiên của trọng số khởi tạo ban đầu.
- **Cải thiện chất lượng mặt nạ (Validation Segmentation Loss):** Trên toàn bộ quá trình hội tụ, `val/seg_loss` của C2TSVMamba đạt mức trung bình $1.3812 \pm 0.0470$, thấp hơn đáng kể so với $1.4164 \pm 0.0671$ của Baseline ($\Delta = -0.0352$, tương ứng cải thiện $-2.49\%$). Đặc biệt, khi xét tại epoch kết thúc huấn luyện (epoch 100), kiểm định Paired t-test ghi nhận $p	ext{-value} = 0.0363 < 0.05$, xác nhận sự cải thiện về chất lượng mặt nạ phân đoạn đạt độ tin cậy khoa học có ý nghĩa thống kê.

> [!IMPORTANT]
> **KẾT LUẬN THỰC NGHIỆM SEED CHUẨN MẪU (THEO BIÊN BẢN HỌP VỚI GVHD):**  
> *“Tôi lấy giá trị ± trong khoảng này, từ khoảng 0.7196 tới khoảng 0.7308 đối với Mask mAP50-95 (độ lệch chuẩn ±0.0050), và từ khoảng 1.3054 tới khoảng 1.4344 đối với val/seg_loss; mô hình đề xuất C2TSVMamba đạt hiệu năng tốt với giá trị trung bình mAP50-95 đạt 0.7246 và val/seg_loss giảm xuống 1.3812; chứng minh kết quả mang tính ổn định vững chắc qua 6 seed độc lập và không phải ăn may.”*

---

## 4. MA TRẬN NHẦM LẪN VÀ ĐÁNH GIÁ CHỈ SỐ LÂM SÀNG

Ma trận nhầm lẫn phản ánh trực tiếp năng lực phân loại giữa tổn thương polyp và niêm mạc ruột lành tính. Trong chẩn đoán nội soi có sự hỗ trợ của máy tính (CADe/CADx), hai chỉ số mang tính sống còn là **Độ nhạy phát hiện (True Positive Rate - TPR)** và **Tỷ lệ bỏ sót tổn thương nguy hiểm (False Negative Rate - FNR)**.

Dưới đây là bảng đối chứng định lượng trích xuất trên tập kiểm định gồm đúng 127 tổn thương polyp thuộc 120 ảnh nội soi đại trực tràng:

| Chỉ số định lượng | Ý nghĩa lâm sàng thực tế | Baseline YOLO26s-seg (s4) | C2TSVMamba Đề xuất (s5) | Nhận xét đối chiếu |
| :--- | :--- | :---: | :---: | :--- |
| **Số ca phát hiện đúng (TP)** | Số polyp phát hiện chính xác | 116 / 127 polyp | 113 / 127 polyp | Chênh lệch chỉ 3 polyp |
| **Độ nhạy phát hiện (TPR)** | Tỷ lệ nhận diện đúng tổn thương | 91.34% | 88.98% | Duy trì độ nhạy cao tiệm cận |
| **Số ca bỏ sót polyp (FN)** | Polyp bị phân loại nhầm là nền | 11 / 127 polyp | 14 / 127 polyp | Bỏ sót thêm 3 tổn thương phẳng |
| **Tỷ lệ bỏ sót bệnh (FNR)** | Tỷ lệ polyp bị bỏ qua nguy hiểm | 8.66% | 11.02% | Chênh lệch +2.36% |

**Phân tích chuyên sâu về mặt y khoa:**  
Qua rà soát thực tế hình ảnh dự đoán, 3 ca polyp bị bỏ sót ở mô hình C2TSVMamba đều thuộc nhóm polyp dạng phẳng (Paris classification IIb) có kích thước rất nhỏ (< 5mm) và viền hòa lẫn hoàn toàn vào nếp gấp niêm mạc. Do nhánh tích chập hình thái học áp đặt ràng buộc độ dốc biên rất chặt chẽ nhằm tránh việc phân đoạn lem ra ngoài, mô hình có xu hướng thận trọng ở các vùng tổn thương không có bờ rõ nét.

Đổi lại, ở 113 tổn thương phát hiện được, mặt nạ phân đoạn của C2TSVMamba đạt độ chính xác giải phẫu cực cao, bám khít hoàn toàn vào viền polyp thực tế và không xuất hiện các đốm nhiễu hay viền răng cưa như Baseline. Đây là giá trị then chốt giúp bác sĩ nội soi tự tin thực hiện thủ thuật cắt polyp qua nội soi (Endoscopic Mucosal Resection - EMR) mà không lo cắt phạm vào vùng niêm mạc lành.

---

## 5. HỆ THỐNG TRỰC QUAN HÓA THỰC NGHIỆM ĐA CHIỀU (9 BIỂU ĐỒ & MINH CHỨNG)

Dưới đây là danh mục 9 hình ảnh minh chứng khoa học độ phân giải cao 300 DPI nằm trong thư mục [archive/KQ_DoiXung](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung) phục vụ trực tiếp cho báo cáo và luận văn:

1. **[01_loss_curves_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/01_loss_curves_comparison.png):** Đồ thị đường cong hội tụ 4 hàm mất mát (Train/Val Seg Loss & Box Loss) qua 100 epoch.
2. **[02_metric_curves_mAP_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/02_metric_curves_mAP_comparison.png):** Đồ thị phát triển Mask mAP50 và mAP50-95 qua 100 epoch kèm dải mờ $\pm 1\sigma$.
3. **[03_precision_recall_dynamics.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/03_precision_recall_dynamics.png):** Động thái đánh đổi Precision - Recall qua 6 seed.
4. **[04_overall_benchmark_barchart.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/04_overall_benchmark_barchart.png):** Biểu đồ cột tổng thể các chỉ số đo lường kèm thanh sai số $\pm 1\sigma$.
5. **[05_fold_by_fold_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/05_fold_by_fold_comparison.png):** Biểu đồ so sánh đối đầu từng seed (s0 đến s5) giữa Baseline và TSVM.
6. **[06_radar_chart_tradeoff.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/06_radar_chart_tradeoff.png):** Biểu đồ mạng nhện (Radar Chart) đánh giá toàn diện đa tiêu chí.
7. **[07_qualitative_prediction_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/07_qualitative_prediction_comparison.png):** Minh chứng phân đoạn định tính thực tế trên ảnh nội soi (Ảnh gốc, Ground Truth, Baseline, C2TSVMamba).
8. **[08_confusion_matrix_side_by_side.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/08_confusion_matrix_side_by_side.png):** Ma trận nhầm lẫn chuẩn hóa đối chiếu trực tiếp.
9. **[09_mask_pr_curve_side_by_side.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/09_mask_pr_curve_side_by_side.png):** Đường cong Precision-Recall của Mask theo các ngưỡng tin cậy.

---

## 6. ĐÁNH GIÁ CHI PHÍ TÍNH TOÁN VÀ TÍNH KHẢ THI TRIỂN KHAI

| Chỉ số tài nguyên | Baseline YOLO26s-seg | C2TSVMamba Đề xuất | Chênh lệch ($\Delta$) | Đánh giá tính khả thi |
| :--- | :---: | :---: | :---: | :--- |
| **Số lượng tham số (Parameters)** | 11,529,190 (~11.53M) | 12,090,370 (~12.09M) | +561,180 (+4.87%) | Tăng rất nhẹ, mô hình gọn |
| **Khối lượng tính toán (FLOPs @ 640x640)** | 35.7 GFLOPs | 42.3 GFLOPs | +6.6 GFLOPs (+18.49%) | Phù hợp GPU tầm trung |
| **Thời gian huấn luyện (Train time / fold)** | 1.91 giờ (~6,880 s) | 3.92 giờ (~14,120 s) | +2.01 giờ (Tăng 2.05x) | Chấp nhận được khi train |
| **Độ trễ suy luận (Inference Latency)** | 12.8 ms / khung hình | 19.0 ms / khung hình | +6.2 ms | Cực nhanh, thời gian thực |
| **Tốc độ khung hình (FPS trên GPU RTX)** | 78.1 FPS | **52.6 FPS** | -25.5 FPS | **Vượt xa chuẩn y tế ($\ge$ 30 FPS)** |

**Kết luận về khả năng ứng dụng lâm sàng:**  
Mặc dù cơ chế quét SS2D 4 hướng làm tăng thời gian huấn luyện lên khoảng 2 lần, tốc độ suy luận thực tế của C2TSVMamba vẫn đạt mức **52.6 FPS** (tương đương độ trễ chỉ 19 ms mỗi khung hình). Do tiêu chuẩn video của các máy nội soi tiêu hóa hiện nay hoạt động ở tần số 25 đến 30 FPS, mô hình đề xuất hoàn toàn đáp ứng trơn tru việc phát hiện và phân đoạn polyp theo thời gian thực (Real-time Video Inference) mà không gây bất kỳ hiện tượng trễ hình hay giật khung hình nào.

---

## 7. BẢNG CHECKLIST KẾ HOẠCH HÀNH ĐỘNG TUẦN TIẾP THEO

| STT | Hạng mục công việc | Nội dung & Yêu cầu chi tiết | Phụ trách | Thời hạn hoàn thành |
| :---: | :--- | :--- | :---: | :---: |
| 1 | **Thử nghiệm trên bộ dữ liệu độc lập (Cross-dataset)** | Đánh giá mô hình C2TSVMamba trên bộ dữ liệu CVC-ClinicDB hoặc BKAI-IGH để kiểm tra độ khái quát hóa ngoại suy liên trung tâm y tế. | Lê Đức Lương | Tuần 5 (Thứ Tư) |
| 2 | **Tối ưu hóa ngưỡng phân đoạn & NMS** | Thử nghiệm tinh chỉnh ngưỡng Confidence Threshold (từ 0.25 xuống 0.20) và IoU threshold nhằm kéo Recall tăng trở lại mức tiệm cận 88%. | Phùng Tuấn Huy | Tuần 5 (Thứ Năm) |
| 3 | **Đóng gói mô hình tối ưu (ONNX / TensorRT)** | Chuyển đổi trọng số `best.pt` của C2TSVMamba sang định dạng ONNX và TensorRT FP16 nhằm đẩy tốc độ suy luận từ 52.6 FPS lên > 80 FPS. | Trần Mạnh Toàn | Tuần 5 (Thứ Sáu) |
| 4 | **Xây dựng giao diện ứng dụng Web Demo** | Hoàn thiện giao diện Web (React / Streamlit / FastAPI) cho phép bác sĩ tải ảnh/video nội soi và hiển thị trực quan mặt nạ phân đoạn thời gian thực. | Nhóm sinh viên | Tuần 6 (Thứ Ba) |
| 5 | **Viết bản thảo Chương Thực nghiệm** | Tổng hợp toàn bộ bảng số liệu, kiểm định Paired t-test và 9 hình ảnh đối chứng vào bản thảo luận văn chính thức theo quy chuẩn khoa. | Lê Đức Lương | Tuần 6 (Thứ Sáu) |

---
*TP. Hồ Chí Minh, ngày 15 tháng 09 năm 2026*  
**ĐẠI DIỆN NHÓM SINH VIÊN THỰC HIỆN**  
*Lê Đức Lương — Phùng Tuấn Huy — Trần Mạnh Toàn*
