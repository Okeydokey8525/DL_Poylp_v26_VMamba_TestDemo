# 07_ung_dung_web: website PolypVision

Mã nguồn ứng dụng web của khóa luận, chép từ bản nộp ngày 11/11/2026.

| Thư mục | Nội dung |
|---|---|
| `polypweb/` | Website Spring Boot (Java 17, cổng 8080): giao diện, tài khoản, lịch sử chẩn đoán, trang `/metrics` |
| `polypweb/ai-service/` | Dịch vụ AI FastAPI (Python 3.12, cổng 8000): nạp YOLO26s-seg và YOLO26s-seg + C2TSVMamba, phân đoạn ảnh và video |
| `co_so_du_lieu/` | Mô tả CSDL MongoDB (`MO_TA_CSDL.md`) và script tạo sẵn collection, chỉ mục (`khoi_tao_csdl.js`) |

Kiến trúc: Trình duyệt → Spring Boot → FastAPI → hai mô hình; Spring Boot lưu dữ liệu vào MongoDB.

**Trọng số mô hình không có trên GitHub.** Trước khi chạy, chép `best.pt` seed 15 của hai mô hình vào `polypweb/ai-service/models/` (tên file và nguồn xem mục "Trọng số mô hình" trong [README chính](../README.md)).

Cách chạy từng bước: mục "Chạy ứng dụng web PolypVision" trong [README chính](../README.md), hoặc `polypweb/README.md`.
