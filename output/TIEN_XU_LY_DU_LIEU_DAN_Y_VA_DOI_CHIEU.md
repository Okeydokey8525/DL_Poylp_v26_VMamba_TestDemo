# Dàn ý và bản đồ đối chiếu tiền xử lý dữ liệu YOLO26-SEG + TSVM

Ngày rà soát workspace: **07/10/2026**. Phạm vi: **Kvasir_YOLO_SEG_BG20, YOLO26s-seg và Topology-Shape-aware VMamba (TSVM)**.

Tài liệu này là hướng dẫn viết và tra cứu bằng chứng, chưa phải bản thảo hoàn chỉnh của chương khóa luận. Các dấu `[ ]` là công việc viết còn cần thực hiện. Mã `PX`, `DL`, `S` giúp nối mục viết với bước xử lý, dữ liệu và source tương ứng; mã `H01`–`H05` đánh dấu vị trí cần chèn hình. Việc đánh dấu được thực hiện trong tài liệu; source và dataset không được chỉnh sửa.

## 1. Cách sử dụng và mức độ xác minh

1. Chọn giai đoạn viết ở phần 1.1, rồi viết các mục tương ứng ở phần 2.
2. Tra mã bước `PX` trong phần 3, sau đó mở file `S` ở phần 4 theo tên hàm và số dòng.
3. Dùng artifact `DL` trong phần 5 và bảng tham số ở phần 6 để đối chiếu số liệu.
4. Kiểm tra phần 7 trước khi khẳng định một bước đã được thực hiện hoặc một kết quả đã được kiểm chứng.
5. Tìm cụm `CHÈN HÌNH` để đến đúng chỗ paste ảnh trong bản thảo; xem bảng vị trí hình ở cuối phần 2 và nguồn tham khảo Việt Nam ở phần 9.1.

Số dòng là vị trí tại thời điểm rà soát, có thể thay đổi nếu source được sửa; tên hàm là mốc tìm kiếm bổ sung.

| Nhãn | Ý nghĩa |
|---|---|
| **CODE** | Đã đọc trực tiếp logic trong source hiện có. |
| **CONFIG** | Giá trị có trong cấu hình thí nghiệm lưu lại. |
| **ARTIFACT** | Có file dữ liệu hoặc metadata tương ứng trong workspace. |
| **CHECKED** | Đã kiểm tra trực tiếp bằng thao tác đọc file trong lần rà soát này. |
| **TO VERIFY** | Cần thêm nguồn dữ liệu, log hoặc kiểm tra trước khi khẳng định. |

**CODE/CONFIG không tự chứng minh mọi phép biến đổi đã chạy trong một lần train trên Kaggle.** Kết quả kiểm tra mới được lưu tại [kiem_tra_du_lieu_bg20.json](kiem_tra_du_lieu_bg20.json). Đây là kiểm tra bộ dữ liệu hiện có, không phải chạy lại converter hay huấn luyện.

### 1.1. Chia việc viết thành 3 giai đoạn

Ba giai đoạn dưới đây là **kế hoạch biên soạn phần khóa luận**, không phải ba bước chạy của model. Viết theo thứ tự để các mục sau dùng được số liệu và thuật ngữ đã thống nhất ở các mục trước.

| Giai đoạn | Phạm vi viết | Công việc và thứ tự thực hiện | Hình/bảng cần đặt | Đầu ra trước khi chuyển giai đoạn |
|---|---|---|---|---|
| **Giai đoạn 1 — Viết phần dữ liệu** | **3.1–3.2**, khoảng 2 trang | Giới thiệu nguồn và loại dữ liệu → đặc điểm ảnh/nhãn → lý do thêm ảnh nền → cách chọn mẫu và chia tập → cấu trúc thư mục YOLO. Đối chiếu DL01–DL06 và bảng 5.1. | **H01** ở cuối 3.1.3; bảng số lượng ở 3.2.2; cây thư mục dạng văn bản ở 3.2.3. | Có bản nháp 3.1–3.2, trích dẫn nguồn dữ liệu và số lượng nhất quán. Ghi rõ phần nào còn chờ xác minh nguồn; không điền thông tin phỏng đoán. |
| **Giai đoạn 2 — Viết các thao tác tiền xử lý** | **3.3–3.5**, khoảng 4,5 trang | Viết chuyển mask sang polygon → chuẩn bị ảnh/mask khi nạp vào model → tăng cường dữ liệu. Với mỗi bước: mục đích → thao tác/tham số → đầu ra → giải thích hình. Tra PX03, PX05–PX08 và S01–S09, S11. | **H02** sau 3.3.4; **H03** sau đoạn LetterBox ở 3.4.1; **H04** sau 3.5.3. Đặt bảng tham số ở cuối 3.5.4. | Có bản nháp mô tả đúng code/config, công thức và các vị trí hình. H02 còn chờ mask nguồn thì giữ dấu chờ; không thay bằng mask tái dựng rồi gọi là mask gốc. |
| **Giai đoạn 3 — Viết kiểm tra và hoàn thiện chương** | **3.6–3.7**, khoảng 1,5 trang, sau đó rà soát toàn chương | Viết kết quả kiểm tra/giới hạn từ DL07 → tổng hợp luồng xử lý → chèn sơ đồ chung → kiểm tra thuật ngữ, nguồn, thông số, chú thích hình và liên kết giữa các mục. | Bảng kiểm tra ở 3.6; **H05** sau đoạn giới thiệu quy trình ở 3.7. | Bản thảo 3.1–3.7 hoàn chỉnh để nhóm rà soát; mọi vị trí hình đã được chèn hoặc ghi rõ dữ liệu còn thiếu. Dùng checklist phần 10 trước khi bàn giao. |

**Cách viết quanh mỗi hình:** trước hình có một câu dẫn và gọi số hình; sau hình có 2–3 câu giải thích điều người đọc cần quan sát và liên hệ với bước xử lý. Các dấu `CHÈN HÌNH` chỉ phục vụ soạn thảo, cần xóa khi hoàn thiện. Nếu đang viết chữ trước, giữ dấu tại đúng vị trí rồi bổ sung hình khi có dữ liệu phù hợp.

## 2. Dàn ý đề xuất và dung lượng

Tên phần đề xuất: **Xây dựng bộ dữ liệu và tiền xử lý cho mô hình phân đoạn polyp**. Số chương `3` chỉ là ví dụ, cần đổi theo mục lục chung của nhóm.

