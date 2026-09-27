# BÁO CÁO KẾT LUẬN RÀ SOÁT KHOA HỌC (REVIEWED SCIENTIFIC CONCLUSIONS)
## Phân tích Thực nghiệm 10 Random Seed (Seed 0 - Seed 9) trên Bộ dữ liệu Kvasir-SEG (BG20)

---

### 1. Phạm vi và Nguyên tắc Đánh giá

Tài liệu này đánh giá lại toàn bộ kết luận thực nghiệm từ bộ dữ liệu 10 seed độc lập của 4 mô hình:
1. **YOLO26s-seg Baseline**
2. **YOLO26s-seg + TSVM** (Topology-Shape-aware VMamba)
3. **YOLO26s-seg + P5 Attention VMamba**
4. **YOLO26s-seg + ITS Mamba**

#### Quy tắc học thuật được áp dụng:
* **Không sử dụng các thuật ngữ tuyệt đối hóa**: Tuyệt đối không dùng các từ *"chứng minh"*, *"tốt nhất"*, *"vượt trội"*, *"tối ưu"*, *"vô địch"*.
* **Tách bạch 3 khía cạnh đo lường**:
  - *Hiệu năng trung bình (Performance)*: Phản ánh qua giá trị kỳ vọng (Mean).
  - *Độ ổn định phương sai (Stability)*: Phản ánh qua độ lệch chuẩn (Std), khoảng biến thiên (Range = Max - Min), và phương sai (Variance).
  - *So sánh cặp từng seed (Seed-wise comparison)*: Thống kê số lượng seed mà một mô hình đạt giá trị cao hơn mô hình khác (tỷ lệ thắng/thua). Tỷ lệ thắng theo seed là một quan sát thống kê mẫu, không đồng nhất với khái niệm độ ổn định phương sai.
* **Chuẩn hóa diễn giải thống kê**: Bất kỳ sự khác biệt nào có giá trị $p > 0.05$ trong kiểm định Student's t-test (hoặc Wilcoxon signed-rank test) đều **không có ý nghĩa thống kê** (not statistically significant).
* **Chuẩn hóa diễn giải Ma trận nhầm lẫn (Confusion Matrix)**: Ma trận nhầm lẫn đo lường kết quả phân loại ở ngưỡng phát hiện trên tập ảnh test ($N = 167$ ảnh, gồm 127 polyp và 40 background). Không suy diễn các cơ chế biểu diễn hình học nội tại (như khả năng bảo tồn topology hay biên dạng tế bào) từ ma trận này khi chưa có thực nghiệm định lượng hình học tương ứng.

---

### 2. Tổng hợp Định lượng 10 Seed (Kvasir-SEG BG20)

*Dữ liệu trích xuất từ 10 lần chạy độc lập (Seed 0 đến Seed 9), giữ nguyên toàn bộ giá trị gốc.*

| Mô hình | Box mAP50-95 (Mean ± Std) | Mask mAP50-95 (Mean ± Std) | Mask mAP50 (Mean ± Std) | Precision (Mask) | Recall (Mask) | Validation Loss (Mean ± Std) | Best Epoch (Mean ± Std) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **YOLO26s-seg Baseline** | $0.7816 \pm 0.0104$ | $0.7210 \pm 0.0129$ | $0.8879 \pm 0.0118$ | $0.9023 \pm 0.0339$ | $0.8584 \pm 0.0252$ | $1.7649 \pm 0.0298$ | $88.5 \pm 9.6$ |
| **YOLO26s-seg + TSVM** | $0.7869 \pm 0.0076$ | $0.7246 \pm 0.0078$ | $0.8863 \pm 0.0110$ | $0.9118 \pm 0.0246$ | $0.8625 \pm 0.0173$ | $1.7454 \pm 0.0177$ | $86.8 \pm 10.4$ |
| **YOLO26s-seg + P5 VMamba** | $0.7788 \pm 0.0084$ | $0.7165 \pm 0.0075$ | $0.8756 \pm 0.0121$ | $0.8983 \pm 0.0285$ | $0.8338 \pm 0.0220$ | $1.7582 \pm 0.0199$ | $87.9 \pm 8.2$ |
| **YOLO26s-seg + ITS Mamba** | $0.7801 \pm 0.0125$ | $0.7203 \pm 0.0101$ | $0.8824 \pm 0.0089$ | $0.9205 \pm 0.0268$ | $0.8485 \pm 0.0261$ | $1.7630 \pm 0.0210$ | $88.0 \pm 9.7$ |

---

### 3. Phân tích So sánh Chi tiết: Baseline vs. TSVM

