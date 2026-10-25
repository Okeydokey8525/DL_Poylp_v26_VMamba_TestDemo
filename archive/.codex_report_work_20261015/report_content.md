# MỞ ĐẦU
## 1 Lý do chọn đề tài
Phân đoạn polyp từ ảnh nội soi là bài toán xác định vùng tổn thương ở mức điểm ảnh. So với việc chỉ trả về hộp bao, mặt nạ cung cấp mô tả cụ thể hơn về hình dạng và vị trí của đối tượng. Tuy nhiên, màu sắc polyp có thể gần với niêm mạc xung quanh; nếp gấp, phản quang và thay đổi kích thước quan sát cũng làm việc phân biệt đối tượng trở nên khó khăn. Các bộ dữ liệu công khai như Kvasir-SEG tạo điều kiện nghiên cứu những vấn đề này trong một quy trình có thể kiểm tra lại [1], [2].
YOLO26-seg cung cấp khung phát hiện và phân đoạn từng đối tượng trong một mô hình thống nhất. Trong khi đó, Visual State Space Model và cơ chế SS2D của VMamba tạo cách truyền thông tin giữa các vị trí xa nhau trên bản đồ đặc trưng [15], [16]. Đề tài khảo sát việc kết hợp ngữ cảnh toàn cục đó với đặc trưng hình dạng cục bộ ngay trong backbone YOLO26s-seg. Câu hỏi nghiên cứu là liệu khối kết hợp có cải thiện chất lượng phân đoạn và tính ổn định qua các lần khởi tạo, khi giữ cố định dữ liệu và siêu tham số huấn luyện hay không.
Đề tài triển khai C2TSVMamba tại tầng 10, đồng thời xử lý vấn đề độ chính xác số khi lưu và nạp checkpoint. Cặp đối chứng chính gồm YOLO26s-seg cơ bản và YOLO26s-seg tích hợp TSVM với checkpoint FP32. Kết quả được xem xét trên 20 cặp seed, thay vì lựa chọn một lượt chạy thuận lợi để đại diện cho toàn bộ phương pháp.
## 2 Mục tiêu và câu hỏi nghiên cứu
Mục tiêu tổng quát là xây dựng, giải thích và đánh giá phương pháp tích hợp TSVM vào YOLO26s-seg cho phân đoạn polyp trên bộ dữ liệu BG20, sau đó tích hợp hai mô hình vào ứng dụng minh họa PolypVision. Mục tiêu cụ thể gồm mô tả đúng luồng tính toán của khối đề xuất; bảo đảm các lượt huấn luyện có thể đối chiếu; phân tích chênh lệch trung bình và biến thiên giữa seed; và kiểm tra việc nạp checkpoint thực nghiệm vào dịch vụ suy luận.
Ba câu hỏi được đặt ra. Thứ nhất, TSVM FP32 có đạt mask mAP50–95 trung bình cao hơn baseline trên tập kiểm định cố định không? Thứ hai, phân bố kết quả giữa 20 seed có thay đổi và bằng chứng thống kê hỗ trợ đến mức nào? Thứ ba, các checkpoint đã lưu có thể được nạp đúng kiến trúc và suy luận trong cùng luồng ứng dụng Web và Mobile hay không? Câu hỏi thứ ba là kiểm tra kỹ thuật triển khai, không phải kiểm chứng hiệu quả lâm sàng.
## 3 Đối tượng và phạm vi nghiên cứu
Đối tượng nghiên cứu là ảnh nội soi tĩnh có polyp và ảnh normal-cecum từ nguồn công khai. Bộ BG20 gồm 1.200 ảnh, chia thành 1.040 ảnh huấn luyện và 160 ảnh kiểm định. Chỉ có một lớp đối tượng là polyp; ảnh nền mang nhãn rỗng. Thực nghiệm chính gồm seed 0 đến 19 của hai mô hình, mỗi lượt 100 epoch và kích thước ảnh cấu hình 640 pixel.
Các kết quả TSVM không mang hậu tố FP32 thuộc giai đoạn nghiên cứu trước và không được gộp vào phép so sánh chính. Các bài báo quốc tế được dùng để định vị phương pháp và tham khảo kết quả đã công bố, không được xem là những mô hình mà nhóm đã chạy lại. Bộ dữ liệu hiện có không cung cấp tập kiểm thử độc lập hoặc định danh bệnh nhân; vì vậy, kết luận định lượng giới hạn ở tập kiểm định BG20 và biến thiên tối ưu hóa theo seed.
## 4 Phương pháp thực hiện và đóng góp
Đề tài sử dụng phương pháp thực nghiệm có đối chứng. Hai kiến trúc được huấn luyện với cùng tập ảnh, nhãn và cấu hình tối ưu hóa. Mỗi lượt chạy được lưu riêng results.csv và args.yaml; số liệu được ghép theo seed để tính chênh lệch, khoảng tin cậy và kiểm định. Khi có khác biệt giữa mô tả và cấu hình đã lưu, cấu hình cùng số liệu gốc là căn cứ cho phần thực nghiệm.
Đóng góp của đề tài nằm ở thiết kế khối TSVM kết hợp SS2D với nhánh hình dạng đa tỉ lệ và có hướng trong wrapper C2; phân tích khả năng tích hợp tại tầng sâu của YOLO26s-seg; duy trì checkpoint FP32 cho nhánh trạng thái; và nối kết kết quả thực nghiệm với ứng dụng minh họa. Những đóng góp này cần được phân biệt với các ý tưởng có trước về Mamba cho polyp, topology guidance và convolutional gating.
## 5 Bố cục báo cáo
Chương 1 trình bày cơ sở và nghiên cứu liên quan. Chương 2 mô tả kiến trúc, luồng dữ liệu và độ chính xác số. Chương 3 trình bày dữ liệu và tiền xử lý. Chương 4 mô tả notebook huấn luyện cùng ứng dụng PolypVision. Chương 5 trình bày quy tắc so sánh, kết quả 20 seed, các giới hạn và đối chiếu tài liệu. Phần kết luận tổng hợp kết quả và xác định các công việc cần kiểm chứng tiếp theo.

