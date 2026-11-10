# 14. Chỉ số topology (lỗi Betti)

> **Cập nhật 10/11/2026:** PraNet và U-Net là bản 640×640 có tăng cường (xem [10](10_SO_SANH_PRANET_UNET.md)). Hai dòng YOLO không đổi. Số khớp mục "cấu trúc vùng" trong Chương 4 của bản Word cuối.

Mục đích: kiểm tra TSVM (tên đầy đủ *Topology-Shape-aware* VMamba) có cho mặt nạ đúng hình dạng tổng thể hơn mô hình gốc không, tức ít vỡ mảnh và ít lỗ thủng hơn. Dice và mAP gần như không phạt các lỗi này vì chúng chỉ chiếm ít pixel.

**Nguồn:** [`scripts/danh_gia_topology.py`](scripts/danh_gia_topology.py) → [bang/pixel_640/13_topology_tung_anh.csv](bang/pixel_640/13_topology_tung_anh.csv) (4 mô hình × 20 seed × 160 ảnh × 2 ngưỡng), [bang/pixel_640/14_topology_tung_seed.csv](bang/pixel_640/14_topology_tung_seed.csv), [bang/pixel_640/15_topology_thong_ke.csv](bang/pixel_640/15_topology_thong_ke.csv). Log: [bang/pixel_640/_log_topology.txt](bang/pixel_640/_log_topology.txt).

## Cách tính

- Giao thức suy luận giống hệt [10](10_SO_SANH_PRANET_UNET.md): nhãn là mặt nạ vẽ từ đa giác ở độ phân giải gốc; YOLO imgsz 640, conf 0,25, iou 0,7, gộp mọi mặt nạ; PraNet/U-Net kéo về 640×640, ngưỡng 0,5.
- **b0** = số mảnh (thành phần liên thông 8 hướng của vùng polyp). **b1** = số lỗ (vùng nền 4 liên thông không chạm biên ảnh).
- Chỉ đếm mảnh và lỗ có diện tích ≥ 20 pixel, trùng ngưỡng loại đốm nhiễu khi tạo nhãn (Chương 4). Ngưỡng 0 (đếm mọi mảnh) ghi kèm để kiểm tra độ nhạy.
- Trên 120 ảnh polyp: nhãn có 113 ảnh 1 mảnh, 7 ảnh 2 mảnh, không ảnh nào có lỗ.
- Chỉ số theo seed: `topo_ok` = tỉ lệ ảnh có cả b0 và b1 khớp nhãn; `err_b0`, `err_b1` = trung bình |dự đoán − nhãn|; `frag_rate` = tỉ lệ ảnh dự đoán **nhiều** mảnh hơn nhãn; `hole_rate` = tỉ lệ ảnh có lỗ; `miss_rate` = tỉ lệ ảnh dự đoán **ít** mảnh hơn nhãn; `bg_b0` = số mảnh thừa trung bình trên 40 ảnh nền.

## Kết quả (ngưỡng 20 pixel, mean ± SD qua 20 seed)

| Chỉ số | YOLO26s-seg | + TSVM | PraNet 640 | U-Net 640 |
|---|---:|---:|---:|---:|
| Ảnh đúng topology (`topo_ok`) ↑ | 0,797 ± 0,027 | 0,808 ± 0,026 | **0,877 ± 0,041** | 0,099 ± 0,031 |
| Lỗi Betti-0 ↓ | 0,198 ± 0,045 | **0,191 ± 0,032** | 0,200 ± 0,163 | 6,043 ± 0,861 |
| Lỗi Betti-1 ↓ | 0,105 ± 0,039 | 0,094 ± 0,027 | **0,026 ± 0,017** | 2,978 ± 0,442 |
| Ảnh vỡ mảnh / thừa mảnh ↓ | **0,082 ± 0,027** | **0,082 ± 0,018** | 0,096 ± 0,039 | 0,846 ± 0,038 |
| Ảnh có lỗ ↓ | 0,073 ± 0,020 | 0,063 ± 0,014 | **0,020 ± 0,013** | 0,690 ± 0,054 |
| Ảnh thiếu mảnh ↓ | 0,071 ± 0,023 | 0,066 ± 0,016 | 0,015 ± 0,010 | **0,002 ± 0,003** |
| Mảnh thừa trên ảnh nền ↓ | **0,015 ± 0,024** | **0,015 ± 0,021** | 0,041 ± 0,015 | 2,360 ± 0,639 |

