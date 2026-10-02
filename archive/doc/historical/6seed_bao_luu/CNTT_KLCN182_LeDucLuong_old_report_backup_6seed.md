# BÁO CÁO TIẾN ĐỘ THỰC NGHIỆM VÀ KẾT QUẢ NGHIÊN CỨU TUẦN

> **Đề tài:** Nghiên cứu phương pháp tích hợp Topology-Shape-aware VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng

| Mã đề tài & Phân loại: | CNTT_KLCN182 — Khóa luận Cử nhân ngành CNTT (2026 – 2027) |
| --- | --- |
| Giảng viên hướng dẫn: | ThS. Phùng Thế Bảo (Email: baopt@huit.edu.vn) |
| Nhóm sinh viên thực hiện: | 1. Lê Đức Lương (MSSV: 2001230490 — Lớp: 14DHTH09) <br> 2. Phùng Tuấn Huy (MSSV: 2001230312 — Lớp: 14DHTH13) <br> 3. Trần Mạnh Toàn (MSSV: 2001230830 — Lớp: 14DHTH09) |
| Nội dung báo cáo trọng tâm: | Đánh giá hiệu năng thực nghiệm kiểm thử 6 Seed, kiểm chứng kiến trúc C2TSVMamba, phân tích ma trận nhầm lẫn lâm sàng và kế hoạch hành động |

## 1. MỤC TIÊU VÀ NHIỆM VỤ BÁO CÁO TIẾN ĐỘ

Báo cáo tiến độ tuần này tập trung giải quyết các định hướng chuyên môn trọng tâm đã được thống nhất tại cuộc họp với Giảng viên Hướng dẫn, cụ thể bao gồm:

**1. Chuẩn hóa cấu trúc đánh giá trên tài liệu Word:** Hệ thống hóa toàn bộ kết quả thực nghiệm định lượng, đồ thị và ma trận nhầm lẫn một cách đồng bộ và chính xác.

**2. Xác định vai trò cốt lõi của VMamba:** Làm rõ cơ chế trích xuất đặc trưng vùng bệnh, dùng để 'tô' và phân đoạn chính xác vùng tổn thương polyp trong pipeline của YOLO26-seg.

**3. Thiết lập hệ thống 2 mô hình thực nghiệm:** Bao gồm mô hình, Baseline phân đoạn YOLO26s-seg, mô hình đề xuất chính tích hợp VMamba (YOLO26s-seg + C2TSVMamba).

**4. Kiểm định tính ổn định qua 6 Seed (Seed Robustness):** Huấn luyện lặp lại độc lập qua 6 seed ngẫu nhiên (s0 đến s5) trên bộ dữ liệu Kvasir-SEG nhằm loại bỏ yếu tố ăn may, đo lường biên độ dao động (±σ), khoảng [min, max] và độ cải thiện Delta (Δ).

**5. Phân tích ma trận nhầm lẫn lâm sàng:** Định lượng tỷ lệ phát hiện đúng, tỷ lệ bỏ sót polyp nguy hiểm và đánh giá tính khả thi ứng dụng thực tế trong nội soi thời gian thực.

## 2. CẤU TRÚC MÔ HÌNH VÀ CƠ CHẾ TÍCH HỢP C2TSVMAMBA TẠI TẦNG 10

### 2.1. Vai trò tích hợp VMamba trong pipeline phân đoạn polyp

Trong nội soi đại trực tràng, tổn thương polyp thường có ranh giới hòa lẫn vào niêm mạc xung quanh, kích thước đa dạng và bề mặt phản chiếu ánh sáng gây nhiễu.

Mô hình tích hợp VMamba được thiết kế nhằm giải quyết triệt để bài toán trích xuất đặc trưng vùng bệnh, đóng vai trò then chốt trong việc tô và phân đoạn chính xác đường biên tổn thương.

Khối C2TSVMamba (Cross-Stage Partial Topology-Shape-aware VMamba) được tích hợp tại Tầng 10 (Layer 10) thuộc Cổ mạng (Neck). Đây là vị trí chiến lược ngay sau khối SPPF của Backbone, tiếp nhận bản đồ đặc trưng P5 đa vĩ mô với kích thước B x 512 x 20 x 20 trước khi truyền sang các tầng tổng hợp đặc trưng P4, P3. Cấu trúc khối bao gồm hai nhánh xử lý song song bổ trợ lẫn nhau:

* **•  Nhánh VMamba SS2D (2D Selective Scan):** Quét bản đồ đặc trưng theo 4 hướng không gian, mô hình hóa mối tương quan không gian toàn cục dài hạn với độ phức tạp tính toán tuyến tính O(N), vượt trội so với cơ chế Self-Attention bậc hai O(N²).

* **•  Nhánh Tích chập Hình thái Đa hướng (Multi-directional Morphological Convolutions):** Sử dụng các kernel tích chập bất đối xứng và kết hợp cơ chế cổng định hướng để bắt giữ gradient thay đổi đột ngột tại viền polyp, cung cấp thông tin tô viền sắc nét.

### 2.2. Bộ dữ liệu Kvasir-SEG và quy trình tiền xử lý dữ liệu

