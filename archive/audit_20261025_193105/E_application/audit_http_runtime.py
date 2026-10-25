"""Exercise isolated current-source Web/AI. Never targets real user database/storage."""
from pathlib import Path
import base64,csv,hashlib,json,secrets,time
import requests

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
WEB='http://127.0.0.1:18080';AI='http://127.0.0.1:18000'
VAL=ROOT/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/images/val'
POLYP=VAL/'cju0s690hkp960855tjuaqvv0.jpg'
BG=VAL/'bg_0111fb06-3113-4abf-9050-7bfb8d4688f5.jpg'
RESULTS=[]

def record(name,r,expected,extra=None):
    row={'case':name,'status':r.status_code,'expected_status':expected,'pass':r.status_code in expected,'url':r.url,'bytes':len(r.content),'extra':extra}
    if 'application/json' in r.headers.get('Content-Type',''):
        try:row['json']={k:v for k,v in r.json().items() if 'base64' not in k.lower()}
        except (ValueError,AttributeError):pass
    RESULTS.append(row)
    (HERE/'runtime_http_results.json').write_text(json.dumps(RESULTS,ensure_ascii=False,indent=2),encoding='utf-8')
    print(name,r.status_code,row['pass'],flush=True)
    return r

def csrf(s):
    r=s.get(WEB+'/api/v1/auth/csrf',timeout=20);r.raise_for_status();v=r.json();return {v['headerName']:v['token']}

def account(name,email,password):
    s=requests.Session();h=csrf(s)
    r=s.post(WEB+'/api/v1/auth/register',headers=h,json={'fullName':name,'email':email,'password':password,'confirmPassword':password,'acceptedTerms':True},timeout=20)
    record('register_'+name,r,[201,409]);h=csrf(s)
    record('login_'+name,s.post(WEB+'/api/v1/auth/login',headers=h,json={'email':email,'password':password},timeout=20),[200])
    return s

def upload(s,url,model=None,image=POLYP):
    with image.open('rb') as f:return s.post(WEB+url,headers=csrf(s),data={'modelType':model} if model else {},files={'image':(image.name,f,'image/jpeg')},timeout=90,allow_redirects=False)

health=requests.get(AI+'/health',timeout=30);record('ai_health',health,[200]);(HERE/'runtime/health.json').write_text(json.dumps(health.json(),indent=2),encoding='utf-8')
record('web_health',requests.get(WEB+'/actuator/health',timeout=30),[200])
record('unauthenticated_diagnose',requests.get(WEB+'/diagnose',allow_redirects=False,timeout=20),[302])
record('unauthenticated_api',requests.get(WEB+'/api/v1/diagnoses',timeout=20),[401])
record('csrf_missing_login',requests.post(WEB+'/api/v1/auth/login',json={'email':'audit@example.invalid','password':'invalid123'},timeout=20),[403])

