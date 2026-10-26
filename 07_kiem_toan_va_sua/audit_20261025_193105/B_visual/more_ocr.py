import json
from pathlib import Path
from PIL import Image,ImageOps
O=Path(__file__).resolve().parent;R=O.parents[1];rs=json.loads((O/'inventory.json').read_text(encoding='utf-8'));jobs=[]
for r in rs:
 if r['group']!='raw' or Path(r['path']).name not in ['confusion_matrix.png','confusion_matrix_normalized.png']:continue
 for typ,(cx,cy) in {'TP':(1110,524),'FP':(1890,524),'FN':(1110,1302),'TN':(1890,1302)}.items():
  if Path(r['path']).name=='confusion_matrix.png' and typ!='TP':continue
  im=Image.open(R/r['path']).convert('RGB').crop((cx-190,cy-85,cx+190,cy+85))
  # Dark-blue cell uses white text, pale cells black text. Select by local background.
  pix=im.getpixel((5,5));dark=sum(pix)<380
  im=im.convert('L')
  im=im.point(lambda x: (0 if x>160 else 255) if dark else (0 if x<100 else 255))
  dest=O/'ocr_input'/f"{r['id']}_{typ}_threshold.png";ImageOps.expand(im,40,fill=255).save(dest)
  jobs.append({'id':r['id'],'type':typ,'path':str(dest)})
(O/'more_ocr_jobs.json').write_text(json.dumps(jobs),encoding='utf-8');print(len(jobs))
