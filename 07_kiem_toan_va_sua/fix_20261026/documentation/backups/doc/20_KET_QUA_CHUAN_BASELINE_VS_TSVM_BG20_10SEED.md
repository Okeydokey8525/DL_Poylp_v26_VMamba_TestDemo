# KẾT QUẢ THỰC NGHIỆM CHUẨN — BASELINE YOLO26s-seg vs TSVM (10 SEED, Kvasir-SEG BG20)

> **Đề tài:** `CNTT_KLCN182` — Nghiên cứu tích hợp VMamba vào YOLO26-seg phân đoạn polyp
> **Phạm vi:** Đối chiếu **2 mô hình** — **Baseline (YOLO26s-seg)** và **TSVM (YOLO26s-seg + Topology-Shape-aware VMamba)**
> **Cập nhật:** 02/10/2026 — **Số liệu đã được kiểm chứng lại 100% từ `results.csv` gốc**
> **Nguồn số liệu duy nhất (source of truth):** `archive/Ket_Qua_V2/KetQua_Nen/*/*/results.csv`

---

## 0. CAM KẾT TRUY XUẤT NGUỒN GỐC SỐ LIỆU

Tài liệu này là **điểm tham chiếu duy nhất** cho mọi con số Baseline/TSVM đưa vào báo cáo khóa luận cử nhận.

### 0.1. Quy trình trích xuất đã kiểm chứng

Từ **20 tệp `results.csv`** (Baseline `s0`–`s9`, TSVM `s0`–`s9`), mỗi tệp 100 epoch, tại
`archive/Ket_Qua_V2/KetQua_Nen/`:

1. Đọc từng tệp `results.csv` (23 cột, 100 dòng = 100 epoch).
2. Xác định **epoch tối ưu** = dòng có `metrics/mAP50-95(M)` lớn nhất (tương ứng `weights/best.pt`).
3. Trích xuất 15 chỉ số tại epoch đó.

**Kết quả kiểm chứng lại (đợt 02/10/2026):**

| Hạng mục kiểm chứng | Phạm vi | Kết quả |
| :--- | :--- | :---: |
| Đối chiếu ô-by-ô từ `results.csv` → `raw_10seeds_extracted_metrics.csv` | 20 run × 17 trường = 340 ô | **Sai số = 0 (khớp tuyệt đối)** |
| Toàn bộ bảng thống kê dẫn xuất (`02_statistics`, `03_metrics`, `06_reports/summary.csv`) | 559 phép kiểm | **0 sai lệch** |
| Đối chiếu với `Stracth/bg20_all_seeds_metrics.csv` | 20 run | **Sai số = 0** |

> **Kết luận:** Toàn bộ chỉ số **mAP, Precision, Recall, Loss, Best Epoch** trong báo cáo này là trung thực, có thể trích dẫn cho luận văn.

### 0.2. Cảnh báo về Ma trận Nhầm Lẫn (đọc mục 5 trước khi trích dẫn)

Dữ liệu ma trận nhầm lẫn **KHÔNG** được suy ra từ `results.csv`. Nó được đọc bằng **OCR** từ ảnh `confusion_matrix.png` của mỗi lượt chạy. Đợt kiểm chứng 02/10/2026 phát hiện 3 hạn chế mà luận văn **bắt buộc phải nêu**:

1. **17/20 lượt chạy**: TP / FP / FN khớp **chính xác** với ảnh `confusion_matrix.png`.
2. **3 lượt chạy TSVM (s0, s5, s8)**: số liệu trong CSV **không khớp** ảnh `confusion_matrix.png`. Ảnh của 3 run này thuộc một lượt validation bị lỗi (suy giảm recall gần 0: TP lần lượt 59, 0, 6 trên tổng 127 polyp), **mâu thuẫn với `results.csv` của chính các run đó** (recall 0.853 / 0.882 / 0.877). Ba dòng này **không thể kiểm chứng** từ bất kỳ artifact nào trong repository.
3. **Cột TN không hề được Ultralytics đo.** Trong `ultralytics/utils/metrics.py` (`ConfusionMatrix.process_batch`, dòng 427–434), khi một ảnh nền không có ground-truth, code **chỉ cộng FP** và **không có nhánh `matrix[self.nc, self.nc] += 1`**. Do đó ô background↔background luôn bằng 0 và hiển thị trống trên biểu đồ (dòng 550 loại bỏ các giá trị `< 0.005`). Cả 20 ảnh đều xác nhận ô này trống. Giá trị `TN` trong CSV **đúng bằng `40 − FP`** ở cả 20 dòng → đây là **số tái dựng theo giả định**, không phải số đo thực nghiệm.

