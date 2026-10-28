# CHƯƠNG 1. TỔNG QUAN

> **Ghi chú soạn thảo (xóa khi nộp):** số tài liệu tham khảo theo `TLTK/00_TONG_HOP_NOI_DUNG_71_TAI_LIEU.md`. Các tài liệu còn thiếu đã được bổ sung vào danh mục ngày 28/10/2026 ([72]–[77]). Phần mô tả công trình được viết theo bản tóm tắt; trước khi nộp cần đối chiếu lại với bài gốc.

Chương này trình bày bối cảnh của bài toán phân đoạn polyp, các bộ dữ liệu công khai và các hướng nghiên cứu chính. Thứ tự trình bày đi từ mạng tích chập, qua Transformer, đến mô hình không gian trạng thái Mamba. Cuối chương, đề tài được đặt cạnh các công trình gần nhất để chỉ ra khoảng trống mà khóa luận hướng tới.

## 1.1. Bối cảnh y khoa

### 1.1.1. Ung thư đại trực tràng và polyp

Ung thư đại trực tràng đứng thứ ba về số ca mắc mới và thứ hai về số ca tử vong trong các bệnh ung thư năm 2022 [1]. Phần lớn các ca phát triển qua nhiều năm từ polyp, tức những khối mô nhô lên từ niêm mạc ruột. Không phải polyp nào cũng hóa ác, nhưng u tuyến (adenoma) là loại có nguy cơ cao. Phát hiện và cắt bỏ polyp sớm khi nội soi giúp giảm nguy cơ tiến triển thành ung thư [77].

### 1.1.2. Giới hạn của nội soi

Nội soi đại tràng là phương pháp chuẩn để tìm polyp, nhưng kết quả phụ thuộc vào kinh nghiệm, sự tập trung của bác sĩ và chất lượng chuẩn bị ruột. Hai nhóm bằng chứng cho thấy giới hạn này:
- **Tỉ lệ bỏ sót cao.** Khi bệnh nhân được nội soi hai lần liên tiếp, lần đầu bỏ sót khoảng 26% u tuyến; với u tuyến phẳng, tỉ lệ này khoảng 34% [2].
- **Phát hiện nhiều hơn thì giảm nguy cơ.** Theo dõi hơn 300 nghìn ca nội soi cho thấy tỉ lệ phát hiện u tuyến của bác sĩ tăng 1% thì nguy cơ ung thư xuất hiện giữa hai lần nội soi giảm khoảng 3% [3].

Vì vậy, các hệ thống máy tính hỗ trợ phát hiện và khoanh vùng polyp được xem là công cụ có ích. Những hệ thống như vậy không thay bác sĩ ra quyết định. Vai trò của chúng là nhắc bác sĩ chú ý những vùng nghi ngờ có thể bị bỏ qua.

## 1.2. Bài toán phân đoạn polyp

### 1.2.1. Phát biểu bài toán

Đầu vào là một ảnh nội soi màu. Đầu ra là mặt nạ nhị phân cùng kích thước ảnh: điểm ảnh thuộc polyp mang giá trị 1, còn lại mang giá trị 0. Đề tài giải bài toán ở dạng **phân đoạn thực thể** (instance segmentation): mỗi polyp có hộp bao, độ tin cậy và mặt nạ riêng. Các mặt nạ có thể gộp lại thành một mặt nạ chung khi cần so sánh với các phương pháp phân đoạn ngữ nghĩa. Mục 2.1 phân biệt rõ các dạng bài toán này.

So với chỉ vẽ hộp bao, mặt nạ cho biết chính xác hình dạng và đường biên của tổn thương. Thông tin này có ích khi bác sĩ cần ước lượng kích thước hoặc quan sát ranh giới polyp với niêm mạc lành.

### 1.2.2. Các khó khăn đặc thù

