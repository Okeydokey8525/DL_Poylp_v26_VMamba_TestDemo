import sys,json,shutil
from pathlib import Path
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];sys.path.append(str(R/'.codex_report_work_20261015/packages'))
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
P=R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32';dest=O/'reproduced_legacy';(dest/'figures').mkdir(parents=True,exist_ok=True)
p=R/'Stracth/Bao_Cao/phan_tich_20seed_fp32.py';ns={'__file__':str(p),'__name__':'audit'}
exec(compile(p.read_text(encoding='utf-8'),str(p),'exec'),ns);ns['OUT']=dest
curves,df=ns['load']();summary=pd.read_csv(P/'summary_20seeds_paired.csv');ns['figures'](df,curves,summary,13)
for name in ['ve_ma_tran_nham_lan_20seed.py','ve_ma_tran_nham_lan_20seed_ultralytics.py']:
 plt.rcdefaults();p=R/'Stracth/Bao_Cao'/name;code=p.read_text(encoding='utf-8')
 for stem in ['12_confusion_matrix_mean_comparison.png','13_confusion_matrix_mean_ultralytics.png']:
  code=code.replace(f'OUT = DATA / "figures" / "{stem}"',f'OUT = Path({str(dest/"figures"/stem)!r})')
 exec(compile(code,str(p),'exec'),{'__file__':str(p),'__name__':'audit'})
bench=O/'reproduced_benchmark'
for d in ['raw','tables','figures']:(bench/d).mkdir(parents=True,exist_ok=True)
for p in (P/'efficiency_benchmark/raw').glob('*'):
 if p.is_file():shutil.copy2(p,bench/'raw'/p.name)
p=P/'efficiency_benchmark/scripts/summarize.py';code=p.read_text(encoding='utf-8').split('fwd=[s for s in summary')[0]
code=code.replace("O=R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/efficiency_benchmark'",f'O=Path({str(bench)!r})')
plt.rcdefaults();exec(compile(code,str(p),'exec'),{'__file__':str(p),'__name__':'audit'})
results=[]
for folder,source in [(dest,P),(bench,P/'efficiency_benchmark')]:
 for p in folder.rglob('*.png'):
  rel=p.relative_to(folder);a=np.asarray(Image.open(source/rel).convert('RGB'));b=np.asarray(Image.open(p).convert('RGB'));same=a.shape==b.shape
  results.append({'path':str(source.relative_to(R)/rel),'same_shape':same,'pixel_identical':bool(np.array_equal(a,b)) if same else False,'mean_abs_pixel_diff':float(np.abs(a.astype(float)-b).mean()) if same else None})
(O/'other_reproduction_pixel_comparison.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('Identical',sum(x['pixel_identical'] for x in results),'of',len(results));print([r for r in results if not r['pixel_identical']])
