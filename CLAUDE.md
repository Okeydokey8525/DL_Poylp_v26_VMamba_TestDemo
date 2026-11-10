# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Repo khóa luận (HUIT, CNTT_KLCN182, GVHD Phùng Thế Bảo): YOLO26s-seg (mô hình gốc) so với YOLO26s-seg + C2TSVMamba (TSVM FP32) cho phân đoạn polyp. Đây là repo **nghiên cứu + báo cáo**, không phải ứng dụng: không có build, lint hay bộ test.

**Trạng thái 10/11/2026:** đã dọn cho bản nộp (hạn 11/11/2026). Bản Word cuối là `06_bao_cao/CNTT_KLCN182-PhungTheBao.docx`. Thư mục dự án đổi tên từ `Test_Mau` thành `CNTT_KLCN182_PhungTheBao`. Kết quả cũ, bản nháp và ghi chú làm việc (kể cả `NGU_CANH_DU_AN.md`, `HUONG_DAN_LAM_VIEC_VOI_CLAUDE.md`, `KE_HOACH_HOAN_THIEN_NOP_BAI.md`, `06_bao_cao/md_bao_cao*/`, `06_bao_cao/slide/KE_HOACH_SLIDE.md`, `07_kiem_toan_va_sua/`, phần lớn `99_luu_tru/`) đã **chuyển** sang `..\_Luu_Tru_Ngoai\Test_Mau\` (giữ đường dẫn con), tra trong `PATH_MAP.csv`.

**Đọc trước:**
1. [README.md](README.md) và [00_tai_lieu_tong_quan/00_README.md](00_tai_lieu_tong_quan/00_README.md): kết quả và mục lục.
2. [00_tai_lieu_tong_quan/13_BAN_DO_THU_MUC.md](00_tai_lieu_tong_quan/13_BAN_DO_THU_MUC.md): thư mục nào chứa gì.
3. Ngữ cảnh làm việc cũ (nếu cần): `..\_Luu_Tru_Ngoai\Test_Mau\NGU_CANH_DU_AN.md`, `HUONG_DAN_LAM_VIEC_VOI_CLAUDE.md`.

## Quy tắc bắt buộc

- Giao tiếp bằng tiếng Việt.
- Chủ dự án nói "chưa chỉnh gì / đang hỏi đáp / đang thảo luận" → chỉ bàn và lập kế hoạch, không sửa file cho tới khi được xác nhận ("triển khai", "ok làm đi").
- Không bịa số liệu. Mọi con số phải truy được về CSV trong `00_tai_lieu_tong_quan/bang/` hoặc script sinh ra nó; chưa có bằng chứng thì ghi "chưa xác minh".
- Báo cáo dùng **20 seed (seed 0–19)**: Δ mAP50–95 = +0,0043, KTC 95% [−0,0002; 0,0088], p = 0,061, TSVM tốt hơn 13/20. **Không có ý nghĩa thống kê** ở α = 0,05: chỉ viết "xu hướng", không viết "vượt trội". SD TSVM nhỏ hơn, Levene p = 0,026 (thăm dò). Số thập phân trong báo cáo dùng dấu phẩy.
- **PraNet/U-Net trong báo cáo là bản 640×640 có tăng cường** (`bang/pixel_640/`, khóa `pranet640`/`unet640`): PraNet cao hơn TSVM ở mọi độ đo theo pixel (Dice +0,0316, p < 0,001) và về topology. Không viết "TSVM ngang/vượt PraNet". Bản 352 đã chuyển ra lưu trữ ngoài, không dùng.
- Ablation và C2PSA rộng là bản **20 seed** (`bang/ablation_20seed/`): ba biến thể không khác bản đầy đủ có ý nghĩa thống kê; C2PSA rộng thấp hơn TSVM 0,0070 (p < 0,001) và không hơn mô hình gốc.
- Không suy ra TN = 40 − FP, Dice/IoU từ mAP, hay lợi ích topology: TSVM chỉ nhích hơn mô hình gốc, không có ý nghĩa thống kê, và kém PraNet rõ rệt (`00_tai_lieu_tong_quan/14_CHI_SO_TOPOLOGY.md`).
- Không sửa dữ liệu gốc (`01_du_lieu/`), checkpoint (`03_`, `05_`) hay `99_luu_tru/`. Di chuyển thư mục thì ghi vào `PATH_MAP.md` / `PATH_MAP.csv`. Không xóa file: thứ không nộp chuyển sang `..\_Luu_Tru_Ngoai\Test_Mau\`.
- AV/AVF/ITSVM, Polyp-PVT, VM-UNet, MambaPSA không có trong báo cáo (chỉ hướng phát triển).
- Bản Word đã nộp thầy là gốc, không ghi đè. Không commit `.pt`/`.pth`/`.zip`, PDF đề cương.
- Commit lên nhánh `Okeydokey` khi được đồng ý; không push nếu chưa được yêu cầu.
- Không đọc hay đưa nội dung `..\Ung_Dung\polypweb\GhiChu.txt` (tài khoản test) và `~/.kaggle/kaggle.json` vào git hay báo cáo.

## Lệnh thường dùng

Python có GPU (PyTorch cu130) nằm ở đường dẫn ngắn vì giới hạn 260 ký tự của Windows: `C:\venv_kl_gpu\Scripts\python.exe` (lệnh `python` không có trong PATH).

```bash
# Số liệu tổng quan từ dữ liệu gốc -> 00_tai_lieu_tong_quan/bang/00–09 (chỉ đọc dữ liệu gốc)
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/tinh_lai_so_lieu.py [--torch]

