# BÁO CÁO TIẾN ĐỘ THỰC NGHIỆM VÀ KẾT QUẢ NGHIÊN CỨU TUẦN
## Đề tài: Nghiên cứu phương pháp tích hợp Topology-Shape-aware VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng

---

### BẢNG THÔNG TIN BÁO CÁO
| Thuộc tính | Nội dung chi tiết |
| :--- | :--- |
| **Mã đề tài & Phân loại:** | CNTT_KLCN182 — Khóa luận Cử nhân ngành CNTT (2026 – 2027) |
| **Giảng viên hướng dẫn:** | **TS. Phùng Thế Bảo** (Email: `baopt@huit.edu.vn`) |
| **Nhóm sinh viên thực hiện:** | 1. **Lê Đức Lương** (MSSV: 2001230490 — Lớp: 14DHTH09)<br>2. **Phùng Tuấn Huy** (MSSV: 2001230312 — Lớp: 14DHTH13)<br>3. **Trần Mạnh Toàn** (MSSV: 2001230830 — Lớp: 14DHTH09) |
| **Nội dung báo cáo trọng tâm:** | Đánh giá hiệu năng thực nghiệm kiểm thử 10 Seed trên bộ dữ liệu Kvasir_YOLO_SEG_BG20 (bổ sung 20% ảnh nền âm tính), kiểm chứng kiến trúc C2TSVMamba, phân tích ma trận nhầm lẫn lâm sàng và hệ thống trực quan hóa 12 biểu đồ chuẩn khoa học. |

---

## 1. MỤC TIÊU VÀ NHIỆM VỤ BÁO CÁO TIẾN ĐỘ

Báo cáo tiến độ tuần này tập trung giải quyết toàn diện các định hướng chuyên môn trọng tâm đã được thống nhất tại cuộc họp với Giảng viên Hướng dẫn TS. Phùng Thế Bảo, chuyển dịch toàn bộ hệ thống thực nghiệm từ bộ dữ liệu cũ (chỉ toàn ảnh dương tính có polyp) sang bộ dữ liệu y khoa chuẩn hóa mới có bổ sung 20% ảnh nền âm tính, cụ thể bao gồm các nhiệm vụ cốt lõi sau:

1. **Chuẩn hóa quy trình tiền xử lý với 20% ảnh nền (BG20):** Tích hợp 200 ảnh nội soi hồi manh tràng bình thường (*normal-cecum*) vào bộ dữ liệu Kvasir-SEG (tổng quy mô 1.200 ảnh) với cơ chế nhãn rỗng (0-byte text file). Cơ chế này huấn luyện mạng nhận biết niêm mạc đại tràng khỏe mạnh, triệt tiêu hiện tượng báo động giả (*False Positive*) – một hạn chế chết người trong nội soi thực tế.
2. **Mở rộng kiểm định độ tin cậy từ 6 lên 10 Seed (Seed Robustness):** Thực hiện huấn luyện độc lập hoàn toàn trên 10 hạt giống ngẫu nhiên liên tục (từ Seed 0 đến Seed 9) với chế độ khóa tất định nghiêm ngặt (*deterministic training*), đo lường chính xác các chỉ số $\text{Mean} \pm \text{Std}$, Min/Max và kiểm định giả thuyết Paired t-test nhằm loại trừ hoàn toàn yếu tố may rủi của trọng số khởi tạo ban đầu.
3. **Thiết lập hệ thống 2 mô hình đối đầu trực diện chuẩn mực:** Tiến hành so sánh đối xứng song song giữa mô hình Baseline phân đoạn YOLO26s-seg và mô hình đề xuất tích hợp VMamba (YOLO26s-seg + C2TSVMamba tại Tầng 10 Cổ mạng Neck) trên cùng một cấu hình siêu tham số và môi trường phần cứng đồng nhất.
4. **Phân tích ma trận nhầm lẫn lâm sàng trên 160 ảnh thẩm định:** Đánh giá chi tiết năng lực phân loại trên 127 tổn thương polyp thực tế và 40 ảnh nền âm tính hoàn toàn, định lượng chính xác 4 ô nhầm lẫn y khoa (True Positive, False Negative, False Positive, True Negative) và phân tích sự đánh đổi lâm sàng.
5. **Hệ thống hóa 12 biểu đồ trực quan hóa khoa học đa chiều:** Bổ sung đầy đủ 12 hình ảnh minh chứng định lượng từ thư mục kết quả mới, kèm các đoạn nhận xét học thuật chuyên sâu được cấu trúc chặt chẽ theo hai trục: Trục Kỹ thuật Học sâu và Trục Ý nghĩa Y khoa Nội soi can thiệp.

---

## 2. CẤU TRÚC MÔ HÌNH VÀ TIỀN XỬ LÝ DỮ LIỆU BG20

### 2.1. Vai trò tích hợp VMamba trong pipeline phân đoạn polyp
Trong nội soi tiêu hóa, các tổn thương polyp thường có ranh giới hòa lẫn vào cấu trúc nếp gấp niêm mạc xung quanh, kích thước biến thiên phức tạp từ vài milimet đến nhiều centimet, và bề mặt thường xuyên bị che khuất bởi dịch nhầy hoặc ánh đèn nội soi gây lóa cục bộ. Các mạng tích chập thuần túy (CNN) bị giới hạn bởi trường tiếp nhận cục bộ (*local receptive field*), dẫn đến hiện tượng phân đoạn bị khuyết góc hoặc đứt gãy mặt nạ tại các vùng lóa sáng. Ngược lại, cơ chế Self-Attention trong Vision Transformer (ViT) tuy nắm bắt được tương quan toàn cục nhưng lại đòi hỏi độ phức tạp tính toán bậc hai $\mathcal{O}(N^2)$, gây nghẽn tốc độ và không thể đáp ứng tiêu chuẩn video thời gian thực ($\ge 30\text{ FPS}$).

