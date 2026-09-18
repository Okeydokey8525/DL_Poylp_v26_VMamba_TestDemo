# KẾT QUẢ THỰC NGHIỆM CHI TIẾT: CHI PHÍ TÍNH TOÁN, ĐỘ TRỄ VÀ KHẢ NĂNG TRIỂN KHAI THỜI GIAN THỰC
## PHÂN TÍCH THAM SỐ (PARAMS), KHỐI LƯỢNG TÍNH TOÁN (GFLOPS), ĐỘ TRỄ 3 PHA VÀ TỐC ĐỘ KHUNG HÌNH (FPS)

---

> **Phân loại độ tin cậy thông tin theo nguyên tắc dự án:**
> - `[Đã xác nhận]`: Dữ liệu tham số (Params), GFLOPs, kích thước tệp trọng số `best.pt`, mức chiếm dụng VRAM và độ trễ thực nghiệm trên GPU Kaggle Tesla T4.
> - `[Có khả năng / suy luận]`: Tiềm năng đóng gói TensorRT FP16/INT8 triển khai thực địa trên máy tính nhúng phòng mổ (NVIDIA Jetson Orin Nano/AGX).

---

## 1. BẢNG ĐỐI CHIẾU CHI PHÍ TÍNH TOÁN VÀ DUNG LƯỢNG MÔ HÌNH (3 MÔ HÌNH)

| Tiêu chí phần cứng & tính toán | Baseline YOLO26s-seg | C2TSVMamba | C2IAVM (👑 Champion Model) | Đánh giá tính khả thi triển khai |
| :--- | :---: | :---: | :---: | :--- |
| **Số lượng tham số (Parameters)** | **$11.77\text{ M}$** | $12.35\text{ M}$ ($+4.9\%$) | **$12.14\text{ M}$ ($+3.1\%$)** | Cực kỳ gọn nhẹ, chỉ tăng nhẹ $0.37\text{ M}$ |
| **Khối lượng tính toán (GFLOPs)** | **$39.4\text{ GFLOPs}$** | $41.2\text{ GFLOPs}$ ($+4.6\%$) | **$40.8\text{ GFLOPs}$ ($+3.5\%$)** | Tính toán tuyến tính, không bùng nổ bậc 2 |
| **Kích thước trọng số (`best.pt`)** | **$22.7\text{ MB}$** | $24.8\text{ MB}$ | **$24.3\text{ MB}$** | Cực kỳ nhỏ gọn, dễ nạp vào bộ nhớ nhúng |
| **Thời gian huấn luyện 100 Epochs** | **$1.91\text{ giờ}$** | $3.92\text{ giờ}$ ($2.05\times$) | **$3.05\text{ giờ}$ ($1.60\times$)** | C2IAVM nhanh hơn TSVM gần 1 giờ/lần train |
| **Mức đỉnh VRAM huấn luyện (Batch 16)**| **$6.42\text{ GB}$** | $7.35\text{ GB}$ | **$7.19\text{ GB}$** | Huấn luyện hoàn toàn miễn phí trên Kaggle T4 ($<8\text{ GB}$) |

`[Đã xác nhận]`

---

## 2. PHÂN BỔ ĐỘ TRỄ 3 PHA VÀ TỐC ĐỘ SUY LUẬN KHUNG HÌNH (FPS)

Chuẩn camera nội soi tiêu hóa lâm sàng hiện hành yêu cầu tần số quét tối thiểu **$25 - 30\text{ FPS}$** (tương đương độ trễ tối đa $< 33.3\text{ ms}$ cho mỗi khung hình):

| Pha đo lường độ trễ (Latency) | Baseline YOLO26s-seg | C2TSVMamba | C2IAVM (👑 Champion Model) | Ghi chú kỹ thuật |
| :--- | :---: | :---: | :---: | :--- |
| **Pha 1: Tiền xử lý (Pre-process)** | $1.8\text{ ms}$ | $2.6\text{ ms}$ | **$1.8\text{ ms}$** | Letterbox, chuyển đổi màu RGB, FP16 scaling |
| **Pha 2: Suy luận mô hình (Inference)** | $17.5\text{ ms}$ | $23.4\text{ ms}$ | **$20.9\text{ ms}$** | Lan truyền tiến qua Backbone, C2IAVM, Heads |
| **Pha 3: Hậu xử lý & NMS (Post-process)**| $2.2\text{ ms}$ | $2.5\text{ ms}$ | **$2.3\text{ ms}$** | NMS lọc khung, tạo mặt nạ nhị phân Prototype |
| **Tổng độ trễ mỗi khung hình (Total)** | **$21.5\text{ ms}$** | $28.5\text{ ms}$ | **$25.0\text{ ms}$** | **Vượt xa ngưỡng tối thiểu 33.3 ms** |
| **Tốc độ khung hình (FPS tương đương)** | **$46.5\text{ FPS}$** | $35.1\text{ FPS}$ | **$40.0\text{ FPS}$** | **Đạt chuẩn Video Thời Gian Thực (>30 FPS)** |

`[Đã xác nhận]`

---

## 3. CÁC HÌNH ẢNH MINH HỌA TRỰC QUAN ĐÃ KẾT XUẤT (300 DPI)

- Biểu đồ cột chi phí tài nguyên: `05c_computational_resources_barchart.png` (trong cả 2 thư mục `Base vs IAVM` và `Base vs Topolo`).
- Biểu đồ Donut phân rã độ trễ: `07c_pie_inference_latency_breakdown.png` (minh chứng tốc độ 40.0 FPS trên GPU T4).
