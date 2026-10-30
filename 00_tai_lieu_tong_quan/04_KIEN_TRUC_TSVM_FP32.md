# 04. Kiến trúc đề xuất: YOLO26s-seg + C2TSVMamba (TSVM FP32)

## Nguồn

- Cấu hình: [`yolo26-seg-TopologyShapeVMamba.yaml`](../02_ma_nguon/ultralytics_TSVM_FP32/cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml). File này giống hệt `yolo26-seg.yaml` ngoại trừ dòng tầng 10.
- Mã module: [`nn/modules/topology_shape_vmamba.py`](../02_ma_nguon/ultralytics_TSVM_FP32/nn/modules/topology_shape_vmamba.py), 502 dòng.
- Đăng ký module: `nn/tasks.py` (hàm `parse_model`, `C2TSVMamba` nằm trong nhóm module có tham số repeat) và `nn/modules/__init__.py`.
- Số tham số dưới đây đo khi dựng lại mô hình. Nguồn: [bang/08_kien_truc_dung_lai.csv](bang/08_kien_truc_dung_lai.csv).

## Điểm thay đổi

```
Baseline : ... SPPF(9) ── C2PSA(10)      ── neck/head (giống nhau)
Đề xuất  : ... SPPF(9) ── C2TSVMamba(10) ── neck/head (giống nhau)
                          vào/ra 512×20×20
```

Đầu ra tầng 10 đi tới hai nơi: tầng 11 (upsample lên nhánh P4) và tầng 21 (ghép vào đầu ra P5). Vì vậy đặc trưng do TSVM tạo ra ảnh hưởng tới cả ba mức P3/P4/P5 của đầu Segment26.

## Cấu trúc C2TSVMamba (scale s)

```
x (512×20×20)
 └─ cv1: Conv1×1 512→512 ─ split ─┬─ a (256) ───────────────────────────┐
                                  └─ b (256) ─ TSVMamba (1 khối) ─ b' ──┤
                                                                         concat (512)
                                                                         └─ cv2: Conv1×1 512→512 ─ y (512×20×20)
```

`c = int(512 × 0,5) = 256`. Số khối `n = 2 × depth 0,5 = 1`.

## Bên trong khối TSVMamba (mode `topology_shape_vmamba`)

```
b ──┬─ SS2D (VMamba) ─────────────────────────── F_M
    └─ ShapeAwareBranch ─ DirectionalShapeExtractor ─ S
                                                       └─ TopologyShapeGate ─ G = sigmoid(Conv1×1(S)) ∈ [0,1]
F_M' = F_M ⊙ (1 + G)
F    = Conv1×1( concat[F_M', S] )        (fuse, 512→256)
F    = FFN(F)                             (Conv1×1 256→512 → Conv1×1 512→256, không kích hoạt ở cuối)
out  = b + γ · F                          (γ học được, khởi tạo 0,001)
```

| Thành phần | Cài đặt trong mã | Tham số |
|---|---|---:|
| **SS2D** (`vmamba`) | `in_proj` 1×1 tách thành (u, z). Depthwise conv 3×3 rồi SiLU. Quét chọn lọc theo **4 hướng**: hàng xuôi, hàng ngược, cột xuôi, cột ngược. Mỗi hướng có `x_proj` và `dt_proj` riêng, `A = −exp(A_log)`. Đệ quy được giải bằng **quét kết hợp song song** (`parallel_associative_scan`, O(log L) bước). Cộng 4 hướng, nhân cổng SiLU(z), rồi qua `out_proj`. d_inner = 256, d_state = 16, dt_rank = 16, L = 20×20 = 400 | 281.856 |
| **ShapeAwareBranch** | Depthwise conv 3×3 và 5×5 chạy song song, ghép lại, rồi Conv 1×1 | 141.312 |
| **DirectionalShapeExtractor** | Depthwise conv dải 1×5 (ngang), 5×1 (dọc) và 3×3. Độ lớn gradient `sqrt(s_h² + s_v² + 1e-6)`. Ghép 4 nhánh, Conv 1×1 (`topo_fuse`), rồi ghép với đặc trưng hình dạng và Conv 1×1 (`unify`) | 400.640 |
| **TopologyShapeGate** | Conv 1×1 có bias, rồi Sigmoid | 65.792 |
| **fuse** | Conv 1×1 512→256 | 131.584 |
| **FFN** | Conv 1×1 256→512 có kích hoạt, rồi Conv 1×1 512→256 không kích hoạt | 263.680 |
| γ | Một tham số vô hướng, khởi tạo 0,001 | 1 |
| cv1 + cv2 của khối C2 | Hai Conv 1×1 512→512 | 526.336 |
| **Tổng tầng 10** | | **1.811.201** |

