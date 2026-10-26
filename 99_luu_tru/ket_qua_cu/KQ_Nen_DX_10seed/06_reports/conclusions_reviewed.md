# BÁO CÁO KẾT LUẬN RÀ SOÁT KHOA HỌC (REVIEWED SCIENTIFIC CONCLUSIONS)
## Phân tích Thực nghiệm 10 Random Seed (Seed 0 – Seed 9) trên Bộ dữ liệu Kvasir-SEG (BG20)

---

> 🔴 **GHI CHÚ SỬA ĐỔI (02/10/2026):** Bản nháp trước đây của tài liệu này chứa **bộ số liệu hoàn toàn khác** với kết quả thực nghiệm hiện hành ở các cột Box mAP@50-95, Mask mAP@50, Validation Loss, Best Epoch, danh sách seed thắng, giá trị kiểm định *t*-test/Wilcoxon, trung bình ma trận nhầm lẫn, cùng cỡ mẫu ghi sai "167 ảnh". Ngoài ra bản nháp còn đưa số liệu của **P5 Attention VMamba** và **ITS Mamba** — hai dòng mô hình **không tồn tại trong `Ket_Qua_V2/`** và không thể kiểm chứng. Toàn bộ đã được sửa lại theo số liệu tái trích xuất trực tiếp từ 20 tệp `results.csv` và thu hẹp về **2 mô hình**.

---

### 1. Phạm vi và Nguyên tắc Đánh giá

Tài liệu này đánh giá lại toàn bộ kết luận thực nghiệm từ bộ dữ liệu 10 seed độc lập của **2 mô hình**:

1. **YOLO26s-seg Baseline** (đối chuẩn)
2. **YOLO26s-seg + TSVM** (Topology-Shape-aware VMamba, đề xuất)

#### Quy tắc học thuật được áp dụng:
* **Không sử dụng các thuật ngữ tuyệt đối hóa**: Không dùng các từ *"chứng minh"*, *"tốt nhất"*, *"vượt trội"*, *"tối ưu"*, *"vô địch"*.
* **Tách bạch 3 khía cạnh đo lường**:
  - *Hiệu năng trung bình (Performance)*: Phản ánh qua giá trị kỳ vọng (Mean).
  - *Độ ổn định phương sai (Stability)*: Phản ánh qua độ lệch chuẩn (Std), khoảng biến thiên (Range = Max − Min) và phương sai (Variance).
  - *So sánh cặp từng seed (Seed-wise comparison)*: Thống kê số seed mà một mô hình đạt giá trị tốt hơn. **Không** đồng nhất với khái niệm độ ổn định phương sai.
* **Chuẩn hóa diễn giải thống kê**: Bất kỳ khác biệt nào có $p > 0.05$ trong kiểm định Paired *t*-test hoặc Wilcoxon signed-rank đều **không có ý nghĩa thống kê**.
* **Chuẩn hóa diễn giải Ma trận nhầm lẫn**: Tập kiểm định gồm **160 ảnh** (120 ảnh polyp chứa **127 thực thể** + 40 ảnh nền). Không suy diễn cơ chế biểu diễn hình học nội tại từ ma trận này. **Không được trích dẫn cột TN/Specificity như số đo thực nghiệm** (xem mục 4.3).

---

### 2. Tổng hợp Định lượng 10 Seed (Kvasir-SEG BG20)

*Dữ liệu trích xuất tại epoch tối ưu từ 10 lần chạy độc lập (Seed 0 đến Seed 9). Nguồn: `02_statistics/mean_std/full_comparison_mean_std.csv`.*

| Mô hình | Box mAP50-95 (Mean ± Std) | Mask mAP50-95 (Mean ± Std) | Mask mAP50 (Mean ± Std) | Precision (Mask) | Recall (Mask) | Val Seg Loss (Mean ± Std) | Best Epoch (Mean ± Std) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **YOLO26s-seg Baseline** | $0.7262 \pm 0.0198$ | $0.7210 \pm 0.0129$ | $0.9119 \pm 0.0107$ | $0.9023 \pm 0.0339$ | $0.8584 \pm 0.0252$ | $1.3045 \pm 0.0867$ | $87.3 \pm 13.10$ |
| **YOLO26s-seg + TSVM** | $0.7285 \pm 0.0141$ | $0.7246 \pm 0.0078$ | $0.9062 \pm 0.0082$ | $0.9118 \pm 0.0246$ | $0.8625 \pm 0.0173$ | $1.2424 \pm 0.0387$ | $91.7 \pm 4.85$ |

