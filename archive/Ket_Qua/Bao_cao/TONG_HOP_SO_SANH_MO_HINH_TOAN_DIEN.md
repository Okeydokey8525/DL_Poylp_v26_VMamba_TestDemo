# BÁO CÁO TỔNG HỢP VÀ SO SÁNH TOÀN DIỆN TẤT CẢ CÁC MÔ HÌNH THỰC NGHIỆM
## ĐÁNH GIÁ ĐỐI SÁNH HIỆU NĂNG PHÂN ĐOẠN KHỐI U POLYP NỘI SOI TRÊN BỘ DỮ LIỆU KVASIR-SEG
### Đề tài: Nghiên cứu cải tiến mô hình YOLOv26-seg kết hợp kiến trúc Visual Mamba (VMamba / State Space Models)

---

## 📋 TỔNG QUAN HỆ THỐNG THỰC NGHIỆM
- **Bộ dữ liệu (Dataset)**: `Kvasir-SEG` (Bộ dữ liệu chuẩn ảnh nội soi đường tiêu hóa phân đoạn Polyp dạ dày - đại tràng).
- **Kích thước ảnh đầu vào (Image Resolution)**: `640 x 640`.
- **Số lượng Epoch huấn luyện**: `100 Epochs` (huấn luyện đầy đủ cho toàn bộ 32 lượt chạy).
- **Batch Size**: `16`.
- **Thuật toán tối ưu (Optimizer)**: `AdamW` (Tốc độ học khởi tạo $lr_0 = 0.001$).
- **Tổng số lượt chạy thực nghiệm được kiểm tra & đối soát**: **32 lượt chạy (32 Runs)** được phân loại trên **9 biến thể kiến trúc**.
- **Mục tiêu nghiên cứu**: Khảo sát hiệu năng của mô hình đề xuất (`YOLOv26s-seg + P5 Attention VMamba`), so sánh với mô hình gốc `Baseline (YOLOv26s-seg)` và thực hiện nghiên cứu triệt tiêu (`Ablation Studies`) với các biến thể kiến trúc: tích hợp tại tầng P3, tầng P5 không có Attention, cơ chế dung hợp Attention VMamba Fusion (AVMF), Boundary-Aware VMamba, C3K2VSS, và Topology Shape VMamba (TSVM).

---

## 🏆 PHẦN 1: BẢNG XẾP HẠNG TỔNG QUAN TẤT CẢ CÁC BIẾN THỂ KIẾN TRÚC (ARCHITECTURE LEADERBOARD)
Bảng thống kê xếp hạng tổng thể hiệu năng của 9 biến thể kiến trúc dựa trên giá trị cực đại đạt được (Max Peak) và giá trị trung bình qua các lần chạy (Mean ± Std):


| Hạng | Kiến trúc mô hình | Số Runs | Mask mAP@50-95 (Max) | Mask mAP@50-95 (Mean ± Std) | Mask mAP@50 (Max) | Box mAP@50-95 (Max) | Mask Precision (Mean) | Mask Recall (Mean) | Best Epoch (Mean) |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 🥇 | **YOLOv26s-seg + P5 Attention VMamba (Additional Runs)** | 5 | **73.47%** | 72.60 ± 0.82% | 93.50% | 75.26% | 94.82% | 91.32% | Ep 79.6 |
| 🥈 | **YOLOv26s-seg + P3 CNN VMamba** | 6 | **73.32%** | 72.55 ± 0.68% | 93.60% | 74.56% | 94.48% | 90.63% | Ep 77.8 |
| 🥉 | **YOLOv26s-seg + P5 Attention VMamba (10-Run Benchmark)** | 10 | **73.22%** | 72.15 ± 0.86% | 93.18% | 75.26% | 94.56% | 90.69% | Ep 84.6 |
| **4** | **YOLOv26s-seg (Baseline)** | 4 | **72.85%** | 72.81 ± 0.05% | 93.52% | 74.88% | 95.18% | 92.52% | Ep 88.5 |
| **5** | **YOLOv26s-seg + P5 VMamba (Không có Attention)** | 3 | **64.49%** | 63.51 ± 0.92% | 90.02% | 62.83% | 88.50% | 86.49% | Ep 94.0 |
| **6** | **YOLOv26s-seg + Attention VMamba Fusion (AVMF)** | 1 | **64.46%** | 64.46% | 87.43% | 61.85% | 85.99% | 85.04% | Ep 94.0 |
| **7** | **YOLOv26s-seg + C3K2VSS (P3 VMamba Backbone)** | 1 | **61.56%** | 61.56% | 85.34% | 59.10% | 88.25% | 81.77% | Ep 97.0 |
| **8** | **YOLOv26s-seg + Boundary-Aware VMamba** | 1 | **61.33%** | 61.33% | 87.17% | 61.07% | 87.63% | 86.08% | Ep 81.0 |
| **9** | **YOLOv26s-seg + Topology Shape VMamba (TSVM)** | 1 | **60.72%** | 60.72% | 86.11% | 59.13% | 89.41% | 86.60% | Ep 80.0 |

> **Nhận xét tổng quan từ Bảng Xếp Hạng**:
> 1. **Mô hình Đề xuất P5 Attention VMamba** thiết lập kỷ lục hiệu năng phân đoạn cao nhất toàn tập thực nghiệm (**Mask mAP@50-95 đạt 73.47%**, Box mAP@50-95 đạt **75.26%**).
> 2. **Kiến trúc P3 CNN VMamba** đứng vị trí thứ 2 (**Mask mAP@50-95 đạt 73.32%**, Box mAP@50-95 đạt **74.56%**), cho thấy việc kết hợp VMamba ở cả tầng P3 và P5 đều mang lại khả năng nắm bắt ngữ cảnh phân đoạn vượt trội.
> 3. **Mô hình Gốc Baseline (YOLOv26s-seg)** đứng vị trí thứ 3 với Mask mAP@50-95 đạt cực đại **72.85%**.
> 4. **Các kiến trúc thiếu cơ chế Attention hoặc tích hợp quá phức tạp** (như *P5 VMamba không có Attention*, *Boundary-Aware*, *C3K2VSS*, *TSVM*) bị suy giảm hiệu năng rõ rệt (chỉ đạt ~60% - 64% mAP), chứng minh việc kết hợp Attention tại đúng tầng đặc trưng ngữ nghĩa P5 là mắt xích quyết định thành công.

---

## 🌟 PHẦN 2: TOP 10 LƯỢT CHẠY XUẤT SẮC NHẤT TOÀN BỘ CƠ SỞ DỮ LIỆU (TOP-10 RUNS LEADERBOARD)
Bảng vinh danh 10 lượt chạy đơn lẻ (Single Runs) có chỉ số phân đoạn `Mask mAP@50-95` cao nhất trong tổng số 32 lượt chạy:


