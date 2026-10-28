# 10. So sánh với PraNet và U-Net (đánh giá theo pixel)

> **Cập nhật 28/10/2026:** số trong file này tính trên **20 seed** và là **bộ số dùng trong báo cáo**. Bộ 10 seed (chỉ đối chiếu) ở [06b_KET_QUA_10_SEED.md](06b_KET_QUA_10_SEED.md).

Cập nhật 26/10/2026. Số liệu do [scripts/danh_gia_pixel.py](scripts/danh_gia_pixel.py) tính, chạy trên GPU RTX 5050 trong 7,2 phút. Kết quả nằm ở:
- [bang/10_pixel_tung_anh.csv](bang/10_pixel_tung_anh.csv): 12.800 dòng (4 mô hình × 20 seed × 160 ảnh);
- [bang/11_pixel_tung_seed.csv](bang/11_pixel_tung_seed.csv);
- [bang/12_pixel_thong_ke.csv](bang/12_pixel_thong_ke.csv);
- log chạy: [bang/_log_danh_gia_pixel.txt](bang/_log_danh_gia_pixel.txt).

## Vì sao phải đánh giá theo pixel

PraNet và U-Net là mô hình **phân đoạn ngữ nghĩa**: chúng cho ra một mặt nạ xác suất cho cả ảnh, không có từng đối tượng kèm điểm tin cậy. Vì vậy không thể tính mAP cho chúng theo cùng cách với YOLO. Để so sánh công bằng, cả 4 mô hình được đánh giá bằng **cùng một bộ chỉ số theo pixel**: Dice (bằng F1 theo pixel), IoU, Precision và Recall. Bảng mAP của cặp YOLO ở [06](06_KET_QUA_20_SEED.md) vẫn giữ nguyên.

## Các mô hình

| Mô hình | Checkpoint | Cách suy luận |
|---|---|---|
| YOLO26s-seg | `best.pt` (chọn theo fitness box+mask), 20 seed | imgsz 640, conf 0,25, iou 0,7, `retina_masks=True`, gộp mọi mặt nạ của ảnh thành một |
| YOLO26s-seg + TSVM FP32 | như trên | như trên |
| PraNet (biến thể ResNet-50) | `pranet_best_s*.pth` (Dice validation tốt nhất, đánh giá mỗi 5 epoch) | Resize 352×352, chuẩn hóa ImageNet, lấy nhánh `lateral_map_s2`, ngưỡng 0,5 |
| U-Net (32 kênh gốc) | `best_unet_s*.pth` (Dice validation tốt nhất mỗi epoch) | Resize 352×352, chia 255, ngưỡng 0,5 |

Kiến trúc PraNet và U-Net được nạp **trực tiếp từ mã trong notebook huấn luyện** (`99_luu_tru/log_kaggle_cu/*.ipynb`). Cả 20/20 checkpoint mỗi mô hình đều nạp khớp hoàn toàn (`strict=True`).

## Giao thức đánh giá

- **Nhãn chuẩn chính:** mặt nạ vẽ từ polygon YOLO ở **độ phân giải gốc** của ảnh. Đây chính là nhãn mà cả 4 mô hình được huấn luyện.
- **Nhãn chuẩn phụ:** mặt nạ gốc của Kvasir-SEG (cột `raw_*`). Kết quả gần như trùng với nhãn chính, chênh lệch Dice không quá 0,001.
- Mọi dự đoán được đưa về kích thước ảnh gốc trước khi so.
- Chỉ số được tính **trên từng ảnh** cho 120 ảnh có polyp, lấy trung bình trong mỗi seed, rồi tính mean ± SD qua 20 seed. Nếu ảnh có polyp mà mô hình không dự đoán pixel nào thì Dice, IoU, Precision và Recall của ảnh đó đều bằng 0.
- Với 40 ảnh nền: tính tỉ lệ ảnh có ít nhất một pixel bị dự đoán là polyp.
- `dice_micro` là Dice tính gộp pixel của cả 120 ảnh. Chỉ số này cho ảnh polyp lớn trọng số lớn hơn.

## Kết quả (mean ± SD, 20 seed)

| Mô hình | Dice | IoU | Precision | Recall | Dice gộp pixel | Ảnh nền báo nhầm (%) |
|---|---:|---:|---:|---:|---:|---:|
| YOLO26s-seg | 0,8486 ± 0,0171 | 0,7927 ± 0,0170 | 0,8585 ± 0,0170 | 0,8703 ± 0,0193 | 0,8659 ± 0,0313 | 1,2 ± 1,9 |
| **YOLO26s-seg + TSVM** | **0,8540 ± 0,0129** | **0,7998 ± 0,0129** | 0,8632 ± 0,0173 | 0,8730 ± 0,0112 | **0,8785 ± 0,0243** | 1,5 ± 2,1 |
| PraNet (ResNet-50) | **0,8541 ± 0,0068** | 0,7785 ± 0,0063 | **0,8687 ± 0,0117** | **0,8881 ± 0,0145** | 0,8715 ± 0,0060 | **0,8 ± 1,2** |
| U-Net | 0,7097 ± 0,0221 | 0,6069 ± 0,0221 | 0,7964 ± 0,0213 | 0,7167 ± 0,0327 | 0,7412 ± 0,0185 | 20,4 ± 6,4 |

