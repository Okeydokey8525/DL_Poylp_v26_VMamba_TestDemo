from pathlib import Path
import sys,json,time,hashlib
R=Path(__file__).resolve().parents[1];O=Path(__file__).parent
A=(R/'../../Ung_Dung/polypweb/polypweb/ai-service').resolve()
sys.path.insert(0,str(A))
import main,torch
from PIL import Image
torch.set_num_threads(4)
results=[]
source=R/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/images/val'
polyp=sorted(p for p in source.iterdir() if not p.name.startswith('bg_'))[0]
bg=sorted(p for p in source.iterdir() if p.name.startswith('bg_'))[0]
for key,cfg in main.MODEL_CONFIG.items():
    runtime=main.load_model_runtime(key,cfg,'cpu')
    assert runtime.status=='ready', runtime.error
    model=runtime.model
    dtype_counts={}
    for v in model.model.state_dict().values():
        if v.is_floating_point():
            assert torch.isfinite(v).all(),key
            assert v.dtype==torch.float32,(key,v.dtype)
            dtype_counts[str(v.dtype)]=dtype_counts.get(str(v.dtype),0)+1
    record={'key':key,'status':runtime.status,'sha256':runtime.checkpoint_sha256,'params':sum(p.numel() for p in model.model.parameters()),'floating_dtypes':dtype_counts,'seed':model.ckpt.get('train_args',{}).get('seed'),'task':model.task,'samples':[]}
    for label,p in [('polyp',polyp),('background',bg)]:
        # Same RGB decode as the API and fixed operational threshold, not a dataset evaluation.
        img=Image.open(p).convert('RGB')
        pred=main.run_inference(model,'cpu',img)
        import base64
        (O/f'overlay_{"baseline" if cfg.family=="baseline" else "tsvm"}_{label}.jpg').write_bytes(base64.b64decode(pred.pop('resultImageBase64')))
        record['samples'].append({'input':p.name,**pred})
    results.append(record)
    print(key,'ready',record['params'],'params',record['seed'],'seed',flush=True)
(O/'smoke_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('Four actual FP32 predictions complete. Not a throughput or accuracy benchmark.')
