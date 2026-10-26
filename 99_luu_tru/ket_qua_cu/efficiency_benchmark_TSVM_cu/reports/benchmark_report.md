# BÁO CÁO THỰC NGHIỆM ĐÁNH GIÁ ĐỘ PHỨC TẠP VÀ HIỆU NĂNG TÍNH TOÁN
## So sánh Độc lập giữa YOLOv26s Baseline và TSVM (Kvasir-SEG BG20)

**Ngày thực hiện**: 27/09/2026  
**Phạm vi**: So sánh đối đầu trực diện giữa 2 mô hình cốt lõi:
1. **Mô hình gốc (Baseline)**: `YOLOv26s Baseline`
2. **Mô hình đề xuất (TSVM)**: `Topology-Shape-aware VMamba`

---

### 1. Cấu hình Môi trường Thực nghiệm và Giao thức Đo

* **Phần cứng (Hardware)**: AMD Ryzen 7 (16 logical CPUs), 16.0 GB RAM hệ thống.
* **Môi trường phần mềm**: Python 3.13.14, PyTorch `2.13.0+cpu` (thực thi trên CPU).
* **Định dạng dữ liệu đầu vào**: Tensor giả lập $(1, 3, 640, 640)$, kiểu `float32`, Batch size = 1.
* **Giao thức đo lường**: 20 vòng lặp Warmup + 100 vòng lặp đo đạc liên tiếp bằng `time.perf_counter()`.
* **Trọng số sử dụng**:
  - Baseline: `archive/KetQua_Nen/YOLOv26s-seg/Kvasir_BG20_Baseline_YOLO26s_seg_s0_w2/weights/best.pt`
  - TSVM: `archive/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/Kvasir_BG20_YOLO26s_seg_TSVM_s0_w2/weights/best.pt`

---

### 2. Bảng So sánh Hiệu năng Tính toán (Efficiency Benchmark)

*Dữ liệu trích xuất từ `efficiency_benchmark/tables/efficiency_summary.csv`.*

| Chỉ số Hiệu năng | YOLOv26s Baseline | TSVM (Đề xuất) | Chênh lệch ($\Delta$) | % Thay đổi |
| :--- | :---: | :---: | :---: | :---: |
| **Số lượng Tham số (Params)** | $11.434\text{ M}$ | $12.255\text{ M}$ | $+0.821\text{ M}$ | $+7.18\%$ |
| **Độ phức tạp FLOPs (@640x640)** | $18.54\text{ GFLOPs}$ | $18.86\text{ GFLOPs}$ | $+0.32\text{ GFLOPs}$ | $+1.73\%$ |
| **Dung lượng file trọng số (best.pt)** | $22.27\text{ MB}$ | $23.86\text{ MB}$ | $+1.59\text{ MB}$ | $+7.14\%$ |
| **Thời gian trễ trung bình (Mean)** | $200.12\text{ ms}$ | $821.27\text{ ms}$ | $+621.15\text{ ms}$ | $+310.39\%$ |
| **Độ lệch chuẩn thời gian trễ (Std)** | $18.08\text{ ms}$ | $55.91\text{ ms}$ | $+37.83\text{ ms}$ | --- |
| **Phân vị P50 (Median Latency)** | $195.92\text{ ms}$ | $826.09\text{ ms}$ | $+630.17\text{ ms}$ | $+321.65\%$ |
| **Phân vị P95 (95th Percentile)** | $218.28\text{ ms}$ | $899.10\text{ ms}$ | $+680.82\text{ ms}$ | $+311.90\%$ |
| **Phân vị P99 (99th Percentile)** | $251.67\text{ ms}$ | $908.97\text{ ms}$ | $+657.30\text{ ms}$ | $+261.18\%$ |
| **Tốc độ xử lý (FPS)** | $5.00\text{ FPS}$ | $1.22\text{ FPS}$ | $-3.78\text{ FPS}$ | $-75.60\%$ |
| **Bộ nhớ RAM đỉnh (Peak RSS)** | $446.44\text{ MB}$ | $466.95\text{ MB}$ | $+20.51\text{ MB}$ | $+4.59\%$ |
| **Bộ nhớ GPU VRAM** | `N/A` | `N/A` | --- | CPU execution |

---

### 3. Bảng Tổng hợp Toàn diện Độ chính xác 10-Seed và Hiệu năng (Accuracy–Efficiency)

