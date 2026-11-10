# 11. Giới hạn và hướng phát triển

> Số trong file này tính trên **20 seed (seed 0–19)**, là bộ số dùng trong báo cáo.

## Kết luận được phép viết

1. Thay `C2PSA` bằng `C2TSVMamba` ở tầng 10 làm mask mAP50–95 trung bình tăng **+0,0043** (0,7189 → 0,7232). TSVM tốt hơn ở 13/20 seed. Tuy nhiên p = 0,061 và CI 95% chứa 0, nên **chưa đạt ý nghĩa thống kê** ở α = 0,05.
2. Tại epoch tốt nhất, kết quả của TSVM **dao động ít hơn giữa các seed**: SD nhỏ hơn khoảng 39%, seed kém nhất 0,7065 so với 0,6941. Lợi ích này không còn ở epoch 100.
3. Cái giá phải trả là +7,17% tham số và độ trễ khoảng **gấp 2 lần trên CPU**.

## Không được viết

| Không viết | Lý do |
|---|---|
| "TSVM vượt trội có ý nghĩa thống kê" | p = 0,061 > 0,05 |
| "Hai mô hình tương đương" | p > 0,05 không chứng minh tương đương |
| "TSVM bảo toàn topology / hình dạng polyp tốt hơn" | Lỗi Betti đã đo ([14](14_CHI_SO_TOPOLOGY.md)): TSVM chỉ nhích hơn mô hình gốc, không có ý nghĩa thống kê, kém PraNet rõ rệt. Chưa có Hausdorff/clDice |
| "Nhánh hình dạng / cổng chắc chắn cần thiết" | Ablation 20 seed: ba biến thể đều thấp hơn bản đầy đủ nhưng không chênh lệch nào có ý nghĩa thống kê; chỉ viết "xu hướng" ([15](15_ABLATION_VA_C2PSA_RONG.md)) |
| Quy đổi AP sang Dice | Không quy đổi được. Dice/IoU theo pixel đã được tính riêng ([10](10_SO_SANH_PRANET_UNET.md)) |
| Specificity, accuracy theo ảnh, TN = 40 − FP | TN không xác định ([08](08_MA_TRAN_NHAM_LAN.md)) |
| Hiệu quả lâm sàng; "TSVM tổng quát tốt hơn" | Dữ liệu ngoài (`08_du_lieu_thuc_te/`) là bộ công khai, không phải dữ liệu lâm sàng, không tách theo bệnh nhân. Trên đó TSVM không hơn đối chứng về Dice (kém có ý nghĩa ở ClinicDB, ColonDB) |
| "TSVM ổn định hơn ở mọi epoch" | Có 34/100 epoch SD của TSVM lớn hơn ([07](07_HOI_TU_VA_LOSS.md)) |
| VRAM trên GPU; độ trễ GPU như một con số tuyệt đối | VRAM chưa đo. GFLOPs và độ trễ GPU đã đo, nhưng số ms thay đổi 1,5–2 lần giữa hai phiên đo, chỉ tỉ lệ giữa hai mô hình là ổn định ([09](09_HIEU_NANG_TINH_TOAN.md)) |
| "TSVM vượt PraNet", "TSVM ngang PraNet" | PraNet 640 cao hơn TSVM ở mọi độ đo theo pixel (Dice +0,0316, p < 0,001) và về topology; TSVM chỉ báo nhầm ảnh nền ít hơn ([10](10_SO_SANH_PRANET_UNET.md)) |

## Giới hạn của thiết kế thực nghiệm

