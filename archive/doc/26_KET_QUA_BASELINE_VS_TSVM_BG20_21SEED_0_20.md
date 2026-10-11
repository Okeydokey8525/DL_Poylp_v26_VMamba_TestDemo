# KẾT QUẢ SO SÁNH BASELINE YOLO26s-seg vs TSVM — BG20, SEED 0 → 20

> **Đề tài:** `CNTT_KLCN182` — Nghiên cứu tích hợp VMamba vào YOLO26-seg phân đoạn polyp  
> **Phạm vi:** Đối chiếu **2 mô hình** — **Baseline (`yolo26s-seg.pt`)** và **TSVM (`yolo26s-seg-TopologyShapeVMamba.yaml`)**  
> **Phạm vi seed:** **0 → 20 — đủ cả 21 seed cho cả 2 mô hình (N = 21)**  
> **Nguồn số liệu duy nhất:** `archive/Ket_Qua_V2/KetQua_Nen/*/*/results.csv` (đọc trực tiếp, không làm tròn tay)  
> **Quy tắc trích xuất:** Chỉ số tại **epoch tối ưu** = dòng có `metrics/mAP50-95(M)` lớn nhất (tương ứng `weights/best.pt`)  
> **Ngày cập nhật:** 10/10/2026 — đã bổ sung **TSVM seed 10**, nâng N từ 20 lên 21

---

## 0. TÓM TẮT NHANH (TL;DR)

| # | Kết luận | Bằng chứng |
| :---: | :--- | :--- |
| 1 | 🟡 **TSVM cải thiện Mask mAP@50-95 — đạt ngưỡng ý nghĩa ở α = 0.10 nhưng CHƯA đạt ở α = 0.05** — Δ = **+0.00412 (+0.57%)**, *p* = 0.0599, Cohen's d<sub>z</sub> = +0.44 | Bảng 1, mục 3 |
| 2 | **TSVM thắng đa số seed** — thắng **14/7**, kiểm định nhị phân *p* = 0.1892 → **chưa đủ bằng chứng** | Bảng 2, mục 4 |
| 3 | **Điểm mạnh rõ ràng nhất của TSVM là ĐỘ ỔN ĐỊNH** — std Mask mAP@50-95 giảm **38.2%**, phương sai co **2.61×** | Bảng 3, mục 5 |
| 4 | **Val Seg Loss thấp và ổn định hơn** — Δ = -0.02788 (-2.21%), std giảm **52.2%**, thắng **14/21** seed | Bảng 1, mục 3 |
| 5 | **TSVM đắt gấp đôi về thời gian** — 169.3 s/epoch vs 83.7 s/epoch (**2.02×**), tức 4.70 h vs 2.32 h cho 100 epoch | Bảng 4, mục 6 |
| 6 | **Điểm sàn cao hơn** — TSVM min = 0.70650 (s7) vs Baseline 0.69411 (s3), chênh **+0.01239** | Mục 5.2 |

> ⚠️ **Kết luận trung thực (đọc trước khi trích dẫn):** Với N = 21 cặp, **0 chỉ số** đạt ý nghĩa ở α = 0.05, **1 chỉ số** đạt ở α = 0.10. Mask mAP@50-95 có *p* = 0.0599 — **có ý nghĩa ở α = 0.10 nhưng chưa đạt ở α = 0.05**, và **95% CI vẫn chứa 0** ([-0.00019, +0.00843]). Đây là kết quả **tiệm cận ý nghĩa**, chưa đủ mạnh để kết luận TSVM vượt trội. Phát biểu an toàn: **TSVM cho hiệu năng tương đương hoặc nhỉnh hơn, ổn định hơn đáng kể, đổi lại thời gian huấn luyện gấp đôi**.

---

## 1. QUY MÔ THỰC NGHIỆM VÀ CẤU HÌNH

| Hạng mục | Giá trị |
| :--- | :--- |
| Tập dữ liệu | `Kvasir_YOLO_SEG_BG20` (`data_bg20.yaml`) |
| Mô hình Baseline | `yolo26s-seg.pt` (pretrained COCO) |
| Mô hình TSVM | `yolo26s-seg-TopologyShapeVMamba.yaml` (pretrained `yolo26s-seg.pt`) |
| Tập Validation | 160 ảnh = 120 ảnh polyp (**127** thực thể) + 40 ảnh nền âm tính |
| Số epoch | **100 / lượt chạy** — tất cả run đều đủ 100 epoch |
| Hyperparameter | Giống nhau hoàn toàn: `batch=8`, `imgsz=640`, `AdamW`, `lr0=0.001`, `lrf=0.01`, `cos_lr=False`, `close_mosaic=10`, `amp=False`, `deterministic=True` |
| Phần cứng | Kaggle GPU Tesla T4 |

### 1.1. Kiểm kê seed — ✅ ĐỦ CẢ 21 SEED (0 → 20)

| Mô hình | Thư mục | Số seed | Danh sách seed |
| :--- | :--- | :---: | :--- |
| Baseline | `KetQua_Nen/YOLOv26s-seg/` | 23 | 0–22 — **đủ 0–20**, dư 2 seed ngoài phạm vi |
| TSVM | `KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/` | 21 | 0–20 — **đủ cả 21 seed** ✅ |

**Số cặp seed dùng để so sánh ghép (paired): N = 21** — `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`

> ✅ **Cập nhật:** TSVM seed 10 đã được bổ sung (`Kvasir_BG20_YOLO26s_seg_TSVM_s10_w2`, 100 epoch, `args.yaml` xác nhận `seed: 10`, cấu hình khớp hoàn toàn với các run TSVM khác). Phạm vi **0 → 20 hiện đã đầy đủ cho cả 2 mô hình** — không còn thiếu hụt dữ liệu.

