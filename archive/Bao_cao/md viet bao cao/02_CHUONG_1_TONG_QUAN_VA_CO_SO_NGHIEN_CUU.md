# CHƯƠNG 1. TỔNG QUAN VÀ CƠ SỞ NGHIÊN CỨU

---

## 1.1. TỔNG QUAN BÀI TOÁN PHÂN ĐOẠN POLYP TRONG ẢNH NỘI SOI ĐẠI TRỰC TRÀNG

### 1.1.1. Đặc điểm giải phẫu và ý nghĩa lâm sàng của polyp đại tràng
Polyp đại trực tràng là những khối mô tân sinh nhô lên bất thường từ bề mặt lớp biểu mô niêm mạc lòng ruột già (bao gồm manh tràng, kết tràng lên, kết tràng ngang, kết tràng xuống, kết tràng sigma và trực tràng). Về mặt giải phẫu bệnh học, polyp được phân loại thành hai nhóm chính:
- **Polyp không tân sinh (Non-neoplastic)**: Bao gồm polyp tăng sản (hyperplastic polyps), polyp viêm và polyp thừa mô (hamartoma). Nhóm này hầu hết lành tính và có rất ít hoặc không có nguy cơ chuyển dạng ác tính.
- **Polyp tân sinh (Neoplastic)**: Tiêu biểu nhất là các u tuyến (adenomas) như u tuyến ống (tubular adenoma), u tuyến nhánh (villous adenoma) và u tuyến răng cưa (sessile serrated lesion - SSL). Đây là các tổn thương tiền ung thư trực tiếp; qua quá trình đột biến gen tích lũy từ 5 đến 10 năm theo chu trình u tuyến - ung thư (adenoma-carcinoma sequence), các u tuyến này sẽ xâm lấn lớp dưới niêm và chuyển thành ung thư biểu mô đại trực tràng di căn.

Kỹ thuật nội soi đại trực tràng quang học độ phân giải cao (High-Definition White Light Colonoscopy) kết hợp nhuộm màu điện tử (NBI, FICE) hiện là tiêu chuẩn vàng trong tầm soát. Khi phát hiện polyp, bác sĩ nội soi sẽ tiến hành cắt bỏ polyp (polypectomy) ngay trong phiên can thiệp để triệt tiêu nguồn gốc khối u. Tuy nhiên, việc đánh giá chính xác vị trí, diện tích và ranh giới mô lành - mô bệnh đóng vai trò sống còn trong việc quyết định kỹ thuật cắt (cắt bằng thòng lọng nguội, cắt polyp có tiêm phồng dưới niêm mạc EMR, hay bóc tách dưới niêm mạc ESD).

### 1.1.2. Thách thức phân đoạn trong môi trường quang học nội soi
Trong xử lý ảnh y tế tự động, bài toán phân đoạn polyp từ ảnh nội soi được đánh giá là một trong những bài toán phức tạp và nhiều thách thức nhất bởi các yếu tố đặc thù sau:
1. **Ranh giới mờ và độ tương phản thấp (Poor Contrast & Blurry Boundaries)**: Polyp dạng phẳng (sessile/flat) hoặc dạng u tuyến răng cưa thường không có cuống, chỉ hơi gồ nhẹ trên niêm mạc, màu sắc hồng nhạt gần như đồng nhất với niêm mạc đại tràng lành xung quanh, khiến các bộ lọc cạnh truyền thống hoàn toàn bất lực.
2. **Kích thước và hình thái đa dạng (High Intra-class Variation)**: Trong cùng một bệnh nhân, kích thước polyp có thể dao động từ dưới 2 mm (dạng chấm nhỏ) đến trên 30 mm (khối u sùi thùy múi lớn che lấp lòng ruột).
3. **Môi trường nội soi nhiều nhiễu động học (Severe Visual Artifacts)**: Lòng đại tràng liên tục co bóp nhu động; ánh sáng từ đầu camera nội soi tạo ra các điểm chói lóa cục bộ (specular reflections); dịch nhầy ruột, bọt khí, cặn phân và vết máu bám dính trên thành ruột rất dễ bị mô hình học sâu nhầm lẫn là polyp (sinh ra dương tính giả - False Positives).

