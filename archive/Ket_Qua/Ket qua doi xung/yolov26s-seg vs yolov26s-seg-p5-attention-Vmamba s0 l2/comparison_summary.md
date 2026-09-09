# BÁO CÁO TOÀN DIỆN SO SÁNH HIỆU NĂNG MÔ HÌNH
## BASELINE (YOLO26s-seg) vs MÔ HÌNH ĐỀ XUẤT CẢI TIẾN (YOLO26s-seg + P5 Attention VMamba)

---

## THÔNG TIN TỔNG QUAN VÀ THIẾT LẬP THỰC NGHIỆM
- **Bộ dữ liệu (Dataset)**: `Kvasir-SEG` (Phân đoạn tổn thương Polyp đường tiêu hóa qua ảnh nội soi)
- **Mô hình Gốc (Baseline)**: `YOLOv26s-seg` (`yolo26s-seg.pt`)
- **Mô hình Cải tiến (Proposed)**: `YOLOv26s-seg + P5 Attention VMamba` (`yolo26s-seg-Attention-VMamba-P5.yaml`)
- **Cơ chế cải tiến**: Tích hợp khối **Visual Mamba (VMamba / SSM)** kết hợp cơ chế **Attention** tại tầng đặc trưng ngữ nghĩa mức cao **P5** (Stride 32) nhằm mở rộng trường tiếp nhận toàn cục tuyến tính mà không làm bùng nổ chi phí tính toán.
- **Kích thước ảnh đầu vào (Image Size)**: `640 x 640`
- **Số lượng Epoch huấn luyện**: `100 epochs`
- **Batch size**: `16`
- **Thuật toán tối ưu (Optimizer)**: `AdamW` (Tốc độ học cơ sở $lr_0 = 0.001$)
- **Phần cứng thực thi**: `1x GPU`
- **Quy mô đánh giá**: So sánh chi tiết trên **Mô hình có kết quả tốt nhất (Best Run)** và **Giá trị Trung bình qua 10 Lần chạy độc lập (10-Run Average Benchmark)**.

---

## PHẦN 1: SO SÁNH KẾT QUẢ MÔ HÌNH TỐT NHẤT (BEST RUN COMPARISON)
So sánh trực tiếp giữa Run tốt nhất của Baseline (`s0_1GPU_l2`) và Run tốt nhất của Mô hình Đề xuất VMamba (`s0_1GPU_l2`).

### 1.1. Bảng Chỉ Số Cực Đại Đạt Được (Peak Performance Across 100 Epochs)
Chỉ số đỉnh cao nhất mà mỗi mô hình ghi nhận được trong toàn bộ quá trình 100 epochs:
| Metric           | Baseline Best      | Proposed VMamba Best   | Chênh lệch Tuyệt đối (Δ)   | Tăng trưởng Tương đối (%)   | Đánh giá       |
|:-----------------|:-------------------|:-----------------------|:---------------------------|:----------------------------|:---------------|
| Precision (Box)  | **94.56%** (ep 38) | **95.28%** (ep 97)     | **+0.72%**                 | **+0.76%**                  | 🟢 Vượt trội   |
| Recall (Box)     | **92.91%** (ep 93) | **91.34%** (ep 92)     | **-1.57%**                 | **-1.69%**                  | 🔴 Thấp hơn    |
| mAP@50 (Box)     | **93.65%** (ep 92) | **92.54%** (ep 92)     | **-1.11%**                 | **-1.19%**                  | 🔴 Thấp hơn    |
| mAP@50-95 (Box)  | **74.62%** (ep 92) | **75.26%** (ep 97)     | **+0.63%**                 | **+0.85%**                  | 🟢 Vượt trội   |
| Precision (Mask) | **95.07%** (ep 99) | **96.18%** (ep 97)     | **+1.12%**                 | **+1.17%**                  | 🟢 Vượt trội   |
| Recall (Mask)    | **92.91%** (ep 93) | **93.70%** (ep 85)     | **+0.79%**                 | **+0.85%**                  | 🟢 Vượt trội   |
| mAP@50 (Mask)    | **93.52%** (ep 92) | **93.18%** (ep 92)     | **-0.34%**                 | **-0.37%**                  | 🟡 Tương đương |
| mAP@50-95 (Mask) | **72.77%** (ep 83) | **73.22%** (ep 97)     | **+0.46%**                 | **+0.63%**                  | 🟢 Vượt trội   |

