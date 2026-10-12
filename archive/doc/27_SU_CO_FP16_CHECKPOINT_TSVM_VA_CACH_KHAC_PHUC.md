# 27. Sự cố checkpoint FP16 làm sụp TSVM và cách khắc phục

> **Đề tài:** Tích hợp VMamba vào YOLO26-seg phân đoạn polyp (Kvasir BG20)
> **Phạm vi:** TSVM (`yolo26-seg-TopologyShapeVMamba.yaml`, seed 0–20) và Baseline YOLO26s-seg (seed 0–22)
> **Ngày lập:** 12/10/2026
> **Thay thế:** giải thích "do hàm `fuse()`" trong tài liệu 17. Giải thích đó **không đúng** (xem mục 6).
> **Ký hiệu độ tin cậy:** *(Đã xác nhận)* = kiểm tra trực tiếp trên code/CSV/log/ảnh; *(Suy luận)* = lập luận từ số liệu; *(Chưa xác minh)* = chưa có bằng chứng trong repo.

---

## 0. Tóm tắt

1. Khi huấn luyện, mọi seed TSVM đều đạt Mask mAP50 khoảng 0,89–0,93 (`results.csv`). Nhưng ở nhiều seed, khi đánh giá lại file `best.pt` đã lưu, kết quả bị sụp. Seed 5 về 0, seed 8 còn 0,03, seed 0 còn 0,63.
2. **Nguyên nhân:** Ultralytics lưu checkpoint ở **FP16**, mà FP16 chỉ biểu diễn được tối đa **65.504**. Trong khối TSVM ở tầng 10, giá trị đi vào lớp BatchNorm `model.10.m.0.fuse.bn` lên tới hàng triệu. Khi lưu, `running_mean`/`running_var` bị cắt về 65.504, nên lúc suy luận lớp BN tính sai và mô hình sụp.
3. **Vì sao số lại lớn như vậy:** SS2D là một chuỗi phép nhân của chính đầu vào (u·B·C·z) và không có lớp chuẩn hóa ở đầu ra. Lớp BN phía sau che mất độ lớn, nên trọng số trôi tự do. Seed nào trôi xa sẽ bị khuếch đại lên hàng nghìn lần.
4. **Đây là lỗi lưu trữ, không phải lỗi huấn luyện.** `results.csv` được tính ở FP32 nên vẫn đúng. Chỉ cần tính lại thống kê của một lớp BN, seed 5 hồi phục từ 0 lên 0,9099, khớp với 0,9096 lúc train.
5. **Baseline không bị ảnh hưởng**, dù dùng cùng code lưu FP16. Cả 23/23 seed khớp với lúc train, sai lệch ≤ 0,001.
6. **Khắc phục:** (A) lưu checkpoint FP32 và dừng ngay khi có NaN/Inf; (B) suy luận TSVM ở FP32; (C) về lâu dài, thêm LayerNorm vào đầu ra SS2D như VMamba gốc.

---

## 1. Hiện tượng

### 1.1. Cách kiểm tra

- Ultralytics chọn `best.pt` là epoch có **fitness = Box mAP50-95 + Mask mAP50-95** lớn nhất (`utils/metrics.py:1371`). Đó là số ghi trong `results.csv`, tính trên mô hình EMA **FP32 trong RAM**.
- Sau khi train xong, Ultralytics validate lại `best.pt` **đã lưu FP16** và vẽ `MaskPR_curve.png`. Chú thích "all classes X mAP@0.5" trong ảnh chính là kết quả của file đã lưu.
- So hai số này sẽ biết checkpoint có bị hỏng khi lưu hay không. Phương pháp đã được thử trên seed 0: ảnh ghi 0,630, khớp với log Kaggle (`kvasir-yolo26s-seg-topology-shape-awar.log`, dòng 584: Mask mAP50 = 0,63). *(Đã xác nhận)*

### 1.2. TSVM: 21 seed

