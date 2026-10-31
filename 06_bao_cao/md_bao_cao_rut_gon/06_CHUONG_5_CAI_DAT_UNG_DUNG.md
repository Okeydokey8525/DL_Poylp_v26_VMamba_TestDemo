# CHƯƠNG 5. CÀI ĐẶT VÀ ỨNG DỤNG

> **Ghi chú soạn thảo (xóa khi nộp):**
> - Bản rút gọn, nén từ `md_bao_cao/06_CHUONG_5_CAI_DAT_UNG_DUNG.md` (tag git `ban_day_du_147`). Bảng API, cấu trúc kết quả suy luận và cấu trúc bản ghi MongoDB chuyển xuống Phụ lục G. Ba bảng môi trường gộp thành Bảng 5.1; bảng chế độ tách thành phần dùng chung Bảng 3.4.
> - Bản rút gọn giữ **7 ảnh chụp** (Hình 5.1, 5.3–5.8). Các ảnh tùy chọn của bản đầy đủ (trang chủ, đăng nhập, trang phân tích trước khi chạy, dashboard, quản trị, thông báo lỗi, chế độ tối, kết quả kiểm thử, tài liệu API `/docs`) không đưa vào bản này. Số hình ở đây khác số khung [CHỤP HÌNH] của bản đầy đủ.
> - **[CẦN KIỂM TRA]** là điểm cần nhóm xác nhận trước khi nộp.

Chương này trình bày phần cài đặt thực nghiệm (môi trường, cài đặt hai mô hình, huấn luyện trên Kaggle, lưu trữ kết quả) và ứng dụng minh họa PolypVision (kiến trúc, dịch vụ suy luận, lưu trữ, giao diện Web và Mobile).

## 5.1. Môi trường và công cụ

Huấn luyện chạy trên Kaggle theo đề cương; mỗi tài khoản có hạn mức GPU khoảng 30 giờ mỗi tuần, trong khi một lượt mô hình tích hợp mất khoảng 4,7 giờ, nên các lượt được chia cho nhiều tài khoản chạy song song. Kết quả được tải về máy cá nhân để tính lại số liệu, vẽ hình và đo tốc độ.

*Bảng 5.1. Môi trường huấn luyện và đánh giá*

| Thành phần | Giá trị | Ghi chú |
|---|---|---|
| Huấn luyện | Kaggle Notebook, NVIDIA Tesla T4 15 GB, Python 3.12, PyTorch 2.10.0 + CUDA 12.8 **[CẦN KIỂM TRA]** | Theo nhật ký lượt chạy thử; chưa có nhật ký gắn với từng lượt chính |
| Ultralytics | 8.4.127 | Ghi trong mọi tệp `best.pt` |
| Thời gian một lượt (100 epoch) | Mô hình gốc khoảng 2,3 giờ; mô hình tích hợp khoảng 4,7 giờ | Trung bình 20 seed |
| Máy đánh giá | AMD Ryzen 7 250 (8 lõi, 16 luồng), RAM 15,3 GiB; NVIDIA GeForce RTX 5050 Laptop; Windows 11 | Đo độ trễ CPU, GPU; đánh giá theo điểm ảnh |
| Môi trường Python có GPU | PyTorch 2.13.0 + CUDA 13.0 | Script đánh giá theo điểm ảnh |
| Dịch vụ suy luận | Python 3.12, PyTorch 2.6.0 (CPU), Ultralytics 8.4.127 theo `requirements.txt` **[CẦN KIỂM TRA: môi trường ảo hiện cài 8.4.103, nên cài lại cho khớp]** | Ứng dụng PolypVision |

Đề cương quy định Python cho mô hình và API, Java cho Web; nhóm bổ sung Dart/Flutter cho di động. Đề tài chỉ dùng PyTorch (không dùng TensorFlow) vì Ultralytics YOLO26 [42] và các bản cài đặt Mamba đều viết trên PyTorch, nhờ đó khối C2TSVMamba ghép thẳng vào mô hình gốc. Các công cụ khác: NumPy, pandas, OpenCV, SciPy, Matplotlib cho dữ liệu, thống kê và vẽ hình; FastAPI, Uvicorn cho dịch vụ suy luận; Java 17, Spring Boot 4.1, Thymeleaf, Spring Security, Bootstrap 5 và MongoDB cho Web; Flutter cho di động; Git để quản lý mã.