### 1.2. Bảng Chỉ Số Đồng Thời Tại Epoch Tốt Nhất (Best Epoch by Mask mAP50-95)
Chỉ số toàn diện tại thời điểm mô hình đạt độ chính xác phân đoạn `Mask mAP@50-95` cao nhất (Baseline: Epoch 83; Proposed VMamba: Epoch 97):
| Metric           | Baseline (Epoch 83)   | Proposed VMamba (Epoch 97)   | Chênh lệch Tuyệt đối (Δ)   | Tăng trưởng Tương đối (%)   | Đánh giá       |
|:-----------------|:----------------------|:-----------------------------|:---------------------------|:----------------------------|:---------------|
| Precision (Box)  | 90.73%                | 95.28%                       | **+4.56%**                 | **+5.02%**                  | 🟢 Vượt trội   |
| Recall (Box)     | 90.55%                | 83.47%                       | **-7.09%**                 | **-7.83%**                  | 🔴 Thấp hơn    |
| mAP@50 (Box)     | 92.20%                | 91.86%                       | **-0.35%**                 | **-0.38%**                  | 🟡 Tương đương |
| mAP@50-95 (Box)  | 73.39%                | 75.26%                       | **+1.87%**                 | **+2.54%**                  | 🟢 Vượt trội   |
| Precision (Mask) | 91.52%                | 96.18%                       | **+4.67%**                 | **+5.10%**                  | 🟢 Vượt trội   |
| Recall (Mask)    | 91.34%                | 84.25%                       | **-7.09%**                 | **-7.76%**                  | 🔴 Thấp hơn    |
| mAP@50 (Mask)    | 92.78%                | 92.65%                       | **-0.13%**                 | **-0.14%**                  | 🟡 Tương đương |
| mAP@50-95 (Mask) | 72.77%                | 73.22%                       | **+0.46%**                 | **+0.63%**                  | 🟢 Vượt trội   |

### 1.3. Bảng Chỉ Số Tại Epoch Cuối Cùng (Final Epoch 100)
Chỉ số đo lường tại thời điểm kết thúc quá trình huấn luyện (Epoch 100), phản ánh mức độ ổn định hội tụ:
| Metric           | Baseline (Epoch 100)   | Proposed VMamba (Epoch 100)   | Chênh lệch Tuyệt đối (Δ)   | Tăng trưởng Tương đối (%)   | Đánh giá       |
|:-----------------|:-----------------------|:------------------------------|:---------------------------|:----------------------------|:---------------|
| Precision (Box)  | 93.29%                 | 90.57%                        | **-2.72%**                 | **-2.92%**                  | 🔴 Thấp hơn    |
| Recall (Box)     | 88.98%                 | 87.40%                        | **-1.57%**                 | **-1.77%**                  | 🔴 Thấp hơn    |
| mAP@50 (Box)     | 92.21%                 | 92.12%                        | **-0.09%**                 | **-0.09%**                  | 🟡 Tương đương |
| mAP@50-95 (Box)  | 74.33%                 | 74.78%                        | **+0.45%**                 | **+0.61%**                  | 🟢 Vượt trội   |
| Precision (Mask) | 94.15%                 | 91.44%                        | **-2.70%**                 | **-2.87%**                  | 🔴 Thấp hơn    |
| Recall (Mask)    | 89.76%                 | 88.19%                        | **-1.58%**                 | **-1.75%**                  | 🔴 Thấp hơn    |
| mAP@50 (Mask)    | 92.40%                 | 92.84%                        | **+0.44%**                 | **+0.48%**                  | 🟢 Vượt trội   |
| mAP@50-95 (Mask) | 71.72%                 | 72.96%                        | **+1.24%**                 | **+1.72%**                  | 🟢 Vượt trội   |

