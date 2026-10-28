# 08. Triển khai trên dữ liệu thực tế (CLO4)

Đánh giá khả năng tổng quát hóa: lấy các checkpoint đã huấn luyện trên BG20 (Kvasir-SEG + ảnh nền), chạy thẳng trên **ba bộ dữ liệu khác nguồn**, không huấn luyện lại, không tinh chỉnh. Phần này phục vụ mục "Triển khai trên dữ liệu thực tế" (CLO4, 0,75 điểm) của đề cương và mục tương ứng ở Chương 5 và Chương 6.

## Dữ liệu (chỉ đọc, không chép vào đây)

| Khóa | Bộ dữ liệu | Số ảnh | Kích thước | Đường dẫn |
|---|---|---:|---|---|
| `clinicdb` | CVC-ClinicDB | 612 | 384×288 | `DeepLearning/Dataset/CVC-ClinicDB/PNG/{Original, Ground Truth}` |
| `colondb` | CVC-ColonDB | 380 | 574×500 | `DeepLearning/Dataset/CVC-ColonDB_data/CVC-ColonDB/{images, masks}` |
| `etis` | ETIS-LaribPolypDB | 196 | 1225×966 | `DeepLearning/Dataset/ETIS-Larib PolypDB/{images, masks}` |

- Cả ba bộ đều là khung hình cắt từ video nội soi, khác thiết bị và trung tâm so với Kvasir-SEG. Đây là dữ liệu công khai khác nguồn, **không phải dữ liệu lâm sàng** thu tại bệnh viện.
- Mọi ảnh đều có polyp (không có ảnh nền), nên không đo được tỉ lệ báo nhầm trên ảnh nền.
- Mặt nạ được nhị phân hóa ở ngưỡng > 127. Riêng CVC-ClinicDB lưu mặt nạ ở dạng RGB có nhiễu nén, ngưỡng này xử lý được.

## Bộ thứ tư: PolypGen2021 (đã đánh giá 28/10/2026)

- 1.537 ảnh đơn có mặt nạ, thu từ 6 trung tâm: C1 256, C2 301, C3 457, C4 227, C5 208, C6 88 (`Dataset/PolypGen2021_MultiCenterData_v3/.../data_C*/images_C*`). Phần chuỗi video không dùng.
- Cần trích bài báo của bộ dữ liệu (arXiv 2106.04463). `readme.md` ghi CC BY 4.0, `license.txt` ghi CC BY-NC-SA 4.0; cả hai đều cho phép dùng trong khóa luận.

**Cách xử lý:**
- Chạy từng trung tâm (khóa `pg_c1` … `pg_c6`) để tránh tràn RAM vì ảnh lớn tới 1920×1080. Khi tổng hợp có thêm dòng gộp `polypgen`.
- **125 ảnh có mặt nạ rỗng** (giá trị lớn nhất bằng 0, tức ảnh không có polyp): C1 5, C2 31, C3 1, C4 81, C5 2, C6 5. Các ảnh này không tính vào Dice/IoU (1.412 ảnh có polyp), mà dùng để đo `bg_fp_image_rate`: tỉ lệ ảnh không polyp mà mô hình vẫn báo có polyp.
- Bộ gốc có 1 lỗi đặt tên: ảnh `C3_EndoCV2021_00489].jpg` thừa dấu `]`; script bỏ dấu này khi tìm mặt nạ, không đổi tên tệp gốc.
- Không lưu mặt nạ dự đoán seed 0 cho PolypGen (ảnh quá lớn).

**Kết quả 20 seed, Dice theo pixel (trung bình; nguồn `bang/20seed/02_ngoai_thong_ke.csv`):**

