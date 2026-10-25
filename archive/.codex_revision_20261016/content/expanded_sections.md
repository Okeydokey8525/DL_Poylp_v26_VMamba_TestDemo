# Nội dung mở rộng đề xuất cho bản báo cáo ngày 16 tháng 10 năm 2026

Tài liệu này cung cấp các đoạn viết sẵn để CHÈN THÊM sau nội dung hiện có tại từng đề mục được ghi bên dưới. Không thay thế các đoạn đúng, bảng và hình đã có. Số tài liệu [1] đến [24] giữ theo danh mục của bản báo cáo hiện tại. Các đoạn không chứa chỉ dẫn biên tập có thể đưa trực tiếp vào Word.

## Chèn tại MỞ ĐẦU mục 1 Lý do chọn đề tài

Trong bài toán xử lý ảnh nội soi, phát hiện và phân đoạn giải quyết hai mức yêu cầu khác nhau. Hộp bao giúp định vị nhanh một vùng nghi ngờ nhưng có thể bao gồm một phần niêm mạc ngoài đối tượng. Mặt nạ mô tả vùng đối tượng chi tiết hơn, thuận lợi cho việc quan sát đường bao và đối chiếu dự đoán với nhãn chuyên gia của bộ dữ liệu. Tuy vậy, đầu ra mặt nạ vẫn chỉ là kết quả của mô hình trên ảnh quan sát; nó không cung cấp kết luận mô bệnh học hay xác định mức độ ác tính. Việc chọn phân đoạn từng đối tượng trong đề tài xuất phát từ yêu cầu kỹ thuật mô tả vùng polyp cụ thể hơn, đồng thời duy trì đầu ra hộp bao và độ tin cậy trong cùng một luồng suy luận.

Một khó khăn của nghiên cứu là kết quả tốt trong một lượt huấn luyện chưa phản ánh đầy đủ hành vi của kiến trúc. Khởi tạo trọng số, thứ tự mẫu và các phép tăng cường dữ liệu có thể làm thay đổi quá trình tối ưu hóa ngay cả khi dùng cùng tập chia. Nếu chỉ chọn lượt tốt nhất của mỗi mô hình, sự khác biệt quan sát được có thể trộn lẫn tác động của thiết kế với thuận lợi ngẫu nhiên của lượt chạy. Vì vậy, đề tài sử dụng 20 seed cho mỗi kiến trúc, trình bày cả mức trung bình, độ phân tán và chênh lệch ghép cặp. Cách tiếp cận này giúp đặt câu hỏi về độ ổn định của kết quả bên cạnh câu hỏi về mức chính xác cao nhất.

Đề tài cũng quan tâm đến khoảng cách giữa mã huấn luyện và phần mềm minh họa. Một checkpoint có thể tồn tại trên đĩa nhưng vẫn không dùng được trong ứng dụng nếu thiếu lớp tùy biến, sai quy mô mô hình hoặc sai kiểu dữ liệu khi nạp. Đối với SS2D tùy biến, chuyển kiểu số trong quá trình lưu còn có thể ảnh hưởng các tensor trạng thái. Vì vậy, tính tương thích của checkpoint FP32, tên định danh mô hình và đường truyền ảnh được xem là bộ phận của quy trình thực hiện, thay vì chỉ là công việc bổ sung sau khi hoàn thành bảng kết quả.

## Chèn tại MỞ ĐẦU mục 2 Mục tiêu và câu hỏi nghiên cứu

Để thực hiện mục tiêu trên, khóa luận triển khai các nhiệm vụ gắn với những sản phẩm có thể kiểm tra. Nhiệm vụ về dữ liệu tạo bộ ảnh và nhãn YOLO thống nhất, gồm cả ảnh không có đối tượng; nhiệm vụ về mô hình xác định vị trí thay thế C2PSA, mô tả C2TSVMamba và kiểm tra luồng kích thước tensor; nhiệm vụ về thực nghiệm tổ chức kết quả riêng theo seed và kiểm tra cấu hình đã lưu. Nhiệm vụ phân tích tổng hợp số liệu theo một quy tắc chọn epoch công khai, còn nhiệm vụ ứng dụng kết nối checkpoint thực nghiệm với dịch vụ AI và hai client Web, Mobile.

Các nhiệm vụ này tương ứng với bốn nhóm căn cứ trong báo cáo: mã nguồn và YAML để giải thích thiết kế; ảnh, nhãn và thống kê dữ liệu để mô tả đầu vào; args.yaml, results.csv và tệp tổng hợp để đánh giá thực nghiệm; mã ứng dụng, manifest checkpoint và kiểm tra tích hợp để xác nhận khả năng sử dụng trong phần mềm. Khi một kết luận không có căn cứ tương ứng, báo cáo chỉ nêu nó như giả thuyết hoặc hướng phát triển. Chẳng hạn, nhánh có hướng tạo động cơ khảo sát biên, nhưng chưa đủ để tuyên bố cải thiện HD95 khi thực nghiệm chưa đo chỉ số này.

Mức hoàn thành của nghiên cứu được xác định bằng việc thiết kế có thể được giải thích, kết quả có thể được truy nguyên và checkpoint có thể được nạp đúng trong ứng dụng. Mức tăng của một chỉ số không phải điều kiện để lựa chọn hoặc loại bỏ số liệu. Nếu kết quả ghép cặp chưa đủ bằng chứng thống kê, khóa luận vẫn cần báo cáo đầy đủ kết quả đó và xác định thí nghiệm tiếp theo cần thực hiện.

## Chèn tại MỞ ĐẦU mục 3 Đối tượng và phạm vi nghiên cứu

