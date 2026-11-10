# CNTT_KLCN182: Tích hợp VMamba vào YOLO26-seg để phân đoạn polyp

**Đề tài:** Nghiên cứu phương pháp tích hợp VMamba vào YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng (HUIT, mã khóa luận CNTT_KLCN182, GVHD: Phùng Thế Bảo).

**Báo cáo:** [06_bao_cao/CNTT_KLCN182-PhungTheBao.docx](06_bao_cao/CNTT_KLCN182-PhungTheBao.docx) (bản cuối). Mọi số liệu trong thư mục này khớp bản Word đó.

**Trọng tâm:** so sánh YOLO26s-seg (mô hình gốc) với YOLO26s-seg + C2TSVMamba (TSVM FP32) trên dữ liệu BG20, 20 seed (0–19) mỗi mô hình. Kèm theo: PraNet và U-Net (ảnh 640×640, có tăng cường, 20 seed) làm mốc đối chiếu; ablation ba thành phần và đối chứng C2PSA rộng (20 seed); đánh giá trên bốn bộ dữ liệu khác nguồn; ứng dụng web PolypVision.

## Bắt đầu đọc từ đây

- **[00_tai_lieu_tong_quan/00_README.md](00_tai_lieu_tong_quan/00_README.md):** tóm tắt một trang và mục lục 15 file tổng quan. Mọi con số trong đó được tính lại từ dữ liệu gốc bằng script trong `00_tai_lieu_tong_quan/scripts/`.
- **[00_tai_lieu_tong_quan/13_BAN_DO_THU_MUC.md](00_tai_lieu_tong_quan/13_BAN_DO_THU_MUC.md):** thư mục nào chứa gì.

## Kết quả chính (20 seed)

| | YOLO26s-seg | + TSVM FP32 |
|---|---:|---:|
| Mask mAP50–95 | 0,7189 ± 0,0118 | 0,7232 ± 0,0072 |
| Δ, p | | +0,0043, KTC 95% [−0,0002; 0,0088], paired t p = 0,061, 13/20 seed (**chỉ là xu hướng**, không có ý nghĩa thống kê ở α = 0,05) |
| Dice theo pixel | 0,8486 | 0,8540 (p = 0,26) |
| Tham số | 11,43 M | 12,25 M |
| Độ trễ CPU (chỉ forward) | 270 ms | 577 ms |
| Độ trễ GPU (forward) | 26,33 ms | 39,86 ms |

- **Ablation 20 seed:** ba biến thể bỏ bớt thành phần đều thấp hơn bản đầy đủ nhưng không có ý nghĩa thống kê. **C2PSA rộng** (cùng số tham số) thấp hơn TSVM 0,0070 (KTC 95% [0,0038; 0,0101], 17/20 seed) và không hơn mô hình gốc.
- **PraNet 640** cao hơn cả hai mô hình YOLO ở mọi độ đo theo pixel (Dice 0,8856; hơn TSVM 0,0316, p < 0,001). U-Net 640 thấp nhất (Dice 0,6909).
- **Dữ liệu khác nguồn:** TSVM không tốt hơn mô hình gốc về Dice: thấp hơn có ý nghĩa thống kê trên CVC-ClinicDB và CVC-ColonDB, ngang nhau trên ETIS-Larib và PolypGen. Trên ảnh không có polyp của PolypGen, TSVM báo nhầm ít hơn (10,8% so với 13,3%; p = 0,011). Chi tiết ở [08_du_lieu_thuc_te/](08_du_lieu_thuc_te/README.md).

## Cây thư mục

| Thư mục | Nội dung |
|---|---|
| [00_tai_lieu_tong_quan/](00_tai_lieu_tong_quan/00_README.md) | Tài liệu tổng quan, script tính lại số liệu, bảng kết quả (`bang/`) |
| `01_du_lieu/` | Dữ liệu BG20 (1.200 ảnh), split 880/120 do tác giả Kvasir-SEG cung cấp, script tạo dữ liệu |
| `02_ma_nguon/` | Fork Ultralytics 8.4.127 + TSVM + bản vá FP32, fork C2PSA rộng, notebook Kaggle |
| `03_ket_qua_huan_luyen/` | Mô hình gốc, TSVM FP32, ba biến thể ablation, C2PSA rộng (mỗi loại seed 0–19) |
| `04_phan_tich_20seed/` | Số liệu trích từ 40 lượt của hai mô hình chính (đối chiếu với bảng ở `bang/`), ma trận nhầm lẫn và benchmark độ trễ CPU |
| `05_so_sanh_mo_hinh_khac/` | PraNet 640, U-Net 640 (20 seed mỗi mô hình) |
| `06_bao_cao/` | Bản Word cuối, hình (`hinh/`) |
| `08_du_lieu_thuc_te/` | Đánh giá trên CVC-ClinicDB, CVC-ColonDB, ETIS-Larib, PolypGen và 800 ảnh manh tràng |

