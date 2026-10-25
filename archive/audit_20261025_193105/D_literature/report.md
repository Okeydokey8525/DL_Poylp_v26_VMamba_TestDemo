# Kiểm toán tài liệu tham khảo và nghiên cứu liên quan

Ngày kiểm tra 25/10/2026. Phòng D. Bản Word gắn với SHA-256 `2caaf8b42c299f3c73a0087654f8f7d3c2986a83b8878d713613e0c9e1ed0856`. Chỉ ghi đầu ra trong `D_literature`; không sửa TLTK, Word hoặc bibliography gốc; không nộp Turnitin.

## Kết luận

Đã đối chiếu **24 mục tham khảo của Word**, kiểm kê và trích văn bản **24 PDF TLTK**, dùng thêm bốn PDF arXiv công khai tải riêng cho kiểm toán. Metadata của 23 mục được xác nhận qua nguồn chính thức/DOI deposit; trang Kaggle mục [3] tồn tại nhưng chưa chứng minh được phát biểu về nguồn gốc danh sách chia 880/120. Không phát hiện một tài liệu hư cấu trong danh mục đã xác thực. Kết luận này không đồng nghĩa mọi câu gắn citation đều đã có bằng chứng đầy đủ.

Ba dòng số liệu literature trong Bảng 5.8 khớp bảng gốc, có kiểm cả text lẫn ảnh trang PDF. Những công trình gần nhất đã được Word thảo luận, đặc biệt C2PSA replacement và convolutional gating; không có cơ sở gọi đề tài là công trình đầu tiên chỉ vì kết hợp YOLO với Mamba. Kho TLTK có thêm nguồn phù hợp nhưng chưa sử dụng trong Word; không cần bổ sung hàng loạt để tăng số lượng.

## Phương pháp và bằng chứng

- `reference_verification.csv`: 24 dòng, giữ riêng metadata, mức hỗ trợ phát biểu, vị trí Word, nguồn primary, locator và giới hạn.
- `local_pdf_inventory.csv`: 24 PDF, hash, số trang, metadata và text trang đầu. Đây là nhận dạng hiện vật, không tự chứng minh license hoặc chất lượng học thuật.
- `metadata/`: các bản deposit Crossref và listing Kaggle đã lưu trước gián đoạn; các lỗi HTTP403/502 không được diễn giải thành tài liệu không tồn tại.
- `download_log.csv`: bốn PDF public arXiv, URL phiên bản, hash và số trang; chỉ dùng riêng trong kiểm toán.
- `table_images/`: các trang kiểm trực quan Bảng 1 Polyp-Mamba, Bảng I Topo-VM-UNetV2 và Bảng 1 CSG-Mamba. Đã mở ảnh để xác nhận cột/đơn vị.
- Web: mở trực tiếp arXiv, Springer/MICCAI, trang tác giả sách, OpenCV official wiki, Ultralytics và SciPy docs; tra cứu bổ sung các công trình gần bằng nguồn hội nghị/nhà xuất bản gốc.
- `related_work_matrix.csv`: 10 mô hình/công trình, phân biệt task, cơ chế, dữ liệu, độ đo, liên quan và tình trạng coverage. Đây không phải leaderboard.

Nguồn web đang thay đổi theo thời gian; audit ghi ngày truy cập. Mô tả runtime của fork 8.4.127 phải được đối chiếu source tại dự án. Tài liệu Ultralytics hiện tại không thay thế lịch sử mã đã huấn luyện.

## Các điểm cần xử lý

### D-001 Nguồn gốc split 880/120 chưa đủ bằng chứng

Word P0363 viết hai danh sách do nhóm tác giả Kvasir-SEG cung cấp, dẫn Kaggle [3]. Các tệp local chỉ chứng minh danh sách thành viên. Bản giấy Kvasir-SEG, mục 4.2, trình bày thí nghiệm chia 80/10/10; điều này không chứng minh split 880/120 của dự án sai, cũng không phủ định khả năng tồn tại một release khác. Listing Kaggle đang lưu chỉ là một trang có `nextPageToken`, nên không thể suy từ đó rằng toàn release có hoặc không có train/val lists.

