# BÁO CÁO THỰC NGHIỆM ĐÁNH GIÁ ĐỘ PHỨC TẠP VÀ HIỆU NĂNG TÍNH TOÁN (BENCHMARK REPORT)
## Đánh giá Độc lập 4 Mô hình Đạt Chuẩn 10 Seed trên Bộ dữ liệu Kvasir-SEG (BG20)

**Ngày thực hiện**: 27/09/2026  
**Mục đích**: Đo đạc khách quan và độc lập các thông số về dung lượng tham số, độ phức tạp tính toán (FLOPs), thời gian trễ (Latency), thông lượng (FPS), và mức tiêu thụ bộ nhớ (RAM/VRAM) trên cùng một cấu hình phần cứng và môi trường thực thi chuẩn hóa.

---

### 1. Cấu hình Môi trường Thực nghiệm và Giao thức Đo (Protocol)

* **Thiết bị đo (Hardware)**: AMD Ryzen 7 (16 logical CPUs), 16.0 GB System RAM.
* **Môi trường phần mềm (Software Environment)**:
  - Hệ điều hành: Windows 11
  - Python: 3.13.14
  - PyTorch: `2.13.0+cpu` (CPU execution mode)
  - Thư viện đo lường: `thop` (Torch-OpCounter), `psutil`, `time.perf_counter()`
* **Giao thức chuẩn hóa (Benchmark Protocol)**:
  - Định dạng đầu vào: Tensor giả lập cố định $(1, 3, 640, 640)$, kiểu dữ liệu `float32`.
  - Batch size: $1$ (kịch bản suy luận thời gian thực cho từng khung hình nội soi).
  - Khởi động (Warmup): $20$ vòng lặp trước khi bắt đầu bấm giờ.
  - Số lần đo lường chính thức (Measured Iterations): $100$ vòng lặp liên tiếp được lưu vết đầy đủ trong tệp CSV raw.
  - Dọn dẹp tài nguyên (Garbage Collection): Gọi `gc.collect()` và đo lường sự thay đổi bộ nhớ trước/sau khi nạp từng mô hình.

---

### 2. Danh mục Trọng số Checkpoint 4 Mô hình

Toàn bộ các mô hình được nạp từ checkpoint `best.pt` của seed 0 trên bộ dữ liệu Kvasir-SEG BG20 (đều thuộc tập thí nghiệm 10-seed đầy đủ):

1. **YOLOv26s Baseline**:  
   `archive/KetQua_Nen/YOLOv26s-seg/Kvasir_BG20_Baseline_YOLO26s_seg_s0_w2/weights/best.pt`
2. **TSVM (Topology-Shape-aware VMamba)**:  
   `archive/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/Kvasir_BG20_YOLO26s_seg_TSVM_s0_w2/weights/best.pt`
3. **P5 Attention VMamba**:  
   `archive/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_P5_Attention_VMamba/Kvasir_BG20_YOLO26s_seg_P5_Attention_VMamba_s0_w2/weights/best.pt`
4. **ITS Mamba (Interactive Topology VMamba)**:  
   `archive/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_ITSMamba/Kvasir_BG20_YOLO26s_seg_ITSMamba_s0_w2/weights/best.pt`

---

### 3. Bảng Kết quả Tổng hợp Hiệu năng Tính toán (Efficiency Benchmark)

*Dữ liệu trích xuất từ `efficiency_benchmark/tables/efficiency_summary.csv`.*