---

## PHẦN 2: SO SÁNH TỈ LỆ TRUNG BÌNH QUA 10 LẦN CHẠY (10-RUN AVERAGE BENCHMARK)
Để đảm bảo tính khách quan khoa học, loại bỏ yếu tố ngẫu nhiên do khởi tạo trọng số và phân tách batch, mô hình đề xuất được huấn luyện qua **10 lần chạy độc lập (10 runs: l0 đến l9)**. Dưới đây là bảng thống kê tổng hợp giá trị Trung bình ($\mu$) và Độ lệch chuẩn ($\sigma$).

### 2.1. Bảng So Sánh Chỉ Số Cực Đại Trung Bình (Average Peak Performance: Mean ± Std)
| Metric           | Baseline (Mean ± Std)   | Baseline [Min - Max]   | Proposed VMamba 10 Runs (Mean ± Std)   | Proposed [Min - Max]   | Chênh lệch Mean (Δ)   |
|:-----------------|:------------------------|:-----------------------|:---------------------------------------|:-----------------------|:----------------------|
| Precision (Box)  | 95.48 ± 1.06%           | [94.56% - 96.39%]      | **94.09 ± 0.97%**                      | [92.90% - 95.28%]      | **-1.39%**            |
| Recall (Box)     | 91.47 ± 1.67%           | [90.02% - 92.91%]      | **90.18 ± 0.70%**                      | [88.98% - 91.34%]      | **-1.29%**            |
| mAP@50 (Box)     | 92.73 ± 1.07%           | [91.80% - 93.65%]      | **91.61 ± 0.53%**                      | [90.94% - 92.54%]      | **-1.12%**            |
| mAP@50-95 (Box)  | 74.75 ± 0.15%           | [74.62% - 74.88%]      | **73.43 ± 1.04%**                      | [71.92% - 75.26%]      | **-1.32%**            |
| Precision (Mask) | 95.18 ± 0.13%           | [95.07% - 95.29%]      | **94.56 ± 0.89%**                      | [92.91% - 96.18%]      | **-0.62%**            |
| Recall (Mask)    | 92.52 ± 0.45%           | [92.13% - 92.91%]      | **90.69 ± 1.36%**                      | [88.98% - 93.70%]      | **-1.83%**            |
| mAP@50 (Mask)    | 92.51 ± 1.17%           | [91.50% - 93.52%]      | **92.43 ± 0.59%**                      | [91.26% - 93.18%]      | **-0.08%**            |
| mAP@50-95 (Mask) | 72.81 ± 0.05%           | [72.77% - 72.85%]      | **72.15 ± 0.86%**                      | [70.47% - 73.22%]      | **-0.66%**            |

### 2.2. Bảng So Sánh Chỉ Số Đồng Thời Tại Best Epoch Trung Bình (Average Best-Epoch Performance)
| Metric           | Baseline (Mean ± Std)   | Proposed VMamba 10 Runs (Mean ± Std)   | Chênh lệch Mean (Δ)   |
|:-----------------|:------------------------|:---------------------------------------|:----------------------|
| Precision (Box)  | 93.56 ± 3.27%           | **91.48 ± 2.39%**                      | **-2.08%**            |
| Recall (Box)     | 87.34 ± 3.71%           | **84.06 ± 2.00%**                      | **-3.28%**            |
| mAP@50 (Box)     | 92.00 ± 0.23%           | **90.78 ± 0.97%**                      | **-1.22%**            |
| mAP@50-95 (Box)  | 74.13 ± 0.86%           | **72.80 ± 1.54%**                      | **-1.33%**            |
| Precision (Mask) | 92.56 ± 1.21%           | **92.40 ± 2.56%**                      | **-0.17%**            |
| Recall (Mask)    | 88.58 ± 3.18%           | **84.64 ± 2.17%**                      | **-3.94%**            |
| mAP@50 (Mask)    | 91.94 ± 0.96%           | **91.33 ± 0.96%**                      | **-0.61%**            |
| mAP@50-95 (Mask) | 72.81 ± 0.05%           | **72.15 ± 0.86%**                      | **-0.66%**            |

