# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT

> **Ghi chú soạn thảo (xóa khi nộp):**
> - Bản rút gọn, nén từ `md_bao_cao/03_CHUONG_2_CO_SO_LY_THUYET.md` (tag git `ban_day_du_147`). Giữ số mục 2.1–2.8 như bản đầy đủ vì Chương 6 trỏ tới; thứ tự trích dẫn lần đầu giữ nguyên.
> - Mọi ví dụ số trong chương là **ví dụ minh họa tự đặt**, không phải số liệu thực nghiệm.

Chương này trình bày kiến thức nền cho Chương 3 và Chương 6: các bài toán thị giác, mạng tích chập, họ YOLO và YOLO26-seg, cơ chế chú ý, mô hình không gian trạng thái (Mamba, VMamba), các độ đo và phương pháp so sánh hai mô hình qua nhiều lần huấn luyện.

## 2.1. Các bài toán thị giác máy tính

*Bảng 2.1. So sánh ba bài toán thị giác cơ bản*

| Bài toán | Câu hỏi trả lời | Đầu ra | Ví dụ với ảnh nội soi |
|---|---|---|---|
| Phân loại ảnh | Ảnh có gì? | Một nhãn (hoặc xác suất) cho cả ảnh | "Ảnh có polyp" với xác suất 0,97 |
| Phát hiện đối tượng | Đối tượng ở đâu? | Danh sách hộp bao, mỗi hộp có lớp và độ tin cậy | Hộp (x₁, y₁, x₂, y₂) quanh polyp, độ tin cậy 0,91 |
| Phân đoạn ảnh | Điểm ảnh nào thuộc đối tượng? | Mặt nạ cùng kích thước ảnh | Các điểm ảnh thuộc polyp mang giá trị 1 |

**Phân đoạn ngữ nghĩa** gán mỗi điểm ảnh vào một lớp, không phân biệt các đối tượng cùng lớp: ảnh có hai polyp chỉ cho một mặt nạ chung (U-Net [10], PraNet [9]). **Phân đoạn thực thể** tách riêng từng đối tượng, mỗi polyp có hộp bao, độ tin cậy và mặt nạ riêng (YOLO26-seg). Hình 2.1 minh họa bốn kiểu đầu ra trên cùng một ảnh.

![Hình 2.1](../hinh/chung/vi/t01_bon_kieu_dau_ra.png)

*Hình 2.1. Bốn kiểu đầu ra trên cùng một ảnh tập kiểm định có hai polyp: (a) phân loại ảnh, (b) phát hiện đối tượng bằng hộp bao, (c) phân đoạn ngữ nghĩa (hai polyp chung một mặt nạ), (d) phân đoạn thực thể (mỗi polyp một mặt nạ riêng). Hộp bao và mặt nạ vẽ từ nhãn đa giác của ảnh; xác suất ở ô (a) là số minh họa, không phải đầu ra mô hình.*

*Nguồn: ảnh từ Kvasir-SEG [5]; hình do nhóm vẽ.*

Đề tài chọn phân đoạn thực thể vì đầu ra vừa có mặt nạ để quan sát đường biên, vừa có hộp bao và độ tin cậy để hiển thị trong ứng dụng.

## 2.2. Mạng nơ-ron tích chập

Phép tích chập trượt một bộ lọc nhỏ trên ảnh; tại mỗi vị trí, đầu ra là tổng các tích giữa bộ lọc và vùng ảnh bên dưới:

$$ y(i,j) = \sum_{u}\sum_{v} w(u,v)\, x(i+u,\ j+v) + b \tag{2.1} $$