| Trung tâm | Ảnh có polyp | YOLO26s-seg | + TSVM | PraNet | U-Net | TSVM − gốc (p t; p Wilcoxon) |
|---|---:|---|---|---|---|---|
| C1 | 251 | 0,753 | 0,752 | 0,724 | 0,511 | −0,001 (0,85; 0,87) |
| C2 | 270 | 0,753 | 0,749 | 0,759 | 0,543 | −0,005 (0,52; 0,50) |
| C3 | 456 | 0,855 | 0,856 | 0,806 | 0,593 | +0,002 (0,69; 0,99) |
| C4 | 146 | 0,516 | 0,503 | 0,449 | 0,255 | −0,013 (0,28; 0,048) |
| C5 | 206 | 0,474 | 0,472 | 0,418 | 0,292 | −0,002 (0,85; 0,45) |
| C6 | 83 | 0,720 | 0,699 | 0,708 | 0,492 | **−0,021 (0,032; 0,019)** |
| **Gộp** | **1.412** | **0,719** | **0,715** | **0,683** | **0,484** | −0,004 (0,55; 0,25) |

- Gộp cả 6 trung tâm: TSVM và mô hình gốc ngang nhau. TSVM cao hơn PraNet 0,032 (p < 0,001; 17/20 seed) và cao hơn U-Net rất xa.
- Theo từng trung tâm: chỉ C6 có TSVM thấp hơn mô hình gốc ở cả hai kiểm định (83 ảnh, nên cần thận trọng). C4 chỉ có Wilcoxon dưới 0,05, kiểm định t thì không. Các trung tâm khác không khác biệt.
- PraNet tốt hơn hai mô hình YOLO ở C2.
- Báo nhầm trên ảnh không polyp (gộp 125 ảnh): YOLO26s-seg 13,3%, TSVM 10,8%, PraNet 22,6%, U-Net 69,3%. TSVM thấp hơn mô hình gốc 2,5 điểm % (p = 0,011; Wilcoxon 0,018), chủ yếu nhờ C2 và C4. Số ở C3 (1 ảnh) và C5 (2 ảnh) không có ý nghĩa.
- Bộ 10 seed (`bang/10seed/`) cho cùng bức tranh: gộp TSVM 0,722 so với 0,715 (p = 0,49), không trung tâm nào khác biệt có ý nghĩa.

**Kiểm tra trùng ảnh với Kvasir-SEG (27/10/2026)**, script `scripts/kiem_tra_trung_polypgen.py`:
- So 1.537 ảnh PolypGen với 1.000 ảnh Kvasir-SEG bằng ba cách: md5 tệp; pHash và dHash 64 bit; tương quan ảnh xám 64×64 sau khi cắt viền đen (bắt được ảnh bị đổi kích thước, nén lại hoặc cắt viền).
- Kết quả: **0 cặp trùng md5**; tương quan cao nhất chỉ 0,899 (không cặp nào từ 0,90 trở lên), trong khi ảnh trùng thật thường từ 0,97 trở lên. Đã xem bằng mắt 8 cặp gần nhất (5 cặp tương quan cao nhất, 3 cặp pHash gần nhất): đều là ảnh khác nhau (khác polyp, khác góc chụp, khác thiết bị).
- **Kết luận: không có ảnh trùng, không loại ảnh nào.** Danh sách trùng (`bang/polypgen_trung/02_danh_sach_trung.csv`) rỗng nên thư mục `polypgen_trung_kvasir/` không được tạo. Bảng cặp gần nhất của từng ảnh: `bang/polypgen_trung/01_cap_gan_nhat.csv`.
- Giới hạn: phép kiểm tra phát hiện ảnh giống nhau trên toàn khung hình; không phát hiện trường hợp một ảnh chỉ là phần cắt nhỏ của ảnh kia, hoặc hai khung hình liền nhau của cùng một video.

## Mô hình và giao thức

