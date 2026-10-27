# D. Kiểm tra và đề xuất danh mục tài liệu tham khảo (chuẩn IEEE)

Ngày kiểm tra: 26/10/2026 (cập nhật đợt 2 cùng ngày: thêm mục 3.9, 3.10 và cập nhật mục 4). Người kiểm tra: sub-agent "Thủ thư nghiên cứu" (chỉ đọc, không sửa file nguồn).

Nguồn đã đối chiếu:

- `TLTK\MANIFEST.txt`, file Word `... - Tài Liệu Tham Khảo.docx`, `TAI_LIEU_KHONG_TIM_THAY_PDF.txt`.
- Trang đầu và metadata của 24 PDF, đọc bằng `pypdf`.
- Crossref REST API (`api.crossref.org/works/<DOI>`): tác giả, tiêu đề, nơi công bố, tập/số/trang.
- arXiv API (`export.arxiv.org`): tác giả, tiêu đề, ghi chú hội nghị.
- Các trang chính thức: arxiv.org, docs.ultralytics.com, `CITATION.cff` trên GitHub Ultralytics, PyPI, papers.miccai.org, jmlr.org, proceedings.mlsys.org, proceedings.neurips.cc, datasets.simula.no.
- `06_bao_cao/luu_tru_cu/LUA_CHON_VA_BO_SUNG_TAI_LIEU_THAM_KHAO.md`: chỉ dùng để tham khảo.

Ký hiệu trạng thái:

- **OK**: thông tin đã khớp với nguồn chính thức.
- **Sửa**: thông tin đúng nhưng cần chỉnh định dạng hoặc bổ sung chi tiết.
- **Lưu ý**: hợp lệ nhưng có điểm cần nói rõ khi dùng.

---

## 1. Bảng kiểm tra 24 tài liệu hiện có

### 1.1. Lỗi chung trong MANIFEST và file Word

1. **Tên file trong MANIFEST không khớp tên file thực tế (24/24).**
   - MANIFEST ghi tên có dấu " - ", ví dụ `[1] Kvasir-SEG - A Segmented Polyp Dataset.pdf`.
   - File thực tế không có dấu này: `[1] Kvasir-SEG A Segmented Polyp Dataset.pdf`.
   - [4]: MANIFEST ghi tên rút gọn `[4] A Survey on Deep Learning for Polyp Segmentation.pdf`, file thật có tên đầy đủ.
   - [11]: file thật là `... Unified, Real-Time ...`.
   - Không ảnh hưởng đến trích dẫn, nhưng nên sửa nếu có script nào đọc MANIFEST.
2. **File Word chưa theo đúng quy cách IEEE.**
   - Tiêu đề bài báo nên viết hoa kiểu câu (sentence case) trong ngoặc kép.
   - Tên hội nghị và tạp chí cần viết nghiêng, theo dạng viết tắt IEEE.
   - LNCS nên ghi dạng "(Lecture Notes in Computer Science, vol. …)".
   - Bài có hơn 6 tác giả thì ghi "tác giả đầu et al.", bài có từ 6 tác giả trở xuống thì ghi đủ. Word cơ bản đã làm đúng quy tắc này. Lỗi duy nhất là cách ghi tên Việt ở [9] (xem bảng 1.2).
3. **Thứ tự đánh số trong Word theo chủ đề** (dataset → baseline → YOLO → SSM …), **không theo thứ tự xuất hiện**. Chuẩn IEEE yêu cầu đánh số theo thứ tự xuất hiện. Xem Mục 4.
4. Thư mục có file khóa `~$...Tài Liệu Tham Khảo.docx`, nghĩa là file Word có thể đang mở. Không ảnh hưởng gì, chỉ ghi chú lại.

### 1.2. Bảng chi tiết

| Số cũ | Tài liệu | Trạng thái | Lỗi/thiếu trong MANIFEST hoặc Word |
|---|---|---|---|
| [1] | Kvasir-SEG (MMM 2020) | OK | Không có lỗi nội dung. Bài đăng online ngày 24/12/2019, năm của tập sách là 2020. |
| [2] | Benchmark endoluminal (J. Healthcare Eng.) | OK | Crossref ghi trang 1–9. Dùng "Art. no. 4037190" như Word là hợp lệ. |
| [3] | PolypGen (Sci. Data) | OK | Nên thêm "no. 1". |
| [4] | Survey polyp (Visual Intelligence) | OK | Không có lỗi. Có 7 tác giả nên ghi "et al." |
| [5] | U-Net (MICCAI 2015) | OK | Không có lỗi. |
| [6] | UNet++ (DLMIA 2018) | OK | Không có lỗi. |
| [7] | PraNet (MICCAI 2020) | **Lưu ý** | Thông tin trích dẫn đúng. Tuy nhiên bản gốc của PraNet dùng backbone **Res2Net-50**, còn khóa luận dùng biến thể **ResNet-50**. Khi mô tả phải nói rõ là biến thể, và trích thêm ResNet (đề xuất N5). |
| [8] | Polyp-PVT (CAAI AIR) | OK | Crossref ghi mã bài 9150015, năm 2023. Word ghi vol. 2: đúng với năm xuất bản thứ hai của tạp chí. |
| [9] | ColonFormer (IEEE Access) | **Sửa** | Word ghi tác giả cuối là "V. S. Dinh", không nhất quán với 4 tác giả trước (đều ghi theo thứ tự tên Việt). Nên ghi **"D. V. Sang"**: trên bài báo tên là "Dinh Viet Sang", Crossref lưu "Viet Sang Dinh". Trang 80575–80586 đúng. |
| [10] | TransFuse (MICCAI 2021) | OK | Không có lỗi. |
| [11] | YOLO v1 (CVPR 2016) | OK | Trang 779–788 trùng nhau ở IEEE Xplore và CVF. |
| [12] | **Ultralytics YOLO26** (arXiv) | **OK (đã xác minh có thật)** | Xem phần riêng 1.3. |
| [13] | S4 (ICLR 2022) | OK | Trang OpenReview bị chặn bằng challenge nên không mở được. arXiv ghi "ICLR 2022 (Outstanding Paper HM)", đủ để xác nhận. |
| [14] | Mamba (COLM 2024) | **Lưu ý** | arXiv không có journal-ref, và OpenReview bị chặn. Hội nghị COLM 2024 được xác nhận qua nhiều nguồn thứ cấp (trang seminar ĐH Yonsei, tin về giải Outstanding Paper tại COLM 2024). Nếu Hội đồng yêu cầu chặt, có thể trích dạng arXiv:2312.00752. |
| [15] | VMamba (NeurIPS 2024) | OK | Crossref xác nhận trang 103031–103063 và DOI 10.52202/079017-3273. arXiv ghi "NeurIPS 2024 spotlight". |
| [16] | U-Mamba | OK | Chỉ có bản preprint arXiv (v1, 9/1/2024). |
| [17] | Mamba-UNet | OK | Chỉ có bản preprint arXiv (v2, 30/3/2024). |
| [18] | Swin-UMamba (MICCAI 2024) | **Sửa** | Word thiếu số tập LNCS. Đúng là **LNCS 15009** (Part IX), trang 615–625. |
| [19] | Polyp-Mamba (MICCAI 2024) | OK | LNCS 15008, trang 510–521. |
| [20] | PolyMamba (MICCAI 2025) | **Lưu ý** | LNCS 15970, trang 455–465. Bài đăng online 20/9/2025, nhưng Crossref ghi năm của tập là 2026. Đề xuất ghi 2025 (năm hội nghị và năm online), và dùng nhất quán. |
| [21] | SAM-Mamba (WACV 2025) | **Sửa** | Word và MANIFEST thiếu DOI. Crossref xác nhận **doi: 10.1109/WACV61041.2025.00457**, trang 4655–4664. |
| [22] | Mamba YOLO (AAAI 2025) | OK | Vol. 39, no. 8, trang 8205–8213. |
| [23] | FPN (CVPR 2017) | **Sửa** | Word ghi trang 2117–2125, là số trang của bản **CVF Open Access**. Nếu dùng DOI IEEE thì phải ghi trang theo IEEE Xplore là **936–944** (Crossref). |
| [24] | EfficientDet (CVPR 2020) | **Sửa** | Tương tự [23]: Word ghi trang 10781–10790 (CVF), còn DOI IEEE ứng với trang **10778–10787**. |

### 1.3. Riêng [12] YOLO26: kết luận xác minh

- **Có thật.** Trang `arxiv.org/abs/2606.03748` hiển thị:
  - Tiêu đề: "Ultralytics YOLO26: Unified Real-Time End-to-End Vision Models".
  - 6 tác giả: Glenn Jocher, Jing Qiu, Mengyu Liu, Shuai Lyu, Fatih Cagatay Akyon, Muhammet Esat Kalfaoglu.
  - Chỉ có bản v1, nộp ngày 2/6/2026. Phân loại cs.CV (kèm cs.AI). Dài 31 trang, 8 hình.
  - DOI: 10.48550/arXiv.2606.03748.
- **PDF trong máy khớp với bản arXiv.** Metadata của PDF có `/arXivID = https://arxiv.org/abs/2606.03748v1`, `/DOI` trùng với DOI trên, và Creator là "arXiv GenPDF". Trang 1 có dấu "arXiv:2606.03748v1 [cs.CV] 2 Jun 2026".
- **Ultralytics chính thức yêu cầu trích bài này.** `CITATION.cff` trên GitHub (`preferred-citation`) và trang `docs.ultralytics.com/models/yolo26/` đều đưa BibTeX trỏ về arXiv:2606.03748. Trang docs cho biết mô hình YOLO26 được phát hành từ tháng 1/2026, còn bài báo ra sau, vào tháng 6/2026.
- **Hạn chế cần nêu trong khóa luận:** đây là preprint, **chưa qua phản biện**. Kết quả trong bài chủ yếu đo trên COCO, chưa thử trên ảnh y khoa.
- **Khuyến nghị:**
  - Giữ [12] làm nguồn học thuật chính cho YOLO26.
  - **Bổ sung một trích dẫn phần mềm** (đề xuất N28) cho đúng phiên bản thư viện đã dùng: Ultralytics **8.4.127**, đã kiểm tra trên PyPI (phát hành 23/8/2026, giấy phép AGPL-3.0). Phiên bản này trùng với `__version__` trong fork `02_ma_nguon/ultralytics_TSVM_FP32`.

### 1.4. Bản IEEE chuẩn của 24 tài liệu (giữ số cũ)

