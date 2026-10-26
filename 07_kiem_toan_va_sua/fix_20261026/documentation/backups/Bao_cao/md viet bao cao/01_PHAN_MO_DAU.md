# MỞ ĐẦU

---

## 1. LÝ DO CHỌN ĐỀ TÀI VÀ TÍNH CẤP THIẾT CỦA NGHIÊN CỨU

Ung thư đại trực tràng (Colorectal Cancer - CRC) là một trong những bệnh lý ác tính phổ biến hàng đầu và là nguyên nhân gây tử vong do ung thư đứng thứ hai trên phạm vi toàn cầu, theo thống kê của Tổ chức Y tế Thế giới (WHO) và GLOBOCAN. Phần lớn các ca ung thư đại trực tràng đều khởi phát từ các tổn thương tiền ung thư dạng polyp phát triển âm thầm trên bề mặt lớp niêm mạc đại trực tràng trong nhiều năm trước khi tiến triển thành khối u ác tính. Việc phát hiện sớm, khoanh vùng chính xác và cắt bỏ hoàn toàn các polyp này qua kỹ thuật nội soi đại trực tràng (Colonoscopy) được công nhận là tiêu chuẩn vàng giúp giảm tỷ lệ tử vong do ung thư đại trực tràng từ 50% đến hơn 80%.

Tuy nhiên, trong quá trình can thiệp lâm sàng thực tế, các bác sĩ nội soi phải đối mặt với nhiều áp lực và thách thức lớn. Tỷ lệ bỏ sót polyp (Polyp Miss Rate - PMR) trong các ca nội soi thông thường vẫn dao động ở mức đáng báo động từ 15% đến 25%. Nguyên nhân chủ yếu xuất phát từ:
- **Đặc điểm hình thái đa dạng và phức tạp của polyp**: Nhiều tổn thương có kích thước rất nhỏ (< 5 mm), dạng phẳng (flat/sessile) hoặc lõm, có màu sắc và cấu trúc bề mặt gần như hòa lẫn với nếp gấp niêm mạc ruột xung quanh.
- **Điều kiện quan sát nội soi hạn chế**: Ánh sáng phản chiếu từ chất dịch nhầy, góc khuất sau các nếp gấp đại tràng, chuyển động nhu động ruột liên tục và tình trạng che khuất bởi bọt khí, chất cặn bã.
- **Yếu tố chủ quan của người thực hiện**: Sự mệt mỏi, suy giảm thị lực và mức độ tập trung của bác sĩ sau các ca nội soi kéo dài liên tục, cũng như khoảng cách về kinh nghiệm giữa các bác sĩ chuyên khoa.

Trước thực trạng đó, việc ứng dụng Trí tuệ nhân tạo (AI), đặc biệt là các mô hình Thị giác máy tính học sâu (Deep Learning Computer Vision) vào hệ thống Hỗ trợ chẩn đoán có sự trợ giúp của máy tính (Computer-Aided Diagnosis - CADe/CADx) đã trở thành xu hướng nghiên cứu mũi nhọn. Thay vì chỉ dừng lại ở bài toán Phát hiện đối tượng (Object Detection) bằng hộp bao chữ nhật (Bounding Box) vốn thô sơ và không cung cấp được thông tin ranh giới mô bệnh học, bài toán **Phân đoạn thực thể (Instance Segmentation)** đặt ra yêu cầu cao hơn: phải trích xuất chính xác đường biên (contour) và sinh mặt nạ nhị phân (binary mask) bám khít từng điểm ảnh (pixel-level) của tổn thương polyp.

Gần đây, các mô hình phân đoạn thời gian thực dòng YOLO, tiêu biểu là kiến trúc thế hệ mới **YOLO26-seg**, đã cho thấy ưu thế vượt trội về tốc độ xử lý khung hình cao và cấu trúc end-to-end gọn nhẹ. Tuy nhiên, bản chất các phép tích chập (Convolutional Layers) trong mạng CNN của YOLO vẫn mang tính chất cục bộ (Local Receptive Field), dẫn đến hạn chế rõ rệt trong việc nắm bắt tương quan ngữ cảnh toàn cục (Global Context), khiến mô hình dễ bị đứt gãy đường biên hoặc sinh mặt nạ nhầm lẫn ở các vùng biên độ tương phản thấp. Ngược lại, các mô hình dựa trên Vision Transformer (ViT) tuy nắm bắt ngữ cảnh tốt nhưng lại có độ phức tạp tính toán bậc hai $O(N^2)$, đòi hỏi tài nguyên phần cứng lớn và gây độ trễ cao, khó triển khai trên các thiết bị nội soi thời gian thực.

