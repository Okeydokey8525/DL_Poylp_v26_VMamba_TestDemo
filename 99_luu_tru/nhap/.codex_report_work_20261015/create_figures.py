from pathlib import Path
import sys,json
O=Path(__file__).parent;sys.path.insert(0,str(O/'packages'))
import numpy as np,pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image,ImageDraw
R=O.parent;F=O/'figures';F.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':220})
d=pd.read_csv(O/'verified_raw.csv');sm=pd.read_csv(O/'verified_statistics.csv').set_index('metric')
colors=['#305775','#a85e36'];labels=['YOLO26s-seg','TSVM FP32']; curves=json.loads((O/'curves.json').read_text())
fig,axs=plt.subplots(1,2,figsize=(10,4.1),layout='constrained')
for ax,key,title in zip(axs,['mask_map50_95','mask_precision'],['Mask mAP50–95','Mask Precision']):
    a=d[d.model=='Baseline'][key].to_numpy();b=d[d.model=='TSVM'][key].to_numpy()
    for i,(x,y) in enumerate(zip(a,b)):ax.plot([0,1],[x,y],color='#b0b6bd',lw=.8,zorder=1)
    ax.scatter(np.zeros(20),a,color=colors[0],s=24,zorder=2);ax.scatter(np.ones(20),b,color=colors[1],s=24,zorder=2)
    ax.set(xticks=[0,1],xticklabels=labels,title=title,xlim=(-.3,1.3));ax.grid(axis='y',alpha=.2)
fig.savefig(F/'paired.png');plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4.2),layout='constrained');keys=['mask_map50_95','mask_map50','mask_precision','mask_recall','box_map50_95','box_recall']
for i,k in enumerate(keys):
    v=sm.loc[k];ax.errorbar(v.delta*100,i,xerr=[[(v.delta-v.ci_low)*100],[(v.ci_high-v.delta)*100]],fmt='o',color=colors[1],capsize=4)
ax.axvline(0,color='#555',ls='--');ax.set(yticks=range(len(keys)),yticklabels=['Mask mAP50–95','Mask mAP50','Mask Precision','Mask Recall','Box mAP50–95','Box Recall'],xlabel='Chênh lệch TSVM − Baseline và KTC 95% (điểm phần trăm)');ax.invert_yaxis();ax.grid(axis='x',alpha=.2);fig.savefig(F/'ci.png');plt.close(fig)
for key,out,yl in [('metrics/mAP50-95(M)','curves','Mask mAP50–95'),('val/seg_loss','loss','Validation segmentation loss')]:
    fig,ax=plt.subplots(figsize=(9,4.4),layout='constrained')
    for m,c,l in zip(['Baseline','TSVM'],colors,labels):
        mat=np.array([x[key] for x in curves[m]]);mu=mat.mean(0);sd=mat.std(0,ddof=1);x=np.arange(1,101)
        ax.plot(x,mu,color=c,label=l);ax.fill_between(x,mu-sd,mu+sd,color=c,alpha=.15)
    ax.set(xlabel='Epoch',ylabel=yl);ax.grid(alpha=.2);ax.legend();fig.savefig(F/(out+'.png'));plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4.2),layout='constrained')
a=d[d.model=='Baseline'].mask_map50_95.to_numpy();b=d[d.model=='TSVM'].mask_map50_95.to_numpy();delta=(b-a)*100
ax.bar(range(20),delta,color=[colors[1] if x>0 else colors[0] for x in delta]);ax.axhline(0,color='#444');ax.set(xticks=range(20),xlabel='Seed',ylabel='Δ Mask mAP50–95 (điểm phần trăm)');ax.grid(axis='y',alpha=.2);fig.savefig(F/'seed_delta.png');plt.close(fig)
fig,ax=plt.subplots(figsize=(7,4.2),layout='constrained');ax.boxplot([a,b],tick_labels=labels,showmeans=True);ax.scatter(np.full(20,1)+np.linspace(-.07,.07,20),a,s=15,color=colors[0]);ax.scatter(np.full(20,2)+np.linspace(-.07,.07,20),b,s=15,color=colors[1]);ax.set_ylabel('Mask mAP50–95');ax.grid(axis='y',alpha=.2);fig.savefig(F/'distribution.png');plt.close(fig)

