# BÁO CÁO ĐẶC TẢ HƯỚNG NGHIÊN CỨU
## Tích hợp Topology-Shape-aware VMamba vào YOLO26-seg cho phân đoạn polyp từ ảnh nội soi đại trực tràng

---

## 1. Bối cảnh đề tài

Đề tài tổng thể:

**“Nghiên cứu phương pháp tích hợp VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng.”**

Bài toán chính là **instance segmentation polyp** trên ảnh nội soi đại trực tràng.

Mô hình cần thực hiện:

- phát hiện vị trí polyp;
- xác định số lượng polyp;
- tạo mask phân đoạn cho từng polyp;
- đặc biệt quan tâm đến độ chính xác của biên mask và khả năng xử lý các polyp có hình dạng đa dạng.

Dataset chính:

**Kvasir-SEG**, được chuyển đổi sang định dạng segmentation phù hợp với YOLO.

Các metric quan tâm:

- Dice;
- IoU;
- Precision;
- Recall;
- F1-score;
- mask mAP50;
- mask mAP50-95;
- inference speed;
- số lượng tham số;
- FLOPs/GFLOPs hoặc chi phí tính toán.

---

# 2. Vấn đề nghiên cứu

YOLO26-seg có khả năng phát hiện và phân đoạn đối tượng, tuy nhiên đối với polyp, bài toán có một số khó khăn:

### 2.1. Hình dạng polyp đa dạng

Polyp có thể:

- tròn;
- dài;
- méo;
- có cuống;
- phẳng;
- có biên không đều;
- thay đổi kích thước;
- có hình dạng phức tạp.

Do đó, chỉ sử dụng đặc trưng thông thường có thể chưa đủ để mô hình biểu diễn tốt hình dạng của polyp.

### 2.2. Biên polyp khó xác định

Trong ảnh nội soi:

- màu polyp có thể gần với mô xung quanh;
- biên có thể mờ;
- ánh sáng phản chiếu;
- nhiễu;
- texture phức tạp;
- vùng polyp có thể bị che một phần.

Vì vậy mask dự đoán có thể:

- bị thiếu một phần;
- ăn ra ngoài polyp;
- bị lõm;
- bị đứt;
- hoặc không giữ được cấu trúc của vùng polyp.

### 2.3. Quan hệ không gian và ngữ cảnh

Một điểm ảnh hoặc feature tại một vị trí không chỉ phụ thuộc vào vùng lân cận rất gần mà còn có thể cần thông tin từ các vùng xa hơn.

Ví dụ:

Một vùng biên khó phân biệt có thể cần thông tin từ toàn bộ vùng polyp để xác định nó thuộc polyp hay background.

Đây là phần mà **VMamba** được đưa vào để khai thác thông tin không gian và ngữ cảnh dài hạn.

---

# 3. Ý tưởng nghiên cứu chính

Ý tưởng là không chỉ tích hợp VMamba đơn thuần vào YOLO26-seg.

Thay vào đó, xây dựng một module lai:

**Topology-Shape-aware VMamba**

Module này kết hợp ba thành phần chính:

1. **VMamba branch**
   - khai thác thông tin không gian;
   - mô hình hóa ngữ cảnh dài hạn;
   - sử dụng cơ chế selective scan/SS2D.

2. **Shape-aware branch**
   - tập trung vào hình dạng;
   - biên;
   - hướng;
   - cấu trúc cục bộ của polyp.

3. **Topology-aware mechanism**
   - định hướng bảo toàn cấu trúc liên kết của vùng polyp;
   - hạn chế tình trạng mask bị đứt hoặc cấu trúc bị biến dạng.

Ý tưởng tổng quát:

> **VMamba giúp mô hình “nhìn rộng” để hiểu ngữ cảnh, Shape-aware giúp mô hình “nhìn hình dạng và biên”, còn Topology-aware giúp quan tâm đến tính liên kết/cấu trúc của vùng được phân đoạn.**

---

# 4. Topology là gì?

Topology trong bài toán segmentation có thể hiểu đơn giản là:

> **đặc trưng về cấu trúc liên kết của một vùng.**

Không chỉ quan tâm vùng đó có hình dạng như thế nào mà còn quan tâm:

- các phần của vùng có liên tục với nhau không;
- vùng có bị chia thành nhiều phần không;
- có xuất hiện lỗ/hole bất thường không;
- cấu trúc của vùng dự đoán có tương ứng với cấu trúc thật không.

Ví dụ:

Ground Truth:

```text
████████
████████
████████
```

Mask dự đoán:

```text
██  ████
██  ████
██  ████
```

Hai vùng có thể vẫn có diện tích tương đối lớn, nhưng cấu trúc đã bị chia bởi một khoảng trống.

IoU/Dice có thể vẫn cho kết quả tương đối tốt trong một số trường hợp, nhưng về mặt cấu trúc, mask đã bị thay đổi.

Do đó topology hướng tới việc quan tâm thêm:

**“Vùng polyp có giữ được cấu trúc liên kết hợp lý hay không?”**

---

# 5. Shape và Topology khác nhau như thế nào?

Cần phân biệt rõ hai khái niệm.

## Shape

Shape tập trung vào:

- hình dạng;
- đường biên;
- độ cong;
- hướng;
- kích thước;
- cấu trúc cục bộ.

Ví dụ:

```text
    ███
  ███████
 █████████
  ███████
    ███
```

Shape-aware muốn mô hình hiểu:

> vùng này có hình dạng gần tròn/oval và biên nằm ở đâu.

---

## Topology

Topology quan tâm nhiều hơn đến:

- tính liên thông;
- cấu trúc kết nối;
- thành phần liên thông;
- lỗ/hole;
- sự liên tục của vùng.

Ví dụ:

```text
████████
████████
████████
```

là một vùng liên thông.

Trong khi:

```text
██  ████
██  ████
██  ████
```

đã bị chia thành hai vùng.

---

## Có thể hiểu ngắn gọn

**Shape:**

> “Nó có hình dạng như thế nào?”

**Topology:**

> “Các phần của nó liên kết với nhau như thế nào?”

---

# 6. VMamba có vai trò gì?

VMamba là thành phần chịu trách nhiệm chính về:

**khai thác thông tin không gian và ngữ cảnh dài hạn.**

Trong feature map:

```text
H × W × C
```

VMamba sử dụng cơ chế SS2D để xử lý thông tin theo không gian hai chiều.

Có thể hình dung:

```text
        Feature Map

→ → → → → → → → →
→ → → → → → → → →
→ → → → → → → → →
→ → → → → → → → →

và các hướng quét khác
```

Mục đích là giúp feature tại một vị trí có thể sử dụng thông tin từ các vùng xa hơn.

Do đó:

**VMamba = Context / Long-range Spatial Modeling**

Nói đơn giản:

> VMamba giúp mô hình nhìn rộng hơn thay vì chỉ tập trung vào vùng lân cận.

---

# 7. Shape-aware branch có vai trò gì?

Shape-aware branch là một nhánh riêng chạy song song với VMamba.

Nó tập trung vào:

- biên;
- hướng;
- độ cong;
- cấu trúc cục bộ;
- hình dạng của polyp.

Một thiết kế có thể sử dụng:

### Local shape extraction

```text
DWConv 3×3
DWConv 5×5
```

để lấy đặc trưng hình dạng ở nhiều receptive field.

Sau đó sử dụng directional operators:

```text
Horizontal: 1×5
Vertical:   5×1
Curvature:  3×3
```

và gradient:

```text
G = sqrt(Sh² + Sv² + ε)
```

Mục tiêu là tạo ra feature:

```text
S = Shape Feature
```

---

# 8. Topology-aware mechanism

Đây là phần quan trọng cần thiết kế cẩn thận.

Nếu muốn gọi module là **Topology-Shape-aware VMamba**, topology không nên chỉ là tên gọi.

Cần có cơ chế thực sự liên quan đến cấu trúc liên kết.

Có thể nghiên cứu theo hướng:

### Hướng A — Topology-aware feature extraction

Tạo feature mô tả cấu trúc liên kết từ feature map.

Ví dụ:

```text
Feature Map
     ↓
Structural / Connectivity Extraction
     ↓
Topology Feature T
```

Sau đó kết hợp:

```text
T + S + VMamba
```

---

### Hướng B — Topology-aware gating

Topology feature tạo ra gate:

```text
G_T = sigmoid(Conv1×1(T))
```

Shape feature tạo ra gate:

```text
G_S = sigmoid(Conv1×1(S))
```

Sau đó:

```text
G_TS = f(G_T, G_S)
```

và dùng gate để điều chỉnh VMamba:

```text
F_M' = F_M ⊙ (1 + G_TS)
```

Trong đó:

- `F_M`: feature từ VMamba;
- `G_TS`: topology-shape gate;
- `⊙`: phép nhân từng phần tử.

---

# 9. Tại sao phải điều chỉnh VMamba bằng Topology/Shape?

VMamba có khả năng lấy context rộng.

Tuy nhiên:

> context rộng không đồng nghĩa với việc feature tự động hiểu được cấu trúc hình dạng và topology của polyp.

Do đó Shape/Topology branch có thể đóng vai trò như một tín hiệu hướng dẫn.

Ví dụ:

```text
                 ┌───────────────┐
Input Feature ──►│    VMamba     │
                 └───────┬───────┘
                         │
                         ▼
                       F_M
                         │
                         │ × Gate
                         ▼
                       F_M'
                         
Input Feature ──► Shape/Topology
                       │
                       ▼
                  G_TS / G_T
```

Gate cho mô hình biết:

> “Ở những vị trí có đặc trưng cấu trúc/hình dạng quan trọng, hãy tăng mức chú ý của feature VMamba.”

---

# 10. Vì sao vẫn cần giữ Shape/Topology feature sau khi tạo Gate?

Không nên chỉ dùng Shape/Topology để tạo gate rồi bỏ nó đi.

Ví dụ:

```text
Shape/Topology
      │
      ├────► Gate ─────► VMamba modulation
      │
      └────────────────► Fusion
```

Lý do:

Gate chỉ là một tín hiệu điều chỉnh.

Nếu chỉ dùng gate:

```text
Shape → Gate → VMamba
```

thì một phần thông tin shape/topology ban đầu có thể không được truyền trực tiếp sang feature cuối.

Do đó nên giữ lại feature:

```text
F_M'
```

và:

```text
F_TS
```

để fusion.

---

# 11. Cơ chế fusion

Sau khi có:

```text
F_M' = VMamba feature đã được điều chỉnh
```

và:

```text
F_TS = Topology-Shape feature
```

có thể:

```text
F_cat = Concat(F_M', F_TS)
```

Ví dụ:

```text
F_M'  = [B, 64, 40, 40]

F_TS  = [B, 64, 40, 40]

Concat
   ↓

[B, 128, 40, 40]
```

Sau đó:

```text
Conv 1×1
```

để học cách trộn các channel.

Ví dụ:

```text
128 channels
      ↓
Conv 1×1
      ↓
64 channels
```

Sau đó có thể sử dụng FFN để tiếp tục biến đổi/refine feature.

---

# 12. FFN có vai trò gì?

FFN = Feed-Forward Network.

Trong module này, FFN không phải một nguồn feature thứ ba.

Nó là bước:

> biến đổi và tinh chỉnh representation sau khi các feature đã được fusion.

Có thể hình dung:

```text
Concat
   ↓
Conv 1×1
   ↓
Learned Channel Mixing
   ↓
FFN
   ↓
Feature Refinement
```

---

# 13. Residual connection

Sau fusion có thể sử dụng residual:

```text
Y = X + γF_out
```

Trong đó:

- `X`: feature đầu vào;
- `F_out`: feature đã được xử lý;
- `γ`: learnable scaling parameter.

Có thể khởi tạo:

```text
γ = 0.001
```

Mục đích:

Ban đầu module mới chỉ tác động nhẹ lên feature của YOLO26.

Trong quá trình training, model tự học mức độ đóng góp phù hợp.

Điều này giúp việc thay thế block ổn định hơn.

---

# 14. Kiến trúc tổng thể đề xuất

Kiến trúc có thể được biểu diễn:

