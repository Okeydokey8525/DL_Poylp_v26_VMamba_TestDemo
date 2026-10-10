# Đặc tả cho AI: sửa lỗi checkpoint TSVM (FP16 overflow) và thêm TSVM-LN

> **Cách dùng:** đưa nguyên file này cho AI coding agent, ví dụ Claude Code, Cursor hay Copilot, đang mở repo
> `DL_Poylp_v26_VMamba_TestDemo`. Kèm câu lệnh: *"Đọc toàn bộ file này rồi thực hiện các nhiệm vụ T1–T6 theo đúng thứ tự,
> sau mỗi nhiệm vụ chạy phần Kiểm tra và báo kết quả."*
>
> Người lập: nhóm thực nghiệm, ngày 10/10/2026.
> Bản cài đặt tham chiếu đã chạy và kiểm thử nằm trong thư mục anh em `../DL_Poylp_v26_VMamba_TestDemo_V2/`. AI **được phép đọc**
> thư mục này để đối chiếu, nhưng phải tự sửa trong repo hiện tại.

---

## 0. Quy tắc bắt buộc cho AI

1. **Không sửa** các tệp sau: CSV gốc, checkpoint `*.pt`, ảnh kết quả cũ trong `archive/Ket_Qua_V2/KetQua_Nen/`, `KQ_Nen_DX_10seed/01_raw_analysis/`, `KetQua_XacThuc/`. Mọi script phân tích phải ghi ra **thư mục mới**.
2. **Không bịa số.** Mọi số trong báo cáo phải lấy từ tệp hoặc lệnh đã chạy.
3. Gắn nhãn cho mọi nhận định: **Đã xác nhận** (đã chạy hoặc đo), **Suy luận**, hoặc **Chưa xác minh**.
4. **Không** dùng `ultralytics` cài từ PyPI. Luôn nạp fork `archive/ultralytics_Topology-Shape-aware VMamba/` bằng `importlib`, như hàm `bootstrap` trong `scripts/analysis/diagnose_saved_heads.py`.
5. **Không** đổi tham số train lịch sử: epochs 100, batch 8, imgsz 640, AdamW, lr0 0.001, amp False, ... (xem `args.yaml` của mỗi run).
6. Chế độ TSVM cũ phải cho **đầu ra giống từng bit** với trước khi sửa (nhiệm vụ T3 có kiểm tra).
7. Đọc `CURRENT_PROJECT_STATUS.md` và `CLAUDE.md` trước khi bắt đầu.

---

## 1. Bối cảnh: sự cố và nguyên nhân đã xác nhận

**Hiện tượng (Đã xác nhận):**
- TSVM seed 0, 5, 8 có `results.csv` cho Mask mAP50 khoảng 0,90–0,92.
- Khi nạp `best.pt` để đánh giá lại: seed 5 → 0,000; seed 8 → 0,030; seed 0 → 0,631.
- Tái hiện được trên CPU bằng `archive/Ket_Qua_V2/KetQua_XacThuc/best_and_last/results N/runs/*/weights/best.pt`.

**Nguyên nhân (Đã xác nhận bằng thí nghiệm nhân quả):**
1. `engine/trainer.py::save_model` lưu EMA bằng `.half()` (FP16, tối đa 65.504), rồi `torch.nan_to_num_` biến `inf` thành 65.504. `utils/torch_utils.py::strip_optimizer` cũng gọi `.half()`.
2. BatchNorm `model.10.m.0.fuse.bn` (trong `TSVMamba`, ngay sau `torch.cat([f_m_mod, s])`) có `running_mean` thật tới **1.503.116** ở seed 5. Khi lưu FP16, giá trị này bị cắt về 65.504.
3. Số kênh `running_mean` bị cắt, trên 256: seed 5 là 256, seed 8 là 248, seed 0 là 49, seed 9 là 4, các seed khác 0. Thứ tự này khớp đúng mức hỏng.
4. Thí nghiệm nhân quả: giữ nguyên trọng số, chỉ đo lại `running_mean` và `running_var` của lớp này bằng FP32 trên 256 ảnh train. Mask mAP50 trở lại: seed 5 0,9099 (lúc train 0,9096), seed 8 0,9129 (lúc train 0,9150), seed 0 0,9074 (lúc train 0,9040).

