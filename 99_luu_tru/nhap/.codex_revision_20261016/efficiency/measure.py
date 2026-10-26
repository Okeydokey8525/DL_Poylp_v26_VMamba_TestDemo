"""Actual single-process-per-checkpoint CPU FP32 benchmark; no training."""
from pathlib import Path
import os,sys,json,csv,time,gc,platform,hashlib,subprocess
R=next(p for p in Path(__file__).resolve().parents if (p/'ultralytics').is_dir() and (p/'Ket_Qua_V2').is_dir())
OUT=R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/efficiency_benchmark'
APP=(R/'../../Ung_Dung/polypweb/polypweb/ai-service').resolve()
for folder in ['raw','tables','reports','figures']:(OUT/folder).mkdir(parents=True,exist_ok=True)
os.environ['OMP_NUM_THREADS']='4';os.environ['MKL_NUM_THREADS']='4'
sys.path.insert(0,str(APP))
import main,torch,numpy as np,psutil,ultralytics
from PIL import Image
from ultralytics.utils import LOGGER
LOGGER.setLevel('ERROR')
torch.set_num_threads(4);torch.set_num_interop_threads(1)
torch.manual_seed(0);np.random.seed(0)
label=sys.argv[1];key='YOLO26s-seg' if label=='baseline' else 'YOLO26s-TSVM-FP32-seg'
proc=psutil.Process();rss_start=proc.memory_info().rss
cfg=main.MODEL_CONFIG[key];rt=main.load_model_runtime(key,cfg,'cpu')
assert rt.status=='ready',rt.error
yolo=rt.model
params=sum(p.numel() for p in yolo.model.parameters())
param_bytes=sum(p.numel()*p.element_size() for p in yolo.model.parameters())
buffer_bytes=sum(p.numel()*p.element_size() for p in yolo.model.buffers())
floating={}
for tensor in yolo.model.state_dict().values():
    if tensor.is_floating_point():
        assert tensor.dtype==torch.float32 and bool(torch.isfinite(tensor).all())
        floating[str(tensor.dtype)]=floating.get(str(tensor.dtype),0)+1
source=R/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/images/val'
paths=sorted(p for p in source.iterdir() if not p.name.startswith('bg_'))[:10]+sorted(p for p in source.iterdir() if p.name.startswith('bg_'))[:10]
imgs=[Image.open(p).convert('RGB') for p in paths]
kwargs=dict(imgsz=640,device='cpu',half=False,rect=False,batch=1,conf=0.25,iou=0.7,max_det=300,verbose=False,save=False)
rss_samples=[rss_start,proc.memory_info().rss]
with torch.inference_mode():
    # The first pipeline call sets up AutoBackend and applies standard Conv-BN fusion.
    first=yolo.predict(source=imgs[0],**kwargs)
    # AutoBackend resets CPU threads during setup; enforce protocol after setup.
    torch.set_num_threads(4)
    assert torch.get_num_threads()==4
    tensor=yolo.predictor.preprocess([np.asarray(imgs[0])[:,:,::-1].copy()])
    assert tuple(tensor.shape)==(1,3,640,640) and tensor.dtype==torch.float32
    assert not yolo.predictor.model.fp16
    rss_samples.append(proc.memory_info().rss)
    rows=[]
    for mode in ['forward_only','predict_pipeline']:
        for j in range(20):
            if mode=='forward_only': yolo.model(tensor)
            else:yolo.predict(source=imgs[j%20],**kwargs)
        for i in range(100):
            start=time.perf_counter_ns()
            if mode=='forward_only': result=yolo.model(tensor)
            else:result=yolo.predict(source=imgs[i%20],**kwargs)
            elapsed=(time.perf_counter_ns()-start)/1e6
            # Memory and output checks are outside the timed boundary.
            rss_samples.append(proc.memory_info().rss)
            row={'model':key,'mode':mode,'iteration':i+1,'image':paths[i%20].name if mode=='predict_pipeline' else paths[0].name,'latency_ms':elapsed}
            if mode=='predict_pipeline':
                pred=result[0]
                row.update(detections=len(pred.boxes),preprocess_ms=pred.speed['preprocess'],inference_ms=pred.speed['inference'],postprocess_ms=pred.speed['postprocess'])
                assert bool(torch.isfinite(pred.boxes.data).all())
                if pred.masks is not None: assert bool(torch.isfinite(pred.masks.data).all())
            rows.append(row)
        print(label,mode,'mean_ms',np.mean([r['latency_ms'] for r in rows if r['mode']==mode]),flush=True)
cpu_name=subprocess.check_output(['powershell','-NoProfile','-Command','(Get-CimInstance Win32_Processor).Name'],text=True).strip()
metadata={'model':key,'checkpoint':str(cfg.path),'sha256':rt.checkpoint_sha256,'checkpoint_bytes':cfg.path.stat().st_size,'seed':yolo.ckpt.get('train_args',{}).get('seed'),'parameters_unfused':params,'fp32_parameter_bytes_unfused':param_bytes,'buffer_bytes_unfused':buffer_bytes,'parameters_fused':sum(p.numel() for p in yolo.model.parameters()),'floating_state_dtypes_before_fusion':floating,'precision':'float32','autocast':False,'device':'cpu','cuda_available':torch.cuda.is_available(),'cuda_device_count':torch.cuda.device_count(),'cpu_name':cpu_name,'logical_cpus':psutil.cpu_count(),'physical_cpus':psutil.cpu_count(logical=False),'system_ram_bytes':psutil.virtual_memory().total,'python':sys.version,'torch':torch.__version__,'ultralytics':ultralytics.__version__,'ultralytics_path':ultralytics.__file__,'numpy':np.__version__,'os':platform.platform(),'threads':torch.get_num_threads(),'interop_threads':torch.get_num_interop_threads(),'warmups_per_mode':20,'measured_iterations_per_mode':100,'batch':1,'tensor_shape':list(tensor.shape),'rect':False,'conf':0.25,'iou':0.7,'max_det':300,'rss_process_before_model_bytes':rss_start,'rss_process_sample_max_bytes':max(rss_samples),'rss_delta_sample_max_bytes':max(rss_samples)-rss_start,'rss_metric':'sampled RSS, not allocator peak; process includes Python/PyTorch/loaded model/predictor/images','gflops':None,'gflops_reason':'No validated counting rule for custom parallel selective scan; THOP Conv-only totals would omit operations.','utc_finished':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'inputs':[{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'original_hw':[im.height,im.width]} for p,im in zip(paths,imgs)]}
(OUT/'raw'/f'{label}_environment.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
fields=['model','mode','iteration','image','latency_ms','detections','preprocess_ms','inference_ms','postprocess_ms']
with (OUT/'raw'/f'{label}_timings.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
print(label,'COMPLETE',flush=True)
