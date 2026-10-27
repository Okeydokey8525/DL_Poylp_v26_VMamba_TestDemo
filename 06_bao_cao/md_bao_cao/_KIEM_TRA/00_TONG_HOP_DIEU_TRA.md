# Tổng hợp giai đoạn điều tra (điểm dừng 1), ngày 26/10/2026

Có bốn báo cáo chi tiết trong thư mục này. Các phát hiện quan trọng dưới đây đã được chủ biên kiểm tra lại trực tiếp trong mã nguồn.

| Báo cáo | Phục vụ | Kết quả chính |
|---|---|---|
| [A_gop_y_chuong_4_du_lieu.md](A_gop_y_chuong_4_du_lieu.md) | Ch.4 | Kiểm 94 nhận định: 79 đúng, 9 đúng một phần, 1 sai, 5 không kiểm được. Có danh sách đổi số 3.x thành 4.x |
| [B_ly_thuyet_va_mo_hinh.md](B_ly_thuyet_va_mo_hinh.md) | Ch.2, Ch.3 | Bảng sự thật kiến trúc, công thức, loss và chỉ số; điểm mã khác lý thuyết gốc; lỗi trong bản Word cũ |
| [C_ung_dung_polypvision.md](C_ung_dung_polypvision.md) | Ch.5 | Kiến trúc Web/FastAPI/Flutter, API, kiểm thử; 15 ảnh cần chụp và 3 sơ đồ |
| [D_tai_lieu_tham_khao.md](D_tai_lieu_tham_khao.md) | Mọi chương | 24 tài liệu cũ đều có thật (6 mục sửa nhỏ); thêm 47 tài liệu đã xác minh; danh mục IEEE 71 mục (61 bắt buộc) |

## Phát hiện phải phản ánh đúng trong báo cáo

1. **YOLO26 không dùng NMS** khi suy luận và kiểm định: mô hình end2end chỉ lọc theo conf và lấy top-300 (`utils/nms.py:66`). Tham số `iou=0.7` không có tác dụng. Cơ chế này bắt nguồn từ YOLOv10. *(Đã kiểm.)*
2. **Tầng 22 của cả hai mô hình vẫn có attention**: `C3k2(attn=True)` chứa `PSABlock` (`block.py:1103–1107`). Mô hình đề xuất **chỉ thay attention ở tầng 10**. *(Đã kiểm.)*
3. **`val/sem_loss = 0`** vì nhánh semseg chỉ chạy khi huấn luyện (`block.py:2017`). *(Đã kiểm.)*
4. **Khi kiểm định, ảnh được gom theo tỉ lệ khung (`rect=True`, `pad=0.5`)**, nên khung có cạnh dài **672**, không phải 640 (`detect/train.py:76`, `data/build.py:310`). *(Đã kiểm.)*
5. Phép quét song song trong SS2D có độ sâu log₂L nhưng tổng công việc **O(L log L)**, nên **không gọi là "tuyến tính"**. Mã SS2D không có hệ số skip D, không có LayerNorm đầu ra, và có thêm clamp ΔA.
6. 790.016 tham số của tầng 10 nhận trọng số từ C2PSA (cv1, cv2, m.0.ffn). Bản Word cũ mô tả sai điểm này.
7. Bài YOLO26 dùng bộ tối ưu MuSGD, còn đề tài dùng **AdamW**.
8. Ứng dụng: **không tính diện tích** polyp; so sánh 2 mô hình chạy **tuần tự**; trang `/diagnoses/demo` dùng dữ liệu giả lập; số kiểm thử đã chạy là Java 274/274 và FastAPI 51/51 (ngày 26/10). Con số Flutter 498 chỉ có trong README.
9. **Công trình gần nhất: MambaPSA** (arXiv 2607.12681, preprint). Bài này cũng thay C2PSA của YOLO26 bằng Mamba. Chương 1 phải nêu rõ TSVM khác MambaPSA ở đâu.
10. [12] YOLO26 (arXiv 2606.03748) có thật và là trích dẫn chính thức của Ultralytics, nhưng là preprint chưa qua phản biện.

## Chương 4 (bạn cùng nhóm): các điểm sai hoặc chưa có bằng chứng

- **Sai:** mục 3.4 ghi khung kiểm định 640; đúng là cạnh dài 672 (xem điểm 4 ở trên).
- **Đã có bằng chứng (27/10/2026):** "split 880/120 do tác giả Kvasir-SEG cung cấp" — `train.txt`/`val.txt` và README đi kèm bản Kaggle của D. Jha, trùng md5 với `01_du_lieu/`.
- **Thiếu môi trường chạy:** "tái tạo 1.000/1.000 nhãn" (OpenCV 5.0 cho 1.000/1.000; OpenCV 4.12 chỉ cho 999/1.000).
- **Đúng một phần:**
  - "một nửa số vùng ≤ 10%": thực tế 48,3%;
  - "10 epoch cuối huấn luyện trên ảnh nguyên vẹn": vẫn còn affine, HSV và lật ảnh;
  - log Albumentations là của lượt TSVM cũ;
  - câu kết chương bỏ qua dao động giữa các seed.
- Chi tiết từng câu và câu đề xuất sửa: xem báo cáo A.

## Quyết định cần chủ dự án chốt trước khi viết

1. Chương 4 "giữ nguyên câu chữ". Với lỗi 640/672 và câu về nguồn split, chọn cách xử lý:
   - (a) giữ nguyên và gửi góp ý cho bạn cùng nhóm tự sửa; hoặc
   - (b) cho phép sửa đúng các câu sai, có đánh dấu.
2. Danh mục tài liệu tham khảo: dùng 61 mục bắt buộc, hay thêm cả 10 mục tùy chọn?
3. Đưa MambaPSA vào chương 1 làm công trình liên quan gần nhất (đề xuất: **có**).
