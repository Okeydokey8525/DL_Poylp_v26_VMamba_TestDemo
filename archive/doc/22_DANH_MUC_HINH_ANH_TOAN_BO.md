# 🖼️ DANH MỤC HÌNH ẢNH TOÀN BỘ & ÁNH XẠ VÀO CHƯƠNG BÁO CÁO
## 43 hình ảnh — Kvasir-SEG BG20, Baseline vs TSVM, 10 seed

> **Ngày lập:** 02/10/2026
> **Phạm vi:** Toàn bộ hình ảnh sinh từ thực nghiệm 10 seed hiện hành
> **Ghi chú:** Mọi đường dẫn đã được **kiểm tra tồn tại thực tế** trên đĩa.

---

## A. NHÓM A — HIỆU NĂNG (dùng chính)

*Nguồn: `Ket_Qua_V2/KQ_Nen_DX_10seed/05_charts/performance/` — tạo bởi `generate_10seed_thesis_package.py`*

| Mã | Tệp | Nội dung | Chương đề xuất |
| :--- | :--- | :--- | :--- |
| `A1` | `05_charts/performance/01_mask_map50_95_comparison.png` | Mean ± Std Mask mAP@50-95 | **CHƯƠNG KẾT QUẢ — HÌNH CHÍNH** |
| `A2` | `05_charts/performance/05_val_seg_loss_comparison.png` | Mean ± Std Val Seg Loss | **Chương Kết quả — HÌNH CHÍNH** |
| `A3` | `05_charts/performance/03_precision_recall_comparison.png` | Precision & Recall của Mask | Chương Kết quả — phân tích trade-off |
| `A4` | `05_charts/performance/02_mask_map50_comparison.png` | Mean ± Std Mask mAP@50 | Chương Kết quả |
| `A5` | `05_charts/performance/04_box_metrics_comparison.png` | 4 chỉ số Bounding Box | Chương Kết quả — *đối chiếu phần phân vùng* |

---

## B. NHÓM B — ĐỘ ỔN ĐỊNH (điểm mạnh rõ nhất của TSVM)

*Nguồn: `.../05_charts/stability/`*

| Mã | Tệp | Nội dung | Chương đề xuất |
| :--- | :--- | :--- | :--- |
| `B1` | `05_charts/stability/10_mean_std_errorbars.png` | Thanh sai số Mean ± Std đa chỉ số | **CHƯƠNG KẾT QUẢ — HÌNH CHÍNH** (chứng minh giảm 39.7% Std) |
| `B2` | `05_charts/stability/06_seed_mask_map50_95_trends.png` | Diễn biến Mask mAP@50-95 qua 10 seed | Chương Kết quả |
| `B3` | `05_charts/stability/07_seed_box_map50_95_trends.png` | Diễn biến Box mAP@50-95 qua 10 seed | Chương Kết quả — *phụ* |

---

## C. NHÓM C — PHÂN PHỐI THỰC NGHIỆM

*Nguồn: `.../05_charts/distribution/`*

| Mã | Tệp | Nội dung | Chương đề xuất |
| :--- | :--- | :--- | :--- |
| `C1` | `05_charts/distribution/08_boxplot_mask_map50_95.png` | Boxplot + điểm phân tán | **CHƯƠNG KẾT QUẢ — HÌNH CHÍNH** |
| `C2` | `05_charts/distribution/09_histogram_kde_mask_map50_95.png` | Histogram + đường KDE | Chương Kết quả — *phụ* |

---

## D. NHÓM D — TƯƠNG QUAN

*Nguồn: `.../05_charts/correlation/`*

| Mã | Tệp | Nội dung | Chương đề xuất |
| :--- | :--- | :--- | :--- |
| `D1` | `05_charts/correlation/11_scatter_precision_vs_recall.png` | Phân tán Precision vs Recall | Chương Phân tích — *thảo luận trade-off* |
| `D2` | `05_charts/correlation/12_scatter_map_vs_precision.png` | mAP@50-95 vs Precision | Chương Phân tích — *phụ* |
| `D3` | `05_charts/correlation/13_scatter_map_vs_recall.png` | mAP@50-95 vs Recall | Chương Phân tích — *phụ* |

---

## E. NHÓM E — TỔNG HỢP

*Nguồn: `.../05_charts/summary/`*

