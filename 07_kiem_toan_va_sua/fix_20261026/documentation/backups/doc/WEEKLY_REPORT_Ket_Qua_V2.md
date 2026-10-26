# BÁO CÁO TUẦN — KET_QUA_V2 (10-Seed Baseline vs TSVM)

**SOURCE SCOPE:** `archive/` only — primarily `archive/Ket_Qua_V2/**`.

**Evidence tagging used throughout:**

| Tag | Meaning |
|---|---|
| `OBSERVED` | Read directly from an artifact (CSV, JSON, YAML, PNG, code) |
| `DERIVED` | Computed from artifacts; the computation is stated |
| `INTERPRETATION` | Reading of the evidence; no new measurement |
| `UNVERIFIED` | No supporting artifact found in the archive |

**Conflict rule applied:** where a Markdown document disagrees with a raw artifact, the artifact wins and the disagreement is recorded in §6. No source file was modified.

---

## 1. THÔNG TIN TUẦN

| Field | Value |
|---|---|
| **Thời gian (week dates)** | `NOT AVAILABLE` — no date range for a reporting week exists anywhere in `archive/` |
| **Chủ đề (topic)** | Đánh giá định lượng mô hình phân đoạn polyp YOLO26-seg (Baseline) đối đầu với biến thể tích hợp Topology-Shape-aware VMamba (TSVM) trên `Kvasir_YOLO_SEG_BG20`, thực nghiệm 10 seed · `OBSERVED` (`Ket_Qua_V2/KQ_Nen_DX_10seed/README.md`) |
| **Phạm vi công việc (scope)** | Chuẩn bị dữ liệu BG20 · huấn luyện 20 lượt (2 mô hình × 10 seed) · trích xuất & kiểm định thống kê · đối chiếu ma trận nhầm lẫn · audit provenance · đo chi phí tính toán · `OBSERVED` |

---

## 2. MỤC TIÊU TUẦN

Only objectives with an artifact in the archive are listed.

1. Chuẩn hóa quy trình tiền xử lý với 20 % ảnh nền âm tính (BG20) — **evidence**: `Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/dataset_bg20_summary.json` (`status: SUCCESS`, 1 200 images), `data_bg20.yaml`, `selected_normal_cecum_val_40.txt` · `OBSERVED`
2. Mở rộng kiểm định độ tin cậy lên **10 seed** — **evidence**: `Ket_Qua_V2/KetQua_Nen/` contains exactly 2 model directories with 10 run folders each · `OBSERVED`
3. Thiết lập đối đầu song song 2 mô hình (Baseline vs TSVM) — **evidence**: `raw_10seeds_extracted_metrics.csv` = 20 rows = 2 models × 10 seeds · `OBSERVED`
4. Phân tích ma trận nhầm lẫn trên 160 ảnh thẩm định — **evidence**: `04_confusion_matrix/count/*.csv`, `percentage/*.csv`, 20 `confusion_matrix.png` · `OBSERVED`
5. Hệ thống hóa biểu đồ trực quan hóa — **evidence**: 12 PNG in `KQ_Nen_DX_10seed/figures/`, 16 PNG in `05_charts/` · `OBSERVED`
6. Đo chi phí tính toán và độ trễ suy luận — **evidence**: `Ket_Qua_V2/efficiency_benchmark/tables/efficiency_summary.csv` · `OBSERVED`

---

## 3. CÔNG VIỆC ĐÃ THỰC HIỆN

### 3.1 Dataset

- `OBSERVED` — `Kvasir_YOLO_SEG_BG20` built with `status: SUCCESS`; **1 200** images = **1 040** train (880 polyp + 160 background) + **160** val (120 polyp + 40 background). Negatives from `normal-cecum` (Kvasir v2), selected with `random_seed: 42`. Evidence: `dataset_bg20_summary.json`, `data_bg20.yaml`.
- `OBSERVED` — `images/val/` contains exactly **160** image files; `images/train/` exactly **1 040**.
- `OBSERVED` — `total_polyps_val: 127` — the validation split carries **127 polyp objects**.
- `OBSERVED` — background images carry **empty labels** (`empty_labels_train: 160`, `empty_labels_val: 40`), the mechanism that lets a detector be scored on false alarms.

### 3.2 Experimental setup

From `KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/…_s0_w2/args.yaml` (verified for TSVM seed 0; the other 19 runs share the structure):

