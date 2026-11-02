# K. Kế hoạch bản báo cáo cả quyển khoảng 70 trang

> Trạng thái (02/11/2026): **đề xuất, chưa duyệt, chưa sửa file nào.** Chủ dự án đang chọn mục nào giữ, rút hay bỏ (điền cột "Quyết định").

## 1. Bối cảnh

Khóa luận HUIT, mã CNTT_KLCN182: so sánh YOLO26s-seg (mô hình gốc) với YOLO26s-seg + C2TSVMamba (TSVM FP32) cho phân đoạn polyp. Hiện có hai bản báo cáo Word:

| Bản | Thư mục markdown | File Word/PDF | Số trang |
|---|---|---|---|
| Đầy đủ | `06_bao_cao/md_bao_cao/` | `06_bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_V3_day_du.docx/.pdf` | 147 (tag git `ban_day_du_147`) |
| Rút gọn | `06_bao_cao/md_bao_cao_rut_gon/` | `06_bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_V3_rut_gon.docx/.pdf` | 109 (thân 70) |

Yêu cầu mới: **cả quyển**, tính từ bìa đến hết phụ lục, còn khoảng 70 trang. Kế hoạch làm thành **bản thứ ba** trong thư mục `06_bao_cao/md_bao_cao_70/` (tạo từ bản rút gọn). Hai bản cũ giữ nguyên. Kế hoạch của bản rút gọn: [J_ke_hoach_ban_rut_gon_70.md](J_ke_hoach_ban_rut_gon_70.md).

## 2. Quy tắc bắt buộc khi cắt

- **Không thêm và không đổi số liệu.** Mọi con số phải giữ nguyên như bản rút gọn, truy được về `00_tai_lieu_tong_quan/bang/*.csv`.
- Kết quả chính viết là **"xu hướng"**: Δ mAP50–95 = +0,0043, CI 95% [−0,0002; 0,0088], p = 0,061, TSVM tốt hơn 13/20 seed. **Không có ý nghĩa thống kê.** Không viết "vượt trội". Độ ổn định (Levene p = 0,026) chỉ là thăm dò. Topology: TSVM chỉ nhích hơn mô hình gốc, không có ý nghĩa thống kê, kém PraNet rõ rệt.
- Số thập phân dùng dấu phẩy.
- **Phải giữ** các phần có trong tiêu chí chấm: độ đo, ablation (6.6), dữ liệu thực tế (6.7, 5.7), phân công (Bảng 0.2), ứng dụng (Ch.5).
- Tài liệu tham khảo kiểu IEEE, đánh số theo lần trích đầu tiên. Bỏ tài liệu nào thì đánh số lại toàn bộ và kiểm tra thứ tự 1→N. **Bỏ tài liệu phải được chủ dự án đồng ý.**
- Đánh số hình, bảng, công thức lại cho liền mạch. Câu nào dẫn tới hình, bảng hay mục đã bỏ thì sửa câu đó.
- AV/AVF/ITSVM không đưa vào báo cáo.
- Làm mẫu một chương trước (đề xuất Ch.2 hoặc Ch.6). Chủ dự án duyệt mức cắt rồi mới làm các chương còn lại.

## 3. Cách ghép và kiểm tra

```bash
# chạy ở thư mục gốc repo; cần python3.13 (có pypandoc, docxcompose) và Microsoft Word
python3.13 06_bao_cao/ghep_word/ghep_word.py --md md_bao_cao_70 --ra 70
# kiểm tra số liệu, thứ tự trích dẫn và đánh số so với bản đầy đủ (chạy trong 06_bao_cao)
python3.13 ghep_word/kiem_tra_rut_gon.py .
```

Script kiểm tra hiện đọc cố định thư mục `md_bao_cao_rut_gon`, cần thêm tham số chọn thư mục. Muốn mục lục chỉ hiện 2 cấp thì sửa phần sinh mục lục trong `ghep_word.py` (hiện là 3 cấp).

## 4. Cấu trúc bản rút gọn hiện tại và gợi ý

Số trang là số trang vật lý trong PDF bản rút gọn. Trang của từng mục nhỏ là ước lượng theo vị trí đề mục.

