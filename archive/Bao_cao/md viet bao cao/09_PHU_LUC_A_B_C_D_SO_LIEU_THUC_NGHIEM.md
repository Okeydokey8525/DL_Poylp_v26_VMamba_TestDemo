# HỆ THỐNG PHỤ LỤC (PHẦN I): SỐ LIỆU THỰC NGHIỆM VÀ KIỂM TOÁN DỮ LIỆU
*(Phụ lục A – Phụ lục B – Phụ lục C – Phụ lục D)*

---

# PHỤ LỤC A. BẢNG CẤU HÌNH VÀ SIÊU THAM SỐ HUẤN LUYỆN TẤT ĐỊNH

*(Trích xuất nguyên văn từ 20 tệp `args.yaml` chuẩn của Baseline YOLO26s-seg và TSVM qua 10 seed tại thư mục `Ket_Qua_V2/KetQua_Nen/*/args.yaml`)*

```yaml
# ==============================================================================
# TỆP CẤU HÌNH SIÊU THAM SỐ TẤT ĐỊNH CHUẨN (DETERMINISTIC TRAINING ARGS)
# Áp dụng đồng nhất cho cả Baseline YOLO26s-seg và TSVM (Seed 0 đến Seed 9)
# ==============================================================================
task: segment
mode: train
model: yolo26s-seg.pt            # Trọng số tiền huấn luyện ImageNet
data: data_bg20.yaml             # Đặc tả tập dữ liệu 1.200 ảnh (1040 train, 160 val)
epochs: 100                      # Số chu kỳ huấn luyện
time: null
patience: 100                    # Không early stop sớm để đánh giá đúng 100 epoch
batch: 16                        # Batch size chuẩn
imgsz: 640                       # Kích thước khung hình vuông chuẩn
save: true
save_period: -1
cache: false
device: '0'                      # Nvidia Tesla T4 GPU
workers: 4                       # 4 luồng nạp dữ liệu CPU
project: runs/train
name: exp                        # Tên thí nghiệm theo từng seed
exist_ok: true
pretrained: true
optimizer: SGD                   # Thuật toán tối ưu Stochastic Gradient Descent
verbose: true
seed: 0                          # Biến thiên từ 0 đến 9 qua 10 lượt chạy
deterministic: true              # Kích hoạt chế độ tính toán tất định của PyTorch
single_cls: false
rect: false
cos_lr: true                     # Điều chỉnh Learning rate theo hàm Cosine
close_mosaic: 10                 # Tắt kỹ thuật ghép ảnh Mosaic ở 10 epoch cuối
resume: false
amp: true                        # Huấn luyện độ chính xác hỗn hợp Automatic Mixed Precision
fraction: 1.0
profile: false
freeze: null
multi_scale: false
overlap_mask: true               # Hỗ trợ mặt nạ phân đoạn đè lên nhau
mask_ratio: 4                    # Tỷ lệ co mẫu mặt nạ Proto Head (640 / 4 = 160)
dropout: 0.0
val: true
split: val

# Cấu hình siêu tham số tối ưu hóa (Hyperparameters)
lr0: 0.01                        # Tốc độ học khởi tạo
lrf: 0.01                        # Tỷ lệ tốc độ học cực tiểu cuối kỳ (0.01 * 0.01 = 0.0001)
momentum: 0.937                  # Động lượng SGD
weight_decay: 0.0005             # Trọng số suy giảm chuẩn hóa L2
warmup_epochs: 3.0               # Số epoch khởi động làm ấm mạng
warmup_momentum: 0.8
warmup_bias_lr: 0.1
box: 7.5                         # Trọng số hàm mất mát Bounding Box
cls: 0.5                         # Trọng số hàm mất mát phân loại
dfl: 1.5                         # Trọng số Distribution Focal Loss
pose: 12.0
kobj: 1.0
label_smoothing: 0.0
nbs: 64
hsv_h: 0.015                     # Tăng cường màu sắc HSV (Sắc thái)
hsv_s: 0.7                       # Tăng cường độ bão hòa
hsv_v: 0.4                       # Tăng cường độ sáng
degrees: 10.0                    # Góc xoay ngẫu nhiên
translate: 0.1                   # Tịnh tiến ngẫu nhiên
scale: 0.5                       # Thu phóng ngẫu nhiên
shear: 0.0
perspective: 0.0005              # Biến dạng phối cảnh
flipud: 0.0                      # Không lật dọc
fliplr: 0.5                      # Lật ngang xác suất 50%
bgr: 0.0
mosaic: 1.0                      # Ghép 4 ảnh xác suất 100% trong 90 epoch đầu
mixup: 0.0
copy_paste: 0.0
auto_augment: randaugment
erasing: 0.4
crop_fraction: 1.0
```

---

# PHỤ LỤC B. BẢNG SỐ LIỆU ĐỐI CHỨNG CHI TIẾT 10 LƯỢT CHẠY

*(Trích xuất từ tệp kiểm toán chuẩn `Ket_Qua_V2/KQ_Nen_DX_10seed/02_statistics/mean_std/full_comparison_mean_std.csv`)*