---

### 3. Phân tích So sánh Chi tiết: Baseline vs. TSVM

#### 3.1. Về Hiệu năng Trung bình (Performance)
- **Mask mAP50-95**: TSVM ($0.7246$) cao hơn Baseline ($0.7210$) một khoảng $\Delta = +0.0036$ (tương đương $+0.36$ điểm phần trăm, mức tăng tương đối $+0.49\%$).
- **Box mAP50-95**: TSVM ($0.7285$) cao hơn Baseline ($0.7262$) một khoảng $\Delta = +0.0023$ ($+0.32\%$).
- **Mask mAP50**: TSVM ($0.9062$) thấp hơn Baseline ($0.9119$) một khoảng $\Delta = -0.0056$ ($-0.62\%$).
- **Mask Precision**: TSVM cao hơn Baseline ($\Delta = +0.0095$, $+1.05\%$). **Mask Recall**: TSVM cao hơn ($\Delta = +0.0041$, $+0.48\%$).
- **Box Recall**: TSVM cao hơn Baseline nhiều nhất trong nhóm Box ($\Delta = +0.0133$, $+1.58\%$).

#### 3.2. Về Độ ổn định Phương sai (Stability)
Đây là **khía cạnh cải thiện rõ nhất** của TSVM trên mẫu thực nghiệm này:

- **Mask mAP50-95**:
  - Độ lệch chuẩn: $\sigma$ giảm từ $0.01285$ (Baseline) xuống $0.00776$ (TSVM) — **giảm $39.7\%$**.
  - Phương sai mẫu: $1.65 \times 10^{-4} \to 6.02 \times 10^{-5}$ — **hệ số co $2.75 \times$**.
  - Khoảng giá trị (Range): TSVM $0.02735$ (từ $0.70650$ đến $0.73385$), hẹp hơn Baseline $0.04252$ (từ $0.69411$ đến $0.73663$) — **giảm $35.7\%$**.
  - Đáy hiệu năng: TSVM nâng đáy từ $0.69411$ (Baseline, s3) lên $0.70650$ (TSVM, s7), chênh $+0.0124$.
- **Box mAP50-95**: $\sigma$ giảm từ $0.01975$ xuống $0.01410$ (**−28.6%**); Range giảm $27.3\%$.
- **Box Recall**: $\sigma$ giảm từ $0.03373$ xuống $0.01523$ (**−54.8%**); phương sai co **4.90 lần**.
- **Validation Seg Loss**:
  - $\sigma$ giảm từ $0.08666$ xuống $0.03867$ — **giảm $55.4\%$**, phương sai co **5.02 lần**.
  - Range giảm từ $0.24788$ xuống $0.12429$ (**−49.9%**).
- **Best Epoch**: $\sigma$ giảm từ $13.10$ xuống $4.85$ (**−62.9%**); TSVM đạt đỉnh ổn định hơn (Range $15$ so với $39$).
- **Ngoại lệ đáng chú ý**: **Val Cls Loss** của TSVM tăng ($0.5591 \to 0.6148$, $+9.97\%$) và $\sigma$ tăng ($0.0635 \to 0.0884$), với một giá trị ngoại lệ $0.83094$ ở seed 7. Đây là điểm **bất lợi** cần nêu.
- **Nhận định khoa học**: Trên mẫu 10 seed này, cấu hình TSVM thể hiện độ tán xạ kết quả quanh giá trị trung bình **thấp hơn** trên 8/12 chỉ số đo.

#### 3.3. Về So sánh Cặp từng Seed (Seed-wise Head-to-Head)
Xét từng cặp seed tương ứng ($s \in \{0, 1, \dots, 9\}$):

| Chỉ số | TSVM thắng | Baseline thắng | TSVM thắng ở seed |
| :--- | :---: | :---: | :--- |
| **Mask mAP50-95** | **6/10** | 4/10 | 1, 2, 3, 6, 8, 9 |
| **Box mAP50-95** | **6/10** | 4/10 | 1, 2, 3, 6, 8, 9 |
| **Val Seg Loss** *(thấp hơn = thắng)* | **8/10** | 2/10 | 0, 1, 2, 3, 4, 7, 8, 9 |
| Mask mAP50 | 3/10 | 7/10 | — |
| Mask Precision / Mask Recall | 5/10, 6/10 | 5/10, 4/10 | — |

