# Context: bản báo cáo đã nộp và nhận xét của GVHD (06/11/2026)

Đọc file này trước khi sửa bản Word nộp thầy. Kế hoạch ở `KE_HOACH.md`, cách viết ở `.claude/skills/van-phong-bao-cao-nhom/SKILL.md`.

## 1. Các file

| File | Vai trò |
|---|---|
| `06_bao_cao/BaoCaoKhoaLuan_CNTT_KLCN182.docx` | Bản đã nộp thầy (77 trang). **Không ghi đè.** |
| `06_bao_cao/new_bao_cao/BaoCaoKhoaLuan_CNTT_KLCN182.docx` | Bản gần giống, trước khi nộp (76 trang). Không dùng làm gốc. |
| `06_bao_cao/Nhan_xet_KLCN-CNTT-182.docx` | Nhận xét của GVHD: 4 ý hình thức, 6 ý nội dung |
| `06_bao_cao/Bieu mau do an_khoa luan. K.CNTT_HUIT_2025_V3.docx` | Biểu mẫu Khoa, lấy trang cam đoan và nhận xét |
| `06_bao_cao/sua_theo_nhan_xet/` | Nơi đặt bản sửa và ghi chú |

## 2. Cấu trúc bản đã nộp

- **Đầu sách:** Bìa chính (thiếu GVHD, mã đề tài), bìa phụ, Lời cảm ơn, Mục lục, Danh mục ký hiệu, Danh mục hình, Danh mục bảng. Chưa có Lời cam đoan, trang nhận xét, Tóm tắt.
- **Ch.1 Tổng quan:** 1.1–1.5, phân công ở Bảng 1.5.
- **Ch.2 Cơ sở lý thuyết:** 2.1–2.9, công thức (2.1)–(2.28).
- **Ch.3 Phương pháp đề xuất:** 3.1.1–3.1.9 và 3.2.1–3.2.5.
- **Ch.4 Thực nghiệm:** 4.1–4.9; ablation 10 seed ở 4.5.5 / Bảng 4.7.
- **Ch.5 Kết luận:** 5.1–5.3.
- **TLTK:** 33 mục IEEE, trích theo thứ tự 1→33.
- **Định dạng:** A4; lề trái 3,5 cm, ba lề còn lại 2,5 cm; Times New Roman 13; giãn dòng 1,3; thụt đầu dòng 1 cm. Style Heading 1–3, Image Caption, Table Caption. Mục lục và danh mục là trường tự động.

## 3. Đã kiểm (05–06/11/2026)

- **TLTK:**
  - 33/33 mục có thật; 22 DOI khớp Crossref/DataCite; 26 mục có PDF trong `../TLTK`.
  - Lỗi: [7] phải là "H. Dao Viet"; [4] và [9] cần ghi phiên bản arXiv (v1) và ngày truy cập.
- **Số liệu trong bài:**
  - Khớp `00_tai_lieu_tong_quan/bang/`: 20 seed (04), pixel (12), ablation 10 seed (`bang/ablation_10seed/`).
  - Seed 0: mô hình gốc 0,7366, TSVM 0,7245.
- **Lỗi đã định vị** (xem `KE_HOACH.md` mục 3–4):
  - "kiễm", "tron đó", "Hình 4.5;", "10,8%,";
  - 3 dòng chỉ có dấu chấm;
  - 6 chỗ "..".
- **Danh mục và chú thích:**
  - Danh mục hình thiếu Hình 4.4 và 4.7 (cần cập nhật trường).
  - 34/41 hình, bảng chưa có câu dẫn trong bài.

## 4. Nhận xét của GVHD tóm tắt

| Nhóm | Ý chính | Quyết định |
|---|---|---|
| Hình thức 1 | Thiếu cam đoan, nhận xét; bìa thiếu GVHD và mã đề tài | Sửa |
| Hình thức 2–3 | Câu dài, chính tả, dấu câu | Sửa |
| Hình thức 4 | arXiv ghi phiên bản, ngày truy cập; thêm 3–5 mô hình SOTA | Sửa |
| Nội dung 1 | Kết quả chưa có ý nghĩa; thống nhất Tóm tắt, Ch.1, Ch.5; phân tích CVC; 42 seed | Sửa chữ; 42 seed thì không làm |
| Nội dung 2 | Không có tập test riêng | Không train lại; thêm epoch 100 (Δ +0,0025, p 0,456); đưa vào hướng phát triển |
| Nội dung 3 | "Ổn định hơn rõ" mâu thuẫn với Ch.5 | Sửa câu |
| Nội dung 4 | So sánh chưa công bằng; thiếu đối chứng cùng số tham số; ablation 20 seed | Đang chạy ablation 20 seed và C2PSA rộng; sẽ làm PraNet/U-Net ở 640, Polyp-PVT, VM-UNet, MambaPSA |
| Nội dung 5 | Ảnh nền thiếu đa dạng | Không làm, đưa vào hạn chế |
| Nội dung 6 | Ứng dụng dùng seed 0 chưa đại diện | Chọn seed gần trung vị nếu kịp; ý kiến bác sĩ đưa vào hạn chế |

## 5. Số liệu dùng được ngay

- **Kết quả chính (20 seed):** Δ +0,0043, KTC 95% [−0,0002; 0,0088], p = 0,061, 13/20.
- **Độ lệch chuẩn:** 0,0072 so với 0,0118. Levene p = 0,026, chỉ thăm dò.
- **Epoch 100 cố định:** 0,7093 so với 0,7119, Δ +0,0025, p 0,456. Nguồn `bang/04b_do_nhay_quy_tac_epoch.csv`.
- **Epoch của best.pt:** Δ +0,0048, p 0,062.
- **C2PSA rộng:** `[-1, 2, C2PSA, [1024, 0.75]]`, scale s, tầng 10 có 1.830.016 tham số (TSVM 1.811.201, +1%). Tầng 10 học từ đầu, giống TSVM.
