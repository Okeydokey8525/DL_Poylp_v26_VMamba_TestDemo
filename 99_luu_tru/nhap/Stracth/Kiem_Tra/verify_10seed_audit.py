"""
================================================================================
verify_10seed_audit.py  —  KIỂM CHỨNG TỰ ĐỘNG BỘ KẾT QUẢ 10 SEED (Baseline vs TSVM)
================================================================================
Tác giả   : Nhóm nghiên cứu CNTT_KLCN182
Ngày tạo  : 02/10/2026   (bản 1.0)
Mục đích  : Tái trích xuất độc lập toàn bộ số liệu từ 20 tệp `results.csv` GỐC
            và đối chiếu với mọi bảng thống kê đã sinh ra trong
            `Ket_Qua_V2/KQ_Nen_DX_10seed/`.

CÁCH DÙNG
---------
    python Stracth/verify_10seed_audit.py

KẾT QUẢ
--------
    - In báo cáo PASS/FAIL từng phép kiểm ra màn hình.
    - Ghi file `Ket_Qua_V2/KQ_Nen_DX_10seed/07_audit/audit_report.csv` và
      `audit_report.md` để đính kèm phụ lục luận văn.
    - Mã thoát (exit code): 0 = toàn bộ PASS, 1 = có FAIL.

NGUYÊN TẮC
-----------
    KHÔNG BAO GIỜ sửa tệp CSV gốc để cho khớp với báo cáo.
    Script chỉ ĐỌC và so sánh. Mọi sai lệch phải được sửa ở phía báo cáo
    hoặc phía script sinh dữ liệu, không sửa dữ liệu thô.
================================================================================
"""

from __future__ import annotations

import io
import re
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------- 1. ĐƯỜNG DẪN
ROOT = Path(__file__).resolve().parent.parent          # .../archive
KQ = ROOT / "Ket_Qua_V2" / "KetQua_Nen"                # dữ liệu gốc
PKG = ROOT / "Ket_Qua_V2" / "KQ_Nen_DX_10seed"         # gói kết quả phái sinh
OUT = PKG / "07_audit"
OUT.mkdir(parents=True, exist_ok=True)

TPL = {
    "Baseline": KQ / "YOLOv26s-seg" / "Kvasir_BG20_Baseline_YOLO26s_seg_s{}_w2",
    "TSVM": KQ / "Kvasir_BG20_YOLO26s_seg_TSVM" / "Kvasir_BG20_YOLO26s_seg_TSVM_s{}_w2",
}
N_SEED = 10

# ánh xạ: cột trong results.csv -> cột trong raw_10seeds_extracted_metrics.csv
COLMAP = {
    "metrics/mAP50-95(M)": "mask_map50_95", "metrics/mAP50(M)": "mask_map50",
    "metrics/precision(M)": "mask_precision", "metrics/recall(M)": "mask_recall",
    "metrics/mAP50-95(B)": "box_map50_95", "metrics/mAP50(B)": "box_map50",
    "metrics/precision(B)": "box_precision", "metrics/recall(B)": "box_recall",
    "val/seg_loss": "val_seg_loss", "val/box_loss": "val_box_loss",
    "val/cls_loss": "val_cls_loss", "val/l1_loss": "val_l1_loss",
    "train/seg_loss": "train_seg_loss", "train/box_loss": "train_box_loss",
    "train/cls_loss": "train_cls_loss",
}
# loss: THẤP hơn là tốt hơn -> seed thắng khi giá trị nhỏ hơn
IS_LOSS = {"val_seg_loss", "val_box_loss", "val_cls_loss", "val_l1_loss",
           "train_seg_loss", "train_box_loss", "train_cls_loss"}

# metric_key -> tên hiển thị trong các bảng CSV đã sinh
METRIC_NAME = {
    "mask_map50_95": "Mask mAP@50-95", "mask_map50": "Mask mAP@50",
    "mask_precision": "Mask Precision", "mask_recall": "Mask Recall",
    "box_map50_95": "Box mAP@50-95", "box_map50": "Box mAP@50",
    "box_precision": "Box Precision", "box_recall": "Box Recall",
    "val_seg_loss": "Val Seg Loss", "val_box_loss": "Val Box Loss",
    "val_cls_loss": "Val Cls Loss", "val_l1_loss": "Val L1 Loss",
    "best_epoch": "Best Epoch",
}
ALL_METRICS = list(METRIC_NAME)