**Lưu ý về phạm vi phân tích:**

1. Yêu cầu là seed **0 → 20**, tức **21 giá trị seed** — mỗi giá trị đều có đủ 2 mô hình. ✅
2. Baseline có **2 seed ngoài phạm vi** (s21, s22) → **không đưa vào** kiểm định để giữ tính đối xứng (paired). Xem mục 4.3.
3. Toàn bộ phân tích dùng **N = 21 cặp**, tăng 1 so với phiên bản trước (N = 20).

---

## 2. DANH SÁC LƯỢT CHẠY ĐÃ PHÂN TÍCH

- **Baseline:** 23 thư mục × `results.csv` (23 cột, 100 dòng)
- **TSVM:** 21 thư mục × `results.csv` (23 cột, 100 dòng)
- **Tổng file đã đọc:** 44 — **tất cả đều đủ 100 epoch**, không có run bị cắt cụt
- **Cột đã dùng:** `metrics/mAP50-95(M)`, `metrics/mAP50(M)`, `metrics/precision(M)`, `metrics/recall(M)`, `metrics/mAP50-95(B)`, `metrics/mAP50(B)`, `metrics/precision(B)`, `metrics/recall(B)`, `val/box_loss`, `val/seg_loss`, `val/cls_loss`, `val/l1_loss`, `train/*_loss`, `time`
- **Cột bị loại:** `val/sem_loss` — bằng **0.0 tuyệt đối ở cả 43 run**, nên không mang thông tin.

---

## 3. BẢNG TỔNG HỢP CHỈ SỐ — SO SÁNH CHIẾU CẶP (N = 21)

*Bảng 1 — Bảng trung bình chính. `Δ = TSVM − Baseline`. Với Loss, Δ âm là tốt.*

| Chỉ số | Baseline (Mean ± Std) | TSVM (Mean ± Std) | Δ | % thay đổi | *p* (paired *t*) | *p* (Wilcoxon) | Thắng/Thua (seed) | Mô hình tốt hơn |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| Mask mAP@50-95 | 0.71882 ± 0.01147 | 0.72294 ± 0.00709 | +0.00412 | +0.57% | 0.0599 * | 0.0701 | 14/7 | TSVM |
| Mask mAP@50 | 0.90608 ± 0.01270 | 0.90827 ± 0.00835 | +0.00219 | +0.24% | 0.4922 ns | 0.6091 | 11/10 | TSVM |
| Mask Precision | 0.90429 ± 0.02803 | 0.91433 ± 0.02274 | +0.01004 | +1.11% | 0.2570 ns | 0.4948 | 12/9 | TSVM |
| Mask Recall | 0.85894 ± 0.02358 | 0.85895 ± 0.01748 | +0.00001 | +0.00% | 0.9991 ns | 0.9169 | 10/11 | TSVM |
| Box mAP@50-95 | 0.72284 ± 0.01554 | 0.72719 ± 0.01309 | +0.00435 | +0.60% | 0.2213 ns | 0.1032 | 14/7 | TSVM |
| Box mAP@50 | 0.89960 ± 0.01221 | 0.90115 ± 0.00825 | +0.00155 | +0.17% | 0.5944 ns | 0.7593 | 12/9 | TSVM |
| Box Precision | 0.90055 ± 0.02562 | 0.90659 ± 0.02316 | +0.00603 | +0.67% | 0.4241 ns | 0.4319 | 12/9 | TSVM |
| Box Recall | 0.84976 ± 0.02858 | 0.85213 ± 0.01415 | +0.00237 | +0.28% | 0.7293 ns | 0.9584 | 11/10 | TSVM |
| Val Seg Loss | 1.26197 ± 0.08452 | 1.23409 ± 0.04038 | -0.02788 | -2.21% | 0.2234 ns | 0.2722 | 7/14 | TSVM |
| Val Box Loss | 0.72776 ± 0.03646 | 0.72416 ± 0.03805 | -0.00360 | -0.50% | 0.7348 ns | 0.5392 | 7/14 | TSVM |
| Val Cls Loss | 0.59616 ± 0.07332 | 0.61296 ± 0.06665 | +0.01680 | +2.82% | 0.3504 ns | 0.5621 | 8/13 | Baseline |
| Val L1 Loss | 0.01631 ± 0.00101 | 0.01612 ± 0.00091 | -0.00019 | -1.17% | 0.4927 ns | 0.4948 | 9/12 | TSVM |
| Train Seg Loss | 0.84232 ± 0.12985 | 0.79769 ± 0.12368 | -0.04463 | -5.30% | 0.2847 ns | 0.3038 | 10/11 | TSVM |
| Train Box Loss | 0.60306 ± 0.09648 | 0.57382 ± 0.09848 | -0.02924 | -4.85% | 0.3720 ns | 0.3377 | 10/11 | TSVM |
| Train Cls Loss | 0.39926 ± 0.14403 | 0.36225 ± 0.13562 | -0.03701 | -9.27% | 0.4291 ns | 0.4120 | 9/12 | TSVM |
| Best Epoch | 86.47619 ± 11.43949 | 90.47619 ± 11.19651 | +4.00000 | +4.63% | 0.2933 ns | 0.1503 | 12/8 | — |

**Cách đọc:** `***` = *p* < 0.01 · `**` = *p* < 0.05 · `*` = *p* < 0.10 (tiệm cận ý nghĩa) · `ns` = không ý nghĩa.  
Cột **Thắng/Thua** = số seed mà **TSVM tốt hơn** / số seed **Baseline tốt hơn** (với Loss, "tốt hơn" nghĩa là **thấp hơn**).  
Cột **Mô hình tốt hơn** dựa trên **giá trị trung bình**, chưa cần ý nghĩa thống kê.

