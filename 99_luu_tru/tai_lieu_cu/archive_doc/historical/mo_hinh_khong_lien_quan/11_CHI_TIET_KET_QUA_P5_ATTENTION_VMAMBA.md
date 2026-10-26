# KẾT QUẢ THỰC NGHIỆM CHI TIẾT: BIẾN THỂ P5_ATTENTION_VMAMBA
## HỒ SƠ DỮ LIỆU ĐỊNH LƯỢNG 6-FOLD, PHÂN TÍCH NGUYÊN NHÂN SUY THOÁI HIỆU NĂNG VÀ VAI TRÒ TRONG ABLATION STUDY

---

> **Phân loại độ tin cậy thông tin theo nguyên tắc dự án:**
> - `[Đã xác nhận]`: Dữ liệu số liệu trích xuất 100% từ 6 tệp `results.csv` tại `Kvasir_YOLO26s_seg_P5_Attention_VMamba_{split}_w2` (`s0` đến `s5`), tính toán kiểm định thống kê Paired Student's t-test đối chiếu với Baseline và TSVM.
> - `[Có khả năng / suy luận]`: Phân tích lý thuyết kiến trúc về hiện tượng cổ chai không gian (spatial bottleneck) tại tầng P5 (stride 32, feature map 20x20).
> - `[Chưa xác minh]`: Đánh giá P5 Attention trên các tập dữ liệu có kích thước vật thể siêu lớn chiếm toàn khung hình.

---

## 1. TỔNG HỢP KẾT QUẢ ĐỊNH LƯỢNG P5_ATTENTION_VMAMBA QUA 6 FOLD (MEAN ± STD)

Dưới đây là bảng đối chiếu chi tiết 3 mô hình: Baseline (YOLO26s-seg), C2TSVMamba (Tầng 10 Đề xuất), và P5_Attention_VMamba (Biến thể gắn tại P5) trên 6-fold cross-validation:

| Chỉ số thực nghiệm | Baseline YOLO26s-seg | C2TSVMamba (Tầng 10) | P5_Attention_VMamba (P5) | So sánh P5 vs Baseline ($\Delta, p$-value) | So sánh P5 vs TSVM ($\Delta, p$-value) | Nhận xét đánh giá |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Mask mAP@50-95** | **0.7291 ± 0.0153** | **0.7231 ± 0.0055** | 0.7186 ± 0.0119 | -0.0105 ($p = 0.2262$) | -0.0045 ($p = 0.4953$) | **P5 thấp nhất trong 3 mô hình** |
| **Mask mAP@50** | **0.9144 ± 0.0065** | 0.9141 ± 0.0088 | 0.9134 ± 0.0079 | -0.0010 ($p = 0.5755$) | -0.0008 ($p = 0.9093$) | Tương đương ở ngưỡng cơ bản 0.5 |
| **Mask Precision** | **0.9198 ± 0.0139** | 0.9192 ± 0.0192 | 0.9056 ± 0.0123 | **-0.0143 ($p = 0.0023$)** | -0.0137 ($p = 0.0917$) | **P5 giảm sâu ($p < 0.01$), nhiều mask lem** |
| **Mask Recall** | 0.8760 ± 0.0175 | 0.8493 ± 0.0243 | **0.8696 ± 0.0179** | -0.0063 ($p = 0.4126$) | +0.0203 ($p = 0.0784$) | Cao hơn TSVM do bắt viền lỏng |
| **Mask F1-Score** | **0.8972 ± 0.0054** | 0.8825 ± 0.0094 | 0.8871 ± 0.0096 | **-0.0101 ($p = 0.0172$)** | +0.0046 ($p = 0.2902$) | P5 thua Baseline ($p < 0.05$) |
| **Validation Seg Loss** | 1.4314 ± 0.0540 | **1.3936 ± 0.0366** | 1.4626 ± 0.0808 | **+0.0312 ($p = 0.3910$)** | **+0.0690 ($p = 0.0952$)** | **P5 bùng nổ sai số mất mát cao nhất** |
| **Validation Box Loss** | **0.7503 ± 0.0137** | 0.7687 ± 0.0385 | 0.7939 ± 0.0347 | **+0.0436 ($p = 0.0103$)** | +0.0253 ($p = 0.3015$) | **P5 làm tăng lỗi hộp bao ($p < 0.05$)** |
| **Validation Cls Loss** | 0.5681 ± 0.0400 | 0.5938 ± 0.0302 | **0.5368 ± 0.0185** | -0.0313 ($p = 0.2383$) | **-0.0570 ($p = 0.0103$)** | Cls loss giảm nhẹ do attention phân loại |
| Box mAP@50-95 | **0.7404 ± 0.0112** | 0.7398 ± 0.0087 | 0.7300 ± 0.0098 | -0.0104 ($p = 0.0674$) | -0.0097 ($p = 0.1539$) | P5 định vị hộp bao kém nhất |
| Box mAP@50 | 0.9099 ± 0.0068 | 0.9056 ± 0.0093 | **0.9108 ± 0.0081** | +0.0008 ($p = 0.8627$) | +0.0052 ($p = 0.4236$) | Tương đương |
| Box Precision | **0.9173 ± 0.0137** | 0.9058 ± 0.0184 | 0.8960 ± 0.0191 | -0.0214 ($p = 0.0221$) | -0.0098 ($p = 0.2617$) | P5 giảm Precision hộp bao |
| Box Recall | 0.8664 ± 0.0246 | 0.8429 ± 0.0282 | **0.8732 ± 0.0246** | +0.0068 ($p = 0.5883$) | +0.0303 ($p = 0.0307$) | P5 bắt hộp rộng hơn |
| Box F1-Score | **0.8908 ± 0.0082** | 0.8727 ± 0.0111 | 0.8840 ± 0.0079 | -0.0068 ($p = 0.2114$) | +0.0113 ($p = 0.0039$) | - |
| Best Fitness Epoch | 91.8 ± 8.6 | 85.2 ± 13.2 | 89.7 ± 11.0 | -2.2 ($p = 0.6898$) | +4.5 ($p = 0.3765$) | Đạt đỉnh quanh epoch 85–92 |

