# Góp ý kiểm định chương 4 "Dữ liệu và tiền xử lý"

Nguồn được kiểm: `06_bao_cao/Tien_Xu_Ly_Du_Lieu.docx` (bản gốc ghi "CHƯƠNG 3", có 121 đoạn, 2 bảng, 5 hình, 13 công thức và 11 tài liệu tham khảo riêng của chương). Ngày kiểm: 26/10/2026. Người kiểm chỉ đọc dữ liệu, không sửa docx hay dữ liệu.

Ký hiệu trong bảng: P*n* là đoạn thứ *n* trong docx (đánh số theo các đoạn có nội dung, tính từ tiêu đề chương).

## 0. Cách kiểm và môi trường

- **Trích chương:** giải nén docx và đọc `word/document.xml`, giữ style `u1/u2/u3/Chuthich`. Năm ảnh trong `word/media/` đã được xem trực tiếp.
- **Đo lại dữ liệu:** một script tạm (đặt ở thư mục Temp, không ghi vào repo) chạy trên:
  - `01_du_lieu/tao_BG20/Kvasir-SEG/{images,masks}` (1.000 + 1.000 tệp);
  - `01_du_lieu/tao_BG20/normal-cecum/normal-cecum` (1.000 tệp);
  - `01_du_lieu/Kvasir_YOLO_SEG_BG20/`.

  Môi trường: Python 3.13, **OpenCV 5.0.0, NumPy 2.5.1**. Thuật toán chép nguyên hàm `convert_mask_to_yolo_polygons` của `01_du_lieu/scripts_tien_xu_ly/convert_kvasir_with_background_to_yolo_seg.py` (dòng 53–129).
- **Cấu hình:** đọc trực tiếp 40/40 `03_ket_qua_huan_luyen/*/*/args.yaml` bằng grep, và đối chiếu với `00_tai_lieu_tong_quan/bang/03_cau_hinh_args.csv`.
- **Mã nguồn:** fork `02_ma_nguon/ultralytics_TSVM_FP32/` (`__init__.py:3` ghi `__version__ = "8.4.127"`). Đã so thêm với gói pip `ultralytics 8.4.127` trong `C:\venv_kl_gpu`. Tệp `data/build.py`, `data/utils.py`, `models/yolo/detect/train.py`, `detect/val.py` và `segment/train.py` giống hệt nhau. Tệp `data/augment.py`, `data/base.py` và `data/dataset.py` chỉ khác ở phần cache RAM và một lệnh tắt khi phép warp là đồng nhất; với `cache=False`, các khác biệt này không đổi kết quả tiền xử lý.

## 1. Tóm tắt

| Kết luận | Số nhận định |
|---|---:|
| Đúng | 79 |
| Một phần (đúng ý chính nhưng thiếu điều kiện, lệch số nhỏ hoặc nguồn chưa đúng) | 9 |
| Sai | 1 |
| Không kiểm được | 5 |
| **Tổng** | **94** |

Đánh giá chung: chương viết **rất sát dữ liệu và mã nguồn**. Hầu hết con số đo lại được trùng tới chữ số cuối, kể cả các số khó như Otsu 5–8, 1.206/143/1.063 đường bao, 333,2 → 24,6 điểm, 377 → 21 điểm và dòng nhãn ví dụ.

Các vấn đề cần sửa trước khi đưa vào báo cáo:

1. **Sai (mục 3.4, P59):** khung kiểm định trong lúc huấn luyện có cạnh dài **672**, không phải 640. Lý do: chế độ `rect` dùng `pad=0.5`, `stride=32` và lô 16 ảnh.
2. **Nguồn gốc split 880/120 (mục 3.2, P17)** được ghi là "do nhóm tác giả Kvasir-SEG cung cấp [3]", nhưng repo không có bằng chứng. Tài liệu tổng quan `02_DU_LIEU_BG20.md` dặn rõ không nên ghi như vậy.
3. **Tái tạo 1.000/1.000 nhãn (mục 3.7, P101)** đúng với OpenCV 5.0.0, nhưng hồ sơ kiểm toán cũ ghi 999/1.000 trên OpenCV 4.12.0. Cần ghi kèm môi trường.
4. **Nhật ký Albumentations (P83)** là log của lượt TSVM **cũ** (fork FP16), không thuộc 40 lượt chính.
5. Ý "một nửa số vùng polyp ≤ 10%" hơi lệch: trung vị là 10,27%, và 48,3% số vùng ≤ 10%.
6. Trích dẫn [2] (MMSys'17) cho ý "mỗi lớp 1.000 ảnh" nhiều khả năng không đúng phiên bản Kvasir. Chưa kiểm được bản PDF.

## 2. Bảng kiểm từng nhận định

| # | Mục | Trích câu (ngắn) | Kết luận | Bằng chứng | Đề xuất sửa |
|---|---|---|---|---|---|
| 1 | Mở đầu (P3) | "Quá trình tiền xử lý được chia thành hai giai đoạn" | Đúng | Script chạy một lần (`convert_...py`). Phần còn lại chạy trong dataloader (`data/dataset.py:313-333`). | — |
| 2 | Mở đầu (P3) | "Các thao tác và thông số… đều được đối chiếu với mã nguồn" | Một phần | Phần lớn khớp, trừ khung kiểm định 672 (xem #54). | Giữ câu sau khi sửa #54. |
| 3 | 3.1.1 (P6) | "1.000 ảnh… Jha và cộng sự công bố năm 2020 [1]" | Đúng | Đếm được 1.000 ảnh và 1.000 mặt nạ. Bài [1] ghi "Each folder contains 1000 images". | — |
| 4 | 3.1.1 (P6) | "lấy từ lớp polyp của bộ dữ liệu Kvasir [2]" | Đúng | [1] §3.3 ghi tác giả tải toàn bộ lớp polyp của Kvasir lên Labelbox (và §3.1 nói đã thay 13 ảnh). | Có thể thêm "đã thay 13 ảnh". Nguồn đúng cho ý này là [1]. |
| 5 | 3.1.1 (P6) | "kỹ sư và bác sĩ… Labelbox… bác sĩ chuyên khoa tiêu hóa… kiểm tra lại" | Đúng | [1] §3.3: một kỹ sư và một bác sĩ khoanh vùng, sau đó một bác sĩ tiêu hóa giàu kinh nghiệm duyệt lại. | — |
| 6 | 3.1.1 (P6) | "mặt nạ cùng tên… polyp màu trắng" | Đúng | Kiểm 1.000/1.000 cặp ảnh–mặt nạ: cùng tên và cùng kích thước. [1] ghi tiền cảnh màu trắng. | — |
| 7 | 3.1.1 (P7) | "333 kích thước khác nhau" | Đúng | Đo được 333 kích thước trên 1.000 ảnh. | — |
| 8 | 3.1.1 (P7) | "rộng 332–1.920… cao 352–1.072" | Đúng | Rộng 332–1.920, cao 352–1.072. | — |
| 9 | 3.1.1 (P7) | "phổ biến nhất… xấp xỉ 622 × 530" | Đúng | 622×530 có 78 ảnh. Các kích thước kế tiếp là 626×547 (66), 626×546 (61), 622×529 (56). Trung vị là 621×530. | — |
| 10 | 3.1.1 (P7) | "nhỏ nhất… 0,15%… lớn nhất… 81%" | Đúng | Tính theo diện tích đường bao (`contourArea`) chia W·H trên 1.063 vùng: nhỏ nhất 0,1545%, lớn nhất 80,99%. | Nên nói rõ "tính trên 1.063 vùng sau chuyển đổi". |
| 11 | 3.1.1 (P7) | "một nửa số vùng polyp chiếm không quá 10%" | Một phần | Trung vị là 10,27%. Có 513/1.063 vùng (48,3%) ≤ 10%. | "khoảng một nửa số vùng (48%) chiếm không quá 10% diện tích ảnh; trung vị xấp xỉ 10,3%". |
| 12 | 3.1.1 (P7) | "chữ… hoặc ô hình nhỏ ScopeGuide [1]" | Đúng | [1] có câu nói một số ảnh chứa hình đầu dò định vị ống soi ScopeGuide (Olympus). Có thể thấy trong Hình 3.1c và Hình 3.3a. | — |
| 13 | 3.1.1 (P8) | "cả ảnh và mặt nạ đều… JPEG [1]" | Đúng | Thư mục `masks/` chỉ có tệp `.jpg`. [1] chỉ viết "image files are encoded using JPEG". | — |
| 14 | 3.1.1 (P8) | "mặt nạ không còn hoàn toàn chỉ gồm hai giá trị" | Đúng | Mỗi mặt nạ có 13–18 mức xám khác nhau. | Có thể thêm "13–18 mức xám". |
| 15 | 3.1.2 (P10) | "Kvasir gồm 8 lớp ảnh, mỗi lớp 1.000 ảnh [1], [2]" | Một phần | [1] §3.1 ghi 8.000 ảnh, 8 lớp, mỗi lớp 1.000 ảnh. Thư mục normal-cecum có đúng 1.000 ảnh. Bài [2] (MMSys'17) không có trong `TLTK/` nên chưa đối chiếu được. Theo hiểu biết của người kiểm, bài này mô tả bản đầu (4.000 ảnh, 500 ảnh/lớp). | Ghi rõ "Kvasir v2 (8.000 ảnh, 8 lớp × 1.000)" và trích [1]. Chỉ dùng [2] để dẫn nguồn gốc bộ dữ liệu. |
| 16 | 3.1.2 (P10) | "không chứa polyp và đều có kích thước 720 × 576" | Đúng | 1.000/1.000 ảnh normal-cecum có kích thước 720×576. Ý "không polyp" dựa trên nhãn lớp, không kiểm từng ảnh. | — |
| 17 | 3.1.2 (P10) | "Manh tràng là đoạn đầu của đại tràng… mốc giải phẫu" | Đúng | Kiến thức giải phẫu phổ thông, phù hợp với cách Kvasir xếp lớp này vào nhóm mốc giải phẫu ([1] §3.1). | Nên thêm trích dẫn. |
| 18 | 3.1.2 (P11) | "bổ sung ảnh không có polyp giúp mô hình học…, giảm báo động giả" | Không kiểm được | Đây là lập luận động cơ. Đề tài không có thí nghiệm đối chứng có/không ảnh nền. | Viết thận trọng: "nhằm giúp mô hình…". Không khẳng định hiệu quả. |
| 19 | 3.1.2 (P15) | "Ảnh c… góc dưới bên trái có ô hình ScopeGuide" | Đúng | Đã xem `media/image1.png`: góc dưới trái có ô màu xanh. | — |
| 20 | 3.2 (P17) | "880… 120… do nhóm tác giả Kvasir-SEG cung cấp trong… train.txt và val.txt [3]" | Không kiểm được | Repo không ghi nguồn gốc hai danh sách. `00_tai_lieu_tong_quan/02_DU_LIEU_BG20.md` (mục Giới hạn) dặn không nên ghi như vậy. Liên kết Kaggle [3] chưa được tải về đối chiếu. | Bỏ phần quy nguồn, hoặc tải lại tệp gốc từ [3] và so SHA-256 với `01_du_lieu/train.txt`, `val.txt` trước khi giữ. Câu gợi ý: "Ảnh polyp được chia theo hai danh sách cố định gồm 880 ảnh huấn luyện và 120 ảnh kiểm định (`train.txt`, `val.txt`)." |
| 21 | 3.2 (P17) | "có thể so sánh với các nghiên cứu khác dùng cùng cách chia" | Không kiểm được | Phụ thuộc vào #20. | Bỏ ý này nếu chưa chứng thực được nguồn. |
| 22 | 3.2 (P17) | "không có ảnh nào xuất hiện ở cả hai tập" | Đúng | `00_kiem_tra_du_lieu.json`: hai danh sách không giao nhau. Đo lại: 0 tên trùng, 0 SHA-256 trùng. | — |
| 23 | 3.2 (P18) | "sắp xếp 1.000 tên tệp… seed bằng 42… chọn ngẫu nhiên 200 ảnh… 160… 40" | Đúng | Script dòng 186–193 (`sorted(...)`, `random.seed(42)`, `random.sample(...,200)`, `[:160]`, `[160:]`). | — |
| 24 | 3.2 (P18) | "mỗi lần chạy lại… đúng 200 ảnh như nhau" | Đúng | Chạy lại trên Python 3.13 ra cùng danh sách và cùng thứ tự với `selected_normal_cecum_train_160.txt` và `selected_normal_cecum_val_40.txt`. | — |
| 25 | 3.2 (P18) | "lưu lại thành hai tệp văn bản" | Đúng | Script dòng 225–228. Hai tệp có trong `Kvasir_YOLO_SEG_BG20/`. | Có thể nêu tên hai tệp. |
| 26 | 3.2 (P19) | "BG20… 20% của 1.000… 16,67%… 15,38%… 25%" | Đúng | 200/1.000 = 20%; 200/1.200 = 16,67%; 160/1.040 = 15,38%; 40/160 = 25%. | — |
| 27 | 3.2 (Bảng 3.1) | 880/120/1.000; 160/40/200; 1.040/160/1.200; 936/127/1.063 | Đúng | `00_tai_lieu_tong_quan/bang/01_du_lieu_bg20.csv`. Đếm lại được 1.063 dòng nhãn. | Ghi "Nguồn: đếm trực tiếp trên bộ dữ liệu BG20". |
| 28 | 3.2 (P22) | "120 ảnh polyp… 127 vùng polyp" | Đúng | csv: val có 127 đối tượng. `dataset_bg20_summary.json` ghi `total_polyps_val: 127`. | Có thể thêm: 41 ảnh train và 7 ảnh val có từ 2 vùng trở lên. |
| 29 | 3.2 (P22) | "một ảnh có thể chứa nhiều polyp tách rời…, mỗi polyp… một nhãn riêng" | Đúng | Mỗi đường bao ngoài được ghi thành một dòng (script dòng 86–117). | Nên viết "mỗi vùng liên thông", vì đôi khi một polyp bị che nên tách làm hai vùng. |
| 30 | 3.2 (P23) | "images… labels… train và val… YAML… một lớp… polyp… chỉ số 0" | Đúng | Cấu trúc thư mục có thật. `data_bg20.yaml` ghi `names: {0: polyp}`. | Nói thêm: khi chạy trên Kaggle, notebook tạo YAML riêng (`/kaggle/working/data_bg20.yaml`, `nc: 1`) theo `args.yaml`. |
| 31 | 3.2 (P23) | "tiền tố bg_… nhãn rỗng… 0 byte" | Đúng | Script dòng 256–264. csv ghi `empty_labels` 160/40 và `empty_labels_not_bg` bằng 0. | — |
| 32 | 3.3 (P25) | "mỗi dòng… chỉ số lớp và dãy tọa độ… chuẩn hóa 0–1 [4]" | Đúng | Đúng định dạng YOLO-seg. Kiểm 1.063/1.063 dòng. | — |
| 33 | 3.3 (P25) | "năm bước… thư viện OpenCV" | Đúng | Gồm `threshold`, `morphologyEx`, `findContours`/`contourArea`, `approxPolyDP` và bước chuẩn hóa (dòng 74–114). | — |
| 34 | 3.3 (P25) | "ảnh nội soi được sao chép nguyên vẹn" | Đúng | `shutil.copy2` (dòng 244). 1.000/1.000 ảnh polyp trong BG20 trùng từng byte với ảnh gốc. | — |
| 35 | 3.3.1 (P27) | "mặt nạ được đọc và chuyển thành ảnh xám" | Đúng | Dòng 62–69: đọc màu bằng `imread`, sau đó `COLOR_BGR2GRAY`. | — |
| 36 | 3.3.1 (P27) | "mặt nạ dùng trong Hình 3.2 có 15 mức xám" | Đúng | Ảnh `cju1ats0y372e08011yazcsxm`: 15 giá trị khác nhau. | — |
| 37 | 3.3.1 (P27) | "pixel có giá trị lớn hơn t được gán thành 255" | Đúng | `THRESH_BINARY + THRESH_OTSU` (dòng 74). | — |
| 38 | 3.3.1 (P28–P30) | Công thức (3.1), (3.2) phương sai giữa lớp | Đúng | Đúng định nghĩa của Otsu [6]. | — |
| 39 | 3.3.1 (P31) | "ngưỡng Otsu chỉ nằm trong khoảng từ 5 đến 8" | Đúng | t = 7 (820 mặt nạ), 6 (98), 8 (78), 5 (4). | Có thể thêm "phần lớn là 7". |
| 40 | 3.3.2 (P33–P35) | "phép đóng… (3.3)… hình vuông 3 × 3… một lần" | Đúng | `MORPH_RECT (3,3)`, `MORPH_CLOSE`, `iterations=1` (dòng 77–78). | — |
| 41 | 3.3.3 (P37) | "Suzuki và Abe… đường bao ngoài cùng… chỉ giữ điểm đầu và cuối" | Đúng | `RETR_EXTERNAL`, `CHAIN_APPROX_SIMPLE` (dòng 81). `findContours` của OpenCV cài đặt thuật toán Suzuki–Abe [8]. | Nói thêm: lấy đường bao ngoài cũng bỏ qua các lỗ bên trong vùng. |
| 42 | 3.3.3 (P38) | "nhỏ hơn 20 pixel vuông đều bị loại bỏ" | Đúng | `area < min_area=20` (dòng 55, 87–89). Diện tích tính theo `contourArea` (công thức Green), không phải số pixel. | — |
| 43 | 3.3.3 (P38) | "1.206 đường bao… 143… bị loại… 1.063" | Đúng | Đo lại được 1.206 / 143 / 1.063. | — |
| 44 | 3.3.4 (P40) | "trung bình khoảng 333 điểm cho mỗi polyp" | Đúng | 333,155 điểm/vùng, tính sau `CHAIN_APPROX_SIMPLE`. | — |
| 45 | 3.3.4 (P40–P42) | Douglas–Peucker; ε = 0,002·L | Đúng | `approxPolyDP(cnt, 0.002*arcLength(cnt, True), True)` (dòng 99–100). | — |
| 46 | 3.3.4 (P42) | "lệch… không quá 2 pixel" (ví dụ L = 1.000) | Đúng | Tính chất của Douglas–Peucker: mọi điểm gốc cách đa giác rút gọn không quá ε. | — |
| 47 | 3.3.4 (P42) | "ít hơn 3 đỉnh… giữ lại đường bao ban đầu" | Đúng | Dòng 103–106. Nếu đường bao gốc cũng dưới 3 điểm thì bị bỏ. | — |
| 48 | 3.3.4 (P42) | "333,2 xuống còn 24,6… giảm 92,6%… 10 đến 80 đỉnh" | Đúng | 333,155 → 24,637 (giảm 92,6%). Số đỉnh nhỏ nhất 10, lớn nhất 80. | Nói thêm: trung vị là 22 (train) và 26 (val) (`01_du_lieu_bg20.csv`). |
| 49 | 3.3.5 (P44–P46) | "chia cho W và H… giới hạn 0–1… làm tròn 6 chữ số" | Đúng | `np.clip(pt/width)`, định dạng `:.6f` (dòng 111–114). Mặt nạ và ảnh cùng kích thước (1.000/1.000). | — |
| 50 | 3.3.5 (P46) | "0 0.321027 0.000000 0.292135 0.041667… 21 đỉnh" | Đúng | `labels/train/cju1ats0y372e08011yazcsxm.txt`: 1 dòng, 21 đỉnh, có đúng tiền tố này. | — |
| 51 | 3.3.5 (P51) | "377 điểm… một đốm nhiễu nhỏ hơn 20 pixel vuông… 21 đỉnh" | Đúng | Mặt nạ trên cho 2 đường bao: một đường 377 điểm (diện tích 50.943) và một đường 1 điểm (diện tích 0) bị loại. | Có thể ghi "một điểm nhiễu đơn lẻ". |
| 52 | 3.4 (P53–P56) | "thu phóng… giữ nguyên tỷ lệ… cạnh dài nhất bằng 640"; (3.6), (3.7) làm tròn lên | Đúng | `data/base.py:276-279`: `r = imgsz/max(h0,w0)` và `min(ceil(w0*r), imgsz)`, nội suy `INTER_LINEAR`. Áp dụng cho cả train lẫn val. | Nói thêm: ảnh nhỏ hơn 640 (rộng tối thiểu 332) được **phóng to**. Công thức (3.7) nên có thêm `min(·, 640)`. |
| 53 | 3.4 (P57–P58) | "LetterBox thêm… xám 114 vào hai phía của cạnh ngắn"; (3.8) | Một phần | `LetterBox(new_shape=(640,640), scaleup=False)` (`data/dataset.py:319`). Ảnh đã được thu về cạnh dài 640, nên LetterBox **không thu phóng thêm**, chỉ thêm viền. Ở chế độ rect thực tế, viền được thêm ở **cả hai chiều** (xem #54). | "Ở nhánh kiểm định, ảnh đã thu phóng được đặt vào giữa khung đích và phần thiếu được tô màu xám 114, chia đều cho hai phía." |
| 54 | 3.4 (P59) | "khung đích… có thể là hình chữ nhật với cạnh dài 640 pixel" | **Sai** | Validator trong lúc huấn luyện dùng `rect=True` (`models/yolo/detect/train.py:76`), `pad=0.5` (`data/build.py:249`: `pad = 0.0 if mode == "train" else 0.5`) và lô `batch*2 = 16` (`engine/trainer.py:298`). `data/base.py:408` cho `batch_shapes = ceil(shape*640/32 + 0.5)*32`. Tính trên 160 ảnh val, 10 lô có khung (cao × rộng) là 544×672 (3 lô), 576×672 (5), 608×672 (1) và 672×672 (1). Cạnh dài luôn là **672**. | "Khi đánh giá, các ảnh có tỷ lệ khung hình gần nhau được gom thành lô 16 ảnh. Khung đích của mỗi lô được làm tròn lên bội số của 32 và cộng thêm một nửa bước, nên có cạnh dài 672 pixel và cạnh ngắn từ 544 đến 672 pixel. Ảnh vẫn giữ cạnh dài 640 và được viền xám ở cả hai chiều." |
| 55 | 3.4 (P59) | "nhánh huấn luyện… khung 640 × 640… cùng với các phép tăng cường…, xám 114" | Đúng | `RandomPerspective(size=(imgsz,imgsz))` (`augment.py:2813-2821`), `borderValue=114` (dòng 1193–1196). Mosaic dùng nền 114 (dòng 603). | — |
| 56 | 3.4 (P60, P64) | "ảnh… tập kiểm định có kích thước lớn nhất…: 1.920 × 1.072… 1/3… 640 × 358… 141 pixel" | Đúng | `cjyzul1qggwwj07216mhiv5sy` thuộc val, là ảnh lớn nhất trong 1.000 ảnh. 640/1.920 = 1/3; ⌈1.072/3⌉ = 358; (640 − 358)/2 = 141. | Ghi chú dưới hình: đây là minh họa với khung vuông 640. Khi đánh giá thực tế, ảnh này nằm trong lô khung 544×672, viền trên/dưới 93 pixel, trái/phải 16 pixel. |
| 57 | 3.5 (P66) | "qua 100 epoch, mô hình gần như không gặp lại đúng một ảnh hai lần" | Không kiểm được | Nhận định định tính, hợp lý với Mosaic và affine ngẫu nhiên, nhưng không đo được. | "…hiếm khi gặp lại một biến thể giống hệt nhau". |
| 58 | 3.5 (P66) | "Tăng cường dữ liệu chỉ áp dụng cho tập huấn luyện" | Đúng | `data/dataset.py:313-319`: `augment=False` thì chỉ dùng LetterBox. | — |
| 59 | 3.5 (P67) | "thứ tự: Mosaic, dịch chuyển và thu phóng, HSV, cuối cùng là lật ngang" | Đúng | `augment.py:2812-2852`: Mosaic → CopyPaste(p=0) → RandomPerspective → MixUp(0) → CutMix(0) → **Albumentations** → HSV → flipud(0) → fliplr. | Nên chèn "các phép Albumentations xác suất nhỏ" giữa thu phóng và HSV cho đủ. |
| 60 | 3.5 (Bảng 3.2) | 10 dòng tham số | Đúng | Cả 40/40 `args.yaml` có: mosaic 1.0, close_mosaic 10, translate 0.1, scale 0.5, hsv 0.015/0.7/0.4, fliplr 0.5, flipud/degrees/shear/perspective 0, mixup/cutmix/copy_paste 0. | Nguồn ghi rõ: "`args.yaml` của 40 lượt huấn luyện". |
| 61 | 3.5.1 (P69) | "Mosaic… được giới thiệu trong YOLOv4 [10]" | Đúng | [10] trình bày Mosaic là phép tăng cường mới. | — |
| 62 | 3.5.1 (P69) | "khung trống 1.280 × 1.280… màu xám… chọn ngẫu nhiên một điểm làm tâm ghép" | Đúng | `np.full((imgsz*2, imgsz*2, c), 114)` (dòng 603). Tâm `uniform(320, 960)` (dòng 507). | — |
| 63 | 3.5.1 (P69) | "khung ghép được dịch chuyển, thu phóng và cắt về 640 × 640" | Đúng | Ảnh ghép đi tiếp qua `RandomPerspective(size=(640,640))`. | — |
| 64 | 3.5.1 (P69) | "Ảnh nền cũng có thể được ghép chung với ảnh polyp" | Đúng | Ba ảnh phụ được lấy ngẫu nhiên từ buffer (dòng 491–494), không phân biệt ảnh nền. | Lưu ý: ba ảnh phụ lấy từ **bộ đệm các ảnh vừa nạp**, không phải đều trên toàn tập. |
| 65 | 3.5.1 (P70) | "xác suất 1,0… tắt trong 10 epoch cuối" | Đúng | `engine/trainer.py:459-460`: `epoch == epochs - close_mosaic` (đánh số từ 0), tức tắt từ epoch thứ 91. | — |
| 66 | 3.5.1 (P70) | "mô hình được tinh chỉnh trên ảnh nguyên vẹn" | Một phần | `close_mosaic()` chỉ đặt mosaic, mixup, cutmix và copy_paste về 0 (`data/dataset.py:364-374`). Affine, HSV, lật và Albumentations **vẫn chạy**. | "…mô hình được huấn luyện trên từng ảnh đơn lẻ không ghép, vẫn kèm dịch chuyển, thu phóng, đổi màu và lật". |
| 67 | 3.5.2 (P72–P74) | (3.9) `x' = s·(x−cx)+tx`; s ∈ [0,5; 1,5]; tx lệch tâm tối đa 10% | Đúng | `augment.py:1103-1131`: C dời tâm ảnh về gốc, R chỉ có tỉ lệ s ~ U(0,5; 1,5) vì góc = 0, T ~ U(0,4; 0,6)·640, tức 320 ± 64 pixel. | — |
| 68 | 3.5.2 (P74) | "phần ngoài khung bị cắt…, xám 114, đa giác… biến đổi theo cùng công thức" | Đúng | `warpAffine(..., borderValue=114)`. `apply_segments` nhân với M rồi clip. | Nói thêm: sau biến đổi, các đối tượng còn lại quá nhỏ bị loại (`box_candidates`: cạnh ≤ 2 px hoặc diện tích < 1% so với trước), `augment.py:1230-1231` và `:1410`. |
| 69 | 3.5.2 (P74) | "xoay, cắt xiên… phối cảnh… bằng 0" | Đúng | Cả 40/40 `args.yaml` có degrees = shear = perspective = 0. | — |
| 70 | 3.5.3 (P76) | "gh, gs, gv… chọn đều trong… ±0,015, ±0,7, ±0,4" | Đúng | `np.random.uniform(-1,1,3)*[hgain,sgain,vgain]` (`augment.py:1476`). | — |
| 71 | 3.5.3 (P77–P78) | (3.10) `H' = (H + 180·gh) mod 180`; (3.11) S', V' = min(255, ·) | Đúng | `lut_hue = (x + r[0]*180) % 180`; `lut_sat = clip(x*(1+r[1]), 0, 255)`; `lut_val` tương tự. | Chi tiết phụ: mã giữ `S = 0` không đổi (`lut_sat[0]=0`). |
| 72 | 3.5.3 (P79) | "sắc độ… 0 đến 179… tối đa khoảng 2,7 đơn vị" | Đúng | 0,015 × 180 = 2,7. | — |
| 73 | 3.5.3 (P79) | "vị trí polyp và nhãn không thay đổi" | Đúng | `RandomHSV` chỉ đổi `img`. | — |
| 74 | 3.5.4 (P81–P82) | "xác suất 0,5… (3.12) x' = 1 − x" | Đúng | `RandomFlip(direction="horizontal", p=0.5)`. Tại bước này tọa độ đang ở đơn vị pixel nên mã tính x' = W − x, tương đương 1 − x khi đã chuẩn hóa. | — |
| 75 | 3.5.4 (P83) | "lật dọc không… MixUp, CutMix, Copy-Paste… bằng 0" | Đúng | Cả 40/40 `args.yaml`. | — |
| 76 | 3.5.4 (P83) | "Albumentations… làm mờ, lọc trung vị, xám, CLAHE, mỗi phép 1%; chỉ hoạt động khi… có cài" | Đúng | `augment.py:2091` (import trong try), dòng 2109–2112: Blur, MedianBlur, ToGray, CLAHE với p = 0.01. | — |
| 77 | 3.5.4 (P83) | "nhật ký… TSVM với seed 0 trên Kaggle ghi nhận nhánh này đã được kích hoạt" | Một phần | Log có thật: `99_luu_tru/log_kaggle_cu/seed0_log.txt:62` và `:523`. Nhưng đây là lượt TSVM **cũ** (fork FP16, tên run không có `_FP32`). Không có log cho 40 lượt chính, kể cả Baseline (chạy bằng ultralytics cài từ pip). | "…nhật ký một lượt huấn luyện thử nghiệm trên Kaggle (cùng môi trường) cho thấy nhánh này được kích hoạt; repo không lưu nhật ký của 40 lượt chính." |
| 78 | 3.5 (P90) | Mô tả Hình 3.4 (a–f) | Đúng | Đã xem `media/image4.png`: a–f khớp chú thích. Đường bao xanh đi theo polyp ở b, d, f. Ô e có một ảnh nền. | Ảnh a có viền xám trên/dưới, nên ghi "ảnh sau khi đặt vào khung 640 × 640". Ảnh e minh họa không có vùng xám như Mosaic thật. |
| 79 | 3.5 (P90) | "Ảnh c có màu cam đậm hơn do độ bão hòa tăng và độ sáng giảm" | Không kiểm được | Hệ số dùng để vẽ hình không được lưu. | Ghi hệ số đã dùng (ví dụ gs = +0,5; gv = −0,2) vào chú thích. |
| 80 | 3.6 (P93) | "OpenCV đọc… BGR… đảo lại thành… RGB" | Đúng | `Format._format_img`: đảo kênh khi `random > bgr`, với `bgr = 0` nên luôn đảo. | — |
| 81 | 3.6 (P94) | "sắp xếp lại… số kênh, chiều cao, chiều rộng…; mỗi lô gồm 8 ảnh" | Đúng | `img.transpose(2,0,1)`; batch 8 (args). | Thêm: lô kiểm định có 16 ảnh. |
| 82 | 3.6 (P95–P97) | "chuyển sang số thực và chia cho 255…; không trừ… ImageNet" | Đúng | `models/yolo/detect/train.py:119` và `detect/val.py:76`: `.float() / 255`. Không có bước chuẩn hóa nào khác. | Nói rõ: phép chia thực hiện trên GPU trong `preprocess_batch`, sau khi đã ghép lô. |
| 83 | 3.6 (P98) | "mask_ratio bằng 4…; 640 × 640… 160 × 160" | Đúng | `data/utils.py:441-447`: `fillPoly` ở độ phân giải đầy đủ rồi `resize` về (h/4, w/4). | "nhỏ hơn 4 lần **mỗi chiều**". |
| 84 | 3.6 (P98) | "overlap_mask… gộp vào một mặt nạ…, mỗi polyp… số thứ tự riêng" | Đúng | `polygons2masks_overlap` (`data/utils.py:468-493`): sắp theo diện tích giảm dần, gán chỉ số i+1, vùng nhỏ nằm đè lên vùng lớn. | — |
| 85 | 3.6 (P98) | "Với ảnh nền, mặt nạ chỉ gồm toàn giá trị 0" | Đúng | Nhánh `nl == 0` trong `Format.apply_instances` trả về `torch.zeros`. | — |
| 86 | 3.7 (P100) | "chương trình chuyển đổi tự kiểm tra… 1.040… 160… 160 và 40… dừng lại và báo lỗi" | Đúng | Script dòng 268–288 (`assert`). `dataset_bg20_summary.json` ghi 160/40. | Lưu ý: kiểm tra dùng `assert` nên bị tắt khi chạy `python -O`. |
| 87 | 3.7 (P101) | "mỗi ảnh có đúng một tệp nhãn… không có tệp nhãn nào thiếu ảnh" | Đúng | `image_label_stem_match = True` cho cả hai tập (csv). | — |
| 88 | 3.7 (P101) | "1.063 dòng… lớp 0, ít nhất ba đỉnh… tọa độ trong 0–1" | Đúng | Đo lại: 1.063 dòng, chỉ có lớp `0`, 0 dòng lỗi, ít nhất 10 đỉnh. | — |
| 89 | 3.7 (P101) | "Không có ảnh nào trùng tên hoặc trùng… SHA-256" | Đúng | Đo lại: 0 tên trùng, 0 SHA-256 trùng giữa train và val, 0 trùng bên trong từng tập. `00_kiem_tra_du_lieu.json` ghi `trung_byte_train_val: 0`. | — |
| 90 | 3.7 (P101) | "cả 1.000 tệp nhãn thu được đều trùng khớp từng ký tự" | Một phần | Đo lại trên **OpenCV 5.0.0 / NumPy 2.5.1**: 1.000/1.000 trùng. Nhưng `99_luu_tru/tai_lieu_cu/archive_doc/28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md:43` ghi **999/1.000** trên OpenCV 4.12.0 / NumPy 2.2.6 (tệp `ck2bxiswtxuw80838qkisqjwz.txt` lệch một đỉnh khoảng 3 px). Môi trường tạo bộ dữ liệu gốc không được ghi lại. | "Chạy lại chương trình trên OpenCV 5.0.0 và NumPy 2.5.1 cho 1.000/1.000 tệp nhãn trùng từng ký tự. Kết quả phụ thuộc phiên bản OpenCV: trên OpenCV 4.12.0 có 1 tệp lệch một đỉnh." |
| 91 | 3.7 (P101) | "seed bằng 42 cũng cho ra đúng danh sách 200 ảnh" | Đúng | Giống #24. | — |
| 92 | 3.7 (P101) | "bộ dữ liệu có thể được tái tạo đầy đủ từ dữ liệu gốc" | Một phần | Đúng khi có sẵn `train.txt`/`val.txt` (chưa rõ nguồn gốc) và đúng phiên bản OpenCV (#90). | "…có thể được tái tạo từ dữ liệu gốc và hai danh sách chia tập, với điều kiện dùng phiên bản OpenCV tương ứng." |
| 93 | 3.7 (P102) | Giới hạn: không có định danh bệnh nhân, mã băm không bắt ảnh gần trùng, không có tập test | Đúng | Khớp `02_DU_LIEU_BG20.md` (mục Giới hạn). | Nên thêm: tập kiểm định vừa dùng để **chọn epoch** vừa dùng để **báo cáo**. |
| 94 | 3.8 (P108–P109) | Hình 3.5; "Quy trình tiền xử lý… hai mô hình… hoàn toàn giống nhau" | Một phần | Hình đúng với quy trình (`media/image5.png`). 40 `args.yaml` chỉ khác `model`/`pretrained` (`03_cau_hinh_args.csv`). Mã dữ liệu của fork và pip 8.4.127 tương đương về chức năng. Hai chỗ chưa ổn: khối cuối hình ghi "YOLO26-seg + TSVM", trong khi quy trình dùng chung cho cả hai mô hình; và câu "khác biệt… phản ánh tác động của kiến trúc" bỏ qua dao động ngẫu nhiên giữa các seed. | Sửa khối cuối thành "YOLO26s-seg (đối chứng) / YOLO26s-seg + TSVM". Câu kết gợi ý: "…nhờ đó dữ liệu và tiền xử lý không phải là nguồn tạo ra khác biệt giữa hai mô hình; dao động ngẫu nhiên được kiểm soát bằng 20 seed ghép cặp (Chương 6)." |

## 3. Những điểm thiếu nên bổ sung (không phải lỗi sai)

1. **Nói rõ vai trò kép của tập kiểm định.** Chương đã ghi không có tập test (P102). Cần nói thêm rằng 160 ảnh validation vừa dùng để chọn epoch tốt nhất vừa dùng để báo cáo kết quả, nên kết quả có thể hơi lạc quan.
2. **Nguồn gốc split 880/120 chưa được chứng thực** (#20). Nếu muốn giữ trích dẫn [3], cần tải `train.txt`/`val.txt` từ nguồn [3] và so SHA-256 với `01_du_lieu/train.txt` và `01_du_lieu/val.txt`.
3. **Môi trường tái tạo nhãn** (#90). Có hai kết quả: 1.000/1.000 trên OpenCV 5.0.0 và 999/1.000 trên OpenCV 4.12.0. Phiên bản OpenCV dùng khi tạo bộ dữ liệu gốc không được ghi lại.
4. **Khung kiểm định thực tế** (#53–#54): rect, lô 16, `pad=0.5`, cạnh dài 672. LetterBox ở nhánh val không phóng to (`scaleup=False`).
5. **Lấy mẫu lại đa giác:** khi nạp nhãn, Ultralytics nội suy mỗi đa giác thành 1.000 điểm trước khi tăng cường (`data/dataset.py:396`, `update_labels_info`). Vì vậy việc rút gọn còn khoảng 25 đỉnh chỉ làm gọn tệp nhãn, không làm giảm độ mịn của mặt nạ huấn luyện ở cùng mức. Nên viết lại ý "dung lượng nhãn giảm" (P51) cho chính xác.
6. **Lọc đối tượng sau affine/Mosaic** (`box_candidates`): polyp bị cắt còn quá nhỏ sẽ bị loại khỏi nhãn của ảnh đó.
7. **Mosaic chọn ảnh phụ từ bộ đệm** các ảnh vừa nạp, không chọn đều trên toàn tập (#64).
8. **Ảnh nhỏ được phóng to** lên cạnh dài 640, nội suy song tuyến tính (`INTER_LINEAR`). Kvasir-SEG có ảnh rộng chỉ 332 px.
9. **YAML khi huấn luyện:** `data_bg20.yaml` trong repo trỏ tới đường dẫn tuyệt đối cũ (`.../Test_Mau/archive/Kvasir_YOLO_SEG_BG20`). Các lượt Kaggle dùng `/kaggle/working/data_bg20.yaml` do notebook tạo.
10. **Hai mô hình chạy hai bản mã khác nhau:** Baseline dùng `ultralytics==8.4.127` từ pip, TSVM dùng fork. Mã dữ liệu tương đương về chức năng với cấu hình này (`cache=False`). Việc Albumentations có được cài trong môi trường Baseline hay không chưa có log xác nhận.
11. **Thống kê bổ sung đã có sẵn:** 48 ảnh có từ 2 vùng polyp trở lên (41 train, 7 val); trung vị số đỉnh 22 (train) và 26 (val); 305 và 58 kích thước ảnh khác nhau ở train và val (`01_du_lieu_bg20.csv`).
12. **`multi_scale=0`, `rect=False` (train), `cache=False`, `fraction=1.0`:** nên nêu một câu để người đọc biết không có các phép biến đổi kích thước khác.
13. **Tài liệu tham khảo của chương** đánh số riêng [1]–[11]. Khi ghép vào báo cáo cần đổi sang số thứ tự chung theo IEEE. Riêng [2] (#15) cần xác minh lại phiên bản Kvasir.
14. **Mô hình được gọi là "YOLO26-seg"** trong cả chương, còn báo cáo dùng "YOLO26s-seg" (scale s). Nên thống nhất.

## 4. Danh sách số cần đổi 3.x → 4.x (cho chủ biên)

**Tiêu đề:** "CHƯƠNG 3. XÂY DỰNG BỘ DỮ LIỆU VÀ TIỀN XỬ LÝ DỮ LIỆU" → "CHƯƠNG 4…". Đề mục cuối "TÀI LIỆU THAM KHẢO CỦA CHƯƠNG 3" sẽ bỏ khi gộp danh mục chung.

**Đề mục (21):**
- Mục chính: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8.
- Mục con: 3.1.1, 3.1.2, 3.3.1, 3.3.2, 3.3.3, 3.3.4, 3.3.5, 3.5.1, 3.5.2, 3.5.3, 3.5.4.

**Hình (5):** Hình 3.1, 3.2, 3.3, 3.4, 3.5.

**Bảng (2):** Bảng 3.1, 3.2.

**Công thức (13):** (3.1) đến (3.13).

**Tham chiếu chéo trong lời văn** (cần đổi theo):

| Đoạn | Tham chiếu |
|---|---|
| P8 | "mục 3.3" |
| P11 | "Hình 3.1" |
| P15 | "Hình 3.1" |
| P19 | "Bảng 3.1" |
| P27 | "mục 3.1.1", "Hình 3.2" |
| P38 | "Bảng 3.1" |
| P46 | "Hình 3.2" |
| P47 | "Hình 3.2" |
| P59 | "mục 3.5" |
| P60 | "Hình 3.3" |
| P67 | "Bảng 3.2" |
| P86 | "Bảng 3.2", "Hình 3.4" |
| P89 | "Bảng 3.2" |
| P104 | "Hình 3.5" |

Lưu ý thêm: P102 và P109 có cụm "các chương sau". Nếu chương thực nghiệm là Chương 6 thì giữ được. Các công thức hiện nằm trong đối tượng OMML cùng dòng với số "(3.x)", nên phải sửa trong Word.

## 5. Dữ liệu dùng được cho chương 4 (đã xác minh)

| Số liệu | Giá trị | Nguồn |
|---|---|---|
| Ảnh polyp train / val / tổng | 880 / 120 / 1.000 | `bang/01_du_lieu_bg20.csv`; `train.txt`, `val.txt` |
| Ảnh nền train / val / tổng | 160 / 40 / 200 | csv; `selected_normal_cecum_*.txt` |
| Tổng ảnh train / val / toàn bộ | 1.040 / 160 / 1.200 | csv; `dataset_bg20_summary.json` |
| Số vùng polyp train / val / tổng | 936 / 127 / 1.063 | csv; đo lại 1.063 dòng nhãn |
| Ảnh có ≥ 2 vùng polyp | 41 / 7 | csv |
| Tỷ lệ ảnh nền: toàn bộ / train / val | 16,67% / 15,38% / 25% | tính từ các số trên |
| Kvasir-SEG: số kích thước, rộng, cao | 333; 332–1.920; 352–1.072 | đo lại trên `tao_BG20/Kvasir-SEG/images` |
| Kích thước phổ biến nhất | 622×530 (78 ảnh) | đo lại |
| normal-cecum | 1.000 ảnh, cả 1.000 ảnh 720×576 | đo lại |
| Diện tích vùng / ảnh | nhỏ nhất 0,1545%, lớn nhất 80,99%, trung vị 10,27%, 48,3% số vùng ≤ 10% | đo lại (theo `contourArea`, 1.063 vùng) |
| Số mức xám mỗi mặt nạ | 13–18 (mặt nạ ở Hình 3.2: 15) | đo lại |
| Ngưỡng Otsu | 5–8 (7: 820; 6: 98; 8: 78; 5: 4) | đo lại |
| Đường bao: tổng / bị loại / giữ | 1.206 / 143 / 1.063 | đo lại; khớp tài liệu kiểm toán cũ |
| Số điểm trung bình trước / sau rút gọn | 333,16 / 24,64 (giảm 92,6%); số đỉnh 10–80 | đo lại |
| Trung vị số đỉnh train / val | 22 / 26 | csv |
| Ví dụ Hình 3.2 | `cju1ats0y372e08011yazcsxm` (train): 377 → 21 điểm | đo lại |
| Ví dụ Hình 3.3 | `cjyzul1qggwwj07216mhiv5sy` (val), 1.920×1.072 → 640×358 | đo lại; `data/base.py:276-279` |
| Tái tạo nhãn | 1.000/1.000 (OpenCV 5.0.0, NumPy 2.5.1); 999/1.000 (OpenCV 4.12.0, NumPy 2.2.6) | đo lại; `archive_doc/28_...md:43` |
| Tái tạo danh sách ảnh nền (seed 42) | khớp 200/200, đúng thứ tự | đo lại |
| Trùng giữa train và val | 0 tên, 0 SHA-256 | đo lại; `00_kiem_tra_du_lieu.json` |
| Ảnh polyp trong BG20 so với ảnh gốc | 1.000/1.000 trùng từng byte | đo lại |
| Tăng cường (40/40 lượt) | mosaic 1,0; close_mosaic 10; translate 0,1; scale 0,5; HSV 0,015/0,7/0,4; fliplr 0,5; còn lại bằng 0 | `03_ket_qua_huan_luyen/*/*/args.yaml` |
| Mặt nạ huấn luyện | `mask_ratio=4` (640 → 160), `overlap_mask=True` | args; `data/utils.py:441-493` |
| Kích thước lô | train 8; val 16 | args; `engine/trainer.py:298` |
| Khung kiểm định (rect) | 544–672 × 672, cạnh dài luôn 672 | `data/base.py:386-408`, `data/build.py:249` (pad 0,5) |
| Chuẩn hóa đầu vào | chia 255, đảo BGR→RGB, CHW, không dùng mean/std | `detect/train.py:119`, `detect/val.py:76`, `augment.py` (`Format`) |
