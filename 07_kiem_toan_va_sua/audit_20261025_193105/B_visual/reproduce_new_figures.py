from pathlib import Path
import sys,shutil,json
import numpy
O=Path(__file__).resolve().parent;R=O.parents[1];sys.path.append(str(R/'.codex_report_work_20261015/packages'))
dest=O/'reproduced';dest.mkdir(exist_ok=True)
src=R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32'
for name in ['raw_20seeds_extracted_metrics.csv','raw_20seeds_confusion_matrices.csv','summary_20seeds_paired.csv']:
 shutil.copy2(src/name,dest/name)
p=R/'Stracth/Bao_Cao/generate_20seed_fp32_thesis_package.py'
code=p.read_text(encoding='utf-8').replace("OUT=ROOT/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32'",f'OUT=Path({str(dest)!r})')
# Preserve original __file__ for ROOT discovery; all writes are confined to dest.
exec(compile(code,str(p),'exec'),{'__file__':str(p),'__name__':'__audit_reproduction__'})
from PIL import Image
import numpy as np
results=[]
for p in dest.rglob('*.png'):
 rel=p.relative_to(dest);original=src/rel
 a=np.asarray(Image.open(original).convert('RGB'));b=np.asarray(Image.open(p).convert('RGB'))
 same=a.shape==b.shape
 results.append({'path':str(rel),'same_shape':same,'pixel_identical':bool(np.array_equal(a,b)) if same else False,'mean_abs_pixel_diff':float(np.abs(a.astype(float)-b).mean()) if same else None})
(O/'reproduction_pixel_comparison.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('pixel identical',sum(x['pixel_identical'] for x in results),'of',len(results))