TOL = 5e-5      # dung sai cho bảng đã làm tròn 5 chữ số thập phân
TOL_RAW = 5e-6  # dung sai cho bảng trích xuất nguyên bản

RESULTS: list[dict] = []


def chk(section: str, label: str, ok: bool, detail: str = "") -> bool:
    RESULTS.append({"phan": section, "kiem_tra": label,
                    "ket_qua": "PASS" if ok else "FAIL", "chi_tiet": detail})
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"  {detail}" if detail and not ok else ""))
    return ok


def cmp(section: str, label: str, got, exp, tol: float = TOL) -> bool:
    got = np.atleast_1d(np.asarray(got, dtype=float))
    exp = np.atleast_1d(np.asarray(exp, dtype=float))
    if got.shape != exp.shape:
        return chk(section, label, False, f"kích thước {got.shape} != {exp.shape}")
    d = np.abs(got - exp)
    i = int(np.argmax(d))
    return chk(section, label, bool(d.max() <= tol),
               f"sai lệch lớn nhất {d.max():.3g} tại chỉ số {i}: {got[i]} vs {exp[i]}")


# ------------------------------------------------- 2. TRÍCH XUẤT TỪ results.csv
def extract_all() -> pd.DataFrame:
    print("\n" + "=" * 96)
    print("BƯỚC 1 — Trích xuất lại từ 20 tệp results.csv GỐC")
    print("=" * 96)
    rows, missing = [], []
    for model, tpl in TPL.items():
        for seed in range(N_SEED):
            d = Path(str(tpl).format(seed))
            f = d / "results.csv"
            if not f.exists():
                missing.append(str(f))
                continue
            df = pd.read_csv(f)
            df.columns = [c.strip() for c in df.columns]
            df = df.apply(lambda s: s.str.strip() if s.dtype == object else s)
            best = df.loc[df["metrics/mAP50-95(M)"].idxmax()]
            rec = {"model": model, "seed": seed,
                   "best_epoch": int(best["epoch"]), "total_epochs": len(df),
                   "run_path": str(d)}
            for src, dst in COLMAP.items():
                rec[dst] = float(best[src]) if src in best.index else np.nan
            rows.append(rec)
    for m in missing:
        print(f"  [FAIL] Thiếu tệp: {m}")
    chk("1. results.csv", f"Tồn tại đủ {len(TPL)*N_SEED} tệp results.csv",
        not missing and len(rows) == len(TPL) * N_SEED, f"thiếu {len(missing)}")
    ext = pd.DataFrame(rows).sort_values(["model", "seed"]).reset_index(drop=True)
    ext.to_csv(OUT / "reextracted_from_results_csv.csv", index=False)
    print(f"  -> Đã ghi {OUT / 'reextracted_from_results_csv.csv'} ({len(ext)} dòng)")
    return ext