Mục tiêu biên soạn: **khoảng 8 trang**, gồm hình, bảng, công thức. Nếu thành viên khác đã viết nguồn dữ liệu và phân chia dữ liệu, phần 3.3–3.7 có thể chiếm khoảng 5–6 trang. Đây là đề xuất biên soạn, không phải giới hạn bắt buộc của trường.

### 3.1. Nguồn dữ liệu và đặc điểm bộ dữ liệu — khoảng 1 trang

- [ ] **3.1.1. Bộ dữ liệu Kvasir-SEG:** giới thiệu nguồn, số ảnh polyp, kiểu ảnh, kiểu mask, nhiệm vụ phân đoạn; bổ sung trích dẫn bài công bố/trang dữ liệu gốc đã xác minh.
- [ ] **3.1.2. Dữ liệu ảnh nền normal-cecum:** trình bày nguồn ảnh nền được ghi trong script/metadata và mục đích bổ sung mẫu không có polyp.
- [ ] **3.1.3. Đặc điểm ảnh và mặt nạ:** mô tả ảnh polyp, ảnh nền và kiểu nhãn; minh họa cặp ảnh–mask khi có mask nguồn, dựa trên đặc điểm thực sự quan sát được.

**Bằng chứng:** DL01, DL02, S01. **Còn thiếu:** ảnh và mask nguồn tại các đường dẫn converter yêu cầu; không dùng mask tái dựng từ polygon để thay cho “mask gốc” mà không ghi rõ.

> **[CHÈN HÌNH H01 TẠI ĐÂY — cuối mục 3.1.3, sau đoạn mô tả ảnh polyp và ảnh nền]**
>
> **Nội dung:** một hình ghép hai ô: (a) ảnh nội soi có polyp, (b) ảnh nền normal-cecum được chọn trong BG20. Có thể dùng hai ảnh train đã liên kết ở phần 5.2. Nếu đã tìm lại mask nguồn, có thể thêm ô (c) mask gốc tương ứng với ảnh (a), ghi rõ từng ô.
>
> **Chú thích đề xuất:** “Hình 3.1. Ví dụ ảnh có polyp và ảnh nền trong bộ dữ liệu sử dụng.” Nếu thêm mask, sửa chú thích để nêu thêm mặt nạ tương ứng. Ghi ID ảnh và nguồn dữ liệu đã xác minh.
>
> **Đoạn sau hình:** giải thích ảnh polyp có nhãn polygon, ảnh nền dùng file nhãn rỗng; không diễn giải nền thành lớp object thứ hai.

### 3.2. Xây dựng và phân chia bộ dữ liệu BG20 — khoảng 1 trang

- [ ] **3.2.1. Bổ sung ảnh nền và biểu diễn nhãn âm tính:** 200 ảnh nền, seed chọn mẫu 42, nhãn `.txt` rỗng, tiền tố `bg_`.
- [ ] **3.2.2. Phân chia tập huấn luyện và tập xác thực:** giữ danh sách polyp 880/120; thêm nền 160/40; lập bảng phân bố cuối cùng.
- [ ] **3.2.3. Tổ chức dữ liệu theo định dạng YOLO:** thư mục ảnh/nhãn, quy tắc cùng tên file, lớp `0: polyp`, cấu hình YAML.

**Bằng chứng:** PX01, PX02, PX04; DL01–DL06. **Vị trí bảng:** cuối 3.2.2, sau đoạn mô tả cách chia tập, dùng số liệu phần 5.1. **Không cần paste ảnh ở mục 3.2:** cây thư mục tại 3.2.3 trình bày bằng văn bản, không cần ảnh chụp màn hình thư mục.

### 3.3. Chuyển đổi mặt nạ sang nhãn polygon — khoảng 2 trang

- [ ] **3.3.1. Nhị phân hóa mặt nạ bằng Otsu:** đầu vào là mask, chuyển sang ảnh xám rồi xác định ngưỡng.
- [ ] **3.3.2. Xử lý hình thái học và trích xuất đường bao:** Closing với kernel chữ nhật 3 × 3, một lần; lấy đường bao ngoài.
- [ ] **3.3.3. Lọc vùng nhỏ và đơn giản hóa đường bao:** loại vùng có diện tích < 20 pixel²; `epsilon = 0.002 × chu_vi`; xử lý trường hợp polygon còn dưới 3 điểm.
- [ ] **3.3.4. Chuẩn hóa tọa độ và xuất nhãn:** chia x cho chiều rộng, y cho chiều cao của mask; chặn trong [0, 1]; ghi lớp 0 và các cặp tọa độ.

**Bằng chứng:** PX03, S01. **Công thức:** `x_norm = x/W`, `y_norm = y/H`, `epsilon = 0.002L`.

> **[CHÈN HÌNH H02 TẠI ĐÂY — cuối mục 3.3.4, sau công thức chuẩn hóa tọa độ và ví dụ định dạng nhãn]**
>
> **Nội dung:** một hình ghép các bước trên cùng một mẫu: mask gốc → nhị phân Otsu → Closing 3 × 3 → đường bao được giữ sau lọc → polygon xấp xỉ phủ lên ảnh nội soi. Ghi rõ tên từng ô; nếu mẫu không bị thay đổi bởi Closing/lọc vùng nhỏ, trình bày đúng kết quả quan sát được.
>
> **Chú thích đề xuất:** “Hình 3.2. Minh họa các bước chuyển mặt nạ polyp sang nhãn polygon YOLO-SEG.” Ghi ID mẫu, tham số S01 và ngày sinh hình; nếu chạy mới để minh họa, ghi rõ đây là hình minh họa tạo từ quy trình trong source.
>
> **Đoạn sau hình:** giải thích quan hệ giữa mask và polygon, tác động quan sát được của từng bước; không khẳng định mask được bảo toàn tuyệt đối hoặc chất lượng model tăng lên chỉ từ hình này.
>
> **Trạng thái:** chờ tìm lại mask nguồn tại phần 5.3. Có thể tham khảo cách minh họa Closing ở VN04, phần 9.1; hình dùng trong mục này cần thể hiện mẫu của đề tài.

Phân biệt: chuẩn hóa tọa độ nhãn ở mục này và chuẩn hóa giá trị pixel ảnh ở mục 3.4 là hai phép xử lý khác nhau. Các bước Otsu/Closing không được mô tả thành xử lý trên ảnh nội soi RGB.

### 3.4. Chuẩn bị ảnh và nhãn khi nạp vào mô hình — khoảng 1 trang

- [ ] **3.4.1. Điều chỉnh kích thước và LetterBox:** giải thích resize giữ tỷ lệ và padding; ghi `imgsz=640`; phân biệt hình dạng đầu vào train và validation theo batch.

