# J. Kế hoạch làm bản rút gọn (phần thân khoảng 70 trang)

Ngày lập: 31/10/2026. Đã duyệt và **triển khai xong đợt 0–7 ngày 31/10/2026** (đợt 8: cập nhật ngữ cảnh xong, chờ commit).

**Kết quả đo (PDF ghép từ Word):**

| Phần | Bản đầy đủ | Bản rút gọn | Mục tiêu |
|---|---:|---:|---:|
| Trang đầu | 16 | 15 | 15 |
| Mở đầu | 8 | 6 | 5 |
| Ch.1 | 9 | 6 | 7 |
| Ch.2 | 17 | 10 | 11 |
| Ch.3 | 24 | 12 | 12 |
| Ch.4 | 10 | 8 | 7 |
| Ch.5 | 18 | 9 (chưa chèn 7 ảnh chụp, dự kiến thêm 3–4) | 11 |
| Ch.6 | 28 | 16 | 16 |
| Kết luận | 5 | 3 | 3 |
| **Thân** | **119** | **70** | **khoảng 72** |
| Tài liệu tham khảo | 7 | 7 | 6–7 |
| Phụ lục | 5 | 17 | 8–10 |
| **Cả quyển** | **147** | **109** | **khoảng 100** |

Phụ lục mới đặt tên theo thứ tự xuất hiện: **E** phân công theo hạng mục (Bảng 0.3 cũ), **F** chi tiết Ch.3 (truy vết tensor, ví dụ quét, ước tính chi phí, hình cơ cấu tham số), **G** API và MongoDB của ứng dụng, **H** 11 hình và 3 bảng phụ của Ch.6. Phụ lục dài hơn dự kiến vì giữ đủ hình phụ; nếu cần sát 100 trang, có thể bỏ bớt hình ở Phụ lục H.

**Kiểm tra bằng script** (`ghep_word/kiem_tra_rut_gon.py`, chạy `python3.13 ghep_word/kiem_tra_rut_gon.py .` trong `06_bao_cao/`, ngày 31/10): hình, bảng, công thức đánh số liên tục; mọi chỗ nhắc Bảng/Hình/(x.y)/mục trỏ đúng; 57 tài liệu, thứ tự lần trích đầu 1→57; mọi con số trong bản rút gọn đều có trong bản đầy đủ (ngoài số mục và tham số YAML).

**Phản biện (subagent, 31/10):** không thấy chỗ sai nghĩa kết quả chính; đã sửa 8 điểm: ví dụ mặt nạ mẫu thiếu giá trị P₁, P₂; thêm lại ví dụ Δ₃ = 2 (Mamba chọn lọc) và ví dụ giải mã hộp ở Ch.2; Thuật toán 3.2 cũ chuyển thành Thuật toán PL.1 (Phụ lục F.4); Levene "chỉ đúng ở epoch tốt nhất" ở Kết luận; ghi rõ 11,8/20,4 ms của mô hình nào; MambaPSA "tăng tốc trên CPU"; "chỉ 5 seed" ở mục 3.7; thống nhất thứ tự toán hạng (2.7) với (3.14) ở cả hai bản.

**Sửa kèm ở bản đầy đủ:** mục 3.9–3.10 còn ghi "chưa huấn luyện các chế độ tách thành phần", "số tham số ước tính", nay sửa theo thực tế (ablation đã chạy, số tham số đếm từ checkpoint, khớp); năm dòng chèn hình Ch.4 đổi sang dạng `![Hình 4.x](...)` để vào danh mục hình. Script ghép Word nhận thêm `Hình PL.x` và gợi ý cỡ `{width=..cm}`.

## 1. Hai bản báo cáo song song

| | Bản đầy đủ (giữ nguyên) | Bản rút gọn (làm mới) |
|---|---|---|
| Markdown | `06_bao_cao/md_bao_cao/` (không sửa nữa, chỉ sửa lỗi nếu phát hiện) | `06_bao_cao/md_bao_cao_rut_gon/` (sao từ bản đầy đủ rồi nén) |
| Word, PDF | `CNTT_KLCN182_BaoCaoKhoaLuan_V3_day_du.docx/.pdf` (147 trang) | `CNTT_KLCN182_BaoCaoKhoaLuan_V3_rut_gon.docx/.pdf` (khoảng 100 trang) |
| Ghép Word | `ghep_word.py --md md_bao_cao --ra day_du` | `ghep_word.py --md md_bao_cao_rut_gon --ra rut_gon` |

