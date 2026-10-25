from pathlib import Path
import csv, json, statistics as st, math, re, hashlib, collections
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
P='Ket_Qua_V2/KQ_Nen_DX_20seed_FP32'
def readcsv(p):
    with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(name,rows):
    if not rows:return
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
blocks=readcsv(str(OUT.relative_to(ROOT)/'word_blocks.csv'));byid={r['id']:r for r in blocks}
raw={}; recomputed=[]; epoch=[]; configchecks=[]
cols={'mask_map50_95':'metrics/mAP50-95(M)','mask_map50':'metrics/mAP50(M)','mask_precision':'metrics/precision(M)','mask_recall':'metrics/recall(M)',
      'box_map50_95':'metrics/mAP50-95(B)','box_map50':'metrics/mAP50(B)','box_precision':'metrics/precision(B)','box_recall':'metrics/recall(B)',
      'val_seg_loss':'val/seg_loss','val_box_loss':'val/box_loss','val_cls_loss':'val/cls_loss','val_l1_loss':'val/l1_loss','val_sem_loss':'val/sem_loss'}
for model,parent,prefix in [('Baseline','YOLOv26s-seg','Kvasir_BG20_Baseline_YOLO26s_seg'),('TSVM','Kvasir_BG20_YOLO26s_seg_TSVM_FP32','Kvasir_BG20_YOLO26s_seg_TSVM_FP32')]:
    raw[model]=[]
    for seed in range(20):
        path=f'Ket_Qua_V2/KetQua_Nen/{parent}/{prefix}_s{seed}_w2'
        rr=readcsv(path+'/results.csv'); rr=[{k.strip():float(v) for k,v in r.items()} for r in rr]
        assert len(rr)==100 and [r['epoch'] for r in rr]==list(range(1,101))
        r=max(rr,key=lambda x:x[cols['mask_map50_95']]);fit=max(rr,key=lambda x:x[cols['mask_map50_95']]+x[cols['box_map50_95']])
        record={'model':model,'seed':seed,'max_mask_epoch':int(r['epoch']),'max_fitness_epoch':int(fit['epoch']),**{k:r[v] for k,v in cols.items()},'source':path+'/results.csv','csv_line':int(r['epoch'])+1}
        recomputed.append(record);raw[model].append(record);epoch.append(record['max_mask_epoch']!=record['max_fitness_epoch'])
        args={l.split(':',1)[0]:l.split(':',1)[1].strip() for l in (ROOT/path/'args.yaml').read_text(encoding='utf-8').splitlines() if ':' in l}
        expected={'epochs':'100','patience':'100','batch':'8','imgsz':'640','optimizer':'AdamW','lr0':'0.001','weight_decay':'0.0005','warmup_epochs':'5.0','lrf':'0.01','cos_lr':'false','workers':'2','amp':'false','deterministic':'true','close_mosaic':'10','mask_ratio':'4','overlap_mask':'true','mosaic':'1.0','translate':'0.1','scale':'0.5','hsv_h':'0.015','hsv_s':'0.7','hsv_v':'0.4','fliplr':'0.5','flipud':'0.0','degrees':'0.0','shear':'0.0','perspective':'0.0','mixup':'0.0','cutmix':'0.0','copy_paste':'0.0','seed':str(seed)}
        for k,v in expected.items():configchecks.append({'model':model,'seed':seed,'field':k,'expected':v,'actual':args.get(k),'status':'MATCH' if args.get(k)==v else 'MISMATCH','source':path+'/args.yaml'})
writecsv('raw_metrics_recomputed.csv',recomputed);writecsv('training_configuration_checks.csv',configchecks)

def t_p(t,df=19):
    t=abs(t);c=math.exp(math.lgamma((df+1)/2)-math.lgamma(df/2))/math.sqrt(df*math.pi)
    f=lambda x:c*(1+x*x/df)**(-(df+1)/2)
    n=10000;h=t/n
    return max(0.,min(1.,1-2*h/3*(f(0)+f(t)+sum((4 if i%2 else 2)*f(i*h) for i in range(1,n)))))
