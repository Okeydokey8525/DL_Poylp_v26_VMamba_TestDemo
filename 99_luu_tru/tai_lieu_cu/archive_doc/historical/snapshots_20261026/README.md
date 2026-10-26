# 📚 PROJECT KNOWLEDGE BASE — ĐỌC TỪ ĐÂY

> **Đề tài:** `CNTT_KLCN182` — Nghiên cứu tích hợp VMamba vào YOLO26-seg phân đoạn polyp
> **Cập nhật:** 02/10/2026 (phiên bản `v3.1`)
> **Phạm vi dữ liệu hiện tại:** **2 mô hình** — Baseline (YOLO26s-seg) và TSVM, mỗi mô hình **10 seed**, tập Kvasir-SEG BG20

---

## 🚀 BẠN LÀ AI MỚI? ĐỌC THEO THỨ TỰ NÀY

| Bước | Đọc gì | Mất bao lâu |
| :---: | :--- | :---: |
| 1 | ⭐ **[`20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md`](20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md)** — nguồn số liệu chuẩn | 15 phút |
| 2 | ⭐ **[`21_HUONG_DAN_BAN_GIAO_AI_MOI_VA_VIEC_CONG_TAI.md`](21_HUONG_DAN_BAN_GIAO_AI_MOI_VA_VIEC_CONG_TAI.md)** — đọc gì, làm gì tiếp, đừng làm gì | 10 phút |
| 3 | [`AI_WORK_OPTIMIZATION_RULE.md`](AI_WORK_OPTIMIZATION_RULE.md) + [`nguyen-tac-lam-viec-dai.md`](nguyen-tac-lam-viec-dai.md) — quy tắc làm việc bắt buộc | 10 phút |
| 4 | [`23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md`](23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md) — cài đặt, chạy lại pipeline | 10 phút |

> ⚠️ **Trước khi viết bất kỳ con số nào vào báo cáo:** đọc [`20_...md` §0.2 và §5.2](20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md) để biết **những gì không được trích dẫn**.

---

## ⭐ SỐ LIỆU CHUẨN — ĐỌC TRƯỚC TIÊN

### [`20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md`](20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md)

| Nội dung | Mô tả |
| :--- | :--- |
| §0 | Cam kết truy xuất nguồn gốc — kết quả kiểm chứng 340 ô / **694 phép kiểm ĐẠT** |
| §0.2 | 🔴 **Cảnh báo giới hạn ma trận nhầm lẫn — phải đọc** |
| §1 | Quy mô thực nghiệm & cấu hình (160 ảnh val = 120 polyp với 127 thực thể + 40 nền) |
| §2 | Bảng tổng hợp 13 chỉ số (Mean ± Std, Δ, %, p-value) |
| §3 | Độ ổn định: Std giảm 39.7%, phương sai co 2.75×, Range giảm 35.7% |
| §4 | So sánh từng seed + t-test & Wilcoxon đầy đủ |
| §5 | Ma trận nhầm lẫn + bảng hạn chế + **danh sách phát biểu được/không được dùng** |
| §6 | Chi phí tính toán, khả năng triển khai thời gian thực |
| §7 | Ánh xạ hình ảnh khuyến nghị |
| §8 | Danh mục tệp để đối chiếu |
| §9 | Giới hạn nghiên cứu cần nêu |

**Kết luận chủ đạo:** *Không chỉ số nào đạt ý nghĩa thống kê ở α = 0.05 (p = 0.3839). Đóng góp quan sát được rõ nhất của TSVM là **giảm phân tán** và **giảm Val Seg Loss**.*

---

## 1. Danh mục tài liệu

### 1.1. Bắt buộc — dùng hằng ngày

| Tài liệu | Mô tả |
| :--- | :--- |
| ⭐ [`20_KET_QUA_CHUAN_..._10SEED.md`](20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md) | **NGUỒN SỐ LIỆU DUY NHẤT** cho khóa luận cử nhận |
| ⭐ [`21_HUONG_DAN_BAN_GIAO_AI_MOI_...md`](21_HUONG_DAN_BAN_GIAO_AI_MOI_VA_VIEC_CONG_TAI.md) | Thứ tự đọc, câu hỏi thường gặp, việc còn tồ đọng, đừng làm gì |
| [`AI_WORK_OPTIMIZATION_RULE.md`](AI_WORK_OPTIMIZATION_RULE.md) | Quy tắc tối ưu công việc cho AI |
| [`nguyen-tac-lam-viec-dai.md`](nguyen-tac-lam-viec-dai.md) | Nguyên tắc làm việc & viết học thuật (34 KB — tài liệu chuẩn lớn nhất) |
| [`CURRENT_PROJECT_STATUS.md`](CURRENT_PROJECT_STATUS.md) | Trạng thái hiện tại |
| [`LICHSU_CAP_NHAT.md`](LICHSU_CAP_NHAT.md) | Nhật ký phiên bản |