| Hyper-parameter | Value |
|---|---|
| model | `/kaggle/working/yolo26s-seg-TopologyShapeVMamba.yaml` |
| data | `/kaggle/working/data_bg20.yaml` |
| epochs | 100 |
| batch | 8 |
| imgsz | 640 |
| workers | 2 |
| optimizer | AdamW |
| lr0 | 0.001 |
| weight_decay | 0.0005 |
| warmup_epochs | 5.0 |
| close_mosaic | 10 |
| cos_lr | false |
| amp | false |
| seed | 0 (per-run index) |
| deterministic | true |

All rows `OBSERVED` from `args.yaml`.
`UNVERIFIED` — the Kaggle GPU model and torch/Python versions recorded in `doc/00` have **no artifact**; `args.yaml` records only `device: '0'`.
### 3.3 Baseline

- `OBSERVED` — Baseline is `YOLOv26s-seg` (`KetQua_Nen/YOLOv26s-seg/`), 10 run folders `Kvasir_BG20_Baseline_YOLO26s_seg_s{0..9}_w2`, each with a 100-row `results.csv` and an `args.yaml`.
- `OBSERVED` — efficiency profile: 11.434 M params, 18.54 GFLOPs, 22.27 MB checkpoint, 200.12 ms, 5.00 FPS (`efficiency_summary.csv`).

### 3.4 TSVM

- `OBSERVED` — TSVM is `Kvasir_BG20_YOLO26s_seg_TSVM`, 10 run folders `…_TSVM_s{0..9}_w2`, each with a 100-row `results.csv` and an `args.yaml` pointing at `yolo26s-seg-TopologyShapeVMamba.yaml`.
- `OBSERVED` — the architectural block sits at **layer 10** of `cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml` (`- [-1, 2, C2TSVMamba, [1024]] # 10`).
- `OBSERVED` — efficiency profile: 12.255 M params, 18.86 GFLOPs, 23.86 MB checkpoint, 821.27 ms, 1.22 FPS (`efficiency_summary.csv`).
- `UNVERIFIED` — no GPU-side efficiency measurement exists in the archive; the CSV is `thop` + CPU timing and `Peak_VRAM_MB` is empty.

### 3.5 Multi-seed experiment

- `OBSERVED` — **20** `results.csv`, 100 rows each = 2 models × 10 seeds × 100 epochs.
- `OBSERVED` — `raw_10seeds_extracted_metrics.csv` holds exactly 20 data rows with 21 fields; it contains **no** IoU / mIoU / Dice / F1 column.
- `OBSERVED` — metrics are read at each run's **best epoch**, not at epoch 100.

### 3.6 Evaluation

- `OBSERVED` — 13 metrics compared: 4 Mask detection, 4 Box detection, 4 validation losses, 1 Best Epoch (`full_comparison_mean_std.csv`, `summary.csv`).

### 3.7 Confusion matrix

- `OBSERVED` — per-seed confusion counts exist for all 20 runs, plus mean count and mean percentage files.
- `OBSERVED` — all 20 rows satisfy `TP + FN = 127` and `FP + TN = 40` (re-checked row by row; 0 violations).
- `OBSERVED` — 20 `confusion_matrix.png` artefacts, one per run.
- `PROVENANCE` — the TN cell is never produced by the metric code (§5.4); 3 of 20 PNGs disagree with their CSV (§5.5).

### 3.8 Statistical analysis

- `OBSERVED` — paired t-test and Wilcoxon signed-rank reported per metric in `summary.csv`.
- `OBSERVED` — `statistically_significant_005` is **False for all 13 metrics**. Minimum paired-t p = **0.090772** (Val Seg Loss); minimum Wilcoxon p = **0.083984**.
- `OBSERVED` — seed win/loss/tie counts in `seed_win_loss_summary.csv`; min/max/range in `metrics_min_max_range.csv`.

### 3.9 Audit / provenance

- `OBSERVED` — forensic audit package exists: `FORENSIC_EXPERIMENT_AUDIT.md`, `final_audit_report.md`, `conclusions_reviewed.md`, `07_audit/audit_report.md` + `.csv`.
- `OBSERVED` — `Stracth/` contains **55** Python scripts, including `verify_10seed_audit.py`, `re_evaluate_seed5.py`, `extract_cm_data.py`, `_forensic_cm_ocr.py`.
- `OBSERVED` — PNG ↔ `results.csv` mtime census: **19/20 identical**; TSVM s5 PNG is **+312.7 minutes** later.
- `UNVERIFIED` — `verify_10seed_audit.py` was **not re-executed** in this pass.
---