## 5.2. Cài đặt hai mô hình

### 5.2.1. Mô hình gốc YOLO26s-seg

Mô hình gốc dùng nguyên bản Ultralytics 8.4.127, khởi tạo từ `yolo26s-seg.pt` tiền huấn luyện trên COCO [41], lớp đầu ra đổi từ 80 lớp sang 1 lớp `polyp` (tệp `data_bg20.yaml` khai báo `nc: 1`, `names: {0: polyp}`). Lệnh huấn luyện chính:

```python
model = YOLO("yolo26s-seg.pt")
model.train(data="data_bg20.yaml", epochs=100, imgsz=640, batch=8,
            optimizer="AdamW", lr0=0.001, warmup_epochs=5.0,
            amp=False, deterministic=True, seed=SEED, workers=2,
            patience=100, close_mosaic=10)
```

*Bảng 5.2. Siêu tham số huấn luyện (giống nhau ở mọi lượt của cả hai mô hình)*

| Nhóm | Tham số |
|---|---|
| Dữ liệu | Ảnh vào 640×640; không lưu đệm ảnh (`cache=False`) |
| Tối ưu | AdamW [40]; tốc độ học ban đầu 0,001, cuối 0,01 × ban đầu; momentum 0,937; suy giảm trọng số 0,0005; khởi động 5 epoch |
| Lịch | 100 epoch; lô 8 ảnh; không dừng sớm (`patience=100`); tắt Mosaic ở 10 epoch cuối |
| Tăng cường | Mosaic [39] 1,0; lật ngang 0,5; co giãn 0,5; dịch 0,1; đổi màu HSV (0,015; 0,7; 0,4); không xoay, không lật dọc, không MixUp |
| Mặt nạ | Tỉ lệ thu nhỏ mặt nạ 4 (mặt nạ 160×160) |
| Độ chính xác số | FP32 hoàn toàn (`amp=False`) |
| Tất định | `deterministic=True`, 2 luồng nạp dữ liệu, seed cố định cho từng lượt |

