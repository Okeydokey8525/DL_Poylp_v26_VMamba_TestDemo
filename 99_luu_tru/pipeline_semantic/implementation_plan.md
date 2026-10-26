# Kvasir-SEG Semantic Segmentation Pipeline — Implementation Record

> Đây là **pipeline phụ trợ** cho semantic segmentation, không phải pipeline huấn luyện chính BG20 YOLO26s.
>
> Trạng thái: các file triển khai tương ứng đã tồn tại trong repository. Nội dung dưới đây được giữ để mô tả yêu cầu và implementation contract của pipeline.

## Mục đích

Pipeline chuẩn bị Kvasir-SEG và lớp PyTorch Dataset cho các nghiên cứu semantic segmentation như U-Net/PraNet, giữ split từ `train.txt` và `val.txt`.

## Input CLI

Script `data_prep/prepare_kvasir_semantic.py` nhận:

- `--images-dir`
- `--masks-dir`
- `--train-list`
- `--val-list`
- `--output-dir`
- `--expected-train-count` (mặc định 880)
- `--expected-val-count` (mặc định 120)

## Split và output

Split được lấy trực tiếp từ `train.txt` và `val.txt`.

Output semantic dataset:

`Kvasir_Semantic_880_120/`

gồm train/val images, masks_original, masks_binary, splits, manifest, summary và QA.

## Quy tắc xử lý

- Giữ resolution gốc; resize do transform lúc train.
- Binary mask: grayscale, pixel >127 → 255, còn lại → 0.
- PNG lossless.
- Hash SHA-256 cho integrity.
- Kiểm tra duplicate stem/hash, missing pair và mask bất thường.
- `split_manifest.csv` bắt buộc.
- Dataset PyTorch trả image [3,H,W] float32 và mask [1,H,W] float32; không double-normalize.
- Không overwrite âm thầm khi output tồn tại.
- Unit/integration tests được hỗ trợ; integration real-data có thể skip nếu thiếu environment configuration.

## Source files

- `data_prep/prepare_kvasir_semantic.py`
- `datasets/kvasir_semantic_dataset.py`
- `tests/unit/`
- `tests/integration/`

## Lưu ý

Pipeline này mô tả semantic dataset 880/120. Nó **không phải** metadata của dataset BG20 1.200 ảnh dùng trong các thực nghiệm YOLO26s hiện tại.

Xem `CURRENT_PROJECT_STATUS.md` để biết trạng thái dự án nghiên cứu chính.
