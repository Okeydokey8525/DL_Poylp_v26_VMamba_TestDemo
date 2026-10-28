# 14. Chỉ số topology (lỗi Betti)

Bổ sung ngày 28/10/2026. Mục đích: kiểm tra xem TSVM (tên đầy đủ *Topology-Shape-aware* VMamba) có cho mặt nạ đúng hình dạng tổng thể hơn mô hình gốc không, tức ít vỡ mảnh và ít lỗ thủng hơn. Dice và mAP gần như không phạt các lỗi này vì chúng chỉ chiếm ít pixel.

**Nguồn:** [`scripts/danh_gia_topology.py`](scripts/danh_gia_topology.py) → [bang/13_topology_tung_anh.csv](bang/13_topology_tung_anh.csv) (4 mô hình × 20 seed × 160 ảnh × 2 ngưỡng), [bang/14_topology_tung_seed.csv](bang/14_topology_tung_seed.csv), [bang/15_topology_thong_ke.csv](bang/15_topology_thong_ke.csv). Bản 10 seed (đối chiếu) ở `bang/10seed/`. Log: [bang/_log_topology.txt](bang/_log_topology.txt), 10,2 phút suy luận trên RTX 5050 Laptop.

## Cách tính

- Giao thức suy luận giống hệt [10](10_SO_SANH_PRANET_UNET.md): nhãn là mặt nạ vẽ từ đa giác ở độ phân giải gốc; YOLO imgsz 640, conf 0,25, iou 0,7, gộp mọi mặt nạ; PraNet/U-Net resize 352, ngưỡng 0,5.
- **b0** = số mảnh (thành phần liên thông 8 hướng của vùng polyp). **b1** = số lỗ (vùng nền 4 liên thông không chạm biên ảnh).
- Chỉ đếm mảnh và lỗ có diện tích ≥ 20 pixel, trùng ngưỡng loại đốm nhiễu khi tạo nhãn (Chương 4). Ngưỡng 0 (đếm mọi mảnh) ghi kèm để kiểm tra độ nhạy.
- Trên 120 ảnh polyp: nhãn có 113 ảnh 1 mảnh, 7 ảnh 2 mảnh, không ảnh nào có lỗ.
- Chỉ số theo seed: `topo_ok` = tỉ lệ ảnh có cả b0 và b1 khớp nhãn; `err_b0`, `err_b1` = trung bình |dự đoán − nhãn|; `frag_rate` = tỉ lệ ảnh dự đoán **nhiều** mảnh hơn nhãn; `hole_rate` = tỉ lệ ảnh có lỗ; `miss_rate` = tỉ lệ ảnh dự đoán **ít** mảnh hơn nhãn; `bg_b0` = số mảnh thừa trung bình trên 40 ảnh nền.

## Kết quả (ngưỡng 20 pixel, mean ± SD qua 20 seed)

| Chỉ số | YOLO26s-seg | + TSVM | PraNet | U-Net |
|---|---:|---:|---:|---:|
| Ảnh đúng topology (`topo_ok`) ↑ | 0,797 ± 0,027 | 0,808 ± 0,026 | **0,914 ± 0,021** | 0,260 ± 0,045 |
| Lỗi Betti-0 ↓ | 0,198 ± 0,045 | 0,191 ± 0,032 | **0,086 ± 0,025** | 2,745 ± 0,641 |
| Lỗi Betti-1 ↓ | 0,105 ± 0,039 | 0,094 ± 0,027 | **0,004 ± 0,006** | 1,215 ± 0,419 |
| Ảnh vỡ mảnh / thừa mảnh ↓ | 0,082 ± 0,027 | 0,082 ± 0,018 | **0,057 ± 0,021** | 0,638 ± 0,046 |
| Ảnh có lỗ ↓ | 0,073 ± 0,020 | 0,063 ± 0,014 | **0,004 ± 0,005** | 0,432 ± 0,069 |
| Ảnh thiếu mảnh ↓ | 0,071 ± 0,023 | 0,066 ± 0,016 | **0,027 ± 0,008** | 0,028 ± 0,016 |
| Mảnh thừa trên ảnh nền ↓ | 0,015 ± 0,024 | 0,015 ± 0,021 | **0,009 ± 0,015** | 0,489 ± 0,182 |

### So sánh ghép cặp TSVM với mô hình gốc (cùng seed, n = 20)

| Chỉ số | Δ (TSVM − gốc) | Paired t p | Wilcoxon p | TSVM tốt hơn / kém hơn |
|---|---:|---:|---:|---:|
| Ảnh đúng topology | +0,011 | 0,139 | 0,206 | 10 / 8 |
| Lỗi Betti-0 | −0,007 | 0,568 | 0,338 | 10 / 8 |
| Lỗi Betti-1 | −0,011 | 0,350 | 0,444 | 11 / 8 |
| Ảnh có lỗ | −0,010 | 0,099 | 0,221 | 9 / 7 |
| Ảnh vỡ mảnh | +0,000 | 0,953 | 0,948 | 9 / 9 |

Với ngưỡng 0 pixel, kết luận không đổi: ảnh đúng topology 0,758 so với 0,770 (Δ +0,013; p = 0,086; Wilcoxon 0,073).

## Diễn giải

1. **TSVM không cải thiện topology có ý nghĩa thống kê so với mô hình gốc.** Mọi chỉ số đều nhích theo chiều có lợi cho TSVM (đúng topology +1,1 điểm %, ít lỗ hơn 1 điểm %), nhưng p > 0,05 ở mọi chỉ số. Chỉ được viết là "xu hướng nhỏ, chưa có bằng chứng thống kê". **Không** được viết "TSVM cải thiện topology".
2. **PraNet có topology tốt nhất, rõ rệt** (91% ảnh đúng so với 81% của TSVM, TSVM kém hơn ở 20/20 seed, p < 0,001). Mặt nạ của PraNet hầu như không có lỗ. Lý do hợp lý: PraNet xuất một bản đồ xác suất trơn rồi lấy ngưỡng, còn YOLO ghép mặt nạ từ prototype 160×160 rồi phóng lên, dễ tạo lỗ và mép răng cưa. Đây là điểm cần nêu thẳng khi so sánh, cùng với việc TSVM có IoU cao hơn PraNet ([10](10_SO_SANH_PRANET_UNET.md)).
3. U-Net kém xa cả ba về mọi chỉ số topology (chỉ 26% ảnh đúng).
4. Lỗi topology của hai mô hình YOLO chia đều giữa vỡ mảnh, có lỗ và thiếu mảnh (mỗi loại 6–8% số ảnh), không có một kiểu lỗi trội hẳn.

## Giới hạn

- Chỉ đo trên 160 ảnh validation, 20 seed của cùng một bộ dữ liệu. Chưa đo topology trên dữ liệu ngoài.
- Nhãn đa giác vốn không có lỗ, nên lỗi Betti-1 bằng đúng số lỗ của dự đoán. Không đo được trường hợp polyp thật có lỗ.
- Ngưỡng 20 pixel tính ở độ phân giải gốc (ảnh 332–1.920 pixel chiều rộng), nên cùng một ngưỡng tương ứng diện tích tương đối khác nhau giữa các ảnh.
