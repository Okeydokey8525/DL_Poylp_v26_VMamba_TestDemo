# MỞ ĐẦU

> **Ghi chú soạn thảo (xóa khi nộp):**
> - Bản rút gọn (thân khoảng 70 trang), nén từ bản đầy đủ `md_bao_cao/01_MO_DAU.md` (tag git `ban_day_du_147`). Số liệu giữ nguyên.
> - Chỗ ghi **[ĐIỀN]** là ô nhóm tự điền. Bảng phân công theo hạng mục đã chuyển xuống Phụ lục E.

## 1. Lý do chọn đề tài

Ung thư đại trực tràng là một trong những bệnh ung thư phổ biến và gây tử vong nhiều nhất. Theo ước tính GLOBOCAN năm 2022, bệnh này chiếm 9,6% số ca ung thư mới, đứng thứ ba, và 9,3% số ca tử vong do ung thư, đứng thứ hai [1]. Phần lớn các ca bệnh phát triển từ polyp ở niêm mạc ruột, nên phát hiện và cắt bỏ polyp sớm qua nội soi là cách phòng bệnh quan trọng [2]. Tuy vậy, polyp vẫn bị bỏ sót với tỉ lệ đáng kể [3], trong khi phát hiện được nhiều u tuyến hơn gắn với nguy cơ ung thư thấp hơn [4]. Một công cụ tự động khoanh vùng polyp trên ảnh vì thế có giá trị hỗ trợ thực tế.

Bài toán đặt ra là **phân đoạn polyp**: xác định những điểm ảnh thuộc polyp, chứ không chỉ đánh dấu một hộp bao quanh. Bài toán khó vì polyp có màu và kết cấu gần giống niêm mạc, đường biên mờ, ảnh có phản quang, nếp gấp, bọt che khuất, và kích thước polyp thay đổi lớn. Các bộ dữ liệu công khai như Kvasir-SEG [5] cho phép nghiên cứu bài toán này theo một quy trình có thể kiểm tra lại.

YOLO26-seg [6] (công bố năm 2026, bản tiền ấn phẩm) phát hiện và phân đoạn từng đối tượng trong một lần suy luận, không cần bước lọc trùng NMS. Ngữ cảnh toàn cục của mô hình chủ yếu đến từ khối chú ý đặt ở mức đặc trưng sâu nhất; các khối còn lại phần lớn là tích chập, chỉ nhìn vùng lân cận nhỏ. VMamba [7] là một cách khác để lấy ngữ cảnh toàn cục: mô-đun SS2D quét bản đồ đặc trưng theo bốn hướng. Đề tài kết hợp cơ chế quét này với một nhánh trích đặc trưng hình dạng và đường biên, vốn là manh mối quan trọng với polyp. Việc thay thế không nhằm làm mô hình nhẹ hơn: khối mới làm tăng số tham số và thời gian suy luận, và mức tăng đó là một câu hỏi cần đo.

Từ đó, đề tài đặt câu hỏi: **thay khối chú ý ở tầng sâu của YOLO26-seg bằng một khối VMamba có thêm nhánh nhận biết hình dạng thì chất lượng phân đoạn polyp thay đổi thế nào, và phải trả thêm bao nhiêu chi phí tính toán?** Để kết luận không dựa vào một lần huấn luyện may mắn, mỗi mô hình được huấn luyện lặp lại với 20 seed (seed 0–19), rồi so sánh ghép cặp có kiểm định thống kê.

## 2. Mục tiêu nghiên cứu

**Mục tiêu tổng quát:** nghiên cứu và đánh giá phương pháp tích hợp khối VMamba vào YOLO26-seg cho bài toán phân đoạn polyp trên ảnh nội soi đại trực tràng, đồng thời xây dựng ứng dụng minh họa.

**Mục tiêu cụ thể** (theo đề cương đã duyệt):
1. Khảo sát cơ sở lý thuyết và các công trình liên quan đến phân đoạn polyp, YOLO26-seg, Mamba và VMamba.
2. Xây dựng và tiền xử lý bộ dữ liệu ảnh nội soi có mặt nạ phân đoạn từ các bộ dữ liệu công khai, dùng một cách chia dữ liệu thống nhất cho mọi thực nghiệm.
3. Đề xuất và cài đặt khối C2TSVMamba thay khối C2PSA ở tầng 10 của YOLO26-seg.
4. So sánh mô hình đề xuất với YOLO26-seg nguyên bản về chất lượng phân đoạn và chi phí tính toán; xây dựng ứng dụng minh họa.

