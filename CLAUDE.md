# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a thesis research repo (documentation is mostly in Vietnamese). It integrates VMamba into YOLO26-seg for colorectal polyp instance segmentation on the Kvasir **BG20** dataset. Training runs on Kaggle (Tesla T4). This repo holds the custom Ultralytics fork, the experiment artifacts, the analysis/audit scripts, and the thesis documentation. It is not a packaged application: there is no build step and no dependency manifest.

## Source-of-truth rules (mandatory)

These rules come from `README.md` and `CURRENT_PROJECT_STATUS.md`, and they override convenience:

- Trust sources in this order: `CURRENT_PROJECT_STATUS.md` → raw CSV / artifact / config / source → historical docs. When docs and raw data disagree, raw data wins.
- **Never edit raw CSVs, checkpoints or original run plots** to make reports match. Never invent numbers. Analysis scripts must write to a *new* output directory.
- Label every claim as **Current/Verified**, **Historical** or **NOT VERIFIED IN REPOSITORY**. Code that exists only on local/Kaggle (e.g. the P3 `C3k2VSS` / `yolo26-vmamba-p3-seg.yaml` direction) is NOT VERIFIED until it has been pushed.
- Don't call a module "topology-aware" just because of its name. Don't call a difference significant when the stats don't support it (e.g. Baseline vs TSVM mask mAP@50-95: p = 0.3839).
- Before large tasks, read `archive/doc/AI_WORK_OPTIMIZATION_RULE.md` and `archive/doc/nguyen-tac-lam-viec-dai.md`. Their core points: classify the task size first, don't read the whole repo, only spawn subagents for truly independent parallel work, and state your certainty level ("Đã xác nhận / Suy luận / Chưa xác minh").
- Sync flow: local/Kaggle code → verify → push source/config/artifact → update `CURRENT_PROJECT_STATUS.md` → update README and the docs in `archive/doc/`.

## Architecture (big picture)

- **Custom Ultralytics fork**: `archive/ultralytics_Topology-Shape-aware VMamba/` (note the spaces in the path). **Never use `ultralytics` from PyPI.** The fork's `Segment26` head (in `nn/modules/head.py`) adds a one-to-many / one-to-one dual branch, and `fuse()` removes the one2many head. That fuse/head-selection behavior is the subject of `archive/doc/17_SU_CO_FUSE_...md` and of the seed-audit scripts.
  - TSVM model: `cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml`. It puts `C2TSVMamba` at **layer 10** (top of the backbone, P5, 20×20 at 640 input), and the `Segment26` head consumes P3/P4/P5 (layers 16/19/22).
  - Module code: `nn/modules/topology_shape_vmamba.py` (SS2D, ShapeAwareBranch, DirectionalShapeExtractor, TopologyShapeGate, TSVMamba, C2TSVMamba). New modules must be exported in `nn/modules/__init__.py` and registered in `parse_model` in `nn/tasks.py`.
  - Scripts load the fork by putting it on `sys.path` or binding it through `importlib` as the `ultralytics` package (see `bootstrap` in `scripts/analysis/diagnose_saved_heads.py`).
- **Results**: `archive/Ket_Qua_V2/`
  - `KetQua_Nen/`: original per-seed runs (`results.csv` is the only source of metrics). Treat it as read-only.
  - `KQ_Nen_DX_10seed/`: the 10-seed analysis package (Baseline, TSVM, P5 Attention-VMamba, ITSMamba; IAVM has only 7 seeds and must not be mixed in). Its raw sources are `01_raw_analysis/raw_10seeds_*.csv`.
  - `Kvasir_YOLO_SEG_BG20/`: dataset metadata. Train has 1040 images (880 polyp + 160 background); val has 160 images (120 polyp with 127 instances, plus 40 normal-cecum backgrounds with **empty** label files).
