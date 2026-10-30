# Tài liệu tổng quan: YOLO26s-seg (Baseline) và TSVM FP32

Bộ tài liệu được viết mới ngày 26/10/2026 cho phần trọng tâm của khóa luận: **so sánh YOLO26s-seg với YOLO26s-seg + C2TSVMamba (TSVM FP32) trên dữ liệu BG20.**

> **Cập nhật 28/10/2026:** chủ dự án **chốt dùng 20 seed (seed 0–19)** cho báo cáo. Các file 06–11 bên dưới (số 20 seed, `bang/*.csv`, hình `06_bao_cao/hinh/ket_qua_20seed/`) là bộ số chính. Bộ 10 seed ([06b_KET_QUA_10_SEED.md](06b_KET_QUA_10_SEED.md), `bang/10seed/`, `hinh/ket_qua_10seed/`) chỉ giữ để đối chiếu.

- Bộ này không chép lại tài liệu cũ. Mọi con số được **tính lại từ dữ liệu gốc** (`results.csv`, `args.yaml`, `best.pt`, mã nguồn, thư mục ảnh) bằng [scripts/tinh_lai_so_lieu.py](scripts/tinh_lai_so_lieu.py) (`--seeds 10` cho bộ 10 seed đối chiếu). Tài liệu cũ chỉ dùng để đối chiếu.
- Số thập phân dùng dấu phẩy. Các file CSV trong `bang/` dùng dấu chấm.

## Tóm tắt một trang (20 seed, seed 0–19)

| | Baseline | TSVM FP32 |
|---|---:|---:|
| Thay đổi kiến trúc | Tầng 10 là `C2PSA` | Tầng 10 là `C2TSVMamba` (SS2D 4 hướng + nhánh hình dạng/hướng + cổng) |
| Tham số | 11.434.463 | 12.254.688 (+7,17%) |
| **Mask mAP50–95** (20 seed, epoch cực đại) | **0,7189 ± 0,0118** | **0,7232 ± 0,0072** |
| Δ, CI 95%, p | | +0,0043, [−0,0002; 0,0088], paired t p = 0,061 (Wilcoxon 0,070) |
| Số seed TSVM tốt hơn | | 13/20 |
| Độ ổn định (Levene, thăm dò) | | SD nhỏ hơn khoảng 39%, p = 0,026 |
| Mask mAP50 | 0,9069 | 0,9083 (+0,0014; p = 0,668) |
| Mask Precision / Recall | 0,904 / 0,859 | 0,914 / 0,859 |
| TP / FP / FN (trên 127 polyp) | 110,55 / 16,45 / 16,45 | 110,65 / 15,75 / 16,35 |
| Độ trễ CPU (forward) | 270 ms | 577 ms (khoảng 2,1 lần) |
| Độ trễ GPU (forward, lần đo 2, trung vị) | 26,33 ms | 39,86 ms (tỉ lệ khoảng 1,5–1,7 lần; chỉ dùng tỉ lệ) |
| Thời gian huấn luyện 100 epoch (Kaggle) | khoảng 2,3 giờ | khoảng 4,6 giờ |

**Kết luận ngắn:** Trên 20 seed, TSVM có mask mAP50–95 trung bình cao hơn 0,0043 nhưng **chưa có ý nghĩa thống kê** (p = 0,061). TSVM dao động ít hơn giữa các seed (Levene p = 0,026, thăm dò). TSVM chạy chậm khoảng gấp đôi trên CPU. Theo pixel, Dice của TSVM là 0,854 so với 0,849 của đối chứng (p = 0,26), ngang PraNet (0,854) và hơn hẳn U-Net (0,710). Trên dữ liệu ngoài (`08_du_lieu_thuc_te/`), TSVM không tốt hơn đối chứng về Dice: kém hơn có ý nghĩa thống kê trên ClinicDB và ColonDB, không khác biệt có ý nghĩa trên ETIS và PolypGen. TSVM báo nhầm ít hơn trên ảnh không có polyp của PolypGen. Ablation (seed 0–4, `bang/17_*.csv`): cả ba biến thể bỏ bớt một thành phần đều thấp hơn bản đầy đủ (bỏ cổng −0,0036, chỉ SS2D −0,0068, chỉ nhánh hình dạng −0,0110), không chênh lệch nào có ý nghĩa thống kê.

