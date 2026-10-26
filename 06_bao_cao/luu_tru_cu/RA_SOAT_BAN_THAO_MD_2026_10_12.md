# Rà soát bản thảo báo cáo ngày 12/10/2026

## 1. Kết luận và phạm vi

**Các file Markdown đúng vai trò là bản thảo các phần/chương của báo cáo, nhưng chưa đủ chính xác để ghép vào bản Word nộp. Có thể giữ khung 5 chương; cần sửa nội dung kỹ thuật, số liệu, cách diễn giải và bằng chứng hình ảnh.** Các lỗi nghiêm trọng nhất nằm ở Chương 2, Chương 4, Chương 5, phần kết luận và hai file phụ lục.

Đã đọc 11 bản thảo `00`–`10` trong `md viet bao cao`; trích nội dung văn bản từ hai DOCX mẫu và tiền xử lý; đối chiếu với script chuyển dữ liệu, hai notebook Kaggle, YAML mô hình, module TSVM, loss, code lưu checkpoint, log CSV, args.yaml, bảng benchmark và các phần liên quan của mã ứng dụng trong `../Ung_Dung/polypweb`.

Phân biệt mức kiểm chứng:

- **Đã xác nhận trực tiếp:** số ảnh/nhãn/vùng polyp; thông số huấn luyện trong args; cấu trúc code; số cell notebook; trung bình và độ lệch chuẩn Mask mAP50-95 tính lại từ results.csv; sai khác giữa bản thảo và bảng nguồn.
- **Có tài liệu nguồn nhưng chưa chạy lại:** p-value trong bảng thống kê cũ, kết quả kiểm toán 694 phép kiểm, benchmark thời gian và chẩn đoán biên độ/hiệu chỉnh BN trong tài liệu 27.
- **Chưa xác minh:** phiên bản trọng số đang được server ứng dụng thực sự sử dụng; thử nghiệm ngoại suy; tốc độ GPU; hiệu quả lâm sàng; số đo nguyên bản về sai số polygon dưới 0,5%.

Không huấn luyện lại, không sửa dữ liệu/log/trọng số, không chạy ứng dụng và không sửa mã ứng dụng. DOCX được đọc ở mức nội dung/OOXML, chưa render để đánh giá bố cục trang; biên bản này không xác nhận định dạng bản Word cuối cùng đạt chuẩn.

## 2. Cấu trúc và đối chiếu mẫu HUIT

Mẫu `Bieu mau do an_khoa luan. K.CNTT_HUIT_2025_V3.docx` cho phép đổi tên chương phù hợp tính chất đề tài. Vì vậy, không cần đổi cả báo cáo về tên “khảo sát/phân tích/thiết kế hệ thống” chỉ để giống ví dụ trong mẫu.

Khung đang dùng có thể giữ: mở đầu; tổng quan; phương pháp đề xuất; dữ liệu; cài đặt và ứng dụng; thực nghiệm; kết luận; tài liệu tham khảo; phụ lục. Mô hình ở Chương 2 được mô tả độc lập với dữ liệu ở Chương 3 nên cách sắp xếp này có thể chấp nhận.

Khi ghép Word phải áp dụng đúng quy định đã đọc từ mẫu:

- A4; Times New Roman; lề trái 3,5 cm, các lề còn lại 2,5 cm.
- Nội dung cỡ 13, canh đều, giãn dòng Multiple 1,3; Before/After 6 pt.
- Tên chương cỡ 18, đậm, in hoa, giữa; cấp 1.1 cỡ 14; cấp thấp hơn cỡ 13.
- Bảng cỡ 12; tiêu đề bảng phía trên, hình phía dưới; đánh số theo chương.
- Bìa không đánh số; phần đầu số La Mã; từ mở đầu số Ả Rập; số trang giữa phía dưới.
- Có mục lục chính tự động, danh mục hình/bảng tự động. File `00` hiện chưa có phần mục lục chính tương ứng.

Các trang nhận xét, dòng chuyên ngành, mã đề tài và thông tin bìa cần thống nhất với đề cương đã duyệt; mẫu không tự xác nhận các dữ kiện này. Không tự điền tháng nộp hoặc ghi đã hoàn tất những tuần chưa diễn ra.

## 3. Kết quả rà soát theo từng file

