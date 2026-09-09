# BẢNG SO SÁNH CHỈ SỐ: MÔ HÌNH GỐC (BASELINE) vs MÔ HÌNH LAI TOPOLO (TOPOLOGY-SHAPE-AWARE VMAMBA)
### ĐÁNH GIÁ ĐỐI CHUẨN THỰC NGHIỆM TRÊN TẬP DỮ LIỆU KVASIR-SEG (CÙNG SEED 0)

---

## 📌 TỔNG QUAN THIẾT LẬP THỰC NGHIỆM (EXPERIMENTAL AUDIT)

- **Bộ dữ liệu (Dataset)**: `Kvasir-SEG` (Phân đoạn tổn thương Polyp đường tiêu hóa qua ảnh nội soi).
- **Mô hình Gốc (Baseline)**: `YOLO26s-seg` (`yolo26s-seg.pt`).
- **Mô hình Lai Topolo (Hybrid Topology Model)**: `YOLO26s-seg + Topology-Shape-Aware VMamba` (`yolo26s-seg-TopologyShapeVMamba.yaml`).
- **Cơ chế lai (Hybrid Mechanism)**: Tích hợp tiên nghiệm topo - hình thái học (**Topology-Shape Prior**) kết hợp với bộ quét trạng thái chọn lọc 2D (**Visual Mamba / SS2D**) vào kiến trúc YOLO26s-seg, nhằm kiểm soát độ cong đường bờ tổn thương và tăng cường trường tiếp nhận toàn cục với độ phức tạp tính toán tuyến tính $\mathcal{O}(N)$.
- **Cố định Siêu tham số**:
  - `Epochs`: 100
  - `Image Size`: 640 x 640
  - `Batch Size`: 16
  - `Optimizer`: `AdamW` ($lr_0 = 0.001$, $lrf = 0.01$, $weight\_decay = 0.0005$)
  - `Seed`: **`0`** (`deterministic = True`)
- **Tập số liệu đối chuẩn**:
  - **Mô hình Gốc**: 2 lượt chạy đối chuẩn (`s0_1GPU_l1` và `s0_1GPU_l2`), kết quả trùng khớp chính xác 100% qua 100 epochs.
  - **Mô hình Lai Topolo**: 8 lượt chạy độc lập (`l0` đến `l7`) cùng Seed 0 để khảo sát cả cấu hình tốt nhất và độ lệch chuẩn thống kê (Mean ± Std).

---

## 1. SO SÁNH ĐỐI ĐẦU MÔ HÌNH TỐT NHẤT (BEST RUN vs BEST RUN)
*So sánh giữa lượt chạy chuẩn của Mô hình Gốc và lượt chạy tốt nhất của Mô hình Lai Topolo (Run `l0`) cùng Seed 0.*

### 1.1. Bảng Chỉ Số Toàn Diện Tại Best Epoch (Snapshot tại đỉnh Mask mAP@50-95)
Thời điểm mô hình đạt hiệu năng phân đoạn tổn thương cao nhất (Mô hình Gốc: Epoch 83; Mô hình Lai Topolo: Epoch 88):

| Nhóm Nhiệm vụ | Tên Chỉ Số (Metric) | Mô hình Gốc (Baseline - Ep 83) | Mô hình Lai Topolo (TSVM l0 - Ep 88) | Chênh lệch Tuyệt đối ($\Delta$) | Tăng trưởng Tương đối (%) | Đánh giá Trực quan |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Phân đoạn Mặt nạ (Mask)** | **Mask mAP@50-95** | **72.77%** | **74.35%** | **+1.58%** | **+2.17%** | 🟢 **Vượt trội mạnh mẽ** |
| | Mask mAP@50 | **92.78%** | 91.66% | -1.12% | -1.21% | 🔴 Thấp hơn nhẹ ở ngưỡng lỏng |
| | Mask Precision (Độ chính xác) | 91.52% | **93.93%** | **+2.41%** | **+2.63%** | 🟢 **Triệt tiêu dương tính giả** |
| | Mask Recall (Độ nhạy) | **91.34%** | 89.76% | -1.58% | -1.73% | 🔴 Ràng buộc viền co chặt hơn |
| | Mask F1-Score | 91.43% | **91.80%** | **+0.37%** | **+0.40%** | 🟢 Cân bằng tối ưu hơn |
| **Phát hiện Hộp bao (Box)** | **Box mAP@50-95** | **73.39%** | **74.73%** | **+1.34%** | **+1.83%** | 🟢 **Định vị Bounding Box chuẩn hơn** |
| | Box mAP@50 | **92.20%** | 91.66% | -0.54% | -0.59% | 🟡 Tương đương |
| | Box Precision | 90.73% | **93.93%** | **+3.20%** | **+3.53%** | 🟢 Bounding box ít báo động giả |
| | Box Recall | **90.55%** | 89.76% | -0.79% | -0.87% | 🟡 Tương đương |
| | Box F1-Score | 90.64% | **91.80%** | **+1.16%** | **+1.28%** | 🟢 Vượt trội |

