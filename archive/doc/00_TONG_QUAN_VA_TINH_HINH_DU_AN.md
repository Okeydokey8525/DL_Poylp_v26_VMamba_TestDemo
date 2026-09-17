# TỔNG QUAN DỰ ÁN & BÀN GIAO TRẠNG THÁI HIỆN TẠI
## DÀNH CHO CÁC AI VÀ KỸ SƯ TIẾP QUẢN DỰ ÁN

---

> [!IMPORTANT]
> **THÔNG TIN ĐỀ TÀI KHÓA LUẬN CỬ NHÂN**
> - **Mã đề tài:** `CNTT_KLCN182`
> - **Tên đề tài:** *Nghiên cứu phương pháp tích hợp VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng*
> - **Giảng viên hướng dẫn:** ThS. Phùng Thế Bảo (Khoa CNTT - Trường Đại học Công Thương TP.HCM - HUIT)
> - **Sinh viên thực hiện:** Lê Đức Lương (MSSV: 2001230490 - Lớp: 14DHTH09) cùng nhóm nghiên cứu
> - **Tập dữ liệu:** Kvasir-SEG (1.000 ảnh nội soi đại trực tràng có ground-truth mask pixel)
> - **Quy trình thẩm định:** 6-Fold Cross-Validation (`s0` đến `s5`), 100 epochs/fold, `batch=8`, `imgsz=640`

---

## 1. MỤC TIÊU CỐT LÕI VÀ BỐI CẢNH NGHIÊN CỨU

Theo đề cương chi tiết đã được GVHD duyệt:
1. **Thách thức:** Các mô hình học sâu hiện nay (như YOLO-seg tiêu chuẩn) gặp khó khăn trong việc phân đoạn polyp có đường biên mờ, dải màu tương đồng với niêm mạc xung quanh, hoặc hình thái dị dạng phức tạp.
2. **Giải pháp đề xuất:** Tích hợp cơ chế Không gian Trạng thái Thị giác (**Visual State-Space - VMamba**) với khả năng mô hình hóa ngữ cảnh toàn cục tuyến tính $O(N)$ kết hợp định hướng hình thái và cấu trúc topo (**Topology-Shape Awareness**) vào mô hình **YOLO26-seg**.
3. **Trọng tâm đánh giá:** Đo lường đồng thời độ chính xác phân đoạn mặt nạ (Mask mAP50, mAP50-95, Precision, Recall, F1, Loss phân đoạn) và chi phí tài nguyên (tham số, kích thước checkpoint, thời gian huấn luyện).

---

## 2. QUYẾT ĐỊNH CHIẾN LƯỢC QUAN TRỌNG: LỰA CHỌN MÔ HÌNH BÁO CÁO

Trong quá trình nghiên cứu thực nghiệm, nhóm đã phát triển và chạy 6-fold cross-validation cho 2 biến thể cải tiến:
1. **Biến thể 1: `TSVM` (Topology-Shape-aware VMamba)** tại tầng 10 (thay thế khối `C2PSA`).
2. **Biến thể 2: `P5_Attention_VMamba` (Parallel Attention || VMamba)** tại tầng 10.

### Kết quả thẩm định thực tế & Quyết định:
- **Biến thể `P5_Attention_VMamba`:** Mặc dù tăng được Recall phát hiện hộp bao, nhưng lại làm **hàm mất mát phân đoạn tăng lên 1.4626** (tệ hơn cả Baseline 1.4314) và **làm suy giảm Mask Precision nghiêm trọng** ($p = 0.0023$). Điều này đi ngược trực tiếp với mục tiêu *"sinh mặt nạ sắc nét, bám sát tổn thương"* của đề cương.
- **Biến thể `TSVM` (Topology-Shape-aware VMamba):** Đạt được sự cải thiện vượt bậc và có ý nghĩa thống kê về mặt nạ phân đoạn:
  - **Validation Segmentation Loss (`val/seg_loss`) giảm có ý nghĩa thống kê ($p = 0.0363 < 0.05$)** từ 1.4314 xuống 1.3936 (thấp hơn Baseline ở 5/6 fold).
  - **Độ ổn định (phương sai) giữa các fold giảm gần 3 lần** ($Std = 0.0055$ so với $0.0153$ của Baseline).
  - Mask Precision duy trì mức rất cao **0.9192** (ngang ngửa Baseline 0.9198).

> [!NOTE]
> **QUYẾT ĐỊNH:**
> Toàn bộ tài liệu, báo cáo, và công việc tiếp theo **TẬP TRUNG 100% VÀO `TSVM` VÀ `BASELINE`**.
> Mô hình `P5_Attention_VMamba` không dùng làm kết quả chính, chỉ được dùng làm bằng chứng phụ trong phần *Ablation Study* (nghiên cứu bóc tách biến thể).

---

## 3. TỔNG QUAN HỆ THỐNG TÀI LIỆU TIẾP QUẢN TRONG THƯ MỤC `doc/`