# CHƯƠNG 1 TỔNG QUAN VÀ CƠ SỞ NGHIÊN CỨU
## 1.1 Bài toán phân đoạn polyp
### 1.1.1 Phân đoạn ngữ nghĩa và phân đoạn từng đối tượng
Phân đoạn ngữ nghĩa gán một lớp cho mỗi điểm ảnh, trong khi phân đoạn từng đối tượng còn tách các đối tượng cùng lớp thành những mặt nạ riêng. Trong BG20, một ảnh có thể có nhiều vùng polyp tách rời; vì vậy số đối tượng lớn hơn số ảnh có polyp. YOLO26-seg xử lý bài toán theo hướng từng đối tượng, đồng thời xuất hộp bao, độ tin cậy và mặt nạ. Đặc điểm này quyết định cách sử dụng Precision, Recall và AP trong đánh giá.
Đối với ảnh nền, hệ thống cần có khả năng không trả về đối tượng. Một lớp background trong ma trận phát hiện thường biểu thị các trường hợp không ghép được giữa dự đoán và nhãn; nó không đồng nghĩa với việc bộ dữ liệu có một lớp bệnh học thứ hai. Tương tự, số dương tính giả tính theo đối tượng không tự chuyển được thành số ảnh nền có báo động giả.
### 1.1.2 Các khó khăn về hình ảnh và dữ liệu
Biên mờ có thể khiến mặt nạ thu hẹp hoặc lan sang niêm mạc; phản quang có thể tạo khoảng trống trong vùng dự đoán. Polyp nhỏ cần giữ được chi tiết không gian, còn polyp lớn cần thông tin ngữ cảnh rộng. Tuy nhiên, những mô tả này là động cơ thiết kế. Muốn khẳng định một module cải thiện biên hoặc liên thông, cần độ đo và tập ca kiểm chứng tương ứng, ngoài các chỉ số phát hiện tổng hợp.
Kvasir-SEG và ảnh normal-cecum có khác biệt về bối cảnh giải phẫu, thiết bị và các ký hiệu xuất hiện trong khung hình. Việc thêm mẫu âm có ích cho nghiên cứu phát hiện sai, nhưng nguồn âm chỉ từ một mốc giải phẫu chưa đại diện cho mọi niêm mạc lành. Do đó, phân bố BG20 là một thiết lập nghiên cứu cụ thể, chưa phản ánh đầy đủ phân bố khung hình của một phiên nội soi.
## 1.2 Các mô hình nền tảng
### 1.2.1 Mạng tích chập và kiến trúc encoder decoder
Mạng tích chập học các mẫu cục bộ bằng kernel dùng chung giữa các vị trí. Depthwise convolution thực hiện lọc riêng từng kênh, còn convolution 1×1 trộn thông tin giữa các kênh. Những thao tác này được dùng trong nhánh hình dạng của TSVM để tạo nhiều trường tiếp nhận mà không cần attention theo mọi cặp vị trí.
U-Net tổ chức encoder và decoder với các kết nối bỏ qua để kết hợp thông tin ngữ nghĩa sâu và chi tiết ở độ phân giải cao [12]. PraNet khai thác reverse attention cho phân đoạn polyp [13]. Các hướng này cho thấy thông tin toàn cục và chi tiết biên cần được kết hợp ở nhiều mức, nhưng cách kết hợp và nhiệm vụ đầu ra khác nhau giữa từng mô hình.
### 1.2.2 YOLO26 và đầu phân đoạn
Trong mã được sử dụng, YOLO26s-seg gồm backbone, neck hợp nhất đa mức và đầu Segment26. Backbone cơ bản kết thúc bằng SPPF và C2PSA. Đầu phân đoạn nhận đặc trưng P3, P4 và P5; mặt nạ được tạo từ các prototype và hệ số của từng đối tượng. Cấu hình end2end được bật và reg_max bằng 1. Vì vậy không nên diễn giải YOLO26 như một bản sao nguyên trạng của các phiên bản YOLO dùng DFL với nhiều bin [16].
Chữ s xác định quy mô small thông qua hệ số depth bằng 0,50 và width bằng 0,50. Mã nguồn và notebook của đề tài tạo YAML có scale s rõ ràng. Việc chỉ mở tệp YAML chung mà không chỉ định scale có thể dẫn đến sử dụng biến thể mặc định khác; đây là một yếu tố cần kiểm tra khi tái lập hoặc khi nạp mô hình từ kiến trúc.
## 1.3 Mamba và mô hình trạng thái thị giác
### 1.3.1 Biểu diễn trạng thái chọn lọc
Một mô hình trạng thái rời rạc truyền thông tin qua trạng thái ẩn h. Với Mamba, một số tham số phụ thuộc đầu vào, cho phép đáp ứng thay đổi theo nội dung thay vì áp dụng cùng một bộ lọc cố định cho toàn chuỗi [14]. Trong triển khai của đề tài, bước thời gian Δ được tạo qua softplus, ma trận chuyển trạng thái A có giá trị âm và mỗi vị trí tạo các hệ số B, C.
@EQ hₜ = exp(ΔₜA) ⊙ hₜ₋₁ + ΔₜBₜuₜ ; yₜ = Σₙ Cₜ,ₙhₜ,ₙ
Biểu thức trên mô tả phép lặp thực tế trong module, với thành phần đầu vào được tính bằng ΔBu. Đây là cách cài đặt trạng thái chọn lọc của đề tài; không đồng nhất toàn bộ các thành phần hoặc tối ưu phần cứng của thư viện Mamba gốc.
### 1.3.2 Cơ chế SS2D bốn hướng
VMamba mở rộng cách xử lý chuỗi sang dữ liệu ảnh thông qua SS2D [15]. Một bản đồ H×W được sắp thành chuỗi theo hàng và theo cột; hai chuỗi đảo chiều bổ sung hai hướng ngược lại. Kết quả được đưa về đúng vị trí không gian rồi hợp nhất. Bốn hướng này là hàng xuôi, hàng ngược, cột xuôi và cột ngược, không phải bốn đường quét chéo.
Ở tầng P5 với ảnh 640×640, chiều dài chuỗi là L = 20×20 = 400. Đặt module ở độ phân giải thấp giúp giới hạn chi phí quét nhưng có thể làm mất chi tiết biên nhỏ. Vì thế lợi ích dự kiến của nhánh hình dạng tại P5 cần được đánh giá thực nghiệm; không thể suy ra độ chính xác biên trực tiếp từ vị trí module.
## 1.4 Nghiên cứu liên quan và vị trí của đề tài
### 1.4.1 Mamba cho phân đoạn polyp
Polyp-Mamba kết hợp biểu diễn đa tỉ lệ và cơ chế đưa ngữ nghĩa toàn cục vào đặc trưng cục bộ [17]. Công trình này cho thấy việc dùng Visual Mamba trong phân đoạn polyp đã có trước đề tài. Điểm cần đối chiếu là cách xây dựng nhánh hình dạng và vị trí tích hợp trong YOLO26s-seg, thay vì chỉ sự xuất hiện của Mamba.
Topo-VM-UNetV2 sử dụng persistent homology từ probability map để tạo topology attention map và đưa vào Topo-SDI [18]. TSVM hiện tại tạo guidance trực tiếp từ các convolution học được. Do đó, hai mô hình có động cơ gần nhau nhưng nguồn tín hiệu topology khác nhau; TSVM chưa có phép đo hoặc ràng buộc topology tường minh như persistent homology.
CSG-Mamba đặt convolutional scoring gate tại bottleneck của mạng Vision Mamba để điều chỉnh đặc trưng bằng thông tin cục bộ [19]. Đây là đối chiếu gần về cơ chế gating. TSVM sử dụng nhiều kích thước và hướng kernel, phép điều chỉnh 1+G và hợp nhất thêm nhánh hình dạng trong wrapper C2.
### 1.4.2 Mamba trong YOLO và các hướng về biên
MambaPSA thay C2PSA cuối backbone YOLO26 bằng lõi Mamba, giữ cơ chế chia nhánh và ghép kênh, đồng thời khảo sát vị trí module trong neck [20]. Công trình đánh giá phát hiện đối tượng trên PASCAL VOC. Vì vậy, đóng góp của đề tài không được định nghĩa đơn thuần là thay C2PSA bằng Mamba trong YOLO26; nó gắn với thiết kế TSVM và thực nghiệm phân đoạn polyp.
SAM-MaGuP kết hợp boundary distillation và Mamba adapter với SAM cho polyp [21]. Hướng nghiên cứu này nhấn mạnh nhu cầu kiểm chứng biên riêng. Trong đề tài, kết quả mAP chưa đủ để suy ra lợi ích trên HD95, Boundary F1 hoặc tính liên thông; những phép đo đó được xác định là phần mở rộng.
@TABLE related
### 1.4.3 Phạm vi tính mới
Đề tài xem C2TSVMamba là một thiết kế kết hợp có thể kiểm chứng, không tuyên bố phát minh ra SS2D, convolution đa tỉ lệ hoặc sigmoid gating. Điểm phân biệt gồm nhánh hình dạng có hướng, guidance một chiều từ nhánh đó đến SS2D, cách hợp nhất hai nhánh và tích hợp vào YOLO26s-seg tại tầng 10. Tuy nhiên, các đóng góp riêng của từng thành phần chỉ có thể tách bạch bằng ablation có đối chứng.
Từ topology trong tên module biểu thị định hướng học cấu trúc. Các kernel học được không bảo đảm số thành phần liên thông hoặc số lỗ của mặt nạ. Khóa luận vì vậy phân biệt cơ chế kiến trúc, giả thuyết tác dụng và kết quả đã đo; không dùng tên module thay cho bằng chứng về bảo toàn topology.
## 1.5 Tóm tắt chương
Các nghiên cứu liên quan cho thấy bài toán kết hợp ngữ cảnh dài hạn và chi tiết hình dạng đã được quan tâm trong phân đoạn polyp. Đề tài chọn một vị trí tích hợp cụ thể trong YOLO26s-seg và kiểm tra bằng thực nghiệm ghép cặp nhiều seed. Cơ sở này dẫn đến yêu cầu mô tả chính xác khối TSVM và phân biệt tác động kiến trúc với độ chính xác số của checkpoint ở chương tiếp theo.