1. **Không có tập test riêng.** Cùng 160 ảnh validation được dùng để chọn epoch và để báo cáo, nên có thiên lệch lựa chọn. Phân tích độ nhạy ở [06](06_KET_QUA_20_SEED.md) giảm bớt mối lo này nhưng không loại bỏ được.
2. **Tập validation nhỏ:** 127 đối tượng polyp. Chỉ vài đối tượng phát hiện đúng hay sai cũng làm AP thay đổi đáng kể.
3. **20 seed chỉ phản ánh biến thiên do huấn luyện**, không phải biến thiên do dữ liệu. Không có cross-validation.
4. **Một kiến trúc, một vị trí:** chỉ thử ở tầng 10, scale s, đầu vào 640.
5. **Ablation** (`vmamba_only`, `shape_only`, `shape_vmamba_no_guidance`) và đối chứng **C2PSA rộng** đã chạy đủ 20 seed ([15](15_ABLATION_VA_C2PSA_RONG.md)). Ba biến thể đều thấp hơn bản đầy đủ (−0,0040 / −0,0044 / −0,0031) nhưng không chênh lệch nào có ý nghĩa thống kê (paired t p = 0,17 / 0,09 / 0,15). C2PSA rộng thấp hơn TSVM có ý nghĩa thống kê (−0,0070; p < 0,001). Các biến thể ablation có số tham số khác nhau; C2PSA rộng giúp tách phần do thêm tham số.
6. Một phần tầng 10 của TSVM nhận trọng số của `C2PSA`; phần mới khởi tạo ngẫu nhiên ([04](04_KIEN_TRUC_TSVM_FP32.md#khởi-tạo-trọng-số)). Kết quả có thể phụ thuộc vào cách khởi tạo này.
7. Repo **không lưu notebook đúng phiên bản** đã chạy các lượt TSVM FP32, và không có log Kaggle gắn với 40 lượt chính ([05](05_CAU_HINH_HUAN_LUYEN.md)).
8. ~~Chưa có tài liệu chứng thực nguồn gốc hai danh sách split 880/120.~~ Đã giải quyết 27/10/2026: hai danh sách đi kèm bản Kaggle của tác giả Kvasir-SEG (xem `02_DU_LIEU_BG20.md`).

## Hướng phát triển (theo thứ tự ưu tiên đề xuất)

1. ~~Tính Dice/IoU theo pixel cho 4 mô hình~~: **đã làm** ([10](10_SO_SANH_PRANET_UNET.md)); PraNet/U-Net đã được huấn luyện lại ở 640×640 có tăng cường giống YOLO. Còn có thể làm thêm: tối ưu ngưỡng cho từng mô hình; huấn luyện Polyp-PVT, VM-UNet cùng điều kiện làm mốc Transformer và Mamba.
2. ~~Đánh giá chéo dataset~~: **đã làm ngày 28/10/2026** trên CVC-ClinicDB, CVC-ColonDB, ETIS, PolypGen (`08_du_lieu_thuc_te/`). Còn thiếu: tập test độc lập tách theo bệnh nhân, dữ liệu lâm sàng thật.
3. ~~Ablation 20 seed~~: **đã làm** ([15](15_ABLATION_VA_C2PSA_RONG.md)).
4. ~~Chỉ số topology (lỗi Betti)~~: **đã đo ngày 28/10/2026** ([14](14_CHI_SO_TOPOLOGY.md)). Còn có thể làm thêm: chỉ số hình dạng và biên (Hausdorff 95, Boundary F1), clDice.
5. **Tối ưu tốc độ:** dùng kernel selective-scan, đếm FLOPs đúng cho phép quét. GFLOPs và độ trễ GPU đã đo ([09](09_HIEU_NANG_TINH_TOAN.md)); FLOPs của TSVM vẫn là cận dưới.
6. **Thêm seed hoặc cross-validation** để tăng độ mạnh thống kê. Giả sử hiệu ứng thật đúng bằng d_z = 0,445 quan sát được, paired t-test hai phía (α = 0,05) với 20 cặp chỉ có power khoảng **0,47**. Cần **42 cặp** để đạt power 80%. Con số này tính từ phân phối t không trung tâm và nằm trong log của script. Đây là ước lượng dựa trên chính dữ liệu hiện có, nên chỉ dùng để định hướng.
