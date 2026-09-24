import os, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

data_root = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen")
out_root = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KQ_DoiXung\Base vs TSVM_BG20\02_Ghep_DoiXung_TungSeed")

dir_cm = out_root / "Confusion_Matrix"
dir_pr = out_root / "Mask_PR_Curve"
dir_pred = out_root / "Val_Predictions"

def make_side_by_side(img1_path, img2_path, out_path, title_left, title_right, main_title):
    if not img1_path.exists() or not img2_path.exists():
        print(f"⚠️ Thiếu ảnh: {img1_path} hoặc {img2_path}")
        return None
        
    im1 = Image.open(img1_path)
    im2 = Image.open(img2_path)
    
    target_h = max(im1.height, im2.height)
    w1 = int(im1.width * (target_h / im1.height))
    w2 = int(im2.width * (target_h / im2.height))
    
    im1_resized = im1.resize((w1, target_h), Image.Resampling.LANCZOS)
    im2_resized = im2.resize((w2, target_h), Image.Resampling.LANCZOS)
    
    header_h = 100
    sub_header_h = 50
    total_w = w1 + w2 + 30
    total_h = target_h + header_h + sub_header_h + 20
    
    canvas = Image.new('RGB', (total_w, total_h), color=(255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    try:
        font_main = ImageFont.truetype("arialbd.ttf", 36)
        font_sub = ImageFont.truetype("arialbd.ttf", 26)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    bbox_m = draw.textbbox((0, 0), main_title, font=font_main)
    mw = bbox_m[2] - bbox_m[0]
    draw.text(((total_w - mw)//2, 25), main_title, fill=(17, 24, 39), font=font_main)
    
    bbox_l = draw.textbbox((0, 0), title_left, font=font_sub)
    lw = bbox_l[2] - bbox_l[0]
    draw.rectangle([10, header_h - 10, w1 + 10, header_h + sub_header_h - 10], fill=(239, 246, 255))
    draw.text((10 + (w1 - lw)//2, header_h + 5), title_left, fill=(30, 58, 138), font=font_sub)
    
    bbox_r = draw.textbbox((0, 0), title_right, font=font_sub)
    rw = bbox_r[2] - bbox_r[0]
    draw.rectangle([w1 + 20, header_h - 10, total_w - 10, header_h + sub_header_h - 10], fill=(255, 247, 237))
    draw.text((w1 + 20 + (w2 - rw)//2, header_h + 5), title_right, fill=(154, 52, 18), font=font_sub)
    
    canvas.paste(im1_resized, (10, header_h + sub_header_h))
    canvas.paste(im2_resized, (w1 + 20, header_h + sub_header_h))
    
    canvas.save(out_path, quality=95)
    print(f"✅ Đã tạo cập nhật: {out_path.name}")
    return canvas

def make_grid_summary(img_list, out_grid_path, grid_title):
    if len(img_list) < 6:
        return
    thumb_w = 900
    scaled = []
    for im in img_list:
        th = int(im.height * (thumb_w / im.width))
        scaled.append(im.resize((thumb_w, th), Image.Resampling.LANCZOS))
        
    grid_w = thumb_w * 2 + 30
    grid_h = scaled[0].height * 3 + 120 + 40
    
    canvas = Image.new('RGB', (grid_w, grid_h), color=(255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    try:
        font_g = ImageFont.truetype("arialbd.ttf", 44)
    except:
        font_g = ImageFont.load_default()
        
    bbox = draw.textbbox((0, 0), grid_title, font=font_g)
    gw = bbox[2] - bbox[0]
    draw.text(((grid_w - gw)//2, 35), grid_title, fill=(17, 24, 39), font=font_g)
    
    for idx, im in enumerate(scaled):
        row = idx // 2
        col = idx % 2
        x = 10 + col * (thumb_w + 10)
        y = 120 + row * (im.height + 15)
        canvas.paste(im, (x, y))
        
    canvas.save(out_grid_path, quality=90)
    print(f"🌟 ĐÃ CẬP NHẬT GRID TỔNG HỢP: {out_grid_path.name}")

# Cập nhật riêng Seed 5 và tạo lại Grid
cm_imgs, pr_imgs = [], []
for s in range(6):
    p_b_cm = data_root / f"Kvasir_BG20_Baseline_YOLO26s_seg_s{s}_w2" / "confusion_matrix_normalized.png"
    p_t_cm = data_root / f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2" / "confusion_matrix_normalized.png"
    out_cm = dir_cm / f"CM_s{s}_Base_vs_TSVM.png"
    
    p_b_pr = data_root / f"Kvasir_BG20_Baseline_YOLO26s_seg_s{s}_w2" / "MaskPR_curve.png"
    p_t_pr = data_root / f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2" / "MaskPR_curve.png"
    out_pr = dir_pr / f"PR_s{s}_Base_vs_TSVM.png"
    
    if s == 5:
        im_cm = make_side_by_side(
            p_b_cm, p_t_cm, out_cm,
            title_left="Baseline YOLO26s-seg (Seed 5) | Mask mAP: 0.7350",
            title_right="TSVM (Topology-Shape) (Seed 5) | Mask mAP: 0.7285",
            main_title="So Sánh Ma Trận Nhầm Lẫn Chuẩn Hóa Đối Xứng - Seed 5"
        )
        im_pr = make_side_by_side(
            p_b_pr, p_t_pr, out_pr,
            title_left="Baseline YOLO26s-seg (Seed 5)",
            title_right="TSVM (Topology-Shape) (Seed 5)",
            main_title="So Sánh Đường Cong Mask Precision-Recall - Seed 5"
        )
    else:
        im_cm = Image.open(out_cm)
        im_pr = Image.open(out_pr)
        
    cm_imgs.append(im_cm)
    pr_imgs.append(im_pr)

make_grid_summary(cm_imgs, dir_cm / "CM_All_6Seeds_Summary_Grid.png", "BẢNG ĐỐI CHIẾU MA TRẬN NHẦM LẪN TOÀN BỘ 6 SEEDS (BASELINE VS TSVM)")
make_grid_summary(pr_imgs, dir_pr / "PR_All_6Seeds_Summary_Grid.png", "BẢNG ĐỐI CHIẾU ĐƯỜNG CONG MASK PR TOÀN BỘ 6 SEEDS (BASELINE VS TSVM)")
print("🎉 CẬP NHẬT HOÀN TẤT!")
