from pathlib import Path
from pypdf import PdfReader
import csv,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
TLTK=ROOT.parent.parent/'TLTK'
(OUT/'local_text').mkdir(exist_ok=True)
rows=[]
for p in sorted(TLTK.glob('*.pdf'),key=lambda p:int(re.search(r'\[(\d+)\]',p.name)[1])):
    n=int(re.search(r'\[(\d+)\]',p.name)[1]);r=PdfReader(p)
    pages=[page.extract_text() or '' for page in r.pages]
    text='\n\n'.join(f'===== PAGE {i+1} =====\n'+s for i,s in enumerate(pages))
    dest=OUT/'local_text'/f'TLTK-{n:02}.txt';dest.write_text(text,encoding='utf-8')
    md=r.metadata or {}
    rows.append({'local_id':f'TLTK-{n:02}','filename':p.name,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pages':len(pages),'pdf_title':md.get('/Title',''),'pdf_author':md.get('/Author',''),'first_page_text':pages[0][:3000],'extracted_file':str(dest),'characters':len(text)})
with (OUT/'local_pdf_inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print('PDF extracted',len(rows))
for x in rows:print(x['local_id'],x['pages'],repr(x['pdf_title']),x['first_page_text'][:300].replace('\n',' '))