## 4. KẾT QUẢ THỰC NGHIỆM

**Seed count: 10 per model, 20 runs total. `OBSERVED`.**
Values are copied from `02_statistics/mean_std/full_comparison_mean_std.csv`; Δ and % are that file's own columns (not recomputed here). Anything computed in this document is marked `DERIVED` with the arithmetic shown.

### 4.1 Main metrics (10 seeds)

| Metric | Baseline (Mean ± Std) | TSVM (Mean ± Std) | Δ | % | p (paired t) | Sig @ 0.05 |
|---|---|---|---:|---:|---:|:---:|
| Mask mAP@50-95 | 0.7210 ± 0.0129 | 0.7246 ± 0.0078 | +0.0036 | +0.49 % | 0.3839 | No |
| Mask mAP@50 | 0.9119 ± 0.0107 | 0.9062 ± 0.0082 | −0.0056 | −0.62 % | 0.2273 | No |
| Mask Precision | 0.9023 ± 0.0339 | 0.9118 ± 0.0246 | +0.0095 | +1.05 % | 0.5428 | No |
| Mask Recall | 0.8584 ± 0.0252 | 0.8625 ± 0.0173 | +0.0041 | +0.48 % | 0.5907 | No |
| Box mAP@50-95 | 0.7262 ± 0.0198 | 0.7285 ± 0.0141 | +0.0023 | +0.32 % | 0.7152 | No |
| Box mAP@50 | 0.9011 ± 0.0116 | 0.9006 ± 0.0090 | −0.0004 | −0.05 % | 0.9334 | No |
| Box Precision | 0.8992 ± 0.0326 | 0.9062 ± 0.0251 | +0.0070 | +0.78 % | 0.5921 | No |
| Box Recall | 0.8434 ± 0.0337 | 0.8567 ± 0.0152 | +0.0133 | +1.58 % | 0.2674 | No |
| Val Seg Loss | 1.3045 ± 0.0867 | 1.2424 ± 0.0387 | −0.0622 | −4.76 % | 0.0908 | No |
| Val Box Loss | 0.7239 ± 0.0434 | 0.7305 ± 0.0399 | +0.0066 | +0.91 % | 0.7008 | No |
| Val Cls Loss | 0.5591 ± 0.0635 | 0.6148 ± 0.0884 | +0.0557 | +9.97 % | 0.0943 | No |
| Val L1 Loss | 0.0164 ± 0.0012 | 0.0162 ± 0.0009 | −0.0002 | −1.02 % | 0.6995 | No |
| Best Epoch | 87.3 ± 13.10 | 91.7 ± 4.85 | +4.40 | +5.04 % | 0.3149 | No |

**Direction is mixed:** TSVM is higher on 7 metrics and lower on 5 (Mask mAP@50, Box mAP@50, Val Box Loss, Val Cls Loss; and for the loss rows a *higher* value means *worse*). Val Cls Loss worsens by +9.97 %.

### 4.2 Dispersion and extremes

`OBSERVED` — `metrics_min_max_range.csv`:

| Metric | Baseline Min (seed) | Baseline Max (seed) | Range | TSVM Min (seed) | TSVM Max (seed) | Range |
|---|---|---|---:|---|---|---:|
| Mask mAP@50-95 | 0.69411 (s3) | 0.73663 (s0) | 0.04252 | 0.70650 (s7) | 0.73385 (s8) | 0.02735 |

`DERIVED` (from the Std columns): variance ratio = (0.012854 / 0.007755)² = **2.75 ×**. Std reduction = 1 − 0.007755/0.012854 = **−39.7 %**. Range reduction = 1 − 0.02735/0.04252 = **−35.7 %**.
`INTERPRETATION` — dispersion is lower for TSVM **on this metric**; the archive does not show contraction on every metric, so "more stable" must not be stated globally.

### 4.3 Seed win / loss

`OBSERVED` — `seed_win_loss_summary.csv`:

| Metric | TSVM wins | Baseline wins | Ties |
|---|---:|---:|---:|
| Mask mAP@50-95 | 6 | 4 | 0 |
| Mask mAP@50 | 3 | 7 | 0 |
| Mask Precision | 5 | 5 | 0 |
| Mask Recall | 6 | 4 | 0 |
| Val Seg Loss | 8 | 2 | 0 |
| Val Cls Loss | 2 | 8 | 0 |

`OBSERVED` — TSVM leads on Mask mAP@50-95 at seeds **s1, s2, s3, s6, s8, s9** (`FORENSIC_EXPERIMENT_AUDIT.md` §9, consistent with `raw_10seeds_extracted_metrics.csv`).

### 4.4 Confusion matrix means

`OBSERVED` — `04_confusion_matrix/count/baseline_cm_mean_count.csv` and `tsvm_cm_mean_count.csv`:

| Cell | Baseline | TSVM |
|---|---:|---:|
| True Polyp → Pred Polyp (TP) | 110.3 | 111.2 |
| True Polyp → Pred Background (FN) | 16.7 | 15.8 |
| True Background → Pred Polyp (FP) | 16.8 | 14.6 |
| True Background → Pred Background (TN) | 23.2 | 25.4 |

`OBSERVED` — percentages (`percentage/*.csv`): sensitivity (TP rate) **86.85 % → 87.56 %**; FP rate **42.0 % → 36.5 %**; TN rate **58.0 % → 63.5 %**.

### 4.5 Cost and latency

`OBSERVED` — `Ket_Qua_V2/efficiency_benchmark/tables/efficiency_summary.csv` (`thop` profile + CPU timing, 200 raw rows):

| Quantity | Baseline | TSVM |
|---|---:|---:|
| Params (M) | 11.434 | 12.255 |
| GFLOPs | 18.54 | 18.86 |
| Checkpoint (MB) | 22.27 | 23.86 |
| Latency mean (ms) | 200.12 | 821.27 |
| Latency P50 / P95 / P99 (ms) | 195.92 / 218.28 / 251.67 | 826.09 / 899.10 / 908.97 |
| FPS | 5.00 | 1.22 |
| Peak VRAM | *(empty ⇒ not measured)* | *(empty ⇒ not measured)* |
---

## 5. CÁC PHÁT HIỆN QUAN TRỌNG

### 5.1 Dataset composition — 160 / 120 / 40 / 127

`OBSERVED` — `dataset_bg20_summary.json` (`total_val: 160`, `val_polyp_images: 120`, `val_background_images: 40`, `total_polyps_val: 127`) cross-checked against 160 files in `images/val/` and against all 20 rows of the confusion-matrix CSV (`TP + FN = 127`, `FP + TN = 40`).

`INTERPRETATION` — **the three quantities have different units and must never be mixed:** 160 is the number of *validation images*; 120 and 40 partition those images; **127 is the number of polyp *objects***. The arithmetic `127 + 40 = 167` therefore does **not** describe any image count and does not appear in the current evidence base.

### 5.2 Direction of the TSVM effect is favourable on detection, mixed overall

`OBSERVED` — from §4.1. Detection-side means favour TSVM on Mask mAP@50-95, Mask Precision, Mask Recall, Box mAP@50-95, Box Precision and Box Recall; they favour Baseline on Mask mAP@50 and Box mAP@50. On losses, TSVM improves Val Seg Loss and Val L1 Loss but degrades Val Box Loss and Val Cls Loss.

`INTERPRETATION` — a fair summary is "mean detection quality is comparable, with TSVM slightly higher on 6 of 8 detection metrics", not "TSVM is better".

### 5.3 Dispersion contracts on Mask mAP@50-95

`DERIVED` — σ 0.012854 → 0.007755 (ratio 2.75 ×), range 0.04252 → 0.02735. See §4.2 for the arithmetic. `OBSERVED` seeds: Baseline worst = s3, TSVM worst = s7.

### 5.4 TN is reconstructed, never measured

`OBSERVED` — `ultralytics_Topology-Shape-aware VMamba/utils/metrics.py`, `ConfusionMatrix.process_batch` (~lines 427–434) increments **only FP** for an image with empty ground truth and then returns; there is **no** `matrix[nc,nc] += 1` branch. Line 550 filters values `< 0.005`, so the background↔background cell renders empty on the PNGs.

`OBSERVED` — `raw_10seeds_confusion_matrices.csv` satisfies `TN = 40 − FP` in **20/20** rows.

