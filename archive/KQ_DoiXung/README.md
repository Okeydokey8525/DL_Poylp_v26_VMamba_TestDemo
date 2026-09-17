# HỆ THỐNG BIỂU ĐỒ VÀ HÌNH ẢNH ĐỐI CHỨNG THỰC NGHIỆM (300 DPI)
## Khóa Luận Cử Nhân CNTT: YOLO26s-seg vs YOLO26s-seg + C2TSVMamba (Kvasir-SEG, 6-Fold Cross-Validation)

Thư mục này chứa toàn bộ các biểu đồ đối sánh định lượng và định tính phục vụ cho Báo cáo tiến độ tuần và Khóa luận tốt nghiệp. Tất cả các hình ảnh đều được xuất ở độ phân giải cao chuẩn in ấn (300 DPI), đường nét sắc nét, phông chữ chuẩn học thuật.

---

### PHẦN 0: DỮ LIỆU TỔNG HỢP TRUNG BÌNH (MEAN ± STD) CHO 2 MÔ HÌNH
Để thuận tiện cho việc đối chiếu và lập trình tạo các biểu đồ mới mà không cần đọc lặp lại 12 file kết quả riêng lẻ của 6 seed trong scratch_summary.csv, thư mục này cung cấp 2 file CSV chuẩn hóa đã tính sẵn giá trị trung bình kèm độ lệch chuẩn (Mean ± Std):

1. **summary_mean_std_2models.csv** (Dạng bảng đối sánh theo từng chỉ số - Tương đương Bảng 1 báo cáo):
   - **Cấu trúc:** Mỗi dòng là một chỉ số (metric, display_name, category).
   - **Các cột số liệu:** aseline_mean, aseline_std, aseline_mean_pm_std (chuỗi định dạng Mean ± Std), aseline_range ([Min – Max]), 	svm_mean, 	svm_std, 	svm_mean_pm_std, 	svm_range, delta ($\Delta$), delta_pct (%), p_value (Kiểm định Paired t-test qua 6 seed), significance (mức ý nghĩa), clinical_interpretation (ý nghĩa lâm sàng).
   - **Mục đích:** Tra cứu nhanh số liệu làm bảng Word, báo cáo, và làm nhãn biểu đồ.

2. **summary_models_2rows.csv** (Dạng bảng 2 dòng cho 2 mô hình - Sẵn sàng cho code Python):
   - **Cấu trúc:** Dòng 1 là Baseline YOLO26s-seg, Dòng 2 là C2TSVMamba (Proposed).
   - **Mục đích:** Phù hợp cho code vẽ đồ thị cột (Bar chart), đồ thị radar (Radar chart) chỉ với cú pháp df['mask_map50_95_mean'] và yerr=df['mask_map50_95_std'].

`python
# Ví dụ vẽ biểu đồ cột từ summary_mean_std_2models.csv:
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('summary_mean_std_2models.csv')
row = df[df['metric'] == 'mask_map50_95'].iloc[0]
models = ['Baseline', 'C2TSVMamba']
means = [row['baseline_mean'], row['tsvm_mean']]
stds = [row['baseline_std'], row['tsvm_std']]

plt.figure(figsize=(6, 4), dpi=300)
plt.bar(models, means, yerr=stds, capsize=6, color=['#2563EB', '#DC2626'], alpha=0.85)
plt.ylabel('Mask mAP@50-95')
plt.title('So sánh Mask mAP@50-95 (Mean ± Std, 6 Seeds)')
plt.savefig('map50_95_demo.png', bbox_inches='tight')
`

---
### PHẦN 1: CÁC BIỂU ĐỒ ĐƠN LẺ (1 HÌNH 1 BIỂU ĐỒ - KHÔNG GHI CHÚ CALLOUT / SẠCH SẼ)
*Được tạo theo yêu cầu riêng biệt để nhìn rõ ràng, dễ chèn vào slide và các mục báo cáo chuyên sâu; lấy trung bình 6 seed độc lập (s0 đến s5) kèm dải độ lệch chuẩn ±1σ.*

#### Nhóm 1: Hàm Mất Mát (Loss Curves)
1. `val_seg_loss_comparison.png` (hoặc `01a_val_seg_loss_comparison.png`):
   - **Tên:** Validation Segmentation Loss qua 100 Epoch (Mean ± 1 Std).
   - **Ý nghĩa:** Biểu đồ cốt lõi chứng minh C2TSVMamba giảm mất mát phân đoạn mặt nạ so với Baseline, kiểm soát overfitting tốt hơn.
2. `val_seg_loss_comparison_zoomed.png` (hoặc `01a_val_seg_loss_comparison_zoomed.png`):
   - **Tên:** Validation Segmentation Loss (Tập trung dải hội tụ từ epoch 2 đến 100, thang đo y [1.2, 2.6]).
   - **Ý nghĩa:** Phóng to khu vực hội tụ để thấy rõ khoảng cách cải thiện ổn định và dải sai số hẹp của C2TSVMamba so với Baseline.
3. `train_seg_loss_comparison.png` (hoặc `01b_train_seg_loss_comparison.png`):
   - **Tên:** Training Segmentation Loss qua 100 Epoch.
4. `val_box_loss_comparison.png` (hoặc `01c_val_box_loss_comparison.png`):
   - **Tên:** Validation Bounding Box Loss qua 100 Epoch.
5. `val_cls_loss_comparison.png` (hoặc `01d_val_cls_loss_comparison.png`):
   - **Tên:** Validation Classification Loss qua 100 Epoch.

