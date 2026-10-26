# Kiểm tra benchmark

- 400 dòng timing thật; 4 nhóm ×100, không NaN/vô hạn/độ trễ âm.
- SHA-256 checkpoint khớp metadata.
- Danh sách ảnh/hash và giao thức của hai mô hình trùng nhau.
- Có kết quả hộp/mặt nạ hữu hạn từ pipeline thật.
- Không tái dùng timing hoặc GFLOPs từ bộ 10 seed.
- Đếm detection không dùng để suy ra AP/độ chính xác trên tập dữ liệu.
- raw/*_environment.json có phiên bản, CPU, precision và RSS.