```text
                         Input Feature X
                                │
                                ▼
                    ┌──────────────────────┐
                    │     C2 Structure     │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
          ┌──────────────┐           ┌─────────────────┐
          │    VMamba    │           │ Shape/Topology  │
          │    Branch    │           │     Branch      │
          └──────┬───────┘           └────────┬────────┘
                 │                            │
                 │ F_M                        │ F_TS
                 │                            │
                 │                     ┌──────┴───────┐
                 │                     │              │
                 │                     ▼              ▼
                 │                  Shape Gate   Topology Gate
                 │                     │              │
                 │                     └──────┬───────┘
                 │                            │
                 │                            ▼
                 │                         G_TS
                 │                            │
                 └────────────────────────────┤
                                              ▼
                              F_M' = F_M ⊙ (1 + G_TS)
                                              │
                       ┌──────────────────────┴──────────────┐
                       │                                     │
                       ▼                                     ▼
                    F_M'                                  F_TS
                       │                                     │
                       └──────────────┬──────────────────────┘
                                      ▼
                                   Concat
                                      │
                                      ▼
                                  Conv 1×1
                                      │
                                      ▼
                                     FFN
                                      │
                                      ▼
                              Residual + γ
                                      │
                                      ▼
                              Output Feature Y
                                      │
                                      ▼
                              YOLO26 Neck/Head
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                    Detection                  Segmentation
```

---

# 15. Vị trí tích hợp vào YOLO26-seg

Không thay đổi toàn bộ YOLO26.

Mục tiêu là giữ nguyên YOLO26-seg và thay thế **một block nghiên cứu cụ thể**.

Ví dụ:

```text
YOLO26-seg
    │
    ├── Backbone
    │
    ├── ...
    │
    ├── Layer 10: C2PSA
    │
    ├── Neck
    │
    └── Segmentation Head
```

Thay bằng:

```text
YOLO26-seg
    │
    ├── Backbone
    │
    ├── ...
    │
    ├── Layer 10: C2TSVMamba
    │
    ├── Neck
    │
    └── Segmentation Head
```

Điểm quan trọng:

**Không thay đổi toàn bộ YOLO26-seg.**

Chỉ thay block nghiên cứu tại vị trí được chọn.

---

# 16. C2TSVMamba nghĩa là gì?

Tên module:

**C2TSVMamba**

có thể hiểu:

```text
C2       +       TS       +       VMamba
│                 │                 │
│                 │                 └── VMamba/SS2D
│                 │
│                 └── Topology-Shape
│
└── C2-style wrapper
```

C2 được giữ lại vì module mới được thiết kế để đóng vai trò tương thích với cấu trúc C2PSA trong YOLO26.

Có thể hiểu:

```text
C2PSA
= C2 + PSA

C2TSVMamba
= C2 + Topology-Shape + VMamba
```

Điểm nghiên cứu nằm ở việc:

> giữ cấu trúc C2-style để tích hợp vào YOLO26 nhưng thay cơ chế xử lý bên trong bằng hybrid Topology-Shape + VMamba.

---

# 17. Điểm khác biệt giữa C2PSA và C2TSVMamba

## C2PSA

Mục đích chính:

- xử lý feature;
- khai thác quan hệ giữa các feature;
- sử dụng cơ chế PSA/attention.

Có thể biểu diễn đơn giản:

```text
Input
  ↓
C2
  ↓
PSA / Attention
  ↓
Output
```

---

## C2TSVMamba

Đề xuất:

```text
Input
  ↓
C2
  ↓
 ┌───────────────┬────────────────┐
 │               │                │
 ▼               ▼                │
VMamba       Shape/Topology       │
 │               │                │
 │               ▼                │
 │             Gate               │
 │               │                │
 └───────► Modulation ◄───────────┘
                 │
                 ▼
              Fusion
                 │
                 ▼
                FFN
                 │
                 ▼
              Residual
```

---

# 18. Ý tưởng khoa học của phương pháp

Giả thuyết nghiên cứu:

> Việc kết hợp khả năng mô hình hóa ngữ cảnh không gian dài hạn của VMamba với các đặc trưng hình dạng và cấu trúc liên kết có thể giúp YOLO26-seg biểu diễn tốt hơn các polyp có hình dạng đa dạng và cải thiện chất lượng mask, đặc biệt tại các vùng biên và cấu trúc khó phân đoạn.

Nói đơn giản:

```text
VMamba
   ↓
Context
   +
Shape
   ↓
Boundary / Geometry
   +
Topology
   ↓
Connectivity / Structure
   =
Better Representation
   ↓
Better Segmentation
```

