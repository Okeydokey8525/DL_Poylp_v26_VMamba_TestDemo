# FORENSIC EXPERIMENT AUDIT — KQ_Nen_DX_10seed

**Đối tượng:** `06_reports/summary.csv` và `03_metrics/segmentation/segmentation_metrics_summary.csv`
**Phương thức:** READ → TRACE → VERIFY → ANALYZE → REPORT (không training, không sửa/xóa dữ liệu gốc)
**Ngày chạy audit:** 02/10/2026
**Mức độ chính xác:** mọi con số quan trọng được gắn nhãn `[VERIFIED]` / `[DERIVED]` / `[UNVERIFIED]` / `[DISCREPANCY]`

---

## 1. NGUỒN DỮ LIỆU (Data Sources)

### 1.1 Ba tầng dữ liệu

**Tầng A — Raw experimental evidence** `[VERIFIED]`

| Nguồn | Số file | Ghi chú |
| :--- | ---: | :--- |
| `Ket_Qua_V2\KetQua_Nen\YOLOv26s-seg\Kvasir_BG20_Baseline_YOLO26s_seg_s{0..9}_w2\results.csv` | 10 | Baseline, mỗi file 100 epoch |
| `Ket_Qua_V2\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM\Kvasir_BG20_YOLO26s_seg_TSVM_s{0..9}_w2\results.csv` | 10 | TSVM (đề xuất), mỗi file 100 epoch |
| `confusion_matrix.png` trong 20 thư mục run | 20 | Artifact CM của Ultralytics |

**Tầng B — Extracted / processed metrics** `[VERIFIED]`

| File | Dòng | Ghi chú |
| :--- | ---: | :--- |
| `01_raw_analysis/raw_10seeds_extracted_metrics.csv` | 20 | 1 dòng/run, trích tại best epoch |
| `01_raw_analysis/raw_10seeds_confusion_matrices.csv` | 20 | CM 20 run |
| `02_statistics/mean_std/full_comparison_mean_std.csv` | 13 | |
| `02_statistics/min_max/metrics_min_max_range.csv` | 13 | |
| `02_statistics/seed_comparison/seed_by_seed_metrics_and_deltas.csv` | 10 | |
| `02_statistics/seed_comparison/seed_win_loss_summary.csv` | 13 | |
| `03_metrics/segmentation/segmentation_metrics_summary.csv` | 4 | **Mục tiêu 2** |
| `03_metrics/bounding_box/bounding_box_metrics_summary.csv` | 4 | |
| `03_metrics/loss/validation_loss_metrics_summary.csv` | 4 | |
| `04_confusion_matrix/count/*` , `04_confusion_matrix/percentage/*` | 6 CSV | |

**Tầng C — Final report** `[VERIFIED]`

| File | Dòng |
| :--- | ---: |
| `06_reports/summary.csv` | 13 | **Mục tiêu 1** |
| `06_reports/summary.md`, `conclusions.md`, `README.md` | — |

**Tầng audit độc lập (02/10/2026):** `07_audit/audit_report.csv` (694 dòng), `07_audit/reextracted_from_results_csv.csv` (20 dòng), `07_audit/doc_path_report.csv`.

### 1.2 Cấu hình thực nghiệm

- **Dataset:** Kvasir-SEG + 20% nền âm tính (`data_bg20.yaml`). Validation = 160 ảnh (120 ảnh polyp / 127 GT box-mask; 40 ảnh `normal-cecum`). `[VERIFIED]`
- **Số experiment:** 20 run = 2 mô hình × 10 seed (seed 0–9), 100 epochs/run. `[VERIFIED — 20/20 results.csv đọc trực tiếp, mỗi file đúng 100 dòng]`
- **Baseline:** YOLO26s-seg chuẩn. **Proposed/TSVM:** YOLO26s-seg + nhánh Topology-Shape-aware VMamba. `[VERIFIED — theo README §1]`
- **Seed:** đủ 0–9 cho cả 2 mô hình, **không thiếu, không duplicate** `[VERIFIED — kiểm `duplicated(model,seed)` = 0]`

---

## 2. METHODOLOGY (Cách audit)

1. Xác định workspace → định vị chính xác 2 file CSV mục tiêu (không hard-code path).
2. Đọc full cả 2 file (schema, dtype, missing, duplicate, unique).
3. Truy ngược script sinh file → đọc code sinh.
4. **Tái trích xuất độc lập từ Tầng A**: tự đọc 20 `results.csv`, tự chọn best epoch bằng `idxmax(metrics/mAP50-95(M))`, tự tính lại toàn bộ thống kê bằng pandas/numpy/scipy.
5. Đối chiếu Tầng A ↔ Tầng B ↔ Tầng C và 6 file trung gian.
6. Cross-check CM cả về mặt toán học lẫn **đọc trực tiếp 3 ảnh `confusion_matrix.png`** gây tranh cãi.
7. 3 subagent kiểm chứng độc lập (CSV Auditor, Source Tracer, Independent Cross Checker), không tin kết quả của nhau.

