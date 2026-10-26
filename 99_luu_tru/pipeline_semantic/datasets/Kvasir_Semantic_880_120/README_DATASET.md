# Kvasir_Semantic_880_120

## 1. Nguồn Dữ Liệu
Bộ dữ liệu Kvasir-SEG gốc là một bộ dữ liệu về hình ảnh nội soi tiêu hóa, chứa 1.000 cặp ảnh (images) và nhãn phân vùng (masks) polyp. 
Bộ dataset `Kvasir_Semantic_880_120` này được tinh chế lại từ Kvasir-SEG để sử dụng chuyên biệt cho bài toán Semantic Segmentation (phân vùng ngữ nghĩa).

## 2. Split và Cấu Trúc Thư Mục
Dữ liệu được chia cứng thành hai tập: **880 ảnh train** và **120 ảnh validation**. 
Việc phân chia này bám sát hoàn toàn với cấu trúc chia của bộ Kvasir_YOLO_SEG để đảm bảo tính công bằng khi so sánh chéo (cross-evaluation) các mô hình sau này.
Danh sách các file trong từng tập được ghi cụ thể trong `splits/train.txt` và `splits/val.txt`.

**Cấu trúc thư mục:**
```text
Kvasir_Semantic_880_120/
├── train/
│   ├── images/              # (880) Ảnh gốc
│   ├── masks_original/      # (880) Mask gốc lấy trực tiếp từ Kvasir-SEG
│   └── masks_binary/        # (880) Mask đã nhị phân hóa (chỉ 0 và 255)
├── val/
│   ├── images/              # (120) Ảnh gốc
│   ├── masks_original/      # (120) Mask gốc lấy trực tiếp từ Kvasir-SEG
│   └── masks_binary/        # (120) Mask đã nhị phân hóa
├── splits/
│   ├── train.txt
│   └── val.txt
├── split_manifest.csv       # Danh sách 1000 file kèm mã băm SHA-256 (phục vụ đối soát)
├── dataset_summary.json     # Siêu dữ liệu và log quá trình tạo dataset
└── qa/                      # Thư mục lưu trữ ảnh preview và báo cáo QA
    ├── qa_report.md
    └── previews/
```

## 3. Quy Tắc Xử Lý Binary Mask
Tất cả các ảnh và mask **được giữ nguyên độ phân giải** (không resize). Tập ảnh không bị biến đổi augment hay normalize.
Các mask nằm trong thư mục `masks_binary` được tạo theo quy tắc chặt chẽ như sau:
1. Đọc mask gốc dưới định dạng Grayscale.
2. Áp dụng ngưỡng (Threshold) cứng là **127**.
   - Các pixel có cường độ màu `> 127` sẽ được chuyển thành **255** (đại diện cho vùng Polyp - Foreground).
   - Các pixel có cường độ màu `<= 127` sẽ được chuyển thành **0** (đại diện cho Background).
3. KHÔNG sử dụng morphology (erosion/dilation) hoặc thay đổi đường viền contour.
4. Đầu ra được lưu dưới dạng ảnh PNG Lossless.

## 4. Hướng Dẫn Sử Dụng (Mount trên Kaggle)
Bộ dữ liệu này được đóng gói tối ưu để sử dụng trên nền tảng Kaggle Kernel.

1. **Tạo Dataset:** Tại Kaggle, chọn Add Data -> Upload -> nén toàn bộ thư mục `Kvasir_Semantic_880_120` thành file `.zip` rồi upload lên.
2. **Mount Dataset vào Notebook:** Sau khi Dataset sẵn sàng, bạn truy xuất dữ liệu trong Notebook bằng đường dẫn:
   ```python
   DATA_DIR = "/kaggle/input/kvasir-semantic-880-120"
   TRAIN_IMG_DIR = f"{DATA_DIR}/train/images"
   TRAIN_MASK_DIR = f"{DATA_DIR}/train/masks_binary"
   ```
3. Khuyến nghị bạn sử dụng thư viện `albumentations` để load và thực hiện các bước augmentation (như Resize, Normalize, RandomFlip, ...) trong quá trình chạy Dataloader. Không nên normalize dữ liệu sẵn trên đĩa cứng.