> **[HÌNH ẢNH MINH HỌA — HÌNH 1.1]**  
> - **Đường dẫn tệp gốc**: `figures/kvasir_polyp_samples_diversity.png` (Ảnh trích từ bộ dữ liệu Kvasir-SEG)  
> - **Tên tiêu đề chuẩn**: *Hình 1.1: Đặc điểm hình thái đa dạng của các dạng polyp đại trực tràng từ bộ dữ liệu nội soi Kvasir-SEG*  
> 
> **[PHẦN NHẬN XÉT VÀ PHÂN TÍCH HỌC THUẬT]**:  
> - *Phân tích định lượng*: Hình 1.1 minh họa 4 ca bệnh điển hình: (a) Polyp có cuống kích thước lớn (> 15mm), nổi rõ trong lòng ruột; (b) Polyp dạng phẳng trải rộng với bờ ranh giới rất mờ; (c) Polyp nhỏ li ti (< 3mm) nằm kẹp giữa nếp gấp niêm mạc; (d) Ca bệnh có ánh đèn flash phản chiếu mạnh gây lóa trắng bề mặt tổn thương.  
> - *Ý nghĩa kỹ thuật & bệnh học*: Sự đa dạng cực đoan này đòi hỏi mô hình học sâu không thể chỉ dựa vào đặc trưng màu sắc hoặc đường biên cục bộ (local texture). Thay vào đó, mô hình bắt buộc phải có trường tiếp nhận đủ lớn để nắm bắt tương quan không gian toàn cục (global structural context), từ đó phân biệt được đâu là nếp gấp ruột sinh lý bình thường và đâu là khối mô tân sinh bất thường.

### 1.1.3. Khảo sát các độ đo đánh giá trong phân đoạn ảnh y tế
Để lượng hóa độ chính xác của các thuật toán phân đoạn ảnh, cộng đồng y khoa và thị giác máy tính quốc tế sử dụng một hệ thống các chỉ số chuẩn tắc sau:

1. **Hệ số tương đồng Dice (Dice Similarity Coefficient - DSC / F1-score)**:  
   Đo lường mức độ trùng khớp giữa mặt nạ phân đoạn dự đoán của mô hình ($P$) và mặt nạ chuẩn Ground Truth ($G$):
   $$\text{Dice}(P, G) = \frac{2 \times |P \cap G|}{|P| + |G|} = \frac{2 \times TP}{2 \times TP + FP + FN}$$
   Giá trị Dice dao động trong khoảng $[0, 1]$. Trong y tế, chỉ số Dice đặc biệt ưu tiên việc phát hiện đúng diện tích tổn thương và phạt nặng các trường hợp bỏ sót (FN).

2. **Chỉ số tương đồng Jaccard (Intersection over Union - IoU)**:  
   Được định nghĩa là tỷ lệ giữa diện tích phần giao và diện tích phần hợp của hai vùng mặt nạ:
   $$\text{IoU}(P, G) = \frac{|P \cap G|}{|P \cup G|} = \frac{TP}{TP + FP + FN}$$
   Mối quan hệ toán học chặt chẽ giữa Dice và IoU được biểu diễn qua công thức biến đổi: $\text{IoU} = \frac{\text{Dice}}{2 - \text{Dice}}$.

3. **Độ chính xác (Precision) và Độ nhạy (Recall / Sensitivity)**:  
   $$\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}$$
   Trong tầm soát polyp, **Recall** có ý nghĩa sống còn vì thể hiện tỷ lệ polyp thật sự được phát hiện, giảm thiểu tối đa hiện tượng bỏ sót (FN). Ngược lại, **Precision** phản ánh mức độ tin cậy của cảnh báo, giúp bác sĩ không bị phân tâm bởi các báo động giả (FP).

