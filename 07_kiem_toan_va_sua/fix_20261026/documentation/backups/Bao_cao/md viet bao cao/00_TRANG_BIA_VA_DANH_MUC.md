# PHẦN ĐẦU: TRANG BÌA VÀ CÁC DANH MỤC KHÓA LUẬN CỬ NHÂN

---

## 1. TRANG BÌA CHÍNH (BÌA NGOÀI)

```text
               BỘ CÔNG THƯƠNG
 TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG THÀNH PHỐ HỒ CHÍ MINH
              KHOA CÔNG NGHỆ THÔNG TIN
                   ---------------
                    (LOGO TRƯỜNG)




                  KHÓA LUẬN CỬ NHÂN
                NGÀNH CÔNG NGHỆ THÔNG TIN
                  CHUYÊN NGÀNH: [CNTT]
                  MÃ ĐỀ TÀI: CNTT_KLCN182



NGHIÊN CỨU PHƯƠNG PHÁP TÍCH HỢP VMAMBA VÀO MÔ HÌNH 
YOLO26-SEG TRONG PHÂN ĐOẠN POLYP TỪ ẢNH NỘI SOI ĐẠI TRỰC TRÀNG




       Sinh viên thực hiện:
       1. LÊ ĐỨC LƯƠNG      - MSSV: 2001230490 - Lớp: 14DHTH09
       2. PHÙNG TUẤN HUY    - MSSV: 2001230312 - Lớp: 14DHTH13
       3. TRẦN MẠNH TOÀN    - MSSV: 2001230830 - Lớp: 14DHTH09

       Giảng viên hướng dẫn:
       TS. PHÙNG THẾ BẢO





               TP. HỒ CHÍ MINH, NĂM 2026
```

---

## 2. TRANG BÌA PHỤ (BÌA LÓT BÊN TRONG)

```text
               BỘ CÔNG THƯƠNG
 TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG THÀNH PHỐ HỒ CHÍ MINH
              KHOA CÔNG NGHỆ THÔNG TIN
                   ---------------
                    (LOGO TRƯỜNG)




                  KHÓA LUẬN CỬ NHÂN
                NGÀNH CÔNG NGHỆ THÔNG TIN
                  CHUYÊN NGÀNH: [CNTT]
                  MÃ ĐỀ TÀI: CNTT_KLCN182



NGHIÊN CỨU PHƯƠNG PHÁP TÍCH HỢP VMAMBA VÀO MÔ HÌNH 
YOLO26-SEG TRONG PHÂN ĐOẠN POLYP TỪ ẢNH NỘI SOI ĐẠI TRỰC TRÀNG




       Sinh viên thực hiện:
       1. LÊ ĐỨC LƯƠNG      - MSSV: 2001230490 - Lớp: 14DHTH09
       2. PHÙNG TUẤN HUY    - MSSV: 2001230312 - Lớp: 14DHTH13
       3. TRẦN MẠNH TOÀN    - MSSV: 2001230830 - Lớp: 14DHTH09

       Giảng viên hướng dẫn:
       TS. PHÙNG THẾ BẢO





               TP. HỒ CHÍ MINH, NĂM 2026
```

---

## 3. LỜI CẢM ƠN

Trong suốt quá trình học tập và hoàn thành khóa luận tốt nghiệp cử nhân ngành Công nghệ Thông tin tại Trường Đại học Công Thương Thành phố Hồ Chí Minh (HUIT), nhóm sinh viên chúng em đã nhận được sự quan tâm, giảng dạy tận tình và hỗ trợ quý báu từ quý Thầy, Cô và gia đình.

Trước hết, nhóm xin gửi lời tri ân sâu sắc nhất đến Ban Giám hiệu Trường Đại học Công Thương Thành phố Hồ Chí Minh cùng toàn thể quý Thầy, Cô Khoa Công nghệ Thông tin. Những kiến thức nền tảng vững chắc và chuyên sâu được quý Thầy Cô truyền thụ trong suốt 4 năm đại học chính là hành trang quan trọng giúp chúng em tiếp cận và nghiên cứu các công nghệ học sâu tiên tiến phục vụ đề tài khóa luận này.