**Quy ước aggregation đã xác minh từ code** `[VERIFIED]`:

- Chọn best epoch: `df['metrics/mAP50-95(M)'].idxmax()` — khớp README.
- `mean` = trung bình 10 giá trị per-seed; `std` = **`ddof=1` (sample std)**.
- `delta = tsvm_mean − baseline_mean`; `percent_change = delta / baseline_mean × 100`.
- `range = max − min`; `median` = trung vị 10 seed.
- **Không rounding** khi ghi `summary.csv` (số float đầy đủ); rounding 4 chữ số chỉ có ở file display (`full_comparison_mean_std.csv`, `.md`).
- Quy ước "thắng": metric thường → cao hơn thắng; metric `*_loss` → **thấp hơn thắng** (best/worst seed dùng `argmin`/`argmax` đảo chiều).
- Kiểm định: `scipy.stats.ttest_rel(tsvm, baseline)` (paired, 2-sided) và `scipy.stats.wilcoxon(tsvm, b)` (mặc định `zero_method='wilcox'`); cờ `statistically_significant_005` chỉ dựa trên **p_ttest < 0.05**.

---

## 3. SCHEMA 2 CSV CHÍNH

Cả 2 file có **cùng schema 28 cột** `[VERIFIED]`:

| Cột | Ý nghĩa | Kiểu |
| :--- | :--- | :--- |
| `metric_key`, `metric_name` | Khóa/nhãn metric | str |
| `baseline_mean/std/min/max/median/range` | Thống kê 10 seed Baseline | float |
| `baseline_best_seed`, `baseline_worst_seed` | Seed tốt/xấu nhất (0-based) | int |
| `tsvm_mean/std/min/max/median/range` | Thống kê 10 seed TSVM | float |
| `tsvm_best_seed`, `tsvm_worst_seed` | Seed tốt/xấu nhất (0-based) | int |
| `delta_tsvm_minus_baseline` | Δ tuyệt đối | float |
| `percent_change` | Δ phần trăm | float |
| `tsvm_wins_seeds`, `baseline_wins_seeds`, `ties_seeds` | Số seed TSVM/Baseline/hòa tốt hơn | int |
| `paired_ttest_stat`, `p_value_ttest` | Paired t-test | float |
| `wilcoxon_stat`, `p_value_wilcoxon` | Wilcoxon signed-rank | float |
| `statistically_significant_005` | Cờ p_ttest < 0.05 | bool |

**Kết quả kiểm schema:**

| Kiểm tra | `summary.csv` | `segmentation_metrics_summary.csv` |
| :--- | :--- | :--- |
| Dòng dữ liệu / cột | 13 × 28 `[VERIFIED]` | 4 × 28 `[VERIFIED]` |
| Missing values | **0** `[VERIFIED]` | **0** `[VERIFIED]` |
| Duplicate rows | **0** `[VERIFIED]` | **0** `[VERIFIED]` |
| Ragged rows | không `[VERIFIED]` | không `[VERIFIED]` |
| Seed index range | 52/52 giá trị ∈ [0,9] `[VERIFIED]` | 16/16 ∈ [0,9] `[VERIFIED]` |

**Mối quan hệ 2 file:** `segmentation_metrics_summary.csv` là **tập con chính xác 100%** của `summary.csv` — 4 dòng `mask_map50_95, mask_map50, mask_precision, mask_recall`, so sánh cả ở mức float64 lẫn **raw string: 0/112 cell sai lệch** `[VERIFIED]`.

**13 `metric_key` trong `summary.csv`:** `mask_map50_95, mask_map50, mask_precision, mask_recall, box_map50_95, box_map50, box_precision, box_recall, val_seg_loss, val_box_loss, val_cls_loss, val_l1_loss, best_epoch`.

**Không có cột IoU / mIoU / Dice / F1 trong bất kỳ file nào của 2 file mục tiêu** `[VERIFIED — quét tên cột và giá trị metric_key/metric_name: 0 kết quả]`.

---

## 4. SEGMENTATION METRICS

Nguồn: `segmentation_metrics_summary.csv` (4 dòng) — **khớp tuyệt đối với `summary.csv`** `[VERIFIED]`.

| metric_key | Baseline Mean±Std | TSVM Mean±Std | Δ | Δ% | W/B/T | p_ttest | p_wilcoxon | Sig@0.05 |
| :--- | ---: | ---: | ---: | ---: | :---: | ---: | ---: | :---: |
| Mask mAP@50-95 | 0.721029 ± 0.012854 | 0.724579 ± 0.007755 | +0.003550 | +0.4924% | 6/4/0 | 0.3839 | 0.4316 | False |
| Mask mAP@50 | 0.911863 ± 0.010662 | 0.906216 ± 0.008220 | −0.005647 | −0.6193% | 3/7/0 | 0.2273 | 0.2754 | False |
| Mask Precision | 0.902278 ± 0.033899 | 0.911769 ± 0.024596 | +0.009491 | +1.0519% | 5/5/0 | 0.5428 | 0.6250 | False |
| Mask Recall | 0.858360 ± 0.025171 | 0.862498 ± 0.017318 | +0.004138 | +0.4821% | 6/4/0 | 0.5907 | 0.6250 | False |