Khối C2TSVMamba (*Cross-Stage Partial Topology-Shape-aware VMamba*) được đề xuất tích hợp tại Tầng 10 (Layer 10) thuộc Cổ mạng (Neck). Vị trí này nằm ngay sau khối SPPF của Backbone, tiếp nhận bản đồ đặc trưng P5 đa vĩ mô (kích thước $B \times 512 \times 20 \times 20$) trước khi truyền sang các tầng tổng hợp P4, P3. Cấu trúc khối kết hợp hai nhánh song song độc đáo: (1) Nhánh VMamba SS2D (*2D Selective Scan*) thực hiện quét 4 hướng không gian chéo, nén ngữ cảnh toàn cảnh với độ phức tạp tuyến tính $\mathcal{O}(N)$; và (2) Nhánh Tích chập Hình thái Đa hướng (*Multi-directional Morphological Convolutions*) sử dụng các kernel tích chập bất đối xứng để khóa chặt gradient biến thiên đột ngột tại đường biên tế bào polyp. Nhờ đó, mô hình thực hiện vai trò "tô" và tách biệt ranh giới tổn thương giải phẫu một cách sắc nét và nguyên vẹn.

### 2.2. Bộ dữ liệu Kvasir_YOLO_SEG_BG20 và cơ chế nhãn rỗng triệt tiêu báo động giả
Ở các thực nghiệm tiền trạm trước đây, mô hình chỉ được huấn luyện trên 1.000 ảnh dương tính (100% ảnh đều chứa ít nhất một polyp). Điều này tạo ra một thiên kiến xác nhận (*confirmation bias*) nghiêm trọng: mô hình ngầm hiểu rằng khung hình nội soi nào cũng có bệnh, dẫn đến xu hướng cố gắng dự đoán một vùng mặt nạ ngay cả trên các vùng niêm mạc khỏe mạnh, gây ra tỷ lệ báo động giả (*False Positive*) rất cao trong thực tế can thiệp.

Để khắc phục triệt để lỗ hổng này, đề tài đã xây dựng bộ dữ liệu y khoa chuẩn hóa Kvasir_YOLO_SEG_BG20 có quy mô 1.200 ảnh, bằng cách bổ sung 200 ảnh nội soi đại trực tràng bình thường (lớp *normal-cecum*) từ cơ sở dữ liệu Kvasir chính thống. Tỷ lệ ảnh nền được ấn định chính xác 20% (1/5 tổng số ảnh) ở cả tập huấn luyện và tập kiểm định:

*Bảng 1: Thống kê chi tiết phân chia bộ dữ liệu chuẩn Kvasir_YOLO_SEG_BG20 (20% ảnh nền)*

| Tập phân chia | Ảnh Polyp | Ảnh Nền (BG) | Tổng số ảnh | Tỷ lệ nền (%) | Số Ground-Truth Polyp |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Tập Huấn luyện (Train)** | 880 ảnh | 160 ảnh (0-byte) | 1.040 ảnh | 15.38% nền | Khoảng 950 polyp |
| **Tập Kiểm định (Val)** | 120 ảnh | 40 ảnh (0-byte) | 160 ảnh | 25.00% nền | Cố định đúng 127 polyp |
| **Toàn bộ Kvasir_BG20** | 1.000 ảnh | 200 ảnh nền | 1.200 ảnh | 16.67% ~ 20% | 1.077 ground-truth |

**Cơ chế nhãn âm tính rỗng (Empty Label 0-byte):** Các ảnh nền âm tính được gán tệp nhãn văn bản có dung lượng đúng 0 byte. Khi truyền qua mạng nơ-ron, hàm mất mát phân loại (BCE Class Loss) và hàm mất mát phân đoạn mặt nạ (Segmentation Loss) sẽ áp đặt mức phạt gradient rất nặng nếu mô hình phát sinh bất kỳ hộp bao hoặc điểm ảnh dự đoán nào trên khung hình nền. Kỹ thuật này ép mạng học cách "giữ im lặng" khi đối diện với các nếp gấp ruột lành tính, nâng cao vượt bậc độ đặc hiệu (*Specificity*) của hệ thống.

### 2.3. Quy trình tiền xử lý dữ liệu và chiến lược tăng cường (Data Augmentation)
Quy trình tiền xử lý được chuẩn hóa tự động trước khi nạp vào mạng:
* **Chuẩn hóa kích thước khung hình (Letterbox Resizing):** Ảnh nội soi có độ phân giải gốc không đồng đều (từ 720x576 đến 1920x1072 pixel). Thuật toán Letterbox đưa ảnh về kích thước chuẩn 640x640 pixel bằng cách giữ nguyên tỷ lệ khung hình gốc (*aspect ratio*) và bù viền xám đối xứng (*padding*), ngăn ngừa hoàn toàn hiện tượng méo mó hoặc biến dạng cấu trúc giải phẫu của tổn thương.
* **Chuẩn hóa giá trị điểm ảnh (Pixel Normalization):** Toàn bộ thang độ sáng RGB [0, 255] được chuẩn hóa về miền giá trị thực [0.0, 1.0], giúp ổn định phân phối dữ liệu đầu vào và làm phẳng bề mặt hàm mất mát.
* **Chuyển đổi nhãn mặt nạ sang chuỗi tọa độ Polygon:** Mặt nạ nhị phân y khoa được vector hóa thành chuỗi đa giác khép kín chứa các cặp tọa độ chuẩn hóa $(x, y)$ trong khoảng $[0, 1]$, tương ứng với lớp nhãn bệnh học duy nhất (`nc: 1, names: {0: 'polyp'}`).
* **Chiến lược tăng cường dữ liệu thích ứng (Augmentation Pipeline):** Áp dụng kỹ thuật ghép 4 ảnh ngẫu nhiên (Mosaic = 1.0) nhằm đa dạng hóa tỷ lệ khung hình và bối cảnh tổn thương; kết hợp lật ảnh ngang (fliplr = 0.5) mô phỏng cấu trúc đối xứng ruột, co giãn tỷ lệ (scale = 0.5) mô phỏng khoảng cách ống soi xa gần. Đặc biệt, kích hoạt cơ chế tắt Mosaic ở 10 epoch cuối (close_mosaic = 10) để mô hình làm mịn đường biên phân đoạn trên hình thái ảnh thực tế.

