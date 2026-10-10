# Lý thuyết học tập — YOLO26-seg + VMamba cho phân đoạn polyp

Bộ tài liệu tự học cho người mới tiếp cận đề tài. Nội dung bám theo code, config và kết quả có trong repo (cập nhật 10/10/2026).

| Bài | Nội dung | Thời gian đọc |
|---|---|---|
| [Bài 1 — YOLO26-seg, VMamba và chỉ số đánh giá](Bai01_YOLO26seg_VMamba_va_ChiSoDanhGia.md) | Kiến trúc YOLO26-seg, cơ chế prototype mask, NMS-free, VMamba/SS2D, khối TSVM, IoU → Precision/Recall → mAP@50-95, thống kê 10 seed, đọc kết quả đề tài | ~60 phút |
| [Bài 2 — Tiền xử lý dữ liệu](Bai02_TienXuLyDuLieu.md) | Mask → polygon (Otsu, Closing, contour, approxPolyDP), bộ BG20 và ảnh nền, chia tập, LetterBox, chuẩn hóa, augmentation | ~40 phút |

## Bản giáo trình PDF

Bản PDF viết thành văn xuôi kiểu giáo trình và có thêm phần kiến thức nền. Định dạng: Times New Roman 13, thụt dòng đầu 1,27 cm, cách trước/sau 3 pt, giãn dòng bội số 1,37.

- [GiaoTrinh_Bai01_YOLO26seg_VMamba_ChiSoDanhGia.pdf](GiaoTrinh_Bai01_YOLO26seg_VMamba_ChiSoDanhGia.pdf), 34 trang
- [GiaoTrinh_Bai02_TienXuLyDuLieu.pdf](GiaoTrinh_Bai02_TienXuLyDuLieu.pdf), 21 trang

Nội dung nằm ở `ma_nguon/noi_dung_bai0x.txt`; hình của Bài 1 nằm trong `hinh/`. Bài 2 dùng lại hình trong `output/tien_xu_ly/hinh/`. Dựng lại từ gốc repo:

```powershell
$env:PYTHONIOENCODING = "utf-8"
python output/LyThuyet_HocTap/ma_nguon/sinh_hinh_bai01.py
python output/LyThuyet_HocTap/ma_nguon/dung_pdf.py output/LyThuyet_HocTap/ma_nguon/noi_dung_bai01.txt output/LyThuyet_HocTap/GiaoTrinh_Bai01_YOLO26seg_VMamba_ChiSoDanhGia.pdf
python output/LyThuyet_HocTap/ma_nguon/dung_pdf.py output/LyThuyet_HocTap/ma_nguon/noi_dung_bai02.txt output/LyThuyet_HocTap/GiaoTrinh_Bai02_TienXuLyDuLieu.pdf
```

## Lộ trình học theo Pareto

Ba buổi đọc, ưu tiên 20% kiến thức mang lại 80% hiểu biết:

1. **Buổi 1 (30 phút) — Nắm khung:** đọc **Phần 0** của cả hai bài và các hộp "💡 Ý chính". Tự vẽ lại sơ đồ dòng chảy: *dữ liệu → mô hình → chỉ số*.
2. **Buổi 2 (60 phút) — Hiểu cơ chế:** Bài 1 Phần 2–4 (YOLO26-seg) và Phần 7 (chỉ số). Bài 2 Phần 3–4 (mask → polygon, BG20).
3. **Buổi 3 (45 phút) — Đề tài và phản biện:** Bài 1 Phần 5–6 (VMamba, TSVM) và Phần 8 (kết quả). Làm hết các câu tự kiểm tra và đọc bảng "Hiểu lầm thường gặp".

## Ba câu cần nói được khi bảo vệ

1. *"Đề tài giữ nguyên YOLO26s-seg, chỉ thay khối attention C2PSA ở layer 10 bằng khối C2TSVMamba, gồm nhánh VMamba quét 4 hướng để lấy ngữ cảnh toàn cục và nhánh trích đặc trưng hình dạng/biên có hướng dùng để điều biến."*
2. *"Dữ liệu là Kvasir-SEG cộng 200 ảnh nền nhãn rỗng (BG20). Mask được chuyển sang polygon YOLO bằng Otsu, Closing, contour và approxPolyDP. Tập train có 1.040 ảnh, tập val có 160 ảnh."*
3. *"Trên 10 seed, Mask mAP@50-95 của TSVM là 0.7246 ± 0.0078, của baseline là 0.7210 ± 0.0129. TSVM ổn định hơn, nhưng chênh lệch chưa có ý nghĩa thống kê (p = 0.3839)."*

## Ký hiệu độ tin cậy dùng trong tài liệu

- ✅ **Đã xác nhận:** đọc trực tiếp trong code, config, CSV hoặc dữ liệu của repo.
- 📘 **Kiến thức chung:** lý thuyết phổ biến trong ngành.
- ⚠️ **Chưa xác minh:** chưa có bằng chứng trong repo, cần kiểm tra trước khi đưa vào khóa luận.
