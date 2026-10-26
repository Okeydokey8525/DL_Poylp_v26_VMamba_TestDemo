# 🔗 ĐƯỜNG DẪN HỎNG — ĐÃ XỬ LÝ XONG
## Kết quả kiểm tra tự động sau đợt sửa v3.1

> **Ngày:** 02/10/2026
> **Công cụ:** `Stracth/check_doc_paths.py`
> **Tiêu chuẩn nghiệm thu đạt được:** ✅ **0 đường dẫn hỏng trong tài liệu đang hoạt động.**

---

## 1. KẾT QUẢ

| Mốc | Số đường dẫn hỏng | Ghi chú |
| :--- | ---: | :--- |
| Ban đầu (27/09/2026) | **88** | Trong 37 tệp `.md` |
| Sau vòng 1 — sửa tự động | 47 | `fix_doc_paths.py --apply` (27 quy tắc) |
| Sau vòng 2 — theo phương án duyệt | 21 | `fix_doc_paths_round2.py --apply` (23 quy tắc) |
| Sau vòng 3 — sửa thủ công | 18 | 2 tệp sửa trực tiếp |
| **Hiện tại — tài liệu đang hoạt động** | **0** ✅ | `doc/` (trừ `historical/`) |
| Hiện tại — trong `historical/` | **18** | **Giữ nguyên có chủ đích** (xem mục 3) |

**Diễn giải:** Toàn bộ đường dẫn hỏng trong tài liệu đang hoạt động đã được sửa. 18 đường dẫn còn lại nằm **chỉ trong `doc/historical/`** — đây là tài liệu lịch sử, đường dẫn cũ là chính xác theo thời điểm viết.

---

## 2. CÁC QUY TẮC ĐÃ ÁP DỤNG

### 2.1. Vòng 1 — sửa tự động (`fix_doc_paths.py`, 27 quy tắc)

| Đường dẫn cũ | Đường dẫn đúng | Nguyên nhân |
| :--- | :--- | :--- |
| `archive/KQ_Nen_DX_10seed/…` | `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/…` | Thư mục được di chuyển vào `Ket_Qua_V2/` ngày 28/09/2026 |
| `archive/KetQua_Nen/…` | `archive/Ket_Qua_V2/KetQua_Nen/…` | Tên biến thể viết sai dấu gạch |
| `archive/efficiency_benchmark/…` | `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/…` | Nằm trong gói kết quả |
| `archive/Kvasir_YOLO_SEG(_BG20)/…` | `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/…` | Đổi tên khi tách BG20 |
| `archive/convert_*_to_yolo_seg.py` | `archive/Stracth/convert_*_to_yolo_seg.py` | Chuyển script vào thư mục `Stracth/` |

### 2.2. Vòng 2 — sửa theo phương án đã duyệt (`fix_doc_paths_round2.py`, 23 quy tắc)

| Đường dẫn cũ | Xử lý đã áp dụng |
| :--- | :--- |
| `archive/doc/02_…`, `archive/doc/BAO_CAO_TIEN_DO_…` | → `archive/doc/historical/thuc_nghiem_6fold_5mo_hinh/…` |
| `archive/doc/05_KET_QUA_MAP_…` | → `archive/doc/historical/05_…` |
| `archive/doc/01_KIEN_TRUC_C2IAVM_…`, `09_…`, `11_…`, `12_…`, `14_…` | → `archive/doc/historical/mo_hinh_khong_lien_quan/…` |
| `archive/Khac_phuc/…` | Ghi chú: *"(đã xóa khỏi repo năm 2026)"* — **không còn trên đĩa** |
| `archive/KQ_Poylp`, `archive/Ket_Qua_V1`, `archive/Ket_Qua_2` | Ghi chú: *"(không còn trong repo)"* |
| `archive/KQ_DoiXung/…` | → `archive/Ket_Qua_V2/KQ_Nen_DX_10seed` |
| `archive/Kvasir_YOLO_SEG` | → `archive/Kvasir_YOLO_SEG.rar` _(bản gốc 1.000 ảnh — **KHÔNG dùng để train**)_ |
| `archive/Kvasir_YOLO_SEG_BG20` | → `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20` _(bản **dùng để train**)_ |
| `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/report.txt` | → `.../dataset_bg20_summary.json` (tệp thật) |
| `archive/KQ_Nen_DX_10seed/07a_pie_…png`, `05b_fold_…png` | Ghi chú: **chưa được tạo** + trỏ tới CSV dữ liệu + mục §K của `doc/22` |