> **Hệ quả thực tế:** Các phát biểu về **Specificity / TN** và phần lớn phát biểu về **giảm báo động giả (FP)** phải được diễn đạt là **quan sát mô tả trên tập kiểm định hiện tại**, không được dùng làm bằng chứng định lượng mạnh. Chi tiết ở mục 5.

---

## 1. QUY MÔ THỰC NGHIỆM VÀ CẤU HÌNH

| Hạng mục | Giá trị |
| :--- | :--- |
| Tập dữ liệu | `Kvasir_YOLO_SEG_BG20` (`data_bg20.yaml`) |
| Tổng số ảnh | 1.200 (1.000 ảnh Kvasir-SEG gốc + 200 ảnh nền âm tính `normal-cecum`) |
| Tập Train | 1.040 ảnh (880 ảnh polyp có nhãn đa giác + 160 ảnh nền rỗng) |
| Tập Validation | **160 ảnh** = 120 ảnh polyp (**127** polyp ground-truth) + 40 ảnh nền âm tính |
| Số lần chạy | **20** = 10 seed (0–9) × 2 mô hình |
| Số epoch | 100 / lượt chạy (tất cả 20 run đều đủ 100 epoch) |
| Quy tắc trích xuất | Chỉ số tại **epoch tối ưu** (`best.pt`, theo `metrics/mAP50-95(M)`) |
| Phần cứng | Kaggle GPU Tesla T4 |

> ⚠️ **Lưu ý diễn đạt:** Tập kiểm định có **160 ảnh** và **127 thực thể polyp**. Một số tài liệu cũ ghi "167 ảnh" — đây là **sai**, do cộng nhầm 127 *thực thể* với 40 *ảnh*. Không sử dụng con số 167.

---

## 2. BẢNG TỔNG HỢP CHỈ SỐ CHÍNH (Mean ± Std)

*Bảng 1 — So sánh định lượng 10 seed, Baseline vs TSVM (nguồn: `02_statistics/mean_std/full_comparison_mean_std.csv`)*

| Chỉ số | Baseline YOLO26s-seg | TSVM (đề xuất) | Δ (TSVM − Baseline) | % thay đổi | *p*-value (paired *t*-test) | Kết luận |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Mask mAP@50-95** | 0.7210 ± 0.0129 | **0.7246 ± 0.0078** | +0.0036 | +0.49% | 0.3839 | Không ý nghĩa |
| Mask mAP@50 | **0.9119 ± 0.0107** | 0.9062 ± 0.0082 | −0.0056 | −0.62% | 0.2273 | Không ý nghĩa |
| Mask Precision | 0.9023 ± 0.0339 | **0.9118 ± 0.0246** | +0.0095 | +1.05% | 0.5428 | Không ý nghĩa |
| Mask Recall | 0.8584 ± 0.0252 | **0.8625 ± 0.0173** | +0.0041 | +0.48% | 0.5907 | Không ý nghĩa |
| **Box mAP@50-95** | 0.7262 ± 0.0198 | **0.7285 ± 0.0141** | +0.0023 | +0.32% | 0.7152 | Không ý nghĩa |
| Box mAP@50 | **0.9011 ± 0.0116** | 0.9006 ± 0.0090 | −0.0004 | −0.05% | 0.9334 | Không ý nghĩa |
| Box Precision | 0.8992 ± 0.0326 | **0.9062 ± 0.0251** | +0.0070 | +0.78% | 0.5921 | Không ý nghĩa |
| Box Recall | 0.8434 ± 0.0337 | **0.8567 ± 0.0152** | +0.0133 | +1.58% | 0.2674 | Không ý nghĩa |
| **Val Seg Loss** | 1.3045 ± 0.0867 | **1.2424 ± 0.0387** | −0.0622 | −4.76% | 0.0908 | Tiệm cận α = 0.10 |
| Val Box Loss | **0.7239 ± 0.0434** | 0.7305 ± 0.0399 | +0.0066 | +0.91% | 0.7008 | Không ý nghĩa |
| Val Cls Loss | **0.5591 ± 0.0635** | 0.6148 ± 0.0884 | +0.0557 | +9.97% | 0.0943 | Tiệm cận α = 0.10 |
| Val L1 Loss | 0.0164 ± 0.0012 | **0.0162 ± 0.0009** | −0.0002 | −1.02% | 0.6995 | Không ý nghĩa |
| Best Epoch | 87.3 ± 13.10 | **91.7 ± 4.85** | +4.4 | +5.04% | 0.3149 | Không ý nghĩa |

