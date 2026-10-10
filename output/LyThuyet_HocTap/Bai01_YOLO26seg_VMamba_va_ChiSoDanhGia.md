# BÀI 1 — YOLO26-seg, VMamba và các chỉ số đánh giá

> **Dành cho:** sinh viên mới tiếp cận phân đoạn ảnh (instance segmentation) và mô hình Mamba.
> **Mục tiêu:** đọc xong bạn giải thích được (1) YOLO26-seg biến một ảnh nội soi thành "khung + mặt nạ polyp" như thế nào, (2) VMamba là gì và vì sao gắn vào YOLO, (3) các con số mAP, Precision, Recall, p-value trong kết quả đề tài nghĩa là gì.
> **Cách đọc:** đọc Phần 0 (Pareto) trước. Nếu chỉ có 30 phút, đọc Phần 0 + các hộp "💡 Ý chính" là đủ nắm 80%.

Ký hiệu độ chắc chắn dùng trong bài:

| Nhãn | Nghĩa |
|---|---|
| ✅ **Đã xác nhận** | Đọc trực tiếp trong code/config/CSV của repo. |
| 📘 **Kiến thức chung** | Lý thuyết phổ biến trong ngành, không phụ thuộc repo. |
| ⚠️ **Chưa xác minh** | Thông tin từ công bố bên ngoài hoặc suy luận, chưa kiểm được trong repo. |

---

## Phần 0 — Pareto: 20% kiến thức cho 80% hiểu biết

Nếu phải chọn **5 ý** để nắm cả đề tài, hãy nắm 5 ý này. Mọi phần sau chỉ là giải thích chi tiết cho chúng.

| # | Ý cốt lõi (20%) | Vì sao nó "gánh" 80% | Đọc chi tiết |
|---|---|---|---|
| 1 | **YOLO = Backbone → Neck → Head.** Backbone trích đặc trưng, Neck trộn đặc trưng nhiều tỉ lệ (P3/P4/P5), Head ra kết quả. | Mọi cải tiến (kể cả TSVM) chỉ là thay một khối trong 3 phần này. | Phần 2 |
| 2 | **Mặt nạ = hệ số × prototype.** Mô hình học 32 "mặt nạ mẫu" chung, mỗi đối tượng chỉ cần 32 con số để pha trộn chúng thành mặt nạ riêng. | Đây là cách YOLO-seg làm phân đoạn mà vẫn nhanh. | Phần 3 |
| 3 | **YOLO26 bỏ NMS nhờ 2 nhánh head (one-to-many để học, one-to-one để dự đoán).** | Giải thích cấu trúc head, hàm loss và cả sự cố `fuse()` trong lịch sử đề tài. | Phần 4 |
| 4 | **VMamba = "quét" ảnh theo 4 hướng để mỗi điểm nhìn được toàn ảnh, chi phí tăng tuyến tính.** Đề tài đặt khối này (TSVM) ở **layer 10**, thay cho khối attention C2PSA. | Đây chính là đóng góp kiến trúc của đề tài. | Phần 5, 6 |
| 5 | **Chỉ số chính là Mask mAP@50-95**, trung bình trên 10 seed, kèm kiểm định thống kê. Kết quả hiện tại: TSVM cao hơn nhẹ nhưng **chưa có ý nghĩa thống kê** (p = 0.3839). | Biết đọc bảng kết quả và không phóng đại kết luận khi bảo vệ. | Phần 7, 8 |

> 💡 **Ý chính:** Ảnh → (Backbone có TSVM ở đỉnh) → (Neck trộn P3/P4/P5) → (Head Segment26: khung + lớp + 32 hệ số; Proto26: 32 prototype) → mặt nạ polyp → đo bằng Mask mAP@50-95.

---

## Phần 1 — Bài toán: ta đang dạy máy làm gì?

### 1.1. Ba mức "nhìn" ảnh

Tưởng tượng bác sĩ nhìn một ảnh nội soi đại tràng:

| Mức | Câu hỏi | Đầu ra | Ví dụ |
|---|---|---|---|
| Phân loại (classification) | "Ảnh có polyp không?" | 1 nhãn cho cả ảnh | "Có polyp" |
| Phát hiện (detection) | "Polyp nằm ở đâu?" | Khung chữ nhật (bounding box) | Khung quanh polyp |
| **Phân đoạn thực thể (instance segmentation)** | "Chính xác những pixel nào là polyp, và là polyp thứ mấy?" | **Khung + mặt nạ (mask) cho từng đối tượng** | Tô màu đúng viền từng polyp |

Đề tài làm mức thứ 3. Có một lớp duy nhất: `0: polyp` ✅. Ảnh "nền" (niêm mạc manh tràng bình thường, *normal-cecum*) **không có đối tượng nào** — mô hình phải học cách *không* báo polyp trên những ảnh này.

> 📘 **Phân biệt:** *Semantic segmentation* chỉ tô "pixel nào là polyp" mà không tách từng polyp. *Instance segmentation* tách riêng polyp 1, polyp 2… YOLO-seg là instance segmentation.

### 1.2. Vì sao chọn YOLO?

📘 YOLO ("You Only Look Once") dự đoán mọi đối tượng trong **một lần chạy mạng**, nên nhanh — phù hợp hướng ứng dụng nội soi thời gian thực. Đề tài dùng bản **YOLO26s-seg** (s = small) của Ultralytics làm baseline ✅.

---

## Phần 2 — Kiến trúc YOLO26-seg: Backbone → Neck → Head