#### 3.1. Về Hiệu năng Trung bình (Performance)
- **Mask mAP50-95**: Giá trị trung bình của TSVM ($0.7246$) cao hơn Baseline ($0.7210$) một khoảng chênh lệch $\Delta = +0.0036$ (tương đương $+0.36$ điểm phần trăm, hoặc mức tăng tương đối $+0.50\%$).
- **Box mAP50-95**: TSVM ($0.7869$) cao hơn Baseline ($0.7816$) một khoảng $\Delta = +0.0053$ ($+0.68\%$).
- **Mask mAP50**: TSVM ($0.8863$) thấp hơn Baseline ($0.8879$) một khoảng $\Delta = -0.0016$ ($-0.18\%$).
- **Precision / Recall**: TSVM ghi nhận Precision trung bình cao hơn Baseline ($0.9118$ so với $0.9023$, $\Delta = +0.0095$) và Recall trung bình cao hơn Baseline ($0.8625$ so với $0.8584$, $\Delta = +0.0041$).

#### 3.2. Về Độ ổn định Phương sai (Stability)
- **Mask mAP50-95**:
  - Độ lệch chuẩn của TSVM đạt $\sigma = 0.0078$, thấp hơn so với Baseline $\sigma = 0.0129$ (mức giảm độ lệch chuẩn là $39.5\%$).
  - Khoảng giá trị (Range = Max - Min): TSVM có biên độ dao động $0.0242$ (từ $0.7135$ đến $0.7377$), hẹp hơn so với Baseline có biên độ dao động $0.0410$ (từ $0.6974$ đến $0.7384$).
  - Phương sai mẫu: TSVM ($6.08 \times 10^{-5}$) thấp hơn Baseline ($1.66 \times 10^{-4}$).
- **Validation Loss**:
  - TSVM có độ lệch chuẩn loss là $\sigma = 0.0177$, thấp hơn so với Baseline $\sigma = 0.0298$ (giảm $40.6\%$).
  - Biên độ dao động loss của TSVM là $0.0526$, hẹp hơn mức $0.0988$ của Baseline.
- **Nhận định khoa học**: Trên mẫu thực nghiệm 10 seed này, cấu hình TSVM thể hiện độ tán xạ kết quả quanh giá trị trung bình thấp hơn so với cấu hình Baseline.

#### 3.3. Về So sánh Cặp từng Seed (Seed-wise Head-to-Head)
- Xét trên từng cặp seed tương ứng ($s \in \{0, 1, \dots, 9\}$):
  - **Mask mAP50-95**: TSVM đạt kết quả cao hơn Baseline ở **6/10 seed** (Seed 0, 1, 2, 4, 6, 8), và thấp hơn ở **4/10 seed** (Seed 3, 5, 7, 9).
  - **Box mAP50-95**: TSVM cao hơn Baseline ở **8/10 seed**.
  - **Validation Loss**: TSVM có giá trị loss thấp hơn Baseline ở **8/10 seed**.
- **Lưu ý chuẩn mực**: Tỷ lệ thắng 6/10 seed cho thấy không có sự áp đảo tuyệt đối ở mọi lần khởi tạo ngẫu nhiên. Đây là hiện tượng bình thường trong huấn luyện mạng nơ-ron sâu với tập dữ liệu y tế quy mô vừa.

#### 3.4. Về Kiểm định Ý nghĩa Thống kê (Statistical Hypothesis Testing)
- **Kiểm định Paired Student's t-test (Baseline vs TSVM trên 10 seed)**:
  - *Mask mAP50-95*: $t = -0.9138$, $p = 0.3839$.
  - *Box mAP50-95*: $t = -1.8906$, $p = 0.0912$.
  - *Validation Loss*: $t = 1.8941$, $p = 0.0908$.
- **Kiểm định phi tham số Wilcoxon Signed-Rank Test**:
  - *Mask mAP50-95*: $W = 19.0$, $p = 0.4316$.
  - *Validation Loss*: $W = 9.0$, $p = 0.1055$.
- **Kết luận học thuật bắt buộc**:
  - Vì tất cả các giá trị $p > 0.05$, **chưa có đủ bằng chứng thống kê để bác bỏ giả thuyết không ($H_0$)** ở mức ý nghĩa tiêu chuẩn $\alpha = 0.05$.
  - Mặc dù TSVM ghi nhận giá trị trung bình cao hơn và phương sai thấp hơn trên mẫu 10 seed, sự chênh lệch hiệu năng mAP không đạt ngưỡng có ý nghĩa thống kê. Trong báo cáo khoa học và luận văn, kết quả này phải được trình bày là: *"TSVM cho thấy xu hướng cải thiện nhẹ về giá trị trung bình và giảm phương sai trên 10 seed thử nghiệm, tuy nhiên sự khác biệt về mặt thống kê chưa đạt mức có ý nghĩa với cỡ mẫu $N=10$ ($p = 0.384$)"*.

---

### 4. Rà soát Phân tích Ma trận Nhầm lẫn (Confusion Matrix)

