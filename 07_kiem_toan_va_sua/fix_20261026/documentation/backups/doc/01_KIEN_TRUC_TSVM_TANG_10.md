# CHI TIẾT KIẾN TRÚC TOPOLOGY-SHAPE-AWARE VMAMBA TẠI TẦNG 10
## PHÂN TÍCH MODULE `C2TSVMamba` TRONG MÔ HÌNH ĐỀ XUẤT YOLO26s-seg-TSVM

---

## 1. VỊ TRÍ TÍCH HỢP TẠI TẦNG 10 CỦA BACKBONE

Tệp cấu hình kiến trúc:
`cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml`

Trong mô hình **Baseline YOLO26s-seg**, tầng 10 ở cuối backbone (sau khối SPPF) sử dụng:
```yaml
# Baseline Backbone Layer 10
- [-1, 2, C2PSA, [1024]] # C2 Pointwise Spatial Attention (Self-Attention chuẩn)
```

Trong mô hình **Cải tiến YOLO26s-seg-TSVM**, tầng 10 được thay thế bằng module:
```yaml
# TSVM Backbone Layer 10
- [-1, 2, C2TSVMamba, [1024]] # C2 Topology-Shape-aware VMamba
```

### Tại sao lại tích hợp tại Tầng 10 (Backbone P5)?
1. **Giảm thiểu độ trễ tính toán:** Tại tầng P5, kích thước không gian của feature map đã được giảm 32 lần (với ảnh đầu vào $640 	imes 640$, feature map P5 chỉ còn $20 	imes 20$). Việc áp dụng cơ chế quét tuần tự 2D (SS2D) tại kích thước $20 	imes 20$ giúp kiểm soát chi phí tính toán, tránh làm bùng nổ thời gian huấn luyện so với việc đặt ở P3 ($80 	imes 80$) hay P4 ($40 	imes 40$).
2. **Khai thác ngữ nghĩa cấp cao kết hợp hình học topo:** Tầng cuối của backbone chứa các đặc trưng giàu ngữ nghĩa phân loại polyp, nhưng thường bị mất mát chi tiết ranh giới hình học do nhiều tầng tích chập stride=2. Việc chèn khối định hướng hình thái và topo tại đây giúp "nắn chỉnh" lại các đặc trưng viền trước khi chuyển tiếp sang Neck (FPN/PAN) để giải mã mặt nạ.

---

## 2. KIẾN TRÚC BÊN TRONG CỦA MODULE `C2TSVMamba`

Mã nguồn triển khai chi tiết:
`nn/modules/topology_shape_vmamba.py` (502 dòng code PyTorch thuần, không phụ thuộc C++/CUDA extension bên ngoài).

Kiến trúc được xây dựng từ **6 khối thành phần phân cấp**:

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 Đầu vào x: [B, C, H, W]                │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                         ┌────────────────────┴────────────────────┐
                         │                                         │
                         ▼                                         ▼
            ┌───────────────────────────┐             ┌───────────────────────────┐
            │      1. Nhánh Toàn cục    │             │      2. Nhánh Cục bộ      │
            │           (SS2D)          │             │    (ShapeAwareBranch &    │
            │ - 4 hướng quét SS2D       │             │ DirectionalShapeExtractor)│
            │ - Associative Scan log(L) │             │ - Dải tích chập 1x5, 5x1  │
            │ - Ngữ cảnh toàn cục O(N)  │             │ - Gradient biên topo d    │
            └─────────────┬─────────────┘             └─────────────┬─────────────┘
                          │                                         │
                          │        ┌─────────────────────────┐      │
                          │        │ 3. Cổng điều phối Topo  │      │
                          │        │   (TopologyShapeGate)   │◄─────┘
                          │        │ - Sinh bản đồ trọng số  │
                          │        │   Gate map G in [0, 1]  │
                          │        └────────────┬────────────┘
                          │                     │
                          ▼                     ▼
                  ┌────────────────────────────────────────────────────────┐
                  │               4. Điều phối và Hợp nhất                 │
                  │              F_modulated = F_ss2d * G                  │
                  │       F_fuse = Conv1x1(Concat(F_modulated, F_shape))   │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                                              ▼
                  ┌────────────────────────────────────────────────────────┐
                  │               5. Tinh chỉnh FFN (Refinement)           │
                  │             F_ffn = Conv1x1(GELU(Conv3x3(F_fuse)))     │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                                              ▼
                  ┌────────────────────────────────────────────────────────┐
                  │          6. Kết nối tàn dư có trọng số học được        │
                  │             Output = x + gamma * F_ffn (gamma=1e-3)    │
                  └────────────────────────────────────────────────────────┘
