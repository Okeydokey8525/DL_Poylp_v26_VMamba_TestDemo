# DL_Poylp_v26_VMamba_TestDemo

## Nghiên cứu tích hợp VMamba vào YOLO26-seg cho phân đoạn polyp đại trực tràng

Repository này phục vụ khóa luận:

> **Nghiên cứu phương pháp tích hợp VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng.**

Dự án tập trung vào **nghiên cứu kiến trúc, dữ liệu và thực nghiệm mô hình**. Phần web hoặc ứng dụng di động trong tương lai chỉ dùng để **minh họa kết quả nghiên cứu**, không phải phần mềm chẩn đoán y tế và không thay thế đánh giá của bác sĩ.

---

## 1. Tình trạng repository hiện tại

Repository hiện được sử dụng chủ yếu để lưu:

- dữ liệu và các tệp hỗ trợ tiền xử lý Kvasir-SEG;
- kết quả huấn luyện YOLO26-seg baseline;
- kết quả huấn luyện YOLO26-VMamba-seg;
- báo cáo kiểm toán kết quả;
- cấu hình, biểu đồ, log và trọng số của các run đã thực hiện.

### Lưu ý quan trọng

Hai thư mục mã nguồn Ultralytics từng được đưa vào repository đã được xóa để tránh lưu trùng toàn bộ source gốc và làm repository quá lớn.

Vì vậy, phiên bản hiện tại **không chứa đầy đủ source Ultralytics custom để dựng lại mô hình trực tiếp chỉ bằng cách clone repository này**. Khi tiếp tục phát triển, nhóm sẽ:

1. lấy source sạch từ repository chính thức của Ultralytics;
2. cố định phiên bản hoặc commit nền;
3. bổ sung riêng các file thay đổi liên quan đến VMamba;
4. ghi rõ hướng dẫn tích hợp và tái lập thí nghiệm.

README cũ từng mô tả cả source Ultralytics đã bị xóa và chứa bảng kết quả YOLO11 không còn phù hợp với nội dung hiện tại. README này chỉ tổng hợp phần được xác nhận cho **YOLO26-seg và YOLO26-VMamba-seg**.

---

## 2. Mục tiêu nghiên cứu

Các mục tiêu chính của dự án gồm:

1. Khảo sát các phương pháp phân đoạn polyp, kiến trúc YOLO26-seg, State Space Model, Mamba và VMamba.
2. Xây dựng quy trình dữ liệu Kvasir-SEG có thể kiểm tra và tái lập.
3. Huấn luyện YOLO26-seg nguyên bản làm mô hình cơ sở.
4. Nghiên cứu nhiều phương án tích hợp một hoặc nhiều khối Visual State-Space vào backbone hoặc vùng kết hợp đặc trưng đa tỉ lệ.
5. So sánh mô hình đề xuất với YOLO26-seg baseline và ít nhất một mô hình phân đoạn đối chứng.
6. Đánh giá đồng thời chất lượng phân đoạn và chi phí tính toán.
7. Thực hiện ablation study về vị trí tích hợp, số lượng block và cấu hình VMamba.
8. Xây dựng web/app minh họa kết quả của mô hình tốt nhất sau thực nghiệm.

---

## 3. Phạm vi nghiên cứu

### Bài toán

- Đầu vào: ảnh nội soi đại trực tràng.
- Đầu ra: mặt nạ vùng polyp, đường biên, hộp bao và độ tin cậy dự đoán.
- Số lớp: `1` lớp `polyp`.
- Nhiệm vụ chính: instance segmentation.

### Không thuộc phạm vi

Dự án không thực hiện:

- chẩn đoán loại mô bệnh học;
- đánh giá mức độ ác tính;
- tư vấn hoặc khuyến nghị điều trị;
- triển khai lâm sàng trong bệnh viện;
- sử dụng ứng dụng minh họa để thay thế bác sĩ.

---

## 4. Dữ liệu Kvasir-SEG

Dữ liệu chính là **Kvasir-SEG**, gồm ảnh nội soi và mặt nạ phân đoạn mức điểm ảnh.

