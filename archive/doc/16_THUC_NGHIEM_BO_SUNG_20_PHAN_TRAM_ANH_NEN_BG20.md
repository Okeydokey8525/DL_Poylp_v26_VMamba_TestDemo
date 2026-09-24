# BỘ DỮ LIỆU MỞ RỘNG KVASIR_YOLO_SEG_BG20 VÀ HƯỚNG DẪN HUẤN LUYỆN ĐỐI SÁNH
## ĐÁNH GIÁ ĐỘ ĐẶC HIỆU (SPECIFICITY) VÀ TRIỆT TIÊU HIỆN TƯỢNG BÁO ĐỘNG GIẢ NỀN

---

> **Phân loại độ tin cậy thông tin theo nguyên tắc dự án:**
> - `[Đã xác nhận]`: Dữ liệu 1.000 ảnh polyp gốc (Kvasir-SEG), 200 ảnh nền manh tràng lành (`normal-cecum`), đường dẫn dataset Kaggle `/kaggle/input/datasets/luonglieu/kvasir-yolo-seg-bg20/Kvasir_YOLO_SEG_BG20`, mã nguồn huấn luyện trên Ultralytics 8.4.127.
> - `[Có khả năng / suy luận]`: Khả năng hạ tỷ lệ ô `[Predicted: polyp, True: background]` từ 1.00 xuống dưới 0.15 khi có sự xuất hiện của 40 ảnh nền trong tập validation.
> - `[Chưa xác minh]`: Sự biến thiên nhỏ của Mask mAP@50-95 khi bổ sung 20% ảnh nền (chờ kết quả chạy thực tế trên Kaggle GPU T4).

---

## 1. BỐI CẢNH VÀ ĐỘNG LỰC NGHIÊN CỨU

Trong các thí nghiệm 6-fold trước đây trên tập dữ liệu chuẩn Kvasir-SEG (1.000 ảnh đều chứa polyp):
* Ma trận nhầm lẫn chuẩn hóa của cả Baseline và C2IAVM đều hiển thị **`1.00`** tại ô `[Predicted: polyp, True: background]`.
* **Nguyên nhân cốt lõi:** Do Kvasir-SEG không chứa bất kỳ khung hình nội soi âm tính (ảnh ruột bình thường không có polyp) nào. Khái niệm True Negative (TN) trên mô nền không được định nghĩa, dẫn tới công thức chuẩn hóa theo cột:
  $$\frac{\text{FP}}{\text{FP} + \text{TN}} = \frac{\text{FP}}{\text{FP} + 0} = \mathbf{1.00} \ (100\%)$$
* Để chứng minh mô hình có khả năng "từ chối" dự đoán trên niêm mạc bình thường và đo lường độ đặc hiệu (Specificity) thực tế, nhóm nghiên cứu đã xây dựng bộ dữ liệu độc lập **`Kvasir_YOLO_SEG_BG20`**.

---

## 2. QUY CÁCH PHÂN BỔ BỘ DỮ LIỆU KVASIR_YOLO_SEG_BG20

* **Nguồn ảnh âm tính:** Trích xuất ngẫu nhiên cố định (`random.seed(42)`) đúng **200 ảnh** từ kho 1.000 ảnh nội soi manh tràng bình thường `normal-cecum` (bộ dữ liệu gốc Kvasir v2 của Pogorelov et al.).
* **Định dạng nhãn ảnh nền:** File `.txt` tương ứng có **kích thước đúng 0 byte** (file rỗng theo chuẩn của Ultralytics YOLO).
* **Đường dẫn dataset trên Kaggle:**  
  `[Đã xác nhận]` **`/kaggle/input/datasets/luonglieu/kvasir-yolo-seg-bg20/Kvasir_YOLO_SEG_BG20`**

| Phân vùng dữ liệu | Ảnh Polyp (Kvasir-SEG) | Ảnh Nền (`normal-cecum`) | Tổng số ảnh | Đặc tả file nhãn (`.txt`) |
| :--- | :---: | :---: | :---: | :--- |
| **Tập Train** | 880 ảnh | **160 ảnh** | **1.040 ảnh** | 880 file polygon + 160 file rỗng (0-byte) |
| **Tập Val** | 120 ảnh (127 polyp) | **40 ảnh** | **160 ảnh** | 120 file polygon + 40 file rỗng (0-byte) |
| **Tổng cộng** | **1.000 ảnh** | **200 ảnh** (20%) | **1.200 ảnh** | Tỷ lệ train/val giữ đúng chuẩn 80/20 |