Trong phạm vi dữ liệu, BG20 là tên thiết lập bổ sung 200 ảnh nền vào 1.000 ảnh Kvasir-SEG, không có nghĩa 20% tổng 1.200 ảnh đều là ảnh nền. Tỷ lệ nền trên toàn bộ dữ liệu là 16,67%; các tập train và validation có tỷ lệ khác nhau theo danh sách đã được tạo. Các seed của thực nghiệm thay đổi quá trình huấn luyện trên cùng danh sách này, không tạo lại 20 phép chia dữ liệu. Vì vậy, nghiên cứu đánh giá biến thiên do tối ưu hóa trong một thiết lập cố định và chưa lượng hóa toàn bộ bất định do lấy mẫu dữ liệu.

Trong phạm vi hệ thống, Web và Mobile sử dụng ảnh tĩnh tải lên. Báo cáo phân biệt thời gian tính toán mô hình với thời gian của một yêu cầu ứng dụng, vì yêu cầu còn có truyền mạng, giải mã ảnh và tạo kết quả hiển thị. Thực nghiệm hiệu năng chỉ được sử dụng trong điều kiện phần cứng, số lần lặp và phạm vi đo đã công bố. Việc chạy được trên máy cá nhân chưa đủ để suy rộng sang thiết bị nội soi chuyên dụng hoặc khẳng định vận hành video thời gian thực.

## Chèn tại MỞ ĐẦU mục 4 Phương pháp thực hiện và đóng góp

Quy trình nghiên cứu bắt đầu bằng khảo sát các hướng phân đoạn dựa trên CNN, mô hình trạng thái và cơ chế hướng dẫn cấu trúc, sau đó đối chiếu với mã nguồn đang sử dụng. Bước mô hình hóa xác định giả thuyết: ngữ cảnh từ SS2D có thể bổ sung thông tin cho nhánh hình dạng, còn nhánh hình dạng có thể điều chỉnh đáp ứng toàn cục trước hợp nhất. Bước thực nghiệm giữ cố định những điều kiện có thể đối chiếu và lưu kết quả của cả hai nhóm. Bước phân tích xem xét giả thuyết qua độ đo đã xác định, không suy ngược cơ chế từ một biểu đồ thuận lợi.

Giá trị khoa học của khóa luận nằm ở một trường hợp tích hợp cụ thể được mô tả đến mức có thể tái lập, cùng cách phân biệt kiến trúc, độ chính xác số và quy tắc tổng hợp kết quả. Giá trị thực hành nằm ở quy trình chuyển đổi nhãn, tổ chức các lượt chạy và tích hợp checkpoint vào PolypVision. Các sản phẩm này có thể phục vụ học tập, trình diễn và kiểm thử phương pháp trên ảnh công khai. Chúng chưa thay thế một nghiên cứu đánh giá lâm sàng trên bệnh nhân hoặc một hệ thống được chứng nhận sử dụng trong khám chữa bệnh.

## Chèn tại 1.1.1 Phân đoạn ngữ nghĩa và phân đoạn từng đối tượng

Có thể biểu diễn một mẫu có nhãn bằng cặp ảnh I và tập đối tượng G = {g₁, g₂, …, gₘ}. Mỗi đối tượng đi kèm lớp, hộp bao suy ra từ vùng nhãn và mặt nạ hoặc đa giác. Đầu ra mô hình là một tập dự đoán có số phần tử thay đổi, mỗi phần tử gồm hộp bao, điểm tin cậy, lớp và mặt nạ. Với ảnh nền, m bằng 0 và đầu ra mong muốn là tập rỗng. Biểu diễn này giải thích vì sao số đối tượng, số ảnh và số pixel phải được thống kê riêng, cũng như vì sao tệp nhãn rỗng là một mẫu hợp lệ của bài toán.

Từ góc độ đánh giá, mô hình có thể định vị một đối tượng tương đối đúng nhưng dự đoán đường bao còn thô; ngược lại, mặt nạ có hình dạng hợp lý nhưng không được ghép thành true positive nếu không đạt ngưỡng IoU đang xét. Vì vậy, một kết quả hộp bao tốt chưa thay thế được đánh giá mặt nạ. Báo cáo giữ riêng các chỉ số Box và Mask, đồng thời không đồng nhất F1 tính trên đối tượng với Dice tính trên pixel. Hai đại lượng chỉ có cùng dạng công thức khi dùng cùng định nghĩa TP, FP và FN trên cùng không gian đánh giá.

## Chèn tại 1.1.2 Các khó khăn về hình ảnh và dữ liệu

Các khó khăn về hình ảnh còn tác động khác nhau ở từng giai đoạn xử lý. Khi co ảnh về kích thước đầu vào, đối tượng chiếm ít diện tích có thể chỉ còn một số ít ô đặc trưng ở tầng sâu. Khi raster hóa đa giác hoặc tăng lại mặt nạ về kích thước ảnh gốc, đường bao có thể thay đổi do nội suy và ngưỡng hóa. Do đó, sai khác trên mặt nạ cuối cùng không nhất thiết chỉ bắt nguồn từ khối trích đặc trưng. Quy trình đánh giá cần giữ thống nhất kích thước đầu vào, cách hậu xử lý và dạng nhãn được dùng làm chuẩn.

Ảnh nội soi cũng có những dấu hiệu ngoài đối tượng như viền đen, ký hiệu và vùng thông tin chèn vào khung hình. Nếu các dấu hiệu đó liên quan đến nguồn dữ liệu, mô hình có thể tận dụng đặc điểm nguồn thay vì chỉ học cấu trúc polyp. Kiểm tra trùng ảnh bằng mã băm là một bước kiểm soát hữu ích nhưng chỉ loại trừ trùng khớp tệp chính xác; nó chưa xác định được ảnh gần trùng, các khung hình liền nhau hoặc nhiều ảnh của cùng bệnh nhân. Đây là lý do cần diễn giải mức tổng quát hóa phù hợp với metadata hiện có.

