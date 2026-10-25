from pathlib import Path
import sys,json,re,unicodedata
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as ET
O=Path(__file__).parent;sys.path.insert(0,str(O/'packages'))
import pymupdf
sys.stdout.reconfigure(encoding='utf-8')
stage=sys.argv[1] if len(sys.argv)>1 else 'render_v2'
pdf=pymupdf.open(O/stage/'working_report.pdf');nav=json.loads((O/'navigation.json').read_text(encoding='utf-8'))
def norm(s):return re.sub(r'\s+','',unicodedata.normalize('NFKC',s).casefold()).replace('–','-').replace('−','-')
pages=[{'page':i+1,'text':p.get_text(),'words':len(p.get_text().split())} for i,p in enumerate(pdf)]
start=next(i for i,p in enumerate(pages) if p['text'].splitlines()[:2]==['1','MỞ ĐẦU'])
mapping={};missing=[]
heading_names={e['bookmark'] for e in nav['headings']}
for entry in nav['headings']+nav['figures']+nav['tables']:
    token=norm(entry['text'])
    if entry['bookmark'] in heading_names:
        found=[i for i in range(start,len(pages)) if any(norm(b[4])==token for b in pdf[i].get_text('blocks'))]
        if not found:found=[i for i in range(start,len(pages)) if token in norm(pages[i]['text'])]
    else:
        found=[i for i in range(start,len(pages)) if token in norm(pages[i]['text'])]
    if not found:missing.append(entry['text'])
    else:mapping[entry['bookmark']]=str(found[0]-start+1)
if missing:raise RuntimeError('Unmatched navigation entries: '+str(missing))
path=O/'working_report.docx'
with ZipFile(path) as z:parts={i.filename:(i,z.read(i.filename)) for i in z.infolist()}
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};q=lambda t:'{'+ns['w']+'}'+t
root=ET.fromstring(parts['word/document.xml'][1]);n=0
for fld in root.findall('.//w:fldSimple',ns):
    instr=fld.get(q('instr'),'');m=re.search(r'PAGEREF\s+(\S+)',instr)
    if m and m.group(1) in mapping:
        t=fld.find('.//w:t',ns)
        if t is not None:t.text=mapping[m.group(1)];n+=1
parts['word/document.xml']=(parts['word/document.xml'][0],ET.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True))
tmp=O/'nav_cached.docx'
with ZipFile(tmp,'w',ZIP_DEFLATED) as z:
    for name,(info,blob) in parts.items():z.writestr(info,blob)
tmp.replace(path)
(O/'page_mapping.json').write_text(json.dumps({'main_start_physical':start+1,'mapping':mapping,'pages':len(pdf)},ensure_ascii=False,indent=2),encoding='utf-8')
(O/f'pdf_pages_{stage}.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
print('Cached',n,'navigation references;',len(pdf),'pages; main text starts physical page',start+1)
print('Sparse pages:',[(p['page'],p['words']) for p in pages if p['words']<40])