| File | Mức cần sửa | Nội dung chính |
|---|---|---|
| `00_TRANG_BIA_VA_DANH_MUC.md` | Vừa | Bổ sung mục lục chính; đồng bộ tên hình/bảng sau khi bỏ kết quả chưa có bằng chứng; xác nhận thông tin bìa; tránh hai bìa có nội dung hoàn toàn giống nhau. |
| `01_PHAN_MO_DAU.md` | Nhiều | Bỏ cam kết triệt tiêu FP, triển khai lâm sàng/thời gian thực và ngoại suy đã hoàn thành; dẫn nguồn số liệu y khoa; chốt phạm vi seed; xác nhận phân công và tiến độ. |
| `02_CHUONG_1_TONG_QUAN_VA_CO_SO_NGHIEN_CUU.md` | Nhiều | Phân biệt độ đo điểm ảnh/đối tượng; sửa mô tả anchor-free và 4 hướng SS2D; bỏ bảng FPS so sánh không cùng giao thức và tuyên bố chưa có nghiên cứu nào nếu chưa khảo sát đầy đủ. |
| `03_CHUONG_2_PHAN_TICH_VA_THIET_KE_MO_HINH_DE_XUAT.md` | Rất nhiều | Vẽ lại đúng C2TSVMamba với nhánh hình dạng, hướng, gate, concat, fuse, FFN và gamma; sửa DFL/L1; tách lý thuyết ZOH khỏi phép cập nhật trong code; bỏ LayerNorm không có trong fork gốc. |
| `04_CHUONG_3_XAY_DUNG_BO_DU_LIEU_VA_TIEN_XU_LY.md` | Nhiều | Dùng nội dung DOCX tiền xử lý làm nền rồi đối chiếu code; sửa tên script, JPG/Otsu/closing/20 pixel, BG20, chia tập, augmentation và giới hạn rò rỉ dữ liệu. |
| `05_CHUONG_4_CAI_DAT_THUAT_TOAN_VA_UNG_DUNG_MINH_HOA.md` | Rất nhiều | Thay bảng thông số; mô tả đúng notebook 3/4 cell chạy từng seed; viết đúng API, phiên bản Spring và khác biệt mô hình nghiên cứu–ứng dụng. |
| `06_CHUONG_5_THU_NGHIEM_VA_DANH_GIA_KET_QUA.md` | Rất nhiều | Thay bảng từng seed; sửa dòng Box; bỏ Dice/IoU suy từ P/R đối tượng và TN giả định; bỏ GPU/ngoại suy chưa có nguồn; phân biệt log FP32 với checkpoint FP16. |
| `07_KET_LUAN_VA_HUONG_PHAT_TRIEN.md` | Rất nhiều | Viết lại theo bằng chứng sau khi sửa Chương 5; bỏ hiệu quả lâm sàng, tính tái lập 100%, nhiệm vụ hoàn tất toàn bộ và lời hứa tối ưu FP16 khi chưa khắc phục vấn đề số học. |
| `08_TAI_LIEU_THAM_KHAO.md` | Vừa | Đã sửa mã arXiv HarDNet-MSEG; bổ sung trích dẫn tại đoạn sử dụng; thống nhất danh mục của DOCX dữ liệu với danh mục chung; còn cần kiểm toàn bộ metadata và đề cương “8 tài liệu bắt buộc”. |
| `09_PHU_LUC_A_B_C_D_SO_LIEU_THUC_NGHIEM.md` | Rất nhiều | Không gọi cấu hình SGD/AMP/batch16 là nguyên văn args; thay bảng B/C sai; báo đúng giới hạn của audit; không áp dụng dấu PASS của CSV sang toàn bộ bản thảo. |
| `10_PHU_LUC_E_F_G_H_BENCHMARK_NOTEBOOK_UNG_DUNG.md` | Rất nhiều | Bỏ GPU/VRAM chưa đo; thay notebook minh họa khác nguồn; sửa hướng dẫn theo ứng dụng; bỏ tự chấm 100%/xuất sắc; chuyển tuần tương lai về kế hoạch; đã bỏ thông tin đăng nhập. |

## 4. Các sai lệch phải sửa trước khi viết bản cuối

### 4.1. Số liệu thực nghiệm và giao thức chọn epoch

Tính lại trực tiếp từ 42 results.csv của hai mô hình, seed 0–20, chọn epoch có Mask mAP50-95 lớn nhất như script `archive/Stracth/Kiem_Tra/verify_10seed_audit.py`. Tất cả 42 file có 100 dòng epoch.