**Ví dụ.** Với vùng ảnh $x = \begin{bmatrix} 10 & 10 & 80 \\ 10 & 10 & 80 \\ 10 & 10 & 80 \end{bmatrix}$ và bộ lọc biên dọc $w = \begin{bmatrix} -1 & 0 & 1 \\ -1 & 0 & 1 \\ -1 & 0 & 1 \end{bmatrix}$, đầu ra tại tâm là $3\times(-10 + 80) = 210$, báo hiệu biên dọc; ở vùng đồng nhất đầu ra bằng 0. Trong CNN, các bộ lọc được học từ dữ liệu.

Tích chập phù hợp với ảnh nhờ kết nối cục bộ, chia sẻ trọng số (lớp $k\times k$ từ $C_\text{in}$ sang $C_\text{out}$ kênh có $k^2 C_\text{in} C_\text{out}$ trọng số, không phụ thuộc kích thước ảnh) và đồng biến tịnh tiến. Đề tài dùng thêm **tích chập 1×1** để đổi số kênh và **tích chập theo chiều sâu** (một bộ lọc riêng cho từng kênh, rất ít tham số). Các thành phần đi kèm gồm chuẩn hóa theo lô (BN), hàm kích hoạt $\mathrm{SiLU}(x) = x\cdot\sigma(x)$ (khối `Conv` của YOLO gồm tích chập, BN, SiLU) và kết nối tắt $y = x + F(x)$. Hạn chế chính là **trường tiếp nhận**: xếp chồng tích chập 3×3 chỉ mở rộng dần vùng nhìn, nên CNN thuần khó nắm ngữ cảnh toàn ảnh. Đây là động cơ để thêm attention hoặc SSM vào mạng.

## 2.3. Họ mô hình YOLO

### 2.3.1. Ý tưởng phát hiện một giai đoạn

Mô hình hai giai đoạn như Mask R-CNN [34] đề xuất vùng trước rồi phân loại từng vùng; YOLO [18] gộp làm một: ảnh đi qua mạng một lần, mỗi ô trên bản đồ đặc trưng dự đoán trực tiếp hộp bao, lớp và độ tin cậy. Một mô hình YOLO hiện đại gồm:
- **Backbone:** trích đặc trưng qua các mức P1–P5, mức P$k$ bằng $1/2^k$ ảnh vào (ảnh 640×640 thì P5 là 20×20).
- **Neck:** FPN [35] truyền ngữ nghĩa từ mức sâu xuống mức nông, PAN [36] truyền chi tiết vị trí theo chiều ngược lại.
- **Head:** dự đoán tại P3, P4, P5, ứng với đối tượng nhỏ, vừa, lớn.

### 2.3.2. Gán nhãn, hàm mất mát và bỏ NMS

YOLO26 dùng bộ gán nhãn căn chỉnh nhiệm vụ của TOOD [37]: một điểm dự đoán được chọn khi vừa có điểm lớp cao vừa có hộp trùng tốt với hộp thật. Hộp được học bằng mất mát CIoU [38], mở rộng IoU bằng hạng tử phạt khoảng cách tâm và độ lệch tỉ lệ khung. Để bỏ bước lọc trùng NMS, YOLOv10 [20] huấn luyện song song **đầu một-nhiều** (mỗi đối tượng gán cho nhiều điểm, nhiều tín hiệu học) và **đầu một-một** (mỗi đối tượng đúng một điểm, đầu ra không trùng); khi suy luận chỉ dùng đầu một-một. YOLO26 kế thừa cơ chế này.

### 2.3.3. Phân đoạn thực thể bằng mặt nạ mẫu

Theo YOLACT [19], nhánh Proto sinh $K$ **mặt nạ mẫu** $P_1, \dots, P_K$ dùng chung cho cả ảnh; với mỗi đối tượng, đầu dự đoán sinh $K$ **hệ số** $c_1, \dots, c_K$, và mặt nạ là tổ hợp tuyến tính qua sigmoid, sau đó cắt theo hộp bao:

$$ \hat M = \sigma\Big(\sum_{k=1}^{K} c_k P_k\Big) \tag{2.2} $$