> **[CHÈN HÌNH H03 TẠI ĐÂY — trong mục 3.4.1, sau đoạn giải thích resize giữ tỷ lệ và padding, trước mục 3.4.2]**
>
> **Nội dung:** cùng một ảnh polyp ở ba ô: ảnh đầu vào → ảnh resize giữ tỷ lệ → ảnh sau padding bằng LetterBox. Ghi kích thước thực của từng ô và chỉ rõ vùng padding; có thể phủ polygon tương ứng để thấy nhãn thay đổi cùng ảnh.
>
> **Chú thích đề xuất:** “Hình 3.3. Minh họa điều chỉnh kích thước ảnh bằng resize giữ tỷ lệ và LetterBox.” Nếu chọn đầu ra 640 × 640 để minh họa, ghi rõ đó là ví dụ với hình dạng đích này, không đại diện cho mọi batch validation.
>
> **Đoạn sau hình:** giải thích tỷ lệ ảnh được giữ, phần padding bổ sung và tọa độ nhãn được biến đổi tương ứng. Tra PX05, S03–S05 để sinh hình đúng cách xử lý.

- [ ] **3.4.2. Chuyển đổi kênh màu và tensor:** BGR → RGB trong cấu hình `bgr=0`; HWC → CHW; ghép batch thành BCHW.
- [ ] **3.4.3. Chuẩn hóa pixel và tạo mask huấn luyện:** ảnh chuyển sang float và chia 255; polygon được raster hóa, giảm độ phân giải mask theo `mask_ratio=4`, xử lý chồng lấp theo `overlap_mask=true`.

**Bằng chứng:** PX05, PX07, PX08; S03–S08. **Công thức:** `I_norm = I/255`. Với ảnh 640 × 640, mask sau giảm tỷ lệ 4 có kích thước 160 × 160; đây là ví dụ phụ thuộc hình dạng ảnh.

### 3.5. Tăng cường dữ liệu huấn luyện — khoảng 1,5 trang

- [ ] **3.5.1. Mosaic:** ghép ảnh trong huấn luyện; xác suất cấu hình 1.0; đóng Mosaic trong 10 epoch cuối.
- [ ] **3.5.2. Dịch chuyển, thay đổi tỷ lệ và lật ngang:** trình bày các phép đang bật và thông số thực tế.
- [ ] **3.5.3. Biến đổi màu HSV:** giải thích thay đổi sắc độ, độ bão hòa, độ sáng cùng các hệ số cấu hình.

> **[CHÈN HÌNH H04 TẠI ĐÂY — sau phần viết mục 3.5.3, trước mục 3.5.4]**
>
> **Nội dung:** một hình tổng hợp có ô gốc và các ô minh họa lật ngang, dịch chuyển/thay đổi tỷ lệ, biến đổi HSV, Mosaic. Phủ nhãn polygon lên ảnh có polyp để kiểm tra biến đổi hình học; với HSV, hình học nhãn giữ nguyên. Mosaic dùng các mẫu từ tập train, không ghép ảnh validation vào hình minh họa huấn luyện.
>
> **Chú thích đề xuất:** “Hình 3.4. Minh họa các phép tăng cường dữ liệu trong cấu hình huấn luyện YOLO26-SEG + TSVM.” Ghi ID ảnh, các phép/tham số, seed sinh hình nếu có và ngày sinh hình. Ví dụ mới cần được ghi là minh họa, không phải ảnh batch của lần train lịch sử.
>
> **Đoạn sau hình:** giải thích biến đổi hình học tác động đồng thời lên ảnh và nhãn, HSV thay đổi màu ảnh; xác suất/hệ số cụ thể lấy từ phần 6. Không thêm xoay, lật dọc, MixUp, CutMix hoặc Copy-Paste vào hình mô tả cấu hình đang đối chiếu.
>
> **Tham khảo bố cục:** VN01 ở phần 9.1 có hình tăng cường dữ liệu cho phân đoạn. Các phép của tài liệu tham khảo không tự động trở thành phép đã dùng trong đề tài.

- [ ] **3.5.4. Cấu hình train/validation:** tăng cường ngẫu nhiên được bật khi `mode == 'train'`; validation dùng nhánh xử lý đánh giá.

**Bằng chứng:** PX06, S02–S05, S09. **Vị trí bảng:** cuối 3.5.4, tổng hợp các tham số tăng cường dữ liệu từ phần 6. Không cần chụp `args.yaml` thành ảnh.

Blur/MedianBlur/ToGray/CLAHE chỉ được trình bày như nhánh mặc định **có điều kiện** của Albumentations, trừ khi có log môi trường xác nhận. Khi tạo hình minh họa mới, ghi đó là ví dụ minh họa và thông số sinh ảnh; không gọi là artifact lịch sử nếu chưa đối chiếu.

### 3.6. Kiểm tra tính toàn vẹn và khả năng tái lập — khoảng 1 trang

- [ ] **3.6.1. Số lượng ảnh và nhãn:** ảnh có nhãn tương ứng; nhãn rỗng đúng số lượng; đối chiếu split và danh sách ảnh nền.
- [ ] **3.6.2. Tính hợp lệ của polygon:** lớp 0, ít nhất 3 cặp tọa độ, giá trị hữu hạn thuộc [0, 1].
- [ ] **3.6.3. Tái lập và giới hạn kiểm tra:** phân biệt seed chọn ảnh nền với seed train; lưu manifest; báo cáo kiểm tra trùng tên/nội dung file và giới hạn đối với ảnh gần trùng, bệnh nhân.

**Bằng chứng:** PX09; DL02–DL05, DL07; S01, S08. Kiểm tra SHA-256 trong DL07 là kiểm tra bổ sung ngày 07/10/2026, không phải bước đã có trong script chuyển đổi gốc.

**Không cần paste ảnh ở mục 3.6:** dùng bảng tiêu chí, kết quả và giới hạn kiểm tra sau 3.6.2 hoặc cuối 3.6.3; lấy kết quả từ DL07. Không thay bảng này bằng ảnh chụp log terminal.

### 3.7. Tổng hợp quy trình tiền xử lý — khoảng 0,5 trang

- [ ] Vẽ sơ đồ phân biệt xử lý mask trước khi train và biến đổi ảnh/nhãn khi nạp dữ liệu.
- [ ] Nêu đầu ra: dataset YOLO-SEG một lớp, ảnh nền có nhãn rỗng, batch ảnh và mask sẵn sàng cho huấn luyện.
- [ ] Nêu rõ TSVM xử lý đặc trưng trong mô hình; không có bước chuẩn bị nhãn riêng cho TSVM trong pipeline đã rà soát.

