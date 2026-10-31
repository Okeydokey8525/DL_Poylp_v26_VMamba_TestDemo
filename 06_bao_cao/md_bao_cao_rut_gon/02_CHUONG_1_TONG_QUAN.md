# CHƯƠNG 1. TỔNG QUAN

> **Ghi chú soạn thảo (xóa khi nộp):** bản rút gọn, nén từ `md_bao_cao/02_CHUONG_1_TONG_QUAN.md` (tag git `ban_day_du_147`). Thứ tự trích dẫn lần đầu giữ nguyên như bản đầy đủ.

Chương này trình bày bối cảnh bài toán phân đoạn polyp, các bộ dữ liệu công khai và các hướng nghiên cứu chính, từ mạng tích chập, Transformer đến mô hình không gian trạng thái Mamba, rồi chỉ ra khoảng trống mà khóa luận hướng tới.

## 1.1. Bối cảnh và bài toán phân đoạn polyp

Ung thư đại trực tràng đứng thứ ba về số ca mắc mới và thứ hai về số ca tử vong trong các bệnh ung thư năm 2022 [1]. Phần lớn các ca phát triển qua nhiều năm từ polyp; u tuyến (adenoma) là loại có nguy cơ hóa ác cao, và cắt bỏ polyp sớm khi nội soi giúp giảm nguy cơ ung thư [2]. Tuy vậy, kết quả nội soi phụ thuộc vào kinh nghiệm và sự tập trung của bác sĩ:
- khi nội soi hai lần liên tiếp, lần đầu bỏ sót khoảng 26% u tuyến, với u tuyến phẳng khoảng 34% [3];
- tỉ lệ phát hiện u tuyến của bác sĩ tăng 1% thì nguy cơ ung thư xuất hiện giữa hai lần nội soi giảm khoảng 3% [4].

Hệ thống máy tính hỗ trợ khoanh vùng polyp vì thế có ích: không thay bác sĩ ra quyết định, mà nhắc chú ý những vùng nghi ngờ có thể bị bỏ qua.

**Phát biểu bài toán.** Đầu vào là một ảnh nội soi màu; đầu ra là mặt nạ nhị phân cùng kích thước, điểm ảnh thuộc polyp mang giá trị 1. Đề tài giải bài toán ở dạng **phân đoạn thực thể**: mỗi polyp có hộp bao, độ tin cậy và mặt nạ riêng; các mặt nạ có thể gộp lại để so sánh với phương pháp phân đoạn ngữ nghĩa (mục 2.1). So với hộp bao, mặt nạ cho biết hình dạng và đường biên tổn thương.

**Khó khăn đặc thù** [11]: polyp có tương phản thấp với niêm mạc, nhất là polyp phẳng; ảnh có phản quang, bọt, dịch, nếp gấp và nhòe; kích thước và hình dạng polyp rất đa dạng; thiết bị và quy trình khác nhau giữa các trung tâm làm mô hình kém đi khi gặp ảnh nơi khác [12]; dữ liệu có nhãn ít vì vẽ mặt nạ cần chuyên gia. Do đó mô hình cần cùng lúc nhìn chi tiết cục bộ để bám đường biên và nắm ngữ cảnh toàn ảnh để phân biệt polyp với vùng trông giống polyp.

## 1.2. Các bộ dữ liệu công khai

*Bảng 1.1. Một số bộ dữ liệu phân đoạn polyp công khai*