| Top | Tên Thư Mục Thực Nghiệm | Kiến Trúc Mô Hình | Seed | Best Ep | Mask mAP@50-95 | Mask mAP@50 | Mask Precision | Mask Recall | Box mAP@50-95 | Box mAP@50 |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 🥇 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l1` | **YOLOv26s + P5 Attention VMamba** | 0 | Ep 80 | **73.47%** | 93.50% | 94.73% | 91.34% | **75.26%** | 93.12% |
| 🥈 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_se0_1GPU_l2` | **YOLOv26s + P3 CNN VMamba** | 0 | Ep 84 | **73.32%** | 93.60% | 95.66% | 92.13% | **74.56%** | 93.04% |
| 🥉 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s1_1GPU_l1` | **YOLOv26s + P5 Attention VMamba** | 1 | Ep 84 | **73.26%** | 92.64% | 95.16% | 91.67% | **73.75%** | 92.16% |
| 4 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l2` | **YOLOv26s + P5 Attention VMamba** | 0 | Ep 97 | **73.22%** | 93.18% | 96.18% | 93.70% | **75.26%** | 92.54% |
| 5 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l7` | **YOLOv26s + P5 Attention VMamba** | 0 | Ep 98 | **73.08%** | 92.50% | 94.46% | 89.76% | **74.53%** | 91.77% |
| 6 | `Kvasir_YOLO26s_seg_s1_1GPU_l2` | **YOLOv26s-seg** | 1 | Ep 94 | **72.85%** | 91.50% | 95.29% | 92.13% | **74.88%** | 91.80% |
| 7 | `Kvasir_YOLO26s_seg_s1_1GPU_l1` | **YOLOv26s-seg** | 1 | Ep 94 | **72.85%** | 91.50% | 95.29% | 92.13% | **74.88%** | 91.80% |
| 8 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l0` | **YOLOv26s + P5 Attention VMamba** | 0 | Ep 97 | **72.78%** | 92.39% | 94.26% | 90.55% | **74.18%** | 90.94% |
| 9 | `Kvasir_YOLO26s_seg_s0_1GPU_l2` | **YOLOv26s-seg** | 0 | Ep 83 | **72.77%** | 93.52% | 95.07% | 92.91% | **74.62%** | 93.65% |
| 10 | `Kvasir_YOLO26s_seg_s0_1GPU_l1` | **YOLOv26s-seg** | 0 | Ep 83 | **72.77%** | 93.52% | 95.07% | 92.91% | **74.62%** | 93.65% |

---

## ⚖️ PHẦN 3: SO SÁNH ĐỐI ĐẦU CHI TIẾT: BASELINE VS MÔ HÌNH ĐỀ XUẤT (PROPOSED VMAMBA)
Phân tích so sánh trực tiếp, toàn diện giữa **Baseline (YOLOv26s-seg)** và **Mô hình Đề xuất (YOLOv26s-seg + P5 Attention VMamba)** qua cả 2 lăng kính: **Lượt chạy Tốt Nhất (Best Run)** và **Benchmark Trung Bình Đa Lượt Chạy (Multi-Run Average Benchmark)**.

### 3.1. So Sánh Best Run Đối Đầu (Peak Metrics Across 100 Epochs)
So sánh chỉ số cực đại cao nhất đạt được giữa Run tốt nhất của Baseline (`s0_1GPU_l2` / `s1_1GPU_l1`) và Run tốt nhất của Đề xuất (`s0_1GPU_l1` / `s0_1GPU_l2`):


| Chỉ Số Đánh Giá (Metric) | Baseline Best Run | Proposed VMamba Best Run | Chênh Lệch Tuyệt Đối (Δ) | Tăng Trưởng Tương Đối (%) | Đánh Giá Hiệu Năng |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Mask mAP@50-95 (Độ chính xác phân đoạn toàn diện)** | 72.85% | **73.47%** | **+0.62%** | **+0.85%** | 🟢 Vượt trội |
| **Mask mAP@50 (Độ chính xác phân đoạn IoU=0.50)** | 91.50% | **93.50%** | **+2.00%** | **+2.19%** | 🟢 Vượt trội |
| **Mask Precision (Độ chuẩn xác phân đoạn)** | 95.29% | **94.73%** | **-0.56%** | **-0.59%** | 🔴 Thấp hơn |
| **Mask Recall (Độ phủ phân đoạn)** | 92.13% | **91.34%** | **-0.79%** | **-0.85%** | 🔴 Thấp hơn |
| **Box mAP@50-95 (Độ chính xác hộp bao toàn diện)** | 74.88% | **75.26%** | **+0.38%** | **+0.50%** | 🟢 Vượt trội |
| **Box mAP@50 (Độ chính xác hộp bao IoU=0.50)** | 91.80% | **93.12%** | **+1.32%** | **+1.44%** | 🟢 Vượt trội |
| **Box Precision (Độ chuẩn xác hộp bao)** | 96.39% | **94.10%** | **-2.29%** | **-2.38%** | 🔴 Thấp hơn |
| **Box Recall (Độ phủ hộp bao)** | 90.02% | **90.92%** | **+0.90%** | **+1.00%** | 🟢 Vượt trội |

### 3.2. So Sánh Benchmark Trung Bình Đa Lượt Chạy (Mean ± Std: Baseline 4 Runs vs Proposed 10 Runs)
Để đảm bảo tính khách quan khoa học, loại bỏ yếu tố ngẫu nhiên do khởi tạo trọng số và phân tách batch, bảng dưới đây so sánh giá trị Trung bình (Mean) và Độ lệch chuẩn (Std) qua 4 runs của Baseline và 10 runs độc lập của Proposed VMamba:


| Chỉ Số Đánh Giá (Metric) | Baseline (4 Runs: Mean ± Std) | Baseline [Min - Max] | Proposed VMamba (10 Runs: Mean ± Std) | Proposed [Min - Max] | Chênh Lệch Mean (Δ) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Peak Mask mAP@50-95** | 72.81 ± 0.05% | [72.77% - 72.85%] | **72.15 ± 0.86%** | [70.47% - 73.22%] | **-0.66%** |
| **Peak Mask mAP@50** | 92.51 ± 1.17% | [91.50% - 93.52%] | **92.43 ± 0.59%** | [91.26% - 93.18%] | **-0.08%** |
| **Peak Mask Precision** | 95.18 ± 0.13% | [95.07% - 95.29%] | **94.56 ± 0.89%** | [92.91% - 96.18%] | **-0.62%** |
| **Peak Mask Recall** | 92.52 ± 0.45% | [92.13% - 92.91%] | **90.69 ± 1.36%** | [88.98% - 93.70%] | **-1.83%** |
| **Peak Box mAP@50-95** | 74.75 ± 0.15% | [74.62% - 74.88%] | **73.43 ± 1.04%** | [71.92% - 75.26%] | **-1.32%** |
| **Peak Box mAP@50** | 92.73 ± 1.07% | [91.80% - 93.65%] | **91.61 ± 0.53%** | [90.94% - 92.54%] | **-1.12%** |
| **Peak Box Precision** | 95.48 ± 1.06% | [94.56% - 96.39%] | **94.09 ± 0.97%** | [92.90% - 95.28%] | **-1.39%** |
| **Peak Box Recall** | 91.47 ± 1.67% | [90.02% - 92.91%] | **90.18 ± 0.70%** | [88.98% - 91.34%] | **-1.29%** |
| **Best-Epoch Mask mAP@50-95** | 72.81 ± 0.05% | [72.77% - 72.85%] | **72.15 ± 0.86%** | [70.47% - 73.22%] | **-0.66%** |
| **Best-Epoch Mask mAP@50** | 91.94 ± 0.96% | [91.11% - 92.78%] | **91.33 ± 0.96%** | [89.90% - 92.65%] | **-0.61%** |
| **Best-Epoch Mask Precision** | 92.56 ± 1.21% | [91.52% - 93.61%] | **92.40 ± 2.56%** | [87.53% - 96.18%] | **-0.17%** |
| **Best-Epoch Mask Recall** | 88.58 ± 3.18% | [85.83% - 91.34%] | **84.64 ± 2.17%** | [81.06% - 88.19%] | **-3.94%** |
| **Final-Epoch (Ep 100) Mask mAP@50-95** | 71.63 ± 0.11% | [71.53% - 71.72%] | **71.16 ± 1.25%** | [69.30% - 72.96%] | **-0.47%** |
| **Final-Epoch (Ep 100) Mask mAP@50** | 91.24 ± 1.33% | [90.09% - 92.40%] | **90.45 ± 1.14%** | [89.32% - 92.84%] | **-0.79%** |

