# PHỤ LỤC

> **Ghi chú soạn thảo (xóa khi ghép Word):**
> - Các bảng PL.1–PL.3 được sinh tự động từ CSV trong `00_tai_lieu_tong_quan/bang/` (đã đối chiếu với Chương 6), không gõ tay. Nếu tính lại số liệu thì sinh lại bảng.
> - Phụ lục không trích tài liệu tham khảo mới.

## Phụ lục A. Kết quả từng seed

### A.1. Mô hình gốc và mô hình đề xuất (20 seed)

Mỗi lượt lấy tại epoch đầu tiên đạt mask mAP50–95 cao nhất. P, R là Precision và Recall của mặt nạ tại cùng epoch. Cột "epoch" là epoch được chọn.

*Bảng PL.1. Chỉ số mặt nạ của từng seed trên tập kiểm định*

| Seed | Gốc: mAP50–95 | Gốc: mAP50 | Gốc: P | Gốc: R | Gốc: epoch | TSVM: mAP50–95 | TSVM: mAP50 | TSVM: P | TSVM: R | TSVM: epoch | Δ mAP50–95 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0,7366 | 0,9136 | 0,9535 | 0,8189 | 89 | 0,7245 | 0,9040 | 0,9312 | 0,8529 | 88 | −0,0121 |
| 1 | 0,7165 | 0,8952 | 0,8533 | 0,8504 | 98 | 0,7274 | 0,9115 | 0,9437 | 0,8661 | 98 | +0,0109 |
| 2 | 0,7138 | 0,9072 | 0,9139 | 0,8355 | 100 | 0,7259 | 0,9003 | 0,9220 | 0,8377 | 83 | +0,0121 |
| 3 | 0,6941 | 0,9052 | 0,8786 | 0,8545 | 61 | 0,7213 | 0,9164 | 0,9188 | 0,8909 | 89 | +0,0272 |
| 4 | 0,7274 | 0,9062 | 0,9387 | 0,8819 | 99 | 0,7197 | 0,9024 | 0,9018 | 0,8676 | 97 | −0,0077 |
| 5 | 0,7350 | 0,9264 | 0,9318 | 0,8605 | 94 | 0,7285 | 0,9096 | 0,9013 | 0,8819 | 90 | −0,0066 |
| 6 | 0,7153 | 0,9080 | 0,8865 | 0,8611 | 81 | 0,7254 | 0,9006 | 0,9223 | 0,8504 | 95 | +0,0101 |
| 7 | 0,7145 | 0,9154 | 0,8983 | 0,8347 | 71 | 0,7065 | 0,8903 | 0,8595 | 0,8425 | 88 | −0,0080 |
| 8 | 0,7318 | 0,9319 | 0,9114 | 0,8912 | 96 | 0,7339 | 0,9103 | 0,8883 | 0,8768 | 93 | +0,0021 |
| 9 | 0,7253 | 0,9097 | 0,8568 | 0,8949 | 84 | 0,7329 | 0,9166 | 0,9288 | 0,8583 | 96 | +0,0076 |
| 10 | 0,7045 | 0,8811 | 0,8780 | 0,8661 | 82 | 0,7198 | 0,9103 | 0,9542 | 0,8425 | 100 | +0,0153 |
| 11 | 0,7299 | 0,9091 | 0,9253 | 0,8783 | 99 | 0,7226 | 0,9097 | 0,9168 | 0,8661 | 87 | −0,0072 |
| 12 | 0,7056 | 0,8828 | 0,9019 | 0,8347 | 87 | 0,7157 | 0,9031 | 0,9162 | 0,8583 | 89 | +0,0101 |
| 13 | 0,7315 | 0,9109 | 0,9348 | 0,8347 | 97 | 0,7306 | 0,9250 | 0,8926 | 0,8819 | 99 | −0,0009 |
| 14 | 0,7223 | 0,9072 | 0,9014 | 0,8637 | 74 | 0,7211 | 0,9064 | 0,9231 | 0,8500 | 96 | −0,0012 |
| 15 | 0,7176 | 0,9040 | 0,9171 | 0,8713 | 80 | 0,7262 | 0,9100 | 0,9347 | 0,8425 | 84 | +0,0086 |
| 16 | 0,7125 | 0,8965 | 0,9213 | 0,8425 | 96 | 0,7237 | 0,9121 | 0,9027 | 0,8763 | 93 | +0,0113 |
| 17 | 0,7274 | 0,9227 | 0,8615 | 0,9134 | 73 | 0,7301 | 0,9219 | 0,9147 | 0,8740 | 100 | +0,0027 |
| 18 | 0,7022 | 0,9004 | 0,8875 | 0,8583 | 94 | 0,7082 | 0,8935 | 0,8762 | 0,8361 | 47 | +0,0060 |
| 19 | 0,7136 | 0,9045 | 0,9303 | 0,8408 | 71 | 0,7195 | 0,9113 | 0,9403 | 0,8268 | 91 | +0,0059 |
| **TB ± SD** | 0,7189 ± 0,0118 | 0,9069 | 0,9041 | 0,8594 | | 0,7232 ± 0,0072 | 0,9083 | 0,9145 | 0,8590 | | +0,0043 |

