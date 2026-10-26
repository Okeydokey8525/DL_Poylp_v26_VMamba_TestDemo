# Khóa luận: Tích hợp VMamba vào YOLO26-seg để phân đoạn polyp

**Đề tài:** Nghiên cứu phương pháp tích hợp VMamba vào YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng.
**Trọng tâm hiện tại (26/10/2026):** so sánh YOLO26s-seg (Baseline) với YOLO26s-seg + C2TSVMamba (TSVM FP32), mỗi mô hình 20 seed, trên dữ liệu BG20.

## Bắt đầu đọc từ đây

→ **[00_tai_lieu_tong_quan/00_README.md](00_tai_lieu_tong_quan/00_README.md)**: tóm tắt một trang và mục lục 13 chương. Mọi con số trong đó được tính lại từ dữ liệu gốc.

## Kết quả chính

| | Baseline | TSVM FP32 |
|---|---:|---:|
| Mask mAP50–95 (20 seed) | 0,7189 ± 0,0118 | 0,7232 ± 0,0072 |
| Δ, p | | +0,0043, paired t p = 0,061 (chưa có ý nghĩa thống kê ở α = 0,05) |
| Tham số | 11,43 M | 12,25 M |
| Độ trễ CPU (forward) | 270 ms | 577 ms |

## Cây thư mục

| Thư mục | Nội dung |
|---|---|
| [00_tai_lieu_tong_quan/](00_tai_lieu_tong_quan/00_README.md) | Bộ tài liệu tổng quan, script tính lại số liệu, bảng kết quả |
| `01_du_lieu/` | Dữ liệu BG20 (1.200 ảnh), split 880/120, script tạo dữ liệu |
| `02_ma_nguon/` | Fork Ultralytics 8.4.127 + TSVM + bản vá FP32, notebook Kaggle |
| `03_ket_qua_huan_luyen/` | 40 lượt huấn luyện chính: Baseline và TSVM FP32, seed 0–19 |
| `04_phan_tich_20seed/` | Gói phân tích 20 seed: CSV, thống kê, hình, benchmark hiệu năng |
| `05_so_sanh_mo_hinh_khac/` | PraNet, U-Net (để so sánh, hiện mới có checkpoint) |
| `06_bao_cao/` | Báo cáo Word/PDF khóa luận và biểu mẫu |
| `07_kiem_toan_va_sua/` | Kiểm toán ngày 25/10 và sửa lỗi ngày 26/10 |
| `99_luu_tru/` | Lịch sử và thử nghiệm không thuộc bộ chính (TSVM cũ, AV/AVF/ITSVM, 10 seed, tài liệu cũ…) |

Chi tiết từng thư mục: [00_tai_lieu_tong_quan/13_BAN_DO_THU_MUC.md](00_tai_lieu_tong_quan/13_BAN_DO_THU_MUC.md).

## Sắp xếp lại ngày 26/10/2026

Repo trước đây để mọi thứ trong `archive/`. Ngày 26/10/2026 toàn bộ được chuyển sang cây trên, chỉ di chuyển và đổi tên, không xóa hay sửa nội dung. Muốn tra một đường dẫn cũ (ví dụ trong script hoặc tài liệu cũ) đã chuyển đi đâu, xem [PATH_MAP.md](PATH_MAP.md).

## Lưu ý

Dự án phục vụ học tập và nghiên cứu. Kết quả phân đoạn không thay thế chẩn đoán y khoa.