**Khóa tất định.** Notebook đặt seed cho `random`, `numpy`, `torch` (cả CUDA), đặt `PYTHONHASHSEED`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`, tắt `cudnn.benchmark` và bật `torch.use_deterministic_algorithms(True)`, nên cùng seed thì cùng thứ tự dữ liệu và cùng khởi tạo.

### 5.2.2. Mô hình tích hợp VMamba

Khối C2TSVMamba không có trong Ultralytics gốc, nên nhóm tạo bản sao (fork) của Ultralytics 8.4.127:

*Bảng 5.3. Các tệp được thêm hoặc sửa trong fork*

| Tệp | Nội dung thay đổi |
|---|---|
| `nn/modules/topology_shape_vmamba.py` (mới) | Cài đặt SS2D, ShapeAwareBranch, DirectionalShapeExtractor, TopologyShapeGate, TSVMamba và C2TSVMamba |
| `nn/modules/__init__.py`, `nn/tasks.py` | Xuất các lớp mới; đăng ký `C2TSVMamba` để trình đọc YAML dựng được mô hình |
| `cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml` (mới) | Giống `yolo26-seg.yaml`, chỉ đổi tầng 10: `C2PSA` → `C2TSVMamba` |
| `engine/trainer.py`, `utils/torch_utils.py` | Bản vá lưu checkpoint ở FP32, mô tả trong `PATCH_FP32.md` |
| `tests/test_topology_shape_vmamba.py` (mới) | Kiểm thử tự động cho khối mới |

Mô hình tích hợp được dựng từ YAML ở cỡ *s* rồi nạp trọng số, cùng tham số huấn luyện ở Bảng 5.2:

```python
model = YOLO("yolo26s-seg-TopologyShapeVMamba.yaml").load("yolo26s-seg.pt")
```

Lưu ý: Ultralytics đoán cỡ mô hình từ **tên tệp YAML**; tên phải chứa `yolo26s`, nếu không mô hình bị dựng ở cỡ *n* và không nạp được trọng số. Bản vá FP32 (mục 3.5.3) đổi hàm lưu mô hình, `MultiTrainer` và `strip_optimizer` sang `.float()`, và báo lỗi ngay khi gặp NaN hoặc vô cùng; vì vậy mô hình tích hợp được gọi là **TSVM FP32**. Thí nghiệm tách thành phần dùng cùng notebook, chỉ đổi đối số tầng 10 trong YAML, ví dụ `[-1, 2, C2TSVMamba, [1024, 0.5, 16, 3, "vmamba_only"]]`; ba chế độ ở Bảng 3.4, mỗi chế độ chạy seed 0–4, tổng 15 lượt chia cho 6 tài khoản Kaggle.

## 5.3. Quy trình huấn luyện và lưu trữ kết quả thực nghiệm

Đề tài dùng ba notebook Kaggle: notebook mô hình gốc (tạo `data_bg20.yaml`, cài `ultralytics==8.4.127`, khóa tất định, huấn luyện, nén kết quả); notebook mô hình tích hợp (thêm bước nạp fork bằng liên kết tượng trưng tên `ultralytics` và tải `yolo26s-seg.pt`); notebook tách thành phần (thêm ô chọn chế độ, seed và ô **kiểm tra mô hình** trước khi huấn luyện, sai số tham số tầng 10 thì dừng ngay để không tốn giờ GPU). Bản notebook mô hình tích hợp còn lưu trong kho mã trỏ tới fork cũ (FP16); khi chạy các lượt chính, đường dẫn đã được sửa sang fork FP32, bằng chứng là mọi `best.pt` của mô hình tích hợp đều lưu FP32 **[NÊN LƯU LẠI BẢN NOTEBOOK ĐÃ SỬA VÀO KHO MÃ]**.

> **[CHỤP HÌNH 5.1] Notebook Kaggle đang chạy.**
> - **Màn hình:** notebook tách thành phần trên Kaggle (đang chạy), khung bên phải mở mục *Input* (thấy hai dataset `kvasir-yolo-seg-bg20` và `ultralytics-topology-shape-aware-vmamba-fp32`) và *Settings* (thấy Accelerator là GPU).
> - **Cần thấy:** đầu ra của ô kiểm tra mô hình, có dòng "Tham số tầng 10 = … ✅", và vài dòng nhật ký huấn luyện có cột epoch, loss, mAP.
> - **Lưu ý:** che tên tài khoản Kaggle nếu không muốn công khai.

Mỗi lượt huấn luyện lưu riêng một thư mục `Kvasir_BG20_<Mô hình>_s<seed>_w2` gồm `args.yaml` (toàn bộ cấu hình), `results.csv` (chỉ số và loss từng epoch) và `weights/best.pt`, đặt trong `03_ket_qua_huan_luyen/` theo từng mô hình (`Baseline_YOLO26s_seg/`, `TSVM_FP32/`, và `Vmamba_only/`, `Shape_only/`, `No_guidance/` cho thí nghiệm tách thành phần). Từ các tệp này, script `tinh_lai_so_lieu.py` tính lại mọi số liệu ra bảng CSV, `danh_gia_pixel.py` suy luận lại để tính Dice và IoU theo điểm ảnh cho bốn mô hình, `ve_hinh.py` vẽ hình. Mọi con số trong Chương 6 truy được về bảng và script tương ứng (Phụ lục C).

## 5.4. Ứng dụng PolypVision: yêu cầu và kiến trúc

Theo đề cương, ứng dụng cần cho phép tải ảnh nội soi, phân đoạn polyp và hiển thị mặt nạ, đường biên, độ tin cậy, lưu trữ kết quả dự đoán và so sánh mô hình gốc với mô hình tích hợp VMamba. Nhóm bổ sung quản lý tài khoản, phân quyền, lịch sử, trang quản trị và ứng dụng di động.

*Bảng 5.4. Đối chiếu yêu cầu đề cương với chức năng đã cài đặt*

| Yêu cầu | Web | Mobile | Ghi chú |
|---|---|---|---|
| Tải ảnh nội soi | Có | Có (chọn từ thư viện hoặc chụp) | JPG, JPEG, PNG; tối đa 10 MB |
| Hiển thị mặt nạ phân đoạn | Có | Có | Ảnh chồng (overlay) mặt nạ lên ảnh gốc |
| Hiển thị đường biên polyp | Có | Có | Dịch vụ suy luận vẽ thêm đường viền vàng theo đa giác của từng mặt nạ (`masks.xy`) sau khi Ultralytics tô mặt nạ và hộp bao |
| Hiển thị độ tin cậy | Có (thanh tiến trình, %) | Có | Độ tin cậy cao nhất trong các đối tượng; dịch vụ trả thang 0–1, Website đổi sang 0–100 |
| Lưu trữ kết quả | Có (MongoDB + tệp ảnh) | Không lưu | Mobile cố ý không lưu ảnh để bảo vệ quyền riêng tư |
| So sánh hai mô hình | Có | Có | Chạy lần lượt hai mô hình trên cùng ảnh |

Hệ thống gồm ba thành phần (Hình 5.2). **Dịch vụ suy luận FastAPI** giữ hai mô hình, dùng chung cho nhánh Web (trình duyệt → Spring Boot → FastAPI; Spring Boot quản lý tài khoản, lịch sử, MongoDB, tệp ảnh) và nhánh Mobile (Flutter → FastAPI, không tài khoản, không lưu lịch sử). Tách dịch vụ suy luận giúp nạp mô hình một lần, phần Java không phụ thuộc PyTorch, và có thể chuyển dịch vụ sang máy có GPU mà không đổi giao diện.

![Hình 5.2](../hinh/chung/vi/s01_kien_truc_ung_dung.png)

*Hình 5.2. Kiến trúc hệ thống PolypVision. Website (Spring Boot, cổng 8080) và ứng dụng di động (Flutter) là hai client độc lập của cùng dịch vụ suy luận FastAPI (cổng 8000). Chỉ nhánh Web có MongoDB và kho tệp ảnh.*

## 5.5. Dịch vụ suy luận và tổ chức lưu trữ

Khi khởi động, dịch vụ nạp hai checkpoint lấy từ **seed 0**: `YOLO26s-seg` (mô hình gốc) và `YOLO26s-TSVM-FP32-seg` (mô hình tích hợp). Mã khối C2TSVMamba được chép vào dịch vụ và đăng ký đúng đường dẫn mô-đun ghi trong checkpoint; mô hình được ép về FP32 và suy luận với `half=False`; tệp `experiment_manifest.json` lưu mã băm SHA-256 của từng checkpoint, dịch vụ trả mã băm của tệp đang nạp ở API `/health` để đối chiếu. Ở seed 0, epoch của `best.pt` trùng epoch có mask mAP50–95 cao nhất (mô hình gốc epoch 89, mô hình tích hợp epoch 88), nhưng riêng seed này mô hình tích hợp có mask mAP50–95 **thấp hơn** mô hình gốc (0,7245 so với 0,7366), nên các hình so sánh trên ứng dụng chỉ có tính minh họa. Ngưỡng tin cậy mặc định 0,25, kích thước ảnh 640. Dịch vụ có API riêng cho Web (`/health`, `/predict`) và cho Mobile (`/api/v1/models`, `/api/v1/inference`, `/api/v1/comparison`…), kiểm tra ảnh đầu vào trước khi suy luận và không lưu ảnh sau khi xử lý; danh sách API và cấu trúc kết quả ở Phụ lục G. Thời gian `processingTimeMs` trả về gồm cả tiền xử lý và hậu xử lý, không phải phép đo hiệu năng khoa học.

Chỉ nhánh Web lưu kết quả: tài khoản (tập `users`, mật khẩu băm bằng BCrypt) và lịch sử phân tích (tập `diagnosis_history`) trong MongoDB, ảnh gốc và ảnh kết quả trong thư mục `storage/original/` và `storage/results/`. Một lần so sánh tạo hai bản ghi có cùng `comparisonGroupId`, nên dùng chung cấu trúc cho phân tích đơn lẻ và so sánh. Người dùng thường chỉ xem và xóa được dữ liệu của mình; tài khoản quản trị xem được thống kê toàn hệ thống.

## 5.6. Giao diện và chức năng

**Website** (Spring Boot, Thymeleaf, Bootstrap 5) có: đăng ký, đăng nhập, phân quyền `USER` và `ADMIN`; phân tích một ảnh bằng một trong hai mô hình; so sánh hai mô hình trên cùng ảnh; lịch sử phân tích và so sánh có tìm kiếm, lọc, phân trang; tải ảnh kết quả, xóa dữ liệu; hồ sơ, đổi mật khẩu; trang quản trị và thống kê. Các cơ chế bảo mật cơ bản gồm phiên đăng nhập, chống giả mạo yêu cầu (CSRF), băm mật khẩu và tiêu đề HTTP bảo mật.

> **[CHỤP HÌNH 5.3] Kết quả phân tích một ảnh.** *(Hình quan trọng nhất của chương)*
> - **Thao tác:** đăng nhập bằng **tài khoản thử tạo riêng cho việc chụp hình**, vào trang *Phân tích* (`/diagnose`, **không** dùng trang `/diagnoses/demo` vì đó là kết quả mẫu cố định). Chọn một ảnh tập kiểm định có polyp rõ (gợi ý: một trong ba ảnh ở Hình q01 Chương 6), mô hình *YOLO26s-TSVM-FP32-seg*, bấm *Phân tích*.
> - **Cần thấy cùng lúc:** ảnh gốc và ảnh có mặt nạ chồng lên, đường viền vàng; **ô độ tin cậy dạng %** có thanh tiến trình; số polyp; thời gian xử lý; tên mô hình; dòng cảnh báo y khoa.

> **[CHỤP HÌNH 5.4] Kết quả so sánh hai mô hình.**
> - **Thao tác:** vào trang *So sánh* (`/compare`), tải **cùng ảnh** ở Hình 5.3, bấm chạy.
> - **Cần thấy:** hai cột kết quả cạnh nhau, mỗi cột có ảnh overlay, độ tin cậy, số mặt nạ và thời gian xử lý. Chú thích chỉ mô tả, **không kết luận** mô hình nào tốt hơn từ một ảnh.

> **[CHỤP HÌNH 5.5] Lịch sử phân tích.**
> - **Thao tác:** sau khi đã phân tích vài ảnh (đơn lẻ và so sánh), vào trang *Lịch sử* (`/history`).
> - **Cần thấy:** danh sách bản ghi có ảnh thu nhỏ, tên mô hình, độ tin cậy, thời điểm; ô tìm kiếm, bộ lọc, phân trang.

> **[CHỤP HÌNH 5.6] Dữ liệu lưu trữ.** *(Minh chứng "tổ chức lưu trữ kết quả" của đề cương)*
> - **Thao tác:** mở MongoDB Compass, tập `diagnosis_history`, mở bản ghi của lần phân tích ở Hình 5.3; mở thêm thư mục `storage/`. Ghép thành một hình hai phần.
> - **Cần thấy:** các trường `modelType`, `confidence`, `originalImageUrl`, `resultImageUrl`, `createdAt`… và hai thư mục `original/`, `results/` có tệp ảnh tương ứng.
> - **Lưu ý:** không chụp tập `users` (có email và mã băm mật khẩu).

**Ứng dụng di động** (Flutter) gọi thẳng dịch vụ suy luận, phục vụ trình diễn nhanh: màn hình chính hiển thị trạng thái dịch vụ và hai mô hình; suy luận một mô hình hoặc so sánh hai mô hình; kiểm tra ảnh (JPG, JPEG, PNG, tối đa 10 MB); tiến trình tải lên, hủy, thử lại, báo lỗi; xem ảnh toàn màn hình; tự co giãn theo màn hình, chế độ sáng và tối.

> **[CHỤP HÌNH 5.7] Ứng dụng di động** (một hình ba phần: (a) màn hình chính, (b) kết quả suy luận, (c) so sánh hai mô hình).
> - **Thao tác:** chạy dịch vụ suy luận với `--host 0.0.0.0`, chạy ứng dụng trên máy ảo Android (`AI_BASE_URL=http://10.0.2.2:8000`) hoặc điện thoại thật cùng mạng; dùng cùng ảnh ở Hình 5.3, chọn mô hình tích hợp.
> - **Cần thấy:** (a) trạng thái dịch vụ "sẵn sàng" và hai mô hình; (b) ảnh overlay, độ tin cậy, số mặt nạ, thời gian xử lý; (c) kết quả hai mô hình trên cùng màn hình.

