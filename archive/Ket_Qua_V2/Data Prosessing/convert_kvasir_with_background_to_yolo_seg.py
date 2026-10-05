#!/usr/bin/env python3
"""
convert_kvasir_with_background_to_yolo_seg.py
=============================================
Author: Senior AI Engineer & Antigravity IDE
Description:
    Tạo bộ dữ liệu độc lập Kvasir_YOLO_SEG_BG20 bổ sung 20% ảnh nền âm tính (negative background frames)
    từ kho dữ liệu normal-cecum (Kvasir v2) vào tập Kvasir-SEG hiện tại.

Cấu trúc phân bổ (200 ảnh nền = 20% của 1.000 ảnh gốc):
    - Tập Train: 880 ảnh polyp + 160 ảnh nền = 1.040 ảnh (880 nhãn polygon + 160 nhãn rỗng 0-byte)
    - Tập Val:   120 ảnh polyp +  40 ảnh nền =   160 ảnh (120 nhãn polygon +  40 nhãn rỗng 0-byte)
    - Tỷ lệ train/val giữ chuẩn 80/20.
    - Cố định random.seed(42) để đảm bảo 100% tính tái lập khoa học.
    - Hoàn toàn KHÔNG ghi đè hay thay đổi bất kỳ file dữ liệu cũ nào.
"""

import os
import sys
import json
import shutil
import random
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any

# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
import numpy as np
from tqdm import tqdm

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("KvasirBG20")


def convert_mask_to_yolo_polygons(
    mask_path: Path, 
    min_area: float = 20.0, 
    epsilon_ratio: float = 0.002
) -> Tuple[List[str], List[Dict[str, Any]], Tuple[int, int]]:
    """
    Chuyển đổi binary mask thành các dòng nhãn polygon chuẩn hóa YOLO
    bằng ngưỡng Otsu và approxPolyDP để tối ưu hóa số lượng điểm.
    """
    mask = cv2.imread(str(mask_path))
    if mask is None:
        raise ValueError(f"Không thể đọc file mask: {mask_path}")
        
    if len(mask.shape) == 3:
        gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    else:
        gray = mask
        
    height, width = gray.shape[:2]
    
    # 1. Ngưỡng thích nghi Otsu
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 2. Xử lý hình thái học (Morphological Close) để lấp lỗ nhỏ
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # 3. Tìm đường bao ngoài (External Contours)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    yolo_lines = []
    poly_stats = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
            
        bx, by, bw, bh = cv2.boundingRect(cnt)
        bbox_area = bw * bh
        aspect_ratio = float(bw) / float(bh) if bh > 0 else 0.0
        
        pts_orig = cnt.squeeze()
        num_pts_before = len(pts_orig) if len(pts_orig.shape) == 2 else len(cnt)
        
        # 4. Tối ưu hóa đa giác bằng approxPolyDP
        arc_len = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon_ratio * arc_len, True)
        pts_approx = approx.squeeze()
        
        if len(pts_approx.shape) < 2 or len(pts_approx) < 3:
            pts_approx = pts_orig
            if len(pts_approx.shape) < 2 or len(pts_approx) < 3:
                continue
                
        num_pts_after = len(pts_approx)
        
        norm_coords = []
        for pt in pts_approx:
            x_norm = np.clip(pt[0] / float(width), 0.0, 1.0)
            y_norm = np.clip(pt[1] / float(height), 0.0, 1.0)
            norm_coords.append(f"{x_norm:.6f} {y_norm:.6f}")
            
        line = f"0 {' '.join(norm_coords)}\n"
        yolo_lines.append(line)
        
        poly_stats.append({
            "area": area,
            "num_points_before": num_pts_before,
            "num_points_after": num_pts_after,
            "bbox_width": bw,
            "bbox_height": bh,
            "bbox_area": bbox_area,
            "aspect_ratio": aspect_ratio
        })
        
    return yolo_lines, poly_stats, (width, height)