| Mã | Tệp | Nội dung | Chương đề xuất |
| :--- | :--- | :--- | :--- |
| `E1` | `05_charts/summary/20_delta_tsvm_vs_baseline.png` | Thanh ngang Δ (TSVM − Baseline) | **CHƯƠNG KẾT QUẢ — HÌNH CHÍNH** |
| `E2` | `05_charts/summary/18_grouped_bar_main_metrics.png` | Grouped bar 6 chỉ số chính | Chương Kết quả |
| `E3` | `05_charts/summary/19_radar_chart_main_metrics.png` | Radar đa chiều | Chương Kết quả — *phụ* |

---

## F. NHÓM F — MẪU 12 BIỂU ĐỒ THỰC NGHIỆM

*Nguồn: `Ket_Qua_V2/KQ_Nen_DX_10seed/figures/` — tạo bởi `render_kq_doixung_templates_2models.py`*

| Mã | Tệp | Nội dung | Chương đề xuất |
| :--- | :--- | :--- | :--- |
| `F1` | `figures/04_convergence_loss_curves.png` | Lưới 2×2 đường cong hội tụ 4 hàm mất mát (100 epoch) | **CHƯƠNG KẾT QUẢ — HÌNH CHÍNH** (chứng minh hội tụ) |
| `F2` | `figures/01_overall_benchmark_barchart.png` | Cột đôi 4 chỉ số chính ± 1σ | Chương Kết quả |
| `F3` | `figures/02_val_seg_loss_barchart.png` | Val Seg Loss + % cải thiện | Chương Kết quả |
| `F4` | `figures/03_seed_by_seed_barchart.png` | Cột nhóm từng seed 0–9 | Chương Kết quả — *thay cho C1 nếu muốn nhấn mạnh từng cặp* |
| `F5` | `figures/05_metric_curves_mAP.png` | Diễn biến mAP qua 100 epoch | Chương Kết quả |
| `F6` | `figures/07b_pie_head_to_head_winrate.png` | Donut tỷ lệ thắng 6/10 | Chương Kết quả |
| `F7` | `figures/09_metric_stability_band_area.png` | Dải bao phủ [Min, Max] + đường Mean | Chương Kết quả |
| `F8` | `figures/10_radar_multiobjective_tradeoff.png` | Radar 8 trục Box/Mask đối xứng | Chương Phân tích |
| `F9` | `figures/11_boxplot_variance_stability.png` | Boxplot + jitter | Chương Kết quả — *phụ* |

---

## G. ⚠️ NHÓM G — MA TRẬN NHẦM LẪN (CÓ GIỚI HẠN, KHÔNG NÊN LÀ HÌNH CHÍNH)

*Nguồn: `Ket_Qua_V2/KQ_Nen_DX_10seed/figures/`*

| Mã | Tệp | Nội dung | Tình trạng |
| :--- | :--- | :--- | :--- |
| `G1` | `figures/12_confusion_matrix_mean_comparison.png` | Ma trận nhầm lẫn chuẩn hóa trung bình | ⚠️ Chứa ô TN là **số tái dựng** |
| `G2` | `figures/13_confusion_matrix_diff_heatmap.png` | Heatmap hiệu số TSVM − Baseline | ⚠️ Kế thừa giới hạn của G1 |
| `G3` | `figures/14_confusion_cells_grouped_barchart.png` | Cột nhóm TP/FN/FP/TN | ⚠️ Kế thừa giới hạn của G1 |

**3 giới hạn bắt buộc phải nêu nếu dùng nhóm này** (chi tiết: [`20_KET_QUA_CHUAN_..._10SEED.md`](20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md) §0.2 và §5.2):

1. **Ô TN không phải số đo.** `ultralytics/utils/metrics.py:427-434` thiếu nhánh cộng vào ô background↔background → ô này luôn = 0, hiển thị trống trên cả 20 ảnh gốc. TN trong CSV = $40 - FP$ (số tái dựng).
2. **3/20 lượt chạy TSVM (s0, s5, s8) không đối chiếu được** với ảnh gốc.
3. Chỉ nên trình bày như **quan sát mô tả**.

> **Khuyến nghị:** Đưa nhóm G vào **phụ lục** hoặc chương Phân tích, **không** đặt ở chương Kết quả chính.

---

## H. NHÓM H — HIỆU NĂNG PHẦN CỨNG

*Nguồn: `Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/figures/`*

