# Kết quả chạy báo nhầm trên 800 ảnh cecum (máy Lương, 07/11/2026)

- **Script:** `08_du_lieu_thuc_te/scripts/danh_gia_nen_cecum.py`, bản Huy gửi, chép từ `06_bao_cao/` và không sửa.
- **Môi trường:** `C:\venv_kl_gpu\Scripts\python.exe`, torch 2.13.0+cu130, GPU NVIDIA GeForce RTX 5050 Laptop GPU (8 GiB).
- **Phạm vi:** chỉ suy luận. Chạy sau khi lượt ablation ngoài đã xong.

## Bước 2: kiểm tra (`--kiem-tra`)

```
GPU: NVIDIA GeForce RTX 5050 Laptop GPU
Ảnh cecum chưa dùng: 800
Checkpoint có: 80/80
KIỂM TRA: ĐỦ, có thể chạy
```

## Bước 3: đối chiếu môi trường (`--doi-chieu`)

```
ĐỐI CHIẾU: 0/40 ảnh nền lệch kết luận báo nhầm so với bang/10_pixel_tung_anh.csv
```

## Bước 4: chạy thật

```
Tổng thời gian: 27.6 phút
Số seed đã có: {'baseline': 20, 'pranet': 20, 'tsvm': 20, 'unet': 20}
Gần trùng với 160 ảnh nền train (corr64 >= 0.95): 0/800
```

- **Số file CSV trong `nen_cecum/tung_luot/`:** 80/80 (baseline, tsvm, pranet, unet × seed 0–19). Mỗi file có đúng 800 dòng.
- **Có thêm:**
  - `nen_cecum/00_gan_trung_voi_train.csv`;
  - `20seed/06_nen_cecum_tung_seed.csv`;
  - `20seed/07_nen_cecum_thong_ke.csv`.
- **Lỗi:** không có.
- **Tệp gửi Huy:** `nen_cecum.zip` (1,4 MB), kèm hai file 06 và 07.

Không tự tính hay diễn giải kết quả.
