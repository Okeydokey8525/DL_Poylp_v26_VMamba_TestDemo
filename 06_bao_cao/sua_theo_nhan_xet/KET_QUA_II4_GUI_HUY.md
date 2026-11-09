# Kết quả II.4: đánh giá lại PraNet/U-Net 640 (chỉ suy luận)

Ngày 09/11/2026, nhánh `Okeydokey`.

**Hash commit:** `3777f19d1fe2774089ac7177e2cedf101189fd0d` (`3777f19d`), chưa push.

## 1. Đã làm gì

- `00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py`:
  - Thêm khóa `pranet640` và `unet640`.
  - Ảnh được kéo thẳng về 640×640, đúng cách tiền xử lý trong notebook huấn luyện.
  - Kiến trúc lấy từ `02_ma_nguon/notebook_kaggle/`.
  - Checkpoint nạp bằng `load_state_dict(strict=True)`.
  - Khóa `pranet`/`unet` (352) giữ nguyên.
- `danh_gia_topology.py`, `danh_gia_du_lieu_ngoai.py`: thêm `--out` và lọc mô hình khi tổng hợp.
  - Mặc định `--models` vẫn là bộ chính, nên các bảng cũ không bị ghi đè.
- Vị trí kết quả mới:
  - `00_tai_lieu_tong_quan/bang/pixel_640/`: bảng 10–15 (pixel, topology), `du_lieu_ngoai/{10,20}seed/`, `du_lieu_dinh_tinh/`, log.
  - `08_du_lieu_thuc_te/bang/tung_luot/*640_s*.csv`: 360 file, gồm 9 tập × 2 mô hình × 20 seed.
- Không ghi đè `bang/10–15_*.csv` hay `08_du_lieu_thuc_te/bang/20seed/` (đã so sánh, giống từng byte).
- Không commit `.pth` hay `.zip`.
- Không sửa Word, không viết nhận xét.

## 2. Bảng tóm tắt 20 seed (seed 0–19)

Trung bình ± SD qua 20 seed. Dice, IoU, Precision, Recall tính trên 120 ảnh polyp của tập val; tỉ lệ báo nhầm tính trên 40 ảnh nền.

| Mô hình | Dice | IoU | Precision | Recall | Ảnh nền báo nhầm |
|---|---|---|---|---|---|
| YOLO26s-seg (Baseline) | 0,8486 ± 0,0171 | 0,7927 ± 0,0170 | 0,8585 ± 0,0170 | 0,8703 ± 0,0193 | 0,0125 ± 0,0190 |
| YOLO26s-seg + TSVM | 0,8540 ± 0,0129 | 0,7998 ± 0,0129 | 0,8632 ± 0,0173 | 0,8730 ± 0,0112 | 0,0150 ± 0,0205 |
| PraNet 640 | 0,8856 ± 0,0053 | 0,8212 ± 0,0073 | 0,9044 ± 0,0111 | 0,9064 ± 0,0080 | 0,0275 ± 0,0077 |
| U-Net 640 | 0,6909 ± 0,0261 | 0,5713 ± 0,0283 | 0,7836 ± 0,0258 | 0,7165 ± 0,0252 | 0,5738 ± 0,0691 |

Bản 352 cũ để đối chiếu (bảng `bang/11–12`):

| Mô hình | Dice | IoU | Precision | Recall | Ảnh nền báo nhầm |
|---|---|---|---|---|---|
| PraNet 352 | 0,8541 ± 0,0068 | 0,7785 | 0,8687 | 0,8881 | 0,0075 |
| U-Net 352 | 0,7097 ± 0,0221 | 0,6069 | 0,7964 | 0,7167 | 0,2037 |

So sánh ghép cặp Dice qua 20 seed (nguồn: `pixel_640/12_pixel_thong_ke.csv`):