### 2.3. Vòng 3 — sửa thủ công (2 tệp)

| Tệp | Sửa |
| :--- | :--- |
| `doc/06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md` | 2 tham chiếu hình `07a_…png`, `05b_…png` không tồn tại → ghi chú + trỏ CSV |
| `doc/kvasir_yolo_seg_output_spec.md` | `report.txt` → `dataset_bg20_summary.json` |

---

## 3. 18 ĐƯỜNG DẪN CÒN LẠI TRONG `historical/` — GIỮ NGUYÊN CÓ CHỦ ĐÍCH

| Tệp | Số | Lý do giữ |
| :--- | ---: | :--- |
| `historical/thuc_nghiem_6fold_5mo_hinh/BAO_CAO_TIEN_DO_TUAN_HOAN_CHINH.md` | 13 | Trỏ tới `archive/Ket_Qua/`, `archive/KQ_DoiXung/` — cấu trúc **trước v3.1**. Sửa đường dẫn sẽ làm sai lịch sử. |
| `historical/05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md` | 4 | ↑ |
| `historical/thuc_nghiem_6fold_5mo_hinh/02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md` | 1 | ↑ |

> **Quy ước:** Tài liệu trong `historical/` **ghi lại trạng thái tại thời điểm viết**. Đường dẫn hỏng ở đó là **thông tin lịch sử có giá trị**, không phải lỗi. Xem [`historical/README.md`](historical/README.md).

**Cách xử lý dài hạn (tùy chọn):** nếu muốn đạt `exit code = 0` tuyệt đối cho `check_doc_paths.py`, thêm vào `SELF_REPORT` trong script:
```python
SELF_REPORT = {"24_DANH_SACH_DUONG_DAN_HONG.md",
               "21_HUONG_DAN_BAN_GIAO_AI_MOI_VA_VIEC_CONG_TAI.md"}
```
rồi bổ sung điều kiện bỏ qua `doc/historical/`.

---

## 4. NGUYÊN NHÂN GỐC & CÁCH PHÒNG TRÁNH

| Nguyên nhân | Cách phòng tránh |
| :--- | :--- |
| Thư mục `KQ_Nen_DX_10seed` được **di chuyển** vào `Ket_Qua_V2/` (28/09/2026) nhưng tài liệu viết trước đó không cập nhật | Chạy `check_doc_paths.py` trước mỗi lần commit tài liệu |
| Tên biến thể: `KetQua_Nen` (thực) vs `Ket_Qua_Nen` (sai) | `fix_doc_paths.py` đã gom quy tắc đổi tên |
| `Khac_phuc/`, `KQ_DoiXung/`, `Ket_Qua_V1/`, `KQ_Poylp/`, `Ket_Qua_2/` đã bị dọn khỏi repo | Đã ghi chú tường minh tại các tài liệu liên quan |
| Tài liệu lịch sử bị di chuyển vào `historical/` nhưng tài liệu đang hoạt động vẫn trỏ tới | Đợt v3.1 đã cập nhật 8 tham chiếu sang đường dẫn mới |

### 3 script bảo trì

| Script | Chức năng |
| :--- | :--- |
| `Stracth/check_doc_paths.py` | Quét & báo cáo. Tự bỏ qua 2 tệp tự-trích-dẫn (`21`, `24`) |
| `Stracth/fix_doc_paths.py` | Sửa quy tắc đổi tên thư mục (vòng 1) |
| `Stracth/fix_doc_paths_round2.py` | Sửa đường dẫn tới thư mục đã dọn / đã chuyển (vòng 2) |

> Cả 3 script chạy ở **chế độ xem trước**; thêm `--apply` mới ghi file. Luôn kiểm tra bằng `git diff` trước khi ghi.

---

*Cập nhật cùng [`LICHSU_CAP_NHAT.md`](LICHSU_CAP_NHAT.md).*