Giao thức hiện tại:

| Tập dữ liệu | Số ảnh |
|---|---:|
| Train | 880 |
| Validation | 120 |
| Tổng | 1.000 |

Repository sử dụng split cố định `880/120` để các mô hình được huấn luyện và đánh giá trong cùng điều kiện.

### Tiền xử lý

File chính:

```text
archive/convert_kvasir_to_yolo_seg.py
```

Script này thực hiện các công việc như:

- tìm ảnh và mask Kvasir-SEG;
- chuẩn hóa mặt nạ;
- dùng threshold để tách vùng polyp;
- làm sạch mask bằng phép toán hình thái;
- trích contour;
- đơn giản hóa polygon;
- chuyển nhãn sang định dạng YOLO segmentation;
- thống kê đặc điểm vùng polyp;
- tạo ảnh preview kiểm tra nhãn;
- tạo biểu đồ và tệp tổng hợp dữ liệu.

Định dạng đầu ra dự kiến:

```text
Kvasir_YOLO_SEG/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── dataset.yaml
```

---

## 5. Các mô hình trong thực nghiệm hiện tại

### 5.1. YOLO26-seg baseline

Đã huấn luyện các scale:

- YOLO26n-seg;
- YOLO26s-seg;
- YOLO26m-seg;
- YOLO26l-seg;
- YOLO26x-seg.

Baseline được dùng để:

- kiểm tra dữ liệu;
- tạo mốc so sánh;
- đánh giá ảnh hưởng thực sự của VMamba;
- so sánh độ chính xác, số tham số và tốc độ.

### 5.2. YOLO26-VMamba-seg

Phiên bản VMamba đã thử nghiệm trong các run hiện tại sử dụng một khối Visual State-Space tích hợp vào phần đặc trưng sâu của YOLO26-seg.

Cấu hình tham chiếu đã thử:

```text
YOLO26-seg backbone
→ C2PSA
→ VMambaBlock
→ neck đa tỉ lệ
→ Segment26 head
```

Khối VMamba trong phương án này hướng đến:

- khai thác quan hệ không gian dài;
- kết hợp ngữ cảnh toàn cục;
- xử lý feature map hai chiều bằng selective scan;
- giữ đầu ra tương thích với neck và segmentation head.

Đây chỉ là **một phương án tích hợp đã thử nghiệm**, không phải vị trí duy nhất hoặc kiến trúc cuối cùng của đề tài. Các hướng khác như tích hợp tại tầng trung gian của backbone hoặc trong neck vẫn cần được nghiên cứu và ablation.

---

## 6. Kết quả huấn luyện đã xác nhận

Các kết quả dưới đây được tổng hợp từ:

```text
archive/training_results_audit.md
```

Tất cả run sử dụng Kvasir-SEG với split `880 train / 120 validation`, ảnh đầu vào `640 × 640` và 100 epoch.

| STT | Dòng mô hình | Run | Mask mAP50 | Mask mAP50-95 | Best epoch |
|---:|---|---|---:|---:|---:|
| 1 | Baseline | `Kvasir_YOLO26n_seg_100e_16b` | 0.9141 | 0.7238 | 89 |
| 2 | Baseline | `Kvasir_YOLO26s_seg_100e_16b` | **0.9282** | **0.7280** | 94 |
| 3 | Baseline | `Kvasir_YOLO26m_seg_100e_16b` | 0.9164 | 0.7084 | 80 |
| 4 | Baseline | `Kvasir_YOLO26l_seg_100e_16b` | 0.9169 | 0.7215 | 82 |
| 5 | Baseline | `Kvasir_YOLO26x_seg_100e_16b` | 0.9203 | 0.7116 | 92 |
| 6 | VMamba | `Kvasir_YOLO26n_VMamba_seg_100e_16b` | 0.8365 | 0.6095 | 100 |
| 7 | VMamba | `Kvasir_YOLO26s_VMamba_seg_100e_16b` | 0.8321 | 0.5883 | 100 |
| 8 | VMamba | `Kvasir_YOLO26m_VMamba_seg_100e_16b` | 0.8122 | 0.5780 | 99 |
| 9 | VMamba | `Kvasir_YOLO26l_VMamba_seg_100e_16b` | 0.8045 | 0.5439 | 76 |
| 10 | VMamba | `Kvasir_YOLO26x_VMamba_seg_100e_16b` | 0.7897 | 0.5449 | 92 |

