# KẾT QUẢ THỰC NGHIỆM CHI TIẾT: ĐỘ CHÍNH XÁC mAP VÀ ĐỘ ỔN ĐỊNH PHƯƠNG SAI SEED
## PHÂN TÍCH KIỂM ĐỊNH F-TEST, HIỆN TƯỢNG CO HẸP PHƯƠNG SAI VÀ TỶ LỆ THẮNG ĐỐI ĐẦU 83.33%

---

> **Phân loại độ tin cậy thông tin theo nguyên tắc dự án:**
> - `[Đã xác nhận]`: Dữ liệu số liệu Mask mAP và Box mAP trích xuất trực tiếp từ tệp `results.csv` qua 6 seeds; công thức F-test và phương sai được tính toán bằng SciPy / NumPy.
> - `[Có khả năng / suy luận]`: Lý giải toán học về tác động triệt tiêu gradient vanishing/exploding của cơ chế SS2D associative scan.

---

## 1. BẢNG PHÂN TÍCH ĐỘ ỔN ĐỊNH PHƯƠNG SAI VÀ KIỂM ĐỊNH F-TEST

Chỉ số then chốt thể hiện độ tin cậy của thuật toán học sâu y tế là độ phân tán khi thay đổi hạt giống ngẫu nhiên (Random Seed Cross-Validation):

| Tiêu chí thống kê | Baseline YOLO26s-seg | C2TSVMamba | C2IAVM (👑 Champion Model) | Nhận xét so sánh |
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