> Viết nghiêng tên hội nghị/tạp chí khi chuyển sang Word. Trong markdown dùng `*…*`.

- [1] D. Jha *et al.*, "Kvasir-SEG: A segmented polyp dataset," in *MultiMedia Modeling (MMM 2020)* (Lecture Notes in Computer Science, vol. 11962). Cham, Switzerland: Springer, 2020, pp. 451–462, doi: 10.1007/978-3-030-37734-2_37.
- [2] D. Vázquez *et al.*, "A benchmark for endoluminal scene segmentation of colonoscopy images," *J. Healthcare Eng.*, vol. 2017, Art. no. 4037190, 2017, doi: 10.1155/2017/4037190.
- [3] S. Ali *et al.*, "A multi-centre polyp detection and segmentation dataset for generalisability assessment," *Sci. Data*, vol. 10, no. 1, Art. no. 75, 2023, doi: 10.1038/s41597-023-01981-y.
- [4] J. Mei *et al.*, "A survey on deep learning for polyp segmentation: Techniques, challenges and future trends," *Vis. Intell.*, vol. 3, no. 1, Art. no. 1, 2025, doi: 10.1007/s44267-024-00071-w.
- [5] O. Ronneberger, P. Fischer, and T. Brox, "U-Net: Convolutional networks for biomedical image segmentation," in *Medical Image Computing and Computer-Assisted Intervention – MICCAI 2015* (Lecture Notes in Computer Science, vol. 9351). Cham, Switzerland: Springer, 2015, pp. 234–241, doi: 10.1007/978-3-319-24574-4_28.
- [6] Z. Zhou, M. M. Rahman Siddiquee, N. Tajbakhsh, and J. Liang, "UNet++: A nested U-Net architecture for medical image segmentation," in *Deep Learning in Medical Image Analysis and Multimodal Learning for Clinical Decision Support (DLMIA/ML-CDS 2018)* (Lecture Notes in Computer Science, vol. 11045). Cham, Switzerland: Springer, 2018, pp. 3–11, doi: 10.1007/978-3-030-00889-5_1.
- [7] D.-P. Fan *et al.*, "PraNet: Parallel reverse attention network for polyp segmentation," in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2020* (Lecture Notes in Computer Science, vol. 12266). Cham, Switzerland: Springer, 2020, pp. 263–273, doi: 10.1007/978-3-030-59725-2_26.
- [8] B. Dong, W. Wang, D.-P. Fan, J. Li, H. Fu, and L. Shao, "Polyp-PVT: Polyp segmentation with pyramid vision transformers," *CAAI Artif. Intell. Res.*, vol. 2, Art. no. 9150015, 2023, doi: 10.26599/AIR.2023.9150015.
- [9] N. T. Duc, N. T. Oanh, N. T. Thuy, T. M. Triet, and D. V. Sang, "ColonFormer: An efficient transformer based method for colon polyp segmentation," *IEEE Access*, vol. 10, pp. 80575–80586, 2022, doi: 10.1109/ACCESS.2022.3195241.
- [10] Y. Zhang, H. Liu, and Q. Hu, "TransFuse: Fusing transformers and CNNs for medical image segmentation," in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2021* (Lecture Notes in Computer Science, vol. 12901). Cham, Switzerland: Springer, 2021, pp. 14–24, doi: 10.1007/978-3-030-87193-2_2.
- [11] J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, "You only look once: Unified, real-time object detection," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, Las Vegas, NV, USA, 2016, pp. 779–788, doi: 10.1109/CVPR.2016.91.
- [12] G. Jocher, J. Qiu, M. Liu, S. Lyu, F. C. Akyon, and M. E. Kalfaoglu, "Ultralytics YOLO26: Unified real-time end-to-end vision models," 2026, *arXiv:2606.03748*, doi: 10.48550/arXiv.2606.03748.
- [13] A. Gu, K. Goel, and C. Ré, "Efficiently modeling long sequences with structured state spaces," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2022. [Online]. Available: https://openreview.net/forum?id=uYLFoz1vlAC
- [14] A. Gu and T. Dao, "Mamba: Linear-time sequence modeling with selective state spaces," in *Proc. 1st Conf. Lang. Model. (COLM)*, Philadelphia, PA, USA, 2024. [Online]. Available: https://openreview.net/forum?id=tEYskw1VY2
- [15] Y. Liu *et al.*, "VMamba: Visual state space model," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 37, 2024, pp. 103031–103063, doi: 10.52202/079017-3273.
- [16] J. Ma, F. Li, and B. Wang, "U-Mamba: Enhancing long-range dependency for biomedical image segmentation," 2024, *arXiv:2401.04722*, doi: 10.48550/arXiv.2401.04722.
- [17] Z. Wang, J.-Q. Zheng, Y. Zhang, G. Cui, and L. Li, "Mamba-UNet: UNet-like pure visual Mamba for medical image segmentation," 2024, *arXiv:2402.05079*, doi: 10.48550/arXiv.2402.05079.
- [18] J. Liu *et al.*, "Swin-UMamba: Mamba-based UNet with ImageNet-based pretraining," in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2024* (Lecture Notes in Computer Science, vol. 15009). Cham, Switzerland: Springer, 2024, pp. 615–625, doi: 10.1007/978-3-031-72114-4_59.
- [19] Z. Xu *et al.*, "Polyp-Mamba: Polyp segmentation with visual Mamba," in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2024* (Lecture Notes in Computer Science, vol. 15008). Cham, Switzerland: Springer, 2024, pp. 510–521, doi: 10.1007/978-3-031-72111-3_48.
- [20] R. Fu, S. Hu, X. Zheng, C. Tang, and X. Liu, "PolyMamba: Spatial-prior guided Mamba for polyp segmentation with high-frequency enhancement," in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2025* (Lecture Notes in Computer Science, vol. 15970). Cham, Switzerland: Springer, 2025, pp. 455–465, doi: 10.1007/978-3-032-05141-7_44.
- [21] T. K. Dutta, S. Majhi, D. R. Nayak, and D. Jha, "SAM-Mamba: Mamba guided SAM architecture for generalized zero-shot polyp segmentation," in *Proc. IEEE/CVF Winter Conf. Appl. Comput. Vis. (WACV)*, Tucson, AZ, USA, 2025, pp. 4655–4664, doi: 10.1109/WACV61041.2025.00457.
- [22] Z. Wang, C. Li, H. Xu, X. Zhu, and H. Li, "Mamba YOLO: A simple baseline for object detection with state space model," in *Proc. AAAI Conf. Artif. Intell.*, vol. 39, no. 8, 2025, pp. 8205–8213, doi: 10.1609/aaai.v39i8.32885.
- [23] T.-Y. Lin, P. Dollár, R. Girshick, K. He, B. Hariharan, and S. Belongie, "Feature pyramid networks for object detection," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, Honolulu, HI, USA, 2017, pp. 936–944, doi: 10.1109/CVPR.2017.106.
- [24] M. Tan, R. Pang, and Q. V. Le, "EfficientDet: Scalable and efficient object detection," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, Seattle, WA, USA, 2020, pp. 10778–10787, doi: 10.1109/CVPR42600.2020.01079.

**Tổng kết Mục 1:** cả 24/24 tài liệu đều có thật và hợp lệ.

- 0 tài liệu bịa hoặc sai hoàn toàn.
- 6 tài liệu cần sửa hoặc bổ sung chi tiết: [9], [18], [21], [23], [24], cùng tên file trong MANIFEST.
- 3 tài liệu cần lưu ý khi dùng: [7], [14], [20].
- [12] đã xác minh là có thật.

---

## 2. Tóm tắt và mục đích sử dụng (diễn giải bằng lời của người kiểm tra)