- **Đánh dấu bản đầy đủ trong git:** gắn tag `ban_day_du_147` vào commit trước khi bắt đầu, để luôn quay lại được.
- **Dùng chung** thư mục hình (`06_bao_cao/hinh/`), số liệu (`bang/*.csv`) và `_KIEM_TRA/`. Thư mục rút gọn nằm cùng cấp nên đường dẫn `../hinh/...` vẫn đúng.
- **Không đổi bất kỳ con số kết quả nào.** Bản rút gọn chỉ bớt lời giải thích, bớt hình phụ và chuyển chi tiết xuống phụ lục.

## 2. Hiện trạng và mục tiêu từng phần

| Phần | Trang hiện tại | Từ hiện tại | Mục tiêu trang | Mục tiêu từ |
|---|---:|---:|---:|---:|
| Mở đầu | 8 | 2.993 | 5 | 1.500 |
| Ch.1 Tổng quan | 9 | 3.323 | 7 | 2.300 |
| Ch.2 Cơ sở lý thuyết | 17 | 6.459 | 11 | 3.600 |
| Ch.3 Mô hình đề xuất | 24 | 8.145 | 12 | 3.500 |
| Ch.4 Dữ liệu | 10 | 3.113 | 7 | 2.000 |
| Ch.5 Cài đặt, ứng dụng | 18 (+7 khi chèn ảnh) | 4.987 | 11 (gồm 6–8 ảnh chụp) | 2.300 |
| Ch.6 Thực nghiệm | 27 | 8.242 | 16 | 4.200 |
| Kết luận | 6 | 1.604 | 3 | 900 |
| **Phần thân** | **119 (125 khi có ảnh)** | **38.866** | **khoảng 72** | **khoảng 20.300** |
| Trang đầu | 16 | | 15 | |
| Tài liệu tham khảo | 7 | | 6–7 | |
| Phụ lục | 5 | | 8–10 | |
| **Cả quyển** | **147** | | **khoảng 100** | |

## 3. Cách nén từng phần

Nguyên tắc chung:
- **Giữ:** mọi bảng số chính, câu kết luận chính kèm số liệu, các mục thang điểm yêu cầu (định nghĩa có ví dụ, các bước thuật toán, ưu và nhược điểm, độ đo, ablation, dữ liệu thực tế, ứng dụng, phân công).
- **Bỏ:** phần "Kết chương" dài (thay bằng 2–3 câu), câu dẫn nhập lặp, giải thích lặp giữa các chương, ví dụ trùng ý.
- **Chuyển xuống Phụ lục:** chi tiết kỹ thuật dài, hình bổ sung, bảng API.

| Phần | Giữ trong thân | Chuyển xuống Phụ lục | Bỏ hoặc viết gọn |
|---|---|---|---|
| **Mở đầu** | Lý do; mục tiêu và CH1–CH4; đối tượng, phạm vi; phương pháp; đóng góp; Bảng 0.1 (kế hoạch), Bảng 0.2 (phân công) | Bảng 0.3 (phân công theo hạng mục) | Viết gọn mỗi mục; mục 7 (bố cục) còn một đoạn |
| **Ch.1** | 1.1–1.2 gộp; Bảng 1.1 dữ liệu; các hướng nghiên cứu (mỗi công trình 1–2 câu); Bảng 1.2, 1.3; 1.6 trong nước | | Kết chương còn 2 câu; bớt giải thích U-Net, Transformer |
| **Ch.2** | 2.1 có Hình 2.1; YOLO, YOLO26-seg (các bước, ưu nhược); SSM, Mamba, VMamba (các bước, ưu nhược); độ đo (mỗi độ đo một công thức, giữ một ví dụ tính chung); kiểm định t, Wilcoxon, d_z | | Gọn 2.2 (CNN) và 2.5 (attention) thành một mục ngắn; bỏ ví dụ trùng (giữ ví dụ tích chập, ví dụ IoU/Dice, ví dụ quét SS2D); bỏ ví dụ giải mã hộp |
| **Ch.3** | Động cơ (3.1, gọn); kiến trúc tổng thể (Hình a01); khối C2TSVMamba: ý tưởng, ba thành phần, công thức chính, Hình a02, Bảng tham số tóm tắt; thuật toán quét: ý tưởng, độ phức tạp (gọn); ưu nhược điểm; các chế độ ablation | Truy vết kích thước tensor (3.3.6); bảng tham số chi tiết; ví dụ phép quét từng bước (3.4.3); ước tính chi phí tầng 10 (3.4.5) | Gộp 3.5–3.8 (khởi tạo, mất mát, quy trình, FP32) thành một mục "Huấn luyện và lưu trọng số" khoảng 1,5 trang |
| **Ch.4** | Nguồn dữ liệu, BG20, chuyển nhãn (5 bước, công thức chính), đổi kích thước, tăng cường; Hình 4.5 quy trình | | Gộp 4.6–4.8; thu nhỏ hình 4.1–4.4. **Chương của bạn cùng nhóm: ghi chú lại các chỗ đã nén** |
| **Ch.5** | Môi trường (gộp 3 bảng còn 1); cài đặt hai mô hình (gọn); cấu trúc lưu kết quả; PolypVision: kiến trúc, chức năng, 6–8 ảnh chụp quan trọng nhất; dữ liệu thực tế (5.9) | Bảng API (5.6.2), cấu trúc bản ghi MongoDB (5.7), bảng kiểm thử | Bớt mô tả notebook Kaggle; 5.10 và 5.11 gộp còn một đoạn |
| **Ch.6** | Thiết lập (gọn); Bảng 6.2 + Hình h02 (từng seed) + Hình h04 (ma trận nhầm lẫn); độ ổn định (Bảng 6.3, gọn); Bảng pixel + Hình p01 + q01; topology (Bảng 6.9 + Hình o01); chi phí (Bảng 6.10, 6.11); ablation (Bảng 6.12 + Hình k01); dữ liệu ngoài (Bảng 6.14 + Hình x01 + x03); thảo luận (gọn) | Hình h01, r01, r02, r04, h03, c01, p02, p03, o02, e02, x02; Bảng 6.15, 6.16 | Bỏ các đoạn mô tả lặp lại số đã có trong bảng; 6.9 kết chương còn 3 câu |
| **Kết luận** | Kết quả đạt được (gọn); trả lời CH1–CH4 (mỗi câu 3–4 dòng); hạn chế, hướng phát triển dạng gạch đầu dòng ngắn | | Bỏ phần lặp lại Chương 6 |
| **Phụ lục** | Giữ A–D hiện có; thêm E (chi tiết Ch.3), F (hình kết quả bổ sung), G (API và lưu trữ của ứng dụng), Bảng 0.3 | | |

