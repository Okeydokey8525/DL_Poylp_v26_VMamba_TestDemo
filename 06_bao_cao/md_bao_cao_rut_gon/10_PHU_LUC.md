# PHỤ LỤC

> **Ghi chú soạn thảo (xóa khi ghép Word):**
> - Các bảng PL.1–PL.3 được sinh tự động từ CSV trong `00_tai_lieu_tong_quan/bang/` (đã đối chiếu với Chương 6), không gõ tay. Nếu tính lại số liệu thì sinh lại bảng.
> - Phụ lục không trích tài liệu tham khảo mới.
> - **Bản rút gọn:** Phụ lục E–H chứa phần chuyển khỏi thân: E phân công theo hạng mục (Bảng 0.3 cũ), F chi tiết khối C2TSVMamba (Ch.3), G API và lưu trữ của PolypVision (Ch.5), H kết quả thực nghiệm bổ sung (Ch.6). Số liệu chép nguyên từ bản đầy đủ.

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

Hai mô hình YOLO, cùng ba biến thể tách thành phần, dùng chung toàn bộ siêu tham số dưới đây. Chúng chỉ khác nhau ở tệp cấu hình mô hình (`model`). Mô hình gốc khởi tạo trực tiếp từ `yolo26s-seg.pt`. Mô hình đề xuất và các biến thể được dựng từ tệp YAML rồi nạp trọng số từ cùng tệp này, chỉ ở các tầng trùng tên và trùng kích thước (mục 3.5.1).

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

## Phụ lục E. Phân công theo hạng mục công việc

*Bảng PL.7. Phân công theo hạng mục công việc (C: chính, H: hỗ trợ)*

| Hạng mục | Lê Đức Lương | Phùng Tuấn Huy | Trần Mạnh Toàn |
|---|:---:|:---:|:---:|
| Khảo sát tài liệu, viết Chương 1 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Cơ sở lý thuyết, viết Chương 2 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Thu thập và tiền xử lý dữ liệu, viết Chương 4 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Thiết kế và cài đặt khối C2TSVMamba, viết Chương 3 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Huấn luyện Baseline và TSVM trên Kaggle | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Huấn luyện PraNet, U-Net | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Thí nghiệm tách thành phần (ablation) | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Phân tích thống kê, vẽ hình, viết Chương 6 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Dịch vụ suy luận FastAPI | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Website Spring Boot, MongoDB | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Ứng dụng di động Flutter | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Viết Chương 5 | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Mở đầu, Kết luận, định dạng báo cáo | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |
| Slide và chuẩn bị bảo vệ | [ĐIỀN] | [ĐIỀN] | [ĐIỀN] |

## Phụ lục F. Chi tiết khối C2TSVMamba

### F.1. Truy vết kích thước tensor

*Bảng PL.8. Kích thước tensor qua khối C2TSVMamba (một ảnh 640×640)*

| Bước | Phép toán | Kích thước ra |
|---|---|---|
| Vào tầng 10 | $x$ | 512×20×20 |
| cv1, chia đôi | Conv 1×1, split | $a$: 256×20×20; $b$: 256×20×20 |
| SS2D, bước 1–2 | in_proj, DWConv 3×3 | $U$, $Z$: 256×20×20 mỗi phần |
| SS2D, bước 3 | Trải phẳng | 4 chuỗi, mỗi chuỗi 256×400 |
| SS2D, bước 4 | x_proj, dt_proj | $\Delta$: 256×400; $B$, $C$: 16×400 (mỗi hướng) |
| SS2D, bước 5 | $\bar A$, $\Delta B u$, quét | 256×16×400 (đệm lên 512 khi quét) |
| SS2D, bước 5–7 | Đọc ra, gộp 4 hướng, cổng Z, out_proj | $F_M$: 256×20×20 |
| Nhánh hình dạng | (3.7)–(3.9) | $S$: 256×20×20 |
| Cổng, điều biến | (3.10) | $G$, $F'_M$: 256×20×20 |
| fuse, FFN, nối tắt | (3.11) | $b'$: 256×20×20 |
| Ghép, cv2 | Concat, Conv 1×1 | $y$: 512×20×20 |

![Hình PL.1](../hinh/chung/vi/m01_tham_so_tang10.png)

