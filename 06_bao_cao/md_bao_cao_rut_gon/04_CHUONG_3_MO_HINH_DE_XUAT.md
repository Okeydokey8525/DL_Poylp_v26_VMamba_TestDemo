# CHƯƠNG 3. MÔ HÌNH ĐỀ XUẤT

> **Ghi chú soạn thảo (xóa khi nộp):** bản rút gọn, nén từ `md_bao_cao/04_CHUONG_3_MO_HINH_DE_XUAT.md` (tag git `ban_day_du_147`). Truy vết kích thước tensor, ví dụ phép quét từng bước, ước tính chi phí tầng 10 và hình cơ cấu tham số đã chuyển xuống Phụ lục F. Các mục 3.5, 3.6, 3.8 cũ (khởi tạo, mất mát, lưu FP32) gộp thành mục 3.5; Thuật toán 3.2 cũ (quy trình suy luận và huấn luyện, mục 3.7 cũ) chuyển xuống Phụ lục F thành Thuật toán PL.1.

Mô hình đề xuất giữ nguyên gần như toàn bộ YOLO26s-seg, chỉ thay khối C2PSA ở tầng 10 bằng khối mới C2TSVMamba. Bên trong khối có nhánh SS2D quét đặc trưng theo kiểu VMamba và nhánh hình dạng dùng tích chập có hướng, điều khiển nhánh SS2D qua một cổng. Thông số trong chương đọc từ mã nguồn đã dùng để huấn luyện (fork Ultralytics 8.4.127 [42] cùng mô-đun `topology_shape_vmamba.py`) và được kiểm tra bằng cách dựng mô hình rồi đếm tham số.

## 3.1. Ý tưởng và động cơ thiết kế

Để khoanh đúng polyp có biên mờ, màu gần niêm mạc và kích thước đa dạng, mô hình cần **ngữ cảnh rộng** (vùng đang xét là khối lồi lên hay chỉ là phản quang, nếp gấp) và **hình dạng của vùng** (trải theo hướng nào, đường bao ra sao). Trong YOLO26-seg, ngữ cảnh rộng ở cuối backbone do C2PSA đảm nhận bằng attention [43] trên P5 (20×20); thông tin không gian cục bộ của khối này chỉ đến từ một tích chập theo chiều sâu 3×3 làm mã hóa vị trí. Các công trình gần đây cho thấy biên và hình dạng là manh mối có ích cho polyp [27], [28], còn Mamba [23] và VMamba [7] đưa ra cách khác để thu ngữ cảnh toàn cục. Từ đó, đề tài thay C2PSA bằng một khối kết hợp quét chọn lọc kiểu VMamba với nhánh tích chập có hướng.

**Vì sao chọn tầng 10:**
1. Đây là khối attention duy nhất trong backbone, nên hai mô hình chỉ khác nhau ở cách tổng hợp ngữ cảnh tại một vị trí.
2. Chuỗi cần quét ngắn: P5 chỉ có 20×20 = 400 vị trí, mỗi vị trí đã mang thông tin ngữ nghĩa cao.
3. Đầu ra tầng 10 đi vào tầng 11 (phóng to xuống P4, P3) và tầng 21 (nhánh P5 đi lên), nên đặc trưng của khối mới có mặt ở cả ba mức của đầu Segment26.
4. Giao diện vào/ra 512×20×20 giữ nguyên, không phải sửa neck, head hay hàm mất mát.

**Phạm vi đóng góp.** SS2D là ý tưởng của VMamba [7], quét chọn lọc đến từ Mamba [23], tích chập theo chiều sâu, cổng sigmoid và nối tắt có hệ số là kỹ thuật quen thuộc. Đóng góp của đề tài là thiết kế cách ghép các thành phần này (trong đó nhánh hình dạng điều biến nhánh SS2D qua cổng), cài đặt lại SS2D bằng PyTorch thuần, tích hợp vào YOLO26s-seg cho phân đoạn polyp và đánh giá trên 20 seed. Khác với MambaPSA [30] (phát hiện vật thể, nhắm giảm chi phí, thêm BiViM ở neck) và Mamba YOLO [29] (thay nhiều khối), đề tài chỉ thay một tầng và bổ sung nhánh hình dạng.

