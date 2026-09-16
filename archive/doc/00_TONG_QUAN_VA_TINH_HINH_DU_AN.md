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

## 3. TỔNG QUAN CÁC TÀI LIỆU TIẾP QUẢN TRONG THƯ MỤC `doc/`

Để hỗ trợ AI hoặc thành viên tiếp quản nắm bắt ngay lập tức toàn bộ dự án, hệ thống tài liệu được phân chia thành các tệp chuyên sâu:

1. [`00_TONG_QUAN_VA_TINH_HINH_DU_AN.md`](file:///c:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/00_TONG_QUAN_VA_TINH_HINH_DU_AN.md): Bản tóm lược điều hành, bối cảnh, các quyết định cốt lõi và lộ trình tiếp theo.
2. [`01_KIEN_TRUC_TSVM_TANG_10.md`](file:///c:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/01_KIEN_TRUC_TSVM_TANG_10.md): Phân tích kỹ thuật chuyên sâu về mã nguồn của module `C2TSVMamba` tại tầng 10, cấu trúc toán học của 6 khối con, luồng tensor và file YAML.
3. [`02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md`](file:///c:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md): Toàn bộ bảng số liệu thực tế 6-fold, kiểm định thống kê Paired t-test ($p$-values), phân tích ưu/nhược điểm và lập luận khoa học cho luận văn.
4. [`03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md`](file:///c:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md): Bản đồ phân bố file trong toàn bộ workspace, vị trí code, script thực thi tại `Stracth/`, và hướng dẫn tái lập kết quả 100%.

---

## 4. NGUYÊN TẮC LÀM VIỆC BẮT BUỘC CHO AI TIẾP QUẢN
1. **Tuyệt đối trung thực (No Fabrication):** Mọi số liệu báo cáo phải được trích xuất từ 12 file `results.csv` thực tế của 6 splits. Không tự ý bịa đặt số liệu để làm cho kết quả "nghe có vẻ đẹp hơn".
2. **Tôn trọng sự thật khoa học:** Thừa nhận thẳng thắn sự đánh đổi (Trade-off): TSVM tối ưu hóa ranh giới mặt nạ (`val/seg_loss` giảm, std giảm 3 lần), nhưng bị giảm nhẹ Mask Recall (-3.04%) và thời gian huấn luyện tăng 2.06 lần do cơ chế quét 2D tuần tự của Mamba.
3. **Phân biệt rõ mức độ chắc chắn:**
   - **[Đã xác nhận]:** Có số liệu cụ thể từ `results.csv`, code trong `topology_shape_vmamba.py` hoặc log chạy thực tế.
   - **[Suy luận / Phân tích]:** Giải thích bản chất hiện tượng dựa trên kiến trúc và lý thuyết toán học.
   - **[Chưa xác minh]:** Những thí nghiệm chưa chạy (như test trên tập ngoài ETIS-Larib hay CVC-ClinicDB).