| Bộ dữ liệu | Số ảnh | Đặc điểm | Vai trò trong đề tài |
|---|---|---|---|
| Kvasir-SEG [5] | 1.000 | Ảnh polyp kèm mặt nạ do bác sĩ vẽ và chuyên gia duyệt; độ phân giải khác nhau | Nguồn ảnh polyp chính |
| Kvasir [8] | Bản v2: 8 lớp, mỗi lớp 1.000 ảnh | Ảnh nội soi tiêu hóa phân loại theo mốc giải phẫu, tổn thương, thủ thuật | Lấy 200 ảnh lớp *normal-cecum* làm ảnh nền |
| CVC-ClinicDB [13] | 612 | Khung hình cắt từ video nội soi, kèm mặt nạ | Dữ liệu ngoài, kiểm tra trên dữ liệu thực tế |
| CVC-ColonDB [14] | 380 (bản dùng trong các benchmark phân đoạn từ PraNet [9]; bài gốc mô tả 300 ảnh) | Khung hình cắt từ 15 đoạn video nội soi | Dữ liệu ngoài |
| ETIS-Larib [15] | 196 | Nhiều polyp nhỏ, khó phát hiện | Dữ liệu ngoài |
| PolypGen [12] | 1.537 ảnh đơn từ 6 trung tâm (1.412 có polyp, 125 không polyp) | Thu ở nhiều bệnh viện và thiết bị | Dữ liệu ngoài, đánh giá theo từng trung tâm |

Kvasir-SEG được chọn làm dữ liệu huấn luyện vì có mặt nạ chất lượng, được dùng phổ biến và có sẵn danh sách chia huấn luyện/kiểm định của nhóm tác giả. Bốn bộ còn lại khác nguồn với Kvasir-SEG, dùng để kiểm tra mô hình trên dữ liệu chưa thấy (mục 6.7).

## 1.3. Các hướng nghiên cứu phân đoạn polyp

### 1.3.1. Mạng tích chập dạng mã hóa – giải mã

**U-Net** [10] gồm nửa mã hóa giảm kích thước, tăng số kênh; nửa giải mã phóng to dần; và các kết nối tắt chuyển chi tiết không gian từ nửa mã hóa sang nửa giải mã, nhờ đó học được với lượng ảnh nhỏ. **PraNet** [9] dự đoán bản đồ vị trí thô rồi dùng *chú ý ngược*: xóa vùng đã chắc chắn là polyp để tập trung tinh chỉnh vùng biên còn mơ hồ. Nhóm này bám tốt chi tiết cục bộ, nhưng mỗi lớp tích chập chỉ nhìn vùng nhỏ; muốn có ngữ cảnh toàn ảnh phải xếp chồng nhiều lớp và giảm kích thước nhiều lần.

### 1.3.2. Transformer và mô hình lai

Cơ chế tự chú ý cho mỗi vị trí so sánh trực tiếp với mọi vị trí khác, nên có ngữ cảnh toàn cục ngay trong một lớp. **Polyp-PVT** [16] dùng Pyramid Vision Transformer làm bộ mã hóa, thêm mô-đun hợp nhất đặc trưng; **ColonFormer** [17] (nhóm tác giả Việt Nam) dùng bộ mã hóa Transformer phân cấp và mô-đun tinh chỉnh biên. Hạn chế chung là chi phí: với $N$ vị trí, attention phải tính $N^2$ cặp tương quan (mục 2.5).

### 1.3.3. Phát hiện và phân đoạn một giai đoạn: họ YOLO

YOLO [18] xem phát hiện vật thể là một phép hồi quy: ảnh đi qua mạng một lần và cho ra trực tiếp hộp bao và lớp, nên nhanh hơn nhiều so với mô hình hai giai đoạn. Các phiên bản sau thêm nhánh mặt nạ theo cách của YOLACT [19] để phân đoạn thực thể; YOLOv10 [20] đưa ra cách huấn luyện hai đầu để bỏ NMS, cùng khối chú ý một phần PSA. **YOLO26** [6] (Ultralytics, 2026, bản tiền ấn phẩm) kế thừa suy luận không cần NMS và khối C2PSA ở cuối backbone, có đầu riêng cho phân đoạn (mục 2.4). Họ YOLO đã được dùng cho polyp nhưng chủ yếu ở bài toán phát hiện bằng hộp bao, ví dụ YOLOv4 cải tiến cho phát hiện polyp thời gian thực [21].

### 1.3.4. Mô hình không gian trạng thái, Mamba và VMamba

