# 🔬 Nghiên Cứu Phương Pháp Tích Hợp Topology-Shape-aware VMamba Vào YOLO26-seg Cho Phân Đoạn Polyp Từ Ảnh Nội Soi Đại Trực Tràng

> **Dự án Khóa luận tốt nghiệp Cử nhân / Đồ án Nghiên cứu Deep Learning y khoa**  
> **Chủ đề:** Tích hợp mô hình trạng thái không gian (State Space Models / VMamba) kết hợp đặc trưng hình học (Shape) và cấu trúc liên kết (Topology) vào kiến trúc YOLO26-seg trong bài toán phân đoạn polyp trực tràng.

---

## 📑 Liên Kết Nhanh & Tài Liệu Quan Trọng

### 📚 HỆ THỐNG HỒ SƠ PHÂN TÍCH THỰC NGHIỆM ĐỊNH LƯỢNG (AI KNOWLEDGE BASE)

Hệ thống tài liệu Markdown phân rã toàn diện từng kết quả theo chuẩn `nguyen-tac-lam-viec-dai.md`:

* 📑 **Kiến trúc & Bàn giao Điều hành:**
  * [`00_TONG_QUAN_VA_TINH_HINH_DU_AN.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/00_TONG_QUAN_VA_TINH_HINH_DU_AN.md): Bối cảnh nghiên cứu, quyết định chiến lược và hướng dẫn tiếp quản.
  * [`01_KIEN_TRUC_TSVM_TANG_10.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/01_KIEN_TRUC_TSVM_TANG_10.md): Phân tích module `C2TSVMamba` tại tầng 10, cấu trúc toán học 6 khối con và file YAML.
  * [`02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md): Bảng số liệu tổng hợp 6-fold cross-validation và kiểm định thống kê Paired t-test.
  * [`03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md): Sơ đồ cây thư mục và hướng dẫn tái lập kết quả thực nghiệm 100%.

* 🔬 **Hồ sơ Phân tích Từng Kết quả Chuyên sâu (Deep-Dive Result Dossiers):**
  * [`04_KET_QUA_LOSS_VA_HOI_TU.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/04_KET_QUA_LOSS_VA_HOI_TU.md): Phân tích `val/seg_loss` (1.3812 vs 1.4164, giảm -2.48%, $p = 0.0363$) và kiểm soát quá khớp.
  * [`05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md): Mask mAP@50 (0.9134), Mask mAP@50-95 (0.7246) và sự **thu hẹp độ lệch chuẩn 3 lần** ($0.0150 
ightarrow 0.0050$).
  * [`06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md): Đánh đổi Precision (91.71%) vs Recall (85.45%), polyp dạng phẳng (Paris IIb, < 5mm) và ý nghĩa trong phẫu thuật EMR/ESD.
  * [`07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md): Ma trận nhầm lẫn 127 ca tổn thương, đối chiếu cặp Paired Head-to-Head trên từng seed.
  * [`08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md): Tham số (12.09M), GFLOPs (42.3), checkpoint 23.86 MB, độ trễ 3 pha (21.2 ms = 47.2 FPS) đáp ứng thời gian thực chuẩn nội soi 25–30 FPS.
  * [`09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md): Nghiên cứu triệt tiêu chứng minh lý do Tầng 10 (Neck chuyển tiếp, stride 16, 40x40) vượt trội hơn đặt tại P5 (stride 32, 20x20).
  * [`10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md): Đánh giá định tính chất lượng mặt nạ, độ trơn nhẵn, chống lem mô lành và kháng phản xạ ánh sáng (glare).
  * [`11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md): Toàn bộ số liệu 6-fold biến thể P5_Attention_VMamba và phân tích lý do thất bại kỹ thuật.



