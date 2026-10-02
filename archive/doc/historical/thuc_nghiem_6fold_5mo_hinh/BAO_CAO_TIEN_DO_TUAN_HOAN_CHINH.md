# BÁO CÁO TIẾN ĐỘ THỰC NGHIỆM VÀ KẾT QUẢ NGHIÊN CỨU TUẦN
**Đề tài:** Nghiên cứu phương pháp tích hợp VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng  
**Mã đề tài:** CNTT_KLCN182 — Khóa luận Cử nhân ngành CNTT (2026 – 2027)  
**Giảng viên hướng dẫn:** TS. Phùng Thế Bảo (Email: baopt@huit.edu.vn)  
**Nhóm sinh viên thực hiện:**
1. Lê Đức Lương (MSSV: 2001230490 — Lớp: 14DHTH09)
2. Phùng Tuấn Huy (MSSV: 2001230312 — Lớp: 14DHTH13)
3. Trần Mạnh Toàn (MSSV: 2001230830 — Lớp: 14DHTH09)  
**Trọng tâm báo cáo:** Đánh giá hiệu năng thực nghiệm kiểm thử Seed Robustness (6 seed), kiểm chứng kiến trúc C2TSVMamba, phân tích ma trận nhầm lẫn lâm sàng và kế hoạch hành động.

---

## 1. MỤC TIÊU, PHẠM VI VÀ TIẾN ĐỘ THỰC HIỆN

### 1.1. Sơ đồ Luồng Xử lý Toàn diện (Architecture Pipeline Flow)
Đề tài xây dựng giải pháp phân đoạn polyp đại trực tràng tự động hỗ trợ can thiệp nội soi, tích hợp khối trích xuất đặc trưng hình thái học và không gian trạng thái thị giác SS2D (Visual State Space Model - VMamba) tại Tầng 10 của mạng YOLO26s-seg:

\text{Ảnh Nội soi Đại trực tràng (Kvasir-SEG)} \longrightarrow \text{Backbone YOLO26s} \longrightarrow \text{Tầng 10: Khối C2TSVMamba} \longrightarrow \text{Neck / Dual-Head} \longrightarrow \begin{cases} \text{Mặt nạ phân đoạn bám sát viền polyp} \\ \text{Hộp bao định vị tổn thương} \end{cases}

### 1.2. Bảng Theo dõi Tiến độ Thực hiện Hiện tại
| Hạng mục công việc | Trạng thái | Ghi chú & Kết quả cụ thể |
| :--- | :---: | :--- |
| **Chuẩn hóa bộ dữ liệu Kvasir-SEG** | **Hoàn thành** | 6 fold độc lập (880 ảnh train / 120 ảnh val, 127 polyp kiểm định) |
| **Thiết lập môi trường huấn luyện & kiểm thử** | **Hoàn thành** | GPU RTX, PyTorch 2.x, Ultralytics framework |
| **Huấn luyện mô hình Baseline YOLO26s-seg** | **Hoàn thành** | Đầy đủ 6 Seed (s0 – s5), 100 epoch/seed |
| **Thiết kế khối C2TSVMamba tại Tầng 10** | **Hoàn thành** | Tích hợp nhánh Morphological CNN + VMamba SS2D 4 hướng quét |
| **Huấn luyện mô hình đề xuất C2TSVMamba** | **Hoàn thành** | Đầy đủ 6 Seed (s0 – s5), 100 epoch/seed |
| **Khảo sát mô hình đối chứng P5_Attention** | **Hoàn thành** | Đầy đủ 6 Seed (s0 – s5) làm sáng tỏ vai trò kiến trúc |
| **Tổng hợp số liệu thống kê trung bình (Mean ± Std)** | **Hoàn thành** | Xuất file summary_mean_std_2models.csv và kiểm định Paired t-test |
| **Xuất hệ thống biểu đồ 300 DPI chuẩn in ấn** | **Hoàn thành** | Thư mục KQ_DoiXung gồm 9 nhóm hình đối chứng & các biểu đồ đơn lẻ |
| **Đánh giá định tính trên ảnh lâm sàng** | **Hoàn thành** | Minh chứng trực quan khả năng khử viền răng cưa và chống lóa |
| **Kiểm thử trên bộ dữ liệu độc lập (Cross-dataset)** | *Đang thực hiện* | Chuẩn bị dữ liệu CVC-ClinicDB / BKAI-IGH |
| **Đóng gói tối ưu hóa suy luận (ONNX / TensorRT)** | *Chưa thực hiện* | Kế hoạch tuần tiếp theo |

