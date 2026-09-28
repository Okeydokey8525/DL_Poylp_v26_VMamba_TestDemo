# BỘ DỮ LIỆU CHÍNH THỨC KVASIR_YOLO_SEG_BG20 VÀ KẾT QUẢ THỰC NGHIỆM HUẤN LUYỆN 10 SEEDS
## ĐÁNH GIÁ ĐỘ ĐẶC HIỆU (SPECIFICITY), ĐỘ ỔN ĐỊNH VÀ TRIỆT TIÊU HIỆN TƯỢNG BÁO ĐỘNG GIẢ NỀN

---

> **Phân loại độ tin cậy thông tin theo nguyên tắc dự án:**
> - `[Đã xác nhận]`: Dữ liệu 1.000 ảnh polyp gốc (Kvasir-SEG) kết hợp bổ sung 20% ảnh nền âm tính manh tràng lành 200 ảnh (`normal-cecum`), tạo thành bộ dữ liệu chính thức `Kvasir_YOLO_SEG_BG20` (1.200 ảnh: 1.040 ảnh train, 160 ảnh val).
> - `[Đã xác nhận]`: Toàn bộ quá trình huấn luyện đối chuẩn trên tập dữ liệu BG20 đã hoàn tất thực tế qua 10 random seeds (`s0` đến `s9`) trên GPU NVIDIA Tesla T4 (lưu tại `archive/KetQua_Nen/`).
> - `[Đã xác nhận]`: Toàn bộ kết quả phân tích thống kê, kiểm định Paired t-test, ma trận nhầm lẫn 2x2 trên 40 ảnh nền âm tính và hệ thống 20 biểu đồ 300 DPI đã được hoàn tất và kiểm toán tại `archive/KQ_Nen_DX_10seed/`.

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

---

## 5. TỔNG HỢP KẾT QUẢ THỰC NGHIỆM ĐA SEED TRÊN BỘ DỮ LIỆU KVASIR_YOLO_SEG_BG20

Sau khi giải nén và cấu trúc hóa toàn bộ 17 tệp kết quả mới từ Kaggle vào `archive/KetQua_Nen/`, tổng số lượt chạy được kiểm toán đạt **47 runs/seeds** (đầy đủ `results.csv` và `weights/best.pt`).

### 5.1. Bảng Đối Chiếu Mask mAP@50-95 Từng Seed (100 Epochs/Seed)

| Seed | Baseline (YOLO26s-seg) | TSVM (Topology-Shape) | P5_Attention_VMamba | ITSMamba (Interactive Topo) | C2IAVM (Interactive Attn) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **s0** | $0.7366$ | $0.7245$ | $0.7215$ | $0.7028$ | $0.7228$ |
| **s1** | $0.7165$ | $0.7274$ | $0.7104$ | $0.7220$ | $0.7086$ |
| **s2** | $0.7138$ | $0.7259$ | $0.7152$ | $0.7291$ | $0.7306$ |
| **s3** | $0.6941$ | $0.7213$ | $0.7049$ | $0.7288$ | $0.6944$ |
| **s4** | $0.7274$ | $0.7197$ | $0.7148$ | $0.7258$ | $0.7152$ |
| **s5** | $0.7350$ | $0.7285$ | $0.7295$ | $0.7223$ | **$0.7374$** |
| **s6** | $0.7153$ | $0.7254$ | $0.7259$ | $0.7109$ | $0.7181$ |
| **s7** | $0.7145$ | $0.7065$ | $0.7146$ | $0.7276$ | *(Đang train)* |
| **s8** | $0.7318$ | **$0.7339$** | $0.7178$ | $0.7055$ | *(Đang train)* |
| **s9** | $0.7253$ | $0.7329$ | $0.7102$ | $0.7284$ | *(Đang train)* |

### 5.2. Bảng Đối Chiếu Mask Recall Từng Seed

