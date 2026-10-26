from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import quote
import json,sys
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent
(OUT/'metadata').mkdir(exist_ok=True)
items=[('CIT-001','https://api.crossref.org/works/'+quote('10.1007/978-3-030-37734-2_37',safe='')),('CIT-002','https://api.crossref.org/works/'+quote('10.1145/3083187.3083212',safe='')),('CIT-006','https://api.crossref.org/works/'+quote('10.1109/TSMC.1979.4310076',safe='')),('CIT-008','https://api.crossref.org/works/'+quote('10.1016/0734-189X(85)90016-7',safe='')),('CIT-009','https://api.crossref.org/works/'+quote('10.3138/FM57-6770-U75U-7727',safe='')),('CIT-017','https://api.crossref.org/works/'+quote('10.1007/978-3-031-72111-3_48',safe='')),('KAGGLE_FILES','https://www.kaggle.com/api/v1/datasets/list/debeshjha1/kvasirseg')]
def one(item):
 name,url=item
 try:
  raw=urlopen(Request(url,headers={'User-Agent':'ResearchReferenceAudit/1.0'}),timeout=25).read()
  j=json.loads(raw);(OUT/'metadata'/f'{name}.json').write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
  m=j.get('message',j);return {'id':name,'url':url,'status':'retrieved','title':m.get('title','') if isinstance(m,dict) else '', 'keys':list(m)[:8] if isinstance(m,dict) else []}
 except Exception as e:return {'id':name,'url':url,'status':str(e)}
results=list(ThreadPoolExecutor(max_workers=4).map(one,items))
(OUT/'metadata_fetch_log.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
for r in results:print(r)