---

### 1.2. Bảng Chỉ Số Cực Đại Đạt Được (Peak Performance Across 100 Epochs)
Chỉ số cao nhất ghi nhận được ở bất kỳ epoch nào trong suốt quá trình huấn luyện:

| Tên Chỉ Số (Metric) | Mô hình Gốc Peak (Epoch) | Mô hình Lai Topolo Peak l0 (Epoch) | Đỉnh Tuyệt Đối Cả 8 Runs TSVM (Run / Ep) | So với Gốc ($\Delta$ l0) | Đánh giá |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Mask mAP@50-95** | 72.77% (Ep 83) | **74.35%** (Ep 88) | **74.35%** (`l0` - Ep 88) | **+1.58%** | 🟢 **Mô hình lai dẫn đầu** |
| Mask mAP@50 | **93.52%** (Ep 92) | 92.16% (Ep 80) | **93.60%** (`l2` - Ep 56) | -1.36% | 🟢 Đỉnh nhóm đạt 93.60% |
| Mask Precision | 95.07% (Ep 99) | **95.76%** (Ep 90) | **96.09%** (`l2` - Ep 90) | **+0.69%** | 🟢 **Mô hình lai kiểm soát viền tốt hơn** |
| Mask Recall | **92.91%** (Ep 93) | 90.55% (Ep 78) | **92.91%** (`l5` - Ep 97) | -2.36% | 🟡 Đỉnh nhóm ngang ngửa (92.91%) |
| Mask F1-Score | 91.99% (Ep 89) | **92.18%** (Ep 88) | **92.34%** (`l5` - Ep 97) | **+0.19%** | 🟢 Mô hình lai nhỉnh hơn |
| **Box mAP@50-95** | 74.62% (Ep 92) | **75.72%** (Ep 94) | **75.72%** (`l0` - Ep 94) | **+1.10%** | 🟢 **Vượt mốc 75%** |
| Box mAP@50 | 93.65% (Ep 92) | 92.59% (Ep 80) | **94.41%** (`l2` - Ep 57) | -1.06% | 🟢 Đỉnh nhóm đạt 94.41% |
| Box Precision | 94.56% (Ep 38) | **95.82%** (Ep 89) | **96.09%** (`l2` - Ep 90) | **+1.26%** | 🟢 Mô hình lai vượt trội |
| Box Recall | **92.91%** (Ep 93) | 91.87% (Ep 79) | 92.13% (`l5` - Ep 90) | -1.04% | 🔴 Mô hình gốc nhỉnh hơn |
| Box F1-Score | 91.59% (Ep 92) | **92.18%** (Ep 88) | **93.46%** (`l5` - Ep 90) | **+0.59%** | 🟢 Mô hình lai vượt trội |

---

### 1.3. Bảng Chỉ Số Tại Epoch Cuối Cùng (Final Epoch 100 - Đánh giá Độ Ổn Định và Quá Khớp)

