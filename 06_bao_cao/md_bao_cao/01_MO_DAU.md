# MỞ ĐẦU

> **Ghi chú soạn thảo (xóa khi nộp):**
> - Thông tin đề tài, nhóm, GVHD và mục tiêu lấy theo đề cương đã duyệt (`CNTT_KLCN182-Phung The Bao.pdf`) và bản báo cáo cũ `CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong_MoRong_FP32.docx`. Lời văn được viết lại để tránh trùng lặp khi kiểm tra Turnitin.
> - Chỗ ghi **[ĐIỀN]** là ô nhóm tự điền.
> - Số tài liệu tham khảo đã đánh lại theo thứ tự trích dẫn lần đầu (IEEE) ngày 28/10/2026; danh mục ở `08_TAI_LIEU_THAM_KHAO.md`, bảng số cũ → mới ở `_KIEM_TRA/F_bang_doi_so_tai_lieu.csv`.

## 1. Lý do chọn đề tài

Ung thư đại trực tràng là một trong những bệnh ung thư phổ biến và gây tử vong nhiều nhất. Theo ước tính GLOBOCAN năm 2022, bệnh này chiếm 9,6% số ca ung thư mới, đứng thứ ba, và 9,3% số ca tử vong do ung thư, đứng thứ hai [1]. Phần lớn các ca bệnh phát triển từ polyp ở niêm mạc ruột, nên phát hiện và cắt bỏ polyp sớm qua nội soi là cách phòng bệnh quan trọng [2].

Tuy vậy, kết quả nội soi phụ thuộc nhiều vào người thực hiện, và polyp vẫn bị bỏ sót với tỉ lệ đáng kể [3]. Phát hiện được nhiều u tuyến hơn gắn với nguy cơ ung thư thấp hơn [4]. Chương 1 trình bày chi tiết các số liệu này. Chúng cho thấy một công cụ tự động khoanh vùng polyp trên ảnh có giá trị hỗ trợ thực tế.

Bài toán đặt ra là **phân đoạn polyp**: xác định chính xác những điểm ảnh thuộc polyp, chứ không chỉ đánh dấu một hộp bao quanh. Đây là bài toán khó vì:
- màu và kết cấu của polyp thường gần giống niêm mạc xung quanh, đường biên mờ;
- ảnh có vùng phản quang, nếp gấp, bọt hoặc dịch che khuất;
- kích thước polyp thay đổi lớn, từ rất nhỏ đến chiếm gần hết khung hình.

Các bộ dữ liệu công khai như Kvasir-SEG [5] cho phép nghiên cứu bài toán này theo một quy trình có thể kiểm tra lại.

Về phương pháp, YOLO26-seg [6] (công bố năm 2026, bản tiền ấn phẩm) phát hiện và phân đoạn từng đối tượng trong một lần suy luận, không cần bước lọc trùng NMS, nên phù hợp với yêu cầu xử lý nhanh. Ngữ cảnh toàn cục của mô hình chủ yếu đến từ các khối chú ý (attention) đặt ở mức đặc trưng sâu nhất; phần lớn các khối còn lại là tích chập, chỉ nhìn vùng lân cận nhỏ. Mô hình không gian trạng thái thị giác VMamba [7] là một cách khác để lấy ngữ cảnh toàn cục: mô-đun SS2D quét bản đồ đặc trưng theo bốn hướng, nhờ đó mỗi vị trí nhận thông tin từ cả bốn phía. Đề tài kết hợp cơ chế quét này với một nhánh trích đặc trưng hình dạng và đường biên, vốn là manh mối quan trọng với polyp. Việc thay thế không nhằm làm mô hình nhẹ hơn: ở tầng 10, bản đồ đặc trưng chỉ có 20×20 vị trí, và khối mới thực tế làm tăng số tham số cũng như thời gian suy luận. Chi phí tăng thêm là một câu hỏi cần đo (CH3).

Từ đó, đề tài đặt câu hỏi: **thay khối chú ý ở tầng sâu của YOLO26-seg bằng một khối VMamba có thêm nhánh nhận biết hình dạng thì chất lượng phân đoạn polyp thay đổi thế nào, và phải trả thêm bao nhiêu chi phí tính toán?** Để trả lời một cách tin cậy, đề tài không dựa vào một lần huấn luyện may mắn. Mỗi mô hình được huấn luyện lặp lại với 20 seed khác nhau (seed 0–19), rồi so sánh ghép cặp có kiểm định thống kê.

## 2. Mục tiêu nghiên cứu