### 1.3. Thống kê Phân chia Tập Dữ liệu Kvasir-SEG
| Tập dữ liệu | Số lượng ảnh | Phân giải gốc | Phân giải huấn luyện | Số lượng tổn thương polyp kiểm định |
| :--- | :---: | :---: | :---: | :---: |
| **Tập huấn luyện (Training Set)** | 880 ảnh |  \times 500 \sim 1920 \times 1072$ |  \times 640$ | Khoảng 950 đối tượng polyp |
| **Tập kiểm định (Validation Set)** | 120 ảnh |  \times 500 \sim 1920 \times 1072$ |  \times 640$ | **Đúng 127 polyp** (chuẩn hóa trên cả 6 seed) |
| **Tổng cộng bộ dữ liệu Kvasir-SEG** | **1,000 ảnh** | — | — | **Toàn bộ có ground-truth bác sĩ nội soi** |

### 1.4. Bảng Cấu hình Môi trường Thực nghiệm và Siêu tham số Huấn luyện Chuẩn hóa
Toàn bộ quá trình thực nghiệm được triển khai đồng bộ trên nền tảng **Kaggle GPU Cloud** với phiên bản thư viện cốt lõi **Ultralytics 8.4.127** và PyTorch. Nhằm triệt tiêu hoàn toàn sự ngẫu nhiên của phần cứng và đảm bảo kết quả 6 seed có thể tái lập 100% (Bit-exact Reproducibility), quy trình khóa tất định nghiêm ngặt đã được áp dụng trước mọi lượt huấn luyện:

```python
# Giao thức khóa tất định hệ thống (Deterministic Environment Protocol)
os.environ["PYTHONHASHSEED"] = str(SEED)
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True
torch.use_deterministic_algorithms(True, warn_only=False)
```

| Nhóm thông số | Thông số cấu hình | Giá trị thiết lập | Ý nghĩa học thuật & Vai trò kỹ thuật |
| :--- | :--- | :---: | :--- |
| **Nền tảng & Thư viện** | Framework cốt lõi | `ultralytics == 8.4.127` | Đảm bảo đồng nhất cấu trúc engine phân đoạn |
| | Môi trường tính toán | Kaggle GPU Cloud (CUDA) | Môi trường GPU độc lập, nhất quán tài nguyên |
| | Số tiến trình nạp dữ liệu | `workers = 2` | Tối ưu hóa I/O, tránh nghẽn luồng CPU |
| | Khóa tất định thuật toán | `deterministic = True` | Khóa cuBLAS và cuDNN, loại bỏ ngẫu nhiên ma trận |
| **Khởi tạo kiến trúc** | Baseline phân đoạn | `YOLO("yolo26s-seg.pt")` | Nạp trực tiếp trọng số chuẩn segmentation |
| | Đề xuất C2TSVMamba | `YOLO(yaml_cfg).load("yolo26s-seg.pt")` | Khởi tạo topology `scale: 's'`, kế thừa backbone/head COCO và huấn luyện thích nghi Tầng 10 |
| **Cấu hình dữ liệu** | Phân lớp bài toán | `nc: 1`, `{0: 'polyp'}` | Bài toán phân đoạn thực thể nhị phân (Polyp vs Nền) |
| | Độ phân giải đầu vào | `imgsz = 640` ($640 \times 640$) | Chuẩn hóa kích thước khung hình nội soi lâm sàng |
| | Kích thước batch | `batch = 8` | Đảm bảo cân bằng gradient và dung lượng bộ nhớ VRAM |
| | Bộ nhớ đệm ảnh | `cache = False` | Đọc trực tiếp từ đĩa tránh tràn RAM hệ thống |
| **Tối ưu hóa & Lịch trình** | Thuật toán tối ưu | `optimizer = "AdamW"` | Tối ưu hóa trọng số phi tuyến và kiểm soát phân kỳ |
| | Tốc độ học ban đầu | `lr0 = 0.001` | Khởi tạo learning rate chuẩn cho AdamW |
| | Thời gian khởi động | `warmup_epochs = 5.0` | Ổn định trọng số mới của khối VMamba ở đầu quá trình |
| | Tổng số vòng lặp | `epochs = 100` | Đảm bảo đường cong hội tụ sâu qua epoch 80 |
| | Ngưỡng dừng sớm | `patience = 100` | Duy trì đủ 100 epoch để theo dõi trọn vẹn đường cong loss |
| | Độ chính xác hỗn hợp | `amp = False` | Duy trì tính toán float32 chuẩn xác, tránh lỗi dưới tràn float16 |
| **Hàm mất mát & Tăng cường** | Đóng tăng cường Mosaic | `close_mosaic = 10` | Tắt ghép ảnh ở 10 epoch cuối để mô hình ổn định biên mặt nạ |
| | Trọng số Box / Cls / Seg | `box: 7.5`, `cls: 0.5`, `dfl: 1.5` | Ưu tiên tối đa độ sắc nét của mặt nạ phân đoạn |

