# Bộ hình khóa luận và bài báo

Bộ hình được vẽ lại toàn bộ ngày 26/10/2026 từ CSV đã kiểm chứng. Hình cũ đã chuyển sang `99_luu_tru/hinh_cu/`.

- `vi/`: bản tiếng Việt cho khóa luận, rộng 16 cm, dấu phẩy thập phân.
- `en/`: bản tiếng Anh cho bài báo IEEE, rộng một cột 8,9 cm. Riêng `q01` rộng hai cột.
- Mỗi hình có `.png` (300 dpi, chèn Word) và `.pdf` (vector, nộp tạp chí).
- Script: `scripts/ve_hinh.py`. Chạy `python ve_hinh.py` để vẽ tất cả, hoặc `python ve_hinh.py --chi r01 p01` để vẽ một số hình.
- Quy cách:
  - phông mặc định của matplotlib;
  - màu Okabe–Ito: đối chứng `#0072B2`, TSVM `#D55E00`, PraNet `#009E73`, U-Net `#CC79A7`;
  - mỗi hình một biểu đồ, tối đa hai;
  - thanh lỗi là **±1 SD qua 20 seed**, trừ khi có ghi chú khác.
- `du_lieu_dinh_tinh/`: mặt nạ dự đoán seed 0 của 4 mô hình (nén `npz`), do `00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py` tạo, dùng cho hình `q01`.

## Danh mục

Số hình trong báo cáo (ví dụ Hình 6.3) sẽ được gán khi viết từng chương. Cột "Chương" là vị trí dự kiến.

| Mã | Chương | Nội dung | Loại biểu đồ | Nguồn số liệu |
|---|---|---|---|---|
| m01_tham_so_tang10 | 3 | Số tham số từng thành phần của C2TSVMamba, so với C2PSA | Thanh ngang | `bang/08_kien_truc_dung_lai.csv` |
| d01_thanh_phan_bg20 | 4 | Số ảnh polyp và ảnh nền trong train/val | Cột chồng | Đếm trực tiếp nhãn BG20 |
| d02_so_polyp_moi_anh | 4 | Phân bố số polyp mỗi ảnh | Cột kép | Đếm trực tiếp nhãn BG20 |
| d03_so_dinh_polygon | 4 | Số đỉnh của polygon nhãn (1.063 đối tượng) | Histogram | Đếm trực tiếp nhãn BG20 |
| d04_dien_tich_polyp | 4 | Diện tích polyp so với ảnh (thang log) | Histogram | Tính từ polygon (công thức shoelace) |
| h01_cot_kep_chi_so_mask | 6 | Mean ± SD: mask mAP50–95, mAP50, P, R, F1 | Cột kép | `bang/02_ket_qua_tung_seed.csv` |
| h01b_diem_tung_seed_chi_so_mask | 6 | Giá trị từng seed của 5 chỉ số trên | Điểm (tán xạ) | như trên |
| h02_ghep_cap_tung_seed | 6 | mAP50–95 nối cặp theo seed (13 tăng / 7 giảm) | Tán xạ nối cặp | như trên |
| r01_delta_tung_seed | 6 | Δ mAP50–95 từng seed, sắp xếp | Thanh | như trên |
| r02_hop_phan_bo | 6 | Phân bố mAP50–95 của 20 seed | Hộp | như trên |
| r03_histogram_delta | 6 | Phân bố 20 hiệu số ghép cặp | Histogram | như trên |
| r04_do_nhay_quy_tac_epoch | 6 | mAP theo 3 quy tắc chọn epoch, kèm p | Điểm + thanh SD | `bang/04b_do_nhay_quy_tac_epoch.csv` |
| r05_precision_recall | 6 | Precision và Recall từng seed | Tán xạ | `bang/02_ket_qua_tung_seed.csv` |
| h03_duong_mien_mask_map_theo_epoch | 6 | mAP50–95 theo epoch, có ô phóng to 70–100 | Đường + miền ±SD | `bang/05_duong_cong_theo_epoch.csv` |
| c01_val_seg_loss | 6 | Val seg loss theo epoch (▼ là điểm thấp nhất) | Đường + miền ±SD | như trên |
| c02_train_seg_loss | 6 | Train seg loss, có mốc tắt mosaic | Đường | như trên |
| h04_ma_tran_nham_lan | 6 | Ma trận nhầm lẫn trung bình (đối tượng) | Heatmap (2 ô) | `bang/06_ma_tran_nham_lan_tung_seed.csv` |
| e01_tp_fp_fn | 6 | TP/FP/FN mean ± SD | Cột kép | như trên |
| e02_do_tre_cpu | 6 | Độ trễ CPU, forward và pipeline | Cột kép | `04_phan_tich_20seed/efficiency_benchmark/tables/efficiency_summary.csv` |
| e03_tham_so_dung_luong | 6 | Số tham số và bộ nhớ tham số FP32 | Cột (2 biểu đồ) | như trên |
| p01_cot_kep_pixel | 6 | Dice/IoU/P/R theo pixel của 4 mô hình | Cột kép | `bang/11_pixel_tung_seed.csv` |
| p02_diem_dice_tung_seed | 6 | Dice từng seed của 4 mô hình | Điểm (tán xạ) | như trên |
| p03_bao_nham_anh_nen | 6 | Tỉ lệ ảnh nền bị báo nhầm | Cột | như trên |
| q01_minh_hoa_dinh_tinh | 6 | Ảnh gốc, nhãn, dự đoán của 4 mô hình (seed 0, 3 ảnh) | Lưới ảnh | `bang/10_pixel_tung_anh.csv` và `du_lieu_dinh_tinh/` |

Tổng cộng 24 hình. Hai sơ đồ kiến trúc của chương 3 (toàn mô hình và khối TSVMamba) sẽ vẽ khi viết chương 3.

## Ghi chú khi dùng

- `q01` chọn 3 ảnh tự động từ seed 0: ảnh cả 4 mô hình đều tốt nhất; ảnh TSVM hơn đối chứng nhiều nhất; ảnh khó nhất. **Đây chỉ là minh họa**, không dùng để kết luận mô hình nào tốt hơn.
- `h04`: ô nền/nền ghi "không xác định" vì TN không xác định được ở mức đối tượng.
- Biểu đồ cột bắt đầu từ 0. Khi cần thấy chênh lệch nhỏ thì dùng biểu đồ điểm (`h01b`, `h02`, `r04`, `p02`).