*Hình PL.1. Số tham số của từng thành phần trong khối C2TSVMamba. Tiêu đề hình ghi tổng của C2TSVMamba và của C2PSA để so sánh.*

### F.2. Ví dụ phép quét song song

Xét chuỗi $L = 4$ với $a = (0{,}5;\ 0{,}8;\ 0{,}5;\ 0{,}9)$ và $b = (1;\ 2;\ 0;\ 1)$. Tính tuần tự theo (3.13): $h_1 = 1$; $h_2 = 0{,}8 \cdot 1 + 2 = 2{,}8$; $h_3 = 0{,}5 \cdot 2{,}8 + 0 = 1{,}4$; $h_4 = 0{,}9 \cdot 1{,}4 + 1 = 2{,}26$. Thuật toán 3.1 ($K = 2$, không cần đệm) cho kết quả ở Bảng PL.9.

*Bảng PL.9. Các vòng của phép quét song song trên ví dụ*

| Vòng | Vị trí 1 | Vị trí 2 | Vị trí 3 | Vị trí 4 |
|---|---|---|---|---|
| Ban đầu $(a, b)$ | (0,5; 1) | (0,8; 2) | (0,5; 0) | (0,9; 1) |
| step = 1 | (0,5; 1) | (0,4; 0,8·1 + 2 = **2,8**) | (0,4; 0,5·2 + 0 = 1) | (0,45; 0,9·0 + 1 = 1) |
| step = 2 | (0,5; **1**) | (0,4; **2,8**) | (0,2; 0,4·1 + 1 = **1,4**) | (0,18; 0,45·2,8 + 1 = **2,26**) |

Sau vòng cuối, thành phần $b$ là $(1;\ 2{,}8;\ 1{,}4;\ 2{,}26)$, trùng với kết quả tính tuần tự. Ở vòng step = 2, vị trí 4 kết hợp cặp của vị trí 2 (đã chứa thông tin vị trí 1, 2) với cặp của chính nó (đã chứa vị trí 3, 4), nên chỉ sau hai vòng đã gom đủ bốn phần tử.

**Tổng khối lượng tính.** Vòng thứ $j$ xử lý $P - 2^{j}$ vị trí, nên tổng số phép kết hợp là $\sum_{j=0}^{K-1} (P - 2^{j}) = K\cdot P - (P - 1)$. Với $P = 512$, $K = 9$: mỗi chuỗi 4.097 phép kết hợp (tính tuần tự chỉ 399), mỗi ảnh có 16.384 chuỗi nên khoảng 67 triệu phép kết hợp, mỗi phép gồm hai phép nhân và một phép cộng. Nếu đặt khối ở P4 ($L = 1.600$) hay P3 ($L = 6.400$), số vòng tăng lên 11 và 13.

### F.3. Ước tính chi phí tầng 10

Ước tính giải tích số phép nhân–cộng (MAC), tính tay theo kích thước từng lớp cho một ảnh 640×640. Đề tài không báo cáo GFLOPs đo bằng công cụ cho riêng tầng này, vì công cụ đếm tự động không đếm đúng phép quét tự viết.

*Bảng PL.10. Ước tính chi phí phần xử lý chính của tầng 10. Không tính cv1, cv2 vì hai khối dùng chung, khoảng 210 triệu MAC.*

| Khối | Thành phần | Triệu MAC |
|---|---|---:|
| PSABlock (C2PSA) | qkv 52,4; $QK^\top$ 20,5; nhân với V 41,0; proj 26,2; mã hóa vị trí 0,9; FFN 104,9 | ≈ 246 |
| TSVMamba | SS2D: các phép chiếu và tích chập | ≈ 112 |
| | Nhánh hình dạng, cổng, fuse, FFN | ≈ 399 |
| | **Cộng** | **≈ 511** |

Phép quét song song không tính được bằng MAC: khoảng 67 triệu phép kết hợp, tức khoảng 200 triệu phép toán từng phần tử. Khoản tăng thêm khoảng 0,27 tỉ MAC, trong khi toàn mô hình theo ghi chú của Ultralytics cỡ 37 GFLOPs, nên số phép tính toàn mô hình chỉ tăng khoảng 1–2%. Trên CPU (chỉ forward, 4 luồng, checkpoint seed 0), mỗi ảnh mất khoảng 270 ms với mô hình đối chứng và 577 ms với mô hình đề xuất.