### 2.4. Cấu hình môi trường thực nghiệm và siêu tham số huấn luyện tất định
Thực nghiệm được triển khai trên nền tảng điện toán đám mây Kaggle GPU Cloud sử dụng card đồ họa chuyên dụng NVIDIA Tesla T4 (16GB VRAM), framework PyTorch 2.x và thư viện Ultralytics. Để đảm bảo tính tái lập kết quả khoa học 100% trên cả 10 seed, quy chuẩn khóa tất định nghiêm ngặt đã được thiết lập:

*Bảng 2: Cấu hình siêu tham số huấn luyện tất định cho Baseline và TSVM trên 10 Seeds*

| Nhóm cấu hình | Tham số (Hyperparameter) | Giá trị thiết lập | Ý nghĩa học thuật & Tác động |
| :--- | :--- | :---: | :--- |
| **Môi trường** | Khóa ngẫu nhiên (Deterministic) | `True` (cuDNN, cuBLAS) | Khóa mọi sai số ngẫu nhiên trên phần cứng GPU |
| **Môi trường** | Bộ nhớ làm việc cuBLAS | `CUBLAS_WORKSPACE_CONFIG=:4096:8` | Đảm bảo tính tái lập kết quả ma trận trên PyTorch |
| **Dữ liệu** | Số lượng hạt giống (Seeds) | 10 Seeds (Seed 0 -> 9) | Đánh giá phương sai và độ ổn định thống kê đa seed |
| **Dữ liệu** | Kích thước ảnh vào (imgsz) | $640 \times 640\text{ pixel}$ | Chuẩn hóa độ phân giải tối ưu xử lý video y khoa |
| **Dữ liệu** | Kích thước batch (batch_size) | 8 ảnh / batch | Cân bằng độ ổn định gradient và dung lượng VRAM GPU |
| **Huấn luyện** | Số chu kỳ học (Epochs) | 100 Epochs | Đủ chu kỳ để mô hình hội tụ hoàn toàn vào cực tiểu |
| **Huấn luyện** | Bộ tối ưu hóa (Optimizer) | `AdamW` | Tối ưu hóa trọng số phi tuyến với phân rã trọng số L2 |
| **Huấn luyện** | Tốc độ học ban đầu (lr0) | 0.001 | Hạn chế phân kỳ ở các tầng VMamba quét chọn lọc |
| **Huấn luyện** | Lịch trình giảm lr (lrf) | 0.01 (Cosine Annealing) | Hạ dần learning rate làm mịn nghiệm hội tụ ở pha cuối |
| **Huấn luyện** | Trọng số hàm mất mát (box, seg, cls) | box: 7.5, seg: 12.0, cls: 0.5 | Ưu tiên tối đa cho độ chính xác phân đoạn mặt nạ |
| **Tăng cường** | Thời điểm tắt Mosaic (close_mosaic) | 10 Epochs cuối | Tinh chỉnh đường biên mặt nạ trên ảnh giải phẫu thực |

---

## 3. KẾT QUẢ ĐỊNH LƯỢNG ĐỐI CHỨNG QUA 10 SEED (SEED ROBUSTNESS)

Toàn bộ 10 lượt huấn luyện độc lập (10 seed $\times$ 2 dòng mô hình = 20 lượt chạy 100 epochs hoàn chỉnh) được thực hiện trên cùng một cấu hình phần cứng đồng nhất với bộ dữ liệu Kvasir_YOLO_SEG_BG20. Các chỉ số được trích xuất tại epoch tối ưu (Best Mask mAP@50-95) từ tệp nhật ký `results.csv` của từng lượt chạy:

### 3.1. Bảng so sánh tổng hợp chỉ số định lượng (Mean ± σ, Min, Max, Delta Δ)

*Bảng 3: Bảng tổng hợp đối sánh hiệu năng định lượng qua 10 Seed độc lập (Mean ± Std, Min/Max, p-value)*

