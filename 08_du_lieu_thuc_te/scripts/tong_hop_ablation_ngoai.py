"""Tổng hợp ablation và C2PSA rộng trên CVC-ClinicDB, CVC-ColonDB (nhận xét phản biện II.1), không cần GPU.

Đọc kết quả từng lượt do danh_gia_ablation_ngoai.py tạo (../bang/tung_luot_ablation/) và kết quả mô hình gốc, TSVM
có sẵn (../bang/tung_luot/{clinicdb,colondb}_{baseline,tsvm}_s*.csv, không chạy lại). Chỉ số từng lượt tính đúng như
summarize() của danh_gia_du_lieu_ngoai.py (Dice/IoU/Precision/Recall trung bình theo ảnh có polyp, no_pred_rate là
tỉ lệ ảnh polyp không có điểm ảnh dự đoán nào), nên dòng baseline/tsvm khớp ../bang/20seed/01_ngoai_tung_seed.csv.

Ghi vào --out (mặc định ../bang/ablation_ngoai/20seed/), không ghi chỗ nào khác:
    01_ablation_ngoai_tung_seed.csv   (bộ × mô hình × seed)
    02_ablation_ngoai_thong_ke.csv    (trung bình ± SD, và so sánh ghép cặp theo seed)

Quy ước so sánh ghép cặp: dòng có a, b là hiệu a − b qua các seed chung; a_higher là số seed a lớn hơn b. Có hai
nhóm: mỗi biến thể và C2PSA rộng so với mô hình gốc (a = biến thể, b = baseline) và so với TSVM (a = tsvm, b = biến
thể); thêm tsvm so với baseline để đối chiếu.

    python tong_hop_ablation_ngoai.py --seeds 0 1 ... 19
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import danh_gia_du_lieu_ngoai as ng  # noqa: E402

dg = ng.dg
SETS = ["clinicdb", "colondb"]
VARIANTS = ["abl_vmamba_only", "abl_shape_only", "abl_no_guidance", "c2psa_rong"]
MODELS = ["baseline", "tsvm", *VARIANTS]
METRICS = ["no_pred_rate", "recall", "dice", "iou", "precision"]


def per_seed(df):
    rows = []
    for (key, model, s), g in df.groupby(["dataset", "model", "seed"], sort=False):
        g = g[g.gt_px > 0]   # CVC không có ảnh không polyp; giữ điều kiện như summarize()
        m = np.array([dg.per_image_metrics(a, b, c) for a, b, c in zip(g.tp, g.fp, g.fn)])
        r = {"dataset": key, "model": model, "seed": s, "n_images": len(g)}
        r["dice"], r["iou"], r["precision"], r["recall"] = np.nanmean(m, 0)
        r["no_pred_rate"] = float((g.pred_px == 0).mean())
        rows.append(r)
    return pd.DataFrame(rows).sort_values(["dataset", "model", "seed"])


def paired(d, a, b, key):
    x, y = d[d.model == a].set_index("seed"), d[d.model == b].set_index("seed")
    c = x.index.intersection(y.index)
    out = []
    for m in METRICS:
        diff = x.loc[c, m] - y.loc[c, m]
        ok = len(c) >= 3 and diff.std() > 0
        out.append({"dataset": key, "loai": "ghep_cap", "model": f"{a}_vs_{b}", "a": a, "b": b, "metric": m,
                    "n_seeds": len(c), "mean": diff.mean(), "sd": diff.std(ddof=1),
                    "paired_t_p": stats.ttest_rel(x.loc[c, m], y.loc[c, m]).pvalue if ok else np.nan,
                    "wilcoxon_p": stats.wilcoxon(x.loc[c, m], y.loc[c, m]).pvalue if ok else np.nan,
                    "a_higher": int((diff > 0).sum())})
    return out


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", nargs="*", type=int, default=list(range(20)))
    ap.add_argument("--out", type=Path, default=ng.BANG / "ablation_ngoai" / "20seed")
    a = ap.parse_args()
    seeds = sorted(set(a.seeds))

    files = []
    for key in SETS:
        for m in ("baseline", "tsvm"):
            files += [ng.LUOT / f"{key}_{m}_s{s}.csv" for s in seeds]
        for v in VARIANTS:
            files += [ng.BANG / "tung_luot_ablation" / f"{key}_{v}_s{s}.csv" for s in seeds]
    thieu = [f for f in files if not f.exists()]
    assert not thieu, f"Thiếu {len(thieu)} lượt, ví dụ {thieu[:3]}"
    df = pd.concat([pd.read_csv(f, encoding="utf-8-sig") for f in files], ignore_index=True)

    sd = per_seed(df)
    a.out.mkdir(parents=True, exist_ok=True)
    sd.to_csv(a.out / "01_ablation_ngoai_tung_seed.csv", index=False, encoding="utf-8-sig")

    st = []
    for key in SETS:
        d = sd[sd.dataset == key]
        for model in MODELS:
            g = d[d.model == model]
            for m in METRICS:
                st.append({"dataset": key, "loai": "mo_hinh", "model": model, "metric": m, "n_seeds": len(g),
                           "mean": g[m].mean(), "sd": g[m].std(ddof=1), "min": g[m].min(), "max": g[m].max()})
        st += paired(d, "tsvm", "baseline", key)
        for v in VARIANTS:
            st += paired(d, v, "baseline", key)
            st += paired(d, "tsvm", v, key)
    st = pd.DataFrame(st)
    st.to_csv(a.out / "02_ablation_ngoai_thong_ke.csv", index=False, encoding="utf-8-sig")
    print(f"Đã ghi {a.out} ({len(seeds)} seed)")
    with pd.option_context("display.float_format", "{:.4f}".format, "display.width", 220, "display.max_rows", 400):
        print(st[st.metric.isin(["no_pred_rate", "recall", "dice"])].drop(columns=["loai"]).to_string(index=False))


if __name__ == "__main__":
    main()
