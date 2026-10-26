from pathlib import Path
import hashlib,json,shutil

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'fix_20261026/documentation';BACKUP=OUT/'backups'
changes=json.loads((OUT/'documentation_changes.json').read_text(encoding='utf-8'))
def edit(relative,transform):
    p=ROOT/relative;original=p.read_text(encoding='utf-8');target=BACKUP/relative;target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():shutil.copy2(p,target)
    updated=transform(original);p.write_text(updated,encoding='utf-8')
    changes.append({'path':str(p.resolve()),'before_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'after_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})

def builder(s):
    s=s.replace('    - Tỷ lệ train/val giữ chuẩn 80/20.','    - Phân bổ cuối cùng là 1.040 train / 160 validation; không phải tỷ lệ 80/20 toàn bộ.')
    s=s.replace('    - Cố định random.seed(42) để đảm bảo 100% tính tái lập khoa học.','    - Cố định lựa chọn ảnh nền bằng seed 42; độ khớp nhãn còn cần đối chiếu môi trường OpenCV.')
    s=s.replace('import os\n','import os\nimport argparse\nimport platform\nimport hashlib\n',1)
    s=s.replace('from tqdm import tqdm','''try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        """Progress display is optional; the conversion algorithm is unchanged."""
        return iterable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")''',1)
    start=s.index('def main():')
    end=s.index('    # 2. Đọc danh sách ID gốc',start)
    s=s[:start]+'''def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build BG20 into a NEW directory without changing the canonical dataset or active YAML."
    )
    parser.add_argument("--archive-root", type=Path,
                        default=Path(__file__).resolve().parents[2],
                        help="Archive folder containing train.txt and val.txt")
    parser.add_argument("--source-root", type=Path, default=None,
                        help="Folder containing Kvasir-SEG and normal-cecum (relative to archive if not absolute)")
    parser.add_argument("--output", type=Path, default=Path("generated/Kvasir_YOLO_SEG_BG20_replay"),
                        help="New output folder, relative to archive if not absolute; existing folders are refused")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate inputs and background selection without writing output")
    args = parser.parse_args(argv)
    base_dir = args.archive_root.resolve()

    def archive_path(value):
        return (value if value.is_absolute() else base_dir / value).resolve()

    source_root = archive_path(args.source_root) if args.source_root else base_dir / "Ket_Qua_V2" / "Data Prosessing"
    source_root = source_root.resolve()
    output_dir = archive_path(args.output)
    images_dir = source_root / "Kvasir-SEG" / "images"
    masks_dir = source_root / "Kvasir-SEG" / "masks"
    train_txt_path = base_dir / "train.txt"
    val_txt_path = base_dir / "val.txt"
    cecum_dir = source_root / "normal-cecum"
    canonical_dir = (base_dir / "Ket_Qua_V2" / "Kvasir_YOLO_SEG_BG20").resolve()

    if output_dir == canonical_dir or output_dir.is_relative_to(source_root):
        parser.error("Output must be outside the source tree and must not be the canonical BG20 dataset.")
    if output_dir.exists():
        parser.error(f"Output already exists; choose a NEW folder (nothing was deleted): {output_dir}")
    for label, path in [("Kvasir images", images_dir), ("Kvasir masks", masks_dir),
                        ("train split", train_txt_path), ("validation split", val_txt_path),
                        ("normal-cecum", cecum_dir)]:
        if not path.exists():
            parser.error(f"Missing {label}: {path}")
    logger.info("Nguồn: %s | Đầu ra mới: %s", source_root, output_dir)

'''+s[end:]
    old='''    # 4. Khởi tạo cấu trúc thư mục đầu ra
    if output_dir.exists():
        logger.warning(f"Thư mục {output_dir} đã tồn tại. Tiến hành làm sạch thư mục cũ...")
        shutil.rmtree(output_dir)
        
'''
    assert old in s
    s=s.replace(old,'''    # Validate individual input membership before creating any output.
    for image_id in train_polyp_ids + val_polyp_ids:
        stem = image_id[:-4] if image_id.lower().endswith(".jpg") else image_id
        for folder in (images_dir, masks_dir):
            if not (folder / f"{stem}.jpg").is_file():
                parser.error(f"Missing source file: {folder / (stem + '.jpg')}")
    train_stems = {Path(x).stem for x in train_polyp_ids}
    val_stems = {Path(x).stem for x in val_polyp_ids}
    if len(train_stems) != 880 or len(val_stems) != 120 or train_stems & val_stems:
        parser.error("Split lists must have 880/120 unique, disjoint polyp IDs.")

    if args.dry_run:
        print(json.dumps({
            "status": "DRY_RUN", "source_root": str(source_root), "output_directory": str(output_dir),
            "train_polyp_images": len(train_polyp_ids), "val_polyp_images": len(val_polyp_ids),
            "train_background_images": len(cecum_train), "val_background_images": len(cecum_val),
            "output_created": False, "active_yaml_modified": False,
            "selected_background_names": [p.name for p in selected_cecum],
            "opencv": cv2.__version__, "numpy": np.__version__
        }, ensure_ascii=False, indent=2))
        return

    # 4. Create a fresh output tree. Never delete or merge an existing directory.
    output_dir.mkdir(parents=True, exist_ok=False)
''',1)
    s=s.replace("path: {str(output_dir.resolve()).replace('\\\\', '/')}","path: {output_dir.resolve().as_posix()}")
    start=s.index('    # Cũng xuất 1 bản copy ra root archive để tiện dùng')
    end=s.index('    # 9. Tóm tắt kết quả thành công',start)
    s=s[:start]+'''    # The canonical archive/data_bg20.yaml is intentionally never overwritten.
    environment = {
        "python": platform.python_version(), "opencv": cv2.__version__, "numpy": np.__version__,
        "seed_background": 42, "min_area": 20.0, "epsilon_ratio": 0.002,
        "train_list_sha256": hashlib.sha256(train_txt_path.read_bytes()).hexdigest(),
        "val_list_sha256": hashlib.sha256(val_txt_path.read_bytes()).hexdigest(),
        "source_root": str(source_root), "output_directory": str(output_dir),
        "active_yaml_modified": False,
        "label_reproduction_note": "Byte-identical labels depend on verified inputs and tested implementation/environment; compare before use."
    }
    (output_dir / "reproduction_environment.json").write_text(
        json.dumps(environment, ensure_ascii=False, indent=2), encoding="utf-8"
    )

'''+s[end:]
    return s