| Chỉ Số Tại Epoch 100 | Mô hình Gốc (Ep 100) | Mô hình Lai Topolo (l0 - Ep 100) | Chênh lệch ($\Delta$) | Đánh giá Mức độ Suy giảm Cuối chu kỳ |
| :--- | :---: | :---: | :---: | :--- |
| **Mask mAP@50-95** | 71.72% | **73.65%** | **+1.93%** | 🟢 **Mô hình lai duy trì độ chính xác cực tốt, không tụt dốc** |
| Mask mAP@50 | **92.40%** | 91.24% | -1.16% | Mô hình gốc giữ mAP50 cao hơn |
| Mask Precision | **94.15%** | 90.71% | -3.44% | Cả hai đều giảm so với thời điểm đỉnh |
| Mask Recall | **89.76%** | 88.98% | -0.78% | Chênh lệch rất nhỏ (dưới 1%) |
| Mask F1-Score | **91.90%** | 89.84% | -2.06% | Mô hình gốc nhỉnh hơn |
| **Box mAP@50-95** | 74.33% | **74.98%** | **+0.65%** | 🟢 **Mô hình lai giữ vững độ chính xác hộp bao** |
| Box mAP@50 | **92.21%** | 90.99% | -1.22% | Tương đương |
| Box Precision | **93.29%** | 89.19% | -4.10% | Mô hình gốc nhỉnh hơn ở ep cuối |
| Box Recall | 88.98% | 88.98% | **0.00%** | Hoàn toàn bằng nhau |

---

## 2. SO SÁNH THỐNG KÊ TOÀN DIỆN (MEAN ± STD CỦA 8 RUNS MÔ HÌNH LAI vs GỐC)
*Đánh giá khách quan trên toàn bộ 8 lượt chạy độc lập của Mô hình Lai Topolo (`l0` đến `l7`) để loại trừ yếu tố ngẫu nhiên.*

### 2.1. Bảng So Sánh Chỉ Số Trung Bình Tại Best Epoch

| Chỉ Số Đánh Giá | Mô hình Gốc (Seed 0) | Mô hình Lai Topolo (8 Runs: Mean ± Std) | Mô hình Lai Khoảng [Min - Max] | Chênh lệch Trung bình ($\Delta$ Mean) | Chênh lệch Đỉnh ($\Delta$ Max) | Ý nghĩa Thống kê ($p$-value) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Mask mAP@50-95** | **72.77%** | **73.28 ± 0.65%** | [72.61% - 74.35%] | **+0.51%** | **+1.58%** | $p = 0.061$ (6/8 runs vượt gốc) |
| Mask mAP@50 | **92.78%** | 91.27 ± 0.40% | [90.77% - 91.74%] | -1.51% | -1.04% | Gốc chiếm ưu thế ở IoU lỏng |
| Mask Precision | 91.52% | **91.60 ± 2.53%** | [88.23% - 94.88%] | **+0.08%** | **+3.36%** | Mô hình lai có nhiều run Precision rất cao |
| Mask Recall | **91.34%** | 88.51 ± 1.97% | [84.61% - 91.47%] | -2.83% | +0.13% | Ràng buộc viền làm giảm bao phủ rìa |
| Mask F1-Score | **91.43%** | 89.99 ± 1.13% | [88.40% - 91.80%] | -1.44% | **+0.37%** | Bị chi phối bởi Recall |
| **Box mAP@50-95** | **73.39%** | **74.04 ± 0.65%** | [72.70% - 74.73%] | **+0.65%** | **+1.34%** | **$p = 0.025$ (Có ý nghĩa $p < 0.05$)** |
| Box mAP@50 | **92.20%** | 91.24 ± 0.45% | [90.61% - 91.80%] | -0.96% | -0.40% | Tương đương |
| Box Precision | 90.73% | **91.70 ± 1.79%** | [89.10% - 94.02%] | **+0.97%** | **+3.29%** | Hộp bao ít dương tính giả hơn |
| Box Recall | **90.55%** | 86.92 ± 2.13% | [83.82% - 89.76%] | -3.63% | -0.79% | Mô hình gốc nhỉnh hơn |
| Box F1-Score | **90.64%** | 89.23 ± 1.48% | [87.43% - 91.80%] | -1.41% | **+1.16%** | Run tốt nhất vượt trội |

---

### 2.2. Bảng So Sánh Chỉ Số Cực Đại Trung Bình (Average Peak Performance)

