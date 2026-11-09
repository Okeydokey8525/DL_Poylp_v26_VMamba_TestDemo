# Phản hồi: checkpoint PraNet và U-Net bản 640 (20 seed mỗi mô hình)

Trả lời yêu cầu lấy checkpoint để đánh giá lại Bảng 4.8 theo nhận xét phản biện II.4. Kiểm tra ngày 09/11/2026 trên máy của Lương.

## 1. Tóm tắt

- **Đủ 40 file, không thiếu seed nào.** PraNet 640 có 20 file, U-Net 640 có 20 file, seed 0–19, không trùng.
- **Tên file checkpoint tốt nhất:**
  - PraNet: `pranet_best_s<SEED>.pth`
  - U-Net: `best_unet_s<SEED>.pth` (tiền tố `best_` đứng **trước**, không phải `unet_best_`)
- **Mỗi file là một `state_dict` thuần** (OrderedDict trọng số, khóa dạng `layer0.0.weight`…). File không chứa số epoch hay optimizer, nên nạp bằng `model.load_state_dict(torch.load(path, map_location="cpu"))`.
- **Dung lượng:** PraNet khoảng 94,4 MiB/file (tổng khoảng 1,84 GiB), U-Net khoảng 29,7 MiB/file (tổng khoảng 0,58 GiB). Tổng cộng khoảng 2,4 GiB. File `.pth` gần như không nén nhỏ thêm được.
- **Nơi lưu trong máy:** `Test_Mau/05_so_sanh_mo_hinh_khac/PraNet_640/` và `UNet_640/`, đúng cấu trúc bạn yêu cầu.

## 2. Đã kiểm tra những gì

1. **Đủ và không trùng:** mỗi thư mục `<Mô hình>_640_aug_s<SEED>/` (seed 0–19) có đúng một file best, một `last.pth`, một `results.csv`, một `tom_tat.txt`.
2. **Khớp với zip gốc tải từ Kaggle:** so CRC32 của từng file best trong máy với file cùng tên bên trong `runs_<Mô hình>_640_aug_s<SEED>.zip` (tab Output trên Kaggle). Kết quả: **40/40 khớp**. `tom_tat.txt` trong zip cũng giống từng ký tự bản trong máy.
3. **Khớp với git:** 40 file `tom_tat.txt` trong máy chính là bản đã commit ở `aba071e0` (`git status` sạch). Vậy checkpoint và `tom_tat.txt` trên git thuộc cùng một lượt chạy.
4. **Khớp `best_epoch`:** với mỗi seed, epoch có `val_dice` cao nhất trong `results.csv` trùng `best_epoch` và `best_val_dice` trong `tom_tat.txt` (40/40).
5. **Seed chạy lại nhiều lần:** chỉ có U-Net seed 10 và 17, mỗi seed bị tải trùng 1–2 lần (`runs_UNet_640_aug_s10 (1).zip`, `..._s17 (1).zip`, `..._s17 (2).zip`). Các bản này đã được so trước đó và giống hệt bản chính, nên không có hai phiên bản khác nhau.

Lưu ý: vì file `.pth` không lưu số epoch, "file best đúng là của epoch `best_epoch`" được xác nhận gián tiếp. File best và `tom_tat.txt` nằm trong cùng một zip đầu ra của cùng một lượt chạy, và notebook chỉ ghi file best khi `val_dice` vượt mức tốt nhất trước đó.

## 3. Tên notebook và version Kaggle

- Mã notebook trong repo: `02_ma_nguon/notebook_kaggle/pranet-new.ipynb` và `02_ma_nguon/notebook_kaggle/unet-new.ipynb` (bản 640 có tăng cường, ghi đè bản 352 cũ).
- **Tên notebook và số version trên Kaggle: chưa xác minh.** Thông tin này không lưu trong máy. Lương mở Kaggle → Your Work → notebook PraNet/U-Net → Versions để ghi lại:

| Mô hình | Tên notebook trên Kaggle | Version (theo seed) |
|---|---|---|
| PraNet 640 | _(Lương điền)_ | _(Lương điền)_ |
| U-Net 640 | _(Lương điền)_ | _(Lương điền)_ |

## 4. Cách gửi

