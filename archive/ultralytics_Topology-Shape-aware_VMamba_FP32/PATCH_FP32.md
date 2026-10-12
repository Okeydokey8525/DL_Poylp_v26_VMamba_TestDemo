# Bản vá lưu checkpoint FP32

Thư mục này là bản sao của `archive/ultralytics_Topology-Shape-aware VMamba/` (Ultralytics 8.4.127 + TSVM), tạo ngày 12/10/2026. Bản sao chỉ khác bản gốc ở **3 chỗ trong 2 tệp**. Bản gốc được giữ nguyên.

Lý do: xem `archive/doc/27_SU_CO_FP16_CHECKPOINT_TSVM_VA_CACH_KHAC_PHUC.md`. Thống kê BatchNorm `model.10.m.0.fuse.bn` của TSVM vượt giới hạn FP16 (65.504), nên khi lưu bị cắt và `best.pt` bị sụp.

| Tệp | Hàm | Trước | Sau |
|---|---|---|---|
| `engine/trainer.py` | `save_model` | `deepcopy(ema).half()`, chép đè tensor NaN của EMA bằng tensor của model, rồi `nan_to_num_` | `deepcopy(ema).float()`; nếu có NaN/Inf thì `raise FloatingPointError` |
| `engine/trainer.py` | `MultiTrainer` (`multitrain_base.pt`) | `deepcopy(self.model).half()` | `deepcopy(self.model).float()` |
| `utils/torch_utils.py` | `strip_optimizer` | `x["model"].half()` | `x["model"].float()`; nếu có NaN/Inf thì `raise FloatingPointError` |

Hai thay đổi ở `save_model` và `strip_optimizer` giống với bản vá trong `../DL_Poylp_v26_VMamba_TestDemo_V2/03_ma_nguon/` (`PATCH_FP32.md`). Thay đổi ở `MultiTrainer` là phần bổ sung.

Phần **không đổi**: `convert_optimizer_state_dict_to_fp16` vẫn nén `exp_avg` của optimizer trong `last.pt` (chỉ dùng khi resume, không chứa thống kê BN). Kiến trúc TSVM cũng giữ nguyên, nên trọng số và kết quả train giống bản gốc.

## Đã kiểm tra (12/10/2026, CPU)

- Dựng model TSVM, đặt `running_mean` của BN tầng 10 = 1.503.116 (giá trị thật của seed 5):
  - Bản gốc: `float16`, giá trị lưu = 65.504 (**bị cắt**). Đặt `inf` vào EMA thì vẫn lưu, không báo lỗi.
  - Bản này: `float32`, giá trị lưu = 1.503.116 (**giữ nguyên**) qua cả `save_model` lẫn `strip_optimizer`. Đặt `inf` vào EMA thì `FloatingPointError`.
- `tests/test_topology_shape_vmamba.py`: 22 đạt, 2 bỏ qua, 1 lỗi. Lỗi là `test_00_baseline_yaml_integrity`, **có sẵn ở bản gốc**: Windows đổi xuống dòng của `yolo26-seg.yaml` sang CRLF; đổi về LF thì SHA256 khớp.

## Dùng trên Kaggle

- Nạp thư mục này làm gói `ultralytics` (symlink hoặc `importlib`) thay cho bản gốc.
- Giữ `amp=False`. Validate/predict với `half=False`.
- Sau khi train, kiểm tra:
  - `best.pt` của TSVM s khoảng 49 MB (FP32), không phải khoảng 25 MB.
  - Mask mAP khi validate `best.pt` lệch ≤ 0,005 so với epoch có fitness cao nhất trong `results.csv`.
