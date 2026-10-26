"""Inspect/validate existing trusted project checkpoints without altering source files."""
from pathlib import Path
import argparse, csv, gc, hashlib, importlib.util, json, os, shutil, sys, time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
os.environ['YOLO_CONFIG_DIR']=str(HERE/'ultralytics_settings')
os.environ['MPLCONFIGDIR']=str(HERE/'matplotlib_cache')
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('ultralytics',ROOT/'ultralytics_Topology-Shape-aware_VMamba_FP32/__init__.py',submodule_search_locations=[str(ROOT/'ultralytics_Topology-Shape-aware_VMamba_FP32')])
pkg=importlib.util.module_from_spec(spec);sys.modules['ultralytics']=pkg;spec.loader.exec_module(pkg)
import torch
from ultralytics import YOLO
torch.set_num_threads(4);torch.set_num_interop_threads(1)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def runs():
    for label,parent,prefix in [('Baseline','YOLOv26s-seg','Kvasir_BG20_Baseline_YOLO26s_seg'),('TSVM','Kvasir_BG20_YOLO26s_seg_TSVM_FP32','Kvasir_BG20_YOLO26s_seg_TSVM_FP32')]:
        for seed in range(20):
            p=ROOT/'Ket_Qua_V2/KetQua_Nen'/parent/f'{prefix}_s{seed}_w2'
            yield label,seed,p

def inventory():
    records=[]
    for label,seed,run in runs():
        p=run/'weights/best.pt';r={'model':label,'seed':seed,'path':str(p),'exists':p.exists()}
        if p.exists():
            try:
                ck=torch.load(p,map_location='cpu',weights_only=False)
                net=ck.get('ema') if ck.get('ema') is not None else ck['model']
                sd=net.state_dict();floating=[(k,v) for k,v in sd.items() if v.is_floating_point()]
                r.update(sha256=sha(p),bytes=p.stat().st_size,epoch=ck.get('epoch'),stored_version=ck.get('version'),date=ck.get('date'),
                         floating_dtypes=sorted({str(v.dtype) for k,v in floating}),
                         nonfinite=[k for k,v in floating if not torch.isfinite(v).all()],
                         layer10=type(net.model[10]).__name__,
                         layer5_conv_shape=list(net.model[5].conv.weight.shape),
                         layer6_output_channels=getattr(getattr(net.model[6],'cv2',None),'conv',None).out_channels if hasattr(getattr(net.model[6],'cv2',None),'conv') else None)
                if label=='TSVM':
                    r['bn10']={k:{'max_abs':float(v.float().abs().max()),'at_fp16_limit':int((v.float().abs()==65504).sum())} for k,v in sd.items() if 'model.10.m.0.fuse.bn.running_' in k}
                del ck,net,sd,floating;gc.collect()
            except Exception as e:r['error']=repr(e)
        records.append(r)
        (HERE/'checkpoint_inventory.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
        print(label,seed,r.get('floating_dtypes'),r.get('nonfinite'),r.get('error',''),flush=True)
    print('CHECKPOINT_INVENTORY_COMPLETE',len(records),flush=True)

def mirror():
    dst=HERE/'validation_dataset';src=ROOT/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20'
    for kind in ['images','labels']:
        target=dst/kind/'val';target.mkdir(parents=True,exist_ok=True)
        for p in (src/kind/'val').iterdir():
            if p.is_file() and p.suffix.lower() in {'.jpg','.jpeg','.png','.txt'}:
                if not (target/p.name).exists():shutil.copyfile(p,target/p.name)
    data=HERE/'validation_data.yaml'
    data.write_text('path: '+dst.as_posix()+'\ntrain: images/val\nval: images/val\nnames:\n  0: polyp\n',encoding='utf-8')
    return data

def validate(limit,model_filter=None):
    data=mirror();out=HERE/('checkpoint_validation_rect16_'+model_filter+'.jsonl' if model_filter else 'checkpoint_validation_rect16.jsonl')
    done={(r['model'],r['seed']) for r in [json.loads(l) for l in out.read_text().splitlines()]} if out.exists() else set()
    n=0
    for label,seed,run in runs():
        if model_filter and label!=model_filter:continue
        if (label,seed) in done:continue
        if limit and n>=limit:break
        n+=1;p=run/'weights/best.pt';r={'model':label,'seed':seed,'checkpoint_sha256':sha(p),'runtime_ultralytics':str(pkg.__file__),'torch':torch.__version__,'threads':4,'batch':16,'imgsz':640,'half':False,'rect':True,'data':str(data)}
        t=time.monotonic()
        try:
            with (run/'results.csv').open(encoding='utf-8-sig') as f:rows=[{k.strip():float(v) for k,v in row.items()} for row in csv.DictReader(f)]
            expected=max(rows,key=lambda row:row['metrics/mAP50-95(B)']+row['metrics/mAP50-95(M)'])
            model=YOLO(str(p));model.model.float()
            metrics=model.val(data=str(data),device='cpu',batch=16,imgsz=640,workers=0,half=False,rect=True,plots=False,save_json=False,save_txt=False,project=str(HERE/'revalidation'),name=f'{label}_s{seed}_rect16',exist_ok=True,verbose=False)
            r.update(actual={k:float(v) for k,v in metrics.results_dict.items()},expected_fitness_epoch=int(expected['epoch']),
                     expected={k:expected[k] for k in ['metrics/mAP50-95(M)','metrics/mAP50(M)','metrics/mAP50-95(B)','metrics/mAP50(B)']})
            r['deltas']={k:r['actual'][k]-v for k,v in r['expected'].items()}
            r['mask_AP_difference_over_0_005']=any(abs(r['deltas'][k])>.005 for k in ['metrics/mAP50-95(M)','metrics/mAP50(M)'])
            del model,metrics;gc.collect()
        except Exception as e:r['error']=repr(e)
        r['seconds']=time.monotonic()-t
        with out.open('a',encoding='utf-8') as f:f.write(json.dumps(r)+'\n')
        print('VALIDATION_COMPLETE',json.dumps(r),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['inventory','validate']);parser.add_argument('--limit',type=int,default=0);parser.add_argument('--model',choices=['Baseline','TSVM']);args=parser.parse_args()
    inventory() if args.mode=='inventory' else validate(args.limit,args.model)