## 3.2. Kiến trúc tổng thể

Mô hình gồm backbone (tầng 0–10, giảm từ 640×640 xuống 20×20, tầng 9 là SPPF, tầng 10 là vị trí thay đổi), neck (tầng 11–22, FPN [35] đi xuống và PAN [36] đi lên, cho P3 80×80, P4 40×40, P5 20×20) và đầu Segment26 (tầng 23) dự đoán hộp, điểm lớp, hệ số mặt nạ và sinh 32 mặt nạ mẫu 160×160 theo YOLACT [19] (Hình 3.1).

![Hình 3.1](../hinh/chung/vi/a01_kien_truc_tong_the.png)

*Hình 3.1. Kiến trúc YOLO26s-seg và vị trí khối C2TSVMamba (tầng 10). Kích thước tensor ghi theo dạng C×H×W, tính cho ảnh vào 640×640 với hệ số quy mô s. Tầng 22 (C3k2, attn=True) có PSABlock ở cả hai mô hình.*

Tệp cấu hình của mô hình đề xuất sao từ `yolo26-seg.yaml`, chỉ khác dòng khai báo tầng 10 (Bảng 3.1). Tầng 22 của cả hai mô hình vẫn có PSABlock, nên mô hình đề xuất chỉ thay attention ở tầng 10. Khi suy luận, cả hai chạy end-to-end: chỉ dùng đầu một-một, lấy tối đa 300 đối tượng, không NMS [20].

*Bảng 3.1. So sánh mô hình đối chứng và mô hình đề xuất*

| Tiêu chí | YOLO26s-seg (đối chứng) | YOLO26s-seg + C2TSVMamba (đề xuất) |
|---|---|---|
| Khối ở tầng 10 | C2PSA (1 PSABlock, 4 đầu attention) | C2TSVMamba (1 khối TSVMamba) |
| Vào/ra tầng 10 | 512×20×20 | 512×20×20 |
| Tham số tầng 10 | 990.976 | 1.811.201 |
| Tham số toàn mô hình | 11.434.463 | 12.254.688 (+7,17%) |
| Tầng 0–9 và 11–23 | Giống nhau | Giống nhau |
| Hàm mất mát, dữ liệu, siêu tham số | Giống nhau | Giống nhau |

## 3.3. Khối C2TSVMamba

### 3.3.1. Khung tách–xử lý–ghép

C2TSVMamba giữ khuôn ngoài của C2PSA: đặc trưng vào $x \in \mathbb{R}^{512\times20\times20}$ qua tích chập 1×1 (kèm BN, SiLU), chia đôi theo kênh thành $a$ và $b$ (mỗi phần 256 kênh); $a$ đi thẳng, $b$ qua khối TSVMamba; hai phần ghép lại rồi qua một tích chập 1×1 nữa:

$$ [a,\ b] = \mathrm{split}\big(\mathrm{Conv}_{1\times1}^{\,cv1}(x)\big), \qquad y = \mathrm{Conv}_{1\times1}^{\,cv2}\big([\,a \,\|\, \mathrm{TSVMamba}(b)\,]\big) \tag{3.1} $$

Cách chia đôi giống thiết kế CSP từ YOLOv4 [39], giúp giảm chi phí và giữ đường gradient ngắn. Với quy mô s, số khối TSVMamba thực tế là $\max(\mathrm{round}(2\times0{,}5),1) = 1$. Bên trong TSVMamba (Hình 3.2), $b$ đi đồng thời vào nhánh SS2D và nhánh hình dạng; nhánh hình dạng sinh bản đồ cổng $G$ điều biến đầu ra SS2D; hai nhánh được hợp nhất, tinh chỉnh qua FFN, nhân hệ số $\gamma$ rồi cộng trở lại vào $b$.

![Hình 3.2](../hinh/chung/vi/a02_khoi_c2tsvmamba.png)

*Hình 3.2. Cấu trúc khối C2TSVMamba. Khung nét đứt là khối TSVMamba. Đặc trưng bên trong khối có kích thước 256×20×20. Chi tiết nhánh SS2D ở Hình 3.4.*

### 3.3.2. Nhánh SS2D