#### Nhóm 2: Độ Chính Xác Trung Bình mAP (mAP Curves)
6. `mask_map50_95_comparison.png` (hoặc `02a_mask_map50_95_comparison.png`):
   - **Tên:** Mask mAP@50-95 (Segmentation) qua 100 Epoch (Mean ± 1 Std).
   - **Ý nghĩa:** Biểu đồ trọng tâm chứng minh độ ổn định vượt trội (độ lệch chuẩn giảm 3 lần: ±0.0050 so với ±0.0150 của Baseline).
7. `mask_map50_comparison.png` (hoặc `02b_mask_map50_comparison.png`):
   - **Tên:** Mask mAP@50 (Segmentation) qua 100 Epoch.
8. `box_map50_95_comparison.png` (hoặc `02c_box_map50_95_comparison.png`):
   - **Tên:** Bounding Box mAP@50-95 (Detection) qua 100 Epoch.
9. `box_map50_comparison.png` (hoặc `02d_box_map50_comparison.png`):
   - **Tên:** Bounding Box mAP@50 (Detection) qua 100 Epoch.

#### Nhóm 3: Precision và Recall (Đánh Đổi & Hội Tụ)
10. `mask_precision_comparison.png` (hoặc `03a_mask_precision_comparison.png`):
    - **Tên:** Mask Precision qua 100 Epoch.
11. `mask_recall_comparison.png` (hoặc `03b_mask_recall_comparison.png`):
    - **Tên:** Mask Recall qua 100 Epoch (Đánh đổi do cơ chế siết chặt biên).
12. `box_precision_comparison.png` (hoặc `03c_box_precision_comparison.png`):
    - **Tên:** Bounding Box Precision qua 100 Epoch.
13. `box_recall_comparison.png` (hoặc `03d_box_recall_comparison.png`):
    - **Tên:** Bounding Box Recall qua 100 Epoch.

---

### PHẦN 2: CÁC BIỂU ĐỒ TỔNG HỢP VÀ ĐỐI CHỨNG ĐA CHIỀU

14. `01_loss_curves_comparison.png`:
    - Biểu đồ 4-trong-1 so sánh đồng thời 4 hàm mất mát: Train/Val Seg Loss và Train/Val Box/Cls Loss (đã làm sạch, không ghi chú callout).
15. `02_metric_curves_mAP_comparison.png`:
    - Biểu đồ 4-trong-1 so sánh đồng thời Mask mAP và Box mAP ở ngưỡng 50 và 50-95 (đã làm sạch).
16. `03_precision_recall_dynamics.png`:
    - Biểu đồ 4-trong-1 so sánh Precision và Recall cho cả Mask và Box qua 100 epoch.
17. `04_overall_benchmark_barchart.png`:
    - Biểu đồ cột tổng thể các chỉ số đo lường kèm thanh sai số ±1σ.
18. `05_fold_by_fold_comparison.png`:
    - Biểu đồ cột nhóm so sánh đối đầu trực diện giữa Baseline và TSVM trên từng seed (s0 đến s5).
19. `06_radar_chart_tradeoff.png`:
    - Biểu đồ mạng nhện (Radar Chart) đánh giá toàn diện đa tiêu chí: mAP, Precision, Recall, Độ ổn định seed, Tốc độ (FPS), Độ gọn nhẹ.
20. `07_qualitative_prediction_comparison.png`:
    - Minh chứng phân đoạn định tính thực tế trên ảnh nội soi: Ảnh gốc, Ground Truth, Dự đoán Baseline, Dự đoán C2TSVMamba đề xuất.
21. `08_confusion_matrix_side_by_side.png`:
    - Ma trận nhầm lẫn chuẩn hóa đặt cạnh nhau giữa Baseline (s4) và C2TSVMamba (s5) trên 127 tổn thương polyp.
22. `09_mask_pr_curve_side_by_side.png`:
    - Đường cong Precision-Recall của Mask (AUC) ở ngưỡng IoU 0.5.


---

### PHẦN 3: CÁC BIỂU ĐỒ DẠNG CỘT (BAR CHARTS) RIÊNG CHO VAL/SEG_LOSS
*Được thiết kế chuyên biệt để nhìn rõ ràng mức độ giảm mất mát phân đoạn giữa Baseline và TSVM mà không bị nén thang đo như biểu đồ đường 100 epoch.*

23. `val_seg_loss_barchart_comparison.png` (hoặc `01a_val_seg_loss_barchart.png`):
    - **Tên:** Biểu đồ cột nhóm so sánh val/seg_loss từng Seed (Seed 0 đến Seed 5) và Cột Tổng hợp Trung bình (Mean ± 1 Std).
    - **Đặc điểm:** Thang đo được căn chỉnh tối ưu (1.22 đến 1.58), hiển thị chính xác giá trị số thập phân trên từng cột. Nhìn vào thấy ngay TSVM thấp hơn Baseline ở 5/6 seed và ở mức trung bình.
24. `val_seg_loss_comprehensive_barchart.png`:
    - **Tên:** Biểu đồ cột 2 phần: (a) So sánh giá trị Trung bình 6 seed của cả 3 dòng mô hình (Baseline, P5_Attention, TSVM), và (b) Chi tiết đối đầu trực tiếp 6 seed.
    - **Ý nghĩa:** Làm nổi bật sự thất bại của P5_Attention (loss tăng vọt lên 1.4630) và sự thành công của TSVM (loss giảm sâu xuống 1.3812).
25. `val_seg_loss_reduction_barchart.png`:
    - **Tên:** Biểu đồ mức giảm Loss (Delta = Baseline - TSVM) qua từng seed.
    - **Ý nghĩa:** Cột màu xanh lá cây (> 0) khẳng định TSVM giảm loss thành công ở 5/6 seed với mức giảm trung bình +0.0352.
