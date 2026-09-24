# NHẬT KÝ & LỊCH SỬ CẬP NHẬT DỰ ÁN (PROJECT CHANGELOG)
## ĐỀ TÀI KHÓA LUẬN CỬ NHÂN: NGHIÊN CỨU TÍCH HỢP VMAMBA VÀO YOLO26-SEG PHÂN ĐOẠN POLYP
### Mã Đề Tài: `CNTT_KLCN182` | Trường Đại học Công Thương TP.HCM (HUIT)

---

## 📌 BẢNG TỔNG HỢP CÁC PHIÊN BẢN CẬP NHẬT

| Phiên bản | Ngày cập nhật | Nội dung chính | Trạng thái |
| :---: | :---: | :--- | :---: |
| **v1.0** | 10/2025 | Khởi tạo baseline YOLO26s-seg và khảo sát dữ liệu chuẩn Kvasir-SEG (1.000 ảnh) | Đã hoàn thành |
| **v1.5** | 11/2025 | Tích hợp thử nghiệm VMamba tại các vị trí: P3 (Sobel), Neck, Proto Head (Gặp OOM) | Đã ghi nhận Ablation |
| **v2.0** | 12/2025 | Cố định kiến trúc tích hợp VMamba tại **Layer 10 (P5, $20\times 20$)**; phát triển 4 hướng: C2TSVMamba, P5 Attention-VMamba, C2ITSMamba, C2IAVM (Proposed Champion) | Đã hoàn thành 6-fold |
| **v2.2** | 01/2026 | Hoàn thiện hệ thống tài liệu chuẩn học thuật (Doc 00 -> 15) và bảng đối chuẩn 6-fold cross-validation | Đã nghiệm thu |
| **v2.5** | 02/2026 | Mở rộng tập dữ liệu **Kvasir_YOLO_SEG_BG20** (+20% ảnh nền âm tính `normal-cecum`) giải quyết triệt để vấn đề độ đặc hiệu (Specificity) | Đã hoàn thành dataset |
| **v2.6** | 03/2026 | Kiểm toán chất lượng kết quả huấn luyện BG20; phát hiện & giải quyết sự cố `model.fuse()` tự động của Ultralytics gây lỗi ảnh trên Kaggle; khôi phục thành công trọn bộ **24 ảnh kết quả chuẩn / seed** tại thư mục `archive/Khac_phuc/` | **Hiện tại (Mới nhất)** |

---

## 🕒 CHI TIẾT TỪNG MỐC CẬP NHẬT

### 🚀 Phiên bản v2.6 (24/03/2026) – Kiểm toán & Khắc phục Sự cố Xuất ảnh trên Kaggle
* **Người thực hiện:** Nhóm nghiên cứu `CNTT_KLCN182` & AI Pair Programming.
* **Mục tiêu:** Kiểm toán toàn diện các artifact sau huấn luyện của mô hình TSVM trên tập BG20, làm rõ nguyên nhân số liệu đúng nhưng ảnh bị lỗi và tái lập trọn vẹn 24 ảnh kết quả/seed.
* **Chi tiết thay đổi & phát hiện kỹ thuật:**
  1. **Làm rõ tính toàn vẹn của dữ liệu gốc:**
     - Xác thực các tệp `results.csv` tại cả 6 seed của mô hình TSVM đều chứa số liệu thực nghiệm chính xác, trung thực. Seed 0 đạt Mask mAP@50 là **$0.9040$**; Seed 5 đạt Mask mAP@50 là **$0.9096$**.
     - Checkpoint `weights/best.pt` của cả 2 seed hoàn toàn nguyên vẹn, chứa đầy đủ các trọng số chất lượng cao của nhánh One-to-Many.
  2. **Phát hiện nguyên nhân gốc rễ (Root Cause):**
     - Ở epoch cuối cùng trên Kaggle, Ultralytics tự động gọi `model.fuse()`. Trong custom head `Segment26`, hàm này đã xóa bỏ nhánh One-to-Many (`self.cv2 = self.cv3 = self.cv4 = None`) và ép chuyển model sang nhánh One-to-One (End-to-End).
     - Do nhánh One-to-One tại Seed 5 chưa hội tụ (confidence tối đa chỉ đạt 0.028), việc suy diễn bị sụp đổ, sinh ra các bounding box rác kéo dài từ đỉnh xuống đáy màn hình ($y_1=0 \to y_2=640$) và làm rỗng 8 đồ thị đánh giá (AUC = 0).
     - Phát hiện lỗi thứ tự tọa độ trong Pillow 10+ (`ValueError: x1 must be greater than or equal to x0`) trên background thread của `plot_images`, làm đứt gãy việc lưu các file `val_batch*_pred.jpg`.
  3. **Khắc phục thành công và nghiệm thu 24 ảnh chuẩn / seed:**
     - Thiết lập cơ chế vô hiệu hóa `fuse()`, khóa cứng `Detect.end2end = False` và bổ sung patch sắp xếp tọa độ an toàn cho Pillow.
     - Xuất lại đầy đủ, chính xác **24/24 file ảnh** cho cả Seed 0 và Seed 5 (gồm 7 ảnh train, 3 ảnh val labels, 1 ảnh results.png, 3 ảnh val predictions sạch cột dọc, 2 ảnh confusion matrix, 8 ảnh performance curves chuẩn 300 DPI khớp 100% với `results.csv`).
     - Đóng gói toàn bộ kết quả vào thư mục độc lập:
       - `archive/Khac_phuc/Kvasir_BG20_YOLO26s_seg_TSVM_s0_w2/`
       - `archive/Khac_phuc/Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2/`
  4. **Cập nhật tài liệu mới:**
     - Khởi tạo [doc/17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md).
     - Xây dựng script hướng dẫn tái lập cho Kaggle: [archive/Stracth/kaggle_val_fix_guide.py](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/kaggle_val_fix_guide.py).

