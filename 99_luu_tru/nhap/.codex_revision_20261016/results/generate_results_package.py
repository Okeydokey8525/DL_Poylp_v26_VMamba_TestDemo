"""Rebuild the 20-seed FP32 analysis without training or model inference.

Inputs are retained unchanged. All derived data is regenerated from 40 results.csv.
Confusion counts are inherited from the supplied extraction, explicitly distinguished
from metric CSVs and never converted into image-level TN or specificity.
"""
from pathlib import Path
import sys, json, hashlib, shutil
import numpy as np
import pandas as pd
import yaml
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32'
MODELS=['Baseline','TSVM']; NAMES=['YOLO26s-seg','TSVM FP32']; COLORS=['#286594','#de792a']
COLS={'mask_map50_95':'metrics/mAP50-95(M)','mask_map50':'metrics/mAP50(M)',
      'mask_precision':'metrics/precision(M)','mask_recall':'metrics/recall(M)',
      'box_map50_95':'metrics/mAP50-95(B)','box_map50':'metrics/mAP50(B)',
      'box_precision':'metrics/precision(B)','box_recall':'metrics/recall(B)',
      'val_seg_loss':'val/seg_loss','val_box_loss':'val/box_loss','val_cls_loss':'val/cls_loss','val_l1_loss':'val/l1_loss','val_sem_loss':'val/sem_loss'}
LABELS={'mask_map50_95':'Mask mAP50–95','mask_map50':'Mask mAP50','mask_precision':'Mask precision',
        'mask_recall':'Mask recall','box_map50_95':'Box mAP50–95','box_map50':'Box mAP50',
        'box_precision':'Box precision','box_recall':'Box recall','val_seg_loss':'Val segmentation loss',
        'val_box_loss':'Val box loss','val_cls_loss':'Val class loss','val_l1_loss':'Val L1 loss','val_sem_loss':'Val semantic loss'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
 'axes.spines.right':False,'axes.grid':True,'grid.alpha':.18,'savefig.dpi':300})
FIGURES=[]; MANIFEST=[]
def write_text(path,text):
    p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def csv(frame,path):
    p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);frame.to_csv(p,index=False,encoding='utf-8-sig')
def manifest(path,role):
    MANIFEST.append({'path':str(path.relative_to(ROOT)),'role':role,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size})
def save(fig,path,description):
    p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);fig.tight_layout();fig.savefig(p,bbox_inches='tight',facecolor='white');plt.close(fig)
    FIGURES.append({'path':path,'description':description})
def chart(title,size=(8,4)):
    f,a=plt.subplots(figsize=size);a.set_title(title,pad=12);return f,a

rows=[];epochs=[];curves={m:[] for m in MODELS};audit=[];configs=[]
for m in MODELS:
    for seed in range(20):
        name=f'Kvasir_BG20_Baseline_YOLO26s_seg_s{seed}_w2' if m=='Baseline' else f'Kvasir_BG20_YOLO26s_seg_TSVM_FP32_s{seed}_w2'
        parent='YOLOv26s-seg' if m=='Baseline' else 'Kvasir_BG20_YOLO26s_seg_TSVM_FP32'
        run=ROOT/'Ket_Qua_V2/KetQua_Nen'/parent/name
        p=run/'results.csv';df=pd.read_csv(p);df.columns=df.columns.str.strip()
        cfg=yaml.safe_load((run/'args.yaml').read_text(encoding='utf-8'))
        assert cfg['amp'] is False and cfg['batch']==8 and cfg['imgsz']==640 and cfg['epochs']==100
        configs.append({'experiment_model':m,'seed':seed,**{k:cfg.get(k) for k in ['epochs','batch','imgsz','amp','optimizer','lr0','lrf','weight_decay','warmup_epochs','workers','deterministic','cos_lr','mosaic','close_mosaic','overlap_mask','mask_ratio','fliplr','flipud','scale','translate','hsv_h','hsv_s','hsv_v']}})
        assert len(df)==100 and list(df.epoch)==list(range(1,101))
        assert df.select_dtypes('number').notna().all().all()
        r=df.loc[df[COLS['mask_map50_95']].idxmax()]
        fitness=df[COLS['mask_map50_95']]+df[COLS['box_map50_95']]
        fitness_epoch=int(df.loc[fitness.idxmax(),'epoch'])
        record={'model':m,'seed':seed,'best_epoch':int(r.epoch),**{k:float(r[v]) for k,v in COLS.items()},'run_path':str(run.relative_to(ROOT))}
        rows.append(record);curves[m].append(df)
        epochs.append({'model':m,'seed':seed,'max_mask_epoch':int(r.epoch),'sum_box_mask_fitness_epoch':fitness_epoch,'different':int(r.epoch)!=fitness_epoch})
        for file in ['results.csv','args.yaml','confusion_matrix.png','confusion_matrix_normalized.png']:
            if (run/file).exists():manifest(run/file,'training_source')
        audit.append({'model':m,'seed':seed,'epochs':len(df),'finite_numeric':True,'run_path':str(run.relative_to(ROOT))})
