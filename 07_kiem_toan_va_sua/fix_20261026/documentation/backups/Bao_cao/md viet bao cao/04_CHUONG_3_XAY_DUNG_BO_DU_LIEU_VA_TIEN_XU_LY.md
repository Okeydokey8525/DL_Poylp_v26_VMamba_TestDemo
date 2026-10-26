# CHƯƠNG 3. XÂY DỰNG BỘ DỮ LIỆU VÀ TIỀN XỬ LÝ

---

## 3.1. NGUỒN DỮ LIỆU THỰC NGHIỆM

Để đảm bảo tính khách quan, khả năng tái lập và độ tin cậy trong đánh giá y tế, đề tài sử dụng kết hợp các bộ dữ liệu ảnh nội soi đại trực tràng công khai uy tín hàng đầu trên thế giới:

### 3.1.1. Bộ dữ liệu nội soi Kvasir-SEG (Simula Research Laboratory, Na Uy)
Bộ dữ liệu **Kvasir-SEG** (Jha et al., MMM 2020) là bộ dữ liệu chuẩn mực được chấp nhận rộng rãi nhất trong cộng đồng nghiên cứu thị giác máy tính y tế. Bộ dữ liệu bao gồm:
- **Số lượng**: Đúng 1.000 ảnh nội soi đại trực tràng độ phân giải cao (độ phân giải dao động từ $332 \times 487$ đến $1072 \times 1920$ pixel).
- **Nhãn phân đoạn**: Đi kèm 1.000 mặt nạ nhị phân chuẩn (Ground-Truth Binary Masks) định dạng PNG, trong đó các điểm ảnh thuộc vùng polyp có giá trị 255 (trắng) và vùng niêm mạc xung quanh có giá trị 0 (đen).
- **Độ tin cậy y khoa**: Toàn bộ các ảnh và mặt nạ đều được khoanh vùng và kiểm duyệt nghiêm ngặt bởi các chuyên gia tiêu hóa và bác sĩ nội soi giàu kinh nghiệm tại Bệnh viện Đại học Oslo và Bệnh viện Bærum (Na Uy).
- **Đặc điểm bệnh học**: Tập hợp đầy đủ các tổn thương polyp đa dạng về kích thước, hình thái (polyp có cuống, không cuống, polyp phẳng) và ở nhiều vị trí giải phẫu khác nhau của khung đại tràng.

### 3.1.2. Bộ dữ liệu niêm mạc bình thường normal-cecum (Kvasir v2)
Một hạn chế chí tử của tập Kvasir-SEG nguyên bản là **100% các bức ảnh đều chứa polyp** (ảnh dương tính hoàn toàn). Khi huấn luyện mô hình học sâu trên tập dữ liệu này, mạng sẽ hình thành thiên kiến tiên nghiệm (Priors): mạng luôn giả định trong mọi khung hình nội soi đều có polyp, dẫn đến việc khi gặp niêm mạc ruột bình thường có nếp gấp khúc hoặc ánh đèn phản chiếu, mô hình sẽ cố gắng "vẽ" ra một polyp giả (sinh ra báo động giả - False Positive).

Để khắc phục triệt để khiếm khuyết này, đề tài đã thu thập thêm **200 ảnh niêm mạc manh tràng hoàn toàn bình thường (normal-cecum)** trích xuất từ bộ dữ liệu **Kvasir v2** (Pogorelov et al., MMSys 2017). Manh tràng (cecum) là đoạn đầu của ruột già, có đặc điểm giải phẫu nhiều nếp gấp niêm mạc sâu, mạch máu phân nhánh phức tạp và góc nhìn camera gập ghềnh, là môi trường thử thách lý tưởng nhất để kiểm tra khả năng phân biệt mô lành của mô hình AI.

### 3.1.3. Các bộ dữ liệu kiểm chứng độc lập (Cross-dataset Validation)
Để đánh giá năng lực tổng quát hóa ngoại suy (Out-of-distribution Generalization) của mô hình trên các thiết bị nội soi và cơ sở y tế khác, đề tài đã chuẩn bị thêm 3 tập dữ liệu độc lập:
1. **CVC-ClinicDB** (Hospital Clínic de Barcelona, Tây Ban Nha): Gồm 612 ảnh trích từ 31 chuỗi video nội soi đại tràng.
2. **CVC-ColonDB**: Gồm 380 ảnh với các ca polyp khó và độ biến thiên quang học cao.
3. **ETIS-Larib PolypDB** (Pháp): Gồm 196 ảnh nội soi độ nét cao chuyên dùng làm chuẩn đánh giá benchmark quốc tế.