> 🟡 **Lưu ý về ngưỡng α:** Dấu `*` (*p* < 0.10) là ngưỡng **thường dùng trong thực nghiệm học sâu** vì cỡ mẫu hạn chế. Tuy nhiên, **ngưỡng chuẩn trong thống kê là α = 0.05** — và tại ngưỡng này, 0 chỉ số đạt ý nghĩa. Khi trích dẫn, **phải nêu rõ đang dùng ngưỡng nào**.

> 🔴 **Phát biểu bắt buộc khi trích dẫn Bảng 1:**
> *"Với N = 21 lượt chạy độc lập, **không chỉ số nào** đạt mức ý nghĩa thống kê ở ngưỡng α = 0.05. Chỉ số **Mask mAP@50-95** đạt ý nghĩa ở ngưỡng α = 0.10 thường dùng trong thực nghiệm học sâu (Δ = +0.00412, *p* = 0.0599), song khoảng tin cậy 95% vẫn chứa 0 ([-0.00019, +0.00843]) nên chưa thể khẳng định TSVM vượt trội Baseline. **Val Seg Loss** cho xu hướng giảm nhẹ (Δ = -0.02788, *p* = 0.2234)."*

### 3.1. Khoảng tin cậy 95% của chênh lệch trung bình

Khoảng tin cậy cho Δ cho biết mức chắc chắn của ước lượng:

| Chỉ số | Δ trung bình | 95% CI của Δ | Chứa 0? | Diễn giải |
| :--- | ---: | :--- | :---: | :--- |
| Mask mAP@50-95 | +0.00412 | [-0.00019, +0.00843] | **Có** | CI rộng, không loại được 0 |
| Box mAP@50-95 | +0.00435 | [-0.00284, +0.01155] | **Có** | CI rộng, không loại được 0 |
| Mask Precision | +0.01004 | [-0.00791, +0.02799] | **Có** | CI rộng, không loại được 0 |
| Mask Recall | +0.00001 | [-0.01164, +0.01165] | **Có** | CI rộng, không loại được 0 |
| Val Seg Loss | -0.02788 | [-0.07416, +0.01840] | **Có** | CI rộng, không loại được 0 |
| Val Cls Loss | +0.01680 | [-0.01985, +0.05345] | **Có** | CI rộng, không loại được 0 |

> **Nhận xét:** Cả 6 khoảng tin cậy đều **chứa 0** → chưa có bằng chứng thống kê rằng TSVM khác biệt thật sự so với Baseline. Để có kết luận chắc chắn, cần **tăng N** (xem mục 8.2).

---

## 4. SO SÁNH TỪNG SEED

*Bảng 2 — Chi tiết từng hạt giống. Chỉ số tại epoch tối ưu của mỗi run.*

| Seed | B: Best Ep | B: Mask mAP@50-95 | B: Val Seg Loss | T: Best Ep | T: Mask mAP@50-95 | T: Val Seg Loss | Δ Mask mAP | Δ Seg Loss | Thắng |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| 0 | 89 | 0.73663 | 1.3412 | 88 | 0.72451 | 1.2809 | -0.01212 | -0.0603 | Baseline |
| 1 | 98 | 0.71649 | 1.2788 | 98 | 0.72739 | 1.2630 | +0.01090 | -0.0158 | TSVM |
| 2 | 100 | 0.71377 | 1.3292 | 83 | 0.72591 | 1.1838 | +0.01214 | -0.1454 | TSVM |
| 3 | 61 | 0.69411 | 1.2881 | 89 | 0.72126 | 1.1777 | +0.02715 | -0.1103 | TSVM |
| 4 | 99 | 0.72741 | 1.4390 | 97 | 0.71970 | 1.2364 | -0.00771 | -0.2027 | Baseline |
| 5 | 94 | 0.73505 | 1.2022 | 90 | 0.72845 | 1.3020 | -0.00660 | +0.0998 | Baseline |
| 6 | 81 | 0.71531 | 1.2043 | 95 | 0.72537 | 1.2472 | +0.01006 | +0.0430 | TSVM |
| 7 | 71 | 0.71449 | 1.2447 | 88 | 0.70650 | 1.2371 | -0.00799 | -0.0076 | Baseline |
| 8 | 96 | 0.73175 | 1.4501 | 93 | 0.73385 | 1.2371 | +0.00210 | -0.2130 | TSVM |
| 9 | 84 | 0.72528 | 1.2679 | 96 | 0.73285 | 1.2586 | +0.00757 | -0.0094 | TSVM |
| 10 | 82 | 0.70452 | 1.1607 | 100 | 0.71982 | 1.2575 | +0.01530 | +0.0967 | TSVM |
| 11 | 99 | 0.72987 | 1.1349 | 87 | 0.72264 | 1.2725 | -0.00723 | +0.1375 | Baseline |
| 12 | 87 | 0.70556 | 1.3268 | 89 | 0.71569 | 1.1868 | +0.01013 | -0.1400 | TSVM |
| 13 | 97 | 0.73151 | 1.2072 | 99 | 0.73061 | 1.2865 | -0.00090 | +0.0793 | Baseline |
| 14 | 74 | 0.72232 | 1.3148 | 96 | 0.72107 | 1.2054 | -0.00125 | -0.1094 | Baseline |
| 15 | 80 | 0.71758 | 1.2646 | 84 | 0.72621 | 1.2185 | +0.00863 | -0.0461 | TSVM |
| 16 | 96 | 0.71248 | 1.2589 | 93 | 0.72374 | 1.2222 | +0.01126 | -0.0367 | TSVM |
| 17 | 73 | 0.72744 | 1.2427 | 100 | 0.73015 | 1.2111 | +0.00271 | -0.0315 | TSVM |
| 18 | 94 | 0.70220 | 1.2076 | 47 | 0.70821 | 1.1386 | +0.00601 | -0.0690 | TSVM |
| 19 | 71 | 0.71359 | 1.1622 | 91 | 0.71949 | 1.2343 | +0.00590 | +0.0722 | TSVM |
| 20 | 90 | 0.71778 | 1.1755 | 97 | 0.71829 | 1.2587 | +0.00051 | +0.0832 | TSVM |

