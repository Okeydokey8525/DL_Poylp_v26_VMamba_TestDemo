# BÁO CÁO ÁNH XẠ SCRIPT VÀ NGUỒN GỐC KẾT QUẢ THỰC NGHIỆM 10 SEED (BG20)
## Chuyên đề: Truy xuất nguồn gốc mã nguồn (Provenance Tracking) của thư mục `Ket_Qua_V2/KQ_Nen_DX_10seed`

> **Tài liệu bàn giao AI / GPT Handoff Document**  
> **Ngày lập:** 29/09/2026  
> **Mục tiêu:** Cung cấp tài liệu định danh chính xác, có thể xác minh trực tiếp trên source code và artifact về nguồn gốc sinh ra toàn bộ các tệp dữ liệu, bảng thống kê và biểu đồ tại `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/`. Giúp các AI tiếp theo (GPT, Claude, Gemini) nắm bắt ngay cơ chế hoạt động mà không cần đọc lại toàn bộ repository.  
> **Nguyên tắc tuân thủ:** [AI_WORK_OPTIMIZATION_RULE.md](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/AI_WORK_OPTIMIZATION_RULE.md) và [nguyen-tac-lam-viec-dai.md](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/nguyen-tac-lam-viec-dai.md).

---

## 1. TỔNG QUAN VỊ TRÍ VÀ LỊCH SỬ DI CHUYỂN ĐƯỜNG DẪN

### 1.1. Thư mục khảo sát hiện tại
- **Đường dẫn chuẩn:** [`archive/Ket_Qua_V2/KQ_Nen_DX_10seed/`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed)
- **Tập dữ liệu nền tảng:** `Kvasir_YOLO_SEG_BG20` (1.200 ảnh = 1.000 ảnh Kvasir-SEG gốc + 200 ảnh nền âm tính `normal-cecum`). Tập kiểm định gồm 160 ảnh (120 ảnh chứa 127 polyp ground-truth + 40 ảnh nền âm tính).
- **Mô hình đối sánh trọng tâm:**
  1. **Baseline**: YOLO26s-seg chuẩn (`KetQua_Nen/YOLOv26s-seg/`) qua 10 seeds (`s0`–`s9`).
  2. **TSVM**: YOLO26s-seg tích hợp nhánh Topology-Shape VMamba tại Layer 10 (`KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/`) qua 10 seeds (`s0`–`s9`).

### 1.2. Nhật ký biến thiên cấu trúc thư mục (Git Provenance)
- **Giai đoạn tạo dựng (Commit `37968c4fcb`, 27/09/2026):** Toàn bộ bộ phân tích 10 seed ban đầu được khởi tạo tại thư mục `archive/KQ_Nen_DX_10seed/`.
- **Giai đoạn tái cấu trúc (Commit `92616d0949`, 28/09/2026):** Nhằm quy hoạch đồng nhất các kết quả phiên bản mới vào không gian làm việc `Ket_Qua_V2/`, thư mục trên đã được di chuyển sang `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/`.
- **Cảnh báo quan trọng cho AI/GPT:** Trong mã nguồn các file script tại `Stracth/`, các biến đường dẫn hardcoded (như `ROOT_OUT` hoặc `fig_dir`) ban đầu mang giá trị `archive\KQ_Nen_DX_10seed`. Khi thực thi lại, bắt buộc phải cập nhật sang đường dẫn hiện tại `archive\Ket_Qua_V2\KQ_Nen_DX_10seed` để ghi đúng vị trí mới.

---

## 2. BẢN ĐỒ ÁNH XẠ SCRIPT VÀ PHÂN HỆ ĐẦU RA

Cấu trúc thư mục `Ket_Qua_V2/KQ_Nen_DX_10seed/` gồm **3 phân hệ độc lập**, được sinh ra từ các script Python chuyên biệt:

```text
Ket_Qua_V2/KQ_Nen_DX_10seed/
├── 01_raw_analysis/  ────────┐
├── 02_statistics/            │
├── 03_metrics/               ├─► [PHÂN HỆ 1]: generate_10seed_thesis_package.py
├── 04_confusion_matrix/      │
├── 05_charts/                │
├── 06_reports/       ────────┘
├── figures/          ────────┐
├── reports/          ────────┴─► [PHÂN HỆ 2]: render_kq_doixung_templates_2models.py
└── efficiency_benchmark/ ────► [PHÂN HỆ 3]: benchmark_runner.py & plot_efficiency_charts_2models.py
```