**Kiểm thử.** Mỗi thành phần có bộ kiểm thử tự động riêng (Bảng 5.5); ngoài ra nhóm đã kiểm thử thủ công trên điện thoại Android thật các chức năng kiểm tra trạng thái, suy luận, so sánh, phóng to, thử lại khi lỗi, xoay màn hình, chế độ tối.

*Bảng 5.5. Kết quả kiểm thử tự động* **[CẦN KIỂM TRA: chạy lại các lệnh kiểm thử trước khi nộp và cập nhật số]**

| Thành phần | Công cụ | Kết quả ghi nhận |
|---|---|---|
| Ứng dụng di động | `flutter test` | 498/498 ca đạt |
| Dịch vụ suy luận | `pytest` | 50/50 ca đạt |
| Website | `mvnw test` (JUnit) | 261/261 ca đạt |

## 5.7. Triển khai trên dữ liệu thực tế

Để kiểm tra mô hình trên ảnh **khác nguồn**, nhóm dùng bốn bộ dữ liệu công khai không tham gia huấn luyện: CVC-ClinicDB (612 ảnh), CVC-ColonDB (380 ảnh), ETIS-Larib (196 ảnh) và phần ảnh đơn của PolypGen (1.537 ảnh từ 6 trung tâm). Việc triển khai gồm đánh giá định lượng (chạy checkpoint 20 seed của bốn mô hình trên toàn bộ bốn bộ, tính Dice, IoU, Precision, Recall theo điểm ảnh, kết quả ở mục 6.7) và minh họa trên ứng dụng bằng chức năng so sánh.