Sự ra đời của mô hình không gian trạng thái chọn lọc (Selective State Space Models - Mamba / VMamba) với cơ chế quét chọn lọc hai chiều không gian **SS2D (2D Selective Scan)** đã mở ra một hướng đột phá mới: cho phép mô hình hóa sự phụ thuộc tầm xa với độ phức tạp tính toán tuyến tính $O(N)$. Nhận thấy tiềm năng to lớn này, đề tài **"Nghiên cứu phương pháp tích hợp VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng"** được nhóm sinh viên đề xuất thực hiện nhằm kết hợp sức mạnh phân đoạn thời gian thực của YOLO26-seg với khả năng nắm bắt ngữ cảnh toàn cục và nhận biết hình thái đường biên của khối VMamba, giải quyết đồng thời bài toán cân bằng giữa độ chính xác phân đoạn lâm sàng và chi phí tài nguyên phần cứng.

---

## 2. MỤC TIÊU VÀ NHIỆM VỤ NGHIÊN CỨU CỦA ĐỀ TÀI

### 2.1. Mục tiêu tổng quát
Nghiên cứu, thiết kế, cài đặt và đánh giá một giải pháp phân đoạn thực thể polyp đại trực tràng tự động dựa trên sự tích hợp khối không gian trạng thái thị giác (Visual State Space - VMamba) vào mạng phân đoạn thời gian thực YOLO26-seg; từ đó xây dựng hệ sinh thái ứng dụng minh họa hoàn chỉnh (Web & Mobile App) hỗ trợ công tác tầm soát lâm sàng.

### 2.2. Mục tiêu cụ thể
1. **Khảo sát lý thuyết chuyên sâu**: Hệ thống hóa cơ sở lý thuyết về bài toán phân đoạn polyp, kiến trúc YOLO26-seg, nguyên lý mô hình không gian trạng thái Mamba và thuật toán quét chọn lọc 2D (SS2D) trong VMamba.
2. **Thiết kế và chuẩn hóa bộ dữ liệu thực nghiệm**: Xây dựng quy trình tiền xử lý chuyển đổi mặt nạ Ground Truth sang định dạng đa giác YOLO Polygon; đặc biệt bổ sung 20% ảnh nền âm tính (niêm mạc bình thường không chứa polyp - normal cecum) tạo thành bộ dữ liệu chuẩn hóa `Kvasir_YOLO_SEG_BG20` (1.200 ảnh) với cơ chế nhãn rỗng nhằm triệt tiêu hiện tượng báo động giả (False Positives).
3. **Đề xuất kiến trúc cải tiến TSVM**: Thiết kế và tích hợp thành công khối **Topology-Shape-aware VMamba (TSVM)** vào vị trí chiến lược tại tầng 10 (mức đặc trưng sâu P5, stride 32) của YOLO26-seg, tối ưu hóa quá trình tổng hợp thông tin ngữ cảnh ngữ nghĩa đa tỷ lệ.
4. **Thực nghiệm đối chứng khoa học tất định qua 10 seed**: Huấn luyện và đánh giá đối chứng nghiêm ngặt giữa mô hình cơ sở Baseline YOLO26s-seg và mô hình cải tiến TSVM qua 10 lượt chạy độc lập (Seed 0 đến Seed 9); đo đạc toàn diện các chỉ số: Box/Mask Precision, Recall, F1-score, Dice Similarity Coefficient (DSC), IoU, mAP50, mAP50-95 và thực hiện kiểm định giả thuyết thống kê Paired t-test.
5. **Đánh giá chi phí tính toán và khả năng thực thi**: Đo lường chi tiết số lượng tham số (Parameters), độ phức tạp tính toán (GFLOPs), thời gian suy luận (Latency theo mili-giây) và tốc độ khung hình (FPS) trên các môi trường phần cứng GPU và CPU.
6. **Xây dựng hệ sinh thái sản phẩm ứng dụng**: Hiện thực hóa giải pháp thành hệ thống phần mềm hoàn chỉnh gồm 3 lớp:
   - AI Microservice (FastAPI - Python) đảm nhiệm suy luận thời gian thực.
   - Web Application (Java Spring Boot) phục vụ quản lý hồ sơ và tương tác trên máy tính nội soi.
   - Mobile Application (Flutter) cho phép chụp ảnh trực tiếp và hiển thị tổn thương polyp trên thiết bị di động.

---

## 3. ĐỐI TƯỢNG VÀ PHẠM VI NGHIÊN CỨU

