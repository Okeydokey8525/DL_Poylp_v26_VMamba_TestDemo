# Kiểm toán độc lập số liệu Baseline và TSVM FP32

Ngày thực hiện: 25/10/2026. Phòng A, chỉ ghi vào `audit_20261025_193105/A_numeric/`.

## Kết luận trong phạm vi đã kiểm tra

Không phát hiện sai khác số học trong các giá trị máy đọc đã kiểm của **36 CSV thuộc gói 20 seed FP32**, gồm các bảng thống kê chính, bảng trích xuất tại gốc, bảng theo epoch, các bảng confusion matrix dẫn xuất và bảng benchmark. Việc này xác nhận phép tổng hợp khớp với tệp nguồn đang lưu; **không tự chứng minh quá trình huấn luyện, nguồn checkpoint hoặc độ đúng của ảnh confusion matrix**.

Có **3 vấn đề ngữ nghĩa trong các hiện vật legacy**: hai nơi còn lưu `TN_reconstructed = 40 - FP` và một bảng gọi số lượt loss cao hơn là `tsvm_wins`. Các bảng mới đã loại TN suy diễn và dùng đúng chiều lower-is-better cho loss. Không được mở rộng kết luận PASS số học thành PASS toàn bộ dự án.

## Phương pháp và độ bao phủ

- Triển khai mới: `audit_numeric.py`, không import hoặc chạy builder có sẵn. Python của app venv; SciPy 1.18.1 cài riêng trong `A_numeric/packages`, không đổi môi trường ứng dụng. Phiên bản cụ thể trong `environment.json`.
- Kiểm tra trực tiếp 40 `results.csv` của Baseline/TSVM_FP32, seed 0–19: mỗi file 100 epoch liên tục; toàn bộ giá trị số hữu hạn; các metric AP/P/R nằm trong [0,1]; loss không âm; `args.yaml` ghi đúng seed.
- 76 dòng coverage = 40 CSV nguồn và 36 CSV trong gói dẫn xuất/benchmark. Tổng **105.678 phép so sánh ô** trong phạm vi đã khai báo, phần lớn là kiểm tra tính hợp lệ raw; đây không phải số claim độc lập. Xem `coverage.csv` để biết loại kiểm tra từng file.
- Tái trích 13 metric tại dòng đầu tiên đạt cực đại mask mAP50–95. So lại best epoch, metric và run path cho mọi bảng trích xuất liên quan.
- Tái tính mean, SD mẫu ddof=1, min/max/median/quartile, delta ghép seed, CI t hai phía, paired t, Wilcoxon hai phía, Cohen dz, Shapiro, Levene trung vị, win/loss/tie, sign test. Kiểm thêm `best_epoch` của bảng legacy.
- Kiểm 2.200 dòng mean/SD theo epoch. Kiểm công thức TP/FP/FN, precision/recall theo đối tượng, trung bình/SD và tỷ lệ phần trăm của các bảng CM mới, nhưng **nguồn số đếm vẫn là extraction kế thừa**; đối chiếu ảnh thuộc phòng B.
- Tự băm 240 hiện vật nguồn gồm results, args, best/last checkpoint và ảnh CM nếu có; tái kiểm 163 hash trong manifest có sẵn. Không phát hiện hash manifest không khớp. Hash chỉ xác nhận danh tính byte tại thời điểm đọc.
- So toàn bộ cấu hình với Baseline seed 0. Chỉ khác các trường danh tính hoặc chính sách nạp mô hình dự kiến: `seed`, `model`, `name`, `save_dir`, `pretrained`. Không có khác biệt trường siêu tham số khác trong args đang lưu. `pretrained=True` của baseline và đường dẫn pretrained của TSVM là cách khai báo khác nhau; args không chứng minh trực tiếp mọi trọng số ban đầu.
- Benchmark: tính lại 400 dòng timing, bốn nhóm ×100; mean/SD/percentile/serial throughput và các thành phần pipeline khớp bảng. Kiểm hash checkpoint/custom module của metadata. Các trường tham số/RSS được đối chiếu metadata, chưa tái đo độc lập phần cứng/RSS trong phòng A.