*Nguồn: `bang/02_ket_qua_tung_seed.csv`. Dòng cuối là trung bình qua 20 seed; với mAP50–95 có kèm độ lệch chuẩn.*

### A.2. Dice theo pixel của bốn mô hình (20 seed)

*Bảng PL.2. Dice theo pixel trên 120 ảnh có polyp của tập kiểm định*

| Seed | YOLO26s-seg | TSVM | PraNet | U-Net |
|---:|---:|---:|---:|---:|
| 0 | 0,8727 | 0,8366 | 0,8547 | 0,7182 |
| 1 | 0,8624 | 0,8659 | 0,8635 | 0,7172 |
| 2 | 0,8394 | 0,8554 | 0,8619 | 0,6914 |
| 3 | 0,8232 | 0,8580 | 0,8475 | 0,7092 |
| 4 | 0,8736 | 0,8529 | 0,8431 | 0,6857 |
| 5 | 0,8468 | 0,8712 | 0,8503 | 0,6696 |
| 6 | 0,8632 | 0,8349 | 0,8534 | 0,6844 |
| 7 | 0,8223 | 0,8293 | 0,8515 | 0,7313 |
| 8 | 0,8748 | 0,8552 | 0,8504 | 0,7080 |
| 9 | 0,8254 | 0,8636 | 0,8549 | 0,7322 |
| 10 | 0,8540 | 0,8647 | 0,8372 | 0,7255 |
| 11 | 0,8601 | 0,8715 | 0,8519 | 0,7446 |
| 12 | 0,8448 | 0,8656 | 0,8560 | 0,6898 |
| 13 | 0,8525 | 0,8651 | 0,8559 | 0,7413 |
| 14 | 0,8453 | 0,8421 | 0,8561 | 0,7092 |
| 15 | 0,8469 | 0,8372 | 0,8677 | 0,7039 |
| 16 | 0,8259 | 0,8562 | 0,8555 | 0,7367 |
| 17 | 0,8557 | 0,8636 | 0,8609 | 0,6861 |
| 18 | 0,8274 | 0,8443 | 0,8547 | 0,7236 |
| 19 | 0,8553 | 0,8468 | 0,8544 | 0,6852 |
| **TB ± SD** | 0,8486 ± 0,0171 | 0,8540 ± 0,0129 | 0,8541 ± 0,0068 | 0,7097 ± 0,0221 |

*Nguồn: `bang/11_pixel_tung_seed.csv`. Dice là trung bình theo ảnh; ảnh bị bỏ sót hoàn toàn có Dice bằng 0.*

### A.3. Thí nghiệm tách thành phần (5 seed)

*Bảng PL.3. Mask mAP50–95 từng seed của năm cấu hình*

