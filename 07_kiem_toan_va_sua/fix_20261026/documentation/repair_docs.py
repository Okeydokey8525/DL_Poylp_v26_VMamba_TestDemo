"""Apply the documented source-of-truth fixes; never edit raw experiment artifacts."""
from pathlib import Path
import hashlib,json,shutil

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'fix_20261026/documentation'
BACKUP=OUT/'backups'
changes=[]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def backup(p):
    p=p.resolve()
    if p.exists():
        relative=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('parent_project')/p.name
        target=BACKUP/relative;target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():shutil.copy2(p,target)
        return sha(target)
    return None

def write(relative,text):
    p=ROOT/relative;before=backup(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text,encoding='utf-8')
    changes.append({'path':str(p.resolve()),'before_sha256':before,'after_sha256':sha(p)})

snap=ROOT/'doc/historical/snapshots_20261026';snap.mkdir(parents=True,exist_ok=True)
for name in ['README.md','CURRENT_PROJECT_STATUS.md','01_KIEN_TRUC_TSVM_TANG_10.md']:
    p=ROOT/'doc'/name;target=snap/name
    if not target.exists():shutil.copy2(p,target)
write('doc/historical/snapshots_20261026/README_SNAPSHOT.md', '''# Các bản tài liệu trước chỉnh sửa ngày 26 tháng 10 năm 2026

Các tệp trong thư mục này là bản sao nguyên trạng để truy vết. Nội dung có thể mô tả 10 seed, chẩn đoán cũ hoặc trạng thái đã bị thay thế; không dùng làm nguồn hiện trạng. Nguồn hiện tại nằm ở [README](../../README.md) và [CURRENT_PROJECT_STATUS](../../CURRENT_PROJECT_STATUS.md).
''')

write('doc/README.md', '''# Tài liệu hiện trạng YOLO26s seg và TSVM FP32

Cập nhật tài liệu ngày **26/10/2026** sau kiểm toán độc lập. Phạm vi nghiên cứu hiện dùng **hai mô hình, 20 seed mỗi mô hình (0–19), tổng 40 lượt huấn luyện**, trên BG20. Tài liệu này mô tả workspace local, không khẳng định đã đồng bộ lên GitHub.

## Đọc theo thứ tự

1. [Trạng thái và nguồn hiện tại](CURRENT_PROJECT_STATUS.md).
2. [Kiến trúc TSVM thực sự được cài đặt](01_KIEN_TRUC_TSVM_TANG_10.md).
3. [Hướng dẫn tái lập BG20 và các giới hạn](28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md).
4. [Báo cáo kiểm toán ngày 25/10](../audit_20261025_193105/AUDIT_REPORT.md), gồm báo cáo của năm phòng và các giới hạn kiểm tra.
5. [Báo cáo kết quả chuẩn 20 seed](../Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/06_reports/summary.md) và [quản lý hiện vật legacy](../Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/LEGACY_ARTIFACTS.md).

## Nguồn ưu tiên

| Nội dung | Nguồn cần đối chiếu |
|---|---|
| Lịch sử từng lượt | `Ket_Qua_V2/KetQua_Nen/YOLOv26s-seg/` và `Kvasir_BG20_YOLO26s_seg_TSVM_FP32/`, chỉ seed 0–19 |
| Bảng chính | `KQ_Nen_DX_20seed_FP32/01_raw_analysis/`, `02_statistics/`, `03_metrics/` |
| Ma trận đối tượng | `KQ_Nen_DX_20seed_FP32/04_confusion_matrix/`; TN ảnh là N/A |
| Kiến trúc và lưu checkpoint | `ultralytics_Topology-Shape-aware_VMamba_FP32/` |
| Dữ liệu đang dùng | `Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/` |
| Bản Word chính | `Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx` |
| Chỉnh sửa sau kiểm toán | `fix_20261026/`, tách khỏi bằng chứng kiểm toán trước sửa |

## Kết luận số liệu cần giữ nguyên

Mask mAP50–95 tại epoch cực đại mask của từng lượt: Baseline **0,718868 ± 0,011768**; TSVM FP32 **0,723171 ± 0,007197**. Chênh lệch **+0,004303**, paired t-test **p = 0,061431**, CI95% **[−0,000228; 0,008834]**. Chưa đạt ý nghĩa thống kê ở α = 0,05. SD mẫu thấp hơn khoảng 38,85% là quan sát trong tập seed đã khảo sát.

Có **16/40 lượt** khác epoch giữa cực đại mask AP và fitness box+mask chọn `best.pt`. Không gọi bảng max-mask là kết quả đánh giá lại checkpoint. Kiểm toán đã tái đánh giá 40 `best.pt` theo giao thức riêng, gắn hash, và không thấy sai lệch mask AP vượt 0,005 so với dòng fitness; một số P/R của Baseline không tái tạo chính xác. Chi tiết nằm trong báo cáo kiểm toán, không thay endpoint chính.

## Giới hạn bắt buộc

- Không suy TN ảnh bằng `40 − FP` đối tượng; không dùng trường legacy để tính specificity.
- Không suy Dice, IoU pixel, topology hoặc hiệu quả lâm sàng từ AP/P/R đối tượng.
- Chưa có test ngoài hay ablation 20 seed đầy đủ; cùng validation được dùng chọn epoch.
- Nguồn phát hành hai danh sách split 880/120 chưa được chứng thực đủ để gán cho tác giả dataset.
- Tái tạo nhãn trên OpenCV 4.12.0 và NumPy 2.2.6 cho 999/1.000 tệp trùng từng ký tự; một đỉnh của một nhãn khác khoảng 3 pixel. Không tự sửa nhãn hiện hành.
- Chưa có báo cáo Turnitin và cấu hình trường; không kết luận đạt ngưỡng 30%. Mobile chưa được chạy trong kiểm toán.

## Tài liệu lịch sử

Bộ 10 seed, bộ 21 seed TSVM cũ và các bản thảo trong `Bao_cao/md viet bao cao/` được giữ để truy vết, không dùng mặc định để sinh lại Word hiện tại. Header lịch sử không biến nội dung sai cũ thành kết quả đã được xác nhận. [Snapshot các điểm vào trước sửa](historical/snapshots_20261026/README_SNAPSHOT.md) giữ nguyên văn các phiên bản cũ.

Các quy tắc làm việc và trình bày vẫn dùng khi phù hợp: [AI_WORK_OPTIMIZATION_RULE](AI_WORK_OPTIMIZATION_RULE.md), [nguyên tắc làm việc](nguyen-tac-lam-viec-dai.md), các hướng dẫn phong cách Word. Không dùng chúng để thay thế raw/config/code.
''')