# CHƯƠNG 2 PHÂN TÍCH VÀ THIẾT KẾ MÔ HÌNH ĐỀ XUẤT
## 2.1 Kiến trúc đối chứng YOLO26s seg
Mô hình cơ bản sử dụng cấu hình yolo26-seg với scale s, số lớp được thay bằng một lớp polyp khi huấn luyện. Các khối Conv giảm độ phân giải; C3k2 học và hợp nhất đặc trưng; SPPF bổ sung trường tiếp nhận; C2PSA thực hiện xử lý đặc trưng ở cuối backbone. Neck kết hợp các mức sâu và nông để đầu Segment26 dự đoán trên ba thang không gian.
@FIG architecture|Hình 2.1 Kiến trúc YOLO26s seg và vị trí thay thế module ở tầng 10
Khối thay thế có cùng kích thước đầu vào và đầu ra với C2PSA. Những kết nối lên neck và các chỉ số tầng ở đầu phân đoạn được giữ tương thích. Cách can thiệp này giúp xác định rõ phần kiến trúc thay đổi, nhưng không có nghĩa tổng số tham số hoặc động lực tối ưu hóa của hai mô hình giống nhau.
@TABLE layers
## 2.2 Wrapper C2TSVMamba
C2TSVMamba trước hết chiếu đầu vào bằng convolution 1×1 rồi tách thành hai nhánh a và b có cùng số kênh. Nhánh a đi tắt, nhánh b đi qua TSVMamba. Hai nhánh được ghép và chiếu lại bằng convolution 1×1. Với đầu vào 512 kênh, hệ số e bằng 0,5 tạo mỗi nhánh 256 kênh; đây là số kênh được SS2D bên trong xử lý.
@EQ [a, b] = split(Conv₁×₁(x)) ; y = Conv₁×₁(concat(a, TSVMamba(b)))
YAML ghi repeats bằng 2, nhưng parser áp dụng depth multiplier bằng 0,5 cho biến thể s nên số block nội bộ là 1. Điều kiện c1 = c2 được kiểm tra trong constructor. Vì module có đường đi tắt và phép chiếu đầu ra, residual trong TSVMamba chỉ là một phần của toàn wrapper, không phải đường đi duy nhất của đặc trưng.
## 2.3 Các nhánh của TSVMamba
### 2.3.1 Nhánh SS2D toàn cục
Đầu vào được chiếu thành hai tensor u và z. Tensor u qua convolution depthwise 3×3 và SiLU, sau đó được trải thành bốn chuỗi có cùng chiều dài. Ở mỗi hướng, phép chiếu tuyến tính sinh Δ, B và C; A được tham số hóa bằng âm của hàm mũ để tạo đáp ứng suy giảm. Kết quả quét được đưa lại về lưới không gian rồi cộng giữa bốn hướng. Tensor z tạo điều biến SiLU trước phép chiếu đầu ra.
State dimension mặc định bằng 16; expand bằng 1,0 và dt_rank bằng ceil(c/16). Với c bằng 256, dt_rank bằng 16. Mã hiện tại không có LayerNorm đầu ra SS2D hoặc nhánh skip D độc lập giống một số cấu hình VMamba tham chiếu. Vì vậy, thuật ngữ SS2D trong báo cáo chỉ cách quét chọn lọc đang được cài đặt, không ngụ ý đồng nhất từng chi tiết với mọi phiên bản VMamba gốc.
### 2.3.2 Nhánh hình dạng đa tỉ lệ và có hướng
ShapeAwareBranch áp dụng hai convolution depthwise 3×3 và 5×5 song song rồi ghép bằng convolution 1×1. DirectionalShapeExtractor tiếp tục xử lý theo kernel ngang 1×5, kernel dọc 5×1 và kernel cục bộ 3×3. Các kernel này được học cùng mô hình và tạo một thiên hướng biểu diễn theo kích thước, hướng, thay vì một phép trích biên cố định.
@EQ S_grad = √(S_h² + S_v² + 10⁻⁶)
Đáp ứng S_grad được ghép với S_h, S_v và S_local để tạo biểu diễn cấu trúc, sau đó kết hợp lại với đặc trưng shape ban đầu. Vì S_h và S_v là đầu ra convolution có BatchNorm và activation, biểu thức trên không phải gradient đạo hàm không gian chuẩn như Sobel. Tương tự, convolution 3×3 không tự tạo ra phép đo độ cong hình học tường minh.
### 2.3.3 Guidance và hợp nhất
@EQ G = sigmoid(Conv₁×₁(S)) ; F′_M = F_M ⊙ (1 + G)
@EQ y = x + γ · FFN(Conv₁×₁(concat(F′_M, S)))
Cổng sigmoid có giá trị trong đoạn từ 0 đến 1 nên hệ số trực tiếp nhân với F_M nằm từ 1 đến 2. Nó điều chỉnh mức khuếch đại theo vị trí và kênh; không trực tiếp làm nhỏ biên độ F_M dưới giá trị ban đầu. Khả năng hạn chế dự đoán nền, nếu có, là kết quả của toàn bộ mạng sau hợp nhất và phải được đo ở đầu ra.
@FIG tsvm|Hình 2.2 Hai nhánh SS2D và hình dạng cùng cơ chế guidance trong TSVMamba
FFN dùng hai convolution 1×1 với số kênh mở rộng gấp đôi rồi thu lại. Hệ số residual γ là một tham số học được, khởi tạo 0,001, nhằm giới hạn tác động ban đầu của nhánh mới. Giá trị khởi tạo nhỏ không chứng minh quá trình huấn luyện luôn ổn định; thống kê kích hoạt và checkpoint vẫn cần được kiểm tra.
## 2.4 Độ phức tạp và độ chính xác số
### 2.4.1 Chi phí của phép quét đang triển khai
Hàm parallel_associative_scan ghép cặp phép chuyển trạng thái theo các bước có độ lệch 1, 2, 4 và tiếp tục nhân đôi. Chuỗi được đệm đến lũy thừa hai gần nhất. Với L bằng 400, chuỗi đệm có 512 vị trí và có 9 bước ghép. Mỗi bước vẫn tạo và xử lý các tensor trải trên phần lớn chiều dài chuỗi.
Khi cố định batch, kênh và state dimension, số bước phụ thuộc là O(log L), còn tổng công việc tensor của triển khai này là O(L log L). Không thể suy ra thời gian suy luận tuyến tính hoặc tốc độ cao chỉ từ tính chất của Mamba trong tài liệu gốc. Các tensor trạng thái có chiều B×D×N×L cũng ảnh hưởng đáng kể đến bộ nhớ và chi phí đọc ghi.
### 2.4.2 Vì sao cần checkpoint FP32
Trong fork cơ bản, bước lưu checkpoint chuyển bản sao EMA sang half. Đối với TSVM, nhánh trạng thái có thể tạo các giá trị lớn trước BatchNorm; các running statistics lớn có nguy cơ vượt miền số hữu hạn FP16. Việc tắt AMP lúc train không thay đổi phép chuyển kiểu trong hàm lưu checkpoint. Vì vậy, amp=False và lưu FP32 là hai yêu cầu khác nhau.
Bản FP32 đổi snapshot EMA và checkpoint sau strip_optimizer sang float32, đồng thời dừng với FloatingPointError khi phát hiện tensor NaN hoặc Inf. Thay đổi này bảo toàn biểu diễn số của checkpoint; nó không thêm một nhánh kiến trúc mới. Ứng dụng cũng ép mô hình về float32 và không yêu cầu half khi suy luận. Kiểm tra nạp thành công chưa thay thế cho việc đánh giá lại toàn bộ tập kiểm định từ checkpoint.
## 2.5 Huấn luyện và khởi tạo trọng số
Baseline được tạo từ yolo26s-seg.pt. Mô hình đề xuất được tạo từ YAML scale s rồi nạp các trọng số tương thích từ cùng tệp pretrained. Các tham số của module thay thế không có đối ứng trong C2PSA nên được khởi tạo riêng. Đây là học chuyển giao từ checkpoint YOLO phân đoạn; không mô tả trực tiếp như nạp trọng số ImageNet cho toàn bộ TSVM.
Hàm mất mát thuộc pipeline Segment26 của fork Ultralytics, bao gồm thành phần phát hiện và phân đoạn theo cấu hình. Đề tài không bổ sung topology loss, persistent homology loss hoặc một boundary supervision riêng trong khối TSVM. Các hệ số có tên trong args.yaml phải được diễn giải cùng nhánh thực thi; riêng reg_max bằng 1 làm mất mát DFL dạng nhiều bin không hoạt động như ở cấu hình reg_max lớn hơn 1.
## 2.6 Các chế độ ablation và giả thuyết kiểm chứng
Mã nguồn có bốn mode: topology_shape_vmamba, vmamba_only, shape_only và shape_vmamba_no_guidance. Chúng cho phép phân biệt vai trò ngữ cảnh, hình dạng và guidance. Thực nghiệm chính được trình bày trong báo cáo hiện gồm baseline và full TSVM FP32; chưa có bộ 20 seed tương ứng cho từng mode để định lượng đóng góp riêng.
@TABLE ablation
Thử nghiệm ablation trong tương lai cần dùng cùng seed, dữ liệu, pretrained policy, epoch và tiêu chí chọn checkpoint. Nếu thêm một module làm tăng tham số, có thể bổ sung đối chứng convolution với mức tham số tương đương. Điều này giúp tránh quy kết mọi mức tăng cho guidance khi nguyên nhân có thể gồm dung lượng mạng hoặc thay đổi tối ưu hóa.
## 2.7 Tóm tắt chương
Mô hình đề xuất thay một block sâu bằng C2TSVMamba, kết hợp trạng thái toàn cục với tín hiệu hình dạng học được. Bản FP32 xử lý vấn đề lưu và suy luận chính xác số, không thay đổi sơ đồ kiến trúc. Những mô tả này xác định các giả thuyết cần đánh giá và giới hạn những khẳng định có thể rút ra từ thực nghiệm.

