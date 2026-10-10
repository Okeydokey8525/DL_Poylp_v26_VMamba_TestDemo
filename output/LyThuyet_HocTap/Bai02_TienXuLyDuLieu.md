# BÀI 2 — Tiền xử lý dữ liệu cho YOLO26-seg (bộ Kvasir BG20)

> **Dành cho:** sinh viên mới tiếp cận, chưa từng chuẩn bị dữ liệu cho một mô hình phân đoạn.
> **Mục tiêu:** đọc xong bạn giải thích được dữ liệu đi từ "ảnh nội soi + mặt nạ trắng đen" tới "batch tensor đưa vào YOLO26-seg + TSVM" qua những bước nào, mỗi bước để làm gì, tham số bao nhiêu.
> **Cách đọc:** đọc Phần 0 (Pareto) trước, sau đó theo đúng thứ tự dòng chảy dữ liệu.

Ký hiệu độ chắc chắn:

| Nhãn | Nghĩa |
|---|---|
| ✅ **Đã xác nhận** | Đọc trực tiếp từ code, config, hoặc kiểm tra file dữ liệu trong repo. |
| 📘 **Kiến thức chung** | Lý thuyết phổ biến. |
| ⚠️ **Chưa xác minh** | Chưa có đủ bằng chứng trong repo. |

---

## Phần 0 — Pareto: 5 ý gánh 80% chương tiền xử lý

| # | Ý cốt lõi | Vì sao quan trọng |
|---|---|---|
| 1 | **Có 2 giai đoạn tách biệt:** (A) *chuẩn bị bộ dữ liệu một lần* trước khi train (mask → polygon, thêm ảnh nền, chia tập); (B) *biến đổi mỗi lần nạp ảnh* trong lúc train (resize, augmentation, chia 255). | Nhầm hai giai đoạn là lỗi phổ biến nhất khi viết chương này. |
| 2 | **Mask được chuyển thành polygon** (Otsu → Closing → contour → lọc → đơn giản hóa → chuẩn hóa tọa độ) vì YOLO-seg đọc nhãn dạng polygon. Các phép này làm **trên mask**, không làm trên ảnh nội soi. | Đây là bước "của riêng đề tài", nối dữ liệu Kvasir với YOLO. |
| 3 | **BG20 = thêm 200 ảnh nền có nhãn rỗng** (= 20% của 1.000 ảnh polyp) để mô hình học "không phải chỗ nào đỏ cũng là polyp". | Giải thích chữ "BG20" và các chỉ số báo nhầm (FP). |
| 4 | **Chia tập: polyp 880/120, nền 160/40 → train 1.040, val 160.** | Mọi con số đánh giá đều tính trên 160 ảnh val (127 polyp). |
| 5 | **Lúc train:** LetterBox về 640, Mosaic + lật ngang + dịch/scale + HSV, đóng Mosaic 10 epoch cuối, pixel chia 255. **Lúc val:** không augmentation. | Đây là phần "tăng cường dữ liệu" mà hội đồng hay hỏi. |

> 💡 **Một câu tóm tắt:** *Mask → polygon + ảnh nền nhãn rỗng → chia 1.040/160 → mỗi lần nạp: resize/LetterBox, augmentation (chỉ train), RGB-CHW, chia 255 → vào mô hình.*

