# 📦 KHO TÀI LIỆU LỊCH SỬ (HISTORICAL ARCHIVE)

> **Ngày lập:** 02/10/2026 — trong đợt kiểm chứng số liệu phiên bản **v3.1**
> **Mục đích:** Lưu trữ tài liệu **KHÔNG còn đại diện cho trạng thái hiện tại** của dự án, nhưng vẫn giữ để truy vết và tra cứu lịch sử nghiên cứu.

---

## ⛔ QUY TẮC BẮT BUỘC

| # | Quy tắc |
| :--- | :--- |
| 1 | **Không dùng bất kỳ tài liệu nào trong thư mục này làm nguồn số liệu cho báo cáo khóa luận cử nhận.** |
| 2 | **Nguồn số duy nhất** cho báo cáo là [`../20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md`](../20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md) và các tệp CSV trong `Ket_Qua_V2/KQ_Nen_DX_10seed/`. |
| 3 | Số liệu trong các tài liệu này thuộc **thực nghiệm cũ** (6 seed, 6-fold cross-validation, tập Kvasir-SEG thuần polyp) — **không cùng cấu hình** với bộ thực nghiệm hiện hành (10 seed, BG20). |
| 4 | Khi trích dẫn tài liệu ở đây trong phần **phụ lục/tiểu sử**, phải ghi rõ: *"thực nghiệm giai đoạn trước, 6 seed, tập dữ liệu chưa bổ sung ảnh nền âm tính"*. |

---

## 📂 Cấu trúc

### `6seed_bao_luu/` — Bản sao lưu báo cáo giai đoạn 6-seed

| File | Mô tả | Tình trạng |
| :--- | :--- | :--- |
| `CNTT_KLCN182_LeDucLuong_backup_6seed.docx` | Bản `.docx` sao lưu báo cáo 6-seed (10 MB) | Có thể xóa vĩnh viễn |
| `CNTT_KLCN182_LeDucLuong_old_report_backup_6seed.md` | Bản `.md` của file trên | ⚠️ **Lưu trữ sai encoding** — byte `0xBB` không hợp lệ UTF-8, mọi trình đọc văn bản đều lỗi. Có thể xóa vĩnh viễn |

> ℹ️ Bản `.docx`/`.pdf` **chính** (10 seed, tại thư mục gốc `archive/`) chưa được tái tạo từ số liệu đã sửa — xem ghi chú bên dưới.

### `thuc_nghiem_6fold_5mo_hinh/` — Đối chiếu 5 mô hình, 6-fold (không còn dữ liệu gốc)

| File | Mô tả | Vì sao lưu trữ |
| :--- | :--- | :--- |
| `02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md` | Bảng đối chiếu Baseline + C2TSVMamba + P5 + C2ITSMamba + C2IAVM qua 6-fold | Chứa số liệu **chỉ tồn tại ở đây**; phục vụ tra cứu lịch sử phát triển kiến trúc |
| `BAO_CAO_TIEN_DO_TUAN_HOAN_CHINH.md` | Báo cáo tiến độ giai đoạn 6-seed | Ghi nhận mốc phát triển dự án |

> ⚠️ Số liệu 5 mô hình trong 2 file này **đã bị loại bỏ khỏi** `KQ_Nen_DX_10seed/06_reports/conclusions_reviewed.md` vì không thể kiểm chứng — `Ket_Qua_V2/` hiện chỉ chứa dữ liệu gốc cho **Baseline** và **TSVM**.

### `mo_hinh_khong_lien_quan/` — Các dòng mô hình ngoài phạm vi Baseline/TSVM