### F.4. Quy trình suy luận và huấn luyện của mô hình đề xuất

Ở mô hình đối chứng, quy trình giống hệt; chỉ khác bước 3 dùng C2PSA.

*Thuật toán PL.1. Suy luận và huấn luyện YOLO26s-seg + C2TSVMamba*

```
SUY LUẬN (một ảnh I)
1. Letterbox: co ảnh để cạnh dài bằng 640, giữ tỉ lệ, thêm viền xám
2. Backbone tầng 0–9: trích đặc trưng, ra 512×20×20 tại tầng 9
3. Tầng 10 – C2TSVMamba: cv1 → chia (a, b) → TSVMamba(b) theo (3.12) → ghép → cv2
4. Neck tầng 11–22: FPN đi xuống, PAN đi lên → P3, P4, P5
5. Segment26, đầu một-một: với mỗi điểm neo dự đoán hộp, điểm lớp, 32 hệ số mặt nạ;
   Proto26 sinh 32 mặt nạ mẫu 160×160
6. Lấy 300 dự đoán có điểm cao nhất, bỏ các dự đoán dưới ngưỡng tin cậy (không NMS)
7. Với mỗi dự đoán còn lại: tính Σ c_k·P_k, phóng về kích thước ảnh,
   nhị phân hóa (sigmoid > 0,5), rồi cắt theo hộp
8. Trả về danh sách (hộp, điểm tin cậy, mặt nạ)

MỘT BƯỚC HUẤN LUYỆN (lô ảnh đã tăng cường, epoch e)
1. Lan truyền xuôi như bước 2–5, cho cả hai đầu một-nhiều và một-một
2. Gán nhãn: TAL + STAL, top-10 cho đầu một-nhiều, top-7 rồi giữ 1 cho đầu một-một
3. Tính mất mát mỗi đầu theo Bảng 3.3; tổng hợp theo (3.15) với α(e)
4. Lan truyền ngược, cập nhật trọng số bằng AdamW; cập nhật bản trung bình động (EMA) của trọng số
5. Cuối epoch: kiểm định trên tập val bằng trọng số EMA, lưu best.pt khi chỉ số tốt hơn
```

## Phụ lục G. API và cấu trúc lưu trữ của ứng dụng PolypVision

*Bảng PL.11. Các API của dịch vụ suy luận*

| Phương thức | Đường dẫn | Dùng cho | Chức năng |
|---|---|---|---|
| GET | `/health` | Web | Trạng thái dịch vụ, thiết bị, danh sách mô hình |
| POST | `/predict` | Web | Nhận ảnh (`image`) và tên mô hình (`modelType`), trả kết quả một mô hình |
| GET | `/api/v1/health` | Mobile | Trạng thái tổng hợp |
| GET | `/api/v1/models` | Mobile | Danh sách hai mô hình và trạng thái sẵn sàng |
| POST | `/api/v1/inference` | Mobile | Nhận ảnh (`image`) và khóa mô hình (`modelKey`), suy luận một mô hình |
| POST | `/api/v1/comparison` | Mobile | Nhận ảnh (`image`), chạy cả hai mô hình trên cùng ảnh |

*Bảng PL.12. Các trường chính trong kết quả suy luận của API `/predict`*

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| `detected` | logic | Có phát hiện polyp hay không |
| `label` | chuỗi | Tên lớp (`polyp`) |
| `confidence` | số thực | Độ tin cậy cao nhất trong các đối tượng phát hiện |
| `maskCount` | số nguyên | Số mặt nạ (số polyp) phát hiện được |
| `processingTimeMs` | số thực | Thời gian gọi mô hình, tính bằng mili giây |
| `resultImageBase64` | chuỗi | Ảnh JPEG chồng mặt nạ và hộp bao, mã hóa Base64 |

