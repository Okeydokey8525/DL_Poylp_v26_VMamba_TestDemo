<!-- HISTORICAL_DRAFT_DO_NOT_BUILD_CURRENT -->
> **BẢN THẢO LỊCH SỬ — KHÔNG DÙNG ĐỂ SINH LẠI WORD HIỆN TẠI.** Nhãn cập nhật26/10/2026. Nội dung dưới đây chưa đồng bộ bộ20seedFP32 và có các phát biểu/số liệu đã bị kiểm toán thay thế. Bản Word chính cùng nguồn hiện tại được chỉ rõ tại [doc/README](../../doc/README.md) và [CURRENT_PROJECT_STATUS](../../doc/CURRENT_PROJECT_STATUS.md). Giữ bản thảo để truy vết, không đổi tên N10 thành N20 hoặc sử dụng TN/Dice/GPUclaim cũ như kết quả đã đo.

# TÀI LIỆU THAM KHẢO

---

*(Danh mục làm việc theo dạng IEEE. Chỉ giữ trong bản nộp những nguồn thực sự được trích dẫn; xem bảng tuyển chọn tại `../LUA_CHON_VA_BO_SUNG_TAI_LIEU_THAM_KHAO.md`. Số [1]–[15] được giữ để thuận tiện đối chiếu bản thảo; cần đánh số lại theo thứ tự xuất hiện sau khi chốt nội dung.)*

