# Kế hoạch: nhận xét II.4, đánh giá lại PraNet và U-Net bản 640 (phương án B)

Ngày 09/11/2026. Yêu cầu của Huy: chạy trên máy Lương, nhánh `Okeydokey`. **Chỉ suy luận, không huấn luyện lại.** Chỉ gửi số, không sửa Word và không viết nhận xét vào báo cáo (phần đó Huy làm).

## 1. Có ảnh hưởng đến kế hoạch cũ không?

**Cùng hướng với kế hoạch cũ:** yêu cầu này chính là bước A3 và A4 trong `KE_HOACH_HOAN_THIEN_NOP_BAI.md`, cộng thêm phần dữ liệu ngoài. Tuy vậy có **4 điểm phải sửa** trong kế hoạch cũ:

| # | Kế hoạch cũ | Theo yêu cầu của Huy | Sửa thành |
|---|---|---|---|
| 1 | Chuyển bảng 352 cũ sang `bang/ban_352_cu/` rồi ghi bảng 640 đè lên `bang/10–12_*.csv` | **Không ghi đè** `bang/10–12_*.csv` (Word đang dùng). Ghi vào thư mục riêng `bang/pixel_640/` | Ghi vào `bang/pixel_640/`; bảng cũ để nguyên chỗ |
| 2 | Thay khóa `pranet`/`unet` bằng bản 640 | **Giữ nguyên** `pranet`/`unet` (352), thêm khóa mới `pranet640`/`unet640` | Thêm khóa mới, không đổi khóa cũ |
| 3 | Phần C: chuyển `05_/PraNet`, `05_/UNet` (352) và `99_luu_tru/log_kaggle_cu` ra `_Luu_Tru_Ngoai` | Số 352 cũ **phải tái lập được**, nên khóa `pranet`/`unet` phải chạy được | **Giữ** `05_/PraNet`, `05_/UNet` và `99_luu_tru/log_kaggle_cu/` trong bộ nộp |
| 4 | Phần D: tự viết bản báo cáo cuối bằng markdown | Huy sửa Word; Lương chỉ gửi số | Cần thống nhất với Huy để không làm trùng (xem mục 7) |

Các bước A1, A2, A5, A6, A7 và phần C còn lại của kế hoạch cũ không bị ảnh hưởng, làm sau phần II.4.

## 2. Đã kiểm tra trước khi làm

- **Checkpoint:** đủ 40 file, tên và đường dẫn đúng như Huy ghi. Cả 40 khớp zip gốc Kaggle và `tom_tat.txt` ở `aba071e0` (chi tiết trong `05_so_sanh_mo_hinh_khac/PHAN_HOI_CHECKPOINT_640.md`).
- **Notebook mới** `02_ma_nguon/notebook_kaggle/{pranet,unet}-new.ipynb` có 5 cell. Các lớp mạng (`PraNet`, `RFB`, … và `UNet`, `DoubleConv`) nằm ở **cell 2**, không phải cell 1 như notebook cũ. Cell 2 không có phần siêu tham số, nên không cần cắt như bản cũ; chỉ cắt trước dòng `# 5. HÀM LOSS` (PraNet) và `# 4. HÀM LOSS` (U-Net).
- **Tiền xử lý trong notebook 640:**
  - đọc BGR rồi đổi sang RGB;
  - kéo thẳng về 640×640 (`cv2.resize`, `INTER_LINEAR`, không letterbox);
  - chia 255;
  - PraNet thêm chuẩn hóa ImageNet (`CHUAN_HOA = "imagenet"`), U-Net chỉ chia 255 (`"chia255"`).
  - Khi chọn checkpoint, PraNet lấy **đầu ra thứ nhất** (`logits, _, _, _ = model(imgs)`).
  - Tất cả khớp mô tả của Huy.
- **Script hiện có:**
  - `danh_gia_pixel.py` đã có `--out`, `--models`, `--seeds`, nhưng kích thước 352 đang cố định trong `predict_semantic` và `notebook_classes()` chỉ đọc notebook cũ.
  - `danh_gia_topology.py` **chưa có `--out`**.
  - `danh_gia_du_lieu_ngoai.py` ghi từng lượt vào `08_/bang/tung_luot/` (tên file theo khóa mô hình nên chỉ thêm file mới, không đè). Phần tổng hợp hiện ghi vào `08_/bang/10seed/` và `20seed/`, nên **cần thêm `--out`**.

## 3. Các bước