| Mô hình | Tham số (MParams) | GFLOPs (@640x640) | Dung lượng Trọng số (MB) | Mean Latency (ms) | Std Latency (ms) | P50 (ms) | P95 (ms) | P99 (ms) | Thông lượng (FPS) | Peak RAM (MB) | Peak VRAM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **YOLOv26s Baseline** | $11.434$ | $18.54$ | $22.27$ | $200.12$ | $18.08$ | $195.92$ | $218.28$ | $251.67$ | $5.00$ | $446.44$ | `N/A` |
| **P5 Attention VMamba**| $11.719$ | $18.70$ | $22.82$ | $477.98$ | $13.11$ | $474.55$ | $501.46$ | $518.70$ | $2.09$ | $451.11$ | `N/A` |
| **ITS Mamba** | $12.229$ | $18.94$ | $23.83$ | $651.27$ | $26.03$ | $648.99$ | $689.51$ | $736.68$ | $1.54$ | $462.01$ | `N/A` |
| **TSVM (Đề xuất)** | $12.255$ | $18.86$ | $23.86$ | $821.27$ | $55.91$ | $826.09$ | $899.10$ | $908.97$ | $1.22$ | $466.95$ | `N/A` |

---

### 4. Bảng Tổng hợp Toàn diện Độ chính xác – Hiệu năng (Accuracy–Efficiency Synthesis)

*Ghép dữ liệu 10 seed từ `archive/doc/16_...md` và benchmark mới tại `efficiency_benchmark/tables/accuracy_efficiency_summary.csv`.*

| Mô hình | Mask mAP50-95 (Mean) | Mask mAP Std | Mask Precision | Mask Recall | Params (M) | GFLOPs | Latency (ms) | P95 (ms) | FPS | Peak RAM (MB) | GPU VRAM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **YOLOv26s Baseline** | $0.7210$ | $0.0129$ | $0.9023$ | $0.8584$ | $11.434$ | $18.54$ | $200.12$ | $218.28$ | $5.00$ | $446.44$ | `N/A` |
| **TSVM (Đề xuất)** | $0.7246$ | $0.0078$ | $0.9118$ | $0.8625$ | $12.255$ | $18.86$ | $821.27$ | $899.10$ | $1.22$ | $466.95$ | `N/A` |
| **P5 Attention VMamba**| $0.7165$ | $0.0075$ | $0.8983$ | $0.8338$ | $11.719$ | $18.70$ | $477.98$ | $501.46$ | $2.09$ | $451.11$ | `N/A` |
| **ITS Mamba** | $0.7203$ | $0.0101$ | $0.9205$ | $0.8485$ | $12.229$ | $18.94$ | $651.27$ | $689.51$ | $1.54$ | $462.01$ | `N/A` |

---

### 5. Phân tích Khoa học Đánh đổi (Trade-off) và Đường biên Pareto (Pareto Frontier)

#### 5.1. Về Tham số và Độ phức tạp Lý thuyết (Params & GFLOPs)
- **Gia tăng tham số**: TSVM có $12.255$ triệu tham số, tăng $+0.821$ triệu tham số ($+7.18\%$) so với Baseline ($11.434$ triệu tham số). P5 Attention VMamba có dung lượng nhẹ nhất trong các biến thể mở rộng ($11.719$M).
- **Độ phức tạp FLOPs**: Sự chênh lệch FLOPs lý thuyết giữa 4 mô hình là rất nhỏ (dao động từ $18.54$ GFLOPs đến $18.94$ GFLOPs, mức tăng chỉ từ $+0.86\%$ đến $+2.16\%$). Điều này cho thấy kiến trúc VMamba tuyến tính về mặt lý thuyết giữ cho số phép tính đại số không bị bùng nổ theo kích thước đặc trưng.

#### 5.2. Về Thời gian Trễ Thực tế trên CPU (Inference Latency & FPS)
- **Hiện tượng suy giảm thông lượng**:
  - Baseline thuần CNN đạt thời gian trễ $200.12$ ms (tương đương $5.00$ FPS trên CPU).
  - Cấu hình TSVM có thời gian trễ trung bình tăng lên $821.27$ ms ($1.22$ FPS).
  - P5 Attention VMamba đạt $477.98$ ms ($2.09$ FPS) và ITS Mamba đạt $651.27$ ms ($1.54$ FPS).