## Chèn tại 1.2.1 Mạng tích chập và kiến trúc encoder decoder

Trong các tầng nông, một kernel nhỏ quan sát vùng lân cận và học những biến đổi màu sắc, cạnh hoặc kết cấu. Khi xếp chồng nhiều tầng và giảm độ phân giải, trường tiếp nhận lý thuyết mở rộng, đồng thời đặc trưng mang nhiều thông tin ngữ nghĩa hơn. Vì vậy, không chính xác khi mô tả mọi mạng tích chập là hoàn toàn không có ngữ cảnh toàn cục. Vấn đề thiết kế là cơ chế trao đổi thông tin giữa các vị trí, chi phí tính toán và mức bảo toàn chi tiết không gian. Đề tài đưa thêm nhánh trạng thái để khảo sát một cách trao đổi thông tin bổ sung cho nền tích chập đã có.

Kết nối bỏ qua và hợp nhất đa mức giải quyết yêu cầu kết hợp ngữ nghĩa với định vị ở những cách khác nhau. Trong mạng encoder decoder, các tầng nông có thể được nối trực tiếp với tầng giải mã tương ứng; trong YOLO26-seg, các mức đặc trưng đi qua neck trước khi đầu dự đoán sử dụng chúng. Sự khác biệt về đường truyền đặc trưng và đầu ra khiến một module đạt kết quả tốt trong U-Net chưa đương nhiên đạt cùng tác dụng khi chuyển sang YOLO. Việc tích hợp cần được đánh giá như một cấu hình mới, dù nguyên lý thành phần có thể đã được công bố.

## Chèn tại 1.2.2 YOLO26 và đầu phân đoạn

Cơ chế mặt nạ nguyên mẫu giúp phân chia công việc thành hai phần. Nhánh prototype tạo một cơ sở mặt nạ dùng chung cho ảnh; nhánh hệ số xác định cách kết hợp cơ sở đó cho từng dự đoán. Số prototype là chiều biểu diễn của tổ hợp này, không phải số lượng polyp tối đa trong ảnh. Những mặt nạ prototype trung gian cũng không được xem riêng như nhãn giải phẫu vì chúng được tối ưu để phối hợp với hệ số đầu ra.

Ở giai đoạn suy luận, đầu ra cần được chuyển từ không gian đặc trưng về ảnh quan sát và áp dụng quy tắc chọn dự đoán của phiên bản đang dùng. Vì vậy, khi tái lập cần cố định không chỉ tên YOLO mà cả phiên bản Ultralytics, chế độ end2end, ngưỡng tin cậy và các tham số hậu xử lý liên quan. Việc đổi tên tệp trọng số hoặc dùng một lớp head khác có thể làm thay đổi hành vi ngay cả khi giao diện hiển thị vẫn ghi cùng tên mô hình.

## Chèn tại 1.3.1 Biểu diễn trạng thái chọn lọc

Trạng thái ẩn là một biểu diễn nén được cập nhật lần lượt theo vị trí chuỗi. Với cùng một đầu vào hiện tại, đầu ra có thể khác nhau nếu trạng thái tích lũy từ các vị trí trước khác nhau. Trong selective SSM, các đại lượng phụ thuộc nội dung làm cho mức cập nhật và cách đọc trạng thái thay đổi theo dữ liệu. Tuy nhiên, không nên gán sẵn ý nghĩa y khoa cho mỗi tham số, chẳng hạn khẳng định Δ luôn nhỏ ở vùng phản quang và luôn lớn tại biên polyp. Ý nghĩa đó chỉ có thể được khảo sát qua phân tích đáp ứng thực tế, chưa được bảo đảm bởi cấu trúc phương trình.

Ma trận chuyển trạng thái được tham số hóa để có các hệ số suy giảm; bước thời gian dương giúp định nghĩa mức chuyển tiếp tại từng vị trí. Tính chất này hỗ trợ cách mô hình hóa bộ nhớ trên chuỗi nhưng không tự bảo đảm mọi phép tính luôn ổn định ở tất cả kiểu số. Giá trị đầu vào, phép chiếu, phép tích lũy và các thống kê chuẩn hóa vẫn có thể có miền giá trị rộng. Vì vậy, phân tích cấu trúc trạng thái và kiểm tra kiểu số của checkpoint là hai công việc cần đi cùng nhau trong triển khai của khóa luận.

## Chèn tại 1.3.2 Cơ chế SS2D bốn hướng

Nếu chỉ trải bản đồ theo hàng, hai vị trí kề nhau theo cột có thể cách nhau W bước trên chuỗi, trong khi các vị trí ở cuối hàng và đầu hàng tiếp theo lại liên tiếp trong thứ tự xử lý. Bổ sung thứ tự theo cột giúp mạng có thêm một cách tiếp cận quan hệ lân cận. Các hướng đảo chiều cung cấp phụ thuộc từ chiều ngược lại khi kết quả được hợp nhất. Đây là cách xử lý ảnh thông qua nhiều thứ tự chuỗi, chưa phải một chứng minh rằng đầu ra bất biến với phép quay hoặc phản chiếu ảnh.

Sau quét, các phép đảo và chuyển vị phải được thực hiện ngược đúng với quá trình tạo chuỗi. Nếu ghép một chuỗi chưa phục hồi về cùng tọa độ, phép cộng sẽ kết hợp thông tin của những vị trí không tương ứng. Việc giải thích SS2D vì thế cần mô tả cả thứ tự quét lẫn bước đưa kết quả trở lại lưới H×W, thay vì chỉ liệt kê bốn hướng. Mã nguồn của đề tài thực hiện cả hai thao tác trước khi đưa tensor đến phép điều biến và chiếu đầu ra.

