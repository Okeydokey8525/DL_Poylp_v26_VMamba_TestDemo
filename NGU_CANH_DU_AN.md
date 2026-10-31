# Ngữ cảnh dự án (dành cho AI/người mới tiếp nhận)

Cập nhật: 29/10/2026. Hạn nộp khóa luận: **08/11/2026**.

Thứ tự đọc:
1. File này.
2. [CLAUDE.md](CLAUDE.md) (quy tắc, lệnh) hoặc [AGENTS.md](AGENTS.md).
3. [00_tai_lieu_tong_quan/00_README.md](00_tai_lieu_tong_quan/00_README.md).

Cách chủ dự án làm việc và lịch sử công việc: [HUONG_DAN_LAM_VIEC_VOI_CLAUDE.md](HUONG_DAN_LAM_VIEC_VOI_CLAUDE.md).

## 1. Dự án là gì

**Khóa luận tốt nghiệp cử nhân CNTT, Trường ĐH Công Thương TP.HCM (HUIT), mã CNTT_KLCN182.**
- GVHD: Phùng Thế Bảo.
- Nhóm: Lê Đức Lương (2001230490), Phùng Tuấn Huy (2001230312), Trần Mạnh Toàn (2001230830).

Đề tài: *Nghiên cứu phương pháp tích hợp VMamba vào YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng.*

- **Bài toán:** phân đoạn thực thể (instance segmentation), một lớp `polyp`, trên ảnh nội soi.
- **Mô hình đối chứng:** **YOLO26s-seg** (Ultralytics 8.4.127).
- **Mô hình đề xuất:** **YOLO26s-seg + C2TSVMamba (TSVM FP32)**. Tầng 10 (`C2PSA`, mức P5, đặc trưng 20×20) được thay bằng khối VMamba gồm:
  - quét chọn lọc 4 hướng (SS2D);
  - nhánh hình dạng và nhánh hướng;
  - cổng điều biến `F·(1+G)`.
