# Kvasir-SEG Semantic Segmentation Pipeline - Implementation Plan

Dự án này nhằm mục đích xây dựng một pipeline chuẩn bị dữ liệu và lớp PyTorch Dataset cho bộ dữ liệu Kvasir-SEG, đặc biệt phục vụ cho các mô hình semantic segmentation như U-Net và PraNet, đồng thời giữ nguyên chính xác phân chia (split) từ file `train.txt` và `val.txt` gốc.

## Kế hoạch Cập nhật & Ràng buộc Mới
1. **Input CLI:** Script nhận `--images-dir`, `--masks-dir`, `--train-list`, `--val-list`, `--output-dir`. Tuỳ chọn `--expected-train-count` (mặc định 880) và `--expected-val-count` (mặc định 120).
2. **Split Data:** Lấy split trực tiếp từ `train.txt` và `val.txt`, không quét thư mục YOLO.
3. **Image/Mask Resolution:** Giữ nguyên kích thước gốc. Việc resize được giao phó cho Albumentations transform lúc huấn luyện.
4. **Output Structure:** 
   ```text
   Kvasir_Semantic_880_120/
   ├── train/
   │   ├── images/
   │   ├── masks_original/
   │   └── masks_binary/
   ├── val/
   │   ├── images/
   │   ├── masks_original/
   │   └── masks_binary/
   ├── splits/
   │   ├── train.txt
   │   └── val.txt
   ├── split_manifest.csv
   ├── dataset_summary.json
   └── qa/
       ├── qa_report.md
       └── previews/
           ├── train/
           └── val/
   ```
5. **Giảm Dependency:** Sử dụng `cv2.connectedComponentsWithStats` thay cho `scikit-image`.
6. **Binary Mask Rule:** Đọc ảnh sang grayscale. Pixel `> 127` thành `255`, ngược lại thành `0`. Lưu dạng PNG lossless. Ràng buộc ghi chú quy tắc này vào summary và report.
7. **Validation & Checks:**
   - Cùng stem (duplicate stem) hoặc nhiều file cho cùng một stem.
   - Trùng lặp nội dung theo mã băm SHA-256 (nội bộ split và chéo train-val).
   - Mask bất thường: Rỗng (all 0) hoặc Kín (all 255).
   - Hash Integrity: Khớp mã SHA-256 giữa source và output.
   - Ràng buộc binary mask chỉ có 2 giá trị 0 và 255.
8. **Manifest File:** `split_manifest.csv` là bắt buộc, ghi lại source path, output path, và SHA-256 hash cho từng ảnh và mask.
9. **PyTorch Dataset:**
   - Không transform: trả về image `[3, H, W]` float32 (range `0-1`) và mask `[1, H, W]` float32 (values `0, 1`).
   - Có transform: trả về nguyên gốc theo transform, tuyệt đối không tự scale/normalize lần 2.
10. **Idempotency (Overwrite Logic):** 
    - Nếu folder tồn tại và `--overwrite=False`: Kiểm tra `split_manifest.csv` và kiểm tra hash để đảm bảo toàn vẹn. Nếu hoàn chỉnh thì skip; nếu không hoàn chỉnh hoặc lỗi thì báo fail rõ ràng. Không âm thầm ghi đè.
11. **Testing:** Unit test với dữ liệu dummy. Integration test với real data bị skip nếu thiếu biến môi trường cấu hình đường dẫn.

## Proposed Changes (Cấu trúc file nguồn)
- `data_prep/prepare_kvasir_semantic.py`
- `datasets/kvasir_semantic_dataset.py`
- `tests/unit/test_kvasir_semantic_dataset.py`
- `tests/unit/test_prepare_kvasir_semantic.py`
- `tests/integration/test_kvasir_pipeline_integration.py`

*(Kế hoạch đã được cập nhật và duyệt, sẽ tiến hành triển khai mã nguồn ngay lập tức)*