**Câu hỏi nghiên cứu:**
- **CH1.** Trên cùng dữ liệu và cấu hình huấn luyện, mô hình tích hợp có mask mAP50–95 trung bình cao hơn mô hình gốc không, và chênh lệch có ý nghĩa thống kê không? Dao động giữa các seed (khoảng 0,01) lớn hơn mức chênh lệch có thể kỳ vọng (vài phần nghìn), nên khả năng phát hiện một chênh lệch nhỏ vẫn hạn chế dù có 20 seed.
- **CH2.** Mỗi thành phần của khối đề xuất (nhánh SS2D, nhánh hình dạng, cổng điều khiển) đóng góp bao nhiêu? Câu hỏi này được trả lời bằng thí nghiệm tách thành phần (ablation).
- **CH3.** Khối đề xuất làm tăng số tham số, chi phí tính toán và thời gian suy luận bao nhiêu?
- **CH4.** Mô hình đã huấn luyện có chạy đúng trong một ứng dụng thực tế (Web, Mobile) không, và hoạt động ra sao trên ảnh ngoài tập huấn luyện?

## 3. Đối tượng và phạm vi nghiên cứu

**Đối tượng nghiên cứu:** ảnh nội soi đại trực tràng dạng ảnh tĩnh; mô hình YOLO26s-seg (cỡ *small*) và mô hình YOLO26s-seg tích hợp khối C2TSVMamba; mô-đun quét chọn lọc hai chiều SS2D của VMamba.

**Phạm vi:**
- **Dữ liệu:** bộ BG20 gồm 1.200 ảnh, là 1.000 ảnh polyp của Kvasir-SEG [5] và 200 ảnh manh tràng bình thường của Kvasir v2 [8] làm ảnh nền; chia 1.040 ảnh huấn luyện và 160 ảnh kiểm định, phần polyp dùng đúng danh sách chia 880/120 của nhóm tác giả bộ dữ liệu. Không có tập kiểm tra riêng: chỉ số được đo và epoch tốt nhất được chọn trên tập kiểm định, nên số tuyệt đối có thể lạc quan hơn thực tế, nhưng hạn chế này như nhau cho cả hai mô hình.
- **Dữ liệu thực tế:** bốn bộ dữ liệu công khai khác nguồn (CVC-ClinicDB 612 ảnh, CVC-ColonDB 380 ảnh, ETIS-Larib 196 ảnh, phần ảnh đơn của PolypGen 1.537 ảnh từ 6 trung tâm), dùng nguyên checkpoint, không huấn luyện lại. Đây không phải dữ liệu thu tại bệnh viện.
- **Mô hình và thực nghiệm:** một lớp đối tượng (polyp); hai mô hình chỉ khác nhau ở tầng 10, mọi siêu tham số khác giống nhau; 100 epoch, ảnh vào 640×640, 20 seed. PraNet [9] và U-Net [10] được huấn luyện trên cùng dữ liệu để đối chiếu chỉ số theo điểm ảnh.
- **Ứng dụng:** PolypVision gồm dịch vụ suy luận (FastAPI), website (Spring Boot) và ứng dụng di động (Flutter), xử lý ảnh tĩnh, chưa xử lý video trực tiếp. Ứng dụng phục vụ nghiên cứu, **không phải thiết bị y tế**.

## 4. Phương pháp nghiên cứu

- **Nghiên cứu lý thuyết:** tổng hợp tài liệu về phân đoạn polyp, họ YOLO, cơ chế chú ý, mô hình không gian trạng thái, Mamba và VMamba (Chương 1, Chương 2).
- **Thực nghiệm có đối chứng:** mô hình gốc là nhóm đối chứng, mô hình tích hợp là nhóm thử nghiệm; hai mô hình dùng chung dữ liệu, tiền xử lý, siêu tham số và danh sách seed, nên khác biệt có hệ thống chỉ đến từ tầng 10. Kết quả ghép cặp theo seed, kiểm định bằng t ghép cặp và Wilcoxon, kèm khoảng tin cậy 95% và cỡ hiệu ứng. Thí nghiệm tách thành phần tắt lần lượt từng nhánh để đo đóng góp.
- **Độ đo** (mục 2.7): mask mAP50–95 (độ đo chính), mask mAP50, Precision, Recall, F1; Dice, IoU theo điểm ảnh; số tham số, FLOPs, thời gian suy luận trên CPU và GPU.
- **Nghiên cứu ứng dụng:** xây dựng PolypVision, tích hợp hai checkpoint, cho phép tải ảnh, xem mặt nạ, độ tin cậy và so sánh hai mô hình trên cùng ảnh.

## 5. Đóng góp của đề tài

- **Về mô hình:** thiết kế và cài đặt khối C2TSVMamba thay khối C2PSA ở tầng 10 của YOLO26s-seg, kết hợp nhánh SS2D quét bốn hướng với nhánh đặc trưng hình dạng đa tỉ lệ có hướng qua một cổng điều khiển. Bản cài đặt chỉ dùng PyTorch, không cần biên dịch kernel CUDA riêng.
- **Về kỹ thuật:** phát hiện lỗi tràn số khi lưu checkpoint FP16 (một thống kê của lớp chuẩn hóa lô trong khối mới vượt giới hạn FP16) và chuyển sang lưu FP32.
- **Về đánh giá:** so sánh trên 20 seed ghép cặp có kiểm định, khoảng tin cậy và cỡ hiệu ứng; thí nghiệm tách thành phần; đánh giá trên bốn bộ dữ liệu ngoài; mọi con số truy được về tệp kết quả gốc và script tính lại.
- **Về ứng dụng:** PolypVision có dịch vụ suy luận dùng chung cho Web và Mobile, so sánh được hai mô hình trên cùng ảnh.

