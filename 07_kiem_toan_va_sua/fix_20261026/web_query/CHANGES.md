# Sửa truy vấn lịch sử so sánh

Ngày thực hiện: 26/10/2026. Phạm vi: repository lịch sử so sánh và các test trực tiếp liên quan.

## Nguyên nhân và thay đổi

MongoDB không cho phép đặt một stage `$facet` bên trong nhánh của `$facet` khác. Pipeline cũ dùng facet ngoài cho `invalidGroups`/`records`, rồi facet bên trong `records` cho `metadata`/`data`, nên trang lịch sử thật trả 503 và API trả 500.

`ComparisonHistorySearchRepository.java` được sửa thành một `$facet` duy nhất với ba nhánh cùng cấp:

- `invalidGroups`: đếm nhóm của người dùng hiện tại không đủ hai kết quả hợp lệ.
- `metadata`: lọc các nhóm hợp lệ, áp dụng bộ lọc sau nhóm, rồi đếm tổng.
- `data`: dùng cùng điều kiện lọc với metadata, sau đó sắp xếp, bỏ qua và giới hạn trang.

Mapper đọc `metadata` và `data` trực tiếp từ kết quả ngoài. Vẫn lọc user trước `$group`; số đếm vẫn là số phiên, không phải số document; giữ điều kiện cặp Baseline/TSVM, tên ảnh, URL ảnh gốc và thứ tự phụ theo group ID.

## Kiểm chứng

Đã cập nhật hai unit test hiện có theo cấu trúc phản hồi mới, có kiểm chỉ tồn tại một `$facet`.

Thêm `ComparisonHistoryMongoIntegrationTests.java` gồm bốn test chạy trực tiếp trên MongoDB, bật bằng `COMPARISON_TEST_MONGODB_URI`:

1. Collection rỗng không lỗi và trả trang rỗng.
2. 25 cặp hợp lệ được phân trang đúng; loại nhóm thiếu, trùng, khác tên ảnh hoặc URL; không trộn nhóm giữa hai chủ sở hữu.
3. Từ khóa được hiểu theo nghĩa literal, các bộ lọc phát hiện và ngày địa phương áp dụng trước cả đếm và phân trang.
4. Sắp xếp tổng thời gian có thứ tự phụ ổn định; trang vượt phạm vi vẫn giữ tổng đúng.

Mỗi test tự tạo database có tên ngẫu nhiên bắt đầu `polypweb_comparison_it_`, rồi chỉ xóa chính database đó. Test không tự bật nếu thiếu biến môi trường.

Lệnh đã thực thi trong bản sao build cách ly `project/`:

```powershell
$env:COMPARISON_TEST_MONGODB_URI='mongodb://127.0.0.1:27019/?serverSelectionTimeoutMS=3000'
.\mvnw.cmd '-Dtest=ComparisonHistorySearchRepositoryTests,ComparisonHistoryMongoIntegrationTests' test
```

Kết quả: **6 test chạy, 0 failure, 0 error, 0 skipped; BUILD SUCCESS**. MongoDB 8.3 dùng binary có sẵn, khởi động riêng trên localhost:27019 với dữ liệu trong thư mục sửa lỗi. Đã shutdown sạch, exitCode 0. Log: `query_tests.log`, `mongo.log`, `shutdown.log`.

Các bản sao trước khi sửa nằm trong `backups/`. Không sửa raw CSV, checkpoint, nhãn, Word hoặc các file UI. Kiểm thử toàn Web sau khi gộp các thay đổi được trưởng tổng kiểm thực hiện riêng.