Phán quyết: **thiếu provenance**, không phải xác nhận rò rỉ dữ liệu hoặc gán sai toàn bộ tập. Cần release/version, URL hoặc snapshot có chính hai tệp và hash. Trước đó nên mô tả trung tính “đề tài sử dụng danh sách có sẵn 880/120” thay vì khẳng định nguồn tác giả. [Kvasir-SEG](https://arxiv.org/abs/1911.07069), [Kaggle được trích](https://www.kaggle.com/datasets/debeshjha1/kvasirseg).

### D-002 Hai bộ đánh số tài liệu không đồng nhất

TLTK `[20]` là PolyMamba, Word `[20]` là MambaPSA; TLTK `[21]` là SAM-Mamba, Word `[21]` là SAM-MaGuP. Đây là các công trình khác nhau. Sáu paper được Word trích có PDF cùng công trình trong 24 PDF gốc; PDF YOLO26 trong TLTK là nguồn nền liên quan cho citation tài liệu online [16], không phải cùng một hiện vật. Bốn paper gần đề tài còn lại đã có bản audit download.

Phán quyết: sai lệch **chỉ mục giữa hai bộ sưu tập**, không tự kết luận citation nội bộ Word sai. Dùng ID ổn định `CIT-xxx` và mapping tiêu đề/DOI; không sao chép số `[n]` giữa TLTK và báo cáo.

### D-003 Nên cân nhắc thêm PolyMamba

PolyMamba đã có trong TLTK-20 và được xác thực tại MICCAI 2025. Nó là đối chiếu phù hợp cho spatial prior và frequency guidance, bổ sung bối cảnh cho hướng thiết kế của TSVM. Đây là đề xuất coverage, không phải bằng chứng báo cáo hiện tại không đủ điều kiện học thuật. [Nguồn MICCAI](https://papers.miccai.org/miccai-2025/0704-Paper3872.html).

### D-004 Hỗ trợ fulltext còn giới hạn ở hai mục

Sách Gonzalez/Woods ấn bản 4 năm 2018 xác nhận metadata qua website tác giả; mục morphology được liệt kê nhưng chưa có fulltext hợp pháp trong TLTK để kiểm trang/công thức chính xác. Suzuki/Abe xác nhận được DOI, tác giả, năm và trang qua primary metadata; publisher fulltext trả403. Không đánh dấu hai nguồn này là giả. Có thể bổ sung locator sách và OpenCV API/source cho thao tác cụ thể. [Trang sách của tác giả](https://www.imageprocessingplace.com/DIP-4E/dip4e_main_page.htm), [DOI Suzuki/Abe](https://doi.org/10.1016/0734-189X(85)90016-7).

## Bảng 5.8 trong Word

| Dòng Word | Bằng chứng PDF | Kết quả kiểm |
|---|---|---|
| T17R002 Polyp-Mamba | Table 1, trang 6: Dice 0,940; IoU 0,881. Cùng trang ghi train 900 Kvasir + 550 ClinicDB; input 224 | Khớp |
| T17R003 Topo-VM-UNetV2 | Table I, trang 5: 91,95% và 86,54%; phần thực nghiệm ghi 900+550, input 256 | Khớp sau chuyển % sang 0–1 |
| T17R004 CSG-Mamba | Table 1, trang 9: Dice 0,9220; mIoU 0,8677; phần 4 ghi 800/100/100, input 256 và 3 seed | Khớp |

Đây là số tác giả công bố, không phải nhóm đã tái huấn luyện. Task, mask evaluation và split khác BG20; không so trực tiếp với mask AP của đề tài. Nguồn: [MICCAI Polyp-Mamba](https://papers.miccai.org/miccai-2024/paper/0697_paper.pdf), [Topo-VM-UNetV2](https://arxiv.org/abs/2505.06210), [CSG-Mamba](https://arxiv.org/abs/2608.14146).

## Công trình gần và phạm vi tính mới

MambaPSA là đối chiếu gần nhất về thay C2PSA cuối backbone YOLO26; bài thử phát hiện trên VOC. CSG-Mamba gần về convolutional bottleneck gate. Topo-VM-UNetV2 dùng persistent homology, khác guidance convolution của TSVM. Word hiện đã phân biệt những điều này đúng hướng. Phạm vi đóng góp có thể bảo vệ là thiết kế cụ thể và thực nghiệm của dự án, với giới hạn ablation/topology đã khai báo; không suy ra novelty tuyệt đối từ kết quả tìm kiếm. [MambaPSA](https://arxiv.org/abs/2607.12681).

Danh sách bổ sung trong `suggested_references.md` ưu tiên nguồn có vai trò rõ ràng. Các đầu mối mới chỉ đọc abstract được gắn nhãn partial; chưa đưa số hiệu năng chưa kiểm vào bảng.

## Rà soát trích dẫn và Turnitin

Đã chạy một phép sàng lọc hẹp, tái lập được: **462 block nội dung** trước danh mục tham khảo, so với **28 text nguồn**, tìm chuỗi liên tiếp **12 token chuẩn hóa giống hệt**. Không tìm thấy cặp block–nguồn thỏa điều kiện. Phương pháp loại phần P0733 trở đi nhưng vẫn giữ các bảng; manifest phạm vi ở `local_overlap_scope.json`.

Kết quả **không phải 0% trùng lặp**, không xác nhận báo cáo không đạo văn và không dự đoán tỷ lệ Turnitin. Nguồn phần lớn tiếng Anh, báo cáo tiếng Việt; phép kiểm không phát hiện dịch sát, diễn giải sát, nguồn ngoài kho, bài nộp trước hoặc tự trùng. Cần đọc ngữ nghĩa và báo cáo Turnitin của đúng file, đúng thiết lập trường. Không thực hiện upload.

Các đoạn Word về công trình gần đều có citation và diễn giải phân biệt thiết kế. Không phát hiện đoạn nguyên văn dài trong phạm vi sàng lọc hẹp; không suy rộng kết quả sang toàn bộ cơ sở dữ liệu Turnitin hoặc chỉ báo AI writing.

## Trạng thái bàn giao

Phòng C có thể đóng bước xác thực metadata của 23 mục; CIT-003 vẫn cần provenance. Bảng T17 ba dòng khớp nguồn. D-001/D-004 là thiếu bằng chứng, D-002 là chỉ mục cần quản lý, D-003 là đề xuất mở rộng. D-005 giữ nguyên **chưa đánh giá Turnitin**. Root cần tổng kiểm chéo một nguồn/bảng; không dùng kết quả D để chứng thực code, checkpoint hoặc phần mềm đã chạy.

Giữ nguyên mọi nguồn gốc. Mọi chỉnh sửa câu chữ, nguồn tham khảo hoặc manifest là bước sau kiểm toán.
