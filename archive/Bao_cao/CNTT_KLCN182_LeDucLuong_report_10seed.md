# BÁO CÁO TIẾN ĐỘ THỰC NGHIỆM VÀ KẾT QUẢ NGHIÊN CỨU

> **Đề tài:** Nghiên cứu phương pháp tích hợp Topology-Shape-aware VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng
>
> **Mã đề tài & Phân loại:** CNTT_KLCN182 — Khóa luận Cử nhân ngành CNTT (2026–2027)
>
> **Giảng viên hướng dẫn:** ThS. Phùng Thế Bảo
>
> **Sinh viên thực hiện:** Lê Đức Lương; Phùng Tuấn Huy; Trần Mạnh Toàn

---

## 1. MỤC TIÊU VÀ NHIỆM VỤ BÁO CÁO

Báo cáo này cập nhật kết quả thực nghiệm từ phiên bản báo cáo trước đây sử dụng 6 seed sang hệ thống kiểm thử mở rộng 10 seed. Mục tiêu chính là đánh giá khách quan sự khác biệt giữa **YOLO26s-seg Baseline** và **YOLO26s-seg tích hợp Topology-Shape-aware VMamba (TSVM)** trên cùng cấu hình dữ liệu và quy trình huấn luyện.

Các nhiệm vụ trọng tâm gồm:

1. Chuẩn hóa và tổng hợp kết quả của 20 lần chạy độc lập, gồm 10 seed cho Baseline và 10 seed cho TSVM.
2. So sánh hiệu năng phân đoạn thông qua Mask mAP@50-95, Mask mAP@50, Precision và Recall.
3. Đánh giá hiệu năng phát hiện Bounding Box.
4. Phân tích Validation Segmentation Loss và Best Epoch.
5. Đánh giá độ ổn định của mô hình trước thay đổi random seed thông qua Mean, Standard Deviation, Min, Max và Range.
6. Phân tích seed-by-seed để tránh phụ thuộc vào một lần chạy đơn lẻ.
7. Phân tích Confusion Matrix và khả năng phân biệt ảnh nền âm tính trong cấu hình BG20.
8. Sử dụng kiểm định thống kê để phân biệt chênh lệch số học với chênh lệch có ý nghĩa thống kê.

> **Nguyên tắc báo cáo:** Các nhận xét trong tài liệu này chỉ dựa trên bộ kết quả 10-seed đã được kiểm tra. Chênh lệch về trị số không được tự động diễn giải thành sự vượt trội có ý nghĩa thống kê.

---

## 2. THIẾT LẬP THỰC NGHIỆM

### 2.1. Hai mô hình đối sánh

| Thành phần | Baseline | TSVM |
|---|---|---|
| Kiến trúc cơ sở | YOLO26s-seg | YOLO26s-seg |
| Cấu hình | `yolo26s-seg.pt` | `yolo26s-seg-TopologyShapeVMamba.yaml` |
| Thành phần bổ sung | Không | Nhánh Topology-Shape-aware VMamba |
| Số seed | 10 | 10 |
| Seed | 0–9 | 0–9 |
| Epoch/run | 100 | 100 |
| Tổng số run | 10 | 10 |

Tổng cộng có **20 lần chạy thực nghiệm độc lập**. Metric được trích xuất tại epoch tối ưu (`best.pt`) theo **Mask mAP@50-95**.

### 2.2. Bộ dữ liệu

Thực nghiệm sử dụng cấu hình **Kvasir-SEG với 20% ảnh nền âm tính (`data_bg20.yaml`)**.

Tập validation gồm:

- **160 ảnh** tổng cộng.
- **120 ảnh có polyp**, với **127 đối tượng ground-truth**.
- **40 ảnh nền âm tính `normal-cecum`**, không có polyp.

Việc bổ sung ảnh nền âm tính cho phép đánh giá thêm khả năng hạn chế dự đoán dương tính giả trên những ảnh không chứa polyp.

### 2.3. Nguyên tắc lựa chọn kết quả

Kết quả được tổng hợp từ các `results.csv` của 20 run. Các metric tổng hợp được đối chiếu với dữ liệu nguồn tại đúng `best_epoch`.

**Không sửa raw `results.csv`, checkpoint hoặc dữ liệu nguồn chỉ vì phát hiện khác biệt với một ảnh biểu diễn kết quả.** Trong trường hợp giữa CSV và ảnh xuất có bất nhất, số liệu nguồn đã được kiểm tra được ưu tiên và vấn đề xuất ảnh phải được ghi nhận riêng.

---

## 3. HỆ THỐNG ĐÁNH GIÁ

