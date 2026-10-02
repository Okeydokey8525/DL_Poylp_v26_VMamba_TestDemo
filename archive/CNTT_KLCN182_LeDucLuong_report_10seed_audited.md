# BÁO CÁO TIẾN ĐỘ THỰC NGHIỆM VÀ KẾT QUẢ NGHIÊN CỨU — BẢN ĐÃ RÀ SOÁT

> **Đề tài:** Nghiên cứu phương pháp tích hợp Topology-Shape-aware VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng
>
> **Mã đề tài:** CNTT_KLCN182
>
> **Giảng viên hướng dẫn:** ThS. Phùng Thế Bảo
>
> **Sinh viên:** Lê Đức Lương; Phùng Tuấn Huy; Trần Mạnh Toàn

---

## 1. MỤC TIÊU VÀ PHẠM VI

Báo cáo cập nhật thực nghiệm từ phiên bản 6-seed lên hệ thống 10-seed, gồm **20 lần chạy độc lập**: 10 seed cho YOLO26s-seg Baseline và 10 seed cho YOLO26s-seg + Topology-Shape-aware VMamba (TSVM).

Mục tiêu là mô tả hiệu năng, độ phân tán giữa các seed, Validation Segmentation Loss, Confusion Matrix và benchmark hiện có. Các kết luận được giới hạn trong phạm vi bộ dữ liệu và phép đo đã xác minh.

> **Nguyên tắc:** Chênh lệch về trị số không được tự động diễn giải thành sự vượt trội có ý nghĩa thống kê hoặc bằng chứng về một cơ chế kiến trúc cụ thể.

---

## 2. THIẾT LẬP THỰC NGHIỆM

### 2.1. Mô hình đối sánh

| Thành phần | Baseline | TSVM |
|---|---|---|
| Kiến trúc cơ sở | YOLO26s-seg | YOLO26s-seg |
| Cấu hình | `yolo26s-seg.pt` | `yolo26s-seg-TopologyShapeVMamba.yaml` |
| Thành phần bổ sung | Không | Nhánh Topology-Shape-aware VMamba |
| Seed | 0–9 | 0–9 |
| Epoch/run | 100 | 100 |
| Số run | 10 | 10 |

Tổng cộng: **20 run**. Metric chính được tổng hợp tại epoch tối ưu theo **Mask mAP@50-95**.

### 2.2. Dataset và cấu hình BG20

Thực nghiệm sử dụng `Kvasir_YOLO_SEG_BG20` với **1.200 ảnh**, gồm 1.000 ảnh Kvasir-SEG gốc và 200 ảnh nền âm tính `normal-cecum`.

Không được diễn giải tên **BG20** thành “20% ảnh nền ở cả train và validation”. Tỷ lệ thực tế được ghi như sau:

| Phạm vi | Số ảnh | Ảnh nền âm tính | Tỷ lệ ảnh nền |
|---|---:|---:|---:|
| Toàn bộ dataset | 1.200 | 200 | **16,67%** |
| Train | Theo cấu hình dataset | — | **15,38%** |
| Validation | 160 | 40 | **25%** |

Validation có **160 ảnh**, gồm:

- 120 ảnh chứa polyp.
- 127 đối tượng polyp ground-truth trong 120 ảnh này.
- 40 ảnh nền âm tính.

**127 là số đối tượng, không phải số ảnh**; vì vậy không cộng 127 + 40 để thành 167 ảnh validation.

---

## 3. KẾT QUẢ 10-SEED

### 3.1. So sánh tổng quát