# Pixel (Dice/IoU/P/R) và topology, 4 mô hình × 20 seed -> bang/pixel_640/ (cần GPU; --tu-bang chỉ tổng hợp lại)
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/danh_gia_topology.py
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/tinh_ma_tran_anh.py

# Ablation, C2PSA rộng -> bang/ablation_20seed/ ; FLOPs + độ trễ GPU -> bang/16_*
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/tinh_ablation.py --torch
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/tinh_c2psa_rong.py --torch
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/do_flops_gpu.py

# Dữ liệu khác nguồn -> bang/pixel_640/du_lieu_ngoai/, nen_cecum/
C:\venv_kl_gpu\Scripts\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_du_lieu_ngoai.py --chi-tong-hop
C:\venv_kl_gpu\Scripts\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_nen_cecum.py --chi-tong-hop

# Hình -> 06_bao_cao/hinh/{chung, ket_qua_20seed, ket_qua_20seed_640, ablation_20seed}/{vi,en}
C:\venv_kl_gpu\Scripts\python.exe 06_bao_cao/hinh/scripts/ve_hinh.py [--chi h01 p01]
C:\venv_kl_gpu\Scripts\python.exe 06_bao_cao/hinh/scripts/ve_so_do.py

# Số liệu trang /metrics của web -> ..\Ung_Dung\polypweb\polypweb\src\main\resources\research\research-metrics.json
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/xuat_chi_so_web.py
```

## Kiến trúc tổng thể

**Luồng dữ liệu:** `01_du_lieu/` (BG20: 1.040 train = 880 polyp + 160 nền, 160 val = 120 polyp + 40 nền; không có tập test) → huấn luyện trên Kaggle bằng notebook `02_ma_nguon/notebook_kaggle/` → `03_ket_qua_huan_luyen/{Baseline_YOLO26s_seg, TSVM_FP32, Vmamba_only, Shape_only, No_guidance, C2PSA_rong}/..._s{seed}_w2/` và `05_so_sanh_mo_hinh_khac/{PraNet_640, UNet_640}/` → `00_tai_lieu_tong_quan/scripts/` tính số vào `bang/` → `ve_hinh.py` vẽ hình → bản Word.

**Nguồn sự thật** là `00_tai_lieu_tong_quan/` (16 file md + `bang/`). Endpoint chính: mask mAP50–95 tại epoch cực đại của từng lượt.

**Fork Ultralytics** (`02_ma_nguon/ultralytics_TSVM_FP32/`): Ultralytics 8.4.127 + TSVM + bản vá lưu checkpoint float32. Hai mô hình chỉ khác tầng 10: `C2PSA` → `C2TSVMamba` (SS2D quét 4 hướng + nhánh hình dạng/hướng + cổng `F·(1+G)`).
- Module: `nn/modules/topology_shape_vmamba.py`; đăng ký trong `nn/tasks.py`.
- Cấu hình: `cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml` (đối chứng: `yolo26-seg.yaml`).
- Thư mục fork không tên là `ultralytics`, nên script tạo junction tên `ultralytics` trỏ tới fork trong thư mục tạm rồi chèn vào `sys.path` (`danh_gia_pixel.py`, hàm `import_fork`).

**PraNet / U-Net 640**: kiến trúc nạp từ `02_ma_nguon/notebook_kaggle/{pranet-new,unet-new}.ipynb` (cell 2).

## Báo cáo và hình

- Báo cáo cuối là file Word, không còn ghép từ markdown. Chương markdown bản V3 và công cụ `ghep_word/` ở lưu trữ ngoài.
- Slide bảo vệ làm trên Canva (thiết kế `DAHPtP9XqEY`); kế hoạch ở `..\_Luu_Tru_Ngoai\Test_Mau\06_bao_cao\slide\KE_HOACH_SLIDE.md`. Mỗi lần sửa phải cho xem trước; chủ dự án duyệt mới commit giao dịch Canva.
- Quy cách hình: `06_bao_cao/hinh/README.md`. Màu Okabe–Ito (gốc `#0072B2`, TSVM `#D55E00`, PraNet `#009E73`, U-Net `#CC79A7`); thanh lỗi ±1 SD qua 20 seed; bản `vi/` dùng dấu phẩy thập phân.