Ngoài các trường trên còn `success`, `modelType`, `originalFileName` và `message`. Các API cho Mobile dùng cấu trúc riêng: mỗi kết quả có `modelKey`, `modelName`, `modelFamily`, các trường suy luận như trên, ảnh kết quả đặt trong `overlay.data`, kèm `requestId`, kích thước ảnh gốc và một câu cảnh báo nghiên cứu; kết quả so sánh gồm hai phần `baseline`, `vmamba` và `totalProcessingTimeMs`. Khi lỗi, các API `/api/v1/*` trả cấu trúc JSON gồm `requestId`, `status`, `code`, `message`, `fieldErrors`. Nhánh Mobile có giới hạn số yêu cầu suy luận đồng thời và thời gian chờ tối đa; nhánh Web dùng khóa riêng cho từng mô hình. Spring Boot còn cung cấp bộ REST API riêng (`/api/v1/auth`, `/api/v1/diagnoses`, `/api/v1/comparisons`, `/api/v1/dashboard`, `/api/v1/me`).

*Bảng PL.13. Tập `users` trong MongoDB*

| Trường | Ý nghĩa |
|---|---|
| `id` | Mã tài khoản |
| `fullName`, `email` | Họ tên và email; email là duy nhất |
| `passwordHash` | Mật khẩu đã băm bằng BCrypt, không lưu mật khẩu gốc |
| `role` | `USER` hoặc `ADMIN` |
| `enabled` | Tài khoản đang hoạt động hay bị khóa |
| `createdAt`, `updatedAt` | Thời điểm tạo và cập nhật |

*Bảng PL.14. Tập `diagnosis_history` trong MongoDB*

| Trường | Ý nghĩa |
|---|---|
| `id`, `userId` | Mã bản ghi, tài khoản sở hữu |
| `fileName` | Tên tệp ảnh người dùng tải lên |
| `modelType` | Mô hình đã dùng |
| `detected`, `label`, `confidence`, `maskCount` | Kết quả suy luận; `confidence` lưu theo thang 0–100 |
| `processingTimeMs` | Thời gian xử lý |
| `imageWidth`, `imageHeight` | Kích thước ảnh |
| `originalImageUrl`, `resultImageUrl` | Đường dẫn tới ảnh gốc và ảnh kết quả |
| `createdAt` | Thời điểm phân tích |
| `comparisonGroupId`, `comparisonResult` | Gắn hai bản ghi của cùng một lần so sánh với nhau |

## Phụ lục H. Kết quả thực nghiệm bổ sung

### H.1. So sánh hai mô hình YOLO trên tập kiểm định

![Hình PL.2](../hinh/ket_qua_20seed/vi/h01_cot_kep_chi_so_mask.png)

*Hình PL.2. Trung bình các chỉ số mặt nạ của hai mô hình trên 20 seed. Thanh lỗi là ±1 độ lệch chuẩn qua các seed.*

![Hình PL.3](../hinh/ket_qua_20seed/vi/r01_delta_tung_seed.png)

*Hình PL.3. Hiệu số mask mAP50–95 (TSVM − gốc) của từng seed, sắp xếp từ nhỏ đến lớn.*

![Hình PL.4](../hinh/ket_qua_20seed/vi/r02_hop_phan_bo.png)

*Hình PL.4. Phân bố mask mAP50–95 qua 20 seed của hai mô hình.*

![Hình PL.5](../hinh/ket_qua_20seed/vi/r04_do_nhay_quy_tac_epoch.png)

*Hình PL.5. Mask mAP50–95 theo ba quy tắc chọn epoch. Điểm là trung bình, thanh là ±1 độ lệch chuẩn.*

![Hình PL.6](../hinh/ket_qua_20seed/vi/h03_duong_mien_mask_map_theo_epoch.png)

*Hình PL.6. Mask mAP50–95 trên tập kiểm định theo epoch. Đường là trung bình 20 seed, miền tô là ±1 độ lệch chuẩn. Ô nhỏ phóng to đoạn epoch 70–100.*

*Bảng PL.15. Mask mAP50–95 tại một số epoch*

| Epoch | YOLO26s-seg | TSVM |
|---:|---:|---:|
| 5 | 0,5320 ± 0,0427 | 0,5076 ± 0,0485 |
| 10 | 0,5687 ± 0,0355 | 0,5606 ± 0,0347 |
| 30 | 0,6349 ± 0,0183 | 0,6320 ± 0,0287 |
| 50 | 0,6716 ± 0,0208 | 0,6709 ± 0,0091 |
| 70 | 0,6890 ± 0,0125 | 0,6931 ± 0,0120 |
| 90 | 0,7035 ± 0,0152 | 0,7084 ± 0,0102 |
| 100 | 0,7093 ± 0,0132 | 0,7119 ± 0,0130 |

