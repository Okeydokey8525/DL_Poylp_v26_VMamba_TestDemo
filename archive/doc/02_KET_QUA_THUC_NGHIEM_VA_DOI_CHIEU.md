# KẾT QUẢ THỰC NGHIỆM ĐỊNH LƯỢNG 6-FOLD: BASELINE VS TSVM
## DỮ LIỆU THỰC TẾ 100% TRÍCH XUẤT TỪ CÁC TỆP `results.csv`

---

## 1. BẢNG SO SÁNH TỔNG HỢP & KIỂM ĐỊNH THỐNG KÊ (PAIRED T-TEST)

Thực nghiệm được thực hiện trên 6 splits độc lập (`s0` đến `s5`) của tập dữ liệu Kvasir-SEG (100 epochs/fold). Dưới đây là giá trị **Trung bình ± Độ lệch chuẩn** ($	ext{Mean} \pm 	ext{Std}$) và kiểm định cặp Paired Student's t-test ($df = 5$):

| Nhóm chỉ số | Tên chỉ số | Baseline (YOLO26s-seg) | Cải tiến (TSVM) | Chênh lệch ($\Delta$) | Tỷ lệ thay đổi | $p$-value | Ý nghĩa thống kê ($p < 0.05$) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Hàm mất mát** | **Val Seg Loss (Lỗi phân đoạn)** | 1.4314 ± 0.0540 | **1.3936 ± 0.0366** | **-0.0378** | **-2.64%** | **0.0363** | **CÓ (TSVM giảm tốt hơn)** |
| | **Val Box Loss** | **0.7503 ± 0.0137** | 0.7687 ± 0.0385 | +0.0183 | +2.44% | 0.2605 | Không |
| | **Val Cls Loss** | **0.5681 ± 0.0400** | 0.5938 ± 0.0302 | +0.0257 | +4.52% | 0.2207 | Không |
| **Mặt nạ (Mask)** | **Mask mAP@50** | **0.9144 ± 0.0065** | 0.9141 ± 0.0088 | -0.0003 | -0.03% | 0.9641 | Không khác biệt |
| | **Mask mAP@50-95** | **0.7291 ± 0.0153** | 0.7231 ± **0.0055** | -0.0060 | -0.82% | 0.4683 | Không khác biệt |
| | **Mask Precision** | **0.9198 ± 0.0139** | 0.9192 ± 0.0192 | -0.0006 | -0.07% | 0.9397 | Không khác biệt |
| | **Mask Recall** | **0.8760 ± 0.0175** | 0.8493 ± 0.0243 | -0.0266 | -3.04% | **0.0495** | **CÓ (Baseline cao hơn)** |
| | **Mask F1-Score** | **0.8972 ± 0.0054** | 0.8825 ± 0.0094 | -0.0146 | -1.63% | **0.0042** | **CÓ (Baseline cao hơn)** |
| **Hộp bao (Box)** | **Box mAP@50** | **0.9099 ± 0.0068** | 0.9056 ± 0.0093 | -0.0044 | -0.48% | 0.5103 | Không khác biệt |
| | **Box mAP@50-95** | **0.7404 ± 0.0112** | 0.7398 ± **0.0087** | -0.0007 | -0.09% | 0.9293 | Không khác biệt |
| | **Box Precision** | **0.9173 ± 0.0137** | 0.9058 ± 0.0184 | -0.0116 | -1.26% | 0.2705 | Không khác biệt |
| | **Box Recall** | **0.8664 ± 0.0246** | 0.8429 ± 0.0282 | -0.0235 | -2.71% | 0.1596 | Không |
| | **Box F1-Score** | **0.8908 ± 0.0082** | 0.8727 ± 0.0111 | -0.0180 | -2.03% | **0.0159** | **CÓ (Baseline cao hơn)** |

---

## 2. DỮ LIỆU CHI TIẾT TỪNG FOLD (SPLIT-BY-SPLIT)

Dưới đây là giá trị thực tế tại epoch đạt điểm đánh giá cao nhất (`best fitness`) của từng split:

### A. Chỉ số Mặt nạ Phân đoạn (Mask Segmentation Metrics)

| Split | Mô hình | Best Epoch | Mask Precision | Mask Recall | Mask F1-Score | Mask mAP@50 | Mask mAP@50-95 | Val Seg Loss |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **s0** | Baseline | 100 | **0.9250** | 0.8737 | **0.8986** | **0.9208** | **0.7232** | 1.4142 |
| | TSVM | 100 | 0.8886 | **0.8793** | 0.8839 | 0.9061 | 0.7201 | **1.3922** |
| **s1** | Baseline | 98 | 0.9177 | **0.8785** | **0.8977** | **0.9223** | **0.7435** | **1.4150** |
| | TSVM | 100 | **0.9295** | 0.8307 | 0.8774 | 0.9060 | 0.7212 | 1.4241 |
| **s2** | Baseline | 80 | **0.9142** | **0.8740** | **0.8937** | 0.9049 | 0.7271 | 1.3605 |
| | TSVM | 79 | 0.9096 | 0.8661 | 0.8874 | **0.9146** | **0.7291** | **1.3324** |
| **s3** | Baseline | 100 | 0.9388 | **0.8455** | **0.8897** | **0.9148** | **0.7240** | 1.4183 |
| | TSVM | 72 | **0.9416** | 0.8189 | 0.8760 | 0.9088 | 0.7171 | **1.3771** |
| **s4** | Baseline | 85 | 0.8974 | **0.8976** | **0.8975** | 0.9127 | **0.7496** | 1.4600 |
| | TSVM | 71 | **0.9136** | 0.8347 | 0.8724 | **0.9268** | 0.7202 | **1.4016** |
| **s5** | Baseline | 88 | 0.9260 | **0.8864** | **0.9058** | 0.9107 | 0.7073 | 1.5208 |
| | TSVM | 89 | **0.9324** | 0.8661 | 0.8981 | **0.9224** | **0.7308** | **1.4344** |

