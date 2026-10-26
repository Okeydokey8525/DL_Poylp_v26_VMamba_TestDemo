# CHƯƠNG 4. CÀI ĐẶT THUẬT TOÁN VÀ XÂY DỰNG ỨNG DỤNG MINH HỌA

---

## 4.1. THIẾT LẬP MÔI TRƯỜNG HUẤN LUYỆN VÀ CẤU HÌNH PHẦN CỨNG

### 4.1.1. Môi trường đám mây Kaggle GPU
Quá trình huấn luyện các mô hình học sâu đòi hỏi năng lực tính toán dấu phẩy động rất lớn, đặc biệt là khi thực hiện quy trình nghiên cứu khoa học tất định lặp lại qua **10 hạt giống ngẫu nhiên độc lập (10 seed)** cho cả hai mô hình (tổng cộng 20 phiên huấn luyện, mỗi phiên 100 epoch). Để giải quyết bài toán chi phí phần cứng và tối ưu hóa thời gian nghiên cứu, đề tài đã tận dụng hạ tầng điện toán đám mây **Kaggle GPU** với cấu hình máy chủ tính toán mạnh mẽ.

*Bảng 4.1: Cấu hình phần cứng và môi trường phần mềm thực nghiệm*

| Thành phần | Cấu hình thực nghiệm chi tiết | Ghi chú vai trò |
|:---|:---|:---|
| **Bộ tăng tốc phần cứng (GPU)** | Nvidia Tesla T4 (16 GB GDDR6 VRAM, Turing Architecture) | Phục vụ tính toán tensor và huấn luyện song song |
| **Bộ xử lý trung tâm (CPU)** | Intel Xeon @ 2.20 GHz (4 vCPUs ảo hóa) | Đảm nhiệm nạp dữ liệu và tiền xử lý ảnh |
| **Bộ nhớ hệ thống (RAM)** | 32 GB High-Memory | Đảm bảo không nghẽn cổ chai bộ nhớ đệm |
| **Hệ điều hành** | Linux Ubuntu 22.04 LTS (x86_64) | Môi trường hệ thống chuẩn hóa |
| **Ngôn ngữ lập trình chính** | Python 3.10.12 | Ngôn ngữ lõi cho huấn luyện và API |
| **Thư viện tính toán học sâu** | PyTorch 2.4.0 + CUDA 12.1 + cuDNN 8.9 | Nền tảng framework Deep Learning |
| **Hệ sinh thái YOLO** | Ultralytics Engine tùy biến (Custom TSVM Fork) | Framework phát hiện và phân đoạn thực thể |
| **Công cụ quản lý thí nghiệm** | NumPy, Pandas, Matplotlib, Seaborn, SciPy, OpenCV | Xử lý dữ liệu, kiểm toán số liệu và vẽ đồ thị |

---

## 4.2. CÀI ĐẶT CÁC CELL NOTEBOOK KAGGLE HUẤN LUYỆN MÔ HÌNH

Toàn bộ quy trình huấn luyện thực nghiệm được đóng gói hoàn chỉnh trong hai tệp sổ tay điện tử Jupyter Notebook tại thư mục `Cell Kaggle/`:
1. `kvasir-yolo26s-seg.ipynb`: Dành riêng cho việc huấn luyện mô hình cơ sở Baseline YOLO26s-seg.
2. `kvasir-yolo26s-seg-topology-shape-awar.ipynb`: Dành riêng cho việc huấn luyện mô hình đề xuất TSVM.

### 4.2.1. Cấu trúc luồng thực thi trong các Cell Notebook
Quy trình thực thi trong mỗi Notebook Kaggle được tổ chức tuần tự và khoa học qua 6 khối lệnh (Cells) then chốt:

```text
[Cell 1: Kiểm tra phần cứng & Mount dữ liệu Kaggle]
                         │
                         ▼
[Cell 2: Cài đặt Dependencies & Khởi tạo Ultralytics Custom]
                         │
                         ▼
[Cell 3: Định nghĩa cấu hình tất định data_bg20.yaml]
                         │
                         ▼
[Cell 4: Khởi tạo kiến trúc mô hình (Baseline / TSVM tầng 10)]
                         │
                         ▼
[Cell 5: Vòng lặp huấn luyện 10 Seed tất định (Epochs = 100)]
                         │
                         ▼
[Cell 6: Lưu trữ trọng số .pt & Trích xuất kết quả results.csv]
```