> **[CHỤP HÌNH 5.8] So sánh hai mô hình trên ảnh ngoài** (một hình hai phần: (a) ảnh CVC-ClinicDB, (b) ảnh ETIS-Larib).
> - **Thao tác:** trang *So sánh* của Website; mỗi bộ chọn một ảnh đại diện cho xu hướng chung ở mục 6.7, không chọn trường hợp hiếm.
> - **Cần thấy:** ảnh overlay và độ tin cậy của hai mô hình. Chú thích ghi rõ tên bộ dữ liệu và tên tệp ảnh.

Kết quả trên ứng dụng chỉ có tính minh họa; kết luận về khả năng tổng quát hóa dựa trên đánh giá định lượng ở Chương 6. Bốn bộ dữ liệu là ảnh công khai, không phải dữ liệu lâm sàng thu tại bệnh viện.

## 5.8. Hạn chế và kết chương

Phần cài đặt còn các hạn chế: phép quét SS2D viết bằng PyTorch thuần nên mô hình tích hợp chậm khoảng gấp đôi trên CPU; thông tin GPU và phiên bản PyTorch trên Kaggle chỉ có từ nhật ký lượt chạy thử; ứng dụng di động chưa có tài khoản, lịch sử và chưa chạy ngoại tuyến; chưa có HTTPS và giới hạn tần suất gọi API, ảnh lưu trên đĩa cục bộ; ứng dụng không phải thiết bị y tế, độ tin cậy hiển thị là điểm của mô hình chứ không phải xác suất mắc bệnh.