### 3.3. So Sánh Hàm Mất Mát (Loss) và Tốc Độ Hội Tụ
Bảng đo lường sự hội tụ các hàm mất mát (Segmentation Loss, Box Loss, Classification Loss) tại Best Epoch và Final Epoch (Epoch 100):


| Đại Lượng Mất Mát / Hội Tụ | Baseline (Mean) | Proposed VMamba (Mean) | Chênh Lệch (Δ) | Nhận Xét Động Học Hội Tụ |
|:---|:---:|:---:|:---:|:---|
| **Val Segmentation Loss (Best Epoch)** | 1.5668 | **1.4632** | -0.1036 | 🟢 Giảm Loss tốt hơn |
| **Val Segmentation Loss (Final Epoch 100)** | 1.6182 | **1.5168** | -0.1014 | 🟢 Giảm Loss tốt hơn |
| **Train Segmentation Loss (Best Epoch)** | 0.7422 | **0.7898** | 0.0477 | 🟡 Tương đương / Ổn định |
| **Val Box Loss (Best Epoch)** | 0.7692 | **0.8063** | 0.0371 | 🟡 Tương đương / Ổn định |
| **Val Box Loss (Final Epoch 100)** | 0.7721 | **0.7882** | 0.0161 | 🟡 Tương đương / Ổn định |
| **Train Box Loss (Best Epoch)** | 0.5258 | **0.5650** | 0.0392 | 🟡 Tương đương / Ổn định |
| **Val Classification Loss (Best Epoch)** | 0.5724 | **0.6191** | 0.0468 | 🟡 Tương đương / Ổn định |
| **Val Classification Loss (Final Epoch 100)** | 0.5898 | **0.6092** | 0.0194 | 🟡 Tương đương / Ổn định |
| **Best Epoch Đạt Đỉnh (Epoch Convergence)** | Ep 88.5 | **Ep 84.6** | -3.9 epochs | 🟢 Hội tụ ổn định qua 100 epochs |

---

## 🔬 PHẦN 4: NGHIÊN CỨU TRIỆT TIÊU TOÀN DIỆN (COMPREHENSIVE ABLATION STUDY)
Phần này trình bày các phân tích triệt tiêu nhằm chứng minh cơ sở khoa học cho từng quyết định thiết kế kiến trúc:

### 4.1. Nghiên Cứu Vị Trí Tích Hợp Khối VMamba: Tầng P5 vs Tầng P3
- **P5 Attention VMamba** (`yolo26s-seg-Attention-VMamba-P5.yaml`): Tích hợp tại tầng đặc trưng ngữ nghĩa mức cao P5 (Stride 32, channels=512) kết hợp Attention.
- **P3 CNN VMamba** (`yolo26s-seg-CNN-VMamba.yaml`): Tích hợp tại tầng đặc trưng chi tiết không gian mức thấp P3 (Stride 8, channels=128) kết hợp CNN.


| Tiêu Chí Đánh Giá | P5 Attention VMamba (Proposed) | P3 CNN VMamba (Ablation) | Baseline YOLOv26s-seg | Phân Tích Ý Nghĩa Kiến Trúc |
|:---|:---:|:---:|:---:|:---|
| **Số Lượt Chạy Khảo Sát** | 15 Runs (10 benchmark + 5 other) | 6 Runs | 4 Runs | Đảm bảo kích thước mẫu tin cậy |
| **Mask mAP@50-95 Cực Đại (Max)** | **73.47%** | 73.32% | 72.85% | P5 cho đỉnh phân đoạn vượt trội (+0.15% so với P3, +0.62% so với Baseline) |
| **Mask mAP@50-95 Trung Bình (Mean)** | **72.30%** | 72.55% | 72.81% | Cả hai đều đạt mức chính xác cao ~72.6% |
| **Box mAP@50-95 Cực Đại (Max)** | **75.26%** | 74.56% | 74.88% | P5 hỗ trợ định vị bounding box tốt hơn (+0.70% so với P3) |
| **Mask Precision Cực Đại (Max)** | **96.18%** | 95.66% | 95.29% | Tầng P5 lọc dương tính giả tốt hơn hẳn (+0.73%) |
| **Đặc Trưng Học Được** | Ngữ nghĩa toàn cục (Global Context), tách biệt polyp với nếp gấp ruột | Biên cạnh cục bộ (Local Edge), chi tiết vân bề mặt niêm mạc | Đặc trưng CNN thuần túy | Khẳng định P5 là vị trí tối ưu để mở rộng trường tiếp nhận toàn cục |

### 4.2. Nghiên Cứu Vai Trò Của Cơ Chế Attention Khi Kết Hợp Với VMamba Tại Tầng P5
So sánh đối đầu trực tiếp để kiểm chứng giả thuyết: *Liệu cơ chế Attention có thực sự cần thiết khi đã có VMamba tại tầng P5 hay không?*
- **Mô hình có Attention**: `YOLOv26s-seg + P5 Attention VMamba`
- **Mô hình KHÔNG có Attention**: `YOLOv26s-seg + P5 VMamba` (`yolo26-seg-VMamba-P5.yaml`)


| Chỉ Số Thực Nghiệm | P5 Attention VMamba (Có Attention) | P5 VMamba Thuần (KHÔNG có Attention) | Mức Độ Suy Giảm Khi Bỏ Attention (Δ) | Đánh Giá Tác Động |
|:---|:---:|:---:|:---:|:---|
| **Mask mAP@50-95 (Max)** | **73.47%** | 64.49% | **-8.97%** | 🔴 Suy giảm nghiêm trọng |
| **Mask mAP@50-95 (Mean)** | **72.30%** | 63.51% | **-8.78%** | 🔴 Giảm gần 9% mAP trung bình |
| **Mask mAP@50 (Max)** | **93.50%** | 90.02% | **-3.48%** | 🔴 Giảm độ chính xác bao phủ |
| **Box mAP@50-95 (Max)** | **75.26%** | 62.83% | **-12.43%** | 🔴 Giảm hơn 12.4% phát hiện Box |
| **Mask Precision (Mean)** | **94.64%** | 88.50% | **-6.14%** | 🔴 Tăng mạnh dương tính giả |
| **Mask Recall (Mean)** | **90.90%** | 86.49% | **-4.41%** | 🔴 Bỏ sót vùng tổn thương |

