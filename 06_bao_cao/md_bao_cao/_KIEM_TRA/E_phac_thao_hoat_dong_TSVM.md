# Phác thảo hoạt động của mô hình TSVM (YOLO26s-seg + C2TSVMamba)

Ghi chú tham khảo, soạn ngày 27/10/2026, không phải nội dung chương báo cáo.

**Nguồn:**
- Mã nguồn: `02_ma_nguon/ultralytics_TSVM_FP32/nn/modules/topology_shape_vmamba.py`.
- Cấu hình: `02_ma_nguon/ultralytics_TSVM_FP32/cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml`.
- Kích thước tensor và số tham số: `00_tai_lieu_tong_quan/bang/08_kien_truc_dung_lai.csv`.

Mọi kích thước ghi theo YOLO26s-seg với ảnh đầu vào 640×640.

## 1. TSVM nằm ở đâu trong mô hình

```
Ảnh 3×640×640
   │
   ▼  BACKBONE (giống hệt Baseline từ tầng 0 tới 9)
 tầng 0–3  Conv/C3k2 ............ 128×80×80
 tầng 4    C3k2 ───────────────── 256×80×80  (P3) ──────────────┐
 tầng 5–6  Conv/C3k2 ──────────── 256×40×40  (P4) ────────┐     │
 tầng 7–8  Conv/C3k2 ............ 512×20×20               │     │
 tầng 9    SPPF ................. 512×20×20               │     │
 tầng 10 ★ C2TSVMamba ─────────── 512×20×20  (P5) ──┐     │     │
           (Baseline dùng C2PSA)                    │     │     │
   ▼  HEAD (giống hệt Baseline)                     │     │     │
 tầng 11–13  Upsample + ghép P4 → 256×40×40 ◄───────┘─────┘     │
 tầng 14–16  Upsample + ghép P3 → 128×80×80 ◄───────────────────┘ → nhánh nhỏ
 tầng 17–19  đi xuống + ghép    → 256×40×40                        → nhánh vừa
 tầng 20–22  đi xuống + ghép tầng 10 → 512×20×20                   → nhánh lớn
 tầng 23     Segment26 (P3, P4, P5) → hộp + 32 hệ số mask + prototype
```

Điểm chính:
- Hai mô hình chỉ khác nhau ở tầng 10, trên bản đồ đặc trưng 20×20, tức mỗi ô ứng với một vùng 32×32 pixel của ảnh.
- Đầu ra tầng 10 đi vào head theo hai đường: đi lên qua tầng 11 tới P4 và P3, và nối thẳng vào tầng 21 của nhánh P5. Vì vậy cả ba mức đầu ra đều nhận đặc trưng đã qua TSVM.
- Tham số tầng 10 tăng từ 990.976 (C2PSA) lên 1.811.201 (C2TSVMamba). Toàn mô hình tăng từ 11.434.463 lên 12.254.688.

## 2. Lớp vỏ C2TSVMamba (tách đôi kênh)

```
x: 512×20×20
   │
 cv1 (Conv 1×1, 512→512)
   │
 split ──► a: 256×20×20 ─────────────────────────┐   (nửa này đi thẳng, không qua xử lý)
   │                                             │
   └────► b: 256×20×20 ──► TSVMamba (n = 1) ──► b'
                                                 │
                              concat [a, b'] = 512×20×20
                                                 │
                                   cv2 (Conv 1×1, 512→512)
                                                 │
                                       y: 512×20×20
```

Cách tách kênh này giống C2PSA. Chỉ một nửa số kênh (256) đi qua khối TSVMamba, và có đúng một khối (n = 1).

## 3. Khối TSVMamba: hai nhánh song song, một cổng, một nhánh tắt

