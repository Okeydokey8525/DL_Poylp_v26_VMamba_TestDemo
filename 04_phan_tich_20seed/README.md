# 04_phan_tich_20seed

Số liệu trích từ 40 lượt chính (mô hình gốc và TSVM FP32, seed 0–19) và đo độ trễ CPU. Bảng số dùng trong báo cáo nằm ở `00_tai_lieu_tong_quan/bang/`; các file ở đây là đầu vào hoặc dùng để đối chiếu.

| File | Dùng ở đâu |
|---|---|
| `01_raw_analysis/raw_20seeds_extracted_metrics.csv` | Chỉ số mask/box tại epoch cực đại của từng lượt. `tinh_lai_so_lieu.py` đối chiếu với `results.csv` gốc: 0 ô lệch |
| `01_raw_analysis/raw_20seeds_confusion_matrices.csv` | TP/FP/FN theo đối tượng của từng lượt, đọc từ `confusion_matrix.png` của Ultralytics. `tinh_lai_so_lieu.py` đọc file này để ghi `bang/06_ma_tran_nham_lan_tung_seed.csv` |
| `06_reports/summary.csv` | Thống kê ghép cặp (gồm Levene p = 0,026). `tinh_lai_so_lieu.py` đối chiếu với `bang/04_thong_ke_ghep_cap.csv`: sai số 0 |
| `efficiency_benchmark/` | Độ trễ CPU (forward và pipeline), bộ nhớ, số tham số của hai mô hình seed 0. Hình `e02`, `e03` đọc `tables/efficiency_summary.csv` |
