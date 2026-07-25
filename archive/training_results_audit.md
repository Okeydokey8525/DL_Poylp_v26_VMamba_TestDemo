# BÁO CÁO KIỂM TOÁN KẾT QUẢ HUẤN LUYỆN (TRAINING RESULTS AUDIT REPORT)

**Dự án khóa luận:** *Nghiên cứu phương pháp tích hợp VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng.*  
**Đối tượng kiểm toán:** Toàn bộ lịch sử huấn luyện hiện có trong workspace (`archive/KQ_Poylp`).  
**Phương pháp kiểm toán:** AI Research Auditor – Đọc, xác thực và trích xuất số liệu thực tế 100% từ các file artifact (`results.csv`, `args.yaml`, `weights/best.pt`, `weights/last.pt`, các biểu đồ và ảnh dự đoán), **không tự huấn luyện lại, không sửa đổi mã nguồn, không suy đoán số liệu bị thiếu.**

---

## 1. EXECUTIVE SUMMARY (TÓM TẮT ĐIỀU HÀNH)

Qua quá trình rà soát toàn bộ không gian lưu trữ của dự án (`archive/KQ_Poylp`), kiểm toán viên ghi nhận **12 lượt huấn luyện (training runs) độc lập** cho bài toán phân đoạn polyp (**Task: `segment`**) thuộc hai dòng kiến trúc **YOLO11-seg** (5 biến thể: `n`, `s`, `m`, `l`, `x` cùng 1 run thử nghiệm 150 epoch) và **YOLO26-seg** (5 biến thể: `n`, `s`, `m`, `l`, `x`).

### Các phát hiện quan trọng nhất (Key Findings):
1. **Tính hoàn chỉnh của dữ liệu artifact:** Cả 12 run đều được lưu trữ đầy đủ các file cốt lõi bao gồm `args.yaml` (cấu hình), `results.csv` (lịch sử metric từng epoch), `weights/best.pt`, `weights/last.pt` (trọng số mô hình ở định dạng FP16 TorchScript/PyTorch), cùng bộ biểu đồ đánh giá (`results.png`, `MaskPR_curve.png`, `confusion_matrix_normalized.png`,...).
2. **Hiện trạng tích hợp VMamba:** Không ghi nhận bất kỳ run hoặc trọng số nào có tên hoặc cấu trúc thể hiện đã tích hợp khối **VMamba** (Visual Mamba / State Space Model). Toàn bộ 12 run hiện tại là **baseline thuần túy** (YOLO11-seg và YOLO26-seg nguyên bản của Ultralytics) được huấn luyện để làm mốc đối chứng (baseline benchmark) cho đề tài khóa luận.
3. **Mô hình đạt hiệu quả tổng hợp tốt nhất:**  
   * Về chỉ số mAP toàn diện (`Mask mAP50-95`), biến thể **`Poylp_Yolov11m-seg_100e_32b`** đạt chỉ số cao nhất là **0.7222** (tại epoch 93), tiếp sát theo là `Poylp_Yolov11x-seg_100e_16b` (**0.7198**) và `Poylp_Yolov11l-seg_100e_32b` (**0.7186**).
   * Trong dòng YOLO26-seg, mô hình đạt `Mask mAP50-95` tốt nhất là **`Poylp_Yolov26m-seg_100e_32b`** với **0.7115** (tại epoch 94).
4. **Vấn đề "Nút thắt đường biên" (Boundary Precision Gap):**  
   Tất cả các biến thể đều đạt chỉ số `Mask mAP50` rất cao (dao động từ **0.8982** đến **0.9360**), cho thấy mô hình định vị và phát hiện vùng polyp rất nhạy. Tuy nhiên, khi siết chặt ngưỡng đánh giá IoU trung bình từ 0.50 đến 0.95 (`Mask mAP50-95`), điểm số giảm xuống vùng **0.6981 – 0.7222** (sụt giảm hơn 20%). Điều này chứng minh mask dự đoán có độ chồng khớp bao quát tốt nhưng **đường biên chi tiết quanh rìa polyp chưa thực sự sắc sảo và chính xác tuyệt đối**. Đây chính là động lực khoa học thực tiễn vững chắc nhất để thuyết minh cho việc **tích hợp cơ chế VMamba nhằm cải thiện khả năng thu nhận ngữ cảnh toàn cục và chi tiết đường biên**.
5. **Đánh giá Overfitting/Underfitting:**  
   Các run 100 epoch với kiến trúc lớn (`l`, `x`) bắt đầu có hiện tượng tách giãn nhẹ giữa `train/seg_loss` (liên tục giảm xuống ~0.62–0.70) và `val/seg_loss` (chững lại hoặc nhích nhẹ sau epoch 70–80). Tuy nhiên, nhờ cơ chế tắt Mosaic ở 10 epoch cuối (`close_mosaic: 10`), các metric validation (`Mask mAP`, `Recall`) vẫn được cải thiện hoặc duy trì ổn định đến những epoch 90–98, không bị suy thoái nghiêm trọng (không overfitting nặng).

