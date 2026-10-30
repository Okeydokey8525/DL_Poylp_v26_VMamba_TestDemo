# I. Kế hoạch rút gọn tài liệu tham khảo: 80 → 57

Ngày lập: 30/10/2026. **Chưa triển khai**, chờ chủ dự án duyệt.

- Căn cứ: đề xuất ban đầu, kiểm tra chéo của subagent, và đối chiếu lại từng câu trích trong các chương.
- Số [n] trong file này là **số hiện tại** (bản 80 tài liệu).
- Số dòng lấy theo file ngày 30/10/2026.

## 1. Danh sách bỏ (23 tài liệu)

| Số | Tài liệu | Lý do |
|---|---|---|
| [12] | EndoScene (Vázquez 2017) | Trùng vai trò với [11]; trong Bảng 1.1 chỉ ghi "Tham khảo" |
| [17] | UNet++ | Nhánh CNN đã có U-Net [10] và PraNet [9] |
| [20] | TransFuse | Nhánh Transformer đã có Polyp-PVT [18] và ColonFormer [19] |
| [27] | Vision Mamba (Vim) | Chỉ là nền cho VMamba [7] |
| [29] | Mamba-UNet | Bản arXiv; ý "Mamba cho ảnh y tế" đã có [28], [30], [31] |
| [33] | SAM-Mamba | 14 trích dẫn, vai trò phụ |
| [34] | SAM-MaGuP | Vai trò trùng với [32], [35] |
| [36] | CSG-Mamba | Bản arXiv, 0 trích dẫn |
| [41] | BlazeNeo | Mục 1.6 đã có [19], [40], [42] |
| [43] | PolyPVT-MambaNet | LNNS, 0 trích dẫn |
| [44] | ResNet | Kiến thức phổ thông |
| [52] | Adam | Bài AdamW [51] đã mô tả Adam |
| [53] | GFL/DFL | Việc YOLO26 bỏ DFL đã có trong [6] |
| [57] | ViT | Nền phụ |
| [58] | Swin Transformer | Nền phụ |
| [62] | Jaccard 1912 | Chỉ nêu nguồn gốc tên gọi |
| [63] | Dice 1945 | Chỉ nêu nguồn gốc tên gọi |
| [69] | Cohen 1988 | Quy ước đã được Lakens [68] trình bày lại |
| [72] | Trang Ultralytics: định dạng nhãn | Gộp vào [55] |
| [77] | Trang Ultralytics: tăng cường dữ liệu | Gộp vào [55] |
| [73] | OpenCV (Dr. Dobb's) | Phần mềm; giữ tên thư viện, bỏ số trích |
| [78] | PyTorch | Phần mềm; giữ tên thư viện, bỏ số trích |
| [79] | SciPy | Phần mềm; giữ tên thư viện, bỏ số trích |

**Không bỏ** (subagent chỉ ra, đã đối chiếu đúng):
- [59] S4D: Ch.3 dòng 189, 460.
- [61] Hillis–Steele: Ch.3 dòng 344, là thuật toán đề tài đã cài.
- [48] TOOD: Ch.2 dòng 86, Ch.3 dòng 480.
- [49] CIoU: Ch.2 dòng 88, Ch.3 dòng 492.
- [67] Demšar: Ch.2 dòng 382, Ch.6 dòng 59.
- [30] Swin-UMamba: Ch.1 dòng 103, Ch.2 dòng 272.
- [32] PolyMamba, [24] Pacal, [11] khảo sát, [45] Mask R-CNN, [42] YOLOv8 trong nước.

## 2. Các câu cần sửa (31 chỗ, 7 file)

### Chương 1: `02_CHUONG_1_TONG_QUAN.md` (13 chỗ)

| Dòng | Hiện tại | Sửa thành |
|---|---|---|
| 31 | "Các khảo sát về phân đoạn polyp [11] và các bộ dữ liệu chuẩn [12] nêu một số khó khăn chung:" | "Các khảo sát về phân đoạn polyp [11] nêu một số khó khăn chung:" |
| 51 | Dòng bảng "Bộ chuẩn CVC (EndoScene) [12] …" | Xóa cả dòng |
| 65 | Câu "**UNet++** [17] thay các kết nối tắt đơn…" | Xóa câu |
| 76 | Gạch đầu dòng "**TransFuse** [20] …" | Xóa gạch đầu dòng |
| 94–96 | "Hai cách đưa Mamba vào ảnh được dùng nhiều:" + gạch "Vision Mamba (Vim) [27]…" + gạch "VMamba [7]…" | Gộp thành một đoạn: "Để đưa Mamba vào ảnh, VMamba [7] đề xuất mô-đun SS2D, …" (giữ nguyên nội dung câu VMamba) |
| 102 | Gạch đầu dòng "**Mamba-UNet** [29] …" | Xóa |
| 108 | Gạch đầu dòng "**SAM-Mamba** [33] và **SAM-MaGuP** [34] …" | Xóa |
| 110 | Gạch đầu dòng "**CSG-Mamba** [36] …" | Xóa |
| 113 | "Nhiều công trình [32], [34], [35] bổ sung thông tin biên, tần số cao hoặc tô-pô…" | "Các công trình [32], [35] bổ sung thông tin biên, tần số cao hoặc tô-pô…" |
| 130 | Ô bảng "U-Net [10], UNet++ [17], PraNet [9]" | "U-Net [10], PraNet [9]" |
| 131 | Ô bảng "Polyp-PVT [18], ColonFormer [19], TransFuse [20]" | "Polyp-PVT [18], ColonFormer [19]" |
| 163 | Gạch đầu dòng "**BlazeNeo** [41] …" | Xóa |
| 167 | Đoạn "Về Mamba, PolyPVT-MambaNet [43] …" | Xóa đoạn. Giữ câu kết "chưa thấy công trình trong nước nào đưa khối Mamba vào mô hình họ YOLO" (nhận định về việc chưa có, không cần nguồn) |

### Chương 2: `03_CHUONG_2_CO_SO_LY_THUYET.md` (9 chỗ)

| Dòng | Hiện tại | Sửa thành |
|---|---|---|
| 70 | "**Kết nối tắt dạng cộng (residual)** [44] cộng đầu vào…" | Bỏ "[44]" |
| 154 | "Đề tài dùng AdamW [51], là biến thể của Adam [52] tách phần…" | "…AdamW [51], là biến thể của Adam tách phần…" |
| 157 | "YOLO26 bỏ thành phần DFL [53] vốn dùng…" | "YOLO26 bỏ thành phần DFL vốn dùng… [6]" |
| 185 | Câu "ViT [57] áp dụng cơ chế này cho ảnh…" | Xóa câu |
| 193 | "Các mô hình như Swin Transformer [58] giảm chi phí … Mô hình không gian trạng thái là một hướng khác: …" | "Mô hình không gian trạng thái là một hướng giảm chi phí: giữ tính toàn cục nhưng chi phí tăng chậm hơn." (bỏ câu Swin) |
| 239 | "Vision Mamba [27] quét hai chiều xuôi và ngược. VMamba [7] đề xuất…" | Xóa câu Vision Mamba |
| 272 | Ô bảng "Có nhiều kết quả tốt trên ảnh y tế [28]–[31]" | "[28], [30], [31]" (khoảng [28]–[31] có chứa [29] bị bỏ; regex đánh số không bắt được dạng này, phải sửa tay) |
| 301 | "IoU còn gọi là chỉ số Jaccard [62]; Dice có nguồn gốc từ hệ số tương đồng của Dice [63]." | "IoU còn gọi là chỉ số Jaccard; Dice còn gọi là hệ số Sørensen–Dice." |
| 388 | "Theo quy ước của Cohen [69], được Lakens [68] trình bày lại…" | "Theo quy ước của Cohen, được Lakens [68] trình bày lại…" |

### Chương 3: `04_CHUONG_3_MO_HINH_DE_XUAT.md` (1 chỗ)

| Dòng | Hiện tại | Sửa thành |
|---|---|---|
| 43 | "…thông tin biên và hình dạng là manh mối có ích [32], [34], [35]." | "…[32], [35]." |

### Chương 4: `05_CHUONG_4_DU_LIEU_TIEN_XU_LY.md` (3 chỗ, văn bản của bạn cùng nhóm)

| Dòng | Hiện tại | Sửa thành |
|---|---|---|
| 5 (ghi chú) | Bảng đổi số "[4] → [72] …; [5] → [73] …; [11] → [77] …" | Ghi: [4] và [11] gộp vào [55]; [5] bỏ số trích; thêm dòng "rút gọn tài liệu tham khảo 30/10/2026" |
| 53 | "…chuẩn hóa về đoạn từ 0 đến 1 [72]. … bằng thư viện OpenCV [73], …" | "…từ 0 đến 1 [55]. … bằng thư viện OpenCV, …" |
| 129 | "Mosaic được tắt trong 10 epoch cuối [77]." | "…10 epoch cuối [55]." |

### Chương 5: `06_CHUONG_5_CAI_DAT_UNG_DUNG.md` (2 chỗ)

| Dòng | Hiện tại | Sửa thành |
|---|---|---|
| 52 | Ô bảng "Python, PyTorch [78], Ultralytics [55]" | "Python, PyTorch, Ultralytics [55]" |
| 53 | Ô bảng "NumPy, pandas, OpenCV, SciPy [79], Matplotlib" | Bỏ "[79]" |

### Chương 6: `07_CHUONG_6_THUC_NGHIEM_DANH_GIA.md` (3 chỗ)

| Dòng | Hiện tại | Sửa thành |
|---|---|---|
| 63 | "Các phép tính dùng thư viện SciPy [79]." | "Các phép tính dùng thư viện SciPy." |
| 98 | "…ở mức nhỏ đến vừa theo quy ước của Cohen [69]." | "…theo quy ước của Cohen [68]." |
| 330 | "Bộ đếm `FlopCounterMode` của PyTorch [78] chỉ đếm…" | Bỏ "[78]" |

Mở đầu, Kết luận, Phụ lục, Trang đầu: không trích tài liệu nào trong 23 mục, **không phải sửa**.

## 3. Các file khác bị ảnh hưởng

| File | Việc cần làm |
|---|---|
| `08_TAI_LIEU_THAM_KHAO.md` | Bỏ 23 mục, đánh số lại 57 mục theo lần trích đầu, sửa ghi chú đầu file |
| `_KIEM_TRA/F_bang_doi_so_tai_lieu.csv` | Thêm cột số mới (57), đánh dấu 23 mục bỏ |
| `_KIEM_TRA/H_su_dung_tai_lieu.md` | Sinh lại |
| `_KIEM_TRA/G_doi_chieu_thang_diem.md` | Sửa dòng §1.6 (còn 3 công trình trong nước) |
| `TLTK/` | Chuyển PDF của các mục bỏ sang `khong_con_trich/` (17 file có PDF); cập nhật `DOI_CHIEU_80_TAI_LIEU.md` thành bản 57, ghi chú trong `00_TONG_HOP…` và `DOI_CHUNG_6_BAI_THU_PHI.md` ([43] không còn trong báo cáo) |
| `CLAUDE.md`, `AGENTS.md`, `NGU_CANH_DU_AN.md`, `HUONG_DAN_LAM_VIEC_VOI_CLAUDE.md` | Đổi "80 tài liệu" thành "57", ghi lại quyết định rút gọn |
| File Word, PDF báo cáo | Ghép lại bằng `ghep_word.py` |
| `_KIEM_TRA/00_TONG_HOP_DIEU_TRA.md`, `B_…`, `D_…`, `D2_…` | **Không sửa**: đây là ghi chép điều tra cũ dùng số tạm; ghi một dòng chú thích là số đã lỗi thời |

## 4. Kế hoạch chạy theo đợt

| Đợt | Việc | Kiểm tra sau đợt |
|---|---|---|
| 0 | Sao lưu thư mục `md_bao_cao/` vào scratchpad; commit trạng thái hiện tại làm điểm quay lại (khi chủ dự án đồng ý) | Có bản sao |
| 1 | Sửa 13 chỗ ở Chương 1 | Đọc lại mục 1.2.2, 1.3, 1.4, 1.5, 1.6 cho liền mạch; không còn [12], [17], [20], [27], [29], [33], [34], [36], [41], [43] |
| 2 | Sửa 10 chỗ ở Chương 2, 3 (gồm khoảng "[28]–[31]") | Không còn [44], [52], [53], [57], [58], [62], [63], [69] ở Ch.2; Ch.3 không còn [34] |
| 3 | Sửa 8 chỗ ở Chương 4, 5, 6 và ghi chú Ch.4 | Không còn [72], [73], [77], [78], [79], [69] |
| 4 | Chạy script: bỏ 23 mục khỏi danh mục, đánh số lại 1→57 theo lần trích đầu, cập nhật bảng đối số, sinh lại bảng H | Thứ tự lần trích đầu đúng 1→57; mọi mục đều được trích; không số nào > 57; dò lại 10 trích dẫn ngẫu nhiên xem trỏ đúng tài liệu |
| 5 | Subagent phản biện đọc lại các câu đã sửa và danh mục mới (chỉ đọc) | Không có câu thiếu nguồn, không còn trích dẫn trỏ sai |
| 6 | Cập nhật TLTK và các file ngữ cảnh | Bảng đối chiếu TLTK ghi 57 mục |
| 7 | Ghép lại Word, xuất PDF, xem ảnh vài trang (Ch.1, Ch.2, Tài liệu tham khảo) | Danh mục 57 mục, số trang hợp lý |
| 8 | Commit lên `Okeydokey` (khi được đồng ý), không push | |

Thời gian dự kiến: khoảng 1,5 giờ.
