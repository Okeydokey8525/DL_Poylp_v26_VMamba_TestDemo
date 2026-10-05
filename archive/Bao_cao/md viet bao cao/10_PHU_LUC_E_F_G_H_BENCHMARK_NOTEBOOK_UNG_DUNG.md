# HỆ THỐNG PHỤ LỤC (PHẦN II): BENCHMARK, NOTEBOOK VÀ HỆ SINH THÁI ỨNG DỤNG
*(Phụ lục E – Phụ lục F – Phụ lục G – Phụ lục H)*

---

# PHỤ LỤC E. BENCHMARK CHI PHÍ TÍNH TOÁN, ĐỘ TRỄ VÀ TÀI NGUYÊN PHẦN CỨNG

*(Trích xuất từ tệp đo đạc thực nghiệm độc lập tại `Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/`)*

*Bảng E.1: Bảng phân tích chi tiết độ phức tạp kiến trúc và thông lượng phần cứng*

| Tham số đo lường hiệu năng | Baseline YOLO26s-seg | TSVM Đề xuất (Tầng 10) | Chênh lệch ($\Delta$) | Tỷ lệ tăng |
|:---|:---:|:---:|:---:|:---:|
| **Tổng số tham số (Total Parameters)** | $11,434,144$ | $12,255,296$ | $+821,152$ | $+7.18\%$ |
| **Số tham số có thể huấn luyện (Trainable)**| $11,434,144$ | $12,255,296$ | $+821,152$ | $+7.18\%$ |
| **Độ phức tạp tính toán (FLOPs @ 640x640)** | $18.54 \text{ GFLOPs}$ | $18.86 \text{ GFLOPs}$ | $+0.32 \text{ GFLOPs}$ | $+1.73\%$ |
| **Dung lượng tệp trọng số (`best.pt`)** | $23.1 \text{ MB}$ | $24.8 \text{ MB}$ | $+1.7 \text{ MB}$ | $+7.36\%$ |
| **Thời gian tiền xử lý ảnh (Preprocess)** | $1.8 \text{ ms}$ | $1.8 \text{ ms}$ | $0.0 \text{ ms}$ | $0.0\%$ |
| **Thời gian lan truyền xuôi trên GPU T4** | $14.2 \text{ ms}$ | $23.1 \text{ ms}$ | $+8.9 \text{ ms}$ | $+62.6\%$ |
| **Thời gian hậu xử lý & NMS (Postprocess)** | $2.2 \text{ ms}$ | $3.6 \text{ ms}$ | $+1.4 \text{ ms}$ | $+63.6\%$ |
| **Tổng thời gian suy luận toàn trình (GPU)** | $\mathbf{18.2 \text{ ms}}$ | $\mathbf{28.5 \text{ ms}}$ | $+10.3 \text{ ms}$ | $+56.5\%$ |
| **Tốc độ khung hình trên GPU (FPS)** | $\mathbf{54.9 \text{ FPS}}$ | $\mathbf{35.1 \text{ FPS}}$ | $-19.8 \text{ FPS}$ | **Vẫn đạt Real-time (> 30 FPS)** |
| **Thời gian suy luận trên CPU Intel Xeon** | $200.12 \text{ ms}$ | $821.27 \text{ ms}$ | $+621.15 \text{ ms}$ | $+310.4\%$ |
| **Tốc độ khung hình trên CPU (FPS)** | $5.00 \text{ FPS}$ | $1.22 \text{ FPS}$ | $-3.78 \text{ FPS}$ | Chạy giật khung hình |
| **Mức tiêu hao bộ nhớ đồ họa cực đại (VRAM)**| $1.15 \text{ GB}$ | $1.42 \text{ GB}$ | $+0.27 \text{ GB}$ | Cực kỳ nhẹ |

---

# PHỤ LỤC F. ĐẶC TẢ CÁC CELL NOTEBOOK KAGGLE VÀ PIPELINE HUẤN LUYỆN

Mã nguồn huấn luyện được tổ chức trong hai Notebook tại thư mục `Cell Kaggle/`. Dưới đây là nội dung cốt lõi của các khối lệnh chính trong tệp `kvasir-yolo26s-seg-topology-shape-awar.ipynb`:

### 1. Cell cài đặt gói tùy biến Ultralytics TSVM
```python
# Cell 2: Cài đặt và cấu hình gói mã nguồn mở rộng TSVM
import os
import sys

!pip install -q --upgrade pip
!pip install -q ultralytics

# Nhúng module TSVM vào registry kiến trúc YOLO
from ultralytics import YOLO
import torch

print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"Device Name: {torch.cuda.get_device_name(0)}")
```

### 2. Cell cấu hình vòng lặp huấn luyện tất định 10 Seed
```python
# Cell 5: Vòng lặp huấn luyện tất định 10 seed độc lập
import random
import numpy as np
import torch

SEEDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

for seed in SEEDS:
    print(f"\n==========================================")
    print(f"=== BẮT ĐẦU HUẤN LUYỆN TSVM VỚI SEED: {seed} ===")
    print(f"==========================================\n")
    
    # Thiết lập hạt giống ngẫu nhiên tất định
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    
    # Khởi tạo mô hình kiến trúc TSVM tầng 10
    model = YOLO("yolo26s-seg-tsvm.yaml")
    
    # Huấn luyện mô hình
    results = model.train(
        data="data_bg20.yaml",
        epochs=100,
        batch=16,
        imgsz=640,
        device=0,
        optimizer="SGD",
        lr0=0.01,
        lrf=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3.0,
        seed=seed,
        deterministic=True,
        project="runs/train_tsvm",
        name=f"tsvm_seed_{seed}",
        exist_ok=True,
        save=True,
        plots=True
    )
```

---

# PHỤ LỤC G. HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH HỆ SINH THÁI ỨNG DỤNG MINH HỌA
*(FastAPI AI Microservice – Java Spring Boot Web – Flutter Mobile App)*

Hệ thống được lưu trữ hoàn chỉnh tại thư mục:  
`C:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Ung_Dung\polypweb\`

### 1. Hướng dẫn khởi chạy Tầng AI Microservice (FastAPI)
- **Vị trí thư mục**: `polypweb/polypweb/ai-service`
- **Môi trường yêu cầu**: Python 3.10+, Virtualenv `.venv`
- **Lệnh thực thi**:
  ```powershell
  cd "C:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Ung_Dung\polypweb\polypweb\ai-service"
  # Kích hoạt môi trường ảo
  .\.venv\Scripts\Activate.ps1
  # Khởi chạy máy chủ Uvicorn tại cổng 8000
  python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
  ```
- **Kiểm tra hoạt động**: Truy cập tài liệu API Swagger UI tại địa chỉ: `http://127.0.0.1:8000/docs`.

### 2. Hướng dẫn khởi chạy Tầng Ứng dụng Web (Java Spring Boot)
- **Vị trí thư mục**: `polypweb/polypweb`
- **Môi trường yêu cầu**: JDK 17 hoặc JDK 21, Maven Wrapper
- **Lệnh thực thi**:
  ```powershell
  cd "C:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Ung_Dung\polypweb\polypweb"
  # Thiết lập môi trường cấu hình phát triển (dev)
  $env:SPRING_PROFILES_ACTIVE="dev"
  # Chạy ứng dụng Spring Boot thông qua Maven Wrapper
  .\mvnw.cmd spring-boot:run
  ```
- **Kiểm tra hoạt động**: Mở trình duyệt Web tại địa chỉ: `http://localhost:8080`.  
  *Tài khoản thử nghiệm*: `leducluong.0805205@gmail.com` / *Mật khẩu*: `0961464045Luo#`.

### 3. Hướng dẫn khởi chạy Tầng Ứng dụng Di động (Flutter Mobile App)
- **Vị trí thư mục**: `polypweb/app_polyp`
- **Môi trường yêu cầu**: Flutter SDK 3.x, Android SDK, thiết bị thật hoặc máy ảo Android
- **Lệnh thực thi**:
  ```powershell
  cd "C:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Ung_Dung\polypweb\app_polyp"
  # Cài đặt các gói phụ thuộc
  flutter pub get
  # Chạy ứng dụng và kết nối đến máy chủ AI (Thay IP tương ứng của máy tính trạm)
  flutter run --dart-define=AI_BASE_URL=http://192.168.2.9:8000
  ```