write('doc/CURRENT_PROJECT_STATUS.md', '''# Trạng thái hiện tại đã đối chiếu của dự án

Cập nhật ngày **26/10/2026**. Đây là trạng thái **workspace local** sau kiểm toán ngày 25/10 và trong đợt chỉnh sửa tài liệu ngày 26/10. Không khẳng định trạng thái GitHub khi chưa đối chiếu remote. Snapshot cũ giữ tại [historical/snapshots_20261026](historical/snapshots_20261026/README_SNAPSHOT.md).

## Phạm vi thực nghiệm chính

- Baseline: YOLO26s-seg; nguồn `Ket_Qua_V2/KetQua_Nen/YOLOv26s-seg/`, chọn seed 0–19.
- Đề xuất: YOLO26s-seg với C2TSVMamba tại layer 10; nguồn `Ket_Qua_V2/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM_FP32/`, seed 0–19.
- **40 lượt × 100 epoch**, cùng cấu hình chính: imgsz640, batch8, AdamW, lr0=0,001, warmup5, close_mosaic10, amp=False, deterministic=True.
- Các thư mục Baseline ngoài 0–19 và TSVM không có hậu tố FP32 là lịch sử; không trộn vào bảng chính.

## Dữ liệu

`Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/` có 1.200 ảnh: train1.040 (880 polyp + 160 nền), validation160 (120 ảnh polyp + 40 nền); validation chứa127 đối tượng polyp. Ảnh nền có nhãn rỗng. BG20 là 200 ảnh bổ sung so với1.000 ảnh polyp, không phải20% của tổng1.200 ảnh.

Đã kiểm số lượng, định dạng nhãn và không trùng byte ảnh train/val. Điều này không chứng minh tách bệnh nhân hoặc không có ảnh gần trùng. Danh sách880/120 được dùng cố định; provenance phát hành bởi tác giả dataset chưa đủ bằng chứng. Tái tạo1.000mask giữ đúng1.063 đối tượng; 999nhãn khớp từng ký tự ở OpenCV4.12.0/NumPy2.2.6, một nhãn khác một đỉnh nhỏ; nguyên nhân chưa xác định. [Tái lập BG20](28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md).

## Số liệu chính

| Chỉ số tại epoch cực đại mask AP | Baseline | TSVM FP32 |
|---|---:|---:|
| Mask mAP50–95, mean ± sample SD | 0,718868 ± 0,011768 | 0,723171 ± 0,007197 |
| Mask mAP50 | 0,906889 | 0,908274 |
| Mask Precision | 0,904095 | 0,914452 |
| Mask Recall | 0,859367 | 0,858979 |
| Val segmentation loss | 1,266294 | 1,232862 |

Δ mask mAP50–95 = +0,004303; paired t p=0,061431, Wilcoxon p≈0,069580; CI95% chứa0. Không kết luận ưu thế trung bình ở α0,05 hoặc tương đương. TSVM cao hơn13/20 cặp; SD thấp hơn khoảng38,85% là quan sát có giới hạn.

Nguồn chuẩn: [06_reports/summary.md](../Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/06_reports/summary.md), các CSV trong `01_raw_analysis`, `02_statistics`, `03_metrics`. `val/sem_loss` ghi0 ở mọi lượt không được diễn giải thành lỗi thực bằng0. YOLO26 dùng `val/l1_loss`, không đổi tên thành DFL.

## Epoch và checkpoint

Bảng chính lấy các metric cùng dòng đầu tiên đạt cực đại mask mAP50–95. `best.pt` được chọn theo tổng box+mask fitness; có16/40 lượt khác epoch. Kiểm toán đã đọc40best.pt, xác nhận TSVM float32 hữu hạn và Baseline lưu float16; cả hai được chuyển float32 khi suy luận. Seed, tên run và embedded history khớp raw đang lưu.

Đã tái đánh giá40best.pt với validation sao chép riêng, CPU float32, research fork8.4.127, rect=True,batch16,imgsz640,half=False,workers0. Không có sai lệch mask AP vượt0,005 so với CSV fitness. Một số P/R Baseline khác; không ghi PASS AP như mọi metric khớp chính xác. Phân tích này là kiểm chứng phụ, không thay endpoint max-mask hoặc test độc lập.

44.000 ô non-time TSVM cũ/FP32 trùng, còn2.000 ô time khác. Đây là lineage cần giữ log; có thể phù hợp rerun tất định khi chỉ sửa đường lưu, không tự chứng minh hay phủ định huấn luyện lại.

## Ma trận nhầm lẫn và topology

Số TP/FP/FN là đối tượng; TP+FN=127. Không suy số ảnh nền đúng bằng40−FP. Dùng bảng mới trong `04_confusion_matrix`; TN ảnh N/A. Các trường legacy `TN_reconstructed` bị đánh dấu không hợp lệ để suy specificity. Val seg loss thấp hơn ở14/20 cặp khi dùng lower-is-better; root summary cũ đếm chiều tăng cho ra6, không dùng cột đó như số lượt thắng.

Không có Dice pixel, HD95, Betti/clDice hoặc bằng chứng trực tiếp bảo toàn topology trong bộ chính. Bốn ablation mode có trong source nhưng chưa có bộ20seed đối chứng đầy đủ.

## Kiến trúc và phần mềm

Fork dùng cho TSVM FP32: `ultralytics_Topology-Shape-aware_VMamba_FP32/`. C2TSVMamba thay C2PSA tại layer10/P5; gate nhân1+G, FFN haiConv1×1, residualγ khởi tạo0,001. Tham khảo [kiến trúc đã sửa](01_KIEN_TRUC_TSVM_TANG_10.md).

PolypVision có Web Java/Spring Boot và FastAPI; Mobile Direct AI là nhánh riêng. Kiểm toán đã chạy Web/inference thật và phát hiện lỗi lịch sử so sánh cùng một số lỗi hiển thị. Đợt sửa mã ngày26/10 được ghi riêng tại `fix_20261026/`; chỉ kết luận đã sửa và kiểm thử sau khi có log của đợt sửa, không dùng test mock cũ làm chứng nhận chạy toàn trình. Mobile chưa chạy trong đợt kiểm toán.

## Nguồn bằng chứng và giới hạn

[Báo cáo kiểm toán](../audit_20261025_193105/AUDIT_REPORT.md) lưu hash của bản Word và tệp nguồn **trước sửa**. Các thống kê gốc, checkpoint và nhãn không được sửa để khớp câu chữ. Các thay đổi tài liệu/mã sau kiểm toán có log trong `fix_20261026/`.

Chưa có báo cáo Turnitin/settings trường; chưa đánh giá ngưỡng30%. Chưa kiểm chứng GPU lịch sử, external test, patient-level split, đầy đủ topology/ablation, mobile hoặc tải production. Khi thiếu bằng chứng, ghi chưa xác minh.
''')