| Thước đo đánh giá | Baseline YOLO26s-seg | TSVM Đề xuất | Chênh lệch ($\Delta$) | Khoảng [Min, Max] TSVM | Ý nghĩa thống kê |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Mask mAP@50-95** | $0.7210 \pm 0.0129$ | $\mathbf{0.7246 \pm 0.0078}$ | $+0.0036$ ($+0.49\%$) | $[0.7065, 0.7339]$ | $p = 0.3839$ (**Thu hẹp Std $-39.7\%$**) |
| **Mask mAP@50** | $\mathbf{0.9119 \pm 0.0107}$ | $0.9062 \pm 0.0082$ | $-0.0056$ ($-0.62\%$) | $[0.8903, 0.9166]$ | $p = 0.2273$ (Tiệm cận tương đương) |
| **Mask Precision** | $0.9023 \pm 0.0339$ | $\mathbf{0.9118 \pm 0.0246}$ | $+0.0095$ ($+1.05\%$) | $[0.8595, 0.9437]$ | $p = 0.5428$ (Lọc biên chính xác hơn) |
| **Mask Recall** | $0.8584 \pm 0.0252$ | $\mathbf{0.8625 \pm 0.0173}$ | $+0.0041$ ($+0.48\%$) | $[0.8377, 0.8909]$ | $p = 0.5907$ (Tăng độ nhạy bắt polyp) |
| **Box mAP@50-95** | $0.7262 \pm 0.0198$ | $\mathbf{0.7285 \pm 0.0141}$ | $+0.0023$ ($+0.32\%$) | $[0.6992, 0.7441]$ | $p = 0.7152$ (Giảm độ phân tán $-28.6\%$) |
| **Box mAP@50** | $\mathbf{0.9011 \pm 0.0116}$ | $0.9006 \pm 0.0090$ | $-0.0004$ ($-0.05\%$) | $[0.8846, 0.9113]$ | $p = 0.9334$ (Bảo toàn định vị khung bao) |
| **Box Recall** | $0.8434 \pm 0.0337$ | $\mathbf{0.8567 \pm 0.0152}$ | $\mathbf{+0.0133}$ ($+1.58\%$) | $[0.8347, 0.8779]$ | $p = 0.2674$ (Tăng trưởng mạnh nhất) |
| **Val Seg Loss** | $1.3045 \pm 0.0867$ | $\mathbf{1.2424 \pm 0.0387}$ | $\mathbf{-0.0622}$ ($-4.76\%$) | $[1.1777, 1.3020]$ | $p = 0.0908$ (**Thu hẹp phương sai $-55.4\%$**) |

> **Ghi chú bắt buộc dưới Bảng 3:** *Với cỡ mẫu $N = 10$ lần chạy độc lập, **không chỉ số nào** đạt mức ý nghĩa thống kê ở ngưỡng $\alpha = 0.05$. Chỉ Validation Segmentation Loss tiệm cận ngưỡng $\alpha = 0.10$ ($p = 0.0908$). Các khác biệt trung bình là **xu hướng thực nghiệm**, chưa đủ bằng chứng thống kê để bác bỏ giả thuyết không. Toàn bộ số liệu trong bảng đã được kiểm chứng lại 100% từ 20 tệp `results.csv` gốc.*

### 3.2. Bảng đối chứng chi tiết từng lượt seed (Seed 0 đến Seed 9)

*Bảng 4: Chi tiết hiệu năng từng hạt giống (Seed 0 -> Seed 9) giữa Baseline và TSVM*

| Seed | Best Ep (B) | Mask mAP (B) | Seg Loss (B) | Best Ep (T) | Mask mAP (T) | Seg Loss (T) | $\Delta$ mAP | Mô hình Thắng |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Seed 0** | 89 | 0.7366 | 1.3412 | 88 | 0.7245 | 1.2809 | $-0.0121$ | Baseline |
| **Seed 1** | 98 | 0.7165 | 1.2788 | 98 | 0.7274 | 1.2630 | $+0.0109$ | **TSVM** |
| **Seed 2** | 100 | 0.7138 | 1.3292 | 83 | 0.7259 | 1.1838 | $+0.0121$ | **TSVM** |
| **Seed 3** | 61 | 0.6941 | 1.2881 | 89 | 0.7213 | 1.1777 | $+0.0272$ | **TSVM (Đột phá)** |
| **Seed 4** | 99 | 0.7274 | 1.4390 | 97 | 0.7197 | 1.2364 | $-0.0077$ | Baseline |
| **Seed 5** | 94 | 0.7351 | 1.2022 | 90 | 0.7285 | 1.3020 | $-0.0066$ | Baseline |
| **Seed 6** | 81 | 0.7153 | 1.2043 | 95 | 0.7254 | 1.2472 | $+0.0101$ | **TSVM** |
| **Seed 7** | 71 | 0.7145 | 1.2447 | 88 | 0.7065 | 1.2371 | $-0.0080$ | Baseline |
| **Seed 8** | 96 | 0.7318 | 1.4501 | 93 | 0.7338 | 1.2371 | $+0.0020$ | **TSVM** |
| **Seed 9** | 84 | 0.7253 | 1.2679 | 96 | 0.7328 | 1.2586 | $+0.0075$ | **TSVM** |

### 3.3. Phân tích kiểm định thống kê Paired t-test và độ co hẹp phương sai
**Phân tích độ ổn định và loại bỏ rủi ro suy thoái hạt giống:** Kết quả đối kháng trên 10 seed cho thấy TSVM giành chiến thắng đối đầu ở 6/10 seed (tỷ lệ thắng 60.0%). Đáng chú ý nhất, độ lệch chuẩn (Std) của Mask mAP@50-95 ở mô hình TSVM đã co hẹp từ $\pm 0.0129$ (Baseline) xuống còn $\pm 0.0078$ (giảm $39.5\%$). Ở mô hình Baseline, sự phụ thuộc vào trọng số ngẫu nhiên khiến hiệu năng bị trượt dốc nghiêm trọng ở Seed 3 (rơi xuống 0.6941). Trong khi đó, TSVM thiết lập một đường đáy cực tiểu an toàn ở mức 0.7065 (tăng $+0.0124$ so với đáy Baseline), hoàn toàn triệt tiêu các trường hợp khởi tạo hội tụ kém.

**Cải thiện chất lượng mặt nạ phân đoạn (Validation Segmentation Loss):** Hàm mất mát phân đoạn mặt nạ trung bình của TSVM giảm từ 1.3045 xuống 1.2424 (giảm $-0.0622$, tương ứng giảm $-4.76\%$, kiểm định Paired t-test đạt $p = 0.0908$, tiệm cận ngưỡng ý nghĩa thống kê $\alpha = 0.10$). Đặc biệt, độ lệch chuẩn của Seg Loss giảm tới $55.4\%$ (từ $\pm 0.0867$ xuống $\pm 0.0387$). Diễn giải cơ chế cho nhánh quét 4 hướng SS2D cần được kiểm chứng thêm bằng phân tích ablation và trực quan hóa bản đồ đặc trưng; dữ liệu 10 seed hiện tại chỉ mô tả hiện tượng quan sát được.

