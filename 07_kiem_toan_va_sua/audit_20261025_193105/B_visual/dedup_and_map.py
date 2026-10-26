import sys,json,csv
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8');O=Path(__file__).resolve().parent;R=O.parents[1]
rs=json.loads((O/'inventory.json').read_text(encoding='utf-8'));seen=set();clean=[]
for r in rs:
 if r['path'] in seen and r['group']=='raw':continue
 seen.add(r['path']);clean.append(r)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
for m in ['Baseline','TSVM']:
 for s in range(20):
  sub=[r for r in clean if r['group']=='raw' and r['model']==m and r['seed']==s]
  canvas=Image.new('RGB',(1520,2900),'#eeeeee');d=ImageDraw.Draw(canvas)
  for k,r in enumerate(sub):
   im=Image.open(R/r['path']).convert('RGB');im.thumbnail((748,535));x=k%2*760;y=k//2*580
   canvas.paste(im,(x+(760-im.width)//2,y+45));d.text((x+4,y+3),f"{r['id']} {m} seed {s} {Path(r['path']).name}",font=font,fill='black')
  canvas.save(O/'sheets'/f'unique_{m}_{s:02}.jpg',quality=95)
(O/'inventory.json').write_text(json.dumps(clean,ensure_ascii=False,indent=2),encoding='utf-8')
keys=list(dict.fromkeys(k for r in clean for k in r))
with (O/'figure_inventory.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,keys);w.writeheader();w.writerows(clean)
print('Unique',len(clean),'package',sum(r['group']=='package' for r in clean),'raw',sum(r['group']=='raw' for r in clean),'word',sum(r['group']=='word' for r in clean))
for r in clean:
 if r['group']=='word':print(r['id'],r['caption'][:110],r['source'])
