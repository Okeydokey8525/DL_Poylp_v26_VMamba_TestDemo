---
name: van-phong-bao-cao-nhom
description: Dùng khi viết mới hoặc sửa nội dung bản Word khóa luận CNTT-KLCN182 (bản nộp GVHD) để giữ đúng văn phong và định dạng của nhóm, và khi sửa theo nhận xét của thầy.
---

# Văn phong và cách sửa báo cáo của nhóm

Học từ bản đã nộp `06_bao_cao/BaoCaoKhoaLuan_CNTT_KLCN182.docx`. Bản này phần lớn do nhóm tự viết, máy dò AI cho tỷ lệ thấp. Mục tiêu khi sửa: **giữ giọng của nhóm, chỉ làm câu gọn và đúng hơn**. Không viết lại kiểu văn máy.

## 1. Giữ những gì nhóm đang làm tốt

- **Xưng hô:** "nhóm" và "đề tài". Không dùng "chúng em", "chúng tôi", "ta".
- **Giải thích bằng hình ảnh dễ hiểu trước, công thức sau.** Ví dụ: "Có thể hình dung mỗi bộ lọc như một mẫu nhỏ mà mạng đi tìm trong ảnh".
- **Lý thuyết luôn gắn về đề tài:** lưới 20×20, chuỗi 400 phần tử, 880/120 ảnh, tầng 10.
- **Bố cục mỗi mô hình:** ý tưởng → các bước ("Bước 1… Bước 5") → ưu và nhược điểm. Mỗi chương có "Kết chương".
- **Trung thực về giới hạn:** nói thẳng chỗ chưa làm hoặc chưa chứng minh được.
- **Từ nối dùng ít:** cả bài chỉ khoảng 5 lần "Tuy nhiên / Ngoài ra / Bên cạnh đó". Không dùng gạch ngang dài (—), rất ít dấu chấm phẩy.

## 2. Sửa những lỗi nhóm hay mắc (thầy đã chỉ ra)

- **Câu quá dài:** trung bình 33 từ, có câu hơn 100 từ. Tách để mỗi câu một ý, khoảng 15–30 từ.
- **Thiếu dấu phẩy sau trạng ngữ.** Sai: "Để kiểm tra … nhóm giữ nguyên…". Đúng: "Để kiểm tra …, nhóm giữ nguyên…".
- **Từ nối trùng nghĩa:** "vì vậy nhờ đó", "do đó nên". Giữ một từ.
- **Câu thiếu chủ ngữ hoặc ghép sai,** ví dụ "Cụ thể có kết quả ta có:". Viết lại thành "Kết quả cụ thể như sau:".
- **Dấu chấm kép "..", dấu chấm đứng một mình trên một dòng, dấu phẩy thừa trước dấu chấm.**
- **Hình và bảng không được nhắc trong bài.** Mỗi hình, bảng cần một câu dẫn, ví dụ "(Hình 4.6)" hoặc "Bảng 4.4 cho thấy…".

## 3. Quy tắc nội dung (bắt buộc)

- **Số thập phân dùng dấu phẩy** (0,7232). Hàng nghìn dùng dấu chấm (1.000).
- **Mọi con số phải truy được về `00_tai_lieu_tong_quan/bang/*.csv`.** Chưa có số thì để ô **[CHỜ KẾT QUẢ]**. Không đoán số.
- **Kết quả chính viết là "xu hướng", không có ý nghĩa thống kê** (Δ +0,0043, p = 0,061). Không viết "vượt trội", "ổn định hơn rõ".
- **Levene p = 0,026 chỉ để thăm dò.** Lợi thế độ lệch chuẩn chỉ thấy ở epoch tốt nhất.
- **Tóm tắt, mục tiêu ở Ch.1 và kết luận ở Ch.5 phải cùng một giọng.**
- **Tên gọi thống nhất:** "YOLO26s-seg", "C2TSVMamba", "mô hình gốc", "mô hình đề xuất". Không viết "YOLOv26".
- **Tài liệu tham khảo:** IEEE, đánh số theo lần trích đầu. Bài arXiv ghi phiên bản (v1) và ngày truy cập. Không tự thêm tài liệu khi chủ dự án chưa đồng ý; thêm thì phải dời số mọi tài liệu phía sau.

## 4. Định dạng Word phải giữ

- A4; lề trái 3,5 cm, ba lề còn lại 2,5 cm; Times New Roman 13; giãn dòng 1,3; thụt đầu dòng 1 cm.
- Tiêu đề dùng Heading 1–3 ("CHƯƠNG 1: TỔNG QUAN", "1.1. …", "1.2.1. …").
- Chú thích dùng style Image Caption hoặc Table Caption, dạng "Hình 4.5: …" (dấu hai chấm). Hình lấy từ bài báo thì ghi nguồn [n] cuối chú thích.
- Công thức canh giữa, số (2.13) canh phải.
- Sửa xong thì cập nhật trường (mục lục, danh mục hình, danh mục bảng), rồi xuất PDF và đếm trang. Mục tiêu 70–80 trang cả quyển.

## 5. Cách sửa file Word

1. **Không ghi đè bản đã nộp.** Sao ra `06_bao_cao/sua_theo_nhan_xet/` rồi sửa trên bản sao.
2. **Sửa chữ nhỏ trên từng run bằng python-docx** để giữ định dạng. Đoạn viết lại thì thay nội dung đoạn, giữ style của đoạn.
3. **Ghi lại từng thay đổi** (mục, trước, sau) vào `sua_theo_nhan_xet/NHAT_KY_SUA.md` để nhóm duyệt.
4. **Cập nhật trường và xuất PDF bằng Word COM** (`win32com.client`), dùng `python3.13`.
5. **Báo lại số trang và danh sách chỗ còn [CHỜ KẾT QUẢ].**