Toàn bộ 4 dòng: `[VERIFIED]` — tái tính từ 20 `results.csv`, sai số ≤ 1.78e-15.

### 4.1 Về IoU, Dice, F1 — CÂU TRẢ LỜI QUYẾT ĐỊNH

- **IoU / mIoU:** **KHÔNG tồn tại** trong 2 file CSV mục tiêu lẫn toàn bộ gói kết quả. `[VERIFIED]`
- **Dice / F1:** **KHÔNG tồn tại** dưới dạng cột. `[VERIFIED]`
- **Không được đồng nhất F1 với Dice.** Đây là 2 định nghĩa khác nhau:
  - Dice = 2TP / (2TP + FP + FN)
  - F1 (theo precision/recall) = 2PR/(P+R) — chỉ trùng Dice nếu P, R cùng tính trên đúng một tập TP/FP/FN.
- **Không thể suy ra Dice/IoU/F1 từ confusion matrix của gói này.** Lý do:
  1. Không file nào chứa Dice/IoU/F1 (các nhắc "IoU" trong doc là **ngưỡng matching IoU=0.45**, không phải chỉ số).
  2. CM tính ở ngưỡng cố định `conf=0.25, IoU=0.45` mức object/ảnh, trong khi metric `results.csv` là mAP/P/R Ultralytics tích hợp trên dải IoU 0.5:0.95 với sweep confidence tại **best epoch** — hai định nghĩa khác nhau, không thể quy đổi.
  3. Ô **TN không bao giờ được Ultralytics cộng** (`ultralytics/utils/metrics.py`, `process_batch`) → `TN = 40 − FP` là **số tái dựng**, không phải số đo.

**Minh chứng số (chỉ để chứng minh KHÔNG được đồng nhất)** `[DERIVED]`:

| Quantity | Baseline | TSVM |
| :--- | ---: | ---: |
| Dice tính từ mean-CM (`2TP/(2TP+FP+FN)`) | 0.868162 | 0.879747 |
| F1 suy từ mean Mask P/R (`2PR/(P+R)`) | 0.879772 | 0.886447 |
| Chênh lệch | 0.011610 | 0.006700 |

→ Hai con số **không bằng nhau**, chứng minh không thể coi Dice = F1 ở đây. Cả hai đều `[DERIVED]`, **không phải số liệu đo được và không có trong bất kỳ file nào** → `[UNVERIFIED]` nếu dùng làm số liệu luận văn.

---

## 5. BOX METRICS

| Metric | Baseline | TSVM | Δ | Δ% | W/B/T | p_ttest | Sig |
| :--- | ---: | ---: | ---: | ---: | :---: | ---: | :---: |
| Box mAP@50-95 | 0.726191 | 0.728522 | +0.002331 | +0.3210% | 6/4/0 | 0.7152 | False |
| Box mAP@50 | 0.901050 | 0.900614 | −0.000436 | −0.0484% | 5/5/0 | 0.9334 | False |
| Box Precision | 0.899239 | 0.906244 | +0.007005 | +0.7790% | 5/5/0 | 0.5921 | False |
| Box Recall | 0.843439 | 0.856745 | +0.013306 | +1.5776% | 6/4/0 | 0.2674 | False |

Std (ddof=1): Box mAP@50-95 = 0.019752 (B) vs 0.014100 (T); Box mAP@50 = 0.011645 vs 0.009029; Box P = 0.032603 vs 0.025072; Box R = 0.033725 vs 0.015228.
Toàn bộ `[VERIFIED]`.

## 6. MASK METRICS

Xem bảng ở **Mục 4**. Tách tách riêng với Box:

| Metric | Baseline | TSVM | Δ | Δ% |
| :--- | ---: | ---: | ---: | ---: |
| Mask Precision | 0.902278 | 0.911769 | +0.009491 | +1.0519% |
| Mask Recall | 0.858360 | 0.862498 | +0.004138 | +0.4821% |
| **Mask mAP50** | 0.911863 | 0.906216 | −0.005647 | −0.6193% |
| **Mask mAP50-95** | 0.721029 | 0.724579 | +0.003550 | +0.4924% |

`[VERIFIED]` — cả 4 dòng.

## 7. BASELINE vs PROPOSED (Tổng hợp)