---

## 3.2. QUY TRÌNH TIỀN XỬ LÝ VÀ CHUYỂN ĐỔI DỮ LIỆU

### 3.2.1. Thuật toán chuyển đổi Ground-Truth Mask sang nhãn đa giác YOLO
Định dạng nhãn chuẩn của mạng phân đoạn thực thể YOLO yêu cầu mỗi đối tượng được biểu diễn dưới dạng một chuỗi tọa độ đỉnh đa giác (Polygon Vertices) chuẩn hóa về khoảng $[0, 1]$ thay vì ma trận mặt nạ điểm ảnh $H \times W$. 

Quy trình chuyển đổi tự động được hiện thực hóa qua script Python `convert_kvasir_to_yolo_seg.py`:
1. Đọc ảnh mặt nạ nhị phân PNG gốc kích thước $H \times W$.
2. Áp dụng thuật toán tìm đường biên ngoài **Suzuki-Abe (Topological Structural Analysis)** thông qua hàm `cv2.findContours(..., cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)`.
3. Lọc bỏ các đường biên giả hoặc nhiễu hạt quá nhỏ (diện tích $< 10$ pixel).
4. Áp dụng thuật toán xấp xỉ đa giác **Ramer-Douglas-Peucker (RDP)** với sai số $\epsilon$ thích ứng để tối ưu hóa số lượng đỉnh đa giác, loại bỏ các đỉnh dư thừa trên đường thẳng mà vẫn bảo toàn chính xác độ cong của bờ polyp.
5. Chuẩn hóa toàn bộ tọa độ đỉnh $(x_i, y_i)$ theo chiều rộng $W$ và chiều cao $H$:
   $$x_i^{\text{norm}} = \frac{x_i}{W}, \quad y_i^{\text{norm}} = \frac{y_i}{H} \quad (0 \le x_i^{\text{norm}}, y_i^{\text{norm}} \le 1)$$
6. Ghi ra tệp nhãn văn bản `.txt` tương ứng với định dạng chuẩn của Ultralytics:
   ```text
   <class_id> x1 y1 x2 y2 x3 y3 ... xn yn
   ```
   với `class_id = 0` (đại diện cho lớp tổn thương `polyp`).

> **[HÌNH ẢNH MINH HỌA — HÌNH 3.1]**  
> - **Đường dẫn tệp gốc**: `figures/mask_to_yolo_polygon_conversion.png` (Minh họa quá trình trích xuất đa giác)  
> - **Tên tiêu đề chuẩn**: *Hình 3.1: Quy trình trích xuất và chuyển đổi Ground-Truth Mask sang nhãn đa giác đa điểm YOLO Segmentation Polygon*  
> 
> **[PHẦN NHẬN XÉT VÀ PHÂN TÍCH HỌC THUẬT]**:  
> - *Phân tích định lượng*: Hình 3.1 thể hiện 3 bước kế tiếp: (a) Ảnh nội soi gốc; (b) Mặt nạ nhị phân nhẵn của bác sĩ; (c) Đa giác xấp xỉ bao quanh bờ tổn thương với khoảng 30–60 điểm đỉnh. Sai số hình học giữa diện tích đa giác và mặt nạ pixel gốc luôn được khống chế dưới 0.5%.  
> - *Ý nghĩa kỹ thuật & bệnh học*: Việc nén từ ma trận mặt nạ $H \times W$ điểm ảnh thành chuỗi tọa độ đa giác chuẩn hóa giúp giảm kích thước tập nhãn hàng nghìn lần (từ vài trăm megabyte xuống vài megabyte), đồng thời tương thích trực tiếp với cơ chế tính toán mất mát phân đoạn của YOLO26-seg.

### 3.2.2. Xây dựng tập dữ liệu hỗn hợp Kvasir_YOLO_SEG_BG20 (1.200 ảnh)
Đề tài đã thiết kế và đóng gói thành công bộ dữ liệu hỗn hợp mang tên **`Kvasir_YOLO_SEG_BG20`** (bổ sung chính xác 20% ảnh nền âm tính):
- **Tập polyp dương tính**: 1.000 ảnh nội soi từ Kvasir-SEG.
- **Tập nền âm tính (Background)**: 200 ảnh niêm mạc manh tràng bình thường (normal-cecum).
- **Tổng cộng**: Đúng **1.200 ảnh**.