Ví dụ với $K = 2$ trên lưới 2×2: $P_1 = \begin{bmatrix} 4 & 4 \\ -4 & -4 \end{bmatrix}$ (nửa trên), $P_2 = \begin{bmatrix} 4 & -4 \\ 4 & -4 \end{bmatrix}$ (nửa trái). Đối tượng có hệ số $(1,\ 1)$ cho tổng $\begin{bmatrix} 8 & 0 \\ 0 & -8 \end{bmatrix}$, qua sigmoid và ngưỡng "lớn hơn 0,5" chỉ ô trên–trái thuộc đối tượng; đối tượng có hệ số $(-1,\ 0)$ cho tổng $\begin{bmatrix} -4 & -4 \\ 4 & 4 \end{bmatrix}$, tức nửa dưới. Chỉ với vài hệ số, mỗi đối tượng có mặt nạ riêng. YOLO26-seg dùng $K = 32$ mặt nạ mẫu kích thước 160×160.

## 2.4. Mô hình YOLO26-seg

### 2.4.1. Kiến trúc

YOLO26 [6] được Ultralytics công bố năm 2026 (bản tiền ấn phẩm). Đề tài dùng cỡ *small* (YOLO26s-seg), hệ số độ sâu và độ rộng 0,5.

*Bảng 2.2. Các khối chính của YOLO26s-seg (ảnh vào 640×640)*

| Phần | Tầng | Khối | Vai trò | Đầu ra |
|---|---|---|---|---|
| Backbone | 0–1 | Conv 3×3, bước 2 | Giảm kích thước nhanh | 64×160×160 |
| | 2–8 | C3k2 xen kẽ Conv bước 2 | Trích đặc trưng ở P3, P4, P5 | 512×20×20 |
| | 9 | SPPF | Gộp đặc trưng nhiều tỉ lệ bằng max-pooling lặp | 512×20×20 |
| | **10** | **C2PSA** | **Chú ý toàn cục trên P5. Đây là tầng mà đề tài thay thế** | 512×20×20 |
| Neck | 11–22 | Upsample, Concat, C3k2 | FPN đi xuống rồi PAN đi lên; riêng C3k2 ở tầng 22 có thêm khối PSA | P3 128×80×80, P4 256×40×40, P5 512×20×20 |
| Head | 23 | Segment26 | Hộp, lớp, 32 hệ số mặt nạ, Proto 32×160×160 | Tối đa 300 đối tượng |

C3k2 là khối tích chập kiểu CSP (chia kênh làm hai, một phần đi qua các khối nút cổ chai rồi ghép lại); SPPF áp dụng max-pooling 5×5 ba lần nối tiếp và ghép kết quả. **C2PSA** có cùng khuôn tách–xử lý–ghép, phần xử lý là khối PSA [20] gồm attention đa đầu và mạng truyền thẳng; ở cỡ *s*, C2PSA có 990.976 tham số.

### 2.4.2. Các bước của thuật toán YOLO26-seg

**Suy luận:**
1. **Tiền xử lý:** co ảnh cho cạnh dài bằng 640, giữ tỉ lệ, thêm viền thành bội số của 32 (letterbox), chia giá trị điểm ảnh cho 255.
2. **Backbone và neck:** trích đặc trưng qua tầng 0–10, trộn ba mức P3, P4, P5 theo FPN rồi PAN.
3. **Head:** tại mỗi điểm, đầu một-một dự đoán bốn khoảng cách tới cạnh hộp, điểm lớp và 32 hệ số mặt nạ; nhánh Proto26 sinh 32 mặt nạ mẫu.
4. **Chọn đối tượng:** lấy tối đa 300 dự đoán điểm cao nhất, bỏ dự đoán dưới ngưỡng tin cậy; không có NMS.
5. **Tạo mặt nạ:** tính theo (2.2), phóng về kích thước ảnh, nhị phân hóa ở 0,5, cắt theo hộp; trả về hộp, độ tin cậy, mặt nạ của từng đối tượng.

