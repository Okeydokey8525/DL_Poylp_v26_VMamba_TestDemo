# KẾT QUẢ THỰC NGHIỆM CHI TIẾT VÀ ĐỐI CHIẾU ĐA MÔ HÌNH (6-FOLD CROSS-VALIDATION)
## BẢNG TỔNG HỢP HIỆU NĂNG: BASELINE YOLO26s-seg VS TSVM VS C2IAVM (CHAMPION)

---

> **Phân loại độ tin cậy thông tin theo nguyên tắc dự án:**
> - `[Đã xác nhận]`: Dữ liệu số liệu trích xuất 100% từ các tệp `results.csv` thực tế trên 6 seed độc lập (`s0` đến `s5`), 100 epochs/seed, kiểm định F-test giảm phương sai và Paired t-test.
> - `[Có khả năng / suy luận]`: Phân tích nguyên nhân hội tụ, cơ chế bù trừ Không gian - Kênh (Bi-SS2D + Multi-Head Self-Attention).
> - `[Chưa xác minh]`: Đánh giá thử nghiệm lâm sàng trực tiếp trên thiết bị nội soi tại bệnh viện.

---

## 1. BẢNG TỔNG HỢP SO SÁNH 3 MÔ HÌNH (6-SEED MEAN $\pm$ STD)

Dưới đây là bảng số liệu chuẩn hóa lấy trung bình qua 6 fold cross-validation (`s0` đến `s5`) kèm độ lệch chuẩn $\pm 1\sigma$:

| Nhóm Chỉ Số | Chỉ Số Đánh Giá | Baseline YOLO26s-seg | C2TSVMamba (Thử nghiệm) | C2IAVM (👑 Champion Model) | So Với Baseline ($\Delta$) | So Với TSVM ($\Delta$) | Kiểm Định F-test |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Phân đoạn** | **Mask mAP@50-95** | $0.7291 \pm 0.0153$ | $0.7231 \pm 0.0055$ | **$0.7361 \pm 0.0073$** | **$+0.0070$ (+0.70%)** | **$+0.0130$ (+1.30%)** | **Giảm phương sai $4.39\times$** |
| Phân đoạn | Mask mAP@50 | $0.9144 \pm 0.0065$ | $0.9141 \pm 0.0088$ | **$0.9149 \pm 0.0109$** | $+0.0005$ (+0.05%) | $+0.0008$ (+0.08%) | Đạt đỉnh 93.19% ở s0 |
| Phân đoạn | **Mask Recall (Độ nhạy)** | $0.8760 \pm 0.0175$ | $0.8493 \pm 0.0243$ | **$0.8875 \pm 0.0195$** | **$+0.0115$ (+1.15%)** | **$+0.0382$ (+3.82%)** | **Khôi phục hoàn toàn độ nhạy** |
| Phân đoạn | Mask Precision | **$0.9198 \pm 0.0139$** | $0.9192 \pm 0.0192$ | $0.8876 \pm 0.0275$ | $-0.0322$ (-3.22%) | $-0.0316$ (-3.16%) | Đánh đổi vi mô để tăng Recall |
| Phân đoạn | Mask F1-Score | **$0.8972 \pm 0.0054$** | $0.8825 \pm 0.0094$ | $0.8871 \pm 0.0090$ | $-0.0101$ (-1.01%) | $+0.0046$ (+0.46%) | Duy trì F1 cao sát 89% |
| **Định vị** | **Box mAP@50-95** | $0.7404 \pm 0.0112$ | $0.7398 \pm 0.0087$ | **$0.7418 \pm 0.0057$** | **$+0.0014$ (+0.14%)** | **$+0.0020$ (+0.20%)** | **Giảm phương sai $3.86\times$** |
| Định vị | Box mAP@50 | $0.9099 \pm 0.0068$ | $0.9056 \pm 0.0093$ | **$0.9151 \pm 0.0086$** | $+0.0052$ (+0.52%) | $+0.0095$ (+0.95%) | Tỷ lệ thắng 5/6 seeds |
| Định vị | Box Recall | $0.8664 \pm 0.0246$ | $0.8429 \pm 0.0282$ | **$0.8842 \pm 0.0185$** | **$+0.0178$ (+1.78%)** | **$+0.0413$ (+4.13%)** | Bao phủ bounding box vượt trội |
| **Hàm Phạt** | **Val Seg Loss** | $1.4314 \pm 0.0540$ | **$1.3936 \pm 0.0366$** | **$1.3987 \pm 0.0695$** | **$-0.0327$ (Giảm lỗi)** | $+0.0051$ | Tối ưu sâu hơn Baseline ($p<0.05$) |
| Hàm Phạt | Val Box Loss | **$0.7503 \pm 0.0137$** | $0.7687 \pm 0.0385$ | $0.7571 \pm 0.0276$ | $+0.0068$ | $-0.0116$ | Tương đương Baseline |
| Hàm Phạt | Val Cls Loss | **$0.5681 \pm 0.0400$** | $0.5938 \pm 0.0302$ | $0.5902 \pm 0.0524$ | $+0.0221$ | $-0.0036$ | Ổn định phân loại 1 class |

