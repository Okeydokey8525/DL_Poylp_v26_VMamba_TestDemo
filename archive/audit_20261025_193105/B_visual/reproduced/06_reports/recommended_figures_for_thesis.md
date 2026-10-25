# Hình ưu tiên cho Chương 5

1. `05_charts/performance/01_mask_map50_95_comparison.png`: bảng điểm chính mean ± SD; phải kèm CI và p.
2. `05_charts/summary/20_delta_tsvm_vs_baseline.png`: độ lớn và bất định của các chênh lệch.
3. `05_charts/summary/21_paired_mask_map_delta.png`: thể hiện 13 tăng/7 giảm, tránh chỉ chọn seed thuận lợi.
4. `05_charts/distribution/08_boxplot_mask_map50_95.png`: toàn bộ phân phối20seed, không chỉ mean.
5. `05_charts/convergence/22_validation_losses_mean_sd.png`: tiến trình5 loss, band là SD.
6. `05_charts/convergence/23_map_curves_mean_sd.png`: tiến trình mask/box AP100 epoch.
7. `04_confusion_matrix/count/mean_tp_fn_fp_comparison.png`: TP/FN/FP ở mức phát hiện; không có TN/specificity.
8. `05_charts/performance/03_precision_recall_comparison.png`: đánh đổi precision/recall.

Các hình radar, KDE, scatter có thể để phụ lục vì chỉ có tính mô tả. Bổ sung hình qualitative từ val_batch... nếu dùng phải ghi seed và đó là checkpoint best.pt (fitness), không đồng nhất với bảng max-mask. Không chọn hình theo kết quả đẹp nhất rồi coi là đại diện ngẫu nhiên.
