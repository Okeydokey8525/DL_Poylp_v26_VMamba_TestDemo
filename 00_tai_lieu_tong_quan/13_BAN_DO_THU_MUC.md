# 13. Bản đồ thư mục

Cập nhật 10/11/2026 cho bản nộp. Thư mục đã được dọn: kết quả cũ (PraNet/U-Net 352, bộ 10 seed, ablation 5 và 10 seed), bản Word nháp, ghi chú làm việc, hiện vật kiểm toán và phần lớn `99_luu_tru/` được **chuyển** (không xóa) sang thư mục anh em `_Luu_Tru_Ngoai/<tên thư mục dự án>/`, giữ nguyên đường dẫn con. Bảng tra đường dẫn cũ sang mới nằm ở [PATH_MAP.md](../PATH_MAP.md) và [PATH_MAP.csv](../PATH_MAP.csv).

## Cây thư mục

```
CNTT_KLCN182_PhungTheBao/
├── README.md                    điểm vào cho người đọc
├── PATH_MAP.md, PATH_MAP.csv    tra đường dẫn cũ sang mới
├── 00_tai_lieu_tong_quan/       tài liệu tổng quan (16 file .md), scripts/, bang/
├── 01_du_lieu/                  BG20, split 880/120, script tạo dữ liệu, ảnh gốc
├── 02_ma_nguon/                 fork Ultralytics + TSVM FP32, fork C2PSA rộng, notebook Kaggle
├── 03_ket_qua_huan_luyen/       Baseline, TSVM_FP32, Vmamba_only, Shape_only, No_guidance, C2PSA_rong (mỗi loại seed 0–19)
├── 04_phan_tich_20seed/         gói phân tích 20 seed cũ hơn (đã đối chiếu khớp), benchmark CPU
├── 05_so_sanh_mo_hinh_khac/     PraNet_640, UNet_640 (20 seed mỗi mô hình)
├── 06_bao_cao/                  bản Word cuối, nhận xét của GVHD, biểu mẫu, hinh/
├── 08_du_lieu_thuc_te/          đánh giá trên CVC-ClinicDB, CVC-ColonDB, ETIS-Larib, PolypGen, 800 ảnh manh tràng
└── 99_luu_tru/                  chỉ còn lượt TSVM cũ (checkpoint FP16) để đối chiếu với bản FP32
```

## Bộ chính

| Nội dung | Đường dẫn |
|---|---|
| Dữ liệu BG20 (1.200 ảnh và nhãn YOLO) | `01_du_lieu/Kvasir_YOLO_SEG_BG20/` |
| Danh sách split polyp 880/120 | `01_du_lieu/train.txt`, `01_du_lieu/val.txt` |
| YAML dữ liệu | `01_du_lieu/data_bg20.yaml` (trường `path` vẫn là đường dẫn tuyệt đối lúc tạo, xem ghi chú bên dưới) |
| Ảnh gốc Kvasir-SEG và normal-cecum | `01_du_lieu/tao_BG20/` |
| **Script tiền xử lý BG20** | `01_du_lieu/scripts_tien_xu_ly/convert_kvasir_with_background_to_yolo_seg.py` |
| Fork Ultralytics 8.4.127 + TSVM + bản vá FP32 | `02_ma_nguon/ultralytics_TSVM_FP32/` (module `nn/modules/topology_shape_vmamba.py`, cấu hình `cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml`) |
| Fork cho đối chứng C2PSA rộng | `02_ma_nguon/ultralytics_C2PSA_rong/` |
| Notebook Kaggle | `02_ma_nguon/notebook_kaggle/` (YOLO gốc, TSVM, `ablation/`, `c2psa_rong/`, `pranet-new.ipynb`, `unet-new.ipynb` bản 640) |
| **Mô hình gốc, seed 0–19** | `03_ket_qua_huan_luyen/Baseline_YOLO26s_seg/Kvasir_BG20_Baseline_YOLO26s_seg_s{0..19}_w2/` |
| **TSVM FP32, seed 0–19** | `03_ket_qua_huan_luyen/TSVM_FP32/Kvasir_BG20_YOLO26s_seg_TSVM_FP32_s{0..19}_w2/` |
| Ablation, seed 0–19 | `03_ket_qua_huan_luyen/Vmamba_only/`, `Shape_only/`, `No_guidance/` |
| C2PSA rộng, seed 0–19 | `03_ket_qua_huan_luyen/C2PSA_rong/` |
| PraNet 640, U-Net 640, seed 0–19 | `05_so_sanh_mo_hinh_khac/PraNet_640/`, `UNet_640/` |
| Bảng số liệu | `00_tai_lieu_tong_quan/bang/` (xem [12](12_TRUY_VET_SO_LIEU.md)) |
| Hình báo cáo | `06_bao_cao/hinh/` (xem `06_bao_cao/hinh/README.md`) |
| Dữ liệu ngoài | `08_du_lieu_thuc_te/` (script, kết quả từng lượt, ảnh định tính); bảng tổng hợp ở `00_tai_lieu_tong_quan/bang/pixel_640/du_lieu_ngoai/`, `nen_cecum/` |
| **Báo cáo Word cuối** | `06_bao_cao/CNTT_KLCN182-PhungTheBao.docx` |
| Nhận xét của GVHD | `06_bao_cao/Nhan_xet_KLCN-CNTT-182.docx`, `Nhan_xet_KLCN-CNTT-182 (1).docx` |
| Biểu mẫu khoa | `06_bao_cao/Bieu mau do an_khoa luan. K.CNTT_HUIT_2025_V3.docx` |

