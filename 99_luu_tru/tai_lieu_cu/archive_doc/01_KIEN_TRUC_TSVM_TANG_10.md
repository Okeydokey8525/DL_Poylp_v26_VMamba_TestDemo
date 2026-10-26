# Kiến trúc C2TSVMamba tại tầng 10 của YOLO26s seg

Đối chiếu source ngày 26/10/2026. Đây là mô tả triển khai trong `ultralytics_Topology-Shape-aware_VMamba_FP32/`, không phải khẳng định mọi chi tiết giống VMamba gốc hoặc lợi ích topology đã được đo.

## Vị trí và kích thước sau scale s

YAML: `cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml`. Tầng 10 sau SPPF thay C2PSA bằng C2TSVMamba; đầu Segment26 lấy các tầng 16,19,22.

| Vị trí | Stride | Map khi input 640×640 | Kênh thực |
|---|---:|---:|---:|
| Backbone P3, layer 4 | 8 | 80×80 | 256 |
| Backbone P4, layer 6 | 16 | 40×40 | 256 |
| Backbone P5, layer 10 | 32 | 20×20 | 512 |
| Head P3/P4/P5, layer 16/19/22 | 8/16/32 | 80×80 / 40×40 / 20×20 | 128 / 256 / 512 |

YAML ghi 1024 kênh và repeats 2 trước scaling. Biến thể s có width 0,5 và depth 0,5 nên wrapper nhận 512 kênh, phần lõi có 256 kênh với e=0,5, một TSVMamba nội bộ. Không lấy cấu hình tensor 1024 kênh tổng quát làm kích thước mô hình s thực nghiệm.

## Luồng forward thực tế

```text
x → cv1(1×1) → tách(a,b)
                    b → TSVMamba → b′
      concat(a,b′) → cv2(1×1) → output

TSVMamba(x):
  F_M = SS2D(x)
  S_shape = ShapeAwareBranch(x)
  S = DirectionalShapeExtractor(S_shape)
  G = sigmoid(Conv1×1(S))
  F_M_mod = F_M * (1 + G)
  F_fused = Conv1×1(concat(F_M_mod,S))
  F_out = Conv1×1_no_activation(Conv1×1_SiLU(F_fused))
  y = x + gamma * F_out
```

`gamma` là tham số học được, khởi tạo 0,001. Đây là lựa chọn khởi tạo residual, không tự chứng minh hội tụ hay gradient luôn ổn định.

## SS2D và phép scan

Đầu vào chiếu 1×1 thành u,z; u qua depthwise 3×3 và SiLU. Bốn chuỗi là raster thuận/ngược và chuỗi sau transpose thuận/ngược. Mỗi hướng sinh delta,B,C; delta dùng softplus, A=-exp(A_logs). Source clamp delta*A vào[-50,0] trước exp. Trạng thái dùng recurrence:

\[
h_t=a_t h_{t-1}+b_t,\qquad b_t=\Delta_t B_t u_t.
\]

Đầu ra y_k là tổng theo chiều state của C*h. Các hướng được đưa về lưới rồi cộng; sau đó nhânSiLU(z) và qua out_proj 1×1. Source hiện không có LayerNorm đầu ra SS2D hoặc nhánh skipD độc lập.

Với lõi 256 kênh: d_state=16, expand=1, dt_rank=ceil(256/16)=16. L=H*W=400 tại P5; scan đệm lên 512 và có 9 bước ghép với độ lệch 1,2,4,...,256. **Parallel depth O(log L)** nhưng mỗi bước xử lý tensor dọc chuỗi; **tổng công việc tensor O(L log L)** khi giữ batch/kênh/state cố định. Không gọi triển khai PyTorch này là kernel tuyến tính tối ưu chỉ từ tên Mamba.

## Nhánh hình dạng và guidance

ShapeAwareBranch dùng depthwise 3×3 và 5×5 song song rồi ghép qua Conv 1×1. DirectionalShapeExtractor có kernel 1×5,5×1,3×3 và tín hiệu sqrt(s_h²+s_v²+1e-6), ghép qua cácConv 1×1. s_h/s_v là đáp ứng bộ lọc học được có BN/activation, không phải đạo hàm Sobel tường minh; kernel 3×3 không tự đo độ cong hay Betti.

TopologyShapeGate là Conv 2 d(c,c,kernel 1) + Sigmoid, **không có channel-reduction ratio 4** trong source này. G∈[0,1] nên hệ số 1+G∈[1,2]: phép nhân trực tiếp khuếch đại F_M, không triệt nền bằng cách nhân hệ số nhỏ hơn 1. Hành vi nền cuối mạng cần đo ở đầu ra.

FFN gồm Conv(c,2 c,1,act=True) rồi Conv(2 c,c,1,act=False). Lớp Conv của fork dùng BN và mặc địnhSiLU; không phải Conv 3×3/GELU như sơ đồ cũ.

## Ablation và độ chính xác số

| Mode source | SS2D | Shape | Guidance |
|---|---|---|---|
| topology_shape_vmamba | có | có | có |
| vmamba_only | có | không | không |
| shape_only | không | có | không |
| shape_vmamba_no_guidance | có | có | không |

Đây là các mode có trong code, chưa phải bốn nhóm thực nghiệm 20 seed đã hoàn tất. Bộ chính chỉ đối chiếu Baseline/fullTSVM FP32. Chưa có độ đo topology hoặc ablation để quy chênh lệch AP cho từng nhánh.

Bản FP32 đổi đường lưu EMA/strip_optimizer sangfloat32 và từ chối snapshot không hữu hạn; kiến trúc không đổi. `amp=False` khi train chưa tự bảo đảm đường lưu không ép half. Suy luận TSVM dùngfloat32,half=False. Không khẳng định AMP/FP16 an toàn vì nhánh SS2D có thể có biên độ lớn trướcBN. Sự cố và bản vá được lưu trong tài liệu 27 như hồ sơ lịch sử, không dùng trạng thái cũ “chưa train lại” làm trạng thái hiện tại.

## Bằng chứng đã có

Kiểm toán ngày 25/10 đã đọc 40 best.pt và source, xác nhận layer 10 đúng kiểu lớp, P4 thực 256 kênh, TSVM lưu tensorfloat32 hữu hạn. Không đưa lại các số tham số synthetic 1024 kênh hoặc lời khẳng định backward hoàn hảo từ tài liệu cũ như kết quả mới.

Chi tiết: [báo cáo kiểm toán](../audit_20261025_193105/AUDIT_REPORT.md), [checkpoint inventory](../audit_20261025_193105/root/checkpoint_inventory.json), [trạng thái](CURRENT_PROJECT_STATUS.md). File triển khai là bằng chứng cuối cùng khi tài liệu mâu thuẫn.
