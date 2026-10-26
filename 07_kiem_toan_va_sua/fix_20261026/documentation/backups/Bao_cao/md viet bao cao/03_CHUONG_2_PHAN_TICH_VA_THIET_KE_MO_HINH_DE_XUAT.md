# CHƯƠNG 2. PHÂN TÍCH VÀ THIẾT KẾ MÔ HÌNH ĐỀ XUẤT

---

## 2.1. NGUYÊN LÝ PHÂN ĐOẠN THỰC THỂ TRONG YOLO26-SEG

### 2.1.1. Luồng dữ liệu qua Backbone, PAN-FPN và Proto Segment Head
Mô hình YOLO26-seg xử lý ảnh nội soi đầu vào kích thước chuẩn $3 \times 640 \times 640$ thông qua một luồng dữ liệu liên tục khép kín gồm ba thành phần kiến trúc chính:

1. **Mạng xương sống (Backbone)**:
   - Đảm nhiệm chức năng trích xuất đặc trưng phân cấp từ thấp đến cao. Ảnh đầu vào ban đầu đi qua tầng tích chập Stem để giảm độ phân giải không gian và tăng số kênh đặc trưng.
   - Qua các tầng tiếp theo, dữ liệu lần lượt được biến đổi qua các mức phân giải giảm dần với hệ số bước nhảy (stride):
     - Mức **P3** (stride 8): Bản đồ đặc trưng có kích thước $80 \times 80$, bảo tồn độ phân giải không gian cao và chi tiết kết cấu bề mặt cục bộ (edges, textures).
     - Mức **P4** (stride 16): Kích thước $40 \times 40$, đại diện cho mức đặc trưng ngữ nghĩa trung gian.
     - Mức **P5** (stride 32): Kích thước $20 \times 20$, chứa đựng thông tin ngữ nghĩa trừu tượng cao nhất và trường tiếp nhận lớn nhất của mạng.

2. **Mạng cổ dung hợp đa tỷ lệ (PAN-FPN Neck)**:
   - Sử dụng cơ chế kết hợp hai chiều: đường dẫn từ trên xuống (Top-down) đưa thông tin ngữ nghĩa phong phú từ mức P5 xuống P3 để bổ trợ cho việc định vị chi tiết; tiếp theo đường dẫn từ dưới lên (Bottom-up) truyền các đặc trưng vị trí không gian chính xác từ P3 ngược lên P5.
   - Quá trình này giúp mô hình nhận diện tốt cả những polyp kích thước siêu nhỏ (nhờ mức P3) lẫn các khối polyp lớn trải rộng (nhờ mức P5).

3. **Đầu phân đoạn nguyên mẫu (Proto Segment Head)**:
   - Áp dụng nguyên lý YOLACT tiên tiến: Nhánh Protonet lấy đặc trưng giàu chi tiết nhất từ mức P3 (kích thước $80 \times 80$) đi qua một chuỗi các lớp tích chập để tạo ra $k = 32$ mặt nạ nguyên mẫu (Prototype Masks) kích thước $\frac{H}{4} \times \frac{W}{4} = 160 \times 160$.
   - Đồng thời, tại mỗi vị trí dự đoán trên bản đồ đặc trưng, các nhánh tích chập song song sẽ dự đoán:
     - Tọa độ hộp bao bounding box $(x, y, w, h)$.
     - Điểm tin cậy phân loại lớp (Class Confidence).
     - Véc-tơ gồm $k = 32$ hệ số mặt nạ (Mask Coefficients) $C = [c_1, c_2, \dots, c_k]$.