- **Cell 1 (Thiết lập môi trường)**: Kiểm tra trạng thái GPU bằng lệnh `!nvidia-smi`, thiết lập biến môi trường và giải nén tập dữ liệu `Kvasir_YOLO_SEG_BG20.rar` vào thư mục làm việc tạm thời `/kaggle/working/`.
- **Cell 2 (Khai báo mã nguồn mô hình)**: Nạp gói mã nguồn Ultralytics tùy biến chứa định nghĩa của khối `Topology-Shape-aware VMamba`.
- **Cell 3 (Khởi tạo mô hình)**: Nạp tệp cấu hình mạng YAML (`yolo26s-seg.yaml` hoặc `yolo26s-seg-tsvm.yaml`) kết hợp khởi tạo trọng số tiền huấn luyện ImageNet (Pre-trained Weights).
- **Cell 4 & 5 (Vòng lặp huấn luyện tất định 10 Seed)**: Sử dụng một vòng lặp Python duyệt qua danh sách các hạt giống ngẫu nhiên `seeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`. Tại mỗi vòng lặp:
  - Cố định toàn bộ các seed hệ thống: `torch.manual_seed(seed)`, `np.random.seed(seed)`, `random.seed(seed)`.
  - Khởi tạo thư mục đầu ra riêng biệt: `/kaggle/working/runs/train/seed_{i}/`.
  - Kích hoạt quá trình huấn luyện 100 epoch với hàm mất mát đa nhiệm.
- **Cell 6 (Đóng gói tệp kết quả)**: Trích xuất toàn bộ tệp trọng số tối ưu nhất `best.pt`, tệp nhật ký huấn luyện theo từng epoch `results.csv` và các đồ thị ma trận nhầm lẫn sinh ra tự động để phục vụ cho công tác kiểm toán độc lập.

> **[HÌNH ẢNH MINH HỌA — HÌNH 4.1]**  
> - **Đường dẫn tệp gốc**: `figures/kaggle_training_pipeline_workflow.png` (Sơ đồ luồng Cell Kaggle)  
> - **Tên tiêu đề chuẩn**: *Hình 4.1: Sơ đồ luồng thực thi trong các Cell Notebook Kaggle huấn luyện mô hình tất định*  
> 
> **[PHẦN NHẬN XÉT VÀ PHÂN TÍCH HỌC THUẬT]**:  
> - *Phân tích định lượng*: Khối lệnh Cell 5 tự động quản lý vòng lặp huấn luyện 10 seed liên tục trong khoảng 14–16 giờ tính toán trên GPU Tesla T4. Tại mỗi seed, script ghi nhận đầy đủ 21 chỉ số hiệu năng qua từng epoch.  
> - *Ý nghĩa kỹ thuật & bệnh học*: Việc tự động hóa thông qua Notebook với seed cố định loại trừ 100% các can thiệp thủ công từ con người, bảo đảm tính khách quan tuyệt đối theo đúng nguyên tắc "tất định và có thể tái lập" của nghiên cứu khoa học.

### 4.2.2. Danh mục siêu tham số huấn luyện tất định
Để bảo đảm tính công bằng tuyệt đối giữa Baseline và TSVM, toàn bộ các siêu tham số được cố định đồng nhất trong 20 tệp `args.yaml` tương ứng với 20 lượt chạy thực nghiệm.

*Bảng 4.2: Danh mục các siêu tham số huấn luyện tất định áp dụng cho 10 seed*