### 3.1. Nhóm chỉ số phân đoạn

Các chỉ số chính gồm:

- Mask mAP@50-95.
- Mask mAP@50.
- Mask Precision.
- Mask Recall.

Trong đó Mask mAP@50-95 được sử dụng làm tiêu chí chính để xác định epoch tối ưu.

### 3.2. Nhóm chỉ số Bounding Box

- Box mAP@50-95.
- Box mAP@50.
- Box Precision.
- Box Recall.

### 3.3. Validation Loss

Chỉ số **Validation Segmentation Loss** được sử dụng để theo dõi chất lượng tối ưu hóa trên tập validation và mức độ dao động giữa các seed.

### 3.4. Độ ổn định giữa các seed

Đánh giá được thực hiện bằng:

- Mean.
- Standard Deviation (Std).
- Minimum.
- Maximum.
- Range = Max − Min.
- So sánh seed-by-seed.

### 3.5. Kiểm định thống kê

Chênh lệch giữa hai mô hình được trình bày dưới dạng:

- `Δ = TSVM − Baseline`.
- Phần trăm thay đổi.
- p-value.
- Diễn giải theo ngưỡng `α = 0.05`.

---

## 4. KẾT QUẢ THỰC NGHIỆM 10-SEED

### 4.1. So sánh hiệu năng tổng quát

| Nhóm | Metric | Baseline (Mean ± Std) | TSVM (Mean ± Std) | Δ | % thay đổi | p-value | Kết luận tại α=0.05 |
|---|---|---:|---:|---:|---:|---:|---|
| Segmentation | Mask mAP@50-95 | 0.7210 ± 0.0129 | **0.7246 ± 0.0078** | +0.0036 | +0.49% | 0.3839 | Chưa có ý nghĩa thống kê |
| Segmentation | Mask mAP@50 | **0.9119 ± 0.0107** | 0.9062 ± 0.0082 | -0.0056 | -0.62% | 0.2273 | Chưa có ý nghĩa thống kê |
| Segmentation | Mask Precision | 0.9023 ± 0.0339 | **0.9118 ± 0.0246** | +0.0095 | +1.05% | 0.5428 | Chưa có ý nghĩa thống kê |
| Segmentation | Mask Recall | 0.8584 ± 0.0252 | **0.8625 ± 0.0173** | +0.0041 | +0.48% | 0.5907 | Chưa có ý nghĩa thống kê |
| Bounding Box | Box mAP@50-95 | 0.7262 ± 0.0198 | **0.7285 ± 0.0141** | +0.0023 | +0.32% | 0.7152 | Chưa có ý nghĩa thống kê |
| Bounding Box | Box mAP@50 | **0.9011 ± 0.0116** | 0.9006 ± 0.0090 | -0.0004 | -0.05% | 0.9334 | Chưa có ý nghĩa thống kê |
| Bounding Box | Box Precision | 0.8992 ± 0.0326 | **0.9062 ± 0.0251** | +0.0070 | +0.78% | 0.5921 | Chưa có ý nghĩa thống kê |
| Bounding Box | Box Recall | 0.8434 ± 0.0337 | **0.8567 ± 0.0152** | +0.0133 | +1.58% | 0.2674 | Chưa có ý nghĩa thống kê |
| Loss | Val Seg Loss | 1.3045 ± 0.0867 | **1.2424 ± 0.0387** | -0.0622 | -4.76% | 0.0908 | Chưa đạt α=0.05 |
| Training | Best Epoch | 87.3 ± 13.1 | 91.7 ± 4.9 | +4.4 | +5.04% | 0.3149 | Chưa có ý nghĩa thống kê |

**Nhận xét:** Mask mAP@50-95 trung bình của TSVM cao hơn Baseline `0.0036`, tương ứng `+0.49%`. Tuy nhiên, p-value `0.3839` lớn hơn `0.05`, vì vậy kết quả hiện tại chỉ cho thấy một chênh lệch thực nghiệm dương về trị số trung bình, chưa đủ để khẳng định sự khác biệt có ý nghĩa thống kê ở mức α=0.05.

Đối với Mask mAP@50, Baseline có giá trị trung bình cao hơn TSVM. Trong khi đó, Mask Precision, Mask Recall, Box mAP@50-95, Box Precision và Box Recall đều có trị số trung bình cao hơn ở TSVM. Các p-value tương ứng đều lớn hơn 0.05.

### 4.2. Phân tích độ ổn định Mask mAP@50-95

| Metric | Baseline | TSVM |
|---|---:|---:|
| Mean | 0.7210 | 0.7246 |
| Std | 0.0129 | 0.0078 |
| Min | 0.6941 (s3) | 0.7065 (s7) |
| Max | 0.7366 (s0) | 0.7339 (s8) |
| Range | 0.0425 | 0.0273 |