Các khảo sát về phân đoạn polyp [8] và các bộ dữ liệu chuẩn [9] nêu một số khó khăn chung:
- **Tương phản thấp.** Màu và kết cấu của polyp gần giống niêm mạc xung quanh, nhất là với polyp phẳng. Đường biên vì thế mờ.
- **Nhiễu do điều kiện chụp.** Ảnh có vùng phản quang của đèn nội soi, bọt, dịch, nếp gấp ruột và chuyển động gây nhòe.
- **Kích thước và hình dạng đa dạng.** Polyp có thể chỉ chiếm vài phần trăm khung hình hoặc gần như toàn bộ ảnh, có dạng tròn, dạng cuống hoặc dạng phẳng.
- **Khác biệt giữa các trung tâm.** Mỗi bệnh viện dùng thiết bị và quy trình khác nhau. Mô hình học tốt trên dữ liệu của một nơi có thể kém đi khi gặp ảnh từ nơi khác [10].
- **Dữ liệu có nhãn ít.** Vẽ mặt nạ cho từng điểm ảnh cần chuyên gia và tốn nhiều thời gian, nên các bộ dữ liệu thường chỉ có vài trăm đến vài nghìn ảnh.

Những khó khăn này giải thích vì sao một mô hình phân đoạn polyp cần hai năng lực cùng lúc: nhìn chi tiết cục bộ để bám sát đường biên, và nắm ngữ cảnh toàn ảnh để phân biệt polyp với các vùng trông giống polyp.

## 1.3. Các bộ dữ liệu công khai

*Bảng 1.1. Một số bộ dữ liệu phân đoạn polyp công khai*

| Bộ dữ liệu | Số ảnh | Đặc điểm | Vai trò trong đề tài |
|---|---|---|---|
| Kvasir-SEG [4] | 1.000 | Ảnh polyp kèm mặt nạ do bác sĩ vẽ và chuyên gia duyệt; độ phân giải khác nhau | Nguồn ảnh polyp chính |
| Kvasir [5] | Bản v2: 8 lớp, mỗi lớp 1.000 ảnh | Ảnh nội soi tiêu hóa phân loại theo mốc giải phẫu, tổn thương, thủ thuật | Lấy 200 ảnh lớp *normal-cecum* làm ảnh nền |
| CVC-ClinicDB [73] | 612 | Khung hình cắt từ video nội soi, kèm mặt nạ | Dữ liệu ngoài, kiểm tra trên dữ liệu thực tế |
| CVC-ColonDB [74] | 380 | Khung hình cắt từ video nội soi | Dữ liệu ngoài |
| ETIS-Larib [75] | 196 | Nhiều polyp nhỏ, khó phát hiện | Dữ liệu ngoài |
| Bộ chuẩn CVC (EndoScene) [9] | Gộp từ các bộ CVC | Nhãn cho polyp, lòng ruột và vùng phản quang | Tham khảo |
| PolypGen [10] | 1.537 ảnh đơn từ 6 trung tâm (1.412 có polyp, 125 không polyp) | Thu ở nhiều bệnh viện và thiết bị, dùng để đánh giá khả năng tổng quát hóa | Dữ liệu ngoài, đánh giá theo từng trung tâm |

Trong đề tài, Kvasir-SEG được chọn làm dữ liệu huấn luyện vì có mặt nạ chất lượng, được dùng phổ biến và có sẵn danh sách chia huấn luyện/kiểm định do nhóm tác giả cung cấp. Ba bộ CVC-ClinicDB, CVC-ColonDB và ETIS-Larib là ảnh cắt từ video, khác nguồn với Kvasir-SEG. Đề tài dùng chúng để kiểm tra mô hình trên dữ liệu chưa thấy khi huấn luyện **[CHỜ KẾT QUẢ, xem Chương 6]**.

## 1.4. Các hướng nghiên cứu phân đoạn polyp

### 1.4.1. Mạng tích chập dạng mã hóa – giải mã

**U-Net** [11] là kiến trúc nền của phân đoạn ảnh y tế. Mạng gồm hai nửa đối xứng:
- nửa mã hóa giảm dần kích thước và tăng dần số kênh để trích đặc trưng ngữ nghĩa;
- nửa giải mã phóng to dần để khôi phục kích thước ảnh;
- các kết nối tắt (skip connection) chuyển chi tiết không gian từ nửa mã hóa sang nửa giải mã.

