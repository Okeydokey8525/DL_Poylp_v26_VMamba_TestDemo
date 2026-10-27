# 02. Dữ liệu BG20

Mọi con số dưới đây do [scripts/tinh_lai_so_lieu.py](scripts/tinh_lai_so_lieu.py) đếm trực tiếp trên thư mục dữ liệu. Kết quả nằm ở [bang/01_du_lieu_bg20.csv](bang/01_du_lieu_bg20.csv) và [bang/00_kiem_tra_du_lieu.json](bang/00_kiem_tra_du_lieu.json).

## Nguồn

| Thành phần | Nguồn | Vị trí trong repo |
|---|---|---|
| 1.000 ảnh polyp và mặt nạ nhị phân | Kvasir-SEG | `01_du_lieu/tao_BG20/Kvasir-SEG/` |
| Ảnh nền (không có polyp) | Lớp `normal-cecum` của Kvasir v2 | `01_du_lieu/tao_BG20/normal-cecum/` |
| Bộ dữ liệu đã chuyển sang định dạng YOLO | Kết quả của script chuyển đổi | `01_du_lieu/Kvasir_YOLO_SEG_BG20/` |

## Cấu trúc và số lượng (đếm lại)

| | Train | Validation | Tổng |
|---|---:|---:|---:|
| Ảnh polyp | 880 | 120 | 1.000 |
| Ảnh nền (tên bắt đầu `bg_`) | 160 | 40 | 200 |
| **Tổng ảnh** | **1.040** | **160** | **1.200** |
| File nhãn | 1.040 | 160 | 1.200 |
| Nhãn rỗng (0 byte) | 160 | 40 | 200 |
| Nhãn rỗng nhưng không phải ảnh nền | 0 | 0 | 0 |
| Số đối tượng polyp (số dòng polygon) | 936 | **127** | 1.063 |
| Ảnh có từ 2 polyp trở lên | 41 | 7 | 48 |

- Chỉ có một lớp, `0: polyp`. Mọi tọa độ đã chuẩn hóa về [0, 1].
- Mỗi polygon có 10–80 đỉnh ở train và 14–79 đỉnh ở validation. Trung vị là 22 (train) và 26 (validation).
- Ảnh có nhiều kích thước khác nhau: 305 kích thước ở train và 58 ở validation. Kích thước phổ biến nhất là 720×576.

**Cách hiểu "BG20":** 200 ảnh nền bằng 20% của **1.000 ảnh polyp**, không phải 20% của tổng 1.200 ảnh. Tỉ lệ train/validation cuối cùng là 1.040/160, không phải 80/20.

## Kiểm tra tính nhất quán

| Kiểm tra | Kết quả |
|---|---|
| `01_du_lieu/train.txt` (880 ID) trùng khớp với các ảnh polyp trong `images/train` | Đạt |
| `01_du_lieu/val.txt` (120 ID) trùng khớp với các ảnh polyp trong `images/val` | Đạt |
| Danh sách train và validation không giao nhau | Đạt |
| `selected_normal_cecum_train_160.txt` và `selected_normal_cecum_val_40.txt` khớp với các ảnh `bg_*` | Đạt |
| Ảnh nền train và validation không giao nhau | Đạt |
| Ảnh trùng từng byte giữa train và validation | 0 ảnh |
| Mỗi ảnh có đúng một file nhãn cùng tên | Đạt |

## Cách tạo bộ dữ liệu

Script: [`01_du_lieu/scripts_tien_xu_ly/convert_kvasir_with_background_to_yolo_seg.py`](../01_du_lieu/scripts_tien_xu_ly/convert_kvasir_with_background_to_yolo_seg.py). Đây là script **duy nhất** cần chạy để đi từ dữ liệu thô đến bộ dữ liệu sạch. Lệnh chạy ở [13](13_BAN_DO_THU_MUC.md#ghi-chú-sau-khi-sắp-xếp).

Thuật toán chuyển mặt nạ sang polygon (hàm `convert_mask_to_yolo_polygons`) **kế thừa nguyên vẹn** từ bản không nền cũ `99_luu_tru/nhap/Stracth/Du_Lieu/convert_kvasir_to_yolo_seg.py`. Hai bản chỉ khác comment và câu báo lỗi. Bản BG20 bỏ phần thống kê, biểu đồ và ảnh xem trước của bản cũ, và thêm bước chọn ảnh nền, kiểm tra an toàn và chế độ `--dry-run`. Tính cả file thì khoảng 30% dòng code trùng nhau.

1. Đọc hai danh sách cố định `train.txt` (880) và `val.txt` (120).
2. Với mỗi mặt nạ:
   - nhị phân hóa bằng ngưỡng Otsu;
   - đóng hình thái học (morphological close) với kernel 3×3;
   - lấy đường bao ngoài (`RETR_EXTERNAL`) và bỏ vùng có diện tích nhỏ hơn 20 pixel;
   - đơn giản hóa đa giác bằng `approxPolyDP` với ε = 0,002 × chu vi.

   Mỗi đường bao còn lại thành một dòng polygon YOLO.
3. Chọn ngẫu nhiên 200 ảnh normal-cecum với `random.seed(42)`. 160 ảnh đầu vào train, 40 ảnh sau vào validation. Mỗi ảnh nền được thêm tiền tố `bg_` và có nhãn rỗng.
4. Script hiện tại chỉ ghi ra **thư mục mới** (mặc định `generated/Kvasir_YOLO_SEG_BG20_replay`). Nó từ chối ghi đè bộ dữ liệu đang dùng.

## Giới hạn

- **Không có tập test riêng.** Tập validation 160 ảnh vừa dùng để chọn epoch vừa dùng để báo cáo kết quả (xem [11](11_GIOI_HAN_VA_HUONG_PHAT_TRIEN.md)).
- Chưa có bằng chứng về việc tách theo bệnh nhân. Kiểm tra trùng byte không loại trừ được ảnh gần trùng.
- Hai danh sách 880/120 do tác giả Kvasir-SEG cung cấp: chúng đi kèm bản Kaggle debeshjha1/kvasirseg (README: "We have provided train-val split for the fair comparison"), bản gốc ở `DeepLearning/Dataset/Kvasir-SEG_data/`, trùng md5 với `01_du_lieu/train.txt`, `val.txt` (kiểm 27/10/2026).
- Theo [hướng dẫn tái lập trong tài liệu cũ](../99_luu_tru/tai_lieu_cu/archive_doc/28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md), chạy lại script trên OpenCV 4.12.0 và NumPy 2.2.6 cho 999/1.000 nhãn trùng từng ký tự. Bộ tài liệu này **không chạy lại** bước đó.
- Ở bản gốc, `data_bg20.yaml` trỏ tới đường dẫn tuyệt đối trên máy local. Trên Kaggle, notebook tự tạo `data_bg20.yaml` riêng với `nc: 1` ([05](05_CAU_HINH_HUAN_LUYEN.md)).
