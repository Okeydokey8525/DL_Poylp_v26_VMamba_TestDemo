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
├── Ket_Qua_2\                                  <-- DỮ LIỆU HUẤN LUYỆN 6-FOLD GỐC (KVASIR-SEG)
│   ├── YOLO26s_seg_IAVM\                       (Kết quả C2IAVM 6 seed)
│   ├── YOLO26s_seg_ITSMamba\                   (Kết quả ITSMamba 6 seed)
│   ├── YOLO26s_seg_P5_Attention_VMamba\        (Kết quả P5_Attention 6 seed)
│   └── YOLO26s_seg_TSVM\                       (Kết quả TSVM 6 seed)
│
├── KetQua_Nen\                                 <-- KHO KẾT QUẢ HUẤN LUYỆN TRÊN TẬP MỞ RỘNG BG20
│   ├── YOLOv26s-seg\                           (Baseline YOLO26s-seg: Đủ 10 seed s0 -> s9)
│   ├── Kvasir_BG20_YOLO26s_seg_TSVM\           (TSVM: Đủ 10 seed s0 -> s9)
│   ├── Kvasir_BG20_YOLO26s_seg_P5_Attention_VMamba\ (P5_Attention: Đủ 10 seed s0 -> s9)
│   ├── Kvasir_BG20_YOLO26s_seg_ITSMamba\       (ITSMamba: Đủ 10 seed s0 -> s9)
│   └── Kvasir_BG20_YOLO26s_seg_IAVM\           (C2IAVM: Đã hoàn tất 7 seed s0 -> s6)
│
├── KQ_Nen_DX_10seed\                           <-- BỘ PHÂN TÍCH & TRỰC QUAN HÓA 10 SEED (BASELINE VS TSVM)
│   ├── 01_raw_analysis\                        (20 records trích xuất từ results.csv và ma trận nhầm lẫn)
│   ├── 02_statistics\                          (Mean±Std, Min-Max, Seed-by-seed deltas, Win/Loss)
│   ├── 03_metrics\                             (Segmentation, Bounding Box, Loss sub-tables)
│   ├── 04_confusion_matrix\                    (Ma trận đếm và ma trận % chuẩn hóa trung bình 10 seed)
│   ├── 05_charts\                              (20 biểu đồ nghiên cứu khoa học đạt chuẩn 300 DPI)
│   ├── 06_reports\                             (Báo cáo tổng hợp summary.md, conclusions.md, summary.csv)
│   └── README.md                               (Tài liệu mục lục và hướng dẫn chi tiết gói 10 seed)
│
├── Khac_phuc\                                  <-- ARTIFACT KHÔI PHỤC 24 ẢNH CHUẨN (KHÔNG FUSE)
│   ├── Kvasir_BG20_YOLO26s_seg_TSVM_s0_w2\     (Trọn bộ 24 ảnh chuẩn 300 DPI seed 0)
│   └── Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2\     (Trọn bộ 24 ảnh chuẩn 300 DPI seed 5)
│
├── doc\                                        <-- TÀI LIỆU DÀNH CHO AI TIẾP QUẢN
│   ├── 00_TONG_QUAN_VA_TINH_HINH_DU_AN.md      (Bản tóm lược điều hành & tình hình dự án)
│   ├── 01_KIEN_TRUC_TSVM_TANG_10.md            (Phân tích chi tiết code module tầng 10)
│   ├── 02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md  (Bảng số liệu thực nghiệm & kiểm định p-value)
│   └── 03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md (Bản đồ thư mục & hướng dẫn thực thi)
│
├── Kvasir_YOLO_SEG_BG20\                       <-- TẬP DỮ LIỆU CHÍNH THỨC CỦA ĐỀ TÀI (1.200 ẢNH, ĐÃ HUẤN LUYỆN 10 SEEDS)
│   ├── images\ (train: 1.040 [880 polyp + 160 nền], val: 160 [120 polyp + 40 nền])
│   ├── labels\ (train: 1.040 [160 rỗng 0-byte], val: 160 [40 rỗng 0-byte])
│   ├── selected_normal_cecum_train_160.txt     (Lưu vết ID 160 ảnh nền train)
│   ├── selected_normal_cecum_val_40.txt       (Lưu vết ID 40 ảnh nền val)
│   └── data_bg20.yaml                         (File cấu hình Ultralytics YOLO chính thức cho tập BG20)
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

### Bước 2: Tái lập kiểm toán và phân tích 10 Seed trên tập BG20
Chạy script tổng hợp và kiểm toán tự động kết quả thực nghiệm 10 seeds (`s0` đến `s9`) trên tập dữ liệu chính thức `Kvasir_YOLO_SEG_BG20`:
```bash
python "c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Stracth\summarize_ketqua_nen.py"
```
*Kết quả:* Kiểm toán 47 runs trong `KetQua_Nen/` và xuất file tổng hợp `bg20_all_seeds_metrics.csv`.

### Bước 3: Tái lập toàn bộ 20 biểu đồ khoa học 10 Seed (Baseline vs TSVM)
Chạy script phân tích đối sánh 10 seed tại thư mục `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/`:
- Dữ liệu thống kê: [`06_reports/summary.csv`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/summary.csv)
- Báo cáo nhận xét học thuật: [`06_reports/conclusions.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/conclusions.md)
- 20 biểu đồ 300 DPI trong `05_charts/` và 12 biểu đồ template đối xứng chuẩn hóa trong `figures/`.

### Bước 4: Tái lập Benchmark Hiệu năng Độc lập (Efficiency Benchmark)
Thực thi đo đạc tham số, GFLOPs, dung lượng checkpoint, thời gian trễ và FPS trên CPU:
- Báo cáo chi tiết: [`efficiency_benchmark/reports/benchmark_report.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/reports/benchmark_report.md)
- Bảng tổng hợp: [`efficiency_benchmark/tables/accuracy_efficiency_summary.csv`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/tables/accuracy_efficiency_summary.csv)

---

## 3. CHECKLIST CÔNG VIỆC CỦA DỰ ÁN

- [x] Chuẩn hóa bộ dữ liệu chính thức `Kvasir_YOLO_SEG_BG20` (1.200 ảnh, bổ sung 20% ảnh nền âm tính `normal-cecum`).
- [x] Huấn luyện hoàn tất 10 random seeds (`s0`–`s9`) trên Kaggle GPU Tesla T4 cho Baseline và TSVM (lưu tại `KetQua_Nen/`).
- [x] Kiểm toán dữ liệu và giải quyết triệt để sự cố `model.fuse()` khi xuất ảnh Kaggle.
- [x] Xây dựng bộ phân tích đối sánh 10 seed chuyên sâu (39 tệp dữ liệu, 20 biểu đồ 300 DPI) tại `KQ_Nen_DX_10seed/`.
- [x] Đo đạc và xây dựng bộ benchmark hiệu năng tính toán độc lập tại `efficiency_benchmark/`.
- [x] Đồng bộ hóa toàn bộ tài liệu thuyết minh và báo cáo kỹ thuật tại `doc/`.
- [ ] Tích hợp bảng số liệu 10 seed và hệ thống biểu đồ đạt chuẩn vào bản thảo luận văn Word (`Baocao/Bao_cao_Khoa_luan_Cu_nhan_VMamba_YOLO26-seg_Polyp.docx`).