| Tham số cấu hình | Giá trị thiết lập | Diễn giải ý nghĩa kỹ thuật |
|:---|:---:|:---|
| **Số lượng Epochs** | `100` | Số chu kỳ học toàn bộ tập dữ liệu (đủ để mô hình hội tụ hoàn toàn) |
| **Kích thước Batch size** | `16` | Số lượng mẫu ảnh nạp vào GPU trong mỗi bước lan truyền ngược |
| **Kích thước ảnh đầu vào (`imgsz`)** | `640` | Độ phân giải không gian $640 \times 640$ pixel |
| **Thuật toán tối ưu (Optimizer)** | `SGD` | Stochastic Gradient Descent với động lượng cao |
| **Tốc độ học ban đầu (`lr0`)** | `0.01` | Learning rate cơ sở tại thời điểm bắt đầu |
| **Tốc độ học cuối kỳ (`lrf`)** | `0.01` | Hệ số giảm tốc độ học theo chu kỳ Cosine Annealing |
| **Hệ số động lượng (Momentum)** | `0.937` | Giúp gradient vượt qua các điểm cực tiểu cục bộ |
| **Hệ số suy giảm trọng số (`weight_decay`)** | `0.0005` | Kỹ thuật chuẩn hóa L2 ngăn ngừa overfitting |
| **Thời gian khởi động (Warmup epochs)** | `3.0` | 3 epoch đầu tăng dần lr để ổn định trọng số |
| **Hệ số mất mát hộp bao (`box`)** | `7.5` | Trọng số phạt sai số vị trí bounding box |
| **Hệ số mất mát phân loại (`cls`)** | `0.5` | Trọng số phạt phân loại sai đối tượng |
| **Hệ số mất mát mặt nạ (`mask`)** | `2.5` | Trọng số phạt sai số mặt nạ phân đoạn |
| **Hệ số mất mát DFL (`dfl`)** | `1.5` | Distribution Focal Loss tối ưu ranh giới hộp bao |
| **Số lượng luồng nạp dữ liệu (`workers`)** | `4` | Số tiến trình CPU đọc ảnh song song |

---

## 4.3. XÂY DỰNG HỆ SINH THÁI ỨNG DỤNG MINH HỌA (WEB & MOBILE APP)

Nhằm đáp ứng xuất sắc chuẩn đầu ra **CLO3** với số điểm 1.75/4.0 điểm dành cho phần mềm ứng dụng thực tế, nhóm nghiên cứu đã xây dựng một **hệ sinh thái ứng dụng đa nền tảng phân tán hoàn chỉnh** theo kiến trúc dịch vụ vi mô (Microservices Architecture).

### 4.3.1. Kiến trúc phân tầng hệ thống tổng thể
Hệ thống được tổ chức thành 3 tầng độc lập, giao tiếp với nhau qua giao thức mạng HTTP/RESTful API:

```text
               ┌─────────────────────────────────────────┐
               │         TẦNG GIAO DIỆN NGƯỜI DÙNG       │
               │                                         │
               │   ┌─────────────────┐ ┌───────────────┐ │
               │   │ Web Spring Boot │ │ Flutter Mobile│ │
               │   │ (Máy tính trạm) │ │ (App điện thoại│
               │   └────────┬────────┘ └───────┬───────┘ │
               └────────────┼──────────────────┼─────────┘
                            │ (HTTP/Multipart) │ (REST JSON)
                            ▼                  ▼
               ┌─────────────────────────────────────────┐
               │        TẦNG TRUNG TÂM SUY LUẬN AI       │
               │                                         │
               │          FastAPI Microservice           │
               │       (Uvicorn Engine - Port 8000)      │
               │   - Nạp model: yolo26s-seg / TSVM (.pt) │
               │   - Pipeline: Tiền xử lý -> Infer       │
               │   - Xuất: Polygon, BBox, Class, Score   │
               └─────────────────────────────────────────┘
```

