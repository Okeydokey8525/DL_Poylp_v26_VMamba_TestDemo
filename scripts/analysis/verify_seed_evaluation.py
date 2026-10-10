"""Audit saved CSVs and isolate head selection versus fusion in fresh processes.

Run --help. Requires the ORIGINAL custom Ultralytics package only for evaluation.
Never edits checkpoints, original run plots, or original CSVs.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

ARMS = ("many_unfused", "many_fused", "one_unfused", "one_fused")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")


def best_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        rows = [{key.strip(): value.strip() for key, value in row.items()} for row in csv.DictReader(handle)]
    if len(rows) != 100 or [int(row["epoch"]) for row in rows] != list(range(1, 101)):
        raise ValueError(f"Expected epochs 1..100 exactly: {path}")
    keys = [key for key in rows[0] if key.startswith("metrics/")]
    for row in rows:
        for key in keys:
            value = float(row[key])
            if not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"Invalid metric {key}: {path}, epoch {row['epoch']}")
    # This is a CSV selection rule, not proof of which epoch produced best.pt.
    best = max(rows, key=lambda row: float(row["metrics/mAP50-95(M)"]))
    peak50 = max(rows, key=lambda row: float(row["metrics/mAP50(M)"]))
    return {"csv_sha256": sha256(path), "selection": "maximum Mask mAP50-95",
            "epoch": int(best["epoch"]), "metrics": {key: float(best[key]) for key in keys},
            "peak_mask_map50_epoch": int(peak50["epoch"]),
            "peak_mask_map50": float(peak50["metrics/mAP50(M)"])}


def dataset_manifest(root):
    """Reject missing labels; never reinterpret a missing label as normal tissue."""
    root = Path(root).resolve()
    images = sorted(p for p in (root / "images/val").rglob("*") if p.suffix.lower() in IMAGE_SUFFIXES)
    records, backgrounds, instances = [], [], 0
    for image in images:
        relative = image.relative_to(root / "images/val")
        label = (root / "labels/val" / relative).with_suffix(".txt")
        if not label.is_file():
            raise ValueError(f"Missing label: {label}")
        lines = [line.split() for line in label.read_text(encoding="utf-8").splitlines() if line.strip()]
        for line in lines:
            numbers = [float(value) for value in line]
            if numbers[0] != 0 or len(numbers) < 7 or (len(numbers) - 1) % 2:
                raise ValueError(f"Expected class-0 segmentation polygon: {label}")
            if any(not math.isfinite(value) or not 0 <= value <= 1 for value in numbers[1:]):
                raise ValueError(f"Invalid polygon coordinates: {label}")
        instances += len(lines)
        if not lines:
            backgrounds.append(str(image))
        records.append({"image": relative.as_posix(), "image_sha256": sha256(image),
                        "label_sha256": sha256(label), "instances": len(lines)})
    counts = {"images": len(images), "background_images": len(backgrounds), "instances": instances}
    if counts != {"images": 160, "background_images": 40, "instances": 127}:
        raise ValueError(f"BG20 validation counts mismatch: {counts}")
    digest = hashlib.sha256(json.dumps(records, sort_keys=True).encode()).hexdigest()
    return {"root": str(root), "counts": counts, "sha256": digest, "records": records,
            "background_paths": backgrounds}


def architecture(model):
    head = model.model[-1]
    return {"head": type(head).__name__, "end2end": bool(head.end2end),
            "parameters": sum(p.numel() for p in model.parameters()),
            "one2many_present": all(getattr(head, key, None) is not None for key in ("cv2", "cv3", "cv4")),
            "one2one_present": all(getattr(head, key, None) is not None for key in
                                    ("one2one_cv2", "one2one_cv3", "one2one_cv4"))}


def comparisons(summary):
    """Report evidence without selecting a winning arm or replacing report data."""
    output = []
    for seed in summary["csv_audit"]:
        groups = {arm: [t["result"] for t in summary["trials"]
                        if str(t["seed"]) == seed and t["arm"] == arm and "result" in t] for arm in ARMS}
        row = {"seed": int(seed), "arms": {}, "fusion_deltas": {}}
        reference = summary["csv_audit"][seed]["metrics"]
        for arm, results in groups.items():
            if not results:
                continue
            keys = [key for key in reference if key in results[0]["metrics"]]
            row["arms"][arm] = {
                "metrics_minus_csv": {key: results[0]["metrics"][key] - reference[key] for key in keys},
                "repeats": len(results),
                "repeat_max_absolute_difference": max(
                    (abs(r["metrics"][key] - results[0]["metrics"][key])
                     for r in results[1:] for key in keys), default=None),
                "same_inputs_and_source": len({(r["checkpoint_sha256"], r["dataset_sha256"],
                                                  r["python_source_sha256"]) for r in results}) == 1}
        for head in ("many", "one"):
            fused, unfused = groups[f"{head}_fused"], groups[f"{head}_unfused"]
            if fused and unfused:
                row["fusion_deltas"][head] = {
                    key: fused[0]["metrics"][key] - unfused[0]["metrics"][key]
                    for key in reference if key in fused[0]["metrics"] and key in unfused[0]["metrics"]}
        output.append(row)
    return output


def worker(args):
    # Run in the Kaggle environment used for training: no pip upgrade here.
    import torch
    import ultralytics
    from ultralytics import YOLO
    from ultralytics.nn.tasks import BaseModel
    from ultralytics.utils.torch_utils import init_seeds

    out = Path(args.out).resolve()
    manifest = dataset_manifest(args.dataset_root)
    checkpoint = Path(args.checkpoint).resolve()
    original_hash = sha256(checkpoint)
    init_seeds(args.seed, deterministic=True)
    yolo = YOLO(str(checkpoint))
    model = yolo.model
    before = architecture(model)
    if not before["one2many_present"] or not before["one2one_present"]:
        raise ValueError("Checkpoint must contain BOTH segmentation heads before comparison")
    head = model.model[-1]
    head.end2end = args.arm.startswith("one_")
    if bool(head.end2end) != args.arm.startswith("one_"):
        raise ValueError("Head selection failed; check for a previous global Detect.end2end patch")
    fusion_calls = []
    original_fuse = BaseModel.fuse

    def controlled_fuse(self, *positional, **keywords):
        fusion_calls.append(args.arm)
        if args.arm.endswith("_unfused"):
            return self
        return original_fuse(self, *positional, **keywords)

    # Intercept actual model fusion, independent of AutoBackend signature changes.
    # Process-local patch is restored below; other trials use fresh processes.
    BaseModel.fuse = controlled_fuse
    data = out / "data.yaml"
    import yaml
    data.write_text(yaml.safe_dump({"path": str(Path(args.dataset_root).resolve()),
                                   "train": "images/train", "val": "images/val",
                                   "names": {0: "polyp"}}), encoding="utf-8")
    try:
        settings = dict(data=str(data), split="val", imgsz=args.imgsz, batch=args.batch,
                        device=args.device, workers=0, half=False, augment=False,
                        conf=0.001, iou=0.7, max_det=300, rect=True, plots=True,
                        save_json=True, save_txt=True, save_conf=True,
                        project=str(out), name="validation", exist_ok=False)
        metrics = yolo.val(**settings)
        after = architecture(model)
        if not fusion_calls:
            raise RuntimeError("Fusion hook was not called; this version needs separate verification")
        if after["end2end"] != args.arm.startswith("one_"):
            raise RuntimeError("Unexpected head selection after validation")
        if args.arm.endswith("_unfused") and (after["parameters"] != before["parameters"]
                                                or not after["one2many_present"]):
            raise RuntimeError("Unfused trial changed model structure")
        values = {key: float(value) for key, value in metrics.results_dict.items()}
        if any(not math.isfinite(value) for value in values.values()):
            raise RuntimeError("Validation produced non-finite metrics")
        # Explicit image-level specificity at a fixed operating threshold.
        # This separate prediction pass is NOT the AP/maximum-F1 operating point.
        background_rows = []
        for result in yolo.predict(source=manifest["background_paths"], stream=True,
                                   imgsz=args.imgsz, batch=args.batch, device=args.device,
                                   half=False, augment=False, conf=0.25, iou=0.7,
                                   max_det=300, rect=True, save=False, verbose=False):
            background_rows.append({"image": str(result.path), "predictions": len(result.boxes)})
        if len(background_rows) != 40 or len({row["image"] for row in background_rows}) != 40:
            raise RuntimeError("Background prediction did not cover 40 unique images")
        fp_images = sum(row["predictions"] > 0 for row in background_rows)
        package_root = Path(ultralytics.__file__).parent
        source_digest = hashlib.sha256()
        for path in sorted(package_root.rglob("*.py")):
            source_digest.update(path.relative_to(package_root).as_posix().encode())
            source_digest.update(bytes.fromhex(sha256(path)))
        result = {"seed": args.seed, "arm": args.arm, "checkpoint": str(checkpoint),
                  "checkpoint_sha256": original_hash, "dataset_sha256": manifest["sha256"],
                  "ultralytics_version": ultralytics.__version__, "ultralytics_path": str(package_root),
                  "python_source_sha256": source_digest.hexdigest(), "torch": torch.__version__,
                  "cuda": torch.version.cuda, "settings": settings, "before": before, "after": after,
                  "fusion_calls": len(fusion_calls), "metrics": values,
                  "background_operating_point": {"conf": 0.25, "iou": 0.7, "fp_images": fp_images,
                                                 "tn_images": 40 - fp_images,
                                                 "specificity": (40 - fp_images) / 40,
                                                 "per_image": background_rows}}
        if sha256(checkpoint) != original_hash:
            raise RuntimeError("Checkpoint changed on disk")
        write_json(out / "verified_metrics.json", result)
    finally:
        BaseModel.fuse = original_fuse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-root", type=Path)
    parser.add_argument("--dataset-root", type=Path, help="BG20 root containing images/val and labels/val")
    parser.add_argument("--out", type=Path, required=True, help="NEW output directory")
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 5, 8])
    parser.add_argument("--arms", choices=ARMS, nargs="+", default=list(ARMS))
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--device", default="0")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--checkpoint", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--seed", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--arm", choices=ARMS, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        worker(args)
        return
    if not args.runs_root or (not args.audit_only and not args.dataset_root):
        parser.error("--runs-root required; evaluation also requires --dataset-root")
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    args.out.mkdir(parents=True, exist_ok=False)
    summary = {"status": "csv_audit_only" if args.audit_only else "incomplete", "csv_audit": {}, "trials": []}
    if args.dataset_root:
        write_json(args.out / "dataset_manifest.json", dataset_manifest(args.dataset_root))
    for seed in args.seeds:
        run = args.runs_root / f"Kvasir_BG20_YOLO26s_seg_TSVM_s{seed}_w2"
        summary["csv_audit"][str(seed)] = best_csv(run / "results.csv")
        if not args.audit_only and not (run / "weights/best.pt").is_file():
            raise FileNotFoundError(run / "weights/best.pt")
    write_json(args.out / "summary.json", summary)
    for seed in ([] if args.audit_only else args.seeds):
        checkpoint = args.runs_root / f"Kvasir_BG20_YOLO26s_seg_TSVM_s{seed}_w2/weights/best.pt"
        for arm in args.arms:
            for repeat in range(1, args.repeats + 1):
                out = args.out / f"seed{seed}_{arm}_repeat{repeat}"
                out.mkdir()
                command = [sys.executable, str(Path(__file__).resolve()), "--worker", "--checkpoint", str(checkpoint.resolve()),
                           "--seed", str(seed), "--arm", arm, "--dataset-root", str(args.dataset_root.resolve()),
                           "--out", str(out.resolve()), "--device", args.device,
                           "--imgsz", str(args.imgsz), "--batch", str(args.batch)]
                print(f"Evaluating seed {seed}: {arm}, repeat {repeat}", flush=True)
                with (out / "console.log").open("w", encoding="utf-8") as log:
                    completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
                trial = {"seed": seed, "arm": arm, "repeat": repeat, "exit_code": completed.returncode,
                         "output": str(out.resolve())}
                result_file = out / "verified_metrics.json"
                if completed.returncode == 0 and result_file.exists():
                    trial["result"] = json.loads(result_file.read_text(encoding="utf-8"))
                summary["trials"].append(trial)
                write_json(args.out / "summary.json", summary)
    if not args.audit_only:
        summary["comparisons"] = comparisons(summary)
        summary["status"] = "evaluated_requires_review" if all("result" in t for t in summary["trials"]) else "failed"
        write_json(args.out / "summary.json", summary)
        if summary["status"] == "failed":
            raise SystemExit("Some trials failed. Inspect console.log; do not publish these as verified results.")
    print(f"Saved {args.out / 'summary.json'}")


if __name__ == "__main__":
    main()