---

# 19. Vì sao hướng này phù hợp với bài toán polyp?

Polyp segmentation không chỉ cần biết:

> “Đây có phải polyp không?”

mà còn cần:

> “Biên polyp nằm chính xác ở đâu?”

và:

> “Toàn bộ vùng polyp có được phân đoạn liên tục và hợp lý không?”

Do đó có ba nhu cầu:

### Nhu cầu 1 — Context

VMamba giải quyết:

**“Nhìn rộng để hiểu ngữ cảnh.”**

### Nhu cầu 2 — Shape

Shape-aware giải quyết:

**“Hiểu hình dạng, biên và cấu trúc cục bộ.”**

### Nhu cầu 3 — Topology

Topology-aware giải quyết:

**“Quan tâm đến tính liên kết và cấu trúc của vùng dự đoán.”**

---

# 20. Cần đặc biệt chú ý: Topology không được chỉ là tên gọi

Đây là vấn đề quan trọng nhất khi triển khai hướng này.

Nếu module chỉ có:

```text
DWConv
Gradient
Directional Feature
Gate
VMamba
```

thì phần triển khai thực tế chủ yếu là:

**Shape-aware / Structure-aware**

chứ chưa phải topology-aware theo nghĩa chặt.

Nếu muốn sử dụng tên:

**Topology-Shape-aware VMamba**

cần bổ sung một cơ chế topology thực sự.

Ví dụ có thể nghiên cứu:

### 20.1. Connectivity constraint

Đánh giá tính liên thông của prediction và ground truth.

### 20.2. Topology-aware loss

Thêm loss liên quan tới topology:

```text
L_total =
L_detection
+ L_segmentation
+ λ L_topology
```

### 20.3. Skeleton / centerline representation

Trích xuất cấu trúc skeleton hoặc medial representation để mô hình học cấu trúc.

### 20.4. Connected-component consistency

Khuyến khích cấu trúc connected components của prediction phù hợp với ground truth.

### 20.5. Euler characteristic

Có thể nghiên cứu các đại lượng topology như Euler characteristic nếu phù hợp với bài toán.

### 20.6. Persistent homology

Nếu muốn nghiên cứu sâu hơn, persistent homology có thể được xem xét để mô tả cấu trúc topology.

---

# 21. Không được tự động kết luận topology đã được giải quyết

Khi đánh giá mô hình, không được viết:

> “Module đảm bảo topology của polyp được bảo toàn.”

nếu chưa có topology constraint hoặc metric chứng minh điều đó.

Nên viết:

> “Module được thiết kế theo định hướng khai thác đặc trưng topology và shape của vùng polyp.”

Hoặc nếu đã triển khai topology loss:

> “Topology-aware loss được sử dụng để khuyến khích tính nhất quán về cấu trúc liên kết giữa mask dự đoán và ground truth.”

Đây là cách diễn đạt khoa học hơn.

---

# 22. Thiết kế thực nghiệm bắt buộc

Không nên chỉ train:

```text
YOLO26-seg
vs
YOLO26 + C2TSVMamba
```

mà nên có ablation study.

## Experiment 1 — Baseline

```text
YOLO26-seg
```

---

## Experiment 2 — VMamba only

```text
YOLO26-seg
+
VMamba
```

Mục đích:

Xác định riêng đóng góp của VMamba.

---

## Experiment 3 — Shape only

```text
YOLO26-seg
+
Shape-aware
```

Mục đích:

Xác định riêng đóng góp của Shape-aware.

---

## Experiment 4 — VMamba + Shape

```text
YOLO26-seg
+
VMamba
+
Shape-aware
```

Mục đích:

Kiểm tra hiệu quả của hybrid.

---

## Experiment 5 — VMamba + Shape + Topology

```text
YOLO26-seg
+
VMamba
+
Shape-aware
+
Topology-aware
```

Đây là mô hình đề xuất cuối cùng.

---

# 23. Bảng ablation đề xuất

