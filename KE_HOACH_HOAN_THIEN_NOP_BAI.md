# Kế hoạch hoàn thiện để nộp (09/11/2026, hạn 11/11/2026)

Mục tiêu:
- so sánh công bằng: PraNet và U-Net dùng bản **640** (cùng kích thước ảnh và cùng cách tăng cường dữ liệu với YOLO), theo góp ý của giảng viên;
- cập nhật kết quả mới: ablation 20 seed, C2PSA rộng;
- thêm chế độ mô phỏng thời gian thực cho web;
- dọn thư mục `Test_Mau` thành bộ nộp gọn.

Nguyên tắc chung:
- Không xóa file nào. Thứ gì không nộp thì chuyển sang `..\_Luu_Tru_Ngoai\Test_Mau\` và giữ nguyên đường dẫn con.
- Mỗi lần di chuyển đều ghi vào `PATH_MAP.md` và `PATH_MAP.csv`.
- Kết quả cũ không ghi đè tại chỗ: chuyển ra trước rồi mới sinh bản mới.
- Số liệu nào cũng phải truy được về script và bảng CSV.
- Chỉ commit khi bạn đồng ý.

---

## Phần A. Số liệu và hình (làm trước, vì báo cáo và web đều dùng)

| # | Việc | Đầu ra | Máy | Thời gian |
|---|---|---|---|---|
| A1 | Vẽ hình ablation 20 seed: thêm lựa chọn `--ablation-seeds 20` vào `ve_hinh.py` | `06_bao_cao/hinh/ablation_20seed/` (k01, k02; vi và en) | CPU | 10 phút |
| A2 | Script mới `tinh_c2psa_rong.py`: so sánh ghép cặp C2PSA rộng với Baseline và với TSVM, đếm tham số từ `best.pt` | `bang/20_c2psa_rong_tung_seed.csv`, `bang/20b_c2psa_rong_thong_ke.csv`, hình k03 (điểm từng seed của 3 mô hình) | CPU | 30 phút |
| A3 | Chuyển `danh_gia_pixel.py` sang PraNet và U-Net bản 640 (chi tiết bên dưới) | Bảng 10–12 mới | GPU | 1–2 giờ |
| A4 | Chạy lại topology cho PraNet và U-Net bản 640 (`danh_gia_topology.py`) | Bảng 13–15 mới | GPU | khoảng 1 giờ |
| A5 | Vẽ lại các hình có PraNet và U-Net | p01, p02, p03, o01, o02 và hình bảng so sánh 4 mô hình | CPU | 10 phút |
| A6 | Cập nhật bộ tài liệu tổng quan | `00_tai_lieu_tong_quan/06_…`, `10_SO_SANH_PRANET_UNET.md`, `12_TRUY_VET_SO_LIEU.md`, `NGU_CANH_DU_AN.md` | — | 1 giờ |
| A7 | Cập nhật trang Chỉ số trên web: chạy `xuat_chi_so_web.py` (dòng tham chiếu PraNet/U-Net 640, thêm C2PSA rộng) | `research-metrics.json` | CPU | 15 phút |

**Chi tiết A3.** Hiện script dùng PraNet và U-Net bản 352: checkpoint lấy từ `05_/PraNet`, `05_/UNet`, kiến trúc nạp từ notebook trong `99_luu_tru/log_kaggle_cu`, ảnh resize 352. Sẽ đổi thành:
- **Checkpoint:** `05_/PraNet_640/PraNet_640_aug_s{seed}/pranet_best_s{seed}.pth` và `05_/UNet_640/UNet_640_aug_s{seed}/best_unet_s{seed}.pth`. Đây là bản có Dice trên tập val tốt nhất, không phải `last.pth`.
- **Kiến trúc:** nạp từ notebook mới `02_ma_nguon/notebook_kaggle/{pranet,unet}-new.ipynb`. Trước khi chạy, kiểm tra từng lớp mạng khớp với checkpoint.
- **Suy luận:** ảnh kéo về 640×640, giống lúc huấn luyện. Dự đoán phóng về kích thước gốc rồi lấy ngưỡng 0,5.
- **Giao thức đánh giá giữ nguyên như YOLO:** mặt nạ chuẩn ở độ phân giải gốc, đủ 160 ảnh val (40 ảnh nền), các phép tính Dice, IoU, P, R như cũ.
- Phần Baseline và TSVM **không chạy lại** (lấy lại từ bảng bằng `--tu-bang`).
- Bảng 352 cũ được chuyển sang `bang/ban_352_cu/` trước khi ghi bảng mới.

**Kết luận có thể đổi.** Câu "TSVM kém PraNet rõ rệt" và các so sánh với PraNet/U-Net sẽ được viết lại theo số mới. Chưa có số thì chưa viết.

---

## Phần B. Web: chế độ "Mô phỏng thời gian thực" (bản gọn)

Video đã quay được phát lại đúng tốc độ gốc, mỗi khung được phân tích và hiển thị ngay. Đây là **mô phỏng**, không phải hệ thống nhúng vào máy nội soi.

| # | Việc |
|---|---|
| B1 | AI service: thêm "phiên phân tích" chạy nền, dùng lại hàm xử lý video hiện có. Mỗi khung vừa ghi vào MP4 vừa đưa vào luồng xem trực tiếp. Có giới hạn tốc độ để phát đúng thời gian thực (máy nhanh không bị tua nhanh). Thêm endpoint xem luồng (MJPEG), endpoint trạng thái (tiến độ, tốc độ đạt được, số khung có polyp) và endpoint lấy kết quả khi xong. |
| B2 | Web Spring: trên trang Video có lựa chọn "Mô phỏng thời gian thực". Trang xem trực tiếp hiển thị luồng hình, đèn "Phát hiện polyp", tốc độ (ví dụ "30 khung/giây, kịp thời gian thực" hoặc "chậm hơn 2,4 lần") và thanh tiến độ. Khi xong, tự lưu MP4 và lịch sử vào MongoDB rồi chuyển sang trang kết quả hiện có. |
| B3 | Ghi chú trên trang: "Mô phỏng trên video đã quay; chưa phải hệ thống thời gian thực gắn vào thiết bị nội soi." |
| B4 | Viết test cho AI service và web. Thử trên GPU bằng video 10 giây tự tạo (không dùng LDPolypVideo). Cập nhật README. |

Thời gian: khoảng nửa ngày. Có thể làm song song trong lúc GPU chạy A3 và A4, nhưng hai việc dùng chung GPU nên phần đo tốc độ của B4 phải chạy sau A4.

---

## Phần C. Dọn thư mục `Test_Mau` để nộp

Chuyển sang `..\_Luu_Tru_Ngoai\Test_Mau\` (cùng ổ nên chuyển ngay, không tốn thêm chỗ):

| Mục | Dung lượng | Ghi chú |
|---|---|---|
| `05_so_sanh_mo_hinh_khac/PraNet/`, `UNet/` (bản 352) | 2,6 GB | Làm sau A3. Bảng 352 cũ giữ trong `bang/ban_352_cu/` để đối chiếu |
| `99_luu_tru/` trừ `ket_qua_cu/TSVM_cu_checkpoint_FP16_seed0-20/` | khoảng 9,6 GB | Mục giữ lại được `tinh_lai_so_lieu.py` đọc để chứng minh lỗi FP16. Sau A3, `log_kaggle_cu` không còn được script nào dùng |
| `07_kiem_toan_va_sua/` | 1,3 GB | Hồ sơ kiểm toán nội bộ |
| Các file Word cũ ở gốc `06_bao_cao/`, cùng `luu_tru_cu/`, `new_bao_cao/`, `md_bao_cao_70/` | khoảng 60 MB | Danh sách đã gửi ngày 09/11 |
| Các bảng và hình 10 seed: `bang/10seed/`, `bang/ablation_10seed/`, `hinh/ket_qua_10seed/`, `hinh/ablation_10seed/` | nhỏ | Chỉ để đối chiếu |
| File làm việc với AI: `AGENTS.md`, `CHUYEN_GIAO_CODEX.md`, `HUONG_DAN_LAM_VIEC_VOI_CLAUDE.md`, `.claude/`, `.vscode/` | nhỏ | **Chuyển sau cùng**, ngay trước khi nộp |

Sau khi chuyển, sửa lại các đường dẫn script còn trỏ tới thư mục đã chuyển, rồi chạy thử từng script để chắc không gãy.

Cấu trúc sau khi dọn (giữ số thứ tự 00–08):

```text
Test_Mau/
  README.md                  mục lục cho người chấm + cách chạy web
  00_tai_lieu_tong_quan/     tài liệu tổng quan, scripts/, bang/ (CSV kết quả)
  01_du_lieu/                BG20 880/120 + 40 ảnh nền val, script tạo dữ liệu
  02_ma_nguon/               fork Ultralytics TSVM FP32, C2PSA rộng, notebook Kaggle
  03_ket_qua_huan_luyen/     6 nhóm × 20 seed: Baseline, TSVM_FP32, Vmamba_only, Shape_only, No_guidance, C2PSA_rong
  04_phan_tich_20seed/       phân tích thống kê, benchmark CPU
  05_so_sanh_mo_hinh_khac/   PraNet_640, UNet_640 (20 seed mỗi mô hình)
  06_bao_cao/                Word/PDF báo cáo, hinh/, slide/, nhận xét, biểu mẫu
  08_du_lieu_thuc_te/        đánh giá trên 4 bộ dữ liệu ngoài
  99_luu_tru/                chỉ còn checkpoint TSVM FP16 cũ (bằng chứng lỗi FP16)
  PATH_MAP.md / .csv