### B. Chỉ số Phát hiện Hộp bao (Bounding Box Metrics)

| Split | Mô hình | Box Precision | Box Recall | Box F1-Score | Box mAP@50 | Box mAP@50-95 | Val Box Loss |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **s0** | Baseline | **0.9345** | 0.8504 | **0.8905** | **0.9180** | **0.7484** | **0.7313** |
| | TSVM | 0.8806 | **0.8714** | 0.8760 | 0.9020 | 0.7337 | 0.7666 |
| **s1** | Baseline | 0.9095 | **0.8708** | **0.8898** | **0.9159** | **0.7512** | **0.7353** |
| | TSVM | **0.9208** | 0.8236 | 0.8695 | 0.8911 | 0.7479 | 0.7360 |
| **s2** | Baseline | **0.9142** | **0.8740** | **0.8937** | 0.9061 | 0.7334 | **0.7584** |
| | TSVM | 0.9014 | 0.8583 | 0.8793 | **0.9091** | **0.7348** | 0.7949 |
| **s3** | Baseline | 0.9305 | **0.8268** | **0.8756** | 0.9086 | 0.7320 | 0.7534 |
| | TSVM | **0.9325** | 0.8110 | 0.8675 | 0.9017 | **0.7431** | **0.7348** |
| **s4** | Baseline | **0.8974** | **0.8976** | **0.8975** | 0.9118 | **0.7513** | **0.7606** |
| | TSVM | 0.8963 | 0.8189 | 0.8558 | **0.9120** | 0.7286 | 0.8322 |
| **s5** | Baseline | **0.9177** | **0.8786** | **0.8977** | 0.8993 | 0.7261 | 0.7630 |
| | TSVM | 0.9030 | 0.8740 | 0.8883 | **0.9174** | **0.7505** | **0.7475** |

---

## 3. SO SÁNH CHI PHÍ TÀI NGUYÊN VÀ THỜI GIAN HUẤN LUYỆN

| Chỉ số tài nguyên | Baseline (YOLO26s-seg) | Cải tiến (TSVM) | So sánh chênh lệch |
| :--- | :---: | :---: | :--- |
| **Dung lượng file trọng số (`best.pt`)** | 22.27 MB | 23.86 MB | TSVM lớn hơn **+1.59 MB (+7.1%)** |
| **Thời gian huấn luyện 1 fold (100 ep)** | **1.91 giờ** (6.859 s) | **3.92 giờ** (14.118 s) | TSVM lâu hơn **gấp 2.06 lần (+106%)** |
| **Tổng thời gian huấn luyện 6 folds** | **11.43 giờ** | **23.53 giờ** | Tốn thêm **12.1 giờ GPU** |
| **Epoch đạt điểm cao nhất trung bình** | Epoch 91.8 | Epoch 85.2 | TSVM có xu hướng hội tụ sớm hơn |

---

## 4. PHÂN TÍCH KHOA HỌC KHÁCH QUAN & BIỆN LUẬN HỌC THUẬT

### A. Những điểm mạnh đã được chứng minh của TSVM:
1. **Tối ưu hóa chất lượng mặt nạ phân đoạn ($p = 0.0363 < 0.05$):**
   Hàm mất mát phân đoạn `val/seg_loss` của TSVM giảm từ **1.4314** xuống **1.3936** (giảm ở 5/6 split). Đây là bằng chứng định lượng then chốt chứng minh cơ chế kết hợp dải tích chập hình học ($1	imes5, 5	imes1$) và gradient biên khả vi trong `TSVMamba` đã trực tiếp giúp mô hình sinh ra mặt nạ khớp hơn với ranh giới polyp thực tế.
2. **Tính vững chắc (Robustness) vượt trội giữa các fold:**
   Độ lệch chuẩn của `Mask mAP@50-95` ở TSVM là **0.0055**, thấp hơn gần **3 lần** so với Baseline (**0.0153**). Mô hình cải tiến chứng minh khả năng khái quát hóa (generalization) rất đồng đều, không bị biến động mạnh theo cách chia tập dữ liệu.

### B. Những hạn chế và sự đánh đổi (Trade-offs):
1. **Chỉ số mAP tổng thể không tăng đột biến:** Mask mAP@50 đạt 0.9141 (so với 0.9144 của Baseline); Mask mAP@50-95 đạt 0.7231 (so với 0.7291 của Baseline). Cải tiến không mang lại sự bứt phá về mAP toàn dải.
2. **Sự đánh đổi về Mask Recall:** Do ràng buộc hình học topo quá chặt chẽ, TSVM có xu hướng dự đoán thận trọng, dẫn đến Mask Recall giảm nhẹ từ **0.8760** xuống **0.8493** ($-3.04\%$, $p = 0.0495$).
3. **Chi phí thời gian:** Thuật toán quét 2D (SS2D) làm tăng thời gian huấn luyện gấp 2.06 lần trên GPU.
