# Tuyển chọn và bổ sung tài liệu tham khảo

Ngày rà soát: 12/10/2026.

## Phạm vi đã chốt với nhóm

- Web cuối dự kiến triển khai **YOLO26s-seg + TSVM**, đang huấn luyện lại. Đây là mục tiêu triển khai đã được người dùng xác nhận, chưa phải bằng chứng mô hình mới đã được tích hợp và chạy trong web hiện tại.
- Phần huấn luyện và kết quả tiếp tục chờ đợt chạy mới sau sự cố checkpoint FP16 ở tài liệu 27. Lần cập nhật này chỉ tuyển chọn và bổ sung tài liệu tham khảo.
- Bộ 24 PDF trong thư mục `DeepLearning/TLTK` do nhóm tự tuyển chọn, không phải danh sách bắt buộc của giảng viên. Không cần đưa cả 24 bài vào báo cáo.
- Không xóa hoặc thay đổi PDF gốc. “Đọc thêm” trong bảng dưới nghĩa là chưa cần đưa vào danh mục nộp nếu nội dung báo cáo không sử dụng bài đó.

## Cách đọc bảng

`TLTK` là số trong manifest của thư mục tài liệu gốc; `BC` là số trong `md viet bao cao/08_TAI_LIEU_THAM_KHAO.md`. Hai hệ thống số khác nhau, không chép trực tiếp số TLTK thành trích dẫn trong chương.

Danh mục 08 hiện là **danh mục làm việc gồm 31 nguồn**, giữ số cũ [1]–[15] và thêm [16]–[31]. Số lượng này không phải yêu cầu về độ dài báo cáo. Khi hoàn thiện, chỉ giữ nguồn đã trích dẫn, rồi đánh số lại theo thứ tự xuất hiện và đồng bộ toàn bộ chương/phụ lục.

## Tuyển chọn 24 tài liệu nhóm đã có

| TLTK | Tài liệu | Đề xuất | BC | Lý do và vị trí sử dụng |
|---:|---|---|---|---|
| 1 | Kvasir-SEG | Giữ | [1] | Nguồn chính cho 1.000 ảnh polyp và mask; chương dữ liệu. |
| 2 | A Benchmark for Endoluminal Scene Segmentation… | Có điều kiện | — | Chỉ cần nếu mô tả bộ dữ liệu/benchmark tương ứng hoặc hướng đánh giá mở rộng; hiện chưa có kết quả liên bộ dữ liệu được xác minh. |
| 3 | A multi-centre polyp detection and segmentation dataset… | Có điều kiện | — | Dùng khi giới thiệu hoặc thực nghiệm trên dữ liệu đa trung tâm; không đưa vào để ngụ ý nhóm đã dùng bộ dữ liệu này. |
| 4 | Survey của Mei et al. | Giữ | [16] | Tổ chức tổng quan CNN, Transformer, Mamba và các khó khăn phân đoạn polyp; vẫn trích bài gốc khi trình bày từng phương pháp. |
| 5 | U-Net | Giữ | [9] | Nền tảng encoder–decoder trong tổng quan. |
| 6 | U-Net++ | Đọc thêm | — | Chỉ thêm nếu có đoạn phân tích skip connection lồng nhau; không cần kéo dài tổng quan bằng danh sách mô hình. |
| 7 | PraNet | Giữ | [10] | Công trình polyp có liên quan trực tiếp, đã xuất hiện trong bản thảo. |
| 8 | Polyp-PVT | Giữ | [12] | Đại diện hướng Transformer; ưu tiên bản xuất bản 2023, phân biệt với preprint 2021. |
| 9 | ColonFormer | Giữ | [31] | Bản thảo đã nhắc đến nhưng danh mục cũ thiếu mục tương ứng. |
| 10 | TransFuse | Đọc thêm | — | Chỉ cần nếu phân tích riêng việc kết hợp CNN–Transformer; không phải kiến trúc TSVM của nhóm. |
| 11 | You Only Look Once | Đọc thêm | — | Có thể thêm nếu viết lịch sử YOLO; nguồn [6], [7] sát mô hình đang dùng hơn. |
| 12 | Ultralytics YOLO26 | Giữ | [6] | Nền tảng YOLO26; cấu hình riêng YOLO26s-seg của nhóm phải đối chiếu YAML và mã nguồn. |
| 13 | S4 | Đọc thêm | — | Chỉ cần nếu trình bày sâu quá trình phát triển SSM trước Mamba; không bắt buộc cho mô tả TSVM. |
| 14 | Mamba | Giữ | [2] | Selective state space model; phân biệt bản arXiv 2023 với công bố COLM 2024. |
| 15 | VMamba | Giữ | [4] | Nguồn cho visual state space và SS2D; không đồng nhất với Vision Mamba/Vim [3]. |
| 16 | U-Mamba | Đọc thêm | — | Có thể chọn làm một ví dụ Mamba trong phân đoạn y khoa nếu tổng quan cần mở rộng. |
| 17 | Mamba-UNet | Đọc thêm | — | Tránh lặp vai trò với U-Mamba/Swin-UMamba khi không phân tích khác biệt. |
| 18 | Swin-UMamba | Đọc thêm | — | Phù hợp nếu bàn về tiền huấn luyện; không dùng để khẳng định nhóm có cùng quy trình pretraining. |
| 19 | Polyp-Mamba | Giữ | [5] | Công trình Mamba cho polyp; giúp đặt phương pháp nhóm trong bối cảnh nghiên cứu. |
| 20 | PolyMamba | Giữ | [18] | Liên quan prior không gian và biên/tần số; dùng để so sánh ý tưởng, không coi module của bài là module nhóm đã cài. |
| 21 | SAM-Mamba | Đọc thêm | — | Phù hợp hướng phát triển SAM/zero-shot nếu thực sự có phần thảo luận; không thuộc pipeline YOLO26s + TSVM hiện tại. |
| 22 | Mamba YOLO | Giữ | [17] | Có nghiên cứu kết hợp Mamba và YOLO trước đó; tránh tuyên bố nhóm là công trình đầu tiên tích hợp hai hướng này. |
| 23 | Feature Pyramid Networks | Giữ | [19] | Cơ sở tổng hợp đặc trưng đa tỉ lệ; không có nghĩa neck của nhóm giống nguyên bản FPN. |
| 24 | EfficientDet | Đọc thêm | — | Chỉ cần nếu phân tích BiFPN/EfficientDet. Chưa có căn cứ coi BiFPN là thành phần đang dùng trong TSVM. |