stats={}
for k in cols:
    a=[r[k] for r in raw['Baseline']];b=[r[k] for r in raw['TSVM']];d=[y-x for x,y in zip(a,b)];sd=st.stdev(d)
    stats[k]={'baseline_mean':st.mean(a),'baseline_sd':st.stdev(a),'tsvm_mean':st.mean(b),'tsvm_sd':st.stdev(b),'delta_tsvm_minus_baseline':st.mean(d),
              'delta_ci95_low':st.mean(d)-2.093024054408263*sd/math.sqrt(20),'delta_ci95_high':st.mean(d)+2.093024054408263*sd/math.sqrt(20),
              'paired_t_p':t_p(st.mean(d)/(sd/math.sqrt(20))) if sd else math.nan}
stored={r['metric']:r for r in readcsv(P+'/02_statistics/mean_std/full_comparison_mean_std.csv')}
cellchecks=[]
def check(block,field,observed,expected,digits,source):
    # Half a unit in the last displayed place, allowing floating tie rounding.
    ok=abs(observed-expected)<=.500001*10**(-digits)
    cellchecks.append({'word_id':block,'field':field,'word_value':observed,'expected_unrounded':expected,'display_decimals':digits,'status':'MATCH' if ok else 'MISMATCH','source':source})
def nums(s):return [float(x.replace(',','.')) for x in re.findall(r'[-−]?\d+,\d+',s.replace('−','-'))]
keys=list(cols)[:8]+['val_seg_loss']
for ri,k in enumerate(keys,2):
    id=f'T10R{ri:03d}';rr=nums(byid[id]['text'])
    for field,v in zip(['baseline_mean','baseline_sd','tsvm_mean','tsvm_sd','delta_tsvm_minus_baseline'],rr):check(id,field,v,stats[k][field],4,'40 raw results.csv, same selected max-mask row')
for ri,k in enumerate(['mask_map50_95','mask_map50','mask_precision','mask_recall','box_map50_95','box_recall','val_seg_loss'],2):
    id=f'T11R{ri:03d}';vv=nums(byid[id]['text'])
    for field,v in zip(['delta_ci95_low','delta_ci95_high','paired_t_p','wilcoxon_two_sided_p'],vv):
        expect=float(stored[k][field]) if field=='wilcoxon_two_sided_p' else stats[k][field]
        check(id,field,v,expect,4,'raw CSV + independent stdlib mean/SD/t integration; Wilcoxon checked to stored table and A independent SciPy')
for seed in range(20):
    id=f'T12R{seed+2:03d}';parts=byid[id]['text'].split(' | ');a=raw['Baseline'][seed];b=raw['TSVM'][seed]
    expected=[seed,a['max_mask_epoch'],b['max_mask_epoch'],a['mask_map50_95'],b['mask_map50_95'],b['mask_map50_95']-a['mask_map50_95']]
    for j,(v,e) in enumerate(zip(parts,expected)):check(id,str(j),float(v.replace(',','.')),e,0 if j<3 else 5,a['source']+'; '+b['source'])
for ri,m in [(2,'Baseline'),(3,'TSVM')]:
    x=[r['mask_map50_95'] for r in raw[m]];values=nums(byid[f'T13R{ri:03d}']['text'])
    for f,v,e in zip(['min','median','max','range'],values,[min(x),st.median(x),max(x),max(x)-min(x)]):check(f'T13R{ri:03d}',f,v,e,5,'40 raw CSV')
for index,r in enumerate(recomputed,2):
    id=f'T18R{index:03d}';parts=byid[id]['text'].split(' | ')
    for field,v in zip(['seed','max_mask_epoch','max_fitness_epoch'],parts[1:]):check(id,field,float(v),r[field],0,r['source'])
cm=readcsv(P+'/01_raw_analysis/raw_20seeds_confusion_matrices.csv')
for ri,m in [(2,'Baseline'),(3,'TSVM')]:
    subset=[r for r in cm if r['model']==m];vv=nums(byid[f'T14R{ri:03d}']['text']);ex=[]
    for k in ['TP','FP','FN']:x=[float(r[k]) for r in subset];ex.extend([st.mean(x),st.stdev(x)])
    for j,(v,e) in enumerate(zip(vv,ex)):check(f'T14R{ri:03d}',str(j),v,e,2,'inherited CM extraction, validity against raw images delegated B')

def quantile(x,p):
    xx=sorted(x);h=(len(xx)-1)*p;i=int(h);return xx[i]+(xx[min(i+1,len(xx)-1)]-xx[i])*(h-i)
