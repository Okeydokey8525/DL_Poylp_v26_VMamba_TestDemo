# Sửa hiển thị và metadata Web

Đã chỉnh mã nguồn Web gốc; không chỉnh checkpoint, CSV, nhãn dữ liệu hoặc dữ liệu MongoDB thật.

## Nhận diện mô hình

- `DiagnosisController` dùng `DiagnosisModel.fromModelType` để xác định TSVM, thay phép tìm chuỗi `vmamba` vốn không khớp khóa `YOLO26s-TSVM-FP32-seg`.
- Kết quả lịch sử có tên mô hình không thuộc danh mục hiện tại hiển thị “Mô hình cũ”, tránh mặc định gắn Baseline.
- Trang chủ lấy số lượng và tên mô hình từ `DiagnosisModel`, không còn mô tả Nano. Nhãn là “mô hình được hỗ trợ”, không khẳng định mô hình luôn đang online.
- Copy trang chủ phân biệt xem giới thiệu công khai với phân tích ảnh/lịch sử cần đăng nhập.
- Demo dùng tên mô hình hiện tại và ghi “Ảnh minh họa” thay kích thước giả định.

## Kích thước ảnh

- `DiagnosisHistory` có thêm hai trường nullable `imageWidth`, `imageHeight`.
- `FileStorageService.readOriginalImageDimensions` đọc header bằng ImageIO, chỉ từ đường dẫn ảnh gốc nằm trong storage đã kiểm soát; không giải mã cả mảng pixel cho bước metadata.
- Khi lưu phân tích đơn hoặc hai kết quả so sánh, `DiagnosisHistoryService.populateImageDimensions` ghi kích thước thực vào document trước khi lưu.
- Khi xem bản ghi cũ, ưu tiên metadata hợp lệ; nếu chưa có thì đọc header ảnh gốc còn tồn tại. Nếu không xác định được, hiển thị “Chưa xác định”. Không tự ghi migration vào MongoDB khi đọc.
- Không còn hằng 1280 × 720 trong đường hiển thị ảnh thật hoặc placeholder của trang kết quả.
- README module Web mô tả chính sách metadata và tương thích bản ghi cũ.

## Kiểm tra

- Đã chạy bản sao build cách ly trong `source_snapshot` để không ghi vào target của dự án gốc.
- 88 test được chọn: `ImageMetadataRegressionTests`, `SecurityIntegrationTests`, `DiagnosisAnalysisServiceTests`, `ModelComparisonServiceTests`, `OwnershipServiceTests`: **88 pass, 0 failure, 0 error**.
- Có 9 regression mới: 5 kiểm metadata với ảnh PNG thật/kho lưu thật và 4 kiểm HTML Thymeleaf của TSVM/Baseline/mô hình cũ/trang chủ.
- Ảnh kiểm 621 × 530 được đọc và lưu đúng cho cả phân tích đơn và so sánh. Bản ghi cũ thiếu ảnh hiển thị “Chưa xác định”; bản ghi còn ảnh đọc lại đúng kích thước và không gọi repository.save.
- Lần chạy đầu có 2 lỗi kỳ vọng của harness do class HTML có nhiều khoảng trắng. Đã giữ log đầu `targeted_tests.log`, đổi assertion sang so lớp CSS không phụ thuộc số khoảng trắng, chạy lại thành công trong `targeted_tests_rerun.log`.
- Đây là kiểm component/mock/render. Root thực hiện tiếp Web/MongoDB/FastAPI thật sau khi gộp cả sửa truy vấn.

## Tệp thay đổi thuộc phòng hiển thị

- `src/main/java/com/polyp/polypweb/controller/DiagnosisController.java`
- `src/main/java/com/polyp/polypweb/controller/HomeController.java`
- `src/main/java/com/polyp/polypweb/document/DiagnosisHistory.java`
- `src/main/java/com/polyp/polypweb/service/FileStorageService.java`
- `src/main/java/com/polyp/polypweb/service/DiagnosisHistoryService.java`
- `src/main/java/com/polyp/polypweb/service/ModelComparisonService.java` (chỉ đoạn lưu metadata, không sửa truy vấn)
- `src/main/resources/templates/index.html`
- `src/main/resources/templates/diagnosis-result.html`
- `src/test/java/com/polyp/polypweb/SecurityIntegrationTests.java`
- `src/test/java/com/polyp/polypweb/service/ImageMetadataRegressionTests.java` (mới)
- `README.md`

Backup trước sửa nằm trong `backups/`. Các bản ghi cũ không bị sửa hoặc di chuyển.