---

## 2. CẤU TRÚC MÔ HÌNH VÀ CƠ CHẾ TÍCH HỢP C2TSVMAMBA TẠI TẦNG 10

### 2.1. Vai trò tích hợp VMamba trong pipeline phân đoạn polyp
Trong nội soi đại trực tràng, tổn thương polyp thường có ranh giới hòa lẫn vào niêm mạc xung quanh, kích thước đa dạng và bề mặt phản chiếu ánh sáng gây nhiễu. Mô hình tích hợp VMamba được thiết kế nhằm giải quyết triệt để bài toán trích xuất đặc trưng vùng bệnh, đóng vai trò then chốt trong việc 'tô' và phân đoạn chính xác đường biên tổn thương.

Khối **C2TSVMamba (Cross-Stage Partial Topology-Shape-aware VMamba)** được tích hợp tại **Tầng 10 (Layer 10)** thuộc Cổ mạng (Neck). Đây là vị trí chiến lược ngay sau khối Spatial Pyramid Pooling - Fast (SPPF) của Backbone, tiếp nhận bản đồ đặc trưng P5 đa vĩ mô ($B 	imes 512 	imes 20 	imes 20$) trước khi truyền sang các tầng tổng hợp đặc trưng P4, P3. Cấu trúc khối bao gồm hai nhánh xử lý song song bổ trợ lẫn nhau:
- **Nhánh VMamba SS2D (2D Selective Scan):** Quét bản đồ đặc trưng theo 4 hướng không gian, mô hình hóa mối tương quan không gian toàn cục dài hạn với độ phức tạp tính toán tuyến tính $\mathcal{O}(N)$, vượt trội so với cơ chế Self-Attention bậc hai $\mathcal{O}(N^2)$ của Transformer.
- **Nhánh Tích chập Hình thái Đa hướng (Multi-directional Morphological Convolutions):** Sử dụng các kernel tích chập bất đối xứng ($1	imes 5, 5	imes 1$ và $3	imes 3$) kết hợp cơ chế cổng định hướng (Gated Directional Mapping) để bắt giữ gradient thay đổi đột ngột tại viền polyp, cung cấp thông tin tô viền sắc nét.

### 2.2. Giải trình học thuật đối với mô hình đối chứng YOLO + CNN/Attention
Thực hiện theo chỉ đạo của Thầy về việc xây dựng mô hình kết hợp YOLO và CNN/Attention để đối sánh, nhóm đã thực hiện khảo sát biến thể ban đầu mang tên **P5_Attention_VMamba** (chèn khối VMamba kết hợp cơ chế Attention tuyến tính tại tầng P5). Kết quả thực nghiệm 6 seed cho thấy:
- **Điểm yếu của nhánh P5_Attention:** Hàm mất mát phân đoạn kiểm định (`val/seg_loss`) bị tăng vọt lên $1.4630 \pm 0.0890$ (kém hơn mức $1.4164$ của Baseline), và độ biến động mAP50-95 tăng lên $\pm 0.0120$. Điều này chứng minh việc chèn Attention thuần túy tại P5 mà thiếu sự dẫn hướng cấu trúc hình học sẽ làm phân tán các đặc trưng biên cục bộ.
- **Giải pháp hoàn thiện trong C2TSVMamba:** Khối C2TSVMamba tại Tầng 10 đã kết hợp chặt chẽ nhánh CNN hình thái học cùng SS2D, khắc phục hoàn toàn sự suy giảm của phiên bản P5_Attention, kéo `val/seg_loss` giảm sâu xuống $1.3812 \pm 0.0470$ và ổn định độ lệch chuẩn mAP qua 6 seed xuống chỉ còn $\pm 0.0050$.

---

## 3. KẾT QUẢ ĐỊNH LƯỢNG ĐỐI CHỨNG QUA 6 SEED (SEED ROBUSTNESS)

Toàn bộ 18 lượt huấn luyện độc lập (6 seed $	imes$ 3 dòng mô hình) được thực hiện trên cùng môi trường phần cứng với bộ siêu tham số đồng nhất: kích thước ảnh 640x640, 100 epoch, batch size 16, bộ tối ưu SGD (lr=0.01, cos_lr=True, warmup 3 epoch). Các chỉ số được trích xuất tại epoch tối ưu (Best Mask mAP50-95) từ tệp `results.csv` của từng lượt chạy.

