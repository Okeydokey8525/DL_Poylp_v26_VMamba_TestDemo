# Khóa luận: Tích hợp VMamba vào YOLO26-seg để phân đoạn polyp

**Đề tài:** Nghiên cứu phương pháp tích hợp VMamba vào YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng (HUIT, CNTT_KLCN182).

**Trọng tâm (cập nhật 29/10/2026):** so sánh YOLO26s-seg (Baseline) với YOLO26s-seg + C2TSVMamba (TSVM FP32) trên dữ liệu BG20. Báo cáo dùng **20 seed (0–19)** cho mỗi mô hình. PraNet và U-Net dùng để so sánh. Ablation dùng seed 0–4 (15 lượt, mục 6.6): bỏ bất kỳ thành phần nào cũng làm trung bình thấp hơn bản đầy đủ, nhưng không có ý nghĩa thống kê.

## Bắt đầu đọc từ đây

- **[NGU_CANH_DU_AN.md](NGU_CANH_DU_AN.md):** ngữ cảnh, kết quả đã xác minh, trạng thái báo cáo và việc còn lại.
- **[00_tai_lieu_tong_quan/00_README.md](00_tai_lieu_tong_quan/00_README.md):** tóm tắt một trang và mục lục các file tổng quan. Mọi con số trong đó được tính lại từ dữ liệu gốc.
- Hướng dẫn cho AI:
  - [CLAUDE.md](CLAUDE.md) (Claude Code);
  - [AGENTS.md](AGENTS.md) (Codex và các agent khác);
  - [HUONG_DAN_LAM_VIEC_VOI_CLAUDE.md](HUONG_DAN_LAM_VIEC_VOI_CLAUDE.md) (cách làm việc và lịch sử).

## Kết quả chính (20 seed)

| | Baseline | TSVM FP32 |
|---|---:|---:|
| Mask mAP50–95 | 0,7189 ± 0,0118 | 0,7232 ± 0,0072 |
| Δ, p | | +0,0043, paired t p = 0,061, 13/20 seed (chưa có ý nghĩa thống kê ở α = 0,05) |
| Dice theo pixel | 0,849 | 0,854 (p = 0,26) |
| Tham số | 11,43 M | 12,25 M |
| Độ trễ CPU (chỉ forward) | 270 ms | 577 ms |
| Độ trễ GPU | | chậm hơn khoảng 1,5–1,7 lần |

Trên dữ liệu ngoài (CVC-ClinicDB, CVC-ColonDB, ETIS, PolypGen), TSVM không tốt hơn Baseline về Dice. Trên ClinicDB và ColonDB, TSVM kém hơn có ý nghĩa thống kê. Riêng trên ảnh không có polyp của PolypGen, TSVM báo nhầm ít hơn Baseline (p = 0,011). Chi tiết ở [08_du_lieu_thuc_te/](08_du_lieu_thuc_te/README.md).

## Cây thư mục

| Thư mục | Nội dung |
|---|---|
| [00_tai_lieu_tong_quan/](00_tai_lieu_tong_quan/00_README.md) | Bộ tài liệu tổng quan, script tính lại số liệu, bảng kết quả |
| `01_du_lieu/` | Dữ liệu BG20 (1.200 ảnh), split 880/120 do tác giả Kvasir-SEG cung cấp, script tạo dữ liệu |
| `02_ma_nguon/` | Fork Ultralytics 8.4.127 + TSVM + bản vá FP32, notebook Kaggle (kể cả ablation) |
| `03_ket_qua_huan_luyen/` | 40 lượt chính (Baseline và TSVM FP32, seed 0–19) và các lượt ablation (`Vmamba_only/`, `Shape_only/`) |
| `04_phan_tich_20seed/` | Gói phân tích 20 seed cũ và benchmark hiệu năng CPU |
| `05_so_sanh_mo_hinh_khac/` | Checkpoint PraNet, U-Net (20 seed mỗi mô hình) |
| `06_bao_cao/` | Chương báo cáo markdown (`md_bao_cao/`), hình (`hinh/`), kế hoạch slide (`slide/`), Word và biểu mẫu |
| `07_kiem_toan_va_sua/` | Kiểm toán ngày 25/10 và sửa lỗi ngày 26/10 |
| `08_du_lieu_thuc_te/` | Đánh giá trên 4 bộ dữ liệu ngoài |
| `99_luu_tru/` | Lịch sử và thử nghiệm không thuộc bộ chính (TSVM cũ, AV/AVF/ITSVM, tài liệu cũ…) |

Chi tiết từng thư mục: [00_tai_lieu_tong_quan/13_BAN_DO_THU_MUC.md](00_tai_lieu_tong_quan/13_BAN_DO_THU_MUC.md).

## Sắp xếp lại ngày 26/10/2026

Repo trước đây để mọi thứ trong `archive/`. Ngày 26/10/2026 toàn bộ được chuyển sang cây thư mục trên. Việc này chỉ di chuyển và đổi tên, không xóa hay sửa nội dung. Muốn tra một đường dẫn cũ đã chuyển đi đâu, xem [PATH_MAP.md](PATH_MAP.md).

## Lưu ý

Dự án phục vụ học tập và nghiên cứu. Kết quả phân đoạn không thay thế chẩn đoán y khoa.
