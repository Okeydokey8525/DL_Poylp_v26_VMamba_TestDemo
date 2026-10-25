from pathlib import Path
import sys,json,csv,re,statistics
import numpy as np
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8');O=Path(__file__).resolve().parent;R=O.parents[1];P=R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32'
rs=json.loads((O/'inventory.json').read_text(encoding='utf-8'));by={r['id']:r for r in rs};ocr=json.loads((O/'ocr_results.json').read_text());more=json.loads((O/'more_ocr_results.json').read_text())
lookup={(x['id'],x['type']):x for x in ocr};lookup.update({(x['id'],x['type']):x for x in more})
cms={(x['model'],int(x['seed'])):x for x in csv.DictReader((P/'raw_20seeds_confusion_matrices.csv').open(encoding='utf-8-sig'))};checks=[];curve_checks=[];curves={}
def number(text):
 m=re.search(r'\d+(?:\.\d+)?',text);return float(m.group()) if m else None
for row in rs:
 if row['group']!='raw':continue
 p=R/row['path'];name=p.name;m=row['model'];s=int(row['seed']);ref=cms[m,s]
 if name.startswith('confusion_matrix'):
  for cell in ['TP','FP','FN','TN']:
   got=number(lookup.get((row['id'],cell),{}).get('text',''))
   expected=(float(ref[cell]) if ref.get(cell) else None) if name=='confusion_matrix.png' else {'TP':float(ref['TP'])/127,'FN':float(ref['FN'])/127,'FP':1.,'TN':None}[cell]
   status='PASS_BLANK' if expected is None and got is None else 'PASS' if expected is not None and got is not None and abs(got-expected)<(.0051 if 'normalized' in name else .01) else 'UNRESOLVED'
   checks.append(dict(id=row['id'],model=m,seed=s,kind=name,cell=cell,expected=expected,observed=got,status=status))
  continue
 a=np.asarray(Image.open(p).convert('RGB'));h,w=a.shape[:2];black=a[:,:int(w*.7),:].max(2)<80
 yidx=np.flatnonzero(black.sum(1)>w*.45);xidx=np.flatnonzero(black.sum(0)>h*.65)
 if len(yidx)<2 or len(xidx)<2:
  curve_checks.append(dict(id=row['id'],model=m,seed=s,file=name,status='AXIS_NOT_DETECTED'));continue
 top,bottom=int(yidx.min()+1),int(yidx.max()-1);left,right=int(xidx.min()+1),int(xidx.max()-1)
 b=a[top:bottom+1,left:right+1];blue=(b[:,:,0]<100)&(b[:,:,1]<100)&(b[:,:,2]>180)
 xx=[];yy=[]
 for x in range(blue.shape[1]):
  ys=np.flatnonzero(blue[:,x])
  if len(ys):xx.append(x);yy.append(float(np.median(ys)))
 if len(xx)<100:
  curve_checks.append(dict(id=row['id'],model=m,seed=s,file=name,status='CURVE_NOT_DETECTED'));continue
 x=np.arange(blue.shape[1]);vals=1-np.interp(x,xx,yy)/(bottom-top);curves[m,s,name]=vals.tolist()
 record=dict(id=row['id'],model=m,seed=s,file=name,status='DIGITIZED',axis_bbox=f'{left},{top},{right},{bottom}',detected_columns=len(xx),total_columns=len(x),minimum=float(vals.min()),maximum=float(vals.max()))
 if name.endswith('PR_curve.png'):
  legend=number(lookup.get((row['id'],'legend'),{}).get('text',''));area=float(np.trapezoid(vals,x/(len(x)-1)));record.update(legend_ap50=legend,pixel_integral=area,area_minus_legend=area-legend if legend else None)
  with (p.parent/'results.csv').open(encoding='utf-8-sig') as f:history=[{k.strip():float(v) for k,v in q.items()} for q in csv.DictReader(f)]
  fit=max(history,key=lambda q:q['metrics/mAP50-95(M)']+q['metrics/mAP50-95(B)']);col='metrics/mAP50(B)' if name.startswith('Box') else 'metrics/mAP50(M)'
  record.update(fitness_epoch=int(fit['epoch']),fitness_log_ap50=fit[col],legend_minus_log=legend-fit[col] if legend else None)
 curve_checks.append(record)
f1=[]
for m in ['Baseline','TSVM']:
 for s in range(20):
  for kind in ['Box','Mask']:
   try:
    pv=np.array(curves[m,s,kind+'P_curve.png']);rv=np.array(curves[m,s,kind+'R_curve.png']);fv=np.array(curves[m,s,kind+'F1_curve.png'])
    grid=np.linspace(.02,.98,600);pv=np.interp(grid,np.linspace(0,1,len(pv)),pv);rv=np.interp(grid,np.linspace(0,1,len(rv)),rv);fv=np.interp(grid,np.linspace(0,1,len(fv)),fv)
    err=np.abs(fv-2*pv*rv/(pv+rv+1e-12));f1.append(dict(model=m,seed=s,kind=kind,mean_abs_error=float(err.mean()),max_abs_error=float(err.max()),note='smoothed plotted curves; approximate digitization, not raw PR arrays'))
   except KeyError:pass
for name,rows in [('cm_ocr_comparison.csv',checks),('raw_curve_digitization.csv',curve_checks),('f1_pixel_consistency.csv',f1)]:
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (O/name).open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
print('CM statuses',{s:sum(r['status']==s for r in checks) for s in set(r['status'] for r in checks)})
print('CM unresolved',[r for r in checks if r['status']=='UNRESOLVED'])
pr=[r for r in curve_checks if 'legend_minus_log' in r];print('PR',len(pr),'max legend-log',max(abs(r['legend_minus_log']) for r in pr),'max area-legend',max(abs(r['area_minus_legend']) for r in pr))
print('PR delta>0.005',[r for r in pr if abs(r['legend_minus_log'])>.005])
print('Pixel F1',len(f1),'max MAE',max(x['mean_abs_error'] for x in f1),'max point error',max(x['max_abs_error'] for x in f1))