`DERIVED` — therefore every TN / TN-rate value in §4.4 is a **reconstruction under the 40-negative-image design**, not an observed measurement, and no per-image specificity inference is available.

### 5.5 Confusion-matrix artefacts: 17/20 match, TSVM s0/s5/s8 do not

`OBSERVED` — `FORENSIC_EXPERIMENT_AUDIT.md` §11-D1 records for the three runs:

| Run | `confusion_matrix.png` (TP/FN/FP) | CSV row (TP/FN/FP) |
|---|---|---|
| TSVM s0 | 59 / 68 / 10 | 108 / 19 / 8 |
| TSVM s5 | 0 / 127 / 90 | 112 / 15 / 7 |
| TSVM s8 | 6 / 121 / 8 | 111 / 16 / 14 |

The remaining **17 of 20** runs match exactly.

`OBSERVED` — mtime census: 19 of 20 PNG mtimes equal their `results.csv` mtime; TSVM s5 is **+312.7 minutes** later (PNG 23/09 15:06:10 vs `results.csv` 23/09 09:53:28).

`DERIVED` — substituting the three PNG rows gives TSVM mean FP = (146 − (8+7+14) + (10+90+8)) / 10 = **22.5**, versus the CSV value 14.6 and Baseline 16.8. The sign of the FP comparison therefore depends on which artefact is treated as authoritative.

`UNVERIFIED` — the PNG values were read by the forensic OCR script; **this reporting pass did not re-run the OCR**.

### 5.6 Seed-5 provenance mechanism (partially explained)

`OBSERVED` — `Stracth/re_evaluate_seed5.py` loads `…_s5_w2/weights/best.pt`, calls `model.val(..., project=archive/Stracth/seed5_re_eval, name="val_run", plots=True, batch=16, device="cpu")`, and then copies `confusion_matrix.png` and `confusion_matrix_normalized.png` from that separate validation folder into the original seed-5 run folder with `shutil.copy2`.

`INTERPRETATION` — this accounts for the s5 PNG's later timestamp and for a plot produced under a different validation configuration. It is a **provenance finding about an artefact**, not a claim that the s5 training run itself is invalid.

`UNKNOWN` — the same explanation does **not** apply to s0 and s8, whose PNG mtimes equal their `results.csv` mtimes. The archive records their cause as "NGUYÊN NHÂN CHƯA XÁC ĐỊNH được". No root cause is asserted here.

### 5.7 Cost and latency

`OBSERVED` — §4.5. The only file-backed generation is a `thop` profile plus CPU timing; `Peak_VRAM_MB` is empty in both rows.

`INTERPRETATION` — TSVM costs +0.821 M parameters and +0.32 GFLOPs over Baseline, but measures ~4.1× the mean CPU latency (821.27 vs 200.12 ms). Because no GPU latency measurement exists in the archive, the deployment-speed question cannot be answered from this evidence.

### 5.8 Audit coverage

`OBSERVED` — 20 `results.csv`, 20 `confusion_matrix.png`, 22 CSV artefacts in `KQ_Nen_DX_10seed/`, 12 figures in `figures/`, 16 in `05_charts/`, 15 in `efficiency_benchmark/figures/`, 55 scripts in `Stracth/`.
---

## 6. VẤN ĐỀ / RỦI RO (có evidence)

