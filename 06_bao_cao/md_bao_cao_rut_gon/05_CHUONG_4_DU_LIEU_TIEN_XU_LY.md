# CHƯƠNG 4. XÂY DỰNG BỘ DỮ LIỆU VÀ TIỀN XỬ LÝ DỮ LIỆU

> **Ghi chú cho người biên tập (xóa khi ghép Word):**
> - Bản rút gọn, nén nhẹ từ `md_bao_cao/05_CHUONG_4_DU_LIEU_TIEN_XU_LY.md` (chương của bạn cùng nhóm, lấy từ `Tien_Xu_Ly_Du_Lieu_v3.docx`; tag git `ban_day_du_147`). Số liệu, công thức, bảng, hình và trích dẫn giữ nguyên.
> - **Các chỗ đã nén, cần báo người viết chương:** gộp hai đoạn 4.1.1; viết gọn lời giải thích của năm bước chuyển nhãn (4.3.1–4.3.5 thành "Bước 1–5") và mục 4.4; gộp ba đoạn mô tả phép tăng cường ở 4.5 thành gạch đầu dòng; gộp 4.6–4.8 thành mục 4.6; thu nhỏ Hình 4.2, 4.4, 4.5.
> - Ba chỗ sửa sự thật so với v3 (đã có ở bản đầy đủ): mục 4.2 danh sách chia do nhóm tác giả cung cấp; mục 4.1.2 "Kvasir phiên bản 2"; câu cuối trỏ "Chương 6". Hình 4.5 đã sửa ô cuối (29/10/2026).

Chương này trình bày cách xây dựng bộ dữ liệu BG20 từ hai nguồn ảnh nội soi công khai và các bước đưa ảnh cùng nhãn về dạng mô hình YOLO26-seg sử dụng được. Quá trình gồm giai đoạn chuẩn bị, thực hiện một lần trước khi huấn luyện (chọn ảnh, chia tập, chuyển mặt nạ thành nhãn đa giác), và giai đoạn nạp dữ liệu, diễn ra mỗi khi ảnh được đưa vào mô hình (đổi kích thước, tăng cường, chuẩn hóa).

## 4.1. Nguồn dữ liệu

### 4.1.1. Bộ dữ liệu Kvasir-SEG

Kvasir-SEG gồm 1.000 ảnh nội soi đường tiêu hóa có polyp, do Jha và cộng sự công bố năm 2020 [5]. Mỗi ảnh đi kèm một mặt nạ do kỹ sư và bác sĩ khoanh vùng, được bác sĩ chuyên khoa tiêu hóa kiểm tra lại; pixel thuộc polyp màu trắng, còn lại màu đen. Dữ liệu có ba đặc điểm cần xử lý: ảnh có 333 kích thước khác nhau, chiều rộng từ 332 đến 1.920 pixel; kích thước polyp chênh lệch lớn, vùng nhỏ nhất chỉ chiếm 0,15% diện tích ảnh, lớn nhất khoảng 81%, và khoảng 48% số vùng chiếm không quá 10%; ảnh và mặt nạ lưu ở định dạng nén JPEG [5], nên biên polyp có các mức xám trung gian và mặt nạ cần nhị phân hóa lại (mục 4.3).

### 4.1.2. Ảnh nền normal-cecum

Bộ dữ liệu Kvasir phiên bản 2 gồm 8 lớp ảnh, mỗi lớp 1.000 ảnh [5], [8]. Đề tài dùng lớp normal-cecum (ảnh manh tràng bình thường, 720 × 576 pixel) làm ảnh nền, tức mẫu âm tính không chứa polyp. Nếu chỉ học trên ảnh có polyp, mô hình dễ cho rằng ảnh nào cũng có polyp và khoanh nhầm nếp gấp hay vùng phản quang. Hình 4.1 minh họa hai nguồn dữ liệu.

![Hình 4.1](../hinh/chuong4/h4_1.png)

*Hình 4.1. Ví dụ ảnh có polyp, mặt nạ phân đoạn gốc và ảnh nền trong bộ dữ liệu BG20*

*Nguồn: ảnh a và b từ bộ dữ liệu Kvasir-SEG [5], ảnh c từ lớp normal-cecum của bộ dữ liệu Kvasir [8], đề tài ghép và đặt chú thích.*

## 4.2. Xây dựng và phân chia bộ dữ liệu BG20