> 🔴 **Phát biểu bắt buộc khi trích dẫn Bảng 1:**
> *"Với cỡ mẫu N = 10 lần chạy độc lập, **không chỉ số nào** đạt mức ý nghĩa thống kê ở ngưỡng α = 0.05. Các khác biệt về giá trị trung bình là **xu hướng thực nghiệm**, chưa đủ bằng chứng để bác bỏ giả thuyết không."*

---

## 3. ĐỘ ỔN ĐỊNH GIỮA CÁC SEED

*Bảng 2 — Mức co cụm phương sai khi bổ sung TSVM (nguồn: `02_statistics/min_max/metrics_min_max_range.csv`)*

| Chỉ số | Std Baseline | Std TSVM | Giảm Std | Phương sai | Hệ số co | Range Baseline | Range TSVM | Giảm Range |
| :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **Mask mAP@50-95** | 0.01285 | 0.00776 | **−39.7%** | 1.65e−4 → 6.02e−5 | **2.75×** | 0.04252 | 0.02735 | **−35.7%** |
| Mask mAP@50 | 0.01066 | 0.00822 | −22.9% | 1.14e−4 → 6.76e−5 | 1.68× | 0.03671 | 0.02636 | −28.2% |
| Mask Precision | 0.03390 | 0.02460 | −27.4% | 1.15e−3 → 6.05e−4 | 1.90× | 0.10024 | 0.08419 | −16.0% |
| Mask Recall | 0.02517 | 0.01732 | −31.2% | 6.34e−4 → 3.00e−4 | 2.11× | 0.07603 | 0.05326 | −30.0% |
| **Box mAP@50-95** | 0.01975 | 0.01410 | −28.6% | 3.90e−4 → 1.99e−4 | 1.96× | 0.06173 | 0.04488 | −27.3% |
| Box Recall | 0.03373 | 0.01523 | −54.8% | 1.14e−3 → 2.32e−4 | 4.90× | 0.11541 | 0.04320 | −62.6% |
| **Val Seg Loss** | 0.08666 | 0.03867 | **−55.4%** | 7.51e−3 → 1.49e−3 | **5.02×** | 0.24788 | 0.12429 | **−49.9%** |
| Best Epoch | 13.098 | 4.855 | **−62.9%** | 1.72e+2 → 2.36e+1 | **7.28×** | 39 | 15 | **−61.5%** |

**Giá trị cực trị (Min / Max / Median) — Mask mAP@50-95:**

| Mô hình | Min | Seed Min | Max | Seed Max | Median | Range |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Baseline | 0.69411 | s3 | 0.73663 | s0 | 0.720885 | 0.04252 |
| TSVM | 0.70650 | s7 | 0.73385 | s8 | 0.725640 | 0.02735 |

**Đáy hiệu năng (worst-case floor):** TSVM nâng đáy hiệu năng từ **0.6941** (Baseline, s3) lên **0.7065** (TSVM, s7) — chênh **+0.0124**. Đây là quan sát mô tả phân bố thực nghiệm; **không dùng riêng thống kê này để suy diễn nguyên nhân kiến trúc.**

---

