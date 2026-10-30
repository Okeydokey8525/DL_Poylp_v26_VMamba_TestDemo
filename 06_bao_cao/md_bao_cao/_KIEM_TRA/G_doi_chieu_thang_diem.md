# G. Đối chiếu báo cáo với đề cương và thang điểm

Ngày đối chiếu: 29/10/2026. Nguồn tiêu chí là đề cương chính thức `06_bao_cao/CNTT_KLCN182-Phung The Bao.pdf`, gồm mục 5 (mục tiêu), mục 6 (yêu cầu) và mục 9 (thang điểm). Báo cáo được đối chiếu ở dạng markdown trong `06_bao_cao/md_bao_cao/`.

Ký hiệu trạng thái:
- ✅: đã có đủ.
- ⚠️: có nhưng cần nhóm bổ sung hoặc lưu ý.
- ⏳: làm ở giai đoạn sau (ghép Word, slide, bảo vệ).

## 1. Thang điểm (mục 9 đề cương)

### Tiêu chí 1–4: tổng quan, kế hoạch, lý thuyết, thuật toán

| STT | Tiêu chí | Điểm | Vị trí trong báo cáo | Trạng thái |
|---|---|---:|---|---|
| 1 | Lý do chọn đề tài, mục tiêu nghiên cứu | 0,25 | Mở đầu §1, §2 | ✅ |
| 1 | Khảo sát các công trình liên quan | 0,75 | Ch.1: §1.3 bộ dữ liệu, §1.4 sáu hướng nghiên cứu (CNN mã hóa–giải mã, Transformer, YOLO, SSM/Mamba, Mamba cho polyp, Mamba trong YOLO), §1.5 bảng tổng hợp và khoảng trống, §1.6 trong nước | ✅ |
| 1 | Đối tượng, phương pháp, độ đo (Dice, IoU, P, R, F1, mAP50, mAP50–95, tốc độ suy luận, số tham số, chi phí tính toán) | 0,25 | Mở đầu §3, §4; định nghĩa và ví dụ tính tay ở Ch.2 §2.7; kết quả đo ở Ch.6 §6.2, §6.3, §6.5 | ✅ F1 có ở cả hai mức: theo pixel (Dice = F1, §2.7.2) và theo đối tượng (mask F1, §6.2) |
| 2 | Lập kế hoạch và phân công | 0,25 | Mở đầu §6: Bảng 0.1 kế hoạch 12 tuần, Bảng 0.2 và 0.3 phân công, §6.3 cách phối hợp | ⚠️ Khung đã đủ, nhưng các ô **[ĐIỀN]** do nhóm điền sau khi ghép Word |
| 3 | Khái niệm: phân loại, phát hiện, phân đoạn ảnh | 0,5 | Ch.2 §2.1, Bảng và Hình 2.1 (bốn kiểu đầu ra trên cùng một ảnh nội soi) | ✅ |
| 3 | Mô hình YOLO; YOLO26-seg và VMamba | (trong 0,5) | Ch.2 §2.3 họ YOLO, §2.4 YOLO26-seg, §2.6 SSM, Mamba, VMamba | ✅ |
| 3 | Ví dụ minh họa | 0,25 | Ch.2 có ví dụ cho tích chập, gán nhãn, giải mã hộp, rời rạc hóa SSM, thứ tự quét SS2D, IoU/Dice, AP, kiểm định; Ch.3 §3.3.6 truy vết tensor, §3.4.3 ví dụ phép quét | ✅ |
| 4 | Các bước thuật toán YOLO26-seg, VMamba | 0,25 | Ch.2 §2.4.2 các bước YOLO26-seg; §2.6.3–2.6.4 Mamba và SS2D; Ch.3 §3.4 thuật toán quét song song, §3.7 quy trình suy luận và huấn luyện | ✅ |
| 4 | Ưu, nhược điểm YOLO26-seg, VMamba | 0,25 | Ch.2 §2.4.3, §2.6.5; Ch.3 §3.9 (mô hình đề xuất) | ✅ |
| 4 | Mô tả bộ dữ liệu thực nghiệm | 0,5 | Ch.4 (nguồn, BG20, chuyển nhãn, đổi kích thước, tăng cường, kiểm tra toàn vẹn); Ch.1 §1.3 | ✅ Đã sửa nguồn của cách chia 880/120 và ô cuối Hình 4.5 |