raw=pd.DataFrame(rows);ep=pd.DataFrame(epochs)
original=pd.read_csv(OUT/'raw_20seeds_extracted_metrics.csv').sort_values(['model','seed']).reset_index(drop=True)
recheck=raw.sort_values(['model','seed']).reset_index(drop=True)
for c in original.columns:
    if c in ['model','run_path']:continue
    assert np.allclose(original[c],recheck[c],atol=1e-12,rtol=0),c
csv(raw,'01_raw_analysis/reextracted_20seeds_metrics.csv')
csv(raw,'01_raw_analysis/raw_20seeds_extracted_metrics.csv')
csv(ep,'01_raw_analysis/epoch_selection_audit.csv')
shutil.copy2(OUT/'raw_20seeds_confusion_matrices.csv',OUT/'01_raw_analysis/raw_20seeds_confusion_matrices_original.csv')
summary=[];ranges=[];paired=[];wins=[]
for k in COLS:
    a=raw[raw.model=='Baseline'].sort_values('seed')[k].to_numpy();b=raw[raw.model=='TSVM'].sort_values('seed')[k].to_numpy();d=b-a
    varying=bool(d.std(ddof=1)>0)
    ci=stats.t.interval(.95,19,loc=d.mean(),scale=stats.sem(d)) if varying else (np.nan,np.nan)
    direction=-1 if k.startswith('val_') else 1
    nwin=int((d*direction>0).sum());nloss=int((d*direction<0).sum());ntie=20-nwin-nloss
    summary.append({'metric':k,'label':LABELS[k],'better':'lower' if direction<0 else 'higher','n_pairs':20,
       'baseline_mean':a.mean(),'baseline_sd':a.std(ddof=1),'tsvm_mean':b.mean(),'tsvm_sd':b.std(ddof=1),
       'delta_tsvm_minus_baseline':d.mean(),'relative_delta_pct':d.mean()/a.mean()*100 if a.mean()!=0 else np.nan,
       'delta_ci95_low':ci[0],'delta_ci95_high':ci[1],'paired_t_p':stats.ttest_rel(b,a).pvalue if varying else np.nan,
       'wilcoxon_two_sided_p':stats.wilcoxon(b,a).pvalue if varying else np.nan,'cohen_dz':d.mean()/d.std(ddof=1) if varying else np.nan,
       'shapiro_delta_p':stats.shapiro(d).pvalue if varying else np.nan,'levene_median_p':stats.levene(a,b,center='median').pvalue if a.std()+b.std()>0 else np.nan,
       'tsvm_wins':nwin,'baseline_wins':nloss,'ties':ntie,'sign_test_p':stats.binomtest(nwin,nwin+nloss,.5).pvalue if nwin+nloss else np.nan,
       'inference_status':'paired analysis' if varying else 'constant logged values; inferential tests N/A'})
    wins.append({'metric':k,'tsvm_wins':nwin,'baseline_wins':nloss,'ties':ntie,'lower_is_better':direction<0})
    for m,x in zip(MODELS,[a,b]):
        ranges.append({'metric':k,'model':m,'min':x.min(),'min_seed':int(x.argmin()),'max':x.max(),'max_seed':int(x.argmax()),'median':np.median(x),'range':np.ptp(x),'q25':np.percentile(x,25),'q75':np.percentile(x,75)})
    for seed in range(20):paired.append({'metric':k,'seed':seed,'baseline':a[seed],'tsvm_fp32':b[seed],'delta':d[seed]})
sm=pd.DataFrame(summary);pair=pd.DataFrame(paired)
stored_summary=pd.read_csv(OUT/'summary_20seeds_paired.csv').set_index('metric')
for _,r in sm.iterrows():
    if r.metric in stored_summary.index:
        old=stored_summary.loc[r.metric]
        assert abs(r.paired_t_p-old.p_ttest)<1e-12
        assert abs(r.baseline_mean-old.baseline_mean)<1e-12
        assert abs(r.tsvm_mean-old.tsvm_mean)<1e-12
csv(sm,'02_statistics/mean_std/full_comparison_mean_std.csv')
csv(pd.DataFrame(ranges),'02_statistics/min_max/metrics_min_max_range.csv')
csv(pair,'02_statistics/seed_comparison/seed_by_seed_metrics_and_deltas.csv')
csv(pd.DataFrame(wins),'02_statistics/seed_comparison/seed_win_loss_summary.csv')
csv(sm,'06_reports/summary.csv')
for group,prefix in [('segmentation','mask_'),('bounding_box','box_'),('loss','val_')]:
    csv(sm[sm.metric.str.startswith(prefix)],f'03_metrics/{group}/{group}_metrics_summary.csv')
