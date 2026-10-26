# 13. Bản đồ thư mục

Cây thư mục được sắp xếp lại ngày 26/10/2026. Toàn bộ 84 mục (51.091 file, 16,88 GiB) chỉ được **di chuyển hoặc đổi tên**, không có file nào bị xóa hay sửa nội dung. Bảng tra đường dẫn cũ sang mới nằm ở [PATH_MAP.md](../PATH_MAP.md) và [PATH_MAP.csv](../PATH_MAP.csv).

## Cây thư mục

```
Test_Mau/
├── README.md                    điểm vào
├── PATH_MAP.md, PATH_MAP.csv    tra đường dẫn cũ sang mới
├── 00_tai_lieu_tong_quan/       bộ tài liệu này (14 file .md, scripts/, bang/)
├── 01_du_lieu/                  BG20, split, script tạo dữ liệu
├── 02_ma_nguon/                 fork TSVM FP32, notebook Kaggle
├── 03_ket_qua_huan_luyen/       40 lượt chính (Baseline + TSVM FP32, seed 0–19)
├── 04_phan_tich_20seed/         gói phân tích 20 seed (CSV, hình, benchmark)
├── 05_so_sanh_mo_hinh_khac/     PraNet, U-Net
├── 06_bao_cao/                  Word/PDF khóa luận
├── 07_kiem_toan_va_sua/         kiểm toán 25/10 và sửa lỗi 26/10
└── 99_luu_tru/                  lịch sử và thử nghiệm, không dùng cho bảng chính
```

## Bộ chính

| Nội dung | Đường dẫn |
|---|---|
| Dữ liệu BG20 (1.200 ảnh và nhãn YOLO) | `01_du_lieu/Kvasir_YOLO_SEG_BG20/` (bản nén: `01_du_lieu/Kvasir_YOLO_SEG_BG20.rar`) |
| Danh sách split polyp 880/120 | `01_du_lieu/train.txt`, `01_du_lieu/val.txt` |
| YAML dữ liệu bản local | `01_du_lieu/data_bg20.yaml` (trường `path` vẫn là đường dẫn tuyệt đối cũ, xem ghi chú bên dưới) |
| Ảnh gốc (dữ liệu thô) Kvasir-SEG và normal-cecum | `01_du_lieu/tao_BG20/` |
| **Script tiền xử lý BG20** (dữ liệu thô → dữ liệu sạch) | `01_du_lieu/scripts_tien_xu_ly/convert_kvasir_with_background_to_yolo_seg.py` |
| Script chuyển đổi tham khảo (không dùng cho BG20) | `99_luu_tru/nhap/Stracth/Du_Lieu/convert_kvasir_to_yolo_seg.py` (bản không nền), `convert_datasets_to_yolo_seg.py` (CVC/ETIS) |
| Fork Ultralytics 8.4.127 + TSVM + bản vá FP32 | `02_ma_nguon/ultralytics_TSVM_FP32/` |
| Notebook Kaggle | `02_ma_nguon/notebook_kaggle/` (bản TSVM là bản trước khi vá FP32) |
| **Baseline, seed 0–19** | `03_ket_qua_huan_luyen/Baseline_YOLO26s_seg/Kvasir_BG20_Baseline_YOLO26s_seg_s{0..19}_w2/` |
| **TSVM FP32, seed 0–19** | `03_ket_qua_huan_luyen/TSVM_FP32/Kvasir_BG20_YOLO26s_seg_TSVM_FP32_s{0..19}_w2/` |
| Gói phân tích 20 seed | `04_phan_tich_20seed/` (cấu trúc con 01–07, `figures/`, `efficiency_benchmark/` giữ nguyên) |
| Báo cáo Word chính | `06_bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx` |
| Báo cáo bản mở rộng FP32 | `06_bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong_MoRong_FP32.docx` |
| Biểu mẫu và mẫu khóa luận | `06_bao_cao/Bieu mau do an_khoa luan. K.CNTT_HUIT_2025_V3.docx`, `06_bao_cao/mau/KhoaLuanMau.pdf` |
| Kiểm toán và sửa lỗi | `07_kiem_toan_va_sua/audit_20261025_193105/`, `07_kiem_toan_va_sua/fix_20261026/` |

Mỗi thư mục run có: `args.yaml`, `results.csv`, `weights/best.pt` và `last.pt`, các ảnh đường cong (`Mask*`, `Box*`), `confusion_matrix*.png`, cùng ảnh batch huấn luyện và validation.

## Mô hình so sánh

| Nội dung | Đường dẫn | Tình trạng |
|---|---|---|
| PraNet, 20 seed | `05_so_sanh_mo_hinh_khac/PraNet/` | Chỉ có `.pth` |
| U-Net, 20 seed | `05_so_sanh_mo_hinh_khac/UNet/` | Chỉ có `.pth` |

## 99_luu_tru