def main():
    base_dir = Path(r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive")
    logger.info(f"Thư mục gốc làm việc: {base_dir}")
    
    # 1. Định vị các đường dẫn dữ liệu đầu vào
    images_dir = base_dir / "Kvasir-SEG" / "Kvasir-SEG" / "images"
    masks_dir = base_dir / "Kvasir-SEG" / "Kvasir-SEG" / "masks"
    train_txt_path = base_dir / "train.txt"
    val_txt_path = base_dir / "val.txt"
    
    cecum_dir = base_dir / "normal-cecum" / "normal-cecum"
    if not cecum_dir.exists():
        cecum_dir = base_dir / "normal-cecum"
        
    output_dir = base_dir / "Kvasir_YOLO_SEG_BG20"
    
    logger.info("Kiểm tra sự tồn tại của dữ liệu nguồn:")
    logger.info(f"  - Kvasir Images   : {images_dir} ({'Tồn tại' if images_dir.exists() else 'THIẾU!'})")
    logger.info(f"  - Kvasir Masks    : {masks_dir} ({'Tồn tại' if masks_dir.exists() else 'THIẾU!'})")
    logger.info(f"  - Train Split     : {train_txt_path} ({'Tồn tại' if train_txt_path.exists() else 'THIẾU!'})")
    logger.info(f"  - Val Split       : {val_txt_path} ({'Tồn tại' if val_txt_path.exists() else 'THIẾU!'})")
    logger.info(f"  - Normal Cecum Dir: {cecum_dir} ({'Tồn tại' if cecum_dir.exists() else 'THIẾU!'})")
    logger.info(f"  - Output Target   : {output_dir}")
    
    assert images_dir.exists(), f"Không tìm thấy thư mục: {images_dir}"
    assert masks_dir.exists(), f"Không tìm thấy thư mục: {masks_dir}"
    assert train_txt_path.exists(), f"Không tìm thấy file: {train_txt_path}"
    assert val_txt_path.exists(), f"Không tìm thấy file: {val_txt_path}"
    assert cecum_dir.exists(), f"Không tìm thấy thư mục: {cecum_dir}"
    
    # 2. Đọc danh sách ID gốc
    with open(train_txt_path, "r", encoding="utf-8") as f:
        train_polyp_ids = [line.strip() for line in f if line.strip()]
    with open(val_txt_path, "r", encoding="utf-8") as f:
        val_polyp_ids = [line.strip() for line in f if line.strip()]
        
    logger.info(f"Số lượng ảnh polyp gốc: Train = {len(train_polyp_ids)} | Val = {len(val_polyp_ids)}")
    assert len(train_polyp_ids) == 880, f"Kỳ vọng 880 ảnh train polyp, thực tế: {len(train_polyp_ids)}"
    assert len(val_polyp_ids) == 120, f"Kỳ vọng 120 ảnh val polyp, thực tế: {len(val_polyp_ids)}"
    
    # 3. Lấy mẫu 200 ảnh nền từ normal-cecum cố định seed 42
    all_cecum_files = sorted(list(cecum_dir.glob("*.jpg")))
    logger.info(f"Tổng số ảnh normal-cecum quét được: {len(all_cecum_files)} ảnh")
    assert len(all_cecum_files) >= 200, f"Cần tối thiểu 200 ảnh normal-cecum, chỉ có: {len(all_cecum_files)}"
    
    random.seed(42)
    selected_cecum = random.sample(all_cecum_files, 200)
    cecum_train = selected_cecum[:160]
    cecum_val = selected_cecum[160:]
    
    logger.info(f"Phân chia ảnh nền normal-cecum: Train = {len(cecum_train)} ảnh | Val = {len(cecum_val)} ảnh")
    
    # 4. Khởi tạo cấu trúc thư mục đầu ra
    if output_dir.exists():
        logger.warning(f"Thư mục {output_dir} đã tồn tại. Tiến hành làm sạch thư mục cũ...")
        shutil.rmtree(output_dir)
        
    for sub in ["images/train", "images/val", "labels/train", "labels/val"]:
        (output_dir / sub).mkdir(parents=True, exist_ok=True)
        
    # Lưu vết 2 danh sách ảnh nền đã chọn
    with open(output_dir / "selected_normal_cecum_train_160.txt", "w", encoding="utf-8") as f:
        f.writelines([f"{p.name}\n" for p in cecum_train])
    with open(output_dir / "selected_normal_cecum_val_40.txt", "w", encoding="utf-8") as f:
        f.writelines([f"{p.name}\n" for p in cecum_val])
    logger.info("Đã xuất lưu vết ID của 200 ảnh nền ra 2 file txt tương ứng.")
    
    # 5. Xử lý sao chép và chuyển đổi ảnh Polyp
    total_polyps_converted = {"train": 0, "val": 0}
    
    for split_name, id_list in [("train", train_polyp_ids), ("val", val_polyp_ids)]:
        logger.info(f"--- Đang xử lý tập POLYP [{split_name.upper()}] ({len(id_list)} ảnh) ---")
        for img_id in tqdm(id_list, desc=f"Polyp {split_name}", unit="img"):
            clean_id = img_id[:-4] if img_id.lower().endswith(".jpg") else img_id
            src_img = images_dir / f"{clean_id}.jpg"
            src_mask = masks_dir / f"{clean_id}.jpg"
            
            dst_img = output_dir / "images" / split_name / f"{clean_id}.jpg"
            dst_lbl = output_dir / "labels" / split_name / f"{clean_id}.txt"
            
            shutil.copy2(src_img, dst_img)
            yolo_lines, _, _ = convert_mask_to_yolo_polygons(src_mask)
            
            with open(dst_lbl, "w", encoding="utf-8") as f:
                f.writelines(yolo_lines)
            total_polyps_converted[split_name] += len(yolo_lines)
            
    # 6. Xử lý sao chép ảnh Nền và tạo file nhãn rỗng 0 byte
    for split_name, cecum_list in [("train", cecum_train), ("val", cecum_val)]:
        logger.info(f"--- Đang xử lý tập NỀN (BACKGROUND) [{split_name.upper()}] ({len(cecum_list)} ảnh) ---")
        for src_img in tqdm(cecum_list, desc=f"Background {split_name}", unit="img"):
            # Thêm tiền tố bg_cecum_ để tránh trùng lặp tên file
            bg_id = f"bg_{src_img.stem}"
            dst_img = output_dir / "images" / split_name / f"{bg_id}.jpg"
            dst_lbl = output_dir / "labels" / split_name / f"{bg_id}.txt"
            
            shutil.copy2(src_img, dst_img)
            
            # Tạo file nhãn rỗng (0-byte) cho ảnh nền
            with open(dst_lbl, "w", encoding="utf-8") as f:
                pass  # Đúng chuẩn file 0 byte của Ultralytics
                
    # 7. Kiểm định tính toàn vẹn (Sanity Check)
    logger.info("--- TIẾN HÀNH KIỂM ĐỊNH TOÀN DIỆN DATASET MỚI ---")
    train_imgs = list((output_dir / "images/train").glob("*.jpg"))
    train_lbls = list((output_dir / "labels/train").glob("*.txt"))
    val_imgs = list((output_dir / "images/val").glob("*.jpg"))
    val_lbls = list((output_dir / "labels/val").glob("*.txt"))
    
    logger.info(f"  * Train Images: {len(train_imgs)} (Kỳ vọng: 1040 = 880 polyp + 160 nền)")
    logger.info(f"  * Train Labels: {len(train_lbls)} (Kỳ vọng: 1040)")
    logger.info(f"  * Val Images  : {len(val_imgs)} (Kỳ vọng: 160 = 120 polyp + 40 nền)")
    logger.info(f"  * Val Labels  : {len(val_lbls)} (Kỳ vọng: 160)")
    
    assert len(train_imgs) == 1040 and len(train_lbls) == 1040, "Sai lệch số lượng tập train!"
    assert len(val_imgs) == 160 and len(val_lbls) == 160, "Sai lệch số lượng tập val!"
    
    # Kiểm tra số lượng file rỗng (0 byte)
    empty_train_lbls = [p for p in train_lbls if p.stat().st_size == 0]
    empty_val_lbls = [p for p in val_lbls if p.stat().st_size == 0]
    logger.info(f"  * Số file nhãn rỗng tập Train: {len(empty_train_lbls)} (Kỳ vọng: 160)")
    logger.info(f"  * Số file nhãn rỗng tập Val  : {len(empty_val_lbls)} (Kỳ vọng: 40)")
    
    assert len(empty_train_lbls) == 160, "Số lượng file rỗng train không đúng 160!"
    assert len(empty_val_lbls) == 40, "Số lượng file rỗng val không đúng 40!"
    
    # 8. Sinh file data_bg20.yaml
    yaml_content = f"""# Dataset Kvasir-SEG mở rộng bổ sung 20% ảnh nền âm tính (normal-cecum)
path: {str(output_dir.resolve()).replace('\\', '/')}
train: images/train
val: images/val

names:
  0: polyp

metadata:
  total_images: 1200
  train_images: 1040  # 880 polyp + 160 background
  val_images: 160     # 120 polyp + 40 background
  background_source: normal-cecum (Kvasir v2)
  random_seed: 42
"""
    yaml_path = output_dir / "data_bg20.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    logger.info(f"Đã tạo file cấu hình Ultralytics tại: {yaml_path}")
    
    # Cũng xuất 1 bản copy ra root archive để tiện dùng
    root_yaml_path = base_dir / "data_bg20.yaml"
    with open(root_yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    logger.info(f"Đã lưu bản sao cấu hình tại: {root_yaml_path}")
    
    # 9. Tóm tắt kết quả thành công
    summary = {
        "status": "SUCCESS",
        "output_directory": str(output_dir.resolve()),
        "dataset_yaml": str(yaml_path.resolve()),
        "train_polyp_images": 880,
        "train_background_images": 160,
        "total_train": 1040,
        "val_polyp_images": 120,
        "val_background_images": 40,
        "total_val": 160,
        "total_dataset_images": 1200,
        "empty_labels_train": len(empty_train_lbls),
        "empty_labels_val": len(empty_val_lbls),
        "total_polyps_val": total_polyps_converted["val"]
    }
    with open(output_dir / "dataset_bg20_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    logger.info("=================================================================")
    logger.info("HOÀN TẤT TIỀN XỬ LÝ: Bộ dữ liệu Kvasir_YOLO_SEG_BG20 đã sẵn sàng!")
    logger.info(f"Tổng số ảnh: 1.200 (1.040 train / 160 val) | YAML: {yaml_path}")
    logger.info("=================================================================")


if __name__ == "__main__":
    main()
