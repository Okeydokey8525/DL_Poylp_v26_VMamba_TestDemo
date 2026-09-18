# BỘ BIỂU ĐỒ SO SÁNH ĐỐI CHỨNG TOÀN DIỆN: BASELINE YOLO26s-seg VS C2IAVM (CHAMPION MODEL)
**Đề tài Khóa luận Cử nhân CNTT (CNTT_KLCN182) - Trường Đại học Công Thương TP.HCM (HUIT)**
**Nhóm sinh viên thực hiện:** Lê Đức Lương, Phùng Tuấn Huy, Trần Mạnh Toàn
**Giảng viên hướng dẫn:** ThS. Phùng Thế Bảo (`baopt@huit.edu.vn`)

---

## 1. TỔNG QUAN VÀ Ý NGHĨA KHOA HỌC
Thư mục này chứa toàn bộ các dạng biểu đồ trực quan hóa số liệu thực nghiệm khoa học, so sánh đối chuẩn giữa:
1. **Mô hình gốc (Baseline):** `Baseline YOLO26s-seg` chuẩn Ultralytics.
2. **Mô hình đề xuất (Champion):** `IAVM` (`C2IAVM - Interactive Attention-VMamba Fusion`) tích hợp cơ chế song song hóa Không gian - Kênh (Bi-SS2D + Multi-Head Self-Attention).

Tất cả các số liệu đều được tính toán chuẩn hóa trên **6-Fold Cross-Validation độc lập (Seeds `s0` đến `s5`)**, huấn luyện đủ **100 epochs/seed** với dải phương sai $\pm 1\text{ Std}$ và độ phân giải xuất bản **300 DPI**.

---

## 2. BẢNG TỔNG HỢP SỐ LIỆU ĐỐI CHUẨN (6 SEED MEAN $\pm$ STD)

| Nhóm Chỉ Số | Tên Chỉ Số | Baseline YOLO26s-seg | C2IAVM (IAVM - Ours) | Độ Lệch ($\Delta$) | Tỷ Lệ Thắng (Win Rate) | Giảm Phương Sai |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Phân đoạn (Mask)** | **Mask mAP@50-95** | $0.7291 \pm 0.0153$ | **$0.7361 \pm 0.0073$** | **$+0.0070$ (+0.70%)** | **5/6 seeds (83.33%)** | **$4.39\times$ (F-test)** |
| Phân đoạn (Mask) | Mask mAP@50 | $0.9144 \pm 0.0065$ | **$0.9149 \pm 0.0109$** | $+0.0005$ (+0.05%) | 3/6 seeds (50.00%) | Đạt đỉnh 93.19% ở s0 |
| Phân đoạn (Mask) | **Mask Recall (Độ nhạy)** | $0.8760 \pm 0.0175$ | **$0.8875 \pm 0.0195$** | **$+0.0115$ (+1.15%)** | **5/6 seeds (83.33%)** | Phát hiện 112.7/127 polyp |
| Phân đoạn (Mask) | Mask Precision | **$0.9198 \pm 0.0139$** | $0.8876 \pm 0.0275$ | $-0.0322$ (-3.22%) | Đánh đổi vì Recall | Giảm rủi ro sót polyp |
| Phân đoạn (Mask) | Mask F1-Score | $0.8972 \pm 0.0054$ | $0.8871 \pm 0.0090$ | $-0.0101$ (-1.01%) | Cân bằng P-R cao | Duy trì sát mốc 89% |
| **Định vị (Box)** | **Box mAP@50-95** | $0.7404 \pm 0.0112$ | **$0.7418 \pm 0.0057$** | **$+0.0014$ (+0.14%)** | **4/6 seeds (66.67%)** | **$3.86\times$** |
| Định vị (Box) | Box mAP@50 | $0.9099 \pm 0.0068$ | **$0.9151 \pm 0.0086$** | $+0.0052$ (+0.52%) | **5/6 seeds (83.33%)** | Bao phủ khung vượt trội |
| Định vị (Box) | Box Recall | $0.8664 \pm 0.0246$ | **$0.8842 \pm 0.0185$** | **$+0.0178$ (+1.78%)** | **5/6 seeds (83.33%)** | Phát hiện vùng tổn thương |
| **Hàm Phạt (Loss)** | **Val Seg Loss** | $1.4314 \pm 0.0540$ | **$1.3987 \pm 0.0695$** | **$-0.0327$ (Giảm lỗi)**| **4/6 seeds (66.67%)** | Nghiệm tối ưu sâu hơn |
| Hàm Phạt (Loss) | Val Box Loss | $0.7503 \pm 0.0137$ | $0.7571 \pm 0.0276$ | $+0.0068$ | Tương đương | Duy trì chất lượng khung |
| Hàm Phạt (Loss) | Val Cls Loss | $0.5681 \pm 0.0400$ | $0.5902 \pm 0.0524$ | $+0.0221$ | Ổn định | Phân loại 1-class polyp |