# ------------------------------------------------- 3. ĐỐI CHIẾU CÁC BẢNG CSV
def audit(ext: pd.DataFrame) -> None:
    B = ext[ext.model == "Baseline"].sort_values("seed").reset_index(drop=True)
    T = ext[ext.model == "TSVM"].sort_values("seed").reset_index(drop=True)

    # 3.1 bảng trích xuất gốc
    print("\n" + "=" * 96)
    print("BƯỚC 2 — Đối chiếu bảng trích xuất (raw_10seeds_extracted_metrics.csv)")
    print("=" * 96)
    raw = pd.read_csv(PKG / "01_raw_analysis" / "raw_10seeds_extracted_metrics.csv")
    raw = raw.sort_values(["model", "seed"]).reset_index(drop=True)
    n_cell = 0
    for m in list(COLMAP.values()) + ["best_epoch", "total_epochs"]:
        diff = (ext[m].astype(float) - raw[m].astype(float)).abs()
        n_cell += len(diff)
        chk("2. raw", f"{m} ({len(diff)}/20 khớp tuyệt đối)",
            bool((diff <= (0 if m in ("best_epoch", "total_epochs") else TOL_RAW)).all()),
            f"sai lệch lớn nhất {diff.max():.3g}")
    print(f"  -> Tổng cộng {n_cell} ô dữ liệu đã đối chiếu")

    # 3.2 mean ± std
    print("\n" + "=" * 96)
    print("BƯỚC 3 — Tính lại Mean ± Std, Δ, %, kiểm định paired t-test")
    print("=" * 96)
    pub = pd.read_csv(PKG / "02_statistics" / "mean_std" / "full_comparison_mean_std.csv")
    for key, name in METRIC_NAME.items():
        r = pub[pub.metric_name == name]
        if r.empty:
            chk("3. mean_std", f"Có dòng '{name}'", False); continue
        r = r.iloc[0]
        cmp("3. mean_std", f"{name}.baseline_mean", B[key].mean(), r.baseline_mean)
        cmp("3. mean_std", f"{name}.baseline_std", B[key].std(ddof=1), r.baseline_std)
        cmp("3. mean_std", f"{name}.tsvm_mean", T[key].mean(), r.tsvm_mean)
        cmp("3. mean_std", f"{name}.tsvm_std", T[key].std(ddof=1), r.tsvm_std)
        cmp("3. mean_std", f"{name}.delta", T[key].mean() - B[key].mean(),
            r.delta_tsvm_minus_baseline)
        cmp("3. mean_std", f"{name}.percent_change",
            (T[key].mean() - B[key].mean()) / B[key].mean() * 100, r.percent_change)
        tt = stats.ttest_rel(T[key], B[key])
        cmp("3. mean_std", f"{name}.p_value_ttest", tt.pvalue, r.p_value_ttest)
        chk("3. mean_std", f"{name}.cờ ý nghĩa α=0.05",
            bool(r.statistically_significant_005) == bool(tt.pvalue < 0.05))

    # 3.3 min / max / range
    print("\n" + "=" * 96)
    print("BƯỚC 4 — Tính lại Min, Max, Median, Range, seed cực trị")
    print("=" * 96)
    mm = pd.read_csv(PKG / "02_statistics" / "min_max" / "metrics_min_max_range.csv")
    for key, name in METRIC_NAME.items():
        r = mm[mm.metric_name == name]
        if r.empty:
            chk("4. min_max", f"Có dòng '{name}'", False); continue
        r = r.iloc[0]
        for pre, d in (("baseline", B), ("tsvm", T)):
            s = d[key]
            # Quy ước: loss -> THẤP hơn tốt hơn; mAP/P/R -> CAO hơn tốt hơn.
            # best_epoch -> CAO hơn tốt hơn (hội tụ muộn ở epoch lớn = ổn định hơn).
            lower_better = key in IS_LOSS
            cmp("4. min_max", f"{name}.{pre}_min", s.min(), r[f"{pre}_min"])
            cmp("4. min_max", f"{name}.{pre}_max", s.max(), r[f"{pre}_max"])
            cmp("4. min_max", f"{name}.{pre}_median", s.median(), r[f"{pre}_median"])
            cmp("4. min_max", f"{name}.{pre}_range", s.max() - s.min(), r[f"{pre}_range"])
            bs = int(s.idxmin() if lower_better else s.idxmax())
            ws = int(s.idxmax() if lower_better else s.idxmin())
            chk("4. min_max", f"{name}.{pre}_best_seed", bs == r[f"{pre}_best_seed"],
                f"{bs} vs {r[f'{pre}_best_seed']}")
            chk("4. min_max", f"{name}.{pre}_worst_seed", ws == r[f"{pre}_worst_seed"],
                f"{ws} vs {r[f'{pre}_worst_seed']}")

    # 3.4 seed-by-seed + win/loss
    print("\n" + "=" * 96)
    print("BƯỚC 5 — Đối chiếu bảng từng seed, Δ, và tỷ lệ thắng/thua")
    print("=" * 96)
    sb = pd.read_csv(PKG / "02_statistics" / "seed_comparison" / "seed_by_seed_metrics_and_deltas.csv")
    cmp("5. seed_cmp", "Cột seed", sb.seed.to_numpy(), np.arange(N_SEED))
    for key in ALL_METRICS:
        cmp("5. seed_cmp", f"Baseline_{key}", B[key].to_numpy(), sb[f"Baseline_{key}"].to_numpy(), TOL_RAW)
        cmp("5. seed_cmp", f"TSVM_{key}", T[key].to_numpy(), sb[f"TSVM_{key}"].to_numpy(), TOL_RAW)
        cmp("5. seed_cmp", f"Delta_{key}", (T[key] - B[key]).to_numpy(), sb[f"Delta_{key}"].to_numpy(), TOL_RAW)
    wl = pd.read_csv(PKG / "02_statistics" / "seed_comparison" / "seed_win_loss_summary.csv")
    for key, name in METRIC_NAME.items():
        r = wl[wl.Metric == name]
        if r.empty:
            chk("5. seed_cmp", f"Có dòng win/loss '{name}'", False); continue
        r = r.iloc[0]
        lower_better = key in IS_LOSS
        # best_epoch: epoch CAO hơn = hội tụ tốt hơn -> xem là thắng khi lớn hơn
        ties = int((B[key].to_numpy() == T[key].to_numpy()).sum())
        tw = sum(1 for i in range(N_SEED)
                 if ((T[key].iloc[i] < B[key].iloc[i]) if lower_better
                     else (T[key].iloc[i] > B[key].iloc[i])))
        chk("5. seed_cmp", f"{name}.tsvm_wins", tw == r["TSVM Thắng (số seed)"],
            f"{tw} vs {r['TSVM Thắng (số seed)']}")
        chk("5. seed_cmp", f"{name}.baseline_wins", N_SEED - tw - ties == r["Baseline Thắng (số seed)"],
            f"{N_SEED - tw - ties} vs {r['Baseline Thắng (số seed)']}")
        chk("5. seed_cmp", f"{name}.ties", ties == r["Hòa"], f"{ties} vs {r['Hòa']}")

    # 3.5 bảng phân tích sâu 03_metrics
    print("\n" + "=" * 96)
    print("BƯỚC 6 — Đối chiếu các bảng phân tích sâu trong 03_metrics (kèm Wilcoxon)")
    print("=" * 96)
    for rel in ["03_metrics/segmentation/segmentation_metrics_summary.csv",
                "03_metrics/bounding_box/bounding_box_metrics_summary.csv",
                "03_metrics/loss/validation_loss_metrics_summary.csv"]:
        d = pd.read_csv(PKG / rel)
        for _, r in d.iterrows():
            key = r.metric_key
            chk("6. 03_metrics", f"{key}: tên metric khớp", METRIC_NAME.get(key) == r.metric_name)
            for pre, dd in (("baseline", B), ("tsvm", T)):
                s = dd[key]
                lower_better = key in IS_LOSS
                cmp("6. 03_metrics", f"{key}.{pre}_mean", s.mean(), r[f"{pre}_mean"])
                cmp("6. 03_metrics", f"{key}.{pre}_std", s.std(ddof=1), r[f"{pre}_std"])
                cmp("6. 03_metrics", f"{key}.{pre}_min", s.min(), r[f"{pre}_min"])
                cmp("6. 03_metrics", f"{key}.{pre}_max", s.max(), r[f"{pre}_max"])
                cmp("6. 03_metrics", f"{key}.{pre}_median", s.median(), r[f"{pre}_median"])
                cmp("6. 03_metrics", f"{key}.{pre}_range", s.max() - s.min(), r[f"{pre}_range"])
                bs = int(s.idxmin() if lower_better else s.idxmax())
                ws = int(s.idxmax() if lower_better else s.idxmin())
                chk("6. 03_metrics", f"{key}.{pre}_best_seed", bs == r[f"{pre}_best_seed"])
                chk("6. 03_metrics", f"{key}.{pre}_worst_seed", ws == r[f"{pre}_worst_seed"])
            cmp("6. 03_metrics", f"{key}.delta", T[key].mean() - B[key].mean(), r.delta_tsvm_minus_baseline)
            cmp("6. 03_metrics", f"{key}.percent_change",
                (T[key].mean() - B[key].mean()) / B[key].mean() * 100, r.percent_change)
            ties = int((B[key].to_numpy() == T[key].to_numpy()).sum())
            lower_better = key in IS_LOSS
            wins = sum(1 for i in range(N_SEED)
                       if ((T[key].iloc[i] < B[key].iloc[i]) if lower_better
                           else (T[key].iloc[i] > B[key].iloc[i])))
            chk("6. 03_metrics", f"{key}.tsvm_wins_seeds", wins == r.tsvm_wins_seeds,
                f"{wins} vs {r.tsvm_wins_seeds}")
            chk("6. 03_metrics", f"{key}.baseline_wins_seeds",
                N_SEED - wins - ties == r.baseline_wins_seeds)
            chk("6. 03_metrics", f"{key}.ties_seeds", ties == r.ties_seeds)
            tt = stats.ttest_rel(T[key], B[key])
            cmp("6. 03_metrics", f"{key}.paired_ttest_stat", tt.statistic, r.paired_ttest_stat)
            cmp("6. 03_metrics", f"{key}.p_value_ttest", tt.pvalue, r.p_value_ttest)
            w = stats.wilcoxon(T[key], B[key])
            cmp("6. 03_metrics", f"{key}.wilcoxon_stat", w.statistic, r.wilcoxon_stat)
            cmp("6. 03_metrics", f"{key}.p_value_wilcoxon", w.pvalue, r.p_value_wilcoxon)

    # 3.6 ma trận nhầm lẫn
    print("\n" + "=" * 96)
    print("BƯỚC 7 — Ma trận nhầm lẫn: kiểm tra tính nhất quán nội bộ")
    print("=" * 96)
    cm = pd.read_csv(PKG / "01_raw_analysis" / "raw_10seeds_confusion_matrices.csv")
    b_cm, t_cm = cm[cm.model == "Baseline"], cm[cm.model == "TSVM"]
    for tag, d in (("Baseline", b_cm), ("TSVM", t_cm)):
        chk("7. CM", f"{tag}: TP + FN = 127", bool((d.TP + d.FN == 127).all()))
        chk("7. CM", f"{tag}: FP + TN = 40", bool((d.FP + d.TN == 40).all()))
        cmp("7. CM", f"{tag}: TP_rate_%", d["TP_rate_%"].to_numpy(),
            (d.TP / (d.TP + d.FN) * 100).to_numpy())
        cmp("7. CM", f"{tag}: FP_rate_%", d["FP_rate_%"].to_numpy(),
            (d.FP / (d.FP + d.TN) * 100).to_numpy())
    chk("7. CM", "CẢNH BÁO: cột TN == 40 − FP (số tái dựng, KHÔNG phải số đo của Ultralytics)",
        bool(((cm.FP + cm.TN) == 40).all()),
        "Nếu đúng, mọi báo cáo phải nêu đây là số suy dựng")
    for tag, fn, d in (("baseline", "baseline_cm_mean_count.csv", b_cm),
                       ("tsvm", "tsvm_cm_mean_count.csv", t_cm)):
        got = pd.read_csv(PKG / "04_confusion_matrix" / "count" / fn, index_col=0)
        cmp("7. CM", f"{tag}_cm_mean_count: TP", d.TP.mean(), got.loc["True Polyp", "Pred Polyp"])
        cmp("7. CM", f"{tag}_cm_mean_count: FN", d.FN.mean(), got.loc["True Polyp", "Pred Background"])
        cmp("7. CM", f"{tag}_cm_mean_count: FP", d.FP.mean(), got.loc["True Background", "Pred Polyp"])
        cmp("7. CM", f"{tag}_cm_mean_count: TN", d.TN.mean(), got.loc["True Background", "Pred Background"])
    print("\n  ⚠️  GIỚI HẠN ĐÃ BIẾT (không kiểm tự động được, cần OCR confusion_matrix.png):")
    print("      • Ô background↔background LUÔN = 0 vì metrics.py:427-434 thiếu nhánh cộng TN.")
    print("      • 17/20 lượt chạy: TP/FP/FN khớp ảnh gốc. 3/20 (TSVM s0, s5, s8) KHÔNG khớp.")
    print("      → Xem doc/20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md mục §0.2 và §5.2.")

    # 3.7 đối chiếu bg20_all_seeds_metrics.csv
    print("\n" + "=" * 96)
    print("BƯỚC 8 — Đối chiếu bảng tổng hợp Stracth/bg20_all_seeds_metrics.csv")
    print("=" * 96)
    alt = ROOT / "Stracth" / "bg20_all_seeds_metrics.csv"
    if alt.exists():
        a = pd.read_csv(alt)
        a = a[a.model.isin(list(TPL))].sort_values(["model", "seed"]).reset_index(drop=True)
        e = ext.sort_values(["model", "seed"]).reset_index(drop=True)
        for src, dst in (("mask_mAP50_95", "mask_map50_95"), ("mask_mAP50", "mask_map50"),
                         ("mask_precision", "mask_precision"), ("mask_recall", "mask_recall"),
                         ("box_mAP50_95", "box_map50_95"), ("box_MAP50", "box_map50"),
                         ("box_precision", "box_precision"), ("box_recall", "box_recall"),
                         ("val_seg_loss", "val_seg_loss")):
            if src in a.columns:
                cmp("8. alt", f"bg20_all_seeds_metrics.{src}", a[src].to_numpy(), e[dst].to_numpy(), TOL_RAW)
    else:
        chk("8. alt", "Tồn tại Stracth/bg20_all_seeds_metrics.csv", False)