### Tiêu chí 5–10: cài đặt, ứng dụng, báo cáo, bảo vệ

| STT | Tiêu chí | Điểm | Vị trí trong báo cáo | Trạng thái |
|---|---|---:|---|---|
| 5 | Mô tả cấu hình hệ thống | 0,25 | Ch.5 §5.1.1–5.1.2, Bảng 5.1–5.2 | ✅ |
| 5 | Lựa chọn môi trường thử nghiệm | 0,25 | Ch.5 §5.1.1 (Kaggle GPU), §5.1.2 (máy đo hiệu năng) | ✅ |
| 5 | Lựa chọn ngôn ngữ lập trình | 0,25 | Ch.5 §5.1.3, Bảng 5.3 | ✅ Đã thêm câu giải thích vì sao chỉ dùng PyTorch (đề cương nêu cả TensorFlow) |
| 5 | Cài đặt thuật toán cơ sở YOLO26-seg | 0,5 | Ch.5 §5.2 | ✅ |
| 5 | Cài đặt thành phần cải tiến: tích hợp VMamba vào backbone hoặc vùng kết hợp đặc trưng đa tỉ lệ | 0,5 | Ch.3 (thiết kế); Ch.5 §5.3 (cài đặt). Khối đặt ở tầng 10, cuối backbone (§3.1.2) | ✅ |
| 5 | Đánh giá thực nghiệm Dice, IoU, P, R, F1, mAP50, mAP50–95, tốc độ suy luận, số tham số | 0,5 | Ch.6 §6.2 (mAP, P, R, F1, 20 seed); §6.3 (Dice, IoU, P, R theo pixel, có PraNet và U-Net); §6.4 (topology); §6.5 (tham số, GFLOPs, độ trễ CPU và GPU); §6.6 (ablation) | ✅ |
| 5 | Cài đặt giao diện | 0,5 | Ch.5 §5.8.1 Website, §5.8.2 di động | ⚠️ Chờ nhóm chụp màn hình (`[CHÈN HÌNH]`) |
| 5 | Tổ chức cấu trúc lưu trữ kết quả | 0,25 | Ch.5 §5.4.2 (kết quả huấn luyện), §5.7 (kết quả phân tích của ứng dụng, MongoDB) | ✅ |
| 5 | Chức năng nhận diện và phân đoạn polyp | 0,5 | Ch.5 §5.5.1, §5.6 (API), §5.8 (mặt nạ, đường biên vàng, độ tin cậy) | ✅ |
| 5 | Chức năng so sánh YOLO26-seg nguyên bản và mô hình tích hợp VMamba | 0,5 | Ch.5 §5.5.1, §5.6.2 (API so sánh), §5.8 (trang so sánh trên Web và di động) | ⚠️ Chờ ảnh chụp |
| 5 | Triển khai trên dữ liệu thực tế (CLO4) | 0,75 | Ch.5 §5.9; Ch.6 §6.7 (4 bộ ngoài, 20 seed, 4 mô hình, theo từng trung tâm PolypGen, tỉ lệ báo nhầm) | ✅ Ghi rõ đây là dữ liệu công khai khác nguồn, không phải dữ liệu bệnh viện. Ảnh chụp ứng dụng chạy trên ảnh ngoài chờ nhóm chụp |
| 6 | Nội dung kiến thức trong báo cáo | 0,5 | Toàn bộ | ✅ Kết luận và Phụ lục viết ở giai đoạn B |
| 7 | Hình thức, định dạng báo cáo | 0,5 | Theo Biểu mẫu V3 | ⏳ Giai đoạn C (ghép Word) |
| 8 | Thái độ, tác phong | 0,5 | Không thuộc báo cáo | – |
| 9 | Phong cách báo cáo, slide | 0,5 | Slide nhóm tự thiết kế | ⏳ |
| 10 | Điểm khuyến khích NCKH | tối đa 1,0 | Không thuộc phạm vi hiện tại | – |