### 2.1. Hình dung bằng ví dụ đời thường

Hãy nghĩ tới việc đọc một bức ảnh như **xem bản đồ ở nhiều mức zoom**:

- **Zoom gần (P3, chi tiết):** thấy viền, mạch máu, polyp nhỏ.
- **Zoom vừa (P4).**
- **Zoom xa (P5, tổng quan):** thấy bố cục cả vùng ruột, biết "chỗ này trông bất thường".

YOLO tạo ra cả 3 mức zoom rồi kết hợp chúng.

### 2.2. Số liệu cụ thể với ảnh 640×640 ✅

"Stride" là số lần ảnh bị thu nhỏ. P3/8 nghĩa là thu nhỏ 8 lần.

| Mức | Stride | Kích thước lưới | Số ô | Giỏi phát hiện |
|---|---|---|---|---|
| P3 | 8 | 80×80 | 6.400 | polyp nhỏ, viền chi tiết |
| P4 | 16 | 40×40 | 1.600 | polyp vừa |
| P5 | 32 | 20×20 | 400 | polyp lớn, ngữ cảnh toàn cục |

Tổng cộng **8.400 vị trí** mà head đưa ra dự đoán cho mỗi ảnh. Mỗi vị trí trả lời: "Ở đây có polyp không? Khung bao nhiêu? Mặt nạ trông thế nào?"

### 2.3. Sơ đồ kiến trúc (theo file YAML của đề tài) ✅

File: `archive/ultralytics_Topology-Shape-aware VMamba/cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml`

```text
Ảnh 640×640×3
  │
  ▼  BACKBONE (trích đặc trưng)
  0  Conv (stride 2)            → P1  320×320
  1  Conv (stride 2)            → P2  160×160
  2  C3k2
  3  Conv (stride 2)            → P3   80×80
  4  C3k2  ──────────────────────────────────┐ (đặc trưng P3)
  5  Conv (stride 2)            → P4   40×40  │
  6  C3k2  ─────────────────────────────┐     │ (đặc trưng P4)
  7  Conv (stride 2)            → P5   20×20  │
  8  C3k2                                │     │
  9  SPPF  (gom ngữ cảnh nhiều cỡ)      │     │
 10  ★ C2TSVMamba ★ (baseline: C2PSA)  ──┼──┐  │
  │                                      │  │  │
  ▼  NECK (trộn đặc trưng: đi lên rồi đi xuống)
 11-13  Upsample + nối với layer 6  → P4      │
 14-16  Upsample + nối với layer 4  → P3 (16) ── ra Head
 17-19  Conv xuống + nối layer 13   → P4 (19) ── ra Head
 20-22  Conv xuống + nối layer 10   → P5 (22) ── ra Head
  │
  ▼  HEAD
 23  Segment26( P3=16, P4=19, P5=22 )
       ├─ nhánh box   → 4 số tọa độ khung
       ├─ nhánh class → điểm tin cậy "là polyp"
       ├─ nhánh mask  → 32 hệ số
       └─ Proto26     → 32 prototype mask (160×160)
```

> 💡 **Ý chính:** File YAML của TSVM và baseline **giống hệt nhau, chỉ khác dòng layer 10**: baseline dùng `C2PSA` (khối attention), đề tài dùng `C2TSVMamba` ✅. Đây là thí nghiệm "thay đúng một biến" — rất tốt về phương pháp.

### 2.4. Các khối cơ bản (đủ dùng)

| Khối | Giải thích cho người mới |
|---|---|
| `Conv` | Tích chập + BatchNorm + hàm kích hoạt SiLU. Stride 2 → ảnh nhỏ đi một nửa. |
| `C3k2` | Khối tích chập "chia nhánh rồi ghép lại" (CSP), giúp học sâu mà ít tham số. |
| `SPPF` | Gộp (pooling) nhiều lần liên tiếp để mỗi điểm "thấy" vùng rộng hơn. |
| `C2PSA` | Khối có **self-attention** — cho mỗi điểm nhìn toàn ảnh. Đây là khối bị TSVM thay. |
| `Upsample` + `Concat` | Phóng to bản đồ đặc trưng rồi ghép với bản đồ cùng kích thước ở backbone (giống FPN/PAN). |

📘 **BatchNorm (BN)** chuẩn hóa đặc trưng bằng trung bình và phương sai *chạy* (running mean/var) học trong quá trình train. Nhớ khái niệm này — nó liên quan tới sự cố seed 0/5/8 ở Phần 8.4.

---

## Phần 3 — Mặt nạ được tạo ra như thế nào? (Prototype × Hệ số)

Đây là ý **quan trọng nhất** của "-seg".

### 3.1. Trực giác: hộp màu pha sẵn

Giả sử bạn có **32 tấm giấy can** (prototype), mỗi tấm tô sẵn một "mẫu" khác nhau trên toàn ảnh: tấm thì sáng ở vùng viền tròn, tấm thì sáng ở vùng đỏ, tấm thì sáng ở góc trái…

Với mỗi polyp, mô hình chỉ cần nói: "lấy 0.9 × tấm 1 + (−0.3) × tấm 2 + … + 0.5 × tấm 32". Chồng lên nhau ra đúng hình polyp đó. **32 con số đó là "hệ số mặt nạ" (mask coefficients).**

→ Lợi ích: không phải vẽ mặt nạ riêng cho 8.400 vị trí; chỉ vẽ 32 prototype **một lần cho cả ảnh**, rồi mỗi đối tượng chỉ tốn 32 số.