## Chèn tại 1.4.3 Phạm vi tính mới

Tính mới được xem xét trên ba mức. Ở mức nguyên lý, selective state space, quét nhiều hướng, convolution đa tỉ lệ và gating đều có các công trình trước. Ở mức tổ chức kiến trúc, đề tài xác định một đường truyền guidance cụ thể từ biểu diễn hình dạng sang nhánh SS2D rồi hợp nhất trong wrapper C2 tại P5. Ở mức thực nghiệm và triển khai, đề tài tổ chức 20 cặp seed trên BG20 và xử lý tính tương thích của checkpoint FP32 với ứng dụng. Việc tách ba mức giúp xác định đóng góp đúng phạm vi và tránh biến một tổ hợp kỹ thuật thành tuyên bố ưu tiên tuyệt đối.

Khảo sát tài liệu là căn cứ định vị chứ chưa thể chứng minh không có bất kỳ nhóm nào trên thế giới nghiên cứu cấu hình gần giống. Đặc biệt, các công trình gần về Mamba trong YOLO26 hoặc guidance cấu trúc cần được đối chiếu theo thời điểm công bố, nhiệm vụ, vị trí chèn module và loại tín hiệu điều khiển. Khóa luận vì vậy sử dụng cách diễn đạt “đề xuất và đánh giá một cấu hình tích hợp” thay cho khẳng định “lần đầu tiên” khi chưa có bằng chứng đầy đủ về quyền ưu tiên.

## Chèn tại 2.1 Kiến trúc đối chứng YOLO26s seg

Với tensor đầu vào B×3×640×640, các mức P3, P4 và P5 lần lượt có kích thước không gian 80×80, 40×40 và 20×20. P3 giữ nhiều vị trí không gian hơn nhưng mức ngữ nghĩa thấp hơn; P5 có ít vị trí hơn và được xây dựng từ nhiều tầng trích đặc trưng. Neck trao đổi thông tin giữa các mức bằng upsample, concatenate và các khối xử lý tiếp theo. Khối thay thế ở cuối backbone có thể ảnh hưởng những đặc trưng được truyền xuống các mức khác qua neck, dù nó không trực tiếp nằm trên bản đồ phân giải cao nhất.

Trong cấu hình đầu Segment26, 32 hệ số mặt nạ của mỗi đối tượng được kết hợp với 32 prototype dùng chung. Có thể viết logit mặt nạ của đối tượng i tại vị trí (u,v) dưới dạng tổng các tích aᵢⱼPⱼ(u,v), sau đó chuyển sang đáp ứng mặt nạ theo bước hậu xử lý tương ứng. Công thức mô tả cơ chế tổ hợp tuyến tính; các thao tác crop, nội suy và ngưỡng hóa cần được xem là những bước riêng khi tạo mặt nạ trên ảnh gốc. Nhờ đó, có thể phân biệt tác động lên đặc trưng với tác động của quy trình dựng mặt nạ đầu ra.

@EQ Mᵢ(u,v) = sigmoid(Σⱼ₌₁³² aᵢⱼPⱼ(u,v))

Phương án thay C2PSA được chọn nhằm giữ giao diện giữa backbone và neck tương thích. Nếu chèn thêm một tầng mà không điều chỉnh các chỉ số from trong YAML, những kết nối ghép đặc trưng và đầu Segment26 có thể trỏ sai tầng. Ở thiết kế hiện tại, vị trí tầng 10 được thay bằng C2TSVMamba nên các tham chiếu từ neck được giữ theo cùng cấu trúc chỉ số. Khả năng tương thích này cần được kiểm tra sau khi parser áp dụng scale, thay vì chỉ so sánh tên các dòng trong YAML.

## Chèn tại 2.2 Wrapper C2TSVMamba

Hai đường truyền trong wrapper tạo ra một phần đặc trưng được chuyển qua lõi tùy biến và một phần được giữ qua nhánh ngắn. Phép ghép kênh ở cuối không phải lấy trung bình hai nhánh; convolution 1×1 tiếp theo học cách kết hợp chúng. Vì vậy, ngay cả khi hệ số residual trong TSVMamba được khởi tạo nhỏ, toàn wrapper vẫn có các phép chiếu được huấn luyện. Cách mô tả này tránh coi module mới như một phép cộng gần bằng 0 hoàn toàn không thay đổi backbone lúc khởi tạo.

Số kênh của lõi 256 cũng là cơ sở để xác định đúng chi phí. Nếu lấy 512 kênh đầu vào wrapper làm số kênh của SS2D sẽ đánh giá sai kích thước các tensor trạng thái và các phép chiếu. Tương tự, repeats bằng 2 trên YAML là giá trị trước co giãn chiều sâu; số block thực sự của biến thể s là 1. Báo cáo sử dụng kích thước sau parser để giải thích mô hình đã chạy, còn giá trị trước parser được giữ để người đọc hiểu cách dùng cùng một YAML cho nhiều quy mô.

## Chèn tại 2.3.1 Nhánh SS2D toàn cục

Tại mỗi hướng, tín hiệu đầu vào được chiếu để sinh các hệ số phụ thuộc vị trí; trạng thái sau đó kết hợp thông tin hiện tại với trạng thái trước. Những hệ số này được chia sẻ hoặc bố trí theo các chiều tensor của triển khai, không phải một ma trận attention H×W giữa mọi cặp vị trí. Điều này tạo cơ chế truyền thông tin khác với self-attention. Mặc dù độ dài chuỗi ở P5 chỉ bằng 400, lõi vẫn phải xử lý chiều kênh và chiều trạng thái 16; chỉ nêu độ dài chuỗi sẽ chưa phản ánh đủ chi phí thực tế.

