# ⚙️ MÔI TRƯỜNG THIẾT LẬP & TÁI CHẠY TOÀN BỘ PIPELINE
## Hướng dẫn cài đặt và chạy lại từ đầu

> **Ngày lập:** 02/10/2026
> **Đối tượng:** AI hoặc thành viên mới cần tái tạo số liệu / biểu đồ / báo cáo

---

## 1. MÔI TRƯỜNG ĐÃ XÁC NHẬN

| Thành phần | Phiên bản / Giá trị |
| :--- | :--- |
| Hệ điều hành | Windows (đường dẫn trong tài liệu dùng `c:\LeDucLuong\HK VII\...`) |
| Python | **3.13.14** |
| pandas | 3.0.5 |
| numpy | 2.5.1 |
| scipy | 1.18.1 |
| GPU huấn luyện | Kaggle — NVIDIA Tesla T4 |
| Mã nguồn Ultralytics (fork) | `ultralytics_Topology-Shape-aware VMamba/` — bản fork có nhánh **One-to-Many** |

### Thư viện cần cài thêm

```powershell
pip install pandas numpy scipy matplotlib seaborn pillow
pip install rapidocr-onnxruntime        # chỉ cần khi OCR confusion_matrix.png
```

> ⚠️ **Không cài `ultralytics` từ PyPI.** Phải dùng bản fork trong thư mục `ultralytics_Topology-Shape-aware VMamba/` vì kiến trúc `Segment26` với nhánh One-to-Many là thay đổi tùy biến. Thêm vào `sys.path` **trước** khi import.

```python
import sys
repo = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\ultralytics_Topology-Shape-aware VMamba"
if repo not in sys.path:
    sys.path.insert(0, repo)
```

---

## 2. BIẾN MÔI TRƯỜNG BẮT BUỘC

Để tiết kiệm thời gian sửa từng script, đặt các biến sau trước khi chạy:

```powershell
$env:PYTHONIOENCODING = "utf-8"                    # bắt buộc: tiếng Việt trong console
$env:KETQUA_V2 = "c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Ket_Qua_V2"
$env:STracH = "c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth"
```

> 🔴 **Cảnh báo đường dẫn hardcode.** Tại thời điểm lập tài liệu này, các script dưới đây **vẫn hardcode** `ROOT_OUT = ".../archive/Ket_Qua_V2/KQ_Nen_DX_10seed"` — **thiếu đoạn `Ket_Qua_V2/`**. Phải sửa dòng khai báo trước khi chạy:

| Script | Biến cần sửa | Đổi thành |
| :--- | :--- | :--- |
| `generate_10seed_thesis_package.py` | `ROOT_OUT` (dòng 13) | `.../archive/Ket_Qua_V2/KQ_Nen_DX_10seed` |
| `render_kq_doixung_templates_2models.py` | `fig_dir` (dòng 12) | `.../archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures` |
| `plot_efficiency_charts_2models.py` | `target_fig_dirs` | `.../archive/Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/figures` |

---

## 3. CẤU TRÚC THƯ MỤC CẦN CÓ

```
archive/
├── Ket_Qua_V2/
│   ├── KetQua_Nen/                        ← DỮ LIỆU GỐC, KHÔNG BAO GIỜ SỬA
│   │   ├── YOLOv26s-seg/
│   │   │   └── Kvasir_BG20_Baseline_YOLO26s_seg_s{0..9}_w2/
│   │   │       ├── results.csv             ← nguồn số liệu duy nhất
│   │   │       ├── confusion_matrix.png
│   │   │       └── weights/best.pt
│   │   └── Kvasir_BG20_YOLO26s_seg_TSVM/
│   │       └── Kvasir_BG20_YOLO26s_seg_TSVM_s{0..9}_w2/
│   │           ├── results.csv
│   │           ├── confusion_matrix.png
│   │           └── weights/best.pt
│   ├── KQ_Nen_DX_10seed/                  ← gói kết quả phái sinh
│   │   ├── 01_raw_analysis/ … 06_reports/
│   │   ├── 07_audit/                      ← sinh ra bởi verify_10seed_audit.py
│   │   ├── 05_charts/  figures/
│   │   └── efficiency_benchmark/
│   ├── Kvasir_YOLO_SEG_BG20/               ← dataset (images/, labels/)
│   └── efficiency_benchmark/
├── Stracth/                               ← 46 script Python
├── ultralytics_Topology-Shape-aware VMamba/  ← fork Ultralytics
└── data_bg20.yaml                         ← cấu hình dataset
```