4. **Độ chính xác trung bình mAP (Mean Average Precision)**:  
   Độ đo chuẩn tắc trong hệ sinh thái YOLO.
   - $\text{mAP@50}$: Độ chính xác trung bình tính tại ngưỡng trùng khớp $\text{IoU} = 0.50$.
   - $\text{mAP@50-95}$: Giá trị trung bình của mAP được quét qua 10 ngưỡng IoU liên tiếp từ $0.50$ đến $0.95$ với bước nhảy $0.05$. Đây là chỉ số khắt khe nhất phản ánh độ sắc nét và độ khớp vi mô của đường biên mặt nạ.

---

## 1.2. TỔNG QUAN MÔ HÌNH YOLO VÀ BƯỚC TIẾN CỦA YOLO26-SEG

### 1.2.1. Quá trình phát triển các thế hệ YOLO trong phân đoạn thực thể
Họ mô hình YOLO (You Only Look Once), khởi xướng từ công trình kinh điển của Joseph Redmon (2016), đã tạo nên một cuộc cách mạng trong thị giác máy tính nhờ chuyển đổi bài toán phát hiện đối tượng từ cơ chế hai giai đoạn (Two-stage như Faster R-CNN) sang bài toán hồi quy đơn giai đoạn (One-stage) thực thi theo thời gian thực.

Trong bài toán phân đoạn thực thể, bước ngoặt lớn xuất hiện từ phiên bản YOLOv5-seg và YOLOv8-seg thông qua việc tích hợp nguyên lý **YOLACT (You Only Look At CoefficienTs)**. Thay vì dự đoán mặt nạ điểm ảnh trực tiếp vốn cực kỳ tốn kém tài nguyên, mạng chia làm hai nhánh song song:
1. Nhánh **Protonet**: Sinh ra một tập hợp gồm $k$ mặt nạ nguyên mẫu (Prototype Masks) kích thước cố định đại diện cho toàn bộ bức ảnh.
2. Nhánh **Mask Coefficient**: Tại mỗi hộp bao phát hiện được, mô hình dự đoán một véc-tơ gồm $k$ hệ số mặt nạ tương ứng.
3. Mặt nạ phân đoạn cuối cùng của từng đối tượng được tái tạo nhanh chóng thông qua phép nhân ma trận giữa véc-tơ hệ số và các mặt nạ nguyên mẫu, theo sau bởi hàm kích hoạt Sigmoid và cắt xén (cropping) theo khung bao.

### 1.2.2. Kiến trúc tổng thể của YOLO26-seg
Phiên bản thế hệ mới **YOLO26-seg** (Ultralytics, 2026) kế thừa và nâng cấp toàn diện cấu trúc mạng:
- **Backbone**: Sử dụng các khối tích chập nâng cao giúp tối ưu hóa luồng truyền gradient, tăng tốc độ tính toán trên phần cứng GPU hiện đại.
- **Neck**: Kiến trúc PAN-FPN (Path Aggregation Network - Feature Pyramid Network) kết hợp các đường dẫn truyền đặc trưng từ dưới lên (Bottom-up) và từ trên xuống (Top-down), cho phép dung hợp thông tin từ mức độ phân giải cao (P3, stride 8) đến mức ngữ nghĩa sâu (P5, stride 32).
- **Head**: Thiết kế không neo (Anchor-free) tách biệt hoàn toàn giữa nhánh phát hiện hộp bao, nhánh phân loại nhãn và nhánh dự đoán hệ số phân đoạn, giúp loại bỏ việc gán nhãn thủ công và tăng tốc độ suy luận đáng kể.

Mặc dù YOLO26-seg đạt tốc độ khung hình rất ấn tượng (trên 60 FPS), mô hình vẫn bộc lộ hạn chế cố hữu của các mạng CNN: kích thước bộ lọc tích chập cục bộ ($3\times3$ hoặc $5\times5$) khiến mô hình gặp khó khăn trong việc nhận thức các mối quan hệ hình học xa, dẫn đến việc mặt nạ phân đoạn polyp phẳng thường bị rách rưới hoặc biến dạng.

---

## 1.3. MÔ HÌNH KHÔNG GIAN TRẠNG THÁI (SSM) VÀ KIẾN TRÚC VMAMBA