Để hỗ trợ AI hoặc thành viên tiếp quản nắm bắt ngay lập tức toàn bộ dự án, hệ thống tài liệu được tổ chức theo chuẩn **AI-Consumable Project Knowledge Base** (phù hợp với `nguyen-tac-lam-viec-dai.md`):

### Nhóm 1: Tài liệu Kiến trúc & Điều hành Cốt lõi
1. [`00_TONG_QUAN_VA_TINH_HINH_DU_AN.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/00_TONG_QUAN_VA_TINH_HINH_DU_AN.md): Bản tóm lược điều hành, bối cảnh, các quyết định cốt lõi và lộ trình tiếp theo.
2. [`01_KIEN_TRUC_TSVM_TANG_10.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/01_KIEN_TRUC_TSVM_TANG_10.md): Phân tích kỹ thuật chuyên sâu về mã nguồn module `C2TSVMamba` tại tầng 10, cấu trúc toán học của 6 khối con, luồng tensor và file YAML.
3. [`02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md): Bảng số liệu tổng hợp đối chiếu 6-fold, kiểm định thống kê Paired t-test ($p$-values) và các kết luận cốt lõi.
4. [`03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md): Bản đồ phân bố file trong toàn bộ workspace, vị trí code, script thực thi tại `Stracth/`, và hướng dẫn tái lập kết quả 100%.

### Nhóm 2: Hồ sơ Chuyên sâu Từng Kết quả Thực nghiệm (Deep-Dive Result Dossiers)
5. [`04_KET_QUA_LOSS_VA_HOI_TU.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/04_KET_QUA_LOSS_VA_HOI_TU.md): Phân tích hàm mất mát phân đoạn (`val/seg_loss`), động lực học hội tụ 100 epochs, kiểm soát quá khớp (overfitting bounce) và kiểm định $p = 0.0363$.
6. [`05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md): Phân tích chi tiết Mask mAP@50 (0.9134), Mask mAP@50-95 (0.7246) và phát hiện đột phá: **thu hẹp độ lệch chuẩn (Std) 3 lần** ($0.0150 
ightarrow 0.0050$).
7. [`06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md): Phân tích sự đánh đổi Precision (91.71%) vs Recall (85.45%), nguyên nhân hình thái học ở polyp dạng phẳng (Paris IIb, < 5mm) và giá trị sống còn trong phẫu thuật EMR/ESD.
8. [`07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md): Ma trận nhầm lẫn và đếm số ca tổn thương trên 127 polyp kiểm thử, đối chiếu cặp từng seed (Paired Head-to-Head), lý giải tính chất các ca False Negative.
9. [`08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md): Tham số (12.09M), GFLOPs (42.3), dung lượng tệp `best.pt` (23.86 MB), phân rã độ trễ 3 pha (Pre 0.4ms, Inf 19.0ms, Post 1.8ms), thông lượng 47.2 FPS đáp ứng chuẩn nội soi thời gian thực (25-30 FPS).
10. [`09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md): Nghiên cứu triệt tiêu (Ablation Study) chứng minh vì sao tích hợp tại Tầng 10 (Neck chuyển tiếp, stride 16) vượt trội hoàn toàn so với đặt tại tầng P5 sâu nhất (stride 32).
11. [`10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md): Đánh giá định tính hình thái mặt nạ, triệt tiêu răng cưa, chống lem mô lành và kháng phản xạ ánh sáng (glare).
12. [`11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md): Báo cáo chi tiết số liệu 6-fold của biến thể P5_Attention_VMamba, phân tích nguyên nhân suy thoái hiệu năng và giá trị trong Ablation Study.](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md): Đánh giá định tính hình thái mặt nạ trực quan, triệt tiêu răng cưa, chống lem viền mô lành và khả năng kháng nhiễu phản xạ ánh sáng (glare reflection).

---

## 4. NGUYÊN TẮC LÀM VIỆC BẮT BUỘC CHO AI TIẾP QUẢN
1. **Tuyệt đối trung thực (No Fabrication):** Mọi số liệu báo cáo phải được trích xuất từ 12 file `results.csv` thực tế của 6 splits. Không tự ý bịa đặt số liệu để làm cho kết quả "nghe có vẻ đẹp hơn".
2. **Tôn trọng sự thật khoa học:** Thừa nhận thẳng thắn sự đánh đổi (Trade-off): TSVM tối ưu hóa ranh giới mặt nạ (`val/seg_loss` giảm, std giảm 3 lần), nhưng bị giảm nhẹ Mask Recall (-3.04%) và thời gian huấn luyện tăng 2.06 lần do cơ chế quét 2D tuần tự của Mamba.
3. **Phân biệt rõ mức độ chắc chắn:**
   - **[Đã xác nhận]:** Có số liệu cụ thể từ `results.csv`, code trong `topology_shape_vmamba.py` hoặc log chạy thực tế.
   - **[Suy luận / Phân tích]:** Giải thích bản chất hiện tượng dựa trên kiến trúc và lý thuyết toán học.
   - **[Chưa xác minh]:** Những thí nghiệm chưa chạy (như test trên tập ngoài ETIS-Larib hay CVC-ClinicDB).