Đặc biệt, nhóm xin bày tỏ lòng biết ơn chân thành và sâu sắc nhất tới **TS. Phùng Thế Bảo** – Giảng viên hướng dẫn trực tiếp của đề tài. Thầy đã luôn định hướng khoa học chuẩn xác, truyền cảm hứng nghiên cứu, kiên nhẫn hướng dẫn và đưa ra những đóng góp chuyên môn quý báu trong suốt quá trình nhóm khảo sát thuật toán, thiết kế mô hình TSVM, xử lý thực nghiệm đối chứng 10 seed tất định và xây dựng hệ sinh thái ứng dụng minh họa. Sự chỉ bảo nghiêm cẩn và tâm huyết của Thầy không chỉ giúp nhóm hoàn thành tốt khóa luận mà còn rèn luyện cho chúng em tác phong làm việc khoa học, trung thực và trách nhiệm.

Nhóm cũng xin chân thành cảm ơn quý Thầy, Cô trong Hội đồng chấm khóa luận tốt nghiệp đã dành thời gian đọc, nhận xét và đưa ra những ý kiến phản biện sắc bén giúp đề tài ngày càng hoàn thiện hơn.

Cuối cùng, chúng con xin gửi lời cảm ơn vô hạn đến Cha Mẹ và gia đình – nguồn động viên tinh thần và chỗ dựa vững chắc nhất cho chúng con trong suốt quá trình học tập và phấn đấu.

Dù đã rất nỗ lực nghiên cứu và hoàn thiện khóa luận với tinh thần nghiêm túc cao nhất, song do thời gian và kinh nghiệm thực tế còn hạn chế, đề tài chắc chắn không tránh khỏi những thiếu sót. Nhóm chúng em rất mong nhận được những lời chỉ dẫn, đóng góp quý báu từ quý Thầy Cô để công trình nghiên cứu được hoàn thiện hơn nữa.

*Tp. Hồ Chí Minh, ngày … tháng … năm 2026*  
**Nhóm sinh viên thực hiện**  
*Lê Đức Lương – Phùng Tuấn Huy – Trần Mạnh Toàn*

---

## 4. NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN

**1. Về tinh thần, thái độ và tác phong làm việc của nhóm sinh viên:**  
.................................................................................................................................................................................  
.................................................................................................................................................................................  
.................................................................................................................................................................................  

**2. Về tính cấp thiết, phương pháp nghiên cứu và hàm lượng khoa học của đề tài:**  
.................................................................................................................................................................................  
.................................................................................................................................................................................  
.................................................................................................................................................................................  

**3. Về kết quả đạt được và sản phẩm ứng dụng (Mô hình AI, Web, Mobile App):**  
.................................................................................................................................................................................  
.................................................................................................................................................................................  
.................................................................................................................................................................................  

**4. Điểm đánh giá và kết luận:**  
- Điểm đánh giá (bằng số): ....................... (Bằng chữ: ....................................................................................)  
- Kết luận: Cho phép / Không cho phép sinh viên được bảo vệ trước Hội đồng chấm khóa luận cử nhân.  

*Tp. Hồ Chí Minh, ngày … tháng … năm 2026*  
**Giảng viên hướng dẫn**  
*(Ký và ghi rõ họ tên)*  



**TS. Phùng Thế Bảo**

---

## 5. NHẬN XÉT CỦA GIẢNG VIÊN PHẢN BIỆN

**1. Về hình thức trình bày và cấu trúc của quyển báo cáo khóa luận:**  
.................................................................................................................................................................................  
.................................................................................................................................................................................  

**2. Về độ tin cậy của phương pháp nghiên cứu và kết quả thực nghiệm:**  
.................................................................................................................................................................................  
.................................................................................................................................................................................  

**3. Về tính ứng dụng và độ hoàn thiện của sản phẩm phần mềm (Web & App):**  
.................................................................................................................................................................................  
.................................................................................................................................................................................  

**4. Những ưu điểm chính và điểm cần hoàn thiện của đề tài:**  
.................................................................................................................................................................................  
.................................................................................................................................................................................  

**5. Câu hỏi dành cho sinh viên trong buổi bảo vệ:**  
- *Câu hỏi 1*: ......................................................................................................................................................  
- *Câu hỏi 2*: ......................................................................................................................................................  

**6. Điểm đánh giá:**  
- Điểm đánh giá (bằng số): ....................... (Bằng chữ: ....................................................................................)  

*Tp. Hồ Chí Minh, ngày … tháng … năm 2026*  
**Giảng viên phản biện**  
*(Ký và ghi rõ họ tên)*  

---

## 6. DANH MỤC CÁC KÝ HIỆU VÀ CHỮ VIẾT TẮT

