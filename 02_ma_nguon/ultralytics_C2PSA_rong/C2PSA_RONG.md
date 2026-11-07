# Ultralytics cho mô hình C2PSA rộng (đối chứng cùng số tham số)

Tạo ngày 06/11/2026, theo nhận xét của GVHD (nội dung 4: ablation thiếu đối chứng cùng số tham số).

- **Nguồn:** sao nguyên `../ultralytics_TSVM_FP32/`, gồm Ultralytics 8.4.127, mô-đun TSVM và bản vá lưu checkpoint FP32 (`PATCH_FP32.md`).
- **Thay đổi duy nhất:** thêm tệp `cfg/models/26/yolo26s-seg-C2PSA-rong.yaml`. Không sửa tệp mã nào.

| | Tầng 10 | Tham số tầng 10 |
|---|---|---|
| Mô hình gốc | `[-1, 2, C2PSA, [1024]]` | 990.976 |
| **C2PSA rộng** | `[-1, 2, C2PSA, [1024, 0.75]]` | **1.830.016** |
| TSVM (C2TSVMamba) | `[-1, 2, C2TSVMamba, [1024]]` | 1.811.201 |

## Ý nghĩa

C2PSA rộng giữ nguyên kiến trúc gốc nhưng nới độ rộng kênh ẩn của khối PSA. Hệ số `e` tăng từ 0,5 lên 0,75, tức 384 kênh và 6 đầu chú ý. Nhờ vậy tầng 10 có số tham số gần bằng C2TSVMamba (+1%).

So C2PSA rộng với TSVM cho biết mức nhỉnh hơn của TSVM đến từ thiết kế hay chỉ do có nhiều tham số hơn.

Tầng 10 của C2PSA rộng khác kích thước với `yolo26s-seg.pt` nên **học từ đầu**, giống TSVM. Các tầng còn lại nạp trọng số có sẵn.

## Cách dùng trên Kaggle

1. Nén thư mục này và tải lên Kaggle thành dataset, ví dụ slug `ultralytics-c2psa-rong`.
2. Chạy notebook `../notebook_kaggle/c2psa_rong/kvasir-yolo26s-seg-c2psa-rong.ipynb`, chỉ sửa `SEED`.
3. Kết quả đặt vào `03_ket_qua_huan_luyen/C2PSA_rong/`.