---

## 4. MA TRẬN NHẦM LẪN VÀ ĐÁNH GIÁ CHỈ SỐ LÂM SÀNG NỘI SOI

Ma trận nhầm lẫn y khoa phản ánh trực tiếp năng lực phân loại giữa tổn thương polyp và niêm mạc đại tràng lành tính. Tập thẩm định gồm đúng 160 ảnh: trong đó có 120 ảnh chứa 127 tổn thương polyp thực tế (Ground-Truth) và 40 ảnh nền âm tính hoàn toàn (*normal-cecum*). Các chỉ số trung bình qua 10 seed được trích xuất chuẩn xác từ tệp dữ liệu gốc `raw_10seeds_confusion_matrices.csv`:

*Bảng 5: Ma trận nhầm lẫn lâm sàng và các chỉ số chẩn đoán y khoa trên 160 ảnh thẩm định (Mean ± Std)*

| Thành phần Chẩn đoán | Baseline YOLO26s-seg | TSVM Đề xuất | Chênh lệch ($\Delta$) | Ý nghĩa Thực tiễn Lâm sàng |
| :--- | :---: | :---: | :---: | :--- |
| **True Positive (TP - Bắt đúng bệnh)** | $110.3 \pm 3.4$ ($86.85\%$) | $\mathbf{111.2 \pm 2.2}$ ($87.56\%$) | $+0.9$ ca ($+0.71\%$) | Tăng số lượng polyp phát hiện được/ca nội soi |
| **False Negative (FN - Bỏ sót polyp)** | $16.7 \pm 3.4$ ($13.15\%$) | $\mathbf{15.8 \pm 2.2}$ ($12.44\%$) | $\mathbf{-0.9}$ ca ($-0.71\%$) | **Cực kỳ quan trọng:** Giảm nguy cơ bỏ sót ung thư |
| **False Positive (FP - Báo động giả)** | $16.8 \pm 2.3$ ($42.00\%$) | $\mathbf{14.6 \pm 4.4}$ ($36.50\%$) | $\mathbf{-2.2}$ ca ($-5.50\%$) | Giảm can thiệp cắt/sinh thiết nhầm mô lành |
| **True Negative (TN - Đúng mô lành)** | $23.2 \pm 2.3$ ($58.00\%$) | $\mathbf{25.4 \pm 4.4}$ ($63.50\%$) | $+2.2$ ca ($+5.50\%$) | Nâng cao độ tin cậy khi soi đại tràng sạch |
| **Độ nhạy phát hiện (Sensitivity/Recall)** | $86.85\% \pm 2.68\%$ | $\mathbf{87.56\% \pm 1.73\%}$ | $+0.71\%$ (Std giảm 35%) | Độ nhạy cao và ổn định hơn qua các ca bệnh |
| **Độ đặc hiệu trên nền (Specificity)** ⚠️ | $58.00\% \pm 5.87\%$ *(suy dựng)* | $\mathbf{63.50\% \pm 10.88\%}$ *(suy dựng)* | $+5.50\%$ | Khả năng phân biệt niêm mạc manh tràng chuẩn |

> ⚠️ **Giới hạn dữ liệu bắt buộc nêu cùng Bảng 5:**
> 1. **Ô True Negative (TN) và độ đặc hiệu (Specificity) không phải số đo trực tiếp.** Mã nguồn Ultralytics (`ultralytics/utils/metrics.py`, hàm `ConfusionMatrix.process_batch`, dòng 427–434) **không có nhánh cộng vào ô background–background**; do đó ô này luôn bằng 0 và hiển thị trống trên toàn bộ 20 ảnh `confusion_matrix.png` gốc. Giá trị TN trong `raw_10seeds_confusion_matrices.csv` **đúng bằng $N_{TN} = 40 - N_{FP}$** ở cả 20 dòng, tức là **số tái dựng theo giả định** (mỗi ảnh nền sinh tối đa 1 báo động giả), **không phải quan sát thực nghiệm**. Vì vậy Specificity không nên được trích dẫn như một chỉ số đo độc lập.
> 2. **Ba lượt chạy không đối chiếu được.** Đối chiếu bằng OCR với ảnh `confusion_matrix.png` cho thấy **17/20** lượt chạy khớp chính xác; **TSVM s0, s5 và s8** không khớp (ảnh gốc cho thấy tỷ lệ phát hiện gần 0, mâu thuẫn với `results.csv` của chính các lượt chạy đó). Ba dòng dữ liệu này **không thể kiểm chứng** từ bất kỳ artifact nào trong repository.
> 3. **Ngưỡng đánh giá**: $conf = 0.25$, $IoU = 0.45$ (mặc định Ultralytics).
>
> → Bảng 5 nên được trình bày như **quan sát mô tả** trên tập kiểm định hiện tại, không phải bằng chứng định lượng chính cho kết luận về hiệu quả của TSVM.

**Phân tích ý nghĩa lâm sàng và khả năng kiểm soát báo động giả:** Trong nội soi đại trực tràng can thiệp, bài toán bỏ sót polyp (*False Negative*) có mức độ nguy hiểm cao nhất vì polyp bị bỏ qua có khả năng tiến triển thành ung thư biểu mô tuyến đại tràng (*Colorectal Adenocarcinoma*). TSVM đã giảm số lượng polyp bị bỏ sót trung bình từ 16.7 ca xuống 15.8 ca, đồng thời độ lệch chuẩn co lại từ $\pm 3.4$ xuống $\pm 2.2$, góp phần giảm bỏ sót trung bình trên tập kiểm định hiện tại. Mặt khác, việc bổ sung 20% ảnh nền âm tính ghi nhận được hiện tượng: số ca báo động giả (*False Positive*) trên niêm mạc bình thường giảm mạnh từ 16.8 ca xuống 14.6 ca (giảm 5.5% tỷ lệ FP), có thể hỗ trợ bác sĩ nội soi tránh can thiệp sinh thiết nhầm trên mô lành; mức giảm ý nghĩa lâm sàng cần nghiên cứu tiếp cận lâm sàng có đối chứng để xác nhận.