| Metric | Baseline (Mean ± Std) | TSVM (Mean ± Std) | Δ (TSVM−Baseline) | % thay đổi | p-value |
|---|---:|---:|---:|---:|---:|
| Mask mAP@50-95 | 0.7210 ± 0.0129 | **0.7246 ± 0.0078** | +0.0036 | +0.49% | 0.3839 |
| Mask mAP@50 | **0.9119 ± 0.0107** | 0.9062 ± 0.0082 | -0.0056 | -0.62% | 0.2273 |
| Mask Precision | 0.9023 ± 0.0339 | **0.9118 ± 0.0246** | +0.0095 | +1.05% | 0.5428 |
| Mask Recall | 0.8584 ± 0.0252 | **0.8625 ± 0.0173** | +0.0041 | +0.48% | 0.5907 |
| Box mAP@50-95 | 0.7262 ± 0.0198 | **0.7285 ± 0.0141** | +0.0023 | +0.32% | 0.7152 |
| Box mAP@50 | **0.9011 ± 0.0116** | 0.9006 ± 0.0090 | -0.0004 | -0.05% | 0.9334 |
| Box Precision | 0.8992 ± 0.0326 | **0.9062 ± 0.0251** | +0.0070 | +0.78% | 0.5921 |
| Box Recall | 0.8434 ± 0.0337 | **0.8567 ± 0.0152** | +0.0133 | +1.58% | 0.2674 |
| Val Seg Loss | 1.3045 ± 0.0867 | **1.2424 ± 0.0387** | -0.0622 | -4.76% | 0.0908 |
| Best Epoch | 87.3 ± 13.1 | 91.7 ± 4.9 | +4.4 | +5.04% | 0.3149 |

Tất cả p-value trong bảng đều lớn hơn 0,05. Do đó, các chênh lệch trên được trình bày như **kết quả quan sát được**, chưa phải bằng chứng về khác biệt có ý nghĩa thống kê ở α=0,05.

### 3.2. Seed-by-seed

- **Mask mAP@50-95:** TSVM cao hơn ở 6/10 seed; Baseline cao hơn ở 4/10.
- **Mask Precision:** TSVM 5/10; Baseline 5/10.
- **Mask Recall:** TSVM 6/10; Baseline 4/10.
- **Validation Segmentation Loss:** TSVM thấp hơn ở 8/10 seed; Baseline thấp hơn ở 2/10.

Các tỷ lệ này chỉ mô tả số lần thắng theo từng seed, không tự thân chứng minh tính ưu việt thống kê.

---

## 4. ĐỘ ỔN ĐỊNH MASK mAP@50-95

| Metric | Baseline | TSVM |
|---|---:|---:|
| Mean | 0.7210 | 0.7246 |
| Std | 0.0129 | 0.0078 |
| Min | 0.6941 (s3) | 0.7065 (s7) |
| Max | 0.7366 (s0) | 0.7339 (s8) |
| Range | 0.0425 | 0.0273 |

Std giảm từ `0.0129` xuống `0.0078`, còn Range giảm từ `0.0425` xuống `0.0273`. Đây là mô tả về độ phân tán trong 10 seed hiện tại; không suy diễn nguyên nhân cơ chế từ riêng thống kê này.

---

## 5. VALIDATION SEGMENTATION LOSS

TSVM có Val Seg Loss `1.2424 ± 0.0387`, thấp hơn Baseline `1.3045 ± 0.0867`, với Δ = `-0.0622` (`-4.76%`) và `p=0.0908`.

Vì `p>0.05`, không khẳng định đây là cải thiện có ý nghĩa thống kê ở α=0,05. Đồng thời, không quy trực tiếp chênh lệch loss cho SS2D hoặc một cơ chế quét cụ thể; dữ liệu hiện tại không đủ để chứng minh quan hệ nhân quả đó.

---

## 6. PRECISION, RECALL VÀ BOUNDING BOX

### 6.1. Segmentation

**Mask Precision:** Baseline `0.9023 ± 0.0339`; TSVM `0.9118 ± 0.0246`; Δ `+0.0095`; p=`0.5428`; seed-by-seed **5/10 vs 5/10**.

**Mask Recall:** Baseline `0.8584 ± 0.0252`; TSVM `0.8625 ± 0.0173`; Δ `+0.0041`; p=`0.5907`; seed-by-seed **6/10 vs 4/10**.

### 6.2. Bounding Box