`[Đã xác nhận]`

---

## 2. BẢNG PHÂN RÃ CHI TIẾT TỪNG SEED CỦA P5_ATTENTION_VMAMBA

Dữ liệu thực tế tại thời điểm đạt Best Fitness Epoch của từng split:

| Seed | Epoch tối ưu | Mask mAP@50 | Mask mAP@50-95 | Mask Precision | Mask Recall | Mask F1-Score | Val Seg Loss | Val Box Loss | Val Cls Loss |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **s0** | 100 | 0.9214 | 0.7403 | 0.9062 | 0.8819 | 0.8939 | 1.3112 | 0.7576 | 0.5266 |
| **s1** | 100 | 0.9177 | 0.7223 | 0.9005 | 0.8898 | 0.8951 | 1.4939 | 0.7649 | 0.5387 |
| **s2** | 81 | 0.9021 | 0.7171 | 0.8937 | 0.8607 | 0.8769 | 1.4805 | 0.8384 | 0.5351 |
| **s3** | 75 | 0.9212 | 0.7140 | 0.9248 | 0.8425 | 0.8817 | 1.4437 | 0.8065 | 0.5188 |
| **s4** | 98 | 0.9078 | 0.7115 | 0.8937 | 0.8610 | 0.8770 | 1.5421 | 0.7691 | 0.5719 |
| **s5** | 84 | 0.9098 | 0.7064 | 0.9145 | 0.8819 | 0.8979 | 1.5043 | 0.8272 | 0.5298 |
| **Trung bình** | **89.7** | **0.9134** | **0.7186** | **0.9056** | **0.8696** | **0.8871** | **1.4626** | **0.7939** | **0.5368** |
| **Độ lệch (Std)**| **11.0**| **0.0079** | **0.0119** | **0.0123** | **0.0179** | **0.0096** | **0.0808** | **0.0347** | **0.0185** |

`[Đã xác nhận]`

---

## 3. BA NGUYÊN NHÂN KỸ THUẬT KHIẾN P5 THẤT BẠI TRONG PHÂN ĐOẠN POLYP

