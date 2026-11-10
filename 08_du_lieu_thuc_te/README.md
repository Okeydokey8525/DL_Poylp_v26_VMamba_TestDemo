# 08. Đánh giá trên dữ liệu khác nguồn

> **Cập nhật 10/11/2026 (bản nộp):** PraNet và U-Net là bản **640×640 có tăng cường** (`pranet640`, `unet640`); kết quả **20 seed** (seed 0–19). Bảng tổng hợp nằm ở `00_tai_lieu_tong_quan/bang/pixel_640/du_lieu_ngoai/20seed/` và `pixel_640/nen_cecum/`. Số khớp Mục 4.7 của bản Word cuối.

Lấy các checkpoint đã huấn luyện trên BG20 (Kvasir-SEG + ảnh nền), chạy thẳng trên **bốn bộ dữ liệu khác nguồn**, không huấn luyện lại, không tinh chỉnh. Thêm một phép đo báo nhầm trên **800 ảnh manh tràng** cùng nguồn Kvasir nhưng chưa dùng khi huấn luyện.

## Dữ liệu (chỉ đọc, không chép vào đây)

| Khóa | Bộ dữ liệu | Số ảnh | Kích thước | Đường dẫn (cạnh thư mục dự án) |
|---|---|---:|---|---|
| `clinicdb` | CVC-ClinicDB | 612 | 384×288 | `DeepLearning/Dataset/CVC-ClinicDB/PNG/{Original, Ground Truth}` |
| `colondb` | CVC-ColonDB | 380 | 574×500 | `DeepLearning/Dataset/CVC-ColonDB_data/CVC-ColonDB/{images, masks}` |
| `etis` | ETIS-LaribPolypDB | 196 | 1225×966 | `DeepLearning/Dataset/ETIS-Larib PolypDB/{images, masks}` |
| `pg_c1` … `pg_c6` | PolypGen2021, 6 trung tâm | 1.537 | tới 1920×1080 | `DeepLearning/Dataset/PolypGen2021_MultiCenterData_v3/.../data_C*/images_C*` |
| `cecum800` | 800 ảnh normal-cecum của Kvasir v2 không nằm trong BG20 | 800 | | `01_du_lieu/tao_BG20/` |

- Các bộ CVC và ETIS là khung hình cắt từ video nội soi, khác thiết bị và trung tâm so với Kvasir-SEG. Đây là dữ liệu công khai khác nguồn, **không phải dữ liệu lâm sàng** thu tại bệnh viện, và không tách theo bệnh nhân.
- Mặt nạ được nhị phân hóa ở ngưỡng > 127.
- PolypGen: **125 ảnh có mặt nạ rỗng** (không có polyp: C1 5, C2 31, C3 1, C4 81, C5 2, C6 5). Các ảnh này không tính vào Dice/IoU (1.412 ảnh có polyp) mà dùng để đo tỉ lệ ảnh không polyp bị báo nhầm (`bg_fp_image_rate`). Bộ gốc có ảnh `C3_EndoCV2021_00489].jpg` thừa dấu `]`; script bỏ dấu này khi tìm mặt nạ, không đổi tên tệp gốc. Giấy phép: `readme.md` ghi CC BY 4.0, `license.txt` ghi CC BY-NC-SA 4.0; cả hai cho phép dùng trong khóa luận.

**Kiểm tra trùng ảnh PolypGen với Kvasir-SEG** (`scripts/kiem_tra_trung_polypgen.py`): so 1.537 ảnh với 1.000 ảnh Kvasir-SEG bằng md5, pHash/dHash 64 bit và tương quan ảnh xám 64×64 sau khi cắt viền đen. Kết quả: 0 cặp trùng md5, tương quan cao nhất 0,899; đã xem bằng mắt 8 cặp gần nhất, đều là ảnh khác nhau. Không loại ảnh nào. Bảng: `bang/polypgen_trung/`.

**Kiểm tra gần trùng 800 ảnh manh tràng** với 160 ảnh nền huấn luyện (tương quan ảnh xám ≥ 0,95): `bang/nen_cecum/00_gan_trung_voi_train.csv`. Không ảnh nào gần trùng (tương quan cao nhất 0,934), nên số "không gần trùng" bằng số trên cả 800 ảnh.

## Mô hình và giao thức

- 4 mô hình × seed 0–19: YOLO26s-seg, YOLO26s-seg + TSVM FP32, PraNet (ResNet-50) 640, U-Net 640. Thêm ba biến thể ablation và C2PSA rộng trên CVC-ClinicDB, CVC-ColonDB.
- Giao thức suy luận giống hệt `00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py` (các script ở đây gọi lại hàm của script đó):
  - YOLO: imgsz 640, conf 0,25, iou 0,7, `retina_masks=True`, `half=False`; gộp mọi mặt nạ của ảnh thành một.
  - PraNet/U-Net: kéo về 640×640, ngưỡng 0,5, phóng về kích thước gốc.
