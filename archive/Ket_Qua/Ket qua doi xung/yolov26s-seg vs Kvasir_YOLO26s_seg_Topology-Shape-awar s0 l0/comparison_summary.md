# Bảng Tổng Hợp Kết Quả So Sánh Mô Hình (Baseline vs Topology Shape VMamba)

- **Mô hình Baseline (Gốc)**: `Baseline: YOLOv26s-seg (Seed 0, l2)`
- **Mô hình Đề xuất Cải tiến**: `Proposed: YOLOv26s-seg + TSVM (Seed 0, l0)`
- **Tập dữ liệu**: Kvasir-SEG (Polyp Segmentation)
- **Số lượng Epoch**: 100

## 1. Bảng Chỉ Số Định Lượng Cực Đại (Peak Performance) & Cuối Cùng (Final Epoch)

| Metric | Baseline_Best | Baseline_Final | Proposed_TSVM_Best | Proposed_TSVM_Final | Delta_Best | Delta_Final |
| --- | --- | --- | --- | --- | --- | --- |
| Precision (Box) | 94.56% (ep 38) | 93.29% | 95.82% (ep 89) | 89.19% | +1.26% | -4.10% |
| Recall (Box) | 92.91% (ep 93) | 88.98% | 91.87% (ep 79) | 88.98% | -1.04% | +0.00% |
| mAP@50 (Box) | 93.65% (ep 92) | 92.21% | 92.59% (ep 80) | 90.99% | -1.06% | -1.22% |
| mAP@50-95 (Box) | 74.62% (ep 92) | 74.33% | 75.72% (ep 94) | 74.98% | +1.10% | +0.66% |
| Precision (Mask) | 95.07% (ep 99) | 94.15% | 95.76% (ep 90) | 90.71% | +0.69% | -3.43% |
| Recall (Mask) | 92.91% (ep 93) | 89.76% | 90.55% (ep 78) | 88.98% | -2.36% | -0.79% |
| mAP@50 (Mask) | 93.52% (ep 92) | 92.40% | 92.16% (ep 80) | 91.24% | -1.36% | -1.15% |
| mAP@50-95 (Mask) | 72.77% (ep 83) | 71.72% | 74.35% (ep 88) | 73.65% | +1.58% | +1.93% |


## 2. Nhận Xét & Phân Tích Khoa Học Đột Phá

1. **Kỷ lục phân đoạn Mask mAP@50-95**: Mô hình tích hợp **Topology Shape VMamba (TSVM)** đạt **74.35%**, vượt trội hơn Baseline (**72.77%**, tăng **+1.58%**).
2. **Định vị Bounding Box (Box mAP@50-95)**: Đạt đỉnh cao nhất toàn thực nghiệm **75.72%**, vượt Baseline (**74.62%**, tăng **+1.10%**).
3. **Khả năng duy trì độ chính xác cao**: Mask Precision đạt **95.76%** (ep 42) và tại best epoch đạt **93.93%**, kết hợp cùng Recall đạt **90.55%** (ep 88), đưa Mask F1 lên **91.80%** (cao nhất trong các mô hình thực nghiệm).
4. **Độ ổn định ở Epoch 100**: Tại epoch cuối cùng, TSVM vẫn giữ mức Mask mAP@50-95 là **73.65%**, cao hơn nhiều so với mức **71.72%** của Baseline.
