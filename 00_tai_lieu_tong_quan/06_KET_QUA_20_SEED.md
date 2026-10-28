# 06. Kết quả 20 seed

> **Cập nhật 28/10/2026:** số trong file này tính trên **20 seed** và là **bộ số dùng trong báo cáo**. Bộ 10 seed (chỉ đối chiếu) ở [06b_KET_QUA_10_SEED.md](06b_KET_QUA_10_SEED.md).

Số liệu được tính lại từ 40 file `results.csv` gốc bằng [scripts/tinh_lai_so_lieu.py](scripts/tinh_lai_so_lieu.py). Kết quả nằm ở [bang/02_ket_qua_tung_seed.csv](bang/02_ket_qua_tung_seed.csv), [bang/04_thong_ke_ghep_cap.csv](bang/04_thong_ke_ghep_cap.csv) và [bang/04b_do_nhay_quy_tac_epoch.csv](bang/04b_do_nhay_quy_tac_epoch.csv). Bộ số này **trùng khớp hoàn toàn** với gói phân tích `04_phan_tich_20seed/`: 0 ô lệch so với raw CSV, sai số 0 so với `06_reports/summary.csv`.

## Quy tắc trích số

- Với mỗi lượt, lấy **dòng đầu tiên đạt mask mAP50–95 lớn nhất** trong 100 epoch. Mọi chỉ số khác trong bảng lấy cùng dòng đó.
- Tập đánh giá: validation 160 ảnh (120 ảnh polyp có 127 đối tượng, cộng 40 ảnh nền).
- SD là độ lệch chuẩn mẫu (ddof = 1). CI 95% là khoảng tin cậy t của hiệu ghép cặp, n = 20.
- Endpoint chính là **mask mAP50–95**. Các chỉ số khác chỉ mang tính thăm dò và chưa hiệu chỉnh đa kiểm định.

## Bảng tổng hợp (mean ± SD, 20 seed)

| Chỉ số | Baseline | TSVM FP32 | Δ (TSVM − Base) | CI 95% của Δ | Paired t p | Wilcoxon p | TSVM tốt hơn |
|---|---:|---:|---:|---:|---:|---:|---:|
|**Mask mAP50–95**|0,7189 ± 0,0118|0,7232 ± 0,0072|+0,0043|[−0,0002; 0,0088]|0,061|0,070|13/20|
|Mask mAP50|0,9069 ± 0,0125|0,9083 ± 0,0086|+0,0014|[−0,0053; 0,0080]|0,668|0,812|10/20|
|Mask Precision|0,9041 ± 0,0287|0,9145 ± 0,0233|+0,0104|[−0,0086; 0,0293]|0,266|0,498|11/20|
|Mask Recall|0,8594 ± 0,0241|0,8590 ± 0,0179|−0,0004|[−0,0126; 0,0119]|0,948|0,926|9/20|
|Box mAP50–95|0,7228 ± 0,0159|0,7273 ± 0,0134|+0,0045|[−0,0031; 0,0121]|0,227|0,105|13/20|
|Box mAP50|0,9006 ± 0,0116|0,9014 ± 0,0083|+0,0008|[−0,0053; 0,0069]|0,778|1,000|11/20|
|Box Precision|0,9006 ± 0,0263|0,9067 ± 0,0238|+0,0061|[−0,0102; 0,0224]|0,442|0,475|11/20|
|Box Recall|0,8501 ± 0,0293|0,8522 ± 0,0145|+0,0021|[−0,0128; 0,0170]|0,771|0,956|10/20|
|Val seg loss ↓|1,2663 ± 0,0843|1,2329 ± 0,0410|−0,0334|[−0,0807; 0,0138]|0,155|0,177|14/20|
|Val box loss ↓|0,7303 ± 0,0355|0,7247 ± 0,0389|−0,0056|[−0,0283; 0,0171]|0,614|0,388|14/20|
|Val cls loss ↓|0,5862 ± 0,0587|0,6088 ± 0,0655|+0,0226|[−0,0138; 0,0591]|0,209|0,349|7/20|
|Val L1 loss ↓|0,016366 ± 0,000994|0,016153 ± 0,000920|−0,000214|[−0,000810; 0,000382]|0,461|0,475|12/20|

↓ nghĩa là thấp hơn thì tốt hơn. Cột "TSVM tốt hơn" đếm số seed TSVM cho kết quả tốt hơn theo đúng chiều của từng chỉ số.

Giá trị đầy đủ 6 chữ số của endpoint chính: Baseline **0,718868 ± 0,011768**, TSVM FP32 **0,723171 ± 0,007197**, Δ = **+0,004303** (+0,43 điểm phần trăm, +0,60% tương đối), CI 95% [−0,000228; 0,008834], p = 0,061431.

## Diễn giải endpoint chính