smoke=[]
for model in ['YOLO26s-seg','YOLO26s-TSVM-FP32-seg']:
    for image in [POLYP,BG]:
        with image.open('rb') as f:r=requests.post(AI+'/predict',data={'modelType':model},files={'image':(image.name,f,'image/jpeg')},timeout=90)
        record('true_inference_'+model+'_'+('polyp' if image==POLYP else 'background'),r,[200])
        if r.ok:
            j=r.json();encoded=j.pop('resultImageBase64',None)
            if encoded:(HERE/'screenshots'/('overlay_'+model+'_'+('polyp' if image==POLYP else 'background')+'.jpg')).write_bytes(base64.b64decode(encoded))
            smoke.append({'input':image.name,'input_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),**j})
(HERE/'runtime/true_inference_smoke.json').write_text(json.dumps(smoke,indent=2),encoding='utf-8')
record('ai_reject_non_image',requests.post(AI+'/predict',data={'modelType':'YOLO26s-seg'},files={'image':('bad.txt',b'not an image','text/plain')},timeout=20),[415])
record('ai_reject_unknown_model',requests.post(AI+'/predict',data={'modelType':'unknown'},files={'image':('x.jpg',b'x','image/jpeg')},timeout=20),[422])

credentials={'email':'audit_primary_20261025@example.invalid','password':'Audit'+secrets.token_hex(8)+'7','other_email':'audit_other_20261025@example.invalid','other_password':'Audit'+secrets.token_hex(8)+'8'}
(HERE/'runtime/test_credentials.json').write_text(json.dumps(credentials),encoding='utf-8')
a=account('Audit Primary',credentials['email'],credentials['password']);b=account('Audit Other',credentials['other_email'],credentials['other_password'])
record('authenticated_me',a.get(WEB+'/api/v1/me',timeout=20),[200])
diags=[]
for model in ['YOLO26s-seg','YOLO26s-TSVM-FP32-seg']:
    r=record('web_api_create_'+model,upload(a,'/api/v1/diagnoses',model),[201])
    if r.status_code==201:diags.append(r.json())
record('web_history_list',a.get(WEB+'/api/v1/diagnoses',timeout=20),[200])
for d in diags:
    did=d['id']
    record('owner_detail_'+did,a.get(WEB+'/api/v1/diagnoses/'+did,timeout=20),[200])
    record('nonowner_detail_'+did,b.get(WEB+'/api/v1/diagnoses/'+did,timeout=20),[404,403])
    record('nonowner_export_'+did,b.get(WEB+'/diagnoses/'+did+'/metadata.json',timeout=20),[404,403])
    record('nonowner_delete_'+did,b.delete(WEB+'/api/v1/diagnoses/'+did,headers=csrf(b),timeout=20),[404,403])
    record('owner_export_metadata_'+did,a.get(WEB+'/diagnoses/'+did+'/metadata.json',timeout=20),[200])
    for kind in ['original','result']:
        r=record('owner_download_'+kind+'_'+did,a.get(WEB+'/diagnoses/'+did+'/download/'+kind,timeout=20),[200])
        if r.ok:(HERE/'runtime'/('download_'+did+'_'+kind+'.jpg')).write_bytes(r.content)

r=record('web_api_compare',upload(a,'/api/v1/comparisons'),[201]);comparison=r.json() if r.status_code==201 else None
if comparison:
    gid=comparison['comparisonGroupId']
    record('comparison_html',a.get(WEB+'/comparisons/'+gid,timeout=20),[200])
    record('comparison_metadata',a.get(WEB+'/comparisons/'+gid+'/metadata.json',timeout=20),[200])
    record('nonowner_comparison',b.get(WEB+'/api/v1/comparisons/'+gid,timeout=20),[404,403])
    record('nonowner_comparison_delete',b.delete(WEB+'/api/v1/comparisons/'+gid,headers=csrf(b),timeout=20),[404,403])
    record('owner_comparison_delete',a.delete(WEB+'/api/v1/comparisons/'+gid,headers=csrf(a),timeout=20),[204])
    record('comparison_after_delete',a.get(WEB+'/api/v1/comparisons/'+gid,timeout=20),[404])

record('reject_empty_web_image',a.post(WEB+'/api/v1/diagnoses',headers=csrf(a),data={'modelType':'YOLO26s-seg'},timeout=20),[400,422])
record('reject_invalid_web_image',a.post(WEB+'/api/v1/diagnoses',headers=csrf(a),data={'modelType':'YOLO26s-seg'},files={'image':('bad.jpg',b'bad jpeg','image/jpeg')},timeout=20),[400,415,422])
if diags:
    did=diags[-1]['id'];record('owner_delete_diagnosis',a.delete(WEB+'/api/v1/diagnoses/'+did,headers=csrf(a),timeout=20),[204]);record('diagnosis_after_delete',a.get(WEB+'/api/v1/diagnoses/'+did,timeout=20),[404])
(HERE/'runtime/created_records.json').write_text(json.dumps({'diagnoses':diags,'comparison':comparison},indent=2),encoding='utf-8')
print('COMPLETE',len(RESULTS),'cases; failures',sum(not r['pass'] for r in RESULTS),flush=True)
