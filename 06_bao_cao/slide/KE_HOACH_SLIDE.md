# Kế hoạch slide bảo vệ (Canva "Khóa luận cử nhân", DAHPtP9XqEY)

Cập nhật 28/10/2026. Khổ 1920×1080, mẫu của trường. Ký hiệu bố cục:
- **Z** = so le hình–chữ (hình một bên, 2–4 dòng chữ bên kia, đổi bên mỗi slide);
- **H** = chỉ một hình lớn + tiêu đề ngắn (thuyết trình bằng lời, lời nói để ở ghi chú);
- **C** = chữ / số liệu nổi bật, không có hình.

Mã hình là tên tệp trong `06_bao_cao/hinh/` (`chung/vi/`, `ket_qua_20seed/vi/`, `chuong4/`). "Mới" = hình cần vẽ thêm bằng `ve_hinh.py`. "Chụp" = ảnh màn hình ứng dụng (Chương 5).

## Phần chính

| # | Phần | Slide | Bố cục | Hình |
|---:|---|---|---|---|
| 1 | Mở đầu | Bìa | C | |
| 2 | | Nội dung trình bày | C | |
| 3 | | Lý do chọn đề tài | C (số liệu trái, ý phải) | |
| 4 | | Mục tiêu và câu hỏi nghiên cứu (CH1–CH4) | C | |
| 5 | | Đối tượng, phạm vi, đóng góp | C | |
| 6 | Lý thuyết | Bốn kiểu đầu ra: phân loại, phát hiện, phân đoạn ngữ nghĩa, thực thể | H | t01 |
| 7 | | YOLO26-seg: các bước, ưu/nhược | Z | a01 (phần gốc) |
| 8 | | SSM, Mamba, VMamba: quét chọn lọc | Z | a03 |
| 9 | Mô hình đề xuất | Kiến trúc tổng thể, vị trí tầng 10 | H | a01 |
| 10 | | Khối C2TSVMamba | H | a02 |
| 11 | | Nhánh SS2D | H | a04 |
| 12 | | Số tham số tầng 10 so với C2PSA | Z | m01 |
| 13 | Dữ liệu | Nguồn dữ liệu: Kvasir-SEG + ảnh nền | Z | h4_1 |
| 14 | | Thành phần BG20 (1.040 / 160) | Z | d01 |
| 15 | | Số polyp mỗi ảnh | H | d02 |
| 16 | | Diện tích polyp | H | d04 |
| 17 | | Mặt nạ → nhãn đa giác | Z | h4_2 |
| 18 | | Số đỉnh đa giác | H | d03 |
| 19 | | Thu phóng giữ tỉ lệ + LetterBox (640 / 672) | Z | h4_3 |
| 20 | | Tăng cường dữ liệu | H | h4_4 |
| 21 | | Quy trình tiền xử lý | H | h4_5 (chờ sửa ô cuối) |
| 22 | Thực nghiệm | Thiết lập: 20 seed ghép cặp, kiểm định t + Wilcoxon | C | |
| 23 | Kết quả 20 seed | Tổng quan 5 chỉ số mặt nạ | H | h01 |
| 24 | | Mask mAP50–95 từng seed (nối cặp) | H | h02 |
| 25 | | Hiệu số Δ từng seed | H | r01 |
| 26 | | Phân bố hiệu số | H | r03 |
| 27 | | Mask mAP50 từng seed | H | Mới (h05) |
| 28 | | Precision và Recall từng seed | H | r05 |
| 29 | | Giá trị từng seed của 5 chỉ số | H | h01b |
| 30 | | Độ ổn định: phân bố 20 seed | H | r02 |
| 31 | | Độ nhạy theo quy tắc chọn epoch | H | r04 |
| 32 | | mAP50–95 theo epoch | H | h03 |
| 33 | | Val seg loss theo epoch | H | c01 |
| 34 | | Train seg loss, mốc tắt Mosaic | H | c02 |
| 35 | | Ma trận nhầm lẫn | H | h04 |
| 36 | | TP / FP / FN | H | e01 |
| 37 | Theo pixel | Dice, IoU, P, R của 4 mô hình | H | p01 |
| 38 | | Dice từng seed | H | p02 |
| 39 | | Báo nhầm ảnh nền | H | p03 |
| 40 | | Ví dụ dự đoán | H | q01 |
| 41 | Topology | Tỉ lệ ảnh đúng topology | H | o01 |
| 42 | | Các kiểu lỗi topology | H | o02 |
| 43 | Chi phí | Số tham số và dung lượng | H | e03 |
| 44 | | Độ trễ CPU | H | e02 |
| 45 | | GFLOPs và độ trễ GPU | H | Mới (g01) |
| 46 | Ablation | Thiết kế 3 biến thể | C | |
| 47 | | Kết quả mAP50–95 năm cấu hình | H | Mới (k01, chờ Kaggle) |
| 48 | | Hiệu số so với mô hình đầy đủ | H | Mới (k02, chờ Kaggle) |
| 49 | Dữ liệu ngoài | Dice trên 4 bộ dữ liệu | H | x01 |
| 50 | | PolypGen theo trung tâm | H | x02 |
| 51 | | Báo nhầm trên PolypGen | H | x03 |
| 52 | Ứng dụng | Kiến trúc PolypVision | H | s01 |
| 53 | | Web: phân tích một ảnh | H | Chụp 5.7 |
| 54 | | Web: so sánh hai mô hình | H | Chụp 5.8 |
| 55 | | Web: lịch sử, bảng điều khiển | H | Chụp 5.9 / 5.10 |
| 56 | | Di động: suy luận | H | Chụp 5.13 |
| 57 | | Di động: so sánh | H | Chụp 5.14 |
| 58 | | Ảnh ngoài trên ứng dụng | H | Chụp 5.17 / 5.18 |
| 59 | Kết luận | Kết luận (trả lời CH1–CH4) | C | |
| 60 | | Hạn chế | C | |
| 61 | | Hướng phát triển | C | |
| 62 | | Cảm ơn | C | |

**Tổng phần chính: khoảng 62 slide** (8 C mở đầu/kết luận, khoảng 45 H, khoảng 9 Z).

## Slide dự phòng (sau trang Cảm ơn, dùng khi hội đồng hỏi)

Bảng số liệu đầy đủ (Bảng 6.2, 6.7, 6.9, 6.11, 6.14), kiểm tra trùng ảnh PolypGen, tỉ lệ bỏ sót trọn ảnh trên dữ liệu ngoài, ảnh chụp trang quản trị và lịch sử. Khoảng 5–8 slide.

## Hình cần vẽ thêm

- h05: mask mAP50 từng seed nối cặp (giống h02).
- g01: GFLOPs và độ trễ GPU hai mô hình (từ `bang/16_flops_do_tre_gpu.csv`).
- k01, k02: ablation, chờ kết quả Kaggle.

## Ghi chú thời lượng

Nếu thời gian trình bày là 15–20 phút, 62 slide nghĩa là khoảng 15–20 giây mỗi slide. Các slide H chỉ cần nói một ý. Nếu hội đồng giới hạn chặt hơn, chuyển các slide 26, 29, 34, 36, 15, 18 sang phần dự phòng.