csv(sm[sm.metric.str.startswith('val_')],'03_metrics/loss/validation_loss_metrics_summary.csv')

def meanbars(keys,title,path):
    f,a=chart(title,(max(6,len(keys)*1.7),4.5));x=np.arange(len(keys));w=.35
    for i,m in enumerate(MODELS):
        sub=sm.set_index('metric').loc[keys];means=sub['baseline_mean' if i==0 else 'tsvm_mean'];sd=sub['baseline_sd' if i==0 else 'tsvm_sd']
        positions=x+(i-.5)*.4
        a.bar(positions,means,.34,yerr=sd,capsize=4,color=COLORS[i],label=NAMES[i])
        for pos,value,error in zip(positions,means,sd):a.text(pos,value+error+.015,f'{value:.4f}',ha='center',va='bottom',fontsize=8)
    a.set_xticks(x,[LABELS[k].replace(' ','\n',1) for k in keys]);a.legend();a.set_ylabel('Mean ± sample SD, 20 seeds')
    if all(not k.startswith('val_') for k in keys):a.set_ylim(0,1)
    if len(keys)==1:a.set_xlim(-.75,.75)
    save(f,path,'Mean ± SD; selected epoch = maximum validation mask mAP50–95')
meanbars(['mask_map50_95'],'Mask mAP50–95 across 20 seeds','05_charts/performance/01_mask_map50_95_comparison.png')
meanbars(['mask_map50'],'Mask mAP50 across 20 seeds','05_charts/performance/02_mask_map50_comparison.png')
meanbars(['mask_precision','mask_recall'],'Mask precision and recall','05_charts/performance/03_precision_recall_comparison.png')
meanbars([k for k in COLS if k.startswith('box_')],'Bounding-box metrics','05_charts/performance/04_box_metrics_comparison.png')
meanbars(['val_seg_loss'],'Validation segmentation loss (lower is better)','05_charts/performance/05_val_seg_loss_comparison.png')
for n,k in [(6,'mask_map50_95'),(7,'box_map50_95')]:
    f,a=chart(f'{LABELS[k]} by paired seed')
    for m,c,label in zip(MODELS,COLORS,NAMES):a.plot(range(20),raw[raw.model==m][k],'o-',color=c,label=label)
    a.set_xticks(range(20));a.set_xlabel('Seed');a.set_ylabel(LABELS[k]);a.legend()
    save(f,f'05_charts/stability/{n:02}_seed_{k}_trends.png','Paired seed comparison; seed has no temporal interpretation')
f,a=chart('Distribution of mask mAP50–95')
values=[raw[raw.model==m].mask_map50_95.to_numpy() for m in MODELS]
a.boxplot(values,tick_labels=NAMES,showmeans=True)
for i,(v,c) in enumerate(zip(values,COLORS),1):a.scatter(i+np.linspace(-.07,.07,20),v,c=c,s=24,zorder=3)
a.set_ylabel('Mask mAP50–95');save(f,'05_charts/distribution/08_boxplot_mask_map50_95.png','All 40 observations; sample median, quartiles and mean')
f,a=chart('Mask mAP50–95 distribution (descriptive KDE)')
xs=np.linspace(.68,.755,300)
for v,c,n in zip(values,COLORS,NAMES):
    a.hist(v,bins=np.linspace(.69,.745,9),alpha=.25,density=True,color=c)
    a.plot(xs,stats.gaussian_kde(v)(xs),color=c,label=n)
a.set_xlabel('Mask mAP50–95');a.set_ylabel('Density');a.legend();save(f,'05_charts/distribution/09_histogram_kde_mask_map50_95.png','KDE is descriptive for only 20 seeds, not a normality claim')
meanbars(['mask_map50_95','mask_map50','mask_precision','mask_recall'],'Main segmentation metrics','05_charts/stability/10_mean_std_errorbars.png')
for n,x,y in [(11,'mask_precision','mask_recall'),(12,'mask_precision','mask_map50_95'),(13,'mask_recall','mask_map50_95')]:
    f,a=chart(f'{LABELS[y]} versus {LABELS[x]}')
    for m,c,nm in zip(MODELS,COLORS,NAMES):
        r=raw[raw.model==m];a.scatter(r[x],r[y],color=c,label=nm,alpha=.8)
    a.set_xlabel(LABELS[x]);a.set_ylabel(LABELS[y]);a.legend();save(f,f'05_charts/correlation/{n:02}_scatter_{y}_vs_{x}.png','Descriptive association across seeds; not causal')