| Metric | Baseline | TSVM | Δ | p-value |
|---|---:|---:|---:|---:|
| Box mAP@50-95 | 0.7262 ± 0.0198 | 0.7285 ± 0.0141 | +0.0023 | 0.7152 |
| Box mAP@50 | 0.9011 ± 0.0116 | 0.9006 ± 0.0090 | -0.0004 | 0.9334 |
| Box Precision | 0.8992 ± 0.0326 | 0.9062 ± 0.0251 | +0.0070 | 0.5921 |
| Box Recall | 0.8434 ± 0.0337 | 0.8567 ± 0.0152 | +0.0133 | 0.2674 |

---

## 7. CONFUSION MATRIX VÀ ẢNH NỀN ÂM TÍNH

Validation gồm **160 ảnh**: 120 ảnh chứa **127 đối tượng polyp** và 40 ảnh nền âm tính.

| Chỉ số | Baseline | TSVM |
|---|---:|---:|
| TP trung bình | 110.3 | 111.2 |
| FN trung bình | 16.7 | 15.8 |
| FP trung bình trên nhóm nền | 16.8 | 14.6 |
| TN trung bình trên nhóm nền | 23.2 | 25.4 |

TP/FN và FP/TN đang dùng các đơn vị mẫu khác nhau trong cách tổng hợp hiện tại: TP/FN đối chiếu với 127 đối tượng polyp, còn FP/TN đối chiếu với 40 ảnh nền. Vì vậy không cộng các ô này để suy ra tổng số ảnh và không diễn giải trực tiếp thành chỉ số chẩn đoán cấp ảnh hoặc lợi ích lâm sàng.

### 7.1. S0, S5 và S8

Một số PNG confusion matrix của TSVM s0/s5/s8 từng bị ảnh hưởng bởi lỗi train/export. Do đó:

- Không dùng PNG lỗi để phủ định metric CSV.
- CSV metric đã kiểm tra tiếp tục là nguồn chính cho phân tích 10 seed.
- Khi đưa hình vào báo cáo phải ghi rõ giới hạn của các PNG liên quan.

---

## 8. EFFICIENCY BENCHMARK

Benchmark hiện có gồm **100 phép đo latency/model** và là phép đo **CPU**, không phải GPU Tesla T4.

| Metric | Baseline | TSVM |
|---|---:|---:|
| Mean latency | 200.12 ms | 821.27 ms |
| P50 | 195.92 ms | 826.09 ms |
| P95 | 218.28 ms | 899.10 ms |
| P99 | 251.67 ms | 908.97 ms |
| FPS tương ứng | 5.00 | 1.22 |

Do chưa có phép đo GPU Tesla T4 được xác minh trong bộ nguồn hiện tại, **không sử dụng** giá trị `19.8 ms / 50.5 FPS` trên Tesla T4 và **không kết luận** rằng TSVM đã được chứng minh chạy thời gian thực trên GPU.

Nếu cần benchmark GPU, phải có phép đo riêng và ghi rõ GPU, input size, batch size, precision, warm-up, backend/engine và phương pháp đo.

---

## 9. THẢO LUẬN

### 9.1. Hiệu năng phân đoạn

TSVM đạt Mask mAP@50-95 trung bình `0.7246`, so với `0.7210` của Baseline, Δ=`+0.0036` (`+0.49%`). TSVM thắng 6/10 seed, nhưng `p=0.3839`. Vì vậy chỉ nên ghi nhận đây là **chênh lệch thực nghiệm dương**, chưa đủ để khẳng định khác biệt có ý nghĩa thống kê.

Mask mAP@50 lại cao hơn ở Baseline, nên không thể mô tả TSVM là cải thiện đồng đều trên mọi metric.

### 9.2. Độ ổn định

TSVM có Std và Range thấp hơn đối với Mask mAP@50-95 trong 10 seed. Đây là một đặc điểm về phân tán quan sát được trong thiết lập hiện tại, không phải bằng chứng độc lập về nguyên nhân kiến trúc.

### 9.3. Validation Loss

Loss trung bình thấp hơn ở TSVM, nhưng `p=0.0908` chưa đạt α=0,05. Không dùng kết quả này để khẳng định cơ chế SS2D, topology-shape hoặc một quan hệ nhân quả cụ thể.

### 9.4. Ảnh nền âm tính

