# Bộ hình khóa luận và bài báo

Cập nhật 10/11/2026 (bản nộp). Mọi hình vẽ lại từ CSV đã kiểm chứng trong `00_tai_lieu_tong_quan/bang/`.

Thư mục:
- `chung/`: hình không phụ thuộc nhóm seed (a01–a08, d01–d04, e02, e03, m01, s01, t01). a05–a08 là hình khổ 16:9 vẽ riêng cho slide bảo vệ.
- `ket_qua_20seed/`: hình kết quả của hai mô hình YOLO trên **seed 0–19** (h01, h01b, h02, h03, h04, r01–r05, c01, c02, e01).
- `ket_qua_20seed_640/`: 11 hình có 4 mô hình (p01–p05, q01, o01, o02, x01–x03), PraNet/U-Net **bản ảnh 640×640 có tăng cường** (đọc `bang/pixel_640/`). Nhãn trên hình ghi "PraNet (ResNet-50)", "U-Net"; ghi "ảnh 640×640" ở chú thích hình.
- `ablation_20seed/`: k01, k02 (ablation seed 0–19, `bang/ablation_20seed/17_*`) và k03 (C2PSA rộng, `bang/ablation_20seed/19_*`).
- `chuong4/`: hình của Chương 4 do người viết chương cung cấp.
- `chuong2/`: 4 hình lấy từ bài báo gốc cho Chương 2, ghi nguồn dưới hình: `yolact_mat_na_mau` [YOLACT], `yolo26_kien_truc` và `yolo26_cac_khoi` [YOLO26], `vmamba_ss2d` [VMamba]. Không có bản `vi/`, `en/`.

Trong mỗi thư mục:
- `vi/`: bản tiếng Việt cho khóa luận, rộng 16 cm, dấu phẩy thập phân.
- `en/`: bản tiếng Anh cho bài báo IEEE, rộng một cột 8,9 cm. Riêng `q01` rộng hai cột.
- Mỗi hình có `.png` (300 dpi, chèn Word) và `.pdf` (vector).

Vẽ lại:
- `python scripts/ve_hinh.py`: vẽ tất cả và tự ghi vào đúng thư mục ở trên; `--chi r01 p01` để vẽ một số hình.
- `python scripts/ve_so_do.py`: sơ đồ a01–a08 và s01.
- Đã chạy lại ngày 10/11/2026: mọi hình PNG trùng bản trước 100% điểm ảnh.

Quy cách:
- phông mặc định của matplotlib;
- màu Okabe–Ito: mô hình gốc `#0072B2`, TSVM `#D55E00`, PraNet `#009E73`, U-Net `#CC79A7`;
- mỗi hình một biểu đồ, tối đa hai;
- thanh lỗi là **±1 SD qua 20 seed**, trừ khi có ghi chú khác.

## Danh mục

