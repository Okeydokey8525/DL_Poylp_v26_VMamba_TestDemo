# Hướng dẫn Lương: chạy báo nhầm trên 800 ảnh cecum (chỉ suy luận)

> **Lương ơi:** bước này **không train**, chỉ chạy suy luận 80 checkpoint có sẵn trên máy ông (40 YOLO + 20 PraNet + 20 U-Net) trên 800 ảnh normal-cecum mà BG20 chưa dùng. Thời gian ước tính khoảng 1–2 giờ GPU (chưa xác minh). Ông chỉ cần chạy rồi **gửi lại thư mục kết quả**; phần tổng hợp và viết vào báo cáo Huy làm.
>
> **Mục đích:** trả lời phản biện II.5 (mẫu âm thiếu đa dạng). Cần biết báo nhầm 10,8% trên PolypGen là do ảnh chưa thấy hay do khác miền. Máy Huy không có GPU và không có checkpoint nên không chạy được.
>
> Huy đã kiểm tra: 800 ảnh này không gần trùng với 160 ảnh nền huấn luyện (0/800 ảnh có tương quan ≥ 0,95).

Có hai cách: tự làm theo mục A, hoặc dán prompt ở mục B cho AI làm. **Nếu máy đang chạy ablation ngoài thì chạy xong cái đó trước**, vì hai việc cùng dùng GPU.

---

## A. Tự làm (4 bước)

**Bước 1. Chép script.** Huy gửi kèm file `danh_gia_nen_cecum.py`. Chép vào thư mục repo của ông:

```
08_du_lieu_thuc_te/scripts/danh_gia_nen_cecum.py
```

File này dùng lại hàm của `00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py` và `08_du_lieu_thuc_te/scripts/kiem_tra_trung_polypgen.py`, nên phải đặt đúng thư mục này. Ảnh cecum (`01_du_lieu/tao_BG20/normal-cecum/`) đã có trong git, không cần tải thêm.

**Bước 2. Kiểm tra** (mở terminal tại thư mục gốc repo):

```
C:\venv_kl_gpu\Scripts\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_nen_cecum.py --kiem-tra
```

Phải thấy `Ảnh cecum chưa dùng: 800`, `Checkpoint có: 80/80` và `KIỂM TRA: ĐỦ, có thể chạy`. Nếu có dòng `THIẾU` thì dừng lại và chụp màn hình gửi Huy.

**Bước 3. Đối chiếu môi trường** (khoảng 1 phút):

```
C:\venv_kl_gpu\Scripts\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_nen_cecum.py --doi-chieu
```

Lệnh này chạy mô hình gốc seed 0 trên 40 ảnh nền kiểm định, rồi so với kết quả cũ trong `bang/10_pixel_tung_anh.csv`. Kết quả mong đợi là `ĐỐI CHIẾU: 0/40 ảnh nền lệch`. Nếu lệch từ 2 ảnh trở lên thì chụp màn hình gửi Huy trước khi chạy tiếp.

**Bước 4. Chạy thật:**

```
C:\venv_kl_gpu\Scripts\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_nen_cecum.py
```

Script chạy 4 mô hình × 20 seed = 80 lượt. Nếu bị ngắt giữa chừng, chạy lại đúng lệnh này; các lượt đã xong sẽ được bỏ qua.

**Gửi lại cho Huy:**
- Nén thư mục `08_du_lieu_thuc_te/bang/nen_cecum/` (trong đó `tung_luot/` phải đủ **80 file CSV**) thành `nen_cecum.zip`.
- Gửi kèm hai file `08_du_lieu_thuc_te/bang/20seed/06_nen_cecum_tung_seed.csv` và `07_nen_cecum_thong_ke.csv`.
- Gửi kèm dòng `Tổng thời gian: ...` và kết quả bước 3.

---

## B. Prompt cho AI (copy nguyên khung dưới đây)

````markdown
Trong repo khóa luận polyp trên máy này, mình cần chạy script suy luận trên 800 ảnh normal-cecum rồi đóng gói kết quả.
KHÔNG train, KHÔNG sửa script nào có sẵn, KHÔNG xóa hay ghi đè file trong 03_ket_qua_huan_luyen/, 05_so_sanh_mo_hinh_khac/,
01_du_lieu/, 08_du_lieu_thuc_te/bang/tung_luot/. Chỉ được tạo thư mục 08_du_lieu_thuc_te/bang/nen_cecum/ và hai file
08_du_lieu_thuc_te/bang/20seed/06_nen_cecum_tung_seed.csv, 07_nen_cecum_thong_ke.csv.

1. Chép file danh_gia_nen_cecum.py mình gửi vào 08_du_lieu_thuc_te/scripts/.
2. Ở thư mục gốc repo, chạy:
   C:\venv_kl_gpu\Scripts\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_nen_cecum.py --kiem-tra
   Nếu không thấy "KIỂM TRA: ĐỦ, có thể chạy" thì DỪNG, báo lại các dòng "THIẾU". Không tự sửa đường dẫn trong script.
3. Chạy: ... danh_gia_nen_cecum.py --doi-chieu
   Ghi lại dòng "ĐỐI CHIẾU ...". Nếu lệch từ 2/40 ảnh trở lên thì DỪNG và báo lại.
4. Chạy: ... danh_gia_nen_cecum.py   (không tham số; khoảng 1–2 giờ; bị ngắt thì chạy lại, lượt đã xong tự bỏ qua)
5. Kiểm tra 08_du_lieu_thuc_te/bang/nen_cecum/tung_luot/ có đủ 80 file CSV
   (cecum800_{baseline,tsvm,pranet,unet}_s0 … s19) và có hai file 06_, 07_ trong bang/20seed/.
6. Nén thư mục nen_cecum/ thành nen_cecum.zip. Viết file KET_QUA_CHAY_NEN_CECUM.md gồm: kết quả bước 2, dòng đối chiếu
   bước 3, tổng thời gian bước 4, số file CSV, và lỗi nếu có. Không tự tính hay diễn giải kết quả.
````

---

**Hạn:** cần kết quả trong hôm nay (07/11) để kịp chèn vào báo cáo trước hạn nộp 08/11. Nếu không chạy kịp thì báo Huy sớm; nhóm sẽ trả lời II.5 bằng phần hạn chế và hướng phát triển, không có số 800 ảnh.
