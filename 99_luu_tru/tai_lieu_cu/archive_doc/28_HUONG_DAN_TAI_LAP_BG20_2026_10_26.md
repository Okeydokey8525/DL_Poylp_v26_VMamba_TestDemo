# Tái lập dữ liệu BG 20 trong workspace hiện tại

Cập nhật 26/10/2026. Hướng dẫn này phân biệt **bộ dữ liệu đang dùng** với **bản tái tạo mới**. Không chạy chương trình chuyển đổi để ghi đè ảnh/nhãn hoặc kết quả huấn luyện đã công bố.

## Đường dẫn và môi trường

Từ thư mục `archive`:

- Dữ liệu hiện hành: `Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/`.
- Ảnh/mask gốc: `Ket_Qua_V2/Data Prosessing/Kvasir-SEG/{images,masks}/`.
- Ảnh âm: `Ket_Qua_V2/Data Prosessing/normal-cecum/normal-cecum/` (builder tự nhận dạng lớp thư mục lồng này).
- Split cố định: `train.txt` và `val.txt` tại gốc archive. Chưa đủ provenance để khẳng định nhóm tác giả dataset phát hành hai danh sách này.
- Builder đúng cho BG 20: `Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py`. `Stracth/Du_Lieu/convert_kvasir_to_yolo_seg.py` chỉ chuyển phần polyp, không tự bổ sung 200 ảnh nền.
- Cấu hình dùng ngay: `data_bg20.yaml`; trường path là đường dẫn tuyệt đối tới dữ liệu hiện hành. Khi chuyển máy, tạo cấu hình local tương ứng, không giả định path tương đối của Ultralytics luôn tính từ YAML.

Kiểm toán đã dùng Python 3.12.14, OpenCV 4.12.0, NumPy 2.2.6 cho replay nhãn. Builder cầnPython 3.12,OpenCV,NumPy; tqdm chỉ dùng cho progress và có fallback khi thiếu. Không trộn phiên bản rồi cam kết byte-identical mà chưa kiểm lại. Phiên bản của lần tạo mới được lưu trong `reproduction_environment.json`.

## Kiểm tra trước khi ghi

```powershell
python "Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py" --help
python "Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py" --dry-run
```

`--dry-run` kiểm nguồn/split và danh sách 200 ảnh nền, không tạo output hoặc cập nhật YAML đang dùng. Script xác định archive từ vị trí chính nó; không phụ thuộc cwd. Có thể chỉ định `--archive-root`, `--source-root`, `--output` khi layout khác.

## Tạo bản tái lập riêng

```powershell
python "Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py" --output "generated/Kvasir_YOLO_SEG_BG20_replay_20261026"
```

Đầu ra mặc định là `generated/Kvasir_YOLO_SEG_BG20_replay`. Mọi đường dẫn output tương đối được tính từ archive. Script **từ chối thư mục đã tồn tại**, từ chối output bên trong nguồn ảnh/mask và không xóa đệ quy. Nó chỉ ghi YAML vào output mới, không ghi đè `archive/data_bg20.yaml`. Muốn tạo lần khác, chọn tên thư mục output mới.

## Các bước dữ liệu và kiểm chứng

1. Giữ split 880/120 của ảnh polyp.
2. Mặt nạBGR→gray, Otsu, morphology close 3×3 một lần; external contours, loại area<20 px².
3. `approxPolyDP` với epsilon 0,002×chu vi, fallback contour khi ít hơn 3 đỉnh; chuẩn hóa và ghi 6 chữ số thập phân.
4. Sắp tên 1.000 ảnh normal-cecum, seed 42 chọn 200;160 train và 40 val. Ảnh âm có prefixbg_ và label rỗng.
5. Kiểm 1.040 ảnh/nhãntrain,160 ảnh/nhãnval,160/40 label rỗng; so hash ảnh, nhãn và danh sách với bộ hiện hành.

Không chỉ kiểm count. Kiểm toán tái tạo 1.000 mask cho Otsu 5–8;1.206 contour,loại 143,giữ 1.063; vertices trung bình 333,1552→24,6369. 999/1.000 nhãn trùng từng ký tự ở môi trường đã nêu. `ck2bxiswtxuw80838qkisqjwz.txt` khác một đỉnh khoảng 3 px; hai polygon có IoU 0,99981118 và 27 pixel raster khác. **Chưa xác định nguyên nhân**; không tự thay nhãn validation để làm kết quả đẹp hơn. Các ảnh polyp và 200 ảnh nền sao chép khớp byte.

Bằng chứng: [preprocessing độc lập](../audit_20261025_193105/root/preprocessing_independent.json), [replay bằng hàm builder và kiểm raster](../audit_20261025_193105/B_visual/dataset_label_crosscheck.json). Tệp và nhãn hiện hành được giữ nguyên.

## Dùng cho huấn luyện và đánh giá

Baseline nạp `yolo26s-seg.pt`; TSVM dựng YAML scale s và nạp phần pretrained tương thích từ cùng nguồn. TSVM phải import đúng fork `ultralytics_Topology-Shape-aware_VMamba_FP32/`, trainamp=False, lưu FP32 và suy luậnhalf=False. In đường dẫn import và phiên bản thực dùng. Hai notebook trong `Cell Kaggle/` chạy từng seed; notebook TSVM lịch sử có đường dẫn fork cũ nên phải điều chỉnh đúng môi trường trước dùng, không coi đổi tên run là xác nhận FP32.

Giữ args,CSV,hashcheckpoint,code/YAML và hashdataset cùng log. Không train hoặc suy luận trên output mới rồi gán kết quả sang run cũ. Cấu hình Kaggle do notebook tạo theo mount Kaggle; sửa pathlocal không chứng minh historical Kaggle đã dùng sai dữ liệu.

Validator trong train dùng rectangular validation và batch 16 khi batchtrain 8. Kiểm toán replaybest.pt dùngrect=True,batch 16,imgsz 640,half=False,CPU và bản sao validation riêng. Một probe rect=False,batch 4 có AP khác, không được tính là lỗi checkpoint trước khi đồng nhất giao thức. Bảng chính chọn max-mask, còn best.pt chọn fitness box+mask;16/40 run khác epoch.

## Kết quả và hiện vật legacy

Dùng [gói 20 seed](../Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/README.md) và các bảng chuẩn bên trong thư mục 01–06. [LEGACY_ARTIFACTS](../Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/LEGACY_ARTIFACTS.md) chỉ rõ trường TN sai và cột winsloss ngược chiều trong các tệp gốc cũ. Không sửa raw hoặc đọc đè các trường đó như dữ liệu đo. Chưa có Dice pixel, topology hay testngoài; chưa đánh giáTurnitin 30%.

## Builder báo cáo Markdown lịch sử

`Stracth/Bao_Cao/build_huit_final_report_from_md.py` không còn ghi đè báo cáo chính mặc định. Nó chặn các tệp có marker lịch sử. Nếu cần một bản sao lịch sử để truy vết, phải truyền `--allow-historical-drafts --output <tệp-docx-mới>`; hai đường dẫn Word chính và mọi tệp đã tồn tại vẫn bị từ chối. Opt-in không xác nhận các claim cũ là đúng. Không chạy các builder báo cáo khác lên bản Word hiện tại trước khi kiểm tra nguồn và output.
