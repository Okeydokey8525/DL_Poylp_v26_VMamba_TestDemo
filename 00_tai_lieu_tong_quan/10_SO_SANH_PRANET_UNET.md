# 10. So sánh với PraNet và U-Net

## Vai trò

PraNet và U-Net là hai mô hình **phân đoạn ngữ nghĩa** (theo pixel) hay được dùng làm mốc trên Kvasir-SEG. Đồ án chỉ dùng chúng để **so sánh chỉ số** với Baseline và TSVM FP32. Chúng không phải mô hình đề xuất.

## Hiện trạng trong repo (kiểm tra ngày 26/10/2026)

| | PraNet | U-Net |
|---|---|---|
| Vị trí | `05_so_sanh_mo_hinh_khac/PraNet/` | `05_so_sanh_mo_hinh_khac/UNet/` |
| Có gì | 20 file `pranet_best_s{0..19}.pth`, mỗi file khoảng 94 MiB | 20 file `best_unet_s{0..19}.pth` |
| Nội dung file | Chỉ có `state_dict` (674 khóa), **không có** metric, epoch hay cấu hình | Chỉ có `state_dict` (118 khóa), **không có** metric |
| Script huấn luyện, log, CSV kết quả | **Không có** trong repo | **Không có** trong repo |

**Kết luận: hiện chưa có số liệu nào của PraNet và U-Net.** Bộ tài liệu này không ghi bất kỳ con số nào cho hai mô hình này.

## Cần lưu ý trước khi so sánh

1. **Khác loại bài toán.** YOLO26-seg báo mAP theo đối tượng (instance), còn PraNet và U-Net thường báo Dice và IoU theo pixel. Hai nhóm chỉ số này **không quy đổi được** cho nhau. Muốn so sánh công bằng thì phải tính **cùng một bộ chỉ số theo pixel** (Dice, IoU, có thể thêm Precision/Recall theo pixel) cho cả 4 mô hình. Với YOLO, cần gộp các mặt nạ instance của mỗi ảnh thành một mặt nạ nhị phân.
2. **Cùng dữ liệu và cùng tập validation:** 160 ảnh BG20, trong đó có 40 ảnh nền. Với ảnh nền, Dice không xác định khi cả nhãn và dự đoán đều rỗng. Cần thống nhất trước cách xử lý (ví dụ tính riêng trên 120 ảnh polyp, và báo số ảnh nền có dự đoán dương tính giả).
3. **Cùng quy tắc chọn checkpoint và cùng 20 seed** để có thể so sánh ghép cặp.
4. Cần lưu lại script huấn luyện và cấu hình của PraNet và U-Net vào repo để truy vết.

## Việc cần làm (chưa thực hiện, cần thống nhất trước)

- Viết script **chỉ suy luận** trên 160 ảnh validation cho cả 4 mô hình × 20 seed, rồi tính Dice và IoU theo pixel với cùng một quy ước.
- Bổ sung kết quả vào file này cùng script tái lập.
