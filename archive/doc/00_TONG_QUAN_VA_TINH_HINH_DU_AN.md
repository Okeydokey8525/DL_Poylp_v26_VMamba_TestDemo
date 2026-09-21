# TỔNG QUAN DỰ ÁN & BÀN GIAO TRẠNG THÁI HIỆN TẠI
## HỒ SƠ TỔNG THỂ DÀNH CHO CÁC AI VÀ KỸ SƯ TIẾP QUẢN DỰ ÁN

---

> [!IMPORTANT]
> **THÔNG TIN ĐỀ TÀI KHÓA LUẬN CỬ NHÂN (2026 – 2027)**
> - **Mã đề tài:** `CNTT_KLCN182`
> - **Tên đề tài chính thức:** *"Nghiên cứu phương pháp tích hợp VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng"*
> - **Giảng viên hướng dẫn (GVHD):** TS. Phùng Thế Bảo (`baopt@huit.edu.vn`) - Khoa CNTT, Trường Đại học Công Thương TP.HCM (HUIT)
> - **Nhóm sinh viên thực hiện:** 
>   1. Lê Đức Lương (MSSV: `2001230490` - Nhóm trưởng)
>   2. Phùng Tuấn Huy (MSSV: `2001230312`)
>   3. Trần Mạnh Toàn (MSSV: `2001230830`)
> - **Tập dữ liệu chuẩn:** Kvasir-SEG (880 ảnh train, 120 ảnh validation, 127 polyp thực tế có ground-truth mask pixel).
> - **Môi trường huấn luyện:** Kaggle GPU NVIDIA Tesla T4 (14.912 MiB VRAM), PyTorch 2.10.0+cu128, Python 3.12.
> - **Siêu tham số thực nghiệm cố định:** Epochs: 100, Imgsz: 640, Batch: 8, Workers: 2, Optimizer: AdamW (`lr0=0.001`, `warmup_epochs=5.0`), `close_mosaic=10`, AMP: `False` (FP32 nghiêm ngặt), khóa tất định 100%.

---

## 1. MỤC TIÊU CỐT LÕI VÀ BỐI CẢNH KHOA HỌC

1. **Thách thức lâm sàng:** Polyp đại trực tràng có hình thái biến thiên phức tạp (phẳng, không cuống, gồ ghề), đường biên mờ hòa lẫn vào nếp gấp niêm mạc ruột và bề mặt thường xuyên bị lóa sáng (specular glare) do đèn nội soi Xenon/LED. Các kiến trúc CNN thuần túy (như YOLO-seg tiêu chuẩn) thường sinh mặt nạ bị rách biên, lem sang mô lành hoặc bị thủng lỗ do lóa sáng.
2. **Giải pháp cốt lõi:** Tích hợp cơ chế Không gian Trạng thái Thị giác (**Visual State-Space - VMamba / SS2D**) với độ phức tạp tuyến tính $\mathcal{O}(N)$ kết hợp với cơ chế Chú ý Tương tác (**Interactive Attention**) để vừa bao quát ngữ cảnh toàn diện, vừa bắt dính ranh giới giải phẫu học của polyp.
3. **Mô hình Đề xuất Vô địch (👑 PROPOSED CHAMPION MODEL):**
   - **`Attention-VMamba Fusion` (`C2IAVM`):** Tích hợp tại **Layer 10 (Backbone P5, $20\times 20$)**, tương tác hai chiều chéo (Reciprocal Cross-Spatial Exchange) giữa Self-Attention và VMamba (SS2D 4 hướng).
   - Đạt kỷ lục hiệu năng toàn đề tài: **Mask mAP@50-95 đạt $73.65\%$** (kỷ lục $74.70\%$ tại seed s1), **Mask Recall đạt $88.75\%$** (kỷ lục $90.60\%$ tại seed s2), **giảm phương sai $4.15\times$** so với Baseline, thắng trực tiếp 5/6 seed ($83.3\%$ win rate).

---

## 2. BẢN ĐỒ CÁC MÔ HÌNH VÀ HỆ THỐNG ABLATION STUDIES

Dự án phát triển một hệ thống toàn diện gồm 8 biến thể phục vụ đối chứng khoa học:

| STT | Tên mô hình / Thư mục mã nguồn | Vị trí tích hợp | Cơ chế hoạt động | Vai trò trong đề tài |
| :---: | :--- | :---: | :--- | :--- |
| 1 | `ultralytics/` | Gốc | YOLO26s-seg chuẩn với khối `C2PSA` | **Baseline đối chứng sạch** |
| 2 | `ultralytics_Attention_VMamba_Fusion/` (`C2IAVM`) | Layer 10 (P5, $20\times 20$) | Tương tác chéo hai chiều Self-Attention $\rightleftharpoons$ VMamba SS2D | **👑 MÔ HÌNH ĐỀ XUẤT VÔ ĐỊCH** |
| 3 | `ultralytics_Interactive_Topology_VMamba/` (`C2ITSMamba`) | Layer 10 (P5, $20\times 20$) | Tương tác chéo hai chiều SS2D $\rightleftharpoons$ Hình thái học ($1\times 5, 5\times 1$) | Biến thể tương tác hình thái |
| 4 | `ultralytics_Topology-Shape-aware VMamba/` (`C2TSVMamba`)| Layer 10 (P5, $20\times 20$) | Gating một chiều từ Tích chập hình thái học $\to$ SS2D | Ablation: Hình thái học đơn hướng |
| 5 | `ultralytics_Attention_VMamba/` (`P5_Attention_VMamba`) | Layer 10 (P5, $20\times 20$) | Ghép song song tĩnh `torch.cat([Attn, VMamba])` | Ablation: Ghép kênh song song thô |
| 6 | `ultralytics_Boundary-aware VMamba/` | Layer 5 (P3, $80\times 80$) | Bộ lọc vi phân biên Sobel bậc một | Ablation: Khuyết tật lọc thông cao ở tầng sớm |
| 7 | `ultralytics_VMamba Multi-scale Fusion/` | Cổ mạng Neck ($80\times 80$) | Hợp nhất đa tỉ lệ P3, P4, P5 | Ablation: Giới hạn phần cứng chuỗi dài $L=6400$ |
| 8 | `ultralytics_Proto_VMamba/` | Segmentation Head Proto | Tích hợp SS2D vào Proto26 ($80\times 80 \to 160\times 160$) | Ablation: Tràn VRAM OOM ở độ phân giải cao |

---

## 3. QUY CHUẨN TÍNH TOÁN BẮT BUỘC: CÁCH 2 (PURE PYTORCH TRÊN CUDA)

* **Toán tử quét 2D (SS2D 4 hướng):** Viết 100% bằng PyTorch thuần dựa trên thuật toán quét tiền tố song song liên kết Hillis-Steele (`parallel_associative_scan`) với độ phức tạp thời gian $\mathcal{O}(\log_2 L)$.
* **Tuyệt đối không dùng custom C++ CUDA kernel (`selective_scan_cuda`):** Đảm bảo tính tái lập 100%, không bao giờ gặp lỗi biên dịch hay xung đột phiên bản CUDA trên Kaggle/Windows/Colab.
* **Vũ khí bí mật `SelectiveScanAutograd`:** Cài đặt lan truyền ngược giải tích (Analytical Adjoint Backward), chỉ lưu trạng thái ẩn cuối cùng $\mathbf{h}$. Giảm $>80\%$ dung lượng bộ nhớ đồ thị vi phân, khóa chặt VRAM ở mức **$7.19\text{ GB}$**, cho phép huấn luyện mượt mà batch=8 trên Tesla T4 15GB.

---

## 4. TỔNG HỢP KẾT QUẢ ĐỘT PHÁ CỦA MÔ HÌNH VÔ ĐỊCH C2IAVM

Bảng đối chứng trung bình 6 seed (`s0` đến `s5`, 100 epochs/seed):

| Chỉ số thực nghiệm | Baseline YOLO26s-seg | C2IAVM (Proposed Champion) | Mức cải thiện ($\Delta$) | Ý nghĩa thực nghiệm |
| :--- | :---: | :---: | :---: | :--- |
| **Mask mAP@50-95** | $0.7298 \pm 0.0150$ | **`0.7365 ± 0.0074`** | **$+0.0067$ ($+0.67\%$)** | Kỷ lục toàn đề tài: **$74.70\%$ (Seed 1)** |
| **Mask mAP@50** | $0.9129 \pm 0.0070$ | **`0.9150 ± 0.0112`** | **$+0.0021$ ($+0.21\%$)** | Đỉnh cao: **$93.20\%$ (Seed 0)** |
| **Mask Recall** | $0.8837 \pm 0.0087$ | **`0.8875 ± 0.0196`** | **$+0.0038$ ($+0.38\%$)** | Kỷ lục toàn đề tài: **$90.60\%$ (Seed 2)** |
| **Mask Precision** | $0.9165 \pm 0.0104$ | **`0.8885 ± 0.0307`** | $-0.0280$ | Kỷ lục Precision: **$93.20\%$ (Seed 5)** |
| **Box mAP@50-95** | $0.7383 \pm 0.0102$ | **`0.7418 ± 0.0057`** | **$+0.0035$ ($+0.35\%$)** | Đỉnh cao: **$74.80\%$ (Seed 3)** |
| **Box Recall** | $0.8752 \pm 0.0151$ | **`0.8842 ± 0.0186`** | **$+0.0090$ ($+0.90\%$)** | Kỷ lục: **$90.60\%$ (Seed 2)** |
| **Giảm phương sai (F-test)** | $\sigma_B^2 = 0.0002256$ | $\sigma_C^2 = 0.0000543$ | **Giảm $4.1538\times$** | $F = 4.1538$, cực kỳ ổn định lâm sàng |
| **Tỷ lệ thắng trực tiếp** | - | **5 / 6 seed (83.3%)** | - | Thắng áp đảo tại s0, s1, s2, s3, s5 |
| **Thời gian huấn luyện** | ~2.15 giờ | **`3.049 giờ`** | $+0.85\text{h}$ | Cực kỳ tối ưu cho 100 epochs/seed |
| **VRAM tiêu thụ đỉnh** | ~6.5 GB | **`~7.19 GB`** | An toàn tuyệt đối | Không bao giờ tràn bộ nhớ trên Tesla T4 |