| Seed | Mask mAP50 lúc train (FP32) | Mask mAP50 của `best.pt` (FP16) | Chênh | Đánh giá |
|---|---|---|---|---|
| 0 | 0,9040 | 0,630 | −0,274 | **Sụp** |
| 1 | 0,9115 | 0,911 | −0,001 | Bình thường |
| 2 | 0,9003 | 0,899 | −0,001 | Bình thường |
| 3 | 0,9164 | 0,917 | +0,001 | Bình thường |
| 4 | 0,9024 | 0,899 | −0,003 | Bình thường |
| 5 | 0,9096 | **0,0000** ¹ | −0,910 | **Sụp hoàn toàn** |
| 6 | 0,9061 | 0,908 | +0,002 | Bình thường |
| 7 | 0,8940 | 0,885 | −0,009 | Hỏng nhẹ |
| 8 | 0,9150 | 0,033 | −0,882 | **Sụp** |
| 9 | 0,9123 | 0,918 | +0,006 | Bình thường |
| 10 | 0,9103 | 0,113 | −0,797 | **Sụp** |
| 11 | 0,9097 | 0,909 | −0,001 | Bình thường |
| 12 | 0,8949 | 0,768 | −0,127 | **Sụp** |
| 13 | 0,9311 | 0,931 | 0,000 | Bình thường |
| 14 | 0,9064 | 0,046 | −0,860 | **Sụp** |
| 15 | 0,9143 | 0,905 | −0,009 | Hỏng nhẹ |
| 16 | 0,9121 | 0,687 | −0,225 | **Sụp** |
| 17 | 0,9219 | 0,867 | −0,055 | Hỏng vừa |
| 18 | 0,8935 | 0,892 | −0,002 | Bình thường |
| 19 | 0,8967 | 0,643 | −0,254 | **Sụp** |
| 20 | 0,9081 | 0,901 | −0,007 | Bình thường |

*(Đã xác nhận: `results.csv` và `MaskPR_curve.png` trong `archive/Ket_Qua_V2/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/`)*

¹ Giá trị 0,0000 của seed 5 lấy từ lần đánh giá lại `best.pt` (`../DL_Poylp_v26_VMamba_TestDemo_V2/07_doi_chieu_lich_su/ket_qua/tong_hop_10_seed.csv`). Ảnh `MaskPR_curve.png` của seed 5 trong `KetQua_Nen` ghi 0,910 nhưng **có dấu hiệu bị vẽ lại**: đường cong trơn như hàm toán học, kích thước 2100×1500 khác các seed khác (2250×1500), và các cặp ảnh `Box*_curve.png`/`Mask*_curve.png` trùng md5. **Không dùng các ảnh này của seed 5.** *(Dấu hiệu: đã xác nhận. "Vẽ lại": suy luận)*

**Tổng cộng có 7 seed sụp nặng (0, 5, 8, 10, 14, 16, 19), 2 seed sụp vừa (12, 17) và 2 seed hỏng nhẹ (7, 15).** Tài liệu cũ chỉ nhắc seed 0, 5, 8.

### 1.3. Baseline YOLO26s-seg: 23 seed

Cả 23 seed (s0–s22) có mAP50 trong ảnh PR khớp `results.csv`, chênh tối đa **±0,001** (chỉ là sai số làm tròn). Cả 23 seed đều dùng `amp: false`, `results.csv` đủ 100 dòng, không có NaN/Inf, và ảnh không có dấu hiệu bị vẽ lại. *(Đã xác nhận)*

---

## 2. Nguyên nhân trực tiếp: code lưu FP16

Hai fork `archive/ultralytics/` (Baseline) và `archive/ultralytics_Topology-Shape-aware VMamba/` (TSVM) cùng là Ultralytics 8.4.127. Phần lưu checkpoint **giống hệt nhau**:

| Tệp | Dòng | Việc làm |
|---|---|---|
| `engine/trainer.py` | 728 | `ema = deepcopy(ema).half()`: đổi EMA sang FP16 khi lưu mỗi epoch |
| `engine/trainer.py` | 734 | `torch.nan_to_num_(v)`: **lặng lẽ** thay `inf` bằng 65.504, nên không có cảnh báo nào |
| `utils/torch_utils.py` | 828 | `strip_optimizer`: `x["model"].half()` khi ghi `best.pt`/`last.pt` cuối cùng |

- `amp=False` **không cứu được**, vì tham số này chỉ ảnh hưởng tới tính toán lúc train, không ảnh hưởng tới bước lưu file. *(Đã xác nhận)*
- Có thể nhận ra từ kích thước file: `best.pt` khoảng **25 MB** là FP16 (12,25 triệu tham số × 2 byte). Nếu là FP32 thì phải khoảng **49 MB**. *(Suy luận từ số tham số)*

---

## 3. Nguyên nhân gốc: SS2D khuếch đại giá trị kích hoạt