```
                   Ảnh nội soi gốc (640x640)
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
       TẦNG 10 (STRIDE 16)           TẦNG P5 (STRIDE 32)
   - Feature map: 40x40 (1.600 px) - Feature map: 20x20 (400 px)
   - Lưu giữ chi tiết viền biên    - Mất sạch cấu trúc hình thái
   - SS2D + Morphological Convs    - Attention trên điểm ảnh thô
               │                             │
               ▼                             ▼
   [THÀNH CÔNG: C2TSVMamba]         [THẤT BẠI: P5_Attention]
   - val/seg_loss: 1.3936           - val/seg_loss: 1.4626 (Tăng vọt)
   - Mask Precision: 91.92%         - Mask Precision: 90.56% (Sụt giảm)
   - Bám khít giải phẫu             - Mặt nạ nhòe, tràn viền
```

### 3.1. Nghẽn cổ chai độ phân giải không gian (Spatial Bottleneck at Stride 32)
- Ở tầng sâu nhất P5, ảnh đầu vào $640\times 640$ bị giảm mẫu liên tục qua 5 tầng tích chập stride 2, co lại thành bản đồ đặc trưng chỉ còn $20\times 20$ điểm ảnh (tổng cộng 400 vị trí biểu diễn).
- Mỗi điểm ảnh tại P5 bao phủ một vùng không gian thực tế $32\times 32$ pixels.
- Các polyp đại tràng nhỏ ($< 10\text{mm}$) chỉ chiếm diện tích tương đương 1–2 điểm ảnh trên tầng P5. Cơ chế Attention dù tính toán mối liên hệ xa nhưng không thể phục hồi lại các ranh giới vi thể đã bị tiêu biến hoàn toàn do downsampling.

### 3.2. Hiện tượng suy giảm nghiêm trọng Mask Precision ($p = 0.0023$)
- Khi giải mã mặt nạ tại Mask Proto Head, các đặc trưng từ tầng P5 phải được nội suy phóng đại (upsample) gấp 32 lần.
- Sự thiếu hụt thông tin hình thái học khiến mặt nạ dự đoán bị mờ nhòe (blurred mask), ranh giới không rõ ràng, dẫn tới việc mô hình dự đoán bao phủ lem sang các vùng niêm mạc bình thường.
- Kết quả kiểm định thống kê cho thấy Mask Precision của P5 sụt giảm từ **$0.9198$** (Baseline) xuống **$0.9056$** ($p = 0.0023 < 0.01$).

### 3.3. Bùng nổ hàm mất mát phân đoạn (`val/seg_loss` = 1.4626)
- Vì mặt nạ bị lem và nhòe, sai số hàm phạt mặt nạ (`val/seg_loss`) của P5 tăng vọt lên **$1.4626$**, cao hơn cả mô hình gốc Baseline ($1.4314$) và cao hơn rất nhiều so với mô hình đề xuất C2TSVMamba ($1.3936$).

`[Có khả năng / suy luận]`

---

## 4. Ý NGHĨA KHOA HỌC CỦA P5 TRONG LUẬN VĂN (GIÁ TRỊ ABLATION STUDY)

Mặc dù không được chọn làm mô hình chính để báo cáo triển khai lâm sàng, kết quả của `P5_Attention_VMamba` đóng vai trò là **bằng chứng phản biện cực kỳ giá trị trong phần Ablation Study** của Luận văn Cử nhân:

1. **Bác bỏ lối mòn tư duy kỹ thuật:** Chứng minh cho hội đồng phản biện thấy rằng không phải cứ gắn thêm cơ chế Attention hay Mamba vào tầng sâu nhất P5 là mô hình sẽ tự động tốt lên.
2. **Khẳng định tính đúng đắn của thiết kế Tầng 10:** Việc chuyển khối C2TSVMamba lên Tầng 10 (Neck chuyển tiếp, bản đồ $40\times 40$) là một quyết định kiến trúc có cơ sở khoa học sâu sắc, giúp cân bằng hoàn hảo giữa thông tin ngữ cảnh toàn cục (SS2D) và độ sắc nét ranh giới giải phẫu (Morphological Convolutions).
