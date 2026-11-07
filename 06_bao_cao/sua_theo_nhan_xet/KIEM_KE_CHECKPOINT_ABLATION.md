# Kiểm kê checkpoint ablation (07/11/2026)

Chỉ đọc thư mục `03_ket_qua_huan_luyen/` trên máy Lương; không tải, không sửa, không train.
Mask mAP50–95 lớn nhất lấy từ cột `metrics/mAP50-95(M)` trong `results.csv`.

## Tổng kết

| Biến thể | Số seed đủ best.pt, 100 epoch, seed khớp | Số lượt tìm thấy |
|---|---|---|
| Vmamba_only | 10 | 10 |
| Shape_only | 10 | 10 |
| No_guidance | 10 | 10 |

## Chi tiết

| Biến thể | Seed | Có best.pt | Vị trí | Kích thước | Số epoch | Mask mAP50–95 lớn nhất | Seed trong args.yaml (tệp model) |
|---|---|---|---|---|---|---|---|
| Vmamba_only | 0 | có | `03_ket_qua_huan_luyen/Vmamba_only/Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s0_w2/weights/best.pt` | 44.5 MiB | 100 | 0.7145 | 0 (yolo26s-seg-TSVM-ABL-vmamba_only.yaml) |
| Vmamba_only | 1 | có | `03_ket_qua_huan_luyen/Vmamba_only/Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s1_w2/weights/best.pt` | 44.5 MiB | 100 | 0.7389 | 1 (yolo26s-seg-TSVM-ABL-vmamba_only.yaml) |
| Vmamba_only | 2 | có | `03_ket_qua_huan_luyen/Vmamba_only/Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s2_w2/weights/best.pt` | 44.5 MiB | 100 | 0.7145 | 2 (yolo26s-seg-TSVM-ABL-vmamba_only.yaml) |
| Vmamba_only | 3 | có | `03_ket_qua_huan_luyen/Vmamba_only/Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s3_w2/weights/best.pt` | 44.5 MiB | 100 | 0.7115 | 3 (yolo26s-seg-TSVM-ABL-vmamba_only.yaml) |
| Vmamba_only | 4 | có | `03_ket_qua_huan_luyen/Vmamba_only/Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s4_w2/weights/best.pt` | 44.5 MiB | 100 | 0.7054 | 4 (yolo26s-seg-TSVM-ABL-vmamba_only.yaml) |
| Vmamba_only | 5 | có | `03_ket_qua_huan_luyen/Vmamba_only/Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s5_w2/weights/best.pt` | 44.5 MiB | 100 | 0.7290 | 5 (yolo26s-seg-TSVM-ABL-vmamba_only.yaml) |
| Vmamba_only | 6 | có | `03_ket_qua_huan_luyen/Vmamba_only/Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s6_w2/weights/best.pt` | 44.5 MiB | 100 | 0.7229 | 6 (yolo26s-seg-TSVM-ABL-vmamba_only.yaml) |
| Vmamba_only | 7 | có | `03_ket_qua_huan_luyen/Vmamba_only/Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s7_w2/weights/best.pt` | 44.5 MiB | 100 | 0.7264 | 7 (yolo26s-seg-TSVM-ABL-vmamba_only.yaml) |
| Vmamba_only | 8 | có | `03_ket_qua_huan_luyen/Vmamba_only/Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s8_w2/weights/best.pt` | 44.5 MiB | 100 | 0.7125 | 8 (yolo26s-seg-TSVM-ABL-vmamba_only.yaml) |
| Vmamba_only | 9 | có | `03_ket_qua_huan_luyen/Vmamba_only/Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s9_w2/weights/best.pt` | 44.5 MiB | 100 | 0.7131 | 9 (yolo26s-seg-TSVM-ABL-vmamba_only.yaml) |
| Shape_only | 0 | có | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s0_w2/weights/best.pt` | 45.5 MiB | 100 | 0.7107 | 0 (yolo26s-seg-TSVM-ABL-shape_only.yaml) |
| Shape_only | 1 | có | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s1_w2/weights/best.pt` | 45.5 MiB | 100 | 0.7091 | 1 (yolo26s-seg-TSVM-ABL-shape_only.yaml) |
| Shape_only | 2 | có | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s2_w2/weights/best.pt` | 45.5 MiB | 100 | 0.7049 | 2 (yolo26s-seg-TSVM-ABL-shape_only.yaml) |
| Shape_only | 3 | có | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s3_w2/weights/best.pt` | 45.5 MiB | 100 | 0.7296 | 3 (yolo26s-seg-TSVM-ABL-shape_only.yaml) |
| Shape_only | 4 | có | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s4_w2/weights/best.pt` | 45.5 MiB | 100 | 0.7095 | 4 (yolo26s-seg-TSVM-ABL-shape_only.yaml) |
| Shape_only | 5 | có | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s5_w2/weights/best.pt` | 45.5 MiB | 100 | 0.7205 | 5 (yolo26s-seg-TSVM-ABL-shape_only.yaml) |
| Shape_only | 6 | có | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s6_w2/weights/best.pt` | 45.5 MiB | 100 | 0.7229 | 6 (yolo26s-seg-TSVM-ABL-shape_only.yaml) |
| Shape_only | 7 | có | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s7_w2/weights/best.pt` | 45.5 MiB | 100 | 0.7215 | 7 (yolo26s-seg-TSVM-ABL-shape_only.yaml) |
| Shape_only | 8 | có | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s8_w2/weights/best.pt` | 45.5 MiB | 100 | 0.7129 | 8 (yolo26s-seg-TSVM-ABL-shape_only.yaml) |
| Shape_only | 9 | có | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s9_w2/weights/best.pt` | 45.5 MiB | 100 | 0.7225 | 9 (yolo26s-seg-TSVM-ABL-shape_only.yaml) |
| No_guidance | 0 | có | `03_ket_qua_huan_luyen/No_guidance/Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s0_w2/weights/best.pt` | 47.1 MiB | 100 | 0.7160 | 0 (yolo26s-seg-TSVM-ABL-shape_vmamba_no_guidance.yaml) |
| No_guidance | 1 | có | `03_ket_qua_huan_luyen/No_guidance/Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s1_w2/weights/best.pt` | 47.1 MiB | 100 | 0.7275 | 1 (yolo26s-seg-TSVM-ABL-shape_vmamba_no_guidance.yaml) |
| No_guidance | 2 | có | `03_ket_qua_huan_luyen/No_guidance/Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s2_w2/weights/best.pt` | 47.1 MiB | 100 | 0.7209 | 2 (yolo26s-seg-TSVM-ABL-shape_vmamba_no_guidance.yaml) |
| No_guidance | 3 | có | `03_ket_qua_huan_luyen/No_guidance/Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s3_w2/weights/best.pt` | 47.1 MiB | 100 | 0.7172 | 3 (yolo26s-seg-TSVM-ABL-shape_vmamba_no_guidance.yaml) |
| No_guidance | 4 | có | `03_ket_qua_huan_luyen/No_guidance/Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s4_w2/weights/best.pt` | 47.1 MiB | 100 | 0.7193 | 4 (yolo26s-seg-TSVM-ABL-shape_vmamba_no_guidance.yaml) |
| No_guidance | 5 | có | `03_ket_qua_huan_luyen/No_guidance/Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s5_w2/weights/best.pt` | 47.1 MiB | 100 | 0.7263 | 5 (yolo26s-seg-TSVM-ABL-shape_vmamba_no_guidance.yaml) |
| No_guidance | 6 | có | `03_ket_qua_huan_luyen/No_guidance/Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s6_w2/weights/best.pt` | 47.1 MiB | 100 | 0.7082 | 6 (yolo26s-seg-TSVM-ABL-shape_vmamba_no_guidance.yaml) |
| No_guidance | 7 | có | `03_ket_qua_huan_luyen/No_guidance/Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s7_w2/weights/best.pt` | 47.1 MiB | 100 | 0.7173 | 7 (yolo26s-seg-TSVM-ABL-shape_vmamba_no_guidance.yaml) |
| No_guidance | 8 | có | `03_ket_qua_huan_luyen/No_guidance/Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s8_w2/weights/best.pt` | 47.1 MiB | 100 | 0.7298 | 8 (yolo26s-seg-TSVM-ABL-shape_vmamba_no_guidance.yaml) |
| No_guidance | 9 | có | `03_ket_qua_huan_luyen/No_guidance/Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s9_w2/weights/best.pt` | 47.1 MiB | 100 | 0.7176 | 9 (yolo26s-seg-TSVM-ABL-shape_vmamba_no_guidance.yaml) |

## Lượt không tìm thấy hoặc có lỗi

- Không có.
