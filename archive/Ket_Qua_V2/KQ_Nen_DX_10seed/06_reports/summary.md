# Báo Cáo Tổng Hợp Thống Kê Thực Nghiệm 10 Seed
## Đối tượng so sánh: YOLO26s-seg Baseline vs YOLO26s-seg + TSVM

Tập dữ liệu kiểm định: `Kvasir-SEG (data_bg20.yaml)` — Tổng cộng 160 ảnh (120 ảnh polyp có nhãn gồm 127 đối tượng ground-truth, 40 ảnh nền âm tính `normal-cecum`).
Số lần lặp ngẫu nhiên: 10 seeds độc lập (seed 0 đến 9), huấn luyện 100 epochs, trích xuất metric tại epoch tối ưu (best.pt) theo `Mask mAP@50-95`.

---

## 1. Bảng So Sánh Hiệu Năng Tổng Quát (Mean ± Standard Deviation)

| Nhóm Metric | Metric | Baseline (Mean ± Std) | TSVM (Mean ± Std) | Δ (TSVM - Baseline) | % Thay đổi | p-value (t-test) | Ý nghĩa (α=0.05) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Segmentation** | Mask mAP@50-95 | 0.7210 ± 0.0129 | 0.7246 ± 0.0078 | +0.0036 | +0.49% | 0.3839 | Chưa (p > 0.05) |
| | Mask mAP@50 | 0.9119 ± 0.0107 | 0.9062 ± 0.0082 | -0.0056 | -0.62% | 0.2273 | Chưa |
| | Mask Precision | 0.9023 ± 0.0339 | 0.9118 ± 0.0246 | +0.0095 | +1.05% | 0.5428 | Chưa |
| | Mask Recall | 0.8584 ± 0.0252 | 0.8625 ± 0.0173 | +0.0041 | +0.48% | 0.5907 | Chưa |
| **Bounding Box** | Box mAP@50-95 | 0.7262 ± 0.0198 | 0.7285 ± 0.0141 | +0.0023 | +0.32% | 0.7152 | Chưa |
| | Box mAP@50 | 0.9011 ± 0.0116 | 0.9006 ± 0.0090 | -0.0004 | -0.05% | 0.9334 | Chưa |
| | Box Precision | 0.8992 ± 0.0326 | 0.9062 ± 0.0251 | +0.0070 | +0.78% | 0.5921 | Chưa |
| | Box Recall | 0.8434 ± 0.0337 | 0.8567 ± 0.0152 | +0.0133 | +1.58% | 0.2674 | Chưa |
| **Loss** | Val Seg Loss | 1.3045 ± 0.0867 | 1.2424 ± 0.0387 | -0.0622 | -4.76% | 0.0908 | Chưa |
| **Training** | Best Epoch | 87.3 ± 13.1 | 91.7 ± 4.9 | +4.4 | +5.04% | 0.3149 | Chưa |

---

## 2. Phân Tích Độ Ổn Định và Phân Bố (Dispersion Analysis)

| Metric | Mô hình | Min (Seed) | Max (Seed) | Range (Max - Min) | Độ lệch chuẩn (Std) | Tỷ lệ phương sai (F-ratio) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Mask mAP@50-95** | Baseline | 0.6941 (s3) | 0.7366 (s0) | 0.0425 | 0.0129 | Baseline / TSVM = 2.75x |
| | TSVM | 0.7065 (s7) | 0.7339 (s8) | 0.0273 | 0.0078 | (Độ biến thiên giảm 39.5%) |
| **Mask Precision** | Baseline | 0.8533 | 0.9535 | 0.1002 | 0.0339 | Baseline / TSVM = 1.90x |
| | TSVM | 0.8595 | 0.9437 | 0.0842 | 0.0246 | (Độ biến thiên giảm 27.4%) |
| **Val Seg Loss** | Baseline | 1.2022 | 1.4501 | 0.2479 | 0.0867 | Baseline / TSVM = 5.02x |
| | TSVM | 1.1777 | 1.3020 | 0.1243 | 0.0387 | (Độ biến thiên giảm 55.4%) |

---

## 3. So Sánh Seed-by-Seed (Tỷ lệ thắng/thua theo từng hạt ngẫu nhiên)

- **Mask mAP@50-95**: TSVM cao hơn ở **6/10 seed** (s1, s2, s3, s6, s8, s9); Baseline cao hơn ở **4/10 seed** (s0, s4, s5, s7).
- **Mask Precision**: TSVM cao hơn ở **5/10 seed**; Baseline cao hơn ở **5/10 seed**.
- **Mask Recall**: TSVM cao hơn ở **6/10 seed**; Baseline cao hơn ở **4/10 seed**.
- **Validation Segmentation Loss**: TSVM có loss thấp hơn ở **8/10 seed**; Baseline thấp hơn ở **2/10 seed**.