### 3.1. Vị trí lớp bị hỏng

```
Tầng 10: C2TSVMamba ─ TSVMamba:
    f_m  = SS2D(x)                      ← nguồn số lớn
    s    = nhánh shape/topology(x)      ← luôn nhỏ (~6–10)
    f    = f_m · (1 + gate),  gate ∈ [0,1]
    fuse = Conv1x1 → BatchNorm → SiLU   ← model.10.m.0.fuse.bn (lớp bị cắt)
    out  = x + γ · FFN(fuse)
```

Chữ `fuse` ở đây là **tên của lớp Conv**, không liên quan tới hàm `model.fuse()`.

### 3.2. SS2D là một chuỗi phép nhân

Code ở `nn/modules/topology_shape_vmamba.py:144-209`:

| Bước | Công thức | Bậc theo đầu vào u |
|---|---|---|
| ① | `u, z = in_proj(x)`; `u = SiLU(conv2d(u))` | 1 |
| ② | `B = W_B·u`, `C = W_C·u`, `dt = softplus(W_dt·u)` (tham số "selective" sinh từ chính u) | 1 |
| ③ | `b = dt · B · u` | khoảng 2 |
| ④ | `h_t = a_t · h_{t-1} + b_t` (quét 400 token × 4 hướng) | khoảng 2 |
| ⑤ | `y = Σ_{n=1..16} C_n · h_n`, cộng 4 hướng | khoảng 3 |
| ⑥ | `y = y · SiLU(z)` | khoảng 4 |
| ⑦ | `out_proj(y)`, **không có bước chuẩn hóa nào trước đó** | |

Conv thông thường là phép tuyến tính: đầu vào gấp 2 thì đầu ra gấp 2. SS2D là tích của nhiều đại lượng cùng phụ thuộc vào đầu vào, nên **chênh lệch nhỏ về độ lớn trọng số `W_B`, `W_C` bị phóng đại theo lũy thừa**. *(Code: đã xác nhận. Bậc lũy thừa: suy luận)*

### 3.3. Số đo theo từng bước (10 seed)

*(Đã xác nhận: `../DL_Poylp_v26_VMamba_TestDemo_V2/07_doi_chieu_lich_su/ket_qua/bien_do/bien_do_10_seed.csv`, `tham_so_nho/tham_so_nho_10_seed.csv`)*

| Seed | Vào TSVM | \|B\| TB | `b` max | Vào `out_proj` | **Trước BN** | Số kênh `running_mean` > 65.504 |
|---|---|---|---|---|---|---|
| 5 | 7,3 | 3,18 | 17.252 | 17,9 triệu | **17,6 triệu** | **256/256** |
| 8 | 11,3 | 4,67 | 2.728 | 5,3 triệu | **4,3 triệu** | **248/256** |
| 0 | 8,6 | 2,24 | 1.688 | 1,5 triệu | **1,1 triệu** | **49/256** |
| 7 | 11,5 | 2,77 | 2.138 | 1,3 triệu | 0,70 triệu | 0 |
| 9 | 9,0 | 2,77 | 1.009 | 1,0 triệu | 0,57 triệu | 4 |
| 4 | 9,7 | 1,36 | 1.238 | 1,2 triệu | 0,55 triệu | 0 |
| 2 | 10,4 | 0,56 | 121 | 38 nghìn | 43 nghìn | 0 |
| 6 | 11,8 | 0,73 | 133 | 49 nghìn | 37 nghìn | 0 |
| 1 | 8,4 | 0,39 | 280 | 67 nghìn | 24 nghìn | 0 |
| 3 | 9,2 | 0,55 | 40 | 3,9 nghìn | 1,8 nghìn | 0 |

Đọc bảng:
- **Đầu vào của mọi seed gần như bằng nhau** (7–12). Chênh lệch sinh ra hoàn toàn bên trong SS2D.
- Biên độ trước BN tương quan rất chặt với |B| (ρ = 0,92) và |C| (ρ = 0,93). Seed 5 có |B| lớn hơn seed 3 khoảng 6 lần, nhưng biên độ trước BN lớn hơn khoảng **10.000 lần**.
- `h` max bằng `b` max ở mọi seed. Như vậy tích lũy dọc chuỗi (bước ④) **không phải** bước khuếch đại chính; thủ phạm là chuỗi nhân B·C·z. *(Suy luận từ số liệu)*

### 3.4. Vì sao trong lúc train không có gì kìm số lại

