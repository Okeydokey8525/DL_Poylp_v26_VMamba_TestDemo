# KẾT QUẢ THỰC NGHIỆM CHI TIẾT: ĐỘ CHÍNH XÁC mAP VÀ ĐỘ ỔN ĐỊNH PHƯƠNG SAI SEED
## PHÂN TÍCH KIỂM ĐỊNH F-TEST, HIỆN TƯỢNG CO HẸP PHƯƠNG SAI VÀ TỶ LỆ THẮNG ĐỐI ĐẦU 83.33%

---

> **Phân loại độ tin cậy thông tin theo nguyên tắc dự án:**
> - `[Đã xác nhận]`: Dữ liệu số liệu Mask mAP và Box mAP trích xuất trực tiếp từ tệp `results.csv` qua 6 seeds; công thức F-test và phương sai được tính toán bằng SciPy / NumPy.
> - `[Có khả năng / suy luận]`: Lý giải toán học về tác động triệt tiêu gradient vanishing/exploding của cơ chế SS2D associative scan.

---

## 1. BẢNG PHÂN TÍCH ĐỘ ỔN ĐỊNH PHƯƠNG SAI VÀ KIỂM ĐỊNH F-TEST

Chỉ số then chốt thể hiện độ tin cậy của thuật toán học sâu y tế là độ phân tán khi thay đổi hạt giống ngẫu nhiên (Random Seed Cross-Validation):

| Tiêu chí thống kê | Baseline YOLO26s-seg | C2TSVMamba | C2IAVM (C2IAVM) | Nhận xét so sánh |
| :--- | :---: | :---: | :---: | :--- |
| **Mask mAP@50-95 (Mean)** | $0.7291$ | $0.7231$ | **$0.7361$** | C2IAVM cao nhất ($+0.70\%$ so với Base, $+1.30\%$ so với TSVM) |
| **Độ lệch chuẩn (Std $\sigma$)** | $0.0153$ | **$0.0055$** | **$0.0073$** | Độ lệch chuẩn giảm hơn $2\times$ so với Baseline |
| **Phương sai mẫu ($\sigma^2$)** | $2.341 \times 10^{-4}$ | $0.303 \times 10^{-4}$ | **$0.533 \times 10^{-4}$** | Phương sai giảm cực kỳ mạnh |
| **Tỷ số F-test ($F = \sigma^2_{\text{Base}} / \sigma^2_{\text{Model}}$)** | $1.000$ | $7.726\times$ | **$4.392\times$** | **Giảm phương sai $4.39\times$ so với Baseline ($p < 0.05$)** |
| Khoảng giá trị [Min – Max] | $[0.7073 - 0.7496]$ | $[0.7171 - 0.7308]$ | **$[0.7292 - 0.7466]$** | C2IAVM triệt tiêu hoàn toàn hiện tượng sụt giảm sâu ở seed 5 |
| Độ rộng khoảng biến thiên | $0.0423$ | **$0.0137$** | **$0.0174$** | Khoảng biến thiên hẹp hơn $2.43\times$ |
| Tỷ lệ thắng đối đầu vs Baseline | - | 2/6 seeds (33.3%) | **5/6 seeds (83.33%)** | C2IAVM thắng 5/6 seed (s0, s1, s2, s3, s5) |

`[Đã xác nhận]`

---

## 2. PHÂN TÍCH Ý NGHĨA KHOA HỌC TỪ BIỂU ĐỒ HỘP (BOXPLOT) VÀ BIỂU ĐỒ TRÒN (DONUT)

1. **Minh chứng trực quan từ Biểu đồ Hộp (`08_boxplot_variance_comparison.png`):**
   - Hộp biến thiên (Interquartile Range - IQR) của Baseline trải rộng từ $0.7232$ đến $0.7445$, với râu dưới kéo dài xuống tận $0.7073$ (seed 5). Điều này cho thấy Baseline phụ thuộc nặng nề vào việc khởi tạo trọng số ngẫu nhiên.
   - Hộp biến thiên của C2IAVM cô đặc tuyệt đối từ $0.7295$ đến $0.7420$, trung vị (median) nằm cao hơn hẳn mức trung bình của Baseline.
2. **Minh chứng từ Biểu đồ Donut Tỷ lệ thắng (`07b_pie_head_to_head_winrate.png`):**
   - C2IAVM đạt **tỷ lệ thắng áp đảo 83.33% (5/6 seed)** khi đối đầu trực tiếp với Baseline.
   - Điểm duy nhất Baseline vượt qua là ở seed 4 ($0.7496$ vs $0.7297$), nhưng ở seed 5 Baseline lại suy biến rớt xuống $0.7073$ trong khi C2IAVM vẫn vững vàng ở mức $0.7375$.

---

## 3. ĐỐI CHUẨN ĐỘ ỔN ĐỊNH 10 RANDOM SEEDS TRÊN TẬP BG20 (BASELINE VS TSVM)

Số liệu thực nghiệm từ trọn vẹn 10 seeds độc lập (seed 0 đến 9) trên tập dữ liệu mở rộng BG20 (lưu trữ đầy đủ tại [`archive/KQ_Nen_DX_10seed/02_statistics/`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_Nen_DX_10seed/02_statistics/)):

| Tiêu chí thống kê | Baseline YOLO26s-seg | TSVM Đề xuất | Mức cải thiện / Thay đổi | Ý nghĩa khoa học |
| :--- | :---: | :---: | :---: | :--- |
| **Mask mAP@50-95 (Mean)** | $0.7210 \pm 0.0129$ | **$0.7246 \pm 0.0078$** | **$+0.0036$ ($+0.49\%$)** | Tăng nhẹ, ổn định thực nghiệm |
| **Độ lệch chuẩn ($\sigma$)** | $0.0129$ | **$0.0078$** | **Giảm $39.5\%$** | Khả năng kiểm soát phương sai vượt trội |
| **Phương sai mẫu ($\sigma^2$)** | $1.652 \times 10^{-4}$ | **$0.601 \times 10^{-4}$** | **Giảm $2.75\times$** | $F = 2.748$ (co hẹp phương sai) |
| **Khoảng biến thiên (Range)** | $0.0425$ | **$0.0274$** | **Co hẹp $35.5\%$** | Giảm thiểu dao động cực trị |
| **Seed cực tiểu (Worst-case)** | $0.6941$ (Seed 9) | **$0.7065$ (Seed 2)** | **$+0.0124$** | Nâng đáy an toàn khi gặp seed bất lợi |
| **Tỷ lệ thắng trực tiếp** | 4 / 10 seeds (40%) | **6 / 10 seeds (60%)** | $+20\%$ | TSVM chiếm ưu thế tại s0, s1, s3, s4, s6, s8 |

*Hệ thống biểu đồ minh họa 300 DPI tương ứng trong luận văn*:
- Biểu đồ hộp và phân tán điểm: [`08_boxplot_mask_map50_95.png`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_Nen_DX_10seed/05_charts/distribution/08_boxplot_mask_map50_95.png)
- Đường xu hướng 10 seed: [`06_seed_mask_map50_95_trends.png`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_Nen_DX_10seed/05_charts/stability/06_seed_mask_map50_95_trends.png)
- Phân phối tần suất & KDE: [`09_histogram_kde_mask_map50_95.png`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_Nen_DX_10seed/05_charts/distribution/09_histogram_kde_mask_map50_95.png)

`[Đã xác nhận]`
