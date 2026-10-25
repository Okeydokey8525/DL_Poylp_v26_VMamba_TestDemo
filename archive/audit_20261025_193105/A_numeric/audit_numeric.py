"""Independent read-only numerical audit; writes only alongside this script.

Run with the app venv; SciPy is isolated in ./packages. Does not import builders.
"""
from pathlib import Path
import sys, csv, json, hashlib, math, statistics, collections, platform

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(OUT / 'packages'))
import numpy as np
from scipy import stats
import scipy
import yaml

BASE = ROOT / 'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32'
RAW = ROOT / 'Ket_Qua_V2/KetQua_Nen'
METRICS = {
 'mask_map50_95':'metrics/mAP50-95(M)', 'mask_map50':'metrics/mAP50(M)',
 'mask_precision':'metrics/precision(M)', 'mask_recall':'metrics/recall(M)',
 'box_map50_95':'metrics/mAP50-95(B)', 'box_map50':'metrics/mAP50(B)',
 'box_precision':'metrics/precision(B)', 'box_recall':'metrics/recall(B)',
 'val_seg_loss':'val/seg_loss','val_box_loss':'val/box_loss',
 'val_cls_loss':'val/cls_loss','val_l1_loss':'val/l1_loss','val_sem_loss':'val/sem_loss'}
RUNS = {'Baseline':('YOLOv26s-seg','Kvasir_BG20_Baseline_YOLO26s_seg'),
        'TSVM':('Kvasir_BG20_YOLO26s_seg_TSVM_FP32','Kvasir_BG20_YOLO26s_seg_TSVM_FP32')}
coverage=[];issues=[];manifest=[];allrows={};selected={};epochs={};configs={};checks=[]

def rel(p):
 try:return str(Path(p).resolve().relative_to(ROOT)).replace('\\','/')
 except ValueError:return str(p)