Độ lệch chuẩn Mask mAP@50-95 giảm từ `0.0129` xuống `0.0078`. Biên độ dao động giảm từ `0.0425` xuống `0.0273`. Theo phân tích thống kê của bộ kết quả, độ biến thiên của TSVM giảm khoảng **39.5%** so với Baseline.

Kết quả này mô tả sự phân bố của các lần chạy trong thực nghiệm 10-seed; không sử dụng riêng thống kê Min/Max hoặc Range để suy luận nguyên nhân cơ chế.

### 4.3. Phân tích seed-by-seed

Đối với **Mask mAP@50-95**:

- TSVM có trị số cao hơn Baseline ở **6/10 seed**: s1, s2, s3, s6, s8, s9.
- Baseline cao hơn TSVM ở **4/10 seed**: s0, s4, s5, s7.

Đối với **Mask Precision**:

- TSVM cao hơn ở 5/10 seed.
- Baseline cao hơn ở 5/10 seed.

Đối với **Mask Recall**:

- TSVM cao hơn ở 6/10 seed.
- Baseline cao hơn ở 4/10 seed.

Đối với **Validation Segmentation Loss**:

- TSVM có loss thấp hơn ở 8/10 seed.
- Baseline có loss thấp hơn ở 2/10 seed.

Các thống kê này cho thấy kết quả không nên được đánh giá chỉ từ một seed đơn lẻ.

---

## 5. PHÂN TÍCH VALIDATION SEGMENTATION LOSS

| Chỉ số | Baseline | TSVM | Δ | % thay đổi | p-value |
|---|---:|---:|---:|---:|---:|
| Val Seg Loss | 1.3045 ± 0.0867 | 1.2424 ± 0.0387 | -0.0622 | -4.76% | 0.0908 |

TSVM có Validation Segmentation Loss trung bình thấp hơn Baseline `0.0622`, tương ứng giảm `4.76%`. Đồng thời, Std giảm từ `0.0867` xuống `0.0387`.

Kết quả kiểm định có `p = 0.0908`, lớn hơn ngưỡng `0.05`. Vì vậy, mức giảm quan sát được chưa đạt ngưỡng ý nghĩa thống kê nghiêm ngặt được đặt ra trong báo cáo.

---

## 6. PHÂN TÍCH PRECISION VÀ RECALL

### 6.1. Mask Precision

- Baseline: `0.9023 ± 0.0339`.
- TSVM: `0.9118 ± 0.0246`.
- Δ: `+0.0095`.
- Thay đổi: `+1.05%`.
- p-value: `0.5428`.

### 6.2. Mask Recall

- Baseline: `0.8584 ± 0.0252`.
- TSVM: `0.8625 ± 0.0173`.
- Δ: `+0.0041`.
- Thay đổi: `+0.48%`.
- p-value: `0.5907`.

Kết quả cho thấy cả Precision và Recall trung bình đều tăng ở TSVM, đồng thời độ lệch chuẩn của cả hai chỉ số giảm. Tuy nhiên, các chênh lệch này chưa đạt ý nghĩa thống kê tại α=0.05.

---

## 7. PHÂN TÍCH BOUNDING BOX

| Metric | Baseline | TSVM | Δ | % thay đổi | p-value |
|---|---:|---:|---:|---:|---:|
| Box mAP@50-95 | 0.7262 ± 0.0198 | 0.7285 ± 0.0141 | +0.0023 | +0.32% | 0.7152 |
| Box mAP@50 | 0.9011 ± 0.0116 | 0.9006 ± 0.0090 | -0.0004 | -0.05% | 0.9334 |
| Box Precision | 0.8992 ± 0.0326 | 0.9062 ± 0.0251 | +0.0070 | +0.78% | 0.5921 |
| Box Recall | 0.8434 ± 0.0337 | 0.8567 ± 0.0152 | +0.0133 | +1.58% | 0.2674 |

Box mAP@50-95, Box Precision và Box Recall có trị số trung bình cao hơn ở TSVM. Box mAP@50 giảm rất nhỏ `0.0004`. Tất cả p-value đều lớn hơn 0.05.

---

## 8. CONFUSION MATRIX VÀ KHẢ NĂNG PHÂN BIỆT ẢNH NỀN

Phân tích Confusion Matrix được tổng hợp trên 10 seed, với 127 đối tượng polyp ground-truth và 40 ảnh nền âm tính.