Nhờ cấu trúc này, U-Net huấn luyện được với lượng ảnh nhỏ. **UNet++** [12] thay các kết nối tắt đơn bằng một mạng các đường nối lồng nhau, nhằm thu hẹp khoảng cách ngữ nghĩa giữa đặc trưng của hai nửa.

**PraNet** [13] là mạng thiết kế riêng cho polyp. Mạng trước hết dự đoán một bản đồ vị trí thô, sau đó dùng *chú ý ngược* (reverse attention): xóa vùng đã chắc chắn là polyp để tập trung tinh chỉnh vùng biên còn mơ hồ. Cách làm này đặt trọng tâm vào đường biên, đúng với khó khăn chính của bài toán.

Điểm mạnh của nhóm này là bám tốt chi tiết cục bộ. Điểm yếu là mỗi lớp tích chập chỉ nhìn một vùng nhỏ. Muốn có ngữ cảnh toàn ảnh, mạng phải xếp chồng nhiều lớp và giảm kích thước nhiều lần, đổi lại mất bớt chi tiết.

### 1.4.2. Transformer và mô hình lai

Transformer dùng cơ chế tự chú ý (self-attention): mỗi vị trí so sánh trực tiếp với mọi vị trí khác. Nhờ vậy mô hình có ngữ cảnh toàn cục ngay trong một lớp. Một số công trình tiêu biểu cho polyp:
- **Polyp-PVT** [14] dùng Pyramid Vision Transformer làm bộ mã hóa, thêm các mô-đun hợp nhất đặc trưng và tách polyp lẫn vào nền.
- **ColonFormer** [15] dùng bộ mã hóa Transformer phân cấp, bộ giải mã nhiều mức và mô-đun tinh chỉnh biên. Đây là công trình của nhóm tác giả Việt Nam.
- **TransFuse** [16] chạy song song một nhánh CNN và một nhánh Transformer rồi trộn hai nhánh. Công trình này cho thấy rõ nhu cầu kết hợp chi tiết cục bộ với ngữ cảnh toàn cục.

Hạn chế chung là chi phí. Với $N$ vị trí, attention phải tính $N^2$ cặp tương quan. Chi phí này tăng rất nhanh khi ảnh lớn hoặc khi áp dụng ở bản đồ đặc trưng có độ phân giải cao (mục 2.5).

### 1.4.3. Phát hiện và phân đoạn một giai đoạn: họ YOLO

YOLO [17] xem phát hiện vật thể là một phép hồi quy: ảnh đi qua mạng một lần và cho ra trực tiếp hộp bao và lớp. Cách làm này nhanh hơn nhiều so với các mô hình hai giai đoạn, nên YOLO được dùng rộng rãi khi cần xử lý thời gian thực. Các phiên bản sau bổ sung nhánh dự đoán mặt nạ theo cách của YOLACT [37] để làm phân đoạn thực thể. YOLOv10 [38] đưa ra cách huấn luyện hai đầu để bỏ bước lọc trùng NMS, cùng khối chú ý một phần PSA.

**YOLO26** [6] là phiên bản được Ultralytics công bố năm 2026 (bản tiền ấn phẩm) và được dùng trong đề tài. Mô hình kế thừa hai cơ chế trên của YOLOv10: suy luận end-to-end không cần NMS và khối C2PSA ở cuối backbone, đồng thời có đầu riêng cho phân đoạn. Chi tiết kiến trúc ở mục 2.4.

Theo khảo sát của nhóm, các công trình phân đoạn polyp phần lớn dùng mạng dạng U (mục 1.4.1 và 1.4.5). Họ YOLO đã được dùng cho polyp, nhưng chủ yếu ở bài toán phát hiện bằng hộp bao, ví dụ YOLOv4 cải tiến cho phát hiện polyp thời gian thực [76]. Điều này tạo một khoảng trống: dùng mô hình phân đoạn thực thể một giai đoạn, vốn nhanh và cho cả hộp bao lẫn độ tin cậy, cho bài toán polyp.

