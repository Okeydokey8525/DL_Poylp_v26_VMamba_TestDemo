# DANH MỤC HÌNH VẼ KHUYẾN NGHỊ CHO LUẬN VĂN (RECOMMENDED FIGURES FOR THESIS)
## Các Biểu đồ Khoa học Trích xuất từ Thực nghiệm 10 Seed (Kvasir-SEG BG20 — Baseline vs TSVM)

Tài liệu này chọn lọc và hướng dẫn cách đưa biểu đồ từ `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/` vào luận văn, kèm chú thích học thuật và mã LaTeX chuẩn.

> 🔴 **GHI CHÚ SỬA ĐỔI (02/10/2026):**
> 1. **Đường dẫn hình cũ (`02_distributions/`, `03_seed_by_seed/`, `04_confusion_matrix/`, `05_multimetric/`) không tồn tại** — cấu trúc thư mục đã được tái tổ chức. Đã cập nhật lại toàn bộ đường dẫn và **đã kiểm tra từng tệp tồn tại thực tế**.
> 2. **Bảng số liệu LaTeX ở mục 3 đã sai** (Box mAP50-95, Mask mAP50, Val Loss, và 5 giá trị *p*-value). Đã thay bằng số liệu tái trích xuất từ `results.csv`.
> 3. **Cỡ mẫu "167 ảnh" → 160 ảnh** (127 thực thể polyp + 40 ảnh nền).
> 4. **Số liệu ma trận nhầm lẫn đã sửa** và bổ sung cảnh báo về giới hạn dữ liệu CM.
> 5. Hình CM **không nên đặt là hình chính** — xem hộp cảnh báo ở mục 1.3.

---

### 1. Danh sách Hình Khuyến nghị Cốt lõi

#### 1.1. Nhóm hình an toàn — khuyến nghị dùng chính

| Mã Hình | Đường dẫn Tệp (đã kiểm tra tồn tại) | Nội dung Khoa học | Vai trò trong Luận Văn |
| :--- | :--- | :--- | :--- |
| **Hình 1** | `05_charts/performance/01_mask_map50_95_comparison.png` | So sánh Mean ± Std Mask mAP@50-95 | Chỉ số hiệu năng chính của bài toán phân đoạn |
| **Hình 2** | `05_charts/performance/05_val_seg_loss_comparison.png` | So sánh Validation Segmentation Loss | Hàm mất mát phân đoạn, khía cạnh giảm rõ nhất (−4.76%) |
| **Hình 3** | `05_charts/distribution/08_boxplot_mask_map50_95.png` | Boxplot + điểm dữ liệu phân tán 10 seed | Trực quan hóa độ co cụm phương sai (Std giảm 39.7%) |
| **Hình 4** | `05_charts/stability/10_mean_std_errorbars.png` | Thanh sai số Mean ± Std đa chỉ số | Tổng hợp sai số mẫu trên nhiều chỉ số cùng lúc |
| **Hình 5** | `05_charts/summary/20_delta_tsvm_vs_baseline.png` | Thanh ngang độ lệch Δ (TSVM − Baseline) | Tổng quan độ lớn và dấu của mọi chênh lệch |

#### 1.2. Nhóm hình bổ trợ

| Mã Hình | Đường dẫn Tệp (đã kiểm tra tồn tại) | Nội dung Khoa học | Vai trò trong Luận Văn |
| :--- | :--- | :--- | :--- |
| Hình 6 | `05_charts/performance/03_precision_recall_comparison.png` | Đánh đổi Precision / Recall | Phân tích trade-off phân đoạn |
| Hình 7 | `05_charts/stability/06_seed_mask_map50_95_trends.png` | Diễn biến Mask mAP@50-95 qua 10 seed | Minh họa biến thiên giữa các lần khởi tạo |
| Hình 8 | `figures/04_convergence_loss_curves.png` | Đường cong hội tụ 4 hàm mất mát qua 100 epoch | Động học huấn luyện |
| Hình 9 | `figures/11_boxplot_variance_stability.png` | Boxplot + jitter (mẫu 2 mô hình) | Bổ trợ Hình 3 ở góc nhìn template khác |
| Hình 10 | `05_charts/summary/18_grouped_bar_main_metrics.png` | Grouped bar 6 chỉ số chính | Tổng quan trực quan |

