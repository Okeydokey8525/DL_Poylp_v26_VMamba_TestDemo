# Sự cố checkpoint TSVM seed 0, 5, 8: khoanh vùng lỗi và bản sửa code

> **Gửi:** nhóm trưởng. **Ngày:** 10/10/2026.
> **Phạm vi:** fork `archive/ultralytics_Topology-Shape-aware VMamba/` (Ultralytics 8.4.127) và các lượt train TSVM trên Kaggle.
>
> Mức độ chắc chắn của từng nhận định được ghi ngay sau nó:
> - **[Đã xác nhận]**: đo hoặc chạy trực tiếp;
> - **[Suy luận]**: rút ra từ cơ chế, chưa đo riêng;
> - **[Chưa xác minh]**: chưa kiểm tra.
>
> Tài liệu giải thích chi tiết hơn: `output/BaoCaoKetQua/BAO_CAO_SU_CO_PHINH_SO_TSVM_SEED_0_5_8.md`.

---

## 0. Tóm tắt cho người bận

| | |
|---|---|
| **Hiện tượng** | TSVM seed 0, 5, 8 cho `results.csv` khoảng 0,90–0,92 Mask mAP50. Nhưng khi mở `best.pt` để đánh giá lại: seed 5 về 0, seed 8 còn 0,03, seed 0 còn 0,63 |
| **Nguyên nhân trực tiếp** | `save_model` lưu checkpoint ở **FP16** (tối đa 65.504) và dùng `nan_to_num_`, nên thống kê BatchNorm của khối TSVM tầng 10 bị **cắt** về 65.504 |
| **Nguyên nhân gốc** | SS2D **không chuẩn hóa đầu ra**, nên tín hiệu trước BatchNorm lên tới **17,6 triệu** ở seed 5 |
| **Không phải do** | Hàm `fuse()` hay nhánh one2many/one2one, như tài liệu 17 đã ghi |
| **Kết quả lúc train có sai không?** | **Không.** `results.csv` được tính trên mô hình FP32 trong bộ nhớ, nên vẫn hợp lệ |
| **Sửa bắt buộc** | Lưu checkpoint FP32: 2 tệp, mục 4.1. Không đổi mô hình, nên kết quả so sánh được với lần train cũ |
| **Sửa đề xuất** | Thêm LayerNorm vào đầu ra SS2D, tạo mô hình **TSVM-LN** (mục 4.3). Đây là mô hình mới, **phải train lại 10 seed** mới biết có tốt hơn hay không |
| **Đã có sẵn** | Toàn bộ code đã sửa và kiểm thử trong `DL_Poylp_v26_VMamba_TestDemo_V2/`, gồm 23 test pytest đều đạt |

---

## 1. Hiện tượng [Đã xác nhận]

| Seed | Mask mAP50 lúc train | Mở `best.pt` FP16 rồi đánh giá |
|---|---|---|
| 0 | 0,904 | **0,631** |
| 5 | 0,910 | **0,000** |
| 8 | 0,915 | **0,030** |
| 1, 2, 3, 4, 6, 9 | 0,900 – 0,916 | gần như bằng lúc train |

Các con số "mở `best.pt`" đã được tái hiện trên máy cá nhân bằng CPU, ra đúng như log Kaggle. Vì vậy lỗi **không phụ thuộc môi trường Kaggle**.

---

## 2. Khoanh vùng lỗi trong code

### ⚠ VÙNG A: Lưu checkpoint FP16 và che lỗi bằng `nan_to_num` (nguyên nhân trực tiếp)

**Tệp:** `archive/ultralytics_Topology-Shape-aware VMamba/engine/trainer.py`, hàm `save_model`, dòng 712–735.

```python
    def save_model(self):
        ...
        ema = unwrap_model(self.ema.ema)
        if not all(torch.isfinite(v).all() for v in ema.state_dict().values() ...):   # ⚠ A1: "sửa" EMA bằng
            model_sd = unwrap_model(self.model).state_dict()                          #     tensor của model khác
            for k, v in ema.state_dict().items():
                if ... not torch.isfinite(v).all() and torch.isfinite(model_sd[k]).all():
                    v.copy_(model_sd[k])
        ema = deepcopy(ema).half().to(memory_format=torch.contiguous_format)          # ⚠ A2: ÉP SANG FP16
        ...                                                                           #     (tối đa 65.504)
        for v in ema.state_dict().values():
            if isinstance(v, torch.Tensor) and v.is_floating_point():
                torch.nan_to_num_(v)                                                  # ⚠ A3: inf → 65.504,
                                                                                      #     lỗi bị che, không báo
```