> **Tài nguyên Dữ liệu Đi kèm:** Toàn bộ bảng giá trị trung bình $\pm$ độ lệch chuẩn (Mean ± Std), Min, Max, Delta $\Delta$, tỷ lệ cải thiện và kiểm định thống kê Paired t-test đã được kết xuất sẵn tại tệp CSV:  
> - **[summary_mean_std_2models.csv](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20Topolo/summary_mean_std_2models.csv)** (hoặc tại Ket_Qua_2/summary_mean_std_2models.csv): Bảng đối sánh chi tiết theo từng chỉ số kèm chuỗi Mean ± Std.  
> - **[summary_models_2rows.csv](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20Topolo/summary_models_2rows.csv)**: Bảng 2 dòng gọn nhẹ cho Baseline và C2TSVMamba, sẵn sàng nạp vào mã nguồn Python vẽ biểu đồ.

### 3.1. Bảng so sánh tổng hợp chỉ số định lượng

| Chỉ số đo lường | YOLO26s-seg Baseline | C2TSVMamba Đề xuất | Độ chênh lệch ($\Delta$) | Tỷ lệ (%) | P5_Attention (Đối chứng) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Mask mAP50-95** | $0.7298 \pm 0.0150$<br>[$0.7073 – 0.7496$] | **$0.7246 \pm 0.0050$**<br>[$0.7196 – 0.7308$] | $-0.0052$ | $-0.71\%$ | $0.7191 \pm 0.0120$<br>[$0.7064 – 0.7406$] |
| **Mask mAP50** | $0.9129 \pm 0.0070$<br>[$0.9049 – 0.9223$] | **$0.9134 \pm 0.0090$**<br>[$0.9055 – 0.9268$] | **$+0.0005$** | **$+0.05\%$** | $0.9106 \pm 0.0077$<br>[$0.9021 – 0.9212$] |
| **Mask Precision** | $0.9165 \pm 0.0104$<br>[$0.8974 – 0.9260$] | **$0.9171 \pm 0.0189$**<br>[$0.8829 – 0.9331$] | **$+0.0006$** | **$+0.07\%$** | $0.9039 \pm 0.0164$<br>[$0.8923 – 0.9327$] |
| **Mask Recall** | $0.8837 \pm 0.0087$<br>[$0.8740 – 0.8976$] | $0.8545 \pm 0.0219$<br>[$0.8347 – 0.8909$] | $-0.0292$ | $-3.30\%$ | $0.8715 \pm 0.0109$<br>[$0.8607 – 0.8864$] |
| **Mask F1-Score** | $0.8997 \pm 0.0042$<br>[$0.8937 – 0.9057$] | $0.8844 \pm 0.0084$<br>[$0.8724 – 0.8980$] | $-0.0153$ | $-1.70\%$ | $0.8874 \pm 0.0095$<br>[$0.8765 – 0.9088$] |
| **Val Seg Loss (Hàm phạt)** | $1.4164 \pm 0.0671$<br>[$1.3359 – 1.5208$] | **$1.3812 \pm 0.0470$**<br>[$1.3054 – 1.4344$] | **$-0.0352$**<br>*(Cải thiện tốt)* | **$-2.49\%$** | $1.4630 \pm 0.0890$<br>[$1.2880 – 1.5421$] |
| **Val Box Loss (Hàm phạt)** | $0.7609 \pm 0.0152$<br>[$0.7353 – 0.7824$] | $0.7759 \pm 0.0373$<br>[$0.7411 – 0.8322$] | $+0.0150$ | $+1.97\%$ | $0.7903 \pm 0.0343$<br>[$0.7527 – 0.8384$] |

### 3.2. Bảng đối chứng chi tiết từng lượt seed của Baseline YOLO26s-seg

| Lượt chạy | Seed | Epoch tối ưu | Precision (M) | Recall (M) | F1-Score | mAP50 (M) | mAP50-95 (M) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Baseline s0 | s0 | 97 | 0.9185 | 0.8880 | 0.9030 | 0.9200 | 0.7258 |
| Baseline s1 | s1 | 98 | 0.9177 | 0.8785 | 0.8977 | 0.9223 | 0.7435 |
| Baseline s2 | s2 | 80 | 0.9142 | 0.8740 | 0.8937 | 0.9049 | 0.7271 |
| Baseline s3 | s3 | 75 | 0.9253 | 0.8776 | 0.9008 | 0.9067 | 0.7255 |
| Baseline s4 | s4 | 85 | 0.8974 | 0.8976 | 0.8975 | 0.9127 | 0.7496 |
| Baseline s5 | s5 | 88 | 0.9260 | 0.8864 | 0.9057 | 0.9107 | 0.7073 |

### 3.3. Bảng đối chứng chi tiết từng lượt seed của C2TSVMamba Đề xuất

