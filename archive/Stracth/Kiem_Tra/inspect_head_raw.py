import sys, os
from pathlib import Path
repo_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\ultralytics_Topology-Shape-aware VMamba"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

import torch, cv2
from PIL import Image
from ultralytics.nn.autobackend import AutoBackend

ckpt_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2\weights\best.pt"
img_path = r"C:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\Kvasir_YOLO_SEG_BG20\images\val\cju0qkwla3r050754x9yodrec.jpg"

ab = AutoBackend(model=ckpt_path, device=torch.device('cpu'), fuse=False)
model = ab.model
head = model.model[-1]

im = cv2.imread(img_path)
im = cv2.resize(im, (640, 640))
im_tensor = torch.from_numpy(im).permute(2, 0, 1).unsqueeze(0).float() / 255.0

with torch.no_grad():
    out = model(im_tensor)

preds = out[1]
print("preds keys:", preds.keys())
one2many = preds["one2many"]
print("one2many keys:", one2many.keys())
print("one2many boxes shape:", one2many["boxes"].shape)
print("one2many scores shape:", one2many["scores"].shape)

# Let's decode one2many
one2many_scores = one2many["scores"].sigmoid()
print("one2many scores max:", one2many_scores.max().item(), "min:", one2many_scores.min().item())

one2one = preds["one2one"]
one2one_scores = one2one["scores"].sigmoid()
print("one2one scores max:", one2one_scores.max().item(), "min:", one2one_scores.min().item())
