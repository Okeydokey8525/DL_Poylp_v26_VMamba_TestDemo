# 08. Ma trận nhầm lẫn

> **Cập nhật 28/10/2026:** số trong file này tính trên **20 seed** và là **bộ số dùng trong báo cáo**. Bộ 10 seed (chỉ đối chiếu) ở [06b_KET_QUA_10_SEED.md](06b_KET_QUA_10_SEED.md).

## Nguồn và cách kiểm tra

- Mỗi lượt có ảnh `confusion_matrix.png`, do Ultralytics vẽ khi đánh giá `best.pt` lúc kết thúc huấn luyện. Ảnh này **không** tương ứng với epoch cực đại mask dùng ở [06](06_KET_QUA_20_SEED.md).
- Số liệu dạng bảng có trong `KQ_Nen_DX_20seed_FP32/01_raw_analysis/raw_20seeds_confusion_matrices.csv`.
- Bộ tài liệu này đã **đọc lại cả 40 ảnh** `confusion_matrix.png`: ghép thành lưới rồi đọc số trên từng ô. Các giá trị đọc được lưu ở [bang/09_ma_tran_doc_tu_anh.csv](bang/09_ma_tran_doc_tu_anh.csv). So với CSV của gói phân tích thì **khớp 40/40 lượt** (TP, FP, FN).
- Ảnh không ghi ngưỡng confidence và IoU đã dùng. Vì vậy không suy ra ngưỡng lâm sàng từ bảng này.

## Cách đọc

Đơn vị là **đối tượng polyp**, không phải ảnh.

| Ô | Ý nghĩa |
|---|---|
| TP | Polyp thật được phát hiện đúng |
| FN | Polyp thật bị bỏ sót |
| FP | Dự đoán thừa: có thể nằm trên ảnh nền **hoặc** trên ảnh có polyp. Một ảnh có thể có nhiều FP |
| TN | **Không xác định (N/A)** |

Ở cả 40 lượt, TP + FN = 127, đúng bằng số polyp thật trong validation.

**Không được** tính TN = 40 − FP và không tính specificity hay accuracy theo ảnh. Lý do: FP không chỉ nằm trên 40 ảnh nền, và không phải mỗi ảnh chỉ có một FP. Một số CSV cũ có cột `TN_reconstructed = 40 − FP`. Cột này không hợp lệ.

## Kết quả (20 seed)

Nguồn: [bang/06_ma_tran_nham_lan_tung_seed.csv](bang/06_ma_tran_nham_lan_tung_seed.csv).

| | Baseline mean ± SD (min–max) | TSVM FP32 mean ± SD (min–max) | Δ mean | Wilcoxon p |
|---|---:|---:|---:|---:|
| TP | 110,55 ± 2,95 (104–116) | 110,65 ± 1,87 (108–114) | +0,10 | 1,000 |
| FN | 16,45 ± 2,95 (11–23) | 16,35 ± 1,87 (13–19) | −0,10 | 1,000 |
| FP | 16,45 ± 3,43 (10–22) | 15,75 ± 3,02 (12–24) | −0,70 | 0,671 |

- Hai mô hình gần như bằng nhau về số polyp phát hiện được, khoảng 110,6/127 (khoảng 87%).
- TSVM ít dự đoán thừa hơn trung bình 0,7 đối tượng, nhưng khác biệt không có ý nghĩa thống kê.
- TP và FN của TSVM có SD nhỏ hơn. Điều này khớp với quan sát về độ ổn định ở [06](06_KET_QUA_20_SEED.md).
- Tỉ lệ TP/127 ở đây là recall **tại ngưỡng của ma trận nhầm lẫn**, khác với Mask Recall ở bảng metric (Ultralytics chọn tại điểm F1 tốt nhất trên đường cong). Không trộn hai con số này.

## Hình cũ (đã chuyển vào lưu trữ)

Bộ hình mới vẽ lại từ CSV nằm ở `06_bao_cao/hinh/`. Các hình cũ dưới đây chỉ giữ để tham khảo.


- [12_confusion_matrix_mean_comparison.png](../99_luu_tru/hinh_cu/figures_20seed/12_confusion_matrix_mean_comparison.png)
- [13_confusion_matrix_mean_ultralytics.png](../99_luu_tru/hinh_cu/figures_20seed/13_confusion_matrix_mean_ultralytics.png)

Đã xem cả hai hình: ô nền/nền để "—" (TN không xác định), đúng với quy ước trên. Hình 12 đặt nhãn thật ở trục dọc, còn hình 13 theo kiểu Ultralytics (nhãn dự đoán ở trục dọc). Hình 12 làm tròn một chữ số thập phân nên ghi TP Baseline là 110,5 và FN TSVM là 16,4, trong khi giá trị chính xác là 110,55 và 16,35.