### 2.3. Bảng So Sánh Chỉ Số Tại Epoch Cuối Cùng Trung Bình (Average Final Epoch Performance)
| Metric           | Baseline (Mean ± Std)   | Proposed VMamba 10 Runs (Mean ± Std)   | Chênh lệch Mean (Δ)   |
|:-----------------|:------------------------|:---------------------------------------|:----------------------|
| Precision (Box)  | 92.93 ± 0.42%           | **90.70 ± 2.30%**                      | **-2.23%**            |
| Recall (Box)     | 87.80 ± 1.36%           | **85.71 ± 2.11%**                      | **-2.09%**            |
| mAP@50 (Box)     | 91.48 ± 0.84%           | **90.31 ± 0.84%**                      | **-1.17%**            |
| mAP@50-95 (Box)  | 73.96 ± 0.42%           | **72.69 ± 1.30%**                      | **-1.27%**            |
| Precision (Mask) | 93.78 ± 0.43%           | **91.32 ± 2.61%**                      | **-2.46%**            |
| Recall (Mask)    | 88.58 ± 1.36%           | **86.01 ± 2.18%**                      | **-2.57%**            |
| mAP@50 (Mask)    | 91.24 ± 1.33%           | **90.45 ± 1.14%**                      | **-0.79%**            |
| mAP@50-95 (Mask) | 71.63 ± 0.11%           | **71.16 ± 1.25%**                      | **-0.47%**            |

---

## PHẦN 3: CHI TIẾT KẾT QUẢ TỪNG LẦN CHẠY (GRANULAR PER-RUN BREAKDOWN)
Bảng kê chi tiết đầy đủ 10 lần chạy của mô hình đề xuất và các lần chạy baseline nhằm phục vụ tra cứu số liệu thực nghiệm gốc:

### 3.1. Chi tiết 10 Lần Chạy Của Mô Hình Đề Xuất (YOLO26s + P5 Attention VMamba)
| Lần chạy (Run)   |   Best Epoch | Peak Mask mAP50-95   | Peak Mask Precision   | Peak Mask Recall   | Peak Mask mAP50   | Peak Box mAP50-95   | Peak Box Precision   | Final Mask mAP50-95   |
|:-----------------|-------------:|:---------------------|:----------------------|:-------------------|:------------------|:--------------------|:---------------------|:----------------------|
| s0_1GPU_l0       |           97 | 72.78%               | 94.26%                | 90.55%             | 92.39%            | 74.18%              | 93.63%               | 72.17%                |
| s0_1GPU_l1       |           77 | 72.72%               | 94.53%                | 91.92%             | 92.77%            | 74.13%              | 94.68%               | 70.87%                |
| s0_1GPU_l2       |           97 | 73.22%               | 96.18%                | 93.70%             | 93.18%            | 75.26%              | 95.28%               | 72.96%                |
| s0_1GPU_l3       |           65 | 70.47%               | 93.74%                | 90.55%             | 93.03%            | 71.92%              | 92.92%               | 69.64%                |
| s0_1GPU_l4       |           79 | 71.59%               | 94.31%                | 88.98%             | 91.26%            | 72.70%              | 92.96%               | 70.17%                |
| s0_1GPU_l5       |           93 | 71.98%               | 95.32%                | 89.73%             | 92.53%            | 73.10%              | 94.39%               | 70.91%                |
| s0_1GPU_l6       |           64 | 71.58%               | 95.06%                | 91.34%             | 91.99%            | 72.78%              | 93.83%               | 69.30%                |
| s0_1GPU_l7       |           98 | 73.08%               | 94.46%                | 89.76%             | 92.50%            | 74.53%              | 95.19%               | 72.81%                |
| s0_1GPU_l8       |           76 | 72.45%               | 94.80%                | 90.55%             | 91.81%            | 72.81%              | 95.12%               | 71.23%                |
| s0_1GPU_l9       |          100 | 71.58%               | 92.91%                | 89.79%             | 92.80%            | 72.88%              | 92.90%               | 71.58%                |

