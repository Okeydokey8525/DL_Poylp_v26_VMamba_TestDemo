# CURRENT_PROJECT_STATUS — VERIFIED SNAPSHOT

Ngày kiểm tra: 28/09/2026
Repository: Okeydokey8525/DL_Poylp_v26_VMamba_TestDemo
Branch: main

## Source of truth

Current/Verified chỉ gồm thông tin có bằng chứng trực tiếp từ tree, source, config, raw CSV hoặc artifact.

Historical là các thí nghiệm cũ được giữ để truy vết.

Not verified in repository là thông tin chỉ tồn tại ở local/Kaggle hoặc chưa có source/config/artifact trên GitHub.

Khi tài liệu và raw data mâu thuẫn: raw data được ưu tiên.

## Dataset BG20

Kvasir_YOLO_SEG_BG20:
- Total 1,200.
- Train 1,040 = 880 polyp + 160 background.
- Validation 160 = 120 polyp + 40 background.
- 127 ground-truth polyp instances trong 120 ảnh polyp validation.
- 40 ảnh background normal-cecum, label rỗng.

## 10-seed artifacts

Gói chính:
archive/Ket_Qua_V2/KQ_Nen_DX_10seed/

Đủ 10 seed:
- Baseline YOLO26s-seg
- TSVM
- P5 Attention-VMamba
- ITSMamba

IAVM hiện chỉ có 7 seed trong repository.

Nguồn raw:
- 01_raw_analysis/raw_10seeds_extracted_metrics.csv
- 01_raw_analysis/raw_10seeds_confusion_matrices.csv

## Baseline vs TSVM

Mask mAP@50-95:
- Baseline: 0.7210 ± 0.0129
- TSVM: 0.7246 ± 0.0078
- Paired t-test: p = 0.3839

Validation Seg Loss:
- Baseline: 1.3045 ± 0.0867
- TSVM: 1.2424 ± 0.0387
- Paired t-test: p = 0.0908

## TSVM hiện có trong GitHub

Source:
archive/ultralytics_Topology-Shape-aware VMamba/

Config:
archive/ultralytics_Topology-Shape-aware VMamba/cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml

Module:
archive/ultralytics_Topology-Shape-aware VMamba/nn/modules/topology_shape_vmamba.py

Đã xác minh:
- C2TSVMamba tại Layer 10.
- Layer 10 ở P5, 20x20 với input 640x640.
- Có SS2D, ShapeAwareBranch, DirectionalShapeExtractor, TopologyShapeGate, TSVMamba.

## P3/C3k2VSS

Tại thời điểm kiểm tra GitHub main không có:
- C3k2VSS
- yolo26-vmamba-p3-seg.yaml
- source tree riêng cho hướng P3 VMamba mới

Phân loại: NOT VERIFIED IN REPOSITORY.

Nếu local/Kaggle đã có implementation mới, phải push source/config trước khi đổi trạng thái.

## Artifact fuse TSVM

archive/doc/17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md là hồ sơ kỹ thuật cho sự cố final evaluation/fuse và phục hồi artifact TSVM seed 0/5.

## Quy trình cập nhật

1. Cập nhật source/config/artifact.
2. Verify trực tiếp.
3. Cập nhật file này.
4. Cập nhật README và tài liệu liên quan.
5. Giữ tài liệu lịch sử, nhưng sửa phần nào khiến lịch sử bị hiểu nhầm là hiện trạng.

## Quy tắc bắt buộc

Đọc trước khi làm task lớn:
- archive/doc/AI_WORK_OPTIMIZATION_RULE.md
- archive/doc/nguyen-tac-lam-viec-dai.md