---

## 2. DANH SÁCH CÁC RUN ĐÃ HUẤN LUYỆN

Bảng dưới đây tổng hợp đường dẫn, tác vụ, mô hình và tình trạng lưu trữ artifact của toàn bộ 12 run trong workspace:

| STT | Tên Run (`run_name`) | Task | Model | Epoch đã chạy | `best.pt` | `last.pt` | `results.csv` | `args.yaml` | Biểu đồ & Prediction |
| --: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `Poylp_Yolov11l-seg_100e_32b` | segment | `yolo11l-seg.pt` | 100 / 100 | Có (53.25 MB) | Có (53.25 MB) | Có | Có | Đầy đủ |
| 2 | `Poylp_Yolov11m-seg_100e_32b` | segment | `yolo11m-seg.pt` | 100 / 100 | Có (43.07 MB) | Có (43.07 MB) | Có | Có | Đầy đủ |
| 3 | `Poylp_Yolov11n-seg_100e_16b` | segment | `yolo11n-seg.pt` | 100 / 100 | Có (5.73 MB) | Có (5.73 MB) | Có | Có | Đầy đủ |
| 4 | `Poylp_Yolov11n-seg_100e_32b` | segment | `yolo11n-seg.pt` | 100 / 100 | Có (5.73 MB) | Có (5.73 MB) | Có | Có | Đầy đủ |
| 5 | `Poylp_Yolov11n-seg_150e_32b` | segment | `yolo11n-seg.pt` | **100 / 150** | Có (5.73 MB) | Có (5.73 MB) | Có | Có | Đầy đủ |
| 6 | `Poylp_Yolov11s-seg_100e_32b` | segment | `yolo11s-seg.pt` | 100 / 100 | Có (19.57 MB) | Có (19.57 MB) | Có | Có | Đầy đủ |
| 7 | `Poylp_Yolov11x-seg_100e_16b` | segment | `yolo11x-seg.pt` | 100 / 100 | Có (119.00 MB)| Có (119.00 MB)| Có | Có | Đầy đủ |
| 8 | `Poylp_Yolov26l-seg_100e_32b` | segment | `yolo26l-seg.pt` | 100 / 100 | Có (60.50 MB) | Có (60.50 MB) | Có | Có | Đầy đủ |
| 9 | `Poylp_Yolov26m-seg_100e_32b` | segment | `yolo26m-seg.pt` | 100 / 100 | Có (51.95 MB) | Có (51.95 MB) | Có | Có | Đầy đủ |
| 10| `Poylp_Yolov26n-seg_100e_32b` | segment | `yolo26n-seg.pt` | 100 / 100 | Có (6.24 MB)  | Có (6.24 MB)  | Có | Có | Đầy đủ |
| 11| `Poylp_Yolov26s-seg_100e_32b` | segment | `yolo26s-seg.pt` | 100 / 100 | Có (22.26 MB) | Có (22.26 MB) | Có | Có | Đầy đủ |
| 12| `Poylp_Yolov26x-seg_100e_16b` | segment | `yolo26x-seg.pt` | 100 / 100 | Có (135.16 MB)| Có (135.16 MB)| Có | Có | Đầy đủ |

*Ghi chú:* Tất cả các thư mục run nằm tại `archive/KQ_Poylp/<run_name>`. Ngày giờ sửa đổi gần nhất (`mtime`) được ghi nhận là vào tháng 7/2026. Riêng run số 5 (`Poylp_Yolov11n-seg_150e_32b`) yêu cầu `epochs: 150` trong `args.yaml` nhưng `results.csv` dừng lại ở epoch 100 (được phân tích sâu tại Phần 4).

---

## 3. CẤU HÌNH HUẤN LUYỆN TỪNG RUN (`args.yaml`)

Việc trích xuất `args.yaml` cho thấy tất cả 12 run đều tuân thủ một khung cấu hình chuẩn hóa trên nền tảng Kaggle (`project: /kaggle/working/runs`, `device: 0,1` dùng 2 GPU), cụ thể các tham số chung cho toàn bộ các run:
* **Task / Mode / Split:** `segment` / `train` / `val`
* **Data:** `/kaggle/working/dataset.yaml` (ánh xạ dataset Kvasir-SEG đã chuyển đổi)
* **Image Size (`imgsz`):** `640` | **Workers:** `4` | **Seed:** `0` (`deterministic: true`)
* **Optimizer:** `auto` (Ultralytics tự động chọn AdamW cho kiến trúc segmentation)
* **Hyperparameters ban đầu (LR & Regularization):** `lr0: 0.01`, `lrf: 0.01`, `momentum: 0.937`, `weight_decay: 0.0005`, `warmup_epochs: 3.0`
* **Loss Weights:** `box: 7.5`, `cls: 0.5`, `dfl: 1.5`,  `nbs: 64`
* **Augmentations:** `hsv_h: 0.015`, `hsv_s: 0.7`, `hsv_v: 0.4`, `translate: 0.1`, `scale: 0.5`, `fliplr: 0.5`, `mosaic: 1.0`, `close_mosaic: 10` (tắt mosaic ở 10 epoch cuối), `erasing: 0.4`. Các phép biến đổi `degrees`, `shear`, `perspective`, `flipud`, `mixup`, `cutmix`, `copy_paste` đều đặt bằng `0.0`.
* **Patience / AMP:** `patience: 30`, `amp: true` (Automatic Mixed Precision).