| Phạm vi | Baseline Mask mAP50-95, mean ± sample std | TSVM Mask mAP50-95, mean ± sample std |
|---|---:|---:|
| Seed 0–9, N=10 | 0,721029 ± 0,012854 | 0,724579 ± 0,007755 |
| Seed 0–20, N=21 | 0,718816 ± 0,011472 | 0,722939 ± 0,007095 |

Các giá trị tổng hợp này khớp tài liệu/bảng thống kê tương ứng. Nhưng bảng từng seed trong bản thảo không khớp nguồn. Ví dụ Baseline seed 3 phải là epoch 61, mAP 0,69411; bản thảo ghi epoch 87, mAP 0,7124. Baseline seed 1 phải là epoch 98, mAP 0,71649; bản thảo ghi 94 và 0,7185. TSVM seed 5 phải là epoch 90, mAP 0,72845; bản thảo ghi 95 và 0,7182.

Một số số tổng hợp cũng sai so với `Ket_Qua_V2/KQ_Nen_DX_10seed/02_statistics/mean_std/full_comparison_mean_std.csv`:

| Chỉ số, N=10 | Baseline đúng theo CSV | TSVM đúng theo CSV | p theo CSV, chưa chạy lại |
|---|---:|---:|---:|
| Box mAP50-95 | 0,726191 ± 0,019752 | 0,728522 ± 0,014100 | 0,7152 |
| Box mAP50 | 0,901050 ± 0,011645 | 0,900614 ± 0,009029 | 0,9334 |
| Val Box Loss | 0,723946 ± 0,043388 | 0,730508 ± 0,039871 | 0,7008 |
| Val Cls Loss | 0,559076 ± 0,063548 | 0,614813 ± 0,088354 | 0,0943 |
| Val L1 Loss | 0,016379 ± 0,001200 | 0,016212 ± 0,000886 | 0,6995 |
| Best Epoch | 87,3 ± 13,0983 | 91,7 ± 4,8546 | 0,3149 |

Bản thảo/Phụ lục B không được tiếp tục dùng các dòng 0,7482/0,7512, Val Box Loss 1,0215/0,9984 hoặc “Val DFL Loss” thay cho L1.

Với 10 seed, TSVM có Val Seg Loss thấp hơn ở **8 seed: 0,1,2,3,4,7,8,9**. Bản thảo liệt kê nhầm seed 6 thay seed 7. Theo CSV gốc, khoảng Mask mAP50-95 là Baseline 0,69411–0,73663; TSVM 0,70650–0,73385, khác cực trị trong bản thảo.

**Phải phân biệt:** epoch đạt Mask mAP lớn nhất dùng trong thống kê và epoch tạo `best.pt`. `SegmentMetrics.fitness` trong fork cộng fitness của box và segmentation; do đó không mặc định checkpoint tốt nhất nằm đúng dòng Mask mAP lớn nhất. Cần khai báo tiêu chí chọn epoch nhất quán khi so sánh CSV với checkpoint.

Nếu chốt 21 seed, phải cập nhật đồng thời các chương, bảng, hình, kiểm định và kết luận; không gắn nhãn N=21 lên bảng N=10. Tài liệu 26 ghi p=0,0599 cho Mask mAP50-95, vẫn trên 0,05. Không đổi ngưỡng alpha sau khi xem kết quả để tuyên bố thành công. Độ lệch chuẩn nhỏ hơn chỉ là quan sát mô tả khi chưa kiểm định chênh lệch phương sai.

### 4.2. Dice, IoU, ma trận nhầm lẫn và tính lâm sàng

`metrics/precision(M)` và `metrics/recall(M)` trong log là độ đo ghép dự đoán–đối tượng theo IoU mặt nạ. Tính `2PR/(P+R)` từ chúng cho F1 ở mức đối tượng, **không cho Dice điểm ảnh của mặt nạ**. Quan hệ Dice–IoU trong Chương 1 chỉ áp dụng khi TP/FP/FN cùng được đếm trên pixel của cùng phép đánh giá. Không thể dùng các cột P/R này để suy ra Dice 0,8865 và IoU 0,7961 như kết quả đo mặt nạ.