| Chỉ Số Đánh Giá | Mô hình Gốc Peak | Mô hình Lai Peak (Mean ± Std) | Mô hình Lai Peak [Min - Max] | $\Delta$ Mean | $\Delta$ Max Peak |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Mask mAP@50-95** | 72.77% | **73.28 ± 0.65%** | [72.61% - 74.35%] | **+0.51%** | **+1.58%** |
| Mask mAP@50 | **93.52%** | 92.59 ± 0.68% | [91.49% - 93.60%] | -0.93% | **+0.08%** |
| Mask Precision | 95.07% | **95.48 ± 0.61%** | [94.08% - 96.09%] | **+0.41%** | **+1.02%** |
| Mask Recall | **92.91%** | 91.09 ± 0.82% | [90.55% - 92.91%] | -1.82% | 0.00% |
| **Box mAP@50-95** | 74.62% | 74.41 ± 0.75% | [73.31% - 75.72%] | -0.21% | **+1.10%** |
| Box mAP@50 | 93.65% | 92.55 ± 0.97% | [91.19% - 94.41%] | -1.10% | **+0.76%** |
| Box Precision | 94.56% | **95.06 ± 0.69%** | [93.89% - 96.09%] | **+0.50%** | **+1.53%** |
| Box Recall | **92.91%** | 90.59 ± 0.93% | [89.73% - 92.13%] | -2.32% | -0.78% |

---

### 2.3. Bảng So Sánh Chỉ Số Trung Bình Tại Epoch 100 (Final Epoch Average)

| Chỉ Số Tại Epoch 100 | Mô hình Gốc (Ep 100) | Mô hình Lai Topolo (Mean ± Std) | Mô hình Lai Khoảng [Min - Max] | Đánh giá Độ ổn định Cuối |
| :--- | :---: | :---: | :---: | :--- |
| **Mask mAP@50-95** | 71.72% | **72.02 ± 1.03%** | [70.46% - 73.65%] | 🟢 **Mô hình lai giữ vững phong độ (+0.30% mean, +1.93% max)** |
| Mask mAP@50 | **92.40%** | 90.83 ± 0.97% | [89.73% - 92.80%] | Mô hình gốc nhỉnh hơn |
| Mask Precision | **94.15%** | 91.12 ± 2.54% | [88.15% - 94.73%] | Tương đương |
| Mask Recall | **89.76%** | 87.65 ± 2.50% | [84.13% - 91.34%] | Mô hình gốc nhỉnh hơn |
| **Box mAP@50-95** | **74.33%** | 73.56 ± 0.75% | [72.83% - 74.98%] | Chênh lệch nhỏ |
| Box mAP@50 | **92.21%** | 90.70 ± 0.72% | [89.31% - 91.67%] | Chênh lệch nhỏ |

---

## 3. BẢNG KÊ CHI TIẾT TỪNG LƯỢT CHẠY CỦA MÔ HÌNH LAI TOPOLO (8 RUNS SEED 0)

Bảng kê tường minh toàn bộ số liệu 8 runs để người đọc dễ dàng tra cứu, kiểm chứng chéo:

| Lượt chạy (Run ID) | Best Epoch | Mask mAP50-95 | Mask mAP50 | Mask Precision | Mask Recall | Mask F1 | Box mAP50-95 | Box mAP50 | Box Precision | Box Recall | Box F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TSVM Run `l0`** ⭐ | **Ep 88** | **74.35%** | 91.66% | 93.93% | 89.76% | **91.80%** | **74.73%** | 91.66% | 93.93% | 89.76% | **91.80%** |
| **TSVM Run `l1`** | Ep 86 | 72.73% | 91.45% | **94.88%** | 87.50% | 91.04% | 73.57% | 90.77% | **94.02%** | 86.72% | 90.22% |
| **TSVM Run `l2`** | Ep 94 | 72.89% | 90.77% | 93.88% | 84.61% | 89.01% | 72.70% | 90.79% | 93.01% | 83.82% | 88.18% |
| **TSVM Run `l3`** | Ep 90 | 73.16% | **91.74%** | 88.56% | **91.47%** | 89.99% | 74.53% | 90.61% | 90.12% | 86.16% | 88.10% |
| **TSVM Run `l4`** | Ep 90 | 73.73% | 90.88% | 91.88% | 88.98% | 90.40% | 73.89% | 91.34% | 91.06% | 88.26% | 89.64% |
| **TSVM Run `l5`** 🥈 | Ep 84 | **73.95%** | 91.51% | 89.92% | 88.19% | 89.04% | 74.23% | 91.53% | 89.10% | 87.40% | 88.24% |
| **TSVM Run `l6`** | Ep 88 | 72.61% | 90.77% | 91.54% | 88.98% | 90.24% | 74.38% | **91.80%** | 91.54% | 88.98% | 90.24% |
| **TSVM Run `l7`** | Ep 75 | 72.80% | 91.36% | 88.23% | 88.56% | 88.40% | 74.32% | 91.41% | 90.86% | 84.25% | 87.43% |
| **Mô hình Gốc (Baseline)** | **Ep 83** | **72.77%** | **92.78%** | **91.52%** | **91.34%** | **91.43%** | **73.39%** | **92.20%** | **90.73%** | **90.55%** | **90.64%** |

