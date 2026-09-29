# Repository Guidelines

## Cấu trúc dự án

- `data_prep/prepare_kvasir_semantic.py` tạo bộ dữ liệu semantic từ ảnh và mask Kvasir; `datasets/kvasir_semantic_dataset.py` nạp dữ liệu cho PyTorch.
- `datasets/Kvasir_Semantic_880_120/` lưu danh sách chia tập, manifest và báo cáo QA; ảnh và mask không được Git theo dõi.
- `tests/unit/` kiểm tra hàm xử lý dữ liệu và dataset; `tests/integration/` kiểm tra pipeline từ đầu đến cuối.
- `archive/ultralytics_Topology-Shape-aware VMamba/` chứa mã YOLO tùy biến; phần còn lại của `archive/` lưu dữ liệu và kết quả thực nghiệm.

## Lệnh phát triển và kiểm thử

Chạy từ thư mục gốc, với Python 3.10+ và các thư viện `pytest`, `numpy`, `opencv-python`, `torch`.

```bash
python -m pytest tests/unit -q
python -m pytest tests/integration -q
python data_prep/prepare_kvasir_semantic.py --help
python smoke_test.py
```

Hai lệnh đầu chạy kiểm thử; `--help` liệt kê tham số chuẩn bị dữ liệu; `smoke_test.py` in thông tin mẫu train/val để kiểm tra thủ công. Khi tạo dữ liệu thật, truyền đường dẫn ảnh, mask, danh sách chia tập và thư mục đầu ra theo `--help`. Không có bước build riêng.

## Quy ước mã nguồn

Dùng thụt lề 4 dấu cách cho Python, tên tệp/hàm/biến dạng `snake_case`, tên lớp dạng `PascalCase`. Ưu tiên đường dẫn tương đối và `pathlib.Path`. Chưa có formatter hoặc linter chung; giữ phong cách của tệp đang sửa, tránh định dạng lại hàng loạt mã trong `archive/`.

## Hướng dẫn kiểm thử

Dùng `pytest`; đặt tệp `test_*.py` và hàm `test_*`. Thêm unit test cho logic mới, integration test khi đổi CLI hoặc cấu trúc đầu ra. Kiểm thử dữ liệu thật cần `KVASIR_IMAGES_DIR`, `KVASIR_MASKS_DIR`, `KVASIR_TRAIN_LIST`, `KVASIR_VAL_LIST`; ca này được bỏ qua nếu thiếu đường dẫn ảnh hoặc mask. Chưa có ngưỡng coverage.

## Commit và pull request

Commit thường có mô tả ngắn bằng tiếng Việt như `chỉnh đường dẫn`; đôi khi dùng `docs:`. Viết tiêu đề cụ thể. Pull request cần nêu mục đích, tệp liên quan, lệnh kiểm thử đã chạy và issue nếu có. Với thay đổi trực quan, đính kèm ảnh hoặc đường dẫn báo cáo. Không commit checkpoint (`*.pt`, `*.pth`, `*.onnx`) hay dữ liệu ảnh lớn bị `.gitignore` loại trừ.