Kết quả tuyển chọn: **13 nguồn nên giữ**, **2 nguồn có điều kiện**, **9 nguồn đọc thêm** trong bộ 24 tài liệu. Đây là lựa chọn theo nội dung dự án, không phải đánh giá chất lượng khoa học của những bài được để lại.

## Nguồn cần bổ sung hoặc giữ ngoài bộ 24 PDF

| Nội dung trong báo cáo | Nguồn BC | Cách sử dụng |
|---|---|---|
| Nguồn ảnh nền | [14] Kvasir đa lớp | Phân biệt với Kvasir-SEG [1]. Nếu ảnh nền lấy từ normal-cecum, nêu rõ lớp nguồn và cách tuyển chọn, không gọi đó là mask âm do Kvasir-SEG cung cấp. |
| Xử lý mask bằng ngưỡng Otsu | [21], [24] | Bài Otsu là cơ sở thuật toán; OpenCV giải thích API thực thi. |
| Closing, contour và xấp xỉ polygon | [22]–[24] | Suzuki–Abe cho truy vết biên, Douglas–Peucker cho xấp xỉ; closing dẫn tài liệu OpenCV. Các tham số 3×3, min-area 20, epsilon 0,002 phải dẫn script của nhóm. |
| Định dạng YOLO segmentation | [25] | Giải thích một dòng cho một đối tượng, tọa độ polygon chuẩn hóa. Số ảnh, số đối tượng, nhãn rỗng phải dựa vào dữ liệu thật. |
| Tăng cường dữ liệu | [26] | Giải thích ý nghĩa tham số. Chỉ mô tả phép tăng cường đã bật trong cấu hình chạy tương ứng; tài liệu không chứng minh nhóm đã dùng tất cả phép biến đổi. |
| Neck đa tỉ lệ/bottom-up | [19], [20] | FPN và PANet làm nền tảng lý thuyết; YAML và mã nguồn quyết định mô tả kiến trúc cụ thể. |
| Prototype mask của instance segmentation | [13] YOLACT | Giữ nếu chương phương pháp giải thích prototype/coefficient; kiểm tra head của fork trước khi khẳng định chi tiết tương đương YOLACT. |
| FastAPI nhận ảnh suy luận | [27] | Nguồn cho tải tệp multipart. Route, trường JSON, xử lý lỗi phải dẫn mã `ai-service` của nhóm. |
| Backend Spring Boot | [28] | Nền tảng ứng dụng; phiên bản dùng lấy từ `pom.xml`, không lấy phiên bản mới nhất của trang docs. |
| Lưu dữ liệu MongoDB | [29] | Cơ sở mô hình document; collection/schema/lịch sử suy luận phải đối chiếu code nhóm. |
| Ứng dụng Flutter | [30] | Chỉ giữ nếu Flutter nằm trong phạm vi báo cáo cuối; nếu báo cáo chỉ trình bày web, chuyển sang phụ lục hoặc bỏ nguồn này. |
| HarDNet-MSEG | [11] | Đã có trong tổng quan; sửa mã arXiv thành 2101.07172. Không lấy FPS của bài làm tốc độ hệ thống của nhóm. |
| Vision Mamba/Vim | [3] | Giữ nếu cần phân biệt Vim với VMamba. Nếu không có đoạn sử dụng thì có thể bỏ để gọn. |
| CVC-ClinicDB/WM-DOVA | [15] | Chỉ giữ nếu thực sự giới thiệu dữ liệu này hoặc nội dung bài. Không tạo bảng kết quả trên ClinicDB khi nhóm chưa chạy. |