| Metric | Baseline | Proposed (TSVM) | Δ | Δ% |
| :--- | ---: | ---: | ---: | ---: |
| Mask mAP50-95 | 0.721029 | 0.724579 | +0.003550 | +0.4924% |
| Mask mAP50 | 0.911863 | 0.906216 | −0.005647 | −0.6193% |
| Mask Precision | 0.902278 | 0.911769 | +0.009491 | +1.0519% |
| Mask Recall | 0.858360 | 0.862498 | +0.004138 | +0.4821% |
| Box mAP50-95 | 0.726191 | 0.728522 | +0.002331 | +0.3210% |
| Box mAP50 | 0.901050 | 0.900614 | −0.000436 | −0.0484% |
| Box Precision | 0.899239 | 0.906244 | +0.007005 | +0.7790% |
| Box Recall | 0.843439 | 0.856745 | +0.013306 | +1.5776% |
| Val Seg Loss (↓tốt hơn) | 1.304545 | 1.242387 | −0.062158 | −4.7647% |
| Val Box Loss (↓) | 0.723946 | 0.730508 | +0.006562 | +0.9064% |
| Val Cls Loss (↓) | 0.559076 | 0.614813 | +0.055737 | +9.9695% |
| Val L1 Loss (↓) | 0.016379 | 0.016212 | −0.000167 | −1.0196% |
| Best Epoch | 87.30 | 91.70 | +4.40 | +5.0401% |

`[VERIFIED]` — tái tính độc lập, sai số ≤ 1.78e-15.

**Không metric nào đạt ý nghĩa thống kê ở α = 0.05.** p_ttest nhỏ nhất = **0.090772** (`val_seg_loss`), p_wilcoxon nhỏ nhất = **0.083984**. Cột `statistically_significant_005 = False` ở cả 13/13 dòng `[VERIFIED]`.

## 8. 10-SEED STABILITY

| Metric | Baseline Mean±Std | TSVM Mean±Std | Δ Mean | Δ Std |
| :--- | ---: | ---: | ---: | ---: |
| Mask mAP50-95 | 0.721029 ± 0.012854 | 0.724579 ± 0.007755 | +0.003550 | −0.005099 |
| Mask mAP50 | 0.911863 ± 0.010662 | 0.906216 ± 0.008220 | −0.005647 | −0.002442 |
| Mask Precision | 0.902278 ± 0.033899 | 0.911769 ± 0.024596 | +0.009491 | −0.009303 |
| Mask Recall | 0.858360 ± 0.025171 | 0.862498 ± 0.017318 | +0.004138 | −0.007852 |
| Box mAP50-95 | 0.726191 ± 0.019752 | 0.728522 ± 0.014100 | +0.002331 | −0.005652 |
| Box mAP50 | 0.901050 ± 0.011645 | 0.900614 ± 0.009029 | −0.000436 | −0.002617 |
| Box Precision | 0.899239 ± 0.032603 | 0.906244 ± 0.025072 | +0.007005 | −0.007531 |
| Box Recall | 0.843439 ± 0.033725 | 0.856745 ± 0.015228 | +0.013306 | −0.018498 |
| Val Seg Loss | 1.304545 ± 0.086664 | 1.242387 ± 0.038667 | −0.062158 | −0.047997 |
| Best Epoch | 87.30 ± 13.098 | 91.70 ± 4.855 | +4.40 | −8.244 |

`[VERIFIED]`.

**Độ ổn định Mask mAP@50-95 (metric chính):**
- Std giảm **39.67%** (1 − 0.007755/0.012854) `[DERIVED]`
- **F-ratio (phương sai) = 2.75×** (σ²_B/σ²_T) `[DERIVED]`
- **Phương sai giảm 63.6%** `[DERIVED]`
- Range: 0.042520 (B) vs 0.027350 (T), giảm 35.7% `[DERIVED]`

## 9. PER-SEED VERIFICATION

### Mask mAP@50-95 (metric chính) — `[VERIFIED]`

| Seed | Baseline | TSVM | Δ | Hướng |
| ---: | ---: | ---: | ---: | :--- |
| 0 | 0.73663 | 0.72451 | −0.01212 | TSVM < B |
| 1 | 0.71649 | 0.72739 | +0.01090 | TSVM > B |
| 2 | 0.71377 | 0.72591 | +0.01214 | TSVM > B |
| 3 | 0.69411 | 0.72126 | +0.02715 | TSVM > B |
| 4 | 0.72741 | 0.71970 | −0.00771 | TSVM < B |
| 5 | 0.73505 | 0.72845 | −0.00660 | TSVM < B |
| 6 | 0.71531 | 0.72537 | +0.01006 | TSVM > B |
| 7 | 0.71449 | 0.70650 | −0.00799 | TSVM < B |
| 8 | 0.73175 | 0.73385 | +0.00210 | TSVM > B |
| 9 | 0.72528 | 0.73285 | +0.00757 | TSVM > B |

