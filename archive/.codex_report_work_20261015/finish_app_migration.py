from pathlib import Path
import shutil
R=Path(__file__).resolve().parents[1];A=(R/'../../Ung_Dung/polypweb').resolve();B=Path(__file__).parent/'app_backup'
skip={'.git','.venv','build','target','.dart_tool','runs','__pycache__','.agents','.codex'}
for p in A.rglob('*'):
    if not p.is_file() or any(s in skip for s in p.relative_to(A).parts):continue
    if p.suffix not in {'.java','.py','.dart','.html','.md'}:continue
    t=p.read_text(encoding='utf-8-sig');u=t.replace('yolo26n-vmamba-seg','yolo26s-tsvm-fp32-seg').replace('yolo26n-seg','yolo26s-seg')
    u=u.replace('Phiên bản nano, ưu tiên tốc độ và tài nguyên tính toán thấp.','Mô hình YOLO26s-seg cơ bản dùng đối chiếu thực nghiệm BG20.').replace('Biến thể nano tích hợp VMambaBlock ở feature map mức cao.','YOLO26s-seg thay C2PSA bằng C2TSVMamba tại tầng 10 và suy luận FP32.')
    if u!=t:
        b=B/p.relative_to(A)
        if not b.exists():b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b)
        p.write_text(u,encoding='utf-8')
p=A/'README.md';t=p.read_text(encoding='utf-8');i=t.index('`YOLO26s-TSVM-FP32-seg` tích hợp');j=t.index('Hai model key/checkpoint',i)
t=t[:i]+'''`YOLO26s-TSVM-FP32-seg` dùng đúng khối `C2TSVMamba` của thực nghiệm BG20, thay `C2PSA` tại layer 10. Khối kết hợp SS2D bốn hướng, nhánh hình dạng đa tỉ lệ và có hướng, cổng guidance `F_M * (1 + G)` và residual scaling. Mã được lưu tại `custom_ultralytics/topology_shape_vmamba.py` và đăng ký theo đường dẫn module trong checkpoint trước khi tải trọng số.

Hai checkpoint mặc định lấy từ seed 0 của thực nghiệm YOLO26s-seg và TSVM FP32, cùng một seed để minh họa. `models/experiment_manifest.json` lưu nguồn và SHA-256. Việc chọn `best.pt` theo fitness của Ultralytics khác việc lấy epoch có mask mAP cao nhất trong bảng tổng hợp 20 seed. Ứng dụng ép mô hình về float32 và suy luận với `half=False`; không dùng lại trọng số TSVM cũ không có FP32.

''' +t[j:];p.write_text(t,encoding='utf-8')
p=A/'polypweb/ai-service/README.md';t=p.read_text(encoding='utf-8');i=t.index('Checkpoint VMamba cần');j=t.index('Không commit checkpoint',i)
t=t[:i]+'''Checkpoint TSVM FP32 cần các lớp trong `ultralytics.nn.modules.topology_shape_vmamba` được đăng ký trước khi tải. Bản mã vendored được sao chép từ thực nghiệm FP32; khối `C2TSVMamba` thay C2PSA ở layer 10. Không dùng `VMambaBlock` của nghiên cứu Nano cũ cho checkpoint này.

Hai trọng số mặc định là `best.pt` của seed 0 từ đúng hai thư mục thực nghiệm Baseline và TSVM_FP32. Nguồn và mã băm nằm trong `models/experiment_manifest.json`. Khi tải, dịch vụ kiểm tra task segment, lớp polyp và sự hiện diện của C2TSVMamba đối với mô hình cải tiến. Cả hai mô hình chạy float32 với `half=False`. Ảnh RGB sau giải mã được truyền dưới dạng PIL để Ultralytics không hiểu nhầm thành BGR.

''' +t[j:];p.write_text(t,encoding='utf-8')
print('Updated lowercase model selectors and architecture documentation.')