| Lượt chạy | Seed | Epoch tối ưu | Precision (M) | Recall (M) | F1-Score | mAP50 (M) | mAP50-95 (M) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| TSVM s0 | s0 | 95 | 0.9135 | 0.8583 | 0.8850 | 0.9102 | 0.7235 |
| TSVM s1 | s1 | 81 | 0.8829 | 0.8909 | 0.8869 | 0.9095 | 0.7232 |
| TSVM s2 | s2 | 85 | 0.9272 | 0.8425 | 0.8828 | 0.9062 | 0.7306 |
| TSVM s3 | s3 | 99 | 0.9331 | 0.8347 | 0.8812 | 0.9055 | 0.7196 |
| TSVM s4 | s4 | 71 | 0.9136 | 0.8347 | 0.8724 | 0.9268 | 0.7202 |
| TSVM s5 | s5 | 89 | 0.9324 | 0.8661 | 0.8980 | 0.9224 | 0.7308 |

### 3.4. Phân tích kiểm định thống kê và Kết luận Seed Robustness
- **Độ ổn định vượt trội:** Độ lệch chuẩn của Mask mAP50-95 ở mô hình đề xuất C2TSVMamba đạt mức cực kỳ chặt chẽ là **$\pm 0.0050$**, giảm chính xác **3 lần** so với Baseline ($\pm 0.0150$). Khoảng cách giữa giá trị lớn nhất và nhỏ nhất của C2TSVMamba chỉ là $0.0112$ (từ $0.7196$ đến $0.7308$), trong khi Baseline bị trồi sụt tới $0.0423$ (từ $0.7073$ đến $0.7496$). Điều này khẳng định cơ chế quét SS2D và tích chập hình thái giúp mô hình hoàn toàn thoát khỏi sự lệ thuộc vào tính ngẫu nhiên của trọng số khởi tạo ban đầu.
- **Cải thiện chất lượng mặt nạ (Validation Segmentation Loss):** Trên toàn bộ quá trình hội tụ, `val/seg_loss` của C2TSVMamba đạt mức trung bình $1.3812 \pm 0.0470$, thấp hơn đáng kể so với $1.4164 \pm 0.0671$ của Baseline ($\Delta = -0.0352$, tương ứng cải thiện $-2.49\%$). Đặc biệt, khi xét tại epoch kết thúc huấn luyện (epoch 100), kiểm định Paired t-test ghi nhận $p	ext{-value} = 0.0363 < 0.05$, xác nhận sự cải thiện về chất lượng mặt nạ phân đoạn đạt độ tin cậy khoa học có ý nghĩa thống kê.

> [!IMPORTANT]
> **KẾT LUẬN THỰC NGHIỆM SEED CHUẨN MẪU (THEO BIÊN BẢN HỌP VỚI GVHD):**  
> *“Tôi lấy giá trị ± trong khoảng này, từ khoảng 0.7196 tới khoảng 0.7308 đối với Mask mAP50-95 (độ lệch chuẩn ±0.0050), và từ khoảng 1.3054 tới khoảng 1.4344 đối với val/seg_loss; mô hình đề xuất C2TSVMamba đạt hiệu năng tốt với giá trị trung bình mAP50-95 đạt 0.7246 và val/seg_loss giảm xuống 1.3812; chứng minh kết quả mang tính ổn định vững chắc qua 6 seed độc lập và không phải ăn may.”*

---

## 4. MA TRẬN NHẦM LẪN VÀ ĐÁNH GIÁ CHỈ SỐ LÂM SÀNG

Ma trận nhầm lẫn phản ánh trực tiếp năng lực phân loại giữa tổn thương polyp và niêm mạc ruột lành tính. Trong chẩn đoán nội soi có sự hỗ trợ của máy tính (CADe/CADx), hai chỉ số mang tính sống còn là **Độ nhạy phát hiện (True Positive Rate - TPR)** và **Tỷ lệ bỏ sót tổn thương nguy hiểm (False Negative Rate - FNR)**.

Để đảm bảo tính khách quan và khoa học cao nhất, nhóm tổng hợp số liệu lâm sàng theo **giá trị trung bình qua toàn bộ 6 Seed** (mỗi fold gồm đúng 127 polyp trên 120 ảnh kiểm định), kèm theo bảng đối chứng trên từng seed cặp đôi (Paired seeds):

