import sys, math, json, cv2, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams.update({"font.family": "Times New Roman", "font.size": 12})
R = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
DP = R / "archive/Ket_Qua_V2/Data Prosessing"; KS = DP / "Kvasir-SEG"
BG = R / "archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20"
GREEN = (0, 230, 0)
info = {}


def rgb(p):
    return cv2.cvtColor(cv2.imread(str(p)), cv2.COLOR_BGR2RGB)


def read_polys(p, w, h):
    ps = []
    for line in Path(p).read_text().splitlines():
        v = list(map(float, line.split()[1:]))
        ps.append(np.array(v).reshape(-1, 2) * [w, h])
    return ps


def panel(ax, img, label, cmap=None):
    ax.imshow(img, cmap=cmap)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_linewidth(0.5); s.set_color("#888")
    ax.set_xlabel(label, fontsize=12, labelpad=4)


SC = 1.25  # figure inches scale; final width set in Word
# ---------- Hinh 3.1: vi du du lieu ----------
pid = "cju0qkwl35piu0993l0dewei2"; bgid = "bg_01af3454-037f-4708-b73c-6ec4423b6a61"
fig, axs = plt.subplots(1, 3, figsize=(15 / 2.54 * SC, 5.0 / 2.54 * SC))
panel(axs[0], rgb(KS / "images" / f"{pid}.jpg"), "a. Ảnh nội soi có polyp")
panel(axs[1], cv2.imread(str(KS / "masks" / f"{pid}.jpg"), 0), "b. Mặt nạ phân đoạn gốc", cmap="gray")
panel(axs[2], rgb(BG / "images/train" / f"{bgid}.jpg"), "c. Ảnh nền normal-cecum")
plt.tight_layout(w_pad=0.6); plt.savefig(OUT / "hinh_3_1_vi_du_du_lieu.png", dpi=220, bbox_inches="tight"); plt.close()