Nếu đề cương yêu cầu Dice/IoU, cần đánh giá mặt nạ dự đoán với mask GT, công bố resize/rasterization, ngưỡng, quy tắc nhiều đối tượng/ảnh nền và cách lấy trung bình. Trước đó ghi chưa đo, bỏ các ô giá trị không có nguồn tính hợp lệ.

Tập val có 120 ảnh polyp nhưng **127 vùng polyp**. CSV confusion matrix Baseline seed 0 có TP=111, FN=16 (tổng 127), FP=18, khác bảng bản thảo TP=112, FN=8, FP=4. Đơn vị của CM phát hiện là đối tượng, không phải ảnh. Một ảnh có thể tạo nhiều FP và FP cũng có thể nằm trên ảnh dương tính, nên **không được tính TN ảnh bằng 40 trừ FP đối tượng**.

Muốn báo Specificity ảnh phải dự đoán riêng trên 40 ảnh nền, đếm mỗi ảnh bị báo nhầm một lần, với ngưỡng xác định trước. Không dùng CM hiện có để khẳng định giảm ca bỏ sót, ADR, độ đặc hiệu >90% hay hiệu quả điều trị.

### 4.3. Sự cố checkpoint FP16 và giới hạn audit

Fork gốc `ultralytics_Topology-Shape-aware VMamba/engine/trainer.py` có chuyển EMA sang `.half()` và `nan_to_num_` trước lưu. Tài liệu 27 và `ultralytics_Topology-Shape-aware_VMamba_FP32/PATCH_FP32.md` giải thích sự cố và bản vá giữ FP32. Đã đối chiếu đoạn code lưu, chưa chạy lại thí nghiệm BN/checkpoint trong lần rà soát này.

Kết quả trong results.csv và hình/CM/dự đoán tạo từ checkpoint cuối là hai loại bằng chứng khác nhau. Không lấy log mAP tốt làm chứng cứ checkpoint triển khai hoạt động tương đương. Cần thêm mục về lỗi lưu FP16, ảnh hưởng đến bằng chứng triển khai, bản vá và tình trạng train/validate lại. Không tự đổi TSVM gốc thành TSVM-LN vì đó là thay đổi kiến trúc.

`07_audit/audit_report.md` thực sự có 694/694 PASS nhưng cũng nêu TN tái dựng và CM TSVM s0/s5/s8 không khớp. Script chủ yếu đối chiếu bảng CSV, không chứng nhận mọi ô của 11 bản thảo hiện tại đúng; các bảng sai phát hiện ở trên là phản ví dụ trực tiếp. Cần báo phạm vi kiểm tra, ngày chạy và giới hạn, bỏ “chính xác/trung thực/tái lập 100%”.

### 4.4. Cấu hình và notebook Kaggle

Các args.yaml đã quét cho giá trị thống nhất: **batch=8, workers=2, AdamW, lr0=0,001, warmup_epochs=5, amp=false, cos_lr=false, degrees=0, perspective=0**. Bản thảo ghi batch16, workers4, SGD, lr0=0,01, warmup3, cosine và xoay/phối cảnh là sai. Giá trị dfl=1,5 còn tồn tại trong args không có nghĩa YOLO26 dùng DFL khi `reg_max=1`.

Notebook Baseline hiện có **3 cell**, TSVM **4 cell**, đều đặt **SEED=10** và chạy một seed/lần; không có vòng lặp 10 seed. Notebook dùng dataset gắn trực tiếp trong `/kaggle/input/...`, tạo YAML trong working, không mô tả thành quy trình 6 cell giải nén RAR. TSVM tạo YAML scale s từ `yolo26-seg-TopologyShapeVMamba.yaml` rồi `.load("yolo26s-seg.pt")`.

Không gọi file YOLO pretrained là trọng số ImageNet khi notebook không thể hiện điều đó. Bảng phiên bản Python/PyTorch/CUDA/OS và cấu hình CPU/RAM Kaggle cần trích log môi trường từng run, không lấy giá trị mẫu làm số đo. Notebook hiện trỏ fork gốc; khi train mới cần chủ động dùng fork FP32 đã vá, nhưng không sửa notebook lịch sử rồi mô tả như trước đây đã dùng bản vá.

### 4.5. Kiến trúc đề xuất

YAML đúng là `cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml`, tầng 10 `C2TSVMamba`, đầu ra 512 kênh ở scale s. Bên trong wrapper tách kênh rồi chạy khối TSVM trên nhánh con; không nên mô tả toàn khối như một VSS tuần tự duy nhất trên 512 kênh.