## 4. SO SÁNH TỪNG SEED VÀ KIỂM ĐỊNH THỐNG KÊ

### 4.1. Bảng từng seed — Mask mAP@50-95

*Bảng 3 — Chi tiết từng hạt giống (nguồn: `02_statistics/seed_comparison/seed_by_seed_metrics_and_deltas.csv`)*

| Seed | Best Ep (B) | Mask mAP@50-95 (B) | Val Seg Loss (B) | Best Ep (T) | Mask mAP@50-95 (T) | Val Seg Loss (T) | Δ mAP | Mô hình thắng |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | 89 | **0.7366** | 1.3412 | 88 | 0.7245 | 1.2809 | −0.0121 | Baseline |
| 1 | 98 | 0.7165 | 1.2788 | 98 | **0.7274** | 1.2630 | +0.0109 | **TSVM** |
| 2 | 100 | 0.7138 | 1.3292 | 83 | **0.7259** | **1.1838** | +0.0121 | **TSVM** |
| 3 | 61 | 0.6941 | 1.2881 | 89 | **0.7213** | **1.1777** | **+0.0272** | **TSVM** |
| 4 | 99 | **0.7274** | 1.4390 | 97 | 0.7197 | 1.2364 | −0.0077 | Baseline |
| 5 | 94 | **0.7351** | **1.2022** | 90 | 0.7285 | 1.3020 | −0.0066 | Baseline |
| 6 | 81 | 0.7153 | 1.2043 | 95 | **0.7254** | 1.2472 | +0.0101 | **TSVM** |
| 7 | 71 | **0.7145** | 1.2447 | 88 | 0.7065 | 1.2371 | −0.0080 | Baseline |
| 8 | 96 | 0.7318 | 1.4501 | 93 | **0.7339** | 1.2371 | +0.0020 | **TSVM** |
| 9 | 84 | 0.7253 | 1.2679 | 96 | **0.7328** | 1.2586 | +0.0075 | **TSVM** |

### 4.2. Tỷ lệ thắng theo từng cặp seed

*Bảng 4 — Số seed TSVM thắng / Baseline thắng (nguồn: `02_statistics/seed_comparison/seed_win_loss_summary.csv`)*

| Chỉ số | TSVM thắng | Baseline thắng | Hòa | TSVM thắng ở seed |
| :--- | :---: | :---: | :---: | :--- |
| **Mask mAP@50-95** | **6/10** | 4/10 | 0 | 1, 2, 3, 6, 8, 9 |
| **Box mAP@50-95** | **6/10** | 4/10 | 0 | 1, 2, 3, 6, 8, 9 |
| Mask mAP@50 | 3/10 | 7/10 | 0 | — |
| Mask Precision | 5/10 | 5/10 | 0 | — |
| Mask Recall | 6/10 | 4/10 | 0 | — |
| Box mAP@50 | 5/10 | 5/10 | 0 | — |
| Box Precision | 5/10 | 5/10 | 0 | — |
| Box Recall | 6/10 | 4/10 | 0 | — |
| **Val Seg Loss** *(thấp hơn = thắng)* | **8/10** | 2/10 | 0 | 0, 1, 2, 3, 4, 7, 8, 9 |
| Val Box Loss *(thấp hơn = thắng)* | 6/10 | 4/10 | 0 | — |
| Val Cls Loss *(thấp hơn = thắng)* | 2/10 | 8/10 | 0 | — |
| Val L1 Loss *(thấp hơn = thắng)* | 6/10 | 4/10 | 0 | — |
| Best Epoch *(cao hơn = thắng)* | 4/10 | 5/10 | 1 | — |

### 4.3. Kiểm định thống kê đầy đủ

*Bảng 5 — Paired t-test và Wilcoxon signed-rank (nguồn: `03_metrics/*/*_summary.csv`)*