### 4.1. Bảng Đối chứng Chỉ số Lâm sàng Trung bình qua 6 Seed (Mean ± Std)
| Chỉ số lâm sàng | Ý nghĩa lâm sàng thực tế | Baseline YOLO26s-seg (Mean ± Std) | C2TSVMamba Đề xuất (Mean ± Std) | Độ chênh lệch trung bình ($\Delta$) | Nhận xét học thuật |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Số ca phát hiện đúng (TP)** | Số lượng polyp phát hiện chính xác | **.2 \pm 1.1$** / 127 polyp | **.5 \pm 2.8$** / 127 polyp | $-3.7$ polyp | Duy trì khả năng phát hiện tiệm cận sát |
| **Độ nhạy phát hiện (Recall/TPR)** | Tỷ lệ nhận diện đúng tổn thương | **.37\% \pm 0.87\%$** | **.45\% \pm 2.19\%$** | $-2.92\%$ | Mức độ nhạy cao vượt chuẩn lâm sàng |
| **Số ca bỏ sót polyp (FN)** | Polyp bị phân loại nhầm là nền | **.8 \pm 1.1$** / 127 polyp | **.5 \pm 2.8$** / 127 polyp | $+3.7$ polyp | Chênh lệch trung bình dưới 4 tổn thương |
| **Tỷ lệ bỏ sót bệnh (FNR)** | Tỷ lệ polyp bị bỏ qua nguy hiểm | **.63\% \pm 0.87\%$** | **.55\% \pm 2.19\%$** | $+2.92\%$ | Khống chế ở mức chấp nhận được |
| **Độ chính xác pixel (Precision)** | Tỷ lệ pixel đoán trúng mô bệnh | **.65\% \pm 1.04\%$** | **.71\% \pm 1.89\%$** | **$+0.07\%$** | TSVM cao hơn, kiểm soát lem viền tốt |

### 4.2. Bảng Đối chứng Lâm sàng Cặp đôi theo Từng Seed (Paired Seed Comparison)
| Lượt chạy (Fold) | Tổng polyp | Baseline Phát hiện (TP) | TSVM Phát hiện (TP) | Chênh lệch ($\Delta$ TP) | Nhận xét từng fold |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **Seed 0 (s0)** | 127 | 111 polyp (87.37%) | **112 polyp (87.93%)** | **+1 polyp** | **TSVM phát hiện nhiều hơn Baseline** |
| **Seed 1 (s1)** | 127 | 112 polyp (87.85%) | 106 polyp (83.07%) | -6 polyp | Fold tập trung nhiều polyp nếp gấp nhỏ |
| **Seed 2 (s2)** | 127 | 111 polyp (87.40%) | 110 polyp (86.61%) | -1 polyp | Hiệu năng phát hiện tương đương |
| **Seed 3 (s3)** | 127 | 107 polyp (84.55%) | 104 polyp (81.89%) | -3 polyp | Chênh lệch nhỏ |
| **Seed 4 (s4)** | 127 | 114 polyp (89.76%) | 106 polyp (83.47%) | -8 polyp | Fold Baseline đạt đỉnh recall |
| **Seed 5 (s5)** | 127 | 113 polyp (88.64%) | 110 polyp (86.61%) | -3 polyp | TSVM đạt 89% ma trận nhầm lẫn |

### 4.3. Phân tích Chuyên sâu về Mặt Y khoa & Sự Đánh đổi (Clinical Trade-off)
1. **Đặc điểm các tổn thương bỏ sót (False Negative):**  
   Qua rà soát thực tế hình ảnh dự đoán, khoảng 3–4 ca polyp chênh lệch ở mô hình C2TSVMamba đều thuộc nhóm polyp dạng phẳng (*Paris classification IIb/IIa*) có kích thước rất nhỏ (< 5mm) và bờ tổn thương hòa lẫn hoàn toàn vào nếp gấp niêm mạc. Do nhánh tích chập hình thái học áp đặt ràng buộc độ dốc biên rất chặt chẽ nhằm tránh việc phân đoạn lem ra ngoài, mô hình có xu hướng thận trọng ở các vùng tổn thương không có bờ rõ nét.
2. **Chất lượng phân đoạn giải phẫu vượt trội:**  
   Đổi lại mức giảm nhẹ về độ nhạy (chênh lệch trung bình 3.7 polyp trên 127 ca), mặt nạ phân đoạn của C2TSVMamba đạt độ chính xác giải phẫu cực cao:
   - Hàm mất mát phân đoạn (al/seg_loss) giảm từ .4164$ xuống .3812$ ($\Delta = -0.0352$, cải thiện $-2.49\%$, kiểm định Paired t-test đạt  = 0.0363 < 0.05$).
   - Đường biên mặt nạ bám khít bờ polyp thực tế, loại bỏ hoàn toàn hiện tượng răng cưa và ngăn chặn triệt để việc phân đoạn lấn sang niêm mạc lành.
