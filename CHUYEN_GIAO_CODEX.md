# Chuyển giao công việc cho Codex (07/11/2026)

Tài liệu này giúp một trợ lý AI khác (Codex) tiếp quản giữa chừng. **Đọc theo thứ tự:** `AGENTS.md`, `CLAUDE.md`, `NGU_CANH_DU_AN.md`, rồi file này, rồi `06_bao_cao/sua_theo_nhan_xet/` (`CONTEXT.md`, `KE_HOACH.md`).

- **Chủ dự án:** Lê Đức Lương. Giao tiếp bằng tiếng Việt.
- **Nhóm:** Lương, Phùng Tuấn Huy, Trần Mạnh Toàn.
- **GVHD:** TS. Phùng Thế Bảo.
- **Hạn nộp:** 08/11/2026.

## 1. Đang ở đâu

GVHD gửi nhận xét `06_bao_cao/Nhan_xet_KLCN-CNTT-182.docx` cho bản đã nộp `06_bao_cao/BaoCaoKhoaLuan_CNTT_KLCN182.docx` (77 trang). Nhóm đang làm hai việc song song:

1. **Sửa báo cáo theo nhận xét.** Theo Lương, phần 1 của kế hoạch (hình thức, chính tả, cam đoan, bìa…) đã do bạn cùng nhóm làm. Kế hoạch đầy đủ ở `06_bao_cao/sua_theo_nhan_xet/KE_HOACH.md`.
2. **Huấn luyện bổ sung trên Kaggle** (nhiều tài khoản), để trả lời mục nội dung 4 của nhận xét: so sánh công bằng, đối chứng cùng số tham số, ablation 20 seed.

## 2. Trạng thái huấn luyện

| Mô hình | Số seed | Trạng thái | Kết quả nằm ở đâu |
|---|---|---|---|
| YOLO26s-seg gốc, TSVM FP32 | 0–19 | ✅ Xong từ trước | `03_ket_qua_huan_luyen/Baseline_YOLO26s_seg/`, `TSVM_FP32/` |
| Ablation `vmamba_only`, `shape_only`, `shape_vmamba_no_guidance` | 0–9 | ✅ Có trong repo | `03_ket_qua_huan_luyen/{Vmamba_only,Shape_only,No_guidance}/` |
| Cùng 3 biến thể ablation | 10–19 | ✅ Lương báo đã train xong, **chưa tải về repo** | Kaggle (nhiều tài khoản) |
| C2PSA rộng (đối chứng cùng số tham số) | 0–19 | ✅ Lương báo xong, **chưa tải về** | Kaggle; đề xuất đặt vào `03_ket_qua_huan_luyen/C2PSA_rong/` |
| PraNet 640 có tăng cường | 0–19 | ✅ Lương báo xong, **chưa tải về** | Kaggle; đề xuất đặt vào `05_so_sanh_mo_hinh_khac/PraNet_640/` |
| **U-Net 640 có tăng cường** | 0–19 | ❌ **Chưa xong.** Lượt trên tài khoản `okeydokey0805` bị hủy | Notebook `02_ma_nguon/notebook_kaggle/unet-new.ipynb` |
| **Polyp-PVT** (mốc Transformer theo yêu cầu "ít nhất 1 baseline Mamba hoặc Transformer" của thầy) | đề xuất 5–10, nếu kịp thì 20 | Ưu tiên tiếp theo. Notebook đã khớp mã gốc và chạy thử 2 epoch trên máy (08/11); chưa chạy trên Kaggle | `02_ma_nguon/notebook_kaggle/polyp_pvt/polyp-pvt.ipynb` |
| VM-UNet | — | Tùy chọn, rủi ro cài đặt cao | `02_ma_nguon/notebook_kaggle/vm_unet/` |
| ~~MambaPSA~~ | — | **Bỏ (07/11).** Không có mã gốc nên không tái hiện | `02_ma_nguon/ultralytics_MambaPSA/` chỉ giữ làm tư liệu |