* 📘 **[BÁO CÁO ĐẶC TẢ HƯỚNG NGHIÊN CỨU (Full Specification)](file:///C:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/BAO_CAO_DAC_TA_HUONG_NGHIEN_CUU.md)**: Tài liệu chi tiết 33 mục đặc tả cơ sở lý thuyết, kiến trúc module lai `C2TSVMamba`, vai trò của từng nhánh (VMamba, Shape, Topology), cơ chế Gating/Fusion, thiết kế ablation study và hướng dẫn trả lời phản biện.
* 💻 **[Mã nguồn Ultralytics Topology-Shape-aware VMamba](file:///C:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/ultralytics_Topology-Shape-aware%20VMamba)**: Source code Ultralytics tùy biến hoàn chỉnh (365 files) tích hợp module `C2TSVMamba` và cấu hình mô hình `yolo26-seg-TopologyShapeVMamba.yaml`.
* 📊 **[Thư mục Kết Quả Huấn Luyện & Đánh Giá (Ket_Qua)](file:///C:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua)**: Báo cáo, bảng dữ liệu `results.csv`, cấu hình `args.yaml`, đường cong PR/F1, ma trận nhầm lẫn của tất cả các thử nghiệm trên Kvasir-SEG và các tập ngoài miền.
* 📈 **[Artifact các run huấn luyện đối chứng (KQ_Poylp)](file:///C:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/KQ_Poylp)**: Dữ liệu chi tiết các lượt huấn luyện đối chứng các thang đo (scale n, s, m, l, x) của YOLOv11, YOLO26, và YOLO26-VMamba.
* 🗂️ **[Tập dữ liệu chuẩn hóa Kvasir_YOLO_SEG](file:///C:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Kvasir_YOLO_SEG)**: Bộ dữ liệu 1.000 ảnh (880 train / 120 val) đã tối ưu hóa đa giác phân đoạn cho YOLO.
* 🌐 **[Các tập dữ liệu kiểm thử ngoài miền (Cac_Dataset)](file:///C:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Cac_Dataset)**: Bộ dữ liệu CVC-ClinicDB, CVC-ColonDB và ETIS-Larib PolypDB phục vụ đánh giá tính khái quát hóa.
* 📋 **[Đặc tả đầu ra dữ liệu Kvasir-SEG](file:///C:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/kvasir_yolo_seg_output_spec.md)** & **[Báo cáo kiểm toán kết quả 10 run YOLO26](file:///C:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/training_results_audit.md)**.

---

## 1. Giới Thiệu Đề Tài & Ý Tưởng Nghiên Cứu Cốt Lõi

### 1.1. Thách thức trong phân đoạn polyp đại trực tràng
Phân đoạn polyp nội soi (Polyp Instance Segmentation) là nhiệm vụ tiền đề quan trọng hỗ trợ phát hiện sớm ung thư đại trực tràng. Tuy nhiên, các mô hình phân đoạn truyền thống thường gặp khó khăn bởi 3 yếu tố:
1. **Hình dạng đa dạng & biến thiên phức tạp:** Polyp có thể phẳng, dài, có cuống, viền gồ ghề hoặc lồi lõm bất thường.
2. **Biên polyp mờ và ánh sáng phức tạp:** Ánh sáng phản chiếu của niêm mạc ruột, bọt dịch, viền polyp trùng màu với thành ruột dễ khiến viền mask dự đoán bị lõm, đứt gãy hoặc ăn lan ra ngoài.
3. **Mối quan hệ không gian & ngữ cảnh dài hạn:** Phân biệt chính xác một vùng mô nghi ngờ ở biên đòi hỏi phải đối chiếu thông tin ngữ cảnh toàn diện của cả vùng polyp và cấu trúc mô xung quanh.

### 1.2. Giải pháp: Module lai `C2TSVMamba` (Topology-Shape-aware VMamba)
Thay vì tích hợp VMamba một cách đơn thuần, đề tài đề xuất module lai **C2TSVMamba** thay thế block `C2PSA` tại Layer 10 (tầng cổ chai sâu nhất của Backbone/Neck) trong kiến trúc YOLO26-seg:

```text
                                Input Feature X
                                       │
                                       ▼
                           ┌──────────────────────┐
                           │     C2 Structure     │
                           └──────────┬───────────┘
                                      │
                        ┌─────────────┴─────────────┐
                        │                           │
                        ▼                           ▼
                 ┌──────────────┐           ┌─────────────────┐
                 │    VMamba    │           │ Shape/Topology  │
                 │    Branch    │           │     Branch      │
                 └──────┬───────┘           └────────┬────────┘
                        │                            │
                        │ F_M                        │ F_TS
                        │                            │
                        │                     ┌──────┴───────┐
                        │                     │              │
                        │                     ▼              ▼
                        │                  Shape Gate   Topology Gate
                        │                     │              │
                        │                     └──────┬───────┘
                        │                            │
                        │                            ▼
                        │                         G_TS
                        │                            │
                        └────────────────────────────┤
                                                     ▼
                                     F_M' = F_M ⊙ (1 + G_TS)
                                                     │
                              ┌──────────────────────┴──────────────┐
                              │                                     │
                              ▼                                     ▼
                           F_M'                                  F_TS
                              │                                     │
                              └──────────────┬──────────────────────┘
                                             ▼
                                          Concat
                                             │
                                             ▼
                                         Conv 1×1
                                             │
                                             ▼
                                            FFN
                                             │
                                             ▼
                                     Residual + γ
                                             │
                                             ▼
                                     Output Feature Y
```

Ba thành phần cốt lõi của module:
1. **VMamba Branch (2D Selective Scan - SS2D):** Khai thác ngữ cảnh không gian dài hạn hai chiều với độ phức tạp tuyến tính $\mathcal{O}(N)$, giúp mô hình "nhìn rộng" hơn CNN cục bộ.
2. **Shape-aware Branch:** Sử dụng tích chập đa hướng (directional conv $1\times 5, 5\times 1$, curvature $3\times 3$) và gradient viền để mô hình "nhìn rõ hình dạng và đường viền".
3. **Topology-aware Mechanism:** Định hướng bảo toàn cấu trúc liên kết và tính liên thông của vùng phân đoạn, hạn chế tối đa việc mask bị chia tách hoặc đục lỗ bất thường.
4. **Modulation & Residual Scaling:** Dùng gate đặc trưng hình học/cấu trúc để điều biến feature map của VMamba, kết hợp qua FFN và scale bằng tham số học được $\gamma$ để bảo đảm độ ổn định khi tích hợp vào YOLO26.

---

## 2. Cấu Trúc Toàn Diện Của Repository

Repository được tổ chức chuẩn mực theo hệ thống các folder chức năng. **Lưu ý:** Mã nguồn tùy biến, các bộ dữ liệu và toàn bộ kết quả thực nghiệm nằm tập trung bên trong thư mục `archive/`:

```text
DL_Poylp_v26_VMamba_TestDemo/
├── BAO_CAO_DAC_TA_HUONG_NGHIEN_CUU.md       # [ĐẶC TẢ] Báo cáo chi tiết 33 mục về phương pháp & thực nghiệm
├── README.md                                # Tài liệu tổng quan toàn bộ repository
├── datasets/                                # Pipeline dữ liệu Kvasir Semantic 880/120
│   ├── Kvasir_Semantic_880_120/             # Dữ liệu semantic segmentation
│   └── kvasir_semantic_dataset.py           # Tiện ích xây dựng dataset
├── tests/                                   # Các kiểm thử tích hợp (integration tests)
└── archive/                                 # THƯ MỤC TRỌNG TÂM CỦA DỰ ÁN
    ├── BAO_CAO_DAC_TA_HUONG_NGHIEN_CUU.md   # Bản sao đặc tả hướng nghiên cứu
    │
    ├── ultralytics_Topology-Shape-aware VMamba/ # [MÃ NGUỒN] Thư viện Ultralytics tích hợp C2TSVMamba
    │   ├── nn/modules/topology_shape_vmamba.py  # Triển khai module Topology-Shape-aware VMamba
    │   ├── cfg/models/26/                       # File cấu hình kiến trúc YOLO26s-TopologyShapeVMamba
    │   ├── models/yolo/segment/                 # Pipeline huấn luyện và đánh giá segmentation
    │   └── ... (365 files mã nguồn đầy đủ)
    │
    ├── Ket_Qua/                                 # [KẾT QUẢ] Thư mục kết quả chính thức của các mô hình
    │   ├── CVC_ClinicDB/                        # Kết quả thử nghiệm trên tập ClinicDB
    │   ├── ColonDB/                             # Kết quả thử nghiệm trên tập ColonDB
    │   ├── ETIS_Larib/                          # Kết quả thử nghiệm trên tập ETIS-Larib
    │   ├── Kvasir_YOLO26s_seg/                  # Kết quả mô hình baseline YOLO26s trên Kvasir-SEG
    │   ├── Kvasir_YOLO26s_seg_Topology-Shape-awar/ # Kết quả mô hình đề xuất TS-VMamba
    │   ├── Cac_Mo_Hinh_Khac/                    # Kết quả các biến thể thử nghiệm khác
    │   └── Bao_cao/                             # Đồ thị so sánh tổng hợp (F1, PR, metrics)
    │
    ├── KQ_Poylp/                                # [ARTIFACTS] Chi tiết các run huấn luyện đối chứng
    │   ├── YOLOv11-seg/                         # Huấn luyện YOLO11 (n, s, m, l, x)
    │   ├── YOLOv26-seg/                         # Huấn luyện YOLO26 (n, s, m, l, x)
    │   └── YOLOv26-seg-VMamba_P5_sau_C2PSA/     # Huấn luyện YOLO26 tích hợp VMamba P5
    │
    ├── Kvasir_YOLO_SEG/                         # [DATASET CHÍNH] Kvasir-SEG chuyển đổi sang YOLO
    │   ├── images/ (train: 880 ảnh, val: 120 ảnh)
    │   ├── labels/ (train: 880 tệp nhãn, val: 120 tệp nhãn)
    │   ├── dataset.yaml                         # Cấu hình nạp dataset của YOLO
    │   ├── dataset_statistics.csv               # Bảng thống kê kích thước, đa giác, diện tích
    │   ├── dataset_summary.json                 # Tóm tắt phân bố dữ liệu JSON
    │   ├── report.txt                           # Báo cáo tổng hợp số liệu dataset
    │   └── dataset_plots/                       # 5 biểu đồ phân bố độ phân giải, diện tích, bbox
    │
    ├── Cac_Dataset/                             # [DATASET MỞ RỘNG] Kiểm tra tính khái quát hóa
    │   ├── CVC-ClinicDB/ & CVC_ClinicDB_YOLO_SEG/
    │   ├── CVC-ColonDB_data/ & CVC_ColonDB_YOLO_SEG/
    │   └── ETIS-Larib PolypDB/ & ETIS_Larib_YOLO_SEG/
    │
    ├── convert_kvasir_to_yolo_seg.py            # Script chuẩn hóa Kvasir-SEG sang YOLO-seg
    ├── convert_datasets_to_yolo_seg.py          # Script chuẩn hóa ClinicDB, ColonDB, ETIS sang YOLO-seg
    ├── kvasir_yolo_seg_output_spec.md           # Tài liệu đặc tả kỹ thuật tiền xử lý dữ liệu
    └── training_results_audit.md                # Báo cáo kiểm toán 10 run huấn luyện đối chứng
```

---

## 3. Quy Trình Dữ Liệu Thực Nghiệm (Datasets)

1. **Tập dữ liệu chính (In-Domain):**
   * **Kvasir-SEG**: Gồm 1.000 ảnh nội soi đại trực tràng độ phân giải cao và mask chuyên gia.
   * **Phân chia cứng chuẩn hóa:** **880 ảnh Train** ($88\%$) và **120 ảnh Validation** ($12\%$).
   * Tỷ lệ chia được cố định trong `train.txt` và `val.txt` để đảm bảo 100% công bằng khi so sánh chéo (cross-evaluation).

2. **Các tập dữ liệu ngoài miền (Out-of-Distribution - OOD Testing):**
   * **CVC-ClinicDB:** 612 ảnh nội soi trích xuất từ 29 video nội soi tiêu hóa khác nhau.
   * **CVC-ColonDB:** 380 ảnh nội soi đại tràng chứa nhiều polyp phẳng và kích thước nhỏ.
   * **ETIS-Larib PolypDB:** 196 ảnh nội soi từ máy nội soi Pentax độ nét cao, là bộ dữ liệu thử thách cao với nhiều polyp khó phát hiện.

---

## 4. Chính Sách Lưu Trữ Trọng Số Mô Hình (Weights Policy)

> [!NOTE]
> **Tại sao không thấy thư mục `weights/` trên GitHub?**  
> GitHub giới hạn kích thước mỗi file tối đa là **100 MB** và không khuyến nghị lưu trữ trực tiếp các file nhị phân lớn trong Git tree. Trong dự án này, toàn bộ 710 file checkpoint `.pt` (PyTorch model weights) có tổng dung lượng lên đến **~16.92 GB** (nhiều file mô hình lớn như YOLO26x, PraNet, UNet nặng từ 119 MB đến 357 MB).  
> Do đó, file [.gitignore](file:///C:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/.gitignore) đã chặn theo dõi `*.pt` để bảo đảm repository hoạt động nhẹ và ổn định.

* **Những gì đã được lưu đầy đủ 100% trên GitHub:**
  * Toàn bộ bảng log huấn luyện chi tiết từng epoch (`results.csv`).
  * Toàn bộ các ảnh trực quan hóa: biểu đồ huấn luyện (`results.png`), ma trận nhầm lẫn (`confusion_matrix.png`), đường cong precision-recall (`PR_curve.png`), đường cong F1 (`F1_curve.png`).
  * File cấu hình siêu tham số (`args.yaml`).
* **Cách truy cập/tải trọng số mô hình tốt nhất (`best.pt`):**
  * Các file trọng số của các mô hình tốt nhất sẽ được đóng gói và phát hành chính thức qua mục **GitHub Releases** của repository này hoặc Google Drive chia sẻ của nhóm nghiên cứu.

---

## 5. Hướng Dẫn Cài Đặt & Chạy Thực Nghiệm (Quickstart)

### 5.1. Khởi tạo môi trường
Yêu cầu hệ thống: Python $\ge$ 3.10, PyTorch $\ge$ 2.0, CUDA $\ge$ 11.8 (nếu sử dụng GPU).

```bash
# Clone repository
git clone https://github.com/Okeydokey8525/DL_Poylp_v26_VMamba_TestDemo.git
cd DL_Poylp_v26_VMamba_TestDemo

# Cài đặt mã nguồn Ultralytics tùy biến ở chế độ editable
cd "archive/ultralytics_Topology-Shape-aware VMamba"
pip install -e .
```

### 5.2. Tiền xử lý dữ liệu (nếu tải mới từ nguồn thô)
```bash
# Chuyển đổi bộ dữ liệu Kvasir-SEG sang định dạng YOLO Segmentation
python archive/convert_kvasir_to_yolo_seg.py

# Chuyển đổi 3 bộ dữ liệu ClinicDB, ColonDB, ETIS-Larib
python archive/convert_datasets_to_yolo_seg.py
```

### 5.3. Huấn luyện mô hình
```bash
# 1. Huấn luyện Baseline YOLO26s-seg (chuẩn 100 epochs, batch 16, imgsz 640)
yolo segment train \
  data=archive/Kvasir_YOLO_SEG/dataset.yaml \
  model=yolo26s-seg.yaml \
  epochs=100 \
  batch=16 \
  imgsz=640 \
  seed=0 \
  project=archive/Ket_Qua/Kvasir_YOLO26s_seg

# 2. Huấn luyện Mô hình đề xuất YOLO26s-TopologyShapeVMamba
yolo segment train \
  data=archive/Kvasir_YOLO_SEG/dataset.yaml \
  model="archive/ultralytics_Topology-Shape-aware VMamba/cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml" \
  epochs=100 \
  batch=16 \
  imgsz=640 \
  seed=0 \
  project=archive/Ket_Qua/Kvasir_YOLO26s_seg_Topology-Shape-awar
```

### 5.4. Đánh giá kiểm định & Kiểm tra ngoài miền
```bash
# Đánh giá trên tập validation của Kvasir-SEG
yolo segment val \
  data=archive/Kvasir_YOLO_SEG/dataset.yaml \
  model=path/to/best.pt \
  imgsz=640

# Đánh giá khái quát hóa trên tập CVC-ClinicDB
yolo segment val \
  data=archive/Cac_Dataset/CVC_ClinicDB_YOLO_SEG/dataset.yaml \
  model=path/to/best.pt \
  imgsz=640
```

---

## 6. Thiết Kế Thực Nghiệm Ablation Study

Nhằm chứng minh tính khoa học và đóng góp độc lập của từng thành phần, đề tài triển khai kế hoạch ablation study theo bảng đối chứng nghiêm ngặt:

| Thứ tự | Mô hình | VMamba (SS2D) | Shape-aware | Topology-aware | Mục tiêu khoa học |
|:---:|:---|:---:|:---:|:---:|:---|
| **Exp 1** | **YOLO26-seg (Baseline)** | ❌ | ❌ | ❌ | Thiết lập chuẩn đối chứng gốc |
| **Exp 2** | **YOLO26 + VMamba** | ✅ | ❌ | ❌ | Đánh giá riêng hiệu quả mô hình hóa ngữ cảnh rộng |
| **Exp 3** | **YOLO26 + Shape-aware** | ❌ | ✅ | ❌ | Đánh giá riêng khả năng biểu diễn biên và độ cong |
| **Exp 4** | **YOLO26 + VMamba + Shape** | ✅ | ✅ | ❌ | Đánh giá sự tương tác giữa Context và Shape |
| **Exp 5** | **YOLO26 + C2TSVMamba (Đề xuất)** | ✅ | ✅ | ✅ | Đánh giá hoàn chỉnh khi có ràng buộc Topology |

Tất cả các mô hình trong bảng ablation được kiểm soát đồng nhất 100% về: cùng tập dữ liệu, cùng phân chia train/val, cùng kích thước ảnh `imgsz=640`, cùng optimizer, learning rate, số epoch (100 epochs) và random seed.

---

## 7. Thành Viên Thực Hiện & Cố Vấn

* **Sinh viên thực hiện:**
  * **Lê Đức Lương** — MSSV: `2001230490`
  * **Phùng Tuấn Huy** — MSSV: `2001230312`
  * **Trần Mạnh Toàn** — MSSV: `2001230830`
* **Giảng viên hướng dẫn:** **TS. Phùng Thế Bảo**
* **Đơn vị:** Khoa Công nghệ Thông tin, Trường Đại học Công Thương TP. Hồ Chí Minh (HUIT).

---

## 8. Tuyên Bố Giới Hạn Sử Dụng (Disclaimer)

Dự án và mã nguồn được phát triển phục vụ mục đích **học tập, nghiên cứu khoa học và bảo vệ khóa luận tốt nghiệp cử nhân**. Các kết quả dự đoán của mô hình không được sử dụng thay thế các chẩn đoán, kết luận y khoa hoặc phác đồ điều trị của các bác sĩ chuyên khoa trong thực tế lâm sàng.