### So sánh ghép cặp TSVM với mô hình gốc (cùng seed, n = 20)

| Chỉ số | Δ (TSVM − gốc) | Paired t p | Wilcoxon p | TSVM tốt hơn / kém hơn |
|---|---:|---:|---:|---:|
| Ảnh đúng topology | +0,011 | 0,139 | 0,206 | 10 / 8 |
| Lỗi Betti-0 | −0,007 | 0,568 | 0,338 | 10 / 8 |
| Lỗi Betti-1 | −0,011 | 0,350 | 0,444 | 11 / 8 |
| Ảnh có lỗ | −0,010 | 0,099 | 0,221 | 9 / 7 |
| Ảnh vỡ mảnh | +0,000 | 0,953 | 0,948 | 9 / 9 |

Với ngưỡng 0 pixel, kết luận không đổi: ảnh đúng topology 0,770 so với 0,758 (Δ +0,013; p = 0,086; Wilcoxon 0,073).

So với PraNet 640: TSVM có tỉ lệ ảnh đúng topology thấp hơn 0,069 (kém hơn ở 19/20 seed, p < 0,001), nhiều ảnh có lỗ hơn và nhiều ảnh thiếu mảnh hơn (20/20 seed, p < 0,001), nhưng ít mảnh thừa trên ảnh nền hơn (p < 0,001).

## Diễn giải

1. **TSVM không cải thiện topology có ý nghĩa thống kê so với mô hình gốc.** Mọi chỉ số nhích theo chiều có lợi cho TSVM (đúng topology +1,1 điểm %, ít lỗ hơn 1 điểm %), nhưng p > 0,05 ở mọi chỉ số. Chỉ được viết "xu hướng nhỏ, chưa có bằng chứng thống kê", **không** viết "TSVM cải thiện topology".
2. **PraNet 640 có topology tốt nhất** (87,7% ảnh đúng so với 80,8% của TSVM). Mặt nạ PraNet ít lỗ hơn hẳn. Lý do hợp lý: PraNet xuất một bản đồ xác suất trơn rồi lấy ngưỡng, còn YOLO ghép mặt nạ từ prototype 160×160 rồi phóng lên, dễ tạo lỗ và mép răng cưa. Lỗi chính của YOLO là thiếu mảnh do bỏ sót polyp (xem mục 4 của [10](10_SO_SANH_PRANET_UNET.md)).
3. U-Net 640 kém xa cả ba về mọi chỉ số topology (chỉ 9,9% ảnh đúng), chủ yếu do vỡ mảnh và thủng lỗ.
4. Lỗi topology của hai mô hình YOLO chia đều giữa vỡ mảnh, có lỗ và thiếu mảnh (mỗi loại 6–8% số ảnh), không có kiểu lỗi trội hẳn.

## Giới hạn

- Chỉ đo trên 160 ảnh validation, 20 seed của cùng một bộ dữ liệu. Chưa đo topology trên dữ liệu ngoài.
- Nhãn đa giác vốn không có lỗ, nên lỗi Betti-1 bằng đúng số lỗ của dự đoán. Không đo được trường hợp polyp thật có lỗ.
- Ngưỡng 20 pixel tính ở độ phân giải gốc (ảnh rộng 332–1.920 pixel), nên cùng một ngưỡng tương ứng diện tích tương đối khác nhau giữa các ảnh.

## Hình

`06_bao_cao/hinh/ket_qua_20seed_640/{vi,en}/o01_anh_dung_topology`, `o02_kieu_loi_topology`.