---

## 3. CODE HUẤN LUYỆN TRỌN GÓI TRÊN KAGGLE (COPY-PASTE READY)

### 3.1. Kịch Bản 1: Huấn Luyện MÔ HÌNH CẢI TIẾN (Attention-VMamba Fusion - IAVM)

#### CELL 1: SETUP CUSTOM REPO & TẠO DATA_BG20.YAML
```python
# ============================================================
# CELL 1: SETUP REPO CUSTOM ATTENTION-VMAMBA FUSION + DATA_BG20.YAML
# ============================================================
import os, sys, glob, shutil, yaml

# 0. Xóa cache module cũ trong RAM (tránh xung đột)
for k in list(sys.modules.keys()):
    if k.startswith("ultralytics"):
        del sys.modules[k]

# 1. Khai báo chính xác đường dẫn repo Attention-VMamba Fusion trên Kaggle
CUSTOM_REPO_PATH = "/kaggle/input/datasets/luonglieu/ultralytics-attention-vmamba-fusion/ultralytics_Attention_VMamba_Fusion"
if not os.path.exists(CUSTOM_REPO_PATH):
    candidates = glob.glob("/kaggle/input/**/ultralytics_Attention_VMamba_Fusion", recursive=True)
    if not candidates:
        candidates = glob.glob("/kaggle/input/**/yolo26-seg-InteractiveAttentionVMamba.yaml", recursive=True)
        CUSTOM_REPO_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(candidates[0])))) if candidates else None
    else:
        CUSTOM_REPO_PATH = candidates[0]

assert CUSTOM_REPO_PATH and os.path.exists(CUSTOM_REPO_PATH), f"❌ Không tìm thấy repo tại: {CUSTOM_REPO_PATH}"
print(f"📁 Tìm thấy Custom Repo tại: {CUSTOM_REPO_PATH}")

# 2. Xóa symlink cũ và tạo symlink mới tại /kaggle/working/ultralytics
symlink_path = "/kaggle/working/ultralytics"
if os.path.islink(symlink_path) or os.path.exists(symlink_path):
    if os.path.islink(symlink_path):
        os.unlink(symlink_path)
    else:
        shutil.rmtree(symlink_path)

os.symlink(CUSTOM_REPO_PATH, symlink_path)
print("🔗 Đã tạo symlink 'ultralytics' trỏ tới Custom Repo thành công")

if "/kaggle/working" not in sys.path: sys.path.insert(0, "/kaggle/working")
if CUSTOM_REPO_PATH not in sys.path: sys.path.insert(0, CUSTOM_REPO_PATH)

# Kiểm tra nạp module cốt lõi C2IAVM
import ultralytics
from ultralytics.nn.modules import C2IAVM
print("✅ Nạp Ultralytics Custom từ:", ultralytics.__file__)
print("✅ Nạp Module C2IAVM:", C2IAVM)

# 3. Tạo config YAML scale 's' cho Attention-VMamba Fusion
SRC_YAML = os.path.join(CUSTOM_REPO_PATH, "cfg", "models", "26", "yolo26-seg-InteractiveAttentionVMamba.yaml")
assert os.path.exists(SRC_YAML), f"❌ Không tìm thấy file YAML gốc: {SRC_YAML}"

YAML_SCALE_S = "/kaggle/working/yolo26s-seg-InteractiveAttentionVMamba.yaml"
shutil.copy2(SRC_YAML, YAML_SCALE_S)

with open(YAML_SCALE_S, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)
cfg["scale"] = "s"
with open(YAML_SCALE_S, "w", encoding="utf-8") as f:
    yaml.safe_dump(cfg, f, sort_keys=False)
print("✅ Đã tạo file YAML chuẩn scale s:", YAML_SCALE_S)

# 4. Trỏ chính xác vào bộ dữ liệu Kvasir_YOLO_SEG_BG20
DATASET_ROOT = "/kaggle/input/datasets/luonglieu/kvasir-yolo-seg-bg20/Kvasir_YOLO_SEG_BG20"
assert os.path.exists(DATASET_ROOT), f"❌ Không tìm thấy bộ dữ liệu tại: {DATASET_ROOT}"

DATA_YAML = "/kaggle/working/data_bg20.yaml"
with open(DATA_YAML, "w", encoding="utf-8") as f:
    yaml.safe_dump({
        "path": DATASET_ROOT,
        "train": "images/train",
        "val": "images/val",
        "nc": 1,
        "names": {0: "polyp"}
    }, f, sort_keys=False, allow_unicode=True)
print("✅ Đã tạo data_bg20.yaml thành công với dataset:", DATASET_ROOT)
```

