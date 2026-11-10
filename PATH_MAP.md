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

## Chuyển thêm (26/10/2026)

| Đường dẫn cũ | Đường dẫn mới |
|---|---|
| `archive/Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/figures` (sau là `04_phan_tich_20seed/figures`) | `99_luu_tru/hinh_cu/figures_20seed` |
| `archive/Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/05_charts` (sau là `04_phan_tich_20seed/05_charts`) | `99_luu_tru/hinh_cu/charts_20seed` |
| `archive/Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/efficiency_benchmark/figures` | `99_luu_tru/hinh_cu/efficiency_benchmark_figures` |

Lý do: bộ hình được vẽ lại toàn bộ từ CSV, đặt ở `06_bao_cao/hinh/`.

## Tổ chức lại thư mục hình (27/10/2026)

Chuyển bằng `os.rename`, không sửa nội dung: 112 file (56 trong `vi/`, 56 trong `en/`).

| Đường dẫn cũ | Đường dẫn mới |
|---|---|
| `06_bao_cao/hinh/{vi,en}/` các hình a01–a04, d01–d04, e02, e03, m01, q01 | `06_bao_cao/hinh/chung/{vi,en}/` |
| `06_bao_cao/hinh/{vi,en}/` các hình h01, h01b, h02, h03, h04, r01–r05, c01, c02, e01, p01–p03 (20 seed) | `06_bao_cao/hinh/ket_qua_20seed/{vi,en}/` |

Thư mục mới `06_bao_cao/hinh/ket_qua_10seed/{vi,en}/` chứa bộ hình vẽ lại trên seed 0–9. Bảng tương ứng ở `00_tai_lieu_tong_quan/bang/10seed/`.

## Giải nén kết quả ablation (28/10/2026)

Sáu file zip tải từ Kaggle nằm ở thư mục gốc repo được giải nén (đã `unzip -t`, không lỗi). Bản zip gốc được giữ nguyên, chuyển vào `03_ket_qua_huan_luyen/_zip_goc_ablation/`.

| Đường dẫn cũ (zip) | Thư mục kết quả mới |
|---|---|
| `runs_Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s{0,1}_w2.zip` | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s{0,1}_w2/` |
| `runs_Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s{0,1,2,3}_w2.zip` | `03_ket_qua_huan_luyen/Vmamba_only/Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s{0,1,2,3}_w2/` |

## Giải nén kết quả ablation đợt 2 (29/10/2026)

Có tám file zip ở thư mục gốc repo. Cả tám đều qua kiểm tra `unzip -t`, không lỗi. Sau khi giải nén, bản zip gốc được chuyển vào `03_ket_qua_huan_luyen/_zip_goc_ablation/`. Tên thư mục, `seed` và `model` trong `args.yaml` khớp nhau ở cả 15 lượt ablation.

| Đường dẫn cũ (zip) | Thư mục kết quả mới |
|---|---|
| `runs_Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s{2,3}_w2.zip` | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s{2,3}_w2/` |
| `runs_Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s4_w2.zip` | `03_ket_qua_huan_luyen/Vmamba_only/Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s4_w2/` |
| `runs_Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s{0..4}_w2.zip` | `03_ket_qua_huan_luyen/No_guidance/Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s{0..4}_w2/` (thư mục `No_guidance/` mới) |

Ghi chú về `shape_only` seed 3:
- Thư mục cũ chỉ có `results.csv` mà không có `weights/`. Nó được chuyển sang `03_ket_qua_huan_luyen/_zip_goc_ablation/_ban_cu_truoc_khi_giai_nen/` và thay bằng bản trong zip, có đủ `best.pt`/`last.pt`.
- Hai bản `results.csv` giống hệt nhau ở mọi cột chỉ số; chỉ khác cột `time`. Mask mAP50–95 cực đại của cả hai đều là 0,72962.

Bổ sung cùng ngày, `shape_only` seed 4:
- File `runs_Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s4_w2.zip` qua kiểm tra `unzip -t`, không lỗi. Nội dung được giải nén vào `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s4_w2/`, zip gốc chuyển vào `_zip_goc_ablation/`.
- Thư mục cũ (không có `weights/`) được chuyển vào `_zip_goc_ablation/_ban_cu_truoc_khi_giai_nen/`.
- Như ở seed 3, hai bản `results.csv` chỉ khác cột `time`; `args.yaml` giống nhau. Mask mAP50–95 cực đại của cả hai là 0,70953.
- Kết quả: đủ 15/15 lượt ablation, lượt nào cũng có `best.pt` và `last.pt`.

## Chuyển file nén và file trùng ra ngoài repo (09/11/2026)

Dọn thư mục để nộp. Các mục dưới đây được **chuyển** (không xóa) sang `../_Luu_Tru_Ngoai/Test_Mau/`, giữ nguyên đường dẫn con. Danh sách đầy đủ, kèm dung lượng và lý do, nằm ở `../_Luu_Tru_Ngoai/DANH_SACH_DA_CHUYEN.csv`. Muốn trả lại thì chuyển ngược về đúng đường dẫn cũ.