meanbars(['mask_map50_95','mask_map50','mask_precision','mask_recall','box_map50_95','box_map50'],'Overall results: 20 paired seeds','05_charts/summary/18_grouped_bar_main_metrics.png')
keys=['mask_map50_95','mask_map50','mask_precision','mask_recall','box_map50_95','box_map50']
angles=np.linspace(0,2*np.pi,len(keys),endpoint=False);f,a=plt.subplots(figsize=(7,6),subplot_kw={'projection':'polar'})
for m,c,nm in zip(MODELS,COLORS,NAMES):
    v=raw[raw.model==m][keys].mean().to_numpy();a.plot(np.r_[angles,angles[0]],np.r_[v,v[0]],color=c,label=nm)
a.set_xticks(angles,[LABELS[k] for k in keys]);a.set_ylim(0,1);a.set_title('Descriptive mean metrics; full 0–1 scale',pad=22);a.legend(loc='lower right',bbox_to_anchor=(1.25,-.1))
save(f,'05_charts/summary/19_radar_chart_main_metrics.png','Descriptive only; area is not an overall score')
f,a=chart('Paired differences: TSVM FP32 − baseline (95% CI)',(9,5))
sub=sm.set_index('metric').loc[keys];d=sub.delta_tsvm_minus_baseline*100
a.errorbar(d,range(len(keys)),xerr=np.vstack([d-sub.delta_ci95_low*100,sub.delta_ci95_high*100-d]),fmt='o',color=COLORS[1],capsize=4)
a.axvline(0,color='gray',lw=1);a.set_yticks(range(len(keys)),[LABELS[k] for k in keys]);a.set_xlabel('Percentage points; two-sided paired t confidence intervals');a.invert_yaxis()
save(f,'05_charts/summary/20_delta_tsvm_vs_baseline.png','Unadjusted per-metric 95% paired confidence intervals, primary endpoint mask mAP50–95')
f,a=chart('Paired mask mAP50–95 difference by seed')
d=pair[pair.metric=='mask_map50_95'].delta.to_numpy()*100;a.bar(range(20),d,color=[COLORS[1] if v>0 else COLORS[0] for v in d]);a.axhline(0,color='gray',lw=1)
a.set_xticks(range(20));a.set_xlabel('Paired seed');a.set_ylabel('TSVM FP32 − baseline (percentage points)')
save(f,'05_charts/summary/21_paired_mask_map_delta.png','13 improvements and 7 decreases; mean +0.4303 percentage points')
f,a=chart('Head-to-head mask mAP50–95: 20 paired seeds',(7,4))
a.barh(['TSVM FP32 higher','Baseline higher'],[13,7],color=[COLORS[1],COLORS[0]])
for y,v in enumerate([13,7]):a.text(v+.2,y,f'{v}/20 ({v/20*100:.0f}%)',va='center')
a.set_xlim(0,20);a.set_xlabel('Number of paired seeds; ties = 0')
save(f,'05_charts/summary/24_head_to_head_seed_wins.png','Descriptive 13/20 improvements, two-sided sign test p=0.263176')
f,axs=plt.subplots(2,3,figsize=(12,7))
curve_rows=[]
for ax,key in zip(axs.ravel(),['val/seg_loss','val/box_loss','val/cls_loss','val/l1_loss','val/sem_loss']):
    for m,c,nm in zip(MODELS,COLORS,NAMES):
        arr=np.array([df[key] for df in curves[m]]);mean=arr.mean(0);sd=arr.std(0,ddof=1);x=np.arange(1,101)
        ax.plot(x,mean,color=c,label=nm);ax.fill_between(x,mean-sd,mean+sd,color=c,alpha=.15)
        curve_rows.extend({'model':m,'metric':key,'epoch':int(i),'mean':mu,'sd':s} for i,mu,s in zip(x,mean,sd))
    ax.set_title(key);ax.set_xlabel('Epoch');ax.set_ylabel('Loss');ax.legend(fontsize=8)
    if key=='val/sem_loss':ax.text(.5,.25,'Logged zeros; inference N/A',ha='center',transform=ax.transAxes,fontsize=9)
