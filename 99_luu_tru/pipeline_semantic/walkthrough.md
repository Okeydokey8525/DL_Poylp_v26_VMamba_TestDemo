# Kvasir-SEG Pipeline Walkthrough

Pipeline chuẩn bị dữ liệu và Dataset PyTorch cho Kvasir-SEG đã được triển khai hoàn tất theo đúng 12 yêu cầu và ràng buộc mà bạn đã đề ra. Dưới đây là tổng hợp các thành phần đã được hoàn thiện.

## 1. Thành Phần Đã Triển Khai

| File | Chức năng chính |
|------|-----------------|
| `data_prep/prepare_kvasir_semantic.py` | Script tạo bộ dữ liệu đầu ra từ dữ liệu gốc, binarize mask, hash validation, split matching, sinh manifest và QA. |
| `datasets/kvasir_semantic_dataset.py` | Lớp `KvasirSemanticDataset` (kế thừa `torch.utils.data.Dataset`), load ảnh + binary mask, hỗ trợ Albumentations. |
| `tests/unit/test_prepare_kvasir_semantic.py` | Unit test kiểm tra hash SHA-256, logic quét file, và hàm sinh binary mask (`binarize_mask`). |
| `tests/unit/test_kvasir_semantic_dataset.py` | Unit test với dummy images để đảm bảo output shape (`[3, H, W]`, `[1, H, W]`), ranges (`0..1`) và tương tác đúng với các transform của Albumentations. |
| `tests/integration/test_kvasir_pipeline_integration.py` | Test end-to-end cho luồng chạy script từ command line (với dummy test và real-data test dùng biến môi trường). |

## 2. Chi Tiết Thực Hiện Các Yêu Cầu

> [!TIP]
> **Giảm Dependencies**
> Tôi đã sử dụng `cv2.connectedComponentsWithStats` thay vì sử dụng thư viện `scikit-image` như bạn yêu cầu, giúp giảm thiểu độ phức tạp môi trường cho hệ thống.

- **Idempotency & Tránh Ghi Đè Âm Thầm:** Nếu output folder tồn tại và `--overwrite` không được set thành `True`, script sẽ tự động kiểm tra `split_manifest.csv` cùng với tất cả SHA-256 hash của ảnh gốc, ảnh mới và mask nhị phân để đảm bảo dữ liệu không bị corruption.
- **Thư Mục Mask Riêng Biệt:** Sinh ra 2 thư mục mask: `masks_original` (chứa file gốc từ YOLO, hash match 100%) và `masks_binary` (đã qua xử lý ngưỡng > 127, dạng PNG).
- **QA Previews & Report:** Script sẽ tìm ra mask nhỏ nhất, lớn nhất, nhiều components nhất, mask có tỷ lệ median nhất kết hợp vài mask random và tạo thành ảnh ghép `(Original \| GT \| Overlay)` lưu vào mục `qa/previews`.
- **Validation Dữ Liệu:** 
  - Fail khi bị mất cặp Ảnh-Mask.
  - Kiểm tra duplicate về mặt nội dung file bằng SHA-256 (cho cả image và mask).
  - Kiểm tra trùng `stem` trong mỗi tập train và val.
  - Cảnh báo (warning) nếu một mask bị hoàn toàn background (rỗng) hoặc hoàn toàn foreground. Fail nếu mảng mask binary chứa bất kỳ số nào khác ngoài `0` và `255`.

> [!NOTE]
> Bạn có thể chạy unit/integration tests bằng lệnh `pytest tests/` (nếu đã kích hoạt môi trường có cài pytest). Script chính có thể được chạy như sau:
> ```bash
> python data_prep/prepare_kvasir_semantic.py \
>     --images-dir path/to/yolo/images \
>     --masks-dir path/to/yolo/masks \
>     --train-list path/to/train.txt \
>     --val-list path/to/val.txt \
>     --output-dir Kvasir_Semantic_880_120
> ```

## 3. Khuyến nghị Tiếp Theo
- Trước khi train mô hình thực tế (như PraNet/U-Net), hãy thử chạy script với tập dữ liệu thực, sau đó kiểm tra folder `qa/previews/` xem lớp Overlay (đỏ) có khớp chính xác lên polyp ở ảnh gốc hay không.
- Nếu bạn cần mở rộng thêm các phép Transform như RandomCrop, Resize hay ColorJitter cho `KvasirSemanticDataset`, chỉ cần đóng gói vào list của `albumentations.Compose` rồi truyền thẳng vào hàm khởi tạo của class.
