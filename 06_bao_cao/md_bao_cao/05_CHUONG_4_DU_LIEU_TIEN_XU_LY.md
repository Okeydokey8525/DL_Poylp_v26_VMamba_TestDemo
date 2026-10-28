<!--
BẢN DÙNG ĐỂ GÓP Ý — chương 4 do thành viên nhóm phụ trách tiền xử lý dữ liệu viết.
Nguồn: 06_bao_cao/Tien_Xu_Ly_Du_Lieu.docx, chép nguyên văn; chỉ đổi số mục/hình/bảng/công thức từ 3.x sang 4.x.
Kiểm định chi tiết: 06_bao_cao/md_bao_cao/_KIEM_TRA/A_gop_y_chuong_4_du_lieu.md
-->

> **Cách đọc bản góp ý này**
>
> - Lời văn là **nguyên văn** của tác giả chương; chỉ đổi số 3.x → 4.x.
> - ~~Câu bị gạch~~ là câu **sai**, ngay sau đó có ô ❌ ghi lý do, câu đề xuất sửa và bằng chứng.
> - Ô ⚠️ **CHƯA CHÍNH XÁC**: câu đúng một phần, cần chỉnh lại như đề xuất.
> - Ô ❓ **CẦN XÁC NHẬN**: chưa có bằng chứng hoặc cần tác giả bổ sung thông tin.
> - Các câu không có ô góp ý là **đã kiểm tra và đúng** (79/94 nhận định), xem bảng tổng kết ở cuối file.

# CHƯƠNG 4. XÂY DỰNG BỘ DỮ LIỆU VÀ TIỀN XỬ LÝ DỮ LIỆU

Chất lượng của dữ liệu đầu vào ảnh hưởng trực tiếp đến khả năng học của mô hình phân đoạn. Chương này trình bày cách đề tài xây dựng bộ dữ liệu BG20 từ hai nguồn ảnh nội soi công khai và các bước xử lý giúp đưa ảnh cùng nhãn về dạng mà mô hình YOLO26-seg tích hợp khối TSVM có thể sử dụng được.

Quá trình tiền xử lý được chia thành hai giai đoạn. Giai đoạn thứ nhất chỉ thực hiện một lần trước khi huấn luyện, gồm chọn ảnh, chia tập dữ liệu và chuyển mặt nạ phân đoạn thành nhãn đa giác. Giai đoạn thứ hai diễn ra mỗi khi ảnh được nạp vào mô hình, gồm đổi kích thước, tăng cường dữ liệu và chuẩn hóa giá trị đầu vào. Các thao tác và thông số trong chương đều được đối chiếu với mã nguồn, tệp cấu hình huấn luyện và dữ liệu thực tế của đề tài.

## 4.1. Nguồn dữ liệu

### 4.1.1. Bộ dữ liệu Kvasir-SEG

Kvasir-SEG là bộ dữ liệu công khai gồm 1.000 ảnh nội soi đường tiêu hóa có polyp, được Jha và cộng sự công bố năm 2020 [1]. Các ảnh này được lấy từ lớp polyp của bộ dữ liệu Kvasir [2]. Với mỗi ảnh, một nhóm gồm kỹ sư và bác sĩ đã khoanh vùng polyp bằng công cụ gán nhãn Labelbox, sau đó một bác sĩ chuyên khoa tiêu hóa giàu kinh nghiệm kiểm tra lại kết quả [1]. Vùng được khoanh được lưu thành một ảnh mặt nạ cùng tên với ảnh gốc, trong đó các pixel thuộc polyp có màu trắng và các pixel còn lại có màu đen.

Khi kiểm tra trực tiếp 1.000 ảnh, đề tài nhận thấy kích thước ảnh không đồng nhất. Bộ dữ liệu có 333 kích thước khác nhau, chiều rộng thay đổi từ 332 đến 1.920 pixel và chiều cao từ 352 đến 1.072 pixel, phổ biến nhất là các ảnh có kích thước xấp xỉ 622 × 530 pixel. Kích thước polyp cũng chênh lệch rất lớn: vùng polyp nhỏ nhất chỉ chiếm khoảng 0,15% diện tích ảnh, vùng lớn nhất chiếm khoảng 81% và một nửa số vùng polyp chiếm không quá 10% diện tích ảnh. Một số ảnh còn có chữ hiển thị thông tin ca nội soi hoặc ô hình nhỏ của hệ thống ScopeGuide thể hiện vị trí ống soi [1]. Những đặc điểm này cho thấy dữ liệu cần được đưa về một kích thước chung và mô hình cần học được polyp ở nhiều kích cỡ khác nhau.