Cột **Gợi ý**:
- **Giữ:** giữ nguyên.
- **Rút:** viết ngắn lại.
- **Bỏ:** bỏ hẳn hoặc chỉ giữ 1–2 câu.
- Số trong ngoặc là số trang ước tính tiết kiệm được.

Cột **Quyết định** để chủ dự án điền.

### 4.1. Trang đầu: 15 trang (trang 1–15)

| Phần | Trang | Nội dung | Gợi ý | Quyết định |
|---|---|---|---|---|
| Bìa chính, bìa phụ | 1–2 (2 tr) | Theo mẫu của trường | Giữ | |
| Lời cảm ơn | 3 (1 tr) | | Giữ | |
| Mục lục | 4–8 (5 tr) | Hiện có 3 cấp đề mục | Rút: chỉ hiện 2 cấp (−2) | |
| Chữ viết tắt và ký hiệu | 9–11 (3 tr) | Khoảng 40 chữ viết tắt và bảng ký hiệu toán | Rút: bỏ cột "Xuất hiện ở", bớt mục ít dùng (−1) | |
| Danh mục hình, danh mục bảng | 12–15 (4 tr) | Tự sinh | Tự ngắn lại khi bớt hình và bảng | |

### 4.2. Mở đầu: 6 trang (16–21), `01_MO_DAU.md`

| Mục | Trang | Nội dung | Gợi ý | Quyết định |
|---|---|---|---|---|
| 1. Lý do chọn đề tài | khoảng 1 | Gánh nặng ung thư đại trực tràng, nội soi bỏ sót polyp, vì sao chọn YOLO và Mamba | Rút (−0,5) | |
| 2. Mục tiêu | 0,7 | Mục tiêu chung và 5 mục tiêu cụ thể | Giữ | |
| 3. Đối tượng, phạm vi | 0,6 | BG20, hai mô hình, chỉ dùng tập kiểm định | Rút (−0,2) | |
| 4. Phương pháp | 0,4 | 20 seed ghép cặp, kiểm định thống kê | Giữ | |
| 5. Đóng góp | 0,4 | 4 đóng góp | Giữ | |
| 6. Kế hoạch và phân công | 2 | Bảng 0.1 kế hoạch theo tuần, Bảng 0.2 phân công | Bỏ Bảng 0.1 (−1), giữ Bảng 0.2 | |
| 7. Bố cục | 0,2 | Mỗi chương 1 câu | Giữ | |

### 4.3. Chương 1. Tổng quan: 6 trang (21–27), `02_CHUONG_1_TONG_QUAN.md`

| Mục | Trang | Nội dung | Gợi ý | Quyết định |
|---|---|---|---|---|
| 1.1 Bối cảnh | 0,8 | Polyp, nội soi, định nghĩa bài toán phân đoạn | Giữ | |
| 1.2 Bộ dữ liệu công khai | 1 | Bảng 1.1: Kvasir-SEG, CVC-ClinicDB, ColonDB, ETIS, PolypGen | Rút: mỗi bộ dữ liệu 1 dòng (−0,4) | |
| 1.3 Các hướng nghiên cứu | 1,5 | Mã hóa–giải mã (U-Net, PraNet), Transformer, YOLO, Mamba/VMamba, Mamba trong YOLO | Rút: mỗi hướng 2–3 câu (−0,7) | |
| 1.4 Tổng hợp và khoảng trống | 2 | Bảng 1.2 so sánh các hướng, Bảng 1.3 các công trình gần nhất, khoảng trống nghiên cứu | Rút: bỏ Bảng 1.2, giữ Bảng 1.3 (−0,8) | |
| 1.5 Tình hình trong nước | 0,4 | Vài nghiên cứu ở Việt Nam | Giữ | |
| 1.6 Kết chương | 0,1 | | Giữ | |

### 4.4. Chương 2. Cơ sở lý thuyết: 10 trang (27–37), `03_CHUONG_2_CO_SO_LY_THUYET.md`

