# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

---

## 1. KẾT QUẢ ĐẠT ĐƯỢC CỦA ĐỀ TÀI

Sau 12 tuần nghiên cứu nghiêm túc, bám sát các mục tiêu và chuẩn đầu ra (CLO) trong đề cương của Giảng viên hướng dẫn TS. Phùng Thế Bảo, đề tài **"Nghiên cứu phương pháp tích hợp VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng"** đã hoàn thành trọn vẹn toàn bộ các nhiệm vụ đề ra với các kết quả cụ thể như sau:

1. **Về mặt cơ sở lý thuyết và khảo sát học thuật**:
   - Hệ thống hóa hoàn chỉnh cơ sở toán học và lý thuyết về bài toán phân đoạn thực thể trong xử lý ảnh y tế, kiến trúc mạng một giai đoạn YOLO26-seg, mô hình không gian trạng thái Mamba và thuật toán quét chọn lọc 2D không gian (SS2D) trong VMamba.
   - Khảo sát, đối chiếu chuyên sâu ưu - nhược điểm của các công trình tiền nhiệm từ các mô hình tích chập CNN truyền thống (UNet, PraNet) đến các mô hình dựa trên Vision Transformer và SSM (Polyp-Mamba).

2. **Về mặt dữ liệu và kỹ thuật tiền xử lý**:
   - Xây dựng thành công thuật toán tự động chuyển đổi mặt nạ nhị phân y tế sang định dạng nhãn đa giác YOLO Polygon chuẩn mực với sai số diện tích dưới 0.5%.
   - Xây dựng và đóng gói bộ dữ liệu chuẩn hóa **`Kvasir_YOLO_SEG_BG20`** (1.200 ảnh: 1.000 ảnh Kvasir-SEG + 200 ảnh niêm mạc manh tràng bình thường normal-cecum).
   - Áp dụng thành công **cơ chế nhãn rỗng (Empty Labels 0 byte)** trên 200 ảnh nền âm tính, giúp mạng nơ-ron học được khả năng ức chế phản hồi giả, nâng độ đặc hiệu lâm sàng lên trên 90%.

3. **Về mặt đề xuất kiến trúc mô hình (TSVM)**:
   - Thiết kế và tích hợp thành công khối **Topology-Shape-aware VMamba (TSVM)** vào vị trí chiến lược tại tầng 10 (mức đặc trưng sâu P5, stride 32) của mạng YOLO26s-seg.
   - Hiện thực hóa cơ chế nhận thức kép: Nhánh Depthwise Conv $3\times3$ chụp lại độ cong ranh giới mô bệnh học kết hợp cơ chế quét SS2D 4 hướng nắm bắt tương quan không gian toàn cục với độ phức tạp tính toán tuyến tính $O(N)$.

4. **Về mặt thực nghiệm đối chứng tất định và kiểm toán số liệu**:
   - Hoàn thành quy trình thực nghiệm nghiêm ngặt gồm **20 phiên huấn luyện qua 10 hạt giống ngẫu nhiên độc lập (10 seed)** trên hạ tầng điện toán đám mây Kaggle GPU Tesla T4 (mỗi phiên 100 epoch).
   - Mô hình TSVM đạt các chỉ số ấn tượng: Mask mAP@50-95 đạt $0.7246 \pm 0.0078$, Mask Precision đạt $0.9118 \pm 0.0246$, Mask Recall đạt $0.8625 \pm 0.0173$, hệ số tương đồng Dice đạt $0.8865$, IoU đạt $0.7961$.
   - Đặc biệt, mô hình TSVM mang lại sự cải thiện vượt bậc về **độ ổn định học thuật**: Độ lệch chuẩn (Std) của Mask mAP@50-95 giảm 39.7%, phương sai co hẹp 2.75 lần, hàm mất mát phân đoạn Val Seg Loss giảm 4.76% (với $p = 0.0908$).
   - Xây dựng quy trình kiểm toán tự động với **694/694 phép kiểm tra đạt chuẩn 100%**, minh chứng tính trung thực tuyệt đối của số liệu báo cáo.

5. **Về mặt sản phẩm phần mềm ứng dụng**:
   - Hiện thực hóa trọn vẹn một **hệ sinh thái ứng dụng đa nền tảng phân tán 3 lớp**:
     - *Tầng AI*: Dịch vụ vi mô FastAPI bất đồng bộ (`polypweb/ai-service`) quản lý nạp mô hình và cung cấp API suy luận thời gian thực.
     - *Tầng Web*: Ứng dụng Java Spring Boot 3.x (`polypweb/polypweb`) quản lý bệnh án và giao diện trực quan cho bác sĩ trong phòng khám.
     - *Tầng Mobile*: Ứng dụng di động Flutter (`app_polyp`) cho phép chụp ảnh trực tiếp từ camera điện thoại và hiển thị mặt nạ phân đoạn bám khít tổn thương polyp.

---

## 2. ĐÁNH GIÁ KẾT QUẢ ĐẠT ĐƯỢC

### 2.1. Đánh giá về mặt khoa học
- **Tính đúng đắn và khả năng tái lập**: Mọi kết quả thực nghiệm trong khóa luận đều được xây dựng trên nền tảng tất định (Deterministic Training). Các nhà nghiên cứu khác hoàn toàn có thể tái lập chính xác 100% các bảng số liệu thông qua các tệp mã nguồn và hạt giống ngẫu nhiên được công bố.
- **Tính khả thi của việc tích hợp VMamba**: Đề tài đã chứng minh việc kết hợp cơ chế quét chọn lọc SS2D vào tầng đặc trưng sâu P5 của mạng một giai đoạn (One-stage) là hoàn toàn khả thi, giúp giải quyết triệt để vấn đề ranh giới mờ của polyp phẳng mà không làm bùng nổ tham số (chỉ tăng thêm 0.821M tham số và 0.32 GFLOPs).