### 1.2. Kiến trúc & phương pháp

| Tài liệu | Mô tả |
| :--- | :--- |
| [`01_KIEN_TRUC_TSVM_TANG_10.md`](01_KIEN_TRUC_TSVM_TANG_10.md) | TSVM tại Layer 10 / P5 — mô hình đề xuất |
| [`16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md`](16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md) | Vì sao có BG20, cách tạo dataset, cấu hình huấn luyện |
| [`kvasir_yolo_seg_output_spec.md`](kvasir_yolo_seg_output_spec.md) | Đặc tả định dạng dữ liệu YOLO-seg |
| [`YEU_CAU_DAC_TA_DU_LIEU_BO_SUNG_CROSS_DATASET.md`](YEU_CAU_DAC_TA_DU_LIEU_BO_SUNG_CROSS_DATASET.md) | Đặc tả bộ dữ liệu đa trung tâm (tương lai) |
| [`BAO_CAO_DAC_TA_HUONG_NGUEN_CUU.md`](BAO_CAO_DAC_TA_HUONG_NGUEN_CUU.md) | Đề cương nghiên cứu |

### 1.3. Phân tích chuyên sâu (Baseline vs TSVM)

| Tài liệu | Mô tả |
| :--- | :--- |
| [`03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md`](03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md) | Cấu trúc thư mục, hướng dẫn tái lập |
| [`04_KET_QUA_LOSS_VA_HOI_TU.md`](04_KET_QUA_LOSS_VA_HOI_TU.md) | Phân tích hàm mất mát & hội tụ |
| [`06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md`](06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md) | Phân tích đánh đổi Precision/Recall |
| [`07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md`](07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md) | Ma trận nhầm lẫn — **đọc hộp cảnh báo đỏ ở §6.3**; mục 1–5 là lịch sử 6-seed |
| [`08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md`](08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md) | Chi phí tính toán & triển khai |
| [`10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md`](10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md) | Đánh giá chất lượng mặt nạ |
| [`training_results_audit.md`](training_results_audit.md) | Kiểm toán kết quả huấn luyện |

### 1.4. Vận hành & công cụ

| Tài liệu | Mô tả |
| :--- | :--- |
| [`18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md`](18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md) | Script nào sinh tệp nào — truy vết nguồn gốc |
| ⭐ [`23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md`](23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md) | Cài đặt, biến môi trường, quy trình 6 bước, xử lý sự cố |
| ⭐ [`22_DANH_MUC_HINH_ANH_TOAN_BO.md`](22_DANH_MUC_HINH_ANH_TOAN_BO.md) | 43 hình ảnh → ánh xạ vào chương báo cáo |
| [`24_DANH_SACH_DUONG_DAN_HONG.md`](24_DANH_SACH_DUONG_DAN_HONG.md) | 48 đường dẫn hỏng còn lại |
| [`17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md`](17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md) | Sự cố `model.fuse()` trên Kaggle & cách khắc phục |

### 1.5. Văn phong & trình bày

| Tài liệu | Mô tả |
| :--- | :--- |
| [`19_QUY_CHUAN_THIET_KE_WORD_LE_DUC_LUONG.md`](19_QUY_CHUAN_THIET_KE_WORD_LE_DUC_LUONG.md) | Quy chuẩn thiết kế Word: typography, layout, bảng biểu, hình ảnh |
| [`15_CAM_NANG_PHONG_CACH_WORD_VA_NGON_NGU_HOC_THUAT.md`](15_CAM_NANG_PHONG_CACH_WORD_VA_NGON_NGU_HOC_THUAT.md) | Cảnh nâng phong cách Word & ngôn ngữ học thuật |

### 1.6. Lịch sử — chỉ đọc khi tra cứu

| Thư mục | Mô tả |
| :--- | :--- |
| [`historical/`](historical/README.md) | 10 tệp đã lưu trữ: bản sao lưu 6-seed, thực nghiệm 6-fold 5 mô hình, mô hình ngoài phạm vi. ⛔ **Không dùng làm nguồn số.** |

### 1.7. Tổng quan

| Tài liệu | Mô tả |
| :--- | :--- |
| [`00_TONG_QUAN_VA_TINH_HINH_DU_AN.md`](00_TONG_QUAN_VA_TINH_HINH_DU_AN.md) | Tổng quan & lịch sử các giai đoạn nghiên cứu |

---

## 2. Bối cảnh dữ liệu

### BG20 — `Kvasir_YOLO_SEG_BG20` (`data_bg20.yaml`)