---

### PHÂN HỆ 1: Phân Tích Thống Kê 10 Seed & 20 Biểu Đồ Khoa Học 300 DPI
* **Script thực thi:** **[`Stracth/generate_10seed_thesis_package.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/generate_10seed_thesis_package.py)**
* **Dữ liệu đầu vào:**
  - 10 file `results.csv` tại `KetQua_Nen/YOLOv26s-seg/Kvasir_BG20_Baseline_YOLO26s_seg_s{0..9}_w2/results.csv`
  - 10 file `results.csv` tại `KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/Kvasir_BG20_YOLO26s_seg_TSVM_s{0..9}_w2/results.csv`
* **Nhiệm vụ & Logic mã nguồn:**
  - Trích xuất metric tại epoch tối ưu (`best.pt` theo `metrics/mAP50-95(M)`).
  - Tự động kiểm định thống kê bằng `scipy.stats` (Mean, Std, Min, Max, Range, Paired Student's t-test, p-value).
  - Xuất ma trận nhầm lẫn 2x2 thực nghiệm cho 10 seed trên 160 ảnh kiểm định.
* **Chi tiết đầu ra được tạo ra:**
  1. `01_raw_analysis/`: `raw_10seeds_extracted_metrics.csv`, `raw_10seeds_confusion_matrices.csv`.
  2. `02_statistics/`: Bảng tổng hợp Mean ± Std (`mean_std/full_comparison_mean_std.csv`), Min-Max-Range (`min_max/metrics_min_max_range.csv`), chi tiết từng seed và tỷ lệ thắng (`seed_comparison/`).
  3. `03_metrics/`: Phân tách độc lập `segmentation/`, `bounding_box/`, `loss/`.
  4. `04_confusion_matrix/`: Thống kê số đếm và phần trăm (`count/`, `percentage/`) kèm 4 biểu đồ heatmap (`14_cm_count_baseline_mean.png`, `15_cm_count_tsvm_mean.png`, `16_cm_percentage_baseline_mean.png`, `17_cm_percentage_tsvm_mean.png`).
  5. `05_charts/`: **20 biểu đồ khoa học 300 DPI** thuộc 5 nhóm:
     - `performance/`: `01_mask_map50_95_comparison.png` đến `05_val_seg_loss_comparison.png`.
     - `stability/`: `06_seed_mask_map50_95_trends.png`, `07_seed_box_map50_95_trends.png`, `10_mean_std_errorbars.png`.
     - `distribution/`: `08_boxplot_mask_map50_95.png`, `09_histogram_kde_mask_map50_95.png`.
     - `correlation/`: `11_scatter_precision_vs_recall.png`, `12_scatter_map_vs_precision.png`, `13_scatter_map_vs_recall.png`.
     - `summary/`: `18_grouped_bar_main_metrics.png`, `19_radar_chart_main_metrics.png`, `20_delta_tsvm_vs_baseline.png`.
  6. `06_reports/`: Báo cáo học thuật `summary.csv`, `summary.md`, `conclusions.md`.
  7. `README.md` tại thư mục gốc gói dữ liệu.

---

### PHÂN HỆ 2: Hệ Thống 12 Biểu Đồ Đối Sánh Trực Diện Theo Chuẩn Template
* **Script thực thi:** **[`Stracth/render_kq_doixung_templates_2models.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/render_kq_doixung_templates_2models.py)**
* **Script mở rộng (4 mô hình):** [`Stracth/render_kq_doixung_templates_for_10seed.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/render_kq_doixung_templates_for_10seed.py) (dành cho Baseline, TSVM, P5_VMamba, ITSMamba).
* **Mục tiêu:** Kế thừa phong cách đồ họa chuyên nghiệp (typography, bảng màu `#1f77b4` & `#ff7f0e`, error bars, layout) từ gói `KQ_DoiXung`, áp dụng chính xác cho 2 mô hình đối đầu trực tiếp trên 10 seeds (dữ liệu sạch 100%, không bịa số).
* **Chi tiết đầu ra tại `figures/` (12 tệp biểu đồ 300 DPI):**
  1. `01_overall_benchmark_barchart.png`: Cột ghép so sánh 4 chỉ số chính kèm sai số $\pm 1\text{Std}$.
  2. `02_val_seg_loss_barchart.png`: Validation Segmentation Loss và phần trăm cải thiện.
  3. `03_seed_by_seed_barchart.png`: Cột ghép đối chiếu trực tiếp từng cặp seed từ Seed 0 đến Seed 9.
  4. `04_convergence_loss_curves.png`: Lưới đồ thị 2x2 đường cong hội tụ 4 hàm mất mát qua 100 epochs kèm dải bóng mờ $\pm 1\text{Std}$.
  5. `05_metric_curves_mAP.png`: Diễn biến Mask mAP@50-95 và mAP@50 qua 100 epochs.
  6. `07b_pie_head_to_head_winrate.png`: Donut chart tỷ lệ thắng đối đầu (TSVM thắng 6/10 seeds = 60%, Baseline thắng 4/10 seeds = 40%).
  7. `09_metric_stability_band_area.png`: Dải miền bao phủ cực trị $[\text{Min}, \text{Max}]$ kết hợp đường trung bình.
  8. `10_radar_multiobjective_tradeoff.png`: Radar chart 6 trục đánh đổi đa mục tiêu.
  9. `11_boxplot_variance_stability.png`: Biểu đồ hộp kết hợp jitter points chứng minh co hẹp phương sai.
  10. `12_confusion_matrix_mean_comparison.png`: Ma trận nhầm lẫn chuẩn hóa trung bình 10 seeds.
  11. `13_confusion_matrix_diff_heatmap.png`: Heatmap chênh lệch hiệu số ($\text{TSVM} - \text{Baseline}$).
  12. `14_confusion_cells_grouped_barchart.png`: Cột nhóm so sánh trung bình số lượng các ô TP, FN, FP, TN.
* **Tài liệu thuyết minh liên kết:** [`reports/chart_template_mapping.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/reports/chart_template_mapping.md).

---

### PHÂN HỆ 3: Đo Đạc & Trực Quan Hóa Hiệu Năng Phần Cứng (`efficiency_benchmark/`)
* **Script đo đạc thực nghiệm phần cứng:** **[`Stracth/benchmark_runner.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/benchmark_runner.py)**  
  *(Script thay thế độc lập: [`Stracth/benchmark_latency.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/benchmark_latency.py))*
  - Đo đạc trực tiếp trên GPU/CPU: Số tham số (Parameters), Độ phức tạp tính toán (GFLOPs @ 640x640), Kích thước model (.pt), Độ trễ suy luận (Latency Mean, Median, P90, P95, P99), Tốc độ khung hình (FPS), Chiếm dụng bộ nhớ (VRAM và RAM).
  - Xuất dữ liệu bảng: `raw/efficiency_raw_benchmark.csv`, `tables/efficiency_summary.csv`, `tables/accuracy_efficiency_summary.csv`.
* **Script vẽ 15 biểu đồ hiệu năng:** **[`Stracth/plot_efficiency_charts_2models.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/plot_efficiency_charts_2models.py)**  
  *(Phiên bản 4 mô hình: [`Stracth/plot_efficiency_charts.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/plot_efficiency_charts.py))*
  - Đầu ra tại `efficiency_benchmark/figures/`:
    + `fig01_params.png`, `fig02_gflops.png`, `fig03_model_size.png`.
    + `fig04_latency_mean.png`, `fig05_latency_percentiles.png`, `fig06_fps.png`.
    + `fig07_vram_status.png`, `fig08_ram.png`.
    + `fig09_map_vs_latency.png`, `fig10_map_vs_fps.png`, `fig11_map_vs_params.png`, `fig12_map_vs_gflops.png`, `fig13_map_vs_ram.png`.
    + `fig14_pareto_map_vs_latency.png`, `fig15_pareto_map_vs_gflops.png` (Đường biên tối ưu Pareto).
  - Báo cáo đi kèm: `reports/benchmark_report.md`, `reports/benchmark_audit.md`.

---

## 3. BẢNG TRA CỨU NHANH DÀNH CHO GPT / AI HANDOFF

Khi người dùng hoặc AI cần tái tạo, kiểm tra hoặc chỉnh sửa bất kỳ thành phần nào, hãy tra cứu bảng này:

| Đối tượng cần cập nhật / kiểm tra | Thư mục lưu trữ đích | File Python chịu trách nhiệm | Biến đường dẫn cần lưu ý trong script |
| :--- | :--- | :--- | :--- |
| **Bảng thống kê 10 seed & 20 chart khoa học** | `Ket_Qua_V2/KQ_Nen_DX_10seed/` (`01` đến `06`) | [`Stracth/generate_10seed_thesis_package.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/generate_10seed_thesis_package.py) | `ROOT_OUT = Path(r".../Ket_Qua_V2/KQ_Nen_DX_10seed")` |
| **12 biểu đồ đối sánh trực diện (Template)** | `Ket_Qua_V2/KQ_Nen_DX_10seed/figures/` | [`Stracth/render_kq_doixung_templates_2models.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/render_kq_doixung_templates_2models.py) | `fig_dir = r".../Ket_Qua_V2/KQ_Nen_DX_10seed/figures"` |
| **Bản vẽ 4 mô hình mở rộng** | Tuỳ chọn (`KQ_Nen_DX_10seed/figures`) | [`Stracth/render_kq_doixung_templates_for_10seed.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/render_kq_doixung_templates_for_10seed.py) | `fig_dir = r".../Ket_Qua_V2/KQ_Nen_DX_10seed/figures"` |
| **Dữ liệu đo đạc phần cứng (Latency, FPS)** | `.../efficiency_benchmark/tables/` & `raw/` | [`Stracth/benchmark_runner.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/benchmark_runner.py) | `raw_path`, `summary_path`, `joint_path` |
| **15 biểu đồ phần cứng & Pareto** | `.../efficiency_benchmark/figures/` | [`Stracth/plot_efficiency_charts_2models.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/plot_efficiency_charts_2models.py) | `target_fig_dirs` |

---

## 4. QUY TRÌNH TÁI THỰC THI (RE-EXECUTION PROTOCOL CHO AI TIẾP QUẢN)

Nếu một AI tiếp nhận yêu cầu chạy lại hoặc làm mới toàn bộ gói kết quả này, thực hiện tuần tự 4 bước sau:

1. **Bước 1 - Kiểm tra tệp nguồn thô:** Xác nhận 20 thư mục seed tại `archive/KetQua_Nen/YOLOv26s-seg/` và `archive/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/` còn nguyên vẹn tệp `results.csv`.
2. **Bước 2 - Chạy gói phân tích hạt nhân:**
   - Cập nhật dòng 13 của [`Stracth/generate_10seed_thesis_package.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/generate_10seed_thesis_package.py) trỏ tới `Ket_Qua_V2/KQ_Nen_DX_10seed`.
   - Chạy lệnh: `python "Stracth/generate_10seed_thesis_package.py"`.
3. **Bước 3 - Render 12 biểu đồ template đối sánh:**
   - Cập nhật dòng 12 của [`Stracth/render_kq_doixung_templates_2models.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/render_kq_doixung_templates_2models.py) trỏ tới `Ket_Qua_V2/KQ_Nen_DX_10seed/figures`.
   - Chạy lệnh: `python "Stracth/render_kq_doixung_templates_2models.py"`.
4. **Bước 4 - Cập nhật biểu đồ Benchmark hiệu năng:**
   - Cập nhật danh sách thư mục đích trong [`Stracth/plot_efficiency_charts_2models.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/plot_efficiency_charts_2models.py).
   - Chạy lệnh: `python "Stracth/plot_efficiency_charts_2models.py"`.

---

## 5. CAM KẾT KIỂM TOÁN TÍNH TOÀN VẸN (AUDIT & INTEGRITY)

* **Bảo toàn dữ liệu lịch sử:** Tuyệt đối không can thiệp, không chỉnh sửa và không retrain đè lên các tệp dữ liệu thô gốc trong `archive/KetQua_Nen/`.
* **Chống bịa đặt số liệu (No Hallucination):** 100% các giá trị trong bảng và biểu đồ đều được tính toán theo công thức toán học từ dữ liệu thực tế, không có số liệu giả định hay làm tròn thiên vị.
* **Chuẩn đồ họa xuất bản:** Mọi biểu đồ được xuất với chuẩn in ấn độ phân giải cao $\ge 300\text{ DPI}$, phông chữ khoa học không bị lỗi dấu tiếng Việt và có thanh sai số đo lường thực tế.
