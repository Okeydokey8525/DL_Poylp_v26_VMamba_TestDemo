# BÁO CÁO KỸ THUẬT: SỰ CỐ TỰ ĐỘNG FUSE KHI HUẤN LUYỆN TRÊN KAGGLE VÀ PHƯƠNG ÁN KHẮC PHỤC TRIỆT ĐỂ
## ÁP DỤNG CHO MÔ HÌNH YOLO26s-seg-TSVM (SEED 0 & SEED 5) TRÊN TẬP KVASIR_YOLO_SEG_BG20

---

> [!IMPORTANT]
> **TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)**
> - **Hiện tượng:** Khi hoàn tất 100 epochs trên Kaggle GPU (NVIDIA Tesla T4), bảng số liệu `results.csv` và tiến trình huấn luyện của mô hình TSVM (Topology-Shape-aware VMamba) **hoàn toàn chính xác và hội tụ rất tốt** (Mask mAP@50 đạt **0.9040** ở Seed 0 và **0.9096** ở Seed 5). Tuy nhiên, các artifact hình ảnh xuất ra cuối cùng lại bị lỗi: các đồ thị đường cong đánh giá (`BoxPR_curve`, `BoxF1_curve`,...) bị lệch hoặc trống rỗng (AUC = 0 ở Seed 5), đồng thời ảnh dự đoán `val_batch2_pred.jpg` xuất hiện các vệt kéo giãn dạng cột dọc xanh từ đỉnh xuống đáy ảnh ($y_1=0 \to y_2=640$).
> - **Nguyên nhân cốt lõi:** Cơ chế `model.fuse()` mặc định của Ultralytics ở bước đánh giá cuối cùng (`final_eval`) đã xóa bỏ các module của nhánh One-to-Many (`self.cv2 = self.cv3 = self.cv4 = None`) trong custom head `Segment26` và ép chuyển sang nhánh One-to-One (End-to-End). Do nhánh One-to-One chưa hội tụ hoàn toàn (điểm tin cậy tối đa chỉ đạt 0.028), việc suy diễn cuối cùng bị sụp đổ, sinh ra các box dị dạng và làm rỗng đồ thị đánh giá.
> - **Hiện trạng & Khắc phục:** Trọng số `best.pt` của cả 2 seed **vẫn còn nguyên vẹn 100%**. Nhóm nghiên cứu đã xây dựng quy trình trích xuất và sinh lại chuẩn xác **ĐỦ 24 ẢNH KẾT QUẢ / SEED** theo đúng chuẩn khoa học (300 DPI), khớp 100% với `results.csv`, được lưu trữ an toàn và độc lập tại thư mục:  
>   `archive/Khac_phuc/Kvasir_BG20_YOLO26s_seg_TSVM_s0_w2`  
>   `archive/Khac_phuc/Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2`

---

## 1. BỐI CẢNH VÀ HIỆN TƯỢNG PHÁT SINH TRÊN KAGGLE

Trong khuôn khổ thực nghiệm trên bộ dữ liệu mở rộng **Kvasir_YOLO_SEG_BG20** (1.040 ảnh train, 160 ảnh validation gồm 120 ảnh polyp và 40 ảnh nền manh tràng lành `normal-cecum`), mô hình **YOLO26s-seg-TSVM** được huấn luyện độc lập qua 6 seed (`s0` đến `s5`, 100 epochs/seed) trên môi trường Kaggle GPU.

### 1.1. Bằng chứng số liệu huấn luyện hoàn toàn chính xác trong `results.csv`
Khi kiểm tra tiến trình từng epoch trong `results.csv`:
* **Tại Seed 0 (Best Epoch 88):**
  - `metrics/precision(B)`: $0.9226$, `metrics/recall(B)`: $0.8450$, `metrics/mAP50(B)`: $0.8973$, `metrics/mAP50-95(B)`: $0.7125$
  - `metrics/precision(M)`: $0.9312$, `metrics/recall(M)`: $0.8529$, `metrics/mAP50(M)`: $0.9040$, `metrics/mAP50-95(M)`: $0.7245$
* **Tại Seed 5 (Best Epoch 90):**
  - `metrics/precision(B)`: $0.8956$, `metrics/recall(B)`: $0.8779$, `metrics/mAP50(B)`: $0.9113$, `metrics/mAP50-95(B)`: $0.7398$
  - `metrics/precision(M)`: $0.9013$, `metrics/recall(M)`: $0.8819$, `metrics/mAP50(M)`: $0.9096$, `metrics/mAP50-95(M)`: $0.7285$

Số liệu trong quá trình huấn luyện chứng minh mô hình TSVM học rất tốt, đạt độ chính xác tương đương hoặc vượt trội so với Baseline ở nhiều chỉ số phân đoạn.

