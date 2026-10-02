# 🧭 HƯỚNG DẪN BÀN GIAO CHO AI MỚI & VIỆC CÒN TỒ ĐỌNG
## Tài liệu đọc đầu tiên khi tiếp nhận dự án `CNTT_KLCN182`

> **Mục đích:** Cho một AI (hoặc một thành viên mới) biết **đọc gì, theo thứ tự nào, làm gì tiếp theo, và không được làm gì**.
> **Ngày lập:** 02/10/2026 — tương ứng phiên bản `v3.1` trong [`LICHSU_CAP_NHAT.md`](LICHSU_CAP_NHAT.md).

---

## PHẦN 1 — ĐỌC THEO THỨ TỰ NÀO (bắt buộc)

Đọc đúng thứ tự dưới đây. **Không được bỏ qua mục 1–3.**

| Bước | Đọc tài liệu | Mục đích | Mất bao lâu |
| :---: | :--- | :--- | :---: |
| **1** | [`README.md`](README.md) | Bản đồ knowledge base, phạm vi dữ liệu hiện tại | 2 phút |
| **2** | [`20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md`](20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md) | **NGUỒN SỐ LIỆU DUY NHẤT.** 9 bảng số đã kiểm chứng | 15 phút |
| **3** | [`20_...md` §0.2 và §5.2](20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md) — *Giới hạn ma trận nhầm lẫn* | **Bắt buộc.** Biết điều gì **không** được trích dẫn | 5 phút |
| **4** | [`AI_WORK_OPTIMIZATION_RULE.md`](AI_WORK_OPTIMIZATION_RULE.md) + [`nguyen-tac-lam-viec-dai.md`](nguyen-tac-lam-viec-dai.md) | Quy tắc làm việc bắt buộc của dự án | 10 phút |
| **5** | [`01_KIEN_TRUC_TSVM_TANG_10.md`](01_KIEN_TRUC_TSVM_TANG_10.md) | Kiến trúc mô hình đề xuất (Layer 10 / P5) | 10 phút |
| **6** | [`16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md`](16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md) | Vì sao có tập BG20, cách tạo, cấu hình huấn luyện | 15 phút |
| **7** | [`18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md`](18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md) | Script nào sinh ra tệp nào — truy vết nguồn gốc | 10 phút |
| **8** | [`22_DANH_MUC_HINH_ANH_TOAN_BO.md`](22_DANH_MUC_HINH_ANH_TOAN_BO.md) | Chọn hình nào cho chương nào | 10 phút |
| **9** | [`23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md`](23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md) | Cài đặt, chạy lại pipeline từ đầu | 10 phút |
| **10** | [`CURRENT_PROJECT_STATUS.md`](CURRENT_PROJECT_STATUS.md) | Trạng thái hiện tại của dự án | 5 phút |

> **Tài liệu trong [`historical/`](historical/README.md)**: chỉ đọc khi tra cứu lịch sử phát triển kiến trúc. **Không dùng làm nguồn số cho báo cáo.**

---

## PHẦN 2 — CÂU HỎI THƯỜNG GẶP → TRẢ LỜI Ở ĐÂU

| Câu hỏi của AI | Trả lời ở đâu |
| :--- | :--- |
| "Số liệu chuẩn để viết báo cáo ở đâu?" | `doc/20_...md` §2 (bảng tổng hợp), §3 (từng seed), §4 (kiểm định) |
| "Cấu trúc tập dữ liệu thế nào?" | `doc/20_...md` §1 + `doc/kvasir_yolo_seg_output_spec.md` |
| "TSVM khác Baseline ở chỗ nào?" | `doc/01_KIEN_TRUC_TSVM_TANG_10.md` |
| "Dùng hình nào cho chương X?" | `doc/22_DANH_MUC_HINH_ANH_TOAN_BO.md` |
| "Viết bảng LaTeX thế nào?" | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/recommended_figures_for_thesis.md` §3 |
| "Viết kết luận mà không nói quá thì sao?" | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/conclusions.md` + `conclusions_reviewed.md` |
| "Chạy lại số liệu thế nào?" | `doc/23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md` |
| "Kiểm tra số liệu có đúng không?" | `python Stracth/verify_10seed_audit.py` |
| "Số nào KHÔNG được trích dẫn?" | `doc/20_...md` §5.2 + `final_audit_report.md` §2.2 |
| "Trước đây dự án từng làm gì?" | `historical/README.md` |

