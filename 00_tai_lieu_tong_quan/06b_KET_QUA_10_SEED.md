# 06b. Kết quả 10 seed (seed 0–9): chỉ đối chiếu

> **Cập nhật 28/10/2026:** chủ dự án chốt dùng **20 seed** cho báo cáo ([06](06_KET_QUA_20_SEED.md)). File này giữ lại để đối chiếu, không đưa vào báo cáo.

Ngày 27/10/2026 chủ dự án quyết định lấy **10 seed (seed 0–9)** làm trọng tâm báo cáo. Đây là 10 seed đầu theo thứ tự đã chạy, không chọn lọc theo kết quả. Bộ số 20 seed ([06_KET_QUA_20_SEED.md](06_KET_QUA_20_SEED.md)) vẫn giữ nguyên và **không đưa vào báo cáo**. Số chính thức sẽ chốt sau (xem mục "Chưa chốt").

**Nguồn số liệu:** `bang/10seed/*.csv`. Sinh lại bằng:

```bash
python 00_tai_lieu_tong_quan/scripts/tinh_lai_so_lieu.py --seeds 10
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py --tu-bang --seeds 0 1 2 3 4 5 6 7 8 9 --out 00_tai_lieu_tong_quan/bang/10seed
```

Lệnh thứ hai chỉ lọc `bang/10_pixel_tung_anh.csv` (đã suy luận cho 20 seed) theo seed rồi tổng hợp lại, không suy luận lại. Đã kiểm tra: `11_pixel_tung_seed.csv` của bản 10 seed trùng khớp từng ô với 10 dòng đầu của bản 20 seed (sai lệch lớn nhất bằng 0).

**Hình:** `06_bao_cao/hinh/ket_qua_10seed/{vi,en}/` (16 hình), vẽ bằng `python 06_bao_cao/hinh/scripts/ve_hinh.py` (mặc định `--seeds 10`).

## 1. Chỉ số mặt nạ tại epoch cực đại mask mAP50–95 (endpoint chính)

| Chỉ số | Đối chứng (mean ± SD) | TSVM FP32 (mean ± SD) | Δ (TSVM − ĐC) | CI 95% của Δ | t ghép cặp p | Wilcoxon p | Seed TSVM tốt hơn |
|---|---|---|---|---|---|---|---|
| **Mask mAP50–95** | **0,7210 ± 0,0129** | **0,7246 ± 0,0078** | **+0,0036** | [−0,0052; 0,0123] | **0,384** | 0,432 | **6/10** |
| Mask mAP50 | 0,9119 ± 0,0107 | 0,9062 ± 0,0082 | −0,0056 | [−0,0155; 0,0042] | 0,227 | 0,275 | 3/10 |
| Mask Precision | 0,9023 ± 0,0339 | 0,9118 ± 0,0246 | +0,0095 | [−0,0245; 0,0434] | 0,543 | 0,625 | 5/10 |
| Mask Recall | 0,8584 ± 0,0252 | 0,8625 ± 0,0173 | +0,0041 | [−0,0126; 0,0209] | 0,591 | 0,625 | 6/10 |
| Box mAP50–95 | 0,7262 ± 0,0198 | 0,7285 ± 0,0141 | +0,0023 | [−0,0117; 0,0163] | 0,715 | 0,492 | 6/10 |
| Val seg loss (thấp hơn là tốt) | 1,3045 ± 0,0867 | 1,2424 ± 0,0387 | −0,0622 | [−0,1364; 0,0121] | 0,091 | 0,084 | 8/10 |

Cohen d_z của mask mAP50–95 bằng 0,289. Với hiệu ứng cỡ này, power của kiểm định t ghép cặp ở n = 10 chỉ khoảng 0,13. Cần khoảng 96 cặp seed để đạt power 80%.

**Cách viết trong báo cáo:**
- TSVM có mask mAP50–95 trung bình cao hơn 0,0036 nhưng **không có ý nghĩa thống kê** (p = 0,38; CI 95% chứa 0). Không viết "vượt trội" hay "cải thiện rõ rệt".
- Ở mask mAP50, TSVM **thấp hơn** đối chứng 0,0056 (cũng không có ý nghĩa thống kê). Phải nêu điều này, không được bỏ qua.
- TSVM có SD giữa các seed nhỏ hơn (0,0078 so với 0,0129). Đây là quan sát mô tả, chưa kiểm định.

## 2. Từng seed (mask mAP50–95)