```

---

### CHI TIẾT TOÁN HỌC & CÁC LỚP CỐT LÕI

#### 1. Hàm `parallel_associative_scan(a, b)`
- **Nhiệm vụ:** Giải phương trình hồi quy tuyến tính không gian trạng thái:
  $$h_t = a_t \cdot h_{t-1} + b_t$$
- **Cơ chế:** Sử dụng thuật toán quét song song liên kết (Parallel Associative Scan) với độ phức tạp $O(\log L)$ thay vì vòng lặp `for` tuần tự $O(L)$ trong Python.
- **Tính tương thích:** Hoàn toàn khả vi (fully differentiable), tương thích tự động với Automatic Mixed Precision (AMP FP16/BF16).

#### 2. Lớp `SS2D` (2D Selective Scan Module)
- Triển khai cơ chế quét 4 hướng để chuyển đổi ảnh 2D thành chuỗi 1D:
  - **Hướng 0:** Quét theo hàng từ trái qua phải (Raster forward).
  - **Hướng 1:** Quét theo hàng ngược lại (Raster backward).
  - **Hướng 2:** Quét theo cột từ trên xuống dưới (Column-major forward).
  - **Hướng 3:** Quét theo cột ngược lại (Column-major backward).
- Dự phóng tham số liên tục sang rời rạc:
  $$\Delta = 	ext{softplus}(	ext{Linear}(u) + \Delta_{	ext{bias}})$$
  $$ar{A} = \exp(\Delta \cdot A), \quad ar{B} = \Delta \cdot B$$
- Sau khi chạy scan trên cả 4 hướng, các chuỗi ẩn được gập lại thành lưới 2D và hợp nhất qua cổng gating $z$.

#### 3. Lớp `ShapeAwareBranch` & `DirectionalShapeExtractor`
- **Mục đích:** Khắc phục nhược điểm của Mamba (quét theo chuỗi dễ làm mờ ranh giới tần số cao của polyp).
- **Cấu trúc:**
  - Dải tích chập ngang (Horizontal strip kernel $1 	imes 5$): bắt tính liên tục ngang.
  - Dải tích chập dọc (Vertical strip kernel $5 	imes 1$): bắt tính liên tục dọc.
  - Nhân tích chập $3 	imes 3$: đo độ cong bề mặt cục bộ.
- **Độ lớn gradient biên khả vi (Differentiable Boundary Gradient Magnitude):**
  $$|
abla S| = \sqrt{s_h^2 + s_v^2 + \epsilon}$$
  Giúp mô hình phản ứng cực kỳ nhạy với đường viền polyp kể cả khi độ tương phản với niêm mạc rất thấp.

#### 4. Lớp `TopologyShapeGate`
- Sử dụng phép nén kênh (channel reduction $	ext{ratio} = 4$) và kích hoạt Sigmoid để sinh ma trận điều phối $G \in [0, 1]$.
- Ma trận $G$ điều tiết trực tiếp các đặc trưng toàn cục của SS2D: các vùng thuộc về ranh giới hình thái polyp sẽ được khuếch đại, vùng nền nhiễu sẽ bị triệt tiêu.

#### 5. Lớp `TSVMamba` & `C2TSVMamba`
- `TSVMamba`: Đóng gói toàn bộ luồng xử lý trên kèm hệ số tàn dư học được $\gamma$ (khởi tạo nhỏ $\gamma = 10^{-3}$ để đảm bảo ổn định gradient trong những epoch đầu tiên khi chuyển từ pre-trained weights).
- `C2TSVMamba`: Lớp bao ngoài Cross-Stage Partial kế thừa giao diện Ultralytics:
  - Tách kênh đầu vào làm 2 nhánh qua tích chập `cv1`.
  - Một nhánh đi qua chuỗi $n$ khối `TSVMamba`, nhánh còn lại đóng vai trò shortcut.
  - Hợp nhất và chiếu kênh qua tích chập `cv2`.

---

## 3. KẾT QUẢ KIỂM THỬ ĐƠN VỊ (UNIT TEST VERIFICATION)

Script kiểm định độc lập:
`Stracth/verify_tsvm_layer10.py`

Khi thực thi trên tensor giả lập P5 (`shape=[2, 1024, 20, 20]`), kết quả xác nhận:
- **Số lượng tham số của khối Tầng 10:** 12.090.370 tham số (~46.12 MB ở định dạng FP32).
- **Kích thước đầu ra:** Hoàn toàn trùng khớp `[2, 1024, 20, 20]` (Bảo toàn 100% shape).
- **Gradient flow:** Lan truyền ngược (Backward Pass) hoàn hảo, không có hiện tượng NaN/Inf, không bị triệt tiêu gradient (vanishing gradient).