→ **TSVM > Baseline ở 6/10 seed** (s1, s2, s3, s6, s8, s9); **Baseline > TSVM ở 4/10** (s0, s4, s5, s7); **hòa 0**. Khớp cột `tsvm_wins_seeds = 6` `[VERIFIED]`.

### Box mAP@50-95 — `[VERIFIED]`

| Seed | Baseline | TSVM | Δ | | Seed | Baseline | TSVM | Δ |
| ---: | ---: | ---: | ---: |---| ---: | ---: | ---: | ---: |
| 0 | 0.75226 | 0.71251 | −0.03975 | | 5 | 0.74495 | 0.73980 | −0.00515 |
| 1 | 0.73278 | 0.74407 | +0.01129 | | 6 | 0.70833 | 0.72572 | +0.01739 |
| 2 | 0.72117 | 0.73151 | +0.01034 | | 7 | 0.70504 | 0.69919 | −0.00585 |
| 3 | 0.69053 | 0.72284 | +0.03231 | | 8 | 0.73306 | 0.74239 | +0.00933 |
| 4 | 0.74385 | 0.73128 | −0.01257 | | 9 | 0.72994 | 0.73591 | +0.00597 |

→ TSVM > Baseline ở **6/10 seed** `[VERIFIED]`.

---

## 10. SOURCE TRACE

```text
[Layer A]  20 × results.csv  (Ket_Qua_V2/KetQua_Nen/...  s{0..9}_w2)
              │  best epoch = idxmax('metrics/mAP50-95(M)')   [VERIFIED: đọc code dòng 55]
              │  đọc TRỰC TIẾP trong RAM, KHÔNG qua file trung gian
              ▼
[Script]   Stracth/generate_10seed_thesis_package.py   (mtime 29/09/2026 18:38:34, git clean)
              │  dòng  92 → 01_raw_analysis/raw_10seeds_extracted_metrics.csv   (18:39:29)
              │  dòng 281 → 03_metrics/segmentation/segmentation_metrics_summary.csv (18:39:30)
              │  dòng 808 → 06_reports/summary.csv                                (18:39:38)
              ▼
[Layer C]  summary.csv  ⊃  segmentation_metrics_summary.csv   [VERIFIED: 0/112 cell khác]

[Audit lần 2] Stracth/verify_10seed_audit.py (02/10/2026) → 07_audit/*
              → 694/694 PASS, 0 FAIL  [VERIFIED]
```

**Chi tiết các liên kết:**

| Liên kết | Trạng thái | Bằng chứng |
| :--- | :--- | :--- |
| 20 `results.csv` → `raw_10seeds_extracted_metrics.csv` | `[VERIFIED]` | Tái trích xuất độc lập: **max sai lệch = 0.0** trên 260 ô (13 metric × 20 run) |
| `df_raw` → `summary.csv` | `[VERIFIED]` | Tái tính 13 metric × 24 trường: **max sai số = 1.78e-15** |
| `df_raw` → `segmentation_metrics_summary.csv` | `[VERIFIED]` | Subset 4 dòng, 0/112 cell khác (cả raw string) |
| `summary.csv` ↔ 6 file trung gian (`02_statistics/*`, `03_metrics/*`) | `[VERIFIED]` | Đối chiếu: max sai số 9.95e-17 |
| `verify_10seed_audit.py` → `07_audit/*` | `[VERIFIED]` | 694/694 PASS, 0 FAIL (đọc lại `audit_report.csv`) |
| `raw_10seeds_extracted_metrics.csv` ↔ `reextracted_from_results_csv.csv` | `[VERIFIED]` | 0 khác biệt dữ liệu; khác **thứ tự cột** (`run_path` cột 5 vs 20) → không byte-identical |
| **Biến thể script thực thi → đường dẫn hiện tại** | `[UNVERIFIED]` | Xem §12.7 |

---

## 11. DISCREPANCY / AUDIT FINDINGS

### D1 — 3 dòng CM không khớp ảnh `confusion_matrix.png` của chính run đó `[DISCREPANCY]` — mức CAO

**Đã đọc trực tiếp 3 ảnh (không chỉ OCR):**

| Run | SOURCE A: `confusion_matrix.png` (đọc trực tiếp) | SOURCE B: `raw_10seeds_confusion_matrices.csv` | DIFFERENCE |
| :--- | :--- | :--- | :--- |
| TSVM s0 | TP=59, FN=68, FP=10, TN=0 | TP=108, FN=19, FP=8, TN=32 | ΔTP = **49** |
| TSVM s5 | TP=0, FN=127, FP=90, TN=0 | TP=112, FN=15, FP=7, TN=33 | ΔTP = **112** |
| TSVM s8 | TP=6, FN=121, FP=8, TN=0 | TP=111, FN=16, FP=14, TN=26 | ΔTP = **105** |

