# 📚 PROJECT KNOWLEDGE BASE

> Knowledge Base của dự án nghiên cứu VMamba + YOLO26-seg.
>
> **Snapshot ưu tiên:** 28/09/2026.  
> **Nguồn trạng thái:** `/CURRENT_PROJECT_STATUS.md` và `archive/doc/CURRENT_PROJECT_STATUS.md`.

## 1. Cách đọc Knowledge Base

### Current / Verified
Dùng trước:
- `CURRENT_PROJECT_STATUS.md`
- raw CSV/artifact trong `archive/Ket_Qua_V2/`
- source/config trong `archive/ultralytics_Topology-Shape-aware VMamba/`

### Historical
Các hồ sơ `00_...` đến `17_...` mô tả các giai đoạn nghiên cứu, thí nghiệm và sự cố đã xảy ra. Chúng được giữ để truy vết và không mặc định đại diện cho trạng thái hiện tại.

### Working rules
Đọc trước khi làm task quan trọng:
- `archive/doc/AI_WORK_OPTIMIZATION_RULE.md`
- `archive/doc/nguyen-tac-lam-viec-dai.md`

## 2. Tài liệu cốt lõi

- `00_TONG_QUAN_VA_TINH_HINH_DU_AN.md` — tổng quan/lịch sử giai đoạn nghiên cứu.
- `01_KIEN_TRUC_TSVM_TANG_10.md` — chi tiết TSVM Layer 10/P5.
- `01_KIEN_TRUC_C2IAVM_CHAMPION_VA_CAC_BIEN_THE.md` — hồ sơ C2IAVM, historical.
- `02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md` — kết quả đối chiếu cũ, đọc theo context.
- `03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md` — tài liệu cấu trúc/reproducibility.
- `04_KET_QUA_LOSS_VA_HOI_TU.md` đến `12_CHI_TIET_KET_QUA_IAVM_INTERACTIVE_ATTENTION_VMAMBA.md` — các hồ sơ phân tích từng hướng.
- `14_HUONG_8_INTERACTIVE_TOPOLOGY_VMAMBA.md` — hồ sơ ITSMamba.
- `15_CAM_NANG_PHONG_CACH_WORD_VA_NGON_NGU_HOC_THUAT.md` — phong cách báo cáo.
- `16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md` — BG20 và các thực nghiệm mở rộng.
- `17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md` — sự cố/fix artifact.
- `18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md` — báo cáo ánh xạ script và nguồn gốc dữ liệu 10-seed trong `Ket_Qua_V2/KQ_Nen_DX_10seed` (AI handoff cho GPT).
- `LICHSU_CAP_NHAT.md` — changelog.
- `training_results_audit.md` — audit kết quả.
- `kvasir_yolo_seg_output_spec.md` — đặc tả dữ liệu YOLO-seg.

## 3. Cấu trúc artifact hiện tại

Các nhóm chính trong GitHub:

- `archive/Ket_Qua_V1/`
- `archive/Ket_Qua_V2/`
- `archive/Kvasir-SEG/`
- `archive/Cac_Dataset/`
- `archive/Stracth/`
- `archive/ultralytics_Topology-Shape-aware VMamba/`

Không sử dụng các tên thư mục cũ trong tài liệu lịch sử như `archive/Ket_Qua/` nếu tree hiện tại không có chúng.

## 4. Dataset và kết quả hiện tại

BG20:

- 1.200 ảnh.
- 1.040 train.
- 160 validation.
- 120 validation ảnh polyp + 40 background.
- 127 ground-truth polyp instances trong phần validation polyp.

Bộ 10-seed chính gồm Baseline, TSVM, P5 Attention-VMamba và ITSMamba. IAVM chưa đủ 10 seed trong repository.

## 5. Quy tắc sử dụng tài liệu

- Không lấy một tài liệu historical làm source of truth cho current state.
- Không tự tạo số liệu.
- Không sửa raw CSV để khớp báo cáo.
- Nếu source/config chưa tồn tại trên GitHub, không mô tả nó là implementation hiện tại.
- Khi local/Kaggle mới hơn GitHub, phải ghi rõ trạng thái chưa đồng bộ.
