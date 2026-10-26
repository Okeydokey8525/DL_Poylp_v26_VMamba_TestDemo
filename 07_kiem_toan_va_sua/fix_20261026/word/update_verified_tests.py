from pathlib import Path
import hashlib,json,shutil,sys,zipfile
from lxml import etree as E
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];main=ROOT/'Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx';alias=ROOT/'Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong_MoRong_FP32.docx'
log=json.loads((HERE/'changes.json').read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(main)==log['after_sha256']==sha(alias)
tests=json.loads((ROOT/'fix_20261026/integration/java_test_summary.json').read_text())
assert tests['totals']=={'tests':274,'failures':0,'errors':0,'skipped':0}
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(main) as z:members={x.filename:(x,z.read(x.filename)) for x in z.infolist()}
rt=E.fromstring(members['word/document.xml'][1]);table=rt.findall('w:body/w:tbl',NS)[8];rows=table.findall('w:tr',NS)
def get(n):return ''.join(t.text or '' for t in n.findall('.//w:t',NS))
def replace(n,new,where):
 old=get(n);ts=n.findall('.//w:t',NS)
 if not ts:ts=[E.SubElement(E.SubElement(n,'{'+NS['w']+'}r'),'{'+NS['w']+'}t')]
 ts[0].text=new
 for t in ts[1:]:t.text=''
 log['changes'].append({'location':where,'old':old,'new':new})
assert get(rows[2].findall('w:tc',NS)[2])=='261 kiểm thử đạt'
replace(rows[2].findall('w:tc',NS)[1],'Unit/MockMvc, API, phân quyền và MongoDB thật','Bảng 4.3 / Spring Boot / Phạm vi')
replace(rows[2].findall('w:tc',NS)[2],'274 kiểm thử đạt','Bảng 4.3 / Spring Boot / Kết quả')
replace(rows[3].findall('w:tc',NS)[2],'498 đạt (log cũ)','Bảng 4.3 / Flutter / Kết quả')
p=rt.findall('w:body/w:p',NS)[513];assert get(p)==''
replace(p,'Ngày 26/10/2026: FastAPI 51 và Web 274 kiểm thử đạt, gồm 4 test MongoDB thật. Flutter dùng log cũ, chưa chạy lại.','P0514 / thời điểm và phạm vi kiểm thử')
updated=E.tostring(rt,encoding='UTF-8',xml_declaration=True,standalone=True);tmp=HERE/'report_final.docx'
with zipfile.ZipFile(tmp,'w') as z:
 for name,(info,data) in members.items():z.writestr(info,updated if name=='word/document.xml' else data)
for target in [main,alias]:
    stage=target.with_name(target.stem+'.fix_20261026.tmp.docx')
    shutil.copy2(tmp,stage)
    stage.replace(target)
log['after_sha256']=sha(main);log['alias_sha256']=sha(alias)
(HERE/'changes.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8');print('Updated verified tests and historical Mobile qualifier; edits',len(log['changes']))