| Đường dẫn cũ | Ghi chú |
|---|---|
| `03_ket_qua_huan_luyen/_zip_goc_ablation/` (gồm `_ban_chay_lai/`, `_ban_cu_truoc_khi_giai_nen/`) | Zip gốc Kaggle, đã giải nén vào `03_` |
| `03_ket_qua_huan_luyen/_zip_goc_C2PSA_rong/` | Zip gốc Kaggle, đã giải nén vào `03_` |
| `05_so_sanh_mo_hinh_khac/_zip_goc_640/` (gồm `_ban_trung/`) | Zip gốc PraNet/U-Net 640, đã giải nén vào `05_` |
| `01_du_lieu/Kvasir_YOLO_SEG_BG20.rar` | Bản nén của thư mục dữ liệu (thư mục vẫn còn) |
| `02_ma_nguon/*.rar` | Bản nén để tải lên Kaggle (thư mục nguồn vẫn còn) |
| `02_ma_nguon/ultralytics_MambaPSA/`, `02_ma_nguon/notebook_kaggle/mambapsa/` | MambaPSA đã bỏ |
| `06_bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong_MoRong_FP32.docx` | Trùng từng byte với `CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx` |
| `06_bao_cao/CNTT_KLCN182_LeDucLuong (2).docx`, `06_bao_cao/luu_tru_cu/CNTT_KLCN182_LeDucLuong (2).docx/.pdf` | Trùng từng byte với bản `_13-10` |
| `.pytest_cache/`, `01_du_lieu/tao_BG20/__pycache__/`, `archive/` (rỗng) | Bộ nhớ đệm, thư mục rỗng |

## Giải nén No_guidance seed 14 và 15 (09/11/2026)

Hai file `runs_Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s{14,15}_w2.zip` ở thư mục gốc qua kiểm tra `unzip -t`, không lỗi. Nội dung được giải nén vào `03_ket_qua_huan_luyen/No_guidance/Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s{14,15}_w2/`; mỗi lượt có `best.pt` và `last.pt`. `args.yaml` khớp seed 13 ở mọi khóa trừ `seed`, `name`. Zip gốc được chuyển sang `../_Luu_Tru_Ngoai/Test_Mau/03_ket_qua_huan_luyen/_zip_goc_ablation/`. No_guidance đủ 20/20 seed.

## Dọn cho bản nộp (10/11/2026)

Đối chiếu với bản Word cuối `06_bao_cao/CNTT_KLCN182-PhungTheBao.docx`. Mọi thứ không thuộc kết quả trong bản Word, cùng bản nháp và ghi chú làm việc, được **chuyển** (không xóa) sang `../_Luu_Tru_Ngoai/Test_Mau/`, giữ nguyên đường dẫn con: 546 mục, 42.258 file, 12,77 GiB. Danh sách từng mục (đường dẫn cũ, mới, số file, số byte, lý do) nằm ở cuối `PATH_MAP.csv` (trạng thái `CHUYEN_RA_NGOAI_10_11`) và ở `../_Luu_Tru_Ngoai/DANH_SACH_DA_CHUYEN.csv`. Muốn trả lại thì chuyển ngược về đúng đường dẫn cũ.