| Chỉ số | Baseline | TSVM |
|---|---:|---:|
| TP trung bình | 110.3 (86.9%) | 111.2 (87.6%) |
| FN trung bình | 16.7 (13.1%) | 15.8 (12.4%) |
| FP trung bình trên ảnh nền | 16.8 (42.0%) | 14.6 (36.5%) |
| TN trung bình trên ảnh nền | 23.2 (58.0%) | 25.4 (63.5%) |

Trong bộ dữ liệu thực nghiệm này, TSVM có FP trung bình thấp hơn Baseline `2.2` trường hợp mỗi lần chạy, đồng thời TN trung bình cao hơn `2.2` trường hợp.

Các con số trên mô tả hiện tượng quan sát được trong tập validation cụ thể và không được diễn giải thành bằng chứng về hiệu quả lâm sàng hoặc khả năng tổng quát hóa ngoài bộ dữ liệu.

### 8.1. Lưu ý về S0, S5 và S8

Trong quá trình xử lý kết quả Kaggle, TSVM seed **s0, s5 và s8** từng gặp sự cố liên quan đến quá trình train/export ảnh. Một số PNG confusion matrix sau khắc phục vẫn không phản ánh đúng số liệu CSV nguồn.

Do đó:

- Không sử dụng riêng PNG lỗi của S0/S5/S8 để kết luận metric CSV sai.
- Các metric CSV của ba seed này vẫn được giữ theo dữ liệu nguồn đã kiểm tra.
- Khi sử dụng hình confusion matrix trong tài liệu, cần phân biệt rõ giữa **số liệu CSV đã xác minh** và **ảnh xuất bị lỗi/không đồng nhất**.

---

## 9. PHÂN TÍCH ĐỘ ỔN ĐỊNH VÀ PHÂN BỐ

### 9.1. Mask mAP@50-95

Baseline có Range `0.0425`, trong khi TSVM có Range `0.0273`. Std tương ứng là `0.0129` và `0.0078`.

### 9.2. Mask Precision

- Baseline: Range `0.1002`, Std `0.0339`.
- TSVM: Range `0.0842`, Std `0.0246`.
- Độ biến thiên giảm khoảng `27.4%` theo phân tích thống kê hiện tại.

### 9.3. Validation Segmentation Loss

- Baseline: Range `0.2479`, Std `0.0867`.
- TSVM: Range `0.1243`, Std `0.0387`.
- Độ biến thiên giảm khoảng `55.4%` theo phân tích hiện tại.

Nhìn tổng thể, các thống kê mô tả cho thấy TSVM có phân bố kết quả tập trung hơn ở một số metric quan trọng. Đây là kết quả về **độ ổn định thực nghiệm giữa các seed**, không phải bằng chứng độc lập về nguyên nhân của sự ổn định.

---

## 10. THẢO LUẬN

### 10.1. Hiệu năng phân đoạn

Mask mAP@50-95 trung bình của TSVM cao hơn Baseline `0.0036` (`+0.49%`). Tuy nhiên, mức chênh lệch này chưa đạt ý nghĩa thống kê với `p=0.3839`.

Đáng chú ý, Mask mAP@50 lại cao hơn ở Baseline. Vì vậy, kết quả 10-seed không cho phép mô tả TSVM là mô hình cải thiện đồng đều trên mọi thước đo phân đoạn.

### 10.2. Độ ổn định

Một đặc điểm nổi bật của bộ kết quả là TSVM có Std và Range thấp hơn đối với Mask mAP@50-95, Mask Precision và Validation Segmentation Loss. Điều này cho thấy kết quả TSVM trong 10 lần khởi tạo có mức phân tán thấp hơn ở các chỉ số được phân tích.

### 10.3. False Positive trên ảnh nền

Trong 40 ảnh nền âm tính `normal-cecum`, TSVM có FP trung bình `14.6`, thấp hơn Baseline `16.8`. TN trung bình tương ứng tăng từ `23.2` lên `25.4`.

Kết quả này là một quan sát đáng chú ý của cấu hình BG20, nhưng cần được kiểm chứng thêm trên các bộ dữ liệu độc lập trước khi suy rộng thành kết luận về khả năng tổng quát hóa.

### 10.4. Ý nghĩa thống kê

Các p-value được báo cáo cho các metric chính đều lớn hơn `0.05`. Vì vậy, các chênh lệch quan sát được cần được diễn giải là **kết quả thực nghiệm trên 10 seed**, thay vì khẳng định rằng TSVM đã tạo ra sự khác biệt có ý nghĩa thống kê chắc chắn.

---

## 11. GIỚI HẠN CỦA THỰC NGHIỆM