| # | Issue | Evidence | Type |
|---|---|---|---|
| 1 | **No metric reaches statistical significance.** All 13 rows `statistically_significant_005 = False`; min p = 0.090772 | `full_comparison_mean_std.csv` | `OBSERVED` |
| 2 | **The FP comparison flips depending on the artefact used** (14.6 vs 22.5) | `FORENSIC_EXPERIMENT_AUDIT.md` §11-D1; §5.5 above | `DERIVED` |
| 3 | **3 of 20 confusion-matrix PNGs contradict their own CSV** | same source; mtime census | `OBSERVED` |
| 4 | **TN / Specificity are reconstructed, not measured** | `utils/metrics.py` `process_batch`; 20/20 CSV rows | `OBSERVED` |
| 5 | **Efficiency data is CPU-only; VRAM unmeasured**, while `doc/20` §6 cites this CSV while printing GPU numbers and concluding "50.5 FPS beats the 25–30 FPS threshold" | `efficiency_summary.csv` vs `doc/20_KET_QUA_CHUAN…` §6 | `OBSERVED` conflict; artefact wins |
| 6 | **A stale FP baseline `17.4` survives in five documents**, giving "−16.1 %"; the raw CM gives 16.8 → 14.6 = −13.1 % | `raw_10seeds_confusion_matrices.csv`; `doc/LICHSU_CAP_NHAT.md` v3.1 lists 17.4 as retired | `OBSERVED` conflict; artefact wins |
| 7 | **Seed win counts in `doc/06` §3 are wrong**: claims Mask Precision 7/10 (actual 5/10) and Mask Recall 5/10 with 1 tie (actual 6/10, 0 ties) | `seed_win_loss_summary.csv` | `OBSERVED` conflict; artefact wins |
| 8 | **A stale 4-model benchmark package** claims 4 models / 400 raw rows and prints P5 and ITS Mamba figures | `efficiency_summary.csv` = 2 rows; `efficiency_raw_benchmark.csv` = 200 rows; `KetQua_Nen/` = 2 model dirs | `OBSERVED` conflict; artefact wins |
| 9 | **`data_bg20.yaml` `path:` points at a directory that does not exist** (dataset is under `Ket_Qua_V2/`) | `data_bg20.yaml` vs filesystem | `OBSERVED` |
| 10 | **Two unreconciled audit totals** — `final_audit_report.md` says 559/559, `07_audit/audit_report.md` and `FORENSIC_EXPERIMENT_AUDIT.md` say 694/694 | both report files | `OBSERVED`; scope undefined |
| 11 | **`Stracth/` count is stated as 46 / 48 in two documents; actual 55** | `archive/Stracth/*.py` enumeration | `OBSERVED` |
| 12 | **Run inventory overstated** as "47 runs / 4 models / 40 `results.csv`" in several documents | `KetQua_Nen/` = 20 `results.csv`, 2 models | `OBSERVED` conflict; artefact wins |

Per the general rules, none of the above was silently corrected in the source documents. They are recorded here for the reviewer.

---

## 7. NHỮNG GÌ CHƯA THỂ KẾT LUẬN

1. **Statistical superiority of TSVM.** Not established. Minimum p = 0.090772 (paired t), 0.083984 (Wilcoxon). With N = 10 no conclusion is available from the archive.
2. **Root cause of the TSVM s0 and s8 confusion-matrix mismatch.** `UNKNOWN`. The PNG mtime equals the `results.csv` mtime, so there is no overwrite evidence. No prediction dump exists to replay.
3. **The true direction of the FP comparison.** Depends on whether the CSV or the PNG artefacts are authoritative; the archive discloses the conflict but does not adjudicate it.
4. **GPU latency / VRAM and real-time feasibility.** No artifact. The CPU measurement (5.00 / 1.22 FPS) cannot answer the endoscopy real-time question.
5. **Why TSVM's mean Val Cls Loss worsens by +9.97 %** (0.5591 → 0.6148), including the seed-7 outlier 0.83094 recorded in `conclusions_reviewed.md` §5. No artifact explains the mechanism. `UNKNOWN`.
6. **Seed randomness / independence.** Seed labels 0–9 exist in `args.yaml`; no RNG-provenance artifact demonstrates how the seeds were drawn. `UNVERIFIED`.
7. **Training environment (GPU model, torch / Python versions).** `doc/00` states Kaggle T4, torch 2.10.0+cu128, Python 3.12; `args.yaml` records only `device: '0'`. `UNVERIFIED`.
8. **P5 VMamba and ITS Mamba models.** Their run directories and checkpoints are absent; the efficiency figures attributed to them have no backing row. Permanently unavailable from this archive.
9. **All 6-fold / single-seed historical results** (C2IAVM, P5-Attention, ITSMamba, Boundary-aware, Multi-scale). Raw data deleted; the quarantine manifest forbids citing them.
10. **Whether the `.pdf` report still carries the six superseded p-values.** Unresolved in the audit (FlateDecode streams).
11. **Whether IoU / mIoU / Dice / F1 were ever intended as reportable metrics.** No such column exists in the package.
12. **Supervisor academic title.** The archive is internally inconsistent ("TS." vs "ThS."). `NEEDS VERIFICATION` from outside the archive.
---

## 8. KẾT LUẬN TUẦN