- Nén hai thư mục, **chỉ lấy file best**, giữ nguyên cấu trúc:
  - `PraNet_640/PraNet_640_aug_s<SEED>/pranet_best_s<SEED>.pth`
  - `UNet_640/UNet_640_aug_s<SEED>/best_unet_s<SEED>.pth`
- Upload Google Drive rồi gửi link. **Không commit hay push `.pth` hoặc `.zip` lên git** (`.gitignore` đã chặn sẵn).
- Sau khi tải về, kiểm tra SHA-256 theo bảng ở mục 6. Trên PowerShell:

```powershell
Get-FileHash .\PraNet_640\PraNet_640_aug_s0\pranet_best_s0.pth -Algorithm SHA256
```

## 5. Cách khác, không cần gửi file

Máy của Lương đã có đủ checkpoint và GPU, nên có thể chạy đánh giá lại ngay trên máy (bước A3–A5 trong `KE_HOACH_HOAN_THIEN_NOP_BAI.md`):
- đánh giá theo pixel và topology, cùng giao thức với YOLO;
- vẽ lại hình;
- gửi CSV và hình cho bạn chèn vào Word.

Cách này tránh phải tải 2,4 GiB qua Drive.

## 6. Danh sách 40 file

Cột `best_val_dice` là Dice trên tập val theo cách tính của notebook huấn luyện (theo ảnh; ảnh nền không báo điểm nào được tính đúng hoàn toàn). Cách tính này **chưa cùng giao thức** với Dice theo pixel của YOLO trong Bảng 4.8.

