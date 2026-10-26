# Danh mục hình và quy tắc diễn giải

|Hình|Diễn giải/giới hạn|
|---|---|
|`05_charts/performance/01_mask_map50_95_comparison.png`|Mean ± SD; selected epoch = maximum validation mask mAP50–95|
|`05_charts/performance/02_mask_map50_comparison.png`|Mean ± SD; selected epoch = maximum validation mask mAP50–95|
|`05_charts/performance/03_precision_recall_comparison.png`|Mean ± SD; selected epoch = maximum validation mask mAP50–95|
|`05_charts/performance/04_box_metrics_comparison.png`|Mean ± SD; selected epoch = maximum validation mask mAP50–95|
|`05_charts/performance/05_val_seg_loss_comparison.png`|Mean ± SD; selected epoch = maximum validation mask mAP50–95|
|`05_charts/stability/06_seed_mask_map50_95_trends.png`|Paired seed comparison; seed has no temporal interpretation|
|`05_charts/stability/07_seed_box_map50_95_trends.png`|Paired seed comparison; seed has no temporal interpretation|
|`05_charts/distribution/08_boxplot_mask_map50_95.png`|All 40 observations; sample median, quartiles and mean|
|`05_charts/distribution/09_histogram_kde_mask_map50_95.png`|KDE is descriptive for only 20 seeds, not a normality claim|
|`05_charts/stability/10_mean_std_errorbars.png`|Mean ± SD; selected epoch = maximum validation mask mAP50–95|
|`05_charts/correlation/11_scatter_mask_recall_vs_mask_precision.png`|Descriptive association across seeds; not causal|
|`05_charts/correlation/12_scatter_mask_map50_95_vs_mask_precision.png`|Descriptive association across seeds; not causal|
|`05_charts/correlation/13_scatter_mask_map50_95_vs_mask_recall.png`|Descriptive association across seeds; not causal|
|`05_charts/summary/18_grouped_bar_main_metrics.png`|Mean ± SD; selected epoch = maximum validation mask mAP50–95|
|`05_charts/summary/19_radar_chart_main_metrics.png`|Descriptive only; area is not an overall score|
|`05_charts/summary/20_delta_tsvm_vs_baseline.png`|Unadjusted per-metric 95% paired confidence intervals, primary endpoint mask mAP50–95|
|`05_charts/summary/21_paired_mask_map_delta.png`|13 improvements and 7 decreases; mean +0.4303 percentage points|
|`05_charts/summary/24_head_to_head_seed_wins.png`|Descriptive 13/20 improvements, two-sided sign test p=0.263176|
|`05_charts/convergence/22_validation_losses_mean_sd.png`|40 runs; mean ± sample SD per epoch, not a confidence interval|
|`05_charts/convergence/23_map_curves_mean_sd.png`|20 seeds per curve, 100 epochs; early training band may be wider for TSVM|
|`05_charts/convergence/25_val_losses_mean_sd_epoch11_100.png`|Mean ± SD of actual val loss columns; epochs 11–100; no DFL column exists|
|`05_charts/convergence/26_train_losses_mean_sd.png`|Mean ± SD of actual train loss columns; epochs 1–100; no DFL column exists|
|`04_confusion_matrix/count/baseline_mean_count.png`|N/A background/background; FP excluded from percentage because no valid ground-truth background denominator|
|`04_confusion_matrix/percentage/baseline_mean_percentage.png`|N/A background/background; FP excluded from percentage because no valid ground-truth background denominator|
|`04_confusion_matrix/count/tsvm_fp32_mean_count.png`|N/A background/background; FP excluded from percentage because no valid ground-truth background denominator|
|`04_confusion_matrix/percentage/tsvm_fp32_mean_percentage.png`|N/A background/background; FP excluded from percentage because no valid ground-truth background denominator|
|`04_confusion_matrix/count/mean_tp_fn_fp_comparison.png`|Counts inherited from saved confusion matrices; not clinical specificity|
