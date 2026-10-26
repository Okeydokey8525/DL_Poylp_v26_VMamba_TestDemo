from pathlib import Path
import shutil,json,hashlib,re
R=Path(__file__).resolve().parents[1]; O=Path(__file__).parent
A=(R/'../../Ung_Dung/polypweb').resolve(); service=A/'polypweb/ai-service'
backup=O/'app_backup'; manifest=[]
suffixes={'.py','.java','.html','.dart','.md','.properties','.json','.yml','.yaml'}
skip={'.git','.venv','build','target','.dart_tool','.idea','node_modules','runs','__pycache__','.agents','.codex'}
for p in A.rglob('*'):
    if not p.is_file() or any(x in skip for x in p.relative_to(A).parts):continue
    if p.suffix not in suffixes and not p.name.startswith('.env'):continue
    text=p.read_text(encoding='utf-8-sig',errors='strict')
    new=text.replace('YOLO26n-VMamba-seg','YOLO26s-TSVM-FP32-seg').replace('YOLO26n-seg + VMamba','YOLO26s-seg + TSVM FP32').replace('YOLO26n-seg','YOLO26s-seg').replace('yolo26n-vmamba-seg-best.pt','yolo26s-tsvm-fp32-best.pt').replace('yolo26n-seg-best.pt','yolo26s-seg-best.pt')
    if new!=text:
        b=backup/p.relative_to(A);b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b)
        p.write_text(new,encoding='utf-8');manifest.append(str(p.relative_to(A)))
source=R/'ultralytics_Topology-Shape-aware_VMamba_FP32/nn/modules/topology_shape_vmamba.py'
shutil.copy2(source,service/'custom_ultralytics/topology_shape_vmamba.py')
main=service/'main.py';text=main.read_text(encoding='utf-8')
start=text.index('VMAMBA_MODULE_PATH =');end=text.index('\n\nVMAMBA_MODULE_ERROR:',start)
text=text[:start]+'''VMAMBA_MODULE_PATH = BASE_DIR / "custom_ultralytics" / "topology_shape_vmamba.py"


def register_vmamba_module() -> None:
    """Register the exact TSVM classes referenced by the FP32 experiment checkpoint."""
    import ultralytics.nn.modules as modules_package
    import ultralytics.nn.tasks as tasks_package

    module_name = "ultralytics.nn.modules.topology_shape_vmamba"
    if module_name in sys.modules:
        tsvm_module = sys.modules[module_name]
    else:
        if not VMAMBA_MODULE_PATH.is_file():
            raise RuntimeError(f"TSVM module was not found: {VMAMBA_MODULE_PATH}")
        spec = importlib.util.spec_from_file_location(module_name, VMAMBA_MODULE_PATH)
        if spec is None or spec.loader is None:
            raise RuntimeError("Could not create the TSVM module specification")
        tsvm_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = tsvm_module
        try:
            spec.loader.exec_module(tsvm_module)
        except Exception:
            sys.modules.pop(module_name, None)
            raise
    setattr(modules_package, "topology_shape_vmamba", tsvm_module)
    for name in ("C2TSVMamba", "TSVMamba", "SS2D", "ShapeAwareBranch",
                 "DirectionalShapeExtractor", "TopologyShapeGate"):
        setattr(modules_package, name, getattr(tsvm_module, name))
        setattr(tasks_package, name, getattr(tsvm_module, name))
''' +text[end:]
text=text.replace('        model.to(device)\n','        model.to(device)\n        model.model.float()  # Preserve FP32 for the TSVM state-space and BatchNorm path.\n        if config.family == "vmamba" and not any(\n            type(layer).__name__ == "C2TSVMamba" for layer in model.model.modules()\n        ):\n            raise RuntimeError("research checkpoint does not contain C2TSVMamba")\n')
text=text.replace('        device=device,\n        verbose=False,','        device=device,\n        half=False,\n        verbose=False,')
text=text.replace('Real baseline and VMamba segmentation service for PolypVision stage 3D.','YOLO26s-seg and Topology-Shape-aware VMamba FP32 segmentation service.')
main.write_text(text,encoding='utf-8')
req=service/'requirements.txt';b=backup/req.relative_to(A);b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(req,b)
req.write_text(req.read_text().replace('ultralytics==8.4.103','ultralytics==8.4.127'),encoding='utf-8');manifest.append(str(req.relative_to(A)))
items=[]
for key,relative,dest in [
    ('YOLO26s-seg','YOLOv26s-seg/Kvasir_BG20_Baseline_YOLO26s_seg_s0_w2','yolo26s-seg-best.pt'),
    ('YOLO26s-TSVM-FP32-seg','Kvasir_BG20_YOLO26s_seg_TSVM_FP32/Kvasir_BG20_YOLO26s_seg_TSVM_FP32_s0_w2','yolo26s-tsvm-fp32-best.pt')]:
    src=R/'Ket_Qua_V2/KetQua_Nen'/relative/'weights/best.pt';dst=service/'models'/dest
    shutil.copy2(src,dst)
    items.append({'model_key':key,'seed':0,'selection':'existing best.pt selected by Ultralytics box+mask fitness; not the max-mask summary epoch','source_run':relative,'file':dest,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'bytes':dst.stat().st_size,'inference_precision':'float32'})
(service/'models/experiment_manifest.json').write_text(json.dumps({'experiment':'Kvasir BG20 20 seeds FP32','models':items},ensure_ascii=False,indent=2),encoding='utf-8')
(O/'app_migration.json').write_text(json.dumps({'root':str(A),'changed_files':manifest,'checkpoints':items},ensure_ascii=False,indent=2),encoding='utf-8')
print('Updated',len(manifest),'source/config/test files; checkpoint selection fixed at seed 0 for both models.')
