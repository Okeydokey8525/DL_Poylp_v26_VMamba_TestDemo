# Kiểm tra trình duyệt sau sửa

Mở ứng dụng local 127.0.0.1:18080, DB riêng polypweb_fix_20261026, đăng nhập bằng tài khoản fixture @example.invalid.

1. Trang chủ hiện YOLO26s-seg và YOLO26s-TSVM-FP32-seg, hai mô hình hỗ trợ, so sánh hai mô hình.
2. Trang /comparisons mở bình thường, tổng 1 group, hiện đúng Baseline 88,3% và VMamba 58,4%; không còn trang lỗi 503.
3. Trang /history hiện đúng hai kết quả thuộc tài khoản thử.
4. Mở kết quả TSVM: tiêu đề đúng khóa YOLO26s-TSVM-FP32-seg, badge VMAMBA, 2 mask, kích thước 621 × 530 px, trạng thái đã lưu MongoDB.

Lưu screenshot comparison_history.png và tsvm_result.png. Ảnh chụp viewport nên metadata ở phần dưới được xác nhận bằng cây truy cập giao diện, không khẳng định screenshot đầu trang chứa đủ metadata. Không chạy lại inference trong lượt duyệt này; dùng kết quả thật đã tạo bởi 39 phép kiểm HTTP trước đó.