| Mục | Trang | Nội dung | Gợi ý | Quyết định |
|---|---|---|---|---|
| 2.1 Các bài toán thị giác | 1,3 | Hình 2.1 so sánh 4 kiểu đầu ra, Bảng 2.1 | Rút: giữ hình, bỏ bảng (−0,5) | |
| 2.2 Mạng tích chập | 0,5 | Tích chập, kết nối tắt | Bỏ (−0,5): kiến thức phổ thông | |
| 2.3 Họ YOLO | 1 | Phát hiện một giai đoạn, gán nhãn, bỏ NMS, mặt nạ mẫu | Rút (−0,4) | |
| 2.4 YOLO26-seg | 2 | Kiến trúc (Bảng 2.2), các bước thuật toán, ưu/nhược (Bảng 2.3) | Rút phần các bước thuật toán (−0,5), giữ kiến trúc | |
| 2.5 Cơ chế chú ý và chi phí | 0,3 | Attention có chi phí O(N²) | Bỏ, gộp 1 câu vào 2.6 (−0,3) | |
| 2.6 SSM, Mamba, VMamba | 2 | Rời rạc hóa, SSM chọn lọc, SS2D quét 4 hướng, ưu/nhược (Bảng 2.4) | Giữ, bỏ Bảng 2.4 (−0,4) | |
| 2.7 Độ đo | 1,3 | TP/FP/FN, IoU, Dice, AP, mAP50–95, FLOPs | Giữ | |
| 2.8 Kiểm định thống kê | 1 | Vì sao cần nhiều seed, kiểm định t ghép cặp, Wilcoxon, cỡ hiệu ứng | Rút (−0,3) | |
| 2.9 Kết chương | 0,1 | | Giữ | |

### 4.5. Chương 3. Mô hình đề xuất: 12 trang (38–49), `04_CHUONG_3_MO_HINH_DE_XUAT.md`

| Mục | Trang | Nội dung | Gợi ý | Quyết định |
|---|---|---|---|---|
| 3.1 Ý tưởng và động cơ | 1 | Vì sao thay ở tầng 10, vì sao dùng SS2D và nhánh hình dạng | Rút (−0,4) | |
| 3.2 Kiến trúc tổng thể | 1 | Hình 3.1, Bảng 3.1 các tầng | Giữ | |
| 3.3 Khối C2TSVMamba | 4,5 | Tách–xử lý–ghép (H3.2), SS2D (H3.3, H3.4), nhánh hình dạng, cổng F·(1+G), FFN, số tham số (B3.2) | Lõi của đề tài. Rút: bỏ H3.4 (−1) | |
| 3.4 Quét kết hợp song song | 1,5 | Thuật toán quét, độ phức tạp | Bỏ, giữ 2 câu (−1,2) | |
| 3.5 Huấn luyện và lưu trọng số | 1,5 | Khởi tạo, mất mát (công thức 3.15, Bảng 3.3), lỗi FP16 làm tràn BatchNorm | Rút Bảng 3.3 (−0,3). Giữ phần FP32 vì hội đồng hay hỏi | |
| 3.6 Ưu điểm và hạn chế | 0,6 | 5 ưu điểm, 5 hạn chế | Bỏ, gộp vào Kết luận (−0,5) | |
| 3.7 Các chế độ tách thành phần | 0,7 | Bảng 3.4: 4 chế độ ablation | Giữ | |
| 3.8 Kết chương | 0,2 | | Giữ | |

### 4.6. Chương 4. Dữ liệu và tiền xử lý: 8 trang (50–57), `05_CHUONG_4_DU_LIEU_TIEN_XU_LY.md`

| Mục | Trang | Nội dung | Gợi ý | Quyết định |
|---|---|---|---|---|
| 4.1 Nguồn dữ liệu | 1 | Kvasir-SEG, ảnh nền normal-cecum (H4.1) | Rút: bỏ H4.1 (−0,4) | |
| 4.2 Bộ BG20 và cách chia | 1 | Bảng 4.1: 1.040 ảnh huấn luyện, 160 ảnh kiểm định | Giữ | |
| 4.3 Chuyển mặt nạ thành đa giác | 1,5 | 5 bước (H4.2), số đỉnh 333,2 → 24,6 | Giữ, rút chữ (−0,4) | |
| 4.4 Đổi kích thước | 1 | LetterBox 640 (H4.3) | Bỏ hình, còn 2 câu (−0,7) | |
| 4.5 Tăng cường dữ liệu | 2 | H4.4, Bảng 4.2 các phép tăng cường | Rút: giữ bảng, bỏ hình (−0,8) | |
| 4.6 Kiểm tra toàn vẹn và quy trình | 1,5 | md5, H4.5 sơ đồ tổng | Rút (−0,6) | |