Nhánh này cài đặt lại SS2D của VMamba [7]: trải bản đồ đặc trưng thành bốn chuỗi theo bốn thứ tự (Hình 3.3), cho mỗi chuỗi qua SSM chọn lọc rồi gộp lại, để mỗi vị trí nhận thông tin từ mọi phía. Ký hiệu: $D = 256$ kênh, $N = 16$ chiều trạng thái, $L = H\times W = 400$.

![Hình 3.3](../hinh/chung/vi/a03_quet_bon_huong.png)

*Hình 3.3. Bốn thứ tự duyệt của SS2D, minh họa trên lưới 4×4 (thực tế là 20×20, L = 400). Chấm tròn đánh dấu vị trí đầu chuỗi, ô vuông đánh dấu vị trí cuối chuỗi.*

![Hình 3.4](../hinh/chung/vi/a04_ss2d.png)

*Hình 3.4. Các bước bên trong nhánh SS2D như được cài đặt. Bước ③ đến ⑤ được thực hiện riêng cho từng hướng.*

Các bước tính (Hình 3.4):
1. **Chiếu vào:** tích chập 1×1 không bias nâng $b$ lên 512 kênh, chia thành $U$ (nội dung sẽ quét) và $Z$ (cổng ở bước cuối), mỗi phần 256 kênh.
2. **Trộn cục bộ:** $U$ qua tích chập theo chiều sâu 3×3 và SiLU được $\tilde U$, như tích chập ngắn trước SSM của Mamba [23].
3. **Trải phẳng bốn hướng:** theo hàng, hàng đảo ngược, cột, cột đảo ngược; gọi $\Pi_k$ là phép trải thứ $k$ và $u^{(k)} = \Pi_k(\tilde U)$.
4. **Sinh tham số phụ thuộc đầu vào** cho mỗi hướng, với $\Delta$ qua phép chiếu hạng thấp (hạng 16) rồi mở rộng lên 256 kênh:

$$ \Delta^{(k)}_t = \mathrm{softplus}\big(W^{(k)}_{\Delta}\, W^{(k)}_{x,\Delta}\, u^{(k)}_t + b^{(k)}_{\Delta}\big) \in \mathbb{R}^{D}, \quad B^{(k)}_t = W^{(k)}_{x,B}\, u^{(k)}_t \in \mathbb{R}^{N}, \quad C^{(k)}_t = W^{(k)}_{x,C}\, u^{(k)}_t \in \mathbb{R}^{N} \tag{3.2} $$

5. **Rời rạc hóa, quét và đọc ra**, với $A^{(k)} = -\exp(A^{(k)}_{\log})$ dạng chéo luôn âm theo S4D [44]:

$$ \bar A^{(k)}_{t,d,n} = \exp\!\Big(\mathrm{clip}\big(\Delta^{(k)}_{t,d}\, A^{(k)}_{d,n},\ -50,\ 0\big)\Big) \tag{3.3} $$

$$ h^{(k)}_{t,d,n} = \bar A^{(k)}_{t,d,n}\, h^{(k)}_{t-1,d,n} + \Delta^{(k)}_{t,d}\, B^{(k)}_{t,n}\, u^{(k)}_{t,d}, \qquad h^{(k)}_{0} = 0 \tag{3.4} $$

$$ y^{(k)}_{t,d} = \sum_{n=1}^{N} C^{(k)}_{t,n}\, h^{(k)}_{t,d,n} \tag{3.5} $$

6. **Gộp bốn hướng:** đảo phép trải phẳng của từng $y^{(k)}$ về lưới 20×20 rồi cộng lại.
7. **Cổng và chiếu ra:**

$$ F_M = W_{\text{out}} * \Big( \big(\textstyle\sum_{k=1}^{4} \Pi_k^{-1}(y^{(k)})\big) \odot \mathrm{SiLU}(Z) \Big) \in \mathbb{R}^{256\times20\times20} \tag{3.6} $$

