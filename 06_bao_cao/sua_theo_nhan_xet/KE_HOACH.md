# Kế hoạch sửa báo cáo theo nhận xét của GVHD (06/11/2026)

- **Bản gốc:** `06_bao_cao/BaoCaoKhoaLuan_CNTT_KLCN182.docx` (bản đã nộp thầy, 77 trang). Không ghi đè bản này.
- **Nhận xét:** `06_bao_cao/Nhan_xet_KLCN-CNTT-182.docx`.
- **Bản sửa:** `06_bao_cao/sua_theo_nhan_xet/BaoCaoKhoaLuan_CNTT_KLCN182_sua.docx`. Sửa trực tiếp trên Word, giữ nguyên định dạng của nhóm.
- **Mục tiêu:** 70–80 trang cả quyển. Viết theo văn phong của nhóm (xem `.claude/skills/van-phong-bao-cao-nhom/SKILL.md`).
- **Trạng thái:** CHỜ DUYỆT. Chưa sửa gì.

## Phần 1. Sửa ngay trên Word (không cần kết quả mới)

| # | Việc | Chỗ sửa | Ghi chú |
|---|---|---|---|
| 1 | Thêm Lời cam đoan, trang Nhận xét GVHD, trang Nhận xét GVPB | Sau bìa phụ | Lấy khung từ `Bieu mau do an_khoa luan. K.CNTT_HUIT_2025_V3.docx` |
| 2 | Bìa chính thêm GVHD và mã đề tài CNTT-KLCN182 | Bìa chính | Giống bìa phụ |
| 3 | Sửa lỗi thầy chỉ ra | "kiễm" → "kiểm" (4.2.1); "tron đó" → "trong đó" (4.3.1); "Hình 4.5;" → "Hình 4.5:" (chú thích và danh mục); "10,8%," (4.7); dòng chỉ có dấu chấm (2.1.2, 4.5.3, 4.6) | Đã định vị đủ |
| 4 | Xóa 6 dấu ".." | 3.1.6 (2 chỗ), 4.4.1, 4.5.1, 4.7, 5.3 | Đã định vị đủ 6 chỗ |
| 5 | Tách câu dài, bỏ từ thừa | Toàn văn, ưu tiên các câu thầy dẫn: "vì vậy nhờ đó…", "Cụ thể có kết quả ta có:", câu hỏi trung tâm ở 1.1 | Mỗi câu một ý, thêm dấu phẩy sau trạng ngữ |
| 6 | Thêm phần Tóm tắt (khoảng 1 trang) | Sau Lời cảm ơn | Kết quả chính là xu hướng, chưa có ý nghĩa thống kê |
| 7 | Thống nhất kết luận ở Ch.1 (mục tiêu) và Ch.5 | 1.3, 5.1 | Cùng giọng "xu hướng / thăm dò" |
| 8 | Sửa "ổn định hơn rõ" | 4.5.1 | SD nhỏ hơn khoảng 39%, chỉ thấy ở epoch tốt nhất, Levene chỉ để tham khảo |
| 9 | Thêm kết quả epoch 100 cố định | 4.5.1 | Δ +0,0025, p 0,456 (`bang/04b`); trả lời ý "chọn epoch trên tập kiểm định" |
| 10 | Thêm đoạn phân tích vì sao kém trên CVC-ClinicDB, CVC-ColonDB | 4.7 | Viết dạng giả thuyết, không khẳng định |
| 11 | TLTK: ghi phiên bản arXiv và ngày truy cập cho [4], [9]; sửa họ tác giả [7] thành "H. Dao Viet" | TLTK | |
| 12 | Thêm 3–5 mô hình SOTA kèm điểm trên Kvasir-SEG lấy từ bài gốc (Polyp-PVT, VM-UNet…) | Bảng 1.1 hoặc 4.6 | Phải đọc PDF gốc, ghi rõ "số do tác giả công bố". Tài liệu mới cần chủ dự án đồng ý |
| 13 | Câu dẫn cho các hình, bảng chưa được nhắc trong bài | Toàn văn | Ví dụ "(Hình 4.6)" |
| 14 | Bỏ Bảng 1.3 trùng với 4.2.1; cập nhật mục lục, danh mục hình (đang thiếu Hình 4.4, 4.7) | Ch.1, đầu sách | Bấm F9 trong Word |
| 15 | Viết lại 5.2 Hạn chế và 5.3 Hướng phát triển | Ch.5 | Gồm: tách tập test (khoảng 139 giờ GPU), 42 seed, ảnh nền đa dạng, ý kiến bác sĩ |
| 16 | Rút gọn để bù phần thêm (khoảng 4 trang) | Ch.2 là chính | Giữ tổng 70–80 trang |

## Phần 2. Chờ kết quả huấn luyện (nhóm đang chạy)

| Việc | Trạng thái | Khi có kết quả |
|---|---|---|
| Ablation seed 10–19 (đủ 20 seed) | Đang chạy | `tinh_ablation.py --seeds 20` (cần mở rộng), vẽ lại k01/k02, sửa 4.5.5 và Bảng 4.7 |
| C2PSA rộng (e = 0,75, tầng 10 = 1.830.016 tham số), seed 0–19 | Đang chạy | Thêm vào bảng ablation, kiểm định ghép cặp với TSVM |
| PraNet, U-Net ở 640, có tăng cường | Sẽ làm | Cập nhật Bảng 4.8, Hình 4.10 |
| Polyp-PVT, VM-UNet | Sẽ làm | Thêm vào 4.6 |
| Tái hiện MambaPSA | Sẽ làm | Rủi ro: bài gốc làm phát hiện vật thể trên PASCAL VOC; cần kiểm mã nguồn có công khai không |

Trong bản sửa, các mục chờ kết quả để ô **[CHỜ KẾT QUẢ]**. Không điền số khi chưa chạy đủ.

## Phần 3. Không làm, đưa vào Hạn chế và Hướng phát triển

- Tách tập test riêng hoặc dùng 5-fold.
- Tăng lên khoảng 42 cặp seed.
- Ảnh nền đa dạng (nhiều vị trí giải phẫu, thử tỷ lệ 10/20/40%).
- Ý kiến định tính của bác sĩ nội soi.

## Thứ tự làm

1. Phần 1, mục 1–5 (lỗi thầy chỉ ra). Nhanh, chắc chắn.
2. Phần 1, mục 6–10 (nội dung, dùng số đã có).
3. Phần 1, mục 11–16 (TLTK, câu dẫn, rút gọn), rồi xuất PDF và đếm trang.
4. Phần 2: điền số khi kết quả về.