| Seed | Gốc (C2PSA) | TSVM đầy đủ | `vmamba_only` | `shape_only` | `shape_vmamba_no_guidance` |
|---:|---:|---:|---:|---:|---:|
| 0 | 0,7366 | 0,7245 | 0,7145 | 0,7107 | 0,7160 |
| 1 | 0,7165 | 0,7274 | 0,7389 | 0,7091 | 0,7275 |
| 2 | 0,7138 | 0,7259 | 0,7145 | 0,7049 | 0,7209 |
| 3 | 0,6941 | 0,7213 | 0,7115 | 0,7296 | 0,7172 |
| 4 | 0,7274 | 0,7197 | 0,7054 | 0,7095 | 0,7193 |
| **TB ± SD** | 0,7177 ± 0,0160 | 0,7238 ± 0,0032 | 0,7170 ± 0,0128 | 0,7128 ± 0,0097 | 0,7201 ± 0,0045 |
| Giờ huấn luyện TB | 2,32 | 4,61 | 4,58 | 2,41 | 4,62 |

*Nguồn: `bang/17_ablation_tung_seed.csv`. Hai cột đầu là seed 0–4 của các lượt chính.*

## Phụ lục B. Cấu hình huấn luyện

Hai mô hình YOLO, cùng ba biến thể tách thành phần, dùng chung toàn bộ siêu tham số dưới đây. Chúng chỉ khác nhau ở tệp cấu hình mô hình (`model`). Mô hình gốc khởi tạo trực tiếp từ `yolo26s-seg.pt`. Mô hình đề xuất và các biến thể được dựng từ tệp YAML rồi nạp trọng số từ cùng tệp này, chỉ ở các tầng trùng tên và trùng kích thước (mục 3.5).

*Bảng PL.4. Siêu tham số huấn luyện (theo `args.yaml` của 40 lượt chính)*

| Nhóm | Tham số | Giá trị |
|---|---|---|
| Chung | `epochs`, `batch`, `imgsz` | 100; 8; 640 |
| | `workers`, `device` | 2; GPU 0 |
| | `patience` | 100 (không dừng sớm) |
| | `amp` | False (huấn luyện FP32) |
| | `deterministic` | True |
| | `seed` | 0–19 (lượt chính), 0–4 (tách thành phần) |
| Tối ưu | `optimizer` | AdamW |
| | `lr0`, `lrf` | 0,001; 0,01 |
| | `momentum`, `weight_decay` | 0,937; 0,0005 |
| | `warmup_epochs`, `cos_lr` | 5; False |
| Tăng cường dữ liệu | `mosaic`, `close_mosaic` | 1,0; tắt ở 10 epoch cuối |
| | `mixup` | 0 |
| | `fliplr`, `flipud`, `degrees` | 0,5; 0; 0 |
| | `scale`, `translate` | 0,5; 0,1 |
| | `hsv_h`, `hsv_s`, `hsv_v` | 0,015; 0,7; 0,4 |
| Phân đoạn và đánh giá | `overlap_mask`, `mask_ratio` | True; 4 |
| | `iou`, `max_det` | 0,7; 300 |
| | `rect`, `cache` | False; False |

*Nguồn: `bang/03_cau_hinh_args.csv` (40 lượt chính, mọi tham số giống nhau giữa hai mô hình trừ `model` và `pretrained`) và `bang/18_ablation_cau_hinh_args.csv` (15 lượt tách thành phần, không khác lượt TSVM cùng seed).*

## Phụ lục C. Tổ chức mã nguồn và tệp kết quả

*Bảng PL.5. Các thư mục chính của kho mã*