```text
╔══════════ GIAI ĐOẠN A: CHUẨN BỊ BỘ DỮ LIỆU (chạy 1 lần) ══════════╗
║ Ảnh polyp Kvasir-SEG ───── sao chép nguyên ───────────────┐       ║
║ Mask Kvasir-SEG ── xám → Otsu → Closing 3×3 → contour     │       ║
║                 → bỏ vùng < 20 px² → approxPolyDP         ├─→ BG20║
║                 → chuẩn hóa [0,1] → file .txt             │       ║
║ Ảnh normal-cecum ── chọn 200 (seed 42) → 160 / 40         │       ║
║                 → sao chép + file .txt RỖNG ──────────────┘       ║
╚═══════════════════════════════════════════════════════════════════╝
╔══════════ GIAI ĐOẠN B: NẠP DỮ LIỆU (mỗi lần lấy ảnh) ═════════════╗
║ TRAIN: đọc ảnh → resize → Mosaic/dịch/scale/lật/HSV               ║
║        → RGB, CHW, polygon → mask 160×160 → batch → /255 → MODEL  ║
║ VAL:   đọc ảnh → resize → LetterBox → RGB, CHW → /255 → ĐÁNH GIÁ  ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## Phần 1 — Vì sao phải tiền xử lý?

📘 Mô hình học sâu chỉ "hiểu" **tensor số** có kích thước cố định, theo đúng định dạng nhãn mà thư viện quy định. Dữ liệu gốc thì:

- Ảnh có **kích thước khác nhau** (Kvasir-SEG có ảnh từ khoảng 332×487 đến 1920×1072 — 📘 theo mô tả bộ dữ liệu công bố).
- Nhãn gốc là **ảnh mặt nạ** trắng đen, còn YOLO-seg cần **file văn bản chứa tọa độ polygon**.
- Chỉ có ảnh **có** polyp → mô hình chưa từng thấy ảnh "không có gì", dễ báo nhầm.
- Chỉ ~1.000 ảnh → ít, dễ học thuộc (overfit) → cần **tăng cường dữ liệu**.

Mỗi bước tiền xử lý trong bài này giải quyết một trong 4 vấn đề trên. Khi viết khóa luận, hãy luôn trình bày theo mẫu: **vấn đề → mục đích → cách làm + tham số → kết quả**.

---

## Phần 2 — Nguồn dữ liệu

| Nguồn | Nội dung | Vai trò |
|---|---|---|
| **Kvasir-SEG** | 1.000 ảnh nội soi có polyp + 1.000 mask nhị phân (trắng = polyp, đen = nền) | Dữ liệu chính |
| **normal-cecum** (thuộc bộ Kvasir) | Ảnh manh tràng bình thường, **không có polyp** | Ảnh nền (background / negative) |

> 💡 Ảnh nền **không phải lớp thứ hai**. Trong YAML chỉ có một lớp `0: polyp` ✅. Ảnh nền đơn giản là ảnh không có đối tượng nào.

⚠️ Ảnh và mask gốc **hiện không có** tại các đường dẫn mà script yêu cầu trong workspace này. Repo chỉ còn bộ BG20 đã chuyển đổi. Vì vậy hình minh họa "mask gốc" cần tìm lại dữ liệu nguồn, **không** lấy mask vẽ lại từ polygon rồi gọi là mask gốc.

---

## Phần 3 — Chuyển mask thành nhãn polygon (bước quan trọng nhất)

Script: `archive/Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py`, hàm `convert_mask_to_yolo_polygons()` ✅.

### 3.1. Vì sao cần polygon?

📘 Định dạng nhãn YOLO-seg: mỗi đối tượng là **một dòng**:

```text
<lớp> x1 y1 x2 y2 x3 y3 ... xn yn
```

Tọa độ đã **chuẩn hóa về [0, 1]** (chia cho chiều rộng/cao ảnh). Ví dụ thật trong repo ✅ (`labels/val/cju0s690hkp960855tjuaqvv0.txt`):

```text
0 0.465378 0.539623 0.450886 0.550943 0.434783 0.554717 0.428341 0.575472 ...
```

→ Lớp 0 (polyp), theo sau là các cặp (x, y) đi vòng quanh viền polyp.

So sánh: mask là ảnh lưu **mọi pixel**; polygon chỉ lưu **các đỉnh của đường viền** → gọn hơn rất nhiều, và YOLO tự vẽ (raster hóa) lại thành mask khi train.

### 3.2. Sáu bước, mỗi bước một câu hỏi

| Bước | Thao tác | Câu hỏi nó trả lời | Tham số ✅ |
|---|---|---|---|
| 1 | Đọc mask, chuyển **ảnh xám** | "Bỏ kênh màu thừa" | `COLOR_BGR2GRAY` |
| 2 | **Ngưỡng Otsu** → ảnh nhị phân 0/255 | "Pixel nào là polyp?" — mask JPEG có viền mờ/giá trị lưng chừng, cần phân định rõ | `THRESH_BINARY + THRESH_OTSU` |
| 3 | **Closing** (giãn rồi co) | "Lấp các lỗ, khe nhỏ trong vùng polyp" | kernel chữ nhật 3×3, 1 lần |
| 4 | **Tìm đường bao ngoài** (contour) | "Viền của từng vùng polyp ở đâu?" | `RETR_EXTERNAL`, `CHAIN_APPROX_SIMPLE` |
| 5 | **Lọc vùng nhỏ** | "Bỏ chấm nhiễu không phải polyp" | diện tích < 20 pixel² thì bỏ |
| 6 | **Đơn giản hóa** bằng `approxPolyDP` | "Giảm số đỉnh mà vẫn giữ hình dạng" | `epsilon = 0.002 × chu vi` |
| 7 | **Chuẩn hóa** tọa độ, ghi file | "Đưa về [0, 1] để không phụ thuộc kích thước ảnh" | `x/W`, `y/H`, kẹp trong [0, 1] |

### 3.3. Giải thích từng kỹ thuật cho người mới

**Otsu (📘):** tự động chọn ngưỡng sao cho hai nhóm pixel (sáng/tối) **tách nhau rõ nhất** — cụ thể là làm cực đại phương sai *giữa* hai nhóm. Không cần chọn ngưỡng bằng tay như "lớn hơn 127 là trắng". Với mask gần như chỉ có hai mức, Otsu cho ngưỡng ổn định.

**Closing (📘):** hình dung vùng trắng là một vũng nước:
- *Giãn (dilation)*: nước lan ra 1 pixel mỗi phía → các khe nhỏ bị lấp.
- *Co (erosion)*: nước rút lại 1 pixel → vùng trở về kích thước gần như cũ, nhưng khe đã lấp thì vẫn lấp.

**Contour ngoài (RETR_EXTERNAL):** chỉ lấy viền **bao ngoài**. Hệ quả cần biết: nếu mask có "lỗ" bên trong, lỗ đó **không được lưu** riêng trong nhãn.

**approxPolyDP (thuật toán Douglas–Peucker 📘):** bỏ những đỉnh nằm gần như thẳng hàng. Sai số cho phép `epsilon` = 0,2% chu vi. Ví dụ viền dài 1.000 pixel → cho phép lệch tối đa 2 pixel. Đủ nhỏ để giữ hình polyp, đủ lớn để bỏ đỉnh thừa. Nếu sau khi đơn giản còn dưới 3 đỉnh (không thành đa giác), script **quay về dùng contour gốc** ✅.

**Chuẩn hóa tọa độ:** `x_norm = x / W`, `y_norm = y / H`. Ví dụ ảnh rộng 622 pixel, điểm x = 289 → x_norm ≈ 0.465. Nhờ vậy khi ảnh bị resize, nhãn vẫn đúng.

> ⚠️ **Lỗi viết hay gặp:** "Ảnh nội soi được xử lý bằng Otsu và Closing." → **Sai.** Otsu/Closing chỉ áp dụng lên **mask**. Ảnh nội soi được **sao chép nguyên vẹn** ✅.

> ⚠️ Không viết "polygon bảo toàn tuyệt đối mask gốc" — Closing, lọc vùng nhỏ, bỏ lỗ trong và đơn giản hóa đều có thể làm khác đi một chút. Chưa có đo định lượng trong repo.

---

## Phần 4 — Xây bộ BG20 và chia tập

### 4.1. Thêm ảnh nền (BG = background)

| Việc | Chi tiết ✅ |
|---|---|
| Số ảnh nền | **200** = 20% của 1.000 ảnh polyp → tên "BG20" |
| Cách chọn | Sắp xếp danh sách file, rồi chọn ngẫu nhiên với **seed 42** (để lần sau chọn y hệt) |
| Chia | 160 vào train, 40 vào val |
| Nhãn | File `.txt` **rỗng (0 byte)**, tên ảnh có tiền tố `bg_` |

📘 **Vì sao ảnh nền giúp ích?** Niêm mạc ruột có nếp gấp, mạch máu, vùng phản quang… dễ bị nhầm thành polyp. Nếu mô hình chỉ từng thấy ảnh có polyp, nó dễ "đoán bừa" có polyp ở đâu đó. Ảnh nền nhãn rỗng dạy mô hình rằng: *"ảnh này không có gì để báo cả"* → giảm báo nhầm (FP).

> ⚠️ Cách nói đúng: "200 ảnh nền bằng **20% số ảnh polyp**". Trong tổng 1.200 ảnh, nền chiếm **16,67%**, **không phải** 20%.

> ⚠️ Seed 42 là seed **chọn ảnh nền**, khác với seed 0–9 dùng để **train**. Đừng gộp làm một.

### 4.2. Bảng số lượng (đã kiểm tra trực tiếp ✅)

| | Train | Val | Tổng |
|---|---:|---:|---:|
| Ảnh polyp | 880 | 120 | 1.000 |
| Ảnh nền | 160 | 40 | 200 |
| **Tổng ảnh** | **1.040** | **160** | **1.200** |
| File nhãn rỗng | 160 | 40 | 200 |
| Số polygon (đối tượng) | 936 | **127** | 1.063 |

Chú ý: **số polygon > số ảnh polyp** vì một ảnh có thể có nhiều polyp (hoặc một polyp bị tách thành nhiều vùng). Đây là lý do tập val có **120 ảnh polyp nhưng 127 đối tượng** — con số 127 bạn sẽ gặp lại khi tính Recall (Bài 1, Phần 7).

Danh sách polyp 880/120 lấy theo file `archive/train.txt` và `archive/val.txt` có sẵn ✅. Đề tài **không có tập test độc lập** — chỉ có train và val. Khi viết, không được nói "đánh giá trên tập test".

### 4.3. Cấu trúc thư mục YOLO ✅

```text
Kvasir_YOLO_SEG_BG20/
├── images/
│   ├── train/   (1.040 ảnh .jpg)
│   └── val/     (160 ảnh)
├── labels/
│   ├── train/   (1.040 file .txt — cùng tên với ảnh)
│   └── val/     (160 file .txt)
└── data_bg20.yaml   (đường dẫn + nc: 1 + names: polyp)
```

📘 Quy tắc vàng: ảnh `abc.jpg` ↔ nhãn `abc.txt`, cùng tên, nằm ở thư mục `labels` song song với `images`.

### 4.4. Kiểm tra toàn vẹn dữ liệu ✅ (kiểm tra bổ sung ngày 07/10/2026)

Kết quả trong `output/kiem_tra_du_lieu_bg20.json`:
- Không thiếu nhãn, không có nhãn "mồ côi" (không kèm ảnh).
- Mọi dòng polygon: lớp 0, ít nhất 3 cặp tọa độ, giá trị trong [0, 1].
- **Không trùng tên** và **không trùng nội dung file** (SHA-256) giữa train và val → không bị rò rỉ dữ liệu ở mức file.

⚠️ Giới hạn: chưa kiểm tra **ảnh gần trùng** (cùng polyp, khung hình kề nhau) hay **cùng bệnh nhân** giữa train và val — Kvasir-SEG không cung cấp mã bệnh nhân. Khi viết, nêu rõ giới hạn này.

---

## Phần 5 — Nạp ảnh vào mô hình (mỗi lần lấy ảnh)

Phần này do thư viện Ultralytics (fork của đề tài) tự làm; đề tài **cấu hình** chứ không tự viết code. Tham số lấy từ `args.yaml` của lần train ✅.

### 5.1. Resize và LetterBox

Mô hình cần ảnh kích thước `imgsz = 640`.

- **Resize giữ tỉ lệ:** cạnh dài thu về 640, cạnh ngắn co theo tỉ lệ → không méo polyp.
- **LetterBox:** phần còn trống được **đệm (padding)** bằng màu xám để thành khung đủ kích thước. Giống xem phim màn ảnh rộng trên TV có hai dải đen.

```text
Ảnh gốc 1280×1024  →  resize 640×512  →  đệm thêm 64 px trên + 64 px dưới  →  640×640
```

Tọa độ polygon được biến đổi **cùng lúc** với ảnh để vẫn khớp.

⚠️ Chi tiết chính xác: ở validation, Ultralytics có thể dùng **batch chữ nhật** (`rect` theo chế độ val), nên ảnh val không nhất thiết vuông 640×640. Cách viết an toàn: "kích thước cấu hình `imgsz = 640`".

### 5.2. Định dạng tensor

| Bước | Từ → Sang | Lý do |
|---|---|---|
| Đổi kênh màu | BGR → RGB | OpenCV đọc ảnh theo BGR; mô hình pretrained học trên RGB (`bgr = 0.0`) |
| Đổi trục | HWC → CHW | PyTorch quy ước (Kênh, Cao, Rộng) |
| Gộp batch | CHW → BCHW | `batch = 8` ảnh mỗi bước |
| **Chuẩn hóa pixel** | `0..255` → `0..1` bằng **chia 255** | Giá trị nhỏ giúp huấn luyện ổn định |

> ⚠️ Đề tài **không** chuẩn hóa theo mean/std ImageNet — chỉ chia 255 ✅.
> 📘 Phân biệt: *chuẩn hóa tọa độ nhãn* (Phần 3, chia W/H) và *chuẩn hóa pixel ảnh* (chia 255) là **hai việc khác nhau**.

### 5.3. Từ polygon trở lại mask huấn luyện

Khi train, YOLO **vẽ lại** polygon thành mask:
- `mask_ratio = 4` → mask nhỏ hơn ảnh 4 lần: ảnh 640×640 → mask **160×160** ✅. Khớp đúng kích thước 32 prototype của Proto26 (Bài 1, Phần 3).
- `overlap_mask = true` → các polyp trong cùng ảnh được gộp vào **một** mask, mỗi polyp mang một chỉ số riêng (1, 2, 3…), thay vì lưu nhiều mask rời.

---

## Phần 6 — Tăng cường dữ liệu (Data Augmentation)

### 6.1. Ý tưởng

📘 Với ~1.000 ảnh, mô hình dễ "học thuộc". Augmentation tạo ra **biến thể mới mỗi epoch** của cùng một ảnh (lật, dịch, đổi màu…) để mô hình học **đặc điểm thật của polyp** chứ không phải học thuộc từng ảnh. Chỉ áp dụng cho **train** ✅; val giữ nguyên để đánh giá công bằng.

Nguyên tắc: phép biến đổi **hình học** phải đổi **cả ảnh lẫn nhãn**; phép biến đổi **màu** chỉ đổi ảnh, nhãn giữ nguyên.

### 6.2. Các phép đang BẬT ✅ (`args.yaml`)

| Phép | Tham số | Hiểu nôm na | Loại |
|---|---|---|---|
| **Mosaic** | `mosaic = 1.0` | Ghép 4 ảnh train thành 1 ảnh → mỗi ảnh huấn luyện có nhiều ngữ cảnh, polyp xuất hiện ở nhiều vị trí/kích thước | Hình học |
| **Đóng Mosaic** | `close_mosaic = 10` | Tắt Mosaic ở **10 epoch cuối** (91–100) để mô hình quen với ảnh "thật" giống lúc đánh giá | Lịch trình |
| Dịch chuyển | `translate = 0.1` | Dịch ảnh ngẫu nhiên tối đa ~10% | Hình học |
| Thay đổi tỉ lệ | `scale = 0.5` | Phóng/thu ngẫu nhiên trong khoảng ±50% (không phải "luôn thu còn 50%") | Hình học |
| Lật ngang | `fliplr = 0.5` | 50% khả năng lật trái–phải | Hình học |
| HSV | `hsv_h = 0.015`, `hsv_s = 0.7`, `hsv_v = 0.4` | Biên độ thay đổi sắc độ / độ bão hòa / độ sáng (là **biên độ**, không phải xác suất) — mô phỏng khác biệt đèn, máy nội soi | Màu |
| *(Random erasing)* | `erasing = 0.4` | Có trong `args.yaml` nhưng **không áp dụng cho seg**: trong code chỉ hàm `classify_augmentations()` (tác vụ phân loại) dùng tham số này ✅. Không đưa vào chương tiền xử lý. | — |

### 6.3. Các phép đang TẮT ✅ (giá trị 0)

`degrees` (xoay), `shear` (xô lệch), `perspective` (phối cảnh), `flipud` (lật dọc), `mixup`, `cutmix`, `copy_paste`, `multi_scale`.

> ⚠️ Khi vẽ hình minh họa augmentation, **chỉ vẽ các phép đang bật**. Đừng thêm "xoay ảnh" hay "lật dọc" vì thấy trong tài liệu khác.

📘 Albumentations (Blur, MedianBlur, ToGray, CLAHE, mỗi phép p = 0.01) là nhánh **có điều kiện** — chỉ chạy nếu môi trường cài thư viện này. ⚠️ Chưa có log xác nhận lần train lịch sử đã dùng, nên chỉ nhắc như "mặc định có điều kiện".

---

## Phần 7 — Liên hệ với đề tài: tiền xử lý ảnh hưởng tới kết quả ra sao?

| Bước tiền xử lý | Ảnh hưởng tới mô hình / chỉ số |
|---|---|
| Mask → polygon (Closing, đơn giản hóa, bỏ lỗ) | Định nghĩa "viền thật" mà Mask mAP@50-95 so sánh. Viền nhãn càng sai lệch thì mAP ở IoU cao (0.9, 0.95) càng khó đạt. |
| Ảnh nền nhãn rỗng | Tác động trực tiếp tới **FP** trên 40 ảnh nền val và tới **Precision**. |
| Chia 880/120 cố định | Cả Baseline và TSVM dùng **cùng** split → so sánh công bằng; khác biệt chỉ do kiến trúc + seed. |
| `mask_ratio = 4` → mask 160×160 | Giới hạn độ mịn viền; khớp độ phân giải prototype. |
| Augmentation giống hệt cho cả hai mô hình | Đảm bảo nguyên tắc "thay một biến" — chỉ khác layer 10 ✅. So hai file `args.yaml` seed 0: chỉ khác dòng `model`, `name`, `pretrained`, `save_dir`; mọi tham số dữ liệu và augmentation trùng nhau. |
| Chia 255, không mean/std | Đúng quy ước của trọng số pretrained `yolo26s-seg.pt`. |

> 💡 **TSVM không có bước tiền xử lý riêng.** TSVM là một khối bên trong mô hình (layer 10), xử lý **đặc trưng**, không xử lý ảnh hay nhãn. Toàn bộ pipeline dữ liệu của Baseline và TSVM là một.

---

## Phần 8 — Hiểu lầm thường gặp

| Hiểu lầm | Đúng là |
|---|---|
| "Ảnh nội soi được Otsu/Closing/CLAHE trước khi train" | Otsu/Closing chỉ làm trên **mask**; ảnh được sao chép nguyên. |
| "Ảnh nền là lớp thứ 2" | Chỉ có 1 lớp `polyp`; ảnh nền là ảnh **không có đối tượng**, nhãn rỗng. |
| "BG20 = 20% bộ dữ liệu là ảnh nền" | 20% so với **số ảnh polyp**; trong tổng là 16,67%. |
| "Chia train/val 80/20" | Polyp 880/120 (88/12); tổng 1.040/160. |
| "Có tập test" | Chỉ có train + val. |
| "Seed 42 là seed huấn luyện" | 42 là seed chọn ảnh nền; train dùng seed 0–9. |
| "scale = 0.5 nghĩa là ảnh thu còn một nửa" | Là **biên độ** phóng/thu ngẫu nhiên. |
| "hsv_s = 0.7 là 70% xác suất" | Là biên độ thay đổi độ bão hòa. |
| "Ảnh val luôn 640×640" | Val có thể dùng batch chữ nhật; chỉ nói `imgsz = 640`. |

---

## Phần 9 — Tự kiểm tra (có đáp án)

1. **Kể 2 giai đoạn của tiền xử lý.**
   → (A) chuẩn bị bộ dữ liệu một lần: mask → polygon, thêm ảnh nền, chia tập; (B) biến đổi khi nạp: resize/LetterBox, augmentation, RGB/CHW, chia 255.
2. **Vì sao dùng Otsu thay vì ngưỡng cố định 127?**
   → Otsu tự chọn ngưỡng tách hai nhóm pixel tốt nhất, chịu được mask có viền mờ do nén ảnh.
3. **`epsilon = 0.002 × chu vi`, viền dài 800 px thì sai số cho phép là bao nhiêu?**
   → 1,6 pixel.
4. **Tập val có bao nhiêu ảnh, bao nhiêu polyp, bao nhiêu ảnh nền?**
   → 160 ảnh; 127 polyp trong 120 ảnh polyp; 40 ảnh nền.
5. **Ảnh 1000×800, imgsz 640. Sau resize giữ tỉ lệ là bao nhiêu? Đệm bao nhiêu để vuông?**
   → 640×512; đệm thêm 128 px chiều cao (64 trên + 64 dưới).
6. **Vì sao tắt Mosaic 10 epoch cuối?**
   → Ảnh Mosaic khác ảnh thật; giai đoạn cuối cho mô hình thích nghi với phân bố ảnh giống lúc đánh giá.
7. **Lật ngang có phải sửa nhãn không? Đổi HSV thì sao?**
   → Lật ngang: có (x → 1 − x). HSV: không, chỉ đổi màu.
8. **TSVM có cần chuẩn bị dữ liệu khác Baseline không?**
   → Không. Cùng bộ BG20, cùng tham số nạp và augmentation; TSVM chỉ là khối trong mô hình.

---

## Phụ lục — Bảng tham số tổng hợp (dùng khi viết chương 3) ✅

| Nhóm | Tham số | Giá trị |
|---|---|---|
| Chuyển mask | Otsu | `THRESH_BINARY + THRESH_OTSU` |
| | Closing | kernel RECT 3×3, 1 lần |
| | Contour | `RETR_EXTERNAL`, `CHAIN_APPROX_SIMPLE` |
| | `min_area` | 20 pixel² |
| | `epsilon_ratio` | 0.002 × chu vi |
| Bộ dữ liệu | Ảnh nền | 200 (seed chọn 42), 160 train / 40 val |
| | Lớp | 1 (`0: polyp`) |
| Nạp ảnh | `imgsz` | 640 |
| | `bgr` | 0.0 (chuyển sang RGB) |
| | Pixel | chia 255 |
| | `mask_ratio`, `overlap_mask` | 4, true |
| Augmentation | `mosaic`, `close_mosaic` | 1.0, 10 |
| | `translate`, `scale`, `fliplr` | 0.1, 0.5, 0.5 |
| | `hsv_h`, `hsv_s`, `hsv_v` | 0.015, 0.7, 0.4 |
| | Tắt | `degrees`, `shear`, `perspective`, `flipud`, `mixup`, `cutmix`, `copy_paste`, `multi_scale` = 0 |

## Nguồn trong repo để tra cứu thêm

- Script chuyển đổi: `archive/Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py`.
- Bộ dữ liệu: `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/`.
- Cấu hình train: `archive/Ket_Qua_V2/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/Kvasir_BG20_YOLO26s_seg_TSVM_s0_w2/args.yaml`.
- Dàn ý + bản đồ đối chiếu chi tiết (số dòng code, vị trí chèn hình): `output/TIEN_XU_LY_DU_LIEU_DAN_Y_VA_DOI_CHIEU.md`.
- Kết quả kiểm tra dữ liệu: `output/kiem_tra_du_lieu_bg20.json`, `output/tien_xu_ly/kiem_tra/BAO_CAO_KIEM_TRA.md`.
- Code xử lý khi nạp: `archive/ultralytics_Topology-Shape-aware VMamba/data/` (`augment.py`, `dataset.py`, `base.py`, `utils.py`).