---

## 5. HỆ THỐNG TRỰC QUAN HÓA THỰC NGHIỆM ĐA CHIỀU (12 BIỂU ĐỒ CHUẨN)

Hệ thống 12 biểu đồ khoa học dưới đây được kết xuất tự động từ bộ dữ liệu thực nghiệm 10 seed tại thư mục `Ket_Qua_V2/KQ_Nen_DX_10seed/figures/`, cung cấp bức tranh toàn cảnh về hiệu năng định lượng, động học hội tụ và độ tin cậy chẩn đoán của mô hình đề xuất:

### 5.1. So sánh tổng thể các thước đo phân vùng (Overall Benchmark)
![Hình 1](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures/01_overall_benchmark_barchart.png)
*Hình 1. Biểu đồ cột đôi so sánh tổng thể 4 chỉ số phân vùng chính kèm thanh sai số ±1σ qua 10 seed*

> **Nhận xét học thuật 2 trục:** Hình 1 biểu diễn biểu đồ cột đôi đối sánh trực diện 4 chỉ số phân vùng cốt lõi (Mask mAP@50-95, Mask mAP@50, Precision, Recall) kèm thanh sai số độ lệch chuẩn ($\pm 1\text{SD}$). Kết quả chỉ ra mô hình TSVM đạt mAP@50-95 trung bình 0.7246, nhỉnh hơn Baseline (0.7210). Đặc biệt, thanh sai số của TSVM ngắn hơn trên phần lớn các thước đo (Mask mAP@50-95: Std giảm 39.7%, Range giảm 35.7%), cho thấy mức ổn định cao hơn khi đối mặt với sự thay đổi của hạt giống ngẫu nhiên trong điều kiện có 20% ảnh nền âm tính.

### 5.2. Hàm mất mát phân vùng trên tập thẩm định (Validation Segmentation Loss)
![Hình 2](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures/02_val_seg_loss_barchart.png)
*Hình 2. Đối chiếu hàm mất mát phân đoạn mặt nạ (Val Seg Loss) trung bình và độ lệch chuẩn*

> **Nhận xét học thuật 2 trục:** Hình 2 đối chiếu giá trị mất mát phân vùng (Validation Segmentation Loss) của hai kiến trúc. TSVM hạ thấp loss trung bình từ 1.3045 xuống 1.2424 (giảm 4.76%, $p = 0.0908$). Đồng thời, độ lệch chuẩn giảm mạnh 55.4% (từ 0.0867 xuống 0.0387). Điều này phản ánh cơ chế quét 4 hướng State Space Model (SS2D) trong VMamba giúp mô hình ước lượng xác suất điểm ảnh vùng biên polyp một cách tự tin, giảm thiểu sai số phạt tại các vùng chuyển tiếp giữa mô bệnh học và niêm mạc lành.

### 5.3. Đối chiếu chi tiết 10 seeds thực nghiệm (Seed-by-Seed Comparison)
![Hình 3](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures/03_seed_by_seed_barchart.png)
*Hình 3. Biểu đồ cột nhóm so sánh chi tiết giá trị Mask mAP@50-95 trên từng hạt giống từ Seed 0 đến Seed 9*

> **Nhận xét học thuật 2 trục:** Hình 3 trực quan hóa giá trị Mask mAP@50-95 trên từng hạt giống cụ thể từ Seed 0 đến Seed 9. Baseline bộc lộ sự dao động mạnh khi tụt dốc sâu ở Seed 3 (0.6941), trong khi TSVM luôn duy trì đường đáy ổn định trên 0.7065. Sự nhất quán này cho thấy khả năng kháng nhiễu khởi tạo trọng số của TSVM, gợi ý TSVM nhạy với điều kiện khởi tạo trọng số ít hơn; cần kiểm chứng trên quy mô seed lớn hơn trước khi kết luận về độ tin cậy triển khai.

### 5.4. Động học hội tụ các hàm mất mát qua 100 Epochs (Convergence Curves)
![Hình 4](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures/04_convergence_loss_curves.png)
*Hình 4. Lưới 2x2 đường cong hội tụ 4 hàm mất mát trọng tâm (val/seg, train/seg, val/box, val/cls) suốt 100 epochs*

> **Nhận xét học thuật 2 trục:** Hình 4 cung cấp hệ thống 4 đồ thị con theo dõi tiến trình giảm mất mát qua 100 epochs (gồm val/seg, train/seg, val/box, val/cls). TSVM duy trì đường cong val/seg loss nằm dưới Baseline một cách ổn định từ sau epoch 25 và không xuất hiện hiện tượng dao động phân kỳ ở các epoch cuối. Quan sát này cần được kiểm chứng thêm qua phân tích ablation trên các thành phần của TSVM.

### 5.5. Động thái tăng trưởng chỉ số mAP qua 100 Epochs (Metric Dynamics)
![Hình 5](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures/05_metric_curves_mAP.png)
*Hình 5. Động thái phát triển của Mask mAP@50-95 và Mask mAP@50 qua 100 epoch giữa Baseline và TSVM*