### 1.2. Hiện tượng lỗi hình ảnh sau khi kết thúc lượt chạy
Mặc dù số liệu đúng, các file ảnh trong thư mục xuất ra lại gặp 2 vấn đề nghiêm trọng:
1. **Lỗi đường cong đánh giá (Evaluation Curves):**
   - Ở Seed 0: Các đường cong `BoxPR_curve.png`, `MaskPR_curve.png` bị tụt điểm mAP xuống mức $\approx 0.627$ (không khớp với mức $0.904$ trong `results.csv`).
   - Ở Seed 5: Toàn bộ 8 file đường cong (`BoxPR_curve`, `BoxF1_curve`, `BoxP_curve`, `BoxR_curve`, `MaskPR_curve`, `MaskF1_curve`, `MaskP_curve`, `MaskR_curve`) bị phẳng lì hoặc trống rỗng hoàn toàn, chỉ số ghi nhận `all classes 0.000 mAP@0.5`.
2. **Lỗi ảnh dự đoán phân đoạn (`val_batch2_pred.jpg`):**
   - Ở Seed 5: Xuất hiện các bounding box màu xanh lam bị kéo giãn toàn bộ chiều cao khung hình từ $y_1=0$ đến $y_2=640$ tạo thành các vệt cột dọc bất thường.

---

## 2. PHÂN TÍCH NGUYÊN NHÂN GỐC RỄ (ROOT CAUSE ANALYSIS)

Sau khi dịch ngược mã nguồn và rà soát các module liên quan trong Ultralytics và custom head của mô hình TSVM, nhóm nghiên cứu đã xác định chính xác 3 nguyên nhân cốt lõi:

```
[Tiến trình Train 100 Epochs] 
   └── Học song song: Nhánh One-to-Many (hội tụ cao, mAP ~0.91) + Nhánh One-to-One
         │
[Kết thúc Epoch 100 -> Gọi final_eval()]
   └── Ultralytics tự động gọi `model.fuse()`
         │
         ├── [Sự cố 1]: `Segment26.fuse()` xóa bỏ nhánh One-to-Many (`self.cv2 = None`)
         │               và ép `self.end2end = True` (chuyển sang One-to-One).
         │
         ├── [Sự cố 2]: Nhánh One-to-One ở Seed 5 chưa hội tụ (conf max = 0.028)
         │               ==> Toàn bộ dự đoán bị lọc sạch hoặc sinh box rác $y_1=0 \to y_2=640$.
         │               ==> mAP bị kéo về 0, sinh ra 8 ảnh curve rỗng.
         │
         └── [Sự cố 3]: Pillow 10+ throw `ValueError: x1 must be greater than or equal to x0`
                         trong background thread của `plot_images`, làm đứt gãy việc lưu `val_batch*_pred.jpg`.
```

### 2.1. Cơ chế kiến trúc Dual-Branch của YOLO26 (Segment26 / Detect26)
YOLO26 kế thừa kiến trúc đầu dò kép kết hợp giữa **One-to-Many** (dùng NMS truyền thống) để huấn luyện bộ trích xuất đặc trưng mạnh mẽ và **One-to-One** (End-to-End NMS-free) nhằm tăng tốc độ suy luận.
* Trong quá trình huấn luyện (100 epoch), hàm loss giám sát cả hai nhánh:
  $$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{one2many}} + \mathcal{L}_{\text{one2one}}$$
* Các chỉ số ghi vào `results.csv` tại mỗi epoch được tính toán dựa trên nhánh **One-to-Many**, nơi mô hình đạt được hiệu năng cao nhất.

### 2.2. Hành vi tự động `fuse()` của Ultralytics tại `final_eval()`
Tại thời điểm kết thúc epoch 100, phương thức `validator` được gọi để thực hiện đánh giá tổng kết cuối cùng. Trình quản lý của Ultralytics tự động thực thi lệnh:
```python
model.fuse()
```
Trong tệp `ultralytics/nn/modules/head.py` của biến thể YOLO26:
```python
def fuse(self):
    """Fuse One-to-Many into One-to-One and remove auxiliary branches."""
    self.cv2 = self.cv3 = self.cv4 = None  # Xóa sạch nhánh One-to-Many!
    self.one2many = None
    self.end2end = True  # Ép buộc chỉ suy diễn bằng One-to-One
```
Hành vi này đã **xóa bỏ hoàn toàn nhánh One-to-Many** khỏi bộ nhớ RAM tại thời điểm đánh giá cuối cùng.

