# HỆ THỐNG BIỂU ĐỒ VÀ HÌNH ẢNH ĐỐI CHỨNG THỰC NGHIỆM (300 DPI)
## Khóa Luận Cử Nhân CNTT: YOLO26s-seg vs YOLO26s-seg + C2TSVMamba (Kvasir-SEG, 6-Fold Cross-Validation)

Thư mục này chứa toàn bộ các biểu đồ đối sánh định lượng và định tính phục vụ cho Báo cáo tiến độ tuần và Khóa luận tốt nghiệp. Tất cả các hình ảnh đều được xuất ở độ phân giải cao chuẩn in ấn (300 DPI), đường nét sắc nét, phông chữ chuẩn học thuật.

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
