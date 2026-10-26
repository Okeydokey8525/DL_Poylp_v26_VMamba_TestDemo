# Tài liệu hiện trạng YOLO26s seg và TSVM FP32

Cập nhật tài liệu ngày **26/10/2026** sau kiểm toán độc lập. Phạm vi nghiên cứu hiện dùng **hai mô hình, 20 seed mỗi mô hình (0–19), tổng 40 lượt huấn luyện**, trên BG 20. Tài liệu này mô tả workspace local, không khẳng định đã đồng bộ lên GitHub.

## Đọc theo thứ tự

1. [Trạng thái và nguồn hiện tại](CURRENT_PROJECT_STATUS.md).
2. [Kiến trúc TSVM thực sự được cài đặt](01_KIEN_TRUC_TSVM_TANG_10.md).
3. [Hướng dẫn tái lập BG 20 và các giới hạn](28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md).
4. [Báo cáo kiểm toán ngày 25/10](../audit_20261025_193105/AUDIT_REPORT.md), gồm báo cáo của năm phòng và các giới hạn kiểm tra.
5. [Báo cáo kết quả chuẩn 20 seed](../Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/06_reports/summary.md) và [quản lý hiện vật legacy](../Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/LEGACY_ARTIFACTS.md).

## Nguồn ưu tiên

| Nội dung | Nguồn cần đối chiếu |
|---|---|
| Lịch sử từng lượt | `Ket_Qua_V2/KetQua_Nen/YOLOv26s-seg/` và `Kvasir_BG20_YOLO26s_seg_TSVM_FP32/`, chỉ seed 0–19 |
| Bảng chính | `KQ_Nen_DX_20seed_FP32/01_raw_analysis/`, `02_statistics/`, `03_metrics/` |
| Ma trận đối tượng | `KQ_Nen_DX_20seed_FP32/04_confusion_matrix/`; TN ảnh là N/A |
| Kiến trúc và lưu checkpoint | `ultralytics_Topology-Shape-aware_VMamba_FP32/` |
| Dữ liệu đang dùng | `Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/` |
| Bản Word chính | `Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx` |
| Chỉnh sửa sau kiểm toán | `fix_20261026/`, tách khỏi bằng chứng kiểm toán trước sửa |

## Kết luận số liệu cần giữ nguyên

Mask mAP 50–95 tại epoch cực đại mask của từng lượt: Baseline **0,718868 ± 0,011768**; TSVM FP32 **0,723171 ± 0,007197**. Chênh lệch **+0,004303**, paired t-test **p = 0,061431**, CI 95% **[−0,000228; 0,008834]**. Chưa đạt ý nghĩa thống kê ở α = 0,05. SD mẫu thấp hơn khoảng 38,85% là quan sát trong tập seed đã khảo sát.

Có **16/40 lượt** khác epoch giữa cực đại mask AP và fitness box+mask chọn `best.pt`. Không gọi bảng max-mask là kết quả đánh giá lại checkpoint. Kiểm toán đã tái đánh giá 40 `best.pt` theo giao thức riêng, gắn hash, và không thấy sai lệch mask AP vượt 0,005 so với dòng fitness; một số P/R của Baseline không tái tạo chính xác. Chi tiết nằm trong báo cáo kiểm toán, không thay endpoint chính.

## Giới hạn bắt buộc

- Không suy TN ảnh bằng `40 − FP` đối tượng; không dùng trường legacy để tính specificity.
- Không suy Dice, IoU pixel, topology hoặc hiệu quả lâm sàng từ AP/P/R đối tượng.
- Chưa có test ngoài hay ablation 20 seed đầy đủ; cùng validation được dùng chọn epoch.
- Nguồn phát hành hai danh sách split 880/120 chưa được chứng thực đủ để gán cho tác giả dataset.
- Tái tạo nhãn trên OpenCV 4.12.0 và NumPy 2.2.6 cho 999/1.000 tệp trùng từng ký tự; một đỉnh của một nhãn khác khoảng 3 pixel. Không tự sửa nhãn hiện hành.
- Chưa có báo cáo Turnitin và cấu hình trường; không kết luận đạt ngưỡng 30%. Mobile chưa được chạy trong kiểm toán.

## Tài liệu lịch sử

Bộ 10 seed, bộ 21 seed TSVM cũ và các bản thảo trong `Bao_cao/md viet bao cao/` được giữ để truy vết, không dùng mặc định để sinh lại Word hiện tại. Header lịch sử không biến nội dung sai cũ thành kết quả đã được xác nhận. [Snapshot các điểm vào trước sửa](historical/snapshots_20261026/README_SNAPSHOT.md) giữ nguyên văn các phiên bản cũ.

Các quy tắc làm việc và trình bày vẫn dùng khi phù hợp: [AI_WORK_OPTIMIZATION_RULE](AI_WORK_OPTIMIZATION_RULE.md), [nguyên tắc làm việc](nguyen-tac-lam-viec-dai.md), các hướng dẫn phong cách Word. Không dùng chúng để thay thế raw/config/code.