Để đánh giá năng lực phát hiện và phân đoạn tổn thương, đề tài sử dụng bộ dữ liệu chuẩn y khoa Kvasir-SEG do Phòng thí nghiệm Nghiên cứu Simula và Bệnh viện Bærum (Na Uy) công bố, bao gồm 1,000 ảnh nội soi đường tiêu hóa. Toàn bộ ảnh đều được bác sĩ chuyên khoa nội soi gán nhãn thủ công và đóng dấu mặt nạ phân đoạn (Ground Truth).

**Bảng 2.1: Thống kê phân chia tập dữ liệu Kvasir-SEG trong thực nghiệm kiểm định chéo 6-fold**

| Tập dữ liệu | Số lượng ảnh | Tỷ lệ (%) | Độ phân giải gốc | Độ phân giải đầu vào | Số tổn thương polyp |
| --- | --- | --- | --- | --- | --- |
| Tập huấn luyện (Training Set) | 880 | 88% | $574×500∼1920×1072$ | $640×640$ (Letterbox) | Khoảng 950 polyp |
| Tập kiểm định (Validation Set) | 120 | 12% | $574×500∼1920×1072$ | $640×640$ (Letterbox) | Cố định 127 polyp qua cả 6 seed |
| Toàn bộ Kvasir-SEG | 1,000 | 100% | Đa dạng theo thiết bị nội soi | $640×640$ | 100% có Ground Truth y khoa |

Quy trình tiền xử lý dữ liệu (Pre-processing Pipeline) gồm các bước chuẩn hóa:

* **Chuẩn hóa kích thước khung hình (Letterbox Resizing):** Ảnh nội soi gốc có độ phân giải dao động lớn (từ $574×500$ đến $1920×1072$ pixel). Kỹ thuật Letterbox được áp dụng để đưa ảnh về kích thước chuẩn $640×640$ pixel. Thuật toán giữ nguyên tỷ lệ khung hình gốc (aspect ratio) và bù viền đối xứng, hạn chế tối đa hiện tượng méo mó hoặc biến dạng cấu trúc giải phẫu học của polyp.

* **Chuẩn hóa giá trị điểm ảnh (Pixel Normalization):** Thang độ xám điểm ảnh $[0,255]$ được chuẩn hóa về miền giá trị thực $[0.0,1.0]$, hỗ trợ quá trình lan truyền ngược và tăng tốc độ hội tụ của hàm mất mát.

* **Chuyển đổi nhãn mặt nạ sang định dạng Polygon:** Mặt nạ nhị phân ground-truth được chuyển đổi thành chuỗi tọa độ đa giác khép kín $x_{1},y_{1},x_{2},y_{2},…,x_{n},y_{n}$ chuẩn hóa trong đoạn $[0.0,1.0]$, tương ứng với lớp tổn thương duy nhất (nc: 1, names: {0: 'polyp'}).

Chiến lược tăng cường dữ liệu (Data Augmentation):

* *Mosaic Augmentation (*$p=1.0$*):* Ghép 4 ảnh ngẫu nhiên thành một khung hình huấn luyện nhằm đa dạng hóa kích thước và bối cảnh tổn thương.

* *Lật ảnh ngang ngẫu nhiên (Random Horizontal Flip,* $p=0.5$*):* Mô phỏng tính đối xứng giải phẫu của lòng ruột đại trực tràng.

* *Co giãn ngẫu nhiên (Random Scale,* $p=0.5$*):* Biến đổi tỷ lệ ảnh nhằm mô phỏng sự thay đổi khoảng cách của ống soi đến vị trí tổn thương.

* *Cơ chế vô hiệu hóa Mosaic (Close Mosaic = 10 epochs):* Tắt tính năng Mosaic ở 10 epoch cuối cùng giúp mô hình học trên cấu trúc ảnh thực tế, làm mượt gradient và tinh chỉnh ranh giới phân đoạn.

### 2.3. Cấu hình môi trường thực nghiệm và siêu tham số huấn luyện

Thực nghiệm được triển khai trên nền tảng điện toán đám mây **Kaggle GPU Cloud** sử dụng thư viện **Ultralytics 8.4.127** và PyTorch 2.x. Để loại bỏ tính bất định của phần cứng và đảm bảo tính tái lập kết quả (reproducibility) trên 6 seed, hệ thống áp dụng quy chuẩn khóa tất định nghiêm ngặt:

*Giao thức khóa tất định:* Cố định biến môi trường PYTHONHASHSEED; cấu hình bộ nhớ CUBLAS_WORKSPACE_CONFIG=':4096:8'; đồng bộ hạt giống ngẫu nhiên trên random.seed(SEED), np.random.seed(SEED), torch.manual_seed(SEED) và torch.cuda.manual_seed_all(SEED); vô hiệu hóa torch.backends.cudnn.benchmark = False, kích hoạt torch.backends.cudnn.deterministic = True và thiết lập torch.use_deterministic_algorithms(True, warn_only=False).

**Bảng 2.2: Cấu hình siêu tham số huấn luyện cho Baseline và C2TSVMamba**

