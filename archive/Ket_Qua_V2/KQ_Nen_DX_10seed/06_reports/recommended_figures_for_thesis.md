# DANH MỤC HÌNH VẼ KHUYẾN NGHỊ CHO LUẬN VĂN (RECOMMENDED FIGURES FOR THESIS)
## Các Biểu đồ Khoa học Trích xuất từ Thực nghiệm 10 Seed (Kvasir-SEG BG20)

Tài liệu này chọn lọc và hướng dẫn cách đưa các biểu đồ từ thư mục `archive/KQ_Nen_DX_10seed/` vào luận văn tốt nghiệp, kèm theo chú thích học thuật (Academic Caption) và mã nguồn LaTeX chuẩn.

---

### 1. Danh sách Hình Khuyến nghị Cốt lõi

| Mã Hình | Đường dẫn Tệp | Nội dung Khoa học | Vai trò trong Luận văn |
| :--- | :--- | :--- | :--- |
| **Hình 1** | `02_distributions/fig04_distribution_comparison.png` | Phân phối mAP50-95 và Validation Loss qua Boxplot & KDE | Chứng minh tính ổn định phương sai giữa Baseline và TSVM |
| **Hình 2** | `03_seed_by_seed/fig07_seed_comparison_bar.png` | So sánh trực diện từng seed (Seed 0 đến Seed 9) | Minh họa chi tiết tính biến động từng lần khởi tạo (6/10 seed TSVM > Baseline) |
| **Hình 3** | `03_seed_by_seed/fig09_head_to_head_scatter.png` | Đồ thị phân tán Head-to-Head qua đường chéo đồng nhất $y=x$ | Trực quan hóa độ chênh lệch từng seed và khoảng tin cậy |
| **Hình 4** | `04_confusion_matrix/fig14_confusion_matrix_comparison.png` | Ma trận nhầm lẫn chuẩn hóa (TP, FN, FP, TN) trên 167 ảnh | Đánh giá khả năng phân loại polyp vs background |
| **Hình 5** | `05_multimetric/fig17_multimetric_radar.png` | Biểu đồ Radar đa chỉ số (mAP, P, R, F1, Loss stability) | Cung cấp cái nhìn toàn diện về đặc tính cân bằng của mô hình |

---

### 2. Chi tiết Từng Hình & Mã LaTeX Chuẩn Mực

#### Hình 1: Phân phối Hiệu năng và Độ Ổn định (Distribution Comparison)
- **Tệp nguồn**: `archive/KQ_Nen_DX_10seed/02_distributions/fig04_distribution_comparison.png`
- **Mục đích**: Trực quan hóa giá trị trung bình (Mean), khoảng tứ phân vị (IQR), và độ rộng phân phối của mAP50-95 cũng như Validation Loss qua 10 seed.
- **Diễn giải học thuật**:
  > *Biểu đồ hộp (Boxplot) và ước lượng mật độ hàm nhân (KDE) cho thấy phân phối Mask mAP50-95 của cấu hình TSVM tập trung hơn (Std = 0.0078) so với Baseline (Std = 0.0129). Đồng thời, phân phối Validation Loss của TSVM dịch chuyển về phía giá trị nhỏ hơn và có độ phân tán hẹp hơn.*

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/fig04_distribution_comparison.png}
    \caption{So sánh phân phối xác suất thực nghiệm của Mask mAP50-95 và Validation Loss giữa YOLO26s-seg Baseline và TSVM qua 10 lần khởi tạo ngẫu nhiên độc lập (Seed 0 - 9). Đường nét đứt biểu diễn giá trị trung bình; các điểm biểu diễn kết quả từng seed cụ thể.}
    \label{fig:distribution_comparison_10seed}
\end{figure}
```

---

#### Hình 2: So sánh Cặp Từng Seed Cụ thể (Head-to-Head Scatter)
- **Tệp nguồn**: `archive/KQ_Nen_DX_10seed/03_seed_by_seed/fig09_head_to_head_scatter.png`
- **Mục đích**: Trực quan hóa mối tương quan và vị trí tương đối giữa kết quả của TSVM ($y$) so với Baseline ($x$) trên từng seed.
- **Diễn giải học thuật**:
  > *Các điểm dữ liệu nằm phía trên đường phân giác $y = x$ tương ứng với các seed mà TSVM đạt kết quả cao hơn Baseline (6/10 seed đối với Mask mAP50-95 và 8/10 seed đối với Box mAP50-95). Khoảng tin cậy 95% được hiển thị phản ánh độ phân tán của dữ liệu mẫu.*

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.85\linewidth]{figures/fig09_head_to_head_scatter.png}
    \caption{Biểu đồ tương quan Head-to-Head theo từng seed giữa YOLO26s-seg Baseline (trục hoành) và TSVM (trục tung). Đường nét đứt $y=x$ là mốc cân bằng; các điểm phía trên đường chéo chỉ ra các lần chạy TSVM đạt kết quả tốt hơn Baseline.}
    \label{fig:head_to_head_scatter}
\end{figure}
```

