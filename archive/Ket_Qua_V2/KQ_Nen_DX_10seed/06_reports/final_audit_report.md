# BÁO CÁO KIỂM TOÁN TÍNH TOÀN VẸN VÀ CHUẨN MỰC KHOA HỌC (FINAL AUDIT REPORT)
## Kiểm toán Bộ Kết quả Thực nghiệm 10 Seed (Kvasir-SEG BG20) — Baseline vs TSVM

**Thời gian kiểm toán:** 27/09/2026 (lần 1) — **Tái kiểm toán độc lập: 02/10/2026 (lần 2)**
**Đối tượng kiểm toán:** Kết quả thực nghiệm 10 seed tại `archive/Ket_Qua_V2/KetQua_Nen/` và bộ phân tích tại `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/`.
**Phạm vi:** 2 mô hình — Baseline (YOLO26s-seg) và TSVM (YOLO26s-seg + Topology-Shape-aware VMamba).

> 🔴 **GHI CHÚ SỬA ĐỔI LẦN 2 (02/10/2026):** Bản nháp đầu tiên của báo cáo này chứa **bảng số liệu sai lệch hoàn toàn** (bảng mAP@50-95 từng seed, giá trị trung bình ma trận nhầm lẫn, biên độ Range, cỡ mẫu "167 ảnh") — những con số không thuộc bộ kết quả 10 seed BG20 hiện hành. Toàn bộ đã được **thay bằng số liệu tái trích xuất trực tiếp từ `results.csv`** và kiểm chứng lại. Ngoài ra, phát hiện mới về **cột TN của ma trận nhầm lẫn** và **3 lượt chạy TSVM không đối chiếu được** (mục 2.1 và mục 4).

---

### 1. Mục đích và Quy chuẩn Kiểm toán

Báo cáo này xác minh độc lập:
1. **Tính nguyên vẹn dữ liệu gốc (Raw Data Integrity)**: Không có tệp dữ liệu gốc (raw csv, checkpoints) nào bị chỉnh sửa, làm sai lệch hoặc ghi đè.
2. **Tính toán học và nhất quán số liệu (Mathematical & Metric Consistency)**: Kiểm tra Mean, Std, Min, Max, Range, Variance, $\Delta$, %, $p$-value, Win/Loss.
3. **Tính toàn vẹn của Ma trận nhầm lẫn (Confusion Matrix Integrity)**: Kiểm tra ràng buộc $TP + FN = 127$, $FP + TN = 40$ trên toàn bộ 10 seed của cả hai mô hình.
4. **Truy xuất nguồn gốc số liệu (Provenance)**: Đối chiếu từng ô dữ liệu giữa báo cáo và tệp `results.csv` gốc.
5. **Chuẩn mực văn phong học thuật (Academic Tone & Scientific Rigor)**.

---

### 2. Kết quả tái kiểm toán lần 2 (02/10/2026)

#### 2.1. Đối chiếu tự động toàn bộ chuỗi dữ liệu

| Hạng mục kiểm tra | Phạm vi | Kết quả |
| :--- | :--- | :---: |
| Trích xuất lại từ 20 tệp `results.csv` (Baseline $s0$–$s9$, TSVM $s0$–$s9$), tại epoch tối ưu theo `metrics/mAP50-95(M)` | 20 run × 17 trường = **340 ô** | **ĐẠT — sai số tuyệt đối = 0** |
| Đối chiếu với `01_raw_analysis/raw_10seeds_extracted_metrics.csv` | 340 ô | **ĐẠT** |
| Tính lại & đối chiếu `02_statistics/mean_std/full_comparison_mean_std.csv` | mean, std, Δ, %, *p*-test, cờ ý nghĩa × 13 chỉ số | **ĐẠT** |
| Tính lại & đối chiếu `02_statistics/min_max/metrics_min_max_range.csv` | min, max, median, range, seed cực trị × 13 chỉ số | **ĐẠT** |
| Tính lại & đối chiếu `02_statistics/seed_comparison/` | seed-by-seed, delta, win/loss | **ĐẠT** |
| Tính lại & đối chiếu `03_metrics/{segmentation,bounding_box,loss}/*_summary.csv` | 28 trường × 12 chỉ số (kèm Wilcoxon) | **ĐẠT** |
| Đối chiếu `06_reports/summary.csv` | toàn bảng | **ĐẠT** |
| Đối chiếu `Stracth/bg20_all_seeds_metrics.csv` | 20 run | **ĐẠT — sai số = 0** |
| **TỔNG SỐ PHÉP KIỂM** | | **559 / 559 ĐẠT — 0 sai lệch** |