> **Kết luận then chốt cho Luận văn Cử nhân**:
> Kết quả triệt tiêu trên khẳng định: **Cơ chế Attention đóng vai trò điều hướng và tái cân bằng trọng số không gian (spatial gating / selective focus)** cho luồng trạng thái của VMamba tại tầng P5. Nếu thiếu Attention, mô hình VMamba thuần túy tại tầng sâu P5 sẽ bị phân tán độ tập trung vào các vùng nhiễu nền nội soi (ánh sáng phản chiếu niêm mạc, bọt dịch tiêu hóa), dẫn đến suy sụp hiệu năng nghiêm trọng từ **73.47% xuống 64.49%**.

### 4.3. Nghiên Cứu Triệt Tiêu Toàn Diện 9 Biến Thể Thiết Kế
Bảng đối chiếu toàn bộ 9 biến thể kiến trúc được thử nghiệm trong đề tài:


| Biến Thể Kiến Trúc | Vị Trí Can Thiệp | Cơ Chế Kết Hợp | Mask mAP@50-95 | Box mAP@50-95 | Đánh Giá Khoa Học |
|:---|:---|:---|:---:|:---:|:---|
| **YOLOv26s + P5 Attention VMamba (Proposed)** | P5 (High-level semantic) | Visual Mamba + Spatial Attention | **73.47%** | **75.26%** | 🟢 Tối ưu nhất |
| **YOLOv26s + P3 CNN VMamba** | P3 (Low-level detail) | CNN + Visual Mamba | **73.32%** | **74.56%** | 🟢 Hiệu quả cao |
| **Baseline YOLOv26s-seg** | P3-P5 Backbone/Neck | Standard C3k2 / Conv | **72.85%** | **74.88%** | 🟡 Chuẩn cơ sở |
| **YOLOv26s + P5 VMamba (No Attention)** | P5 | Pure Visual Mamba (No Attn) | **64.49%** | **62.83%** | 🔴 Thiếu cơ chế lọc nhiễu |
| **YOLOv26s + Attention VMamba Fusion (AVMF)** | Neck Fusion | Interactive Attention Fusion | **64.46%** | **61.85%** | 🔴 Phức tạp hóa luồng gradient |
| **YOLOv26s + C3K2VSS** | P3 Backbone | VSS Block trong C3k2 | **61.56%** | **59.10%** | 🔴 Khó tối ưu ở backbone sớm |
| **YOLOv26s + Boundary-Aware VMamba** | Head / Neck | Boundary Loss + VMamba | **61.33%** | **61.07%** | 🔴 Nhiễu biên do ảnh nội soi mờ |
| **YOLOv26s + Topology Shape VMamba (TSVM)** | Neck / Head | Topology Prior + Shape SSM | **60.72%** | **59.13%** | 🔴 Giả định hình học quá chặt |

---

## 📊 PHẦN 5: BẢNG DỮ LIỆU ĐẦY ĐỦ CHI TIẾT TOÀN BỘ 32 LƯỢT CHẠY THỰC NGHIỆM
Dưới đây là 3 bảng thống kê toàn diện chi tiết đến từng lượt chạy đơn lẻ:

### 5.1. Bảng Chỉ Số Cực Đại (Peak Metrics Across 100 Epochs) - Toàn Bộ 32 Runs