### 3.2. Công thức tối thiểu 📘

```text
mask_i = sigmoid( c_i · P )        rồi cắt (crop) theo khung của đối tượng i
```

- `P`: 32 prototype, mỗi cái 160×160.
- `c_i`: vector 32 hệ số của đối tượng *i*.
- `sigmoid` đưa giá trị về (0, 1); ngưỡng 0.5 → pixel thuộc polyp.

### 3.3. Trong code đề tài ✅

- `Segment26` (`nn/modules/head.py`) có `nm=32` (số prototype), `npr=256` (số kênh trung gian).
- `Proto26` (`nn/modules/block.py`) **trộn đặc trưng P4, P5 về P3** rồi phóng to ×2 → 160×160. Khác Proto đời cũ chỉ dùng P3.
- Khi train, `Proto26` có thêm **nhánh `semseg`** (phân đoạn ngữ nghĩa phụ trợ) để "dạy thêm" cho mạng; khi suy luận nhánh này bị bỏ qua (`fuse()` đặt `semseg = None`). Đó là nguồn gốc cột `sem_loss` trong `results.csv`.

> 💡 **Ý chính:** Mặt nạ có độ phân giải 160×160 rồi mới phóng về kích thước ảnh. Vì vậy viền mặt nạ phụ thuộc mạnh vào **chất lượng đặc trưng P3** — điểm cần nhớ khi bàn hướng cải tiến (ví dụ đặt VMamba ở P3).

---

## Phần 4 — Điểm mới của YOLO26: NMS-free, hai nhánh head

### 4.1. NMS là gì và tại sao muốn bỏ? 📘

Các YOLO cũ thường đưa ra **nhiều khung chồng nhau** cho cùng một polyp. Sau đó dùng **NMS** (Non-Maximum Suppression): giữ khung điểm cao nhất, xóa các khung trùng nhiều với nó. NMS là bước hậu xử lý thủ công, tốn thời gian và có ngưỡng phải chỉnh.

YOLO26 được thiết kế **end-to-end**: mạng tự học để mỗi đối tượng **chỉ có một dự đoán**, nên không cần NMS.

### 4.2. Hai nhánh head ✅

Trong config: `end2end: True`, `reg_max: 1`.

| Nhánh | Gán nhãn | Vai trò |
|---|---|---|
| **one2many** (`cv2`, `cv3`, `cv4`) | 1 polyp ↔ nhiều vị trí dự đoán (top-k = 10) | Cho nhiều tín hiệu học → train nhanh, ổn định. |
| **one2one** (`one2one_cv2/cv3/cv4`) | 1 polyp ↔ đúng 1 vị trí (top-k cuối = 1) | Dùng khi dự đoán → không cần NMS. |

Hàm loss (`E2ELoss` trong `utils/loss.py`) trộn hai nhánh:

```text
loss = w_o2m · loss_one2many + (1 − w_o2m) · loss_one2one
w_o2m giảm tuyến tính từ 0.8 (đầu train) xuống 0.1 (cuối train)
```

→ Đầu train dựa vào one2many cho dễ học; cuối train dồn trọng số sang one2one vì đó là nhánh sẽ dùng thật.

**`fuse()`:** khi chuẩn bị suy luận, Ultralytics gọi `fuse()` → **xóa nhánh one2many** (`cv2 = cv3 = cv4 = None`) và xóa `semseg` của Proto26 ✅. Mô hình nhẹ hơn, kết quả không đổi vì đằng nào cũng chỉ dùng one2one.

### 4.3. Các thay đổi khác của YOLO26

| Thay đổi | Trạng thái |
|---|---|
| `reg_max: 1` → bỏ DFL (Distribution Focal Loss); thay bằng **L1 loss** cho tọa độ khung → cột `l1_loss` trong `results.csv` | ✅ (`utils/loss.py`: `"dfl_loss" if self.use_dfl else "l1_loss"`) |
| Có optimizer **MuSGD** trong fork | ✅ có code; nhưng đề tài train bằng **AdamW**, `lr0 = 0.001` (theo `args.yaml`) ✅ |
| ProgLoss, STAL (gán nhãn ưu tiên vật thể nhỏ) | ⚠️ theo công bố của Ultralytics, bài này không kiểm chứng chi tiết trong code |

### 4.4. Các thành phần loss bạn sẽ thấy trong `results.csv` ✅

| Cột | Đo cái gì | Nói nôm na |
|---|---|---|
| `box_loss` | Khung dự đoán lệch khung thật bao nhiêu (dựa trên IoU) | Khung đặt có chuẩn không |
| `l1_loss` | Sai số tuyệt đối của tọa độ khung | Bổ sung cho box_loss (thay DFL) |
| `cls_loss` | Phân loại "có polyp / không" (BCE) | Có nhận ra polyp không, có báo nhầm nền không |
| `seg_loss` | Mặt nạ dự đoán khác mặt nạ thật từng pixel (BCE trong khung) | Tô viền có đúng không |
| `sem_loss` | Nhánh phân đoạn ngữ nghĩa phụ trợ (BCE + Dice) | Chỉ có khi train |

Loss càng **thấp** càng tốt. `train/...` là trên tập train, `val/...` là trên tập validation. Nếu `train` giảm mà `val` tăng → dấu hiệu **overfitting** (học thuộc).

---

## Phần 5 — VMamba từ con số 0

### 5.1. Vấn đề: làm sao để mỗi điểm "nhìn" được cả ảnh?