1. **SS2D thiếu `out_norm`.** VMamba gốc có LayerNorm trên `y` trước khi nhân với `SiLU(z)`; fork này bỏ mất bước đó. *(Đã xác nhận: fork V2 thêm lại thành tùy chọn với chú thích "as in VMamba")*
2. **BN che mất độ lớn.** Vì `BN(k·x) = BN(x)`, f_m lớn gấp 1.000 lần thì đầu ra BN vẫn như cũ. Loss không phạt độ lớn, nên |B| và |C| trôi tự do; weight decay 0,0005 quá yếu để kéo lại. *(Tính chất BN: đã xác nhận. Cơ chế trôi: suy luận)*
3. **Seed chỉ là may rủi.** Khởi tạo và thứ tự dữ liệu khác nhau nên mỗi seed trôi một mức. Seed 5 không có gì đặc biệt, chỉ là trôi xa nhất.
4. **Lúc train mọi thứ ở FP32**, nên không có gì bị cắt và `results.csv` vẫn đúng.

---

## 4. Vì sao bị cắt thì mô hình sụp

Khi suy luận, BN tính `ŷ = (x − μ) / √(σ² + ε) · w + b`, với μ và σ² lấy từ checkpoint.

| Seed | μ thật lớn nhất | μ sau khi lưu | Độ lệch sau chuẩn hóa (÷ √65.504 ≈ 256) | Kết quả |
|---|---|---|---|---|
| 5 | 1.503.116 | 65.504 | ≈ **5.600 σ**, trên cả 256 kênh | mAP = 0 |
| 8 | 537.008 | 65.504 | ≈ **1.840 σ**, trên 248 kênh | mAP ≈ 0,03 |
| 0 | 115.929 | 65.504 | ≈ **197 σ**, trên 49 kênh | mAP ≈ 0,63 |
| 9 | 77.938 | 65.504 | ≈ 49 σ, chỉ 4 kênh | không ảnh hưởng |

Bình thường đầu ra BN chỉ dao động khoảng ±3 σ. Lệch tới hàng trăm, hàng nghìn σ thì đặc trưng P5 thành rác, và mức hỏng đi đúng theo số kênh bị cắt. `running_var` bị cắt ở cả 10 seed nhưng chỉ gây hại nhẹ, ví dụ seed 7 mất khoảng 0,011. *(Số liệu: đã xác nhận. Cơ chế cho phương sai: suy luận)*

---

## 5. Bằng chứng nhân quả: chỉ sửa một lớp BN là mô hình hồi phục

Thí nghiệm `../DL_Poylp_v26_VMamba_TestDemo_V2/07_doi_chieu_lich_su/hieu_chinh_bn.py` **chỉ tính lại thống kê FP32 của `model.10.m.0.fuse.bn`**. Thí nghiệm không đụng tới head, `fuse()` hay bất kỳ trọng số nào khác.

| Seed | Lúc train | `best.pt` như đã lưu | Sau khi hiệu chỉnh BN |
|---|---|---|---|
| 5 | 0,9096 (0,7285) | **0,0000** (0,0000) | **0,9099** (0,7243) |
| 8 | 0,9150 (0,7333) | **0,0298** (0,0102) | **0,9129** (0,7333) |
| 0 | 0,9040 (0,7245) | **0,6306** (0,4580) | **0,9074** (0,7247) |
| 7 | 0,8940 (0,7022) | 0,8829 (0,6907) | 0,8910 (0,7008) |
| 9 | 0,9123 (0,7326) | 0,9185 (0,7377) | 0,9135 (0,7330) |

*Định dạng: Mask mAP50 (Mask mAP50-95). Nguồn: `tong_hop_10_seed.csv`. (Đã xác nhận)*

Bản hiệu chỉnh **chỉ dùng làm bằng chứng**. Giá trị thống kê thật đã mất khi lưu, nên `best.pt` cũ không thể khôi phục chính xác và không dùng làm kết quả chính thức.

---

## 6. Vì sao giải thích cũ "do `fuse()`" là sai

Tài liệu 17 cho rằng `model.fuse()` xóa nhánh one2many, buộc mô hình dùng nhánh one2one chưa học tốt. Giải thích này mâu thuẫn với dữ liệu:

1. **Khi đánh giá, head luôn dùng one2one**, kể cả lúc tính `results.csv` mỗi epoch (`nn/modules/head.py:181`). Bỏ one2many không làm thay đổi nhánh đang được dùng. *(Đã xác nhận)*
2. Lớp bị hỏng nằm ở **backbone (tầng 10)**, dùng chung cho cả hai nhánh, nên nhánh nào cũng hỏng như nhau. *(Đã xác nhận)*
3. Log Kaggle của seed 0 cho thấy validate với "chặn fuse" ra 0,630, "cứu hộ" ra 0,631, tức là can thiệp vào fuse không làm số thay đổi. Notebook vẫn in "ĐÃ CỨU HỘ XONG! … khôi phục về chuẩn: 0.6313", một **thông báo thành công giả**. *(Đã xác nhận, dòng 581–600 của log)*
4. Hiệu chỉnh BN (mục 5) sửa được lỗi mà không đụng tới head. *(Đã xác nhận)*

Các tài liệu dựa trên giải thích "fuse" (`17_SU_CO_FUSE_...md`, `25_KICH_BAN_PHAN_BIEN_SU_CO_FUSE_...md`, `GIAI_THICH_SU_CO_FUSE_CHO_NGUOI_DOC.md`) cần được đối chiếu lại với tài liệu này. *(Chưa rà soát nội dung)*

---

## 7. Ảnh hưởng tới kết quả khóa luận

| Nội dung | Dùng được? |
|---|---|
| `results.csv` của mọi seed, cả TSVM lẫn Baseline | **Được.** Tính ở FP32 lúc train |
| Bảng so sánh mAP Baseline với TSVM (tài liệu 20, 26) | **Được**, vì lấy từ `results.csv` |
| Ma trận nhầm lẫn, đường PR/F1/P/R, ảnh dự đoán của **Baseline** | **Được** (23/23 seed khớp) |
| Các sản phẩm trên của **TSVM seed 0, 5, 7, 8, 10, 12, 14, 15, 16, 17, 19** | **Không**, vì sinh từ checkpoint đã hỏng |
| Ảnh đường cong của TSVM seed 5 trong `KetQua_Nen` | **Không**, nghi bị vẽ lại (mục 1.2) |
| `best.pt`/`last.pt` cũ của các seed TSVM bị sụp | **Không**, giá trị thật đã mất |
| Suy luận TSVM ở FP16 (AMP, TensorRT FP16, GPU nhúng) | **Không an toàn**, vì giá trị kích hoạt vượt giới hạn FP16 ngay cả khi checkpoint là FP32 *(Suy luận)* |

---

## 8. Cách khắc phục

### 8.1. Khắc phục A (bắt buộc): lưu checkpoint FP32 và dừng khi có NaN/Inf

Bản vá có ở hai nơi:
- **Trong repo này:** `archive/ultralytics_Topology-Shape-aware_VMamba_FP32/` (tạo ngày 12/10/2026), là bản sao của fork gốc đã vá. Xem `PATCH_FP32.md` trong thư mục đó. Fork gốc được giữ nguyên. *(Đã kiểm tra: với `running_mean` = 1.503.116, bản gốc lưu thành 65.504, bản vá giữ nguyên 1.503.116; `inf` trong EMA thì bản vá dừng bằng `FloatingPointError`)*
- **Trong V2:** `../DL_Poylp_v26_VMamba_TestDemo_V2/03_ma_nguon/` (diff đầy đủ ở `PATCH_FP32.md`).

Bản vá sửa 2 tệp:

**`engine/trainer.py` → `save_model`:**

```diff
-        ema = deepcopy(ema).half().to(memory_format=torch.contiguous_format)
+        ema = deepcopy(ema).float().to(memory_format=torch.contiguous_format)
 ...
-        for v in ema.state_dict().values():
-            if isinstance(v, torch.Tensor) and v.is_floating_point():
-                torch.nan_to_num_(v)
+        invalid = [k for k, v in ema.state_dict().items()
+                   if isinstance(v, torch.Tensor) and v.is_floating_point() and not torch.isfinite(v).all()]
+        if invalid:
+            raise FloatingPointError(f"Non-finite EMA snapshot tensors: {invalid}")
```

Bản vá cũng bỏ đoạn chép đè tensor EMA bằng tensor của model khi gặp NaN, vì đoạn đó che lỗi.

**`utils/torch_utils.py` → `strip_optimizer`:**