| File | Mô hình | Vì sao lưu trữ |
| :--- | :--- | :--- |
| `01_KIEN_TRUC_C2IAVM_CHAMPION_VA_CAC_BIEN_THE.md` | C2IAVM | Hồ sơ kiến trúc champion giai đoạn 6-fold |
| `09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md` | L10 vs P5 | Ablation định vị VMamba (P5 chọn vì tránh OOM) |
| `11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md` | P5 Attention-VMamba | Chứng minh VMamba dạng attention đơn lẻ không cải thiện |
| `12_CHI_TIET_KET_QUA_IAVM_INTERACTIVE_ATTENTION_VMAMBA.md` | C2IAVM | Chứa con số "167 ảnh" **sai** — đã ghi nhận, không dùng |
| `14_HUONG_8_INTERACTIVE_TOPOLOGY_VMAMBA.md` | ITSMamba (hướng 8) | Hồ sơ hướng nghiên cứu thứ 8 |

### `05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md` (ở gốc `historical/`)

Bản chuyên đề về mAP và độ ổn định seed dùng số liệu 6-fold 5 mô hình. **Trùng chủ đề** với `doc/20_...` (bản 10 seed 2 mô hình đã kiểm chứng) → giữ bản cũ trong kho.

---

## 🔴 GHI CHÚ QUAN TRỌNG VỀ BÁO CÁO `.docx`

Tại thời điểm lập kho này:

| Tệp | Tình trạng |
| :--- | :--- |
| `CNTT_KLCN182_LeDucLuong.docx` / `.pdf` (thư mục gốc `archive/`) | ⚠️ **Vẫn chứa 6 giá trị *p*-value sai** (0.2319, 0.4439, 0.7027, 0.7677, 0.9189, 0.2887) và cụm từ "167 đối tượng". Đã xác nhận bằng cách đọc trực tiếp `word/document.xml`. |
| `Stracth/generate_final_word_report.py` | ✅ **Đã sửa** (v3.1) — tái chạy script sẽ sinh ra `.docx` với số liệu đúng. |
| `CNTT_KLCN182_LeDucLuong_old_report.md` (thư mục gốc `archive/`) | ✅ **Đã sửa** (v3.1) — bản văn bản đã hiệu chỉnh, dùng để đối chiếu nội dung sau khi tái tạo `.docx`. |

**Việc cần làm tiếp:** chạy lại `Stracth/generate_final_word_report.py` để tái tạo `CNTT_KLCN182_LeDucLuong.docx` với số liệu đã hiệu chỉnh, đồng thời bổ sung hai hộp cảnh báo bắt buộc (dưới Bảng 3 và Bảng 5) như đã làm trong bản `.md`.

---

## 📌 Danh sách tệp bị chuyển vào kho (v3.1, 02/10/2026)

Tổng cộng **10 tệp** được chuyển khỏi vị trí cũ:

```
Nhóm A (2)  CNTT_KLCN182_LeDucLuong_backup_6seed.docx
            CNTT_KLCN182_LeDucLuong_old_report_backup_6seed.md
Nhóm B (2)  doc/02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md
            doc/BAO_CAO_TIEN_DO_TUAN_HOAN_CHINH.md
Nhóm C (6)  doc/01_KIEN_TRUC_C2IAVM_CHAMPION_VA_CAC_BIEN_THE.md
            doc/05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md
            doc/09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md
            doc/11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md
            doc/12_CHI_TIET_KET_QUA_IAVM_INTERACTIVE_ATTENTION_VMAMBA.md
            doc/14_HUONG_8_INTERACTIVE_TOPOLOGY_VMAMBA.md
```

> ⚠️ **Sai lệch so với kế hoạch:** `CNTT_KLCN182_LeDucLuong_old_report.md` (Nhóm A) **được giữ lại tại thư mục gốc** thay vì chuyển vào kho — vì đây là bản văn bản đã hiệu chỉnh của báo cáo và tệp `.docx` chính vẫn còn số liệu sai (xem ghi chú trên).

---

*Nhật ký kho lịch sử được duy trì trong [`../LICHSU_CAP_NHAT.md`](../LICHSU_CAP_NHAT.md).*