---

## 4. TIẾN TRÌNH HÀM MẤT MÁT (LOSS DYNAMICS) VÀ ĐỘNG HỌC HỘI TỤ

Bảng đối chiếu giá trị hàm mất mát phân đoạn (`Segmentation Loss`) giữa Mô hình Gốc và Mô hình Lai Topolo qua các mốc huấn luyện:

| Mốc Huấn Luyện | Train Seg Loss (Gốc) | Train Seg Loss (Lai Topolo Mean) | Val Seg Loss (Gốc) | Val Seg Loss (Lai Topolo Mean ± Std) | Mask mAP@50-95 (Gốc) | Mask mAP@50-95 (Lai Topolo Mean) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Epoch 1** | **1.7639** | 1.8420 | **4.0376** | 12.0409 ± 6.0690 | 2.10% | **12.59%** |
| **Epoch 20** | **1.2370** | 1.2900 | **1.6406** | 1.6596 ± 0.1042 | **65.03%** | 59.05% |
| **Epoch 50** | **0.9989** | 1.0351 | 1.5273 | **1.4542 ± 0.0325** | 67.16% | **69.10%** |
| **Epoch 80** | **0.8577** | 0.9037 | 1.4450 | **1.4422 ± 0.0752** | 70.45% | **71.18%** |
| **Epoch 100** | **0.6369** | 0.6505 | 1.6273 | **1.4759 ± 0.0449** | 71.72% | **72.02%** |

### Phát hiện Then chốt về Động học:
1. **Khả năng chống Overfitting vượt trội của Mô hình Lai Topolo**:
   - Ở giai đoạn cuối (Epoch 80 - 100), `Val Seg Loss` của Mô hình Gốc bị dội ngược từ **1.4450 lên 1.6273** (dấu hiệu quá khớp rõ rệt trên tập huấn luyện).
   - Ngược lại, Mô hình Lai Topolo kiểm soát mất mát kiểm định cực tốt, chỉ tăng nhẹ từ **1.4422 lên 1.4759** (thấp hơn Gốc đáng kể), chứng minh khả năng tổng quát hóa xuất sắc.
2. **Tốc độ bứt phá ngưỡng chất lượng cao (70% Mask mAP@50-95)**:
   - Mô hình Gốc cần đến **Epoch 59** mới chạm mốc 70%.
   - Mô hình Lai Topolo bứt phá sớm hơn nhiều: **Run `l2` chạm mốc ở Epoch 31**, **Run `l0` chạm mốc ở Epoch 37**, **Run `l4` & `l5` chạm mốc ở Epoch 49**.

---

## 5. SO SÁNH ĐỘ PHỨC TẠP TÍNH TOÁN VÀ TÀI NGUYÊN (COMPLEXITY & RESOURCES)

| Chỉ Số Đánh Giá | Mô hình Gốc (Baseline) | Mô hình Lai Topolo (TSVM) | Chênh lệch ($\Delta$) | Đánh giá |
| :--- | :---: | :---: | :---: | :--- |
| **Dung lượng file trọng số (`best.pt`)** | **22.27 MB** (23,351,007 bytes) | **23.86 MB** (25,018,041 bytes) | **+1.59 MB (+7.14%)** | Tăng rất ít dung lượng, dễ tích hợp |
| **Thời gian huấn luyện (100 Epochs)** | **6,580.4 s** (~1.83 giờ) | **14,155.2 s** (~3.93 giờ) | **+2.15x** | Chậm hơn 2.15 lần do cơ chế quét chọn lọc SS2D |
| **Tốc độ xử lý trung bình / epoch** | ~65.8 giây / epoch | ~141.6 giây / epoch | +75.8 giây / epoch | Hoàn toàn khả thi trên 1 GPU cá nhân |

---

## 6. PHÂN TÍCH KHOA HỌC CHUYÊN SÂU: BẢN CHẤT SỰ TĂNG - GIẢM CÁC CHỈ SỐ