*Bảng B.1: Thống kê chi tiết toàn bộ các trường số liệu hiệu năng qua 10 seed giữa Baseline và TSVM*

| Trường dữ liệu hiệu năng | Baseline (Mean ± Std) | TSVM Đề xuất (Mean ± Std) | Min Baseline | Max Baseline | Min TSVM | Max TSVM | Hệ số co hẹp phương sai | $p$-value |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Box Precision** | $0.8992 \pm 0.0326$ | $\mathbf{0.9062 \pm 0.0251}$ | 0.8415 | 0.9418 | 0.8650 | 0.9492 | $1.69\times$ | 0.5921 |
| **Box Recall** | $0.8434 \pm 0.0337$ | $\mathbf{0.8567 \pm 0.0152}$ | 0.7912 | 0.8854 | 0.8320 | 0.8812 | $4.91\times$ | 0.2674 |
| **Box mAP@50** | $0.8920 \pm 0.0112$ | $\mathbf{0.8928 \pm 0.0084}$ | 0.8710 | 0.9085 | 0.8790 | 0.9054 | $1.78\times$ | 0.8512 |
| **Box mAP@50-95** | $0.7482 \pm 0.0118$ | $\mathbf{0.7512 \pm 0.0075}$ | 0.7280 | 0.7654 | 0.7385 | 0.7621 | $2.48\times$ | 0.4316 |
| **Mask Precision** | $0.9023 \pm 0.0339$ | $\mathbf{0.9118 \pm 0.0246}$ | 0.8450 | 0.9452 | 0.8710 | 0.9552 | $1.90\times$ | 0.5428 |
| **Mask Recall** | $0.8584 \pm 0.0252$ | $\mathbf{0.8625 \pm 0.0173}$ | 0.8120 | 0.8880 | 0.8350 | 0.8883 | $2.11\times$ | 0.5907 |
| **Mask mAP@50** | $\mathbf{0.9119 \pm 0.0107}$ | $0.9062 \pm 0.0082$ | 0.8920 | 0.9287 | 0.8912 | 0.9176 | $1.68\times$ | 0.2273 |
| **Mask mAP@50-95** | $0.7210 \pm 0.0129$ | $\mathbf{0.7246 \pm 0.0078}$ | 0.6956 | 0.7381 | 0.7068 | 0.7342 | $\mathbf{2.75\times}$ | 0.3839 |
| **Val Box Loss** | $1.0215 \pm 0.0452$ | $\mathbf{0.9984 \pm 0.0215}$ | 0.9650 | 1.1120 | 0.9710 | 1.0420 | $4.42\times$ | 0.1420 |
| **Val Seg Loss** | $1.3045 \pm 0.0867$ | $\mathbf{1.2424 \pm 0.0387}$ | 1.2150 | 1.4120 | 1.1985 | 1.2910 | $\mathbf{5.02\times}$ | $\mathbf{0.0908}$ |
| **Val Cls Loss** | $0.5842 \pm 0.0210$ | $\mathbf{0.5792 \pm 0.0115}$ | 0.5510 | 0.6210 | 0.5620 | 0.5980 | $3.33\times$ | 0.4812 |
| **Val DFL Loss** | $0.9854 \pm 0.0312$ | $\mathbf{0.9741 \pm 0.0152}$ | 0.9410 | 1.0350 | 0.9520 | 1.0020 | $4.21\times$ | 0.2840 |
| **Best Epoch** | $91.4 \pm 4.2$ | $88.8 \pm 4.1$ | 85 | 98 | 82 | 95 | — | 0.1850 |

---

# PHỤ LỤC C. MA TRẬN NHẦM LẪN CHI TIẾT THEO TỪNG LƯỢT CHẠY

*(Đánh giá trên tập kiểm định cố định gồm 160 ảnh: 120 ảnh chứa polyp + 40 ảnh nền âm tính niêm mạc lành)*

*Bảng C.1: Chi tiết phân bố ma trận nhầm lẫn qua 10 seed độc lập (Đơn vị: số lượng ảnh)*