> **[HÌNH ẢNH MINH HỌA — HÌNH 2.1]**  
> - **Đường dẫn tệp gốc**: `figures/yolo26_seg_baseline_architecture.png` (Sơ đồ kiến trúc YOLO26-seg gốc)  
> - **Tên tiêu đề chuẩn**: *Hình 2.1: Sơ đồ kiến trúc tổng thể của mô hình cơ sở YOLO26-seg*  
> 
> **[PHẦN NHẬN XÉT VÀ PHÂN TÍCH HỌC THUẬT]**:  
> - *Phân tích định lượng*: Sơ đồ mô tả tường minh luồng lan truyền xuôi từ ảnh đầu vào $3 \times 640 \times 640$ qua các khối tích chập trích xuất P3 ($80 \times 80 \times 128$), P4 ($40 \times 40 \times 256$), P5 ($20 \times 20 \times 512$), sau đó dung hợp qua mạng PAN-FPN và đưa vào nhánh Proto Head sinh ra 32 mặt nạ nguyên mẫu $160 \times 160$.  
> - *Ý nghĩa kỹ thuật & bệnh học*: Việc tách rời giữa việc sinh mặt nạ nguyên mẫu và tính toán hệ số tuyến tính giúp mạng giữ được tốc độ khung hình cực cao (> 50 FPS). Tuy nhiên, vì toàn bộ mạng chỉ sử dụng các phép tích chập chuẩn, các mặt nạ nguyên mẫu tại nhánh P3 rất dễ bị nhiễu bởi các nếp gấp ruột có màu sắc tương đồng nếu không có sự định hướng ngữ cảnh toàn cục mạnh mẽ từ tầng P5.

### 2.1.2. Hàm mất mát phân đoạn đa nhiệm (Multi-task Loss Function)
Quá trình tối ưu hóa mô hình YOLO26-seg trong huấn luyện được điều phối bởi hàm mất mát kết hợp đa nhiệm:
$$\mathcal{L}_{\text{total}} = \lambda_{\text{box}} \mathcal{L}_{\text{box}} + \lambda_{\text{cls}} \mathcal{L}_{\text{cls}} + \lambda_{\text{dfl}} \mathcal{L}_{\text{dfl}} + \lambda_{\text{mask}} \mathcal{L}_{\text{mask}}$$

Trong đó:
1. **Mất mát phân loại ($\mathcal{L}_{\text{cls}}$)**: Sử dụng hàm mất mát nhị phân Binary Cross-Entropy (BCE) có trọng số:
   $$\mathcal{L}_{\text{cls}} = -\sum_{i} \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]$$
2. **Mất mát hộp bao ($\mathcal{L}_{\text{box}}$ & $\mathcal{L}_{\text{dfl}}$)**: Sử dụng Complete IoU (CIoU) Loss kết hợp Distribution Focal Loss (DFL) để tối ưu đồng thời vị trí tâm, tỷ lệ khung hình và độ phân tán của biên hộp bao.
3. **Mất mát mặt nạ phân đoạn ($\mathcal{L}_{\text{mask}}$)**:
   Mặt nạ dự đoán $\hat{M}$ của từng thực thể được tạo ra qua phép nhân ma trận giữa hệ số mặt nạ $C$ và ma trận mặt nạ nguyên mẫu $P$:
   $$\hat{M} = \sigma \left( \sum_{j=1}^{k} c_j \cdot P_j \right)$$
   Mất mát mặt nạ được tính bằng hàm Binary Cross-Entropy trên từng điểm ảnh bên trong vùng hộp bao Ground Truth:
   $$\mathcal{L}_{\text{mask}} = -\frac{1}{\Omega} \sum_{(u, v) \in \Omega} \left[ M(u, v) \log \hat{M}(u, v) + (1 - M(u, v)) \log (1 - \hat{M}(u, v)) \right]$$
   với $\Omega$ là tập hợp các điểm ảnh thuộc vùng bao của tổn thương polyp.

---

## 2.2. PHÂN TÍCH TOÁN HỌC CƠ CHẾ QUÉT CHỌN LỌC SS2D TRONG VMAMBA

### 2.2.1. Phương trình không gian trạng thái liên tục và rời rạc hóa
Hệ thống không gian trạng thái tuyến tính liên tục (Continuous-time SSM) được định nghĩa bởi hệ phương trình vi phân:
$$h'(t) = \mathbf{A} h(t) + \mathbf{B} x(t)$$
$$y(t) = \mathbf{C} h(t)$$
với $x(t) \in \mathbb{R}$ là tín hiệu đầu vào, $h(t) \in \mathbb{R}^N$ là trạng thái tiềm ẩn bên trong, $y(t) \in \mathbb{R}$ là tín hiệu đầu ra; $\mathbf{A} \in \mathbb{R}^{N \times N}, \mathbf{B} \in \mathbb{R}^{N \times 1}, \mathbf{C} \in \mathbb{R}^{1 \times N}$.

