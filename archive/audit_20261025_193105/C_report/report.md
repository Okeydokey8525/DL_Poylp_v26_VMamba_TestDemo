# Rà soát nội dung báo cáo chính và đối chiếu dự án

Ngày kiểm tra: 25/10/2026. Phòng C. Phạm vi chỉ đọc nguồn; mọi đầu ra mới nằm trong `audit_20261025_193105/C_report/`.

## Kết luận hiện tại

Bản Word chính mô tả bộ **20 cặp seed FP32** và trình bày các giới hạn khoa học rõ hơn nhiều bản Markdown cũ. Chưa phát hiện sai số trong **357 phép đối chiếu ô số đã thực hiện** của các bảng thống kê, từng seed, epoch và timing. **1.240 trường cấu hình** trích từ 40 `args.yaml` khớp các giá trị được nêu cho thực nghiệm. Đây là kết luận về phép tổng hợp và cách viết; không tự chứng nhận nguồn dữ liệu, mọi checkpoint hoặc toàn bộ ảnh.

Có **hai lỗi nội dung cụ thể trong Word**: số kênh P4 ở Bảng 2.1 và số mặt nạ của ví dụ TSVM ở mục 4.6. Có thêm khoảng trống tái lập về đường dẫn dữ liệu/chương trình BG20. Các Markdown hiện không đồng bộ với Word và có những phát biểu sai hoặc không có bằng chứng nếu dùng cho thực nghiệm hiện tại.

Phòng D cần xác minh tài liệu tham khảo; phòng E cần xác minh ứng dụng. Không dự đoán tỷ lệ Turnitin, không khẳng định đạt ngưỡng dưới 30%.

## Tài liệu, định danh và phương pháp

- Word: `Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx`.
- SHA-256: `2caaf8b42c299f3c73a0087654f8f7d3c2986a83b8878d713613e0c9e1ed0856`.
- Trích OOXML theo thứ tự: **783 đoạn**, **19 bảng**, **24 mục tham khảo**, **13 đoạn có OMML**. Công thức Unicode thường cũng được giữ trong văn bản.
- `Pxxxx` là chỉ số đoạn trực tiếp trong body; `TxxRxxx` là bảng và hàng. Các ID gắn với hash Word trên; không phải số trang. `word_blocks.csv` giữ nguyên văn và section; `full_block_review_coverage.csv` lưu phạm vi đọc của từng block không rỗng.
- Đã đọc nội dung tất cả chương, phần đầu, kết luận và phụ lục; kiểm tra nguồn theo nhóm claim. Không đánh dấu mọi câu lý thuyết hoặc mọi thông tin tác giả là đã xác minh ngoại sinh.
- Dùng Python bundled, thư viện chuẩn và Pillow; không chạy builder báo cáo, converter dữ liệu, train hoặc inference. Tính mean/SD từ raw CSV; p t-test bằng tích phân mật độ t với thư viện chuẩn; CI dùng t tới hạn df19. Wilcoxon đối chiếu bảng hiện có và phòng A tính độc lập bằng SciPy.
- Đọc kỹ năng Word. Lượt này không tạo/sửa/giao một Word mới, không nghiệm thu bố cục toàn trang. Phòng B kiểm ảnh nhúng và mapping; không suy lỗi công thức chỉ từ text extraction làm mất bố trí phân số/dấu mũ.

## Hai sai lệch đã xác nhận trong Word

### C-001 Bảng 2.1 ghi sai số kênh Backbone P4

Vị trí `T03R003`: `Backbone P4 | 16 | 40 × 40 | 512`.

YAML `ultralytics_Topology-Shape-aware_VMamba_FP32/cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml:13,26-27` có small width 0,5 và base channel 512 tại layer 5/6. Parser `nn/tasks.py:2071` áp dụng width nên đầu ra là **256 kênh**. Root kiểm checkpoint và xác nhận layer 6 cv2 out_channels=256 ở cả Baseline và TSVM. Các hàng P3/P5/head còn lại của bảng phù hợp phép scale khi kiểm tĩnh.

Ảnh hưởng: sai mô tả kích thước kiến trúc, không làm thay đổi bảng mAP. Phòng B xem Hình 2.1 và xác nhận sơ đồ không ghi số kênh P4 nên không lặp lại lỗi này.

### C-002 Đoạn ví dụ nói TSVM có một mặt nạ, JSON ghi hai

Vị trí `P0515`, mục 4.6: “Cả hai mô hình trả một mặt nạ trên ảnh polyp…”.

`.codex_revision_20261016/smoke_results.json` lưu trên cùng ảnh `cju0s690hkp960855tjuaqvv0.jpg`: Baseline maskCount=1, TSVM maskCount=**2**, confidence TSVM khoảng 0,58384. Checkpoint hash khớp những hash ghi trong phụ lục C. Cả hai ảnh nền có maskCount=0. Bản lưu `.codex_report_work_20261015/smoke_results.json` cũng là nguồn lịch sử tương ứng.