bench={}
for model,file in [('Baseline','baseline'),('TSVM','tsvm')]:
    rr=readcsv(P+f'/efficiency_benchmark/raw/{file}_timings.csv')
    for mode in ['forward_only','predict_pipeline']:
        vv=[float(r['latency_ms']) for r in rr if r['mode']==mode]
        bench[(model,mode)]={'mean':st.mean(vv),'sd':st.stdev(vv),'p50':quantile(vv,.5),'p95':quantile(vv,.95),'p99':quantile(vv,.99),'fps':1000/st.mean(vv)}
for ri,mode,fields in [(2,'forward_only',['mean','sd']),(3,'forward_only',['p50']),(4,'forward_only',['p95']),(5,'forward_only',['p99']),(6,'forward_only',['fps']),
                        (7,'predict_pipeline',['mean','sd']),(8,'predict_pipeline',['p50']),(9,'predict_pipeline',['p95']),(10,'predict_pipeline',['p99']),(11,'predict_pipeline',['fps'])]:
    id=f'T16R{ri:03d}';vv=nums(byid[id]['text']);expected=[bench[(m,mode)][f] for m in ['Baseline','TSVM'] for f in fields]
    for j,(v,e) in enumerate(zip(vv,expected)):check(id,str(j),v,e,2,'400 stored raw timing rows; no rerun')
writecsv('numeric_cell_checks.csv',cellchecks)

issues=[]
def issue(id,severity,status,location,title,evidence,impact,request):
    issues.append({'issue_id':id,'severity':severity,'status':status,'word_location':location,'title':title,'evidence':evidence,'impact':impact,'next_evidence_or_action':request})
issue('C-001','medium','CONFIRMED_MISMATCH','T03R003 / Bảng 2.1','Backbone P4 channel count is 512 in Word, actual 256',
      'YAML cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml:13,26-27; nn/tasks.py:2071; root/checkpoint_inventory.json corroborates layer6 cv2 out_channels=256 for both models',
      'Architecture table is inaccurate; does not change CSV statistics.','Correct only after authorized; keep audit evidence unchanged.')
issue('C-002','medium','CONFIRMED_MISMATCH','P0515 / mục 4.6','Word says both models return one mask; saved TSVM smoke has two',
      '.codex_revision_20261016/smoke_results.json: TSVM samples[0].maskCount=2, baseline=1; same checkpoint hashes/sample as report',
      'Demonstration narrative is inaccurate and may hide an additional detection.','E validate response semantics; B inspect actual Hình 4.2. This finding is against historical saved evidence, not a new runtime claim.')
issue('C-003','medium','CONFIRMED_REPRODUCIBILITY_GAP','P0766 / Phụ lục A','Appendix points to polyp-only converter and omits actual BG20 builder',
      'Stracth/Du_Lieu/convert_kvasir_to_yolo_seg.py:773 sets output Kvasir_YOLO_SEG, no normal-cecum addition; actual builder Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py:124-150 has stale source paths',
      'Following appendix alone cannot reproduce BG20 in current layout. Existing dataset counts may still be correct.','Document actual BG20 builder, current input paths and read-only reproduction protocol.')
issue('C-004','medium','CONFIRMED_REPRODUCIBILITY_GAP','P0369; P0467; P0765','Local data YAML points to a missing dataset directory',
      'archive/data_bg20.yaml:2 path ends archive/Kvasir_YOLO_SEG_BG20; actual dataset is archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20; root/dataset_independent.json',
      'Local reproduction/config use needs correction; does not prove historical Kaggle path was wrong.','Keep historical Kaggle args separate; fix local path only in a later authorized edit.')
issue('C-005','high','CONFIRMED_DOCUMENT_DRIFT','Bao_cao/md viet bao cao/06_...md:27,80-93,216; main P0550/P0666/P0702','Markdown draft contradicts main FP32 Word on seed scope, TN, Dice and GPU speed',
      'Draft chapter5 uses10seed, TN=40-FP as valid, unmeasured Dice and GPU18.2/28.5ms; main Word explicitly rejects these claims',
      'Rebuilding report from drafts can reintroduce unsupported claims; this is not an error in current Word numeric tables.','Mark drafts historical or synchronize only after approval; do not silently treat them as current source.')
