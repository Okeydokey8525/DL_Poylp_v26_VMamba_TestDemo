# Đối sánh 20 seed: YOLO26s-seg và TSVM FP32

## Thiết kế và quy tắc đọc số liệu
40 lần huấn luyện đã lưu, seed 0–19 ghép cặp, 100 epoch/lần. Script này chỉ đọc tệp, không huấn luyện hay suy luận lại. Tập validation: 160 ảnh, 40 ảnh nền và 127 đối tượng polyp. Các seed dùng cùng một tập validation; kiểm định mô tả biến thiên huấn luyện, không chứng minh khả năng tổng quát trên bệnh viện khác.

Bảng chính trích **epoch có validation mask mAP50–95 lớn nhất** (khi hòa chọn dòng đầu tiên). Đây là quy tắc của CSV gốc, **không đồng nhất với epoch của best.pt**: fitness lưu checkpoint là tổng box mAP50–95 và mask mAP50–95. Có 16/40 lần khác epoch. Xem `01_raw_analysis/epoch_selection_audit.csv`. Chỉ số tại epoch tối ưu validation có thiên lệch lựa chọn; cần test độc lập cho kết luận tổng quát.

## Kết quả chính
- Baseline mask mAP50–95: 0.718868 ± 0.011768.
- TSVM FP32: 0.723171 ± 0.007197.
- Chênh lệch TSVM − baseline: 0.004303, tức **+0.4303 điểm phần trăm**; thay đổi tương đối 0.5986%.
- Khoảng tin cậy 95% của chênh lệch ghép cặp: [-0.000228; 0.008834].
- Paired t-test hai phía p=0.061431; Wilcoxon hai phía p=0.069580. **Chưa đạt ý nghĩa thống kê ở α=0,05**.
- TSVM tăng 13/20 seed, giảm 7/20; sign test p=0.263176. Đây không phải xác suất thắng trên một bệnh nhân mới.
- SD giảm 38.85% tại epoch được chọn. Đây là quan sát ổn định cuối cùng; không khẳng định mọi epoch đều có band hẹp hơn.

## Bảng tổng hợp
|Chỉ số|Baseline mean ± SD|TSVM FP32 mean ± SD|Δ|Paired t p|
|---|---:|---:|---:|---:|
|Mask mAP50–95|0.718868 ± 0.011768|0.723171 ± 0.007197|+0.004303|0.061431|
|Mask mAP50|0.906888 ± 0.012468|0.908273 ± 0.008569|+0.001385|0.667528|
|Mask precision|0.904095 ± 0.028748|0.914451 ± 0.023323|+0.010356|0.266225|
|Mask recall|0.859366 ± 0.024112|0.858979 ± 0.017934|-0.000387|0.947902|
|Box mAP50–95|0.722758 ± 0.015941|0.727274 ± 0.013429|+0.004516|0.227473|
|Box mAP50|0.900609 ± 0.011598|0.901444 ± 0.008346|+0.000835|0.777627|
|Box precision|0.900635 ± 0.026285|0.906741 ± 0.023754|+0.006106|0.441746|
|Box recall|0.850120 ± 0.029275|0.852220 ± 0.014507|+0.002100|0.770891|
|Val segmentation loss|1.266294 ± 0.084303|1.232862 ± 0.041025|-0.033432|0.155157|
|Val box loss|0.730292 ± 0.035467|0.724728 ± 0.038944|-0.005564|0.613671|
|Val class loss|0.586163 ± 0.058730|0.608810 ± 0.065538|+0.022646|0.209157|
|Val L1 loss|0.016366 ± 0.000994|0.016153 ± 0.000920|-0.000214|0.461457|
|Val semantic loss|0.000000 ± 0.000000|0.000000 ± 0.000000|+0.000000|N/A|

## Kiểm định và giới hạn
SD dùng ddof=1. Paired t CI và p-value dùng 20 hiệu số cùng seed; Wilcoxon là kiểm tra độ nhạy, Shapiro cho hiệu số chỉ là chẩn đoán. Không diễn giải Shapiro p>0,05 như bằng chứng chắc chắn phân phối chuẩn. Endpoint chính là mask mAP50–95. Các p-value khác chưa hiệu chỉnh đa kiểm định, có tính thăm dò; Levene chỉ thăm dò vì bỏ qua cấu trúc ghép cặp. Không coi p>0,05 là chứng minh hai mô hình tương đương. Cột val/sem_loss được ghi bằng 0 trong cả 40 run, do đó kiểm định và thay đổi tương đối là N/A; không diễn giải đây là mức lỗi bằng 0 trên dữ liệu thực. YOLO26 trong các CSV này có val/l1_loss, không có val/dfl_loss; không kế thừa nhãn DFL từ biểu đồ cũ.

## Ma trận nhầm lẫn
CSV gốc có TN trống và trường `TN_reconstructed=40-FP`. Trường này **không hợp lệ**: FP là số phát hiện dư, có thể nằm trên ảnh chứa polyp và có nhiều phát hiện trên cùng ảnh. Không thể suy ra số ảnh nền dự đoán đúng bằng 40−FP. Gói mới giữ CSV gốc để truy vết, loại trường suy diễn khỏi mọi bảng/hình mới, để ô nền/nền là N/A và không tính specificity/accuracy ảnh. Phần trăm chỉ chuẩn hóa cột 127 đối tượng polyp; FP không được chuẩn hóa bằng 40. Các số TP/FP/FN kế thừa bảng trích từ ảnh confusion matrix đã lưu, chưa đối chiếu bằng suy luận mới. TP+FN=127 được kiểm tra đủ 40 dòng. Không trộn precision/recall tại ngưỡng CM với precision/recall được Ultralytics chọn theo đường cong trong bảng metric. Các ảnh CM cuối quá trình huấn luyện thuộc đánh giá checkpoint best.pt theo fitness; không được coi là cùng epoch với bảng max-mask trong các lần hai quy tắc chọn khác nhau. CSV CM kế thừa không lưu ngưỡng confidence/IoU nên không suy diễn một ngưỡng lâm sàng từ bảng này.

## Không có trong dữ liệu này
Không có Dice, IoU trung bình vùng, Hausdorff, Betti, clDice hay xác nhận topology trực tiếp. Không quy đổi AP thành Dice/IoU. Tên topology/shape là định hướng thiết kế; lợi ích topology cần thí nghiệm riêng. Benchmark hiệu suất ở thư mục riêng, không suy ra FPS từ thời gian epoch, không gán số của TSVM cũ sang FP32.