**Hướng dẫn chạy và cấu hình:** `02_ma_nguon/notebook_kaggle/README_HUAN_LUYEN_BO_SUNG.md`.

- **C2PSA rộng:**
  - thư mục fork `02_ma_nguon/ultralytics_C2PSA_rong/`, YAML `cfg/models/26/yolo26s-seg-C2PSA-rong.yaml`;
  - tầng 10 là `[-1, 2, C2PSA, [1024, 0.75]]`, có 1.830.016 tham số (TSVM: 1.811.201).
- **MambaPSA: KHÔNG DÙNG.** Thư mục `02_ma_nguon/ultralytics_MambaPSA/` là bản tái hiện theo mô tả (tác giả chưa công bố mã). Chủ dự án quyết định không đưa vào báo cáo vì không đối chứng được. Câu trả lời phản biện:
  - MambaPSA chưa có mã nguồn và trọng số công bố, nên nhóm không tái hiện;
  - nhóm dùng Polyp-PVT (có mã gốc) làm mốc Transformer;
  - biến thể Chỉ SS2D trong ablation (thay C2PSA bằng khối SSM thuần) là phương án gần nhất về ý tưởng; phải nói rõ là "gần về ý tưởng", không phải MambaPSA.
- **PraNet/U-Net 640:**
  - giống YOLO ở: dữ liệu, ảnh 640, 100 epoch, batch 8, seed, FP32, tăng cường (HSV, lật ngang, dịch, co giãn, mosaic và tắt mosaic 10 epoch cuối);
  - khác YOLO ở: hàm mất mát, bộ tối ưu, lr và lịch lr (giữ theo notebook cũ), không có EMA, kéo ảnh về hình vuông thay vì letterbox, chọn epoch theo Dice val;
  - đầu ra của mỗi lượt: `runs/<Mô hình>_640_aug_s<SEED>/` gồm `results.csv`, `pranet_best_s{SEED}.pth` hoặc `best_unet_s{SEED}.pth`, `last.pth`, `tom_tat.txt`.

## 3. Việc tiếp theo (theo thứ tự)

1. **Đưa kết quả về repo**
   - Chủ dự án tải zip từ Kaggle. **Hỏi trước khi tự tải** bằng `kaggle kernels output`.
   - Giải nén vào thư mục riêng ở bảng trên. Không ghi đè kết quả cũ: PraNet/U-Net 352 trong `05_so_sanh_mo_hinh_khac/PraNet`, `UNet` phải giữ nguyên.
   - Kiểm tra mỗi lượt:
     - YOLO: đủ 100 dòng trong `results.csv`, có `best.pt`, `args.yaml` khớp seed và khớp cấu hình 20 seed chính;
     - PraNet/U-Net: đủ 100 epoch trong `results.csv` và có checkpoint tốt nhất.
2. **Ablation 20 seed và C2PSA rộng**
   - `00_tai_lieu_tong_quan/scripts/tinh_ablation.py` hiện có `--seeds` với `choices=(5, 10)`, ghi ra `bang/ablation_<n>seed/`. Cần thêm 20, và thêm cấu hình `C2PSA_rong` vào `CONFIGS`.
   - So ghép cặp với TSVM theo seed.
   - Bảng 5 seed và 10 seed cũ phải giữ nguyên.
3. **Vẽ hình**
   - `06_bao_cao/hinh/scripts/ve_hinh.py --ablation-seeds` hiện có `choices=(5, 10)`, ghi vào `hinh/ablation_<n>seed/`. Mở rộng cho 20.
4. **Đánh giá theo điểm ảnh cho PraNet/U-Net 640**
   - `00_tai_lieu_tong_quan/scripts/danh_gia_pixel.py` đang nạp kiến trúc từ `99_luu_tru/log_kaggle_cu/*.ipynb` và chạy ở 352.
   - Cần thêm tùy chọn 640 và ghi ra thư mục riêng (ví dụ `bang/pixel_640/`).
   - Kiến trúc PraNet/U-Net trong notebook mới giống bản cũ; chỉ khác kích thước ảnh và cách huấn luyện.