> **[CHÈN HÌNH H05 TẠI ĐÂY — trong mục 3.7, sau đoạn giới thiệu quy trình chung và trước đoạn kết nối sang phần huấn luyện]**
>
> **Nội dung:** vẽ lại sơ đồ phần 8, thể hiện chuẩn bị BG20 trước khi train, nhánh nạp train và nhánh nạp validation. Tách rõ ảnh RGB và mask nguồn; đặt TSVM trong khối model, sau bước chuẩn hóa batch.
>
> **Chú thích đề xuất:** “Hình 3.5. Quy trình xây dựng dữ liệu và tiền xử lý cho YOLO26-SEG + TSVM.” Ghi “Tổng hợp từ source và cấu hình của đề tài” và dẫn các mốc PX liên quan.
>
> **Đoạn sau hình:** mô tả đầu ra của quy trình, sự khác nhau giữa train/validation và vai trò đầu vào của model. Dùng sơ đồ đã vẽ rõ chữ, không paste ảnh chụp toàn bộ source code.

**Bằng chứng:** PX01–PX10, S10. Kiến trúc, optimizer, learning rate, loss và kết quả mAP nên được triển khai ở các phần tương ứng khác của khóa luận.

### Bản đồ vị trí paste ảnh trong bản thảo

Kế hoạch đề xuất có **5 hình tổng hợp** để giữ dung lượng khoảng 8 trang. `H01`–`H05` là mã tra cứu trong Markdown; số “Hình 3.x” chỉ là gợi ý, cần đổi theo chương và thứ tự hình chung của khóa luận. Các hình chưa được tạo/chèn trong lần chỉnh tài liệu này.

| Mã | Giai đoạn viết | Paste ở đâu? | Nội dung cần thấy | Nguồn tạo hình / tình trạng |
|---|---|---|---|---|
| **H01** | 1 | Cuối **3.1.3** | Ảnh polyp và ảnh nền; mask gốc là ô bổ sung nếu có | Ảnh có sẵn ở DL01, ví dụ phần 5.2; mask nguồn còn thiếu tại đường dẫn kỳ vọng. |
| **H02** | 2 | Cuối **3.3.4** | Mask → Otsu → Closing → contour → polygon | S01/PX03; chờ mask nguồn trước khi tạo đủ các ô. |
| **H03** | 2 | Trong **3.4.1**, sau đoạn LetterBox | Ảnh trước/sau resize và padding, kích thước thực | Ảnh DL01 + PX05; cần sinh hình minh họa từ cách xử lý trong source. |
| **H04** | 2 | Sau **3.5.3**, trước 3.5.4 | Các augmentation đang bật và nhãn tương ứng | Tập train DL01 + S02–S05/PX06; cần sinh hình minh họa. |
| **H05** | 3 | Trong **3.7**, sau đoạn giới thiệu quy trình | Sơ đồ tổng thể trước train, train và validation | Vẽ từ phần 8, đối chiếu PX01–PX09 và S10. |

**Các mục dùng chữ/bảng thay cho ảnh:** 3.2 dùng bảng số lượng và cây thư mục; 3.4.2 dùng mô tả HWC → CHW → BCHW; 3.4.3 dùng công thức chia 255 và mô tả raster hóa mask; 3.5.4 dùng bảng cấu hình; 3.6 dùng bảng kiểm tra. Không cần thêm hình riêng cho các mục này trong kế hoạch 5 hình.

## 3. Đánh dấu từng bước xử lý và vị trí code

| Mã bước | Thao tác | File và mốc tra cứu | Mục viết | Bằng chứng |
|---|---|---|---|---|
| **PX01** | Định vị đầu vào; đọc split polyp 880/120 | S01, `main()`, dòng 121; các đường dẫn 122–135, đọc ID 151–159 | 3.1, 3.2 | CODE; danh sách ID đã CHECKED |
| **PX02** | Chọn 200 ảnh nền từ danh sách file được sắp xếp; chia 160/40 | S01, dòng 163–169; lưu danh sách 182–185 | 3.2, 3.6 | CODE + ARTIFACT + CHECKED |
| **PX03** | Mask → polygon YOLO | S01, `convert_mask_to_yolo_polygons()`, dòng 42; xám 51–58, Otsu 63, Closing 66–67, contour 70, diện tích 76–78, epsilon 88–89, fallback 92–95, chuẩn hóa 99–106 | 3.3 | CODE; chưa chạy lại trên mask nguồn |
| **PX04** | Sao chép ảnh polyp/nền, ghi nhãn polygon/nhãn rỗng, sinh YAML | S01, dòng 191–204, 209–221, 248–272 | 3.2 | CODE + ARTIFACT |
| **PX05** | Đọc ảnh và resize; chuẩn bị hình dạng batch; LetterBox | S04, `load_image()` dòng 228, resize 268–281, `set_rectangle()` dòng 386; S03, `build_transforms()` dòng 304; S05, `LetterBox` dòng 1634 | 3.4 | CODE + CONFIG |
| **PX06** | Augmentation khi train, đóng Mosaic cuối quá trình train | S07, `build_yolo_dataset()`, dòng 272; S03, dòng 313–319 và `close_mosaic()` dòng 364; S05, `v8_transforms()` dòng 2773; S09, dòng 459–460 và 1079 | 3.5 | CODE + CONFIG |
| **PX07** | RGB/CHW; polygon → mask, xử lý overlap, giảm tỷ lệ mask | S05, `Format._format_img()` dòng 2437, `Format._format_segments()` dòng 2467; S08, `polygon2mask()` dòng 426, `polygons2masks_overlap()` dòng 468; S03, dòng 328–330 | 3.4 | CODE + CONFIG |
| **PX08** | Chuyển batch sang device, float, chia 255 | S06, `preprocess_batch()` dòng 107, phép chia dòng 119; S11, `SegmentationTrainer` kế thừa `DetectionTrainer`, dòng 13 | 3.4 | CODE |
| **PX09** | Sanity check số lượng và nhãn rỗng; kiểm tra khi nạp YOLO | S01, dòng 224–245; S08, `verify_image_label()` dòng 320; DL07 là kiểm tra bổ sung độc lập | 3.6 | CODE + CHECKED |
| **PX10** | Suy luận trên ảnh thông thường: LetterBox, RGB, tensor, chia 255 | S12, `preprocess()` dòng 160; `pre_transform()` dòng 200 | 3.7 hoặc phần ứng dụng | CODE; nhánh tensor đầu vào có quy ước riêng |

