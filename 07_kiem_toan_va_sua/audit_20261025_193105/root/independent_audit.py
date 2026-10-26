"""Read-only independent audit; writes only in this audit's root directory."""
from pathlib import Path
import argparse, csv, hashlib, json, math, statistics, sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(2**20), b''):
            h.update(b)
    return h.hexdigest()

def snapshot():
    files = []
    for name in ['Ket_Qua_V2/KetQua_Nen', 'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32',
                 'Ket_Qua_V2/KQ_Nen_DX_10seed', 'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20',
                 'Bao_cao', 'doc', 'ultralytics_Topology-Shape-aware_VMamba_FP32',
                 'ultralytics_Topology-Shape-aware VMamba', 'Cell Kaggle', 'Stracth/Bao_Cao']:
        for p in (ROOT/name).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:
                files.append(p)
    for p in (ROOT.parents[1]/'TLTK').glob('*'):
        if p.is_file() and not p.name.startswith('~$'):
            files.append(p)
    app = ROOT.parents[1]/'Ung_Dung/polypweb'
    excluded = {'.git', '.venv', 'venv', 'node_modules', 'build', 'target', '.dart_tool', '__pycache__', 'storage', '.pytest_cache'}
    for p in app.rglob('*'):
        if p.is_file() and not excluded.intersection(p.relative_to(app).parts) and p.suffix.lower() in {'.py','.java','.dart','.yaml','.yml','.xml','.html','.js','.css','.md','.json','.txt','.pt'}:
            files.append(p)
    records = [{'path': str(p.resolve()), 'bytes':p.stat().st_size, 'sha256':digest(p)} for p in sorted(set(files))]
    (HERE/'source_before.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Snapshot files',len(records),'bytes',sum(x['bytes'] for x in records),flush=True)

def numeric():
    models = [('Baseline','YOLOv26s-seg','Kvasir_BG20_Baseline_YOLO26s_seg'),
              ('TSVM','Kvasir_BG20_YOLO26s_seg_TSVM_FP32','Kvasir_BG20_YOLO26s_seg_TSVM_FP32')]
    results = {}; selected=[]
    for model,parent,prefix in models:
        results[model]=[]
        for seed in range(20):
            p=ROOT/'Ket_Qua_V2/KetQua_Nen'/parent/f'{prefix}_s{seed}_w2/results.csv'
            with p.open(encoding='utf-8-sig') as f:
                rows=[{k.strip():float(v) for k,v in r.items()} for r in csv.DictReader(f)]
            assert [r['epoch'] for r in rows]==list(range(1,101))
            assert all(math.isfinite(v) for r in rows for v in r.values())
            mask=max(rows,key=lambda r:r['metrics/mAP50-95(M)'])
            fitness=max(rows,key=lambda r:r['metrics/mAP50-95(M)']+r['metrics/mAP50-95(B)'])
            results[model].append((mask,fitness))
            selected.append({'model':model,'seed':seed,'max_mask_epoch':int(mask['epoch']),'max_fitness_epoch':int(fitness['epoch']),
                             'mask_AP_at_max_mask':mask['metrics/mAP50-95(M)'],'mask_AP_at_max_fitness':fitness['metrics/mAP50-95(M)']})
    summary=[]
    for rule in [0,1]:
        a=[r[rule]['metrics/mAP50-95(M)'] for r in results['Baseline']]
        b=[r[rule]['metrics/mAP50-95(M)'] for r in results['TSVM']]
        d=[y-x for x,y in zip(a,b)];se=statistics.stdev(d)/math.sqrt(20);t=statistics.mean(d)/se
        df=19;c=math.exp(math.lgamma(10)-math.lgamma(9.5))/math.sqrt(df*math.pi)
        f=lambda x:c*(1+x*x/df)**(-10)
        end=abs(t);n=20000;h=end/n
        integ=h/3*(f(0)+f(end)+sum((4 if i%2 else 2)*f(i*h) for i in range(1,n)))
        summary.append({'rule':['max_mask','max_box_plus_mask'][rule],'baseline_mean':statistics.mean(a),'baseline_sd':statistics.stdev(a),
                        'tsvm_mean':statistics.mean(b),'tsvm_sd':statistics.stdev(b),'delta':statistics.mean(d),
                        'paired_t':t,'two_sided_p_numerical_integral':1-2*integ,
                        'CI95':[statistics.mean(d)-2.093024054408263*se,statistics.mean(d)+2.093024054408263*se],
                        'tsvm_wins':sum(x>0 for x in d)})
    (HERE/'numeric_independent.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    with (HERE/'epoch_selection_independent.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=selected[0]);w.writeheader();w.writerows(selected)
    print(json.dumps(summary,indent=2),flush=True)

def dataset():
    base=ROOT/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20';out={};hashes=[]
    for split in ['train','val']:
        ims=[p for p in (base/'images'/split).glob('*') if p.is_file()]
        labs=list((base/'labels'/split).glob('*.txt'));bad=[];n=0;empty=0
        for p in labs:
            lines=p.read_text().splitlines();empty+=not any(s.strip() for s in lines)
            for line in lines:
                if not line.strip():continue
                v=line.split();n+=1
                if len(v)<7 or len(v)%2!=1 or v[0]!='0' or not all(math.isfinite(float(x)) and 0<=float(x)<=1 for x in v[1:]):bad.append(p.name)
        hashes.append({digest(p) for p in ims})
        out[split]={'images':len(ims),'labels':len(labs),'empty':empty,'instances':n,'invalid_labels':bad,
                    'missing_labels':sorted({p.stem for p in ims}-{p.stem for p in labs}),
                    'orphan_labels':sorted({p.stem for p in labs}-{p.stem for p in ims})}
    out['exact_image_hash_overlap']=len(hashes[0]&hashes[1])
    out['root_data_yaml_path_exists']=(ROOT/'Kvasir_YOLO_SEG_BG20').exists()
    out['actual_data_path']=str(base)
    (HERE/'dataset_independent.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))

def verify():
    records=json.loads((HERE/'source_before.json').read_text(encoding='utf-8'));changed=[]
    for r in records:
        p=Path(r['path'])
        if not p.exists() or digest(p)!=r['sha256']:changed.append(r['path'])
    out={'checked':len(records),'changed_or_missing':changed}
    (HERE/'source_after_check.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(out)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['snapshot','numeric','dataset','verify']);a=parser.parse_args()
    {'snapshot':snapshot,'numeric':numeric,'dataset':dataset,'verify':verify}[a.mode]()