| Mã | Thư mục | Nội dung | Loại biểu đồ | Nguồn số liệu |
|---|---|---|---|---|
| t01_bon_kieu_dau_ra | chung | Phân loại, hộp bao, mặt nạ ngữ nghĩa, mặt nạ thực thể trên một ảnh val có hai polyp | Lưới ảnh | Nhãn đa giác BG20 |
| s01_kien_truc_ung_dung | chung | Kiến trúc PolypVision (Web, Mobile, FastAPI, hai mô hình) | Sơ đồ | Mã nguồn `Ung_Dung/polypweb` |
| a01–a04 | chung | Kiến trúc tổng thể, khối C2TSVMamba, quét bốn hướng, SS2D | Sơ đồ | Mã `topology_shape_vmamba.py` |
| a05_nhanh_hinh_dang_cong | chung (slide) | Nhân tích chập có hướng, luồng tính S và cổng 1 + G ∈ (1, 2) | Sơ đồ 16:9 | Mã `topology_shape_vmamba.py` |
| a06_quet_song_song | chung (slide) | Quét song song Hillis–Steele trên chuỗi L = 4 | Sơ đồ 16:9 | Mã `topology_shape_vmamba.py` |
| a07_che_do_tach_thanh_phan | chung (slide) | Bốn chế độ của TSVMamba, thành phần bị bỏ vẽ nét đứt, kèm tham số tầng 10 | Sơ đồ 16:9 | `bang/ablation_20seed/17b_ablation_tong_hop.csv` (cột `params_layer10`) |
| a08_uu_nhuoc_diem | chung (slide) | Ưu và hạn chế của mô hình đề xuất dạng thẻ | Thẻ chữ 16:9 | |
| m01_tham_so_tang10 | chung | Số tham số từng thành phần của C2TSVMamba, so với C2PSA | Thanh ngang | `bang/08_kien_truc_dung_lai.csv` |
| d01_thanh_phan_bg20 | chung | Số ảnh polyp và ảnh nền trong train/val | Cột chồng | Đếm trực tiếp nhãn BG20 |
| d02_so_polyp_moi_anh | chung | Phân bố số polyp mỗi ảnh | Cột kép | Đếm trực tiếp nhãn BG20 |
| d03_so_dinh_polygon | chung | Số đỉnh của polygon nhãn (1.063 đối tượng) | Histogram | Đếm trực tiếp nhãn BG20 |
| d04_dien_tich_polyp | chung | Diện tích polyp so với ảnh (thang log) | Histogram | Tính từ polygon (công thức shoelace) |
| e02_do_tre_cpu | chung | Độ trễ CPU, forward và pipeline | Cột kép | `04_phan_tich_20seed/efficiency_benchmark/tables/efficiency_summary.csv` |
| e03_tham_so_dung_luong | chung | Số tham số và bộ nhớ tham số FP32 | Cột (2 biểu đồ) | như trên |
| h01_cot_kep_chi_so_mask | ket_qua_20seed | Mean ± SD: mask mAP50–95, mAP50, P, R, F1 | Cột kép | `bang/02_ket_qua_tung_seed.csv` |
| h01b_diem_tung_seed_chi_so_mask | ket_qua_20seed | Giá trị từng seed của 5 chỉ số trên | Điểm | như trên |
| h02_ghep_cap_tung_seed | ket_qua_20seed | mAP50–95 nối cặp theo seed (13 tăng / 7 giảm) | Tán xạ nối cặp | như trên |
| r01_delta_tung_seed | ket_qua_20seed | Δ mAP50–95 từng seed, sắp xếp | Thanh | như trên |
| r02_hop_phan_bo | ket_qua_20seed | Phân bố mAP50–95 theo seed | Hộp | như trên |
| r03_histogram_delta | ket_qua_20seed | Phân bố 20 hiệu số ghép cặp | Histogram | như trên |
| r04_do_nhay_quy_tac_epoch | ket_qua_20seed | mAP theo 3 quy tắc chọn epoch, kèm p | Điểm + thanh SD | `bang/04b_do_nhay_quy_tac_epoch.csv` |
| r05_precision_recall | ket_qua_20seed | Precision và Recall từng seed | Tán xạ | `bang/02_ket_qua_tung_seed.csv` |
| h03_duong_mien_mask_map_theo_epoch | ket_qua_20seed | mAP50–95 theo epoch, có ô phóng to 70–100 | Đường + miền ±SD | `bang/05_duong_cong_theo_epoch.csv` |
| c01_val_seg_loss | ket_qua_20seed | Val seg loss theo epoch (▼ là điểm thấp nhất) | Đường + miền ±SD | như trên |
| c02_train_seg_loss | ket_qua_20seed | Train seg loss, có mốc tắt mosaic | Đường | như trên |
| h04_ma_tran_nham_lan | ket_qua_20seed | Ma trận nhầm lẫn trung bình (đối tượng) | Heatmap (2 ô) | `bang/06_ma_tran_nham_lan_tung_seed.csv` |
| e01_tp_fp_fn | ket_qua_20seed | TP/FP/FN mean ± SD | Cột kép | như trên |
| p01_cot_kep_pixel | ket_qua_20seed_640 | Dice/IoU/P/R theo pixel của 4 mô hình | Cột kép | `bang/pixel_640/11_pixel_tung_seed.csv` |
| p02_diem_dice_tung_seed | ket_qua_20seed_640 | Dice từng seed của 4 mô hình | Điểm | như trên |
| p03_bao_nham_anh_nen | ket_qua_20seed_640 | Tỉ lệ ảnh nền bị báo nhầm | Cột | như trên |
| p04_bao_nham_cecum | ket_qua_20seed_640 | Tỉ lệ 800 ảnh normal-cecum chưa dùng bị báo nhầm, 4 mô hình | Cột | `bang/pixel_640/nen_cecum/06_nen_cecum_tung_seed.csv` |
| p05_loi_cap_anh | ket_qua_20seed_640 | Lỗi theo ảnh trên 160 ảnh val: ảnh polyp bỏ sót cả ảnh (FN/120), ảnh nền báo nhầm (FP/40) | Cột nhóm | `bang/pixel_640/20_ma_tran_anh_tung_seed.csv` |
| q01_minh_hoa_dinh_tinh | ket_qua_20seed_640 | Ảnh gốc, nhãn, dự đoán của 4 mô hình (seed 0, 3 ảnh); Hình 4.10 bản Word | Lưới ảnh | `bang/pixel_640/10_pixel_tung_anh.csv` và `bang/pixel_640/du_lieu_dinh_tinh/` |
| o01_anh_dung_topology | ket_qua_20seed_640 | Tỉ lệ ảnh polyp có số mảnh và số lỗ khớp nhãn, 4 mô hình | Cột | `bang/pixel_640/14_topology_tung_seed.csv` (ngưỡng 20 pixel) |
| o02_kieu_loi_topology | ket_qua_20seed_640 | Ba kiểu lỗi topology: thừa mảnh, có lỗ, thiếu mảnh | Cột nhóm | như trên |
| x01_dice_du_lieu_ngoai | ket_qua_20seed_640 | Dice của 4 mô hình trên CVC-ClinicDB, CVC-ColonDB, ETIS-Larib, PolypGen; Hình 4.11 bản Word | Cột nhóm | `bang/pixel_640/du_lieu_ngoai/20seed/01_ngoai_tung_seed.csv` |
| x02_dice_polypgen_trung_tam | ket_qua_20seed_640 | Dice trên từng trung tâm C1–C6 của PolypGen | Cột nhóm | như trên |
| x03_bao_nham_polypgen | ket_qua_20seed_640 | Tỉ lệ 125 ảnh không polyp của PolypGen bị báo nhầm | Cột | như trên |
| k01_ablation_tung_seed | ablation_20seed | mask mAP50–95 từng seed của 5 cấu hình | Điểm nối cặp | `bang/ablation_20seed/17_ablation_tung_seed.csv` |
| k02_ablation_delta | ablation_20seed | Δ của 3 biến thể so với TSVM đầy đủ, cột ± 1 SD và điểm từng seed | Cột + điểm | như trên |
| k03_c2psa_rong | ablation_20seed | mAP50–95 từng seed của mô hình gốc, C2PSA rộng, TSVM | Điểm nối cặp | `bang/ablation_20seed/19_c2psa_rong_tung_seed.csv` |

## Ghi chú khi dùng

- `q01` chọn 3 ảnh tự động từ seed 0: ảnh cả 4 mô hình đều tốt nhất; ảnh TSVM hơn mô hình gốc nhiều nhất; ảnh khó nhất. **Đây chỉ là minh họa**, không dùng để kết luận mô hình nào tốt hơn.
- `h04`: ô nền/nền ghi "không xác định" vì TN không xác định được ở mức đối tượng.
- Biểu đồ cột bắt đầu từ 0. Khi cần thấy chênh lệch nhỏ thì dùng biểu đồ điểm (`h01b`, `h02`, `r04`, `p02`).
