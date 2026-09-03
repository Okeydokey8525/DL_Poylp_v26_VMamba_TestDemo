#!/usr/bin/env python3
"""
convert_datasets_to_yolo_seg.py
================================
Author: Senior AI Engineer (Computer Vision & Medical AI)
Description:
    Convert CVC-ClinicDB, CVC-ColonDB, and ETIS-Larib PolypDB datasets into
    standard Ultralytics YOLOv11-seg, YOLOv12-seg, and YOLO26-seg segmentation format.
    
    Adheres 100% to the exact quality, preprocessing, and statistical pipeline established
    by convert_kvasir_to_yolo_seg.py:
    1. Polygon Optimization: cv2.approxPolyDP with epsilon_ratio (0.002).
    2. Adaptive Thresholding: cv2.THRESH_BINARY + cv2.THRESH_OTSU.
    3. Morphological Cleaning: 3x3 Morphological Close (1 iteration).
    4. Dataset Statistics CSV: Exports granular per-object metrics to dataset_statistics.csv.
    5. Enhanced Reporting: COCO Object Size Classification, Min/Max/Median/Mean/Std metrics.
    6. Side-by-Side Visual Previews: Renders 20 previews [Original | Ground Truth Mask | YOLO Overlay].
    7. Publication-Ready Plots: Exports 5 high-res (300 DPI) distribution charts to dataset_plots/.
    8. Machine-Readable Summary: Exports full statistics to dataset_summary.json.
    9. Dataset YAML: Generates clean, ready-to-train dataset.yaml.
    10. Rigorous Validation: 100% checks for coordinate bounds, class ID, point counts, no duplicates.
"""

import os
import sys
import csv
import json
import shutil
import random
import argparse
import logging
from pathlib import Path
from collections import Counter
from typing import List, Tuple, Dict, Any

import cv2
import numpy as np
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')  # Headless backend
import matplotlib.pyplot as plt

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("PolypYOLOConverter")


# ---------------------------------------------------------------------------
# Dataset Configurations
# ---------------------------------------------------------------------------
DATASET_CONFIGS = {
    "clinicdb": {
        "name": "CVC-ClinicDB",
        "output_name": "CVC_ClinicDB_YOLO_SEG",
        "images_dir": Path("CVC-ClinicDB/PNG/Original"),
        "masks_dir": Path("CVC-ClinicDB/PNG/Ground Truth"),
        "img_ext": ".png",
        "mask_ext": ".png",
        "train_ratio": 0.80,
        "seed": 42
    },
    "colondb": {
        "name": "CVC-ColonDB",
        "output_name": "CVC_ColonDB_YOLO_SEG",
        "images_dir": Path("CVC-ColonDB_data/CVC-ColonDB/images"),
        "masks_dir": Path("CVC-ColonDB_data/CVC-ColonDB/masks"),
        "img_ext": ".png",
        "mask_ext": ".png",
        "train_ratio": 0.80,
        "seed": 42
    },
    "etis": {
        "name": "ETIS-Larib PolypDB",
        "output_name": "ETIS_Larib_YOLO_SEG",
        "images_dir": Path("ETIS-Larib PolypDB/images"),
        "masks_dir": Path("ETIS-Larib PolypDB/masks"),
        "img_ext": ".png",
        "mask_ext": ".png",
        "train_ratio": 0.80,
        "seed": 42
    }
}


def create_output_structure(output_dir: Path) -> None:
    """
    Create standard YOLO segmentation directory structure along with plots and preview folders.
    """
    logger.info(f"Creating output structure at: {output_dir.resolve()}")
    if output_dir.exists():
        logger.warning(f"Output directory {output_dir} already exists. Cleaning old splits to prevent stale data...")
        if (output_dir / "images").exists():
            shutil.rmtree(output_dir / "images")
        if (output_dir / "labels").exists():
            shutil.rmtree(output_dir / "labels")
        
    subdirs = [
        "images/train",
        "images/val",
        "labels/train",
        "labels/val",
        "preview",
        "dataset_plots"
    ]
    
    for sub in subdirs:
        (output_dir / sub).mkdir(parents=True, exist_ok=True)


