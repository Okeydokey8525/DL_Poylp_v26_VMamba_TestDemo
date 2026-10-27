# B. Lý thuyết và mô hình: bảng sự thật cho Chương 2 và Chương 3

Người soạn: sub-agent "Chuyên gia mô hình và cơ sở lý thuyết". Ngày 26/10/2026. Chế độ chỉ đọc.

**Quy ước mức xác minh** (ghi cuối mỗi dòng hoặc mỗi mục):

- **[MÃ]**: đọc trực tiếp trong mã nguồn fork `02_ma_nguon/ultralytics_TSVM_FP32/` (đường dẫn rút gọn từ thư mục này).
- **[BẢNG]**: lấy từ `00_tai_lieu_tong_quan/bang/*.csv` (đo bằng cách dựng lại mô hình).
- **[BÀI n]**: đối chiếu với văn bản PDF trong `..\TLTK\` số [n]. Văn bản được trích bằng `pypdf` 6.16.2 (Python hệ thống) ra thư mục tạm. Chỉ tra các đoạn cần thiết, không đọc toàn văn.
- **[HIỂU BIẾT]**: kiến thức chung về bài báo hoặc mã chính thức, **chưa đối chiếu được với PDF hoặc mã trong repo**. Phải kiểm tra lại trước khi viết thành câu khẳng định.
- **[SUY LUẬN]**: tự suy ra hoặc tự ước tính, chưa đo.

Trừ khi ghi khác, mọi kích thước tensor đều cho đầu vào 1×3×640×640, scale `s`, `nc=1`.

---

## 1. Bảng sự thật kiến trúc, công thức và tham số

### 1.1 Vị trí thay đổi trong YOLO26s-seg

| Mục | Giá trị | Nguồn |
|---|---|---|
| YAML đối chứng | `cfg/models/26/yolo26-seg.yaml`. `end2end: True` (dòng 9), `reg_max: 1` (dòng 10), scale `s: [0.50, 0.50, 1024]` (dòng 14) | [MÃ] |
| YAML đề xuất | `yolo26-seg-TopologyShapeVMamba.yaml`. Lệnh `diff` cho thấy **chỉ khác dòng tầng 10**: `[-1, 2, C2TSVMamba, [1024]]` thay `[-1, 2, C2PSA, [1024]]`. Các khác biệt còn lại chỉ nằm ở chú thích | [MÃ] |
| Tầng 10 | Mức P5, stride 32, vào/ra 512×20×20 | [BẢNG] 08 |
| Số khối bên trong | YAML ghi `2`, parser áp dụng `max(round(2·0,5),1)=1` (`nn/tasks.py`, dòng `n = n_ = max(round(n * depth), 1)`). C2TSVMamba nằm trong `repeat_modules` (`nn/tasks.py:2048`) | [MÃ] |
| Kênh | `c2 = make_divisible(min(1024,1024)·0,5, 8) = 512` (`nn/tasks.py:2071`). Kênh ẩn `c = int(512·0,5) = 256` | [MÃ], [BẢNG] |
| Đầu ra tầng 10 đi tới | Tầng 11 (Upsample lên P4) và tầng 21 (Concat với tầng 20 để tạo P5 của head) | [MÃ] YAML dòng 36, 49 |
| Tham số toàn mô hình | Baseline 11.434.463; TSVM 12.254.688; chênh lệch +820.225 (+7,17%), nằm hết ở tầng 10 | [BẢNG] 08 |

**Phát hiện cần nêu ở Chương 3:** tầng 22 của **cả hai mô hình** là `C3k2` với tham số YAML `[1024, True, 0.5, True]`, nghĩa là `c3k=True, e=0.5, attn=True`. Khi `attn=True`, mỗi khối con là `Sequential(Bottleneck, PSABlock)` (`nn/modules/block.py:1103-1107`). Vì vậy TSVM chỉ bỏ attention ở tầng 10. **Neck vẫn còn một PSABlock ở tầng 22 (P5 của head).** Bài YOLO26 cũng vẽ khối này là "C3k2 1024, e=0.5, attn=True" (Hình S1) [BÀI 12]. Báo cáo không được viết rằng "mô hình đề xuất thay toàn bộ attention bằng Mamba". [MÃ]

### 1.2 Các khối nền của YOLO26s-seg (để viết mục 2.x và 3.1)

| Khối | Cài đặt trong mã | Dòng |
|---|---|---|
| `Conv` | Conv2d (không bias) → BatchNorm2d → SiLU (`default_act = nn.SiLU()`). `initialize_weights` đặt BN `eps=1e-3`, `momentum=0.03` | `nn/modules/conv.py` (class Conv); `utils/torch_utils.py:563-573` |
| `C2f` / `C3k2` | `cv1` 1×1 → tách đôi → chuỗi khối con, mỗi khối nhận đầu ra khối trước → ghép tất cả → `cv2` 1×1. Khối con có ba loại: `Bottleneck`, `C3k` (khi `c3k=True`) hoặc `Bottleneck+PSABlock` (khi `attn=True`) | `block.py:294-319`, `1075-1112` |
| `SPPF` | `cv1` 1×1 (không kích hoạt) rồi 3 lần MaxPool 5×5 nối tiếp, ghép 4 nhánh, `cv2` 1×1. YAML truyền `shortcut=True` và c1=c2, nên **có cộng tắt** `y + x` | `block.py:214-244`; YAML dòng 31 `[1024, 5, 3, True]` |
| `Attention` | `qkv` Conv1×1 (không kích hoạt), `num_heads = c//64 = 4`, `head_dim = 64`, `key_dim = 32`, softmax(QᵀK/√32), cộng mã hóa vị trí `pe` (depthwise 3×3 trên V), rồi `proj` | `block.py:1277-1339` |
| `PSABlock` | `x ← x + Attn(x)`; `x ← x + FFN(x)`, trong đó FFN = Conv1×1 c→2c (SiLU) → Conv1×1 2c→c (không kích hoạt) | `block.py:1342-1384` |
| `C2PSA` | `cv1` → tách (a, b) → `b ← PSABlock^n(b)` → `cv2(concat(a,b))` | `block.py:1447-1499` |
| `Segment26` | Kế thừa `Segment`/`Detect`. Có hai bộ đầu: one2many (`cv2, cv3, cv4`) và one2one (bản `deepcopy`). Prototype dùng `Proto26` | `nn/modules/head.py:37-443` |
| `Proto26` | Cộng P3 với P4, P5 sau khi chiếu 1×1 về 128 kênh và upsample nearest; Conv 3×3 lên 256; `Proto` (Conv3×3 → ConvTranspose ×2 → Conv3×3 → Conv1×1 → 32 prototype); nhánh `semseg` **chỉ chạy khi `self.training`** và bị xóa khi `fuse()` | `block.py:88-107`, `1991-2024` |

Tham số C2PSA tầng 10 do tôi tự tính lại theo mã, khớp [BẢNG]: `cv1+cv2` = 2×(512·512+1024) = 526.336; qkv = 256·512+1024 = 132.096; proj = 66.048; pe = 2.816; ffn = 263.680. Tổng = **990.976**. ✔

Đầu Detect (scale s, nc=1): `c2 = max(16, 128/4, 4) = 32` kênh cho nhánh hộp; `c3 = max(128, 1) = 128` kênh cho nhánh lớp; `c4 = max(128/4, 32) = 32` cho hệ số mặt nạ. Số anchor = 80² + 40² + 20² = **8.400**. Prototype 32×160×160. [MÃ] `head.py:116-129`, `333-335`; [SUY LUẬN] số học.

### 1.3 Luồng tensor qua C2TSVMamba (B = 1)