- 17/20 run còn lại: CSV khớp chính xác với ảnh `[VERIFIED]`.
- **Dòng tự kiểm của chính dự án** (`07_audit/audit_report.md`): *"17/20 lượt chạy có TP/FP/FN khớp chính xác confusion_matrix.png (đã đối chiếu bằng OCR). 3/20 lượt chạy TSVM (s0, s5, s8) không khớp."* → dự án **đã tự disclose** phát hiện này `[VERIFIED]`.

**Phân tích nguồn gốc (bằng chứng mới của audit này):**

| Kiểm tra | Kết quả | Trạng thái |
| :--- | :--- | :--- |
| CM-implied recall `TP/(TP+FN)` của **CSV** vs `mask_recall` (results.csv) cho 3 run | 0.85039/0.85286 (Δ0.0025), 0.88189/0.88189 (Δ0.0000), 0.87402/0.87675 (Δ0.0027) → **thỏa hơn mức trung bình** | `[DERIVED]` |
| CM-implied recall của **PNG** vs `mask_recall` | 0.4646/0.85286 (Δ0.388), 0.0000/0.88189 (Δ0.882), 0.0472/0.87675 (Δ0.830) → **mâu thuẫn trầm trọng** | `[DERIVED]` |
| Timestamp PNG vs results.csv (20 run) | 19/20 **bằng nhau tuyệt đối**; riêng **TSVM s5 PNG = 23/09 15:06:10, results.csv = 23/09 09:53:28 → lệch +312.7 phút** | `[VERIFIED]` |
| Cửa sổ thời gian trùng khớp | `diagnose_seed5.py` 14:36:10 → `re_evaluate_seed5.py` 15:04:33 → `data_bg20_val.yaml` 15:04:48 → `update_pairwise_seed5.py` 15:05:28 → **PNG s5 15:06:10** | `[VERIFIED]` |

**Đánh giá (không tự chọn số, chỉ nêu bằng chứng):**

```text
SOURCE A = confusion_matrix.png (3 run TSVM)
SOURCE B = raw_10seeds_confusion_matrices.csv
DIFFERENCE = ΔTP 49 / 112 / 105
POSSIBLE CAUSE =
   - s5: PNG BỊ GHI ĐÈ bởi script chẩn đoán (bằng chứng timestamp +312.7' khớp cửa sổ re_evaluate_seed5.py)
   - s0, s8: NGUYÊN NHÂN CHƯA XÁC ĐỊNH được (timestamp PNG == results.csv)
VERIFICATION STATUS = DISCREPANCY (s0, s5, s8) / UNVERIFIED (nguồn gốc s0, s8)
```

**Ảnh hưởng:** bảng CM và kết luận *"TSVM giảm FP 14.6 vs 16.8"* trong README §4 **phụ thuộc vào nguồn nào đúng**:

| Kịch bản | FP mean Baseline | FP mean TSVM | Hướng kết luận |
| :--- | ---: | ---: | :--- |
| Dùng CSV (nguồn hiện tại) | 16.80 | **14.60** | TSVM giảm FP |
| Thay 3 dòng bằng giá trị PNG | 16.80 | **22.50** | TSVM **tăng** FP → **đảo ngược** |

Bằng chứng thời gian + độ nhất quán với `results.csv` **nghiêng về phía CSV đúng, PNG sai** — nhưng vì không có prediction dump nào trong workspace để tái lập, trạng thái cuối vẫn là `[DISCREPANCY]`. **Không được dùng con số FP/TN này làm số liệu chính trong luận văn cho tới khi được tái lập.**

### D2 — TN là số tái dựng, không phải số đo `[DISCREPANCY — đã được dự án disclose]`

- `TN = 40 − FP` đúng ở **cả 20/20 dòng** `[VERIFIED]`.
- Lý do: Ultralytics `ConfusionMatrix.process_batch` không bao giờ cộng ô background/background → TN không tồn tại trong nguồn `[VERIFIED — đọc code]`.
- Hệ quả: `TN mean 23.2 (B) / 25.4 (T)` và mọi claim dạng "TN tăng", "specificity" là **suy diễn theo giả định**, không phải đo lường `[UNVERIFIED]`.
- Ngưỡng CM: `conf=0.25, IoU=0.45` `[VERIFIED]`.

### D3 — README liệt kê 2 file không tồn tại `[DISCREPANCY — mức THẤP, tài liệu]`

| File README §2 khai báo | Thực tế |
| :--- | :--- |
| `04_confusion_matrix/percentage/baseline_cm_percentage_per_seed.csv` | **KHÔNG tồn tại** |
| `04_confusion_matrix/percentage/tsvm_cm_percentage_per_seed.csv` | **KHÔNG tồn tại** |

`[VERIFIED — Test-Path = False]`. Thư mục `percentage/` chỉ có 2 file `*_mean_percentage.csv` + 2 PNG.

### D4 — Không kiểm được % CM từng seed `[UNVERIFIED]`

Chỉ có `*_cm_count_per_seed.csv` (2 file) và `*_cm_mean_percentage.csv` (2 file); không có bản percentage per-seed → không cross-check được % từng seed.