### Nhận xét hiện tại

- Baseline tốt nhất trong nhóm run hiện có là `YOLO26s-seg`, đạt `Mask mAP50-95 = 0.7280`.
- Các cấu hình VMamba hiện tại đạt `Mask mAP50-95` trong khoảng `0.5439–0.6095`.
- Phương án VMamba hiện tại **chưa cải thiện độ chính xác so với baseline**.
- Một số run VMamba đạt best epoch ở cuối quá trình huấn luyện, cho thấy mô hình có thể hội tụ chậm hoặc cấu hình tích hợp chưa phù hợp.
- Kết quả này là cơ sở để tiếp tục nghiên cứu vị trí chèn, số lượng block, residual scaling, learning rate, warm-up và chiến lược nạp pretrained.

Không được dùng các kết quả trên để tuyên bố rằng VMamba đã nâng cao hiệu quả mô hình. Kết luận đúng ở thời điểm hiện tại là:

> Phương án tích hợp VMamba đã thử nghiệm có thể huấn luyện và đánh giá, nhưng chưa vượt YOLO26-seg baseline.

---

## 7. Đánh giá thực nghiệm

### Chất lượng mặt nạ

Các chỉ số dự kiến sử dụng:

- Dice Score;
- IoU/Jaccard;
- Precision;
- Recall;
- F1-score;
- Mask mAP50;
- Mask mAP50-95.

### Hiệu quả tính toán

- số tham số;
- GFLOPs;
- kích thước trọng số;
- VRAM;
- thời gian huấn luyện;
- latency trên một ảnh;
- FPS.

### Phân tích định tính

Cần phân tích riêng các trường hợp:

- polyp nhỏ;
- polyp phẳng;
- biên mờ;
- màu gần nền;
- phản sáng;
- nhiễu;
- false positive;
- false negative;
- mask co hụt hoặc lấn nền.

---

## 8. Kế hoạch ablation study

### Ablation 1 — Vị trí tích hợp

So sánh các phương án như:

- không dùng VMamba;
- VMamba tại tầng sâu của backbone;
- VMamba tại tầng trung gian của backbone;
- VMamba tại vùng fusion đa tỉ lệ trong neck.

### Ablation 2 — Số lượng block

- 0 block;
- 1 block;
- 2 block.

### Ablation 3 — Cấu hình block

Có thể khảo sát một biến tại một thời điểm, ví dụ:

- residual thường và residual scaling;
- selective scan hai hướng và bốn hướng;
- thay đổi `d_state`;
- có hoặc không có local convolution branch.

### Thí nghiệm mở rộng về scale

Ưu tiên các scale:

- n;
- s;
- m.

Các scale l và x chỉ thực hiện khi tài nguyên cho phép. Khảo sát scale là thí nghiệm mở rộng về quy mô mô hình, không phải ablation chính của VMamba.

---

## 9. Cấu trúc nội dung chính của repository

```text
DL_Poylp_v26_VMamba_TestDemo/
├── README.md
└── archive/
    ├── KQ_Poylp/                       # Artifact các run huấn luyện
    ├── Kvasir-SEG/                     # Dữ liệu Kvasir-SEG gốc nếu được lưu trong repo
    ├── Kvasir_YOLO_SEG/                # Dữ liệu đã chuyển sang YOLO segmentation
    ├── convert_kvasir_to_yolo_seg.py   # Script chuyển mask sang polygon YOLO
    ├── train.txt                       # Danh sách ảnh train
    ├── val.txt                         # Danh sách ảnh validation
    ├── training_results_audit.md       # Báo cáo chính thức của 10 run YOLO26
    └── audit_runs_data.json            # Metadata kiểm toán cũ
```