Luồng chính theo `TSVMamba.forward`: SS2D(x); nhánh shape; directional extractor; gate sigmoid; nhân đặc trưng SS2D với (1+gate); concat với đặc trưng shape/topology; Conv fuse; FFN; residual `x + gamma*f_out`. Gamma khởi tạo 0,001. Sơ đồ hiện tại thiếu hầu hết thành phần làm nên đóng góp TSVM và đưa LayerNorm vào nơi fork gốc không có.

SS2D tạo raster xuôi/ngược và column-major xuôi/ngược bằng flatten/transpose/flip, không phải bốn đường quét chéo. Code dùng `a=exp(clamp(dt*A))` và thành phần vào `dt*B*u`; không được trình bày công thức ZOH đầy đủ như phép rời rạc hóa thực thi y hệt trong fork.

YAML có `end2end=True`, `reg_max=1`; `BboxLoss` chọn nhánh L1 khi không dùng DFL. Chương 2 cần mô tả loss theo criterion thực tế, kể cả nhánh end-to-end và các thành phần segmentation liên quan, không chép công thức generic DFL/objectness của dòng khác. Không gọi tầng 10 là “tối ưu” nếu chưa có ablation vị trí; code có các mode ablation không chứng minh đã chạy chúng.

### 4.6. Dữ liệu và đối chiếu DOCX của thành viên

Đếm trực tiếp trên thư mục dữ liệu:

| Thành phần | Train | Val |
|---|---:|---:|
| Ảnh | 1.040 | 160 |
| Tệp nhãn | 1.040 | 160 |
| Nhãn rỗng 0 byte | 160 | 40 |
| Dòng nhãn đối tượng | 936 | 127 |
| Ảnh thiếu nhãn tương ứng | 0 | 0 |

Không có tên ảnh trùng giữa train và val. Chưa kiểm lại hash hoặc trùng gần giống/patient-level trong lần rà soát này, nên không diễn giải việc không trùng tên là loại trừ mọi rò rỉ dữ liệu.

`Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py` đọc mask `.jpg`, chuyển xám, Otsu, closing 3×3 một lần, RETR_EXTERNAL/CHAIN_APPROX_SIMPLE, min_area=20, approxPolyDP epsilon=0,002×chu vi, chuẩn hóa và ghi 6 chữ số thập phân. Bản thảo ghi PNG, ngưỡng 10 pixel, bỏ Otsu/closing và dùng tên script khác là sai.

BG20 nghĩa **200 ảnh nền bằng 20% của 1.000 ảnh polyp**, không phải 20% tổng dữ liệu. Tỷ lệ nền toàn tập 16,67%, train 15,38%, val 25%; không làm tròn 16,67 thành “xấp xỉ 20%” để giải thích tên tập. Polyp lấy theo train.txt/val.txt có sẵn; seed42 áp dụng chọn/chia ảnh nền, không chia ngẫu nhiên toàn bộ 1.200 ảnh theo cùng tỷ lệ phân tầng.

DOCX `Tien_Xu_Ly_Du_Lieu.docx` mô tả đúng hơn bản Markdown về pipeline, tỷ lệ BG20, số vùng và giới hạn đánh giá. Nên dùng làm nền Chương 3. Tuy nhiên, các số đo như 333 kích thước ảnh, phân bố diện tích, Otsu 5–8, số contour bị loại, trung bình đỉnh và tái tạo nhãn/hash cần giữ kèm script/output kiểm chứng; lần này chưa chạy lại các phép đó. Khi gộp phải đổi số tài liệu tham khảo cục bộ sang danh mục chung và giữ đầy đủ công thức Word dạng OMML, vì trích w:t đơn thuần không đọc được nội dung công thức.

YAML dataset hiện vẫn ghi đường dẫn cũ `archive/Kvasir_YOLO_SEG_BG20` trong khi vị trí người dùng chỉ định là `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20`. Đây là cấu hình cần chỉnh khi chạy cục bộ, không sửa lịch sử trong biên bản này; notebook tự tạo YAML theo vị trí Kaggle nên là trường hợp khác.

### 4.7. Ứng dụng minh họa và mô hình đang khai báo