# ---------- Hinh 3.2: mat na -> da giac ----------
sid = "cju1ats0y372e08011yazcsxm"
img = rgb(KS / "images" / f"{sid}.jpg"); g = cv2.imread(str(KS / "masks" / f"{sid}.jpg"), 0); h, w = g.shape
thr, th = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cl = cv2.morphologyEx(th, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
cs, _ = cv2.findContours(cl, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
big = [c for c in cs if cv2.contourArea(c) >= 20]
before = sum(len(c) for c in big)
approx = [cv2.approxPolyDP(c, 0.002 * cv2.arcLength(c, True), True) for c in big]
after = sum(len(a) for a in approx)
stored = read_polys(BG / "labels/train" / f"{sid}.txt", w, h)
info["h32"] = {"id": sid, "size": [w, h], "otsu": thr, "contours_all": len(cs), "kept": len(big),
               "pts_before": before, "pts_after": after, "stored_pts": [len(p) for p in stored],
               "gray_unique": int(np.unique(g).size)}
c_img = img.copy(); cv2.drawContours(c_img, big, -1, GREEN, 2)
p_img = img.copy()
for a in approx:
    cv2.polylines(p_img, [a], True, GREEN, 2)
    for pt in a.reshape(-1, 2):
        cv2.circle(p_img, (int(pt[0]), int(pt[1])), 5, (255, 230, 0), -1)
fig, axs = plt.subplots(2, 2, figsize=(15 / 2.54 * SC, 11.6 / 2.54 * SC))
panel(axs[0, 0], img, "a. Ảnh nội soi gốc")
panel(axs[0, 1], g, "b. Mặt nạ gốc trước xử lý", cmap="gray")
panel(axs[1, 0], c_img, f"c. Đường bao ban đầu: {before} điểm")
panel(axs[1, 1], p_img, f"d. Đa giác đơn giản hóa: {after} điểm")
plt.tight_layout(h_pad=0.8, w_pad=0.6); plt.savefig(OUT / "hinh_3_2_mat_na_sang_da_giac.png", dpi=220, bbox_inches="tight"); plt.close()

# ---------- Hinh 3.3: LetterBox ----------
vid = "cjyzul1qggwwj07216mhiv5sy"
im = rgb(BG / "images/val" / f"{vid}.jpg"); H0, W0 = im.shape[:2]
polys = read_polys(BG / "labels/val" / f"{vid}.txt", W0, H0)
r = 640 / max(H0, W0); nw, nh = min(math.ceil(W0 * r), 640), min(math.ceil(H0 * r), 640)
rs = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_LINEAR)
dw, dh = (640 - nw) / 2, (640 - nh) / 2
top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1)); left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
lb = cv2.copyMakeBorder(rs, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
info["h33"] = {"id": vid, "orig": [W0, H0], "r": r, "resized": [nw, nh], "pad_top": top, "pad_bottom": bottom,
               "pad_left": left, "pad_right": right, "final": [lb.shape[1], lb.shape[0]]}
a_img = im.copy(); b_img = lb.copy()
for p in polys:
    cv2.polylines(a_img, [p.astype(np.int32)], True, GREEN, 6)
    cv2.polylines(b_img, [(p * r + [left, top]).astype(np.int32)], True, GREEN, 2)
fig, axs = plt.subplots(1, 2, figsize=(15 / 2.54 * SC, 5.8 / 2.54 * SC), gridspec_kw={"width_ratios": [W0 / H0, 1]})
panel(axs[0], a_img, f"a. Ảnh gốc {W0} × {H0} pixel")
panel(axs[1], b_img, f"b. Sau LetterBox {lb.shape[1]} × {lb.shape[0]} pixel")
plt.tight_layout(w_pad=1.2); plt.savefig(OUT / "hinh_3_3_letterbox.png", dpi=220, bbox_inches="tight"); plt.close()


# ---------- Hinh 3.4: tang cuong ----------
def load640(split, i):
    im = cv2.imread(str(BG / "images" / split / f"{i}.jpg")); h0, w0 = im.shape[:2]; r = 640 / max(h0, w0)
    im = cv2.resize(im, (min(math.ceil(w0 * r), 640), min(math.ceil(h0 * r), 640)))
    lp = BG / "labels" / split / f"{i}.txt"
    ps = [p * r for p in read_polys(lp, w0, h0)] if lp.stat().st_size else []
    return im, ps


def hsv(im, r):
    x = np.arange(256, dtype=np.int16)
    lh = ((x + r[0] * 180) % 180).astype(np.uint8)
    ls = np.clip(x * (r[1] + 1), 0, 255).astype(np.uint8)
    lv = np.clip(x * (r[2] + 1), 0, 255).astype(np.uint8); ls[0] = 0
    hh, ss, vv = cv2.split(cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    return cv2.cvtColor(cv2.merge((cv2.LUT(hh, lh), cv2.LUT(ss, ls), cv2.LUT(vv, lv))), cv2.COLOR_HSV2BGR)


def affine(im, ps, s, tx, ty, out=640):
    h, w = im.shape[:2]
    C = np.eye(3); C[0, 2] = -w / 2; C[1, 2] = -h / 2
    Sm = np.eye(3); Sm[0, 0] = Sm[1, 1] = s
    T = np.eye(3); T[0, 2] = 0.5 * out + tx * out; T[1, 2] = 0.5 * out + ty * out
    M = T @ Sm @ C
    o = cv2.warpAffine(im, M[:2], (out, out), borderValue=(114, 114, 114))
    return o, [(np.c_[p, np.ones(len(p))] @ M.T)[:, :2] for p in ps]


def draw(im, ps, t=2):
    im = im.copy(); m = np.zeros(im.shape[:2], np.uint8)
    for p in ps:
        mm = np.zeros_like(m); cv2.fillPoly(mm, [p.astype(np.int32)], 1)
        cs2, _ = cv2.findContours(mm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(im, cs2, -1, (0, 230, 0), t)
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


base, bps = load640("train", sid)
flip = cv2.flip(base, 1); fps = [np.c_[base.shape[1] - p[:, 0], p[:, 1]] for p in bps]
rh = [0.012, 0.55, -0.30]; hs = hsv(base, rh)
af, aps = affine(base, bps, s=0.62, tx=0.08, ty=-0.06)
ids = [("train", sid), ("train", "cju0qkwl35piu0993l0dewei2"), ("train", bgid), ("train", "cju1c3218411b08014g9f6gig")]
s = 640; canvas = np.full((2 * s, 2 * s, 3), 114, np.uint8); xc, yc = 700, 610; mps = []
for k, (sp, i) in enumerate(ids):
    im2, ps = load640(sp, i); h2, w2 = im2.shape[:2]
    if k == 0:
        x1a, y1a, x2a, y2a = max(xc - w2, 0), max(yc - h2, 0), xc, yc
        x1b, y1b, x2b, y2b = w2 - (x2a - x1a), h2 - (y2a - y1a), w2, h2
    elif k == 1:
        x1a, y1a, x2a, y2a = xc, max(yc - h2, 0), min(xc + w2, 2 * s), yc
        x1b, y1b, x2b, y2b = 0, h2 - (y2a - y1a), min(w2, x2a - x1a), h2
    elif k == 2:
        x1a, y1a, x2a, y2a = max(xc - w2, 0), yc, xc, min(2 * s, yc + h2)
        x1b, y1b, x2b, y2b = w2 - (x2a - x1a), 0, w2, min(y2a - y1a, h2)
    else:
        x1a, y1a, x2a, y2a = xc, yc, min(xc + w2, 2 * s), min(2 * s, yc + h2)
        x1b, y1b, x2b, y2b = 0, 0, min(w2, x2a - x1a), min(y2a - y1a, h2)
    canvas[y1a:y2a, x1a:x2a] = im2[y1b:y2b, x1b:x2b]
    mps += [p + [x1a - x1b, y1a - y1b] for p in ps]
mo, mops = affine(canvas, mps, s=0.95, tx=0.03, ty=0.02)
comb, cps = affine(hsv(flip, [-0.01, -0.4, 0.25]), fps, s=1.15, tx=-0.05, ty=0.04)
info["h34"] = {"base_id": sid, "hsv_gain_example": rh, "affine_example": {"scale": 0.62, "tx": 0.08, "ty": -0.06},
               "mosaic_center": [xc, yc], "mosaic_ids": [i for _, i in ids]}
fig, axs = plt.subplots(2, 3, figsize=(15 / 2.54 * SC, 12.2 / 2.54 * SC))
panel(axs[0, 0], draw(*affine(base, bps, 1.0, 0, 0)), "a. Ảnh gốc 640 × 640")
panel(axs[0, 1], draw(*affine(flip, fps, 1.0, 0, 0)), "b. Lật ngang")
panel(axs[0, 2], draw(*affine(hs, bps, 1.0, 0, 0)), "c. Thay đổi màu HSV")
panel(axs[1, 0], draw(af, aps), "d. Dịch chuyển và thu nhỏ")
panel(axs[1, 1], draw(mo, mops), "e. Mosaic bốn ảnh")
panel(axs[1, 2], draw(comb, cps), "f. Kết hợp nhiều phép")
plt.tight_layout(h_pad=1.8, w_pad=0.5); plt.savefig(OUT / "hinh_3_4_tang_cuong.png", dpi=220, bbox_inches="tight"); plt.close()

json.dump(info, open(OUT / "thong_so_sinh_hinh.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=float)
print(json.dumps(info, indent=1, default=float, ensure_ascii=False))
