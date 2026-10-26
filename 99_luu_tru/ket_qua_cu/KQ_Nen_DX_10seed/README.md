# Kết Quả Thực Nghiệm Đối Sánh 10 Seed: YOLO26s-seg Baseline vs YOLO26s-seg + TSVM
## Thư mục: `KQ_Nen_DX_10seed`

Tài liệu và bộ dữ liệu này phục vụ viết báo cáo chuyên đề / luận văn tốt nghiệp, cung cấp đầy đủ số liệu thống kê mô tả, kiểm định thống kê và hệ thống biểu đồ đạt chuẩn xuất bản (300 DPI).

---

## 1. Nguồn Dữ Liệu Thực Nghiệm
- **Tập dữ liệu**: Kvasir-SEG cấu hình kèm 20% ảnh nền âm tính (`data_bg20.yaml`).
  - Tập Validation: 160 ảnh (120 ảnh chứa polyp với 127 bounding box / mask ground-truth; 40 ảnh `normal-cecum` không có polyp).
- **Baseline Model**: YOLO26s-seg chuẩn (`yolo26s-seg.pt`).
  - Nguồn kết quả: `KetQua_Nen/YOLOv26s-seg/Kvasir_BG20_Baseline_YOLO26s_seg_s{0..9}_w2/results.csv`
- **TSVM Model**: YOLO26s-seg tích hợp nhánh nhận thức hình thái và topo (`yolo26s-seg-TopologyShapeVMamba.yaml`).
  - Nguồn kết quả: `KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/Kvasir_BG20_YOLO26s_seg_TSVM_s{0..9}_w2/results.csv`
- **Số lượng seed**: 10 random seeds độc lập (seed 0 đến 9) cho mỗi mô hình (tổng cộng 20 lần chạy thực nghiệm hoàn chỉnh, 100 epochs/run).
- **Nguyên tắc trích xuất**: Metric được ghi nhận tại epoch tối ưu (`best.pt`) dựa trên `metrics/mAP50-95(M)`.

---

## 2. Cấu Trúc Thư Mục Kết Quả

