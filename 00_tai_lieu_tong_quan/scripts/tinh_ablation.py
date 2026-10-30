"""Tổng hợp thí nghiệm tách thành phần (ablation) của C2TSVMamba, seed 0–4.

Năm cấu hình: đối chứng (C2PSA), TSVM đầy đủ (hai cấu hình này lấy seed 0–4 của các lượt chính) và ba biến thể
vmamba_only, shape_only, shape_vmamba_no_guidance. Endpoint giống bộ chính: mask mAP50–95 tại epoch đầu tiên đạt
cực đại của từng lượt. So sánh ghép cặp theo seed. Với 5 cặp, Wilcoxon hai phía không thể có p < 0,0625, nên các
giá trị p chỉ ghi để tham khảo.

Script CHỈ ĐỌC 03_ket_qua_huan_luyen/ và ghi vào ../bang/:
    17_ablation_tung_seed.csv   (25 dòng: 5 cấu hình × 5 seed)
    17b_ablation_tong_hop.csv   (5 dòng)
    18_ablation_cau_hinh_args.csv (tham số huấn luyện khác với lượt TSVM chính cùng seed)

    python tinh_ablation.py                                        # chỉ số từ results.csv
    C:\\venv_kl_gpu\\Scripts\\python.exe tinh_ablation.py --torch  # thêm số tham số đếm từ best.pt
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy import stats

HERE = Path(__file__).resolve().parent
RUNS_DIR = HERE.parent.parent / "03_ket_qua_huan_luyen"
OUT = HERE.parent / "bang"

SEEDS = range(5)
CONFIGS = {  # tên -> (thư mục mẫu, có SS2D, có nhánh hình dạng, có cổng)
    "Baseline": (RUNS_DIR / "Baseline_YOLO26s_seg" / "Kvasir_BG20_Baseline_YOLO26s_seg_s{}_w2", 0, 0, 0),
    "TSVM_day_du": (RUNS_DIR / "TSVM_FP32" / "Kvasir_BG20_YOLO26s_seg_TSVM_FP32_s{}_w2", 1, 1, 1),
    "vmamba_only": (RUNS_DIR / "Vmamba_only" / "Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s{}_w2", 1, 0, 0),
    "shape_only": (RUNS_DIR / "Shape_only" / "Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s{}_w2", 0, 1, 0),
    "shape_vmamba_no_guidance": (RUNS_DIR / "No_guidance" / "Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s{}_w2",
                                 1, 1, 0),
}
METRICS = {
    "mask_map50_95": "metrics/mAP50-95(M)",
    "mask_map50": "metrics/mAP50(M)",
    "mask_precision": "metrics/precision(M)",
    "mask_recall": "metrics/recall(M)",
}
# khác nhau nhưng không ảnh hưởng huấn luyện (tên, đường dẫn, file YAML mô hình)
ARGS_IGNORE = {"name", "model", "save_dir", "project", "data", "pretrained"}


def read_results(run: Path) -> pd.DataFrame:
    df = pd.read_csv(run / "results.csv")
    df.columns = [c.strip() for c in df.columns]
    return df


def count_params(cleanup_holder: list) -> dict:
    """Số tham số toàn mô hình và tầng 10, đếm từ best.pt (cần torch và fork TSVM)."""
    import torch
    sys.path.insert(0, str(HERE))
    import danh_gia_pixel as dg
    cleanup_holder.append(dg.import_fork())
    out = {}
    for cfg, (pat, *_) in CONFIGS.items():
        for s in SEEDS:
            ck = torch.load(Path(str(pat).format(s)) / "weights" / "best.pt", map_location="cpu", weights_only=False)
            m = ck.get("ema") or ck["model"]
            out[(cfg, s)] = (sum(p.numel() for p in m.parameters()),
                             sum(p.numel() for p in m.model[10].parameters()), type(m.model[10]).__name__)
    return out


def paired(x: np.ndarray, y: np.ndarray) -> dict:
    """y so với x, ghép cặp theo seed."""
    d = y - x
    r = {"delta": d.mean(), "delta_sd": d.std(ddof=1), "so_seed_hon": int((d > 0).sum())}
    if d.std() > 0:
        se = d.std(ddof=1) / math.sqrt(len(d))
        q = stats.t.ppf(0.975, len(d) - 1)
        r.update(ci95_low=d.mean() - q * se, ci95_high=d.mean() + q * se,
                 paired_t_p=stats.ttest_rel(y, x).pvalue, wilcoxon_p=stats.wilcoxon(y, x).pvalue)
    return r


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--torch", action="store_true", help="đếm tham số từ best.pt")
    a = ap.parse_args()

    # 1. Cấu hình huấn luyện: so từng lượt với lượt TSVM chính cùng seed
    ref = {s: yaml.safe_load((Path(str(CONFIGS["TSVM_day_du"][0]).format(s)) / "args.yaml").read_text(encoding="utf-8"))
           for s in SEEDS}
    arg_rows = []
    for cfg, (pat, *_) in CONFIGS.items():
        for s in SEEDS:
            args = yaml.safe_load((Path(str(pat).format(s)) / "args.yaml").read_text(encoding="utf-8"))
            assert args["seed"] == s, (cfg, s)
            for k in sorted(set(args) | set(ref[s])):
                if k not in ARGS_IGNORE and args.get(k) != ref[s].get(k):
                    arg_rows.append({"cau_hinh": cfg, "seed": s, "tham_so": k, "TSVM_chinh": ref[s].get(k), "luot_nay": args.get(k)})
    pd.DataFrame(arg_rows, columns=["cau_hinh", "seed", "tham_so", "TSVM_chinh", "luot_nay"]).to_csv(
        OUT / "18_ablation_cau_hinh_args.csv", index=False, encoding="utf-8-sig")
    print(f"Tham số huấn luyện khác lượt TSVM chính cùng seed (bỏ qua {sorted(ARGS_IGNORE)}): {len(arg_rows)}")
    for r in arg_rows:
        print("  ", r)

    # 2. Chỉ số tại epoch cực đại mask mAP50–95
    cleanup = []
    params = count_params(cleanup) if a.torch else {}
    try:
        rows = []
        for cfg, (pat, ss2d, shape, gate) in CONFIGS.items():
            for s in SEEDS:
                run = Path(str(pat).format(s))
                df = read_results(run)
                i = int(df["metrics/mAP50-95(M)"].values.argmax())  # dòng ĐẦU TIÊN đạt cực đại
                r = {"cau_hinh": cfg, "seed": s, "ss2d": ss2d, "nhanh_hinh_dang": shape, "cong": gate,
                     "epochs_logged": len(df), "max_mask_epoch": int(df["epoch"].iloc[i]),
                     "train_time_s": float(df["time"].iloc[-1]), "has_best_pt": (run / "weights" / "best.pt").is_file()}
                for k, c in METRICS.items():
                    r[k] = float(df[c].iloc[i])
                if params:
                    r["params_total"], r["params_layer10"], r["layer10_class"] = params[(cfg, s)]
                rows.append(r)
    finally:
        for c in cleanup:
            c()
    per = pd.DataFrame(rows)
    per.to_csv(OUT / "17_ablation_tung_seed.csv", index=False, encoding="utf-8-sig")
    print("Số epoch:", sorted(per.epochs_logged.unique()), "| đủ best.pt:", bool(per.has_best_pt.all()))

    # 3. Tổng hợp và so sánh ghép cặp
    def vec(cfg, k):
        return per[per.cau_hinh == cfg].sort_values("seed")[k].to_numpy()

    summ = []
    for cfg in CONFIGS:
        g = per[per.cau_hinh == cfg]
        r = {"cau_hinh": cfg, "n_seed": len(g), "train_time_h_mean": g.train_time_s.mean() / 3600}
        if params:
            r["params_total"] = int(g.params_total.iloc[0])
            r["params_layer10"] = int(g.params_layer10.iloc[0])
            assert g.params_layer10.nunique() == 1, cfg
        for k in METRICS:
            r[f"{k}_mean"], r[f"{k}_sd"] = g[k].mean(), g[k].std(ddof=1)
        for ref_cfg, tag in (("Baseline", "vs_baseline"), ("TSVM_day_du", "vs_day_du")):
            if cfg != ref_cfg:
                for k, v in paired(vec(ref_cfg, "mask_map50_95"), vec(cfg, "mask_map50_95")).items():
                    r[f"{tag}_{k}"] = v
        summ.append(r)
    summ = pd.DataFrame(summ)
    summ.to_csv(OUT / "17b_ablation_tong_hop.csv", index=False, encoding="utf-8-sig")
    with pd.option_context("display.float_format", "{:.6f}".format, "display.width", 250, "display.max_columns", 50):
        print(per.drop(columns=["has_best_pt"]).to_string(index=False))
        print(summ.T.to_string(header=False))


if __name__ == "__main__":
    main()