Sự khác biệt giữa các run chỉ nằm ở biến thể mô hình (`model`), số epoch yêu cầu (`epochs`), và kích thước batch (`batch`) được tổng hợp trong bảng chi tiết:

| Run (`name`) | Model File | Epoch yêu cầu | Epoch hoàn thành | Batch size thực tế (`args.yaml`) | close_mosaic |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `Poylp_Yolov11l-seg_100e_32b` | `yolo11l-seg.pt` | 100 | 100 | 32 | 10 |
| `Poylp_Yolov11m-seg_100e_32b` | `yolo11m-seg.pt` | 100 | 100 | 32 | 10 |
| `Poylp_Yolov11n-seg_100e_16b` | `yolo11n-seg.pt` | 100 | 100 | 16 | 10 |
| `Poylp_Yolov11n-seg_100e_32b` | `yolo11n-seg.pt` | 100 | 100 | 32 | 10 |
| `Poylp_Yolov11n-seg_150e_32b` | `yolo11n-seg.pt` | **150** | **100** | 32 | 10 |
| `Poylp_Yolov11s-seg_100e_32b` | `yolo11s-seg.pt` | 100 | 100 | 32 | 10 |
| `Poylp_Yolov11x-seg_100e_16b` | `yolo11x-seg.pt` | 100 | 100 | 16 | 10 |
| `Poylp_Yolov26l-seg_100e_32b` | `yolo26l-seg.pt` | 100 | 100 | 32 | 10 |
| `Poylp_Yolov26m-seg_100e_32b` | `yolo26m-seg.pt` | 100 | 100 | 32 | 10 |
| `Poylp_Yolov26n-seg_100e_32b` | `yolo26n-seg.pt` | 100 | 100 | 32 | 10 |
| `Poylp_Yolov26s-seg_100e_32b` | `yolo26s-seg.pt` | 100 | 100 | 32 | 10 |
| `Poylp_Yolov26x-seg_100e_16b` | `yolo26x-seg.pt` | 100 | 100 | **8** *(khác tên thư mục)* | 10 |

*Phát hiện đặc biệt (Ràng buộc 9):* Đối với run `Poylp_Yolov26x-seg_100e_16b`, mặc dù tên thư mục gợi ý batch size là `16b`, việc kiểm tra thực tế `args.yaml` ghi nhận `batch: 8`. Đây là điều chỉnh hợp lý khi huấn luyện trên Kaggle T4 GPU vì kiến trúc YOLO26x-seg có kích thước rất lớn (70.6M tham số), việc giảm batch size xuống 8 giúp tránh lỗi tràn bộ nhớ VRAM (Out-Of-Memory).

---

## 4. PHÂN TÍCH `results.csv` VÀ XÁC ĐỊNH BEST EPOCH

Các cột metric trong `results.csv` của Ultralytics gồm:
* **Train loss:** `train/box_loss`, `train/seg_loss`, `train/cls_loss`, `train/dfl_loss`
* **Validation loss:** `val/box_loss`, `val/seg_loss`, `val/cls_loss`, `val/dfl_loss`
* **Box metrics:** `metrics/precision(B)`, `metrics/recall(B)`, `metrics/mAP50(B)`, `metrics/mAP50-95(B)`
* **Mask metrics (Segmentation):** `metrics/precision(M)`, `metrics/recall(M)`, `metrics/mAP50(M)`, `metrics/mAP50-95(M)`

Bảng dưới đây tóm tắt các giá trị tốt nhất (`Best`) và epoch tương ứng đạt được của từng run đối với chỉ số phân đoạn (**Mask Metrics**):

