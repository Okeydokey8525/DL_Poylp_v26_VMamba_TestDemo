# BÁO CÁO ĐẶC TẢ HƯỚNG NGHIÊN CỨU — TÀI LIỆU THIẾT KẾ

> [!IMPORTANT]
> Đây là **đặc tả hướng nghiên cứu**, không phải snapshot implementation hiện tại.
>
> Repository hiện có implementation TSVM tại Layer 10/P5 trong `archive/ultralytics_Topology-Shape-aware VMamba/`. Các hướng khác, bao gồm P3/C3k2VSS, chỉ được xem là hiện hành sau khi source/config tương ứng được push và xác minh trên GitHub.
>
> Dataset và kết quả thực nghiệm hiện tại được ưu tiên theo `CURRENT_PROJECT_STATUS.md` và raw artifact trong `archive/Ket_Qua_V2/`.

## 1. Bối cảnh đề tài

Đề tài tổng thể:

**“Nghiên cứu phương pháp tích hợp VMamba vào mô hình YOLO26-seg trong phân đoạn polyp từ ảnh nội soi đại trực tràng.”**

Bài toán chính là **instance segmentation polyp** trên ảnh nội soi đại trực tràng.

Các metric quan tâm gồm Dice, IoU, Precision, Recall, F1-score, mask mAP50, mask mAP50-95 và chi phí tính toán.

> **Phân biệt trạng thái:** Nội dung các mục sau mô tả thiết kế/giả thuyết của hướng Topology-Shape-aware VMamba. Không được dùng tài liệu này một mình để kết luận module nào đang chạy ở GitHub.

## 2. Vấn đề nghiên cứu

YOLO26-seg có khả năng phát hiện và phân đoạn đối tượng. Đối với polyp, các khó khăn chính gồm hình dạng đa dạng, biên mờ, ánh sáng phản chiếu, texture phức tạp và nhu cầu khai thác ngữ cảnh không gian rộng.

VMamba được nghiên cứu để khai thác thông tin không gian và ngữ cảnh dài hạn.

## 3. Ý tưởng Topology-Shape-aware VMamba

Hướng thiết kế này kết hợp:

1. **VMamba branch** — khai thác context/SS2D.
2. **Shape-aware branch** — tập trung hình dạng, biên, hướng và cấu trúc cục bộ.
3. **Topology-aware mechanism** — hướng tới tính liên thông/cấu trúc của vùng phân đoạn.

Các thành phần này được nghiên cứu để tạo feature fusion, gating/modulation và residual refinement.

## 4. Shape và Topology

**Shape** tập trung vào hình dạng, đường biên, độ cong, hướng và cấu trúc cục bộ.

**Topology** tập trung vào tính liên thông, connected components, lỗ/hole và cấu trúc kết nối.

Không được đồng nhất hai khái niệm.

## 5. Vai trò của VMamba

VMamba/SS2D được sử dụng để mô hình hóa quan hệ không gian và context dài hạn trên feature map.

Trong implementation TSVM hiện có của repository, source thực tế cần được xem tại:

`archive/ultralytics_Topology-Shape-aware VMamba/nn/modules/topology_shape_vmamba.py`

## 6. Topology không được chỉ là tên gọi

Nếu implementation chỉ có directional convolution, gradient, shape feature và gating thì không nên tuyên bố đã giải quyết topology theo nghĩa chặt.

Nếu nghiên cứu topology-aware loss, connectivity constraint, skeleton/centerline, connected-component consistency, Euler characteristic hoặc persistent homology, phải mô tả đúng cơ chế thực tế và có metric/ablation chứng minh.

## 7. Kiến trúc TSVM đã có trong repository

Implementation hiện có:

`archive/ultralytics_Topology-Shape-aware VMamba/nn/modules/topology_shape_vmamba.py`

Config:

`archive/ultralytics_Topology-Shape-aware VMamba/cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml`

Theo snapshot đã xác minh, `C2TSVMamba` được tích hợp tại **Layer 10/P5**.

Đây là thông tin implementation; các sơ đồ thiết kế trong tài liệu này chỉ có giá trị khi khớp source thực tế.

## 8. Thiết kế thực nghiệm

Đặc tả này đề xuất ablation theo các thành phần:

- YOLO26-seg baseline
- YOLO26 + VMamba
- YOLO26 + Shape
- YOLO26 + VMamba + Shape
- YOLO26 + VMamba + Shape + Topology

Đây là **thiết kế/giả thuyết nghiên cứu**, không phải tuyên bố rằng tất cả các biến thể trên đã được huấn luyện trong repository.

## 9. Kiểm soát tính công bằng

Các mô hình so sánh cần giữ nhất quán dataset, split, imgsz, batch, epochs, optimizer, learning rate, augmentation, seed, hardware và evaluation protocol; thay đổi chính nên là kiến trúc đang được kiểm tra.

## 10. Quy tắc khi tiếp tục triển khai

1. Không thay đổi baseline nếu chưa có lý do nghiên cứu.
2. Xác định rõ vị trí module trong architecture.
3. Giữ tensor shape/channel tương thích.
4. Không gọi topology-aware đầy đủ nếu source không có cơ chế topology tương ứng.
5. Có baseline và ablation phù hợp.
6. Không kết luận dựa trên ý tưởng; kết luận phải dựa trên artifact thực nghiệm.
7. Phân biệt Current/Verified với Historical/Proposed.
8. Khi code mới tồn tại ở local/Kaggle nhưng chưa push, ghi rõ **NOT VERIFIED IN REPOSITORY**.

## 11. Tài liệu nguồn trạng thái

Để biết repository hiện chạy/đang có gì, đọc:

`CURRENT_PROJECT_STATUS.md`

và:

`archive/doc/CURRENT_PROJECT_STATUS.md`

Raw artifact được ưu tiên hơn diễn giải trong tài liệu khi có xung đột.
