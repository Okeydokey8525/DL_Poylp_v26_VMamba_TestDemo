# Kết quả 20 seed: YOLO26s-seg và TSVM FP32

Gói mở rộng ngày 16/10/2026. Giữ nguyên đầu vào ở thư mục gốc và `figures/` cũ. Các dẫn xuất mới dựa trực tiếp vào 40 results.csv; chỉ dùng TSVM có hậu tố FP32.

|Thư mục|Nội dung|
|---|---|
|01_raw_analysis|Trích lại40 run,13 chỉ số,epoch lựa chọn và đường cong mean/SD100 epoch|
|02_statistics|Mean/SD, CI95% ghép cặp, pairedt, Wilcoxon, extrema, từng seed và thắng/thua|
|03_metrics|Tách metric mask, box và validationloss|
|04_confusion_matrix|TP/FP/FN và heatmap; TN luôn N/A; cảnh báo dữ liệu kế thừa|
|05_charts|Hiệu năng, độ ổn định, phân phối, tương quan, tổng hợp và hội tụ|
|06_reports|Báo cáo diễn giải, CSV và hình khuyến nghị cho luận văn|
|07_audit|Kiểm tra nguồn, SHA256, môi trường và danh mục hình|
|efficiency_benchmark|Benchmark FP32 riêng; có script và phạm vi đo riêng|

## Tái lập
Chạy `Stracth/Bao_Cao/generate_20seed_fp32_thesis_package.py` bằng Python có numpy, pandas, scipy, matplotlib, PyYAML. Script tìm gốc dự án theo vị trí tệp, không phụ thuộc thư mục làm việc. Với môi trường hiện tại dùng Python bundled và PYTHONPATH trỏ `.codex_report_work_20261015/packages`.

Đọc `06_reports/summary.md` trước khi trích dẫn. Quan trọng: epoch max mask ≠ best.pt trong16/40 run; p chính0,061431; không có TN ảnh, Dice hay kiểm chứng topology. Kết quả10seed là thực nghiệm khác, chỉ mượn cách tổ chức thư mục và không sao chép số liệu.