Thư mục chỉ chứa các mô hình và kết quả có trong bản Word cuối.

Repo GitHub không chứa checkpoint (`best.pt`, `*_best_*.pth` của 160 lượt huấn luyện, khoảng 7,9 GB) vì vượt giới hạn dung lượng của GitHub. Bản đầy đủ có checkpoint nằm trong bản nộp gửi GVHD.

## Chạy ứng dụng web PolypVision

Ứng dụng nằm ở repo riêng, cạnh thư mục này: `..\Ung_Dung\polypweb\` (GitHub: <https://github.com/Okeydokey8525/UngDung_Poylp>). Gồm hai phần chạy song song:

| Phần | Thư mục | Cổng | Vai trò |
|---|---|---|---|
| AI service (FastAPI, Python) | `..\Ung_Dung\polypweb\polypweb\ai-service\` | 8000 | Nạp hai mô hình, nhận ảnh hoặc video, trả mặt nạ phân đoạn |
| Web (Spring Boot, Java) | `..\Ung_Dung\polypweb\polypweb\` | 8080 | Giao diện, tài khoản, lịch sử; lưu dữ liệu vào MongoDB |

### Cần cài sẵn

- Java 17 (Maven đã có sẵn qua `mvnw.cmd`, không cần cài).
- Python 3.12.
- MongoDB chạy ở `mongodb://localhost:27017` (cài dạng Windows service thì tự chạy khi bật máy).
- GPU không bắt buộc; chạy CPU vẫn được nhưng chậm hơn.

### Trọng số mô hình

Web dùng `best.pt` của **seed 15** cho cả hai mô hình (seed có chênh lệch mAP50–95 gần trung vị 20 seed nhất). Hai file đã có sẵn trong `ai-service\models\`:

| File trong `models\` | Lấy từ |
|---|---|
| `yolo26s-seg-best.pt` | `03_ket_qua_huan_luyen/Baseline_YOLO26s_seg/Kvasir_BG20_Baseline_YOLO26s_seg_s15_w2/weights/best.pt` |
| `yolo26s-tsvm-fp32-best.pt` | `03_ket_qua_huan_luyen/TSVM_FP32/Kvasir_BG20_YOLO26s_seg_TSVM_FP32_s15_w2/weights/best.pt` |

Nếu thiếu thì chép lại từ hai đường dẫn trên và đổi tên cho đúng. Mã băm để đối chiếu nằm trong `models\experiment_manifest.json`.

### Bước 1: chạy AI service (cửa sổ PowerShell thứ nhất)

Có hai môi trường Python, chọn một:

| Môi trường | Đường dẫn | Chạy trên |
|---|---|---|
| **GPU (khuyến nghị, máy này đã cài sẵn)** | `C:\venv_polyp_ai` | GPU NVIDIA (PyTorch 2.13 + CUDA 13.0) |
| CPU | `ai-service\.venv` | CPU (PyTorch 2.6 bản CPU) |

Môi trường GPU phải đặt ở đường dẫn ngắn `C:\venv_polyp_ai`: gói PyTorch CUDA có tên file rất dài, cài vào `ai-service\.venv` sẽ vượt giới hạn 260 ký tự của Windows và báo lỗi `WinError 206`.

Lần đầu trên máy khác, tạo môi trường GPU (cần Python 3.12):

```powershell
cd "..\Ung_Dung\polypweb\polypweb\ai-service"
python -m venv C:\venv_polyp_ai
C:\venv_polyp_ai\Scripts\python.exe -m pip install --upgrade pip
C:\venv_polyp_ai\Scripts\python.exe -m pip install -r requirements-gpu.txt
C:\venv_polyp_ai\Scripts\python.exe -m pip install fastapi==0.139.2 uvicorn==0.51.0 python-multipart==0.0.32 numpy==2.2.6 pillow==11.3.0 opencv-python==4.12.0.88 ultralytics==8.4.127
```

Máy không có GPU thì tạo `.venv` và cài `requirements.txt` như cũ.

Các lần sau chỉ cần chạy:

```powershell
cd "..\Ung_Dung\polypweb\polypweb\ai-service"
C:\venv_polyp_ai\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Chạy bằng CPU thì thay `C:\venv_polyp_ai\Scripts\python.exe` bằng `.\.venv\Scripts\python.exe`.