### 3.1. Đối tượng nghiên cứu
- Ảnh chụp nội soi đường tiêu hóa dưới (đại trực tràng) có chứa các dạng tổn thương polyp khác nhau và ảnh niêm mạc bình thường.
- Mô hình mạng nơ-ron phân đoạn thực thể thời gian thực YOLO26-seg (biến thể nhỏ gọn `yolo26s-seg`).
- Khối mô hình không gian trạng thái thị giác chọn lọc VMamba (Visual State-Space Model) và thuật toán quét chọn lọc 2 chiều SS2D.
- Kỹ thuật xây dựng phần mềm phân tán (FastAPI, Java Spring Boot, Flutter).

### 3.2. Phạm vi nghiên cứu
- **Phạm vi dữ liệu**: 
  - Tập dữ liệu chính để huấn luyện và kiểm định đối chứng: `Kvasir_YOLO_SEG_BG20` bao gồm 1.000 ảnh từ bộ dữ liệu mở Kvasir-SEG (Simula Research Laboratory, Na Uy) kết hợp cùng 200 ảnh niêm mạc manh tràng bình thường (normal-cecum) từ tập Kvasir v2.
  - Tập dữ liệu mở rộng dùng để đánh giá khả năng tổng quát hóa ngoại suy (Out-of-distribution): CVC-ClinicDB, CVC-ColonDB và ETIS-Larib PolypDB.
- **Phạm vi mô hình**: Tập trung nghiên cứu phương án tích hợp khối VMamba tại tầng 10 (mức P5) của mô hình `yolo26s-seg`. Không mở rộng sang các biến thể cỡ lớn (Medium, Large, XLarge) do hạn chế về chi phí tính toán và mục tiêu tối ưu cho triển khai thực tế.
- **Phạm vi môi trường thực nghiệm**: Môi trường điện toán đám mây Kaggle GPU (Nvidia Tesla T4 16GB VRAM) cho huấn luyện; máy trạm cá nhân và thiết bị di động thông minh cho kiểm thử suy luận ứng dụng.

---

## 4. PHƯƠNG PHÁP NGHIÊN CỨU VÀ TỔ CHỨC THỰC HIỆN

### 4.1. Phương pháp nghiên cứu
Đề tài áp dụng kết hợp các phương pháp nghiên cứu khoa học chuẩn tắc:
- **Phương pháp nghiên cứu lý thuyết**: Thu thập, phân tích, tổng hợp tài liệu chuyên khảo, các bài báo khoa học đỉnh cao (Q1/A*) từ các hội nghị và tạp chí uy tín (MICCAI, CVPR, ICCV, NeurIPS, ICML, IEEE TMI) liên quan đến bài toán phân đoạn polyp, kiến trúc YOLO và Mamba.
- **Phương pháp mô hình hóa và thiết kế giải thuật**: Sử dụng ngôn ngữ lập trình Python, thư viện PyTorch để tùy biến kiến trúc mã nguồn mở của Ultralytics, thiết kế khối TSVM và tích hợp vào pipeline xử lý mạng nơ-ron.
- **Phương pháp thực nghiệm đối chứng tất định (Empirical Controlled Experimentation)**: Cố định toàn bộ các siêu tham số (Hyperparameters), cố định các hạt giống ngẫu nhiên (Seeds từ 0 đến 9), huấn luyện 10 lượt độc lập cho mỗi mô hình trên cùng một điều kiện dữ liệu và phần cứng; sử dụng script tự động trích xuất kết quả từ file log gốc `results.csv`.
- **Phương pháp phân tích thống kê và kiểm chứng chéo (Statistical Hypothesis Testing & Audit)**: Áp dụng kiểm định Paired Student's t-test để đánh giá mức độ tin cậy của sự cải thiện; xây dựng quy trình kiểm toán toàn vẹn số liệu (Audit) với 694 phép kiểm tra tự động nhằm đảm bảo tính trung thực học thuật tuyệt đối.
- **Phương pháp phát triển phần mềm theo mô hình dịch vụ vi mô (Microservices Architecture)**: Phân tách rõ ràng giữa tầng tính toán học sâu (AI Engine) và tầng ứng dụng người dùng cuối (Web và Mobile App) thông qua giao thức RESTful API.