write('doc/01_KIEN_TRUC_TSVM_TANG_10.md', r'''# Kiến trúc C2TSVMamba tại tầng 10 của YOLO26s seg

Đối chiếu source ngày26/10/2026. Đây là mô tả triển khai trong `ultralytics_Topology-Shape-aware_VMamba_FP32/`, không phải khẳng định mọi chi tiết giống VMamba gốc hoặc lợi ích topology đã được đo.

## Vị trí và kích thước sau scale s

YAML: `cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml`. Tầng10 sau SPPF thay C2PSA bằng C2TSVMamba; đầu Segment26 lấy các tầng16,19,22.

| Vị trí | Stride | Map khi input640×640 | Kênh thực |
|---|---:|---:|---:|
| Backbone P3, layer4 | 8 | 80×80 | 256 |
| Backbone P4, layer6 | 16 | 40×40 | 256 |
| Backbone P5, layer10 | 32 | 20×20 | 512 |
| Head P3/P4/P5, layer16/19/22 | 8/16/32 | 80×80 / 40×40 / 20×20 | 128 / 256 / 512 |

YAML ghi1024kênh và repeats2 trước scaling. Biến thể s có width0,5 và depth0,5 nên wrapper nhận512kênh, phần lõi có256kênh với e=0,5, một TSVMamba nội bộ. Không lấy cấu hình tensor1024kênh tổng quát làm kích thước mô hình s thực nghiệm.

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

`gamma` là tham số học được, khởi tạo0,001. Đây là lựa chọn khởi tạo residual, không tự chứng minh hội tụ hay gradient luôn ổn định.

## SS2D và phép scan

Đầu vào chiếu1×1 thành u,z; u qua depthwise3×3 và SiLU. Bốn chuỗi là raster thuận/ngược và chuỗi sau transpose thuận/ngược. Mỗi hướng sinh delta,B,C; delta dùng softplus, A=-exp(A_logs). Source clamp delta*A vào[-50,0] trước exp. Trạng thái dùng recurrence:

\[
h_t=a_t h_{t-1}+b_t,\qquad b_t=\Delta_t B_t u_t.
\]

Đầu ra y_k là tổng theo chiều state của C*h. Các hướng được đưa về lưới rồi cộng; sau đó nhânSiLU(z) và qua out_proj1×1. Source hiện không có LayerNorm đầu ra SS2D hoặc nhánh skipD độc lập.

Với lõi256kênh: d_state=16, expand=1, dt_rank=ceil(256/16)=16. L=H*W=400 tại P5; scan đệm lên512 và có9 bước ghép với độ lệch1,2,4,...,256. **Parallel depth O(log L)** nhưng mỗi bước xử lý tensor dọc chuỗi; **tổng công việc tensor O(L log L)** khi giữ batch/kênh/state cố định. Không gọi triển khai PyTorch này là kernel tuyến tính tối ưu chỉ từ tên Mamba.

## Nhánh hình dạng và guidance

ShapeAwareBranch dùng depthwise3×3 và5×5 song song rồi ghép qua Conv1×1. DirectionalShapeExtractor có kernel1×5,5×1,3×3 và tín hiệu sqrt(s_h²+s_v²+1e-6), ghép qua cácConv1×1. s_h/s_v là đáp ứng bộ lọc học được có BN/activation, không phải đạo hàm Sobel tường minh; kernel3×3 không tự đo độ cong hay Betti.

TopologyShapeGate là Conv2d(c,c,kernel1) + Sigmoid, **không có channel-reduction ratio4** trong source này. G∈[0,1] nên hệ số1+G∈[1,2]: phép nhân trực tiếp khuếch đại F_M, không triệt nền bằng cách nhân hệ số nhỏ hơn1. Hành vi nền cuối mạng cần đo ở đầu ra.

FFN gồm Conv(c,2c,1,act=True) rồi Conv(2c,c,1,act=False). Lớp Conv của fork dùng BN và mặc địnhSiLU; không phải Conv3×3/GELU như sơ đồ cũ.

## Ablation và độ chính xác số

| Mode source | SS2D | Shape | Guidance |
|---|---|---|---|
| topology_shape_vmamba | có | có | có |
| vmamba_only | có | không | không |
| shape_only | không | có | không |
| shape_vmamba_no_guidance | có | có | không |

Đây là các mode có trong code, chưa phải bốn nhóm thực nghiệm20seed đã hoàn tất. Bộ chính chỉ đối chiếu Baseline/fullTSVM FP32. Chưa có độ đo topology hoặc ablation để quy chênh lệch AP cho từng nhánh.

Bản FP32 đổi đường lưu EMA/strip_optimizer sangfloat32 và từ chối snapshot không hữu hạn; kiến trúc không đổi. `amp=False` khi train chưa tự bảo đảm đường lưu không ép half. Suy luận TSVM dùngfloat32,half=False. Không khẳng định AMP/FP16 an toàn vì nhánh SS2D có thể có biên độ lớn trướcBN. Sự cố và bản vá được lưu trong tài liệu27 như hồ sơ lịch sử, không dùng trạng thái cũ “chưa train lại” làm trạng thái hiện tại.

## Bằng chứng đã có

Kiểm toán ngày25/10 đã đọc40best.pt và source, xác nhận layer10 đúng kiểu lớp, P4 thực256kênh, TSVM lưu tensorfloat32 hữu hạn. Không đưa lại các số tham số synthetic1024kênh hoặc lời khẳng định backward hoàn hảo từ tài liệu cũ như kết quả mới.

Chi tiết: [báo cáo kiểm toán](../audit_20261025_193105/AUDIT_REPORT.md), [checkpoint inventory](../audit_20261025_193105/root/checkpoint_inventory.json), [trạng thái](CURRENT_PROJECT_STATUS.md). File triển khai là bằng chứng cuối cùng khi tài liệu mâu thuẫn.
''')