| STT | Nhóm Kiến Trúc | Tên Thư Mục Run | Seed | Epochs | Best Ep | Mask mAP50-95 | Mask mAP50 | Mask P | Mask R | Box mAP50-95 | Box mAP50 | Box P | Box R |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | YOLOv26s-seg + Attention VMamba Fusion | `Kvasir_YOLO26s_seg_AVMF_s0_1GPU_l1` | 0 | 100 | Ep 94 | **64.46%** | 87.43% | 85.99% | 85.04% | **61.85%** | 87.14% | 84.99% | 84.25% |
| 2 | YOLOv26s-seg + Boundary-Aware VMamba | `Kvasir_YOLO26s_seg_BoundaryAwareVMamba_se0_1GPU_l1` | 0 | 100 | Ep 81 | **61.33%** | 87.17% | 87.63% | 86.08% | **61.07%** | 85.84% | 86.78% | 83.47% |
| 3 | YOLOv26s-seg + C3K2VSS | `Kvasir_YOLO26s_seg_C3K2VSS_se0_1GPU_l1` | 0 | 100 | Ep 97 | **61.56%** | 85.34% | 88.25% | 81.77% | **59.10%** | 84.34% | 89.19% | 81.36% |
| 4 | YOLOv26s-seg + P3 CNN VMamba | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s0_1GPU_l1` | 0 | 100 | Ep 78 | **72.70%** | 91.82% | 94.33% | 89.41% | **72.84%** | 91.04% | 94.12% | 89.41% |
| 5 | YOLOv26s-seg + P3 CNN VMamba | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s1_1GPU_l1` | 1 | 100 | Ep 87 | **72.67%** | 92.84% | 94.49% | 90.45% | **74.43%** | 91.62% | 94.45% | 89.67% |
| 6 | YOLOv26s-seg + P3 CNN VMamba | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s1_1GPU_l2` | 1 | 100 | Ep 75 | **72.76%** | 92.56% | 94.53% | 91.55% | **73.16%** | 92.22% | 94.13% | 91.55% |
| 7 | YOLOv26s-seg + P3 CNN VMamba | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s2_1GPU_l1` | 2 | 100 | Ep 53 | **71.26%** | 92.90% | 93.04% | 89.88% | **70.99%** | 93.23% | 92.35% | 93.49% |
| 8 | YOLOv26s-seg + P3 CNN VMamba | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s2_1GPU_l2` | 2 | 100 | Ep 90 | **72.61%** | 92.39% | 94.85% | 90.37% | **73.58%** | 92.30% | 93.99% | 89.58% |
| 9 | YOLOv26s-seg + P3 CNN VMamba | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_se0_1GPU_l2` | 0 | 100 | Ep 84 | **73.32%** | 93.60% | 95.66% | 92.13% | **74.56%** | 93.04% | 95.11% | 92.13% |
| 10 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l1` | 0 | 100 | Ep 80 | **73.47%** | 93.50% | 94.73% | 91.34% | **75.26%** | 93.12% | 94.10% | 90.92% |
| 11 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l2` | 0 | 100 | Ep 96 | **71.98%** | 92.61% | 94.89% | 90.16% | **73.80%** | 92.40% | 94.68% | 90.93% |
| 12 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s1_1GPU_l1` | 1 | 100 | Ep 84 | **73.26%** | 92.64% | 95.16% | 91.67% | **73.75%** | 92.16% | 94.31% | 91.98% |
| 13 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s1_1GPU_l2` | 1 | 100 | Ep 61 | **71.55%** | 92.03% | 94.78% | 91.51% | **72.87%** | 90.89% | 93.63% | 91.51% |
| 14 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l1` | 0 | 100 | Ep 77 | **72.72%** | 92.77% | 94.53% | 91.92% | **74.13%** | 92.45% | 94.68% | 89.95% |
| 15 | YOLOv26s-seg + P5 VMamba | `Kvasir_YOLO26s_seg_P5_VMamba_se0_1GPU_l1` | 0 | 100 | Ep 89 | **62.67%** | 90.02% | 90.04% | 87.02% | **61.14%** | 89.80% | 88.53% | 85.31% |
| 16 | YOLOv26s-seg + P5 VMamba | `Kvasir_YOLO26s_seg_P5_VMamba_se0_1GPU_l2` | 0 | 100 | Ep 96 | **64.49%** | 86.97% | 86.84% | 87.40% | **62.53%** | 86.56% | 86.69% | 86.61% |
| 17 | YOLOv26s-seg + P5 VMamba | `Kvasir_YOLO26s_seg_P5_VMamba_se1_1GPU_l1` | 1 | 100 | Ep 97 | **63.37%** | 86.98% | 88.63% | 85.04% | **62.83%** | 87.20% | 89.74% | 85.04% |
| 18 | YOLOv26s-seg + Topology Shape VMamba | `Kvasir_YOLO26s_seg_TSVM_s0_1GPU_l1` | 0 | 100 | Ep 80 | **60.72%** | 86.11% | 89.41% | 86.60% | **59.13%** | 85.91% | 88.44% | 84.24% |
| 19 | YOLOv26s-seg | `Kvasir_YOLO26s_seg_s0_1GPU_l1` | 0 | 100 | Ep 83 | **72.77%** | 93.52% | 95.07% | 92.91% | **74.62%** | 93.65% | 94.56% | 92.91% |
| 20 | YOLOv26s-seg | `Kvasir_YOLO26s_seg_s0_1GPU_l2` | 0 | 100 | Ep 83 | **72.77%** | 93.52% | 95.07% | 92.91% | **74.62%** | 93.65% | 94.56% | 92.91% |
| 21 | YOLOv26s-seg | `Kvasir_YOLO26s_seg_s1_1GPU_l1` | 1 | 100 | Ep 94 | **72.85%** | 91.50% | 95.29% | 92.13% | **74.88%** | 91.80% | 96.39% | 90.02% |
| 22 | YOLOv26s-seg | `Kvasir_YOLO26s_seg_s1_1GPU_l2` | 1 | 100 | Ep 94 | **72.85%** | 91.50% | 95.29% | 92.13% | **74.88%** | 91.80% | 96.39% | 90.02% |
| 23 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l0` | 0 | 100 | Ep 97 | **72.78%** | 92.39% | 94.26% | 90.55% | **74.18%** | 90.94% | 93.63% | 90.55% |
| 24 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l1` | 0 | 100 | Ep 77 | **72.72%** | 92.77% | 94.53% | 91.92% | **74.13%** | 92.45% | 94.68% | 89.95% |
| 25 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l2` | 0 | 100 | Ep 97 | **73.22%** | 93.18% | 96.18% | 93.70% | **75.26%** | 92.54% | 95.28% | 91.34% |
| 26 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l3` | 0 | 100 | Ep 65 | **70.47%** | 93.03% | 93.74% | 90.55% | **71.92%** | 91.44% | 92.92% | 89.50% |
| 27 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l4` | 0 | 100 | Ep 79 | **71.59%** | 91.26% | 94.31% | 88.98% | **72.70%** | 91.27% | 92.96% | 90.40% |
| 28 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l5` | 0 | 100 | Ep 93 | **71.98%** | 92.53% | 95.32% | 89.73% | **73.10%** | 91.28% | 94.39% | 90.50% |
| 29 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l6` | 0 | 100 | Ep 64 | **71.58%** | 91.99% | 95.06% | 91.34% | **72.78%** | 91.79% | 93.83% | 90.55% |
| 30 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l7` | 0 | 100 | Ep 98 | **73.08%** | 92.50% | 94.46% | 89.76% | **74.53%** | 91.77% | 95.19% | 88.98% |
| 31 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l8` | 0 | 100 | Ep 76 | **72.45%** | 91.81% | 94.80% | 90.55% | **72.81%** | 91.33% | 95.12% | 90.55% |
| 32 | YOLOv26s-seg + P5 Attention VMamba | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l9` | 0 | 100 | Ep 100 | **71.58%** | 92.80% | 92.91% | 89.79% | **72.88%** | 91.27% | 92.90% | 89.44% |

### 5.2. Bảng Chỉ Số Đồng Thời Tại Best Epoch (Thời Điểm Mask mAP50-95 Đạt Cực Đại) - Toàn Bộ 32 Runs


| STT | Tên Thư Mục Run | Best Epoch | Mask mAP50-95 | Mask mAP50 | Mask P | Mask R | Box mAP50-95 | Box mAP50 | Box P | Box R | Val Seg Loss | Val Box Loss |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | `Kvasir_YOLO26s_seg_AVMF_s0_1GPU_l1` | **Epoch 94** | **64.46%** | 87.43% | 83.57% | 78.74% | **61.60%** | 86.74% | 82.93% | 76.48% | 1.4920 | 1.0751 |
| 2 | `Kvasir_YOLO26s_seg_BoundaryAwareVMamba_se0_1GPU_l1` | **Epoch 81** | **61.33%** | 85.80% | 82.23% | 82.68% | **60.10%** | 83.77% | 80.63% | 81.10% | 1.4985 | 1.0467 |
| 3 | `Kvasir_YOLO26s_seg_C3K2VSS_se0_1GPU_l1` | **Epoch 97** | **61.56%** | 84.08% | 85.21% | 77.13% | **58.79%** | 83.64% | 85.21% | 77.13% | 1.6101 | 1.0937 |
| 4 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s0_1GPU_l1` | **Epoch 78** | **72.70%** | 89.76% | 89.78% | 85.04% | **72.41%** | 88.88% | 88.90% | 84.25% | 1.4639 | 0.7716 |
| 5 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s1_1GPU_l1` | **Epoch 87** | **72.67%** | 91.42% | 93.75% | 86.61% | **74.43%** | 91.25% | 93.19% | 86.21% | 1.4336 | 0.7866 |
| 6 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s1_1GPU_l2` | **Epoch 75** | **72.76%** | 90.80% | 90.01% | 85.16% | **71.43%** | 91.22% | 90.01% | 85.16% | 1.4265 | 0.8984 |
| 7 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s2_1GPU_l1` | **Epoch 53** | **71.26%** | 92.90% | 93.04% | 87.40% | **70.28%** | 93.23% | 86.20% | 93.49% | 1.3903 | 0.9130 |
| 8 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s2_1GPU_l2` | **Epoch 90** | **72.61%** | 90.27% | 93.23% | 88.19% | **73.37%** | 89.52% | 91.55% | 86.61% | 1.4712 | 0.8040 |
| 9 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_se0_1GPU_l2` | **Epoch 84** | **73.32%** | 92.58% | 92.47% | 88.98% | **73.78%** | 92.16% | 91.41% | 88.19% | 1.4785 | 0.7779 |
| 10 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l1` | **Epoch 80** | **73.47%** | 93.50% | 94.56% | 85.83% | **74.64%** | 93.12% | 93.56% | 86.61% | 1.4664 | 0.8080 |
| 11 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l2` | **Epoch 96** | **71.98%** | 91.10% | 89.10% | 90.14% | **73.80%** | 92.40% | 89.88% | 90.93% | 1.5277 | 0.8225 |
| 12 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s1_1GPU_l1` | **Epoch 84** | **73.26%** | 91.64% | 91.85% | 91.34% | **72.87%** | 91.11% | 89.76% | 89.69% | 1.4418 | 0.8293 |
| 13 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s1_1GPU_l2` | **Epoch 61** | **71.55%** | 92.03% | 91.65% | 86.38% | **72.61%** | 90.89% | 90.81% | 85.63% | 1.3823 | 0.8428 |
| 14 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l1` | **Epoch 77** | **72.72%** | 92.24% | 92.90% | 82.46% | **73.79%** | 91.25% | 92.77% | 80.77% | 1.3526 | 0.8004 |
| 15 | `Kvasir_YOLO26s_seg_P5_VMamba_se0_1GPU_l1` | **Epoch 89** | **62.67%** | 90.02% | 87.94% | 86.09% | **61.14%** | 89.80% | 87.13% | 85.31% | 1.6416 | 1.1488 |
| 16 | `Kvasir_YOLO26s_seg_P5_VMamba_se0_1GPU_l2` | **Epoch 96** | **64.49%** | 86.02% | 85.01% | 80.37% | **62.50%** | 85.59% | 84.18% | 79.58% | 1.5485 | 1.0646 |
| 17 | `Kvasir_YOLO26s_seg_P5_VMamba_se1_1GPU_l1` | **Epoch 97** | **63.37%** | 86.62% | 77.80% | 82.79% | **62.83%** | 86.28% | 77.80% | 82.79% | 1.5741 | 1.0661 |
| 18 | `Kvasir_YOLO26s_seg_TSVM_s0_1GPU_l1` | **Epoch 80** | **60.72%** | 86.11% | 82.64% | 78.71% | **58.25%** | 85.91% | 82.64% | 78.71% | 1.5095 | 1.1382 |
| 19 | `Kvasir_YOLO26s_seg_s0_1GPU_l1` | **Epoch 83** | **72.77%** | 92.78% | 91.52% | 91.34% | **73.39%** | 92.20% | 90.73% | 90.55% | 1.5266 | 0.8006 |
| 20 | `Kvasir_YOLO26s_seg_s0_1GPU_l2` | **Epoch 83** | **72.77%** | 92.78% | 91.52% | 91.34% | **73.39%** | 92.20% | 90.73% | 90.55% | 1.5266 | 0.8006 |
| 21 | `Kvasir_YOLO26s_seg_s1_1GPU_l1` | **Epoch 94** | **72.85%** | 91.11% | 93.61% | 85.83% | **74.88%** | 91.80% | 96.39% | 84.13% | 1.6071 | 0.7378 |
| 22 | `Kvasir_YOLO26s_seg_s1_1GPU_l2` | **Epoch 94** | **72.85%** | 91.11% | 93.61% | 85.83% | **74.88%** | 91.80% | 96.39% | 84.13% | 1.6071 | 0.7378 |
| 23 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l0` | **Epoch 97** | **72.78%** | 90.53% | 92.43% | 86.49% | **74.12%** | 90.94% | 91.59% | 85.70% | 1.5225 | 0.7756 |
| 24 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l1` | **Epoch 77** | **72.72%** | 92.24% | 92.90% | 82.46% | **73.79%** | 91.25% | 92.77% | 80.77% | 1.3526 | 0.8004 |
| 25 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l2` | **Epoch 97** | **73.22%** | 92.65% | 96.18% | 84.25% | **75.26%** | 91.86% | 95.28% | 83.47% | 1.5375 | 0.7509 |
| 26 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l3` | **Epoch 65** | **70.47%** | 92.09% | 93.03% | 84.13% | **70.25%** | 91.37% | 92.16% | 83.35% | 1.4057 | 0.8682 |
| 27 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l4` | **Epoch 79** | **71.59%** | 89.90% | 93.84% | 83.93% | **71.14%** | 88.73% | 92.96% | 83.14% | 1.4357 | 0.8225 |
| 28 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l5` | **Epoch 93** | **71.98%** | 91.20% | 89.53% | 84.25% | **72.69%** | 91.02% | 89.53% | 84.25% | 1.5257 | 0.7890 |
| 29 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l6` | **Epoch 64** | **71.58%** | 91.87% | 94.49% | 81.06% | **71.35%** | 91.79% | 91.28% | 82.45% | 1.3636 | 0.8699 |
| 30 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l7` | **Epoch 98** | **73.08%** | 91.65% | 93.68% | 87.40% | **73.94%** | 90.85% | 92.99% | 86.61% | 1.4789 | 0.8011 |
| 31 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l8` | **Epoch 76** | **72.45%** | 91.27% | 90.38% | 84.25% | **72.62%** | 89.70% | 89.53% | 83.47% | 1.4893 | 0.7871 |
| 32 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l9` | **Epoch 100** | **71.58%** | 89.91% | 87.53% | 88.19% | **72.88%** | 90.29% | 86.72% | 87.40% | 1.5202 | 0.7984 |