### 1.3.1. Cơ sở lý thuyết của State Space Models (Mamba)
Mô hình không gian trạng thái cổ điển (State Space Models - SSM) có nguồn gốc từ lý thuyết điều khiển tự động, mô tả một hệ thống tuyến tính liên tục ánh xạ chuỗi tín hiệu đầu vào 1 chiều $x(t) \in \mathbb{R}$ sang chuỗi đầu ra $y(t) \in \mathbb{R}$ thông qua biến trạng thái ẩn $h(t) \in \mathbb{R}^N$:
$$\frac{dh(t)}{dt} = \mathbf{A}h(t) + \mathbf{B}x(t)$$
$$y(t) = \mathbf{C}h(t) + \mathbf{D}x(t)$$
Trong đó: $\mathbf{A} \in \mathbb{R}^{N \times N}$ là ma trận chuyển trạng thái hệ thống, $\mathbf{B} \in \mathbb{R}^{N \times 1}$ là ma trận chiếu đầu vào, $\mathbf{C} \in \mathbb{R}^{1 \times N}$ là ma trận chiếu đầu ra, và $\mathbf{D}$ là hệ số truyền thẳng.

Đột phá lớn nhất của kiến trúc **Mamba** (Albert Gu & Tri Dao, 2023) là đưa vào **Cơ chế chọn lọc phụ thuộc tham số (Selective Scan Mechanism - S6)**: Thay vì cố định các ma trận $\mathbf{B}, \mathbf{C}$ và bước thời gian rời rạc hóa $\mathbf{\Delta}$, Mamba biến chúng thành các hàm phụ thuộc trực tiếp vào dữ liệu đầu vào: $\mathbf{B}(x), \mathbf{C}(x), \mathbf{\Delta}(x)$. Điều này cho phép mô hình chọn lọc ghi nhớ thông tin quan trọng và chủ động quên đi các thông tin nhiễu, tương tự như cơ chế Attention của Transformer nhưng với độ phức tạp tính toán chỉ là tuyến tính **$O(N)$** thay vì bậc hai $O(N^2)$.

### 1.3.2. Cơ chế quét chọn lọc hai chiều không gian SS2D (2D Selective Scan)
Dữ liệu hình ảnh 2 chiều không có tính chất thứ tự tự nhiên như chuỗi văn bản 1 chiều. Nếu chỉ trải phẳng (flatten) ảnh thành 1 chuỗi dài, các điểm ảnh liền kề theo phương thẳng đứng sẽ bị đẩy ra rất xa nhau trong chuỗi 1 chiều, phá hủy tính liên kết không gian.

Để giải quyết triệt để vấn đề này, kiến trúc **VMamba (Visual State Space Model)** (Liu et al., 2024) đã đề xuất khối quét chọn lọc không gian hai chiều **SS2D (2D Selective Scan)**:
1. Ma trận đặc trưng hình ảnh 2 chiều kích thước $H \times W \times C$ được quét đồng thời theo **4 hướng quét độc lập**:
   - Quét từ góc trên-trái xuống dưới-phải (Top-Left to Bottom-Right).
   - Quét từ góc dưới-phải lên trên-trái (Bottom-Right to Top-Left).
   - Quét từ góc trên-phải xuống dưới-trái (Top-Right to Bottom-Left).
   - Quét từ góc dưới-trái lên trên-phải (Bottom-Left to Top-Right).
2. Mỗi chuỗi quét được xử lý song song thông qua cơ chế chọn lọc SSM 1D để nắm bắt ngữ cảnh từ mọi hướng.
3. Sau đó, 4 chuỗi đầu ra được phục hồi (unfold) về lại cấu trúc không gian 2D ban đầu và cộng tổng hợp nhất.