| Thư mục | Nội dung |
|---|---|
| `01_du_lieu/` | Bộ BG20 ở định dạng YOLO, danh sách chia `train.txt`/`val.txt`, script tiền xử lý |
| `02_ma_nguon/ultralytics_TSVM_FP32/` | Ultralytics 8.4.127 có thêm khối C2TSVMamba (`nn/modules/topology_shape_vmamba.py`) và bản vá lưu checkpoint FP32 |
| `02_ma_nguon/notebook_kaggle/` | Notebook huấn luyện trên Kaggle, gồm cả notebook tách thành phần |
| `03_ket_qua_huan_luyen/` | 40 lượt chính và 15 lượt tách thành phần; mỗi lượt có `args.yaml`, `results.csv`, `weights/` |
| `05_so_sanh_mo_hinh_khac/` | Trọng số PraNet và U-Net (20 seed mỗi mô hình) |
| `00_tai_lieu_tong_quan/scripts/` | Script tính lại số liệu, đánh giá theo pixel, topology, FLOPs và độ trễ GPU, tách thành phần |
| `00_tai_lieu_tong_quan/bang/` | Các bảng CSV kết quả dùng trong báo cáo |
| `08_du_lieu_thuc_te/` | Script và kết quả đánh giá trên bốn bộ dữ liệu ngoài |
| `06_bao_cao/hinh/` | Hình của báo cáo và script vẽ hình |

*Bảng PL.6. Script tạo ra số liệu trong báo cáo*

| Script | Đầu vào | Đầu ra | Dùng ở |
|---|---|---|---|
| `tinh_lai_so_lieu.py` | `results.csv`, `args.yaml`, ảnh dữ liệu | `bang/01–09_*.csv` | Ch.4, Ch.6 (mục 6.2) |
| `danh_gia_pixel.py` | Checkpoint 4 mô hình × 20 seed, 160 ảnh kiểm định | `bang/10–12_*.csv` | Ch.6 (mục 6.3) |
| `danh_gia_topology.py` | Như trên | `bang/13–15_*.csv` | Ch.6 (mục 6.4) |
| `do_flops_gpu.py` | Checkpoint seed 0 của hai mô hình | `bang/16*_*.csv` | Ch.6 (mục 6.5) |
| `tinh_ablation.py` | `results.csv`, `args.yaml`, `best.pt` của 25 lượt | `bang/17*_*.csv`, `bang/18_*.csv` | Ch.6 (mục 6.6) |
| `08_du_lieu_thuc_te/scripts/` | Checkpoint 4 mô hình × 20 seed, 4 bộ dữ liệu ngoài | `08_du_lieu_thuc_te/bang/20seed/*.csv` | Ch.6 (mục 6.7) |
| `ve_hinh.py`, `ve_so_do.py` | Các bảng CSV | Hình PNG 300 dpi và PDF | Toàn báo cáo |

## Phụ lục D. Hướng dẫn chạy lại

Các lệnh chạy từ thư mục gốc của kho mã. Script chỉ đọc dữ liệu và kết quả huấn luyện, chỉ ghi vào thư mục `bang/` và `hinh/`. Các bước cần GPU dùng môi trường Python có PyTorch hỗ trợ CUDA.

```
# 1. Tính lại số liệu tổng hợp từ 40 lượt chính
python 00_tai_lieu_tong_quan/scripts/tinh_lai_so_lieu.py

# 2. Đánh giá theo pixel và topology của 4 mô hình (cần GPU)
python 00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py
python 00_tai_lieu_tong_quan/scripts/danh_gia_topology.py

# 3. FLOPs và độ trễ GPU (cần GPU)
python 00_tai_lieu_tong_quan/scripts/do_flops_gpu.py

# 4. Tách thành phần, có đếm tham số từ checkpoint (cần PyTorch)
python 00_tai_lieu_tong_quan/scripts/tinh_ablation.py --torch

# 5. Vẽ lại toàn bộ hình
python 06_bao_cao/hinh/scripts/ve_hinh.py
```

Để huấn luyện lại một lượt, mở notebook trong `02_ma_nguon/notebook_kaggle/` trên Kaggle (GPU), đặt seed và tệp cấu hình mô hình cần chạy, rồi tải thư mục kết quả về `03_ket_qua_huan_luyen/`. Notebook đặt `deterministic=True` và khóa seed cho mọi thư viện. Trong đề tài, lượt `shape_only` seed 3 và seed 4 mỗi lượt có hai bản kết quả với thời gian huấn luyện khác nhau. Hai bản `results.csv` giống hệt nhau ở mọi cột chỉ số qua cả 100 epoch, cho thấy với cùng phiên bản thư viện và cùng loại GPU, kết quả lặp lại được.