#### CELL 2: KHÓA TẤT ĐỊNH & TRAIN ATTENTION-VMAMBA FUSION TRÊN BG20
```python
# ============================================================
# CELL 2: KHÓA TẤT ĐỊNH & HUẤN LUYỆN ATTENTION-VMAMBA TRÊN BG20
# ============================================================
import os, random, numpy as np, torch
from ultralytics import YOLO

# 1. THIẾT LẬP SIÊU THAM SỐ (ĐỒNG BỘ ĐỐI SÁNH SEED 0)
SEED = 0  # Đối soát trực tiếp với ma trận nhầm lẫn Seed 0 ban đầu
WORKERS = 2
EPOCHS = 100

# 2. KHÓA TẤT ĐỊNH HỆ THỐNG
os.environ["PYTHONHASHSEED"] = str(SEED)
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)

torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True
torch.use_deterministic_algorithms(True, warn_only=False)

# 3. KHỞI TẠO MODEL VÀ LOAD TRỌNG SỐ PRETRAINED
yaml_cfg = "/kaggle/working/yolo26s-seg-InteractiveAttentionVMamba.yaml"
model = YOLO(yaml_cfg).load("yolo26s-seg.pt")

# 4. TIẾN HÀNH HUẤN LUYỆN
results = model.train(
    data="/kaggle/working/data_bg20.yaml",
    epochs=EPOCHS,
    imgsz=640,
    batch=8,
    device=0,
    workers=WORKERS,
    cache=False,
    amp=False,
    optimizer="AdamW",
    seed=SEED,
    lr0=0.001,
    warmup_epochs=5.0,
    deterministic=True,
    patience=100,
    close_mosaic=10,
    project="/kaggle/working/runs_bg20",
    name=f"Kvasir_BG20_YOLO26s_seg_IAVM_s{SEED}_w{WORKERS}",
    exist_ok=True,
    plots=True
)

print(f"\n🎉 Huấn luyện thành công Attention-VMamba Fusion trên tập BG20 Seed {SEED}!")
```

---

### 3.2. Kịch Bản 2: Huấn Luyện MÔ HÌNH ĐỐI CHỨNG (Baseline YOLO26s-seg)

#### CELL 1: CÀI ULTRALYTICS & TẠO DATA_BG20.YAML CHO BASELINE
```python
# ============================================================
# CELL 1: CÀI ULTRALYTICS ĐỒNG BỘ 8.4.127 + TẠO DATA_BG20.YAML
# ============================================================
!pip install -q ultralytics==8.4.127

import os, yaml, ultralytics
print("✅ Phiên bản Ultralytics chuẩn:", ultralytics.__version__)

DATASET_ROOT = "/kaggle/input/datasets/luonglieu/kvasir-yolo-seg-bg20/Kvasir_YOLO_SEG_BG20"
assert os.path.exists(DATASET_ROOT), f"❌ Không tìm thấy bộ dữ liệu tại: {DATASET_ROOT}"

data_config = {
    "path": DATASET_ROOT,
    "train": "images/train",
    "val": "images/val",
    "nc": 1,
    "names": {0: "polyp"}
}

DATA_YAML = "/kaggle/working/data_bg20.yaml"
with open(DATA_YAML, "w", encoding="utf-8") as f:
    yaml.safe_dump(data_config, f, sort_keys=False, allow_unicode=True)

print("✅ Đã tạo data_bg20.yaml thành công!")
```

#### CELL 2: KHÓA TẤT ĐỊNH & TRAIN BASELINE TRÊN BG20
```python
# ============================================================
# CELL 2: KHÓA TẤT ĐỊNH & TRAIN BASELINE YOLO26s-seg TRÊN BG20
# ============================================================
import os, random, numpy as np, torch
from ultralytics import YOLO

# 1. SIÊU THAM SỐ
SEED = 0  # Đồng bộ hoàn toàn với kịch bản IAVM
WORKERS = 2  
EPOCHS = 100    

# 2. KHÓA TẤT ĐỊNH HỆ THỐNG
os.environ["PYTHONHASHSEED"] = str(SEED)
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)

torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True
torch.use_deterministic_algorithms(True, warn_only=False)

# 3. HUẤN LUYỆN BASELINE GỐC
model = YOLO("yolo26s-seg.pt")

results = model.train(
    data="/kaggle/working/data_bg20.yaml",
    epochs=EPOCHS,
    imgsz=640,
    batch=8,
    device=0,
    workers=WORKERS,
    cache=False,
    amp=False,
    optimizer="AdamW",
    seed=SEED,
    lr0=0.001,
    warmup_epochs=5.0,
    deterministic=True,
    patience=100,
    close_mosaic=10,
    project="/kaggle/working/runs_bg20",
    name=f"Kvasir_BG20_Baseline_YOLO26s_seg_s{SEED}_w{WORKERS}",
    exist_ok=True,
    plots=True
)

print(f"\n🎉 Huấn luyện thành công Baseline trên tập BG20 Seed {SEED}!")
```

