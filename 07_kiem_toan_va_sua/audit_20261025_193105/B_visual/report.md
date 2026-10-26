# Kiểm toán hình ảnh kết quả và hình nhúng báo cáo

Ngày kiểm: 25/10/2026. Phòng B. Chỉ ghi trong thư mục kiểm toán riêng; không sửa hình, dữ liệu, mã nguồn hoặc Word gốc.

## Kết luận theo phạm vi

Không tìm thấy sai lệch số liệu xác định trong **27 hình kết quả mới và 8 hình benchmark**: khi tái sinh vào thư mục riêng, cả 35 PNG giống từng pixel với hình đang lưu. Phòng A đã kiểm độc lập dữ liệu và thống kê đầu vào; việc dùng lại generator để kiểm PNG chỉ xác nhận tính nhất quán giữa generator và hiện vật, không tự chứng minh generator hay nguồn huấn luyện đúng.

**40 ma trận số đếm** khớp bảng trích hiện có ở 120 ô TP/FP/FN. **40 ma trận chuẩn hóa** khớp 120 ô có số; 80 ô TN của hai loại ma trận đều trống. **80 legend PR** khớp AP50 theo epoch fitness trong sai số lớn nhất 0,00125. Không phát hiện trường hợp lệch quá 0,005 trong phép so legend này. Đây là kiểm từ hình, không thay cho suy luận lại checkpoint.

**33 vị trí ảnh trong Word** đều truy được ảnh nguồn có cùng SHA-256. Có hai vị trí logo và 31 vị trí hình khoa học/minh họa. Mapping nguồn không chứng nhận mọi câu nhận xét, nguồn checkpoint hay bố cục từng trang Word.

Không gán 11 PNG legacy khác pixel khi tái sinh thành lỗi số liệu: chín hình cùng kích thước nhưng bố cục/chữ khác; hai hình CM khác kích thước. Các giá trị được kiểm và nguồn dữ liệu phù hợp. Nguyên nhân cụ thể của khác biệt render chưa được xác minh.

## Độ bao phủ và phương pháp

| Nhóm | Số lượng | Cách kiểm | Giới hạn |
|---|---:|---|---|
| Hình trong gói 20 seed | 46 | Kiểm kê/hash, overview; 27 kết quả mới + 8 benchmark tái sinh và so RGB từng pixel; 11 legacy đọc code/nhãn và so bản tái sinh | Tái sinh bằng generator hiện có không độc lập về thuật toán thống kê; A cung cấp kiểm dữ liệu độc lập |
| Raw count/normalized CM | 80 | OCR các ô từ ảnh gốc và đối chiếu counts/chuẩn hóa; xem overview theo run | OCR có giới hạn; phép cộng khớp chưa chứng minh đúng checkpoint/giao thức |
| Raw PR | 80 | OCR legend AP50, đối chiếu epoch fitness, số hóa đường xanh từ pixel | Diện tích số hóa gần đúng, không phải AP tính từ prediction arrays |
| Raw P/R/F1 confidence | 240 | Số hóa đường; 80 bộ P/R/F1 so quan hệ F1 xấp xỉ | Các đường đã smoothing nên không kỳ vọng đồng nhất từng pixel với công thức |
| Ảnh nhúng Word | 33 vị trí | Trích media/relationships, crop, caption/context; đối chiếu hash nguồn và nội dung | Không nghiệm thu toàn bộ 97 trang render trong phòng B |

Tổng inventory: **479 vị trí/tệp**, gồm 46 package, 400 raw và 33 Word. Phần raw đã loại trùng do glob PR/P/R; không cộng một ảnh nhiều lần. `coverage.csv` phân biệt overview contact-sheet, kiểm định lượng và giới hạn. Overview không được gọi là kiểm mọi chi tiết ở độ phân giải gốc.

Trước gián đoạn, phòng B đã xem overview package, Word và Baseline; phần tiếp tục xem đủ overview TSVM seed 0–19 và kiểm thêm ảnh gốc/Word ở độ phân giải cao. Không phát hiện bất thường đồ họa thô trong overview. Một số contact sheet bị khó đọc khi giao diện thu nhỏ; không dùng đó làm bằng chứng nguồn ảnh bị cắt. Khi nghi vấn đã mở ảnh gốc kiểm lại.

## Các phép kiểm định lượng từ hình

`cm_ocr_comparison.csv` có **320 phép kiểm**: 240 ô có số PASS và 80 ô trống PASS_BLANK. Với ma trận đếm, TP+FN=127 được đối chiếu dữ liệu A. Với ma trận Ultralytics chuẩn hóa, TP/FN được chia theo cột 127 GT objects; FP hiển thị 1,00 là đặc tính chuẩn hóa cột background chỉ có ô FP, **không phải tỷ lệ báo nhầm 100% trên 40 ảnh âm**. TN không được suy ra bằng 40−FP.

`raw_curve_digitization.csv` có **320 đường** số hóa. Trên 80 PR:

- Lệch lớn nhất giữa legend AP50 và log tại epoch fitness: **0,00125**.
- Lệch lớn nhất giữa diện tích đường số hóa và legend: **0,00363734**.
- Hai đại lượng không đồng nhất chính xác do ảnh đã raster hóa, độ dày đường, smoothing và cách tích phân AP. Không dùng sai khác gần đúng này để tự sửa raw AP.

`f1_pixel_consistency.csv` có 80 nhóm Box/Mask × model/seed. MAE lớn nhất giữa F1 vẽ và 2PR/(P+R) từ đường vẽ là **0,00486011**; sai khác điểm đơn lớn nhất **0,0586516**, thường ở vùng đường dốc/smoothing. Không coi quan hệ từ đường vẽ là kiểm raw arrays chính xác hoặc là Dice pixel.

## Hình trong Word và các nguồn biểu đồ riêng

`word_figure_mapping.csv` nối từng Figure ID với media trong DOCX, nguồn giữ lại, caption/context và crop. Tất cả 33 mapping kiểm lại hash đều khớp; không có crop khai báo trong các vị trí kiểm. Các hình chương 5 dùng PNG mới hoặc các hình riêng trong `.codex_report_work_20261015/figures`/`.codex_revision_20261016/figures`.

Đối với các hình riêng paired/CI/seed-delta, kiểm thêm bảng `verified_raw.csv`, `verified_statistics.csv` với kết quả độc lập A: **560 ô số, không sai khác**. Kiểm `curves.json` của bộ tạo hình Word với 40 raw CSV: **88.000 ô non-time, không sai khác**. Code tạo CI dùng đúng Box Recall cho trục cuối; không được nhầm với hình CI khác trong package có Box mAP50.

Hình 2.1 không ghi số kênh P4 nên không lặp lại lỗi 512/256 ở Bảng 2.1 do C/root phát hiện. Hình 2.2 thể hiện guidance 1+G đúng code. Hình 4.1 phân biệt Web qua Spring Boot và Mobile gọi FastAPI. Các sơ đồ là minh họa luồng, không biểu diễn đầy đủ mọi tensor/parser.

Hình 4.2 (`V0537`, media image13.png) khớp byte với `qualitative.png` giữ lại; ảnh gốc, đường nhãn và hai overlay cùng trường hợp. Một nhãn/box nhìn thấy không chứng minh chỉ có một mask vì các prediction có thể chồng lên nhau hoặc overlay chỉ hiển thị một phần. C/root đã tìm Word P0515 nói cả hai mô hình một mask trong khi saved smoke TSVM hai mask. Đây là lỗi lời văn cần E/root kiểm lại nghĩa trường; **không có căn cứ từ hình để kết luận ảnh giả hay mask thứ hai chắc chắn là FP**.

## Sai khác và giới hạn cần báo

### B-001 Quy ước SD không đồng nhất giữa hai thế hệ hình

`Stracth/Bao_Cao/phan_tich_20seed_fp32.py:234` dùng `mat.std(0)` tức ddof=0 trong hai hình legacy `figures/04_convergence_loss_curves.png`, `figures/05_metric_curves_mAP.png`. Bộ mới dùng ddof=1. Với 20 seed, SD ddof=0 bằng sqrt(19/20) lần SD mẫu, nhỏ hơn khoảng **2,532%**. Đây là khác quy ước đã xác nhận, không phải đổi trung bình hay p-value. Hình mới nhúng Word dùng SD mẫu. Khuyến nghị ghi rõ định nghĩa hoặc thống nhất các thế hệ hình ở bước sửa sau.

### B-002 11 hình legacy chưa tái tạo giống từng pixel

Kết quả trong `other_reproduction_pixel_comparison.json`: 9 hình cùng shape khác pixel, 2 hình CM khác shape. Mở đối chiếu hình overall cho thấy cùng con số nhưng tiêu đề/trục dịch vị trí. Chưa xác định nguyên nhân render chính xác; thư viện/font/rcParams hoặc phiên bản script chỉ là khả năng cần truy snapshot. Không suy ra dữ liệu sai từ non-identical pixels. Khuyến nghị lưu phiên bản generator và môi trường render riêng cho các hình legacy.

### B-003 Kiểm tra chéo một nhãn không tái tạo giống từng ký tự

Root replay 1.000 mask hiện chỉ 999 nhãn trùng hoàn toàn. Phòng B độc lập trích đúng hàm chuyển đổi bằng AST và xác nhận trường hợp `labels/val/ck2bxiswtxuw80838qkisqjwz.txt` với numpy 2.2.6/OpenCV 4.12.0: cả hai đa giác 30 đỉnh, chỉ đỉnh index 19 khác từ (0,621578;0,328846) sang (0,616747;0,334615), tương đương khoảng (−3;+3) pixel trên ảnh 621×520.