| Bước | Phép toán | Kích thước ra | Mã |
|---|---|---|---|
| vào | x | 512×20×20 | |
| `cv1` | Conv1×1 512→512 + BN + SiLU | 512×20×20 | `topology_shape_vmamba.py:476, 500` |
| split | a, b | 256×20×20 mỗi nhánh | `:500` |
| **SS2D** `in_proj` | Conv2d 1×1 256→512, không bias | 512×20×20 → u, z: 256×20×20 | `:101, 144-145` |
| `conv2d` + SiLU | depthwise 3×3, không bias | u: 256×20×20 | `:104-111, 148` |
| cross-scan | 4 chuỗi: hàng xuôi, hàng ngược (flip), cột xuôi (transpose), cột ngược | 4 × (256×400) | `:151-158` |
| `x_proj[k]` | Linear 256 → 16+16+16, không bias | 400×48 → Δ_raw 400×16, B 400×16, C 400×16 | `:117, 168-169` |
| `dt_projs[k]` + softplus | Linear 16→256, có bias | Δ: 256×400 | `:120-122, 171-172` |
| rời rạc hóa | A = −exp(A_log[k]) (256×16); ΔA clamp [−50, 0]; Ā = exp(ΔA) | Ā, ΔBu: 256×16×400 | `:179-187` |
| quét | `parallel_associative_scan`, đệm L lên 512 | h: 256×16×400 | `:20-55, 190` |
| đọc ra | y_k = Σ_n C_n h_n (einsum) | 256×400 | `:193` |
| cross-merge | đảo flip/transpose về lưới, **cộng** 4 hướng | 256×20×20 | `:197-203` |
| cổng z | Y ⊙ SiLU(z) | 256×20×20 | `:206` |
| `out_proj` | Conv2d 1×1 256→256, không bias | F_M: 256×20×20 | `:129, 209` |
| **ShapeAwareBranch** | dw3×3 ‖ dw5×5 (Conv+BN+SiLU), ghép 512, Conv1×1 → 256 | S_shape: 256×20×20 | `:213-243` |
| **DirectionalShapeExtractor** | dw 1×5, dw 5×1, dw 3×3; S_grad; ghép 1024 → `topo_fuse` 256; ghép với S_shape 512 → `unify` 256 | S: 256×20×20 | `:246-293` |
| **TopologyShapeGate** | Conv2d 1×1 có bias → Sigmoid | G: 256×20×20, giá trị trong (0, 1) | `:296-323` |
| điều biến | F_M′ = F_M ⊙ (1 + G) | 256×20×20 | `:407` |
| `fuse` | concat[F_M′, S] 512 → Conv1×1 + BN + SiLU → 256 | 256×20×20 | `:378, 409` |
| `ffn` | Conv1×1 256→512 (SiLU) → Conv1×1 512→256 (BN, không kích hoạt) | 256×20×20 | `:381-384, 411` |
| residual | b′ = b + γ · F | 256×20×20 | `:387, 413` |
| `cv2` | concat(a, b′) 512 → Conv1×1 512→512 + BN + SiLU | 512×20×20 | `:477, 502` |

Ghi chú mã [MÃ]:
- `self.act = nn.SiLU()` khai báo ở `:112` nhưng **không dùng**; forward gọi `F.silu`. Không ảnh hưởng kết quả.
- Mỗi hướng có `x_proj`, `dt_projs` và `A_logs` riêng (`A_logs` có kích thước 4×256×16).
- B và C dùng chung cho mọi kênh d tại mỗi vị trí (kích thước N). Δ có giá trị riêng cho từng kênh, sinh qua phép chiếu hạng thấp (dt_rank = 16).

### 1.4 Công thức của từng nhánh (dùng trong Chương 3)

Ký hiệu: $\mathcal{C}^{k\times k}_{g}$ là Conv (k×k, nhóm g) + BN + SiLU; $\mathcal{C}^{1\times1}$ là Conv 1×1 + BN + SiLU; $\sigma$ là sigmoid; $\odot$ là nhân từng phần tử; $[\cdot\,\|\,\cdot]$ là ghép kênh.

**Khung C2 (wrapper):**
$$[a,\;b] = \mathrm{split}\big(\mathcal{C}^{1\times1}_{\text{cv1}}(x)\big),\qquad y = \mathcal{C}^{1\times1}_{\text{cv2}}\big([a \,\|\, \mathrm{TSVM}(b)]\big)$$

**SS2D:**
$$[U, Z] = W_{\text{in}} * b,\qquad \tilde U = \mathrm{SiLU}\big(\mathrm{DWConv}_{3\times3}(U)\big)$$
Với hướng $k \in \{0,1,2,3\}$, gọi $\Pi_k$ là phép sắp lưới H×W thành chuỗi L = HW: hàng xuôi, hàng ngược, cột xuôi, cột ngược. Đặt $u^{(k)} = \Pi_k(\tilde U) \in \mathbb{R}^{L\times D}$. Khi đó:
$$\Delta^{(k)}_t = \mathrm{softplus}\big(W^{(k)}_{\Delta}\,W^{(k)}_{x,\Delta}\,u^{(k)}_t + b^{(k)}_{\Delta}\big)\in\mathbb{R}^{D},\quad B^{(k)}_t = W^{(k)}_{x,B}\,u^{(k)}_t\in\mathbb{R}^{N},\quad C^{(k)}_t = W^{(k)}_{x,C}\,u^{(k)}_t\in\mathbb{R}^{N}$$
$$A^{(k)} = -\exp\big(A^{(k)}_{\log}\big)\in\mathbb{R}^{D\times N},\qquad \bar A^{(k)}_{t,d,n} = \exp\Big(\mathrm{clip}\big(\Delta^{(k)}_{t,d}A^{(k)}_{d,n},\,-50,\,0\big)\Big)$$
$$h^{(k)}_{t,d,n} = \bar A^{(k)}_{t,d,n}\,h^{(k)}_{t-1,d,n} + \Delta^{(k)}_{t,d}\,B^{(k)}_{t,n}\,u^{(k)}_{t,d},\qquad h^{(k)}_{0}=0$$
$$y^{(k)}_{t,d} = \sum_{n=1}^{N} C^{(k)}_{t,n}\,h^{(k)}_{t,d,n}$$
$$F_M = W_{\text{out}} * \Big(\big(\textstyle\sum_{k=0}^{3}\Pi_k^{-1}(y^{(k)})\big)\odot \mathrm{SiLU}(Z)\Big)$$
D = 256, N = 16, L = 400. Không có hạng tử $D\cdot u$ (skip). [MÃ]

**Nhánh hình dạng:**
$$S_{\text{shape}} = \mathcal{C}^{1\times1}\big([\mathcal{C}^{3\times3}_{dw}(b)\,\|\,\mathcal{C}^{5\times5}_{dw}(b)]\big)$$
$$S_h=\mathcal{C}^{1\times5}_{dw}(S_{\text{shape}}),\quad S_v=\mathcal{C}^{5\times1}_{dw}(S_{\text{shape}}),\quad S_{loc}=\mathcal{C}^{3\times3}_{dw}(S_{\text{shape}}),\quad S_{grad}=\sqrt{S_h^2+S_v^2+10^{-6}}$$
$$S_{topo} = \mathcal{C}^{1\times1}\big([S_h\|S_v\|S_{loc}\|S_{grad}]\big),\qquad S = \mathcal{C}^{1\times1}\big([S_{\text{shape}}\|S_{topo}]\big)$$
Lưu ý: S_h và S_v đã đi qua BN và SiLU, nên S_grad **không phải** gradient không gian kiểu Sobel. Nó là "độ lớn" của hai đáp ứng học được. [MÃ]