---

## PHẦN 3 — BẢNG THUẬT TỪ KHÓA / VIẾT TẮT

| Thuật ngữ | Ý nghĩa |
| :--- | :--- |
| **Baseline** | YOLO26s-seg chuẩn (`yolo26s-seg.pt`), mô hình đối chứng |
| **TSVM** | Topology-Shape-aware VMamba — mô hình đề xuất: YOLO26s-seg + nhánh SS2D tại Layer 10 (P5, 20×20) |
| **BG20** | `Kvasir_YOLO_SEG_BG20` — Kvasir-SEG + 20% ảnh nền âm tính `normal-cecum`; 1.200 ảnh |
| **SS2D** | 2D Selective Scan — cơ chế quét chọn lọc 4 hướng trong VMamba |
| **One-to-Many** | Nhánh đầu ra đa nhãn của `Segment26`; nhánh One-to-One là nhánh end-to-end |
| **DFL** | Distribution Focal Loss — hàm mất mát hồi quy bounding box (cột `val/l1_loss`) |
| **TP / FP / TN / FN** | True/False Positive/Negative — xem cảnh báo ở `doc/20_...md` §0.2 trước khi dùng TN |
| **best_epoch** | Epoch có `metrics/mAP50-95(M)` cao nhất; metric được trích tại epoch này |
| **Độ lệch chuẩn mẫu** | `ddof=1` — dùng nhất quán trong mọi bảng thống kê |
| **W2** | Worker 2 — hậu tố thư mục lượt chạy (`..._s0_w2`) |

---

## PHẦN 4 — 🔴 VIỆC CÒN TỒ ĐỌNG (Xử lý theo thứ tự ưu tiên)

> Đây là danh sách **việc chưa làm**. AI mới tiếp nhận nên bắt đầu từ P0.

### P0 — Bắt buộc làm trước khi nộp báo cáo

| # | Việc | Vì sao | Ước lượng |
| :--- | :--- | :--- | :--- |
| **P0-1** | ✅ **ĐÃ XONG** — Tái tạo `CNTT_KLCN182_LeDucLuong.docx` | Script đã chạy lại; 11/11 số liệu cũ đã loại khỏi tệp |
| **P0-2** | ✅ **ĐÃ XONG** — Thêm 2 hộp cảnh báo bắt buộc vào `.docx` | Đã chèn dưới Bảng 3 và Bảng 5; dòng TN/Specificity gắn nhãn "TÁI DỰNG" |
| **P0-3** | ✅ **ĐÃ XONG** — Chạy `verify_10seed_audit.py` | **694/694 phép kiểm ĐẠT**; báo cáo tại `KQ_Nen_DX_10seed/07_audit/` |
| **P0-4** | 🆕 **Tái tạo `CNTT_KLCN182_LeDucLuong.pdf`** từ `.docx` mới | File `.pdf` vẫn là bản cũ (chứa số liệu sai) | 5 phút |

### P1 — Nâng chất lượng khoa học