#### 2.2. Những điểm KHÔNG đạt (phát hiện mới)

| # | Vấn đề | Mức độ | Chi tiết |
| :--- | :--- | :---: | :--- |
| 1 | **Ô TN của ma trận nhầm lẫn không được đo** | 🔴 Cao | `ultralytics/utils/metrics.py` dòng 427–434: khi ảnh nền không có GT, code **chỉ cộng FP**, không có nhánh `matrix[self.nc, self.nc] += 1`. Ô background↔background luôn = 0 (dòng 550 loại giá trị < 0.005 nên hiển thị trống). Cả 20 ảnh `confusion_matrix.png` đều xác nhận ô này **trống**. Giá trị `TN` trong CSV **đúng bằng $40 - FP$** ở cả 20 dòng → là **số tái dựng theo giả định**, không phải số đo. |
| 2 | **3 lượt chạy TSVM không đối chiếu được ảnh CM** | 🔴 Cao | OCR ảnh `confusion_matrix.png`: **TSVM s0** (CSV: TP 108 / FP 8 / FN 19 — Ảnh: **59 / 10 / 68**), **TSVM s5** (CSV: 112 / 7 / 15 — Ảnh: **0 / 90 / 127**), **TSVM s8** (CSV: 111 / 14 / 16 — Ảnh: **6 / 8 / 121**). Ảnh của 3 run này cho thấy recall gần 0, **mâu thuẫn với `results.csv` của chính các run đó** (recall 0.853 / 0.882 / 0.877). `confusion_matrix.png` của s5 có mtime khác `results.csv` (15:06:10 vs 09:53:28), trùng với các script chẩn đoán lỗi. 17/20 run còn lại khớp **chính xác**. |
| 3 | **Số mẫu ghi sai là "167 ảnh"** | 🟡 Trung bình | Tập kiểm định có **160 ảnh** (120 ảnh polyp chứa **127 thực thể** + 40 ảnh nền). "167" là do cộng nhầm 127 *thực thể* với 40 *ảnh*. Đã sửa toàn bộ. |

---

### 3. Bảng Kiểm toán Chi tiết (Audit Checklist)