### 1.4.4. Mô hình không gian trạng thái và Mamba

Mô hình không gian trạng thái (State Space Model, SSM) xuất phát từ lý thuyết điều khiển. Mô hình duy trì một trạng thái ẩn và cập nhật trạng thái đó theo từng phần tử của chuỗi.
- **S4** [18] đưa ra cách tham số hóa giúp SSM xử lý hiệu quả chuỗi rất dài.
- **Mamba** [19] cho các tham số của SSM phụ thuộc vào đầu vào. Nhờ cơ chế chọn lọc này, mô hình tự quyết định giữ hay quên thông tin ở từng bước. Mamba có chi phí tăng gần tuyến tính theo độ dài chuỗi khi dùng thuật toán quét tối ưu cho GPU.

Ảnh là dữ liệu hai chiều, không có thứ tự tự nhiên như chuỗi. Hai cách đưa Mamba vào ảnh được dùng nhiều:
- **Vision Mamba (Vim)** [46] trải ảnh thành chuỗi các mảnh rồi quét theo hai chiều xuôi và ngược.
- **VMamba** [7] đề xuất mô-đun SS2D, quét bản đồ đặc trưng theo bốn hướng (trái sang phải, phải sang trái, trên xuống dưới, dưới lên trên) rồi gộp kết quả. Nhờ vậy, mỗi vị trí nhận được thông tin từ cả bốn phía. Đề tài dùng SS2D làm nhánh ngữ cảnh toàn cục.

### 1.4.5. Mamba cho ảnh y tế và polyp

Từ năm 2024, nhiều công trình đưa Mamba vào phân đoạn ảnh y tế:
- **U-Mamba** [20] chèn khối lai CNN–SSM vào khung nnU-Net.
- **Mamba-UNet** [21] xây dựng mạng dạng U hoàn toàn bằng khối Visual Mamba.
- **Swin-UMamba** [22] cho thấy bộ mã hóa Mamba được khởi tạo từ trọng số tiền huấn luyện trên ImageNet cải thiện rõ kết quả phân đoạn y tế. Điểm này liên quan trực tiếp tới đề tài, vì nhánh SS2D trong khối đề xuất được khởi tạo mới, không có trọng số tiền huấn luyện.

Riêng với polyp:
- **Polyp-Mamba** [23] kết hợp Visual Mamba với mô-đun ngữ nghĩa theo tỉ lệ.
- **PolyMamba** [24] thêm thông tin vị trí có sẵn để bù cho kiểu quét cố định của Mamba, và dùng lọc tần số cao có cổng để làm rõ biên polyp.
- **SAM-Mamba** [25] và **SAM-MaGuP** [26] gắn Mamba vào mô hình nền tảng Segment Anything. SAM-MaGuP dùng Mamba để đưa thông tin biên có sẵn vào mô hình, giúp phân đoạn tốt hơn trên dữ liệu khác nguồn.
- **Topo-VM-UNetV2** [27] đưa thông tin tô-pô vào mạng VM-UNetV2: bản đồ chú ý tô-pô được tính bằng phương pháp đồng điều bền vững (persistent homology), rồi đưa vào mô-đun hợp nhất đặc trưng SDI qua quy trình huấn luyện hai giai đoạn.
- **CSG-Mamba** [28] dùng cổng chấm điểm bằng tích chập trong mạng SSM cho polyp, cho thấy hướng nghiên cứu này vẫn đang phát triển trong năm 2026.

Hai nhận xét rút ra từ nhóm công trình này:
1. **Hình dạng và đường biên là manh mối quan trọng.** Nhiều công trình [24], [26], [27] bổ sung thông tin biên, tần số cao hoặc tô-pô vào các mạng dùng Mamba. Đây là cơ sở để khối đề xuất có thêm nhánh hình dạng và hướng.
2. **Gần như tất cả đều là mạng dạng U** cho phân đoạn ngữ nghĩa. Rất ít công trình đưa Mamba vào mô hình phân đoạn thực thể một giai đoạn như YOLO-seg.

