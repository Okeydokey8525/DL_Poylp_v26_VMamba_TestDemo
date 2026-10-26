# PATH_MAP: đường dẫn cũ sang đường dẫn mới

Ngày 26/10/2026 cây thư mục được sắp xếp lại. Có **84 mục, 51.091 file, 16,88 GiB**, tất cả chỉ được di chuyển bằng `os.rename` (không xóa, không sửa nội dung). Sau khi chuyển, số file và tổng dung lượng của từng mục đã được kiểm tra lại và khớp 84/84. Danh sách đầy đủ từng mục kèm số file và dung lượng nằm ở [PATH_MAP.csv](PATH_MAP.csv).

**Cách dùng:** script và tài liệu cũ (trong `07_kiem_toan_va_sua/`, `99_luu_tru/`, `04_phan_tich_20seed/…/scripts/`, `06_bao_cao/luu_tru_cu/`) vẫn ghi đường dẫn `archive/...`. Chúng được giữ nguyên làm bằng chứng. Khi cần chạy lại hoặc đọc, thay tiền tố cũ bằng tiền tố mới theo bảng dưới. Hãy khớp tiền tố **dài nhất** trước.

| Đường dẫn cũ | Đường dẫn mới |
|---|---|
| `TaiLieu_TongQuan_Base_TSVM_FP32` | `00_tai_lieu_tong_quan` |
| `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20` | `01_du_lieu/Kvasir_YOLO_SEG_BG20` |
| `archive/train.txt` | `01_du_lieu/train.txt` |
| `archive/val.txt` | `01_du_lieu/val.txt` |
| `archive/data_bg20.yaml` | `01_du_lieu/data_bg20.yaml` |
| `archive/Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py` | `01_du_lieu/scripts_tien_xu_ly/convert_kvasir_with_background_to_yolo_seg.py` (chuyển thêm ngày 26/10) |
| `archive/Ket_Qua_V2/Data Prosessing` | `01_du_lieu/tao_BG20` |
| `archive/Kvasir_YOLO_SEG_BG20.rar` | `01_du_lieu/Kvasir_YOLO_SEG_BG20.rar` |
| `archive/ultralytics_Topology-Shape-aware_VMamba_FP32` | `02_ma_nguon/ultralytics_TSVM_FP32` |
| `archive/ultralytics_Topology-Shape-aware_VMamba_FP32.rar` | `02_ma_nguon/ultralytics_TSVM_FP32.rar` |
| `archive/Cell Kaggle` | `02_ma_nguon/notebook_kaggle` |
| `archive/Ket_Qua_V2/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM_FP32` | `03_ket_qua_huan_luyen/TSVM_FP32` |
| `archive/Ket_Qua_V2/KQ_Nen_DX_20seed_FP32` | `04_phan_tich_20seed` |
| `archive/Ket_Qua_V2/KQ_Model_Khac/PraNet` | `05_so_sanh_mo_hinh_khac/PraNet` |
| `archive/Ket_Qua_V2/KQ_Model_Khac/Unet` | `05_so_sanh_mo_hinh_khac/UNet` |
| `archive/Bao_cao/md viet bao cao` | `06_bao_cao/luu_tru_cu/md_viet_bao_cao` |
| `archive/Bao_cao/backup` | `06_bao_cao/luu_tru_cu/backup` |
| `archive/Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong_Cu.docx` | `06_bao_cao/luu_tru_cu/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong_Cu.docx` |
| `output/KhoaLuanMau.pdf` | `06_bao_cao/mau/KhoaLuanMau.pdf` |
| `archive/audit_20261025_193105` | `07_kiem_toan_va_sua/audit_20261025_193105` |
| `archive/fix_20261026` | `07_kiem_toan_va_sua/fix_20261026` |
| `archive/audit_runs_data.json` | `07_kiem_toan_va_sua/audit_runs_data.json` |
| `archive/Ket_Qua_V2/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM` | `99_luu_tru/ket_qua_cu/TSVM_cu_checkpoint_FP16_seed0-20` |
| `archive/Ket_Qua_V2/KQ_Model_Khac/Kvasir_BG20_YOLO26s_seg_AV_FP32` | `99_luu_tru/thu_nghiem_ket_hop/AV_FP32` |
| `archive/Ket_Qua_V2/KQ_Model_Khac/Kvasir_BG20_YOLO26s_seg_AVF_FP32` | `99_luu_tru/thu_nghiem_ket_hop/AVF_FP32` |
| `archive/Ket_Qua_V2/KQ_Model_Khac/Kvasir_BG20_YOLO26s_seg_ITSVM_FP32` | `99_luu_tru/thu_nghiem_ket_hop/ITSVM_FP32` |
| `archive/Ket_Qua_V2/KQ_Nen_DX_10seed` | `99_luu_tru/ket_qua_cu/KQ_Nen_DX_10seed` |
| `archive/Ket_Qua_V2/efficiency_benchmark` | `99_luu_tru/ket_qua_cu/efficiency_benchmark_TSVM_cu` |
| `archive/ultralytics_Topology-Shape-aware VMamba` | `99_luu_tru/ma_nguon_cu/ultralytics_TSVM_cu_FP16` |
| `archive/ultralytics` | `99_luu_tru/ma_nguon_cu/ultralytics_8.4.127_goc` |
| `archive/Kvasir_YOLO_SEG.rar` | `99_luu_tru/du_lieu_cu/Kvasir_YOLO_SEG.rar` |
| `archive/doc` | `99_luu_tru/tai_lieu_cu/archive_doc` |
| `README.md` | `99_luu_tru/tai_lieu_cu/README_goc_cu.md` |
| `CURRENT_PROJECT_STATUS.md` | `99_luu_tru/tai_lieu_cu/CURRENT_PROJECT_STATUS_goc_cu.md` |
| `BAO_CAO_DAC_TA_HUONG_NGHIEN_CUU.md` | `99_luu_tru/tai_lieu_cu/BAO_CAO_DAC_TA_HUONG_NGHIEN_CUU.md` |
| `archive/Stracth` | `99_luu_tru/nhap/Stracth` |
| `archive/.codex_report_work_20261015` | `99_luu_tru/nhap/.codex_report_work_20261015` |
| `archive/.codex_revision_20261016` | `99_luu_tru/nhap/.codex_revision_20261016` |
| `archive/__pycache__` | `99_luu_tru/nhap/archive__pycache__` |
| `archive/kvasir-yolo26s-seg-topology-shape-awar (1).log` | `99_luu_tru/log_kaggle_cu/kvasir-yolo26s-seg-topology-shape-awar (1).log` |
| `archive/kvasir-yolo26s-seg-topology-shape-awar (2).log` | `99_luu_tru/log_kaggle_cu/kvasir-yolo26s-seg-topology-shape-awar (2).log` |
| `archive/kvasir-yolo26s-seg-topology-shape-awar (3).log` | `99_luu_tru/log_kaggle_cu/kvasir-yolo26s-seg-topology-shape-awar (3).log` |
| `archive/seed0_log.txt` | `99_luu_tru/log_kaggle_cu/seed0_log.txt` |
| `data_prep` | `99_luu_tru/pipeline_semantic/data_prep` |
| `datasets` | `99_luu_tru/pipeline_semantic/datasets` |
| `tests` | `99_luu_tru/pipeline_semantic/tests` |
| `analyze_runs.py` | `99_luu_tru/pipeline_semantic/analyze_runs.py` |
| `analyze_runs_p1.py` | `99_luu_tru/pipeline_semantic/analyze_runs_p1.py` |
| `smoke_test.py` | `99_luu_tru/pipeline_semantic/smoke_test.py` |
| `implementation_plan.md` | `99_luu_tru/pipeline_semantic/implementation_plan.md` |
| `task.md` | `99_luu_tru/pipeline_semantic/task.md` |
| `walkthrough.md` | `99_luu_tru/pipeline_semantic/walkthrough.md` |
| `archive/Ket_Qua_V2/KetQua_Nen/YOLOv26s-seg/Kvasir_BG20_Baseline_YOLO26s_seg_s{0..19}_w2` | `03_ket_qua_huan_luyen/Baseline_YOLO26s_seg/Kvasir_BG20_Baseline_YOLO26s_seg_s{0..19}_w2` |
| `archive/Ket_Qua_V2/KetQua_Nen/YOLOv26s-seg/Kvasir_BG20_Baseline_YOLO26s_seg_s{20,21,22}_w2` | `99_luu_tru/ket_qua_cu/Baseline_seed20-22/Kvasir_BG20_Baseline_YOLO26s_seg_s{20,21,22}_w2` |
| `archive/Bao_cao/Bieu mau do an_khoa luan. K.CNTT_HUIT_2025_V3.docx` | `06_bao_cao/Bieu mau do an_khoa luan. K.CNTT_HUIT_2025_V3.docx` |
| `archive/Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx` | `06_bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx` |
| `archive/Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong_MoRong_FP32.docx` | `06_bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong_MoRong_FP32.docx` |
| `archive/Bao_cao/CNTT_KLCN182_LeDucLuong (2).docx` | `06_bao_cao/CNTT_KLCN182_LeDucLuong (2).docx` |
| `archive/Bao_cao/CNTT_KLCN182_LeDucLuong (2).pdf` | `06_bao_cao/CNTT_KLCN182_LeDucLuong (2).pdf` |
| `archive/Bao_cao/CNTT_KLCN182_LeDucLuong_13-10.docx` | `06_bao_cao/CNTT_KLCN182_LeDucLuong_13-10.docx` |
| `archive/Bao_cao/CNTT_KLCN182_LeDucLuong_13-10.pdf` | `06_bao_cao/CNTT_KLCN182_LeDucLuong_13-10.pdf` |
| `archive/Bao_cao/LUA_CHON_VA_BO_SUNG_TAI_LIEU_THAM_KHAO.md` | `06_bao_cao/LUA_CHON_VA_BO_SUNG_TAI_LIEU_THAM_KHAO.md` |
| `archive/Bao_cao/RA_SOAT_BAN_THAO_MD_2026_10_12.md` | `06_bao_cao/RA_SOAT_BAN_THAO_MD_2026_10_12.md` |
| `archive/Bao_cao/Tien_Xu_Ly_Du_Lieu.docx` | `06_bao_cao/Tien_Xu_Ly_Du_Lieu.docx` |

Các thư mục cũ đã rỗng sau khi chuyển: `archive/Ket_Qua_V2/...`, `archive/Bao_cao`, `output/`. Chúng đã được xóa (riêng `archive/` có thể còn lại dưới dạng thư mục rỗng nếu đang bị chương trình khác mở).