- **Lưu ý chuẩn mực**: Tỷ lệ thắng 6/10 là quan sát thống kê mẫu, **không** phải bằng chứng về sự vượt trội. Baseline thắng rõ ở seed 0, 4, 5, 7.

#### 3.4. Về Kiểm định Ý nghĩa Thống kê (Statistical Hypothesis Testing)

| Chỉ số | *t* | *p* (*t*-test) | *W* | *p* (Wilcoxon) |
| :--- | :---: | :---: | :---: | :---: |
| Mask mAP50-95 | +0.9153 | 0.3839 | 19.0 | 0.4316 |
| Box mAP50-95 | +0.3766 | 0.7152 | 20.0 | 0.4922 |
| Box Recall | +1.1824 | 0.2674 | 16.0 | 0.2754 |
| **Val Seg Loss** | **−1.8939** | **0.0908** | 10.0 | 0.0840 |
| Val Cls Loss | +1.8698 | 0.0943 | 10.0 | 0.0840 |

- **Kết luận học thuật bắt buộc**:
  - **Không chỉ số nào** có $p \le 0.05$. Vì vậy **chưa có đủ bằng chứng thống kê để bác bỏ giả thuyết không ($H_0$)** ở $\alpha = 0.05$.
  - Hai chỉ số **Val Seg Loss** ($p = 0.0908$) và **Val Cls Loss** ($p = 0.0943$) chỉ **tiệm cận** ngưỡng $\alpha = 0.10$; đồng thời chúng **ngược dấu nhau** (một cái giảm, một cái tăng) nên không tạo thành bằng chứng nhất quán.
  - **Cách trình bày đúng trong luận văn**: *"TSVM cho thấy xu hướng cải thiện nhẹ ở giá trị trung bình và độ ổn định phương sai trên 10 seed thử nghiệm, tuy nhiên sự khác biệt chưa đạt mức có ý nghĩa thống kê với cỡ mẫu $N = 10$ ($p = 0.384$)."*

---

### 4. Rà soát Phân tích Ma trận Nhầm lẫn (Confusion Matrix)

Dữ liệu ma trận nhầm lẫn tổng hợp trên 10 seed tại ngưỡng đánh giá mặc định ($conf = 0.25$, $IoU = 0.45$).

#### 4.1. Quy mô tập kiểm định
- **160 ảnh**: 120 ảnh chứa polyp (**127 thực thể ground-truth**) + 40 ảnh nền không chứa polyp (*normal-cecum*).
- Ràng buộc: $TP + FN = 127$; $FP + TN = 40$ — thỏa mãn tuyệt đối trên cả 20 dòng dữ liệu.
- ⚠️ **Không dùng con số "167 ảnh"** — đó là kết quả cộng nhầm 127 *thực thể* với 40 *ảnh*.

#### 4.2. Bảng số đếm trung bình

| Mô hình | TP (Mean ± Std) | FN (Mean ± Std) | FP (Mean ± Std) ⚠️ | TN ⚠️ | Sensitivity | FP-rate trên nền |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline** | $110.3 \pm 3.40$ | $16.7 \pm 3.40$ | $16.8 \pm 2.35$ | $23.2 \pm 2.35$ | $86.85\%$ | $42.00\%$ |
| **TSVM** | $111.2 \pm 2.20$ | $15.8 \pm 2.20$ | $14.6 \pm 4.35$ | $25.4 \pm 4.35$ | $87.56\%$ | $36.50\%$ |

#### 4.3. ⚠️ Hạn chế bắt buộc phải nêu trong luận văn