### 1.4.6. Mamba trong họ YOLO

Hai công trình gần nhất với đề tài là:
- **Mamba YOLO** [29] thay các khối của YOLO bằng khối SSM (ODSS) để thêm ngữ cảnh toàn cục. Công trình thử trên COCO và PASCAL VOC cho bài toán phát hiện vật thể. Phần lớn backbone được thay thế.
- **MambaPSA** [30] thay đúng khối C2PSA ở cuối backbone YOLO26 bằng một khối Mamba nhẹ, đồng thời thêm mô-đun Mamba hai chiều (BiViM) ở neck. Công trình thử trên PASCAL VOC cho bài toán phát hiện vật thể, với YOLO26 cỡ *nano*. Theo bài báo, so với YOLO26-nano gốc, toàn mô hình giảm 2,9% số tham số, giảm 12,1% FLOPs và tăng tốc độ trên CPU, trong khi mAP50:95 gần như giữ nguyên (giảm 0,1 điểm). Bài báo là bản tiền ấn phẩm. Mọi kết quả chỉ từ **một seed huấn luyện**, và chính các tác giả lưu ý rằng dao động giữa các seed có thể ngang mức chênh lệch được báo cáo.

## 1.5. Tổng hợp và khoảng trống nghiên cứu

### 1.5.1. Bảng tổng hợp các hướng tiếp cận

*Bảng 1.2. Tổng hợp các nhóm phương pháp phân đoạn polyp*

| Nhóm | Ví dụ | Điểm mạnh | Hạn chế |
|---|---|---|---|
| CNN dạng U | U-Net [11], UNet++ [12], PraNet [13] | Bám chi tiết cục bộ và đường biên tốt; ít dữ liệu vẫn học được | Vùng nhìn của mỗi lớp nhỏ, ngữ cảnh toàn cục hạn chế |
| Transformer, mô hình lai | Polyp-PVT [14], ColonFormer [15], TransFuse [16] | Có ngữ cảnh toàn cục ngay trong một lớp | Chi phí tăng theo bình phương số vị trí; cần nhiều dữ liệu hoặc tiền huấn luyện |
| YOLO một giai đoạn | YOLO [17], YOLO26 [6] | Nhanh; cho cả hộp bao, độ tin cậy và mặt nạ | Ít được nghiên cứu cho phân đoạn polyp; mặt nạ có độ phân giải thấp hơn ảnh |
| Mamba dạng U | U-Mamba [20], Polyp-Mamba [23], PolyMamba [24], Topo-VM-UNetV2 [27] | Ngữ cảnh toàn cục với chi phí thấp hơn attention; một số có thêm thông tin biên, tô-pô | Chủ yếu là phân đoạn ngữ nghĩa; quét theo thứ tự cố định |
| Mamba trong YOLO | Mamba YOLO [29], MambaPSA [30] | Thêm ngữ cảnh toàn cục vào mô hình nhanh | Đến nay chỉ thử cho phát hiện vật thể trên dữ liệu tổng quát |

### 1.5.2. Vị trí của đề tài

*Bảng 1.3. So sánh đề tài với các công trình gần nhất*

| Tiêu chí | Mamba YOLO [29] | MambaPSA [30] | Topo-VM-UNetV2 [27] | **Đề tài** |
|---|---|---|---|---|
| Mô hình nền | YOLO | YOLO26 cỡ *nano* | VM-UNetV2 (dạng U) | **YOLO26s-seg** |
| Bài toán | Phát hiện vật thể | Phát hiện vật thể | Phân đoạn ngữ nghĩa | **Phân đoạn thực thể** |
| Dữ liệu | COCO, VOC | PASCAL VOC | Ảnh polyp | **Ảnh polyp (Kvasir-SEG + ảnh nền)** |
| Phạm vi thay đổi | Thay phần lớn backbone | Thay C2PSA, thêm khối ở neck | Thêm bản đồ chú ý tô-pô | **Chỉ thay C2PSA ở tầng 10** |
| Khối Mamba | Khối SSM riêng | Mamba nhẹ, BiViM hai chiều | VMamba | **SS2D bốn hướng + nhánh hình dạng có hướng + cổng** |
| Cách đánh giá | Một lần chạy **[CẦN KIỂM TRA]** | Một seed (tác giả tự nêu là hạn chế) | 5 seed, lấy trung bình | **20 seed ghép cặp, có kiểm định thống kê** |

