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
- **GFLOPs (cập nhật 28/10/2026):** đã đo bằng `FlopCounterMode` của PyTorch, xem mục bên dưới. Bộ đếm này không tính phép theo phần tử trong phép quét SS2D, nên GFLOPs của TSVM là **cận dưới**. Không chép GFLOPs từ tài liệu cũ.
- VRAM không đo được vì phiên đo chạy trên CPU. Không ghi là 0.
- Độ chính xác (20 seed, epoch cực đại mask) và độ trễ (một checkpoint seed 0) là hai đại lượng khác nguồn. Có thể đặt cạnh nhau để bàn về đánh đổi, nhưng không coi là một điểm Pareto đã kiểm định.

## Bổ sung 28/10/2026: FLOPs và độ trễ GPU

Script [`scripts/do_flops_gpu.py`](scripts/do_flops_gpu.py). Checkpoint `best.pt` seed 0 trong `03_ket_qua_huan_luyen/` (cùng checkpoint với phép đo CPU). Đã đo **hai lần** trong ngày 28/10/2026:

| | Lần 1 (chiều, ở trường) | Lần 2 (tối, **số dùng trong báo cáo**) |
|---|---|---|
| Thiết lập | 3 vòng × 300 lần đo, xen kẽ hai mô hình | 5 vòng × 200 lần đo, đảo thứ tự mỗi vòng; trước mỗi khối chờ GPU dưới 55 °C; ghi nhiệt độ và xung nhịp |
| Kết quả | [bang/16_lan1_flops_do_tre_gpu.csv](bang/16_lan1_flops_do_tre_gpu.csv), [16b_lan1](bang/16b_lan1_do_tre_gpu_tung_lan.csv), [log](bang/_log_flops_gpu_lan1.txt) | [bang/16_flops_do_tre_gpu.csv](bang/16_flops_do_tre_gpu.csv), [16b](bang/16b_do_tre_gpu_tung_lan.csv) (2.000 lần đo), [16c](bang/16c_do_tre_gpu_nhiet_do.csv) (nhiệt độ, xung nhịp từng khối), [log](bang/_log_flops_gpu.txt) |

Chung cho cả hai lần: NVIDIA GeForce RTX 5050 Laptop GPU, PyTorch 2.13.0+cu130, Ultralytics 8.4.127 (fork TSVM FP32); FP32, batch 1, đầu vào 1×3×640×640, đã gộp Conv-BN, chỉ forward (không tiền/hậu xử lý), 50 lần khởi động trước mỗi khối, đo bằng CUDA event. FLOPs: `torch.utils.flop_counter.FlopCounterMode` (conv, matmul, bmm, einsum) và `get_flops` của Ultralytics để đối chiếu.

| | Baseline | TSVM FP32 | Tỉ lệ |
|---|---:|---:|---:|
| GFLOPs (FlopCounterMode) | 34,29 | 34,82 | +1,5% |
| GFLOPs (Ultralytics `get_flops`) | 37,32 | 37,86 | +1,4% |
| **Lần 2:** độ trễ trung vị (5 vòng) | 26,33 ms | 39,86 ms | **1,51 lần** |
| Lần 2: trung bình ± SD | 26,99 ± 3,20 ms | 41,42 ± 6,82 ms | 1,53 lần |
| Lần 2: nhỏ nhất | 20,79 ms | 29,80 ms | 1,43 lần |
| Lần 2: phân vị 10% | 23,49 ms | 34,99 ms | 1,49 lần |
| Lần 2: tỉ lệ trung vị theo từng vòng | | | 1,44–1,63 |
| Lần 1: nhỏ nhất | 11,77 ms | 20,39 ms | 1,73 lần |
| Lần 1: trung vị vòng đầu | 13,68 ms | 23,76 ms | 1,74 lần |
| Lần 1: trung vị cả 3 vòng | 15,80 ms | 39,06 ms | 2,47 lần |

Diễn giải:
- **FLOPs gần như không đổi (+1,5%) nhưng độ trễ tăng khoảng 1,5–1,7 lần trên GPU và 2,1 lần trên CPU.** Phần tính toán thêm của SS2D nhỏ; chi phí chủ yếu đến từ phép quét gồm nhiều bước nối tiếp (9 vòng Hillis–Steele cho L = 400), nhiều tensor trung gian và phép theo phần tử, vốn bị giới hạn bởi băng thông bộ nhớ và số lần gọi kernel chứ không bởi số phép nhân. Đây là lý do GFLOPs không phản ánh đúng tốc độ của khối Mamba viết bằng PyTorch thuần.
- **Lần 2 được kiểm soát nhiệt:** GPU ở 41–51 °C, xung nhịp SM 2.842–2.850 MHz ở mọi khối đo, không phải chờ nguội lần nào. Tỉ lệ giữa hai mô hình ổn định qua 5 vòng (1,44–1,63). Vì vậy báo cáo dùng **lần 2**.
- **Độ trễ tuyệt đối không ổn định giữa hai phiên:** lần 2 chậm hơn lần 1 khoảng 1,5–2 lần ở cả hai mô hình dù GPU không nóng và chạy ở xung tối đa. Nguyên nhân chưa xác minh; giả thuyết là với batch 1, thời gian bị chi phối bởi phía CPU (gọi kernel, chế độ nguồn của máy) hơn là bởi GPU. Ở lần 1, độ trễ tăng dần qua các vòng (Baseline 13,7 → 16,6 → 29,5 ms) nên trước đây được giải thích là do GPU nóng; lần 2 cho thấy cách giải thích này chưa chắc chắn. **Chỉ nên báo cáo tỉ lệ giữa hai mô hình, không báo cáo số ms như một hằng số của máy.**
- Vẫn là một máy, một seed. Không suy ra tốc độ trên GPU máy chủ hay hệ thống nội soi thật.
- `get_flops` của Ultralytics cho số lớn hơn FlopCounterMode khoảng 3 GFLOPs ở cả hai mô hình (khác cách đếm); tỉ lệ giữa hai mô hình như nhau.

## Hình cũ (đã chuyển vào lưu trữ)

Bộ hình mới vẽ lại từ CSV nằm ở `06_bao_cao/hinh/`. Các hình cũ dưới đây chỉ giữ để tham khảo.


- [fig01_latency_mean.png](../99_luu_tru/hinh_cu/efficiency_benchmark_figures/fig01_latency_mean.png)
- [fig07_accuracy_latency_tradeoff.png](../99_luu_tru/hinh_cu/efficiency_benchmark_figures/fig07_accuracy_latency_tradeoff.png)
- [fig05_parameters_fp32_memory.png](../99_luu_tru/hinh_cu/efficiency_benchmark_figures/fig05_parameters_fp32_memory.png)
