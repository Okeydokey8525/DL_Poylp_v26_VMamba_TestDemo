# YÊU CẦU ĐẶC TẢ CHI TIẾT: THU THẬP, CHUẨN HÓA VÀ ĐÓNG GÓI DỮ LIỆU NỘI SOI BỔ SUNG
## Đề tài: Phân đoạn Polyp Đại Trực Tràng Hỗ trợ Can thiệp Nội soi (CADe/CADx)
**Hệ thống mục tiêu:** YOLO26s-seg kết hợp C2TSVMamba (Visual State Space Model)  
**Tổ chức thực hiện:** Nhóm nghiên cứu Khóa luận Cử nhân CNTT (CNTT_KLCN182)

---

### I. MỤC TIÊU VÀ BỐI CẢNH DỰ ÁN

Hiện tại, nhóm nghiên cứu đã hoàn tất huấn luyện và kiểm định mô hình nhận diện và phân đoạn polyp đại trực tràng trên bộ dữ liệu cơ sở **Kvasir-SEG** (1,000 ảnh) qua 6 seed độc lập (với tỷ lệ chia 880 ảnh train / 120 ảnh val, tập val cố định 127 polyp). Mô hình đề xuất **C2TSVMamba** đã chứng minh được:
1. **Độ ổn định vượt trội:** Giảm độ lệch chuẩn của Mask mAP@50-95 xuống 3 lần (±0.0050 so với ±0.0150 của Baseline).
2. **Chất lượng đường biên mặt nạ:** Giảm hàm mất mát phân đoạn kiểm định (`val/seg_loss`) xuống 1.3812 (p = 0.0363 < 0.05), triệt tiêu hiện tượng răng cưa và ngăn chặn việc phân đoạn lem ra niêm mạc lành.

**Tuy nhiên, để hoàn thiện luận văn và đáp ứng các tiêu chuẩn đánh giá khắt khe của hội đồng bảo vệ, nhóm cần mở rộng tập dữ liệu nhằm giải quyết 3 bài toán trọng tâm:**
- **Bài toán 1 (Kiểm thử độc lập - Cross-dataset Generalization):** Đánh giá tính tổng quát hóa của mô hình trên các nguồn bệnh nhân và thiết bị nội soi độc lập ngoài Kvasir-SEG (đặc biệt là bệnh nhân Việt Nam).
- **Bài toán 2 (Kiểm soát báo động giả - False Positive / Specificity):** Bổ sung ảnh âm tính (ảnh nội soi bình thường hoàn toàn không có polyp) để định lượng tỷ lệ phát hiện nhầm trên niêm mạc lành, bọt khí, dịch phân.
- **Bài toán 3 (Thách thức tổn thương phẳng & ca khó - Hard Cases):** Bổ sung các ca polyp nhỏ (< 5mm), dạng phẳng (Paris classification IIa/IIb), hoặc ảnh có đốm sáng lóa (glare) để tối ưu hóa độ nhạy phát hiện.

---

### II. CÁC NHÓM DỮ LIỆU CẦN THU THẬP & BỔ SUNG

#### 1. Nhóm Dữ liệu 1: Bộ dữ liệu Kiểm thử Độc lập Đa trung tâm (Cross-dataset Benchmark)
*Ưu tiên đóng gói thành các tập Test Set độc lập (không dùng để train lại, dùng để đánh giá độ tổng quát hóa Zero-shot / Transfer performance):*

1. **Bộ dữ liệu BKAI-IGH NeoPolyp (Ưu tiên số 1):**
   - **Nguồn gốc:** Viện Nghiên cứu Dữ liệu lớn (VinBigdata) hợp tác cùng Bệnh viện Đại học Y Hà Nội (IGH).
   - **Ý nghĩa:** Đây là dữ liệu thực tế trên bệnh nhân Việt Nam, sử dụng các dòng máy nội soi phổ biến tại Việt Nam (Olympus, Fujifilm).
   - **Số lượng:** Tối thiểu **600 – 1,000 ảnh** có ground-truth mặt nạ phân đoạn.
2. **Bộ dữ liệu CVC-ClinicDB / CVC-ColonDB (Ưu tiên số 2):**
   - **Nguồn gốc:** Bệnh viện Hospital Clínic de Barcelona (Tây Ban Nha).
   - **Số lượng:** **612 ảnh** (CVC-ClinicDB) hoặc **380 ảnh** (CVC-ColonDB).
   - **Đặc điểm:** Độ phân giải chuẩn 384 x 288 trích xuất từ video nội soi rút dây quang.