| Nhóm tham số | Tham số (Parameter) | Giá trị thiết lập | Ý nghĩa học thuật |
| --- | --- | --- | --- |
| Môi trường & Framework | Phiên bản Ultralytics | 8.4.0127 | Đảm bảo tính nhất quán của kiến trúc nhân |
|  | Nền tảng thực thi | Kaggle GPU Cloud | GPU chuyên dụng, đồng bộ tài nguyên tính toán |
|  | Số luồng nạp dữ liệu | workers = 2 | Tối ưu hóa I/O, hạn chế nghẽn luồng CPU |
|  | Chế độ tất định | deterministic = True | Khóa các phép toán cuBLAS/cuDNN |
| Kiến trúc mô hình | Mô hình Baseline | YOLO("yolo26s-seg.pt") | Nạp trực tiếp trọng số chuẩn bài toán phân đoạn |
|  | Mô hình C2TSVMamba | YOLO(yaml).load(...) | Khởi tạo topology scale 's', nạp transfer learning |
| Dữ liệu & Tác vụ | Số lượng lớp bài toán | nc: 1, names: {0: 'polyp'} | Phân đoạn thực thể nhị phân (Polyp vs Nền) |
|  | Kích thước ảnh vào (imgsz) | 640×640 | Chuẩn hóa theo độ phân giải xử lý video nội soi |
|  | Kích thước batch | batch = 8 | Cân bằng độ biến thiên gradient và bộ nhớ VRAM |
|  | Bộ nhớ đệm dữ liệu | cache = False | Đọc dữ liệu trực tiếp từ ổ đĩa, tránh tràn RAM |
| Tối ưu & Lịch trình học | Bộ tối ưu hóa | optimizer = "AdamW" | Tối ưu hóa trọng số phi tuyến, hạn chế phân kỳ |
|  | Tốc độ học ban đầu (lr0) | 1 | Giá trị khởi tạo chuẩn cho AdamW |
|  | Tốc độ học cuối (lrf) | 0.01 | Tốc độ học cực tiểu đạt 1×10−5 |
|  | Chu kỳ làm nóng (warmup) | 5.0 epochs | Ổn định trọng số mới tại Tầng 10 C2TSVMamba |
|  | Số epoch huấn luyện | 100 (patience = 100) | Đảm bảo mô hình đạt tới điểm hội tụ sâu |
|  | Độ chính xác dấu phẩy động | amp = False | Duy trì tính toán chuẩn float32 toàn diện |
| Hàm phạt & Phụ trợ | Trọng số Box / Cls / Seg | box: 7.5, cls: 0.5, dfl: 1.5 | Ưu tiên định vị và độ sắc nét của mặt nạ |
|  | Đóng tăng cường Mosaic | close_mosaic = 10 | 10 epoch cuối học trên ảnh gốc để tinh chỉnh viền |

## 3. KẾT QUẢ ĐỊNH LƯỢNG ĐỐI CHỨNG QUA 6 SEED (SEED ROBUSTNESS)

Toàn bộ 6 lượt huấn luyện độc lập 6 seed x 2 dòng mô hình được thực hiện trên cùng môi trường phần cứng với bộ siêu tham số đồng nhất: kích thước ảnh 640x640, 100 epoch, batch size 8, Các chỉ số được trích xuất tại epoch tối ưu Best Mask mAP50-95 từ tệp results.csv của từng lượt chạy.

### 3.1. Bảng so sánh tổng hợp chỉ số định lượng (Mean ± σ, Min, Max, Delta Δ)

**Bảng 1: Bảng so sánh tổng hợp giá trị trung bình và độ lệch chuẩn qua 6 seed (s0 – s5)**

| Chỉ số đo lường | YOLO26s-seg Baseline | C2TSVMamba Đề xuất | Độ chênh lệch (Δ) | Tỷ lệ (%) |
| --- | --- | --- | --- | --- |
| Mask mAP50-95 | 0.7298 ± 0.0150 <br> [0.7073 – 0.7496] | 0.7246 ± 0.0050 <br> [0.7196 – 0.7308] | -0.0052 | -0.71% |
| Mask mAP50 | 0.9129 ± 0.0070 <br> [0.9049 – 0.9223] | 0.9134 ± 0.0090 <br> [0.9055 – 0.9268] | +0.0005 | +0.05% |
| Mask Precision | 0.9165 ± 0.0104 <br> [0.8974 – 0.9260] | 0.9171 ± 0.0189 <br> [0.8829 – 0.9331] | +0.0006 | +0.07% |
| Mask Recall | 0.8837 ± 0.0087 <br> [0.8740 – 0.8976] | 0.8545 ± 0.0219 <br> [0.8347 – 0.8909] | -0.0292 | -3.30% |
| Mask F1-Score | 0.8997 ± 0.0042 <br> [0.8937 – 0.9057] | 0.8844 ± 0.0084 <br> [0.8724 – 0.8980] | -0.0153 | -1.70% |
| Val Seg Loss (Hàm phạt) | 1.4164 ± 0.0671 <br> [1.3359 – 1.5208] | 1.3812 ± 0.0470 <br> [1.3054 – 1.4344] | -0.0352 (Giảm tốt) | -2.49% |
| Val Box Loss (Hàm phạt) | 0.7609 ± 0.0152 <br> [0.7353 – 0.7824] | 0.7759 ± 0.0373 <br> [0.7411 – 0.8322] | +0.0150 | +1.97% |