| Nhóm | Đường dẫn cũ | Bản dùng thay |
|---|---|---|
| PraNet/U-Net 352 | `05_so_sanh_mo_hinh_khac/PraNet/`, `UNet/`; `00_tai_lieu_tong_quan/bang/10–15`, `20`, `20b`, `_log_danh_gia_pixel.txt`, `_log_topology.txt`; hình `ket_qua_20seed/*/p0*, o0*, x0*`, `chung/*/q01_*`, `hinh/du_lieu_dinh_tinh/`; `08_du_lieu_thuc_te/bang/20seed/`, lượt `*_pranet_s*`, `*_unet_s*`, `du_lieu_dinh_tinh/*_pranet.npz`, `*_unet.npz`, log 352 | `05_so_sanh_mo_hinh_khac/PraNet_640/`, `UNet_640/`; `bang/pixel_640/`; `hinh/ket_qua_20seed_640/` |
| Bộ 10 seed | `bang/10seed/`, `00_tai_lieu_tong_quan/06b_KET_QUA_10_SEED.md`, `hinh/ket_qua_10seed/`, `08_du_lieu_thuc_te/bang/10seed/` | bộ 20 seed |
| Ablation 5 và 10 seed | `bang/17_*`, `17b_*`, `18_*`, `_log_ablation.txt`, `bang/ablation_10seed/`, `hinh/ablation_10seed/`, `hinh/chung/*/k01_*`, `k02_*` | `bang/ablation_20seed/`, `hinh/ablation_20seed/` |
| Lần đo GPU thứ nhất | `bang/16_lan1_*`, `16b_lan1_*`, `_log_flops_gpu_lan1.txt` | `bang/16_*`, `16b_*`, `16c_*` |
| Word/PDF cũ và nháp | các `.docx`/`.pdf` cũ trong `06_bao_cao/` (kể cả `CNTT_KLCN182-Phung The Bao.pdf`), `06_bao_cao/{md_bao_cao, md_bao_cao_70, md_bao_cao_rut_gon, ghep_word, new_bao_cao, luu_tru_cu, mau}/` | `06_bao_cao/CNTT_KLCN182-PhungTheBao.docx` |
| Ghi chú làm việc | `AGENTS.md`, `CHUYEN_GIAO_CODEX.md`, `HUONG_DAN_LAM_VIEC_VOI_CLAUDE.md`, `KE_HOACH_HOAN_THIEN_NOP_BAI.md`, `NGU_CANH_DU_AN.md`, `.vscode/`, `06_bao_cao/{chinhsua, sua_theo_nhan_xet, slide}/`, `06_bao_cao/HUONG_DAN_LUONG_CHAY_*.md`, `05_so_sanh_mo_hinh_khac/PHAN_HOI_CHECKPOINT_640.md`, `08_du_lieu_thuc_te/bang/KET_QUA_CHAY_*.md`, `03_ket_qua_huan_luyen/Shape_only/HUONG_DAN_KIEM_TRA_KAGGLE.md` | |
| Bản trùng, file nén | `06_bao_cao/danh_gia_nen_cecum.py` (trùng `08_du_lieu_thuc_te/scripts/`), `08_du_lieu_thuc_te/bang/*.zip` (đã giải nén) | |
| Kiểm toán | `07_kiem_toan_va_sua/` | |
| Lưu trữ cũ | `99_luu_tru/` trừ `ket_qua_cu/TSVM_cu_checkpoint_FP16_seed0-20/` | |
| Mô hình không chạy | `02_ma_nguon/notebook_kaggle/polyp_pvt/`, `vm_unet/` | |

Cùng ngày:
- Script đổi mặc định sang bản dùng trong báo cáo: `danh_gia_pixel.py`, `danh_gia_topology.py` ghi vào `bang/pixel_640/`; `tinh_ablation.py` mặc định 20 seed; `08_du_lieu_thuc_te/scripts/danh_gia_du_lieu_ngoai.py`, `danh_gia_nen_cecum.py` ghi vào `bang/pixel_640/du_lieu_ngoai/`, `nen_cecum/`; `ve_hinh.py` tự ghi từng hình vào đúng thư mục; `xuat_chi_so_web.py` lấy PraNet/U-Net 640. Đã chạy lại mọi script không cần GPU: bảng sinh lại giống bản trước (chênh lớn nhất 1e-16), hình PNG trùng 100% điểm ảnh.
- File `research-metrics.json` của web được xuất lại: mốc PraNet/U-Net trên trang `/metrics` đổi từ bản 352 sang bản 640.
- Đổi tên thư mục dự án `Test_Mau` → `CNTT_KLCN182_PhungTheBao` (bước cuối). Thư mục lưu trữ ngoài giữ tên `_Luu_Tru_Ngoai/Test_Mau/`.

## Dọn lần hai cho bản nộp (10/11/2026, tối)

Rà lại để thư mục nộp chỉ còn mô hình và kết quả có trong bản Word cuối. 23 mục chuyển sang `../_Luu_Tru_Ngoai/Test_Mau/` (giữ đường dẫn con), liệt kê trong `PATH_MAP.csv` với trạng thái `CHUYEN_RA_NGOAI_10_11b`.

| Nhóm | Đã chuyển | Còn lại |
|---|---|---|
| TSVM cũ (checkpoint FP16) | `99_luu_tru/` (cả thư mục) | `tinh_lai_so_lieu.py` bỏ qua mục 3b khi không có thư mục này |
| Gói phân tích 20 seed đời đầu | `04_phan_tich_20seed/{02_statistics, 03_metrics, 04_confusion_matrix, 07_audit}`, `06_reports/*.md`, bốn CSV phụ trong `01_raw_analysis/`, các file ở gốc gói (`facts.json`, `raw_20seeds_*.csv`, `summary_20seeds_paired.csv`, `LEGACY_ARTIFACTS.md`, `README.md` cũ) | `01_raw_analysis/raw_20seeds_{extracted_metrics, confusion_matrices}.csv`, `06_reports/summary.csv`, `efficiency_benchmark/`, README mới |
| Bảng dữ liệu ngoài 10 seed | `00_tai_lieu_tong_quan/bang/pixel_640/du_lieu_ngoai/10seed/` | `du_lieu_ngoai/20seed/` |
| Tài liệu làm việc | `06_bao_cao/Nhan_xet_KLCN-CNTT-182*.docx`, `06_bao_cao/Bieu mau do an_khoa luan. K.CNTT_HUIT_2025_V3.docx` | |

Script: bỏ khóa `pranet`/`unet` (bản 352) khỏi `danh_gia_pixel.py`, sửa docstring cũ. Chạy lại mọi script không cần GPU: bảng CSV và hình PNG không đổi.