axs.ravel()[-1].axis('off')
save(f,'05_charts/convergence/22_validation_losses_mean_sd.png','40 runs; mean ± sample SD per epoch, not a confidence interval')
f,axs=plt.subplots(1,2,figsize=(11,4.5))
for ax,key in zip(axs,['metrics/mAP50-95(M)','metrics/mAP50-95(B)']):
    for m,c,nm in zip(MODELS,COLORS,NAMES):
        arr=np.array([df[key] for df in curves[m]]);mean=arr.mean(0);sd=arr.std(0,ddof=1);x=np.arange(1,101)
        ax.plot(x,mean,color=c,label=nm);ax.fill_between(x,mean-sd,mean+sd,color=c,alpha=.15)
        curve_rows.extend({'model':m,'metric':key,'epoch':int(i),'mean':mu,'sd':s} for i,mu,s in zip(x,mean,sd))
    ax.set_title(key);ax.set_xlabel('Epoch');ax.set_ylabel('mAP50–95');ax.legend(fontsize=8)
save(f,'05_charts/convergence/23_map_curves_mean_sd.png','20 seeds per curve, 100 epochs; early training band may be wider for TSVM')
for group,start,n in [('val',11,25),('train',1,26)]:
    f,axs=plt.subplots(2,2,figsize=(10,7))
    for ax,key in zip(axs.ravel(),[f'{group}/seg_loss',f'{group}/box_loss',f'{group}/cls_loss',f'{group}/l1_loss']):
        for m,c,nm in zip(MODELS,COLORS,NAMES):
            arr=np.array([df[key] for df in curves[m]]);mu=arr.mean(0);sd=arr.std(0,ddof=1);x=np.arange(1,101)
            sl=slice(start-1,None);ax.plot(x[sl],mu[sl],color=c,label=nm);ax.fill_between(x[sl],mu[sl]-sd[sl],mu[sl]+sd[sl],color=c,alpha=.15)
            if group=='train':curve_rows.extend({'model':m,'metric':key,'epoch':int(i),'mean':v,'sd':s} for i,v,s in zip(x,mu,sd))
        ax.set_title(key);ax.set_xlabel('Epoch');ax.set_ylabel('Loss');ax.legend(fontsize=8)
    save(f,f'05_charts/convergence/{n}_{group}_losses_mean_sd'+('_epoch11_100' if group=='val' else '')+'.png',f'Mean ± SD of actual {group} loss columns; epochs {start}–100; no DFL column exists')
csv(pd.DataFrame(curve_rows),'01_raw_analysis/per_epoch_mean_sd.csv')

# Detection background row/column is not an image-level binary confusion matrix.
cm=pd.read_csv(OUT/'raw_20seeds_confusion_matrices.csv');assert len(cm)==40
assert (cm.TP+cm.FN==127).all() and cm.TN.isna().all()
valid=cm[['model','seed','TP','FP','FN']].copy();valid['ground_truth_objects']=127
valid['object_recall_at_cm_threshold']=valid.TP/(valid.TP+valid.FN)
valid['object_precision_at_cm_threshold']=valid.TP/(valid.TP+valid.FP)
valid['source_status']='inherited extraction from saved confusion_matrix.png; not re-inference'
csv(valid,'04_confusion_matrix/count/validated_detection_counts_per_seed.csv')
csv(valid,'01_raw_analysis/raw_20seeds_confusion_matrices.csv')
cmmeans=valid.groupby('model')[['TP','FP','FN','object_recall_at_cm_threshold','object_precision_at_cm_threshold']].agg(['mean','std'])
cmmeans.columns=['_'.join(c) for c in cmmeans.columns];csv(cmmeans.reset_index(),'04_confusion_matrix/count/detection_counts_mean_sd.csv')
for m,nm in zip(MODELS,['baseline','tsvm_fp32']):
    r=valid[valid.model==m];csv(r,f'04_confusion_matrix/count/{nm}_cm_count_per_seed.csv')
    csv(pd.DataFrame({'seed':r.seed,'TP_pct_of_ground_truth_objects':r.TP/127*100,'FN_pct_of_ground_truth_objects':r.FN/127*100,'FP_pct':np.nan,'TN_pct':np.nan}),f'04_confusion_matrix/percentage/{nm}_cm_percentage_per_seed.csv')
    mean=r[['TP','FP','FN']].mean();matrix=np.array([[mean.TP,mean.FP],[mean.FN,np.nan]])
    csv(pd.DataFrame([{'predicted':'polyp','true_polyp':mean.TP,'true_background':mean.FP},{'predicted':'background','true_polyp':mean.FN,'true_background':np.nan}]),f'04_confusion_matrix/count/{nm}_cm_mean_count.csv')
    for percentage in [False,True]:
        mat=matrix.copy()
        if percentage:mat[:,0]=mat[:,0]/127*100;mat[0,1]=np.nan
        folder='percentage' if percentage else 'count';f,a=chart(f'{NAMES[MODELS.index(m)]}: '+('ground-truth object column (%)' if percentage else 'mean detection counts'),(6.5,5))
        a.grid(False);a.imshow(np.ma.masked_invalid(mat),cmap='Blues',vmin=0,vmax=100 if percentage else 127)
        for y in range(2):
            for x in range(2):
                value=mat[y,x];label=(f'{value:.2f}%' if percentage else f'{value:.2f}') if np.isfinite(value) else 'N/A'
                a.text(x,y,label,ha='center',va='center',fontsize=14,color='white' if np.isfinite(value) and value>65 else 'black')
        a.set_xticks([0,1],['polyp','background']);a.set_yticks([0,1],['polyp','background']);a.set_xlabel('Ground truth');a.set_ylabel('Prediction')
        save(f,f'04_confusion_matrix/{folder}/{nm}_mean_{folder}.png','N/A background/background; FP excluded from percentage because no valid ground-truth background denominator')
        if percentage:csv(pd.DataFrame([{'predicted':'polyp','true_polyp_pct':mean.TP/127*100,'true_background_pct':np.nan},{'predicted':'background','true_polyp_pct':mean.FN/127*100,'true_background_pct':np.nan}]),f'04_confusion_matrix/{folder}/{nm}_mean_percentage.csv')
