# 🔬 Nghiên Cứu Phương Pháp Tích Hợp VMamba Vào YOLO26-seg Trong Phân Đoạn Polyp Nội Soi Đại Trực Tràng

> **Khóa luận Cử nhân ngành Công Nghệ Thông Tin (2026 – 2027) — Trường Đại học Công Thương TP.HCM (HUIT)**  
> **Mã đề tài:** `CNTT_KLCN182`  
> **Giảng viên hướng dẫn:** ThS. Phùng Thế Bảo (`baopt@huit.edu.vn`)  
> **Nhóm sinh viên thực hiện:** Lê Đức Lương (2001230490), Phùng Tuấn Huy (2001230312), Trần Mạnh Toàn (2001230830)  
> **Mô hình đề xuất cốt lõi (👑 PROPOSED CHAMPION MODEL):** `Attention-VMamba Fusion` (`C2IAVM`)

---

## 📑 HỆ THỐNG TÀI LIỆU KNOWLEDGE BASE (13 TỆP MARKDOWN CHUYÊN SÂU)

Toàn bộ hệ thống tài liệu được module hóa chặt chẽ theo chuẩn AI-Consumable Knowledge Base:

### 1. Tài liệu Kiến trúc & Điều hành Cốt lõi
* 📘 [`00_TONG_QUAN_VA_TINH_HINH_DU_AN.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/00_TONG_QUAN_VA_TINH_HINH_DU_AN.md): Bối cảnh đề tài, thông tin nhóm tác giả, quy chuẩn tính toán Pure PyTorch trên CUDA và bảng đối chứng 6 seed của `C2IAVM`.
* 💻 [`01_KIEN_TRUC_C2IAVM_CHAMPION_VA_CAC_BIEN_THE.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/01_KIEN_TRUC_C2IAVM_CHAMPION_VA_CAC_BIEN_THE.md): Bản đặc tả kỹ thuật kiến trúc, luồng tensor, thuật toán quét Hillis-Steele $\mathcal{O}(\log_2 L)$ và lớp vi phân giải tích `SelectiveScanAutograd`.
* 📊 [`02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md): Bảng số liệu thực nghiệm 6-fold đối chứng 3 mô hình (Baseline vs TSVM vs C2IAVM), kiểm định F-test giảm phương sai $4.39\times$ và Paired t-test.
* 🗂️ [`03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md): Sơ đồ các thư mục workspace và hướng dẫn tái lập kết quả thực nghiệm 100%.

### 2. Hồ sơ Phân tích Từng Kết quả Chuyên sâu (Deep-Dive Dossiers)
* 📈 [`04_KET_QUA_LOSS_VA_HOI_TU.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/04_KET_QUA_LOSS_VA_HOI_TU.md): Phân tích động lực học loss, kiểm soát hàm phạt phân đoạn và chống quá khớp cuối khóa.
* 🎯 [`05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md): Phân tích chi tiết Mask mAP@50-95, kiểm định F-test co hẹp phương sai 4.39x và tỷ lệ thắng 83.33%.
* ⚕️ [`06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md): Đánh đổi Precision vs Recall, phân tích lâm sàng phát hiện 112.7/127 polyp, giảm tỷ lệ bỏ sót xuống 11.25%.
* 🔍 [`07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md): Ma trận nhầm lẫn chuẩn hóa đối chiếu và đường cong Precision-Recall phân đoạn.
* ⚡ [`08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md): Tham số (12.14M), GFLOPs (40.8), độ trễ 3 pha (25.0 ms), tốc độ 40.0 FPS trên GPU T4.
* 🔬 [`09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md): Khảo sát thực nghiệm bóc tách 8 biến thể (P5 vs P3 Sobel vs Ghép tĩnh vs C2IAVM).
* 🖼️ [`10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md): So sánh trực quan chất lượng mặt nạ phân đoạn đối chiếu Ground Truth.
* 📋 [`11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md): Chi tiết kết quả thực nghiệm biến thể P5.
* 🏆 [`12_CHI_TIET_KET_QUA_IAVM_INTERACTIVE_ATTENTION_VMAMBA.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/12_CHI_TIET_KET_QUA_IAVM_INTERACTIVE_ATTENTION_VMAMBA.md): Hồ sơ toàn diện về mô hình vô địch C2IAVM.

---

## 🎨 HỆ THỐNG BIỂU ĐỒ ĐỐI CHUẨN XUẤT BẢN (300 DPI)

Hai thư mục biểu đồ đã được kết xuất hoàn chỉnh, đối xứng 100%:
1. 📁 [`KQ_DoiXung/Base vs IAVM`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20IAVM): **45 tệp biểu đồ** đối chiếu Baseline vs Mô hình vô địch C2IAVM (Cột, Tròn/Donut, Radar, Boxplot, Đường cong hội tụ 100 epoch).
2. 📁 [`KQ_DoiXung/Base vs Topolo`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_DoiXung/Base%20vs%20Topolo): **46 tệp biểu đồ** đối chiếu Baseline vs Mô hình thử nghiệm TSVM.