- 4 mô hình × **seed 0–19**; bảng tổng hợp tách riêng cho 10 seed (seed 0–9, khớp bộ trọng tâm) và 20 seed: YOLO26s-seg, YOLO26s-seg + TSVM FP32, PraNet (ResNet-50), U-Net.
- Giao thức suy luận và cách tính chỉ số giống hệt `00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py`; script ở đây gọi lại các hàm của script đó.
  - YOLO: imgsz 640, conf 0,25, iou 0,7, `retina_masks=True`, `half=False`; gộp mọi mặt nạ của ảnh thành một.
  - PraNet/U-Net: resize 352×352, ngưỡng 0,5, phóng về kích thước gốc.
- Chỉ số theo pixel: Dice, IoU, Precision, Recall (trung bình theo ảnh), Dice/IoU gộp toàn tập (`_micro`), và tỉ lệ ảnh mà mô hình không dự đoán điểm nào (`no_pred_rate`, tức bỏ sót cả ảnh).
- So sánh ghép cặp theo seed giữa TSVM và từng mô hình còn lại: kiểm định t ghép cặp và Wilcoxon.

## Chạy lại

```bash
cd 08_du_lieu_thuc_te/scripts
C:\venv_kl_gpu\Scripts\python.exe danh_gia_du_lieu_ngoai.py                 # 3 bộ × 4 mô hình × seed 0–9
C:\venv_kl_gpu\Scripts\python.exe danh_gia_du_lieu_ngoai.py --seeds 10 11 12 13 14 15 16 17 18 19
C:\venv_kl_gpu\Scripts\python.exe danh_gia_du_lieu_ngoai.py --chi-tong-hop  # chỉ tổng hợp lại bảng
```

Mỗi lượt (bộ dữ liệu, mô hình, seed) ghi một tệp riêng, nên chạy lại sẽ bỏ qua lượt đã xong. Bảng tổng hợp ghi vào `bang/10seed/` (seed 0–9) và `bang/20seed/` (seed 0–19); mỗi bảng chỉ được ghi khi đã đủ lượt.

## Cấu trúc

```
08_du_lieu_thuc_te/
├── README.md
├── scripts/danh_gia_du_lieu_ngoai.py
├── bang/
│   ├── tung_luot/<bộ>_<mô hình>_s<seed>.csv   # TP/FP/FN từng ảnh của từng lượt
│   ├── 10seed/, 20seed/
│   │   ├── 01_ngoai_tung_seed.csv              # chỉ số theo seed
│   │   └── 02_ngoai_thong_ke.csv               # mean ± SD, so sánh ghép cặp
│   └── _log_chay.txt, _log_chay_seed10-19.txt
└── du_lieu_dinh_tinh/pred_seed0_<bộ>_<mô hình>.npz   # mặt nạ dự đoán seed 0, cho hình minh họa
```

## Kết quả (chạy ngày 27/10/2026, 240 lượt, tổng khoảng 30 phút trên RTX 5050 Laptop)

### 10 seed (seed 0–9)

Dice theo pixel, trung bình ± SD (nguồn: `bang/10seed/02_ngoai_thong_ke.csv`):

| Bộ dữ liệu | YOLO26s-seg | + TSVM | PraNet | U-Net | TSVM − YOLO26s-seg (p t ghép cặp; seed TSVM cao hơn) |
|---|---|---|---|---|---|
| CVC-ClinicDB | 0,783 ± 0,022 | 0,774 ± 0,016 | 0,753 ± 0,026 | 0,511 ± 0,032 | −0,009 (p = 0,23; 4/10) |
| CVC-ColonDB | 0,628 ± 0,026 | 0,608 ± 0,017 | 0,535 ± 0,030 | 0,358 ± 0,063 | **−0,020 (p = 0,041; Wilcoxon 0,065; 2/10)** |
| ETIS-LaribPolypDB | 0,525 ± 0,056 | 0,547 ± 0,044 | 0,456 ± 0,031 | 0,285 ± 0,022 | +0,022 (p = 0,43; 5/10) |