---

#### Hình 3: Đánh giá Phân loại trên Tập Test qua Ma trận Nhầm lẫn (Confusion Matrix)
- **Tệp nguồn**: `archive/KQ_Nen_DX_10seed/04_confusion_matrix/fig14_confusion_matrix_comparison.png`
- **Mục đích**: Phân tích khả năng phân loại nhị phân (Polyp vs Background) trung bình qua 10 seed tại ngưỡng đánh giá chuẩn.
- **Diễn giải học thuật**:
  > *Trên tập kiểm tra gồm 167 ảnh (127 ảnh chứa polyp và 40 ảnh nền thuần túy), TSVM đạt tỷ lệ phát hiện polyp thành công trung bình 113.8 / 127 ca ($89.61\%$), so với 112.4 / 127 ca ($88.50\%$) của Baseline. Trên tập ảnh nền, TSVM giảm số lượng kích hoạt giả xuống 11.8 ca so với 13.5 ca ở Baseline.*

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\linewidth]{figures/fig14_confusion_matrix_comparison.png}
    \caption{Ma trận nhầm lẫn trung bình qua 10 seed (kèm độ lệch chuẩn) trên tập test Kvasir-SEG BG20 gồm 167 ảnh. Phản ánh số ca True Positive, False Negative đối với lớp Polyp ($N=127$) và False Positive, True Negative đối với lớp Background ($N=40$).}
    \label{fig:confusion_matrix_10seed}
\end{figure}
```

---

#### Hình 4: So sánh Đa Chiều Đánh giá Mô hình (Multimetric Radar Chart)
- **Tệp nguồn**: `archive/KQ_Nen_DX_10seed/05_multimetric/fig17_multimetric_radar.png`
- **Mục đích**: Trình bày tổng thể các khía cạnh: Độ chính xác phát hiện (Box mAP), Độ chính xác phân vùng (Mask mAP, mAP50), Cân bằng Precision-Recall, và Chỉ số ổn định nghịch đảo (1 - Std).
- **Diễn giải học thuật**:
  > *Biểu đồ mạng nhện đa chỉ số cho thấy sự cân bằng giữa các mục tiêu: TSVM thể hiện sự vượt trội về độ ổn định (phương sai thấp hơn) và chỉ số Box mAP/Precision, trong khi mAP50 có giá trị tương đương với Baseline.*

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.85\linewidth]{figures/fig17_multimetric_radar.png}
    \caption{Biểu đồ Radar so sánh toàn diện các khía cạnh hiệu năng giữa YOLO26s-seg Baseline và TSVM trên 10 seed. Các trục đã được chuẩn hóa về thang đo $[0, 1]$ tương đối.}
    \label{fig:multimetric_radar}
\end{figure}
```

---

### 3. Bảng Số liệu Khuyến nghị Đưa vào Báo cáo

Bảng tóm tắt kết quả kiểm định thống kê và sai số mẫu khuyến nghị cho phần thực nghiệm luận văn:

```latex
\begin{table}[htbp]
\centering
\caption{Tổng hợp so sánh hiệu năng 10 seed giữa Baseline và TSVM trên tập dữ liệu Kvasir-SEG (BG20). Giá trị trình bày dưới dạng Trung bình $\pm$ Độ lệch chuẩn mẫu.}
\label{tab:10seed_benchmark_results}
\small
\begin{tabular}{lcccc}
\hline
\textbf{Chỉ số (Metric)} & \textbf{YOLO26s-seg} & \textbf{TSVM (Đề xuất)} & \textbf{Chênh lệch ($\Delta$)} & \textbf{$p$-value ($t$-test)} \\
\hline
Box mAP50-95 & $0.7816 \pm 0.0104$ & $0.7869 \pm 0.0076$ & $+0.0053$ & $0.0912$ \\
Mask mAP50-95 & $0.7210 \pm 0.0129$ & $0.7246 \pm 0.0078$ & $+0.0036$ & $0.3839$ \\
Mask mAP50 & $0.8879 \pm 0.0118$ & $0.8863 \pm 0.0110$ & $-0.0016$ & $0.7580$ \\
Mask Precision & $0.9023 \pm 0.0339$ & $0.9118 \pm 0.0246$ & $+0.0095$ & $0.4682$ \\
Mask Recall & $0.8584 \pm 0.0252$ & $0.8625 \pm 0.0173$ & $+0.0041$ & $0.6698$ \\
Validation Loss & $1.7649 \pm 0.0298$ & $1.7454 \pm 0.0177$ & $-0.0195$ & $0.0908$ \\
\hline
Tỷ lệ Seed thắng (mAP) & \multicolumn{2}{c}{TSVM đạt điểm cao hơn ở 6/10 seed (60\%)} & --- & --- \\
Biên độ mAP (Range) & $0.0410$ & $0.0242$ & Giảm $41.0\%$ & --- \\
\hline
\end{tabular}
\end{table}
```