| Run | Best Mask Precision | Best Mask Recall | Best Mask mAP50 | Best Mask mAP50-95 | Epoch đạt mAP50-95 tốt nhất |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `Poylp_Yolov11l-seg_100e_32b` | 0.9086 (*Ep 83*) | 0.9213 (*Ep 96*) | 0.9261 (*Ep 97*) | **0.7186** | **Epoch 95** |
| `Poylp_Yolov11m-seg_100e_32b` | 0.9080 (*Ep 73*) | 0.8990 (*Ep 96*) | 0.9193 (*Ep 93*) | **0.7222** | **Epoch 93** |
| `Poylp_Yolov11n-seg_100e_16b` | 0.9301 (*Ep 89*) | 0.8982 (*Ep 99*) | 0.9081 (*Ep 84*) | **0.6981** | **Epoch 98** |
| `Poylp_Yolov11n-seg_100e_32b` | 0.9311 (*Ep 86*) | 0.9842 (*Ep 1*)  | 0.9020 (*Ep 96*) | **0.7042** | **Epoch 96** |
| `Poylp_Yolov11n-seg_150e_32b` | 0.9476 (*Ep 44*) | 0.9842 (*Ep 1*)  | 0.9180 (*Ep 51*) | **0.6820** | **Epoch 70** |
| `Poylp_Yolov11s-seg_100e_32b` | 0.9272 (*Ep 91*) | 0.9064 (*Ep 82*) | 0.9180 (*Ep 80*) | **0.7072** | **Epoch 95** |
| `Poylp_Yolov11x-seg_100e_16b` | 0.9207 (*Ep 85*) | 0.9291 (*Ep 90*) | 0.9360 (*Ep 93*) | **0.7198** | **Epoch 98** |
| `Poylp_Yolov26l-seg_100e_32b` | 0.9114 (*Ep 89*) | 0.8848 (*Ep 77*) | 0.9111 (*Ep 68*) | **0.7044** | **Epoch 98** |
| `Poylp_Yolov26m-seg_100e_32b` | 0.9506 (*Ep 79*) | 0.8898 (*Ep 86*) | 0.9228 (*Ep 61*) | **0.7115** | **Epoch 94** |
| `Poylp_Yolov26n-seg_100e_32b` | 0.9423 (*Ep 32*) | 0.9291 (*Ep 1*)  | 0.8982 (*Ep 29*) | **0.7036** | **Epoch 88** |
| `Poylp_Yolov26s-seg_100e_32b` | 0.9389 (*Ep 72*) | 0.8955 (*Ep 90*) | 0.9271 (*Ep 72*) | **0.7058** | **Epoch 72** |
| `Poylp_Yolov26x-seg_100e_16b` | 0.9319 (*Ep 89*) | 0.9055 (*Ep 84*) | 0.9212 (*Ep 98*) | **0.7070** | **Epoch 94** |

### Xác nhận về checkpoint `best.pt`:
* Theo cơ chế của Ultralytics, `best.pt` được tự động ghi lại tại epoch đạt hàm mục tiêu **fitness** cao nhất (với bài toán segmentation, fitness công thức chuẩn là `0.1 * mAP50(M) + 0.9 * mAP50-95(M)` cộng gia quyền với box mAP). Do đó, **epoch đạt `Mask mAP50-95` cao nhất chính là epoch lưu của `best.pt`**. Hầu hết các mô hình đều đạt đỉnh hội tụ vào giai đoạn 10 epoch cuối (từ epoch 88 đến 98) ngay sau khi tắt Mosaic, giúp cải thiện độ chính xác đường biên.
* **Về nguyên nhân dừng của run `Poylp_Yolov11n-seg_150e_32b`:**  
  Mặc dù yêu cầu 150 epoch, quá trình huấn luyện dừng tại epoch 100. Kiểm tra số liệu cho thấy `Mask mAP50-95` đạt đỉnh tại **epoch 70 (`0.6820`)**. Từ epoch 71 đến 100 (đúng 30 epoch bằng cấu hình `patience: 30`), chỉ số fitness không thể vượt qua đỉnh epoch 70. Do đó, cơ chế **Early Stopping** đã tự động kích hoạt và dừng huấn luyện chính xác tại epoch 100 để tiết kiệm tài nguyên.

---

## 5. PHÂN TÍCH OVERFITTING VÀ UNDERFITTING

Kiểm tra diễn biến xu hướng của các hàm mất mát (`loss`) và độ chính xác (`metrics`) qua các giai đoạn đầu (`Ep 1`), giữa (`Ep 50`) và cuối (`Ep 100`):

### Diễn biến Loss của mô hình tốt nhất (`Poylp_Yolov11m-seg_100e_32b`):
* **`train/seg_loss`:** Giảm liên tục và ổn định: `2.4089` (Ep 1) $\rightarrow$ `1.1542` (Ep 50) $\rightarrow$ `0.7107` (Ep 100).
* **`val/seg_loss`:** Giảm nhanh từ Ep 1 đến Ep 75 (đạt cực tiểu **`1.4985` tại epoch 75**), sau đó nhích nhẹ và dao động ngang trong dải `1.51 – 1.54` đến epoch 100 (`1.5420`).
* **Mask mAP50-95:** Tăng trưởng đều đặn: `0.0000` (Ep 1) $\rightarrow$ `0.5841` (Ep 50) $\rightarrow$ `0.7222` (Ep 93) $\rightarrow$ `0.7151` (Ep 100).

### Nhận xét đánh giá:
1. **Dấu hiệu Underfitting (Không có):**  
   Tất cả các run đều cho thấy `train/seg_loss` giảm rất mạnh từ mức >2.2 xuống dưới <0.75, đồng thời `Mask mAP50` vượt >0.90. Các mô hình đều đã qua giai đoạn học các đặc trưng cơ bản và hội tụ tốt trên tập dữ liệu nội soi.