| Mục Kiểm toán | Tiêu chí Kiểm tra | Kết quả Kiểm tra | Đánh giá |
| :--- | :--- | :--- | :---: |
| **Raw Data Integrity** | Tệp gốc `KetQua_Nen/` không bị chỉnh sửa | Giữ nguyên 100% 20 tệp `results.csv` và checkpoint của cả 2 mô hình qua 10 seed | **ĐẠT (PASS)** |
| **Sample Size** | Đủ 10 seed độc lập ($s \in \{0, \dots, 9\}$) | Baseline 10 seed, TSVM 10 seed; đều đủ 100 epoch | **ĐẠT (PASS)** |
| **Provenance (lần 2)** | Đối chiếu 340 ô giữa `results.csv` và bảng trích xuất | Sai số = 0 tuyệt đối | **ĐẠT (PASS)** |
| **Derived Statistics (lần 2)** | Tính lại 559 đại lượng thống kê | 0 sai lệch | **ĐẠT (PASS)** |
| **Mask mAP50-95 Metrics** | Baseline: $0.7210 \pm 0.0129$<br>TSVM: $0.7246 \pm 0.0078$ | Khớp chính xác với bảng tổng hợp từ raw CSV | **ĐẠT (PASS)** |
| **Statistical Test ($t$-test)** | $p$-value Mask mAP50-95 $= 0.3839$<br>$p$-value Val Seg Loss $= 0.0908$ | Tính chính xác bằng SciPy Paired t-test | **ĐẠT (PASS)** |
| **Statistical Wording** | Khẳng định $p > 0.05$ là **không có ý nghĩa thống kê** | Đã loại bỏ các câu khẳng định "chứng minh vượt trội", chỉnh sửa thành "không có ý nghĩa thống kê ở mức $\alpha = 0.05$" | **ĐẠT (PASS)** |
| **Seed-wise vs Stability** | Phân biệt tỷ lệ thắng 6/10 seed và độ ổn định | Đã tách bạch: 6/10 seed là so sánh từng cặp; độ ổn định định nghĩa qua Std ($0.0078$ vs $0.0129$, giảm $39.7\%$) và Range ($0.02735$ vs $0.04252$, giảm $35.7\%$) | **ĐẠT (PASS)** |
| **Confusion Matrix Sums** | $TP + FN = 127$<br>$FP + TN = 40$ | Ràng buộc thỏa mãn tuyệt đối trên cả 20 dòng | **ĐẠT (PASS)** |
| **CM Provenance (lần 2)** | Cột TN có phải số đo thực nghiệm? | **KHÔNG** — là số tái dựng $40 - FP$ | **KHÔNG ĐẠT** |
| **CM Consistency (lần 2)** | Đối chiếu 20 ảnh `confusion_matrix.png` | 17/20 khớp; TSVM s0, s5, s8 không khớp | **KHÔNG ĐẠT** |
| **Sample Size Label (lần 2)** | Ghi đúng số ảnh tập kiểm định | Đã sửa "167 ảnh" → **160 ảnh** (127 thực thể polyp + 40 ảnh nền) | **ĐẠT (PASS)** |
| **Mechanism Attribution** | Không suy diễn Topology/Shape feature từ confusion matrix | Đã loại bỏ suy đoán cơ chế hình học từ số đếm phân loại ảnh | **ĐẠT (PASS)** |
| **Chart Fidelity** | Biểu đồ khớp số liệu trong bảng CSV | Biểu đồ khớp 100% với số liệu trong bảng CSV | **ĐẠT (PASS)** |

---

### 4. Chi tiết Xác minh Số liệu Cốt lõi

#### 4.1. Xác minh số liệu từng seed — Mask mAP@50-95
*(nguồn: `02_statistics/seed_comparison/seed_by_seed_metrics_and_deltas.csv`)*

| Seed | Baseline | TSVM | Chênh lệch ($\Delta$) | Trạng thái |
| :---: | :---: | :---: | :---: | :--- |
| 0 | 0.73663 | 0.72451 | −0.01212 | Baseline cao hơn |
| 1 | 0.71649 | 0.72739 | +0.01090 | TSVM cao hơn |
| 2 | 0.71377 | 0.72591 | +0.01214 | TSVM cao hơn |
| 3 | 0.69411 | 0.72126 | +0.02715 | TSVM cao hơn |
| 4 | 0.72741 | 0.71970 | −0.00771 | Baseline cao hơn |
| 5 | 0.73505 | 0.72845 | −0.00660 | Baseline cao hơn |
| 6 | 0.71531 | 0.72537 | +0.01006 | TSVM cao hơn |
| 7 | 0.71449 | 0.70650 | −0.00799 | Baseline cao hơn |
| 8 | 0.73175 | 0.73385 | +0.00210 | TSVM cao hơn |
| 9 | 0.72528 | 0.73285 | +0.00757 | TSVM cao hơn |
| **Mean** | **0.72103** | **0.72458** | **+0.00355** | **TSVM cao hơn ở 6/10 seed** |
| **Std** | **0.01285** | **0.00776** | Giảm **39.7%** | **TSVM phân tán hẹp hơn** |
| **Median** | **0.72089** | **0.72564** | +0.00476 | — |
| **Min** | **0.69411** (s3) | **0.70650** (s7) | +0.01239 | Đáy hiệu năng TSVM cao hơn |
| **Max** | **0.73663** (s0) | **0.73385** (s8) | −0.00278 | Cực đại tương đương |
| **Range** | **0.04252** | **0.02735** | Giảm **35.7%** | Biên độ TSVM hẹp hơn |

