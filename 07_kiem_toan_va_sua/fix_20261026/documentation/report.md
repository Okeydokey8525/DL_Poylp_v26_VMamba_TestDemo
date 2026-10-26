# Chỉnh sửa tài liệu và khả năng tái lập ngày 26 tháng 10 năm 2026

Đã sửa tài liệu và script hỗ trợ trong phạm vi được giao; không sửa Word (parent xử lý riêng), Web, raw CSV, checkpoint, nhãn hay hình kết quả gốc. Các bản sao trước sửa nằm trong `backups/`; `documentation_changes.json` ghi hash trước/sau của từng tệp.

## Thay đổi

- Thay `doc/README.md` và `doc/CURRENT_PROJECT_STATUS.md` bằng điểm vào 20 seed FP32; lưu snapshot cũ; phân biệt max-mask với best-fitness và kết quả replay checkpoint. Không đổi endpoint hay p-value chính.
- Sửa `doc/01_KIEN_TRUC_TSVM_TANG_10.md` theo source: layer10/P5, kích thước sau scale s, gate1+G, không ratio4, FFN haiConv1×1, workO(LlogL)/depthO(logL), không hứa AMP/topology/backward đã được chứng minh.
- Thêm `doc/28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md`; sửa `data_bg20.yaml` tới dữ liệu hiện hành. Hướng dẫn ghi đúng builder BG20, thư mục normal-cecum lồng, môi trường và sai khác999/1000nhãn đã xác nhận.
- Builder BG20 tự tìm archive/source hiện tại, có `--dry-run`, `--output`, không xóa/merge thư mục hiện hữu và không ghi root YAML. Output mặc định là bản replay mới; từ chối nằm trong nguồn, canonicaldataset hoặc rawrun. Có fallback khi thiếu tqdm; thuật toán chuyển mask và seed không thay đổi.
- Đánh dấu21hồ sơ/ghi chú cũ và11bản thảo Markdown là lịch sử. Riêng hồ sơ27 giữ vai trò giải thích cơ chế FP16; chỉ trạng thái cũ bị thay thế. Parent README/CURRENT được thêm redirect, phần snapshot nguyên văn giữ lại.
- Thêm `LEGACY_ARTIFACTS.md` và sửa READMEgói20seed để ngăn dùng TN_reconstructed và thắngloss đảo chiều; trỏ đúng bảng mới TSVM14vsBaseline6. Không thay bất kỳ byte CSV/JSON/PNGcũ.
- Chặn builder Word Markdown lịch sử ở chế độ mặc định. Muốn xuất lịch sử phải opt-in và chọn tệp mới; luôn từ chối hai Word chính hoặc output đã tồn tại. Không tạo Word trong các phép kiểm guard.

## Kiểm chứng

- `--help` và `--dry-run` chạy được trên Python app venv; dry-run không tạo output.
- Full build vào `fix_20261026/documentation/reproduced_bg20`:1.040train/160val,160/40nhãn rỗng,936/127instances. 1.200ảnh và danh sách200ảnh nền khớp byte; nhãn999/1000khớp, đúng một khác biệt đã được kiểm toán trước đó. Không đưa output replay vào dữ liệu huấn luyện hiện hành.
- Các lệnh output đã tồn tại/canonical dataset và ghi đè Word chính đều bị chặn, exit2. Canonical child cũng bị từ chối, không tạo thư mục.
- Sáu Markdown hiện hành không có link nội bộ thiếu;11bản thảo có marker lịch sử; Python hỗ trợ parse được.
- 2494tệp dữ liệu/CSV/JSON/PNGnguồn được so với manifest kiểm toán cũ:0thay đổi/mất. `protected_sources_check.json` lưu chi tiết.

## Phần chưa đóng

Không sửa nhãn sai khác một đỉnh, không khẳng định split880/120 do tác giả phát hành, không đánh giáTurnitin30%. Trạng thái Web sau sửa được parent cập nhật theo kiểm thử thật sau khi gộp các phòng; tài liệu không tự ghi pass chỉ vì code đổi.