Mô hình không gian trạng thái (SSM) duy trì một trạng thái ẩn và cập nhật theo từng phần tử của chuỗi. **S4** [22] đưa ra cách tham số hóa giúp SSM xử lý chuỗi rất dài; **Mamba** [23] cho tham số SSM phụ thuộc đầu vào để mô hình tự chọn giữ hay quên thông tin, với chi phí gần tuyến tính theo độ dài chuỗi. Để áp dụng cho ảnh, **VMamba** [7] đề xuất mô-đun SS2D quét bản đồ đặc trưng theo bốn hướng rồi gộp kết quả, nhờ đó mỗi vị trí nhận thông tin từ cả bốn phía. Đề tài dùng SS2D làm nhánh ngữ cảnh toàn cục.

Trong ảnh y tế, **U-Mamba** [24] chèn khối lai CNN–SSM vào nnU-Net; **Swin-UMamba** [25] cho thấy bộ mã hóa Mamba khởi tạo từ trọng số tiền huấn luyện ImageNet cải thiện rõ kết quả, điều liên quan trực tiếp vì nhánh SS2D của đề tài được khởi tạo mới. Riêng với polyp, **Polyp-Mamba** [26] kết hợp Visual Mamba với mô-đun ngữ nghĩa theo tỉ lệ; **PolyMamba** [27] thêm thông tin vị trí và lọc tần số cao có cổng để làm rõ biên; **Topo-VM-UNetV2** [28] đưa bản đồ chú ý tô-pô tính bằng đồng điều bền vững vào VM-UNetV2. Hai nhận xét rút ra: hình dạng và đường biên là manh mối quan trọng [27], [28]; và gần như tất cả là mạng dạng U cho phân đoạn ngữ nghĩa.

### 1.3.5. Mamba trong họ YOLO

- **Mamba YOLO** [29] thay phần lớn backbone YOLO bằng khối SSM (ODSS), thử trên COCO và PASCAL VOC cho phát hiện vật thể.
- **MambaPSA** [30] thay đúng khối C2PSA ở cuối backbone YOLO26 cỡ *nano* bằng khối Mamba nhẹ và thêm mô-đun BiViM ở neck, thử trên PASCAL VOC. Theo bài báo, toàn mô hình giảm 2,9% số tham số, giảm 12,1% FLOPs và tăng tốc độ trên CPU, mAP50:95 gần như giữ nguyên (giảm 0,1 điểm). Bài là bản tiền ấn phẩm, kết quả từ **một seed**, và tác giả lưu ý dao động giữa các seed có thể ngang mức chênh lệch được báo cáo.

## 1.4. Tổng hợp và khoảng trống nghiên cứu

*Bảng 1.2. Tổng hợp các nhóm phương pháp phân đoạn polyp*

| Nhóm | Ví dụ | Điểm mạnh | Hạn chế |
|---|---|---|---|
| CNN dạng U | U-Net [10], PraNet [9] | Bám chi tiết cục bộ và đường biên tốt; ít dữ liệu vẫn học được | Vùng nhìn của mỗi lớp nhỏ, ngữ cảnh toàn cục hạn chế |
| Transformer, mô hình lai | Polyp-PVT [16], ColonFormer [17] | Có ngữ cảnh toàn cục ngay trong một lớp | Chi phí tăng theo bình phương số vị trí; cần nhiều dữ liệu hoặc tiền huấn luyện |
| YOLO một giai đoạn | YOLO [18], YOLO26 [6] | Nhanh; cho cả hộp bao, độ tin cậy và mặt nạ | Ít được nghiên cứu cho phân đoạn polyp; mặt nạ có độ phân giải thấp hơn ảnh |
| Mamba dạng U | U-Mamba [24], Polyp-Mamba [26], PolyMamba [27], Topo-VM-UNetV2 [28] | Ngữ cảnh toàn cục với chi phí thấp hơn attention; một số có thêm thông tin biên, tô-pô | Chủ yếu là phân đoạn ngữ nghĩa; quét theo thứ tự cố định |
| Mamba trong YOLO | Mamba YOLO [29], MambaPSA [30] | Thêm ngữ cảnh toàn cục vào mô hình nhanh | Đến nay chỉ thử cho phát hiện vật thể trên dữ liệu tổng quát |

*Bảng 1.3. So sánh đề tài với các công trình gần nhất*