| # | Việc | Vì sao | Ước lượng |
| :--- | :--- | :--- | :--- |
| **P1-1** | **Tái tạo ma trận nhầm lẫn cho TSVM `s0`, `s5`, `s8`** | Ảnh `confusion_matrix.png` của 3 run này thuộc lượt validation bị lỗi (recall ≈ 0), **mâu thuẫn với `results.csv`**. Không thể trích dẫn CM cho tới khi tạo lại. Cần chạy lại `val` với `weights/best.pt` tương ứng. | 1–2 giờ GPU |
| **P1-2** | **Tạo bộ đếm TN/Specificity riêng** ngoài mã nguồn Ultralytics | Ô background↔background luôn = 0 (thiếu nhánh cộng trong `metrics.py:427-434`). Muốn có Specificity đáng tin cần tự đếm. | 2–3 giờ |
| **P1-3** | Phân tích công suất thống kê (power analysis) | Δ = +0.0036 với N = 10 không đạt ý nghĩa. Cần trả lời "cần bao nhiêu seed mới đủ sức phát hiện". | 1 giờ |
| **P1-4** | Phân tích ablation TSVM trên BG20 10 seed | Chưa có. Hiện mới chứng minh được "hiệu quả tổng thể", chưa tách được đóng góp từng thành phần. | 1–2 ngày GPU |

### P2 — Bổ sung cho hồ sơ

| # | Việc | Ghi chú |
| :--- | :--- | :--- |
| **P2-1** | Sửa 4 heatmap CM (`14_cm_count_*`, `15_cm_count_*`, `16_cm_percentage_*`, `17_cm_percentage_*`) mà `doc/07_...md` vẫn tham chiếu nhưng **không tồn tại** trong `KQ_Nen_DX_10seed/04_confusion_matrix/` | Có thể tái sinh từ `raw_10seeds_confusion_matrices.csv` bằng `Stracth/generate_10seed_thesis_package.py` |
| **P2-2** | ✅ **ĐÃ XONG** — Sửa đường dẫn chết trong `doc/` | **88 → 0** trong tài liệu đang hoạt động. Xem `doc/24_...md` |
| **P2-3** | Xóa vĩnh viễn 2 tệp trong `historical/6seed_bao_luu/` | Đã được duyệt chuyển vào kho; không còn giá trị sử dụng |
| **P2-4** | Bổ sung 2 hình: `07a_pie_polyp_clinical_breakdown.png`, `05b_fold_by_fold_recall.png` | `doc/06_...md` vẫn tham chiếu; xem `doc/22_...md` §K |
| **P2-5** | Tạo biểu đồ phân phối thống kê Δ theo seed (túi Wilcoxon) | Củng cố phần kiểm định |
| **P2-6** | Đồng bộ `CNTT_KLCN182_LeDucLuong_old_report.md` với `.docx` mới | Bản `.md` đã đúng; nếu `.docx` tái sinh lần nữa cần đồng bộ lại |

---

## PHẦN 5 — ⛔ ĐỪNG LÀM

| # | Đừng | Lý do |
| :--- | :--- | :--- |
| 1 | **Đừng sửa `results.csv` trong `KetQua_Nen/`** để cho khớp báo cáo | Vi phạm nguyên tắc `nguyen-tac-lam-viec-dai.md`. Mọi sai lệch phải sửa ở phía báo cáo. |
| 2 | **Đừng dùng số liệu trong `doc/historical/`** cho báo cáo | Thuộc thực nghiệm 6 seed / 6-fold, khác cấu hình. Xem `historical/README.md`. |
| 3 | **Đừng trích dẫn Specificity / ô TN** như chỉ số đo | Đó là số tái dựng $40 - FP$, không phải số đo. Xem `doc/20_...md` §0.2. |
| 4 | **Đừng viết "chứng minh", "vượt trội", "tối ưu", "vô địch"** | Không chỉ số nào có $p \le 0.05$. Vi phạm `nguyen-tac-lam-viec-dai.md`. |
| 5 | **Đừng suy diễn cơ chế** ("SS2D giúp bảo toàn topology…") từ số liệm mAP/CM | Cần ablation định lượng + trực quan hóa đặc trưng. |
| 6 | **Đừng thêm mô hình mới vào `conclusions*.md`** nếu không có `results.csv` gốc trong `Ket_Qua_V2/` | Đã xảy ra lỗi này: `conclusions_reviewed.md` từng đưa số liệu P5/ITS Mamba không tồn tại. |
| 7 | **Đừng chạy lại huấn luyện** mà không hỏi trước | Mỗi lượt ~100 epoch, tốn nhiều giờ GPU. |