#### 2. Nhóm Dữ liệu 2: Khung hình Nội soi Âm tính (Negative / Non-polyp Background Frames)
*Hiện tại tập Kvasir-SEG 100% đều là ảnh chứa polyp. Điều này khiến mô hình chưa được kiểm định khả năng "từ chối" dự đoán khi gặp niêm mạc bình thường.*

- **Số lượng yêu cầu:** **200 – 300 ảnh âm tính hoàn toàn**.
- **Tiêu chí nội dung ảnh âm:**
  * Khung hình niêm mạc đại trực tràng hoàn toàn khỏe mạnh, không có polyp.
  * Khung hình chứa các yếu tố gây nhiễu thường gặp trong phòng nội soi:
    - Bọt khí (air bubbles) và bọt nhầy do dịch tiêu hóa.
    - Cặn thức ăn, dịch phân còn sót sau khi chuẩn bị ruột (stool residue/debris).
    - Nếp gấp niêm mạc ruột gập khúc tạo bóng tối cục bộ (haustral folds / shadows).
    - Mạch máu dưới niêm mạc nổi rõ (submucosal vascular pattern).
- **Quy tắc gán nhãn bắt buộc:** File .txt tương ứng của ảnh âm tính phải là **tệp rỗng (dung lượng 0 byte)** theo đúng chuẩn của Ultralytics YOLO.

#### 3. Nhóm Dữ liệu 3: Tập Ca khó Lâm sàng (Clinical Hard Cases & Edge Cases)
*Nhóm cần tối thiểu **100 – 150 ảnh** thuộc các nhóm bệnh học đặc thù để làm thực nghiệm phân tích chuyên sâu (Subgroup Analysis):*

- **Ca khó 1 (Polyp phẳng / Teo bờ - Paris IIb/IIa):** Polyp dạng phẳng hoặc hơi lõm, không có cuống, kích thước nhỏ dưới 5mm, màu sắc tương đồng trên 90% với niêm mạc xung quanh.
- **Ca khó 2 (Chói sáng / Phản xạ gương - Specular Reflection / Glare):** Vùng polyp bị phủ bởi đốm sáng trắng cường độ cao phát ra từ đèn nội soi xenon/LED.
- **Ca khó 3 (Nhòe chuyển động - Motion Blur):** Khung hình trích xuất khi đầu dây soi đang di chuyển nhanh hoặc nhu động ruột co thắt mạnh.
- **Ca khó 4 (Polyp khuất bờ):** Polyp nằm sau bờ nếp gấp đại tràng, chỉ nhìn thấy một góc 30-50% diện tích tổn thương.

---

### III. QUY CHUẨN ĐỊNH DẠNG DỮ LIỆU & CẤU TRÚC BÀN GIAO (TECHNICAL SPECIFICATION)

#### 1. Quy cách Hình ảnh (Images)
- **Định dạng file:** `.jpg` hoặc `.png` (RGB, 3 kênh màu, 8-bit per channel).
- **Độ phân giải:** Giữ nguyên tỷ lệ khung hình gốc của máy nội soi, tối thiểu 512 x 512 pixel (hệ thống sẽ tự động resize và pad letterbox về 640 x 640 khi nạp vào model).
- **Quy tắc đặt tên:** Tên file viết liền không dấu, không khoảng trắng, ví dụ: `bkai_polyp_0012.jpg`, `neg_normal_0045.jpg`, `clinic_hard_0078.jpg`.

#### 2. Quy chuẩn Định dạng Nhãn Phân đoạn (YOLO-Seg Polygon Format)
Toàn bộ nhãn phân đoạn phải được chuyển đổi về định dạng chuẩn của Ultralytics YOLO Segmentation:
- Mỗi ảnh có đúng một tệp `.txt` cùng tên nằm trong thư mục `labels/`.
- Mỗi dòng đại diện cho một tổn thương polyp, bắt đầu bằng `class_id` là `0`:
  ```
  0 x1 y1 x2 y2 x3 y3 ... xn yn
  ```
- **Tọa độ chuẩn hóa:** Toàn bộ tọa độ x_i, y_i phải được chuẩn hóa về dải [0.0, 1.0]:
  x_i = pixel_x / image_width, y_i = pixel_y / image_height
