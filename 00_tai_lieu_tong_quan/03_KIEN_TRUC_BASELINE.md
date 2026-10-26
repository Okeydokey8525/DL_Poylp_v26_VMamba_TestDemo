# 03. Kiến trúc Baseline: YOLO26s-seg

## Nguồn

- Cấu hình: [`cfg/models/26/yolo26-seg.yaml`](../02_ma_nguon/ultralytics_TSVM_FP32/cfg/models/26/yolo26-seg.yaml), dùng hệ số scale `s` (`[depth 0,50, width 0,50, max_channels 1024]`).
- Trên Kaggle, Baseline được khởi tạo bằng `YOLO("yolo26s-seg.pt")` với Ultralytics 8.4.127 cài từ pip. File YAML trên giống bản trong fork.
- Kích thước tensor dưới đây đo bằng cách dựng lại mô hình (`nc=1`) và chạy một ảnh 640×640. Nguồn: [bang/08_kien_truc_dung_lai.csv](bang/08_kien_truc_dung_lai.csv).

## Bảng tầng (đầu vào 1×3×640×640)

| Tầng | Module | Lấy đầu vào từ | Đầu ra (C×H×W) | Ghi chú |
|---:|---|---|---|---|
| 0 | Conv 3×3, s2 | ảnh | 32×320×320 | P1/2 |
| 1 | Conv 3×3, s2 | 0 | 64×160×160 | P2/4 |
| 2 | C3k2 | 1 | 128×160×160 | |
| 3 | Conv 3×3, s2 | 2 | 128×80×80 | P3/8 |
| 4 | C3k2 | 3 | 256×80×80 | Nhánh tắt P3 sang neck |
| 5 | Conv 3×3, s2 | 4 | 256×40×40 | P4/16 |
| 6 | C3k2 | 5 | 256×40×40 | Nhánh tắt P4 sang neck |
| 7 | Conv 3×3, s2 | 6 | 512×20×20 | P5/32 |
| 8 | C3k2 | 7 | 512×20×20 | |
| 9 | SPPF | 8 | 512×20×20 | |
| **10** | **C2PSA** | 9 | **512×20×20** | **Tầng bị thay ở mô hình đề xuất** |
| 11 | Upsample ×2 | 10 | 512×40×40 | Neck |
| 12 | Concat | 11, 6 | 768×40×40 | |
| 13 | C3k2 | 12 | 256×40×40 | |
| 14 | Upsample ×2 | 13 | 256×80×80 | |
| 15 | Concat | 14, 4 | 512×80×80 | |
| 16 | C3k2 | 15 | 128×80×80 | Đầu ra P3 (nhỏ) |
| 17 | Conv 3×3, s2 | 16 | 128×40×40 | |
| 18 | Concat | 17, 13 | 384×40×40 | |
| 19 | C3k2 | 18 | 256×40×40 | Đầu ra P4 (vừa) |
| 20 | Conv 3×3, s2 | 19 | 256×20×20 | |
| 21 | Concat | 20, 10 | 768×20×20 | Nhận trực tiếp đầu ra tầng 10 |
| 22 | C3k2 | 21 | 512×20×20 | Đầu ra P5 (lớn) |
| 23 | Segment26 | 16, 19, 22 | hộp, lớp, hệ số mặt nạ, prototype | `[nc, 32, 256]` |

Ở mức P4 (tầng 5–6), số kênh thực tế là **256**. Lý do: YAML ghi 512, nhân hệ số width 0,5. Tầng 10 nằm ở mức P5, bản đồ đặc trưng 20×20 khi đầu vào 640×640.

## Tầng 10 của Baseline: C2PSA

`C2PSA` (scale s) có 1 khối PSA. Kênh ẩn c = 256, tổng **990.976** tham số. Khối này tách đặc trưng thành hai nửa và cho một nửa qua attention đa đầu kèm FFN, rồi ghép lại. Mô hình đề xuất giữ nguyên khuôn tách-xử lý-ghép này, chỉ thay phần xử lý ([04](04_KIEN_TRUC_TSVM_FP32.md)).

## Đầu Segment26

YOLO26 chạy ở chế độ `end2end: True` và `reg_max: 1`. Vì vậy loss không có thành phần DFL. Log ghi `l1_loss` cho hồi quy hộp, và có thêm cột `sem_loss` ([07](07_HOI_TU_VA_LOSS.md)). Đầu ra phân đoạn gồm 32 hệ số mặt nạ cho mỗi đối tượng và prototype 256 kênh.

## Quy mô

| | Giá trị | Nguồn |
|---|---:|---|
| Tham số (nc=1, chưa gộp Conv-BN) | **11.434.463** | Dựng lại mô hình; trùng với `best.pt` và benchmark |
| Checkpoint `best.pt` | khoảng 22,27 MiB, lưu **float16** | [bang/07_checkpoint_best_pt.csv](bang/07_checkpoint_best_pt.csv) |

Checkpoint Baseline lưu ở float16 là mặc định của Ultralytics. Baseline không bị lỗi tràn số như TSVM. Kiểm tra 20/20 checkpoint cho thấy mọi tensor đều hữu hạn.