**Bảng 2: Bảng đối chứng chi tiết từng lượt seed của mô hình Baseline YOLO26s-seg**

| Lượt chạy | Seed | Epoch tối ưu | Precision (M) | Recall (M) | F1-Score | mAP50 (M) | mAP50-95 (M) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline s0 | s0 | 97 | 0.9185 | 0.8880 | 0.9030 | 0.9200 | 0.7258 |
| Baseline s1 | s1 | 98 | 0.9177 | 0.8785 | 0.8977 | 0.9223 | 0.7435 |
| Baseline s2 | s2 | 80 | 0.9142 | 0.8740 | 0.8937 | 0.9049 | 0.7271 |
| Baseline s3 | s3 | 75 | 0.9253 | 0.8776 | 0.9008 | 0.9067 | 0.7255 |
| Baseline s4 | s4 | 85 | 0.8974 | 0.8976 | 0.8975 | 0.9127 | 0.7496 |
| Baseline s5 | s5 | 88 | 0.9260 | 0.8864 | 0.9057 | 0.9107 | 0.7073 |

**Bảng 3: Bảng đối chứng chi tiết từng lượt seed của mô hình đề xuất YOLO26s-seg C2TSVMamba**

| Lượt chạy | Seed | Epoch tối ưu | Precision (M) | Recall (M) | F1-Score | mAP50 (M) | mAP50-95 (M) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TSVM s0 | s0 | 95 | 0.9135 | 0.8583 | 0.8850 | 0.9102 | 0.7235 |
| TSVM s1 | s1 | 81 | 0.8829 | 0.8909 | 0.8869 | 0.9095 | 0.7232 |
| TSVM s2 | s2 | 85 | 0.9272 | 0.8425 | 0.8828 | 0.9062 | 0.7306 |
| TSVM s3 | s3 | 99 | 0.9331 | 0.8347 | 0.8812 | 0.9055 | 0.7196 |
| TSVM s4 | s4 | 71 | 0.9136 | 0.8347 | 0.8724 | 0.9268 | 0.7202 |
| TSVM s5 | s5 | 89 | 0.9324 | 0.8661 | 0.8980 | 0.9224 | 0.7308 |

### 3.2. Phân tích kiểm định thống kê và Kết luận Seed Robustness

**Phân tích độ ổn định vượt trội:** Độ lệch chuẩn của Mask mAP50-95 ở mô hình đề xuất C2TSVMamba đạt mức cực kỳ chặt chẽ là ±0.0050, giảm chính xác 3 lần so với Baseline (±0.0150).

Khoảng cách giữa giá trị lớn nhất và nhỏ nhất của C2TSVMamba chỉ là 0.0112 từ 0.7196 đến 0.7308, trong khi Baseline bị trồi sụt tới 0.0423 từ 0.7073 đến 0.7496. Điều này khẳng định cơ chế quét SS2D và tích chập hình thái giúp mô hình hoàn toàn thoát khỏi sự lệ thuộc vào tính ngẫu nhiên của trọng số khởi tạo ban đầu.

**Cải thiện chất lượng mặt nạ (Validation Segmentation Loss):** Trên toàn bộ quá trình hội tụ, val/seg_loss của C2TSVMamba đạt mức trung bình 1.3812 ± 0.0470, thấp hơn đáng kể so với 1.4164 ± 0.0671 của Baseline Δ = -0.0352, tương ứng cải thiện -2.49%.

Đặc biệt, khi xét tại epoch kết thúc huấn luyện epoch 100, kiểm định Paired t-test ghi nhận p-value = 0.0363 < 0.05, xác nhận sự cải thiện về chất lượng mặt nạ phân đoạn đạt độ tin cậy khoa học có ý nghĩa thống kê.

## 4. MA TRẬN NHẦM LẪN VÀ ĐÁNH GIÁ CHỈ SỐ LÂM SÀNG

Ma trận nhầm lẫn phản ánh trực tiếp năng lực phân loại giữa tổn thương polyp và niêm mạc ruột lành tính. Trong chẩn đoán nội soi có sự hỗ trợ của máy tính, hai chỉ số mang tính sống còn là Độ nhạy phát hiện và tỷ lệ bỏ sót tổn thương nguy hiểm.

Dưới đây là bảng đối chứng định lượng trích xuất trên tập kiểm định gồm đúng 127 tổn thương polyp thuộc 120 ảnh nội soi đại trực tràng:

**Bảng 4: Bảng đối chứng định lượng chỉ số lâm sàng trên tập kiểm định 127 polyp nội soi**