#### 1.3. ⚠️ Nhóm hình ma trận nhầm lẫn — CẢNH BÁO TRƯỚC KHI DÙNG

| Mã Hình | Đường dẫn Tệp | Nội dung | Cảnh báo |
| :--- | :--- | :--- | :--- |
| Hình C1 | `figures/12_confusion_matrix_mean_comparison.png` | Ma trận nhầm lẫn chuẩn hóa trung bình | ⚠️ Chứa ô **TN là số tái dựng**, không phải số đo |
| Hình C2 | `figures/14_confusion_cells_grouped_barchart.png` | Cột nhóm TP / FN / FP / TN | ⚠️ Như trên |

**Ba lý do nên đặt hình CM ở vị trí phụ (không phải hình chính):**

1. **Ô TN không được Ultralytics đo.** Trong `ultralytics/utils/metrics.py` (`ConfusionMatrix.process_batch`, dòng 427–434), khi ảnh nền không có ground-truth, code **chỉ cộng FP** và **không có nhánh `matrix[self.nc, self.nc] += 1`**. Ô background↔background luôn bằng 0, bị loại khỏi ghi nhãn (dòng 550) và hiển thị **trống** — xác nhận trên cả 20 ảnh `confusion_matrix.png`. Giá trị TN trong dữ liệu CSV **đúng bằng $40 - FP$** ở cả 20 dòng → là **số tái dựng theo giả định**, không phải số đo thực nghiệm.
2. **3/20 lượt chạy không đối chiếu được.** Đối chiếu OCR với ảnh `confusion_matrix.png`: **17/20** run khớp chính xác; **TSVM s0, s5, s8** không khớp (ảnh cho thấy recall gần 0, mâu thuẫn với `results.csv` của chính các run đó).
3. **Giả định ẩn.** Việc suy dựng TN ngầm giả định mỗi ảnh nền sinh tối đa 1 báo động giả.

> **Nếu vẫn dùng hình CM**, chú thích **bắt buộc** phải chứa câu: *"Ô True Negative được tái dựng theo giả định $N_{TN} = 40 - N_{FP}$ do mã nguồn Ultralytics không ghi nhận ô background↔background; ô này hiển thị trống trên toàn bộ 20 ảnh ma trận nhầm lẫn gốc. Ba trong hai mươi lượt chạy (TSVM s0, s5, s8) không đối chiếu được với ảnh gốc do artifact thuộc lượt validation bị lỗi."*

---

### 2. Chi tiết Từng Hình & Mã LaTeX Chuẩn Mực

#### Hình 1: So sánh Mask mAP@50-95 (Chỉ số hiệu năng chính)
- **Tệp nguồn**: `Ket_Qua_V2/KQ_Nen_DX_10seed/05_charts/performance/01_mask_map50_95_comparison.png`
- **Diễn giải học thuật**:
  > *Biểu đồ cột so sánh giá trị trung bình Mask mAP@50-95 kèm thanh sai số độ lệch chuẩn mẫu của TSVM ($0.7246 \pm 0.0078$) và Baseline ($0.7210 \pm 0.0129$) trên 10 lần khởi tạo ngẫu nhiên độc lập. Chênh lệch giá trị trung bình là $+0.0036$ ($+0.49\%$), không có ý nghĩa thống kê ($p = 0.3839$, kiểm định paired $t$-test, $N = 10$); tuy nhiên độ lệch chuẩn của TSVM thấp hơn $39.7\%$ và khoảng biến thiên hẹp hơn $35.7\%$.*

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\linewidth]{figures/01_mask_map50_95_comparison.png}
    \caption{So sánh Mask mAP@50-95 giữa YOLO26s-seg Baseline và TSVM qua 10 lần khởi tạo ngẫu nhiên độc lập (Seed 0--9). Thanh sai số biểu diễn độ lệch chuẩn mẫu.}
    \label{fig:mask_map50_95_10seed}
