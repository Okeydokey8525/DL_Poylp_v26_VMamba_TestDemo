# D2. Danh sách tải tài liệu tham khảo bổ sung (47 mục mới)

Nguồn đầu vào: `D_tai_lieu_tham_khao.md`, mục 4 (danh mục 71 mục, đánh số mới). 24 mục đã có PDF trong `TLTK\` được bỏ qua: [4], [6]–[25], [29], [33], [35].

Ngày kiểm tra: 27/10/2026. Cách kiểm: gửi yêu cầu HTTP lấy 1 byte (`Range: bytes=0-0`) hoặc HEAD để đọc mã trạng thái, kiểu nội dung và tổng dung lượng. Không tải toàn bộ tệp nào. Trạng thái OA (truy cập mở) được đối chiếu thêm bằng API Unpaywall và API chuyển mã PMC.

**Thư mục đích đề xuất khi tải:** `C:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\TLTK\bo_sung\`

## 1. Tóm tắt

| Loại | Ý nghĩa | Số mục | Các mục |
|---|---|---|---|
| 1 | Truy cập mở, có PDF từ nguồn chính thức | **28** | [1], [5], [28], [30], [31], [34], [36]–[40], [42]–[48], [52]–[55], [61], [63], [64], [67]–[69] |
| 2 | Bản chính thức trả phí, có bản công khai hợp pháp (arXiv, PMC, trang tác giả hoặc trường) | **8** | [3], [26], [27], [32], [41], [49], [50], [62] |
| 3 | Chỉ có bản trả phí hoặc là sách | **11** | [2], [51], [56], [57], [58], [59], [60], [65], [66], [70], [71] |
| | **Tổng** | **47** | 10 mục tùy chọn (*): [3], [28], [32], [41], [42], [45], [46], [57], [70], [71] |

**Dung lượng ước tính (1 MB = 10^6 byte):**
- Loại 1: khoảng **54,4 MB**, tính cho 24 tệp đã đo được. Mục [40] lấy theo bản arXiv vì trang AAAI không trả dung lượng. Chưa đo được [1] và [52] (Wiley chặn truy cập tự động). [55] là phần mềm, không có PDF.
- Loại 2: khoảng **33,1 MB** cho 7 tệp. [3] (PMC) chưa đo được.
- **Tổng loại 1 + 2: khoảng 87,5 MB.** Cộng thêm 3 tệp chưa đo, ước khoảng **90–95 MB**.

**Lưu ý chung:**
- Wiley (onlinelibrary.wiley.com), ACM DL, PMC (tệp PDF) và Elsevier trả mã 403 hoặc trang chống bot khi kiểm bằng script. Mở bằng trình duyệt thì bình thường. Với các link này, cột Ghi chú ghi rõ cách xác minh.
- Link CVF Open Access là bản do CVF công bố hợp pháp, trùng nội dung với bản IEEE Xplore (chỉ khác watermark). Khi trích dẫn vẫn dùng DOI IEEE như trong danh mục.
- Với bản arXiv của bài đã đăng hội nghị hoặc tạp chí (loại 2), nên đối chiếu số trang, số hình, số bảng với bản chính thức trước khi trích chi tiết.

## 2. Bảng chính

| Số mới | Tài liệu (tác giả năm, tiêu đề ngắn) | Loại | Link tải PDF hợp pháp | Link DOI/trang chính thức | Dung lượng | Tên file đề xuất | Ghi chú |
|---|---|---|---|---|---|---|---|
| [1] | Bray 2024, Global cancer statistics 2022 (GLOBOCAN) | 1 | https://onlinelibrary.wiley.com/doi/pdfdirect/10.3322/caac.21834 | https://doi.org/10.3322/caac.21834 | chưa rõ | `[1] Global Cancer Statistics 2022 GLOBOCAN Estimates.pdf` | Unpaywall xác nhận OA gold (bản xuất bản). Script bị 403 do chống bot, mở bằng trình duyệt. |
| [2] | Zhao 2019, Adenoma miss rate of tandem colonoscopy | 3 | không có | https://doi.org/10.1053/j.gastro.2019.01.260 | — | `[2] Magnitude Risk Factors and Factors Associated with Adenoma Miss Rate of Tandem Colonoscopy.pdf` | Unpaywall: closed. DOI chuyển tới Elsevier (PII S0016508519303609). Xem mục 3. |
| [3]* | Corley 2014, Adenoma detection rate and risk of CRC | 2 | https://pmc.ncbi.nlm.nih.gov/articles/PMC4036494/ (PDF: https://pmc.ncbi.nlm.nih.gov/articles/PMC4036494/pdf/nihms-584314.pdf) | https://doi.org/10.1056/NEJMoa1309086 | chưa rõ | `[3] Adenoma Detection Rate and Risk of Colorectal Cancer and Death.pdf` | Bản PMC Author Manuscript (NIHMS), trang đã kiểm đúng tiêu đề. Script không đo được tệp PDF (PMC chống bot). |
| [5] | Pogorelov 2017, KVASIR multi-class GI dataset | 1 | https://doras.dcu.ie/21821/1/Pogorelov_et_al._2017.pdf | https://doi.org/10.1145/3083187.3083212 | 7,96 MB | `[5] KVASIR A Multi-Class Image Dataset for Computer Aided Gastrointestinal Disease Detection.pdf` | Unpaywall: OA gold trên ACM DL (ACM chặn script, 403). Link DORAS (kho của DCU) đã kiểm: PDF, HTTP 206. Đây là bản nộp (submitted version). |
| [26] | Dutta 2025, Mamba guided boundary prior matters (SAM-MaGuP) | 2 | https://arxiv.org/pdf/2507.01509 | https://doi.org/10.1007/978-3-032-05141-7_37 | 1,52 MB | `[26] Mamba Guided Boundary Prior Matters A New Perspective for Generalized Polyp Segmentation.pdf` | Bản chính thức: MICCAI 2025, LNCS 15970 (Springer). |
| [27] | Adame 2025, Topo-VM-UNetV2 | 2 | https://arxiv.org/pdf/2505.06210 | https://doi.org/10.1109/CBMS65348.2025.00059 | 2,60 MB | `[27] Topo-VM-UNetV2 Encoding Topology into Vision Mamba UNet for Polyp Segmentation.pdf` | Bản chính thức: IEEE CBMS 2025. |
| [28]* | Wang 2026, CSG-Mamba | 1 | https://arxiv.org/pdf/2608.14146 | https://arxiv.org/abs/2608.14146 | 3,12 MB | `[28] CSG-Mamba A Convolutional Scoring Gating Vision State Space Network for Endoscopic Polyp Segmentation.pdf` | Trang abs đã kiểm đúng tiêu đề và tác giả (Wang, Wu, Song, Ren). Là preprint. |
| [30] | Chan 2026, MambaPSA | 1 | https://arxiv.org/pdf/2607.12681 | https://arxiv.org/abs/2607.12681 | 0,21 MB | `[30] MambaPSA A Mamba-based Replacement for C2PSA in YOLO26.pdf` | Trang abs đã kiểm đúng tiêu đề. Là preprint. |
| [31] | He 2016, Deep residual learning (ResNet) | 1 | https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf | https://doi.org/10.1109/CVPR.2016.90 | 0,60 MB | `[31] Deep Residual Learning for Image Recognition.pdf` | CVF Open Access. |
| [32]* | Gao 2021, Res2Net | 2 | https://arxiv.org/pdf/1904.01169 | https://doi.org/10.1109/TPAMI.2019.2938758 | 1,49 MB | `[32] Res2Net A New Multi-Scale Backbone Architecture.pdf` | Unpaywall: green, bản arXiv. |
| [34] | Liu 2018, PANet | 1 | https://openaccess.thecvf.com/content_cvpr_2018/papers/Liu_Path_Aggregation_Network_CVPR_2018_paper.pdf | https://doi.org/10.1109/CVPR.2018.00913 | 3,75 MB | `[34] Path Aggregation Network for Instance Segmentation.pdf` | CVF Open Access. |
| [36] | He 2017, Mask R-CNN | 1 | https://openaccess.thecvf.com/content_ICCV_2017/papers/He_Mask_R-CNN_ICCV_2017_paper.pdf | https://doi.org/10.1109/ICCV.2017.322 | 1,96 MB | `[36] Mask R-CNN.pdf` | CVF Open Access. |
| [37] | Bolya 2019, YOLACT | 1 | https://openaccess.thecvf.com/content_ICCV_2019/papers/Bolya_YOLACT_Real-Time_Instance_Segmentation_ICCV_2019_paper.pdf | https://doi.org/10.1109/ICCV.2019.00925 | 4,18 MB | `[37] YOLACT Real-Time Instance Segmentation.pdf` | CVF Open Access. |
| [38] | Wang 2024, YOLOv10 | 1 | https://proceedings.neurips.cc/paper_files/paper/2024/file/c34ddd05eb089991f06f3c5dc36836e0-Paper-Conference.pdf | https://doi.org/10.52202/079017-3429 | 1,21 MB | `[38] YOLOv10 Real-Time End-to-End Object Detection.pdf` | Bản NeurIPS chính thức, trang Abstract đã kiểm đúng tiêu đề. Dự phòng: https://arxiv.org/pdf/2405.14458 (1,35 MB). |
| [39] | Feng 2021, TOOD | 1 | https://openaccess.thecvf.com/content/ICCV2021/papers/Feng_TOOD_Task-Aligned_One-Stage_Object_Detection_ICCV_2021_paper.pdf | https://doi.org/10.1109/ICCV48922.2021.00349 | 3,18 MB | `[39] TOOD Task-Aligned One-Stage Object Detection.pdf` | CVF Open Access. |
| [40] | Zheng 2020, Distance-IoU loss | 1 | https://ojs.aaai.org/index.php/AAAI/article/download/6999/6853 | https://doi.org/10.1609/aaai.v34i07.6999 | chưa rõ (bản arXiv 3,40 MB) | `[40] Distance-IoU Loss Faster and Better Learning for Bounding Box Regression.pdf` | AAAI OJS, HTTP 200, application/pdf. Dự phòng: https://arxiv.org/pdf/1911.08287. |
| [41]* | Zheng 2022, Enhancing geometric factors (CIoU, TCYB) | 2 | https://arxiv.org/pdf/2005.03572 | https://doi.org/10.1109/TCYB.2021.3095305 | 7,30 MB | `[41] Enhancing Geometric Factors in Model Learning and Inference for Object Detection and Instance Segmentation.pdf` | Unpaywall: green, bản arXiv. |
| [42]* | Li 2020, Generalized focal loss | 1 | https://proceedings.neurips.cc/paper_files/paper/2020/file/f0bda020d2470f2e74990a07a607ebd9-Paper.pdf | https://proceedings.neurips.cc/paper_files/paper/2020/hash/f0bda020d2470f2e74990a07a607ebd9-Abstract.html | 1,62 MB | `[42] Generalized Focal Loss Learning Qualified and Distributed Bounding Boxes for Dense Object Detection.pdf` | Bản NeurIPS chính thức. |
| [43] | Vaswani 2017, Attention is all you need | 1 | https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf | https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html | 0,57 MB | `[43] Attention Is All You Need.pdf` | Bản NeurIPS chính thức. |
| [44] | Dosovitskiy 2021, ViT (An image is worth 16x16 words) | 1 | https://arxiv.org/pdf/2010.11929 | https://arxiv.org/abs/2010.11929 | 3,74 MB | `[44] An Image Is Worth 16x16 Words Transformers for Image Recognition at Scale.pdf` | ICLR 2021. Bản arXiv là bản tác giả công bố. |
| [45]* | Liu 2021, Swin Transformer | 1 | https://openaccess.thecvf.com/content/ICCV2021/papers/Liu_Swin_Transformer_Hierarchical_Vision_Transformer_Using_Shifted_Windows_ICCV_2021_paper.pdf | https://doi.org/10.1109/ICCV48922.2021.00986 | 1,39 MB | `[45] Swin Transformer Hierarchical Vision Transformer Using Shifted Windows.pdf` | CVF Open Access. |
| [46]* | Zhu 2024, Vision Mamba (Vim) | 1 | https://raw.githubusercontent.com/mlresearch/v235/main/assets/zhu24f/zhu24f.pdf | https://arxiv.org/abs/2401.09417 | 1,00 MB | `[46] Vision Mamba Efficient Visual Representation Learning with Bidirectional State Space Model.pdf` | Bản PMLR v235 (ICML 2024), lưu trên kho GitHub chính thức của PMLR. Dự phòng: https://arxiv.org/pdf/2401.09417 (1,12 MB). |
| [47] | Gu 2022, S4D (diagonal SSM) | 1 | https://proceedings.neurips.cc/paper_files/paper/2022/file/e9a32fade47b906de908431991440f7c-Paper-Conference.pdf | https://doi.org/10.52202/068431-2607 | 2,03 MB | `[47] On the Parameterization and Initialization of Diagonal State Space Models.pdf` | Bản NeurIPS chính thức, trang Abstract đã kiểm đúng tiêu đề. Dự phòng: https://arxiv.org/pdf/2206.11893. |
| [48] | Blelloch 1990, Prefix sums and their applications | 1 | https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf | https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf | 0,31 MB | `[48] Prefix Sums and Their Applications.pdf` | Trang của tác giả (CMU). Tệp "Ble93" là bản chương sách 1993, mở rộng từ báo cáo CMU-CS-90-190. Nếu trích theo bản này thì nên sửa mục [48] theo chương sách, hoặc ghi chú rõ phiên bản. |
| [49] | Lin 2014, Microsoft COCO | 2 | https://arxiv.org/pdf/1405.0312 | https://doi.org/10.1007/978-3-319-10602-1_48 | 8,07 MB | `[49] Microsoft COCO Common Objects in Context.pdf` | Bản chính thức: ECCV 2014 (Springer). Cần kiểm lại số tập LNCS (8693) theo trang DOI. |
| [50] | Everingham 2010, PASCAL VOC challenge | 2 | http://host.robots.ox.ac.uk/pascal/VOC/pubs/everingham10.pdf | https://doi.org/10.1007/s11263-009-0275-4 | 8,56 MB | `[50] The PASCAL Visual Object Classes VOC Challenge.pdf` | Trang dự án VOC của Đại học Oxford (chuyển tới thor.robots.ox.ac.uk). Bản dự phòng ở kho của Đại học Edinburgh bị chặn script (403). |
| [51] | Dice 1945, Measures of ecologic association | 3 | không có | https://doi.org/10.2307/1932409 | — | `[51] Measures of the Amount of Ecologic Association Between Species.pdf` | Unpaywall: closed (Wiley/ESA và JSTOR). Xem mục 3. |
| [52] | Jaccard 1912, Distribution of the flora in the alpine zone | 1 | https://onlinelibrary.wiley.com/doi/pdfdirect/10.1111/j.1469-8137.1912.tb05611.x | https://doi.org/10.1111/j.1469-8137.1912.tb05611.x | chưa rõ | `[52] The Distribution of the Flora in the Alpine Zone.pdf` | Unpaywall: OA bronze (miễn phí trên trang Wiley). Script bị 403, mở bằng trình duyệt. |
| [53] | Kingma 2015, Adam | 1 | https://arxiv.org/pdf/1412.6980 | https://arxiv.org/abs/1412.6980 | 0,58 MB | `[53] Adam A Method for Stochastic Optimization.pdf` | ICLR 2015. Bản arXiv là bản chính. |
| [54] | Loshchilov 2019, Decoupled weight decay (AdamW) | 1 | https://arxiv.org/pdf/1711.05101 | https://arxiv.org/abs/1711.05101 | 6,06 MB | `[54] Decoupled Weight Decay Regularization.pdf` | ICLR 2019. |
| [55] | Jocher 2026, Ultralytics YOLO (phần mềm, v8.4.127) | 1 | không có PDF | https://github.com/ultralytics/ultralytics | — | (không có PDF; nếu cần lưu bằng chứng thì in trang README hoặc trang release ra PDF) | Phần mềm mã nguồn mở (AGPL-3.0). Kho GitHub trả HTTP 200. |
| [56] | Otsu 1979, Threshold selection from gray-level histograms | 3 | không có | https://doi.org/10.1109/TSMC.1979.4310076 (IEEE Xplore 4310076) | — | `[56] A Threshold Selection Method from Gray-Level Histograms.pdf` | Unpaywall: closed. Xem mục 3. |
| [57]* | Serra 1982, Image Analysis and Mathematical Morphology (sách) | 3 | không có | Không có DOI. Bản ghi thư mục: https://ci.nii.ac.jp/ncid/BA00374208 , https://find.library.upenn.edu/catalog/992182773503681 | — | — | Sách Academic Press, ISBN 0-12-637240-3. Xem mục 3. |
| [58] | Gonzalez và Woods 2018, Digital Image Processing, 4th ed. (sách) | 3 | không có | https://imageprocessingplace.com/DIP-4E/dip4e_how_to_order.htm | — | — | Pearson, ISBN 978-0-13-335672-4, eText 978-0-13-473480-4. Xem mục 3. |
| [59] | Suzuki và Abe 1985, Border following | 3 | không có | https://doi.org/10.1016/0734-189X(85)90016-7 | — | `[59] Topological Structural Analysis of Digitized Binary Images by Border Following.pdf` | Unpaywall: closed (Elsevier). Xem mục 3. |
| [60] | Douglas và Peucker 1973, Line reduction algorithm | 3 | không có | https://doi.org/10.3138/FM57-6770-U75U-7727 | — | `[60] Algorithms for the Reduction of the Number of Points Required to Represent a Digitized Line or Its Caricature.pdf` | Unpaywall: closed (UTP). Xem mục 3. |
| [61] | Bochkovskiy 2020, YOLOv4 | 1 | https://arxiv.org/pdf/2004.10934 | https://arxiv.org/abs/2004.10934 | 3,94 MB | `[61] YOLOv4 Optimal Speed and Accuracy of Object Detection.pdf` | Preprint arXiv, đúng với cách trích trong danh mục. |
| [62] | Deng 2009, ImageNet | 2 | https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf | https://doi.org/10.1109/CVPR.2009.5206848 | 3,51 MB | `[62] ImageNet A Large-Scale Hierarchical Image Database.pdf` | Bản do nhóm tác giả đăng trên trang dự án ImageNet. Bản IEEE trả phí. |
| [63] | Paszke 2019, PyTorch | 1 | https://proceedings.neurips.cc/paper_files/paper/2019/file/bdbca288fee7f92f2bfa9f7012727740-Paper.pdf | https://proceedings.neurips.cc/paper_files/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html | 0,28 MB | `[63] PyTorch An Imperative Style High-Performance Deep Learning Library.pdf` | Bản NeurIPS chính thức. Dự phòng: https://arxiv.org/pdf/1912.01703. |
| [64] | Bouthillier 2021, Accounting for variance in ML benchmarks | 1 | https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf | https://proceedings.mlsys.org/paper_files/paper/2021/hash/0184b0cd3cfb185989f858a1d9f5c1eb-Abstract.html | 0,89 MB | `[64] Accounting for Variance in Machine Learning Benchmarks.pdf` | Bản MLSys chính thức. Dự phòng: https://arxiv.org/pdf/2103.03098. |
| [65] | Student 1908, The probable error of a mean | 3 | không có | https://doi.org/10.2307/2331554 | — | `[65] The Probable Error of a Mean.pdf` | DOI chuyển tới JSTOR. Unpaywall: closed. Bài thuộc phạm vi công cộng về niên đại nhưng chưa tìm thấy bản miễn phí chính thức. Xem mục 3. |
| [66] | Wilcoxon 1945, Individual comparisons by ranking methods | 3 | không có | https://doi.org/10.2307/3001968 | — | `[66] Individual Comparisons by Ranking Methods.pdf` | DOI chuyển tới JSTOR. Unpaywall: closed. Xem mục 3. |
| [67] | Demšar 2006, Statistical comparisons of classifiers | 1 | https://www.jmlr.org/papers/volume7/demsar06a/demsar06a.pdf | https://www.jmlr.org/papers/v7/demsar06a.html | 0,27 MB | `[67] Statistical Comparisons of Classifiers over Multiple Data Sets.pdf` | JMLR, truy cập mở. |
| [68] | Virtanen 2020, SciPy 1.0 | 1 | https://www.nature.com/articles/s41592-019-0686-2.pdf | https://doi.org/10.1038/s41592-019-0686-2 | 1,65 MB | `[68] SciPy 1.0 Fundamental Algorithms for Scientific Computing in Python.pdf` | Nature Methods OA. Dự phòng: PMC7056644 (https://pmc.ncbi.nlm.nih.gov/articles/PMC7056644/), arXiv 1907.10121. |
| [69] | Lakens 2013, Effect sizes primer | 1 | https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2013.00863/pdf | https://doi.org/10.3389/fpsyg.2013.00863 | 0,52 MB | `[69] Calculating and Reporting Effect Sizes to Facilitate Cumulative Science.pdf` | Frontiers OA. Dự phòng: PMC3840331. |
| [70]* | Cohen 1988, Statistical Power Analysis, 2nd ed. (sách) | 3 | không có | https://doi.org/10.4324/9780203771587 | — | — | Routledge/Taylor & Francis, trang sách đã kiểm đúng tiêu đề. Xem mục 3. |
| [71]* | Wong 2011, Points of view: Color blindness | 3 | không có | https://doi.org/10.1038/nmeth.1618 | — | `[71] Points of View Color Blindness.pdf` | Trang Nature Methods đã kiểm đúng tiêu đề. Unpaywall: closed, không có trên PMC. Xem mục 3. |

## 3. Loại 3: cách lấy hợp pháp

Không tìm thấy bản PDF miễn phí hợp pháp cho 11 mục dưới đây. Unpaywall đều trả "closed", và không có bản trên PMC hay arXiv. Không dùng Sci-Hub, LibGen, Z-Library hay bản do người khác tải lên ResearchGate.

**Cách lấy chung:**
- Trước hết hỏi **thư viện trường** (thư viện số, tài khoản truy cập IEEE Xplore, ScienceDirect, JSTOR, Wiley nếu trường có mua).
- Dùng dịch vụ **mượn liên thư viện hoặc cung cấp bản sao bài báo** (ILL/document delivery) qua thư viện.
- Gửi email xin bản tác giả, nếu tác giả còn hoạt động. Cách này dùng được cho [2].
- **JSTOR "Register & Read"**: tạo tài khoản JSTOR cá nhân miễn phí để đọc trực tuyến một số bài mỗi tháng. Cách này có thể dùng cho [51], [65], [66]. Tài khoản do sinh viên tự tạo. Cách này chỉ cho đọc trực tuyến, không cho tải PDF.
- Với khóa luận, các bài kinh điển ([51], [56], [59], [60], [65], [66]) thường chỉ cần trích định nghĩa hoặc công thức. Có thể đọc bản chính thức qua thư viện rồi ghi chú lại trang và công thức, không nhất thiết phải lưu PDF.

| Số mới | Tài liệu | Trang chính thức | Giá (nếu thấy) | Gợi ý cách lấy hợp pháp |
|---|---|---|---|---|
| [2] | Zhao 2019, Gastroenterology | https://doi.org/10.1053/j.gastro.2019.01.260 | chưa thấy (Elsevier, trả theo bài) | Thư viện trường (ScienceDirect hoặc ClinicalKey). Gửi email cho tác giả liên hệ xin bản PDF. Đọc tóm tắt miễn phí trên PubMed. |
| [51] | Dice 1945, Ecology | https://doi.org/10.2307/1932409 | chưa thấy | JSTOR (Register & Read hoặc tài khoản trường), Wiley/ESA qua thư viện, ILL. |
| [56] | Otsu 1979, IEEE TSMC | https://doi.org/10.1109/TSMC.1979.4310076 | chưa thấy (IEEE, trả theo bài) | IEEE Xplore qua tài khoản trường. ILL. |
| [57]* | Serra 1982, sách | Bản ghi thư mục CiNii: https://ci.nii.ac.jp/ncid/BA00374208 | chưa thấy (sách đã cũ, chủ yếu còn bản cũ) | Mượn ở thư viện trường hoặc qua liên thư viện, xem trước trên Google Books, hoặc tìm trong WorldCat. Vì là mục tùy chọn, có thể bỏ và chỉ giữ [58]. |
| [58] | Gonzalez và Woods 2018, sách 4th ed. | https://imageprocessingplace.com/DIP-4E/dip4e_how_to_order.htm (trang Pearson: https://www.pearson.com/en-us/subject-catalog/p/digital-image-processing/P200000003224, HTTP 200 nhưng chưa đọc được giá) | chưa rõ | Thư viện trường (thường có bản in), Google Books xem trước, thuê hoặc mua eText Pearson. |
| [59] | Suzuki và Abe 1985, CVGIP | https://doi.org/10.1016/0734-189X(85)90016-7 | chưa thấy (Elsevier, trả theo bài) | ScienceDirect qua thư viện trường. ILL. |
| [60] | Douglas và Peucker 1973, Cartographica | https://doi.org/10.3138/FM57-6770-U75U-7727 | chưa thấy (UTP Journals) | Thư viện trường, ILL. Nội dung thuật toán cũng được mô tả trong tài liệu OpenCV (`approxPolyDP`), nhưng tài liệu đó không thay thế được bài gốc khi trích dẫn. |
| [65] | Student 1908, Biometrika | https://doi.org/10.2307/2331554 | chưa thấy | JSTOR (Register & Read hoặc tài khoản trường), Oxford Academic qua thư viện. |
| [66] | Wilcoxon 1945, Biometrics Bulletin | https://doi.org/10.2307/3001968 | chưa thấy | JSTOR (Register & Read hoặc tài khoản trường). |
| [70]* | Cohen 1988, sách 2nd ed. | https://doi.org/10.4324/9780203771587 | chưa thấy | Thư viện trường (bản in hoặc eBook Taylor & Francis), Google Books xem trước, ILL. Có thể chỉ trích các ngưỡng d = 0,2/0,5/0,8 qua [69] (Lakens, OA) nếu bỏ mục này. |
| [71]* | Wong 2011, Nature Methods | https://doi.org/10.1038/nmeth.1618 | chưa thấy (Nature, trả theo bài) | Thư viện trường (Nature.com). Bài chỉ có 1 trang, có thể đọc bản chính thức qua thư viện rồi ghi chú lại nội dung cần dùng. |

## 4. Gợi ý thao tác khi tải

1. Tạo thư mục `C:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\TLTK\bo_sung\`.
2. Tải loại 1 và loại 2 theo cột "Link tải PDF hợp pháp" bằng trình duyệt, vì Wiley, ACM và PMC chặn công cụ tự động. Lưu với tên ở cột "Tên file đề xuất".
3. Với các mục có link dự phòng ([38], [40], [46], [47], [63], [64], [68], [69]), ưu tiên bản chính thức, chỉ dùng arXiv hoặc PMC khi bản chính thức không mở được.
4. Với [48], sửa thông tin trích dẫn cho khớp phiên bản tải về (chương sách 1993 hay báo cáo kỹ thuật 1990).
5. Cập nhật `MANIFEST.txt` sau khi tải xong, nếu nhóm vẫn dùng tệp này.