| Cách | Ý tưởng | Điểm mạnh | Điểm yếu |
|---|---|---|---|
| **CNN** (tích chập) | Mỗi điểm chỉ nhìn ô 3×3 xung quanh; xếp nhiều lớp mới nhìn rộng | Nhanh, giỏi chi tiết cục bộ (viền, kết cấu) | Khó nắm ngữ cảnh xa |
| **Transformer / Attention** | Mỗi điểm so sánh với **mọi** điểm khác | Nhìn toàn cục | Chi phí ∝ N² (N = số điểm). 400 điểm → 160.000 cặp |
| **Mamba / SSM** | Đi **tuần tự** qua các điểm, mang theo một "trí nhớ" tóm tắt | Nhìn toàn cục, chi phí ∝ N | Ảnh 2D phải "duỗi" thành chuỗi 1D |

### 5.2. Trực giác SSM: đọc sách có ghi chú

Tưởng tượng bạn đọc một cuốn sách từng trang. Bạn không nhớ hết từng chữ, nhưng có **một cuốn sổ ghi chú** (trạng thái ẩn `h`). Mỗi trang mới:

1. Quên bớt một phần ghi chú cũ (nhân với hệ số `a` từ 0 đến 1).
2. Thêm thông tin quan trọng của trang hiện tại (`b`).
3. Khi cần trả lời, đọc từ sổ ghi chú (`C`).

Công thức (📘 State Space Model rời rạc):

```text
h_t = a_t · h_{t-1} + b_t          (cập nhật trí nhớ)
y_t = C_t · h_t                     (đọc ra kết quả)
```

**"Selective" (chọn lọc)** — điểm làm Mamba khác SSM cổ điển: các hệ số `a_t`, `b_t`, `C_t` **phụ thuộc vào chính dữ liệu đang đọc**. Gặp thông tin quan trọng (ví dụ vùng đỏ bất thường) → ghi mạnh vào sổ; gặp niêm mạc bình thường → ghi nhẹ. Giống người đọc thông minh biết chỗ nào cần ghi chú.

### 5.3. Vì sao "V" — Vision Mamba (VMamba)?

Ảnh là 2D, nhưng SSM đọc chuỗi 1D. Nếu chỉ đọc từ trái→phải, trên→dưới, điểm ở đầu ảnh không biết gì về cuối ảnh. **VMamba** giải bằng **SS2D (2D Selective Scan): quét 4 hướng** rồi cộng lại:

```text
Hướng 0: theo hàng, trái→phải, trên→dưới   →→→→
Hướng 1: ngược hướng 0                       ←←←←
Hướng 2: theo cột, trên→dưới                 ↓↓↓↓
Hướng 3: ngược hướng 2                       ↑↑↑↑
```

Sau 4 lượt, mỗi điểm đã nhận thông tin từ mọi phía của ảnh.

### 5.4. SS2D trong code đề tài ✅

File: `nn/modules/topology_shape_vmamba.py`, class `SS2D`. Đi theo từng bước:

| Bước | Code | Giải thích |
|---|---|---|
| 1 | `in_proj` → tách `u`, `z` | `u` là dữ liệu sẽ quét, `z` là "cổng" điều tiết đầu ra |
| 2 | `conv2d` depthwise 3×3 + SiLU | Trộn thông tin lân cận trước khi quét |
| 3 | Tạo 4 chuỗi `u_0..u_3` (flatten, flip, transpose) | 4 hướng quét |
| 4 | `x_proj`, `dt_projs` → `dt`, `B`, `C` | Các hệ số **phụ thuộc dữ liệu** (tính chọn lọc) |
| 5 | `a = exp(dt · A)`, `A = −exp(A_logs)` | Hệ số "quên", luôn trong (0, 1] |
| 6 | `parallel_associative_scan(a, b)` | Tính toàn bộ `h_t` **song song** trong O(log L) bước, thay vì vòng for từng điểm |
| 7 | Gập 4 hướng về lưới 2D, **cộng lại** | Hợp nhất thông tin 4 phía |
| 8 | `y * SiLU(z)` rồi `out_proj` | Cổng điều tiết + chiếu ra |

Ở layer 10 (P5, lưới 20×20) chuỗi dài **L = 400**. Mô hình bản `s` có 512 kênh ở layer này; `C2TSVMamba` tách đôi nên khối TSVMamba bên trong làm việc với **256 kênh**, `d_state = 16` ✅ (suy từ YAML: width 0.5 × 1024, `e = 0.5`).

> 💡 **Ý chính:** VMamba = SSM chọn lọc + quét 4 hướng. Nó đóng vai trò giống attention (nhìn toàn cục) nhưng chi phí tuyến tính theo số điểm.

> ⚠️ **Lưu ý trung thực:** SS2D trong fork là bản **cài đặt thuần PyTorch** (associative scan song song), không phải CUDA kernel chính thức của VMamba. Khi viết khóa luận nên mô tả là "triển khai SS2D theo ý tưởng VMamba", không khẳng định tốc độ bằng bản gốc.

---

## Phần 6 — TSVM: VMamba "có ý thức về hình dạng" của đề tài

### 6.1. Ý tưởng

Polyp có đặc điểm **hình học**: thường tròn/bầu dục, viền liền mạch. VMamba giỏi ngữ cảnh toàn cục nhưng không chuyên về viền. TSVM (Topology-Shape-aware VMamba) ghép **2 nhánh**:

```text
                x (đặc trưng P5)
        ┌───────────┴────────────┐
        ▼                        ▼
   SS2D (VMamba)           ShapeAwareBranch
   ngữ cảnh toàn cục       (DWConv 3×3 + 5×5)
        │                        ▼
        │               DirectionalShapeExtractor
        │               (1×5 ngang, 5×1 dọc, 3×3,
        │                độ lớn gradient √(h²+v²))
        │                        │ = S
        │                        ▼
        │               TopologyShapeGate (1×1 + sigmoid) → G ∈ [0,1]
        ▼                        │
   F_M  ⊙ (1 + G)  ◄─────────────┘     (hình dạng "khuếch đại" đặc trưng toàn cục)
        │
   ghép với S → Conv 1×1 → FFN
        │
   out = x + γ · (...)       γ khởi tạo 0.001
```

### 6.2. Giải thích từng chi tiết cho người mới

| Thành phần | Ý nghĩa trực giác |
|---|---|
| `ShapeAwareBranch` | Hai "kính lúp" cỡ 3×3 và 5×5 tìm đường cong, viền cục bộ. |
| `DirectionalShapeExtractor` | Kernel dải **1×5** bắt viền chạy ngang, **5×1** bắt viền chạy dọc; `√(h² + v²)` giống công thức độ lớn gradient (như bộ lọc Sobel) → chỗ nào có biên mạnh sẽ sáng. |
| `TopologyShapeGate` | Biến thông tin hình dạng thành bản đồ trọng số G từ 0 đến 1. |
| `F_M ⊙ (1 + G)` | Chỗ nào có dấu hiệu hình dạng (G cao) thì đặc trưng VMamba được **tăng lên tối đa gấp đôi**; chỗ khác giữ nguyên (×1). Dùng `1 + G` thay vì `G` để không bao giờ "tắt hẳn" thông tin toàn cục. |
| `γ = 0.001` (residual scaling) | Lúc mới train, khối mới gần như "trong suốt" (out ≈ x) → không phá đặc trưng pretrained; γ được học tăng dần. Đây là mẹo ổn định phổ biến. |
| `C2TSVMamba` | Vỏ bọc kiểu C2/C2PSA: chia kênh làm hai, một nửa đi qua TSVMamba, rồi ghép lại. Nhờ đó cắm thay `C2PSA` mà không đổi số kênh. |

Code còn có các **chế độ ablation** (`mode`): `vmamba_only`, `shape_only`, `shape_vmamba_no_guidance`, `topology_shape_vmamba` ✅ — dùng để chứng minh từng nhánh có đóng góp. ⚠️ Repo hiện **chưa có** kết quả 10 seed cho từng chế độ ablation này.

### 6.3. Nhận xét phản biện (nên tự chuẩn bị trước khi bảo vệ)

- **Tên "topology-aware" cần dùng thận trọng.** Về bản chất, nhánh này là tích chập có hướng + độ lớn gradient. Không có loss topo (ví dụ đếm số thành phần liên thông, persistent homology). Nên viết: "khối trích đặc trưng hình dạng và biên có hướng, *được đặt tên* topology-shape-aware".
- **TSVM chỉ ở P5 (20×20).** Mỗi ô P5 ứng với 32×32 pixel ảnh gốc → thông tin viền chi tiết đã bị nén nhiều. Còn mặt nạ chủ yếu sinh từ P3 (Phần 3.3). Đây là lý do có ý tưởng đặt VMamba ở P3 (`C3k2VSS`) — nhưng hướng P3 hiện **⚠️ chưa có trong repo (NOT VERIFIED IN REPOSITORY)**.

---

## Phần 7 — Các chỉ số đánh giá (đọc kỹ phần này)

### 7.1. Viên gạch đầu tiên: IoU

**IoU (Intersection over Union)** = phần giao / phần hợp của vùng dự đoán và vùng thật.

```text
         Dự đoán  ████████
         Thật          ████████
         Giao          ███        IoU = Giao / Hợp
         Hợp      ███████████
```

- IoU = 1: trùng khít. IoU = 0: không chạm nhau.
- **Box IoU:** tính trên hai khung chữ nhật.
- **Mask IoU:** tính trên **từng pixel** của hai mặt nạ → khắt khe hơn nhiều với viền.

**Ví dụ số:** mặt nạ thật 1.000 pixel, dự đoán 900 pixel, trùng 800 pixel. Hợp = 1.000 + 900 − 800 = 1.100. IoU = 800 / 1.100 ≈ **0.727**.

### 7.2. TP, FP, FN — khi nào một dự đoán là "đúng"?

Chọn một **ngưỡng IoU**, ví dụ 0.5:

| Ký hiệu | Nghĩa | Ví dụ trong nội soi |
|---|---|---|
| **TP** (True Positive) | Dự đoán khớp một polyp thật với IoU ≥ ngưỡng | Tô đúng polyp |
| **FP** (False Positive) | Dự đoán không khớp polyp nào (hoặc IoU thấp, hoặc trùng lặp) | Báo polyp trên niêm mạc bình thường → **báo động giả** |
| **FN** (False Negative) | Polyp thật mà không dự đoán nào khớp | **Bỏ sót polyp** — nguy hiểm nhất về lâm sàng |
| TN (True Negative) | "Không báo gì và đúng là không có gì" | Trong phát hiện đối tượng, TN **không đếm được tự nhiên** (vô số vị trí trống) |

### 7.3. Precision và Recall

```text
Precision = TP / (TP + FP)     "Trong những gì mô hình báo, bao nhiêu % là thật?"
Recall    = TP / (TP + FN)     "Trong các polyp thật, mô hình tìm được bao nhiêu %?"
```