issue('C-006','medium','CONFIRMED_DOCUMENT_DRIFT','doc/01_KIEN_TRUC_TSVM_TANG_10.md:49,62,69; main P0315/P0321/P0327','Architecture Markdown diagram is stale relative to code and Word',
      'MD shows F_ss2d*G, FFN Conv3x3+GELU and O(N); code has1+G, two1x1 Conv and tensor work O(LlogL)',
      'Readers following knowledge base can misunderstand actual implementation.','Treat code and current Word as implementation evidence; correct MD later.')
issue('C-007','medium','CONFIRMED_DOCUMENT_DRIFT','doc/CURRENT_PROJECT_STATUS.md:68-92; doc/README.md:5,120; main P0535','Current-status entry documents remain snapshots of older experiments',
      'Current-status text prioritizes10seed and FP+TN=40; latest Word/main package20seed FP32 differs',
      'Entry-point documentation can direct future agents to the wrong experiment.','Preserve dates/history; add explicit latest-status index later.')
issue('C-008','medium','INSUFFICIENT_EVIDENCE','P0363 / reference[3]','Attribution of fixed880/120 split to original dataset authors needs provenance',
      'Local train.txt/val.txt demonstrate membership/counts, not authorship or official release provenance; Kaggle citation must be verified by D',
      'Do not infer scientific comparability solely from claiming an official split.','D inspect original Kaggle/files and source paper release, report support level.')
issue('C-009','medium','PENDING_LITERATURE_REVIEW','P0268-P0273; T02; T17; P0733-P0756','24 references and paper comparison numbers need primary-source verification',
      'citation_inventory.csv contains full reference text/DOI/URL; local source comparison claims retained for D',
      'C validates separation of protocols, not external metadata or numerical correctness of paper tables.','D verify all24 citations; specifically[17]-[21] and T17 sizes/Dice/IoU.')
issue('C-010','medium','PENDING_APPLICATION_REVIEW','T09R002-T09R006; P0515; P0772-P0779','Application test totals and current runtime need E confirmation',
      '.codex_revision_20261016/test_status.json stores51/261/498 and smoke_results.json stores true checkpoint results; these are historical logs, not a new run',
      'Historical test counts cannot be asserted as current all-suite status without replay or source/log context.','E distinguish code/mock/real inference/end-to-end; cross-check saved logs and model key/precision/contracts.')
issue('C-011','medium','NOT_ASSESSED','Whole report','Turnitin percentage cannot be determined from this local audit',
      'No Turnitin report, school exclusion settings or submission-history evidence supplied; no external upload performed',
      'No basis to promise a similarity score below30% or an AI-writing result.','Obtain official report/settings; D/C review source-level overlaps and citation fidelity without evasion.')
writecsv('issues.csv',issues)

ledger=[]
def claim(id,ids,claim,status,source,method,limits=''):
    ledger.append({'claim_id':id,'word_ids':ids,'claim':claim,'status':status,'source_evidence':source,'method':method,'limits':limits})
