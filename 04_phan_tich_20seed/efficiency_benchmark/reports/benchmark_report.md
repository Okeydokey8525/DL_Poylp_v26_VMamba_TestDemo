# Benchmark thực đo: YOLO26s-seg và TSVM FP32

Thiết bị: AMD Ryzen 7 250 w/ Radeon 780M Graphics; 8 lõi/16 luồng logic; RAM 15.31 GiB. Windows; Python 3.12.14, PyTorch 2.6.0+cpu, Ultralytics 8.4.103. CUDA khả dụng: False.

## Giao thức và ranh giới đo

- Hai checkpoint seed 0 đúng cặp thực nghiệm 20 seed; SHA-256 và đường dẫn trong raw/*_environment.json. Không sử dụng checkpoint TSVM cũ không có FP32.
- CPU, float32, autocast tắt, 4 intra-op threads, 1 inter-op thread; batch 1, đầu vào chính xác 1×3×640×640; rect=False; conf=0.25, IoU=0.7, max_det=300. Trạng thái float32 và hữu hạn được kiểm tra trước đo.
- Mỗi mô hình chạy trong tiến trình Python riêng; baseline trước, TSVM sau. Mỗi chế độ 20 lượt warmup và 100 lượt đo bằng perf_counter_ns; torch.inference_mode; nhật ký không in trong vòng đo.
- Forward only: tensor float32 đã letterbox/chuẩn hóa từ ảnh polyp đầu tiên, tái sử dụng cùng tensor cho 100 lượt; chỉ model.forward, không gồm tiền/hậu xử lý. Đo sau khởi tạo predictor và fusion chuẩn của Ultralytics (gộp Conv-BN và loại nhánh one2many khỏi đầu end-to-end).
- Predict pipeline: 20 ảnh validation cố định (10 polyp + 10 background theo tên sắp xếp), giải mã PIL RGB trước đo; lặp 5 chu kỳ. Bao gồm chuyển ảnh/letterbox/normalize, forward và hậu xử lý segmentation thật của Ultralytics. Không gồm đọc file, giải mã JPEG, HTTP, hàng đợi web, overlay, base64 hoặc trình duyệt.
- Các cột preprocess/inference/postprocess lấy từ result.speed thực tế, chỉ để mô tả thành phần. Chênh lệch với đồng hồ bao ngoài là chi phí pipeline còn lại; không gán tỷ lệ giả định cho backbone/head.
- Số tham số kiến trúc và bộ nhớ tham số float32 được đếm trước fusion. RSS là cực đại trong các mẫu RSS lấy ngoài vùng bấm giờ, không phải peak allocator hoặc riêng bộ nhớ mô hình. Hai quá trình nạp độc lập giúp hạn chế nhiễm từ mô hình trước nhưng cache/OS vẫn tác động.

## Kết quả

| Mô hình | Chế độ | Mean ± SD (ms) | P50 | P95 | P99 | ảnh/s nối tiếp |
|---|---|---:|---:|---:|---:|---:|
| YOLO26s-seg | forward_only | 269.56 ± 18.71 | 270.97 | 297.76 | 308.62 | 3.71 |
| YOLO26s-seg | predict_pipeline | 286.56 ± 20.09 | 286.82 | 319.22 | 326.73 | 3.49 |
| YOLO26s-TSVM-FP32-seg | forward_only | 577.36 ± 24.40 | 576.84 | 623.50 | 636.82 | 1.73 |
| YOLO26s-TSVM-FP32-seg | predict_pipeline | 567.86 ± 24.45 | 566.94 | 611.67 | 638.48 | 1.76 |

| Mô hình | Tham số (M) | File checkpoint (MiB) | Tham số FP32 (MiB) | RSS sampled (MiB) |
|---|---:|---:|---:|---:|
| YOLO26s-seg | 11.434463 | 22.27 | 43.62 | 511.97 |
| YOLO26s-TSVM-FP32-seg | 12.254688 | 47.37 | 46.75 | 545.60 |

## Diễn giải và giới hạn

- Không lấy hiệu mean của hai chế độ forward_only và predict_pipeline để suy ra chi phí tiền/hậu xử lý: forward dùng một tensor lặp lại, pipeline dùng 20 ảnh và chạy ở pha sau. Mean pipeline của TSVM nhỏ hơn forward khoảng 9.50 ms trong lần đo này; khác biệt có thể liên quan tới dữ liệu/cache/dao động thời gian; các thành phần pipeline phải đọc từ result.speed thực đo trong cùng lượt.
- TSVM tăng tham số 7.17%; latency forward gấp 2.14 lần, pipeline gấp 1.98 lần trong lần đo CPU này.
- File baseline lưu tensor huấn luyện dạng FP16, nhưng cả hai mô hình đã được chuyển sang FP32 khi suy luận. Do đó không suy ra lượng RAM float32 chỉ từ dung lượng file best.pt. Các tensor FP16 gốc không có nghĩa benchmark dùng FP16.
- Không báo GFLOPs tổng vì chưa có quy tắc đếm được kiểm chứng cho custom parallel selective scan; số THOP chỉ đếm Conv/Linear sẽ thiếu phép toán. Không sao chép GFLOPs của TSVM cũ. VRAM: không áp dụng trong phiên CPU, không phải 0 MiB GPU.
- Đây là đo triển khai trên một máy, một seed, một thứ tự chạy; 100 lượt timing không phải 100 seed hoặc 100 mẫu độc lập để kiểm định ưu thế mô hình. OS, điện năng/nhiệt, nền Python và tác vụ khác có thể làm thay đổi độ trễ. Không suy rộng sang GPU hoặc hệ thống nội soi thời gian thực.
- Cột độ chính xác trong accuracy_efficiency_summary.csv dùng mean ± SD của 20 seed tại epoch cực đại mask AP, còn benchmark dùng seed-0 best.pt được chọn bởi box+mask fitness. Hai đại lượng giúp thảo luận đánh đổi tổng quát; không khẳng định AP cụ thể của checkpoint đo tốc độ hay Pareto có ý nghĩa thống kê.
- Không huấn luyện, không chỉnh checkpoint, không dùng ảnh validation để tối ưu tham số. Giải mã và các kiểm tra tensor/RSS nằm ngoài ranh giới bấm giờ.

## Tái lập

Chạy hai tiến trình measure.py baseline và measure.py tsvm bằng venv ai-service, lần lượt; chạy verify_checkpoints.py bằng cùng venv để kiểm tra dtype lưu trữ, sau đó chạy summarize.py bằng bundled Python với numpy/matplotlib. Bản sao scripts nằm trong scripts/. Kiểm tra hash môi trường trước khi so sánh lại. Mọi mốc thời gian gốc được lưu trong raw/.