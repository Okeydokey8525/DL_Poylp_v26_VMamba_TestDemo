"""Independent reconstruction of labels in memory; never executes dataset builder."""
from pathlib import Path
import csv, hashlib, json, random, statistics, sys
import cv2
cv2.setNumThreads(1)
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
SRC=ROOT/'Ket_Qua_V2/Data Prosessing';DST=ROOT/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20'
rows=[];all_before=[];all_after=[];fractions=[];bad=[];image_bad=[]
for p in sorted((SRC/'Kvasir-SEG/masks').glob('*.jpg')):
    im=cv2.imread(str(p));gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);h,w=gray.shape
    threshold,mask=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    closed=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)),iterations=1)
    contours,_=cv2.findContours(closed,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    lines=[];removed=0
    for contour in contours:
        area=cv2.contourArea(contour)
        if area<20:removed+=1;continue
        approx=cv2.approxPolyDP(contour,0.002*cv2.arcLength(contour,True),True).reshape(-1,2)
        if len(approx)<3:approx=contour.reshape(-1,2)
        if len(approx)<3:continue
        all_before.append(len(contour));all_after.append(len(approx));fractions.append(area/(w*h))
        coords=' '.join(f'{max(0,min(1,float(x)/w)):.6f} {max(0,min(1,float(y)/h)):.6f}' for x,y in approx)
        lines.append('0 '+coords+'\n')
    matches=list((DST/'labels').glob('*/'+p.stem+'.txt'))
    same=len(matches)==1 and matches[0].read_text()==''.join(lines)
    if not same:bad.append(p.name)
    if len(matches)==1:
        split=matches[0].parent.name;src_img=SRC/'Kvasir-SEG/images'/p.name;dst_img=DST/'images'/split/p.name
        if src_img.read_bytes()!=dst_img.read_bytes():image_bad.append(p.name)
    rows.append({'file':p.name,'otsu':threshold,'contours':len(contours),'removed':removed,'kept':len(lines),'label_exact_match':same})
cecum=sorted((SRC/'normal-cecum').rglob('*.jpg'));rng=random.Random(42);selection=rng.sample(cecum,200)
bg={}
for split,paths in [('train',selection[:160]),('val',selection[160:])]:
    stored=(DST/f'selected_normal_cecum_{split}_{160 if split=="train" else 40}.txt').read_text().splitlines()
    chosen=[p.name for p in paths]
    bg[split]={'selection_order_exact':chosen==stored,'missing_or_extra':sorted(set(chosen)^set(stored)),
               'copied_image_byte_mismatches':[p.name for p in paths if p.read_bytes()!=(DST/'images'/split/('bg_'+p.name)).read_bytes()]}
out={'opencv':cv2.__version__,'masks_checked':len(rows),'otsu_min':min(r['otsu'] for r in rows),'otsu_max':max(r['otsu'] for r in rows),
     'contours':sum(r['contours'] for r in rows),'removed_under_20':sum(r['removed'] for r in rows),'kept':sum(r['kept'] for r in rows),
     'vertices_before_mean':statistics.mean(all_before),'vertices_after_mean':statistics.mean(all_after),'vertices_after_min':min(all_after),'vertices_after_max':max(all_after),
     'vertex_reduction_pct':100*(1-statistics.mean(all_after)/statistics.mean(all_before)),
     'region_area_fraction_min':min(fractions),'region_area_fraction_max':max(fractions),'region_area_fraction_median':statistics.median(fractions),
     'labels_not_exact':bad,'polyp_copy_byte_mismatches':image_bad,'background':bg}
(HERE/'preprocessing_independent.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
with (HERE/'preprocessing_per_mask.csv').open('w',newline='',encoding='utf-8-sig') as f:
    wr=csv.DictWriter(f,fieldnames=rows[0]);wr.writeheader();wr.writerows(rows)
print(json.dumps(out,indent=2))