| Hạng mục | Giá trị |
| :--- | :--- |
| Tổng số ảnh | **1.200** (1.000 Kvasir-SEG gốc + 200 nền âm tính `normal-cecum`) |
| Tập Train | 1.040 ảnh (880 polyp có nhãn + 160 nền rỗng) |
| Tập Validation | **160 ảnh** = 120 ảnh polyp (**127 thực thể**) + 40 ảnh nền |
| Huấn luyện | 100 epoch, AdamW, lr0=0.001, close_mosaic=10, imgsz=640, batch=8 |
| Số lượt chạy | **20** (10 seed × 2 mô hình) |

> ⚠️ **Không dùng con số "167 ảnh"** — đó là kết quả cộng nhầm 127 *thực thể* với 40 *ảnh*.

---

## 3. Phạm vi số liệu đã kiểm chứng (v3.1, 02/10/2026)

| Đối tượng | Kết quả |
| :--- | :--- |
| Trích xuất từ 20 tệp `results.csv` gốc | 340 ô, **sai số tuyệt đối = 0** |
| Tính lại toàn bộ bảng thống kê phái sinh | **694/694 phép kiểm ĐẠT** |
| Lệnh tái kiểm tra | `python Stracth/verify_10seed_audit.py` |

**Giới hạn đã biết về ma trận nhầm lẫn:**
1. Ô **TN không phải số đo** — là giá trị tái dựng $40 - FP$ (thiếu nhánh cộng trong `ultralytics/utils/metrics.py:427-434`).
2. **3/20 lượt chạy TSVM (s0, s5, s8)** không đối chiếu được với ảnh `confusion_matrix.png` gốc.

**Chỉ `Ket_Qua_V2/` chứa dữ liệu gốc cho 2 mô hình.** Các dòng P5 Attention-VMamba, ITS Mamba, IAVM, C2IAVM, C2TSVMamba thuộc thực nghiệm 6 seed / 6-fold cũ — không có `results.csv` trong bộ hiện hành.

---

## 4. Cấu trúc artifact

```
archive/
├── Ket_Qua_V2/
│   ├── KetQua_Nen/              ← DỮ LIỆU GỐC (không bao giờ sửa)
│   │   ├── YOLOv26s-seg/                (Baseline s0–s9)
│   │   └── Kvasir_BG20_YOLO26s_seg_TSVM/ (TSVM s0–s9)
│   ├── KQ_Nen_DX_10seed/        ← gói kết quả phái sinh (01–07)
│   ├── Kvasir_YOLO_SEG_BG20/    ← dataset
│   └── efficiency_benchmark/
├── Stracth/                     ← 48 script Python
├── ultralytics_Topology-Shape-aware VMamba/  ← fork Ultralytics (có One-to-Many)
├── data_bg20.yaml
└── doc/                         ← knowledge base (file này)
```

Không dùng tên thư mục cũ (``Ket_Qua_V1/` (không còn trong repo)`, `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/`) — không còn tồn tại.

---

## 5. Quy tắc sử dụng tài liệu

1. **Không lấy tài liệu trong `historical/` làm source of truth** cho trạng thái hiện tại.
2. **Không tự tạo số liệu.** Mọi con số phải truy được về `results.csv` hoặc CSV trong `Ket_Qua_V2/`.
3. **Không sửa raw CSV** để cho khớp báo cáo.
4. **Sau mỗi lần sửa số liệu**, chạy `python Stracth/verify_10seed_audit.py`.
5. **Không trích dẫn Specificity / ô TN** như chỉ số đo.
6. **Không dùng ngôn ngữ tuyệt đối hóa** ("chứng minh", "vượt trội") — không chỉ số nào có p ≤ 0.05.
7. Nếu source/config chưa tồn tại trên GitHub, **không mô tả nó là implementation hiện tại**.
8. Khi local/Kaggle mới hơn GitHub, **phải ghi rõ trạng thái chưa đồng bộ**.

---

## 6. Bảng tra cứu nhanh — câu hỏi thường gặp

| Câu hỏi | Tra cứu tại |
| :--- | :--- |
| Số liệu chuẩn để viết báo cáo? | `20_...md` §2–§4 |
| Số nào **không** được trích dẫn? | `20_...md` §5.2 |
| Cấu trúc dataset? | `20_...md` §1 |
| TSVM khác Baseline ở đâu? | `01_KIEN_TRUC_TSVM_TANG_10.md` |
| Dùng hình nào? | `22_DANH_MUC_HINH_ANH_TOAN_BO.md` |
| Chạy lại pipeline? | `23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md` |
| Kiểm tra số liệu? | `python Stracth/verify_10seed_audit.py` |
| Việc còn tồ đọng? | `21_...md` Phần 4 |
| Script nào sinh tệp nào? | `18_...md` |
| Mã LaTeX bảng/hình? | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/recommended_figures_for_thesis.md` |

---

*Tài liệu này được duy trì cùng [`LICHSU_CAP_NHAT.md`](LICHSU_CAP_NHAT.md). Khi thêm tài liệu mới, cập nhật cả hai.*
