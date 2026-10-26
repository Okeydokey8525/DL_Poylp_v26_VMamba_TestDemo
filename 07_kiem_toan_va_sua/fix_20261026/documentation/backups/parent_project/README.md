# DL_Poylp_v26_VMamba_TestDemo

> Khóa luận: Nghiên cứu phương pháp tích hợp VMamba vào YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng.  
> Snapshot GitHub main được kiểm tra: 28/09/2026.

> [!IMPORTANT]
> Repository chứa nhiều thế hệ thí nghiệm trong archive/. Không phải mọi kiến trúc, dataset và kết quả trong archive đều là trạng thái hiện tại.
>
> Thứ tự ưu tiên: CURRENT_PROJECT_STATUS.md → raw CSV/artifact/config/source → tài liệu lịch sử.
>
> Code mới chỉ tồn tại ở local/Kaggle nhưng chưa push lên GitHub phải được ghi là NOT VERIFIED IN REPOSITORY.

## 1. Trạng thái đã xác minh

### Dataset chính thức BG20

Kvasir_YOLO_SEG_BG20:

- 1.200 ảnh tổng.
- Train: 1.040 = 880 polyp + 160 background.
- Validation: 160 = 120 polyp + 40 background.
- 120 ảnh polyp validation chứa 127 ground-truth instances.
- 40 ảnh background dùng normal-cecum với label rỗng.

Metadata và artifact chính nằm dưới archive/Ket_Qua_V2/.

### Bộ 10 seed

archive/Ket_Qua_V2/KQ_Nen_DX_10seed/ chứa bộ phân tích 10 seed cho:

1. Baseline YOLO26s-seg
2. TSVM
3. P5 Attention-VMamba
4. ITSMamba

IAVM chưa đủ 10 seed trong repository và không được trộn vào bộ 10-seed đầy đủ.

Nguồn raw ưu tiên:

- 01_raw_analysis/raw_10seeds_extracted_metrics.csv
- 01_raw_analysis/raw_10seeds_confusion_matrices.csv
- 02_statistics/mean_std/full_comparison_mean_std.csv
- 02_statistics/min_max/metrics_min_max_range.csv

Mask mAP@50-95, Mean ± Sample Std:

| Model | Value |
|---|---:|
| Baseline | 0.7210 ± 0.0129 |
| TSVM | 0.7246 ± 0.0078 |

Paired t-test: p = 0.3839. Không gọi khác biệt này là có ý nghĩa thống kê ở alpha = 0.05.

## 2. Kiến trúc TSVM hiện có trên GitHub

Source:
archive/ultralytics_Topology-Shape-aware VMamba/

Config:
archive/ultralytics_Topology-Shape-aware VMamba/cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml

Module:
archive/ultralytics_Topology-Shape-aware VMamba/nn/modules/topology_shape_vmamba.py

Đã xác minh:

- C2TSVMamba tại Layer 10.
- Layer 10 thuộc P5; với input 640x640, feature map là 20x20.
- Source có SS2D, ShapeAwareBranch, DirectionalShapeExtractor, TopologyShapeGate và TSVMamba.
- Segmentation head sử dụng feature P3/P4/P5.

## 3. P3 VMamba mới — chưa đồng bộ

Workspace/Kaggle có thể đang theo dõi hướng mới với C3k2VSS và yolo26-vmamba-p3-seg.yaml.

Tuy nhiên tree GitHub main ngày 28/09/2026 không có các file/source này.

Vì vậy hiện tại phải ghi:

**P3/C3k2VSS = NOT VERIFIED IN REPOSITORY.**

Không được cập nhật tài liệu thành “code hiện có” cho tới khi source/config được push lên GitHub.

## 4. Cấu trúc repository thực tế

DL_Poylp_v26_VMamba_TestDemo/
- README.md
- CURRENT_PROJECT_STATUS.md
- BAO_CAO_DAC_TA_HUONG_NGHIEN_CUU.md
- analyze_runs.py
- analyze_runs_p1.py
- implementation_plan.md
- task.md
- walkthrough.md
- data_prep/
- datasets/
- tests/
- archive/
  - Ket_Qua_V1/
  - Ket_Qua_V2/
  - Kvasir-SEG/
  - Cac_Dataset/
  - Stracth/
  - doc/
  - ultralytics_Topology-Shape-aware VMamba/

Các tên cũ như archive/Ket_Qua/, archive/KQ_Poylp/ và archive/Kvasir_YOLO_SEG/ không phải cấu trúc hiện tại của GitHub main.

## 5. Knowledge Base

Hai quy tắc bắt buộc:

- archive/doc/AI_WORK_OPTIMIZATION_RULE.md
- archive/doc/nguyen-tac-lam-viec-dai.md

Tài liệu trạng thái:

- CURRENT_PROJECT_STATUS.md
- archive/doc/CURRENT_PROJECT_STATUS.md

Knowledge Base:

- archive/doc/README.md
- archive/doc/LICHSU_CAP_NHAT.md
- các hồ sơ kỹ thuật 00 đến 17 trong archive/doc/

AI nên đọc theo thứ tự:
1. AI_WORK_OPTIMIZATION_RULE.md
2. nguyen-tac-lam-viec-dai.md
3. CURRENT_PROJECT_STATUS.md
4. README.md
5. Chỉ đọc hồ sơ lịch sử liên quan task.

## 6. Pipeline semantic phụ trợ

Các file:

- data_prep/prepare_kvasir_semantic.py
- datasets/kvasir_semantic_dataset.py
- tests/unit/
- tests/integration/

được giữ cho pipeline chuẩn bị Kvasir-SEG semantic segmentation phục vụ nghiên cứu như U-Net/PraNet.

implementation_plan.md, task.md và walkthrough.md mô tả pipeline phụ trợ này; không được hiểu nhầm là pipeline huấn luyện chính BG20 YOLO26s.

## 7. Quy tắc tài liệu và số liệu

- Không sửa raw CSV để làm khớp báo cáo.
- Không tự tạo số liệu.
- Không gọi một kiến trúc là current nếu chưa có source/config/artifact xác minh.
- Không gọi topology-aware đầy đủ chỉ dựa trên tên module.
- Khi có xung đột, raw data và source thực tế được ưu tiên.
- Tài liệu cũ được giữ để truy vết, nhưng phải phân biệt rõ Historical với Current/Verified.

## 8. Luồng đồng bộ chuẩn

Local/Kaggle code
→ verify
→ push source/config/artifact cần thiết
→ update CURRENT_PROJECT_STATUS.md
→ update README và tài liệu kỹ thuật liên quan.

## 9. Disclaimer

Dự án phục vụ học tập, nghiên cứu khoa học và khóa luận. Kết quả phân đoạn không thay thế chẩn đoán hoặc quyết định điều trị y khoa.
