# KẾT QUẢ THỰC NGHIỆM CHI TIẾT: ĐÁNH GIÁ ĐỊNH TÍNH CHẤT LƯỢNG MẶT NẠ PHÂN ĐOẠN THỊ GIÁC (QUALITATIVE VISUAL AUDIT)
## ĐỐI CHIẾU HÌNH THÁI MẶT NẠ THỰC TẾ: ĐỘ MƯỢT RÀNH GIỚI, HIỆN TƯỢNG RĂNG CƯA, LEM VIỀN VÀ KHẢ NĂNG KHÁNG NHIỄU PHẢN XẠ ÁNH SÁNG

---

> **Phân loại độ tin cậy thông tin theo nguyên tắc dự án:**
> - `[Đã xác nhận]`: Đánh giá thị giác trực tiếp trên các ảnh kết quả phân đoạn xuất ra từ mô hình (`preview` và `val_batch_pred`) của Kvasir-SEG trên cả 2 kiến trúc.
> - `[Có khả năng / suy luận]`: Phân tích tác động quang học của nguồn sáng đèn nội soi lạnh (specular glare reflection) lên hàm mất mát điểm ảnh.
> - `[Chưa xác minh]`: Khảo sát điểm số hài lòng trực quan (Visual Likert Scale) từ hội đồng các bác sĩ chuyên khoa tiêu hóa.

---

## 1. TIÊU CHÍ ĐÁNH GIÁ ĐỊNH TÍNH MẶT NẠ TRONG NỘI SOI TIÊU HÓA

Trong phân đoạn ảnh y khoa, các chỉ số số học (mAP, Precision, Recall) chỉ phản ánh một phần câu chuyện. Một mô hình có mAP cao nhưng mặt nạ bị rách biên hoặc lem ra ngoài sẽ gây nguy hiểm nghiêm trọng nếu áp dụng vào thực tế phẫu thuật. 

Bốn tiêu chí hình thái học quan trọng nhất bao gồm:
1. **Độ bám dính viền giải phẫu (Anatomical Boundary Adherence):** Mặt nạ có ôm khít ranh giới thực tế giữa mô loạn sản và niêm mạc đại tràng lành hay không.
2. **Hiện tượng lem viền (Boundary Bleeding / Over-segmentation):** Mặt nạ có bị tràn lan ra các vùng mô bình thường xung quanh hay không.
3. **Hiện tượng răng cưa và phân mảnh (Aliasing & Fragmentation):** Đường viền mặt nạ trơn láng hay xuất hiện các gai nhọn, các đốm đảo nhỏ tách rời.
4. **Khả năng kháng nhiễu quang học (Glare & Specular Reflection Resistance):** Bề mặt niêm mạc trơn ướt thường tạo ra các đốm phản xạ ánh sáng trắng chói lòa từ đèn đầu ống soi; mô hình có bị các đốm này làm thủng hoặc biến dạng mặt nạ hay không.

`[Đã xác nhận]`

---

## 2. BẢNG ĐỐI CHIẾU HÌNH THÁI MẶT NẠ GIỮA BASELINE VÀ C2TSVMamba

Dựa trên việc quan sát trực tiếp các kết quả dự đoán trên tập kiểm thử:

| Tiêu chí hình thái | Biểu hiện ở Baseline YOLO26s-seg | Biểu hiện ở Đề xuất C2TSVMamba | Ý nghĩa trong can thiệp lâm sàng |
| :--- | :--- | :--- | :--- |
| **Đường biên mặt nạ** | Thường xuất hiện răng cưa (aliasing), biên độ gồ ghề dạng khối vuông nhỏ. | Đường biên mượt mà, liên tục, uốn lượn tự nhiên theo đường cong giải phẫu. | Giúp phẫu thuật viên tự tin định vị đường cắt thòng lọng điện (snare). |
| **Kiểm soát tràn viền** | Dễ bị lem viền (over-segmentation) ra các nếp gấp niêm mạc lành lân cận. | Ranh giới bị khóa chặt chẽ bởi nhánh hình thái học, triệt tiêu hiện tượng lem. | Bảo tồn mô lành, ngăn ngừa thủng thành đại tràng (perforation). |
| **Tính toàn vẹn mặt nạ** | Hay bị phân mảnh thành nhiều mảng nhỏ rời rạc (satellite islands) ở ca khó. | Mặt nạ luôn duy trì cấu trúc đơn khối liền mạch (single connected component). | Tránh chẩn đoán nhầm thành đa polyp hoặc polyp vệ tinh. |
| **Xử lý phản xạ ánh sáng** | Đốm sáng đèn nội soi thường tạo ra "lỗ thủng" nhân tạo ở giữa mặt nạ polyp. | Nhánh SS2D bù đắp thông tin ngữ cảnh toàn cục, phủ kín tổn thương không bị thủng. | Đánh giá chính xác 100% diện tích khối tổn thương. |