write('doc/28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md', '''# Tái lập dữ liệu BG20 trong workspace hiện tại

Cập nhật26/10/2026. Hướng dẫn này phân biệt **bộ dữ liệu đang dùng** với **bản tái tạo mới**. Không chạy chương trình chuyển đổi để ghi đè ảnh/nhãn hoặc kết quả huấn luyện đã công bố.

## Đường dẫn và môi trường

Từ thư mục `archive`:

- Dữ liệu hiện hành: `Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/`.
- Ảnh/mask gốc: `Ket_Qua_V2/Data Prosessing/Kvasir-SEG/{images,masks}/`.
- Ảnh âm: `Ket_Qua_V2/Data Prosessing/normal-cecum/`.
- Split cố định: `train.txt` và `val.txt` tại gốc archive. Chưa đủ provenance để khẳng định nhóm tác giả dataset phát hành hai danh sách này.
- Builder đúng cho BG20: `Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py`. `Stracth/Du_Lieu/convert_kvasir_to_yolo_seg.py` chỉ chuyển phần polyp, không tự bổ sung200ảnh nền.
- Cấu hình dùng ngay: `data_bg20.yaml`; trường path là đường dẫn tuyệt đối tới dữ liệu hiện hành. Khi chuyển máy, tạo cấu hình local tương ứng, không giả định path tương đối của Ultralytics luôn tính từ YAML.

Kiểm toán đã dùng Python3.12.14, OpenCV4.12.0, NumPy2.2.6 cho replay nhãn. Builder cầnPython3.12,OpenCV,NumPy; tqdm chỉ dùng cho progress và có fallback khi thiếu. Không trộn phiên bản rồi cam kết byte-identical mà chưa kiểm lại. Phiên bản của lần tạo mới được lưu trong `reproduction_environment.json`.

## Kiểm tra trước khi ghi

```powershell
python "Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py" --help
python "Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py" --dry-run
```

`--dry-run` kiểm nguồn/split và danh sách200ảnh nền, không tạo output hoặc cập nhật YAML đang dùng. Script xác định archive từ vị trí chính nó; không phụ thuộc cwd. Có thể chỉ định `--archive-root`, `--source-root`, `--output` khi layout khác.

## Tạo bản tái lập riêng

```powershell
python "Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py" --output "generated/Kvasir_YOLO_SEG_BG20_replay_20261026"
```

Đầu ra mặc định là `generated/Kvasir_YOLO_SEG_BG20_replay`. Mọi đường dẫn output tương đối được tính từ archive. Script **từ chối thư mục đã tồn tại**, từ chối output bên trong nguồn ảnh/mask và không xóa đệ quy. Nó chỉ ghi YAML vào output mới, không ghi đè `archive/data_bg20.yaml`. Muốn tạo lần khác, chọn tên thư mục output mới.

## Các bước dữ liệu và kiểm chứng

1. Giữ split880/120 của ảnh polyp.
2. Mặt nạBGR→gray, Otsu, morphology close3×3 một lần; external contours, loại area<20px².
3. `approxPolyDP` với epsilon0,002×chu vi, fallback contour khi ít hơn3đỉnh; chuẩn hóa và ghi6chữ số thập phân.
4. Sắp tên1.000ảnh normal-cecum, seed42 chọn200;160train và40val. Ảnh âm có prefixbg_ và labelrỗng.
5. Kiểm1.040ảnh/nhãntrain,160ảnh/nhãnval,160/40labelrỗng; so hash ảnh, nhãn và danh sách với bộ hiện hành.

Không chỉ kiểm count. Kiểm toán tái tạo1.000mask cho Otsu5–8;1.206contour,loại143,giữ1.063; vertices trung bình333,1552→24,6369. 999/1.000nhãn trùng từng ký tự ở môi trường đã nêu. `ck2bxiswtxuw80838qkisqjwz.txt` khác một đỉnh khoảng3px; hai polygon có IoU0,99981118 và27pixel raster khác. **Chưa xác định nguyên nhân**; không tự thay nhãn validation để làm kết quả đẹp hơn. Các ảnh polyp và200ảnh nền sao chép khớp byte.

Bằng chứng: [preprocessing độc lập](../audit_20261025_193105/root/preprocessing_independent.json), [replay bằng hàm builder và kiểm raster](../audit_20261025_193105/B_visual/dataset_label_crosscheck.json). Tệp và nhãn hiện hành được giữ nguyên.

## Dùng cho huấn luyện và đánh giá

Baseline nạp `yolo26s-seg.pt`; TSVM dựng YAML scale s và nạp phần pretrained tương thích từ cùng nguồn. TSVM phải import đúng fork `ultralytics_Topology-Shape-aware_VMamba_FP32/`, trainamp=False, lưu FP32 và suy luậnhalf=False. In đường dẫn import và phiên bản thực dùng. Hai notebook trong `Cell Kaggle/` chạy từng seed; notebook TSVM lịch sử có đường dẫn fork cũ nên phải điều chỉnh đúng môi trường trước dùng, không coi đổi tên run là xác nhận FP32.

Giữ args,CSV,hashcheckpoint,code/YAML và hashdataset cùng log. Không train hoặc suy luận trên output mới rồi gán kết quả sang run cũ. Cấu hình Kaggle do notebook tạo theo mount Kaggle; sửa pathlocal không chứng minh historical Kaggle đã dùng sai dữ liệu.

Validator trong train dùng rectangular validation và batch16 khi batchtrain8. Kiểm toán replaybest.pt dùngrect=True,batch16,imgsz640,half=False,CPU và bản sao validation riêng. Một probe rect=False,batch4 có AP khác, không được tính là lỗi checkpoint trước khi đồng nhất giao thức. Bảng chính chọn max-mask, còn best.pt chọn fitness box+mask;16/40run khác epoch.

## Kết quả và hiện vật legacy

Dùng [gói20seed](../Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/README.md) và các bảng chuẩn bên trong thư mục01–06. [LEGACY_ARTIFACTS](../Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/LEGACY_ARTIFACTS.md) chỉ rõ trường TN sai và cột winsloss ngược chiều trong các tệp gốc cũ. Không sửa raw hoặc đọc đè các trường đó như dữ liệu đo. Chưa có Dice pixel, topology hay testngoài; chưa đánh giáTurnitin30%.
''')

