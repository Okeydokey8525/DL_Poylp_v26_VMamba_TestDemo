# Kết quả chạy ablation trên dữ liệu ngoài (máy Lương, 07/11/2026)

Script: `08_du_lieu_thuc_te/scripts/danh_gia_ablation_ngoai.py` (bản Huy gửi, không sửa).
Môi trường: `C:\venv_kl_gpu\Scripts\python.exe`, torch 2.13.0+cu130, GPU NVIDIA GeForce RTX 5050 Laptop GPU (8 GiB).
Chỉ suy luận; không train, không sửa hay ghi đè tệp có sẵn.

## Bước 2: kiểm tra (`--kiem-tra`)

```
GPU: NVIDIA GeForce RTX 5050 Laptop GPU
KIỂM TRA: ĐỦ, có thể chạy
```

## Bước 3: đối chiếu môi trường (`--doi-chieu`)

```
ĐỐI CHIẾU tsvm s0 clinicdb: 0/612 ảnh lệch số điểm ảnh dự đoán; ảnh không dự đoán: cũ 64, mới 64
```

## Bước 4: chạy thật

```
Xong. Tổng thời gian: 10.3 phút. Kết quả: ...\08_du_lieu_thuc_te\bang\tung_luot_ablation
```

- Số file CSV: **60/60**, gồm 2 bộ (clinicdb, colondb) × 3 biến thể (abl_vmamba_only, abl_shape_only, abl_no_guidance) × seed 0–9. Mỗi tổ hợp bộ dữ liệu – biến thể có đủ 10 file.
- Số dòng mỗi file: clinicdb 612, colondb 380, đúng bằng số ảnh của từng bộ.
- Lỗi: không có.
- Tệp gửi Huy: `08_du_lieu_thuc_te/bang/tung_luot_ablation.zip` (439,7 KB).

Chưa tổng hợp và chưa diễn giải kết quả; phần đó Huy làm.