Đây là mâu thuẫn giữa lời văn và kết quả smoke đã lưu. Không tự gán mặt nạ thứ hai là false positive khi chưa kiểm dự đoán/nhãn. Phòng B xem Hình 4.2: một nhãn nhìn thấy không đủ để suy số mask do chồng lấp/hậu xử lý; hình không công bố maskCount nên **không kết luận hình giả**. Phòng E cần kiểm nghĩa trường phản hồi và suy luận thật theo phạm vi được giao.

## Tái lập dữ liệu và tài liệu không đồng bộ

### C-003/C-004 Hướng dẫn tái lập chưa đầy đủ cho layout hiện tại

`P0766` chỉ tới `Stracth/Du_Lieu/convert_kvasir_to_yolo_seg.py`. Hàm main tại dòng 773 đặt output `Kvasir_YOLO_SEG`, không thực hiện bổ sung normal-cecum để tạo BG20. Builder BG20 thực tế có tại `Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py`; main dòng 124–150 vẫn trỏ các input theo layout cũ và output `archive/Kvasir_YOLO_SEG_BG20`.

`archive/data_bg20.yaml:2` cũng chỉ tới thư mục `archive/Kvasir_YOLO_SEG_BG20` không tồn tại; bộ dữ liệu thực ở `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20`. Root xác nhận độc lập. Đây là lỗi tái lập cục bộ, **không suy ra Kaggle historical train đã nạp sai dữ liệu**, vì `args.yaml` dùng đường dẫn Kaggle riêng.

### C-005 Các bản thảo Markdown có thể tái đưa lỗi cũ vào Word

`Bao_cao/md viet bao cao/06_CHUONG_5_THU_NGHIEM_VA_DANH_GIA_KET_QUA.md` vẫn dùng bộ 10 seed (dòng 23–40), xem `TN=40-FP` là hợp lệ (80–93), có Dice/IoU không cùng định nghĩa với AP và tốc độ GPU 18,2/28,5ms (216). Word mới `P0550/P0666/P0702` đã loại những diễn giải này.

`05_CHUONG_4_...md:80` ghi optimizer SGD, khác AdamW trong 40 args và Word T07R005; cùng bản thảo còn mô tả notebook tự vòng lặp nhiều seed tại dòng 67, khác notebook thực tế. `07_KET_LUAN_...md:24` vẫn liệt kê Dice/IoU như kết quả đo. Không được dùng các bản này làm nguồn sinh lại báo cáo hiện tại mà chưa xử lý sai lệch.

### C-006 Sơ đồ kiến trúc Markdown sai cơ chế hiện tại

`doc/01_KIEN_TRUC_TSVM_TANG_10.md:49,62,69` ghi O(N), `F_ss2d*G` và FFN Conv3×3/GELU. Code có tensor work O(LlogL), `F_m*(1+G)` và FFN hai Conv1×1. Word `P0315/P0321/P0327` mô tả đúng những điểm này.

### C-007 Các điểm vào kiến thức vẫn ở giai đoạn trước

`doc/CURRENT_PROJECT_STATUS.md:68-92` còn số liệu 10 seed và ràng buộc FP+TN=40; `doc/README.md:5,120` giới thiệu 10 seed/20 lượt. Ngày snapshot cũ có thể giải thích phạm vi lịch sử, nhưng tên “current” và quy tắc ưu tiên nguồn có nguy cơ khiến người tiếp quản dùng nhầm bộ. Cần giữ lịch sử và phân nhãn hiện trạng rõ hơn trong bước chỉnh sửa sau này.

## Đối chiếu theo chương

| Phần | Kết quả đối chiếu | Giới hạn còn lại |
|---|---|---|
| Tóm tắt/mở đầu | Đúng 20 cặp, 40 lượt, FP32 và giới hạn validation | Không kiểm chứng thông tin hành chính/tác giả |
| Chương 1 | Phân biệt instance/pixel, ảnh/object và tính mới được viết có điều kiện | D xác minh mô tả từng paper và citation |
| Chương 2 | Gate1+G, kernels, gamma, modes, số bước9/pad512, O(LlogL), lưu FP32 phù hợp code | P4 sai kênh; công thức recurrence là mô tả giản lược, không hiển thị clamp số học |
| Chương 3 | Counts BG20 khớp; C đọc 1000 ảnh polyp và 1000 normal-cecum, xác nhận kích thước/333size như P0353/P0356; preprocessing và HSV đúng code | Root/B kiểm chi tiết Otsu5–8, contours1206/143, vertices333,2→24,6 và ví dụ; nguồn chính thức split880/120 cần D |
| Chương 4 | Notebook từng seed và cảnh báo fork cũ được nêu đúng; static registry/FP32 có căn cứ | C002; số test51/261/498 là evidence lịch sử cần E kiểm; không coi mock là inference |
| Chương 5 | Tables5.1/5.2/5.3/5.4 và AppendixB được kiểm số; p=.061431, CI chứa0; Levene được giới hạn thăm dò; TN không sử dụng | CM chỉ khớp bảng trích kế thừa, B kiểm với ảnh; D kiểm Table5.8 |
| Benchmark | Tính lại mean/SD và phân vị từ400timing; protocol timer đọc từ script; không trộn forward/pipeline; không suyGPU | Không đo lại trong lượt này; metadata lịch sử chưa phải bằng chứng thao tác vật lý thực tế |
| Kết luận/phụ lục | Không thấy đảo p>0,05 thành ưu thế; topology/test ngoài là kế hoạch; checkpoint và maxmask được tách | Chưa đánh giá lại AP tất cả checkpoint; C003/C004 về tái lập |