**Ví dụ:** tập val có **127 polyp** ✅. Mô hình đúng 111, bỏ sót 16, báo nhầm 18.
- Precision = 111 / (111 + 18) = **0.860**
- Recall = 111 / (111 + 16) = **0.874**

📘 Trong y tế thường ưu tiên **Recall** (không bỏ sót polyp), nhưng Precision quá thấp sẽ làm bác sĩ mệt vì báo động giả. **F1 = 2PR / (P + R)** cân bằng hai cái.

**Ngưỡng tin cậy (confidence):** mỗi dự đoán có một điểm 0–1. Hạ ngưỡng → báo nhiều hơn → Recall tăng, Precision giảm. Đây là sự đánh đổi.

### 7.4. AP — diện tích dưới đường Precision–Recall

Thay vì chọn một ngưỡng confidence, ta **quét mọi ngưỡng** và vẽ đường **Precision theo Recall**. **AP (Average Precision)** = diện tích dưới đường đó (0 đến 1).

- AP cao = mô hình vừa tìm được nhiều polyp, vừa ít báo nhầm, *ở mọi mức ngưỡng*.
- Fork dùng cách nội suy **101 điểm kiểu COCO** ✅ (`np.linspace(0, 1, 101)` trong `utils/metrics.py`).

### 7.5. mAP@50 và mAP@50-95

- **mAP** = trung bình AP qua các lớp. Đề tài chỉ có 1 lớp → mAP = AP của lớp polyp.
- **mAP@50:** AP với ngưỡng IoU = 0.5. Dễ tính đúng: chỉ cần trùng khoảng một nửa.
- **mAP@50-95:** trung bình AP ở **10 ngưỡng IoU: 0.50, 0.55, …, 0.95** ✅ (`torch.linspace(0.5, 0.95, 10)`). Muốn điểm cao phải khớp **rất sát** viền.

| Chỉ số | Hỏi gì | Đề tài dùng để |
|---|---|---|
| Box mAP@50 | "Tìm thấy polyp không?" | Tham khảo |
| **Mask mAP@50-95** | "Tô viền polyp chính xác tới đâu?" | **Chỉ số chính** để so sánh mô hình và chọn epoch tốt nhất ✅ |

> 💡 **Ý chính:** Mask mAP@50 của đề tài ≈ 0.91 nhưng Mask mAP@50-95 ≈ 0.72. Khoảng cách này nói rằng mô hình **tìm polyp rất tốt** nhưng **viền chưa thật sát** ở ngưỡng IoU cao. Muốn cải thiện, phải cải thiện chất lượng viền.

### 7.6. (B) và (M) trong `results.csv` ✅

`metrics/mAP50-95(B)` = Box, `metrics/mAP50-95(M)` = Mask. Đừng trộn hai loại khi so sánh.

### 7.7. Dice và IoU — liên hệ với các bài báo phân đoạn polyp

Nhiều bài về Kvasir-SEG (U-Net, PraNet) báo cáo **Dice** và **mIoU** theo pixel, không phải mAP.

```text
Dice = 2·|A∩B| / (|A| + |B|)        Dice = 2·IoU / (1 + IoU)
```

Ví dụ IoU = 0.8 → Dice ≈ 0.889. ⚠️ Pipeline YOLO BG20 của đề tài **không xuất Dice**. Vì vậy **không so sánh trực tiếp** Mask mAP@50-95 của đề tài với "Dice 0.9x" của bài báo khác — hai thước đo khác nhau, tập chia dữ liệu cũng khác.

### 7.8. Ma trận nhầm lẫn và chuyện TN trên ảnh nền

File `raw_10seeds_confusion_matrices.csv` có cột TP, FN, FP, TN. Ví dụ Baseline seed 0: TP=111, FN=16, FP=18, TN=22 ✅.

- TP + FN = **127** = số polyp thật.
- FP + TN = **40** = số ảnh nền.

⚠️ Cần biết: Ultralytics **không tự đếm TN**. Báo cáo kiểm toán (`06_reports/FORENSIC_EXPERIMENT_AUDIT.md`) xác nhận **TN = 40 − FP là số tái dựng**, và các con số FP/TN đang ở trạng thái *DISCREPANCY* (chênh lệch giữa ảnh PNG và CSV). → **Không dùng FP/TN làm số liệu chính** cho tới khi tái lập được.

### 7.9. Các chỉ số thống kê nhiều seed

Một lần train có yếu tố ngẫu nhiên (khởi tạo, thứ tự batch, augmentation). Train 1 lần rồi kết luận là **không đáng tin**. Đề tài train **10 seed (0–9)** cho mỗi mô hình ✅.

| Khái niệm | Giải thích |
|---|---|
| **Mean ± Std** | Trung bình và độ lệch chuẩn qua 10 seed. Std nhỏ = mô hình ổn định. |
| **Best epoch** | Epoch có Mask mAP@50-95 cao nhất trong `results.csv` (cách đề tài trích số liệu) ✅ |
| **Paired t-test** | So sánh từng cặp cùng seed (Baseline seed k vs TSVM seed k). Hỏi: "Chênh lệch trung bình có khác 0 thật không, hay do may rủi?" |
| **p-value** | Xác suất thấy chênh lệch lớn cỡ này *nếu thực ra hai mô hình như nhau*. **p < 0.05** → thường gọi là "có ý nghĩa thống kê". |
| **F-ratio (tỉ số phương sai)** | Std² của mô hình này chia mô hình kia → so độ ổn định. |
| **Win rate theo seed** | Đếm số seed mà mô hình A thắng B. Tham khảo, không thay thế kiểm định. |