- Chỉ số theo pixel: Dice, IoU, Precision, Recall (trung bình theo ảnh), Dice/IoU gộp toàn tập (`_micro`), tỉ lệ ảnh có polyp mà mô hình không dự đoán điểm nào (`no_pred_rate`, tức bỏ sót cả ảnh).
- So sánh ghép cặp theo seed giữa TSVM và từng mô hình: kiểm định t ghép cặp và Wilcoxon.

## Kết quả 20 seed

Dice theo pixel, trung bình ± SD (nguồn: `00_tai_lieu_tong_quan/bang/pixel_640/du_lieu_ngoai/20seed/02_ngoai_thong_ke.csv`):

| Bộ dữ liệu | YOLO26s-seg | + TSVM | PraNet 640 | U-Net 640 | TSVM − gốc (p t; p Wilcoxon; seed TSVM cao hơn) |
|---|---|---|---|---|---|
| CVC-ClinicDB | 0,786 ± 0,018 | 0,770 ± 0,021 | 0,769 ± 0,015 | 0,600 ± 0,035 | **−0,016 (0,006; 0,006; 5/20)** |
| CVC-ColonDB | 0,631 ± 0,023 | 0,601 ± 0,029 | 0,586 ± 0,017 | 0,425 ± 0,042 | **−0,030 (< 0,001; < 0,001; 3/20)** |
| ETIS-LaribPolypDB | 0,535 ± 0,053 | 0,529 ± 0,044 | 0,551 ± 0,046 | 0,365 ± 0,035 | −0,005 (0,77; 0,50; 7/20) |
| PolypGen (gộp 1.412 ảnh) | 0,719 ± 0,021 | 0,715 ± 0,014 | 0,723 ± 0,015 | 0,519 ± 0,029 | −0,004 (0,55; 0,25; 7/20) |

PolypGen theo trung tâm (Dice trung bình):

| Trung tâm | Ảnh có polyp | YOLO26s-seg | + TSVM | PraNet 640 | U-Net 640 | TSVM − gốc (p t; p Wilcoxon) |
|---|---:|---:|---:|---:|---:|---|
| C1 | 251 | 0,753 | 0,752 | 0,734 | 0,559 | −0,001 (0,85; 0,87) |
| C2 | 270 | 0,753 | 0,749 | 0,778 | 0,552 | −0,005 (0,52; 0,50) |
| C3 | 456 | 0,855 | 0,856 | 0,856 | 0,634 | +0,002 (0,69; 0,99) |
| C4 | 146 | 0,516 | 0,503 | 0,530 | 0,290 | −0,013 (0,28; 0,048) |
| C5 | 206 | 0,474 | 0,472 | 0,495 | 0,333 | −0,002 (0,85; 0,45) |
| C6 | 83 | 0,720 | 0,699 | 0,682 | 0,516 | **−0,021 (0,032; 0,019)** |

**Diễn giải:**
- **TSVM không tốt hơn mô hình gốc trên dữ liệu khác nguồn.** TSVM thấp hơn có ý nghĩa thống kê trên CVC-ClinicDB và CVC-ColonDB (cả hai kiểm định p < 0,01); ngang nhau trên ETIS-Larib và PolypGen gộp. Theo trung tâm, chỉ C6 (83 ảnh) có TSVM thấp hơn ở cả hai kiểm định.
- Phần giảm Dice của TSVM trên ClinicDB và ColonDB đến từ việc **bỏ sót cả polyp**: `no_pred_rate` của TSVM so với mô hình gốc là 13,4% so với 11,3% (ClinicDB, p = 0,003) và 32,0% so với 28,2% (ColonDB, p < 0,001).
- So với PraNet 640: TSVM ngang PraNet trên ClinicDB, ColonDB (p > 0,05), ETIS và PolypGen gộp (p > 0,05); PraNet cao hơn ở C2, C4, C5, TSVM cao hơn ở C1, C6. U-Net 640 thấp nhất ở mọi bộ.
- **Báo nhầm trên 125 ảnh không polyp của PolypGen:** YOLO26s-seg 13,3%, TSVM 10,8%, PraNet 640 15,9%, U-Net 640 81,9%. TSVM thấp hơn mô hình gốc 2,5 điểm % (p = 0,011; Wilcoxon 0,018), chủ yếu nhờ C2 và C4; thấp hơn PraNet 5,1 điểm % (p < 0,001).
- Một giả thuyết (chưa kiểm chứng): khối SS2D và nhánh hình dạng được khởi tạo mới và chỉ học từ 1.040 ảnh BG20, nên dễ khớp theo đặc trưng riêng của Kvasir hơn khối C2PSA đã tiền huấn luyện trên COCO.

### Báo nhầm trên 800 ảnh manh tràng chưa dùng

Nguồn: `00_tai_lieu_tong_quan/bang/pixel_640/nen_cecum/07_nen_cecum_thong_ke.csv`.

