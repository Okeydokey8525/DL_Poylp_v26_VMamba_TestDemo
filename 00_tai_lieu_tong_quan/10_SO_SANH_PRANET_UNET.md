# 10. So sánh với PraNet và U-Net (đánh giá theo pixel)

> **Cập nhật 10/11/2026:** PraNet và U-Net trong báo cáo là bản **huấn luyện lại ở ảnh 640×640, có tăng cường dữ liệu giống YOLO** (theo nhận xét phản biện II.4), 20 seed. Số trong file này khớp Bảng 4.8 của bản Word cuối.

Số liệu do [scripts/danh_gia_pixel.py](scripts/danh_gia_pixel.py) tính (suy luận trên GPU RTX 5050 Laptop). Kết quả:
- [bang/pixel_640/10_pixel_tung_anh.csv](bang/pixel_640/10_pixel_tung_anh.csv): 4 mô hình × 20 seed × 160 ảnh;
- [bang/pixel_640/11_pixel_tung_seed.csv](bang/pixel_640/11_pixel_tung_seed.csv);
- [bang/pixel_640/12_pixel_thong_ke.csv](bang/pixel_640/12_pixel_thong_ke.csv);
- ma trận nhầm lẫn theo ảnh: [bang/pixel_640/20_ma_tran_anh_tung_seed.csv](bang/pixel_640/20_ma_tran_anh_tung_seed.csv), [20b_ma_tran_anh_tong_hop.csv](bang/pixel_640/20b_ma_tran_anh_tong_hop.csv);
- log: [bang/pixel_640/_log_pixel.txt](bang/pixel_640/_log_pixel.txt).

Trong các bảng, PraNet và U-Net mang khóa `pranet640`, `unet640`. Hai dòng YOLO giống hệt bản đánh giá trước (đã đối chiếu, chênh 0).

## Vì sao phải đánh giá theo pixel

PraNet và U-Net là mô hình **phân đoạn ngữ nghĩa**: chúng cho ra một mặt nạ xác suất cho cả ảnh, không có từng đối tượng kèm điểm tin cậy. Vì vậy không tính được mAP cho chúng theo cùng cách với YOLO. Cả 4 mô hình được đánh giá bằng **cùng một bộ chỉ số theo pixel**: Dice (bằng F1 theo pixel), IoU, Precision và Recall. Bảng mAP của cặp YOLO ở [06](06_KET_QUA_20_SEED.md) giữ nguyên.

## Các mô hình

| Mô hình | Checkpoint | Cách suy luận |
|---|---|---|
| YOLO26s-seg | `best.pt` (chọn theo fitness box+mask), 20 seed | imgsz 640, conf 0,25, iou 0,7, `retina_masks=True`, gộp mọi mặt nạ của ảnh thành một |
| YOLO26s-seg + TSVM FP32 | như trên | như trên |
| PraNet (biến thể ResNet-50) | `05_so_sanh_mo_hinh_khac/PraNet_640/PraNet_640_aug_s*/pranet_best_s*.pth` (Dice val tốt nhất mỗi epoch) | Kéo về 640×640, chuẩn hóa ImageNet, lấy nhánh `lateral_map_s2`, ngưỡng 0,5 |
| U-Net (32 kênh gốc) | `05_so_sanh_mo_hinh_khac/UNet_640/UNet_640_aug_s*/best_unet_s*.pth` | Kéo về 640×640, chia 255, ngưỡng 0,5 |

Kiến trúc PraNet và U-Net được nạp **trực tiếp từ mã trong notebook huấn luyện** `02_ma_nguon/notebook_kaggle/{pranet-new,unet-new}.ipynb`. Cả 20/20 checkpoint mỗi mô hình nạp khớp hoàn toàn (`strict=True`).

Huấn luyện PraNet/U-Net 640 (xem [README_HUAN_LUYEN_BO_SUNG.md](../02_ma_nguon/notebook_kaggle/README_HUAN_LUYEN_BO_SUNG.md)): ảnh 640×640, 100 epoch, batch 8, seed 0–19, tăng cường lấy đúng giá trị trong `args.yaml` của YOLO (HSV, lật ngang, dịch, co giãn, mosaic tắt ở 10 epoch cuối). Kiến trúc, hàm mất mát, bộ tối ưu giữ như notebook gốc.

## Giao thức đánh giá

- **Nhãn chuẩn chính:** mặt nạ vẽ từ polygon YOLO ở **độ phân giải gốc** của ảnh, đúng nhãn mà cả 4 mô hình được huấn luyện.
- **Nhãn chuẩn phụ:** mặt nạ gốc của Kvasir-SEG (cột `raw_*`).
- Mọi dự đoán được đưa về kích thước ảnh gốc trước khi so.
- Chỉ số tính **trên từng ảnh** cho 120 ảnh có polyp, lấy trung bình trong mỗi seed, rồi tính mean ± SD qua 20 seed. Ảnh có polyp mà mô hình không dự đoán pixel nào thì Dice, IoU, Precision, Recall của ảnh đó bằng 0.
- 40 ảnh nền: tỉ lệ ảnh có ít nhất một pixel bị dự đoán là polyp.
- `dice_micro`: Dice tính gộp pixel của cả 120 ảnh, cho ảnh polyp lớn trọng số lớn hơn.

## Kết quả (mean ± SD, 20 seed)