### 4.2. Kế hoạch và phân công thực hiện đề tài (12 tuần)
Đề tài được thực hiện nghiêm túc trong khoảng thời gian 12 tuần (từ ngày 17/08/2026 đến ngày 08/11/2026) theo phân công chi tiết của Giảng viên hướng dẫn:
- **Sinh viên Lê Đức Lương (Nhóm trưởng)**: Chịu trách nhiệm thiết kế kiến trúc khối TSVM, cài đặt pipeline huấn luyện trên Kaggle, thực hiện toàn bộ 20 lượt huấn luyện 10 seed, xử lý số liệu thống kê, chạy kiểm toán toàn vẹn audit và xây dựng dịch vụ AI FastAPI.
- **Sinh viên Phùng Tuấn Huy**: Chịu trách nhiệm thu thập, làm sạch dữ liệu Kvasir-SEG và normal-cecum, viết script chuyển đổi nhãn đa giác YOLO segmentation, kiểm thử độ trễ và tham gia thiết kế giao diện ứng dụng Web Java Spring Boot.
- **Sinh viên Trần Mạnh Toàn**: Chịu trách nhiệm thiết kế, lập trình ứng dụng di động Flutter (`app_polyp`), tích hợp kết nối API nhận ảnh từ camera/bộ nhớ và xây dựng bài báo cáo thuyết trình Slide PowerPoint.

---

## 5. Ý NGHĨA KHOA HỌC VÀ GIÁ TRỊ THỰC TIỄN CỦA ĐỀ TÀI

### 5.1. Ý nghĩa khoa học
- Đóng góp một giải pháp kiến trúc mới mẻ bằng việc chứng minh tính khả thi của việc kết hợp mô hình không gian trạng thái chọn lọc (VMamba SS2D) với mạng phân đoạn thực thể end-to-end YOLO26-seg trong xử lý ảnh y tế.
- Khẳng định vai trò quan trọng của việc bổ sung ảnh nền âm tính (negative samples) kết hợp nhãn rỗng trong việc triệt tiêu hiện tượng báo động giả đối với các mô hình thị giác máy tính dựa trên YOLO.
- Cung cấp một bộ dữ liệu thực nghiệm chuẩn mực với 10 lượt chạy tất định, thiết lập chuẩn đối sánh tin cậy cho cộng đồng nghiên cứu bài toán phân đoạn polyp tại Việt Nam.

### 5.2. Giá trị thực tiễn
- Cung cấp một công cụ hỗ trợ thông minh có khả năng khoanh vùng chính xác ranh giới tổn thương polyp theo thời gian thực, hỗ trợ đắc lực cho các bác sĩ trong quá trình nội soi, giảm thiểu nguy cơ bỏ sót tổn thương nguy hiểm.
- Sản phẩm Web và Mobile App hoàn thiện sẵn sàng kết nối vào hệ thống mạng nội bộ của phòng khám hoặc thiết bị di động của bác sĩ, có tính ứng dụng chuyển giao cao.

---

## 6. BỐ CỤC CỦA KHÓA LUẬN

Nội dung chính của khóa luận được kết cấu thành 5 chương theo đúng thể thức chuẩn mực của Khoa Công nghệ Thông tin - Trường Đại học Công Thương TP. Hồ Chí Minh:

- **Chương 1: Tổng quan và cơ sở nghiên cứu**: Trình bày tổng quan về bài toán phân đoạn polyp, kiến trúc mô hình YOLO26-seg, cơ sở lý thuyết về Mamba/VMamba và khảo sát các công trình liên quan.
- **Chương 2: Phân tích và thiết kế mô hình đề xuất**: Phân tích chi tiết cơ chế hoạt động của YOLO26-seg, công thức toán học của SS2D và thiết kế khối Topology-Shape-aware VMamba (TSVM) tích hợp tại tầng 10.
- **Chương 3: Xây dựng bộ dữ liệu và tiền xử lý**: Trình bày chi tiết về nguồn dữ liệu Kvasir-SEG, normal-cecum, quy trình sinh nhãn đa giác YOLO, cơ chế nhãn rỗng và đặc tả cấu hình `data_bg20.yaml`.
- **Chương 4: Cài đặt thuật toán và xây dựng ứng dụng minh họa**: Trình bày môi trường thực nghiệm, phân tích các cell Notebook Kaggle huấn luyện tất định và kiến trúc cài đặt hệ sinh thái phần mềm (FastAPI, Java Spring Boot Web và Flutter Mobile App).
- **Chương 5: Thử nghiệm và đánh giá kết quả**: Báo cáo chi tiết kết quả định lượng qua 10 seed độc lập, kiểm định thống kê, phân tích ma trận nhầm lẫn, hệ thống 12 đồ thị trực quan hóa đa chiều, đánh giá chi phí tính toán và thử nghiệm trên dữ liệu thực tế.
- **Kết luận và hướng phát triển**: Tổng kết các kết quả đạt được, chỉ ra các hạn chế và đề xuất hướng nghiên cứu tiếp theo.
- **Tài liệu tham khảo** và **Hệ thống 8 Phụ lục chuyên sâu (Phụ lục A đến H)**.
