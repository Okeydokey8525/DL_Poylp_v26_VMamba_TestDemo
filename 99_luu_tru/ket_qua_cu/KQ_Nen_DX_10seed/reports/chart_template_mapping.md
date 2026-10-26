# BẢNG ÁNH XẠ VÀ KẾ THỪA TEMPLATE BIỂU ĐỒ (CHART TEMPLATE MAPPING)
## Chuyển giao Thiết kế Đồ họa từ `KQ_DoiXung` sang Bộ Dữ liệu 10-Seed (`KQ_Nen_DX_10seed`)

**Ngày lập**: 27/09/2026  
**Mục tiêu**: Kế thừa ngôn ngữ thị giác (Visual Style/Template) từ `KQ_DoiXung` (layout, palette màu, typography, error bar, subtitle, grid) và áp dụng trung thực lên **dữ liệu thực nghiệm 10 seed của 2 mô hình đối đầu trực diện** (Baseline YOLO26s-seg và TSVM Topology-Shape).  
**Nguyên tắc**: *Reuse visual design, NOT old data. Không bịa số. Không sửa raw data. Không retrain.*

---

### 1. Bảng Ánh xạ Chi tiết Từng Biểu đồ

| Tên Tệp Biểu đồ trong `figures/` | Template Nguồn trong `KQ_DoiXung/` | Những Cải tiến & Điều chỉnh để Phù hợp 10-Seed (2 Mô hình) | Trạng thái |
| :--- | :--- | :--- | :---: |
| **`01_overall_benchmark_barchart.png`** | `Base vs TSVM_BG20/01_.../01_overall_benchmark_barchart.png` | Chuẩn hóa so sánh 2 mô hình (Baseline vs TSVM) trên 10 seed; hiển thị Mean ± 1 Std chính xác với nhãn số khoa học, không đè chữ | **Hoàn thành** |
| **`02_val_seg_loss_barchart.png`** | `Base vs TSVM_BG20/01_.../02_val_seg_loss_barchart.png` | Hiển thị Validation Seg Loss của 2 mô hình; tính toán $\Delta$ và % chênh lệch đối chiếu so với Baseline (-1.10% loss mean, -40.6% std) | **Hoàn thành** |
| **`03_seed_by_seed_barchart.png`** | `Base vs TSVM_BG20/01_.../03_seed_by_seed_barchart.png` | Mở rộng từ 6 seed (`s0`–`s5`) lên **đủ 10 seed (`s0`–`s9`)**; nhóm 2 cột mô hình cho từng seed trực quan | **Hoàn thành** |
| **`04_convergence_loss_curves.png`** | `Base vs TSVM_BG20/01_.../04_convergence_loss_curves.png` | Lưới đồ thị 2x2 cho 4 hàm mất mát (val/seg, train/seg, val/box, val/cls) suốt 100 epochs, dải mờ bao phủ $\pm 1\text{ Std}$ của 10 seed giữa Baseline và TSVM | **Hoàn thành** |
| **`05_metric_curves_mAP.png`** | `Base vs TSVM_BG20/01_.../05_metric_curves_mAP.png` | Đồ thị 1x2 theo dõi tiến trình Mask mAP@50-95 và Mask mAP@50 qua 100 epochs với dải độ lệch chuẩn 10 seed giữa Baseline và TSVM | **Hoàn thành** |
| **`07b_pie_head_to_head_winrate.png`** | `Base vs TSVM_BG20/01_.../07b_pie_head_to_head_winrate.png` | Donut chart biểu diễn tỷ lệ thắng đối đầu trực diện giữa Baseline và TSVM (6/10 seed TSVM thắng, 4/10 seed Baseline thắng) | **Hoàn thành** |
| **`09_metric_stability_band_area.png`** | `Base vs TSVM_BG20/01_.../09_metric_stability_band_area.png` | Biểu đồ dải bao phủ cực trị [Min, Max] kết hợp đường trung bình Mean của 10 seed Baseline vs TSVM | **Hoàn thành** |
| **`10_radar_multiobjective_tradeoff.png`** | `Base vs TSVM_BG20/01_.../10_radar_multiobjective_tradeoff.png` | Biểu đồ Radar đối xứng 8 trục so sánh các chỉ số kết quả thực tế qua 10 seed: Nửa bên trái là Box Detection (Box mAP@50-95, Box mAP@50, Box P, Box R), nửa bên phải là Mask Segmentation (Mask mAP@50-95, Mask mAP@50, Mask P, Mask R) | **Hoàn thành** |
| **`11_boxplot_variance_stability.png`** | `Base vs TSVM_BG20/01_.../11_boxplot_variance_stability.png` | Boxplot kết hợp các điểm phân tán jitter scatter points của 10 seed chuyên biệt cho Mask mAP@50-95 (đã tinh gọn bỏ subplot Loss), tập trung kiểm chứng tính ổn định hạt giống và co hẹp phương sai | **Hoàn thành** |
| **`12_confusion_matrix_mean_comparison.png`** | `Base vs TSVM_BG20/01_.../12_confusion_matrix_mean_comparison.png` | Ma trận nhầm lẫn chuẩn hóa trung bình 10 seed trên **160 ảnh kiểm định** (120 ảnh chứa polyp với $TP+FN=127$ thực thể, 40 ảnh nền với $FP+TN=40$) đối đầu Baseline vs TSVM. ⚠️ Ô TN là số tái dựng $40-FP$, không phải số đo của Ultralytics | **Hoàn thành (có giới hạn)** |
| **`13_confusion_matrix_diff_heatmap.png`** | `Base vs TSVM_BG20/01_.../13_confusion_matrix_diff_heatmap.png` | Heatmap chênh lệch hiệu số chuẩn hóa (TSVM - Baseline) với bảng màu `RdBu_r` | **Hoàn thành** |
| **`14_confusion_cells_grouped_barchart.png`** | `Base vs TSVM_BG20/01_.../14_confusion_cells_grouped_barchart.png` | Biểu đồ cột nhóm so sánh số lượng trung bình các ô TP, FN, FP, TN kèm thanh sai số $\pm 1\text{ Std}$ giữa 2 mô hình | **Hoàn thành** |