| Chỉ số | *t* | *p* (*t*-test) | *W* | *p* (Wilcoxon) | Kết luận ở α = 0.05 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| Mask mAP@50-95 | +0.9153 | 0.3839 | 19.0 | 0.4316 | Không ý nghĩa |
| Mask mAP@50 | −1.2957 | 0.2273 | 16.0 | 0.2754 | Không ý nghĩa |
| Mask Precision | +0.6326 | 0.5428 | 22.0 | 0.6250 | Không ý nghĩa |
| Mask Recall | +0.5577 | 0.5907 | 22.0 | 0.6250 | Không ý nghĩa |
| Box mAP@50-95 | +0.3766 | 0.7152 | 20.0 | 0.4922 | Không ý nghĩa |
| Box mAP@50 | −0.0859 | 0.9334 | 25.0 | 0.8457 | Không ý nghĩa |
| Box Precision | +0.5555 | 0.5921 | 20.0 | 0.4922 | Không ý nghĩa |
| Box Recall | +1.1824 | 0.2674 | 16.0 | 0.2754 | Không ý nghĩa |
| **Val Seg Loss** | **−1.8939** | **0.0908** | 10.0 | 0.0840 | Tiệm cận α = 0.10 |
| Val Box Loss | +0.3967 | 0.7008 | 25.0 | 0.8457 | Không ý nghĩa |
| Val Cls Loss | +1.8698 | 0.0943 | 10.0 | 0.0840 | Tiệm cận α = 0.10 |
| Val L1 Loss | −0.3986 | 0.6995 | 24.0 | 0.7695 | Không ý nghĩa |

**Diễn giải chuẩn học thuật (dùng nguyên văn hoặc tương đương):**
> *"Trên mẫu 10 lần chạy độc lập, TSVM cho thấy **xu hướng cải thiện nhẹ** ở giá trị trung bình Mask mAP@50-95 (+0.0036, +0.49%) kèm **độ co cụm phương sai đáng kể** (Std giảm 39.7%, phương sai giảm 2.75 lần) và **giảm hàm mất mát phân đoạn** (−4.76%, *p* = 0.0908, tiệm cận ngưỡng α = 0.10). Tuy nhiên, **không chỉ số nào đạt ý nghĩa thống kê ở α = 0.05** với cỡ mẫu N = 10. Vì vậy, đóng góp quan trọng nhất quan sát được của TSVM nằm ở **nâng cao độ ổn định khởi tạo** và **giảm biến thiên giữa các lần chạy**, chứ chưa phải cải thiện hiệu năng tuyệt đối."*

---

## 5. MA TRẬN NHẦM LẪN (ĐỌC KỸ MỤC 0.2 TRƯỚC)

### 5.1. Số đếm trung bình

*Bảng 6 — Ma trận nhầm lẫn trung bình 10 seed (nguồn: `04_confusion_matrix/count/*_cm_mean_count.csv`)*

| | Baseline (Mean ± Std) | TSVM (Mean ± Std) | Δ |
| :--- | :---: | :---: | :---: |
| **True Polyp → Pred Polyp (TP)** | 110.3 ± 3.40 | **111.2 ± 2.20** | +0.9 |
| **True Polyp → Pred Background (FN)** | 16.7 ± 3.40 | **15.8 ± 2.20** | −0.9 |
| **True Background → Pred Polyp (FP)** | 16.8 ± 2.35 | **14.6 ± 4.35** | −2.2 |
| **True Background → Pred Background (TN)** ⚠️ | 23.2 ± 2.35 *(suy dựng)* | **25.4 ± 4.35** *(suy dựng)* | +2.2 |

*Bảng 7 — Ma trận nhầm lẫn chuẩn hóa (%)*

| | Baseline | TSVM |
| :--- | :---: | :---: |
| True Polyp | 86.85% TP / 13.15% FN | 87.56% TP / 12.44% FN |
| True Background | 42.00% FP / 58.00% TN ⚠️ | 36.50% FP / 63.50% TN ⚠️ |

### 5.2. ⚠️ Hạn chế bắt buộc phải nêu

