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

for d in [dir_cm, dir_pr, dir_pred]:
    d.mkdir(parents=True, exist_ok=True)

# Đọc kết quả best mAP của từng seed để ghi lên header
csv_details = out_root.parent / "04_BangSoLieu_Va_BaoCao" / "head_to_head_seed_details.csv"
df_details = pd.read_csv(csv_details)

def get_seed_info(model, seed):
    sub = df_details[(df_details['Model'] == model) & (df_details['Seed'] == seed)]
    if len(sub) > 0:
        return sub.iloc[0]['Mask_mAP50_95']
    return 0.0

def make_side_by_side(img1_path, img2_path, out_path, title_left, title_right, main_title):
    if not img1_path.exists() or not img2_path.exists():
        print(f"⚠️ Thiếu ảnh: {img1_path} hoặc {img2_path}")
        return None
        
    im1 = Image.open(img1_path)
    im2 = Image.open(img2_path)
    
    # Đồng bộ chiều cao
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
        
    # Vẽ main title
    bbox_m = draw.textbbox((0, 0), main_title, font=font_main)
    mw = bbox_m[2] - bbox_m[0]
    draw.text(((total_w - mw)//2, 25), main_title, fill=(17, 24, 39), font=font_main)
    
    # Header bên trái (Baseline - Blue)
    bbox_l = draw.textbbox((0, 0), title_left, font=font_sub)
    lw = bbox_l[2] - bbox_l[0]
    draw.rectangle([10, header_h - 10, w1 + 10, header_h + sub_header_h - 10], fill=(239, 246, 255))
    draw.text((10 + (w1 - lw)//2, header_h + 5), title_left, fill=(30, 58, 138), font=font_sub)
    
    # Header bên phải (TSVM - Orange)
    bbox_r = draw.textbbox((0, 0), title_right, font=font_sub)
    rw = bbox_r[2] - bbox_r[0]
    draw.rectangle([w1 + 20, header_h - 10, total_w - 10, header_h + sub_header_h - 10], fill=(255, 247, 237))
    draw.text((w1 + 20 + (w2 - rw)//2, header_h + 5), title_right, fill=(154, 52, 18), font=font_sub)
    
    # Dán ảnh
    canvas.paste(im1_resized, (10, header_h + sub_header_h))
    canvas.paste(im2_resized, (w1 + 20, header_h + sub_header_h))
    
    canvas.save(out_path, quality=95)
    print(f"✅ Đã tạo: {out_path.name}")
    return canvas

# 1. GHÉP CONFUSION MATRIX THEO TỪNG SEED
print("\n--- BẮT ĐẦU GHÉP CONFUSION MATRIX TỪNG SEED ---")
cm_images = []
for s in range(6):
    p_base = data_root / f"Kvasir_BG20_Baseline_YOLO26s_seg_s{s}_w2" / "confusion_matrix_normalized.png"
    p_tsvm = data_root / f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2" / "confusion_matrix_normalized.png"
    out_file = dir_cm / f"CM_s{s}_Base_vs_TSVM.png"
    
    map_b = get_seed_info("Baseline", f"s{s}")
    map_t = get_seed_info("TSVM", f"s{s}")
    
    im = make_side_by_side(
        p_base, p_tsvm, out_file,
        title_left=f"Baseline YOLO26s-seg (Seed {s}) | Mask mAP: {map_b:.4f}",
        title_right=f"TSVM (Topology-Shape) (Seed {s}) | Mask mAP: {map_t:.4f}",
        main_title=f"So Sánh Ma Trận Nhầm Lẫn Chuẩn Hóa Đối Xứng - Seed {s}"
    )
    if im:
        cm_images.append(im)

# 2. GHÉP MASK PR CURVES THEO TỪNG SEED
print("\n--- BẮT ĐẦU GHÉP MASK PR CURVES TỪNG SEED ---")
pr_images = []
for s in range(6):
    p_base = data_root / f"Kvasir_BG20_Baseline_YOLO26s_seg_s{s}_w2" / "MaskPR_curve.png"
    p_tsvm = data_root / f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2" / "MaskPR_curve.png"
    out_file = dir_pr / f"PR_s{s}_Base_vs_TSVM.png"
    
    map_b = get_seed_info("Baseline", f"s{s}")
    map_t = get_seed_info("TSVM", f"s{s}")
    
    im = make_side_by_side(
        p_base, p_tsvm, out_file,
        title_left=f"Baseline YOLO26s-seg (Seed {s})",
        title_right=f"TSVM (Topology-Shape) (Seed {s})",
        main_title=f"So Sánh Đường Cong Mask Precision-Recall - Seed {s}"
    )
    if im:
        pr_images.append(im)

# 3. GHÉP VAL BATCH PREDICTIONS THEO TỪNG SEED
print("\n--- BẮT ĐẦU GHÉP VAL PREDICTIONS TỪNG SEED ---")
pred_images = []
for s in range(6):
    p_base = data_root / f"Kvasir_BG20_Baseline_YOLO26s_seg_s{s}_w2" / "val_batch0_pred.jpg"
    p_tsvm = data_root / f"Kvasir_BG20_YOLO26s_seg_TSVM_s{s}_w2" / "val_batch0_pred.jpg"
    out_file = dir_pred / f"Pred_s{s}_Base_vs_TSVM.png"
    
    im = make_side_by_side(
        p_base, p_tsvm, out_file,
        title_left=f"Dự Đoán Baseline YOLO26s-seg (Seed {s})",
        title_right=f"Dự Đoán TSVM (Topology-Shape) (Seed {s})",
        main_title=f"So Sánh Dự Đoán Trực Quan Phân Đoạn Trên Tập Test - Seed {s}"
    )
    if im:
        pred_images.append(im)

# 4. TẠO SUMMARY GRID 6 SEEDS (2 CỘT x 3 HÀNG)
def make_grid_summary(img_list, out_grid_path, grid_title):
    if len(img_list) < 6:
        return
    # resize các ảnh ghép về kích thước vừa phải
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
    print(f"🌟 ĐÃ XUẤT GRID TỔNG HỢP: {out_grid_path.name}")

print("\n--- BẮT ĐẦU XUẤT CÁC BẢNG GRID TỔNG HỢP 6 SEEDS ---")
make_grid_summary(cm_images, dir_cm / "CM_All_6Seeds_Summary_Grid.png", "BẢNG ĐỐI CHIẾU MA TRẬN NHẦM LẪN TOÀN BỘ 6 SEEDS (BASELINE VS TSVM)")
make_grid_summary(pr_images, dir_pr / "PR_All_6Seeds_Summary_Grid.png", "BẢNG ĐỐI CHIẾU ĐƯỜNG CONG MASK PR TOÀN BỘ 6 SEEDS (BASELINE VS TSVM)")
make_grid_summary(pred_images, dir_pred / "Pred_All_6Seeds_Summary_Grid.png", "BẢNG ĐỐI CHIẾU DỰ ĐOÁN PHÂN ĐOẠN THỰC TẾ TOÀN BỘ 6 SEEDS (BASELINE VS TSVM)")

print("\n🎉 HOÀN THÀNH TẤT CẢ CÁC ẢNH GHÉP ĐỐI XỨNG TỪNG SEED VÀ BẢNG GRID TỔNG HỢP!")