| Ký hiệu / Chữ viết tắt | Tên tiếng Anh đầy đủ | Giải thích nghĩa tiếng Việt |
|:---|:---|:---|
| **AI** | Artificial Intelligence | Trí tuệ nhân tạo |
| **API** | Application Programming Interface | Giao diện lập trình ứng dụng |
| **AUC** | Area Under the Curve | Diện tích dưới đường cong |
| **BG20** | Background 20% | Tập dữ liệu bổ sung 20% ảnh nền âm tính (niêm mạc bình thường) |
| **CNN** | Convolutional Neural Network | Mạng nơ-ron tích chập |
| **CRC** | Colorectal Cancer | Ung thư đại trực tràng |
| **CUDA** | Compute Unified Device Architecture | Nền tảng tính toán song song trên GPU của Nvidia |
| **DSC** | Dice Similarity Coefficient | Hệ số tương đồng Dice (chỉ số đánh giá độ trùng khớp mặt nạ) |
| **FN** | False Negative | Âm tính giả (bỏ sót tổn thương polyp) |
| **FP** | False Positive | Dương tính giả (báo động nhầm niêm mạc lành là polyp) |
| **FPS** | Frames Per Second | Tốc độ xử lý khung hình trên giây |
| **GFLOPs** | Giga Floating-point Operations | Tỷ phép tính dấu phẩy động (độ phức tạp tính toán) |
| **GPU** | Graphics Processing Unit | Bộ vi xử lý đồ họa |
| **GT** | Ground Truth | Nhãn chuẩn / Mặt nạ thực tế do chuyên gia y tế gán |
| **IoU** | Intersection over Union | Tỷ lệ phần giao trên phần hợp (Jaccard Index) |
| **mAP** | Mean Average Precision | Độ chính xác trung bình trung bình |
| **mAP50** | Mean Average Precision at IoU=0.50 | Độ chính xác trung bình tại ngưỡng IoU 0.50 |
| **mAP50-95** | Mean Average Precision at IoU=0.50:0.95 | Độ chính xác trung bình tổng hợp từ ngưỡng IoU 0.50 đến 0.95 |
| **PAN-FPN** | Path Aggregation Network - Feature Pyramid Network | Mạng kim tự tháp đặc trưng tổng hợp đường dẫn |
| **PR Curve** | Precision-Recall Curve | Đường cong biểu diễn đánh đổi giữa Precision và Recall |
| **P5** | Feature Level 5 (Stride 32) | Mức đặc trưng sâu nhất tại tầng trích xuất của Backbone |
| **SSM** | State Space Model | Mô hình không gian trạng thái |
| **SS2D** | 2D Selective Scan | Cơ chế quét chọn lọc không gian 2 chiều trong VMamba |
| **TN** | True Negative | Âm tính thật (nhận diện đúng niêm mạc bình thường) |
| **TP** | True Positive | Dương tính thật (phát hiện và phân đoạn đúng polyp) |
| **TSVM** | Topology-Shape-aware VMamba | Kiến trúc đề xuất tích hợp VMamba nhận biết hình thái và topo |
| **VRAM** | Video Random Access Memory | Bộ nhớ truy xuất ngẫu nhiên của GPU |
| **YOLO** | You Only Look Once | Họ mô hình thị giác máy tính phát hiện/phân đoạn thời gian thực |

---

## 7. DANH MỤC CÁC HÌNH VẼ

*(Ghi chú: Trong bản Word cuối cùng, mục này được tự động chèn bằng trường `TOC \h \z \c "Hình"`. Dưới đây là danh mục toàn bộ các hình vẽ được quy hoạch chuẩn xác trong báo cáo)*