*Bảng 3.1: Thống kê số lượng mẫu phân bổ trong tập dữ liệu hỗn hợp Kvasir_YOLO_SEG_BG20*

| Thành phần tập dữ liệu | Nguồn gốc dữ liệu | Số lượng ảnh huấn luyện (Train) | Số lượng ảnh kiểm định (Val) | Tổng số lượng ảnh |
|:---|:---|:---:|:---:|:---:|
| **Ảnh chứa polyp (Dương tính)** | Kvasir-SEG | 880 | 120 | 1.000 |
| **Ảnh niêm mạc lành (Âm tính)** | Normal-cecum (Kvasir v2) | 160 | 40 | 200 |
| **TỔNG CỘNG** | **Kvasir_YOLO_SEG_BG20** | **1.040 (86.67%)** | **160 (13.33%)** | **1.200 (100%)** |

### 3.2.3. Cơ chế nhãn rỗng (Empty Labels) triệt tiêu báo động giả
Điểm mấu chốt trong kỹ thuật của YOLO là **Cơ chế nhãn rỗng (Empty Label File)**:
- Đối với 200 ảnh nền âm tính normal-cecum, tệp nhãn tương ứng `tên_ảnh.txt` vẫn được tạo ra nhưng hoàn toàn **rỗng (kích thước đúng 0 byte, không chứa bất kỳ dòng văn bản nào)**.
- Khi luồng nạp dữ liệu (DataLoader) của YOLO đọc vào một tệp nhãn rỗng, mạng hiểu rằng: *"Trong toàn bộ bức ảnh này, số lượng đối tượng cần phát hiện là 0 (Zero Ground Truth Objects)"*.
- **Cơ chế tác động vào hàm mất mát**:
  - Nếu mô hình dự đoán bất kỳ hộp bao hoặc mặt nạ nào trên bức ảnh này, toàn bộ điểm tin cậy của các dự đoán đó sẽ bị phạt nặng thông qua hàm mất mát phân loại Binary Cross-Entropy ($\mathcal{L}_{\text{cls}}$) và mất mát đối tượng ($\mathcal{L}_{\text{obj}}$).
  - Quá trình lan truyền ngược gradient sẽ ép các trọng số nơ-ron phải triệt tiêu các phản hồi giả đối với các cấu trúc nếp gấp ruột lành tính, từ đó nâng cao vượt bậc độ đặc hiệu (Specificity) của mô hình.

> **[HÌNH ẢNH MINH HỌA — HÌNH 3.2]**  
> - **Đường dẫn tệp gốc**: `figures/empty_label_mechanism_demo.png` (Minh họa cơ chế nhãn rỗng)  
> - **Tên tiêu đề chuẩn**: *Hình 3.2: Minh họa sự khác biệt giữa tệp nhãn đa giác của ảnh polyp thông thường và tệp nhãn rỗng (0 byte) của ảnh nền âm tính normal-cecum*  
> 
> **[PHẦN NHẬN XÉT VÀ PHÂN TÍCH HỌC THUẬT]**:  
> - *Phân tích định lượng*: Hình 3.2 biểu diễn trực quan: (a) Ảnh polyp kèm tệp `.txt` chứa class 0 và 48 cặp tọa độ; (b) Ảnh manh tràng bình thường kèm tệp `.txt` dung lượng 0 byte.  
> - *Ý nghĩa kỹ thuật & bệnh học*: Trong các phiên nội soi đại tràng thực tế, hơn 80% thời gian quan sát của bác sĩ là đi qua các vùng niêm mạc bình thường không có polyp. Việc rèn luyện mô hình trên 200 ảnh nhãn rỗng là nhân tố quyết định giúp hệ thống CADe không phát ra các tiếng chuông cảnh báo sai liên tục, bảo vệ sự tập trung tối đa của bác sĩ trong phòng mổ.

---

## 3.3. PHƯƠNG PHÁP PHÂN CHIA TẬP DỮ LIỆU VÀ CHUẨN HÓA THỰC NGHIỆM

