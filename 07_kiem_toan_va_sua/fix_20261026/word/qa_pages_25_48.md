# QA trực quan Word — trang PDF 25–48

Ngày kiểm tra: 2026-10-26. Người kiểm tra: sub-agent fix_web_display.

Nguồn: `fix_20261026/word/rendered_verified/page-N.png`, kích thước gốc 1414 × 2000. Đã mở riêng **tất cả 24 trang** bằng `view_image` với `detail: original`; không chỉ xem contact sheet. Đã đọc hướng dẫn documents/SKILL.md và verify_render.md. Không sửa Word, ứng dụng hoặc dữ liệu; không render lại.

Kết quả: không phát hiện chữ bị cắt, ký tự lỗi, bảng/hình chồng chữ hoặc vượt lề trong phạm vi 25–48. Các trang nhiều chữ vẫn có khoảng cách tới số trang; kiểm tra bổ sung crop chân trang 35 xác nhận đoạn cuối và footer tách biệt. Khoảng trắng cuối trang 34 và 47 gắn với chuyển phần/đặt hình trang kế tiếp, không phải mất nội dung.

| Trang PDF | Số trang in | Nội dung đã xem và nhận xét |
|---|---:|---|
| 25 | 12 | Kết chương 1; chữ, dấu và footer rõ. |
| 26 | 13 | Mở chương 2, Hình 2.1 và Bảng 2.1; **Backbone P4 = 256** hiển thị rõ. Bảng nối trang kế tiếp không cắt hàng. |
| 27 | 14 | Bảng 2.1 tiếp tục, lặp tiêu đề; P4 head 256, P5 head 512 rõ; công thức và mục tiếp theo không chồng lấn. |
| 28 | 15 | Công thức wrapper và mô tả SS2D rõ, không lỗi glyph. |
| 29 | 16 | Các nhánh/kích thước đặc trưng và công thức rõ; đoạn nối trang sau tự nhiên. |
| 30 | 17 | Công thức 1+G, Hình 2.2, chú thích và văn bản không chồng nhau. |
| 31 | 18 | Phần độ phức tạp; chữ dày nhưng không bị cắt. |
| 32 | 19 | FP32 và thiết lập huấn luyện; bố cục rõ. |
| 33 | 20 | Ablation và Bảng 2.2; đường viền, hàng và chữ rõ. |
| 34 | 21 | Kết chương 2; khoảng trắng cuối trang chấp nhận được trước chương 3. |
| 35 | 22 | Mở chương 3; kiểm tra thêm crop chân trang xác nhận dòng cuối không sát/chồng footer. |
| 36 | 23 | Nguồn normal-cecum và Hình 3.1; ảnh, chú thích, nguồn đọc được. |
| 37 | 24 | Phân chia BG20 và Bảng 3.1 rõ. Đoạn 880/120 nêu hai danh sách cố định và **nguồn phát hành riêng chưa được xác minh**; không còn khẳng định provenance chưa có bằng chứng. |
| 38 | 25 | Otsu, các công thức 3.1–3.3 và mục Closing rõ, không cắt chỉ số. |
| 39 | 26 | Contour và Douglas–Peucker, công thức epsilon; dấu/ký hiệu rõ, đoạn nối trang sau bình thường. |
| 40 | 27 | Chuẩn hóa tọa độ, Hình 3.2 gồm bốn ảnh; nhãn con, chú thích và nguồn đầy đủ. |
| 41 | 28 | Đổi kích thước và LetterBox; công thức 3.6–3.8 đọc được, không chồng số công thức. |
| 42 | 29 | Hình 3.3 hai ảnh trước/sau và đoạn mô tả; tăng cường dữ liệu nối trang sau, không cắt chữ. |
| 43 | 30 | Mosaic, affine, công thức 3.9 và mở HSV; không lỗi hiển thị. |
| 44 | 31 | HSV, lật ngang, công thức 3.10–3.12; Bảng 3.2 bắt đầu và sang trang kế tiếp sạch. |
| 45 | 32 | Bảng 3.2 tiếp tục với tiêu đề lặp; Hình 3.4 sáu ảnh, chú thích/nguồn rõ. |
| 46 | 33 | Chuẩn hóa đầu vào và mở kiểm tra toàn vẹn; công thức 3.13 rõ, không chồng lấn. |
| 47 | 34 | Toàn vẹn dữ liệu: nêu rõ **999 tệp nhãn khớp từng ký tự**, một tệp lệch một đỉnh 3 pixel trên mỗi trục, **chưa xác định nguyên nhân**; giữ nhãn hiện hành. Nêu giới hạn bệnh nhân/gần trùng/tập kiểm thử. Không lỗi bố cục. |
| 48 | 35 | Sơ đồ Hình 3.5, chú thích, nguồn và diễn giải rõ; đoạn cuối tới FP32 không bị cắt/chồng footer. |

## Giới hạn

Đây là QA trực quan của bản render trong phạm vi trang được giao, không thay thế kiểm chứng khoa học lại toàn bộ các phát biểu. Các điểm nội dung được xác nhận ở đây là những gì thực sự hiển thị trên trang. Không phát sinh lỗi cần sửa từ lượt QA này.
