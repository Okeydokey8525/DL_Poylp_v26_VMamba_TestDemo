# Kiểm tra báo cáo xây dựng dữ liệu và tiền xử lý

Ngày kiểm tra: 10/10/2026. Phạm vi: nguồn dữ liệu, phân chia BG20, chuyển mặt nạ sang đa giác, xử lý khi nạp ảnh, nguồn hình và mức độ phù hợp với chương tiền xử lý.

**Kết luận: số liệu và quy trình cốt lõi khớp dữ liệu/mã nguồn hiện có; báo cáo chưa nên được xem là hoàn toàn chính xác về cách diễn đạt và dẫn nguồn.** Có 7 điểm cần chỉnh hoặc làm rõ bên dưới. Không phát hiện sai số lượng ảnh, nhãn hỏng, sai danh sách chia tập hay hình không tái tạo được. Đây là kiểm tra dữ liệu và tài liệu, không phải đánh giá hiệu quả mô hình hay xác nhận lâm sàng.

Đã đọc cả `Chuong3_XayDungDuLieu_TienXuLy.docx` và `Chuong3_XayDungDuLieu_TienXuLy_co_nguon.docx`. Nội dung đoạn văn của hai bản giống nhau khi bỏ các dòng “Nguồn:”; hai bảng cũng giống nhau. Bản có nguồn là đối tượng đối chiếu chính; số trang dưới đây theo bản PDF dựng lại bằng Word, gồm 17 trang. `xem_truoc_nguon_anh.docx/pdf` là tài liệu xem trước cách ghi nguồn hình, không phải bản đầy đủ của chương.

## Kết quả đối chiếu trực tiếp

| Nội dung trong báo cáo | Kết quả kiểm tra mới | Đánh giá |
| --- | --- | --- |
| Train 880 polyp + 160 nền; val 120 polyp + 40 nền | Train 1.040 ảnh/1.040 nhãn, val 160 ảnh/160 nhãn; 160/40 nhãn rỗng | Đúng |
| Danh sách polyp 880/120 có sẵn từ tác giả | Hai danh sách địa phương khớp từng ID và đúng thứ tự với hai tệp trong GitHub của Debesh Jha | Đúng nội dung; cần dẫn nguồn trực tiếp |
| 200 ảnh nền chọn bằng seed 42 | Sắp xếp 1.000 tên ảnh rồi `random.Random(42).sample(..., 200)` tái tạo đúng thứ tự của hai danh sách 160/40 và đúng tập ảnh đã sao chép | Đúng |
| BG20 là 20% so với 1.000 ảnh polyp | 200/1.000 = 20%; 200/1.200 = 16,67%; nền train 15,38%, nền val 25% | Đúng |
| 936/127 dòng đa giác, tổng 1.063 | Đếm trực tiếp đúng 936/127; mọi dòng lớp 0, ít nhất 3 đỉnh, tọa độ hữu hạn trong [0,1] | Đúng số dòng; cần phân biệt với số polyp thực |
| Không thiếu ảnh/nhãn, không trùng hoàn toàn train/val | Không thiếu cặp; không trùng stem và SHA-256 giữa hai tập; cũng không có tệp ảnh trùng byte trong từng tập | Đúng trong giới hạn phép kiểm |
| Ảnh gốc được sao chép nguyên vẹn | SHA-256 của cả 1.200 ảnh BG20 khớp nguồn cục bộ tương ứng, gồm cả 200 ảnh nền | Đúng |
| Chuyển lại 1.000 mặt nạ thu được cùng nhãn | Cả 1.000 nội dung nhãn khớp. Tệp lưu dùng CRLF, chuỗi trả về của hàm dùng LF; khi ghi theo quy ước Windows thì khớp byte | Đúng; phân biệt nội dung và ký tự xuống dòng |
| Otsu, Closing 3×3 một lần, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE, lọc diện tích <20, epsilon 0,002×chu vi | Khớp hàm `convert_mask_to_yolo_polygons` đang có | Đúng |
| 1.206 đường bao, bỏ 143, giữ 1.063 | Tính lại từ 1.000 mặt nạ cho đúng các giá trị này | Đúng |
| Điểm trung bình 333,2 → 24,6; giảm 92,6%; 10–80 đỉnh | Tính lại 333,1552 → 24,6369; giảm 92,60499%; 10–80 | Đúng |
| 333 kích thước; W 332–1.920; H 352–1.072; phổ biến 622×530 | Tính lại khớp; kích thước 622×530 có 78 ảnh | Đúng |
| 1.000 ảnh normal-cecum đều 720×576 | Kiểm tra toàn bộ 1.000 ảnh nguồn, không chỉ 200 ảnh chọn, đều đúng | Đúng cho bản dữ liệu cục bộ |
| Otsu 5–8; hình 3.2 có 15 mức xám, 377 → 21 điểm | Tính lại khớp; ID `cju1ats0y372e08011yazcsxm` | Đúng |
| Hình 3.3: 1.920×1.072 → 640×358, viền trên/dưới 141 | Tái tạo khớp; ID `cjyzul1qggwwj07216mhiv5sy` | Đúng cho minh họa khung vuông |
| imgsz 640, batch 8, mask_ratio 4, overlap_mask=true; thông số tăng cường | 20 `args.yaml` của baseline và TSVM cùng bộ giá trị tiền xử lý được kiểm tra | Đúng về cấu hình đã lưu |
| BGR→RGB, HWC→CHW, chia 255; không chuẩn hóa ImageNet | Khớp `Format` và `preprocess_batch`; cấu hình bgr=0 | Đúng |
| Albumentations đã bật trong lần TSVM seed 0 | `output/tien_xu_ly/kiem_tra/bang_chung/seed0_log.txt:62` ghi Blur, MedianBlur, ToGray, CLAHE, mỗi phép p=0,01 | Có bằng chứng nhật ký |