**Nguyên nhân gốc (Đã xác nhận bằng đo; cơ chế là Suy luận):**
- `SS2D.forward` không chuẩn hóa đầu ra. Tín hiệu trước BatchNorm đạt 1,8·10³ (seed 3) đến 1,76·10⁷ (seed 5).
- Biên độ tương quan với `|B|` (Spearman ρ = 0,92), `|C|` (ρ = 0,93) và `dt` nhỏ nhất 5 % (ρ = −0,87). Không tương quan với đầu vào khối TSVM (ρ = −0,15) hay nhánh shape (ρ = 0,16).
- BatchNorm phía sau che biên độ khi train, nên độ chính xác lúc train **không** bị ảnh hưởng (ρ giữa biên độ và Mask mAP50-95 = 0,32, p = 0,37).

**Giải thích cũ là sai:** `archive/doc/17_SU_CO_FUSE_...md` đổ lỗi cho `model.fuse()` xóa nhánh one2many. Nhưng `nn/modules/head.py:181` cho thấy đánh giá luôn dùng one2one khi `end2end=True`. Lớp hỏng chỉ **trùng tên** `fuse`.

---

## 2. Nhiệm vụ

### T1. Lưu checkpoint FP32, không che lỗi (BẮT BUỘC)

**Tệp:** `archive/ultralytics_Topology-Shape-aware VMamba/engine/trainer.py`, hàm `save_model`, khoảng dòng 712–735.

**Yêu cầu:**
- Xóa khối "resync EMA from live model": vòng lặp `v.copy_(model_sd[k])`.
- Đổi `deepcopy(ema).half()` thành `deepcopy(ema).float()`.
- Xóa vòng lặp `torch.nan_to_num_(v)`.
- Thêm kiểm tra: nếu bất kỳ tensor số thực nào trong `ema.state_dict()` không hữu hạn thì `raise FloatingPointError(f"Non-finite EMA snapshot tensors: {keys}")`.

**Tệp:** `utils/torch_utils.py`, hàm `strip_optimizer`, khoảng dòng 828.

**Yêu cầu:**
- Đổi `x["model"].half()` thành `x["model"].float()`.
- Thêm kiểm tra không hữu hạn tương tự, `raise FloatingPointError`.

**Tham chiếu:** diff đầy đủ trong `../DL_Poylp_v26_VMamba_TestDemo_V2/03_ma_nguon/PATCH_FP32.md`.

**Kiểm tra:**
- Train 1 epoch trên tập con, sau đó `torch.load(best.pt)["model"]`: mọi tensor số thực có `dtype == torch.float32`.
- Kích thước `best.pt` YOLO26s-seg-TSVM khoảng 49,6 MB, không còn 25 MB.

### T2. Đánh giá đúng checkpoint đã lưu và tự phát hiện lỗi (BẮT BUỘC)

Viết script đánh giá **mới**, không sửa script cũ. Script này:
1. Nạp `best.pt` trong **tiến trình Python mới**, ép `model.float().eval()`.
2. **Tắt fuse:** tạm gán `ultralytics.nn.tasks.BaseModel.fuse = lambda self, *a, **k: self`, chạy validator xong thì khôi phục. Đếm số `BatchNorm2d` trước và sau, nếu khác nhau thì báo lỗi.
3. Dùng `SegmentationValidator` với `imgsz=640, conf=0.001, iou=0.7, max_det=300, rect=True, end2end=True, plots=False`.
4. So 4 chỉ số `metrics/mAP50(B)`, `metrics/mAP50-95(B)`, `metrics/mAP50(M)`, `metrics/mAP50-95(M)` với dòng best epoch trong `results.csv`. Best epoch là epoch có (Box mAP50-95 + Mask mAP50-95) lớn nhất. Nếu |chênh| > 0,005 thì `status = "AP_MISMATCH"` và thoát với mã lỗi.
5. Ghi ra `evaluation/metrics.json` có `status`, cùng `evaluation/per_image.csv` gồm TP/FN/FP theo từng ảnh ở `conf > 0.25`, IoU ≥ 0,5.
6. Kiểm tra sha256 của `best.pt` trước và sau, để chắc không bị sửa.

**Tham chiếu:** hàm `evaluate` trong `../DL_Poylp_v26_VMamba_TestDemo_V2/04_kaggle/polyp_v2.py`.

**Kiểm tra:**
- Chạy trên `best.pt` cũ của TSVM seed 5 phải ra `AP_MISMATCH`, tức phát hiện được lỗi.
- Chạy trên `best.pt` FP32 mới train ở T1 phải ra `OK`.

### T3. Thêm tùy chọn LayerNorm cho SS2D, tạo mô hình TSVM-LN (ĐỀ XUẤT)

