# CURRENT PROJECT STATUS — VERIFIED SNAPSHOT

> **Ngày kiểm tra:** 28/09/2026  
> **Nguồn kiểm tra:** repository GitHub `Okeydokey8525/DL_Poylp_v26_VMamba_TestDemo`, nhánh `main`.  
> **Mục đích:** Đây là tài liệu trạng thái hiện tại được ưu tiên khi các tài liệu lịch sử trong `archive/doc/` có thông tin khác nhau.

## 1. Quy tắc đọc tài liệu

- **Current / Verified:** Chỉ ghi thông tin có thể đối chiếu trực tiếp với tree, code, config, CSV hoặc artifact đang có trong repository.
- **Historical:** Các thí nghiệm/kiến trúc cũ vẫn được giữ để truy vết nhưng không được dùng mặc định để mô tả trạng thái hiện tại.
- **Not verified in repository:** Không ghi một kiến trúc, kết quả hoặc đường dẫn là hiện tại nếu repository không chứa bằng chứng tương ứng.
- Khi có xung đột giữa báo cáo tổng hợp và raw data, **raw data được ưu tiên**; báo cáo phải được sửa theo raw data.

## 2. Trạng thái repository

Repository hiện có mã nguồn nghiên cứu, dataset/pipeline, artifact huấn luyện, các gói phân tích 10-seed và nhiều tài liệu lịch sử trong `archive/`.

Đáng chú ý, repository hiện **không có** các đường dẫn sau:

- `C3k2VSS`
- `yolo26-vmamba-p3-seg.yaml`
- một source tree riêng cho hướng P3 VMamba mới

Do đó, các thông tin về kiến trúc P3 mới chỉ nên được xem là **trạng thái ngoài repository / chưa đồng bộ vào GitHub**, không được mô tả như code hiện có trong repo này.

## 3. Dataset chính thức của các thực nghiệm BG20

Repository hiện lưu bộ dữ liệu/metadata liên quan đến:

`Kvasir_YOLO_SEG_BG20`

Quy mô được tài liệu và artifact hiện tại mô tả:

- 1.000 ảnh Kvasir-SEG có polyp.
- Bổ sung 200 ảnh nền âm tính `normal-cecum`.
- Tổng: **1.200 ảnh**.
- Train: **1.040 ảnh = 880 polyp + 160 nền**.
- Validation: **160 ảnh = 120 ảnh polyp + 40 nền**.
- 120 ảnh polyp validation chứa **127 ground-truth polyp instances**.
- Các file label của ảnh nền được để rỗng (0 byte).

## 4. Bộ kết quả 10-seed hiện có

`archive/Ket_Qua_V2/KQ_Nen_DX_10seed/01_raw_analysis/raw_10seeds_extracted_metrics.csv` hiện chứa **4 mô hình × 10 seed**:

1. Baseline
2. TSVM
3. P5_Attention_VMamba
4. ITS Mamba

Riêng IAVM không thuộc bộ 10-seed đầy đủ này; artifact trong repository chỉ có 7 seed cho IAVM. Vì vậy không được trộn IAVM vào bảng 10-seed đầy đủ nếu chưa bổ sung đủ seed.

Gói `KQ_Nen_DX_10seed` hiện là bộ đối sánh **Baseline vs TSVM**; các mô hình khác được lưu trong raw/analysis để phục vụ khảo sát rộng hơn.

## 5. Số liệu Baseline vs TSVM phải dùng

Nguồn chuẩn cho bộ đối sánh là:

- `01_raw_analysis/raw_10seeds_extracted_metrics.csv`
- `01_raw_analysis/raw_10seeds_confusion_matrices.csv`
- `02_statistics/mean_std/full_comparison_mean_std.csv`
- `02_statistics/min_max/metrics_min_max_range.csv`

Các giá trị Mean ± Sample Std của Mask mAP@50-95:

| Model | Mask mAP@50-95 |
|---|---:|
| Baseline | **0.7210 ± 0.0129** |
| TSVM | **0.7246 ± 0.0078** |

Paired t-test cho Mask mAP@50-95: **p = 0.3839**, do đó không được mô tả là có ý nghĩa thống kê ở α = 0.05.

Validation Segmentation Loss:

| Model | Val Seg Loss |
|---|---:|
| Baseline | **1.3045 ± 0.0867** |
| TSVM | **1.2424 ± 0.0387** |

Paired t-test: **p = 0.0908**. Có thể mô tả là xu hướng giảm / gần ngưỡng α = 0.10, nhưng không được gọi là có ý nghĩa thống kê ở α = 0.05.

## 6. Confusion Matrix — số liệu đã đối chiếu raw CSV

Từ `raw_10seeds_confusion_matrices.csv`:

- Baseline mean: **TP 110.3, FN 16.7, FP 16.8, TN 23.2**.
- TSVM mean: **TP 111.2, FN 15.8, FP 14.6, TN 25.4**.

Ràng buộc dữ liệu:

- TP + FN = 127 cho mỗi seed/model.
- FP + TN = 40 cho mỗi seed/model.

Không được dùng các giá trị CM khác xuất hiện trong tài liệu cũ nếu chúng không khớp raw CSV.

## 7. Kiến trúc TSVM hiện có trong repository

Source tree hiện có:

`archive/ultralytics_Topology-Shape-aware VMamba/`

Config:

`archive/ultralytics_Topology-Shape-aware VMamba/cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml`

Config này đặt:

- `C2TSVMamba` tại **Layer 10**.
- Layer 10 nằm ở P5 / 20×20.
- Head kết nối lại feature P5 tại layer 22.
- Segmentation head dùng các feature P3/P4/P5.

Implementation module:

`archive/ultralytics_Topology-Shape-aware VMamba/nn/modules/topology_shape_vmamba.py`

Trong source này có các thành phần như `SS2D`, `ShapeAwareBranch`, `DirectionalShapeExtractor`, `TopologyShapeGate` và `TSVMamba`.

## 8. Phân loại tài liệu

### Có thể dùng làm nguồn hiện trạng
- File này.
- Raw CSV và các bảng thống kê được sinh từ raw CSV.
- Config/source thực tế đang tồn tại trong repository.
- `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/` cho kết quả 10-seed tương ứng.

### Historical / cần đọc với ngữ cảnh
Các hồ sơ nghiên cứu cũ trong `archive/doc/`, đặc biệt những tài liệu mô tả 6-seed, Kvasir-SEG thuần 1.000 ảnh, C2IAVM hoặc các hướng kiến trúc cũ.

Các tài liệu lịch sử không bị xóa chỉ vì đã cũ; chúng được giữ để truy vết quá trình nghiên cứu.

## 9. Quy tắc cập nhật từ nay

Khi code/kiến trúc/dataset thay đổi:

1. Cập nhật artifact/code trước.
2. Kiểm tra bằng chứng thực tế.
3. Cập nhật tài liệu Current/Verified.
4. Tài liệu cũ chỉ sửa nếu nó đang trình bày thông tin lịch sử như trạng thái hiện tại.
5. Không sửa raw CSV để làm khớp báo cáo.
6. Không đưa số liệu mới vào tài liệu nếu chưa có artifact chứng minh.

## 10. Giới hạn quan trọng

Tài liệu này chỉ phản ánh **repository GitHub tại thời điểm kiểm tra**. Nếu workspace/Kaggle/local project đã có code mới hơn nhưng chưa push lên repository, trạng thái đó chưa thể được xác nhận từ GitHub.