> ⚠️ **CHƯA CHÍNH XÁC**: Trung vị diện tích là 10,27%; chỉ 513/1.063 vùng (48,3%) chiếm không quá 10%. **Đề xuất:** "khoảng một nửa số vùng (48%) chiếm không quá 10% diện tích ảnh, trung vị xấp xỉ 10,3%". Các số 0,15% và 81% là đúng.
>
> 🔎 *Bằng chứng:* đo lại trên 1.063 polygon nhãn của BG20 (báo cáo kiểm định A, mục #11).

Ngoài ra, cả ảnh và mặt nạ đều được lưu ở định dạng nén JPEG [1]. Phép nén này làm xuất hiện một số pixel có mức xám trung gian dọc theo ranh giới giữa vùng trắng và vùng đen, nên mặt nạ không còn hoàn toàn chỉ gồm hai giá trị. Đây là lý do mặt nạ cần được nhị phân hóa lại trước khi chuyển thành nhãn, như trình bày ở mục 4.3.

### 4.1.2. Ảnh nền normal-cecum

Bộ dữ liệu Kvasir gồm 8 lớp ảnh, mỗi lớp 1.000 ảnh, bao gồm các mốc giải phẫu, các phát hiện bệnh lý và các thủ thuật nội soi [1], [2]. Đề tài sử dụng lớp normal-cecum, tức ảnh chụp manh tràng bình thường, làm nguồn ảnh nền. Manh tràng là đoạn đầu của đại tràng và là mốc giải phẫu mà bác sĩ thường phải quan sát trong quá trình nội soi. Các ảnh thuộc lớp này không chứa polyp và đều có kích thước 720 × 576 pixel.

> ⚠️ **CHƯA CHÍNH XÁC**: Con số 8 lớp × 1.000 ảnh là của **Kvasir phiên bản 2** (8.000 ảnh), được xác nhận trong bài [1]. Bài [2] (MMSys'17) mô tả bản đầu của Kvasir. **Đề xuất:** ghi "Kvasir v2 (8 lớp, mỗi lớp 1.000 ảnh) [1]" và dùng [2] để dẫn nguồn gốc bộ dữ liệu. Thư mục normal-cecum có đúng 1.000 ảnh, đều 720 × 576 (đã đếm).
>
> 🔎 *Bằng chứng:* bài [1] mục 3.1; thư mục `01_du_lieu/tao_BG20/normal-cecum/`.

Ảnh nền đóng vai trò là mẫu âm tính. Nếu mô hình chỉ được huấn luyện trên ảnh có polyp, nó có xu hướng cho rằng ảnh nào cũng chứa polyp và dễ khoanh nhầm các nếp gấp hay vùng phản quang trên niêm mạc bình thường, gây ra báo động giả. Việc bổ sung ảnh không có polyp giúp mô hình học được trường hợp không có đối tượng nào cần phân đoạn. Hình 4.1 minh họa một ảnh polyp, mặt nạ tương ứng và một ảnh nền được sử dụng trong đề tài.

> ❓ **CẦN XÁC NHẬN**: Đây là lập luận về động cơ; đề tài **không có thí nghiệm** so sánh huấn luyện có và không có ảnh nền, nên chưa chứng minh được ảnh nền làm giảm báo động giả. **Đề xuất** viết thận trọng: "Việc bổ sung ảnh không có polyp **nhằm giúp** mô hình học…".

![](../hinh/chuong4/h4_1.png)

*Hình 4.1. Ví dụ ảnh có polyp, mặt nạ phân đoạn gốc và ảnh nền trong bộ dữ liệu BG20*

*Nguồn: ảnh a và b từ bộ dữ liệu Kvasir-SEG [1], ảnh c từ lớp normal-cecum của bộ dữ liệu Kvasir [2]; đề tài ghép và đặt chú thích.*

Trong Hình 4.1, ảnh a và mặt nạ b có cùng kích thước, vùng trắng của mặt nạ trùng khớp với vị trí polyp trên ảnh. Ảnh c là ảnh manh tràng bình thường, góc dưới bên trái có ô hình ScopeGuide. Ảnh nền không có mặt nạ đi kèm vì không có vùng nào cần phân đoạn.

## 4.2. Xây dựng và phân chia bộ dữ liệu BG20

Ảnh polyp được chia theo danh sách có sẵn gồm 880 ảnh huấn luyện và 120 ảnh kiểm định do nhóm tác giả Kvasir-SEG cung cấp trong hai tệp train.txt và val.txt [3]. Việc dùng danh sách có sẵn thay vì tự chia ngẫu nhiên giúp kết quả của đề tài có thể so sánh với các nghiên cứu khác dùng cùng cách chia, đồng thời bảo đảm không có ảnh nào xuất hiện ở cả hai tập.

> ✅ **ĐÚNG** (kiểm lại 27/10/2026, gỡ nhận xét ❌ trước đó): Bản Kvasir-SEG do D. Jha (tác giả đầu của Kvasir-SEG) đăng trên Kaggle [3] có sẵn `train.txt`, `val.txt` và tệp README ghi *"We have provided train-val split for the fair comparison of the model"*. Ở máy nhóm, ba tệp này nằm trong `DeepLearning/Dataset/Kvasir-SEG_data/`, ngày tệp 22/02/2024. `01_du_lieu/train.txt` và `val.txt` trùng từng byte với hai tệp này (cùng md5). Script tiền xử lý chỉ **đọc** hai danh sách (`train_txt_path = base_dir / "train.txt"`), không tự chia. Nhận xét ❌ trước đây sai vì chỉ xem thư mục con `Kvasir-SEG/` (images, masks, bbox) và trang Simula, không xem thư mục ngoài chứa tệp chia.
>
> **Gợi ý nhỏ (không bắt buộc):** có thể thêm một câu nguồn: "Hai danh sách được phân phối kèm bản Kvasir-SEG trên Kaggle của tác giả [3]; trang chính thức của Simula chỉ cung cấp ảnh và mặt nạ."
>
> 🔎 *Bằng chứng:* `01_du_lieu/train.txt` (880 dòng), `01_du_lieu/val.txt` (120 dòng), không giao nhau (`00_tai_lieu_tong_quan/bang/00_kiem_tra_du_lieu.json`); md5 `train.txt` = `ebf7ac9d90bda36353f12366a095007b` ở cả `Dataset/Kvasir-SEG_data/` và `01_du_lieu/`.

Đối với ảnh nền, chương trình sắp xếp 1.000 tên tệp normal-cecum theo thứ tự, cố định hạt giống ngẫu nhiên seed bằng 42 rồi chọn ngẫu nhiên 200 ảnh. Trong đó, 160 ảnh đầu tiên được đưa vào tập huấn luyện và 40 ảnh còn lại được đưa vào tập kiểm định. Nhờ sắp xếp danh sách trước khi chọn và cố định seed, mỗi lần chạy lại chương trình đều cho ra đúng 200 ảnh như nhau. Danh sách ảnh được chọn cũng được lưu lại thành hai tệp văn bản để đối chiếu về sau.

Tên gọi BG20 thể hiện số ảnh nền bằng 20% của 1.000 ảnh polyp gốc. Cần lưu ý rằng khi tính trên toàn bộ 1.200 ảnh, ảnh nền chỉ chiếm 16,67%; tỷ lệ này là 15,38% trong tập huấn luyện và 25% trong tập kiểm định. Phân bố cuối cùng của bộ dữ liệu được tổng hợp trong Bảng 4.1.

*Bảng 4.1. Phân bố ảnh và nhãn trong bộ dữ liệu BG20*

| **Thành phần** | **Huấn luyện** | **Kiểm định** | **Tổng** |
|---|---|---|---|
| Ảnh có polyp | 880 | 120 | 1.000 |
| Ảnh nền normal-cecum | 160 | 40 | 200 |
| Tổng số ảnh | 1.040 | 160 | 1.200 |
| Số vùng polyp được gán nhãn | 936 | 127 | 1.063 |

*Nguồn: đề tài thống kê từ bộ dữ liệu BG20.*

Số vùng polyp lớn hơn số ảnh polyp vì một ảnh có thể chứa nhiều polyp tách rời nhau, mỗi polyp được gán một nhãn riêng. Chẳng hạn, 120 ảnh polyp của tập kiểm định chứa tổng cộng 127 vùng polyp.

Bộ dữ liệu được tổ chức theo định dạng của thư viện Ultralytics. Thư mục images chứa ảnh và thư mục labels chứa nhãn, mỗi thư mục chia tiếp thành train và val. Mỗi ảnh có một tệp nhãn dạng văn bản cùng tên. Tệp cấu hình YAML khai báo đường dẫn dữ liệu và một lớp duy nhất là polyp với chỉ số 0. Ảnh nền được thêm tiền tố bg_ vào tên tệp để tránh trùng tên và đi kèm một tệp nhãn rỗng có dung lượng 0 byte. Tệp nhãn rỗng cho mô hình biết ảnh không chứa polyp nào, vì vậy ảnh nền không phải là một lớp đối tượng thứ hai.

## 4.3. Chuyển mặt nạ phân đoạn thành nhãn đa giác

Mặt nạ của Kvasir-SEG là một ảnh, mỗi pixel cho biết vị trí đó có thuộc polyp hay không. Trong khi đó, YOLO26-seg yêu cầu nhãn ở dạng văn bản: mỗi dòng mô tả một đối tượng, gồm chỉ số lớp và dãy tọa độ các đỉnh của đa giác bao quanh đối tượng, các tọa độ được chuẩn hóa về đoạn từ 0 đến 1 [4]. Vì vậy, đề tài chuyển mỗi mặt nạ thành nhãn đa giác qua năm bước dưới đây, sử dụng các hàm xử lý ảnh của thư viện OpenCV [5]. Công đoạn này chỉ tác động lên mặt nạ, còn ảnh nội soi được sao chép nguyên vẹn sang bộ dữ liệu mới.

### 4.3.1. Nhị phân hóa mặt nạ bằng phương pháp Otsu

Đầu tiên, mặt nạ được đọc và chuyển thành ảnh xám, mỗi pixel có giá trị từ 0 đến 255. Do ảnh hưởng của nén JPEG đã nêu ở mục 4.1.1, mặt nạ không chỉ có hai giá trị 0 và 255; ví dụ, mặt nạ dùng trong Hình 4.2 có 15 mức xám khác nhau. Nhị phân hóa là việc chọn một ngưỡng *t*: pixel có giá trị lớn hơn *t* được gán thành 255 và thuộc polyp, các pixel còn lại được gán thành 0.

Phương pháp Otsu [6] chọn ngưỡng này một cách tự động. Thuật toán thử lần lượt mọi ngưỡng có thể, mỗi ngưỡng chia các pixel thành nhóm tối và nhóm sáng, rồi giữ lại ngưỡng làm hai nhóm tách biệt nhau rõ nhất. Mức độ tách biệt được đo bằng phương sai giữa hai nhóm:

$$
{\sigma }_{B}^{2}(t)={\omega }_{0}(t)\cdot {\omega }_{1}(t)\cdot {[{\mu }_{0}(t)-{\mu }_{1}(t)]}^{2} \tag{4.1}
$$

$$
{t}^{*}=\mathrm{arg} \mathrm{max}_{0\le t\le 255}{\sigma }_{B}^{2}(t) \tag{4.2}
$$

Trong đó, *ω*<sub>0</sub> và *ω*<sub>1</sub> là tỷ lệ số pixel thuộc nhóm tối và nhóm sáng; *μ*<sub>0</sub> và *μ*<sub>1</sub> là mức xám trung bình của hai nhóm. Ngưỡng tối ưu *t*<sup>*</sup> là ngưỡng làm cho phương sai giữa hai nhóm đạt giá trị lớn nhất. Trên 1.000 mặt nạ của đề tài, ngưỡng Otsu chỉ nằm trong khoảng từ 5 đến 8. Điều này cho thấy mặt nạ gốc gần như đã nhị phân, và bước Otsu chủ yếu loại bỏ các pixel nhiễu do nén ảnh tạo ra.

### 4.3.2. Làm liền vùng polyp bằng phép đóng hình thái học

Sau khi nhị phân hóa, trên mặt nạ có thể còn những lỗ đen rất nhỏ bên trong vùng polyp hoặc những khe hở mảnh trên đường biên. Đề tài sử dụng phép đóng, còn gọi là Closing, thuộc nhóm phép toán hình thái học [7] để làm liền các chỗ này. Phép đóng gồm hai bước liên tiếp:

$$
A\bullet B=(A\oplus B)\ominus B \tag{4.3}
$$

Trong đó, *A* là tập các pixel trắng của mặt nạ và *B* là phần tử cấu trúc, ở đây là một hình vuông kích thước 3 × 3 pixel. Phép giãn nở, ký hiệu ⊕, làm vùng trắng phình ra thêm một pixel về mọi phía nên các lỗ và khe nhỏ bị lấp kín. Phép co, ký hiệu ⊖, sau đó thu vùng trắng lại một pixel để đường biên trở về gần vị trí ban đầu. Kết quả là vùng polyp liền mạch hơn nhưng kích thước gần như không thay đổi. Phép đóng chỉ được áp dụng một lần với phần tử cấu trúc nhỏ để tránh làm sai lệch hình dạng polyp.

### 4.3.3. Tìm đường bao và loại bỏ vùng nhiễu nhỏ

Đường bao là chuỗi các điểm nằm trên ranh giới của một vùng trắng. OpenCV tìm đường bao dựa trên thuật toán dò biên của Suzuki và Abe [8]. Đề tài chỉ lấy đường bao ngoài cùng của mỗi vùng, vì nhãn YOLO mô tả mỗi đối tượng bằng đúng một đa giác khép kín. Khi lưu đường bao, các đoạn thẳng nằm ngang, dọc hoặc chéo chỉ được giữ lại điểm đầu và điểm cuối nhằm giảm bớt số điểm không cần thiết.

Tiếp theo, mọi đường bao có diện tích nhỏ hơn 20 pixel vuông đều bị loại bỏ. Những vùng nhỏ như vậy thường là các đốm nhiễu, nếu giữ lại sẽ khiến mô hình học những đối tượng không có thật. Trên toàn bộ 1.000 mặt nạ, chương trình tìm được 1.206 đường bao, trong đó 143 đường bao bị loại do quá nhỏ, còn lại đúng 1.063 vùng polyp như trong Bảng 4.1.

### 4.3.4. Đơn giản hóa đường bao

Đường bao thu được bám theo từng pixel trên biên nên có rất nhiều điểm, trung bình khoảng 333 điểm cho mỗi polyp. Để nhãn gọn hơn, đề tài dùng thuật toán Douglas–Peucker [9]. Thuật toán bắt đầu bằng đoạn thẳng nối hai đầu của đường cong, sau đó tìm điểm nằm xa đoạn thẳng này nhất. Nếu khoảng cách lớn hơn ngưỡng sai số *ε*, điểm đó được giữ lại và quá trình lặp lại cho hai nửa đường cong; ngược lại, mọi điểm ở giữa đều bị bỏ đi. Ngưỡng sai số được tính theo chu vi của đường bao:

$$
\varepsilon =0,002\cdot L \tag{4.4}
$$

Trong đó, *L* là chu vi đường bao tính bằng pixel. Ví dụ, một polyp có chu vi 1.000 pixel sẽ có *ε* bằng 2 pixel, nghĩa là đa giác sau khi rút gọn lệch khỏi đường bao ban đầu không quá 2 pixel. Cách tính theo chu vi giúp polyp lớn và polyp nhỏ được rút gọn với mức độ tương xứng. Nếu đa giác thu được có ít hơn 3 đỉnh, chương trình giữ lại đường bao ban đầu. Kết quả, số điểm trung bình của mỗi đa giác giảm từ 333,2 xuống còn 24,6 điểm, tức giảm 92,6%, và mỗi đa giác có từ 10 đến 80 đỉnh.

### 4.3.5. Chuẩn hóa tọa độ và ghi tệp nhãn

Cuối cùng, tọa độ mỗi đỉnh được chia cho chiều rộng *W* và chiều cao *H* của mặt nạ để đưa về đoạn từ 0 đến 1:

$$
\hat{x}=\frac{x}{W},  \hat{y}=\frac{y}{H} \tag{4.5}
$$

Giá trị sau chuẩn hóa được giới hạn trong đoạn từ 0 đến 1 và làm tròn đến 6 chữ số thập phân. Mỗi polyp được ghi thành một dòng trong tệp nhãn theo cấu trúc: chỉ số lớp, sau đó là lần lượt các cặp tọa độ x̂ và ŷ của từng đỉnh. Ví dụ, dòng nhãn của ảnh trong Hình 4.2 bắt đầu bằng 0 0.321027 0.000000 0.292135 0.041667 và tiếp tục cho đến hết 21 đỉnh. Nhờ chuẩn hóa, nhãn không phụ thuộc vào kích thước ảnh, nên khi ảnh được phóng to hay thu nhỏ ở các bước sau, đa giác vẫn khớp đúng vị trí polyp.

Hình 4.2 minh họa toàn bộ công đoạn chuyển đổi trên một ảnh thuộc tập huấn luyện, từ mặt nạ gốc đến đa giác cuối cùng.

![](../hinh/chuong4/h4_2.png)

*Hình 4.2. Trước và sau khi chuyển mặt nạ phân đoạn thành nhãn đa giác*

*Nguồn: ảnh a và b từ bộ dữ liệu Kvasir-SEG [1]; ảnh c và d do đề tài tạo bằng chương trình chuyển đổi mặt nạ của đề tài.*

Ảnh b là mặt nạ gốc trước khi xử lý. Sau các bước Otsu, phép đóng và tìm đường bao, ảnh c cho thấy đường bao màu xanh gồm 377 điểm bám sát biên polyp. Ở mặt nạ này còn có một đốm nhiễu nhỏ hơn 20 pixel vuông và đã bị loại bỏ. Sau khi đơn giản hóa, đa giác trong ảnh d chỉ còn 21 đỉnh, được đánh dấu bằng các chấm màu vàng, nhưng vẫn giữ được hình dạng của polyp. Như vậy, dung lượng nhãn giảm đáng kể trong khi thông tin về vị trí và hình dạng polyp gần như được bảo toàn.

## 4.4. Đổi kích thước ảnh

Từ mục này trở đi, các bước xử lý diễn ra mỗi khi ảnh được nạp vào mô hình. Mô hình được cấu hình với kích thước đầu vào 640 pixel, trong khi ảnh gốc có nhiều kích thước khác nhau. Nếu kéo giãn trực tiếp mọi ảnh thành hình vuông 640 × 640, polyp sẽ bị méo và mô hình học sai hình dạng thật của tổn thương. Vì vậy, ảnh được thu phóng nhưng vẫn giữ nguyên tỷ lệ giữa chiều rộng và chiều cao, sao cho cạnh dài nhất bằng 640 pixel:

$$
r=\frac{640}{\mathrm{max} (W,H)} \tag{4.6}
$$

$$
{W}^{'}=\lceil r\cdot W\rceil ,  {H}^{'}=\lceil r\cdot H\rceil \tag{4.7}
$$

Trong đó, *W* và *H* là kích thước ảnh gốc, *r* là hệ số thu phóng, *W*′ và *H*′ là kích thước sau khi thu phóng, được làm tròn lên thành số nguyên. Ảnh lúc này có cạnh dài bằng 640 nhưng cạnh ngắn vẫn nhỏ hơn 640.

Ở nhánh kiểm định, đề tài dùng kỹ thuật LetterBox để đưa ảnh về khung đích. Ảnh đã thu phóng ở trên không bị phóng to thêm mà được đặt vào giữa khung đích; phần còn thiếu được tô màu xám có giá trị 114, giống như các dải đen trên màn hình khi xem phim có tỷ lệ khung hình khác. Phần viền được chia đều cho hai phía:

$$
{p}_{x}=\frac{{S}_{W}-{W}^{'}}{2},  {p}_{y}=\frac{{S}_{H}-{H}^{'}}{2} \tag{4.8}
$$

Trong đó, *S*<sub>W</sub> × *S*<sub>H</sub> là kích thước khung đích, *p*<sub>x</sub> là độ rộng viền thêm vào mỗi bên trái và phải, *p*<sub>y</sub> là độ rộng viền thêm vào mỗi phía trên và dưới. Tọa độ đa giác cũng được nhân với *r* và cộng thêm *p*<sub>x</sub>, *p*<sub>y</sub>, nhờ đó nhãn luôn trùng với vị trí polyp trên ảnh mới.

Trong quá trình kiểm định thực tế, các ảnh có tỷ lệ khung hình gần nhau được gom thành lô 16 ảnh. Khung đích của mỗi lô được làm tròn lên bội số của 32 và cộng thêm nửa bước, nên có cạnh dài 672 pixel và cạnh ngắn từ 544 đến 672 pixel; ảnh vẫn giữ cạnh dài 640 và được viền xám ở hai phía. Với 160 ảnh kiểm định, 10 lô có các khung 544 × 672 (3 lô), 576 × 672 (5 lô), 608 × 672 (1 lô) và 672 × 672 (1 lô). Cách làm này giúp giảm phần viền thừa so với khung vuông. Ở nhánh huấn luyện, việc đưa ảnh vào khung 640 × 640 được thực hiện cùng với các phép tăng cường dữ liệu ở mục 4.5, phần trống cũng được tô màu xám 114.

Hình 4.3 minh họa kết quả trước và sau công đoạn đổi kích thước trên một ảnh của tập kiểm định có kích thước lớn nhất trong bộ dữ liệu, với khung đích 640 × 640 pixel.

![](../hinh/chuong4/h4_3.png)

*Hình 4.3. Trước và sau khi đổi kích thước ảnh bằng thu phóng giữ tỷ lệ và LetterBox*

*Nguồn: ảnh a từ bộ dữ liệu Kvasir-SEG [1]; ảnh b do đề tài tạo theo cách xử lý LetterBox trong mã nguồn Ultralytics.*

Ảnh gốc có kích thước 1.920 × 1.072 pixel nên hệ số thu phóng là 1/3, ảnh sau thu nhỏ có kích thước 640 × 358 pixel. LetterBox bổ sung hai dải xám, mỗi dải cao 141 pixel, ở phía trên và phía dưới để tạo thành khung 640 × 640 pixel. Có thể thấy polyp không bị méo và đường bao màu xanh vẫn nằm đúng vị trí sau khi đổi kích thước. Hình 4.3 dùng khung vuông 640 × 640 để minh họa; khi kiểm định thực tế, ảnh này thuộc lô có khung 544 × 672, nên viền trên và dưới mỗi phía 93 pixel, viền trái và phải mỗi phía 16 pixel.

## 4.5. Tăng cường dữ liệu

Tập huấn luyện chỉ có 1.040 ảnh, khá ít đối với một mô hình học sâu. Khi dữ liệu ít, mô hình dễ ghi nhớ từng ảnh huấn luyện thay vì học các đặc điểm chung của polyp, dẫn đến kết quả kém trên ảnh mới. Tăng cường dữ liệu khắc phục vấn đề này bằng cách tạo ra một biến thể ngẫu nhiên khác nhau của ảnh mỗi lần ảnh được nạp vào mô hình. Nhờ vậy, qua 100 epoch, mô hình gần như không gặp lại đúng một ảnh hai lần. Tăng cường dữ liệu chỉ áp dụng cho tập huấn luyện; tập kiểm định được giữ nguyên để việc đánh giá phản ánh đúng khả năng của mô hình trên ảnh thật.

> ❓ **CẦN XÁC NHẬN**: Nhận định định tính, hợp lý nhưng không đo được. **Đề xuất:** "…mô hình hiếm khi gặp lại một biến thể giống hệt nhau".

Các phép biến đổi được chia thành hai nhóm. Phép biến đổi hình học như ghép ảnh, dịch chuyển, thu phóng và lật làm thay đổi vị trí các pixel, nên đa giác nhãn được biến đổi theo đúng cách tương ứng. Phép biến đổi màu chỉ thay đổi giá trị màu của pixel, nên nhãn được giữ nguyên. Trong mã nguồn, các phép được thực hiện theo thứ tự: Mosaic, dịch chuyển và thu phóng, biến đổi màu HSV, cuối cùng là lật ngang. Thông số của từng phép được lấy từ tệp cấu hình của lần huấn luyện và tổng hợp trong Bảng 4.2.

### 4.5.1. Ghép bốn ảnh bằng Mosaic

Mosaic là kỹ thuật ghép bốn ảnh huấn luyện thành một ảnh, được giới thiệu trong YOLOv4 [10]. Trong mã nguồn, chương trình tạo một khung trống 1.280 × 1.280 pixel màu xám, chọn ngẫu nhiên một điểm làm tâm ghép, rồi đặt bốn ảnh vào bốn góc xung quanh điểm này. Sau đó, khung ghép được dịch chuyển, thu phóng và cắt về kích thước 640 × 640 pixel. Kết quả là một ảnh huấn luyện chứa nhiều bối cảnh khác nhau, polyp xuất hiện ở nhiều vị trí và kích thước, đôi khi chỉ hiện ra một phần. Ảnh nền cũng có thể được ghép chung với ảnh polyp, giúp mô hình phân biệt polyp với niêm mạc bình thường ngay trong cùng một ảnh.

Với xác suất bằng 1,0, Mosaic được áp dụng cho mọi ảnh trong phần lớn quá trình huấn luyện. Tuy nhiên, ảnh ghép không giống ảnh nội soi thật, nên Mosaic được tắt trong 10 epoch cuối của tổng số 100 epoch [11]. Ở giai đoạn này, mô hình được tinh chỉnh trên ảnh nguyên vẹn, gần với điều kiện sử dụng thực tế hơn.

> ⚠️ **CHƯA CHÍNH XÁC**: Khi tắt Mosaic, mã chỉ đặt `mosaic`, `mixup`, `cutmix`, `copy_paste` về 0; **dịch chuyển, thu phóng, đổi màu HSV, lật và Albumentations vẫn chạy**. **Đề xuất:** "…mô hình được huấn luyện trên từng ảnh đơn lẻ không ghép, vẫn kèm dịch chuyển, thu phóng, đổi màu và lật."
>
> 🔎 *Bằng chứng:* `02_ma_nguon/ultralytics_TSVM_FP32/data/dataset.py` dòng 364–374 (`close_mosaic`).

### 4.5.2. Dịch chuyển và thu phóng ngẫu nhiên

Phép dịch chuyển và thu phóng được thực hiện bằng một phép biến đổi affine. Mỗi điểm có tọa độ *x*, *y* trên ảnh được chuyển đến vị trí mới theo công thức:

$$
{x}^{'}=s\cdot (x-{c}_{x})+{t}_{x},  {y}^{'}=s\cdot (y-{c}_{y})+{t}_{y} \tag{4.9}
$$

Trong đó, *c*<sub>x</sub> và *c*<sub>y</sub> là tọa độ tâm ảnh đầu vào. Hệ số thu phóng *s* được chọn ngẫu nhiên trong đoạn từ 0,5 đến 1,5, tương ứng với tham số scale bằng 0,5, nghĩa là ảnh có thể bị thu nhỏ còn một nửa hoặc phóng to gấp rưỡi. Vị trí tâm mới *t*<sub>x</sub>, *t*<sub>y</sub> được chọn ngẫu nhiên lệch khỏi tâm khung 640 × 640 tối đa 10% kích thước khung, tương ứng với tham số translate bằng 0,1. Phép biến đổi này giúp mô hình nhận ra polyp ở các khoảng cách quan sát và vị trí khác nhau trong khung hình. Phần ảnh nằm ngoài khung bị cắt bỏ, phần trống được tô màu xám 114, và đa giác nhãn được biến đổi theo cùng công thức. Các phép xoay, cắt xiên và biến đổi phối cảnh đều có tham số bằng 0, nên không được sử dụng.

### 4.5.3. Biến đổi màu trong không gian HSV

Màu sắc ảnh nội soi thay đổi theo nguồn sáng, máy nội soi và vị trí chụp. Để mô hình không phụ thuộc vào một điều kiện màu cụ thể, ảnh được chuyển sang không gian màu HSV, trong đó H là sắc độ, tức màu cơ bản như đỏ hay cam; S là độ bão hòa, tức độ đậm nhạt của màu; V là độ sáng. Với mỗi ảnh, ba hệ số ngẫu nhiên *g*<sub>h</sub>, *g*<sub>s</sub>, *g*<sub>v</sub> được chọn đều trong các đoạn từ −0,015 đến 0,015, từ −0,7 đến 0,7 và từ −0,4 đến 0,4. Giá trị của từng pixel được biến đổi như sau:

$$
{H}^{'}=(H+180\cdot {g}_{h}) mod 180 \tag{4.10}
$$

$$
{S}^{'}=\mathrm{min} (255,S\cdot (1+{g}_{s})),  {V}^{'}=\mathrm{min} (255,V\cdot (1+{g}_{v})) \tag{4.11}
$$

Trong OpenCV, sắc độ nhận giá trị từ 0 đến 179, nên phép chia lấy dư cho 180 giúp sắc độ quay vòng trên bánh xe màu. Sắc độ chỉ được dịch rất ít, tối đa khoảng 2,7 đơn vị trên thang 180, để màu niêm mạc không bị biến thành những màu phi thực tế như xanh lá hay xanh dương. Ngược lại, độ bão hòa và độ sáng được thay đổi nhiều hơn để mô phỏng các điều kiện chiếu sáng khác nhau. Vì đây là phép biến đổi màu, vị trí polyp và nhãn không thay đổi.

### 4.5.4. Lật ngang và các phép bổ sung

Mỗi ảnh có xác suất 0,5 bị lật ngang, tức đối xứng qua trục dọc ở giữa ảnh. Khi đó, tọa độ ngang đã chuẩn hóa của mọi đỉnh đa giác được tính lại theo công thức:

$$
{\hat{x}}^{'}=1-\hat{x} \tag{4.12}
$$

Polyp có thể nằm ở bất kỳ phía nào của khung hình, nên ảnh lật ngang vẫn là một ảnh nội soi hợp lý và giúp tăng gấp đôi số trường hợp vị trí mà mô hình được học. Phép lật dọc không được sử dụng. Các phép trộn ảnh như MixUp, CutMix và Copy-Paste cũng đều có tham số bằng 0. Ngoài ra, mã nguồn có một nhánh tăng cường bổ sung từ thư viện Albumentations gồm làm mờ, lọc trung vị, chuyển ảnh xám và cân bằng độ tương phản cục bộ CLAHE, mỗi phép chỉ có xác suất 1%. Nhánh này chỉ hoạt động khi môi trường có cài thư viện Albumentations; nhật ký huấn luyện mô hình TSVM với seed 0 trên Kaggle ghi nhận nhánh này đã được kích hoạt.

> ⚠️ **CHƯA CHÍNH XÁC**: Nhật ký được dẫn có thật nhưng là của **lượt TSVM cũ** (bản lưu checkpoint FP16, tên run không có `_FP32`), không thuộc 40 lượt chính. Repo không lưu nhật ký của 40 lượt chính, kể cả Baseline. **Đề xuất:** "…nhật ký một lượt huấn luyện thử nghiệm trên Kaggle (cùng môi trường) cho thấy nhánh này được kích hoạt; repo không lưu nhật ký của 40 lượt chính."
>
> 🔎 *Bằng chứng:* `99_luu_tru/log_kaggle_cu/seed0_log.txt` dòng 62 và 523.

*Bảng 4.2. Thông số tăng cường dữ liệu trong cấu hình huấn luyện*

| **Phép biến đổi** | **Tham số** | **Giá trị** | **Ý nghĩa** |
|---|---|---|---|
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

Hình 4.4 minh họa tác động của từng phép tăng cường lên cùng một ảnh huấn luyện. Để dễ quan sát, các hệ số trong hình được chọn cố định trong phạm vi cho phép của Bảng 4.2; khi huấn luyện, các hệ số này được chọn ngẫu nhiên cho từng ảnh.

![](../hinh/chuong4/h4_4.png)

*Hình 4.4. Ảnh huấn luyện trước và sau các phép tăng cường dữ liệu*

*Nguồn: ảnh gốc từ bộ dữ liệu Kvasir-SEG [1] và Kvasir [2]; các phép biến đổi do đề tài tạo minh họa theo thông số trong Bảng 4.2.*

So với ảnh gốc a, ảnh b được lật ngang nên polyp chuyển sang phía bên phải. Ảnh c có màu cam đậm hơn do độ bão hòa tăng và độ sáng giảm, nhưng đường bao màu xanh không đổi. Ảnh d được thu nhỏ và dịch lệch khỏi tâm, phần trống được tô xám. Ảnh e là kết quả Mosaic từ bốn ảnh, trong đó có một ảnh nền, và các polyp chỉ hiện ra một phần ở góc ảnh. Ảnh f kết hợp lật ngang, biến đổi màu và phóng to. Trong mọi trường hợp, đường bao luôn khớp với polyp, cho thấy nhãn được biến đổi đồng bộ với ảnh.

> ❓ **CẦN XÁC NHẬN**: Hệ số dùng để vẽ Hình 4.4 không được lưu lại nên không kiểm tra được mô tả. **Đề xuất:** ghi các hệ số đã dùng vào chú thích hình (ví dụ *g<sub>s</sub>* = +0,5; *g<sub>v</sub>* = −0,2).

## 4.6. Định dạng và chuẩn hóa dữ liệu đầu vào

Sau khi tăng cường, ảnh và nhãn được chuyển thành dạng số mà mạng nơ-ron có thể tính toán. Công đoạn này gồm bốn thao tác.

**Đổi thứ tự kênh màu.** Thư viện OpenCV đọc ảnh theo thứ tự kênh xanh dương, xanh lá, đỏ, gọi là BGR. Ảnh được đảo lại thành thứ tự đỏ, xanh lá, xanh dương, gọi là RGB, là thứ tự màu thông dụng của các mô hình học sâu.

**Sắp xếp lại chiều dữ liệu.** Ảnh ban đầu được lưu theo thứ tự chiều cao, chiều rộng, số kênh màu. Ảnh được sắp xếp lại thành số kênh màu, chiều cao, chiều rộng, rồi nhiều ảnh được ghép thành một lô. Trong cấu hình huấn luyện, mỗi lô gồm 8 ảnh.

**Chuẩn hóa giá trị pixel.** Mỗi pixel ban đầu là số nguyên từ 0 đến 255. Giá trị này được chuyển sang số thực và chia cho 255:

$$
{I}_{\mathrm{norm}}=\frac{I}{255} \tag{4.13}
$$

Trong đó, *I* là giá trị pixel ban đầu và *I*<sub>norm</sub> là giá trị sau chuẩn hóa, nằm trong đoạn từ 0 đến 1. Đưa dữ liệu về một thang nhỏ giúp quá trình tối ưu ổn định hơn và tránh việc các giá trị lớn chi phối phép tính. Đề tài chỉ chia cho 255, không trừ giá trị trung bình hay chia cho độ lệch chuẩn của bộ dữ liệu ImageNet.

**Tạo mặt nạ huấn luyện từ đa giác.** Hàm mất mát phân đoạn cần so sánh dự đoán của mô hình với một mặt nạ, nên đa giác trong tệp nhãn được tô đầy để tạo lại mặt nạ. Để tiết kiệm bộ nhớ, mặt nạ có độ phân giải nhỏ hơn ảnh 4 lần theo tham số mask_ratio bằng 4; với ảnh 640 × 640 pixel, mặt nạ có kích thước 160 × 160. Khi tham số overlap_mask được bật, các polyp trong cùng một ảnh được gộp vào một mặt nạ duy nhất, mỗi polyp được đánh một số thứ tự riêng. Với ảnh nền, mặt nạ chỉ gồm toàn giá trị 0.

## 4.7. Kiểm tra tính toàn vẹn của dữ liệu

Ngay sau khi tạo bộ dữ liệu, chương trình chuyển đổi tự kiểm tra số lượng ảnh và nhãn của từng tập, gồm 1.040 ảnh và 1.040 tệp nhãn ở tập huấn luyện, 160 ảnh và 160 tệp nhãn ở tập kiểm định, cùng với số tệp nhãn rỗng lần lượt là 160 và 40. Nếu một con số không khớp, chương trình dừng lại và báo lỗi.

Bên cạnh đó, đề tài thực hiện thêm một lượt kiểm tra độc lập trên bộ dữ liệu đã dùng để huấn luyện. Kết quả cho thấy mỗi ảnh có đúng một tệp nhãn và không có tệp nhãn nào thiếu ảnh. Toàn bộ 1.063 dòng nhãn đều có chỉ số lớp 0, có ít nhất ba đỉnh và mọi tọa độ đều nằm trong đoạn từ 0 đến 1. Không có ảnh nào trùng tên hoặc trùng hoàn toàn nội dung giữa tập huấn luyện và tập kiểm định, được xác định bằng cách so sánh mã băm SHA-256 của từng tệp ảnh. Khi chạy lại chương trình chuyển đổi trên 1.000 mặt nạ gốc, cả 1.000 tệp nhãn thu được đều trùng khớp từng ký tự với nhãn đang sử dụng. Bước chọn ngẫu nhiên ảnh nền với seed bằng 42 cũng cho ra đúng danh sách 200 ảnh đã lưu. Như vậy, bộ dữ liệu có thể được tái tạo đầy đủ từ dữ liệu gốc.

> ⚠️ **CHƯA CHÍNH XÁC**: Kết quả này **phụ thuộc phiên bản OpenCV**: chạy lại trên OpenCV 5.0.0 / NumPy 2.5.1 cho 1.000/1.000 tệp trùng; trên OpenCV 4.12.0 / NumPy 2.2.6 chỉ 999/1.000 (tệp `ck2bxiswtxuw80838qkisqjwz.txt` lệch một đỉnh khoảng 3 px). Câu "có thể được tái tạo đầy đủ" cũng cần thêm điều kiện: có hai danh sách `train.txt`/`val.txt` và đúng phiên bản OpenCV. **Đề xuất:** "Chạy lại chương trình trên OpenCV 5.0.0 và NumPy 2.5.1 cho 1.000/1.000 tệp nhãn trùng từng ký tự; kết quả có thể lệch nhẹ ở phiên bản OpenCV khác. Bộ dữ liệu có thể được tái tạo từ dữ liệu gốc và hai danh sách chia tập."
>
> 🔎 *Bằng chứng:* chạy lại `01_du_lieu/scripts_tien_xu_ly/convert_kvasir_with_background_to_yolo_seg.py` (báo cáo A, #90, #92); `99_luu_tru/tai_lieu_cu/archive_doc/28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md` dòng 43.

Lượt kiểm tra này vẫn có một số giới hạn. Các tệp dữ liệu mà đề tài sử dụng không có thông tin định danh bệnh nhân, nên chưa thể khẳng định hai tập không chứa ảnh của cùng một bệnh nhân. Phép so sánh mã băm chỉ phát hiện được các ảnh giống nhau hoàn toàn, chưa phát hiện được các ảnh gần giống nhau như hai khung hình liên tiếp. Ngoài ra, bộ dữ liệu chỉ gồm tập huấn luyện và tập kiểm định, không có tập kiểm thử độc lập, nên kết quả thực nghiệm ở các chương sau được đánh giá trên tập kiểm định.

## 4.8. Tổng hợp quy trình tiền xử lý

Hình 4.5 tóm tắt toàn bộ quy trình xây dựng bộ dữ liệu và tiền xử lý đã trình bày trong chương.

![](../hinh/chuong4/h4_5.png)

*Hình 4.5. Quy trình xây dựng bộ dữ liệu BG20 và tiền xử lý dữ liệu*

*Nguồn: đề tài tự xây dựng.*

Phần phía trên của sơ đồ là giai đoạn chuẩn bị dữ liệu, chỉ thực hiện một lần trước khi huấn luyện. Ảnh polyp từ Kvasir-SEG được giữ nguyên, còn mặt nạ được chuyển thành nhãn đa giác; ảnh normal-cecum được chọn ngẫu nhiên và gắn nhãn rỗng. Hai nguồn này hợp lại thành bộ dữ liệu BG20 gồm 1.200 ảnh. Phần phía dưới là giai đoạn xử lý khi nạp dữ liệu, được chia thành hai nhánh. Nhánh huấn luyện có thêm bước tăng cường dữ liệu để tạo sự đa dạng, còn nhánh kiểm định chỉ đổi kích thước bằng LetterBox để giữ ảnh gần với thực tế nhất. Cả hai nhánh đều kết thúc bằng bước định dạng và chuẩn hóa trước khi đưa vào mô hình.

Cần lưu ý rằng khối TSVM là một thành phần bên trong mô hình, xử lý đặc trưng sau khi ảnh đã được chuẩn hóa. Quy trình tiền xử lý của mô hình YOLO26-seg gốc và mô hình tích hợp TSVM là hoàn toàn giống nhau, nhờ đó sự khác biệt về kết quả giữa hai mô hình ở các chương sau phản ánh tác động của kiến trúc chứ không phải của dữ liệu.

> ⚠️ **CHƯA CHÍNH XÁC**: Hai điểm: (1) khối cuối của Hình 4.5 ghi "YOLO26-seg + TSVM" trong khi quy trình dùng chung cho **cả hai** mô hình — nên sửa thành "YOLO26s-seg (đối chứng) / YOLO26s-seg + TSVM"; (2) câu "sự khác biệt… phản ánh tác động của kiến trúc" bỏ qua **dao động ngẫu nhiên giữa các seed**. **Đề xuất câu kết:** "…nhờ đó dữ liệu và tiền xử lý không phải là nguồn tạo ra khác biệt giữa hai mô hình; dao động ngẫu nhiên được kiểm soát bằng 20 seed ghép cặp (Chương 6)."
>
> 🔎 *Bằng chứng:* 40 tệp `args.yaml` chỉ khác `model`/`pretrained` (`00_tai_lieu_tong_quan/bang/03_cau_hinh_args.csv`).

## TÀI LIỆU THAM KHẢO CỦA CHƯƠNG 4

> ℹ️ **GHI CHÚ ĐÁNH SỐ**: Khi ghép vào báo cáo, danh mục riêng [1]–[11] của chương sẽ được đổi sang số thứ tự chung theo chuẩn IEEE (xem `_KIEM_TRA/D_tai_lieu_tham_khao.md`). Lời văn chương này giữ nguyên số [1]–[11] để bạn cùng nhóm dễ đối chiếu.

[1]D. Jha, P. H. Smedsrud, M. A. Riegler, P. Halvorsen, T. de Lange, D. Johansen, and H. D. Johansen, “Kvasir-SEG: A Segmented Polyp Dataset,” in  *MultiMedia Modeling, MMM 2020*, Lecture Notes in Computer Science, vol. 11962, Springer, Cham, 2020, pp. 451–462, doi: 10.1007/978-3-030-37734-2_37.

[2]K. Pogorelov, K. R. Randel, C. Griwodz, S. L. Eskeland, T. de Lange, D. Johansen, C. Spampinato, D.-T. Dang-Nguyen, M. Lux, P. T. Schmidt, M. Riegler, and P. Halvorsen, “Kvasir: A Multi-Class Image Dataset for Computer Aided Gastrointestinal Disease Detection,” in  *Proceedings of the 8th ACM on Multimedia Systems Conference, MMSys’17*, ACM, 2017, pp. 164–169.

[3]D. Jha, “Kvasir-SEG Data: Polyp segmentation & detection,” Kaggle. https://www.kaggle.com/datasets/debeshjha1/kvasirseg, truy cập ngày 09/10/2026.

[4]Ultralytics, “Instance Segmentation Datasets Overview,” Ultralytics Docs. https://docs.ultralytics.com/datasets/segment/, truy cập ngày 09/10/2026.

[5]G. Bradski, “The OpenCV Library,”  *Dr. Dobb’s Journal of Software Tools*, vol. 25, no. 11, pp. 120–125, 2000.

[6]N. Otsu, “A Threshold Selection Method from Gray-Level Histograms,”  *IEEE Transactions on Systems, Man, and Cybernetics*, vol. 9, no. 1, pp. 62–66, 1979.

[7]R. C. Gonzalez and R. E. Woods,  *Digital Image Processing*, 4th ed. New York, NY, USA: Pearson, 2018.

[8]S. Suzuki and K. Abe, “Topological Structural Analysis of Digitized Binary Images by Border Following,”  *Computer Vision, Graphics, and Image Processing*, vol. 30, no. 1, pp. 32–46, 1985.

[9]D. H. Douglas and T. K. Peucker, “Algorithms for the Reduction of the Number of Points Required to Represent a Digitized Line or its Caricature,”  *Cartographica: The International Journal for Geographic Information and Geovisualization*, vol. 10, no. 2, pp. 112–122, 1973.

[10]A. Bochkovskiy, C.-Y. Wang, and H.-Y. M. Liao, “YOLOv4: Optimal Speed and Accuracy of Object Detection,” arXiv:2004.10934, 2020.

[11]Ultralytics, “Data Augmentation using Ultralytics YOLO,” Ultralytics Docs. https://docs.ultralytics.com/guides/yolo-data-augmentation/, truy cập ngày 09/10/2026.

---

## PHỤ LỤC GÓP Ý (không thuộc nội dung chương)

### Tổng kết kiểm định

| Kết luận | Số nhận định |
|---|---:|
| Đúng | 80 (gồm nguồn chia tập 880/120, kiểm lại 27/10/2026) |
| Đúng một phần (⚠️) | 9 |
| Sai (❌) | 1 — khung kiểm định 640 → 672 (**đã sửa trong mục 4.4 ngày 28/10/2026**, cùng ô ⚠️ về LetterBox) |
| Chưa kiểm được (❓) | 4 |
| **Tổng** | **94** |

Một số con số đã đo lại và trùng khớp: 333 kích thước ảnh; ngưỡng Otsu 5–8; 1.206 đường bao, loại 143, còn 1.063; trung bình 333,2 → 24,6 điểm, 10–80 đỉnh mỗi đa giác; ví dụ Hình 4.2 (15 mức xám, 377 → 21 đỉnh, dòng nhãn mẫu khớp); Bảng 4.1 và 4.2 khớp 40/40 tệp `args.yaml`.

### Gợi ý bổ sung (không phải lỗi)

1. Nói rõ 160 ảnh kiểm định **vừa dùng để chọn epoch tốt nhất vừa dùng để báo cáo kết quả**, nên kết quả có thể hơi lạc quan.
2. Khi nạp nhãn, Ultralytics **nội suy mỗi đa giác thành 1.000 điểm** (`data/dataset.py` dòng 396), nên việc rút gọn còn khoảng 25 đỉnh chủ yếu làm gọn tệp nhãn, không làm mặt nạ huấn luyện thô hơn. Câu "dung lượng nhãn giảm đáng kể…" ở mục 4.3 có thể viết rõ ý này.
3. Sau phép affine/Mosaic, polyp bị cắt còn quá nhỏ sẽ bị loại khỏi nhãn của ảnh đó (`box_candidates`).
4. Mosaic chọn ảnh phụ từ **bộ đệm các ảnh vừa nạp**, không chọn đều trên toàn tập.
5. Ảnh nhỏ (rộng tới 332 px) được **phóng to** lên cạnh dài 640 bằng nội suy song tuyến tính.
6. Baseline chạy bằng `ultralytics==8.4.127` cài từ pip, TSVM chạy bằng bản fork; phần mã dữ liệu của hai bản tương đương về chức năng với cấu hình đã dùng.
7. Thống kê có sẵn có thể đưa thêm: 48 ảnh có từ 2 polyp trở lên (41 train, 7 val); trung vị số đỉnh 22 (train) và 26 (val).
8. Tên mô hình nên thống nhất là **YOLO26s-seg** (biến thể s) như các chương khác.

### Câu hỏi gửi tác giả chương

1. **[ĐÃ SỬA 28/10/2026] Khung kiểm định (mục 4.4):** bạn dựa vào nguồn nào để ghi cạnh dài 640? Mã Ultralytics 8.4.127 cho thấy khi kiểm định trong lúc huấn luyện, ảnh được gom lô theo tỉ lệ khung (`rect=True`) và cộng nửa bước đệm (`pad=0.5`), nên khung có cạnh dài 672 (bằng chứng ở ô ❌ mục 4.4). Nếu bạn đang mô tả bước suy luận chứ không phải kiểm định thì ghi rõ là bước nào.
2. ~~Chia tập 880/120 (mục 4.2)~~: đã giải quyết, danh sách do tác giả Kvasir-SEG cung cấp kèm bản Kaggle [3].
3. **Hình 4.4:** các hệ số tăng cường dùng để vẽ hình là bao nhiêu?