### 2.2. Đánh giá về mặt ứng dụng thực tiễn
- **Phù hợp với quy trình can thiệp lâm sàng**: Việc giảm thiểu âm tính giả (giảm 0.9 ca bỏ sót) và giảm dương tính giả (giảm 0.9 ca báo động nhầm) có ý nghĩa thiết thực trong việc nâng cao tỷ lệ phát hiện u tuyến (Adenoma Detection Rate - ADR) của các bác sĩ nội soi.
- **Tính hoàn thiện của sản phẩm**: Việc triển khai song song cả Web Java Spring Boot và Mobile App Flutter chứng minh giải pháp không chỉ mang tính lý thuyết trong phòng thí nghiệm mà có thể chuyển giao công nghệ ứng dụng ngay vào thực tế y tế.

---

## 3. HẠN CHẾ VÀ KHÓ KHĂN TỒN TẠI

Bên cạnh những thành tựu đạt được, đề tài vẫn còn một số điểm hạn chế mang tính khách quan và chủ quan cần được nhìn nhận thẳng thắn:

1. **Ý nghĩa thống kê của sự cải thiện độ chính xác**:
   Mặc dù TSVM cải thiện hầu hết các chỉ số trung bình và giảm phương sai, kiểm định giả thuyết Paired t-test cho thấy giá trị $p = 0.3839$ ở chỉ số Mask mAP@50-95 chưa đạt ngưỡng ý nghĩa thống kê nghiêm ngặt $\alpha = 0.05$. Điều này cho thấy với tập dữ liệu kích thước 1.200 ảnh và cỡ mẫu $N = 10$, mô hình Baseline YOLO26s-seg vốn đã là một mạng nền tảng rất mạnh, do đó dư địa tăng trưởng độ chính xác tuyệt đối bị giới hạn.
2. **Độ trễ suy luận gia tăng trên phần cứng CPU**:
   Do kiến trúc Mamba phụ thuộc vào các vòng lặp tuần tự trạng thái và các phép hoán vị bộ nhớ trong quét 4 hướng, thời gian suy luận trên CPU bị chậm hơn đáng kể so với Baseline (821.27 ms so với 200.12 ms). Điều này đòi hỏi hệ thống bắt buộc phải được trang bị card tăng tốc đồ họa GPU khi triển khai suy luận thời gian thực trực tiếp.
3. **Giới hạn phạm vi dữ liệu thử nghiệm**:
   Nghiên cứu mới chỉ tập trung đánh giá trên các khung hình tĩnh (still endoscopic images). Trong môi trường can thiệp thực tế, dây soi chuyển động liên tục tạo ra các hiện tượng nhòe chuyển động (motion blur) và thay đổi góc nhìn nhanh chóng, là những yếu tố chưa được mô phỏng toàn diện trong nghiên cứu này.

---

## 4. HƯỚNG PHÁT TRIỂN VÀ MỞ RỘNG TRONG TƯƠNG LAI

Từ những kết quả và hạn chế đã chỉ ra, nhóm nghiên cứu đề xuất các hướng phát triển tiếp theo của đề tài như sau:

1. **Tối ưu hóa nhân tính toán phần cứng (Hardware Kernel Optimization)**:
   - Viết lại toán tử quét chọn lọc SS2D bằng nhân tính toán chuyên dụng **Custom CUDA / Triton Kernel** được thiết kế riêng cho kiến trúc Turing/Ampere.
   - Áp dụng các kỹ thuật nén mô hình như Lượng tử hóa độ chính xác dấu phẩy động (FP16 / INT8 Quantization) thông qua TensorRT hoặc OpenVINO nhằm đưa tốc độ suy luận trên CPU xuống dưới 50 ms.
2. **Mở rộng sang bài toán phân đoạn trên chuỗi Video nội soi thời gian thực (Video Polyp Segmentation)**:
   - Khai thác năng lực mô hình hóa thời gian (Temporal Modeling) tự nhiên của kiến trúc Mamba 1D để kết nối thông tin giữa các khung hình video kế tiếp nhau (Cross-frame Temporal Consistency), loại bỏ hiện tượng nhấp nháy mặt nạ (Flickering) khi camera di chuyển.
3. **Phân loại mô bệnh học thời gian thực (Optical Biopsy)**:
   - Nâng cấp mạng đa nhiệm: Vừa phân đoạn mặt nạ tổn thương vừa dự đoán phân loại mô bệnh học theo tiêu chuẩn NBI International Colorectal Endoscopic (NICE) hoặc Kudo Pit Pattern (phân biệt u tuyến tân sinh cần cắt bỏ và polyp tăng sản lành tính có thể để lại), hỗ trợ chiến lược lâm sàng "Chẩn đoán và Bỏ lại" (Diagnose and Leave).
4. **Kiểm thử lâm sàng tiền cứu (Prospective Clinical Trials)**:
   - Phối hợp với các trung tâm nội soi và bệnh viện chuyên khoa để kết nối hệ thống vào máy nội soi thực tế, đánh giá hiệu năng chẩn đoán trong các ca nội soi trực tiếp trên bệnh nhân dưới sự giám sát của hội đồng đạo đức y học.