| Model | VMamba | Shape | Topology | Mục đích |
|---|---:|---:|---:|---|
| YOLO26-seg | ❌ | ❌ | ❌ | Baseline |
| YOLO26 + VMamba | ✅ | ❌ | ❌ | Đánh giá VMamba |
| YOLO26 + Shape | ❌ | ✅ | ❌ | Đánh giá Shape |
| YOLO26 + VMamba + Shape | ✅ | ✅ | ❌ | Đánh giá hybrid |
| YOLO26 + VMamba + Shape + Topology | ✅ | ✅ | ✅ | Mô hình đề xuất |

Nếu kết quả:

```text
Baseline
   <
VMamba
   <
VMamba + Shape
   <
VMamba + Shape + Topology
```

thì sẽ có bằng chứng tốt hơn cho giả thuyết nghiên cứu.

---

# 24. Các metric cần theo dõi

## Segmentation

- Dice;
- IoU;
- mask mAP50;
- mask mAP50-95.

## Detection

- Precision;
- Recall;
- mAP50;
- mAP50-95.

## Computational

- Parameters;
- GFLOPs;
- inference latency;
- FPS nếu phù hợp;
- VRAM.

## Nếu topology được triển khai thực sự

Có thể bổ sung:

- topology error;
- connected-component consistency;
- Betti-number based metric;
- Euler characteristic difference;

tùy theo phương pháp topology được chọn.

---

# 25. Kiểm soát tính công bằng của thí nghiệm

Baseline và proposed model phải sử dụng cùng:

- dataset;
- train/validation split;
- image size;
- batch size;
- epochs;
- optimizer;
- learning rate;
- augmentation;
- random seed;
- hardware;
- evaluation protocol.

Chỉ nên thay đổi:

**module kiến trúc nghiên cứu.**

Ví dụ:

```text
YOLO26-seg
       │
       ├── cùng dataset
       ├── cùng seed
       ├── cùng epochs
       ├── cùng optimizer
       ├── cùng imgsz
       └── cùng GPU
                 │
          Architecture
             thay đổi
```

Như vậy nếu kết quả thay đổi, có cơ sở tốt hơn để quy cho module.

---

# 26. Ví dụ minh họa trực quan

Giả sử polyp có dạng:

```text
        ████
      ████████
     ██████████
      ████████
        ████
```

### VMamba

Tập trung vào context:

```text
←────────────────────→
      Toàn vùng
```

Nó giúp hiểu mối quan hệ giữa các vùng xa nhau.

### Shape-aware

Tập trung:

```text
      ↑ biên
   ←───────→
    hình dạng
```

### Topology-aware

Quan tâm:

```text
      vùng có liên tục?
             ↓
       █████████
       █████████
       █████████
```

có bị:

```text
███   █████
███   █████
```

hay không.

### Hybrid

```text
Context
   +
Shape
   +
Topology
   ↓
Better Feature
   ↓
Better Mask
```

---

# 27. Câu trả lời khi giảng viên hỏi “Tại sao cần Topology?”

Có thể trả lời:

> “Trong phân đoạn polyp, không chỉ cần dự đoán đúng diện tích mà còn cần mask giữ được cấu trúc hợp lý. Một mask có thể có IoU tương đối tốt nhưng vẫn bị đứt hoặc xuất hiện cấu trúc bất thường. Vì vậy em muốn nghiên cứu thêm đặc trưng topology, tức là tính liên kết và cấu trúc của vùng polyp, bên cạnh shape và context.”

---

# 28. Nếu giảng viên hỏi “VMamba chưa đủ sao?”

Trả lời:

> “VMamba chủ yếu được sử dụng để khai thác thông tin không gian và ngữ cảnh dài hạn. Tuy nhiên segmentation còn yêu cầu biểu diễn chính xác hình dạng và cấu trúc của đối tượng. Vì vậy em đặt giả thuyết rằng việc bổ sung Shape-aware và Topology-aware mechanism có thể cung cấp thông tin bổ sung cho VMamba. Em sẽ kiểm chứng giả thuyết này bằng ablation study thay vì giả định trước rằng nó chắc chắn tốt hơn.”

---

# 29. Nếu giảng viên hỏi “Topology của em nằm ở đâu trong code?”

Câu trả lời phải phụ thuộc vào implementation thực tế.

Nếu chỉ có Shape branch:

> “Phần hiện tại chủ yếu mới khai thác shape, boundary, directional và structural features. Vì vậy em chưa nên khẳng định đây là topology-aware đầy đủ. Nếu sử dụng tên Topology-Shape-aware, em sẽ bổ sung một topology mechanism hoặc topology-aware loss để tên gọi phản ánh đúng implementation.”

Nếu đã có topology loss:

> “Topology được đưa vào thông qua topology-aware loss, nhằm tạo thêm ràng buộc để cấu trúc liên kết của mask dự đoán gần với ground truth.”

Nếu đã có topology feature:

> “Topology được biểu diễn thành feature và đưa vào gate/fusion cùng với shape feature.”

---

# 30. Mục tiêu cuối cùng của hướng nghiên cứu

Mục tiêu không phải tạo một module phức tạp chỉ để tăng số lượng thành phần.

Mục tiêu là kiểm chứng giả thuyết:

> **Kết hợp khả năng mô hình hóa ngữ cảnh dài hạn của VMamba với thông tin shape và topology có thể cải thiện chất lượng phân đoạn polyp, đặc biệt đối với các trường hợp có hình dạng phức tạp, biên khó xác định và cấu trúc mask dễ bị sai lệch.**

Pipeline:

```text
Kvasir-SEG
     ↓
YOLO segmentation format
     ↓
YOLO26-seg baseline
     ↓
Replace selected C2PSA block
     ↓
C2TSVMamba
     ↓
 ┌─────────────┬──────────────┬───────────────┐
 │             │              │
VMamba       Shape         Topology
 │             │              │
 │             └──────┬───────┘
 │                    │
 └──────────────┬─────┘
                ↓
             Fusion
                ↓
             YOLO26
                ↓
       Detection + Mask
                ↓
           Evaluation
```

---

# 31. Tóm tắt một câu

**VMamba chịu trách nhiệm khai thác ngữ cảnh không gian dài hạn, Shape-aware tập trung vào hình dạng và biên, còn Topology-aware tập trung vào cấu trúc liên kết của vùng polyp; ba nguồn thông tin được kết hợp trong một module C2-compatible để thay thế block C2PSA tại vị trí nghiên cứu của YOLO26-seg.**

---

# 32. Quy tắc quan trọng cho AI tiếp tục triển khai

AI tiếp tục thực hiện hướng nghiên cứu này phải tuân thủ:

1. Không thay đổi baseline `YOLO26-seg` gốc.
2. Không tự ý thay đổi nhiều layer nếu chưa có lý do nghiên cứu.
3. Phải xác định rõ vị trí module mới trong architecture.
4. Phải giữ kích thước feature map/channel tương thích với YOLO26.
5. Không gọi một thành phần là “topology-aware” nếu implementation không thực sự có cơ chế topology.
6. Phải phân biệt:
   - context;
   - shape;
   - topology.
7. Phải có baseline và ablation study.
8. Không được kết luận module tốt hơn chỉ vì ý tưởng nghe hợp lý.
9. Kết luận phải dựa trên metric thực nghiệm.
10. Nếu topology mechanism chưa được triển khai, phải nói rõ đây là phần cần nghiên cứu/bổ sung chứ không được giả định là đã có.
11. Ưu tiên thiết kế module có khả năng train end-to-end và tương thích với pipeline YOLO26-seg.
12. Ưu tiên giữ chi phí tính toán hợp lý vì đề tài cần so sánh cả accuracy và computational cost.

---

# 33. Từ khóa để AI hiểu đúng hướng

```text
YOLO26-seg
Polyp Instance Segmentation
Kvasir-SEG
VMamba
SS2D
Long-range Spatial Context
Shape-aware Feature Extraction
Boundary-aware Representation
Directional Feature
Topology-aware Segmentation
Connectivity
Connected Components
Topology-aware Loss
C2-compatible Block
C2PSA Replacement
Feature Gating
Feature Modulation
Feature Fusion
Ablation Study
Dice
IoU
Mask mAP50
Mask mAP50-95
Inference Latency
Parameters
GFLOPs
```

**Định hướng cốt lõi:**

```text
YOLO26-seg
      +
VMamba
      +
Shape-aware
      +
Topology-aware
      ↓
C2TSVMamba
      ↓
Better contextual + geometric + structural representation
      ↓
Better polyp segmentation
```