- **Về chữ "FP32":** chỉ có nghĩa là **checkpoint được lưu ở float32**. Fork cũ lưu float16 nên BatchNorm tầng 10 bị tràn số. Cả hai mô hình đều huấn luyện với `amp=False`.
- **Mô hình so sánh thêm:** **PraNet** (backbone ResNet-50) và **U-Net** (32 kênh), mỗi mô hình 20 seed.
- **Ứng dụng minh họa PolypVision:** web Spring Boot, ai-service FastAPI, app Flutter. Mã nằm ngoài repo, ở `C:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Ung_Dung\polypweb\`.

## 2. Thiết kế thực nghiệm và kết quả chính (đã xác minh)

### Dữ liệu và huấn luyện
- **Dữ liệu BG20**, tổng 1.200 ảnh:
  - Train 1.040 ảnh = 880 ảnh polyp + 160 ảnh nền.
  - Validation 160 ảnh = 120 ảnh polyp + 40 ảnh nền, chứa 127 đối tượng polyp.
  - Ảnh nền lấy từ normal-cecum (Kvasir v2).
  - Cách chia 880/120 **do tác giả Kvasir-SEG cung cấp** trên Kaggle (đã kiểm tra md5).
  - **Không có tập test riêng.**
- **Huấn luyện** trên Kaggle: 2 mô hình × 20 seed (0–19) × 100 epoch.
  - Cấu hình: imgsz 640, batch 8, AdamW, lr0 0,001, close_mosaic 10, `deterministic=True`.
  - Hai mô hình chỉ khác nhau ở tầng 10.
  - Khi validation, ảnh được letterbox thành khung 672.
- **Endpoint chính:** mask mAP50–95 tại epoch đạt cực đại của từng lượt chạy.
- **Báo cáo dùng 20 seed (0–19), chốt ngày 28/10/2026.** Số thập phân viết bằng dấu phẩy. Bộ 10 seed chỉ giữ để đối chiếu (`00_tai_lieu_tong_quan/06b_KET_QUA_10_SEED.md`).

### Kết quả 20 seed (dùng trong báo cáo)

| Chỉ số | Baseline | TSVM FP32 |
|---|---:|---:|
| Mask mAP50–95 | 0,7189 ± 0,0118 | 0,7232 ± 0,0072 |
| Δ, CI 95%, p | | +0,0043, [−0,0002; 0,0088], paired t p = 0,061 (Wilcoxon 0,070), d_z = 0,44 |
| Số seed TSVM cao hơn | | 13/20 |
| Độ ổn định (Levene trung vị, thăm dò) | | SD nhỏ hơn, p = 0,026 |
| Mask F1 (từ P và R) | 0,8806 | 0,8856 (p = 0,259; 12/20) |
| Tham số | 11.434.463 | 12.254.688 (+7,17%) |
| Tham số tầng 10 | 990.976 (C2PSA) | 1.811.201 (C2TSVMamba) |
| Độ trễ CPU (chỉ forward) | 269,6 ms | 577,4 ms (khoảng 2,1 lần) |
| Độ trễ GPU (lần đo 2, trung vị) | 26,33 ms | 39,86 ms (tỉ lệ khoảng 1,5–1,7 lần) |

→ **Chưa đạt ý nghĩa thống kê ở α = 0,05.** Không được viết "vượt trội". Không hiệu chỉnh so sánh bội, nên chỉ có endpoint chính được kết luận chắc chắn.

### Kết quả khác đã đo
- **Theo pixel** (Dice/IoU/P/R, 4 mô hình × 20 seed): Dice TSVM 0,854, đối chứng 0,849 (p = 0,26), PraNet 0,854, U-Net 0,710. Số liệu ở `00_tai_lieu_tong_quan/10_SO_SANH_PRANET_UNET.md`.
- **Topology** (lỗi Betti): TSVM chỉ nhích hơn mô hình gốc, không có ý nghĩa thống kê, và kém PraNet rõ rệt. Số liệu ở `14_CHI_SO_TOPOLOGY.md`.
- **Dữ liệu ngoài, Dice** (Baseline / TSVM / PraNet / U-Net), số liệu ở `08_du_lieu_thuc_te/`:

  | Bộ dữ liệu | Baseline | TSVM | PraNet | U-Net | TSVM so với Baseline |
  |---|---:|---:|---:|---:|---|
  | ClinicDB | 0,786 | 0,770 | 0,752 | 0,525 | kém hơn, p = 0,006 |
  | ColonDB | 0,631 | 0,601 | 0,539 | 0,375 | kém hơn, p < 0,001 |
  | ETIS | 0,535 | 0,529 | 0,466 | 0,284 | không khác biệt có ý nghĩa |
  | PolypGen | 0,719 | 0,715 | 0,683 | 0,484 | không khác biệt có ý nghĩa |

  Trên ảnh không có polyp của PolypGen, tỉ lệ báo nhầm là 13,3% / 10,8% / 22,6% / 69,3% (TSVM so với Baseline: p = 0,011).
- **GPU:** số ms tuyệt đối lệch 1,5–2 lần giữa hai phiên đo, nguyên nhân chưa xác minh. Chỉ báo cáo tỉ lệ giữa hai mô hình. Lần 1 được giữ lại với hậu tố `_lan1`.

### Đã kiểm chứng
- 40 file `results.csv` gốc khớp 100% với gói phân tích.
- Ma trận nhầm lẫn (TP/FP/FN) khớp 40/40 với ảnh gốc.
- Kiến trúc dựng lại có số tham số trùng với checkpoint.

### Không được suy diễn
- TN = 40 − FP.
- Dice hoặc IoU tính ra từ mAP.
- Lợi ích về topology vượt quá số đã đo.
- `val/sem_loss = 0` chỉ là giá trị ghi log, không có nghĩa là lỗi bằng 0.

## 3. Cây thư mục (`Test_Mau/`, git, nhánh `Okeydokey`)

| Thư mục | Nội dung |
|---|---|
| `00_tai_lieu_tong_quan/` | **Nguồn sự thật**: các file md `00`–`14`, `scripts/` (`tinh_lai_so_lieu.py`, `danh_gia_pixel.py`, `danh_gia_topology.py`, `do_flops_gpu.py`), `bang/*.csv` |
| `01_du_lieu/` | `Kvasir_YOLO_SEG_BG20/`, `train.txt`/`val.txt`, `tao_BG20/` (dữ liệu thô), `scripts_tien_xu_ly/` |
| `02_ma_nguon/` | Fork `ultralytics_TSVM_FP32/` (module ở `nn/modules/topology_shape_vmamba.py`); `notebook_kaggle/` (có `ablation/`) |
| `03_ket_qua_huan_luyen/` | 40 lượt chính `Baseline_YOLO26s_seg/`, `TSVM_FP32/` (seed 0–19). Ablation: `Vmamba_only/`, `Shape_only/` (có hướng dẫn `HUONG_DAN_KIEM_TRA_KAGGLE.md`); zip gốc ở `_zip_goc_ablation/` |
| `04_phan_tich_20seed/` | Gói phân tích cũ (đã đối chiếu khớp) và benchmark CPU |
| `05_so_sanh_mo_hinh_khac/` | `PraNet/`, `UNet/`: file `.pth` của 20 seed |
| `06_bao_cao/` | `md_bao_cao/` (các chương, bản đầy đủ 147 trang), `md_bao_cao_rut_gon/` (bản rút gọn, thân khoảng 70 trang), `ghep_word/` (script ghép Word theo Biểu mẫu V3), `hinh/` (hình kèm script `ve_hinh.py`, `ve_so_do.py`), `slide/` (kế hoạch slide), `Tien_Xu_Ly_Du_Lieu_v3.docx`, biểu mẫu V3, Word cũ |
| `07_kiem_toan_va_sua/` | Kiểm toán 25/10 và nhật ký sửa 26/10. Chỉ đọc |
| `08_du_lieu_thuc_te/` | Đánh giá trên 4 bộ dữ liệu ngoài (script, bảng, ảnh định tính) |
| `99_luu_tru/` | Lịch sử: TSVM cũ FP16, AV/AVF/ITSVM (**không đưa vào báo cáo**), tài liệu cũ, notebook PraNet/U-Net |
| `PATH_MAP.md` | Bảng tra đường dẫn cũ `archive/...` sang đường dẫn mới |

Ngoài repo:
- `..\TLTK\`: PDF tài liệu tham khảo và tệp tổng hợp nội dung.
- `..\Ung_Dung\`: ứng dụng PolypVision.
- `C:\venv_kl_gpu\`: môi trường Python có PyTorch cu130 cho GPU RTX 5050 laptop. Gọi bằng `C:\venv_kl_gpu\Scripts\python.exe`.

## 4. Trạng thái báo cáo và việc còn lại (29/10/2026)

**Hai bản báo cáo (31/10/2026).** Bản đầy đủ `md_bao_cao/` (Word/PDF `_V3_day_du`, 147 trang, tag `ban_day_du_147`) và bản rút gọn `md_bao_cao_rut_gon/` (Word/PDF `_V3_rut_gon`, 109 trang: trang đầu 15, thân 70, tài liệu tham khảo 7, phụ lục 17). Bản rút gọn giữ mọi bảng số chính, đủ 57 tài liệu đúng thứ tự, không có số liệu mới (kiểm bằng script); chi tiết Ch.3, API Ch.5, hình phụ Ch.6 chuyển xuống Phụ lục E–H; Ch.5 còn 7 khung ảnh chụp. Kế hoạch và tiến độ ở `_KIEM_TRA/J_ke_hoach_ban_rut_gon_70.md`.

**Các chương markdown** trong `06_bao_cao/md_bao_cao/` (bản đầy đủ):

| File | Trạng thái |
|---|---|
| `00_TRANG_DAU.md` | Thông tin bìa, Lời cảm ơn (bản nháp, nhóm sửa), danh mục chữ viết tắt và ký hiệu (29/10) |
| `01_MO_DAU.md` | Đã viết; phạm vi dữ liệu ngoài và đóng góp đã cập nhật. Còn các ô [ĐIỀN] ở §6 (kế hoạch, phân công) do nhóm điền sau khi ghép Word |
| `02`–`04` (Ch.1–3) | Đã viết, tài liệu tham khảo đã đánh số lại. Mục 1.6 trong nước: ColonFormer, NeoUNet, nghiên cứu YOLOv8 tại Hà Nội; ô cách đánh giá của Mamba YOLO ở Bảng 1.3 đã xác minh 30/10 |
| `05_CHUONG_4_DU_LIEU_TIEN_XU_LY.md` | Chuyển từ bản v3; đã sửa nguồn split, 640 → 672, ô cuối Hình 4.5 |
| `06_CHUONG_5_CAI_DAT_UNG_DUNG.md` | Đã viết. Còn `[CHỤP HÌNH]` chờ chụp màn hình ứng dụng, và vài ô [CẦN KIỂM TRA] (môi trường Kaggle, số ca kiểm thử tự động) |
| `07_CHUONG_6_THUC_NGHIEM_DANH_GIA.md` | Đã viết đủ 6.1–6.9, kể cả 6.6 ablation (Bảng 6.12, Hình 6.16 = k01, nhận xét) điền ngày 29/10 |
| `08_TAI_LIEU_THAM_KHAO.md` | 57 tài liệu, chuẩn IEEE. Ngày 30/10 rút gọn từ 80 (bỏ 23 mục chỉ kể tên, trùng vai trò, arXiv ít trích dẫn, trích phần mềm), có subagent kiểm tra chéo; cả 57 đều được trích, thứ tự lần trích đầu đúng 1→57. 50/57 có PDF trong `TLTK/` (`TLTK/DOI_CHIEU_57_TAI_LIEU.md`) |
| `09_KET_LUAN.md`, `10_PHU_LUC.md` | Đã viết ngày 29/10 (Kết luận trả lời CH1–CH4; Phụ lục có bảng từng seed sinh từ CSV) |
| `_KIEM_TRA/G_doi_chieu_thang_diem.md` | Đối chiếu từng tiêu chí của đề cương với mục trong báo cáo (29/10) |

**Ablation** (seed 0–4, mỗi chế độ 5 lượt). Sau đợt giải nén thứ hai (29/10), đã **đủ 15/15 lượt, mỗi lượt 100 epoch**, nằm ở `03_ket_qua_huan_luyen/{Vmamba_only, Shape_only, No_guidance}/`.

| Chế độ | Seed đủ 100 epoch | Ghi chú |
|---|---|---|
| `vmamba_only` | s0–s4 | có `weights/` |
| `shape_only` | s0–s4 | có `weights/` (bổ sung s4 ngày 29/10) |
| `shape_vmamba_no_guidance` | s0–s4 | có `weights/` |

Kết quả (seed 0–4, `bang/17_*.csv`, `scripts/tinh_ablation.py`): bản đầy đủ 0,7238 ± 0,0032; `vmamba_only` 0,7170 ± 0,0128; `shape_only` 0,7128 ± 0,0097; bỏ cổng 0,7201 ± 0,0045. Cả ba biến thể đều thấp hơn bản đầy đủ nhưng không có ý nghĩa thống kê (p = 0,22 / 0,10 / 0,08). Chỉ viết là "xu hướng". Hình k01, k02 ở `06_bao_cao/hinh/chung/`.

**Việc khác:**
- Giai đoạn C (chờ chủ dự án duyệt nội dung A, B): ghép Word theo `Bieu mau do an_khoa luan. K.CNTT_HUIT_2025_V3.docx`. Cài thêm công cụ nếu cần (pandoc, latex2mathml); có `MML2OMML.XSL` của Office để chuyển công thức.
- Hình 4.5 đã sửa ô cuối bằng cách vẽ đè (bản gốc `h4_5_ban_goc.png`). Nếu nhóm còn tệp nguồn của hình thì sửa cả ở đó.
- Chủ dự án chụp màn hình PolypVision.
- Kiểm tra Turnitin (< 30%), gửi GVHD khoảng 04–05/11.
- **Slide bảo vệ (Canva):**
  - Đã xong slide 1–3: bìa, nội dung trình bày, lý do chọn đề tài.
  - Còn khoảng 59 slide theo `06_bao_cao/slide/KE_HOACH_SLIDE.md`.
  - Cần vẽ thêm hình h05 và g01.
  - Cần hỏi giới hạn thời gian trình bày.

**Quy cách hình** (`06_bao_cao/hinh/README.md`):
- Bản `vi/` dùng dấu phẩy thập phân, kèm bản `en/`.
- Mỗi hình xuất PNG 300 dpi và PDF.
- Phông mặc định của matplotlib.
- Màu Okabe–Ito: đối chứng `#0072B2`, TSVM `#D55E00`, PraNet `#009E73`, U-Net `#CC79A7`.
- Mỗi hình một biểu đồ, tối đa hai. Không dùng biểu đồ tròn hay rada, không xếp lưới 2×2.

## 5. Quy tắc làm việc với chủ dự án (bắt buộc)

- Giao tiếp bằng **tiếng Việt**.
- Khi chủ dự án nói **"chưa chỉnh gì / đang hỏi đáp / đang thảo luận"**: chỉ trao đổi và lập kế hoạch, **không sửa file**.
- Việc lớn: trình bày kế hoạch, chờ xác nhận ("triển khai", "ok làm đi").
- Việc hàng loạt: làm mẫu trước.
- Không bịa số liệu. Mọi con số phải truy được về CSV hoặc script; khi chưa có bằng chứng thì ghi "chưa xác minh".
- Không sửa dữ liệu gốc, checkpoint hay hiện vật kiểm toán. Di chuyển thư mục thì ghi lại vào `PATH_MAP.md`.
- Chỉ commit lên nhánh `Okeydokey` khi được đồng ý. Không push nếu chưa được yêu cầu.
- Phải hỏi trước khi tải tệp hoặc chạy `kaggle kernels push`.
- Không đọc, không đưa vào git hay báo cáo:
  - token Kaggle;
  - `Ung_Dung/polypweb/GhiChu.txt` (tài khoản test).
- File đề cương PDF của trường không commit.