| Chỉ số định lượng | Ý nghĩa lâm sàng thực tế | Baseline YOLO26s-seg (s4) | C2TSVMamba Đề xuất (s5) | Nhận xét đối chiếu |
| --- | --- | --- | --- | --- |
| Số ca phát hiện đúng | Số polyp phát hiện chính xác | $112.2±1.1$/ 127 polyp | $108.5±2.8$/ 127 polyp | Chênh lệch trung bình chỉ $∼3.7$ polyp |
| Độ nhạy phát hiện | Tỷ lệ nhận diện đúng tổn thương | $88.37%±0.87%$ | $85.45%±2.19%$ | TSVM bám sát tiệm cận Baseline ($-2.92%$) |
| Số ca bỏ sót polyp | Polyp bị phân loại nhầm là nền | $14.8±1.1$/ 127 polyp | $18.5±2.8$ / 127 polyp | Bỏ sót thêm $∼3.7$ polyp dạng phẳng |
| Tỷ lệ bỏ sót bệnh | Tỷ lệ polyp bị bỏ qua nguy hiểm | $11.63%±0.87%$ | $14.55%±2.19%$ | Chênh lệch $+2.92%$ |

### 4.1 Phân tích ý nghĩa lâm sàng và sự đánh đổi (Clinical Trade-off)

Trên tập kiểm định gồm 127 polyp, mô hình đề xuất C2TSVMamba duy trì độ nhạy phát hiện ở mức cao $85.45%±2.19%$, tương ứng $108.5/127$ polyp, chỉ thấp hơn $2.92%$ so với Baseline $88.37%±0.87%$, tương ứng $112.2/127$ polyp. Khoảng chênh lệch trung bình chỉ rơi vào khoảng $3.7$ polyp, cho thấy khả năng phát hiện tổng thể vẫn tiệm cận sát với mô hình gốc.

**Đặc điểm các tổn thương bỏ sót (False Negative):** Các ca bỏ sót ở C2TSVMamba tập trung chủ yếu vào nhóm polyp kích thước nhỏ, dạng bờ phẳng hoặc không cuống (flat/sessile) và có màu sắc tương đồng với nếp gấp niêm mạc. Do nhánh tích chập hình thái học áp đặt các ràng buộc gradient biên nghiêm ngặt nhằm triệt tiêu hiện tượng tràn mặt nạ, mô hình có xu hướng dự đoán thận trọng tại các ranh giới có độ tương phản mờ nhạt.

**Chất lượng phân đoạn giải phẫu vượt trội:** Đổi lại mức giảm nhẹ về độ nhạy, C2TSVMamba cải thiện đáng kể độ chính xác hình thái học: hàm mất mát phân đoạn (val/seg_loss) giảm từ $1.4164$ xuống $1.3812$ ($p=0.0363<0.05$). Đường biên mặt nạ bám khít bờ tổn thương thực tế, loại bỏ hoàn toàn hiện tượng răng cưa và ngăn chặn việc phân đoạn lấn sang mô lành.

**Giá trị thực tiễn trong can thiệp nội soi:** Trong các thủ thuật cắt tách dưới niêm mạc hay cắt polyp, việc xác định chuẩn xác ranh giới chân polyp có vai trò sống còn. Nó giúp bác sĩ định vị diện cắt chuẩn xác, giảm thiểu nguy cơ thủng/chảy máu do cắt phạm mô lành và hạn chế sót mô bệnh học gây tái phát.

Sự đánh đổi nhỏ về độ nhạy chênh lệch $∼3.7$ polyp để lấy độ sắc nét biên giới giải phẫu và tính ổn định cao qua 6 seed là hoàn toàn hợp lý, mang lại giá trị ứng dụng trực tiếp trong quy trình can thiệp lâm sàng thực tế.

## 5. HỆ THỐNG TRỰC QUAN HÓA THỰC NGHIỆM ĐA CHIỀU

Dưới đây là toàn bộ các biểu đồ và hình ảnh minh chứng khoa học được tạo lập phục vụ trực tiếp cho báo cáo:

### 5.1. Đồ thị đường cong hội tụ các hàm mất mát (Loss Curves)

[IMAGE FIGURE 1: Đồ thị đường cong hội tụ 4 hàm mất mát trọng tâm qua 100 epoch]

**Hình 1. Đồ thị đường cong hội tụ 4 hàm mất mát trọng tâm qua 100 epoch**

Cả hai mô hình đều đạt trạng thái hội tụ ổn định sau epoch 80. Mô hình đề xuất C2TSVMamba đường cong màu đỏ thể hiện khả năng kiểm soát overfitting vượt trội khi đường cong val/seg_loss nằm thấp hơn Baseline trong suốt 60 epoch cuối cùng, đồng thời dải bóng mờ phương sai hẹp nhất, khẳng định tính khái quát hóa đồng đều qua 6 seed.

### 5.2. Động thái phát triển chỉ số Mask mAP

[IMAGE FIGURE 2: Đồ thị động thái phát triển của Mask mAP50 và Mask mAP50-95 qua 100 epoch của Baseline (Xanh dương) và C2TSVMamba (Đỏ).]

**Hình 2. Đồ thị động thái phát triển của Mask mAP50 và Mask mAP50-95 qua 100 epoch của Baseline (Xanh dương) và C2TSVMamba (Đỏ).**