- TSVM có mask mAP50–95 trung bình cao hơn 0,0043 và cao hơn ở 13/20 seed. Tuy vậy CI 95% **chứa 0**, paired t p = 0,061 và Wilcoxon p = 0,070. **Chưa đạt ý nghĩa thống kê ở α = 0,05.** Sign test 13/20 cho p = 0,263. Hiệu ứng chuẩn hóa ghép cặp Cohen's d_z = 0,44.
- p > 0,05 **không chứng minh** hai mô hình tương đương. Có thể viết: "TSVM cho xu hướng tăng nhỏ, nhưng chưa đủ bằng chứng thống kê với 20 seed".
- **Độ ổn định:** SD của TSVM nhỏ hơn khoảng 38,85% (0,0072 so với 0,0118). Khoảng min–max của TSVM là 0,7065–0,7339, của Baseline là 0,6941–0,7366. Theo `summary.csv` của gói phân tích, kiểm định Levene (trung vị) cho p = 0,026. Kiểm định này bỏ qua cấu trúc ghép cặp nên chỉ mang tính thăm dò. Không có nghĩa là mọi epoch đều ổn định hơn: ở epoch 30, SD của TSVM lớn hơn Baseline ([07](07_HOI_TU_VA_LOSS.md)).
- Mask Precision tăng khoảng 1 điểm, Recall gần như không đổi. Cả hai đều không có ý nghĩa thống kê.

## Bảng từng seed (mask mAP50–95 tại epoch cực đại)

|Seed|Baseline|Epoch|TSVM FP32|Epoch|Δ|
|---:|---:|---:|---:|---:|---:|
|0|0,73663|89|0,72451|88|−0,01212|
|1|0,71649|98|0,72739|98|+0,01090|
|2|0,71377|100|0,72591|83|+0,01214|
|3|0,69411|61|0,72126|89|+0,02715|
|4|0,72741|99|0,71970|97|−0,00771|
|5|0,73505|94|0,72845|90|−0,00660|
|6|0,71531|81|0,72537|95|+0,01006|
|7|0,71449|71|0,70650|88|−0,00799|
|8|0,73175|96|0,73385|93|+0,00210|
|9|0,72528|84|0,73285|96|+0,00757|
|10|0,70452|82|0,71982|100|+0,01530|
|11|0,72987|99|0,72264|87|−0,00723|
|12|0,70556|87|0,71569|89|+0,01013|
|13|0,73151|97|0,73061|99|−0,00090|
|14|0,72232|74|0,72107|96|−0,00125|
|15|0,71758|80|0,72621|84|+0,00863|
|16|0,71248|96|0,72374|93|+0,01126|
|17|0,72744|73|0,73015|100|+0,00271|
|18|0,70220|94|0,70821|47|+0,00601|
|19|0,71359|71|0,71949|91|+0,00590|

Seed tốt nhất của Baseline (0,7366, seed 0) cao hơn seed tốt nhất của TSVM (0,7339, seed 8). Lợi thế của TSVM thể hiện ở việc **nâng các seed yếu** (min 0,7065 so với 0,6941), chứ không phải ở đỉnh.

## Độ nhạy theo quy tắc chọn epoch

Chọn epoch theo mask mAP lớn nhất trên chính tập validation tạo ra thiên lệch lựa chọn. Vì vậy script tính lại so sánh với hai quy tắc khác:

| Quy tắc chọn epoch | Baseline | TSVM FP32 | Δ | Paired t p | Wilcoxon p | TSVM tốt hơn |
|---|---:|---:|---:|---:|---:|---:|
| Mask mAP50–95 lớn nhất (**endpoint chính**) | 0,7189 ± 0,0118 | 0,7232 ± 0,0072 | +0,0043 | 0,061 | 0,070 | 13/20 |
| Fitness box + mask lớn nhất (epoch của `best.pt`) | 0,7174 ± 0,0129 | 0,7222 ± 0,0075 | +0,0048 | 0,062 | 0,076 | 14/20 |
| Epoch 100 (cuối huấn luyện) | 0,7093 ± 0,0132 | 0,7119 ± 0,0130 | +0,0025 | 0,456 | 0,349 | 12/20 |

- Hai quy tắc dựa trên "điểm tốt nhất" cho kết luận gần giống nhau.
- Ở epoch 100, khoảng cách thu hẹp còn +0,0025. Khi đó SD hai mô hình gần bằng nhau (0,0132 và 0,0130). Như vậy **độ ổn định thấp hơn về SD chỉ đúng tại epoch tốt nhất**, không còn ở cuối huấn luyện.
- Có 16/40 lượt mà epoch cực đại mask khác epoch fitness (Baseline 8, TSVM 8). Vậy giá trị trong bảng chính **không phải** là kết quả đánh giá file `best.pt`.

## Hình cũ (đã chuyển vào lưu trữ)

Bộ hình mới vẽ lại từ CSV nằm ở `06_bao_cao/hinh/`. Các hình cũ dưới đây chỉ giữ để tham khảo.


Gói phân tích đã có hình vẽ sẵn, tham khảo khi đưa vào báo cáo (bộ tài liệu này không vẽ lại):

- [01_overall_benchmark_barchart.png](../99_luu_tru/hinh_cu/figures_20seed/01_overall_benchmark_barchart.png)
- [03_seed_by_seed_barchart.png](../99_luu_tru/hinh_cu/figures_20seed/03_seed_by_seed_barchart.png)
- [11_boxplot_variance_stability.png](../99_luu_tru/hinh_cu/figures_20seed/11_boxplot_variance_stability.png)
- [21_paired_mask_map_delta.png](../99_luu_tru/hinh_cu/charts_20seed/summary/21_paired_mask_map_delta.png)
- [20_delta_tsvm_vs_baseline.png](../99_luu_tru/hinh_cu/charts_20seed/summary/20_delta_tsvm_vs_baseline.png)

Trước khi dùng hình nào trong báo cáo, cần đối chiếu số trên hình với bảng ở trên.