## Tệp thay đổi

- `doc\historical\snapshots_20261026\README_SNAPSHOT.md`
- `doc\README.md`
- `doc\CURRENT_PROJECT_STATUS.md`
- `doc\01_KIEN_TRUC_TSVM_TANG_10.md`
- `doc\28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md`
- `Ket_Qua_V2\KQ_Nen_DX_20seed_FP32\README.md`
- `Ket_Qua_V2\KQ_Nen_DX_20seed_FP32\LEGACY_ARTIFACTS.md`
- `doc\00_TONG_QUAN_VA_TINH_HINH_DU_AN.md`
- `doc\03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md`
- `doc\04_KET_QUA_LOSS_VA_HOI_TU.md`
- `doc\06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md`
- `doc\07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md`
- `doc\08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md`
- `doc\10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md`
- `doc\16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md`
- `doc\17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md`
- `doc\18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md`
- `doc\20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md`
- `doc\21_HUONG_DAN_BAN_GIAO_AI_MOI_VA_VIEC_CONG_TAI.md`
- `doc\22_DANH_MUC_HINH_ANH_TOAN_BO.md`
- `doc\23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md`
- `doc\24_DANH_SACH_DUONG_DAN_HONG.md`
- `doc\25_KICH_BAN_PHAN_BIEN_SU_CO_FUSE_VA_MA_TRAN_NHAM_LAN.md`
- `doc\26_KET_QUA_BASELINE_VS_TSVM_BG20_21SEED_0_20.md`
- `doc\27_SU_CO_FP16_CHECKPOINT_TSVM_VA_CACH_KHAC_PHUC.md`
- `doc\GIAI_THICH_SU_CO_FUSE_CHO_NGUOI_DOC.md`
- `doc\training_results_audit.md`
- `doc\WEEKLY_REPORT_Ket_Qua_V2.md`
- `Bao_cao\md viet bao cao\00_TRANG_BIA_VA_DANH_MUC.md`
- `Bao_cao\md viet bao cao\01_PHAN_MO_DAU.md`
- `Bao_cao\md viet bao cao\02_CHUONG_1_TONG_QUAN_VA_CO_SO_NGHIEN_CUU.md`
- `Bao_cao\md viet bao cao\03_CHUONG_2_PHAN_TICH_VA_THIET_KE_MO_HINH_DE_XUAT.md`
- `Bao_cao\md viet bao cao\04_CHUONG_3_XAY_DUNG_BO_DU_LIEU_VA_TIEN_XU_LY.md`
- `Bao_cao\md viet bao cao\05_CHUONG_4_CAI_DAT_THUAT_TOAN_VA_UNG_DUNG_MINH_HOA.md`
- `Bao_cao\md viet bao cao\06_CHUONG_5_THU_NGHIEM_VA_DANH_GIA_KET_QUA.md`
- `Bao_cao\md viet bao cao\07_KET_LUAN_VA_HUONG_PHAT_TRIEN.md`
- `Bao_cao\md viet bao cao\08_TAI_LIEU_THAM_KHAO.md`
- `Bao_cao\md viet bao cao\09_PHU_LUC_A_B_C_D_SO_LIEU_THUC_NGHIEM.md`
- `Bao_cao\md viet bao cao\10_PHU_LUC_E_F_G_H_BENCHMARK_NOTEBOOK_UNG_DUNG.md`
- `..\README.md`
- `..\CURRENT_PROJECT_STATUS.md`
- `doc\LICHSU_CAP_NHAT.md`
- `data_bg20.yaml`
- `Ket_Qua_V2\Data Prosessing\convert_kvasir_with_background_to_yolo_seg.py`
- `Stracth\Bao_Cao\build_huit_final_report_from_md.py`
- `doc\historical\snapshots_20261026\01_KIEN_TRUC_TSVM_TANG_10.md`
- `doc\historical\snapshots_20261026\CURRENT_PROJECT_STATUS.md`
- `doc\historical\snapshots_20261026\README.md`