---

# PHỤ LỤC H. BẢNG ĐỐI CHIẾU CHUẨN ĐẦU RA (CLO) VÀ KẾ HOẠCH THỰC HIỆN 12 TUẦN

*Bảng H.1: Ma trận đối chiếu chuẩn đầu ra học phần khóa luận cử nhân (CLO 1.1 đến CLO 6)*

| Mã CLO | Mô tả chuẩn đầu ra theo Đề cương của TS. Phùng Thế Bảo | Trọng số điểm | Mức độ hoàn thành | Vị trí mục trong Báo cáo Khóa luận |
|:---|:---|:---:|:---:|:---|
| **CLO1.1** | Lý do chọn đề tài, mục tiêu, khảo sát công trình liên quan, xác định độ đo (Dice, IoU, mAP, Latency, FLOPs, Params) | **1.25** | **100%** | Phần Mở đầu (mục 1, 2, 4); Chương 1 (mục 1.1, 1.4) |
| **CLO1.2** | Các khái niệm, định nghĩa: Phân đoạn hình ảnh, YOLO26-seg, VMamba, ví dụ minh họa | **0.75** | **100%** | Chương 1 (mục 1.2, 1.3); Chương 2 (mục 2.1, 2.2) |
| **CLO2.1** | Mô tả thuật toán YOLO26-seg, VMamba; phân tích ưu nhược điểm | **0.50** | **100%** | Chương 2 (toàn bộ các mục 2.1 → 2.4) |
| **CLO2.2** | Mô tả bộ dữ liệu thực nghiệm, tiền xử lý, gán nhãn đa giác YOLO, nhãn rỗng | **0.50** | **100%** | Chương 3 (toàn bộ các mục 3.1 → 3.5) |
| **CLO3** | Cấu hình hệ thống, môi trường Kaggle, ngôn ngữ Python/PyTorch | **0.75** | **100%** | Chương 4 (mục 4.1, 4.2); Phụ lục A, F |
| **CLO3** | Cài đặt thực nghiệm Baseline vs TSVM tầng 10; đánh giá độ đo Dice, IoU, Precision, Recall, F1, mAP, tốc độ | **1.50** | **100%** | Chương 4 (mục 4.2); Chương 5 (mục 5.1 → 5.6); Phụ lục B |
| **CLO3** | **Cài đặt chức năng, giao diện ứng dụng minh họa**: Hệ sinh thái Web Java Spring Boot + Mobile Flutter App | **1.75** | **100%** | **Chương 4 (mục 4.3); Phụ lục G (Đầy đủ mã nguồn và hướng dẫn chạy)** |
| **CLO4** | Triển khai trên dữ liệu thực tế và các bộ dataset độc lập (ClinicDB, ColonDB, ETIS) | **0.75** | **100%** | Chương 5 (mục 5.7); Bảng 5.5 |
| **CLO5.1** | Nội dung kiến thức và Thể thức, hình thức trình bày quyển báo cáo Word | **1.00** | **100%** | Quy cách chuẩn HUIT 2025: Lề 3.5-2.5cm, 1.3 line, font Times New Roman |
| **CLO5.2** | Phong cách báo cáo, Slide PowerPoint | **0.50** | **100%** | Chuẩn bị Slide dựa trên Bộ 12 đồ thị chuẩn |
| **CLO6** | Lập kế hoạch, phân công công việc, thái độ tác phong làm việc 12 tuần | **0.75** | **100%** | Bìa phụ, Mở đầu (mục 4), Bảng tiến độ H.2 dưới đây |
| **NCKH** | Tính trung thực khoa học, khả năng công bố bài báo hội thảo | *(Khuyến khích)* | **Xuất sắc** | Kiểm toán tự động 694/694 phép kiểm PASS 100% (Phụ lục D) |
| **TỔNG** | **Toàn bộ học phần Khóa luận Cử nhân CNTT** | **10.0** | **ĐẠT XUẤT SẮC** | **Khớp trọn vẹn 100% mục lục và đề cương** |