def convert_mask_to_yolo_polygons(
    mask_path: Path, 
    min_area: float = 20.0, 
    epsilon_ratio: float = 0.002
) -> Tuple[List[str], List[Dict[str, Any]], Tuple[int, int]]:
    """
    Convert a binary segmentation mask into YOLO normalized polygon strings
    using Adaptive Otsu Thresholding, Morphological Close, and approxPolyDP optimization.
    """
    mask = cv2.imread(str(mask_path))
    if mask is None:
        raise ValueError(f"Failed to read mask file: {mask_path}")
        
    if len(mask.shape) == 3:
        gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    else:
        gray = mask
        
    height, width = gray.shape[:2]
    
    # 1. Adaptive Thresholding using OTSU + THRESH_BINARY
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 2. Morphological Cleaning: 3x3 kernel, Morph Close strictly once
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # 3. Find external contours
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
        
        # 4. Polygon Optimization using cv2.approxPolyDP
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


def get_dataset_splits(
    images_dir: Path, 
    img_ext: str, 
    train_ratio: float = 0.80, 
    seed: int = 42
) -> Tuple[List[str], List[str]]:
    """
    Split dataset image stems into train and val lists using reproducible seed.
    """
    files = sorted(list(images_dir.glob(f"*{img_ext}")))
    if not files:
        # Fallback to any image extension if specific extension not matched
        files = sorted(list(images_dir.glob("*.*")))
        
    stems = sorted([f.stem for f in files if f.is_file()])
    if not stems:
        raise FileNotFoundError(f"No image files found in {images_dir}")
        
    random.seed(seed)
    shuffled = stems.copy()
    random.shuffle(shuffled)
    
    n_train = int(len(shuffled) * train_ratio)
    train_ids = sorted(shuffled[:n_train])
    val_ids = sorted(shuffled[n_train:])
    
    return train_ids, val_ids


def process_dataset_split(
    split_name: str,
    id_list: List[str],
    images_dir: Path,
    masks_dir: Path,
    output_dir: Path,
    img_ext: str = ".png",
    mask_ext: str = ".png",
    epsilon_ratio: float = 0.002
) -> List[Dict[str, Any]]:
    """
    Process a dataset split (train or val), copying images and generating YOLO labels.
    """
    logger.info(f"Processing split [{split_name.upper()}] ({len(id_list)} samples)...")
    split_stats = []
    
    for img_id in tqdm(id_list, desc=f"Converting {split_name}", unit="img"):
        clean_id = img_id.strip()
        if not clean_id:
            continue
            
        src_img_path = images_dir / f"{clean_id}{img_ext}"
        src_mask_path = masks_dir / f"{clean_id}{mask_ext}"
        
        if not src_img_path.exists():
            # Try finding with any case or extension
            matches = list(images_dir.glob(f"{clean_id}.*"))
            if matches:
                src_img_path = matches[0]
            else:
                logger.error(f"Missing source image for ID {clean_id}: {src_img_path}")
                continue
                
        if not src_mask_path.exists():
            matches = list(masks_dir.glob(f"{clean_id}.*"))
            if matches:
                src_mask_path = matches[0]
            else:
                logger.error(f"Missing source mask for ID {clean_id}: {src_mask_path}")
                continue
            
        dst_img_path = output_dir / "images" / split_name / f"{clean_id}{src_img_path.suffix}"
        dst_lbl_path = output_dir / "labels" / split_name / f"{clean_id}.txt"
        
        shutil.copy2(src_img_path, dst_img_path)
        yolo_lines, poly_stats, (w, h) = convert_mask_to_yolo_polygons(src_mask_path, epsilon_ratio=epsilon_ratio)
        
        with open(dst_lbl_path, "w", encoding="utf-8") as f:
            f.writelines(yolo_lines)
            
        split_stats.append({
            "id": clean_id,
            "split": split_name,
            "width": w,
            "height": h,
            "num_polyps": len(yolo_lines),
            "poly_stats": poly_stats,
            "img_path": dst_img_path,
            "mask_path": src_mask_path,
            "lbl_path": dst_lbl_path
        })
        
    return split_stats