| Mã | Tệp | Nội dung | Chương đề xuất |
| :--- | :--- | :--- | :--- |
| `H1` | `efficiency_benchmark/figures/fig01_params.png` | Số tham số | Chương Độ phức tạp — *nhóm 3 hình gộp* |
| `H2` | `efficiency_benchmark/figures/fig02_gflops.png` | GFLOPs @ 640×640 | ↑ |
| `H3` | `efficiency_benchmark/figures/fig03_model_size.png` | Kích thước `.pt` | ↑ |
| `H4` | `efficiency_benchmark/figures/fig04_latency_mean.png` | Độ trễ trung bình | ↑ |
| `H5` | `efficiency_benchmark/figures/fig05_latency_percentiles.png` | Phân vị độ trễ P50/P90/P95/P99 | ↑ |
| `H6` | `efficiency_benchmark/figures/fig06_fps.png` | FPS | ↑ |
| `H7` | `efficiency_benchmark/figures/fig07_vram_status.png` | Peak VRAM | ↑ |
| `H8` | `efficiency_benchmark/figures/fig08_ram.png` | RAM | ↑ |
| `H9` | `efficiency_benchmark/figures/fig09_map_vs_latency.png` | mAP vs độ trễ | Phân tích đánh đổi hiệu năng – tài nguyên |
| `H10` | `efficiency_benchmark/figures/fig10_map_vs_fps.png` | mAP vs FPS | ↑ |
| `H11` | `efficiency_benchmark/figures/fig11_map_vs_params.png` | mAP vs tham số | ↑ |
| `H12` | `efficiency_benchmark/figures/fig12_map_vs_gflops.png` | mAP vs GFLOPs | ↑ |
| `H13` | `efficiency_benchmark/figures/fig13_map_vs_ram.png` | mAP vs RAM | ↑ |
| `H14` | `efficiency_benchmark/figures/fig14_pareto_map_vs_latency.png` | Đường biên Pareto (mAP–độ trễ) | **Chương Độ phức tạp — HÌNH CHÍNH** |
| `H15` | `efficiency_benchmark/figures/fig15_pareto_map_vs_gflops.png` | Đường biên Pareto (mAP–GFLOPs) | ↑ |

---

## I. BỘ HÌNH KHUYẾN NGHỊ TỐI THIỂU (8 hình)

Nếu bài báo giới hạn số hình, dùng 8 hình sau — phủ đủ 4 khía cạnh:

| # | Mã | Vai trò |
| :---: | :--- | :--- |
| 1 | `A1` | Hiệu năng chính (Mask mAP@50-95) |
| 2 | `F1` | Hội tụ 100 epoch |
| 3 | `B1` | Độ ổn định (giảm 39.7% Std) |
| 4 | `C1` | Phân phối thực nghiệm (boxplot) |
| 5 | `E1` | Độ lệch Δ toàn bộ chỉ số |
| 6 | `F4` | So sánh từng cặp seed |
| 7 | `H14` | Đường biên Pareto hiệu năng – chi phí |
| 8 | `G1` ⚠️ | Ma trận nhầm lẫn *(kèm chú thích cảnh báo)* |

**Bổ sung mã LaTeX chuẩn** cho từng hình: [`../Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/recommended_figures_for_thesis.md`](../Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/recommended_figures_for_thesis.md)

---

## J. QUY ƯỚC ĐẶT TÊN HÌNH TRONG BÁO CÁO

| Quy ước | Áp dụng |
| :--- | :--- |
| Đánh số liên tục theo thứ tự xuất hiện | `Hình 1.`, `Hình 2.`, … |
| Mã trong `Ket_Qua_V2` giữ nguyên trong nội dung tài liệu | `A1`, `B1`, `E1` |
| Chú thích hình dạng: *Hình X. Mô tả.* (in nghiêng, dưới hình) | Bắt buộc |
| Nguồn dữ liệu dưới chú thích khi dùng hình CM | Bắt buộc với nhóm G |
| Đơn vị DPI | Toàn bộ đã ở **300 DPI** |

---

## K. BỔ SUNG CẦN TẠO (chưa tồn tại)

| Hình cần tạo | Lý do | Script đề xuất |
| :--- | :--- | :--- |
| `14_cm_count_baseline_mean.png`, `15_cm_count_tsvm_mean.png` | `doc/07_...md` vẫn tham chiếu nhưng không tồn tại | `generate_10seed_thesis_package.py` (mục 4) |
| `16_cm_percentage_baseline_mean.png`, `17_cm_percentage_tsvm_mean.png` | ↑ | ↑ |
| Biểu đồ phân phối *thống kê* của Δ theo seed (túi Wilcoxon) | Củng cố phần kiểm định | Viết mới |
| Biểu đồ hiệu năng theo epoch (train vs val) cho từng seed | Bổ trợ F1/F5 | `render_kq_doixung_templates_2models.py` |

---

*Danh mục này được kiểm tra tồn tại tự động. Cập nhật cùng [`LICHSU_CAP_NHAT.md`](LICHSU_CAP_NHAT.md).*