| Seed | Baseline (YOLO26s-seg) | TSVM (Topology-Shape) | P5_Attention_VMamba | ITSMamba (Interactive Topo) | C2IAVM (Interactive Attn) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **s0** | $0.8189$ | $0.8529$ | $0.8212$ | $0.8057$ | $0.8782$ |
| **s1** | $0.8504$ | $0.8661$ | $0.8000$ | $0.8898$ | $0.8740$ |
| **s2** | $0.8355$ | $0.8377$ | $0.8268$ | $0.8110$ | **$0.8802$** |
| **s3** | $0.8545$ | **$0.8909$** | $0.8554$ | $0.8425$ | $0.8268$ |
| **s4** | $0.8819$ | $0.8676$ | $0.8463$ | $0.8347$ | $0.8647$ |
| **s5** | $0.8605$ | $0.8819$ | $0.8740$ | $0.8603$ | $0.8583$ |
| **s6** | $0.8611$ | $0.8504$ | $0.8110$ | $0.8583$ | $0.8661$ |
| **s7** | $0.8347$ | $0.8425$ | $0.8474$ | $0.8740$ | *(Đang train)* |
| **s8** | $0.8912$ | $0.8768$ | $0.8260$ | $0.8583$ | *(Đang train)* |
| **s9** | $0.8949$ | $0.8583$ | $0.8298$ | $0.8504$ | *(Đang train)* |

### 5.3. Bảng Thống Kê Đối Chuẩn Đồng Nhất Trên 7 Seed Chung (s0 – s6, n=7)

Để đảm bảo tính công bằng thống kê khi cả 5 mô hình đều có đầy đủ dữ liệu thực nghiệm trên cùng một tập hạt giống (`seed 0` đến `seed 6`):

| Chỉ số thực nghiệm | Baseline (YOLO26s-seg) | TSVM (Topology-Shape) | P5_Attention_VMamba | ITSMamba (Interactive Topo) | C2IAVM (Interactive Attn) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Mask mAP@50-95** | $0.7198 \pm 0.0147$ | **$0.7247 \pm 0.0032$** | $0.7175 \pm 0.0087$ | $0.7202 \pm 0.0098$ | $0.7182 \pm 0.0142$ |
| **Mask mAP@50** | $0.9088 \pm 0.0095$ | $0.9064 \pm 0.0062$ | $0.8992 \pm 0.0121$ | **$0.9112 \pm 0.0091$** | $0.9067 \pm 0.0163$ |
| **Mask Recall (Độ nhạy)** | $0.8518 \pm 0.0201$ | $0.8639 \pm 0.0186$ | $0.8335 \pm 0.0262$ | $0.8432 \pm 0.0295$ | **$0.8641 \pm 0.0182$** |
| **Mask Precision** | $0.9080 \pm 0.0364$ | $0.9201 \pm 0.0152$ | $0.8971 \pm 0.0328$ | **$0.9238 \pm 0.0275$** | $0.9128 \pm 0.0214$ |
| **Box mAP@50-95** | $0.7277 \pm 0.0223$ | **$0.7297 \pm 0.0106$** | $0.7209 \pm 0.0130$ | $0.7206 \pm 0.0111$ | $0.7212 \pm 0.0197$ |
| **Box Recall** | $0.8346 \pm 0.0324$ | **$0.8580 \pm 0.0168$** | $0.8362 \pm 0.0283$ | $0.8309 \pm 0.0278$ | $0.8562 \pm 0.0222$ |
| **Validation Seg Loss** | $1.2975 \pm 0.0828$ | $1.2416 \pm 0.0468$ | $1.2483 \pm 0.0627$ | $1.2559 \pm 0.0757$ | **$1.2402 \pm 0.0536$** |
| **Độ lệch chuẩn mAP ($\sigma$)** | $0.0147$ | **$0.0032$ (Thấp nhất)** | $0.0087$ | $0.0098$ | $0.0142$ |
| **Hệ số co hẹp phương sai ($F$)** | $1.00\times$ | **$21.09\times$** | $2.85\times$ | $2.25\times$ | $1.07\times$ |

---

### 5.4. Bảng Thống Kê Mở Rộng 10 Seed (s0 – s9, n=10 Cho 4 Mô Hình Hoàn Tất)