The 10-seed BG20 comparison between Baseline and TSVM was completed on the full experimental matrix available in the archive: 2 models × 10 seeds × 100 epochs = 20 runs, evaluated at each run's best epoch, with 13 metrics analysed by paired t-test and Wilcoxon tests and a per-seed confusion matrix on 160 validation images.

On the evidence recorded in `Ket_Qua_V2`, the two architectures are close in detection quality. TSVM has the higher mean on Mask mAP@50-95 (+0.0036), Mask Precision (+0.0095), Mask Recall (+0.0041), Box mAP@50-95 (+0.0023), Box Precision (+0.0070) and Box Recall (+0.0133), and the lower mean on Mask mAP@50 (−0.0056) and Box mAP@50 (−0.0004). Of the four validation losses, TSVM improves Seg Loss (−0.0622) and L1 Loss, while Box Loss and Cls Loss are higher. None of these 13 comparisons is statistically significant at α = 0.05; the smallest p-value is 0.090772. The description that matches the evidence is therefore "comparable performance with small, mixed and non-significant differences", together with a narrower descriptive observation that seed-to-seed dispersion on Mask mAP@50-95 is smaller for TSVM (σ 0.0078 vs 0.0129).

Two constraints must travel with any use of these results. First, the confusion-matrix evidence is internally inconsistent: 17 of 20 PNG artefacts match their CSV, and substituting the three remaining rows would reverse the false-positive comparison. Second, TN and Specificity are reconstructions under the negative-image design rather than direct measurements, and the cost data is CPU-only.

---

## 9. EVIDENCE INDEX

