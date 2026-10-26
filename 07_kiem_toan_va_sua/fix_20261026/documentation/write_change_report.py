from pathlib import Path
import ast,hashlib,json,re
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'fix_20261026/documentation'
manifest=json.loads((OUT/'documentation_changes.json').read_text(encoding='utf-8'))
for row in manifest:
    p=Path(row['path']);row['after_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
(OUT/'documentation_changes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
old=json.loads((ROOT/'audit_20261025_193105/root/source_before.json').read_text(encoding='utf-8'))
dataset=(ROOT/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20').resolve();package=(ROOT/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32').resolve()
selected=[]
for row in old:
    p=Path(row['path'])
    if p.is_relative_to(dataset) or (p.is_relative_to(package) and p.suffix.lower() in {'.csv','.json','.png','.jpg'}):selected.append(row)
bad=[row['path'] for row in selected if not Path(row['path']).exists() or hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()!=row['sha256']]
guards=json.loads((OUT/'guard_exit_codes.json').read_text(encoding='utf-8-sig'))
proof={'protected_original_files_checked':len(selected),'changed_or_missing':bad,'guard_exit_codes':guards,'historical_headers_checked':[]}
for row in manifest:
    p=Path(row['path'])
    if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'))
    if p.suffix=='.md' and ('md viet bao cao' in p.parts or p.name in ['20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md','26_KET_QUA_BASELINE_VS_TSVM_BG20_21SEED_0_20.md']):
        head=p.read_text(encoding='utf-8').split('\n\n',1)[0]
        assert 'LỊCH SỬ' in head or 'HISTORICAL' in head
        proof['historical_headers_checked'].append(str(p.relative_to(ROOT)))
assert not bad
assert all(v==2 for v in guards.values())
(OUT/'protected_sources_check.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# Chỉnh sửa tài liệu và khả năng tái lập ngày 26 tháng 10 năm 2026','',
'Đã sửa tài liệu và script hỗ trợ trong phạm vi được giao; không sửa Word (parent xử lý riêng), Web, raw CSV, checkpoint, nhãn hay hình kết quả gốc. Các bản sao trước sửa nằm trong `backups/`; `documentation_changes.json` ghi hash trước/sau của từng tệp.','',
'## Thay đổi','',
'- Thay `doc/README.md` và `doc/CURRENT_PROJECT_STATUS.md` bằng điểm vào 20 seed FP32; lưu snapshot cũ; phân biệt max-mask với best-fitness và kết quả replay checkpoint. Không đổi endpoint hay p-value chính.','- Sửa `doc/01_KIEN_TRUC_TSVM_TANG_10.md` theo source: layer10/P5, kích thước sau scale s, gate1+G, không ratio4, FFN haiConv1×1, workO(LlogL)/depthO(logL), không hứa AMP/topology/backward đã được chứng minh.','- Thêm `doc/28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md`; sửa `data_bg20.yaml` tới dữ liệu hiện hành. Hướng dẫn ghi đúng builder BG20, thư mục normal-cecum lồng, môi trường và sai khác999/1000nhãn đã xác nhận.','- Builder BG20 tự tìm archive/source hiện tại, có `--dry-run`, `--output`, không xóa/merge thư mục hiện hữu và không ghi root YAML. Output mặc định là bản replay mới; từ chối nằm trong nguồn, canonicaldataset hoặc rawrun. Có fallback khi thiếu tqdm; thuật toán chuyển mask và seed không thay đổi.','- Đánh dấu21hồ sơ/ghi chú cũ và11bản thảo Markdown là lịch sử. Riêng hồ sơ27 giữ vai trò giải thích cơ chế FP16; chỉ trạng thái cũ bị thay thế. Parent README/CURRENT được thêm redirect, phần snapshot nguyên văn giữ lại.','- Thêm `LEGACY_ARTIFACTS.md` và sửa READMEgói20seed để ngăn dùng TN_reconstructed và thắngloss đảo chiều; trỏ đúng bảng mới TSVM14vsBaseline6. Không thay bất kỳ byte CSV/JSON/PNGcũ.','- Chặn builder Word Markdown lịch sử ở chế độ mặc định. Muốn xuất lịch sử phải opt-in và chọn tệp mới; luôn từ chối hai Word chính hoặc output đã tồn tại. Không tạo Word trong các phép kiểm guard.','',
'## Kiểm chứng','',
'- `--help` và `--dry-run` chạy được trên Python app venv; dry-run không tạo output.','- Full build vào `fix_20261026/documentation/reproduced_bg20`:1.040train/160val,160/40nhãn rỗng,936/127instances. 1.200ảnh và danh sách200ảnh nền khớp byte; nhãn999/1000khớp, đúng một khác biệt đã được kiểm toán trước đó. Không đưa output replay vào dữ liệu huấn luyện hiện hành.','- Các lệnh output đã tồn tại/canonical dataset và ghi đè Word chính đều bị chặn, exit2. Canonical child cũng bị từ chối, không tạo thư mục.','- Sáu Markdown hiện hành không có link nội bộ thiếu;11bản thảo có marker lịch sử; Python hỗ trợ parse được.','- '+str(len(selected))+'tệp dữ liệu/CSV/JSON/PNGnguồn được so với manifest kiểm toán cũ:0thay đổi/mất. `protected_sources_check.json` lưu chi tiết.','',
'## Phần chưa đóng','',
'Không sửa nhãn sai khác một đỉnh, không khẳng định split880/120 do tác giả phát hành, không đánh giáTurnitin30%. Trạng thái Web sau sửa được parent cập nhật theo kiểm thử thật sau khi gộp các phòng; tài liệu không tự ghi pass chỉ vì code đổi.','',
'## Tệp thay đổi','']
lines.extend('- `'+str(Path(x['path']).relative_to(ROOT) if Path(x['path']).is_relative_to(ROOT) else Path('..')/Path(x['path']).name)+'`' for x in manifest)
(OUT/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('CHANGED',len(manifest),'PROTECTED',len(selected),'BAD',len(bad))