**Tệp:** `archive/ultralytics_Topology-Shape-aware VMamba/utils/torch_utils.py`, hàm `strip_optimizer`, dòng 828.

```python
    x["model"].half()  # to FP16                                                      # ⚠ A4: ép FP16 lần nữa
```

**Hậu quả:** mọi giá trị lớn hơn 65.504 bị cắt mà không có cảnh báo nào. Log Kaggle ghi `best.pt, 25.0MB`, đúng một nửa kích thước bản FP32.

### ⚠ VÙNG B: SS2D không chuẩn hóa đầu ra (nguyên nhân gốc)

**Tệp:** `archive/ultralytics_Topology-Shape-aware VMamba/nn/modules/topology_shape_vmamba.py`, `SS2D.forward`, dòng 168–210.

```python
            dt = F.softplus(self.dt_projs[k](dt_raw).transpose(1, 2))     # bước quét, phụ thuộc ảnh
            ...
            a_mat = torch.exp(delta_A)                                    # hệ số nhớ: dt rất nhỏ → a ≈ 1
            b_mat = dt.unsqueeze(2) * B_mat.unsqueeze(1) * u_k.unsqueeze(2)   # ⚠ B1: cổng ghi B không bị giới hạn
            h = parallel_associative_scan(a_mat, b_mat)                   # ⚠ B2: cộng dồn tới 400 ô khi a ≈ 1
            y_k = torch.einsum("bdnl,bnl->bdl", h, C_mat)                 # ⚠ B3: cổng đọc C không bị giới hạn
        ...
        y = y_0 + y_1 + y_2 + y_3                                         # cộng 4 hướng quét
                                                                          # ⚠ B4: THIẾU chuẩn hóa ở đây
        y = y * F.silu(z, inplace=False)
        out = self.out_proj(y)
```

Ngay sau đó, trong `TSVMamba.forward` (dòng 409), đầu ra cỡ triệu được ghép với nhánh shape chỉ cỡ 6–10, rồi đưa vào `self.fuse`, tức Conv kèm **BatchNorm `model.10.m.0.fuse.bn`**. Đây chính là lớp bị cắt.

### ⚠ VÙNG C: Chẩn đoán sai trước đây

`archive/doc/17_SU_CO_FUSE_...md` cho rằng `fuse()` xóa nhánh one2many. Điều này không khớp với code:
- `nn/modules/head.py:181` cho thấy khi đánh giá, head **luôn** dùng one2one nếu `end2end=True`, kể cả lúc đánh giá từng epoch để ghi `results.csv`. [Đã xác nhận]
- Lớp hỏng **tình cờ tên là `fuse`** (`model.10.m.0.fuse.bn`), không liên quan tới `model.fuse()`. [Suy luận về nguồn gốc nhầm lẫn]

---

## 3. Bằng chứng

### 3.1. Quét checkpoint: số kênh BatchNorm bị cắt đúng ở 65.504 [Đã xác nhận]

Lớp `model.10.m.0.fuse.bn` có 256 kênh.

| Seed | `running_mean` bị cắt | `running_var` bị cắt | Mean thật lớn nhất (đo lại bằng FP32) |
|---|---|---|---|
| **5** | **256/256** | 256 | **1.503.116** |
| **8** | **248/256** | 256 | **537.008** |
| **0** | **49/256** | 256 | **115.929** |
| 9 | 4/256 | 256 | 77.938 |
| 7 | 0 | 256 | 30.952 |
| 4 | 0 | 256 | 21.262 |
| 6 | 0 | 256 | 2.398 |
| 2 | 0 | 256 | 1.248 |
| 1 | 0 | 244 | 620 |
| 3 | 0 | 218 | 13 |

`running_var` bị cắt ở mọi seed và chỉ gây hại nhẹ. Rõ nhất là seed 7: Mask mAP50 thấp hơn lúc train 0,011, hiệu chỉnh lấy lại được phần lớn. Chính `running_mean` bị cắt mới làm hỏng mô hình, vì BatchNorm lấy đầu vào trừ đi một trung bình sai. Mức hỏng xếp đúng thứ tự 5 > 8 > 0.