**Tổng hợp thắng/thua (Mask mAP@50-95): TSVM thắng 14 — hòa 0 — Baseline thắng 7.**

### 4.1. Kiểm định nhị phân trên tỷ lệ thắng

- Giả thuyết H₀: xác suất TSVM thắng Baseline ở một seed ngẫu nhiên = 50%
- Quan sát: TSVM thắng **14/21** = 67%
- Kiểm định nhị phân chính xác (exact binomial, hai phía): ***p* = 0.1892** → **không có bằng chứng** TSVM thắng thường xuyên hơn

> Tỷ lệ thắng 14/21 **trông** thuận lợi cho TSVM, nhưng kiểm định nhị phân cho thấy tỷ lệ này **vẫn nằm trong miền dao động ngẫu nhiên** (*p* = 0.1892). Không được trích dẫn riêng tỷ lệ thắng như bằng chứng độc lập.

### 4.2. Nhận dạng seed nổi bật

- **Lợi thế lớn nhất của TSVM:** seed **3** (Δ = +0.02715)
- **Lợi thế lớn nhất của Baseline:** seed **0** (Δ = -0.01212)
- **Các seed chênh lệch nhỏ (|Δ| < 0.005):** 8, 13, 14, 17, 20 → phần lớn các seed gần như **ngang nhau**

### 4.3. Hai seed của Baseline nằm ngoài phạm vi (s21, s22)

Hai lượt chạy dưới đây **nằm ngoài phạm vi yêu cầu (seed 0 → 20)** nên không đưa vào kiểm định. Ghi lại để không ai vô tình dùng chúng:

| Seed | Best Ep | Mask mAP@50-95 | Mask mAP@50 | Box mAP@50-95 | Val Seg Loss |
| :---: | ---: | ---: | ---: | ---: | ---: |
| 21 | 75 | 0.70930 | 0.88838 | 0.70586 | 1.1981 |
| 22 | 84 | 0.70194 | 0.90669 | 0.69931 | 1.2221 |

> Cả 2 đều cho Mask mAP@50-95 dưới mức trung bình Baseline (0.71882). Việc Baseline có thêm các seed yếu **không làm thay đổi** kết luận so sánh.

---

## 5. ĐỘ ỔN ĐỊNH — ĐIỂM MẠNH THẬT SỰ CỦA TSVM

*Bảng 4 — So sánh mức co cụm phương sai giữa 2 mô hình.*

| Chỉ số | Std Baseline | Std TSVM | Giảm Std | Phương sai | Hệ số co | Range B | Range T | Giảm Range |
| :--- | ---: | ---: | ---: | :--- | ---: | ---: | ---: | ---: |
| Mask mAP@50-95 | 0.01147 | 0.00709 | +38.2% | 1.32e-04 → 5.03e-05 | 2.61× | 0.04252 | 0.02735 | +35.7% |
| Mask mAP@50 | 0.01270 | 0.00835 | +34.3% | 1.61e-04 → 6.98e-05 | 2.31× | 0.05080 | 0.03469 | +31.7% |
| Mask Precision | 0.02803 | 0.02274 | +18.9% | 7.86e-04 → 5.17e-04 | 1.52× | 0.10024 | 0.09468 | +5.5% |
| Mask Recall | 0.02358 | 0.01748 | +25.9% | 5.56e-04 → 3.06e-04 | 1.82× | 0.09449 | 0.06416 | +32.1% |
| Box mAP@50-95 | 0.01554 | 0.01309 | +15.8% | 2.42e-04 → 1.71e-04 | 1.41× | 0.06173 | 0.05014 | +18.8% |
| Box mAP@50 | 0.01221 | 0.00825 | +32.5% | 1.49e-04 → 6.80e-05 | 2.19× | 0.04286 | 0.03284 | +23.4% |
| Box Precision | 0.02562 | 0.02316 | +9.6% | 6.56e-04 → 5.37e-04 | 1.22× | 0.10429 | 0.08419 | +19.3% |
| Box Recall | 0.02858 | 0.01415 | +50.5% | 8.17e-04 → 2.00e-04 | 4.08× | 0.12996 | 0.05108 | +60.7% |
| Val Seg Loss | 0.08452 | 0.04038 | +52.2% | 7.14e-03 → 1.63e-03 | 4.38× | 0.31514 | 0.16346 | +48.1% |
| Val Box Loss | 0.03646 | 0.03805 | -4.3% | 1.33e-03 → 1.45e-03 | 0.92× | 0.13533 | 0.12520 | +7.5% |
| Val Cls Loss | 0.07332 | 0.06665 | +9.1% | 5.38e-03 → 4.44e-03 | 1.21× | 0.30027 | 0.29793 | +0.8% |
| Best Epoch | 11.44 | 11.20 | +2.1% | 1.31e+02 → 1.25e+02 | 1.04× | 39.00 | 53.00 | -35.9% |

### 5.1. Diễn giải