| Mô hình | Tỉ lệ ảnh bị báo nhầm (mean ± SD, 20 seed) | So với 40 ảnh nền kiểm định |
|---|---:|---:|
| YOLO26s-seg | 1,3% ± 0,5 | 1,2% |
| + TSVM | 1,4% ± 0,5 | 1,5% |
| PraNet 640 | 3,9% ± 1,0 | 2,8% |
| U-Net 640 | 61,1% ± 6,2 | 57,4% |

Hai mô hình YOLO báo nhầm như nhau trên ảnh manh tràng (p = 0,76), nên ưu điểm báo nhầm ít hơn của TSVM chỉ thấy trên PolypGen (khác nguồn). TSVM báo nhầm ít hơn PraNet 640 (p < 0,001).

### Ablation và C2PSA rộng trên CVC (20 seed)

Nguồn: `bang/ablation_ngoai/20seed/02_ablation_ngoai_thong_ke.csv`. Dice trung bình:

| Biến thể | CVC-ClinicDB | Δ so với gốc (p t) | CVC-ColonDB | Δ so với gốc (p t) |
|---|---:|---:|---:|---:|
| Gốc | 0,786 | | 0,631 | |
| TSVM đầy đủ | 0,770 | −0,016 (0,006) | 0,601 | −0,030 (< 0,001) |
| `vmamba_only` | 0,777 | −0,009 (0,040) | 0,608 | −0,023 (0,014) |
| `shape_only` | 0,778 | −0,008 (0,090) | 0,609 | −0,022 (0,006) |
| `shape_vmamba_no_guidance` | 0,774 | −0,012 (0,037) | 0,616 | −0,015 (0,134) |
| C2PSA rộng | 0,779 | −0,007 (0,162) | 0,602 | −0,029 (< 0,001) |

Mọi biến thể đều thấp hơn mô hình gốc trên cả hai bộ CVC, kể cả C2PSA rộng (không có SS2D hay nhánh hình dạng). TSVM không khác các biến thể còn lại có ý nghĩa thống kê (p > 0,05). Như vậy mức giảm trên CVC không gắn riêng với một thành phần của C2TSVMamba.

## Chạy lại

```bash
cd 08_du_lieu_thuc_te/scripts
C:\venv_kl_gpu\Scripts\python.exe danh_gia_du_lieu_ngoai.py                 # 4 mô hình × seed 0–19 × mọi bộ
C:\venv_kl_gpu\Scripts\python.exe danh_gia_du_lieu_ngoai.py --chi-tong-hop  # chỉ tổng hợp lại bảng
C:\venv_kl_gpu\Scripts\python.exe danh_gia_nen_cecum.py --chi-tong-hop      # 800 ảnh manh tràng
C:\venv_kl_gpu\Scripts\python.exe danh_gia_ablation_ngoai.py                # biến thể ablation, C2PSA rộng trên CVC
C:\venv_kl_gpu\Scripts\python.exe tong_hop_ablation_ngoai.py
```

Mỗi lượt (bộ dữ liệu, mô hình, seed) ghi một tệp riêng trong `bang/tung_luot/`, nên chạy lại sẽ bỏ qua lượt đã xong. Đã chạy thử `--chi-tong-hop` ngày 10/11/2026: bảng tổng hợp sinh lại giống hệt.

## Cấu trúc

```
08_du_lieu_thuc_te/
├── README.md
├── scripts/                danh_gia_du_lieu_ngoai.py, danh_gia_nen_cecum.py, danh_gia_ablation_ngoai.py,
│                           tong_hop_ablation_ngoai.py, kiem_tra_trung_polypgen.py
├── bang/
│   ├── tung_luot/                <bộ>_<mô hình>_s<seed>.csv: TP/FP/FN từng ảnh của từng lượt
│   ├── tung_luot_ablation/       như trên, cho biến thể ablation và C2PSA rộng
│   ├── ablation_ngoai/20seed/    bảng tổng hợp ablation trên CVC
│   ├── nen_cecum/                kiểm tra gần trùng, từng lượt trên 800 ảnh manh tràng, log
│   ├── polypgen_trung/           kiểm tra trùng PolypGen với Kvasir-SEG
│   └── _log_chay_640.txt, _log_chay_ablation_20seed.txt
└── du_lieu_dinh_tinh/      mặt nạ dự đoán seed 0 (pred_seed0_<bộ>_<mô hình>.npz), cho hình minh họa
```

## Lưu ý khi viết báo cáo

- Đây là đánh giá **khác miền**: chỉ số thấp hơn nhiều so với tập kiểm định Kvasir là bình thường; không so trực tiếp với số trong các bài báo huấn luyện trên Kvasir + ClinicDB.
- Không viết "TSVM tổng quát hóa tốt hơn". Phải nêu rõ TSVM thấp hơn mô hình gốc trên hai bộ CVC.