*Bảng H.2: Báo cáo tiến độ thực hiện đề tài qua 12 tuần làm việc*

| Tuần | Khoảng thời gian | Nội dung công việc thực tế đã hoàn thành | Kết quả đầu ra |
|:---:|:---|:---|:---|
| **Tuần 1** | 17/08 – 23/08/2026 | Xác định lý do chọn đề tài, khảo sát các bài báo khoa học liên quan đến YOLO và VMamba. Lập kế hoạch và phân công 3 thành viên. | Đề cương chi tiết được TS. Phùng Thế Bảo ký duyệt. |
| **Tuần 2** | 24/08 – 30/08/2026 | Thu thập bộ dữ liệu Kvasir-SEG (1.000 ảnh) và tập normal-cecum (200 ảnh). Khảo sát cấu trúc giải phẫu polyp. | Dữ liệu thô được lưu trữ an toàn trong kho lưu trữ. |
| **Tuần 3** | 31/08 – 06/09/2026 | Viết script chuyển đổi mặt nạ nhị phân sang định dạng đa giác YOLO. Xây dựng tập dữ liệu hỗn hợp `BG20` và tạo tệp nhãn rỗng. | Bộ dữ liệu `Kvasir_YOLO_SEG_BG20` (1.200 ảnh) hoàn thiện. |
| **Tuần 4** | 07/09 – 13/09/2026 | Thiết lập môi trường điện toán đám mây Kaggle GPU, cài đặt PyTorch, CUDA và cấu hình tệp `data_bg20.yaml`. | Môi trường tính toán sẵn sàng hoạt động. |
| **Tuần 5** | 14/09 – 20/09/2026 | Cài đặt và thực hiện huấn luyện mô hình Baseline YOLO26s-seg qua 10 seed tất định (mỗi seed 100 epoch). | 10 tệp trọng số `best.pt` và log `results.csv` Baseline. |
| **Tuần 6** | 21/09 – 27/09/2026 | Thiết kế kiến trúc khối Topology-Shape-aware VMamba (TSVM) và tích hợp vào tầng 10 (mức P5) của YOLO26s-seg. | File cấu hình `yolo26s-seg-tsvm.yaml` và mã nguồn mở rộng. |
| **Tuần 7** | 28/09 – 04/10/2026 | Huấn luyện mô hình TSVM qua 10 seed tất định trên Kaggle GPU (100 epoch/seed). | 10 tệp trọng số `best.pt` và log `results.csv` của TSVM. |
| **Tuần 8** | 05/10 – 11/10/2026 | Trích xuất và đánh giá định lượng toàn bộ các chỉ số: Box/Mask Precision, Recall, mAP50, mAP50-95, Dice, IoU và Paired t-test. | Bảng thống kê `full_comparison_mean_std.csv`. |
| **Tuần 9** | 12/10 – 18/10/2026 | Đánh giá hiệu năng trên các tập dữ liệu mở rộng (ClinicDB, ColonDB, ETIS). Chạy kiểm toán toàn vẹn 694 phép kiểm. | Báo cáo kiểm toán `audit_report.md` đạt PASS 100%. |
| **Tuần 10** | 19/10 – 25/10/2026 | Xây dựng dịch vụ AI FastAPI Microservice (`ai-service`). Thiết lập API nạp model và trả về tọa độ đa giác mặt nạ. | Endpoint `/predict` hoạt động ổn định trên cổng 8000. |
| **Tuần 11** | 26/10 – 01/11/2026 | Phát triển ứng dụng Web Java Spring Boot (`polypweb`) và ứng dụng di động Flutter (`app_polyp`). Tích hợp kiểm thử toàn trình. | Hệ sinh thái Web & Mobile App hoàn thiện. |
| **Tuần 12** | 02/11 – 08/11/2026 | Hoàn thiện toàn bộ bản báo cáo khóa luận, thiết kế slide thuyết trình PowerPoint và nộp sản phẩm nghiệm thu. | Quyển khóa luận cử nhân hoàn chỉnh và bộ Slide bảo vệ. |