| Số cũ | Tóm tắt (2–3 câu) | Dùng ở đâu, cho ý gì |
|---|---|---|
| [1] | Nhóm tác giả công bố 1.000 ảnh nội soi có polyp, kèm mặt nạ pixel do bác sĩ vẽ và chuyên gia duyệt lại. Từ mặt nạ, họ sinh thêm hộp bao. Bài cũng chạy vài mô hình cơ sở để chứng minh dữ liệu dùng được. | Mở đầu, Ch1 (dữ liệu công khai), Ch4 (nguồn 1.000 ảnh polyp, dạng mặt nạ gốc trước khi chuyển sang polygon YOLO). |
| [2] | Bài gộp hai bộ CVC thành một benchmark nội soi có nhãn cho polyp, lòng ruột và vùng phản chiếu. FCN được dùng làm mốc so sánh. Bài cũng nêu tỷ lệ bỏ sót polyp là một hạn chế của nội soi. | Ch1: các bộ dữ liệu khác, khó khăn của ảnh nội soi (phản xạ, tương phản thấp). Ch6: hạn chế do chưa kiểm tra chéo bộ dữ liệu. |
| [3] | PolypGen là bộ dữ liệu thu từ 6 trung tâm, có nhãn phát hiện và phân đoạn được chuyên gia xác nhận. Mục tiêu là đo khả năng tổng quát hóa khi đổi bệnh viện hoặc thiết bị. | Ch1: xu hướng đánh giá đa trung tâm. Ch6, Kết luận: nêu hạn chế (chỉ dùng Kvasir-SEG, không có tập test độc lập) và hướng phát triển. |
| [4] | Bài tổng quan hệ thống hóa các phương pháp phân đoạn polyp theo nhóm: chú ý biên, cơ chế attention, hợp nhất đặc trưng. Bài tổng hợp các bộ dữ liệu và chỉ số đánh giá, đồng thời chỉ ra các thách thức còn mở. | Ch1: khung tổng quan nghiên cứu liên quan, phân loại phương pháp. Ch2: định nghĩa chỉ số Dice/IoU dùng trong lĩnh vực. |
| [5] | U-Net có nhánh mã hóa thu nhỏ để lấy ngữ cảnh và nhánh giải mã đối xứng để khôi phục độ phân giải. Hai nhánh nối với nhau bằng skip connection. Mạng huấn luyện được với ít ảnh nhờ tăng cường dữ liệu. | Ch1, Ch2: kiến trúc encoder–decoder. Ch6: mô hình so sánh U-Net (bản 32 kênh của khóa luận là biến thể, cần nói rõ). |
| [6] | UNet++ thay skip connection đơn của U-Net bằng các đường nối lồng nhau, dày đặc, để thu hẹp khoảng cách ngữ nghĩa giữa encoder và decoder. Mạng có giám sát sâu ở nhiều mức. | Ch1: dòng phát triển của họ U-Net. Ch2: ý tưởng hợp nhất đa mức. |
| [7] | PraNet dùng bộ giải mã cục bộ song song để lấy bản đồ vị trí thô, rồi dùng chú ý ngược để lần lượt tinh chỉnh vùng biên. Mô hình được đánh giá trên 5 bộ dữ liệu polyp. | Ch1, Ch2: phương pháp chuyên cho polyp. Ch6: mô hình so sánh (biến thể ResNet-50, khác bản gốc Res2Net-50). |
| [8] | Polyp-PVT dùng Pyramid Vision Transformer làm encoder. Mô hình có 3 mô-đun: hợp nhất tầng cao, nhận diện polyp "ngụy trang" ở tầng thấp, và lan truyền thông tin tương đồng. | Ch1: hướng dùng Transformer cho polyp. Ch2: so sánh độ phức tạp của attention với SSM. |
| [9] | ColonFormer kết hợp encoder Transformer phân cấp với decoder nhiều mức và mô-đun tinh chỉnh biên, đánh giá trên 5 bộ dữ liệu. Đây là công trình của nhóm tác giả Việt Nam. | Ch1: nghiên cứu trong nước và quốc tế về Transformer cho polyp. |
| [10] | TransFuse chạy song song một nhánh CNN và một nhánh Transformer, rồi trộn hai nhánh bằng mô-đun BiFusion. Cách này vừa giữ chi tiết cục bộ, vừa có ngữ cảnh toàn cục. | Ch1, Ch2: lập luận cần cả ngữ cảnh xa lẫn chi tiết gần, là động cơ để thêm khối toàn cục vào backbone CNN. |
| [11] | YOLO coi phát hiện vật thể là bài toán hồi quy một lần qua mạng, trực tiếp từ ảnh ra hộp bao và xác suất lớp. Nhờ vậy mô hình đạt tốc độ thời gian thực. | Ch1, Ch2: nguồn gốc họ YOLO, triết lý detector một giai đoạn. |
| [12] | Báo cáo kỹ thuật chính thức của YOLO26, mô tả: đầu dự đoán kép cho suy luận không cần NMS, bỏ DFL, bộ tối ưu MuSGD, hàm mất mát tăng dần và cơ chế gán nhãn ưu tiên vật thể nhỏ. Bài có thêm các đầu cho phân đoạn, pose và hộp xoay. | Mở đầu, Ch2 (kiến trúc YOLO26-seg), Ch3 (mô hình đối chứng và vị trí tầng 10), Ch5 (cấu hình). Ghi rõ đây là preprint. |
| [13] | S4 tham số hóa mô hình không gian trạng thái liên tục sao cho tính toán hiệu quả trên chuỗi rất dài. Mô hình xử lý tốt các bài toán cần phụ thuộc xa. | Ch2: nền tảng toán học của SSM (phương trình trạng thái, rời rạc hóa). |
| [14] | Mamba cho các tham số của SSM phụ thuộc vào đầu vào (cơ chế chọn lọc) để mô hình chủ động giữ hoặc bỏ thông tin. Bài kèm thuật toán quét song song tối ưu cho phần cứng, nên chi phí tăng tuyến tính theo độ dài chuỗi. | Ch2: selective scan, độ phức tạp tuyến tính. Ch3: cơ sở của khối VMamba. |
| [15] | VMamba đưa Mamba vào ảnh bằng mô-đun SS2D: quét ảnh theo 4 hướng để biến bản đồ đặc trưng 2D thành các chuỗi 1D, rồi gộp kết quả lại. Mô hình được dùng làm backbone thị giác với chi phí tuyến tính. | Mở đầu, Ch2, Ch3: nguồn trực tiếp của khối SS2D/VSS mà khóa luận tích hợp vào tầng 10. |
| [16] | U-Mamba chèn khối lai CNN–SSM vào khung nnU-Net cho phân đoạn y sinh, và tự cấu hình theo từng bộ dữ liệu. | Ch1: Mamba trong phân đoạn ảnh y tế. |
| [17] | Mamba-UNet dựng kiến trúc dạng U thuần bằng khối Visual Mamba, có skip connection, và thử trên ảnh MRI tim. | Ch1: Mamba trong phân đoạn ảnh y tế. |
| [18] | Swin-UMamba cho thấy khởi tạo encoder Mamba từ trọng số tiền huấn luyện trên ImageNet giúp cải thiện rõ phân đoạn y tế, trong đó có ảnh nội soi. | Ch1: vai trò của tiền huấn luyện. Ch6: bàn về việc TSVM khởi tạo ngẫu nhiên ở tầng 10. |
| [19] | Polyp-Mamba kết hợp Visual Mamba với các mô-đun ngữ nghĩa nhận biết tỉ lệ và tiêm ngữ nghĩa toàn cục để phân đoạn polyp. | Ch1: Mamba áp dụng trực tiếp cho polyp. |
| [20] | PolyMamba bổ sung tiên nghiệm không gian để bù cho kiểu quét cố định của Mamba, và dùng lọc tần số cao có cổng để làm rõ biên polyp. | Ch1: hạn chế của quét cố định, động cơ cho nhánh hình dạng/hướng của khối TSVM (chỉ dùng ở mức gợi ý ý tưởng). |
| [21] | SAM-Mamba gắn mô-đun Mamba vào Segment Anything để tăng khả năng phân đoạn polyp zero-shot trên bộ dữ liệu chưa thấy. | Ch1: xu hướng mô hình nền tảng kết hợp Mamba. |
| [22] | Mamba YOLO thay các khối của YOLO bằng khối SSM (ODSS) để thêm ngữ cảnh toàn cục, và thử trên COCO và VOC. | Ch1, Ch3: tiền lệ gần nhất về việc tích hợp SSM vào YOLO, giúp định vị đóng góp của khóa luận. |
| [23] | FPN tận dụng tháp đặc trưng sẵn có của CNN, thêm đường từ trên xuống và kết nối ngang để mọi tỉ lệ đều có đặc trưng giàu ngữ nghĩa. | Ch2: neck đa tỉ lệ của YOLO (P3–P5). |
| [24] | EfficientDet đề xuất BiFPN có trọng số để trộn đặc trưng hai chiều, kèm phép co giãn phức hợp cho cả mạng. | Ch2: các biến thể neck hợp nhất đa tỉ lệ. |

---

## 3. Tài liệu đề xuất bổ sung (đã xác minh)

Cách xác minh: "CR" là kiểm qua Crossref (DOI phân giải được, metadata khớp), "AX" qua arXiv API, "Web" qua trang chính thức hoặc catalog thư viện. Mã N1–N34 dùng tạm, số chính thức nằm ở Mục 4.

### 3.1. Gánh nặng ung thư đại trực tràng và vai trò của nội soi

- **N1.** F. Bray, M. Laversanne, H. Sung, J. Ferlay, R. L. Siegel, I. Soerjomataram, and A. Jemal, "Global cancer statistics 2022: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries," *CA Cancer J. Clin.*, vol. 74, no. 3, pp. 229–263, 2024, doi: 10.3322/caac.21834.
  - Xác minh: CR.
  - Lý do: số liệu dịch tễ mới nhất của GLOBOCAN.
  - Dùng ở: Mở đầu (lý do chọn đề tài).
  - Phương án thay thế nếu muốn dùng bản 2020: H. Sung *et al.*, *CA Cancer J. Clin.*, vol. 71, no. 3, pp. 209–249, 2021, doi: 10.3322/caac.21660 (CR). Chỉ chọn **một** trong hai.
- **N2.** S. Zhao *et al.*, "Magnitude, risk factors, and factors associated with adenoma miss rate of tandem colonoscopy: A systematic review and meta-analysis," *Gastroenterology*, vol. 156, no. 6, pp. 1661–1674.e11, 2019, doi: 10.1053/j.gastro.2019.01.260.
  - Xác minh: CR.
  - Lý do: định lượng tỷ lệ bỏ sót adenoma qua các nghiên cứu nội soi lặp lại, là động cơ cho hệ hỗ trợ bằng AI.
  - Dùng ở: Mở đầu, Ch1.
- **N3.** D. A. Corley *et al.*, "Adenoma detection rate and risk of colorectal cancer and death," *N. Engl. J. Med.*, vol. 370, no. 14, pp. 1298–1306, 2014, doi: 10.1056/NEJMoa1309086.
  - Xác minh: CR.
  - Lý do: liên hệ giữa tỷ lệ phát hiện adenoma và nguy cơ ung thư hoặc tử vong.
  - Dùng ở: Mở đầu. *Không bắt buộc.*
  - Thay thế khác: J. C. van Rijn *et al.*, "Polyp miss rate determined by tandem colonoscopy: A systematic review," *Am. J. Gastroenterol.*, vol. 101, no. 2, pp. 343–350, 2006, doi: 10.1111/j.1572-0241.2006.00390.x (CR).

### 3.2. Dữ liệu Kvasir v2 (normal-cecum)

- **N4.** K. Pogorelov *et al.*, "KVASIR: A multi-class image dataset for computer aided gastrointestinal disease detection," in *Proc. 8th ACM Multimedia Syst. Conf. (MMSys)*, Taipei, Taiwan, 2017, pp. 164–169, doi: 10.1145/3083187.3083212.
  - Xác minh: CR, cùng trang `datasets.simula.no/kvasir`. Trang này **yêu cầu trích bài này** khi dùng dữ liệu, và chỉ cho phép dùng vào nghiên cứu hoặc giáo dục.
  - Lý do: nguồn của 200 ảnh nền normal-cecum.
  - Dùng ở: Mở đầu, Ch1, Ch4.
  - Lưu ý: trang Simula gọi lớp này là "Cecum" (mốc giải phẫu). Thư mục tải về đặt tên `normal-cecum`. Bài báo không nêu số ảnh của bản v2, nên các con số về v2 phải lấy từ dữ liệu thật.

### 3.3. Xử lý ảnh trong chương dữ liệu

- **N5. (dùng cho Ch2/Ch6)** Xem 3.4 (ResNet).
- **N18.** N. Otsu, "A threshold selection method from gray-level histograms," *IEEE Trans. Syst., Man, Cybern.*, vol. 9, no. 1, pp. 62–66, 1979, doi: 10.1109/TSMC.1979.4310076.
  - Xác minh: CR. Dùng ở: Ch4 (nhị phân hóa mặt nạ).
- **N19.** J. Serra, *Image Analysis and Mathematical Morphology*. London, U.K.: Academic Press, 1982. ISBN: 0-12-637240-3.
  - Xác minh: Web (catalog ĐH Pennsylvania, CiNii).
  - Dùng ở: Ch4 (phép đóng hình thái học). Sách không có DOI.