### Thống kê và điều kiện so sánh

Quy tắc max-mask của Word khớp trích xuất gốc; 16/40 argmax khác fitness box+mask được tính lại. Không ghép cực đại của mỗi metric vào một run tưởng tượng. Word có lưu ý same seed không bảo đảm cùng toàn bộ luồng RNG, validation đã chọn epoch, không có patient-disjoint metadata, p>0,05 không phải tương đương. Những lưu ý này phù hợp phạm vi bằng chứng hiện có.

SD giảm khoảng38,85% là quan sát mô tả. Levene p≈0,0257 được gọi thăm dò, không được dùng làm kết luận ưu thế trung bình. AP được phân biệt với Dice điểm ảnh. Counts CM không bị chuyển thành specificity. Phòng A tái tính độc lập bằng SciPy đồng ý phần số liệu mới; các legacy fields sai trong root summary không xuất hiện như kết luận đúng trong Word.

## Liêm chính học thuật và Turnitin

`citation_inventory.csv` giữ 24 tài liệu, ID ổn định `CIT-001`–`CIT-024`, nguyên văn bibliographic entry, DOI/URL. D cần xác minh metadata và đoạn nguồn hỗ trợ; DOI tồn tại không đủ xác nhận claim. Riêng `P0363` gán danh sách880/120 cho tác giả dataset cần chứng cứ provenance; file train/val cục bộ chỉ chứng minh danh sách, không chứng minh quyền tác giả hoặc tính “official”.

Lượt này không đối chiếu toàn bộ câu với cơ sở dữ liệu Turnitin và chưa có báo cáo/thiết lập loại trừ của trường hoặc lịch sử bài nhóm đã nộp. Các chương có nội dung phương pháp phổ biến, cùng đoạn dữ liệu được kế thừa từ báo cáo nhóm trước, nên cần kiểm nguồn từng đoạn khi có báo cáo thật; không suy đây là đạo văn từ trùng nội bộ và không tự gán một phần trăm trùng lặp.

Không cam kết “qua Turnitin”, không viết lại để né phát hiện. Các vấn đề citation/close paraphrase cần xử lý theo ý nghĩa, nguồn gốc và quyền sử dụng; nguyên văn cần chỉ rõ trích dẫn. Chỉ số similarity và chỉ báo AI writing phải được đọc riêng theo quy định trường. D xử lý overlap với PDF/tài liệu gốc; C chưa chứng nhận novelty hoặc toàn bộ trích dẫn.

## Bàn giao và trạng thái

- **A**: đã trao đổi về stats/epoch; A độc lập SciPy xác nhận bảng mới. Chứng thực checkpoint là tầng riêng.
- **B**: đã trao đổi và thống nhất C001 không lặp trong sơ đồ; C002 là lỗi lời văn so với JSON, không kết luận hình giả. Mapping/kiểm hình đầy đủ nằm trong báo cáo B.
- **D**: dùng citation inventory, `T02/T17`, `P0268-P0280/P0363/P0733-P0756`; cần phản hồi mức hỗ trợ, phiên bản và số liệu.
- **E**: kiểm `T09/P0515`, historical test logs, API/runtime4mức; phân biệt current run và lịch sử.
- **Root**: review cuối và xử lý các bằng chứng còn thiếu. `issues.csv` ghi riêng confirmed mismatch, reproducibility gap và pending; không tự gộp thiếu bằng chứng thành lỗi hoặc PASS.

Đầu ra: `word_blocks.csv`, `word_extracted.txt`, `equations.csv`, `citation_inventory.csv`, `claim_evidence.csv`, `numeric_cell_checks.csv`, `training_configuration_checks.csv`, `raw_metrics_recomputed.csv`, `issues.csv`, `evidence_requests.csv`, `full_block_review_coverage.csv`, `review_summary.json`, hai script tái lập. **Không sửa bản gốc**.