## 2. Mục tiêu và yêu cầu (mục 5, 6 đề cương)

| Yêu cầu | Đáp ứng | Ghi chú |
|---|---|---|
| Khảo sát lý thuyết, công trình về phân đoạn polyp, YOLO26-seg, Mamba, VMamba | Ch.1, Ch.2 | ✅ |
| Xây dựng, tiền xử lý dữ liệu; cách chia thống nhất | Ch.4; mọi lượt huấn luyện dùng cùng BG20 và cùng danh sách chia | ✅ |
| "Đề xuất và cài đặt **các phương án** tích hợp VMamba vào backbone hoặc vùng kết hợp đặc trưng" | Một phương án chính (C2TSVMamba ở tầng 10) và ba biến thể tách thành phần (§6.6) | ⚠️ Nhóm từng thử thêm các phương án kết hợp khác (AV, AVF, ITSVM), nhưng theo quyết định của nhóm không đưa vào báo cáo. Nếu hội đồng hỏi "đã thử phương án nào khác", có thể trả lời miệng. Có thể cân nhắc thêm một câu ở Ch.3 §3.1.3 rằng nhóm đã thử sơ bộ các cách ghép khác và chọn tầng 10 vì lý do §3.1.2, không nêu số liệu |
| So sánh với YOLO26-seg nguyên bản về chất lượng và chi phí | Ch.6 §6.2–6.5 | ✅ |
| Xây dựng ứng dụng web minh họa | Ch.5 (Web Spring Boot, di động Flutter, FastAPI) | ✅ |
| Yêu cầu "mặt nạ bám sát, đường biên sắc nét" | Đo bằng mAP50–95 (nhạy với độ khớp biên), Dice/IoU, topology | ✅ Kết quả chỉ là xu hướng; không viết là đã cải thiện đường biên |
| "Thực hiện ablation study để **khẳng định tính đúng đắn** của giải pháp" | §6.6, 5 seed × 3 biến thể | ⚠️ Kết quả cho thấy xu hướng bản đầy đủ tốt nhất, nhưng **không khẳng định được** bằng thống kê. Báo cáo viết đúng mức "xu hướng, thăm dò"; không đổi văn phong để khớp chữ "khẳng định" của đề cương |
| Môi trường: Python cho mô hình và API, Java cho Web; PyTorch, TensorFlow, Ultralytics; Kaggle GPU | Ch.5 §5.1 | ✅ TensorFlow không dùng, đã giải thích |
| Kế hoạch 12 tuần theo mục 10 đề cương | Mở đầu Bảng 0.1 lấy đúng nội dung 12 tuần | ⚠️ Nhóm điền cột phụ trách, sản phẩm, trạng thái |

## 3. Việc còn lại rút ra từ đối chiếu

1. **Nhóm:** điền các ô [ĐIỀN] ở Mở đầu §6 sau khi ghép Word.
2. **Nhóm:** chụp màn hình ứng dụng cho Ch.5, gồm cả ảnh ứng dụng chạy trên ảnh của bộ dữ liệu ngoài.
3. **Giai đoạn B:**
   - viết Kết luận (trả lời mục tiêu và câu hỏi nghiên cứu, hạn chế, hướng phát triển);
   - viết Phụ lục;
   - viết Lời cảm ơn và danh mục chữ viết tắt;
   - bổ sung ý ablation vào phần Đóng góp của Mở đầu.
4. **Giai đoạn C:** định dạng theo Biểu mẫu V3 (tiêu chí 7).
5. **Cần nhóm quyết định:** có thêm câu về các phương án ghép đã thử sơ bộ (AV, AVF, ITSVM) vào Ch.3 §3.1.3 hay không. Mặc định là không thêm, giữ đúng quyết định trước đây.
