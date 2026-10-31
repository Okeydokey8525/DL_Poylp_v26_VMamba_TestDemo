# Repository Guidelines

Last updated: 29/10/2026. Thesis deadline: 08/11/2026.

## Project Structure & Module Organization
This research repository compares YOLO26s-seg (Baseline) with YOLO26s-seg + C2TSVMamba (TSVM FP32) for polyp segmentation (HUIT thesis CNTT_KLCN182). Read these before contributing, in order:
1. `NGU_CANH_DU_AN.md`: context, verified results, current status.
2. `CLAUDE.md`: mandatory rules and commands.
3. `00_tai_lieu_tong_quan/00_README.md`: source-of-truth overview.

`HUONG_DAN_LAM_VIEC_VOI_CLAUDE.md` describes the owner's working style and the history of the work.

- `00_tai_lieu_tong_quan/`: source of truth. Reference docs (`00`–`14`), analysis scripts in `scripts/`, generated CSV tables in `bang/` (20 seeds; `bang/10seed/` is comparison only).
- `01_du_lieu/`: BG20 images, labels, the 880/120 split (provided by the Kvasir-SEG authors), and preprocessing scripts.
- `02_ma_nguon/`: Ultralytics 8.4.127 fork, model YAMLs, module tests, and Kaggle notebooks (ablation notebook in `notebook_kaggle/ablation/`). TSVM implementation: `ultralytics_TSVM_FP32/nn/modules/topology_shape_vmamba.py`.
- `03_ket_qua_huan_luyen/`: training artifacts.
  - Main runs: `Baseline_YOLO26s_seg/`, `TSVM_FP32/` (seeds 0–19).
  - Ablation runs (seeds 0–4, all 15 complete; summarised in `bang/17_*.csv` by `scripts/tinh_ablation.py`, report section 6.6): `Vmamba_only/`, `Shape_only/`, `No_guidance/`.
- `04_phan_tich_20seed/`: older statistical package and CPU benchmarks.
- `05_so_sanh_mo_hinh_khac/`: PraNet and U-Net checkpoints (20 seeds each).
- `06_bao_cao/`: thesis material.
  - `md_bao_cao/`: one markdown file per chapter (Mở đầu, Ch.1–6, references); `_KIEM_TRA/` holds review notes.
  - `hinh/`: figures and the scripts that draw them.
  - `slide/`: defense slide plan.
  - Word templates.
- `08_du_lieu_thuc_te/`: external-dataset evaluation (CVC-ClinicDB, CVC-ColonDB, ETIS, PolypGen).
- `07_kiem_toan_va_sua/`, `99_luu_tru/`: preserved audit evidence and historical experiments. Read only.

## Build, Test, and Development Commands
Run from the repository root. There is no build or dependency manifest.
- Analysis uses NumPy, pandas, SciPy, Pillow, PyYAML, and Matplotlib.
- Model operations also require PyTorch and the fork's dependencies.
- The GPU interpreter is `C:\venv_kl_gpu\Scripts\python.exe` (short path because of the Windows 260-character limit).

```powershell
python 00_tai_lieu_tong_quan/scripts/tinh_lai_so_lieu.py            # 20-seed tables -> bang/
python 06_bao_cao/hinh/scripts/ve_hinh.py --chi h01 r01              # selected figures (20 seeds)
C:\venv_kl_gpu\Scripts\python.exe 00_tai_lieu_tong_quan/scripts/do_flops_gpu.py   # FLOPs + GPU latency
python -m unittest discover -s 02_ma_nguon/ultralytics_TSVM_FP32/tests -p "test_topology_shape_vmamba.py"
```

Notes on these commands:
- Add `--torch` to the analysis command for checkpoint and model checks.
- Use `--seeds 10` only for the 10-seed comparison set.
- Regeneration writes derived artifacts, so review their diffs.
- GPU latency on this laptop depends on temperature. Report ratios between the two models, not absolute milliseconds.

## Coding Style & Naming Conventions
- Python: four-space indentation, `snake_case` functions and files, `PascalCase` model classes.
- Follow neighboring code and the numbered Vietnamese directory and chapter names. No formatter or linter is configured.
- Keep figure IDs such as `h01`; see `06_bao_cao/hinh/README.md` for export conventions.
- Report text:
  - decimal comma (`0,7189`);
  - IEEE references numbered by first citation (57 entries in `08_TAI_LIEU_THAM_KHAO.md` since the 30/10/2026 trim from 80; adding a reference means renumbering every later one).

## Testing Guidelines
The fork uses `unittest`, with `test_*.py` files and `test_*` methods. No coverage threshold is configured.
- **Model changes:** check shapes, finite outputs, gradients, and baseline integrity.
- **Analysis changes:** reconcile generated tables with the source `results.csv` files and inspect the affected figures.
- Record the commands and environment used, and any checks that were not verified.

## Commit & Pull Request Guidelines
History uses short, descriptive Vietnamese or English subjects; no prefix is enforced. Keep commits focused.
- **PR descriptions:** explain the changes, the affected scripts and artifacts, how they were validated, and linked issues when applicable. Attach figure previews for visual changes.
- **Branch and push:** commit to `Okeydokey` only when the owner authorizes it. Push only when asked.

## Research Integrity & Agent Instructions
**Communication and workflow**
- Communicate with the owner in Vietnamese.
- "chưa chỉnh gì / đang hỏi đáp" means discuss and plan only; do not edit files.
- For large tasks, present a plan and wait for explicit approval.
- For batch work, make a small sample first.

**Reporting results**
- Report **20 seeds (0–19)**. The 10-seed set is for comparison only.
- Primary endpoint: mask mAP50–95. Δ = +0,0043, p = 0,061, 13/20 seeds. This is not significant, so write "xu hướng" (trend) and never "vượt trội" (superior).
- Trace every number to a CSV or script; otherwise write "chưa xác minh" (not verified).
- Distinguish validation from testing; there is no separate test set.
- Do not infer TN = 40 − FP.
- Do not derive Dice from mAP.
- Do not claim topology gains; use only the measured numbers in `14_CHI_SO_TOPOLOGY.md`.

**Files and secrets**
- Preserve datasets, checkpoints, audit evidence, and archives.
- Record relocations in `PATH_MAP.md` and `PATH_MAP.csv`.
- Keep credentials out of Git. Never read `..\Ung_Dung\polypweb\GhiChu.txt`.
- Ask before downloading files or running `kaggle kernels push`.

**Scope**
- Keep AV, AVF, and ITSVM (`99_luu_tru/thu_nghiem_ket_hop/`) out of the report.
