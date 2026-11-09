"""Đối chứng cùng cỡ tham số: C2PSA mở rộng (C2PSA_rong) so với TSVM đầy đủ và mô hình gốc, seed 0–19.

Câu hỏi: TSVM tốt hơn mô hình gốc có phải chỉ vì tầng 10 nhiều tham số hơn không? C2PSA_rong giữ khối C2PSA của
mô hình gốc nhưng nới rộng để số tham số gần với C2TSVMamba. Endpoint giống bộ chính: mask mAP50–95 tại epoch
đầu tiên đạt cực đại của từng lượt; so sánh ghép cặp theo seed (dùng lại hàm của tinh_ablation.py).

Script CHỈ ĐỌC 03_ket_qua_huan_luyen/ và ghi vào ../bang/ablation_20seed/:
    19_c2psa_rong_tung_seed.csv     (60 dòng: Baseline, TSVM_day_du, C2PSA_rong × 20 seed)
    19b_c2psa_rong_tong_hop.csv     (3 dòng, kèm so sánh ghép cặp với Baseline và TSVM_day_du)
    19c_c2psa_rong_cau_hinh_args.csv (tham số huấn luyện của C2PSA_rong khác lượt gốc cùng seed)

    python tinh_c2psa_rong.py                                        # chỉ số từ results.csv
    C:\\venv_kl_gpu\\Scripts\\python.exe tinh_c2psa_rong.py --torch  # thêm số tham số đếm từ best.pt
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tinh_ablation as ta  # noqa: E402

SEEDS = range(20)
OUT = HERE.parent / "bang" / "ablation_20seed"
CONFIGS = {
    "Baseline": ta.CONFIGS["Baseline"][0],
    "TSVM_day_du": ta.CONFIGS["TSVM_day_du"][0],
    "C2PSA_rong": ta.RUNS_DIR / "C2PSA_rong" / "Kvasir_BG20_YOLO26s_seg_C2PSA_rong_s{}_w2",
}


def run_dir(cfg: str, s: int) -> Path:
    return Path(str(CONFIGS[cfg]).format(s))


def count_params() -> dict:
    import torch
    import danh_gia_pixel as dg
    cleanup = dg.import_fork()
    out = {}
    try:
        for cfg in CONFIGS:
            for s in SEEDS:
                ck = torch.load(run_dir(cfg, s) / "weights" / "best.pt", map_location="cpu", weights_only=False)
                m = ck.get("ema") or ck["model"]
                out[(cfg, s)] = (sum(p.numel() for p in m.parameters()),
                                 sum(p.numel() for p in m.model[10].parameters()), type(m.model[10]).__name__)
    finally:
        cleanup()
    return out


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--torch", action="store_true", help="đếm tham số từ best.pt")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    # 1. Tham số huấn luyện của C2PSA_rong so với lượt gốc cùng seed (bỏ qua tên, đường dẫn, YAML mô hình)
    arg_rows = []
    for s in SEEDS:
        ref = yaml.safe_load((run_dir("Baseline", s) / "args.yaml").read_text(encoding="utf-8"))
        args = yaml.safe_load((run_dir("C2PSA_rong", s) / "args.yaml").read_text(encoding="utf-8"))
        assert args["seed"] == s, s
        for k in sorted(set(args) | set(ref)):
            if k not in ta.ARGS_IGNORE and args.get(k) != ref.get(k):
                arg_rows.append({"seed": s, "tham_so": k, "Baseline": ref.get(k), "C2PSA_rong": args.get(k)})
    pd.DataFrame(arg_rows, columns=["seed", "tham_so", "Baseline", "C2PSA_rong"]).to_csv(
        OUT / "19c_c2psa_rong_cau_hinh_args.csv", index=False, encoding="utf-8-sig")
    print(f"Tham số huấn luyện C2PSA_rong khác lượt gốc cùng seed: {len(arg_rows)}")
    for r in arg_rows:
        print("  ", r)

    # 2. Chỉ số tại epoch cực đại mask mAP50–95
    params = count_params() if a.torch else {}
    rows = []
    for cfg in CONFIGS:
        for s in SEEDS:
            run = run_dir(cfg, s)
            df = ta.read_results(run)
            i = int(df["metrics/mAP50-95(M)"].values.argmax())  # dòng ĐẦU TIÊN đạt cực đại
            r = {"cau_hinh": cfg, "seed": s, "epochs_logged": len(df), "max_mask_epoch": int(df["epoch"].iloc[i]),
                 "train_time_s": float(df["time"].iloc[-1]), "has_best_pt": (run / "weights" / "best.pt").is_file()}
            for k, c in ta.METRICS.items():
                r[k] = float(df[c].iloc[i])
            if params:
                r["params_total"], r["params_layer10"], r["layer10_class"] = params[(cfg, s)]
            rows.append(r)
    per = pd.DataFrame(rows)
    per.to_csv(OUT / "19_c2psa_rong_tung_seed.csv", index=False, encoding="utf-8-sig")
    print("Số epoch:", sorted(per.epochs_logged.unique()), "| đủ best.pt:", bool(per.has_best_pt.all()))

    # 3. Tổng hợp và so sánh ghép cặp
    def vec(cfg):
        return per[per.cau_hinh == cfg].sort_values("seed")["mask_map50_95"].to_numpy()

    summ = []
    for cfg in CONFIGS:
        g = per[per.cau_hinh == cfg]
        r = {"cau_hinh": cfg, "n_seed": len(g), "train_time_h_mean": g.train_time_s.mean() / 3600}
        if params:
            assert g.params_layer10.nunique() == 1, cfg
            r["params_total"], r["params_layer10"] = int(g.params_total.iloc[0]), int(g.params_layer10.iloc[0])
            r["layer10_class"] = g.layer10_class.iloc[0]
        for k in ta.METRICS:
            r[f"{k}_mean"], r[f"{k}_sd"] = g[k].mean(), g[k].std(ddof=1)
        # Quy ước: chênh = cấu hình này − cấu hình tham chiếu
        for ref_cfg, tag in (("Baseline", "vs_baseline"), ("TSVM_day_du", "vs_day_du")):
            if cfg != ref_cfg:
                for k, v in ta.paired(vec(ref_cfg), vec(cfg)).items():
                    r[f"{tag}_{k}"] = v
        summ.append(r)
    summ = pd.DataFrame(summ)
    summ.to_csv(OUT / "19b_c2psa_rong_tong_hop.csv", index=False, encoding="utf-8-sig")
    with pd.option_context("display.float_format", "{:.6f}".format, "display.width", 250, "display.max_columns", 60):
        print(summ.T.to_string(header=False))


if __name__ == "__main__":
    main()
