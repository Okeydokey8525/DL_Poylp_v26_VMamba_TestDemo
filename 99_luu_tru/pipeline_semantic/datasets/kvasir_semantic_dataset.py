import os
from pathlib import Path

import cv2
import numpy as np
import torch
from torch.utils.data import Dataset


class KvasirSemanticDataset(Dataset):
    """
    PyTorch Dataset for Kvasir-SEG Semantic Segmentation.
    Expects directory structure:
    data_dir/
      split/
        images/
        masks_binary/
    """
    def __init__(self, data_dir, split="train", transform=None):
        self.data_dir = Path(data_dir)
        self.split = split
        self.transform = transform
        
        self.images_dir = self.data_dir / split / "images"
        self.masks_dir = self.data_dir / split / "masks_binary"
        
        if not self.images_dir.exists():
            raise FileNotFoundError(f"Images directory not found: {self.images_dir}")
        if not self.masks_dir.exists():
            raise FileNotFoundError(f"Masks directory not found: {self.masks_dir}")

        # Gather file paths
        self.image_paths = sorted([p for p in self.images_dir.iterdir() if p.is_file()])
        self.samples = []
        for img_path in self.image_paths:
            stem = img_path.stem
            # Mask is always saved as PNG from the preparation script
            mask_path = self.masks_dir / f"{stem}.png"
            if not mask_path.exists():
                raise FileNotFoundError(f"Corresponding mask not found for {img_path.name}")
            self.samples.append((img_path, mask_path))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, mask_path = self.samples[idx]
        
        # Read image
        image = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Failed to read image: {img_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Read mask
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        if mask is None:
            raise ValueError(f"Failed to read mask: {mask_path}")

        # Apply Albumentations transform if provided
        if self.transform is not None:
            transformed = self.transform(image=image, mask=mask)
            image = transformed["image"]
            mask = transformed["mask"]
            
            # If transform doesn't return tensors (e.g. ToTensorV2 was not used)
            if not isinstance(image, torch.Tensor):
                # We assume the user handled normalization. We just convert to tensor [C, H, W]
                if image.ndim == 3:
                    image = torch.from_numpy(image.transpose(2, 0, 1).copy()).float()
                else:
                    image = torch.from_numpy(image.copy()).float()
            
            if not isinstance(mask, torch.Tensor):
                mask = torch.from_numpy(mask.copy()).float()
                if mask.ndim == 2:
                    mask = mask.unsqueeze(0)
                elif mask.ndim == 3 and mask.shape[-1] == 1:
                    mask = mask.permute(2, 0, 1)

            # Ensure mask values are 0/1 (they might be 0/255 if transform didn't normalize)
            # If max value is > 1.0, we assume it's still 0/255
            if mask.max() > 1.0:
                mask = mask / 255.0
                
        else:
            # No transform: convert directly to float32 tensors [0, 1]
            image = image.astype(np.float32) / 255.0
            image = torch.from_numpy(image.transpose(2, 0, 1))
            
            mask = mask.astype(np.float32) / 255.0
            mask = torch.from_numpy(mask).unsqueeze(0)

        return image, mask