- **Độ mịn của đa giác (Polygon Vertex Density):**
  * Số đỉnh đa giác (n) tối thiểu >= 8 điểm và tối đa <= 80 điểm.
  * Tuyệt đối không dùng bounding box 4 góc để làm mask.
  * Đường biên đa giác phải ôm sát bờ tổn thương thực tế, không lấn ra ngoài mô lành và không bị cắt cụt chân polyp.
- **Đối với ảnh âm tính (Background frame):** Tạo file .txt rỗng (0 byte).

#### 3. Cấu trúc Thư mục Đóng gói Bàn giao (Directory Structure)
Mỗi bộ dữ liệu (ví dụ `BKAI_NeoPolyp_YOLO_SEG`) phải được tổ chức độc lập theo đúng cấu trúc sau:

```
BKAI_NeoPolyp_YOLO_SEG/
├── data.yaml                     # File cấu hình nạp dữ liệu chuẩn
├── metadata.csv                  # Bảng tra cứu nguồn gốc ảnh (nếu có)
├── images/
│   ├── train/                    # 80% nếu dùng cho fine-tune
│   ├── val/                      # 10% kiểm định
│   └── test/                     # 10% kiểm thử độc lập
└── labels/
    ├── train/                    # File .txt polygon tương ứng
    ├── val/
    └── test/
```

Nội dung tệp **`data.yaml`** đi kèm:
```yaml
path: ./BKAI_NeoPolyp_YOLO_SEG
train: images/train
val: images/val
test: images/test

nc: 1
names:
  0: polyp
```

---

### IV. QUY TRÌNH KIỂM ĐỊNH CHẤT LƯỢNG DỮ LIỆU TRƯỚC KHI BÀN GIAO (QUALITY ASSURANCE)

Bên thực hiện dữ liệu bắt buộc chạy script Python tự động kiểm tra tính hợp lệ trước khi nén gửi:

```python
import os, glob
from PIL import Image

def audit_dataset(dataset_dir):
    print(f"=== KIỂM ĐỊNH DỮ LIỆU: {dataset_dir} ===")
    for split in ['train', 'val', 'test']:
        img_dir = os.path.join(dataset_dir, 'images', split)
        lbl_dir = os.path.join(dataset_dir, 'labels', split)
        if not os.path.exists(img_dir): continue
        
        imgs = set(os.path.splitext(f)[0] for f in os.listdir(img_dir))
        lbls = set(os.path.splitext(f)[0] for f in os.listdir(lbl_dir))
        
        diff = imgs.symmetric_difference(lbls)
        assert len(diff) == 0, f"Lỗi lệch file giữa images và labels tại {split}: {diff}"
        
        for lbl_file in glob.glob(os.path.join(lbl_dir, '*.txt')):
            with open(lbl_file, 'r') as f:
                lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if not parts: continue
                assert parts[0] == '0', f"Class ID phải là 0: {lbl_file}"
                coords = [float(x) for x in parts[1:]]
                assert len(coords) >= 8 and len(coords) % 2 == 0, f"Đa giác < 4 đỉnh: {lbl_file}"
                for c in coords:
                    assert 0.0 <= c <= 1.0, f"Tọa độ ngoài dải [0, 1]: {c} in {lbl_file}"
        print(f"Split {split}: {len(imgs)} ảnh hợp lệ 100%!")
```

---

### V. BÁO CÁO THỐNG KÊ (DELIVERABLES CHECKLIST) KÈM THEO

Khi bàn giao, đề nghị bên thực hiện cung cấp kèm **Bảng Thống kê Tóm tắt** theo mẫu sau:

| Hạng mục dữ liệu | Tên bộ dữ liệu | Số lượng ảnh | Số polyp xác nhận | Số ảnh âm (background) | Kích thước file nén |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Kiểm thử độc lập** | BKAI-IGH NeoPolyp | ... ảnh | ... polyp | ... ảnh | ... MB |
| **Kiểm thử độc lập** | CVC-ClinicDB | 612 ảnh | ... polyp | 0 ảnh | ... MB |
| **Khung hình âm tính** | Normal_Colon_Frames | ... ảnh | 0 polyp | ... ảnh âm | ... MB |
| **Ca khó (Hard cases)** | Flat_and_Small_Polyps | ... ảnh | ... polyp | 0 ảnh | ... MB |

---
**Liên hệ kỹ thuật & Hỗ trợ tích hợp:**  
Nhóm nghiên cứu Đề tài CNTT_KLCN182 — ĐH Công Thương TP.HCM (HUIT).