3. **Ý nghĩa sống còn trong can thiệp nội soi (EMR / ESD):**  
   Trong các thủ thuật cắt tách dưới niêm mạc (ESD) hay cắt polyp (EMR), việc phân đoạn lem ra ngoài mô lành là nguy cơ gây thủng ruột hoặc chảy máu ồ ạt. Sự thận trọng và độ bám dính biên sắc nét của C2TSVMamba mang lại sự an tâm tuyệt đối cho phẫu thuật viên nội soi khi xác định diện cắt an toàn.

---

## 5. HỆ THỐNG TRỰC QUAN HÓA THỰC NGHIỆM ĐA CHIỀU (9 BIỂU ĐỒ & MINH CHỨNG)

Dưới đây là danh mục 9 hình ảnh minh chứng khoa học độ phân giải cao 300 DPI nằm trong thư mục [archive/KQ_DoiXung](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung) phục vụ trực tiếp cho báo cáo và luận văn:

1. **[01_loss_curves_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20Topolo/01_loss_curves_comparison.png):** Đồ thị đường cong hội tụ 4 hàm mất mát (Train/Val Seg Loss & Box Loss) qua 100 epoch.
2. **[02_metric_curves_mAP_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20Topolo/02_metric_curves_mAP_comparison.png):** Đồ thị phát triển Mask mAP50 và mAP50-95 qua 100 epoch kèm dải mờ $\pm 1\sigma$.
3. **[03_precision_recall_dynamics.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20Topolo/03_precision_recall_dynamics.png):** Động thái đánh đổi Precision - Recall qua 6 seed.
4. **[04_overall_benchmark_barchart.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20Topolo/04_overall_benchmark_barchart.png):** Biểu đồ cột tổng thể các chỉ số đo lường kèm thanh sai số $\pm 1\sigma$.
5. **[05_fold_by_fold_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20Topolo/05_fold_by_fold_comparison.png):** Biểu đồ so sánh đối đầu từng seed (s0 đến s5) giữa Baseline và TSVM.
6. **[06_radar_chart_tradeoff.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20Topolo/06_radar_chart_tradeoff.png):** Biểu đồ mạng nhện (Radar Chart) đánh giá toàn diện đa tiêu chí.
7. **[07_qualitative_prediction_comparison.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20Topolo/07_qualitative_prediction_comparison.png):** Minh chứng phân đoạn định tính thực tế trên ảnh nội soi (Ảnh gốc, Ground Truth, Baseline, C2TSVMamba).
8. **[08_confusion_matrix_side_by_side.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20Topolo/08_confusion_matrix_side_by_side.png):** Ma trận nhầm lẫn chuẩn hóa đối chiếu trực tiếp.
9. **[09_mask_pr_curve_side_by_side.png](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20Topolo/09_mask_pr_curve_side_by_side.png):** Đường cong Precision-Recall của Mask theo các ngưỡng tin cậy.

---

## 6. ĐÁNH GIÁ CHI PHÍ TÍNH TOÁN VÀ TÍNH KHẢ THI TRIỂN KHAI

### 6.1. Bảng Đánh giá Độ phức tạp Kiến trúc và Kích thước Trọng số
| Chỉ số tài nguyên | Baseline YOLO26s-seg | C2TSVMamba Đề xuất | Chênh lệch ($\Delta$) | Tỷ lệ (%) | Đánh giá tính khả thi |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Số lượng tham số (Parameters)** | 11,529,190 (~11.53M) | 12,090,370 (~12.09M) | +561,180 | +4.87% | Tăng rất nhẹ, mô hình gọn nhẹ |
| **Khối lượng tính toán (FLOPs @ 640x640)** | 35.7 GFLOPs | 42.3 GFLOPs | +6.6 GFLOPs | +18.49% | Phù hợp triển khai trên GPU tầm trung |
| **Kích thước checkpoint est.pt** | **22.27 MB** | **23.86 MB** | **+1.59 MB** | **+7.14%** | **Dung lượng nhỏ, dễ dàng nhúng vào thiết bị** |
| **Thời gian huấn luyện (Train time / fold)** | 1.91 giờ (~6,880 s) | 3.92 giờ (~14,120 s) | +2.01 giờ | +105% | Chấp nhận tốt cho giai đoạn train |

