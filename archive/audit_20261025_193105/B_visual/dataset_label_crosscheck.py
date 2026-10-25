"""Independent one-label replay and raster comparison; source is never modified."""
import ast,json,sys,hashlib
from pathlib import Path
import cv2,numpy as np
sys.stdout.reconfigure(encoding='utf-8')
O=Path(__file__).resolve().parent;R=O.parents[1]
source=R/'Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py'
tree=ast.parse(source.read_text(encoding='utf-8'))
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='convert_mask_to_yolo_polygons')
fn.returns=None
for arg in fn.args.args:arg.annotation=None
ns={'cv2':cv2,'np':np,'Path':Path}
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(source),'exec'),ns)
name='ck2bxiswtxuw80838qkisqjwz'
maskpath=R/'Ket_Qua_V2/Data Prosessing/Kvasir-SEG/masks'/f'{name}.jpg'
stored=(R/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/labels/val'/f'{name}.txt').read_text()
lines,_,(w,h)=ns['convert_mask_to_yolo_polygons'](maskpath);replayed=''.join(lines)
def raster(text):
    canvas=np.zeros((h,w),np.uint8)
    for line in text.splitlines():
        coords=np.array(list(map(float,line.split()[1:]))).reshape(-1,2)
        poly=np.rint(coords*np.array([w,h])).astype(np.int32)
        cv2.fillPoly(canvas,[poly],1)
    return canvas.astype(bool)
a=raster(stored);b=raster(replayed)
pts_a=np.array(list(map(float,stored.split()[1:]))).reshape(-1,2)
pts_b=np.array(list(map(float,replayed.split()[1:]))).reshape(-1,2)
diff=[]
if pts_a.shape==pts_b.shape:
    for i,(x,y) in enumerate(zip(pts_a,pts_b)):
        if not np.array_equal(x,y):diff.append({'vertex_zero_based':i,'stored':x.tolist(),'replayed':y.tolist(),'delta_pixels':((y-x)*[w,h]).tolist()})
out={'file':name,'numpy':np.__version__,'opencv':cv2.__version__,'size':[w,h],'same_text':stored==replayed,
     'stored_points':len(pts_a),'replayed_points':len(pts_b),'different_vertices':diff,
     'rasterization':'round(normalized coordinate * original dimensions); cv2.fillPoly',
     'stored_area':int(a.sum()),'replayed_area':int(b.sum()),'different_pixels':int(np.logical_xor(a,b).sum()),
     'polygon_pair_iou':float(np.logical_and(a,b).sum()/np.logical_or(a,b).sum()),
     'cause':'not established; version or implementation difference is a hypothesis, not proof'}
(O/'dataset_label_crosscheck.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