> ⚠️ **Lưu ý tiêu chí chọn best.pt:** Ultralytics lưu `best.pt` theo `fitness` = **Box mAP@50-95 + Mask mAP@50-95** ✅ (`SegmentMetrics.fitness` trong `utils/metrics.py`). Còn bảng phân tích 10 seed chọn epoch theo **Mask mAP@50-95 riêng**. Hai tiêu chí thường trùng nhưng **không bắt buộc trùng** — nếu đánh giá lại `best.pt`, hãy kiểm tra epoch.

---

## Phần 8 — Liên hệ kết quả thật của đề tài

### 8.1. Cấu hình huấn luyện ✅ (`args.yaml`, TSVM seed 0)

| Tham số | Giá trị | Nghĩa |
|---|---|---|
| `pretrained` | `yolo26s-seg.pt` | Khởi tạo từ trọng số đã học sẵn |
| `epochs` | 100 | Số vòng học |
| `batch` | 8 | Số ảnh mỗi bước |
| `imgsz` | 640 | Kích thước ảnh đầu vào |
| `optimizer`, `lr0` | AdamW, 0.001 | Thuật toán tối ưu, tốc độ học ban đầu |
| `box`, `cls`, `dfl` | 7.5, 0.5, 1.5 | Trọng số các thành phần loss |
| GPU | Kaggle Tesla T4 | |

### 8.2. Kết quả 10 seed ✅ (`KQ_Nen_DX_10seed/06_reports/summary.md`)

| Chỉ số | Baseline | TSVM | Δ | p-value |
|---|---|---|---|---|
| **Mask mAP@50-95** | 0.7210 ± 0.0129 | 0.7246 ± 0.0078 | +0.0036 | 0.3839 |
| Mask mAP@50 | 0.9119 ± 0.0107 | 0.9062 ± 0.0082 | −0.0056 | 0.2273 |
| Mask Precision | 0.9023 ± 0.0339 | 0.9118 ± 0.0246 | +0.0095 | 0.5428 |
| Mask Recall | 0.8584 ± 0.0252 | 0.8625 ± 0.0173 | +0.0041 | 0.5907 |
| Val Seg Loss | 1.3045 ± 0.0867 | 1.2424 ± 0.0387 | −0.0622 | 0.0908 |

### 8.3. Cách đọc đúng (và cách nói khi bảo vệ)

1. **TSVM cao hơn 0.36 điểm phần trăm Mask mAP@50-95, nhưng p = 0.3839 > 0.05 → chưa đủ bằng chứng thống kê để nói TSVM tốt hơn.** Không được viết "cải thiện đáng kể".
2. **Std của TSVM nhỏ hơn** (0.0078 so với 0.0129) → TSVM **có xu hướng ổn định hơn** qua các seed. Đây là điểm tích cực có thể nêu, kèm chữ "xu hướng".
3. Val Seg Loss thấp hơn ở 8/10 seed, p = 0.0908 → **gần** ngưỡng nhưng vẫn chưa đạt.
4. Mask mAP@50 của TSVM lại thấp hơn nhẹ → không có cải thiện đồng loạt.

Câu gợi ý: *"Trên 10 seed, TSVM đạt Mask mAP@50-95 trung bình 0.7246 so với 0.7210 của baseline, với độ lệch chuẩn thấp hơn; tuy nhiên kiểm định t ghép cặp cho p = 0.3839, nên chênh lệch chưa có ý nghĩa thống kê ở mức α = 0.05."*

### 8.4. Sự cố seed 0/5/8 — bài học về BatchNorm và FP16

Khi đánh giá lại `best.pt`/`last.pt` của TSVM seed 0, 5, 8, kết quả **sụp** (ví dụ seed 5 có TP = 0) dù `results.csv` lúc train vẫn tốt.

- Hồ sơ cũ (doc 17) cho rằng do `fuse()`. **Báo cáo mới nhất** (`output/BaoCaoKetQua/BAO_CAO_SU_CO_PHINH_SO_TSVM_SEED_0_5_8.md`) xác định nguyên nhân là **tràn số FP16 ở thống kê BatchNorm của layer 10** khi checkpoint được lưu ở dạng nửa độ chính xác — không phải do `fuse()`.
- Trực giác: nhánh SS2D khuếch đại tín hiệu lên tới **hàng triệu**, nên BatchNorm ngay sau đó phải nhớ trung bình (`running_mean`) cỡ hàng triệu. Code cũ lưu checkpoint ở **FP16**, mà FP16 chỉ chứa tối đa **65.504** → giá trị bị **cắt** về 65.504. Mở file ra dùng, BN trừ sai trung bình → dự đoán hỏng. Hiệu chỉnh lại thống kê BN đưa Mask mAP50 seed 5 từ 0 về 0,9099, khớp giá trị lúc train (0,9096).
- Bản vá lưu checkpoint FP32 nằm ở dự án anh em `../DL_Poylp_v26_VMamba_TestDemo_V2/`.

> 💡 **Bài học:** Số liệu 10 seed lấy từ `results.csv` (đo trong lúc train) không bị ảnh hưởng; còn **checkpoint** của 3 seed thì có vấn đề. Luôn phân biệt "số đo lúc train" và "đánh giá lại từ file trọng số".

---

