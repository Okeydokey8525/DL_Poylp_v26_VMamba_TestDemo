# 01. Đề tài và phạm vi

## Đề tài

**Nghiên cứu phương pháp tích hợp VMamba vào YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng.**

Bài toán là phân đoạn thực thể (instance segmentation) một lớp `polyp`: với mỗi ảnh nội soi, mô hình trả về hộp bao và mặt nạ cho từng polyp. Ảnh không có polyp (ảnh nền) phải không có dự đoán.

## Hai mô hình được so sánh

| Vai trò | Mô hình | Khác biệt duy nhất |
|---|---|---|
| Đối chứng (Baseline) | YOLO26s-seg gốc của Ultralytics 8.4.127 | Tầng 10 là `C2PSA` |
| Đề xuất | YOLO26s-seg + TSVM FP32 | Tầng 10 thay bằng `C2TSVMamba` (Topology-Shape-aware VMamba) |

Hai mô hình dùng chung toàn bộ phần còn lại: backbone tầng 0–9, neck, đầu `Segment26`, dữ liệu, siêu tham số và 20 seed. Chi tiết ở [03](03_KIEN_TRUC_BASELINE.md), [04](04_KIEN_TRUC_TSVM_FP32.md), [05](05_CAU_HINH_HUAN_LUYEN.md).

"FP32" trong tên mô hình đề xuất nghĩa là **checkpoint được lưu ở float32**. Lý do và bằng chứng nằm ở [05](05_CAU_HINH_HUAN_LUYEN.md#vì-sao-gọi-là-tsvm-fp32).

## Câu hỏi nghiên cứu

1. Thay `C2PSA` ở tầng 10 (mức P5, bản đồ 20×20) bằng một khối VMamba có nhánh hình dạng và hướng thì độ chính xác mặt nạ có tăng không?
2. Mức thay đổi đó có ổn định qua nhiều seed huấn luyện không?
3. Đổi lại thì tốn thêm bao nhiêu tham số và thời gian suy luận?

## Thiết kế thực nghiệm

- Dữ liệu: Kvasir-SEG mở rộng thêm 200 ảnh nền normal-cecum, gọi là **BG20** ([02](02_DU_LIEU_BG20.md)).
- 2 mô hình × **20 seed (0–19)** × 100 epoch, tổng **40 lượt** huấn luyện trên Kaggle.
- So sánh **ghép cặp theo seed**. Chỉ số chính (endpoint) là **mask mAP50–95** trên tập validation ([06](06_KET_QUA_20_SEED.md)).

## Trong phạm vi bộ tài liệu này

- Dữ liệu BG20, kiến trúc hai mô hình, cấu hình huấn luyện.
- Kết quả 20 seed, hội tụ, ma trận nhầm lẫn, chi phí tính toán.
- Giới hạn và hướng phát triển.

## Ngoài phạm vi

| Nội dung | Lý do |
|---|---|
| AV, AVF, ITSVM (`99_luu_tru/thu_nghiem_ket_hop/`) | Thử nghiệm các dạng kết hợp khác, **không đưa vào báo cáo** |
| Baseline seed 20–22, TSVM cũ (checkpoint FP16, 21 seed), bộ 10 seed cũ | Lịch sử, không thuộc bộ chính |
| PraNet, U-Net | Chỉ dùng để so sánh chỉ số. Hiện chưa có số liệu ([10](10_SO_SANH_PRANET_UNET.md)) |
| Ứng dụng PolypVision (Web/Mobile) | Không thuộc phần mô hình. Bộ tài liệu này không mô tả ứng dụng |
