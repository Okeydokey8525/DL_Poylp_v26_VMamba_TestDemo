# Ablation C2TSVMamba tại tầng 10

Mục đích: tách đóng góp của từng thành phần trong TSVMamba. Mọi thứ khác giữ **giống hệt** 20 seed TSVM FP32: cùng repo fork FP32, cùng dữ liệu BG20, cùng siêu tham số và cùng seed.

| Chế độ (`MODE`) | Giữ lại | Bỏ đi | Câu hỏi trả lời | Tham số tầng 10 |
|---|---|---|---|---:|
| (đầy đủ, đã có 20 seed) | SS2D, nhánh hình dạng, cổng | — | — | 1.811.201 |
| `vmamba_only` | SS2D | Nhánh hình dạng, cổng, fuse | Riêng VMamba đóng góp bao nhiêu? | 1.071.873 |
| `shape_only` | Nhánh hình dạng | SS2D, cổng, fuse | Riêng nhánh hình dạng đóng góp bao nhiêu? | 1.331.969 |
| `shape_vmamba_no_guidance` | SS2D và nhánh hình dạng, nối thẳng qua fuse | Cổng (1+G) | Cổng có giúp gì không? | 1.745.409 |

Mã của 3 chế độ đã có sẵn trong `nn/modules/topology_shape_vmamba.py`, không cần sửa repo. Notebook chỉ đổi tham số tầng 10 trong YAML: `[1024]` → `[1024, 0.5, 16, 3, MODE]`.

## Cách chạy một lượt

1. Tạo notebook mới trên Kaggle và import `kvasir-yolo26s-seg-tsvm-ablation.ipynb`.
2. **Add Input:** thêm 2 dataset `ultralytics-topology-shape-aware-vmamba-fp32` và `kvasir-yolo-seg-bg20` (các bạn đã dùng cho 20 seed TSVM FP32). Nếu tài khoản khác giữ dataset, sửa tên tài khoản trong `CUSTOM_REPO_PATH` và `DATASET_ROOT` ở Cell 1.
3. **Settings:** Accelerator = GPU (cùng loại GPU đã dùng cho 20 seed), Internet = ON (để tải `yolo26s-seg.pt`).
4. Ở **Cell 0**, sửa 2 dòng `MODE` và `SEED`.
5. Chọn **Save Version → Save & Run All (Commit)** để chạy nền khoảng 4–5 giờ, không cần mở trình duyệt.
6. Cell 3 tự kiểm tra cấu trúc: nếu `mode` hoặc số tham số tầng 10 sai, notebook dừng ngay, chưa tốn giờ GPU.
7. Xong thì tải `runs_Kvasir_BG20_YOLO26s_seg_ABL_<MODE>_s<SEED>_w2.zip` ở tab Output và đặt vào `03_ket_qua_huan_luyen/Ablation_TSVM/`.

## Lịch chạy đề xuất: 3 chế độ × seed 0–4 = 15 lượt (≈ 68 giờ GPU)

| Tài khoản | Lượt 1 | Lượt 2 | Lượt 3 |
|---|---|---|---|
| TK1 | vmamba_only s0 | vmamba_only s3 | shape_vmamba_no_guidance s4 |
| TK2 | vmamba_only s1 | vmamba_only s4 | |
| TK3 | vmamba_only s2 | shape_only s3 | |
| TK4 | shape_only s0 | shape_only s4 | |
| TK5 | shape_only s1 | shape_vmamba_no_guidance s0 | shape_vmamba_no_guidance s3 |
| TK6 | shape_only s2 | shape_vmamba_no_guidance s1 | shape_vmamba_no_guidance s2 |

Mỗi tài khoản dùng tối đa khoảng 14 giờ, dưới hạn mức GPU khoảng 30 giờ/tuần của Kaggle. Nếu chạy song song đủ 6 tài khoản thì xong trong khoảng 1,5 ngày.

## Cách đọc kết quả

- So **từng cặp cùng seed** với Baseline và TSVM đầy đủ (seed 0–4 đã có), dùng cùng chỉ số mask mAP50-95 lớn nhất mỗi lượt như phân tích 20 seed.
- 5 seed chỉ đủ để thấy **xu hướng**, không đủ cho ý nghĩa thống kê, vì độ lệch giữa các seed (~0,01) lớn hơn mức chênh cần đo (~0,004). Báo cáo phải ghi rõ giới hạn này.
