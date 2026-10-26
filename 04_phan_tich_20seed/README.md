# Kết quả 20 seed YOLO26s seg và TSVM FP32

Gói mở rộng 16/10/2026; hướng dẫn nguồn cập nhật 26/10/2026 sau kiểm toán. **Hai mô hình ×20 seed(0–19) ×100 epoch =40 lượt huấn luyện.** Chỉ dùng nhóm TSVM có hậu tố FP32 cho bộ đối sánh chính.

## Nguồn nên dùng

| Thư mục | Nội dung |
|---|---|
| 01_raw_analysis | Trích lại 40 run,13 metric,epoch lựa chọn và đường cong mean/sampleSD |
| 02_statistics | Mean/sampleSD,CI 95%,pairedt,Wilcoxon,extrema,từngseed và win/loss |
| 03_metrics | Mask/box/validationloss |
| 04_confusion_matrix | TP/FP/FN theo đối tượng; TNảnhN/A; không specificity suy diễn |
| 05_charts | Các hình mới dùng sampleSDddof=1 |
| 06_reports | Diễn giải, CSV và mapping hình cho luận văn |
| 07_audit | Manifest của lần sinh 16/10; giữ nguyên để truy vết |
| efficiency_benchmark | BenchmarkCPU FP32 riêng, không dùng thời gian epoch làmFPS |

**Đọc [summary](06_reports/summary.md) trước trích dẫn.** Endpoint chính là epoch max-mask, khác best.pt box+maskfitness trong 16/40 run. MaskmAP 50–95: Baseline 0,718868±0,011768;TSVM 0,723171±0,007197;p=0,061431,CI 95%chứa 0. Không kết luận ưu thế trung bình tạiα 0,05 hoặc topology/lâm sàng.

## Hiện vật cũ không dùng làm nguồn mặc định

Các file `facts.json`, `raw_20seeds_confusion_matrices.csv`, `summary_20seeds_paired.csv` ở gốc và `figures/` được giữ nguyên. Một số trường có ngữ nghĩa không hợp lệ hoặc quy ước khác gói mới. **Không đọc `TN_reconstructed` thành TNảnh; không đọc `tsvm_wins=6` của valsegloss như số lần loss tốt hơn.** Chi tiết và đường dẫn thay thế nằm trong [LEGACY_ARTIFACTS.md](LEGACY_ARTIFACTS.md). Việc thêm cảnh báo không thay đổi raw, CSV, JSON, PNG hoặc manifest cũ.

## Tái lập và kiểm toán

Builder thống kê: `Stracth/Bao_Cao/generate_20seed_fp32_thesis_package.py`; đây là chương trình **ghi lại dẫn xuất**, không dùng chỉ để kiểm tra hiện trạng. Nên chạy kiểm toán đọc riêng hoặc chỉ tái sinh vào thư mục mới sau khi bảo toàn nguồn.

[Hướng dẫn BG 20](../../doc/28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md) giải thích pathlocal, builder đúng và output mới không ghi đè. [Kiểm toán độc lập 25/10](../../audit_20261025_193105/AUDIT_REPORT.md) đã kiểm số học 36 CSV,35 PNG mới,40 checkpoint và các giới hạn. Mọi chỉnh sửa ngày 26/10 nằm trong `fix_20261026/`; không đổi bằng chứng của lần kiểm trước.