Vì $\Delta A \le 0$ nên $\bar A \in (0, 1]$: trạng thái cũ luôn mờ dần với tốc độ do $\Delta$ quyết định. Số hạng đầu vào dùng xấp xỉ $\bar B \approx \Delta B$ như Mamba [23]; phép cắt clip chỉ có trong bản cài đặt này để tránh lấy exp của số âm quá lớn; (3.4) được giải bằng phép quét song song (mục 3.4). Mỗi hướng có tham số chiếu và $A_{\log}$ riêng. So với VMamba gốc, bản cài đặt không có hạng tử nhảy $D\cdot u$ (thay bằng nối tắt có hệ số $\gamma$ ở ngoài khối), không có LayerNorm sau khi gộp, vẫn giữ cổng $\mathrm{SiLU}(Z)$, khởi tạo phép chiếu $\Delta$ theo mặc định PyTorch và không dùng kernel CUDA tối ưu.

### 3.3.3. Nhánh hình dạng

Nhánh hình dạng chỉ gồm tích chập, cung cấp thông tin hình học của vùng đặc trưng: trải theo hướng nào, rộng hẹp ra sao. Ở mức P5, một nhân 1×5 đã phủ khoảng 160 pixel ảnh gốc, nên nhánh này nắm hình dạng ở mức vùng lớn, không phải chi tiết biên từng pixel; đề tài chưa có thí nghiệm riêng kiểm chứng nhánh thực sự học được hình dạng.

**ShapeAwareBranch** chạy song song hai tích chập theo chiều sâu 3×3 và 5×5 (kèm BN, SiLU), ghép lại và trộn kênh bằng tích chập 1×1:

$$ S_{\text{shape}} = \mathrm{Conv}_{1\times1}\big(\big[\mathrm{DW}_{3\times3}(b) \,\|\, \mathrm{DW}_{5\times5}(b)\big]\big) \tag{3.7} $$

**DirectionalShapeExtractor** chạy song song ba tích chập theo chiều sâu (dải ngang 1×5, dải dọc 5×1, 3×3), tính thêm độ lớn tổng hợp $S_{grad}$, rồi trộn hai lần bằng tích chập 1×1:

$$ S_h = \mathrm{DW}_{1\times5}(S_{\text{shape}}),\quad S_v = \mathrm{DW}_{5\times1}(S_{\text{shape}}),\quad S_{loc} = \mathrm{DW}_{3\times3}(S_{\text{shape}}),\quad S_{grad} = \sqrt{S_h^2 + S_v^2 + 10^{-6}} \tag{3.8} $$

$$ S_{topo} = \mathrm{Conv}_{1\times1}\big([S_h \,\|\, S_v \,\|\, S_{loc} \,\|\, S_{grad}]\big), \qquad S = \mathrm{Conv}_{1\times1}\big([S_{\text{shape}} \,\|\, S_{topo}]\big) \tag{3.9} $$

$S_{grad}$ có dạng giống độ lớn gradient trong xử lý ảnh [52], nhưng $S_h$, $S_v$ là đáp ứng của các nhân học được, nên nó không phải gradient ảnh như bộ lọc Sobel mà là một đặc trưng ít phụ thuộc hướng. Đầu ra $S$ có kích thước 256×20×20.

### 3.3.4. Cổng

Từ $S$, một tích chập 1×1 có bias và hàm sigmoid sinh bản đồ cổng $G$ điều biến đầu ra SS2D:

$$ G = \sigma\big(W_g * S + b_g\big) \in (0,1)^{256\times20\times20}, \qquad F'_M = F_M \odot (1 + G) \tag{3.10} $$

Hệ số $(1 + G)$ luôn trong khoảng (1, 2): cổng chỉ khuếch đại, không tắt hẳn vị trí nào, tránh mất tín hiệu SS2D lúc đầu huấn luyện. Vì sau bước hợp nhất còn một lớp BN, tác dụng thực tế là đổi tầm quan trọng tương đối giữa các vị trí và kênh. Thông tin đi một chiều: nhánh hình dạng điều khiển nhánh SS2D. Chữ "topology" trong tên `TopologyShapeGate` chỉ là ý đồ thiết kế; đề tài không dùng hàm mất mát hay ràng buộc tô-pô nào.

### 3.3.5. Hợp nhất, mạng truyền thẳng và nối tắt có hệ số

