# Kết quả II.1: ablation và C2PSA rộng trên CVC, đủ 20 seed

Ngày 09/11/2026, nhánh `Okeydokey`.

**Hash commit:** `cfea12bed8f3ce5a189a27090186b3dcd65d04e1` (`cfea12be`), đã push.

## 1. Đã làm gì

- **Kiểm tra checkpoint (bước 1):** đủ 80/80 `best.pt` (Vmamba_only, Shape_only, No_guidance, C2PSA_rong × seed 0–19). Mỗi file lớn hơn 1 MB; `args.yaml` có `epochs: 100` và `seed` khớp tên thư mục. Không thiếu file nào.
- **`08_du_lieu_thuc_te/scripts/danh_gia_ablation_ngoai.py`:**
  - Thêm `"c2psa_rong": (["C2PSA_rong"], "Kvasir_BG20_YOLO26s_seg_C2PSA_rong_s{s}_w2")` vào `VARIANTS`.
  - Sửa docstring: thêm C2PSA rộng và lần chạy đủ seed 0–19.
  - Mặc định `--seeds` vẫn là seed 0–9.
  - Thêm assert số tham số tầng 10 ở seed đầu của mỗi biến thể (mục 4).
- **Kết quả từng lượt:** 100 lượt mới (3 biến thể × seed 10–19, cùng C2PSA rộng × seed 0–19, × 2 bộ CVC) ghi vào `08_du_lieu_thuc_te/bang/tung_luot_ablation/`.
  - Thư mục hiện có 160 file. ClinicDB mỗi file 612 dòng, ColonDB mỗi file 380 dòng.
  - 60 lượt cũ (seed 0–9) không bị chạy lại hay thay đổi.
- **Tổng hợp:**
  - `phan_tich_ablation_ngoai.py` và `bang/ablation_ngoai/01_*`, `02_*` **không có trong repo**, kể cả trên `origin/Okeydokey` và `origin/phungtuanhuy18`; chắc chỉ có ở máy Huy. Vì vậy Lương không sửa được script đó và không so từng byte được với bản 10 seed.
  - Thay vào đó, Lương viết script mới tên khác để tránh đụng file của Huy: `08_du_lieu_thuc_te/scripts/tong_hop_ablation_ngoai.py` (không cần GPU). Chỉ số từng lượt tính đúng như `summarize()` của `danh_gia_du_lieu_ngoai.py`.
  - Kết quả ghi vào `08_du_lieu_thuc_te/bang/ablation_ngoai/20seed/01_ablation_ngoai_tung_seed.csv` và `02_ablation_ngoai_thong_ke.csv`.
  - Huy có thể chạy lại bằng script của Huy rồi so với hai file này.
- **Kiểm tra:** dòng `baseline`, `tsvm` (no_pred_rate, Recall, Dice, IoU, Precision của ClinicDB và ColonDB, 80 dòng) khớp tuyệt đối `08_du_lieu_thuc_te/bang/20seed/01_ngoai_tung_seed.csv` (chênh lớn nhất 0,0).
- **Không sửa:** `bang/20seed/`, `bang/tung_luot/`, Word, checkpoint. Không commit `.pt`, `.pth`, `.zip`.

Định nghĩa:
- `no_pred_rate`: tỉ lệ ảnh polyp không có điểm ảnh dự đoán nào.
- Recall, Dice: trung bình theo ảnh có polyp.

Số liệu là trung bình ± SD qua 20 seed (seed 0–19).

## 2. Bảng 20 seed theo từng bộ

**CVC-ClinicDB (612 ảnh)**

| Mô hình | no_pred_rate | Recall | Dice |
|---|---|---|---|
| YOLO26s-seg (gốc) | 0,1134 ± 0,0226 | 0,8178 ± 0,0183 | 0,7860 ± 0,0178 |
| YOLO26s-seg + TSVM | 0,1344 ± 0,0236 | 0,7960 ± 0,0218 | 0,7702 ± 0,0208 |
| Chỉ SS2D (vmamba_only) | 0,1249 ± 0,0223 | 0,8047 ± 0,0184 | 0,7766 ± 0,0177 |
| Chỉ nhánh hình dạng (shape_only) | 0,1237 ± 0,0245 | 0,8065 ± 0,0208 | 0,7778 ± 0,0206 |
| Bỏ cổng (no_guidance) | 0,1297 ± 0,0204 | 0,8018 ± 0,0182 | 0,7735 ± 0,0160 |
| C2PSA rộng | 0,1245 ± 0,0207 | 0,8075 ± 0,0190 | 0,7785 ± 0,0156 |

