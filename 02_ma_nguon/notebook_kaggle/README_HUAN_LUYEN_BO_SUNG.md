# Huấn luyện bổ sung theo nhận xét GVHD (06/11/2026)

Mọi notebook giữ đúng tham số huấn luyện của 40 lượt YOLO chính: BG20 880/120, 100 epoch, batch 8, seed 0–19. Mỗi lượt chỉ cần sửa `SEED` ở Cell 0.

## Thứ tự ưu tiên

| # | Mô hình | Notebook | Cần tải lên Kaggle | Trạng thái kiểm tra |
|---|---|---|---|---|
| 1 | YOLO26s-seg + **C2PSA rộng** (đối chứng cùng số tham số) | `c2psa_rong/kvasir-yolo26s-seg-c2psa-rong.ipynb` | Thư mục `02_ma_nguon/ultralytics_C2PSA_rong` (slug `ultralytics-c2psa-rong`) và dataset BG20 | Đã kiểm tầng 10 trên máy: 1.830.016 tham số |
| 2 | **PraNet** 640, có tăng cường | `pranet-new.ipynb` (đã ghi đè bản 352) | Dataset BG20; bật Internet để tải ResNet-50 | Đã chạy thử 2 epoch trên máy |
| 3 | **U-Net** 640, có tăng cường | `unet-new.ipynb` (đã ghi đè bản 352) | Dataset BG20 | Đã chạy thử 2 epoch trên máy |
| 4 | **Polyp-PVT** (mốc Transformer, mã gốc của tác giả) | `polyp_pvt/polyp-pvt.ipynb` | Dataset BG20; bật Internet (tải mã gốc và PVTv2-B2) | Đã chạy thử 2 epoch trên máy (08/11), bộ nhớ GPU đỉnh 12,9 GiB ở batch 8. Xem mục Polyp-PVT bên dưới |
| 5 | **VM-UNet** (tùy chọn) | `vm_unet/vm-unet.ipynb` | Dataset BG20; bật Internet (cài mamba_ssm, tải mã gốc) | Chưa chạy thử, rủi ro cài đặt cao |
| — | ~~MambaPSA~~ **(BỎ, 07/11/2026)** | `mambapsa/` (giữ làm tư liệu) | — | Không có mã gốc công bố nên không tái hiện; xem `ultralytics_MambaPSA/MAMBAPSA.md` |

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

## Polyp-PVT: chạy trên Kaggle

**Cần chuẩn bị:**
1. Tạo notebook mới, **Import** file `polyp_pvt/polyp-pvt.ipynb`.
2. **Add Input:** dataset BG20 `okeydokey0805/kvasir-yolo-seg-bg20`. Kiểm tra đường dẫn `DATASET_ROOT` ở Cell 0 khớp với Kaggle.
3. **Settings:**
   - Accelerator: **GPU T4 x2** hoặc **GPU P100**. Notebook chỉ dùng 1 GPU.
   - Internet: **On**, vì Cell 2 tải mã gốc từ GitHub và trọng số `pvt_v2_b2.pth` (khoảng 101 MB, đã kiểm link còn sống ngày 08/11).
   - Không cần tải Ultralytics hay dataset nào khác.
4. **Sửa `SEED`** ở Cell 0, rồi chạy bằng **Save Version → Save & Run All (Commit)**, để chạy song song được nhiều lượt.
5. **Tải về:** `runs_PolypPVT_640_aug_s<SEED>.zip` ở tab Output.

**So với mã gốc** (`DengPingFan/Polyp-PVT`):
- **Dùng nguyên:**
  - kiến trúc `lib/pvt.py`, `lib/pvtv2.py` và trọng số ImageNet của PVTv2-B2;
  - hàm mất mát `structure_loss` chép từ `Train.py`;
  - AdamW, lr 1e-4 giữ cố định (bản gốc không giảm lr trong 100 epoch), weight decay 1e-4, cắt gradient 0,5;
  - dự đoán lúc đánh giá là `P1 + P2` qua sigmoid.
- **Đổi để so sánh công bằng với YOLO:**
  - ảnh 640 (gốc 352);
  - batch 8 (gốc 16);
  - tăng cường giống YOLO thay cho huấn luyện đa tỷ lệ {0,75; 1; 1,25};
  - 100 epoch (vòng lặp gốc thực chất chạy 99 epoch);
  - checkpoint tốt nhất chọn theo Dice trên val BG20.

**Rủi ro:**
- Bộ nhớ GPU đỉnh khoảng 12,9 GiB, T4 có 15 GiB. Nếu báo `CUDA out of memory`, chọn P100 (16 GiB). Không giảm batch, vì như vậy lệch điều kiện với YOLO.
- Thời gian một lượt trên Kaggle **chưa đo**: máy laptop 8 GiB phải tràn sang RAM nên không suy ra được. Chạy seed 0 trước, xem `time_s` trong `results.csv`, rồi mới quyết định 5, 10 hay 20 seed.
- Nếu Kaggle không tải được trọng số: tải tay `pvt_v2_b2.pth` từ trang phát hành của `whai362/PVT` (tag v2), thêm làm Dataset, rồi gán `PVT_WEIGHT_DATASET` ở Cell 2.

## Lưu ý

- **Chạy seed 0 trước** để đo thời gian một lượt, rồi mới quyết định chạy 20 hay 10 seed.
- **Kết quả đặt vào thư mục riêng, không ghi đè:**
  - `03_ket_qua_huan_luyen/C2PSA_rong/`, `03_ket_qua_huan_luyen/MambaPSA/`;
  - `05_so_sanh_mo_hinh_khac/<Mô hình>_640/`.
  - Kết quả PraNet/U-Net 352 cũ ở `05_so_sanh_mo_hinh_khac/PraNet`, `UNet` giữ nguyên.
- **Đánh giá theo điểm ảnh:** `danh_gia_pixel.py` hiện nạp kiến trúc PraNet/U-Net từ `99_luu_tru/log_kaggle_cu/` và chạy ở 352. Khi có kết quả 640, cần thêm tùy chọn 640 cho script này.
