from pathlib import Path
import argparse,hashlib,json
import requests
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];WEB='http://127.0.0.1:18080'
credentials=json.loads((HERE/'runtime/test_credentials.json').read_text())
parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['before','after_restart','ai_off']);args=parser.parse_args()
records=[];session=requests.Session()
def csrf():
 v=session.get(WEB+'/api/v1/auth/csrf',timeout=20).json();return {v['headerName']:v['token']}
def rec(name,r,expected):
 d={'stage':args.stage,'case':name,'status':r.status_code,'expected_status':expected,'pass':r.status_code in expected,'requestId':r.headers.get('X-Request-Id')}
 if 'json' in r.headers.get('Content-Type',''):
  try:d['json']=r.json()
  except ValueError:pass
 records.append(d);print(name,d['status'],d['pass'],flush=True);return r
rec('login',session.post(WEB+'/api/v1/auth/login',headers=csrf(),json={'email':credentials['email'],'password':credentials['password']},timeout=20),[200])
created=json.loads((HERE/'runtime/created_records.json').read_text());did=created['diagnoses'][0]['id']
if args.stage=='before':
 rec('comparison_history_html',session.get(WEB+'/comparisons',timeout=20),[200])
 rec('comparison_history_api',session.get(WEB+'/api/v1/comparisons',timeout=20),[200])
 rec('single_history_html',session.get(WEB+'/history',timeout=20),[200])
 rec('dashboard',session.get(WEB+'/dashboard',timeout=20),[200])
 rec('correct_multipart_empty',session.post(WEB+'/api/v1/diagnoses',headers=csrf(),data={'modelType':'YOLO26s-seg'},files={'image':('empty.jpg',b'','image/jpeg')},timeout=20),[400])
 rec('unknown_web_model',session.post(WEB+'/api/v1/diagnoses',headers=csrf(),data={'modelType':'invalid'},files={'image':('empty.jpg',b'x','image/jpeg')},timeout=20),[400])
 rec('delete_without_csrf',session.delete(WEB+'/api/v1/diagnoses/'+did,timeout=20),[403])
 r=rec('original_before_restart',session.get(WEB+'/diagnoses/'+did+'/download/original',timeout=20),[200])
 (HERE/'runtime/persistence_before.json').write_text(json.dumps({'id':did,'image_sha256':hashlib.sha256(r.content).hexdigest()}))
elif args.stage=='after_restart':
 rec('record_survives_web_restart',session.get(WEB+'/api/v1/diagnoses/'+did,timeout=20),[200])
 r=rec('original_survives_web_restart',session.get(WEB+'/diagnoses/'+did+'/download/original',timeout=20),[200])
 old=json.loads((HERE/'runtime/persistence_before.json').read_text())
 records.append({'stage':args.stage,'case':'stored_image_bytes_preserved','pass':hashlib.sha256(r.content).hexdigest()==old['image_sha256']})
elif args.stage=='ai_off':
 before=session.get(WEB+'/api/v1/diagnoses',timeout=20).json()
 p=ROOT/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/images/val/cju0s690hkp960855tjuaqvv0.jpg'
 with p.open('rb') as f:r=session.post(WEB+'/api/v1/diagnoses',headers=csrf(),data={'modelType':'YOLO26s-seg'},files={'image':(p.name,f,'image/jpeg')},timeout=30)
 rec('ai_off_no_false_success',r,[503,504])
 after=session.get(WEB+'/api/v1/diagnoses',timeout=20).json()
 records.append({'stage':args.stage,'case':'failed_inference_does_not_create_history','pass':before==after,'before':before,'after':after})
(HERE/f'runtime_http_{args.stage}.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