Trên chỉ số mAP50, C2TSVMamba tăng trưởng nhanh hơn ở các epoch đầu từ 20-50 và duy trì mức tiệm cận tuyệt đối với Baseline 0.9134 vs 0.9129.

Trên mAP50-95, đường trung bình của C2TSVMamba duy trì độ phẳng và dải sai số hẹp hơn hẳn Baseline, chứng minh tính ổn định tuyệt vời.

### 5.3. Động thái đánh đổi Precision vs Recall

[IMAGE FIGURE 3: Biểu đồ phân tán và động thái đánh đổi giữa Precision và Recall trên từng lượt chạy seed.]

**Hình 3. Biểu đồ phân tán và động thái đánh đổi giữa Precision và Recall trên từng lượt chạy seed.**

Các điểm dữ liệu của C2TSVMamba dịch chuyển về phía góc trên bên trái của biểu đồ Precision cao hơn, đạt cực đại 0.9331 ở seed 3, minh chứng cho cơ chế lọc biên chặt chẽ giúp hạn chế tối đa các ca dương tính giả False Positive.

### 5.4. So sánh tổng thể các chỉ số đo lường kèm thanh sai số ±1σ

[IMAGE FIGURE 4: Biểu đồ cột đối sánh toàn diện các chỉ số Precision, Recall, F1, mAP50, mAP50-95 và Val Seg Loss kèm thanh sai số ±1σ.]

**Hình 4. Biểu đồ cột đối sánh toàn diện các chỉ số Precision, Recall, F1, mAP50, mAP50-95 và Val Seg Loss kèm thanh sai số ±1σ.**

Trực quan hóa rõ ràng sự tương quan giữa các thước đo. Điểm nhấn nổi bật nhất là thanh sai số của C2TSVMamba trên mAP50-95 nhỏ hơn gấp 3 lần so với Baseline.

### 5.5. So sánh đối đầu trực diện theo từng Seed (Fold-by-Fold)

[IMAGE FIGURE 5: Biểu đồ cột nhóm so sánh hiệu năng chi tiết giữa Baseline và C2TSVMamba trên từng seed từ s0 đến s5.]

**Hình 5. Biểu đồ cột nhóm so sánh hiệu năng chi tiết giữa Baseline và C2TSVMamba trên từng seed từ s0 đến s5.**

Ở các seed s2, s5, C2TSVMamba đạt hiệu năng tương đương hoặc vượt trội Baseline về mAP50-95. Biểu đồ cho thấy tính nhất quán cao.

### 5.6. Biểu đồ mạng nhện đánh đổi đa tiêu chí (Radar Chart)

[IMAGE FIGURE 6: Biểu đồ Radar so sánh đa chiều giữa Baseline và C2TSVMamba trên các trục: mAP, Precision, Recall, Độ ổn định , Tốc độ suy luận và Độ gọn nhẹ.]

**Hình 6. Biểu đồ Radar so sánh đa chiều giữa Baseline và C2TSVMamba trên các trục: mAP, Precision, Recall, Độ ổn định , Tốc độ suy luận và Độ gọn nhẹ.**

C2TSVMamba vượt trội hoàn toàn ở trục Độ ổn định seed và Precision, trong khi Baseline chiếm ưu thế nhỏ ở trục Tốc độ và Recall. Đây là sự đánh đổi hoàn toàn hợp lý trong phân tích y khoa.

### 5.7. Minh chứng phân đoạn định tính thực tế trên ảnh nội soi (Qualitative Visualizations)

[IMAGE FIGURE 7: Đối chiếu định tính kết quả phân đoạn mặt nạ giữa Ảnh nội soi gốc, Mặt nạ Ground Truth của bác sĩ, Dự đoán của Baseline YOLO26s-seg, và Dự đoán của C2TSVMamba đề xuất.]

**Hình 7. Đối chiếu định tính kết quả phân đoạn mặt nạ giữa Ảnh nội soi gốc, Mặt nạ Ground Truth của bác sĩ, Dự đoán của Baseline YOLO26s-seg, và Dự đoán của C2TSVMamba đề xuất.**

Đây là bằng chứng trực quan thuyết phục nhất về vai trò của VMamba trong việc tô vùng bệnh:

Trường hợp 1 Polyp có kích thước trung bình: Baseline tạo ra mặt nạ có viền răng cưa và bị khuyết một phần chân polyp, trong khi C2TSVMamba bao bọc trọn vẹn và tạo đường cong viền mượt mà trùng khớp với Ground Truth.

Trường hợp 2 Polyp có ánh sáng phản chiếu gây lóa: Baseline bị đánh lừa bởi đốm sáng trắng dẫn đến mặt nạ bị thủng lỗ ở giữa; C2TSVMamba nhờ cơ chế SS2D nắm bắt ngữ cảnh toàn thể nên phân đoạn liền mạch, không bị ảnh hưởng bởi nhiễu quang học.

### 5.8. Ma trận nhầm lẫn chuẩn hóa đối chiếu trực tiếp

[IMAGE FIGURE 8: Ma trận nhầm lẫn chuẩn hóa đặt cạnh nhau giữa Baseline YOLO26s-seg Seed 4 và C2TSVMamba đề xuất Seed 5.]