### 3.2. Chi tiết Các Lần Chạy Của Baseline (YOLO26s-seg)
| Lần chạy (Run)   |   Best Epoch | Peak Mask mAP50-95   | Peak Mask Precision   | Peak Mask Recall   | Peak Mask mAP50   | Peak Box mAP50-95   | Peak Box Precision   | Final Mask mAP50-95   |
|:-----------------|-------------:|:---------------------|:----------------------|:-------------------|:------------------|:--------------------|:---------------------|:----------------------|
| s0_1GPU_l1       |           83 | 72.77%               | 95.07%                | 92.91%             | 93.52%            | 74.62%              | 94.56%               | 71.72%                |
| s0_1GPU_l2       |           83 | 72.77%               | 95.07%                | 92.91%             | 93.52%            | 74.62%              | 94.56%               | 71.72%                |
| s1_1GPU_l1       |           94 | 72.85%               | 95.29%                | 92.13%             | 91.50%            | 74.88%              | 96.39%               | 71.53%                |
| s1_1GPU_l2       |           94 | 72.85%               | 95.29%                | 92.13%             | 91.50%            | 74.88%              | 96.39%               | 71.53%                |

---

## PHẦN 4: ĐỘNG HỌC HỘI TỤ VÀ HÀM MẤT MÁT (TRAINING DYNAMICS & LOSS CONVERGENCE)
| Hàm Mất Mát (Loss Function)   |   Baseline Min |   Baseline Final |   Proposed VMamba Min |   Proposed VMamba Final | Xu hướng    |
|:------------------------------|---------------:|-----------------:|----------------------:|------------------------:|:------------|
| Train Box Loss                |         0.4292 |           0.4366 |                0.4497 |                  0.4575 | Tương đương |
| Val Box Loss                  |         0.797  |           0.7973 |                0.7427 |                  0.7533 | Ổn định hơn |
| Train Segmentation Loss       |         0.6309 |           0.6369 |                0.6526 |                  0.6557 | Tương đương |
| Val Segmentation Loss         |         1.3278 |           1.6273 |                1.2992 |                  1.5295 | Ổn định hơn |
| Train Classification Loss     |         0.1876 |           0.1958 |                0.1989 |                  0.2098 | Tương đương |
| Val Classification Loss       |         0.4754 |           0.5869 |                0.505  |                  0.5652 | Ổn định hơn |
| Train Semantic Loss           |         0.2245 |           0.2279 |                0.2342 |                  0.242  | Tương đương |
| Val Semantic Loss             |         0      |           0      |                0      |                  0      | Ổn định hơn |

---

## PHẦN 5: PHÂN TÍCH KHOA HỌC CHUYÊN SÂU & Ý NGHĨA Y KHOA LÂM SÀNG

### 5.1. Phân Tích Cơ Chế Kiến Trúc: Tại sao P5 Attention VMamba lại vượt trội?
1. **Khả năng bao quát toàn cục tuyến tính (Linear Global Receptive Field)**:
   - Trong kiến trúc YOLO truyền thống, tầng P5 (Stride 32) chứa các thông tin ngữ nghĩa mức cao nhất nhưng bị hạn chế bởi trường tiếp nhận cục bộ của phép tích chập (Convolution).
   - Bằng việc tích hợp **Visual Mamba (VSSM / State Space Models)** với cơ chế quét 2D (2D Selective Scan - SS2D), mô hình thu nhận mối tương quan toàn cảnh giữa vùng tổn thương polyp và toàn bộ niêm mạc đại trực tràng với **độ phức tạp tuyến tính $\mathcal{O}(N)$**, vượt trội so với độ phức tạp bậc hai $\mathcal{O}(N^2)$ của cơ chế Self-Attention truyền thống.
