# Kết Luận Và Nhận Xét Khoa Học (Academic Conclusions)
## Đối sánh 10 Seed: YOLO26s-seg Baseline và YOLO26s-seg + TSVM

Tất cả các nhận xét dưới đây được xây dựng hoàn toàn dựa trên dữ liệu thực nghiệm kiểm chứng từ 10 lần chạy lặp ngẫu nhiên (seed 0 đến 9), tuân thủ nguyên tắc khách quan, không dùng kết luận mang tính tuyệt đối hóa.

---

### Nhóm 1 — Performance (Hiệu năng tổng thể)
- **Mask mAP@50-95**: TSVM đạt trung bình **0.7246 ± 0.0078**, so với Baseline là **0.7210 ± 0.0129**. Chênh lệch thực nghiệm là **+0.0036 (+0.50%)**.
- **Mask mAP@50**: TSVM đạt **0.9062 ± 0.0082**, Baseline đạt **0.9119 ± 0.0107** (chênh lệch **-0.0056, -0.62%**).
- **Kiểm định thống kê**: Phép kiểm Paired t-test cho thấy p-value của Mask mAP@50-95 là **0.3839** (p > 0.05). Do đó, mức tăng mAP trung bình (+0.0036) là một **chênh lệch thực nghiệm dương tính ở mức vừa phải**, chưa đạt ngưỡng ý nghĩa thống kê nghiêm ngặt α=0.05 để khẳng định có sự cách biệt mang tính xác định tuyệt đối về độ đo mAP đơn thuần.

### Nhóm 2 — Stability (Độ ổn định giữa các seed)
- **Độ co cụm phương sai (Variance Contraction)**: Độ lệch chuẩn của Mask mAP@50-95 giảm từ **0.0129** (Baseline) xuống **0.0078** (TSVM), tương ứng tỷ lệ phương sai giảm **2.75 lần**.
- **Biên độ dao động (Range = Max - Min)**: Baseline dao động từ 0.6941 đến 0.7366 (Range = **0.0425**), trong khi TSVM chỉ dao động từ 0.7065 đến 0.7339 (Range = **0.0274**, giảm 35.5%).
- **Đáy hiệu năng (Worst-case floor)**: Seed thấp nhất của TSVM là 0.7065 (seed 2), cao hơn đáng kể so với seed thấp nhất của Baseline là 0.6941 (seed 9). Điều này phản ánh cơ chế Topology-Shape aware giúp mô hình hạn chế hiện tượng sụt giảm hiệu năng nghiêm trọng khi gặp các cấu hình khởi tạo ngẫu nhiên bất lợi.

### Nhóm 3 — Precision/Recall Trade-off
- **Mask Precision**: Tăng từ **0.9023 ± 0.0339** lên **0.9118 ± 0.0246** (+0.0095, +1.05%, p = 0.5428). TSVM duy trì độ chính xác phát hiện cao hơn và ổn định hơn.
- **Mask Recall**: Tăng nhẹ từ **0.8584 ± 0.0252** lên **0.8625 ± 0.0173** (+0.0041, +0.48%).
- **Tương quan P vs R**: Biểu đồ phân tán (Chart 11) cho thấy đám mây điểm của TSVM tập trung chặt chẽ hơn về góc trên bên phải (vùng trade-off tối ưu), trong khi Baseline có các điểm phân tán rộng ra ngoài biên.

### Nhóm 4 — Validation Loss
- **Validation Segmentation Loss**: Giảm từ **1.3045 ± 0.0867** (Baseline) xuống **1.2424 ± 0.0387** (TSVM). Mức giảm trung bình là **-0.0622 (-4.76%)**.
- **Ý nghĩa thống kê**: Phép kiểm định Paired t-test đạt **p = 0.0908** (ở mức xu hướng cận ý nghĩa thống kê với α=0.10, nhưng chưa đạt ngưỡng nghiêm ngặt α=0.05). Mức giảm này thể hiện hàm mục tiêu phân đoạn của TSVM có xu hướng hội tụ ổn định và thấp hơn trên tập validation.

### Nhóm 5 — Confusion Matrix & Background Discrimination
Dựa trên ma trận nhầm lẫn trung bình 10 seed (127 polyp ground-truth, 40 ảnh nền âm tính):
- **True Positive (TP)**: TSVM đạt trung bình **111.2** (87.56%), cao hơn Baseline **110.3** (86.85%).
- **False Negative (FN)**: TSVM giảm bỏ sót polyp xuống còn **15.8** (12.44%) so với Baseline **16.7** (13.15%).
- **False Positive (FP trên ảnh nền)**: TSVM giảm số dự đoán dương tính giả xuống **14.6** (36.50%) so với Baseline là **17.4** (43.50%). Số ca FP trung bình giảm **2.8 ca/lần chạy** (giảm 16.1% lượng dự đoán sai trên ảnh nền).
- **True Negative (TN trên ảnh nền)**: TSVM nhận diện đúng vùng nền đạt **25.4** (63.50%) so với Baseline **22.6** (56.50%).
- **Nhận định**: Cải tiến cấu trúc không gian hình thái (Topology-Shape) giúp mạng phân biệt tốt hơn giữa nếp gấp niêm mạc đại tràng thông thường và tổn thương polyp thật, dẫn đến giảm đáng kể cảnh báo giả trên ảnh nền.

### Nhóm 6 — Seed Consistency
- Cả hai mô hình đều có sự phụ thuộc nhất định vào random seed (đặc trưng cố hữu của huấn luyện Deep Learning trên tập dữ liệu y tế quy mô vừa).
- Tuy nhiên, TSVM thể hiện tính phụ thuộc thấp hơn: khoảng tin cậy của TSVM hẹp hơn, độ phân tán giữa các lần chạy giảm và đáy hiệu năng được nâng đỡ rõ rệt so với Baseline.

---

### Giới Hạn Nghiên Cứu Cần Nêu Trong Luận Văn
1. Tập kiểm tra gồm 160 ảnh từ một trung tâm nội soi (Kvasir-SEG). Cần kiểm thử thêm trên các tập đa trung tâm (CVC-ClinicDB, BKAI-IGH, ETIS-Larib) để đánh giá tính tổng quát hóa ngoại suy.
2. Dù mAP@50-95 tăng nhẹ (+0.49%) và Val Seg Loss giảm (-4.76%, p=0.0908), các phép kiểm định t-test đều có p > 0.05. Do đó không kết luận tuyệt đối mà trình bày đúng bản chất: đóng góp chính của TSVM nằm ở **nâng cao độ ổn định hạt ngẫu nhiên (thu hẹp phương sai 2.75 lần)** và **cải thiện độ đặc hiệu nhận diện ảnh nền (giảm 16.1% FP)**.
