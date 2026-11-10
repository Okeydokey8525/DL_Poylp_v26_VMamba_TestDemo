# Tài liệu tổng quan: YOLO26s-seg (mô hình gốc) và YOLO26s-seg + C2TSVMamba (TSVM FP32)

Bộ tài liệu cho phần trọng tâm của khóa luận CNTT_KLCN182: **so sánh YOLO26s-seg với YOLO26s-seg + C2TSVMamba trên dữ liệu BG20**, kèm hai mô hình đối chiếu PraNet, U-Net và các thí nghiệm bổ sung.

> **Cập nhật 10/11/2026 (bản nộp):** mọi số ở đây khớp bản Word cuối `06_bao_cao/CNTT_KLCN182-PhungTheBao.docx`. Báo cáo dùng **20 seed (seed 0–19)**. PraNet và U-Net là bản **ảnh 640×640, có tăng cường dữ liệu** (bảng ở `bang/pixel_640/`). Ablation và C2PSA rộng là bản **20 seed** (`bang/ablation_20seed/`).

- Mọi con số được **tính lại từ dữ liệu gốc** (`results.csv`, `args.yaml`, `best.pt`, checkpoint `.pth`, thư mục ảnh) bằng các script trong [scripts/](scripts/).
- Số thập phân trong tài liệu dùng dấu phẩy. Các file CSV trong `bang/` dùng dấu chấm.

## Tóm tắt một trang (20 seed, seed 0–19)

| | YOLO26s-seg | + TSVM FP32 |
|---|---:|---:|
| Thay đổi kiến trúc | Tầng 10 là `C2PSA` | Tầng 10 là `C2TSVMamba` (SS2D 4 hướng + nhánh hình dạng/hướng + cổng) |
| Tham số | 11.434.463 | 12.254.688 (+7,17%) |
| **Mask mAP50–95** (20 seed, epoch cực đại) | **0,7189 ± 0,0118** | **0,7232 ± 0,0072** |
| Δ, KTC 95%, p | | +0,0043, [−0,0002; 0,0088], paired t p = 0,061 (Wilcoxon 0,070) |
| Số seed TSVM cao hơn | | 13/20 |
| Độ ổn định (Levene, thăm dò) | | SD nhỏ hơn khoảng 39%, p = 0,026 |
| Mask mAP50 | 0,9069 | 0,9083 (+0,0014; p = 0,668) |
| Mask Precision / Recall | 0,904 / 0,859 | 0,914 / 0,859 |
| TP / FP / FN (trên 127 polyp) | 110,55 / 16,45 / 16,45 | 110,65 / 15,75 / 16,35 |
| Độ trễ CPU (forward) | 270 ms | 577 ms (khoảng 2,1 lần) |
| Độ trễ GPU (forward, trung vị) | 26,33 ms | 39,86 ms (chỉ dùng tỉ lệ khoảng 1,5 lần) |
| Độ trễ đầu-cuối qua web, CPU / GPU (trung vị) | 198,94 / 45,79 ms | 422,14 / 49,52 ms |
| Thời gian huấn luyện 100 epoch (Kaggle) | khoảng 2,3 giờ | khoảng 4,7 giờ |

**Kết luận ngắn:**
- Trên 20 seed, TSVM có mask mAP50–95 trung bình cao hơn 0,0043 nhưng **không có ý nghĩa thống kê** (p = 0,061): chỉ là **xu hướng** tăng nhỏ. TSVM dao động ít hơn giữa các seed (Levene p = 0,026, thăm dò). TSVM chạy chậm khoảng gấp đôi trên CPU.
- **Ablation 20 seed** ([15](15_ABLATION_VA_C2PSA_RONG.md)): ba biến thể bỏ bớt thành phần đều thấp hơn bản đầy đủ nhưng không có ý nghĩa thống kê. **C2PSA rộng** (cùng số tham số) thấp hơn TSVM 0,0070 (KTC 95% [0,0038; 0,0101], TSVM cao hơn ở 17/20 seed) và không hơn mô hình gốc (p = 0,31).
- **Theo pixel** ([10](10_SO_SANH_PRANET_UNET.md)): Dice TSVM 0,8540 so với 0,8486 của mô hình gốc (p = 0,26). **PraNet 640 cao hơn cả hai mô hình YOLO** ở mọi độ đo (Dice 0,8856; hơn TSVM 0,0316, p < 0,001); U-Net 640 thấp nhất (Dice 0,6909). TSVM báo nhầm ảnh nền 1,5%, PraNet 2,8%, U-Net 57,4%.
- **Topology** ([14](14_CHI_SO_TOPOLOGY.md)): TSVM chỉ nhích hơn mô hình gốc (80,8% so với 79,7% ảnh đúng topology), không có ý nghĩa thống kê, và kém PraNet 640 rõ rệt (87,7%).
- **Dữ liệu ngoài** (`08_du_lieu_thuc_te/`): TSVM không tốt hơn mô hình gốc về Dice, thấp hơn có ý nghĩa thống kê trên CVC-ClinicDB và CVC-ColonDB, ngang nhau trên ETIS-Larib và PolypGen. Trên 125 ảnh không có polyp của PolypGen, TSVM báo nhầm ít hơn (10,8% so với 13,3%). Trên 800 ảnh manh tràng chưa dùng, hai mô hình YOLO báo nhầm như nhau (1,3% và 1,4%).