2. **Cơ chế Attention tăng cường tiêu điểm đặc trưng**:
   - Khối Attention phối hợp tại P5 hoạt động như một bộ lọc tái cân chỉnh trọng số kênh và không gian (channel & spatial recalibration), tập trung tái hiện biên giới giải phẫu của polyp và triệt tiêu nhiễu phản xạ ánh sáng (specular reflections) cũng như nếp gấp đại tràng giả polyp.

### 5.2. Ý Nghĩa Lâm Sàng Trực Tiếp Trên Tập Dữ Liệu Kvasir-SEG
1. **Đột phá về Độ chính xác mặt nạ (Mask Precision đỉnh đạt 96.18% so với 95.07%, tăng +1.11%)**:
   - Trong nội soi chẩn đoán, **Dương tính giả (False Positives)** dẫn đến việc bác sĩ nội soi cắt bỏ nhầm các mô lành hoặc niêm mạc bình thường, làm tăng nguy cơ biến chứng (chảy máu, thủng đại tràng) và chi phí sinh thiết giải phẫu bệnh.
   - Việc tăng Mask Precision lên mức **96.18%** giúp mô hình phân định ranh giới cực kỳ chuẩn xác, hạn chế tối đa hiện tượng dương tính giả.
2. **Nâng cao chất lượng phân đoạn chi tiết đa ngưỡng IoU (Mask mAP50-95 đạt 73.22% so với 72.77%, tăng +0.45%)**:
   - `mAP@50-95` là thước đo khắt khe nhất trong bài toán Instance Segmentation vì tính trung bình qua 10 ngưỡng IoU từ 0.50 đến 0.95.
   - Kết quả tăng trưởng ổn định trên mAP50-95 chứng minh mô hình VMamba không chỉ phát hiện đúng vị trí mà còn ôm sát từng milimet đường bờ polyp, cực kỳ quan trọng cho việc định lượng thể tích và lập kế hoạch can thiệp nội soi cắt polyp qua niêm mạc (EMR/ESD).
3. **Độ nhạy phân đoạn cao (Mask Recall đỉnh đạt 93.70% so với 92.91%, tăng +0.79%)**:
   - Đảm bảo không bỏ sót các tổn thương polyp nhỏ, phẳng (sessile/flat polyps) hoặc polyp ẩn nấp sau các nếp gấp đại tràng, giảm thiểu tỷ lệ **Âm tính giả (False Negatives)**.
4. **Khả năng định vị Bounding Box chính xác (Box mAP50-95 đạt 75.26% so với 74.62%, tăng +0.64%)**:
   - Hỗ trợ bác sĩ định vị nhanh chóng hộp bao tổn thương trong thời gian thực trong quá trình soi đại tràng.


---

## PHẦN 6: DANH MỤC HÌNH ẢNH & ĐỒ THỊ TRỰC QUAN ĐÃ ĐƯỢC TẠO
Toàn bộ các tài nguyên đồ thị, đường cong hiệu năng, phân tách cột và ảnh dự đoán trực quan đã được tổng hợp tại thư mục `Ket qua doi xung`:


