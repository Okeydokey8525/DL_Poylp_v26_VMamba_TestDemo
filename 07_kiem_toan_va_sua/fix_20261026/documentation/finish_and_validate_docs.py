from pathlib import Path
import csv,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'fix_20261026/documentation'
records=json.loads((OUT/'documentation_changes.json').read_text(encoding='utf-8'))

def pretty_plain(s):
    protected=[]
    def keep(m):
        token='\ue000'+chr(0xe100+len(protected))+'\ue001';protected.append(m.group())
        prefix=' ' if m.start()>0 and s[m.start()-1].isalnum() else ''
        suffix=' ' if m.end()<len(s) and s[m.end()].isalnum() else ''
        return prefix+token+suffix
    s=re.sub(r'YOLO26[nsmlx]?|FP(?:16|32|64)|SS2D|C2TSVMamba|C2PSA|Segment26|\bP[345]\b|\bP\d{4}\b|\bT\d{2}R\d{3}\b|\bL1\b|\bF1\b|\b\d+(?:\.\d+)?e[-+]?\d+\b',keep,s)
    letter=r'A-Za-zÀ-ÖØ-öø-ÿĀ-ỹ'
    s=re.sub(r'(['+letter+r'])(?=\d)',r'\1 ',s)
    s=re.sub(r'(\d)(?=['+letter+r'])',r'\1 ',s)
    for i,p in enumerate(protected):s=s.replace('\ue000'+chr(0xe100+i)+'\ue001',p)
    s=s.replace('cặpGT','cặp GT').replace('labelrỗng','label rỗng').replace('amp=False','amp=False').replace('rawCSV','raw CSV')
    return s

def pretty(s):
    parts=re.split(r'(```.*?```|`[^`]*`|\]\([^)]*\))',s,flags=re.S)
    return ''.join(p if i%2 else pretty_plain(p) for i,p in enumerate(parts))

active=['doc/README.md','doc/CURRENT_PROJECT_STATUS.md','doc/01_KIEN_TRUC_TSVM_TANG_10.md',
        'doc/28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md','Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/README.md',
        'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/LEGACY_ARTIFACTS.md']
for relative in active:
    p=ROOT/relative;s=p.read_text(encoding='utf-8');s=pretty(s)
    if relative.endswith('28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md'):
        s=s.replace('`Ket_Qua_V2/Data Prosessing/normal-cecum/`.','`Ket_Qua_V2/Data Prosessing/normal-cecum/normal-cecum/` (builder tự nhận dạng lớp thư mục lồng này).')
        if '## Builder báo cáo Markdown lịch sử' not in s:s += '''
## Builder báo cáo Markdown lịch sử

`Stracth/Bao_Cao/build_huit_final_report_from_md.py` không còn ghi đè báo cáo chính mặc định. Nó chặn các tệp có marker lịch sử. Nếu cần một bản sao lịch sử để truy vết, phải truyền `--allow-historical-drafts --output <tệp-docx-mới>`; hai đường dẫn Word chính và mọi tệp đã tồn tại vẫn bị từ chối. Opt-in không xác nhận các claim cũ là đúng. Không chạy các builder báo cáo khác lên bản Word hiện tại trước khi kiểm tra nguồn và output.
'''
    s=s.replace('lr 0','lr0').replace('float 16','float16').replace('float 32','float32').replace('ddof 0','ddof=0').replace('ddof 1','ddof=1')
    if relative.endswith('28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md'):
        heading='## Builder báo cáo Markdown lịch sử'
        first=s.find(heading);second=s.find(heading,first+len(heading)) if first>=0 else -1
        if second>=0:s=s[:second].rstrip()+'\n'
    p.write_text(s,encoding='utf-8')

for row in records:
    p=Path(row['path'])
    if p.exists():row['after_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
(OUT/'documentation_changes.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')

missing=[]
for relative in active:
    p=ROOT/relative;s=p.read_text(encoding='utf-8')
    for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',s):
        if target.startswith(('http:','https:','#')):continue
        path=target.strip('<>').split('#')[0]
        if path and not (p.parent/path).exists():missing.append({'file':relative,'target':target})
source=ROOT/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20';reproduced=OUT/'reproduced_bg20'
data={'active_documents':len(active),'missing_active_doc_links':missing,'historical_drafts':0,'reproduction':{}}
for p in (ROOT/'Bao_cao/md viet bao cao').glob('*.md'):
    assert 'HISTORICAL_DRAFT_DO_NOT_BUILD_CURRENT' in p.read_text(encoding='utf-8')[:100]
    data['historical_drafts']+=1
if reproduced.exists():
    for split in ['train','val']:
        images=list((reproduced/'images'/split).glob('*.jpg'));labels=list((reproduced/'labels'/split).glob('*.txt'))
        data['reproduction'][split]={'images':len(images),'labels':len(labels),'empty':sum(not p.read_text().strip() for p in labels),'instances':sum(len(p.read_text().splitlines()) for p in labels)}
    labels=[p for split in ['train','val'] for p in (reproduced/'labels'/split).glob('*.txt') if p.read_text().strip()]
    diff=[str(p.relative_to(reproduced)) for p in labels if p.read_bytes()!=(source/p.relative_to(reproduced)).read_bytes()]
    data['reproduction']['nonempty_labels']=len(labels);data['reproduction']['label_byte_mismatches']=diff
    image_diff=[str(p.relative_to(reproduced)) for split in ['train','val'] for p in (reproduced/'images'/split).glob('*.jpg') if hashlib.sha256(p.read_bytes()).digest()!=hashlib.sha256((source/p.relative_to(reproduced)).read_bytes()).digest()]
    data['reproduction']['image_byte_mismatches']=image_diff
    data['reproduction']['background_lists_exact']={split:(reproduced/f'selected_normal_cecum_{split}_{160 if split=="train" else 40}.txt').read_bytes()==(source/f'selected_normal_cecum_{split}_{160 if split=="train" else 40}.txt').read_bytes() for split in ['train','val']}
data['builder_has_recursive_delete']='rmtree(' in (ROOT/'Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py').read_text(encoding='utf-8')
(OUT/'validation.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(data,ensure_ascii=False,indent=2))
