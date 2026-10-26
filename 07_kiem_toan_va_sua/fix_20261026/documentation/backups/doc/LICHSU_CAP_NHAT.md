# NHẬT KÝ & LỊCH SỬ CẬP NHẬT DỰ ÁN (PROJECT CHANGELOG)
## ĐỀ TÀI KHÓA LUẬN CỬ NHÂN: NGHIÊN CỨU TÍCH HỢP VMAMBA VÀO YOLO26-SEG PHÂN ĐOẠN POLYP
### Mã Đề Tài: `CNTT_KLCN182` | Trường Đại học Công Thương TP.HCM (HUIT)

---

## 📌 BẢNG TỔNG HỢP CÁC PHIÊN BẢN CẬP NHẬT

| Phiên bản | Ngày cập nhật | Nội dung chính | Trạng thái |
| :---: | :---: | :--- | :---: |
| **v1.0** | 10/2025 | Khởi tạo baseline YOLO26s-seg và khảo sát dữ liệu chuẩn Kvasir-SEG (1.000 ảnh) | Đã hoàn thành |
| **v1.5** | 11/2025 | Tích hợp thử nghiệm VMamba tại các vị trí: P3 (Sobel), Neck, Proto Head (Gặp OOM) | Đã ghi nhận Ablation |
| **v2.0** | 12/2025 | Cố định kiến trúc tích hợp VMamba tại **Layer 10 (P5, $20\times 20$)**; phát triển 4 hướng: C2TSVMamba, P5 Attention-VMamba, C2ITSMamba, C2IAVM (Mô hình Đề xuất C2IAVM) | Đã hoàn thành 6-fold |
| **v2.2** | 01/2026 | Hoàn thiện hệ thống tài liệu chuẩn học thuật (Doc 00 -> 15) và bảng đối chuẩn 6-fold cross-validation | Đã nghiệm thu |
| **v2.5** | 02/2026 | Mở rộng tập dữ liệu **Kvasir_YOLO_SEG_BG20** (+20% ảnh nền âm tính `normal-cecum`) giải quyết triệt để vấn đề độ đặc hiệu (Specificity) | Đã hoàn thành dataset |
| **v2.6** | 24/03/2026 | Kiểm toán chất lượng kết quả huấn luyện BG20; phát hiện & giải quyết sự cố `model.fuse()` tự động của Ultralytics gây lỗi ảnh trên Kaggle; khôi phục thành công trọn bộ **24 ảnh kết quả chuẩn / seed** tại thư mục ``Khac_phuc/` (đã xóa khỏi repo năm 2026)` | Đã hoàn thành |
| **v2.7** | 27/03/2026 | Giải nén, phân loại và tích hợp 17 file kết quả huấn luyện mới từ Kaggle vào `archive/Ket_Qua_V2/KetQua_Nen/`; mở rộng kiểm chứng Seed Robustness lên **10 seed** (tổng 47 runs/seeds); xây dựng công cụ kiểm toán và tổng hợp số liệu tự động | Đã hoàn thành |
| **v2.8** | 27/03/2026 | Hoàn thành bộ phân tích chuyên sâu và trực quan hóa kết quả thực nghiệm 10 seed giữa **Baseline (YOLO26s-seg)** và **TSVM (Topology-Shape)** đạt chuẩn luận văn (39 files, 11 bảng CSV, 20 biểu đồ 300 DPI) tại `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/` | Đã hoàn thành |
| **v2.9** | 28/03/2026 | Đồng bộ hóa toàn diện tập dữ liệu chính thức **`Kvasir_YOLO_SEG_BG20`** (1.200 ảnh, bổ sung 20% ảnh nền âm tính `normal-cecum`); xác nhận trạng thái đã hoàn tất huấn luyện 10 seed thực tế và cập nhật xuyên suốt hệ thống tài liệu `doc/` | Đã hoàn thành |
| **v3.0** | 29/09/2026 | Khảo sát và lập tài liệu truy xuất nguồn gốc mã nguồn (Provenance Tracking) của thư mục `Ket_Qua_V2/KQ_Nen_DX_10seed/`, định danh các script Python sinh dữ liệu và hướng dẫn tái chạy cho GPT/AI tiếp quản ([`18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md)) | Đã hoàn thành |
| **v3.1** | 02/10/2026 | **Kiểm chứng toàn bộ số liệu 10 seed (694 phép kiểm); sửa 3 nhóm sai lệch; ban hành 5 tài liệu mới; lưu trữ 10 tệp lịch sử vào `doc/historical/`** | **Hiện tại (Mới nhất)** |

---

## 🕒 CHI TIẾT TỪNG MỐC CẬP NHẬT

### 🔴 Phiên bản v3.1 (02/10/2026) – Kiểm Chứng Lại Toàn Bộ Số Liệu 10 Seed & Chuẩn Hóa Tài Liệu Khóa Luận Cử Nhận

* **Người thực hiện:** Nhóm nghiên cứu `CNTT_KLCN182` & AI Pair Programming.
* **Mục tiêu:** Tái trích xuất độc lập toàn bộ số liệu từ 20 tệp `results.csv` gốc để kiểm chứng tính trung thực của bộ kết quả 10 seed, sửa các tài liệu chứa số liệu sai lệch, và ban hành một tài liệu kết quả chuẩn duy nhất cho khóa luận cử nhận.

#### 1. Kết quả kiểm chứng số liệu

| Hạng mục kiểm tra | Phạm vi | Kết quả |
| :--- | :--- | :---: |
| Trích xuất lại từ 20 tệp `results.csv` (Baseline $s0$–$s9$, TSVM $s0$–$s9$) tại epoch tối ưu theo `metrics/mAP50-95(M)` | 20 run × 17 trường = **340 ô** | **Sai số tuyệt đối = 0** |
| Đối chiếu `01_raw_analysis/raw_10seeds_extracted_metrics.csv` | 340 ô | **ĐẠT** |
| Tính lại toàn bộ bảng thống kê dẫn xuất (`02_statistics`, `03_metrics`, `06_reports/summary.csv`) | **559 phép kiểm** | **0 sai lệch** |
| Đối chiếu `Stracth/bg20_all_seeds_metrics.csv` | 20 run | **Sai số = 0** |

> ✅ **Kết luận:** Toàn bộ **chỉ số mAP, Precision, Recall, Loss, Best Epoch** trong bộ kết quả 10 seed là **trung thực và có thể trích dẫn cho luận văn**.

#### 2. Ba nhóm sai lệch phát hiện và đã sửa

| # | Vấn đề | Mức độ | Xử lý |
| :--- | :--- | :---: | :--- |
| **1** | **`final_audit_report.md`, `conclusions_reviewed.md`, `recommended_figures_for_thesis.md`** chứa bảng số liệu hoàn toàn khác bộ kết quả hiện hành: bảng mAP@50-95 từng seed sai lệch toàn bộ, cột Box mAP@50-95 / Mask mAP@50 / Validation Loss / Best Epoch sai, danh sách seed thắng sai (ghi 8/10 cho Box thay vì 6/10), giá trị kiểm định *t*-test và Wilcoxon sai, trung bình ma trận nhầm lẫn sai (TP 112.4/113.8 thay vì 110.3/111.2), biên độ Range sai (0.0410/0.0242 thay vì 0.0425/0.0274). Ngoài ra `conclusions_reviewed.md` còn đưa số liệu của **P5 Attention VMamba** và **ITS Mamba** — hai dòng mô hình **không tồn tại trong `Ket_Qua_V2/`**. | 🔴 Cao | Viết lại toàn bộ 03 tài liệu theo số liệu tái trích xuất từ `results.csv`; thu hẹp về **2 mô hình**. |
| **2** | **Cột TN của ma trận nhầm lẫn không phải số đo.** `ultralytics/utils/metrics.py` hàm `ConfusionMatrix.process_batch` (dòng 427–434) **không có nhánh cộng vào ô background–background**; ô này luôn bằng 0, bị loại khỏi ghi nhãn (dòng 550) và hiển thị **trống** — xác nhận trên cả 20 ảnh `confusion_matrix.png`. Giá trị TN trong CSV **đúng bằng $40 - FP$** ở cả 20 dòng → là **số tái dựng theo giả định**. | 🔴 Cao | Ghi cảnh báo vào **4 tài liệu** (`final_audit_report.md`, `conclusions_reviewed.md`, `recommended_figures_for_thesis.md`, báo cáo luận văn) và bản kết quả chuẩn. Hạ hình CM khỏi nhóm "hình chính". |
| **3** | **3 lượt chạy TSVM không đối chiếu được** với ảnh ma trận nhầm lẫn: `s0` (CSV 108/8/19 — ảnh **59/10/68**), `s5` (CSV 112/7/15 — ảnh **0/90/127**), `s8` (CSV 111/14/16 — ảnh **6/8/121**). Ảnh gốc cho thấy tỷ lệ phát hiện gần 0, **mâu thuẫn với `results.csv` của chính các lượt chạy đó**. 17/20 lượt chạy còn lại khớp chính xác. | 🔴 Cao | Công khai như giới hạn dữ liệu; yêu cầu tái tạo ma trận nhầm lẫn cho 3 seed này trước khi dùng làm bằng chứng. |
| **4** | **Cỡ mẫu ghi sai "167 ảnh"** — do cộng nhầm 127 *thực thể* với 40 *ảnh*. | 🟡 TB | Sửa thành **160 ảnh** (120 ảnh polyp chứa 127 thực thể + 40 ảnh nền). |
| **5** | `CNTT_KLCN182_LeDucLuong_old_report.md`: **6 giá trị *p*-value sai** trong Bảng 3 (0.2319→0.2273, 0.4439→0.5428, 0.7027→0.5907, 0.7677→0.7152, 0.9189→0.9334, 0.2887→0.2674), **2 khoảng [Min, Max] sai** (Box mAP@50, Box Recall), sai số làm tròn Δ và tỷ lệ giảm Std. | 🟡 TB | Sửa lại theo `full_comparison_mean_std.csv`. |
| **6** | `recommended_figures_for_thesis.md` trỏ tới **đường dẫn hình không tồn tại** (`02_distributions/`, `03_seed_by_seed/`, `04_confusion_matrix/`, `05_multimetric/`) do cấu trúc thư mục đã được tái tổ chức. | 🟡 TB | Cập nhật lại toàn bộ đường dẫn, **đã kiểm tra từng tệp tồn tại thực tế**. |
| **7** | **Ngôn ngữ tuyệt đối hóa** trong báo cáo luận văn ("chứng minh", "vượt trọi", "xác lập giá trị thực tế", quy kết nguyên nhân cho cơ chế SS2D/Bi-FPN) — trái với kết luận thống kê $p > 0.05$. | 🟡 TB | Diễn đạt lại theo chuẩn khách quan; bổ sung ghi chú bắt buộc dưới Bảng 3 và Bảng 5. |

#### 3. Tài liệu mới ban hành (5 tài liệu)

| Tài liệu | Mục đích |
| :--- | :--- |
| **[`20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md`](20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md)** | **NGUỒN SỐ LIỆU CHUẨN** cho khóa luận cử nhận. 9 mục, 9 bảng: cam kết truy xuất nguồn gốc, cảnh báo ma trận nhầm lẫn, quy mô thực nghiệm, bảng 13 chỉ số, độ ổn định, từng seed + t-test/Wilcoxon, ma trận nhầm lẫn kèm hạn chế, chi phí tính toán, hình ảnh, giới hạn nghiên cứu. |
| **[`21_HUONG_DAN_BAN_GIAO_AI_MOI_VA_VIEC_CONG_TAI.md`](21_HUONG_DAN_BAN_GIAO_AI_MOI_VA_VIEC_CONG_TAI.md)** | Hướng dẫn tiếp nhận cho AI mới: thứ tự đọc 10 bước, bảng tra cứu 10 câu hỏi thường gặp, bảng thuật ngữ, **danh sách việc tồ đọng P0–P2**, 7 điều **đừng làm**, thứ tự ưu tiên khi xung đột số liệu, lệnh thường dùng. |
| **[`22_DANH_MUC_HINH_ANH_TOAN_BO.md`](22_DANH_MUC_HINH_ANH_TOAN_BO.md)** | Danh mục **43 hình ảnh** chia 8 nhóm (A–H), kèm ánh xạ từng hình vào chương báo cáo; đề xuất bộ 8 hình tối thiểu; liệt kê 4 hình cần tạo thêm. |
| **[`23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md`](23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md)** | Môi trường đã xác nhận, thư viện cần cài, **cảnh báo đường dẫn hardcode**, quy trình tái chạy 6 bước, hướng dẫn sửa ma trận nhầm lẫn (P1-1/P1-2), bảng 7 sự cố thường gặp. |
| **[`24_DANH_SACH_DUONG_DAN_HONG.md`](24_DANH_SACH_DUONG_DAN_HONG.md)** | Báo cáo đường dẫn hỏng: **88 → 48** sau đợt sửa tự động; phân loại 19 cái trong `historical/` (không sửa) và 29 cái cần sửa tay. |

#### 4. Công cụ kiểm chứng mới (3 script)

| Script | Chức năng | Kết quả |
| :--- | :--- | :--- |
| `Stracth/verify_10seed_audit.py` | Tái trích xuất từ 20 `results.csv` gốc và đối chiếu **mọi** bảng phái sinh; sinh `07_audit/audit_report.md` | **694/694 ĐẠT**, exit 0 |
| `Stracth/check_doc_paths.py` | Quét đường dẫn hỏng trong 37 tệp `.md` | **0** cái trong tài liệu đang hoạt động |
| `Stracth/fix_doc_paths.py` + `fix_doc_paths_round2.py` | Sửa tự động (chế độ `--apply`) | **88 → 0** (50 quy tắc) |

> **Nguyên tắc được nhấn mạnh trong cả 4 script:** không bao giờ sửa tệp CSV gốc để cho khớp báo cáo.

#### 4b. Tái tạo báo cáo Word (P0-1, P0-2 — ĐÃ HOÀN THÀNH)

* Đã chạy lại `Stracth/generate_final_word_report.py` (đã sửa 17 quy tắc số liệu + chèn 2 hộp cảnh báo).
* Kiểm chứng bằng cách đọc trực tiếp `word/document.xml` của `CNTT_KLCN182_LeDucLuong.docx`:
  * **11/11 số liệu cũ đã loại khỏi tệp** (0.2319, 0.4439, 0.7027, 0.7677, 0.9189, 0.2887, "167 ", 112.4, 113.8, 17.4, 22.6).
  * **33/33 số liệu đúng có mặt** (0.7210, 0.7246, 0.9119, 0.9062, 1.3045, 1.2424, p = 0.3839, p = 0.2273, p = 0.0908, 110.3, 111.2, 16.8, 14.6, …).
  * 2 hộp cảnh báo bắt buộc đã được chèn dưới **Bảng 3** và **Bảng 5**.
  * Dòng TN / Specificity trong Bảng 5 được gắn nhãn **"[TÁI DỰNG, xem ghi chú]"** và in nghiêng.
* Kích thước `.docx`: 3.12 MB. **Lưu ý:** file `.pdf` cũ **chưa** được tái tạo từ `.docx` mới.

#### 4c. Xác minh các thư mục đã bị dọn khỏi repo

| Thư mục/tệp | Kết quả tra cứu |
| :--- | :--- |
| `archive/Khac_phuc/` | ❌ Không còn (tệp `Khac_phuc.rar` cũng **đã bị xóa**) → đã ghi chú trong 3 tài liệu |
| `archive/Ket_Qua_V1/`, `archive/Ket_Qua_2/`, `archive/KQ_Poylp/` | ❌ Không còn trên đĩa → đã ghi chú |
| `archive/KQ_DoiXung/` | ❌ Không còn → đã đổi tên sang `Ket_Qua_V2/KQ_Nen_DX_10seed` |
| `archive/Kvasir_YOLO_SEG.rar` (71.4 MB) | ✅ Còn — **bản gốc 1.000 ảnh, KHÔNG dùng để train** |
| `archive/Kvasir_YOLO_SEG_BG20.rar` (98.2 MB) | ✅ Còn — **bản dùng để train** |
| `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/` | ✅ Còn — bản train đã giải nén (`report.txt` không tồn tại → dùng `dataset_bg20_summary.json`) |

#### 5. Kiểm chứng toàn bộ chuỗi (bổ sung)

* Đã kiểm tra **tồn tại thực tế của toàn bộ 43 hình ảnh** trong `Ket_Qua_V2/KQ_Nen_DX_10seed/` trước khi ghi vào `doc/22`.
* Đã đọc trực tiếp `word/document.xml` của `CNTT_KLCN182_LeDucLuong.docx` để xác nhận 6 p-value sai vẫn còn trong bản Word (xem P0-1).

#### 6. Lưu trữ tài liệu lịch sử (10 tệp → `doc/historical/`)

| Nhóm | Số tệp | Vị trí mới |
| :--- | ---: | :--- |
| A. Sao lưu 6-seed (nhóm A) | 2 | `doc/historical/6seed_bao_luu/` |
| B. Thực nghiệm 6-fold 5 mô hình (nhóm B) | 2 | `doc/historical/thuc_nghiem_6fold_5mo_hinh/` |
| C. Mô hình ngoài phạm vi Baseline/TSVM (nhóm C) | 6 | `doc/historical/mo_hinh_khong_lien_quan/` |

Kèm `doc/historical/README.md` với quy tắc sử dụng và ghi chú về trạng thái `.docx`.

> ⚠️ **Sai lệch so với kế hoạch:** `CNTT_KLCN182_LeDucLuong_old_report.md` **được giữ lại tại thư mục gốc** thay vì chuyển vào kho — vì đây là bản văn bản đã hiệu chỉnh, trong khi `.docx` chính vẫn còn số liệu sai.

#### 7. Cập nhật chỉ mục

* Viết lại toàn bộ [`doc/README.md`](README.md) theo cấu trúc "START HERE": thứ tự đọc 4 bước, danh mục 7 nhóm, bối cảnh dữ liệu, phạm vi kiểm chứng, bảng tra cứu nhanh.

---

### 🌟 Phiên bản v3.0 (29/09/2026) – Thiết Lập Báo Cáo Ánh Xạ Script Và Nguồn Gốc Kết Quả 10-Seed Phục Vụ Bàn Giao GPT
* **Người thực hiện:** Nhóm nghiên cứu & AI Pair Programming.
* **Mục tiêu:** Định danh chính xác mối quan hệ giữa mã nguồn thực thi và các tệp dữ liệu, biểu đồ trong `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/`, hỗ trợ bàn giao và trao đổi thông tin chuẩn xác cho các mô hình AI khác (GPT).
* **Nội dung hoàn thành:**
  1. Ban hành tài liệu [`18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md) phân tích rõ 3 phân hệ bên trong `Ket_Qua_V2/KQ_Nen_DX_10seed`:
     - Phân hệ thống kê 10-seed & 20 chart khoa học (`01` -> `06`): Do script [`generate_10seed_thesis_package.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/generate_10seed_thesis_package.py) sinh ra.
     - Phân hệ 12 biểu đồ đối sánh trực diện (`figures/`): Do script [`render_kq_doixung_templates_2models.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/render_kq_doixung_templates_2models.py) sinh ra.
     - Phân hệ Benchmark hiệu năng phần cứng (`efficiency_benchmark/`): Do script [`benchmark_runner.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/benchmark_runner.py) và [`plot_efficiency_charts_2models.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/plot_efficiency_charts_2models.py) sinh ra.
  2. Cung cấp bảng tra cứu nhanh (Quick lookup table) và quy trình 4 bước tái thực thi (Re-execution protocol) xử lý sự chuyển dịch đường dẫn từ `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/` sang `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/`.
  3. Cập nhật chỉ mục tại [`archive/doc/README.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/README.md).

### 🌟 Phiên bản v2.9 (28/03/2026) – Đồng Bộ Hóa Tập Dữ Liệu Chính Thức Kvasir_YOLO_SEG_BG20 Xuyên Suốt Tài Liệu
* **Người thực hiện:** Nhóm nghiên cứu `CNTT_KLCN182` & AI Pair Programming.
* **Mục tiêu:** Cập nhật dứt điểm định nghĩa tập dữ liệu trong toàn bộ hệ thống file `.md` tại `archive/doc/`, xác định `Kvasir_YOLO_SEG_BG20` là tập dữ liệu chính thức của đề tài, đã có 20% ảnh nền âm tính và các mô hình đã được huấn luyện đối chuẩn thực tế trên tập này qua 10 random seeds (không còn ở trạng thái dự kiến hay chờ kết quả).
* **Chi tiết công việc & Kết quả thực hiện:**
  1. **Quy cách bộ dữ liệu chính thức:**
     - Tổng cộng 1.200 ảnh: gồm 1.000 ảnh polyp từ Kvasir-SEG và bổ sung 200 ảnh niêm mạc manh tràng bình thường (`normal-cecum`) từ Kvasir v2.
     - Tập Train: 1.040 ảnh (880 ảnh polyp có nhãn đa giác + 160 ảnh nền rỗng 0-byte).
     - Tập Validation: 160 ảnh (120 ảnh polyp chứa 127 polyp GT + 40 ảnh nền rỗng 0-byte).
     - Tệp cấu hình chuẩn: `data_bg20.yaml`.
  2. **Trạng thái thực nghiệm:**
     - Toàn bộ các dòng mô hình (Baseline YOLO26s-seg, TSVM, P5_Attention, ITSMamba) đã được huấn luyện hoàn tất trên Kaggle GPU Tesla T4 (lưu trữ đầy đủ tại `archive/Ket_Qua_V2/KetQua_Nen/`).
     - Khắc phục triệt để hiện tượng 1.00 False Positive do thiếu True Negative trong tập thuần polyp cũ.
  3. **Đồng bộ hóa tài liệu thuyết minh:**
     - Cập nhật [`00_TONG_QUAN_VA_TINH_HINH_DU_AN.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/00_TONG_QUAN_VA_TINH_HINH_DU_AN.md), [`16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md), [`03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md), [`kvasir_yolo_seg_output_spec.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/kvasir_yolo_seg_output_spec.md), [`README.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/README.md), [`YEU_CAU_DAC_TA_DU_LIEU_BO_SUNG_CROSS_DATASET.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/YEU_CAU_DAC_TA_DU_LIEU_BO_SUNG_CROSS_DATASET.md).

---

### 🌟 Phiên bản v2.8 (27/03/2026) – Xây Dựng Trọn Bộ Phân Tích & Hệ Thống Biểu Đồ 10 Seed Chuẩn Luận Văn
* **Người thực hiện:** Nhóm nghiên cứu `CNTT_KLCN182` & AI Pair Programming.
* **Mục tiêu:** Xây dựng quy trình khép kín từ trích xuất dữ liệu, tính toán thống kê mô tả, kiểm định giả thuyết (Paired t-test, Wilcoxon), ma trận nhầm lẫn chuẩn hóa và 20 biểu đồ khoa học 300 DPI phục vụ luận văn tốt nghiệp.
* **Chi tiết công việc & Kết quả thực hiện:**
  1. **Khởi tạo và chuẩn hóa thư mục đích:**
     - Thiết lập cấu trúc [`archive/Ket_Qua_V2/KQ_Nen_DX_10seed/`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed) với 6 phân hệ con: `01_raw_analysis`, `02_statistics`, `03_metrics`, `04_confusion_matrix`, `05_charts`, `06_reports`.
  2. **Trích xuất dữ liệu thực tế 100% (Không suy diễn số liệu):**
     - Đọc trọn vẹn 10 seeds (`s0` đến `s9`) của Baseline và TSVM từ `results.csv` tại epoch tối ưu Mask mAP@50-95.
     - Kiểm định ma trận nhầm lẫn 2x2 trên 160 ảnh kiểm định (127 polyp GT + 40 ảnh nền âm tính), tính ma trận đếm trung bình và ma trận phần trăm chuẩn hóa theo hàng.
  3. **Kết xuất 20 biểu đồ khoa học đạt chuẩn 300 DPI:**
     - 5 biểu đồ Performance (Mask mAP50-95, mAP50, Precision/Recall, Bounding Box, Val Seg Loss).
     - 3 biểu đồ Stability (Đường xu hướng 10 seed mAP@50-95, Box mAP@50-95, Error bar đa chỉ số).
     - 2 biểu đồ Distribution (Boxplot kèm jitter strip plot, Histogram kèm KDE).
     - 3 biểu đồ Correlation (Phân tán Precision vs Recall, tương quan mAP với Precision và Recall).
     - 4 biểu đồ Confusion Matrix (Heatmap đếm và chuẩn hóa % cho Baseline và TSVM).
     - 3 biểu đồ Summary (Grouped bar chart tổng hợp, Radar chart đa chiều, Thanh ngang phân kỳ $\Delta$).
  4. **Soạn thảo báo cáo học thuật chuẩn mực:**
     - [`summary.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/summary.md): Bảng tổng hợp Mean ± Std, Min/Max/Range, Tỷ lệ thắng seed.
     - [`conclusions.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/conclusions.md): Đánh giá khách quan theo 6 nhóm tiêu chí khoa học, không dùng từ ngữ tâng bốc.
     - [`README.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/README.md): Hướng dẫn sử dụng và mục lục hệ thống.

---

### 🌟 Phiên bản v2.7 (27/03/2026) – Tiếp nhận Kết quả Mới, Tích hợp & Mở rộng Kiểm thử 10 Seed (BG20)
* **Người thực hiện:** Nhóm nghiên cứu `CNTT_KLCN182` & AI Pair Programming.
* **Mục tiêu:** Giải nén, sắp xếp toàn bộ các tệp kết quả nén mới từ Kaggle vào đúng các thư mục mô hình trong `archive/Ket_Qua_V2/KetQua_Nen/`, thống kê số lượng seed, kiểm toán tính toàn vẹn và lập bảng tổng hợp số liệu thực nghiệm mở rộng.
* **Chi tiết công việc & Kết quả thực hiện:**
  1. **Giải nén và cấu trúc hóa toàn bộ 17 tệp kết quả nén mới:**
     - Tiếp nhận 17 tệp zip tại `archive/Ket_Qua_V2/KetQua_Nen/` gồm: `results.zip`, `runs.zip`, `runs (1).zip` đến `runs (15).zip`.
     - Giải nén sạch và phân loại chính xác vào 5 thư mục mô hình tương ứng:
       + `YOLOv26s-seg/`: Tiếp nhận thêm 4 seed (`s6`, `s7`, `s8`, `s9`), nâng tổng số lên **10/10 seed** (từ `s0` đến `s9`).
       + `Kvasir_BG20_YOLO26s_seg_TSVM/`: Tiếp nhận thêm 4 seed (`s6`, `s7`, `s8`, `s9`), nâng tổng số lên **10/10 seed** (từ `s0` đến `s9`).
       + `Kvasir_BG20_YOLO26s_seg_P5_Attention_VMamba/`: Tiếp nhận thêm 4 seed (`s6`, `s7`, `s8`, `s9`), nâng tổng số lên **10/10 seed** (từ `s0` đến `s9`).
       + `Kvasir_BG20_YOLO26s_seg_ITSMamba/`: Tiếp nhận thêm 4 seed (`s6`, `s7`, `s8`, `s9`), nâng tổng số lên **10/10 seed** (từ `s0` đến `s9`).
       + `Kvasir_BG20_YOLO26s_seg/` (Mô hình C2IAVM): Tiếp nhận thêm seed `s6`, nâng tổng số lên **7 seed** (từ `s0` đến `s6`, sẵn sàng đón nhận `s7`-`s9`).
  2. **Thống kê và kiểm toán toàn vẹn:**
     - Tổng cộng toàn bộ thư mục `KetQua_Nen`: **47 runs / seeds** hoàn chỉnh.
     - Kiểm toán 100% (47/47 thư mục): Đều có tệp nhật ký huấn luyện `results.csv` và checkpoint trọng số tốt nhất `weights/best.pt`.
  3. **Xây dựng công cụ kiểm toán & Tổng hợp số liệu:**
     - Xây dựng script kiểm toán và tổng hợp tự động [archive/Stracth/summarize_ketqua_nen.py](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/summarize_ketqua_nen.py).
     - Kết xuất bảng số liệu toàn diện 47 lượt chạy lưu tại [archive/Stracth/bg20_all_seeds_metrics.csv](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/bg20_all_seeds_metrics.csv).
  4. **Cập nhật tài liệu kỹ thuật dự án:**
     - Cập nhật mục 5 trong [doc/16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md).
     - Cập nhật trạng thái trong [doc/README.md](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/README.md) và [doc/LICHSU_CAP_NHAT.md](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/LICHSU_CAP_NHAT.md).

---

### 🚀 Phiên bản v2.6 (24/03/2026) – Kiểm toán & Khắc phục Sự cố Xuất ảnh trên Kaggle
* **Người thực hiện:** Nhóm nghiên cứu `CNTT_KLCN182` & AI Pair Programming.
* **Mục tiêu:** Kiểm toán toàn diện các artifact sau huấn luyện của mô hình TSVM trên tập BG20, làm rõ nguyên nhân số liệu đúng nhưng ảnh bị lỗi và tái lập trọn vẹn 24 ảnh kết quả/seed.
* **Chi tiết thay đổi & phát hiện kỹ thuật:**
  1. **Làm rõ tính toàn vẹn của dữ liệu gốc:**
     - Xác thực các tệp `results.csv` tại cả 6 seed của mô hình TSVM đều chứa số liệu thực nghiệm chính xác, trung thực. Seed 0 đạt Mask mAP@50 là **$0.9040$**; Seed 5 đạt Mask mAP@50 là **$0.9096$**.
     - Checkpoint `weights/best.pt` của cả 2 seed hoàn toàn nguyên vẹn, chứa đầy đủ các trọng số chất lượng cao của nhánh One-to-Many.
  2. **Phát hiện nguyên nhân gốc rễ (Root Cause):**
     - Ở epoch cuối cùng trên Kaggle, Ultralytics tự động gọi `model.fuse()`. Trong custom head `Segment26`, hàm này đã xóa bỏ nhánh One-to-Many (`self.cv2 = self.cv3 = self.cv4 = None`) và ép chuyển model sang nhánh One-to-One (End-to-End).
     - Do nhánh One-to-One tại Seed 5 chưa hội tụ (confidence tối đa chỉ đạt 0.028), việc suy diễn bị sụp đổ, sinh ra các bounding box rác kéo dài từ đỉnh xuống đáy màn hình ($y_1=0 \to y_2=640$) và làm rỗng 8 đồ thị đánh giá (AUC = 0).
     - Phát hiện lỗi thứ tự tọa độ trong Pillow 10+ (`ValueError: x1 must be greater than or equal to x0`) trên background thread của `plot_images`, làm đứt gãy việc lưu các file `val_batch*_pred.jpg`.
  3. **Khắc phục thành công và nghiệm thu 24 ảnh chuẩn / seed:**
     - Thiết lập cơ chế vô hiệu hóa `fuse()`, khóa cứng `Detect.end2end = False` và bổ sung patch sắp xếp tọa độ an toàn cho Pillow.
     - Xuất lại đầy đủ, chính xác **24/24 file ảnh** cho cả Seed 0 và Seed 5 (gồm 7 ảnh train, 3 ảnh val labels, 1 ảnh results.png, 3 ảnh val predictions sạch cột dọc, 2 ảnh confusion matrix, 8 ảnh performance curves chuẩn 300 DPI khớp 100% với `results.csv`).
     - Đóng gói toàn bộ kết quả vào thư mục độc lập:
       - ``Khac_phuc/…` (đã xóa khỏi repo năm 2026)/`
       - ``Khac_phuc/…` (đã xóa khỏi repo năm 2026)/`
  4. **Cập nhật tài liệu mới:**
     - Khởi tạo [doc/17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md).
     - Xây dựng script hướng dẫn tái lập cho Kaggle: [archive/Stracth/kaggle_val_fix_guide.py](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Stracth/kaggle_val_fix_guide.py).

---

### 📦 Phiên bản v2.5 (15/02/2026) – Mở rộng Tập Dữ liệu Kvasir_YOLO_SEG_BG20
* **Nội dung:**
  - Bổ sung 200 ảnh nội soi manh tràng lành (`normal-cecum` từ Kvasir v2) với nhãn rỗng 0-byte (160 ảnh vào tập Train, 40 ảnh vào tập Validation) để giải quyết triệt để hiện tượng báo động giả mô nền và ô `1.00` trong ma trận nhầm lẫn chuẩn hóa.
  - Xây dựng tài liệu kỹ thuật [doc/16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md).
  - Chuẩn hóa bộ siêu tham số khóa tất định 100% trên Kaggle GPU (AdamW, lr0=0.001, close_mosaic=10, 100 epochs, seed cố định 0 -> 5).

---

### 🏆 Phiên bản v2.0 (20/12/2025) – Hoàn thành Thực nghiệm 4 Hướng Tích hợp VMamba
* **Nội dung:**
  - Thực nghiệm đối chuẩn 6-fold cross-validation nghiêm ngặt giữa Baseline YOLO26s-seg và 4 hướng tiếp cận cải tiến.
  - Khảo sát mô hình đề xuất trọng tâm **`C2IAVM` (Attention-VMamba Fusion)**: Mask mAP@50-95 đạt **$73.61\%$** (kỷ lục $74.66\%$), giảm phương sai $4.39\times$, thể hiện hiệu năng cân bằng giữa không gian và kênh.
  - Hoàn tất bộ tài liệu học thuật từ `00_TONG_QUAN_VA_TINH_HINH_DU_AN.md` đến `15_CAM_NANG_PHONG_CACH_WORD_VA_NGON_NGU_HOC_THUAT.md`.

---

### 🧪 Phiên bản v1.0 -> v1.5 (10/2025 – 11/2025) – Nghiên cứu Cơ sở & Thăm dò Kiến trúc
* **Nội dung:**
  - Thiết lập baseline chuẩn YOLO26s-seg trên tập dữ liệu Kvasir-SEG gốc.
  - Khảo sát các điểm nghẽn bộ nhớ của VMamba: chứng minh việc gắn SS2D tại tầng sớm P3 hoặc Proto Head gây tràn bộ nhớ (OOM) trên GPU 15GB.
  - Phát hiện và chuẩn hóa giải pháp tính toán **Cách 2: Pure PyTorch với `SelectiveScanAutograd`**, giải phóng sự phụ thuộc vào custom C++ CUDA kernel.

---
*Nhật ký này được duy trì và cập nhật liên tục theo tiến độ thực tế của đề tài.*