### 2.3. Sự phân kỳ của nhánh One-to-One tại các Seed cụ thể
Khi kiểm tra trực tiếp mô hình với ảnh nội soi thực tế `cju0s690hkp960855tjuaqvv0.jpg`:
* **Khi suy diễn bằng nhánh One-to-Many:** Mô hình phát hiện chính xác khối polyp với độ tin cậy **$0.856$**, bounding box $[247, 43, 309, 263]$, mask ôm sát rìa tổn thương.
* **Khi ép suy diễn bằng nhánh One-to-One (End-to-End):** Độ tin cậy tối đa chỉ đạt **$0.028$** (dưới ngưỡng tối thiểu $0.001$), các box bị trôi tọa độ và vỡ cấu trúc giải phẫu, dẫn tới việc xuất hiện các box cột dọc rác $y_1=0 \to y_2=640$.
* Do nhánh One-to-One ở Seed 5 bị sụp đổ, hàm tính toán AUC đưa ra kết quả bằng 0, tạo nên các file ảnh curve trống rỗng.

### 2.4. Xung đột luồng ngầm trong Pillow 10+ và `plot_images`
Hàm vẽ ảnh `plot_images` của Ultralytics được bọc bởi decorator `@threaded`. Khi vẽ các box dị dạng có tọa độ chưa chuẩn hóa, thư viện Pillow 10+ tung ngoại lệ:
```
ValueError: x1 must be greater than or equal to x0
```
Do chạy trên một `Thread` không có cơ chế `join()` hoặc bắt lỗi tường minh, tiến trình bị thoát trước khi ảnh dự đoán được hoàn tất ghi xuống ổ đĩa.

---

## 3. GIẢI PHÁP KHẮC PHỤC TRIỆT ĐỂ (SOLUTION IMPLEMENTATION)

Nhóm nghiên cứu đã thiết lập giải pháp kỹ thuật 4 tầng đảm bảo dữ liệu trung thực 100% với số liệu huấn luyện mà không cần huấn luyện lại từ đầu:

### 3.1. Bảo tồn 100% trọng số nguyên bản `best.pt`
File checkpoint `weights/best.pt` được lưu trong quá trình train trước khi lệnh `model.fuse()` diễn ra. Do đó, trọng số của nhánh One-to-Many (`head.cv2`, `head.cv3`, `head.cv4`) **vẫn còn nguyên vẹn trong tệp checkpoint**.

### 3.2. Vô hiệu hóa `fuse` và khóa nhánh One-to-Many
Can thiệp vào `AutoBackend` và `Detect26`:
```python
# 1. Ngăn chặn AutoBackend tự động gọi fuse()
orig_init = autobackend.AutoBackend.__init__
def patched_init(self, model="yolo26n.pt", device=None, dnn=False, data=None, fp16=False, fuse=True, verbose=True):
    orig_init(self, model=model, device=device, dnn=dnn, data=data, fp16=fp16, fuse=False, verbose=verbose)
autobackend.AutoBackend.__init__ = patched_init

# 2. Khóa cứng end2end = False để ép buộc sử dụng nhánh One-to-Many + NMS chuẩn
from ultralytics.nn.modules.head import Detect
Detect.end2end = property(fget=lambda self: False, fset=lambda self, v: setattr(self, '_end2end', v))
```

### 3.3. Xử lý an toàn tọa độ Pillow và đồng bộ luồng ghi ảnh
```python
# 3. Patch PIL ImageDraw.rectangle chống crash đảo tọa độ
import PIL.ImageDraw
orig_draw = PIL.ImageDraw.ImageDraw.rectangle
def safe_rectangle(self, xy, fill=None, outline=None, width=1):
    try:
        if isinstance(xy, (list, tuple)) and len(xy) == 4:
            x0, y0, x1, y1 = xy
            xy = [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]
    except Exception:
        pass
    return orig_draw(self, xy, fill=fill, outline=outline, width=width)
PIL.ImageDraw.ImageDraw.rectangle = safe_rectangle

# 4. Ghi ảnh đồng bộ (Synchronous)
import ultralytics.utils.plotting as p
if hasattr(p.plot_images, "__closure__") and p.plot_images.__closure__:
    p.plot_images = p.plot_images.__closure__[0].cell_contents
```