Trong `../Ung_Dung/polypweb/polypweb/pom.xml`, Spring Boot là **4.1.0**, Java **17**, có MongoDB, Thymeleaf và Spring Security; không phải Spring Boot 3.x như bản thảo.

`ai-service/main.py` khai báo model key **YOLO26n-seg** và **YOLO26n-VMamba-seg**, file mặc định `yolo26n-seg-best.pt`/`yolo26n-vmamba-seg-best.pt`, đăng ký lớp **VMambaBlock** ở `ultralytics.nn.modules.vmamba`. Báo cáo nghiên cứu lại là **YOLO26s + C2TSVMamba**. Đây là khác biệt xác nhận từ cấu hình/code; chưa kiểm checkpoint và biến môi trường runtime nên chưa kết luận chắc mô hình server đang chạy là gì. Không được viết ứng dụng đã triển khai TSVM s nếu chưa đối chiếu trọng số, class, scale và kết quả dự đoán.

API legacy thực tế: **POST /predict**, phản hồi có `processingTimeMs`, `maskCount`, `modelType`, `resultImageBase64` và các trường trạng thái. API trực tiếp cho mobile: **/api/v1/health, /api/v1/models, POST /api/v1/inference, POST /api/v1/comparison**. Không có căn cứ cho `POST /api/v1/predict` và payload `TSVM_Layer10/polygon_points/area_pixels` trong bản thảo.

Flutter có đường gọi FastAPI trực tiếp và đường API backend cho auth/history/diagnosis/comparison. Chương ứng dụng nên mô tả luồng thực tế, các use case, lưu lịch sử và giới hạn; không cần tự nhận toàn bộ là microservices hoàn chỉnh. Chưa đo thời gian toàn trình, kích thước APK, hoặc kiểm máy thật, nên bỏ khẳng định <1 giây/<35 MB/chạy mượt nếu không có log nghiệm thu.

### 4.8. Benchmark, ngoại suy và hình minh họa

Nguồn `Ket_Qua_V2/efficiency_benchmark/reports/benchmark_report.md` ghi **AMD Ryzen 7, 16 GB RAM, CPU**, tensor giả lập batch1 640×640, warmup20, đo100 lượt. Bảng summary có latency 200,12/821,27 ms, FPS 5,00/1,22; **VRAM để trống/N/A**. Bản thảo đổi CPU thành Intel Xeon và thêm GPU T4 18,2/28,5 ms, VRAM 1,15/1,42 GB là không được nguồn này hỗ trợ.

Cần ghi đây là benchmark forward trên tensor và checkpoint lịch sử, không phải toàn trình web và không chứng nhận chất lượng checkpoint. THOP có thể không đếm hết thao tác custom SS2D; tránh suy từ FLOPs sang tốc độ hoặc kết luận ưu thế so với ViT chưa đo cùng giao thức.

Chưa tìm thấy artifact kết quả gốc hỗ trợ các số ngoại suy ClinicDB 0,812/0,826; ColonDB 0,685/0,698; ETIS 0,624/0,641 trong phạm vi nguồn đã kiểm. Chuyển thành hướng thử nghiệm dự kiến hoặc bỏ bảng; chỉ đưa lại khi có dataset split, checkpoint, lệnh đánh giá và output thực tế.

Kiểm tra các đường PNG được ghi trong bản thảo theo ba gốc liên quan (thư mục bản thảo, KQ_Nen_DX_10seed, efficiency_benchmark) cho thấy **19 đường chưa có tệp tại các vị trí đó**. Các hình đang ghi là “minh họa” không thể đi kèm nhận xét như đã quan sát IoU=0,882, mặt nạ bao trọn 100%, polyp <5 mm hoặc SSL nếu chưa có ảnh, đo mặt nạ và nhãn lâm sàng tương ứng. Hình có thể đang nằm ở tên khác; phải ánh xạ về tệp thật trước khi chèn. Các placeholder nên chuyển sang checklist biên tập, không đưa nguyên khối hướng dẫn AI vào nội dung báo cáo cuối.

### 4.9. Tài liệu tham khảo, văn phong và tiến độ

Đã kiểm nguồn chính thức: YOLO26 arXiv:2606.03748 tồn tại và nêu bỏ DFL; VMamba arXiv:2401.10166 và Vision Mamba arXiv:2401.09417 là hai công trình riêng; Polyp-Mamba có DOI nêu trong bản thảo. HarDNet-MSEG **đúng là arXiv:2101.07172**, còn mã 2101.07151 trỏ tới công trình toán khác. Đã sửa mục [11].