Nhánh z được tách từ phép chiếu đầu vào và điều biến đáp ứng sau quét. Nhánh này khác với guidance hình dạng: z thuộc cấu trúc nội bộ SS2D, còn guidance được tạo từ tensor S của nhánh ShapeAwareBranch. Hai tín hiệu tác động ở các vị trí khác nhau trong luồng tính toán. Khi thực hiện ablation no_guidance, cần hiểu phần bị bỏ là guidance giữa hai nhánh; không đồng nghĩa mọi điều biến bên trong SS2D đều bị loại bỏ.

## Chèn tại 2.3.2 Nhánh hình dạng đa tỉ lệ và có hướng

Depthwise convolution giới hạn việc lọc không gian trong từng kênh, sau đó convolution 1×1 trộn các đáp ứng giữa kênh. Kernel 3×3 và 5×5 tiếp cận những lân cận có độ rộng khác nhau; các kernel 1×5 và 5×1 tạo thiên hướng theo hai trục chính. Việc phối hợp này là một giả thuyết thiết kế về biểu diễn cấu trúc, không phải gán nhãn thủ công điểm nào thuộc biên. Tất cả các trọng số của nhánh vẫn được học qua mục tiêu phân đoạn và phát hiện chung.

Đại lượng căn bậc hai từ hai đáp ứng ngang, dọc cung cấp một tín hiệu kết hợp độ lớn. Hằng số 10⁻⁶ giúp phép căn có đối số dương khi hai đáp ứng gần 0. Tín hiệu này được đưa vào cùng các đáp ứng có dấu và nhánh cục bộ, vì chỉ giữ độ lớn có thể làm mất thông tin về hướng và dấu của các bộ lọc. Dù vậy, việc mạng học được cấu trúc hữu ích nào vẫn phải được khảo sát bằng đầu ra và ablation; không thể suy ra một đường bao hoàn chỉnh chỉ từ biểu thức của S_grad.

## Chèn tại 2.3.3 Guidance và hợp nhất

Guidance một chiều có nghĩa tensor hình dạng được dùng để tạo trọng số điều chỉnh nhánh trạng thái; mã không xây dựng một bước điều chỉnh ngược độc lập từ SS2D về ShapeAwareBranch trước hợp nhất. Tuy nhiên, trong lan truyền ngược, gradient của mục tiêu vẫn đi qua cả hai đường truyền và phép hợp nhất. Do đó, “một chiều” mô tả hướng tính toán của tín hiệu guidance trong forward, không phải nhánh shape được tách khỏi quá trình học của toàn mạng.

Hệ số γ được học và khởi tạo bằng 0,001 để bắt đầu với đóng góp residual có biên độ nhỏ. Mục đích thiết kế là hạn chế thay đổi đột ngột của đường residual khi đưa module mới vào mạng đã sử dụng trọng số pretrained. Đây là cơ chế khởi tạo, chưa phải bằng chứng bảo đảm hội tụ hoặc loại bỏ hoàn toàn gradient bất ổn. Việc kết hợp hai nhánh qua convolution và FFN vẫn có thể thay đổi phân bố đặc trưng, cần được xem cùng diễn biến loss và các kiểm tra tensor hữu hạn.

## Chèn tại 2.4.1 Chi phí của phép quét đang triển khai

Đặt module ở P3 với đầu vào 640×640 sẽ làm độ dài không gian tăng từ 400 lên 6.400 vị trí, tức gấp 16 lần P5, trước khi xét các thay đổi về kênh. Tại P4, độ dài là 1.600 vị trí, gấp 4 lần P5. Những tỷ lệ này giải thích động cơ chọn tầng sâu để giới hạn quy mô phép quét; chúng chưa xác định tỷ lệ tăng latency của cả mạng vì mỗi tầng còn khác về kênh, kernel và khả năng song song. Muốn khẳng định P5 là vị trí tốt nhất cần thí nghiệm vị trí có cùng quy trình đánh giá.

Các đại lượng Parameters, kích thước tệp checkpoint, FLOPs và latency đo những mặt khác nhau. Số tham số phản ánh lượng trọng số học được; kích thước checkpoint còn phụ thuộc kiểu số và thành phần được lưu; số phép toán là đại lượng ước lượng theo mô hình đếm; latency phụ thuộc cả triển khai và phần cứng. Đối với phép quét tùy biến, một công cụ đếm chỉ nhận diện convolution có thể bỏ qua phần trạng thái và cho ra tổng chưa đầy đủ. Kết quả benchmark cần nêu rõ những toán tử được đếm và những phần còn thiếu, đồng thời ưu tiên số đo thời gian thực tế cho cấu hình đang sử dụng.

## Chèn tại 2.4.2 Vì sao cần checkpoint FP32

FP16 và FP32 khác nhau không chỉ về số bit lưu trữ mà cả miền giá trị hữu hạn và độ chính xác biểu diễn. Khi một tensor hữu hạn ở float32 được ép sang float16, giá trị có thể vượt miền biểu diễn hoặc bị làm tròn mạnh. Việc chuyển lại sang float32 sau đó không phục hồi được thông tin đã mất. Do đó, nạp một checkpoint bị tràn ở thời điểm lưu rồi gọi .float() không tương đương lưu và giữ tensor hữu hạn bằng FP32 từ đầu.

Quy trình FP32 của đề tài cần được xem theo vòng đời: tính toán trong huấn luyện, sao chép EMA để lưu, loại bỏ thành phần không cần thiết của checkpoint, nạp ở dịch vụ và thực hiện predict. Chỉ đặt amp=False kiểm soát một phần của vòng đời này. Khi kiểm tra checkpoint, cần xác nhận tensor dấu phẩy động có kiểu phù hợp và không chứa NaN hoặc Inf. Việc thay giá trị không hữu hạn bằng số hữu hạn để cho mô hình tiếp tục chạy sẽ che đi lỗi số học; bản fork chọn phát hiện và từ chối trường hợp đó để giữ khả năng kiểm tra nguyên nhân.

