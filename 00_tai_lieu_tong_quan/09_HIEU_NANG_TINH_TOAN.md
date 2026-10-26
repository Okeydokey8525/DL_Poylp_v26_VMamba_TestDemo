# 09. Chi phí tính toán

## Nguồn và mức xác minh

- Số liệu độ trễ lấy từ benchmark có sẵn: [`KQ_Nen_DX_20seed_FP32/efficiency_benchmark/`](../04_phan_tich_20seed/efficiency_benchmark/reports/benchmark_report.md). Bảng tổng hợp ở `tables/efficiency_summary.csv`, 400 lượt đo thô ở `raw/`.
- Bộ tài liệu này **không đo lại** độ trễ. Bộ tài liệu đã kiểm tra lại:
  - Số tham số: dựng lại mô hình được 11.434.463 và 12.254.688, **trùng** với benchmark ([bang/08_kien_truc_dung_lai.csv](bang/08_kien_truc_dung_lai.csv)).
  - Kích thước và kiểu dữ liệu của `best.pt`: 22,27 MiB (float16) và 47,37 MiB (float32), **trùng** với benchmark ([bang/07_checkpoint_best_pt.csv](bang/07_checkpoint_best_pt.csv)).
  - Benchmark đo trên bản sao checkpoint đặt trong thư mục ai-service. SHA-256 ghi trong `raw/*_environment.json` **trùng** với `best.pt` seed 0 trong `03_ket_qua_huan_luyen/`: Baseline `61ebd028…`, TSVM FP32 `b0578c76…`. Vậy benchmark dùng đúng checkpoint của bộ chính.

## Điều kiện đo

| | |
|---|---|
| Phần cứng | CPU AMD Ryzen 7 250 (8 lõi/16 luồng), RAM 15,3 GiB, **không có GPU** |
| Phần mềm | Windows, Python 3.12.14, PyTorch 2.6.0+cpu, Ultralytics 8.4.103 (môi trường của ai-service PolypVision) |
| Checkpoint | `best.pt` của **seed 0** cho mỗi mô hình (TSVM dùng bản FP32) |
| Thiết lập | float32, batch 1, đầu vào 1×3×640×640, 4 luồng intra-op, 20 lần khởi động rồi 100 lần đo, mỗi mô hình chạy trong một tiến trình riêng |
| Hai chế độ đo | `forward_only`: chỉ `model.forward`, sau khi gộp Conv-BN. `predict_pipeline`: 20 ảnh validation, gồm letterbox, forward và hậu xử lý mặt nạ |

## Kết quả

| Mô hình | Chế độ | Mean ± SD (ms) | P50 | P95 | Ảnh/s (chạy nối tiếp) |
|---|---|---:|---:|---:|---:|
| Baseline | forward_only | 269,56 ± 18,71 | 270,97 | 297,76 | 3,71 |
| Baseline | predict_pipeline | 286,56 ± 20,09 | 286,82 | 319,22 | 3,49 |
| TSVM FP32 | forward_only | 577,36 ± 24,40 | 576,84 | 623,50 | 1,73 |
| TSVM FP32 | predict_pipeline | 567,86 ± 24,45 | 566,94 | 611,67 | 1,76 |

| | Baseline | TSVM FP32 | Tỉ lệ |
|---|---:|---:|---:|
| Tham số (chưa gộp Conv-BN) | 11.434.463 | 12.254.688 | +7,17% |
| Tham số sau khi gộp Conv-BN | 10.365.727 | 11.184.672 | +7,90% |
| Độ trễ forward (CPU) | 269,56 ms | 577,36 ms | **khoảng 2,14 lần** |
| Độ trễ pipeline (CPU) | 286,56 ms | 567,86 ms | **khoảng 1,98 lần** |
| File `best.pt` | 22,27 MiB | 47,37 MiB | (float16 so với float32) |

## Diễn giải

- Tham số chỉ tăng 7%, nhưng độ trễ trên CPU tăng **khoảng gấp đôi**. Nguyên nhân là SS2D quét 4 hướng trên chuỗi L = 400 vị trí, với tensor trung gian kích thước (B, 256, 16, 400) cho mỗi hướng. Phần quét song song cài bằng `torch.cat` trong vòng lặp Python (log₂ 512 = 9 bước), không dùng kernel CUDA/selective-scan tối ưu như Mamba gốc.
- Đây là đo trên **một máy CPU, một seed, một thứ tự chạy**. 100 lần đo không phải 100 mẫu độc lập. **Không suy ra** tốc độ trên GPU hay hệ thống nội soi thời gian thực.
- **Không báo GFLOPs.** THOP không đếm đúng phép quét song song tự viết, nên con số GFLOPs sẽ thiếu. Không chép GFLOPs từ tài liệu cũ.
- VRAM không đo được vì phiên đo chạy trên CPU. Không ghi là 0.
- Độ chính xác (20 seed, epoch cực đại mask) và độ trễ (một checkpoint seed 0) là hai đại lượng khác nguồn. Có thể đặt cạnh nhau để bàn về đánh đổi, nhưng không coi là một điểm Pareto đã kiểm định.

## Hình cũ (đã chuyển vào lưu trữ)

Bộ hình mới vẽ lại từ CSV nằm ở `06_bao_cao/hinh/`. Các hình cũ dưới đây chỉ giữ để tham khảo.


- [fig01_latency_mean.png](../99_luu_tru/hinh_cu/efficiency_benchmark_figures/fig01_latency_mean.png)
- [fig07_accuracy_latency_tradeoff.png](../99_luu_tru/hinh_cu/efficiency_benchmark_figures/fig07_accuracy_latency_tradeoff.png)
- [fig05_parameters_fp32_memory.png](../99_luu_tru/hinh_cu/efficiency_benchmark_figures/fig05_parameters_fp32_memory.png)