Ghi chú PX05: S06 dòng 76 đặt `rect=mode == 'val'`. Validation có thể dùng batch chữ nhật; S04 gắn `rect_shape` theo batch và LetterBox sử dụng hình dạng đó. Vì vậy viết “kích thước cấu hình `imgsz=640`” chính xác hơn khẳng định mọi ảnh validation đều thành 640 × 640.

## 4. Chỉ mục source có thể mở trực tiếp

Các link là đường dẫn tương đối từ folder `output` để tài liệu vẫn dùng được khi chuyển cả repository sang máy khác. Số dòng được ghi riêng trong phần 3.

| Mã | File | Vai trò |
|---|---|---|
| **S01** | [convert_kvasir_with_background_to_yolo_seg.py](<../archive/Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py>) | Script chuẩn bị BG20, chuyển mask và lưu metadata. |
| **S02** | [args.yaml của TSVM seed 0](<../archive/Ket_Qua_V2/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/Kvasir_BG20_YOLO26s_seg_TSVM_s0_w2/args.yaml>) | Cấu hình train lưu lại, nguồn thông số ưu tiên trong tài liệu này. |
| **S03** | [data/dataset.py](<../archive/ultralytics_Topology-Shape-aware VMamba/data/dataset.py>) | YOLODataset, nhánh train/val, formatter và đóng Mosaic. |
| **S04** | [data/base.py](<../archive/ultralytics_Topology-Shape-aware VMamba/data/base.py>) | Đọc ảnh, resize, batch chữ nhật. |
| **S05** | [data/augment.py](<../archive/ultralytics_Topology-Shape-aware VMamba/data/augment.py>) | LetterBox, augmentation và Format. |
| **S06** | [models/yolo/detect/train.py](<../archive/ultralytics_Topology-Shape-aware VMamba/models/yolo/detect/train.py>) | Dataloader, chuẩn hóa batch trước khi vào model. |
| **S07** | [data/build.py](<../archive/ultralytics_Topology-Shape-aware VMamba/data/build.py>) | Khởi tạo dataset với augmentation chỉ cho train. |
| **S08** | [data/utils.py](<../archive/ultralytics_Topology-Shape-aware VMamba/data/utils.py>) | Xác minh ảnh/nhãn và raster hóa polygon thành mask. |
| **S09** | [engine/trainer.py](<../archive/ultralytics_Topology-Shape-aware VMamba/engine/trainer.py>) | Thời điểm đóng Mosaic. |
| **S10** | [YAML kiến trúc TSVM](<../archive/ultralytics_Topology-Shape-aware VMamba/cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml>) và [topology_shape_vmamba.py](<../archive/ultralytics_Topology-Shape-aware VMamba/nn/modules/topology_shape_vmamba.py>) | C2TSVMamba tại layer 10; phân biệt module model với tiền xử lý. |
| **S11** | [models/yolo/segment/train.py](<../archive/ultralytics_Topology-Shape-aware VMamba/models/yolo/segment/train.py>) | Kế thừa xử lý batch từ DetectionTrainer. |
| **S12** | [engine/predictor.py](<../archive/ultralytics_Topology-Shape-aware VMamba/engine/predictor.py>) | Tiền xử lý ở nhánh suy luận. |
| **S13** | [notebook train TSVM](<../archive/Cell Kaggle/kvasir-yolo26s-seg-topology-shape-awar.ipynb>) | Cell có tiêu đề “CELL 1” tạo data YAML trên Kaggle; cell có tiêu đề “CELL 2” gọi `model.train()`. Notebook hiện ghi SEED = 10; không dùng nó để thay seed trong artifact seed 0. |
| **S14** | [args.yaml của baseline seed 0](<../archive/Ket_Qua_V2/KetQua_Nen/YOLOv26s-seg/Kvasir_BG20_Baseline_YOLO26s_seg_s0_w2/args.yaml>) | Đối chiếu cấu hình dữ liệu giữa baseline và TSVM seed 0. Các tham số liệt kê ở phần 6 đã được đối chiếu tương ứng. |

Tên hàm `v8_transforms` trong source là tên pipeline dùng chung; không có nghĩa mô hình đang nghiên cứu là YOLOv8.

## 5. Đánh dấu dữ liệu, cấu hình và artifact

| Mã | Vị trí | Cách sử dụng khi viết |
|---|---|---|
| **DL01** | [Kvasir_YOLO_SEG_BG20](../archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/) | Bộ dữ liệu đầu ra thực tế: `images/train`, `images/val`, `labels/train`, `labels/val`. |
| **DL02** | [dataset_bg20_summary.json](../archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/dataset_bg20_summary.json) | Metadata số lượng lịch sử; đã đối chiếu với file hiện có. |
| **DL03** | [train.txt](../archive/train.txt), [val.txt](../archive/val.txt) | Danh sách ID polyp gốc được converter sử dụng; tương ứng 880/120 ảnh. |
| **DL04** | [selected_normal_cecum_train_160.txt](../archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/selected_normal_cecum_train_160.txt) | Danh sách 160 ảnh nền train trước khi thêm tiền tố `bg_`. |
| **DL05** | [selected_normal_cecum_val_40.txt](../archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/selected_normal_cecum_val_40.txt) | Danh sách 40 ảnh nền validation trước khi thêm tiền tố `bg_`. |
| **DL06** | [data_bg20.yaml trong dataset](../archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/data_bg20.yaml), [data_bg20_local.yaml](tien_xu_ly/kiem_tra/bang_chung/data_bg20_local.yaml) | YAML trong dataset còn đường dẫn máy cũ. YAML local chỉ tới dataset trong workspace hiện tại. Notebook S13 tạo YAML riêng trên Kaggle. |
| **DL07** | [kiem_tra_du_lieu_bg20.json](kiem_tra_du_lieu_bg20.json) | Kết quả kiểm tra bổ sung 07/10/2026, gồm số lượng, định dạng nhãn, manifest và SHA-256 giữa train/val. |
| **DL08** | [README.md](../README.md), [CURRENT_PROJECT_STATUS.md](../CURRENT_PROJECT_STATUS.md) | Phân biệt pipeline BG20 chính với semantic phụ trợ và các thế hệ thí nghiệm. Đối chiếu với source/artifact khi tài liệu trạng thái khác workspace. |

### 5.1. Số lượng đã kiểm tra trực tiếp