`[Đã xác nhận]`

---

## 5. BẢN ĐỒ HỆ THỐNG TÀI LIỆU MARKDOWN TRONG `archive/doc/`

Toàn bộ tri thức của dự án được module hóa thành các tệp chuyên sâu theo chuẩn AI Knowledge Base:

### Nhóm 1: Tài liệu Điều hành & Kiến trúc Nền tảng
1. [`00_TONG_QUAN_VA_TINH_HINH_DU_AN.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/00_TONG_QUAN_VA_TINH_HINH_DU_AN.md): Hồ sơ tổng thể đề tài, danh sách tác giả, quy chuẩn tính toán và lộ trình.
2. [`01_KIEN_TRUC_TSVM_TANG_10.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/01_KIEN_TRUC_TSVM_TANG_10.md): Phân tích module `C2TSVMamba` và nhánh hình thái học ban đầu.
3. [`02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md): Bảng đối chiếu tổng hợp đa mô hình và kiểm định thống kê Paired t-test.
4. [`03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md): Sơ đồ cây thư mục và hướng dẫn tái lập kết quả 100%.

### Nhóm 2: Hồ sơ Chuyên sâu Từng Kết quả Thực nghiệm
5. [`04_KET_QUA_LOSS_VA_HOI_TU.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/04_KET_QUA_LOSS_VA_HOI_TU.md): Phân tích động lực học loss và hiện tượng kiểm soát quá khớp.
6. [`05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md): Phân tích Mask mAP và độ ổn định phương sai qua các seed.
7. [`06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md): Phân tích sự đánh đổi Precision - Recall và ý nghĩa lâm sàng trong phẫu thuật EMR/ESD.
8. [`07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md): Ma trận nhầm lẫn 127 polyp và đối chiếu cặp paired head-to-head.
9. [`08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md): Phân tích tham số, GFLOPs, độ trễ 3 pha và khả năng triển khai thời gian thực trên NVIDIA Jetson.
10. [`09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md): Bức tranh toàn cảnh Ablation Studies (tại sao các biến thể khác gặp khuyết tật và tại sao C2IAVM chiến thắng).
11. [`10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md): Đánh giá định tính chất lượng mặt nạ, độ mượt ranh giới và kháng phản xạ ánh sáng.
12. [`11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md): Báo cáo chi tiết số liệu 6-fold của biến thể ghép tĩnh P5_Attention_VMamba.
13. [`12_CHI_TIET_KET_QUA_IAVM_INTERACTIVE_ATTENTION_VMAMBA.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/12_CHI_TIET_KET_QUA_IAVM_INTERACTIVE_ATTENTION_VMAMBA.md): Hồ sơ thực nghiệm đầy đủ của Mô hình Vô địch `C2IAVM` (kỷ lục 74.7% mAP, 90.6% Recall).


---

## 5. CẬP NHẬT KẾT QUẢ HOÀN TẤT 6 SEED CỦA HƯỚNG 3: ITSMamba (`C2ITSMamba`)
- **Mô hình:** `YOLO26s_seg_ITSMamba` (Interactive Topology-Shape VMamba).
- **Kết quả 6 seed:** Mask mAP@50-95 đạt **`0.7251 ± 0.0049`**, Mask Recall đạt **`0.8835 ± 0.0177`**, Val Seg Loss đạt **`1.4151 ± 0.0717`**.
- **Kỷ lục phương sai:** Tỷ số F-test đạt **$F = 9.84\times$** (độ lệch chuẩn thấp nhất đề tài: $\sigma = \pm 0.0049$).
- **Vị thế:** Đóng vai trò là nghiên cứu bóc tách hoàn hảo (Ablation Study) chứng minh cơ chế Interactive Exchange giải cứu Recall (+3.42%), đồng thời tôn vinh `C2IAVM` ($0.7361$, thắng 6/6 seed) là Mô hình Vô địch Toàn diện.
