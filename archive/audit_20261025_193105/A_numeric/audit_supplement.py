from pathlib import Path
import sys,csv,json,math,collections,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,str(OUT/'packages'))
import numpy as np
from scipy import stats
def read(p):
 with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def raw(p):return [{k.strip():float(v) for k,v in r.items()} for r in read(p)]
def write(name,rs):
 fields=list(dict.fromkeys(k for r in rs for k in r))
 with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rs)
base=ROOT/'Ket_Qua_V2/KetQua_Nen';line=[];hist={};summ=[];group=collections.defaultdict(list)
for seed in range(20):
 old=raw(base/'Kvasir_BG20_YOLO26s_seg_TSVM'/f'Kvasir_BG20_YOLO26s_seg_TSVM_s{seed}_w2/results.csv')
 new=raw(base/'Kvasir_BG20_YOLO26s_seg_TSVM_FP32'/f'Kvasir_BG20_YOLO26s_seg_TSVM_FP32_s{seed}_w2/results.csv')
 for k in old[0]:line.append({'seed':seed,'column':k,'rows_compared':min(len(old),len(new)),'different_numeric_cells':sum(a[k]!=b[k] for a,b in zip(old,new)),'old_final':old[-1][k],'new_final':new[-1][k]})
 for model,parent,prefix in [('Baseline','YOLOv26s-seg','Kvasir_BG20_Baseline_YOLO26s_seg'),('TSVM','Kvasir_BG20_YOLO26s_seg_TSVM_FP32','Kvasir_BG20_YOLO26s_seg_TSVM_FP32')]:
  rr=raw(base/parent/f'{prefix}_s{seed}_w2/results.csv');hist[model,seed]=rr
  group[hashlib.sha256(json.dumps([{k:v for k,v in r.items() if k!='time'} for r in rr],sort_keys=True).encode()).hexdigest()].append((model,seed))
for rule in ['max_mask','max_fitness','final_epoch']:
 vals={}
 for (model,seed),rr in hist.items():
  sel=max(rr,key=lambda r:r['metrics/mAP50-95(M)']) if rule=='max_mask' else max(rr,key=lambda r:r['metrics/mAP50-95(M)']+r['metrics/mAP50-95(B)']) if rule=='max_fitness' else rr[-1]
  vals[model,seed]=sel['metrics/mAP50-95(M)']
 a=np.array([vals['Baseline',s] for s in range(20)]);b=np.array([vals['TSVM',s] for s in range(20)]);d=b-a
 ci=stats.t.interval(.95,19,loc=d.mean(),scale=stats.sem(d))
 summ.append({'rule':rule,'baseline_mean':a.mean(),'baseline_sd':a.std(ddof=1),'tsvm_mean':b.mean(),'tsvm_sd':b.std(ddof=1),'delta':d.mean(),'ci_low':ci[0],'ci_high':ci[1],'paired_t_p':stats.ttest_rel(b,a).pvalue,'tsvm_wins':int((d>0).sum()),'baseline_wins':int((d<0).sum())})
old21=[]
for model,parent,prefix in [('Baseline','YOLOv26s-seg','Kvasir_BG20_Baseline_YOLO26s_seg'),('TSVM','Kvasir_BG20_YOLO26s_seg_TSVM','Kvasir_BG20_YOLO26s_seg_TSVM')]:
 for seed in range(21):
  rr=raw(base/parent/f'{prefix}_s{seed}_w2/results.csv');r=max(rr,key=lambda r:r['metrics/mAP50-95(M)'])
  old21.append({'model':model,'seed':seed,'maxmask_epoch':r['epoch'],'mask_map50_95':r['metrics/mAP50-95(M)']})
a=np.array([r['mask_map50_95'] for r in old21 if r['model']=='Baseline']);b=np.array([r['mask_map50_95'] for r in old21 if r['model']=='TSVM'])
summary21={'n':21,'baseline_mean':a.mean(),'baseline_sd':a.std(ddof=1),'tsvm_mean':b.mean(),'tsvm_sd':b.std(ddof=1),'paired_t_p':stats.ttest_rel(b,a).pvalue,'note':'Historical unpatched TSVM; not interchangeable with 20seed_FP32. CSV arithmetic only.'}
facts=json.loads((ROOT/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/facts.json').read_text());pairs={}
for model in ['Baseline','TSVM']:
 ar=np.array([[r['metrics/mAP50-95(M)'] for r in hist[model,s]] for s in range(20)])
 pairs[model]=ar.max(axis=0)-ar.min(axis=0)  # legacy facts use min/max envelope, not SD band
expected={'n_seeds':20,'sign_test_p_mask_map50_95':stats.binomtest(13,20,.5).pvalue,'tsvm_wins_mask_map50_95':13,'baseline_wins_mask_map50_95':7,'band_narrower_epochs':int((pairs['TSVM']<pairs['Baseline']).sum()),'band_mean_width_change_pct':(pairs['TSVM'].mean()/pairs['Baseline'].mean()-1)*100,'cm_missing_cells':40}
sel=read(OUT/'independent_selected_metrics.csv')
for model,key in [('Baseline','baseline'),('TSVM','tsvm')]:
 ar=np.array([float(r['mask_map50_95']) for r in sel if r['model']==model])
 expected.update({f'median_{key}':np.median(ar),f'min_{key}':ar.min(),f'min_{key}_seed':int(ar.argmin()),f'max_{key}':ar.max(),f'max_{key}_seed':int(ar.argmax())})
fr=[{'field':k,'expected':v,'actual':facts[k],'matches':math.isclose(v,float(facts[k]),abs_tol=2e-11,rel_tol=2e-11)} for k,v in expected.items()]
write('lineage_numeric_columns_old_vs_fp32.csv',line);write('selection_sensitivity.csv',summ);write('historical_21seed_independent.csv',old21);write('facts_independent_validation.csv',fr)
(OUT/'supplement_summary.json').write_text(json.dumps({'numeric_lineage_total_cells':sum(r['rows_compared'] for r in line),'numeric_lineage_different_cells':sum(r['different_numeric_cells'] for r in line),'different_columns':sorted(set(r['column'] for r in line if r['different_numeric_cells'])),'duplicate_histories_within_current40':{h:v for h,v in group.items() if len(v)>1},'historical21':summary21,'selection_sensitivity':summ,'facts_matches':all(r['matches'] for r in fr)},indent=2,default=float),encoding='utf-8')
print(json.dumps({'lineage_columns_different':sorted(set(r['column'] for r in line if r['different_numeric_cells'])),'facts_matches':all(r['matches'] for r in fr),'sensitivity':summ,'historical21':summary21},indent=2,default=float))