def diagram(name,boxes,edges,size=(9,5)):
    fig,ax=plt.subplots(figsize=size);ax.set(xlim=(0,10),ylim=(0,6));ax.axis('off')
    for key,(x,y,w,h,text) in boxes.items():
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.03,rounding_size=.05',facecolor='#eef2f5',edgecolor='#6b7b86',lw=1))
        ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=10)
    for s,t in edges:
        x,y,w,h,_=boxes[s];xx,yy,ww,hh,_=boxes[t]
        if abs((y+h/2)-(yy+hh/2))>.8:
            start=(x+w/2,y if y>yy else y+h);end=(xx+ww/2,yy+hh if y>yy else yy)
        else:start=(x+w,y+h/2);end=(xx,yy+hh/2)
        ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','color':'#404a54','lw':1.2})
    fig.tight_layout();fig.savefig(F/(name+'.png'),bbox_inches='tight');plt.close(fig)
diagram('architecture',{'in':(.2,2.7,1.3,.8,'Ảnh RGB\n640 × 640'),'back':(2,2.4,2,1.4,'Backbone YOLO26s\nConv · C3k2 · SPPF'),'mod':(4.7,2.4,2,1.4,'Layer 10\nC2PSA → C2TSVMamba\nP5 20 × 20'),'neck':(7.3,3.6,2.3,1,'Neck\nP3 · P4 · P5'),'head':(7.3,1.4,2.3,1,'Segment26\nBox · class · mask')},[('in','back'),('back','mod'),('mod','neck'),('neck','head')],(10,4.5))
diagram('tsvm',{'x':(.2,2.6,1,.8,'Đặc trưng x'),'ss':(2,4.1,2.3,1,'SS2D bốn hướng\nF_M'),'shape':(2,.8,2.3,1.5,'DW 3×3 và 5×5\nDW 1×5, 5×1, 3×3\nĐáp ứng có hướng S'),'gate':(5,.9,1.8,1.2,'Conv 1×1\nSigmoid → G'),'mod':(5,4.1,1.8,1,'F_M ⊙ (1 + G)'),'fuse':(7.6,2.4,2.1,1.5,'Concat với S\nConv 1×1 · FFN\nx + γF')},[('x','ss'),('x','shape'),('shape','gate'),('gate','mod'),('ss','mod'),('mod','fuse'),('shape','fuse')],(10,5))
diagram('application',{'web':(.2,4.4,2.3,1,'Trình duyệt Web'),'spring':(3.1,4.4,2.8,1,'Spring Boot\nTài khoản · lịch sử'),'db':(7,4.4,2.6,1,'MongoDB\nKho ảnh cục bộ'),'mobile':(.2,.7,2.3,1,'Flutter Mobile\nDirect AI'),'api':(3.1,1.8,2.8,1.3,'FastAPI dùng chung\nKiểm tra ảnh · hàng đợi\nOverlay và metadata'),'models':(7,1.8,2.6,1.3,'YOLO26s-seg\nTSVM FP32\nCheckpoint seed 0')},[('web','spring'),('spring','db'),('spring','api'),('mobile','api'),('api','models')],(10,5.6))
# Real inference and ground truth on the same example; no invented UI screenshot.
ds=R/'Ket_Qua_V2/Kvasir_YOLO_SEG_BG20';name=json.loads((O/'smoke_results.json').read_text())[0]['samples'][0]['input']
orig=Image.open(ds/'images/val'/name).convert('RGB');gt=orig.copy();draw=ImageDraw.Draw(gt)
for line in (ds/'labels/val'/(Path(name).stem+'.txt')).read_text().splitlines():
    pts=list(map(float,line.split()[1:]));xy=[(pts[i]*gt.width,pts[i+1]*gt.height) for i in range(0,len(pts),2)];draw.line(xy+[xy[0]],fill='#00ee55',width=4)
fig,axs=plt.subplots(2,2,figsize=(9,7.6),layout='constrained')
for ax,img,title in zip(axs.flat,[orig,gt,Image.open(O/'overlay_baseline_polyp.jpg'),Image.open(O/'overlay_tsvm_polyp.jpg')],['Ảnh gốc','Đường bao nhãn YOLO','YOLO26s-seg · seed 0','TSVM FP32 · seed 0']):ax.imshow(img);ax.set_title(title);ax.axis('off')
fig.savefig(F/'qualitative.png');plt.close(fig)
print('Created',len(list(F.glob('*.png'))),'report figures')