- **N20.** R. C. Gonzalez and R. E. Woods, *Digital Image Processing*, 4th ed. New York, NY, USA: Pearson, 2018. ISBN: 978-0-13-335672-4.
  - Xác minh: Web (catalog thư viện Đức, trang môn học ĐH Rowan).
  - Dùng ở: Ch2 hoặc Ch4 (giáo trình nền cho ngưỡng, hình thái học, đường biên). Có thể chỉ chọn một trong N19 và N20.
- **N21.** S. Suzuki and K. Abe, "Topological structural analysis of digitized binary images by border following," *Comput. Vis., Graph., Image Process.*, vol. 30, no. 1, pp. 32–46, 1985, doi: 10.1016/0734-189X(85)90016-7.
  - Xác minh: CR. Dùng ở: Ch4 (`cv2.findContours`).
  - **Chú ý:** Crossref có thêm một bản ghi 10.1016/0734-189X(85)90136-7 (vol. 29, tr. 396), đó chỉ là bản tóm tắt. Phải dùng DOI ...90016-7.
- **N22.** D. H. Douglas and T. K. Peucker, "Algorithms for the reduction of the number of points required to represent a digitized line or its caricature," *Cartographica*, vol. 10, no. 2, pp. 112–122, 1973, doi: 10.3138/FM57-6770-U75U-7727.
  - Xác minh: CR. Dùng ở: Ch4 (`cv2.approxPolyDP`).

### 3.4. Kiến trúc và huấn luyện

- **N5.** K. He, X. Zhang, S. Ren, and J. Sun, "Deep residual learning for image recognition," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, Las Vegas, NV, USA, 2016, pp. 770–778, doi: 10.1109/CVPR.2016.90.
  - Xác minh: CR. Dùng ở: Ch2 (kết nối tắt), Ch6 (backbone ResNet-50 của PraNet).
- **N6. (không bắt buộc)** S.-H. Gao, M.-M. Cheng, K. Zhao, X.-Y. Zhang, M.-H. Yang, and P. Torr, "Res2Net: A new multi-scale backbone architecture," *IEEE Trans. Pattern Anal. Mach. Intell.*, vol. 43, no. 2, pp. 652–662, 2021, doi: 10.1109/TPAMI.2019.2938758.
  - Xác minh: CR. Dùng ở: Ch6, khi nói PraNet gốc dùng Res2Net-50 còn khóa luận dùng ResNet-50.
- **N7.** S. Liu, L. Qi, H. Qin, J. Shi, and J. Jia, "Path aggregation network for instance segmentation," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, Salt Lake City, UT, USA, 2018, pp. 8759–8768, doi: 10.1109/CVPR.2018.00913.
  - Xác minh: CR. Dùng ở: Ch2 (đường bottom-up trong neck YOLO).
- **N8.** K. He, G. Gkioxari, P. Dollár, and R. Girshick, "Mask R-CNN," in *Proc. IEEE Int. Conf. Comput. Vis. (ICCV)*, Venice, Italy, 2017, pp. 2980–2988, doi: 10.1109/ICCV.2017.322.
  - Xác minh: CR. Dùng ở: Ch2 (phân đoạn thực thể hai giai đoạn).
- **N9.** D. Bolya, C. Zhou, F. Xiao, and Y. J. Lee, "YOLACT: Real-time instance segmentation," in *Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)*, Seoul, South Korea, 2019, pp. 9156–9165, doi: 10.1109/ICCV.2019.00925.
  - Xác minh: CR. Dùng ở: Ch2, Ch3 (prototype và hệ số mặt nạ của đầu Segment trong YOLO).
- **N10.** A. Vaswani *et al.*, "Attention is all you need," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 30, 2017, pp. 5998–6008.
  - Xác minh: AX (arXiv:1706.03762) và Web (proceedings.neurips.cc).
  - Dùng ở: Ch2 (self-attention, độ phức tạp bậc hai).
- **N11.** A. Dosovitskiy *et al.*, "An image is worth 16x16 words: Transformers for image recognition at scale," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2021. [Online]. Available: https://arxiv.org/abs/2010.11929
  - Xác minh: AX. Dùng ở: Ch2 (ViT).
- **N12. (không bắt buộc)** Z. Liu *et al.*, "Swin Transformer: Hierarchical vision transformer using shifted windows," in *Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)*, Montreal, QC, Canada, 2021, pp. 9992–10002, doi: 10.1109/ICCV48922.2021.00986.
  - Xác minh: CR. Dùng ở: Ch2, nếu nhắc Swin-UMamba [18] hoặc attention theo cửa sổ.
- **N13. (không bắt buộc)** L. Zhu, B. Liao, Q. Zhang, X. Wang, W. Liu, and X. Wang, "Vision Mamba: Efficient visual representation learning with bidirectional state space model," in *Proc. 41st Int. Conf. Mach. Learn. (ICML)*, 2024. [Online]. Available: https://arxiv.org/abs/2401.09417
  - Xác minh: AX (ghi chú tác giả: "accepted by ICML 2024").
  - Dùng ở: Ch2, để phân biệt Vim (quét 2 chiều) với VMamba (quét 4 hướng).
- **N23.** A. Bochkovskiy, C.-Y. Wang, and H.-Y. M. Liao, "YOLOv4: Optimal speed and accuracy of object detection," 2020, *arXiv:2004.10934*.
  - Xác minh: AX. Dùng ở: Ch5 (tăng cường Mosaic, `close_mosaic`).
- **N24.** D. P. Kingma and J. Ba, "Adam: A method for stochastic optimization," in *Proc. 3rd Int. Conf. Learn. Represent. (ICLR)*, San Diego, CA, USA, 2015. [Online]. Available: https://arxiv.org/abs/1412.6980
  - Xác minh: AX. Dùng ở: Ch2, Ch5.
- **N25.** I. Loshchilov and F. Hutter, "Decoupled weight decay regularization," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2019. [Online]. Available: https://arxiv.org/abs/1711.05101
  - Xác minh: AX. Dùng ở: Ch5 (optimizer AdamW).
- **N26.** J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei, "ImageNet: A large-scale hierarchical image database," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, Miami, FL, USA, 2009, pp. 248–255, doi: 10.1109/CVPR.2009.5206848.
  - Xác minh: CR. Dùng ở: Ch2, Ch5 (backbone tiền huấn luyện cho PraNet).
  - Nếu cần nguồn về cuộc thi ILSVRC: O. Russakovsky *et al.*, *Int. J. Comput. Vis.*, vol. 115, no. 3, pp. 211–252, 2015, doi: 10.1007/s11263-015-0816-y (CR).
- **N17.** T.-Y. Lin *et al.*, "Microsoft COCO: Common objects in context," in *Computer Vision – ECCV 2014* (Lecture Notes in Computer Science, vol. 8693). Cham, Switzerland: Springer, 2014, pp. 740–755, doi: 10.1007/978-3-319-10602-1_48.
  - Xác minh: CR. Số tập LNCS 8693 lấy theo hiểu biết chung, Crossref không trả về số tập, nên **cần kiểm lại**. Nếu không kiểm được thì bỏ cụm "vol. 8693".
  - Dùng ở: Ch2 (cách tính mAP50–95 kiểu COCO), Ch5 (trọng số khởi tạo của YOLO26s-seg).
- **N27.** A. Paszke *et al.*, "PyTorch: An imperative style, high-performance deep learning library," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 32, 2019. [Online]. Available: https://arxiv.org/abs/1912.01703
  - Xác minh: AX. Dùng ở: Ch5.
- **N28.** G. Jocher, J. Qiu, and A. Chaurasia, *Ultralytics YOLO*, version 8.4.127. Ultralytics, 2026. [Online]. Available: https://github.com/ultralytics/ultralytics
  - Xác minh:
    - Tác giả lấy từ `CITATION.cff`.
    - Phiên bản 8.4.127 có trên PyPI (23/8/2026, AGPL-3.0) và trùng với fork trong repo.
  - Dùng ở: Ch3, Ch5, để chỉ đúng mã nguồn đã chạy (bổ sung cho [12]).

### 3.5. Chỉ số đánh giá

- **N14.** L. R. Dice, "Measures of the amount of ecologic association between species," *Ecology*, vol. 26, no. 3, pp. 297–302, 1945, doi: 10.2307/1932409.
  - Xác minh: CR. Dùng ở: Ch2, Ch6 (Dice).
- **N15.** P. Jaccard, "The distribution of the flora in the alpine zone," *New Phytol.*, vol. 11, no. 2, pp. 37–50, 1912, doi: 10.1111/j.1469-8137.1912.tb05611.x.
  - Xác minh: CR. Dùng ở: Ch2, Ch6 (IoU, tức hệ số Jaccard).
- **N16.** M. Everingham, L. Van Gool, C. K. I. Williams, J. Winn, and A. Zisserman, "The PASCAL visual object classes (VOC) challenge," *Int. J. Comput. Vis.*, vol. 88, no. 2, pp. 303–338, 2010, doi: 10.1007/s11263-009-0275-4.
  - Xác minh: CR. Crossref ghi ngày online 9/9/2009, năm của số tạp chí là 2010.
  - Dùng ở: Ch2 (AP, đường precision–recall).

### 3.6. Thống kê

- **N29.** Student, "The probable error of a mean," *Biometrika*, vol. 6, no. 1, pp. 1–25, 1908, doi: 10.2307/2331554.
  - Xác minh: CR. Trang đầu là 1. Trang cuối 25 lấy theo hiểu biết chung, nên kiểm lại trên JSTOR.
  - Dùng ở: Ch6 (kiểm định t ghép cặp).
- **N30.** F. Wilcoxon, "Individual comparisons by ranking methods," *Biometrics Bull.*, vol. 1, no. 6, pp. 80–83, 1945, doi: 10.2307/3001968.
  - Xác minh: CR. Trang đầu là 80. Trang cuối 83 lấy theo hiểu biết chung, nên kiểm lại.
  - Dùng ở: Ch6 (Wilcoxon signed-rank).
- **N31.** J. Demšar, "Statistical comparisons of classifiers over multiple data sets," *J. Mach. Learn. Res.*, vol. 7, pp. 1–30, 2006. [Online]. Available: https://www.jmlr.org/papers/v7/demsar06a.html
  - Xác minh: Web (jmlr.org).
  - Dùng ở: Ch6, làm căn cứ chọn Wilcoxon khi so sánh hai mô hình.