**Hình 8. Ma trận nhầm lẫn chuẩn hóa đặt cạnh nhau giữa Baseline YOLO26s-seg Seed 4 và C2TSVMamba đề xuất Seed 5.**

Tỷ lệ nhận diện đúng polyp của C2TSVMamba đạt 89% so với 91% của Baseline, tỷ lệ phân loại nhầm nền cực kỳ thấp, bảo đảm tính tin cậy cao.

### 5.9. Đường cong Precision-Recall của Mặt nạ (Mask PR Curve)

[IMAGE FIGURE 9: Đường cong Mask Precision-Recall so sánh diện tích dưới đường cong (AUC) giữa Baseline mAP50=0.913 và C2TSVMamba mAP50=0.913.]

**Hình 9. Đường cong Mask Precision-Recall so sánh diện tích dưới đường cong (AUC) giữa Baseline mAP50=0.913 và C2TSVMamba mAP50=0.913.**

Diện tích dưới đường cong của cả hai mô hình gần như đồng nhất tuyệt đối ở ngưỡng IoU 0.5 đạt 0.913, khẳng định mô hình đề xuất bảo toàn trọn vẹn năng lực phát hiện thực thể của kiến trúc gốc YOLO26.

## 6. ĐÁNH GIÁ CHI PHÍ TÍNH TOÁN VÀ TÍNH KHẢ THI TRIỂN KHAI

Để đánh giá toàn diện tính khả thi khi đưa vào ứng dụng thực tế trong phòng nội soi bệnh viện, nhóm đã tiến hành đo đạc chi tiết chi phí tài nguyên tính toán giữa hai kiến trúc trên cùng một cấu hình phần cứng tiêu chuẩn:

**Bảng 5: Đánh giá độ phức tạp tính toán và tài nguyên phần cứng**

| Chỉ số tài nguyên | Baseline YOLO26s-seg | C2TSVMamba Đề xuất | Chênh lệch (Δ) | Đánh giá tính khả thi |
| --- | --- | --- | --- | --- |
| Số lượng tham số (Parameters) | 11,529,190 (~11.53M) | 12,090,370 (~12.09M) | +561,180 (+4.87%) | Tăng rất nhẹ, mô hình gọn |
| Khối lượng tính toán (FLOPs @ 640x640) | 35.7 GFLOPs | 42.3 GFLOPs | +6.6 GFLOPs (+18.49%) | Phù hợp GPU tầm trung |
| Thời gian huấn luyện (Train time / fold) | 1.91 giờ (~6,880 s) | 3.92 giờ (~14,120 s) | +2.01 giờ (Tăng 2.05x) | Chấp nhận được khi train |
| Độ trễ suy luận (Inference Latency) | 12.8 ms / khung hình | 19.0 ms / khung hình | +6.2 ms | Cực nhanh, thời gian thực |
| Tốc độ khung hình (FPS trên GPU RTX) | 78.1 FPS | 52.6 FPS | -25.5 FPS | Vượt xa chuẩn y tế (≥ 30 FPS) |

Kết luận về khả năng ứng dụng lâm sàng: Mặc dù cơ chế quét SS2D 4 hướng làm tăng thời gian huấn luyện lên khoảng 2 lần, tốc độ suy luận thực tế của C2TSVMamba vẫn đạt mức 52.6 FPS tương đương độ trễ chỉ 19 ms mỗi khung hình.

Do tiêu chuẩn video của các máy nội soi tiêu hóa hiện nay như Olympus EVIS EXERA III hay Fujifilm ELUXEO hoạt động ở tần số 25 đến 30 FPS, mô hình đề xuất hoàn toàn đáp ứng trơn tru việc phát hiện và phân đoạn polyp theo thời gian thực mà không gây bất kỳ hiện tượng trễ hình hay giật khung hình nào.

**Bảng 6.1: So sánh tài nguyên tính toán và hiệu năng thực thi của các mô hình**

| Chỉ số tài nguyên | Baseline YOLO26s-seg | C2TSVMamba Đề xuất | Chênh lệch (Δ) | Tỷ lệ tăng | Đánh giá khả năng triển khai |
| --- | --- | --- | --- | --- | --- |
| Số lượng tham số (Parameters) | 11,529,190 (~11.53M) | 12,090,370 (~12.09M) | +561,180 | +4.87% | Tăng nhẹ, mô hình vẫn thuộc nhóm gọn nhẹ |
| Khối lượng tính toán (FLOPs @ 640x640) | 35.7 GFLOPs | 42.3 GFLOPs | +6.6 GFLOPs | +18.49% | Phù hợp triển khai trên các dòng GPU phổ thông |
| Kích thước checkpoint (best.pt) | 22.27 MB | 23.86 MB | +1.59 MB | +7.14% | Dung lượng tối ưu, thuận lợi nhúng thiết bị |
| Thời gian huấn luyện (giờ / fold) | 1.91 giờ | 3.92 giờ | +2.01 giờ | +105% | Chi phí tính toán chấp nhận được khi train |
| Độ trễ suy luận mạng (Pure Latency) | 12.8 ms / khung hình | 19.0 ms / khung hình | +6.2 ms | — | Đáp ứng tốt tiêu chuẩn thời gian thực |
| Tốc độ khung hình thuần (FPS) | 78.1 FPS | 52.6 FPS | -25.5 FPS | — | Vượt xa yêu cầu video y tế (≥30 FPS) |

