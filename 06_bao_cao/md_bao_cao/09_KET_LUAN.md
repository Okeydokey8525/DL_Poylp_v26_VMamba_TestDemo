# KẾT LUẬN

> **Ghi chú soạn thảo (xóa khi ghép Word):**
> - Bố cục theo Biểu mẫu V3: kết quả đạt được, đánh giá kết quả, hạn chế, hướng phát triển.
> - Mọi con số lấy lại từ Chương 6 và từ `00_tai_lieu_tong_quan/bang/*.csv`. Phần này không có số mới.
> - Phần này không trích tài liệu mới, để giữ đúng thứ tự đánh số IEEE.

## 1. Kết quả đạt được

Đề tài đã thực hiện đủ chu trình nghiên cứu đặt ra trong đề cương: khảo sát, xây dựng dữ liệu, thiết kế mô hình, thực nghiệm và xây dựng ứng dụng.

**Về lý thuyết và khảo sát:**
- Hệ thống hóa các hướng phân đoạn polyp: mạng tích chập mã hóa–giải mã, Transformer, họ YOLO và các mô hình không gian trạng thái (Mamba, VMamba).
- Chỉ ra khoảng trống: trong phạm vi khảo sát, chưa thấy công trình nào đánh giá việc đưa khối VMamba vào YOLO26-seg cho phân đoạn polyp bằng nhiều lượt huấn luyện có kiểm định thống kê.
- Trình bày các bước, ưu điểm và nhược điểm của YOLO26-seg và VMamba, kèm ví dụ tính tay cho các khái niệm và độ đo.

**Về dữ liệu:**
- Xây dựng bộ BG20 gồm 1.200 ảnh: 1.000 ảnh polyp của Kvasir-SEG theo đúng danh sách chia 880/120 của nhóm tác giả, và 200 ảnh manh tràng bình thường làm ảnh nền.
- Chuyển mặt nạ sang nhãn đa giác theo quy trình có kiểm tra toàn vẹn.
- Toàn bộ thực nghiệm dùng chung một bộ dữ liệu và một cách chia.

**Về mô hình:**
- Thiết kế và cài đặt khối C2TSVMamba thay khối C2PSA ở tầng 10 của YOLO26s-seg. Khối gồm nhánh SS2D quét bốn hướng, nhánh trích đặc trưng hình dạng và một cổng điều biến.
- Bản cài đặt chỉ dùng PyTorch, có ba chế độ tách thành phần dựng sẵn.
- Phát hiện lỗi tràn số khi lưu checkpoint ở FP16 và sửa bằng cách lưu FP32.

**Về thực nghiệm:**
- Huấn luyện 40 lượt chính: 2 mô hình × 20 seed.
- Huấn luyện 15 lượt tách thành phần: 3 biến thể × 5 seed.
- Huấn luyện PraNet và U-Net, mỗi mô hình 20 seed.
- Đánh giá đủ các độ đo trong đề cương: mask mAP50–95, mAP50, Precision, Recall, F1, Dice, IoU, số tham số, FLOPs và thời gian suy luận trên CPU và GPU. Đề tài đo thêm chỉ số topology của mặt nạ.
- Đánh giá khả năng tổng quát hóa trên bốn bộ dữ liệu ngoài với tổng cộng 2.725 ảnh.
- Mọi con số trong báo cáo đều tính lại được từ tệp kết quả gốc bằng script.

**Về ứng dụng:** xây dựng PolypVision gồm ba thành phần:
- dịch vụ suy luận FastAPI dùng chung;
- website Spring Boot lưu lịch sử trong MongoDB;
- ứng dụng di động Flutter.

Ứng dụng cho phép tải ảnh, hiển thị mặt nạ, đường biên và độ tin cậy, đồng thời so sánh mô hình gốc với mô hình tích hợp VMamba trên cùng một ảnh.

## 2. Đánh giá kết quả

