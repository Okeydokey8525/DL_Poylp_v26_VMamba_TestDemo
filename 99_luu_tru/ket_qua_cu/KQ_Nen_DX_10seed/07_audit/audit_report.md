# BÁO CÁO KIỂM CHỨNG TỰ ĐỘNG — BỘ KẾT QUẢ 10 SEED (Baseline vs TSVM)

**Sinh tự động bởi:** `Stracth/verify_10seed_audit.py`
**Thời điểm chạy:** 02/10/2026 11:34:30
**Phạm vi:** 20 lượt chạy, 13 chỉ số

## Tổng kết

| Hạng mục | Số phép kiểm | Đạt | Không đạt |
| :--- | ---: | ---: | ---: |
| 1. results.csv | 1 | 1 | 0 |
| 2. raw | 17 | 17 | 0 |
| 3. mean_std | 104 | 104 | 0 |
| 4. min_max | 156 | 156 | 0 |
| 5. seed_cmp | 79 | 79 | 0 |
| 6. 03_metrics | 312 | 312 | 0 |
| 7. CM | 17 | 17 | 0 |
| 8. alt | 8 | 8 | 0 |
| **TỔNG** | **694** | **694** | **0** |


## Giới hạn còn lại của ma trận nhầm lẫn (không kiểm tự động được)

1. **Ô TN không phải số đo.** `ultralytics/utils/metrics.py`, hàm `ConfusionMatrix.process_batch` dòng 427–434, khi ảnh nền không có ground-truth code **chỉ cộng FP** rồi `return` — không có nhánh `matrix[self.nc, self.nc] += 1`. Ô background↔background luôn bằng 0, bị loại khỏi ghi nhãn (dòng 550) và hiển thị trống. Giá trị TN trong CSV **đúng bằng 40 − FP** ở cả 20 dòng → là **số tái dựng theo giả định**.
2. **17/20 lượt chạy** có TP/FP/FN khớp chính xác ảnh `confusion_matrix.png` (đã đối chiếu bằng OCR). **3/20 lượt chạy TSVM (s0, s5, s8) không khớp** — ảnh gốc cho thấy tỷ lệ phát hiện gần 0, mâu thuẫn với `results.csv` của chính các lượt chạy đó.
3. Vì vậy ma trận nhầm lẫn chỉ nên dùng như **quan sát mô tả**, không phải bằng chứng định lượng chính.

---
*Nguyên tắc: không bao giờ sửa tệp CSV gốc để cho khớp với báo cáo.*