**Huấn luyện** mỗi lô ảnh:
1. **Tăng cường dữ liệu:** ghép bốn ảnh (Mosaic) [39], lật, co giãn, đổi màu; Mosaic tắt ở 10 epoch cuối.
2. **Lan truyền xuôi** qua cả hai đầu; đặc trưng vào đầu một-một được tách khỏi đồ thị gradient.
3. **Gán nhãn:** đầu một-nhiều lấy 10 điểm tốt nhất cho mỗi đối tượng, đầu một-một giữ 1 điểm; YOLO26 thêm quy tắc STAL nới kích thước vật rất nhỏ khi chọn ứng viên [6].
4. **Tính mất mát** hộp (CIoU và L1), lớp, mặt nạ và ngữ nghĩa phụ cho hai đầu; trọng số đầu một-nhiều giảm tuyến tính từ 0,8 xuống 0,1.
5. **Cập nhật trọng số** bằng AdamW [40] và cập nhật bản trung bình động (EMA); cuối mỗi epoch đánh giá trên tập kiểm định và lưu trọng số tốt nhất.

YOLO26 bỏ thành phần DFL của các phiên bản trước, hồi quy trực tiếp bốn khoảng cách kèm mất mát L1 [6]. **Ví dụ giải mã hộp:** điểm ở ô (cột 10, hàng 12) của P3 (bước 8 pixel) có tâm $\big((10 + 0{,}5)\times 8,\ (12 + 0{,}5)\times 8\big) = (84,\ 100)$; nếu bốn khoảng cách tới cạnh trái, trên, phải, dưới là $(2,\ 1,\ 3,\ 4)$ ô, tức $(16,\ 8,\ 24,\ 32)$ pixel, thì hộp bao là $(68,\ 92,\ 108,\ 132)$.

### 2.4.3. Ưu và nhược điểm

*Bảng 2.3. Ưu và nhược điểm của YOLO26-seg với bài toán phân đoạn polyp*

| Ưu điểm | Nhược điểm |
|---|---|
| Một lần suy luận cho cả hộp bao, độ tin cậy và mặt nạ | Mặt nạ mẫu chỉ có độ phân giải 160×160, có thể làm mất chi tiết biên của polyp nhỏ |
| Không cần NMS nên thời gian suy luận ổn định, dễ triển khai | Thiết kế cho dữ liệu tổng quát (COCO), chưa có thành phần riêng cho biên mờ |
| Có trọng số tiền huấn luyện trên COCO [41], giúp học nhanh với dữ liệu nhỏ | Attention chỉ có ở mức P5 (C2PSA ở tầng 10 và khối PSA trong tầng 22); các mức P3, P4 chỉ có tích chập |
| Thư viện Ultralytics [42] hoàn chỉnh: huấn luyện, đánh giá, xuất mô hình | Bài báo YOLO26 là bản tiền ấn phẩm, một số chi tiết chỉ có trong mã nguồn |
| Có nhiều cỡ mô hình (n, s, m, l, x) để cân đối tốc độ và độ chính xác | Mặt nạ bị cắt theo hộp, nên hộp sai thì mặt nạ cũng sai |

## 2.5. Cơ chế chú ý và chi phí tính toán

Cơ chế tự chú ý của Transformer [43] tính từ chuỗi $N$ vị trí ba ma trận truy vấn $Q$, khóa $K$, giá trị $V$, rồi:

$$ \mathrm{Attention}(Q, K, V) = \mathrm{softmax}\Big(\frac{QK^\top}{\sqrt{d}}\Big) V \tag{2.3} $$