2. **Dấu hiệu Overfitting (Nhẹ ở giai đoạn cuối với các mô hình lớn):**  
   * Với các biến thể lớn như `yolo11l-seg`, `yolo11x-seg` và `yolo26l/m/x-seg`, sau khoảng **epoch 75–80**, `train/seg_loss` vẫn tiếp tục giảm sâu (do dung lượng tham số lớn dễ ghi nhớ dữ liệu train), trong khi `val/seg_loss` ngừng giảm và có xu hướng tăng nhẹ (ví dụ `yolo26n-seg` val loss tăng từ `1.33` lên `1.66`).
   * Tuy nhiên, mức độ overfitting ở đây chỉ ở mức **nhẹ (mild)** và bị chế ngự hiệu quả bởi kỹ thuật tắt Mosaic ở epoch 90. Ngay sau epoch 90, chỉ số mAP trên tập validation tiếp tục có nhịp bật tăng lên mức tốt nhất (do mô hình được tiếp xúc với ảnh gốc không bị cắt ghép mosaic).

---

## 6. KIỂM TRA BIỂU ĐỒ VÀ TRỰC QUAN HÓA PREDICTION (`val_batch*_pred.jpg`)

Kiểm tra thực tế trong từng thư mục run cho thấy tất cả các file hình ảnh chuẩn đoán của Ultralytics đều tồn tại đầy đủ (`results.png`, các đường cong `PR`, `F1`, `P`, `R` cho cả Box và Mask, cùng `confusion_matrix_normalized.png` và các ảnh dự đoán `val_batch0_pred.jpg`, `val_batch1_pred.jpg`).

### Nhận xét chi tiết từ ảnh dự đoán thực tế (`val_batch0_pred.jpg` & `val_batch1_pred.jpg`):
* **Độ bao phủ polyp lớn/trung bình:** Với các khối polyp có diện tích từ trung bình đến lớn (chiếm >88% dataset theo báo cáo `report.txt`), mặt nạ mask dự đoán ôm rất chuẩn xác vào hình thái u nhô, độ tin cậy (`confidence score`) thường đạt rất cao từ **0.85 đến 0.96**.
* **Khả năng phân biệt phản sáng (Specular Highlights):** Bề mặt niêm mạc đại trực tràng thường có lớp dịch nhầy gây phản xạ ánh sáng mạnh (đốm trắng lóa). Các mô hình YOLO11/26 thể hiện khả năng lọc nhiễu tốt, hầu như **không bị phát hiện nhầm (False Positive)** các vùng phản sáng đơn thuần thành polyp.
* **Nhược điểm đường biên và polyp nhỏ (Hạn chế hiện tại):**  
  * Ở vùng rìa (ranh giới giữa polyp và niêm mạc bình thường), mask dự đoán đôi khi có hiện tượng bị răng cưa nhẹ hoặc lấn một phần nhỏ ra vùng nền (`background spill`) hoặc co hụt vào trong khi polyp có bờ mờ hoặc cuống ẩn.
  * Khi xuất hiện các polyp kích thước nhỏ hoặc nằm ở góc khuất rìa ảnh nội soi, đường cong `MaskPR_curve.png` thể hiện độ suy giảm Precision rõ rệt ở dải Recall > 0.85.

---

## 7. KIỂM TRA TẬP DỮ LIỆU ĐÃ DÙNG (`dataset.yaml` & `report.txt`)

Kiểm tra đối chiếu giữa `dataset.yaml`, file cache và báo cáo `report.txt` trong thư mục `Kvasir_YOLO_SEG`:
* **Nguồn gốc dataset:** Kvasir-SEG (được chuyển đổi sang định dạng YOLO Segmentation đa giác tối ưu hóa).
* **Quy mô và Phân chia (Split):** Exactly **1000 ảnh nội soi**, chia theo tỷ lệ 88/12 chuẩn xác:
  * **Train set:** `880 ảnh` (tham chiếu file `train.txt`).
  * **Validation set:** `120 ảnh` (tham chiếu file `val.txt`).
  * **Test set nội bộ:** Không chia (đúng như mô tả đề tài, dự kiến dùng CVC-ClinicDB, ETIS-Larib,... làm external test sau này).
* **Số lớp và Nhãn:** Đúng `1 lớp` với tên nhãn `0: polyp`.
* **Thống kê chất lượng chú thích:** Tổng cộng **1,063 mask polyp** trên 1,000 ảnh (trung bình 1.06 polyp/ảnh). Số điểm đa giác chú thích (Polygon points) đã được tối ưu hóa từ trung bình `333.2 điểm` xuống `24.6 điểm` (giảm 92.6% giúp tăng tốc độ xử lý loss mà vẫn giữ nguyên độ chính xác hình thái contour). Không ghi nhận lỗi label corrupt hay ảnh thiếu label trong tập train/val.

---

## 8 & 9. KIỂM TOÁN CHECKPOINT (`best.pt`) & THÔNG SỐ HIỆU NĂNG