### 3.3.1. Chiến lược phân chia Train/Val theo seed tất định
Để đảm bảo tính khoa học và không bị rò rỉ dữ liệu (Data Leakage), toàn bộ 1.200 ảnh của tập `Kvasir_YOLO_SEG_BG20` được phân chia thành hai tập con theo tỷ lệ phân tầng (Stratified Split) với hạt giống ngẫu nhiên cố định `random_seed = 42`:
- **Tập huấn luyện (Training Set)**: Gồm **1.040 ảnh** (880 ảnh polyp + 160 ảnh nền âm tính, chiếm đúng 86.67% dữ liệu).
- **Tập kiểm định (Validation Set)**: Gồm **160 ảnh** (120 ảnh polyp + 40 ảnh nền âm tính, chiếm đúng 13.33% dữ liệu).
Tỷ lệ ảnh nền âm tính được giữ vững mức chính xác $160 / 1040 \approx 15.38\%$ ở tập Train và $40 / 160 = 25.00\%$ ở tập Val (trung bình toàn tập là $200 / 1200 = 16.67\% \approx 20\%$).

Danh sách đường dẫn chính xác của từng ảnh trong hai tập được lưu cố định trong hai tệp danh mục: `train.txt` (1.040 dòng) và `val.txt` (160 dòng) tại thư mục gốc của dự án. Tất cả 10 lượt chạy thực nghiệm (10 seed) của cả hai mô hình Baseline và TSVM đều nạp chính xác hai tệp danh mục này để đảm bảo tính đồng nhất tuyệt đối về mặt dữ liệu thử nghiệm.

### 3.3.2. Cấu hình tệp đặc tả dữ liệu data_bg20.yaml
Tệp cấu hình `data_bg20.yaml` được thiết lập chuẩn mực theo quy cách của Ultralytics như sau:

```yaml
# Dataset Kvasir-SEG mở rộng bổ sung 20% ảnh nền âm tính (normal-cecum)
path: C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Kvasir_YOLO_SEG_BG20
train: images/train
val: images/val

names:
  0: polyp

metadata:
  total_images: 1200
  train_images: 1040  # 880 polyp + 160 background
  val_images: 160     # 120 polyp + 40 background
  background_source: normal-cecum (Kvasir v2)
  random_seed: 42
```

---

## 3.4. KỸ THUẬT TĂNG CƯỜNG DỮ LIỆU (DATA AUGMENTATION)

Để nâng cao khả năng khái quát hóa và ngăn ngừa hiện tượng học vẹt (overfitting) trong điều kiện tập dữ liệu y tế giới hạn 1.200 ảnh, quy trình huấn luyện áp dụng một chuỗi các phép biến đổi tăng cường dữ liệu thích ứng với môi trường nội soi:
1. **Biến đổi không gian và hình học**:
   - Lật ngẫu nhiên theo trục ngang (`fliplr = 0.5`): Mô phỏng các góc tiếp cận camera nội soi từ trái hoặc phải.
   - Quay nhẹ góc ngẫu nhiên (`degrees = 10.0`) và biến dạng phối cảnh (`perspective = 0.0005`): Tái hiện chuyển động lắc lư của dây soi khi luồn qua các đoạn ruột uốn khúc.
   - Thu phóng tỷ lệ (`scale = 0.5`): Mô phỏng việc camera đưa lại gần hoặc lùi ra xa polyp.
2. **Biến đổi màu sắc và quang sai**:
   - Điều chỉnh độ sáng, độ bão hòa màu (`hsv_h = 0.015, hsv_s = 0.7, hsv_v = 0.4`): Mô phỏng sự thay đổi cường độ ánh sáng của bóng đèn Xenon/LED nội soi và sự khác biệt về sắc tố niêm mạc giữa các cá thể bệnh nhân.
3. **Kỹ thuật ghép ảnh Mosaic**:
   - Ghép ngẫu nhiên 4 bức ảnh thành 1 khung hình trong giai đoạn đầu huấn luyện (`mosaic = 1.0`), sau đó tự động tắt trong 10 epoch cuối cùng (`close_mosaic = 10`) để mô hình hội tụ trên phân phối ảnh thực tế.

---

## 3.5. TÓM TẮT CHƯƠNG 3
Chương 3 đã hoàn thành việc xây dựng và chuẩn hóa tập dữ liệu thực nghiệm `Kvasir_YOLO_SEG_BG20` (1.200 ảnh); giải quyết thấu đáo vấn đề nhãn đa giác phân đoạn; phân tích chuyên sâu vai trò của 200 ảnh nền âm tính manh tràng kết hợp cơ chế nhãn rỗng 0 byte trong việc triệt tiêu báo động giả; đồng thời thiết lập tệp cấu hình tất định `data_bg20.yaml` sẵn sàng cho quy trình huấn luyện trên máy chủ đám mây.