### Lưu ý về `audit_runs_data.json`

Tệp `archive/audit_runs_data.json` còn chứa metadata lịch sử của một số run YOLO11 từ giai đoạn khảo sát trước. Nội dung này **không phải bảng kết quả chính thức hiện tại của repository**.

Khi xem kết quả chính thức của đề tài ở trạng thái hiện tại, ưu tiên:

```text
archive/training_results_audit.md
```

và các artifact thực tế trong:

```text
archive/KQ_Poylp/
```

---

## 10. Cách sử dụng repository hiện tại

### Đọc kết quả nghiên cứu

1. Đọc `README.md` để xem tổng quan.
2. Đọc `archive/training_results_audit.md` để xem kết quả 10 run đã xác nhận.
3. Mở từng thư mục run trong `archive/KQ_Poylp/` để xem:
   - `args.yaml`;
   - `results.csv`;
   - biểu đồ metric;
   - confusion matrix;
   - ảnh validation;
   - `best.pt` và `last.pt` nếu được lưu.

### Tiền xử lý dữ liệu

Sử dụng:

```bash
python archive/convert_kvasir_to_yolo_seg.py
```

Trước khi chạy cần kiểm tra lại đường dẫn dữ liệu và tham số trong script để phù hợp với máy local hoặc Kaggle.

### Tái lập mô hình

Source custom hiện chưa được lưu đầy đủ trong repository. Để tái lập mô hình, nhóm cần bổ sung trong giai đoạn tiếp theo:

- commit Ultralytics nền;
- module VMamba;
- file đăng ký module;
- YAML mô hình;
- utility chuyển trọng số pretrained;
- notebook hoặc script Kaggle;
- requirements và hướng dẫn môi trường.

---

## 11. Ứng dụng minh họa dự kiến

Ứng dụng chỉ phục vụ nghiên cứu và trình bày kết quả.

Các chức năng dự kiến:

- tải ảnh nội soi;
- chọn mô hình baseline hoặc VMamba;
- hiển thị ảnh gốc;
- hiển thị mask;
- hiển thị contour và overlay;
- hiển thị bounding box;
- hiển thị confidence;
- hiển thị latency;
- so sánh trực quan hai mô hình;
- lưu hoặc tải ảnh kết quả.

Web và ứng dụng di động nên dùng chung một backend suy luận để tránh triển khai hai pipeline mô hình khác nhau.

---

## 12. Hướng phát triển tiếp theo

1. Chuẩn hóa lại cấu trúc repository sau khi xóa source Ultralytics trùng lặp.
2. Lưu riêng các patch hoặc file custom thay vì đưa toàn bộ Ultralytics vào repository.
3. Hoàn thiện ba phương án VMamba độc lập của ba thành viên.
4. Sàng lọc kiến trúc bằng unit test và smoke train.
5. Thực hiện ablation về vị trí, số block và cấu hình block.
6. Huấn luyện ít nhất một mô hình đối chứng như U-Net hoặc PraNet.
7. Tính Dice, IoU và F1-score chung cho các mô hình.
8. Đánh giá ngoài miền trên CVC-ClinicDB, CVC-ColonDB hoặc ETIS-Larib khi có điều kiện.
9. Xây dựng backend inference dùng chung.
10. Hoàn thiện web và app di động minh họa.

---

## 13. Thành viên thực hiện

- **Lê Đức Lương** — MSSV: 2001230490
- **Phùng Tuấn Huy** — MSSV: 2001230312
- **Trần Mạnh Toàn** — MSSV: 2001230830

Giảng viên hướng dẫn: **TS. Phùng Thế Bảo**.

---

## 14. Tuyên bố giới hạn sử dụng

Repository và các ứng dụng liên quan chỉ phục vụ:

- học tập;
- nghiên cứu;
- đánh giá thuật toán;
- trình bày khóa luận.

Kết quả mô hình không được sử dụng như một công cụ chẩn đoán, tiên lượng hoặc quyết định điều trị trong thực tế y tế.