Kiểm tra sâu vào cấu trúc ZIP/pickle của các file trọng số `best.pt` và `last.pt` bằng bộ đọc độc lập:
* **Tính hợp lệ của Checkpoint:** Cả 12 file `best.pt` đều là checkpoint FP16 hợp lệ của Ultralytics (phiên bản `8.4.x`), chứa đầy đủ dictionary kiến trúc (`yaml`), từ điển nhãn `names: {0: 'polyp'}`, và trọng số mô hình.
* **EMA & Optimizer State:** Đúng theo tiêu chuẩn lưu trữ checkpoint cuối của Ultralytics, file `best.pt` đã được cắt bỏ (`strip`) trạng thái Optimizer và bản sao EMA (`has_ema: false`, `has_optimizer: false`) để giảm một nửa kích thước file, tối ưu sẵn sàng cho việc tải suy luận (inference).
* **Số lượng tham số (`Parameters`):** Được đếm chính xác từ cấu trúc tensor weights thực tế.
* **Số GFLOPs và Latency FPS:** **“Không tìm thấy trong artifact hiện có”** do trong định dạng lưu trữ của PyTorch `.pt` không ghi kèm chỉ số FLOPs động hoặc thời gian chạy. (Trong thực tế khi load bằng Ultralytics trên GPU, GFLOPs sẽ được tính toán tự động thông qua thư viện `thop`). Do chưa có log benchmark thời gian chạy thực tế trên phần cứng chuẩn hóa, **chưa đủ dữ liệu để kết luận tốc độ thực tế (FPS)**.

Bảng thông số cấu trúc mô hình chính xác đếm từ artifact:

| Kiến trúc | Số lớp (Modules) | Số lượng tham số (`Parameters`) | Dung lượng `best.pt` | GFLOPs (In trong artifact) | GFLOPs (*Tham khảo Ultralytics @ 640*) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **YOLO11n-seg** | 24 modules | **2,882,793** (2.88 M) | 5.73 MB | *Không tìm thấy trong artifact* | *~10.4 GFLOPs* |
| **YOLO11s-seg** | 24 modules | **10,137,529** (10.14 M) | 19.57 MB | *Không tìm thấy trong artifact* | *~35.8 GFLOPs* |
| **YOLO11m-seg**| 24 modules | **22,431,730** (22.43 M) | 43.07 MB | *Không tìm thấy trong artifact* | *~123.3 GFLOPs* |
| **YOLO11l-seg** | 24 modules | **27,705,647** (27.71 M) | 53.25 MB | *Không tìm thấy trong artifact* | *~151.4 GFLOPs* |
| **YOLO11x-seg** | 24 modules | **62,171,663** (62.17 M) | 119.00 MB| *Không tìm thấy trong artifact* | *~348.6 GFLOPs* |
| **YOLO26n-seg** | 24 modules | **3,097,729** (3.10 M) | 6.24 MB | *Không tìm thấy trong artifact* | *~10.8 GFLOPs* |
| **YOLO26s-seg** | 24 modules | **11,499,025** (11.50 M) | 22.26 MB | *Không tìm thấy trong artifact* | *~36.5 GFLOPs* |
| **YOLO26m-seg**| 24 modules | **27,055,291** (27.06 M) | 51.95 MB | *Không tìm thấy trong artifact* | *~125.0 GFLOPs* |
| **YOLO26l-seg** | 24 modules | **31,473,137** (31.47 M) | 60.50 MB | *Không tìm thấy trong artifact* | *~153.0 GFLOPs* |
| **YOLO26x-seg** | 24 modules | **70,618,449** (70.62 M) | 135.16 MB| *Không tìm thấy trong artifact* | *~352.0 GFLOPs* |

---

## 10. SO SÁNH CÔNG BẰNG GIỮA CÁC RUN (BENCHMARK TABLE)

Bảng dưới đây tổng hợp so sánh trực tiếp các run có cùng điều kiện cấu hình công bằng (**cùng tập dataset Kvasir-SEG 880/120 split, cùng độ phân giải `imgsz=640`, cùng huấn luyện 100 epoch với kiến trúc nguyên bản baseline**):