def hashfile(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def readcsv(p):
 with Path(p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(name,rows):
 rows=list(rows)
 if not rows:return
 fields=list(dict.fromkeys(k for row in rows for k in row))
 with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def problem(p,row,col,expected,actual,severity='P1',cause='Confirmed mismatch',fix='Regenerate derived value from independently verified source'):
 issues.append(dict(file=rel(p),row=row,column=col,expected=expected,actual=actual,severity=severity,cause=cause,recommendation=fix))
def equal(a,b,tol=2e-11):
 if a is None or (isinstance(a,float) and math.isnan(a)):
  return b is None or str(b).strip().lower() in ('','nan','none','n/a')
 if isinstance(a,bool):return str(a).lower()==str(b).lower()
 if isinstance(a,(int,float,np.number)):
  try:return math.isclose(float(a),float(b),abs_tol=tol,rel_tol=tol)
  except (ValueError,TypeError):return False
 return str(a)==str(b)
def compare(p,rs,expected,keycols,columns=None,scope='derived numeric table'):
 em={tuple(str(r[k]) for k in keycols):r for r in expected};seen=set();nc=0;nb=0
 for lineno,row in enumerate(rs,2):
  key=tuple(str(row[k]) for k in keycols)
  if key in seen:problem(p,lineno,'key','unique',key);nb+=1
  seen.add(key)
  if key not in em:problem(p,lineno,'key','known source key',key);nb+=1;continue
  ex=em[key]
  for c in columns or list(ex):
   if c not in row or c in keycols:continue
   nc+=1
   if not equal(ex[c],row[c]):problem(p,lineno,c,ex[c],row[c]);nb+=1
 missing=set(em)-seen
 for key in missing:problem(p,'missing','key',key,'missing');nb+=1
 coverage.append(dict(file=rel(p),rows=len(rs),checked_cells=nc,status='FAIL' if nb else 'PASS',scope=scope,note=f'missing keys={len(missing)}; schema intersection tested'))

for model,(folder,prefix) in RUNS.items():
 for seed in range(20):
  run=RAW/folder/f'{prefix}_s{seed}_w2'
  p=run/'results.csv';rs=readcsv(p)
  rows=[{k.strip():float(v) for k,v in r.items()} for r in rs]
  allrows[model,seed]=rows
  schema=list(rows[0]);finite=all(math.isfinite(v) for r in rows for v in r.values())
  continuous=[r['epoch'] for r in rows]==list(range(1,101))
  metric_bounds=all(0<=r[v]<=1 for r in rows for k,v in METRICS.items() if k.startswith(('mask_','box_')))
  loss_nonnegative=all(r[k]>=0 for r in rows for k in schema if k.endswith('_loss'))
  cfg=yaml.safe_load((run/'args.yaml').read_text(encoding='utf-8'));configs[model,seed]=cfg
  best=max(rows,key=lambda r:r[METRICS['mask_map50_95']])
  bf=max(rows,key=lambda r:r[METRICS['mask_map50_95']]+r[METRICS['box_map50_95']])
  selected[model,seed]={'model':model,'seed':seed,'best_epoch':int(best['epoch']),'total_epochs':len(rows),'run_path':str(run.relative_to(ROOT)),**{k:best[v] for k,v in METRICS.items()},**{k.replace('/','_'):v for k,v in best.items() if k.startswith('train/')}}
  epochs[model,seed]={'model':model,'seed':seed,'max_mask_epoch':int(best['epoch']),'sum_box_mask_fitness_epoch':int(bf['epoch']),'different':int(best['epoch'])!=int(bf['epoch'])}
  ok=finite and continuous and metric_bounds and loss_nonnegative and cfg['seed']==seed
  checks.append({'model':model,'seed':seed,'epochs':len(rows),'finite_numeric':finite,'run_path':str(run.relative_to(ROOT))})
  coverage.append(dict(file=rel(p),rows=len(rows),checked_cells=len(rows)*len(schema),status='PASS' if ok else 'FAIL',scope='raw schema/epoch/finite/bounds',note=json.dumps({'columns':schema,'continuous':continuous,'metric_bounds':metric_bounds,'loss_nonnegative':loss_nonnegative,'args_seed':cfg['seed']})))
  if not ok:problem(p,'all','raw_checks','all pass',ok)
  for x in [run/'results.csv',run/'args.yaml',run/'weights/best.pt',run/'weights/last.pt',run/'confusion_matrix.png',run/'confusion_matrix_normalized.png']:
   manifest.append({'path':rel(x),'exists':x.exists(),'bytes':x.stat().st_size if x.exists() else None,'sha256':hashfile(x) if x.exists() else None,'model':model,'seed':seed})
print('Raw 40 runs read and manifested',flush=True)
writecsv('source_manifest.csv',manifest);writecsv('independent_selected_metrics.csv',selected.values());writecsv('independent_epoch_selection.csv',epochs.values())

# Cross-run configuration equality, expected identity/model/path differences listed.
configdiff=[];reference=configs['Baseline',0]
for (model,seed),cfg in configs.items():
 for k in sorted(set(reference)|set(cfg)):
  if reference.get(k)!=cfg.get(k):
   configdiff.append({'model':model,'seed':seed,'key':k,'baseline_s0':repr(reference.get(k)),'actual':repr(cfg.get(k)),'expected_identity_difference':k in ['seed','model','name','save_dir','pretrained']})
writecsv('configuration_differences.csv',configdiff)
unexpected=[r for r in configdiff if not r['expected_identity_difference']]
for r in unexpected:problem('args.yaml',f"{r['model']} seed {r['seed']}",r['key'],r['baseline_s0'],r['actual'],cause='Configuration difference; impact requires interpretation')

# Independent statistics; all selected metrics plus best_epoch for legacy table.
summaries={};ranges=[];paired=[];wins=[]
for metric in [*METRICS,'best_epoch']:
 a=np.array([selected['Baseline',s][metric] for s in range(20)],float)
 b=np.array([selected['TSVM',s][metric] for s in range(20)],float);d=b-a
 lower=metric.startswith('val_');direction=-1 if lower else 1
 nw=int(np.count_nonzero(d*direction>0));nl=int(np.count_nonzero(d*direction<0));nt=20-nw-nl
 varying=np.std(d,ddof=1)>0
 ci=stats.t.interval(.95,19,loc=float(np.mean(d)),scale=float(stats.sem(d))) if varying else [None,None]
 sm={'metric':metric,'better':'lower' if lower else 'higher','n_pairs':20,
 'baseline_mean':float(np.mean(a)),'baseline_sd':float(np.std(a,ddof=1)),'tsvm_mean':float(np.mean(b)),'tsvm_sd':float(np.std(b,ddof=1)),
 'delta_tsvm_minus_baseline':float(np.mean(d)),'relative_delta_pct':float(np.mean(d)/np.mean(a)*100) if np.mean(a)!=0 else None,
 'delta_ci95_low':ci[0],'delta_ci95_high':ci[1],
 'paired_t_p':float(stats.ttest_rel(b,a).pvalue) if varying else None,
 'wilcoxon_two_sided_p':float(stats.wilcoxon(b,a,alternative='two-sided').pvalue) if varying else None,
 'cohen_dz':float(np.mean(d)/np.std(d,ddof=1)) if varying else None,
 'shapiro_delta_p':float(stats.shapiro(d).pvalue) if varying else None,
 'levene_median_p':float(stats.levene(a,b,center='median').pvalue) if np.std(a)+np.std(b)>0 else None,
 'tsvm_wins':nw,'baseline_wins':nl,'ties':nt,
 'sign_test_p':float(stats.binomtest(nw,nw+nl,.5,alternative='two-sided').pvalue) if nw+nl else None}
 summaries[metric]=sm
 wins.append({'metric':metric,'tsvm_wins':nw,'baseline_wins':nl,'ties':nt,'lower_is_better':lower})
 for model,x in [('Baseline',a),('TSVM',b)]:
  ranges.append({'metric':metric,'model':model,'min':float(min(x)),'min_seed':int(np.argmin(x)),'max':float(max(x)),'max_seed':int(np.argmax(x)),'median':float(np.median(x)),'range':float(np.ptp(x)),'q25':float(np.percentile(x,25)),'q75':float(np.percentile(x,75))})
 for seed,(aa,bb,dd) in enumerate(zip(a,b,d)):paired.append({'metric':metric,'seed':seed,'baseline':aa,'tsvm_fp32':bb,'delta':dd})
writecsv('independent_summary.csv',summaries.values());writecsv('independent_extrema.csv',ranges);writecsv('independent_seed_deltas.csv',paired)

cm_source=readcsv(BASE/'raw_20seeds_confusion_matrices.csv');cm=[]
for r in cm_source:
 tp,fp,fn=(int(r[k]) for k in ['TP','FP','FN'])
 cm.append({'model':r['model'],'seed':int(r['seed']),'TP':tp,'FP':fp,'FN':fn,'ground_truth_objects':127,'object_recall_at_cm_threshold':tp/(tp+fn),'object_precision_at_cm_threshold':tp/(tp+fp)})
 if tp+fn!=127 or r['TN']!='':problem(BASE/'raw_20seeds_confusion_matrices.csv',r['seed'],'counts','TP+FN127 TNblank',r)

# Every CSV dispatched by schema, independent of pre-existing builder.
for p in sorted(BASE.rglob('*.csv')):
 rs=readcsv(p);fields=list(rs[0]) if rs else [];name=p.name
 if name in ['baseline_timings.csv','tsvm_timings.csv','efficiency_raw_benchmark.csv','efficiency_summary.csv','accuracy_efficiency_summary.csv']:continue
 if 'baseline_mean' in fields:
  expected=[]
  for metric,sm in summaries.items():
   ex=dict(sm)
   ex.update({'delta':sm['delta_tsvm_minus_baseline'],'p_ttest':sm['paired_t_p'],'p_wilcoxon':sm['wilcoxon_two_sided_p'],'levene_p':sm['levene_median_p']})
   expected.append(ex)
  exp=[r for r in expected if r['metric'] in {x['metric'] for x in rs}]
  # Legacy root table defines wins by positive difference even for loss; flag semantic ambiguity separately.
  if name=='summary_20seeds_paired.csv':
   for ex in exp:
    if ex['metric'].startswith('val_'):ex['tsvm_wins'],ex['baseline_wins']=ex['baseline_wins'],ex['tsvm_wins']
  compare(p,rs,exp,['metric'])
 elif 'best_epoch' in fields:
  exp=[]
  for x in selected.values():
   ex=dict(x)
   if name=='raw_20seeds_extracted_metrics.csv' and p.parent==BASE:pass
   exp.append(ex)
  compare(p,rs,exp,['model','seed'],[k for k in fields if k!='run_path'])
  for lineno,row in enumerate(rs,2):
   actual=Path(row['run_path']);actual=actual if actual.is_absolute() else ROOT/actual
   expected=ROOT/selected[row['model'],int(row['seed'])]['run_path']
   if actual.resolve()!=expected.resolve():problem(p,lineno,'run_path',rel(expected),row['run_path'])
 elif 'max_mask_epoch' in fields:compare(p,rs,list(epochs.values()),['model','seed'])
 elif 'experiment_model' in fields:
  exp=[{'experiment_model':m,'seed':s,**cfg} for (m,s),cfg in configs.items()]
  # cfg seed overrides same numeric value intentionally.
  compare(p,rs,exp,['experiment_model','seed'],[x for x in fields if x not in ['experiment_model','seed']])
 elif 'finite_numeric' in fields:compare(p,rs,checks,['model','seed'],[k for k in fields if k!='run_path'])
 elif 'min_seed' in fields:compare(p,rs,[x for x in ranges if x['metric'] in METRICS],['metric','model'])
 elif 'tsvm_fp32' in fields:compare(p,rs,[x for x in paired if x['metric'] in METRICS],['metric','seed'])
 elif 'lower_is_better' in fields:compare(p,rs,[x for x in wins if x['metric'] in METRICS],['metric'])
 elif name=='per_epoch_mean_sd.csv':
  exp=[]
  for row in rs:
   model,metric,ep=row['model'],row['metric'],int(row['epoch'])
   vals=np.array([allrows[model,s][ep-1][metric] for s in range(20)])
   exp.append({'model':model,'metric':metric,'epoch':ep,'mean':float(vals.mean()),'sd':float(vals.std(ddof=1))})
  compare(p,rs,exp,['model','metric','epoch'])
 elif 'TP' in fields:
  exp=[x for x in cm if x['model'] in {r['model'] for r in rs}]
  compare(p,rs,exp,['model','seed'],scope='arithmetic against inherited CM extraction; NOT verification against raw images/checkpoints')
 elif 'TP_mean' in fields:
  exp=[]
  for model in RUNS:
   vals=[x for x in cm if x['model']==model];ex={'model':model}
   for k in ['TP','FP','FN','object_recall_at_cm_threshold','object_precision_at_cm_threshold']:
    ar=np.array([v[k] for v in vals]);ex[k+'_mean']=ar.mean();ex[k+'_std']=ar.std(ddof=1)
   exp.append(ex)
  compare(p,rs,exp,['model'],scope='CM summary arithmetic only; source image verification delegated B_visual')
 elif 'TP_pct_of_ground_truth_objects' in fields:
  model='Baseline' if name.startswith('baseline') else 'TSVM'
  exp=[{'seed':r['seed'],'TP_pct_of_ground_truth_objects':r['TP']/127*100,'FN_pct_of_ground_truth_objects':r['FN']/127*100,'FP_pct':None,'TN_pct':None} for r in cm if r['model']==model]
  compare(p,rs,exp,['seed'])
 elif 'predicted' in fields:
  model='Baseline' if name.startswith('baseline') else 'TSVM';vals=[x for x in cm if x['model']==model]
  mtp=np.mean([x['TP'] for x in vals]);mfp=np.mean([x['FP'] for x in vals]);mfn=np.mean([x['FN'] for x in vals])
  exp=[{'predicted':'polyp','true_polyp':mtp,'true_background':mfp,'true_polyp_pct':mtp/127*100,'true_background_pct':None},
       {'predicted':'background','true_polyp':mfn,'true_background':None,'true_polyp_pct':mfn/127*100,'true_background_pct':None}]
  compare(p,rs,exp,['predicted'])
 else:coverage.append(dict(file=rel(p),rows=len(rs),checked_cells=0,status='NOT_CHECKED',scope='unrecognized schema',note=str(fields)))

# Existing manifest: verify hashes but do not accept its PASS claims as evidence.
existing=json.loads((BASE/'07_audit/source_manifest.json').read_text(encoding='utf-8'))
mh=[]
for item in existing['inputs']:
 p=ROOT/item['path'];actual=hashfile(p) if p.exists() else None
 ok=actual==item['sha256'];mh.append({'path':rel(p),'expected':item['sha256'],'actual':actual,'match':ok})
 if not ok:problem(p,'file','sha256',item['sha256'],actual)
writecsv('existing_manifest_recheck.csv',mh)

# Identity/lineage across archived old 10/21-seed runs.
lineage=[]
for (model,seed),rec in selected.items():
 current=ROOT/rec['run_path'];others=[]
 if model=='TSVM':others.append(RAW/'Kvasir_BG20_YOLO26s_seg_TSVM'/f'Kvasir_BG20_YOLO26s_seg_TSVM_s{seed}_w2')
 for other in others:
  for fname in ['results.csv','args.yaml','weights/best.pt','confusion_matrix.png']:
   p,q=current/fname,other/fname
   lineage.append({'model':model,'seed':seed,'artifact':fname,'current':rel(p),'historical':rel(q),'current_exists':p.exists(),'historical_exists':q.exists(),'same_sha256':hashfile(p)==hashfile(q) if p.exists() and q.exists() else None,'interpretation':'Byte equality supports shared artifact lineage, not proof of misconduct; inequality does not independently establish retraining.'})
oldpath=ROOT/'Ket_Qua_V2/KQ_Nen_DX_10seed/01_raw_analysis/raw_10seeds_extracted_metrics.csv'
old10=readcsv(oldpath);old_comp=[]
for r in old10:
 if r['model'] not in RUNS:continue
 model,seed=r['model'],int(r['seed']);oldrun=Path(r['run_path'])
 with (oldrun/'results.csv').open(encoding='utf-8-sig') as f:rr=[{k.strip():float(v) for k,v in x.items()} for x in csv.DictReader(f)]
 best=max(rr,key=lambda x:x[METRICS['mask_map50_95']])
 for k,col in METRICS.items():
  if k in r:old_comp.append({'model':model,'seed':seed,'metric':k,'old_10seed':float(r[k]),'old_raw_recalculated':best[col],'old_matches_raw':equal(best[col],r[k]),'new_20seed_fp32':selected[model,seed][k],'equal_old_and_new':equal(selected[model,seed][k],r[k]),'old_run':rel(oldrun)})
writecsv('lineage_old_vs_fp32.csv',lineage);writecsv('old10_vs_20_metric_lineage.csv',old_comp)

# Benchmark arithmetic, source timing integrity and environment-derived fields.
bench=BASE/'efficiency_benchmark';br=[]
for key in ['baseline','tsvm']:
 env=json.loads((bench/'raw'/f'{key}_environment.json').read_text(encoding='utf-8'))
 times=readcsv(bench/'raw'/f'{key}_timings.csv');br+=times
 for mode in ['forward_only','predict_pipeline']:
  rows=[r for r in times if r['mode']==mode];v=np.array([float(r['latency_ms']) for r in rows])
  ex={'model':env['model'],'mode':mode,'n':len(v),'mean_ms':v.mean(),'sd_ms':v.std(ddof=1),'p50_ms':np.percentile(v,50),'p95_ms':np.percentile(v,95),'p99_ms':np.percentile(v,99),'min_ms':v.min(),'max_ms':v.max(),'serial_images_per_second':1000/v.mean(),
  'parameters_unfused':env['parameters_unfused'],'params_M':env['parameters_unfused']/1e6,'checkpoint_MiB':env['checkpoint_bytes']/2**20,
  'fp32_parameter_MiB_unfused':env['fp32_parameter_bytes_unfused']/2**20,'sampled_process_RSS_MiB':env['rss_process_sample_max_bytes']/2**20,'sampled_process_RSS_delta_MiB':env['rss_delta_sample_max_bytes']/2**20,'GFLOPs':None,'VRAM_MiB':None}
  if mode=='predict_pipeline':
   for col in ['preprocess','inference','postprocess']:ex['mean_'+col+'_ms']=np.mean([float(r[col+'_ms']) for r in rows])
   ex['mean_unattributed_pipeline_overhead_ms']=ex['mean_ms']-sum(ex['mean_'+col+'_ms'] for col in ['preprocess','inference','postprocess'])
   ex['iterations_with_detections']=sum(float(r['detections'])>0 for r in rows)
   model='Baseline' if key=='baseline' else 'TSVM';ex['mask_map50_95_20seed_mean']=summaries['mask_map50_95']['baseline_mean' if key=='baseline' else 'tsvm_mean'];ex['mask_map50_95_20seed_sd']=summaries['mask_map50_95']['baseline_sd' if key=='baseline' else 'tsvm_sd']
  summaries.setdefault('_benchmark',[]).append(ex)
  if len(v)!=100 or not np.isfinite(v).all() or not (v>0).all():problem(bench/'raw'/f'{key}_timings.csv',mode,'timings','100 finite positive',str(v))
 for field in ['checkpoint','custom_module_path']:
  if field in env:
   p=Path(env[field]);target=env['sha256'] if field=='checkpoint' else env['custom_module_sha256'];actual=hashfile(p) if p.exists() else None
   if not actual or actual.lower()!=target.lower():problem(bench/'raw'/f'{key}_environment.json',field,'sha256',target,actual)
for name in ['efficiency_summary.csv','accuracy_efficiency_summary.csv']:
 p=bench/'tables'/name;rs=readcsv(p);exp=[x for x in summaries['_benchmark'] if name=='efficiency_summary.csv' or x['mode']=='predict_pipeline']
 compare(p,rs,exp,['model','mode'],scope='benchmark arithmetic from stored timings; metadata identity checked, not replay of historic clock')
p=bench/'raw/efficiency_raw_benchmark.csv';compare(p,readcsv(p),br,['model','mode','iteration'],scope='merged timings equality')
for key in ['baseline','tsvm']:
 p=bench/'raw'/f'{key}_timings.csv';rs=readcsv(p)
 coverage.append(dict(file=rel(p),rows=len(rs),checked_cells=len(rs),status='PASS',scope='latency finite/positive and each mode 100',note='Timing authenticity not inferable from CSV alone; no rebenchmark performed'))
writecsv('benchmark_independent_summary.csv',summaries.pop('_benchmark'))

# Source ambiguities in intentionally retained legacy artifacts.
problem(BASE/'facts.json','cm_mean','TN_reconstructed','N/A: object FP does not determine image TN','23.55 baseline; 24.25 TSVM','P2','Confirmed invalid image-level interpretation retained in legacy artifact; main 04_confusion_matrix excludes it','Quarantine/deprecate this field; retain source bytes for traceability and prevent downstream reuse')
problem(BASE/'raw_20seeds_confusion_matrices.csv','all 40','TN_reconstructed','N/A for image-level TN','40 minus object FP','P2','Confirmed formula exists; arithmetic valid but inference invalid','Keep original archived; do not cite as measured TN or specificity')
problem(BASE/'summary_20seeds_paired.csv','val_seg_loss','tsvm_wins','14 when lower loss is better','6 (counts higher loss)','P2','Confirmed legacy win direction differs from new lower_is_better schema','Label legacy higher/lower counts or use new canonical win-loss table')

writecsv('coverage.csv',coverage);writecsv('discrepancies.csv',issues)
(OUT/'environment.json').write_text(json.dumps({'python':sys.executable,'python_version':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'tolerance':'abs and rel 2e-11 for stored floating calculations; exact selected rows from raw decimal values','read_only_source':True},indent=2),encoding='utf-8')
(OUT/'audit_state.json').write_text(json.dumps({'summary':summaries,'manifest_count':len(manifest),'existing_manifest_checked':len(mh),'issues':issues,'config_unexpected_differences':unexpected,'epoch_rule_differences':sum(x['different'] for x in epochs.values()),'coverage_files':len(coverage)},indent=2,default=lambda v:float(v)),encoding='utf-8')
print('DONE:',len(coverage),'coverage rows;',len(issues),'issues;',sum(x['different'] for x in epochs.values()),'different epoch rules',flush=True)