### So sánh ghép cặp TSVM với từng mô hình (cùng seed)

| So với | Chỉ số | Δ (TSVM − mô hình kia) | Paired t p | Wilcoxon p | TSVM cao hơn |
|---|---|---:|---:|---:|---:|
| YOLO26s-seg | Dice | +0,0054 | 0,260 | 0,246 | 13/20 |
| | IoU | +0,0071 | 0,130 | 0,114 | 14/20 |
| | Ảnh nền báo nhầm | +0,25 điểm % | 0,694 | 0,793 | |
| PraNet | Dice | −0,0001 | 0,982 | 0,927 | 12/20 |
| | IoU | **+0,0213** | **< 0,001** | **< 0,001** | 19/20 |
| | Recall | **−0,0151** | **0,002** | **0,001** | 5/20 |
| U-Net | Dice | **+0,1443** | **< 0,001** | **< 0,001** | 20/20 |
| | Ảnh nền báo nhầm | **−18,9 điểm %** | **< 0,001** | **< 0,001** | |

## Diễn giải

1. **So với đối chứng YOLO26s-seg:** theo pixel, TSVM vẫn cho xu hướng tăng nhẹ (Dice +0,005, IoU +0,007, tăng ở 13–14/20 seed) và SD nhỏ hơn. Nhưng **chưa có ý nghĩa thống kê**. Điều này nhất quán với kết luận theo mAP ở [06](06_KET_QUA_20_SEED.md).
2. **So với PraNet:** Dice trung bình gần như bằng nhau. TSVM có **IoU cao hơn rõ** (19/20 seed, p < 0,001), cho thấy khi đã khoanh vùng thì biên mặt nạ khớp sát hơn. Ngược lại, PraNet có **Recall cao hơn**, và PraNet rất ổn định giữa các seed (SD Dice 0,007).
3. **So với U-Net:** cả hai mô hình YOLO và PraNet đều hơn hẳn U-Net. U-Net còn báo nhầm khoảng 20% ảnh nền.
4. **Điểm yếu của YOLO theo pixel:** ở ngưỡng conf 0,25, YOLO **không dự đoán gì** trên trung bình khoảng 6,5/120 ảnh có polyp (đối chứng 6,45, TSVM 6,65; ít nhất 2, nhiều nhất 10 ảnh mỗi seed). Con số này ở PraNet là 0,95 và ở U-Net là 2,5 (cột `polyp_imgs_no_pred`). Mỗi ảnh bỏ sót như vậy có Dice bằng 0, kéo trung bình Dice của YOLO xuống. Đây là lý do Dice gộp pixel của YOLO cao hơn Dice trung bình theo ảnh.

## Giới hạn của phép so sánh

- **Thiết lập huấn luyện khác nhau:**
  - YOLO: 640 px, có tăng cường dữ liệu (mosaic, HSV, lật…), AdamW lr0 0,001, khởi tạo từ trọng số COCO.
  - PraNet: 352 px, không tăng cường dữ liệu, Adam lr 1e-4, backbone tiền huấn luyện ImageNet.
  - U-Net: 352 px, không tăng cường dữ liệu, khởi tạo ngẫu nhiên.

  Kết quả phản ánh các cấu hình cụ thể này, không phải giới hạn tối đa của từng kiến trúc.
- PraNet ở đây dùng **ResNet-50**, khác bản gốc dùng Res2Net-50, và phần Aggregation đã được chỉnh lại. Không so trực tiếp với số liệu trong bài báo gốc.
- Cả 4 mô hình đều chọn checkpoint trên **cùng tập validation** dùng để báo cáo, nên có thiên lệch lựa chọn. Không có tập test độc lập.
- Ngưỡng cố định (conf 0,25 cho YOLO, xác suất 0,5 cho PraNet và U-Net) chưa được tối ưu riêng cho từng mô hình.
- Kết quả trên GPU khớp với CPU: kiểm tra trên PraNet seed 0 cho mặt nạ trùng 100% pixel.

## Hình

Thư mục `06_bao_cao/hinh/{vi,en}/`:
- `p01_cot_kep_pixel`: Dice/IoU/P/R của 4 mô hình;
- `p02_diem_dice_tung_seed`: Dice từng seed;
- `p03_bao_nham_anh_nen`: tỉ lệ ảnh nền bị báo nhầm;
- `q01_minh_hoa_dinh_tinh`: ảnh minh họa seed 0.
