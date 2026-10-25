# Đối chiếu bản cũ và phương án mở rộng

## Phạm vi đã đọc

- Bản cũ: 756 đoạn, 15 bảng, 3 inline shape, 110.667 ký tự trong đoạn văn.
- Bản hiện tại: 589 đoạn, 17 bảng, 17 inline shape, 84.097 ký tự trong đoạn văn.
- Các số ký tự không bao gồm văn bản ô bảng. Số shape không đồng nghĩa số hình kết quả thực nghiệm vì gồm logo.
- Bản cũ dùng Normal cho phần lớn đề mục và chứa nhiều khung hình chờ chèn. Vì vậy, không đánh giá độ hoàn chỉnh chỉ bằng số đoạn hoặc số trang.

## Nội dung bản cũ nên khai thác

1. Mở đầu: đi từ bối cảnh, lý do kỹ thuật, mục tiêu tổng quát đến nhiệm vụ cụ thể, đối tượng, phạm vi và ý nghĩa. Bản hiện tại đúng nhưng rút gọn quá mạnh, làm mất đường dẫn lập luận và cách kiểm tra mức hoàn thành.
2. Chương 1: giải thích các dạng bài toán, vai trò mặt nạ, giới hạn đặc trưng cục bộ và ngữ cảnh; cần viết liền mạch hơn thay vì chỉ định nghĩa ngắn.
3. Chương 2: diễn giải backbone/neck/head, prototype và hệ số mặt nạ, kích thước tensor và phân tích vị trí tích hợp. Bản mới có các điểm chính xác quan trọng cần giữ nguyên, nhưng cần giải thích thêm quan hệ giữa các bước.
4. Chương 4: phân tích notebook theo trình tự, từ dữ liệu đến kết quả; mô tả luồng người dùng và giao thức, không chỉ liệt kê công nghệ. Bản mới có mô tả phần mềm đúng và kiểm tra thật tốt hơn bản cũ; cần thêm bối cảnh vận hành cho các chi tiết đó.
5. Chương 5: khai thác hình theo từng câu hỏi thay vì chèn hình để minh họa chung. Root đang xử lý phần này từ nguồn FP32 mới.

## Nội dung cũ không được khôi phục nguyên văn

- Các tỷ lệ bệnh học/giảm tử vong/bỏ sót không có nguồn gắn với câu và phạm vi; mô tả can thiệp y khoa quá cụ thể so với nhiệm vụ tin học.
- Các câu trên60FPS hoặc50FPS không có điều kiện đo và không phải benchmark FP32 hiện tại.
- Khẳng định VMamba quét bốn đường chéo; mã thực hiện row/column forward/reverse.
- Khẳng định mã quét tùy biến có tổng công việc O(L); mã prefix hiện tại có tổng công việc O(LlogL).
- Giải thích Δ tự động nhỏ ở nhiễu/lớn ở biên như kết quả đã đo.
- “Không có công trình nào”, “lần đầu tiên”, “bảo đảm topology”, “triệt tiêu FP”, “độ chính xác lâm sàng”, “sẵn sàng chuyển giao” khi chưa có bằng chứng tương ứng.
- Công thức DFL nhiều bin áp vào YOLO26 reg_max1; mã BboxLoss hiện tại có nhánh khác khi reg_max không lớn hơn1.
- Diễn giải 200/1200≈20%; đúng là16,67% của toàn bộ dữ liệu, BG20 là tỷ lệ bổ sung200 trên1.000 ảnh polyp.
- Dice/IoU suy ra từ objectPrecision/Recall; các đại lượng không chung đơn vị đánh giá.
- TN=40−FP từ ma trận đối tượng; không có ánh xạ hợp lệ sang số ảnh âm.
- Khẳng định chạy CVC-ClinicDB, CVC-ColonDB, ETIS khi chưa có log dự đoán.
- Kế hoạch/phân công cá nhân12tuần, chứng nhận CLO, số phép audit hoặc điểm đánh giá không có bằng chứng.
- Khung “[KHUNG HÌNH ẢNH]”, chỉ dẫn chèn trườngTOC và đoạn phân tích placeholder cần loại bỏ hoàn toàn.

## Gói nội dung sẵn tích hợp

`expanded_intro_ch1_ch2_ch4.md` là phiên bản thay thế toàn bộ phần trước Chương5 của report_content.md hiện tại. Giữ nguyên các directive, bảng, hình, tham chiếu và nội dung đã đúng; thêm30khối theo các anchor tương ứng. `expanded_sections.md` lưu riêng phần bổ sung để kiểm tra và điều chỉnh. `expanded_report_content.md` kèm cả Chương5 cũ cho đối chiếu nhưng không nên dùng nguyên Chương5 đó sau khi root hoàn thành bộ kết quả mới.

Không sửa DOCX hoặc nguồn ứng dụng trong phân công này. Chưa thực hiện render; root tích hợp rồi QA toàn bộ tài liệu cuối.
