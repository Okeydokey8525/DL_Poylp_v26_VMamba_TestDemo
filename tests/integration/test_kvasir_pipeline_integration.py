import os
import subprocess
from pathlib import Path
import pytest
import cv2
import numpy as np

@pytest.fixture
def dummy_source_data(tmp_path):
    img_dir = tmp_path / "images"
    mask_dir = tmp_path / "masks"
    img_dir.mkdir()
    mask_dir.mkdir()
    
    # Create 3 dummy samples with unique masks to prevent hash duplicate errors
    stems = ["sample_1", "sample_2", "sample_3"]
    for i, stem in enumerate(stems):
        img = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
        mask = np.zeros((64, 64), dtype=np.uint8)
        mask[20:40, 20+i:40+i] = 200  # Shift the mask slightly to make it unique
        
        cv2.imwrite(str(img_dir / f"{stem}.jpg"), img)
        cv2.imwrite(str(mask_dir / f"{stem}.png"), mask)
        
    train_list = tmp_path / "train.txt"
    val_list = tmp_path / "val.txt"
    
    train_list.write_text("sample_1\nsample_2\n")
    val_list.write_text("sample_3\n")
    
    return img_dir, mask_dir, train_list, val_list

def test_pipeline_dummy_data(dummy_source_data, tmp_path):
    img_dir, mask_dir, train_list, val_list = dummy_source_data
    out_dir = tmp_path / "output_dataset"
    
    script_path = Path("data_prep/prepare_kvasir_semantic.py").resolve()
    
    cmd = [
        "python", str(script_path),
        "--images-dir", str(img_dir),
        "--masks-dir", str(mask_dir),
        "--train-list", str(train_list),
        "--val-list", str(val_list),
        "--output-dir", str(out_dir),
        "--expected-train-count", "2",
        "--expected-val-count", "1"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    
    # Check outputs
    assert (out_dir / "train" / "images" / "sample_1.jpg").exists()
    assert (out_dir / "val" / "masks_binary" / "sample_3.png").exists()
    assert (out_dir / "dataset_summary.json").exists()
    assert (out_dir / "split_manifest.csv").exists()
    assert (out_dir / "qa" / "qa_report.md").exists()

@pytest.mark.skipif(
    not os.environ.get("KVASIR_IMAGES_DIR") or not os.environ.get("KVASIR_MASKS_DIR"),
    reason="Real data paths not provided in environment variables"
)
def test_pipeline_real_data(tmp_path):
    img_dir = os.environ["KVASIR_IMAGES_DIR"]
    mask_dir = os.environ["KVASIR_MASKS_DIR"]
    train_list = os.environ["KVASIR_TRAIN_LIST"]
    val_list = os.environ["KVASIR_VAL_LIST"]
    
    out_dir = tmp_path / "Kvasir_Semantic_880_120"
    
    script_path = Path("data_prep/prepare_kvasir_semantic.py").resolve()
    
    cmd = [
        "python", str(script_path),
        "--images-dir", img_dir,
        "--masks-dir", mask_dir,
        "--train-list", train_list,
        "--val-list", val_list,
        "--output-dir", str(out_dir),
        "--expected-train-count", "880",
        "--expected-val-count", "120"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed on real data: {result.stderr}"
    
    # Check if exact number of files exists
    train_images = list((out_dir / "train" / "images").glob("*"))
    val_images = list((out_dir / "val" / "images").glob("*"))
    
    assert len(train_images) == 880
    assert len(val_images) == 120
