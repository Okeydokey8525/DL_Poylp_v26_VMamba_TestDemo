# KẾT LUẬN

> **Ghi chú soạn thảo (xóa khi ghép Word):** bản rút gọn, nén từ `md_bao_cao/09_KET_LUAN.md` (tag git `ban_day_du_147`). Mọi con số lấy lại từ Chương 6, không có số mới, không trích tài liệu mới.

## 1. Kết quả đạt được

Đề tài đã thực hiện đủ chu trình đặt ra trong đề cương:
- **Khảo sát và lý thuyết:** hệ thống hóa các hướng phân đoạn polyp từ CNN, Transformer, họ YOLO đến Mamba và VMamba; chỉ ra khoảng trống về việc đưa VMamba vào YOLO26-seg cho phân đoạn polyp có đánh giá nhiều seed.
- **Dữ liệu:** xây dựng bộ BG20 gồm 1.200 ảnh (1.000 ảnh polyp Kvasir-SEG theo đúng danh sách chia 880/120, 200 ảnh nền), chuyển mặt nạ sang nhãn đa giác có kiểm tra toàn vẹn.
- **Mô hình:** thiết kế và cài đặt khối C2TSVMamba (SS2D bốn hướng, nhánh hình dạng, cổng điều biến) thay C2PSA ở tầng 10, chỉ dùng PyTorch, có ba chế độ tách thành phần; phát hiện và sửa lỗi tràn số khi lưu checkpoint FP16.
- **Thực nghiệm:** 40 lượt chính (2 mô hình × 20 seed), 15 lượt tách thành phần (3 biến thể × 5 seed), PraNet và U-Net mỗi mô hình 20 seed; đủ các độ đo trong đề cương, thêm chỉ số topology; đánh giá trên bốn bộ dữ liệu ngoài với 2.725 ảnh.
- **Ứng dụng:** PolypVision gồm dịch vụ suy luận FastAPI, website Spring Boot lưu lịch sử trong MongoDB và ứng dụng di động Flutter, cho phép so sánh hai mô hình trên cùng ảnh.

## 2. Đánh giá kết quả

**CH1.** Mask mAP50–95 trung bình tăng từ 0,7189 lên 0,7232 (Δ = +0,0043), mô hình tích hợp cao hơn ở 13/20 seed, nhưng **chưa có ý nghĩa thống kê** (KTC 95% [−0,0002; 0,0088], $p = 0{,}061$). Dice theo pixel (0,854 so với 0,849) và chỉ số topology cho cùng kết luận. Độ lệch chuẩn giữa các seed nhỏ hơn khoảng 39% (Levene $p = 0{,}026$, thăm dò, chỉ đúng ở epoch tốt nhất).

**CH2.** Trên 5 seed, cả ba biến thể bỏ bớt thành phần đều có trung bình thấp hơn bản đầy đủ: bỏ cổng −0,0036, chỉ giữ SS2D −0,0068, chỉ giữ nhánh hình dạng −0,0110. Theo xu hướng, hai nhánh bổ sung cho nhau và cổng góp thêm một phần nhỏ; không chênh lệch nào có ý nghĩa thống kê.

**CH3.** Số tham số tăng 7,2%, số phép tính tăng khoảng 1,5%; độ trễ tăng khoảng 1,5 lần trên GPU và 2,1 lần trên CPU, thời gian huấn luyện khoảng gấp đôi, chủ yếu do phép quét SS2D viết bằng PyTorch thuần.

**CH4.** Cả hai checkpoint chạy được trong PolypVision trên Web và di động. Trên dữ liệu ngoài, mọi mô hình đều giảm chất lượng rõ (Dice của mô hình tích hợp 0,53–0,77); mô hình tích hợp **không tổng quát hóa tốt hơn** mô hình gốc, thấp hơn có ý nghĩa trên CVC-ClinicDB và CVC-ColonDB, chỉ báo nhầm ít hơn trên ảnh không polyp của PolypGen (10,8% so với 13,3%). Hai mô hình YOLO vẫn tốt hơn PraNet và U-Net trên dữ liệu ngoài.

**Tổng hợp:** đề tài hoàn thành các mục tiêu về quy trình; còn mục tiêu cải thiện chất lượng mặt nạ **chưa đạt ở mức có thể khẳng định**: khối C2TSVMamba chỉ cho xu hướng tăng nhỏ, chưa bù được chi phí suy luận tăng thêm và không giữ được trên dữ liệu khác nguồn. Đề tài báo cáo trung thực kết quả này thay vì chọn một lần huấn luyện có lợi.

## 3. Hạn chế

- Không có tập kiểm thử riêng; tập kiểm định nhỏ (120 ảnh polyp, 127 đối tượng); dữ liệu huấn luyện từ một nguồn, ảnh nền chưa đa dạng.
- Hai mươi seed chỉ phản ánh dao động do huấn luyện; ước tính cần khoảng 42 cặp để có lực kiểm định 80% với mức chênh lệch quan sát được. Thí nghiệm tách thành phần chỉ có 5 seed, các biến thể khác số tham số. Các phép so sánh phụ không được hiệu chỉnh.
- Chỉ thử một vị trí tích hợp (tầng 10), một cỡ mô hình (*s*), một độ phân giải (640); phần tham số mới khởi tạo ngẫu nhiên trong khi C2PSA được tiền huấn luyện trên COCO; phép quét chậm.
- PraNet và U-Net huấn luyện ở độ phân giải khác, không tăng cường dữ liệu, nên so sánh chỉ mang tính tham khảo.
- Ứng dụng chỉ xử lý ảnh tĩnh, chưa có HTTPS và giới hạn tần suất gọi API, ứng dụng di động chưa có tài khoản; không phải thiết bị y tế.

## 4. Hướng phát triển

1. **Đánh giá chặt chẽ hơn:** thêm tập kiểm thử độc lập theo bệnh nhân hoặc trung tâm, tăng số seed hoặc kiểm định chéo, mở rộng ablation lên 20 seed kèm biến thể cùng số tham số.
2. **Tổng quát hóa:** huấn luyện trên nhiều nguồn ảnh, đa dạng hóa ảnh nền, tiền huấn luyện khối VMamba trước khi ghép.
3. **Vị trí tích hợp khác:** đặt khối VMamba ở neck hoặc ở nhiều tầng, như đề cương gợi ý.
4. **Tăng tốc:** dùng kernel selective-scan CUDA, lượng tử hóa để chạy trên thiết bị biên.
5. **Độ đo biên:** Hausdorff 95, Boundary F1, clDice.
6. **Ứng dụng:** xử lý video thời gian thực, bảo mật đường truyền, đồng bộ tài khoản giữa Web và di động, thu thập phản hồi của bác sĩ.