### Bước 1: sửa `00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py`
1. Thêm `NB_640 = REPO / "02_ma_nguon" / "notebook_kaggle"` và 2 khóa mới vào `MODELS`:
   - `pranet640` → `05_so_sanh_mo_hinh_khac/PraNet_640/PraNet_640_aug_s{s}/pranet_best_s{s}.pth`
   - `unet640` → `05_so_sanh_mo_hinh_khac/UNet_640/UNet_640_aug_s{s}/best_unet_s{s}.pth`
2. Thêm bảng kích thước ảnh theo mô hình: `pranet`/`unet` dùng 352, `pranet640`/`unet640` dùng 640. Bỏ số 352 cố định trong `predict_semantic`.
3. `notebook_classes()`: bản 352 giữ nguyên (notebook cũ, cell 1); bản 640 đọc notebook mới, cell 2. Mỗi notebook mới chạy trong namespace riêng.
4. Chuẩn hóa xác định theo họ mô hình: `pranet*` dùng ImageNet, `unet*` chia 255.
5. Nạp checkpoint bằng `load_state_dict(..., strict=True)`. **Nếu lệch khóa thì dừng và báo Huy, không tắt `strict`.**
6. Thêm `--out` cho phần ghi ảnh định tính (nếu có), để bản 640 không ghi đè vào `06_bao_cao/hinh/du_lieu_dinh_tinh/`.
7. **Kiểm tra trước khi chạy đủ:** chạy thử `pranet640` và `unet640` với seed 0. Dice trung bình phải gần mức `best_val_dice` trong `tom_tat.txt` (PraNet 0,906; U-Net 0,606), nhưng **không cần bằng nhau** vì notebook tính trên mặt nạ 640×640, còn script tính trên mặt nạ gốc. Nếu lệch quá xa (ví dụ Dice gần 0) thì dừng tìm lỗi tiền xử lý.

### Bước 2: đánh giá theo điểm ảnh, ghi ra `bang/pixel_640/`
```
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py --models baseline tsvm pranet640 unet640 --out 00_tai_lieu_tong_quan/bang/pixel_640
```
**Kiểm tra:** các dòng `baseline` và `tsvm` trong `pixel_640/11_pixel_tung_seed.csv` phải trùng `bang/11_pixel_tung_seed.csv`. Lệch thì báo Huy.

Ước tính khoảng 20–30 phút GPU: 4 mô hình × 20 seed × 160 ảnh. YOLO chạy lại để đối chiếu.

### Bước 3: topology
- Thêm `--out` vào `danh_gia_topology.py`, mặc định vẫn là `bang/`.
- Chạy với `--models baseline tsvm pranet640 unet640 --out 00_tai_lieu_tong_quan/bang/pixel_640`.
- Kiểm tra: dòng `baseline`/`tsvm` trùng `bang/14_topology_tung_seed.csv`.
- Ước tính khoảng 20–30 phút.

### Bước 4: dữ liệu ngoài (nếu kịp)
- Thêm `--out` cho phần tổng hợp của `08_du_lieu_thuc_te/scripts/danh_gia_du_lieu_ngoai.py`, ví dụ `08_du_lieu_thuc_te/bang/pixel_640_20seed/`. **Không ghi đè `bang/20seed/`.**
- Chạy `--models pranet640 unet640 --seeds 0 … 19`. Từng lượt ghi file mới vào `tung_luot/`. Phần tổng hợp đọc thêm các lượt `baseline`/`tsvm` đã có để so sánh.
- Ước tính khoảng 1 giờ GPU: 3 bộ dữ liệu (khoảng 1.190 ảnh) × 2 mô hình × 20 seed.

### Bước 5: gửi lại cho Huy
1. **Bảng tóm tắt 20 seed (trung bình ± SD)** cho 4 mô hình: Dice, IoU, Precision, Recall, tỉ lệ ảnh nền báo nhầm. Kèm thời gian chạy từng bước và lỗi gặp phải (nếu có). Số thập phân dùng dấu phẩy.
2. **Commit lên `Okeydokey`:**
   - chỉ gồm 3 script đã sửa và các CSV mới trong `bang/pixel_640/`, `08_/bang/tung_luot/` (lượt 640), `08_/bang/pixel_640_20seed/`;
   - **không commit `.pth`/`.zip`** (`.gitignore` đã chặn).
   - Gửi Huy mã hash commit.