def report_builder(s):
    s=s.replace('import os\n','import os\nimport argparse\nfrom pathlib import Path\n',1)
    s=s.replace('WORKSPACE = r"c:\\LeDucLuong\\HK VII\\LuanCuNhan\\DeepLearning\\Test_Mau\\archive"',
                'WORKSPACE = str(Path(__file__).resolve().parents[2])')
    s=s.replace('def main():\n','def _build_historical_report():\n',1)
    old="if __name__ == '__main__':\n    main()"
    assert old in s
    s=s.replace(old,'''def main(argv=None):
    """Historical drafts require explicit opt-in and may never overwrite the current report."""
    parser = argparse.ArgumentParser(description="Historical Markdown report builder (not the current FP32 source).")
    parser.add_argument("--allow-historical-drafts", action="store_true",
                        help="Explicitly build a historical copy; this does not validate its old claims")
    parser.add_argument("--output", type=Path,
                        help="Required NEW .docx destination, never the current report")
    args = parser.parse_args(argv)
    historical = [name for name in MD_FILES
                  if (Path(MD_DIR) / name).is_file()
                  and "HISTORICAL_DRAFT_DO_NOT_BUILD_CURRENT" in
                  (Path(MD_DIR) / name).read_text(encoding="utf-8")[:200]]
    if historical and not args.allow_historical_drafts:
        parser.error("Historical drafts are blocked. Read archive/doc/README.md; use --allow-historical-drafts only for an explicitly historical copy.")
    if args.output is None:
        parser.error("--output is required; this builder no longer writes to the current report by default.")
    output = args.output.resolve()
    protected = {(Path(WORKSPACE) / "Bao_cao" / name).resolve() for name in (
        "CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx",
        "CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong_MoRong_FP32.docx")}
    if output in protected or output.exists() or output.suffix.lower() != ".docx":
        parser.error("Choose a new .docx path outside the two current report files; existing files are refused.")
    output.parent.mkdir(parents=True, exist_ok=True)
    global OUTPUT_PATH
    OUTPUT_PATH = str(output)
    _build_historical_report()


if __name__ == '__main__':
    main()''')
    return s

edit(Path('Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py'),builder)
edit(Path('Stracth/Bao_Cao/build_huit_final_report_from_md.py'),report_builder)
(OUT/'documentation_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
print('Updated support scripts safely')