**Tệp:** `archive/ultralytics_Topology-Shape-aware VMamba/nn/modules/topology_shape_vmamba.py`.

**Yêu cầu:**
- `SS2D.__init__` nhận thêm tham số `out_norm: bool = False`. Khi `True`, đặt `self.out_norm = nn.LayerNorm(self.d_inner)`; khi `False`, đặt `self.out_norm = None`. Viết dòng này ngay trước `self.out_proj`.
- Trong `SS2D.forward`, sau `y = y_0 + y_1 + y_2 + y_3` và **trước** `y = y * F.silu(z)`:
  ```python
  norm = getattr(self, "out_norm", None)  # checkpoint cũ không có thuộc tính này
  if norm is not None:
      y = norm(y.permute(0, 2, 3, 1)).permute(0, 3, 1, 2)
  ```
- Trong `TSVMamba.__init__`: nếu `mode` kết thúc bằng `"_ln"` thì `out_norm=True` và `self.mode = mode[:-3]`, để `forward` dùng chung với mô hình cũ. Truyền `out_norm` vào `SS2D(...)`.
- Tạo `cfg/models/26/yolo26-seg-TopologyShapeVMamba-LN.yaml` bằng cách sao chép `yolo26-seg-TopologyShapeVMamba.yaml`, **chỉ** đổi dòng tầng 10 thành:
  ```yaml
  - [-1, 2, C2TSVMamba, [1024, 0.5, 16, 3, "topology_shape_vmamba_ln"]] # 10
  ```
  Không cần sửa `nn/tasks.py`, vì `parse_model` truyền `mode` theo vị trí `(c1, c2, n, e, d_state, d_conv, mode)`.

**Kiểm tra (viết thành pytest):**
1. **Tương thích ngược:** dựng mô hình từ YAML TSVM cũ (scale `s`, `nc=1`). Danh sách khóa `state_dict` và tổng tham số (**12.254.688**) phải giống fork trước khi sửa.
2. **Giống từng bit:** nạp `best.pt` lịch sử của seed 3, chạy cùng một tensor ngẫu nhiên (`torch.manual_seed(1)`) qua fork trước và sau khi sửa. `torch.equal` phải ra `True`.
3. **TSVM-LN:** tổng tham số **12.255.200** (+512). Khóa mới chỉ gồm `model.10.m.0.vmamba.out_norm.weight` và `.bias`.
4. **Chặn biên độ:** khối `TSVMamba(32)`, nhân trọng số `x_proj` lên 100 lần. Đầu ra bản gốc phải tăng hơn 1.000 lần (đo được khoảng 21.869), bản `_ln` tăng dưới 5 lần (đo được khoảng 2,9).
5. Xóa thuộc tính `out_norm` khỏi một khối cũ, giả lập checkpoint cũ: `forward` vẫn chạy được.

**Tham chiếu:** `../DL_Poylp_v26_VMamba_TestDemo_V2/03_ma_nguon/ultralytics/nn/modules/topology_shape_vmamba.py` và `06_kiem_tra/test_tsvm_ln.py`.

**Lưu ý:** TSVM-LN là **mô hình mới**. Không được báo cáo nó tốt hơn khi chưa train 10 seed và chưa làm kiểm định (xem T6).

### T4. Chẩn đoán FP16 cho mỗi lượt train (KHUYẾN NGHỊ)

Sau khi train, quét `best.pt` FP32 và ghi vào `run.json` mục:
```json
"fp16_risk": {"fp16_max": 65504, "max_abs_value": ..., "bn_layers_over_fp16": [{"layer": "...", "channels_mean_over": n, "channels_var_over": n, ...}], "mean_would_be_clipped": true}
```
Mục đích là đo được, trên các lượt mới, seed nào sẽ hỏng nếu vẫn lưu FP16. Đây là bằng chứng độc lập cho khóa luận.

**Tham chiếu:** hàm `fp16_risk` trong `polyp_v2.py` của V2.

### T5. Sửa tài liệu cho khớp nguyên nhân thật (BẮT BUỘC)

- Trong `archive/doc/17_SU_CO_FUSE_...md` và `archive/doc/GIAI_THICH_SU_CO_FUSE_CHO_NGUOI_DOC.md`: **giữ nội dung lịch sử**, nhưng thêm một khung cảnh báo ở đầu tệp. Khung này nói rõ:
  - nguyên nhân là FP16 cắt thống kê BatchNorm, không phải `fuse()`;
  - câu "`best.pt` nguyên vẹn 100 %" là **sai**;
  - kèm link tới báo cáo mới.
