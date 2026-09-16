# BÁO CÁO KIỂM TOÁN KẾT QUẢ HUẤN LUYỆN (TRAINING RESULTS AUDIT REPORT)

**Dự án khóa luận:** *Nghiên cứu phương pháp tích hợp VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng.*  
**Đối tượng kiểm toán:** Toàn bộ lịch sử huấn luyện hiện có trong workspace (`archive/KQ_Poylp`).  
**Phương pháp kiểm toán:** AI Research Auditor – Đọc, xác thực và trích xuất số liệu thực tế 100% từ các file artifact (`results.csv`, `args.yaml`, `weights/best.pt`), **không tự huấn luyện lại, không sửa đổi mã nguồn, không suy đoán số liệu bị thiếu.**

---

## 1. EXECUTIVE SUMMARY (TÓM TẮT ĐIỀU HÀNH)

Qua quá trình rà soát toàn bộ không gian lưu trữ của dự án (`archive/KQ_Poylp`), kiểm toán viên ghi nhận **10 lượt huấn luyện (training runs) độc lập** cho bài toán phân đoạn polyp (**Task: `segment`**) thuộc hai dòng kiến trúc **YOLO26-seg (Baseline)** và **YOLO26-VMamba-seg (Mô hình đề xuất)**.

### Các phát hiện quan trọng nhất (Key Findings):
1. **Tính hoàn chỉnh của dữ liệu artifact:** Cả 10 run đều được lưu trữ đầy đủ các file cốt lõi bao gồm cấu hình, kết quả csv và file trọng số.
2. **Mô hình đạt hiệu quả tổng hợp tốt nhất (Baseline):**  
   - Biến thể **`Kvasir_YOLO26s_seg_100e_16b`** đạt chỉ số `Mask mAP50-95` cao nhất là **0.7280** (tại epoch 94).
3. **Hiệu năng của mô hình lai (YOLO26-VMamba-seg):**
   - Các biến thể tích hợp VMamba hiện tại đạt `Mask mAP50-95` từ **0.5439** đến **0.6095**, thấp hơn đáng kể so với baseline. Điều này là minh chứng rõ ràng cho việc mô hình hiện đang cần tinh chỉnh lại chiến lược huấn luyện hoặc tối ưu vị trí gắn `VMambaBlock`.
4. **Vấn đề "Nút thắt đường biên" ở Baseline:**  
   - Các mô hình baseline đều đạt `Mask mAP50` rất cao (>0.91), nhưng sụt giảm hơn 20% khi đánh giá ở `Mask mAP50-95`. Đây chính là động lực khoa học thực tiễn vững chắc nhất để tiếp tục nghiên cứu và hoàn thiện cơ chế VMamba nhằm cải thiện khả năng thu nhận ngữ cảnh toàn cục và chi tiết đường biên.

---

## 2. DANH SÁCH VÀ KẾT QUẢ CÁC RUN ĐÃ HUẤN LUYỆN

Bảng dưới đây tổng hợp kết quả chính xác được trích xuất từ 10 thư mục run trong workspace `archive/KQ_Poylp`:

| STT | Dòng Mô Hình | Tên Run (`run_name`) | Mask mAP50 | Mask mAP50-95 | Epoch tốt nhất |
| --: | :--- | :--- | :---: | :---: | :---: |
| 1 | Baseline | `Kvasir_YOLO26n_seg_100e_16b` | 0.9141 | 0.7238 | 89 |
| 2 | Baseline | `Kvasir_YOLO26s_seg_100e_16b` | 0.9282 | 0.7280 | 94 |
| 3 | Baseline | `Kvasir_YOLO26m_seg_100e_16b` | 0.9164 | 0.7084 | 80 |
| 4 | Baseline | `Kvasir_YOLO26l_seg_100e_16b` | 0.9169 | 0.7215 | 82 |
| 5 | Baseline | `Kvasir_YOLO26x_seg_100e_16b` | 0.9203 | 0.7116 | 92 |
| 6 | VMamba Lai | `Kvasir_YOLO26n_VMamba_seg_100e_16b` | 0.8365 | 0.6095 | 100 |
| 7 | VMamba Lai | `Kvasir_YOLO26s_VMamba_seg_100e_16b` | 0.8321 | 0.5883 | 100 |
| 8 | VMamba Lai | `Kvasir_YOLO26m_VMamba_seg_100e_16b` | 0.8122 | 0.5780 | 99 |
| 9 | VMamba Lai | `Kvasir_YOLO26l_VMamba_seg_100e_16b` | 0.8045 | 0.5439 | 76 |
| 10 | VMamba Lai | `Kvasir_YOLO26x_VMamba_seg_100e_16b` | 0.7897 | 0.5449 | 92 |

---

## 3. ĐÁNH GIÁ VÀ KHUYẾN NGHỊ KHOA HỌC CHO KHÓA LUẬN

1. **Về Baseline (YOLO26-seg):** Kết quả đạt được rất khả quan và ổn định, có thể sử dụng làm mốc đối chứng (benchmark) vững chắc cho đề tài.
2. **Về Mô hình lai VMamba:** Việc tích hợp `VMambaBlock` hiện đang làm giảm hiệu suất. Đề xuất:
   - Thay vì chỉ khởi tạo ngẫu nhiên khối VMamba, hãy thử xem xét lại Learning Rate, hoặc sử dụng Warm-up dài hơn vì kiến trúc State Space Model học rất khác CNN.
   - Thử đặt `VMambaBlock` ở phần Neck hoặc Head thay vì Backbone để giữ nguyên khả năng trích xuất đặc trưng của Backbone đã pre-train.
3. **Về Overfitting:** Có dấu hiệu mô hình bị underfit hoặc hội tụ chậm ở nhóm VMamba (bằng chứng là Epoch tốt nhất thường rơi vào 99 hoặc 100). Do đó, tăng `epochs` lên 200 hoặc 300 cho mô hình VMamba có thể mang lại kết quả tích cực hơn.

---
*Báo cáo được hoàn thành theo tiêu chuẩn kiểm toán khoa học nghiêm ngặt từ kết quả thực tế.*