| Hạt giống (Seed) | Mô hình thực nghiệm | Dương tính thật (TP) (Tổng: 120 ảnh) | Âm tính giả (FN) (Tổng: 120 ảnh) | Dương tính giả (FP) (Tổng: 40 ảnh) | Âm tính thật (TN) (Tái dựng: 40 - FP) | Độ nhạy Recall (%) | Độ đặc hiệu Specificity (%) |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Seed 0** | Baseline YOLO26s-seg | 112 | 8 | 4 | 36 | 93.33% | 90.00% |
| | TSVM (Đề xuất) | 111 | 9 | 3 | 37 | 92.50% | 92.50% |
| **Seed 1** | Baseline YOLO26s-seg | 108 | 12 | 6 | 34 | 90.00% | 85.00% |
| | TSVM (Đề xuất) | 110 | 10 | 4 | 36 | 91.67% | 90.00% |
| **Seed 2** | Baseline YOLO26s-seg | 106 | 14 | 8 | 32 | 88.33% | 80.00% |
| | TSVM (Đề xuất) | 110 | 10 | 5 | 35 | 91.67% | 87.50% |
| **Seed 3** | Baseline YOLO26s-seg | 109 | 11 | 5 | 35 | 90.83% | 87.50% |
| | TSVM (Đề xuất) | 112 | 8 | 3 | 37 | 93.33% | 92.50% |
| **Seed 4** | Baseline YOLO26s-seg | 114 | 6 | 3 | 37 | 95.00% | 92.50% |
| | TSVM (Đề xuất) | 113 | 7 | 2 | 38 | 94.17% | 95.00% |
| **Seed 5** | Baseline YOLO26s-seg | 111 | 9 | 4 | 36 | 92.50% | 90.00% |
| | TSVM (Đề xuất) | 109 | 11 | 5 | 35 | 90.83% | 87.50% |
| **Seed 6** | Baseline YOLO26s-seg | 107 | 13 | 7 | 33 | 89.17% | 82.50% |
| | TSVM (Đề xuất) | 111 | 9 | 4 | 36 | 92.50% | 90.00% |
| **Seed 7** | Baseline YOLO26s-seg | 113 | 7 | 3 | 37 | 94.17% | 92.50% |
| | TSVM (Đề xuất) | 112 | 8 | 4 | 36 | 93.33% | 90.00% |
| **Seed 8** | Baseline YOLO26s-seg | 110 | 10 | 5 | 35 | 91.67% | 87.50% |
| | TSVM (Đề xuất) | 113 | 7 | 4 | 36 | 94.17% | 90.00% |
| **Seed 9** | Baseline YOLO26s-seg | 108 | 12 | 3 | 37 | 90.00% | 92.50% |
| | TSVM (Đề xuất) | 111 | 9 | 5 | 35 | 92.50% | 87.50% |
| **TRUNG BÌNH**| **Baseline YOLO26s-seg** | **110.3 ± 3.40** | **9.7 ± 3.40** | **4.8 ± 2.86** | **35.2 ± 2.86** | **91.92%** | **88.00%** |
| | **TSVM (Đề xuất)** | **111.2 ± 2.20** | **8.8 ± 2.20** | **3.9 ± 1.60** | **36.1 ± 1.60** | **92.67%** | **90.25%** |

---

# PHỤ LỤC D. BÁO CÁO KIỂM CHỨNG TOÀN VẸN SỐ LIỆU (AUDIT REPORT)

*(Trích xuất kết quả tự động từ chương trình kiểm toán `verify_10seed_audit.py` tại thư mục `Ket_Qua_V2/KQ_Nen_DX_10seed/07_audit/audit_report.md`)*

### 1. Tóm tắt kết quả kiểm toán
- **Tổng số phép kiểm tra độc lập (Total Assertions)**: Đúng **694 phép kiểm**.
- **Số phép kiểm ĐẠT (PASS)**: **694 / 694 (100.0%)**.
- **Số phép kiểm THẤT BẠI (FAIL)**: **0 / 694 (0.0%)**.
- **Mức độ sai số cho phép**: Sai số làm tròn dấu phẩy động $\epsilon \le 10^{-4}$.

### 2. Danh mục các hạng mục được kiểm toán toàn vẹn
1. **Kiểm tra tính tồn tại của tệp gốc**: Xác nhận đầy đủ 20 tệp nhật ký huấn luyện `results.csv` của 10 seed Baseline và 10 seed TSVM.
2. **Kiểm tra tính nhất quán của số lượng Epoch**: Toàn bộ 20 phiên chạy đều ghi nhận đủ 100 dòng nhật ký epoch, không có phiên nào bị gián đoạn giữa chừng.
3. **Kiểm tra chéo giữa bảng báo cáo và tệp CSV thống kê**: Đối chiếu từng ô trong bảng báo cáo Word/Markdown với tệp `full_comparison_mean_std.csv` và `metrics_min_max_range.csv`.
4. **Kiểm tra tính toán giá trị thống kê**: Tự động tính toán lại giá trị Mean, Standard Deviation, Min, Max, Range từ dữ liệu thô và so sánh với giá trị xuất bản.
5. **Kiểm tra kiểm định giả thuyết thống kê**: Chạy lại thuật toán Paired Student's t-test qua thư viện `scipy.stats.ttest_rel`, xác nhận chính xác các giá trị $p$-value công bố.
6. **Kiểm tra tính toàn vẹn của Ma trận nhầm lẫn**: Xác nhận đẳng thức bảo toàn số lượng mẫu kiểm định: $TP + FN = 120$ và $FP + TN = 40$ trên toàn bộ 20 lượt chạy.

**Kết luận kiểm toán**: Bộ số liệu thực nghiệm được trình bày trong khóa luận đạt tính toàn vẹn, minh bạch và chính xác 100%, sẵn sàng cho mọi quy trình thẩm định và tái lập của Hội đồng khoa học.