Sai số so sánh số thực: absolute/relative 2×10^-11 cho phép tính lưu dưới dạng decimal, tránh đánh dấu chênh lệch thứ tự cộng số thực. Không dùng dung sai này để thay thế hoặc làm tròn dữ liệu nguồn.

## Kết quả chính tái tính

| Quy tắc chọn | Baseline mask AP mean ± SD | TSVM FP32 mask AP mean ± SD | Delta | CI95% delta | Paired t p | TSVM thắng |
|---|---|---|---|---|---|---|
| Max mask AP | 0,718868 ± 0,011768 | 0,723171 ± 0,007197 | +0,004303 | [-0,000228; 0,008834] | 0,061431 | 13/20 |
| Max box+mask fitness | 0,717397 ± 0,012877 | 0,722199 ± 0,007527 | +0,004802 | [-0,000264; 0,009868] | 0,061898 | 14/20 |
| Epoch cuối 100 | 0,709340 ± 0,013226 | 0,711855 ± 0,012953 | +0,002514 | [-0,004404; 0,009432] | 0,456256 | 12/20 |

Có 16/40 run khác epoch giữa max-mask và max-fitness. Các kết quả trên là tính từ lịch sử CSV, không phải đánh giá lại checkpoint. Cả ba quy tắc đều chưa cho bằng chứng khác biệt trung bình ở alpha 0,05. Thay quy tắc không được thực hiện sau khi xem p nhằm chọn kết quả thuận lợi.

Độ giảm SD tại các epoch max-mask riêng của từng run khoảng 38,85%. Với dải min–max theo từng epoch, TSVM hẹp hơn 53/100 epoch và độ rộng dải trung bình tăng 0,76256%; các giá trị legacy `facts.json` này khớp khi dùng đúng định nghĩa **min–max envelope**, không nhầm với mean ± SD band.

## Ba vấn đề cần quản lý

| ID | Tệp | Phát hiện và bằng chứng | Phán quyết | Khuyến nghị |
|---|---|---|---|---|
| A01 | `facts.json`, `cm_mean.*.TN_reconstructed` | Lưu mean/SD của 40 trừ FP đối tượng: Baseline 23,55; TSVM 24,25 | P2: công thức số học có thật nhưng không phải TN ảnh hợp lệ | Giữ bản gốc để truy vết, đánh dấu deprecated, ngăn downstream dùng để tính specificity |
| A02 | Root `raw_20seeds_confusion_matrices.csv`, 40 dòng | `TN` trống nhưng `TN_reconstructed` được điền 40−FP | P2: ngữ nghĩa ảnh/object không hợp lệ nếu coi là TN đo được | Dùng bảng mới trong `04_confusion_matrix`; không diễn giải trường này là số ảnh âm đúng |
| A03 | Root `summary_20seeds_paired.csv`, dòng `val_seg_loss` | `tsvm_wins=6`, `baseline_wins=14` đếm chiều lớn hơn; lower loss tốt hơn thì TSVM thắng14 | P2: tên wins không nhất quán chiều tốt hơn, không phải sai raw loss | Công bố legacy counts là higher/lower hoặc dùng `02_statistics/seed_comparison/seed_win_loss_summary.csv` có lower_is_better |

Chi tiết machine-readable gồm file/row/expected/actual/severity/cause/recommendation trong `discrepancies.csv`. Không sửa bất kỳ tệp nguồn hoặc bảng dẫn xuất gốc nào.

## Liên hệ bộ 10 seed, 21 seed và nguồn FP32