Đề tài không khẳng định mô hình đề xuất tốt hơn mô hình gốc khi chưa có bằng chứng thống kê; kết quả và mức độ tin cậy được trình bày ở Chương 6.

## 6. Kế hoạch thực hiện và phân công công việc

Đề tài thực hiện trong 12 tuần, từ 17/08/2026 đến 08/11/2026, nội dung từng tuần theo đề cương đã duyệt.

*Bảng 0.1. Kế hoạch thực hiện theo tuần*

| Tuần | Thời gian | Nội dung công việc | Người phụ trách | Sản phẩm | Trạng thái |
|---|---|---|---|---|---|
| 1 | 17/08 – 23/08 | Xác định lý do chọn đề tài, khảo sát các công trình liên quan. Lập kế hoạch và phân công | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| 2 | 24/08 – 30/08 | Thu thập, phân tích bộ dữ liệu ảnh polyp đại tràng (Kaggle và nguồn công khai) | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| 3 | 31/08 – 06/09 | Làm sạch, chuyển nhãn, tiền xử lý dữ liệu cho 1.000 ảnh polyp và ảnh nền | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| 4 | 07/09 – 13/09 | Mô tả bài toán, thiết lập môi trường huấn luyện, chọn ngôn ngữ và framework | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| 5 | 14/09 – 20/09 | Cài đặt và huấn luyện mô hình gốc YOLO26-seg | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| 6 | 21/09 – 27/09 | Cài đặt và huấn luyện các mô hình so sánh | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| 7 | 28/09 – 04/10 | Cài đặt thành phần cải tiến: tích hợp VMamba vào YOLO26-seg | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| 8 | 05/10 – 11/10 | Thực nghiệm và đánh giá bằng Dice, IoU, Precision, Recall, F1, mAP50, mAP50–95, tốc độ suy luận, số tham số, chi phí tính toán | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| 9 | 12/10 – 18/10 | Đánh giá trên dữ liệu thực tế. So sánh và chọn mô hình | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| 10 | 19/10 – 25/10 | Xây dựng backend, tổ chức lưu trữ kết quả dự đoán | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| 11 | 26/10 – 01/11 | Cài đặt chức năng, thiết kế giao diện Web/App: tải ảnh, hiển thị mặt nạ polyp và độ tin cậy | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| 12 | 02/11 – 08/11 | Hoàn chỉnh báo cáo, thiết kế slide, nộp báo cáo | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |

> **Gợi ý điền:** cột "Sản phẩm" ghi thứ kiểm tra được (ví dụ "bộ dữ liệu BG20 ở định dạng YOLO", "API `/predict`"); cột "Trạng thái" ghi "Hoàn thành", "Hoàn thành trễ (lý do)" hoặc "Điều chỉnh (lý do)".

*Bảng 0.2. Phân công nhiệm vụ trong nhóm*

| Thành viên | MSSV | Lớp | Vai trò | Nhiệm vụ chính | Chương phụ trách viết | Mức đóng góp (%) |
|---|---|---|---|---|---|---|
| Lê Đức Lương | 2001230490 | 14DHTH09 | [ĐIỀN, ví dụ: Nhóm trưởng] | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Phùng Tuấn Huy | 2001230312 | 14DHTH13 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Trần Mạnh Toàn | 2001230830 | 14DHTH09 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |

Phân công chi tiết theo hạng mục công việc ở Phụ lục E. Nhóm gặp giảng viên hướng dẫn ít nhất một lần mỗi tuần; mã nguồn, cấu hình và kết quả huấn luyện được quản lý bằng Git **[ĐIỀN: tên kho/nền tảng nếu muốn nêu]**; các lượt huấn luyện được chia cho nhiều tài khoản Kaggle để chạy song song. [ĐIỀN: công cụ trao đổi trong nhóm, tần suất họp nhóm.]

## 7. Bố cục báo cáo

Ngoài Mở đầu và Kết luận, báo cáo gồm sáu chương: Chương 1 tổng quan bài toán, dữ liệu công khai và các hướng nghiên cứu; Chương 2 cơ sở lý thuyết về YOLO26-seg, Mamba, VMamba, các độ đo và kiểm định thống kê; Chương 3 mô hình đề xuất C2TSVMamba; Chương 4 dữ liệu và tiền xử lý; Chương 5 cài đặt và ứng dụng PolypVision; Chương 6 thực nghiệm và đánh giá. Phụ lục gồm kết quả từng seed, cấu hình huấn luyện, tổ chức mã nguồn, hướng dẫn chạy lại và các chi tiết được chuyển khỏi phần thân.
