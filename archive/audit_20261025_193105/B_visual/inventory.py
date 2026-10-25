from pathlib import Path
import sys,hashlib,json,csv,zipfile,xml.etree.ElementTree as ET
from PIL import Image,ImageOps,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
PKG=ROOT/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32'
(OUT/'embedded').mkdir(exist_ok=True);(OUT/'sheets').mkdir(exist_ok=True);(OUT/'ocr_input').mkdir(exist_ok=True)
rows=[]
def add(p,group,model='',seed='',caption='',source=''):
 im=Image.open(p);im.verify();im=Image.open(p)
 row=dict(id=f'V{len(rows)+1:04}',group=group,model=model,seed=seed,path=str(p.relative_to(ROOT)),width=im.width,height=im.height,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),caption=caption,source=source,visual_status='not_yet_inspected',numeric_status='not_yet_verified')
 rows.append(row);return row
for p in sorted(PKG.rglob('*')):
 if p.suffix.lower() in ['.png','.jpg','.jpeg']:add(p,'package')
for model,parent,prefix in [('Baseline','YOLOv26s-seg','Kvasir_BG20_Baseline_YOLO26s_seg'),('TSVM','Kvasir_BG20_YOLO26s_seg_TSVM_FP32','Kvasir_BG20_YOLO26s_seg_TSVM_FP32')]:
 for seed in range(20):
  run=ROOT/'Ket_Qua_V2/KetQua_Nen'/parent/f'{prefix}_s{seed}_w2'
  for pattern in ['confusion_matrix*.png','*PR_curve.png','*P_curve.png','*R_curve.png','*F1_curve.png']:
   for p in sorted(run.glob(pattern)):add(p,'raw',model,seed)
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
doc=ROOT/'Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx'
with zipfile.ZipFile(doc) as z:
 rels={x.attrib['Id']:x.attrib['Target'] for x in ET.fromstring(z.read('word/_rels/document.xml.rels'))}
 body=ET.fromstring(z.read('word/document.xml')).find('w:body',ns);children=list(body)
 for i,el in enumerate(children):
  for blip in el.findall('.//a:blip',ns):
   rid=blip.attrib.get('{'+ns['r']+'}embed');target=rels.get(rid,'')
   if not target:continue
   member='word/'+target;dest=OUT/'embedded'/Path(target).name
   dest.write_bytes(z.read(member));following=[]
   for nxt in children[i+1:i+5]:
    text=''.join(x.text or '' for x in nxt.findall('.//w:t',ns))
    if text:following.append(text)
   matches=[r['path'] for r in rows if r['sha256']==hashlib.sha256(dest.read_bytes()).hexdigest()]
   r=add(dest,'word',caption=' | '.join(following),source=';'.join(matches));r['xml_body_index']=i
   crop=el.find('.//a:srcRect',ns);r['crop']=json.dumps(crop.attrib if crop is not None else {})
# Search same-byte sources for embedded figures beyond package (diagram/preprocessing/app work).
unknown={r['sha256'] for r in rows if r['group']=='word' and not r['source']}
byhash={}
for folder in ['.codex_report_work_20261015/figures','.codex_revision_20261016/figures','Bao_cao']:
 for p in (ROOT/folder).rglob('*'):
  if p.is_file() and p.suffix.lower() in ['.png','.jpg','.jpeg']:
   h=hashlib.sha256(p.read_bytes()).hexdigest()
   if h in unknown:byhash.setdefault(h,[]).append(str(p.relative_to(ROOT)))
for r in rows:
 if r['group']=='word' and not r['source']:r['source']=';'.join(byhash.get(r['sha256'],[]))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
def sheets(rs,prefix,w=850,h=660,ncol=2,nrow=2):
 for j in range(0,len(rs),ncol*nrow):
  chunk=rs[j:j+ncol*nrow];canvas=Image.new('RGB',(w*ncol,h*nrow),'#eeeeee');draw=ImageDraw.Draw(canvas)
  for k,r in enumerate(chunk):
   im=Image.open(ROOT/r['path']).convert('RGB');im.thumbnail((w-16,h-75));x=(k%ncol)*w;y=(k//ncol)*h
   canvas.paste(im,(x+(w-im.width)//2,y+65));label=f"{r['id']} {r['model']} s{r['seed']} {Path(r['path']).name}"
   draw.text((x+8,y+5),label[:72],font=font,fill='black');draw.text((x+8,y+30),str(Path(r['path']).parent)[-85:],font=font,fill='black')
  canvas.save(OUT/'sheets'/f'{prefix}_{j//(ncol*nrow):02}.jpg',quality=94)
sheets([r for r in rows if r['group']=='package'],'package')
sheets([r for r in rows if r['group']=='word'],'word')
# compact per-run curve sheets; 8 curves per model/seed, each resized to 660x500
for model in ['Baseline','TSVM']:
 for seed in range(20):
  subset=[r for r in rows if r['group']=='raw' and r['model']==model and r['seed']==seed]
  sheets(subset,f'raw_{model}_{seed:02}',w=760,h=590,ncol=2,nrow=5)
# OCR full package images, raw CM count crops and PR legend crops.
jobs=[]
for r in rows:
 p=ROOT/r['path'];im=Image.open(p).convert('RGB');name=p.name
 if r['group'] in ['package','word']:
  im.thumbnail((2100,2100));dest=OUT/'ocr_input'/f"{r['id']}.png";im.save(dest);jobs.append({'id':r['id'],'type':'full','path':str(dest)})
 elif name=='confusion_matrix.png':
  for key,box in {'TP':(890,404,1330,644),'FP':(1670,404,2110,644),'FN':(890,1182,1330,1422),'TN':(1670,1182,2110,1422)}.items():
   dest=OUT/'ocr_input'/f"{r['id']}_{key}.png";ImageOps.expand(im.crop(box),border=30,fill='white').save(dest);jobs.append({'id':r['id'],'type':key,'path':str(dest)})
 elif name.endswith('PR_curve.png'):
  dest=OUT/'ocr_input'/f"{r['id']}_legend.png";im.crop((int(im.width*.69),0,im.width,int(im.height*.65))).save(dest);jobs.append({'id':r['id'],'type':'legend','path':str(dest)})
fields=list(dict.fromkeys(k for r in rows for k in r))
with (OUT/'figure_inventory.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
(OUT/'inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');(OUT/'ocr_jobs.json').write_text(json.dumps(jobs),encoding='utf-8')
print('Inventory',len(rows),{g:sum(r['group']==g for r in rows) for g in ['package','raw','word']},'OCR jobs',len(jobs))
print('Unmatched word',[(r['id'],r['caption'][:80]) for r in rows if r['group']=='word' and not r['source']])