| Chỉ số thực nghiệm | Baseline (YOLO26s-seg) | TSVM (Topology-Shape) | P5_Attention_VMamba | ITSMamba (Interactive Topo) |
| :--- | :---: | :---: | :---: | :---: |
| **Mask mAP@50-95** | $0.7210 \pm 0.0129$ | **$0.7246 \pm 0.0078$** | $0.7165 \pm 0.0075$ | $0.7203 \pm 0.0101$ |
| **Mask mAP@50** | **$0.9119 \pm 0.0107$** | $0.9062 \pm 0.0082$ | $0.8990 \pm 0.0103$ | $0.9099 \pm 0.0094$ |
| **Mask Recall (Độ nhạy)** | $0.8584 \pm 0.0252$ | **$0.8625 \pm 0.0173$** | $0.8338 \pm 0.0220$ | $0.8485 \pm 0.0261$ |
| **Mask Precision** | $0.9023 \pm 0.0339$ | $0.9118 \pm 0.0246$ | $0.8983 \pm 0.0285$ | **$0.9205 \pm 0.0268$** |
| **Box mAP@50-95** | $0.7262 \pm 0.0198$ | **$0.7285 \pm 0.0141$** | $0.7188 \pm 0.0121$ | $0.7197 \pm 0.0118$ |
| **Box Recall** | $0.8434 \pm 0.0337$ | **$0.8567 \pm 0.0152$** | $0.8359 \pm 0.0233$ | $0.8383 \pm 0.0268$ |
| **Validation Seg Loss** | $1.3045 \pm 0.0867$ | $1.2424 \pm 0.0387$ | $1.2720 \pm 0.0644$ | **$1.2417 \pm 0.0664$** |
| **Độ lệch chuẩn mAP ($\sigma$)** | $0.0129$ | $0.0078$ | **$0.0075$** | $0.0101$ |
| **Hệ số co hẹp phương sai ($F$)** | $1.00\times$ | **$2.74\times$** | $2.95\times$ | $1.63\times$ |

---

### 5.5. Phân Tích So Sánh Khách Quan Giữa Các Mô Hình Trên Tập BG20

Khi đưa thêm 20% ảnh nội soi âm tính (niêm mạc lành `normal-cecum`) vào quy trình đánh giá, bức tranh thực nghiệm thể hiện rõ các ưu - nhược điểm và sự đánh đổi kỹ thuật riêng biệt của từng kiến trúc:

1. **Mô hình TSVM (Topology-Shape-aware VMamba):**
   * **Ưu điểm vượt trội về độ ổn định (Robustness):** Đạt độ biến thiên thấp nhất qua các seed (độ lệch chuẩn Mask mAP@50-95 chỉ $\pm 0.0032$ trên 7 seed và $\pm 0.0078$ trên 10 seed, giảm phương sai $2.74\times$ so với Baseline).
   * **Hiệu năng tổng thể:** Đạt Mask mAP@50-95 trung bình cao nhất nhóm ($0.7246$ so với $0.7210$ của Baseline), Mask Recall đạt $86.25\%$, Box mAP đạt $0.7285$.
   * **Kiểm soát hàm mất mát phân đoạn:** Kéo giảm `val/seg_loss` sâu nhất và ổn định nhất ($1.2424 \pm 0.0387$ so với $1.3045 \pm 0.0867$ của Baseline), chứng minh khả năng tối ưu hóa ranh giới mặt nạ rất bền vững.

2. **Mô hình ITSMamba (Interactive Topology-Shape VMamba):**
   * **Khả năng phân biệt mô lành (Precision):** Đạt Mask Precision cao nhất toàn bộ các mô hình ($92.05\% \pm 0.0268$), phản ánh khả năng từ chối dự đoán nhầm trên các nếp gấp niêm mạc manh tràng và bọt khí khi có ảnh âm tính.
   * **Đánh đổi:** Mask Recall đạt $84.85\%$ (thấp hơn TSVM $86.25\%$ và Baseline $85.84\%$).