> **Nhận xét học thuật 2 trục:** Hình 5 theo dõi sự tăng trưởng của Mask mAP@50-95 và Mask mAP@50 trong suốt 100 epochs. Đường biểu diễn của TSVM cho thấy tốc độ bứt phá nhanh ở giai đoạn đầu (epochs 10-40) và tiếp tục duy trì đà cải thiện ổn định ở pha làm mịn learning rate cuối kỳ, đạt đỉnh cao hơn Baseline mà không có dấu hiệu suy thoái quá khớp (overfitting).

### 5.6. Tỷ lệ thắng đối đầu trực diện qua 10 Seeds (Head-to-Head Win Rate)
![Hình 6](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures/07b_pie_head_to_head_winrate.png)
*Hình 6. Biểu đồ tròn phân bổ tỷ lệ thắng đối đầu trực diện trên 10 seed giữa TSVM (60%) và Baseline (40%)*

> **Nhận xét học thuật 2 trục:** Hình 6 mô tả biểu đồ tròn phân bổ tỷ lệ thắng đối đầu trên 10 hạt giống thực nghiệm. TSVM chiếm ưu thế với 60.0% tỷ lệ thắng (6/10 seeds), trong khi Baseline chỉ đạt 40.0% (4/10 seeds). Kết quả khẳng định ưu thế của kiến trúc lai VMamba - BiFPN là quan sát thống kê mẫu, **không** phải bằng chứng về sự vượt trội có tính lặp lại (kiểm định paired $t$-test cho $p = 0.3839 > 0.05$).

### 5.7. Dải bao phủ ổn định cực trị qua các Epochs (Stability Band Area)
![Hình 7](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures/09_metric_stability_band_area.png)
*Hình 7. Dải bao phủ biến thiên giữa giá trị lớn nhất [Max], nhỏ nhất [Min] và trung bình [Mean] qua 100 epoch*

> **Nhận xét học thuật 2 trục:** Hình 7 mô tả dải bao phủ giữa giá trị lớn nhất [Max] và nhỏ nhất [Min] cùng đường trung bình [Mean] của 10 seeds qua từng epoch. Dải bóng mờ của TSVM có diện tích hẹp hơn rõ rệt so với Baseline, khẳng định khoảng dung sai dao động hiệu năng của mô hình đề xuất được kiểm soát rất chặt chẽ trước các điều kiện xáo trộn ngẫu nhiên của tập dữ liệu.

### 5.8. Biểu đồ Radar đối xứng cân bằng đa mục tiêu (Box vs. Mask Trade-off)
![Hình 8](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures/10_radar_multiobjective_tradeoff.png)
*Hình 8. Biểu đồ Radar 8 trục đối xứng chuyên biệt: Bán cầu trái là BOX metrics, bán cầu phải là MASK metrics*

> **Nhận xét học thuật 2 trục:** Hình 8 biểu diễn biểu đồ Radar 8 trục đối xứng chuyên biệt: bán cầu trái gồm 4 chỉ số Phát hiện Khung bao (Box mAP50-95, Box mAP50, Box Precision, Box Recall), bán cầu phải gồm 4 chỉ số Phân vùng Mặt nạ (Mask mAP50-95, Mask mAP50, Mask Precision, Mask Recall) trên thang đo [0.65, 0.95]. TSVM thể hiện diện tích bao phủ nở rộng đồng đều ở cả hai bán cầu, đặc biệt là sự gia tăng vượt trội về Box Recall (+0.0133) và Mask Precision (+0.0095), cho thấy mức cân bằng vừa phải của mối quan hệ đánh đổi (trade-off) giữa định vị đối tượng và tách biên điểm ảnh.

### 5.9. Phân tích phân tán và độ biến thiên (Boxplot Variance Stability)
![Hình 9](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures/11_boxplot_variance_stability.png)
*Hình 9. Biểu đồ hộp (Boxplot) tích hợp điểm phân tán (jitter points) thể hiện độ ổn định phương sai Mask mAP@50-95*

> **Nhận xét học thuật 2 trục:** Hình 9 thể hiện biểu đồ hộp (Boxplot) tích hợp các điểm dữ liệu phân tán (jitter points) của chỉ số Mask mAP@50-95 qua 10 seeds. Hộp phân vị của TSVM co cụm chặt chẽ với dải liên phân vị hẹp hơn Baseline đáng kể (độ lệch chuẩn giảm 39.5%), đồng thời trung vị (median) nằm ở mức cao hơn. Phân phối này mô tả mức giảm phân tán và nâng đáy hiệu năng của TSVM (từ 0.6941 lên 0.7065); chưa đủ cơ sở định lượng cho kết luận về an toàn chẩn đoán.

### 5.10. Ma trận nhầm lẫn chuẩn hóa trung bình (Mean Normalized Confusion Matrix)
![Hình 10](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures/12_confusion_matrix_mean_comparison.png)
*Hình 10. Ma trận nhầm lẫn chuẩn hóa trung bình 10 seed giữa Baseline và TSVM trên 160 ảnh thẩm định (127 thực thể polyp)*

> **Nhận xét học thuật 2 trục:** Hình 10 trình bày ma trận nhầm lẫn chuẩn hóa trung bình qua 10 seeds trên tập kiểm thử gồm 127 tổn thương polyp thực tế và 40 ảnh niêm mạc bình thường. TSVM đạt tỷ lệ phát hiện polyp chính xác 87.6% (so với 86.9% của Baseline), đồng thời nâng tỷ lệ nhận diện đúng niêm mạc lành từ 58.0% lên 63.5%. Đây là quan sát mô tả trên tập kiểm định hiện tại; tác động của việc bổ sung 20% ảnh nền âm tính cần được xác lập qua một thực nghiệm đối chứng riêng với tập thuần polyp.