FP trung bình trên nhóm 40 ảnh nền là `16.8` với Baseline và `14.6` với TSVM. Đây là quan sát trên validation hiện tại, không phải bằng chứng trực tiếp về lợi ích lâm sàng hay hiệu quả chẩn đoán cấp ảnh.

---

## 10. GIỚI HẠN

1. Validation hiện tại gồm 160 ảnh, trong đó 40 ảnh nền âm tính.
2. Khả năng tổng quát hóa sang bộ dữ liệu độc lập chưa được xác minh.
3. Chênh lệch Mask mAP@50-95 `+0.49%` chưa đạt ý nghĩa thống kê ở α=0,05.
4. Benchmark hiện có là CPU; chưa có benchmark GPU Tesla T4 được xác minh.
5. Một số PNG confusion matrix TSVM s0/s5/s8 có giới hạn do lỗi xuất ảnh.
6. TP/FN và FP/TN được tổng hợp trên các đơn vị mẫu khác nhau; không dùng để suy ra chỉ số cấp ảnh hoặc lợi ích lâm sàng.
7. Các kết quả 10 seed không đủ để tự thân chứng minh quan hệ nhân quả giữa kiến trúc TSVM và từng thay đổi metric.

---

## 11. KẾT LUẬN

Thực nghiệm 10 seed cho mỗi mô hình, tổng cộng 20 run, cho thấy TSVM có Mask mAP@50-95 trung bình `0.7246 ± 0.0078` so với `0.7210 ± 0.0129` của Baseline, Δ=`+0.0036` (`+0.49%`). TSVM thắng 6/10 seed ở metric này, nhưng `p=0.3839` nên chưa có đủ bằng chứng để khẳng định khác biệt có ý nghĩa thống kê ở α=0,05.

TSVM cũng có một số trị số trung bình cao hơn ở Precision, Recall và các metric Bounding Box, đồng thời Val Seg Loss thấp hơn. Các chênh lệch này được báo cáo như kết quả quan sát được vì các p-value tương ứng chưa đạt 0,05.

Độ phân tán của một số metric, đặc biệt Mask mAP@50-95 và Val Seg Loss, thấp hơn ở TSVM trong 10 seed. Đây là kết quả mô tả về độ ổn định của thực nghiệm hiện tại, không phải kết luận về cơ chế.

Trên nhóm 40 ảnh nền âm tính, FP trung bình là `16.8` với Baseline và `14.6` với TSVM. Kết quả này chỉ được xem là một quan sát trong validation cụ thể và không được chuyển thành kết luận về lợi ích lâm sàng.

**Tổng hợp:** bộ 10-seed hiện tại cho thấy một số xu hướng cải thiện về trị số trung bình và độ phân tán ở TSVM, nhưng bằng chứng thống kê hiện có chưa đủ để khẳng định sự khác biệt hiệu năng tổng thể là có ý nghĩa thống kê.

---

## 12. CÔNG VIỆC TIẾP THEO

1. Chuẩn hóa các hình kết quả theo CSV nguồn.
2. Hoàn thiện Confusion Matrix và giữ ghi chú S0/S5/S8.
3. Nếu cần đánh giá real-time, thực hiện benchmark GPU riêng với cấu hình đo đầy đủ.
4. Đưa Mean ± Std, Min–Max và seed-by-seed vào bản Word.
5. Kiểm chứng trên bộ dữ liệu polyp độc lập khi có điều kiện.
6. Bổ sung ablation study nếu cần kiểm tra giả thuyết về cơ chế kiến trúc.

---

## 13. NGUỒN KẾT QUẢ

Bộ kết quả chính:

`archive/Ket_Qua_V2/KQ_Nen_DX_10seed/`

Các nhóm dữ liệu gồm raw analysis, statistics, metrics, confusion matrix, charts và reports. CSV metric của 20 run là nguồn chính cho các thống kê trong báo cáo; PNG confusion matrix bị lỗi ở một số seed không được dùng để phủ định CSV.

> **Trạng thái:** Đây là bản đã rà soát các lỗi về benchmark, tỷ lệ BG20, đơn vị Confusion Matrix và mức độ diễn giải thống kê/cơ chế được nêu trong đợt audit.