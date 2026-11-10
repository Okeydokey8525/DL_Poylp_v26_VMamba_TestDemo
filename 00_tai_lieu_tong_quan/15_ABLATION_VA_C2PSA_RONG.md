# 15. Thí nghiệm tách thành phần (ablation) và đối chứng C2PSA rộng, 20 seed

Bổ sung 10/11/2026. Số khớp Bảng 4.7 của bản Word cuối.

**Nguồn:**
- [scripts/tinh_ablation.py](scripts/tinh_ablation.py) → [bang/ablation_20seed/17_ablation_tung_seed.csv](bang/ablation_20seed/17_ablation_tung_seed.csv), [17b_ablation_tong_hop.csv](bang/ablation_20seed/17b_ablation_tong_hop.csv), [18_ablation_cau_hinh_args.csv](bang/ablation_20seed/18_ablation_cau_hinh_args.csv);
- [scripts/tinh_c2psa_rong.py](scripts/tinh_c2psa_rong.py) → [bang/ablation_20seed/19_c2psa_rong_tung_seed.csv](bang/ablation_20seed/19_c2psa_rong_tung_seed.csv), [19b_c2psa_rong_tong_hop.csv](bang/ablation_20seed/19b_c2psa_rong_tong_hop.csv), [19c_c2psa_rong_cau_hinh_args.csv](bang/ablation_20seed/19c_c2psa_rong_cau_hinh_args.csv);
- dữ liệu gốc: `03_ket_qua_huan_luyen/{Vmamba_only, Shape_only, No_guidance, C2PSA_rong}/`, seed 0–19, mỗi lượt 100 epoch.

Cả hai script chạy với `--torch` để đếm số tham số từ `best.pt`. Mọi tham số huấn luyện khác lượt TSVM chính cùng seed: 0 (bảng 18, 19c).

## Các biến thể

| Biến thể | Tầng 10 | Tham số tầng 10 | Tổng tham số |
|---|---|---:|---:|
| YOLO26s-seg (gốc) | C2PSA | 990.976 | 11.434.463 |
| TSVM đầy đủ (đề xuất) | C2TSVMamba: SS2D + nhánh hình dạng + cổng | 1.811.201 | 12.254.688 |
| `vmamba_only` | chỉ SS2D | 1.071.873 | 11.515.360 |
| `shape_only` | chỉ nhánh hình dạng | 1.331.969 | 11.775.456 |
| `shape_vmamba_no_guidance` | SS2D + nhánh hình dạng, bỏ cổng | 1.745.409 | 12.188.896 |
| C2PSA rộng | C2PSA, hệ số kênh ẩn 0,5 → 0,75 (cùng cỡ tham số với TSVM) | 1.830.016 | 12.273.503 |

## Kết quả mask mAP50–95 (mean ± SD, 20 seed)

| Biến thể | mAP50–95 | Δ so với TSVM đầy đủ [KTC 95%] | p (t ghép cặp) | TSVM cao hơn | Δ so với gốc | p |
|---|---:|---:|---:|---:|---:|---:|
| Gốc | 0,7189 ± 0,0118 | −0,0043 [−0,0088; 0,0002] | 0,061 | 13/20 | | |
| **TSVM đầy đủ** | **0,7232 ± 0,0072** | | | | +0,0043 | 0,061 |
| `vmamba_only` | 0,7192 ± 0,0105 | −0,0040 [−0,0098; 0,0019] | 0,173 | 13/20 | +0,0003 | 0,922 |
| `shape_only` | 0,7188 ± 0,0093 | −0,0044 [−0,0095; 0,0008] | 0,092 | 13/20 | −0,0001 | 0,982 |
| `shape_vmamba_no_guidance` | 0,7201 ± 0,0076 | −0,0031 [−0,0074; 0,0013] | 0,154 | 14/20 | +0,0012 | 0,697 |
| C2PSA rộng | 0,7162 ± 0,0055 | **−0,0070 [−0,0101; −0,0038]** | **< 0,001** | **17/20** | −0,0027 | 0,309 |

"TSVM cao hơn" = số seed (trên 20) mà TSVM đầy đủ có mAP50–95 cao hơn biến thể đó.

## Diễn giải

1. **Ba biến thể tách thành phần** đều có trung bình thấp hơn bản đầy đủ, nhưng không chênh lệch nào có ý nghĩa thống kê ở α = 0,05. Chỉ viết "xu hướng": bản đầy đủ cho kết quả tốt nhất trong các biến thể; không kết luận thành phần nào chắc chắn cần thiết.
2. **C2PSA rộng** (cùng số tham số với TSVM) thấp hơn TSVM có ý nghĩa thống kê (+0,0070 cho TSVM, KTC 95% [0,0038; 0,0101], TSVM cao hơn ở 17/20 seed) và không hơn mô hình gốc (−0,0027; p = 0,31). Nghĩa là xu hướng tăng của TSVM không giải thích được chỉ bằng việc thêm khoảng 820 nghìn tham số.
3. Không biến thể nào hơn mô hình gốc có ý nghĩa thống kê, kể cả TSVM đầy đủ (p = 0,061).

## Dữ liệu ngoài

Các biến thể cũng được chạy suy luận trên CVC-ClinicDB và CVC-ColonDB (20 seed): `08_du_lieu_thuc_te/bang/ablation_ngoai/20seed/`, tóm tắt trong [08_du_lieu_thuc_te/README.md](../08_du_lieu_thuc_te/README.md).

## Hình

`06_bao_cao/hinh/ablation_20seed/{vi,en}/`: `k01_ablation_tung_seed`, `k02_ablation_delta`, `k03_c2psa_rong`.
