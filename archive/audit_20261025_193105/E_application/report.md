# Kiểm toán ứng dụng PolypVision

Ngày kiểm tra 25/10/2026. Phòng E chỉ ghi trong thư mục kiểm toán; không sửa mã nguồn, checkpoint, báo cáo hoặc dữ liệu ứng dụng thật. Mobile không được chạy.

## Kết luận

Web Java và FastAPI khởi động được với MongoDB và storage riêng. Đã thực hiện suy luận thật, cùng một ảnh qua hai checkpoint, kiểm tra quyền sở hữu/xuất/xóa, thao tác trình duyệt tải ảnh và so sánh, và xác minh bản ghi/ảnh còn nguyên sau khi khởi động lại Java.

**Có lỗi chức năng mức cao:** danh sách lịch sử so sánh bị lỗi do `$facet` lồng `$facet`, MongoDB từ chối pipeline với mã 40600. Việc tạo một phiên so sánh và mở trực tiếp chi tiết phiên vẫn hoạt động. Không được kết luận ứng dụng hoàn toàn đúng chỉ từ việc 261 test Java pass.

Có các sai lệch giao diện/metadata: trang chủ còn tên Nano; kết quả TSVM gắn badge Baseline; kích thước ảnh bị ghi cứng 1280×720. Lời văn báo cáo nói TSVM trả một mask cũng không đúng với suy luận thật đã tái hiện: TSVM trả hai, Baseline một trên ảnh minh họa.

## Môi trường và phạm vi

- Nguồn: `DeepLearning/Ung_Dung/polypweb`; Web nằm trong `polypweb/`, FastAPI trong `polypweb/ai-service/`, Mobile trong `app_polyp/`.
- Java 17.0.19, Spring Boot 4.1.0; Python app venv và PyTorch CPU. Chạy Web từ jar dựng trong `source_snapshot/target/`, không dùng target cũ của dự án gốc.
- Đã so **174 tệp nguồn** của snapshot với nguồn hiện tại, tất cả cùng SHA-256. Các template trong jar cũng khớp byte với template nguồn. Bằng chứng: `source_copy_comparison.json`.
- Chỉ bind localhost: Web18080, AI18000, Mongo27018. Database kiểm thử `polypweb_audit_20261025`; storage và dbpath đều nằm trong E_application. Hai tài khoản thử có miền `example.invalid`; không dùng tài khoản/dữ liệu ứng dụng thật.
- `runtime/health.json` ghi 2/2 model ready với SHA checkpoint trùng manifest: Baseline `61ebd028...a3906`; TSVM `b0578c76...2c7a8`. Runtime source ép float32 và `half=False`; root kiểm tensor checkpoint riêng.
- Timing trong lần kiểm này có cold start và tải CPU cạnh tranh với revalidation của root. **Không dùng thời gian phản hồi này làm benchmark hoặc thay số benchmark đã công bố.**

## Các mức bằng chứng

| Kiểm tra | Kết quả | Giới hạn |
|---|---|---|
| Java unit/MockMvc suites | 261 test, 0 failure, 0 error trong bản dựng cách ly | Các phần repository/service được mock; không chứng minh mọi pipeline Mongo thật hợp lệ |
| FastAPI pytest | 51 pass, 3 deprecation warnings, 3,39s | Test doubles/mocks không thay thế suy luận checkpoint thật |
| FastAPI suy luận thật | 4 phép dự đoán: hai model × ảnh polyp và nền | Không phải đánh giá chất lượng cả dataset |
| HTTP qua Web thật | Auth, CSRF, upload, compare, history đơn, export, ownership, delete | Phân biệt với thao tác browser; lỗi comparison-history được giữ nguyên |
| Browser end-to-end | Đăng nhập → chọn ảnh → TSVM → result; tải ảnh → hai model → comparison; đọc lịch sử đơn | Không chạy trên mọi browser/kích thước màn hình |
| Persistence | Bản ghi và SHA ảnh download giữ nguyên sau khi restart Java | Không thử restart máy hoặc MongoDB failover |
| AI không khả dụng | Dừng đúng AI process audit → Web503; lịch sử không tăng | Không phải kiểm thử tải/timeout toàn diện |
| Mobile | Chỉ đọc entrypoint, Direct AI config và README | Không chạy Flutter, không xác nhận lại con số 498 test trong báo cáo |