```
                          b: 256×20×20
           ┌──────────────────┼───────────────────────────┐
           ▼                                              ▼
 ┌─────────────────────┐                ┌──────────────────────────────────┐
 │ NHÁNH TOÀN CỤC: SS2D│                │ NHÁNH HÌNH DẠNG (cục bộ)         │
 │ quét 4 hướng        │                │ ShapeAwareBranch                 │
 │ (mục 4)             │                │   → DirectionalShapeExtractor    │
 └─────────┬───────────┘                │ (mục 5)                          │
           │ F_M: 256×20×20             └───────────────┬──────────────────┘
           │                                            │ S: 256×20×20
           │                              ┌─────────────┤
           │                              ▼             │
           │                   CỔNG: Conv 1×1 + Sigmoid │
           │                     G ∈ (0, 1), 256×20×20  │
           │                              │             │
           ▼                              │             │
   F_M' = F_M ⊙ (1 + G)  ◄────────────────┘             │
           │                                            │
           └──────────── concat [F_M', S] ◄─────────────┘
                              │ 512×20×20
                       fuse: Conv 1×1 → 256
                              │
                       FFN: Conv 1×1 256→512 (SiLU) → Conv 1×1 512→256
                              │ f_out
                              ▼
                 out = b + γ · f_out      (γ học được, khởi tạo 0,001)
```

Ý nghĩa từng bước:
- Nhánh SS2D nhìn toàn bộ 400 ô (20×20), nên mỗi ô nhận được ngữ cảnh từ khắp ảnh.
- Nhánh hình dạng chỉ nhìn lân cận nhỏ, cỡ 3×3 đến 5×5 ô, để bắt biên, cạnh và độ liên tục ngang/dọc.
- Cổng G lấy giá trị trong (0, 1), nên hệ số `1 + G` nằm trong (1, 2). Cổng chỉ **khuếch đại** F_M tại những vị trí và kênh mà nhánh hình dạng thấy nổi bật, không bao giờ triệt tiêu F_M.
- Sau khi điều biến, S vẫn được ghép thêm vào lần nữa. Như vậy thông tin hình dạng vào kết quả theo hai đường: qua cổng và trực tiếp qua `fuse`.
- Vì γ = 0,001 lúc khởi tạo, ban đầu `out ≈ b` và khối gần như là phép đồng nhất. Mô hình tự học xem nên tăng γ đến đâu, nhờ đó huấn luyện ổn định khi chèn khối mới vào giữa backbone.

## 4. Bên trong SS2D (nhánh VMamba)

```
b: 256×20×20
  │ in_proj (Conv 1×1, 256→512) rồi chia đôi
  ├──► u: 256×20×20 ── DWConv 3×3 + SiLU
  └──► z: 256×20×20 (để làm cổng ở cuối)

u được trải thành 4 chuỗi, mỗi chuỗi dài L = 400:
  hướng 0: theo hàng, trái→phải, trên→dưới      1 2 3 … 400
  hướng 1: theo hàng, đảo ngược                 400 … 3 2 1
  hướng 2: theo cột, trên→dưới, trái→phải       (chuyển vị rồi trải)
  hướng 3: theo cột, đảo ngược

Với MỖI hướng k (tham số riêng cho từng hướng):
  x_proj[k]: tại mỗi vị trí t → (Δ_raw: 16, B_t: 16, C_t: 16)
  Δ_t = softplus(dt_proj[k](Δ_raw))      bước thời gian > 0, riêng mỗi kênh
  A   = −exp(A_logs[k])                  âm; khởi tạo −1, −2, …, −16
  a_t = exp(clamp(Δ_t·A, −50, 0)) ∈ (0, 1]   hệ số "quên"
  b_t = Δ_t · B_t · u_t                       lượng "ghi vào"

  Hồi quy:  h_t = a_t ⊙ h_{t−1} + b_t     (h: 256 kênh × 16 trạng thái)
            y_t = Σ_n C_t[n] · h_t[n]

  → tính bằng parallel_associative_scan: đệm 400 lên 512,
    9 bước nhân đôi (1, 2, 4, …, 256), không có vòng lặp theo từng token.

Gộp: đưa 4 chuỗi y về lại lưới 20×20 → y = y0 + y1 + y2 + y3
     y = y ⊙ SiLU(z)
     out_proj (Conv 1×1, 256→256) → F_M
```