## So sánh quy mô với Baseline

| | Baseline (C2PSA) | TSVM FP32 | Chênh lệch |
|---|---:|---:|---:|
| Tham số tầng 10 | 990.976 | 1.811.201 | +820.225 |
| Tham số toàn mô hình | 11.434.463 | 12.254.688 | **+820.225 (+7,17%)** |
| `best.pt` | khoảng 22,27 MiB (float16) | khoảng 47,37 MiB (**float32**) | |

Toàn bộ mức tăng tham số nằm ở tầng 10. Các tầng khác giống hệt Baseline.

## Cách đọc tên "Topology-Shape-aware"

- Mã nguồn chỉ có các phép tích chập theo hướng và độ lớn gradient trên đặc trưng. **Không có** loss hay ràng buộc topology nào (Betti, clDice, persistent homology…). Loss huấn luyện vẫn là loss chuẩn của YOLO26-seg.
- Vì vậy "topology/shape" là **định hướng thiết kế** của module. Chưa có thực nghiệm nào chứng minh mô hình bảo toàn topology của mặt nạ ([11](11_GIOI_HAN_VA_HUONG_PHAT_TRIEN.md)).
- Module hỗ trợ 4 chế độ ablation: `topology_shape_vmamba`, `vmamba_only`, `shape_only`, `shape_vmamba_no_guidance`. Cả 40 lượt của bộ chính đều dùng chế độ đầy đủ `topology_shape_vmamba`. Ablation 3 chế độ còn lại chạy trên seed 0–4 (`03_ket_qua_huan_luyen/{Vmamba_only, Shape_only, No_guidance}/`). Kết quả ở `bang/17_*.csv` và Chương 6 mục 6.6: cả ba biến thể thấp hơn bản đầy đủ, không có ý nghĩa thống kê với 5 seed.

## Khởi tạo trọng số

Notebook dựng mô hình bằng `YOLO(yaml).load("yolo26s-seg.pt")`. Ultralytics chỉ nạp những tensor **trùng tên và trùng kích thước** với checkpoint. Script đối chiếu cấu trúc YOLO26s-seg (là kiến trúc của `yolo26s-seg.pt`) với TSVM và thấy:

- Tầng 0–9 và neck (11–22) trùng hoàn toàn, nên nhận trọng số tiền huấn luyện như Baseline.
- Tầng 10 có **12/58 tensor tham số, tức 790.016/1.811.201 tham số**, trùng tên và kích thước với `C2PSA`. Đó là `cv1`, `cv2` và `m.0.ffn`, vì `PSABlock` cũng có `ffn` cùng hình dạng. Các phần này **nhận trọng số của C2PSA**.
- Phần mới hoàn toàn được **khởi tạo ngẫu nhiên**, gồm 1.021.185 tham số: SS2D, ShapeAwareBranch, DirectionalShapeExtractor, gate, fuse và γ.
- γ = 0,001 làm nhánh TSVMamba gần như không tác động lúc bắt đầu huấn luyện. Ban đầu tầng 10 hoạt động gần như `cv2(concat(a, b))` với `cv1` và `cv2` lấy từ C2PSA.

Nguồn: [bang/08_kien_truc_dung_lai.csv](bang/08_kien_truc_dung_lai.csv), các dòng `l10_*`. Kiểm tra này dựa trên cấu trúc, không mở file `yolo26s-seg.pt` (file không có trong repo). Có một tác dụng phụ cần lưu ý: `m.0.ffn` của TSVMamba nhận trọng số của FFN trong PSA, dù nó đứng sau một đầu vào khác (`fuse`).