@IMPORT_CHAPTER3

# CHƯƠNG 4 CÀI ĐẶT THUẬT TOÁN VÀ ỨNG DỤNG MINH HỌA
## 4.1 Tổ chức cài đặt và môi trường
Mã mô hình cơ bản nằm trong thư mục ultralytics; bản đề xuất dùng ultralytics_Topology-Shape-aware_VMamba_FP32. Hai notebook tại Cell Kaggle mô tả cách khởi tạo dữ liệu, nạp mô hình và huấn luyện một seed. Các tệp args.yaml trong từng thư mục chạy là căn cứ cho siêu tham số đã sử dụng. Việc tổng hợp 20 seed dựa trên 40 lượt lưu độc lập, không dựa vào giả định notebook đã chứa sẵn một vòng lặp tự động 20 seed.
@TABLE training
Cấu hình device bằng 0 xác định thiết bị CUDA được chọn trong phiên Kaggle, nhưng không xác nhận tên GPU, dung lượng VRAM hoặc phiên bản CUDA. Báo cáo không gán một cấu hình Tesla T4 cụ thể cho mọi lượt khi chưa có log tương ứng. AdamW là thuật toán tối ưu có suy giảm trọng số tách biệt [22]. Các phiên bản Python, PyTorch và phần cứng dùng trong kiểm tra ứng dụng cục bộ được tách khỏi môi trường huấn luyện trên Kaggle.
## 4.2 Quy trình notebook và lưu kết quả
### 4.2.1 Notebook baseline
Notebook baseline cài Ultralytics 8.4.127, tạo data_bg20.yaml trỏ tới images/train và images/val, khai báo một lớp polyp. Mô hình được nạp bằng YOLO(yolo26s-seg.pt). Cell huấn luyện đặt seed, batch, epoch và các thiết lập tất định; cuối cùng nén thư mục runs. Danh sách seed phải được thay hoặc điều phối giữa các lượt; bản notebook đang lưu chứa một giá trị SEED cụ thể, không tự chứng minh đã chạy tất cả seed.
### 4.2.2 Notebook mô hình đề xuất và yêu cầu FP32
Notebook đề xuất sao chép YAML chung thành tên yolo26s-seg-TopologyShapeVMamba.yaml và gán scale s, sau đó nạp trọng số pretrained. Tuy nhiên, đường dẫn custom repo trong bản notebook được lưu vẫn nhắc thư mục TSVM cũ. Khi tái lập thực nghiệm FP32 cần trỏ đến fork có PATCH_FP32, kiểm tra đường dẫn module thực sự được import, đặt tên lượt chạy có TSVM_FP32 và xác nhận checkpoint được lưu bằng float32.
Các tệp kết quả được tổ chức theo seed để giữ tương ứng giữa args.yaml, results.csv, weights/best.pt và hình đánh giá. Bảng tổng hợp không thay thế các tệp gốc. Khi cần so sánh mô hình đã triển khai, phải ghi thêm mã băm checkpoint, epoch theo fitness và cấu hình suy luận; các chỉ số tại epoch tối đa mask mAP trong lịch sử train chưa phải mặc nhiên là chỉ số của best.pt.
## 4.3 Tổng quan ứng dụng PolypVision
PolypVision có hai client độc lập dùng chung dịch vụ AI. Trình duyệt giao tiếp với Spring Boot; tầng Web quản lý tài khoản, phân quyền, ảnh và lịch sử trong MongoDB cùng kho tệp cục bộ. Flutter Mobile Direct AI gửi yêu cầu trực tiếp tới FastAPI, không bắt buộc đi qua Web và không dùng MongoDB như một lịch sử cloud mặc định.
@FIG application|Hình 4.1 Kiến trúc Web và Mobile dùng chung dịch vụ suy luận FastAPI
Mã Web khai báo Java 17 và Spring Boot 4.1.0, sử dụng Thymeleaf, Spring Security và Spring Data MongoDB. Mobile sử dụng Flutter và các thư viện Dio, Riverpod, go_router, image_picker. Dịch vụ AI dùng FastAPI, PyTorch, Ultralytics, Pillow và OpenCV. Những thông tin này mô tả mã nguồn hiện tại, không thay cho một phép đo tải đồng thời hoặc khả năng vận hành dài hạn.
## 4.4 Dịch vụ suy luận và hợp đồng API
### 4.4.1 Nạp và định danh mô hình
Registry được chuyển sang hai khóa YOLO26s-seg và YOLO26s-TSVM-FP32-seg. Tệp mặc định là yolo26s-seg-best.pt và yolo26s-tsvm-fp32-best.pt, lấy từ seed 0 của hai nhóm thực nghiệm. Chọn cùng một seed cố định để minh họa tránh việc mỗi mô hình được chọn riêng theo lượt thuận lợi nhất. Đây không phải khẳng định seed 0 đại diện cho phân bố 20 seed.
Trước khi nạp checkpoint TSVM, dịch vụ đăng ký các lớp trong ultralytics.nn.modules.topology_shape_vmamba, tương ứng đúng tên module được lưu trong checkpoint. Sau khi tải, dịch vụ kiểm tra task segment, nhãn polyp và sự hiện diện của C2TSVMamba trong mô hình cải tiến. Tệp experiment_manifest.json ghi nguồn, seed, kích thước và SHA-256 của hai checkpoint để đối chiếu.
### 4.4.2 Tiếp nhận ảnh và suy luận
Ảnh tải lên được kiểm tra MIME và nội dung giải mã, giới hạn 10 MB và 40 triệu pixel. Các lỗi tệp rỗng, tệp giả ảnh, định dạng không hỗ trợ và ảnh hỏng được trả về rõ ràng. Sau xử lý hướng ảnh, dữ liệu RGB được giữ dưới dạng PIL khi chuyển cho Ultralytics. Cách này tránh việc một mảng RGB bị thư viện hiểu là BGR và đảo sai kênh màu.
Cả hai mô hình được chuyển về float32; nhánh predict sử dụng half=False. Dịch vụ trả thông tin phát hiện, nhãn, độ tin cậy, số mặt nạ, thời gian xử lý và ảnh overlay JPEG mã hóa Base64. Độ tin cậy của dự đoán không phải xác suất bệnh ác tính; diện tích mặt nạ ở mức pixel cũng không tự chuyển được thành kích thước tổn thương theo milimét nếu không có hiệu chuẩn hình học.
@TABLE api
### 4.4.3 Điều phối yêu cầu và xử lý lỗi
Các endpoint Mobile sử dụng requestId để theo dõi yêu cầu và trả lỗi JSON thống nhất. Dịch vụ giới hạn số lượt suy luận đồng thời bằng semaphore, áp dụng timeout chờ hàng đợi và timeout xử lý. Mỗi runtime còn có khóa bảo vệ mô hình. Khi một mô hình không sẵn sàng, API cần phản ánh trạng thái degraded hoặc unavailable thay vì trả một kết quả suy luận giả.
Thời gian trong phản hồi được đo quanh lệnh predict. Nó có thể bao gồm khởi tạo predictor ở lần đầu và không nhất thiết bao gồm tải ảnh qua mạng, thời gian chờ, mã hóa ảnh hoặc lưu lịch sử ở tầng Web. Do đó, không dùng trực tiếp thời gian của một yêu cầu minh họa để tuyên bố FPS ổn định cho cả ứng dụng.
## 4.5 Chức năng Web và Mobile
### 4.5.1 Ứng dụng Web
Web cung cấp trang tải ảnh phân tích đơn, trang so sánh hai mô hình trên cùng ảnh, trang kết quả và lịch sử. Nhánh so sánh sử dụng cùng ảnh đầu vào và lưu hai kết quả theo một comparison group. Tầng dịch vụ kiểm tra quyền sở hữu khi truy xuất, xuất hoặc xóa bản ghi. Trang quản trị phục vụ quản lý người dùng và thống kê của ứng dụng.
Khi chuyển phiên bản nghiên cứu, tên mô hình trong lựa chọn, khóa gửi API và tên trả về phải đồng nhất. Chỉ đổi nhãn hiển thị mà không đổi checkpoint hoặc lớp tùy biến sẽ không tạo ra một phép so sánh đúng. Lịch sử của nghiên cứu cũ cần được nhận biết theo modelType đã lưu, không được đổi dữ liệu cũ thành kết quả TSVM FP32 chỉ bằng cách đổi tên giao diện.
### 4.5.2 Ứng dụng Mobile Direct AI
Mobile có các màn hình trạng thái dịch vụ, chọn ảnh, phân tích đơn và so sánh trực tiếp. Danh sách mô hình lấy từ API phải khớp hai khóa được hỗ trợ. Ảnh overlay được giải mã từ Base64 và hiển thị cùng thông tin model, confidence, số mặt nạ và thời gian. Địa chỉ dịch vụ được truyền bằng AI_BASE_URL; khi chạy trên điện thoại cần dùng địa chỉ mạng có thể truy cập từ thiết bị.
Nhánh Mobile Direct AI không được mô tả như đã có lưu hồ sơ bệnh án hoặc đồng bộ lịch sử với Web nếu luồng đó không được triển khai. Phạm vi ứng dụng hiện tại là minh họa nghiên cứu trên ảnh tĩnh. Các chức năng video thời gian thực, định lượng kích thước vật lý và hỗ trợ quyết định lâm sàng cần một quy trình phát triển và kiểm chứng riêng.
## 4.6 Kiểm tra tích hợp với checkpoint thực nghiệm
@TABLE app_tests
Hai checkpoint seed 0 đã được nạp với đúng task segment và lớp polyp; các tensor dấu phẩy động trong mô hình sau tải là float32 và hữu hạn. Kiểm tra thực hiện dự đoán trên cùng một ảnh có polyp và một ảnh normal-cecum cho cả hai mô hình, với ngưỡng confidence 0,25. Cả hai mô hình trả một mặt nạ trên ảnh polyp và không trả mặt nạ trên ảnh nền trong hai ví dụ này.
@FIG qualitative|Hình 4.2 Ví dụ suy luận thực tế của hai checkpoint seed 0 và đường bao nhãn đối chiếu
Hình 4.2 dùng cùng ảnh và cùng checkpoint đã nạp vào dịch vụ. Confidence của hai mô hình khác nhau, nhưng không được dùng một ảnh để suy luận mô hình nào tốt hơn trên toàn bộ dữ liệu. Đường bao nhãn trong hình được dựng từ nhãn YOLO hiện có, không phải một lần gán nhãn y khoa mới. Các kiểm tra giao thức với mô hình giả lập được tách khỏi kiểm tra tải và suy luận với checkpoint thật.
## 4.7 Vận hành và giới hạn ứng dụng
Để vận hành, khởi động dịch vụ AI trước, kiểm tra /health và /api/v1/models, sau đó chạy Spring Boot hoặc Flutter. Web cần cấu hình MongoDB và kho lưu ảnh; Mobile Direct AI chỉ cần kết nối được dịch vụ AI. Tham số đường dẫn checkpoint có thể thay bằng biến môi trường AI_BASELINE_MODEL_PATH và AI_VMAMBA_MODEL_PATH. Các thông tin đăng nhập cá nhân và mật khẩu không được đưa vào báo cáo hoặc bản mã chia sẻ.
Phần mềm là sản phẩm minh họa của đề tài. Kết quả cần được người dùng xem cùng ảnh gốc và bối cảnh nghiên cứu; mô hình chưa được đánh giá tiền cứu trên một quy trình khám bệnh. Việc kiểm tra API, Web hoặc Mobile thành công xác nhận hành vi phần mềm trong các ca kiểm thử, không chứng nhận khả năng sử dụng như thiết bị y tế.
## 4.8 Tóm tắt chương
Chương này nối kết cấu hình thực nghiệm với dịch vụ suy luận và hai client của PolypVision. Việc chuyển sang checkpoint S và TSVM FP32 bao gồm cả tên định danh, mã kiến trúc, độ chính xác số và đường truyền ảnh. Các kết quả kiểm tra phần mềm được trình bày riêng với đánh giá chất lượng mô hình ở chương tiếp theo.