write('Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/README.md', '''# Kết quả 20 seed YOLO26s seg và TSVM FP32

Gói mở rộng16/10/2026; hướng dẫn nguồn cập nhật26/10/2026 sau kiểm toán. **Hai mô hình ×20seed(0–19) ×100epoch =40lượt huấn luyện.** Chỉ dùng nhóm TSVM có hậu tốFP32 cho bộ đối sánh chính.

## Nguồn nên dùng

| Thư mục | Nội dung |
|---|---|
| 01_raw_analysis | Trích lại40run,13metric,epoch lựa chọn và đường cong mean/sampleSD |
| 02_statistics | Mean/sampleSD,CI95%,pairedt,Wilcoxon,extrema,từngseed và win/loss |
| 03_metrics | Mask/box/validationloss |
| 04_confusion_matrix | TP/FP/FN theo đối tượng; TNảnhN/A; không specificity suy diễn |
| 05_charts | Các hình mới dùng sampleSDddof1 |
| 06_reports | Diễn giải, CSV và mapping hình cho luận văn |
| 07_audit | Manifest của lần sinh16/10; giữ nguyên để truy vết |
| efficiency_benchmark | BenchmarkCPUFP32 riêng, không dùng thời gian epoch làmFPS |

**Đọc [summary](06_reports/summary.md) trước trích dẫn.** Endpoint chính là epoch max-mask, khác best.pt box+maskfitness trong16/40run. MaskmAP50–95: Baseline0,718868±0,011768;TSVM0,723171±0,007197;p=0,061431,CI95%chứa0. Không kết luận ưu thế trung bình tạiα0,05 hoặc topology/lâm sàng.

## Hiện vật cũ không dùng làm nguồn mặc định

Các file `facts.json`, `raw_20seeds_confusion_matrices.csv`, `summary_20seeds_paired.csv` ở gốc và `figures/` được giữ nguyên. Một số trường có ngữ nghĩa không hợp lệ hoặc quy ước khác gói mới. **Không đọc `TN_reconstructed` thành TNảnh; không đọc `tsvm_wins=6` của valsegloss như số lần loss tốt hơn.** Chi tiết và đường dẫn thay thế nằm trong [LEGACY_ARTIFACTS.md](LEGACY_ARTIFACTS.md). Việc thêm cảnh báo không thay đổi raw, CSV, JSON, PNG hoặc manifest cũ.

## Tái lập và kiểm toán

Builder thống kê: `Stracth/Bao_Cao/generate_20seed_fp32_thesis_package.py`; đây là chương trình **ghi lại dẫn xuất**, không dùng chỉ để kiểm tra hiện trạng. Nên chạy kiểm toán đọc riêng hoặc chỉ tái sinh vào thư mục mới sau khi bảo toàn nguồn.

[Hướng dẫn BG20](../../doc/28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md) giải thích pathlocal, builder đúng và output mới không ghi đè. [Kiểm toán độc lập25/10](../../audit_20261025_193105/AUDIT_REPORT.md) đã kiểm số học36CSV,35PNG mới,40checkpoint và các giới hạn. Mọi chỉnh sửa ngày26/10 nằm trong `fix_20261026/`; không đổi bằng chứng của lần kiểm trước.
''')