\end{figure}
```

---

#### Hình 2: Hàm mất mát phân đoạn trên tập thẩm định
- **Tệp nguồn**: `Ket_Qua_V2/KQ_Nen_DX_10seed/05_charts/performance/05_val_seg_loss_comparison.png`
- **Diễn giải học thuật**:
  > *Validation Segmentation Loss trung bình của TSVM thấp hơn Baseline ($1.2424 \pm 0.0387$ so với $1.3045 \pm 0.0867$), tương ứng mức giảm $-4.76\%$ với $p = 0.0908$ (tiệm cận ngưỡng $\alpha = 0.10$, chưa đạt ý nghĩa ở $\alpha = 0.05$). Độ lệch chuẩn giảm $55.4\%$, cho thấy hàm mất mát hội tụ ổn định hơn giữa các lần chạy.*

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\linewidth]{figures/05_val_seg_loss_comparison.png}
    \caption{So sánh hàm mất mát phân đoạn mặt nạ trên tập thẩm định (Validation Segmentation Loss) giữa Baseline và TSVM qua 10 seed. Thanh sai số biểu diễn độ lệch chuẩn mẫu.}
    \label{fig:val_seg_loss_10seed}
\end{figure}
```

---

#### Hình 3: Phân phối hiệu năng và độ ổn định (Boxplot)
- **Tệp nguồn**: `Ket_Qua_V2/KQ_Nen_DX_10seed/05_charts/distribution/08_boxplot_mask_map50_95.png`
- **Diễn giải học thuật**:
  > *Biểu đồ hộp kèm các điểm dữ liệu phân tán của Mask mAP@50-95 qua 10 seed. Hộp phân vị của TSVM co cụm chặt hơn Baseline, thể hiện độ lệch chuẩn giảm từ $0.01285$ xuống $0.00776$ và đáy hiệu năng được nâng từ $0.6941$ lên $0.7065$. Đây là quan sát mô tả phân bố thực nghiệm, không phải bằng chứng về cơ chế kiến trúc.*

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\linewidth]{figures/08_boxplot_mask_map50_95.png}
    \caption{Phân phối thực nghiệm của Mask mAP@50-95 qua 10 seed, thể hiện bằng biểu đồ hộp kèm điểm dữ liệu từng lần chạy. Phản ánh mức co cụm phương sai của TSVM so với Baseline.}
    \label{fig:boxplot_mask_map50_95}
\end{figure}
```

---

#### Hình 4: Thanh sai số Mean ± Std đa chỉ số
- **Tệp nguồn**: `Ket_Qua_V2/KQ_Nen_DX_10seed/05_charts/stability/10_mean_std_errorbars.png`
- **Diễn giải học thuật**:
  > *Tổng hợp độ lệch chuẩn mẫu trên nhiều chỉ số. TSVM có độ rộng thanh sai số nhỏ hơn Baseline trên 8/12 chỉ số; ngoại lệ đáng chú ý là Validation Classification Loss, nơi TSVM vừa tăng giá trị trung bình ($+9.97\%$) vừa tăng độ phân tán.*

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/10_mean_std_errorbars.png}
    \caption{Biểu đồ thanh sai số Mean $\pm$ Std đa chỉ số, thể hiện mức ổn định phương sai của TSVM so với Baseline trên 10 seed.}
    \label{fig:mean_std_errorbars}
\end{figure}
```

---

#### Hình 5: Độ lệch Δ giữa TSVM và Baseline
- **Tệp nguồn**: `Ket_Qua_V2/KQ_Nen_DX_10seed/05_charts/summary/20_delta_tsvm_vs_baseline.png`
- **Diễn giải học thuật**:
  > *Tổng quan độ lớn và dấu của mọi chênh lệch Δ (TSVM − Baseline). Không chỉ số nào vượt ngưỡng ý nghĩa thống kê α = 0.05; hai chỉ số Val Seg Loss ($p = 0.0908$) và Val Cls Loss ($p = 0.0943$) chỉ tiệm cận α = 0.10 và có dấu trái chiều nhau.*

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/20_delta_tsvm_vs_baseline.png}
    \caption{Biểu đồ thanh ngang tổng hợp độ lệch $\Delta$ (TSVM $-$ Baseline) trên toàn bộ chỉ số đo lường.}
    \label{fig:delta_tsvm_vs_baseline}