**CVC-ColonDB (380 ảnh)**

| Mô hình | no_pred_rate | Recall | Dice |
|---|---|---|---|
| YOLO26s-seg (gốc) | 0,2816 ± 0,0307 | 0,6639 ± 0,0235 | 0,6308 ± 0,0227 |
| YOLO26s-seg + TSVM | 0,3199 ± 0,0348 | 0,6299 ± 0,0305 | 0,6012 ± 0,0289 |
| Chỉ SS2D (vmamba_only) | 0,3068 ± 0,0345 | 0,6398 ± 0,0274 | 0,6080 ± 0,0278 |
| Chỉ nhánh hình dạng (shape_only) | 0,3059 ± 0,0307 | 0,6387 ± 0,0230 | 0,6086 ± 0,0231 |
| Bỏ cổng (no_guidance) | 0,2993 ± 0,0430 | 0,6455 ± 0,0356 | 0,6157 ± 0,0332 |
| C2PSA rộng | 0,3192 ± 0,0310 | 0,6316 ± 0,0264 | 0,6020 ± 0,0259 |


## 3. So sánh ghép cặp theo seed

- Hiệu là a − b.
- Cột cuối là số seed a cao hơn b; seed bằng nhau không tính.
- Nhóm so sánh:
  - TSVM với mô hình gốc;
  - từng biến thể và C2PSA rộng với mô hình gốc (a = biến thể);
  - TSVM với từng biến thể và C2PSA rộng (a = TSVM).

**CVC-ClinicDB (612 ảnh)**

| So sánh (a − b) | Chỉ số | Chênh lệch | p (t ghép cặp) | p (Wilcoxon) | Số seed a cao hơn |
|---|---|---|---|---|---|
| YOLO26s-seg + TSVM − YOLO26s-seg (gốc) | no_pred_rate | +0,0210 | 0,0030 | 0,0054 | 15/20 |
| YOLO26s-seg + TSVM − YOLO26s-seg (gốc) | recall | −0,0218 | 0,0015 | 0,0032 | 5/20 |
| YOLO26s-seg + TSVM − YOLO26s-seg (gốc) | dice | −0,0158 | 0,0060 | 0,0064 | 5/20 |
| Chỉ SS2D (vmamba_only) − YOLO26s-seg (gốc) | no_pred_rate | +0,0115 | 0,0321 | 0,0421 | 13/20 |
| Chỉ SS2D (vmamba_only) − YOLO26s-seg (gốc) | recall | −0,0131 | 0,0022 | 0,0027 | 5/20 |
| Chỉ SS2D (vmamba_only) − YOLO26s-seg (gốc) | dice | −0,0093 | 0,0400 | 0,0532 | 6/20 |
| YOLO26s-seg + TSVM − Chỉ SS2D (vmamba_only) | no_pred_rate | +0,0095 | 0,2256 | 0,1913 | 11/20 |
| YOLO26s-seg + TSVM − Chỉ SS2D (vmamba_only) | recall | −0,0087 | 0,2112 | 0,1650 | 7/20 |
| YOLO26s-seg + TSVM − Chỉ SS2D (vmamba_only) | dice | −0,0064 | 0,3048 | 0,2943 | 9/20 |
| Chỉ nhánh hình dạng (shape_only) − YOLO26s-seg (gốc) | no_pred_rate | +0,0103 | 0,0720 | 0,0825 | 10/20 |
| Chỉ nhánh hình dạng (shape_only) − YOLO26s-seg (gốc) | recall | −0,0113 | 0,0141 | 0,0400 | 8/20 |
| Chỉ nhánh hình dạng (shape_only) − YOLO26s-seg (gốc) | dice | −0,0082 | 0,0898 | 0,2455 | 10/20 |
| YOLO26s-seg + TSVM − Chỉ nhánh hình dạng (shape_only) | no_pred_rate | +0,0107 | 0,0978 | 0,1054 | 14/20 |
| YOLO26s-seg + TSVM − Chỉ nhánh hình dạng (shape_only) | recall | −0,0105 | 0,0608 | 0,0441 | 6/20 |
| YOLO26s-seg + TSVM − Chỉ nhánh hình dạng (shape_only) | dice | −0,0076 | 0,1335 | 0,1054 | 8/20 |
| Bỏ cổng (no_guidance) − YOLO26s-seg (gốc) | no_pred_rate | +0,0163 | 0,0347 | 0,0438 | 15/20 |
| Bỏ cổng (no_guidance) − YOLO26s-seg (gốc) | recall | −0,0160 | 0,0174 | 0,0153 | 5/20 |
| Bỏ cổng (no_guidance) − YOLO26s-seg (gốc) | dice | −0,0125 | 0,0369 | 0,0532 | 7/20 |
| YOLO26s-seg + TSVM − Bỏ cổng (no_guidance) | no_pred_rate | +0,0047 | 0,4929 | 0,6407 | 9/20 |
| YOLO26s-seg + TSVM − Bỏ cổng (no_guidance) | recall | −0,0058 | 0,3703 | 0,5459 | 10/20 |
| YOLO26s-seg + TSVM − Bỏ cổng (no_guidance) | dice | −0,0033 | 0,5598 | 0,6742 | 10/20 |
| C2PSA rộng − YOLO26s-seg (gốc) | no_pred_rate | +0,0111 | 0,1117 | 0,1304 | 13/20 |
| C2PSA rộng − YOLO26s-seg (gốc) | recall | −0,0104 | 0,0914 | 0,1140 | 7/20 |
| C2PSA rộng − YOLO26s-seg (gốc) | dice | −0,0075 | 0,1620 | 0,1536 | 7/20 |
| YOLO26s-seg + TSVM − C2PSA rộng | no_pred_rate | +0,0099 | 0,0461 | 0,0437 | 13/20 |
| YOLO26s-seg + TSVM − C2PSA rộng | recall | −0,0115 | 0,0123 | 0,0215 | 6/20 |
| YOLO26s-seg + TSVM − C2PSA rộng | dice | −0,0083 | 0,0718 | 0,0897 | 6/20 |