## 4. Những việc kỹ thuật đi kèm

1. **Đánh số lại hình, bảng, công thức** trong từng chương sau khi bỏ hoặc chuyển:
   - viết script đổi cả chú thích lẫn chỗ nhắc trong văn ("Hình 6.9", "Bảng 3.7", "(2.6)");
   - hình và bảng chuyển xuống phụ lục mang số mới "Hình PL.x", "Bảng PL.x".
2. **Tài liệu tham khảo:** cố giữ đủ 57 tài liệu đều được trích. Nếu nén làm mất chỗ trích của tài liệu nào thì:
   - hoặc giữ một câu ngắn có trích tài liệu đó;
   - hoặc bản rút gọn có danh mục riêng, đánh số lại bằng script như đợt rút gọn 57.
3. **Tham chiếu chéo** ("xem mục 3.4.3", "mục 6.2.2") phải trỏ đúng mục còn lại hoặc trỏ sang phụ lục.
4. **Không đổi số liệu:** sau khi nén, dùng script so tất cả các con số trong bản rút gọn với bản đầy đủ. Bản rút gọn chỉ được ít số hơn, không được có số mới hay số khác.

## 5. Kế hoạch chạy theo đợt

| Đợt | Việc | Kiểm tra / duyệt |
|---|---|---|
| 0 | Gắn tag `ban_day_du_147`; đổi tên Word/PDF hiện tại thành `_day_du`; tạo `md_bao_cao_rut_gon/`; thêm tham số `--md`, `--ra` cho `ghep_word.py` | Ghép lại bản đầy đủ ra đúng 147 trang |
| 1 | **Làm mẫu:** nén Mở đầu, Chương 1, Kết luận; ghép thử | **Gửi PDF cho chủ dự án duyệt mức nén và văn phong** trước khi làm tiếp |
| 2 | Nén Chương 2 | Còn đủ ví dụ, các bước, ưu nhược theo thang điểm |
| 3 | Nén Chương 3, tạo Phụ lục E | Công thức chính và trích dẫn còn đủ |
| 4 | Nén Chương 4, 5, tạo Phụ lục G, chuyển Bảng 0.3 | Ghi chú cho bạn cùng nhóm về Ch.4 |
| 5 | Nén Chương 6, tạo Phụ lục F | Mọi bảng số chính còn trong thân |
| 6 | Script đánh số lại hình, bảng, công thức; kiểm tra tham chiếu chéo, trích dẫn 1→N, so số liệu với bản đầy đủ | Không có số mới hay số sai |
| 7 | Ghép Word bản rút gọn, đo trang; nếu lệch ngoài 65–75 trang thân thì chỉnh thêm; subagent phản biện đọc lại toàn bản (chỉ đọc) | Phần thân khoảng 70 trang |
| 8 | Cập nhật file ngữ cảnh (hai bản báo cáo); commit khi chủ dự án đồng ý | |

Thời gian dự kiến: khoảng 5–6 giờ, chia nhiều phiên.
