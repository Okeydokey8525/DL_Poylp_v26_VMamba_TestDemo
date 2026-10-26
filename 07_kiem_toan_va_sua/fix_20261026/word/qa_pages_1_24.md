# Kiểm tra trực quan các trang 1 đến 24

Đã mở riêng từng PNG `rendered_verified/page-N.png` bằng `view_image` với `detail="original"`. Không dùng contact sheet để thay cho việc xem từng trang. Không sửa nguồn hoặc render lại trong lượt QA này.

**Trang thực sự đã xem:** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24.

| Trang | Kết quả quan sát |
|---|---|
| 1 | Bìa, logo, tên đề tài, sinh viên và giảng viên hiển thị rõ; không chồng chữ hoặc cắt mất dòng. |
| 2 | Trắng hoàn toàn. Chưa đối chiếu bản trước nên không xác nhận đây là lỗi mới; cần tổng kiểm xác định có phải mặt sau bìa hoặc section break được giữ nguyên. |
| 3–4 | Lời cảm ơn và cam đoan rõ, không lỗi font; footer số La Mã tách khỏi nội dung. |
| 5–6 | Trang nhận xét có các dòng chấm và vùng trống dành cho giảng viên; đây là form có chủ đích, không phải mất nội dung do render. |
| 7–8 | Tóm tắt Việt/Anh đọc được; dấu tiếng Việt, ký hiệu ±, khoảng tin cậy và số liệu không bị cắt/chồng. |
| 9–10 | Mục lục hai trang; dòng dẫn và số trang đều nhìn thấy, không vượt mép. Các mục dài xuống dòng vẫn đọc được. |
| 11 | Danh mục hình: các mục dài xuống dòng; mục cuối vẫn nằm phía trên footer và không bị cắt. |
| 12 | Danh mục bảng: các dòng và số trang đầy đủ, không tràn lề. |
| 13 | Bảng chữ viết tắt nằm trọn trang; tất cả hàng, đường viền và chữ đều đọc được. |
| 14–17 | Nội dung mở đầu, heading và đoạn văn không chồng/cắt; các dòng cuối trang vẫn cách footer rõ. |
| 18 | Trang ngắn cho phần bố cục; trang 19 bắt đầu chương mới. Vùng trắng lớn là hệ quả của ngắt sang chương mới, không thấy nội dung tràn mất. |
| 19–21 | Chương 1 và các tiểu mục hiển thị bình thường; heading cuối trang 19 có nội dung đi kèm, không đứng đơn độc. |
| 22 | Công thức trạng thái có chỉ số dưới và ký hiệu toán hiển thị đọc được; không có ô vuông thay glyph hoặc clipping. |
| 23 | Các đoạn về SS2D và nghiên cứu liên quan rõ; đoạn tiếp sang trang 24 bình thường. |
| 24 | Bảng 1.1 đủ tiêu đề, header và năm hàng trong cùng trang; không tách hàng xấu. Heading 1.4.3 có đoạn văn đi kèm. |

## Kết luận phạm vi

Không phát hiện lỗi bố cục cần sửa trong phần nội dung đã xem từ trang 1–24. Quan sát duy nhất cần tổng kiểm phân loại là **trang 2 trắng**; chưa có căn cứ quy thành lỗi do lần chỉnh sửa này. Lượt này chỉ kiểm hình thức hiển thị, không tái xác minh nội dung khoa học hay mọi số trang trong trường mục lục.
