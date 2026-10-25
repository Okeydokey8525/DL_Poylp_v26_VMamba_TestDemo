"""Prepare read-only QA views for fixed, non-cherry-picked saved prediction samples."""
from pathlib import Path
import csv,hashlib,sys
from PIL import Image,ImageDraw,ImageFont
sys.stdout.reconfigure(encoding='utf-8')
O=Path(__file__).resolve().parent;R=O.parents[1];out=O/'prediction_samples';out.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24);rows=[]
for model,parent,prefix in [('Baseline','YOLOv26s-seg','Kvasir_BG20_Baseline_YOLO26s_seg'),('TSVM','Kvasir_BG20_YOLO26s_seg_TSVM_FP32','Kvasir_BG20_YOLO26s_seg_TSVM_FP32')]:
    for seed in [0,5,8,18,19]:
        run=R/'Ket_Qua_V2/KetQua_Nen'/parent/f'{prefix}_s{seed}_w2'
        files=[run/'val_batch0_labels.jpg',run/'val_batch0_pred.jpg']
        canvas=Image.new('RGB',(2400,1300),'#eeeeee');draw=ImageDraw.Draw(canvas)
        for i,p in enumerate(files):
            row={'model':model,'seed':seed,'selection_reason':'predeclared historical-problem seeds0,5,8 and late18,19; batch0 only','role':'GT labels' if i==0 else 'saved prediction','path':str(p.relative_to(R)),'exists':p.exists()}
            if p.exists():
                row['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
                im=Image.open(p).convert('RGB');row['width'],row['height']=im.size;im.thumbnail((1180,1220))
                canvas.paste(im,(i*1200+(1200-im.width)//2,70));draw.text((i*1200+15,8),f'{model} seed{seed}: {p.name}',font=font,fill='black')
            rows.append(row)
        canvas.save(out/f'{model}_s{seed}_pair.jpg',quality=96)
keys=list(dict.fromkeys(k for row in rows for k in row))
with (O/'prediction_sample_inventory.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
print('Prepared',len(rows),'source images in10 fixed pairs')