| Đại lượng | Train | Validation | Tổng |
|---|---:|---:|---:|
| Ảnh polyp | 880 | 120 | 1.000 |
| Ảnh nền | 160 | 40 | 200 |
| Tổng ảnh | 1.040 | 160 | 1.200 |
| File nhãn | 1.040 | 160 | 1.200 |
| Nhãn rỗng 0 byte | 160 | 40 | 200 |
| Dòng polygon | 936 | 127 | 1.063 |

Số dòng polygon là số vùng được biểu diễn trong nhãn, không phải số ảnh hoặc số bệnh nhân; một ảnh có thể có nhiều polygon. Không dùng bảng này để suy ra loại mô bệnh học hoặc mức độ bệnh.

Kiểm tra bổ sung: không thiếu nhãn, không có nhãn không kèm ảnh; toàn bộ dòng polygon có lớp 0, ít nhất 3 cặp tọa độ hữu hạn trong [0, 1]. Danh sách ID polyp và danh sách nền khớp artifact. Không trùng tên ảnh giữa train/val và không có file ảnh trùng byte giữa hai tập theo SHA-256. Chi tiết: DL07.

### 5.2. File mẫu để mở và tra cứu

- Ảnh polyp train: [cju0qkwl35piu0993l0dewei2.jpg](../archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/images/train/cju0qkwl35piu0993l0dewei2.jpg), [nhãn polygon tương ứng](../archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/labels/train/cju0qkwl35piu0993l0dewei2.txt).
- Ảnh polyp validation: [cju0s690hkp960855tjuaqvv0.jpg](../archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/images/val/cju0s690hkp960855tjuaqvv0.jpg), [nhãn polygon tương ứng](../archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/labels/val/cju0s690hkp960855tjuaqvv0.txt).
- Ảnh nền train: [bg_01af3454-037f-4708-b73c-6ec4423b6a61.jpg](../archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/images/train/bg_01af3454-037f-4708-b73c-6ec4423b6a61.jpg), [nhãn rỗng](../archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/labels/train/bg_01af3454-037f-4708-b73c-6ec4423b6a61.txt).

### 5.3. Đầu vào được script yêu cầu nhưng chưa có tại đường dẫn tương ứng

S01 kỳ vọng các thư mục sau dưới `base_dir` (biến này đang trỏ tới folder `archive` trên máy tác giả):

```text
Kvasir-SEG/Kvasir-SEG/images/
Kvasir-SEG/Kvasir-SEG/masks/
normal-cecum/normal-cecum/    (hoặc normal-cecum/)
```

Tại workspace này, cả bốn đường dẫn tương ứng dưới `archive/` đều không tồn tại khi kiểm tra. Chỉ xác nhận việc thiếu tại các đường dẫn kỳ vọng, không kết luận dữ liệu nguồn không tồn tại ở mọi nơi khác. Cần tìm/cung cấp lại dữ liệu nguồn trước khi tạo hình “mask gốc” hoặc tái chạy quy trình chuyển đổi. Không thể xác minh lại mức độ bảo toàn mask nguồn chỉ từ polygon đã lưu.

## 6. Bảng thông số cần dùng đúng khi viết

Thông số converter từ S01; thông số train ưu tiên S02. S14 có các giá trị tương ứng cho những thông số train trong bảng này.

| Thông số | Giá trị | Ý nghĩa / cách diễn đạt |
|---|---|---|
| `min_area` | 20.0 | Bỏ contour có diện tích < 20 pixel² trong hệ tọa độ mask nguồn. |
| `epsilon_ratio` | 0.002 | Epsilon của `approxPolyDP` bằng 0.002 lần chu vi contour. |
| Closing | Kernel RECT 3 × 3, 1 lần | Áp dụng lên mask nhị phân. |
| Contour | `RETR_EXTERNAL`, `CHAIN_APPROX_SIMPLE` | Chỉ lấy đường bao ngoài; không lưu riêng lỗ bên trong như một cấu trúc nhãn. |
| Seed chọn nền | 42 | Dùng sau khi sắp xếp danh sách ảnh nền; khác seed train. |
| `imgsz` | 640 | Kích thước cấu hình; không khẳng định mọi batch validation vuông. |
| `rect` trong S02 | false | Cấu hình train lưu lại; nhánh xây dataset validation ở S06 đặt rect theo mode. |
| `multi_scale` | 0.0 | Không bật multi-scale trong cấu hình này. |
| `bgr` | 0.0 | Formatter chuyển ảnh 3 kênh BGR sang RGB. |
| Pixel ảnh | `float() / 255` | Chuẩn hóa pixel về [0, 1], không phải chuẩn hóa mean/std ImageNet. |
| `mask_ratio` | 4 | Độ phân giải mask phụ thuộc H/W của ảnh sau biến đổi. |
| `overlap_mask` | true | Mask hợp nhất mã hóa chỉ số instance, không chỉ là một mask nhị phân chung. |
| `mosaic` | 1.0 | Xác suất Mosaic trong giai đoạn đang bật. |
| `close_mosaic` | 10 | Đóng Mosaic 10 epoch cuối trong cấu hình train 100 epoch. |
| `translate` | 0.1 | Hệ số dịch chuyển ngẫu nhiên. |
| `scale` | 0.5 | Hệ số biến đổi tỷ lệ; không có nghĩa mọi ảnh đều thu nhỏ còn 50%. |
| `fliplr` | 0.5 | Xác suất lật ngang 50%. |
| `hsv_h`, `hsv_s`, `hsv_v` | 0.015; 0.7; 0.4 | Các hệ số biến đổi HSV, không phải xác suất áp dụng 1,5%/70%/40%. |
| `degrees`, `shear`, `perspective`, `flipud` | 0.0 | Không bật các phép này trong cấu hình đối chiếu. |
| `mixup`, `cutmix`, `copy_paste` | 0.0 | Không bật các phép này trong cấu hình đối chiếu. |
| Blur, MedianBlur, ToGray, CLAHE | Mỗi phép `p=0.01` trong code mặc định | Có điều kiện Albumentations; cần log để xác nhận lần chạy lịch sử. |

S02: `seed=0`, `epochs=100`. S13 hiện ghi `SEED=10`; cần chọn đúng artifact khi mô tả một thí nghiệm cụ thể. Không viết seed 42 là seed huấn luyện chung của toàn dự án.

## 7. Những phát biểu cần phân biệt khi viết khóa luận