Ghép $F'_M$ với $S$, dùng tích chập 1×1 (kèm BN, SiLU) đưa 512 về 256 kênh, qua FFN gồm hai tích chập 1×1 (256 → 512 → 256), nhân hệ số $\gamma$ và cộng vào $b$:

$$ F = \mathrm{FFN}\big(\mathrm{Conv}^{\,fuse}_{1\times1}([F'_M \,\|\, S])\big), \qquad b' = b + \gamma\, F, \qquad \gamma_0 = 10^{-3} \tag{3.11} $$

$\gamma$ là số vô hướng khởi tạo 0,001, nên lúc đầu khối gần như không đổi đầu vào ($b' \approx b$) và đóng góp tăng dần trong huấn luyện, tránh xáo trộn các tầng đã tiền huấn luyện. Gộp lại:

$$ \mathrm{TSVMamba}(b) = b + \gamma\cdot\mathrm{FFN}\Big(\mathrm{Conv}^{\,fuse}_{1\times1}\big(\big[\,\mathrm{SS2D}(b)\odot(1+G(b)) \,\|\, S(b)\,\big]\big)\Big) \tag{3.12} $$

### 3.3.6. Số tham số

*Bảng 3.2. Số tham số của tầng 10 (quy mô s)*

| Thành phần | Số tham số | Tỉ lệ trong tầng 10 |
|---|---:|---:|
| cv1 + cv2 (khung C2) | 526.336 | 29,1% |
| SS2D | 281.856 | 15,6% |
| ShapeAwareBranch | 141.312 | 7,8% |
| DirectionalShapeExtractor | 400.640 | 22,1% |
| Cổng | 65.792 | 3,6% |
| fuse | 131.584 | 7,3% |
| FFN | 263.680 | 14,6% |
| $\gamma$ | 1 | ~0% |
| **Tổng C2TSVMamba** | **1.811.201** | 100% |
| C2PSA của mô hình đối chứng | 990.976 | |

Nhánh hình dạng cộng cổng chiếm khoảng 33,5% số tham số của tầng, nhiều hơn chính SS2D; phần tăng thêm so với C2PSA (820.225 tham số) vì thế không chỉ đến từ SS2D. Bảng truy vết kích thước tensor qua từng bước và hình cơ cấu tham số ở Phụ lục F.

## 3.4. Thuật toán quét kết hợp song song

Xét một kênh $d$ và một chiều trạng thái $n$, (3.4) là truy hồi tuyến tính bậc một

$$ h_t = a_t\, h_{t-1} + b_t, \qquad h_0 = 0, \qquad t = 1, \dots, L \tag{3.13} $$

với $a_t = \bar A_t$, $b_t = \Delta_t B_t u_t$. Tính tuần tự cần khoảng 400 lượt phép toán nhỏ nối tiếp, chậm trên GPU dù $4 \times 256 \times 16 = 16.384$ chuỗi chạy song song với nhau. Coi mỗi vị trí là phép biến đổi affine $h \mapsto a_t h + b_t$, hai phép liên tiếp hợp thành một phép cùng dạng:

$$ (a_1, b_1) \circ (a_2, b_2) = (a_2 a_1,\ a_2 b_1 + b_2) \tag{3.14} $$

Toán tử này có tính kết hợp, nên $h_t$ là thành phần thứ hai của tích tiền tố $(a_1,b_1)\circ\cdots\circ(a_t,b_t)$ và tính được bằng quét song song [45]. Mã dùng biến thể Hillis–Steele [46] (Thuật toán 3.1): ở vòng $j$, mỗi vị trí $t$ kết hợp với vị trí $t - 2^{j}$; sau $\lceil\log_2 L\rceil$ vòng, mỗi vị trí đã gom đủ các phần tử đứng trước.

*Thuật toán 3.1. Quét kết hợp song song (theo hàm `parallel_associative_scan`)*

```
Đầu vào : a[1..L], b[1..L]   (xử lý cùng lúc cho mọi kênh d, chiều trạng thái n, hướng k)
Đầu ra  : h[1..L] với h[t] = a[t]·h[t-1] + b[t], h[0] = 0

1. K ← ⌈log2 L⌉ ;  P ← 2^K
2. Đệm a đến độ dài P bằng giá trị 1, đệm b đến độ dài P bằng giá trị 0
   (cặp (1, 0) là phần tử đơn vị của phép ∘, nên không làm sai kết quả)
3. step ← 1
4. while step < P:
5.     với mọi t > step, đồng thời:
6.         b[t] ← a[t]·b[t − step] + b[t]
7.         a[t] ← a[t]·a[t − step]
8.     (các vị trí t ≤ step giữ nguyên)
9.     step ← 2·step
10. return b[1..L]
```

Với $L = 400$, mã đệm lên $P = 512$ và chạy $K = 9$ vòng; dòng 6 và 7 tính cùng lúc bằng cắt lát tensor rồi ghép lại (`torch.cat`). Ví dụ từng vòng trên chuỗi $L = 4$ ở Phụ lục F.

**Độ phức tạp.** Số bước phải chờ nhau giảm từ 399 xuống 9 vòng, nhưng tổng công việc là $O(L\log L)$: mỗi chuỗi cần 4.097 phép kết hợp so với 399 khi tính tuần tự, mỗi ảnh khoảng 67 triệu phép kết hợp. Vì vậy bản cài đặt không có độ phức tạp tuyến tính như Mamba gốc, vốn đạt được nhờ biến thể Blelloch [45] và kernel CUDA gộp phép toán [23]. Bù lại, mã chỉ cần PyTorch, chạy được trên CPU lẫn GPU và cho kết quả tất định. Ở $L = 400$, attention của C2PSA với chi phí $O(L^2)$ vẫn còn rẻ; lợi thế của SSM chỉ thể hiện khi chuỗi rất dài.

**Chi phí tầng 10.** Ước tính tay (Phụ lục F) cho thấy phần xử lý chính của TSVMamba tốn khoảng 511 triệu MAC, gấp khoảng hai lần PSABlock (khoảng 246 triệu), chủ yếu ở nhánh hình dạng và FFN chứ không ở SS2D; với cả mô hình, số phép tính chỉ tăng khoảng 1–2%. Độ trễ thì tăng nhiều hơn hẳn (Chương 6), nhiều khả năng do chi phí bộ nhớ của phép quét: mỗi vòng tạo tensor trung gian 256×16×512 cho từng hướng và ghép lại bằng `torch.cat`. Giả thuyết này chưa được kiểm chứng bằng profiler.

## 3.5. Huấn luyện và lưu trọng số

### 3.5.1. Khởi tạo và học chuyển giao

Cả hai mô hình xuất phát từ `yolo26s-seg.pt` tiền huấn luyện trên COCO [41]; Ultralytics chỉ chép tensor trùng cả tên lẫn kích thước. Ở mô hình đề xuất:
- **Tầng 0–9 và 11–23** nhận trọng số giống hệt mô hình đối chứng (trừ các lớp đầu ra phụ thuộc số lớp, không chép được ở cả hai mô hình).
- **Tầng 10:** 12 trong 58 tensor (cv1, cv2, FFN; 790.016 tham số) trùng tên và kích thước với C2PSA nên được kế thừa; FFN kế thừa chỉ vì trùng tên, không phải tái sử dụng có chủ đích. 1.021.185 tham số còn lại (SS2D, nhánh hình dạng, cổng, fuse, $\gamma$) khởi tạo mới: $A = -(1, 2, \dots, 16)$ theo S4D-Real [44], các lớp khác theo mặc định, $\gamma = 0{,}001$.

Vì $\gamma$ nhỏ, ở những bước đầu tầng 10 hoạt động gần như $\mathrm{cv2}([a \,\|\, b])$: mô hình bắt đầu khi tầng 10 chưa có cơ chế tổng hợp ngữ cảnh, rồi học dần đóng góp của khối mới.

### 3.5.2. Hàm mất mát và chiến lược huấn luyện

Hai mô hình dùng chung hàm mất mát của YOLO26-seg, siêu tham số và danh sách seed, nên khác biệt có hệ thống chỉ quy được cho tầng 10. Tổng mất mát là tổ hợp có trọng số của đầu một-nhiều và đầu một-một [6], [20]:

$$ \mathcal{L} = \alpha(e)\,\mathcal{L}_{\text{o2m}} + \big(1-\alpha(e)\big)\,\mathcal{L}_{\text{o2o}}, \qquad \alpha(e) = 0{,}1 + 0{,}7\cdot\max\!\Big(1 - \frac{e}{E-1},\ 0\Big) \tag{3.15} $$

Với $E = 100$, trọng số đầu một-nhiều giảm từ 0,8 xuống 0,1. Điểm neo dương chọn theo độ đo căn chỉnh của TOOD [37], $t = s^{0{,}5}\cdot u^{6}$ ($s$ là điểm lớp, $u$ là IoU): đầu một-nhiều lấy 10 điểm, đầu một-một chọn 7 ứng viên rồi giữ 1; quy tắc STAL nới cạnh vật nhỏ hơn 8 pixel lên 16 pixel [6].

*Bảng 3.3. Các thành phần mất mát của YOLO26-seg (theo đúng nhánh mã đã chạy)*

| Thành phần | Nội dung | Hệ số |
|---|---|---:|
| Hộp (box) | $1 - \mathrm{CIoU}$ [38], có trọng số theo điểm căn chỉnh | 7,5 |
| L1 | Sai số tuyệt đối trên bốn khoảng cách tới biên hộp. Thay cho DFL vì `reg_max = 1` [6] | 1,5 |
| Lớp (cls) | Entropy chéo nhị phân, dùng nhãn mềm từ bộ gán nhãn | 0,5 |
| Mặt nạ (seg) | Entropy chéo nhị phân theo pixel giữa mặt nạ dự đoán và mặt nạ thật, chỉ tính trong hộp thật | 7,5 |
| Ngữ nghĩa (sem) | 0,5·BCE + 0,5·Dice trên nhánh phân đoạn ngữ nghĩa phụ của Proto26. Chỉ chạy khi huấn luyện | 7,5 |

Vì nhánh ngữ nghĩa phụ chỉ chạy khi huấn luyện, cột `val/sem_loss` trong nhật ký luôn bằng 0, đúng hành vi của mã. Bài báo YOLO26 dùng MuSGD [6], còn đề tài dùng AdamW [40] cho cả hai mô hình: tốc độ học 0,001, suy giảm trọng số 0,0005, FP32 hoàn toàn (`amp=False`), 100 epoch, lô 8 ảnh, chế độ tất định với seed cố định (chi tiết ở Chương 5). Quy trình suy luận và huấn luyện giống các bước ở mục 2.4.2, chỉ khác tầng 10 tính theo (3.1) và (3.12); Thuật toán PL.1 (Phụ lục F) viết đầy đủ hai quy trình này. Đề tài không thêm hàm mất mát nào về biên hay tô-pô.

### 3.5.3. Lưu trọng số ở dạng FP32

Mặc định Ultralytics chuyển mô hình sang FP16 trước khi lưu `best.pt`. Ở seed 5, `running_mean` của lớp BN trong tích chập fuse ở tầng 10 lên tới khoảng 1,5 triệu, vượt giới hạn 65.504 của FP16, nên checkpoint bị tràn số và suy luận sai dù huấn luyện ở FP32 vẫn bình thường. Đề tài sửa mã lưu (hàm lưu mô hình, MultiTrainer, `strip_optimizer`) để giữ FP32 bằng `.float()` thay cho `.half()`, và bỏ đoạn tự thay tensor không hữu hạn trong bản EMA để lỗi được báo ngay. Huấn luyện lại các lượt TSVM bằng mã đã sửa, so sánh `results.csv` trên 20 seed: 44.000 ô số liệu giống hệt, 2.000 ô khác đều thuộc cột thời gian. Như vậy bản sửa chỉ làm checkpoint được lưu đúng; tên "TSVM FP32" chỉ cách lưu này. Nguyên nhân có thể nằm ở thiết kế: SS2D không có lớp chuẩn hóa đầu ra và $F_M$ còn nhân thêm $(1+G)$ trước fuse, nên biên độ trước lớp BN của fuse không bị chặn. Đây mới là giả thuyết.

## 3.6. Ưu điểm và hạn chế của mô hình đề xuất

**Ưu điểm:**
- **Thay đổi tối thiểu:** chỉ một tầng khác, giao diện giữ nguyên, khác biệt quy được cho khối mới.
- **Ngữ cảnh toàn cục có chọn lọc:** SS2D quét bốn hướng, mức ghi nhớ điều chỉnh theo nội dung qua $\Delta$, $B$, $C$.
- **Thông tin hình dạng dẫn dắt đặc trưng toàn cục:** nhánh tích chập có hướng (1×5, 5×1) cùng cổng $(1+G)$, trong khi C2PSA chỉ có tích chập 3×3 làm mã hóa vị trí.
- **Khởi đầu ổn định:** $\gamma = 0{,}001$ cùng việc kế thừa cv1, cv2, FFN giúp bắt đầu gần mô hình gốc.
- **Dễ chạy:** chỉ cần PyTorch, không biên dịch kernel CUDA, chạy được trên CPU, kết quả tất định.

**Hạn chế:**
- **Chi phí tăng:** tham số toàn mô hình +7,17%, checkpoint lớn hơn do lưu FP32, độ trễ CPU khoảng 2,1 lần, thời gian huấn luyện mỗi lượt từ khoảng 2,3 giờ lên 4,7 giờ.
- **Phép quét chưa tối ưu:** tổng công việc $O(L\log L)$, nhiều tensor trung gian; ở P5 ($L = 400$) lợi thế của SSM chưa thể hiện.
- **Khác bản VMamba gốc:** thiếu hạng tử $D$, thiếu LayerNorm đầu ra, khởi tạo $\Delta$ mặc định, có thể liên quan đến sự cố số học ở mục 3.5.3.
- **Tên gọi chưa có bằng chứng:** đo lỗi Betti trên 20 seed, TSVM chỉ nhích hơn mô hình gốc, không có ý nghĩa thống kê (Chương 6).

## 3.7. Các chế độ tách thành phần

Mô-đun TSVMamba có tham số `mode` để bật hoặc tắt từng nhánh (Bảng 3.4). Số tham số tầng 10 của cả bốn chế độ được đếm lại từ checkpoint của các lượt huấn luyện tách thành phần. Mọi lượt chính của TSVM dùng chế độ đầy đủ; ba chế độ còn lại được huấn luyện với seed 0–4 để ghép cặp với mô hình đầy đủ, kết quả ở mục 6.6. Với chỉ 5 seed, đóng góp của từng nhánh mới ở mức thăm dò; ngoài ra, vì các chế độ chênh nhau tới khoảng 740 nghìn tham số, so sánh này chưa tách được phần do cấu trúc với phần do thêm tham số.

*Bảng 3.4. Bốn chế độ của khối TSVMamba*

| Chế độ | Công thức khối | Tham số tầng 10 |
|---|---|---:|
| `topology_shape_vmamba` (đầy đủ, dùng trong đề tài) | (3.12) | 1.811.201 |
| `shape_vmamba_no_guidance` | $b + \gamma\cdot\mathrm{FFN}(\mathrm{fuse}([\mathrm{SS2D}(b) \,\|\, S]))$, bỏ cổng | 1.745.409 |
| `shape_only` | $b + \gamma\cdot\mathrm{FFN}(S)$, bỏ SS2D | 1.331.969 |
| `vmamba_only` | $b + \gamma\cdot\mathrm{FFN}(\mathrm{SS2D}(b))$, bỏ nhánh hình dạng | 1.071.873 |

## 3.8. Kết chương

Mô hình đề xuất chỉ thay C2PSA ở tầng 10 bằng C2TSVMamba cùng giao diện 512×20×20, gồm nhánh SS2D bốn hướng, nhánh hình dạng có hướng với cổng $(1+G)$, và nối tắt có hệ số $\gamma$ nhỏ. Phép truy hồi được giải bằng quét song song Hillis–Steele (9 vòng, tổng công việc $O(L\log L)$). Khối mới thêm 820.225 tham số; số phép tính toàn mô hình chỉ tăng khoảng 1–2% nhưng độ trễ tăng đáng kể do cách cài đặt phép quét. Chương 6 đánh giá chi phí này đổi lại được bao nhiêu về chất lượng phân đoạn.
