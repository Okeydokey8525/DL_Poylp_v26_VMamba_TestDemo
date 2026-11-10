# Huấn luyện bổ sung theo nhận xét GVHD (06/11/2026)

Cập nhật 10/11/2026: các lượt dưới đây **đã chạy xong 20 seed** và có trong báo cáo. Mọi notebook giữ đúng tham số huấn luyện của 40 lượt YOLO chính: BG20 880/120, 100 epoch, batch 8, seed 0–19. Mỗi lượt chỉ cần sửa `SEED` ở Cell 0.

| Mô hình | Notebook | Kết quả | Tài liệu |
|---|---|---|---|
| YOLO26s-seg + **C2PSA rộng** (đối chứng cùng số tham số: tầng 10 có 1.830.016 tham số) | `c2psa_rong/kvasir-yolo26s-seg-c2psa-rong.ipynb`, cần thư mục `02_ma_nguon/ultralytics_C2PSA_rong` | `03_ket_qua_huan_luyen/C2PSA_rong/` | `00_tai_lieu_tong_quan/15_ABLATION_VA_C2PSA_RONG.md` |
| **PraNet** 640, có tăng cường | `pranet-new.ipynb` | `05_so_sanh_mo_hinh_khac/PraNet_640/` | `00_tai_lieu_tong_quan/10_SO_SANH_PRANET_UNET.md` |
| **U-Net** 640, có tăng cường | `unet-new.ipynb` | `05_so_sanh_mo_hinh_khac/UNet_640/` | như trên |
| Ba biến thể ablation | `ablation/kvasir-yolo26s-seg-tsvm-ablation.ipynb` | `03_ket_qua_huan_luyen/{Vmamba_only, Shape_only, No_guidance}/` | `00_tai_lieu_tong_quan/15_ABLATION_VA_C2PSA_RONG.md` |

Polyp-PVT, VM-UNet và MambaPSA đã được cân nhắc nhưng **không chạy**; chỉ nêu ở hướng phát triển của báo cáo.

## PraNet, U-Net (pipeline 640)

- **Ảnh:** 640×640, kéo về hình vuông (không letterbox).
- **Tăng cường** (lấy đúng giá trị trong `args.yaml` của YOLO):
  - HSV: h 0,015; s 0,7; v 0,4;
  - lật ngang 0,5; dịch 0,1; co giãn 0,5;
  - mosaic 4 ảnh, tắt ở 10 epoch cuối;
  - không dùng erasing.
- **Kiến trúc, hàm mất mát, bộ tối ưu, lr:** giữ như notebook gốc của nhóm (PraNet biến thể ResNet-50, U-Net 32 kênh gốc).
- **Đánh giá trên val mỗi epoch** (Dice, IoU theo ảnh; ảnh nền tính là đúng nếu không báo điểm nào). Lưu checkpoint có Dice val tốt nhất.
- **Đầu ra mỗi lượt:** `<Mô hình>_640_aug_s<SEED>/` gồm `results.csv` (loss, Dice, IoU, lr, mosaic, thời gian theo epoch), checkpoint tốt nhất, `last.pth`, `tom_tat.txt`.

## Đánh giá

- Theo pixel và topology: `00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py`, `danh_gia_topology.py`. Kiến trúc nạp trực tiếp từ hai notebook ở đây (cell 2), mặc định đánh giá `baseline tsvm pranet640 unet640`, ghi vào `00_tai_lieu_tong_quan/bang/pixel_640/`.
- Dữ liệu khác nguồn: `08_du_lieu_thuc_te/scripts/`.
- Ablation và C2PSA rộng: `00_tai_lieu_tong_quan/scripts/tinh_ablation.py --torch`, `tinh_c2psa_rong.py --torch`.