write('Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/LEGACY_ARTIFACTS.md', '''# Quản lý các hiện vật legacy trong gói 20 seed FP32

Cập nhật26/10/2026. Các hiện vật liệt kê dưới đây được **giữ nguyên byte** để truy vết. Tệp này ngăn tái sử dụng nhầm trường hoặc hình cũ; không thay thế nguồn thực nghiệm và không sửa số liệu để khớp báo cáo.

| Hiện vật | Vấn đề đã xác nhận | Nguồn nên dùng |
|---|---|---|
| `facts.json` → `cm_mean.*.TN_reconstructed` | Mean của40−FPđối tượng không phải TNảnh | `04_confusion_matrix/count/detection_counts_mean_sd.csv`; TNảnhN/A |
| Root `raw_20seeds_confusion_matrices.csv` → `TN_reconstructed` | Không dùng suy specificity hoặc số ảnh nền đúng | `04_confusion_matrix/count/validated_detection_counts_per_seed.csv` |
| Root `summary_20seeds_paired.csv` → `val_seg_loss.tsvm_wins` | Giá trị6 đếm chiều loss tăng; lower-is-better thì TSVM thắng14, Baseline6 | `02_statistics/seed_comparison/seed_win_loss_summary.csv`, có cột `lower_is_better` |
| `figures/04_convergence_loss_curves.png`, `figures/05_metric_curves_mAP.png` | SDpopulationddof0; band nhỏ hơn sampleSD khoảng2,532% khi n20 | Hình mới trong `05_charts/convergence/`, ddof1 |
| 11hình trong `figures/` | Không tái tạo giống từng pixel ở môi trường kiểm toán, chưa xác định đầy đủ nguyên nhân render | Ưu tiên35hình mới (27kếtquả+8benchmark) có pixelreproduction; không gọi hình legacy là giả từ hash khác |

Phép tính số học của các CSV legacy có thể khớp raw nhưng tên/đơn vị vẫn sai. Không dùng dấu PASS kiểm toán số học để chứng nhận TNảnh hoặc hiệu quả lâm sàng. Một ảnh có thể có nhiều FP và FP có thể nằm trên ảnh polyp;40−FP không có nghĩa là số ảnh nền âm đúng.

Nguồn: [phòngA](../../audit_20261025_193105/A_numeric/report.md), [phòngB](../../audit_20261025_193105/B_visual/report.md), [danh sách phát hiện](../../audit_20261025_193105/ISSUES.csv). Manifest07_audit cũ giữ nguyên; cảnh báo này là bổ sung sau sinh gói.

Các chỉ số chính mới đã có sẵn và không cần sửa: maskAPp=0,061431,CI95%chứa0; không Dicepixel/topology hoặc testngoài. Bộ10seed và21seed là phạm vi lịch sử khác, không ghép số liệu bằng cách đổi nhãnN.
''')