**CVC-ColonDB (380 ảnh)**

| So sánh (a − b) | Chỉ số | Chênh lệch | p (t ghép cặp) | p (Wilcoxon) | Số seed a cao hơn |
|---|---|---|---|---|---|
| YOLO26s-seg + TSVM − YOLO26s-seg (gốc) | no_pred_rate | +0,0383 | 2,6·10⁻⁴ | 9,0·10⁻⁴ | 16/20 |
| YOLO26s-seg + TSVM − YOLO26s-seg (gốc) | recall | −0,0340 | 2,4·10⁻⁴ | 1,7·10⁻⁴ | 3/20 |
| YOLO26s-seg + TSVM − YOLO26s-seg (gốc) | dice | −0,0296 | 5,6·10⁻⁴ | 3,9·10⁻⁴ | 3/20 |
| Chỉ SS2D (vmamba_only) − YOLO26s-seg (gốc) | no_pred_rate | +0,0253 | 0,0310 | 0,0382 | 14/20 |
| Chỉ SS2D (vmamba_only) − YOLO26s-seg (gốc) | recall | −0,0242 | 0,0105 | 0,0121 | 5/20 |
| Chỉ SS2D (vmamba_only) − YOLO26s-seg (gốc) | dice | −0,0228 | 0,0138 | 0,0136 | 6/20 |
| YOLO26s-seg + TSVM − Chỉ SS2D (vmamba_only) | no_pred_rate | +0,0130 | 0,2826 | 0,2110 | 12/20 |
| YOLO26s-seg + TSVM − Chỉ SS2D (vmamba_only) | recall | −0,0098 | 0,3390 | 0,2943 | 8/20 |
| YOLO26s-seg + TSVM − Chỉ SS2D (vmamba_only) | dice | −0,0067 | 0,4837 | 0,2943 | 8/20 |
| Chỉ nhánh hình dạng (shape_only) − YOLO26s-seg (gốc) | no_pred_rate | +0,0243 | 0,0156 | 0,0100 | 16/20 |
| Chỉ nhánh hình dạng (shape_only) − YOLO26s-seg (gốc) | recall | −0,0253 | 0,0043 | 0,0042 | 4/20 |
| Chỉ nhánh hình dạng (shape_only) − YOLO26s-seg (gốc) | dice | −0,0222 | 0,0063 | 0,0073 | 5/20 |
| YOLO26s-seg + TSVM − Chỉ nhánh hình dạng (shape_only) | no_pred_rate | +0,0139 | 0,1100 | 0,1973 | 10/20 |
| YOLO26s-seg + TSVM − Chỉ nhánh hình dạng (shape_only) | recall | −0,0087 | 0,2160 | 0,3884 | 10/20 |
| YOLO26s-seg + TSVM − Chỉ nhánh hình dạng (shape_only) | dice | −0,0074 | 0,2479 | 0,4524 | 10/20 |
| Bỏ cổng (no_guidance) − YOLO26s-seg (gốc) | no_pred_rate | +0,0178 | 0,1934 | 0,2043 | 14/20 |
| Bỏ cổng (no_guidance) − YOLO26s-seg (gốc) | recall | −0,0184 | 0,0925 | 0,0637 | 6/20 |
| Bỏ cổng (no_guidance) − YOLO26s-seg (gốc) | dice | −0,0151 | 0,1336 | 0,1429 | 6/20 |
| YOLO26s-seg + TSVM − Bỏ cổng (no_guidance) | no_pred_rate | +0,0205 | 0,1605 | 0,2110 | 12/20 |
| YOLO26s-seg + TSVM − Bỏ cổng (no_guidance) | recall | −0,0156 | 0,1939 | 0,2611 | 8/20 |
| YOLO26s-seg + TSVM − Bỏ cổng (no_guidance) | dice | −0,0145 | 0,1881 | 0,2774 | 8/20 |
| C2PSA rộng − YOLO26s-seg (gốc) | no_pred_rate | +0,0376 | 2,8·10⁻⁴ | 4,8·10⁻⁴ | 18/20 |
| C2PSA rộng − YOLO26s-seg (gốc) | recall | −0,0323 | 3,3·10⁻⁴ | 1,3·10⁻⁴ | 4/20 |
| C2PSA rộng − YOLO26s-seg (gốc) | dice | −0,0288 | 4,2·10⁻⁴ | 2,1·10⁻⁴ | 3/20 |
| YOLO26s-seg + TSVM − C2PSA rộng | no_pred_rate | +0,0007 | 0,9328 | 0,9679 | 7/20 |
| YOLO26s-seg + TSVM − C2PSA rộng | recall | −0,0016 | 0,8043 | 0,8695 | 11/20 |
| YOLO26s-seg + TSVM − C2PSA rộng | dice | −0,0008 | 0,8997 | 0,9854 | 12/20 |