1. Tập validation hiện tại gồm 160 ảnh, trong đó 40 ảnh là nền âm tính. Đây vẫn là một quy mô dữ liệu giới hạn đối với việc suy rộng kết quả.
2. Dữ liệu Kvasir-SEG có nguồn gốc từ một tập dữ liệu nội soi cụ thể; khả năng tổng quát hóa sang các trung tâm và thiết bị khác chưa được xác minh trong thực nghiệm này.
3. Chênh lệch Mask mAP@50-95 là `+0.49%` nhưng chưa có ý nghĩa thống kê tại α=0.05.
4. Confusion Matrix của một số seed TSVM có giới hạn về ảnh PNG xuất kết quả; do đó cần phân biệt giữa số liệu CSV đã xác minh và hình ảnh xuất.
5. Kết quả 10 seed phản ánh độ ổn định trong phạm vi thiết lập thực nghiệm hiện tại, không phải bằng chứng đầy đủ về độ ổn định trên mọi điều kiện huấn luyện.

---

## 12. KẾT LUẬN

Thực nghiệm mở rộng từ 6 seed lên **10 seed cho mỗi mô hình**, với tổng cộng **20 lần chạy độc lập**, cung cấp cơ sở đầy đủ hơn để đánh giá YOLO26s-seg Baseline và YOLO26s-seg + TSVM.

Trên bộ thực nghiệm hiện tại, TSVM đạt Mask mAP@50-95 trung bình `0.7246 ± 0.0078`, so với `0.7210 ± 0.0129` của Baseline, tương ứng chênh lệch `+0.0036 (+0.49%)`. Đồng thời, độ phân tán của Mask mAP@50-95 giảm từ `0.0129` xuống `0.0078`, và Range giảm từ `0.0425` xuống `0.0273`.

TSVM cũng có Precision và Recall phân đoạn trung bình cao hơn, Validation Segmentation Loss thấp hơn, cùng số FP trung bình thấp hơn trên nhóm ảnh nền âm tính trong cấu hình BG20. Tuy nhiên, các chênh lệch metric được kiểm định trong bộ dữ liệu hiện tại chưa đạt ngưỡng ý nghĩa thống kê `α=0.05`.

Vì vậy, kết luận phù hợp với dữ liệu hiện tại là: **TSVM cho thấy xu hướng cải thiện ở một số chỉ số và đặc biệt cho thấy mức phân tán thấp hơn giữa các seed trong thực nghiệm 10-seed, nhưng chưa có đủ bằng chứng thống kê để khẳng định sự khác biệt hiệu năng tổng thể so với Baseline là có ý nghĩa thống kê.**

---

## 13. CÔNG VIỆC TIẾP THEO

1. Tiếp tục chuẩn hóa các hình biểu diễn kết quả để bảo đảm nhất quán với CSV nguồn.
2. Hoàn thiện bộ hình Confusion Matrix cho phần báo cáo, đồng thời giữ ghi chú về S0/S5/S8.
3. Đưa bảng Mean ± Std, Min–Max và seed-by-seed vào báo cáo Word theo cấu trúc thống nhất.
4. Khi có điều kiện, kiểm chứng trên các bộ dữ liệu polyp độc lập để đánh giá khả năng tổng quát hóa.
5. Trong các thực nghiệm tiếp theo, tiếp tục giữ quy trình nhiều seed nhằm hạn chế kết luận phụ thuộc vào một lần khởi tạo ngẫu nhiên.

---

## 14. NGUỒN DỮ LIỆU VÀ TÀI LIỆU KẾT QUẢ

Bộ kết quả chính được lưu tại:

`archive/Ket_Qua_V2/KQ_Nen_DX_10seed/`

Các thành phần quan trọng:

- `01_raw_analysis/`: số liệu trích xuất từ 20 `results.csv` và confusion matrix theo seed.
- `02_statistics/`: thống kê Mean ± Std, Min–Max và seed-by-seed.
- `03_metrics/`: phân tích segmentation, bounding box và validation loss.
- `04_confusion_matrix/`: ma trận đếm và phần trăm.
- `05_charts/`: biểu đồ hiệu năng, stability, distribution, correlation và summary.
- `06_reports/summary.md`: báo cáo tổng hợp thống kê 10 seed.
- `06_reports/conclusions.md`: các nhận xét khoa học dựa trên 10 seed.

> **Ghi chú:** File này được xây dựng như bản cập nhật báo cáo từ phiên bản 6-seed trước đây. Các số liệu kết quả trong phần thực nghiệm được lấy từ bộ `KQ_Nen_DX_10seed` đã kiểm tra; không sử dụng lại kết quả 6-seed làm kết quả hiện tại.