- **Mask mAP@50-95:** std giảm từ 0.01147 xuống 0.00709 (**38.2%**), phương sai co **2.61×**, range giảm **35.7%**.
- **Val Seg Loss:** std giảm từ 0.08452 xuống 0.04038 (**52.2%**) — mức co lớn nhất về loss, cho thấy hàm phân đoạn của TSVM **hoạt động đều hơn** qua các seed.
- **Best Epoch:** std giảm nhẹ (11.44 → 11.20), nhưng **range lại rộng hơn** (39 → 53 epoch) vì TSVM có seed s18 đạt đỉnh rất sớm (epoch 47). → **Không nên dùng Best Epoch làm luận điểm ổn định**.

> ⚠️ **Giới hạn khi diễn giải:** Giảm phương sai **không tự động** chứng minh TSVM "tốt hơn". Nó chỉ cho thấy kết quả **ít nhạy với lựa chọn hạt giống hơn** — đây là đóng góp thực nghiệm có giá trị, nhưng là **đặc tính khác** chứ không phải **đặc tính vượt trội**.

### 5.2. Giá trị cực trị — Mask mAP@50-95

| Mô hình | Min | Seed Min | Max | Seed Max | Median | Mean | Range |
| :--- | ---: | :---: | ---: | :---: | ---: | ---: | ---: |
| Baseline | 0.69411 | s3 | 0.73663 | s0 | 0.71758 | 0.71882 | 0.04252 |
| TSVM | 0.70650 | s7 | 0.73385 | s8 | 0.72374 | 0.72294 | 0.02735 |

**Đáy hiệu năng (worst-case floor):** TSVM nâng điểm sàn từ **0.69411** (Baseline, s3) lên **0.70650** (TSVM, s7) — chênh **+0.01239**.

**Trần hiệu năng:** TSVM đạt max 0.73385 (s8) vs Baseline 0.73663 (s0) — chênh **-0.00278**.

> **Vì sao quan trọng:** Trong ứng dụng thực tế, bạn huấn luyện **một** lần và cần kết quả **chắc chắn**. Ở đây Baseline có thể rơi xuống 0.69411 (dưới đáng kể so với trung bình), còn TSVM chỉ rơi xuống 0.70650. → TSVM **an toàn hơn về rủi ro triển khai**. Đây là lập luận mạnh hơn nhiều so với so sánh giá trị trung bình.

---

## 6. CHI PHÍ TÍNH TOÁN

*Bảng 4 — Thời gian huấn luyện (từ cột `time` của `results.csv`).*

| Mô hình | N run | Thời gian TB (giờ) | Std (giờ) | Giây/epoch TB | Std (s/ep) | So với Baseline |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | 23 | 2.324 | 0.115 | 83.68 | 4.13 | 1.00× |
| TSVM | 21 | 4.702 | 0.118 | 169.27 | 4.26 | **2.02×** |

> 🔴 **Chi phí:** TSVM tốn **2.02× thời gian** của Baseline. Với 100 epoch trên Tesla T4: **4.70 h** so với **2.32 h** — tức thêm khoảng **143 phút mỗi lượt chạy**.

**Đánh giá hiệu quả chi phí:**

- TSVM mua được **38.2% giảm độ biến thiên** (về mặt ổn định) và **+0.01239** cải thiện điểm sàn,
- đổi lại **nhân đôi thời gian huấn luyện** và **+0.57%** hiệu năng trung bình (ý nghĩa ở α = 0.10, chưa ở α = 0.05).
- → Nếu tiêu chí chính là **độ chính xác tuyệt đối**, TSVM **chưa đáng** chi phí này.
- → Nếu tiêu chí là **tính lặp lại và giảm rủi ro biến thiên**, TSVM **có lý do rõ ràng để dùng**.

---

## 7. ẢNH HƯỞNG CỦA VIỆC BỔ SUNG SEED 10 (N: 20 → 21)

Bổ sung TSVM seed 10 làm thay đổi **đáng kể** bức tranh thống kê. Đây là phần **quan trọng nhất** của bản cập nhật này.

*Bảng 5 — So sánh kết quả trước và sau khi bổ sung seed 10.*

| Chỉ số | N = 20 (trước) | N = 21 (sau) | Thay đổi |
| :--- | ---: | ---: | :--- |
| Mask mAP@50-95 — Δ | +0.00356 | **+0.00412** | Δ tăng |
| Mask mAP@50-95 — *p* (paired t) | 0.1048 | **0.0599** | 🟡 **vượt ngưỡng 0.10** |
| Mask mAP@50-95 — 95% CI | [-0.00082, +0.00794] | **[-0.00019, +0.00843]** | Biên dưới tiến gần 0 |
| Mask mAP@50-95 — số seed TSVM thắng | 13/20 | **14/21** | +1 thắng |
| Cohen's d<sub>z</sub> | +0.38 | **+0.44** | Tăng nhẹ |
| Val Seg Loss — Δ | -0.03411 | **-0.02788** | Hiệu ứng giảm nhẹ |
| Lực kiểm định (power) | 36.6% | **47.6%** | Tăng |

**Lý do:** seed 10 là một lượt chạy mà **TSVM thắng khá rõ** (Mask mAP@50-95: TSVM = 0.71982 vs Baseline = 0.70452, Δ = +0.01530). Đây là lượt thắng lớn thứ **hai** sau seed 3 (Δ = +0.02715). Thêm nó kéo trung bình TSVM lên và đẩy *p*-value giảm mạnh.

### 7.1. ⚠️ Cảnh báo về tính nhạy cảm của kết luận

