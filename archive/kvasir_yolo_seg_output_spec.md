# ĐẶC TẢ ĐẦU RA VÀ HỆ THỐNG DỮ LIỆU HÌNH ẢNH CỦA SCRIPT `convert_kvasir_to_yolo_seg.py`

> **Dự án khóa luận:** *Nghiên cứu phương pháp tích hợp VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng.*  
> **Tập dữ liệu gốc:** Kvasir-SEG (1.000 ảnh nội soi đường tiêu hóa và mặt nạ nhị phân chuyên gia).  
> **Script xử lý:** [`convert_kvasir_to_yolo_seg.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/convert_kvasir_to_yolo_seg.py)  
> **Thư mục đầu ra:** [`Kvasir_YOLO_SEG/`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Kvasir_YOLO_SEG)  

---

## 1. TỔNG QUAN CẤU TRÚC ĐẦU RA (DATASET STRUCTURE)

Khi thực thi script [`convert_kvasir_to_yolo_seg.py`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/convert_kvasir_to_yolo_seg.py), toàn bộ dữ liệu ảnh, nhãn phân đoạn, báo cáo thống kê và đồ thị trực quan được tổ chức chuẩn hóa theo định dạng của **Ultralytics YOLO Segmentation** (tương thích trực tiếp với YOLOv11-seg, YOLOv12-seg, YOLO26-seg và YOLO26-VMamba-seg):

```text
Kvasir_YOLO_SEG/
├── dataset.yaml                  # Cấu hình huấn luyện YOLO
├── dataset_statistics.csv        # Bảng dữ liệu thống kê từng polyp (CSV)
├── dataset_summary.json          # Tóm tắt phân bố dữ liệu dạng JSON
├── report.txt                    # Báo cáo tổng kết khoa học
│
├── images/                       # [LOẠI 1] Tập ảnh huấn luyện & kiểm định
│   ├── train/                    # 880 ảnh (.jpg) nguyên bản
│   └── val/                      # 120 ảnh (.jpg) nguyên bản
│
├── labels/                       # Nhãn đa giác phân đoạn tương ứng
│   ├── train/                    # 880 tệp nhãn (.txt) chuẩn hóa
│   └── val/                      # 120 tệp nhãn (.txt) chuẩn hóa
│
├── preview/                      # [LOẠI 2] 20 ảnh trực quan hóa đối chứng
│   ├── preview_01_train_*.jpg
│   ├── ...
│   └── preview_20_train_*.jpg
│
└── dataset_plots/                # [LOẠI 3] 5 ảnh đồ thị thống kê chuẩn xuất bản
    ├── hist_polygon_points.png   # Phân bố số điểm đa giác sau tối ưu
    ├── hist_contour_area.png     # Phân bố diện tích viền polyp
    ├── hist_bbox_area.png        # Phân bố diện tích bounding box
    ├── hist_aspect_ratio.png     # Phân bố tỷ lệ khung hình (W/H)
    └── hist_image_resolution.png # Biểu đồ các độ phân giải ảnh phổ biến
```

---

## 2. CHI TIẾT 3 LOẠI ĐẦU RA HÌNH ẢNH

### 2.1. Loại 1: Tập ảnh Dataset huấn luyện & đánh giá (`images/train/`, `images/val/`)

Đây là dữ liệu đầu vào cốt lõi được nạp vào mô hình Deep Learning trong quá trình huấn luyện:

* **Số lượng ảnh phân chia:**
  * **Train Set:** **880 ảnh** ($88.0\%$).
  * **Validation Set:** **120 ảnh** ($12.0\%$).
  * Tổng cộng: **1.000 ảnh** (Kiểm toán xác nhận $0\%$ trùng lặp, $0\%$ thiếu nhãn).
* **Đặc tính kỹ thuật của ảnh:**
  * **Bảo toàn nguyên bản (Lossless 100%):** Quá trình xử lý sử dụng lệnh sao chép nhị phân [`shutil.copy2`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/convert_kvasir_to_yolo_seg.py#L233). Không thực hiện tái nén JPEG, không làm biến dạng pixel và không làm suy giảm chất lượng hiển thị y khoa.
  * **Không can thiệp kích thước (No Resize / No Crop / No Pad):** Toàn bộ ảnh giữ nguyên độ phân giải gốc của máy nội soi (ví dụ: $622 \times 529$, $1348 \times 1070$, $720 \times 576$, $332 \times 487$,...). Việc co giãn về kích thước chuẩn như $640 \times 640$ được giao cho bộ xử lý Data Loader của YOLO xử lý động trong lúc nạp batch (`imgsz=640`).
* **Định dạng nhãn đi kèm (`labels/`):**
  * Tương ứng mỗi tệp `images/{split}/{id}.jpg` là tệp nhãn `labels/{split}/{id}.txt`.
  * Mỗi dòng trong tệp nhãn đại diện cho 1 khối polyp:
    $$\text{<class\_id>} \quad x_1 \quad y_1 \quad x_2 \quad y_2 \quad \dots \quad x_n \quad y_n$$
  * Trong đó `class_id = 0` (Polyp), tọa độ $(x_i, y_i)$ được chuẩn hóa trong khoảng $[0.0, 1.0]$.
  * Đa giác được rút gọn bằng thuật toán Ramer–Douglas–Peucker (`cv2.approxPolyDP` với $\epsilon = 0.002$), giúp **giảm 92.6% số điểm dư thừa** (từ trung bình 333.2 điểm xuống còn 24.6 điểm/polyp) nhưng bảo toàn hoàn toàn hình thái giải phẫu của khối u.

---

### 2.2. Loại 2: Ảnh trực quan hóa kiểm tra nhãn đối chứng (`preview/`)

Thư mục `preview/` chứa các ảnh được sinh ra tự động để bác sĩ hoặc kỹ sư AI nghiệm thu độ chính xác của nhãn đa giác:

* **Số lượng:** Mặc định sinh ra **20 ảnh mẫu** được chọn ngẫu nhiên có cố định seed (`random.seed(42)`).
* **Quy cách hình ảnh:** Ghép song song 3 khung hình theo chiều ngang (**Side-by-side Horizontal Stack**):
  $$\text{Kích thước ảnh preview} = (3 \times W) \times H$$
* **Chi tiết 3 khung hình thành phần:**
  1. **Khung trái (`1. Original Image`):** Ảnh nội soi màu gốc, góc trên gắn tiêu đề màu vàng.
  2. **Khung giữa (`2. Ground Truth Mask`):** Ảnh mặt nạ nhị phân gốc từ chuyên gia y tế (vùng polyp màu trắng trên nền đen).
  3. **Khung phải (`3. YOLO Seg Overlay`):** Ảnh gốc được tái hiện nhãn đa giác bằng cách **đọc trực tiếp từ tệp `.txt` vừa tạo**:
     * Vùng polyp được tô phủ màu xanh lá cây bán trong suốt (`fillPoly` với `alpha = 0.35`).
     * Viền ngoài đa giác được vẽ sắc nét màu xanh lá đậm (độ dày 2px).
     * Nhãn chữ `Polyp (YOLO)` được gắn ngay góc trên của polyp.
* **Mục đích:** Đảm bảo trực quan $100\%$ rằng nhãn YOLO sau khi số hóa và rút gọn điểm hoàn toàn khít với mặt nạ Ground Truth gốc.

---

### 2.3. Loại 3: Ảnh đồ thị thống kê phân bố Dataset (`dataset_plots/`)

Thư mục `dataset_plots/` chứa **5 ảnh đồ thị** được vẽ bằng `matplotlib`, xuất ra theo tiêu chuẩn bài báo khoa học / luận văn thạc sĩ - kỹ sư (định dạng `.png`, độ phân giải cao `DPI = 300`, giao diện lưới `seaborn-whitegrid`):

| Tên tệp ảnh | Nội dung & Ý nghĩa khoa học |
| :--- | :--- |
| `hist_polygon_points.png` | **Phân bố số điểm đa giác sau tối ưu:** Thể hiện số lượng điểm tọa độ đại diện cho mỗi khối polyp. Trung vị đạt 22 điểm, trung bình 24.6 điểm, cực đại 80 điểm. |
| `hist_contour_area.png` | **Phân bố diện tích đường viền polyp ($px^2$):** Thể hiện kích thước thực của tổn thương trên ảnh nội soi (nhỏ nhất: $508.5\ px^2$, lớn nhất: $1.099.180\ px^2$). |
| `hist_bbox_area.png` | **Phân bố diện tích Bounding Box ($px^2$):** Phân bố kích thước hộp chữ nhật bao bọc polyp (trung bình $74.790\ px^2$). |
| `hist_aspect_ratio.png` | **Phân bố tỷ lệ khung hình ($W / H$):** Khảo sát hình dạng polyp (tròn, dẹt hay thuôn dài). Có mốc đứt nét tham chiếu tại $AR = 1.0$ (hình vuông). |
| `hist_image_resolution.png` | **Top độ phân giải phổ biến:** Biểu đồ thanh ngang chỉ rõ các kích cỡ ảnh xuất hiện nhiều nhất trong tập dữ liệu Kvasir-SEG (giúp giải thích lý do cần multi-scale training). |

---

## 3. THÔNG SỐ TỔNG KẾT ĐẶC TẢ TỪ BÁO CÁO (REPORT)

Trích xuất trực tiếp từ kết quả chạy thực tế tại [`Kvasir_YOLO_SEG/report.txt`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Kvasir_YOLO_SEG/report.txt):

* **Tổng số ảnh:** 1.000 ảnh (880 Train / 120 Validation).
* **Tổng số mặt nạ polyp được gán nhãn:** 1.063 tổn thương (trung bình 1.06 polyp/ảnh).
* **Phân loại kích cỡ đối tượng theo chuẩn COCO:**
  * **Small ($Area < 1024\ px^2$):** $7$ polyp ($0.7\%$).
  * **Medium ($1024 \le Area \le 9216\ px^2$):** $114$ polyp ($10.7\%$).
  * **Large ($Area > 9216\ px^2$):** $942$ polyp ($88.6\%$).
* **Khả năng tương thích:** Tập dữ liệu đầu ra đã được kiểm toán tự động, sẵn sàng 100% để huấn luyện trên Kaggle/Colab/Server nội bộ:
  ```bash
  yolo segment train data=Kvasir_YOLO_SEG/dataset.yaml model=yolo11x-seg.pt epochs=100 imgsz=640 batch=16
  ```