```diff
-    x["model"].half()  # to FP16
+    x["model"].float()  # preserve FP32 BN statistics in final checkpoints
+    invalid = [k for k, v in x["model"].state_dict().items()
+               if isinstance(v, torch.Tensor) and v.is_floating_point() and not torch.isfinite(v).all()]
+    if invalid:
+        raise FloatingPointError(f"Non-finite checkpoint tensors: {invalid}")
```

FP32 biểu diễn được tới khoảng 3,4·10³⁸, nên không còn bị cắt. Nếu có NaN/Inf thì quá trình **dừng ngay**, không âm thầm sửa số.

**Lưu ý trên Kaggle:** notebook phải nạp đúng fork đã vá. Log seed 0 cho thấy notebook nạp `/kaggle/working/ultralytics` và file lưu ra 25 MB, tức là **chưa vá**.

### 8.2. Khắc phục B (bắt buộc): suy luận TSVM ở FP32

- Validate/predict với `half=False` (mặc định), train với `amp=False`.
- Không export TensorRT/ONNX FP16 cho TSVM nếu chưa áp dụng khắc phục C.

### 8.3. Khắc phục C (khuyến nghị lâu dài): thêm LayerNorm vào đầu ra SS2D

Fork V2 có tùy chọn `SS2D(out_norm=True)`, bật bằng mode có hậu tố `_ln` (ví dụ `topology_shape_vmamba_ln`) và cấu hình `cfg/models/26/yolo26-seg-TopologyShapeVMamba-LN.yaml`. LayerNorm chuẩn hóa `y` trước khi nhân với `SiLU(z)`, giống VMamba gốc, nên chặn được chuỗi khuếch đại ngay tại gốc.

Đo thử bằng cách gắn LN vào trọng số đã train (`thu_layernorm_10_seed.csv`):

| Seed | Đỉnh trước BN (gốc) | Đỉnh trước BN (có LN) | An toàn FP16? |
|---|---|---|---|
| 5 | 17.616.256 | 98 | Không → **Có** |
| 8 | 4.296.117 | 99 | Không → **Có** |
| 0 | 1.121.091 | 102 | Không → **Có** |
| 3 | 1.803 | 19 | Có → Có |

Cả 10/10 seed đều an toàn với FP16. **Chưa xác minh:** đây mới là phép đo biên độ, chưa train lại TSVM-LN nên chưa biết mAP. Đây cũng là **thay đổi kiến trúc**, nên kết quả TSVM-LN phải báo cáo như một mô hình riêng, không trộn với TSVM gốc.

### 8.4. Sửa notebook Kaggle

- Bỏ bước "PHÁT HIỆN SỰ CỐ FUSE / CỨU HỘ", vì nó chẩn đoán sai và báo thành công giả.
- Bỏ đoạn "chặn `model.fuse()`", vì nó không liên quan tới lỗi.
- Thay bằng các kiểm tra ở mục 8.5. Nếu không đạt thì **báo lỗi và dừng**, không tự sửa.

### 8.5. Tiêu chí nghiệm thu cho mỗi run mới

| # | Kiểm tra | Đạt khi |
|---|---|---|
| 1 | Kích thước `best.pt` của TSVM s | khoảng **49 MB** (FP32), không phải khoảng 25 MB |
| 2 | dtype trong checkpoint | mọi tensor dấu phẩy động là `float32` |
| 3 | So `best.pt` với `results.csv` | Mask mAP50 và mAP50-95 lệch **≤ 0,005** so với dòng có fitness cao nhất. Lệch nhiều hơn thì báo `AP_MISMATCH` (hàm `evaluate` trong `04_kaggle/polyp_v2.py` của V2) |
| 4 | Log | không có `FloatingPointError`; nếu có thì lưu log lại để phân tích, không chạy lại cho qua |
| 5 | (khuyến nghị) BN tầng 10 | `max|running_mean|` và `max(running_var)` của `model.10.m.0.fuse.bn` được ghi lại để theo dõi biên độ |

### 8.6. Kiểm tra checkpoint (đoạn mã tham khảo)

```python
import torch
ck = torch.load("best.pt", map_location="cpu", weights_only=False)
m = ck["ema"] if ck.get("ema") is not None else ck["model"]   # best.pt cuối cùng: ema=None, dùng "model"
sd = m.state_dict()
print({str(v.dtype) for v in sd.values() if v.is_floating_point()})   # mong đợi {'torch.float32'}
bn = "model.10.m.0.fuse.bn"
for k in ("running_mean", "running_var"):
    t = sd[f"{bn}.{k}"].float()
    print(k, float(t.abs().max()), int((t.abs() >= 65504).sum()), "kênh chạm ngưỡng FP16")
```