\end{figure}
```

---

#### Hình C1 (⚠️): Ma trận nhầm lẫn chuẩn hóa trung bình
- **Tệp nguồn**: `Ket_Qua_V2/KQ_Nen_DX_10seed/figures/12_confusion_matrix_mean_comparison.png`
- **Diễn giải học thuật (bắt buộc kèm cảnh báo)**:
  > *Ma trận nhầm lẫn chuẩn hóa trung bình qua 10 seed tại ngưỡng $conf = 0.25$. Trên 120 ảnh chứa polyp (127 thực thể ground-truth), TSVM ghi nhận tỷ lệ phát hiện đúng $87.56\%$ so với $86.85\%$ của Baseline. Trên 40 ảnh nền âm tính, tỷ lệ báo động giả giảm từ $42.00\%$ xuống $36.50\%$. **Lưu ý:** ô True Negative là giá trị tái dựng theo giả định $N_{TN} = 40 - N_{FP}$, do mã nguồn Ultralytics không ghi nhận ô background–background (ô này hiển thị trống trên toàn bộ 20 ảnh ma trận nhầm lẫn gốc); ba trong hai mươi lượt chạy (TSVM s0, s5, s8) không đối chiếu được với ảnh gốc do artifact thuộc lượt validation bị lỗi.*

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\linewidth]{figures/12_confusion_matrix_mean_comparison.png}
    \caption{Ma trận nhầm lẫn chuẩn hóa trung bình qua 10 seed trên tập kiểm định gồm 160 ảnh (120 ảnh chứa polyp với $N=127$ thực thể ground-truth, và 40 ảnh nền âm tính). Ô True Negative được tái dựng theo giả định $N_{TN}=40-N_{FP}$ do mã nguồn Ultralytics không ghi nhận ô background--background.}
    \label{fig:confusion_matrix_10seed}
\end{figure}
```

---

### 3. Bảng Số liệu Khuyến nghị Đưa vào Báo cáo

*Bảng tổng hợp đã được kiểm chứng lại 100% từ `02_statistics/mean_std/full_comparison_mean_std.csv`:*

```latex
\begin{table}[htbp]
\centering
\caption{Tổng hợp so sánh hiệu năng 10 seed giữa Baseline và TSVM trên tập dữ liệu Kvasir-SEG (BG20). Giá trị trình bày dưới dạng Trung bình $\pm$ Độ lệch chuẩn mẫu; $\Delta$ là chênh lệch TSVM $-$ Baseline.}
\label{tab:10seed_benchmark_results}
\small
\begin{tabular}{lcccc}
\hline
\textbf{Chỉ số (Metric)} & \textbf{Baseline} & \textbf{TSVM (Đề xuất)} & \textbf{Chênh lệch ($\Delta$)} & \textbf{$p$-value ($t$-test)} \\
\hline
Mask mAP@50-95 & $0.7210 \pm 0.0129$ & $0.7246 \pm 0.0078$ & $+0.0036$ $(+0.49\%)$ & $0.3839$ \\
Mask mAP@50    & $0.9119 \pm 0.0107$ & $0.9062 \pm 0.0082$ & $-0.0056$ $(-0.62\%)$ & $0.2273$ \\
Mask Precision & $0.9023 \pm 0.0339$ & $0.9118 \pm 0.0246$ & $+0.0095$ $(+1.05\%)$ & $0.5428$ \\
Mask Recall    & $0.8584 \pm 0.0252$ & $0.8625 \pm 0.0173$ & $+0.0041$ $(+0.48\%)$ & $0.5907$ \\
Box mAP@50-95  & $0.7262 \pm 0.0198$ & $0.7285 \pm 0.0141$ & $+0.0023$ $(+0.32\%)$ & $0.7152$ \\
Box mAP@50     & $0.9011 \pm 0.0116$ & $0.9006 \pm 0.0090$ & $-0.0004$ $(-0.05\%)$ & $0.9334$ \\
Box Precision  & $0.8992 \pm 0.0326$ & $0.9062 \pm 0.0251$ & $+0.0070$ $(+0.78\%)$ & $0.5921$ \\
Box Recall     & $0.8434 \pm 0.0337$ & $0.8567 \pm 0.0152$ & $+0.0133$ $(+1.58\%)$ & $0.2674$ \\
Val Seg Loss   & $1.3045 \pm 0.0867$ & $1.2424 \pm 0.0387$ & $-0.0622$ $(-4.76\%)$ & $0.0908$ \\
Val Box Loss   & $0.7239 \pm 0.0434$ & $0.7305 \pm 0.0399$ & $+0.0066$ $(+0.91\%)$ & $0.7008$ \\
Val Cls Loss   & $0.5591 \pm 0.0635$ & $0.6148 \pm 0.0884$ & $+0.0557$ $(+9.97\%)$ & $0.0943$ \\
Val L1 Loss    & $0.0164 \pm 0.0012$ & $0.0162 \pm 0.0009$ & $-0.0002$ $(-1.02\%)$ & $0.6995$ \\
\hline
Tỷ lệ seed thắng (Mask mAP@50-95) & \multicolumn{2}{c}{TSVM cao hơn ở $6/10$ seed} & --- & --- \\
Tỷ lệ seed thắng (Val Seg Loss)   & \multicolumn{2}{c}{TSVM thấp hơn ở $8/10$ seed} & --- & --- \\
Độ lệch chuẩn (Std)                & $0.0129$ & $0.0078$ & Giảm $39.7\%$ & --- \\
Biên độ (Range)                    & $0.0425$ & $0.0273$ & Giảm $35.7\%$ & --- \\
Đáy hiệu năng (Min)                & $0.6941$ (s3) & $0.7065$ (s7) & $+0.0124$ & --- \\
\hline
\end{tabular}
\end{table}
```