Nguồn: [YOLO26](https://arxiv.org/abs/2606.03748), [VMamba](https://arxiv.org/abs/2401.10166), [Vision Mamba](https://arxiv.org/abs/2401.09417), [Polyp-Mamba/MICCAI](https://papers.miccai.org/miccai-2024/612-Paper0697.html), [HarDNet-MSEG](https://arxiv.org/abs/2101.07172).

Chương 1 gom tốc độ CNN 30–45 FPS, Transformer <15 FPS, SSM 20–30 FPS là thiếu căn cứ chung: riêng paper HarDNet-MSEG báo 86,7 FPS với RTX2080Ti và độ phân giải/giao thức của paper. Không so trực tiếp với benchmark CPU của đề tài. Không dùng một dải FPS đại diện cho cả họ kiến trúc.

Các tỷ lệ y khoa ở mở đầu cần nguồn gắn ngay câu và định nghĩa điều kiện đo. Bỏ lời khẳng định chắc về bệnh học từ ảnh phân đoạn một lớp; nhãn hiện chỉ là polyp, không phân loại giải phẫu bệnh.

Thay “xuất sắc”, “chí tử”, “triệt để”, “vượt trội”, “100%”, “chuẩn lâm sàng” bằng mô tả định lượng có giới hạn. Ngày rà soát là 12/10/2026, nên tuần 10–12 (19/10–08/11) trong bảng tiến độ chưa thể ghi là công việc quá khứ đã hoàn thành. Trạng thái thực tế phải xác nhận từ nhóm; không tự chấm điểm CLO hoặc kết luận thay hội đồng.

## 5. Chỉnh sửa đã thực hiện và hướng hoàn thiện

Chỉ thực hiện hai sửa đổi chắc chắn trong bản thảo: sửa mã tham khảo HarDNet-MSEG ở file `08`, bỏ thông tin đăng nhập ở file `10`. Tạo biên bản rà soát này. Các chương và số liệu nguồn được giữ để người viết đối chiếu; chưa viết lại đồng loạt khi phạm vi kết quả chính và mô hình ứng dụng chưa được chốt.

Thứ tự hoàn thiện:

1. Chốt N=10 hay N=21, tiêu chí chọn epoch và loại kết quả (log huấn luyện/checkpoint validate lại).
2. Thay các bảng sai từ CSV gốc; loại các độ đo và ngoại suy chưa có bằng chứng; bổ sung giới hạn FP16.
3. Viết đúng Chương 2 theo forward/code và Chương 3 theo DOCX tiền xử lý có đối chiếu.
4. Viết Chương 4 theo notebook/args/API thật; xác nhận ứng dụng có đúng checkpoint nghiên cứu.
5. Viết lại mở đầu, kết luận, phụ lục để không mâu thuẫn; đưa hình thật và trích dẫn vào từng đoạn.
6. Ghép DOCX theo mẫu HUIT, cập nhật trường mục lục/caption và render kiểm toàn bộ trang.

Hai thông tin cần nhóm xác nhận để chỉnh toàn bộ bản thảo nhất quán: **bộ seed chính** và **phiên bản ứng dụng/loại trọng số triển khai**. Ngoài ra, nếu nhóm có kết quả ngoại suy hoặc GPU ở nơi khác, cần chỉ rõ vị trí artifact đó trước khi dùng lại số liệu.

## 6. Ghi nhận kiểm tra cuối

- Đã tính lại mean/sample std từ log gốc cho N=10 và N=21; không chỉ tin bảng Markdown.
- Đã đếm dataset và kiểm ghép ảnh–nhãn, không có ảnh thiếu nhãn và không trùng tên giữa hai split.
- Đã đối chiếu giá trị args.yaml trong hai cây kết quả; không chạy huấn luyện/test mô hình.
- Đã đọc code criterion/fitness, checkpoint saving và API để phân biệt implementation với mô tả.
- Chưa chạy lại p-value, benchmark, suy luận checkpoint, raster hóa Dice/IoU, đối chiếu mask gốc, hoặc layout DOCX; các phần đó được nêu đúng mức kiểm chứng.
- Không tạo script mới, không dùng subagent; tái sử dụng log/config/script kiểm toán có sẵn làm căn cứ.