historical_names=[
'00_TONG_QUAN_VA_TINH_HINH_DU_AN.md','03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md',
'04_KET_QUA_LOSS_VA_HOI_TU.md','06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md','07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md',
'08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md','10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md',
'16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md','17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md',
'18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md','20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md',
'21_HUONG_DAN_BAN_GIAO_AI_MOI_VA_VIEC_CONG_TAI.md','22_DANH_MUC_HINH_ANH_TOAN_BO.md',
'23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md','24_DANH_SACH_DUONG_DAN_HONG.md',
'25_KICH_BAN_PHAN_BIEN_SU_CO_FUSE_VA_MA_TRAN_NHAM_LAN.md','26_KET_QUA_BASELINE_VS_TSVM_BG20_21SEED_0_20.md',
'27_SU_CO_FP16_CHECKPOINT_TSVM_VA_CACH_KHAC_PHUC.md','GIAI_THICH_SU_CO_FUSE_CHO_NGUOI_DOC.md',
'training_results_audit.md','WEEKLY_REPORT_Ket_Qua_V2.md']
for name in historical_names:
    p=ROOT/'doc'/name
    if not p.exists():continue
    banner='''> **TÀI LIỆU LỊCH SỬ — cập nhật nhãn ngày26/10/2026.** Phạm vi, trạng thái và các số liệu bên dưới thuộc thời điểm viết, không phải nguồn hiện trạng20seedFP32. Đọc [trạng thái hiện tại](CURRENT_PROJECT_STATUS.md), [nguồn ưu tiên](README.md) và [hướng dẫn tái lập mới](28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md) trước khi sử dụng. Giữ nội dung cũ để truy vết; không trích các claim bị thay thế như kết quả hiện tại.

'''
    if '27_SU_CO_FP16' in name:
        banner='''> **HỒ SƠ SỰ CỐ LỊCH SỬ — cập nhật nhãn ngày26/10/2026.** Cơ chế lỗi lưu FP16 và bản vá trong tài liệu này vẫn là ngữ cảnh kỹ thuật; mục “chưa train/validate lại” phản ánh thời điểm viết. Bộ20seedFP32 và đánh giá lại40best.pt đã được kiểm toán sau đó. Xem [trạng thái hiện tại](CURRENT_PROJECT_STATUS.md) và [kiểm toán25/10](../audit_20261025_193105/AUDIT_REPORT.md); không biến trạng thái cũ thành hiện trạng.

'''
    elif 'FUSE' in name or 'FUSE' in name.upper():
        banner='''> **CHẨN ĐOÁN LỊCH SỬ ĐÃ BỊ THAY THẾ — cập nhật26/10/2026.** Giải thích lỗi do `fuse()` bên dưới không còn được dùng làm nguyên nhân đã xác nhận. Đọc [hồ sơ FP16](27_SU_CO_FP16_CHECKPOINT_TSVM_VA_CACH_KHAC_PHUC.md) và [trạng thái hiện tại](CURRENT_PROJECT_STATUS.md). Giữ văn bản cũ để truy vết, không dùng làm hướng dẫn “cứu hộ” hiện tại.

'''
    content=p.read_text(encoding='utf-8')
    if not content.startswith(banner):write(Path('doc')/name,banner+content)