---

## 3. DANH MỤC CÁC DẠNG BIỂU ĐỒ ĐÃ TẠO

### Nhóm 1: Biểu đồ cột (Bar Charts) có vạch sai số $\pm 1\text{ Std}$
1. `04_overall_benchmark_barchart.png`: Biểu đồ cột so sánh tổng thể tất cả các chỉ số Mask mAP, Box mAP, Recall, Precision, F1 giữa Baseline và IAVM kèm thanh sai số $\pm$ độ lệch chuẩn.
2. `05_fold_by_fold_comparison.png`: Biểu đồ cột so sánh từng seed độc lập (s0 đến s5) cho Mask mAP@50-95 và Validation Seg Loss, minh chứng tỷ lệ thắng áp đảo **83.33% (5/6 seed)** của IAVM.
3. `05b_fold_by_fold_recall.png`: Biểu đồ cột so sánh độ nhạy (Mask Recall) qua từng seed, làm rõ khả năng bao phủ tổn thương polyp.
4. `01a_val_seg_loss_barchart.png` & `val_losses_barchart.png`: Biểu đồ cột so sánh các hàm mất mát (Seg Loss, Box Loss, Cls Loss) tại điểm cực trị.
5. `05c_computational_resources_barchart.png`: Biểu đồ cột chi phí tính toán (Thời gian huấn luyện 1.91h vs 3.05h, VRAM tiêu thụ 6.42GB vs 7.19GB, Tham số 11.77M vs 12.14M, GFLOPs 39.4 vs 40.8).

### Nhóm 2: Biểu đồ tròn & Donut (Pie & Donut Charts)
1. `07a_pie_polyp_clinical_breakdown.png`: Biểu đồ Donut thể hiện ý nghĩa y khoa lâm sàng: Tỷ lệ phát hiện đúng (True Positive) vs Bỏ sót (False Negative) trên tổng số 127 polyp của tập kiểm thử. C2IAVM giảm tỷ lệ bỏ sót xuống còn **11.25% (14.3 polyp)** so với **12.40% (15.7 polyp)** của Baseline.
2. `07b_pie_head_to_head_winrate.png`: Biểu đồ Donut thể hiện tỷ lệ thắng đối đầu trực tiếp trên 6 seeds (IAVM thắng 5/6 = 83.33%, Baseline thắng 1/6 = 16.67%).
3. `07c_pie_inference_latency_breakdown.png`: Biểu đồ Donut phân tích các pha trễ suy luận (Tiền xử lý 1.8ms, Model 20.9ms, NMS 2.3ms). Tổng thời gian đạt **25.0 ms/frame (~40.0 FPS)**, vượt xa ngưỡng yêu cầu y tế thời gian thực (**>30 FPS**).

### Nhóm 3: Biểu đồ Radar / Mạng nhện (Spider Chart)
1. `06_radar_chart_tradeoff.png`: Đánh giá đa chiều trên 8 trục chuẩn hóa (Mask mAP50-95, Mask mAP50, Mask Recall, Box mAP50-95, Box Recall, Độ ổn định 1/Std, Tối ưu hóa hàm phạt 1/Loss, Tốc độ thời gian thực). Cho thấy sự toàn diện vượt bậc của C2IAVM.

