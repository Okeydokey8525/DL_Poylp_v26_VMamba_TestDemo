# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Repo khóa luận (HUIT, CNTT_KLCN182): YOLO26s-seg (Baseline) so với YOLO26s-seg + C2TSVMamba (TSVM FP32) cho phân đoạn polyp. Đây là repo **nghiên cứu + báo cáo**, không phải ứng dụng: không có build, lint hay bộ test. Việc thường làm là tính lại số liệu, vẽ hình và viết các chương báo cáo markdown.

**Đọc trước:** [NGU_CANH_DU_AN.md](NGU_CANH_DU_AN.md) (ngữ cảnh, kết quả đã xác minh, kế hoạch đang làm, quy tắc làm việc), sau đó [00_tai_lieu_tong_quan/00_README.md](00_tai_lieu_tong_quan/00_README.md).

## Quy tắc bắt buộc

- Giao tiếp bằng tiếng Việt.
- Chủ dự án nói "chưa chỉnh gì / đang hỏi đáp / đang thảo luận" → chỉ bàn và lập kế hoạch, không sửa file cho tới khi được xác nhận ("triển khai", "ok làm đi").
- Không bịa số liệu. Mọi con số phải truy được về CSV trong `00_tai_lieu_tong_quan/bang/` hoặc script sinh ra nó; chưa có bằng chứng thì ghi "chưa xác minh".
- Báo cáo dùng **20 seed (seed 0–19)** (chốt 28/10/2026): Δ mAP50–95 = +0,0043, CI 95% [−0,0002; 0,0088], p = 0,061, TSVM tốt hơn 13/20. **Không có ý nghĩa thống kê** ở α = 0,05: chỉ viết "xu hướng", không viết "vượt trội". Riêng độ ổn định: SD TSVM nhỏ hơn, Levene p = 0,026 (thăm dò). Bộ 10 seed (`bang/10seed/`, `hinh/ket_qua_10seed/`) chỉ giữ để đối chiếu. Số thập phân trong báo cáo dùng dấu phẩy. Không suy ra TN = 40 − FP, Dice/IoU từ mAP, hay lợi ích topology khi chưa có chỉ số topology và ablation.
- Không sửa dữ liệu gốc (`01_du_lieu/`), checkpoint (`03_`, `05_`), hiện vật kiểm toán (`07_kiem_toan_va_sua/`) hay `99_luu_tru/`. Di chuyển thư mục thì ghi vào `PATH_MAP.md` / `PATH_MAP.csv`.
- AV/AVF/ITSVM (trong `99_luu_tru/thu_nghiem_ket_hop/`) chỉ là thử nghiệm, không đưa vào báo cáo.
- Commit lên nhánh `Okeydokey` khi được đồng ý; không push nếu chưa được yêu cầu.
- Không đưa nội dung `..\Ung_Dung\polypweb\GhiChu.txt` (tài khoản test) vào git hay báo cáo.

## Lệnh thường dùng

Python có GPU (PyTorch cu130) nằm ở đường dẫn ngắn vì giới hạn 260 ký tự của Windows: `C:\venv_kl_gpu\Scripts\python.exe`.

```bash
# Tính lại mọi số liệu tổng quan từ dữ liệu gốc -> 00_tai_lieu_tong_quan/bang/*.csv (chỉ đọc)
python 00_tai_lieu_tong_quan/scripts/tinh_lai_so_lieu.py
python 00_tai_lieu_tong_quan/scripts/tinh_lai_so_lieu.py --torch   # thêm kiểm tra checkpoint, dựng lại mô hình

# Đánh giá theo pixel (Dice/IoU/P/R) 4 mô hình × 20 seed -> bang/10–12_*.csv (cần GPU)
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py --seeds 0 1 --models pranet unet

# Bảng 10 seed (chỉ đối chiếu) -> 00_tai_lieu_tong_quan/bang/10seed/
python 00_tai_lieu_tong_quan/scripts/tinh_lai_so_lieu.py --seeds 10
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py --tu-bang --seeds 0 1 2 3 4 5 6 7 8 9 --out 00_tai_lieu_tong_quan/bang/10seed

# Vẽ hình -> 06_bao_cao/hinh/chung/ (không phụ thuộc seed) và hinh/ket_qua_20seed/ (PNG 300 dpi + PDF, vi/ và en/)
python 06_bao_cao/hinh/scripts/ve_hinh.py             # tất cả, kết quả 20 seed (--seeds 10: ghi vào ket_qua_10seed/, chỉ đối chiếu)
python 06_bao_cao/hinh/scripts/ve_hinh.py --chi h01 r01   # chỉ một số mã hình
python 06_bao_cao/hinh/scripts/ve_so_do.py --chi ...      # sơ đồ kiến trúc
```

