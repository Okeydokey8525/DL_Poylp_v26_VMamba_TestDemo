from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).parent/'packages'))
import numpy as np,pandas as pd,yaml
from scipy import stats
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1]; O=Path(__file__).parent
K=R/'Ket_Qua_V2'; S=K/'KQ_Nen_DX_20seed_FP32'
cols={'mask_map50_95':'metrics/mAP50-95(M)','mask_map50':'metrics/mAP50(M)','mask_precision':'metrics/precision(M)','mask_recall':'metrics/recall(M)','box_map50_95':'metrics/mAP50-95(B)','box_map50':'metrics/mAP50(B)','box_precision':'metrics/precision(B)','box_recall':'metrics/recall(B)','val_seg_loss':'val/seg_loss'}
rows=[]; checks=[]; configs=[]; curves={}; runs=[]
for m,d,prefix in [('Baseline','YOLOv26s-seg','Kvasir_BG20_Baseline_YOLO26s_seg'),('TSVM','Kvasir_BG20_YOLO26s_seg_TSVM_FP32','Kvasir_BG20_YOLO26s_seg_TSVM_FP32')]:
    curves[m]=[]
    for s in range(20):
        run=K/'KetQua_Nen'/d/f'{prefix}_s{s}_w2'; df=pd.read_csv(run/'results.csv');df.columns=df.columns.str.strip()
        assert len(df)==100 and df.select_dtypes('number').notna().all().all()
        best=df.loc[df[cols['mask_map50_95']].idxmax()]
        fitness=df[cols['mask_map50_95']]+df[cols['box_map50_95']]
        row={'model':m,'seed':s,'best_epoch':int(best.epoch),**{k:float(best[v]) for k,v in cols.items()},'run_path':str(run.relative_to(R))}
        rows.append(row);curves[m].append(df)
        conf=yaml.safe_load((run/'args.yaml').read_text()); configs.append({**conf,'experiment_model':m,'seed':s})
        ck=run/'weights/best.pt'
        checks.append({'model':m,'seed':s,'max_mask_epoch':int(best.epoch),'fitness_epoch':int(df.loc[fitness.idxmax(),'epoch']),'epochs':len(df),'best_pt_bytes':ck.stat().st_size if ck.exists() else None})
        for f in ['results.csv','args.yaml']:
            runs.append({'path':str((run/f).relative_to(R)),'sha256':hashlib.sha256((run/f).read_bytes()).hexdigest()})
raw=pd.DataFrame(rows); old=pd.read_csv(S/'raw_20seeds_extracted_metrics.csv')
for c in cols:
    assert np.allclose(raw[c],old[c],rtol=0,atol=1e-12),c
summary=[]
for k in [*cols,'best_epoch']:
    a=raw[raw.model=='Baseline'][k].to_numpy();b=raw[raw.model=='TSVM'][k].to_numpy();d=b-a
    ci=stats.t.interval(.95,19,loc=d.mean(),scale=stats.sem(d));p=stats.ttest_rel(b,a).pvalue
    summary.append({'metric':k,'baseline_mean':a.mean(),'baseline_sd':a.std(ddof=1),'tsvm_mean':b.mean(),'tsvm_sd':b.std(ddof=1),'delta':d.mean(),'ci_low':ci[0],'ci_high':ci[1],'p_ttest':p,'p_wilcoxon':stats.wilcoxon(b,a).pvalue,'levene_p':stats.levene(a,b).pvalue,'dz':d.mean()/d.std(ddof=1),'shapiro_delta_p':stats.shapiro(d).pvalue})
sm=pd.DataFrame(summary)
stored=pd.read_csv(S/'summary_20seeds_paired.csv').set_index('metric')
assert all(np.isclose(r['p_ttest'],stored.loc[r['metric'],'p_ttest']) for r in summary)
keys=['epochs','patience','batch','imgsz','workers','optimizer','lr0','lrf','weight_decay','warmup_epochs','deterministic','amp','cos_lr','close_mosaic','overlap_mask','mask_ratio','mosaic','fliplr','flipud','hsv_h','hsv_s','hsv_v','scale','translate','degrees','mixup','cutmix','copy_paste','rect','end2end','pretrained']
cfg={k:{m:sorted(set(str(c.get(k)) for c in configs if c['experiment_model']==m)) for m in ['Baseline','TSVM']} for k in keys}
ds=K/'Kvasir_YOLO_SEG_BG20';data={}; hashes={}
for split in ['train','val']:
    imgs=list((ds/'images'/split).glob('*')); labs=list((ds/'labels'/split).glob('*.txt'));nempty=0;nobj=0
    for l in labs:
        text=l.read_text().strip();nempty+=not bool(text)
        for line in text.splitlines():
            t=line.split();assert t[0]=='0' and len(t)>=7 and len(t)%2==1
            assert all(0<=float(x)<=1 for x in t[1:]);nobj+=1
    data[split]={'images':len(imgs),'labels':len(labs),'empty':nempty,'objects':nobj}
    hashes[split]={hashlib.sha256(p.read_bytes()).hexdigest() for p in imgs}
data['exact_duplicates_between_splits']=len(hashes['train']&hashes['val'])
report={'raw_summary_match':True,'runs':checks,'config_values':cfg,'data':data,'statistics':summary,'fitness_epoch_diff_count':sum(c['max_mask_epoch']!=c['fitness_epoch'] for c in checks),'cm_warning':'TN_reconstructed=40-FP is not a valid image-level true-negative count; exclude from analysis.'}
(O/'verified_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(O/'source_manifest.json').write_text(json.dumps(runs,indent=2),encoding='utf-8')
raw.to_csv(O/'verified_raw.csv',index=False);sm.to_csv(O/'verified_statistics.csv',index=False)
print('VERIFIED 40 runs ×100 epochs; raw CSV and paired statistics match.')
print('DATA',data);print('CONFIG',json.dumps(cfg,ensure_ascii=False));print('different max-mask/fitness epoch',report['fitness_epoch_diff_count'])
print(sm.to_string(index=False))
# Curves stay in a compact serialized form for report plots, without importing any model.
(O/'curves.json').write_text(json.dumps({m:[d.to_dict('list') for d in dfs] for m,dfs in curves.items()}),encoding='utf-8')