- Tái kiểm 240 ô metric của Baseline/TSVM trong raw extraction 10 seed với raw cũ tương ứng: không sai khác. Cũng không có sai khác 240 ô này khi so với metric của cùng model/seed trong bộ 20 FP32 hiện tại.
- Kiểm **46.000 ô số** của toàn bộ 100 epoch ×23 cột ×20 seed TSVM cũ/FP32: chỉ 2.000 ô `time` khác; 44.000 ô còn lại giống hệt về giá trị số. Các tệp CSV khác hash vì time khác. Đây là đặc điểm lineage cần công bố và truy log; **không đủ để kết luận sai, giả hoặc chứng minh rerun**. Huấn luyện tất định với cùng seed và kiến trúc có thể tái tạo lịch sử giống nhau.
- Không có hai lịch sử trong 40 run hiện tại giống hệt nhau khi bỏ cột time. Không đếm bản sao file như seed mới.
- Tái tính riêng 21 seed lịch sử (TSVM chưa vá): Baseline 0,71881619 ± 0,01147236, TSVM 0,72293857 ± 0,00709475; p=0,05990878. Đúng phạm vi lịch sử 21 cặp, không thay thế bộ 20 seed FP32.
- Các checkpoint TSVM cũ và FP32 không trùng hash; ảnh CM trùng hash ở 5/20 cặp TSVM. Sự trùng ảnh không tự chứng minh sai, vì cùng dự đoán có thể sinh cùng ảnh. Đối chiếu pixel/OCR và checkpoint thuộc B/root.
- Phòng A chưa tự giải tuần tự checkpoint hoặc chạy inference. Root đang kiểm dtype/finite và đánh giá lại checkpoint trong nhánh riêng. Vì vậy trạng thái **phép tổng hợp PASS**, trạng thái **nguồn train/rerun và tái đánh giá mọi checkpoint CHƯA CHỨNG THỰC ĐẦY ĐỦ** trong báo cáo A.

## Kiểm tra chéo giữa các phòng

Đã gửi dữ liệu độc lập cho phòng B: `independent_selected_metrics.csv`, `independent_summary.csv`, `independent_extrema.csv`, `benchmark_independent_summary.csv`. Phòng B giữ riêng kết luận ảnh CM và hình Word, không dùng PASS số học để chứng thực hình.

Đã gửi phòng C các thống kê max-mask, chiều loss14/6 và cảnh báo TN. Phòng C yêu cầu xác nhận P4 trong Word; root báo kiểm checkpoint layer6 output256, thuộc phát hiện báo cáo C, không đưa vào kết luận số học A khi A chưa tự load checkpoint.

Root đã bàn giao tính t độc lập bằng thư viện chuẩn cho max-mask và max-fitness; kết quả A khớp ở sai số số thực. Các phép kiểm Wilcoxon/Levene/Shapiro của A dựa SciPy 1.18.1, ghi rõ phiên bản để tái lập.

## Giới hạn và việc cần tiếp nối

1. Raw CSV nhất quán nội bộ không chứng minh dataset/fork thực sự được dùng trong phiên Kaggle; cần log import path, môi trường và provenance snapshot của từng run.
2. Đánh giá lại checkpoint không nằm trong A; không coi dtype hợp lệ là chứng minh AP/CM khớp lịch sử. Nên gắn JSON kết quả với hash checkpoint, dataset và tham số suy luận.
3. TP/FP/FN mới khớp extraction kế thừa về số học. Chưa thể PASS nguồn ảnh nếu B chưa đọc/đối chiếu hoặc chưa replay cùng ngưỡng.
4. Tất cả seed dùng chung validation đã tham gia chọn epoch. Kết quả thống kê không phải test ngoài, không chứng minh ưu thế trên bệnh nhân hoặc bệnh viện khác.
5. Bộ 10 seed được kiểm raw extraction của hai mô hình chính và lineage; không kiểm toàn bộ bảng lịch sử của các mô hình khác, không báo PASS cho chúng.

## Tái lập

Chạy `audit_numeric.py` rồi `audit_supplement.py` bằng app venv Python. Cả hai chỉ đọc nguồn và ghi vào A_numeric. Các builder gốc không được thực thi. Bảng coverage và manifest hỗ trợ tổng kiểm xác nhận phạm vi và phát hiện thay đổi nguồn sau kiểm toán.
