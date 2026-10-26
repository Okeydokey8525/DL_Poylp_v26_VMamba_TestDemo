# 11. Giới hạn và hướng phát triển

## Kết luận được phép viết

1. Thay `C2PSA` bằng `C2TSVMamba` ở tầng 10 làm mask mAP50–95 trung bình tăng **+0,0043** (0,7189 → 0,7232). TSVM tốt hơn ở 13/20 seed. Tuy nhiên p = 0,061 và CI 95% chứa 0, nên **chưa đạt ý nghĩa thống kê** ở α = 0,05.
2. Tại epoch tốt nhất, kết quả của TSVM **dao động ít hơn giữa các seed**: SD nhỏ hơn khoảng 39%, seed kém nhất 0,7065 so với 0,6941. Lợi ích này không còn ở epoch 100.
3. Cái giá phải trả là +7,17% tham số và độ trễ khoảng **gấp 2 lần trên CPU**.

## Không được viết

| Không viết | Lý do |
|---|---|
| "TSVM vượt trội có ý nghĩa thống kê" | p = 0,061 > 0,05 |
| "Hai mô hình tương đương" | p > 0,05 không chứng minh tương đương |
| "TSVM bảo toàn topology / hình dạng polyp tốt hơn" | Không có chỉ số topology (Betti, clDice), không có Hausdorff, không có ablation |
| Quy đổi AP sang Dice | Không quy đổi được. Dice/IoU theo pixel đã được tính riêng ([10](10_SO_SANH_PRANET_UNET.md)) |
| Specificity, accuracy theo ảnh, TN = 40 − FP | TN không xác định ([08](08_MA_TRAN_NHAM_LAN.md)) |
| Hiệu quả lâm sàng, khả năng tổng quát sang bệnh viện khác | Không có tập test ngoài, không tách theo bệnh nhân |
| "TSVM ổn định hơn ở mọi epoch" | Có 34/100 epoch SD của TSVM lớn hơn ([07](07_HOI_TU_VA_LOSS.md)) |
| GFLOPs, VRAM, FPS trên GPU | Chưa đo ([09](09_HIEU_NANG_TINH_TOAN.md)) |
| "TSVM vượt PraNet" | Dice ngang nhau. TSVM chỉ hơn ở IoU, còn PraNet hơn ở Recall ([10](10_SO_SANH_PRANET_UNET.md)) |

## Giới hạn của thiết kế thực nghiệm

1. **Không có tập test riêng.** Cùng 160 ảnh validation được dùng để chọn epoch và để báo cáo, nên có thiên lệch lựa chọn. Phân tích độ nhạy ở [06](06_KET_QUA_20_SEED.md) giảm bớt mối lo này nhưng không loại bỏ được.
2. **Tập validation nhỏ:** 127 đối tượng polyp. Chỉ vài đối tượng phát hiện đúng hay sai cũng làm AP thay đổi đáng kể.
3. **20 seed chỉ phản ánh biến thiên do huấn luyện**, không phải biến thiên do dữ liệu. Không có cross-validation.
4. **Một kiến trúc, một vị trí:** chỉ thử ở tầng 10, scale s, đầu vào 640.
5. Chưa có **ablation 20 seed** cho các chế độ `vmamba_only`, `shape_only`, `shape_vmamba_no_guidance`. Vì vậy chưa biết thành phần nào tạo ra khác biệt.
6. Một phần tầng 10 của TSVM nhận trọng số của `C2PSA`; phần mới khởi tạo ngẫu nhiên ([04](04_KIEN_TRUC_TSVM_FP32.md#khởi-tạo-trọng-số)). Kết quả có thể phụ thuộc vào cách khởi tạo này.
7. Repo **không lưu notebook đúng phiên bản** đã chạy các lượt TSVM FP32, và không có log Kaggle gắn với 40 lượt chính ([05](05_CAU_HINH_HUAN_LUYEN.md)).
8. Chưa có tài liệu chứng thực nguồn gốc hai danh sách split 880/120.

## Hướng phát triển (theo thứ tự ưu tiên đề xuất)

1. ~~Tính Dice/IoU theo pixel cho 4 mô hình~~: **đã làm ngày 26/10/2026** ([10](10_SO_SANH_PRANET_UNET.md)). Còn có thể làm thêm: huấn luyện PraNet/U-Net cùng cấu hình tăng cường dữ liệu với YOLO, và tối ưu ngưỡng cho từng mô hình.
2. **Tập test độc lập hoặc đánh giá chéo dataset** (ví dụ CVC-ClinicDB, ETIS-Larib) để kiểm tra khả năng tổng quát.
3. **Ablation 20 seed** cho 3 chế độ còn lại của TSVMamba.
4. **Chỉ số hình dạng và biên** (Hausdorff 95, Boundary F1) và **chỉ số topology** (số thành phần liên thông, clDice) để kiểm chứng tên gọi "Topology-Shape".
5. **Tối ưu tốc độ:** dùng kernel selective-scan, đo trên GPU và đếm FLOPs đúng cho phép quét.
6. **Thêm seed hoặc cross-validation** để tăng độ mạnh thống kê. Giả sử hiệu ứng thật đúng bằng d_z = 0,445 quan sát được, paired t-test hai phía (α = 0,05) với 20 cặp chỉ có power khoảng **0,47**. Cần **42 cặp** để đạt power 80%. Con số này tính từ phân phối t không trung tâm và nằm trong log của script. Đây là ước lượng dựa trên chính dữ liệu hiện có, nên chỉ dùng để định hướng.
