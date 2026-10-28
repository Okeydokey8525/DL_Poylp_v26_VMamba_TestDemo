# Quy trình "kiểm tra kaggle": ablation `shape_only`

Khi Huy ra lệnh **"kiểm tra kaggle"** (hoặc "tải kết quả kaggle"), làm đúng các bước dưới đây. Thư mục đích là `03_ket_qua_huan_luyen/Shape_only/`.

## Thông tin cố định

| Mục | Giá trị |
|---|---|
| Tài khoản Kaggle | `huyphngtun`. Key ở `C:\Users\huyth\.kaggle\kaggle.json`, **không** đặt key trong repo |
| Kernel | `huyphngtun/kvasir-tsvm-abl-shape-only-s<SEED>` (mỗi seed một kernel) |
| Đã gửi | seed 4 (xong 27/10/2026, 2,24 giờ), seed 3 (gửi 27/10/2026 22:53) |
| Notebook nguồn | `02_ma_nguon/notebook_kaggle/ablation/kvasir-yolo26s-seg-tsvm-ablation.ipynb` |
| File kết quả trên Kaggle | `runs_Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s<SEED>_w2.zip` (bên trong: `runs/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s<SEED>_w2/`) |
| Thư mục đích mỗi seed | `03_ket_qua_huan_luyen/Shape_only/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s<SEED>_w2/` |

Trên Windows, mọi lệnh `kaggle` phải chạy với `PYTHONUTF8=1`. Nếu thiếu, CLI ghi log lỗi vì ký tự ❌/✅ và tạo ra file log rỗng.

## Bước 1: Kiểm tra trạng thái

```bash
export PYTHONUTF8=1
kaggle kernels list --mine --page-size 20 | grep abl-shape-only
for s in 4 3; do kaggle kernels status huyphngtun/kvasir-tsvm-abl-shape-only-s$s; done
```

- `RUNNING`: báo là đang chạy và đã chạy bao lâu (mỗi lượt khoảng 2,2 giờ). Dừng ở đây.
- `ERROR`: tải log (bước 2, chỉ lấy `.log`), tìm `Traceback` hoặc `AssertionError`, báo lỗi ở cell nào. **Không** tự gửi lại khi chưa hỏi Huy.
- `COMPLETE`: sang bước 2.

## Bước 2: Đọc log, xác nhận lượt chạy hợp lệ

Chỉ tải log, chưa tải zip:

```bash
kaggle kernels output huyphngtun/kvasir-tsvm-abl-shape-only-s<SEED> -p <scratchpad>/kg_s<SEED> --file-pattern '.*\.log$' --force
```

Log phải có đủ 4 dòng sau, thiếu dòng nào thì dừng và báo:

1. `Ablation: MODE=shape_only, SEED=<SEED>`
2. `Tham số tầng 10 = 1,331,969 (mong đợi 1,331,969)`
3. `100 epochs completed in ... hours.`
4. `adding: runs/.../weights/best.pt`

## Bước 3: Tải zip và giải nén vào `Shape_only/`

Chỉ làm bước này khi Huy yêu cầu tải về. Nếu chỉ nói "kiểm tra" thì báo kết quả bước 1–2 và để zip trên Kaggle.

```bash
kaggle kernels output huyphngtun/kvasir-tsvm-abl-shape-only-s<SEED> -p <scratchpad>/kg_s<SEED> --file-pattern 'runs_.*\.zip$' --force
unzip -q <scratchpad>/kg_s<SEED>/runs_*.zip -d <scratchpad>/kg_s<SEED>/unz
mv <scratchpad>/kg_s<SEED>/unz/runs/Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s<SEED>_w2 03_ket_qua_huan_luyen/Shape_only/
```

- Nếu thư mục đích đã tồn tại thì **không ghi đè**. Hỏi Huy trước.
- Giữ file zip trên Kaggle, không xóa kernel.

## Bước 4: Kiểm tra kết quả đã tải

Trong thư mục run vừa giải nén:

- Có đủ `args.yaml`, `results.csv`, `weights/best.pt`, `weights/last.pt`, các hình `Mask*`, `Box*`, `confusion_matrix*.png`.
- `results.csv` có đủ 100 dòng epoch.
- So `args.yaml` với `03_ket_qua_huan_luyen/TSVM_FP32/Kvasir_BG20_YOLO26s_seg_TSVM_FP32_s<SEED>_w2/args.yaml`. Chỉ được khác ở `model`, `name`, `save_dir`, `data` (đường dẫn) và `pretrained`. Siêu tham số (epochs, batch, lr0, optimizer, seed, amp, close_mosaic…) phải giống hệt.
- `best.pt` phải là FP32 (khoảng 45 MB trở lên, không phải khoảng 22 MB).

## Bước 5: Báo kết quả

Dùng cùng quy tắc với phân tích 20 seed: lấy **giá trị lớn nhất của `metrics/mAP50-95(M)` trong `results.csv`**. Không dùng số in ra khi validate `best.pt`, vì hai số này được tính khác nhau.

| Seed | Baseline | TSVM đầy đủ | shape_only |
|---:|---:|---:|---:|
| 4 | 0,7274 | 0,7197 | (điền) |
| 3 | (lấy từ `results.csv`) | (lấy từ `results.csv`) | (điền) |

Ghi kèm: epoch đạt cực đại, Mask P/R tại epoch đó và thời gian train. Nhắc lại giới hạn: số seed ít nên chỉ cho thấy xu hướng, chưa đủ cho ý nghĩa thống kê.

## Lưu ý về git

- `.gitignore` loại `*.pt` và `*.zip`, nên trọng số không lên GitHub. Commit phần còn lại lên nhánh `phungtuanhuy18` **chỉ khi Huy bảo**.
- Không push khi Huy chưa yêu cầu.