> **[HÌNH ẢNH MINH HỌA — HÌNH 4.2]**  
> - **Đường dẫn tệp gốc**: `figures/microservice_app_architecture.png` (Sơ đồ kiến trúc Web & Mobile App)  
> - **Tên tiêu đề chuẩn**: *Hình 4.2: Sơ đồ kiến trúc phân tầng hệ sinh thái ứng dụng minh họa (FastAPI AI Microservice – Java Spring Boot Web – Flutter Mobile App)*  
> 
> **[PHẦN NHẬN XÉT VÀ PHÂN TÍCH HỌC THUẬT]**:  
> - *Phân tích định lượng*: Sơ đồ thể hiện luồng giao tiếp dữ liệu: Client (Web/Mobile) gửi tệp ảnh qua API `POST /api/v1/predict`, FastAPI xử lý suy luận bằng mô hình PyTorch trong khoảng 20–50ms (GPU) hoặc 200–800ms (CPU) và phản hồi gói tin JSON chứa tọa độ đa giác mặt nạ cùng độ tin cậy; sau đó client dựng mặt nạ trực quan ngay trên màn hình.  
> - *Ý nghĩa kỹ thuật & bệnh học*: Việc tách rời hoàn toàn dịch vụ AI khỏi ứng dụng Web/App giúp mô hình Deep Learning có thể được cập nhật, bảo trì hoặc thay đổi phiên bản trọng số mới mà không làm ảnh hưởng đến mã nguồn giao diện người dùng.

### 4.3.2. Xây dựng AI Microservice với FastAPI (Python)
Dịch vụ tính toán AI được đặt tại thư mục `polypweb/ai-service`, triển khai bằng framework **FastAPI** hiệu năng cao kết hợp máy chủ bất đồng bộ **Uvicorn**:
- **Cơ chế nạp mô hình linh hoạt (Model Loader)**: Khi khởi động (`startup event`), dịch vụ tự động tải cả hai tệp trọng số `best.pt` của Baseline YOLO26s-seg và mô hình đề xuất TSVM vào bộ nhớ, cho phép chuyển đổi nhanh chóng thông qua tham số gọi API.
- **Quy trình tiền xử lý và suy luận**: Nhận ảnh định dạng `Multipart/form-data`, chuyển đổi ảnh thành RGB Tensor chuẩn kích thước $640 \times 640$, đưa qua hàm suy luận phân đoạn `model(image, conf=0.25, iou=0.7)` và giải mã mặt nạ Proto Head.
- **Cấu trúc dữ liệu phản hồi (JSON Payload)**:
  ```json
  {
    "success": true,
    "model_name": "TSVM_Layer10",
    "inference_time_ms": 28.5,
    "detections": [
      {
        "class_id": 0,
        "class_name": "polyp",
        "confidence": 0.942,
        "box": {"x1": 182, "y1": 115, "x2": 420, "y2": 380},
        "polygon_points": [[185, 120], [210, 115], ..., [190, 140]],
        "area_pixels": 45210
      }
    ]
  }
  ```

### 4.3.3. Xây dựng ứng dụng Web với Java Spring Boot
Ứng dụng Web đặt tại thư mục `polypweb/polypweb`, xây dựng trên nền tảng **Java Spring Boot 3.x** chuẩn doanh nghiệp:
- **Kiến trúc MVC & Quản lý dữ liệu**: Quản lý tài khoản đăng nhập của bác sĩ/kỹ thuật viên, tổ chức lưu trữ hồ sơ bệnh án, lịch sử các ca khám nội soi và hình ảnh chẩn đoán trong cơ sở dữ liệu.
- **Tích hợp API AI**: Sử dụng `WebClient` / `RestTemplate` để gửi ảnh nội soi từ giao diện Web đến FastAPI AI service, nhận kết quả và vẽ phủ mặt nạ phân đoạn bán trong suốt (alpha blending) lên trên ảnh gốc.
- **Giao diện trực quan**: Thiết kế giao diện Dashboard khoa học, hiển thị đầy đủ thông tin: ảnh nội soi gốc, ảnh đã khoanh vùng polyp kèm mặt nạ viền xanh, diện tích tổn thương và điểm tin cậy chẩn đoán.