| Vấn đề | Mức độ | Cách xử lý trong luận văn |
| :--- | :--- | :--- |
| Ô **TN không được Ultralytics đo** (luôn = 0 trên ảnh) | 🔴 Nghiêm trọng | Chỉ trích dẫn **FP** (được đo thật). Với TN/Specificity phải ghi rõ *"suy dựng theo giả định 40 − FP"*. |
| **TSVM s0, s5, s8** không khớp ảnh CM | 🔴 Nghiêm trọng | Nêu rõ 3/20 lượt chạy không kiểm chứng được. **Không** dùng CM làm bằng chứng chính. |
| Giả định ≤ 1 FP/ảnh nền khi suy dựng TN | 🟡 Trung bình | Nêu là giả định. |
| Ngưỡng CM | ℹ️ Thông tin | `conf = 0.25`, `IoU = 0.45` (mặc định Ultralytics). |

**Phát biểu an toàn được phép dùng:**
> *"Trên 40 ảnh nền âm tính của tập kiểm định, số báo động giả trung bình của TSVM là 14.6 so với 16.8 của Baseline (Δ = −2.2). Đây là **quan sát mô tả** trên một tập kiểm định đơn lẻ tại một ngưỡng quyết định cố định; chưa đủ cơ sở để kết luận về nguyên nhân cơ chế kiến trúc."*

**Phát biểu KHÔNG được dùng:** ❌ *"TSVM tăng Specificity lên 70.5%"*, ❌ *"TSVM chứng minh loại bỏ được ảnh giả"*, ❌ *"TSVM nhận diện thêm 1.4 ca polyp so với Baseline"*.

---

## 6. CHI PHÍ TÍNH TOÁN VÀ KHẢ NĂNG TRIỂN KHAI

*Bảng 8 — Đo đạc phần cứng, GPU Tesla T4, đầu vào 640×640 (nguồn: `efficiency_benchmark/tables/efficiency_summary.csv`)*

| Chỉ số | Baseline | TSVM | Δ |
| :--- | :---: | :---: | :---: |
| Số tham số | 11.55 M | 12.16 M | +0.61 M (+5.28%) |
| GFLOPs | 42.3 | 47.4 | +5.1 (+12.06%) |
| Kích thước `.pt` | 23.8 MB | 25.1 MB | +1.3 MB (+5.46%) |
| Độ trễ suy luận | 17.2 ms | 19.8 ms | +2.6 ms |
| Tốc độ khung hình | 58.1 FPS | 50.5 FPS | −7.6 FPS |
| Peak VRAM | 1.42 GB | 1.68 GB | +0.26 GB |

**Kết luận khả thi:** 50.5 FPS vượt ngưỡng 25–30 FPS của hệ thống nội soi tiêu chuẩn (Olympus EVIS X1, Fujifilm ELUXEO 7000). Mức tăng chi phí tính toán +12.06% GFLOPs là chấp nhận được.

---

## 7. HÌNH ẢNH KHUYẾN NGHỊ CHO LUẬN VĂN

*Bảng 9 — Ánh xạ hình ảnh → nội dung khoa học (tất cả đều tồn tại, đã kiểm tra)*

| Mã | Đường dẫn | Nội dung |
| :--- | :--- | :--- |
| H1 | `05_charts/performance/01_mask_map50_95_comparison.png` | So sánh Mean ± Std Mask mAP@50-95 |
| H2 | `05_charts/performance/03_precision_recall_comparison.png` | Đánh đổi Precision / Recall |
| H3 | `05_charts/performance/05_val_seg_loss_comparison.png` | So sánh Validation Seg Loss |
| H4 | `05_charts/stability/10_mean_std_errorbars.png` | Thanh sai số Mean ± Std đa chỉ số |
| H5 | `05_charts/stability/06_seed_mask_map50_95_trends.png` | Diễn biến Mask mAP@50-95 qua 10 seed |
| H6 | `05_charts/distribution/08_boxplot_mask_map50_95.png` | Boxplot + điểm dữ liệu phân tán |
| H7 | `05_charts/summary/18_grouped_bar_main_metrics.png` | Grouped bar 6 chỉ số chính |
| H8 | `05_charts/summary/20_delta_tsvm_vs_baseline.png` | Thanh ngang độ lệch Δ (TSVM − Baseline) |
| H9 | `figures/04_convergence_loss_curves.png` | Đường cong hội tụ 4 hàm mất mát 100 epoch |
| H10 | `figures/11_boxplot_variance_stability.png` | Boxplot + jitter độ ổn định phương sai |
| H11 | `figures/12_confusion_matrix_mean_comparison.png` | Ma trận nhầm lẫn chuẩn hóa ⚠️ (xem mục 5.2) |
| H12 | `figures/14_confusion_cells_grouped_barchart.png` | Cột nhóm so sánh TP/FN/FP/TN ⚠️ (xem mục 5.2) |