Ma trận $QK^\top$ kích thước $N \times N$ cho biết mỗi vị trí chú ý đến vị trí khác bao nhiêu, nên chi phí tăng theo bình phương số vị trí: ở P5 (20×20) có $N^2 = 160.000$ cặp, nhưng ở P3 (80×80) đã khoảng 41 triệu cặp, gấp 256 lần. Vì vậy YOLO chỉ đặt attention ở P5. Mô hình không gian trạng thái là một hướng giữ tính toàn cục với chi phí tăng chậm hơn.

## 2.6. Mô hình không gian trạng thái, Mamba và VMamba

### 2.6.1. Mô hình không gian trạng thái và rời rạc hóa

Mô hình không gian trạng thái (SSM) mô tả hệ có trạng thái ẩn $h(t)$, tín hiệu vào $x(t)$ và ra $y(t)$:

$$ h'(t) = A\,h(t) + B\,x(t), \qquad y(t) = C\,h(t) \tag{2.4} $$

$A$ quyết định cách trạng thái nhớ và quên, $B$ cách đầu vào ghi vào trạng thái, $C$ cách đọc đầu ra. S4 [22] dùng $A$ dạng chéo cộng hạng thấp; S4D [44] đơn giản thành ma trận chéo phần tử âm, được Mamba và VMamba dùng. Với chuỗi rời rạc và bước thời gian $\Delta$, phép rời rạc hóa giữ nguyên trong mỗi bước (zero-order hold) cho:

$$ \bar A = \exp(\Delta A), \qquad \bar B = (\Delta A)^{-1}\big(\exp(\Delta A) - I\big)\,\Delta B \approx \Delta B \tag{2.5} $$

$$ h_t = \bar A\, h_{t-1} + \bar B\, x_t, \qquad y_t = C\, h_t \tag{2.6} $$

Mamba [23] và bản cài đặt của đề tài dùng xấp xỉ Euler $\bar B \approx \Delta B$. Vì $A$ âm nên $0 < \bar A < 1$: trạng thái mới bằng trạng thái cũ đã suy giảm cộng phần đầu vào mới; $\Delta$ lớn thì quên nhanh quá khứ. Ví dụ với $A = -1$, $B = C = 1$, $\Delta = 0{,}5$, chuỗi vào $(1,\ 0,\ 2)$: $\bar A \approx 0{,}607$, các trạng thái lần lượt là 0,500; 0,303; 1,184, tức thông tin cũ mờ dần khi không có đầu vào mới.

### 2.6.2. Mamba: SSM có chọn lọc

Mamba [23] cho $\Delta$, $B$, $C$ **phụ thuộc vào đầu vào** (tính từ $x_t$ qua phép chiếu, $\Delta_t = \mathrm{softplus}(\cdot) > 0$), nên mô hình tự quyết định giữ hay bỏ thông tin ở từng vị trí. Tiếp ví dụ ở mục 2.6.1: nếu ở bước 3 mô hình chọn $\Delta_3 = 2$ thì $\bar A_3 = e^{-2} \approx 0{,}135$, phần quá khứ gần như bị xóa; theo công thức ZOH, trọng số của đầu vào mới là $1 - e^{-2} \approx 0{,}865$, lớn hơn hẳn trường hợp $\Delta = 0{,}5$ (0,393), tức mô hình đã "chọn" tập trung vào đầu vào hiện tại. Khi đó phép truy hồi (2.6) phải tính tuần tự hoặc bằng **thuật toán quét song song** [45], [46]: mỗi bước có dạng $h_t = a_t h_{t-1} + b_t$, và hai bước liên tiếp gộp được thành một bước cùng dạng

$$ (a_1, b_1) \circ (a_2, b_2) = (a_2 a_1,\ a_2 b_1 + b_2) \tag{2.7} $$

Phép gộp có tính kết hợp nên gộp song song theo cây trong khoảng $\log_2 L$ vòng. Mamba gốc có kernel CUDA với chi phí tuyến tính; đề tài dùng biến thể Hillis–Steele [46] viết bằng PyTorch thuần, tổng công việc $O(L \log L)$.