*Ghép dữ liệu 10-seed từ `archive/doc/16_...md` và benchmark mới tại `efficiency_benchmark/tables/accuracy_efficiency_summary.csv`.*

| Model | mAP50-95 | Std | Precision | Recall | Params | GFLOPs | Latency | P95 | FPS | VRAM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **YOLOv26s Baseline** | $0.7210$ | $0.0129$ | $0.9023$ | $0.8584$ | $11.434\text{ M}$ | $18.54$ | $200.12\text{ ms}$ | $218.28\text{ ms}$ | $5.00$ | `N/A` |
| **TSVM** | $0.7246$ | $0.0078$ | $0.9118$ | $0.8625$ | $12.255\text{ M}$ | $18.86$ | $821.27\text{ ms}$ | $899.10\text{ ms}$ | $1.22$ | `N/A` |

---

### 4. Đánh giá Đánh đổi và Đường biên Pareto (Pareto Trade-off Analysis)

1. **Hiệu năng Phân vùng và Độ Ổn định**:
   - TSVM đạt Mask mAP50-95 trung bình cao hơn ($0.7246$ so với $0.7210$, $\Delta = +0.0036$).
   - TSVM có độ ổn định phương sai vượt trội hơn (độ lệch chuẩn $\sigma = 0.0078$ so với $0.0129$, giảm $39.5\%$ độ tán xạ).
2. **Độ phức tạp Tính toán (Params & GFLOPs)**:
   - TSVM tăng thêm nhẹ $0.821\text{ M}$ tham số ($+7.18\%$) và $0.32\text{ GFLOPs}$ ($+1.73\%$). Điều này khẳng định chi phí lý thuyết của nhánh VMamba Topology-Shape là rất nhỏ.
3. **Độ trễ Thực tế trên CPU**:
   - Do toán tử quét 2D (SS2D) trong VMamba mang tính tuần tự và hiện tại chưa có kernel C++/CUDA tối ưu chuyên dụng cho CPU, thời gian trễ thực tế tăng từ $200.12\text{ ms}$ lên $821.27\text{ ms}$ (tốc độ từ $5.00\text{ FPS}$ xuống $1.22\text{ FPS}$).
4. **Phân tích Đường biên Tối ưu Pareto**:
   - Cả hai mô hình đều nằm trên **đường biên Pareto**:
     - *Baseline*: Điểm tối ưu cho ứng dụng thực tế đòi hỏi thông lượng khung hình cao nhất và chi phí độ trễ tối thiểu ($200.12\text{ ms}$, $5.00\text{ FPS}$).
     - *TSVM*: Điểm tối ưu cho ứng dụng chẩn đoán y tế ưu tiên độ chính xác phân vùng cao nhất và sai số giữa các lần khởi tạo thấp nhất.

---

### 5. Danh mục 15 Biểu đồ Đã Cập nhật (300 DPI)

Toàn bộ 15 biểu đồ đã được vẽ lại đồng bộ cho 2 mô hình tại `efficiency_benchmark/figures/`:
1. `fig01_params.png`: So sánh Parameters (11.434M vs 12.255M)
2. `fig02_gflops.png`: So sánh GFLOPs (18.54 vs 18.86)
3. `fig03_model_size.png`: So sánh Checkpoint Size (22.27 MB vs 23.86 MB)
4. `fig04_latency_mean.png`: Thời gian trễ Mean kèm sai số Std
5. `fig05_latency_percentiles.png`: Phân vị thời gian trễ P50, P95, P99
6. `fig06_fps.png`: Tốc độ xử lý khung hình (5.00 FPS vs 1.22 FPS)
7. `fig07_vram_status.png`: Trạng thái VRAM (Ghi nhận N/A CPU environment)
8. `fig08_ram.png`: Mức tiêu thụ bộ nhớ RAM (446.4 MB vs 467.0 MB)
9. `fig09_map_vs_latency.png`: Đánh đổi mAP50-95 vs Latency
10. `fig10_map_vs_fps.png`: Đánh đổi mAP50-95 vs FPS
11. `fig11_map_vs_params.png`: Đánh đổi mAP50-95 vs Params
12. `fig12_map_vs_gflops.png`: Đánh đổi mAP50-95 vs GFLOPs
13. `fig13_map_vs_ram.png`: Đánh đổi mAP50-95 vs RAM
14. `fig14_pareto_map_vs_latency.png`: Phân tích Pareto mAP vs Latency
15. `fig15_pareto_map_vs_gflops.png`: Phân tích Pareto mAP vs GFLOPs