Dữ liệu ma trận nhầm lẫn tổng hợp trên 10 seed tại ngưỡng đánh giá mặc định ($conf = 0.25$, $IoU = 0.5$):
- Tập kiểm tra gồm $N = 167$ ảnh: 127 ảnh chứa polyp (Ground Truth Positive) và 40 ảnh nền không chứa polyp (Ground Truth Negative: Background).
- Tổng $TP + FN = 127$; Tổng $FP + TN = 40$.

| Mô hình | TP (Mean ± Std) | FN (Mean ± Std) | FP (Mean ± Std) | TN (Mean ± Std) | Sensitivity (Recall) | Specificity |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline** | $112.4 \pm 2.8$ | $14.6 \pm 2.8$ | $13.5 \pm 4.2$ | $26.5 \pm 4.2$ | $88.50\%$ | $66.25\%$ |
| **TSVM** | $113.8 \pm 2.1$ | $13.2 \pm 2.1$ | $11.8 \pm 3.1$ | $28.2 \pm 3.1$ | $89.61\%$ | $70.50\%$ |
| **P5 VMamba** | $109.8 \pm 2.6$ | $17.2 \pm 2.6$ | $13.9 \pm 3.7$ | $26.1 \pm 3.7$ | $86.46\%$ | $65.25\%$ |
| **ITS Mamba** | $111.1 \pm 3.2$ | $15.9 \pm 3.2$ | $10.6 \pm 3.3$ | $29.4 \pm 3.3$ | $87.48\%$ | $73.50\%$ |

#### Rà soát diễn giải học thuật:
- **Quan sát số liệu thực tế**:
  - TSVM nhận diện đúng trung bình thêm khoảng $1.4$ ca polyp ($TP = 113.8$ so với $112.4$) và giảm trung bình $1.7$ ca dương tính giả trên ảnh nền ($FP = 11.8$ so với $13.5$).
  - ITS Mamba đạt mức dương tính giả thấp nhất trên tập nền ($FP = 10.6 \pm 3.3$, Specificity $73.50\%$).
- **Điều chỉnh diễn giải (Tránh suy diễn nguyên nhân)**:
  - *Không được viết*: "Điều này chứng minh nhánh Shape-aware giúp mô hình nắm bắt được cấu trúc hình học của polyp và loại bỏ ảnh giả."
  - *Cách viết đúng chuẩn học thuật*: "Về mặt số lượng phát hiện ở cấp độ ảnh, TSVM ghi nhận tỷ lệ True Positive trung bình cao hơn ($89.61\%$ so với $88.50\%$) và tỷ lệ False Positive trên ảnh nền thấp hơn ($11.8$ so với $13.5$) so với Baseline trên tập test gồm 167 ảnh. Cơ chế đóng góp của các thành phần kiến trúc cần được kiểm chứng thêm thông qua các phân tích ablation và trực quan hóa bản đồ đặc trưng."

---

### 5. Tóm tắt Đánh giá 4 Mô hình (10 Seed)

1. **YOLO26s-seg Baseline**:
   - Hoạt động như mốc chuẩn đối sánh cơ sở.
   - Thể hiện độ nhạy tốt (Recall $0.8584$), nhưng có độ phân tán hiệu năng lớn nhất giữa các seed ($\sigma_{mAP} = 0.0129$, Range $0.0410$).
2. **YOLO26s-seg + TSVM**:
   - Đạt Mask mAP50-95 trung bình cao nhất trong 4 mô hình ($0.7246$).
   - Thể hiện sự thu hẹp phương sai và độ lệch chuẩn ($\sigma = 0.0078$) so với Baseline trên cùng 10 seed.
   - Khác biệt hiệu năng so với Baseline không đạt mức ý nghĩa thống kê ($p = 0.384$).
3. **YOLO26s-seg + P5 Attention VMamba**:
   - Ghi nhận Mask mAP50-95 trung bình đạt $0.7165 \pm 0.0075$ (thấp hơn Baseline $0.0045$).
   - Recall trung bình đạt $0.8338$, thấp hơn so với Baseline ($0.8584$) và TSVM ($0.8625$).
   - Kết quả chỉ ra rằng việc tích hợp cơ chế VMamba chỉ ở mức tầng P5 dưới dạng attention đơn lẻ chưa mang lại sự cải thiện hiệu năng phân vùng trên bộ dữ liệu này.
4. **YOLO26s-seg + ITS Mamba**:
   - Ghi nhận Mask mAP50-95 trung bình đạt $0.7203 \pm 0.0101$, tương đương với mức của Baseline ($0.7210$).
   - Đạt Precision trung bình cao nhất ($0.9205 \pm 0.0268$) và số ca FP trên ảnh nền thấp nhất ($10.6$), nhưng có Recall trung bình thấp hơn ($0.8485$ so với $0.8584$).
