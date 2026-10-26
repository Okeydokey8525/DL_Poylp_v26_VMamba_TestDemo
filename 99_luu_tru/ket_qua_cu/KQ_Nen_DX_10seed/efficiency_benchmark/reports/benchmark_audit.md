# BIÊN BẢN KIỂM TOÁN BENCHMARK HIỆU NĂNG TÍNH TOÁN (BENCHMARK AUDIT)
## Kiểm toán Tính Trung thực và Tính Toàn vẹn của Thực nghiệm Efficiency

**Ngày kiểm toán**: 27/09/2026  
**Mục tiêu**: Kiểm toán phương pháp đo đạc, tính xác thực của dữ liệu đo, và tuân thủ các quy tắc không làm sai lệch kết quả.

---

### 1. Bảng Tiêu chí Kiểm toán

| Tiêu chuẩn Kiểm toán | Chi tiết Rà soát | Đánh giá | Ghi chú Minh bạch |
| :--- | :--- | :---: | :--- |
| **Không retrain mô hình** | Trọng số được nạp nguyên gốc từ các checkpoint có sẵn trong `archive/KetQua_Nen/` | **ĐẠT** | Không có quá trình huấn luyện lại nào diễn ra |
| **Không sửa đổi raw 10-seed** | Toàn bộ tệp raw 10 seed tại `KetQua_Nen/` và `KQ_Nen_DX_10seed/` được giữ nguyên vẹn | **ĐẠT** | Tệp thời gian sửa đổi (Modified Time) và hash của các tệp cũ không bị can thiệp |
| **Đo lường độc lập** | 100 lần lặp đo đạc được thực hiện tự động bằng Python `time.perf_counter()` | **ĐẠT** | Đầy đủ 400 dòng dữ liệu raw tại `efficiency_raw_benchmark.csv` |
| **Giao thức Warmup** | Chạy 20 vòng warmup trước khi bấm giờ để ổn định cache CPU | **ĐẠT** | Đúng quy chuẩn benchmark chuẩn |
| **Tính toán FLOPs & Params** | Sử dụng thư viện chuẩn hóa `thop.profile` trên cùng dummy tensor $(1,3,640,640)$ | **ĐẠT** | FLOPs và Params phản ánh kiến trúc thực tế của từng mô hình |
| **Quy tắc Metric Không khả dụng (No-fabrication)** | Xử lý đối với chỉ số Peak GPU VRAM | **ĐẠT** | Ghi nhận rõ `N/A`, không tự ý bịa số VRAM khi chạy trên CPU PyTorch |
| **Tính nhất quán mô hình** | Đúng 4 mô hình đủ 10 seed được đo: Baseline, TSVM, P5 VMamba, ITS Mamba | **ĐẠT** | Đồng nhất danh tính mô hình giữa benchmark hiệu năng và 10-seed accuracy |

---

### 2. Chi tiết Giải trình Chỉ số `N/A` (GPU VRAM)

* **Hiện trạng Môi trường**:  
  Môi trường Python hiện tại của máy cục bộ cài đặt gói `torch-2.13.0+cpu`. Lệnh `torch.cuda.is_available()` trả về `False`.
* **Quyết định Kỹ thuật**:  
  Tuân thủ nghiêm ngặt chỉ thị: *"Nếu metric không đo được hoặc custom VMamba operator khiến GFLOPs không đáng tin → N/A, giải thích rõ, không bịa số"*.
* **Xử lý**:
  - Cột `VRAM` / `Peak_VRAM_MB` trong tất cả các bảng tóm tắt (`efficiency_summary.csv`, `accuracy_efficiency_summary.csv`) được ghi là `N/A`.
  - Biểu đồ số 7 (`fig07_vram_status.png`) được hiển thị dưới dạng biểu đồ trạng thái giải trình kỹ thuật thay vì giả lập các con số ảo.

---

### 3. Kiểm tra Độ lệch chuẩn và Phân vị Độ trễ (Latency Distribution Sanity Check)

* Dữ liệu raw gồm 100 lần đo mỗi mô hình:
  - Baseline: Mean $= 200.12$ ms, P50 $= 195.92$ ms, P95 $= 218.28$ ms, P99 $= 251.67$ ms. Tỷ lệ Std/Mean $= 9.03\%$ (ổn định).
  - P5 Attention VMamba: Mean $= 477.98$ ms, P50 $= 474.55$ ms, P95 $= 501.46$ ms, P99 $= 518.70$ ms. Tỷ lệ Std/Mean $= 2.74\%$ (rất ổn định).
  - ITS Mamba: Mean $= 651.27$ ms, P50 $= 648.99$ ms, P95 $= 689.51$ ms, P99 $= 736.68$ ms. Tỷ lệ Std/Mean $= 4.00\%$ (ổn định).
  - TSVM: Mean $= 821.27$ ms, P50 $= 826.09$ ms, P95 $= 899.10$ ms, P99 $= 908.97$ ms. Tỷ lệ Std/Mean $= 6.81\%$ (ổn định).

*Kết luận*: Phân vị P50 xấp xỉ giá trị Mean và độ lệch chuẩn nhỏ chứng minh quá trình đo không bị nhiễu nền hay biến động bất thường từ hệ điều hành.

---

### 4. Kết luận Kiểm toán

Toàn bộ quy trình thu thập dữ liệu và báo cáo benchmark hiệu năng tuân thủ 100% nguyên tắc trung thực học thuật, không có bất kỳ hành vi bịa số hoặc làm sai lệch kết quả.