> **[HÌNH ẢNH MINH HỌA — HÌNH 1.2]**  
> - **Đường dẫn tệp gốc**: `figures/vmamba_ss2d_mechanism.png` (Sơ đồ cơ chế SS2D)  
> - **Tên tiêu đề chuẩn**: *Hình 1.2: Sơ đồ nguyên lý cơ chế quét chọn lọc hai chiều không gian SS2D trong kiến trúc VMamba*  
> 
> **[PHẦN NHẬN XÉT VÀ PHÂN TÍCH HỌC THUẬT]**:  
> - *Phân tích định lượng*: Khối SS2D biến đổi một bản đồ đặc trưng có độ dài $N = H \times W$ thành 4 chuỗi quét song song. Thay vì tính ma trận tương quan kích thước $N \times N$ với chi phí bộ nhớ $O(N^2)$ như phép Self-Attention của ViT, cơ chế SS2D chỉ tiêu tốn chi phí tính toán và bộ nhớ tuyến tính $O(N)$.  
> - *Ý nghĩa kỹ thuật & bệnh học*: Nhờ việc quét theo cả 4 hướng chéo và dọc/ngang, mỗi điểm ảnh trong vùng polyp đều nhận được thông tin phản hồi từ toàn bộ khung hình nội soi. Điều này giúp mô hình nhận thức được toàn vẹn cấu trúc hình học của polyp ngay cả khi một phần ranh giới bị che khuất hoặc bị lóa sáng bởi đèn nội soi.

---

## 1.4. KHẢO SÁT CÁC CÔNG TRÌNH NGHIÊN CỨU LIÊN QUAN

*Bảng 1.1: So sánh đặc tính của các phương pháp phân đoạn polyp dựa trên CNN, Transformer và SSM*

| Hướng tiếp cận | Mô hình tiêu biểu | Ưu điểm chính | Hạn chế cố hữu | Khả năng chạy Real-time |
|:---|:---|:---|:---|:---:|
| **CNN truyền thống** | UNet (2015), PraNet (2020), HarDNet-MSEG (2021) | Cấu trúc đơn giản, tốc độ huấn luyện nhanh, phát hiện biên cục bộ tốt | Trường tiếp nhận hạn chế, dễ đứt gãy mặt nạ ở polyp phẳng | Khá cao (30–45 FPS) |
| **Vision Transformer** | Polyp-PVT (2021), ColonFormer (2022) | Bao quát ngữ cảnh toàn cục xuất sắc, mặt nạ phân đoạn mịn | Chi phí tính toán $O(N^2)$, số lượng tham số lớn, tiêu tốn VRAM | Thấp (< 15 FPS) |
| **State Space Model (SSM)** | Polyp-Mamba (2024), VM-UNet (2024) | Nắm bắt tương quan tầm xa với độ phức tạp tuyến tính $O(N)$ | Thường thiết kế dạng UNet cồng kềnh, chưa tối ưu cho phát hiện thực thể | Trung bình (20–30 FPS) |
| **Đề xuất của đề tài** | **TSVM + YOLO26-seg** | Dung hợp ngữ cảnh toàn cục SS2D vào mạng one-stage gọn nhẹ, triệt tiêu FP nhờ tập BG20 | Tăng thêm độ trễ suy luận so với CNN thuần túy | **Đạt chuẩn lâm sàng (Real-time)** |

1. **Các nghiên cứu dựa trên mạng tích chập CNN**:
   - Mạng **UNet** và các biến thể nâng cao như ResUNet++, PraNet (Fan et al., MICCAI 2020) đã đạt được nhiều thành tựu lớn trong phân đoạn ảnh y tế. PraNet sử dụng mô-đun Parallel Partial Decoder để kết hợp đặc trưng mức cao và mô-đun Reverse Attention để đào sâu ranh giới. Tuy nhiên, các kiến trúc này hầu hết là mạng phân đoạn ngữ nghĩa (Semantic Segmentation), dự đoán trực tiếp ở mức điểm ảnh trên toàn ảnh nên tốc độ xử lý chậm và dễ sinh cảnh báo giả khi gặp ảnh không có polyp.