Từ các bảng trên, khoảng trống mà đề tài hướng tới gồm ba điểm:
1. Theo khảo sát của nhóm đến tháng 10/2026, chưa thấy công trình nào đưa khối VMamba vào **YOLO26-seg** cho **phân đoạn thực thể polyp**.
2. Các công trình đưa Mamba vào YOLO chưa kết hợp thông tin **hình dạng và đường biên**, trong khi nhóm công trình Mamba cho polyp cho thấy thông tin này quan trọng.
3. Các công trình gần nhất hoặc chỉ báo cáo một lần huấn luyện [30], hoặc lấy trung bình vài seed nhưng không kiểm định thống kê ghép cặp [27]. Với dữ liệu nhỏ như Kvasir-SEG, dao động giữa các lần huấn luyện có thể lớn hơn mức chênh lệch giữa hai mô hình [64]. Cần đánh giá lặp lại nhiều seed, ghép cặp và có kiểm định để kết luận đáng tin.

Đề tài không nhắm tới việc vượt các mô hình tốt nhất hiện nay. Mục tiêu là trả lời câu hỏi có kiểm soát: **chỉ thay một tầng của YOLO26s-seg bằng khối VMamba có nhận biết hình dạng thì kết quả thay đổi thế nào, với độ tin cậy thống kê ra sao, và tốn thêm bao nhiêu chi phí**.

Cũng cần nói rõ một khác biệt với MambaPSA. Khối đề xuất trong đề tài **tăng** số tham số của tầng 10 (khoảng 1,81 triệu so với 0,99 triệu của C2PSA) và làm suy luận trên CPU **chậm hơn**. Đề tài không nhắm tới làm mô hình nhẹ hơn như MambaPSA.

## 1.6. Tình hình nghiên cứu trong nước

Trong nước, ngoài ColonFormer [15] đã nêu ở mục 1.4.2, có thể kể thêm NeoUNet và bộ dữ liệu BKAI-IGH NeoPolyp của nhóm Đại học Bách khoa Hà Nội **[CẦN XÁC MINH VÀ THÊM TLTK]**. **[ĐIỀN: nếu nhóm tìm được thêm công trình trong nước về phân đoạn polyp hoặc ứng dụng YOLO trong nội soi, ví dụ luận văn, bài hội thảo FAIR, RIVF, tạp chí khoa học của các trường, thì bổ sung tại đây; nếu không, giữ đoạn này ngắn.]** Theo khảo sát của nhóm, chưa thấy công trình trong nước nào tích hợp Mamba vào YOLO cho bài toán polyp **[CẦN XÁC NHẬN]**.

## 1.7. Kết chương

Chương 1 đã trình bày:
- bối cảnh y khoa: ung thư đại trực tràng phổ biến, polyp vẫn bị bỏ sót khi nội soi, nên công cụ hỗ trợ khoanh vùng có giá trị;
- bài toán phân đoạn polyp và các khó khăn đặc thù: biên mờ, nhiễu, kích thước đa dạng, ít dữ liệu;
- các bộ dữ liệu công khai, trong đó Kvasir-SEG là nguồn chính của đề tài;
- các hướng nghiên cứu từ CNN, Transformer đến Mamba, và các công trình đưa Mamba vào YOLO.

Khoảng trống được xác định là: chưa có công trình đưa VMamba kèm thông tin hình dạng vào YOLO26-seg cho phân đoạn polyp, với cách đánh giá lặp lại nhiều seed. Chương 2 trình bày cơ sở lý thuyết cần thiết, gồm YOLO26-seg, cơ chế chú ý, mô hình không gian trạng thái, VMamba và các độ đo.