- **Hình 1.1**: Hình thái các dạng polyp đại trực tràng từ bộ dữ liệu nội soi Kvasir-SEG
- **Hình 1.2**: Sơ đồ nguyên lý cơ chế quét chọn lọc hai chiều không gian SS2D trong kiến trúc VMamba
- **Hình 2.1**: Sơ đồ kiến trúc tổng thể của mô hình cơ sở YOLO26-seg
- **Hình 2.2**: Cấu trúc chi tiết khối Topology-Shape-aware VMamba (TSVM) tích hợp tại tầng 10 (mức P5)
- **Hình 3.1**: Quy trình trích xuất và chuyển đổi Ground-Truth Mask sang nhãn đa giác đa điểm YOLO Polygon
- **Hình 3.2**: Minh họa nhãn ảnh polyp thông thường và tệp nhãn rỗng (0 byte) của ảnh nền âm tính normal-cecum
- **Hình 4.1**: Sơ đồ luồng thực thi trong các Cell Notebook Kaggle huấn luyện mô hình tất định
- **Hình 4.2**: Sơ đồ kiến trúc phân tầng hệ sinh thái ứng dụng minh họa (FastAPI AI Microservice – Java Spring Boot Web – Flutter Mobile App)
- **Hình 4.3**: Giao diện ứng dụng Web minh họa tải ảnh nội soi và hiển thị mặt nạ phân đoạn polyp
- **Hình 4.4**: Giao diện ứng dụng di động Flutter minh họa chụp ảnh camera và khoanh vùng tổn thương trực tiếp
- **Hình 5.1**: Đồ thị so sánh đường cong suy giảm hàm mất mát (Loss Convergence) giữa Baseline và TSVM
- **Hình 5.2**: Đồ thị đánh đổi Precision-Recall của hộp bao (Box PR Curve)
- **Hình 5.3**: Đồ thị đánh đổi Precision-Recall của mặt nạ phân đoạn (Mask PR Curve)
- **Hình 5.4**: Đồ thị biến thiên chỉ số F1 theo ngưỡng tin cậy của hộp bao (Box F1-Confidence Curve)
- **Hình 5.5**: Đồ thị biến thiên chỉ số F1 theo ngưỡng tin cậy của mặt nạ phân đoạn (Mask F1-Confidence Curve)
- **Hình 5.6**: Ma trận nhầm lẫn chuẩn hóa (Normalized Confusion Matrix) của Baseline và TSVM
- **Hình 5.7**: Biểu đồ phân phối biến thiên các chỉ số qua 10 lượt chạy độc lập (Seed Distribution)
- **Hình 5.8**: Biểu đồ so sánh độ lệch chuẩn và sự co hẹp phương sai giữa Baseline và TSVM
- **Hình 5.9**: Biểu đồ phân bố độ trễ suy luận (Latency Breakdown) trên phần cứng thử nghiệm
- **Hình 5.10**: Biểu đồ tương quan giữa độ chính xác phân đoạn mặt nạ (Mask mAP50-95) và chi phí tính toán (GFLOPs)
- **Hình 5.11**: So sánh trực quan mặt nạ phân đoạn thực tế trên ca polyp kích thước nhỏ (Small Polyp)
- **Hình 5.12**: So sánh trực quan mặt nạ phân đoạn thực tế trên ca polyp dạng phẳng, ranh giới mờ (Flat/Blurry Polyp)

---

## 8. DANH MỤC CÁC BẢNG BIỂU

*(Ghi chú: Trong bản Word cuối cùng, mục này được tự động chèn bằng trường `TOC \h \z \c "Bảng"`. Dưới đây là danh mục các bảng số liệu chính trong báo cáo)*

- **Bảng 1.1**: So sánh đặc tính của các phương pháp phân đoạn polyp dựa trên CNN, Transformer và SSM
- **Bảng 3.1**: Thống kê số lượng mẫu phân bổ trong tập dữ liệu hỗn hợp Kvasir_YOLO_SEG_BG20
- **Bảng 4.1**: Cấu hình phần cứng và phần mềm môi trường thực nghiệm Kaggle GPU
- **Bảng 4.2**: Danh mục các siêu tham số huấn luyện tất định áp dụng cho 10 seed
- **Bảng 5.1**: Bảng so sánh định lượng tổng hợp hiệu năng Baseline YOLO26s-seg và mô hình TSVM qua 10 seed (Mean ± Std, Range, Δ, p-value)
- **Bảng 5.2**: Kết quả chi tiết hiệu năng phân đoạn của Baseline và TSVM qua từng seed độc lập (Seed 0 đến Seed 9)
- **Bảng 5.3**: Ma trận nhầm lẫn trung bình qua 10 seed và các chỉ số bệnh học lâm sàng (Recall, Specificity tái dựng, Precision)
- **Bảng 5.4**: Bảng đối chứng chi phí tính toán, tham số mô hình, GFLOPs và tốc độ suy luận (Latency, FPS)
- **Bảng 5.5**: Kết quả kiểm thử khả năng tổng quát hóa trên các tập dữ liệu ngoại suy độc lập
- **Bảng H.1**: Ma trận đối chiếu Chuẩn đầu ra (CLO 1.1 đến CLO 6) và các mục trong khóa luận