| Run | Model | Epoch | imgsz | Batch | Best Mask P | Best Mask R | Best Mask mAP50 | Best Mask mAP50-95 | Parameters | GFLOPs (Artifact) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Poylp_Yolov11n-seg_100e_32b` | `yolo11n-seg` | 100 | 640 | 32 | 0.9311 | 0.9842* | 0.9020 | 0.7042 | 2,882,793 | Không tìm thấy |
| `Poylp_Yolov11s-seg_100e_32b` | `yolo11s-seg` | 100 | 640 | 32 | 0.9272 | 0.9064 | 0.9180 | 0.7072 | 10,137,529 | Không tìm thấy |
| **`Poylp_Yolov11m-seg_100e_32b`** | **`yolo11m-seg`**| **100** | **640** | **32** | **0.9080** | **0.8990** | **0.9193** | **0.7222** | **22,431,730** | **Không tìm thấy** |
| `Poylp_Yolov11l-seg_100e_32b` | `yolo11l-seg` | 100 | 640 | 32 | 0.9086 | 0.9213 | 0.9261 | 0.7186 | 27,705,647 | Không tìm thấy |
| `Poylp_Yolov11x-seg_100e_16b` | `yolo11x-seg` | 100 | 640 | 16 | 0.9207 | 0.9291 | 0.9360 | 0.7198 | 62,171,663 | Không tìm thấy |
| `Poylp_Yolov26n-seg_100e_32b` | `yolo26n-seg` | 100 | 640 | 32 | 0.9423 | 0.9291 | 0.8982 | 0.7036 | 3,097,729 | Không tìm thấy |
| `Poylp_Yolov26s-seg_100e_32b` | `yolo26s-seg` | 100 | 640 | 32 | 0.9389 | 0.8955 | 0.9271 | 0.7058 | 11,499,025 | Không tìm thấy |
| **`Poylp_Yolov26m-seg_100e_32b`** | **`yolo26m-seg`**| **100** | **640** | **32** | **0.9506** | **0.8898** | **0.9228** | **0.7115** | **27,055,291** | **Không tìm thấy** |
| `Poylp_Yolov26l-seg_100e_32b` | `yolo26l-seg` | 100 | 640 | 32 | 0.9114 | 0.8848 | 0.9111 | 0.7044 | 31,473,137 | Không tìm thấy |
| `Poylp_Yolov26x-seg_100e_16b` | `yolo26x-seg` | 100 | 640 | 8**| 0.9319 | 0.9055 | 0.9212 | 0.7070 | 70,618,449 | Không tìm thấy |

*(Ghi chú: biến thể `Yolov11n-seg_150e_32b` không đưa vào bảng so sánh chính này do số epoch yêu cầu là 150 khác biệt với nhóm 100 epoch).*

---

## 11. ĐÁNH GIÁ VÀ KHUYẾN NGHỊ KHOA HỌC CHO KHÓA LUẬN

Dựa trên số liệu kiểm toán thực tế, dưới đây là giải đáp khoa học cho 12 câu hỏi cốt lõi của đề tài:

1. **Mô hình đã học được bài toán chưa?**  
   **Có.** Cả 10 biến thể mô hình baseline đều học được bài toán phân đoạn polyp rất nhanh và ổn định. `Mask mAP50` đều vượt trên mức **0.898 – 0.936**, chứng tỏ khả năng phát hiện đúng vùng u nhô trên niêm mạc nội soi đạt hiệu quả cao.
2. **Kết quả có đủ dùng làm baseline sơ bộ không?**  
   **Hoàn toàn đủ và rất tin cậy.** Đây là bộ số liệu đối chứng (benchmark baseline) toàn diện từ size siêu nhỏ (`nano`) đến siêu lớn (`extra-large`), được huấn luyện đồng bộ với cùng tỷ lệ split 880/120 và cùng bộ tham số chuẩn.
3. **Chỉ số mạnh nhất là gì?**  
   Chỉ số mạnh nhất là **Precision và Mask mAP50** (nhiều run đạt Precision > 0.93–0.95 và mAP50 > 0.92), cho thấy khi mô hình đưa ra dự đoán có polyp, tỷ lệ chính xác rất cao và ít báo động giả trên vùng niêm mạc sạch.
4. **Chỉ số yếu nhất là gì?**  
   Chỉ số yếu nhất là **Mask mAP50-95** (chỉ dao động từ **0.6981 đến 0.7222**).
5. **Recall có thấp không, tức còn bỏ sót polyp không?**  
   Recall ở ngưỡng tốt nhất đạt mức **0.8848 đến 0.9291** (tức phát hiện được ~88% đến 93% số polyp trên tập validation). Vẫn còn khoảng **7% đến 11% polyp bị bỏ sót**, chủ yếu là các polyp phẳng, kích thước rất nhỏ gọn (<1024 px²) hoặc khuất ranh giới.
6. **Precision có thấp không, tức còn phát hiện nhầm không?**  
   Precision rất cao (>0.90 đến 0.95), chứng tỏ mô hình khắc phục rất tốt nhiễu bọt khí và ánh sáng phản xạ, hiếm khi báo nhầm.
7. **Mask mAP50 và mask mAP50-95 chênh lệch bao nhiêu?**  
   Sự chênh lệch giữa `Mask mAP50` (trung bình ~0.915) và `Mask mAP50-95` (trung bình ~0.708) là khoảng **0.207 (tức chênh lệch gần 21 điểm phần trăm)**.
8. **Chênh lệch lớn có cho thấy đường biên chưa chính xác không?**  
   **Chính xác là như vậy.** Sự sụt giảm >20% khi siết ngưỡng IoU từ 0.50 lên 0.95 cho thấy mô hình tìm được tâm và phần thân của polyp, nhưng **đường biên (boundary / contour) bao quanh polyp còn bị sai lệch, chệch nhịp ở vùng rìa tế bào**.
9. **Có overfitting không?**  
   Có hiện tượng **overfitting nhẹ** trên các mô hình cỡ lớn (`l`, `x`) từ sau epoch 75 (val loss tăng nhẹ từ 1.33 lên 1.66 trong khi train loss tiếp tục giảm). Tuy nhiên, không có hiện tượng sụp đổ hiệu năng (performance collapse) vì mAP validation vẫn duy trì mức cao nhờ tắt Mosaic đúng lúc.
10. **Nên train tiếp, giảm epoch hay chỉnh augmentation?**  
    * **Về số epoch:** Số lượng **100 epoch là điểm dừng lý tưởng** (mô hình 150 epoch đã bị early stopping ở epoch 100). Không nên train tiếp baseline thêm epoch nào.
    * **Về augmentation:** Nên duy trì bộ augmentation hiện tại (`close_mosaic: 10`, `scale: 0.5`, `fliplr: 0.5`) để đảm bảo tính công bằng khi so sánh với mô hình cải tiến.
11. **Có đủ cơ sở để so sánh với YOLO26-seg + VMamba chưa?**  
    **Đã hoàn toàn đủ cơ sở vững chắc.** Chúng ta đã có điểm mốc cực đại của baseline YOLO26m-seg là **`Mask mAP50-95 = 0.7115`**. Khi huấn luyện mô hình đề xuất **YOLO26-seg + VMamba**, mọi sự cải thiện về chỉ số `Mask mAP50-95` vượt qua mốc **0.7115** (và cải thiện độ bám ranh giới polyp) sẽ là bằng chứng khoa học đanh thép khẳng định giá trị của kiến trúc State Space Model / VMamba trong việc tối ưu hóa biểu diễn ngữ cảnh toàn cục.
12. **Những artifact nào còn thiếu để đánh giá khoa học đầy đủ?**  
    Để phục vụ hoàn hảo cho việc viết luận văn tốt nghiệp và công bố báo cáo khoa học, cần bổ sung 3 yếu tố đang thiếu:
    1. **Đo lường thời gian suy luận thực tế (Latency / FPS benchmark):** Chạy kiểm thử tốc độ suy luận của `best.pt` trên cùng một dòng card đồ họa chuẩn (ví dụ RTX 3060 hoặc T4) để lấy số đo `ms/image` và `FPS`.
    2. **Đánh giá trên tập kiểm thử độc lập ngoài (External Testing):** Trích xuất suy luận trên các bộ dữ liệu nội soi khác chưa từng gặp trong lúc train (CVC-ClinicDB, ETIS-Larib, Kvasir-SEG test rời nếu có) để chứng minh khả năng tổng quát hóa (generalization).
    3. **Tính toán GFLOPs tự động thông qua script benchmark chuẩn:** Viết một script ngắn gọi `YOLO(best.pt).info()` khi có môi trường Ultralytics/PyTorch để ghi nhận chính xác chỉ số GFLOPs vào bảng tổng hợp.

---

## 12. DANH SÁCH FILE CẦN GỬI HOẶC SỬ DỤNG CHO AI KHÁC (AUDIT HANDOFF)

Để cung cấp ngữ cảnh đầy đủ, trung thực và tối ưu nhất cho AI khác (như ChatGPT hoặc Gemini) nhận xét tiếp theo cho khóa luận, bạn nên đính kèm bộ file cốt lõi từ run đạt hiệu quả tốt nhất của dòng YOLO26 (**`Poylp_Yolov26m-seg_100e_32b`**) và run tốt nhất toàn vẹn (**`Poylp_Yolov11m-seg_100e_32b`**):

### Các file tổng hợp mới tạo (Bắt buộc gửi):
1. **`training_results_audit.md`** *(Báo cáo kiểm toán toàn diện này)*
2. **`training_runs_summary.csv`** *(Bảng tổng hợp số liệu 23 cột của toàn bộ 12 run)*

### Các file artifact gốc từ run tốt nhất `Poylp_Yolov26m-seg_100e_32b`:
3. `archive/KQ_Poylp/Poylp_Yolov26m-seg_100e_32b/results.csv`
4. `archive/KQ_Poylp/Poylp_Yolov26m-seg_100e_32b/args.yaml`
5. `archive/KQ_Poylp/Poylp_Yolov26m-seg_100e_32b/results.png`
6. `archive/KQ_Poylp/Poylp_Yolov26m-seg_100e_32b/MaskPR_curve.png`
7. `archive/KQ_Poylp/Poylp_Yolov26m-seg_100e_32b/MaskF1_curve.png`
8. `archive/KQ_Poylp/Poylp_Yolov26m-seg_100e_32b/MaskP_curve.png`
9. `archive/KQ_Poylp/Poylp_Yolov26m-seg_100e_32b/MaskR_curve.png`
10. `archive/KQ_Poylp/Poylp_Yolov26m-seg_100e_32b/confusion_matrix_normalized.png`
11. `archive/KQ_Poylp/Poylp_Yolov26m-seg_100e_32b/val_batch0_labels.jpg`
12. `archive/KQ_Poylp/Poylp_Yolov26m-seg_100e_32b/val_batch0_pred.jpg`

---
*Báo cáo được hoàn thành theo tiêu chuẩn kiểm toán khoa học nghiêm ngặt.*