- **Seed audit tooling**: `scripts/analysis/verify_seed_evaluation.py` audits the saved CSVs. The best epoch is the one with max **Mask mAP50-95**, not mAP50. It also re-evaluates checkpoints across the arms `many/one × fused/unfused`, each in a fresh subprocess. A missing label file is rejected, never treated as background.
- **Kaggle retrain kit**: the old `Check_error/bảng v2/` kit was removed (10/10/2026). Its FP32 checkpoint patch lives on in the sibling project `../DL_Poylp_v26_VMamba_TestDemo_V2/` (`03_ma_nguon/PATCH_FP32.md`), which is the current retrain pipeline (baseline / TSVM / TSVM-LN × seeds 0–9). Root cause of the TSVM seed 0/5/8 checkpoint collapse: `output/BaoCaoKetQua/BAO_CAO_SU_CO_PHINH_SO_TSVM_SEED_0_5_8.md` (FP16 overflow of layer-10 BatchNorm stats, not `fuse()`).
- **Secondary semantic-seg pipeline** (for U-Net/PraNet-style work, *not* the main YOLO BG20 pipeline): `data_prep/prepare_kvasir_semantic.py` → `datasets/kvasir_semantic_dataset.py` (`KvasirSemanticDataset`), with output in `datasets/Kvasir_Semantic_880_120/`. `implementation_plan.md`, `task.md` and `walkthrough.md` describe only this pipeline.
- `archive/doc/` holds the knowledge base (technical dossiers 00–24 and `LICHSU_CAP_NHAT.md`). `archive/doc/21_HUONG_DAN_BAN_GIAO_AI_MOI_...md` and `23_MOI_TRUONG_THIET_LAP_VA_TAI_CHAY.md` cover handoff and environment setup.

## Commands

Run everything from the repo root, because the tests import `data_prep.*` and `datasets.*` as top-level packages.

```powershell
$env:PYTHONIOENCODING = "utf-8"              # required for Vietnamese console output

python -m pytest tests                        # all tests (test_kvasir_semantic_dataset.py needs torch)
python -m pytest tests --ignore=tests/unit/test_kvasir_semantic_dataset.py   # without torch
python -m pytest tests/unit/test_verify_seed_evaluation.py              # one file (no ML runtime needed)
python -m pytest tests/unit/test_prepare_kvasir_semantic.py::test_calculate_sha256   # single test

# Seed audit: CSV-only, or full re-evaluation (needs torch + the fork; normally run on Kaggle GPU)
python scripts/analysis/verify_seed_evaluation.py --audit-only --runs-root <runs> --dataset-root <BG20> --out <new_dir>
python scripts/analysis/verify_seed_evaluation.py --runs-root <runs> --dataset-root <BG20> --out <new_dir> --seeds 0 5 8

# Semantic dataset prep (secondary pipeline)
python data_prep/prepare_kvasir_semantic.py --images-dir <img> --masks-dir <mask> --train-list train.txt --val-list val.txt --output-dir datasets/Kvasir_Semantic_880_120
```

The analysis environment used Python 3.13 with pandas/numpy/scipy/matplotlib/seaborn/pillow. The integration and dataset tests also need `opencv-python` and `torch`. A local venv `.venv-seed-audit/` exists for the seed-audit work.

## Gotchas

- Many older scripts (`analyze_runs.py`, `analyze_runs_p1.py`, and generators under `archive/`) hardcode absolute paths from another machine (`c:\LeDucLuong\...`), sometimes with a wrong `archive/KQ_Poylp` or missing `Ket_Qua_V2/` segment. Fix the path variables before running them (see doc 23 and `archive/doc/24_DANH_SACH_DUONG_DAN_HONG.md`).
- Old names such as `archive/Ket_Qua/`, `archive/KQ_Poylp/` and `archive/Kvasir_YOLO_SEG/` are not the current layout.
- `*.pt`/`*.pth` weights and `runs/` are gitignored, so checkpoints usually live only on Kaggle/local.
- Thesis deliverables live under `output/`: `output/tien_xu_ly/` (chapter 3 preprocessing, figures and the code that builds them) and `output/BaoCaoKetQua/` (result reports, the FP16 incident report, the hand-off docs for the team lead). Reusable tools stay in `scripts/` at the repo root.