**Mục tiêu tổng quát:** nghiên cứu và đánh giá phương pháp tích hợp khối VMamba vào YOLO26-seg cho bài toán phân đoạn polyp trên ảnh nội soi đại trực tràng, đồng thời xây dựng ứng dụng minh họa.

**Mục tiêu cụ thể** (theo đề cương đã duyệt):
1. Khảo sát cơ sở lý thuyết và các công trình liên quan đến phân đoạn polyp, YOLO26-seg, Mamba và VMamba.
2. Xây dựng và tiền xử lý bộ dữ liệu ảnh nội soi có mặt nạ phân đoạn từ các bộ dữ liệu công khai, dùng một cách chia dữ liệu thống nhất cho mọi thực nghiệm.
3. Đề xuất và cài đặt phương án tích hợp khối VMamba vào backbone của YOLO26-seg. Phương án được chọn là khối C2TSVMamba thay khối C2PSA ở tầng 10.
4. So sánh mô hình đề xuất với YOLO26-seg nguyên bản về chất lượng phân đoạn và chi phí tính toán; xây dựng ứng dụng minh họa kết quả.

**Câu hỏi nghiên cứu:**
- **CH1.** Trên cùng dữ liệu và cùng cấu hình huấn luyện, mô hình tích hợp có mask mAP50–95 trung bình cao hơn mô hình gốc không, và chênh lệch đó có ý nghĩa thống kê không? Cần lưu ý trước: dao động giữa các seed (khoảng 0,01) lớn hơn mức chênh lệch có thể kỳ vọng (vài phần nghìn), nên ngay cả với 20 seed, khả năng phát hiện một chênh lệch nhỏ vẫn còn hạn chế.
- **CH2.** Mỗi thành phần của khối đề xuất (nhánh SS2D, nhánh hình dạng, cổng điều khiển) đóng góp bao nhiêu? Câu hỏi này được trả lời bằng thí nghiệm tách thành phần (ablation).
- **CH3.** Khối đề xuất làm tăng số tham số, chi phí tính toán và thời gian suy luận bao nhiêu?
- **CH4.** Mô hình đã huấn luyện có nạp và chạy đúng trong một ứng dụng thực tế (Web, Mobile) không, và hoạt động ra sao trên ảnh ngoài tập huấn luyện?

## 3. Đối tượng và phạm vi nghiên cứu

**Đối tượng nghiên cứu:**
- Ảnh nội soi đại trực tràng dạng ảnh tĩnh, có hoặc không có polyp.
- Mô hình YOLO26s-seg (cỡ *small*) và mô hình YOLO26s-seg tích hợp khối C2TSVMamba.
- Khối VMamba, cụ thể là mô-đun quét chọn lọc hai chiều SS2D.

**Phạm vi dữ liệu:**
- Bộ dữ liệu thực nghiệm BG20 gồm 1.200 ảnh: 1.000 ảnh polyp của Kvasir-SEG [5] và 200 ảnh manh tràng bình thường (lớp *normal-cecum*) của Kvasir v2 [8] làm ảnh nền (không có polyp).
- Dữ liệu chia thành 1.040 ảnh huấn luyện và 160 ảnh kiểm định. Phần ảnh polyp dùng đúng danh sách chia 880/120 do nhóm tác giả bộ dữ liệu cung cấp.
- Bộ dữ liệu không có tập kiểm tra (test) riêng. Mọi chỉ số định lượng chính được đo trên tập kiểm định, và epoch tốt nhất cũng được chọn trên chính tập này. Vì vậy số liệu tuyệt đối có thể lạc quan hơn thực tế. Hạn chế này áp dụng như nhau cho cả hai mô hình, nên không làm lệch phép so sánh giữa chúng.
- Phần triển khai trên dữ liệu thực tế dùng thêm ảnh từ các bộ CVC-ClinicDB, CVC-ColonDB và ETIS-Larib **[CHỜ KẾT QUẢ]**.

**Phạm vi mô hình và thực nghiệm:**
- Chỉ có một lớp đối tượng là polyp.
- Hai mô hình chỉ khác nhau ở tầng 10. Mọi siêu tham số khác giữ giống nhau.
- Mỗi mô hình được huấn luyện 100 epoch, ảnh vào 640×640, với 20 seed (seed 0–19).
- PraNet [9] và U-Net [10] được huấn luyện trên cùng dữ liệu, chỉ để đối chiếu chỉ số theo điểm ảnh.