claim('CARCH01','P0075;P0209;P0285-P0301;T03','Replace C2PSA at layer10, small scaling/channels','PARTIAL_MATCH_WITH_C001','FP32 YAML:13,21-31,36-52; nn/tasks.py:2067-2071','Read source/scaling and checkpoint corroboration','P4 row256 not512')
claim('CARCH02','P0256-P0265;P0304-P0307','SS2D4directions, state16, dt_rank16 and no out_norm/D skip','MATCH_STATIC_CODE','nn/modules/topology_shape_vmamba.py:20-210','Read entire module, directional reversals and tensor operations','Equation omits numerical clamp as abstraction; not a reference implementation equivalence claim')
claim('CARCH03','P0309-P0317;P0321-P0323;T04','Shape kernels, guidance1+G, FFN1x1 and residual gamma.001','MATCH_STATIC_CODE','nn/modules/topology_shape_vmamba.py:213-432','Compare formulas and four mode branches','Does not prove better boundaries/topology')
claim('CARCH04','P0326-P0329','Scan has9steps forL400 padded512; tensor workO(LlogL)','MATCH_STATIC_CODE','nn/modules/topology_shape_vmamba.py:20-60','Count doubling steps and per-step tensor spans','Computational work, not measured GPU speed')
claim('CARCH05','P0331-P0339','FP32 save+strip and fail on NaN; no custom topology loss','MATCH_STATIC_CODE','engine/trainer.py:713-731; utils/torch_utils.py:828-835; nn/modules/topology_shape_vmamba.py','Inspect snapshot dtype and checks; inspect loss path','Historical training exact imported code provenance further checked by A/root')
claim('CDATA01','P0220-P0222;T05;P0364-P0369;P0447','Dataset1040/160,936/127objects,empty160/40','MATCH_LOCAL_DATA','Ket_Qua_V2/Kvasir_YOLO_SEG_BG20; root/dataset_independent.json','Count label files/rows and hashes, root independent corroboration','No patient IDs or near-duplicate audit')
claim('CDATA02','P0353;P0356','1000polyp images333sizes width332-1920 height352-1072;1000cecum720x576','MATCH_INDEPENDENT_IMAGE_READ','Ket_Qua_V2/Data Prosessing/{Kvasir-SEG/images,normal-cecum}','Pillow open every image and count dimensions','Polyp area range/contour counts require mask reprocessing, separately noted')
claim('CDATA03','P0373-P0392;P0397','Otsu, closing3x3, external contours area>=20,epsilon.002L,6decimals','MATCH_STATIC_CODE_WITH_DETAIL_GAPS','Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py:40-119','Read conversion function without running builder','Otsu5-8,1206/143 contour counts,333.2->24.6 vertices and image example not independently recomputed by C; request root/B')
claim('CDATA04','P0399-P0405;P0410','Two-stage resizeceil+LetterBox with114 and rectangular validation','MATCH_STATIC_CODE','data/base.py:268-280,408; data/augment.py:1738-1766; models/yolo/detect/train.py','Inspect actual two-stage loader and batch shapes','Formula is square illustrative case; actual batch target may differ, explicitly stated')
claim('CDATA05','P0413-P0429;T06;P0439-P0444','Mosaic/affine/HSV/flip;RGB/255;maskratio4','MATCH_CONFIG_AND_CODE','40args.yaml; data/augment.py:1475-1487,2812-2860; data/dataset.py; models/yolo/detect/train.py','Check40configs, HSV additive formula, augmentation order, mask formatting','Albumentations activation specific log claim not generalized to all40runs')
claim('CTRAIN01','P0459-P0474;T07','40runs100epochs same documented hyperparameters; notebook single seed old path','MATCH_CONFIG_WITH_REPRODUCTION_GAPS','training_configuration_checks.csv; Cell Kaggle/*.ipynb','Independent config extraction and notebook source read','No inference that saved notebook itself orchestrated40runs; C003/C004')
claim('CSTAT01','P0076;P0082;P0535-P0545;P0767;T18','20pairs,maxmask selection,16epoch disagreements,bestfitness=sum box+mask','MATCH_INDEPENDENT_RECALCULATION','raw_metrics_recomputed.csv; metrics.py:1007-1010,1369-1371','Reread all40CSV,100epochs and bothargmax rules','Does not independently revalidate saved checkpoint AP')
claim('CSTAT02','T10;T11;T12;T13;P0560-P0618;P0634;P0723','Means/SD/deltas/CI/t p/seed wins/ranges','MATCH_RECALCULATION_AT_DISPLAY_PRECISION','numeric_cell_checks.csv; A_numeric independentSciPy','C recomputed raw means/SD/pairedt via integration,CI usingt19; Wilcoxon cross-check stored+A','Levene correctly exploratory with paired caveat; no equivalence or clinical inference')
claim('CCM01','T14;P0656-P0670','CM object counts,invalidTN=40-FP,no specificity','MATCH_TO_INHERITED_COUNTS_AND_CORRECT_SCOPE','raw_20seeds_confusion_matrices.csv; utils/metrics.py; numeric_cell_checks.csv','Recompute meanSD from extractedcounts; read object semantics','Image OCR/provenance is B responsibility; not new fullval inference')
claim('CBENCH01','P0673-P0705;T15;T16;P0725','Params/memory/CPUtimings/protocol/limits','MATCH_TO_STORED_RAW_AND_SCRIPT','efficiency_benchmark/raw/*;scripts/measure.py:20-85; numeric_cell_checks.csv','C recompute400timingmeanSD+quantiles; inspect timer boundary andmetadata','No fresh benchmark; metadata authenticity independent runtime conditions not recreated')
claim('CLIT01','P0268-P0280;T02;T17;P0709-P0712','Priorwork comparisons and publishednumbers','PENDING_D_PRIMARY_SOURCE_VERIFICATION','citation_inventory.csv; word_blocks.csv','All claim locations extracted; protocol separation inspected','No external citation correctness inferred from DOI existence')
claim('CAPP01','P0476-P0528;T08;T09;P0724;P0772-P0779','App architecture/contracts/tests/models/FP32','PARTIAL_STATIC_AND_HISTORICAL_EVIDENCE_PENDING_E','../../Ung_Dung/polypweb; .codex_revision_20261016/{test_status,smoke_results}.json','Read report, compare source main.py/manifest and retained logs','C002 maskcount contradiction; E checks real application; not all-suite rerun by C')
claim('CSCOPE01','P0277-P0280;P0550-P0555;P0714-P0731;T19','No topology/clinical/equivalence claims; externaltest/ablation future','APPROPRIATELY_LIMITED_AS_WRITTEN','FullmainWord; current20seed package','Inspect all chapters, conclusions and appendices','Future work is not evidence it has been executed')
claim('CINTEGRITY01','P0733-P0756;whole report','Citation attribution and similarity risk','NOT_A_TURNITIN_ASSESSMENT','citation_inventory.csv; issuesC008-C011','Reference inventory and localversion distinction','Cannot give similarity%; report/settings/submissionhistory absent; no upload')
for row in cellchecks:
    claim('CELL-'+str(len(ledger)+1).zfill(4),row['word_id'],row['field']+': '+str(row['word_value']),row['status'],row['source'],'Numeric display-rounding check','Numeric correctness does not establish raw experiment provenance')