> 🔴 **Đây là điểm cần đặc biệt lưu ý khi viết luận văn:**
>
> - Chỉ cần thêm **1 seed**, *p*-value của Mask mAP@50-95 chuyển từ **0.1048 → 0.0599**, tức **vượt qua ngưỡng α = 0.10**.
> - Điều này cho thấy kết luận **nhạy cảm với từng lượt chạy đơn lẻ** — hiệu ứng quan sát được vẫn **rất nhỏ**.
> - **Không nên** dùng kết quả *p* = 0.0599 để tuyên bố "TSVM vượt trội". Nếu bỏ seed 10 đi, kết luận sẽ ngược lại.
> - Cách diễn giải đúng: *"xu hướng cải thiện nhỏ, đạt ngưỡng ý nghĩa thống kê ở mức α = 0.10 nhưng chưa vững ở α = 0.05"*.

### 7.2. So sánh với báo cáo 10 seed trước đó

Tài liệu [`20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md`](20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md) dùng 10 seed (0–9). Bảng dưới đây kiểm tra tính nhất quán khi mở rộng lên 21 seed.

*Bảng 6 — Kiểm chứng chéo: cùng 10 seed đầu, tính lại từ `results.csv`.*

| Chỉ số | Báo cáo 10 seed (tài liệu 20) | Tính lại 10 seed (tài liệu này) | Khớp? |
| :--- | ---: | ---: | :---: |
| Mask mAP@50-95 — Baseline | 0.7210 ± 0.0129 | 0.7210 ± 0.0129 | ✅ |
| Mask mAP@50-95 — TSVM | 0.7246 ± 0.0078 | 0.7246 ± 0.0078 | ✅ |
| Val Seg Loss — Baseline | 1.3045 ± 0.0867 | 1.3045 ± 0.0867 | ✅ |
| Val Seg Loss — TSVM | 1.2424 ± 0.0387 | 1.2424 ± 0.0387 | ✅ |

- Chênh lệch Δ Mask mAP@50-95: **+0.00355** (N=10) → **+0.00412** (N=21) — **ổn định**, tăng rất nhẹ

> ✅ **Kiểm chứng thành công:** Kết quả tính lại **khớp tuyệt đối** với báo cáo 10 seed. Quy trình trích xuất nhất quán và đáng tin cậy.

---

## 8. KẾT LUẬN VÀ KHUYẾN NGHỊ

### 8.1. Bảng tổng hợp phán đoán

| Tiêu chí | Thắng | Nhận định |
| :--- | :--- | :--- |
| Mask mAP@50-95 (TB) | 🟡 **TSVM** | Δ = +0.00412 (+0.57%), *p* = 0.0599 — **ý nghĩa ở α=0.10, chưa ở α=0.05** |
| Box mAP@50-95 (TB) | ~Hòa | Δ = +0.00435, *p* = 0.2213 |
| Val Seg Loss (TB) | **TSVM** | Δ = -0.02788 (-2.21%), *p* = 0.2234 — giảm nhẹ |
| Độ ổn định (std) | 🏆 **TSVM** | Giảm std ở **13/15** chỉ số hiệu năng & loss; ngoại lệ: Val Box Loss, Train Box Loss |
| Tỷ lệ thắng theo seed | 🏆 **TSVM** | 14/21 — nhưng *p* = 0.1892, **chưa đủ bằng chứng** |
| Điểm sàn (worst case) | 🏆 **TSVM** | 0.70650 vs 0.69411 |
| Thời gian huấn luyện | 🏆 **Baseline** | TSVM chậm **2.02×** |

### 8.2. Đề xuất bước tiếp theo

1. **Tiếp tục tăng N** nếu muốn đưa kết luận lên mức ý nghĩa α = 0.05 một cách chắc chắn.
2. **Cần tăng N nếu muốn có kết luận thống kê chắc chắn.** Phân tích lực kiểm định (power analysis) cho hiệu ứng Mask mAP@50-95:
   - Hiệu ứng chuẩn hóa quan sát được: d = 0.435 (mức **nhỏ** theo quy ước Cohen)
   - **Lực kiểm định hiện tại (N = 21): 47.6%** — rất thấp, nghĩa là nếu TSVM thực sự tốt hơn, xác suất phát hiện ra là nhỏ
   - Cần **N ≈ 44 cặp** để đạt lực 80%, hoặc **N ≈ 58 cặp** để đạt lực 90%

   > ⚠️ **Ý nghĩa:** Nếu hiệu ứng thật chỉ khoảng +0.57%, cần tăng N lên khoảng **44 lượt chạy/cặp** (tức ~88 lượt chạy, ~309 giờ GPU) mới có thể khẳng định ở ngưỡng α = 0.05. Hiện tại lực kiểm định mới 48%, nên **kết quả dương ở α = 0.10 là chưa đủ chắc**.
3. **Nếu mục tiêu là tối ưu điểm số tuyệt đối, TSVM chưa đáng với 2× thời gian** — cải thiện +0.57% là rất nhỏ.
4. **Nên dùng TSVM nếu mục tiêu là tính lặp lại** — giảm 38.2% std và nâng điểm sàn là lợi thế thực nghiệm rõ ràng.
5. **Đào sâu tìm cải thiện điểm số tuyệt đối thay vì đổi kiến trúc.** Phần lớn run đạt đỉnh ở epoch ≥ 80 (Baseline 16/21, TSVM 20/21), cho thấy mô hình **gần hội tụ** ở 100 epoch. Nên thử **batch lớng hơn**, **nhiều epoch hơn**, hoặc **augmentation mạnh hơn** trước khi kết luận về giới hạn kiến trúc.

### 8.3. Cảnh báo về phát biểu

