from pathlib import Path
import sys,json,hashlib,csv,re,unicodedata
from zipfile import ZipFile
from lxml import etree as E
O=Path(__file__).parent;R=O.parent;P=R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32'
sys.path.insert(0,str(R/'.codex_report_work_20261015/packages'))
import pymupdf
from docx import Document
sys.stdout.reconfigure(encoding='utf-8')
manifest=json.loads((P/'07_audit/source_manifest.json').read_text(encoding='utf-8'))
for x in manifest['inputs']:
    assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256'],x['path']
bench=list(csv.DictReader((P/'efficiency_benchmark/tables/efficiency_summary.csv').open(encoding='utf-8-sig')))
assert len(bench)==4 and all(int(x['n'])==100 for x in bench)
stats=list(csv.DictReader((P/'02_statistics/mean_std/full_comparison_mean_std.csv').open(encoding='utf-8-sig')))
assert len(stats)==13
pdf=pymupdf.open(O/'render_release/working_report.pdf');doc=Document(O/'working_report.docx')
nav=json.loads((O/'navigation.json').read_text(encoding='utf-8'))
with ZipFile(O/'working_report.docx') as z:root=E.fromstring(z.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};q=lambda x:'{'+ns['w']+'}'+x
names=[x.get(q('name')) for x in root.findall('.//w:bookmarkStart',ns)]
assert len(names)==len(set(names))
def norm(s):return re.sub(r'\s+','',unicodedata.normalize('NFKC',s).casefold()).replace('–','-').replace('−','-')
pages=[p.get_text() for p in pdf];start=next(i for i,t in enumerate(pages) if t.splitlines()[:2]==['1','MỞ ĐẦU'])
blocks=[[norm(b[4]) for b in p.get_text('blocks')] for p in pdf]
mapping={}
for e in nav['headings']+nav['figures']+nav['tables']:
    token=norm(e['text']);found=[]
    if e in nav['headings']:found=[i for i in range(start,len(pdf)) if token in blocks[i]]
    if not found:found=[i for i in range(start,len(pdf)) if token in norm(pages[i])]
    assert found,e
    mapping[e['bookmark']]=str(found[0]-start+1)
field_count=0
for fld in root.findall('.//w:fldSimple',ns):
    m=re.search(r'PAGEREF\s+(\S+)',fld.get(q('instr'),''))
    if m:
        field_count+=1
        assert fld.find('.//w:t',ns).text==mapping[m[1]],(m[1],fld.find('.//w:t',ns).text,mapping[m[1]])
changed=[i for i in range(1,len(pdf)+1) if hashlib.sha256((O/'render_release'/f'page-{i}.png').read_bytes()).digest()!=hashlib.sha256((O/'render_final'/f'page-{i}.png').read_bytes()).digest()]
summary={'date':'2026-10-16','source_hashes_passed':len(manifest['inputs']),'metric_count':len(stats),'training_runs':40,'epochs_per_run':100,'benchmark_timing_rows':400,'benchmark_groups':4,'new_result_figures':len(list((P/'05_charts').rglob('*.png')))+len(list((P/'04_confusion_matrix').rglob('*.png'))),'new_benchmark_figures':len(list((P/'efficiency_benchmark/figures').glob('*.png'))),'report_pages':len(pdf),'report_figures':len(nav['figures']),'report_tables_including_abbreviations':len(doc.tables),'navigation_fields_checked':field_count,'pages_changed_after_final_review':changed,'report_sha256':hashlib.sha256((O/'working_report.docx').read_bytes()).hexdigest()}
(P/'07_audit/release_validation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