Đối chiếu với bốn câu hỏi nghiên cứu nêu ở phần Mở đầu:

**CH1. Mô hình tích hợp có chính xác hơn mô hình gốc không?**
- Trên tập kiểm định của BG20, mask mAP50–95 trung bình tăng từ 0,7189 lên 0,7232 (Δ = +0,0043). Mô hình tích hợp cao hơn ở 13/20 seed.
- Chênh lệch này **chưa có ý nghĩa thống kê**: khoảng tin cậy 95% là [−0,0002; 0,0088], $p = 0{,}061$.
- Đánh giá theo pixel (Dice 0,854 so với 0,849) và theo topology cho cùng kết luận: có xu hướng tăng nhỏ, chưa đủ bằng chứng.
- Kết quả ổn định hơn giữa các seed: độ lệch chuẩn nhỏ hơn khoảng 39%, Levene $p = 0{,}026$. Đây là kết quả thăm dò và chỉ đúng ở epoch tốt nhất.

**CH2. Mỗi thành phần đóng góp bao nhiêu?** Trên 5 seed:
- Cả ba biến thể bỏ bớt một thành phần đều có trung bình thấp hơn bản đầy đủ.
- Bỏ cổng giảm ít nhất (−0,0036). Chỉ giữ nhánh SS2D giảm 0,0068. Chỉ giữ nhánh hình dạng giảm nhiều nhất (−0,0110).
- Như vậy, theo xu hướng, hai nhánh bổ sung cho nhau và cổng góp thêm một phần nhỏ.
- Với 5 seed, không chênh lệch nào có ý nghĩa thống kê. Vì vậy đây là kết quả thăm dò, chưa khẳng định được vai trò của từng thành phần.

**CH3. Chi phí tăng bao nhiêu?**
- Số tham số tăng 7,2%, số phép tính chỉ tăng khoảng 1,5%.
- Độ trễ suy luận tăng khoảng 1,5 lần trên GPU và 2,1 lần trên CPU. Thời gian huấn luyện tăng khoảng gấp đôi.
- Phần chi phí thời gian này gần như hoàn toàn do phép quét SS2D viết bằng PyTorch thuần.

**CH4. Mô hình có chạy được trong ứng dụng và trên ảnh ngoài không?**
- Cả hai checkpoint được nạp và chạy trong PolypVision trên Web và di động.
- Trên bốn bộ dữ liệu ngoài, mọi mô hình đều giảm chất lượng rõ rệt: Dice của mô hình tích hợp còn 0,53–0,77.
- Mô hình tích hợp **không tổng quát hóa tốt hơn** mô hình gốc. Nó thấp hơn có ý nghĩa thống kê trên CVC-ClinicDB và CVC-ColonDB, và không khác biệt có ý nghĩa trên ETIS-Larib và PolypGen. Điểm tích cực duy nhất là báo nhầm ít hơn trên ảnh không có polyp của PolypGen (10,8% so với 13,3%).
- Hai mô hình YOLO vẫn tốt hơn PraNet và U-Net trên dữ liệu ngoài.

**Tổng hợp.**
- **Về quy trình, đề tài đã hoàn thành các mục tiêu đề ra:** khảo sát, dữ liệu, mô hình, thực nghiệm và ứng dụng.
- **Về kết quả, mục tiêu cải thiện chất lượng mặt nạ chưa đạt được ở mức có thể khẳng định.** Với cách tích hợp và dữ liệu hiện có, khối C2TSVMamba chỉ cho xu hướng tăng nhỏ trên tập kiểm định. Mức tăng đó chưa đủ bù cho chi phí suy luận tăng thêm, và không giữ được trên dữ liệu khác nguồn.
- Đề tài báo cáo trung thực kết quả này, thay vì chọn một lần huấn luyện có lợi. Đây là một kết quả có giá trị cho các nghiên cứu tiếp theo theo hướng tích hợp Mamba vào mô hình phát hiện thời gian thực.