Bằng chứng máy đọc: [bang_chung_kiem_tra.json](bang_chung_kiem_tra.json). Mã kiểm tra: [kiem_tra_du_lieu.py](kiem_tra_du_lieu.py). Mã chỉ trích xuất hàm chuyển mặt nạ để kiểm tra, không chạy `main()` của chương trình tạo dữ liệu.

## 7 điểm cần chỉnh hoặc làm rõ

### 1. Nguồn [3] chưa chỉ đúng nơi cung cấp danh sách 880/120

Vị trí: mục 3.2, trang 3; tài liệu [3], trang 16.

Đoạn văn dẫn trang Kaggle để chứng minh nguồn hai tệp `train.txt`/`val.txt`. Có thể xác nhận trực tiếp nguồn chia tập từ kho MediaEval 2020 của tác giả: bản địa phương khớp toàn bộ ID và thứ tự với [train.txt](https://github.com/DebeshJha/2020-MediaEval-Medico-polyp-segmentation/blob/master/kvasir-seg-train-val/train.txt) và [val.txt](https://github.com/DebeshJha/2020-MediaEval-Medico-polyp-segmentation/blob/master/kvasir-seg-train-val/val.txt). Không xác nhận được nội dung danh sách từ trang Kaggle qua lần truy cập này vì trang không trả phần nội dung cần đọc.

Đề nghị thay/bổ sung [3] bằng kho tác giả và đường dẫn thư mục `kvasir-seg-train-val`, ghi rõ đây là cách chia được đề tài sử dụng. Không nên gọi chung là cách chia duy nhất của Kvasir-SEG. Lưu bản tải về và SHA-256 trong bộ bằng chứng để đối chiếu về sau. Dẫn nguồn nền rõ là **Kvasir v2**, phù hợp trường `background_source` trong YAML, để phân biệt phiên bản.

### 2. 1.063 đa giác chưa chứng minh có đúng 1.063 polyp riêng biệt

Vị trí: đoạn giải thích sau Bảng 3.1, trang 3; mục 3.3.3–3.3.5, trang 5–6; mục 3.6, trang 13.

Hàm chuyển đổi nhận một mặt nạ ngữ nghĩa và tạo một dòng cho mỗi đường bao ngoài giữ lại. Nó không đọc định danh từng tổn thương. Một polyp bị che khuất hoặc mặt nạ đứt đoạn có thể cho nhiều thành phần; hai vùng tiếp xúc có thể nhập lại. Vì vậy số dòng đúng không đủ để xác nhận số polyp thực.

Đề nghị giữ hàng bảng là “Số vùng/đa giác được gán nhãn”, đổi đoạn giải thích thành: “Một mặt nạ có thể có nhiều vùng tách rời. Sau xử lý, mỗi đường bao ngoài đạt điều kiện được ghi thành một dòng nhãn; tổng cộng có 936 dòng ở train và 127 dòng ở val. Số này là số đa giác do quy trình tạo ra, chưa xác nhận số polyp độc lập về mặt lâm sàng.” Việc coi các vùng dưới 20 là nhiễu cũng là quy tắc lọc, chưa có kiểm duyệt thủ công chứng minh mọi vùng bị bỏ đều là nhiễu.

### 3. Mô tả thứ tự tăng cường thiếu Albumentations ở chuỗi chính

Vị trí: cuối mục 3.5, trang 9; mục 3.5.4, trang 11; Bảng 3.2, trang 11–12.

Đoạn sau đã nhắc Albumentations và nhật ký thực sự xác nhận có bật. Tuy nhiên câu “các phép được thực hiện theo thứ tự…” chưa đầy đủ. Chuỗi đang có trong `v8_transforms` với các xác suất bằng 0 được lược đi là: **Mosaic → affine → Albumentations → HSV → lật ngang → Format**. Albumentations không phải bước tùy ý nằm sau lật.

Đề nghị bổ sung vị trí này trong câu mô tả, đồng thời thêm một dòng/chú thích cho bốn phép p=0,01 trong Bảng 3.2. Không suy ra việc bật nhánh này ở mọi lần chạy chỉ từ một nhật ký seed 0; điều đó còn phụ thuộc môi trường từng lần chạy.

### 4. Tắt Mosaic không đồng nghĩa dùng ảnh “nguyên vẹn”

Vị trí: mục 3.5.1, trang 10.

`close_mosaic()` đặt mosaic/copy_paste/mixup/cutmix về 0 rồi dựng lại transforms; affine, HSV, lật và nhánh Albumentations vẫn còn. Nhật ký seed 0 cũng ghi `Closing dataloader mosaic` ở dòng 522. Ảnh cuối kỳ có thể vẫn bị dịch chuyển, phóng/thu, cắt biên và đổi màu.

Đề nghị sửa thành: “Mosaic được tắt trong 10 epoch cuối; mô hình tiếp tục học trên từng ảnh riêng lẻ với các phép tăng cường còn lại.”

### 5. Trung vị diện tích cần ghi chính xác hơn và nêu cách đo

Vị trí: mục 3.1.1, trang 1.

Tỷ lệ diện tích đường bao/diện tích ảnh tính lại có min **0,15454%**, trung vị **10,27011%**, max **80,98701%**. Min ≈0,15% và max ≈81% khớp. Câu “một nửa số vùng polyp chiếm không quá 10%” hơi chặt so với số liệu. Đề nghị dùng “trung vị khoảng 10,27% diện tích ảnh”.

Các tỷ lệ này đo trên **1.063 đường bao được giữ lại**, không phải tỷ lệ tổng pixel polyp của từng ảnh. `cv2.contourArea` tính diện tích hình học; tài liệu OpenCV chỉ rõ kết quả có thể khác số pixel khác 0 khi tô vùng. Vì vậy nên ghi phương pháp tính cạnh số liệu hoặc trong chú thích. Xem [OpenCV contourArea](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html).

### 6. Kết luận khác biệt kết quả chỉ do kiến trúc vượt bằng chứng tiền xử lý

Vị trí: đoạn cuối mục 3.8, trang 15.

Đối chiếu 20 cấu hình xác nhận các giá trị tiền xử lý được kiểm tra giống nhau. Điều đó hỗ trợ thiết kế đối chiếu, nhưng chưa tự chứng minh mọi khác biệt kết quả chỉ do kiến trúc. Kết luận này còn cần kiểm soát huấn luyện, khởi tạo, phiên bản thư viện và đánh giá ở chương thực nghiệm.

Đề nghị giữ trong phạm vi chương: “Hai mô hình sử dụng cùng bộ dữ liệu và cùng cấu hình tiền xử lý đã lưu, tạo điều kiện thống nhất cho phép so sánh ở chương thực nghiệm.” Các câu về giảm báo động giả hoặc tránh ghi nhớ nên trình bày là mục đích/kỳ vọng; chương này chưa thực nghiệm riêng tác dụng của từng bước. Câu “qua 100 epoch gần như không gặp lại đúng một ảnh hai lần” cũng là diễn giải về sự đa dạng ngẫu nhiên, không phải một phép đo đã thực hiện.

### 7. Nguồn bảng và khả năng tái tạo cần truy vết cụ thể hơn

Vị trí: dòng nguồn Bảng 3.1, Bảng 3.2; mục 3.7; thư mục mã sinh hình.

“Đề tài thống kê” và “tệp cấu hình huấn luyện” đúng về bản chất nhưng chưa chỉ tệp nào. Mã converter `main()` vẫn có đường dẫn máy cũ `C:/LeDucLuong/...`; YAML trong bộ BG20 cũng mang đường dẫn cũ, khác vị trí workspace hiện tại. Kiểm tra lần này tái tạo được logic chuyển nhãn và lấy mẫu; không có nghĩa người đọc chạy nguyên lệnh cũ là dựng xong toàn bộ dữ liệu.

Đề nghị thêm phụ lục truy vết gồm: đường dẫn converter, hai manifest polyp, hai manifest ảnh nền, mẫu `args.yaml` của mỗi mô hình, phiên bản thư viện và lệnh chạy với đường dẫn được cập nhật. Có thể ghi nguồn bảng bằng tên bộ dữ liệu + đường dẫn tương đối; không cần nhồi đường dẫn dài vào phần văn bản chính. Mã kiểm tra kèm báo cáo này cung cấp một lệnh đối chiếu có thể chạy từ thư mục gốc.

## Nguồn gốc và tính tái tạo của hình

Đã chạy lại `figs.py` và `flow.py` vào thư mục tạm rồi so sánh với hình đã giao. **Cả 5 PNG khớp từng byte và pixel**; tệp `.drawio` và JSON thông số cũng khớp. Cả 5 PNG này đúng là các ảnh được nhúng trong bản Word có nguồn. Chi tiết: [doi_chieu_hinh.json](doi_chieu_hinh.json).

| Hình | Nguồn truy được | Nhận xét |
| --- | --- | --- |
| 3.1 | Ảnh/mặt nạ `cju0qkwl35piu0993l0dewei2`; nền `01af3454-037f-4708-b73c-6ec4423b6a61` | Ghép từ ảnh có trong nguồn cục bộ |
| 3.2 | Ảnh/mặt nạ `cju1ats0y372e08011yazcsxm`; xử lý bằng OpenCV trong `figs.py` | Kết quả 377 → 21 điểm khớp nhãn đang dùng |
| 3.3 | Ảnh val `cjyzul1qggwwj07216mhiv5sy`; resize/padding trong `figs.py` | Minh họa khung vuông; bản huấn luyện có thể kiểm định với khung chữ nhật theo lô như báo cáo đã giải thích |
| 3.4 | Bốn ID được lưu trong `hinh/thong_so_sinh_hinh.json`; biến đổi với tham số cố định | Hình minh họa tự dựng theo thông số, không phải ảnh chụp một lô ngẫu nhiên thực tế từ dataloader |
| 3.5 | Nút/cạnh khai báo trong `flow.py` | Sơ đồ tự dựng, đúng hướng luồng chính |

Gợi ý nhỏ: nhãn “Ảnh gốc 640×640” ở ô a Hình 3.4 nên đổi thành “Ảnh sau đổi kích thước/đệm 640×640”; ảnh gốc thực sự của ID này là 623×528. Hình 3.3 nhân tọa độ theo hệ số lý tưởng r; trong dataloader, tỷ lệ thực trên từng chiều sau làm tròn còn được dùng để cập nhật nhãn. Đây là khác biệt dưới một pixel ở ví dụ này, phù hợp xem hình là minh họa, không phải kiểm thử tương đương toàn bộ dataloader.

## Tài liệu tham khảo và phạm vi chương

Thông tin về 1.000 ảnh/mặt nạ, nguồn lớp polyp, Labelbox, chuyên gia kiểm tra nhãn và ScopeGuide phù hợp [bài gốc Kvasir-SEG](https://arxiv.org/html/1911.07069). Bản bài báo có preprint năm 2019, công bố kỷ yếu MMM năm 2020; ghi 2020 trong tài liệu [1] là phù hợp. Mặt nạ JPEG có nhiều mức xám được xác nhận trực tiếp ở dữ liệu địa phương, nên có thể dẫn nguồn dữ liệu kiểm tra thay vì chỉ dựa vào mô tả mặt nạ 1-bit trong bài.

Định dạng đa giác phù hợp [tài liệu Ultralytics về segmentation datasets](https://docs.ultralytics.com/datasets/segment). [Bài Otsu](https://ieeexplore.ieee.org/document/4310076) khớp năm 1979, tập 9, số 1, trang 62–66. Các công thức (3.1)–(3.13) đã đọc cả XML toán và bản dựng Word; không phát hiện lỗi công thức rõ ràng so với cách triển khai được mô tả. [Tài liệu tăng cường Ultralytics](https://docs.ultralytics.com/guides/yolo-data-augmentation) phù hợp giải thích tham số, còn giá trị của thực nghiệm phải lấy từ cấu hình đã lưu.

Các mục 3.1–3.8 đều phù hợp phạm vi xây dựng dữ liệu và tiền xử lý, bao gồm tăng cường trực tuyến và tạo tensor/mặt nạ khi nạp dữ liệu. Đề cập `mask_ratio`, `overlap_mask`, batch và epoch đóng Mosaic là cần thiết để mô tả hành vi. Kiến trúc TSVM chỉ cần một câu xác định ranh giới; không nên suy kết quả hiệu năng tại đây.

Chưa xác minh đầy đủ từng chi tiết xuất bản của toàn bộ 11 mục tham khảo, đặc biệt thông tin tập/số/trang của [5] và sách [7]. Vì vậy kết luận về nguồn là “các nguồn chính và các phát biểu trọng tâm đã đối chiếu”, không phải xác nhận tuyệt đối cả danh mục. Dấu thời gian/ngày truy cập đã ghi trong báo cáo không chứng minh được lịch sử truy cập; lần kiểm tra độc lập này diễn ra ngày 10/10/2026.

## Giới hạn và ghi chú trình bày

- Khớp SHA-256 với nguồn cục bộ chứng minh việc sao chép, không thay thế checksum của gói tải chính thức. Với ảnh polyp và nền, nguồn bộ dữ liệu được xác định qua tài liệu/mã; với danh sách 880/120, đã đối chiếu trực tiếp nội dung trên kho tác giả.
- Không có kiểm tra định danh bệnh nhân hoặc phát hiện ảnh gần giống trong lần này. Báo cáo đã nêu đúng giới hạn đó. Không có tập test độc lập trong bộ BG20 đang kiểm tra.
- Đo thêm để đánh giá thay đổi khi chuyển nhãn: mặt nạ tô lại từ tọa độ nhãn (nhân W/H, làm tròn về pixel gần nhất, `fillPoly` ở kích thước gốc) so với mặt nạ Otsu có IoU trung bình **0,993742**, thấp nhất **0,972838**. Đây là phép đo bảo toàn vùng của chuyển đổi, không phải IoU mô hình; kết quả còn phụ thuộc cách raster hóa. Không dùng nó để tuyên bố nhãn không mất thông tin.
- Bản Word dựng lại có đủ 5 hình, 2 bảng và 13 công thức. Quan sát toàn bộ trang qua ảnh tổng quan và các trang tiêu biểu chưa thấy hình/công thức bị mất. Một số ngắt trang chưa gọn: trang 6 dư khoảng trắng trước hình 3.2; Bảng 3.2 tách trang 11–12; trang 17 chỉ còn hai tài liệu tham khảo. Đây là vấn đề trình bày, không làm sai quy trình.
- Chưa sửa hai bản Word, dữ liệu, cấu hình hay mã huấn luyện. Các tệp mới nằm trong `output/tien_xu_ly/kiem_tra`; bản dựng và hình tái tạo nằm trong `tmp/docs/kiem_tra_tien_xu_ly`.

## Lệnh đối chiếu

Chạy tại thư mục gốc dự án, với Python có `opencv-python`, `numpy`, `python-docx`, `PyYAML`, `lxml` và có mạng để đối chiếu hai manifest:

```powershell
python -X utf8 output/tien_xu_ly/kiem_tra/kiem_tra_du_lieu.py
```

Môi trường kiểm tra lần này: Python 3.13.2, OpenCV 5.0.0, NumPy 2.3.4. Nhật ký Kaggle seed 0 ghi Ultralytics custom 8.4.127; không đồng nhất phiên bản trên máy kiểm tra với phiên bản môi trường huấn luyện.