Raster hóa cùng quy tắc `round(coords×dimensions)` rồi `cv2.fillPoly`: **27 pixel khác**, diện tích 142.983 so với 142.978, IoU giữa hai đa giác **0,99981118**. Đây không phải IoU chất lượng của mô hình. Câu Word `P0447` nói 1.000/1.000 nhãn trùng từng ký tự cần được ràng buộc môi trường hoặc sửa theo kết quả kiểm hiện tại. Chưa chứng minh nguyên nhân, không gọi dữ liệu bị hỏng. Không sửa nhãn nguồn để làm khớp.

## Kiểm tra chéo và phạm vi kết luận cuối

Đã nhận số liệu độc lập A và trao đổi với C về caption, số kênh và số mask. Root kiểm checkpoint/inference riêng; D kiểm nguồn paper, E kiểm ứng dụng. Phòng B xác nhận **hình–bảng–nguồn ảnh nhất quán trong các phép kiểm đã nêu**, không chứng nhận phiên Kaggle đã chạy ra sao, quyền tác giả, topology tốt hơn, ưu thế lâm sàng hoặc mọi checkpoint hoạt động như lịch sử.

Ảnh dự đoán ngoài những ảnh được sử dụng trong báo cáo không được kiểm toàn bộ bằng suy luận mới ở phòng B. Việc replay prediction/checkpoint thuộc root/E và cần đúng confidence/IoU/rect/batch. Không mở rộng PASS trên CM/PR sang toàn bộ inference. Không sửa nguyên bản và không đánh giá tỷ lệ Turnitin.

## Tệp bằng chứng

- `coverage.csv`, `figure_inventory.csv`, `word_figure_mapping.csv`: phạm vi và nguồn.
- `summary.json`, `issues.csv`: kết quả máy đọc và điểm cần xử lý.
- `cm_ocr_comparison.csv`, `raw_curve_digitization.csv`, `f1_pixel_consistency.csv`: kiểm ảnh raw.
- `reproduction_pixel_comparison.json`, `other_reproduction_pixel_comparison.json`: so từng pixel sau tái sinh cách ly.
- `word_custom_chart_numeric_checks.csv`: đối chiếu nguồn số của hình riêng Word.
- `dataset_label_crosscheck.json`, `dataset_label_crosscheck.py`: kiểm độc lập một nhãn khác.

## Bổ sung lấy mẫu ảnh dự đoán ngoài Word

Sau tổng kiểm, chọn trước **hai mô hình × seed 0,5,8,18,19**, mỗi run kiểm cặp `val_batch0_labels.jpg` và `val_batch0_pred.jpg`: 10 cặp, 20 JPEG, đều tồn tại, kích thước 1920×1556. Seed 0/5/8 được chọn vì sự cố lịch sử, seed 18/19 vì nằm ở nhóm muộn; không chọn theo ảnh có lợi cho mô hình. `prediction_sample_review.csv` ghi đủ đường dẫn, hash và nhận xét từng cặp; `prediction_sample_inventory.csv` giữ danh mục từng tệp.

Đã mở cả 10 contact-pair và các crop 1:1 cho trường hợp cần xem rõ. Ảnh GT/pred có cùng thứ tự tile và nền ảnh tương ứng; không thấy ghép nhầm ảnh đầu vào ở mức quan sát. **Mười ảnh GT mosaic có cùng một hash**: đây là cùng batch 16 tile lặp qua 10 run, không phải 160 ảnh độc lập. Không suy kết quả toàn validation hay ưu thế mô hình từ mẫu này.

Quan sát cụ thể: ở cả Baseline seed18 và TSVM seed18, tile hàng2/cột3 `bg_31fc3c22-76d5-484b-839a-8ada69051b4d.jpg` có annotation dự đoán, trong khi tệp GT tương ứng rỗng. Crop gốc hiển thị confidence đã làm tròn khoảng 0,3 và 0,4. Đây là ví dụ báo nhầm trong mẫu, không phải mâu thuẫn dữ liệu hoặc bằng chứng hình bị làm sai. Baseline seed19 có vùng GT ở tile hàng1/cột2 `cju8dqkrqu83i0818ev74qpxq.jpg` nhưng không thấy overlay dự đoán trong tile; điều đó chỉ mô tả hình đã lưu, không chứng minh không có prediction dưới ngưỡng hiển thị.

Các `args.yaml` lưu `conf: null`, `iou: 0.7`; mã plotting hiện có mặc định chỉ vẽ khi `conf > 0.25` và hiển thị một chữ số thập phân. Vì ảnh không ghi riêng ngưỡng plotting và raw prediction arrays, không xác nhận điểm làm việc của JPEG chỉ từ số confidence làm tròn. Không tính TP/FP/FN mới, Dice hay IoU mô hình từ các mosaic. Root/E giữ trách nhiệm replay checkpoint có giao thức được ghi nhận. Crop kiểm tại `prediction_samples/full_resolution_crops.png`; không chỉnh JPEG nguồn.