def validate_converted_dataset(
    output_dir: Path, 
    train_stats: List[Dict[str, Any]], 
    val_stats: List[Dict[str, Any]],
    expected_total: int
) -> bool:
    """
    Perform rigorous post-conversion validation checks on the generated dataset.
    """
    logger.info("Running rigorous data validation on converted YOLO dataset...")
    
    train_imgs = list((output_dir / "images/train").glob("*.*"))
    val_imgs = list((output_dir / "images/val").glob("*.*"))
    num_train_img = len(train_imgs)
    num_val_img = len(val_imgs)
    num_train_lbl = len(list((output_dir / "labels/train").glob("*.txt")))
    num_val_lbl = len(list((output_dir / "labels/val").glob("*.txt")))
    
    logger.info(f"  - Train Images: {num_train_img} | Train Labels: {num_train_lbl}")
    logger.info(f"  - Val Images  : {num_val_img} | Val Labels  : {num_val_lbl}")
    
    errors_found = 0
    total_imgs = num_train_img + num_val_img
    
    if total_imgs != expected_total:
        logger.error(f"Expected {expected_total} total samples, got {total_imgs}!")
        errors_found += 1
        
    if num_train_img != num_train_lbl:
        logger.error(f"Mismatch in train set: {num_train_img} images vs {num_train_lbl} labels!")
        errors_found += 1
    if num_val_img != num_val_lbl:
        logger.error(f"Mismatch in val set: {num_val_img} images vs {num_val_lbl} labels!")
        errors_found += 1
        
    for split in ["train", "val"]:
        imgs = {p.stem for p in (output_dir / f"images/{split}").glob("*.*")}
        lbls = {p.stem for p in (output_dir / f"labels/{split}").glob("*.txt")}
        
        missing_lbl = imgs - lbls
        missing_img = lbls - imgs
        if missing_lbl:
            logger.error(f"Split [{split}]: Images missing label files: {missing_lbl}")
            errors_found += 1
        if missing_img:
            logger.error(f"Split [{split}]: Labels missing image files: {missing_img}")
            errors_found += 1
            
    # Check for duplicate IDs across splits
    train_set = {s["id"] for s in train_stats}
    val_set = {s["id"] for s in val_stats}
    
    if train_set & val_set:
        logger.error("Duplicate images detected across train and val splits!")
        errors_found += 1
    else:
        logger.info("Confirmed zero duplicates across train and validation splits.")
            
    all_stats = train_stats + val_stats
    for stat in all_stats:
        lbl_path = stat["lbl_path"]
        with open(lbl_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line_idx, line in enumerate(lines):
            tokens = line.strip().split()
            if not tokens:
                continue
            class_id = tokens[0]
            if class_id != "0":
                logger.error(f"Invalid class ID '{class_id}' in file {lbl_path.name} (line {line_idx+1})")
                errors_found += 1
                
            coords = tokens[1:]
            if len(coords) % 2 != 0:
                logger.error(f"Odd number of coordinate values ({len(coords)}) in {lbl_path.name} (line {line_idx+1})")
                errors_found += 1
                
            num_points = len(coords) // 2
            if num_points < 3:
                logger.error(f"Polygon has fewer than 3 points ({num_points}) in {lbl_path.name} (line {line_idx+1})")
                errors_found += 1
                
            for val_str in coords:
                try:
                    val = float(val_str)
                    if val < 0.0 or val > 1.0:
                        logger.error(f"Coordinate out of [0.0, 1.0] bounds ({val}) in {lbl_path.name} (line {line_idx+1})")
                        errors_found += 1
                except ValueError:
                    logger.error(f"Non-float coordinate '{val_str}' in {lbl_path.name} (line {line_idx+1})")
                    errors_found += 1
                    
    if errors_found == 0:
        logger.info("SUCCESS: Data validation passed! All images, labels, and polygons are 100% compliant.")
        return True
    else:
        logger.warning(f"WARNING: Data validation completed with {errors_found} errors/warnings detected.")
        return False


def generate_dataset_statistics_csv(output_dir: Path, all_stats: List[Dict[str, Any]]) -> Path:
    """
    Export granular per-object dataset statistics to dataset_statistics.csv.
    """
    csv_path = output_dir / "dataset_statistics.csv"
    logger.info(f"Generating dataset statistics CSV at: {csv_path}")
    
    headers = [
        "image_name", "split", "width", "height", "number_of_polyps", 
        "polygon_points", "contour_area", "bbox_width", "bbox_height", "bbox_area"
    ]
    
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for stat in all_stats:
            img_name = stat["img_path"].name
            split_name = stat["split"]
            w, h = stat["width"], stat["height"]
            num_p = stat["num_polyps"]
            
            if num_p == 0:
                writer.writerow([img_name, split_name, w, h, 0, 0, 0.0, 0, 0, 0.0])
            else:
                for poly in stat["poly_stats"]:
                    writer.writerow([
                        img_name,
                        split_name,
                        w,
                        h,
                        num_p,
                        poly["num_points_after"],
                        f"{poly['area']:.2f}",
                        poly["bbox_width"],
                        poly["bbox_height"],
                        f"{poly['bbox_area']:.2f}"
                    ])
                    
    logger.info(f"Successfully exported statistics for {len(all_stats)} images to CSV.")
    return csv_path


def generate_dataset_plots(output_dir: Path, all_stats: List[Dict[str, Any]], dataset_title: str) -> None:
    """
    Generate publication-ready statistical histogram charts in dataset_plots/.
    """
    plots_dir = output_dir / "dataset_plots"
    logger.info(f"Generating publication-ready statistical plots in '{plots_dir}'...")
    
    pts_list = [p["num_points_after"] for s in all_stats for p in s["poly_stats"]]
    area_list = [p["area"] for s in all_stats for p in s["poly_stats"]]
    barea_list = [p["bbox_area"] for s in all_stats for p in s["poly_stats"]]
    ar_list = [p["aspect_ratio"] for s in all_stats for p in s["poly_stats"]]
    res_list = [f"{s['width']}x{s['height']}" for s in all_stats]
    
    # Set clean aesthetic style
    if 'seaborn-v0_8-whitegrid' in plt.style.available:
        plt.style.use('seaborn-v0_8-whitegrid')
    elif 'seaborn-whitegrid' in plt.style.available:
        plt.style.use('seaborn-whitegrid')
    else:
        plt.style.use('default')
        
    # 1. Histogram of Polygon Points
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.hist(pts_list, bins=min(30, max(5, len(set(pts_list)))), color='#1f77b4', edgecolor='black', alpha=0.85)
    ax.set_title(f'Distribution of Optimized Polygon Points - {dataset_title}', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Number of Points', fontsize=11)
    ax.set_ylabel('Frequency (Number of Polyps)', fontsize=11)
    plt.tight_layout()
    plt.savefig(plots_dir / "hist_polygon_points.png")
    plt.close()
    
    # 2. Histogram of Contour Area
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.hist(area_list, bins=35, color='#2ca02c', edgecolor='black', alpha=0.85)
    ax.set_title(f'Distribution of Polyp Contour Area (px²) - {dataset_title}', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Contour Area (px²)', fontsize=11)
    ax.set_ylabel('Frequency (Number of Polyps)', fontsize=11)
    plt.tight_layout()
    plt.savefig(plots_dir / "hist_contour_area.png")
    plt.close()
    
    # 3. Histogram of Bounding Box Area
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.hist(barea_list, bins=35, color='#d62728', edgecolor='black', alpha=0.85)
    ax.set_title(f'Distribution of Polyp Bounding Box Area (px²) - {dataset_title}', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Bounding Box Area (px²)', fontsize=11)
    ax.set_ylabel('Frequency (Number of Polyps)', fontsize=11)
    plt.tight_layout()
    plt.savefig(plots_dir / "hist_bbox_area.png")
    plt.close()
    
    # 4. Histogram of Aspect Ratio
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.hist(ar_list, bins=35, color='#ff7f0e', edgecolor='black', alpha=0.85)
    ax.axvline(1.0, color='black', linestyle='--', linewidth=1.5, label='Aspect Ratio = 1.0 (Square)')
    ax.set_title(f'Distribution of Polyp Aspect Ratio (W/H) - {dataset_title}', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Aspect Ratio (Width / Height)', fontsize=11)
    ax.set_ylabel('Frequency (Number of Polyps)', fontsize=11)
    ax.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(plots_dir / "hist_aspect_ratio.png")
    plt.close()
    
    # 5. Histogram / Bar Plot of Image Resolutions
    res_counts = Counter(res_list).most_common(12)
    labels = [k for k, v in res_counts]
    values = [v for k, v in res_counts]
    
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    bars = ax.barh(labels[::-1], values[::-1], color='#9467bd', edgecolor='black', alpha=0.85)
    ax.set_title(f'Top Image Resolutions in {dataset_title}', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Number of Images', fontsize=11)
    ax.set_ylabel('Resolution (Width x Height)', fontsize=11)
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=9, fontweight='bold')
    plt.tight_layout()
    plt.savefig(plots_dir / "hist_image_resolution.png")
    plt.close()
    
    logger.info(f"Successfully generated 5 publication-ready plots in '{plots_dir}'.")


def generate_visual_previews(output_dir: Path, all_stats: List[Dict[str, Any]], num_samples: int = 20) -> None:
    """
    Render side-by-side comparison previews: [Original Image | Ground Truth Mask | YOLO Overlay].
    """
    logger.info(f"Generating {num_samples} side-by-side visual preview overlays in '{output_dir / 'preview'}'...")
    
    polyp_samples = [s for s in all_stats if s["num_polyps"] > 0]
    sample_pool = polyp_samples if len(polyp_samples) >= num_samples else all_stats
    
    random.seed(42)  # For consistent, reproducible preview selection
    selected_samples = random.sample(sample_pool, min(num_samples, len(sample_pool)))
    
    preview_dir = output_dir / "preview"
    
    for idx, stat in enumerate(tqdm(selected_samples, desc="Rendering previews", unit="img")):
        img_path = stat["img_path"]
        mask_path = stat["mask_path"]
        lbl_path = stat["lbl_path"]
        w, h = stat["width"], stat["height"]
        
        img_orig = cv2.imread(str(img_path))
        if img_orig is None:
            continue
            
        mask_raw = cv2.imread(str(mask_path))
        if mask_raw is None:
            continue
        if len(mask_raw.shape) == 2:
            mask_bgr = cv2.cvtColor(mask_raw, cv2.COLOR_GRAY2BGR)
        else:
            mask_bgr = mask_raw.copy()
            
        overlay_canvas = img_orig.copy()
        overlay_img = img_orig.copy()
        
        with open(lbl_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            tokens = line.strip().split()
            if not tokens or len(tokens) < 7:
                continue
                
            coords = [float(v) for v in tokens[1:]]
            pts_x = [int(coords[i] * w) for i in range(0, len(coords), 2)]
            pts_y = [int(coords[i+1] * h) for i in range(0, len(coords), 2)]
            
            polygon_pts = np.array(list(zip(pts_x, pts_y)), dtype=np.int32)
            
            cv2.fillPoly(overlay_canvas, [polygon_pts], color=(0, 255, 0))
            cv2.polylines(overlay_img, [polygon_pts], isClosed=True, color=(0, 200, 0), thickness=2)
            cv2.polylines(overlay_canvas, [polygon_pts], isClosed=True, color=(0, 200, 0), thickness=2)
            
            text_x = max(5, polygon_pts[0][0] - 10)
            text_y = max(25, polygon_pts[0][1] - 10)
            cv2.putText(overlay_canvas, "Polyp (YOLO)", (text_x, text_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2, cv2.LINE_AA)
            
        cv2.addWeighted(overlay_canvas, 0.35, overlay_img, 0.65, 0, overlay_img)
        
        header_color = (0, 255, 255)
        cv2.putText(img_orig, "1. Original Image", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, header_color, 2, cv2.LINE_AA)
        cv2.putText(mask_bgr, "2. Ground Truth Mask", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, header_color, 2, cv2.LINE_AA)
        cv2.putText(overlay_img, "3. YOLO Seg Overlay", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, header_color, 2, cv2.LINE_AA)
        
        combined_preview = np.hstack([img_orig, mask_bgr, overlay_img])
        
        preview_path = preview_dir / f"preview_{idx+1:02d}_{stat['split']}_{img_path.stem}.png"
        cv2.imwrite(str(preview_path), combined_preview)
        
    logger.info(f"Successfully generated {len(selected_samples)} side-by-side preview images.")


def generate_dataset_yaml(output_dir: Path) -> Path:
    """
    Generate dataset.yaml file formatted for Ultralytics YOLOv11/v12/v26 segmentation.
    """
    yaml_path = output_dir / "dataset.yaml"
    logger.info(f"Generating Ultralytics configuration file at: {yaml_path}")
    
    yaml_content = (
        "path: .\n"
        "train: images/train\n"
        "val: images/val\n\n"
        "names:\n"
        "  0: polyp\n"
    )
    
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
        
    return yaml_path


def compute_distribution_metrics(val_list: List[float]) -> Dict[str, float]:
    """
    Compute Min, Max, Median, Mean, and Standard Deviation for a list of numerical values.
    """
    if not val_list:
        return {"min": 0.0, "max": 0.0, "median": 0.0, "mean": 0.0, "std": 0.0}
    arr = np.array(val_list, dtype=np.float64)
    return {
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "median": float(np.median(arr)),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr))
    }


def generate_statistical_report(
    output_dir: Path, 
    train_stats: List[Dict[str, Any]], 
    val_stats: List[Dict[str, Any]],
    dataset_title: str
) -> Tuple[Path, Dict[str, Any]]:
    """
    Generate an exhaustive statistical report file (report.txt) summarizing the dataset
    including optimization metrics, Min/Max/Median/Std/Mean distributions, and COCO Size Classifications.
    """
    report_path = output_dir / "report.txt"
    logger.info(f"Generating exhaustive statistical report at: {report_path}")
    
    all_stats = train_stats + val_stats
    total_imgs = len(all_stats)
    train_imgs = len(train_stats)
    val_imgs = len(val_stats)
    
    total_polyps = sum(s["num_polyps"] for s in all_stats)
    avg_polyps = total_polyps / total_imgs if total_imgs > 0 else 0.0
    
    max_polyp_sample = max(all_stats, key=lambda x: x["num_polyps"]) if all_stats else {"id": "N/A", "num_polyps": 0}
    zero_polyp_samples = [s["id"] for s in all_stats if s["num_polyps"] == 0]
    
    pts_before_list = [p["num_points_before"] for s in all_stats for p in s["poly_stats"]]
    pts_after_list = [p["num_points_after"] for s in all_stats for p in s["poly_stats"]]
    area_list = [p["area"] for s in all_stats for p in s["poly_stats"]]
    bw_list = [p["bbox_width"] for s in all_stats for p in s["poly_stats"]]
    bh_list = [p["bbox_height"] for s in all_stats for p in s["poly_stats"]]
    barea_list = [p["bbox_area"] for s in all_stats for p in s["poly_stats"]]
    ar_list = [p["aspect_ratio"] for s in all_stats for p in s["poly_stats"]]
    
    m_bw = compute_distribution_metrics(bw_list)
    m_bh = compute_distribution_metrics(bh_list)
    m_barea = compute_distribution_metrics(barea_list)
    m_carea = compute_distribution_metrics(area_list)
    m_pts = compute_distribution_metrics(pts_after_list)
    
    pts_reduction_pct = ((np.mean(pts_before_list) - m_pts["mean"]) / np.mean(pts_before_list) * 100.0) if pts_before_list else 0.0
    
    min_area_poly = min((p["area"], s["id"]) for s in all_stats for p in s["poly_stats"]) if area_list else (0.0, "N/A")
    max_area_poly = max((p["area"], s["id"]) for s in all_stats for p in s["poly_stats"]) if area_list else (0.0, "N/A")
    
    small_objs = [a for a in area_list if a < 1024.0]
    med_objs = [a for a in area_list if 1024.0 <= a <= 9216.0]
    large_objs = [a for a in area_list if a > 9216.0]
    
    n_small = len(small_objs)
    n_med = len(med_objs)
    n_large = len(large_objs)
    n_total = len(area_list)
    
    pct_small = (n_small / n_total * 100.0) if n_total > 0 else 0.0
    pct_med = (n_med / n_total * 100.0) if n_total > 0 else 0.0
    pct_large = (n_large / n_total * 100.0) if n_total > 0 else 0.0
    
    report_content = [
        "=======================================================================",
        f"               {dataset_title.upper()} TO YOLO SEGMENTATION REPORT     ",
        "=======================================================================",
        f"Generated by: Senior AI Engineer (Computer Vision & Medical AI)",
        f"Target Models: Ultralytics YOLOv11-seg, YOLOv12-seg, YOLO26-seg",
        "",
        "1. DATASET OVERVIEW",
        "-------------------",
        f"Total Images Processed      : {total_imgs}",
        f"  - Train Images            : {train_imgs} ({train_imgs/total_imgs*100:.1f}%)",
        f"  - Validation Images       : {val_imgs} ({val_imgs/total_imgs*100:.1f}%)",
        f"Total Polyp Objects (Masks) : {total_polyps}",
        f"Average Polyps / Image      : {avg_polyps:.2f}",
        f"Image with most polyps      : {max_polyp_sample['id']} ({max_polyp_sample['num_polyps']} polyps)",
        f"Images without polyps (0)   : {len(zero_polyp_samples)} images",
        "",
        "2. POLYGON OPTIMIZATION & ANNOTATION METRICS",
        "--------------------------------------------",
        f"Avg Polygon Points (Before) : {np.mean(pts_before_list):.1f} points" if pts_before_list else "N/A",
        f"Avg Polygon Points (After)  : {m_pts['mean']:.1f} points (Reduced by {pts_reduction_pct:.1f}%)",
        f"Smallest Contour Area       : {min_area_poly[0]:.1f} px² (in file {min_area_poly[1]})",
        f"Largest Contour Area        : {max_area_poly[0]:.1f} px² (in file {max_area_poly[1]})",
        "",
        "3. GRANULAR STATISTICAL DISTRIBUTION (Min / Max / Median / Mean / Std)",
        "----------------------------------------------------------------------",
        f"  - Bbox Width (px)        : Min={m_bw['min']:.1f} | Max={m_bw['max']:.1f} | Median={m_bw['median']:.1f} | Mean={m_bw['mean']:.1f} | Std={m_bw['std']:.1f}",
        f"  - Bbox Height (px)       : Min={m_bh['min']:.1f} | Max={m_bh['max']:.1f} | Median={m_bh['median']:.1f} | Mean={m_bh['mean']:.1f} | Std={m_bh['std']:.1f}",
        f"  - Bbox Area (px²)        : Min={m_barea['min']:.1f} | Max={m_barea['max']:.1f} | Median={m_barea['median']:.1f} | Mean={m_barea['mean']:.1f} | Std={m_barea['std']:.1f}",
        f"  - Contour Area (px²)     : Min={m_carea['min']:.1f} | Max={m_carea['max']:.1f} | Median={m_carea['median']:.1f} | Mean={m_carea['mean']:.1f} | Std={m_carea['std']:.1f}",
        f"  - Polygon Points (After) : Min={int(m_pts['min'])} | Max={int(m_pts['max'])} | Median={m_pts['median']:.1f} | Mean={m_pts['mean']:.1f} | Std={m_pts['std']:.1f}",
        "",
        "4. OBJECT SIZE CLASSIFICATION (COCO Metric for Benchmarking)",
        "------------------------------------------------------------",
        f"  - Small Objects  (Area < 1024 px²)         : {n_small:3d} polyps ({pct_small:5.1f}%)",
        f"  - Medium Objects (1024 <= Area <= 9216 px²): {n_med:3d} polyps ({pct_med:5.1f}%)",
        f"  - Large Objects  (Area > 9216 px²)         : {n_large:3d} polyps ({pct_large:5.1f}%)",
        "",
        "5. INPUT SIZE & QUALITY PRESERVATION",
        "------------------------------------",
        "  - Resizing applied        : NONE (Original resolutions strictly maintained)",
        "  - Cropping/Padding        : NONE",
        "  - Lossless format         : Maintained 100%",
        "",
        "6. TARGET MODEL COMPATIBILITY & BENCHMARKING",
        "--------------------------------------------",
        "The generated dataset is ready for direct Kaggle/Colab upload and SOTA benchmarking:",
        "",
        f"  yolo segment train data={output_dir.name}/dataset.yaml model=yolo11x-seg.pt epochs=100 imgsz=640",
        f"  yolo segment train data={output_dir.name}/dataset.yaml model=yolo12x-seg.pt epochs=100 imgsz=640",
        f"  yolo segment train data={output_dir.name}/dataset.yaml model=yolo26x-seg.pt epochs=100 imgsz=640",
        "",
        "=======================================================================",
        "                         END OF REPORT                                 ",
        "======================================================================="
    ]
    
    report_text = "\n".join(report_content)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
        
    logger.info("Report summary generated:")
    print("\n" + report_text + "\n")
    
    metrics_dict = {
        "dataset_name": dataset_title,
        "overview": {
            "total_images": total_imgs,
            "train_images": train_imgs,
            "val_images": val_imgs,
            "validation_images": val_imgs,
            "total_polyps": total_polyps,
            "average_polyps_per_image": round(avg_polyps, 3),
            "max_polyps_image": max_polyp_sample['id'],
            "max_polyps_count": max_polyp_sample['num_polyps']
        },
        "polygon_optimization": {
            "avg_points_before": round(float(np.mean(pts_before_list)), 2) if pts_before_list else 0.0,
            "avg_points_after": round(m_pts["mean"], 2),
            "points_reduction_percentage": round(pts_reduction_pct, 2)
        },
        "distributions": {
            "bbox_width": m_bw,
            "bbox_height": m_bh,
            "bbox_area": m_barea,
            "contour_area": m_carea,
            "polygon_points": m_pts
        },
        "object_size_classification_coco": {
            "small_less_1024_px2": {"count": n_small, "percentage": round(pct_small, 2)},
            "medium_1024_to_9216_px2": {"count": n_med, "percentage": round(pct_med, 2)},
            "large_greater_9216_px2": {"count": n_large, "percentage": round(pct_large, 2)}
        }
    }
    
    return report_path, metrics_dict


def generate_dataset_summary_json(
    output_dir: Path, 
    metrics: Dict[str, Any]
) -> Path:
    """
    Export all dataset statistics in a clean machine-readable JSON file (dataset_summary.json).
    """
    json_path = output_dir / "dataset_summary.json"
    logger.info(f"Generating machine-readable dataset summary at: {json_path}")
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    logger.info(f"Successfully exported JSON statistics to: {json_path}")
    return json_path


def process_single_dataset(config: Dict[str, Any], base_dir: Path) -> bool:
    """
    Execute end-to-end pipeline for a single dataset configuration.
    """
    dataset_name = config["name"]
    output_name = config["output_name"]
    images_dir = base_dir / config["images_dir"]
    masks_dir = base_dir / config["masks_dir"]
    output_dir = base_dir / output_name
    img_ext = config["img_ext"]
    mask_ext = config["mask_ext"]
    train_ratio = config["train_ratio"]
    seed = config["seed"]
    
    logger.info(f"\n{'='*70}\nProcessing Dataset: {dataset_name} -> {output_name}\n{'='*70}")
    
    if not images_dir.exists():
        raise FileNotFoundError(f"Images directory not found: {images_dir}")
    if not masks_dir.exists():
        raise FileNotFoundError(f"Masks directory not found: {masks_dir}")
        
    # 1. Get split definitions
    train_ids, val_ids = get_dataset_splits(images_dir, img_ext, train_ratio=train_ratio, seed=seed)
    total_expected = len(train_ids) + len(val_ids)
    logger.info(f"Split loaded: {len(train_ids)} train samples, {len(val_ids)} val samples (Total: {total_expected}).")
    
    # 2. Create output structure
    create_output_structure(output_dir)
    
    # Save train.txt and val.txt in output_dir
    with open(output_dir / "train.txt", "w", encoding="utf-8") as f:
        for tid in train_ids:
            f.write(f"{tid}\n")
    with open(output_dir / "val.txt", "w", encoding="utf-8") as f:
        for vid in val_ids:
            f.write(f"{vid}\n")
            
    # 3. Process splits
    train_stats = process_dataset_split("train", train_ids, images_dir, masks_dir, output_dir, img_ext, mask_ext)
    val_stats = process_dataset_split("val", val_ids, images_dir, masks_dir, output_dir, img_ext, mask_ext)
    
    all_stats = train_stats + val_stats
    
    # 4. Rigorous post-conversion validation
    val_ok = validate_converted_dataset(output_dir, train_stats, val_stats, total_expected)
    if not val_ok:
        logger.error(f"Validation failed for {dataset_name}!")
        return False
        
    # 5. Export statistics CSV
    generate_dataset_statistics_csv(output_dir, all_stats)
    
    # 6. Generate 5 publication-ready distribution plots
    generate_dataset_plots(output_dir, all_stats, dataset_name)
    
    # 7. Generate 20 side-by-side visual previews
    generate_visual_previews(output_dir, all_stats, num_samples=20)
    
    # 8. Generate dataset.yaml
    generate_dataset_yaml(output_dir)
    
    # 9. Generate report.txt and dataset_summary.json
    _, metrics_dict = generate_statistical_report(output_dir, train_stats, val_stats, dataset_name)
    generate_dataset_summary_json(output_dir, metrics_dict)
    
    total_lbls = len(list((output_dir / "labels" / "train").glob("*.txt"))) + \
                 len(list((output_dir / "labels" / "val").glob("*.txt")))
                 
    print("\n" + "="*60)
    print(f"       BÁO CÁO TỔNG KẾT CHIA DATASET - {dataset_name.upper()}")
    print("="*60)
    print(f"- Số lượng train       : {len(train_stats)} ({len(train_stats)/len(all_stats)*100:.1f}%)")
    print(f"- Số lượng validation  : {len(val_stats)} ({len(val_stats)/len(all_stats)*100:.1f}%)")
    print(f"- Tổng số ảnh          : {len(all_stats)}")
    print(f"- Tổng số labels       : {total_lbls}")
    print("- Xác nhận             : KHÔNG có duplicate giữa train/val.")
    print("- Xác nhận             : KHÔNG thiếu label (đã kiểm tra 100% khớp ảnh - label).")
    print(f"- Thư mục đầu ra       : {output_dir.resolve()}")
    print("- Xác nhận             : Dataset sẵn sàng để train bằng Ultralytics YOLOv11-seg, YOLOv12-seg và YOLO26-seg.")
    print("="*60 + "\n")
    
    return True


def main():
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
            
    parser = argparse.ArgumentParser(description="Convert Medical Polyp Datasets to Ultralytics YOLOv26-seg format.")
    parser.add_argument(
        "--dataset", 
        type=str, 
        default="all", 
        choices=["clinicdb", "colondb", "etis", "all"],
        help="Target dataset to convert: clinicdb, colondb, etis, or all (default)."
    )
    args = parser.parse_args()
    
    base_dir = Path(".")
    
    logger.info("=== Starting Multi-Dataset Medical Polyp to YOLO Segmentation Pipeline ===")
    
    targets = list(DATASET_CONFIGS.keys()) if args.dataset == "all" else [args.dataset]
    
    success_count = 0
    for target in targets:
        cfg = DATASET_CONFIGS[target]
        ok = process_single_dataset(cfg, base_dir)
        if ok:
            success_count += 1
            
    logger.info(f"Pipeline finished: {success_count}/{len(targets)} datasets converted and verified successfully.")


if __name__ == "__main__":
    main()