| Thư mục | Nội dung |
|---|---|
| `ket_qua_cu/Baseline_seed20-22/` | Baseline seed 20–22 (ngoài bộ chính) |
| `ket_qua_cu/TSVM_cu_checkpoint_FP16_seed0-20/` | TSVM trước khi vá, checkpoint float16 |
| `ket_qua_cu/KQ_Nen_DX_10seed/` | Bộ phân tích 10 seed cũ |
| `ket_qua_cu/efficiency_benchmark_TSVM_cu/` | Benchmark cũ (có GFLOPs, VRAM của TSVM cũ, không dùng) |
| `thu_nghiem_ket_hop/AV_FP32/`, `AVF_FP32/`, `ITSVM_FP32/` | Thử nghiệm dạng kết hợp khác, không đưa vào báo cáo. Mỗi mô hình đủ 20 seed (0–19). AV seed 15 và AVF seed 2 được giải nén bổ sung ngày 26/10 |
| `thu_nghiem_ket_hop/zip_kaggle_goc/` | File zip gốc tải từ Kaggle của AV seed 15 và AVF seed 2, giữ lại sau khi giải nén |
| `ma_nguon_cu/ultralytics_TSVM_cu_FP16/` | Fork TSVM trước khi vá FP32 |
| `ma_nguon_cu/ultralytics_8.4.127_goc/` | Bản sao Ultralytics 8.4.127 |
| `du_lieu_cu/Kvasir_YOLO_SEG.rar` | Bộ dữ liệu không có ảnh nền (cũ) |
| `tai_lieu_cu/archive_doc/` | Toàn bộ `archive/doc` cũ (kể cả AI_WORK_OPTIMIZATION_RULE, nguyên tắc làm việc) |
| `tai_lieu_cu/README_goc_cu.md`, `CURRENT_PROJECT_STATUS_goc_cu.md`, `BAO_CAO_DAC_TA_HUONG_NGHIEN_CUU.md` | Các file điểm vào cũ ở thư mục gốc |
| `log_kaggle_cu/` | 3 log Kaggle và `seed0_log.txt` |
| `nhap/` | `Stracth`, `.codex_report_work_20261015`, `.codex_revision_20261016` |
| `pipeline_semantic/` | `data_prep`, `datasets`, `tests`, `analyze_runs*.py`, `smoke_test.py`, `implementation_plan.md`, `task.md`, `walkthrough.md` |

Bản Word cũ và nháp báo cáo nằm trong `06_bao_cao/luu_tru_cu/`.

## Ghi chú sau khi sắp xếp

- **Script cũ ghi cứng đường dẫn `archive/...`** sẽ không chạy lại được nếu không sửa đường dẫn. Các script này nằm trong `07_kiem_toan_va_sua/`, `99_luu_tru/nhap/.codex_*`, `04_phan_tich_20seed/efficiency_benchmark/scripts/` và tài liệu cũ. Chúng được **giữ nguyên làm bằng chứng**. Muốn chạy lại thì tra [PATH_MAP.md](../PATH_MAP.md).
- Script tạo dữ liệu `01_du_lieu/scripts_tien_xu_ly/convert_kvasir_with_background_to_yolo_seg.py` mặc định suy ra thư mục gốc theo cấu trúc cũ. Sau khi sắp xếp, cần truyền tham số rõ ràng:

  ```bash
  python 01_du_lieu/scripts_tien_xu_ly/convert_kvasir_with_background_to_yolo_seg.py --archive-root 01_du_lieu --source-root tao_BG20 --output generated/BG20_replay --dry-run
  ```

  - Chạy lệnh từ thư mục gốc `Test_Mau`.
  - `--source-root` và `--output` được tính **tương đối với `--archive-root`**.
  - Script đọc `train.txt` và `val.txt` trong `--archive-root`. Nó từ chối ghi vào thư mục đã tồn tại.
  - Đã chạy thử với `--dry-run` (không tạo file nào), cả trước và sau khi chuyển script vào `scripts_tien_xu_ly/`. Script đọc đủ 880/120 ảnh polyp và 1.000 ảnh normal-cecum. Danh sách 200 ảnh nền được chọn với seed 42 **trùng khớp cả thứ tự** với `selected_normal_cecum_train_160.txt` và `selected_normal_cecum_val_40.txt` của bộ dữ liệu đang dùng.
  - Bỏ `--dry-run` thì script tạo bản dựng lại ở `01_du_lieu/generated/BG20_replay`. Bước này chưa chạy.
- `01_du_lieu/data_bg20.yaml` và `Kvasir_YOLO_SEG_BG20/data_bg20.yaml` vẫn ghi đường dẫn tuyệt đối cũ trong trường `path`. Hai file được giữ nguyên vì đó là hiện vật gốc. Khi huấn luyện lại ở máy local, cần tạo YAML mới trỏ tới `01_du_lieu/Kvasir_YOLO_SEG_BG20`.
- Script [`00_tai_lieu_tong_quan/scripts/tinh_lai_so_lieu.py`](scripts/tinh_lai_so_lieu.py) **đã được cập nhật** theo cây mới. Chạy lại sau khi sắp xếp cho ra 11 bảng giống hệt từng byte so với trước.