for p in (ROOT/'Bao_cao/md viet bao cao').glob('*.md'):
    banner='''<!-- HISTORICAL_DRAFT_DO_NOT_BUILD_CURRENT -->
> **BẢN THẢO LỊCH SỬ — KHÔNG DÙNG ĐỂ SINH LẠI WORD HIỆN TẠI.** Nhãn cập nhật26/10/2026. Nội dung dưới đây chưa đồng bộ bộ20seedFP32 và có các phát biểu/số liệu đã bị kiểm toán thay thế. Bản Word chính cùng nguồn hiện tại được chỉ rõ tại [doc/README](../../doc/README.md) và [CURRENT_PROJECT_STATUS](../../doc/CURRENT_PROJECT_STATUS.md). Giữ bản thảo để truy vết, không đổi tên N10 thành N20 hoặc sử dụng TN/Dice/GPUclaim cũ như kết quả đã đo.

'''
    content=p.read_text(encoding='utf-8')
    if 'HISTORICAL_DRAFT_DO_NOT_BUILD_CURRENT' not in content[:100]:write(p.relative_to(ROOT),banner+content)

for name in ['README.md','CURRENT_PROJECT_STATUS.md']:
    p=ROOT.parent/name
    banner='''> **ĐIỂM VÀO HIỆN TẠI —26/10/2026:** Văn bản bên dưới là snapshot lịch sử của dự án. Bộ chính hiện là20seed mỗi mô hình Baseline/TSVMFP32, không phải10seed. Đọc [archive/doc/README](archive/doc/README.md) và [archive/doc/CURRENT_PROJECT_STATUS](archive/doc/CURRENT_PROJECT_STATUS.md). Giữ phần snapshot để truy vết; không dùng trường TN suy diễn hoặc trạng thái cũ như hiện trạng.

'''
    write(Path('..')/name,banner+p.read_text(encoding='utf-8'))

old=(ROOT/'doc/LICHSU_CAP_NHAT.md').read_text(encoding='utf-8')
write('doc/LICHSU_CAP_NHAT.md','''# Cập nhật ngày 26 tháng 10 năm 2026

Đã thay điểm vào tài liệu bằng nguồn20seedFP32 sau kiểm toán25/10; giữ snapshot cũ; sửa mô tả C2TSVMamba theo source; thêm hướng dẫn28 và cảnh báo legacyTN/winloss/ddof. Các bản thảo11MD được đánh dấu lịch sử, không dùng để sinh lại Word hiện tại. Cấu hình local và builderBG20 được sửa theo layout hiện tại, output tái lập mới không ghi đè nguồn. Không sửa rawCSV/checkpoint/nhãn hoặc thay p-value.

Nhật ký cũ bên dưới giữ nguyên như lịch sử; nhãn “hiện tại” của các phiên bản cũ không còn áp dụng. Chi tiết file và kiểm chứng trong `fix_20261026/documentation/` và nguồn hiện tại tại [README](README.md).

---

'''+old)

yaml=(ROOT/'data_bg20.yaml').read_text(encoding='utf-8')
yaml=yaml.replace('path: C:/LeDucLuong/HK VII/LuanCuNhan/DeepLearning/Test_Mau/archive/Kvasir_YOLO_SEG_BG20',
                  'path: '+(ROOT/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20').as_posix())
write('data_bg20.yaml',yaml)
(OUT/'documentation_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
print('WROTE',len(changes),'files; backups preserved')
