# Hợp đồng hoàn thiện báo cáo

Tham chiếu trình bày: Bao_cao/Bieu mau do an_khoa luan. K.CNTT_HUIT_2025_V3.docx và báo cáo hiện tại. Giữ bìa, tác giả, người hướng dẫn, logo và tên đề tài gốc. Toàn bộ nội dung nghiên cứu và phụ lục là vùng được phép sửa theo yêu cầu hoàn thiện báo cáo.

A4 dọc 21 × 29,7 cm; lề trái 3,5 cm, phải/trên/dưới 2,5 cm. Times New Roman 13 pt, dòng 1,3; đoạn căn đều, đầu dòng 0,8 cm, trước/sau 6 pt. Chương 18 pt đậm, giữa, viết hoa; mục cấp hai 14 pt đậm; cấp ba 13 pt đậm. Bảng 12 pt, dòng 1,3, tiêu đề trên bảng, dòng đầu lặp. Hình có tiêu đề bên dưới, đánh số theo chương. Số trang bìa ẩn; phần đầu La Mã; nội dung Ả Rập từ 1. Mục lục và danh mục có liên kết nội bộ và trường cập nhật số trang.

Giữ nội dung và 5 hình cùng công thức của tài liệu Tien_Xu_Ly_Du_Lieu.docx, điều chỉnh các khẳng định vượt phạm vi kiểm chứng. Bỏ phần tài liệu tham khảo riêng chương và hòa vào danh mục chung [1]–[11]. Giữ các quan hệ ảnh khi nhập chương.

Kế hoạch thực hiện: (1) Kiểm kê bản thảo và nguồn gốc; (2) đối chiếu 40 results.csv, args.yaml và dữ liệu; (3) xác minh tài liệu quốc tế; (4) chuyển ứng dụng sang hai checkpoint S/TSVM FP32 và kiểm thử; (5) biên soạn 5 chương và phụ lục, đưa bảng/đồ thị vào đúng vị trí; (6) render toàn văn, kiểm tra mọi trang, đối chiếu số liệu và kiểm tra không còn hình giữ chỗ hoặc mật khẩu; (7) lưu bản hoàn thiện vào đúng tệp yêu cầu, giữ bản gốc dự phòng.

Không gộp kết quả TSVM cũ không có FP32; không tạo Dice hoặc specificity từ AP/ma trận đối tượng; không gán benchmark checkpoint cũ cho FP32. Các nghiên cứu công bố được dẫn nguồn riêng và không xếp hạng với chỉ số khác định nghĩa. Mốc max-mask và best.pt theo box+mask fitness được phân biệt.

Các phần cần viết mới: tổng quan và nghiên cứu liên quan, kiến trúc TSVM đúng mã, FP32 checkpoint, ứng dụng đã đổi mô hình, phương pháp so sánh và 20 seed, giới hạn, kết luận, tài liệu tham khảo, phụ lục nguồn số liệu và hướng dẫn vận hành. Không viết điểm số, nhận xét hoặc chữ ký thay giảng viên.
