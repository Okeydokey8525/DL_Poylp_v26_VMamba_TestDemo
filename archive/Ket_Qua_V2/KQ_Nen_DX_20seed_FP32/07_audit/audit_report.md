# Kiểm tra nguồn và tính tái lập

- 40/40 results.csv đủ 100 epoch liên tục và không có NaN số học.
- Trích lại toàn bộ metric có sẵn trong CSV gốc, khớp tuyệt đối trong sai số 1e-12.
- Đọc thêm val/box_loss, val/cls_loss, val/l1_loss và val/sem_loss trực tiếp từ results.csv.
- Chỉ dùng nhánh `Kvasir_BG20_YOLO26s_seg_TSVM_FP32`, không đọc TSVM cũ.
- 20 cặp seed 0–19. 16/40 epoch max mask khác epoch fitness sum mask+box.
- TP+FN=127 cho 40 dòng, TN trống 40 dòng; bỏ TN_reconstructed trong bảng dẫn xuất.
- SHA256 của nguồn và phiên bản thư viện ở JSON kèm theo. Hash giúp phát hiện thay đổi, không tự chứng minh nội dung OCR đúng.
- Không sửa CSV gốc, facts.json, summary_20seeds_paired.csv hoặc figures gốc.
- Không huấn luyện, không inference, không đổi checkpoint.
