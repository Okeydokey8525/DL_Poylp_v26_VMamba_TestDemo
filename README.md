# DL_Poylp_v26_VMamba_TestDemo

## Nghiên Cứu Phương Pháp Tích Hợp VMamba Vào Mô Hình YOLO26-seg Trong Phân Đoạn Polyp Từ Ảnh Nội Soi Đại Trực Tràng

Repository lưu trữ toàn bộ mã nguồn, cấu hình mô hình, công cụ chuyển đổi trọng số pre-trained và báo cáo kiểm toán thực nghiệm cho đề tài **YOLO26-VMamba-seg**.

👉 **[ĐỌC BÁO CÁO TOÀN DIỆN & HƯỚNG DẪN CHI TIẾT TẠI CHI TIẾT ARCHIVE/README.MD](archive/README.md)**  
👉 **[XEM BÁO CÁO KIỂM TOÁN 12 LƯỢT HUẤN LUYỆN BASELINE (AUDIT REPORT)](archive/training_results_audit.md)**

---

## 🌟 NỔI BẬT DỰ ÁN

- **Mô Hình Lai YOLO26-VMamba-seg:** Tích hợp khối **2D Selective Scan (SS2D)** vào vị trí nút thắt $P_5/32$ (Layer 11) của YOLO26-seg để khắc phục nhược điểm "Nút thắt đường biên" (Boundary Precision Gap).
- **Mã Nguồn Mở Rộng Ultralytics:** Tích hợp trực tiếp `VMambaBlock` trong `ultralytics-main/ultralytics/nn/modules/vmamba.py` hỗ trợ cả **CUDA Fast Path** (thư viện `mamba_ssm`) lẫn **PyTorch Fallback Path** ổn định số học cho GPU/CPU.
- **Công Cụ Weight Transfer:** Module `ultralytics-main/ultralytics/utils/vmamba_weight_transfer.py` tự động chuyển giao trọng số từ baseline YOLO26 pre-trained sang YOLO26-VMamba-seg.
- **Dữ Liệu Thử Nghiệm Kvasir-SEG:** Tiền xử lý 1,000 ảnh nội soi đại trực tràng chuẩn với tập train/val (880/120).

---

## 🚀 QUY TRÌNH THỰC HIỆN RẮN (QUICK START)

```bash
# 1. Cài đặt mô hình ultralytics đã tích hợp VMamba
cd ultralytics-main
pip install -e .

# 2. Kiểm tra tính đúng đắn của khối VMamba
python -c "from ultralytics.utils.vmamba_weight_transfer import verify_vmamba_fast_path; from ultralytics.models import YOLO; yolo = YOLO('ultralytics/cfg/models/26/yolo26-vmamba-seg.yaml'); print(verify_vmamba_fast_path(yolo))"

# 3. Chuyển trọng số baseline và khởi chạy huấn luyện
python -c "from ultralytics.utils.vmamba_weight_transfer import build_yolo26_vmamba_seg; yolo, r = build_yolo26_vmamba_seg(scale='m', pretrained='yolo26m-seg.pt', nc=1); yolo.train(data='../archive/Kvasir_YOLO_SEG/dataset.yaml', epochs=100, imgsz=640, batch=32, device=0)"
```

---

## 📊 KẾT QUẢ HUẤN LUYỆN BASELINE SUMMARY

Tóm tắt chỉ số tốt nhất từ 12 lượt huấn luyện baseline trên Kvasir-SEG (xem chi tiết tại `archive/README.md`):

| Mô Hình | Epoch | Best Mask mAP50 | **Best Mask mAP50-95** | Parameters |
| :--- | :---: | :---: | :---: | :---: |
| **YOLO11m-seg** | 100 | 0.9193 | **0.7222** | 22.43 M |
| **YOLO11x-seg** | 100 | 0.9360 | **0.7198** | 62.17 M |
| **YOLO11l-seg** | 100 | 0.9261 | **0.7186** | 27.71 M |
| **YOLO26m-seg** | 100 | 0.9228 | **0.7115** | 27.06 M |
| **YOLO26x-seg** | 100 | 0.9212 | **0.7070** | 70.62 M |
| **YOLO26s-seg** | 100 | 0.9271 | **0.7058** | 11.50 M |
| **YOLO11n-seg** | 100 | 0.9020 | **0.7042** | 2.88 M |
| **YOLO26n-seg** | 100 | 0.8982 | **0.7036** | 3.10 M |

---

## 📄 LIÊN HỆ & BÁO CÁO KHÓA LUẬN

Mọi thông tin chi tiết về lý thuyết, mã nguồn và số liệu kiểm toán đều được trình bày đầy đủ trong tài liệu [archive/README.md](archive/README.md).