*Nguồn: `bang/05_duong_cong_theo_epoch.csv`. Khi tắt Mosaic ở epoch 91, mAP của cả hai mô hình giảm nhẹ một epoch rồi tăng lại.*

![Hình PL.7](../hinh/ket_qua_20seed/vi/c01_val_seg_loss.png)

*Hình PL.7. Hàm mất mát phân đoạn trên tập kiểm định theo epoch. Dấu ▼ đánh dấu epoch có giá trị trung bình thấp nhất.*

### H.2. Đánh giá theo pixel, topology và độ trễ

![Hình PL.8](../hinh/ket_qua_20seed/vi/p02_diem_dice_tung_seed.png)

*Hình PL.8. Dice theo pixel của từng seed.*

![Hình PL.9](../hinh/ket_qua_20seed/vi/p03_bao_nham_anh_nen.png)

*Hình PL.9. Tỉ lệ ảnh nền bị báo nhầm (có ít nhất một pixel dự đoán là polyp) trên 40 ảnh nền.*

![Hình PL.10](../hinh/ket_qua_20seed/vi/o02_kieu_loi_topology.png)

*Hình PL.10. Tỉ lệ ảnh mắc từng kiểu lỗi topology: thừa mảnh, có lỗ và thiếu mảnh.*

![Hình PL.11](../hinh/chung/vi/e02_do_tre_cpu.png)

*Hình PL.11. Độ trễ trên CPU của hai mô hình ở hai chế độ đo. Thanh lỗi là ±1 độ lệch chuẩn qua 100 lần đo.*

### H.3. Dữ liệu ngoài

*Bảng PL.16. Tỉ lệ ảnh có polyp bị bỏ sót hoàn toàn (mô hình không dự đoán pixel nào)*

| Bộ dữ liệu | YOLO26s-seg | TSVM | PraNet | U-Net | TSVM − gốc | p (t) |
|---|---:|---:|---:|---:|---:|---:|
| CVC-ClinicDB | 11,3% | 13,4% | 10,1% | 7,9% | +2,1 điểm % | 0,003 |
| CVC-ColonDB | 28,2% | 32,0% | 32,0% | 27,0% | +3,8 điểm % | < 0,001 |
| ETIS-Larib | 37,3% | 38,6% | 39,4% | 20,6% | +1,3 điểm % | 0,580 |
| PolypGen (gộp) | 18,1% | 18,9% | 16,3% | 11,5% | +0,8 điểm % | 0,296 |

*Nguồn: `08_du_lieu_thuc_te/bang/20seed/01_ngoai_tung_seed.csv`, `02_ngoai_thong_ke.csv` (chỉ số `no_pred_rate`).*

*Bảng PL.17. Dice theo pixel trên từng trung tâm của PolypGen (20 seed)*

| Trung tâm | Ảnh có polyp | YOLO26s-seg | TSVM | PraNet | U-Net | TSVM − gốc | p (t) | p (Wilcoxon) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C1 | 251 | 0,753 | 0,752 | 0,724 | 0,511 | −0,001 | 0,85 | 0,87 |
| C2 | 270 | 0,753 | 0,749 | 0,759 | 0,543 | −0,005 | 0,52 | 0,50 |
| C3 | 456 | 0,855 | 0,856 | 0,806 | 0,593 | +0,002 | 0,69 | 0,99 |
| C4 | 146 | 0,516 | 0,503 | 0,449 | 0,255 | −0,013 | 0,28 | 0,048 |
| C5 | 206 | 0,474 | 0,472 | 0,418 | 0,292 | −0,002 | 0,85 | 0,45 |
| C6 | 83 | 0,720 | 0,699 | 0,708 | 0,492 | −0,021 | 0,032 | 0,019 |
| **Gộp** | **1.412** | **0,719** | **0,715** | **0,683** | **0,484** | −0,004 | 0,55 | 0,25 |

*Nguồn: `08_du_lieu_thuc_te/bang/20seed/02_ngoai_thong_ke.csv`. PraNet chỉ tốt hơn hai mô hình YOLO ở C2.*

![Hình PL.12](../hinh/ket_qua_20seed/vi/x02_dice_polypgen_trung_tam.png)

*Hình PL.12. Dice theo pixel trên từng trung tâm của PolypGen.*
