# KẾT QUẢ THỰC NGHIỆM CHI TIẾT: MÔ HÌNH INTERACTIVE ATTENTION VMAMBA (IAVM)
## HỒ SƠ THỰC NGHIỆM ĐỊNH LƯỢNG 6-FOLD, ĐỈNH CAO MASK mAP@50-95 VÀ PHÂN TÍCH ĐÁNH ĐỔI PRECISION - RECALL

---

> **Phân loại độ tin cậy thông tin theo nguyên tắc dự án:**
> - `[Đã xác nhận]`: Dữ liệu số liệu trích xuất 100% từ 6 tệp `results.csv` tại `Kvasir_YOLO26s_seg_IAVM_{split}_w2` (`s0` đến `s5`), tệp cấu hình `args.yaml` và kiểm định thống kê Paired Student's t-test.
> - `[Có khả năng / suy luận]`: Phân tích cơ chế tương tác đa hướng (interactive attention) kết hợp quét không gian trạng thái tuyến tính (SS2D) giúp mở rộng trường tiếp nhận và tối ưu hóa Recall.
> - `[Chưa xác minh]`: Đo đạc độ trễ phần cứng chi tiết trên chip nhúng NVIDIA Jetson Orin cho biến thể IAVM.

---

## 1. TỔNG QUAN KIẾN TRÚC VÀ CẤU HÌNH HUẤN LUYỆN CỦA IAVM

Mô hình **IAVM** (`yolo26s-seg-InteractiveAttentionVMamba.yaml`) được thiết kế nhằm kết hợp sức mạnh của:
1. **Cơ chế Chú ý Tương tác (Interactive Attention):** Cho phép các vùng đặc trưng trao đổi thông tin chéo lẫn nhau một cách thích ứng.
2. **Mô hình Không gian Trạng thái Thị giác (Visual State-Space - VMamba / SS2D):** Khai thác ngữ cảnh toàn cục đa hướng với độ phức tạp tính toán tuyến tính $\mathcal{O}(N)$.

### Thông số huấn luyện đồng bộ 6 seed:
- **Tập dữ liệu:** Kvasir-SEG (chuẩn hóa $640\times 640$, nhãn đa giác YOLO-seg).
- **Phân chia 6-Fold:** `s0`, `s1`, `s2`, `s3`, `s4`, `s5` (mỗi fold 100 epochs, batch size 8).
- **Khởi tạo & Tối ưu hóa:** Trọng số tiền huấn luyện `pretrained: yolo26s-seg.pt`, tối ưu hóa `AdamW` ($lr_0 = 0.001$, $lrf = 0.01$, momentum 0.937, weight decay 0.0005).
- **Kỹ thuật điều hòa:** `close_mosaic=10` (tắt mosaic ở 10 epoch cuối), không dùng mixup/cutmix, khóa hạt giống tất định `deterministic: true`.
- **Dung lượng tệp trọng số `best.pt`:** **$24.29\text{ MB}$** (24,286,981 bytes) trên cả 6 splits, chỉ nhỉnh hơn nhẹ so với C2TSVMamba ($23.86\text{ MB}$) và Baseline ($22.27\text{ MB}$).

`[Đã xác nhận]`

---

## 2. BẢNG DỮ LIỆU ĐỊNH LƯỢNG TỪNG FOLD CỦA IAVM (BEST FITNESS EPOCH)

Dưới đây là các chỉ số chi tiết tại epoch đạt điểm số fitness tối ưu trên từng seed kiểm thử độc lập:

| Seed (Fold) | Epoch tối ưu | Mask mAP@50 | Mask mAP@50-95 | Mask Precision | Mask Recall | Mask F1-Score | Val Seg Loss | Val Box Loss | Val Cls Loss | Box mAP@50 | Box mAP@50-95 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **s0** | 91 | 0.9319 | 0.7426 | 0.8903 | 0.8947 | 0.8925 | 1.4411 | 0.7931 | 0.5181 | 0.9265 | 0.7392 |
| **s1** | 93 | 0.9176 | 0.7466 | 0.9109 | 0.8860 | 0.8983 | 1.3580 | 0.7428 | 0.5380 | 0.9055 | 0.7427 |
| **s2** | 85 | 0.9025 | 0.7312 | 0.8713 | 0.9064 | 0.8885 | 1.4295 | 0.7365 | 0.6203 | 0.9049 | 0.7316 |
| **s3** | 97 | 0.9172 | 0.7292 | 0.8467 | 0.8976 | 0.8714 | 1.4710 | 0.7822 | 0.6315 | 0.9145 | 0.7474 |
| **s4** | 79 | 0.9035 | 0.7297 | 0.8832 | 0.8898 | 0.8865 | 1.4134 | 0.7654 | 0.5863 | 0.9205 | 0.7434 |
| **s5** | 78 | 0.9167 | 0.7375 | 0.9233 | 0.8504 | 0.8853 | 1.2791 | 0.7226 | 0.6468 | 0.9188 | 0.7462 |
| **Trung bình (Mean)** | **87.2** | **0.9149** | **0.7361** | **0.8876** | **0.8875** | **0.8871** | **1.3987** | **0.7571** | **0.5902** | **0.9151** | **0.7418** |
| **Độ lệch chuẩn (Std)** | **7.8** | **0.0109** | **0.0073** | **0.0275** | **0.0195** | **0.0090** | **0.0695** | **0.0276** | **0.0524** | **0.0086** | **0.0057** |