> **Ghi chú bắt buộc dưới bảng:**
> *"Với cỡ mẫu $N = 10$ lần chạy độc lập, không chỉ số nào đạt mức ý nghĩa thống kê ở ngưỡng $\alpha = 0.05$. Hai chỉ số Validation Segmentation Loss và Validation Classification Loss chỉ tiệm cận ngưỡng $\alpha = 0.10$ ($p = 0.0908$ và $p = 0.0943$) và có dấu trái chiều nhau. Khác biệt quan sát được rõ nhất giữa hai mô hình nằm ở mức độ ổn định phương sai, không phải ở giá trị hiệu năng trung bình."*

---

### 4. Bảng Số liệu Ma trận Nhầm lẫn (⚠️ kèm cảnh báo)

```latex
\begin{table}[htbp]
\centering
\caption{Ma trận nhầm lẫn trung bình qua 10 seed tại ngưỡng $conf=0.25$, $IoU=0.45$. Ô True Negative là giá trị tái dựng, không phải số đo trực tiếp của Ultralytics.}
\label{tab:confusion_matrix_10seed}
\small
\begin{tabular}{lcccc}
\hline
\textbf{Ô ma trận} & \textbf{Baseline} & \textbf{TSVM} & \textbf{$\Delta$} & \textbf{Trạng thái} \\
\hline
True Polyp $\rightarrow$ Pred Polyp (TP)        & $110.3 \pm 3.40$ & $111.2 \pm 2.20$ & $+0.9$ & Số đo \\
True Polyp $\rightarrow$ Pred Background (FN)     & $16.7 \pm 3.40$  & $15.8 \pm 2.20$  & $-0.9$ & Số đo \\
True Background $\rightarrow$ Pred Polyp (FP)    & $16.8 \pm 2.35$  & $14.6 \pm 4.35$  & $-2.2$ & Số đo \\
True Background $\rightarrow$ Pred Background (TN) & $23.2 \pm 2.35$ (tái dựng) & $25.4 \pm 4.35$ (tái dựng) & $+2.2$ & \textbf{Suy dựng} \\
\hline
Sensitivity (TP-rate)    & $86.85\%$ & $87.56\%$ & $+0.71\%$ & Số đo \\
FP-rate trên ảnh nền     & $42.00\%$ & $36.50\%$ & $-5.50\%$ & Số đo \\
\hline
\end{tabular}
\end{table}
```

> **Ghi chú bắt buộc dưới bảng:**
> *"Ô True Negative được tái dựng theo giả định $N_{TN} = 40 - N_{FP}$: mã nguồn Ultralytics (`ConfusionMatrix.process_batch`) không có nhánh cộng vào ô background--background, nên ô này luôn bằng 0 và hiển thị trống trên toàn bộ 20 ảnh ma trận nhầm lẫn gốc. Ngoài ra, 3 trong 20 lượt chạy (TSVM s0, s5, s8) không đối chiếu được với ảnh gốc do artifact thuộc một lượt validation bị lỗi. Vì vậy bảng này chỉ nên được trình bày như **quan sát mô tả** trên tập kiểm định hiện tại, không phải bằng chứng định lượng về hiệu quả của TSVM."*

---

### 5. Tài liệu tham chiếu chuẩn

> Toàn bộ số liệu chuẩn dùng cho khóa luận cử nhận: [`doc/20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md`](file:///c:/LeDucLuong/HK%20VII/LuanCuNhan/DeepLearning/Test_Mau/archive/doc/20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md)