f,a=chart('Detection TP, FN and FP: mean ± SD (20 seeds)')
for i,(m,nm,c) in enumerate(zip(MODELS,NAMES,COLORS)):
    r=valid[valid.model==m];a.bar(np.arange(3)+(i-.5)*.35,r[['TP','FN','FP']].mean(),.35,yerr=r[['TP','FN','FP']].std(ddof=1),capsize=4,color=c,label=nm)
a.set_xticks(range(3),['TP','FN','FP']);a.set_ylabel('Detection counts, not image counts');a.legend()
save(f,'04_confusion_matrix/count/mean_tp_fn_fp_comparison.png','Counts inherited from saved confusion matrices; not clinical specificity')

main=sm[sm.metric=='mask_map50_95'].iloc[0]
summary_text=f'''# Đối sánh 20 seed: YOLO26s-seg và TSVM FP32

## Thiết kế và quy tắc đọc số liệu
40 lần huấn luyện đã lưu, seed 0–19 ghép cặp, 100 epoch/lần. Script này chỉ đọc tệp, không huấn luyện hay suy luận lại. Tập validation: 160 ảnh, 40 ảnh nền và 127 đối tượng polyp. Các seed dùng cùng một tập validation; kiểm định mô tả biến thiên huấn luyện, không chứng minh khả năng tổng quát trên bệnh viện khác.

Bảng chính trích **epoch có validation mask mAP50–95 lớn nhất** (khi hòa chọn dòng đầu tiên). Đây là quy tắc của CSV gốc, **không đồng nhất với epoch của best.pt**: fitness lưu checkpoint là tổng box mAP50–95 và mask mAP50–95. Có {int(ep.different.sum())}/40 lần khác epoch. Xem `01_raw_analysis/epoch_selection_audit.csv`. Chỉ số tại epoch tối ưu validation có thiên lệch lựa chọn; cần test độc lập cho kết luận tổng quát.

## Kết quả chính
- Baseline mask mAP50–95: {main.baseline_mean:.6f} ± {main.baseline_sd:.6f}.
- TSVM FP32: {main.tsvm_mean:.6f} ± {main.tsvm_sd:.6f}.
- Chênh lệch TSVM − baseline: {main.delta_tsvm_minus_baseline:.6f}, tức **+{main.delta_tsvm_minus_baseline*100:.4f} điểm phần trăm**; thay đổi tương đối {main.relative_delta_pct:.4f}%.
- Khoảng tin cậy 95% của chênh lệch ghép cặp: [{main.delta_ci95_low:.6f}; {main.delta_ci95_high:.6f}].
- Paired t-test hai phía p={main.paired_t_p:.6f}; Wilcoxon hai phía p={main.wilcoxon_two_sided_p:.6f}. **Chưa đạt ý nghĩa thống kê ở α=0,05**.
- TSVM tăng 13/20 seed, giảm 7/20; sign test p={main.sign_test_p:.6f}. Đây không phải xác suất thắng trên một bệnh nhân mới.
- SD giảm {(1-main.tsvm_sd/main.baseline_sd)*100:.2f}% tại epoch được chọn. Đây là quan sát ổn định cuối cùng; không khẳng định mọi epoch đều có band hẹp hơn.

## Bảng tổng hợp
|Chỉ số|Baseline mean ± SD|TSVM FP32 mean ± SD|Δ|Paired t p|
|---|---:|---:|---:|---:|
'''
for _,r in sm.iterrows():
    pvalue=f'{r.paired_t_p:.6f}' if np.isfinite(r.paired_t_p) else 'N/A'
    summary_text+=f'|{r.label}|{r.baseline_mean:.6f} ± {r.baseline_sd:.6f}|{r.tsvm_mean:.6f} ± {r.tsvm_sd:.6f}|{r.delta_tsvm_minus_baseline:+.6f}|{pvalue}|\n'
