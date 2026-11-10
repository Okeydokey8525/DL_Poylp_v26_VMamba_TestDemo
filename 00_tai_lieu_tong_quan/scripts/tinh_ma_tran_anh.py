"""Ma trận nhầm lẫn theo ẢNH (có báo polyp hay không) của 4 mô hình trên 160 ảnh val, từng seed.

Khác ma trận nhầm lẫn theo đối tượng của Ultralytics (bang/06_*, hình h04): PraNet/U-Net không có đối tượng hay độ
tin cậy, nên cách so chung được cho cả 4 mô hình là xét mức ảnh. Một ảnh là "báo polyp" nếu có ít nhất 1 điểm ảnh
dự đoán là polyp (cùng định nghĩa với bg_fp_image_rate trong danh_gia_pixel.py). Cả 4 ô đều ĐẾM trực tiếp trên
từng ảnh (ảnh nền có pred_px = 0 mới tính TN), không suy ra từ ô khác.

    TP: ảnh polyp có báo polyp       FN: ảnh polyp không có điểm ảnh dự đoán nào (bỏ sót cả ảnh)
    FP: ảnh nền bị báo polyp         TN: ảnh nền không có điểm ảnh dự đoán nào

Chỉ đọc <thư mục>/10_pixel_tung_anh.csv, ghi vào cùng thư mục:
    20_ma_tran_anh_tung_seed.csv   (mô hình × seed)
    20b_ma_tran_anh_tong_hop.csv   (trung bình ± SD qua seed của từng ô và các tỉ lệ)

    python tinh_ma_tran_anh.py                       # mặc định ../bang/pixel_640 (PraNet/U-Net 640)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, default=HERE.parent / "bang" / "pixel_640")
    a = ap.parse_args()
    d = pd.read_csv(a.dir / "10_pixel_tung_anh.csv", encoding="utf-8-sig")
    d["bao"] = d.pred_px > 0
    rows = []
    for (m, s), g in d.groupby(["model", "seed"], sort=False):
        pol, bg = g[~g.is_bg], g[g.is_bg]
        r = {"model": m, "seed": s, "n_polyp": len(pol), "n_nen": len(bg),
             "TP": int(pol.bao.sum()), "FN": int((~pol.bao).sum()), "FP": int(bg.bao.sum()), "TN": int((~bg.bao).sum())}
        r["ti_le_phat_hien_anh"] = r["TP"] / r["n_polyp"]
        r["ti_le_bao_nham_nen"] = r["FP"] / r["n_nen"]
        r["do_chinh_xac_anh"] = (r["TP"] + r["TN"]) / (r["n_polyp"] + r["n_nen"])
        rows.append(r)
    per = pd.DataFrame(rows)
    assert (per.n_polyp == 120).all() and (per.n_nen == 40).all(), "Sai số ảnh val"
    per.to_csv(a.dir / "20_ma_tran_anh_tung_seed.csv", index=False, encoding="utf-8-sig")
    cols = ["TP", "FN", "FP", "TN", "ti_le_phat_hien_anh", "ti_le_bao_nham_nen", "do_chinh_xac_anh"]
    summ = []
    for m, g in per.groupby("model", sort=False):
        r = {"model": m, "n_seed": len(g)}
        for c in cols:
            r[f"{c}_mean"], r[f"{c}_sd"] = g[c].mean(), g[c].std(ddof=1)
        summ.append(r)
    summ = pd.DataFrame(summ)
    summ.to_csv(a.dir / "20b_ma_tran_anh_tong_hop.csv", index=False, encoding="utf-8-sig")
    with pd.option_context("display.float_format", "{:.4f}".format, "display.width", 250, "display.max_columns", 30):
        print(summ.to_string(index=False))


if __name__ == "__main__":
    main()