| Cặp so sánh | Chênh Dice | p (t ghép cặp) | Số seed TSVM cao hơn |
|---|---|---|---|
| TSVM − Baseline | +0,0054 | 0,26 | 13/20 |
| TSVM − PraNet 640 | −0,0316 | 1,1·10⁻⁸ | 0/20 |
| TSVM − U-Net 640 | +0,1631 | 6,5·10⁻¹⁷ | 20/20 |

Topology (min_area 20, tỉ lệ ảnh đúng số vùng `topo_ok`, nguồn `pixel_640/15_topology_thong_ke.csv`): Baseline 0,7967; TSVM 0,8079; PraNet 640 0,8771; U-Net 640 0,0992.

## 3. Dữ liệu ngoài: Dice trung bình 20 seed

Nguồn: `pixel_640/du_lieu_ngoai/20seed/02_ngoai_thong_ke.csv`. Các thống kê đầy đủ (SD, p, số seed TSVM cao hơn, IoU/P/R) nằm trong file này.

| Tập | Baseline | TSVM | PraNet 640 | U-Net 640 |
|---|---|---|---|---|
| CVC-ClinicDB | 0,7860 | 0,7702 | 0,7690 | 0,6003 |
| CVC-ColonDB | 0,6308 | 0,6012 | 0,5862 | 0,4249 |
| ETIS-Larib | 0,5347 | 0,5293 | 0,5509 | 0,3652 |
| PolypGen (gộp) | 0,7188 | 0,7153 | 0,7227 | 0,5186 |
| PolypGen C1 | 0,7533 | 0,7519 | 0,7335 | 0,5593 |
| PolypGen C2 | 0,7531 | 0,7486 | 0,7778 | 0,5520 |
| PolypGen C3 | 0,8547 | 0,8563 | 0,8561 | 0,6340 |
| PolypGen C4 | 0,5163 | 0,5031 | 0,5296 | 0,2895 |
| PolypGen C5 | 0,4738 | 0,4718 | 0,4948 | 0,3334 |
| PolypGen C6 | 0,7203 | 0,6992 | 0,6821 | 0,5158 |

## 4. Thời gian chạy và lỗi

- **Máy:** NVIDIA GeForce RTX 5050 Laptop, torch 2.13.0+cu130, Ultralytics 8.4.127 (fork TSVM).
- **Thời gian chạy:**

  | Phần | Phạm vi | Thời gian |
  |---|---|---|
  | Pixel | 4 mô hình × 20 seed × 160 ảnh | 5,6 phút |
  | Topology | 4 mô hình × 20 seed | 6,4 phút |
  | Dữ liệu ngoài | 2 mô hình 640 × 20 seed × 9 tập | 62,5 phút |

- **Lỗi:** không có. Cả 80 checkpoint (40 bản 352 + 40 bản 640) đều nạp được với strict=True, không lệch khóa nào.
- **Kiểm chéo:**
  - Dòng Baseline/TSVM trong `pixel_640/11` và `pixel_640/14` khớp tuyệt đối với `bang/11` và `bang/14` (chênh lớn nhất 0,0).
  - Quy đổi seed 0 về cách notebook tính (160 ảnh, ảnh nền đúng tính Dice = 1) cho PraNet 640 0,9065 và U-Net 640 0,606, khớp `tom_tat.txt` (0,906458 và 0,605972).

## 5. Lưu ý khi viết nhận xét

- **PraNet 640 so với TSVM:**
  - Trên tập val, PraNet 640 cao hơn TSVM rõ rệt và nhất quán (0/20 seed TSVM cao hơn).
  - Trên dữ liệu ngoài, chênh lệch nhỏ và đổi chiều tùy tập: PraNet 640 cao hơn ở ETIS, PolypGen C2, C4, C5; Baseline/TSVM cao hơn ở ClinicDB, ColonDB, C1, C6.
- **U-Net 640 kém bản 352:** Dice thấp hơn, và tỉ lệ báo nhầm ảnh nền tăng từ 0,20 lên 0,57.
- **TSVM so với Baseline:** không có ý nghĩa thống kê (p = 0,26), chỉ nên viết là "xu hướng".