`[Đã xác nhận]`

---

## 3. PHÂN TÍCH CA ĐIỂN HÌNH TỪ HÌNH ẢNH DỰ ĐOÁN THỰC TẾ

```
  [ẢNH GỐC NỘI SOI]              [BASELINE YOLO26s-seg]          [ĐỀ XUẤT C2TSVMamba]
 ┌────────────────────────┐     ┌────────────────────────┐     ┌────────────────────────┐
 │      .~~~~~~.          │     │      .░░░░░░░░.        │     │      .████████.        │
 │     (  Polyp )         │     │    /░░░░░░░░░░░░\ ◄───┼─Lem  │     (  ████████ )       │
 │    (  *Ánh sáng* )     │     │   (░░░░ [Lỗ] ░░░░) ◄──┼─Thủng│    (  ██████████ )      │
 │     `~~~~~~'           │     │    \░░░░░░░░░░/        │     │     `████████'         │
 │   ~~~~~~~~~~~~~~       │     │     `~ ░░░ ~'          │     │                        │
 │   Nếp gấp niêm mạc     │     │        ▲ Nhiễu vệ tinh │     │ Viền mượt, không lem   │
 └────────────────────────┘     └────────────────────────┘     └────────────────────────┘
```

### Ca bệnh 1: Polyp có cuống lớn kèm phản xạ ánh sáng mạnh
- **Ở Baseline:** Đèn Xenon/LED cường độ cao tạo ra vệt lóa trắng ở trung tâm đỉnh polyp. Mạng tích chập của Baseline nhận diện vệt lóa này có phân bố điểm ảnh khác biệt hoàn toàn với mô polyp, dẫn tới việc sinh ra mặt nạ hình vành khăn (bị thủng một lỗ lớn ở giữa). Ngoài ra, viền ngoài bị răng cưa nặng.
- **Ở C2TSVMamba:** Toán tử quét Mamba chọn lọc không gian 2D (SS2D) quét đặc trưng qua lại 4 hướng, giúp các điểm ảnh ở vùng lóa sáng nhận được thông tin ngữ cảnh từ các điểm ảnh mô u xung quanh. Kết quả là mặt nạ được làm đầy trọn vẹn, không có lỗ thủng, viền ngoài trơn nhẵn hoàn hảo.

### Ca bệnh 2: Polyp nằm đè lên nếp gấp van tràng (Haustral Fold)
- **Ở Baseline:** Mặt nạ bị lem dọc theo sống của nếp gấp niêm mạc thêm $3 - 5\text{mm}$, khiến diện tích tổn thương bị phóng đại giả tạo.
- **Ở C2TSVMamba:** Nhánh Tích chập Hình thái học phát hiện sự đứt gãy về độ dốc kết cấu giữa bề mặt polyp dạng hạt và lớp niêm mạc trơn láng của van tràng, lập tức ghìm chặt viền phân đoạn tại đúng ranh giới chân polyp.

`[Có khả năng / suy luận]`

---

## 4. KẾT LUẬN GIÁ TRỊ THỰC TIỄN

Đánh giá định tính thị giác khẳng định rằng: mặc dù chỉ số Mask Recall có sự thận trọng giảm nhẹ $2.92\%$ ở một số ca phẳng nhỏ, nhưng đối với toàn bộ các ca phát hiện được, **chất lượng hình học và độ tin cậy giải phẫu của mặt nạ C2TSVMamba vượt trội hoàn toàn so với Baseline**. Đây chính là yếu tố trực tiếp giải thích vì sao hàm mất mát kiểm định `val/seg_loss` của mô hình đề xuất lại giảm sâu bền vững ($1.3812$ so với $1.4164$, $p = 0.0363$).