# ---------------------------------------------------------------- 4. XUẤT BÁO
def write_report() -> int:
    df = pd.DataFrame(RESULTS)
    df.to_csv(OUT / "audit_report.csv", index=False, encoding="utf-8-sig")

    n_pass = int((df.ket_qua == "PASS").sum())
    n_fail = int((df.ket_qua == "FAIL").sum())

    lines = [
        "# BÁO CÁO KIỂM CHỨNG TỰ ĐỘNG — BỘ KẾT QUẢ 10 SEED (Baseline vs TSVM)",
        "",
        f"**Sinh tự động bởi:** `Stracth/verify_10seed_audit.py`",
        f"**Thời điểm chạy:** {datetime.now():%d/%m/%Y %H:%M:%S}",
        f"**Phạm vi:** {N_SEED * len(TPL)} lượt chạy, {len(METRIC_NAME)} chỉ số",
        "",
        "## Tổng kết",
        "",
        "| Hạng mục | Số phép kiểm | Đạt | Không đạt |",
        "| :--- | ---: | ---: | ---: |",
    ]
    for sec, grp in df.groupby("phan", sort=False):
        lines.append(f"| {sec} | {len(grp)} | {int((grp.ket_qua == 'PASS').sum())} "
                     f"| {int((grp.ket_qua == 'FAIL').sum())} |")
    lines += [f"| **TỔNG** | **{len(df)}** | **{n_pass}** | **{n_fail}** |", ""]

    if n_fail:
        lines += ["## Danh sách phép kiểm KHÔNG ĐẠT", ""]
        for _, r in df[df.ket_qua == "FAIL"].iterrows():
            lines.append(f"- **{r.kiem_tra}** — {r.chi_tiet}")

    lines += [
        "",
        "## Giới hạn còn lại của ma trận nhầm lẫn (không kiểm tự động được)",
        "",
        "1. **Ô TN không phải số đo.** `ultralytics/utils/metrics.py`, hàm "
        "`ConfusionMatrix.process_batch` dòng 427–434, khi ảnh nền không có ground-truth "
        "code **chỉ cộng FP** rồi `return` — không có nhánh `matrix[self.nc, self.nc] += 1`. "
        "Ô background↔background luôn bằng 0, bị loại khỏi ghi nhãn (dòng 550) và hiển thị trống. "
        "Giá trị TN trong CSV **đúng bằng 40 − FP** ở cả 20 dòng → là **số tái dựng theo giả định**.",
        "2. **17/20 lượt chạy** có TP/FP/FN khớp chính xác ảnh `confusion_matrix.png` "
        "(đã đối chiếu bằng OCR). **3/20 lượt chạy TSVM (s0, s5, s8) không khớp** — "
        "ảnh gốc cho thấy tỷ lệ phát hiện gần 0, mâu thuẫn với `results.csv` của chính các lượt chạy đó.",
        "3. Vì vậy ma trận nhầm lẫn chỉ nên dùng như **quan sát mô tả**, không phải bằng chứng "
        "định lượng chính.",
        "",
        "---",
        "*Nguyên tắc: không bao giờ sửa tệp CSV gốc để cho khớp với báo cáo.*",
    ]
    (OUT / "audit_report.md").write_text("\n".join(lines), encoding="utf-8")

    print("\n" + "=" * 96)
    print(f"KẾT QUẢ: {n_pass}/{len(df)} phép kiểm ĐẠT, {n_fail} KHÔNG ĐẠT")
    print(f"Báo cáo: {OUT / 'audit_report.md'}")
    print(f"          {OUT / 'audit_report.csv'}")
    print("=" * 96)
    return 0 if n_fail == 0 else 1


def main() -> int:
    print("=" * 96)
    print("KIỂM CHỨNG TỰ ĐỘNG — BỘ KẾT QUẢ 10 SEED (Baseline YOLO26s-seg vs TSVM)")
    print(f"Thời điểm chạy: {datetime.now():%d/%m/%Y %H:%M:%S}")
    print(f"Nguồn gốc    : {KQ}")
    print("=" * 96)
    ext = extract_all()
    audit(ext)
    return write_report()


if __name__ == "__main__":
    raise SystemExit(main())