5. **Sửa báo cáo**
   - Làm trên bản sao, không ghi đè bản đã nộp, theo `KE_HOACH.md` và skill `.claude/skills/van-phong-bao-cao-nhom/SKILL.md`.
   - Điền số vào các ô [CHỜ KẾT QUẢ]: mục 4.5.5 ablation, 4.6 so sánh mô hình khác, 4.7 dữ liệu ngoài.
   - Viết thêm câu trả lời các mục II.1 và II.5 (xem mục 4 bên dưới).

## 4. Kết quả mới đã chạy xong trên máy Lương (07/11)

**Ablation trên CVC, chỉ suy luận, seed 0–9**
- Script: `08_du_lieu_thuc_te/scripts/danh_gia_ablation_ngoai.py`.
- Đầu ra: `08_du_lieu_thuc_te/bang/tung_luot_ablation/`, 60 CSV; biên bản ở `KET_QUA_CHAY_ABLATION_NGOAI.md`.
- Đối chiếu môi trường: 0/612 ảnh lệch.
- Số tính nhanh (**chưa phải bảng chính thức**, Huy tổng hợp): ba biến thể và TSVM gần như bằng nhau trên CVC (Dice ClinicDB khoảng 0,77; ColonDB khoảng 0,60–0,61), đều thấp hơn mô hình gốc (0,783; 0,628).
- Như vậy giả thuyết "nhánh hình dạng quá khớp với Kvasir" **không được ủng hộ**, vì biến thể không có nhánh hình dạng cũng giảm như TSVM.

**Báo nhầm trên 800 ảnh cecum chưa dùng, 20 seed** (trả lời II.5)
- Script: `08_du_lieu_thuc_te/scripts/danh_gia_nen_cecum.py`.
- Đầu ra:
  - thư mục `08_du_lieu_thuc_te/bang/nen_cecum/`;
  - `bang/20seed/06_nen_cecum_tung_seed.csv`, `07_nen_cecum_thong_ke.csv`;
  - biên bản `KET_QUA_CHAY_NEN_CECUM.md`.
- Đối chiếu môi trường 0/40; ảnh gần trùng với tập train 0/800.
- Tỷ lệ ảnh bị báo nhầm (trung bình):

| Mô hình | Cecum chưa dùng | PolypGen |
|---|---|---|
| YOLO gốc | 1,3% | 13,3% |
| TSVM | 1,4% | 10,8% |
| PraNet | 3,4% | 22,6% |
| U-Net | 30,4% | 69,3% |

→ Báo nhầm trên PolypGen chủ yếu do **khác miền**, không phải do gặp ảnh chưa thấy.

## 5. Quyết định đã chốt với chủ dự án

- **Giữ nguyên chia 880/120.** Các việc sau chỉ ghi vào phần Hạn chế và Hướng phát triển, không làm:
  - tách tập test hoặc 5-fold (khoảng 139 giờ GPU);
  - 42 cặp seed. Lý do có số 42: với d_z = 0,44 và 20 cặp seed, lực kiểm định chỉ khoảng 47%; cần khoảng 42 cặp để đạt 80%;
  - ảnh nền đa dạng;
  - ý kiến bác sĩ.
- **Thêm kết quả epoch 100 cố định vào 4.5.1:** Δ +0,0025, p 0,456 (`bang/04b_do_nhay_quy_tac_epoch.csv`). Đây là câu trả lời cho ý "chọn epoch trên tập kiểm định".
- **Sửa câu "ổn định hơn rõ"** thành: SD nhỏ hơn khoảng 39%, chỉ thấy ở epoch tốt nhất, Levene p = 0,026 chỉ để tham khảo.
- **Tài liệu tham khảo:**
  - [7] sửa thành "H. Dao Viet";
  - [4] và [9] ghi phiên bản arXiv và ngày truy cập;
  - thêm Polyp-PVT hoặc VM-UNet chỉ khi chủ dự án đồng ý, và phải đánh số lại các mục phía sau.