- **N32.** X. Bouthillier *et al.*, "Accounting for variance in machine learning benchmarks," in *Proc. Mach. Learn. Syst. (MLSys)*, vol. 3, 2021. [Online]. Available: https://proceedings.mlsys.org/paper_files/paper/2021/hash/0184b0cd3cfb185989f858a1d9f5c1eb-Abstract.html
  - Xác minh: Web, 16 tác giả. Trang proceedings không ghi số trang.
  - Dùng ở: Ch6, để lý giải việc chạy 20 seed và báo cáo phân phối thay vì một lần chạy.
- **N33.** J. Cohen, *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed. Hillsdale, NJ, USA: Lawrence Erlbaum Associates, 1988, doi: 10.4324/9780203771587.
  - Xác minh: Web (WorldCat). DOI kiểm qua CR, trỏ tới bản tái bản của Routledge.
  - Dùng ở: Ch6 (cỡ hiệu ứng *d*), chỉ cần nếu báo cáo effect size.

### 3.7. Màu hình (chỉ khi cần)

- **N34.** B. Wong, "Points of view: Color blindness," *Nat. Methods*, vol. 8, no. 6, p. 441, 2011, doi: 10.1038/nmeth.1618.
  - Xác minh: CR. Năm 2023 có bản Author Correction (10.1038/s41592-023-01974-0).
  - Dùng ở: Ch6, một câu ghi chú về bảng màu Okabe–Ito. *Không bắt buộc.*

### 3.8. Chưa xác minh hoặc không đưa vào danh mục

| Tài liệu | Tình trạng |
|---|---|
| G. **Bradski**, "The OpenCV Library," *Dr. Dobb's J. Softw. Tools*, 2000 (bản trước của báo cáo này ghi nhầm tên là "Bradley") | Diễn đàn OpenCV xác nhận bài đăng ngày 1/11/2000, nhưng Crossref không có bản ghi. Chưa xác minh được tập, số, trang (thường được trích là vol. 25, no. 11, pp. 120–125, nhưng chưa kiểm được). Nếu cần trích OpenCV thì dùng trang tài liệu chính thức (docs.opencv.org) kèm số phiên bản lấy từ môi trường chạy. |
| Okabe & Ito, "Color Universal Design" (trang web) | Chưa kiểm. Dùng N34 thay thế. |
| HarDNet-MSEG (arXiv:2101.07172) | Đã có trên arXiv (Huang, Wu, Lin), nhưng không cần thiết cho khóa luận. Chỉ thêm nếu Ch1 có nhắc đến. |
| FastAPI, Spring Boot, MongoDB, Flutter (cho Ch5) | Đây là tài liệu web, không phải bài báo. Nếu trích thì dạng "[Online]. Available: URL (truy cập ngày …)", ghi số phiên bản lấy từ `pom.xml`, `requirements.txt`, `pubspec.yaml`. Chưa kiểm trong lần này. |
| Mamba [14] trên OpenReview | Trang bị chặn bởi challenge. Hội nghị COLM 2024 chỉ được xác nhận qua nguồn thứ cấp. |

---

### 3.9. Bổ sung đợt 2 (theo yêu cầu của nhóm mô hình), đã xác minh

Các tài liệu này dùng mã tạm N35–N47. Tài liệu YOLACT đã có ở N9, không lặp lại.

- **N35. (quan trọng nhất)** A. Wang, H. Chen, L. Liu, K. Chen, Z. Lin, J. Han, and G. Ding, "YOLOv10: Real-time end-to-end object detection," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 37, 2024, pp. 107984–108011, doi: 10.52202/079017-3429.
  - Xác minh: CR (DOI, trang) và AX 2405.14458 (ghi chú "NeurIPS 2024 Camera-ready Version"). Bài có 7 tác giả, Crossref chỉ trả 6 tác giả đầu; tác giả thứ 7 là G. Ding, lấy theo arXiv.
  - Lý do: nguồn gốc của huấn luyện hai đầu với gán nhãn kép (một-nhiều và một-một) để suy luận không cần NMS, và của khối PSA (partial self-attention). C2PSA ở tầng 10 của YOLO26 kế thừa từ PSA này.
  - Dùng ở: Ch2 (đầu dự đoán end-to-end của YOLO26) và Ch3 (tầng 10 gốc là C2PSA, bị thay bằng khối VMamba).
- **N36.** C. Feng, Y. Zhong, Y. Gao, M. R. Scott, and W. Huang, "TOOD: Task-aligned one-stage object detection," in *Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)*, Montreal, QC, Canada, 2021, pp. 3490–3499, doi: 10.1109/ICCV48922.2021.00349.
  - Xác minh: CR và AX 2108.07755.
  - Dùng ở: Ch2 và Ch3 (TaskAlignedAssigner, bộ gán nhãn dùng khi huấn luyện).
- **N37.** Z. Zheng, P. Wang, W. Liu, J. Li, R. Ye, and D. Ren, "Distance-IoU loss: Faster and better learning for bounding box regression," in *Proc. AAAI Conf. Artif. Intell.*, vol. 34, no. 7, 2020, pp. 12993–13000, doi: 10.1609/aaai.v34i07.6999.
  - Xác minh: CR. Bài này đề xuất cả DIoU lẫn CIoU.
  - Dùng ở: Ch2 (hàm mất mát hộp bao CIoU).
- **N38.** Z. Zheng *et al.*, "Enhancing geometric factors in model learning and inference for object detection and instance segmentation," *IEEE Trans. Cybern.*, vol. 52, no. 8, pp. 8574–8586, 2022, doi: 10.1109/TCYB.2021.3095305.
  - Xác minh: CR.
  - Đây là bản tạp chí mở rộng của CIoU, có áp dụng cho phân đoạn thực thể. Chỉ cần dùng một trong hai bài N37 và N38; nếu chọn một thì ưu tiên N37.
- **N39. (không bắt buộc)** X. Li *et al.*, "Generalized focal loss: Learning qualified and distributed bounding boxes for dense object detection," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 33, 2020. [Online]. Available: https://proceedings.neurips.cc/paper_files/paper/2020/hash/f0bda020d2470f2e74990a07a607ebd9-Abstract.html
  - Xác minh: Web (proceedings NeurIPS) và AX 2006.04388. Chưa kiểm được số trang.
  - Dùng ở: Ch2. Bài này là nguồn của DFL, chỉ cần khi giải thích việc YOLO26 **bỏ** DFL.
- **N40.** A. Gu, K. Goel, A. Gupta, and C. Ré, "On the parameterization and initialization of diagonal state space models," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 35, 2022, pp. 35971–35983, doi: 10.52202/068431-2607.
  - Xác minh: CR. Thứ tự tác giả theo Crossref là Gu, Goel, Gupta, Ré, khác với bản arXiv 2206.11893 (Gu, Gupta, Goel, Ré). Nên dùng thứ tự của bản proceedings.
  - Dùng ở: Ch2 và Ch3. S4D dùng ma trận A chéo và khởi tạo A_log; đây là cơ sở của cách tham số hóa trong Mamba và VMamba.
- **N41.** G. E. Blelloch, "Prefix sums and their applications," School Comput. Sci., Carnegie Mellon Univ., Pittsburgh, PA, USA, Tech. Rep. CMU-CS-90-190, Nov. 1990. [Online]. Available: https://www.cs.cmu.edu/~scandal/papers/CMU-CS-90-190.html
  - Xác minh: Web (trang CMU và KiltHub). Tài liệu không có DOI.
  - Dùng ở: Ch2 (phép quét song song, nền tảng của selective scan).
- **N42.** P. Virtanen *et al.*, "SciPy 1.0: Fundamental algorithms for scientific computing in Python," *Nat. Methods*, vol. 17, no. 3, pp. 261–272, 2020, doi: 10.1038/s41592-019-0686-2.
  - Xác minh: CR.
  - Dùng ở: Ch6 (`scipy.stats.ttest_rel`, `wilcoxon`). Bài này thay cho hai trang tài liệu SciPy mà bản Word cũ trích ở [23] và [24].
- **N43.** D. Lakens, "Calculating and reporting effect sizes to facilitate cumulative science: A practical primer for t-tests and ANOVAs," *Front. Psychol.*, vol. 4, Art. no. 863, 2013, doi: 10.3389/fpsyg.2013.00863.
  - Xác minh: CR xác nhận vol. 4. Số bài 863 suy ra từ DOI.
  - Dùng ở: Ch6, để báo cáo cỡ hiệu ứng *d_z* cho thiết kế ghép cặp 20 seed. Bài này phù hợp với khóa luận; nếu đã dùng Lakens thì có thể bỏ Cohen (N33).

### 3.10. Kiểm tra trích dẫn trong bản Word cũ

Nguồn: `06_bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx`, mục TÀI LIỆU THAM KHẢO, gồm 24 mục, đọc bằng `python-docx`.

#### 3.10.1. Bốn bài không có trong TLTK

Cả bốn bài **đều có thật**. Tuy nhiên hai bài đã được công bố chính thức, nên bản Word cũ cần cập nhật lại.