- **Nguyên nhân kỹ thuật**: Sự chênh lệch lớn giữa FLOPs lý thuyết (chỉ tăng $+1.7\%$) và thời gian trễ thực tế (tăng ~4 lần) là do:
  1. *Toán tử quét tuần tự (Selective Scan / SSM)*: Cơ chế quét 2D theo 4 hướng phụ thuộc vào các vòng lặp hoặc kernel tối ưu phần cứng. Khi thực thi trên nền tảng CPU mà không có CUDA kernel song song hóa chuyên biệt cho SSM (selective scan CUDA extensions), các toán tử này chịu chi phí điều phối bộ nhớ và phụ thuộc dữ liệu tuần tự cao.
  2. *Chi phí nảy sinh từ phân rã không gian đa hướng*.

#### 5.3. Phân tích Đường biên Tối ưu Pareto
- **Trục Đánh đổi Độ chính xác (mAP) vs Tốc độ (Latency/FPS)**:
  - **YOLOv26s Baseline** nằm trên đường biên Pareto: Đạt tốc độ suy luận nhanh nhất ($200.12$ ms, $5.00$ FPS) với mức mAP khá cao ($0.7210$).
  - **TSVM** nằm trên đường biên Pareto: Đạt độ chính xác trung bình cao nhất ($0.7246$) và độ lệch chuẩn thấp nhất ($\sigma = 0.0078$), chấp nhận thời gian trễ cao hơn ($821.27$ ms).
  - **P5 Attention VMamba** và **ITS Mamba** nằm phía dưới đường biên Pareto: P5 Attention VMamba có mAP thấp hơn ($0.7165$) dù chậm hơn Baseline; ITS Mamba có mAP ($0.7203$) và độ ổn định đều thấp hơn TSVM trong khi vẫn chậm hơn nhiều so với Baseline.
- **Trục Đánh đổi Độ chính xác (mAP) vs Độ phức tạp Tính toán (GFLOPs)**:
  - Baseline đại diện cho điểm tối ưu về chi phí FLOPs thấp nhất ($18.54$ GFLOPs).
  - TSVM đại diện cho điểm tối ưu về độ chính xác phân vùng cao nhất ($0.7246$) trên mức tiêu thụ $18.86$ GFLOPs.

---

### 6. Danh mục Biểu đồ Minh chứng Được Tạo (15 Figures)

Toàn bộ 15 biểu đồ đã được lưu trữ tại `efficiency_benchmark/figures/` với chuẩn 300 DPI:
1. `fig01_params.png`: So sánh số lượng tham số (MParams).
2. `fig02_gflops.png`: So sánh độ phức tạp tính toán lý thuyết (GFLOPs).
3. `fig03_model_size.png`: So sánh dung lượng file trọng số (best.pt).
4. `fig04_latency_mean.png`: Thời gian trễ suy luận trung bình và độ lệch chuẩn.
5. `fig05_latency_percentiles.png`: Phân vị thời gian trễ (P50, P95, P99).
6. `fig06_fps.png`: Tốc độ xử lý khung hình trên giây (FPS).
7. `fig07_vram_status.png`: Trực quan hóa trạng thái VRAM (Ghi nhận N/A môi trường CPU).
8. `fig08_ram.png`: Mức tiêu thụ bộ nhớ RAM tiến trình (RSS).
9. `fig09_map_vs_latency.png`: Biểu đồ tương quan đánh đổi mAP50-95 vs Latency.
10. `fig10_map_vs_fps.png`: Biểu đồ tương quan đánh đổi mAP50-95 vs FPS.
11. `fig11_map_vs_params.png`: Biểu đồ tương quan đánh đổi mAP50-95 vs Params.
12. `fig12_map_vs_gflops.png`: Biểu đồ tương quan đánh đổi mAP50-95 vs GFLOPs.
13. `fig13_map_vs_ram.png`: Biểu đồ tương quan đánh đổi mAP50-95 vs RAM.
14. `fig14_pareto_map_vs_latency.png`: Phân tích đường biên tối ưu Pareto mAP vs Latency.
15. `fig15_pareto_map_vs_gflops.png`: Phân tích đường biên tối ưu Pareto mAP vs GFLOPs.