Ảnh polyp được chia theo danh sách có sẵn gồm 880 ảnh huấn luyện và 120 ảnh kiểm định, do nhóm tác giả Kvasir-SEG cung cấp kèm bản phát hành trên Kaggle trong hai tệp train.txt và val.txt [53], giúp kết quả so sánh được với các nghiên cứu dùng cùng cách chia. Với ảnh nền, chương trình sắp xếp 1.000 tên tệp normal-cecum, cố định seed bằng 42 rồi chọn ngẫu nhiên 200 ảnh (160 huấn luyện, 40 kiểm định), nên mỗi lần chạy lại đều cho đúng 200 ảnh như nhau. Tên BG20 thể hiện số ảnh nền bằng 20% số ảnh polyp; tính trên toàn bộ 1.200 ảnh, ảnh nền chiếm 16,67%.

*Bảng 4.1. Phân bố ảnh và nhãn trong bộ dữ liệu BG20*

| Thành phần | Huấn luyện | Kiểm định | Tổng |
|---|---:|---:|---:|
| Ảnh có polyp | 880 | 120 | 1.000 |
| Ảnh nền normal-cecum | 160 | 40 | 200 |
| Tổng số ảnh | 1.040 | 160 | 1.200 |
| Số vùng polyp được gán nhãn | 936 | 127 | 1.063 |

*Nguồn: đề tài thống kê từ bộ dữ liệu BG20.*

Số vùng polyp lớn hơn số ảnh polyp vì một ảnh có thể chứa nhiều polyp tách rời, mỗi polyp một nhãn riêng. Bộ dữ liệu theo định dạng Ultralytics (hai thư mục images và labels, mỗi ảnh một tệp nhãn cùng tên), chỉ có một lớp polyp với chỉ số 0. Ảnh nền đi kèm tệp nhãn rỗng, nên ảnh nền không phải là một lớp thứ hai.

## 4.3. Chuyển mặt nạ phân đoạn thành nhãn đa giác

YOLO26-seg yêu cầu nhãn dạng văn bản: mỗi dòng gồm chỉ số lớp và tọa độ các đỉnh đa giác bao quanh đối tượng, chuẩn hóa về đoạn 0–1 [42]. Đề tài chuyển mỗi mặt nạ thành nhãn đa giác qua năm bước bằng thư viện OpenCV; ảnh nội soi giữ nguyên.

**Bước 1. Nhị phân hóa bằng phương pháp Otsu.** Do nén JPEG, mặt nạ có thêm mức xám trung gian (mặt nạ ở Hình 4.2 có 15 mức xám). Phương pháp Otsu [54] chọn ngưỡng $t$ tự động, giữ ngưỡng làm phương sai giữa nhóm tối và nhóm sáng lớn nhất:

$$\sigma_B^2(t) = \omega_0(t)\,\omega_1(t)\,\left[\mu_0(t) - \mu_1(t)\right]^2 \tag{4.1}$$

$$t^* = \underset{0 \le t \le 255}{\arg\max}\; \sigma_B^2(t) \tag{4.2}$$

Trong đó $\omega_0, \omega_1$ là tỷ lệ số pixel và $\mu_0, \mu_1$ là mức xám trung bình của nhóm tối và nhóm sáng. Trên 1.000 mặt nạ, $t^*$ chỉ nằm trong khoảng 5 đến 8: mặt nạ gốc gần như đã nhị phân, bước Otsu chủ yếu loại nhiễu do nén.

**Bước 2. Làm liền vùng polyp bằng phép đóng hình thái học** [52], với $A$ là tập pixel trắng và $B$ là phần tử cấu trúc vuông 3 × 3:

$$A \bullet B = (A \oplus B) \ominus B \tag{4.3}$$

Phép giãn nở $\oplus$ làm vùng trắng phình ra một pixel để lấp lỗ và khe, phép co $\ominus$ thu lại một pixel để biên trở về gần vị trí cũ.

**Bước 3. Tìm đường bao và loại vùng nhiễu nhỏ** bằng thuật toán dò biên của Suzuki và Abe [55], chỉ lấy đường bao ngoài cùng của mỗi vùng; đường bao có diện tích nhỏ hơn 20 pixel vuông bị loại. Trên 1.000 mặt nạ, chương trình tìm được 1.206 đường bao, loại 143, còn đúng 1.063 vùng polyp như Bảng 4.1.

**Bước 4. Đơn giản hóa đường bao** bằng thuật toán Douglas–Peucker [56], chỉ giữ những điểm lệch khỏi đoạn thẳng nối hai đầu nhiều hơn ngưỡng