| Word cũ | Trích dẫn trong Word | Kết quả xác minh | Đề xuất IEEE |
|---|---|---|---|
| [18] | D. Adame và cộng sự, "Topo-VM-UNetV2…," arXiv 2025, 2505.06210 | **Có thật.** Nộp lên arXiv ngày 9/5/2025, 8 tác giả: Adame, Nunez, Vazquez, Gurrola, H. Li, H. Tang, B. Fu, P. Gu. **Đã công bố tại IEEE CBMS 2025**, trang 258–263, DOI 10.1109/CBMS65348.2025.00059 (CR). Word cũ chỉ ghi bản arXiv. | D. Adame *et al.*, "Topo-VM-UNetV2: Encoding topology into vision Mamba UNet for polyp segmentation," in *Proc. IEEE 38th Int. Symp. Comput.-Based Med. Syst. (CBMS)*, 2025, pp. 258–263, doi: 10.1109/CBMS65348.2025.00059. |
| [19] | Y. Wang, J. Wu, J. Song và S. Ren, "CSG-Mamba…," arXiv 2026, 2608.14146 | **Có thật.** Nộp lên arXiv ngày 14/8/2026. Tác giả Yuliang Wang, Jiaqi Wu, Jiaye Song, Shuxia Ren, khớp với Word. Ghi chú tác giả: "Accepted by ICONIP 2026". Crossref chưa có bản proceedings, nên giữ dạng arXiv. | Y. Wang, J. Wu, J. Song, and S. Ren, "CSG-Mamba: A convolutional scoring gating vision state space network for endoscopic polyp segmentation," 2026, *arXiv:2608.14146*. |
| [20] | S.-W. Chan và cộng sự, "MambaPSA: A Mamba-based replacement for C2PSA in YOLO26," arXiv 2026, 2607.12681 | **Có thật.** Nộp lên arXiv ngày 14/7/2026, 7 tác giả: S.-W. Chan, C.-M. Lin, H.-J. Pan, C.-Y. Tsai, C.-H. Yang, Y.-C. Wang, J.-S. Chiang. Chỉ có bản preprint, Crossref không có bản ghi. **Rất liên quan:** đây là công trình gần nhất với khóa luận, vì cũng thay C2PSA của YOLO26 bằng khối Mamba. Phải nêu ở Ch1 và nói rõ khác biệt với TSVM. | S.-W. Chan *et al.*, "MambaPSA: A Mamba-based replacement for C2PSA in YOLO26," 2026, *arXiv:2607.12681*. |
| [21] | T. K. Dutta, S. Majhi, D. R. Nayak và D. Jha, "Mamba Guided Boundary Prior Matters…," 2025, arXiv 2507.01509 | **Có thật.** Ghi chú arXiv: "MICCAI-2025". **Đã công bố tại MICCAI 2025**, LNCS 15970 (cùng tập với PolyMamba), trang 380–391, DOI 10.1007/978-3-032-05141-7_37 (CR). Word cũ chỉ ghi bản arXiv. | T. K. Dutta, S. Majhi, D. R. Nayak, and D. Jha, "Mamba guided boundary prior matters: A new perspective for generalized polyp segmentation," in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2025* (Lecture Notes in Computer Science, vol. 15970). Cham, Switzerland: Springer, 2025, pp. 380–391, doi: 10.1007/978-3-032-05141-7_37. |

Mã tạm cho bốn bài này: Mamba Guided Boundary Prior là N44, Topo-VM-UNetV2 là N45, CSG-Mamba là N46, MambaPSA là N47.

#### 3.10.2. So sánh toàn bộ danh mục Word cũ với 24 tài liệu TLTK

| Word cũ | Nội dung | Có trong TLTK không | Ghi chú lệch |
|---|---|---|---|
| [1] | Kvasir-SEG | Có, là [1] | Khớp. Word ghi "MMM, 2020" nhưng thiếu số tập LNCS 11962. |
| [2] | Pogorelov, Kvasir | Không | Đã đề xuất ở N4. Khớp DOI. |
| [3] | Kvasir-SEG trên Kaggle | Không | Đây là trang phân phối lại dữ liệu, không phải nguồn học thuật. Nên bỏ hoặc chỉ ghi chú, vì nguồn chính là [1]. |
| [4] | Ultralytics docs về dataset segment | Không | Tài liệu web. Chỉ giữ nếu Ch4 mô tả định dạng nhãn YOLO-seg. |
| [5] | Bradski, OpenCV 2000 | Không | Chưa xác minh được tập và trang (xem 3.8). |
| [6]–[9] | Otsu, Gonzalez & Woods, Suzuki–Abe, Douglas–Peucker | Không | Khớp với N18, N20, N21, N22. Word cũ dùng đúng DOI của Suzuki–Abe (…90016-7). |
| [10] | YOLOv4 | Không | Khớp với N23. |
| [11] | Ultralytics docs về augmentation | Không | Tài liệu web, có thể giữ cho Ch5. |
| [12] | U-Net | Có, là [5] | Word chỉ dẫn link arXiv, thiếu DOI Springer và số tập LNCS 9351. |
| [13] | PraNet | Có, là [7] | Word chỉ dẫn link arXiv, thiếu DOI. |
| [14] | Mamba | Có, là [14] | **Lệch:** Word ghi "2023, arXiv", trong khi TLTK ghi COLM 2024. Cần thống nhất một cách ghi (xem 1.2). |
| [15] | VMamba | Có, là [15] | Word chỉ dẫn link arXiv, thiếu tập, trang và DOI NeurIPS. |
| [16] | Trang docs "Ultralytics YOLO26" kèm fork 8.4.127 | Tương ứng [12] | **Lệch:** Word trích trang docs thay vì bài arXiv:2606.03748 (TLTK [12]). Nên trích [12] làm nguồn học thuật, cộng thêm N28 cho phần mềm. |
| [17] | Polyp-Mamba | Có, là [19] | Khớp DOI, nhưng thiếu số tập LNCS 15008 và trang. |
| [18]–[21] | Topo-VM-UNetV2, CSG-Mamba, MambaPSA, Mamba Guided Boundary Prior | Không | Xem 3.10.1. Hai bài [18] và [21] cần cập nhật sang bản đã công bố. |
| [22] | AdamW | Không | Khớp với N25. |
| [23], [24] | Trang docs SciPy `ttest_rel` và `wilcoxon` | Không | Nên thay bằng bài SciPy 1.0 (N42); có thể giữ link docs trong chú thích. |

**Có 17 tài liệu TLTK vắng mặt trong Word cũ:** [2], [3], [4], [6], [8], [9], [10], [11], [13], [16], [17], [18], [20], [21], [22], [23], [24]. Ngoài ra, [12] YOLO26 chỉ được trích qua trang docs chứ không phải bài arXiv.

**Quy cách chưa đúng IEEE trong Word cũ:**
- Dùng "và cộng sự" thay cho "*et al.*".
- Dùng "tr." thay cho "pp.".
- Nhiều bài chỉ ghi link arXiv dù đã có DOI chính thức.

Nếu Khoa cho phép viết bằng tiếng Việt thì "và cộng sự" vẫn chấp nhận được, nhưng phải dùng thống nhất trong toàn bộ danh mục.

---

## 4. Danh mục IEEE cuối cùng, đánh số theo thứ tự xuất hiện dự kiến (cập nhật đợt 2)

**Nguyên tắc đánh số:**
- Số được gán theo lần trích dẫn **đầu tiên** trong toàn bộ báo cáo.
- Thứ tự chương dự kiến: Mở đầu, Ch1, Ch2, Ch3, Ch4, Ch5, Ch6.
- Mục đánh dấu (*) là không bắt buộc. Nếu bỏ mục nào thì phải đánh số lại các mục phía sau.
- Khi viết xong, nên để Zotero hoặc Mendeley sinh lại số tự động.

**Mở đầu**

- [1] F. Bray, M. Laversanne, H. Sung, J. Ferlay, R. L. Siegel, I. Soerjomataram, and A. Jemal, "Global cancer statistics 2022: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries," *CA Cancer J. Clin.*, vol. 74, no. 3, pp. 229–263, 2024, doi: 10.3322/caac.21834.
- [2] S. Zhao *et al.*, "Magnitude, risk factors, and factors associated with adenoma miss rate of tandem colonoscopy: A systematic review and meta-analysis," *Gastroenterology*, vol. 156, no. 6, pp. 1661–1674.e11, 2019, doi: 10.1053/j.gastro.2019.01.260.
- [3]* D. A. Corley *et al.*, "Adenoma detection rate and risk of colorectal cancer and death," *N. Engl. J. Med.*, vol. 370, no. 14, pp. 1298–1306, 2014, doi: 10.1056/NEJMoa1309086.
- [4] D. Jha *et al.*, "Kvasir-SEG: A segmented polyp dataset," in *MultiMedia Modeling (MMM 2020)* (Lecture Notes in Computer Science, vol. 11962). Cham, Switzerland: Springer, 2020, pp. 451–462, doi: 10.1007/978-3-030-37734-2_37.
- [5] K. Pogorelov *et al.*, "KVASIR: A multi-class image dataset for computer aided gastrointestinal disease detection," in *Proc. 8th ACM Multimedia Syst. Conf. (MMSys)*, Taipei, Taiwan, 2017, pp. 164–169, doi: 10.1145/3083187.3083212.
- [6] G. Jocher, J. Qiu, M. Liu, S. Lyu, F. C. Akyon, and M. E. Kalfaoglu, "Ultralytics YOLO26: Unified real-time end-to-end vision models," 2026, *arXiv:2606.03748*, doi: 10.48550/arXiv.2606.03748.
- [7] Y. Liu *et al.*, "VMamba: Visual state space model," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 37, 2024, pp. 103031–103063, doi: 10.52202/079017-3273.

**Chương 1: Tổng quan**