---

## 4. QUY TRÌNH TÁI CHẠY

### Bước 1 — Kiểm chứng (luôn làm trước, mất ~30 giây)

```powershell
python .\Stracth\verify_10seed_audit.py
```

**Kết quả mong đợi:** `694/694 phép kiểm ĐẠT, 0 KHÔNG ĐẠT`, mã thoát `0`.

Báo cáo sinh ra:
- `Ket_Qua_V2/KQ_Nen_DX_10seed/07_audit/audit_report.md`
- `Ket_Qua_V2/KQ_Nen_DX_10seed/07_audit/audit_report.csv`
- `Ket_Qua_V2/KQ_Nen_DX_10seed/07_audit/reextracted_from_results_csv.csv`

> Nếu có FAIL: **đừng sửa CSV gốc.** Kiểm tra xem báo cáo hay script sinh dữ liệu sai.

### Bước 2 — Tái sinh bảng thống kê + biểu đồ khoa học

```powershell
# Sửa ROOT_OUT trước (xem mục 2)
python .\Stracth\generate_10seed_thesis_package.py
```

Sinh lại: `01_raw_analysis`, `02_statistics`, `03_metrics`, `04_confusion_matrix`, `05_charts`, `06_reports`.

> ⚠️ **Ghi đè toàn bộ CSV trong `01`–`06`.** Chạy lại chỉ an toàn khi chưa có chỉnh sửa thủ công nào đáng giữ. Nếu đã chỉnh, sao lưu trước.
> ⚠️ Script **nạp** `raw_10seeds_confusion_matrices.csv` từ `01_raw_analysis` như đầu vào cố định — nó **không** tự tính lại ma trận nhầm lẫn.

### Bước 3 — Tái sinh 12 biểu đồ mẫu

```powershell
# Sửa fig_dir trước
python .\Stracth\render_kq_doixung_templates_2models.py
```

Sinh lại thư mục `figures/` (12 hình).

### Bước 4 — Tái sinh biểu đồ hiệu năng phần cứng

```powershell
python .\Stracth\benchmark_runner.py                    # đo đạc (cần GPU)
python .\Stracth\plot_efficiency_charts_2models.py     # vẽ 15 hình
```

### Bước 5 — Tái tạo báo cáo Word (P0-1)

```powershell
python .\Stracth\generate_final_word_report.py
```

Sinh `CNTT_KLCN182_LeDucLuong.docx`. **Đã sửa ở v3.1** — bản tạo ra có số liệu đúng.

### Bước 6 — Kiểm chứng lại sau khi chạy

```powershell
python .\Stracth\verify_10seed_audit.py
```

---

## 5. SỬA LỖI MA TRẬN NHẨM LẪN (nhiệm vụ P1-1/P1-2)

### 5.1. Vì sao cần

Ô background↔background luôn = 0 do thiếu nhánh cộng trong `ConfusionMatrix.process_batch`. Cách khắc phục: tự đếm bằng bộ đếm riêng ngoài Ultralytics.

### 5.2. Nguyên tắc đếm

```
Ma trận = matrix[predicted, true]     # ultralytics/utils/metrics.py
X = "True",  Y = "Predicted"          # hàm plot(), dòng 591-592

                    True=polyp   True=background
Pred=polyp              TP            FP
Pred=background          FN            TN
```

### 5.3. Vì sao 3 seed TSVM (s0, s5, s8) bị sai

| Run | `results.csv` cho thấy | `confusion_matrix.png` cho thấy |
| :--- | :--- | :--- |
| `s0` | recall 0.853, mAP@50 0.904 (bình thường) | TP=59/127 — suy giảm |
| `s5` | recall 0.882, mAP@50 0.910 (bình thường) | TP=0/127 — hoàn toàn hỏng |
| `s8` | recall 0.877, mAP@50 0.910 (bình thường) | TP=6/127 — gần như hỏng |