### 2.6.3. VMamba và mô-đun SS2D

Ảnh không có thứ tự tự nhiên; trải ảnh theo một hướng thì mỗi vị trí chỉ thấy các vị trí đứng trước. VMamba [7] đề xuất **SS2D** với các bước trên bản đồ $C \times H \times W$:
1. **Chiếu vào:** tích chập 1×1 đưa $C$ kênh lên $2EC$ kênh, tách thành nhánh chính $U$ và nhánh cổng $Z$ ($E$ là hệ số mở rộng).
2. **Trộn cục bộ:** $U$ qua tích chập theo chiều sâu 3×3 và SiLU.
3. **Trải thành bốn chuỗi** dài $L = H \times W$: theo hàng, theo hàng đảo ngược, theo cột, theo cột đảo ngược.
4. **Quét chọn lọc:** với mỗi chuỗi, tính $\Delta_t, B_t, C_t$, rời rạc hóa theo (2.5) và chạy truy hồi (2.6).
5. **Gộp:** đưa bốn chuỗi về lưới $H \times W$ và cộng lại.
6. **Cổng và chiếu ra:** nhân với $\mathrm{SiLU}(Z)$, chiếu 1×1 về $C$ kênh.

**Ví dụ trên lưới 2×2** $\begin{bmatrix} a & b \\ c & d \end{bmatrix}$: bốn chuỗi là $a,b,c,d$; $d,c,b,a$; $a,c,b,d$; $d,b,c,a$. Ô $b$ nhận thông tin từ $a$ ở chuỗi thứ nhất, từ $d, c$ ở chuỗi thứ hai, từ $a, c$ ở chuỗi thứ ba và từ $d$ ở chuỗi thứ tư; sau khi cộng, $b$ đã nhận thông tin từ cả ba ô còn lại, điều mà một lần quét không làm được. Bản SS2D của đề tài là bản rút gọn ($E = 1$, không có hạng tử nhảy $D$ và LayerNorm đầu ra), trình bày ở Chương 3.

### 2.6.4. Ưu và nhược điểm của VMamba

*Bảng 2.4. Ưu và nhược điểm của VMamba*

| Ưu điểm | Nhược điểm |
|---|---|
| Mỗi vị trí nhận thông tin toàn ảnh sau một khối | Thứ tự quét cố định, không tự nhiên với ảnh; hai điểm gần nhau theo chiều dọc có thể cách xa nhau trong chuỗi quét hàng |
| Chi phí tăng gần tuyến tính theo số vị trí (với kernel tối ưu), rẻ hơn attention khi ảnh lớn | Ở bản đồ nhỏ như P5 ($L = 400$), lợi thế chi phí so với attention chưa rõ |
| Cơ chế chọn lọc cho phép giữ hay quên thông tin theo nội dung | Kernel tối ưu cần CUDA; bản PyTorch thuần chậm hơn nhiều |
| Có nhiều kết quả tốt trên ảnh y tế [24]–[26] | Huấn luyện từ đầu khó hơn; trọng số tiền huấn luyện ảnh hưởng lớn [25] |
| Không có ma trận $N \times N$ nên tiết kiệm bộ nhớ | Một số chi tiết (khởi tạo $\Delta$, chuẩn hóa đầu ra) nhạy với độ ổn định số |

## 2.7. Các độ đo đánh giá

### 2.7.1. Các đại lượng cơ bản

So sánh dự đoán với nhãn thật cho TP (dự đoán polyp, đúng là polyp), FP (dự đoán polyp nhưng không phải), FN (polyp bị bỏ sót) và TN (dự đoán nền, đúng là nền):

$$ \text{Precision} = \frac{TP}{TP + FP}, \qquad \text{Recall} = \frac{TP}{TP + FN}, \qquad F_1 = \frac{2\cdot\text{Precision}\cdot\text{Recall}}{\text{Precision} + \text{Recall}} \tag{2.8} $$

