# 05. Cấu hình huấn luyện

## Nguồn

- `args.yaml` của 40 lượt trong `03_ket_qua_huan_luyen/`, được script so sánh từng tham số: [bang/03_cau_hinh_args.csv](bang/03_cau_hinh_args.csv).
- Notebook Kaggle: [`kvasir-yolo26s-seg.ipynb`](<../02_ma_nguon/notebook_kaggle/kvasir-yolo26s-seg.ipynb>) (Baseline) và [`kvasir-yolo26s-seg-topology-shape-awar.ipynb`](<../02_ma_nguon/notebook_kaggle/kvasir-yolo26s-seg-topology-shape-awar.ipynb>) (TSVM).

## Siêu tham số (trùng nhau ở cả 40 lượt)

| Nhóm | Tham số |
|---|---|
| Dữ liệu | `data_bg20.yaml` do notebook tạo (`nc: 1`, `names: {0: polyp}`), imgsz 640, `rect=False`, `cache=False` |
| Tối ưu | AdamW, lr0 0,001, lrf 0,01, momentum 0,937, weight_decay 0,0005, warmup 5 epoch, `cos_lr=False` |
| Lịch huấn luyện | 100 epoch, batch 8, `patience=100` (không dừng sớm), `close_mosaic=10` (tắt mosaic ở 10 epoch cuối) |
| Tăng cường | mosaic 1,0, mixup 0, fliplr 0,5, flipud 0, degrees 0, scale 0,5, translate 0,1, HSV (0,015 / 0,7 / 0,4) |
| Mặt nạ | `overlap_mask=True`, `mask_ratio=4` |
| Đánh giá trong lúc huấn luyện | iou 0,7, `conf=None` (mặc định), max_det 300 |
| Độ chính xác số | `amp=False`: **cả hai mô hình huấn luyện hoàn toàn ở FP32** |
| Tất định | `deterministic=True`, `workers=2`, `seed` = số seed trong tên thư mục (đúng 40/40) |
| Thiết bị | `device: 0` (GPU Kaggle) |

Chỉ có hai tham số khác nhau, và đó chính là phần khác về mô hình:

| Tham số | Baseline | TSVM FP32 |
|---|---|---|
| `model` | `yolo26s-seg.pt` | `/kaggle/working/yolo26s-seg-TopologyShapeVMamba.yaml` (scale `s`) |
| `pretrained` | `True` | `yolo26s-seg.pt` |

Cả hai mô hình đều xuất phát từ trọng số tiền huấn luyện `yolo26s-seg.pt` ([04](04_KIEN_TRUC_TSVM_FP32.md#khởi-tạo-trọng-số)).

## Quy trình trên Kaggle (theo notebook)

1. Tạo `data_bg20.yaml` trỏ tới dataset BG20 đã tải lên Kaggle.
2. Khóa tất định cho từng seed:
   - đặt `PYTHONHASHSEED` và `CUBLAS_WORKSPACE_CONFIG=:4096:8`;
   - đặt seed cho `random`, `numpy` và `torch` (kể cả CUDA);
   - đặt `cudnn.benchmark=False` và `cudnn.deterministic=True`;
   - bật `torch.use_deterministic_algorithms(True)`.
3. Baseline: cài `ultralytics==8.4.127` bằng pip, rồi `YOLO("yolo26s-seg.pt").train(...)`.
4. TSVM: tạo symlink để nạp fork tùy chỉnh làm gói `ultralytics`, chép YAML TSVM và đặt `scale: s`, rồi `YOLO(yaml).load("yolo26s-seg.pt").train(...)`.
5. Nén `runs/` và tải về. Kết quả nằm ở `03_ket_qua_huan_luyen/`.

**Lưu ý về notebook trong repo:** notebook TSVM đang lưu trỏ tới fork **cũ** (`ultralytics_Topology-Shape-aware VMamba`, nay ở `99_luu_tru/ma_nguon_cu/ultralytics_TSVM_cu_FP16/`) và đặt tên run **không có** hậu tố `_FP32`. Vậy đây là phiên bản trước bản vá. Các run `TSVM_FP32` có tên `Kvasir_BG20_YOLO26s_seg_TSVM_FP32_s{seed}_w2` theo `args.yaml`, nên khi chạy chúng notebook đã được sửa đường dẫn và tên. Repo không lưu bản notebook đã sửa này. Bằng chứng gián tiếp cho thấy các run này dùng fork FP32: 20/20 file `best.pt` lưu float32 ([bang/07_checkpoint_best_pt.csv](bang/07_checkpoint_best_pt.csv)), trong khi fork cũ ép float16.

## Môi trường

| | Giá trị | Mức xác minh |
|---|---|---|
| Ultralytics | 8.4.127 | Ghi trong 40/40 file `best.pt` |
| Fork TSVM | `02_ma_nguon/ultralytics_TSVM_FP32/` (8.4.127 cộng TSVM cộng bản vá FP32) | Mã nguồn có trong repo |
| GPU, PyTorch | Ba file log Kaggle trong `99_luu_tru/log_kaggle_cu/` ghi Tesla T4 15 GB, torch 2.10.0+cu128, Python 3.12.13 | Các log này thuộc lượt TSVM **cũ**. Chưa có log gắn với 40 lượt của bộ chính |
| Thời gian huấn luyện (cột `time` ở epoch 100) | Baseline 2,32 giờ (2,16–2,55); TSVM FP32 4,68 giờ (4,52–4,96) | [bang/02_ket_qua_tung_seed.csv](bang/02_ket_qua_tung_seed.csv). Phụ thuộc phần cứng Kaggle cấp cho mỗi lượt |

## Vì sao gọi là TSVM FP32

1. **Sự cố.** Fork TSVM ban đầu lưu checkpoint bằng `.half()` (float16) như Ultralytics gốc. Tham số `running_mean` của BatchNorm `model.10.m.0.fuse.bn` vượt giới hạn float16 (65.504); seed 5 có giá trị khoảng 1,5 triệu. Khi lưu, giá trị bị cắt nên `best.pt` cho kết quả sai khi suy luận.
2. **Bản vá** ([`PATCH_FP32.md`](../02_ma_nguon/ultralytics_TSVM_FP32/PATCH_FP32.md)) sửa 3 chỗ trong 2 file:
   - `save_model` và `MultiTrainer` lưu `.float()` thay cho `.half()`;
   - `strip_optimizer` lưu `.float()`;
   - nếu gặp NaN hoặc Inf thì báo `FloatingPointError` thay vì âm thầm thay bằng 0.
3. **Chạy lại** 20 seed với fork đã vá. Script so sánh `results.csv` của TSVM cũ và TSVM FP32 (seed 0–19): **44.000 ô giống hệt, 2.000 ô khác, và tất cả 2.000 ô khác đều thuộc cột `time`** (log ở mục 3b của [bang/_log_chay.txt](bang/_log_chay.txt)).

**Kết luận:** quá trình huấn luyện cho ra cùng metric từng epoch (đúng với thiết lập tất định). Điểm khác duy nhất là checkpoint TSVM FP32 lưu đúng giá trị float32. "FP32" mô tả **cách lưu checkpoint**, không phải một chế độ huấn luyện khác, vì Baseline cũng huấn luyện với `amp=False`.