## Phần 9 — Hiểu lầm thường gặp

| Hiểu lầm | Đúng là |
|---|---|
| "mAP@50-95 là mAP ở IoU 50% đến 95% cộng lại" | Là **trung bình** AP ở 10 ngưỡng IoU 0.50→0.95, bước 0.05. |
| "Precision cao là mô hình tốt" | Có thể chỉ vì mô hình báo rất ít (Recall thấp). Phải xem cả hai, hoặc AP. |
| "TSVM thay toàn bộ backbone bằng Mamba" | Chỉ thay **một khối ở layer 10** (C2PSA → C2TSVMamba). |
| "Mamba nhanh hơn attention nên mô hình nhanh hơn" | Ở 20×20 = 400 điểm, attention vốn đã rẻ; bản SS2D thuần PyTorch còn có thể chậm hơn. Muốn nói về tốc độ phải đo thật. |
| "Nhánh topology học topo của polyp" | Là tích chập có hướng + gradient; không có ràng buộc topo tường minh. |
| "fuse() làm hỏng mô hình" | `fuse()` chỉ bỏ nhánh one2many và semseg — vốn không dùng khi suy luận. Sự cố seed 0/5/8 là do FP16 ở BN. |
| "p = 0.38 nghĩa là 38% khả năng TSVM tốt hơn" | Sai. p-value không phải xác suất giả thuyết đúng; chỉ cho biết dữ liệu chưa đủ bác bỏ "hai mô hình như nhau". |

---

## Phần 10 — Tự kiểm tra (có đáp án)

1. **Ba mức P3/P4/P5 ở ảnh 640 có kích thước bao nhiêu? Tổng số vị trí dự đoán?**
   → 80×80, 40×40, 20×20; tổng 8.400.
2. **Mặt nạ của một polyp được tạo từ đâu?**
   → 32 hệ số của đối tượng × 32 prototype (160×160) → sigmoid → cắt theo khung.
3. **Vì sao YOLO26 không cần NMS?**
   → Nhánh one2one được huấn luyện gán đúng 1 dự đoán cho 1 đối tượng; one2many chỉ hỗ trợ học và bị xóa khi `fuse()`.
4. **VMamba quét bao nhiêu hướng? Tại sao không quét 1 hướng?**
   → 4 hướng; 1 hướng thì điểm đầu chuỗi không nhận được thông tin từ phần sau của ảnh.
5. **Công thức điều biến trong TSVM? Tại sao là (1 + G)?**
   → `F_M ⊙ (1 + G)`; để vùng G ≈ 0 vẫn giữ đặc trưng toàn cục, chỉ khuếch đại chứ không tắt.
6. **127 polyp, đúng 112, bỏ sót 15, báo nhầm 7. Tính P, R.**
   → P = 112/119 ≈ 0.941; R = 112/127 ≈ 0.882.
7. **Vì sao Mask mAP@50-95 thấp hơn nhiều so với Mask mAP@50?**
   → Ngưỡng IoU cao (0.75–0.95) đòi viền gần như khít; mô hình tìm đúng polyp nhưng viền chưa sát.
8. **Có được viết "TSVM cải thiện đáng kể so với baseline" không?**
   → Không. p = 0.3839 > 0.05. Chỉ nói "cao hơn nhẹ, ổn định hơn, chưa có ý nghĩa thống kê".

---

## Phụ lục — Bảng thuật ngữ nhanh

| Thuật ngữ | Nghĩa ngắn |
|---|---|
| Backbone / Neck / Head | Trích đặc trưng / trộn đa tỉ lệ / sinh kết quả |
| Stride | Hệ số thu nhỏ ảnh |
| Prototype mask | Mặt nạ mẫu dùng chung cho cả ảnh |
| Mask coefficient | 32 số pha trộn prototype cho từng đối tượng |
| NMS | Lọc bỏ khung trùng lặp sau dự đoán |
| One2many / One2one | Gán 1 đối tượng cho nhiều / đúng 1 dự đoán |
| SSM | Mô hình không gian trạng thái: trí nhớ `h` cập nhật tuần tự |
| Selective scan | SSM có hệ số phụ thuộc dữ liệu (Mamba) |
| SS2D | Quét chọn lọc 2D theo 4 hướng (VMamba) |
| IoU / Dice | Độ trùng giữa vùng dự đoán và vùng thật |
| AP / mAP | Diện tích dưới đường Precision–Recall / trung bình qua lớp |
| Seed | Hạt giống ngẫu nhiên; đổi seed = một lần train độc lập |
| p-value | Mức bằng chứng chống lại giả thuyết "không khác biệt" |

## Nguồn trong repo để tra cứu thêm

- Kiến trúc: `archive/ultralytics_Topology-Shape-aware VMamba/cfg/models/26/` (so sánh `yolo26-seg.yaml` với `yolo26-seg-TopologyShapeVMamba.yaml`).
- Module TSVM: `archive/ultralytics_Topology-Shape-aware VMamba/nn/modules/topology_shape_vmamba.py`.
- Head và Proto: `nn/modules/head.py` (`Segment26`), `nn/modules/block.py` (`Proto26`).
- Loss: `utils/loss.py` (`v8SegmentationLoss`, `E2ELoss`). Chỉ số: `utils/metrics.py`.
- Kết quả: `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/summary.md`, `01_raw_analysis/`.
- Sự cố FP16: `output/BaoCaoKetQua/BAO_CAO_SU_CO_PHINH_SO_TSVM_SEED_0_5_8.md`.
