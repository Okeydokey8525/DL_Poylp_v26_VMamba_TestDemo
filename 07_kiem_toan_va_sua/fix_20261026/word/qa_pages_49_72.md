# QA trực quan bản Word trang PDF 49–72

Ngày 26/10/2026. Nguồn kiểm tra: `rendered_verified/page-N.png`, kích thước gốc 1414 × 2000. Đã mở riêng **tất cả 24 trang 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72** bằng `view_image` với `detail: original`; không dùng contact sheet thay thế. Chỉ đọc, không sửa nguồn hoặc render lại.

| Trang PDF | Số trang in | Quan sát |
|---|---:|---|
| 49 | 36 | Mở chương 4, Bảng 4.1 đủ các hàng; văn bản và footer không chồng/cắt. |
| 50 | 37 | Nội dung môi trường và notebook baseline; heading và các đoạn rõ, tiếp trang tự nhiên. |
| 51 | 38 | Notebook FP32, quy tắc checkpoint và mở phần ứng dụng; không thấy glyph lỗi hoặc chữ vượt lề. |
| 52 | 39 | Hình kiến trúc 4.1, mũi tên, các ô và caption đều rõ; phần văn bản phía dưới không chồng hình. |
| 53 | 40 | Registry, định danh model và mở luồng suy luận; tên module dài xuống dòng vẫn nằm trong lề. |
| 54 | 41 | Bảng endpoint 4.2 nguyên hàng, chữ và viền rõ; các đoạn phía dưới không cắt. |
| 55 | 42 | Điều phối, xử lý lỗi và chức năng Web; heading đi kèm nội dung, footer tách biệt. |
| 56 | 43 | Nội dung Web và Mobile Direct AI; dấu tiếng Việt và đường dẫn biến môi trường đọc được. |
| 57 | 44 | **Bảng 4.3 hiển thị FastAPI 51, Spring Boot 274, Flutter 498 đạt (log cũ)**. Đoạn ngay dưới ghi ngày 26/10/2026, 4 test MongoDB thật, Flutter chưa chạy lại. Các hàng bảng không bị cắt; đoạn ví dụ ghi Baseline một và TSVM hai mặt nạ, không suy đúng/sai khi thiếu ghép nhãn chuẩn. |
| 58 | 45 | Hình 4.2 bốn ảnh và caption đầy đủ; các đoạn giải thích ở dưới không chồng hình, không tràn footer. |
| 59 | 46 | Vận hành, giới hạn và tóm tắt chương; ngắt đoạn và heading rõ. |
| 60 | 47 | Mở chương 5; tiêu đề hai dòng và nội dung dày nhưng không clipping/chồng footer. |
| 61 | 48 | Nguồn số liệu và quy tắc max-mask so với best.pt; heading và thân bài rõ. |
| 62 | 49 | Các độ đo và công thức thống kê; chỉ số dưới, căn và ký hiệu toán đọc được. Đối chiếu text PDF xác nhận heading đầy đủ 5.2.2. |
| 63 | 50 | Bảng 5.1 đầy đủ chín hàng, chữ/số/SD rõ; diễn giải chênh lệch không bị cắt. |
| 64 | 51 | Biểu đồ 5.1 rõ trục, chú giải, giá trị và error bar; caption và đoạn văn tách biệt. |
| 65 | 52 | Biểu đồ 5.2 và đoạn diễn giải; không thấy cắt nhãn hoặc chồng chữ. |
| 66 | 53 | Biểu đồ Precision/Recall 5.3, chú giải và giá trị rõ; text PDF xác nhận heading đầy đủ 5.3.3. |
| 67 | 54 | Biểu đồ hộp bao 5.4 và hai đoạn giải thích; trục và nhãn rõ, không vượt lề. |
| 68 | 55 | Hình ghép cặp 5.5 và Bảng 5.2; các cột p-value, khoảng tin cậy hiển thị đầy đủ. |
| 69 | 56 | Biểu đồ khoảng tin cậy 5.6 và nội dung p=0,0614; không cắt trục/nhãn hoặc mất chữ ở lề. |
| 70 | 57 | Hình 5.7 và phần đầu Bảng 5.3 seed 0–12; mỗi hàng trọn vẹn, footer tách khỏi bảng. |
| 71 | 58 | Bảng 5.3 tiếp seed 13–19 có lặp header, nội dung và Hình 5.8 rõ; caption/nguồn còn trên footer. |
| 72 | 59 | Biểu đồ hộp 5.9, Bảng 5.4 và diễn giải; không chồng hoặc cắt chữ, bảng giữ đủ hàng. |

Kết luận trong phạm vi đã xem: **không phát hiện lỗi bố cục cần sửa**. Khoảng trắng cuối trang có liên quan đến bố trí hình và chuyển phần, không có dấu hiệu mất nội dung. Đây là QA hình thức hiển thị, không thay thế kiểm chứng lại toàn bộ số liệu khoa học.