| Seed | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Đối chứng | 0,7366 | 0,7165 | 0,7138 | 0,6941 | 0,7274 | 0,7351 | 0,7153 | 0,7145 | 0,7318 | 0,7253 |
| TSVM | 0,7245 | 0,7274 | 0,7259 | 0,7213 | 0,7197 | 0,7285 | 0,7254 | 0,7065 | 0,7339 | 0,7329 |

## 3. Độ nhạy theo quy tắc chọn epoch (mask mAP50–95)

| Quy tắc | Đối chứng | TSVM | Δ | p (t) | Seed TSVM tốt hơn |
|---|---|---|---|---|---|
| Epoch cực đại mask (endpoint chính) | 0,7210 ± 0,0129 | 0,7246 ± 0,0078 | +0,0036 | 0,384 | 6/10 |
| Epoch fitness box+mask (best.pt) | 0,7194 ± 0,0145 | 0,7241 ± 0,0088 | +0,0046 | 0,315 | 6/10 |
| Epoch 100 | 0,7109 ± 0,0149 | 0,7130 ± 0,0132 | +0,0021 | 0,733 | 6/10 |

Δ dương ở cả ba quy tắc, nhưng không quy tắc nào có ý nghĩa thống kê.

## 4. Ma trận nhầm lẫn (đối tượng, trên 127 polyp của tập kiểm định)

| | TP | FP | FN |
|---|---|---|---|
| Đối chứng | 110,3 ± 3,40 | 16,8 ± 2,35 | 16,7 ± 3,40 |
| TSVM | 110,8 ± 2,35 | 15,8 ± 2,39 | 16,2 ± 2,35 |
| Δ, Wilcoxon p | +0,5; p = 0,71 | −1,0; p = 0,62 | −0,5; p = 0,71 |

## 5. Đánh giá theo pixel, 4 mô hình (120 ảnh polyp; 40 ảnh nền)

| Mô hình | Dice | IoU | Precision | Recall | Ảnh nền bị báo nhầm |
|---|---|---|---|---|---|
| YOLO26s-seg (đối chứng) | 0,8504 ± 0,0217 | 0,7947 ± 0,0214 | 0,8642 ± 0,0189 | 0,8678 ± 0,0241 | 1,0% ± 1,75 |
| YOLO26s-seg + TSVM | 0,8523 ± 0,0141 | 0,7987 ± 0,0141 | 0,8596 ± 0,0185 | 0,8730 ± 0,0128 | 1,5% ± 1,75 |
| PraNet (ResNet-50) | 0,8531 ± 0,0061 | 0,7793 ± 0,0054 | 0,8721 ± 0,0103 | 0,8851 ± 0,0126 | 0,25% ± 0,79 |
| U-Net | 0,7047 ± 0,0211 | 0,6025 ± 0,0216 | 0,7996 ± 0,0223 | 0,7100 ± 0,0251 | 21,25% ± 6,26 |

So sánh ghép cặp theo seed:
- TSVM so với đối chứng: Dice +0,0019 (p = 0,83), IoU +0,0040 (p = 0,64). Không khác biệt có ý nghĩa.
- TSVM so với PraNet: Dice −0,0008 (p = 0,86); IoU +0,0194 (p = 0,0013; TSVM cao hơn ở 10/10 seed).
- TSVM so với U-Net: cao hơn ở mọi chỉ số, 10/10 seed (p < 0,001).

## 6. Không đổi theo số seed

Các số sau không phụ thuộc nhóm seed nên giữ nguyên như bộ tài liệu cũ: số tham số (11.434.463 so với 12.254.688, +7,17%), tham số tầng 10, độ trễ CPU (đo trên checkpoint seed 0), cấu hình huấn luyện. Thời gian huấn luyện trung bình trên 10 seed là 2,32 giờ (đối chứng) và 4,62 giờ (TSVM).

## 7. Chưa chốt

- Chủ dự án chưa quyết định dùng 10 hay 20 seed cho bản cuối. Trong các chương, chỗ nhắc số seed được đánh dấu **[CHỐT SỐ SEED]**.
- So với 20 seed (Δ = +0,0043; p = 0,061; 13/20), bộ 10 seed cho Δ nhỏ hơn và p lớn hơn nhiều. Báo cáo cần một câu giải thích vì sao dùng 10 seed (ví dụ theo thông lệ chung hoặc giới hạn tài nguyên). Lý do cụ thể do chủ dự án cung cấp.