Trong nội soi, Recall thấp nghĩa là bỏ sót polyp. Các đại lượng tính được ở **mức điểm ảnh** (mỗi điểm ảnh là một mẫu, dùng khi so sánh mặt nạ) hoặc **mức đối tượng** (một dự đoán là TP khi IoU với polyp thật vượt ngưỡng; ở mức này TN không xác định được).

### 2.7.2. IoU và Dice

Với $G$ là tập điểm ảnh của nhãn thật và $P$ là tập điểm ảnh dự đoán:

$$ \text{IoU} = \frac{|P \cap G|}{|P \cup G|} = \frac{TP}{TP + FP + FN}, \qquad \text{Dice} = \frac{2|P \cap G|}{|P| + |G|} = \frac{2\,TP}{2\,TP + FP + FN} \tag{2.9} $$

Hai chỉ số liên hệ qua $\text{Dice} = 2\,\text{IoU}/(1 + \text{IoU})$; ở mức điểm ảnh, Dice trùng với F1.

**Ví dụ trên lưới 4×4** (1 là polyp):

$$ G = \begin{bmatrix} 0&1&1&0\\ 1&1&1&0\\ 1&1&1&0\\ 0&1&0&0 \end{bmatrix}, \qquad P = \begin{bmatrix} 0&1&1&1\\ 0&1&1&0\\ 1&1&1&0\\ 0&0&0&0 \end{bmatrix} $$

Có $TP = 7$, $FP = 1$, $FN = 2$, nên Precision = 7/8 = 0,875; Recall = 7/9 = 0,778; IoU = 7/10 = 0,700; Dice = 14/17 = 0,824 (khớp với $2 \times 0{,}7 / 1{,}7$). Khi đánh giá cả tập có thể lấy **trung bình theo ảnh** hoặc **gộp toàn tập** (cộng TP, FP, FN rồi mới tính); Chương 6 ghi rõ cách dùng.

### 2.7.3. AP, mAP50 và mAP50–95

Sắp xếp các dự đoán theo độ tin cậy giảm dần, tính Precision và Recall tích lũy được đường Precision–Recall; **AP** là diện tích dưới đường này sau khi làm đơn điệu [47]. Ví dụ tập có 3 polyp, 4 dự đoán xếp theo độ tin cậy là TP, FP, TP, TP: Precision đơn điệu bằng 1,0 trên đoạn Recall 0–1/3 và 0,75 trên đoạn 1/3–1, nên $AP = \tfrac{1}{3}\times 1{,}0 + \tfrac{2}{3}\times 0{,}75 \approx 0{,}833$.
- **mAP50:** AP tại ngưỡng IoU 0,5 (đề tài một lớp nên bằng AP50).
- **mAP50–95:** trung bình AP tại 10 ngưỡng IoU từ 0,50 đến 0,95, bước 0,05 [41]. Ở ngưỡng cao chỉ mặt nạ bám sát biên mới được tính đúng, nên chỉ số này phản ánh độ chính xác đường biên tốt hơn mAP50.

Khi IoU tính giữa hai **mặt nạ**, chỉ số gọi là *mask* mAP. Đề tài lấy **mask mAP50–95** làm độ đo chính.

### 2.7.4. Chi phí tính toán

- **Số tham số:** tích chập $k\times k$ từ $C_\text{in}$ sang $C_\text{out}$ kênh có $k^2 C_\text{in} C_\text{out}$ trọng số; ví dụ tầng đầu của YOLO26s-seg (3×3, 3 sang 32 kênh) có 864 trọng số.
- **FLOPs:** số phép tính dấu phẩy động cho một ảnh, một phép nhân–cộng tính là 2 FLOPs; tích chập trên lưới $H \times W$ cần khoảng $2 k^2 C_\text{in} C_\text{out} H W$ FLOPs.
- **Thời gian suy luận:** đo bằng mili giây, phụ thuộc phần cứng; phân biệt thời gian chỉ chạy mạng với thời gian toàn quy trình.