## Chèn tại 2.5 Huấn luyện và khởi tạo trọng số

Cùng sử dụng nguồn pretrained giúp hai mô hình bắt đầu từ một chính sách khởi tạo có thể đối chiếu, nhưng không làm mọi trọng số giống nhau. Các lớp còn tương thích có thể nhận trọng số từ mô hình gốc; lớp C2TSVMamba thay thế C2PSA có cấu trúc tham số riêng. Vì vậy, mức khác biệt cuối cùng bao gồm cả cách biểu diễn và cách kiến trúc mới được tối ưu từ trạng thái khởi tạo đó. Một thí nghiệm bổ sung huấn luyện từ đầu hoặc khởi tạo theo chính sách khác có thể trả lời câu hỏi khác, nhưng không được trộn vào nhóm kết quả chính nếu điều kiện đã thay đổi.

Đầu phân đoạn và phát hiện được tối ưu chung, trong khi các thành phần loss đã lưu có vai trò giám sát những phần đầu ra khác nhau. Loss thấp hơn không luôn dẫn đến AP cao hơn vì AP còn phụ thuộc thứ hạng điểm tin cậy và quy tắc ghép ở nhiều ngưỡng IoU. Với reg_max bằng 1, nhánh loss hộp bao dùng chế độ tương ứng trong mã, nên không sao chép nguyên công thức DFL nhiều bin từ tài liệu của cấu hình khác. Khóa luận giữ cách diễn giải theo nhánh thực thi và dùng tên cột loss nguyên gốc khi trình bày các đường học.

## Chèn tại 4.1 Tổ chức cài đặt và môi trường

Các thành phần được tổ chức thành ba nhóm. Nhóm nghiên cứu chứa mã Ultralytics cơ bản, fork FP32 và cấu hình mô hình; nhóm thực nghiệm chứa notebook, dữ liệu đã chuyển đổi và các thư mục kết quả theo seed; nhóm ứng dụng chứa dịch vụ AI cùng client Web, Mobile. Cách phân tách này giúp tránh nhầm thư mục dùng để huấn luyện với thư mục cung cấp mô hình cho ứng dụng. Đặc biệt, ứng dụng phải nạp checkpoint đã xác định nguồn và đăng ký đúng mã lớp, chứ không chỉ trỏ đến một thư mục có tên tương tự mô hình đề xuất.

Để tái lập, trước hết cần xác định phiên bản thư viện và module được import thực sự. Python có thể ưu tiên một bản Ultralytics đã cài sẵn hoặc một đường dẫn editable thay vì fork vừa sao chép. Vì vậy, in đường dẫn ultralytics.__file__, kiểm tra sự hiện diện của C2TSVMamba và kiểm tra scale s là những bước có ý nghĩa trước huấn luyện. Cấu hình GPU trong notebook chỉ biểu thị thiết bị yêu cầu; tên GPU thực tế và tài nguyên cần lấy từ phiên đang chạy khi ghi nhận môi trường.

## Chèn tại 4.2.1 Notebook baseline

Quy trình notebook baseline gồm chuẩn bị môi trường, xác nhận cấu trúc ảnh và nhãn, tạo cấu hình dữ liệu, nạp checkpoint pretrained và gọi train với cấu hình thống nhất. Bước kiểm tra dữ liệu cần phân biệt một nhãn rỗng hợp lệ với một nhãn bị thiếu do lỗi chuyển đổi. Trước khi chạy, có thể mở một số ảnh kèm đa giác để xác nhận tọa độ chuẩn hóa và lớp polyp được đọc đúng. Việc chỉ kiểm tra đủ số ảnh mà không kiểm tra nhãn có thể bỏ sót sai lệch đầu vào ảnh hưởng toàn bộ phép so sánh.

Mỗi lượt phải có tên duy nhất gắn với seed để tránh ghi đè và phải giữ args.yaml cùng results.csv. Khi notebook kết thúc hoặc môi trường bị ngắt, chỉ những tệp đã lưu mới là căn cứ xác định mức hoàn thành. Trong bộ số liệu đang dùng, 40 results.csv đều có 100 dòng epoch; đây là bằng chứng lịch sử đã ghi nhận đủ số epoch, khác với việc suy đoán từ một biến EPOCHS trong notebook. Sau khi tải về máy, cần kiểm tra tệp kết quả và trọng số còn tương ứng cùng lượt trước khi tổng hợp.

## Chèn tại 4.2.2 Notebook mô hình đề xuất và yêu cầu FP32

Với mô hình tùy biến, trình tự cài đặt còn gồm đăng ký lớp trong module và parser, tạo YAML có scale s, rồi xây dựng mô hình trước khi nạp các trọng số có thể dùng lại. Kiểm tra tensor đầu vào giả có kích thước đã quy định giúp phát hiện sớm lỗi concatenate hoặc số kênh. Tuy nhiên, một forward pass thành công chưa thay thế kiểm tra loss, backward và checkpoint sau lưu. Đối với bản FP32, cần xác nhận cả đường lưu cuối cùng vì lỗi ép half có thể xuất hiện sau một lượt train vẫn hoạt động bình thường.