| Tiêu chí | Mamba YOLO [29] | MambaPSA [30] | Topo-VM-UNetV2 [28] | **Đề tài** |
|---|---|---|---|---|
| Mô hình nền | YOLO | YOLO26 cỡ *nano* | VM-UNetV2 (dạng U) | **YOLO26s-seg** |
| Bài toán | Phát hiện vật thể | Phát hiện vật thể | Phân đoạn ngữ nghĩa | **Phân đoạn thực thể** |
| Dữ liệu | COCO, VOC | PASCAL VOC | Ảnh polyp | **Ảnh polyp (Kvasir-SEG + ảnh nền)** |
| Phạm vi thay đổi | Thay phần lớn backbone | Thay C2PSA, thêm khối ở neck | Thêm bản đồ chú ý tô-pô | **Chỉ thay C2PSA ở tầng 10** |
| Khối Mamba | Khối SSM riêng | Mamba nhẹ, BiViM hai chiều | VMamba | **SS2D bốn hướng + nhánh hình dạng có hướng + cổng** |
| Cách đánh giá | Báo một kết quả, không nêu số lần chạy hay độ lệch chuẩn | Một seed (tác giả tự nêu là hạn chế) | 5 seed, lấy trung bình | **20 seed ghép cặp, có kiểm định thống kê** |

Khoảng trống mà đề tài hướng tới gồm ba điểm:
1. Theo khảo sát của nhóm đến tháng 10/2026, chưa thấy công trình nào đưa khối VMamba vào **YOLO26-seg** cho **phân đoạn thực thể polyp**.
2. Các công trình đưa Mamba vào YOLO chưa kết hợp thông tin **hình dạng và đường biên**.
3. Các công trình gần nhất chỉ báo cáo một lần huấn luyện [30] hoặc lấy trung bình vài seed mà không kiểm định ghép cặp [28], trong khi với dữ liệu nhỏ, dao động giữa các lần huấn luyện có thể lớn hơn chênh lệch giữa hai mô hình [31].

Đề tài không nhắm tới vượt các mô hình tốt nhất hiện nay, mà trả lời câu hỏi có kiểm soát: **chỉ thay một tầng của YOLO26s-seg bằng khối VMamba có nhận biết hình dạng thì kết quả thay đổi thế nào, với độ tin cậy thống kê ra sao, và tốn thêm bao nhiêu chi phí**. Khác với MambaPSA, khối đề xuất **tăng** số tham số của tầng 10 (khoảng 1,81 triệu so với 0,99 triệu của C2PSA) và làm suy luận trên CPU **chậm hơn**.

## 1.5. Tình hình nghiên cứu trong nước

Nhóm nghiên cứu của Trường Đại học Bách khoa Hà Nội phối hợp với Viện Nghiên cứu và Đào tạo Tiêu hóa, Gan mật có nhiều công trình về polyp: ColonFormer [17] (mục 1.3.2) và **NeoUNet** [32], vừa phân đoạn polyp vừa phân biệt polyp tân sinh với không tân sinh, kèm bộ dữ liệu NeoPolyp (phần công khai BKAI-IGH NeoPolyp-Small có 1.200 ảnh chụp bằng ánh sáng trắng và FICE). Đào Việt Hằng và cộng sự [33] đánh giá YOLOv8 phát hiện polyp trên 30 video nội soi thu tại Hà Nội: mô hình phát hiện được 65/68 polyp nhưng còn nhiều báo nhầm theo từng khung hình (Precision 0,48 ở ngưỡng IoU 0,5), và chỉ dừng ở phát hiện bằng hộp bao. Trong phạm vi khảo sát (arXiv, Crossref và kho tài liệu của một số trường), chưa thấy công trình trong nước nào đưa khối Mamba vào mô hình họ YOLO cho bài toán polyp.

## 1.6. Kết chương

Chương 1 đã xác định khoảng trống: chưa có công trình đưa VMamba kèm thông tin hình dạng vào YOLO26-seg cho phân đoạn polyp, với cách đánh giá lặp lại nhiều seed. Chương 2 trình bày cơ sở lý thuyết cần thiết cho khối đề xuất và cách đánh giá.