| Chủ đề | Cách viết có bằng chứng | Điểm không nên khẳng định khi chưa xác minh |
|---|---|---|
| Nhiệm vụ | Phân đoạn polyp trên ảnh nội soi đại trực tràng, lớp nhãn `polyp`. | Mô hình hiện phân loại nhiều bệnh, ung thư hoặc loại mô bệnh học. |
| BG20 | 200 nền bằng 20% của 1.000 ảnh polyp gốc; nền chiếm 16,67% tổng 1.200 ảnh. | 20% toàn bộ bộ dữ liệu cuối cùng là ảnh nền. |
| Split | Polyp 880/120; tổng sau bổ sung 1.040/160. | Toàn bộ bộ dữ liệu được chia train/val 80/20. Chú thích đầu S01 không khớp số lượng thực tế. |
| Tập test | Pipeline BG20 đã kiểm tra có train và val. | Có tập test độc lập nếu chưa có manifest/artifact của tập đó. |
| Xử lý ảnh | Converter sao chép ảnh; Otsu và Closing xử lý mask. | Toàn bộ ảnh nội soi được Otsu, Closing hoặc CLAHE trước khi lưu BG20. |
| Nhãn nền | Nền dùng `.txt` rỗng, không có object được gán nhãn. | Background là lớp object thứ hai trong YAML hiện tại. |
| Chất lượng mask | Closing, loại vùng nhỏ, lấy contour ngoài và xấp xỉ polygon là các thao tác trong code. | Mask được bảo toàn tuyệt đối hoặc chắc chắn cải thiện độ chính xác; cần kiểm tra định lượng/ablation. |
| Rò rỉ dữ liệu | Kiểm tra bổ sung không thấy trùng tên hay trùng byte giữa train/val. | Đã đảm bảo độc lập theo bệnh nhân hoặc loại hết ảnh gần trùng. |
| Tái lập | Có seed, manifest và cấu hình lưu lại. | Tái lập 100% mọi môi trường chỉ nhờ `random.seed(42)`. |
| Các đời code | Dùng source hiện có và config lưu lại để mô tả pipeline. | Source hôm nay chứng minh đầy đủ phiên bản thư viện đã chạy trong mọi seed lịch sử. |

**Khả năng chạy lại S01:** `base_dir` dòng 122 còn đường dẫn cố định trên máy cũ; `output_dir` dòng 135 khác vị trí artifact trong workspace này. Script còn có `shutil.rmtree(output_dir)` khi output đã tồn tại (dòng 174–176). Cần điều chỉnh và kiểm tra đường dẫn đầu ra trước khi tái chạy. Lần rà soát này không chạy converter.

**Pipeline phụ trợ:** [data_prep/prepare_kvasir_semantic.py](../data_prep/prepare_kvasir_semantic.py) và [datasets/kvasir_semantic_dataset.py](../datasets/kvasir_semantic_dataset.py) thuộc pipeline semantic phụ trợ được README mô tả; không dùng chúng làm bằng chứng cho quy trình chính BG20 YOLO26-SEG + TSVM.

## 8. Sơ đồ quy trình để chuyển thành hình khóa luận

```text
CHUẨN BỊ DATASET TRƯỚC KHI TRAIN

Danh sách ID polyp 880/120 ────────────────┐
Ảnh polyp gốc ── sao chép ────────────────┤
Mask gốc ── xám → Otsu → Closing ────────┤
          → contour → lọc vùng nhỏ       │
          → xấp xỉ polygon               ├─→ BG20: ảnh + nhãn YOLO + YAML
          → tọa độ chuẩn hóa → .txt ─────┤
Ảnh normal-cecum → chọn 200, seed 42     │
          → train 160 / val 40           │
          → sao chép + nhãn rỗng ────────┘

NẠP DỮ LIỆU KHI HUẤN LUYỆN

BG20 train → đọc/resize → augmentation ảnh và nhãn
           → Format: RGB, CHW, polygon thành mask
           → batch → float / 255 → YOLO26-SEG + TSVM

NẠP DỮ LIỆU KHI XÁC THỰC

BG20 val → đọc/resize → LetterBox theo hình dạng batch
         → Format ảnh và mask → chuẩn hóa batch → đánh giá
```

Sơ đồ là bản tổng hợp từ source, không phải bằng chứng cho việc chạy lại. Cần vẽ nhánh ảnh và mask riêng trong hình cuối để tránh hiểu nhầm Otsu áp dụng lên ảnh RGB.

## 9. Tài liệu tham khảo về cấu trúc và số trang

Các nguồn dưới đây phục vụ tham khảo cách viết. Chúng không thay thế bằng chứng code của dự án và không tạo thành quy định giới hạn trang chung của trường. Số trang tính theo số in trong PDF; trang đầu/cuối có thể dùng chung với mục khác.