### 4.7. Chương 5. Cài đặt và ứng dụng: 9 trang (58–66), `06_CHUONG_5_CAI_DAT_UNG_DUNG.md`

> Chương này còn **7 ô [CHỤP HÌNH] chưa có ảnh** (Hình 5.1, 5.3–5.8). Khi chèn ảnh sẽ tăng thêm khoảng 2–3 trang.

| Mục | Trang | Nội dung | Gợi ý | Quyết định |
|---|---|---|---|---|
| 5.1 Môi trường và công cụ | 1 | Bảng 5.1: Kaggle P100, thư viện, phiên bản | Rút (−0,4) | |
| 5.2 Cài đặt hai mô hình | 2,5 | Bảng 5.2, 5.3: tệp yaml, đăng ký module, bản vá FP32 | Rút mạnh vì trùng Ch.3 (−1,5) | |
| 5.3 Quy trình huấn luyện và lưu kết quả | 0,5 | Notebook, cách lưu kết quả | Bỏ (−0,5) | |
| 5.4 PolypVision: yêu cầu và kiến trúc | 2 | H5.2 sơ đồ hệ thống, Bảng 5.4 yêu cầu | Giữ | |
| 5.5 Dịch vụ suy luận và lưu trữ | 0,7 | API, tổ chức lưu trữ | Gộp vào 5.4 (−0,4) | |
| 5.6 Giao diện và chức năng | 2 | Bảng 5.5 chức năng, các ảnh chụp màn hình | Giữ 3–4 ảnh chính, bỏ Bảng 5.5 (−0,5) | |
| 5.7 Triển khai trên dữ liệu thực tế | 0,7 | Chạy thử trên ảnh ngoài | Giữ | |
| 5.8 Hạn chế và kết chương | 0,3 | | Giữ | |

### 4.8. Chương 6. Thực nghiệm và đánh giá: 16 trang (67–82), `07_CHUONG_6_THUC_NGHIEM_DANH_GIA.md`

| Mục | Trang | Nội dung | Gợi ý | Quyết định |
|---|---|---|---|---|
| 6.1 Thiết lập | 1 | 4 mô hình × 20 seed, chỉ số chính, kiểm định | Giữ | |
| 6.2.1 Kết quả tổng hợp | 1,2 | H6.1, Bảng 6.1: +0,0043, p = 0,061, 13/20 | Giữ (kết quả chính) | |
| 6.2.2 Độ ổn định | 0,5 | Bảng 6.2: SD, Levene p = 0,026 | Giữ | |
| 6.2.3 Độ nhạy theo epoch | 0,5 | Bảng 6.3: 3 quy tắc chọn epoch | Bỏ, còn 1 câu (−0,4) | |
| 6.2.4 Quá trình hội tụ | 0,4 | TSVM chậm hơn ở 10 epoch đầu, cao hơn từ epoch 82 | Bỏ, còn 1 câu (−0,3) | |
| 6.2.5 Ma trận nhầm lẫn | 0,7 | H6.2, Bảng 6.4 | Rút: bỏ hình (−0,4) | |
| 6.3 Theo pixel, so với PraNet và U-Net | 3 | H6.3, H6.4, Bảng 6.5, 6.6: Dice, IoU, Precision, Recall | Rút: bỏ H6.4 và Bảng 6.6 (−1) | |
| 6.4 Topology | 1,3 | H6.5, Bảng 6.7: 0,797 → 0,808, PraNet 0,914 | Rút: bỏ hình (−0,4) | |
| 6.5 Chi phí tính toán | 1,7 | Bảng 6.8 tham số và FLOPs, Bảng 6.9 độ trễ CPU/GPU | Gộp thành 1 bảng (−0,5) | |
| 6.6 Ablation | 2 | H6.6, Bảng 6.10: 3 biến thể, đều thấp hơn bản đầy đủ (xu hướng) | Giữ, có trong tiêu chí chấm | |
| 6.7 Dữ liệu thực tế | 2 | H6.7, H6.8, Bảng 6.11: 4 bộ dữ liệu ngoài, PolypGen | Rút: bỏ H6.8 (−0,5), có trong tiêu chí chấm | |
| 6.8 Thảo luận | 1 | Giải thích kết quả, so sánh chi phí và lợi ích | Rút (−0,5) | |
| 6.9 Kết chương | 0,3 | | Giữ | |