3. **Push:** Huy cần thấy commit trên GitHub, nên phải push `Okeydokey`. Theo quy tắc dự án, **chỉ push khi Lương đồng ý**.

## 4. Câu hỏi P/S: commit `9bd5d886` xóa `02_ma_nguon/ultralytics_MambaPSA`

**Cố ý, không phải nhầm.** Câu trả lời gửi Huy:
- Sáng 09/11, đợt 1 dọn thư mục để nộp: các mục không nộp được **chuyển** (không xóa hẳn) sang `DeepLearning/_Luu_Tru_Ngoai/Test_Mau/`, giữ nguyên đường dẫn con. Có ghi vào `PATH_MAP.md`/`.csv` và `_Luu_Tru_Ngoai/DANH_SACH_DA_CHUYEN.csv`.
- MambaPSA đã bỏ từ 07/11 vì không có mã gốc công bố để tái hiện. Ngày 09/11 nhóm chốt lại: bỏ cả MambaPSA, Polyp-PVT và VM-UNet, chỉ nêu trong phần hạn chế.
- Đợt đó chuyển `02_ma_nguon/ultralytics_MambaPSA/`, `02_ma_nguon/notebook_kaggle/mambapsa/`, file `ultralytics_MambaPSA.rar`, cùng 3 file Word trùng từng byte trong `06_bao_cao/`. Commit `9bd5d886` ghi lại việc chuyển này, nên git hiện là "deleted".
- Muốn lấy lại: bản đầy đủ còn trong lịch sử git (ví dụ `git checkout aba071e0 -- 02_ma_nguon/ultralytics_MambaPSA`) và trong `_Luu_Tru_Ngoai`.

**Phát hiện thêm:** commit `9bd5d886` lỡ đưa vào git file khóa tạm của Word `06_bao_cao/~$oCaoKhoaLuan_CNTT_KLCN182 (3)_sua_phan_bien_4_10.docx`. Word tạo file này khi đang mở tài liệu. Đề xuất:
- gỡ khỏi git bằng `git rm --cached`;
- thêm `~$*` vào `.gitignore`.

Việc này nên làm trong một commit riêng, khi bạn đồng ý.

## 5. Những thay đổi khác đang chưa commit (không đưa vào commit II.4)

- `tinh_ablation.py` (thêm lựa chọn 20 seed) và `bang/ablation_20seed/`
- `03_.../No_guidance/..._s14_w2/`, `..._s15_w2/` (`results.csv`, hình; `.pt` bị git bỏ qua)
- `PATH_MAP.md`/`.csv`, `README.md`
- `KE_HOACH_HOAN_THIEN_NOP_BAI.md`, `05_.../PHAN_HOI_CHECKPOINT_640.md`, file kế hoạch này

Đề xuất: commit II.4 tách riêng để Huy merge gọn; các mục trên commit sau, khi bạn duyệt.

## 6. Thứ tự làm và thời gian

| Thứ tự | Việc | Thời gian ước tính |
|---|---|---|
| 1 | Bước 1 (sửa script) + chạy thử seed 0 | 30–45 phút |
| 2 | Bước 2 (pixel), chạy nền | 20–30 phút GPU |
| 3 | Bước 3 (topology), chạy nối tiếp | 20–30 phút GPU |
| 4 | Bước 4 (dữ liệu ngoài), chạy nền | khoảng 1 giờ GPU |
| 5 | Bảng tóm tắt, commit, gửi Huy | 20 phút |
| 6 | Kế hoạch cũ: A1, A2 (ablation 20 seed, C2PSA rộng), A5–A7, C (đã sửa theo mục 1), E | theo `KE_HOACH_HOAN_THIEN_NOP_BAI.md` |

Trong lúc chạy các bước 2–4, GPU bận. Nên tắt AI service của web (cổng 8000) để số đo không bị nhiễu và máy không bị nặng.

## 7. Cần Lương chốt

1. Đồng ý làm II.4 trước, rồi mới làm phần còn lại của kế hoạch cũ?
2. Có làm bước 4 (dữ liệu ngoài, khoảng 1 giờ GPU) không?
3. Sau khi commit, có **push** `Okeydokey` để Huy lấy hash không?
4. **Phần D (báo cáo cuối bằng markdown):** Huy đang sửa Word. Nên bỏ phần D, hay chỉ cập nhật tài liệu tổng quan trong `00_tai_lieu_tong_quan/` để Huy lấy số?
5. Có gỡ file khóa Word `~$…docx` khỏi git trong commit riêng không?