## Mục lục (đọc theo thứ tự)

| # | File | Nội dung |
|---|---|---|
| 01 | [Đề tài và phạm vi](01_DE_TAI_VA_PHAM_VI.md) | Mục tiêu, câu hỏi nghiên cứu, phạm vi |
| 02 | [Dữ liệu BG20](02_DU_LIEU_BG20.md) | 1.200 ảnh, split 1.040/160, 127 polyp ở validation, cách tạo, kiểm tra |
| 03 | [Kiến trúc mô hình gốc](03_KIEN_TRUC_BASELINE.md) | Bảng 24 tầng YOLO26s-seg đo kích thước thực tế |
| 04 | [Kiến trúc TSVM FP32](04_KIEN_TRUC_TSVM_FP32.md) | C2TSVMamba: SS2D, các nhánh, công thức, tham số từng phần, khởi tạo |
| 05 | [Cấu hình huấn luyện](05_CAU_HINH_HUAN_LUYEN.md) | Siêu tham số, quy trình Kaggle, ý nghĩa của "FP32" |
| **06** | [**Kết quả 20 seed**](06_KET_QUA_20_SEED.md) | **Bộ số chính của báo cáo** (mAP theo mặt nạ) |
| 07 | [Hội tụ và loss](07_HOI_TU_VA_LOSS.md) | Đường cong theo epoch, close_mosaic, các thành phần loss |
| 08 | [Ma trận nhầm lẫn](08_MA_TRAN_NHAM_LAN.md) | TP/FP/FN theo đối tượng, vì sao TN là N/A |
| 09 | [Chi phí tính toán](09_HIEU_NANG_TINH_TOAN.md) | Tham số, GFLOPs, độ trễ CPU/GPU, giới hạn của phép đo |
| 10 | [So sánh PraNet, U-Net](10_SO_SANH_PRANET_UNET.md) | Dice/IoU/P/R theo pixel của 4 mô hình × 20 seed (PraNet/U-Net 640) |
| 11 | [Giới hạn và hướng phát triển](11_GIOI_HAN_VA_HUONG_PHAT_TRIEN.md) | Được viết gì, không được viết gì, việc tiếp theo |
| 12 | [Truy vết số liệu](12_TRUY_VET_SO_LIEU.md) | Script, các bảng `bang/`, đối chiếu |
| 13 | [Bản đồ thư mục](13_BAN_DO_THU_MUC.md) | Thư mục nào chứa gì |
| 14 | [Chỉ số topology](14_CHI_SO_TOPOLOGY.md) | Lỗi Betti (số mảnh, số lỗ) của 4 mô hình × 20 seed |
| 15 | [Ablation và C2PSA rộng](15_ABLATION_VA_C2PSA_RONG.md) | Ba biến thể tách thành phần và đối chứng cùng số tham số, 20 seed |

## Cấu trúc thư mục

```
00_tai_lieu_tong_quan/
├── 00_README.md … 15_ABLATION_VA_C2PSA_RONG.md
├── scripts/            tinh_lai_so_lieu.py, danh_gia_pixel.py, danh_gia_topology.py, do_flops_gpu.py,
│                       do_tre_end_to_end.py, tinh_ablation.py, tinh_c2psa_rong.py, tinh_ma_tran_anh.py,
│                       xuat_chi_so_web.py (chỉ đọc dữ liệu gốc, ghi vào bang/)
└── bang/
    ├── 00–09_*.csv     dữ liệu, kết quả 20 seed theo mặt nạ, cấu hình, ma trận nhầm lẫn, checkpoint
    ├── 16_*, 19_*      FLOPs, độ trễ GPU, độ trễ đầu-cuối
    ├── pixel_640/      10–15, 20, 20b: pixel, topology, ma trận theo ảnh của 4 mô hình; du_lieu_ngoai/, nen_cecum/
    └── ablation_20seed/ 17–19: ablation và C2PSA rộng
```

## Các mức xác minh dùng trong tài liệu

- **Đã tính lại hoặc đã kiểm tra:** con số do script sinh ra từ dữ liệu gốc, hoặc đã so trực tiếp với dữ liệu gốc.
- **Lấy từ nguồn có sẵn:** dẫn từ file có sẵn trong repo, có ghi rõ phần nào đã kiểm tra ([12](12_TRUY_VET_SO_LIEU.md)).
- **Chưa xác minh / chưa có:** ghi rõ, không suy diễn.