`app_claim_evidence.csv` lưu 14 phát biểu với mức chứng cứ và đường dẫn cụ thể. Nhật ký JUnit ở `logs/ai_tests.xml` và `source_snapshot/target/surefire-reports/`; Java tổng hợp ở `java_test_summary.json`.

## Lỗi được xác nhận

### E-004 Lịch sử so sánh không truy cập được

- **Vị trí:** `polypweb/src/main/java/com/polyp/polypweb/repository/ComparisonHistorySearchRepository.java`, outer `$facet` quanh dòng50 và inner `$facet` ở nhánh records quanh143–153.
- **Tái hiện:** tạo phiên so sánh thật, sau đó mở `/comparisons`: HTML503. Gọi `/api/v1/comparisons` bằng tài khoản đã đăng nhập: API500. Lịch sử phân tích đơn `/history` và dashboard vẫn200.
- **Nguyên nhân đã chứng minh:** gọi trực tiếp chính repository đã biên dịch với MongoTemplate vào MongoDB audit, nhận `Location40600: $facet is not allowed to be used within a $facet stage`. Harness đọc query thực, không thay source hoặc query.
- **Bằng chứng:** `logs/comparison_diagnostic.log`, `runtime_http_before.json`, `screenshots/06_comparison_history_error.png`, `runtime/ComparisonDiagnostic.java`.
- **Khắc phục đề xuất:** đặt các nhánh data/count/invalidGroups cùng cấp hoặc tách truy vấn; cập nhật mapping kết quả tương ứng. Thêm test Mongo thật cho lịch sử rỗng và có dữ liệu, phân trang/bộ lọc. Chưa áp dụng sửa.
- Tài liệu chính thức liệt kê `$facet` trong các stage không được đặt bên trong `$facet`: [MongoDB $facet](https://www.mongodb.com/docs/manual/reference/operator/aggregation/facet/), phần Behavior. Đã truy cập ngày25/10/2026.

### E-002 TSVM bị gắn badge Baseline

`DiagnosisController.java:147–149` dùng `result.getModelType().toLowerCase().contains("vmamba")`. Chuỗi `YOLO26s-TSVM-FP32-seg` không chứa `vmamba`, nên `diagnosis-result.html:23–24` hiển thị Baseline. Enum `DiagnosisModel` đã có mapping chính xác, và API trả `modelCategory=VMAMBA`; đây là lỗi phân loại trên view, không phải bằng chứng nạp nhầm model. Đề xuất dùng enum/key thống nhất và test HTML TSVM. Bằng chứng `screenshots/03_tsvm_result_badge.png`.

### E-003 Kích thước ảnh hiển thị sai

`DiagnosisHistoryService.java:110` truyền hằng `1280 × 720 px`. Ảnh `cju0s690hkp960855tjuaqvv0.jpg` thực tế621×530, nhưng trang kết quả ghi1280×720. Đề xuất thu width/height khi giải mã và lưu metadata thực; xử lý bản ghi cũ có chủ đích. Bằng chứng `screenshots/04_tsvm_maskcount_dimensions.png`. Chưa sửa.

### E-001 Trang chủ còn tên mô hình Nano

`HomeController.java:18` hard-code `YOLO26n baseline và YOLO26n-VMamba`. Trang phân tích, registry và inference thật đang dùng cặp small. Đề xuất lấy tên từ danh mục thống nhất; đừng chỉ đổi nhãn nếu chưa kiểm checkpoint. Bằng chứng `screenshots/02_home_stale_model.png`, `runtime/health.json`.

### E-005 Copy đăng nhập chưa rõ phạm vi

`templates/index.html:31` ghi không cần đăng nhập để trải nghiệm giao diện minh họa, trong khi `/diagnose` và `/compare` được bảo vệ và redirect302 tới login. Có thể câu này chỉ nói demo tĩnh công khai; vì vậy ghi **mơ hồ về phạm vi**, không gọi là lỗi bỏ qua xác thực. Đề xuất tách rõ demo giới thiệu và inference/lịch sử cần tài khoản.

### E-006 Xác nhận lại lỗi lời văn báo cáo C-002

Suy luận thật dùng cùng ảnh/hash, model/hash và confidence0,25 cho kết quả:

| Mẫu | Baseline masks | TSVM masks |
|---|---:|---:|
| `cju0s690hkp960855tjuaqvv0.jpg` | 1 | 2 |
| `bg_0111fb06-3113-4abf-9050-7bfb8d4688f5.jpg` | 0 | 0 |

Confidence polyp tương ứng0,8833031654 và0,5838399529, khớp log smoke lịch sử. Word P0515 nói một mask cho cả hai nên sai. Không tự gán mask thứ hai là false positive khi chưa thực hiện phép ghép GT. JSON `runtime/true_inference_smoke.json` và browser screenshot04 xác nhận độc lập; root nên gộp E-006 vào C-002 để không đếm hai lần một lỗi.

## Kiểm thử âm và quyền sở hữu

- Không đăng nhập: Web chuyển302 tới login, API401. POST login thiếu CSRF403.
- Hai tài khoản khác nhau: người không sở hữu không xem/xuất/xóa được các bản ghi hoặc phiên so sánh (403); chủ sở hữu xuất được metadata/ảnh (200), xóa được (204), đọc sau xóa404.
- Ảnh sai MIME bị AI415; model không tồn tại422. Web multipart rỗng400; JPEG hỏng422; model sai400. Không có dữ liệu thành công giả trong các trường hợp đã kiểm.
- Có **một kỳ vọng sai của test harness**: case `reject_empty_web_image` ban đầu gửi urlencoded tới endpoint chỉ nhận multipart nên415 là đúng. Giữ nguyên log ban đầu, ghi giải thích ở `runtime_http_review.json`; test bổ sung gửi multipart rỗng đúng giao thức nhận400. Không tính trường hợp này là bug ứng dụng hoặc sửa log cho đẹp.
- Dừng đúng AI audit: Web trả503 và danh sách lịch sử trước/sau giống nhau (`runtime_http_ai_off.json`).

## Tính toàn vẹn và cleanup

Chỉ tạo bản sao build, log, ảnh bằng chứng và dữ liệu kiểm thử trong E_application. Không chỉnh code, config hay checkpoint nguồn. Đã kiểm lại hash174srcfiles, không có tệp nào thay đổi (`source_after_check.json`); root có snapshot phạm vi rộng hơn để tổng kiểm.

Đã dừng AI audit và Java audit bằng PID có kiểm tra executable/command line; Mongo audit được shutdown bằng lệnh admin trên chính localhost27018 và log xác nhận `mongod shutdown complete`, exitCode0. Dữ liệu DB/storage kiểm thử vẫn được giữ để truy vết. `cleanup.json` ghi trạng thái cuối. Các server người dùng trên cổng khác không được đụng tới.

## Phần chưa kiểm chứng

Chưa kiểm admin UI, đổi mật khẩu, mọi tổ hợp bộ lọc, tải đồng thời, video, nhiều browser/điện thoại, hoặc triển khai production. Không xác nhận hiệu quả lâm sàng hay khả năng video thời gian thực. Mobile vẫn source-only. Không dùng test pass để che lỗi pipeline Mongo thật hoặc dùng inference ảnh minh họa để chứng minh ưu thế mAP.
