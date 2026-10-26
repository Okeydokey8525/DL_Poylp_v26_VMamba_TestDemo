from pathlib import Path
from urllib.request import Request,urlopen
from pypdf import PdfReader
import hashlib,csv,sys
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent
(OUT/'downloaded').mkdir(exist_ok=True)
items=[('Topo-VM-UNetV2','https://arxiv.org/pdf/2505.06210v1'),('CSG-Mamba','https://arxiv.org/pdf/2608.14146v1'),('MambaPSA','https://arxiv.org/pdf/2607.12681v1'),('SAM-MaGuP','https://arxiv.org/pdf/2507.01509v1')]
def fetch(item):
 name,url=item
 try:
  blob=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45).read()
  if not blob.startswith(b'%PDF'):raise ValueError('not PDF')
  p=OUT/'downloaded'/f'{name}.pdf';p.write_bytes(blob);r=PdfReader(p)
  text='\n\n'.join(f'===== PAGE {i+1} =====\n'+(pg.extract_text() or '') for i,pg in enumerate(r.pages))
  (OUT/'local_text'/f'{name}.txt').write_text(text,encoding='utf-8')
  return {'name':name,'url':url,'sha256':hashlib.sha256(blob).hexdigest(),'pages':len(r.pages),'status':'downloaded public arxiv PDF for private audit; not redistributed','error':''}
 except Exception as e:return {'name':name,'url':url,'sha256':'','pages':'','status':'unavailable','error':str(e)}
rows=list(ThreadPoolExecutor(max_workers=4).map(fetch,items))
with (OUT/'download_log.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
for r in rows:print(r)