### Nhóm 4: Biểu đồ Hộp phân bố phương sai (Box & Whisker Plots)
1. `08_boxplot_variance_comparison.png`: Biểu đồ hộp thể hiện phân bố giá trị qua 6 folds. Minh chứng trực quan cho hiện tượng co hẹp phương sai: khoảng biến thiên của IAVM hẹp hơn gấp 2 lần, không có hiện tượng suy biến seed như Baseline.

### Nhóm 5: Đường cong hội tụ 100 Epochs (4-in-1 Grids với dải bóng mờ $\pm 1\text{ Std}$)
1. `01_loss_curves_comparison.png`: Lưới 4 biểu đồ hàm phạt (Val Seg Loss, Train Seg Loss, Val Box Loss, Val Cls Loss).
2. `02_metric_curves_mAP_comparison.png`: Lưới 4 biểu đồ độ chính xác mAP (Mask mAP50-95, Mask mAP50, Box mAP50-95, Box mAP50).
3. `03_precision_recall_dynamics.png`: Lưới 4 biểu đồ động học hội tụ Precision & Recall (Mask & Box).

### Nhóm 6: Các biểu đồ đơn lẻ (Single-Metric Standalone Curves)
- `01a_val_seg_loss_comparison.png` & `val_seg_loss_comparison.png`
- `01a_val_seg_loss_comparison_zoomed.png` & `val_seg_loss_comparison_zoomed.png` (Tập trung dải epoch 10-100)
- `01b_train_seg_loss_comparison.png` & `train_seg_loss_comparison.png`
- `01c_val_box_loss_comparison.png` & `val_box_loss_comparison.png`
- `01d_val_cls_loss_comparison.png` & `val_cls_loss_comparison.png`
- `02a_mask_map50_95_comparison.png` & `mask_map50_95_comparison.png`
- `02b_mask_map50_comparison.png` & `mask_map50_comparison.png`
- `02c_box_map50_95_comparison.png` & `box_map50_95_comparison.png`
- `02d_box_map50_comparison.png` & `box_map50_comparison.png`
- `03a_mask_precision_comparison.png` & `mask_precision_comparison.png`
- `03b_mask_recall_comparison.png` & `mask_recall_comparison.png`
- `03c_box_precision_comparison.png` & `box_precision_comparison.png`
- `03d_box_recall_comparison.png` & `box_recall_comparison.png`

### Nhóm 7: Đối chiếu trực quan & Ma trận nhầm lẫn
1. `07_qualitative_prediction_comparison.png`: So sánh trực quan 3 ảnh cạnh nhau (Ground Truth vs Baseline vs IAVM) trên batch kiểm thử.
2. `08_confusion_matrix_side_by_side.png`: Ma trận nhầm lẫn chuẩn hóa giữa hai mô hình tại seed 0.
3. `09_mask_pr_curve_side_by_side.png`: Đường cong Precision-Recall phân đoạn đối chiếu tại seed 0.

---

## 4. HƯỚNG DẪN CHÈN VÀO KHÓA LUẬN & BÁO CÁO (THESIS EMBEDDING GUIDELINES)

1. **Chương 4 - Đánh giá Kết quả Thực nghiệm:**
   - Sử dụng `04_overall_benchmark_barchart.png` làm Hình tổng kết hiệu năng chung.
   - Sử dụng `05_fold_by_fold_comparison.png` và `08_boxplot_variance_comparison.png` để phân tích độ tin cậy và kiểm định phương sai ($F = 4.39$).
   - Sử dụng `07a_pie_polyp_clinical_breakdown.png` trong phần **Thảo luận ý nghĩa y khoa (Clinical Implications)** để chứng minh việc tăng Recall giảm thiểu số ca polyp bị bỏ sót trong nội soi thực tế.
2. **Slide Báo cáo Bảo vệ Khóa luận:**
   - Trượt 1 (Hiệu năng): Chèn `07b_pie_head_to_head_winrate.png` (83.33% Win Rate) và `06_radar_chart_tradeoff.png`.
   - Trượt 2 (Chất lượng phân đoạn): Chèn `07_qualitative_prediction_comparison.png` để chứng minh trực quan bằng mắt cho Hội đồng.
   - Trượt 3 (Độ khả thi triển khai): Chèn `07c_pie_inference_latency_breakdown.png` (>40 FPS đáp ứng thời gian thực).