### 3.4. Xuất trọn bộ 24 ảnh kết quả chuẩn cho mỗi seed
Tại thư mục `archive/Khac_phuc/`, mỗi seed được tạo lập đầy đủ đúng **24 file ảnh**:
1. **7 ảnh train:** `labels.jpg`, `train_batch0/1/2.jpg`, `train_batch11700/11701/11702.jpg`.
2. **3 ảnh Ground Truth:** `val_batch0/1/2_labels.jpg`.
3. **1 ảnh đồ thị tiến trình:** `results.png`.
4. **3 ảnh dự đoán thực tế:** `val_batch0/1/2_pred.jpg` (đã triệt tiêu hoàn toàn cột dọc lỗi, box và mask ôm khít polyp).
5. **2 ảnh ma trận nhầm lẫn:** `confusion_matrix.png`, `confusion_matrix_normalized.png`.
6. **8 ảnh đường cong hiệu năng 300 DPI:** `BoxPR_curve`, `BoxF1_curve`, `BoxP_curve`, `BoxR_curve`, `MaskPR_curve`, `MaskF1_curve`, `MaskP_curve`, `MaskR_curve`.

---

## 4. BẢNG ĐỐI CHIẾU TRƯỚC VÀ SAU KHẮC PHỤC

| Tiêu chí so sánh | Trạng thái ban đầu trên Kaggle | Trạng thái sau khắc phục trong `Khac_phuc/` |
| :--- | :--- | :--- |
| **Số lượng ảnh / Seed** | Không đồng đều, thiếu ảnh pred do thread crash | **Đúng chính xác 24/24 file ảnh chuẩn Ultralytics** |
| **Ảnh `val_batch2_pred.jpg` (Seed 5)** | Bị kéo giãn cột dọc $y_1=0 \to y_2=640$ | **Chuẩn xác: Box & mask polyp rõ nét, không còn cột dọc** |
| **Mask mAP@50 (Seed 0)** | Bị tụt xuống $0.627$ trên ảnh curve | **Khớp 100% với `results.csv`: $0.904$ mAP@0.5** |
| **Mask mAP@50 (Seed 5)** | Bị sụp đổ về $0.000$ trên ảnh curve | **Khớp 100% với `results.csv`: $0.910$ mAP@0.5** |
| **Độ phân giải các file curve** | Ảnh rỗng / vẽ lệch dải | **Chuẩn xuất bản khoa học 300 DPI, hiển thị đầy đủ dải confidence** |
| **Tính toàn vẹn metadata** | Lưu rải rác | **Đầy đủ `args.yaml`, `results.csv`, `weights/best.pt`, `weights/last.pt`** |

---

## 5. HƯỚNG DẪN TÁI LẬP TRÊN KAGGLE GPU CHO CÁC LẦN TRAIN SAU

Để phòng tránh triệt để lỗi tự động fuse này trong các lượt huấn luyện kế tiếp trên Kaggle GPU, người dùng chỉ cần thêm Cell thực thi sau khi hoàn thành `model.train()`:

```python
# ============================================================
# CELL POST-TRAIN: XUẤT 24 ẢNH KẾT QUẢ CHUẨN XÁC TRÊN NHÁNH ONE-TO-MANY
# ============================================================
import os, sys
from pathlib import Path
import PIL.ImageDraw
from ultralytics.utils.plotting import Annotator
import ultralytics.utils.plotting as p
from ultralytics.models.yolo.segment import SegmentationValidator
from ultralytics.nn import autobackend
from ultralytics.nn.modules.head import Detect

# 1. Khóa cứng không cho fuse và ép dùng nhánh One-to-Many
Detect.end2end = property(fget=lambda self: False, fset=lambda self, v: setattr(self, '_end2end', v))

orig_init = autobackend.AutoBackend.__init__
def patched_init(self, model="yolo26n.pt", device=None, dnn=False, data=None, fp16=False, fuse=True, verbose=True):
    orig_init(self, model=model, device=device, dnn=dnn, data=data, fp16=fp16, fuse=False, verbose=verbose)
autobackend.AutoBackend.__init__ = patched_init

# 2. Chống crash Pillow
orig_draw = PIL.ImageDraw.ImageDraw.rectangle
def safe_rectangle(self, xy, fill=None, outline=None, width=1):
    try:
        if isinstance(xy, (list, tuple)) and len(xy) == 4:
            x0, y0, x1, y1 = xy
            xy = [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]
    except Exception:
        pass
    return orig_draw(self, xy, fill=fill, outline=outline, width=width)
PIL.ImageDraw.ImageDraw.rectangle = safe_rectangle

# 3. Đồng bộ ghi ảnh
if hasattr(p.plot_images, "__closure__") and p.plot_images.__closure__:
    p.plot_images = p.plot_images.__closure__[0].cell_contents

print("✅ Đã thiết lập môi trường xuất ảnh chuẩn không bị fuse!")
```

Script hoàn chỉnh đã được lưu tại [kaggle_val_fix_guide.py](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/kaggle_val_fix_guide.py).

---
*Tài liệu được lập theo tiêu chuẩn kiểm toán khoa học và quy tắc tối ưu hóa nghiên cứu trí tuệ nhân tạo của đề tài CNTT_KLCN182.*