[1] D. Jha et al., “Kvasir-SEG: A Segmented Polyp Dataset,” in *MultiMedia Modeling (MMM 2020)*, Lecture Notes in Computer Science, vol. 11962, Springer, Cham, 2020, pp. 451–462. DOI: [10.1007/978-3-030-37734-2_37](https://doi.org/10.1007/978-3-030-37734-2_37).

[2] A. Gu and T. Dao, “Mamba: Linear-Time Sequence Modeling with Selective State Spaces,” in *First Conference on Language Modeling (COLM)*, 2024. [Online]. Available: [OpenReview](https://openreview.net/forum?id=tEYskw1VY2); [bản arXiv, công bố đầu tiên năm 2023](https://arxiv.org/abs/2312.00752).

[3] L. Zhu et al., “Vision Mamba: Efficient Visual Representation Learning with Bidirectional State Space Model,” in *Proceedings of the 41st International Conference on Machine Learning*, PMLR, vol. 235, 2024, pp. 62429–62442. [Online]. Available: [PMLR](https://proceedings.mlr.press/v235/zhu24f.html).

[4] Y. Liu et al., “VMamba: Visual State Space Model,” in *Advances in Neural Information Processing Systems (NeurIPS 2024)*, vol. 37, 2024. [Online]. Available: [https://arxiv.org/abs/2401.10166](https://arxiv.org/abs/2401.10166).

[5] Z. Xu et al., “Polyp-Mamba: Polyp Segmentation with Visual Mamba,” in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2024*, Lecture Notes in Computer Science, vol. 15008, Springer, Cham, 2024, pp. 510–521. DOI: [10.1007/978-3-031-72111-3_48](https://doi.org/10.1007/978-3-031-72111-3_48).

[6] G. Jocher et al., “Ultralytics YOLO26: Unified Real-Time End-to-End Vision Models,” *arXiv preprint arXiv:2606.03748*, 2026. DOI: [10.48550/arXiv.2606.03748](https://arxiv.org/abs/2606.03748).

[7] Ultralytics, “Ultralytics YOLO26,” *Ultralytics Documentation*. [Online]. Available: [tài liệu YOLO26](https://docs.ultralytics.com/models/yolo26). [Truy cập: 12/10/2026].

[8] Simula Research Laboratory, “Kvasir-SEG,” dataset website. [Online]. Available: [trang dữ liệu Kvasir-SEG](https://datasets.simula.no/kvasir-seg/). *(Trang chưa truy cập lại thành công trong lần rà soát 12/10/2026; dùng [1] làm nguồn học thuật chính.)*

[9] O. Ronneberger, P. Fischer, and T. Brox, “U-Net: Convolutional Networks for Biomedical Image Segmentation,” in *Medical Image Computing and Computer-Assisted Intervention – MICCAI 2015*, LNCS, vol. 9351, Springer, Cham, 2015, pp. 234–241.

[10] D.-P. Fan, G.-P. Ji, T. Zhou, G. Chen, H. Fu, J. Shen, and L. Shao, “PraNet: Parallel Reverse Attention Network for Polyp Segmentation,” in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2020*, LNCS, vol. 12266, Springer, Cham, 2020, pp. 263–273.

[11] C.-H. Huang, H.-Y. Wu, and Y.-L. Lin, “HarDNet-MSEG: A Simple Encoder-Decoder Polyp Segmentation Neural Network that Achieves over 0.9 Mean Dice and 86 FPS,” *arXiv preprint arXiv:2101.07172*, 2021. [Online]. Available: [https://arxiv.org/abs/2101.07172](https://arxiv.org/abs/2101.07172).

[12] B. Dong et al., “Polyp-PVT: Polyp Segmentation with Pyramid Vision Transformers,” *CAAI Artificial Intelligence Research*, vol. 2, Art. no. 9150015, 2023. DOI: [10.26599/AIR.2023.9150015](https://doi.org/10.26599/AIR.2023.9150015). Bản tiền công bố: [arXiv:2108.06932](https://arxiv.org/abs/2108.06932), 2021.

[13] D. Bolya, C. Zhou, F. Xiao, and Y. J. Lee, “YOLACT: Real-time Instance Segmentation,” in *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, 2019, pp. 9157–9166.

[14] K. Pogorelov et al., “Kvasir: A Multi-Class Image Dataset for Computer Aided Gastrointestinal Disease Detection,” in *Proceedings of the 8th ACM on Multimedia Systems Conference (MMSys '17)*, 2017, pp. 164–169. DOI: [10.1145/3083187.3083212](https://doi.org/10.1145/3083187.3083212).

[15] J. Bernal, F. J. Sánchez, G. Fernández-Esparrach, D. Gil, C. Rodríguez, and F. Vilariño, “WM-DOVA Maps for Accurate Polyp Highlighting in Colonoscopy: Validation vs. Saliency Maps from Physicians,” *Computerized Medical Imaging and Graphics*, vol. 43, pp. 99–111, 2015.

[16] J. Mei et al., “A survey on deep learning for polyp segmentation: techniques, challenges and future trends,” *Visual Intelligence*, vol. 3, Art. no. 1, 2025. DOI: [10.1007/s44267-024-00071-w](https://doi.org/10.1007/s44267-024-00071-w).

[17] Z. Wang, C. Li, H. Xu, X. Zhu, and H. Li, “Mamba YOLO: A Simple Baseline for Object Detection with State Space Model,” in *Proceedings of the AAAI Conference on Artificial Intelligence*, vol. 39, no. 8, 2025, pp. 8205–8213. DOI: [10.1609/aaai.v39i8.32885](https://doi.org/10.1609/aaai.v39i8.32885).

[18] R. Fu, S. Hu, X. Zheng, C. Tang, and X. Liu, “PolyMamba: Spatial-prior Guided Mamba for Polyp Segmentation with High-Frequency Enhancement,” in *Medical Image Computing and Computer Assisted Intervention – MICCAI 2025*, LNCS, vol. 15970, 2025, pp. 455–465. DOI: [10.1007/978-3-032-05141-7_44](https://doi.org/10.1007/978-3-032-05141-7_44). [Online]. Available: [MICCAI 2025](https://papers.miccai.org/miccai-2025/0704-Paper3872.html).

[19] T.-Y. Lin et al., “Feature Pyramid Networks for Object Detection,” in *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2017, pp. 2117–2125. [Online]. Available: [bài báo](https://arxiv.org/abs/1612.03144).

[20] S. Liu, L. Qi, H. Qin, J. Shi, and J. Jia, “Path Aggregation Network for Instance Segmentation,” in *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2018, pp. 8759–8768. [Online]. Available: [bài báo](https://arxiv.org/abs/1803.01534).

[21] N. Otsu, “A Threshold Selection Method from Gray-Level Histograms,” *IEEE Transactions on Systems, Man, and Cybernetics*, vol. 9, no. 1, pp. 62–66, 1979. DOI: [10.1109/TSMC.1979.4310076](https://doi.org/10.1109/TSMC.1979.4310076).

[22] S. Suzuki and K. Abe, “Topological Structural Analysis of Digitized Binary Images by Border Following,” *Computer Vision, Graphics, and Image Processing*, vol. 30, no. 1, pp. 32–46, 1985. DOI: [10.1016/0734-189X(85)90016-7](https://doi.org/10.1016/0734-189X(85)90016-7).

[23] D. H. Douglas and T. K. Peucker, “Algorithms for the Reduction of the Number of Points Required to Represent a Digitized Line or Its Caricature,” *The Canadian Cartographer*, vol. 10, no. 2, pp. 112–122, 1973. DOI: [10.3138/FM57-6770-U75U-7727](https://doi.org/10.3138/FM57-6770-U75U-7727).

[24] OpenCV, “Image Processing,” *OpenCV Documentation, 4.x*. [Online]. Available: [tài liệu xử lý ảnh](https://docs.opencv.org/4.x/d7/dbd/group__imgproc.html). [Truy cập: 12/10/2026].

[25] Ultralytics, “Instance Segmentation Datasets Overview,” *Ultralytics Documentation*. [Online]. Available: [định dạng dữ liệu segmentation](https://docs.ultralytics.com/datasets/segment/). [Truy cập: 12/10/2026].

[26] Ultralytics, “YOLO Data Augmentation,” *Ultralytics Documentation*. [Online]. Available: [tài liệu tăng cường dữ liệu](https://docs.ultralytics.com/guides/yolo-data-augmentation/). [Truy cập: 12/10/2026].

[27] FastAPI, “Request Files,” *FastAPI Documentation*. [Online]. Available: [tải tệp qua API](https://fastapi.tiangolo.com/tutorial/request-files/). [Truy cập: 12/10/2026].

[28] Spring, “Spring Boot,” *Spring Boot Reference Documentation*. [Online]. Available: [tài liệu Spring Boot](https://docs.spring.io/spring-boot/index.html). [Truy cập: 12/10/2026].

[29] MongoDB, “Data Modeling,” *MongoDB Manual*. [Online]. Available: [mô hình hóa dữ liệu](https://www.mongodb.com/docs/manual/data-modeling/). [Truy cập: 12/10/2026].

[30] Flutter, “Networking,” *Flutter Documentation*. [Online]. Available: [giao tiếp mạng](https://docs.flutter.dev/data-and-backend/networking). [Truy cập: 12/10/2026].

[31] Nguyen Thanh Duc, Nguyen Thi Oanh, Nguyen Thi Thuy, Tran Minh Triet, and Dinh Viet Sang, “ColonFormer: An Efficient Transformer Based Method for Colon Polyp Segmentation,” *IEEE Access*, vol. 10, pp. 80575–80586, 2022. DOI: [10.1109/ACCESS.2022.3195241](https://doi.org/10.1109/ACCESS.2022.3195241). [Online]. Available: [bản arXiv](https://arxiv.org/abs/2205.08473).
