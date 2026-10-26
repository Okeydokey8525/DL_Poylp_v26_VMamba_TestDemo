import os
from pathlib import Path

import cv2
import numpy as np
import pytest
import torch

from datasets.kvasir_semantic_dataset import KvasirSemanticDataset


@pytest.fixture
def mock_dataset_dir(tmp_path):
    data_dir = tmp_path / "mock_dataset"
    train_dir = data_dir / "train"
    images_dir = train_dir / "images"
    masks_dir = train_dir / "masks_binary"
    
    images_dir.mkdir(parents=True)
    masks_dir.mkdir(parents=True)
    
    # Create 2 mock samples
    for i in range(2):
        img = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
        mask = np.zeros((32, 32), dtype=np.uint8)
        mask[10:20, 10:20] = 255
        
        cv2.imwrite(str(images_dir / f"sample_{i}.jpg"), img)
        cv2.imwrite(str(masks_dir / f"sample_{i}.png"), mask)
        
    return data_dir

def test_dataset_no_transform(mock_dataset_dir):
    dataset = KvasirSemanticDataset(data_dir=mock_dataset_dir, split="train", transform=None)
    assert len(dataset) == 2
    
    image, mask = dataset[0]
    
    # Check types
    assert isinstance(image, torch.Tensor)
    assert isinstance(mask, torch.Tensor)
    
    # Check shapes
    assert image.shape == (3, 32, 32)
    assert mask.shape == (1, 32, 32)
    
    # Check values
    assert image.dtype == torch.float32
    assert mask.dtype == torch.float32
    assert image.max() <= 1.0
    assert image.min() >= 0.0
    assert mask.max() <= 1.0
    assert mask.min() >= 0.0
    
    # Check mask values are exactly 0.0 or 1.0
    unique_vals = torch.unique(mask)
    assert torch.all(torch.isin(unique_vals, torch.tensor([0.0, 1.0])))


def test_dataset_with_transform(mock_dataset_dir):
    # Dummy Albumentations-like transform
    class DummyTransform:
        def __call__(self, image, mask):
            # Simulate a transform that returns tensors but doesn't normalize
            img_tensor = torch.from_numpy(image.transpose(2, 0, 1)).float()
            mask_tensor = torch.from_numpy(mask).unsqueeze(0).float()
            return {"image": img_tensor, "mask": mask_tensor}
            
    dataset = KvasirSemanticDataset(data_dir=mock_dataset_dir, split="train", transform=DummyTransform())
    image, mask = dataset[0]
    
    assert isinstance(image, torch.Tensor)
    assert isinstance(mask, torch.Tensor)
    assert image.shape == (3, 32, 32)
    assert mask.shape == (1, 32, 32)
    
    # Since our DummyTransform didn't normalize, we expect max values to be > 1.0 for image
    # but the Dataset class automatically scales mask if it's > 1.0
    assert image.max() > 1.0
    assert mask.max() <= 1.0
    assert mask.min() >= 0.0