# CHƯƠNG 5 THỬ NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ
## 5.1 Thiết kế so sánh và nguồn số liệu
### 5.1.1 Đơn vị thực nghiệm
Phép so sánh chính gồm 20 cặp seed từ 0 đến 19, tức 40 lượt huấn luyện. Mọi lượt có 100 dòng epoch. Nhóm baseline nằm trong YOLOv26s-seg, còn nhóm đề xuất nằm riêng trong Kvasir_BG20_YOLO26s_seg_TSVM_FP32. Cùng chỉ số seed được ghép để phân tích chênh lệch giữa hai kiến trúc; epoch không được coi là 100 quan sát độc lập của hiệu năng cuối cùng.
Việc cố định dữ liệu và cấu hình làm giảm một số nguồn biến thiên, nhưng không bảo đảm hai mạng tiêu thụ chuỗi số ngẫu nhiên giống nhau vì cấu trúc và số tham số khác nhau. Hai mươi seed phản ánh độ nhạy với khởi tạo và tối ưu hóa trên cùng tập chia, không tương đương 20 lần lấy mẫu bệnh nhân hoặc 20 tập kiểm thử độc lập.
### 5.1.2 Quy tắc chọn epoch
Để nhất quán với bộ tổng hợp FP32 đã lưu, mỗi lượt được lấy tại epoch có metrics/mAP50-95(M) lớn nhất; các chỉ số còn lại lấy trên chính dòng đó. Nếu có nhiều epoch bằng nhau, chọn lần xuất hiện đầu tiên. Quy tắc này có tính chọn lọc theo tập kiểm định và tạo mức lạc quan so với một tập kiểm thử chưa dùng để chọn mô hình.
Ultralytics chọn best.pt theo fitness của box và mask, trong fork này là tổng hai thành phần mAP50–95. Đối chiếu lịch sử ghi nhận 16/40 lượt có epoch tối đa mask khác epoch tối đa fitness. Vì vậy, bảng kết quả chương này mô tả lịch sử huấn luyện tại mốc chọn theo mask; các checkpoint seed 0 trong ứng dụng có danh tính riêng và không được mặc nhiên gán mọi số của bảng tổng hợp.
### 5.1.3 Kiểm tra nhất quán
Số liệu được trích lại trực tiếp từ 40 results.csv và đối chiếu với raw_20seeds_extracted_metrics.csv. Trung bình, độ lệch chuẩn, paired t-test, Wilcoxon và khoảng tin cậy được tính lại; các giá trị tương ứng khớp bộ tổng hợp. Các args.yaml được so sánh trên những tham số ảnh hưởng đến huấn luyện. Quá trình này không chạy lại huấn luyện hoặc thay đổi những tệp kết quả gốc.
## 5.2 Độ đo và phương pháp thống kê
### 5.2.1 Các độ đo phát hiện và mặt nạ
IoU đo phần giao chia phần hợp giữa vùng dự đoán và nhãn. Precision và Recall được tính theo các đối tượng dự đoán sau quy tắc ghép; AP tổng hợp đường cong precision–recall ở một ngưỡng IoU. mAP50 dùng ngưỡng 0,50, còn mAP50–95 lấy trung bình ở các ngưỡng từ 0,50 đến 0,95 với bước 0,05. Trong bài toán một lớp, phép trung bình theo lớp chỉ có lớp polyp.
@EQ IoU = |P ∩ G| / |P ∪ G| ; Dice = 2|P ∩ G| / (|P| + |G|)
@EQ Precision = TP/(TP + FP) ; Recall = TP/(TP + FN)
Các chỉ số có hậu tố M thuộc đánh giá mặt nạ, hậu tố B thuộc hộp bao. Dice và IoU theo điểm ảnh có thể được sử dụng trong các bài báo phân đoạn ngữ nghĩa, nhưng không được suy ra từ mAP hoặc từ Precision/Recall theo đối tượng. Bộ CSV thực nghiệm chính hiện không có Dice theo ảnh hoặc HD95 nên không điền các chỉ số đó bằng công thức thay thế.
### 5.2.2 So sánh ghép cặp và khoảng tin cậy
Với mỗi seed i, đặt dᵢ bằng chỉ số TSVM trừ baseline. Trung bình chênh lệch và khoảng tin cậy được tính trên 20 dᵢ. Báo cáo dùng độ lệch chuẩn mẫu với mẫu số n−1. Các khoảng tin cậy của chênh lệch dùng phân bố t với 19 bậc tự do; kiểm định hai phía lấy mức tham chiếu α bằng 0,05 [23].
@EQ dᵢ = TSVMᵢ − Baselineᵢ ; KTC₉₅% = d̄ ± t₀․₉₇₅,₁₉ · s_d/√20
Paired t-test kiểm tra giả thuyết trung bình chênh lệch bằng 0. Wilcoxon signed-rank là phân tích bổ sung theo thứ hạng của các chênh lệch [24]. Kiểm định dấu xét số seed TSVM cao hơn baseline. Mỗi phép kiểm trả lời một câu hỏi khác nhau; p-value không phải xác suất giả thuyết đúng và p lớn hơn 0,05 không chứng minh hai mô hình tương đương.
Mask mAP50–95 là độ đo chính. Các chỉ số còn lại được xem là bổ sung hoặc thăm dò. Khi xem đồng thời nhiều p-value, nguy cơ tìm thấy một kết quả nhỏ do ngẫu nhiên tăng lên. Báo cáo không lựa chọn riêng một kiểm định thuận lợi để tuyên bố ưu thế; kết quả về phương sai được diễn giải thận trọng cùng quy mô mẫu và việc dùng nhiều độ đo.
## 5.3 Kết quả tổng hợp qua 20 seed
@TABLE main_metrics
Mask mAP50–95 tăng từ 0,718868 lên 0,723171, tức chênh 0,004303 trên thang 0–1, tương ứng 0,4303 điểm phần trăm. Độ lệch chuẩn giữa seed giảm từ 0,011768 xuống 0,007197, tương ứng giảm khoảng 38,85%. Hai con số mô tả hai mặt khác nhau: mức trung bình và biến thiên giữa các lượt, không phải cùng một bằng chứng.
Mask mAP50 tăng nhẹ 0,1385 điểm phần trăm. Mask Precision tăng khoảng 1,0356 điểm phần trăm trong khi Mask Recall giảm khoảng 0,0388 điểm phần trăm. Do đó, không thể mô tả tất cả chỉ số đều tăng. Val segmentation loss trung bình thấp hơn ở TSVM FP32, nhưng loss tại epoch chọn theo mAP không nhất thiết là loss nhỏ nhất của lượt đó.
@FIG paired|Hình 5.1 Kết quả ghép cặp của mask mAP50 95 và Precision trên 20 seed
Mỗi đường nối trong Hình 5.1 biểu diễn cùng một seed ở hai kiến trúc. Có cả đường tăng và đường giảm, cho thấy mức cải thiện phụ thuộc lượt khởi tạo. Việc hiển thị từng cặp giúp tránh che lấp các trường hợp TSVM thấp hơn baseline khi chỉ nhìn cột trung bình.
## 5.4 Bằng chứng thống kê và độ ổn định
@TABLE inference
Với độ đo chính, paired t-test cho p = 0,0614 và Wilcoxon cho p = 0,0696. Khoảng tin cậy 95% của chênh lệch là [−0,000228; 0,008834], chứa 0. Vì vậy, dữ liệu hiện tại cho thấy xu hướng tăng trung bình nhưng chưa đủ bằng chứng ở ngưỡng 0,05 để kết luận TSVM có trung bình mask mAP50–95 cao hơn baseline.
@FIG ci|Hình 5.2 Chênh lệch và khoảng tin cậy 95 phần trăm của các chỉ số
Các khoảng trong Hình 5.2 cùng giao đường 0 đối với các chỉ số thể hiện. Phần dương của khoảng thể hiện những mức tăng phù hợp với số liệu; phần âm thể hiện những mức giảm vẫn chưa bị loại trừ. Khoảng tin cậy giúp đọc cả độ lớn và độ bất định, thay vì chỉ phân loại theo một p-value.
@FIG distribution|Hình 5.3 Phân bố mask mAP50 95 giữa các seed
TSVM cao hơn baseline ở 13/20 seed, baseline cao hơn ở 7/20 seed; kiểm định dấu hai phía cho p = 0,2632. Số lượt thắng 65% là thống kê mô tả của 20 cặp, chưa phải xác suất tổng quát rằng TSVM sẽ thắng trong một lần huấn luyện tương lai. Giá trị nhỏ nhất của TSVM cao hơn baseline trong tập seed đang quan sát, nhưng baseline có giá trị cực đại cao hơn TSVM.
Kiểm định Levene theo trung vị đối với mask mAP50–95 cho p khoảng 0,0257. Kết quả này hỗ trợ thăm dò về khác biệt phân tán, nhưng các nhóm có ghép seed và có nhiều kiểm định bổ sung. Báo cáo ưu tiên mô tả độ lệch chuẩn quan sát được, không khẳng định đã chứng minh một quy luật ổn định cho mọi dữ liệu hoặc cấu hình.
## 5.5 Kết quả từng seed và diễn biến huấn luyện
@FIG seed_delta|Hình 5.4 Chênh lệch mask mAP50 95 của từng cặp seed
@TABLE seed_results
Các seed cùng chạy trên một tập chia nên sự khác biệt trong Hình 5.4 chủ yếu phản ánh tối ưu hóa và cách các kiến trúc phản ứng với chuỗi ngẫu nhiên. Không thể dùng bảng này để suy ra khoảng tin cậy theo bệnh nhân. Muốn đánh giá tính tổng quát, cần tập kiểm thử bên ngoài hoặc cách chia theo bệnh nhân bên cạnh việc lặp seed.
@FIG curves|Hình 5.5 Trung bình và độ lệch chuẩn mask mAP50 95 theo epoch
@FIG loss|Hình 5.6 Trung bình và độ lệch chuẩn mất mát phân đoạn kiểm định theo epoch
Vùng tô trong hai hình là trung bình cộng trừ một độ lệch chuẩn giữa 20 seed ở từng epoch, không phải khoảng tin cậy của mô hình tốt nhất. Chỉ số và loss có thể dao động ở cuối huấn luyện; epoch chọn tốt nhất trung bình của TSVM muộn hơn baseline không tự chứng minh mô hình hội tụ nhanh hơn. Tương tự, độ rộng vùng min–max ở từng epoch và độ lệch chuẩn của chỉ số cuối là hai phép mô tả khác nhau.
## 5.6 Ma trận nhầm lẫn và nhận xét định tính
Bộ tổng hợp có các giá trị TP, FP và FN được đọc từ hình ma trận nhầm lẫn theo đối tượng. Chúng được tạo ở một cấu hình đánh giá và ngưỡng confidence cụ thể; không đồng nhất với điểm Precision/Recall được chọn từ đường cong AP hoặc với từng dòng epoch tối đa mask. Vì vậy, phần này dùng chúng như số liệu bổ sung và ghi rõ nguồn, không tái tạo mAP từ ma trận đó.
@TABLE confusion
Ô TN trong ma trận Ultralytics không được tích lũy theo cách đếm ảnh nền đúng. Cột TN_reconstructed trong bộ tổng hợp tính bằng 40 trừ số FP; phép tính đó không hợp lệ vì FP là số đối tượng dự đoán sai và có thể xuất hiện cả trên ảnh có polyp. Một ảnh có thể có nhiều FP. Do đó, báo cáo không tính specificity, accuracy hai lớp hoặc tỷ lệ ảnh nền báo động giả từ cột này.
Ảnh minh họa ở Chương 4 cho thấy khả năng nạp và trả mặt nạ của hai checkpoint, nhưng không được dùng như một bộ đánh giá định tính đã chọn mẫu đầy đủ. Một nghiên cứu về biên cần chọn ca trước khi xem kết quả, nêu tiêu chí ca khó, sử dụng cùng ảnh và checkpoint, rồi đo thêm Boundary F1 hoặc HD95. Những nội dung đó được đưa vào kế hoạch mở rộng thay vì mô tả như đã hoàn thành.
## 5.7 Chi phí mô hình và khả năng triển khai
Hai checkpoint ứng dụng có lần lượt 11.434.463 và 12.254.688 tham số, tương ứng tăng 820.225 tham số, khoảng 7,17%. Số tham số được đếm trực tiếp sau nạp mô hình và không đổi chỉ vì chọn FP32 thay FP16. Kích thước tệp TSVM FP32 lớn hơn còn do số byte biểu diễn mỗi tham số và cấu trúc checkpoint, nên cần tách riêng dung lượng khỏi số tham số.
@TABLE efficiency
Thư mục benchmark cũ có số đo CPU và kích thước checkpoint TSVM khoảng 23,86 MB, thuộc giai đoạn không lưu FP32. Những kết quả đó không được gán cho bản TSVM FP32 mới. Các lần suy luận minh họa hiện có cũng không có warmup và lặp đủ nhiều để làm benchmark. Vì vậy báo cáo chưa đưa ra kết luận FPS, GFLOPs, VRAM hoặc độ trễ GPU cho cặp checkpoint FP32.
Một phép đo hiệu năng tiếp theo cần xác định CPU/GPU, số luồng, batch, kích thước đầu vào, warmup, số lần lặp, đồng bộ CUDA, phiên bản thư viện và phạm vi đo. Có thể báo cáo median cùng p95 và tách thời gian predict khỏi thời gian toàn trình API. Cấu hình FP32 phải được duy trì giống khi sử dụng mô hình cải tiến trong ứng dụng.
## 5.8 Đối chiếu kết quả công bố trong tài liệu
@TABLE literature_results
Các kết quả trong Bảng 5.8 là số do tác giả bài báo công bố, không phải thực nghiệm chạy lại của đề tài. Mỗi nguồn sử dụng cách chia dữ liệu, kích thước ảnh và mô hình khác nhau. Chỉ số Dice/IoU theo điểm ảnh không cùng định nghĩa với mask mAP50–95 theo đối tượng, nên bảng cung cấp bối cảnh nghiên cứu và không tạo bảng xếp hạng trực tiếp giữa TSVM của đề tài và các phương pháp đó.
Để có đối chiếu định lượng trực tiếp, cần lấy cùng dữ liệu và cách chia, giữ nguyên ground truth, quy định cách hợp nhất các instance mask thành mặt nạ semantic, nêu xử lý ảnh rỗng và tính các độ đo giống nhau. Khi bổ sung ảnh nền, không được để số lượng điểm ảnh nền lớn làm chỉ số accuracy che lấp chất lượng vùng polyp.
## 5.9 Hạn chế và nguy cơ ảnh hưởng độ tin cậy
Tập kiểm định đã được dùng để chọn epoch nên kết quả có thể lạc quan. Không có tập test độc lập hoặc định danh bệnh nhân làm hạn chế đánh giá khả năng khái quát. Nguồn âm normal-cecum chưa bao phủ mọi mô lành và các lớp tổn thương khác. Việc chia sẻ cùng seed không bảo đảm mọi biến ngẫu nhiên tương ứng giữa hai mạng.
Chưa có ablation đủ seed để tách vai trò SS2D, shape và guidance. Chưa có Dice/IoU theo điểm ảnh, HD95 hay lỗi topology được tính lại trên cùng checkpoint. Số liệu TP/FP/FN từ hình có thêm giới hạn của việc trích xuất và khác ngưỡng đánh giá. Kết quả 20 seed theo lịch sử train cần phân biệt với một đợt đánh giá lại toàn bộ best.pt sau lưu FP32.
Các giới hạn này không làm mất giá trị của việc triển khai và kiểm tra kiến trúc, nhưng xác định mức độ kết luận phù hợp. Kết quả hiện hỗ trợ khả năng triển khai kỹ thuật và xu hướng tăng mask mAP cùng độ phân tán nhỏ hơn; chưa hỗ trợ tuyên bố vượt trội có ý nghĩa thống kê, bảo toàn topology hoặc hiệu quả lâm sàng.
## 5.10 Tóm tắt chương
Trên 20 cặp seed, TSVM FP32 có mask mAP50–95 trung bình cao hơn 0,4303 điểm phần trăm và độ lệch chuẩn giữa seed nhỏ hơn baseline. Khoảng tin cậy chênh lệch vẫn chứa 0, phù hợp với p-value chưa đạt ngưỡng 0,05. Phân tích đã tách lịch sử huấn luyện, checkpoint ứng dụng, số liệu ma trận nhầm lẫn và kết quả bài báo để tránh so sánh không cùng điều kiện.

# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
## Kết quả đạt được
Đề tài đã xây dựng khối C2TSVMamba thay C2PSA ở tầng 10 của YOLO26s-seg và trình bày luồng tính toán giữa SS2D bốn hướng với nhánh hình dạng đa tỉ lệ, có hướng. Bộ BG20 được tổ chức đúng định dạng instance segmentation, sử dụng nhãn rỗng cho mẫu âm. Phần mô tả tiền xử lý được đối chiếu với tài liệu chuyên biệt, mã chuyển nhãn và cấu hình tăng cường dữ liệu.
Thực nghiệm chính gồm 40 lượt, mỗi lượt 100 epoch; số liệu và thống kê được trích lại nhất quán cho 20 cặp seed. Mask mAP50–95 tăng từ 0,718868 ± 0,011768 lên 0,723171 ± 0,007197. Tuy nhiên, paired t-test p = 0,0614 và khoảng tin cậy chứa 0 nên chưa kết luận ưu thế trung bình ở mức 0,05. Đây là kết quả cần được báo cáo cùng mức độ bất định, thay vì chỉ nêu một tỷ lệ tăng.
PolypVision đã được chuyển từ hai mô hình Nano của giai đoạn trước sang cặp checkpoint YOLO26s-seg và TSVM FP32. Dịch vụ đăng ký đúng module tùy biến, giữ suy luận float32 và truyền ảnh đúng quy ước RGB. Kết quả nạp và dự đoán trên ảnh minh họa xác nhận đường tích hợp kỹ thuật, trong khi các kiểm thử API và client xác nhận các hành vi phần mềm tương ứng.
## Giới hạn của kết luận
Nghiên cứu chưa có tập test ngoài, ablation đầy đủ hoặc bằng chứng topology tường minh. Bộ chỉ số hiện có thiên về phát hiện từng đối tượng, nên chưa trả lời hoàn chỉnh câu hỏi về độ bám biên theo điểm ảnh. Ứng dụng phục vụ minh họa, chưa được đánh giá trong quy trình lâm sàng. Việc duy trì FP32 là điều kiện bảo toàn checkpoint và không tự chứng minh một cải tiến kiến trúc về độ chính xác.
## Hướng phát triển
Ưu tiên đầu tiên là đánh giá lại cùng một tập kiểm định từ các checkpoint đã lưu, dùng chính xác tiêu chí chọn best.pt và lưu kết quả dạng JSON/CSV. Tiếp theo là đánh giá trên tập ngoài như ClinicDB, ColonDB và ETIS theo một giao thức thống nhất, đồng thời bổ sung các nhóm ảnh âm đa dạng hơn. Những phép đo này cần hoàn tất trước khi đưa ra kết luận về khái quát hóa.
Về phương pháp, cần chạy bốn chế độ ablation với ngân sách seed phù hợp, bổ sung độ đo biên và lỗi liên thông. Nếu tiếp tục dùng thuật ngữ topology-aware như một đóng góp chính, cần kiểm chứng bằng Betti errors hoặc phương pháp topology phù hợp. Về triển khai, có thể nghiên cứu chuẩn hóa đầu ra SS2D và kernel quét hiệu quả hơn; mọi tối ưu precision phải được kiểm tra lại trên checkpoint và chất lượng phân đoạn.
Về ứng dụng, hướng mở rộng gồm ghi metadata checkpoint trong từng bản ghi, tạo báo cáo so sánh có thể truy vết, và kiểm thử toàn trình với môi trường triển khai được cố định. Video, tải đồng thời và thời gian đáp ứng cần benchmark riêng. Các chức năng này là kế hoạch phát triển, không được cộng vào những kết quả đã hoàn thành của thực nghiệm ảnh tĩnh.

@REFERENCES
@APPENDICES