---

### 📦 Phiên bản v2.5 (15/02/2026) – Mở rộng Tập Dữ liệu Kvasir_YOLO_SEG_BG20
* **Nội dung:**
  - Bổ sung 200 ảnh nội soi manh tràng lành (`normal-cecum` từ Kvasir v2) với nhãn rỗng 0-byte (160 ảnh vào tập Train, 40 ảnh vào tập Validation) để giải quyết triệt để hiện tượng báo động giả mô nền và ô `1.00` trong ma trận nhầm lẫn chuẩn hóa.
  - Xây dựng tài liệu kỹ thuật [doc/16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md).
  - Chuẩn hóa bộ siêu tham số khóa tất định 100% trên Kaggle GPU (AdamW, lr0=0.001, close_mosaic=10, 100 epochs, seed cố định 0 -> 5).

---

### 🏆 Phiên bản v2.0 (20/12/2025) – Hoàn thành Thực nghiệm 4 Hướng Tích hợp VMamba
* **Nội dung:**
  - Thực nghiệm đối chuẩn 6-fold cross-validation nghiêm ngặt giữa Baseline YOLO26s-seg và 4 hướng tiếp cận cải tiến.
  - Xác lập mô hình đề xuất vô địch **`C2IAVM` (Attention-VMamba Fusion)**: Mask mAP@50-95 đạt **$73.61\%$** (kỷ lục $74.66\%$), giảm phương sai $4.39\times$, thắng áp đảo 5/6 seed đối chứng trực tiếp.
  - Hoàn tất bộ tài liệu học thuật từ `00_TONG_QUAN_VA_TINH_HINH_DU_AN.md` đến `15_CAM_NANG_PHONG_CACH_WORD_VA_NGON_NGU_HOC_THUAT.md`.

---

### 🧪 Phiên bản v1.0 -> v1.5 (10/2025 – 11/2025) – Nghiên cứu Cơ sở & Thăm dò Kiến trúc
* **Nội dung:**
  - Thiết lập baseline chuẩn YOLO26s-seg trên tập dữ liệu Kvasir-SEG gốc.
  - Khảo sát các điểm nghẽn bộ nhớ của VMamba: chứng minh việc gắn SS2D tại tầng sớm P3 hoặc Proto Head gây tràn bộ nhớ (OOM) trên GPU 15GB.
  - Phát hiện và chuẩn hóa giải pháp tính toán **Cách 2: Pure PyTorch với `SelectiveScanAutograd`**, giải phóng sự phụ thuộc vào custom C++ CUDA kernel.

---
*Nhật ký này được duy trì và cập nhật liên tục theo tiến độ thực tế của đề tài.*