---

### 2. Danh mục Biểu đồ Cũ trong `KQ_Nen_DX_10seed` Được Giữ Nguyên

Toàn bộ 20 biểu đồ ban đầu trong các thư mục con chuyên biệt của `KQ_Nen_DX_10seed/` được **giữ nguyên vẹn 100%**:
- `01_summary/`: `fig01_overall_mAP_comparison.png`, `fig02_multimetric_comparison.png`, `fig03_box_vs_mask_mAP.png`.
- `02_distributions/`: `fig04_distribution_comparison.png`, `fig05_metric_violin_plots.png`, `fig06_validation_loss_distribution.png`.
- `03_seed_by_seed/`: `fig07_seed_comparison_bar.png`, `fig08_paired_differences.png`, `fig09_head_to_head_scatter.png`, `fig10_seed_rankings.png`, `fig11_parallel_coordinates.png`, `fig12_performance_gap_lollipop.png`.
- `04_confusion_matrix/`: `fig13_confusion_matrix_raw.png`, `fig14_confusion_matrix_comparison.png`, `fig15_detection_metrics_rates.png`, `fig16_error_distribution.png`.
- `05_multimetric/`: `fig17_multimetric_radar.png`, `fig18_precision_recall_balance.png`, `fig19_best_epoch_vs_mAP.png`, `fig20_statistical_summary_card.png`.

---

### 3. Danh mục Chart Bị Loại Trừ và Lý do Khoa học

| Tên Chart Bị Loại Trừ | Folder Template Nguồn | Lý do Loại trừ (Không thể chuyển giao) |
| :--- | :--- | :--- |
| **Toàn bộ folder `02_Ghep_DoiXung_TungSeed/`** | `Base vs TSVM_BG20/02_.../` | Tuân thủ ngoại lệ chỉ thị: chất lượng ghép đối xứng không đạt chuẩn, không tái sử dụng. |
| **`07a_pie_clinical_breakdown.png`** | `Base vs TSVM_BG20/01_.../` | Dạng biểu đồ tròn 2 phần (Recall vs Bỏ sót) trùng lặp thông tin với biểu đồ cột ma trận nhầm lẫn (fig14) và không thể hiện được thanh sai số $\pm\text{Std}$ khoa học. |
| **`08_cumulative_loss_area_chart.png`** | `Base vs TSVM_BG20/01_.../` | Biểu đồ diện tích tích lũy loss (cumulative loss) không phản ánh quy luật hội tụ gradient của mạng nơ-ron; loss qua các epoch là biến trạng thái tức thời chứ không phải đại lượng tích lũy vật lý. |
| **`15a, 15b, 15c` (Phân rã độ trễ 4 giai đoạn)** | `Base vs TSVM_BG20/01_.../` | Thí nghiệm phân rã thời gian trễ từng module phần cứng (Pre, Backbone, Mask Head, NMS) thuộc phạm vi của báo cáo riêng trong `efficiency_benchmark/`, tránh nhồi nhét vào thư mục 10-seed accuracy. |

---

### 4. Cam kết Kiểm toán

1. **Tuyệt đối không sử dụng dữ liệu cũ của 6-seed**: Toàn bộ các đường cong loss qua 100 epoch và các điểm số metric đều được trích xuất trực tiếp từ 40 tệp `results.csv` thực tế trong `archive/KetQua_Nen/`.
2. **Không sửa đổi dữ liệu gốc**: Dữ liệu thô và các tệp báo cáo cũ không bị can thiệp.
3. **Mọi biểu đồ sinh ra đều đạt độ phân giải in ấn 300 DPI** với tỷ lệ trục và nhãn chú thích rõ ràng.
