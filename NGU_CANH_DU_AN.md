# Ngữ cảnh dự án (dành cho AI/người mới tiếp nhận)

Cập nhật: 26/10/2026. Đọc file này trước, sau đó đọc [README.md](README.md) và [00_tai_lieu_tong_quan/00_README.md](00_tai_lieu_tong_quan/00_README.md).

## 1. Dự án là gì

**Khóa luận tốt nghiệp cử nhân CNTT, Trường ĐH Công Thương TP.HCM (HUIT), mã CNTT_KLCN182, sinh viên Lê Đức Lương.**

Đề tài: *Nghiên cứu phương pháp tích hợp VMamba vào YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng.*

- Bài toán: phân đoạn thực thể (instance segmentation) một lớp `polyp` trên ảnh nội soi.
- Mô hình đối chứng: **YOLO26s-seg** (Ultralytics 8.4.127).
- Mô hình đề xuất: **YOLO26s-seg + C2TSVMamba (TSVM FP32)**. Tầng 10 (`C2PSA`, mức P5, bản đồ đặc trưng 20×20) được thay bằng khối VMamba có quét chọn lọc 4 hướng (SS2D), nhánh hình dạng, nhánh hướng và cổng điều biến `F·(1+G)`.
- "FP32" chỉ có nghĩa là **checkpoint được lưu ở float32**. Fork cũ lưu float16 làm tràn số BatchNorm tầng 10. Cả hai mô hình đều huấn luyện với `amp=False`.
- Mô hình so sánh thêm: **PraNet** (biến thể backbone ResNet-50) và **U-Net** (32 kênh), mỗi mô hình 20 seed.
- Ứng dụng minh họa **PolypVision**: Web Spring Boot, ai-service FastAPI và app Flutter, nằm ở thư mục ngoài repo `C:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Ung_Dung\polypweb\`.

## 2. Thiết kế thực nghiệm và kết quả chính (đã xác minh)

- **Dữ liệu BG20:** 1.200 ảnh.
  - Train 1.040 = 880 ảnh polyp + 160 ảnh nền.
  - Validation 160 = 120 ảnh polyp + 40 ảnh nền, có 127 đối tượng polyp.
  - Ảnh nền lấy từ normal-cecum (Kvasir v2), chọn bằng seed 42.
  - **Không có tập test riêng.**
- **Huấn luyện:** 2 mô hình × 20 seed (0–19) × 100 epoch trên Kaggle. Cấu hình: imgsz 640, batch 8, AdamW, lr0 0,001, close_mosaic 10, `deterministic=True`. Hai mô hình chỉ khác nhau ở tầng 10.
- **Endpoint chính:** mask mAP50–95, lấy tại epoch đạt cực đại của từng lượt.
- **Báo cáo dùng 20 seed (seed 0–19), chốt ngày 28/10/2026.** Thay cho quyết định tạm 10 seed ngày 27/10. Bộ 10 seed giữ lại để đối chiếu (`00_tai_lieu_tong_quan/06b_KET_QUA_10_SEED.md`). Số thập phân trong báo cáo dùng dấu phẩy; có bổ sung chỉ số topology (lỗi Betti).

| 10 seed (đối chiếu) | Baseline | TSVM FP32 |
|---|---:|---:|
| Mask mAP50–95 | 0,7210 ± 0,0129 | 0,7246 ± 0,0078 |
| Δ, CI 95%, p | | +0,0036, [−0,0052; 0,0123], paired t p = 0,384 (Wilcoxon 0,432) |
| Số seed TSVM cao hơn | | 6/10 |
| Mask mAP50 | 0,9119 | 0,9062 (TSVM thấp hơn, p = 0,227) |

| **20 seed (dùng trong báo cáo)** | Baseline | TSVM FP32 |
|---|---:|---:|
| Mask mAP50–95 | 0,718868 ± 0,011768 | 0,723171 ± 0,007197 |
| Δ, CI 95%, p | | +0,004303, [−0,000228; 0,008834], paired t p = 0,061431 (Wilcoxon 0,0696) |
| Số seed TSVM cao hơn | | 13/20 |
| Tham số | 11.434.463 | 12.254.688 (+7,17%) |
| Độ trễ CPU (forward) | 269,6 ms | 577,4 ms (khoảng 2,1 lần) |

→ **Chưa đạt ý nghĩa thống kê ở α = 0,05.** Không được viết là "vượt trội".

**Đã kiểm chứng:**
- 40 file `results.csv` gốc khớp 100% với gói phân tích 20 seed.
- Ma trận nhầm lẫn (TP/FP/FN) khớp 40/40 với ảnh gốc.
- Kiến trúc dựng lại có số tham số trùng với checkpoint.

**Không được suy diễn:**
- TN = 40 − FP (không hợp lệ).
- Dice/IoU từ mAP.
- Lợi ích về topology (chưa có chỉ số topology, chưa có ablation).
- `val/sem_loss = 0` chỉ là giá trị ghi log, không có nghĩa là lỗi bằng 0.

## 3. Cây thư mục (`Test_Mau/`, git, nhánh `Okeydokey`)

| Thư mục | Nội dung |
|---|---|
| `00_tai_lieu_tong_quan/` | **Nguồn sự thật**: 14 file md tổng quan, `scripts/tinh_lai_so_lieu.py` (chỉ đọc dữ liệu, tính lại mọi con số), `bang/*.csv` |
| `01_du_lieu/` | `Kvasir_YOLO_SEG_BG20/` (dữ liệu sạch), `train.txt`/`val.txt` (split 880/120), `tao_BG20/` (dữ liệu thô), `scripts_tien_xu_ly/convert_kvasir_with_background_to_yolo_seg.py` (script tiền xử lý duy nhất) |
| `02_ma_nguon/` | `ultralytics_TSVM_FP32/` (fork: Ultralytics 8.4.127 + TSVM + bản vá FP32; module ở `nn/modules/topology_shape_vmamba.py`), `notebook_kaggle/` |
| `03_ket_qua_huan_luyen/` | 40 lượt chính: `Baseline_YOLO26s_seg/` và `TSVM_FP32/`, seed 0–19 (`args.yaml`, `results.csv`, `weights/best.pt`) |
| `04_phan_tich_20seed/` | Gói phân tích thống kê 20 seed (CSV, báo cáo, benchmark hiệu năng) |
| `05_so_sanh_mo_hinh_khac/` | `PraNet/`, `UNet/`: chỉ có file `.pth` (20 seed mỗi mô hình) |
| `06_bao_cao/` | File Word khóa luận, `Tien_Xu_Ly_Du_Lieu.docx` (chương dữ liệu do bạn cùng nhóm viết), `md_bao_cao/` (đang trống, sẽ viết), `hinh/` (bộ hình mới) |
| `07_kiem_toan_va_sua/` | Kiểm toán ngày 25/10 và nhật ký sửa ngày 26/10 (bằng chứng, không sửa) |
| `99_luu_tru/` | Lịch sử: TSVM cũ (checkpoint FP16), AV/AVF/ITSVM (thử nghiệm, **không đưa vào báo cáo**), bộ 10 seed, tài liệu cũ, hình cũ, notebook PraNet/U-Net (`log_kaggle_cu/*.ipynb`) |
| `PATH_MAP.md` | Bảng tra đường dẫn cũ `archive/...` sang đường dẫn mới |

Ngoài repo:
- `..\TLTK\`: 24 tài liệu tham khảo PDF kèm MANIFEST.
- `..\Ung_Dung\`: ứng dụng PolypVision.
- `C:\venv_kl_gpu\`: Python có PyTorch 2.13.0+cu130 cho GPU RTX 5050. Đặt ở đường dẫn ngắn vì Windows giới hạn đường dẫn 260 ký tự, cài sâu trong `DeepLearning\` sẽ lỗi. Dùng: `C:\venv_kl_gpu\Scripts\python.exe`.

## 4. Việc đang làm (kế hoạch đã thống nhất với chủ dự án)

Mục tiêu: viết lại báo cáo khóa luận dạng **markdown, mỗi chương một file** trong `06_bao_cao/md_bao_cao/`. Khoảng 80 trang trở lên, đầy đủ và cụ thể. Viết mới, không chép từ md hay Word cũ. Turnitin của trường yêu cầu trùng lặp **dưới 30%**.

**Bố cục:**
- Mở đầu.
- Ch.1 Tổng quan.
- Ch.2 Cơ sở lý thuyết.
- Ch.3 Mô hình đề xuất.
- Ch.4 Dữ liệu và tiền xử lý: **giữ nguyên nội dung** `Tien_Xu_Ly_Du_Lieu.docx`, chỉ đổi số 3.x thành 4.x; góp ý ghi riêng.
- Ch.5 Cài đặt và ứng dụng: soạn từ mã nguồn, để chỗ ghi chú `[CHÈN HÌNH]` cho chủ dự án tự chụp.
- Ch.6 Thực nghiệm và đánh giá.
- Kết luận, Tài liệu tham khảo (IEEE), Phụ lục, trang đầu.

**Thứ tự triển khai:**
1. Vẽ lại toàn bộ hình từ CSV. **4 hình mẫu đã được duyệt.**
2. Chạy đánh giá theo pixel (Dice, IoU, Precision, Recall) cho cả 4 mô hình × 20 seed trên 160 ảnh validation, bằng GPU. Giao thức:
   - Nhãn chuẩn là mặt nạ vẽ từ polygon ở độ phân giải gốc.
   - Ngưỡng 0,5 cho PraNet/U-Net; YOLO dùng conf 0,25 rồi gộp mặt nạ.
   - Chỉ số tính trên 120 ảnh polyp; 40 ảnh nền tính tỉ lệ báo nhầm.
3. Điều tra bằng 4 sub-agent chạy song song: dữ liệu, lý thuyết/mô hình, ứng dụng, tài liệu tham khảo (được phép tra web).
4. Viết từng chương. Mỗi chương có sub-agent phản biện kiểm tra số liệu và trích dẫn.
5. Kiểm tra cuối: đối chiếu sự thật và tự đo mức trùng lặp.

**Quy cách hình** (`06_bao_cao/hinh/`, script `scripts/ve_hinh.py`):
- Hai bản riêng: `vi/` (khóa luận, rộng 16 cm, dấu phẩy thập phân) và `en/` (IEEE một cột 8,9 cm).
- Mỗi hình có PNG 300 dpi và PDF vector.
- **Phông mặc định của matplotlib** (không dùng Times New Roman trong hình; Times New Roman chỉ dùng cho Word).
- Màu Okabe–Ito: đối chứng `#0072B2`, TSVM `#D55E00`.
- Mỗi hình **một biểu đồ**, tối đa hai (một biểu đồ cho mỗi mô hình), không làm lưới 2×2.
- Không dùng biểu đồ tròn hay rada.
- Điểm từng seed vẽ thành hình riêng, không chồng lên biểu đồ cột.

## 5. Quy tắc làm việc với chủ dự án (bắt buộc)

- Khi chủ dự án nói **"chưa chỉnh gì / đang hỏi đáp / đang thảo luận"**: chỉ trao đổi và lập kế hoạch, **không sửa file**. Chỉ thực hiện khi được xác nhận rõ ràng ("triển khai", "ok làm đi").
- Giao tiếp bằng **tiếng Việt**.
- Không bịa số liệu. Mọi con số phải truy được về CSV hoặc script. Khi chưa có bằng chứng thì ghi "chưa xác minh".
- Không sửa dữ liệu gốc, checkpoint hay hiện vật kiểm toán. Di chuyển thư mục thì ghi lại vào `PATH_MAP.md`.
- Commit lên nhánh `Okeydokey` khi chủ dự án đồng ý. Không push nếu chưa được yêu cầu.
- `Ung_Dung/polypweb/GhiChu.txt` có tài khoản test kèm mật khẩu: không đưa vào git hay vào báo cáo.
