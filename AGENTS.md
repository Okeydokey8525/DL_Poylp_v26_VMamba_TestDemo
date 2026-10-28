# Repository Guidelines

## Project Structure & Module Organization
This research repository compares YOLO26s-seg with C2TSVMamba (TSVM FP32) for polyp segmentation. Read `NGU_CANH_DU_AN.md`, `CLAUDE.md`, and `00_tai_lieu_tong_quan/00_README.md` before contributing.

- `00_tai_lieu_tong_quan/`: reference documentation, analysis scripts, and generated CSV tables in `bang/`.
- `01_du_lieu/`: BG20 images, labels, splits, and preprocessing scripts.
- `02_ma_nguon/`: Ultralytics fork, model YAMLs, module tests, and Kaggle notebooks. TSVM implementation: `ultralytics_TSVM_FP32/nn/modules/topology_shape_vmamba.py`.
- `03_ket_qua_huan_luyen/`, `05_so_sanh_mo_hinh_khac/`: training artifacts and checkpoints; `04_phan_tich_20seed/`: statistical analysis and benchmarks.
- `06_bao_cao/`: thesis chapters, figure scripts, and exported figures; `08_du_lieu_thuc_te/`: external-dataset evaluation.
- `07_kiem_toan_va_sua/`, `99_luu_tru/`: preserved audit evidence and historical experiments.

## Build, Test, and Development Commands
Run from the repository root. There is no repository-wide build or dependency manifest. Analysis uses NumPy, pandas, SciPy, Pillow, PyYAML, and Matplotlib; model operations additionally require PyTorch and fork dependencies. The documented GPU interpreter is `C:\venv_kl_gpu\Scripts\python.exe`.

```powershell
python 00_tai_lieu_tong_quan/scripts/tinh_lai_so_lieu.py --seeds 10
python 06_bao_cao/hinh/scripts/ve_hinh.py --chi h01 r01
python -m unittest discover -s 02_ma_nguon/ultralytics_TSVM_FP32/tests -p "test_topology_shape_vmamba.py"
```

These regenerate 10-seed tables, export selected figures, and run module tests, respectively. Add `--torch` to the analysis command for checkpoint/model checks. Regeneration writes derived artifacts; review their diffs.

## Coding Style & Naming Conventions
Use four-space Python indentation, `snake_case` functions/files, and `PascalCase` model classes. Follow neighboring code and numbered Vietnamese directory/chapter names. No shared formatter or linter configuration is present. Preserve figure IDs such as `h01`; consult `06_bao_cao/hinh/README.md` for export conventions.

## Testing Guidelines
The fork uses `unittest`, with `test_*.py` files and `test_*` methods. No coverage threshold is configured. For model changes, check shapes, finite outputs, gradients, and baseline integrity. For analysis changes, reconcile generated tables with source run CSVs and inspect affected figures. Record commands, environment, and unverified checks.

## Commit & Pull Request Guidelines
History uses short descriptive Vietnamese and English subjects; no enforced prefix exists. Keep commits focused. PR descriptions should explain changes, affected scripts/artifacts, validation, and linked issues when applicable; attach figure previews for visual changes. Commit to `Okeydokey` only when authorized; push only when requested.

## Research Integrity & Agent Instructions
Communicate with the owner in Vietnamese. Preserve datasets, checkpoints, audit evidence, and archives. Record relocations in `PATH_MAP.md` and `PATH_MAP.csv`. Keep credentials out of Git. Use seeds 0–9 for current thesis reporting; label 20-seed comparisons separately. Trace claims to source tables, distinguish validation from testing, and avoid unsupported statistical or topology claims.