Dấu hiệu "TP = 0, FN = 127, FP rất lớn" là đặc trưng của **lỗi one-to-many / end2-end** khiến lớp dự đoán sai — cùng loại lỗi đã mô tả ở [`17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md`](17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md).

### 5.4. Cách tái tạo

```python
# Nguyên mẫu: Stracth/check_gt_matching.py (đã có sẵn trong repo)
import sys, torch
repo = r"...\archive\ultralytics_Topology-Shape-aware VMamba"
sys.path.insert(0, repo)

from ultralytics.nn import autobackend
from ultralytics.data.utils import check_det_dataset
from ultralytics.models.yolo.segment import SegmentationValidator
from ultralytics.nn.modules.head import Detect

# BẮT BUỘC — vô hiệu hóa end2end (nguyên nhân gốc xem doc/17)
Detect.end2end = property(fget=lambda self: False,
                          fset=lambda self, v: setattr(self, '_end2end', v))

ckpt = r"...\KetQua_V2\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM\Kvasir_BG20_YOLO26s_seg_TSVM_s0_w2\weights\best.pt"
data = r"...\archive\data_bg20.yaml"

val = SegmentationValidator(args=dict(model=ckpt, data=data, device="cuda",
                                      batch=8, imgsz=640, end2end=False,
                                      conf=0.25, workers=0))
# ... chạy val, tự đếm TP/FP/FN/TN cho 40 ảnh nền và 127 thực thể polyp
```

> ⚠️ `conf` mặc định của ma trận nhầm lẫn là **0.25** (khác `0.001` dùng cho PR/mAP). Giữ đúng 0.25 để so sánh được.

---

## 6. XỬ LÝ SỰ CỐ THƯỜNG GẶP

| Triệu chứng | Nguyên nhân | Cách xử lý |
| :--- | :--- | :--- |
| `UnicodeEncodeError: 'charmap' codec` | Console Windows dùng cp1252 | Đặt `$env:PYTHONIOENCODING="utf-8"` |
| `FileNotFoundError` khi chạy script sinh dữ liệu | Đường dẫn hardcode thiếu `Ket_Qua_V2/` | Sửa `ROOT_OUT` / `fig_dir` (mục 2) |
| `AttributeError: 'Path' object has no attribute 'model'` | Quên `pd.read_csv()` trước khi truy vấn | Xem `Stracth/verify_10seed_audit.py` mục 8 làm mẫu |
| Import `ultralytics` sai phiên bản | Cài bản PyPI thay vì fork | `sys.path.insert(0, repo)` **trước** mọi import |
| Dự đoán toàn ảnh về background | Nhánh One-to-One chưa hội tụ / `end2end` bật | Vô hiệu hóa `Detect.end2end`, xem `doc/17` |
| Ảnh `val_batch*_pred.jpg` rỗng | Lỗi thứ tự tọa độ Pillow 10+ | Đã có patch trong `Stracth/kaggle_val_fix_guide.py` |
| Ma trận nhầm lẫn ô TN trống | **Không phải lỗi** — hành vi đúng của Ultralytics | Không cần sửa; chỉ cần nêu cảnh báo trong báo cáo |

---

## 7. KIỂM TRA NHANH TRƯỚC KHI NỘP

```powershell
# 1. Số liệu toàn vẹn
python .\Stracth\verify_10seed_audit.py                        # kỳ vọng: 694/694, exit 0

# 2. Đường dẫn trong tài liệu còn sống
python .\Stracth\check_doc_paths.py                             # kỳ vọng: 0 đường dẫn chết

# 3. Hình ảnh khuyến nghị tồn tại
python .\Stracth\check_figures_exist.py                         # kỳ vọng: 43/43
```

> Hai script kiểm tra mục 2 và 3 được đề xuất bổ sung — xem [`24_DANH_SACH_DUONG_DAN_HONG.md`](24_DANH_SACH_DUONG_DAN_HONG.md).

---

*Đề xuất cập nhật tài liệu này mỗi khi đổi phiên bản mô hình hoặc cấu trúc thư mục.*
