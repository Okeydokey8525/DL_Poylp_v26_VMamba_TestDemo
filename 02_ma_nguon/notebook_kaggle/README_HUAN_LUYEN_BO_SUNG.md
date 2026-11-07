# Huấn luyện bổ sung theo nhận xét GVHD (06/11/2026)

Mọi notebook giữ đúng tham số huấn luyện của 40 lượt YOLO chính: BG20 880/120, 100 epoch, batch 8, seed 0–19. Mỗi lượt chỉ cần sửa `SEED` ở Cell 0.

## Thứ tự ưu tiên

| # | Mô hình | Notebook | Cần tải lên Kaggle | Trạng thái kiểm tra |
|---|---|---|---|---|
| 1 | YOLO26s-seg + **C2PSA rộng** (đối chứng cùng số tham số) | `c2psa_rong/kvasir-yolo26s-seg-c2psa-rong.ipynb` | Thư mục `02_ma_nguon/ultralytics_C2PSA_rong` (slug `ultralytics-c2psa-rong`) và dataset BG20 | Đã kiểm tầng 10 trên máy: 1.830.016 tham số |
| 2 | **PraNet** 640, có tăng cường | `pranet-new.ipynb` (đã ghi đè bản 352) | Dataset BG20; bật Internet để tải ResNet-50 | Đã chạy thử 2 epoch trên máy |
| 3 | **U-Net** 640, có tăng cường | `unet-new.ipynb` (đã ghi đè bản 352) | Dataset BG20 | Đã chạy thử 2 epoch trên máy |
| 4 | YOLO26s-seg + **MambaPSA** (tái hiện theo mô tả bài báo) | `mambapsa/kvasir-yolo26s-seg-mambapsa.ipynb` | Thư mục `02_ma_nguon/ultralytics_MambaPSA` (slug `ultralytics-mambapsa`) | Đã kiểm tầng 10 và chạy xuôi/ngược trên máy; chưa train thử |
| 5 | **Polyp-PVT** | `polyp_pvt/polyp-pvt.ipynb` | Dataset BG20; bật Internet (tải mã gốc và PVTv2-B2) | Chưa chạy thử |
| 6 | **VM-UNet** | `vm_unet/vm-unet.ipynb` | Dataset BG20; bật Internet (cài mamba_ssm, tải mã gốc) | Chưa chạy thử, rủi ro cài đặt cao |

## PraNet, U-Net, Polyp-PVT, VM-UNet (pipeline 640 dùng chung)

- **Ảnh:** 640×640, kéo về hình vuông (không letterbox).
- **Tăng cường** (lấy đúng giá trị trong `args.yaml` của YOLO):
  - HSV: h 0,015; s 0,7; v 0,4;
  - lật ngang 0,5; dịch 0,1; co giãn 0,5;
  - mosaic 4 ảnh, tắt ở 10 epoch cuối;
  - không dùng erasing.
- **Kiến trúc, hàm mất mát, bộ tối ưu, lr:** giữ như notebook cũ. Polyp-PVT và VM-UNet theo bài gốc.
- **Đánh giá trên val mỗi epoch** (Dice, IoU theo ảnh; ảnh nền tính là đúng nếu không báo điểm nào). Lưu checkpoint có Dice val tốt nhất.
- **Đầu ra:** `runs/<Mô hình>_640_aug_s<SEED>/`, gồm `results.csv` (loss, Dice, IoU, lr, mosaic, thời gian theo epoch), checkpoint tốt nhất, `last.pth`, `tom_tat.txt`. Cell cuối nén thành `runs_<RUN_NAME>.zip`.

## Lưu ý

- **Chạy seed 0 trước** để đo thời gian một lượt, rồi mới quyết định chạy 20 hay 10 seed.
- **Kết quả đặt vào thư mục riêng, không ghi đè:**
  - `03_ket_qua_huan_luyen/C2PSA_rong/`, `03_ket_qua_huan_luyen/MambaPSA/`;
  - `05_so_sanh_mo_hinh_khac/<Mô hình>_640/`.
  - Kết quả PraNet/U-Net 352 cũ ở `05_so_sanh_mo_hinh_khac/PraNet`, `UNet` giữ nguyên.
- **Đánh giá theo điểm ảnh:** `danh_gia_pixel.py` hiện nạp kiến trúc PraNet/U-Net từ `99_luu_tru/log_kaggle_cu/` và chạy ở 352. Khi có kết quả 640, cần thêm tùy chọn 640 cho script này.
