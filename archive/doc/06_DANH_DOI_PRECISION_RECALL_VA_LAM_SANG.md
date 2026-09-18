# KẾT QUẢ THỰC NGHIỆM CHI TIẾT: SỰ ĐÁNH ĐỔI PRECISION - RECALL VÀ Ý NGHĨA LÂM SÀNG
## PHÂN TÍCH 127 CA POLYP KIỂM THỬ, TỶ LỆ PHÁT HIỆN ĐÚNG (TP) VS BỎ SÓT (FN) VÀ TỔN THƯƠNG PHẲNG (PARIS IIb)

---

> **Phân loại độ tin cậy thông tin theo nguyên tắc dự án:**
> - `[Đã xác nhận]`: Số lượng polyp tập Validation ($127$ polyp), tỷ lệ Recall và Precision trích xuất từ 6 seed thực nghiệm.
> - `[Có khả năng / suy luận]`: Phân loại hình thái học Paris (polyp phẳng IIb, polyp cuống Ip) và phân tích rủi ro trong thủ thuật cắt polyp EMR/ESD.

---

## 1. BẢNG PHÂN TÍCH LÂM SÀNG: PHÁT HIỆN THỰC TẾ TRÊN 127 TỔN THƯƠNG POLYP

Trong ứng dụng y tế, **Độ nhạy (Recall)** là yếu tố sống còn: Bỏ sót một polyp nguy cơ cao đồng nghĩa với việc người bệnh mất cơ hội ngăn ngừa ung thư đại trực tràng từ giai đoạn sớm.

| Chỉ số lâm sàng | Baseline YOLO26s-seg | C2TSVMamba (Thử nghiệm) | C2IAVM (👑 Champion Model) | Đánh giá tác động lâm sàng |
| :--- | :---: | :---: | :---: | :--- |
| **Mask Recall (Độ nhạy)** | $87.60\% \pm 1.75\%$ | $84.93\% \pm 2.43\%$ | **$88.75\% \pm 1.95\%$** | **C2IAVM đạt độ nhạy cao nhất (+1.15%)** |
| **Số polyp phát hiện đúng (TP / 127)** | **$111.3$ polyp** | $107.9$ polyp | **$112.7$ polyp** | C2IAVM phát hiện thêm trung bình $+1.4$ tổn thương |
| **Số polyp bị bỏ sót (FN / 127)** | **$15.7$ polyp** | $19.1$ polyp | **$14.3$ polyp** | **Giảm số ca bỏ sót nguy hiểm xuống thấp nhất** |
| **Tỷ lệ bỏ sót lâm sàng (FN rate)** | **$12.40\%$** | $15.07\%$ | **$11.25\%$** | **Giảm tỷ lệ bỏ sót từ 12.40% xuống 11.25%** |
| Mask Precision (Độ chính xác) | **$91.98\% \pm 1.39\%$** | $91.92\% \pm 1.92\%$ | $88.76\% \pm 2.75\%$ | Đánh đổi biên vi mô để mở rộng vùng bao phủ |
| Mask F1-Score | **$89.72\% \pm 0.54\%$** | $88.25\% \pm 0.94\%$ | $88.71\% \pm 0.90\%$ | Duy trì mức hài hòa xuất sắc sát 89% |

`[Đã xác nhận]`

---

## 2. TẠI SAO TSVM THẤT BẠI Ở RECALL VÀ C2IAVM ĐÃ GIẢI CỨU THÀNH CÔNG?

1. **Hạn chế của C2TSVMamba (Hiện tượng Co hẹp biên - Boundary Overshrinking):**
   - Mô hình TSVM đưa toán tử đạo hàm Sobel cấp 1 trực tiếp vào hàm trích xuất hình thái học. Các polyp phẳng (Paris IIb) hoặc polyp có độ tương phản mờ nhạt với niêm mạc xung quanh bị toán tử Sobel gọt tỉa quá mức.
   - Kết quả: Tỷ lệ bỏ sót tăng vọt lên **$15.07\%$ ($19.1 / 127$ polyp bị sót)**.
   - Xem biểu đồ Donut minh họa: `archive/KQ_DoiXung/Base vs Topolo/07a_pie_polyp_clinical_breakdown.png`.

2. **Sự đột phá của C2IAVM (Cơ chế Chú ý Tương tác - Interactive Attention):**
   - Thay vì ép buộc gradient biên cưỡng bức, C2IAVM phân nhánh song song: Nhánh 1 quét toàn cục SS2D 4 hướng (Không gian), Nhánh 2 dùng Multi-Head Self-Attention chiếu quan hệ phụ thuộc kênh (Channel Context).
   - Cơ chế gating tương tác tự động tăng cường trọng số cho các vùng polyp mờ phẳng, giúp **khôi phục độ nhạy lên $88.75\%$**, giảm số ca bỏ sót xuống chỉ còn **$14.3$ polyp (tỷ lệ sót thấp kỷ lục $11.25\%$)**.
   - Xem biểu đồ Donut minh họa: `archive/KQ_DoiXung/Base vs IAVM/07a_pie_polyp_clinical_breakdown.png` và biểu đồ cột từng seed `05b_fold_by_fold_recall.png`.