Chương 5 đã trình bày môi trường, cách cài đặt hai mô hình (fork Ultralytics chỉ khác tầng 10, bản vá lưu FP32), quy trình huấn luyện có khóa tất định với kết quả truy được về tệp gốc, và ứng dụng PolypVision đáp ứng các yêu cầu tải ảnh, hiển thị mặt nạ và độ tin cậy, lưu trữ và so sánh hai mô hình. Chương 6 trình bày kết quả thực nghiệm.

---

## Danh sách hình cần chụp (ghi chú soạn thảo, xóa khi nộp)

| Mã | Nội dung | Bắt buộc |
|---|---|---|
| 5.1 | Notebook tách thành phần chạy trên Kaggle | Có |
| 5.3 | Kết quả phân tích: mặt nạ, đường viền, độ tin cậy | **Rất quan trọng** |
| 5.4 | Kết quả so sánh hai mô hình | **Rất quan trọng** |
| 5.5 | Lịch sử phân tích | Có |
| 5.6 | MongoDB Compass và thư mục `storage/` | **Có (minh chứng lưu trữ)** |
| 5.7 | Mobile: màn hình chính, kết quả, so sánh (ba phần) | Có |
| 5.8 | So sánh trên ảnh CVC-ClinicDB, ETIS-Larib (hai phần) | Có |

Hình 5.2 (kiến trúc hệ thống) là hình vẽ. Đường viền polyp bổ sung ngày 28/10/2026, nên các hình 5.3, 5.4, 5.7, 5.8 phải chụp sau ngày này.
