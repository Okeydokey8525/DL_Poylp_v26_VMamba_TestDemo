# Kết Luận Và Nhận Xét Khoa Học (Academic Conclusions)
## Đối sánh 10 Seed: YOLO26s-seg Baseline và YOLO26s-seg + TSVM

Tất cả các nhận xét dưới đây được xây dựng hoàn toàn dựa trên dữ liệu thực nghiệm kiểm chứng từ 10 lần chạy lặp ngẫu nhiên (seed 0 đến 9), tuân thủ nguyên tắc khách quan, không dùng kết luận mang tính tuyệt đối hóa.

---

### Nhóm 1 — Performance (Hiệu năng tổng thể)
- **Mask mAP@50-95**: TSVM đạt trung bình **0.7246 ± 0.0078**, so với Baseline là **0.7210 ± 0.0129**. Chênh lệch thực nghiệm là **+0.0036 (+0.49%).**
- **Mask mAP@50**: TSVM đạt **0.9062 ± 0.0082**, Baseline đạt **0.9119 ± 0.0107** (chênh lệch **-0.0056, -0.62%**).
- **Kiểm định thống kê**: Phép kiểm Paired t-test cho thấy p-value của Mask mAP@50-95 là **0.3839** (p > 0.05). Do đó, mức tăng mAP trung bình (+0.0036) là một **chênh lệch thực nghiệm dương tính ở mức vừa phải**, chưa đạt ngưỡng ý nghĩa thống kê nghiêm ngặt α=0.05 để khẳng định có sự cách biệt mang tính xác định tuyệt đối về độ đo mAP đơn thuần.

### Nhóm 2 — Stability (Độ ổn định giữa các seed)
- **Độ co cụm phương sai (Variance Contraction)**: Độ lệch chuẩn của Mask mAP@50-95 giảm từ **0.0129** (Baseline) xuống **0.0078** (TSVM), tương ứng tỷ lệ phương sai giảm **2.75 lần**.
- **Biên độ dao động (Range = Max - Min)**: Baseline dao động từ 0.6941 đến 0.7366 (Range = **0.0425**), TSVM từ 0.7065 đến 0.7339 (Range = **0.0273**).
- **Đáy hiệu năng (Worst-case floor)**: Seed thấp nhất của TSVM là 0.7065 (seed 7), so với seed thấp nhất của Baseline là 0.6941 (seed 3). Điều này mô tả phân bố thực nghiệm giữa các seed; không dùng riêng thống kê này để khẳng định cơ chế nguyên nhân.

### Nhóm 3 — Precision/Recall Trade-off
- **Mask Precision**: Từ **0.9023 ± 0.0339** lên **0.9118 ± 0.0246** (+0.0095, +1.05%, p = 0.5428).
- **Mask Recall**: Từ **0.8584 ± 0.0252** lên **0.8625 ± 0.0173** (+0.0041, +0.48%).
- **Tương quan P vs R**: Biểu đồ phân tán (Chart 11) cho thấy biểu đồ P–R được dùng để mô tả phân bố thực nghiệm giữa hai mô hình, không suy diễn thêm về cơ chế.

### Nhóm 4 — Validation Loss
- **Validation Segmentation Loss**: Từ **1.3045 ± 0.0867** xuống **1.2424 ± 0.0387**. Mức thay đổi trung bình là **-0.0622 (-4.76%)**.
- **Ý nghĩa thống kê**: Phép kiểm định Paired t-test đạt **p = 0.0908**. Diễn giải ý nghĩa thống kê cần dựa trực tiếp trên ngưỡng α=0.05 để đánh giá mức độ hội tụ của hàm mục tiêu phân đoạn trên tập validation.

### Nhóm 5 — Confusion Matrix & Background Discrimination
Dựa trên ma trận nhầm lẫn trung bình 10 seed (127 polyp ground-truth, 40 ảnh nền âm tính):
- **True Positive (TP)**: TSVM đạt trung bình **111.2** (87.6%), so với Baseline **110.3** (86.9%).
- **False Negative (FN)**: TSVM giảm bỏ sót polyp xuống còn **15.8** (12.4%) so với Baseline **16.7** (13.1%).
- **False Positive (FP trên ảnh nền)**: TSVM có FP trung bình **14.6** (36.5%) so với Baseline **16.8** (42.0%). Chênh lệch trung bình là **-2.2** ca/lần chạy.
- **True Negative (TN trên ảnh nền)**: TSVM có TN trung bình **25.4** (63.5%) so với Baseline **23.2** (58.0%).
- **Nhận định**: Trong bộ dữ liệu kiểm tra này, TSVM có số FP trung bình thấp hơn Baseline. Kết quả này mô tả hiện tượng quan sát được; không đủ để riêng ma trận nhầm lẫn xác định nguyên nhân cơ chế.

### Nhóm 6 — Seed Consistency
- Cả hai mô hình đều có sự phụ thuộc nhất định vào random seed (đặc trưng cố hữu của huấn luyện Deep Learning trên tập dữ liệu y tế quy mô vừa).
- Tuy nhiên, TSVM thể hiện tính phụ thuộc thấp hơn: khoảng tin cậy của TSVM hẹp hơn, độ phân tán giữa các lần chạy giảm và đáy hiệu năng được nâng đỡ rõ rệt so với Baseline.

---

### Giới Hạn Nghiên Cứu Cần Nêu Trong Luận Văn
1. Tập kiểm tra gồm 160 ảnh từ một trung tâm nội soi (Kvasir-SEG). Cần kiểm thử thêm trên các tập đa trung tâm (CVC-ClinicDB, BKAI-IGH, ETIS-Larib) để đánh giá tính tổng quát hóa ngoại suy.
2. Dù Mask mAP@50-95 có mức chênh lệch (+0.49%) và Val Seg Loss giảm (-4.76%, p = 0.0908), mức chênh lệch mAP tổng thể vẫn ở mức vừa phải, đóng góp chính của TSVM nằm ở **nâng cao độ ổn định khởi tạo** và **giảm báo động giả (FP) trên ảnh nền**.
