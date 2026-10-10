"""Inspect and evaluate original TSVM checkpoints without editing source or weights."""
from __future__ import annotations
import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'archive/ultralytics_Topology-Shape-aware VMamba'
DATA = ROOT / 'archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20'
RUNS = ROOT / 'archive/Ket_Qua_V2/KetQua_XacThuc/best_and_last'

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')

def bootstrap(out):
    out = out.resolve()
    (out / 'config').mkdir(parents=True, exist_ok=True)
    os.environ['YOLO_CONFIG_DIR'] = str(out / 'config')
    os.environ['YOLO_AUTOINSTALL'] = 'false'
    os.environ['YOLO_OFFLINE'] = 'true'
    os.environ['MPLCONFIGDIR'] = str(out / 'mplconfig')
    os.environ['OMP_NUM_THREADS'] = '4'
    os.environ['MKL_NUM_THREADS'] = '4'
    spec = importlib.util.spec_from_file_location('ultralytics', PACKAGE / '__init__.py', submodule_search_locations=[str(PACKAGE)])
    module = importlib.util.module_from_spec(spec)
    sys.modules['ultralytics'] = module
    spec.loader.exec_module(module)
    import torch
    torch.set_num_threads(4)
    return torch, module

def checkpoint_path(seed, checkpoint):
    return RUNS / f'results {seed}/runs/Kvasir_BG20_YOLO26s_seg_TSVM_s{seed}_w2/weights/{checkpoint}.pt'