Việc đóng gói kết quả cần giữ mối liên hệ giữa mã nguồn, cấu hình và trọng số. Một bộ tối thiểu gồm phiên bản hoặc bản chụp mã, YAML thực dùng, data.yaml, args.yaml, results.csv, weights và thông tin seed. Những biểu đồ được sinh từ các tệp này là kết quả dẫn xuất, có thể tái tạo khi thuật toán tổng hợp được lưu. Nếu chỉ giữ ảnh biểu đồ mà thiếu số liệu, việc tính lại chênh lệch hoặc đổi quy tắc chọn epoch sẽ khó kiểm tra. Đây là cơ sở cho cách tổ chức bộ kết quả mở rộng ở Chương 5.

## Chèn tại 4.3 Tổng quan ứng dụng PolypVision

Việc tách dịch vụ suy luận khỏi giao diện giúp hai client dùng chung một nguồn mô hình và quy tắc tiền xử lý. Phía giao diện tiếp nhận thao tác người dùng và trình bày kết quả; phía AI chịu trách nhiệm kiểm tra ảnh, lựa chọn runtime, suy luận và tạo dữ liệu phản hồi. Với Web, tầng Spring Boot bổ sung quản lý người dùng và lịch sử; với Mobile Direct AI, yêu cầu được gửi thẳng đến FastAPI. Do đó, một lỗi kết nối dịch vụ có thể ảnh hưởng cả hai client, trong khi lỗi lưu lịch sử trên Web không đồng nghĩa mô hình AI không thể chạy trên Mobile.

Luồng sử dụng chính bắt đầu bằng chọn ảnh và mô hình. Người dùng có thể xem ảnh gốc cùng overlay, số đối tượng, độ tin cậy và thời gian phản hồi được cung cấp. Trong chế độ so sánh, cùng ảnh được gửi đến hai mô hình và hai kết quả được đặt cạnh nhau để quan sát. Thiết kế này phục vụ giải thích sự khác nhau trên một trường hợp; nó không tự tạo nhãn chuẩn và không thay thế bộ đánh giá định lượng. Vì vậy, giao diện cần giữ thông tin tên mô hình và ảnh gốc để người đọc truy nguyên kết quả đang xem.

## Chèn tại 4.4.1 Nạp và định danh mô hình

Checkpoint tùy biến lưu tham chiếu tới các lớp Python đã tạo nên kiến trúc. Nếu tên module hoặc tên lớp không có trong môi trường dịch vụ, lỗi có thể xảy ra ngay khi giải tuần tự, trước bước predict. Vì vậy, bản sao mã TSVM dùng trong ứng dụng phải tương thích với checkpoint và được đăng ký trước khi gọi YOLO để nạp. Kiểm tra số lượng lớp và task sau tải giúp phát hiện trường hợp nạp nhầm một mô hình detection hoặc checkpoint nhiều lớp vào luồng segmentation một lớp.

Manifest đóng vai trò nhận dạng hiện vật thực nghiệm. Khi đổi checkpoint, cần cập nhật đường dẫn nguồn và mã băm, không chỉ đổi nhãn hiển thị. Seed, quy tắc chọn checkpoint và kiểu số cũng cần được giữ cùng thông tin này. Nhờ đó, ảnh minh họa của ứng dụng có thể được đối chiếu lại với đúng tệp trọng số; những kết quả cũ vẫn được nhận biết là của phiên bản trước và không bị gán sang mô hình FP32 bằng thao tác đổi tên.

## Chèn tại 4.4.2 Tiếp nhận ảnh và suy luận

Giới hạn đầu vào có hai lớp: dung lượng tệp hạn chế lượng dữ liệu nhận, còn số pixel hạn chế ảnh giải mã có kích thước quá lớn. Tên đuôi tệp và MIME chỉ là thông tin ban đầu; khả năng giải mã nội dung mới xác nhận dữ liệu có thể được xử lý như ảnh. Sau khi mở ảnh, hệ thống xử lý hướng hiển thị và chuẩn hóa về RGB trước khi chuyển đến mô hình. Các thao tác này giúp ảnh người dùng nhìn thấy và ảnh mô hình nhận vào có cùng cách diễn giải về hướng và màu.

Overlay được tạo từ ảnh đầu vào và kết quả dự đoán để hỗ trợ quan sát. Mã hóa Base64 giúp truyền ảnh này trong phản hồi JSON nhưng làm tăng lượng dữ liệu so với tệp nhị phân tương ứng, nên không nên coi thời gian predict là toàn bộ thời gian phản hồi. Một quy trình đo ứng dụng hoàn chỉnh cần xác định rõ điểm bắt đầu, điểm kết thúc và các bước bao gồm trong phép đo. Phần benchmark mô hình vì vậy được trình bày tách với các kiểm tra chức năng giao thức.

## Chèn tại 4.4.3 Điều phối yêu cầu và xử lý lỗi

Khóa runtime bảo vệ một mô hình khi nhiều yêu cầu cùng truy cập, còn semaphore giới hạn số tác vụ được phép thực hiện theo cấu hình dịch vụ. Những cơ chế này nhằm kiểm soát tài nguyên và hành vi khi tải tăng, không phải bằng chứng rằng hệ thống đã được kiểm thử tải lớn. Một yêu cầu vượt thời gian chờ cần có thông báo phù hợp để client không nhầm thành kết quả “không có polyp”. Tương tự, kết quả rỗng hợp lệ phải được phân biệt với lỗi nạp mô hình, lỗi giải mã hoặc lỗi xử lý.

requestId cung cấp một định danh chung để ghép phản hồi với yêu cầu đang hiển thị. Điều này có ý nghĩa khi người dùng đổi ảnh hoặc gửi lại thao tác trong lúc yêu cầu trước chưa hoàn tất. Thông tin lỗi cần đủ để xác định bước hỏng trong luồng phần mềm nhưng không đưa nội dung nhạy cảm hoặc đường dẫn nội bộ không cần thiết vào thông báo công khai. Ở phía báo cáo, chỉ mô tả các nhóm lỗi và hợp đồng đã triển khai; không coi một vài kiểm tra đơn vị là kiểm chứng an toàn vận hành trong mọi điều kiện.