- [8] J. Mei *et al.*, "A survey on deep learning for polyp segmentation: Techniques, challenges and future trends," *Vis. Intell.*, vol. 3, no. 1, Art. no. 1, 2025, doi: 10.1007/s44267-024-00071-w.
- [9] D. Vázquez *et al.*, "A benchmark for endoluminal scene segmentation of colonoscopy images," *J. Healthcare Eng.*, vol. 2017, Art. no. 4037190, 2017, doi: 10.1155/2017/4037190.
- [10] S. Ali *et al.*, "A multi-centre polyp detection and segmentation dataset for generalisability assessment," *Sci. Data*, vol. 10, no. 1, Art. no. 75, 2023, doi: 10.1038/s41597-023-01981-y.
- [11] O. Ronneberger, P. Fischer, and T. Brox, "U-Net: Convolutional networks for biomedical image segmentation," in *Medical Image Computing and Computer-Assisted Intervention – MICCAI 2015* (Lecture Notes in Computer Science, vol. 9351). Cham, Switzerland: Springer, 2015, pp. 234–241, doi: 10.1007/978-3-319-24574-4_28.
- [12] Z. Zhou, M. M. Rahman Siddiquee, N. Tajbakhsh, and J. Liang, "UNet++: A nested U-Net architecture for medical image segmentation," in *Deep Learning in Medical Image Analysis and Multimodal Learning for Clinical Decision Support (DLMIA/ML-CDS 2018)* (Lecture Notes in Computer Science, vol. 11045). Cham, Switzerland: Springer, 2018, pp. 3–11, doi: 10.1007/978-3-030-00889-5_1.
- [13] D.-P. Fan *et al.*, "PraNet: Parallel reverse attention network for polyp segmentation," in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2020* (Lecture Notes in Computer Science, vol. 12266). Cham, Switzerland: Springer, 2020, pp. 263–273, doi: 10.1007/978-3-030-59725-2_26.
- [14] B. Dong, W. Wang, D.-P. Fan, J. Li, H. Fu, and L. Shao, "Polyp-PVT: Polyp segmentation with pyramid vision transformers," *CAAI Artif. Intell. Res.*, vol. 2, Art. no. 9150015, 2023, doi: 10.26599/AIR.2023.9150015.
- [15] N. T. Duc, N. T. Oanh, N. T. Thuy, T. M. Triet, and D. V. Sang, "ColonFormer: An efficient transformer based method for colon polyp segmentation," *IEEE Access*, vol. 10, pp. 80575–80586, 2022, doi: 10.1109/ACCESS.2022.3195241.
- [16] Y. Zhang, H. Liu, and Q. Hu, "TransFuse: Fusing transformers and CNNs for medical image segmentation," in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2021* (Lecture Notes in Computer Science, vol. 12901). Cham, Switzerland: Springer, 2021, pp. 14–24, doi: 10.1007/978-3-030-87193-2_2.
- [17] J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, "You only look once: Unified, real-time object detection," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, Las Vegas, NV, USA, 2016, pp. 779–788, doi: 10.1109/CVPR.2016.91.
- [18] A. Gu, K. Goel, and C. Ré, "Efficiently modeling long sequences with structured state spaces," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2022. [Online]. Available: https://openreview.net/forum?id=uYLFoz1vlAC
- [19] A. Gu and T. Dao, "Mamba: Linear-time sequence modeling with selective state spaces," in *Proc. 1st Conf. Lang. Model. (COLM)*, Philadelphia, PA, USA, 2024. [Online]. Available: https://openreview.net/forum?id=tEYskw1VY2
- [20] J. Ma, F. Li, and B. Wang, "U-Mamba: Enhancing long-range dependency for biomedical image segmentation," 2024, *arXiv:2401.04722*, doi: 10.48550/arXiv.2401.04722.
- [21] Z. Wang, J.-Q. Zheng, Y. Zhang, G. Cui, and L. Li, "Mamba-UNet: UNet-like pure visual Mamba for medical image segmentation," 2024, *arXiv:2402.05079*, doi: 10.48550/arXiv.2402.05079.
- [22] J. Liu *et al.*, "Swin-UMamba: Mamba-based UNet with ImageNet-based pretraining," in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2024* (Lecture Notes in Computer Science, vol. 15009). Cham, Switzerland: Springer, 2024, pp. 615–625, doi: 10.1007/978-3-031-72114-4_59.
- [23] Z. Xu *et al.*, "Polyp-Mamba: Polyp segmentation with visual Mamba," in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2024* (Lecture Notes in Computer Science, vol. 15008). Cham, Switzerland: Springer, 2024, pp. 510–521, doi: 10.1007/978-3-031-72111-3_48.
- [24] R. Fu, S. Hu, X. Zheng, C. Tang, and X. Liu, "PolyMamba: Spatial-prior guided Mamba for polyp segmentation with high-frequency enhancement," in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2025* (Lecture Notes in Computer Science, vol. 15970). Cham, Switzerland: Springer, 2025, pp. 455–465, doi: 10.1007/978-3-032-05141-7_44.
- [25] T. K. Dutta, S. Majhi, D. R. Nayak, and D. Jha, "SAM-Mamba: Mamba guided SAM architecture for generalized zero-shot polyp segmentation," in *Proc. IEEE/CVF Winter Conf. Appl. Comput. Vis. (WACV)*, Tucson, AZ, USA, 2025, pp. 4655–4664, doi: 10.1109/WACV61041.2025.00457.
- [26] T. K. Dutta, S. Majhi, D. R. Nayak, and D. Jha, "Mamba guided boundary prior matters: A new perspective for generalized polyp segmentation," in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2025* (Lecture Notes in Computer Science, vol. 15970). Cham, Switzerland: Springer, 2025, pp. 380–391, doi: 10.1007/978-3-032-05141-7_37.
- [27] D. Adame *et al.*, "Topo-VM-UNetV2: Encoding topology into vision Mamba UNet for polyp segmentation," in *Proc. IEEE 38th Int. Symp. Comput.-Based Med. Syst. (CBMS)*, 2025, pp. 258–263, doi: 10.1109/CBMS65348.2025.00059.
- [28]* Y. Wang, J. Wu, J. Song, and S. Ren, "CSG-Mamba: A convolutional scoring gating vision state space network for endoscopic polyp segmentation," 2026, *arXiv:2608.14146*.
- [29] Z. Wang, C. Li, H. Xu, X. Zhu, and H. Li, "Mamba YOLO: A simple baseline for object detection with state space model," in *Proc. AAAI Conf. Artif. Intell.*, vol. 39, no. 8, 2025, pp. 8205–8213, doi: 10.1609/aaai.v39i8.32885.
- [30] S.-W. Chan *et al.*, "MambaPSA: A Mamba-based replacement for C2PSA in YOLO26," 2026, *arXiv:2607.12681*.

**Chương 2: Cơ sở lý thuyết**

- [31] K. He, X. Zhang, S. Ren, and J. Sun, "Deep residual learning for image recognition," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, Las Vegas, NV, USA, 2016, pp. 770–778, doi: 10.1109/CVPR.2016.90.
- [32]* S.-H. Gao, M.-M. Cheng, K. Zhao, X.-Y. Zhang, M.-H. Yang, and P. Torr, "Res2Net: A new multi-scale backbone architecture," *IEEE Trans. Pattern Anal. Mach. Intell.*, vol. 43, no. 2, pp. 652–662, 2021, doi: 10.1109/TPAMI.2019.2938758.
- [33] T.-Y. Lin, P. Dollár, R. Girshick, K. He, B. Hariharan, and S. Belongie, "Feature pyramid networks for object detection," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, Honolulu, HI, USA, 2017, pp. 936–944, doi: 10.1109/CVPR.2017.106.
- [34] S. Liu, L. Qi, H. Qin, J. Shi, and J. Jia, "Path aggregation network for instance segmentation," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, Salt Lake City, UT, USA, 2018, pp. 8759–8768, doi: 10.1109/CVPR.2018.00913.
- [35] M. Tan, R. Pang, and Q. V. Le, "EfficientDet: Scalable and efficient object detection," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, Seattle, WA, USA, 2020, pp. 10778–10787, doi: 10.1109/CVPR42600.2020.01079.
- [36] K. He, G. Gkioxari, P. Dollár, and R. Girshick, "Mask R-CNN," in *Proc. IEEE Int. Conf. Comput. Vis. (ICCV)*, Venice, Italy, 2017, pp. 2980–2988, doi: 10.1109/ICCV.2017.322.
- [37] D. Bolya, C. Zhou, F. Xiao, and Y. J. Lee, "YOLACT: Real-time instance segmentation," in *Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)*, Seoul, South Korea, 2019, pp. 9156–9165, doi: 10.1109/ICCV.2019.00925.
- [38] A. Wang *et al.*, "YOLOv10: Real-time end-to-end object detection," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 37, 2024, pp. 107984–108011, doi: 10.52202/079017-3429.
- [39] C. Feng, Y. Zhong, Y. Gao, M. R. Scott, and W. Huang, "TOOD: Task-aligned one-stage object detection," in *Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)*, Montreal, QC, Canada, 2021, pp. 3490–3499, doi: 10.1109/ICCV48922.2021.00349.
- [40] Z. Zheng, P. Wang, W. Liu, J. Li, R. Ye, and D. Ren, "Distance-IoU loss: Faster and better learning for bounding box regression," in *Proc. AAAI Conf. Artif. Intell.*, vol. 34, no. 7, 2020, pp. 12993–13000, doi: 10.1609/aaai.v34i07.6999.
- [41]* Z. Zheng *et al.*, "Enhancing geometric factors in model learning and inference for object detection and instance segmentation," *IEEE Trans. Cybern.*, vol. 52, no. 8, pp. 8574–8586, 2022, doi: 10.1109/TCYB.2021.3095305.
- [42]* X. Li *et al.*, "Generalized focal loss: Learning qualified and distributed bounding boxes for dense object detection," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 33, 2020. [Online]. Available: https://proceedings.neurips.cc/paper_files/paper/2020/hash/f0bda020d2470f2e74990a07a607ebd9-Abstract.html
- [43] A. Vaswani *et al.*, "Attention is all you need," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 30, 2017, pp. 5998–6008.
- [44] A. Dosovitskiy *et al.*, "An image is worth 16x16 words: Transformers for image recognition at scale," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2021. [Online]. Available: https://arxiv.org/abs/2010.11929
- [45]* Z. Liu *et al.*, "Swin Transformer: Hierarchical vision transformer using shifted windows," in *Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)*, Montreal, QC, Canada, 2021, pp. 9992–10002, doi: 10.1109/ICCV48922.2021.00986.
- [46]* L. Zhu, B. Liao, Q. Zhang, X. Wang, W. Liu, and X. Wang, "Vision Mamba: Efficient visual representation learning with bidirectional state space model," in *Proc. 41st Int. Conf. Mach. Learn. (ICML)*, 2024. [Online]. Available: https://arxiv.org/abs/2401.09417
- [47] A. Gu, K. Goel, A. Gupta, and C. Ré, "On the parameterization and initialization of diagonal state space models," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 35, 2022, pp. 35971–35983, doi: 10.52202/068431-2607.
- [48] G. E. Blelloch, "Prefix sums and their applications," School Comput. Sci., Carnegie Mellon Univ., Pittsburgh, PA, USA, Tech. Rep. CMU-CS-90-190, Nov. 1990.
- [49] T.-Y. Lin *et al.*, "Microsoft COCO: Common objects in context," in *Computer Vision – ECCV 2014* (Lecture Notes in Computer Science, vol. 8693). Cham, Switzerland: Springer, 2014, pp. 740–755, doi: 10.1007/978-3-319-10602-1_48.
  - Cần kiểm lại số tập 8693.
- [50] M. Everingham, L. Van Gool, C. K. I. Williams, J. Winn, and A. Zisserman, "The PASCAL visual object classes (VOC) challenge," *Int. J. Comput. Vis.*, vol. 88, no. 2, pp. 303–338, 2010, doi: 10.1007/s11263-009-0275-4.
- [51] L. R. Dice, "Measures of the amount of ecologic association between species," *Ecology*, vol. 26, no. 3, pp. 297–302, 1945, doi: 10.2307/1932409.
- [52] P. Jaccard, "The distribution of the flora in the alpine zone," *New Phytol.*, vol. 11, no. 2, pp. 37–50, 1912, doi: 10.1111/j.1469-8137.1912.tb05611.x.
- [53] D. P. Kingma and J. Ba, "Adam: A method for stochastic optimization," in *Proc. 3rd Int. Conf. Learn. Represent. (ICLR)*, San Diego, CA, USA, 2015. [Online]. Available: https://arxiv.org/abs/1412.6980
- [54] I. Loshchilov and F. Hutter, "Decoupled weight decay regularization," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2019. [Online]. Available: https://arxiv.org/abs/1711.05101

