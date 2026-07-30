import argparse
import csv
import hashlib
import json
import os
import random
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np


def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def find_files(directory, extensions):
    """
    Find files by extension and group them by stem.
    Fails if there are multiple files with the same stem.
    """
    directory = Path(directory)
    if not directory.is_dir():
        raise NotADirectoryError(f"Directory not found: {directory}")

    stem_to_path = {}
    for filepath in directory.rglob("*"):
        if filepath.is_file() and filepath.suffix.lower() in extensions:
            stem = filepath.stem
            if stem in stem_to_path:
                raise ValueError(
                    f"Duplicate stem found in {directory}:\n"
                    f"1) {stem_to_path[stem]}\n"
                    f"2) {filepath}"
                )
            stem_to_path[stem] = filepath
    return stem_to_path


def binarize_mask(mask_path, out_path, threshold=127):
    """
    Reads a mask to grayscale, applies a >threshold,
    and saves as a lossless PNG. Returns True if successful.
    """
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise ValueError(f"Could not read mask: {mask_path}")

    _, binary_mask = cv2.threshold(mask, threshold, 255, cv2.THRESH_BINARY)

    # Check for empty or full masks
    unique_vals = np.unique(binary_mask)
    if len(unique_vals) == 1:
        val = unique_vals[0]
        if val == 0:
            print(f"WARNING: Mask is entirely background (empty): {mask_path}")
        elif val == 255:
            print(f"WARNING: Mask is entirely foreground (full): {mask_path}")
        # Not raising error, just warning, as it can happen in real data, but we flag it.

    # Strict check for only 0 and 255
    if not np.all(np.isin(unique_vals, [0, 255])):
        raise ValueError(f"Binary mask contains values other than 0 and 255: {unique_vals}")

    cv2.imwrite(str(out_path), binary_mask, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    
    # Calculate stats for QA
    fg_pixels = np.count_nonzero(binary_mask)
    num_labels, _, _, _ = cv2.connectedComponentsWithStats(binary_mask, connectivity=8)
    # num_labels includes background, so components = num_labels - 1
    components = max(0, num_labels - 1)
    
    return fg_pixels, binary_mask.size, components, binary_mask


def generate_preview(img_path, gt_mask_path, out_path):
    """
    Generates a 3-panel preview: Original | GT Mask | Overlay
    """
    img = cv2.imread(str(img_path))
    gt_mask = cv2.imread(str(gt_mask_path), cv2.IMREAD_GRAYSCALE)
    
    if img is None or gt_mask is None:
        return
        
    # Resize GT mask to match image if for some reason they differ in shape
    # (Though we shouldn't have changed resolution)
    if gt_mask.shape[:2] != img.shape[:2]:
        gt_mask = cv2.resize(gt_mask, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)

    # Convert GT to BGR for concatenation
    gt_mask_bgr = cv2.cvtColor(gt_mask, cv2.COLOR_GRAY2BGR)
    
    # Create overlay (GT in red)
    overlay = img.copy()
    red_mask = np.zeros_like(img)
    red_mask[:, :, 2] = 255
    
    # Only color the foreground pixels
    alpha = 0.5
    overlay_idx = gt_mask == 255
    overlay[overlay_idx] = cv2.addWeighted(img, 1 - alpha, red_mask, alpha, 0)[overlay_idx]

    # Concatenate horizontally
    preview = np.hstack([img, gt_mask_bgr, overlay])
    cv2.imwrite(str(out_path), preview)


def check_idempotency(out_dir):
    """
    Checks if output dataset exists and is complete by validating the manifest.
    """
    out_dir = Path(out_dir)
    manifest_path = out_dir / "split_manifest.csv"
    if not manifest_path.exists():
        return False

    print("Found existing dataset. Validating integrity from manifest...")
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                img_out = out_dir / row["output_image"]
                mask_orig_out = out_dir / row["output_mask_original"]
                mask_bin_out = out_dir / row["output_mask_binary"]

                if not img_out.exists() or calculate_sha256(img_out) != row["image_hash"]:
                    return False
                if not mask_orig_out.exists() or calculate_sha256(mask_orig_out) != row["mask_hash"]:
                    return False
                if not mask_bin_out.exists():
                    return False
        return True
    except Exception as e:
        print(f"Validation failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Prepare Kvasir-SEG Semantic Segmentation Dataset")
    parser.add_argument("--images-dir", required=True, help="Path to original images directory")
    parser.add_argument("--masks-dir", required=True, help="Path to original masks directory")
    parser.add_argument("--train-list", required=True, help="Path to train.txt (list of stems)")
    parser.add_argument("--val-list", required=True, help="Path to val.txt (list of stems)")
    parser.add_argument("--output-dir", required=True, help="Path to output directory")
    parser.add_argument("--expected-train-count", type=int, default=880, help="Expected number of train images")
    parser.add_argument("--expected-val-count", type=int, default=120, help="Expected number of val images")
    parser.add_argument("--mask-threshold", type=int, default=127, help="Threshold for binarizing mask")
    parser.add_argument("--preview-count", type=int, default=3, help="Number of random previews per split")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing dataset")

    args = parser.parse_args()

    out_dir = Path(args.output_dir)

    if out_dir.exists():
        if not args.overwrite:
            if check_idempotency(out_dir):
                print(f"Dataset already exists and is complete at {out_dir}. Skipping.")
                return
            else:
                print(f"ERROR: Output directory {out_dir} exists but is incomplete or corrupted.")
                print("Use --overwrite to force recreation.")
                sys.exit(1)
        else:
            print(f"Overwriting existing directory {out_dir}...")
            shutil.rmtree(out_dir)

    # 1. Read Splits
    with open(args.train_list, "r") as f:
        train_stems = [line.strip() for line in f if line.strip()]
    with open(args.val_list, "r") as f:
        val_stems = [line.strip() for line in f if line.strip()]

    # Duplicate stems in split check
    if len(train_stems) != len(set(train_stems)):
        raise ValueError("Duplicate stems found in train.txt")
    if len(val_stems) != len(set(val_stems)):
        raise ValueError("Duplicate stems found in val.txt")

    # Cross-split overlap check
    overlap = set(train_stems).intersection(set(val_stems))
    if overlap:
        raise ValueError(f"Found {len(overlap)} overlapping stems between train and val: {overlap}")

    if len(train_stems) != args.expected_train_count:
        raise ValueError(f"Expected {args.expected_train_count} train samples, found {len(train_stems)}")
    if len(val_stems) != args.expected_val_count:
        raise ValueError(f"Expected {args.expected_val_count} val samples, found {len(val_stems)}")

    # 2. Find files
    img_exts = {".jpg", ".jpeg", ".png"}
    mask_exts = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

    img_paths = find_files(args.images_dir, img_exts)
    mask_paths = find_files(args.masks_dir, mask_exts)

    # 3. Setup output structure
    splits = ["train", "val"]
    for split in splits:
        (out_dir / split / "images").mkdir(parents=True, exist_ok=True)
        (out_dir / split / "masks_original").mkdir(parents=True, exist_ok=True)
        (out_dir / split / "masks_binary").mkdir(parents=True, exist_ok=True)
        (out_dir / "qa" / "previews" / split).mkdir(parents=True, exist_ok=True)
    
    (out_dir / "splits").mkdir(parents=True, exist_ok=True)
    shutil.copy(args.train_list, out_dir / "splits" / "train.txt")
    shutil.copy(args.val_list, out_dir / "splits" / "val.txt")

    # 4. Processing Loop
    manifest_data = []
    seen_img_hashes = set()
    seen_mask_hashes = set()
    qa_stats = {"train": [], "val": []}
    
    for split, stems in [("train", train_stems), ("val", val_stems)]:
        print(f"Processing {split} split...")
        for stem in stems:
            if stem not in img_paths:
                raise FileNotFoundError(f"Missing image for stem: {stem}")
            if stem not in mask_paths:
                raise FileNotFoundError(f"Missing mask for stem: {stem}")

            src_img = img_paths[stem]
            src_mask = mask_paths[stem]

            img_hash = calculate_sha256(src_img)
            mask_hash = calculate_sha256(src_mask)

            # Content duplicate check
            if img_hash in seen_img_hashes:
                raise ValueError(f"Duplicate image content found for {src_img} (hash: {img_hash})")
            if mask_hash in seen_mask_hashes:
                raise ValueError(f"Duplicate mask content found for {src_mask} (hash: {mask_hash})")
            
            seen_img_hashes.add(img_hash)
            seen_mask_hashes.add(mask_hash)

            # Define output paths
            out_img = out_dir / split / "images" / src_img.name
            out_mask_orig = out_dir / split / "masks_original" / src_mask.name
            out_mask_bin = out_dir / split / "masks_binary" / f"{stem}.png"

            # Copy and verify
            shutil.copy2(src_img, out_img)
            shutil.copy2(src_mask, out_mask_orig)

            if calculate_sha256(out_img) != img_hash:
                raise IOError(f"Hash mismatch after copying image: {out_img}")
            if calculate_sha256(out_mask_orig) != mask_hash:
                raise IOError(f"Hash mismatch after copying mask: {out_mask_orig}")

            # Binarize
            fg_pixels, total_pixels, components, _ = binarize_mask(out_mask_orig, out_mask_bin, threshold=args.mask_threshold)

            # Record stats
            qa_stats[split].append({
                "stem": stem,
                "fg_pixels": fg_pixels,
                "fg_ratio": fg_pixels / total_pixels,
                "components": components,
                "img_path": out_img,
                "mask_bin_path": out_mask_bin
            })

            # Append to manifest
            manifest_data.append({
                "split": split,
                "stem": stem,
                "source_image": str(src_img.resolve()),
                "source_mask": str(src_mask.resolve()),
                "output_image": out_img.relative_to(out_dir).as_posix(),
                "output_mask_original": out_mask_orig.relative_to(out_dir).as_posix(),
                "output_mask_binary": out_mask_bin.relative_to(out_dir).as_posix(),
                "image_hash": img_hash,
                "mask_hash": mask_hash
            })

    # 5. Write Manifest
    manifest_path = out_dir / "split_manifest.csv"
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=manifest_data[0].keys())
        writer.writeheader()
        writer.writerows(manifest_data)

    # 6. QA Previews Generation
    print("Generating QA previews...")
    preview_records = []
    
    for split in ["train", "val"]:
        stats = qa_stats[split]
        if not stats:
            continue
            
        # Edge cases
        min_area = min(stats, key=lambda x: x["fg_pixels"])
        max_area = max(stats, key=lambda x: x["fg_pixels"])
        max_cc = max(stats, key=lambda x: x["components"])
        
        median_ratio = np.median([x["fg_ratio"] for x in stats])
        median_case = min(stats, key=lambda x: abs(x["fg_ratio"] - median_ratio))
        
        # Random cases
        random_cases = random.sample(stats, min(args.preview_count, len(stats)))
        
        # Combine unique cases
        cases_to_preview = {
            "min_area": min_area,
            "max_area": max_area,
            "max_components": max_cc,
            "median_ratio": median_case,
        }
        for i, c in enumerate(random_cases):
            cases_to_preview[f"random_{i}"] = c
            
        for case_name, case_data in cases_to_preview.items():
            out_preview = out_dir / "qa" / "previews" / split / f"{case_data['stem']}_{case_name}.png"
            generate_preview(case_data["img_path"], case_data["mask_bin_path"], out_preview)
            preview_records.append({
                "split": split,
                "case": case_name,
                "stem": case_data['stem'],
                "path": out_preview.relative_to(out_dir).as_posix()
            })

    # 7. Summary and Report
    summary = {
        "dataset_name": "Kvasir_Semantic_880_120",
        "mask_rule": f"grayscale > {args.mask_threshold} = 255, else 0. PNG lossless.",
        "threshold": args.mask_threshold,
        "foreground_rule": f"pixel > {args.mask_threshold}",
        "output_values": [0, 255],
        "train_count": len(train_stems),
        "val_count": len(val_stems),
        "total_count": len(train_stems) + len(val_stems),
        "train_val_overlap": 0
    }
    with open(out_dir / "dataset_summary.json", "w") as f:
        json.dump(summary, f, indent=4)
        
    with open(out_dir / "qa" / "qa_report.md", "w", encoding="utf-8") as f:
        f.write("# QA Report\n\n")
        f.write("## Dataset Summary\n")
        f.write(f"- Train count: {summary['train_count']}\n")
        f.write(f"- Val count: {summary['val_count']}\n")
        f.write(f"- Mask threshold rule: {summary['mask_rule']}\n\n")
        f.write("## Previews\n")
        for rec in preview_records:
            f.write(f"### {rec['split']} - {rec['case']} ({rec['stem']})\n")
            f.write(f"![{rec['case']}](../{rec['path']})\n\n")

    print(f"Successfully prepared dataset at {out_dir}")

if __name__ == "__main__":
    main()