## 4. Kiểm tra, thời gian chạy, lỗi

Số tham số tầng 10 (`model.model[10]`) đã assert ở seed 0 của mỗi biến thể; cả bốn đều đúng:

| Biến thể | Lớp tầng 10 | Số tham số |
|---|---|---|
| vmamba_only | C2TSVMamba | 1.071.873 |
| shape_only | C2TSVMamba | 1.331.969 |
| no_guidance | C2TSVMamba | 1.745.409 |
| c2psa_rong | C2PSA | 1.830.016 |

- **`--kiem-tra`:** "KIỂM TRA: ĐỦ, có thể chạy" (4 biến thể × 20 seed × 2 bộ).
- **`--doi-chieu`:** "ĐỐI CHIẾU tsvm s0 clinicdb: 0/612 ảnh lệch số điểm ảnh dự đoán; ảnh không dự đoán: cũ 64, mới 64".
- **Máy:** NVIDIA GeForce RTX 5050 Laptop GPU, torch 2.13.0+cu130.
- **Thời gian:** 27,2 phút cho 100 lượt (log: `08_du_lieu_thuc_te/bang/_log_chay_ablation_20seed.txt`).
  - Lâu hơn dự kiến 15–20 phút, có thể do GPU còn chạy dịch vụ khác cùng lúc.
- **Lỗi:** không có.
- **Chưa làm được:** so từng byte bản 10 seed với `bang/ablation_ngoai/01_*`, `02_*`, vì script và bảng đó không có trong repo (xem mục 1).