## Chèn tại 4.5.1 Ứng dụng Web

Luồng phân tích đơn và luồng so sánh cần được quản lý khác nhau ở tầng lịch sử. Một kết quả phân tích đơn gắn với một mô hình, còn một nhóm so sánh phải giữ được hai kết quả của cùng ảnh. Khi xem lại, tên mô hình, thời điểm và thông tin dự đoán cho phép nhận biết đúng nguồn kết quả. Quyền sở hữu được kiểm tra ở phía dịch vụ để việc biết một định danh bản ghi chưa đủ cho phép người dùng khác truy xuất hoặc xóa dữ liệu tương ứng.

Giao diện kết quả cần trình bày mặt nạ như thông tin tham khảo cùng ảnh gốc và độ tin cậy, tránh chuyển điểm confidence thành tỷ lệ xác suất mắc bệnh. Với ảnh không có phát hiện, nội dung phù hợp là mô hình không trả về đối tượng tại ngưỡng đang dùng. Cách diễn đạt này phản ánh đúng đầu ra kỹ thuật và không biến dự đoán rỗng thành kết luận ảnh hoàn toàn bình thường. Các màn hình trong ứng dụng là nơi thể hiện hành vi mô hình để trình diễn đề tài, trong khi nhận định y khoa nằm ngoài chức năng đã kiểm chứng.

## Chèn tại 4.5.2 Ứng dụng Mobile Direct AI

Khác biệt quan trọng của Mobile là địa chỉ localhost được hiểu theo chính thiết bị chạy ứng dụng. Khi thử trên điện thoại, dịch vụ AI phải có địa chỉ mạng có thể truy cập và cấu hình cổng phù hợp; khi thử trên môi trường giả lập, cách truy cập máy chủ cũng phụ thuộc môi trường. Vì vậy, cấu hình AI_BASE_URL được tách khỏi logic phân tích để tránh phải sửa mã chức năng cho mỗi thiết bị. Kiểm tra kết nối và trạng thái mô hình trước khi gửi ảnh giúp phân biệt lỗi mạng với lỗi suy luận.

Ảnh chọn từ bộ nhớ hoặc camera cần được đưa vào cùng quy trình kiểm tra của API. Nguồn ảnh camera có thể tạo góc nhìn và chất lượng khác với dữ liệu nội soi dùng trong thực nghiệm; chức năng chọn ảnh không đồng nghĩa mọi ảnh chụp bất kỳ đều thuộc miền dữ liệu phù hợp. Trong phạm vi trình diễn, Mobile đóng vai trò client gửi ảnh nội soi đã có, nhận overlay và so sánh hai mô hình. Không suy ra khả năng chẩn đoán từ việc giao diện có nút mở camera.

## Chèn tại 4.6 Kiểm tra tích hợp với checkpoint thực nghiệm

Các kiểm tra được phân thành hai nhóm để tránh nhầm phạm vi chứng minh. Kiểm thử phần mềm dùng đầu vào và đối tượng giả lập khi cần để xác nhận định dạng phản hồi, xử lý lỗi, chọn mô hình và tương tác giữa các lớp. Kiểm tra với checkpoint thật xác nhận mô hình được giải tuần tự, lớp tùy biến đã đăng ký, tensor hữu hạn và lệnh predict tạo đầu ra. Cả hai nhóm đều cần cho triển khai, nhưng nhóm thứ nhất không đo độ chính xác phân đoạn, còn nhóm thứ hai với số ảnh ít cũng chưa tạo thành một đánh giá hiệu năng mới.

Hai ví dụ seed 0 trong Hình 4.2 là kiểm tra tính khả dụng của luồng suy luận. Để đánh giá chất lượng checkpoint seed 0 một cách độc lập với biểu đồ huấn luyện, cần chạy lại toàn bộ tập đánh giá với quy tắc cố định và lưu dự đoán, thời gian, cấu hình. Muốn đánh giá ưu thế kiến trúc còn phải xét nhiều seed và bất định như Chương 5. Việc tách các mức kiểm tra giúp báo cáo ghi nhận đúng phần mềm đã chạy mà không gán ý nghĩa vượt quá dữ liệu quan sát.

## Chèn tại 4.7 Vận hành và giới hạn ứng dụng

Khi thay mô hình, trình tự kiểm tra gồm xác nhận manifest, nạp dịch vụ AI, kiểm tra trạng thái sẵn sàng và danh sách mô hình, rồi thử một ảnh trước khi sử dụng các client. Web cần kiểm tra thêm kết nối cơ sở dữ liệu và đường dẫn lưu ảnh; Mobile cần kiểm tra địa chỉ máy chủ từ thiết bị. Sau thay đổi mã hoặc tệp cấu hình, tiến trình đang chạy có thể vẫn giữ runtime cũ trong bộ nhớ, nên cần khởi động lại dịch vụ để xác nhận phiên bản đang phục vụ.

Các giới hạn về dữ liệu và đánh giá của mô hình cũng đi theo ứng dụng. Phần mềm không làm tăng bằng chứng về tổng quát hóa chỉ bằng việc đặt một giao diện quanh checkpoint. Nếu triển khai cho nguồn ảnh khác, cần đánh giá lại miền dữ liệu, cách kiểm soát đầu vào, sai số và yêu cầu bảo vệ thông tin. Trong khóa luận, ứng dụng thể hiện khả năng kết nối một kết quả nghiên cứu với quy trình sử dụng có thể quan sát; những bước đánh giá vận hành dài hạn được xác định là công việc tiếp theo.