Benchmark hiệu năng CPU: `04_phan_tich_20seed/efficiency_benchmark/scripts/` (`run_both.py`, `measure.py`, `summarize.py`), xem README cùng thư mục.

## Kiến trúc tổng thể

**Luồng dữ liệu:** `01_du_lieu/` (BG20: 1.040 train = 880 polyp + 160 nền, 160 val = 120 polyp + 40 nền; không có tập test) → huấn luyện trên Kaggle bằng notebook `02_ma_nguon/notebook_kaggle/` → 40 lượt chạy ở `03_ket_qua_huan_luyen/{Baseline_YOLO26s_seg,TSVM_FP32}/..._s{seed}_w2/` (`args.yaml`, `results.csv`, `weights/best.pt`) → `00_tai_lieu_tong_quan/scripts/` tính lại số liệu vào `bang/` → `ve_hinh.py` đọc `bang/` để vẽ → các chương trong `06_bao_cao/md_bao_cao/`.

**Nguồn sự thật** là `00_tai_lieu_tong_quan/` (14 file md + `bang/*.csv`). `04_phan_tich_20seed/` là gói phân tích cũ hơn, đã đối chiếu khớp. Endpoint chính: mask mAP50–95 tại epoch cực đại của từng lượt.

**Fork Ultralytics** (`02_ma_nguon/ultralytics_TSVM_FP32/`): Ultralytics 8.4.127 + TSVM + bản vá lưu checkpoint float32 (fork cũ lưu FP16 làm tràn BatchNorm tầng 10). Hai mô hình chỉ khác tầng 10: `C2PSA` → `C2TSVMamba` (SS2D quét 4 hướng + nhánh hình dạng/hướng + cổng `F·(1+G)`).
- Module: `nn/modules/topology_shape_vmamba.py`; đăng ký trong `nn/tasks.py` (`C2TSVMamba`, `TSVMamba`).
- Cấu hình mô hình: `cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml` (đối chứng: `yolo26-seg.yaml`).
- Thư mục fork không tên là `ultralytics`, nên script tạo junction/symlink tên `ultralytics` trỏ tới fork trong thư mục tạm rồi chèn vào `sys.path` (xem `danh_gia_pixel.py`, khoảng dòng 100–116) và assert đã import đúng fork. Dùng lại cách này khi cần nạp checkpoint TSVM.

**PraNet / U-Net** (`05_so_sanh_mo_hinh_khac/`): chỉ có `.pth`; kiến trúc được nạp trực tiếp từ notebook huấn luyện trong `99_luu_tru/log_kaggle_cu/*.ipynb`.

**Đường dẫn cũ:** script và tài liệu trong `07_`, `99_luu_tru/`, `04_.../scripts/`, `06_bao_cao/luu_tru_cu/` còn ghi `archive/...`. Khi chạy lại, đổi tiền tố theo `PATH_MAP.md` (khớp tiền tố dài nhất trước); không sửa các file đó.

## Báo cáo và hình

- Chương báo cáo: một file markdown mỗi chương trong `06_bao_cao/md_bao_cao/`; ghi chú điều tra/phản biện trong `_KIEM_TRA/`. Viết mới (Turnitin < 30%), không chép từ md/Word cũ. Ch.4 giữ nguyên nội dung `Tien_Xu_Ly_Du_Lieu.docx` (chỉ đổi số 3.x → 4.x). Tài liệu tham khảo kiểu IEEE.
- Quy cách hình (chi tiết và danh mục mã hình ở `06_bao_cao/hinh/README.md`): phông mặc định matplotlib; màu Okabe–Ito (đối chứng `#0072B2`, TSVM `#D55E00`, PraNet `#009E73`, U-Net `#CC79A7`); mỗi hình một biểu đồ, tối đa hai; không biểu đồ tròn/rada; không lưới 2×2; điểm từng seed vẽ thành hình riêng; thanh lỗi ±1 SD qua các seed (20 seed); bản `vi/` dùng dấu phẩy thập phân.