```

`README.md` sẽ viết lại thành mục lục cho người chấm: mỗi thư mục chứa gì, mở file nào trước, cách chạy lại số liệu, cách chạy web.

---

## Phần D. Báo cáo: file markdown bắt đầu mới

- Viết bản sửa cuối thành **file markdown mới** (ví dụ `06_bao_cao/BAO_CAO_BAN_CUOI.md`), không tạo file Word. Bản Word đã nộp thầy giữ nguyên.
- Sửa theo văn phong của nhóm (skill `van-phong-bao-cao-nhom`):
  1. **So sánh PraNet và U-Net:** bảng và hình theo bản 640. Ghi rõ điều kiện chung: ảnh 640, cùng cách tăng cường, cùng tập val, cùng giao thức đánh giá theo pixel.
  2. **Ablation (mục 6.6):** thay ô [CHỜ KẾT QUẢ] bằng bảng và hình 20 seed. Kết luận: bỏ bất kỳ thành phần nào thì trung bình đều giảm, nhưng không có ý nghĩa thống kê.
  3. **Đối chứng C2PSA rộng** (cùng số tham số): TSVM hơn +0,0070, p = 0,0002, 17/20 seed. Ghi là phân tích phụ, thăm dò. Kết luận chính so với Baseline vẫn là "xu hướng, p = 0,061".
  4. **Mục ứng dụng (4.8):**
     - trọng số seed 15 và quy tắc chọn, kể cả cách phá hòa với seed 19;
     - chạy GPU;
     - video: lấy mẫu, giữ mặt nạ, chế độ "Tất cả khung", mô phỏng thời gian thực;
     - trang Chỉ số, mặt nạ thật, lưu trữ (MongoDB chỉ lưu chỉ số và đường dẫn file);
     - chụp lại màn hình.
  5. **Hạn chế:** Polyp-PVT và VM-UNet chưa chạy; thời gian thực mới là mô phỏng; chưa có đánh giá của bác sĩ.
- Không xuất Word/PDF ở bước này.

---

## Phần E. Kiểm tra cuối và commit

1. Chạy lại toàn bộ script số liệu ở chế độ chỉ đọc, đối chiếu các số trong báo cáo với CSV.
2. Chạy test web và AI service.
3. Commit `Test_Mau` lên nhánh `Okeydokey` và commit repo web khi bạn đồng ý. Chỉ push khi bạn yêu cầu.

---

## Thứ tự và thời gian

| Thời điểm | Việc |
|---|---|
| Chiều tối 09/11 | A1, A2 (CPU) → A3, A4 chạy nền trên GPU; đồng thời làm B1–B3 |
| Tối 09/11 | A5, A6, A7; B4 |
| Sáng 10/11 | Phần C (dọn thư mục), sửa đường dẫn script, chạy thử |
| 10/11 | Phần D (báo cáo) |
| Sáng 11/11 | Phần E, nộp |

## Đã chốt (09/11/2026, chủ dự án duyệt kế hoạch)

- **Thứ tự:** làm Phần B (web mô phỏng thời gian thực) trước. Xong web thì hỏi lại trước khi làm Phần A, C, D, E.
- **Bản báo cáo cuối:** viết thành **file markdown mới**, không tạo file Word. Bản Word đã nộp thầy giữ nguyên.
- **`07_kiem_toan_va_sua/`:** chuyển ra `_Luu_Tru_Ngoai`.
- **Thư mục báo cáo** (`06_bao_cao/`, gồm `md_bao_cao/`…): giữ lại. Các file markdown thuộc kết quả cũ (bộ 10 seed, ablation 5/10 seed, PraNet/U-Net 352, nháp cũ) thì chuyển ra ngoài.
- **Polyp-PVT, VM-UNet, MambaPSA:** bỏ, chỉ nêu trong phần hạn chế.