Trực giác:
- Trạng thái h giống một "bộ nhớ" chạy dọc chuỗi.
- Vì Δ, B và C được tính từ chính nội dung tại từng vị trí, mô hình tự quyết ở mỗi ô nên nhớ lâu (Δ nhỏ, a ≈ 1) hay quên nhanh và ghi mạnh thông tin mới (Δ lớn). Đó là phần "chọn lọc" (selective) của Mamba.
- Quét theo một hướng thì mỗi ô chỉ "thấy" các ô đứng trước nó. Gộp 4 hướng thì mỗi ô nhận thông tin từ cả bốn phía, nên vùng cảm nhận phủ toàn bộ 20×20.
- Chi phí tăng tuyến tính theo L, thay vì bình phương như attention trong C2PSA.

## 5. Nhánh hình dạng và hướng

```
b: 256×20×20
  │ ShapeAwareBranch
  ├─ DWConv 3×3 (+BN+SiLU) ─┐
  └─ DWConv 5×5 (+BN+SiLU) ─┴─ concat 512 → Conv 1×1 → S_shape: 256
                                                │
  DirectionalShapeExtractor                     │
  ├─ DWConv 1×5  → s_h   (liên tục theo chiều ngang)
  ├─ DWConv 5×1  → s_v   (liên tục theo chiều dọc)
  ├─ DWConv 3×3  → s_loc (độ cong cục bộ)
  └─ s_grad = sqrt(s_h² + s_v² + 1e-6)   (giống độ lớn gradient biên)
        concat [s_h, s_v, s_loc, s_grad] = 1024 → Conv 1×1 → S_topo: 256
        concat [S_shape, S_topo] = 512 → Conv 1×1 → S: 256
```

Tất cả là tích chập theo từng kênh (depthwise) với kernel nhỏ, nên nhánh này rẻ và chỉ nhìn cục bộ. Hai kernel dải 1×5 và 5×1 kết hợp thành `s_grad` mô phỏng toán tử gradient kiểu Sobel, nhưng trọng số do mô hình tự học.

## 6. Tóm tắt một lượt suy luận

1. Ảnh đi qua backbone như Baseline tới SPPF, cho bản đồ 512×20×20.
2. `cv1` rồi tách đôi: 256 kênh đi thẳng, 256 kênh vào TSVMamba.
3. Trong TSVMamba, SS2D quét 4 hướng để gom ngữ cảnh toàn ảnh (F_M). Song song, nhánh hình dạng tìm biên và cạnh cục bộ (S).
4. S sinh cổng G, khuếch đại F_M tại vùng có cấu trúc biên rõ: `F_M·(1+G)`.
5. Ghép với S, qua `fuse` và FFN, rồi cộng vào đầu vào với hệ số γ nhỏ.
6. Ghép lại với nửa kênh đi thẳng, qua `cv2`, ra 512×20×20.
7. Head FPN/PAN và Segment26 làm việc như Baseline: ra hộp, hệ số mask và prototype, rồi dựng mặt nạ polyp.

Khi huấn luyện, hàm mất mát, bộ dữ liệu và siêu tham số giống hệt Baseline. Không có hàm mất mát riêng nào cho "hình dạng" hay "topology".

## 7. Lưu ý khi viết vào báo cáo

- **Tên gọi khác với chứng minh.** "Topology" và "Shape" là tên đặt theo ý đồ thiết kế. Trong mã chỉ có tích chập theo hướng và một phép tính kiểu độ lớn gradient, không có ràng buộc hay hàm mất mát nào về topology. Repo cũng chưa có chỉ số topology hay ablation để chứng minh lợi ích này.
- **Có sẵn mã ablation nhưng chưa có kết quả.** `TSVMamba` hỗ trợ 4 chế độ: `topology_shape_vmamba` (bản đầy đủ), `vmamba_only`, `shape_only` và `shape_vmamba_no_guidance`. Ngoài ra có notebook `02_ma_nguon/notebook_kaggle/ablation/kvasir-yolo26s-seg-tsvm-ablation.ipynb`. Tuy vậy, kết quả ablation chưa có trong bộ số liệu đã xác minh.
- **Nguồn gốc độ trễ CPU gấp khoảng 2,1 lần (chưa xác minh).** Đây là suy luận từ cấu trúc mã, chưa đo riêng từng phần. Nhiều khả năng do SS2D: với mỗi hướng phải tạo tensor B×256×16×512 và chạy 9 bước `torch.cat` trong phép quét song song, nhân với 4 hướng.