**Cổng, hợp nhất và residual:**
$$G = \sigma(W_g * S + b_g)\in(0,1)^{C\times H\times W},\qquad F'_M = F_M\odot(1+G)$$
$$F = \mathrm{FFN}\big(\mathcal{C}^{1\times1}_{\text{fuse}}([F'_M\|S])\big),\quad \mathrm{FFN}(v)=\mathrm{BN}\big(W_2*\mathcal{C}^{1\times1}(v)\big),\qquad \mathrm{TSVM}(b) = b + \gamma\,F,\ \ \gamma_0 = 10^{-3}$$
Hệ số nhân $(1+G)$ nằm trong khoảng mở (1, 2): cổng chỉ **khuếch đại** F_M, không làm giảm F_M xuống dưới giá trị gốc. γ là **một vô hướng** dùng chung cho mọi kênh, khác LayerScale (vector theo kênh). [MÃ] cho công thức; [HIỂU BIẾT] cho phần so sánh với LayerScale.

### 1.5 Tham số từng phần (tầng 10, scale s)

| Thành phần | Tham số | Tự tính lại theo mã | Nguồn |
|---|---:|---|---|
| SS2D | 281.856 | in_proj 131.072 + conv 2.304 + x_proj 4·12.288 = 49.152 + dt_proj 4·(4.096+256) = 17.408 + A_logs 16.384 + out_proj 65.536 | [BẢNG] ✔ |
| ShapeAwareBranch | 141.312 | 2.816 + 6.912 + 131.584 | [BẢNG] ✔ |
| DirectionalShapeExtractor | 400.640 | 1.792 + 1.792 + 2.816 + 262.656 + 131.584 | [BẢNG] ✔ |
| TopologyShapeGate | 65.792 | 256·256 + 256 | [BẢNG] ✔ |
| fuse | 131.584 | 512·256 + 512 | [BẢNG] ✔ |
| FFN | 263.680 | (256·512 + 1.024) + (512·256 + 512) | [BẢNG] ✔ |
| γ | 1 | | [BẢNG] |
| cv1 + cv2 | 526.336 | | [BẢNG] ✔ |
| **Tổng** | **1.811.201** | | [BẢNG] |
| C2PSA (đối chứng) | 990.976 | xem mục 1.2 | [BẢNG] ✔ |

Tham số theo từng chế độ ablation, **tính bằng cách cộng/trừ thành phần, chưa dựng mô hình để đo** [SUY LUẬN]:

| Chế độ | Thành phần có | Tham số tầng 10 (ước tính) |
|---|---|---:|
| `topology_shape_vmamba` (đầy đủ) | SS2D, Shape, Directional, Gate, fuse, FFN, γ | 1.811.201 |
| `shape_vmamba_no_guidance` | như trên nhưng bỏ Gate | 1.745.409 |
| `shape_only` | Shape, Directional, FFN, γ (không fuse) | 1.331.969 |
| `vmamba_only` | SS2D, FFN, γ (không fuse) | 1.071.873 |

Các mức tham số này khác nhau nhiều. Nếu chạy ablation thì nên thêm một đối chứng có số tham số tương đương. [SUY LUẬN]

### 1.6 Độ phức tạp (L = 400, D = 256, N = 16)

**Quét song song** [MÃ] `:33-55`:
- `num_steps = (L−1).bit_length() = 9`; chuỗi được đệm lên 512 với phần tử đơn vị (a = 1, b = 0), nên kết quả ở L vị trí đầu không đổi.
- Mỗi bước dùng toán tử kết hợp $(a_1,b_1)\circ(a_2,b_2)=(a_2a_1,\ a_2b_1+b_2)$ với độ lệch 1, 2, 4, …, 256.
- Đây là kiểu quét **Hillis–Steele/Kogge–Stone**: độ sâu ⌈log₂L⌉ = 9 bước, **tổng công việc O(L log L)**. Nó không phải kiểu work-efficient của Blelloch (công việc O(L), độ sâu 2 log L). [MÃ] cho cơ chế; [HIỂU BIẾT] cho tên thuật toán.
- Mamba nêu rằng họ dùng **work-efficient parallel scan** (dẫn Blelloch 1990), cùng kernel fusion và recomputation [BÀI 14, mục 3.3.2]. Mã của đề tài không dùng ba kỹ thuật này.

**Ước tính số phép toán cho một ảnh** [SUY LUẬN, chưa đo bằng profiler]:

| Phần | MAC (triệu) |
|---|---:|
| SS2D: in_proj 52,4; dwconv 0,9; x_proj 19,7; dt_proj 6,6; đọc ra C·h 6,6; out_proj 26,2 | ≈ 112 |
| SS2D: phép quét (khoảng 3 phép tính trên mỗi phần tử × Σ(512−step) × 4.096 × 4 hướng) | ≈ 200 triệu phép toán từng phần tử (quét tuần tự chỉ cần khoảng 52 triệu) |
| Nhánh hình dạng + Directional + Gate + fuse + FFN | ≈ 399 |
| **TSVMamba (không tính cv1/cv2)** | ≈ 511 MAC + khoảng 0,2 G phép toán từng phần tử |
| PSABlock của C2PSA: qkv 52,4; QKᵀ 20,5; AV 41,0; proj 26,2; pe 0,9; ffn 104,9 | ≈ 246 |
| cv1 + cv2 (chung cho cả hai) | ≈ 210 |

Nhận xét [SUY LUẬN]:
- Ở L = 400, attention O(L²) của C2PSA vẫn rẻ. Lợi thế "tuyến tính theo L" của SSM **không thể hiện được** ở P5.
- Độ trễ CPU đo được tăng khoảng 2,14 lần (forward 269,6 → 577,4 ms; nguồn `09_HIEU_NANG_TINH_TOAN.md`). Mức tăng này khớp với các nguồn chi phí trên cộng chi phí bộ nhớ của nhiều phép `torch.cat` trong vòng quét. Chưa có profiler để tách phần nào gây chậm nhất.
- Bộ nhớ autograd của phép quét tỉ lệ với O(B·D·N·L·log L) cho mỗi hướng, vì mỗi bước tạo tensor mới.
- Nếu đặt module ở P4 (L = 1.600) hoặc P3 (L = 6.400), số bước quét tăng lên 11 và 13, còn khối lượng mỗi bước tăng 4 và 16 lần.

### 1.7 Khởi tạo

| Mục | Nội dung | Nguồn |
|---|---|---|
| γ | `torch.full((1,), 0.001)`. Lúc bắt đầu, TSVM(b) ≈ b, nên tầng 10 ≈ `cv2(concat(a, b))` | [MÃ] `:387` |
| A_log | `log(1..16)` lặp cho 256 kênh và 4 hướng, nên A = −[1, …, 16]. Đây là cách khởi tạo S4D-Real mà Mamba dùng | [MÃ] `:125-126`; [BÀI 14] (mục S4D-Real dòng ~412) |
| dt_proj | Khởi tạo mặc định của `nn.Linear`. **Không** khởi tạo bias theo nghịch đảo softplus để Δ ∈ [0,001; 0,1] như Mamba | [MÃ]; [BÀI 14] dòng ~422 nêu Uniform([0,001; 0,1]) |
| Conv/BN | Mặc định PyTorch; BN eps 1e-3, momentum 0,03 (`initialize_weights`) | [MÃ] |
| Nạp pretrained | `YOLO(yaml).load("yolo26s-seg.pt")` dùng `intersect_dicts` (cùng tên và cùng shape) | [MÃ] `utils/torch_utils.py:614-625`; notebook |
| Phần nhận trọng số C2PSA | 12/58 tensor tham số, **790.016/1.811.201** tham số: `cv1`, `cv2`, `m.0.ffn` (FFN của PSABlock có cùng tên và shape) | [BẢNG] 08 |
| Phần khởi tạo ngẫu nhiên | 1.021.185 tham số: SS2D, Shape, Directional, Gate, fuse, γ | [BẢNG] 08 / tài liệu 04 |

Ghi chú [SUY LUẬN]: `m.0.ffn` nhận trọng số FFN của PSA nhưng đầu vào của nó đã khác (đầu ra `fuse` thay cho đầu ra attention). Nên viết đây là "khởi tạo kế thừa theo trùng tên", không phải "tái sử dụng có chủ đích".

### 1.8 Bốn chế độ ablation có trong mã

| mode | forward | Mã |
|---|---|---|
| `topology_shape_vmamba` | đầy đủ (mục 1.4) | `:398-413` |
| `vmamba_only` | b + γ·FFN(SS2D(b)) | `:415-418` |
| `shape_only` | b + γ·FFN(Directional(Shape(b))) | `:420-424` |
| `shape_vmamba_no_guidance` | b + γ·FFN(fuse([SS2D(b) ‖ S])) | `:426-432` |

- Cả 40 lượt chính đều dùng chế độ đầy đủ, vì YAML chỉ truyền `[1024]` nên `mode` lấy giá trị mặc định.
- Muốn đổi chế độ thì viết YAML dạng `[1024, 0.5, 16, 3, "vmamba_only"]`. Parser sẽ giữ chuỗi vì `ast.literal_eval` lỗi và bị bỏ qua (`nn/tasks.py`, vòng `for j, a in enumerate(args)`). [MÃ]
- **Chưa có thực nghiệm ablation nào.**

### 1.9 Hàm mất mát YOLO26-seg (đúng nhánh mã đã chạy)

`SegmentationModel.init_criterion` trả về `E2ELoss(self, v8SegmentationLoss)` vì `end2end=True` (`nn/tasks.py:661-663`). [MÃ]

**(a) Hai nhánh và Progressive Loss** (`utils/loss.py:1293-1325`; cập nhật mỗi epoch ở `engine/trainer.py:588-589`):
$$\mathcal{L} = \alpha(e)\,\mathcal{L}_{\text{o2m}} + \big(1-\alpha(e)\big)\,\mathcal{L}_{\text{o2o}},\qquad \alpha(e)=\max\!\Big(1-\tfrac{e}{\max(E-1,1)},0\Big)(0{,}8-0{,}1)+0{,}1$$
- Với E = 100, α giảm tuyến tính từ 0,8 về 0,1.
- Nhánh one2one nhận đặc trưng đã `detach()` khi huấn luyện (`head.py:176`), nên gradient của one2one không chảy ngược về backbone.
- **Các cột loss ghi trong `results.csv` là loss của nhánh one2one** (`return ..., loss_one2one[1]`).
- Bài YOLO26 mô tả đúng như vậy: (0,8; 0,2) → (0,1; 0,9), cập nhật mỗi epoch [BÀI 12, mục 3.3.2 và 4.1].

**(b) Gán nhãn TAL + STAL** (`loss.py:364-371`, `utils/tal.py`):
- Độ đo căn chỉnh $t = s^{\alpha}\cdot u^{\beta}$, với s là điểm lớp dự đoán, u là IoU hộp; **α = 0,5, β = 6,0** (`tal.py:200`).
- o2m: topk = 10. o2o: topk = 7 rồi topk2 = 1 (mỗi GT một anchor).
- Ứng viên là các tâm anchor nằm trong hộp GT. STAL: nếu w hoặc h < stride nhỏ nhất (8) thì khi **chọn ứng viên** cạnh đó được thay bằng 16 (`tal.py:300-306`).
- Nhãn mềm: target_scores được chuẩn hóa theo align_metric và IoU.
- [BÀI 12] mô tả STAL với s_ref = 16, khớp mã.

**(c) Thành phần loss** (`loss.py:402-560`). Hệ số mặc định trong `cfg/default.yaml`: box 7,5; cls 0,5; dfl 1,5.

| Cột log | Công thức trong mã | Hệ số |
|---|---|---|
| `box_loss` | $\sum_{fg} w_i\,(1-\mathrm{CIoU}_i)/\sum t$, với w là tổng target_score | ×7,5 (`hyp.box`) |
| `l1_loss` | Thay DFL khi `reg_max=1`. L1 trên khoảng cách ltrb **đã nhân stride và chia kích thước ảnh**, có trọng số w (`loss.py:141-155`) | ×1,5 (`hyp.dfl`) |
| `cls_loss` | BCE với nhãn mềm từ TAL, chia Σ target_scores | ×0,5 |
| `seg_loss` | Mặt nạ $\hat M_i = c_i^\top P$ (32 prototype); BCE theo pixel, **cắt trong hộp GT**, lấy trung bình rồi chia diện tích hộp chuẩn hóa, cộng lại và chia số anchor dương (`:564-648`) | ×7,5 (**dùng `hyp.box`**) |
| `sem_loss` | Nhánh `semseg` của Proto26: 0,5·BCE + 0,5·Dice (smooth 1) trên mặt nạ ngữ nghĩa gộp từ instance (`:530-552`, `:294-315`) | ×7,5 (`hyp.box`) |

Tổng loss được nhân với batch size. Không có DFL vì `reg_max=1` nên `dfl_loss = None` (`loss.py:116`). [MÃ]

**Giải thích `val/sem_loss = 0`** [MÃ]: `Proto26.forward` chỉ trả `(p, semantic)` khi `self.training` (`block.py:2017-2019`). Lúc validate, model ở chế độ eval nên `pred_semantic = None` và `loss[4]` giữ bằng 0. Ví dụ seed 0 TSVM: train/sem_loss epoch 1 = 2,436; epoch 100 = 0,257; val/sem_loss luôn bằng 0. Bài YOLO26 cũng nói nhánh này chỉ dùng khi huấn luyện [BÀI 12, mục 3.4.1].

**Bộ tối ưu:** bài YOLO26 dùng MuSGD [BÀI 12], nhưng 40 lượt của đề tài đặt `optimizer=AdamW` (`args.yaml`). Chương 2 cần nói rõ điểm khác này.

### 1.10 Suy luận NMS-free

- `Detect.postprocess` lấy top-k (k = `max_det` = 300) theo điểm lớp trên đầu one2one (`head.py:232-275`).
- `non_max_suppression(..., end2end=True)` chỉ lọc theo `conf_thres` và **bỏ qua NMS** (`utils/nms.py:66-75`).
- Khi validate, `conf` mặc định là 0,001 (`engine/validator.py:139`). Tham số `iou=0.7` trong `args.yaml` **không được dùng** trong nhánh end2end. Tài liệu 05 liệt kê "iou 0,7" như một tham số đánh giá; nên chú thích là không áp dụng.
- Mặt nạ cho ảnh đầu ra: `process_mask` nhân hệ số với prototype, upsample bilinear lên kích thước ảnh, nhị phân bằng **logit > 0** (tương đương sigmoid > 0,5), rồi cắt theo hộp (`utils/ops.py:520-541`). [MÃ]

### 1.11 Độ đo của Ultralytics và cách chọn best.pt

| Mục | Cài đặt | Dòng |
|---|---|---|
| Mask IoU | $\mathrm{IoU}=\frac{|M_1\cap M_2|}{|M_1|+|M_2|-|M_1\cap M_2|}$, tính trên mặt nạ phẳng | `utils/metrics.py:174-189` |
| Độ phân giải so mặt nạ khi validate | **imgsz/4 = 160×160** trong không gian letterbox (vì `process_mask`, không bật save_json) | `models/yolo/segment/val.py:74, 128` |
| Ngưỡng IoU | `linspace(0.5, 0.95, 10)` | `models/yolo/detect/val.py:60` |
| Ghép dự đoán–GT | **Tham lam** theo IoU giảm dần, mỗi GT và mỗi dự đoán dùng một lần, làm riêng cho từng ngưỡng (mặc định `use_scipy=False`, không dùng Hungarian) | `engine/validator.py:318-355` |
| AP | Bao lồi precision (lấy max lũy tiến từ phải sang), **nội suy 101 điểm** recall ∈ {0; 0,01; …; 1}, tích phân bằng **hình thang** (`np.trapezoid`) | `metrics.py:760-789` |
| mAP50, mAP50-95 | AP tại IoU 0,5; trung bình AP trên 10 ngưỡng. Một lớp nên mAP = AP | `metrics.py:792-887` |
| P, R (trong results.csv) | Lấy **tại ngưỡng confidence làm F1 trung bình lớn nhất** (đường F1 được làm mượt, hệ số 0,1). Không phải tại conf 0,25 | `metrics.py:883-884` |
| F1 | $2PR/(P+R)$ tại cùng điểm đó. Không ghi trong results.csv nhưng tính lại được từ P và R | `metrics.py:879` |
| fitness | `Metric.fitness` dùng trọng số [0, 0, 0, 1] × [P, R, mAP50, mAP50-95]. `SegmentMetrics.fitness = seg.fitness() + box.fitness()`, tức **mask mAP50-95 + box mAP50-95** | `metrics.py:1007-1009, 1369-1371, 1206` |
| best.pt | Lưu khi `best_fitness == fitness` của epoch (trọng số EMA) | `engine/trainer.py:766, 872-873` |

Hệ quả cho báo cáo:
- Endpoint chính của đề tài là max mask mAP50-95 theo từng lượt, **khác tiêu chí chọn best.pt** (box + mask). Word cũ ghi 16/40 lượt có hai epoch này khác nhau; tôi chưa tự kiểm lại số 16.
- mAP lúc huấn luyện được tính trên mặt nạ 160×160, không phải độ phân giải gốc.

### 1.12 Bản vá FP32 (đã đọc mã sau vá)

| Vị trí | Sau vá | Dòng |
|---|---|---|
| `BaseTrainer.save_model` | `deepcopy(ema).float()`; nếu có tensor không hữu hạn thì `raise FloatingPointError` (bỏ cơ chế chép đè bằng model và `nan_to_num_`) | `engine/trainer.py:712-731` |
| `MultiTrainer` | `deepcopy(self.model).float()` cho `multitrain_base.pt` | `engine/trainer.py:1235` |
| `strip_optimizer` | `x["model"].float()` và kiểm tra NaN/Inf | `utils/torch_utils.py:828-835` |
| Không đổi | `convert_optimizer_state_dict_to_fp16` vẫn nén trạng thái optimizer trong last.pt | `trainer.py:741` |

Nguyên nhân [tài liệu 05, PATCH_FP32.md]: `running_mean` của `model.10.m.0.fuse.bn` (seed 5) ≈ 1,5×10⁶, vượt ngưỡng 65.504 của FP16.

Giải thích cơ chế [SUY LUẬN]: SS2D trong mã **không có LayerNorm đầu ra**, và F_M còn được nhân thêm hệ số (1+G) ≤ 2 trước khi vào `fuse`. Biên độ đặc trưng trước BN của `fuse` vì vậy không bị chặn. Đây là giả thuyết hợp lý, chưa có số đo phân bố kích hoạt để chứng minh.

---

## 2. Dàn ý Chương 2: Cơ sở lý thuyết

Nguyên tắc chung: trình bày bằng lời của mình, dùng công thức chuẩn và trích dẫn. Mỗi mục kết thúc bằng một đoạn ngắn "liên hệ với đề tài" dẫn sang Chương 3.

### 2.1 Bài toán phân đoạn ảnh y khoa và phân đoạn polyp

- **Cốt lõi:**
  - Phân đoạn ngữ nghĩa gán lớp cho từng pixel. Phân đoạn thực thể còn tách từng đối tượng, cho ra hộp, điểm tin cậy và mặt nạ riêng cho mỗi đối tượng. Ở BG20, một ảnh có thể có nhiều polyp (127 đối tượng trên 120 ảnh validation có polyp), nên dạng thực thể là cách đặt bài toán tự nhiên.
  - Polyp khó phân đoạn vì biên mờ, phản quang, kích thước thay đổi nhiều và ảnh nền dễ gây báo nhầm.
  - Nêu ảnh rỗng (ảnh nền) là mẫu hợp lệ của bài toán.
- **Công thức:** đầu ra thực thể $\{(b_i, s_i, c_i, M_i)\}_{i=1}^{K}$; phân đoạn ngữ nghĩa $f: \mathbb{R}^{H\times W\times3}\to\{0,1\}^{H\times W}$.
- **Trích:**
  - [4] survey polyp; [1] Kvasir-SEG; [2], [3] bộ dữ liệu.
  - CẦN BỔ SUNG: Long et al., "Fully Convolutional Networks for Semantic Segmentation" (CVPR 2015).
  - CẦN BỔ SUNG: He et al., "Mask R-CNN" (ICCV 2017).

### 2.2 Mạng tích chập, kiến trúc mã hóa–giải mã và kim tự tháp đặc trưng

- **Cốt lõi:**
  - Tích chập chia sẻ trọng số giữa các vị trí và có trường tiếp nhận cục bộ, mở rộng dần khi xếp nhiều tầng hoặc giảm độ phân giải.
  - Tích chập depthwise và 1×1 (tách lọc không gian và trộn kênh) là nền của nhánh hình dạng TSVM.
  - BatchNorm và SiLU là thành phần của khối `Conv` trong YOLO.
  - U-Net có skip connection; UNet++.
  - FPN có đường từ trên xuống kèm kết nối ngang; PAN thêm đường từ dưới lên. Neck YOLO26 làm cả hai chiều (tầng 11–22).
  - CSP/C2f/C3k2: tách kênh để giảm tính toán và tăng luồng gradient.
  - SPPF: max-pool nối tiếp để mở rộng trường tiếp nhận.
- **Công thức:**
  - $y = W * x$.
  - Depthwise: $y_c = w_c * x_c$; số tham số $k^2C$ so với $k^2C_{in}C_{out}$.
  - BN: $\hat x = \gamma\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}+\beta$, với running mean/var cập nhật theo momentum. Mục này nối sang sự cố FP16.
  - SiLU: $x\,\sigma(x)$.
  - FPN: $P_l = \mathrm{Conv}(C_l) + \mathrm{Up}(P_{l+1})$.
- **Trích:**
  - [5] U-Net, [6] UNet++, [23] FPN, [24] EfficientDet (BiFPN), [7] PraNet (đối chứng).
  - CẦN BỔ SUNG: Ioffe & Szegedy, "Batch Normalization" (ICML 2015).
  - CẦN BỔ SUNG: Elfwing et al., "Sigmoid-Weighted Linear Units" (2018) hoặc Ramachandran et al., "Searching for Activation Functions" (2017).
  - CẦN BỔ SUNG: Howard et al., "MobileNets" (2017) hoặc Chollet, "Xception" (CVPR 2017), cho depthwise.
  - CẦN BỔ SUNG: Liu et al., "Path Aggregation Network" (CVPR 2018).
  - CẦN BỔ SUNG: Wang et al., "CSPNet" (CVPRW 2020).
  - CẦN BỔ SUNG: He et al., "Spatial Pyramid Pooling" (TPAMI 2015).
  - YOLOv4 (Word cũ [10]) có thể dùng cho mosaic/CSP.

### 2.3 Họ YOLO đến YOLO26-seg

- **Cốt lõi:**
  - YOLO gốc coi phát hiện là bài toán hồi quy một giai đoạn trên lưới [11].
  - Các phiên bản sau dùng anchor-free, gán nhãn động (TAL) và DFL.
  - YOLOv10 đưa ra đầu đôi với gán nhãn nhất quán, cho phép suy luận không NMS.
  - **YOLO26 (đã kiểm trong mã):**
    - (i) Đầu đôi one2many (topk = 10, chỉ dùng khi huấn luyện) và one2one (topk = 7 → topk2 = 1). Suy luận lấy top-300 trên nhánh one2one, **không NMS** (`end2end: True`).
    - (ii) **Bỏ DFL** (`reg_max: 1`); hồi quy trực tiếp 4 khoảng cách, giám sát bằng CIoU + L1.
    - (iii) Progressive Loss (0,8 → 0,1).
    - (iv) STAL cho vật nhỏ.
    - (v) MuSGD. Đề tài **không dùng**, mà dùng AdamW.
  - Đầu Segment26 theo hướng prototype (kiểu YOLACT): mỗi ảnh có 32 prototype dùng chung; mỗi đối tượng có 32 hệ số. Proto26 trộn đa mức P3–P5, có nhánh semantic phụ trợ chỉ dùng khi huấn luyện.
- **Công thức:**
  - Mặt nạ: $\hat M_i = \sigma\big(\sum_{k=1}^{32} c_{ik}P_k\big)$, nhị phân tại 0,5, cắt theo hộp.
  - Proto26: $F = X_3 + \sum_{l\in\{4,5\}} \mathrm{Up}(\phi_l(X_l))$.
  - TAL: $t = s^{\alpha}u^{\beta}$ (α = 0,5, β = 6 trong mã).
  - Loss tổng: mục 1.9(a).
  - CIoU: $1-\mathrm{IoU}+\frac{\rho^2(b,b^{gt})}{c^2}+\alpha v$.
  - DFL (để giải thích vì sao bỏ): $\hat d=\sum_i i\cdot\mathrm{softmax}(z)_i$.
- **Trích:**
  - [11] YOLO; [12] YOLO26 (dùng bài arXiv, **không** chỉ dẫn trang docs như Word cũ); [22] Mamba YOLO (liên hệ).
  - CẦN BỔ SUNG: Wang et al., "YOLOv10: Real-Time End-to-End Object Detection" (NeurIPS 2024). Đây là nguồn của dual assignment và PSA; chính [12] cũng trích bài này.
  - CẦN BỔ SUNG: Feng et al., "TOOD: Task-aligned One-stage Object Detection" (ICCV 2021).
  - CẦN BỔ SUNG: Bolya et al., "YOLACT" (ICCV 2019).
  - CẦN BỔ SUNG: Zheng et al., "Distance-IoU Loss" (AAAI 2020), cho CIoU.
  - CẦN BỔ SUNG: Li et al., "Generalized Focal Loss" (NeurIPS 2020), cho DFL.
  - Tùy chọn: Carion et al., "DETR" (ECCV 2020) cho ý tưởng gán nhãn một–một.

### 2.4 Cơ chế attention và khối PSA trong C2PSA

- **Cốt lõi:**
  - Self-attention: mỗi vị trí lấy tổng có trọng số của mọi vị trí khác; chi phí O(L²).
  - Multi-head attention.
  - PSA (Partial Self-Attention, từ YOLOv10) chỉ cho **một nửa số kênh** qua attention + FFN, nửa còn lại đi tắt, để giảm chi phí.
  - Trong mã: 4 đầu, key_dim = 32, value_dim = 64, có thêm depthwise 3×3 trên V làm mã hóa vị trí.
  - Nói rõ C2PSA ở P5 (L = 400) là khối bị thay; PSABlock trong C3k2 tầng 22 vẫn giữ.
- **Công thức:**
  - $\mathrm{Attn}(Q,K,V)=\mathrm{softmax}(QK^\top/\sqrt{d_k})V$.
  - PSABlock: $x\leftarrow x+\mathrm{Proj}(\mathrm{Attn}+\mathrm{PE}(V))$; $x\leftarrow x+\mathrm{FFN}(x)$.
- **Trích:**
  - CẦN BỔ SUNG: Vaswani et al., "Attention Is All You Need" (NeurIPS 2017).
  - CẦN BỔ SUNG: Dosovitskiy et al., "ViT" (ICLR 2021).
  - CẦN BỔ SUNG: YOLOv10 (như trên, cho PSA).
  - [8], [9], [10] cho attention/transformer trong phân đoạn polyp.
- **Lưu ý tên gọi:** Word cũ có chỗ gọi PSA là "Position-Sensitive Attention", đúng như docstring Ultralytics. YOLOv10 gọi là "partial self-attention". Nên ghi cả hai, chỉ rõ nguồn từng tên. [MÃ] docstring `block.py:1343`; [HIỂU BIẾT] cho tên trong YOLOv10.

### 2.5 Mô hình không gian trạng thái: từ SSM liên tục đến S4, Mamba và VMamba

**2.5.1 SSM liên tục và rời rạc hóa**
- **Cốt lõi:** hệ tuyến tính bất biến theo thời gian ánh xạ tín hiệu u(t) qua trạng thái ẩn x(t). Rời rạc hóa với bước Δ cho ra phép truy hồi, và cũng có thể viết thành tích chập với một kernel dài.
- **Công thức:**
  - $x'(t)=Ax(t)+Bu(t),\ y(t)=Cx(t)+Du(t)$.
  - ZOH: $\bar A=e^{\Delta A}$, $\bar B=(\Delta A)^{-1}(e^{\Delta A}-I)\,\Delta B$.
  - Bilinear (S4 dùng): $\bar A=(I-\tfrac{\Delta}{2}A)^{-1}(I+\tfrac{\Delta}{2}A)$.
  - Truy hồi: $h_t=\bar Ah_{t-1}+\bar Bu_t$, $y_t=Ch_t$.
  - Dạng tích chập: $\bar K=(C\bar B, C\bar A\bar B,\dots,C\bar A^{L-1}\bar B)$, $y=\bar K*u$.
- **Trích:** [13] (dùng phương pháp bilinear, mục 2.3 của bài) [BÀI 13]; [14] (dùng ZOH, phương trình 4) [BÀI 14].

**2.5.2 S4**
- **Cốt lõi:** khởi tạo A theo HiPPO để nhớ được chuỗi dài; tham số hóa A dạng chuẩn tắc cộng hạng thấp (NPLR) để tính kernel nhanh qua nhân Cauchy. Mô hình bất biến theo thời gian (LTI), nên tính được bằng tích chập.
- **Trích:** [13] [BÀI 13: "Normal Plus Low-Rank", "HiPPO", "Cauchy kernel"]. CẦN BỔ SUNG (tùy chọn): Gu et al., "HiPPO" (NeurIPS 2020); Gu et al., "On the Parameterization and Initialization of Diagonal State Space Models (S4D)" (NeurIPS 2022), làm nguồn cho khởi tạo A = −(1…N) mà mã dùng.

**2.5.3 Mamba (selective SSM, S6)**
- **Cốt lõi:**
  - Δ, B, C trở thành hàm của đầu vào, nên mô hình hết bất biến theo thời gian và có khả năng chọn lọc: quên hoặc giữ thông tin tùy nội dung.
  - Vì hết LTI nên không tính bằng tích chập được nữa; phải tính bằng phép quét. Mamba dùng parallel scan có kernel tối ưu phần cứng (kernel fusion, recomputation).
  - Độ phức tạp tuyến tính theo L.
- **Công thức:**
  - $B_t=\mathrm{Linear}_N(u_t)$, $C_t=\mathrm{Linear}_N(u_t)$, $\Delta_t=\mathrm{softplus}(\mathrm{Param}+\mathrm{Broadcast}_D(\mathrm{Linear}_1(u_t)))$. Bài báo mô tả Δ qua phép chiếu hạng thấp; mã dùng dt_rank = 16.
  - $\bar A_t=\exp(\Delta_tA)$; B̄ trong thực hành xấp xỉ bằng $\Delta_tB_t$.
- **Trích:** [14] [BÀI 14: dòng ~227 nêu s_B, s_C, s_Δ và τ_Δ = softplus; mục 3.3.2 về scan]. CẦN BỔ SUNG (cho phép quét): Blelloch, "Prefix Sums and Their Applications" (1990); Hillis & Steele, "Data Parallel Algorithms" (CACM 1986).

**2.5.4 VMamba và SS2D**
- **Cốt lõi:**
  - Ảnh không có thứ tự một chiều tự nhiên. SS2D trải bản đồ thành 4 chuỗi (cross-scan), cho mỗi chuỗi qua một khối S6 riêng, rồi đưa về lưới và gộp lại (cross-merge). Nhờ vậy mỗi vị trí nhận thông tin từ mọi hướng, tức có trường tiếp nhận toàn cục.
  - Chi phí tuyến tính theo số token.
  - Khối VSS cải tiến **bỏ nhánh nhân (gating)** vì tính chọn lọc của SS2D đã đóng vai trò cổng.
- **Trích:** [15] [BÀI 15: Hình 2, mục 4.1–4.2]. Liên hệ: [22] Mamba YOLO (ODSSBlock); [16] U-Mamba; [17] Mamba-UNet; [18] Swin-UMamba; [19] Polyp-Mamba; [20] PolyMamba; [21] SAM-Mamba.

**2.5.5 Đối chiếu lý thuyết với cài đặt trong đề tài** (chi tiết ở phần 4). Bảng tóm tắt:

| Lý thuyết | Mã đề tài |
|---|---|
| A < 0 để ổn định | `A = −exp(A_log)` ✔ |
| ZOH cho A | `exp(ΔA)` ✔, có thêm clamp [−50, 0] |
| B̄ theo ZOH đầy đủ | B̄ ≈ ΔB (xấp xỉ bậc một, giống cách làm thực tế của Mamba) |
| Δ, B, C phụ thuộc đầu vào | ✔ |
| Skip D | **Không có** |
| Parallel scan work-efficient trên CUDA | Hillis–Steele thuần PyTorch, O(L log L) |
| VMamba: LayerNorm sau gộp, bỏ nhánh gating | Không LayerNorm; **giữ** cổng SiLU(z) |

### 2.6 Chỉ số đánh giá

- **Cốt lõi:**
  - Phân biệt độ đo theo đối tượng (P, R, F1, AP, mAP; cần ghép dự đoán–GT theo ngưỡng IoU) với độ đo theo pixel (Dice, IoU, Precision, Recall pixel).
  - Cách Ultralytics tính: mục 1.11 (101 điểm, hình thang, ghép tham lam, P/R tại điểm F1 cực đại, mặt nạ 160×160).
  - Cách đề tài tính độ đo pixel: theo `NGU_CANH_DU_AN.md` mục 4 (nhãn chuẩn vẽ từ polygon ở độ phân giải gốc; conf 0,25 rồi gộp mặt nạ). Agent dữ liệu sẽ xác nhận chi tiết.
- **Công thức:**
  - $\mathrm{IoU}=\frac{TP}{TP+FP+FN}$, $\mathrm{Dice}=\frac{2TP}{2TP+FP+FN}$.
  - $P=\frac{TP}{TP+FP}$, $R=\frac{TP}{TP+FN}$, $F1=\frac{2PR}{P+R}$.
  - $AP=\int_0^1 p_{\text{interp}}(r)\,dr$, với $p_{\text{interp}}(r)=\max_{\tilde r\ge r}p(\tilde r)$, xấp xỉ bằng 101 điểm.
  - $\mathrm{mAP}_{50:95}=\frac1{10}\sum_{\tau\in\{0,5;\dots;0,95\}}AP_\tau$.
- **Quan hệ Dice–IoU:** $\mathrm{Dice}=\frac{2\,\mathrm{IoU}}{1+\mathrm{IoU}}$ và $\mathrm{IoU}=\frac{\mathrm{Dice}}{2-\mathrm{Dice}}$, đúng **cho từng ảnh**. Ánh xạ này đồng biến, nên Dice ≥ IoU. Hai giá trị **trung bình** trên nhiều ảnh không chuyển đổi chính xác bằng công thức này (bất đẳng thức Jensen). Dice pixel trùng F1 pixel về công thức, nhưng khác F1 đối tượng.
- **Lưu ý:** không suy Dice từ mAP; TN không có nghĩa trong ma trận phát hiện.
- **Trích:**
  - CẦN BỔ SUNG: Everingham et al., "The PASCAL VOC Challenge" (IJCV 2010).
  - CẦN BỔ SUNG: Lin et al., "Microsoft COCO" (ECCV 2014), cho mAP50:95 và 101 điểm.
  - CẦN BỔ SUNG: Dice (Ecology 1945); Jaccard (1912).
  - CẦN BỔ SUNG: tài liệu Ultralytics về metric. Nguồn chính vẫn là mã fork.
  - Tùy chọn: Maier-Hein et al., "Metrics Reloaded" (Nat. Methods 2024).

### 2.7 Thống kê so sánh ghép cặp nhiều seed

- **Cốt lõi:**
  - Mỗi seed chạy cả hai mô hình với cùng dữ liệu và cùng cấu hình, nên dữ liệu là cặp. Phân tích trên hiệu $d_i = y_i - x_i$ (TSVM − Baseline).
  - Paired t-test giả định hiệu có phân phối gần chuẩn.
  - Wilcoxon signed-rank là kiểm định phi tham số dựa trên hạng của |d|.
  - Sign test chỉ dùng dấu của d.
  - Cohen's d_z là cỡ ảnh hưởng cho dữ liệu cặp.
  - Có thể thêm phân tích lực mẫu: script đã tính số cặp cần để đạt power 80%.
- **Công thức** (n = 20, df = 19):
  - $\bar d=\frac1n\sum d_i$, $s_d=\sqrt{\frac{\sum(d_i-\bar d)^2}{n-1}}$.
  - $t=\frac{\bar d}{s_d/\sqrt n}$.
  - CI95: $\bar d\pm t_{0,975;19}\,\frac{s_d}{\sqrt n}$.
  - $d_z=\bar d/s_d$, nên $t=d_z\sqrt n$.
  - Wilcoxon: $W^+=\sum_{d_i>0}\mathrm{rank}(|d_i|)$.
  - Sign test: $p=P(\mathrm{Bin}(n,0{,}5)$ cực đoan ít nhất bằng $k)$, hai phía.
- **Số liệu kiểm chứng** (bảng 04, mask mAP50-95): Δ = 0,004303; CI [−0,000228; 0,008834]; t-test p = 0,0614; Wilcoxon p = 0,0696; d_z = 0,4445; 13/20 seed TSVM cao hơn; sign test p = 0,263. Kiểm tra chéo: $t = 0{,}4445\cdot\sqrt{20}\approx 1{,}988$, khớp p ≈ 0,061. [BẢNG]; [SUY LUẬN] cho phép kiểm.
- **Mã:** `00_tai_lieu_tong_quan/scripts/tinh_lai_so_lieu.py:200-202` dùng `stats.ttest_rel`, `stats.wilcoxon`, `cohen_dz = d.mean()/d.std(ddof=1)`, `stats.binomtest`. [MÃ]
- **Trích:**
  - CẦN BỔ SUNG: Student (1908) hoặc một giáo trình thống kê.
  - CẦN BỔ SUNG: Wilcoxon, "Individual Comparisons by Ranking Methods" (Biometrics Bulletin 1945).
  - CẦN BỔ SUNG: Cohen, *Statistical Power Analysis for the Behavioral Sciences* (1988).
  - CẦN BỔ SUNG: Lakens, "Calculating and reporting effect sizes…" (Front. Psychol. 2013), cho d_z.
  - CẦN BỔ SUNG: Virtanen et al., "SciPy 1.0" (Nat. Methods 2020). Word cũ chỉ dẫn trang docs SciPy.
  - Tùy chọn: Bouthillier et al. (MLSys 2021) hoặc Picard (2021) về độ biến thiên theo seed.

### 2.8 Huấn luyện (có thể gộp vào 2.3 hoặc để sang Ch.5/6)

- AdamW; EMA trọng số; mosaic và close_mosaic; FP16 và FP32 (miền giá trị FP16 tối đa 65.504), làm nền cho mục sự cố checkpoint.
- **Trích:** CẦN BỔ SUNG: Loshchilov & Hutter, "AdamW" (ICLR 2019; Word cũ [22]). CẦN BỔ SUNG: IEEE 754-2019 (định dạng số thực). YOLOv4 cho mosaic.

---

## 3. Dàn ý Chương 3: Mô hình đề xuất

### 3.1 Tổng quan và động cơ thiết kế
- Mục tiêu: bổ sung ngữ cảnh toàn cục theo kiểu chọn lọc (SS2D) và thiên hướng hình dạng cục bộ (tích chập có hướng) tại cuối backbone P5, mà không đổi giao diện với neck.
- Cách định vị đóng góp: đề xuất và đánh giá một **cấu hình tích hợp**. Không tuyên bố phát minh SS2D, gating hay tích chập đa tỉ lệ.
- Hình: sơ đồ toàn mạng, đánh dấu tầng 10 và hai đường ra tới tầng 11 và 21.

### 3.2 Kiến trúc đối chứng YOLO26s-seg
- Bảng 24 tầng: lấy từ tài liệu 03, đã khớp bảng 08.
- Nêu riêng: SPPF có shortcut; C3k2 ở tầng 6, 8, 13, 16, 19 dùng C3k (`c3k=True` ở YAML dòng 28, 30; ở tầng 13, 16, 19 tham số `True` thứ hai là c3k); tầng 22 có `attn=True` (PSABlock).
- Đầu Segment26 + Proto26 (mục 1.2); 8.400 anchor; 32 prototype 160×160.
- C2PSA: 1 PSABlock, 4 đầu, 990.976 tham số.

### 3.3 Khối C2TSVMamba
- 3.3.1 Wrapper C2: công thức và bảng luồng tensor (mục 1.3).
- 3.3.2 Nhánh SS2D: công thức mục 1.4; tham số d_inner 256, d_state 16, dt_rank 16, expand 1; quét 4 hướng; hình minh họa cross-scan/cross-merge cho lưới 20×20.
- 3.3.3 ShapeAwareBranch + DirectionalShapeExtractor: công thức và ý nghĩa thiết kế. Nói rõ S_grad không phải Sobel.
- 3.3.4 Cổng TopologyShapeGate và điều biến (1+G): nêu khoảng (1, 2), hướng tín hiệu một chiều (shape → SS2D).
- 3.3.5 Hợp nhất, FFN, residual γ.
- 3.3.6 Bảng tham số (mục 1.5) và so sánh với C2PSA.

### 3.4 Thuật toán quét kết hợp song song
- Phát biểu toán tử kết hợp, chứng minh ngắn tính kết hợp, đưa giả mã theo `parallel_associative_scan`, nói về đệm lên lũy thừa của 2 với phần tử đơn vị.
- Độ phức tạp: độ sâu 9, công việc O(L log L). So sánh với quét tuần tự O(L) và với kernel CUDA của Mamba.
- Bảng ước tính MAC (mục 1.6), ghi rõ là ước tính. Số đo thực tế để ở Chương 6.

### 3.5 Khởi tạo và học chuyển giao
- Mục 1.7: 790.016 tham số kế thừa từ C2PSA; 1.021.185 tham số khởi tạo ngẫu nhiên; γ = 0,001; A theo S4D-Real; Δ khởi tạo mặc định.
- Hệ quả: lúc bắt đầu, tầng 10 gần như là phép chiếu cv1/cv2 kế thừa từ C2PSA, chưa có attention.

### 3.6 Hàm mất mát và chiến lược huấn luyện (dùng chung cho hai mô hình)
- Mục 1.9: E2ELoss, TAL/STAL, CIoU + L1 + BCE + seg BCE + sem (BCE + Dice), hệ số.
- Nêu rõ đề tài **không thêm** loss topology hay biên.
- AdamW thay MuSGD. amp = False. Tham số cấu hình lấy từ tài liệu 05.

### 3.7 Lưu checkpoint FP32
- Mục 1.12: nguyên nhân, bản vá, kiểm chứng (44.000 ô giống hệt; 2.000 ô khác chỉ thuộc cột `time`), giả thuyết cơ chế (thiếu LayerNorm).

### 3.8 Các chế độ ablation và giả thuyết kiểm chứng
- Bảng 4 chế độ, ước tính tham số (mục 1.8, 1.5).
- Ghi rõ **chưa có thực nghiệm**. Đề xuất cho thực nghiệm sau: cùng seed, thêm đối chứng có số tham số tương đương, thêm thí nghiệm vị trí (P4/P3), đo chỉ số biên/topology (Boundary F1, HD95, Betti error).

### 3.9 Tóm tắt chương

---

## 4. Điểm mã khác lý thuyết gốc (Mamba [14], VMamba [15])

| # | Điểm khác | Mã | Gốc | Mức xác minh | Hệ quả có thể có [SUY LUẬN] |
|---|---|---|---|---|---|
| 1 | Không có hạng tử skip D·u | không có `D`/`Ds` | Mamba/VMamba có tham số D (một hệ số skip cho mỗi kênh) | [MÃ]; [HIỂU BIẾT] cho bản gốc (mã chính thức `mamba_ssm`, VMamba `Ds`) | Mất đường tắt tuyến tính bên trong SSM; bù lại có γ-residual ở ngoài |
| 2 | Không có LayerNorm sau cross-merge, không có norm trước SS2D | — | VMamba có LN trong khối VSS (Hình 3 có "LN") và `out_norm` trong SS2D | [MÃ]; [BÀI 15] cho LN ở khối; [HIỂU BIẾT] cho `out_norm` | Biên độ F_M không bị chặn, có thể góp phần làm running_mean của `fuse.bn` lớn (sự cố FP16) |
| 3 | Giữ cổng nhân SiLU(z) | `:206` | Khối VSS cải tiến của VMamba **bỏ** nhánh nhân | [BÀI 15] mục 4.1 | Giống "vanilla VSS"/khối Mamba hơn |
| 4 | d_state = 16, expand = 1 | `:76-77, 484` | VMamba bản nhanh giảm d_state xuống 1, ssm-ratio 1–2 | [BÀI 15] mục 4.3 | Chi phí trạng thái cao hơn bản tối ưu |
| 5 | Phép quét Hillis–Steele thuần PyTorch, O(L log L), nhiều `torch.cat` | `:20-55` | Mamba: kernel CUDA, work-efficient scan, kernel fusion, recomputation; VMamba: CUDA/Triton | [MÃ]; [BÀI 14] mục 3.3.2; [BÀI 15] mục 4.3 | Chậm và tốn bộ nhớ hơn; ưu điểm là chạy được mọi nơi, tất định, export dễ |
| 6 | Δ khởi tạo mặc định | `nn.Linear` | Mamba khởi tạo để Δ ∈ [0,001; 0,1] | [MÃ]; [BÀI 14] | Phạm vi nhớ ban đầu khác thiết kế gốc |
| 7 | Clamp ΔA ∈ [−50, 0] | `:183` | Không có | [MÃ] | Cận trên 0 không bao giờ chặn vì ΔA ≤ 0; cận dưới chỉ có tác dụng khi ΔA < −50 (Ā ≈ 2·10⁻²²), và khi đó gradient theo ΔA bằng 0 |
| 8 | B̄ = ΔB (bậc một) thay ZOH đầy đủ | `:187` | Bài Mamba viết ZOH đầy đủ cho cả A và B | [MÃ]; [BÀI 14]; [HIỂU BIẾT] là mã gốc cũng dùng ΔB | Tương đương cách làm thực tế, nên nói rõ là xấp xỉ |
| 9 | Đặt SSM sau cv1 và trong wrapper C2; residual dùng γ vô hướng; không DropPath | `:413, 476-502` | VSS: x + DropPath(SS2D(LN(x))) + FFN | [MÃ]; [BÀI 15] | Thiết kế riêng của đề tài |
| 10 | Mỗi hướng có x_proj, dt_proj, A_log riêng; cộng 4 hướng khi gộp | `:116-126, 203` | VMamba cũng dùng tham số riêng cho K = 4 hướng và gộp bằng tổng | [MÃ]; [BÀI 15] Hình 2; [HIỂU BIẾT] cho chi tiết tham số | Giống gốc |
| 11 | in_proj, conv2d, out_proj không bias | `bias=False` | VMamba mặc định cũng không bias (theo hiểu biết) | [HIỂU BIẾT] | Không đáng kể |
| 12 | Không có ràng buộc topology; "topology" chỉ là tên module | toàn file | — | [MÃ] | Không được tuyên bố bảo toàn topology |

Các kết luận an toàn nên dùng trong báo cáo:
- "SS2D được cài đặt lại bằng PyTorch thuần theo tinh thần của VMamba, với một số đơn giản hóa (không D, không LayerNorm, Δ khởi tạo mặc định) và một phép quét song song kiểu Hillis–Steele."
- Không viết "độ phức tạp tuyến tính" cho mã của đề tài.

---

## 5. Lỗi hoặc điểm chưa chính xác trong bản Word cũ

Đã đọc nhanh chương 1–2 (`CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx`, trích bằng python-docx). Nhìn chung bản cũ khá thận trọng; phần lớn mô tả kiến trúc **đúng**: kênh 256/512, tầng 10, dt_rank 16, không LN/D, O(L log L), 9 bước, hệ số (1,2), bảng 2.1 kênh P3/P4/P5. Các điểm cần sửa:

| # | Vị trí Word | Nội dung cũ | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | 2.5, đoạn 335 và 337 | "Các tham số của module thay thế không có đối ứng trong C2PSA nên được khởi tạo riêng"; "lớp C2TSVMamba… có cấu trúc tham số riêng" | **Thiếu và gây hiểu nhầm.** 790.016/1.811.201 tham số (cv1, cv2, m.0.ffn) **nhận trọng số C2PSA** | Viết theo mục 1.7 |
| 2 | 2.5, đoạn 336 và 338 | Mô tả loss chung chung: "reg_max = 1 làm DFL nhiều bin không hoạt động" | Thiếu đầu đôi o2m/o2o, Progressive Loss 0,8 → 0,1, thành phần L1 (×1,5), sem loss (BCE + Dice, chỉ khi huấn luyện), seg loss dùng hệ số box 7,5 | Viết theo mục 1.9 |
| 3 | 1.2.2 và TLTK [16] | YOLO26 trích trang docs Ultralytics | TLTK đã có bài arXiv YOLO26 [12] | Trích [12] |
| 4 | 1.2.2 và 2.1 | "Backbone kết thúc bằng SPPF và C2PSA"; không nhắc PSA trong neck | Bỏ sót: C3k2 tầng 22 có `attn=True` (PSABlock), cả hai mô hình đều có. Người đọc có thể hiểu TSVM loại hết attention | Thêm một câu |
| 5 | 1.2.2 | "Cấu hình end2end được bật" | Chưa giải thích end2end = đầu one2one, top-300, **không NMS**; `iou` không dùng khi validate | Bổ sung |
| 6 | 1.3 | Chỉ có công thức truy hồi trong mã | Thiếu nền SSM liên tục, ZOH, S4 (TLTK [13] không được trích ở Word) | Viết mục 2.5 |
| 7 | 1.4.1–1.4.2, Bảng 1.1, TLTK [18]–[21] | Topo-VM-UNetV2, CSG-Mamba (arXiv 2608.14146), MambaPSA (arXiv 2607.12681), "Mamba Guided Boundary Prior Matters"/SAM-MaGuP | **Không có trong TLTK/MANIFEST.** Bốn mục này chưa được xác minh tồn tại hay nội dung. Word [21] khác TLTK [21] ("SAM-Mamba", WACV 2025, cùng nhóm tác giả Dutta/Jha), có thể đã nhầm | Giao agent tài liệu xác minh; nếu không xác minh được thì bỏ |
| 8 | Toàn chương 1–2 | Không trích FPN [23], EfficientDet [24], YOLO [11], S4 [13], Mamba YOLO [22], các bài Mamba y khoa [16]–[20] | TLTK có sẵn mà chưa dùng | Dùng theo phần 6 |
| 9 | 2.1, đoạn 292–293 | $M_i = \mathrm{sigmoid}(\sum a_{ij}P_j)$ | Đúng về nguyên lý; mã nhị phân bằng logit > 0 sau khi upsample, rồi cắt hộp | Ghi chú thêm (không phải lỗi) |
| 10 | 5.6.2 | val/sem_loss = 0 "không áp dụng" | Đúng nhưng thiếu lý do | Nêu: nhánh semseg chỉ chạy khi `training` (mục 1.9) |
| 11 | 5.2.2 | Chưa nêu cách Ultralytics tính P/R/AP | Thiếu: P/R tại điểm F1 cực đại, AP 101 điểm + hình thang, ghép tham lam, mặt nạ 160×160 | Đưa vào 2.6 |
| 12 | Bố cục | Chương 1 trộn tổng quan với lý thuyết; Chương 2 là thiết kế | Bố cục mới tách Ch.2 (lý thuyết) và Ch.3 (mô hình) | Theo dàn ý ở trên |
| 13 | 2.6 | Bốn mode, chưa có số tham số | Các mode có số tham số khác nhau (1,07–1,81 triệu) | Bổ sung bảng mục 1.5 |
| 14 | Docstring trong mã (không phải Word) | `parallel_associative_scan` ghi "AMP-compatible", "O(log L)" | O(log L) là **độ sâu**, công việc là O(L log L). Báo cáo không nên chép câu này | Lưu ý khi viết |

Không phát hiện lỗi số kênh hay vị trí tầng trong Word chương 1–2.

---

## 6. Danh sách tài liệu cần trích cho từng mục

| Mục | Có trong TLTK | CẦN BỔ SUNG |
|---|---|---|
| 2.1 Phân đoạn y khoa/polyp | [1], [2], [3], [4] | FCN (Long 2015); Mask R-CNN (He 2017) |
| 2.2 CNN/encoder–decoder/FPN | [5], [6], [7], [23], [24] | BatchNorm (Ioffe 2015); SiLU/Swish (Elfwing 2018 / Ramachandran 2017); MobileNet hoặc Xception; PANet (Liu 2018); CSPNet (Wang 2020); SPP (He 2015); YOLOv4 (Bochkovskiy 2020) |
| 2.3 YOLO → YOLO26-seg | [11], [12], [22] | **YOLOv10 (Wang 2024)**; TOOD (Feng 2021); YOLACT (Bolya 2019); CIoU/DIoU (Zheng 2020); GFL/DFL (Li 2020); DETR (Carion 2020, tùy chọn) |
| 2.4 Attention/PSA | [8], [9], [10] | Vaswani 2017; ViT (Dosovitskiy 2021); YOLOv10 cho PSA |
| 2.5 SSM/S4/Mamba/VMamba | [13], [14], [15], [16]–[22] | HiPPO (Gu 2020); S4D (Gu 2022); Blelloch 1990; Hillis & Steele 1986; LayerScale (Touvron 2021, nếu so sánh γ) |
| 2.6 Chỉ số | — | PASCAL VOC (Everingham 2010); COCO (Lin 2014); Dice 1945; Jaccard 1912; Metrics Reloaded (Maier-Hein 2024, tùy chọn) |
| 2.7 Thống kê | — | Wilcoxon 1945; Cohen 1988; Lakens 2013; SciPy (Virtanen 2020); Student 1908 hoặc giáo trình |
| 2.8 Huấn luyện | — | AdamW (Loshchilov 2019); IEEE 754-2019 |
| Ch.3 | [12], [14], [15], [22] (Mamba trong YOLO), [19], [20] (Mamba cho polyp) | YOLOv10 (PSA, C2PSA); S4D (khởi tạo A) |
| Word cũ cần xác minh | — | Topo-VM-UNetV2 (arXiv 2505.06210), CSG-Mamba (arXiv 2608.14146), MambaPSA (arXiv 2607.12681), "Mamba Guided Boundary Prior Matters" (arXiv 2507.01509) |

---

### Giới hạn của báo cáo này

- Chỉ đọc mã và PDF; **không chạy mô hình**. Số MAC và độ phức tạp ở mục 1.6 là ước tính giải tích.
- Văn bản PDF trích bằng pypdf; công thức bị vỡ ký tự. Phần đối chiếu bài báo dựa trên đoạn văn và từ khóa, không kiểm tra từng phương trình.
- Các khẳng định ghi [HIỂU BIẾT] (skip D, `out_norm` của VMamba, tên "partial self-attention" của YOLOv10, B̄ = ΔB trong mã Mamba) cần kiểm lại trước khi đưa vào báo cáo.
- Con số "16/40 lượt có epoch max-mask khác epoch max-fitness" lấy từ Word cũ; tôi chưa tự tính lại.