Mỗi thư mục run YOLO có: `args.yaml`, `results.csv`, `weights/best.pt` và `last.pt`, các ảnh đường cong (`Mask*`, `Box*`), `confusion_matrix*.png`, ảnh batch huấn luyện và validation. Mỗi thư mục PraNet/U-Net 640 có `results.csv`, checkpoint tốt nhất, `last.pth`, `tom_tat.txt`.

## 99_luu_tru (còn lại)

| Thư mục | Nội dung |
|---|---|
| `ket_qua_cu/TSVM_cu_checkpoint_FP16_seed0-20/` | TSVM trước khi vá, checkpoint float16. `tinh_lai_so_lieu.py` đọc `results.csv` ở đây để đối chiếu với bản FP32 (mục 3b của log) |

## Đã chuyển ra lưu trữ ngoài (không nộp)

Các mục dưới đây nằm ở `_Luu_Tru_Ngoai/<tên thư mục dự án>/` với cùng đường dẫn con, danh sách đầy đủ trong `PATH_MAP.csv` (mục 10/11/2026):
- PraNet/U-Net 352 không tăng cường: checkpoint `05_so_sanh_mo_hinh_khac/PraNet/`, `UNet/`; bảng `bang/10–15`, `20`, `20b` cũ; hình `p01–p05`, `o01`, `o02`, `q01`, `x01–x03` bản 352; lượt 352 trong `08_du_lieu_thuc_te/bang/tung_luot/`;
- bộ 10 seed (`bang/10seed/`, `hinh/ket_qua_10seed/`, `08_du_lieu_thuc_te/bang/10seed/`, `06b_KET_QUA_10_SEED.md`);
- ablation 5 seed và 10 seed (`bang/17–18` cũ, `bang/ablation_10seed/`, `hinh/ablation_10seed/`, hình `k01`, `k02` 5 seed);
- bản Word, PDF nháp và chương markdown bản V3 (`06_bao_cao/md_bao_cao*/`, `ghep_word/`, `luu_tru_cu/`, `new_bao_cao/`, `mau/`);
- ghi chú làm việc (`AGENTS.md`, `CHUYEN_GIAO_CODEX.md`, `HUONG_DAN_LAM_VIEC_VOI_CLAUDE.md`, `KE_HOACH_HOAN_THIEN_NOP_BAI.md`, `NGU_CANH_DU_AN.md`, `06_bao_cao/chinhsua/`, `sua_theo_nhan_xet/`, `slide/`);
- `07_kiem_toan_va_sua/` (kiểm toán 25/10 và sửa lỗi 26/10);
- `99_luu_tru/` trừ checkpoint FP16 (dữ liệu cũ, mã nguồn cũ, log Kaggle cũ, thử nghiệm AV/AVF/ITSVM);
- notebook Polyp-PVT và VM-UNet (không chạy, chỉ nêu ở hướng phát triển).

## Ghi chú

- Script tạo dữ liệu `01_du_lieu/scripts_tien_xu_ly/convert_kvasir_with_background_to_yolo_seg.py` cần truyền tham số rõ ràng (chạy từ thư mục gốc dự án):

  ```bash
  python 01_du_lieu/scripts_tien_xu_ly/convert_kvasir_with_background_to_yolo_seg.py --archive-root 01_du_lieu --source-root tao_BG20 --output generated/BG20_replay --dry-run
  ```

  - `--source-root` và `--output` được tính **tương đối với `--archive-root`**.
  - Script đọc `train.txt` và `val.txt` trong `--archive-root` và từ chối ghi vào thư mục đã tồn tại.
  - Đã chạy thử với `--dry-run`: script đọc đủ 880/120 ảnh polyp và 1.000 ảnh normal-cecum; danh sách 200 ảnh nền chọn với seed 42 **trùng cả thứ tự** với `selected_normal_cecum_train_160.txt` và `selected_normal_cecum_val_40.txt` của bộ dữ liệu đang dùng.
- `01_du_lieu/data_bg20.yaml` và `Kvasir_YOLO_SEG_BG20/data_bg20.yaml` vẫn ghi đường dẫn tuyệt đối lúc tạo trong trường `path`, giữ nguyên vì là hiện vật gốc. Khi huấn luyện lại ở máy khác, tạo YAML mới trỏ tới `01_du_lieu/Kvasir_YOLO_SEG_BG20`.
- Script trong `04_phan_tich_20seed/efficiency_benchmark/scripts/` còn ghi đường dẫn `archive/...` cũ; muốn chạy lại thì tra [PATH_MAP.md](../PATH_MAP.md).