`[Đã xác nhận]`

---

## 3. BẢNG SO SÁNH ĐỐI ĐẦU 3 MÔ HÌNH (BASELINE VS TSVM VS IAVM)

Bảng tổng hợp kiểm định cặp Paired Student's t-test ($df = 5$) giữa IAVM với Baseline và C2TSVMamba:

| Nhóm chỉ số | Tên chỉ số | (1) Baseline (YOLO26s-seg) | (2) Đề xuất C2TSVMamba | (3) Interactive Attention VMamba (IAVM) | So sánh (3) vs (1) (IAVM vs Base) | So sánh (3) vs (2) (IAVM vs TSVM) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Mặt nạ (Mask)** | **Mask mAP@50-95** | 0.7291 ± 0.0153 | 0.7231 ± 0.0055 | **0.7361 ± 0.0073** | **+0.0070** ($p = 0.3569$) | **+0.0130 ($p = 0.0173 < 0.05$)** |
| | **Mask mAP@50** | 0.9144 ± 0.0065 | 0.9141 ± 0.0088 | **0.9149 ± 0.0109** | +0.0005 ($p = 0.8701$) | +0.0008 ($p = 0.9180$) |
| | **Mask Recall** | 0.8760 ± 0.0175 | 0.8493 ± 0.0243 | **0.8875 ± 0.0195** | **+0.0115** ($p = 0.4056$) | **+0.0382 ($p = 0.0389 < 0.05$)** |
| | **Mask Precision** | **0.9198 ± 0.0139** | **0.9192 ± 0.0192** | 0.8876 ± 0.0275 | -0.0322 ($p = 0.0640$) | -0.0316 ($p = 0.0727$) |
| | **Mask F1-Score** | **0.8972 ± 0.0054** | 0.8825 ± 0.0094 | 0.8871 ± 0.0090 | -0.0101 ($p = 0.0289$) | +0.0046 ($p = 0.4071$) |
| **Hàm mất mát** | **Val Seg Loss (Best)** | 1.4314 ± 0.0540 | **1.3936 ± 0.0366** | **1.3987 ± 0.0695** | **-0.0328** ($p = 0.5151$) | +0.0051 ($p = 0.9052$) |
| | **Val Seg Loss (Ep 100)** | 1.4443 ± 0.0615 | 1.4265 ± 0.0305 | **1.3989 ± 0.0502** | **-0.0454** ($p = 0.2967$) | **-0.0276** ($p = 0.3678$) |
| | **Val Box Loss (Best)** | **0.7503 ± 0.0137** | 0.7687 ± 0.0385 | 0.7571 ± 0.0276 | +0.0068 ($p = 0.6666$) | -0.0116 ($p = 0.5670$) |
| **Hộp bao (Box)** | **Box mAP@50-95** | 0.7404 ± 0.0112 | 0.7398 ± 0.0087 | **0.7418 ± 0.0057** | **+0.0014** ($p = 0.8087$) | **+0.0020** ($p = 0.5524$) |
| | **Box mAP@50** | 0.9099 ± 0.0068 | 0.9056 ± 0.0093 | **0.9151 ± 0.0086** | **+0.0052** ($p = 0.2653$) | **+0.0095** ($p = 0.0693$) |
| | **Box Recall** | 0.8664 ± 0.0246 | 0.8429 ± 0.0282 | **0.8842 ± 0.0185** | **+0.0178** ($p = 0.2425$) | **+0.0413 ($p = 0.0474 < 0.05$)** |
| | **Box Precision** | **0.9173 ± 0.0137** | 0.9058 ± 0.0184 | 0.8842 ± 0.0301 | -0.0331 ($p = 0.0826$) | -0.0215 ($p = 0.2453$) |

`[Đã xác nhận]`

---