**Phạm vi ứng dụng:**
- Ứng dụng PolypVision gồm dịch vụ suy luận (FastAPI), website (Spring Boot) và ứng dụng di động (Flutter).
- Ứng dụng xử lý ảnh tĩnh do người dùng tải lên, chưa xử lý video trực tiếp từ máy nội soi.
- Ứng dụng phục vụ nghiên cứu và minh họa, **không phải thiết bị y tế** và không thay thế chẩn đoán của bác sĩ.

## 4. Phương pháp nghiên cứu

**Nghiên cứu lý thuyết:** đọc và tổng hợp tài liệu về phân đoạn polyp, họ YOLO, cơ chế chú ý, mô hình không gian trạng thái, Mamba và VMamba. Kết quả được trình bày ở Chương 1 và Chương 2.

**Nghiên cứu thực nghiệm có đối chứng:**
- Mô hình gốc YOLO26s-seg là nhóm đối chứng. Mô hình tích hợp là nhóm thử nghiệm.
- Hai mô hình dùng chung dữ liệu, cách tiền xử lý, siêu tham số và danh sách seed. Vì vậy, khác biệt có hệ thống giữa hai mô hình chỉ đến từ tầng 10.
- Kết quả được ghép cặp theo seed. Chênh lệch được kiểm định bằng kiểm định t ghép cặp và kiểm định Wilcoxon, kèm khoảng tin cậy 95% và cỡ hiệu ứng.
- Thí nghiệm tách thành phần (ablation) tắt lần lượt từng nhánh của khối đề xuất để đo đóng góp của từng nhánh.

**Các độ đo sử dụng** (định nghĩa ở mục 2.7):

| Nhóm | Độ đo |
|---|---|
| Chất lượng phân đoạn theo đối tượng | mask mAP50–95 (độ đo chính), mask mAP50, Precision, Recall, F1 |
| Chất lượng phân đoạn theo điểm ảnh | Dice, IoU, Precision, Recall theo điểm ảnh |
| Chi phí | Số tham số, chi phí tính toán (FLOPs) **[CHỜ ĐO]**, thời gian suy luận trên CPU và GPU **[GPU: CHỜ ĐO]**, thời gian huấn luyện |
| Lỗi phát hiện | Số dương tính đúng (TP), dương tính giả (FP), âm tính giả (FN) |

**Nghiên cứu ứng dụng:** xây dựng PolypVision, tích hợp hai checkpoint đã huấn luyện, cho phép tải ảnh, xem mặt nạ, độ tin cậy và so sánh hai mô hình trên cùng một ảnh.

## 5. Đóng góp của đề tài

- **Về mô hình:** thiết kế và cài đặt khối C2TSVMamba thay khối C2PSA ở tầng 10 của YOLO26s-seg. Khối này kết hợp nhánh SS2D quét bốn hướng với nhánh trích đặc trưng hình dạng đa tỉ lệ và có hướng, nối với nhau qua một cổng điều khiển. Bản cài đặt chỉ dùng PyTorch, không cần biên dịch kernel CUDA riêng.
- **Về kỹ thuật:** khi lưu checkpoint ở dạng FP16 (mặc định của Ultralytics), một thống kê của lớp chuẩn hóa lô trong khối mới vượt giới hạn của FP16 và bị tràn số. Đề tài phát hiện vấn đề này và chuyển sang lưu FP32, nhờ đó trọng số của khối mới được lưu và nạp lại đúng.
- **Về đánh giá:** so sánh hai mô hình trên nhiều seed ghép cặp, có kiểm định thống kê, khoảng tin cậy và cỡ hiệu ứng, thay vì chỉ báo cáo một lần chạy tốt nhất. Mọi con số đều truy được về tệp kết quả gốc và script tính lại.
- **Về ứng dụng:** xây dựng PolypVision gồm dịch vụ suy luận dùng chung cho Web và Mobile, có chức năng so sánh hai mô hình trên cùng ảnh.

Đề tài không khẳng định mô hình đề xuất tốt hơn mô hình gốc khi chưa có bằng chứng thống kê. Kết quả cụ thể và mức độ tin cậy được trình bày ở Chương 6.

## 6. Kế hoạch thực hiện và phân công công việc

### 6.1. Kế hoạch theo tuần

Đề tài thực hiện trong 12 tuần, từ 17/08/2026 đến 08/11/2026. Nội dung từng tuần lấy theo đề cương đã duyệt. Cột "Người phụ trách", "Sản phẩm" và "Trạng thái" do nhóm điền.

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