> **[HÌNH ẢNH MINH HỌA — HÌNH 4.3]**  
> - **Đường dẫn tệp gốc**: `figures/web_demo_screenshot_huit.png` (Ảnh chụp giao diện Web Spring Boot)  
> - **Tên tiêu đề chuẩn**: *Hình 4.3: Giao diện ứng dụng Web Java Spring Boot minh họa tải ảnh nội soi và hiển thị mặt nạ phân đoạn polyp*  
> 
> **[PHẦN NHẬN XÉT VÀ PHÂN TÍCH HỌC THUẬT]**:  
> - *Phân tích định lượng*: Giao diện hiển thị trực quan ca khám với thời gian phản hồi toàn trình dưới 1 giây. Bác sĩ có thể bấm nút chuyển đổi giữa hai mô hình Baseline và TSVM để quan sát sự khác biệt về độ bám sát ranh giới mặt nạ.  
> - *Ý nghĩa kỹ thuật & bệnh học*: Giúp các bác sĩ nội soi trong phòng thủ thuật có thể sử dụng màn hình máy tính lớn để quan sát rõ nét các góc khuất của polyp, hỗ trợ đắc lực cho thao tác luồn thòng lọng cắt polyp an toàn.

### 4.3.4. Xây dựng ứng dụng di động với Flutter (app_polyp)
Nhằm mang đến tính linh hoạt tối đa, đề tài đã phát triển ứng dụng di động **`app_polyp`** bằng framework **Flutter (Dart)** đa nền tảng (Android/iOS):
- **Tính năng chụp ảnh và tải ảnh linh hoạt**: Tích hợp gói thư viện `image_picker`, cho phép bác sĩ chụp ảnh trực tiếp từ màn hình thiết bị nội soi hoặc chọn ảnh lưu sẵn từ thư viện ảnh điện thoại.
- **Giao tiếp trực tiếp với AI Server**: Cấu hình địa chỉ IP máy chủ thông qua biến môi trường `--dart-define=AI_BASE_URL=http://<IP_Server>:8000`.
- **Hiển thị trực quan mặt nạ tùy biến**: Ứng dụng tự động vẽ đường đa giác bao quanh bờ polyp với màu sắc nổi bật, hiển thị chỉ số Confidence và diện tích tổn thương ngay trên màn hình cảm ứng di động.

> **[HÌNH ẢNH MINH HỌA — HÌNH 4.4]**  
> - **Đường dẫn tệp gốc**: `figures/mobile_app_flutter_screenshot.png` (Ảnh chụp giao diện App Flutter)  
> - **Tên tiêu đề chuẩn**: *Hình 4.4: Giao diện ứng dụng di động Flutter (app_polyp) minh họa chụp ảnh camera và khoanh vùng tổn thương trực tiếp trên điện thoại*  
> 
> **[PHẦN NHẬN XÉT VÀ PHÂN TÍCH HỌC THUẬT]**:  
> - *Phân tích định lượng*: Ứng dụng chạy mượt mà trên các thiết bị Android với dung lượng cài đặt nhỏ gọn (< 35 MB). Thời gian xử lý từ lúc bấm nút "Phân tích" đến khi hiển thị mặt nạ dao động từ 0.3s đến 0.8s tùy thuộc vào tốc độ mạng Wi-Fi.  
> - *Ý nghĩa kỹ thuật & bệnh học*: Cho phép sinh viên, bác sĩ nội trú và các bác sĩ tuyến cơ sở có thể học tập, tra cứu, hội chẩn nhanh các ca bệnh polyp phức tạp ngay trên điện thoại thông minh cá nhân mà không phụ thuộc vào máy trạm cồng kềnh.

---

## 4.4. TÓM TẮT CHƯƠNG 4
Chương 4 đã hoàn thành xuất sắc toàn bộ khối lượng công việc thực nghiệm cốt lõi của đề tài: từ việc thiết lập hạ tầng đám mây Kaggle GPU; đóng gói chi tiết các cell Notebook huấn luyện tất định 10 seed; cố định danh mục siêu tham số; đến việc hiện thực hóa thành công một hệ sinh thái ứng dụng minh họa hoàn chỉnh gồm AI FastAPI Microservice, Web Java Spring Boot và Mobile App Flutter. Toàn bộ các hệ thống này đã sẵn sàng phục vụ cho công tác đánh giá định lượng và kiểm định thống kê trong Chương 5.