### 3.2. Thí nghiệm nhân quả: chỉ đo lại thống kê 1 lớp BatchNorm [Đã xác nhận]

Thí nghiệm giữ nguyên mọi trọng số. Chỉ đo lại `running_mean` và `running_var` của `model.10.m.0.fuse.bn` bằng FP32 trên 256 ảnh train, rồi đánh giá trên 160 ảnh val. Kết quả Mask mAP50:

| Seed | Lúc train | Mở FP16 như đã lưu | Sau khi đo lại 1 lớp |
|---|---|---|---|
| **5** | 0,9096 | **0,0000** | **0,9099** |
| **8** | 0,9150 | **0,0298** | **0,9129** |
| **0** | 0,9040 | **0,6306** | **0,9074** |
| 9 | 0,9123 | 0,9185 | 0,9135 |
| 1 | 0,9115 | 0,9132 | 0,9132 |
| 2 | 0,9003 | 0,8985 | 0,8991 |
| 3 | 0,9164 | 0,9183 | 0,9183 |
| 4 | 0,9024 | 0,8984 | 0,8998 |
| 6 | 0,9061 | 0,9017 | 0,9003 |
| 7 | 0,8940 | 0,8829 | 0,8910 |

Kết luận:
- Bỏ nguyên nhân thì hết lỗi, nên đây là **bằng chứng nhân quả**.
- Các seed khỏe gần như không đổi, nên phép đo lại không tự làm tăng điểm.
- Chênh lệch còn lại khoảng 0,005 ở seed khỏe có thể do khác batch và cách đệm ảnh khi đánh giá. [Suy luận]

### 3.3. Nguồn gốc biên độ lớn: bên trong SS2D [Đã xác nhận]

Đo trên 8 ảnh val, 10 seed. Hệ số tương quan là Spearman ρ giữa từng đại lượng và biên độ trước BatchNorm:

| Đại lượng | ρ | p |
|---|---|---|
| Đầu vào khối TSVM (khoảng 7–12 ở mọi seed) | −0,15 | 0,68 |
| Nhánh shape (khoảng 6–10 ở mọi seed) | 0,16 | 0,65 |
| `dt` nhỏ nhất 5 %: seed hỏng khoảng 0,01, seed khỏe khoảng 0,35 | **−0,87** | 0,001 |
| \|B\| trung bình: seed hỏng 2,2–4,7, seed khỏe 0,4–0,8 | **0,92** | 0,0002 |
| \|C\| trung bình | **0,93** | 0,0001 |

Tham số `A` gần như không đổi so với lúc khởi tạo ở mọi seed, độ lệch khoảng 0,001. Đây là một quan sát phụ, **chưa giải thích được**.

### 3.4. Độ chính xác lúc train không bị ảnh hưởng [Đã xác nhận]

Biên độ không tương quan với Mask mAP50-95 tại best epoch (ρ = 0,32, p = 0,37). Ba seed hỏng có trung bình 0,7288, bảy seed còn lại 0,7220.

---

## 4. Bản sửa

Toàn bộ code dưới đây đã có trong `DL_Poylp_v26_VMamba_TestDemo_V2/`. Thư mục này được dựng lại độc lập: cùng dữ liệu BG20, trùng từng byte, và cùng cấu hình train lịch sử.

### 4.1. Sửa 1 (BẮT BUỘC): lưu checkpoint FP32, không che lỗi

Sửa vùng A. Mô hình **không đổi**, nên kết quả so sánh trực tiếp được với lần train cũ.

`engine/trainer.py`, hàm `save_model`:

```diff
-        # A transient NaN/Inf permanently poisons the EMA running average ...
+        # Save exactly the EMA used for validation; do not repair its tensors from a different model.
         ema = unwrap_model(self.ema.ema)
-        if not all(torch.isfinite(v).all() for v in ema.state_dict().values() if isinstance(v, torch.Tensor)):
-            model_sd = unwrap_model(self.model).state_dict()
-            for k, v in ema.state_dict().items():
-                if isinstance(v, torch.Tensor) and not torch.isfinite(v).all() and torch.isfinite(model_sd[k]).all():
-                    v.copy_(model_sd[k])
-        ema = deepcopy(ema).half().to(memory_format=torch.contiguous_format)
+        ema = deepcopy(ema).float().to(memory_format=torch.contiguous_format)
         if hasattr(ema, "criterion"):
             ema.criterion = None
-        # Clamp fp16 serialization overflow without mutating the live EMA.
-        for v in ema.state_dict().values():
-            if isinstance(v, torch.Tensor) and v.is_floating_point():
-                torch.nan_to_num_(v)
+        # BN statistics can exceed FP16's range. Preserve them and reject invalid snapshots before writing.
+        invalid = [k for k, v in ema.state_dict().items()
+                   if isinstance(v, torch.Tensor) and v.is_floating_point() and not torch.isfinite(v).all()]
+        if invalid:
+            raise FloatingPointError(f"Non-finite EMA snapshot tensors: {invalid}")
```

`utils/torch_utils.py`, hàm `strip_optimizer`:

```diff
-    x["model"].half()  # to FP16
+    x["model"].float()  # preserve FP32 BN statistics in final checkpoints
+    invalid = [k for k, v in x["model"].state_dict().items()
+               if isinstance(v, torch.Tensor) and v.is_floating_point() and not torch.isfinite(v).all()]
+    if invalid:
+        raise FloatingPointError(f"Non-finite checkpoint tensors: {invalid}")
```

Hệ quả:
- `best.pt` nặng khoảng 50 MB thay vì 25 MB.
- FP32 chứa được giá trị tới khoảng 3,4·10³⁸, nên không còn bị cắt.
- Gặp NaN/Inf thì dừng ngay, không âm thầm sửa số.

Chi tiết bản vá: `V2/03_ma_nguon/PATCH_FP32.md`.

### 4.2. Sửa 2 (BẮT BUỘC): đánh giá đúng checkpoint đã lưu và tự phát hiện lỗi

Sửa vùng C, trong `V2/04_kaggle/polyp_v2.py`:

| Biện pháp | Tác dụng |
|---|---|
| Đánh giá `best.pt` trong **tiến trình mới**, FP32, **tắt fuse** (`BaseModel.fuse` trả về chính nó) | Đánh giá đúng checkpoint đã lưu, không qua bước gộp lớp |
| So 4 chỉ số AP với dòng best epoch trong `results.csv`, sai lệch tối đa 0,005 | Lỗi kiểu seed 0/5/8 bị báo **`AP_MISMATCH`** ngay, lượt đó không được dùng |
| Ghi `fp16_risk` vào `run.json` | Đo được với mỗi lượt mới: lớp nào sẽ bị cắt nếu vẫn lưu FP16 |
| Mỗi lượt kiểm tra `dataset_id` và `code_id` | Không lẫn dữ liệu hay code giữa các lượt |

### 4.3. Sửa 3 (ĐỀ XUẤT, mô hình mới TSVM-LN): thêm LayerNorm vào đầu ra SS2D

Sửa vùng B, tức nguyên nhân gốc. Bản VMamba gốc theo hiểu biết của chúng tôi có `out_norm` ở vị trí này. **[Chưa xác minh]**: cần đối chiếu mã nguồn VMamba gốc.

`nn/modules/topology_shape_vmamba.py`:

```diff
 class SS2D(nn.Module):
-    def __init__(self, d_model, d_state=16, d_conv=3, expand=1.0, dt_rank=None, bias=False):
+    def __init__(self, d_model, d_state=16, d_conv=3, expand=1.0, dt_rank=None, bias=False, out_norm=False):
         ...
+        self.out_norm = nn.LayerNorm(self.d_inner) if out_norm else None
         self.out_proj = nn.Conv2d(self.d_inner, self.d_model, kernel_size=1, bias=bias)

     def forward(self, x):
         ...
         y = y_0 + y_1 + y_2 + y_3
+        # Bound the scan output (getattr: checkpoints pickled before this option have no attribute)
+        norm = getattr(self, "out_norm", None)
+        if norm is not None:
+            y = norm(y.permute(0, 2, 3, 1)).permute(0, 3, 1, 2)
         y = y * F.silu(z, inplace=False)

 class TSVMamba(nn.Module):
     def __init__(self, c, d_state=16, d_conv=3, expand=1.0, mode="topology_shape_vmamba"):
         ...
-        self.mode = mode
+        out_norm = mode.endswith("_ln")
+        self.mode = mode[:-3] if out_norm else mode
         if self.mode in ("topology_shape_vmamba", "vmamba_only", "shape_vmamba_no_guidance"):
-            self.vmamba = SS2D(d_model=c, d_state=d_state, d_conv=d_conv, expand=expand)
+            self.vmamba = SS2D(d_model=c, d_state=d_state, d_conv=d_conv, expand=expand, out_norm=out_norm)
```

