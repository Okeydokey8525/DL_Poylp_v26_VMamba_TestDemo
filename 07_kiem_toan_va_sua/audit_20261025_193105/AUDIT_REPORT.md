		`

# Kiểm toán kết quả TSVM FP32 và PolypVision

Đợt kiểm toán bắt đầu ngày 25/10/2026. Trạng thái: **HOÀN TẤT PHẠM VI ĐÃ KHAI BÁO**. Đây là báo cáo kiểm toán, không phải bản sửa luận văn hoặc mã nguồn.

Bản đối chiếu chính: [CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx>). SHA-256: `2caaf8b42c299f3c73a0087654f8f7d3c2986a83b8878d713613e0c9e1ed0856`.

## Kết luận tổng kiểm

Các phép tổng hợp thống kê chính của bộ 20 seed FP32 **khớp dữ liệu đang lưu**. Chưa phát hiện sai số số học trong 36 CSV đã kiểm; các con số chính trong Word khớp CSV. Có lỗi thật trong mô tả Word, tài liệu legacy, khả năng tái lập cục bộ và ứng dụng Web. Không thể đánh dấu toàn dự án là hoàn toàn đạt chỉ từ kết quả thống kê hoặc test unit pass.

Phán quyết phải tách bốn lớp: **nguồn hiện vật**, **phép tính**, **hình thể hiện**, **câu diễn giải/chạy thực tế**. CSV nhất quán không tự chứng minh nguồn phiên Kaggle; cùng hash không phải chứng nhận độc lập lịch sử huấn luyện. Không có bằng chứng từ cuộc kiểm toán này để cáo buộc giả số liệu.

## Phạm vi và kiểm tra chéo

| Phòng      | Phần đã thực hiện                                                                                                                                 | Bằng chứng chi tiết                                                                                                                                                      |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A           | 40 CSV gốc,36 CSV dẫn xuất/benchmark,13 metric,epoch/statistics và lineage 10/21/20 seed                                                           | [A_numeric/report.md](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/A_numeric/report.md>)                                             |
| B           | 46 hình gói,400 ảnh đường cong/CM,33 ảnh nhúng Word;35 PNG mới pixel-identical; mẫu 10 cặp GT/pred                                          | [B_visual/report.md](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/B_visual/report.md>)                                               |
| C           | 783 đoạn,19 bảng,24 mục tham khảo;357 ô thống kê/epoch/timing;1.240 trường cấu hình                                                        | [C_report/report.md](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/C_report/report.md>)                                               |
| D           | 24 mục tham khảo Word,24 PDF TLTK,4 PDF tải công khai;10 công trình liên quan                                                                   | [D_literature/report.md](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/D_literature/report.md>)                                       |
| E           | Build/test cách ly; Web/FastAPI/Mongo thật, browser, inference, ownership/export/delete/persistence và AI-off                                       | [E_application/report.md](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/E_application/report.md>)                                     |
| Tổng kiểm | Tính lại t/CI bằng thư viện chuẩn; dataset/1.000 mask;40 checkpoint dtype/metadata;AP tái đánh giá; kiểm nguồn/screenshot/paper độc lập | [root/checkpoint_revalidation_summary.json](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/root/checkpoint_revalidation_summary.json>) |

Số phép kiểm ô là phạm vi công việc, không phải số thí nghiệm độc lập hay xác suất không còn lỗi. 357 ô Word là nhóm thống kê/epoch/timing; không có nghĩa mọi con số Word đều đúng (Bảng 2.1 có lỗi P4).

Các phòng kiểm lần đầu độc lập, sau đó trao đổi chứng cứ. Tổng kiểm đã tự kiểm P4 từ checkpoint, log maskCount và suy luận Web, mã/source và screenshot badge/kích thước, pipeline Mongo lồng facet, bảng Polyp-Mamba từ ảnh PDF và các nguồn primary gần đề tài. Các alias cùng lỗi (C-002/E-006/B-C002) được gộp, không đếm thành ba lỗi.

Hai phòng bị gián đoạn giới hạn sử dụng và được tiếp tục từ đầu ra đã lưu; các nhiệm vụ còn thiếu không bị đánh dấu hoàn tất chỉ vì đã có file trung gian.

## Kết quả thống kê gốc

| Quy tắc                            | Baseline maskAP mean ± SD mẫu |            TSVM FP32 |        Δ | paired t p |
| ----------------------------------- | ------------------------------: | -------------------: | --------: | ---------: |
| Cực đại maskAP từng run         |            0,718868 ± 0,011768 | 0,723171 ± 0,007197 | +0,004303 |   0,061431 |
| Cực đại fitness box+mask từ CSV |            0,717397 ± 0,012877 | 0,722199 ± 0,007527 | +0,004802 |   0,061898 |

Endpoint chính trong Word là hàng đầu. CI 95% của Δ=[−0,000228;0,008834], chứa 0; TSVM cao hơn 13/20 cặp và SD mẫu thấp hơn khoảng 38,85%. Chưa đủ bằng chứng ưu thế trung bình tại α = 0,05. Có 16/40 run khác epoch giữa hai quy tắc. Không đổi endpoint sau khi xem p. Tất cả seed dùng cùng validation đã tham gia chọn epoch; chưa phải patient-disjoint/external test.

Lineage được kiểm: 240 ô metric 10 seed khớp nguồn;20 seed TSVM cũ/FP32 có 44.000 ô non-time giống và 2.000 ô time khác. Điều này có thể phù hợp rerun tất định khi bản vá chỉ đổi lưu checkpoint; cần log phiên để chứng thực lịch sử, không suy từ đó là gian lận.

## Kiểm checkpoint và đánh giá lại

40/40 best.pt đọc được:20 Baseline lưu tensor float16,20 TSVM lưu float32, không có tensor không hữu hạn. Seed và tên run trong 40 checkpoint đều khớp thư mục; embedded train_results khớp CSV gốc trong phạm vi được lưu. Metadata nhất quán vẫn không tự chứng minh mọi thao tác lịch sử ngoài máy.

Dataset validation được sao chép vào vùng kiểm toán để tránh ghi cache lên nguồn. 320 tệp ảnh/nhãn của bản sao khớp byte với nguồn. Tái đánh giá dùng research fork 8.4.127 đã vá, PyTorch 2.6.0+cpu, batch 16,rect=True,imgsz 640,half=False,workers 0. Đây là cách batching/resize tương ứng validator trong train, khác phép probe squarebatch 4 ban đầu.

| Model    | Đã tái đánh giá | MaskAP checkpoint mean ± SD | Max absΔAP với CSVfitness | Run có absΔmaskP>0,005 | Run có absΔmaskR>0,005 |
| -------- | --------------------: | ---------------------------: | --------------------------: | -----------------------: | -----------------------: |
| Baseline |                 20/20 |         0.717181 ± 0.012831 |                  0.00148228 |                       10 |                        8 |
| TSVM     |                 20/20 |         0.722201 ± 0.007528 |                  0.00005074 |                        0 |                        0 |

Ngưỡng 0,005 là tiêu chí đối chiếu AP đã khai báo, không phải chứng minh mọi metric giống chính xác. P/R của một số Baseline khác rõ hơn AP; bảng mọi sai khác được giữ tại [root/checkpoint_all_metric_comparison.csv](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/root/checkpoint_all_metric_comparison.csv>). Không quy nguyên nhân chắc chắn cho FP16, backend hoặc điểm F1 nếu chưa có thí nghiệm cô lập. TSVM được đối chiếu riêng; không dùng PASS AP che sai khác P/R.

Đối chiếu phụ trên best.pt tái đánh giá: Δ mask AP=0.005021, paired t p=0.051233, CI 95%=[-0.000030; 0.010071]. Đây là phân tích kiểm chứng phụ, không thay endpoint max-mask ban đầu và không phải test ngoài.

**Hiệu chỉnh phương pháp của chính kiểm toán:** probe đầu rect=False,batch 4 trên Baseline 0 cho AP lệch khoảng−0,00949; sau đối chiếu source và dùng rect=True,batch 16, lệch còn−0,00124. Probe khác giao thức không được tính là lỗi checkpoint. Trường `threads=4` trong JSONL gốc là giá trị yêu cầu trước validator; CPU `select_device` đặt lại 8, đã kiểm ở [root/thread_protocol_verification.json](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/root/thread_protocol_verification.json>). Không dùng timing các lượt này làm benchmark vì còn tải cạnh tranh. Log gốc được giữ, không sửa cho đẹp.

## Dataset và tiền xử lý

Đã kiểm 1.040 ảnh train/1.040 nhãn (160 rỗng,936 instances),160 ảnh val/160 nhãn (40 rỗng,127 instances). Không thiếu/orphanlabel, mọi nhãn class 0, ít nhất 3 đỉnh và tọa độ hữu hạn trong [0,1]; không trùng ảnh hoàn toàn giữa train/val qua SHA-256. Không có metadata bệnh nhân nên không chứng minh patient-disjoint hoặc không có near-duplicates.

Tái tạo 1.000 mask trong bộ nhớ cho Otsu 5–8,1.206 contour,loại 143,giữ 1.063; vertices mean 333,1552→24,6369,range 10–80. Cả 200 ảnh nền chọn seed 42 khớp danh sách và byte ảnh. Có 999 nhãn khớp từng ký tự; một nhãn val khác một đỉnh khoảng 3 px với OpenCV 4.12.0/numpy 2.2.6. Phòng B tái hiện bằng chính hàm builder:27 pixel raster khác, polygon-pair IoU 0,99981118. Đây là khác biệt tái lập nhỏ trong môi trường thử, không chứng minh nhãn bị hỏng và không sửa nhãn trong cuộc kiểm toán. Xem [root/preprocessing_independent.json](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/root/preprocessing_independent.json>) và [B_visual/dataset_label_crosscheck.json](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/B_visual/dataset_label_crosscheck.json>).

## Hình ảnh

27 hình kết quả mới và 8 hình benchmark tái tạo giống từng pixel trong môi trường tái sinh. Phòng A kiểm dữ liệu độc lập để không dùng việc chạy lại cùng script làm chứng nhận duy nhất về số học. 40 CM đếm và 40 CM chuẩn hóa có 240 ô số khớp và 80 ô TN trống. 80 PR có legend AP50 lệch fitness-log tối đa 0,00125; digitization chỉ là xấp xỉ, không thay prediction arrays.

33/33 image occurrences Word truy được nguồn;560 ô số nguồn hình riêng Word và 88.000 giá trị non-time đường cong cached khớp raw/A. Chưa nghiệm thu toàn bộ 97 trang render Word; hash media khớp không bảo đảm mọi chi tiết bố cục trang không bị crop.

11 hình legacy khác pixel khi tái sinh, chưa đủ căn cứ gọi sai số liệu. Hai hình legacy dùng SD tổng thể(ddof0) khác SD mẫu(ddof1) của gói mới. Mẫu10 cặp GT/pred của hai model seeds 0,5,8,18,19 dùng cùng 16 tile; đã thấy false-alarm/missing-overlay examples thông thường. Mẫu không chứng minh ưu thế tổng thể, không đếm thành 160 ảnh độc lập và không chứng nhận ngưỡng JPEG khi thiếu metadata.

## Báo cáo và ứng dụng

Word mới nhìn chung dùng đúng 20 cặp, gate 1+G, FFN 1×1, tensor work O(LlogL), quy tắc epoch và giới hạn topology/Dice. Tuy nhiên phải sửa Bảng 2.1 P4=256, ví dụ TSVM 2 mask, và ràng buộc câu 1.000 nhãn exact-match theo bằng chứng môi trường. Tài liệu Markdown cũ có các phát biểu không còn hợp lệ; không dùng chúng để sinh lại Word trước khi đồng bộ.

Web khởi động và suy luận thật được; 51 pytest và 261 Java test pass không phát hiện pipeline Mongo thật bị cấm. Lịch sử so sánh đang lỗi; registry/inference thật vẫn đúng cặp S. Badge sai là lỗi view, không phải chứng minh nạp nhầm mô hình. Các server kiểm toán đã được dừng, dữ liệu kiểm thử riêng được giữ. Mobile chỉ đọc nguồn, chưa chạy hoặc xác nhận lại 498 test. Xem toàn bộ test/screenshot/cleanup tại [E_application/report.md](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/E_application/report.md>).

## Tài liệu, tính mới và Turnitin

24 mụcWord đã được đối chiếu:23 metadata xác nhận; trangKaggle tồn tại nhưng chưa chứng minh tác giả phát hành split 880/120. Ba dòngBảng 5.8 khớp bảngPDF gốc và giao thức; không dùngDice/IoU của paper để xếp hạng trực tiếp với AP BG20.

Đã lập ma trận 10 công trình gần. [MambaPSA](https://arxiv.org/abs/2607.12681) rất gần về thay C2PSA trong YOLO26; [PolyMamba](https://papers.miccai.org/miccai-2025/0704-Paper3872.html) là nguồn phù hợp spatial-prior/frequencyguidance đã có trongTLTK. Đóng góp phải mô tả ở thiết kế và thí nghiệm cụ thể; không khẳng định đầu tiên tuyệt đối. TLTK vàWord đánh số khác nhau, không copy số[n] giữa hai danh mục. Đề xuất có mục đích trong [D_literature/suggested_references.md](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/D_literature/suggested_references.md>).

Chưa có báo cáoTurnitin hoặc thiết lập trường/lịch sử nộp. Sàng lọc chuỗi khớp chính xác cục bộ không phát hiện dịch sát hoặc nguồn ngoài kho và **không quy đổi được thành phần trămTurnitin**. Không kết luận đạt ngưỡng 30%, không upload lên dịch vụ ngoài, không có đánh giáAI-writing.

## Danh sách cần xử lý

CSV đầy đủ (gồm mức chắc chắn,nguyên nhân và khắc phục): [ISSUES.csv](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/ISSUES.csv>).

| ID          | Mức   | Khu vực                                 | Phát hiện                                                                    |
| ----------- | ------ | ---------------------------------------- | ------------------------------------------------------------------------------ |
| E-004       | high   | Web /comparisons và /api/v1/comparisons | HTML503/API500; Mongo40600 vì $facet lồng $facet                             |
| E-002       | medium | Web trang kết quả TSVM                 | Tên TSVM nhưng badge BASELINE                                                |
| E-003       | medium | Web kích thước ảnh                   | Ảnh621×530 bị hiển thị1280×720                                           |
| C-001       | medium | Word Bảng 2.1 hàng Backbone P4         | 512 kênh; thực tế256 sau scale s                                            |
| C-002       | medium | Word mục4.6 ví dụ polyp               | Viết cả hai trả1 mask; thực tế Baseline1,TSVM2                            |
| C-003/C-004 | medium | Tái lập local/BG20 và phụ lụcA      | Path local không tồn tại; phụ lục thiếu builder bổ sung ảnh nền       |
| C-005       | high   | Bản thảo Markdown báo cáo            | Còn10 seed,SGD,TN suy diễn,Dice/GPU speed chưa đo; khác Word mới         |
| C-006       | medium | Markdown kiến trúc                     | Gate G thay1+G; FFN3×3/GELU thay hai1×1; complexity không khớp triển khai |
| C-007       | medium | Điểm vào tài liệu hiện trạng      | Ưu tiên10 seed/CM cũ trong khi bộ hiện tại20 seed FP32                   |
| A-01/A-02   | medium | Legacy TN trong gói20 seed              | TN_reconstructed=40−FP đối tượng không phải TN ảnh                     |
| A-03        | medium | Legacy bảng thắng/thua loss            | tsvm_wins6 theo chiều tăng; lower-is-better đúng14                         |
| D-001/C-008 | medium | Nguồn gốc split 880/120                | Chưa chứng minh hai danh sách do nhóm tác giả dataset phát hành        |

Các mục informational/thiếu bằng chứng trong CSV không được đếm chung thành lỗi đã xác nhận. Một lỗi được nhiều phòng tìm thấy đã được gộp alias.

## Thứ tự khắc phục đề xuất sau kiểm toán

1. Sửa lịch sử so sánh và test lại trênMongo thật; giữ kiểm ownership/pagination/filter.
2. Đồng nhất model identity trên UI, lưu kích thước thật và sửa mô tả Nano.
3. Sửa các câu/bảng Word được xác nhận sai, giữ kết luận thống kê có điều kiện; không chỉnh số để tạo p<0,05.
4. Sửa hướng dẫn local/BG20 và phân nhãn Markdown/legacyTN/winloss; giữ raw để truy vết.
5. Bổ sung provenance split và mapping tài liệu; lấy báo cáoTurnitin chính thức trước khi kết luận ngưỡng.

Không áp dụng các sửa đổi trên trong cuộc kiểm toán. Không train lại, không sửa checkpoint hoặc dữ liệu nguồn.

## Tính toàn vẹn và giới hạn

Manifest gốc có5580 tệp; kiểm lại thấy0tệp thay đổi hoặc mất: [root/source_after_check.json](<C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/audit_20261025_193105/root/source_after_check.json>). Riêng phòngE kiểm174 srcfiles không đổi. Bằng chứng mới nằm trong thư mục kiểm toán; không có nghĩa mọi tệp ngoài manifest đều đã được băm.

Chưa xác minh lại GPU lịch sử, patient-level leakage, test ngoài, đầy đủablation/topology, fullpageWordlayout, mobile runtime, mọi đường admin/load/production hoặc mọi ngưỡng CM từ prediction arrays. Những phần này không được ngầm ghi PASS. Báo cáo này hỗ trợ sửa sai và giới hạn phát biểu; không phải chứng nhận toàn bộ khóa luận đạt hay đã quaTurnitin.