Bộ 10 seed (chỉ đối chiếu): Δ = +0,0036, p = 0,384, 6/10 seed.

## Mục lục (đọc theo thứ tự)

| # | File | Nội dung |
|---|---|---|
| 01 | [Đề tài và phạm vi](01_DE_TAI_VA_PHAM_VI.md) | Mục tiêu, câu hỏi nghiên cứu, cái gì nằm trong và ngoài phạm vi |
| 02 | [Dữ liệu BG20](02_DU_LIEU_BG20.md) | 1.200 ảnh, split 1.040/160, 127 polyp ở validation, cách tạo, kiểm tra |
| 03 | [Kiến trúc Baseline](03_KIEN_TRUC_BASELINE.md) | Bảng 24 tầng YOLO26s-seg đo kích thước thực tế |
| 04 | [Kiến trúc TSVM FP32](04_KIEN_TRUC_TSVM_FP32.md) | C2TSVMamba: SS2D, các nhánh, công thức, tham số từng phần, khởi tạo |
| 05 | [Cấu hình huấn luyện](05_CAU_HINH_HUAN_LUYEN.md) | Siêu tham số, quy trình Kaggle, ý nghĩa của "FP32" |
| **06** | [**Kết quả 20 seed**](06_KET_QUA_20_SEED.md) | **Bộ số dùng cho báo cáo** |
| 06b | [Kết quả 10 seed](06b_KET_QUA_10_SEED.md) | Bộ 10 seed, chỉ giữ để đối chiếu |
| 07 | [Hội tụ và loss](07_HOI_TU_VA_LOSS.md) | Đường cong theo epoch, close_mosaic, các thành phần loss |
| 08 | [Ma trận nhầm lẫn](08_MA_TRAN_NHAM_LAN.md) | TP/FP/FN theo đối tượng, vì sao TN là N/A |
| 09 | [Chi phí tính toán](09_HIEU_NANG_TINH_TOAN.md) | Tham số, độ trễ CPU, giới hạn của phép đo |
| 10 | [So sánh PraNet, U-Net](10_SO_SANH_PRANET_UNET.md) | Dice/IoU/P/R theo pixel của 4 mô hình × 20 seed, giao thức và giới hạn |
| 11 | [Giới hạn và hướng phát triển](11_GIOI_HAN_VA_HUONG_PHAT_TRIEN.md) | Được viết gì, không được viết gì, việc tiếp theo |
| 14 | [Chỉ số topology](14_CHI_SO_TOPOLOGY.md) | Lỗi Betti (số mảnh, số lỗ) của 4 mô hình × 20 seed; TSVM không khác mô hình gốc có ý nghĩa |
| 12 | [Truy vết số liệu](12_TRUY_VET_SO_LIEU.md) | Script, các bảng `bang/`, đối chiếu, các điểm cần lưu ý ở tài liệu cũ |
| 13 | [Bản đồ thư mục](13_BAN_DO_THU_MUC.md) | File nào thuộc bộ chính, file nào là lịch sử |

## Cấu trúc thư mục

```
00_tai_lieu_tong_quan/
├── 00_README.md … 14_CHI_SO_TOPOLOGY.md
├── scripts/                        # tinh_lai_so_lieu.py, danh_gia_pixel.py, danh_gia_topology.py, do_flops_gpu.py
│                                   # chỉ đọc dữ liệu gốc, ghi vào bang/
└── bang/                           # CSV/JSON kết quả và log chạy
```

## Các mức xác minh dùng trong tài liệu

- **Đã tính lại hoặc đã kiểm tra:** con số do script sinh ra từ dữ liệu gốc, hoặc đã so trực tiếp với dữ liệu gốc.
- **Lấy từ nguồn có sẵn:** dẫn từ file có sẵn trong repo, có ghi rõ phần nào đã kiểm tra ([12](12_TRUY_VET_SO_LIEU.md)).
- **Chưa xác minh / chưa có:** ghi rõ, không suy diễn.
