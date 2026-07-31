from datasets.kvasir_semantic_dataset import KvasirSemanticDataset

try:
    dataset = KvasirSemanticDataset(
        data_dir="datasets/Kvasir_Semantic_880_120",
        split="train",
        transform=None,
    )
    
    sample = dataset[0]
    image, mask = sample # the __getitem__ returns a tuple (image, mask)
    
    print("Dataset size:", len(dataset))
    print("Image shape:", image.shape)
    print("Image dtype:", image.dtype)
    print("Image range:", image.min().item(), "đến", image.max().item())
    print("Mask shape:", mask.shape)
    print("Mask dtype:", mask.dtype)
    print("Mask values:", mask.unique())
    print("Filename:", dataset.image_paths[0].name)
except Exception as e:
    print(f"Error: {e}")

try:
    val_dataset = KvasirSemanticDataset(
        data_dir="datasets/Kvasir_Semantic_880_120",
        split="val",
        transform=None,
    )
    print("Validation dataset size:", len(val_dataset))
except Exception as e:
    print(f"Error loading val: {e}")