---

## PHẦN 6 — QUY TẮC ƯU TIÊN KHI XUNG ĐỘT SỐ LIỆU

Khi hai nguồn cho hai số khác nhau, **đi theo thứ tự này**:

```
1. Ket_Qua_V2/KetQua_Nen/*/*/results.csv        ← dữ liệu gốc, thứ tự cao nhất
2. Ket_Qua_V2/KQ_Nen_DX_10seed/**/*.csv          ← bảng phái sinh (đã kiểm chứng)
3. doc/20_KET_QUA_CHUAN_..._10SEED.md           ← tài liệu chuẩn
4. Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/*.md   ← báo cáo phụ
5. CNTT_KLCN182_LeDucLuong_old_report.md         ← bản nháp văn bản
6. doc/*.md (khác)                               ← ghi chú bối cảnh
7. doc/historical/**                             ← lịch sử, KHÔNG dùng
```

Sau khi thay đổi số liệu ở bất kỳ cấp nào, **chạy lại** `python Stracth/verify_10seed_audit.py` để đảm bảo không phá vỡ tính nhất quán.

---

## PHẦN 7 — LỆNH THƯỜNG DÙNG

```powershell
# Kiểm chứng toàn bộ số liệu (694 phép kiểm)
python .\Stracth\verify_10seed_audit.py

# Tái sinh gói kết quả 01–06 (CẢNH BÁO: ghi đè CSV, chạy khi đã hiểu tác dụng)
python .\Stracth\generate_10seed_thesis_package.py

# Tái sinh 12 biểu đồ mẫu trong figures/
python .\Stracth\render_kq_doixung_templates_2models.py

# Tái tạo báo cáo Word (P0-1)
python .\Stracth\generate_final_word_report.py
```

> ⚠️ `generate_10seed_thesis_package.py` và `render_kq_doixung_templates_2models.py` có **đường dẫn đầu ra hardcode** trỏ tới `archive\KQ_Nen_DX_10seed` (thiếu `Ket_Qua_V2`) — phải cập nhật biến `ROOT_OUT` / `fig_dir` trước khi chạy. Chi tiết ở `doc/18_...md` §1.2.

---

## PHẦN 8 — GHI CHÚ VỀ THAY ĐỔI V3.1

Trước v3.1, ba tài liệu báo cáo trong `06_reports/` chứa **bảng số liệu sai hoàn toàn** (mAP từng seed, Box mAP@50-95, Mask mAP@50, Validation Loss, Best Epoch, giá trị kiểm định, trung bình ma trận nhầm lẫn, biên độ Range). Đã viết lại toàn bộ.

**Bài học rút ra — áp dụng cho mọi đợt cập nhật sau:**

1. **Không bao giờ chép số thủ công** từ báo cáo cũ sang báo cáo mới — luôn đọc từ CSV.
2. **Chạy `verify_10seed_audit.py` sau mỗi lần sửa số liệu.**
3. **Khi thêm/sửa bảng, kiểm tra cả cột *p*-value** — đây là cột bị sai nhiều nhất.
4. **Khi mô hình mới được thêm vào báo cáo**, phải xác nhận có `results.csv` gốc tương ứng trong `Ket_Qua_V2/` trước.

---

*Bảo trì tài liệu này cùng với [`LICHSU_CAP_NHAT.md`](LICHSU_CAP_NHAT.md). Khi hoàn thành một mục ở Phần 4, hãy đánh dấu `[x]` và ghi ngày.*