> **Gợi ý điền:** cột "Sản phẩm" nên ghi thứ kiểm tra được, ví dụ "bộ dữ liệu BG20 ở định dạng YOLO", "các lượt huấn luyện trên Kaggle", "API `/predict`", "Chương 2 bản nháp". Cột "Trạng thái" ghi "Hoàn thành", "Hoàn thành trễ (lý do)" hoặc "Điều chỉnh (lý do)". Nếu thực tế khác kế hoạch (ví dụ phần huấn luyện kéo dài hơn dự kiến), nên ghi rõ để thể hiện việc theo dõi tiến độ.

### 6.2. Phân công công việc

*Bảng 0.2. Phân công nhiệm vụ trong nhóm*

| Thành viên | MSSV | Lớp | Vai trò | Nhiệm vụ chính | Chương phụ trách viết | Mức đóng góp (%) |
|---|---|---|---|---|---|---|
| Lê Đức Lương | 2001230490 | 14DHTH09 | [ĐIỀN, ví dụ: Nhóm trưởng] | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Phùng Tuấn Huy | 2001230312 | 14DHTH13 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Trần Mạnh Toàn | 2001230830 | 14DHTH09 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |

*Bảng 0.3. Phân công theo hạng mục công việc*

Ghi **C** (chính) hoặc **H** (hỗ trợ) vào từng ô.

| Hạng mục | Lê Đức Lương | Phùng Tuấn Huy | Trần Mạnh Toàn |
|---|:---:|:---:|:---:|
| Khảo sát tài liệu, viết Chương 1 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Cơ sở lý thuyết, viết Chương 2 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Thu thập và tiền xử lý dữ liệu, viết Chương 4 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Thiết kế và cài đặt khối C2TSVMamba, viết Chương 3 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Huấn luyện Baseline và TSVM trên Kaggle | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Huấn luyện PraNet, U-Net | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Thí nghiệm tách thành phần (ablation) | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Phân tích thống kê, vẽ hình, viết Chương 6 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Dịch vụ suy luận FastAPI | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Website Spring Boot, MongoDB | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Ứng dụng di động Flutter | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Viết Chương 5 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Mở đầu, Kết luận, định dạng báo cáo | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Slide và chuẩn bị bảo vệ | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |

### 6.3. Cách phối hợp và theo dõi tiến độ

- Nhóm gặp giảng viên hướng dẫn ít nhất một lần mỗi tuần, theo yêu cầu của đề cương. Trước mỗi buổi gặp, các phần việc được gộp vào cùng một tài liệu và một kho mã.
- Mã nguồn, cấu hình và kết quả huấn luyện được quản lý bằng Git **[ĐIỀN: tên kho/nền tảng nếu muốn nêu]**.
- Các lượt huấn luyện được chia cho nhiều tài khoản Kaggle để chạy song song, mỗi lượt lưu riêng tệp `args.yaml`, `results.csv` và trọng số.
- [ĐIỀN: công cụ trao đổi trong nhóm, ví dụ Zalo, Google Drive; tần suất họp nhóm.]

## 7. Bố cục báo cáo

Ngoài phần Mở đầu và Kết luận, báo cáo gồm sáu chương:
- **Chương 1. Tổng quan:** bối cảnh bài toán, các bộ dữ liệu công khai, các hướng nghiên cứu phân đoạn polyp từ CNN, Transformer đến Mamba, và khoảng trống mà đề tài hướng tới.
- **Chương 2. Cơ sở lý thuyết:** các bài toán thị giác máy tính, mạng tích chập, họ YOLO và YOLO26-seg, cơ chế chú ý, mô hình không gian trạng thái, Mamba và VMamba, các độ đo và phương pháp kiểm định thống kê.
- **Chương 3. Mô hình đề xuất:** kiến trúc khối C2TSVMamba, thuật toán quét song song, cách khởi tạo, quy trình huấn luyện và suy luận.
- **Chương 4. Dữ liệu và tiền xử lý:** nguồn dữ liệu, cách xây dựng bộ BG20, chuyển mặt nạ sang nhãn đa giác và các bước tiền xử lý.
- **Chương 5. Cài đặt và ứng dụng:** môi trường thực nghiệm, cài đặt hai mô hình, quy trình huấn luyện trên Kaggle và ứng dụng PolypVision.
- **Chương 6. Thực nghiệm và đánh giá:** kết quả so sánh nhiều seed, thí nghiệm tách thành phần, chi phí tính toán, so sánh với PraNet và U-Net, kết quả trên dữ liệu ngoài.