## 3. Hạn chế

**Về dữ liệu và thiết kế thực nghiệm:**
- Không có tập kiểm thử riêng. Tập kiểm định vừa dùng để chọn epoch vừa dùng để báo cáo, nên số tuyệt đối có thể lạc quan.
- Tập kiểm định nhỏ (120 ảnh polyp, 127 đối tượng).
- Mô hình chỉ học từ một nguồn ảnh. Ảnh nền chỉ lấy từ một lớp manh tràng bình thường nên chưa đa dạng, thể hiện qua tỉ lệ báo nhầm cao trên PolypGen.
- Hai mươi seed chỉ phản ánh dao động do huấn luyện, không phản ánh dao động do dữ liệu. Ước tính cần khoảng 42 cặp để có lực kiểm định 80% với mức chênh lệch quan sát được.
- Thí nghiệm tách thành phần chỉ có 5 seed. Các biến thể có số tham số khác nhau, nên chưa tách được phần do cấu trúc với phần do thêm tham số.
- Nhiều phép so sánh phụ không được hiệu chỉnh, nên các kết quả có $p < 0{,}05$ ngoài chỉ số chính chỉ là gợi ý.

**Về mô hình:**
- Chỉ thử một vị trí tích hợp (tầng 10), một cỡ mô hình (*s*) và một độ phân giải đầu vào (640).
- Phần tham số mới của khối tích hợp được khởi tạo ngẫu nhiên, trong khi khối C2PSA bị thay thế đã được tiền huấn luyện trên COCO.
- Phép quét viết bằng PyTorch thuần nên chậm.

**Về so sánh:** PraNet và U-Net được huấn luyện ở độ phân giải khác và không tăng cường dữ liệu, nên so sánh với hai mô hình này chỉ mang tính tham khảo.

**Về ứng dụng:**
- Chỉ xử lý ảnh tĩnh, chưa xử lý video.
- Chưa có HTTPS và giới hạn tần suất gọi API.
- Ứng dụng di động chưa có tài khoản và lịch sử.
- Ứng dụng không phải thiết bị y tế.

## 4. Hướng phát triển

1. **Đánh giá chặt chẽ hơn:**
   - Thêm tập kiểm thử độc lập, tốt nhất là tách theo bệnh nhân hoặc theo trung tâm.
   - Tăng số seed hoặc dùng kiểm định chéo.
   - Mở rộng thí nghiệm tách thành phần lên 20 seed, kèm biến thể có số tham số tương đương để tách ảnh hưởng của dung lượng mô hình.
2. **Cải thiện khả năng tổng quát hóa:**
   - Huấn luyện trên nhiều nguồn ảnh (Kvasir-SEG, CVC-ClinicDB, PolypGen…).
   - Đa dạng hóa ảnh nền.
   - Thử tiền huấn luyện khối VMamba trên tập ảnh lớn trước khi ghép vào YOLO26-seg.
3. **Thử các vị trí và cách tích hợp khác:** đặt khối VMamba ở vùng kết hợp đặc trưng đa tỉ lệ (neck) hoặc ở nhiều tầng. Đây cũng là hướng mà đề cương gợi ý.
4. **Tăng tốc:** dùng kernel selective-scan viết bằng CUDA, đo lại FLOPs có tính cả phép quét, thử lượng tử hóa để đưa mô hình lên thiết bị biên.
5. **Bổ sung độ đo về hình dạng và biên** (Hausdorff 95, Boundary F1, clDice) để kiểm chứng trực tiếp mục tiêu "mặt nạ bám sát đường biên".
6. **Hoàn thiện ứng dụng:**
   - Xử lý video nội soi theo thời gian thực.
   - Bảo mật đường truyền và giới hạn tần suất gọi API.
   - Đồng bộ tài khoản và lịch sử giữa Web và di động.
   - Thu thập phản hồi của bác sĩ để đánh giá giá trị lâm sàng.