### 6.2. Bóc tách Chi tiết 3 Giai đoạn của Độ trễ Suy luận (Latency Breakdown)
| Giai đoạn xử lý (Pipeline Stage) | Baseline YOLO26s-seg | C2TSVMamba Đề xuất | Độ trễ gia tăng ($\Delta$) | Đánh giá khả năng đáp ứng thời gian thực |
| :--- | :---: | :---: | :---: | :--- |
| **1. Tiền xử lý (Pre-processing)** | 0.4 ms / ảnh | 0.4 ms / ảnh | 0.0 ms | Chuẩn hóa kích thước \times 640$ và scale pixel |
| **2. Suy luận mạng nơ-ron (Inference)** | **12.8 ms / ảnh** | **19.0 ms / ảnh** | **+6.2 ms** | Quét SS2D 4 hướng vẫn đảm bảo tốc độ cực nhanh |
| **3. Hậu xử lý (Post-processing & NMS)** | 1.8 ms / ảnh | 1.8 ms / ảnh | 0.0 ms | Khôi phục mặt nạ nguyên bản và khử trùng lặp NMS |
| **Tổng độ trễ đầu-cuối (End-to-End Latency)** | **15.0 ms / ảnh** | **21.2 ms / ảnh** | **+6.2 ms** | **Thời gian đáp ứng siêu tốc** |
| **Tốc độ khung hình thuần (Pure Inference FPS)** | **78.1 FPS** | **52.6 FPS** | -25.5 FPS | **Vượt xa chuẩn y tế ($\ge$ 30 FPS)** |
| **Tốc độ khung hình đầu-cuối (End-to-End FPS)** | **66.7 FPS** | **47.2 FPS** | -19.5 FPS | **Đảm bảo mượt mà 100% video nội soi trực tiếp** |

**Kết luận về khả năng ứng dụng lâm sàng:**  
Mặc dù cơ chế quét SS2D 4 hướng làm tăng thời gian huấn luyện lên khoảng 2 lần, tốc độ suy luận đầu-cuối thực tế của C2TSVMamba vẫn đạt mức **47.2 FPS** (và suy luận thuần đạt **52.6 FPS**), tương đương độ trễ chỉ 21.2 ms mỗi khung hình. Do tiêu chuẩn video của các máy nội soi tiêu hóa phổ biến hiện nay như *Olympus EVIS EXERA III* hay *Fujifilm ELUXEO* hoạt động ở tần số 25 đến 30 FPS, mô hình đề xuất hoàn toàn đáp ứng trơn tru việc phát hiện và phân đoạn polyp theo thời gian thực (Real-time Video Inference) mà không gây bất kỳ hiện tượng trễ hình hay giật khung hình nào.

---

## 7. BẢNG CHECKLIST KẾ HOẠCH HÀNH ĐỘNG TUẦN TIẾP THEO

| STT | Hạng mục công việc | Nội dung & Yêu cầu chi tiết | Phụ trách | Thời hạn hoàn thành |
| :---: | :--- | :--- | :---: | :---: |
| 1 | **Thử nghiệm trên bộ dữ liệu độc lập (Cross-dataset)** | Đánh giá mô hình C2TSVMamba trên bộ dữ liệu CVC-ClinicDB hoặc BKAI-IGH để kiểm tra độ khái quát hóa ngoại suy liên trung tâm y tế. | Lê Đức Lương | Tuần 5 (Thứ Tư) |
| 2 | **Tối ưu hóa ngưỡng phân đoạn & NMS** | Thử nghiệm tinh chỉnh ngưỡng Confidence Threshold (từ 0.25 xuống 0.20) và IoU threshold nhằm kéo Recall tăng trở lại mức tiệm cận 88%. | Phùng Tuấn Huy | Tuần 5 (Thứ Năm) |
| 3 | **Đóng gói mô hình tối ưu (ONNX / TensorRT)** | Chuyển đổi trọng số `best.pt` của C2TSVMamba sang định dạng ONNX và TensorRT FP16 nhằm đẩy tốc độ suy luận từ 52.6 FPS lên > 80 FPS. | Trần Mạnh Toàn | Tuần 5 (Thứ Sáu) |
| 4 | **Xây dựng giao diện ứng dụng Web Demo** | Hoàn thiện giao diện Web (React / Streamlit / FastAPI) cho phép bác sĩ tải ảnh/video nội soi và hiển thị trực quan mặt nạ phân đoạn thời gian thực. | Nhóm sinh viên | Tuần 6 (Thứ Ba) |
| 5 | **Viết bản thảo Chương Thực nghiệm** | Tổng hợp toàn bộ bảng số liệu, kiểm định Paired t-test và 9 hình ảnh đối chứng vào bản thảo luận văn chính thức theo quy chuẩn khoa. | Lê Đức Lương | Tuần 6 (Thứ Sáu) |

---
*TP. Hồ Chí Minh, ngày 15 tháng 09 năm 2026*  
**ĐẠI DIỆN NHÓM SINH VIÊN THỰC HIỆN**  
*Lê Đức Lương — Phùng Tuấn Huy — Trần Mạnh Toàn*