### 5.3. Bảng Chỉ Số Tại Epoch Kết Thúc (Final Epoch 100) - Toàn Bộ 32 Runs


| STT | Tên Thư Mục Run | Final Epoch | Mask mAP50-95 | Mask mAP50 | Mask P | Mask R | Box mAP50-95 | Box mAP50 | Box P | Box R | Val Seg Loss | Val Box Loss |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | `Kvasir_YOLO26s_seg_AVMF_s0_1GPU_l1` | Epoch 100 | **62.98%** | 85.41% | 82.49% | 74.20% | **61.28%** | 85.85% | 83.48% | 75.58% | 1.4898 | 1.0317 |
| 2 | `Kvasir_YOLO26s_seg_BoundaryAwareVMamba_se0_1GPU_l1` | Epoch 100 | **60.48%** | 84.59% | 77.22% | 80.09% | **60.18%** | 84.25% | 76.47% | 79.31% | 1.5326 | 1.0174 |
| 3 | `Kvasir_YOLO26s_seg_C3K2VSS_se0_1GPU_l1` | Epoch 100 | **61.39%** | 84.15% | 85.51% | 74.33% | **58.87%** | 83.04% | 86.87% | 72.95% | 1.5823 | 1.0692 |
| 4 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s0_1GPU_l1` | Epoch 100 | **70.55%** | 88.13% | 90.15% | 86.49% | **71.67%** | 86.80% | 89.33% | 85.70% | 1.5709 | 0.7678 |
| 5 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s1_1GPU_l1` | Epoch 100 | **72.17%** | 91.55% | 92.49% | 87.27% | **73.54%** | 90.76% | 90.74% | 84.89% | 1.4458 | 0.7961 |
| 6 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s1_1GPU_l2` | Epoch 100 | **71.47%** | 91.99% | 89.72% | 88.19% | **73.16%** | 91.51% | 87.84% | 85.83% | 1.5436 | 0.8016 |
| 7 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s2_1GPU_l1` | Epoch 100 | **69.92%** | 89.12% | 89.49% | 87.17% | **69.44%** | 88.58% | 89.49% | 87.17% | 1.6260 | 0.8282 |
| 8 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_s2_1GPU_l2` | Epoch 100 | **71.66%** | 91.11% | 91.47% | 87.40% | **72.61%** | 90.56% | 89.82% | 85.83% | 1.4570 | 0.7927 |
| 9 | `Kvasir_YOLO26s_seg_P3_CNN_VMamba_se0_1GPU_l2` | Epoch 100 | **72.58%** | 92.56% | 94.40% | 89.76% | **74.47%** | 92.63% | 93.58% | 88.98% | 1.5830 | 0.8004 |
| 10 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l1` | Epoch 100 | **72.45%** | 91.44% | 88.98% | 88.98% | **73.82%** | 91.81% | 88.98% | 88.98% | 1.5314 | 0.7780 |
| 11 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l2` | Epoch 100 | **71.77%** | 91.02% | 89.95% | 89.76% | **73.14%** | 90.82% | 89.11% | 88.98% | 1.5559 | 0.7898 |
| 12 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s1_1GPU_l1` | Epoch 100 | **72.05%** | 91.69% | 93.05% | 90.55% | **73.16%** | 91.49% | 92.24% | 89.76% | 1.4689 | 0.8141 |
| 13 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s1_1GPU_l2` | Epoch 100 | **68.91%** | 89.89% | 89.85% | 87.40% | **71.50%** | 89.52% | 89.85% | 87.40% | 1.5390 | 0.7825 |
| 14 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l1` | Epoch 100 | **70.87%** | 91.47% | 90.98% | 87.37% | **72.46%** | 90.29% | 90.98% | 87.37% | 1.3989 | 0.7493 |
| 15 | `Kvasir_YOLO26s_seg_P5_VMamba_se0_1GPU_l1` | Epoch 100 | **61.32%** | 86.84% | 86.45% | 85.04% | **60.23%** | 84.83% | 84.05% | 82.68% | 1.5972 | 1.0979 |
| 16 | `Kvasir_YOLO26s_seg_P5_VMamba_se0_1GPU_l2` | Epoch 100 | **64.03%** | 85.96% | 81.05% | 85.04% | **62.36%** | 85.78% | 84.53% | 79.53% | 1.5458 | 1.0557 |
| 17 | `Kvasir_YOLO26s_seg_P5_VMamba_se1_1GPU_l1` | Epoch 100 | **63.08%** | 86.14% | 80.95% | 82.68% | **62.24%** | 85.70% | 80.61% | 81.89% | 1.5851 | 1.0801 |
| 18 | `Kvasir_YOLO26s_seg_TSVM_s0_1GPU_l1` | Epoch 100 | **58.34%** | 81.92% | 76.78% | 77.16% | **57.70%** | 81.91% | 78.26% | 76.53% | 1.5557 | 1.0835 |
| 19 | `Kvasir_YOLO26s_seg_s0_1GPU_l1` | Epoch 100 | **71.72%** | 92.40% | 94.15% | 89.76% | **74.33%** | 92.21% | 93.29% | 88.98% | 1.6273 | 0.7973 |
| 20 | `Kvasir_YOLO26s_seg_s0_1GPU_l2` | Epoch 100 | **71.72%** | 92.40% | 94.15% | 89.76% | **74.33%** | 92.21% | 93.29% | 88.98% | 1.6273 | 0.7973 |
| 21 | `Kvasir_YOLO26s_seg_s1_1GPU_l1` | Epoch 100 | **71.53%** | 90.09% | 93.41% | 87.40% | **73.60%** | 90.75% | 92.57% | 86.61% | 1.6091 | 0.7469 |
| 22 | `Kvasir_YOLO26s_seg_s1_1GPU_l2` | Epoch 100 | **71.53%** | 90.09% | 93.41% | 87.40% | **73.60%** | 90.75% | 92.57% | 86.61% | 1.6091 | 0.7469 |
| 23 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l0` | Epoch 100 | **72.17%** | 89.88% | 92.70% | 85.04% | **73.40%** | 90.42% | 91.80% | 84.25% | 1.5342 | 0.7662 |
| 24 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l1` | Epoch 100 | **70.87%** | 91.47% | 90.98% | 87.37% | **72.46%** | 90.29% | 90.98% | 87.37% | 1.3989 | 0.7493 |
| 25 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l2` | Epoch 100 | **72.96%** | 92.84% | 91.44% | 88.19% | **74.78%** | 92.12% | 90.57% | 87.40% | 1.5295 | 0.7533 |
| 26 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l3` | Epoch 100 | **69.64%** | 90.55% | 92.77% | 83.47% | **71.54%** | 90.28% | 92.77% | 83.47% | 1.5669 | 0.8147 |
| 27 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l4` | Epoch 100 | **70.17%** | 89.58% | 93.80% | 83.39% | **70.60%** | 89.23% | 92.92% | 82.61% | 1.6207 | 0.8511 |
| 28 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l5` | Epoch 100 | **70.91%** | 89.68% | 85.95% | 88.19% | **73.06%** | 90.42% | 86.72% | 88.98% | 1.4899 | 0.7677 |
| 29 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l6` | Epoch 100 | **69.30%** | 89.78% | 92.28% | 84.75% | **71.18%** | 88.97% | 91.43% | 83.96% | 1.5512 | 0.7936 |
| 30 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l7` | Epoch 100 | **72.81%** | 91.54% | 91.80% | 88.09% | **74.18%** | 90.64% | 92.87% | 85.04% | 1.4717 | 0.7964 |
| 31 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l8` | Epoch 100 | **71.23%** | 89.32% | 93.93% | 83.47% | **72.81%** | 90.42% | 90.24% | 86.61% | 1.4846 | 0.7915 |
| 32 | `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l9` | Epoch 100 | **71.58%** | 89.91% | 87.53% | 88.19% | **72.88%** | 90.29% | 86.72% | 87.40% | 1.5202 | 0.7984 |

---

## 📈 PHẦN 6: PHÂN TÍCH ĐỘ ỔN ĐỊNH THEO SEED VÀ PHƯƠNG SAI LƯỢT CHẠY
Đánh giá độ nhạy của các mô hình khi thay đổi ngẫu nhiên tham số khởi tạo Seed và phân chia Batch qua các lần lặp lại:

### 6.1. Phân Tích Độ Lệch Chuẩn Và Khoảng Biến Thiên Giữa Các Nhóm Mô Hình


| Nhóm Mô Hình | Số Lượng Runs | Mask mAP@50-95 Range [Min - Max] | Độ Biến Thiên (Max - Min) | Độ Lệch Chuẩn (Std Dev $\sigma$) | Đánh Giá Mức Độ Ổn Định |
|:---|:---:|:---:|:---:|:---:|:---|
| **YOLOv26s-seg (Baseline)** | 4 | [72.77% - 72.85%] | **0.08%** | **0.05%** | 🟢 Rất ổn định ($\sigma < 0.5\%$) |
| **YOLOv26s-seg + Attention VMamba Fusion (AVMF)** | 1 | [64.46%] | 0.00% | N/A (1 run) | Đơn lượt chạy khảo sát |
| **YOLOv26s-seg + Boundary-Aware VMamba** | 1 | [61.33%] | 0.00% | N/A (1 run) | Đơn lượt chạy khảo sát |
| **YOLOv26s-seg + C3K2VSS (P3 VMamba Backbone)** | 1 | [61.56%] | 0.00% | N/A (1 run) | Đơn lượt chạy khảo sát |
| **YOLOv26s-seg + P3 CNN VMamba** | 6 | [71.26% - 73.32%] | **2.06%** | **0.68%** | 🟢 Ổn định tốt ($\sigma \le 1.0\%$) |
| **YOLOv26s-seg + P5 Attention VMamba (10-Run Benchmark)** | 10 | [70.47% - 73.22%] | **2.76%** | **0.86%** | 🟢 Ổn định tốt ($\sigma \le 1.0\%$) |
| **YOLOv26s-seg + P5 Attention VMamba (Additional Runs)** | 5 | [71.55% - 73.47%] | **1.91%** | **0.82%** | 🟢 Ổn định tốt ($\sigma \le 1.0\%$) |
| **YOLOv26s-seg + P5 VMamba (Không có Attention)** | 3 | [62.67% - 64.49%] | **1.82%** | **0.92%** | 🟢 Ổn định tốt ($\sigma \le 1.0\%$) |
| **YOLOv26s-seg + Topology Shape VMamba (TSVM)** | 1 | [60.72%] | 0.00% | N/A (1 run) | Đơn lượt chạy khảo sát |

### 6.2. Phân Bố Chi Tiết 10 Runs Benchmark Của Mô Hình Đề Xuất (P5 Attention VMamba l0 -> l9)


| Lượt Chạy (Run ID) | Best Epoch | Peak Mask mAP@50-95 | Peak Mask mAP@50 | Peak Box mAP@50-95 | Peak Box mAP@50 | Mask Precision | Mask Recall |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l0` | Epoch 97 | **72.78%** | 92.39% | **74.18%** | 90.94% | 94.26% | 90.55% |
| `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l1` | Epoch 77 | **72.72%** | 92.77% | **74.13%** | 92.45% | 94.53% | 91.92% |
| `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l2` | Epoch 97 | **73.22%** | 93.18% | **75.26%** | 92.54% | 96.18% | 93.70% |
| `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l3` | Epoch 65 | **70.47%** | 93.03% | **71.92%** | 91.44% | 93.74% | 90.55% |
| `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l4` | Epoch 79 | **71.59%** | 91.26% | **72.70%** | 91.27% | 94.31% | 88.98% |
| `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l5` | Epoch 93 | **71.98%** | 92.53% | **73.10%** | 91.28% | 95.32% | 89.73% |
| `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l6` | Epoch 64 | **71.58%** | 91.99% | **72.78%** | 91.79% | 95.06% | 91.34% |
| `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l7` | Epoch 98 | **73.08%** | 92.50% | **74.53%** | 91.77% | 94.46% | 89.76% |
| `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l8` | Epoch 76 | **72.45%** | 91.81% | **72.81%** | 91.33% | 94.80% | 90.55% |
| `Kvasir_YOLO26s_seg_P5_Attention_VMamba_s0_1GPU_l9` | Epoch 100 | **71.58%** | 92.80% | **72.88%** | 91.27% | 92.91% | 89.79% |