Với checkpoint cũ, dtype sẽ là `float16`, và các giá trị đúng bằng 65.504 là dấu hiệu đã bị cắt.

Đã chạy thử trên `KetQua_XacThuc/best_and_last/results 0/.../best.pt` (TSVM seed 0) ngày 12/10/2026, cần fork trên `sys.path`. Kết quả: `{'torch.float16'}`, `running_mean` có 49 kênh và `running_var` có 256 kênh đúng bằng 65.504, khớp với mục 3.3. *(Đã xác nhận)*

---

## 9. Việc còn tồn đọng

| Việc | Trạng thái |
|---|---|
| Train lại TSVM các seed bị sụp bằng fork V2 (FP32) | *(Chưa xác minh: chưa có run nào hoàn tất; kế hoạch ở `05_ket_qua/KE_HOACH_20_RUN.csv` của V2)* |
| Train và đánh giá TSVM-LN | *(Chưa xác minh)* |
| Đo biên độ và hiệu chỉnh BN cho TSVM seed 10–20 | *(Chưa làm: hiện chỉ có phép so ảnh PR ở mục 1.2)* |
| Xác minh nguồn gốc ảnh đường cong của TSVM seed 5 | *(Chưa xác minh)* |
| Cập nhật tài liệu 17, 25, `GIAI_THICH_SU_CO_FUSE_CHO_NGUOI_DOC.md`, `CURRENT_PROJECT_STATUS.md`, `LICHSU_CAP_NHAT.md` | Chưa làm |

---

## 10. Trả lời ngắn khi bảo vệ

> "Khi huấn luyện, TSVM đạt khoảng 0,90 Mask mAP50 ở mọi seed. Nhưng Ultralytics lưu checkpoint ở FP16, mà FP16 chỉ biểu diễn được số tối đa khoảng 65 nghìn. Trong khối VMamba, phép quét SS2D là chuỗi phép nhân, không có lớp chuẩn hóa ở đầu ra, nên ở một số seed giá trị vào BatchNorm lên tới hàng triệu. Khi lưu, thống kê BatchNorm bị cắt và mô hình chạy lại bị sai. Đây là lỗi lưu trữ, không phải lỗi huấn luyện: chỉ cần tính lại đúng một lớp BatchNorm, seed 5 hồi phục từ 0 lên 0,91. Các số liệu so sánh trong khóa luận lấy từ `results.csv` ở FP32 nên không bị ảnh hưởng. Baseline không mắc lỗi này vì không có chuỗi phép nhân như SS2D."

---

## 11. Nguồn

| Nguồn | Nội dung |
|---|---|
| `archive/ultralytics_Topology-Shape-aware VMamba/nn/modules/topology_shape_vmamba.py` | SS2D (dòng 131–210), TSVMamba (dòng 389–413) |
| `archive/ultralytics*/engine/trainer.py:728,734`; `utils/torch_utils.py:828` | Lưu FP16 và `nan_to_num` |
| `archive/ultralytics_Topology-Shape-aware VMamba/nn/modules/head.py:181`; `utils/metrics.py:1371` | Đánh giá dùng one2one; công thức fitness |
| `archive/Ket_Qua_V2/KetQua_Nen/{YOLOv26s-seg, Kvasir_BG20_YOLO26s_seg_TSVM}/*/` | `results.csv`, `MaskPR_curve.png`, `args.yaml` |
| `kvasir-yolo26s-seg-topology-shape-awar.log` (gốc repo) | Log Kaggle của TSVM seed 0 |
| `../DL_Poylp_v26_VMamba_TestDemo_V2/07_doi_chieu_lich_su/ket_qua/` | Biên độ, tham số SSM, hiệu chỉnh BN, thử LayerNorm (seed 0–9) |
| `../DL_Poylp_v26_VMamba_TestDemo_V2/03_ma_nguon/PATCH_FP32.md` | Bản vá lưu FP32 |
| `output/BaoCaoKetQua/BAO_CAO_SU_CO_PHINH_SO_TSVM_SEED_0_5_8.md` | Báo cáo sự cố gốc (seed 0, 5, 8). Có trên nhánh `phungtuanhuy2`, **không có trong working tree của nhánh `Okeydokey`** |
