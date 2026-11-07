# Ultralytics cho mô hình YOLO26s-seg + MambaPSA (tái hiện)

Tạo ngày 06/11/2026, theo nhận xét của GVHD (nội dung 4: thiếu tái hiện MambaPSA, công trình gần nhất).

- **Nguồn:** sao nguyên `../ultralytics_TSVM_FP32/` (Ultralytics 8.4.127, TSVM, bản vá lưu checkpoint FP32).
- **Thay đổi:**
  - thêm `nn/modules/mamba_psa.py` (khối `MambaPSA`, `MambaCore1D`);
  - đăng ký `MambaPSA` trong `nn/modules/__init__.py` và `nn/tasks.py` (danh sách import, `base_modules`, `repeat_modules`);
  - thêm `cfg/models/26/yolo26s-seg-MambaPSA.yaml` (tầng 10: `[-1, 2, MambaPSA, [1024]]`).

## Lưu ý quan trọng khi viết báo cáo

- **Đây là bản tái hiện theo mô tả của bài báo**, không phải mã của tác giả. Tính đến 06/11/2026, bài arXiv:2607.12681v1 chưa công bố mã nguồn.
- **Phần làm theo bài báo:** chiếu 1×1, tách hai nửa, một nửa qua lõi Mamba **một chiều**, nửa kia giữ nguyên, ghép rồi qua 1×1.
- **Phần nhóm tự chọn, vì bài báo không ghi:**
  - expand = 2, d_state = 16, d_conv = 4;
  - có nối tắt D, chuẩn hóa GroupNorm trước lõi và kết nối dư.
  - Các giá trị này theo mặc định của Mamba gốc.
- **Phép quét** dùng lại `parallel_associative_scan` của khối TSVM, không cần biên dịch `mamba_ssm`.
- **Bài gốc làm phát hiện vật thể trên PASCAL VOC.** Ở đây khối được đặt vào YOLO26s-seg cho bài toán phân đoạn polyp, nên kết quả không so trực tiếp với số trong bài báo.

| | Tham số tầng 10 |
|---|---|
| C2PSA (mô hình gốc) | 990.976 |
| MambaPSA (tái hiện) | 964.608 (−2,7%) |
| C2TSVMamba | 1.811.201 |

Đã kiểm trên máy (GPU): dựng mô hình, chạy xuôi và ngược tầng 10, chạy cả mô hình ở 640 đều không lỗi. Chưa huấn luyện thử.

## Cách dùng

Nén thư mục này và tải lên Kaggle với slug `ultralytics-mambapsa`, rồi chạy `../notebook_kaggle/mambapsa/kvasir-yolo26s-seg-mambapsa.ipynb`.