### D5 — Dice / IoU / F1 vắng mặt hoàn toàn `[UNVERIFIED]`

Xem §4.1. **Không có số liệu Dice/IoU/F1 verified nào để dùng trong luận văn.**

### D6 — Nhãn "độ biến thiên" trong `summary.md` `[DISCREPANCY — nhãn, mức THẤP]`

`summary.md` đặt cùng một ô: *"Tỉ lệ phương sai (F-ratio) = 2.75×"* và *"(Độ biến thiên giảm 39.5%)"*.

| Đại lượng | Giá trị | Đúng với nhãn nào |
| :--- | ---: | :--- |
| Giảm **std** | 39.5% (dùng std làm tròn 4 số) / **39.67%** (giá trị chính xác) | "độ biến thiên" (nếu hiểu = std) |
| Giảm **phương sai** | **63.6%** | "phương sai" |
| F-ratio = σ²_B/σ²_T | **2.75×** | đúng là tỷ lệ **phương sai** |

→ 39.5% **không phải** mức giảm phương sai. Nếu muốn nói "phương sai giảm 39.5%" thì **sai**; con số đúng là 63.6%. `[DERIVED]`

### D7 — Khoảng trống provenance của script `[UNVERIFIED]`

- `Stracth/generate_10seed_thesis_package.py` (git clean, mtime 29/09 18:38:34) hardcode `ROOT_OUT = ...\archive\KQ_Nen_DX_10seed` và `base_dir = ...\archive\KetQua_Nen\...` — **cả hai đường dẫn này ĐÃ KHÔNG CÒN TỒN TẠI** (đã bị chuyển vào `Ket_Qua_V2/` ở commit `92616d09`, 28/09).
- Nhưng output ghi lúc 18:39:29–38 nằm trong `Ket_Qua_V2\KQ_Nen_DX_10seed\`, và cột `run_path` trỏ tới `Ket_Qua_V2\KetQua_Nen\...`.
- Không tìm thấy bản sao script nào khác trong workspace/temp.
- `doc\18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md` **đã cảnh báo chính xác vấn đề này**: các biến path hardcoded ban đầu mang giá trị `archive\KQ_Nen_DX_10seed`, khi thực thi lại bắt buộc cập nhật sang `archive\Ket_Qua_V2\KQ_Nen_DX_10seed`.
- **Hệ quả:** không xác minh được biến thể code đã chạy (khả năng: patch path không commit, hoặc junction/symlink tạm đã gỡ). **Nếu chạy lại nguyên xi script hiện tại sẽ tạo thư mục mới ở root và `FileNotFoundError`** — vì vậy **không có rủi ro overwrite 2 file mục tiêu**.
- **Lưu ý:** khoảng trống này chỉ ảnh hưởng *provenance của script*, **không ảnh hưởng tính đúng đắn của dữ liệu** — vì toàn bộ số liệu đã được tái trích xuất độc lập từ 20 `results.csv` và khớp 100%.

### Kết luận kiểm discrepancy

| Hạng mục | Trạng thái |
| :--- | :--- |
| 13 metric × mean/std/min/max/median/range/best-worst seed/delta%/win-count/p-value/t-stat/Wilcoxon | **VERIFIED** — max sai số 1.78e-15 |
| `segmentation_metrics_summary.csv` ⊂ `summary.csv` | **VERIFIED** — 0/112 cell |
| 6 file trung gian vs `summary.csv` | **VERIFIED** — max sai số 9.95e-15 |
| 20 `results.csv` → `raw_10seeds_extracted_metrics.csv` | **VERIFIED** — max sai số 0.0 |
| CM nội bộ (count ↔ % ↔ mean, TP+FN=127, FP+TN=40) | **VERIFIED** |
| **CM 3 run TSVM s0/s5/s8 vs ảnh PNG** | **DISCREPANCY** |
| TN / Dice / IoU / F1 | **UNVERIFIED** (không phải số đo hoặc không tồn tại) |
| Provenance script | **UNVERIFIED** |

---

## 12. KẾT LUẬN KỸ THUẬT

Dựa **chỉ trên dữ liệu đã verified**:

**1. Hiệu năng trung bình — cải thiện rất nhỏ, KHÔNG có ý nghĩa thống kê** `[VERIFIED]`
- Mask mAP@50-95: 0.7210 → 0.7246 (**+0.0036, +0.49%**), p_ttest = 0.384, p_wilcoxon = 0.432.
- Box mAP@50-95: 0.7262 → 0.7285 (**+0.0023, +0.32%**), p = 0.715.
- **Cả 13 metric đều p > 0.05**, `statistically_significant_005 = False` ở 13/13 dòng. **Không thể khẳng định TSVM tốt hơn Baseline** ở ngưỡng α = 0.05.

**2. Metric GIẢM (không cải thiện)** `[VERIFIED]`
- **Mask mAP@50 giảm −0.0056 (−0.62%)** — Baseline thắng ở 7/10 seed.
- **Box mAP@50 giảm −0.0004 (−0.05%)** — hòa 5/5.
- **Val Cls Loss tăng +9.97%** (0.5591 → 0.6148) — Baseline thắng 8/10 seed, p = 0.094.
- **Val Box Loss tăng +0.91%**.

**3. Metric TĂNG** `[VERIFIED]`
- Box Recall +1.58% (largest relative gain), Mask Precision +1.05%, Box Precision +0.78%, Mask Recall +0.48%, Mask mAP50-95 +0.49%, Box mAP50-95 +0.32%.
- **Val Seg Loss giảm −4.76%** (1.3045 → 1.2424), TSVM thắng 8/10 seed, p = 0.091 — **gần ngưỡng 0.05 nhưng chưa đạt**.

**4. Ổn định qua seeds — cải thiện rõ rệt nhất** `[VERIFIED]`
- Std Mask mAP@50-95 giảm **39.67%** (0.012854 → 0.007755); phương sai giảm **63.6%**; F-ratio = **2.75×**.
- Range giảm 35.7% (0.04252 → 0.02735).
- Std giảm ở **tất cả 13/13 metric** `[DERIVED — xem bảng §8]`.
- Best Epoch std giảm từ 13.10 → 4.85 (giản nở hội tụ chặt hơn).
- → **Kết luận稳健 duy nhất mà dữ liệu hỗ trợ: TSVM cho kết quả ổn định hơn giữa các seed, không phải hiệu năng cao hơn.**

**5. Head-to-head per-seed** `[VERIFIED]`
- Mask mAP@50-95: TSVM > B ở **6/10 seed**.
- Box mAP@50-95: TSVM > B ở **6/10 seed**.
- Mask mAP@50: TSVM > B chỉ **3/10 seed**.
- Val Seg Loss: TSVM tốt hơn ở **8/10 seed**.

**6. Điểm CẦN KIỂM TRA THÊM (chưa dùng được trong luận văn)**
1. **CM của TSVM s0/s5/s8** — tái lập từ prediction dump hoặc chạy lại validation để xác định CSV hay PNG đúng. **Đừng trích con số FP/TN vào luận văn cho tới lúc đó.** `[DISCREPANCY]`
2. **TN, Dice, IoU, F1** — TN là số tái dựng; Dice/IoU/F1 không tồn tại. Nếu cần Dice/IoU cho luận văn phải **tính lại từ mask predicted** với định nghĩa được khai báo rõ. `[UNVERIFIED]`
3. **Sửa 2 file README khai báo sai** (`*_cm_percentage_per_seed.csv` không tồn tại). `[DISCREPANCY]`
4. **Sửa nhãn** "độ biến thiên giảm 39.5%" → nếu muốn nói phương sai thì phải là 63.6%. `[DISCREPANCY]`
5. **Khắc phục provenance** của `generate_10seed_thesis_package.py` (path hardcode đã chết) để có thể tái lập pipeline. `[UNVERIFIED]`

---

## 13. LIMITATIONS

1. Audit **chỉ đọc** — không training, không re-evaluate model, không sửa/xóa file dữ liệu gốc. File tạm chỉ ghi vào `%TEMP%\opencode\`.
2. **Không có prediction dump / kết quả inference thô** trong workspace → không thể tự tái lập confusion matrix; đây là nguyên nhân khiến D1 kẹt ở `DISCREPANCY`.
3. Ô TN **không bao giờ đo được** theo thiết kế Ultralytics → mọi metric suy từ TN (specificity, tỷ lệ TN) `[UNVERIFIED]`.
4. Dice/IoU/F1 **không tồn tại** trong dữ liệu → không audit được; mọi con số Dice/IoU trong báo cáo này là `[DERIVED]` nhằm chứng minh **không được đồng nhất với F1**.
5. Kiểm định thống kê với **n = 10 cặp seed** → sức mạnh kiểm định thấp; p = 0.091 (`val_seg_loss`) cần được diễn giải cẩn thận (không phải "gần significant" theo nghĩa chứng minh được).
6. Best epoch được chọn **trên chính tập validation** (`idxmax` trên `metrics/mAP50-95(M)` của val) → mAP báo cáo là **validation mAP tại best epoch**, có thiên lệch chọn mẫu; đây là quy ước chung của pipeline nhưng cần nêu trong luận văn.
7. Khoảng trống provenance của script (D7) khiến **không thể chứng minh pipeline sinh số đã được chạy đúng nguyên trạng**; bù lại số liệu đã được tái trích xuất độc lập và khớp 100%.
8. Timestamp file là bằng chứng gián tiếp — có thể bị ảnh hưởng bởi copy/sync file; kết luận về nguyên nhân PNG s5 dựa trên chuỗi bằng chứng khớp thời gian, không phải log trực tiếp.