$$\varepsilon = 0{,}002 \cdot L \tag{4.4}$$

với $L$ là chu vi đường bao (pixel); ví dụ chu vi 1.000 pixel cho $\varepsilon$ bằng 2 pixel. Số điểm trung bình mỗi đa giác giảm từ 333,2 xuống 24,6 (giảm 92,6%), mỗi đa giác có từ 10 đến 80 đỉnh.

**Bước 5. Chuẩn hóa tọa độ và ghi tệp nhãn:**

$$\hat{x} = \frac{x}{W}, \qquad \hat{y} = \frac{y}{H} \tag{4.5}$$

Giá trị làm tròn đến 6 chữ số thập phân; mỗi polyp ghi thành một dòng gồm chỉ số lớp và các cặp tọa độ. Nhờ chuẩn hóa, nhãn không phụ thuộc kích thước ảnh. Hình 4.2 minh họa: đường bao ở ảnh c gồm 377 điểm, sau khi đơn giản hóa đa giác ở ảnh d chỉ còn 21 đỉnh nhưng vẫn giữ được hình dạng polyp.

![Hình 4.2](../hinh/chuong4/h4_2.png){width=11cm}

*Hình 4.2. Trước và sau khi chuyển mặt nạ phân đoạn thành nhãn đa giác*

*Nguồn: ảnh a và b từ bộ dữ liệu Kvasir-SEG [5], ảnh c và d do đề tài tạo bằng chương trình chuyển đổi mặt nạ của đề tài.*

## 4.4. Đổi kích thước ảnh

Mô hình dùng kích thước đầu vào 640 pixel. Để polyp không bị méo, ảnh được thu phóng giữ tỷ lệ sao cho cạnh dài nhất bằng 640:

$$r = \frac{640}{\max(W, H)} \tag{4.6}$$

$$W' = \lceil r \cdot W \rceil, \qquad H' = \lceil r \cdot H \rceil \tag{4.7}$$

Phần thiếu của cạnh ngắn được bù bằng LetterBox: ảnh đặt giữa khung đích, phần trống tô xám 114 và chia đều hai phía:

$$p_x = \frac{640 - W'}{2}, \qquad p_y = \frac{640 - H'}{2} \tag{4.8}$$

Tọa độ đa giác cũng được nhân với $r$ và cộng $p_x$, $p_y$. Ở nhánh huấn luyện, khung đích là 640 × 640; ở nhánh kiểm định, các ảnh có tỷ lệ khung gần nhau được gom thành lô 16 ảnh, khung mỗi lô làm tròn lên bội số của 32 và cộng thêm nửa bước, nên có cạnh dài 672 pixel. Ví dụ ở Hình 4.3, ảnh gốc 1.920 × 1.072 pixel thu còn 640 × 358 pixel, thêm hai dải xám cao 141 pixel ở trên và dưới.

![Hình 4.3](../hinh/chuong4/h4_3.png)

*Hình 4.3. Trước và sau khi đổi kích thước ảnh bằng thu phóng giữ tỷ lệ và LetterBox*

*Nguồn: ảnh a từ bộ dữ liệu Kvasir-SEG [5], ảnh b do đề tài tạo theo cách xử lý LetterBox trong mã nguồn Ultralytics.*

## 4.5. Tăng cường dữ liệu

Tập huấn luyện chỉ có 1.040 ảnh, nên mô hình dễ ghi nhớ từng ảnh. Tăng cường dữ liệu tạo một biến thể ngẫu nhiên khác nhau mỗi lần ảnh được nạp, chỉ áp dụng cho tập huấn luyện. Nhóm phép hình học thay đổi vị trí pixel nên đa giác nhãn biến đổi theo; nhóm phép màu giữ nguyên nhãn (Bảng 4.2).
- **Mosaic** [39] ghép bốn ảnh vào bốn góc quanh một tâm ngẫu nhiên rồi cắt về 640 × 640, tạo polyp ở nhiều vị trí và kích thước; vì ảnh ghép không giống ảnh nội soi thật, Mosaic được tắt trong 10 epoch cuối [42].
- **Affine:** dịch tâm lệch tối đa 10% khung, thu phóng hệ số 0,5 đến 1,5; phần trống tô xám 114.
- **Màu HSV:** gần như giữ nguyên sắc độ để màu niêm mạc không phi thực tế, nhưng thay đổi mạnh độ bão hòa và độ sáng để mô phỏng điều kiện chiếu sáng.
- **Lật ngang** với xác suất 0,5. Lật dọc, xoay, cắt xiên và trộn ảnh không được sử dụng.