**Chương 3: Mô hình đề xuất**

Chương này chủ yếu dùng lại [6], [7], [19], [29], [30], [37], [38] và [47]. Có thêm một mục mới:

- [55] G. Jocher, J. Qiu, and A. Chaurasia, *Ultralytics YOLO*, version 8.4.127. Ultralytics, 2026. [Online]. Available: https://github.com/ultralytics/ultralytics

**Chương 4: Dữ liệu và tiền xử lý**

Chương này dùng lại [4] và [5]. Các mục mới:

- [56] N. Otsu, "A threshold selection method from gray-level histograms," *IEEE Trans. Syst., Man, Cybern.*, vol. 9, no. 1, pp. 62–66, 1979, doi: 10.1109/TSMC.1979.4310076.
- [57]* J. Serra, *Image Analysis and Mathematical Morphology*. London, U.K.: Academic Press, 1982.
- [58] R. C. Gonzalez and R. E. Woods, *Digital Image Processing*, 4th ed. New York, NY, USA: Pearson, 2018.
- [59] S. Suzuki and K. Abe, "Topological structural analysis of digitized binary images by border following," *Comput. Vis., Graph., Image Process.*, vol. 30, no. 1, pp. 32–46, 1985, doi: 10.1016/0734-189X(85)90016-7.
- [60] D. H. Douglas and T. K. Peucker, "Algorithms for the reduction of the number of points required to represent a digitized line or its caricature," *Cartographica*, vol. 10, no. 2, pp. 112–122, 1973, doi: 10.3138/FM57-6770-U75U-7727.

**Chương 5: Cài đặt**

Chương này dùng lại [49], [54] và [55]. Các mục mới:

- [61] A. Bochkovskiy, C.-Y. Wang, and H.-Y. M. Liao, "YOLOv4: Optimal speed and accuracy of object detection," 2020, *arXiv:2004.10934*.
- [62] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei, "ImageNet: A large-scale hierarchical image database," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, Miami, FL, USA, 2009, pp. 248–255, doi: 10.1109/CVPR.2009.5206848.
- [63] A. Paszke *et al.*, "PyTorch: An imperative style, high-performance deep learning library," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 32, 2019. [Online]. Available: https://arxiv.org/abs/1912.01703

**Chương 6: Thực nghiệm và đánh giá**

- [64] X. Bouthillier *et al.*, "Accounting for variance in machine learning benchmarks," in *Proc. Mach. Learn. Syst. (MLSys)*, vol. 3, 2021. [Online]. Available: https://proceedings.mlsys.org/paper_files/paper/2021/hash/0184b0cd3cfb185989f858a1d9f5c1eb-Abstract.html
- [65] Student, "The probable error of a mean," *Biometrika*, vol. 6, no. 1, pp. 1–25, 1908, doi: 10.2307/2331554.
- [66] F. Wilcoxon, "Individual comparisons by ranking methods," *Biometrics Bull.*, vol. 1, no. 6, pp. 80–83, 1945, doi: 10.2307/3001968.
- [67] J. Demšar, "Statistical comparisons of classifiers over multiple data sets," *J. Mach. Learn. Res.*, vol. 7, pp. 1–30, 2006. [Online]. Available: https://www.jmlr.org/papers/v7/demsar06a.html
- [68] P. Virtanen *et al.*, "SciPy 1.0: Fundamental algorithms for scientific computing in Python," *Nat. Methods*, vol. 17, no. 3, pp. 261–272, 2020, doi: 10.1038/s41592-019-0686-2.
- [69] D. Lakens, "Calculating and reporting effect sizes to facilitate cumulative science: A practical primer for t-tests and ANOVAs," *Front. Psychol.*, vol. 4, Art. no. 863, 2013, doi: 10.3389/fpsyg.2013.00863.
- [70]* J. Cohen, *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed. Hillsdale, NJ, USA: Lawrence Erlbaum Associates, 1988, doi: 10.4324/9780203771587.
- [71]* B. Wong, "Points of view: Color blindness," *Nat. Methods*, vol. 8, no. 6, p. 441, 2011, doi: 10.1038/nmeth.1618.

**Bổ sung khi viết Chương 3 (27/10/2026), số tạm, sẽ đánh lại khi chốt danh mục:**

- [72] W. D. Hillis and G. L. Steele Jr., "Data parallel algorithms," *Commun. ACM*, vol. 29, no. 12, pp. 1170–1183, Dec. 1986, doi: 10.1145/7902.7903.
  - Xác minh: DBLP và AcaWiki (sub-agent phản biện Ch.3). Dùng ở: Ch3 mục 3.4.2 (biến thể quét song song trong mã). Theo thứ tự xuất hiện, mục này đứng ngay sau [48].

**Tổng kết danh mục:**
- Tổng cộng **71 mục**, gồm 24 mục cũ và 47 mục mới.
- 10 mục không bắt buộc (*): [3], [28], [32], [41], [42], [45], [46], [57], [70], [71].
- Nếu bỏ cả 10 mục không bắt buộc, danh mục còn **61 mục**.

### 4.1. Bảng ánh xạ số cũ (TLTK [1]–[24]) sang số mới

| Cũ | Mới | | Cũ | Mới | | Cũ | Mới |
|---|---|---|---|---|---|---|---|
| [1] | [4] | | [9] | [15] | | [17] | [21] |
| [2] | [9] | | [10] | [16] | | [18] | [22] |
| [3] | [10] | | [11] | [17] | | [19] | [23] |
| [4] | [8] | | [12] | [6] | | [20] | [24] |
| [5] | [11] | | [13] | [18] | | [21] | [25] |
| [6] | [12] | | [14] | [19] | | [22] | [29] |
| [7] | [13] | | [15] | [7] | | [23] | [33] |
| [8] | [14] | | [16] | [20] | | [24] | [35] |

### 4.2. Ánh xạ mã tạm N sang số mới

| Mã tạm | Mới | Mã tạm | Mới | Mã tạm | Mới |
|---|---|---|---|---|---|
| N1 | [1] | N17 | [49] | N33 | [70] |
| N2 | [2] | N18 | [56] | N34 | [71] |
| N3 | [3] | N19 | [57] | N35 YOLOv10 | [38] |
| N4 | [5] | N20 | [58] | N36 TOOD | [39] |
| N5 | [31] | N21 | [59] | N37 DIoU/CIoU | [40] |
| N6 | [32] | N22 | [60] | N38 CIoU (TCYB) | [41] |
| N7 | [34] | N23 | [61] | N39 GFL | [42] |
| N8 | [36] | N24 | [53] | N40 S4D | [47] |
| N9 | [37] | N25 | [54] | N41 Blelloch | [48] |
| N10 | [43] | N26 | [62] | N42 SciPy | [68] |
| N11 | [44] | N27 | [63] | N43 Lakens | [69] |
| N12 | [45] | N28 | [55] | N44 Mamba Boundary Prior | [26] |
| N13 | [46] | N29 | [65] | N45 Topo-VM-UNetV2 | [27] |
| N14 | [51] | N30 | [66] | N46 CSG-Mamba | [28] |
| N15 | [52] | N31 | [67] | N47 MambaPSA | [30] |
| N16 | [50] | N32 | [64] | | |

### 4.3. Ánh xạ số trong bản Word khóa luận cũ sang số mới

| Word cũ | Mới | Word cũ | Mới |
|---|---|---|---|
| [1] | [4] | [13] | [13] |
| [2] | [5] | [14] | [19] |
| [3] | Bỏ, hoặc chỉ ghi chú link web | [15] | [7] |
| [4] | Tài liệu web; nếu giữ thì thêm vào cuối Ch4 | [16] | [6] và [55] |
| [5] | Chưa xác minh | [17] | [23] |
| [6] | [56] | [18] | [27] |
| [7] | [58] | [19] | [28] |
| [8] | [59] | [20] | [30] |
| [9] | [60] | [21] | [26] |
| [10] | [61] | [22] | [54] |
| [11] | Tài liệu web; nếu giữ thì thêm vào Ch5 | [23], [24] | [68] |
| [12] | [11] | | |

---

## 5. Ghi chú tránh trùng lặp Turnitin khi trích dẫn

1. **Diễn giải, không dịch sát câu.** Đọc xong đoạn gốc thì gấp tài liệu lại, viết theo cấu trúc câu của mình. Đổi cả thứ tự ý (ví dụ nêu kết quả trước, phương pháp sau), không chỉ thay từ đồng nghĩa. Dịch sát từng câu tiếng Anh vẫn có thể bị Turnitin bắt, vì Turnitin có kiểm tra trùng lặp qua bản dịch.
2. **Trích nguyên văn chỉ khi thật cần**, ví dụ định nghĩa hay tên gọi chính thức. Đoạn trích phải ngắn (dưới khoảng 15 từ), đặt trong ngoặc kép và có số [n] ngay sau. Không trích nguyên văn abstract.
3. **Công thức và định nghĩa chuẩn** (Dice, IoU, phương trình SSM, AP) không cần né tránh trùng lặp. Nên viết lại phần lời dẫn quanh công thức và đặt ký hiệu theo cách của mình, khớp với mã nguồn.
4. **Bảng số liệu của bài khác** (ví dụ Dice của PraNet trên Kvasir): nêu một vài con số tiêu biểu kèm [n], không chép nguyên bảng. Phải tách rõ số liệu của tác giả khác với kết quả của khóa luận.
5. **Không tái sử dụng văn bản cũ** (Word, md cũ, bản tóm tắt trong file Word TLTK) cho báo cáo mới, kể cả phần tóm tắt tài liệu trong file Word ở thư mục TLTK, vì các đoạn đó có thể đã nằm trong kho Turnitin.
6. **Danh mục tài liệu tham khảo và trích dẫn trực tiếp có ngoặc kép** thường được loại khỏi phép tính trùng lặp, nếu người nộp bật tùy chọn "Exclude bibliography/quotes". Nên hỏi lại cấu hình mà trường dùng.
7. Chương 4 được giữ nguyên từ `Tien_Xu_Ly_Du_Lieu.docx`. Nếu file này đã từng được nộp lên Turnitin (ví dụ nộp thử), toàn bộ chương có thể bị tính là trùng lặp. Nên kiểm thử sớm.