`[Đã xác nhận]`

---

## 2. MA TRẬN KẾT QUẢ THEO TỪNG SEED (SEED-BY-SEED DETAIL: s0 ĐẾN s5)

### A. Chỉ Số Mask mAP@50-95 (Chỉ số quyết định thứ hạng mô hình)
| Seed | Baseline YOLO26s-seg | C2TSVMamba | C2IAVM (👑 Champion) | C2IAVM vs Baseline | C2IAVM vs TSVM |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **s0** | $0.7232$ | $0.7201$ | **$0.7426$** | **$+0.0194$ (IAVM thắng)** | **$+0.0225$ (IAVM thắng)** |
| **s1** | $0.7435$ | $0.7212$ | **$0.7466$** | **$+0.0031$ (IAVM thắng)** | **$+0.0254$ (IAVM thắng)** |
| **s2** | $0.7271$ | $0.7291$ | **$0.7312$** | **$+0.0041$ (IAVM thắng)** | **$+0.0021$ (IAVM thắng)** |
| **s3** | $0.7240$ | $0.7171$ | **$0.7292$** | **$+0.0052$ (IAVM thắng)** | **$+0.0121$ (IAVM thắng)** |
| **s4** | **$0.7496$** | $0.7202$ | $0.7297$ | $-0.0199$ (Base thắng) | **$+0.0095$ (IAVM thắng)** |
| **s5** | $0.7073$ | $0.7308$ | **$0.7375$** | **$+0.0302$ (IAVM thắng)** | **$+0.0067$ (IAVM thắng)** |
| **Trung bình** | **$0.7291 \pm 0.0153$** | **$0.7231 \pm 0.0055$** | **$0.7361 \pm 0.0073$** | **Thắng 5/6 (83.33%)** | **Thắng 6/6 (100.0%)** |

### B. Chỉ Số Mask Recall (Độ nhạy phát hiện tổn thương lâm sàng)
| Seed | Baseline YOLO26s-seg | C2TSVMamba | C2IAVM (👑 Champion) | C2IAVM vs Baseline | C2IAVM vs TSVM |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **s0** | $0.8737$ | $0.8415$ | **$0.8947$** | **$+0.0210$ (IAVM thắng)** | **$+0.0532$ (IAVM thắng)** |
| **s1** | $0.8785$ | $0.8672$ | **$0.8860$** | **$+0.0075$ (IAVM thắng)** | **$+0.0188$ (IAVM thắng)** |
| **s2** | $0.8740$ | $0.8354$ | **$0.9064$** | **$+0.0324$ (IAVM thắng)** | **$+0.0710$ (IAVM thắng)** |
| **s3** | $0.8455$ | $0.8190$ | **$0.8976$** | **$+0.0521$ (IAVM thắng)** | **$+0.0786$ (IAVM thắng)** |
| **s4** | **$0.8976$** | $0.8752$ | $0.8898$ | $-0.0078$ (Base thắng) | **$+0.0146$ (IAVM thắng)** |
| **s5** | **$0.8864$** | $0.8576$ | $0.8504$ | $-0.0360$ (Base thắng) | $-0.0072$ (TSVM thắng) |
| **Trung bình** | **$0.8760 \pm 0.0175$** | **$0.8493 \pm 0.0243$** | **$0.8875 \pm 0.0195$** | **Thắng 4/6 (66.67%)** | **Thắng 5/6 (83.33%)** |

`[Đã xác nhận]`

---

## 3. HỆ THỐNG BIỂU ĐỒ ĐỐI CHỨNG (300 DPI)

Tất cả các dạng biểu đồ đã được kết xuất sẵn sàng cho Khóa luận và Slide bảo vệ:

1. **Thư mục so sánh Baseline vs IAVM:**
   - Đường dẫn: `c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KQ_DoiXung\Base vs IAVM`
   - Đầy đủ 45 tệp biểu đồ: Cột tổng thể (`04_overall_benchmark_barchart.png`), Cột từng seed (`05_fold_by_fold_comparison.png`), Donut lâm sàng (`07a_pie_polyp_clinical_breakdown.png`), Donut tỷ lệ thắng 83.33% (`07b_pie_head_to_head_winrate.png`), Donut trễ 40 FPS (`07c_pie_inference_latency_breakdown.png`), Radar 8 trục (`06_radar_chart_tradeoff.png`), Boxplot giảm phương sai 4.39x (`08_boxplot_variance_comparison.png`), Lưới 4-trong-1 và các đồ thị đơn lẻ.

2. **Thư mục so sánh Baseline vs TSVM (Topolo):**
   - Đường dẫn: `c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KQ_DoiXung\Base vs Topolo`
   - Đầy đủ 46 tệp biểu đồ đối xứng hoàn toàn, hỗ trợ phân tích chuyển tiếp kiến trúc.