def inspect(seed, checkpoint, torch):
    p = checkpoint_path(seed, checkpoint)
    ck = torch.load(p, map_location='cpu', weights_only=False)
    model = (ck.get('ema') or ck['model']).float().eval()
    head = model.model[-1]
    nonfinite = []
    saturated = []
    large_buffers = []
    for name, value in model.state_dict().items():
        if value.is_floating_point() and not torch.isfinite(value).all():
            nonfinite.append(name)
        if value.is_floating_point() and value.numel():
            count = int((value.abs() >= 65504).sum())
            if count:
                saturated.append({'tensor':name,'count':count,'size':value.numel(),'max_abs':float(value.abs().max())})
            if name.endswith('running_var') and float(value.max()) > 10000:
                large_buffers.append({'tensor':name,'min':float(value.min()),'max':float(value.max()),'median':float(value.median())})
    with (p.parent.parent / 'results.csv').open(encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    # Local source checkpoint selection uses summed Box/Mask mAP50-95 fitness.
    best_fitness_row = max(rows, key=lambda r: float(r['metrics/mAP50-95(B)']) + float(r['metrics/mAP50-95(M)']))
    result = {'seed':seed, 'checkpoint':checkpoint, 'path':str(p), 'sha256':digest(p),
              'version':ck.get('version'), 'date':ck.get('date'), 'epoch':ck.get('epoch'),
              'train_metrics':ck.get('train_metrics'), 'best_fitness':ck.get('best_fitness'),
              'csv_fitness_best_epoch':int(best_fitness_row['epoch']),
              'csv_fitness_best_metrics':{k:float(v) for k,v in best_fitness_row.items() if k.startswith('metrics/')},
              'csv_last_metrics':{k:float(v) for k,v in rows[-1].items() if k.startswith('metrics/')},
              'head':type(head).__name__, 'end2end':bool(head.end2end), 'reg_max':head.reg_max,
              'head_attributes':{k:str(getattr(head,k,None)) for k in ['_end2end','xyxy','shape','stride','nc','nm','max_det']},
              'nonfinite_state_tensors':nonfinite,
              'fp16_limit_state_tensors':saturated, 'large_bn_variances':large_buffers,
              'parameters':sum(p.numel() for p in model.parameters())}
    return model, result

def smoke(model, torch):
    import cv2
    from ultralytics.data.augment import LetterBox
    names = ['cju0s690hkp960855tjuaqvv0.jpg']
    positive = sorted(p for p in (DATA/'images/val').glob('*.jpg') if not p.name.startswith('bg_'))
    if not (DATA/'images/val'/names[0]).exists():
        names = [positive[0].name]
    names += [positive[len(positive)//2].name, sorted((DATA/'images/val').glob('bg_*.jpg'))[0].name]
    images = []
    for name in names:
        bgr = cv2.imread(str(DATA/'images/val'/name))
        rgb = LetterBox(new_shape=(640,640), auto=False)(image=bgr)[...,::-1].copy()
        images.append(torch.from_numpy(rgb).permute(2,0,1).float()/255)
    x = torch.stack(images)
    h = model.model[-1]
    h.end2end = True
    start = time.perf_counter()
    bn_input = {}
    target_bn = model.get_submodule('model.10.m.0.fuse.bn')
    def capture_bn(module, inputs):
        t = inputs[0].double()
        means = t.mean((0,2,3))
        variances = t.var((0,2,3),unbiased=False)
        bn_input.update({'activation_min':float(t.min()),'activation_max':float(t.max()),
                         'channel_mean_min':float(means.min()),'channel_mean_max':float(means.max()),
                         'channel_variance_min':float(variances.min()),'channel_variance_max':float(variances.max())})
    hook = target_bn.register_forward_pre_hook(capture_bn)
    with torch.inference_mode():
        original = model(x)
        hook.remove()
        raw = original[1]
        h.end2end = False
        many_decoded = h._inference(raw['one2many'])
        h.end2end = True
        fused = copy.deepcopy(model)
        fused.fuse(verbose=False)
        fused_output = fused(x)
    result = {'images':names, 'seconds':time.perf_counter()-start, 'heads':{}, 'affected_bn_input':bn_input,
              'one_fused_raw_box_max_difference':float((fused_output[1]['one2one']['boxes']-raw['one2one']['boxes']).abs().max()),
              'one_fused_raw_score_logit_max_difference':float((fused_output[1]['one2one']['scores']-raw['one2one']['scores']).abs().max()),
              'one_fused_max_absolute_output_difference':float((fused_output[0][0]-original[0][0]).abs().max()),
              'one_fused_vs_unfused_max_conf_difference':float((fused_output[0][0][...,4]-original[0][0][...,4]).abs().max())}
    for key in ('one2one','one2many'):
        values = raw[key]['scores'].sigmoid()
        result['heads'][key] = {'max_conf_per_image':values.flatten(1).max(1).values.tolist(),
                                'anchors_conf_above_025':(values > .25).flatten(1).sum(1).tolist(),
                                'raw_box_min':float(raw[key]['boxes'].min()), 'raw_box_max':float(raw[key]['boxes'].max())}
    result['many_decoded_box_range'] = [float(many_decoded[:,:4].min()),float(many_decoded[:,:4].max())]
    return result

def calibrate_bn_from_train(model, torch, out, image_count=128, batch_size=4):
    """Diagnostic derived model: estimate only damaged BN buffers from TRAIN images."""
    import cv2
    import random
    from ultralytics.data.augment import LetterBox
    paths = sorted((DATA/'images/train').glob('*.jpg'))
    random.Random(42).shuffle(paths)
    paths = paths[:image_count]
    bn = model.get_submodule('model.10.m.0.fuse.bn')
    old_mean, old_var = bn.running_mean.clone(), bn.running_var.clone()
    count, mean, m2 = 0, None, None
    class Captured(Exception):
        pass
    def capture(module, inputs):
        nonlocal count,mean,m2
        t = inputs[0].double()
        n = t.shape[0]*t.shape[2]*t.shape[3]
        cur_mean = t.mean((0,2,3))
        cur_m2 = t.var((0,2,3),unbiased=False)*n
        if mean is None:
            mean,m2,count = cur_mean,cur_m2,n
        else:
            delta = cur_mean-mean
            m2 = m2+cur_m2+delta.square()*(count*n/(count+n))
            mean = mean+delta*(n/(count+n))
            count += n
        raise Captured()
    hook = bn.register_forward_pre_hook(capture)
    start = time.perf_counter()
    try:
        with torch.inference_mode():
            for offset in range(0,len(paths),batch_size):
                images = []
                for p in paths[offset:offset+batch_size]:
                    im = LetterBox(new_shape=(640,640),auto=False)(image=cv2.imread(str(p)))[...,::-1].copy()
                    images.append(torch.from_numpy(im).permute(2,0,1).float()/255)
                try:
                    model(torch.stack(images))
                except Captured:
                    pass
                print(f'BN calibration TRAIN {min(offset+batch_size,len(paths))}/{len(paths)}',flush=True)
    finally:
        hook.remove()
    bn.running_mean.copy_(mean.float())
    bn.running_var.copy_((m2/(count-1)).float())
    result = {'purpose':'causal diagnostic, NOT recovery of original FP32 EMA statistics',
              'layer':'model.10.m.0.fuse.bn','split':'train','random_seed':42,'images':len(paths),'batch':batch_size,
              'imgsz':640,'rect':False,'weights_optimized':False,'seconds':time.perf_counter()-start,
              'old_mean':old_mean.tolist(),'old_var':old_var.tolist(),
              'new_mean':bn.running_mean.tolist(),'new_var':bn.running_var.tolist(),
              'calibration_images':[p.name for p in paths]}
    write(out/'bn_calibration.json',result)
    return result

def validate_pair(model, out, torch, batch_size=4, box_only=False):
    """One backbone pass per batch; evaluate both native heads independently."""
    from ultralytics.models.yolo.segment import SegmentationValidator
    from ultralytics.models.yolo.detect import DetectionValidator
    from ultralytics.utils.metrics import ConfusionMatrix
    import yaml
    data_yaml = out / 'data.yaml'
    data_yaml.write_text(yaml.safe_dump({'path':str(DATA), 'train':'images/train','val':'images/val','names':{0:'polyp'}}),encoding='utf-8')
    import ultralytics.data.utils as data_utils
    # Font downloading affects presentation only; keep the audit offline.
    data_utils.check_font = lambda *a, **k: None
    check_det_dataset = data_utils.check_det_dataset
    data = check_det_dataset(str(data_yaml))
    validators = {}
    cms = {}
    img_counts = {}
    per_image = {}
    head = model.model[-1]
    for kind in ('one','many'):
        head.end2end = kind == 'one'
        validator_class = DetectionValidator if box_only else SegmentationValidator
        v = validator_class(save_dir=out/kind, args={'data':str(data_yaml), 'batch':batch_size,'imgsz':640,'device':'cpu',
                                  'workers':0,'plots':False,'conf':0.001,'iou':0.7,'half':False,'rect':True,
                                  'save_json':False,'save_txt':False})
        if box_only:
            v.args.task = 'segment'  # preserve mask-coefficient channels and polygon dataset, measure only boxes
        v.device = torch.device('cpu')
        v.stride = max(int(model.stride.max()), 32)
        v.data = data
        v.training = False
        v.init_metrics(model)
        validators[kind] = v
        cms[kind] = ConfusionMatrix(names={0:'polyp'},task='detect')
        img_counts[kind] = {'tp':0,'fn':0,'fp':0,'tn':0}
        per_image[kind] = []
    loader = validators['one'].get_dataloader(data['val'],batch_size)
    head.end2end = True
    start = time.perf_counter()
    with torch.inference_mode():
        for bi,batch in enumerate(loader):
            batch = validators['one'].preprocess(batch)
            output = model(batch['img'])
            raw = output[1]
            head.end2end = False
            decoded_many = head._inference(raw['one2many'])
            head.end2end = True
            outputs = {'one':output[0], 'many':(decoded_many,output[0][1])}
            for kind,v in validators.items():
                v.batch_i = bi
                predictions = v.postprocess(outputs[kind][0] if box_only else outputs[kind])
                v.update_metrics(predictions,batch)
                for i,pred in enumerate(predictions):
                    target = v._prepare_batch(i,batch)
                    cms[kind].process_batch(pred,target,conf=.25,iou_thres=.45)
                    actual = len(target['cls']) > 0
                    n = int((pred['conf'] > .25).sum())
                    decision = n > 0
                    cell = 'tp' if actual and decision else 'fn' if actual else 'fp' if decision else 'tn'
                    img_counts[kind][cell] += 1
                    per_image[kind].append({'image':str(target['im_file']), 'gt_instances':len(target['cls']),
                                           'detections_above_025':n, 'max_conf':float(pred['conf'].max()) if len(pred['conf']) else 0})
            print(f'batch {bi+1}/{len(loader)} elapsed={time.perf_counter()-start:.1f}s',flush=True)
    result = {'protocol':{'confidence_ap':.001,'confidence_cm':.25,'box_iou_cm':.45,'nms_iou':.7,'imgsz':640,
                          'batch':batch_size,'rect':True,'half':False,'fused':False,'device':'cpu','shared_backbone_pass':True,
                          'box_only':box_only},
              'seconds':time.perf_counter()-start, 'heads':{}}
    for kind,v in validators.items():
        metrics = v.get_stats()
        result['heads'][kind] = {'metrics':{k:float(x) for k,x in metrics.items()}, 'object_cm':cms[kind].matrix.tolist(),
                                 'image_cm':img_counts[kind], 'per_image':per_image[kind]}
    return result

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--seeds',nargs='+',type=int,default=[0,5,8])
    ap.add_argument('--checkpoints',nargs='+',choices=['best','last'],default=['best','last'])
    ap.add_argument('--mode',choices=['inspect','smoke','validate'],default='smoke')
    ap.add_argument('--batch',type=int,default=4)
    ap.add_argument('--calibrate-train',type=int,default=0,help='Diagnostic only: recalibrate damaged BN on N training images')
    ap.add_argument('--box-only',action='store_true',help='Full dataset box AP and CM; skip pixel mask operations')
    ap.add_argument('--apply-calibration',type=Path,help='Apply previously measured TRAIN-only BN statistics to the same checkpoint')
    args = ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    torch,ultralytics = bootstrap(args.out)
    source_hash = hashlib.sha256()
    for p in sorted(PACKAGE.rglob('*.py')):
        source_hash.update(p.relative_to(PACKAGE).as_posix().encode())
        source_hash.update(bytes.fromhex(digest(p)))
    environment = {'python':sys.version,'torch':torch.__version__,'ultralytics':ultralytics.__version__,
                   'source_sha256':source_hash.hexdigest(),'source_path':str(PACKAGE),'mode':args.mode}
    write(args.out/'environment.json',environment)
    for seed in args.seeds:
        for checkpoint in args.checkpoints:
            print(f'Loading seed={seed} checkpoint={checkpoint}',flush=True)
            model,result = inspect(seed,checkpoint,torch)
            folder = args.out / f'seed{seed}_{checkpoint}'
            write(folder/'inspection.json',result)
            if args.calibrate_train:
                result['bn_calibration'] = calibrate_bn_from_train(model,torch,folder,args.calibrate_train,args.batch)
            if args.apply_calibration:
                cal = json.loads(args.apply_calibration.read_text(encoding='utf-8'))
                original = json.loads((args.apply_calibration.parent/'inspection.json').read_text(encoding='utf-8'))
                if original['sha256'] != result['sha256'] or cal['split'] != 'train':
                    raise ValueError('Calibration must come from TRAIN and this exact checkpoint')
                bn = model.get_submodule(cal['layer'])
                bn.running_mean.copy_(torch.tensor(cal['new_mean'],dtype=torch.float32))
                bn.running_var.copy_(torch.tensor(cal['new_var'],dtype=torch.float32))
                result['bn_calibration'] = cal
                torch.save({'model':copy.deepcopy(model).float(),'train_args':getattr(model,'args',{}),
                            'epoch':-1,'train_metrics':None,'version':ultralytics.__version__,
                            'diagnostic_only':True,'source_checkpoint_sha256':result['sha256'],
                            'bn_calibration':cal},folder/'diagnostic_bn_recalibrated_fp32.pt')
            if args.mode == 'smoke':
                result['smoke'] = smoke(model,torch)
                write(folder/'smoke.json',result)
                print(json.dumps(result['smoke'],ensure_ascii=False),flush=True)
            elif args.mode == 'validate':
                result['validation'] = validate_pair(model,folder,torch,args.batch,args.box_only)
                write(folder/'validation.json',result)
                print(json.dumps({k:{'metrics':v['metrics'],'object_cm':v['object_cm'],'image_cm':v['image_cm']} for k,v in result['validation']['heads'].items()}),flush=True)
            if digest(checkpoint_path(seed,checkpoint)) != result['sha256']:
                raise RuntimeError('Checkpoint changed on disk')
    print('Finished. Original checkpoint hashes unchanged.',flush=True)

if __name__ == '__main__':
    main()