Để áp dụng vào tính toán trên máy tính số với dữ liệu rời rạc, hệ liên tục trên được rời rạc hóa thông qua quy tắc xấp xỉ Zero-Order Hold (ZOH) với bước thời gian lấy mẫu $\mathbf{\Delta} \in \mathbb{R}_{>0}$:
$$\mathbf{\bar{A}} = \exp(\mathbf{\Delta} \mathbf{A})$$
$$\mathbf{\bar{B}} = (\mathbf{\Delta} \mathbf{A})^{-1} (\exp(\mathbf{\Delta} \mathbf{A}) - \mathbf{I}) \cdot (\mathbf{\Delta} \mathbf{B})$$

Hệ phương trình trạng thái rời rạc hóa có dạng:
$$h_t = \mathbf{\bar{A}} h_{t-1} + \mathbf{\bar{B}} x_t$$
$$y_t = \mathbf{C} h_t$$

Trong mô hình **Mamba (S6)**, tính chọn lọc thích ứng dữ liệu được hiện thực hóa bằng cách chiếu trực tiếp đầu vào $x_t$ để sinh ra các tham số động:
$$\mathbf{B}_t = \text{Linear}_B(x_t), \quad \mathbf{C}_t = \text{Linear}_C(x_t), \quad \mathbf{\Delta}_t = \text{softplus}(\text{Linear}_\Delta(x_t))$$
Nhờ đó, mô hình tự động điều chỉnh độ lớn bước nhảy $\mathbf{\Delta}_t$: Khi gặp vùng ảnh nhiễu (dịch nhầy, ánh lóa), $\mathbf{\Delta}_t$ tiệm cận 0 khiến $\mathbf{\bar{A}}_t \to \mathbf{I}$ và $\mathbf{\bar{B}}_t \to 0$, hệ thống giữ nguyên trạng thái cũ và bỏ qua thông tin nhiễu; khi gặp vùng ranh giới polyp, $\mathbf{\Delta}_t$ tăng cao giúp mô hình nhanh chóng cập nhật trạng thái mới.

### 2.2.2. Thuật toán quét 4 hướng giải quyết tính bất biến không gian 2D
Đối với bản đồ đặc trưng 2 chiều $\mathbf{X} \in \mathbb{R}^{H \times W \times C}$, thuật toán quét chọn lọc 2D (SS2D) trong VMamba thực hiện 3 bước toán học:

```text
[Bản đồ đặc trưng 2D X (H x W x C)]
                 │
  ┌──────────────┼──────────────┬──────────────┐
  ▼              ▼              ▼              ▼
Quét 1         Quét 2         Quét 3         Quét 4
(Trên-Trái)    (Dưới-Phải)    (Trên-Phải)    (Dưới-Trái)
  │              │              │              │
  ▼              ▼              ▼              ▼
SSM 1D         SSM 1D         SSM 1D         SSM 1D
  │              │              │              │
  └──────────────┼──────────────┴──────────────┘
                 ▼
[Phục hồi không gian 2D & Cộng tổng hợp nhất Y (H x W x C)]
```

1. **Phân rã quét 4 hướng (Scan Expand)**:
   $$\mathbf{X}^{(1)}_{i, j} = \mathbf{X}_{i, j} \quad (\text{Xuôi: Trái } \to \text{ Phải, Trên } \to \text{ Dưới})$$
   $$\mathbf{X}^{(2)}_{i, j} = \mathbf{X}_{H-1-i, W-1-j} \quad (\text{Ngược: Phải } \to \text{ Trái, Dưới } \to \text{ Trên})$$
   $$\mathbf{X}^{(3)}_{i, j} = \mathbf{X}_{j, i} \quad (\text{Dọc xuôi: Trên } \to \text{ Dưới, Trái } \to \text{ Phải})$$
   $$\mathbf{X}^{(4)}_{i, j} = \mathbf{X}_{W-1-j, H-1-i} \quad (\text{Dọc ngược: Dưới } \to \text{ Trên, Phải } \to \text{ Trái})$$