| ❌ KHÔNG được viết | ✅ Nên viết |
| :--- | :--- |
| "TSVM cải thiện mAP 0.6%" | "TSVM cho Mask mAP@50-95 cao hơn 0.57%, đạt ý nghĩa ở α = 0.10 (*p* = 0.060) nhưng chưa ở α = 0.05" |
| "TSVM vượt trội Baseline" | "TSVM cho hiệu năng **tương đương hoặc nhỉnh hơn**, độ biến thiên thấp hơn 38%, đổi lại thời gian gấp đôi" |
| "TSVM thắng 14/21 seed → TSVM tốt hơn" | "TSVM thắng 14/21 seed, nhưng chưa đủ bằng chứng thống kê (*p* = 0.189)" |
| "TSVM nhanh hơn" | "TSVM **chậm gấp đôi**, đổi lại ổn định cao hơn" |

---

## 9. PHỤ LỤC

### 9.1. Toàn bộ chỉ số thống kê đầy đủ

| Chỉ số | B Mean | B Std | B Min | B Max | T Mean | T Std | T Min | T Max | Δ | CI 95% | *p* (t) | *p* (W) | Cohen's dz |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- | ---: | ---: | ---: |
| Mask mAP@50-95 | 0.71882 | 0.01147 | 0.69411 | 0.73663 | 0.72294 | 0.00709 | 0.70650 | 0.73385 | +0.00412 | [-0.00019, +0.00843] | 0.0599 | 0.0701 | +0.435 |
| Mask mAP@50 | 0.90608 | 0.01270 | 0.88108 | 0.93188 | 0.90827 | 0.00835 | 0.89027 | 0.92496 | +0.00219 | [-0.00433, +0.00870] | 0.4922 | 0.6091 | +0.153 |
| Mask Precision | 0.90429 | 0.02803 | 0.85328 | 0.95352 | 0.91433 | 0.02274 | 0.85949 | 0.95417 | +0.01004 | [-0.00791, +0.02799] | 0.2570 | 0.4948 | +0.255 |
| Mask Recall | 0.85894 | 0.02358 | 0.81890 | 0.91339 | 0.85895 | 0.01748 | 0.82677 | 0.89093 | +0.00001 | [-0.01164, +0.01165] | 0.9991 | 0.9169 | +0.000 |
| Box mAP@50-95 | 0.72284 | 0.01554 | 0.69053 | 0.75226 | 0.72719 | 0.01309 | 0.69393 | 0.74407 | +0.00435 | [-0.00284, +0.01155] | 0.2213 | 0.1032 | +0.275 |
| Box mAP@50 | 0.89960 | 0.01221 | 0.87605 | 0.91891 | 0.90115 | 0.00825 | 0.88458 | 0.91742 | +0.00155 | [-0.00442, +0.00752] | 0.5944 | 0.7593 | +0.118 |
| Box Precision | 0.90055 | 0.02562 | 0.84923 | 0.95352 | 0.90659 | 0.02316 | 0.85949 | 0.94368 | +0.00603 | [-0.00939, +0.02145] | 0.4241 | 0.4319 | +0.178 |
| Box Recall | 0.84976 | 0.02858 | 0.77165 | 0.90161 | 0.85213 | 0.01415 | 0.82677 | 0.87785 | +0.00237 | [-0.01174, +0.01649] | 0.7293 | 0.9584 | +0.077 |
| Val Seg Loss | 1.26197 | 0.08452 | 1.13493 | 1.45007 | 1.23409 | 0.04038 | 1.13857 | 1.30203 | -0.02788 | [-0.07416, +0.01840] | 0.2234 | 0.2722 | -0.274 |
| Val Box Loss | 0.72776 | 0.03646 | 0.66545 | 0.80078 | 0.72416 | 0.03805 | 0.67509 | 0.80029 | -0.00360 | [-0.02550, +0.01829] | 0.7348 | 0.5392 | -0.075 |
| Val Cls Loss | 0.59616 | 0.07332 | 0.49582 | 0.79609 | 0.61296 | 0.06665 | 0.53301 | 0.83094 | +0.01680 | [-0.01985, +0.05345] | 0.3504 | 0.5621 | +0.209 |
| Val L1 Loss | 0.01631 | 0.00101 | 0.01473 | 0.01854 | 0.01612 | 0.00091 | 0.01493 | 0.01840 | -0.00019 | [-0.00076, +0.00038] | 0.4927 | 0.4948 | -0.153 |
| Train Seg Loss | 0.84232 | 0.12985 | 0.67891 | 1.03008 | 0.79769 | 0.12368 | 0.67037 | 1.10034 | -0.04463 | [-0.12933, +0.04006] | 0.2847 | 0.3038 | -0.240 |
| Train Box Loss | 0.60306 | 0.09648 | 0.48698 | 0.77890 | 0.57382 | 0.09848 | 0.46570 | 0.85754 | -0.02924 | [-0.09604, +0.03756] | 0.3720 | 0.3377 | -0.199 |
| Train Cls Loss | 0.39926 | 0.14403 | 0.21346 | 0.62072 | 0.36225 | 0.13562 | 0.22386 | 0.70976 | -0.03701 | [-0.13265, +0.05863] | 0.4291 | 0.4120 | -0.176 |
| Best Epoch | 86.48 | 11.44 | 61.00 | 100.00 | 90.48 | 11.20 | 47.00 | 100.00 | +4.00 | [-3.73, +11.73] | 0.2933 | 0.1503 | +0.236 |

### 9.2. Giải thích Cohen's d

| |d<sub>z</sub>| | Mức độ |
| :---: | :--- |
| < 0.2 | rất nhỏ — không đáng kể |
| 0.2 – 0.5 | nhỏ |
| 0.5 – 0.8 | trung bình |
| > 0.8 | lớn |

