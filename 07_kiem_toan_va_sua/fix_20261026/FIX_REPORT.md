# Nhật ký hoàn tất chỉnh sửa ngày 26/10/2026

Phạm vi: bốn nhóm sửa đã được người dùng cho phép sau kiểm toán. Bản kiểm toán trước sửa giữ nguyên tại audit_20261025_193105. Không thay số liệu thí nghiệm để làm đẹp kết quả.

## 1. Lịch sử so sánh Web

ComparisonHistorySearchRepository bỏ cấu trúc $facet lồng nhau mà MongoDB từ chối (lỗi 40600), chuyển các nhánh invalidGroups, metadata, data thành nhánh cùng cấp. Giữ điều kiện chủ sở hữu, group hợp lệ, lọc, đếm trước phân trang và thứ tự ổn định. Thêm bốn kiểm thử với MongoDB thật: dữ liệu rỗng; 25 group và dữ liệu sai/chủ khác; lọc; sắp xếp và trang ngoài phạm vi. Chi tiết mã và log: web_query/CHANGES.md.

## 2. Thông tin hiển thị Web

- Nhận dạng model qua DiagnosisModel thay cho tìm chuỗi vmamba; khóa TSVM FP32 hiện lên đúng VMAMBA. Khóa không nhận dạng hiện Mô hình cũ.
- Lưu imageWidth/imageHeight khi tạo kết quả đơn và so sánh. Bản ghi cũ đọc header ảnh nếu còn ảnh; thiếu thông tin hiện Chưa xác định, không gán 1280×720.
- Trang chủ dùng tên hai cấu hình s đang hỗ trợ, bỏ tên Nano và danh sách cấu hình chưa triển khai; mô tả rõ so sánh hai mô hình trên cùng ảnh.
- Không thực hiện migration ghi hàng loạt vào dữ liệu cũ. Có kiểm thử header ảnh, lưu metadata, render HTML và hồi quy.

## 3. Báo cáo Word

Đã sao lưu và sửa đồng bộ bản chính CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx và bản _MoRong_FP32.docx trong Bao_cao. Chỉ thay word/document.xml; 55 thành phần ZIP còn lại, bao gồm hình và style, giữ nguyên.

- Backbone P4: 512 → 256 kênh, theo mã triển khai.
- Ảnh minh họa: Baseline 1 mask, TSVM 2 mask; số mask không được dùng riêng để suy ra chất lượng.
- Bỏ khẳng định chưa xác minh rằng tác giả dataset cung cấp split 880/120; trình bày đúng hai danh sách cố định đang dùng.
- Ghi đúng 999/1000 nhãn tái tạo khớp từng ký tự. Một nhãn lệch một đỉnh 3 pixel trên mỗi trục, chưa rõ nguyên nhân; giữ nhãn hiện hành.
- Sửa đường dẫn script BG20 và bổ sung hướng dẫn tái lập.
- Cập nhật 274 kiểm thử Java và 51 FastAPI vừa chạy; phân biệt 498 Flutter là log cũ, không chạy lại Mobile.

Chi tiết trước/sau từng đoạn và SHA-256: word/changes.json. Bản cuối render 97 trang tại word/rendered_verified, đã xem trực quan riêng đủ 97 trang qua bốn nhật ký QA. Các thư mục rendered và rendered_final là trung gian, không phải bản xác nhận cuối.

## 4. Tài liệu, cấu hình và khả năng tái lập

- Cập nhật doc/README.md, CURRENT_PROJECT_STATUS và mô tả TSVM theo source: P4=256, gate 1+G, FFN 1×1 và giới hạn phát biểu kiến trúc.
- Đánh dấu các tài liệu 10 seed/draft cũ là lịch sử; thêm chỉ dẫn sang kết quả 20 seed FP32 hiện hành.
- Đánh dấu bảng TN_reconstructed=40−FP cũ không hợp lệ cho ma trận detection; ghi nhận lỗi chiều đếm thắng loss ở tổng hợp cũ. Giữ artifact cũ để truy vết và chỉ dẫn sang bảng chuẩn đã đối chiếu.
- data_bg20.yaml trỏ tới dataset thực tế. Script BG20 nhận CLI/dry-run, từ chối ghi đè thư mục dữ liệu chuẩn hoặc đầu ra đã tồn tại, không còn xóa đệ quy hay tự ghi đè YAML gốc.
- Tái tạo vào thư mục riêng: 1040 train, 160 val; 160/40 nhãn rỗng; 936/127 instance. Cả 1200 ảnh và danh sách nền khớp byte; 999 nhãn khớp và một sai khác đã công khai.
- Chặn script tạo Word lịch sử tự ghi đè báo cáo chính.

Danh sách file và hash: documentation/documentation_changes.json; kiểm tra tái lập: documentation/validation.json.

## Bằng chứng kiểm thử

| Phép kiểm | Kết quả | Bằng chứng |
|---|---|---|
| Java toàn bộ, gồm MongoDB thật | 274 đạt, 0 lỗi, 0 bỏ qua; 4 ca MongoDB thật | integration/java_test_summary.json, logs/maven_full.log |
| FastAPI | 51 đạt; 3 cảnh báo thư viện | integration/logs/ai_tests.log |
| HTTP với Web + AI + MongoDB riêng | 39/39 đạt | integration/runtime_summary.json, runtime_results.json |
| Trình duyệt | Đăng nhập, lịch sử so sánh có group, trang TSVM có badge đúng, 2 mask, 621×530 | integration/screenshots và browser_verification.md |
| Word | Hai bản bằng SHA; chỉ document.xml thay đổi; 97 trang đã QA | final_validation.json, word/qa_pages_*.md |
| Dữ liệu và snapshot source | Đối chiếu SHA với manifest trước sửa và source đã kiểm thử | final_validation.json |

Kiểm tra HTTP gồm tạo hai kết quả inference thật, tạo group so sánh, lịch sử rỗng/có dữ liệu, tải ảnh/metadata và chủ khác bị từ chối. Không dùng thời gian một request để thay benchmark khoa học. Môi trường thử dùng DB/kho ảnh riêng, không dùng DB cá nhân thật. Mã nguồn sửa nằm trong ứng dụng gốc; bản copy integration/project chỉ phục vụ build/test.

## Những điểm còn mở

Không thể kết luận tỷ lệ Turnitin dưới 30% khi chưa có báo cáo và quy định loại trừ của trường; không gửi báo cáo lên dịch vụ bên ngoài. Một đỉnh nhãn lệch chưa rõ nguyên nhân. Các giới hạn test ngoài, ablation, topology, tốc độ GPU và tải đồng thời vẫn còn; không được ghi là đã hoàn thành. Kết quả chính vẫn là mức tăng mask AP trung bình nhỏ, paired t-test p≈0,0614, chưa đạt ngưỡng 0,05.
