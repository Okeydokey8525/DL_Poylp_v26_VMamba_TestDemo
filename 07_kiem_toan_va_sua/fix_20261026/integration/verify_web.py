"""Regression checks against a disposable local Web/AI/Mongo environment."""
from pathlib import Path
import hashlib,json,re,secrets,sys
import requests
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
WEB='http://127.0.0.1:18080';AI='http://127.0.0.1:18000'
IMAGE=ROOT/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/images/val/cju0s690hkp960855tjuaqvv0.jpg'
RESULTS=[]
def check(name,actual,expected,details=None):
    ok=actual==expected;RESULTS.append({'case':name,'actual':actual,'expected':expected,'pass':ok,'details':details})
    (HERE/'runtime_results.json').write_text(json.dumps(RESULTS,ensure_ascii=False,indent=2),encoding='utf-8');print(name,ok,flush=True)
def csrf(s):
    r=s.get(WEB+'/api/v1/auth/csrf',timeout=20);r.raise_for_status();j=r.json();return {j['headerName']:j['token']}
creds={'email':f'fix_{secrets.token_hex(4)}@example.invalid','password':'Fix'+secrets.token_hex(8)+'7','other_email':f'other_{secrets.token_hex(4)}@example.invalid','other_password':'Fix'+secrets.token_hex(8)+'8'}
(HERE/'runtime/test_credentials.json').write_text(json.dumps(creds),encoding='utf-8')
def account(label,email,pw):
    s=requests.Session();r=s.post(WEB+'/api/v1/auth/register',headers=csrf(s),json={'fullName':label,'email':email,'password':pw,'confirmPassword':pw,'acceptedTerms':True},timeout=20);check('register_'+label,r.status_code,201)
    r=s.post(WEB+'/api/v1/auth/login',headers=csrf(s),json={'email':email,'password':pw},timeout=20);check('login_'+label,r.status_code,200);return s
def upload(s,path,model=None):
    with IMAGE.open('rb') as f:return s.post(WEB+path,headers=csrf(s),data={'modelType':model} if model else {},files={'image':(IMAGE.name,f,'image/jpeg')},timeout=90)
health=requests.get(AI+'/health',timeout=30);check('AI health',health.status_code,200)
(HERE/'runtime/health.json').write_text(json.dumps(health.json(),indent=2),encoding='utf-8')
home=requests.get(WEB,timeout=20);check('home',home.status_code,200);check('home contains current S keys','YOLO26s-seg và YOLO26s-TSVM-FP32-seg' in home.text,True);check('home no Nano copy','YOLO26n' in home.text,False)
a=account('Fix Primary',creds['email'],creds['password']);other=account('Fix Other',creds['other_email'],creds['other_password'])
check('empty comparison history HTML',a.get(WEB+'/comparisons',timeout=20).status_code,200)
r=a.get(WEB+'/api/v1/comparisons',timeout=20);check('empty comparison history API',r.status_code,200)
records=[]
for model,badge in [('YOLO26s-seg','Baseline'),('YOLO26s-TSVM-FP32-seg','VMamba')]:
    r=upload(a,'/api/v1/diagnoses',model);check('create '+model,r.status_code,201)
    r.raise_for_status();record=r.json();records.append(record);did=record['id']
    html=a.get(WEB+'/diagnoses/'+did,timeout=20);check('result HTML '+model,html.status_code,200)
    tag=re.search(r'<span[^>]*class="[^"]*model-family-badge[^>]*>(.*?)</span>',html.text,re.S)
    actual_badge=re.sub('<[^>]+>','',tag.group(1)).strip() if tag else None
    check('badge '+model,actual_badge,badge)
    check('actual dimensions '+model,'621 × 530 px' in html.text,True)
    check('no hardcoded dimensions '+model,'1280 × 720 px' in html.text,False)
    check('other user cannot read '+model,other.get(WEB+'/api/v1/diagnoses/'+did,timeout=20).status_code,403)
    for kind in ['original','result']:
        data=a.get(WEB+'/diagnoses/'+did+'/download/'+kind,timeout=20);check('download '+kind+' '+model,data.status_code,200)
        if data.ok:(HERE/'runtime'/f'{did}_{kind}.jpg').write_bytes(data.content)
r=upload(a,'/api/v1/comparisons');check('create comparison',r.status_code,201);r.raise_for_status();comparison=r.json();gid=comparison['comparisonGroupId']
r=a.get(WEB+'/comparisons',timeout=20);check('populated comparison history HTML',r.status_code,200);check('group rendered in history',gid in r.text,True)
r=a.get(WEB+'/api/v1/comparisons',timeout=20);check('populated comparison history API',r.status_code,200);check('group returned in API',gid in r.text,True)
(HERE/'runtime/comparison_history.json').write_text(json.dumps(r.json(),ensure_ascii=False,indent=2),encoding='utf-8')
check('comparison detail HTML',a.get(WEB+'/comparisons/'+gid,timeout=20).status_code,200)
check('nonowner comparison forbidden',other.get(WEB+'/api/v1/comparisons/'+gid,timeout=20).status_code,403)
check('owner comparison export',a.get(WEB+'/comparisons/'+gid+'/metadata.json',timeout=20).status_code,200)
check('other user history isolation',gid in other.get(WEB+'/api/v1/comparisons',timeout=20).text,False)
for model in ['YOLO26s-seg','YOLO26s-TSVM-FP32-seg']:
    with IMAGE.open('rb') as f:r=requests.post(AI+'/predict',data={'modelType':model},files={'image':(IMAGE.name,f,'image/jpeg')},timeout=90)
    check('true inference '+model,r.status_code,200)
    j=r.json();j.pop('resultImageBase64',None);(HERE/'runtime'/('inference_'+model+'.json')).write_text(json.dumps(j,indent=2),encoding='utf-8')
    check('mask count '+model,j.get('maskCount'),1 if model=='YOLO26s-seg' else 2)
state={'diagnoses':records,'comparison':comparison,'image':str(IMAGE),'image_sha256':hashlib.sha256(IMAGE.read_bytes()).hexdigest()}
(HERE/'runtime/created_records.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
summary={'cases':len(RESULTS),'passed':sum(r['pass'] for r in RESULTS),'failed':[r for r in RESULTS if not r['pass']]}
(HERE/'runtime_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');print(summary,flush=True)
sys.exit(bool(summary['failed']))