2. **Xử lý chọn lọc song song qua SSM**:
   $$\mathbf{Y}^{(k)} = \text{S6}(\mathbf{X}^{(k)}), \quad k \in \{1, 2, 3, 4\}$$
3. **Phục hồi và hợp nhất không gian (Scan Merge)**:
   $$\mathbf{Y} = \sum_{k=1}^{4} \text{Unfold}(\mathbf{Y}^{(k)})$$

Phép toán hợp nhất này đảm bảo mỗi vị trí điểm ảnh $(i, j)$ trên bản đồ đặc trưng đều thu nhận trọn vẹn thông tin ngữ cảnh từ toàn bộ các điểm ảnh xung quanh theo mọi hướng không gian mà không làm bùng nổ chi phí tính toán.

---

## 2.3. THIẾT KẾ KIẾN TRÚC TÍCH HỢP TOPOLOGY-SHAPE-AWARE VMAMBA (TSVM)

### 2.3.1. Động cơ và vị trí tích hợp: Tầng 10 (mức P5)
Một trong những quyết định thiết kế quan trọng nhất của đề tài là xác định **vị trí tối ưu** để tích hợp khối VMamba vào mô hình YOLO26-seg. Có ba phương án vị trí tiềm năng:
- *Phương án 1 (Tích hợp tại Stem/P3)*: Tại các tầng đầu, kích thước bản đồ đặc trưng rất lớn ($80 \times 80$ hoặc $160 \times 160$). Việc quét 4 hướng tại mức phân giải này sẽ gây gánh nặng tính toán rất lớn, làm sụt giảm nghiêm trọng tốc độ khung hình (FPS), không phù hợp cho suy luận thời gian thực.
- *Phương án 2 (Tích hợp thay thế toàn bộ Backbone)*: Làm thay đổi hoàn toàn phân phối trọng số tiền huấn luyện (pre-trained weights), đòi hỏi tập dữ liệu huấn luyện khổng lồ hàng triệu ảnh y tế vốn không khả thi.
- *Phương án 3 (Đề xuất của đề tài - Tích hợp tại Tầng 10 / Mức P5)*:
  Tầng 10 là vị trí xuất phát của mức đặc trưng sâu nhất (P5) trước khi đi vào mạng cổ dung hợp PAN-FPN. Tại đây, bản đồ đặc trưng có kích thước $20 \times 20$ với số kênh $C = 512$.
  - Kích thước không gian $20 \times 20$ ($N = 400$ vị trí) là kích thước lý tưởng: Đủ nhỏ để khối quét SS2D thực thi cực nhanh với độ trễ thấp, nhưng lại đủ lớn để đại diện cho toàn bộ ngữ nghĩa trừu tượng của khung hình nội soi.
  - Tích hợp tại đây giúp khối TSVM đóng vai trò như một **"bộ lọc ngữ cảnh toàn cục" (Global Context Refiner)**, giúp tinh chỉnh lại toàn bộ trường đặc trưng mức cao trước khi thông tin này được truyền ngược xuống dẫn đường cho các mức P4 và P3.

### 2.3.2. Cấu trúc chi tiết khối TSVM tại Tầng 10
Khối **Topology-Shape-aware VMamba (TSVM)** được xây dựng với cấu trúc kênh đôi (Dual-branch Topology Architecture):

