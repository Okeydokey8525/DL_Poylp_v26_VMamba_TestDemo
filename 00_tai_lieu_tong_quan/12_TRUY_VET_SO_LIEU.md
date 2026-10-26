# 12. Truy vết số liệu

## Script

[`scripts/tinh_lai_so_lieu.py`](scripts/tinh_lai_so_lieu.py) **chỉ đọc** dữ liệu trong `01_du_lieu/`, `02_ma_nguon/`, `03_ket_qua_huan_luyen/`, `04_phan_tich_20seed/` và `99_luu_tru/ket_qua_cu/` (để so TSVM cũ), và chỉ ghi vào thư mục `bang/`. Script không huấn luyện, không suy luận và không sửa dữ liệu gốc.

```bash
cd 00_tai_lieu_tong_quan/scripts
python tinh_lai_so_lieu.py --torch
```

- Cần: numpy, pandas, scipy, pyyaml, pillow. Với `--torch` cần thêm torch.
- Chạy không có `--torch` thì bỏ qua phần kiểm tra checkpoint và dựng lại mô hình.
- Phần `--torch` tạo một junction (Windows) hoặc symlink tạm trong thư mục Temp, để nạp fork `02_ma_nguon/ultralytics_TSVM_FP32/` dưới tên gói `ultralytics`. Script gỡ link khi chạy xong và không ghi vào fork (`PYTHONDONTWRITEBYTECODE`).
- Lần chạy dùng cho bộ tài liệu này: Python 3.13.14, torch 2.13.0+cpu, ngày 26/10/2026. Toàn bộ đầu ra nằm ở [bang/_log_chay.txt](bang/_log_chay.txt).

## Tệp kết quả trong `bang/`

| Tệp | Nội dung | Dùng ở |
|---|---|---|
| `00_kiem_tra_du_lieu.json` | Kết quả kiểm tra split và trùng byte | [02](02_DU_LIEU_BG20.md) |
| `01_du_lieu_bg20.csv` | Đếm ảnh, nhãn, đối tượng, số đỉnh polygon, kích thước ảnh | [02](02_DU_LIEU_BG20.md) |
| `02_ket_qua_tung_seed.csv` | 40 dòng: metric tại epoch cực đại mask, epoch fitness, metric ở epoch 100, thời gian | [05](05_CAU_HINH_HUAN_LUYEN.md), [06](06_KET_QUA_20_SEED.md) |
| `03_cau_hinh_args.csv` | So sánh 36 tham số `args.yaml` giữa hai mô hình | [05](05_CAU_HINH_HUAN_LUYEN.md) |
| `04_thong_ke_ghep_cap.csv` | Mean, SD, min, max, Δ, CI, t, Wilcoxon, d_z, sign test cho 13 chỉ số | [06](06_KET_QUA_20_SEED.md) |
| `04b_do_nhay_quy_tac_epoch.csv` | So sánh theo 3 quy tắc chọn epoch | [06](06_KET_QUA_20_SEED.md) |
| `05_duong_cong_theo_epoch.csv` | Mean và SD theo từng epoch (mask mAP, các loss) | [07](07_HOI_TU_VA_LOSS.md) |
| `06_ma_tran_nham_lan_tung_seed.csv` | TP/FP/FN 40 lượt, lấy từ CSV của gói phân tích | [08](08_MA_TRAN_NHAM_LAN.md) |
| `07_checkpoint_best_pt.csv` | Kiểu dữ liệu, tính hữu hạn, số tham số, kích thước, phiên bản của 40 `best.pt` | [03](03_KIEN_TRUC_BASELINE.md), [05](05_CAU_HINH_HUAN_LUYEN.md), [09](09_HIEU_NANG_TINH_TOAN.md) |
| `08_kien_truc_dung_lai.csv` | Dựng lại 2 mô hình: tham số, kích thước đầu ra từng tầng, tham số từng nhánh TSVM, phần nhận trọng số tiền huấn luyện | [03](03_KIEN_TRUC_BASELINE.md), [04](04_KIEN_TRUC_TSVM_FP32.md) |
| `09_ma_tran_doc_tu_anh.csv` | TP/FP/FN đọc thủ công từ 40 ảnh `confusion_matrix.png` | [08](08_MA_TRAN_NHAM_LAN.md) |
| `_log_chay.txt` | Toàn bộ đầu ra của lần chạy script | Mọi file |

`09_ma_tran_doc_tu_anh.csv` là tệp **duy nhất không do script sinh ra**. Các số trong đó được đọc bằng mắt từ ảnh ghép lưới, sau đó so với `06_ma_tran_nham_lan_tung_seed.csv` bằng code (khớp 40/40).

## Những số **không** tính lại (lấy từ nguồn có sẵn)

| Số liệu | Nguồn | Đã kiểm tra gì |
|---|---|---|
| Độ trễ, RSS, tham số sau gộp Conv-BN | `KQ_Nen_DX_20seed_FP32/efficiency_benchmark/` | Số tham số chưa gộp, kích thước checkpoint, SHA-256 của checkpoint đều trùng |
| Levene p = 0,026 | `KQ_Nen_DX_20seed_FP32/06_reports/summary.csv` | Không tính lại |
| 999/1.000 nhãn tái tạo khớp từng ký tự | `99_luu_tru/tai_lieu_cu/archive_doc/28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md` | Không chạy lại |
| Môi trường GPU (Tesla T4…) | `99_luu_tru/log_kaggle_cu/*.log` (lượt TSVM cũ) | Chỉ đọc log |

## Đối chiếu với gói phân tích có sẵn

- Raw CSV: 0 ô lệch trên 40 dòng × 14 trường.
- `06_reports/summary.csv`: sai số lớn nhất bằng 0 với mean, Δ, p và CI.
- `epoch_selection_audit.csv`: trùng 40/40, đúng 16 lượt khác epoch.

## Những điểm tài liệu cũ cần lưu ý khi đọc

Bộ tài liệu này không sửa tài liệu cũ, chỉ ghi lại những chỗ dễ gây hiểu nhầm:

| Vị trí | Nội dung | Thực tế |
|---|---|---|
| `99_luu_tru/tai_lieu_cu/CURRENT_PROJECT_STATUS_goc_cu.md` và `99_luu_tru/tai_lieu_cu/README_goc_cu.md` ở thư mục gốc | Phần thân mô tả bộ 10 seed (0,7210 / 0,7246, p = 0,3839) | Chỉ là snapshot cũ. Bộ chính là 20 seed ([06](06_KET_QUA_20_SEED.md)) |
| Comment trong `data_bg20.yaml` | "bổ sung 20% ảnh nền" | 200 ảnh bằng 20% của 1.000 ảnh polyp, không phải 20% tổng số ảnh |
| Notebook TSVM trong `02_ma_nguon/notebook_kaggle/` | Trỏ tới fork cũ, tên run không có `_FP32` | Không phải đúng phiên bản đã chạy bộ chính ([05](05_CAU_HINH_HUAN_LUYEN.md)) |
| `raw_20seeds_confusion_matrices.csv` ở gốc gói | Có cột `TN_reconstructed = 40 − FP` | Cột không hợp lệ ([08](08_MA_TRAN_NHAM_LAN.md)) |
| Nhãn mô hình trong raw CSV của gói | `TSVM` | Trỏ tới thư mục `TSVM_FP32`, dữ liệu vẫn đúng |
