import os
from pathlib import Path
import cv2
import numpy as np
import pytest

from data_prep.prepare_kvasir_semantic import calculate_sha256, find_files, binarize_mask

@pytest.fixture
def temp_workspace(tmp_path):
    # Setup temporary directory structure for tests
    img_dir = tmp_path / "images"
    mask_dir = tmp_path / "masks"
    img_dir.mkdir()
    mask_dir.mkdir()
    return tmp_path, img_dir, mask_dir

def test_calculate_sha256(temp_workspace):
    tmp_path, _, _ = temp_workspace
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello world")
    
    # known sha256 for "hello world"
    expected_hash = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert calculate_sha256(test_file) == expected_hash

def test_find_files(temp_workspace):
    _, img_dir, _ = temp_workspace
    (img_dir / "img1.jpg").touch()
    (img_dir / "img2.png").touch()
    (img_dir / "ignore.txt").touch()

    files = find_files(img_dir, {".jpg", ".png"})
    assert len(files) == 2
    assert "img1" in files
    assert "img2" in files
    assert files["img1"].name == "img1.jpg"

def test_find_files_duplicate_stem(temp_workspace):
    _, img_dir, _ = temp_workspace
    (img_dir / "img1.jpg").touch()
    (img_dir / "img1.png").touch()

    with pytest.raises(ValueError, match="Duplicate stem found"):
        find_files(img_dir, {".jpg", ".png"})

def test_binarize_mask(temp_workspace):
    tmp_path, _, _ = temp_workspace
    mask_path = tmp_path / "dummy_mask.png"
    out_path = tmp_path / "out_mask.png"
    
    # Create dummy mask with values 0, 100, 200
    dummy_mask = np.zeros((10, 10), dtype=np.uint8)
    dummy_mask[0:5, 0:5] = 100 # Should become 0
    dummy_mask[5:10, 5:10] = 200 # Should become 255
    cv2.imwrite(str(mask_path), dummy_mask)

    fg_pixels, total_pixels, components, out_mask = binarize_mask(mask_path, out_path)
    
    assert total_pixels == 100
    assert fg_pixels == 25  # 5x5 block
    assert components == 1  # 1 foreground component
    
    # Check values
    unique_vals = np.unique(out_mask)
    assert len(unique_vals) == 2
    assert 0 in unique_vals
    assert 255 in unique_vals
    
    # 100 should have become 0, 200 should have become 255
    assert out_mask[2, 2] == 0
    assert out_mask[7, 7] == 255