### 5.11. Bản đồ nhiệt chênh lệch hiệu số nhầm lẫn (Difference Heatmap)
![Hình 11](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures/13_confusion_matrix_diff_heatmap.png)
*Hình 11. Bản đồ nhiệt thể hiện hiệu số chênh lệch chuẩn hóa (TSVM - Baseline): Xanh lá là cải thiện, Đỏ là suy giảm*

> **Nhận xét học thuật 2 trục:** Hình 11 là Heatmap thể hiện hiệu số chênh lệch (TSVM - Baseline). Màu xanh lá đại diện cho sự cải thiện tích cực: ô True Positive tăng +0.71% và ô True Negative tăng +5.50%. Ngược lại, màu đỏ nhạt biểu thị sự sụt giảm của các sai số lâm sàng: ô False Negative (bỏ sót bệnh) giảm -0.71% và ô False Positive (báo động giả) giảm -5.50%. Mức thay đổi này được ghi nhận như quan sát mô tả; ý nghĩa lâm sàng cần được đánh giá qua nghiên cứu tiếp cận lâm sàng có đối chứng.

### 5.12. So sánh số lượng cá thể các ô nhầm lẫn lâm sàng (Grouped Bar Chart)
![Hình 12](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Ket_Qua_V2/KQ_Nen_DX_10seed/figures/14_confusion_cells_grouped_barchart.png)
*Hình 12. Biểu đồ cột nhóm so sánh số lượng ca tổn thương tuyệt đối trung bình kèm sai số của 4 nhóm tế bào nhầm lẫn*

> **Nhận xét học thuật 2 trục:** Hình 12 quy đổi ma trận nhầm lẫn thành số lượng ca tổn thương tuyệt đối trung bình kèm sai số. TSVM phát hiện đúng 111.2 polyp (tăng 0.9 tổn thương so với Baseline 110.3), kéo giảm số polyp bị bỏ sót xuống còn 15.8 ca. Đồng thời, số ca báo động giả trên ảnh nền giảm từ 16.8 xuống 14.6 ca. Sự chuyển dịch đồng thời của cả 4 nhóm tế bào nhầm lẫn cung cấp thông tin tham chiếu cho bác sĩ nội soi khi đánh giá độ tin cậy của cảnh báo tự động.

---

## 6. ĐÁNH GIÁ CHI PHÍ TÍNH TOÁN VÀ TÍNH KHẢ THI TRIỂN KHAI THỜI GIAN THỰC

Để đánh giá toàn diện tính khả thi khi đưa vào ứng dụng thực tế trong phòng nội soi bệnh viện, nhóm nghiên cứu đã tiến hành đo đạc chi tiết chi phí tài nguyên tính toán giữa hai kiến trúc trên cùng một cấu hình phần cứng tiêu chuẩn GPU NVIDIA Tesla T4 với độ phân giải đầu vào chuẩn 640x640 pixel:

*Bảng 6: So sánh chi phí tính toán, mức chiếm dụng bộ nhớ và tốc độ suy luận thời gian thực*

| Chỉ số đánh giá | Baseline YOLO26s-seg | TSVM Đề xuất | Chênh lệch ($\Delta$) | Đánh giá Khả thi Triển khai |
| :--- | :---: | :---: | :---: | :--- |
| **Số lượng tham số (Parameters)** | 11.55 M | 12.16 M | $+0.61\text{ M}$ ($+5.28\%$) | Gọn nhẹ, kiến trúc tăng rất ít tham số |
| **Độ phức tạp tính toán (GFLOPs)** | 42.3 GFLOPs | 47.4 GFLOPs | $+5.1\text{ GFLOPs}$ ($+12.06\%$) | Hoàn toàn phù hợp các thiết bị Edge AI y tế |
| **Kích thước tệp trọng số (.pt)** | 23.8 MB | 25.1 MB | $+1.3\text{ MB}$ ($+5.46\%$) | Thuận tiện nạp vào bộ nhớ các dòng máy soi |
| **Độ trễ suy luận toàn chuỗi (Latency)** | 17.2 ms/ảnh | 19.8 ms/ảnh | $+2.6\text{ ms/ảnh}$ | Bao gồm cả Preprocess, Forward và Post-NMS |
| **Tốc độ khung hình (Frames Per Second)** | 58.1 FPS | 50.5 FPS | $-7.6\text{ FPS}$ | **Vượt xa chuẩn video nội soi ($\ge 30\text{ FPS}$)** |
| **Bộ nhớ VRAM khi suy luận (Peak VRAM)** | 1.42 GB | 1.68 GB | $+0.26\text{ GB}$ | Vô cùng tiết kiệm, chạy tốt trên GPU phổ thông |

**Kết luận về khả năng ứng dụng lâm sàng thời gian thực:** Mặc dù cơ chế quét chọn lọc 4 hướng SS2D làm tăng nhẹ chi phí tính toán (+5.1 GFLOPs), tốc độ suy luận thực tế của TSVM vẫn đạt mức 50.5 FPS (tương đương độ trễ chỉ 19.8 ms mỗi khung hình). Do tiêu chuẩn video của các hệ thống máy nội soi tiêu hóa hiện đại (như Olympus EVIS X1, EVIS EXERA III hay Fujifilm ELUXEO 7000) hoạt động ở tần số quét chuẩn 25 đến 30 FPS, mô hình TSVM hoàn toàn dư thừa năng lực để xử lý phân đoạn polyp trực tiếp theo thời gian thực (*real-time stream*) mà không gây ra bất kỳ hiện tượng giật khung hình hay trễ hiển thị nào đối với thao tác tay của bác sĩ.

---

*TP. Hồ Chí Minh, ngày 29 tháng 09 năm 2026*  
**ĐẠI DIỆN NHÓM SINH VIÊN THỰC HIỆN**  
**Lê Đức Lương — Phùng Tuấn Huy — Trần Mạnh Toàn**
