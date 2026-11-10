"""Xuất số liệu cho trang "Chỉ số nghiên cứu" của web PolypVision từ các bảng đã xác minh trong ../bang/.

Không tính lại gì: chỉ đọc 04, pixel_640/12, 16, 19 rồi ghi một file JSON để Spring hiển thị, nhờ vậy
mọi con số trên web truy được về CSV gốc. Chạy lại script này mỗi khi các bảng được cập nhật.

Chạy:  python 00_tai_lieu_tong_quan/scripts/xuat_chi_so_web.py [--ra <đường dẫn JSON>]
Mặc định ghi vào ../Ung_Dung/polypweb/polypweb/src/main/resources/research/research-metrics.json
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BANG = ROOT / "00_tai_lieu_tong_quan" / "bang"
DEFAULT_OUT = (ROOT.parent / "Ung_Dung" / "polypweb" / "polypweb" / "src" / "main" / "resources"
               / "research" / "research-metrics.json")

MASK_METRICS = [
    ("mask_map50_95", "mAP50–95 (mask)"),
    ("mask_map50", "mAP50 (mask)"),
    ("mask_precision", "Precision (mask, theo đối tượng)"),
    ("mask_recall", "Recall (mask, theo đối tượng)"),
]
PIXEL_METRICS = [
    ("dice", "Dice (= F1 theo pixel)"),
    ("iou", "IoU"),
    ("precision", "Precision (pixel)"),
    ("recall", "Recall (pixel)"),
]


def read(name: str) -> list[dict[str, str]]:
    with open(BANG / name, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def num(value: str) -> float | None:
    return float(value) if value not in ("", None) else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ra", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    if hasattr(__import__("sys").stdout, "reconfigure"):
        __import__("sys").stdout.reconfigure(encoding="utf-8")

    paired = {r["metric"]: r for r in read("04_thong_ke_ghep_cap.csv")}
    mask = []
    for key, label in MASK_METRICS:
        r = paired[key]
        mask.append({
            "metric": key, "label": label,
            "baselineMean": num(r["baseline_mean"]), "baselineSd": num(r["baseline_sd"]),
            "tsvmMean": num(r["tsvm_mean"]), "tsvmSd": num(r["tsvm_sd"]),
            "delta": num(r["delta"]), "ci95Low": num(r["ci95_low"]), "ci95High": num(r["ci95_high"]),
            "pairedTP": num(r["paired_t_p"]), "wilcoxonP": num(r["wilcoxon_p"]),
            "tsvmBetterSeeds": int(float(r["tsvm_better_seeds"])),
        })

    px = read("pixel_640/12_pixel_thong_ke.csv")   # PraNet/U-Net bản 640×640
    stat = {(r["model"], r["metric"]): r for r in px}
    pixel = []
    for key, label in PIXEL_METRICS:
        b, t, d = stat[("baseline", key)], stat[("tsvm", key)], stat[("tsvm_vs_baseline", key)]
        pixel.append({
            "metric": key, "label": label,
            "baselineMean": num(b["mean"]), "baselineSd": num(b["sd"]),
            "tsvmMean": num(t["mean"]), "tsvmSd": num(t["sd"]),
            "delta": num(d["mean"]), "pairedTP": num(d["paired_t_p"]), "wilcoxonP": num(d["wilcoxon_p"]),
            "tsvmBetterSeeds": int(float(d["tsvm_higher"])),
        })
    reference = []
    nhan = {"pranet": "PraNet (ResNet-50), ảnh 640×640", "unet": "U-Net, ảnh 640×640"}
    for model, src in (("baseline", "baseline"), ("tsvm", "tsvm"), ("pranet", "pranet640"), ("unet", "unet640")):
        reference.append({
            "model": model, "label": nhan.get(model, stat[(src, "dice")]["label"]),
            "diceMean": num(stat[(src, "dice")]["mean"]), "diceSd": num(stat[(src, "dice")]["sd"]),
            "iouMean": num(stat[(src, "iou")]["mean"]), "iouSd": num(stat[(src, "iou")]["sd"]),
            "bgFpImageRate": num(stat[(src, "bg_fp_image_rate")]["mean"]),
        })

    cost = []
    for r in read("16_flops_do_tre_gpu.csv"):
        cost.append({
            "model": r["model"], "params": int(r["params"]),
            "gflops": num(r["gflops_ultralytics"]),
            "gpuMsMedian": num(r["gpu_ms_median"]), "gpuMsP95": num(r["gpu_ms_p95"]), "gpu": r["gpu"],
        })

    end_to_end = []
    for r in read("19_do_tre_end_to_end.csv"):
        end_to_end.append({
            "device": r["nhan"], "model": r["mo_hinh"], "requests": int(r["so_yeu_cau"]),
            "clientMsMedian": num(r["client_ms_trung_vi"]), "clientMsP95": num(r["client_ms_p95"]),
            "inferMsMedian": num(r["infer_ms_trung_vi"]), "date": r["ngay_do"],
        })

    data = {
        "generatedOn": date.today().isoformat(),
        "seeds": 20,
        "validation": {"images": 160, "polyp": 120, "background": 40},
        "sources": {
            "mask": "bang/04_thong_ke_ghep_cap.csv",
            "pixel": "bang/pixel_640/12_pixel_thong_ke.csv",
            "cost": "bang/16_flops_do_tre_gpu.csv",
            "endToEnd": "bang/19_do_tre_end_to_end.csv",
        },
        "mask": mask, "pixel": pixel, "pixelReference": reference,
        "cost": cost, "endToEnd": end_to_end,
    }
    args.ra.parent.mkdir(parents=True, exist_ok=True)
    args.ra.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã ghi {args.ra}")


if __name__ == "__main__":
    main()