| Statement | Evidence File | Evidence Type |
| --------- | ------------- | ------------- |
| Dataset 1 200 images; 1 040 train; 160 val (120 polyp + 40 background); 127 polyp objects; `random_seed: 42` | `Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/dataset_bg20_summary.json` | Data artifact (JSON) |
| Validation split physically contains 160 images; train 1 040 | `Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/images/val/`, `images/train/` | Directory count |
| 160 / 120 / 40 / 127 declared in the dataset config | `Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/data_bg20.yaml` | Config artifact |
| `data_bg20.yaml` `path:` points to a non-existent directory | `Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/data_bg20.yaml` vs filesystem | Config artifact + enumeration |
| Hyper-parameters (100 epochs, batch 8, imgsz 640, AdamW, lr0 0.001, warmup 5, close_mosaic 10, amp false, deterministic true, seed 0) | `Ket_Qua_V2/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM/…_s0_w2/args.yaml` | Config artifact (YAML) |
| 20 runs, 2 models, 10 seeds each, 100 rows per `results.csv` | `Ket_Qua_V2/KetQua_Nen/**` (20 `results.csv`, 2 model dirs) | Directory enumeration |
| TSVM architectural block at layer 10 | `archive/ultralytics_Topology-Shape-aware VMamba/cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml` | Config artifact |
| All 13 metric means, Std, Δ, %, p-values; all `statistically_significant_005 = False`; min p = 0.090772 | `Ket_Qua_V2/KQ_Nen_DX_10seed/02_statistics/mean_std/full_comparison_mean_std.csv` | Data artifact (CSV) |
| Wilcoxon p-values; seed win/loss/tie counts | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/summary.csv`, `02_statistics/seed_comparison/seed_win_loss_summary.csv` | Data artifact (CSV) |
| Min / max / range and best / worst seed ids | `Ket_Qua_V2/KQ_Nen_DX_10seed/02_statistics/min_max/metrics_min_max_range.csv` | Data artifact (CSV) |
| Per-seed raw metrics at best epoch (20 rows, 21 fields; no IoU/mIoU/Dice/F1) | `Ket_Qua_V2/KQ_Nen_DX_10seed/01_raw_analysis/raw_10seeds_extracted_metrics.csv` | Data artifact (CSV) |
| TSVM leads on Mask mAP@50-95 at s1,s2,s3,s6,s8,s9 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/FORENSIC_EXPERIMENT_AUDIT.md` §9 | Generated report (audited) |
| CM means TP 110.3/111.2, FN 16.7/15.8, FP 16.8/14.6, TN 23.2/25.4 | `Ket_Qua_V2/KQ_Nen_DX_10seed/04_confusion_matrix/count/*_cm_mean_count.csv` | Data artifact (CSV) |
| Sensitivity 86.85 %→87.56 %; FP rate 42.0 %→36.5 %; TN rate 58.0 %→63.5 % | `Ket_Qua_V2/KQ_Nen_DX_10seed/04_confusion_matrix/percentage/*_cm_mean_percentage.csv` | Data artifact (CSV) |
| TP+FN = 127 and FP+TN = 40 in all 20 rows; TN = 40 − FP in all 20 rows | `Ket_Qua_V2/KQ_Nen_DX_10seed/01_raw_analysis/raw_10seeds_confusion_matrices.csv` | Data artifact (CSV) |
| TN cell never populated by the metric code (no `matrix[nc,nc] += 1`); `< 0.005` filter at line 550 | `archive/ultralytics_Topology-Shape-aware VMamba/utils/metrics.py` (`ConfusionMatrix.process_batch`) | Source code |
| 17/20 PNG match; TSVM s0/s5/s8 mismatch (59/0/6 vs 108/112/111); FP 14.6 → 22.5 under substitution; s0/s8 cause unknown | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/FORENSIC_EXPERIMENT_AUDIT.md` §11-D1 | Generated report (audited) |
| PNG ↔ results.csv mtimes: 19/20 identical; TSVM s5 +312.7 min | File mtimes under `Ket_Qua_V2/KetQua_Nen/**` | Filesystem metadata |
| Seed-5 PNG produced by a separate `model.val()` then `shutil.copy2`-copied into the run folder | `archive/Stracth/re_evaluate_seed5.py` | Source code |
| OCR procedure that produced the PNG readings | `archive/Stracth/_forensic_cm_ocr.py` | Source code |
| Params / GFLOPs / checkpoint / latency / FPS; `Peak_VRAM_MB` empty | `Ket_Qua_V2/efficiency_benchmark/tables/efficiency_summary.csv` | Data artifact (CSV) |
| 200 timed measurements (2 models × 100) | `Ket_Qua_V2/efficiency_benchmark/raw/efficiency_raw_benchmark.csv` | Data artifact (CSV) |
| GPU-style efficiency numbers and the "50.5 FPS beats 25–30 FPS" conclusion attributed to the CSV above | `archive/doc/20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md` §6 | Markdown (**conflicts with artifact**) |
| Stale FP baseline 17.4 marked retired | `archive/doc/LICHSU_CAP_NHAT.md` v3.1 | Markdown (changelog) |
| Claimed win counts 7/10 and 5/10 + 1 tie | `archive/doc/06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md` §3 | Markdown (**conflicts with artifact**) |
| 4-model / 400-row benchmark claims (P5 11.719 M / 477.98 ms; ITS 12.229 M / 651.27 ms) | `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/reports/*` | Markdown (**conflicts with artifact**) |
| Claimed "47 runs" | `archive/doc/03_CAU_TRUC…` §2, `doc/16_THUC_NGHIEM…` §5 | Markdown (**conflicts with artifact**) |
| Audit totals 559/559 and 694/694, unreconciled | `…/06_reports/final_audit_report.md` §2.1; `…/07_audit/audit_report.md` §1; `…/FORENSIC_EXPERIMENT_AUDIT.md` §10 | Generated reports |
| Audit generator not re-executed in this pass | `archive/Stracth/verify_10seed_audit.py` | Source code (absence of a run record) |
| 55 scripts in `Stracth/` | `archive/Stracth/*.py` | Directory enumeration |
| 12 thesis figures + 16 analysis charts + 15 efficiency figures | `KQ_Nen_DX_10seed/figures/`, `05_charts/`, `efficiency_benchmark/figures/` | Directory enumeration |
| Claim-family review of the 15 flagged families | `archive/15_CLAIM_FAMILIES_REVIEW.md` | Generated review (this pass) |
| Full 56-file claim audit and final verdict | `archive/MARKDOWN_CLAIM_AUDIT.md` | Generated audit (this pass) |
| Word design specifications (margins, fonts, structure, captions) | `archive/doc/19_…`, `doc/15_…`, `Bao_cao/CNTT_KLCN182_LeDucLuong.docx`, `Stracth/generate_final_word_report.py` | Specification + primary artifact + code |

---

`SOURCE SCOPE = archive/ only`
`PRIMARY SOURCE = archive/Ket_Qua_V2/**`
`NO SOURCE OR EVIDENCE FILE WAS MODIFIED`
`STATUS = COMPLETE`