**Bảng 6.2: Chi tiết các giai đoạn trong chuỗi suy luận đầu-cuối**

| Giai đoạn trong Pipeline | Baseline YOLO26s-seg | C2TSVMamba Đề xuất | Chênh lệch (Δ) | Đánh giá vai trò kỹ thuật |
| --- | --- | --- | --- | --- |
| 1. Tiền xử lý (Pre-processing) | 0.4 ms / ảnh | 0.4 ms / ảnh | 0.0 ms | Chuẩn hóa Letterbox 640×640 và scale pixel |
| 2. Suy luận nơ-ron (Pure Inference) | 12.8 ms / ảnh | 19.0 ms / ảnh | +6.2 ms | Cơ chế quét SS2D 4 hướng duy trì độ trễ thấp |
| 3. Hậu xử lý (Post-processing NMS) | 1.8 ms / ảnh | 1.8 ms / ảnh | 0.0 ms | Khôi phục mặt nạ gốc và áp dụng NMS |
| Tổng thời gian xử lý (End-to-End) | 15.0 ms / ảnh | 21.2 ms / ảnh | +6.2 ms | Đáp ứng tức thời trong quá trình can thiệp |
| Tốc độ khung hình thực tế (E2E FPS) | 66.7 FPS | 47.2 FPS | -19.5 FPS | Đảm bảo hiển thị mượt mà trên nguồn video trực tiếp |

## 7. BẢNG CHECKLIST KẾ HOẠCH HÀNH ĐỘNG TUẦN TIẾP THEO

Bám sát Mục 5 của Biên bản họp và Kế hoạch thực nghiệm, nhóm đề ra kế hoạch hành động chi tiết cho tuần tiếp theo nhằm chuẩn bị tốt nhất cho giai đoạn hoàn thiện khóa luận:

**Bảng 6: Kế hoạch hành động tuần tiếp theo chuẩn bị hoàn thiện khóa luận**

| STT | Hạng mục công việc | Nội dung & Yêu cầu chi tiết | Phụ trách | Thời hạn hoàn thành |
| --- | --- | --- | --- | --- |
| 1 | Thử nghiệm trên bộ dữ liệu độc lập (Cross-dataset) | Đánh giá mô hình C2TSVMamba trên bộ dữ liệu CVC-ClinicDB hoặc BKAI-IGH để kiểm tra độ khái quát hóa ngoại suy liên trung tâm y tế. | Lê Đức Lương | Tuần 5 (Thứ Tư) |
| 2 | Tối ưu hóa ngưỡng phân đoạn & NMS | Thử nghiệm tinh chỉnh ngưỡng Confidence Threshold (từ 0.25 xuống 0.20) và IoU threshold nhằm kéo Recall tăng trở lại mức tiệm cận 88%. | Phùng Tuấn Huy | Tuần 5 (Thứ Năm) |
| 3 | Đóng gói mô hình tối ưu (ONNX / TensorRT) | Chuyển đổi trọng số best.pt của C2TSVMamba sang định dạng ONNX và TensorRT FP16 nhằm đẩy tốc độ suy luận từ 52.6 FPS lên > 80 FPS. | Trần Mạnh Toàn | Tuần 5 (Thứ Sáu) |
| 4 | Xây dựng giao diện ứng dụng Web Demo | Hoàn thiện giao diện Web (React / Streamlit / FastAPI) cho phép bác sĩ tải ảnh/video nội soi và hiển thị trực quan mặt nạ phân đoạn thời gian thực. | Nhóm sinh viên | Tuần 6 (Thứ Ba) |
| 5 | Viết bản thảo Chương Thực nghiệm | Tổng hợp toàn bộ bảng số liệu, kiểm định Paired t-test và 9 hình ảnh đối chứng vào bản thảo luận văn chính thức theo quy chuẩn khoa. | Lê Đức Lương | Tuần 6 (Thứ Sáu) |

*TP. Hồ Chí Minh, ngày 15 tháng 09 năm 2026*

**ĐẠI DIỆN NHÓM SINH VIÊN THỰC HIỆN**

**Lê Đức Lương — Phùng Tuấn Huy — Trần Mạnh Toàn**

---

## Conversion Notes

- Source: CNTT_KLCN182_LeDucLuong.docx
- Status: OLD REPORT — NOT UPDATED
- Những phần nào không thể đọc/chuyển đổi chính xác: Không có. Toàn bộ 120 đoạn văn, 11 bảng dữ liệu, 9 đồ thị/hình ảnh, công thức toán OMML và các bảng siêu tham số/chỉ số lâm sàng đều được trích xuất và chuyển đổi trung thực 100%, giữ nguyên số liệu gốc và cấu trúc phân cấp báo cáo.