```text
               Đầu vào Tầng 9 X (B x 512 x 20 x 20)
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
   Nhánh Residual                   Nhánh TSVM Core
(Identity Shortcut)               ┌───────────────┐
        │                         │  LayerNorm 2D │
        │                         └───────┬───────┘
        │                         ┌───────▼───────┐
        │                         │ Linear Proj   │
        │                         └───────┬───────┘
        │                         ┌───────▼───────┐
        │                         │ Conv 3x3 DW   │ (Topology Boundary)
        │                         └───────┬───────┘
        │                         ┌───────▼───────┐
        │                         │ Silu Activ.   │
        │                         └───────┬───────┘
        │                         ┌───────▼───────┐
        │                         │ Khối SS2D 4-D │ (Global Context)
        │                         └───────┬───────┘
        │                         ┌───────▼───────┐
        │                         │ Linear Out    │
        │                         └───────┬───────┘
        │                                 │
        └────────────────┬────────────────┘
                         ▼
                     Phép Cộng (Add)
                         │
                         ▼
             Đầu ra Tầng 10 (B x 512 x 20 x 20)
```

1. **Chuẩn hóa LayerNorm 2D**: Ổn định phân phối dữ liệu đầu vào, ngăn ngừa hiện tượng bùng nổ gradient trong quá trình lan truyền qua nhiều hướng quét.
2. **Nhánh tích chập sâu Depthwise Conv 3x3 (Nhận biết Topo ranh giới)**: Đảm nhiệm việc trích xuất đặc trưng hình thái đường biên cục bộ và duy trì tính liên tục của cấu trúc topo tổn thương.
3. **Cơ chế quét chọn lọc 4 hướng SS2D Core**: Mô hình hóa sự phụ thuộc không gian tầm xa, kết nối các điểm ảnh phân tán của tổn thương polyp với toàn bộ bối cảnh niêm mạc.
4. **Đường truyền tắt kết nối tàn dư (Residual Shortcut)**: Đảm bảo luồng gradient có thể truyền thẳng qua khối mà không bị tiêu biến, giúp mô hình dễ dàng hội tụ và kế thừa trọn vẹn sức mạnh của trọng số pre-trained.

> **[HÌNH ẢNH MINH HỌA — HÌNH 2.2]**  
> - **Đường dẫn tệp gốc**: `figures/tsvm_layer10_block_diagram.png` (Sơ đồ chi tiết khối TSVM tầng 10)  
> - **Tên tiêu đề chuẩn**: *Hình 2.2: Cấu trúc chi tiết khối Topology-Shape-aware VMamba (TSVM) tích hợp tại tầng 10 (mức P5)*  
> 
> **[PHẦN NHẬN XÉT VÀ PHÂN TÍCH HỌC THUẬT]**:  
> - *Phân tích định lượng*: Khối TSVM tại tầng 10 nhận đầu vào tensor kích thước $[B, 512, 20, 20]$. Sau khi qua nhánh chiếu tuyến tính và khối SS2D 4 hướng, tensor được cộng trực tiếp với tensor tàn dư đầu vào ban đầu thông qua phép cộng phần tử (element-wise addition), giữ nguyên kích thước $[B, 512, 20, 20]$ để tương thích hoàn toàn với đầu vào của tầng 11 tiếp theo.  
> - *Ý nghĩa kỹ thuật & bệnh học*: Việc kết hợp giữa phép tích chập Depthwise $3\times3$ và khối quét SS2D tạo nên cơ chế "kép": Depthwise Conv tập trung chụp lại độ cong của ranh giới polyp (Shape-aware), trong khi SS2D chịu trách nhiệm thẩm định xem cấu trúc đó có phù hợp với bối cảnh giải phẫu toàn đại tràng hay không (Topology-aware).

---

## 2.4. PHÂN TÍCH ƯU ĐIỂM, NHƯỢC ĐIỂM VÀ ĐIỀU KIỆN ÁP DỤNG THUẬT TOÁN ĐỀ XUẤT

Để đáp ứng đầy đủ tiêu chí đánh giá chuẩn đầu ra **CLO2.1** trong đề cương của TS. Phùng Thế Bảo, dưới đây là phân tích đa chiều về thuật toán đề xuất:

### 2.4.1. Ưu điểm nổi bật
1. **Nâng cao độ sắc nét và tính toàn vẹn của mặt nạ phân đoạn**: Nhờ trường tiếp nhận toàn cục của SS2D, mô hình TSVM khắc phục triệt để hiện tượng mặt nạ bị thủng lỗ, đứt gãy hoặc biến dạng khi gặp các ca polyp phẳng có độ tương phản ranh giới cực kỳ thấp.
2. **Tối ưu hóa chi phí tính toán so với Vision Transformer**: Độ phức tạp tính toán tuyến tính $O(N)$ cho phép khối TSVM chỉ làm tăng thêm **0.821 triệu tham số** (từ 11.434M lên 12.255M, tăng vỏn vẹn 7.18%) và chỉ tăng **0.32 GFLOPs** (từ 18.54 lên 18.86 GFLOPs, tăng 1.73%), thấp hơn rất nhiều so với việc chèn các khối Self-Attention của ViT (thường làm tăng 15–30 GFLOPs).
3. **Thu hẹp phương sai và ổn định quá trình hội tụ**: Thực nghiệm qua 10 seed chứng minh mô hình TSVM có độ lệch chuẩn nhỏ hơn mô hình Baseline, phản ánh tính ổn định học thuật vượt trội trước các biến động ngẫu nhiên của dữ liệu.

### 2.4.2. Nhược điểm và hạn chế
1. **Độ trễ suy luận gia tăng**: Mặc dù độ phức tạp lý thuyết là tuyến tính $O(N)$, thuật toán quét 4 hướng đòi hỏi các thao tác hoán vị bộ nhớ (Memory Permutation / Transpose) và phân mảnh chuỗi quét. Trên phần cứng GPU không hỗ trợ nhân tính toán chuyên dụng (Custom Triton/CUDA kernel cho Mamba), thời gian suy luận bị kéo dài đáng kể (từ 200.12 ms lên 821.27 ms trên môi trường thử nghiệm CPU/Kaggle tiêu chuẩn).
2. **Khó khăn trong việc tối ưu hóa song song phần cứng**: Các phép tích chập CNN thông thường được tối ưu hóa cực tốt trên thư viện cuDNN của Nvidia. Ngược lại, các phép toán trạng thái tuần tự của Mamba phụ thuộc nhiều vào băng thông bộ nhớ (SRAM bandwidth), đòi hỏi các kỹ thuật tối ưu hóa phần cứng sâu để đạt hiệu năng tối đa.

### 2.4.3. Điều kiện áp dụng thực tế
- **Yêu cầu phần cứng**: Phù hợp triển khai trên các hệ thống máy trạm có card đồ họa chuyên dụng hỗ trợ CUDA (như Nvidia RTX 3060, RTX 4090 hoặc dòng chuyên dụng T4, A100) để đảm bảo tốc độ suy luận mượt mà.
- **Kịch bản ứng dụng**:
  - *Kịch bản 1 (Hỗ trợ chẩn đoán thời gian thực qua Web)*: Triển khai mô hình trên máy chủ AI trung tâm có GPU, truyền nhận luồng ảnh qua API mạng nội bộ bệnh viện.
  - *Kịch bản 2 (Chẩn đoán xem lại sau nội soi - Post-procedure Review)*: Tải video/ảnh ca khám lên hệ thống để phần mềm tự động quét lại toàn bộ, lập báo cáo phân đoạn chi tiết về kích thước và diện tích polyp phục vụ hội chẩn lâm sàng.

---

## 2.5. TÓM TẮT CHƯƠNG 2
Chương 2 đã hoàn thành việc phân tích sâu sắc nguyên lý hoạt động của mô hình cơ sở YOLO26-seg; chứng minh nền tảng toán học của cơ chế quét chọn lọc không gian 2D (SS2D) trong VMamba; đặc tả thiết kế kiến trúc khối đề xuất TSVM tại vị trí chiến lược tầng 10; và phân tích toàn diện các ưu, nhược điểm cùng điều kiện áp dụng thực tế của thuật toán. Đây là tiền đề kỹ thuật trực tiếp để bước vào quy trình chuẩn bị dữ liệu và cài đặt thực nghiệm trong các chương tiếp theo.