writecsv('claim_evidence.csv',ledger)

# Preserve every block as a review coverage ledger; this is not a blanket PASS.
coverage=[]
for r in blocks:
    if not r['text'].strip():continue
    if r['kind']=='table_row':group='table examined; numeric rows separately tested; literature/app delegated'
    elif r['id'].startswith('P') and int(r['id'][1:])<205:group='frontmatter/navigation; factual biographies not independently authenticated'
    elif r['kind']=='reference':group='citation inventory, D verification pending'
    elif r['kind']=='figure_caption':group='text reviewed, visual content and Word mapping delegated B'
    else:group='read and classified in chapter review; supporting scope in claim_evidence'
    coverage.append({'word_id':r['id'],'kind':r['kind'],'section':r['section'],'text':r['text'],'review_scope':group})
writecsv('full_block_review_coverage.csv',coverage)
writecsv('evidence_requests.csv',[
 {'owner':'D_literature','word_ids':'P0363;T02;T17;P0733-P0756','request':'Verify24references,880/120split provenance andpaper table numbers; compare close textual overlap where sourceavailable','status':'PENDING'},
 {'owner':'E_application','word_ids':'P0476-P0528;T09;P0772-P0779','request':'Confirm runtime vsmock history;51/261/498testcounts;TSVMsmoke2masks vsWord1;endpoint/precision','status':'PENDING'},
 {'owner':'B_visual','word_ids':'P0517;P0519;P0393-P0436;P0562-P0699','request':'Map31figures,check Hình4.2 extraTSVMmask;inspect equations/diagrams,all numerics/caption context','status':'IN_PROGRESS'},
 {'owner':'root','word_ids':'P0353;P0377;P0384;P0388;P0447','request':'If feasible reprocess1000masks:Otsu5-8,1206contours/143removed,333.2->24.6vertices,polygon reproduction;Cverified image dimensions only','status':'PENDING'}])
manifest={'word_sha256':hashlib.sha256((ROOT/'Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx').read_bytes()).hexdigest(),
 'reviewed_paragraphs':783,'tables':19,'references':24,'numeric_cell_checks':len(cellchecks),'numeric_cell_mismatches':sum(r['status']=='MISMATCH' for r in cellchecks),
 'config_field_checks':len(configchecks),'config_field_mismatches':sum(r['status']=='MISMATCH' for r in configchecks),'epoch_selection_disagreements':sum(epoch),
 'original_files_edited':False,'training':False,'inference':False,'external_upload':False}
(OUT/'review_summary.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False))