2. **Các nghiên cứu dựa trên Transformer**:
   - **Polyp-PVT** (Dong et al., 2021) khai thác Pyramid Vision Transformer làm backbone để mô hình hóa ngữ cảnh đa tỷ lệ. Mặc dù đạt chỉ số Dice rất cao trên tập Kvasir-SEG, độ phức tạp tính toán lớn khiến mô hình không thể nhúng vào các thiết bị nội soi cầm tay hoặc hệ thống máy tính cấu hình phổ thông tại các bệnh viện tuyến dưới.
3. **Các nghiên cứu ứng dụng Mamba trong phân đoạn y tế**:
   - Gần đây, **Polyp-Mamba** (Xu et al., MICCAI 2024) đã tiên phong đưa Mamba vào kiến trúc UNet để phân đoạn polyp và chứng minh hiệu quả vượt trội so với Transformer. Tuy nhiên, Polyp-Mamba vẫn là mô hình phân đoạn ngữ nghĩa đơn thuần, chưa được tích hợp vào một pipeline phát hiện thực thể hoàn chỉnh có khả năng xuất đồng thời hộp bao tọa độ, nhãn bệnh học và mặt nạ thời gian thực như hệ sinh thái YOLO.

---

## 1.5. KHOẢNG TRỐNG NGHIÊN CỨU VÀ GIẢI PHÁP ĐỀ XUẤT CỦA ĐỀ TÀI

Từ các khảo sát thực tế trên, đề tài xác định được **3 khoảng trống nghiên cứu then chốt**:
1. **Khoảng trống về mặt kiến trúc**: Chưa có công trình nào nghiên cứu việc tích hợp khối quét chọn lọc không gian hai chiều VMamba vào mạng phân đoạn thực thể end-to-end thế hệ mới nhất YOLO26-seg để tận dụng đồng thời tốc độ suy luận của YOLO và năng lực ngữ cảnh toàn cục tuyến tính của Mamba.
2. **Khoảng trống về xử lý báo động giả trong dữ liệu y tế**: Đa phần các nghiên cứu hiện nay chỉ huấn luyện mô hình trên các tập dữ liệu "lý tưởng" chỉ chứa toàn ảnh dương tính có polyp (như tập Kvasir-SEG 1.000 ảnh gốc). Khi triển khai vào thực tế, khi gặp niêm mạc đại tràng bình thường, mô hình rất dễ bị "ảo giác" (hallucination) và sinh ra các mặt nạ polyp giả.
3. **Khoảng trống về tính ứng dụng thực tiễn**: Các nghiên cứu học thuật thường chỉ dừng lại ở việc báo cáo chỉ số trong bài báo mà thiếu đi một hệ sinh thái phần mềm hoàn chỉnh cho phép bác sĩ tương tác trực tiếp qua Web và ứng dụng di động.

**Giải pháp đề xuất của đề tài**:
- Thiết kế khối cải tiến **Topology-Shape-aware VMamba (TSVM)** và tích hợp chiến lược vào tầng 10 (mức P5) của mô hình YOLO26s-seg.
- Xây dựng quy trình làm giàu dữ liệu chuẩn mực `Kvasir_YOLO_SEG_BG20` bổ sung 20% ảnh niêm mạc bình thường với nhãn rỗng để rèn luyện khả năng ức chế báo động giả.
- Phát triển trọn vẹn hệ thống ứng dụng minh họa gồm FastAPI AI Microservice, Java Spring Boot Web và Flutter Mobile App phục vụ trình diễn và đánh giá lâm sàng.

---

## 1.6. TÓM TẮT CHƯƠNG 1
Chương 1 đã trình bày toàn diện bối cảnh bệnh học và tầm quan trọng của việc phân đoạn polyp đại trực tràng; phân tích sâu sắc các độ đo đánh giá y tế chuẩn mực; phân tích ưu nhược điểm của các kiến trúc YOLO26-seg, State Space Model (Mamba) và khối quét 2D (SS2D). Qua khảo sát các công trình tiền nhiệm, đề tài đã chỉ rõ khoảng trống nghiên cứu và thiết lập cơ sở khoa học vững chắc cho việc thiết kế kiến trúc mô hình đề xuất TSVM sẽ được trình bày chi tiết trong Chương 2.