**Hệ quy ước đặt tên:** Hình CM **không nên đặt là hình chính** trong luận văn do các hạn chế mục 5.2. Nếu dùng, phải kèm chú thích nêu rõ hạn chế.

---

## 8. DANH SÁCH TỆP DỮ LIỆU GỐC ĐỂ ĐỐI CHIẾU

| Cấp | Đường dẫn | Vai trò |
| :--- | :--- | :--- |
| **Nguồn gốc duy nhất** | `KetQua_V2/KetQua_Nen/YOLOv26s-seg/*/results.csv` | 10 file — Baseline |
| **Nguồn gốc duy nhất** | `KetQua_V2/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/*/results.csv` | 10 file — TSVM |
| Trích xuất | `KQ_Nen_DX_10seed/01_raw_analysis/raw_10seeds_extracted_metrics.csv` | 20 dòng, 15 chỉ số |
| Thống kê | `KQ_Nen_DX_10seed/02_statistics/mean_std/full_comparison_mean_std.csv` | Bảng 1 |
| Thống kê | `KQ_Nen_DX_10seed/02_statistics/min_max/metrics_min_max_range.csv` | Bảng 2 |
| Thống kê | `KQ_Nen_DX_10seed/02_statistics/seed_comparison/seed_by_seed_metrics_and_deltas.csv` | Bảng 3 |
| Thống kê | `KQ_Nen_DX_10seed/02_statistics/seed_comparison/seed_win_loss_summary.csv` | Bảng 4 |
| Kiểm định | `KQ_Nen_DX_10seed/03_metrics/{segmentation,bounding_box,loss}/*_summary.csv` | Bảng 5 |
| Ma trận | `KQ_Nen_DX_10seed/01_raw_analysis/raw_10seeds_confusion_matrices.csv` ⚠️ | Bảng 6, 7 |
| Hiệu năng | `KQ_Nen_DX_10seed/efficiency_benchmark/tables/efficiency_summary.csv` | Bảng 8 |
| Script sinh | `Stracth/generate_10seed_thesis_package.py` | Tái tạo `01`–`06` |
| Script sinh | `Stracth/render_kq_doixung_templates_2models.py` | Tái tạo `figures/` |

---

## 9. GIỚI HẠN NGHIÊN CỨU CẦN NÊU

1. **Cỡ mẫu thống kê nhỏ.** N = 10 lượt chạy / mô hình. Với độ lệch chuẩn quan sát được, cần ước lượng công suất thống kê để biết cần bao nhiêu seed mới đủ sức phát hiện Δ = +0.0036 ở α = 0.05.
2. **Đơn trung tâm.** Toàn bộ dữ liệu đến từ Kvasir (Na Uy). Cần kiểm chứng đa trung tâm (CVC-ClinicDB, BKAI-IGH, ETIS-LaribPolypDB) để đánh giá khả năng tổng quát hóa ngoại suy.
3. **Ma trận nhầm lẫn chưa kiểm chứng đầy đủ.** 3/20 lượt chạy không đối chiếu được; cột TN là số tái dựng (mục 5.2).
4. **Chưa có phân tích ablation đầy đủ** trên tập BG20 10 seed cho các thành phần của TSVM.
5. **Ảnh hưởng tốc độ hội tụ.** TSVM đạt Best Epoch trung bình cao hơn (91.7 vs 87.3) — có thể phản ánh tốc độ hội tụ chậm hơn, cần đánh giá thêm trên cấu hình epoch khác.

---

*Tài liệu này được tạo và kiểm chứng ngày 02/10/2026. Mọi số liệu trích dẫn cho khóa luận cử nhận phải lấy từ đây hoặc từ các tệp CSV được liệt kê ở mục 8.*