YAML mới `cfg/models/26/yolo26-seg-TopologyShapeVMamba-LN.yaml` chỉ khác đúng một dòng:

```diff
-  - [-1, 2, C2TSVMamba, [1024]] # 10
+  - [-1, 2, C2TSVMamba, [1024, 0.5, 16, 3, "topology_shape_vmamba_ln"]] # 10 TSVM + LayerNorm on SS2D output
```

Không cần sửa `nn/tasks.py`, vì `parse_model` đã truyền tham số `mode` theo vị trí.

**Đã kiểm chứng [Đã xác nhận]:**

| Kiểm tra | Kết quả |
|---|---|
| Chế độ cũ `topology_shape_vmamba` trong fork đã sửa so với fork gốc | Cùng khóa `state_dict`, cùng 12.254.688 tham số. Chạy checkpoint lịch sử seed 3 cho đầu ra **giống từng bit** |
| Mô hình TSVM-LN | 12.255.200 tham số, thêm đúng 512 tham số (`vmamba.out_norm.weight/bias`) |
| Tăng `x_proj` (sinh `dt`, B, C) lên 100 lần | Bản gốc: đầu ra lớn lên khoảng **21.869 lần**. TSVM-LN: khoảng **2,9 lần**, tức không phụ thuộc độ phình |
| Gắn LayerNorm vào trọng số cũ của 10 seed rồi đo biên độ trước BatchNorm | Seed 5: 17.616.256 → **98**. Cả 10 seed còn ≤ 102, **dưới ngưỡng FP16** |
| Train thử 1 epoch rồi đánh giá trên tập con nhỏ (CPU) | Xem mục 6 |
| pytest `06_kiem_tra/test_tsvm_ln.py` | 4/4 đạt |

**CHƯA biết [Chưa xác minh]:**
- TSVM-LN có cho mAP cao hơn TSVM hay không. LayerNorm sửa **độ ổn định số học**, không hứa hẹn tăng độ chính xác.
- Nhánh shape có còn bị nhánh VMamba "lấn át" không. Sau khi có LayerNorm, hai nhánh cùng thang đo nên có thể nhánh shape đóng góp nhiều hơn, nhưng **phải train mới biết**.

---

## 5. Kế hoạch chạy để chọn ra kết quả tốt nhất

"Tốt nhất" chỉ khẳng định được sau khi train và so sánh có kiểm định. Vì vậy cần chốt quy tắc chọn **trước** khi chạy, để tránh chọn theo kết quả.

| Giai đoạn | Nội dung | Số session Kaggle (T4 x2) |
|---|---|---|
| 0 | SMOKE: 1 epoch cho mỗi mô hình, kiểm tra môi trường | 1–2 |
| 1 (bắt buộc) | baseline và TSVM, seed 0–9, có sửa 1 và sửa 2 | 10 (baseline ở GPU 0, TSVM ở GPU 1) |
| 2 (đề xuất) | TSVM-LN, seed 0–9 | 5 (2 seed song song) |

Notebook `04_kaggle/TRAIN_KAGGLE.ipynb` chỉ cần sửa ô 1:

```python
JOBS = [("baseline", SEED), ("tsvm", SEED)]          # giai đoạn 1, SEED = 0..9
JOBS = [("tsvm_ln", SEED), ("tsvm_ln", SEED + 1)]    # giai đoạn 2, SEED = 0, 2, 4, 6, 8
```

Tổng hợp kết quả:

```powershell
python 05_ket_qua/nhap_ket_qua.py 05_ket_qua/zip_tu_kaggle/*.zip
python 04_kaggle/polyp_v2.py aggregate --runs 05_ket_qua/runs --out 05_ket_qua/tong_hop/<ngay>
```