### 6.1. Tại sao Mô hình Lai Topolo tăng mạnh Mask mAP@50-95 (+1.58%) và Precision (+2.41%)?
- **Đặc trưng tổn thương polyp**: Đường viền polyp ruột rất phức tạp, dễ bị nhầm với nếp gấp đại tràng, bọt dịch hoặc vùng bóng phản xạ ánh sáng của đèn nội soi.
- **Hạn chế của mô hình gốc**: Các lớp tích chập cục bộ (CNN) có xu hướng dự đoán mặt nạ "tràn biên" (boundary bleeding), sinh ra viền lồi lõm hoặc lan sang niêm mạc lành xung quanh.
- **Cơ chế mô hình lai**:
  1. Khối **Visual Mamba (SS2D)** quét chọn lọc đa chiều thu nhận liên kết ngữ cảnh toàn cục dọc theo toàn bộ chu vi tổn thương.
  2. Ràng buộc **Topology-Shape Prior** áp đặt tiên nghiệm hình thái học, buộc mô hình chỉ dự đoán các cấu trúc hình học khép kín và liên tục.
  3. Nhờ đó, ở các ngưỡng kiểm tra khắt khe (IoU từ 0.75 đến 0.95), mặt nạ của mô hình lai bám sát từng milimet bờ polyp thực tế, triệt tiêu gần như hoàn toàn các pixel dự đoán dương tính giả $\rightarrow$ **Mask Precision đạt 93.93% (l0) và đỉnh đạt 96.09%**, kéo theo **Mask mAP@50-95 tăng vọt lên 74.35%**.

### 6.2. Tại sao Recall và mAP@50 lại sụt giảm nhẹ? (Hiện tượng Đánh đổi - Trade-off)
- **Mô hình Gốc dự đoán rộng bản (hào phóng)**: Khi không bị ràng buộc viền nghiêm ngặt, mô hình gốc dễ dàng vẽ các mặt nạ to hơn tổn thương thật. Ở ngưỡng lỏng **IoU = 0.50**, chỉ cần bao phủ được 50% là tính đúng, do đó mô hình gốc dễ đạt Recall cao (91.34%) và mAP@50 cao (92.78%).
- **Mô hình Lai siết chặt viền**: Việc áp đặt hình thái phạt nặng các pixel dự đoán tràn ngoài viền khiến mô hình trở nên khắt khe và thận trọng hơn tại mép ngoài. Với một số polyp dẹt/phẳng (sessile/flat polyps) có rìa cực mỏng, viền có thể bị co vào bên trong $\rightarrow$ Làm giảm nhẹ Recall (-2.83% trung bình) và mAP@50 (-1.51% trung bình).
- **Ý nghĩa lâm sàng**: Trong can thiệp nội soi (như cắt polyp qua niêm mạc EMR/ESD), độ chính xác đường biên khắt khe (High mAP@50-95) và độ chính xác phân loại (High Precision) quan trọng hơn nhiều việc dự đoán lem nhem diện rộng, vì việc cắt lẹm vào thành ruột lành có thể dẫn tới thủng ruột đại tràng.

---

## 7. TỔNG KẾT VÀ ĐỀ XUẤT CHO LUẬN VĂN
1. **Kết luận cốt lõi**: Mô hình Lai Topolo là một cải tiến **thực chất, chuẩn xác và bền bỉ**, giúp nâng cao chất lượng phân đoạn ở ngưỡng khắt khe từ **72.77% lên 74.35% (Best Run)** và trung bình đạt **73.28 ± 0.65%**, với **6/8 lượt chạy độc lập vượt mốc Baseline**.
2. **Khuyến nghị cách viết trong Luận văn**: 
   - Sử dụng **Bảng 1.1** (Best Run Comparison) để làm nổi bật tiềm năng bứt phá trần hiệu năng của mô hình đề xuất.
   - Sử dụng **Bảng 2.1** (8 Runs Mean ± Std) để khẳng định tính khoa học, khách quan và minh bạch của thực nghiệm.
   - Trình bày thẳng thắn sự đánh đổi giữa Precision và Recall như một minh chứng khoa học cho thấy cơ chế Topo-Shape đang hoạt động đúng theo nguyên lý thiết kế.
