# Hướng dẫn Lương: chạy ablation trên CVC (chỉ suy luận)

> **Lương ơi:** file kiểm kê của ông đủ 30 checkpoint, Huy đã đối chiếu mAP với `results.csv`, khớp cả 30 dòng. Bước này chỉ chạy suy luận 30 checkpoint đó trên CVC-ClinicDB và CVC-ColonDB, **không train**, ước tính dưới 1 giờ (chưa xác minh). Ông chỉ cần chạy rồi **gửi lại thư mục kết quả**; phần tổng hợp và viết vào báo cáo Huy làm.
>
> **Mục đích:** trả lời phản biện II.1, kiểm chứng giả thuyết "nhánh hình dạng quá khớp với Kvasir", bằng cách xem biến thể nào bỏ sót polyp nhiều trên CVC.

Có hai cách: tự làm theo các bước ở mục A, hoặc dán prompt ở mục B cho AI làm.

---

## A. Tự làm (4 bước)

**Bước 1. Chép script.** Huy gửi kèm file `danh_gia_ablation_ngoai.py`. Chép vào thư mục repo của ông:

```
08_du_lieu_thuc_te/scripts/danh_gia_ablation_ngoai.py
```

File này nằm cạnh `danh_gia_du_lieu_ngoai.py` và dùng lại hàm của file đó, nên phải đặt đúng thư mục này.

**Bước 2. Kiểm tra** (mở terminal tại thư mục gốc repo):

```
C:\venv_kl_gpu\Scripts\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_ablation_ngoai.py --kiem-tra
```

Phải thấy dòng `KIỂM TRA: ĐỦ, có thể chạy`. Nếu có dòng `THIẾU` thì dừng lại và chụp màn hình gửi Huy. Lỗi hay gặp:
- Thiếu dữ liệu: script đọc ở `DoAnTotNghiepV4\Dataset\CVC-ClinicDB\PNG\...` và `DoAnTotNghiepV4\Dataset\CVC-ColonDB_data\...`, tức thư mục **ngang hàng** với thư mục repo.
- Không có GPU: phải chạy bằng `C:\venv_kl_gpu\Scripts\python.exe`, không dùng python thường.

**Bước 3. Đối chiếu môi trường** (khoảng 1–2 phút, chỉ chạy được nếu máy ông có checkpoint TSVM seed 0 và thư mục `08_du_lieu_thuc_te/bang/tung_luot/`):

```
C:\venv_kl_gpu\Scripts\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_ablation_ngoai.py --doi-chieu
```

Kết quả mong đợi: `0/612 ảnh lệch`, hoặc lệch rất ít. Nếu thấy `Bỏ qua đối chiếu` thì cứ làm tiếp bước 4. Nếu lệch nhiều (trên 10%) thì chụp màn hình gửi Huy trước khi chạy tiếp.

**Bước 4. Chạy thật:**

```
C:\venv_kl_gpu\Scripts\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_ablation_ngoai.py
```

Script chạy 3 biến thể × 10 seed × 2 bộ dữ liệu = 60 lượt. Nếu bị ngắt giữa chừng, chạy lại đúng lệnh này; các lượt đã xong sẽ được bỏ qua.

**Gửi lại cho Huy:**
- Nén thư mục `08_du_lieu_thuc_te/bang/tung_luot_ablation/` (đủ **60 file CSV**) thành `tung_luot_ablation.zip`.
- Gửi kèm dòng cuối của terminal (`Xong. Tổng thời gian: ...`) và kết quả bước 3.

---

## B. Prompt cho AI (copy nguyên khung dưới đây)

````markdown
Trong repo khóa luận polyp trên máy này, mình cần chạy script suy luận ablation trên dữ liệu ngoài rồi đóng gói kết quả.
KHÔNG train, KHÔNG sửa script nào có sẵn, KHÔNG xóa hay ghi đè file trong 03_ket_qua_huan_luyen/, 01_du_lieu/,
08_du_lieu_thuc_te/bang/tung_luot/ hay bang/20seed/. Chỉ được tạo thư mục 08_du_lieu_thuc_te/bang/tung_luot_ablation/.

1. Chép file danh_gia_ablation_ngoai.py mình gửi vào 08_du_lieu_thuc_te/scripts/ (cạnh danh_gia_du_lieu_ngoai.py).
2. Ở thư mục gốc repo, chạy:
   C:\venv_kl_gpu\Scripts\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_ablation_ngoai.py --kiem-tra
   Nếu không thấy "KIỂM TRA: ĐỦ, có thể chạy" thì DỪNG, báo lại các dòng "THIẾU". Không tự sửa đường dẫn trong script.
3. Chạy: ... danh_gia_ablation_ngoai.py --doi-chieu
   Ghi lại dòng "ĐỐI CHIẾU ...". Nếu số ảnh lệch > 10% thì DỪNG và báo lại.
4. Chạy: ... danh_gia_ablation_ngoai.py   (không tham số; mất khoảng dưới 1 giờ; bị ngắt thì chạy lại, lượt đã xong tự bỏ qua)
5. Kiểm tra 08_du_lieu_thuc_te/bang/tung_luot_ablation/ có đủ 60 file CSV
   (2 bộ clinicdb/colondb × 3 biến thể abl_vmamba_only/abl_shape_only/abl_no_guidance × seed 0–9).
6. Nén thư mục đó thành tung_luot_ablation.zip. Viết file KET_QUA_CHAY_ABLATION_NGOAI.md gồm: kết quả bước 2, dòng
   đối chiếu bước 3, tổng thời gian bước 4, số file CSV, và lỗi nếu có. Không tự tính hay diễn giải kết quả.
````

---

**Hạn:** cần kết quả trong hôm nay (07/11) để kịp chèn vào báo cáo trước hạn nộp 08/11. Nếu không chạy được (thiếu GPU hoặc thiếu dữ liệu CVC) thì báo Huy sớm để nhóm giữ nguyên câu "giả thuyết chưa kiểm chứng".