| # | Vấn đề | Mức độ | Xử lý |
| :--- | :--- | :---: | :--- |
| 1 | **Cột TN không phải số đo.** Trong `ultralytics/utils/metrics.py` (`ConfusionMatrix.process_batch`, dòng 427–434), khi ảnh nền không có GT, code **chỉ cộng FP** và **không có nhánh `matrix[self.nc, self.nc] += 1`**. Ô background↔background luôn bằng 0, bị loại khỏi ghi nhãn (dòng 550) và hiển thị trống — xác nhận trên cả 20 ảnh. Giá trị TN trong CSV **đúng bằng $40 - FP$**. | 🔴 Cao | **Chỉ trích dẫn FP** (đo thật). Với TN/Specificity phải ghi rõ *"suy dựng theo giả định $40 - FP$"*. **Không** dùng làm bằng chứng định lượng. |
| 2 | **3/20 lượt chạy không đối chiếu được**: OCR ảnh `confusion_matrix.png` cho thấy **TSVM s0** ($59/10/68$), **TSVM s5** ($0/90/127$), **TSVM s8** ($6/8/121$) khác hẳn giá trị trong CSV. Ảnh cho thấy recall gần 0, **mâu thuẫn với `results.csv` của chính các run đó** (recall $0.853/0.882/0.877$). 17/20 run còn lại khớp chính xác. | 🔴 Cao | **Nêu rõ giới hạn** khi trích dẫn CM. |
| 3 | Ghi đúng quy mô tập kiểm định | 🟡 | Dùng **160 ảnh / 127 thực thể**, không dùng "167". |

#### 4.4. Diễn giải học thuật

- **Quan sát số liệu thực tế**: trên 40 ảnh nền âm tính, FP trung bình của TSVM là $14.6$ so với $16.8$ của Baseline ($\Delta = -2.2$, FP-rate $42.00\% \to 36.50\%$). Ở cấp độ thực thể, TSVM ghi nhận nhiều TP hơn trung bình $0.9$ ca và ít FN hơn $0.9$ ca.
- **Điều chỉnh diễn giải (tránh suy diễn nguyên nhân)**:
  - ❌ *Không được viết*: "Điều này chứng minh nhánh Shape-aware giúp mô hình nắm bắt được cấu trúc hình học của polyp và loại bỏ ảnh giả."
  - ❌ *Không được viết*: "TSVM tăng Specificity lên 70.5%" (con số này không tồn tại trong dữ liệu hiện hành).
  - ✅ *Cách viết đúng*: "Trên 40 ảnh nền âm tính của tập kiểm định, TSVM ghi nhận số báo động giả trung bình thấp hơn ($14.6$ so với $16.8$ của Baseline) tại một ngưỡng quyết định cố định. Đây là quan sát mô tả trên tập kiểm định đơn lẻ; cơ chế đóng góp của từng thành phần kiến trúc cần được kiểm chứng thêm bằng phân tích ablation và trực quan hóa bản đồ đặc trưng."

---

### 5. Tóm tắt Đánh giá 2 Mô hình (10 Seed)

1. **YOLO26s-seg Baseline**:
   - Hoạt động như mốc chuẩn đối sánh cơ sở.
   - Độ nhạy tốt (Mask Recall $0.8584$), nhưng có **độ phân tán hiệu năng lớn nhất** giữa các seed ($\sigma_{mAP} = 0.01285$, Range $0.04252$), với đáy hiệu năng thấp $0.69411$ ở seed 3.
2. **YOLO26s-seg + TSVM**:
   - Mask mAP50-95 trung bình $0.7246 \pm 0.0078$.
   - Thể hiện **sự co hẹp phương sai** đáng kể: $\sigma$ giảm $39.7\%$ (Mask mAP50-95), $55.4\%$ (Val Seg Loss), $54.8\%$ (Box Recall); đáy hiệu năng được nâng lên $0.70650$.
   - Val Seg Loss giảm $-4.76\%$ ($p = 0.0908$), tiệm cận ngưỡng $\alpha = 0.10$.
   - **Khác biệt hiệu năng so với Baseline không đạt ý nghĩa thống kê** ở $\alpha = 0.05$ ($p = 0.384$).
   - **Bất lợi cần nêu**: Val Cls Loss tăng $+9.97\%$ và độ phân tán tăng, với một ngoại lệ $0.83094$ ở seed 7.
   - **Giới hạn dữ liệu**: ma trận nhầm lẫn có 3/20 lượt chạy không kiểm chứng được và cột TN là số tái dựng (mục 4.3).

---

### 6. Tài liệu tham chiếu chuẩn

> Toàn bộ số liệu chuẩn dùng cho khóa luận cử nhận: [`doc/20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md)