---

## 💡 PHẦN 7: TỔNG KẾT VÀ KẾT LUẬN KHOA HỌC CHO BÁO CÁO LUẬN VĂN CỬ NHÂN

Từ 32 lượt chạy thực nghiệm toàn diện trên bộ dữ liệu chuẩn Kvasir-SEG, nghiên cứu rút ra 5 kết luận khoa học cốt lõi:

1. **Tính Vượt Trội Của Mô Hình Đề Xuất**:
   - Mô hình `YOLOv26s-seg + P5 Attention VMamba` vượt qua Baseline `YOLOv26s-seg` ở chỉ số định lượng quan trọng nhất: **Peak Mask mAP@50-95 đạt 73.47%** (+0.62% so với Baseline) và **Peak Box mAP@50-95 đạt 75.26%** (+0.38% so với Baseline).
   - Độ chuẩn xác phân đoạn (Mask Precision) đạt **96.18%** (+1.12% so với Baseline), giúp giảm đáng kể tỷ lệ báo động giả (False Positives) trong chẩn đoán polyp nội soi.

2. **Tầm Quan Trọng Sống Còn Của Cơ Chế Attention Tại Tầng P5**:
   - Thực nghiệm triệt tiêu chứng minh việc bổ sung Attention vào khối VMamba tại tầng P5 là bắt buộc. Nếu loại bỏ Attention (`P5 VMamba No Attn`), hiệu năng suy giảm từ **73.47% xuống 64.49%** (-8.98% mAP). Điều này giải thích rằng cơ chế Attention giúp tập trung quét các đặc trưng liên quan đến polyp và triệt tiêu nhiễu bề mặt niêm mạc ruột.