Hiệu ứng lớn nhất quan sát được: **Val Seg Loss** và **Mask mAP@50-95**, với |d<sub>z</sub>| ≈ 0.435 (mức **nhỏ**). Không chỉ số nào đạt mức trung bình hay lớn → xác nhận khác biệt rất nhỏ so với nhiễu ngẫu nhiên.

### 9.3. Phân tích lực kiểm định (power analysis)

Lực kiểm định = xác suất phát hiện đúng khác biệt khi khác biệt thật sự tồn tại.

| Chỉ số | Giá trị |
| :--- | ---: |
| Hiệu ứng chuẩn hóa *d* (Mask mAP@50-95) | 0.4352 |
| Lực kiểm định tại N = 21 (hiện tại) | **47.6%** |
| N cần thiết cho lực 80% (α = 0.05) | 44 cặp |
| N cần thiết cho lực 90% (α = 0.05) | 58 cặp |
| Thời gian ước tính cho N = 44 cặp | ~309 giờ GPU |

> **Kết luận:** Lực kiểm định ở ngưỡng α = 0.05 vẫn chỉ khoảng 48%. Kết quả *p* = 0.0599 đạt ngưỡng α = 0.10 là **tín hiệu tích cực**, nhưng **chưa đủ chắc chắn** để khẳng định TSVM vượt trội. Bổ sung nhiều seed hơn là hướng đi rõ ràng nhất.

### 9.4. Phương pháp thống kê

| Phương pháp | Mô tả | Lý do chọn |
| :--- | :--- | :--- |
| paired *t*-test | So sánh trung bình 2 mô hình trên **cùng một seed** | Cùng seed ⇒ cùng phân chia dữ liệu ⇒ loại bỏ biến nhiễu seed |
| Wilcoxon signed-rank | Phiên bản phi tham số của paired *t*-test | Kiểm tra kết luận có phụ thuộc giả định phân phối chuẩn hay không |
| Exact binomial test | Kiểm định tỷ lệ thắng | Không cần giả định phân phối cho N nhỏ |
| Cohen's d<sub>z</sub> | Hiệu ứng chuẩn hóa theo std của chênh lệch | Cho biết độ lớn thực tế, không chỉ tính ý nghĩa |
| 95% CI của Δ | Khoảng tin cậy của chênh lệch trung bình | Cho biết mức chắc chắn của ước lượng |

**Ngưỡng quyết định:** α = 0.05. Nếu *p* < 0.05 mới kết luận khác biệt có ý nghĩa.

### 9.5. Tính tái lập

Toàn bộ số liệu trong tài liệu này được trích xuất tự động bằng script đọc trực tiếp `results.csv`. Không có số liệu nào được nhập tay hoặc làm tròn thủ công.

**Quy trình tái lập:**

```text
1. Duyệt thư mục: Ket_Qua_V2/KetQua_Nen/YOLOv26s-seg/         → 23 run
2. Duyệt thư mục: Ket_Qua_V2/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/ → 21 run (đã có seed 10)
3. Với mỗi run: đọc results.csv → chọn dòng có metrics/mAP50-95(M) lớn nhất
4. Trích xuất 16 chỉ số tại dòng đó
5. Ghép cặp theo seed (chỉ giữ seed có đủ cả 2 mô hình) → N = 21
6. Tính Mean, Std, Min, Max, Median, Delta, CI 95%
7. Kiểm định: paired t-test, Wilcoxon signed-rank, exact binomial
```

---

## 10. GHI NHẬN VỀ PHẠM VI DỮ LIỆU

| Vấn đề | Mức độ | Xử lý |
| :--- | :---: | :--- |
| ~~TSVM thiếu seed 10~~ | ✅ Đã xử lý | Đã bổ sung; phạm vi 0–20 đầy đủ, N = 21 cặp |
| Kết quả nhạy cảm với từng seed | 🔴 Cao | Bổ sung 1 seed đã làm *p* đổi 0.105 → 0.0599; xem mục 7.1 |
| Lực kiểm định thấp (48% tại α = 0.05) | 🔴 Cao | Cần N ≈ 44 cặp để khẳng định; xem mục 9.3 |
| Baseline có 2 seed ngoài phạm vi (s21, s22) | 🟡 Thấp | Không đưa vào kiểm định ghép cặp; xem mục 4.3 |
| Cột `val/sem_loss` bằng 0 toàn bộ | 🟡 Thấp | Loại khỏi phân tích |
| Ma trận nhầm lẫn | 🟡 Thấp | Không đưa vào — phải OCR ảnh PNG, xem cảnh báo tại tài liệu 20 mục 0.2 |
| Specificity / TN | 🔴 Cao | **Không được trích dẫn** — Ultralytics không đo cột TN, giá trị là tái dựng giả định |
| Chỉ có 1 tập dữ liệu (Kvasir-SEG) | 🟡 Trung bình | Chưa có bằng chứng khái quát hoá sang tập khác |
| Chỉ 1 kiến trúc TSVM, 1 điểm chèn (P5/layer 10) | 🟡 Trung bình | Chưa khảo sát biến thể khác |

> **Lưu ý:** Các mục 🔴 và 🟡 ở trên **bắt buộc phải nêu** trong luận văn nếu trích dẫn số liệu từ tài liệu này.

---

**Ngày cập nhật:** 10/10/2026 — đã bổ sung TSVM seed 10  
**Phạm vi dữ liệu:** 44 run × 16 chỉ số = 704 giá trị  
**Cặp so sánh:** N = 21 (seed 0 → 20, đầy đủ cả 2 mô hình)  
**Tệp dữ liệu gốc:** `archive/Ket_Qua_V2/KetQua_Nen/`  
**Tài liệu liên quan:** [`20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md`](20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md), [`08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md`](08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md)