Các bài đã có trong thư mục TLTK nhưng thiếu ở danh mục báo cáo cũ được thêm vào 08 là survey [16], Mamba YOLO [17], PolyMamba [18], FPN [19] và ColonFormer [31]. Các mục [20]–[30] bổ sung cơ sở xử lý ảnh, neck, định dạng dữ liệu và công nghệ ứng dụng. Không cần tải lại tất cả PDF để có thể trích dẫn DOI hoặc tài liệu chính thức.

## Gợi ý gắn nguồn vào các phần đang hoàn thiện

| Phần | Nhóm nguồn phù hợp | Bằng chứng nội bộ cần đi kèm |
|---|---|---|
| Tổng quan polyp và nghiên cứu liên quan | [9]–[12], [16]–[18], [31] | Tách số liệu công bố của tác giả khác khỏi kết quả của nhóm. |
| Cơ sở YOLO26, Mamba và TSVM | [2]–[7], [13], [19], [20] | YAML, lớp TSVM và mã head/loss của fork. TSVM là cấu hình/cải tiến của nhóm, không phải tên module nguyên gốc từ bài VMamba. |
| Nguồn dữ liệu và BG20 | [1], [8], [14], [25] | Kvasir-SEG: 1.000 ảnh; 200 ảnh nền được nhóm bổ sung. BG20 là 200/1.000, không phải 20% tổng 1.200 ảnh. Train/val phải trình bày đúng số đã kiểm kê. |
| Tiền xử lý | [21]–[25] | `convert_kvasir_with_background_to_yolo_seg.py`: Otsu → closing → contour ngoài → lọc diện tích → polygon → chuẩn hóa. Không ghi resize/augmentation offline nếu script không thực hiện. |
| Thiết kế và triển khai web | [7], [27]–[29] | Sơ đồ Spring Boot–FastAPI–MongoDB, route, schema, màn hình và kiểm thử thực tế. Mô hình đích là YOLO26s + TSVM, chờ checkpoint mới và kiểm chứng tích hợp. |
| Mobile nếu giữ trong phạm vi | [30] | Mã Flutter, API thực tế và ảnh giao diện; không tự coi mobile là phần đã kiểm thử hoàn chỉnh. |

Chưa chèn hoặc đánh số lại trích dẫn trong các chương ở lần cập nhật này. Chưa hoàn thiện phần huấn luyện, kết quả hay kết luận về ưu thế của TSVM.

## Kiểm chứng nguồn và giới hạn

- Đã kiểm kê manifest, tên tệp và thông tin trong DOCX danh mục của thư mục TLTK; **chưa đọc toàn văn cả 24 PDF**. Việc phân nhóm dựa trên nội dung dự án đã rà soát, metadata và abstract/tài liệu chính thức có liên quan.
- Đã đối chiếu các nguồn bổ sung với trang nhà xuất bản/hội nghị, arXiv của tác giả hoặc tài liệu chính thức. Một số trang DOI bị chặn hoặc lỗi truy cập; không khẳng định mọi liên kết đều đã mở toàn văn thành công.
- Mamba: công bố COLM 2024 được đối chiếu [danh sách nhận bài chính thức của hội nghị](https://github.com/COLM-org/COLM2024/blob/main/AcceptedPapers.html); arXiv phát hành lần đầu tháng 12/2023.
- PolyMamba: dùng năm 2025 theo [BibTeX MICCAI chính thức](https://papers.miccai.org/miccai-2025/0704-Paper3872.html), không tự đổi sang 2026 theo tên tệp/ghi chú khác. Polyp-Mamba [5] và PolyMamba [18] là hai bài khác nhau.
- Mamba YOLO [17]: dùng tên bản AAAI “A Simple Baseline for Object Detection with State Space Model” theo [bản hội nghị](https://ojs.aaai.org/index.php/AAAI/article/download/32885/35040), tránh trộn tên bản tiền công bố “SSMs-Based YOLO…” với metadata hội nghị.
- Trang Kvasir-SEG [8] chưa truy cập lại thành công; giữ liên kết với ghi chú và dùng bài [1] làm nguồn chính. DOI Kvasir đa lớp [14] có trong metadata nguồn dữ liệu; trang ACM chưa mở được toàn văn.
- Tài liệu OpenCV hỗ trợ chi tiết thực thi: [Otsu/thresholding](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html), [morphology/closing](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html), [contour và approxPolyDP](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html). Phiên bản trang hiện hành có thể khác thư viện nhóm đã cài.
- Ngày truy cập 12/10/2026 chỉ ghi cho các trang tài liệu đã truy cập trong đợt rà soát này; bỏ ngày truy cập cũ chưa được xác minh của bản thảo.
- Trước khi nộp: bỏ ghi chú biên tập khỏi danh mục 08, loại nguồn không trích dẫn, kiểm tra lại metadata từ PDF/BibTeX của từng bài được sử dụng sâu và đồng bộ số trích dẫn. Không dùng chỉ riêng abstract để viết phân tích chi tiết kiến trúc hoặc kết luận thực nghiệm.