*Bảng 4.2. Thông số tăng cường dữ liệu trong cấu hình huấn luyện*

| Phép biến đổi | Tham số | Giá trị | Ý nghĩa |
|---|---|---:|---|
| Mosaic | mosaic | 1,0 | Luôn ghép bốn ảnh |
| Tắt Mosaic | close_mosaic | 10 | Tắt trong 10 epoch cuối |
| Dịch chuyển | translate | 0,1 | Lệch tối đa 10% khung |
| Thu phóng | scale | 0,5 | Hệ số từ 0,5 đến 1,5 |
| Sắc độ | hsv_h | 0,015 | Dịch sắc độ rất nhẹ |
| Độ bão hòa | hsv_s | 0,7 | Thay đổi tối đa 70% |
| Độ sáng | hsv_v | 0,4 | Thay đổi tối đa 40% |
| Lật ngang | fliplr | 0,5 | Xác suất 50% |
| Lật dọc, xoay, cắt xiên, phối cảnh | flipud, degrees, shear, perspective | 0 | Không sử dụng |
| Trộn ảnh | mixup, cutmix, copy_paste | 0 | Không sử dụng |

*Nguồn: tệp cấu hình huấn luyện của đề tài.*

Hình 4.4 minh họa từng phép tăng cường trên cùng một ảnh huấn luyện (hệ số chọn cố định trong phạm vi Bảng 4.2); ở cả sáu trường hợp, đường bao luôn khớp với polyp.

![Hình 4.4](../hinh/chuong4/h4_4.png){width=11cm}

*Hình 4.4. Ảnh huấn luyện trước và sau các phép tăng cường dữ liệu*

*Nguồn: ảnh gốc từ bộ dữ liệu Kvasir-SEG [5] và Kvasir [8], các phép biến đổi do đề tài tạo minh họa theo thông số trong Bảng 4.2.*

## 4.6. Chuẩn hóa, kiểm tra toàn vẹn và tổng hợp quy trình

**Chuẩn hóa.** Ảnh được đổi kênh màu từ BGR sang RGB, sắp lại chiều thành kênh × cao × rộng, ghép thành lô 8 ảnh và chia giá trị pixel cho 255 (không trừ trung bình hay chia độ lệch chuẩn của ImageNet). Đa giác được tô đầy để tạo lại mặt nạ huấn luyện 160 × 160, nhỏ hơn ảnh 4 lần; với ảnh nền, mặt nạ chỉ gồm giá trị 0.

**Kiểm tra toàn vẹn.** Chương trình chuyển đổi tự kiểm tra số ảnh và số tệp nhãn của từng tập. Lượt kiểm tra độc lập cho thấy mỗi ảnh có đúng một tệp nhãn, cả 1.063 dòng nhãn hợp lệ, không có ảnh trùng tên hoặc trùng nội dung theo mã băm SHA-256 giữa hai tập. Chạy lại bằng OpenCV 5.0.0, cả 1.000 tệp nhãn trùng khớp từng ký tự, và bước chọn ảnh nền với seed 42 cho đúng danh sách đã lưu. Giới hạn: dữ liệu không có thông tin định danh bệnh nhân nên chưa khẳng định được hai tập không chứa ảnh của cùng bệnh nhân; mã băm chưa phát hiện ảnh gần giống nhau; không có tập kiểm thử độc lập.

**Tổng hợp.** Hình 4.5 tóm tắt quy trình: phần trên là giai đoạn chuẩn bị (một lần), phần dưới là giai đoạn nạp dữ liệu với nhánh huấn luyện có tăng cường và nhánh kiểm định chỉ đổi kích thước bằng LetterBox, cả hai kết thúc bằng bước chuẩn hóa.

![Hình 4.5](../hinh/chuong4/h4_5.png){width=12cm}

*Hình 4.5. Quy trình xây dựng bộ dữ liệu BG20 và tiền xử lý dữ liệu*

*Nguồn: đề tài tự xây dựng.*

Khối TSVM nằm bên trong mô hình và chỉ xử lý đặc trưng sau khi ảnh đã được chuẩn hóa. Hai mô hình dùng chung quy trình tiền xử lý, nên dữ liệu không phải nguồn tạo ra khác biệt giữa chúng; dao động giữa các lần huấn luyện được kiểm soát bằng 20 seed ghép cặp ở Chương 6.
