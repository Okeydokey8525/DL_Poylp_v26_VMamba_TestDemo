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
    - Phân bổ cuối cùng là 1.040 train / 160 validation; không phải tỷ lệ 80/20 toàn bộ.
    - Cố định lựa chọn ảnh nền bằng seed 42; độ khớp nhãn còn cần đối chiếu môi trường OpenCV.
    - Hoàn toàn KHÔNG ghi đè hay thay đổi bất kỳ file dữ liệu cũ nào.
"""

import os
import argparse
import platform
import hashlib
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
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        """Progress display is optional; the conversion algorithm is unchanged."""
        return iterable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build BG20 into a NEW directory without changing the canonical dataset or active YAML."
    )
    parser.add_argument("--archive-root", type=Path,
                        default=Path(__file__).resolve().parents[2],
                        help="Archive folder containing train.txt and val.txt")
    parser.add_argument("--source-root", type=Path, default=None,
                        help="Folder containing Kvasir-SEG and normal-cecum (relative to archive if not absolute)")
    parser.add_argument("--output", type=Path, default=Path("generated/Kvasir_YOLO_SEG_BG20_replay"),
                        help="New output folder, relative to archive if not absolute; existing folders are refused")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate inputs and background selection without writing output")
    args = parser.parse_args(argv)
    base_dir = args.archive_root.resolve()

    def archive_path(value):
        return (value if value.is_absolute() else base_dir / value).resolve()

    source_root = archive_path(args.source_root) if args.source_root else base_dir / "Ket_Qua_V2" / "Data Prosessing"
    source_root = source_root.resolve()
    output_dir = archive_path(args.output)
    images_dir = source_root / "Kvasir-SEG" / "images"
    masks_dir = source_root / "Kvasir-SEG" / "masks"
    train_txt_path = base_dir / "train.txt"
    val_txt_path = base_dir / "val.txt"
    cecum_dir = source_root / "normal-cecum"
    if (cecum_dir / "normal-cecum").is_dir():
        cecum_dir = cecum_dir / "normal-cecum"
    canonical_dir = (base_dir / "Ket_Qua_V2" / "Kvasir_YOLO_SEG_BG20").resolve()

    protected_roots = (source_root, canonical_dir, (base_dir / "Ket_Qua_V2" / "KetQua_Nen").resolve())
    if any(output_dir.is_relative_to(path) for path in protected_roots):
        parser.error("Output must be outside source data, the canonical BG20 dataset, and raw training artifacts.")
    if output_dir.exists():
        parser.error(f"Output already exists; choose a NEW folder (nothing was deleted): {output_dir}")
    for label, path in [("Kvasir images", images_dir), ("Kvasir masks", masks_dir),
                        ("train split", train_txt_path), ("validation split", val_txt_path),
                        ("normal-cecum", cecum_dir)]:
        if not path.exists():
            parser.error(f"Missing {label}: {path}")
    logger.info("Nguồn: %s | Đầu ra mới: %s", source_root, output_dir)

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
    
    # Validate individual input membership before creating any output.
    for image_id in train_polyp_ids + val_polyp_ids:
        stem = image_id[:-4] if image_id.lower().endswith(".jpg") else image_id
        for folder in (images_dir, masks_dir):
            if not (folder / f"{stem}.jpg").is_file():
                parser.error(f"Missing source file: {folder / (stem + '.jpg')}")
    train_stems = {Path(x).stem for x in train_polyp_ids}
    val_stems = {Path(x).stem for x in val_polyp_ids}
    if len(train_stems) != 880 or len(val_stems) != 120 or train_stems & val_stems:
        parser.error("Split lists must have 880/120 unique, disjoint polyp IDs.")

    if args.dry_run:
        print(json.dumps({
            "status": "DRY_RUN", "source_root": str(source_root), "output_directory": str(output_dir),
            "train_polyp_images": len(train_polyp_ids), "val_polyp_images": len(val_polyp_ids),
            "train_background_images": len(cecum_train), "val_background_images": len(cecum_val),
            "output_created": False, "active_yaml_modified": False,
            "selected_background_names": [p.name for p in selected_cecum],
            "opencv": cv2.__version__, "numpy": np.__version__
        }, ensure_ascii=False, indent=2))
        return

    # 4. Create a fresh output tree. Never delete or merge an existing directory.
    output_dir.mkdir(parents=True, exist_ok=False)
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
    logger.info("--- KIỂM TRA SỐ LƯỢNG ẢNH/NHÃN VÀ NHÃN RỖNG CỦA BẢN REPLAY ---")
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
path: {output_dir.resolve().as_posix()}
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
    
    # The canonical archive/data_bg20.yaml is intentionally never overwritten.
    environment = {
        "python": platform.python_version(), "opencv": cv2.__version__, "numpy": np.__version__,
        "seed_background": 42, "min_area": 20.0, "epsilon_ratio": 0.002,
        "train_list_sha256": hashlib.sha256(train_txt_path.read_bytes()).hexdigest(),
        "val_list_sha256": hashlib.sha256(val_txt_path.read_bytes()).hexdigest(),
        "source_root": str(source_root), "output_directory": str(output_dir),
        "active_yaml_modified": False,
        "label_reproduction_note": "Byte-identical labels depend on verified inputs and tested implementation/environment; compare before use."
    }
    (output_dir / "reproduction_environment.json").write_text(
        json.dumps(environment, ensure_ascii=False, indent=2), encoding="utf-8"
    )

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
    logger.info("ĐÃ TẠO BẢN REPLAY BG20: đối chiếu nhãn và môi trường trước khi sử dụng.")
    logger.info(f"Tổng số ảnh: 1.200 (1.040 train / 160 val) | YAML: {yaml_path}")
    logger.info("=================================================================")


if __name__ == "__main__":
    main()
