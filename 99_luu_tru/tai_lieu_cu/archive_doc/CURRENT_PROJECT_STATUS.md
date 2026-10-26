# Trạng thái hiện tại đã đối chiếu của dự án

Cập nhật ngày **26/10/2026**. Đây là trạng thái **workspace local** sau kiểm toán ngày 25/10 và trong đợt chỉnh sửa tài liệu ngày 26/10. Không khẳng định trạng thái GitHub khi chưa đối chiếu remote. Snapshot cũ giữ tại [historical/snapshots_20261026](historical/snapshots_20261026/README_SNAPSHOT.md).

## Phạm vi thực nghiệm chính

- Baseline: YOLO26s-seg; nguồn `Ket_Qua_V2/KetQua_Nen/YOLOv26s-seg/`, chọn seed 0–19.
- Đề xuất: YOLO26s-seg với C2TSVMamba tại layer 10; nguồn `Ket_Qua_V2/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM_FP32/`, seed 0–19.
- **40 lượt × 100 epoch**, cùng cấu hình chính: imgsz 640, batch 8, AdamW, lr0=0,001, warmup 5, close_mosaic 10, amp=False, deterministic=True.
- Các thư mục Baseline ngoài 0–19 và TSVM không có hậu tố FP32 là lịch sử; không trộn vào bảng chính.

## Dữ liệu

`Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/` có 1.200 ảnh: train 1.040 (880 polyp + 160 nền), validation 160 (120 ảnh polyp + 40 nền); validation chứa 127 đối tượng polyp. Ảnh nền có nhãn rỗng. BG 20 là 200 ảnh bổ sung so với 1.000 ảnh polyp, không phải 20% của tổng 1.200 ảnh.

Đã kiểm số lượng, định dạng nhãn và không trùng byte ảnh train/val. Điều này không chứng minh tách bệnh nhân hoặc không có ảnh gần trùng. Danh sách 880/120 được dùng cố định; provenance phát hành bởi tác giả dataset chưa đủ bằng chứng. Tái tạo 1.000 mask giữ đúng 1.063 đối tượng; 999 nhãn khớp từng ký tự ở OpenCV 4.12.0/NumPy 2.2.6, một nhãn khác một đỉnh nhỏ; nguyên nhân chưa xác định. [Tái lập BG 20](28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md).

## Số liệu chính

| Chỉ số tại epoch cực đại mask AP | Baseline | TSVM FP32 |
|---|---:|---:|
| Mask mAP 50–95, mean ± sample SD | 0,718868 ± 0,011768 | 0,723171 ± 0,007197 |
| Mask mAP 50 | 0,906889 | 0,908274 |
| Mask Precision | 0,904095 | 0,914452 |
| Mask Recall | 0,859367 | 0,858979 |
| Val segmentation loss | 1,266294 | 1,232862 |

Δ mask mAP 50–95 = +0,004303; paired t p=0,061431, Wilcoxon p≈0,069580; CI 95% chứa 0. Không kết luận ưu thế trung bình ở α 0,05 hoặc tương đương. TSVM cao hơn 13/20 cặp; SD thấp hơn khoảng 38,85% là quan sát có giới hạn.

Nguồn chuẩn: [06_reports/summary.md](../Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/06_reports/summary.md), các CSV trong `01_raw_analysis`, `02_statistics`, `03_metrics`. `val/sem_loss` ghi 0 ở mọi lượt không được diễn giải thành lỗi thực bằng 0. YOLO26 dùng `val/l1_loss`, không đổi tên thành DFL.

## Epoch và checkpoint

Bảng chính lấy các metric cùng dòng đầu tiên đạt cực đại mask mAP 50–95. `best.pt` được chọn theo tổng box+mask fitness; có 16/40 lượt khác epoch. Kiểm toán đã đọc 40 best.pt, xác nhận TSVM float32 hữu hạn và Baseline lưu float16; cả hai được chuyển float32 khi suy luận. Seed, tên run và embedded history khớp raw đang lưu.

Đã tái đánh giá 40 best.pt với validation sao chép riêng, CPU float32, research fork 8.4.127, rect=True,batch 16,imgsz 640,half=False,workers 0. Không có sai lệch mask AP vượt 0,005 so với CSV fitness. Một số P/R Baseline khác; không ghi PASS AP như mọi metric khớp chính xác. Phân tích này là kiểm chứng phụ, không thay endpoint max-mask hoặc test độc lập.

44.000 ô non-time TSVM cũ/FP32 trùng, còn 2.000 ô time khác. Đây là lineage cần giữ log; có thể phù hợp rerun tất định khi chỉ sửa đường lưu, không tự chứng minh hay phủ định huấn luyện lại.

## Ma trận nhầm lẫn và topology

Số TP/FP/FN là đối tượng; TP+FN=127. Không suy số ảnh nền đúng bằng 40−FP. Dùng bảng mới trong `04_confusion_matrix`; TN ảnh N/A. Các trường legacy `TN_reconstructed` bị đánh dấu không hợp lệ để suy specificity. Val seg loss thấp hơn ở 14/20 cặp khi dùng lower-is-better; root summary cũ đếm chiều tăng cho ra 6, không dùng cột đó như số lượt thắng.

Không có Dice pixel, HD 95, Betti/clDice hoặc bằng chứng trực tiếp bảo toàn topology trong bộ chính. Bốn ablation mode có trong source nhưng chưa có bộ 20 seed đối chứng đầy đủ.

## Kiến trúc và phần mềm

Fork dùng cho TSVM FP32: `ultralytics_Topology-Shape-aware_VMamba_FP32/`. C2TSVMamba thay C2PSA tại layer 10/P5; gate nhân 1+G, FFN haiConv 1×1, residualγ khởi tạo 0,001. Tham khảo [kiến trúc đã sửa](01_KIEN_TRUC_TSVM_TANG_10.md).

PolypVision có Web Java/Spring Boot và FastAPI; Mobile Direct AI là nhánh riêng. Đợt sửa ngày 26/10 đã sửa truy vấn lịch sử so sánh, nhãn mô hình TSVM, kích thước ảnh và tên mô hình trang chủ. Kiểm thử đạt 274 ca Java (gồm 4 ca MongoDB thật), 51 ca FastAPI và 39 kiểm tra HTTP toàn trình trên cơ sở dữ liệu riêng. Đã mở trình duyệt xác nhận lịch sử so sánh và kết quả TSVM hiển thị đúng nhãn, 2 mask, ảnh 621 × 530. Đây là kiểm chứng chức năng trong môi trường local, chưa phải chứng nhận tải hoặc triển khai production. Chi tiết tại [nhật ký sửa](../fix_20261026/FIX_REPORT.md). Mobile chưa chạy lại.

## Nguồn bằng chứng và giới hạn

[Báo cáo kiểm toán](../audit_20261025_193105/AUDIT_REPORT.md) lưu hash của bản Word và tệp nguồn **trước sửa**. Các thống kê gốc, checkpoint và nhãn không được sửa để khớp câu chữ. Các thay đổi tài liệu/mã sau kiểm toán có log trong `fix_20261026/`.

Chưa có báo cáo Turnitin/settings trường; chưa đánh giá ngưỡng 30%. Chưa kiểm chứng GPU lịch sử, external test, patient-level split, đầy đủ topology/ablation, mobile hoặc tải production. Khi thiếu bằng chứng, ghi chưa xác minh.