summary_text+='''
## Kiểm định và giới hạn
SD dùng ddof=1. Paired t CI và p-value dùng 20 hiệu số cùng seed; Wilcoxon là kiểm tra độ nhạy, Shapiro cho hiệu số chỉ là chẩn đoán. Không diễn giải Shapiro p>0,05 như bằng chứng chắc chắn phân phối chuẩn. Endpoint chính là mask mAP50–95. Các p-value khác chưa hiệu chỉnh đa kiểm định, có tính thăm dò; Levene chỉ thăm dò vì bỏ qua cấu trúc ghép cặp. Không coi p>0,05 là chứng minh hai mô hình tương đương. Cột val/sem_loss được ghi bằng 0 trong cả 40 run, do đó kiểm định và thay đổi tương đối là N/A; không diễn giải đây là mức lỗi bằng 0 trên dữ liệu thực. YOLO26 trong các CSV này có val/l1_loss, không có val/dfl_loss; không kế thừa nhãn DFL từ biểu đồ cũ.

## Ma trận nhầm lẫn
CSV gốc có TN trống và trường `TN_reconstructed=40-FP`. Trường này **không hợp lệ**: FP là số phát hiện dư, có thể nằm trên ảnh chứa polyp và có nhiều phát hiện trên cùng ảnh. Không thể suy ra số ảnh nền dự đoán đúng bằng 40−FP. Gói mới giữ CSV gốc để truy vết, loại trường suy diễn khỏi mọi bảng/hình mới, để ô nền/nền là N/A và không tính specificity/accuracy ảnh. Phần trăm chỉ chuẩn hóa cột 127 đối tượng polyp; FP không được chuẩn hóa bằng 40. Các số TP/FP/FN kế thừa bảng trích từ ảnh confusion matrix đã lưu, chưa đối chiếu bằng suy luận mới. TP+FN=127 được kiểm tra đủ 40 dòng. Không trộn precision/recall tại ngưỡng CM với precision/recall được Ultralytics chọn theo đường cong trong bảng metric. Các ảnh CM cuối quá trình huấn luyện thuộc đánh giá checkpoint best.pt theo fitness; không được coi là cùng epoch với bảng max-mask trong các lần hai quy tắc chọn khác nhau. CSV CM kế thừa không lưu ngưỡng confidence/IoU nên không suy diễn một ngưỡng lâm sàng từ bảng này.

## Không có trong dữ liệu này
Không có Dice, IoU trung bình vùng, Hausdorff, Betti, clDice hay xác nhận topology trực tiếp. Không quy đổi AP thành Dice/IoU. Tên topology/shape là định hướng thiết kế; lợi ích topology cần thí nghiệm riêng. Benchmark hiệu suất ở thư mục riêng, không suy ra FPS từ thời gian epoch, không gán số của TSVM cũ sang FP32.
'''
write_text('06_reports/summary.md',summary_text)
write_text('06_reports/conclusions_reviewed.md',summary_text)
write_text('04_confusion_matrix/README.md',summary_text.split('## Ma trận nhầm lẫn')[1].split('## Không có')[0])
write_text('07_audit/audit_report.md',f'''# Kiểm tra nguồn và tính tái lập

- 40/40 results.csv đủ 100 epoch liên tục và không có NaN số học.
- Trích lại toàn bộ metric có sẵn trong CSV gốc, khớp tuyệt đối trong sai số 1e-12.
- Đọc thêm val/box_loss, val/cls_loss, val/l1_loss và val/sem_loss trực tiếp từ results.csv.
- Chỉ dùng nhánh `Kvasir_BG20_YOLO26s_seg_TSVM_FP32`, không đọc TSVM cũ.
- 20 cặp seed 0–19. {int(ep.different.sum())}/40 epoch max mask khác epoch fitness sum mask+box.
- TP+FN=127 cho 40 dòng, TN trống 40 dòng; bỏ TN_reconstructed trong bảng dẫn xuất.
- SHA256 của nguồn và phiên bản thư viện ở JSON kèm theo. Hash giúp phát hiện thay đổi, không tự chứng minh nội dung OCR đúng.
- Không sửa CSV gốc, facts.json, summary_20seeds_paired.csv hoặc figures gốc.
- Không huấn luyện, không inference, không đổi checkpoint.
''')
csv(pd.DataFrame(audit),'07_audit/source_checks.csv')
csv(raw,'07_audit/reextracted_from_results_csv.csv')
cfgdf=pd.DataFrame(configs)
for key in cfgdf.columns.difference(['experiment_model','seed']):assert cfgdf[key].astype(str).nunique()==1,key
csv(cfgdf,'07_audit/training_configuration_comparison.csv')
versions={'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__,'scipy':__import__('scipy').__version__,'matplotlib':matplotlib.__version__,'PyYAML':yaml.__version__}
manifest(OUT/'raw_20seeds_extracted_metrics.csv','existing_input');manifest(OUT/'raw_20seeds_confusion_matrices.csv','existing_cm_input');manifest(Path(__file__),'generator')
write_text('07_audit/source_manifest.json',json.dumps({'versions':versions,'inputs':MANIFEST},ensure_ascii=False,indent=2))
write_text('07_audit/figure_manifest.json',json.dumps(FIGURES,ensure_ascii=False,indent=2))
write_text('06_reports/chart_mapping.md','# Danh mục hình và quy tắc diễn giải\n\n|Hình|Diễn giải/giới hạn|\n|---|---|\n'+''.join(f'|`{r["path"]}`|{r["description"]}|\n' for r in FIGURES))
recommend='''# Hình ưu tiên cho Chương 5

1. `05_charts/performance/01_mask_map50_95_comparison.png`: bảng điểm chính mean ± SD; phải kèm CI và p.
2. `05_charts/summary/20_delta_tsvm_vs_baseline.png`: độ lớn và bất định của các chênh lệch.
3. `05_charts/summary/21_paired_mask_map_delta.png`: thể hiện 13 tăng/7 giảm, tránh chỉ chọn seed thuận lợi.
4. `05_charts/distribution/08_boxplot_mask_map50_95.png`: toàn bộ phân phối20seed, không chỉ mean.
5. `05_charts/convergence/22_validation_losses_mean_sd.png`: tiến trình5 loss, band là SD.
6. `05_charts/convergence/23_map_curves_mean_sd.png`: tiến trình mask/box AP100 epoch.
7. `04_confusion_matrix/count/mean_tp_fn_fp_comparison.png`: TP/FN/FP ở mức phát hiện; không có TN/specificity.
8. `05_charts/performance/03_precision_recall_comparison.png`: đánh đổi precision/recall.

Các hình radar, KDE, scatter có thể để phụ lục vì chỉ có tính mô tả. Bổ sung hình qualitative từ val_batch... nếu dùng phải ghi seed và đó là checkpoint best.pt (fitness), không đồng nhất với bảng max-mask. Không chọn hình theo kết quả đẹp nhất rồi coi là đại diện ngẫu nhiên.
'''
write_text('06_reports/recommended_figures_for_thesis.md',recommend)
write_text('README.md','''# Kết quả 20 seed: YOLO26s-seg và TSVM FP32

Gói mở rộng ngày 16/10/2026. Giữ nguyên đầu vào ở thư mục gốc và `figures/` cũ. Các dẫn xuất mới dựa trực tiếp vào 40 results.csv; chỉ dùng TSVM có hậu tố FP32.

|Thư mục|Nội dung|
|---|---|
|01_raw_analysis|Trích lại40 run,13 chỉ số,epoch lựa chọn và đường cong mean/SD100 epoch|
|02_statistics|Mean/SD, CI95% ghép cặp, pairedt, Wilcoxon, extrema, từng seed và thắng/thua|
|03_metrics|Tách metric mask, box và validationloss|
|04_confusion_matrix|TP/FP/FN và heatmap; TN luôn N/A; cảnh báo dữ liệu kế thừa|
|05_charts|Hiệu năng, độ ổn định, phân phối, tương quan, tổng hợp và hội tụ|
|06_reports|Báo cáo diễn giải, CSV và hình khuyến nghị cho luận văn|
|07_audit|Kiểm tra nguồn, SHA256, môi trường và danh mục hình|
|efficiency_benchmark|Benchmark FP32 riêng; có script và phạm vi đo riêng|

## Tái lập
Chạy `.codex_revision_20261016/results/generate_results_package.py` bằng Python có numpy, pandas, scipy, matplotlib, PyYAML. Script tìm gốc dự án theo vị trí tệp, không phụ thuộc thư mục làm việc. Với môi trường hiện tại dùng Python bundled và PYTHONPATH trỏ `.codex_report_work_20261015/packages`.

Đọc `06_reports/summary.md` trước khi trích dẫn. Quan trọng: epoch max mask ≠ best.pt trong16/40 run; p chính0,061431; không có TN ảnh, Dice hay kiểm chứng topology. Kết quả10seed là thực nghiệm khác, chỉ mượn cách tổ chức thư mục và không sao chép số liệu.
''')
print(f'Created {len(FIGURES)} figures; 40 runs independently checked. Primary paired t p={main.paired_t_p:.9f}.')