- Cập nhật `CURRENT_PROJECT_STATUS.md` ở mục "Artifact fuse TSVM".
- Mục 4 của `output/BaoCaoKetQua/CNTT_KLCN182_LeDucLuong.docx`:
  - không dùng ma trận nhầm lẫn của TSVM seed 0, 5, 8;
  - bỏ hai dòng TN và độ đặc hiệu tái dựng;
  - thêm kiểm định ghép cặp cho TP (p = 0,45) và FP (p = 0,20).

### T6. Train lại và chọn mô hình (BẮT BUỘC cho kết luận cuối)

| Giai đoạn | Mô hình | Seed | Ghi chú |
|---|---|---|---|
| 0 | baseline, tsvm (tùy chọn thêm tsvm_ln) | 0 | SMOKE 1 epoch để kiểm tra môi trường |
| 1 | baseline, tsvm | 0–9 | Có T1 và T2. Baseline và TSVM phải **cùng cách khởi tạo**: dựng từ YAML rồi `.load("yolo26s-seg.pt")` |
| 2 | tsvm_ln | 0–9 | Có T1, T2 và T3 |

**Quy tắc chọn, chốt trước khi xem kết quả:**
1. Chỉ dùng lượt có `status == "OK"`.
2. Chỉ số chính: Mask mAP50-95, trung bình ± SD mẫu trên 10 seed.
3. Kiểm định ghép cặp theo seed với baseline: t-test (`scipy.stats.ttest_rel`) và Wilcoxon. Chỉ viết "tốt hơn" khi p < 0,05.
4. Nếu TSVM-LN không kém TSVM, ưu tiên TSVM-LN vì ổn định số học và triển khai được ở FP16.

**Tham chiếu:** notebook `../DL_Poylp_v26_VMamba_TestDemo_V2/04_kaggle/TRAIN_KAGGLE.ipynb` (biến `JOBS`) và `polyp_v2.py aggregate`.

---

## 3. Định nghĩa "xong" (Definition of Done)

- [ ] T1: `best.pt` mới là FP32. Có NaN/Inf thì train dừng với `FloatingPointError`.
- [ ] T2: script đánh giá báo `AP_MISMATCH` trên `best.pt` cũ seed 5, báo `OK` trên checkpoint FP32 mới.
- [ ] T3: 5 pytest ở phần Kiểm tra đều đạt. Chế độ cũ giống từng bit.
- [ ] T4: `run.json` có `fp16_risk`.
- [ ] T5: tài liệu cũ có khung cảnh báo; `CURRENT_PROJECT_STATUS.md` đã cập nhật.
- [ ] T6: đủ 20 lượt (giai đoạn 1), hoặc 30 lượt (thêm giai đoạn 2), đều `OK`; có bảng mean ± SD và `paired_tests`.
- [ ] Báo cáo cuối gắn nhãn Đã xác nhận / Suy luận / Chưa xác minh cho mọi nhận định.

## 4. Những điều AI KHÔNG được làm

- Không dùng checkpoint cũ đã "hiệu chỉnh BatchNorm" làm kết quả chính thức. Nó chỉ là bằng chứng.
- Không xóa hay ghi đè kết quả cũ. Không chép đè `results.csv`.
- Không giảm batch hay đổi tham số cho riêng một lượt.
- Không gộp các lượt train bằng code khác nhau.
- Không gọi module là "topology-aware" hay "tốt hơn" khi số liệu và kiểm định chưa đủ căn cứ.

## 5. Điểm còn mở (Chưa xác minh) để AI hoặc nhóm kiểm tra thêm

1. VMamba gốc có `out_norm` (LayerNorm) ở vị trí T3 hay không. Cần đối chiếu mã nguồn VMamba chính thức.
2. Tham số `A_logs` của SS2D gần như không đổi sau 100 epoch (lệch khoảng 0,001 so với khởi tạo) ở mọi seed. Chưa rõ nguyên nhân: gradient rất nhỏ, hay một lý do khác.
3. Nhánh shape (biên độ khoảng 6–10) có bị nhánh VMamba (biên độ khoảng 10⁶) lấn át trong phép ghép trước `fuse` hay không. Đề xuất thí nghiệm loại bỏ: cho nhánh `s` bằng 0 trong `cat`, rồi đo lại mAP.
4. Cách Kaggle trừ quota khi dùng T4 x2.