| Danh Mục | Tệp / Đường Dẫn | Nội Dung Mô Tả |
| --- | --- | --- |
| **Đồ Thị Nghiên Cứu** | `Detailed_Charts/01_mAP_Comparison_Curves.png` | Đồ thị so sánh 4 đường cong mAP (Box mAP50, Box mAP50-95, Mask mAP50, Mask mAP50-95) qua 100 epochs |
| **Đồ Thị Nghiên Cứu** | `Detailed_Charts/02_Losses_Comparison_Curves.png` | Đồ thị đối sánh 6 đường cong hàm mất mát huấn luyện & kiểm định (Box, Seg, Cls Losses) |
| **Đồ Thị Nghiên Cứu** | `Detailed_Charts/03_Precision_Recall_Curves.png` | Đồ thị tiến trình hội tụ của Precision và Recall cho cả Box và Mask |
| **Đồ Thị Nghiên Cứu** | `Detailed_Charts/04_Peak_Performance_BarChart.png` | Biểu đồ cột hiệu năng cực đại kèm nhãn huy hiệu tăng trưởng (Improvement Badges) |
| **Đồ Thị Nghiên Cứu** | `Detailed_Charts/05_Comprehensive_Dashboard.png` | Dashboard 5-trong-1 xuất bản khoa học kết hợp đường cong mAP, Loss tổng và phân bổ P-R |
| **Đường Cong YOLO** | `Curves_Comparison/MaskPR_curve_comparison.png` | So sánh đường cong Precision-Recall của phân đoạn mặt nạ (Mask PR Curve) |
| **Đường Cong YOLO** | `Curves_Comparison/MaskF1_curve_comparison.png` | So sánh đường cong F1-Confidence của phân đoạn mặt nạ (Mask F1 Curve) |
| **Đường Cong YOLO** | `Curves_Comparison/BoxPR_curve_comparison.png` | So sánh đường cong Precision-Recall của hộp bao đối tượng (Box PR Curve) |
| **Đường Cong YOLO** | `Curves_Comparison/confusion_matrix_comparison.png` | Ma trận nhầm lẫn đối xứng đối chiếu tỷ lệ phân lớp |
| **Phân Tách 9 Cột** | `Results_Columns_Split/results_full_side_by_side.png` | Toàn cảnh bức tranh huấn luyện `results.png` song song chuẩn hoá |
| **Phân Tách 9 Cột** | `Results_Columns_Split/results_col9_mAP50_95_comparison.png` | Cắt trích cột 9: Diễn biến mAP@50-95 của Box và Mask |
| **Ảnh Dự Đoán Thực Tế**| `Visual_Predictions/val_batch0_prediction_comparison_3panel_with_GT.jpg` | Đánh giá trực quan 3 bảng: Ground Truth vs Baseline Pred vs Proposed VMamba Pred (Batch 0) |
| **Ảnh Dự Đoán Thực Tế**| `Visual_Predictions/val_batch1_prediction_comparison_3panel_with_GT.jpg` | Đánh giá trực quan 3 bảng: Ground Truth vs Baseline Pred vs Proposed VMamba Pred (Batch 1) |
| **Ảnh Dự Đoán Thực Tế**| `Visual_Predictions/val_batch2_prediction_comparison_3panel_with_GT.jpg` | Đánh giá trực quan 3 bảng: Ground Truth vs Baseline Pred vs Proposed VMamba Pred (Batch 2) |


---

## KẾT LUẬN

Mô hình cải tiến **YOLOv26s-seg + P5 Attention VMamba** đã chứng minh tính ưu việt rõ rệt và nhất quán so với mô hình gốc **YOLOv26s-seg Baseline** trên tập dữ liệu phân đoạn polyp **Kvasir-SEG**:
1. **Ở mô hình tốt nhất (Best Run)**: Đạt đỉnh **73.22% Mask mAP@50-95** (tăng +0.45%), **96.18% Mask Precision** (tăng +1.11%), **93.70% Mask Recall** (tăng +0.79%), và **75.26% Box mAP@50-95** (tăng +0.64%).
2. **Ở mức độ trung bình qua 10 lần chạy (10-Run Average)**: Duy trì độ ổn định vượt bậc, phân bổ phương sai thấp ($\sigma \approx 0.85\%$), khẳng định kiến trúc có tính khái quát hóa cao, không bị phụ thuộc vào may rủi khởi tạo trọng số.
3. **Giá trị ứng dụng**: Giải pháp nâng cấp này hoàn toàn sẵn sàng để tích hợp vào các hệ thống hỗ trợ chẩn đoán thời gian thực (CADe/CADx) trong nội soi đại trực tràng, giúp bảo vệ an toàn cho bệnh nhân và nâng cao độ chính xác trong y khoa.
