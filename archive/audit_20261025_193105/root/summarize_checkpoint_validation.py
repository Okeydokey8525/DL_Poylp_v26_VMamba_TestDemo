"""Summarize resumed validation records, preserving the raw JSONL evidence."""
from pathlib import Path
import csv,hashlib,json,math,statistics,sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
comparison=[];actual_by_model={};summary={'complete':False,'models':{},'protocol_note':'rect=True, batch=16, CPU float32, patched research fork8.4.127. Original threads=4 field is requested setting; CPU select_device resets to8 (verified separately). Not a latency benchmark.'}
for model,parent,prefix in [('Baseline','YOLOv26s-seg','Kvasir_BG20_Baseline_YOLO26s_seg'),('TSVM','Kvasir_BG20_YOLO26s_seg_TSVM_FP32','Kvasir_BG20_YOLO26s_seg_TSVM_FP32')]:
    records=[json.loads(l) for l in (HERE/f'checkpoint_validation_rect16_{model}.jsonl').read_text().splitlines()]
    assert len(records)==len({r['seed'] for r in records}), 'duplicate validation record'
    by_seed={}
    for r in records:
        if 'error' in r:continue
        with (ROOT/'Ket_Qua_V2/KetQua_Nen'/parent/f'{prefix}_s{r["seed"]}_w2/results.csv').open(encoding='utf-8-sig') as f:raw=[{k.strip():float(v) for k,v in row.items()} for row in csv.DictReader(f)]
        expected=max(raw,key=lambda x:x['metrics/mAP50-95(B)']+x['metrics/mAP50-95(M)'])
        by_seed[r['seed']]=r['actual']
        for key,value in r['actual'].items():
            if key in expected:comparison.append({'model':model,'seed':r['seed'],'expected_fitness_epoch':int(expected['epoch']),'metric':key,'expected_csv':expected[key],'actual_checkpoint':value,'delta':value-expected[key],'checkpoint_sha256':r['checkpoint_sha256']})
    actual_by_model[model]=by_seed
    info={'records':len(records),'successful':len(by_seed),'errors':[r for r in records if 'error'in r],
          'AP_flags_over_0_005':[r['seed'] for r in records if r.get('mask_AP_difference_over_0_005')],'metrics':{}}
    for key in ['metrics/precision(B)','metrics/recall(B)','metrics/mAP50(B)','metrics/mAP50-95(B)','metrics/precision(M)','metrics/recall(M)','metrics/mAP50(M)','metrics/mAP50-95(M)']:
        sub=[r for r in comparison if r['model']==model and r['metric']==key]
        if sub:
            values=[r['actual_checkpoint'] for r in sub]
            info['metrics'][key]={'actual_mean':statistics.mean(values),'actual_sample_sd':statistics.stdev(values) if len(values)>1 else None,
                                  'max_abs_delta_to_csv':max(abs(r['delta']) for r in sub),'n_abs_delta_over_0_005':sum(abs(r['delta'])>.005 for r in sub)}
    summary['models'][model]=info
summary['complete']=all(x['successful']==20 for x in summary['models'].values())
if summary['complete']:
    delta=[actual_by_model['TSVM'][s]['metrics/mAP50-95(M)']-actual_by_model['Baseline'][s]['metrics/mAP50-95(M)'] for s in range(20)]
    mean=statistics.mean(delta);se=statistics.stdev(delta)/math.sqrt(20);t=mean/se;df=19
    c=math.exp(math.lgamma(10)-math.lgamma(9.5))/math.sqrt(df*math.pi);f=lambda x:c*(1+x*x/df)**(-10)
    n=20000;h=abs(t)/n;integ=h/3*(f(0)+f(abs(t))+sum((4 if i%2 else 2)*f(i*h) for i in range(1,n)))
    summary['secondary_checkpoint_comparison']={'delta_mask_AP':mean,'paired_t_p':1-2*integ,'CI95':[mean-2.093024054408263*se,mean+2.093024054408263*se],
                                              'note':'Secondary reproducibility check at best.pt; does not replace the original max-mask primary endpoint or an independent test set.'}
(HERE/'checkpoint_revalidation_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
if comparison:
    with (HERE/'checkpoint_all_metric_comparison.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=comparison[0]);w.writeheader();w.writerows(comparison)
mirror=HERE/'validation_dataset';original=ROOT/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20';checks=0;bad=[]
for kind in ['images','labels']:
    for p in (mirror/kind/'val').iterdir():
        if not p.is_file():continue
        q=original/kind/'val'/p.name;checks+=1
        if not q.exists() or hashlib.sha256(p.read_bytes()).digest()!=hashlib.sha256(q.read_bytes()).digest():bad.append(str(p))
(HERE/'validation_dataset_integrity.json').write_text(json.dumps({'checked':checks,'mismatches':bad},indent=2),encoding='utf-8')
print(json.dumps({'complete':summary['complete'],'counts':{k:v['successful'] for k,v in summary['models'].items()},'secondary':summary.get('secondary_checkpoint_comparison'),'mirror_checked':checks,'mirror_bad':len(bad)},indent=2))
