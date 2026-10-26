# Quản lý các hiện vật legacy trong gói 20 seed FP32

Cập nhật 26/10/2026. Các hiện vật liệt kê dưới đây được **giữ nguyên byte** để truy vết. Tệp này ngăn tái sử dụng nhầm trường hoặc hình cũ; không thay thế nguồn thực nghiệm và không sửa số liệu để khớp báo cáo.

| Hiện vật | Vấn đề đã xác nhận | Nguồn nên dùng |
|---|---|---|
| `facts.json` → `cm_mean.*.TN_reconstructed` | Mean của 40−FPđối tượng không phải TNảnh | `04_confusion_matrix/count/detection_counts_mean_sd.csv`; TNảnhN/A |
| Root `raw_20seeds_confusion_matrices.csv` → `TN_reconstructed` | Không dùng suy specificity hoặc số ảnh nền đúng | `04_confusion_matrix/count/validated_detection_counts_per_seed.csv` |
| Root `summary_20seeds_paired.csv` → `val_seg_loss.tsvm_wins` | Giá trị 6 đếm chiều loss tăng; lower-is-better thì TSVM thắng 14, Baseline 6 | `02_statistics/seed_comparison/seed_win_loss_summary.csv`, có cột `lower_is_better` |
| `figures/04_convergence_loss_curves.png`, `figures/05_metric_curves_mAP.png` | SDpopulationddof=0; band nhỏ hơn sampleSD khoảng 2,532% khi n 20 | Hình mới trong `05_charts/convergence/`, ddof=1 |
| 11 hình trong `figures/` | Không tái tạo giống từng pixel ở môi trường kiểm toán, chưa xác định đầy đủ nguyên nhân render | Ưu tiên 35 hình mới (27 kếtquả+8 benchmark) có pixelreproduction; không gọi hình legacy là giả từ hash khác |

Phép tính số học của các CSV legacy có thể khớp raw nhưng tên/đơn vị vẫn sai. Không dùng dấu PASS kiểm toán số học để chứng nhận TNảnh hoặc hiệu quả lâm sàng. Một ảnh có thể có nhiều FP và FP có thể nằm trên ảnh polyp;40−FP không có nghĩa là số ảnh nền âm đúng.

Nguồn: [phòngA](../../audit_20261025_193105/A_numeric/report.md), [phòngB](../../audit_20261025_193105/B_visual/report.md), [danh sách phát hiện](../../audit_20261025_193105/ISSUES.csv). Manifest 07_audit cũ giữ nguyên; cảnh báo này là bổ sung sau sinh gói.

Các chỉ số chính mới đã có sẵn và không cần sửa: maskAPp=0,061431,CI 95%chứa 0; không Dicepixel/topology hoặc testngoài. Bộ 10 seed và 21 seed là phạm vi lịch sử khác, không ghép số liệu bằng cách đổi nhãnN.