| Tài liệu | Bậc học | Phạm vi đã xác minh | Bài học về cấu trúc |
|---|---|---|---|
| Nando Metzger, ETH Zurich, 2019 — [DSM Refinement with Deep Encoder-Decoder Networks](https://ethz.ch/content/dam/ethz/special-interest/baug/igp/photogrammetry-remote-sensing-dam/documents/pdf/Student_Theses/BA_Metzger.pdf) | Cử nhân | Mục 3.3, trang 22–26: 5 trang. Nếu thêm dữ liệu gốc ở 3.2 thì cụm này trải 20–26: 7 trang. | Giới thiệu dữ liệu trước; sau đó tiền xử lý, phân chia, tăng cường, chuẩn hóa. |
| Guillem Bonet Filella, ETH Zurich, 2018 — [Cocoa Segmentation in Satellite Images with Deep Learning](https://ethz.ch/content/dam/ethz/special-interest/baug/igp/photogrammetry-remote-sensing-dam/documents/pdf/Student_Theses/BA_BonetFilella.pdf) | Cử nhân | Mục 3.3, trang 27–28: trải 2 trang có nội dung dùng chung. | Trình bày quy trình theo bước và tiêu chí lựa chọn ảnh; mục nhãn/chia dữ liệu nằm riêng. |
| Debleena Sengupta, UCLA, 2019 — [Deep Learning Architectures for Automated Image Segmentation](https://web.cs.ucla.edu/~dt/theses/sengupta-ms-thesis.pdf) | Thạc sĩ | Mục 5.2 từ trang 44 đến đầu trang 50: trải 7 trang, gồm cả loss/metrics. Nội dung chuẩn bị dữ liệu nằm 44 đến một phần 48. | Chia theo từng vấn đề: thống nhất hướng ảnh, chuẩn hóa, tạo patch. Với đồ án này, tách loss/metrics sang phần mô hình/thực nghiệm. |

Nguồn bổ sung về khóa luận được đánh giá cao: Joy Hsu, Stanford, 2021, khóa luận cử nhân về học không giám sát trên ảnh y sinh 2D/3D. [Trang tác giả](https://joycjhsu.github.io/) ghi nhận giải Ben Wegbreit cho khóa luận tốt nhất; [bản lưu Stanford](https://purl.stanford.edu/nv775dt3762) chưa truy cập được toàn văn trong lần tìm kiếm trước. **Không dùng tài liệu này để đưa ra số trang tiền xử lý.**

Khuyến nghị 8 trang ở phần 2 là điều chỉnh theo số bước cụ thể của dự án. Phần 3.3 nên được ưu tiên vì nó nối nhãn mask nguồn với định dạng YOLO-SEG mà model thực sự sử dụng.

### 9.1. Tài liệu Việt Nam có hình minh họa để tham khảo

Các vị trí dưới đây đã được kiểm tra trong lượt tìm tài liệu trước khi cập nhật Markdown. “Trang in” là số trên trang tài liệu; “trang PDF” là vị trí trang trong trình đọc, tính từ 1. Các nguồn này phục vụ chọn cách trình bày hình; không xác nhận kỹ thuật tương ứng đã được áp dụng trong dự án BG20.

| Mã | Tác giả, cơ sở và loại tài liệu | Hình đã tìm được / link tham khảo | Áp dụng khi chuẩn bị hình của đề tài |
|---|---|---|---|
| **VN01** | Nguyễn Tú Anh, 2024; Học viện Khoa học và Công nghệ; luận văn thạc sĩ về kết hợp phân đoạn và phân lớp ảnh da liễu ISIC-2018 | **Hình 2.3**, trang in **47**, trang PDF **60**, minh họa tăng cường dữ liệu cho phân đoạn. [Mở tại trang PDF 60](https://gust.edu.vn/media/30/uftai-ve-tai-day30785.pdf#page=60). | Tham khảo cách đặt hình và giải thích biến đổi đồng thời ảnh/nhãn cho **H04**. Chỉ minh họa các phép đang bật trong S02. |
| **VN02** | Đỗ Minh Tuấn, 2024; Học viện Khoa học và Công nghệ; luận văn thạc sĩ về kết hợp CNN để chẩn đoán ung thư da ở Việt Nam | **Hình 3.3**, trang in **54**, trang PDF **66**: ảnh gốc, cân bằng sáng, cân bằng histogram, loại bỏ tóc. [Mở tại trang PDF 66](https://gust.edu.vn/media/30/uftai-ve-tai-day30787.pdf#page=66). | Tham khảo bố cục các ô trước/sau thao tác cho **H02–H03**; nội dung từng ô thay bằng bước thực tế của đề tài. |
| **VN03** | Tống Võ Anh Thuận và Lê Huỳnh Quang Vũ, 2025; UIT, ĐHQG-HCM; khóa luận đếm người kết hợp WiFi và thị giác máy tính | **Hình 5.5** về Gamma correction và **Hình 4.1** về luồng hệ thống, xem trực tiếp trên [website UIT](https://nc.uit.edu.vn/khoa-luan/ket-hop-tin-hieu-wife-va-thi-giac-may-tinh-trong-bai-toan-dem-nguoi-trong-dieu-kien-thieu-sang). Chưa xác minh số trang trong toàn văn. | Tham khảo cách dùng hình giải thích xử lý ảnh và sơ đồ cho **H03/H05**. Không bổ sung Gamma correction vào mô tả BG20 nếu source/config không có bước này. |
| **VN04** | Vũ Việt Hà, 2009; Trường Đại học Dân lập Hải Phòng; đồ án tốt nghiệp về phép toán hình thái, thuộc xử lý ảnh truyền thống | **Hình 2.8**, trang in và trang PDF **19**, minh họa Closing trên ảnh nhị phân. [Mở tại trang PDF 19](https://lib.hpu.edu.vn/bitstream/handle/123456789/18079/12_VuVietHa_CT901.pdf?isAllowed=y&sequence=1#page=19). | Tham khảo cách thể hiện trước/sau Closing trong **H02**; hình thực nghiệm của đề tài dùng mask polyp và kernel 3 × 3 theo S01. |

**Nguồn hình trong bản thảo:** H01 dùng ảnh trong dataset của đề tài và dẫn nguồn dữ liệu đã xác minh; H02–H04 là hình tạo từ thao tác trong source, cần ghi mẫu/tham số; H05 là sơ đồ tự tổng hợp. Nếu sử dụng lại hoặc vẽ lại một hình từ tài liệu tham khảo, ghi nguồn tương ứng dưới hình và trong danh mục tài liệu tham khảo; không chú thích thành kết quả của đề tài.

## 10. Checklist trước khi bàn giao bản thảo

- [ ] Hoàn thành bản nháp của cả 3 giai đoạn ở phần 1.1; còn dữ liệu/hình nào thiếu thì ghi rõ trạng thái.
- [ ] Đã thay 5 dấu `CHÈN HÌNH` bằng hình đúng nội dung/vị trí hoặc ghi rõ hình còn chờ dữ liệu; chưa có ảnh thì không xem chương là đã hoàn thiện.
- [ ] Mỗi hình có câu dẫn trước hình, chú thích, nguồn và đoạn giải thích sau hình; đánh số theo chương/thứ tự chung của khóa luận.
- [ ] Bổ sung trích dẫn nguồn công bố Kvasir-SEG và nguồn normal-cecum đã xác minh.
- [ ] Nhất quán thuật ngữ: ảnh, mask gốc, polygon, mask huấn luyện, instance, background, train, validation.
- [ ] Mọi thông số có nguồn S01/S02 hoặc artifact của thí nghiệm đang mô tả.
- [ ] Bảng dữ liệu khớp DL07; không nhầm số ảnh với số polygon.
- [ ] Hình ảnh ghi đúng nguồn: mask gốc, mask raster hóa từ polygon, hoặc ảnh sinh minh họa.
- [ ] Không gán Otsu/Closing trên mask thành phép tiền xử lý ảnh RGB.
- [ ] Phân biệt seed chọn nền, seed train và cấu hình notebook mẫu.
- [ ] Phân biệt kiểm tra mới ngày 07/10/2026 với quy trình lịch sử.
- [ ] Không khẳng định có test độc lập, kiểm tra theo bệnh nhân, hoặc cải thiện độ chính xác nếu thiếu bằng chứng.
- [ ] Đối chiếu lại số dòng nếu source thay đổi; ưu tiên tìm theo tên hàm.
- [ ] Mỗi bước được viết theo trình tự: vấn đề dữ liệu → mục đích → phương pháp/thông số → đầu ra minh họa.