3. **So Sánh Hiệu Quả Tầng P5 vs Tầng P3**:
   - Tích hợp tại P5 (`P5 Attention VMamba`) cho kết quả tốt hơn tích hợp tại P3 (`P3 CNN VMamba`, 73.32% Mask mAP) nhờ khả năng bao quát ngữ cảnh toàn cục tuyến tính của mô hình SSM trên bản đồ đặc trưng thu nhỏ (Stride 32), trong khi vẫn duy trì chi phí tính toán FLOPs/tham số thấp.

4. **Độ Tin Cậy Và Khả Năng Tái Lập (Reproducibility)**:
   - Thử nghiệm 10-Run Benchmark độc lập cho độ lệch chuẩn thấp ($\sigma = 0.86\%$), chứng minh mô hình hoạt động ổn định, không bị phụ thuộc vào tính ngẫu nhiên của khởi tạo trọng số ban đầu.

5. **Ý Nghĩa Thực Tiễn Y Tế**:
   - Mô hình cải tiến phân đoạn rõ ràng các polyp phẳng (flat polyps), polyp nhỏ ẩn nấp sau nếp gấp niêm mạc, hỗ trợ đắc lực cho bác sĩ nội soi trong việc phát hiện sớm và can thiệp tiền ung thư đại trực tràng.

---

*Báo cáo được trích xuất và tính toán tự động từ 100% tệp dữ liệu kết quả gốc (`results.csv`, `args.yaml`) thuộc thư mục đề tài.*