- Hai mô hình YOLO vượt PraNet và U-Net rõ rệt trên cả ba bộ (TSVM so với PraNet: Dice cao hơn ở ColonDB và ETIS 10/10 seed, p < 0,001).
- **TSVM không tốt hơn mô hình gốc trên dữ liệu ngoài.** ClinicDB và ETIS: khác biệt không có ý nghĩa. ColonDB: TSVM thấp hơn, kiểm định t cho p = 0,041 nhưng Wilcoxon p = 0,065, nên chỉ nên viết là "có xu hướng thấp hơn". Phải báo cáo thẳng điểm này.
- Độ lệch chuẩn giữa các seed của TSVM nhỏ hơn mô hình gốc ở cả ba bộ (mô tả, chưa kiểm định).
- Tỉ lệ ảnh bị bỏ sót hoàn toàn (`no_pred_rate`) cao: khoảng 12–13% ở ClinicDB, 29–31% ở ColonDB, 36–39% ở ETIS với hai mô hình YOLO, cho thấy mức sụt giảm do khác miền.

### 20 seed (seed 0–19)

Dice theo pixel, trung bình ± SD (nguồn: `bang/20seed/02_ngoai_thong_ke.csv`):

| Bộ dữ liệu | YOLO26s-seg | + TSVM | PraNet | U-Net | TSVM − YOLO26s-seg (p t; p Wilcoxon; seed TSVM cao hơn) |
|---|---|---|---|---|---|
| CVC-ClinicDB | 0,786 ± 0,018 | 0,770 ± 0,021 | 0,752 ± 0,028 | 0,525 ± 0,032 | **−0,016 (0,006; 0,006; 5/20)** |
| CVC-ColonDB | 0,631 ± 0,023 | 0,601 ± 0,029 | 0,539 ± 0,039 | 0,375 ± 0,055 | **−0,030 (0,0006; 0,0004; 3/20)** |
| ETIS-LaribPolypDB | 0,535 ± 0,053 | 0,529 ± 0,044 | 0,466 ± 0,038 | 0,284 ± 0,019 | −0,005 (0,77; 0,50; 7/20) |

- Với 20 seed, **TSVM thấp hơn mô hình gốc có ý nghĩa thống kê** ở CVC-ClinicDB và CVC-ColonDB (cả kiểm định t và Wilcoxon đều p < 0,01). TSVM cũng bỏ sót trọn ảnh nhiều hơn ở hai bộ này (`no_pred_rate` cao hơn, p < 0,01). Ở ETIS không khác biệt.
- TSVM vẫn cao hơn PraNet ở cả ba bộ (p < 0,05) và cao hơn U-Net rất xa.
- Bộ 20 seed không cho thấy TSVM ổn định hơn trên dữ liệu ngoài: SD của TSVM lớn hơn mô hình gốc ở ClinicDB và ColonDB.
- **Hệ quả cho báo cáo:** dù chốt 10 hay 20 seed, không được viết TSVM tổng quát hóa tốt hơn. Nếu chốt 20 seed, phải nêu rõ TSVM kém mô hình gốc trên hai bộ dữ liệu ngoài. Một giả thuyết hợp lý (chưa kiểm chứng): khối SS2D và nhánh hình dạng được khởi tạo mới và chỉ học từ 1.040 ảnh BG20, nên dễ khớp theo đặc trưng riêng của Kvasir hơn khối C2PSA đã tiền huấn luyện trên COCO.

## Lưu ý khi viết báo cáo

- Đây là đánh giá **khác miền** (domain shift): chỉ số thấp hơn nhiều so với tập kiểm định Kvasir là điều bình thường; không so trực tiếp với số trong các bài báo huấn luyện trên Kvasir + ClinicDB.
- Kết luận theo ghép cặp 10 seed, không dựa vào một seed. Hình minh họa trên ứng dụng (Chương 5, Hình 5.17–5.18) chỉ có tính minh họa.
