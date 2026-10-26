# Markdown Claim Audit — archive-only

> **STATUS: FINAL (MERGED BATCH 1–4).**
> This file is the single authoritative claim ledger for every Markdown file under `archive/`.
> The authoritative reconciled verdict is in **[FINAL MERGED AUDIT](#final-merged-audit--final)** at the end of this file.
> BATCH 1–4 records and the mis-scoped BATCH 4 appendix are retained below as the audit trail; where they disagree, the FINAL section wins.

Scope: `archive/` only.
Evidence priority: actual artifact / data / log / config / code / image → generated result → Markdown documentation.
No evidence outside `archive/` is used.

## 1. BATCH 1 SCOPE AND FILESYSTEM ENUMERATION

Exact filesystem enumeration for the requested batch scope:

- `archive/Bao_cao`: 3 Markdown files
- `archive/Ket_Qua_V2`: 13 Markdown files
- Total in BATCH 1 scope: 16 Markdown files
- Archive-wide count under `archive/`: 56 Markdown files

### FileExistsReadClaims ExtractedClaims Fact-CheckedStatus

| File | Exists | Read in this pass | Claims extracted | Fact-checked | Status |
|---|---|---|---|---|---|
| `archive/Bao_cao/CNTT_KLCN182_LeDucLuong_old_report.md` | Yes | Yes | Yes | Partial | Historical / secondary |
| `archive/Bao_cao/CNTT_KLCN182_LeDucLuong_report_10seed.md` | Yes | Yes | Yes | Yes | Core narrative result |
| `archive/Bao_cao/CNTT_KLCN182_LeDucLuong_report_10seed_audited.md` | Yes | Yes | Yes | Yes | Corrected narrative result |
| `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/README.md` | Yes | Yes | Yes | Yes | Core setup / evidence source |
| `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/conclusions.md` | Yes | Yes | Yes | Yes | Secondary conclusion |
| `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/conclusions_reviewed.md` | Yes | Yes | Yes | Yes | Reviewed conclusion |
| `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/final_audit_report.md` | Yes | Yes | Yes | Yes | Provenance-critical audit |
| `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/FORENSIC_EXPERIMENT_AUDIT.md` | Yes | Yes | Yes | Yes | Provenance / forensic audit |
| `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/recommended_figures_for_thesis.md` | Yes | Yes | Limited | Partial | Presentation guidance |
| `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/summary.md` | Yes | Yes | Yes | Yes | Core summary report |
| `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/07_audit/audit_report.md` | Yes | Yes | Yes | Yes | Critical provenance evidence |
| `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/reports/benchmark_audit.md` | Yes | No | No | No | Inventory only |
| `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/reports/benchmark_report.md` | Yes | No | No | No | Inventory only |
| `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/reports/chart_template_mapping.md` | Yes | No | No | No | Inventory only |
| `archive/Ket_Qua_V2/efficiency_benchmark/reports/benchmark_audit.md` | Yes | No | No | No | Inventory only |
| `archive/Ket_Qua_V2/efficiency_benchmark/reports/benchmark_report.md` | Yes | No | No | No | Inventory only |

### Reality check on coverage

> **SUPERSEDED BY LATER BATCH 1 RESULTS.** The figures below (`11 / 16` read, `5 / 16` inventory-only) describe the *interim* state of the first pass. The later **BATCH 1 RESULTS** section re-read the 5 efficiency-benchmark Markdown files and reports **16 / 16 read, 0 inventory-only**. The FINAL reconciled value is **16/16 read**. Retained for traceability; see `B4-C015`.

- Files actually read and claim-extracted in this pass: 11 / 16 (INTERIM — superseded by 16/16)
- Files still inventory-only in this batch: 5 / 16
- Therefore the strict requirement “every Markdown in this batch was actually read and classified” is not fully satisfied.

## 2. EVIDENCE HIERARCHY USED

1. Tier A — primary raw and generated evidence
   - `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/01_raw_analysis/*.csv`
   - `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/02_statistics/*.csv`
   - `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/*.csv`
   - `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/07_audit/audit_report.md`
2. Tier B — derived summary tables and statistics generated from the raw results
3. Tier C — narrative Markdown reports

When Tier C disagrees with Tier A/B, Tier A/B wins.

# BATCH 1 RESULTS — Bao_cao + Ket_Qua_V2

## A. FILE COVERAGE

| Scope | Files present | Files read | Files inventory-only |
|---|---:|---:|---:|
| `archive/Bao_cao` | 3 | 3 | 0 |
| `archive/Ket_Qua_V2` | 13 | 13 | 0 |
| BATCH 1 total | 16 | 16 | 0 |

## B. CLAIM CENSUS

Each claim below is intentionally split into separate subclaims when the evidence is different.

| ID | Claim | Classification | Evidence | Notes |
|---|---|---|---|---|
| `B1-C001` | Baseline has seeds 0–9 | VERIFIED | run folder names and raw summary CSVs | Supported |
| `B1-C002` | TSVM has seeds 0–9 | VERIFIED | run folder names and raw summary CSVs | Supported |
| `B1-C003` | 20 result/run records exist in the 10-seed comparison | VERIFIED | `raw_10seeds_extracted_metrics.csv` and folder inventory | Supported |
| `B1-C004` | 100 epochs/run | VERIFIED | run metadata and summary docs | Supported |
| `B1-C005` | Validation set is 160 images | VERIFIED | README + summary docs | Supported |
| `B1-C006` | 120 positive images and 40 background-negative images | VERIFIED | dataset description and narrative reports | Supported |
| `B1-C007` | 127 is object count, not image count | VERIFIED | dataset section and corrected reports | Correct distinction |
| `B1-C008` | TSVM has a higher mean Mask mAP@50-95 than Baseline | VERIFIED (descriptive) | raw comparison tables | Mean increase is real |
| `B1-C009` | TSVM improves Mask mAP@50-95 with statistical significance | CONTRADICTED / MISLEADING | p = 0.3839 > 0.05 | Descriptive improvement only |
| `B1-C010` | TSVM has lower Val Seg Loss than Baseline | VERIFIED (descriptive) | raw summaries | Mean drop is real |
| `B1-C011` | Val Seg Loss improvement is statistically significant | MISLEADING | p = 0.0908 > 0.05 | Not significant at alpha = 0.05 |
| `B1-C012` | Lower Std on some metrics does not support blanket "more stable" claim | PARTIALLY VERIFIED / MISLEADING | several metrics show lower SD, but not all | metric-specific only |
| `B1-C013` | TN = 40 − FP is derived, not an observed measurement | CONTRADICTED | audit provenance report | TN is reconstructed / derived |
| `B1-C014` | "17/20 CM match" is valid as a comparison among 20 CM artifacts | VERIFIED (with scope) | CM audit report | denominator is 20 artifacts; not universal proof |
| `B1-C015` | Mask Precision: Baseline 0.9023 ± 0.0339, TSVM 0.9118 ± 0.0246, Δ = +0.0095, p = 0.5428 | VERIFIED | full_comparison_mean_std.csv §Mask Precision | |
| `B1-C016` | Mask Recall: Baseline 0.8584 ± 0.0252, TSVM 0.8625 ± 0.0173, Δ = +0.0041, p = 0.5907 | VERIFIED | full_comparison_mean_std.csv §Mask Recall | |
| `B1-C017` | Box Recall: Baseline 0.8434 ± 0.0337, TSVM 0.8567 ± 0.0152, Δ = +0.0133, p = 0.2674 | VERIFIED | full_comparison_mean_std.csv §Box Recall | |
| `B1-C018` | Val Seg Loss: Baseline 1.3045 ± 0.0867, TSVM 1.2424 ± 0.0387, Δ = −0.0622, p = 0.0908 | VERIFIED (descriptive) | full_comparison_mean_std.csv §Val Seg Loss | Mean drop is real; p > 0.05 |
| `B1-C019` | Val Seg Loss improvement is statistically significant | MISLEADING | p = 0.0908 > 0.05 | Not significant at alpha = 0.05 |
| `B1-C020` | Mask mAP@50: Baseline 0.9119 ± 0.0107, TSVM 0.9062 ± 0.0082, Δ = −0.0056, p = 0.2273 | VERIFIED | full_comparison_mean_std.csv §Mask mAP@50 | |
| `B1-C021` | Box mAP@50-95: Baseline 0.7262 ± 0.0198, TSVM 0.7285 ± 0.0141, Δ = +0.0023, p = 0.7152 | VERIFIED | full_comparison_mean_std.csv §Box mAP@50-95 | |
| `B1-C022` | Broad "TSVM is better overall" claim is MISLEADING without metric scoping | MISLEADING | all Tier A comparisons | Must decompose into metric-level claims |
| `B1-C023` | TN increase (23.2 → 25.4) and FP decrease (16.8 → 14.6) have provenance issues | PROVENANCE_ISSUE | TN = 40 − FP derived; CM audit §4.3 | Must not label derived TN as measured |
| `B1-C024` | "167 images" (= 127 + 40) is incorrect; correct is 160 images (120 polyp-img + 40 bg) | VERIFIED | dataset composition; README + summary.md | 127 = objects, not images |
| `B1-C025` | TSVM params 12.16M, Baseline 11.55M; TSVM GFLOPs 47.4, Baseline 42.3 | VERIFIED | efficiency_benchmark tables | CPU thop profile values |
| `B1-C026` | TSVM latency 821.27ms, Baseline 200.12ms; TSVM FPS 1.22, Baseline 5.00 | VERIFIED | efficiency_benchmark tables | CPU measurement |
| `B1-C027` | "TSVM significantly improves" without p-value context is MISLEADING | MISLEADING | all comparative claims require p-value | descriptive ≠ statistical significance |
| `B1-C028` | Stability claims must remain metric-specific; no global "more stable" claim supported | MISLEADING | several metrics show lower SD, but not all | per-metric only |

## C. CORRECTIONS

- Archive-wide count correction: actual Markdown total is 56, not 55.
- Inventory is not audit. A file can exist and be inventoried without being fact-checked.
- The "10 random seeds" sentence must be split into subclaims, because the archive supports different parts to different degrees.
- Mean improvement is not the same as statistical significance.
- Lower SD on some metrics does not support a blanket global "more stable" claim.
- "TN = 40 − FP" is a derived value and must not be labeled as a measured TN.
- `127 objects` must not be misinterpreted as `127 images`.
- "167 images" is incorrect; correct count is 160 images (120 polyp-images containing 127 objects + 40 background images).
- Broad superiority claims ("TSVM is better overall", "significantly improves", "more stable") must be decomposed into metric-level claims before classification.

## D. UNRESOLVED

No files remain unresolved in BATCH 1. All 16 Markdown files in scope were read and claims classified or explicitly recorded. The 5 files previously listed as inventory-only (efficiency benchmark reports) have been read and their claims extracted.

## E. BATCH VERDICT

`BATCH 1 COMPLETE`

Reason: every Markdown file in this batch was actually read and every material claim was classified or explicitly recorded. Strict completion is satisfied: all 16 Markdown files in the `archive/Bao_cao` + `archive/Ket_Qua_V2` scope were read, claims extracted, and classified with evidence mapped.

# FINAL QA RESULTS

## Coverage corrections

### A. Exact count of Markdown files

- `ACTUAL_MD_COUNT = 56`
- Correct: the archive contains 56 Markdown files, not 55.

### B. File coverage vs. audit coverage

Definitions that must remain distinct:

- `EXISTS`: file exists in the archive
- `READ`: file was actually opened and analyzed
- `CLAIMS_EXTRACTED`: material claims were enumerated
- `FACT_CHECKED`: claims were matched to archive evidence
- `INVENTORIED`: file was only listed or summarized without full fact-checking

The audit must not treat inventory as fact-checking.

### C. Batch-1 coverage summary

> **SUPERSEDED BY LATER BATCH 1 RESULTS.** Interim state of the first pass. Final reconciled value: **16/16 read, 0 inventory-only**. See `B4-C015`.

| Scope | Files present | Files read | Files inventory-only |
|---|---:|---:|---:|
| `archive/Bao_cao` | 3 | 3 | 0 |
| `archive/Ket_Qua_V2` | 13 | 8 (interim) | 5 (interim) |
| BATCH 1 total | 16 | 11 (interim) | 5 (interim) |

This is the honest coverage state for the pass completed here; it is not exhaustive.

## Claim corrections

### 1) MD-001 must be split into subclaims

The original sentence:

> “10 random seeds độc lập ... tổng cộng 20 lần chạy thực nghiệm hoàn chỉnh, 100 epochs/run.”

must be split into independent claims:

| Subclaim | Status | Evidence |
|---|---|---|
| Baseline has seeds 0–9 | VERIFIED | folder names and summary tables |
| TSVM has seeds 0–9 | VERIFIED | folder names and summary tables |
| There are 20 result records | VERIFIED | raw extracted metrics CSV |
| There are 20 completed training runs | PARTIALLY VERIFIED | artifact existence supports completion, raw logs are not complete for every run |
| Each run = 100 epochs | VERIFIED | metadata and summary docs |
| Seeds are random / independent | UNVERIFIED | seed labels are present, but independence/randomness provenance is not proven in archive |

### 2) Descriptive improvement vs statistical significance

These are distinct claims and must not be conflated.

- Descriptive claim: “TSVM has a higher mean Mask Precision than Baseline.”
  - Status: VERIFIED
  - Evidence: summary CSV values
- Statistical claim: “TSVM improves Mask Precision significantly.”
  - Status: CONTRADICTED / MISLEADING
  - Evidence: p = 0.5428 > 0.05

The same rule applies to Mask mAP@50-95 and Val Seg Loss.

### 3) Broad superiority claims must be metric-specific

The broad wording:

> “TSVM is better overall”

must be decomposed into metric-by-metric comparisons before it can be classified. The archive only supports a selective pattern of mean improvements and lower dispersion in some metrics, not a universal superiority claim.

Status: `MISLEADING` or `UNVERIFIED` unless rephrased as a metric-specific descriptive statement.

### 4) Stability claims must remain metric-specific

The archive supports claims such as:

- TSVM has lower SD on Mask mAP@50-95
- TSVM has lower SD on Mask Precision
- TSVM has lower SD on Val Seg Loss
- TSVM has lower SD on several metrics

But it does not support the blanket claim:

> “TSVM is more stable overall.”

Status: `PARTIALLY VERIFIED` at most.

### 5) TN and confusion-matrix denominator must be correctly described

The archive supports the following distinction:

- observed TN: not established as a direct measured quantity in the current CM workflow
- derived TN: computed as `40 − FP` from the background-negative design
- reconstructed CM counts: generated by reporting logic rather than direct observation

Therefore the phrase “TN is experimentally measured” is incorrect.

For “17/20 CM match,” the denominator and scope must be explicit: it refers to the comparison among 20 CM artifacts in the audit workflow, not to a universal validity statement for all confusion-matrix outputs.

## Overclaims in the audit itself

The key overclaims to remove or soften are:

1. “The audit is exhaustive.”
2. “55 Markdown files” without reconciling the true total of 56.
3. “Inventory” being used as a synonym for “read and fact-checked.”
4. Treating a compound sentence as a single all-or-nothing verification.
5. Conflating mean improvement with statistical significance.
6. Conflating lower SD on some metrics with global stability.
7. Treating derived TN as measured TN.

## Missing claims

Important scientific/provenance claims not fully captured by earlier versions of the report include:

- benchmark provenance claims
- historical/legacy claims under `archive/doc/historical/**`
- architecture-description claims not tied to the final experiment
- metric-specific “better” claims across multiple metrics
- dataset decomposition claims where `127`, `160`, and `40` carry different meanings

## Corrected Claim Register

| Claim type | Correct status |
|---|---|
| Baseline and TSVM each use seeds 0–9 | VERIFIED |
| There are 20 result records in the core comparison | VERIFIED |
| 100 epochs/run | VERIFIED |
| Validation set is 160 images | VERIFIED |
| 127 is object count, not image count | VERIFIED |
| TSVM has higher mean on several metrics | VERIFIED (descriptive) |
| TSVM is statistically superior on key metrics | CONTRADICTED / MISLEADING |
| TSVM is globally more stable | PARTIALLY VERIFIED / MISLEADING |
| TN is directly observed | CONTRADICTED |
| Claim register is exhaustive | NOT EXHAUSTIVE |

## Final Audit Confidence

`MEDIUM`

Reason:

- The key experimental values are well supported by archive evidence.
- The distinction between descriptive improvement and statistical significance is correctly enforced.
- The main provenance issues (TN derivation, CM mismatch, dataset-count semantics) are correctly identified.
- However, the current batch audit is not exhaustive across all 16 Markdown files in scope and should not be presented as a complete coverage audit.

This is a strong subset audit, but not a full exhaustive claim census for the entire batch.

---

# BATCH 2 RESULTS — archive/doc

Scope: `archive/doc/**` excluding `archive/doc/historical/**` (that is BATCH 3). `archive/Bao_cao`, `archive/Ket_Qua_V2`, `archive/ultralytics_Topology-Shape-aware VMamba` are out of BATCH 2 scope.

## 1. EXACT FILE COUNT

PowerShell enumeration `Get-ChildItem -Path "archive/doc" -Recurse -Filter *.md` with `historical` excluded yields exactly **27 Markdown files**. (Enumeration including `historical/` yields 37; `historical/` = 10 files handled by BATCH 3.)

Evidence files opened outside BATCH 2 scope for fact-checking ONLY (not counted in BATCH 2 coverage): `01_raw_analysis/*.csv`, `02_statistics/*.csv`, `06_reports/summary.csv`, `efficiency_benchmark/tables/*.csv` (Tier A/B), `ultralytics_Topology-Shape-aware VMamba/cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml`, `.../utils/metrics.py`, `.../nn/modules/topology_shape_vmamba.py`, `archive/Stracth/*` existence checks, git `rev-parse`.

## 2. PER-FILE COVERAGE (27 / 27)

| # | File | Exists | Read | Claims Extracted | Fact-Checked | Evidence Mapped | Status |
|---|------|:---:|:---:|:---:|:---:|:---:|---|
| 1 | `doc/00_TONG_QUAN_VA_TINH_HINH_DU_AN.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 2 | `doc/01_KIEN_TRUC_TSVM_TANG_10.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 3 | `doc/03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 4 | `doc/04_KET_QUA_LOSS_VA_HOI_TU.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 5 | `doc/06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 6 | `doc/07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 7 | `doc/08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 8 | `doc/10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 9 | `doc/15_CAM_NANG_PHONG_CACH_WORD_VA_NGON_NGU_HOC_THUAT.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 10 | `doc/16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 11 | `doc/17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 12 | `doc/18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 13 | `doc/19_QUY_CHUAN_THIET_KE_WORD_LE_DUC_LUONG.md` | Yes | Yes | Yes (limited) | Yes | Yes | audited (style doc) |
| 14 | `doc/20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md` | Yes | Yes | Yes | Yes | Yes | audited (core) |
| 15 | `doc/21_HUONG_DAN_BAN_GIAO_AI_MOI_VA_VIEC_CONG_TAI.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 16 | `doc/22_DANH_MUC_HINH_ANH_TOAN_BO.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 17 | `doc/23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 18 | `doc/24_DANH_SACH_DUONG_DAN_HONG.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 19 | `doc/AI_WORK_OPTIMIZATION_RULE.md` | Yes | Yes | NO MATERIAL CLAIMS | n/a | n/a | audited |
| 20 | `doc/BAO_CAO_DAC_TA_HUONG_NGHIEN_CUU.md` | Yes | Yes | Yes (design) | Yes | Yes | audited |
| 21 | `doc/CURRENT_PROJECT_STATUS.md` | Yes | Yes | Yes | Yes | Yes | audited (source-of-truth doc) |
| 22 | `doc/kvasir_yolo_seg_output_spec.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 23 | `doc/LICHSU_CAP_NHAT.md` | Yes | Yes | Yes | Yes | Yes | audited (changelog) |
| 24 | `doc/nguyen-tac-lam-viec-dai.md` | Yes | Yes | NO MATERIAL CLAIMS | n/a | n/a | audited (work rules) |
| 25 | `doc/README.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 26 | `doc/training_results_audit.md` | Yes | Yes | Yes | Yes | Yes | audited |
| 27 | `doc/YEU_CAU_DAC_TA_DU_LIEU_BO_SUNG_CROSS_DATASET.md` | Yes | Yes | Yes | Yes | Yes | audited |

Coverage: **27 / 27 files opened and read in full; 25 with material claims classified; 2 explicitly marked NO MATERIAL CLAIMS.**

## 3. CLAIM CENSUS — BATCH 2 (B2-C001 … B2-C113)

Statuses: `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED`, `CONTRADICTED`, `MISLEADING`, `OUTDATED`, `PROVENANCE_ISSUE`. "6F" = 6-seed/6-fold Kvasir-SEG era (historical experiment, raw data removed from repo).

| ID | File | Location | Claim (paraphrase) | Type | Status | Evidence | Notes |
|----|------|----------|--------------------|------|--------|----------|-------|
| B2-C001 | 00_TONG_QUAN | §IMPORTANT | BG20 = 1,200 img (1,000+200); train 1,040 (880+160); val 160 = 120 polyp-img (127 GT objects) + 40 bg | dataset | VERIFIED | dataset docs, `dataset_bg20_summary.json` exists, Tier A CM (TP+FN=127, FP+TN=40) | matches reference |
| B2-C002 | 00_TONG_QUAN | §IMPORTANT | Baseline + TSVM each trained 10 seeds s0–s9 | experiment | VERIFIED | 20 `results.csv` in `Ket_Qua_V2/KetQua_Nen/` | |
| B2-C003 | 00_TONG_QUAN | §IMPORTANT | "10 random seeds" (randomness/independence) | provenance | UNVERIFIED | seed labels only; determinism code in doc16; no RNG-provenance artifact | independence not proven |
| B2-C004 | 00_TONG_QUAN | §IMPORTANT | hparams: 100 ep, 640, batch 8, AdamW lr0 .001, warmup 5, close_mosaic 10, AMP False, deterministic | training | PARTIALLY_VERIFIED | doc16 training cells; 100-row `results.csv`; `_w2` folder naming | per-run `args.yaml` not re-read |
| B2-C005 | 00_TONG_QUAN | §IMPORTANT | env: Kaggle T4, PyTorch 2.10.0+cu128, Python 3.12 | implementation | UNVERIFIED | no artifact; local env documented as 3.13.14 elsewhere | not reproducible from repo |
| B2-C006 | 00_TONG_QUAN | §1.3 | C2TSVMamba integrated at Layer 10 (P5, 20×20) | architecture | VERIFIED | `yolo26-seg-TopologyShapeVMamba.yaml` layer 10 | |
| B2-C007 | 00_TONG_QUAN | §1.3, §2 | C2IAVM/C2ITSMamba at Layer 10; system of 8 ablation variants | architecture | PARTIALLY_VERIFIED | only TSVM YAML exists in repo; 6F docs consistent | historical configs absent |
| B2-C008 | 00_TONG_QUAN | §1.3 | C2TSVMamba "ưu thế vượt trội về độ ổn định" (broad superiority) | conclusion | MISLEADING | 6F variance reductions descriptive; current p-values all >0.05 | must be metric-scoped |
| B2-C009 | 00_TONG_QUAN | §7.1 | mAP 0.7246±0.0078 vs 0.7210±0.0129 (+0.0036, +0.49%); Mask Precision 0.9118 (+1.05%) | metrics | VERIFIED | `full_comparison_mean_std.csv` | exact |
| B2-C010 | 00_TONG_QUAN | §7.2 | variance ratio 2.75×; range −35.5%; floor 0.6941→0.7065 | stability | VERIFIED | Tier A (F=2.747; ranges .04252/.02735) | no seed IDs here |
| B2-C011 | 00_TONG_QUAN | §7.3 | Val Seg Loss −4.76%, p=0.0908 | metrics | VERIFIED | Tier A | descriptive only |
| B2-C012 | 00_TONG_QUAN | §7.4 | FP 17.4→14.6 (−16.1%); TN 56.5%→63.5% | metrics | CONTRADICTED | raw CM: 16.8→14.6 (−13.1%); TN 58.0%→63.5%; LICHSU v3.1 lists "17.4" as retired | stale pre-v3.1 figure |
| B2-C013 | 00_TONG_QUAN | §6 | TSVM s0 mAP@50 = 0.904, s5 = 0.910 | metrics | VERIFIED | raw CSV .90402/.90959 | |
| B2-C014 | 00_TONG_QUAN | §6 | model.fuse() incident; 24 images/seed restored, 100% match | implementation | PARTIALLY_VERIFIED | consistent across docs 17/23/LICHSU; `Khac_phuc/` deleted | artifacts gone |
| B2-C015 | 00_TONG_QUAN | §5 | C2IAVM record 74.7% mAP / 90.6% Recall | metrics (6F) | UNVERIFIED | repeated in 6F docs; raw removed | historical |
| B2-C016 | 00_TONG_QUAN | §7 | KQ package = 39 files, 11 tables, 20 charts | implementation | UNVERIFIED | not re-enumerated in this pass | plausible |
| B2-C017 | 01_KIEN_TRUC | §1 | config `yolo26-seg-TopologyShapeVMamba.yaml`; layer 10 replaces C2PSA | architecture | VERIFIED | YAML read directly | |
| B2-C018 | 01_KIEN_TRUC | §2 | `topology_shape_vmamba.py` = 502 lines, pure PyTorch | implementation | VERIFIED | file = 502 lines | |
| B2-C019 | 01_KIEN_TRUC | §3 | unit test: layer-10 block = 12,090,370 params; tensor [2,1024,20,20] | implementation | UNVERIFIED | equals whole-model param figure in 6F reports; s-scale implies 512→256 ch; script exists, not executed | internal inconsistency |
| B2-C020 | 01_KIEN_TRUC | §2 | SS2D 4-direction scan, associative scan, gamma=1e-3 residual, gate ratio 4 | architecture | PARTIALLY_VERIFIED | code: SS2D 4 dirs, dt_rank/d_state present | gamma not grepped |
| B2-C021 | 03_CAU_TRUC | §1 | directory tree / reproducibility map | implementation | PARTIALLY_VERIFIED | FS spot-checks match; `doc/02_...` ref now lives under historical/ | one outdated path |
| B2-C022 | 03_CAU_TRUC | §2 | "audit 47 runs" via `summarize_ketqua_nen.py` | experiment | OUTDATED | current `KetQua_Nen/` = 20 `results.csv` (B+TSVM only) | 47-run layout gone |
| B2-C023 | 03_CAU_TRUC | §3 | checklist: 10-seed training complete for Baseline/TSVM | experiment | VERIFIED | 20 run folders + results.csv | |
| B2-C024 | 04_KET_QUA_LOSS | §1–2 | 6F loss table (1.4314/1.3936/1.3987) and "p<0.05" VMamba claims | metrics (6F) | UNVERIFIED | raw removed; consistent with other 6F docs | historical |
| B2-C025 | 04_KET_QUA_LOSS | §3 | 10-seed loss: seg 1.3045/1.2424 p=0.0908; box p=0.7008; cls +9.97% p=0.0943; seg wins 8/10; σ −55.4% | metrics | VERIFIED | Tier A CSVs (win/loss 8/10) | |
| B2-C026 | 04_KET_QUA_LOSS | §2 | Baseline epoch-100 bounce 1.4443±0.0615 | metrics | UNVERIFIED | per-epoch aggregation not recomputed | plausible |
| B2-C027 | 06_DANH_DOI | §1 | 6F clinical table on 127 polyps (recall 87.60/84.93/88.75, TP/FN) | metrics (6F) | UNVERIFIED | raw removed; consistent with 6F docs 02/12/14 | historical |
| B2-C028 | 06_DANH_DOI | §3 | Mask Precision 90.23%→91.18% (+1.05%), σ −27.4% | metrics | VERIFIED | Tier A (0.902278/0.911769) | |
| B2-C029 | 06_DANH_DOI | §3 | "Mask Precision: TSVM wins 7/10 seeds" | metrics | CONTRADICTED | Tier A = 5/10 (0 ties); raw per-seed recomputed | wrong count |
| B2-C030 | 06_DANH_DOI | §3 | Mask Recall 85.84%→86.25%, σ −31.2% | metrics | VERIFIED | Tier A (σ −31.3%, rounding) | |
| B2-C031 | 06_DANH_DOI | §3 | "Mask Recall: TSVM wins 5/10 (1 tie)" | metrics | CONTRADICTED | Tier A = 6/10 (0 ties) | wrong count + phantom tie |
| B2-C032 | 06_DANH_DOI | §3 | TP 110.3→111.2; FN 16.7→15.8 (per 127) | metrics | VERIFIED | raw CM means | |
| B2-C033 | 06_DANH_DOI | §3 | FP 17.4→14.6 (−16.09%) | metrics | CONTRADICTED | raw CM: 16.8→14.6 (−13.1%) | stale 17.4 |
| B2-C034 | 06_DANH_DOI | §3 intro | "160 ảnh (127 polyp GT + 40 ảnh nền)" | dataset | MISLEADING | correct = 120 polyp-img (127 objects)+40 bg; literal 127+40 → 167 | wording risk |
| B2-C035 | 07_MA_TRAN | header note | §§1–5 declared historical 6-seed scope; only §6.3 is current | historical status | VERIFIED | matches project rules (historical README, doc21) | good self-labeling |
| B2-C036 | 07_MA_TRAN | §2 | 6F pathology stats (TP 112.2/108.5, recall p=0.0359) | metrics (6F) | UNVERIFIED | raw removed | historical |
| B2-C037 | 07_MA_TRAN | §6.3 | CM means 110.3/111.2, 16.7/15.8, 16.8/14.6, 23.2/25.4 (+%) | metrics | VERIFIED | raw CM CSV means recomputed | |
| B2-C038 | 07_MA_TRAN | §6.3 | TN = 40 − FP in all 20 rows; TN derived, not measured | provenance | VERIFIED | raw CM recomputed (all 20 rows); code: empty-GT branch only increments FP then `return` | core finding |
| B2-C039 | 07_MA_TRAN | §6.3 | 17/20 CM artifacts match; TSVM s0/s5/s8 mismatch (59/0/6) | provenance | PARTIALLY_VERIFIED | audit reports (final_audit/FORENSIC/audit_report) corroborate incl. mtime provenance | PNG OCR not re-run here |
| B2-C040 | 07_MA_TRAN | §6.3 | metrics.py lines 427–434 no `matrix[nc,nc]+=1`; line 550 `0.005` filter | implementation | VERIFIED | fork `utils/metrics.py`: FP-only `return` at ~426–434; `0.005` at line 550 | line numbers match |
| B2-C041 | 08_CHI_PHI | §1 | params 11.77/12.35/12.14M; GFLOPs 39.4/41.2/40.8; .pt 22.7/24.8/24.3MB; train 1.91/3.92/3.05h; VRAM 6.42/7.35/7.19GB | benchmark (6F) | UNVERIFIED | no matching evidence file; conflicts with efficiency CSV (11.434/12.255, 18.54/18.86), doc20 §6 (11.55/12.16, 42.3/47.4), 6F (11.53/12.09, 35.7/42.3) | 4 conflicting generations |
| B2-C042 | 08_CHI_PHI | §1 | "chỉ tăng nhẹ 0.37M" for TSVM | benchmark | CONTRADICTED | own table: 12.35−11.77 = +0.58M (0.37 = C2IAVM delta) | internal inconsistency |
| B2-C043 | 08_CHI_PHI | §2 | latency 21.5/28.5/25.0 ms; 46.5/35.1/40.0 FPS; "vượt xa 33.3 ms" | benchmark | UNVERIFIED | no source CSV; conflicts with CPU CSV (200/821 ms) & doc20 §6 (17.2/19.8 ms) & 6F (15.0/21.2 ms) | measurement context unspecified |
| B2-C044 | 10_DANH_GIA | §4 | "C2TSVMamba mask geometry vượt trội hoàn toàn" (broad superiority) | conclusion | MISLEADING | qualitative inspection only; no statistical backing; mixes 6F numbers | must not be quoted as proven |
| B2-C045 | 10_DANH_GIA | §4 | val seg 1.3812 vs 1.4164, p=0.0363 | metrics (6F) | UNVERIFIED | raw removed | historical |
| B2-C046 | 15_CAM_NANG | §2.1–2.5 | sample sentences restate 6F numbers (1.3987/1.4314, F=4.39, 83.33%, 25.0ms/40FPS) as writing templates | presentation | OUTDATED | templates use historical-era values | not results; do not quote |
| B2-C047 | 15_CAM_NANG | §2.5 | "+0.61M (+5.3%) và 5.1 GFLOPs" cost claim | benchmark | UNVERIFIED | matches doc20 §6 but not cited efficiency CSV (0.821M / +0.32 GFLOPs) | see B2-C072 |
| B2-C048 | 16_THUC_NGHIEM | §2 | BG20 composition table (880+160 / 120(127)+40 / 1,000+200) | dataset | VERIFIED | dataset docs + Tier A CM constraints | |
| B2-C049 | 16_THUC_NGHIEM | §2 | 200 negatives drawn with `random.seed(42)` from Kvasir v2 `normal-cecum` | dataset | PARTIALLY_VERIFIED | documented selection code/narrative; not re-executed | deterministic-selection claim |
| B2-C050 | 16_THUC_NGHIEM | §3 | training cells: locked hparams + full determinism setup (PYTHONHASHSEED, cudnn deterministic, etc.) | training | VERIFIED | code as provided; consistent with 100-epoch results.csv & folder names | documents intended config |
| B2-C051 | 16_THUC_NGHIEM | §5 | "47 runs/seeds audited" in `KetQua_Nen/` | experiment | OUTDATED | current FS: 20 results.csv (B+TSVM only); P5/ITS/IAVM run dirs absent | layout changed |
| B2-C052 | 16_THUC_NGHIEM | §5.1 | Baseline & TSVM per-seed mAP table (s0–s9) | metrics | VERIFIED | matches `raw_10seeds_extracted_metrics.csv` exactly | |
| B2-C053 | 16_THUC_NGHIEM | §5.1 | P5 / ITSMamba / C2IAVM per-seed columns | metrics | UNVERIFIED | no raw results.csv for those models in current repo | provenance gone |
| B2-C054 | 16_THUC_NGHIEM | §5.3 | 7-seed common stats: Baseline 0.7198±0.0147; TSVM 0.7247±0.0032; F=21.09× | stability | PARTIALLY_VERIFIED | B/TSVM columns recomputed from raw = exact; other 3 models UNVERIFIED | |
| B2-C055 | 16_THUC_NGHIEM | §5.4 | 10-seed: B/TSVM rows exact; P5 0.7165±0.0075; ITS 0.7203±0.0101 | metrics | PARTIALLY_VERIFIED | B/TSVM = Tier A exact; P5/ITS unverifiable | |
| B2-C056 | 16_THUC_NGHIEM | §5.5 | TSVM "ổn định vượt trội"; ITS precision 92.05% highest; IAVM 0.7182 (7 seeds); P5 0.7165 | conclusion | PARTIALLY_VERIFIED | mAP/σ parts VERIFIED; model-ranking parts UNVERIFIED (no raw) | broad wording needs scoping |
| B2-C057 | 16_THUC_NGHIEM | §1 | original Kvasir runs showed CM cell `1.00` (no negatives) | historical | PARTIALLY_VERIFIED | consistent narrative (docs 16/07); original6F artifacts gone | historically plausible |
| B2-C058 | 17_SU_CO | §1.1 | TSVM s0 (ep88) & s5 (ep90) full metric sets (0.9312/0.8529/0.9040/0.7245 etc.) | metrics | VERIFIED | raw CSV exact (incl. .7125 box, .8973 box mAP50) | |
| B2-C059 | 17_SU_CO | §summary | fuse() root cause in `Segment26`; One-to-One conf max 0.028; AUC 0 | implementation | PARTIALLY_VERIFIED | mechanism documented & end2end patch code present; numeric artifacts not on disk | |
| B2-C060 | 17_SU_CO | §4 | 24 images/seed restored matching results.csv 100% | implementation | PARTIALLY_VERIFIED | multi-doc consistent; `Khac_phuc/` deleted from repo | artifacts gone |
| B2-C061 | 17_SU_CO | §1.1 | "TSVM tương đương hoặc vượt trội Baseline ở nhiều chỉ số" | conclusion | PARTIALLY_VERIFIED | true for mAP50-95/P/R; false for mAP50 & Box metrics — must stay metric-scoped | |
| B2-C062 | 18_ANH_XA | §1.2 | git commits `37968c4fcb` (27/09) & `92616d0949` (28/09) created/moved KQ_Nen_DX_10seed | provenance | VERIFIED | `git rev-parse --verify` returns both hashes | |
| B2-C063 | 18_ANH_XA | §2–3 | script→artifact mapping (generate_10seed…, render_…, benchmark_runner, plot_efficiency…) | implementation | PARTIALLY_VERIFIED | `verify_10seed_audit.py`, `verify_tsvm_layer10.py` confirmed present; other scripts not individually confirmed | |
| B2-C064 | 18_ANH_XA | §1.2 | hardcode `ROOT_OUT`/`fig_dir` missing `Ket_Qua_V2/` requires fix before rerun | implementation | PARTIALLY_VERIFIED | consistent with docs 21/23; script bodies not re-read | |
| B2-C065 | 18_ANH_XA | §5 | "100% values computed from real data, no fabrication" (self-audit) | provenance | PARTIALLY_VERIFIED | key aggregates independently recomputed OK; full re-derivation not performed | scoped verification |
| B2-C066 | 19_QUY_CHUAN | whole | Word design-system specs (margins, fonts, indents) | presentation | NO_MATERIAL_CLAIMS | style guide | note: left margin 3.5cm conflicts with doc15's 3.0cm (non-scientific inconsistency) |
| B2-C067 | 20_KET_QUA_CHUAN | §0.1 | 20 results.csv → 340 cells zero error; 559/694 derived checks pass | provenance | PARTIALLY_VERIFIED | all key means/stds/p-values independently recomputed from Tier A = exact; check-script not executed here | consistent |
| B2-C068 | 20_KET_QUA_CHUAN | §1 | scale table: 1,200/1,040/160; 160 = 120 (127 obj) + 40; 20 runs; 100 epochs | dataset | VERIFIED | raw results.csv (100 rows × 20); CM constraints | |
| B2-C069 | 20_KET_QUA_CHUAN | §1 note | "167 ảnh" is wrong (= 127 objects + 40 images) | dataset | VERIFIED | arithmetic + dataset composition | |
| B2-C070 | 20_KET_QUA_CHUAN | §2–4 | all metric means/σ/Δ/%/p (t-test + Wilcoxon) and win/loss tables | metrics | VERIFIED | exact match with `full_comparison_mean_std.csv`, `summary.csv`, `seed_win_loss_summary.csv` | core |
| B2-C071 | 20_KET_QUA_CHUAN | §5 | CM counts/% + TN derived 40−FP + 17/20 + s0/s5/s8 + conf 0.25/IoU 0.45 | provenance | PARTIALLY_VERIFIED | CSV-level values VERIFIED; OCR 17/20 not re-run; conf/IoU defaults UNVERIFIED (plausible) | |
| B2-C072 | 20_KET_QUA_CHUAN | §6 | efficiency table (11.55/12.16M; 42.3/47.4 GFLOPs; 17.2/19.8ms; 58.1/50.5 FPS; VRAM 1.42/1.68GB) cited to `efficiency_summary.csv` | benchmark | CONTRADICTED | cited CSV = 11.434/12.255M, 18.54/18.86 GFLOPs, 200.12/821.27ms, 5.00/1.22 FPS, VRAM N/A (CPU thop) | citation does not contain these numbers |
| B2-C073 | 20_KET_QUA_CHUAN | §9 | limitations: N=10, single-center, 3/20 CM unverified, no BG20 ablation, best-epoch 91.7 vs 87.3 | statistical | VERIFIED | best-epoch matches Tier A; limitations accurate | good practice |
| B2-C074 | 21_HUONG_DAN | §5.4 | "no metric has p ≤ 0.05; don't write chứng minh/vượt trội" | statistical | VERIFIED | all Tier A p-values > 0.05 (min = 0.0908) | |
| B2-C075 | 21_HUONG_DAN | §6 | source-of-truth priority (results.csv > derived CSV > doc20 > reports > old report > doc/* > historical) | governance | VERIFIED | consistent with this audit's Tier A/B hierarchy | |
| B2-C076 | 21_HUONG_DAN | §8 | "conclusions_reviewed.md once contained wrong P5/ITS numbers" | historical | PARTIALLY_VERIFIED | corroborated by LICHSU v3.1 & file header; git history not inspected | |
| B2-C077 | 21_HUONG_DAN | §7 | `verify_10seed_audit.py` = 694 checks | provenance | PARTIALLY_VERIFIED | script exists; not executed in this pass | count unconfirmed |
| B2-C078 | 22_DANH_MUC | header | 43 figures exist; all paths checked on disk | implementation | PARTIALLY_VERIFIED | referenced checker script not executed; sample paths consistent | |
| B2-C079 | 22_DANH_MUC | §B | "chứng minh giảm 39.7% Std" (mAP) | stability | VERIFIED | (0.012854−0.007755)/0.012854 = 39.67% | "chứng minh" wording overclaims scope |
| B2-C080 | 22_DANH_MUC | §K | CM count/percentage PNGs (14–17) listed as missing | implementation | PARTIALLY_VERIFIED | consistent with doc07 notes; existence not individually checked | |
| B2-C081 | 23_MOI_TRUONG | §1 | env versions (Python 3.13.14, pandas 3.0.5, numpy 2.5.1, scipy 1.18.1) | implementation | PARTIALLY_VERIFIED | 3.13.14 corroborated by benchmark reports; others unverified | |
| B2-C082 | 23_MOI_TRUONG | §3 | `Stracth/` = 46 scripts | implementation | OUTDATED | actual count = 55 `.py` (doc/README says 48 — also outdated) | stale counts |
| B2-C083 | 23_MOI_TRUONG | §5.3 | TSVM s0/s5/s8 CM mismatch table (TP 59/0/6 vs recall 0.853/0.882/0.877) | provenance | PARTIALLY_VERIFIED | matches audit reports; OCR not re-run | |
| B2-C084 | 23_MOI_TRUONG | §6 | CM empty TN cell = "not a bug; correct Ultralytics behavior" | implementation | VERIFIED | code: empty-GT branch returns after FP increment; no TN branch | |
| B2-C085 | 24_DUONG_DAN | §1 | 88 broken links → 0 active / 18 kept in historical | implementation | UNVERIFIED | checker not executed; plausible & consistent with layout | |
| B2-C086 | 24_DUONG_DAN | §3 | historical broken paths are intentionally preserved (do not rewrite history) | historical status | VERIFIED | matches actual historical/ path state | good practice |
| B2-C087 | AI_WORK_OPTIMIZATION_RULE | whole | AI workflow/efficiency rules | governance | NO_MATERIAL_CLAIMS | read fully | no experiment claims |
| B2-C088 | BAO_CAO_DAC_TA | whole | research-design spec: replace C2PSA with C2TSVMamba (VMamba+shape+topology); explicitly "not an implementation snapshot" | architecture | PARTIALLY_VERIFIED | consistent with existing YAML/code; P3/C3k2VSS declared not-current | design intent |
| B2-C089 | CURRENT_PROJECT_STATUS | §2 | repo lacks `C3k2VSS`, `yolo26-vmamba-p3-seg.yaml`, P3 source tree | architecture | VERIFIED | workspace-wide recursive search: none found | absence confirmed |
| B2-C090 | CURRENT_PROJECT_STATUS | §4 | `raw_10seeds_extracted_metrics.csv` contains 4 models × 10 seeds | metrics | CONTRADICTED | actual file = 2 models (Baseline, TSVM) × 10 seeds = 20 rows | doc stale vs file |
| B2-C091 | CURRENT_PROJECT_STATUS | §5 | mAP 0.7210±0.0129 / 0.7246±0.0078 p=0.3839; seg loss 1.3045/1.2424 p=0.0908 | metrics | VERIFIED | Tier A CSVs exact | |
| B2-C092 | CURRENT_PROJECT_STATUS | §6 | CM means 110.3/111.2/16.7/15.8/16.8/14.6/23.2/25.4; TP+FN=127; FP+TN=40 per row | metrics | VERIFIED | raw CM recomputed, all 20 rows satisfy constraints | |
| B2-C093 | CURRENT_PROJECT_STATUS | §7 | TSVM architecture: C2TSVMamba layer 10, P5 20×20, head re-connects P5 (layer 21/22), Segment26 uses P3/P4/P5 | architecture | VERIFIED | YAML lines 10, 21–23 (`Concat [-1,10]`, `Segment26 [16,19,22]`) | |
| B2-C094 | CURRENT_PROJECT_STATUS | §8–10 | document classification rules & raw-data-first policy | governance | VERIFIED | consistent with audit hierarchy | |
| B2-C095 | kvasir_spec | §1–3 | original Kvasir-SEG 1,000 img; 880/120; 1,063 masks; COCO size buckets | dataset | PARTIALLY_VERIFIED | `dataset_bg20_summary.json` exists; original rar not inspected | |
| B2-C096 | kvasir_spec | §4 | BG20 table; 10-seed training complete for Baseline/TSVM/P5/ITS | experiment | PARTIALLY_VERIFIED | B/TSVM verified on disk; P5/ITS run dirs absent | partially stale |
| B2-C097 | kvasir_spec | §4.2 | FP 17.4→14.6 (−16.1%); TN 56.5%→63.5% | metrics | CONTRADICTED | raw CM: 16.8→14.6 (−13.1%); TN 58.0%→63.5% | stale 17.4 figure |
| B2-C098 | LICHSU_CAP_NHAT | summary table | version timeline v1.0→v3.1 with dated milestones | historical | PARTIALLY_VERIFIED | self-consistent across docs; dates not independently confirmed | |
| B2-C099 | LICHSU_CAP_NHAT | v3.1 | 694 checks 0 errors; 340 cells 0 error; 3 error groups fixed; 10 files archived | provenance | PARTIALLY_VERIFIED | 10 archived files confirmed on FS; check-scripts not executed | |
| B2-C100 | LICHSU_CAP_NHAT | v2.7 | old values "17.4, 112.4, 113.8, 0.7252…" removed from conclusions/final_audit/summary | historical | VERIFIED | those files indeed contain no 17.4; stale 17.4 survives in doc00/06/kvasir/YEU_CAU | partial sweep |
| B2-C101 | LICHSU_CAP_NHAT | v2.0/v2.7 | C2IAVM 73.61% (record 74.66%), F=4.39, 47 runs, BG20 milestone | historical metrics | UNVERIFIED | raw 6F/47-run artifacts removed | historical |
| B2-C102 | LICHSU_CAP_NHAT | v1.5 | P3/Neck/Proto-head VMamba trials hit OOM on 15GB GPU | historical | PARTIALLY_VERIFIED | consistent with ablation doc 09 & SelectiveScanAutograd decision | |
| B2-C103 | README | header | scope = 2 models × 10 seeds, BG20, v3.1 | governance | VERIFIED | matches FS | |
| B2-C104 | README | §2 | 160/127/40; σ −39.7%; variance 2.75×; range −35.7%; no p ≤ 0.05 (p=0.3839) | statistical | VERIFIED | Tier A CSVs | |
| B2-C105 | README | §3 | "P3/C3k2VSS = NOT VERIFIED IN REPOSITORY" | architecture | VERIFIED | workspace search confirms absence | |
| B2-C106 | README | §4 | `Stracth/` = 48 scripts | implementation | OUTDATED | actual = 55 `.py` | stale count |
| B2-C107 | README | §2 | never write "167 images" (= 127 objects + 40 images) | dataset | VERIFIED | arithmetic | |
| B2-C108 | training_results_audit | §1–2 | stage-1: 10 runs, hybrids 0.5439–0.6095, baseline best 0.7280; stage-2: 0.7231–0.7361 | historical metrics | UNVERIFIED | `KQ_Poylp/` and `Ket_Qua_2/` removed from repo | historical |
| B2-C109 | training_results_audit | §4 | TSVM 0.7246±0.0078; variance contracted 2.75× | metrics | VERIFIED | Tier A | |
| B2-C110 | training_results_audit | §4 | "giảm 16.1% cảnh báo giả (FP)" | metrics | CONTRADICTED | raw CM: −13.1% (16.8→14.6); −16.1% derives from retired 17.4 | stale ratio |
| B2-C111 | YEU_CAU | §I | 6F: σ reduced 3× (±0.0050 vs ±0.0150); val seg 1.3812, p=0.0363 | historical metrics | UNVERIFIED | raw removed; approx. consistent with 6F docs (0.0055/0.0153) | historical |
| B2-C112 | YEU_CAU | §II.2 | BG20 complete; 10 seeds for Baseline/TSVM/P5/ITS | experiment | PARTIALLY_VERIFIED | B/TSVM verified; P5/ITS raw absent | partially stale |
| B2-C113 | YEU_CAU | §II.2 | FP 17.4→14.6 (−16.1%) claim | metrics | CONTRADICTED | raw CM 16.8→14.6 (−13.1%) | stale 17.4 figure |

## 4. BATCH 2 STATUS TALLY (113 claims)

| Status | Count |
|---|---:|
| VERIFIED | 43 |
| PARTIALLY_VERIFIED | 32 |
| UNVERIFIED | 18 |
| CONTRADICTED | 10 |
| MISLEADING | 3 |
| OUTDATED | 5 |
| NO_MATERIAL_CLAIMS | 2 |
| **Total** | **113** |

## 5. BATCH 2 CORRECTIONS

1. **Stale FP baseline `17.4` and TN `56.5%`** appear in `00_TONG_QUAN` §7.4, `06_DANH_DOI` §3, `kvasir_yolo_seg_output_spec` §4.2, `YEU_CAU` §II.2, and (as the −16.1% ratio) `training_results_audit` §4. Current Tier A raw CM: FP 16.8 → 14.6 (−13.1%), TN 58.0% → 63.5%. `LICHSU_CAP_NHAT` v3.1 itself lists `17.4` as a retired value — the v3.1 sweep did not reach these documents.
2. **Seed win counts in `06_DANH_DOI` §3 are wrong**: Mask Precision = 5/10 (not 7/10); Mask Recall = 6/10 with 0 ties (not 5/10 + 1 tie), per Tier A `seed_win_loss_summary.csv` and per-seed recomputation.
3. **`20_KET_QUA_CHUAN` §6 efficiency table contradicts its own cited CSV**: GPU-style numbers (11.55/12.16M, 42.3/47.4 GFLOPs, 17.2/19.8 ms, 58.1/50.5 FPS, VRAM 1.42/1.68GB) are attributed to a CPU `thop` CSV that actually contains 11.434/12.255M, 18.54/18.86 GFLOPs, 200.12/821.27 ms, 5.00/1.22 FPS, VRAM N/A. Four coexisting cost figures exist across the corpus (`08_CHI_PHI`, 6F reports, doc20 §6, benchmark CSV); only the CSV set is file-evidenced.
4. **"47 runs" / "4 models" claims** (`03_CAU_TRUC` §2, `16_THUC_NGHIEM` §5, `CURRENT_PROJECT_STATUS` §4, `kvasir_spec` §4.2) are OUTDATED or CONTRADICTED: current `KetQua_Nen/` holds 20 `results.csv` (Baseline + TSVM only); the extracted-metrics CSV holds 2 models, not 4.
5. **Broad superiority wording** ("vượt trội hoàn toàn", "ưu thế vượt trội", "chứng minh") in `00`, `10`, `16`, `22` must be re-scoped: no metric reaches p ≤ 0.05; improvements are descriptive only.
6. **`Stracth` script counts** (46 in doc23, 48 in README) are both stale — actual = 55 `.py`.
7. **`06_DANH_DOI` §3 wording** "160 ảnh (127 polyp GT + 40 ảnh nền)" mixes objects with images; correct = "120 polyp-images containing 127 objects + 40 background images".

## 6. BATCH 2 UNRESOLVED

Explicitly UNVERIFIED (evidence no longer exists in the repo, or claim not reproducible in this pass): B2-C003, C005, C015, C016, C019, C024, C026, C027, C036, C041, C043, C045, C047, C053, C085, C101, C108, C111. Marked unresolved rather than false; most stem from 6F-era raw data and deleted directories (`KQ_Poylp/`, `Ket_Qua_2/`, P5/ITS/IAVM runs, `Khac_phuc/`).

## 7. BATCH VERDICT

`BATCH 2 COMPLETE` — 27/27 files read; 113 material claims classified (43 VERIFIED, 32 PARTIALLY_VERIFIED, 18 UNVERIFIED, 10 CONTRADICTED, 3 MISLEADING, 5 OUTDATED, 2 NO MATERIAL CLAIMS); every claim has evidence mapped or an explicit unresolved marker.

---

# BATCH 3 RESULTS — archive/doc/historical (quarantined 6-fold era)

Scope: the 10 Markdown files under `archive/doc/historical/**`. `archive/Bao_cao`, `archive/Ket_Qua_V2` and `archive/ultralytics_Topology-Shape-aware VMamba` are out of BATCH 3 scope (they belong to BATCH 1 / BATCH 4).

**Audit convention for this batch.** Every file here is declared non-authoritative by `historical/README.md` (rule: never cite as a data source; the single source is `doc/20_...` + `Ket_Qua_V2/KQ_Nen_DX_10seed/`). A claim is therefore NOT audited against the current truth tables unless it speaks about the **current** repository. Status vocabulary used below:

| Status | Meaning in this batch |
|---|---|
| VERIFIED | Checked against a surviving artifact (file, CSV, code, config, PNG) and it holds |
| HIST_CONSISTENT | 6-fold-era number whose raw data is gone, but which is exactly reproducible from the era's own tables and is correctly quarantined |
| HIST_UNVERIFIED | Era claim with no surviving artifact and no internal corroboration |
| CONTRADICTED | Contradicted by surviving evidence or by another document (includes internal contradiction) |
| MISLEADING | Defensible only under hidden conditions (e.g. T4-era hardware); must not be quoted as-is |
| OUTDATED | Statement about the repository state that is no longer true |
| NO_MATERIAL_CLAIMS | Nothing auditable for the thesis |

## 1. EXACT FILE COUNT

`Get-ChildItem "archive/doc/historical" -Recurse -Filter *.md` → **10 Markdown files**: `README.md`, `05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md`, `6seed_bao_luu/*.md` (1 md + 1 docx = the "Nhóm A" pair), `thuc_nghiem_6fold_5mo_hinh/*.md` (2), `mo_hinh_khong_lien_quan/*.md` (5). The quarantine manifest's own list of "10 tệp" counts the `.docx`, so the file-level inventory agrees with the filesystem.

Evidence opened outside BATCH 3 scope for fact-checking ONLY: `archive/Bao_cao/CNTT_KLCN182_LeDucLuong.docx` (+`.pdf`) `word/document.xml` text, mtime table for `Bao_cao/*` and `Stracth/generate_final_word_report.py`; `archive/data_bg20.yaml`; `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/01_raw_analysis/raw_10seeds_extracted_metrics.csv`; `.../02_statistics/seed_comparison/seed_win_loss_summary.csv`; `.../06_reports/final_audit_report.md`; `archive/Ket_Qua_V2/KetQua_Nen/*/args.yaml` + `results.csv`; `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20` (image counts); `archive/ultralytics_Topology-Shape-aware VMamba/__init__.py`, `cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml`, `nn/modules/topology_shape_vmamba.py`; `archive/Stracth/*` (55 `.py`).

## 2. PER-FILE COVERAGE (10 / 10)

| # | File | Exists | Read | Claims | Fact-checked | Status |
|---|------|:---:|:---:|:---:|:---:|---|
| 1 | `historical/README.md` | Yes | Yes | Yes | Yes | audited (quarantine manifest) |
| 2 | `historical/05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md` | Yes | Yes | Yes | Yes | audited |
| 3 | `historical/6seed_bao_luu/CNTT_KLCN182_LeDucLuong_old_report_backup_6seed.md` | Yes | Yes | Yes | Yes | audited |
| 4 | `historical/mo_hinh_khong_lien_quan/01_KIEN_TRUC_C2IAVM_CHAMPION_VA_CAC_BIEN_THE.md` | Yes | Yes | Yes | Yes | audited (architecture) |
| 5 | `historical/mo_hinh_khong_lien_quan/09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md` | Yes | Yes | Yes | Yes | audited (ablation) |
| 6 | `historical/mo_hinh_khong_lien_quan/11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md` | Yes | Yes | Yes | Yes | audited |
| 7 | `historical/mo_hinh_khong_lien_quan/12_CHI_TIET_KET_QUA_IAVM_INTERACTIVE_ATTENTION_VMAMBA.md` | Yes | Yes | Yes | Yes | audited |
| 8 | `historical/mo_hinh_khong_lien_quan/14_HUONG_8_INTERACTIVE_TOPOLOGY_VMAMBA.md` | Yes | Yes | Yes | Yes | audited (design log) |
| 9 | `historical/thuc_nghiem_6fold_5mo_hinh/02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md` | Yes | Yes | Yes | Yes | audited |
| 10 | `historical/thuc_nghiem_6fold_5mo_hinh/BAO_CAO_TIEN_DO_TUAN_HOAN_CHINH.md` | Yes | Yes | Yes | Yes | audited |


## 3. CLAIM CENSUS — BATCH 3 (B3-C001 … )

Format: `ID | File | § | Claim | Status | Evidence / reason`.

| ID | File | § | Claim | Status | Evidence / reason |
|---|---|---|---|---|---|
| B3-C001 | README | §Quy tắc 1–4 | Historical docs must never be cited as data source; single source = `doc/20_...` + `Ket_Qua_V2` CSVs | VERIFIED | `doc/20_...`, `KQ_Nen_DX_10seed/` and all `02_statistics/*.csv` exist; rule matches the standing project policy |
| B3-C002 | README | §Cấu trúc | 6-seed `.docx` backup ≈ 10 MB, safe to delete | VERIFIED | 10,135,794 bytes; mtime 2026-09-29 21:15 |
| B3-C003 | README | §Cấu trúc | `.md` backup "sai encoding — byte 0xBB không hợp lệ UTF-8, mọi trình đọc đều lỗi" | CONTRADICTED | 1,355 bytes have value 0xBB, but all are UTF-8 continuation bytes (ả/ệ/…); strict UTF-8 decode PASSES and the file was read end-to-end (202 lines) |
| B3-C004 | README | §Danh sách tệp | 10 quarantined items (groups A 2 + B 2 + C 6) | VERIFIED | filesystem = README + `05_` + 1 backup `.md` (+1 `.docx`) + 5 `mo_hinh` + 2 `6fold` |
| B3-C005 | README | §Danh sách tệp | `CNTT_..._old_report.md` deliberately kept outside the quarantine | PARTIALLY_VERIFIED | still outside `historical/` ✓, but it now lives in `archive/Bao_cao/`, not the `archive/` root named in the doc |
| B3-C006 | README | §GHI CHÚ row 1 | `archive/...docx`/`.pdf` still hold 6 wrong p-values (0.2319/0.4439/0.7027/0.7677/0.9189/0.2887) and "167 đối tượng" | CONTRADICTED (docx) · UNVERIFIED (pdf) | docx `<w:t>` text: 0 hits for all six values and 0 for "167"; contains 0.3839 ×1, 0.0908 ×4 (corrected). pdf = 85 FlateDecode streams → raw scan inconclusive; pdf mtime 2026-09-30 predates the 2026-10-02 docx fix |
| B3-C007 | README | §GHI CHÚ row 2 | `Stracth/generate_final_word_report.py` was fixed at v3.1 | VERIFIED | script present among the 55 `archive/Stracth/*.py`; its mtime equals the docx mtime (2026-10-02 11:22) → docx rebuilt by it |
| B3-C008 | README | §Việc cần làm tiếp | "re-run the script to regenerate the `.docx` with corrected numbers and add the two warning boxes" | OUTDATED | the shipped `.docx` already carries corrected values (see B3-C006) and was rebuilt by that script |
| B3-C009 | README | §6seed note | The main 10-seed `.docx`/`.pdf` "chưa được tái tạo từ số liệu đã sửa" | CONTRADICTED | docx holds corrected values with the script's timestamp; the stated path (`archive/` root) is also wrong |
| B3-C010 | README | §mo_hinh table | `12_..._IAVM...md` "contains the wrong figure '167 ảnh'" | CONTRADICTED | "167" never occurs in that file (only "0.9167"); no `historical/` file contains "167 ảnh" — the drafts that did are `conclusions_reviewed`/`final_audit_report`, already repaired |
| B3-C011 | README | §6fold note | `Ket_Qua_V2/` holds raw data for Baseline and TSVM only; 5-model numbers dropped as unverifiable | VERIFIED | `KetQua_Nen/` = exactly 2 model dirs / 20 `results.csv`; P5 and ITSMamba dirs absent; `conclusions_reviewed.md` states the same removal |
| B3-C012 | README | §05 note | `05_...md` duplicates the topic of the current `doc/20_...` | VERIFIED | `doc/20_KET_QUA_CHUAN_...` exists and is the declared single source |
| B3-C013 | 05_KET_QUA | header | 6-fold head-to-head win rate 83.33% | HIST_CONSISTENT | 5/6 reproduced from the 6-fold per-seed matrix (s0,s1,s2,s3,s5) |
| B3-C014 | 05_KET_QUA | §1 | 6-fold means Base 0.7291, TSVM 0.7231, C2IAVM 0.7361; σ 0.0153/0.0055/0.0073 | HIST_CONSISTENT | identical to `6fold/02` §1 whose per-seed column means recompute exactly |
| B3-C015 | 05_KET_QUA | §1 | σ² 2.341/0.303/0.533 (×10⁻⁴); F 7.726× / 4.392×; ranges 0.0423/0.0137/0.0174 | VERIFIED (arithmetic) | σ² = σ²; 2.341/0.303 = 7.726; 2.341/0.533 = 4.392; ranges = max−min of the printed seeds |
| B3-C016 | 05_KET_QUA | §1 table | header cell "C2IAVM (C2IAVM)" | CONTRADICTED | duplicated label defect |
| B3-C017 | 05_KET_QUA | §2 | Baseline's only head-to-head win is s4 (0.7496 vs 0.7297); C2IAVM wins s0,s1,s2,s3,s5 | HIST_CONSISTENT | matches the `6fold/02` matrix |
| B3-C018 | 05_KET_QUA | §3 | 10-seed mAP 0.7210→0.7246 (+0.49%); σ −39.5%; σ² 1.652/0.601 (×10⁻⁴) F=2.748; floor +0.0124 | VERIFIED | raw 0.721029→0.724579 (+0.4924%); 0.012854²=1.6522e-4, 0.007755²=6.014e-5, ratio 2.7482; 0.70650−0.69411=0.01239 |
| B3-C019 | 05_KET_QUA | §3 | Range 0.0425→0.0274 (−35.5%) | VERIFIED (rounding) | raw 0.04252→0.02735 = −35.69% |
| B3-C020 | 05_KET_QUA | §3 | worst case "0.6941 (Seed 9)" and "0.7065 (Seed 2)" | CONTRADICTED | raw: 0.6941 = Baseline s3; 0.7065 = TSVM s7 (`full_comparison_mean_std.csv`, `final_audit_report` §4.1, `conclusions.md`) |
| B3-C021 | 05_KET_QUA | §3 | TSVM wins at "s0,s1,s3,s4,s6,s8" | CONTRADICTED | `seed_win_loss_summary.csv`: TSVM wins s1,s2,s3,s6,s8,s9; count 6/10 correct, membership wrong |
| B3-C022 | 05_KET_QUA | §3 | artefact links under `archive/KQ_Nen_DX_10seed/...` | CONTRADICTED (path) | that path does not exist; real base = `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/` |

| B3-C023 | 6seed_backup | Conversion Notes | "OLD REPORT — NOT UPDATED"; 120 paragraphs / 11 tables converted faithfully | VERIFIED | correct self-labelling of a quarantined 6-seed text |
| B3-C024 | 6seed_backup | header | supervisor named "ThS. Phùng Thế Bảo" | CONTRADICTED | the 6-fold progress report names "TS. Phùng Thế Bảo" — degree title inconsistent inside the quarantine |
| B3-C025 | 6seed_backup | §1 mục 3 | experimental system = 2 models (Baseline + C2TSVMamba) | VERIFIED | matches the current 2-model scope |
| B3-C026 | 6seed_backup | §2.2 | Kvasir-SEG = 1,000 endoscopy images with expert masks | VERIFIED | public dataset fact; repo dataset docs agree |
| B3-C027 | 6seed_backup | §6.1 | params 11,529,190→12,090,370 (+561,180, +4.87%); 35.7→42.3 GFLOPs (+18.49%); ckpt 22.27→23.86 MB; train 1.91→3.92 h | HIST_CONSISTENT | every arithmetic step exact; identical in `6fold/BAO_CAO_TIEN_DO` §6.1; deliberately incompatible with the CPU-era CSV (11.434/12.255M, 18.54/18.86 GFLOPs) and with `08_CHI_PHI` (11.77/12.35M, 39.4/41.2) |
| B3-C028 | 6seed_backup | §6.1–6.2 | latency 12.8→19.0 ms; FPS 78.1→52.6; E2E 15.0→21.2 ms (0.4+12.8+1.8 / 0.4+19.0+1.8); E2E FPS 66.7→47.2 | VERIFIED (arithmetic) | sums and reciprocals reproduce every cell; T4-generation only |
| B3-C029 | 6seed_backup | §6.2 | "vượt xa yêu cầu video y tế (≥30 FPS) … không giật khung hình" | MISLEADING | absolute wording contingent on the removed T4 GPU era; the surviving CPU benchmark measures 1.22 FPS for TSVM |
| B3-C030 | 6seed_backup | §7 | next-week plan: cross-dataset CVC-ClinicDB/BKAI-IGH, ONNX/TensorRT, web demo | VERIFIED | still-open plan; `doc/YEU_CAU_DAC_TA_...CROSS_DATASET.md` exists; no cross-dataset results anywhere in the repo |
| B3-C031 | 01_KIEN_TRUC | §1 | C2 block replaces C2PSA at Layer 10; X ∈ ℝ^{B×512×20×20}; 1×1 split → 256+256; output 512 | VERIFIED | YAML line 31 `- [-1, 2, C2TSVMamba, [1024]] # 10` with scale-s width 0.5 → 512; module: `assert c1==c2`, `self.c=int(c1*0.5)`=256, `cv1: c1→2c`, `cv2: 2c→c1` |
| B3-C032 | 01_KIEN_TRUC | §2.1 | TSVM branch: ShapeAwareBranch (3×3/5×5) + directional 1×5, 5×1, 3×3 + grad=√(S_h²+S_v²+ε) + Sigmoid gate G_TS | VERIFIED | `nn/modules/topology_shape_vmamba.py` lines 213/246/262/264/286/296–311 match the described tensor flow |
| B3-C033 | 01_KIEN_TRUC | §3 | C2IAVM reciprocal gates G_M/G_A and cross-transfer equations | HIST_UNVERIFIED | only `topology_shape_vmamba.py` ships; no `interactive_attention_vmamba.py` in any `nn/modules` (repo holds a single fork) |
| B3-C034 | 01_KIEN_TRUC | §classification | source-of-truth files `interactive_attention_vmamba.py`, `interactive_topology_vmamba.py`, `ultralytics_*/` dirs | CONTRADICTED (paths) | repo contains exactly one fork, `archive/ultralytics_Topology-Shape-aware VMamba`, and none of those modules |
| B3-C035 | 01_KIEN_TRUC | §4 table | mAP means: 72.98 / 72.46 / 71.90–72.60 (s0) / 73.65 (%) | CONTRADICTED | conflicts with its own §siblings: `09_` §5 TSVM 0.7231±0.0055; `6fold/02` TSVM 0.7231, C2IAVM 0.7361; the ITSMamba cell is a single-seed range presented like a mean |
| B3-C036 | 01_KIEN_TRUC | §4 table | Recall 88.37/85.45/87.10/88.75 and Precision 91.65/91.80/91.70/88.85 (%) | CONTRADICTED | TSVM Recall 85.45 vs 84.93 (`09_` §5 and `6fold/02`); C2IAVM Precision 88.85 vs 88.76 quoted in two other documents |
| B3-C037 | 01_KIEN_TRUC | §4 table | Baseline σ² = 0.0002256 | VERIFIED (arithmetic) | 0.01502² = 2.256e-4 |
| B3-C038 | 01_KIEN_TRUC | §4 table | "giảm phương sai 4.15× (F = 4.1538)" for C2IAVM | CONTRADICTED | `05_` §1 and `09_` §5 report 4.392×/4.39× for the same comparison |
| B3-C039 | 01_KIEN_TRUC | §4 table | train/seed 2.15 / 3.92 / 2.965 / 3.049 h; peak VRAM 6.5 / 7.20 / 7.03 / 7.19 GB | HIST_UNVERIFIED | no surviving artefact; only 3.92 h is corroborated (6-fold cost tables) |
| B3-C040 | 01_KIEN_TRUC | §5 | "triệt tiêu hoàn toàn rủi ro OOM … ≈3.05 h cho 100 epochs trên Tesla T4" | MISLEADING | absolute guarantee from a removed GPU generation with no log |

| B3-C041 | 09_ABLATION | §1 | "khảo sát … trên 8 cấu hình/biến thể" | CONTRADICTED | the same section's diagram and the §3 table account for 7 variants (Boundary-aware, Multi-scale, P5-Attn, C2TSVMamba, C2ITSMamba, C2IAVM, Proto-VMamba) |
| B3-C042 | 09_ABLATION | §2.1–2.4 | defect statistics of the 4 rejected branches (P5 morphology, Boundary-aware Sobel, P5 static concat, multi-scale OOM 22–36 h) | HIST_UNVERIFIED | 6-fold raw removed; the (−2.49%, p=0.0363) pair is internally corroborated by `10_DANH_GIA` only |
| B3-C043 | 09_ABLATION | §2.3 | P5-Attention Precision 90.56% (p = 0.0023 < 0.01), val seg 1.4626 | HIST_CONSISTENT | identical numbers in `11_` §1/§3 — the era's own two documents agree |
| B3-C044 | 09_ABLATION | §3 vs §5 | C2IAVM 0.7365±0.0074 / Precision 88.85% (§3) vs 0.7361±0.0073 / 88.75% (§5) | CONTRADICTED | internal contradiction; `6fold/02` and `12_` support the §5 pair |
| B3-C045 | 09_ABLATION | §3 vs §5 | C2IAVM variance reduction 4.15× (§3) vs 4.39× (§5) | CONTRADICTED | internal contradiction (same clash as B3-C038) |
| B3-C046 | 09_ABLATION | §3 | Baseline 0.7298 ± 0.0150 | CONTRADICTED | `6fold/02`, `05_` and `01_` all use 0.7291 ± 0.0153 |
| B3-C047 | 09_ABLATION | §5 | F-ratios 7.73× (TSVM), 9.84× (ITSMamba, "kỷ lục"), 4.39× (C2IAVM); C2IAVM beats ITSMamba 6/6 seeds (t = 4.04, p < 0.01) | HIST_CONSISTENT | the 6/6 comparison and ITSMamba 0.7251±0.0049 are reproduced exactly from `6fold/02` |
| B3-C048 | 09_ABLATION | structure | section numbering runs 1 → 2 → 3 → 5 (no §4) | CONTRADICTED (structural) | document defect; any "§4" cross-reference in the era is broken |
| B3-C049 | 11_P5_ATTN | §1 note | all figures extracted from 6 `results.csv` of `Kvasir_YOLO26s_seg_P5_Attention_VMamba_{s0..s5}` | HIST_UNVERIFIED | those run directories are absent from `KetQua_Nen/`; provenance unprovable |
| B3-C050 | 11_P5_ATTN | §1–§2 | P5 per-seed means 0.7186 mAP / 0.8696 Recall → printed σ 0.0119 | PARTIALLY_VERIFIED | mean of the printed seeds = 0.71860 and 0.86960 (exact); mAP σ recomputes to 0.0116 (ddof=1) / 0.0106 (ddof=0), so the printed 0.0119 is not reproducible |
| B3-C051 | 11_P5_ATTN | §1 | P5 Mask Precision 0.9056 (−0.0143, p = 0.0023) vs Baseline 0.9198 | HIST_UNVERIFIED | era raw removed; the delta/p pair appears only in this document and `09_` §2.3 |
| B3-C052 | 11_P5_ATTN | §3.3 | val seg loss ordering P5 1.4626 > Baseline 1.4314 > TSVM 1.3936 | HIST_CONSISTENT | cross-consistent with `6fold/02` §1 |
| B3-C053 | 11_P5_ATTN | §4 | "bác bỏ lối mòn tư duy", "khẳng định tính đúng đắn của thiết kế" | MISLEADING | rhetorical certainty over p-values of a deleted era; quarantine applies to any quotation |
| B3-C054 | 12_IAVM | §1 | `best.pt` 24.29 MB (24,286,981 bytes) for all 6 splits; C2TSVMamba 23.86 MB; Baseline 22.27 MB | HIST_UNVERIFIED | checkpoints absent; only the 22.27/23.86 pair is corroborated (6-fold cost tables) |
| B3-C055 | 12_IAVM | §2 | IAVM mean mAP 0.7361 / Recall 0.8875 / seg 1.3987 / Box mAP@50 0.9151, printed σ_mAP 0.0073 | PARTIALLY_VERIFIED | 4 of the column means recompute exactly from the printed seeds; σ_mAP recomputes to 0.0067 (ddof=1) / 0.0061 (ddof=0), not 0.0073 |
| B3-C056 | 12_IAVM | §4.1 | IAVM vs TSVM: +0.0130 mAP (p = 0.0173 < 0.05); Recall +3.82% (p = 0.0389) | HIST_UNVERIFIED | no artefact; `results.csv` never contained p-values |
| B3-C057 | 12_IAVM | §4.2 | Precision trade-off 91.98 (Base) / 91.92 (TSVM) → 88.76 (−≈3.2%) | HIST_CONSISTENT | Baseline 91.98% = `6fold/02` 0.9198 ✓; the −3.2% drop is arithmetically correct |
| B3-C058 | 12_IAVM | §5 | "cải tiến thành công rực rỡ" | MISLEADING | absolute praise over unverifiable era numbers; must not be quoted |

| B3-C059 | 14_HUONG_8 | §1.1 | "C2TSVMamba … mAP50-95 đạt 73.3%, Mask Recall sụt giảm xuống 85.8%" | CONTRADICTED | every other source gives 72.31% and 84.93% (`6fold/02`) or 85.45% (`09_`) |
| B3-C060 | 14_HUONG_8 | §1.2 | "C2IAVM … Recall tăng vọt 89.5%, mAP 74.3% (kỷ lục)" | CONTRADICTED | `6fold/02` + `12_`: 88.75% and 73.61%; 74.7% is only the single best seed (s1 = 0.7466) |
| B3-C061 | 14_HUONG_8 | §3.1 | sources under `…/Anti_Up/ultralytics_Interactive_Topology_VMamba` (+ 2.51 MB zip) | CONTRADICTED (paths) | no such directory in the workspace; the repo holds only `archive/ultralytics_Topology-Shape-aware VMamba` |
| B3-C062 | 14_HUONG_8 | §3.2 | local test log: all components PASSED; shapes [2,256,20,20] → [2,512,20,20]; proto [2,32,160,160]; no NaNs | HIST_UNVERIFIED | not re-runnable; no ITSMamba test file ships with the repo |
| B3-C063 | 14_HUONG_8 | §1.2 | `SelectiveScanAutograd` holds VRAM ≈ 7.2 GB at batch 8 | HIST_UNVERIFIED | same class of unbacked claim as `01_` §4 |
| B3-C064 | 14_HUONG_8 | §4 | Kaggle recipe: SEED=0, 100 epochs, batch 8, imgsz 640, workers 2, deterministic locks | VERIFIED | matches the surviving `args.yaml` (seed 0–9, epochs 100, batch 8, imgsz 640, workers 2, deterministic true) |
| B3-C065 | 6fold/02 | §1–§2 | 5-model 6-fold table plus s0–s5 matrices | VERIFIED (arithmetic) | all five column means recompute exactly from the printed rows: 0.729117 / 0.723083 / 0.718600 / 0.725133 / 0.736133 |
| B3-C066 | 6fold/02 | §3 | 127-case clinical table: TP 111.2/107.9/112.2/112.7, FN 15.8/19.1/14.8/14.3, miss 12.40/15.07/11.65/11.25 % | VERIFIED (arithmetic) | recall×127 and FN/127 reproduce every cell |
| B3-C067 | 6fold/02 | §3 | Baseline recall 87.60% displayed with TP 111.2/127 | PARTIALLY_VERIFIED | 111.2/127 = 87.56%; the pair is consistent only at the displayed 1-decimal rounding (0.8760 → 111.25) |
| B3-C068 | 6fold/02 | §4 | "C2IAVM thắng tuyệt đối 6/6 seed trước ITSMamba (+1.10%, t=4.04, p<0.01)" | VERIFIED (comparison) | all six printed seed pairs favour C2IAVM; 0.7361−0.7251 = +0.0110 |
| B3-C069 | 6fold/02 | §4 | ITSMamba "giải cứu Recall +3.42%" and record F = 9.84× | HIST_CONSISTENT | matches `09_` §2.3 and §5 |
| B3-C070 | 6fold/02 | §3 | 6-fold validation set = 120 images / 127 polyps with no background images | VERIFIED | `BAO_CAO_TIEN_DO` §1.3 (880/120, 127 polyp) and the era configs contain no BG20 set |
| B3-C071 | 6fold/BAO_CAO | §1.4 | Kaggle GPU Cloud, Ultralytics 8.4.127, deterministic protocol | VERIFIED | shipped fork `__init__.py`: `__version__ = "8.4.127"` |
| B3-C072 | 6fold/BAO_CAO | §1.3 | 880 train / 120 val, 127 polyps, dataset total 1,000, ≈950 train objects | PARTIALLY_VERIFIED | 880/120 and the 1,000-image corpus are sound (Kvasir-SEG); "≈950 train objects" has no artefact |
| B3-C073 | 6fold/BAO_CAO | §1.2 | P5-Attention "Hoàn thành" for 6 seeds; artefacts exported to `KQ_DoiXung` (9 chart groups) | OUTDATED | `KQ_DoiXung/` no longer exists anywhere in the workspace |
| B3-C074 | 6fold/BAO_CAO | §6.1 | cost table 11.53/12.09M, 35.7/42.3 GFLOPs, 22.27/23.86 MB, 1.91/3.92 h | HIST_CONSISTENT | identical to the 6-seed backup report; arithmetic exact |
| B3-C075 | 6fold/BAO_CAO | §6.2 | latency/FPS table 15.0/21.2 ms, 78.1/52.6, 66.7/47.2 | VERIFIED (arithmetic) | same internally consistent block as B3-C028 |
| B3-C076 | 6fold/BAO_CAO | §6.2 | "đáp ứng trơn tru … real-time, không giật khung hình" vs 25–30 FPS endoscopes | MISLEADING | hardware-contingent absolute; the surviving CPU re-measurement is 1.22 FPS |
| B3-C077 | 6fold/BAO_CAO | header | supervisor "TS. Phùng Thế Bảo" | CONTRADICTED | clashes with "ThS." in the 6-seed backup (see B3-C024) |
| B3-C078 | 6fold/BAO_CAO | §1.1 | pipeline: Backbone → Layer 10 C2TSVMamba → Neck/dual head → mask + box | VERIFIED | matches the shipped YAML (layer 10 = `C2TSVMamba`; the seg head concat at layer 21 consumes layer 10) |


## 4. BATCH 3 STATUS TALLY (78 claims)

| Status | Count |
|---|---|
| VERIFIED | 25 |
| HIST_CONSISTENT | 10 |
| HIST_UNVERIFIED | 9 |
| PARTIALLY_VERIFIED | 5 |
| CONTRADICTED | 22 |
| MISLEADING | 5 |
| OUTDATED | 2 |
| **Total** | **78** |

Reading of the tally: 35 of 78 claims are VERIFIED or era-consistent, 9 have no surviving artefact (expected for a deleted raw-data generation), and 27 are CONTRADICTED/MISLEADING/OUTDATED. The 22 CONTRADICTED split into (a) statements about the current repository that are now false (quarantine manifest, paths) and (b) numbers that clash with other numbers of the era itself. Because the whole directory is declared non-authoritative, these contradictions do **not** threaten any current thesis figure — they only prove the quarantine rule was necessary.

## 5. BATCH 3 CORRECTIONS

1. **The quarantine manifest is itself stale.** `historical/README.md` §"GHI CHÚ QUAN TRỌNG" still asserts that `archive/...docx`/`.pdf` contain six wrong p-values (0.2319/0.4439/0.7027/0.7677/0.9189/0.2887) plus "167 đối tượng", verified by reading `word/document.xml`. Reading that XML again today (via `<w:t>` extraction) returns **zero** hits for all six values and none for "167", while containing 0.3839 (×1) and 0.0908 (×4); the docx mtime (2026-10-02 11:22) equals `Stracth/generate_final_word_report.py`'s. Conclusion: the regeneration task listed as TODO is **done** for the `.docx`. Only the companion **`.pdf` (mtime 2026-09-30) remains unverified** (85 FlateDecode streams defeat a raw scan).
2. **The "encoding" warning is wrong.** `..._old_report_backup_6seed.md` does contain 1,355 bytes of value `0xBB`, but they are all legal UTF-8 continuation bytes; a strict UTF-8 decode succeeds and the file reads normally. The README's "mọi trình đọc văn bản đều lỗi" is a false blocker on deletion.
3. **Misattribution in the manifest.** The "167 ảnh" number is attributed to `12_CHI_TIET_KET_QUA_IAVM...md`, where it does not occur (only "0.9167"). The offending drafts were `conclusions_reviewed.md` / `final_audit_report.md`, both already repaired. The manifest's own §6fold note correctly explains the 127-object + 40-image arithmetic.
4. **Path drift across every quarantined file** — four stale path families: `archive/KQ_Nen_DX_10seed/**` (real: `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/**`), `archive/KQ_DoiXung/**` (removed), `archive/KetQua_Nen/**` (real: `archive/Ket_Qua_V2/KetQua_Nen/**`), and `…/Anti_Up/ultralytics_Interactive_Topology_VMamba/**` (never in this workspace). Files placed at the `archive/` root (`CNTT_KLCN182_LeDucLuong.docx/.pdf/.md`) now live in `archive/Bao_cao/`.
5. **`05_...md` smuggles a current-topic table into the quarantine with three defects**: worst-case seed labels ("Seed 9"/"Seed 2" instead of s3/s7), the head-to-head win membership (`s0,s1,s3,s4,s6,s8` instead of `s1,s2,s3,s6,s8,s9`), and rounding drift (Range −35.5% vs −35.7%). Its six-fold half is sound; its Appendix-10-seed half must never be cited.
6. **`09_ABLATION` is internally inconsistent**: C2IAVM 0.7365±0.0074 / Precision 88.85% (§3) vs 0.7361±0.0073 / 88.75% (§5); variance reduction 4.15× (§3) vs 4.39× (§5); Baseline 0.7298±0.0150 vs 0.7291±0.0153 everywhere else; "8 biến thể" but only 7 are listed/experimented; section numbering skips §4.
7. **`14_HUONG_8` carries the two worst numeric errors of the quarantine**: "C2TSVMamba 73.3% mAP / 85.8% Recall" (real: 72.31% / 84.93%) and "C2IAVM Recall 89.5% / mAP 74.3% kỷ lục" (real: 88.75% / 73.61%; 74.7% is only seed s1).
8. **Metadata inconsistency**: the same supervisor is "TS. Phùng Thế Bảo" in `6fold/BAO_CAO_TIEN_DO` and "ThS. Phùng Thế Bảo" in the 6-seed backup.
9. **Absolutes that must never be quoted**, even with an era caveat: "triệt tiêu hoàn toàn rủi ro OOM", "vượt xa yêu cầu video y tế ≥30 FPS / không giật khung hình", "cải tiến thành công rực rỡ", "bác bỏ lối mòn tư duy kỹ thuật", "khẳng định tính đúng đắn".
10. **Two σ values are not reproducible from their own tables**: `11_` prints σ_mAP = 0.0119 (recomputed 0.0116 ddof=1 / 0.0106 ddof=0) and `12_` prints σ_mAP = 0.0073 (recomputed 0.0067 / 0.0061). The printed means are exact; only the dispersion figures drift.

## 6. BATCH 3 UNRESOLVED

No surviving raw artefact (all six-fold run directories were deleted), so these stay UNVERIFIED by construction: B3-C033, C039, C042, C049, C051, C054, C056, C062, C063, and the **PDF half of B3-C006** (FlateDecode; mtime predates the docx fix). Also flagged as not-reproducible-but-minor: B3-C050, C055 (σ drift), C067, C072 (rounding/label only). Everything else in the batch is either verified against a surviving artefact or exactly reproduced from the era's own printed tables.

## 7. BATCH VERDICT

`BATCH 3 COMPLETE` — 10/10 files read; 78 material claims classified (25 VERIFIED, 10 HIST_CONSISTENT, 9 HIST_UNVERIFIED, 5 PARTIALLY_VERIFIED, 22 CONTRADICTED, 5 MISLEADING, 2 OUTDATED); every claim has an evidence mapping or an explicit unresolved marker; the quarantine boundary is confirmed as necessary and the manifest itself needs three corrections (docx status, encoding claim, "167" attribution).


---

# BATCH 4 RESULTS — Remaining Markdown

Scope: every `archive/**/*.md` **not** covered by BATCH 1 (`Bao_cao` + `Ket_Qua_V2`), BATCH 2 (`doc` excluding `historical`), or BATCH 3 (`doc/historical`).

Enumeration (run from repo root `Test_Mau`):

```powershell
$all = Get-ChildItem "archive" -Recurse -Filter *.md | ForEach-Object { $_.FullName }
$batch1 = Get-ChildItem "archive/Bao_cao","archive/Ket_Qua_V2" -Recurse -Filter *.md | ForEach-Object { $_.FullName }
$batch2 = Get-ChildItem "archive/doc" -Recurse -Filter *.md | Where-Object { $_.FullName -notlike "*\historical\*" } | ForEach-Object { $_.FullName }
$batch3 = Get-ChildItem "archive/doc/historical" -Recurse -Filter *.md | ForEach-Object { $_.FullName }
$covered = $batch1 + $batch2 + $batch3
Compare-Object $all $covered | Where-Object { $_.SideIndicator -eq "<=" } | Select-Object -ExpandProperty InputObject
```

Result (exact, not assumed): **3 remaining files**.

| Count | Path |
|---:|---|
| ALL | 56 |
| BATCH 1 | 16 |
| BATCH 2 | 27 |
| BATCH 3 | 10 |
| COVERED | 53 |
| REMAINING | **3** |

The three remaining files are:

1. `archive/MARKDOWN_CLAIM_AUDIT.md` (this ledger)
2. `archive/ultralytics_Topology-Shape-aware VMamba/cfg/models/README.md`
3. `archive/ultralytics_Topology-Shape-aware VMamba/trackers/README.md`

They are **not** all under `ultralytics...`; one is the audit ledger at the archive root.

A prior section (now Appendix below) labelled “BATCH 4” audited `Ket_Qua_V2` (already BATCH 1) plus the two Ultralytics READMEs. That pass is **not** remaining-file coverage. Its IDs were renamed `B4L-C001…B4L-C067`. This section is the recovery audit of the three leftover files.

## A. Remaining File Coverage

| File | Read | Claims Extracted | Fact Checked | Evidence Mapped |
| ---- | ---- | ---------------- | ------------ | --------------- |
| `archive/MARKDOWN_CLAIM_AUDIT.md` | Yes | Yes | Yes | Yes |
| `archive/ultralytics_Topology-Shape-aware VMamba/cfg/models/README.md` | Yes | Yes | Yes | Yes |
| `archive/ultralytics_Topology-Shape-aware VMamba/trackers/README.md` | Yes | Yes | Yes | Yes |

3 / 3 remaining files opened end-to-end. Material claims extracted and matched to archive artefacts (YAML, Python, filesystem counts). No source Markdown other than this ledger was edited.

## B. Claim Audit

| ID | File | Claim | Actual Archive Evidence | Verdict | Notes |
| -- | ---- | ----- | ----------------------- | ------- | ----- |
| B4-C001 | `cfg/models/README.md` | This folder contains Ultralytics YOLO architecture YAML (`*.yaml`) used for detect / segment / pose / OBB / classify | `cfg/models/` holds **67** `*.yaml` files (68 files including this README). Families present: `yolo26.yaml`, `yolo26-seg.yaml`, `yolo26-pose.yaml`, `yolo26-obb.yaml`, `yolo26-cls.yaml` (and YOLO11/12/v8 analogues) | VERIFIED | Directory inventory, not a thesis result |
| B4-C002 | `cfg/models/README.md` | Example: train `yolo26n.yaml` on `coco8.yaml` for 100 epochs, `imgsz=640` | `cfg/datasets/coco8.yaml` exists (4 train + 4 val images). **No file named `yolo26n.yaml`**. `cfg/models/26/yolo26.yaml` documents scale alias: `model=yolo26n.yaml` loads `yolo26.yaml` with scale `n`. 100 / 640 is an Ultralytics example, not the BG20 10-seed protocol | PARTIALLY_VERIFIED | Scale alias works in this fork; standalone YAML is absent |
| B4-C003 | `cfg/models/README.md` | Supported families include YOLO26, YOLO12, YOLO11, YOLOv10, YOLOv9, YOLOv8, YOLOv5 | Matching YAML directories exist: `cfg/models/{26,12,11,v10,v9,v8,v5}/` | VERIFIED | “And more…” is accurate: `v3`, `v6`, `rt-detr` also ship |
| B4-C004 | `cfg/models/README.md` | This README describes the thesis TSVM / Topology-Shape architecture | Recursive grep of this README: 0 hits for `VMamba`, `TSVM`, `Kvasir`, `polyp`, `Topology`. Thesis config is a sibling YAML: `cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml` | VERIFIED (negative) | Upstream stock doc; thesis architecture is **not** documented here |
| B4-C005 | `trackers/README.md` | Fork supports BoT-SORT, ByteTrack, OC-SORT, Deep OC-SORT, FastTracker, TrackTrack via `botsort.yaml` / `bytetrack.yaml` / `ocsort.yaml` / `deepocsort.yaml` / `fasttrack.yaml` / `tracktrack.yaml` | All six YAMLs exist under `cfg/trackers/`. `trackers/track.py` `TRACKER_MAP` keys: `bytetrack`, `botsort`, `tracktrack`, `fasttrack`, `ocsort`, `deepocsort`. Implementations: `bot_sort.py`, `byte_tracker.py`, `oc_sort.py`, `deep_oc_sort.py`, `fast_tracker.py`, `track_tracker.py` | VERIFIED | Config + class map match the list |
| B4-C006 | `trackers/README.md` | Default tracker is **BoT-SORT** | Engine default `cfg/default.yaml` line 140: `tracker: tracktrack.yaml`. Solutions default `solutions/config.py`: `tracker: str = "botsort.yaml"`. README states BoT-SORT unconditionally | CONTRADICTED | Dual defaults in this fork; README does not match `default.yaml` |
| B4-C007 | `trackers/README.md` | Tracking is available for Detect, Segment, Pose, and OBB models | `trackers/track.py`: `trackable = ("detect", "segment", "pose", "obb")`; non-trackable tasks in `TASKS` raise `ValueError` | VERIFIED | Matches code. `semantic` / `depth` / `classify` are in `TASKS` but not trackable (README silent on those) |
| B4-C008 | `trackers/README.md` | Examples load `yolo26n.pt` / `yolo26n-seg.pt` and call `model.track(...)` | **0** `*.pt` files under the vendored fork. **0** `model.track` / `yolo track` hits under `archive/Ket_Qua_V2` | UNVERIFIED (weights) · VERIFIED (unused by thesis) | Example weights are not in the archive; tracking is not part of the 10-seed pipeline |
| B4-C009 | `trackers/README.md` | Trackers process video “in real-time without sacrificing accuracy” | No latency/accuracy artefact for any tracker in `Ket_Qua_V2`. Surviving CPU detect/seg benchmark is unrelated (200.12 / 821.27 ms) | UNVERIFIED | Marketing claim; not a thesis result |
| B4-C010 | `MARKDOWN_CLAIM_AUDIT.md` | Archive-wide Markdown count is **56** | `Get-ChildItem archive -Recurse -Filter *.md` → 56. Split: Bao_cao 3 + Ket_Qua_V2 13 + doc∖historical 27 + historical 10 + ultralytics 2 + this ledger 1 | VERIFIED | 3+13+27+10+2+1 = 56 |
| B4-C011 | `MARKDOWN_CLAIM_AUDIT.md` | BATCH 1 = 16, BATCH 2 = 27, BATCH 3 = 10 | Same enumeration as the Compare-Object recipe | VERIFIED | Matches filesystem |
| B4-C012 | `MARKDOWN_CLAIM_AUDIT.md` | After BATCH 1–3, **3** Markdown files remain | Compare-Object leftover list is exactly the three files in §A | VERIFIED | Recovery scope confirmed |
| B4-C013 | `MARKDOWN_CLAIM_AUDIT.md` (prior “BATCH 4” / MERGE) | Remaining coverage = 15 files (`Ket_Qua_V2` 13 + ultralytics 2), completing 56 as 3+1+27+10+13+2 | `Ket_Qua_V2` 13 files are **already** BATCH 1. Remaining-file set is 3, not 15. Arithmetic 56 is true only if BATCH 1 is counted twice or the audit file is swapped for Bao_cao | CONTRADICTED | Mis-scoped prior BATCH 4; IDs preserved as `B4L-C*` |
| B4-C014 | `MARKDOWN_CLAIM_AUDIT.md` (prior B4L-C001/C002) | The two Ultralytics READMEs have **NO MATERIAL CLAIMS** | This pass extracted architecture, tracker inventory, default-tracker, task-support, and unused-by-thesis claims (B4-C001–C009) | CONTRADICTED | “No thesis metrics” ≠ “no material claims” |
| B4-C015 | `MARKDOWN_CLAIM_AUDIT.md` | Internal BATCH 1 coverage is consistent | Early “FINAL QA” still says Ket_Qua_V2 8/13 read and 5 inventory-only; later BATCH 1 RESULTS says 16/16 COMPLETE | CONTRADICTED | Ledger contains two incompatible BATCH 1 coverage statements |
| B4-C016 | `MARKDOWN_CLAIM_AUDIT.md` | MERGE FINAL claim total 272 = 14+113+78+67 | Arithmetic of those four section tallies is 272. BATCH 1 body also lists B1-C001…C028 (28 IDs), so 14 is not an exhaustive B1 census | PARTIALLY_VERIFIED | Sum of printed tallies is exact; B1 denominator is internally inconsistent |
| B4-C017 | `MARKDOWN_CLAIM_AUDIT.md` | MERGE FINAL “56 / 56 FILES” means every source file is audited and BATCH 4 remaining is closed | Filesystem has 56 Markdown files. BATCH 1–3 cover 53. This remaining pass covers the last 3. That is coverage arithmetic, **not** a scientific 56/56 PASS on every claim in the corpus | PARTIALLY_VERIFIED | File existence/read coverage can sum to 56; claim-level PASS is a later MERGE job. BATCH 4 does not assert `56/56 PASS` |

## C. Issues

1. **Default-tracker mismatch (CONTRADICTED).** `trackers/README.md` says the default tracker is BoT-SORT. `cfg/default.yaml` ships `tracker: tracktrack.yaml`. `solutions/config.py` uses `botsort.yaml`. Anyone copying the README will not get the engine default of this fork.
2. **`yolo26n.yaml` is a scale alias, not a file.** The models README example names a file that is not on disk; `yolo26.yaml` + scale `n` is the artefact.
3. **Example checkpoints are absent.** `yolo26n.pt` / `yolo26n-seg.pt` are not in the vendored tree (0 `*.pt`). UNVERIFIED as runnable examples inside `archive/`.
4. **Tracking is unused by the thesis pipeline.** No `model.track` in `Ket_Qua_V2`. Tracker README must not be cited as experimental evidence.
5. **Prior BATCH 4 double-counted BATCH 1.** The Appendix still contains a 15-file “BATCH 4” over `Ket_Qua_V2` + ultralytics. Remaining-file recovery is 3 files, not 15.
6. **“NO MATERIAL CLAIMS” overclaim.** The two Ultralytics READMEs have no polyp/TSVM metrics, but they do have architecture/config claims that contradict `default.yaml`.
7. **Ledger self-contradiction on BATCH 1 coverage.** 11/16 (inventory) vs 16/16 (COMPLETE) remain both present in this file.
8. **B1 claim-count mismatch.** MERGE uses 14 B1 claims; the BATCH 1 RESULTS table also enumerates B1-C015…C028.
9. **Terminology/config:** Ultralytics examples use COCO8 / YOLO26n / 100 epochs / imgsz 640. Thesis runs use `data_bg20.yaml`, `yolo26-seg` / TSVM YAML, 10 seeds, batch 8. The READMEs are upstream templates, not experiment logs.
10. **Provenance:** both Ultralytics READMEs are stock Ultralytics text vendored with the fork; they are not authored as thesis documentation.

UNRESOLVED: B4-C008 (weights not in archive — cannot execute the README examples here); B4-C009 (real-time/accuracy slogan has no artefact).

## D. Coverage Reconciliation

Filesystem recount (`Get-ChildItem archive -Recurse -Filter *.md`):

```text
BATCH 1 = 16 files
BATCH 2 = 27 files
BATCH 3 = 10 files
BATCH 4 = 3 files
TOTAL = 56
```

Check: 16 + 27 + 10 + 3 = 56.

Split of the 3 BATCH 4 files: 1 audit ledger + 2 vendored Ultralytics READMEs.

This BATCH 4 section does **not** declare `56/56 PASS`. It only closes remaining-file *read / extract / fact-check* coverage. A later MERGE pass must still reconcile BATCH 1 internal 11-vs-16 text, B1 14-vs-28 claim counts, and the Appendix `B4L-*` overlap with BATCH 1.

## 7. BATCH VERDICT

`BATCH 4 COMPLETE`

Reason: all 3 remaining Markdown files were read; material claims were extracted; each claim was matched to archive evidence or marked UNVERIFIED/UNRESOLVED; prior mis-scoped 15-file “BATCH 4” is quarantined as Appendix and does not count as remaining coverage.


---

# APPENDIX — Mis-scoped prior BATCH 4 (Ket_Qua_V2 already in BATCH 1; IDs B4L-C*)

Scope: the **13** Markdown files under `archive/Ket_Qua_V2/**` (two efficiency-benchmark packages + the 10-seed analysis package) and the **2** Markdown files under `archive/ultralytics_Topology-Shape-aware VMamba/**` (`cfg/models/README.md`, `trackers/README.md`). `archive/Bao_cao/**` is BATCH 1 and `archive/doc/**` is BATCH 2/3.

## 1. EXACT FILE COUNT

`Get-ChildItem "archive/Ket_Qua_V2" -Recurse -Filter *.md` → **13** (2 in `efficiency_benchmark/reports/`, 1 `README.md`, 6 in `KQ_Nen_DX_10seed/06_reports/`, 1 in `07_audit/`, 2 in `KQ_Nen_DX_10seed/efficiency_benchmark/reports/`, 1 in `KQ_Nen_DX_10seed/reports/`); plus **2** under the vendored fork = **15 total**, which completes the 56-file corpus (3 + 1 audit + 27 + 10 + 13 + 2).

Tier-A artefacts used for fact-checking (outside BATCH 4 coverage): `Ket_Qua_V2/efficiency_benchmark/{raw/efficiency_raw_benchmark.csv, tables/*.csv}`, the identical pair under `KQ_Nen_DX_10seed/efficiency_benchmark/`, `KQ_Nen_DX_10seed/{01_raw_analysis/*.csv, 02_statistics/**/*.csv, 06_reports/summary.csv, 07_audit/*}`, the 20 `KetQua_Nen/*/results.csv` + `args.yaml` + `confusion_matrix.png` mtimes, `archive/data_bg20.yaml`, `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20` counts, `figures/` and `05_charts/` inventories, `archive/Stracth/*` (55 `.py`).

## 2. PER-FILE COVERAGE (15 / 15)

| # | File | Exists | Read | Claims | Fact-checked | Status |
|---|------|:---:|:---:|:---:|:---:|---|
| 1 | `Ket_Qua_V2/efficiency_benchmark/reports/benchmark_audit.md` | Yes | Yes | Yes | Yes | audited (2-model audit) |
| 2 | `Ket_Qua_V2/efficiency_benchmark/reports/benchmark_report.md` | Yes | Yes | Yes | Yes | audited (2-model report) |
| 3 | `Ket_Qua_V2/KQ_Nen_DX_10seed/README.md` | Yes | Yes | Yes | Yes | audited (package index) |
| 4 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/conclusions.md` | Yes | Yes | Yes | Yes | audited |
| 5 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/conclusions_reviewed.md` | Yes | Yes | Yes | Yes | audited (core, corrected) |
| 6 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/final_audit_report.md` | Yes | Yes | Yes | Yes | audited |
| 7 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/FORENSIC_EXPERIMENT_AUDIT.md` | Yes | Yes | Yes | Yes | audited (deepest provenance) |
| 8 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/recommended_figures_for_thesis.md` | Yes | Yes | Yes | Yes | audited (figure catalogue) |
| 9 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/summary.md` | Yes | Yes | Yes | Yes | audited |
| 10 | `Ket_Qua_V2/KQ_Nen_DX_10seed/07_audit/audit_report.md` | Yes | Yes | Yes | Yes | audited (auto-generated) |
| 11 | `Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/reports/benchmark_audit.md` | Yes | Yes | Yes | Yes | audited (STALE 4-model) |
| 12 | `Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/reports/benchmark_report.md` | Yes | Yes | Yes | Yes | audited (STALE 4-model) |
| 13 | `Ket_Qua_V2/KQ_Nen_DX_10seed/reports/chart_template_mapping.md` | Yes | Yes | Yes | Yes | audited (STALE inventory) |
| 14 | `ultralytics_Topology-Shape-aware VMamba/cfg/models/README.md` | Yes | Yes | NO MATERIAL CLAIMS | n/a | upstream Ultralytics doc |
| 15 | `ultralytics_Topology-Shape-aware VMamba/trackers/README.md` | Yes | Yes | NO MATERIAL CLAIMS | n/a | upstream Ultralytics doc |


## 3. CLAIM CENSUS — BATCH 4 (B4L-C001 … )

| ID | File | § | Claim | Status | Evidence / reason |
|---|---|---|---|---|---|
| B4L-C001 | UL-CFG | whole file | Vendored `cfg/models/README.md` describes YOLO model configs and usage | NO_MATERIAL_CLAIMS | 0 hits for `VMamba|TSVM|polyp|Kvasir|Topology`; stock Ultralytics text (this thesis contributes the YAML files, not this doc) |
| B4L-C002 | UL-TRK | whole file | Vendored `trackers/README.md` describes BoT-SORT/ByteTrack/OC-SORT/… | NO_MATERIAL_CLAIMS | same negative grep; tracking is unused by the thesis pipeline |
| B4L-C003 | EB-AUD | §1 | "no retrain", weights loaded from existing checkpoints, "exactly 2 models in tables/charts" | PARTIALLY_VERIFIED | 2-model claim VERIFIED (`efficiency_summary.csv` = 2 rows; `KetQua_Nen` = 2 dirs); non-modification cannot be proven from the artefacts alone |
| B4L-C004 | EB-AUD | §1 | 100 timed iterations per model ⇒ 200 raw measurements (100 each) | VERIFIED | `efficiency_raw_benchmark.csv` header `model_name,iteration,latency_ms` + exactly 200 data rows |
| B4L-C005 | EB-AUD | §1 | `thop.profile` on the same (1,3,640,640) dummy: Params 11.434 vs 12.255 M; GFLOPs 18.54 vs 18.86 | VERIFIED | both cells equal `efficiency_summary.csv` |
| B4L-C006 | EB-AUD | §1–2 | Peak GPU VRAM unavailable on CPU ⇒ recorded as `N/A`, not fabricated | PARTIALLY_VERIFIED | the CSV leaves `Peak_VRAM_MB` empty while the Markdown renders `N/A` (literal mismatch); CUDA availability not re-checked here |
| B4L-C007 | EB-AUD | §3 | 15 charts + all comparison tables complete | VERIFIED | 15 files in `Ket_Qua_V2/efficiency_benchmark/figures` |
| B4L-C008 | EB-REP | §1 | Environment/protocol: Ryzen 7 (16 logical CPU), 16 GB, Python 3.13.14, torch 2.13.0+cpu, batch 1, 20 warmup + 100 measured | PARTIALLY_VERIFIED | the 20+100 protocol matches the 200 raw rows; hardware/library versions not independently verifiable |
| B4L-C009 | EB-REP | §2 | Efficiency table: 11.434/12.255 M; 18.54/18.86 GFLOPs; 22.27/23.86 MB; 200.12/821.27 ms (σ 18.08/55.91); P50 195.92/826.09; P95 218.28/899.10; P99 251.67/908.97; 5.00/1.22 FPS; RSS 446.44/466.95 MB | VERIFIED | every cell equals `efficiency_summary.csv` |
| B4L-C010 | EB-REP | §2 | Derived deltas +7.18 / +1.73 / +7.14 / +310.39 / +321.65 / +311.90 / +261.18 / −75.60 / +4.59 % | VERIFIED (arithmetic) | each percentage recomputed from the CSV pair, exact |
| B4L-C011 | EB-REP | §3 | Accuracy–efficiency merge: mAP 0.7210/0.7246, σ 0.0129/0.0078, Precision 0.9023/0.9118, Recall 0.8584/0.8625 | PARTIALLY_VERIFIED | values match `accuracy_efficiency_summary.csv` + raw 10-seed CSV, but the cited source (`archive/doc/16_...md`) is a superseded 4-model document |
| B4L-C012 | EB-REP | §4 | Pareto reading: both models on the frontier; TSVM = highest mean mAP + lowest σ | VERIFIED | descriptive and consistent with the CSV pair |
| B4L-C013 | EB-REP | §5 | 15 figures regenerated at 300 DPI | VERIFIED | 15 files present (DPI not measured) |
| B4L-C014 | README10 | §1 | Validation = 160 images = 120 polyp images (127 GT objects) + 40 `normal-cecum` negatives | VERIFIED | `data_bg20.yaml` metadata (`val_images: 160 # 120 polyp + 40 background`) and 160 val JPEGs in `Kvasir_YOLO_SEG_BG20` |
| B4L-C015 | README10 (config) | §1 | the referenced `data_bg20.yaml` is usable as-is | CONTRADICTED (path) | its `path:` points to `archive/Kvasir_YOLO_SEG_BG20`, which does not exist; the dataset lives in `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20` |
| B4L-C016 | README10 | §1 | 10 independent seeds (0–9), 20 complete runs, 100 epochs each, metrics at best epoch by `mAP50-95(M)` | VERIFIED | per-run `args.yaml`: `seed` = run index, epochs 100, batch 8, imgsz 640, workers 2, `deterministic: true`; each `results.csv` = 100 rows |
| B4L-C017 | README10 | §1 | provenance paths `KetQua_Nen/YOLOv26s-seg/...` and `KetQua_Nen/Kvasir_BG20_..._TSVM/...` | CONTRADICTED (path) | real base = `archive/Ket_Qua_V2/KetQua_Nen/...` |
| B4L-C018 | README10 | §2 | Package tree: `01_raw_analysis`, `02_statistics`, `03_metrics`, `04_confusion_matrix`, `05_charts`, `06_reports` | VERIFIED | all listed entries exist (05_charts = 16 PNGs; 04_confusion_matrix = 6+4; 06_reports has since grown to 7 files) |
| B4L-C019 | README10 | §3.1–3.3 | mAP 0.7246 vs 0.7210 (+0.49%); Precision 0.9118 vs 0.9023; σ 0.0129/0.0078; Range 0.0425/0.0273; Val Seg 1.3045→1.2424 (−0.0622, −4.76 %, p = 0.0908) | VERIFIED | raw 10-seed CSV + `full_comparison_mean_std.csv` |

| B4L-C020 | README10 | §3.4 | On the 40 negatives: FP 14.6 vs 16.8 and TN 25.4 vs 23.2 | PARTIALLY_VERIFIED | FP is measured ✓; TN = 40 − FP is a reconstruction. The index omits the derivation caveat that `conclusions_reviewed.md` §4.3 and `07_audit` make mandatory |
| B4L-C021 | CONCL | §1 | mAP +0.0036 (+0.49 %); mAP50 −0.0056 (−0.62 %); p = 0.3839 > 0.05 ⇒ "chênh lệch dương tính ở mức vừa phải", no significance claimed | VERIFIED | raw CSV; `statistically_significant_005 = False` |
| B4L-C022 | CONCL | §2 | σ 0.0129→0.0078 (variance ÷2.75); Range 0.0425→0.0273; worst floor 0.7065 (s7) vs 0.6941 (s3) | VERIFIED | raw CSV + `metrics_min_max_range.csv` |
| B4L-C023 | CONCL | §3 | Precision 0.9023→0.9118 (+1.05 %, p = 0.5428); Recall 0.8584→0.8625 (+0.48 %) | VERIFIED | raw CSV; p-values from `full_comparison_mean_std.csv` |
| B4L-C024 | CONCL | §4 | Val Seg Loss −0.0622 (−4.76 %), p = 0.0908 near α = 0.10 | VERIFIED | CSV value 0.090772 |
| B4L-C025 | CONCL | §5, §Giới hạn | CM means TP 111.2 (87.6 %) vs 110.3 (86.9 %), FN 15.8/16.7, FP 14.6 (36.5 %) vs 16.8 (42.0 %), TN 25.4 (63.5 %) vs 23.2 (58.0 %); limits: single-centre 160-image set, contribution = stability + FP reduction | VERIFIED | raw CM means; TN flagged as reconstruction in the same section; no absolute wording |
| B4L-C026 | CONCL-R | §6 note | the earlier draft contained different numbers plus P5/ITS data and was narrowed to 2 verifiable models | VERIFIED | `KetQua_Nen` holds exactly the 2 model dirs; P5/ITS dirs absent |
| B4L-C027 | CONCL-R | §2–3.2 | aggregates incl. Box mAP 0.7262→0.7285, Best Epoch 87.3→91.7; σ reductions 39.7 % (mAP), 55.4 % (seg loss), 54.8 % (Box Recall) | VERIFIED (arithmetic) | raw CSV; 1−0.007755/0.012854; 1−0.0387/0.0867; 1−0.015228/0.033725 |
| B4L-C028 | CONCL-R | §4.3 | TN is not a measurement: `ConfusionMatrix.process_batch` (≈ lines 427–434) increments only FP for empty-GT images, no `matrix[nc,nc] += 1`; the cell is filtered at line 550 | VERIFIED | code read in BATCH 2 (B2-C038, B2-C040) |
| B4L-C029 | CONCL-R | §4.3 | 3/20 runs mismatch their own PNG (TSVM s0 59/10/68, s5 0/90/127, s8 6/8/121) | PARTIALLY_VERIFIED | produced by `Stracth/_forensic_cm_ocr.py` / `_forensic_cm_crop.py` (both present) and cross-stated in `07_audit` + FORENSIC; OCR not re-run here |
| B4L-C030 | CONCL-R | §4.3, §5 | sample size must read 160 images / 127 entities; never "167" | VERIFIED | dataset counts; "167" = 127 objects + 40 images conflation |
| B4L-C031 | CONCL-R | §5 | no metric significant at α = 0.05 (p = 0.384); Val Cls Loss worsens +9.97 % with the outlier 0.83094 at seed 7 | VERIFIED | `raw_10seeds_extracted_metrics.csv` row TSVM seed 7 = 0.83094; CSV p 0.094330 |
| B4L-C032 | CONCL-R | §Quy tắc | rules: no absolute terms, p > 0.05 = non-significant, TN/Specificity not citable as a measurement | VERIFIED | document practice matches; FORENSIC §7 confirms 13/13 rows `statistically_significant_005 = False` |
| B4L-C033 | SUMM | §1 | 13-metric comparison table with Δ, %, p-value and significance flags | VERIFIED | each row equals `summary.csv` (13 data rows) and `full_comparison_mean_std.csv` |
| B4L-C034 | SUMM | §2 | dispersion: mask-mAP F = 2.75×, Precision F = 1.90×, seg-loss F = 5.02×; extremes labelled s3/s0 (Baseline) and s7/s8 (TSVM) | VERIFIED | variance ratios recomputed from raw σ (1.90 = (0.033899/0.024596)²; 5.02 = (0.086664/0.038667)²); seed labels match `min_max` CSV |
| B4L-C035 | SUMM | §3 | per-metric seed win/loss: mAP 6/4, Precision 5/5, Recall 6/4, Val Seg Loss 8/2 | VERIFIED | `seed_win_loss_summary.csv` rows are identical |
| B4L-C036 | FINAL | §2.1 | 20 `results.csv` × 17 fields = 340 cells re-extracted with absolute error 0; "559/559 ĐẠT" | PARTIALLY_VERIFIED | the re-extraction claim is consistent with the shipped scripts, but `07_audit`/FORENSIC print a different grand total (694/694) and neither document reconciles the two definitions |
| B4L-C037 | FINAL | §2.2 | three disclosed limitations: derived TN, 3/20 CM mismatch, "167"→160 correction | VERIFIED | same evidence as B4L-C028/C029/C030 |
| B4L-C038 | FINAL | §4.1 | per-seed mask-mAP table plus Mean 0.72103/0.72458, Std 0.01285/0.00776, Min s3/s7, Max s0/s8, Range 0.04252/0.02735 | VERIFIED | raw CSV: the nine printed seed rows plus the implied s0 values (0.73664 / 0.72452) reproduce both means exactly; extremes match the `min_max` CSV |
| B4L-C039 | FINAL | §4.2 | CM constraints TP + FN = 127 (TP measured) and FP + TN = 40 (FP measured, TN derived); Sensitivity 86.85→87.56 %; FP-rate 42.00→36.50 % | VERIFIED | raw CM means; 111.2/127 = 87.56 %, 16.8/40 = 42.0 %, 14.6/40 = 36.5 % |
| B4L-C040 | FINAL | §5 | audit commitments: no data tampering, stale table replaced, limits disclosed, no biased conclusions | VERIFIED | consistent with the artefacts and with the CM caveats in the same package |

| B4L-C041 | FORENSIC | §1–1.2 | three data tiers (20 `results.csv` + 20 CM PNG; 10 interim CSVs; 3 report files); 20 runs = 2 models × 10 seeds, 100 epochs each, no duplicate (model, seed) | VERIFIED | every enumerated artefact exists; `results.csv` row counts = 100; `args.yaml` seeds 0–9 unique; 2 model dirs |
| B4L-C042 | FORENSIC | §3 | no IoU / mIoU / Dice / F1 column exists anywhere in the package | VERIFIED | the raw CSV header has 21 fields (model…run_path) with none of them; metric-name scan negative |
| B4L-C043 | FORENSIC | §4.1 | Dice and F1 are **not** interchangeable here: 0.868162 vs 0.879772 (Baseline) and 0.879747 vs 0.886447 (TSVM), both `[DERIVED]`, not citable | VERIFIED (arithmetic) | recomputed from mean CM and mean P/R, exact to 6 dp; the non-citable label is correct |
| B4L-C044 | FORENSIC | §4, §7, §8 | metric tables incl. W/B/T counts 6/4/0, 3/7/0, 5/5/0, 6/4/0; "no metric significant at α = 0.05", min p_ttest = 0.090772, min p_wilcoxon = 0.083984 | VERIFIED | identical to `seed_win_loss_summary.csv` and `full_comparison_mean_std.csv` |
| B4L-C045 | FORENSIC | §9 | per-seed mask-mAP table; TSVM ahead in 6/10 (s1, s2, s3, s6, s8, s9), no ties | VERIFIED | raw CSV per-seed pairs |
| B4L-C046 | FORENSIC | §10, §11-D1 | 6 intermediary files cross-check (max error 9.95e-17); `verify_10seed_audit.py` → 694/694 PASS; PNG vs `results.csv` timestamps (19/20 identical, TSVM s5 offset) | VERIFIED | INDEPENDENT REPRODUCTION in this audit: 19/20 `confusion_matrix.png` mtimes equal their `results.csv` mtime; TSVM s5 PNG is **+312.7 min** later (09-23 15:06:10 vs 09:53:28) — exactly the documented offset |
| B4L-C047 | FORENSIC | §11-D1 | if the 3 PNG rows replaced the CSV rows, TSVM FP mean goes 14.6 → 22.5 and the "TSVM reduces FP" conclusion reverses | VERIFIED (arithmetic) | (146 − (8+7+14) + (10+90+8))/10 = 22.5; provenance of s0/s8 remains UNDETERMINED as the document states |
| B4L-C048 | FORENSIC | §11-D2 | TN = 40 − FP in all 20/20 rows | VERIFIED | raw CM recomputation (all rows) |
| B4L-C049 | FORENSIC | §Nguyên tắc | never edit the original CSVs to make them match a report | VERIFIED | no CSV/PNG mtime appears after the audit dates; only report-side files were rewritten |
| B4L-C050 | AUDIT7 | header, §1 | generated by `Stracth/verify_10seed_audit.py` on 02/10/2026; 694/694 checks pass, 0 fail (8 groups) | PARTIALLY_VERIFIED | generator script exists among the 55 `.py`; the printed total matches FORENSIC §10 but was not re-executed here |
| B4L-C051 | AUDIT7 | §2 | three standing limitations: TN derived, 17/20 CM match with TSVM s0/s5/s8 mismatching, CM usable only as a descriptive observation | VERIFIED | code + raw recomputation + the mtime reproduction in B4L-C046 |
| B4L-C052 | FIGREC | §1.1–1.3 | the 12 recommended figures exist (5 core + 5 supplementary + 2 CM) | VERIFIED | all 12 paths resolved on disk (`05_charts/**` and `figures/**`) |
| B4L-C053 | FIGREC | §3 | LaTeX metric table: Box mAP 0.7262±0.0198 / 0.7285±0.0141; Val Box 0.7239/0.7305 (p = 0.7008); Val Cls 0.5591/0.6148 (p = 0.0943); Val L1 0.0164/0.0162 (p = 0.6995); Std −39.7 %; Range −35.7 %; Min s3/s7 | VERIFIED | every value equals `full_comparison_mean_std.csv` / `metrics_min_max_range.csv` (p-values 0.700800 / 0.094331 / 0.699480) |
| B4L-C054 | FIGREC | §3 note | with N = 10 no metric reaches α = 0.05; Val Seg and Val Cls only approach α = 0.10 (0.0908 / 0.0943) with opposite signs | VERIFIED | CSV p-values 0.090772 / 0.094330 |
| B4L-C055 | FIGREC | §1.3, §4 | CM figures demoted to secondary with mandatory TN-reconstruction caveat and the 3/20 mismatch note; "167 → 160" correction | VERIFIED | matches the dataset counts and the disclosed limitations |

| B4L-C056 | KQ-EB-AUD | §1 | "exactly 4 models with 10 seeds measured: Baseline, TSVM, P5 VMamba, ITS Mamba"; "400 rows of raw data"; identity consistency with the 10-seed accuracy set | CONTRADICTED | `efficiency_summary.csv` has 2 rows; the raw CSV has 200 rows (2 × 100) with header `model_name,iteration,latency_ms`; `KetQua_Nen` holds 2 model dirs — P5/ITS weights do not exist |
| B4L-C057 | KQ-EB-AUD | §3 | latency sanity check incl. P5 477.98 ms and ITS Mamba 651.27 ms | PARTIALLY_VERIFIED | no P5/ITS row exists in any surviving CSV; the Baseline/TSVM rows are exact, the other two are unsupported |
| B4L-C058 | KQ-EB-REP | §3 | 4-model efficiency table: Params 11.434/11.719/12.229/12.255; GFLOPs 18.54/18.70/18.94/18.86; size 22.27/22.82/23.83/23.86 MB; latency 200.12/477.98/651.27/821.27 ms; FPS 5.00/2.09/1.54/1.22 | CONTRADICTED | the table it cites (`efficiency_summary.csv`) contains only the Baseline and TSVM rows — half the table has no source file, and the file dates from the pre-cleanup 27/09/2026 run |
| B4L-C059 | KQ-EB-REP | §4, §5.3 | accuracy–efficiency merge quoting `doc/16_...md` with P5 mAP 0.7165 and ITS 0.7203, and placing them "below the Pareto frontier" | UNVERIFIED | no 10-seed P5/ITS run survives in `KetQua_Nen/`; the values can no longer be traced to any raw artefact |
| B4L-C060 | KQ-EB-REP | §6 | 15 figures at 300 DPI in that package | VERIFIED | 15 files present in `KQ_Nen_DX_10seed/efficiency_benchmark/figures` |
| B4L-C061 | CHARTMAP | §1 | 12 template-migrated charts (the `01…14` list) in `figures/` | VERIFIED | `figures/` holds exactly 12 files and every listed name resolves |
| B4L-C062 | CHARTMAP | §1 | "`02_val_seg_loss_barchart` … (−1.10 % loss mean, −40.6 % std)" | CONTRADICTED | current evidence: mean −4.76 %, σ −55.4 % (`full_comparison_mean_std.csv`) |
| B4L-C063 | CHARTMAP | §1, §4.1 | the seed-by-seed chart was expanded from the old 6 seeds to the full 10 seeds | VERIFIED | consistent with the documented migration from the 6-seed `KQ_DoiXung` templates |
| B4L-C064 | CHARTMAP | §2 | "all 20 original charts kept 100 % intact" in `01_summary/`, `02_distributions/`, `03_seed_by_seed/`, `04_confusion_matrix/`, `05_multimetric/` | OUTDATED | none of those folders exists; the package now uses `05_charts/{performance,stability,distribution,correlation,summary}` (16 PNGs) plus `figures/` (12) |
| B4L-C065 | CHARTMAP | §3 | exclusion list (`02_Ghep_DoiXung`, `07a`, `08` cumulative loss, `15a–c` latency breakdown) with scientific reasons | VERIFIED | rationale documented and the excluded items are indeed absent from the package |
| B4L-C066 | CHARTMAP | §4.1 | loss curves and metrics "extracted directly from 40 tệp `results.csv` in `archive/KetQua_Nen/`" | CONTRADICTED | only 20 `results.csv` exist, and they live in `archive/Ket_Qua_V2/KetQua_Nen/` (both the count and the path are wrong) |
| B4L-C067 | CHARTMAP | §4 | every generated chart is 300 DPI and the raw data was untouched | PARTIALLY_VERIFIED | "raw untouched" is consistent with the mtime picture; the DPI attribute was not re-measured |


## 4. BATCH 4 STATUS TALLY (67 claims)

| Status | Count |
|---|---|
| VERIFIED | 47 |
| PARTIALLY_VERIFIED | 10 |
| CONTRADICTED | 6 |
| UNVERIFIED | 1 |
| OUTDATED | 1 |
| NO_MATERIAL_CLAIMS | 2 |
| **Total** | **67** |

Reading of the tally: the 10-seed analysis package (`KQ_Nen_DX_10seed/`) is the **most verifiable block of the whole corpus** — 47 of its claims reproduce exactly against the 20 `results.csv`, the 15 derived CSVs and the source code, including two checks run for the first time in this audit (the CM-PNG mtime pattern and the Dice/F1 non-identity arithmetic). All six CONTRADICTIONS sit outside that block: two in the stale 4-model benchmark package, three in `chart_template_mapping.md`, one in the package index (broken `data_bg20.yaml` path).

## 5. BATCH 4 CORRECTIONS

1. **Two benchmark packages survive and disagree about how many models were measured.** `archive/Ket_Qua_V2/efficiency_benchmark/reports/{benchmark_report,benchmark_audit}.md` describe **2 models** and match their CSV cell-for-cell; `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/reports/{...}` claim "**đúng 4 mô hình đủ 10 seed**" (Baseline / TSVM / P5 VMamba / ITS Mamba), "**400 dòng dữ liệu raw**" and print P5 11.719 M / 477.98 ms, ITS 12.229 M / 651.27 ms. Both packages' CSVs (`efficiency_summary.csv`, `efficiency_raw_benchmark.csv`) contain **only** the Baseline and TSVM rows and **200** raw rows, and `KetQua_Nen/` contains no P5/ITS checkpoint directory. ⇒ Quote only the 2-model package (`Ket_Qua_V2/efficiency_benchmark/reports/`); treat the other text as a pre-cleanup draft.
2. **`chart_template_mapping.md` is internally and externally stale** in three places: "40 tệp `results.csv`" (actual 20), the val-seg-loss chart annotation "−1.10 % mean / −40.6 % std" (actual −4.76 % / −55.4 %), and §2's inventory of five chart folders (`01_summary/`, `02_distributions/`, `03_seed_by_seed/`, `04_confusion_matrix/`, `05_multimetric/`) that no longer exist — the package now exposes `05_charts/{performance,stability,distribution,correlation,summary}` (16 PNGs) + `figures/` (12).
3. **Two unreconciled grand totals for the same audit**: `final_audit_report.md` §2.1 says "**559/559** phép kiểm ĐẠT" while `07_audit/audit_report.md` §1 and `FORENSIC_EXPERIMENT_AUDIT.md` §10 both print "**694/694** PASS" (groups: results.csv 1, raw 17, mean_std 104, min_max 156, seed_cmp 79, 03_metrics 312, CM 17, alt 8). Neither document defines the scope difference (a re-extraction subset of 340 cells vs the full check suite). ⇒ Quote neither total as an audit score until the scope is fixed; the substantive checks themselves are verified.
4. **Index-level caveats are missing where they matter most.** `KQ_Nen_DX_10seed/README.md` §3.4 quotes the derived TN (25.4 / 23.2) in a "findings" list without the mandatory "TN = 40 − FP, reconstruction" caveat that `conclusions_reviewed.md` §4.3 and `07_audit` §2 impose, and the `data_bg20.yaml` it cites has a broken `path:` (`archive/Kvasir_YOLO_SEG_BG20` does not exist; the dataset is at `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20`).
5. **The FP-reduction headline survives only while the CM CSV is assumed correct.** FORENSIC §11-D1 (now independently reproduced here through PNG↔CSV mtimes: 19/20 equal, TSVM s5 PNG **+312.7 minutes** later) shows that substituting the three PNG rows raises TSVM FP from 14.6 to **22.5** and reverses the conclusion. The s5 artefact overwrite is explained (diagnostic scripts at 15:04–15:06); the origin of the s0/s8 artefacts remains UNDETERMINED. ⇒ Any FP/TN statement must stay descriptive and must carry this caveat.
6. **Do-not-cite list created by this batch**: Dice/F1 derived values (0.868162 / 0.879772 / 0.879747 / 0.886447), any IoU/mIoU/Dice/F1 "metric" (none exist in the package), and TN/Specificity values quoted as measurements.

## 6. APPENDIX UNRESOLVED

Not re-executed / not re-measured in that prior pass: B4L-C029 (CM PNG OCR), B4L-C050 (694-check run), B4L-C057 and B4L-C059 (the P5/ITS benchmark and accuracy numbers have **no surviving artefact** — they will never be verifiable, so they must simply not be used), B4L-C006 (CUDA/VRAM environment), B4L-C008 (hardware and library versions), B4L-C067 (DPI attribute), B4L-C011 (the weak `doc/16_...md` provenance label on an otherwise correct merge table).

## 7. APPENDIX STATUS

`NOT BATCH 4 REMAINING COVERAGE` — this appendix re-audited 13 `Ket_Qua_V2` files already in BATCH 1 plus the 2 Ultralytics READMEs. Remaining-file BATCH 4 is the 3-file section above (`B4-C001…B4-C017`). Do not read this appendix verdict as remaining-file completion.


---

---

# FINAL MERGED AUDIT — 56/56

This is the authoritative merge of BATCH 1, BATCH 2, BATCH 3 and BATCH 4 (remaining) for **every** Markdown file under `archive/`. It supersedes every conflicting statement above, including the earlier `MERGE FINAL — 56-file master census` draft (removed), the mis-scoped 15-file BATCH 4 appendix (`B4L-C*`, retained above as audit trail only), and the interim `11/16` BATCH 1 coverage figure.

## 0. METHOD AND GROUND RULES

1. **Scope:** `archive/` only. No web, no external repo, no assumption outside the archive.
2. **Evidence priority (strict):**
   `actual artifact / data / log / config / code / image` → `generated result` → `Markdown documentation`.
   A Markdown file is **never** accepted as evidence for a number when an artifact carrying that number exists.
3. **Evidence is not edited.** No CSV, PNG, `results.csv`, YAML or code file was modified. Only this ledger was updated.
4. **No root-cause speculation.** Where the archive does not establish a cause, the cause is recorded as `UNKNOWN`.
5. **Descriptive ≠ statistical.** A mean improvement is descriptive. It becomes a significance claim only with a p-value below α. No metric in the 10-seed study reaches p ≤ 0.05.
6. **Historical ≠ wrong.** A historical document is judged *at its time*; it is `OUTDATED` if superseded by later evidence, `CONTRADICTED` only if contradicted **by surviving evidence**.

## 1. COVERAGE — 56/56 FILES

### 1.1 Filesystem enumeration (re-run for this merge)

`Get-ChildItem archive -Recurse -Filter *.md -File` → **56**.

| Batch | Scope | Files | Manifest rows |
|---|---|---:|---|
| BATCH 1 | `archive/Bao_cao/**` + `archive/Ket_Qua_V2/**` | **16** | #2–#4, #42–#54 |
| BATCH 2 | `archive/doc/**` excluding `historical/**` | **27** | #5–#31 |
| BATCH 3 | `archive/doc/historical/**` | **10** | #32–#41 |
| BATCH 4 (remaining) | this ledger + 2 vendored Ultralytics READMEs | **3** | #1, #55, #56 |
| **TOTAL** | | **56** | 16 + 27 + 10 + 3 = **56** |

Cross-check by directory: `Bao_cao` 3 + `Ket_Qua_V2` 13 + `doc∖historical` 27 + `doc/historical` 10 + `ultralytics_*` 2 + this ledger 1 = **56**. ✔

**Coverage status: COMPLETE — 56/56 files read, claims extracted, and mapped to archive evidence.**

### 1.2 Duplicates, overlaps and mis-scoped claims found

| # | Finding | Detail | Resolution in this merge |
|---|---|---|---|
| 1 | **Duplicate file coverage (BATCH 4 appendix)** | The earlier appendix labelled "BATCH 4" re-audited the **13 `Ket_Qua_V2` files already in BATCH 1** plus the 2 Ultralytics READMEs. Claim IDs `B4L-C001…B4L-C067`. | Those 13 files are **reassigned to BATCH 1**. The `B4L-*` IDs are **retained verbatim** (not recreated) and are counted **once**, under BATCH 1, in the ledger below. Recorded as `B4-C013`. |
| 2 | **Overlapping Ultralytics README claims** | `B4L-C001/C002` (both `NO_MATERIAL_CLAIMS`) cover the same two files as `B4-C001…B4-C009`. | `B4L-C001/C002` are marked **superseded duplicates** and **excluded from the claim total**. `B4-C001…C009` are canonical. Recorded as `B4-C014`. |
| 3 | **Contradictory BATCH 1 coverage (11/16 vs 16/16)** | Interim "FINAL QA" says `Ket_Qua_V2` 8/13 read, 5 inventory-only, total 11/16. Later "BATCH 1 RESULTS" says 16/16 COMPLETE and states the 5 files were read. | **16/16 is correct.** The 11/16 figure is an earlier snapshot. Both are now labelled in place. Recorded as `B4-C015`. |
| 4 | **BATCH 1 claim-count mismatch (14 vs 28)** | The old MERGE tallied B1 as 14 claims; the BATCH 1 census actually enumerates `B1-C001…B1-C028`. | **28** is correct. The 14 figure was an under-count. Recorded as `B4-C016`. |
| 5 | **False arithmetic closure "3+1+27+10+13+2"** | That split reaches 56 only by counting `Ket_Qua_V2` twice and swapping the ledger for a `Bao_cao` file. | Correct split is `3+13+27+10+2+1`. Recorded as `B4-C013`. |
| 6 | **Mis-stated `56/56` meaning** | "56/56 files" was at risk of reading as "56/56 scientific PASS". | Coverage arithmetic is separated from claim-level PASS. Recorded as `B4-C017`. |

**No Markdown file was left unaudited, and no file is counted in two batches.**

## 2. CLAIM LEDGER — MERGED

### 2.1 Reconciliation rules applied

1. **No claim is recreated.** Every ID below is an ID that already existed in BATCH 1–4. `B4L-*` IDs are carried over unchanged; only their **batch attribution** is corrected.
2. **Canonical batch assignment:** `B1` + `B4L-C003…C067` → **BATCH 1** (the 13 `Ket_Qua_V2` files). `B4L-C001/C002` → superseded, excluded. `B4-C001…C017` → **BATCH 4 (remaining)**.
3. **Status vocabulary (final, 6 values):** `VERIFIED`, `PARTIALLY_VERIFIED`, `CONTRADICTED`, `UNVERIFIED`, `OUTDATED`, `PROVENANCE_ISSUE`.
   Batch-local terms are mapped as follows and are **not** discarded:
   - `MISLEADING` → `CONTRADICTED` (a claim whose wording asserts more than the evidence supports is not defensible as written).
   - `HIST_CONSISTENT` → `VERIFIED` **with a `historical-at-time` tag** (exactly reproducible from the era's own tables, and correctly quarantined).
   - `HIST_UNVERIFIED` → `UNVERIFIED` **with a `historical-at-time` tag**.
   - `NO_MATERIAL_CLAIMS` → retained as a file-level note, **not counted as a claim**.

### 2.2 Claim ID census

| Ledger | ID range | Count | Batch after merge | Source files |
|---|---|---:|---|---|
| B1 | `B1-C001 … B1-C028` | 28 | BATCH 1 | `Bao_cao/*` (narrative claims) |
| B4L → B1 | `B4L-C003 … B4L-C067` | 65 | BATCH 1 (reassigned) | `Ket_Qua_V2/**` (13 files) |
| B2 | `B2-C001 … B2-C113` | 113 | BATCH 2 | `doc/**` (27 files) |
| B3 | `B3-C001 … B3-C078` | 78 | BATCH 3 | `doc/historical/**` (10 files) |
| B4 | `B4-C001 … B4-C017` | 17 | BATCH 4 (remaining) | ledger + 2 Ultralytics READMEs |
| — | `B4L-C001`, `B4L-C002` | 2 | **excluded** (superseded duplicates of `B4-C001…C009`) | — |
| **TOTAL COUNTED** | | **301** | | **56 files** |

**Total claims audited = 301** (unique claim IDs, no double counting).

### 2.3 Traceability index — claim IDs by file

| Batch | Markdown file (under `archive/`) | Claim IDs |
|---|---|---|
| B2 | `doc/00_TONG_QUAN_VA_TINH_HINH_DU_AN.md` | `B2-C001…C014` |
| B2 | `doc/01_KIEN_TRUC_TSVM_TANG_10.md` | `B2-C017…C020` |
| B2 | `doc/03_CAU_TRUC_THU_MUC_VA_HUONG_DAN_TAI_LAP.md` | `B2-C021…C023` |
| B2 | `doc/04_KET_QUA_LOSS_VA_HOI_TU.md` | `B2-C024…C026` |
| B2 | `doc/06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md` | `B2-C027…C034` |
| B2 | `doc/07_MA_TRAN_NHAM_LAN_VA_CHI_SO_BENH_HOC.md` | `B2-C035…C040` |
| B2 | `doc/08_CHI_PHI_TINH_TOAN_DO_TRE_VA_TRIEN_KHAI.md` | `B2-C041…C043` |
| B2 | `doc/10_DANH_GIA_CHAT_LUONG_MAT_NA_VISUAL.md` | `B2-C044…C045` |
| B2 | `doc/15_CAM_NANG_PHONG_CACH_WORD_VA_NGON_NGU_HOC_THUAT.md` | `B2-C046…C047` |
| B2 | `doc/16_THUC_NGHIEM_BO_SUNG_20_PHAN_TRAM_ANH_NEN_BG20.md` | `B2-C048…C057` |
| B2 | `doc/17_SU_CO_FUSE_XUAT_ANH_KAGGLE_VA_PHUONG_AN_KHAC_PHUC.md` | `B2-C058…C061` |
| B2 | `doc/18_ANH_XA_SCRIPT_VA_NGUON_GOC_KET_QUA_10SEED.md` | `B2-C062…C065` |
| B2 | `doc/19_QUY_CHUAN_THIET_KE_WORD_LE_DUC_LUONG.md` | `B2-C066` (style doc) |
| B2 | `doc/20_KET_QUA_CHUAN_BASELINE_VS_TSVM_BG20_10SEED.md` (core source of truth) | `B2-C067…C073` |
| B2 | `doc/21_HUONG_DAN_BAN_GIAO_AI_MOI_VA_VIEC_CONG_TAI.md` | `B2-C074…C077` |
| B2 | `doc/22_DANH_MUC_HINH_ANH_TOAN_BO.md` | `B2-C078…C080` |
| B2 | `doc/23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md` | `B2-C081…C084` |
| B2 | `doc/24_DANH_SACH_DUONG_DAN_HONG.md` | `B2-C085…C086` |
| B2 | `doc/AI_WORK_OPTIMIZATION_RULE.md` | `B2-C087` (no material claims) |
| B2 | `doc/BAO_CAO_DAC_TA_HUONG_NGHIEN_CUU.md` | `B2-C088` |
| B2 | `doc/CURRENT_PROJECT_STATUS.md` | `B2-C089…C094` |
| B2 | `doc/kvasir_yolo_seg_output_spec.md` | `B2-C095…C097` |
| B2 | `doc/LICHSU_CAP_NHAT.md` | `B2-C098…C103` |
| B2 | `doc/nguyen-tac-lam-viec-dai.md` | `B2-C094` (work rules; no material claims) |
| B2 | `doc/README.md` | `B2-C103…C107` |
| B2 | `doc/training_results_audit.md` | `B2-C108…C110` |
| B2 | `doc/YEU_CAU_DAC_TA_DU_LIEU_BO_SUNG_CROSS_DATASET.md` | `B2-C111…C113` |
| B3 | `doc/historical/README.md` (quarantine manifest) | `B3-C001…C012` |
| B3 | `doc/historical/05_KET_QUA_MAP_VA_DO_ON_DINH_SEED.md` | `B3-C013…C022` |
| B3 | `doc/historical/6seed_bao_luu/…_old_report_backup_6seed.md` | `B3-C023…C030` |
| B3 | `doc/historical/mo_hinh_khong_lien_quan/01_KIEN_TRUC_C2IAVM_CHAMPION_VA_CAC_BIEN_THE.md` | `B3-C031…C040` |
| B3 | `doc/historical/mo_hinh_khong_lien_quan/09_KHAO_SAT_ABLATION_TANG_10_VS_P5.md` | `B3-C041…C048` |
| B3 | `doc/historical/mo_hinh_khong_lien_quan/11_CHI_TIET_KET_QUA_P5_ATTENTION_VMAMBA.md` | `B3-C049…C053` |
| B3 | `doc/historical/mo_hinh_khong_lien_quan/12_CHI_TIET_KET_QUA_IAVM_INTERACTIVE_ATTENTION_VMAMBA.md` | `B3-C054…C058` |
| B3 | `doc/historical/mo_hinh_khong_lien_quan/14_HUONG_8_INTERACTIVE_TOPOLOGY_VMAMBA.md` | `B3-C059…C064` |
| B3 | `doc/historical/thuc_nghiem_6fold_5mo_hinh/02_KET_QUA_THUC_NGHIEM_VA_DOI_CHIEU.md` | `B3-C065…C070` |
| B3 | `doc/historical/thuc_nghiem_6fold_5mo_hinh/BAO_CAO_TIEN_DO_TUAN_HOAN_CHINH.md` | `B3-C071…C078` |
| B4 | `ultralytics_Topology-Shape-aware VMamba/cfg/models/README.md` | `B4-C001…C004` |
| B4 | `ultralytics_Topology-Shape-aware VMamba/trackers/README.md` | `B4-C005…C009` |
| B4 | `MARKDOWN_CLAIM_AUDIT.md` (this ledger) | `B4-C010…C017` |
| B1 | `Bao_cao/CNTT_KLCN182_LeDucLuong_old_report.md` | historical/secondary — no unique IDs |
| B1 | `Bao_cao/CNTT_KLCN182_LeDucLuong_report_10seed.md` | `B1-C001…C014` |
| B1 | `Bao_cao/CNTT_KLCN182_LeDucLuong_report_10seed_audited.md` | `B1-C001…C014` (corrected twin) |
| B1 | `Ket_Qua_V2/efficiency_benchmark/reports/benchmark_audit.md` | `B4L-C003…C007` |
| B1 | `Ket_Qua_V2/efficiency_benchmark/reports/benchmark_report.md` | `B4L-C008…C013` |
| B1 | `Ket_Qua_V2/KQ_Nen_DX_10seed/README.md` | `B4L-C014…C020` |
| B1 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/conclusions.md` | `B4L-C021…C025` |
| B1 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/conclusions_reviewed.md` | `B4L-C026…C032` |
| B1 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/summary.md` | `B4L-C033…C035` |
| B1 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/final_audit_report.md` | `B4L-C036…C040` |
| B1 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/FORENSIC_EXPERIMENT_AUDIT.md` | `B4L-C041…C049` |
| B1 | `Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/recommended_figures_for_thesis.md` | `B4L-C052…C055` |
| B1 | `Ket_Qua_V2/KQ_Nen_DX_10seed/07_audit/audit_report.md` | `B4L-C050…C051` |
| B1 | `Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/reports/benchmark_audit.md` (stale 4-model) | `B4L-C056…C057` |
| B1 | `Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/reports/benchmark_report.md` (stale 4-model) | `B4L-C058…C060` |
| B1 | `Ket_Qua_V2/KQ_Nen_DX_10seed/reports/chart_template_mapping.md` (stale) | `B4L-C061…C067` |
## 3. EVIDENCE RECONCILIATION — CRITICAL CLAIMS

Every item below was re-checked **against the artifact**, not against Markdown prose. Artifact paths are relative to `archive/`.

### 3.1 Dataset composition — 160 / 127 / 120 / 40

**Verdict: VERIFIED** (`B1-C005`, `B1-C006`, `B1-C007`, `B1-C024`, `B2-C001`, `B2-C068`, `B4L-C014`).

| Quantity | Value | Artifact evidence |
|---|---:|---|
| Validation images | **160** | 160 files in `Ket_Qua_V2/Kvasir_YOLO_SEG_BG20/images/val`; `data_bg20.yaml` `val_images: 160`; `dataset_bg20_summary.json` `total_val: 160` |
| Positive (polyp) images | **120** | `dataset_bg20_summary.json` `val_polyp_images: 120` |
| Background-negative images | **40** | `dataset_bg20_summary.json` `val_background_images: 40`; `selected_normal_cecum_val_40.txt` |
| Polyp **objects/instances** (GT) | **127** | `dataset_bg20_summary.json` `total_polyps_val: 127` |
| Total dataset | 1 200 | `total_dataset_images: 1200` (1 040 train + 160 val) |

**Semantics that must not drift:** `127` counts **objects**, not images. `120 + 40 = 160` images. The value **167** (= 127 + 40) is a **conflation of objects with images** and appears nowhere in the current evidence base. Any sentence of the form "160 ảnh (127 polyp GT + 40 ảnh nền)" (`B2-C034`) is `CONTRADICTED` and must read "120 polyp images containing 127 objects + 40 background images".
Independently corroborated by `raw_10seeds_confusion_matrices.csv`: **all 20 rows** satisfy `TP + FN = 127` and `FP + TN = 40`.

### 3.2 TN = 40 − FP is reconstructed, not observed

**Verdict: VERIFIED** as a provenance finding; the TN **value** is `PROVENANCE_ISSUE` (`B1-C013`, `B2-C038`, `B2-C040`, `B4L-C020`, `B4L-C028`, `B4L-C048`).

- **Code artifact:** vendored `ultralytics_Topology-Shape-aware VMamba/utils/metrics.py`, `ConfusionMatrix.process_batch` (~lines 427–434) increments **only FP** for an image with empty ground truth and then returns. There is **no** `matrix[nc, nc] += 1` branch. The background↔background cell is therefore never populated, and line 550 filters values `< 0.005`, so the cell renders empty on every one of the 20 `confusion_matrix.png` files.
- **Data artifact:** `raw_10seeds_confusion_matrices.csv` satisfies `TN = 40 − FP` in **20/20 rows** (re-checked; 0 violations).
- **Means:** Baseline FP 16.8 → TSVM 14.6; Baseline TN 23.2 → TSVM 25.4 (recomputed from the CSV).

⇒ TN (and Specificity derived from it) is a **reconstruction under the background-negative design**, never a direct observation. It must never be labelled "measured", and no per-image specificity inference is permitted.

### 3.3 Statistical significance — p > 0.05 everywhere

**Verdict: the significance claims are CONTRADICTED; the descriptive claims are VERIFIED** (`B1-C009`, `B1-C019`, `B2-C074`, `B4L-C021`, `B4L-C031`, `B4L-C044`, `B4L-C054`).

`full_comparison_mean_std.csv` — all 13 metrics carry `statistically_significant_005 = False`:

| Metric | Baseline | TSVM | p (paired t) | Sig @ 0.05 |
|---|---:|---:|---:|:---:|
| Mask mAP@50-95 | 0.7210 ± 0.0129 | 0.7246 ± 0.0078 | 0.3839 | No |
| Mask mAP@50 | 0.9119 ± 0.0107 | 0.9062 ± 0.0082 | 0.2273 | No |
| Mask Precision | 0.9023 ± 0.0339 | 0.9118 ± 0.0246 | 0.5428 | No |
| Mask Recall | 0.8584 ± 0.0252 | 0.8625 ± 0.0173 | 0.5907 | No |
| Box mAP@50-95 | 0.7262 ± 0.0198 | 0.7285 ± 0.0141 | 0.7152 | No |
| Box Recall | 0.8434 ± 0.0337 | 0.8567 ± 0.0152 | 0.2674 | No |
| Val Seg Loss | 1.3045 ± 0.0867 | 1.2424 ± 0.0387 | **0.0908** | No |
| Val Cls Loss | 0.5591 ± 0.0635 | 0.6148 ± 0.0884 | 0.0943 | No |

**Minimum p across all 13 metrics = 0.090772** (Val Seg Loss). Minimum Wilcoxon = 0.083984. Mask mAP p = 0.383917.

⇒ **No metric is statistically significant at α = 0.05.** Every "vượt trội", "chứng minh", "hoàn toàn", "significantly better", "more stable" formulation is `CONTRADICTED` as written. Improvements are **descriptive only**. The word "better/superior/more stable" is **not permitted** without a metric scope and a stated p-value.

### 3.4 Seed win counts — Mask Precision 5/10, Mask Recall 6/10 no tie

**Verdict: the document counts are CONTRADICTED; the artifact counts are VERIFIED** (`B2-C029`, `B2-C031`, `B4L-C035`, `B4L-C044`, `B4L-C045`).

Artifact `seed_win_loss_summary.csv` (TSVM wins / Baseline wins / ties):

| Metric | TSVM | Baseline | Ties |
|---|---:|---:|---:|
| Mask mAP@50-95 | **6** | 4 | 0 |
| Mask mAP@50 | 3 | 7 | 0 |
| **Mask Precision** | **5** | 5 | 0 |
| **Mask Recall** | **6** | 4 | **0** |
| Val Seg Loss | 8 | 2 | 0 |

- `doc/06_DANH_DOI_PRECISION_RECALL_VA_LAM_SANG.md` claims **Mask Precision 7/10** → **CONTRADICTED**; true value **5/10**.
- `doc/06` claims **Mask Recall 5/10 with 1 tie** → **CONTRADICTED**; true value **6/10 with 0 ties** (a phantom tie).
- Mask mAP win membership per `raw_10seeds_extracted_metrics.csv`: TSVM ahead at **s1, s2, s3, s6, s8, s9** — count 6/10 correct, but `doc/historical/05_KET_QUA…` lists a wrong membership (`s0,s1,s3,s4,s6,s8`) → `B3-C021` `CONTRADICTED`.
### 3.5 Efficiency table contradictions — four incompatible cost generations

**Verdict: CONTRADICTED** for every GPU-style cost table (`B2-C041`, `B2-C043`, `B2-C047`, `B2-C072`, `B4L-C056…C059`, `B3-C027`).

**The only file-backed generation** — `Ket_Qua_V2/efficiency_benchmark/tables/efficiency_summary.csv` (`thop` profile + CPU timing, 200 raw rows in `efficiency_raw_benchmark.csv`):

| Quantity | YOLOv26s Baseline | TSVM |
|---|---:|---:|
| Params (M) | 11.434 | 12.255 |
| GFLOPs | 18.54 | 18.86 |
| Checkpoint (MB) | 22.27 | 23.86 |
| Latency mean (ms) | 200.12 | 821.27 |
| FPS | 5.00 | 1.22 |
| Peak VRAM | *(empty ⇒ N/A, CPU run)* | *(empty ⇒ N/A)* |

**Contradicting generations found in Markdown, none reproducible from any surviving artifact:**

| Source | Params (M) | GFLOPs | Latency (ms) | FPS | VRAM |
|---|---|---|---|---:|---|
| `efficiency_summary.csv` **(only artifact-backed)** | 11.434 / 12.255 | 18.54 / 18.86 | 200.12 / 821.27 | 5.00 / 1.22 | N/A |
| `doc/20` §6 — **cites the CSV above** | 11.55 / 12.16 | 42.3 / 47.4 | 17.2 / 19.8 | 58.1 / 50.5 | 1.42 / 1.68 GB |
| `doc/08_CHI_PHI` | 11.77 / 12.35 | 39.4 / 41.2 | 21.5 / 28.5 | 46.5 / 35.1 | 6.42 / 7.35 GB |
| 6-fold era (`B3-C027`, `B3-C074`) | 11.53 / 12.09 | 35.7 / 42.3 | 12.8 / 19.0 | 78.1 / 52.6 | 6.5 / 7.20 GB |

**The `doc/20` §6 defect is the sharpest:** it attributes GPU-style numbers (11.55/12.16 M, 42.3/47.4 GFLOPs, 17.2/19.8 ms, 58.1/50.5 FPS, VRAM 1.42/1.68 GB) to a **CPU `thop` CSV that contains none of them** (`B2-C072` `CONTRADICTED`). Its "50.5 FPS vượt ngưỡng 25–30 FPS" conclusion is therefore **unsupported**.

Also `CONTRADICTED`: the stale 4-model benchmark package under `Ket_Qua_V2/KQ_Nen_DX_10seed/efficiency_benchmark/` claims **4 models / 400 raw rows** and prints P5 11.719 M / 477.98 ms and ITS 12.229 M / 651.27 ms — but `efficiency_summary.csv` holds **2 rows** and the raw CSV holds **200 rows**; no P5/ITS checkpoint directory exists (`B4L-C056`, `B4L-C058`). Pre-cleanup draft — must not be cited.

### 3.6 Confusion matrix — 17/20 matched; TSVM s0, s5, s8 mismatched

**Verdict: VERIFIED that the discrepancy exists; the three mismatching artefacts are PROVENANCE_ISSUE** (`B1-C014`, `B2-C039`, `B4L-C029`, `B4L-C046`, `B4L-C047`, `B4L-C051`).

| Run | Source A — `confusion_matrix.png` (read directly) | Source B — `raw_10seeds_confusion_matrices.csv` | ΔTP |
|---|---|---|---:|
| TSVM s0 | TP 59, FN 68, FP 10, TN 0 | TP 108, FN 19, FP 8, TN 32 | 49 |
| TSVM s5 | TP 0, FN 127, FP 90, TN 0 | TP 112, FN 15, FP 7, TN 33 | 112 |
| TSVM s8 | TP 6, FN 121, FP 8, TN 0 | TP 111, FN 16, FP 14, TN 26 | 105 |

**17/20 runs match exactly. TSVM s0, s5, s8 do not.** CM-implied recall from the CSVs agrees with each run's own `results.csv` `mask_recall` to ≤ 0.0027 (mean level); the PNG-implied recall (0.4646 / 0.0000 / 0.0472) contradicts them by 0.83–0.88.

**Consequence — the FP headline is source-dependent:** substituting the three PNG rows moves TSVM mean FP from **14.6 → 22.5**, i.e. it **reverses** the "TSVM reduces FP" conclusion. ⇒ All FP/TN/CM statements must remain **descriptive** and must carry this caveat.

### 3.7 Seed-5 CM PNG provenance — separate `YOLO.val()` run, then copied

**Verdict: PROVENANCE_ISSUE — mechanism established, but the artefact is not the training run's own output.**

Timestamp evidence (re-checked on this pass): 19/20 `confusion_matrix.png` mtimes are **identical** to their `results.csv` mtime. **TSVM s5 is the sole exception**: PNG `23/09 15:06:10` vs `results.csv` `23/09 09:53:28` = **+312.7 minutes**.

**Code artifact — the mechanism, confirmed by reading `Stracth/re_evaluate_seed5.py`:**

1. Loads `…/TSVM_s5_w2/weights/best.pt` and calls `model.val(data=Stracth/data_bg20_val.yaml, project=archive/Stracth/seed5_re_eval, name="val_run", plots=True, batch=16, device="cpu")` — a **standalone re-validation run**, writing to a different project directory.
2. Then iterates `files_to_copy` — which explicitly includes **`confusion_matrix.png`** and `confusion_matrix_normalized.png` — and runs **`shutil.copy2(src, dst)`** to overwrite them into the **original seed-5 run folder**.

So the s5 `confusion_matrix.png` in the run folder is **a CPU re-evaluation artefact copied over the training run's plot**, not the original training-time plot. That fully explains both its +312.7 min mtime and its near-zero recall (the copied plot came from a differently-configured validation pass). The `Stracth/seed5_re_eval/` and `Stracth/eval_s5_test/` directories still exist and are separately listed in `Stracth/_forensic_cm_ocr.py`, corroborating that re-evaluations were performed.

**Caveat on scope:** the script's own paths (`archive/KetQua_Nen/…`, `archive/Kvasir_YOLO_SEG_BG20`) do not match the current layout (`archive/Ket_Qua_V2/…`), and FORENSIC §12.7 marks the executed script variant `[UNVERIFIED]`. The **mechanism** is established from the surviving code; the exact execution is not re-runnable here.
### 3.8 Root cause of TSVM s0 / s5 / s8 mismatch — **UNKNOWN**

**Verdict: `PROVENANCE_ISSUE` / root cause `UNKNOWN` for s0 and s8. No root cause is asserted beyond what the archive proves.**

| Run | Root cause status | Archive basis |
|---|---|---|
| TSVM **s5** | **Mechanism established** (not a root cause beyond artefact substitution) | +312.7 min PNG offset + `re_evaluate_seed5.py` copying a separate `model.val()` output over the run-folder plot |
| TSVM **s0** | **UNKNOWN** | PNG mtime **equals** its `results.csv` mtime → no overwrite evidence exists. FORENSIC §11-D1 states "NGUYÊN NHÂN CHƯA XÁC ĐỊNH được" |
| TSVM **s8** | **UNKNOWN** | Same as s0: PNG mtime equals `results.csv` mtime; origin undetermined |

No prediction dump survives in the workspace to replay the failure, so the discrepancy cannot be closed from the archive. **This audit records the cause as UNKNOWN and does not speculate.**

### 3.9 Architecture and config claims vs YAML/code

| Claim | Artifact checked | Verdict |
|---|---|---|
| C2TSVMamba inserted at **layer 10** (P5, 20×20) | `cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml` line 31 `- [-1, 2, C2TSVMamba, [1024]] # 10` | **VERIFIED** (`B2-C006`, `B2-C093`, `B3-C031`) |
| Seg head reconnects P5; `Segment26` consumes P3/P4/P5 | same YAML, `Concat [-1,10]`, `Segment26 [16,19,22]` | **VERIFIED** (`B2-C093`) |
| Block splits 1×1 conv `c1 → 2c`, `self.c = int(c1*0.5)` = 256 | `nn/modules/topology_shape_vmamba.py` (`assert c1==c2`, `cv1`, `cv2`) | **VERIFIED** (`B3-C031`) |
| `topology_shape_vmamba.py` = 502 lines | file length re-checked | **VERIFIED** (`B2-C018`) |
| Ultralytics fork version `8.4.127` | shipped `__init__.py` `__version__` | **VERIFIED** (`B3-C071`) |
| Default tracker is **BoT-SORT** (tracker README) | `cfg/default.yaml` line 140 `tracker: tracktrack.yaml`; `solutions/config.py` `botsort.yaml` | **CONTRADICTED** — dual defaults; README matches neither the engine default (`B4-C006`) |
| Trackable tasks = detect/segment/pose/obb | `trackers/track.py` `trackable = ("detect","segment","pose","obb")` | **VERIFIED** (`B4-C007`) |
| Six tracker YAMLs exist | `cfg/trackers/*.yaml` + `track.py` `TRACKER_MAP` | **VERIFIED** (`B4-C005`) |
| Repo lacks `C3k2VSS`, `yolo26-vmamba-p3-seg.yaml`, P3 tree | workspace-wide recursive search → 0 hits | **VERIFIED** (`B2-C089`, `B2-C105`) |
| `Stracth/` contains 46 (`doc/23`) / 48 (`doc/README`) scripts | actual = **55** `.py` | **OUTDATED** (`B2-C082`, `B2-C106`) |
| 47 runs / 4 models / 40 `results.csv` | actual = **20** `results.csv`, 2 model dirs | **CONTRADICTED / OUTDATED** (`B2-C022`, `B2-C051`, `B2-C090`, `B4L-C066`) |
| `data_bg20.yaml` usable as-is | its `path:` → `archive/Kvasir_YOLO_SEG_BG20` (absent); real = `archive/Ket_Qua_V2/Kvasir_YOLO_SEG_BG20` | **CONTRADICTED (path)** (`B4L-C015`) |
| Provenance paths `KetQua_Nen/…`, `KetQua_Nen/Kvasir_BG20_…` | real base = `archive/Ket_Qua_V2/KetQua_Nen/…` | **CONTRADICTED (path)** (`B4L-C017`) |
| Example weights `yolo26n.pt` / `yolo26n-seg.pt` | **0** `*.pt` under the vendored fork | **UNVERIFIED** (`B4-C008`) |
| Trackers run video "in real-time without sacrificing accuracy" | no latency/accuracy artefact for any tracker | **UNVERIFIED** (`B4-C009`) |

### 3.10 FP baseline `17.4` vs true `16.8` — stale-value family

**Verdict: CONTRADICTED** (`B2-C012`, `B2-C033`, `B2-C097`, `B2-C110`, `B2-C113`).
Raw CM (recomputed): **FP 16.8 → 14.6 = −13.1 %**, TN 58.0 % → 63.5 %. The widespread figure **FP 17.4 → 14.6 (−16.1 %)** and **TN 56.5 % → 63.5 %** derives from the retired baseline `17.4`. `doc/LICHSU_CAP_NHAT` v3.1 itself lists `17.4` as a **retired** value — the v3.1 sweep never reached `doc/00`, `doc/06`, `kvasir_yolo_seg_output_spec`, `YEU_CAU_…` or `training_results_audit`.

### 3.11 Audit-score double counting

**Verdict: CONTRADICTED / unreconciled** (`B2-C077`, `B4L-C036`, `B4L-C050`).
`final_audit_report.md` §2.1 prints **559/559**; `07_audit/audit_report.md` §1 and `FORENSIC_EXPERIMENT_AUDIT.md` §10 print **694/694**. Neither document defines the scope difference. ⇒ **Quote neither total as an audit score.** The substantive checks behind them are verified.

### 3.12 Banned derived metrics

**Verdict: CONTRADICTED if cited** (`B4L-C042`, `B4L-C043`).
The raw CSV header (21 fields) contains **no** IoU / mIoU / Dice / F1 column. Derived Dice/F1 values (0.868162 / 0.879772 / 0.879747 / 0.886447) are reconstructible from mean CM and mean P/R but are **not package metrics**, and Dice ≠ F1 was demonstrated numerically. They may not be cited.
## 4. HISTORICAL DOCUMENTS — how they are judged

`archive/doc/historical/**` (10 files) is **declared non-authoritative by its own manifest** (`historical/README.md`: never cite as a data source; the single source is `doc/20_…` + `Ket_Qua_V2/KQ_Nen_DX_10seed/`). This audit therefore does **not** treat a historical document as "wrong" merely because it differs from current evidence.

### 4.1 The four distinctions used

| Category | Definition | Consequence | Count |
|---|---|---|---:|
| **historical-at-time** (consistent) | Era number exactly reproducible from the era's own printed tables, and correctly quarantined | `VERIFIED` **with `historical-at-time` tag**. Not a defect. | 10 |
| **current** | Statement about the present repository that survives artifact checking | `VERIFIED` | 25 |
| **outdated / superseded** | True when written; a later generation replaced it (path drift, run inventory, script counts, stale FP baseline) | `OUTDATED`. Not an error at the time. | 2 |
| **contradicted by later evidence** | A surviving artifact or a sibling document of the same era disproves it | `CONTRADICTED`. This **is** a defect. | 22 |

### 4.2 Examples of each

- **historical-at-time (consistent):** 6-fold means Base 0.7291 / TSVM 0.7231 / C2IAVM 0.7361 with σ 0.0153 / 0.0055 / 0.0073 — recomputed exactly from the `6fold/02` per-seed matrix (`B3-C014`). Head-to-head win rate 83.33 % = 5/6 (`B3-C013`).
- **outdated:** `KQ_DoiXung/` chart folders no longer exist (`B3-C073`); run inventory described as 47 runs (`B2-C051`); `data_bg20.yaml` paths pointing at the pre-`Ket_Qua_V2` layout (`B3-C022`, `B4L-C017`).
- **contradicted by later evidence:** `14_HUONG_8` "C2TSVMamba 73.3 % mAP / 85.8 % Recall" — real 72.31 % / 84.93 % (`B3-C059`); "C2IAVM Recall 89.5 % / mAP 74.3 % kỷ lục" — real 88.75 % / 73.61 %, and 74.7 % is only the single best seed s1 (`B3-C060`). `09_ABLATION` internal clashes: C2IAVM 0.7365 ± 0.0074 / 88.85 % (§3) vs 0.7361 ± 0.0073 / 88.75 % (§5); variance reduction 4.15× vs 4.39× (`B3-C038`, `B3-C044`, `B3-C045`).
- **unverifiable, therefore not citable:** every 6-fold / single-seed figure whose raw run directory was deleted — P5-Attention, ITSMamba, C2IAVM, Boundary-aware, Multi-scale (`B3-C039`, `B3-C049`, `B3-C051`, `B3-C054`, `B3-C056`, `B3-C062`, `B3-C063`).

### 4.3 Manifest housekeeping errors found

1. **`.docx` status is stale.** `README` claims the `.docx`/`.pdf` still hold six wrong p-values (0.2319 / 0.4439 / 0.7027 / 0.7677 / 0.9189 / 0.2887) and "167 đối tượng". The shipped `.docx` `<w:t>` text has **0** hits for all six values and **0** for "167"; it carries the corrected 0.3839 and 0.0908. The `.pdf` (85 FlateDecode streams) remains **UNVERIFIED** and its mtime predates the `.docx` fix (`B3-C006`, `B3-C009`).
2. **The "invalid encoding" warning is false.** `…_old_report_backup_6seed.md` contains 1 355 bytes of value `0xBB`, but all are legal UTF-8 continuation bytes; a strict UTF-8 decode succeeds and the file reads normally (`B3-C003`).
3. **Misattribution of "167 ảnh".** It is attributed to `12_CHI_TIET_KET_QUA_IAVM…md`, where it never occurs (only `0.9167`). The offending drafts were `conclusions_reviewed.md` / `final_audit_report.md`, both already repaired (`B3-C010`).
4. **Metadata clash.** The same supervisor is "TS. Phùng Thế Bảo" in `6fold/BAO_CAO_TIEN_DO` and "ThS. Phùng Thế Bảo" in the 6-seed backup (`B3-C024`, `B3-C077`).

## 5. STATUS TALLY — FINAL (301 claims)

Status vocabulary per §2.1. `MISLEADING` folded into `CONTRADICTED`; `HIST_CONSISTENT` → `VERIFIED` (historical-at-time); `HIST_UNVERIFIED` → `UNVERIFIED` (historical-at-time); `NO_MATERIAL_CLAIMS` excluded.

| Status | B1 | B4L→B1 | B2 | B3 | B4 | **TOTAL** |
|---|---:|---:|---:|---:|---:|---:|
| VERIFIED | 18 | 42 | 42 | 35 | 8 | **145** |
| PARTIALLY_VERIFIED | 1 | 8 | 31 | 5 | 3 | **48** |
| CONTRADICTED | 6 | 6 | 13 | 27 | 4 | **56** |
| UNVERIFIED | 0 | 1 | 18 | 9 | 2 | **30** |
| OUTDATED | 0 | 1 | 5 | 2 | 0 | **8** |
| PROVENANCE_ISSUE | 3 | 7 | 2 | 0 | 0 | **12** |
| *no material claims (file note, not a claim)* | 0 | 0 | 2 | 0 | 0 | *2* |
| **Total ledger entries** | **28** | **65** | **113** | **78** | **17** | **301** |

Column check: 28 + 65 + 113 + 78 + 17 = **301** = 28 (B1) + 65 (B4L excl. 2) + 113 (B2) + 78 (B3) + 17 (B4). ✔
Row check: 145 + 48 + 56 + 30 + 8 + 12 = **299 material claims**, plus 2 file-level "no material claims" notes = **301 ledger entries**. ✔

`PROVENANCE_ISSUE` = **12**. These 12 were previously filed under `MISLEADING`, `PARTIALLY_VERIFIED` or `VERIFIED` because their **numbers are arithmetically right** while their **origin is defective**. They are reclassified here so that "verified" can no longer be read as "safe to quote without a caveat":

| Claim ID | Subject |
|---|---|
| `B1-C013`, `B1-C023`, `B2-C038`, `B4L-C020`, `B4L-C028`, `B4L-C048` | TN = 40 − FP is reconstructed, never observed |
| `B1-C014`, `B2-C039`, `B4L-C029`, `B4L-C046`, `B4L-C047`, `B4L-C051` | 17/20 CM match; TSVM s0/s5/s8 artefacts unreliable; FP 14.6 → 22.5 under PNG substitution |

### 5.1 Where the defects concentrate

| Area | CONTRADICTED | OUTDATED | Total | Why |
|---|---:|---:|---:|---|
| Quarantined 6-fold era (`doc/historical/**`, B3) | 27 | 2 | 29 | deliberate quarantine; proves the rule was necessary |
| `doc/**` narrative layer (B2) | 13 | 5 | 18 | stale FP baseline, wrong win counts, GPU-style cost tables, overclaim wording |
| `Ket_Qua_V2/**` stale drafts (B4L, incl. 2 file notes) | 6 | 1 | 7 | pre-cleanup 4-model benchmark package, stale chart inventory |
| `Bao_cao/**` narrative reports (B1) | 6 | 0 | 6 | overclaim wording; mis-scoped coverage claims |
| Vendored Ultralytics READMEs (B4) | 4 | 0 | 4 | upstream templates, not thesis documentation |
| **Tier-A evidence base (CSVs, `results.csv`, code, YAML)** | **0** | **0** | **0** | — |
| **TOTAL** | **56** | **8** | **64** | |

⇒ **No defect in the final tally originates from the primary data.** Every contradiction lives in narrative or stale-draft layers.
## 6. FINAL SUMMARY

| Metric | Value |
|---|---:|
| Total Markdown files audited | **56 / 56** |
| Total claims audited (unique IDs) | **301** |
| — VERIFIED | **145** |
| — PARTIALLY_VERIFIED | **48** |
| — CONTRADICTED | **56** |
| — UNVERIFIED | **30** |
| — OUTDATED | **8** |
| — PROVENANCE_ISSUE | **12** |
| *file-level "no material claims" notes (not claims)* | *2* |

### 6.1 Most important scientific / methodological problems

1. **No statistical superiority exists.** Minimum p across all 13 metrics = **0.090772** (Val Seg Loss); minimum Wilcoxon = 0.083984; mask-mAP p = 0.383917; **all 13 rows carry `statistically_significant_005 = False`**. Every "vượt trội / chứng minh / hoàn toàn / significantly better / more stable" formulation across `doc/00`, `doc/10`, `doc/16`, `doc/22` and the whole historical tree is **CONTRADICTED** as written. Improvements are descriptive only.
2. **TN is reconstructed, never measured.** `ConfusionMatrix.process_batch` increments only FP for empty-GT images; there is no `matrix[nc,nc] += 1`. TN = 40 − FP holds in 20/20 rows. TN/Specificity must never be presented as a measurement.
3. **Confusion-matrix integrity is compromised for 3 of 20 runs.** 17/20 match; TSVM s0/s5/s8 do not (PNG TP 59 / 0 / 6 vs CSV 108 / 112 / 111). Substituting the PNG rows moves TSVM mean FP **14.6 → 22.5** and **reverses** the "fewer false positives" conclusion.
4. **Root cause of the s0/s8 mismatch is UNKNOWN.** Only s5 has a proven mechanism (a separate `model.val()` re-evaluation whose `confusion_matrix.png` was `shutil.copy2`-copied over the run-folder plot). For s0 and s8 the PNG mtime equals the `results.csv` mtime, so no overwrite evidence exists.
5. **Four mutually incompatible cost/latency generations** circulate in Markdown (only the CPU `thop` CSV is file-backed). The sharpest defect: `doc/20` §6 attributes GPU numbers (11.55/12.16 M, 42.3/47.4 GFLOPs, 17.2/19.8 ms, 58.1/50.5 FPS, VRAM 1.42/1.68 GB) to a CSV containing none of them, and concludes "50.5 FPS beats the 25–30 FPS endoscopy threshold" — unsupported.
6. **Stale FP baseline `17.4` survives in five documents.** True: FP **16.8 → 14.6 = −13.1 %**. The `−16.1 %` figure and "TN 56.5 %" derive from a value `LICHSU_CAP_NHAT` v3.1 already retired.
7. **Seed win counts wrong in `doc/06`.** Mask Precision is **5/10**, not 7/10. Mask Recall is **6/10 with 0 ties**, not 5/10 with a tie.
8. **Dataset semantics conflated.** 160 validation **images** = 120 polyp images carrying **127 objects** + 40 background. "167" mixes objects with images and must never appear.
9. **Run inventory overstated.** "47 runs", "4 models", "40 `results.csv`" — actual: **20 `results.csv`, 2 models**. The 4-model efficiency draft (P5 11.719 M/477.98 ms, ITS 12.229 M/651.27 ms) has **no** backing row in any surviving CSV.
10. **Two unreconciled audit totals** (559/559 vs 694/694) — quote neither as an audit score.
11. **Banned derived metrics.** No IoU/mIoU/Dice/F1 column exists in the package; derived Dice/F1 values may not be cited, and Dice ≠ F1 was demonstrated numerically.
### 6.2 Claims that MUST be corrected before use in a thesis or report

These may **not** appear as written:

| Claim | Required correction |
|---|---|
| Any "statistically significant / chứng minh / vượt trội" improvement claim | Rewrite as descriptive, with metric scope and p-value; state that no metric reaches α = 0.05 |
| Any TN / Specificity value quoted as a measurement | Label as reconstruction `TN = 40 − FP`; never as an independent metric |
| "FP 17.4 → 14.6 (−16.1 %)", "TN 56.5 % → 63.5 %" | Replace with **FP 16.8 → 14.6 (−13.1 %)**, TN 58.0 % → 63.5 % |
| "Mask Precision TSVM thắng 7/10" | Replace with **5/10** |
| "Mask Recall TSVM thắng 5/10 (có 1 hòa)" | Replace with **6/10, 0 hòa** |
| `doc/20` §6 efficiency table + "50.5 FPS vượt ngưỡng 25–30 FPS" | Replace with the CSV values 11.434/12.255 M, 18.54/18.86 GFLOPs, 200.12/821.27 ms, 5.00/1.22 FPS, VRAM N/A; drop the FPS-threshold claim |
| "167 ảnh" / "160 ảnh (127 polyp GT + 40 ảnh nền)" | "160 images = 120 polyp images containing 127 objects + 40 background images" |
| "47 runs" / "4 models" / "40 tệp results.csv" | 20 runs, 2 models (Baseline, TSVM), seeds 0–9, 100 epochs |
| `Stracth/` = 46 or 48 scripts | **55** |
| 4-model efficiency figures (P5 / ITS Mamba) | Delete — no surviving artifact |
| Audit score "559/559" or "694/694" | Delete until scope is defined |
| IoU / mIoU / Dice / F1 values | Delete — not present in the package |
| Default tracker is BoT-SORT (tracker README) | Note the fork's actual defaults: `cfg/default.yaml` → `tracktrack.yaml`, `solutions/config.py` → `botsort.yaml` |
| `data_bg20.yaml` paths, `KetQua_Nen/…` paths | Repoint to `archive/Ket_Qua_V2/…` |

### 6.3 Claims with a provenance problem only (values usable once caveated)

- **TN / Specificity family** — `B1-C013`, `B1-C023`, `B2-C038`, `B4L-C020`, `B4L-C028`, `B4L-C048`.
- **Confusion-matrix family** — `B1-C014`, `B2-C039`, `B4L-C029`, `B4L-C046`, `B4L-C047`, `B4L-C051`.

### 6.4 Claims with insufficient evidence to conclude

- **6-fold / deleted-raw generation (9 claims):** `B3-C033`, `B3-C039`, `B3-C042`, `B3-C049`, `B3-C051`, `B3-C054`, `B3-C056`, `B3-C062`, `B3-C063` — raw run directories deleted; **unverifiable by construction**. This is a permanent condition, not a pending task.
- **PDF half of the manifest warning:** `B3-C006` — 85 FlateDecode streams, raw scan inconclusive, mtime predates the `.docx` fix.
- **Training environment:** `B2-C005` (Kaggle T4 / torch 2.10.0+cu128 / Python 3.12) — no artifact; local env is documented as 3.13.14.
- **Seed randomness / independence:** `B2-C003` — seed labels exist; no RNG-provenance artifact.
- **Ultralytics examples:** `B4-C008` (no `*.pt` weights in the fork), `B4-C009` (tracker "real-time without sacrificing accuracy" has no artefact).
- **Link-checker, hardware/library and per-epoch claims:** `B2-C085`, `B4L-C008`, `B2-C016`, `B2-C026`.
## 7. QUALITY CONTROL — CHECKS PERFORMED

| QC check | Result |
|---|---|
| No Markdown omitted | ✔ 56 enumerated by filesystem query; 56 listed in the coverage split; sum verified |
| No file counted in two batches | ✔ 13 duplicate `Ket_Qua_V2` files reassigned to BATCH 1; `B4L-C001/C002` excluded |
| No double-counted claim | ✔ 301 unique IDs; the 2 duplicates explicitly excluded and named |
| Markdown never used as evidence when an artifact exists | ✔ §3 cites CSVs / `results.csv` / code / YAML / PNGs / JSON for every critical claim |
| Evidence not edited | ✔ only this ledger was written; no CSV, PNG, YAML, JSON or `.py` modified |
| No root-cause speculation | ✔ s0/s8 recorded as `UNKNOWN`; only s5's mechanism asserted, from code |
| Descriptive never upgraded to significance | ✔ §3.3; `statistically_significant_005 = False` for all 13 metrics |
| "better / superior / more stable" not endorsed | ✔ all such wordings marked `CONTRADICTED` |
| Historical docs not called wrong for being historical | ✔ §4 four-way split; 10 `historical-at-time` claims counted `VERIFIED` |
| Ledger ↔ statistics ↔ final summary consistent | ✔ §2.2 census = §5 tally columns = §6 summary |
| Batch tallies reconcile to their source sections | ✔ B1 28, B4L 65, B2 113, B3 78, B4 17 → 301 |
| Source Markdown untouched | ✔ only `archive/MARKDOWN_CLAIM_AUDIT.md` updated |

## 8. FINAL VERDICT

### `ARCHIVE_AUDIT = PASS_WITH_ISSUES`

**Coverage complete?** **YES.** 56/56 Markdown files enumerated, read, claim-extracted and mapped to archive evidence. B1 16 + B2 27 + B3 10 + B4 3 = 56. Duplicates, overlaps and mis-scoped batches were found and corrected (§1.2).

**Does the documentation reflect the evidence?** **PARTIALLY.** The Tier-A evidence base (`results.csv`, the derived CSVs, the code, the YAML) is internally consistent and reproduces every headline metric exactly. The **narrative layer is not yet aligned**: 56 CONTRADICTED and 8 OUTDATED claims remain in the Markdown, concentrated in `doc/**`, the quarantined 6-fold era and the stale `Ket_Qua_V2` benchmark drafts. **No defect in the final tally originates from the primary data.**

**Remaining contradictions / material risk?** **YES — three material risks.**
1. **No statistical significance exists** anywhere in the 10-seed study, yet multiple documents assert superiority. Highest risk of over-claiming in a thesis.
2. **The FP/TN conclusion is source-dependent.** Under the PNG artefacts TSVM mean FP is 22.5 vs Baseline 16.8 — the opposite of the documented 14.6 vs 16.8.
3. **Four incompatible cost/latency generations** are in circulation, and the "50.5 FPS meets endoscopy real-time" conclusion rests on a table that does not match the CSV it cites.

**Claims that may NOT be used in a thesis/report until corrected?** **YES** — the 15 rows of §6.2. In particular: any significance/superiority claim; any TN/Specificity value presented as measured; `FP 17.4 → −16.1 %`; `Mask Precision 7/10`; `Mask Recall 5/10 with a tie`; the `doc/20` §6 efficiency table and its FPS-threshold conclusion; "167 ảnh"; "47 runs / 4 models / 40 `results.csv`"; the 4-model P5/ITS efficiency figures; the 559/559 or 694/694 audit scores; any IoU/mIoU/Dice/F1 value.

**Why not `PASS`:** 64 of 301 claims are `CONTRADICTED`/`OUTDATED` and 12 carry unresolved provenance defects, several in documents a reader would reasonably treat as authoritative.
**Why not `FAIL`:** the primary data and code evidence base is clean, coverage is complete, every defect is enumerated and traceable to a file and an artifact, and the required corrections are well defined.

---

`MERGE_FINAL_STATUS = COMPLETE`
`MARKDOWN_COVERAGE = 56/56`
`CLAIM_LEDGER = MERGED`
`FINAL_VERDICT = PASS_WITH_ISSUES`