Kiểm tra: mở <http://127.0.0.1:8000/health>, cả hai mô hình phải ở trạng thái sẵn sàng. Trường `device` cho biết đang chạy `cuda:0` (GPU) hay `cpu`.

### Bước 2: chạy web (cửa sổ PowerShell thứ hai)

```powershell
cd "..\Ung_Dung\polypweb\polypweb"
$env:SPRING_PROFILES_ACTIVE="dev"
.\mvnw.cmd spring-boot:run
```

Mở <http://localhost:8080>. Lần đầu bấm **Đăng ký** để tạo tài khoản, rồi đăng nhập.

### Các chức năng chính

| Trang | Chức năng |
|---|---|
| Chẩn đoán | Tải một ảnh nội soi, chọn mô hình, xem mặt nạ polyp. Có thể kèm mặt nạ thật (ground truth) để tính Dice, IoU, Precision, Recall |
| So sánh | Chạy cùng một ảnh qua cả hai mô hình, đặt kết quả cạnh nhau |
| Video | Tải video nội soi, chọn phân tích 2, 5, 10 khung/giây hoặc tất cả khung (cần GPU). Video kết quả giữ đủ khung và tốc độ của video gốc; khung không được phân tích dùng lại mặt nạ của khung phân tích gần nhất. Kèm dòng thời gian và các đoạn có polyp |
| Video, chế độ mô phỏng thời gian thực | Phát lại video đã quay đúng tốc độ gốc, mặt nạ hiện ngay trên từng khung, kèm tốc độ so với thời gian thực và đèn báo polyp; phát xong tự lưu vào lịch sử. Là mô phỏng, chưa phải hệ thống gắn vào máy nội soi |
| Lịch sử | Xem lại, xóa các lần phân tích ảnh và so sánh |
| Chỉ số (`/metrics`, không cần đăng nhập) | Kết quả 20 seed của hai mô hình và mốc PraNet/U-Net 640, đọc từ bảng CSV trong `00_tai_lieu_tong_quan/bang/` (qua file JSON xuất sẵn) |

Ảnh và video được lưu trong `..\Ung_Dung\polypweb\polypweb\storage\`; MongoDB chỉ lưu chỉ số và đường dẫn file.

### Cập nhật số liệu trang Chỉ số

Khi bảng CSV trong `00_tai_lieu_tong_quan/bang/` thay đổi, chạy lại script dưới đây rồi khởi động lại web:

```powershell
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/xuat_chi_so_web.py
```

Script ghi đè `..\Ung_Dung\polypweb\polypweb\src\main\resources\research\research-metrics.json`.

### Lỗi thường gặp

| Hiện tượng | Cách xử lý |
|---|---|
| Web báo không kết nối được AI service | Chạy bước 1 trước, kiểm tra cổng 8000 |
| Web không khởi động, lỗi MongoDB | Bật MongoDB (`services.msc` → MongoDB Server → Start) |
| AI service báo không tìm thấy checkpoint | Chép lại hai file `.pt` vào `ai-service\models\` theo bảng ở trên |
| `/health` báo `device: cpu` dù máy có GPU | Đang chạy bằng `.venv` (bản CPU); chạy lại bằng `C:\venv_polyp_ai\Scripts\python.exe` |
| Chọn "Tất cả khung" bị báo cần GPU | Như dòng trên |
| Cổng 8080 hoặc 8000 đã bị chiếm | Tắt cửa sổ đang chạy bản cũ rồi chạy lại |

Hướng dẫn đầy đủ (biến môi trường, chạy production, ứng dụng Android): `..\Ung_Dung\polypweb\README.md` và `..\Ung_Dung\polypweb\polypweb\README.md`.

## Lưu ý

Dự án phục vụ học tập và nghiên cứu. Kết quả phân đoạn không thay thế chẩn đoán y khoa.