### 3.3. LƯU Ý KỸ THUẬT QUAN TRỌNG: PHÒNG NGỪA SỰ CỐ TỰ ĐỘNG FUSE TRONG FINAL EVALUATION

> [!WARNING]
> **Hiện tượng lỗi xuất ảnh khi train xong trên Kaggle:**
> * Trong 100 epoch huấn luyện, bảng số liệu `results.csv` hoàn toàn chính xác (ví dụ TSVM Seed 0 đạt Mask mAP@50 = **0.904**, Seed 5 đạt Mask mAP@50 = **0.910**).
> * Tuy nhiên, khi kết thúc epoch 100, Ultralytics tự động gọi `model.fuse()`. Trong custom head `Segment26` (Detect26), hàm `fuse()` sẽ xóa bỏ nhánh One-to-Many (`self.cv2 = None`) và ép chuyển sang nhánh One-to-One (End-to-End).
> * Do nhánh One-to-One tại một số seed (như Seed 5) chưa hội tụ đầy đủ, việc đánh giá cuối cùng bị sụp đổ (mAP về 0), khiến các ảnh đường cong (`BoxPR_curve`, `BoxF1_curve`,...) bị phẳng/rỗng và ảnh `val_batch2_pred.jpg` xuất hiện các box cột dọc lỗi kéo giãn từ $y_1=0$ đến $y_2=640$.
> * Đồng thời, hàm `plot_images` của Ultralytics vướng lỗi thứ tự tọa độ trong Pillow 10+ (`ValueError: x1 must be greater than or equal to x0`) làm gián đoạn lưu ảnh dự đoán.

#### CELL 3: VALIDATION KHẮC PHỤC TRIỆT ĐỂ & XUẤT 24 ẢNH KẾT QUẢ CHUẨN XÁC
Sau khi cell huấn luyện hoàn tất, chạy thêm cell dưới đây để xuất lại trọn bộ 24 ảnh kết quả chuẩn trên nhánh One-to-Many:

```python
# ============================================================
# CELL 3: POST-TRAIN EVALUATION TRÊN NHÁNH ONE-TO-MANY (KHÔNG FUSE)
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

# 2. Xử lý an toàn tọa độ Pillow 10+
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

print("✅ Đã cấu hình môi trường post-eval One-to-Many chuẩn xác!")
```
*Chi tiết toàn bộ phân tích nguyên nhân và giải pháp kỹ thuật xem tại tài liệu:*  
👉 [doc/17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md)

---

## 4. Ý NGHĨA KHOA HỌC KHI ĐƯA VÀO LUẬN VĂN

1. **Khảo sát bóc tách tính đặc hiệu (Specificity Ablation):**
   * Trong 40 ảnh `normal-cecum` ở tập validation: Mô hình C2IAVM với cơ chế quét chọn lọc Selective Scan và tương tác kênh-không gian sẽ ức chế mạnh các tín hiệu giả từ bọt khí, nếp gấp niêm mạc.
   * Ma trận nhầm lẫn sẽ xuất hiện chỉ số **True Negative (TN)** rõ ràng tại ô `[Predicted: background, True: background]` (kỳ vọng đạt từ $0.85$ đến $0.95$).
   * Con số `1.00` ở ô `[Predicted: polyp, True: background]` sẽ tụt xuống dưới mức $0.15$, phản ánh trực quan năng lực loại bỏ báo động giả trong thực tế lâm sàng.
2. **Khẳng định tính liêm chính học thuật:**
   * Tập dữ liệu gốc 1.000 ảnh vẫn là thước đo chuẩn 6-fold xuyên suốt đồ án.
   * Tập BG20 là thực nghiệm mở rộng độc lập, cung cấp bằng chứng thuyết phục trả lời mọi câu hỏi phản biện của Hội đồng về rủi ro can thiệp nhầm trên mô ruột lành.