*Kết luận kiểm toán:* Số liệu toán học đã được xác minh độc lập từ `results.csv`, không có mâu thuẫn hay sai số tính toán. $p = 0.3839 > 0.05$.

#### 4.2. Xác minh Ma trận Nhầm lẫn

*(nguồn: `01_raw_analysis/raw_10seeds_confusion_matrices.csv`, `04_confusion_matrix/count/*_cm_mean_count.csv`)*

- **Tập kiểm định:** 160 ảnh = 120 ảnh polyp (**127 thực thể ground-truth**) + 40 ảnh nền âm tính.
- **Tập mẫu Ground Truth Positive** ($P = 127$ polyp):
  - Baseline: $TP = 110.3 \pm 3.40$, $FN = 16.7 \pm 3.40 \implies TP + FN = 127.0$ (chính xác tuyệt đối).
  - TSVM: $TP = 111.2 \pm 2.20$, $FN = 15.8 \pm 2.20 \implies TP + FN = 127.0$ (chính xác tuyệt đối).
- **Tập mẫu Ground Truth Negative** ($N = 40$ ảnh nền):
  - Baseline: $FP = 16.8 \pm 2.35$ (đo thật), $TN = 23.2 \pm 2.35$ (**suy dựng** = $40 - FP$) $\implies FP + TN = 40.0$.
  - TSVM: $FP = 14.6 \pm 4.35$ (đo thật), $TN = 25.4 \pm 4.35$ (**suy dựng** = $40 - FP$) $\implies FP + TN = 40.0$.
- **Tỷ lệ chuẩn hóa:** Sensitivity $86.85\% \to 87.56\%$; FP trên nền $42.00\% \to 36.50\%$.

⚠️ **Cảnh báo bắt buộc kèm theo khi trích dẫn ma trận nhầm lẫn:**
1. Cột **TN/Specificity** là **số tái dựng theo giả định mỗi ảnh nền sinh tối đa 1 báo động giả**, không phải số đo của Ultralytics.
2. **3/20 lượt chạy (TSVM s0, s5, s8)** không đối chiếu được với ảnh `confusion_matrix.png`; ảnh của các run này thuộc lượt validation bị lỗi, mâu thuẫn với `results.csv` của chính chúng.
3. Vì vậy, ma trận nhầm lẫn **chỉ nên dùng như quan sát mô tả**, không dùng làm bằng chứng định lượng chính cho kết luận về hiệu quả TSVM.

---

### 5. Cam kết Kiểm toán Cuối cùng

1. **Tuyệt đối không có hành vi làm sai lệch dữ liệu**: Toàn bộ kết quả đều phản ánh thực tế từ các tệp log huấn luyện trong `archive/Ket_Qua_V2/KetQua_Nen/`. Đợt kiểm toán lần 2 đã xác nhận điều này bằng cách tái trích xuất độc lập 340 ô dữ liệu với sai số bằng 0.
2. **Số liệu sai lệch đã được loại bỏ**: Bảng số liệu sai trong bản nháp lần 1 (mAP từng seed, trung bình ma trận nhầm lẫn, Range, cỡ mẫu 167) **không thuộc bộ kết quả 10 seed BG20** và đã bị thay thế hoàn toàn bằng số liệu tái trích xuất từ `results.csv`.
3. **Hạn chế còn tồn tại đã được công khai**: Ba hạn chế về ma trận nhầm lẫn tại mục 2.2 được ghi nhận đầy đủ, minh bạch, và phải được nêu trong luận văn.
4. **Không có kết luận thiên vị**: Các hạn chế về mặt thống kê ($p > 0.05$) và sự tương đương hiệu năng ở một số seed đã được ghi nhận đầy đủ.

---

### 6. Tài liệu tham chiếu chuẩn

> Số liệu chuẩn dùng cho khóa luận cử nhận: [`doc/20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md)