## 6. Quy tắc bắt buộc (tóm tắt; bản đầy đủ ở AGENTS.md và CLAUDE.md)

- "Chưa chỉnh gì / đang hỏi đáp" nghĩa là chỉ bàn, không sửa. Việc lớn phải trình kế hoạch và chờ duyệt.
- Không bịa số: mọi con số phải truy được về CSV. Kết quả chính là **xu hướng**, không viết "vượt trội". Số thập phân dùng dấu phẩy.
- Không sửa `01_du_lieu/`, checkpoint trong `03_`, `05_`, các thư mục `07_kiem_toan_va_sua/`, `99_luu_tru/`. Kết quả mới để thư mục riêng.
- **Hỏi trước khi:** commit (chỉ lên nhánh `Okeydokey`), push, `kaggle kernels push`, tải dữ liệu, tải bất cứ thứ gì lên dịch vụ ngoài.
- Không đọc, in hay commit token (`~/.kaggle/kaggle.json`). Không đọc `..\Ung_Dung\polypweb\GhiChu.txt`.

## 7. Lỗi môi trường đã gặp (Windows)

- **Python có GPU:** `C:\venv_kl_gpu\Scripts\python.exe` (torch 2.13 + cu130, GPU RTX 5050 Laptop 8 GiB). Python thường là `python3.13` (có pandas, python-docx, pywin32, pymupdf, nhưng không có yaml).
- **Lỗi in tiếng Việt (cp1252):** chạy với `-X utf8`. Lưu ý cờ `-I` làm Python bỏ qua `PYTHONIOENCODING`.
- **Nạp fork Ultralytics:** thư mục fork không tên `ultralytics`, nên phải tạo junction tạm như `danh_gia_pixel.import_fork()`. Thêm `PYTHONDONTWRITEBYTECODE=1` để không sinh `__pycache__` trong fork.
- **Shell có lớp bọc `rtk`:** một số lệnh `find`/`grep` phức tạp bị chặn. Dùng Python, hoặc `rtk proxy <lệnh>`.
- **Kaggle:**
  - mỗi tài khoản chỉ được **1 phiên GPU tương tác**; chạy song song phải dùng Save & Run All (Commit);
  - `kaggle kernels status/logs` chỉ đọc (log rỗng khi đang chạy);
  - Kaggle CLI 2.2.5 đã đăng nhập tài khoản `okeydokey0805`.
- **RAM máy:** thường chỉ còn khoảng 2 GiB trống. Script nạp cả bộ ảnh vào RAM, nên tắt bớt ứng dụng trước khi chạy.

## 8. File quan trọng mới tạo (06–07/11)

- `06_bao_cao/sua_theo_nhan_xet/`:
  - `KE_HOACH.md`, `CONTEXT.md`, `KIEM_KE_CHECKPOINT_ABLATION.md`.
- `.claude/skills/van-phong-bao-cao-nhom/SKILL.md`: văn phong của nhóm, áp dụng khi sửa Word.
- `02_ma_nguon/`:
  - `ultralytics_C2PSA_rong/`, `ultralytics_MambaPSA/`;
  - `notebook_kaggle/{pranet-new,unet-new}.ipynb` (bản 640), cùng `c2psa_rong/`, `mambapsa/`, `polyp_pvt/`, `vm_unet/`, `README_HUAN_LUYEN_BO_SUNG.md`.
- `00_tai_lieu_tong_quan/bang/ablation_10seed/`, `06_bao_cao/hinh/ablation_10seed/`: ablation 10 seed, ghi riêng, không đè bản 5 seed.
- `08_du_lieu_thuc_te/bang/`:
  - `tung_luot_ablation/`, `nen_cecum/`, `20seed/06_*.csv`, `20seed/07_*.csv`;
  - hai file `KET_QUA_*.md`.