FLOPs không phản ánh đầy đủ tốc độ thực tế: một khối ít FLOPs nhưng gồm nhiều phép tính tuần tự, như phép quét SS2D, vẫn có thể chạy chậm.

## 2.8. So sánh hai mô hình qua nhiều lần huấn luyện

### 2.8.1. Vì sao cần nhiều seed

Khởi tạo trọng số, thứ tự đưa ảnh và tăng cường dữ liệu đều ngẫu nhiên, được điều khiển bằng **seed**; đổi seed có thể cho kết quả khác nhau đáng kể [31]. Đề tài huấn luyện mỗi mô hình với 20 seed giống nhau và **ghép cặp** theo seed: $d_i = \text{TSVM}_i - \text{Baseline}_i$, nhờ đó loại bỏ phần dao động chung ở cùng seed.

### 2.8.2. Kiểm định t ghép cặp

Với $n$ chênh lệch có trung bình $\bar d$ và độ lệch chuẩn $s_d$:

$$ t = \frac{\bar d}{s_d / \sqrt{n}} \tag{2.10} $$

Dưới giả thuyết không (kỳ vọng của $d$ bằng 0), $t$ có phân phối Student với $n-1$ bậc tự do [48]; $p < 0{,}05$ nghĩa là chênh lệch có ý nghĩa thống kê ở mức 5%. Khoảng tin cậy 95% của chênh lệch trung bình là

$$ \bar d \pm t_{0{,}975;\,n-1}\cdot \frac{s_d}{\sqrt n} \tag{2.11} $$

và nếu khoảng này chứa 0 thì chưa đủ cơ sở khẳng định mô hình nào tốt hơn.

### 2.8.3. Kiểm định Wilcoxon và cỡ hiệu ứng

**Kiểm định Wilcoxon dấu–hạng** [49] chỉ dùng thứ hạng của $|d_i|$ và dấu, không cần giả định phân phối chuẩn; Demšar [50] khuyến nghị dùng kiểm định này khi so sánh hai mô hình học máy. Giá trị $p$ không cho biết chênh lệch lớn hay nhỏ, nên đề tài báo thêm **cỡ hiệu ứng** Cohen $d_z$ cho dữ liệu ghép cặp:

$$ d_z = \frac{\bar d}{s_d} \tag{2.12} $$

Theo quy ước của Cohen (được Lakens [51] trình bày lại), $d_z$ khoảng 0,2 là nhỏ, 0,5 là vừa, 0,8 là lớn.

**Ví dụ (số tự đặt).** Năm seed cho chênh lệch $0{,}010;\ -0{,}004;\ 0{,}006;\ 0{,}002;\ 0{,}008$: $\bar d = 0{,}0044$, $s_d \approx 0{,}0055$, $t \approx 1{,}77$ ($p \approx 0{,}15$), Wilcoxon $W = 2$ ($p \approx 0{,}19$), khoảng tin cậy 95% là $[-0{,}0025;\ 0{,}0113]$ chứa 0, trong khi $d_z \approx 0{,}79$. Dù trung bình dương và cỡ hiệu ứng không nhỏ, **với ít cặp và dao động lớn giữa các seed, kết quả vẫn chưa có ý nghĩa thống kê**. Chương 6 dùng đúng các công cụ này.

## 2.9. Kết chương

Chương 2 đã trình bày các thành phần của YOLO26-seg (hai đầu dự đoán bỏ NMS, mặt nạ mẫu, các bước suy luận và huấn luyện), cơ chế chú ý và chi phí bậc hai, SSM, Mamba và mô-đun SS2D của VMamba, các độ đo và phương pháp so sánh ghép cặp qua nhiều seed. Chương 3 dựa trên các kiến thức này để trình bày khối C2TSVMamba.
