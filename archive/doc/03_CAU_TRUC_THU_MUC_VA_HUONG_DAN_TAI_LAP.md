# CẤU TRÚC THƯ MỤC, VAI TRÒ CÁC TỆP TIN & HƯỚNG DẪN TÁI LẬP
## BẢN ĐỒ DỰ ÁN DÀNH CHO CÁC AI VÀ KỸ SƯ TIẾP QUẢN

---

## 1. SƠ ĐỒ CÂY THƯ MỤC DỰ ÁN

Toàn bộ tài nguyên của đề tài phân đoạn polyp được tổ chức mạch lạc như sau:

```
c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\
│
├── ultralytics_Topology-Shape-aware VMamba\   <-- CODEBASE CHÍNH CỦA MÔ HÌNH TSVM
│   ├── cfg\models\26\
│   │   ├── yolo26-seg-TopologyShapeVMamba.yaml  (Cấu hình kiến trúc TSVM tại tầng 10)
│   │   └── yolo26-seg.yaml                     (Cấu hình kiến trúc Baseline YOLO26s-seg)
│   ├── nn\modules\
│   │   └── topology_shape_vmamba.py            (Code nguồn module C2TSVMamba và 6 khối con)
│   └── tests\
│       └── test_topology_shape_vmamba.py       (Bộ test suite 24 bài kiểm thử của nhóm)
│
├── Ket_Qua_2\                                  <-- DỮ LIỆU HUẤN LUYỆN 6-FOLD THỰC TẾ
│   ├── Kvasir_Baseline_YOLO26s_seg_s0_w2\      (Kết quả Baseline fold 0: results.csv, weights)
│   ├── ...                                     (s1 đến s5 của Baseline)
│   ├── Kvasir_YOLO26s_seg_TSVM_s0_w2\          (Kết quả TSVM fold 0: results.csv, weights)
│   └── ...                                     (s1 đến s5 của TSVM)
│
├── doc\                                        <-- TÀI LIỆU DÀNH CHO AI TIẾP QUẢN
│   ├── 00_TONG_QUAN_VA_TINH_HINH_DU_AN.md      (Bản tóm lược điều hành & tình hình dự án)
│   ├── 01_KIEN_TRUC_TSVM_TANG_10.md            (Phân tích chi tiết code module tầng 10)
│   ├── 02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md  (Bảng số liệu thực nghiệm & kiểm định p-value)
│   └── 03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md (Bản đồ thư mục & hướng dẫn thực thi)
│
├── Kvasir_YOLO_SEG_BG20\                       <-- BỘ DỮ LIỆU MỞ RỘNG BỔ SUNG 20% ẢNH NỀN (1.200 ẢNH)
│   ├── images\ (train: 1.040, val: 160)
│   ├── labels\ (train: 1.040 [160 rỗng], val: 160 [40 rỗng])
│   ├── selected_normal_cecum_train_160.txt     (Lưu vết ID 160 ảnh nền train)
│   ├── selected_normal_cecum_val_40.txt       (Lưu vết ID 40 ảnh nền val)
│   └── data_bg20.yaml                         (File cấu hình Ultralytics YOLO cho tập BG20)
│
├── normal-cecum\                              <-- KHO DỮ LIỆU GỐC 1.000 ẢNH KHÔNG BỆNH (KVASIR V2)
│   └── normal-cecum\                          (1.000 file ảnh .jpg niêm mạc manh tràng lành)
│
├── data_bg20.yaml                             (Bản sao cấu hình YAML tại thư mục gốc)
│
├── Stracth\                                    <-- CÁC SCRIPT PYTHON THỰC THI ĐỘC LẬP
│   ├── convert_kvasir_with_background_to_yolo_seg.py (Script tiền xử lý độc lập tạo dataset BG20)
│   ├── evaluate_baseline_vs_tsvm.py            (Tính toán & in bảng kiểm định thống kê)
│   ├── verify_tsvm_layer10.py                  (Kiểm thử forward/backward tensor tầng 10)
│   ├── export_benchmark_summary.py             (Xuất dữ liệu 6-fold ra các file CSV)
│   ├── baseline_vs_tsvm_folds.csv              (Bảng số liệu từng fold chi tiết)
│   └── baseline_vs_tsvm_aggregated.csv         (Bảng số liệu tổng hợp Mean/Std/p-value)
│
├── Baocao\                                     (Bản thảo Word đồ án khóa luận)
│   └── Bao_cao_Khoa_luan_Cu_nhan_VMamba_YOLO26-seg_Polyp.docx
│
└── CNTT_KLCN182-Phung The Bao.docx             (Đề cương chi tiết khóa luận có chữ ký GVHD)
```

---

## 2. HƯỚNG DẪN THỰC THI VÀ TÁI LẬP KẾT QUẢ (REPRODUCIBILITY)

Bất kỳ AI hoặc kỹ sư nào khi tiếp quản dự án đều có thể kiểm tra và tái lập toàn bộ số liệu bằng các câu lệnh sau:

### Bước 1: Kiểm thử kiến trúc module Tầng 10
Chạy script kiểm tra độc lập để xác minh tính toàn vẹn của module `C2TSVMamba`:
```bash
python "c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\verify_tsvm_layer10.py"
```
*Kết quả kỳ vọng:* Xuất ra thông báo `[+] PASS: Forward Pass hoan hao` và `[+] PASS: Backward Pass thanh cong`.

### Bước 2: Tái lập bảng so sánh thống kê 6-Fold
Chạy script đọc 12 tệp `results.csv` và tính toán lại toàn bộ chỉ số kèm $p$-value:
```bash
python "c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\evaluate_baseline_vs_tsvm.py"
```
*Kết quả kỳ vọng:* In bảng so sánh Mean ± Std và khẳng định `val/seg_loss` có $p = 0.0363 < 0.05$.

### Bước 3: Xuất số liệu dạng bảng CSV sạch
Chạy script xuất dữ liệu ra file bảng tính để chèn vào Excel hoặc Word:
```bash
python "c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\export_benchmark_summary.py"
```
*Kết quả:* Tạo ra 2 tệp `baseline_vs_tsvm_folds.csv` và `baseline_vs_tsvm_aggregated.csv` trong thư mục `Stracth/`.

---

## 3. CHECKLIST CÔNG VIỆC CẦN LÀM TIẾP THEO (NEXT STEPS)

- [x] Giải nén toàn bộ các tệp kết quả của Baseline và TSVM ra thư mục làm việc.
- [x] Phân tích code kiến trúc module Tầng 10 (`C2TSVMamba`).
- [x] Lập bảng so sánh đối chiếu và kiểm định ý nghĩa thống kê Paired t-test ($p < 0.05$).
- [x] Xây dựng các script thực thi độc lập đặt tại thư mục `Stracth/`.
- [x] Viết tài liệu bàn giao dự án hoàn chỉnh tại thư mục `doc/`.
- [ ] Cập nhật bảng số liệu thực tế này vào **Chương 5 (Kết quả thực nghiệm & Thảo luận)** của bản thảo luận văn `Baocao/Bao_cao_Khoa_luan_Cu_nhan_VMamba_YOLO26-seg_Polyp.docx`.
- [ ] Chuẩn bị slide PowerPoint tóm tắt luận điểm: *"TSVM cải thiện đáng kể loss phân đoạn ranh giới polyp (p=0.0363) và giảm phương sai giữa các fold 3 lần, giải quyết đúng mục tiêu của đề tài."*