| Mô hình | Dice | IoU | Precision | Recall | Dice gộp pixel | Ảnh nền báo nhầm (%) |
|---|---:|---:|---:|---:|---:|---:|
| YOLO26s-seg | 0,8486 ± 0,0171 | 0,7927 ± 0,0170 | 0,8585 ± 0,0170 | 0,8703 ± 0,0193 | 0,8659 ± 0,0313 | 1,2 ± 1,9 |
| YOLO26s-seg + TSVM | 0,8540 ± 0,0129 | 0,7998 ± 0,0129 | 0,8632 ± 0,0173 | 0,8730 ± 0,0112 | 0,8785 ± 0,0243 | 1,5 ± 2,1 |
| **PraNet 640** | **0,8856 ± 0,0053** | **0,8212 ± 0,0073** | **0,9044 ± 0,0111** | **0,9064 ± 0,0080** | **0,8846 ± 0,0098** | 2,8 ± 0,8 |
| U-Net 640 | 0,6909 ± 0,0261 | 0,5713 ± 0,0283 | 0,7836 ± 0,0258 | 0,7165 ± 0,0252 | 0,7023 ± 0,0263 | 57,4 ± 6,9 |

Nguồn: `bang/pixel_640/12_pixel_thong_ke.csv`.

### So sánh ghép cặp TSVM với từng mô hình (cùng seed, n = 20)

| So với | Chỉ số | Δ (TSVM − mô hình kia) | Paired t p | Wilcoxon p | TSVM cao hơn |
|---|---|---:|---:|---:|---:|
| YOLO26s-seg | Dice | +0,0054 | 0,260 | 0,245 | 13/20 |
| | IoU | +0,0071 | 0,130 | 0,114 | 14/20 |
| | Ảnh nền báo nhầm | +0,25 điểm % | 0,694 | 0,793 | |
| PraNet 640 | Dice | **−0,0316** | **< 0,001** | **< 0,001** | 0/20 |
| | IoU | **−0,0214** | **< 0,001** | **< 0,001** | 3/20 |
| | Recall | **−0,0333** | **< 0,001** | **< 0,001** | 0/20 |
| | Ảnh nền báo nhầm | **−1,25 điểm %** | **0,021** | **0,025** | |
| U-Net 640 | Dice | **+0,1631** | **< 0,001** | **< 0,001** | 20/20 |
| | Ảnh nền báo nhầm | **−55,9 điểm %** | **< 0,001** | **< 0,001** | |

## Diễn giải

1. **So với mô hình gốc YOLO26s-seg:** theo pixel, TSVM có xu hướng tăng nhẹ (Dice +0,005, IoU +0,007, cao hơn ở 13–14/20 seed) và SD nhỏ hơn, nhưng **không có ý nghĩa thống kê**. Nhất quán với kết luận theo mAP ở [06](06_KET_QUA_20_SEED.md).
2. **So với PraNet 640:** khi được huấn luyện cùng độ phân giải và tăng cường, **PraNet cao hơn cả hai mô hình YOLO ở mọi độ đo theo pixel**. TSVM thấp hơn PraNet về Dice ở cả 20/20 seed. Điểm duy nhất TSVM tốt hơn là báo nhầm ảnh nền ít hơn (1,5% so với 2,8%).
3. **So với U-Net 640:** hai mô hình YOLO và PraNet đều hơn hẳn U-Net. U-Net 640 báo nhầm khoảng 57% ảnh nền.
4. **Điểm yếu của YOLO theo pixel:** ở ngưỡng conf 0,25, YOLO **không dự đoán gì** trên trung bình khoảng 6,5/120 ảnh có polyp (mô hình gốc 6,45, TSVM 6,65; ít nhất 2, nhiều nhất 10 ảnh mỗi seed). Con số này ở PraNet 640 và U-Net 640 đều là 0,10 (cột `polyp_imgs_no_pred`). Mỗi ảnh bỏ sót có Dice bằng 0, kéo Dice trung bình của YOLO xuống, và là một phần chênh lệch Recall với PraNet.

## Giới hạn của phép so sánh

- PraNet và U-Net được huấn luyện cùng độ phân giải và tăng cường dữ liệu với YOLO, nhưng vẫn giữ hàm mất mát, bộ tối ưu riêng và chọn checkpoint theo Dice (YOLO chọn theo fitness box+mask).
- PraNet ở đây dùng **ResNet-50**, khác bản gốc dùng Res2Net-50, phần Aggregation đã chỉnh lại. Không so trực tiếp với số trong bài báo gốc.
- Cả 4 mô hình chọn checkpoint trên **cùng tập validation** dùng để báo cáo, nên có thiên lệch lựa chọn. Không có tập test độc lập.
- Ngưỡng cố định (conf 0,25 cho YOLO, xác suất 0,5 cho PraNet và U-Net) chưa tối ưu riêng cho từng mô hình.

## Hình

Thư mục `06_bao_cao/hinh/ket_qua_20seed_640/{vi,en}/`:
- `p01_cot_kep_pixel`: Dice/IoU/P/R của 4 mô hình;
- `p02_diem_dice_tung_seed`: Dice từng seed;
- `p03_bao_nham_anh_nen`: tỉ lệ ảnh nền bị báo nhầm;
- `p04_bao_nham_cecum`: báo nhầm trên 800 ảnh manh tràng chưa dùng;
- `p05_loi_cap_anh`: ma trận nhầm lẫn theo ảnh;
- `q01_minh_hoa_dinh_tinh`: ảnh minh họa seed 0 (Hình 4.10 của bản Word).
