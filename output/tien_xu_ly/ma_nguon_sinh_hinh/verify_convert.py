import sys, importlib.util, json, hashlib
from pathlib import Path
import numpy as np, cv2
R = Path(sys.argv[1]); DP = R/"archive/Ket_Qua_V2/Data Prosessing"; BG = R/"archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20"
spec = importlib.util.spec_from_file_location("conv", DP/"convert_kvasir_with_background_to_yolo_seg.py")
# tqdm may be missing; stub
import types; sys.modules.setdefault("tqdm", types.SimpleNamespace(tqdm=lambda x,**k:x))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
res = {"match":0,"mismatch":[],"pts_before":[],"pts_after":[],"area_ratio":[],"sizes":{}, "removed_small":0,"n_contours_raw":0, "otsu_t":[], "nonbinary_px_frac":[]}
for split in ["train","val"]:
    ids = [l.strip() for l in open(R/f"archive/{split}.txt") if l.strip()]
    for i in ids:
        i = i[:-4] if i.lower().endswith(".jpg") else i
        mp = DP/"Kvasir-SEG/masks"/f"{i}.jpg"
        lines, stats, (w,h) = m.convert_mask_to_yolo_polygons(mp)
        stored = (BG/"labels"/split/f"{i}.txt").read_text()
        if "".join(lines) == stored: res["match"] += 1
        else: res["mismatch"].append(i)
        for s in stats:
            res["pts_before"].append(s["num_points_before"]); res["pts_after"].append(s["num_points_after"])
            res["area_ratio"].append(s["area"]/(w*h))
        res["sizes"][f"{w}x{h}"] = res["sizes"].get(f"{w}x{h}",0)+1
        g = cv2.cvtColor(cv2.imread(str(mp)), cv2.COLOR_BGR2GRAY)
        t,_ = cv2.threshold(g,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU); res["otsu_t"].append(t)
        res["nonbinary_px_frac"].append(float(((g>10)&(g<245)).mean()))
        th = cv2.threshold(g,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)))
        cs,_ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        res["n_contours_raw"] += len(cs); res["removed_small"] += sum(cv2.contourArea(c)<20 for c in cs)
pb, pa, ar = map(np.array,(res["pts_before"],res["pts_after"],res["area_ratio"]))
ws = [int(k.split("x")[0]) for k in res["sizes"]]; hs=[int(k.split("x")[1]) for k in res["sizes"]]
out = {"match":res["match"],"mismatch_n":len(res["mismatch"]),"mismatch_first":res["mismatch"][:5],
 "polygons":len(pb),"pts_before_mean":pb.mean(),"pts_after_mean":pa.mean(),"pts_reduction_pct":100*(1-pa.sum()/pb.sum()),
 "pts_after_min":int(pa.min()),"pts_after_max":int(pa.max()),
 "area_ratio_min":ar.min(),"area_ratio_median":float(np.median(ar)),"area_ratio_max":ar.max(),
 "n_distinct_sizes":len(res["sizes"]),"w_range":[min(ws),max(ws)],"h_range":[min(hs),max(hs)],
 "top_sizes":sorted(res["sizes"].items(),key=lambda x:-x[1])[:5],
 "contours_raw":res["n_contours_raw"],"removed_small":int(res["removed_small"]),
 "otsu_t_min":min(res["otsu_t"]),"otsu_t_max":max(res["otsu_t"]),"nonbinary_mean_frac":float(np.mean(res["nonbinary_px_frac"]))}
# background
cec = sorted((DP/"normal-cecum/normal-cecum").glob("*.jpg")); out["cecum_total"]=len(cec)
import random; random.seed(42); sel = random.sample(cec,200)
tr = [l.strip() for l in open(BG/"selected_normal_cecum_train_160.txt")]; va=[l.strip() for l in open(BG/"selected_normal_cecum_val_40.txt")]
out["bg_selection_reproduced"] = [p.name for p in sel[:160]]==tr and [p.name for p in sel[160:]]==va
bsz={}
for p in sel:
    im=cv2.imread(str(p)); k=f"{im.shape[1]}x{im.shape[0]}"; bsz[k]=bsz.get(k,0)+1
out["bg_sizes"]=bsz
print(json.dumps(out,indent=1,default=float))