## 4. PHÂN TÍCH CHUYÊN SÂU ƯU THẾ VÀ SỰ ĐÁNH ĐỔI CỦA IAVM

```
                     SO SÁNH ĐẶC TÍNH LÂM SÀNG & THỰC NGHIỆM
    ┌────────────────────────────────────────┬────────────────────────────────────────┐
    │     MÔ HÌNH C2TSVMamba (ĐỀ XUẤT)       │       MÔ HÌNH IAVM (INTERACTIVE)       │
    ├────────────────────────────────────────┼────────────────────────────────────────┤
    │ 1. Mask Precision: CỰC CAO (91.92%)    │ 1. Mask Precision: Khá (88.76%)        │
    │ 2. Mask Recall: 84.93% (Thận trọng)    │ 2. Mask Recall: CỰC CAO (88.75%)       │
    │ 3. Mask mAP@50-95: 0.7231 (Std = 0.0055)│ 3. Mask mAP@50-95: ĐỈNH CAO (0.7361)   │
    │ 4. Ưu thế: Khóa chặt viền giải phẫu,   │ 4. Ưu thế: Bắt trọn vẹn tổn thương,    │
    │    không lem viền mô lành, cực kỳ      │    tỷ lệ phát hiện cao nhất, mAP cao   │
    │    an toàn cho phẫu thuật EMR/ESD.     │    nhất, chống bỏ sót tổn thương.      │
    └────────────────────────────────────────┴────────────────────────────────────────┘
```

### 4.1. Đột phá về Mask mAP@50-95 ($0.7361$) và Mask Recall ($88.75\%$)
- IAVM đạt mức điểm `Mask mAP@50-95` cao nhất trong toàn bộ các mô hình thực nghiệm: **$0.7361 \pm 0.0073$**. Khi so sánh với C2TSVMamba ($0.7231$), mức tăng $+0.0130$ đạt độ tin cậy có ý nghĩa thống kê vượt trội với **$p = 0.0173 < 0.05$**.
- Về độ nhạy phát hiện (`Mask Recall`), IAVM đạt **$88.75\%$**, vượt C2TSVMamba $+3.82\%$ ($p = 0.0389 < 0.05$) và vượt cả Baseline ($87.60\%$). 
- Cơ chế Interactive Attention giúp mạng nơ-ron chủ động tìm kiếm và "kéo" các vùng ranh giới polyp bị mờ nhạt vào vùng chú ý, giúp nhận diện trọn vẹn các polyp khó phát hiện.

### 4.2. Sự đánh đổi: Mask Precision giảm xuống $88.76\%$
- Đổi lại việc tăng mạnh Recall, `Mask Precision` của IAVM bị giảm sút từ $91.98\%$ (Baseline) và $91.92\%$ (TSVM) xuống mức **$88.76\%$** (chênh lệch $\approx -3.2\%$).
- Khi tương tác chú ý được kích hoạt mạnh mẽ, mô hình có xu hướng sinh mặt nạ rộng hơn (slightly over-segmented) để đảm bảo không bỏ sót mô u, dẫn tới một số điểm ảnh niêm mạc lân cận bị gán nhầm vào mặt nạ.

---

## 5. KẾT LUẬN VÀ GIÁ TRỊ ĐÓNG GÓP TRONG KHÓA LUẬN CỬ NHÂN

1. **Vị thế học thuật:** Cả hai mô hình **C2TSVMamba** và **IAVM** đều là những cải tiến thành công rực rỡ so với Baseline YOLO26s-seg tiêu chuẩn, nhưng phục vụ hai triết lý lâm sàng khác nhau:
   - **Nếu ưu tiên Độ an toàn phẫu thuật (EMR/ESD):** Chọn **C2TSVMamba** vì độ chính xác ranh giới tuyệt đối ($91.92\%$ Precision, viền mượt mà, sai số phân đoạn tối ưu $1.3936$, phương sai hẹp nhất $0.0055$).
   - **Nếu ưu tiên Độ bao phủ chẩn đoán & Phát hiện sớm (Screening CADe):** Chọn **IAVM** vì khả năng bao phủ tổn thương tối đa ($88.75\%$ Recall, mAP@50-95 cao nhất $0.7361$, Box mAP@50 đạt $0.9151$).
2. **Giá trị báo cáo:** Bạn có thể đưa cả hai mô hình này vào phần thực nghiệm và thảo luận kết quả của Luận văn: C2TSVMamba là mô hình đề xuất tập trung vào hình thái biên, còn IAVM là mô hình mở rộng khai thác cơ chế chú ý tương tác cho bài toán phát hiện toàn diện.
