from pathlib import Path
import sys,json,hashlib
R=next(p for p in Path(__file__).resolve().parents if (p/'ultralytics').is_dir() and (p/'Ket_Qua_V2').is_dir())
O=R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/efficiency_benchmark'
APP=(R/'../../Ung_Dung/polypweb/polypweb/ai-service').resolve();sys.path.insert(0,str(APP))
import main,torch
for k in ['baseline','tsvm']:
    path=O/'raw'/f'{k}_environment.json';m=json.loads(path.read_text(encoding='utf-8'))
    checkpoint=torch.load(m['checkpoint'],map_location='cpu',weights_only=False)
    net=checkpoint.get('ema') or checkpoint['model'];counts={}
    for v in net.state_dict().values():
        if v.is_floating_point():counts[str(v.dtype)]=counts.get(str(v.dtype),0)+1
    m['checkpoint_storage_floating_dtypes']=counts
    m['custom_module_sha256']=hashlib.sha256(main.VMAMBA_MODULE_PATH.read_bytes()).hexdigest()
    m['custom_module_path']=str(main.VMAMBA_MODULE_PATH)
    path.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
    print(k,counts)
    del checkpoint,net
