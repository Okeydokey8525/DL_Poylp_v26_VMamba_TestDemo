# Tài liệu nên cân nhắc bổ sung

Đây là đề xuất, chưa sửa danh mục Word. Chỉ bổ sung khi có câu hoặc phân tích cụ thể cần nguồn; không tăng số lượng một cách hình thức.

1. **PolyMamba — MICCAI 2025**: đã có TLTK-20. Dùng để đối chiếu guidance dựa spatial prior/frequency với guidance convolution của TSVM. [Trang hội nghị và BibTeX](https://papers.miccai.org/miccai-2025/0704-Paper3872.html). PDF đã có; không khẳng định repo hoạt động vì URL GitHub được bài dẫn trả404 tại lần mở kiểm toán.
2. **Mamba YOLO — arXiv:2406.05835v2**: đã có TLTK-22. Bổ sung lịch sử SSM trong phát hiện; khác YOLO26 và khác bài toán polyp. [Nguồn gốc](https://arxiv.org/abs/2406.05835).
3. **Hybrid Graph Mamba — MICCAI 2025**: nguồn mới phù hợp nếu cần phân biệt quan hệ graph với directional kernels. Đã kiểm abstract primary; chưa dùng score của bài trong bảng so sánh. [PDF chính thức](https://papers.miccai.org/miccai-2025/paper/1195_paper.pdf).
4. **Ultralytics YOLO26 original paper — arXiv:2606.03748**: đã có TLTK-12, trong khi Word [16] dẫn tài liệu online. Có thể ghi paper và tài liệu implementation thành hai nguồn rõ ràng. [Paper](https://arxiv.org/abs/2606.03748). Không thay cấu hình fork/args thực bằng training recipe của paper.
5. **OpenCV API chính thức** cho `threshold`, `morphologyEx`, `findContours`, `approxPolyDP`: bổ sung locator cho preprocessing, đồng thời ghi phiên bản thực dùng. [Shape API](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html). Bradski2000 là citation phần mềm tổng quát.
6. **SAM-Mamba — WACV2025**: đã có TLTK-21; chỉ thêm nếu cần phân tích tiền thân SAM-based, không nhầm với SAM-MaGuP đang là Word [21]. [CVF PDF](https://openaccess.thecvf.com/content/WACV2025/papers/Dutta_SAM-Mamba_Mamba_Guided_SAM_Architecture_for_Generalized_Zero-Shot_Polyp_Segmentation_WACV_2025_paper.pdf).
7. **MambaPolyp, DOI10.1002/ima.70445**: đầu mối mới từ publisher, kiểm metadata/abstract; chưa rà đầy đủ giao thức/fulltext nên ưu tiên thấp và chưa đưa kết quả vào báo cáo. [Publisher](https://onlinelibrary.wiley.com/doi/10.1002/ima.70445).

Các nguồn gần nhất MambaPSA, CSG-Mamba, Topo-VM-UNetV2, Polyp-Mamba và SAM-MaGuP đã có trong Word; cần giữ đối chiếu đúng phương pháp thay vì trình bày như vừa phát hiện hoàn toàn mới. Bổ sung Dice/Boundary F1/HD95/topology trong tương lai phải kèm định nghĩa phép đánh giá và thí nghiệm thực, không chỉ thêm citation.