Lệnh `aggregate` tạo bảng mean ± SD cho từng mô hình, cùng kiểm định ghép cặp theo seed (t-test và Wilcoxon) cho **tsvm so với baseline** và **tsvm_ln so với baseline**.

**Quy tắc chọn đề xuất (chốt trước khi chạy):**
1. Chỉ số chính: Mask mAP50-95, trung bình 10 seed.
2. Lượt nào có `status` khác `OK` thì loại.
3. Chỉ kết luận "tốt hơn" khi p < 0,05 trong kiểm định ghép cặp với baseline. Nếu không đạt, chỉ được viết là "chênh lệch quan sát được, không có ý nghĩa thống kê".
4. Nếu TSVM-LN không kém TSVM, ưu tiên TSVM-LN vì ổn định số học, an toàn khi triển khai FP16, và không cần bước hiệu chỉnh.

---

## 6. Trạng thái kiểm chứng của bản sửa

| Hạng mục | Trạng thái |
|---|---|
| Dữ liệu BG20 của V2 trùng từng byte với BG20 đã dùng | Đã xác nhận |
| Trọng số `yolo26s-seg.pt` trùng sha256 bản chính thức v8.4.0 | Đã xác nhận |
| Baseline: train 1 epoch rồi đánh giá trên CPU, toàn bộ dữ liệu | Đã xác nhận: OK, `best.pt` FP32 46,3 MB |
| TSVM: train rồi đánh giá trên tập con, CPU | Đã xác nhận: OK, `best.pt` FP32 49,6 MB |
| TSVM-LN: train 1 epoch rồi đánh giá trên tập con 30 ảnh, CPU, batch 2 | Đã xác nhận: **OK**. `best.pt` FP32 49,6 MB, `fp16_risk` được ghi. Đánh giá chạy trong tiến trình riêng, AP khớp `results.csv` |
| pytest V2 | 23/23 đạt |
| Bundle Kaggle `04_kaggle/upload/v3/` | Giải nén ra, chạy `check` đạt. `code_id` `fe539657…`, trùng với lượt chạy thử TSVM-LN. **Upload bản v3**, không dùng v1 hay v2 |
| Chạy thật trên Kaggle T4 x2 | **Chưa xác minh** |
| mAP của TSVM-LN | **Chưa xác minh**, cần giai đoạn 2 |

---

## 7. Những điều KHÔNG nên làm

- Không dùng `best.pt` đã hiệu chỉnh (`hieu_chinh_bn.py --save`) làm kết quả chính thức. Nó chỉ là bằng chứng.
- Không dùng ma trận nhầm lẫn và đường cong PR của TSVM seed 0, 5, 8 cũ.
- Không đổi batch hay tham số cho riêng một lượt. Nếu buộc phải đổi, đổi trong `protocol.yaml` rồi chạy lại toàn bộ.
- Không gộp các lượt có `code_id` khác nhau. `aggregate` sẽ tự từ chối.
- Không gọi TSVM-LN là "tốt hơn" khi chưa có kết quả 10 seed và kiểm định.

---

## 8. Tệp liên quan (trong `DL_Poylp_v26_VMamba_TestDemo_V2/`)

| Tệp | Nội dung |
|---|---|
| `03_ma_nguon/ultralytics/engine/trainer.py`, `utils/torch_utils.py` | Sửa 1 (FP32) |
| `03_ma_nguon/ultralytics/nn/modules/topology_shape_vmamba.py` | Sửa 3 (`out_norm`, chế độ `_ln`) |
| `03_ma_nguon/ultralytics/cfg/models/26/yolo26-seg-TopologyShapeVMamba-LN.yaml` | Cấu hình TSVM-LN |
| `03_ma_nguon/protocol.yaml` | 3 mô hình: `baseline`, `tsvm`, `tsvm_ln` |
| `04_kaggle/polyp_v2.py` | train, evaluate, aggregate (sửa 2) |
| `04_kaggle/TRAIN_KAGGLE.ipynb` | Notebook Kaggle với biến `JOBS` |
| `07_doi_chieu_lich_su/` | Các thí nghiệm bằng chứng: `hieu_chinh_bn.py`, `do_bien_do.py`, `do_tham_so_nho.py`, `thu_layernorm.py`, kèm kết quả |
| `06_kiem_tra/` | pytest |