| Mô hình | Seed | Đường dẫn | MiB | best_epoch | best_val_dice | SHA-256 |
|---|---:|---|---:|---:|---:|---|
| PraNet_640 | 0 | `PraNet_640/PraNet_640_aug_s0/pranet_best_s0.pth` | 94,4 | 56 | 0,9065 | `6085f70890069c4aab3a7383c43391f4b47f162493bec6cbbd6b4556190cc8b2` |
| PraNet_640 | 1 | `PraNet_640/PraNet_640_aug_s1/pranet_best_s1.pth` | 94,4 | 50 | 0,9025 | `becf2451f668a6376657e4bcfed8fc019ed1997f581498d33009fdb24d2d52a4` |
| PraNet_640 | 2 | `PraNet_640/PraNet_640_aug_s2/pranet_best_s2.pth` | 94,4 | 87 | 0,9080 | `dcaa8f9597b7eb0a049ec843164a7200b84fdb7e61ab22a2c8a3dee98c755c24` |
| PraNet_640 | 3 | `PraNet_640/PraNet_640_aug_s3/pranet_best_s3.pth` | 94,4 | 71 | 0,9052 | `4b3c5fd262b2ec6c7aa6c5a0ce5a2e3bd75ce6581c4ddb12a56bc59c872cc7de` |
| PraNet_640 | 4 | `PraNet_640/PraNet_640_aug_s4/pranet_best_s4.pth` | 94,4 | 43 | 0,9137 | `ac467d53a79917d381caf0fb53913292957f107fc48d0eb620cd34e3c104e201` |
| PraNet_640 | 5 | `PraNet_640/PraNet_640_aug_s5/pranet_best_s5.pth` | 94,4 | 53 | 0,9087 | `2cac89500c5fdbe2b2e196b334ed0cdc5739c8a3958bafb8c015d3db6227cae3` |
| PraNet_640 | 6 | `PraNet_640/PraNet_640_aug_s6/pranet_best_s6.pth` | 94,4 | 85 | 0,9086 | `9438e04e34eae372a0d890b0941579f7b83fb15fcf120a839be289d2b7a43cc5` |
| PraNet_640 | 7 | `PraNet_640/PraNet_640_aug_s7/pranet_best_s7.pth` | 94,4 | 59 | 0,9081 | `906b850d0404f078c5a331c048b5be2ba92fd2e4d3216423f84f3c62818773b1` |
| PraNet_640 | 8 | `PraNet_640/PraNet_640_aug_s8/pranet_best_s8.pth` | 94,4 | 64 | 0,9000 | `0f882d85203e20beb4744dae93620fab8ec788d82c4190a2ba39ecde86f8cedf` |
| PraNet_640 | 9 | `PraNet_640/PraNet_640_aug_s9/pranet_best_s9.pth` | 94,4 | 72 | 0,9140 | `86f1bcf52362c2bd3603c3c70807ad584dd76e55f25f90df99a64a070885ab2f` |
| PraNet_640 | 10 | `PraNet_640/PraNet_640_aug_s10/pranet_best_s10.pth` | 94,4 | 60 | 0,9066 | `e022dff33723b210bfd130760454400d20cf635502cd5e27a683385dbcc0d5c6` |
| PraNet_640 | 11 | `PraNet_640/PraNet_640_aug_s11/pranet_best_s11.pth` | 94,4 | 22 | 0,9036 | `b800eeff7a3c1e0ff3c12ab3a1f183d56a0ec191b0a25828a9b8481784676a1b` |
| PraNet_640 | 12 | `PraNet_640/PraNet_640_aug_s12/pranet_best_s12.pth` | 94,4 | 74 | 0,9136 | `b1772f639851f779000fc93a59b1da5059cff8f2266e1c7fcc897d47ddfdf9f8` |
| PraNet_640 | 13 | `PraNet_640/PraNet_640_aug_s13/pranet_best_s13.pth` | 94,4 | 69 | 0,9105 | `5306b6f8d8891d88e53664afa412646b91fb40e3dae6ffc18a5e5e26138bce44` |
| PraNet_640 | 14 | `PraNet_640/PraNet_640_aug_s14/pranet_best_s14.pth` | 94,4 | 55 | 0,9044 | `98cd2738b285069de5e4f2b90a22e24a6b787fc5c4e99cb1af45998f75e623ef` |
| PraNet_640 | 15 | `PraNet_640/PraNet_640_aug_s15/pranet_best_s15.pth` | 94,4 | 67 | 0,9147 | `2c8f5799256d4532870ce4b8320916b17fbc3f141012f0f87b7bc49d3daa5571` |
| PraNet_640 | 16 | `PraNet_640/PraNet_640_aug_s16/pranet_best_s16.pth` | 94,4 | 57 | 0,8970 | `dcf55a7a2a088ca82424db9c4d6fbc2c6d344c6bb7b3a33f26a3576e150f1c0b` |
| PraNet_640 | 17 | `PraNet_640/PraNet_640_aug_s17/pranet_best_s17.pth` | 94,4 | 53 | 0,9011 | `0bfffbde7c6d318dcb8ef33f55d6dad02f839bc45e325ad1b51b97f24524db97` |
| PraNet_640 | 18 | `PraNet_640/PraNet_640_aug_s18/pranet_best_s18.pth` | 94,4 | 80 | 0,9102 | `52accbdf75e944ccfcdc478b8a968bdb116f9486d1f2575f3db44cf30023ce6c` |
| PraNet_640 | 19 | `PraNet_640/PraNet_640_aug_s19/pranet_best_s19.pth` | 94,4 | 74 | 0,9073 | `964acea86831e6fd5dfd14f7ec0758a4598ffce26e7cd07f27c7fc423637f1fa` |
| UNet_640 | 0 | `UNet_640/UNet_640_aug_s0/best_unet_s0.pth` | 29,7 | 89 | 0,6060 | `8afb854abd6023e70bd7373c2f182894df05db7e81a3f4408b975277ba098145` |
| UNet_640 | 1 | `UNet_640/UNet_640_aug_s1/best_unet_s1.pth` | 29,7 | 96 | 0,6011 | `126a9be92dddc630a585e4801cc110a586ce7c7b7a29863fe32db4b819ae887c` |
| UNet_640 | 2 | `UNet_640/UNet_640_aug_s2/best_unet_s2.pth` | 29,7 | 82 | 0,6252 | `a45ea25a30feb9d6a30dd173c6babfba7685f6b1d6041c3fec95cc84c07cf41d` |
| UNet_640 | 3 | `UNet_640/UNet_640_aug_s3/best_unet_s3.pth` | 29,7 | 95 | 0,5977 | `6bef78ad44ac25ac98ada9b2b12a05203423eb787ce0fca1d09a0611a05a9694` |
| UNet_640 | 4 | `UNet_640/UNet_640_aug_s4/best_unet_s4.pth` | 29,7 | 89 | 0,6464 | `b6a82a010c75a51c5b69db91d6558f9892b89608723f9185bf3bdfde0a60e227` |
| UNet_640 | 5 | `UNet_640/UNet_640_aug_s5/best_unet_s5.pth` | 29,7 | 95 | 0,6506 | `5342d265930c391ba1f0c3b15d46673ed3cf33af5666a170288d6fd9c76f5dc2` |
| UNet_640 | 6 | `UNet_640/UNet_640_aug_s6/best_unet_s6.pth` | 29,7 | 84 | 0,6266 | `1ab2b8ad5c3624dba4eceea1b5f21c22b65f6c6758e9954d7da987204e20c747` |
| UNet_640 | 7 | `UNet_640/UNet_640_aug_s7/best_unet_s7.pth` | 29,7 | 86 | 0,5521 | `bb6ad8326dddd979a466cb7d36c11a5b6aa8003bd98d7aada1280827757f39f0` |
| UNet_640 | 8 | `UNet_640/UNet_640_aug_s8/best_unet_s8.pth` | 29,7 | 67 | 0,6409 | `6a96fa4392f8bc4a8369a418feb3f5b12ad9a62ddfe1bf49e340231a3f39cdff` |
| UNet_640 | 9 | `UNet_640/UNet_640_aug_s9/best_unet_s9.pth` | 29,7 | 73 | 0,6640 | `9a998803658199c17fe09c8d7a755915e31af61a464d17cbd486c6237c75983e` |
| UNet_640 | 10 | `UNet_640/UNet_640_aug_s10/best_unet_s10.pth` | 29,7 | 97 | 0,6187 | `dfdd4b5ab1978f954cf0aed6f8d06dcc49b27f6f3c7a657ab8aad0c2d0fea353` |
| UNet_640 | 11 | `UNet_640/UNet_640_aug_s11/best_unet_s11.pth` | 29,7 | 85 | 0,6634 | `73005677a8f15ffdcd0f1f88ecdaf98b281d22147cb316eed4839950486ffb01` |
| UNet_640 | 12 | `UNet_640/UNet_640_aug_s12/best_unet_s12.pth` | 29,7 | 100 | 0,6385 | `b805e0010d577e8341749644cb7843150826bd887a43df3de9678bad1ec86774` |
| UNet_640 | 13 | `UNet_640/UNet_640_aug_s13/best_unet_s13.pth` | 29,7 | 97 | 0,6330 | `17b267d81598b085f6c3ea1d1733ef797f58b0cc72f62a6b8c118e929e46126c` |
| UNet_640 | 14 | `UNet_640/UNet_640_aug_s14/best_unet_s14.pth` | 29,7 | 94 | 0,6177 | `24faa7e5a0ddf6f598e6b7cb55e41f091065df12e7470bad5ba18efb2d30ff0e` |
| UNet_640 | 15 | `UNet_640/UNet_640_aug_s15/best_unet_s15.pth` | 29,7 | 75 | 0,6062 | `f07f25776a199e595250e540d562fc817cee6e5c9c5ea7fa3fa0c5fefbb9aaf6` |
| UNet_640 | 16 | `UNet_640/UNet_640_aug_s16/best_unet_s16.pth` | 29,7 | 67 | 0,5896 | `0bc48fb9ff2f2af8c57520131c8f775894778276e896c1658f5ebd1edf4bc7ae` |
| UNet_640 | 17 | `UNet_640/UNet_640_aug_s17/best_unet_s17.pth` | 29,7 | 85 | 0,6351 | `d6087afbd7f99bff112010a09ebeef4be82b8f1c8576a9945a9cd1bd50dca1de` |
| UNet_640 | 18 | `UNet_640/UNet_640_aug_s18/best_unet_s18.pth` | 29,7 | 100 | 0,6404 | `349a51d59e4e8849c1c97606f8351923b7c0dce87aa51e3a9d49eb29a6d272d6` |
| UNet_640 | 19 | `UNet_640/UNet_640_aug_s19/best_unet_s19.pth` | 29,7 | 86 | 0,6305 | `6537d1d81edcac8b6bfca958052f3ccdcac3995b0769535761b3c25394238294` |

