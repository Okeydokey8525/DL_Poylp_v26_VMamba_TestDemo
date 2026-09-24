# THƯ MỤC LƯU TRỮ KẾT QUẢ KHẮC PHỤC TRIỆT ĐỂ (TSVM SEED 0 & SEED 5)
## BỘ DỮ LIỆU KVASIR_YOLO_SEG_BG20 (1.200 ẢNH)

---

### 1. Mục Đích & Bối Cảnh Của Thư Mục
Thư mục này lưu trữ kết quả đầu ra chuẩn hóa (đã khắc phục lỗi hình ảnh) của mô hình **YOLO26s-seg-TSVM** tại hai lượt chạy:
1. `Kvasir_BG20_YOLO26s_seg_TSVM_s0_w2` (Seed 0)
2. `Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2` (Seed 5)

### 2. Sự Cố Ban Đầu Trên Kaggle
* Trong 100 epoch huấn luyện, dữ liệu số học trong `results.csv` hoàn toàn chính xác và hội tụ rất cao:
  - **Seed 0:** Mask mAP@50 = **0.9040**, Box mAP@50 = **0.8973** (Epoch 88).
  - **Seed 5:** Mask mAP@50 = **0.9096**, Box mAP@50 = **0.9113** (Epoch 90).
* Tuy nhiên, hàm `model.fuse()` tự động của Ultralytics ở cuối quá trình train trên Kaggle đã vô tình xóa bỏ nhánh One-to-Many (`self.cv2 = None`) và ép chuyển model sang nhánh One-to-One (End-to-End).
* Do nhánh One-to-One chưa hội tụ (đặc biệt ở Seed 5), kết quả đánh giá cuối cùng bị sụp đổ (mAP về 0), khiến các ảnh đường cong (`BoxPR_curve`, `BoxF1_curve`,...) bị phẳng/rỗng và ảnh `val_batch2_pred.jpg` xuất hiện các box cột dọc lỗi kéo giãn từ $y_1=0$ đến $y_2=640$.

### 3. Giải Pháp & Quy Cách 24 Ảnh Chuẩn Trong Thư Mục Này
Nhóm nghiên cứu đã:
* Giữ nguyên 100% checkpoint gốc `weights/best.pt`.
* Khóa cứng không cho fuse, ép dùng nhánh One-to-Many (`Detect.end2end = False`).
* Áp dụng bản vá thứ tự tọa độ an toàn cho Pillow 10+ và đồng bộ hóa luồng ghi ảnh.
* Tái lập chính xác **ĐÚNG 24 FILE ẢNH KẾT QUẢ / SEED** theo chuẩn xuất bản khoa học 300 DPI, khớp 100% với `results.csv`:

| STT | Tên file ảnh | Mô tả |
| :---: | :--- | :--- |
| 1 - 7 | `labels.jpg`, `train_batch0/1/2.jpg`, `train_batch11700/11701/11702.jpg` | 7 ảnh tiến trình train |
| 8 - 10 | `val_batch0/1/2_labels.jpg` | 3 ảnh Ground Truth validation |
| 11 | `results.png` | 1 ảnh tổng hợp tiến trình 100 epochs |
| 12 - 14 | `val_batch0/1/2_pred.jpg` | 3 ảnh dự đoán thực tế (sạch sẽ, không còn cột dọc) |
| 15 - 16 | `confusion_matrix.png`, `confusion_matrix_normalized.png` | 2 ảnh ma trận nhầm lẫn |
| 17 - 24 | `BoxPR/F1/P/R_curve.png`, `MaskPR/F1/P/R_curve.png` | 8 ảnh đường cong hiệu năng 300 DPI |

Kèm theo đầy đủ các file metadata: `args.yaml`, `results.csv`, `weights/best.pt`, `weights/last.pt`.

---
*Tài liệu chi tiết về nguyên nhân kỹ thuật và giải pháp:*  
👉 [doc/17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md)