```text
KQ_Nen_DX_10seed/
├── 01_raw_analysis/
│   ├── raw_10seeds_extracted_metrics.csv       # 20 dòng số liệu trích xuất trực tiếp từ results.csv
│   └── raw_10seeds_confusion_matrices.csv      # Bảng 20 ma trận nhầm lẫn thực nghiệm
├── 02_statistics/
│   ├── mean_std/
│   │   └── full_comparison_mean_std.csv        # Bảng tổng hợp Mean ± Std, Delta, % thay đổi, p-value
│   ├── min_max/
│   │   └── metrics_min_max_range.csv           # Bảng Min, Max, Median, Range và seed cực trị
│   └── seed_comparison/
│       ├── seed_by_seed_metrics_and_deltas.csv # Chi tiết từng seed và delta tương ứng
│       └── seed_win_loss_summary.csv           # Tỷ lệ số seed TSVM thắng / Baseline thắng
├── 03_metrics/
│   ├── segmentation/
│   │   └── segmentation_metrics_summary.csv    # Phân tích sâu các metric Mask (mAP50-95, mAP50, P, R)
│   ├── bounding_box/
│   │   └── bounding_box_metrics_summary.csv    # Phân tích sâu các metric Box
│   └── loss/
│       └── validation_loss_metrics_summary.csv # Phân tích sâu validation loss (seg, box, cls, dfl)
├── 04_confusion_matrix/
│   ├── count/
│   │   ├── baseline_cm_count_per_seed.csv      # Số đếm TP, FN, FP, TN từng seed Baseline
│   │   ├── tsvm_cm_count_per_seed.csv          # Số đếm TP, FN, FP, TN từng seed TSVM
│   │   ├── baseline_cm_mean_count.csv          # Ma trận 2x2 đếm trung bình Baseline
│   │   ├── tsvm_cm_mean_count.csv              # Ma trận 2x2 đếm trung bình TSVM
│   │   ├── 14_cm_count_baseline_mean.png       # Heatmap ma trận đếm Baseline (300 DPI)
│   │   └── 15_cm_count_tsvm_mean.png           # Heatmap ma trận đếm TSVM (300 DPI)
│   └── percentage/
│       ├── baseline_cm_percentage_per_seed.csv # Tỷ lệ % từng seed Baseline
│       ├── tsvm_cm_percentage_per_seed.csv     # Tỷ lệ % từng seed TSVM
│       ├── baseline_cm_mean_percentage.csv     # Ma trận % chuẩn hóa trung bình Baseline
│       ├── tsvm_cm_mean_percentage.csv         # Ma trận % chuẩn hóa trung bình TSVM
│       ├── 16_cm_percentage_baseline_mean.png  # Heatmap ma trận % Baseline (300 DPI)
│       └── 17_cm_percentage_tsvm_mean.png      # Heatmap ma trận % TSVM (300 DPI)
├── 05_charts/
│   ├── performance/
│   │   ├── 01_mask_map50_95_comparison.png     # So sánh Mean ± Std Mask mAP@50-95
│   │   ├── 02_mask_map50_comparison.png        # So sánh Mean ± Std Mask mAP@50
│   │   ├── 03_precision_recall_comparison.png  # So sánh Mask Precision và Recall
│   │   ├── 04_box_metrics_comparison.png       # So sánh 4 chỉ số Bounding Box
│   │   └── 05_val_seg_loss_comparison.png      # So sánh Validation Segmentation Loss
│   ├── stability/
│   │   ├── 06_seed_mask_map50_95_trends.png    # Đường xu hướng 10 seed Mask mAP@50-95
│   │   ├── 07_seed_box_map50_95_trends.png     # Đường xu hướng 10 seed Box mAP@50-95
│   │   └── 10_mean_std_errorbars.png           # Biểu đồ thanh sai số Mean ± Std đa chỉ số
│   ├── distribution/
│   │   ├── 08_boxplot_mask_map50_95.png        # Boxplot kèm điểm dữ liệu phân tán
│   │   └── 09_histogram_kde_mask_map50_95.png  # Histogram và đường mật độ xác suất KDE
│   ├── correlation/
│   │   ├── 11_scatter_precision_vs_recall.png  # Phân tán đánh đổi Precision vs Recall
│   │   ├── 12_scatter_map_vs_precision.png     # Tương quan Mask mAP@50-95 vs Precision
│   │   └── 13_scatter_map_vs_recall.png        # Tương quan Mask mAP@50-95 vs Recall
│   └── summary/
│       ├── 18_grouped_bar_main_metrics.png     # Grouped bar chart tổng hợp 6 chỉ số chính
│       ├── 19_radar_chart_main_metrics.png     # Radar chart toàn cảnh hiệu năng đa chiều
│       └── 20_delta_tsvm_vs_baseline.png       # Biểu đồ thanh ngang độ lệch Δ (TSVM - Baseline)
├── 06_reports/
│   ├── summary.csv                             # File CSV tổng hợp toàn bộ bảng số liệu
│   ├── summary.md                              # Báo cáo tổng hợp số liệu chi tiết
│   └── conclusions.md                          # Nhận xét học thuật khách quan theo 6 nhóm
└── README.md                                   # Tài liệu hướng dẫn và mục lục hệ thống
```

---

## 3. Các Phát Hiện Thực Nghiệm Chính
1. **Hiệu năng trung bình**: Mask mAP@50-95 của TSVM là **0.7246** so với **0.7210** của Baseline (+0.0036, +0.49%); Mask Precision là **0.9118** so với **0.9023**.
2. **Độ ổn định hạt ngẫu nhiên**: Std Mask mAP@50-95 là **0.0129** ở Baseline và **0.0078** ở TSVM; Range lần lượt là **0.0425** và **0.0273**.
3. **Mất mát phân đoạn (Val Seg Loss)**: Mean thay đổi từ **1.3045** xuống **1.2424** (-0.0622, -4.76%, p = 0.0908).
4. **Phân biệt nền & giảm cảnh báo giả**: Trên 40 ảnh nền âm tính, TSVM có FP trung bình **14.6** so với **16.8** của Baseline; TN trung bình lần lượt **25.4** và **23.2**.