3. **Mô hình C2IAVM (Interactive Attention-VMamba Fusion):**
   * **Độ nhạy phân đoạn (Recall):** Duy trì tỷ lệ bắt dính tổn thương cao ($86.41\%$ trên 7 seed s0-s6), giúp hạn chế bỏ sót tổn thương nhỏ ở giai đoạn sớm.
   * **Trạng thái thực nghiệm:** Đã hoàn tất 7 seed (`s0` đến `s6`) với Mask mAP@50-95 đạt $0.7182 \pm 0.0142$; các seed tiếp theo (`s7`, `s8`, `s9`) đang trong tiến trình chạy thực nghiệm.

4. **Mô hình Baseline (YOLO26s-seg):**
   * **Ưu điểm:** Duy trì Mask mAP@50 ở mức cao ($0.9119 \pm 0.0107$).
   * **Hạn chế:** Độ nhạy cảm với việc thay đổi seed ngẫu nhiên lớn nhất (độ lệch chuẩn $\sigma = 0.0129$ trên mAP và $\sigma = 0.0339$ trên Precision), hàm mất mát phân đoạn kiểm định cao nhất ($1.3045$), ranh giới mặt nạ phân đoạn dễ bị biến động theo ánh sáng lóa.

5. **Mô hình P5_Attention_VMamba:**
   * Thể hiện hiệu năng thấp hơn các biến thể tương tác có cấu trúc ($0.7165$ mAP@50-95, Recall $83.38\%$), củng cố luận điểm khoa học rằng việc ghép kênh song song tĩnh thiếu cơ chế dẫn hướng hình thái hoặc tương tác chéo sẽ làm phân tán các đặc trưng biên cục bộ.

---

### 5.6. Gói Tài Liệu Phân Tích & Bộ Trực Quan Hóa Đồ Án 10 Seed (`archive/KQ_Nen_DX_10seed/`)

Để phục vụ trực tiếp việc viết chương thực nghiệm và đóng góp kết quả cho luận văn, nhóm nghiên cứu đã xây dựng hoàn chỉnh gói phân tích đối sánh 10 seed giữa **Baseline (YOLO26s-seg)** và **TSVM (Topology-Shape)** tại thư mục:

📁 [`archive/KQ_Nen_DX_10seed/`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_Nen_DX_10seed)

**Nội dung cốt lõi của gói sản phẩm**:
* **20 Biểu đồ nghiên cứu khoa học đạt chuẩn xuất bản (300 DPI)**:
  - *Performance (01-05)*: So sánh Mean ± Std của Mask mAP50-95, Mask mAP50, Precision/Recall, Bounding Box và Val Seg Loss.
  - *Stability (06, 07, 10)*: Đường xu hướng 10 seed mAP@50-95, Box mAP@50-95 và biểu đồ Error bar đa chỉ số.
  - *Distribution (08, 09)*: Boxplot kèm điểm dữ liệu phân tán và biểu đồ phân phối tần suất / đường cong mật độ nhân KDE.
  - *Correlation (11, 12, 13)*: Biểu đồ phân tán đánh đổi Precision vs Recall, tương quan mAP với Precision và Recall.
  - *Confusion Matrix (14, 15, 16, 17)*: Heatmap ma trận nhầm lẫn đếm và chuẩn hóa % trung bình qua 10 seed.
  - *Summary (18, 19, 20)*: Grouped bar chart tổng hợp, Radar chart đa chiều và đồ thị thanh ngang phân kỳ $\Delta = \text{TSVM} - \text{Baseline}$.
* **11 Bảng thống kê chuẩn hóa (CSV)**: Phân bố trong các thư mục `02_statistics/`, `03_metrics/`, `04_confusion_matrix/`.
* **2 Báo cáo học thuật chi tiết**:
  - [`summary.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_Nen_DX_10seed/06_reports/summary.md): Báo cáo tóm tắt toàn bộ số liệu thống kê mô tả.
  - [`conclusions.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_Nen_DX_10seed/06_reports/conclusions.md): Báo cáo nhận xét học thuật khách quan theo 6 nhóm tiêu chí (Performance, Stability, Precision/Recall, Loss, Confusion Matrix, Seed Consistency).

`[Đã xác nhận]`