### 4.9. Kết luận: 3 trang (83–85), `09_KET_LUAN.md`

| Mục | Nội dung | Gợi ý | Quyết định |
|---|---|---|---|
| 1. Kết quả đạt được | Tóm tắt những gì đã làm | Rút (−0,5) cho cả chương | |
| 2. Đánh giá kết quả | Số liệu chính, trung thực về ý nghĩa thống kê | Giữ | |
| 3. Hạn chế | | Giữ, nhận thêm ý từ 3.6 | |
| 4. Hướng phát triển | | Giữ | |

### 4.10. Tài liệu tham khảo: 7 trang (86–92), 57 mục, `08_TAI_LIEU_THAM_KHAO.md`

Gợi ý bỏ những tài liệu chỉ được trích ở phần bị cắt, ước còn khoảng 40–45 mục, khoảng 5,5 trang (−1,5). **Cần chủ dự án đồng ý.** Danh sách cụ thể sẽ có sau khi chốt các mục bỏ ở trên.

Quyết định:

### 4.11. Phụ lục: 17 trang (93–109), `10_PHU_LUC.md`

| Phụ lục | Trang | Nội dung | Gợi ý | Quyết định |
|---|---|---|---|---|
| A. Kết quả từng seed | 93–94 (2 tr) | PL.1 mAP 20 seed, PL.2 Dice 4 mô hình, PL.3 ablation 5 seed | Giữ PL.1, bỏ PL.2 và PL.3 (−0,7) | |
| B. Cấu hình huấn luyện | 95 (0,7 tr) | Bảng siêu tham số | Giữ | |
| C. Tổ chức mã nguồn | 95–96 (1 tr) | Cây thư mục, tệp kết quả | Bỏ (−1) | |
| D. Hướng dẫn chạy lại | 96–97 (1 tr) | 5 lệnh tính lại số liệu | Bỏ (−1) | |
| E. Phân công theo hạng mục | 97 (0,7 tr) | Bảng PL.7 | Bỏ, đã có Bảng 0.2 ở Mở đầu (−0,7) | |
| F. Chi tiết C2TSVMamba | 98–100 (2,5 tr) | Truy vết tensor, ví dụ quét song song, chi phí tầng 10, Thuật toán PL.1 | Bỏ (−2,5) | |
| G. API PolypVision | 100–102 (3 tr) | 4 bảng API và cấu trúc lưu trữ | Bỏ (−3) | |
| H. Kết quả bổ sung | 103–109 (6,5 tr) | 11 hình phụ, bảng phụ dữ liệu ngoài | Bỏ (−6,5) | |

## 5. Ước tính nếu làm theo hết gợi ý

| Phần | Hiện tại | Sau khi cắt |
|---|---|---|
| Trang đầu | 15 | khoảng 12 |
| Thân | 70 | khoảng 50 (cộng 2–3 trang khi chèn ảnh Ch.5) |
| Tài liệu tham khảo | 7 | khoảng 5,5 |
| Phụ lục | 17 | khoảng 2 |
| **Tổng** | **109** | **khoảng 70–72** |

Nếu sau khi chèn ảnh Ch.5 vẫn vượt 70 trang, thứ tự cắt tiếp theo:
1. Bỏ hẳn Bảng 1.3 (Ch.1).
2. Bỏ H6.7 (6.7) và chỉ giữ Bảng 6.11.
3. Bỏ Phụ lục A.

## 6. Các bước thực hiện (sau khi duyệt)

1. Chủ dự án điền cột "Quyết định" và đồng ý danh sách tài liệu tham khảo bị bỏ.
2. Tạo `06_bao_cao/md_bao_cao_70/` bằng cách sao chép `md_bao_cao_rut_gon/`.
3. Làm mẫu một chương (Ch.2 hoặc Ch.6), chủ dự án duyệt.
4. Làm các chương còn lại, đánh số lại hình, bảng, công thức và tài liệu tham khảo.
5. Cho script kiểm tra nhận tham số thư mục, chạy kiểm tra; sửa mục lục còn 2 cấp trong `ghep_word.py`.
6. Ghép Word và xuất PDF, đếm lại số trang, cập nhật mục 5 của file này.
7. Commit lên nhánh `Okeydokey` khi được đồng ý.
