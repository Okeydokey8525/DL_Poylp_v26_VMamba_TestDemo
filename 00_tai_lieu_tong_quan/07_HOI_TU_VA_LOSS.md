# 07. Hội tụ và loss

Nguồn: [bang/05_duong_cong_theo_epoch.csv](bang/05_duong_cong_theo_epoch.csv), là trung bình và SD theo từng epoch trên 20 seed, tính từ `results.csv`.

## Mask mAP50–95 trên validation theo epoch (mean ± SD, 20 seed)

| Epoch | Baseline | TSVM FP32 |
|---:|---:|---:|
| 1 | 0,2001 ± 0,1124 | 0,1861 ± 0,0953 |
| 5 | 0,5320 ± 0,0427 | 0,5076 ± 0,0485 |
| 10 | 0,5687 ± 0,0355 | 0,5606 ± 0,0347 |
| 20 | 0,6086 ± 0,0293 | 0,6186 ± 0,0178 |
| 30 | 0,6349 ± 0,0183 | 0,6320 ± 0,0287 |
| 50 | 0,6716 ± 0,0208 | 0,6709 ± 0,0091 |
| 70 | 0,6890 ± 0,0125 | 0,6931 ± 0,0120 |
| 90 | 0,7035 ± 0,0152 | 0,7084 ± 0,0102 |
| 100 | 0,7093 ± 0,0132 | 0,7119 ± 0,0130 |

- Trong khoảng 10 epoch đầu, TSVM tăng chậm hơn một chút. Điều này khớp với việc các phần mới của tầng 10 khởi tạo ngẫu nhiên và γ = 0,001 ([04](04_KIEN_TRUC_TSVM_FP32.md#khởi-tạo-trọng-số)).
- Từ epoch 50 đến 81, hai đường đan xen nhau: TSVM thấp hơn ở 11 epoch (50, 52, 53, 55, 57, 62, 65, 66, 67, 72, 81). **Từ epoch 82 đến 100**, trung bình của TSVM luôn cao hơn. Trong các epoch ở bảng trên, khoảng cách lớn nhất là ở epoch 90 (+0,0049).
- SD giữa các seed của TSVM không phải lúc nào cũng nhỏ hơn: có **34/100 epoch** SD của TSVM lớn hơn Baseline, ví dụ epoch 5 và 30.
- Hầu hết các lượt đạt cực đại muộn. Epoch cực đại mask có trung vị 88 (Baseline) và 92 (TSVM), khoảng 61–100 và 47–100 ([bang/_log_chay.txt](bang/_log_chay.txt)).

## Val segmentation loss

| Epoch | Baseline | TSVM FP32 |
|---:|---:|---:|
| 1 | 5,7467 ± 3,7770 | 7,0170 ± 6,8087 |
| 10 | 1,5705 ± 0,1136 | 1,5345 ± 0,0950 |
| 50 | 1,2668 ± 0,0757 | 1,2788 ± 0,0738 |
| 90 | 1,2665 ± 0,0808 | 1,2236 ± 0,0386 |
| 100 | 1,2893 ± 0,0907 | 1,2482 ± 0,0424 |

- Trung bình val seg loss của Baseline thấp nhất ở **epoch 59** (1,2294), sau đó tăng lên 1,2893 ở epoch 100. TSVM thấp nhất ở **epoch 90** (1,2236). Như vậy Baseline có dấu hiệu quá khớp sớm hơn trên loss phân đoạn, dù mask mAP vẫn tăng tới cuối. Đây chỉ là quan sát mô tả, chưa kiểm định.
- Val seg loss tại epoch cực đại mask: Baseline 1,2663 ± 0,0843, TSVM 1,2329 ± 0,0410. TSVM thấp hơn ở 14/20 seed, p = 0,155, không có ý nghĩa thống kê ([06](06_KET_QUA_20_SEED.md)).

## Ảnh hưởng của `close_mosaic=10`

Từ epoch 91, mosaic bị tắt. Train seg loss trung bình giảm đột ngột từ 0,897 xuống 0,738 (Baseline) và từ 0,896 xuống 0,737 (TSVM). Ngay epoch 91, mask mAP trên validation giảm nhẹ (0,7035 → 0,6984 và 0,7084 → 0,7016), sau đó tăng lại. Loss train và validation **không so sánh trực tiếp được** quanh mốc này vì phân phối ảnh huấn luyện đã đổi.

## Các thành phần loss của YOLO26-seg trong log

| Cột | Ý nghĩa | Ghi chú |
|---|---|---|
| `box_loss` | Hồi quy hộp | |
| `seg_loss` | Mặt nạ | Loss chính để theo dõi chất lượng phân đoạn |
| `cls_loss` | Phân lớp | |
| `l1_loss` | L1 trên tọa độ hộp | YOLO26 dùng `reg_max: 1` nên **không có DFL**. Không gọi cột này là `dfl_loss` |
| `sem_loss` | Loss phân đoạn ngữ nghĩa phụ | Có giá trị ở train (khoảng 2,55 ở epoch 1, khoảng 0,25 ở epoch 100) nhưng **`val/sem_loss` bằng 0 ở mọi epoch của cả 40 lượt**. Đây là giá trị không được tính trên validation, không có nghĩa là lỗi bằng 0. Không đưa vào kiểm định |

## Hình có sẵn

- [23_map_curves_mean_sd.png](../04_phan_tich_20seed/05_charts/convergence/23_map_curves_mean_sd.png)
- [22_validation_losses_mean_sd.png](../04_phan_tich_20seed/05_charts/convergence/22_validation_losses_mean_sd.png)
- [25_val_losses_mean_sd_epoch11_100.png](../04_phan_tich_20seed/05_charts/convergence/25_val_losses_mean_sd_epoch11_100.png): bỏ 10 epoch đầu để thang đo dễ đọc hơn.
