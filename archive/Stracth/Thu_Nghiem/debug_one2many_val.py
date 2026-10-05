import sys, torch
repo_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\ultralytics_Topology-Shape-aware VMamba"
if repo_path not in sys.path:
    sys.path.insert(0, repo_path)

from ultralytics.models.yolo.segment import SegmentationValidator
from ultralytics.nn import autobackend
from ultralytics.data.utils import check_det_dataset

def main():
    ckpt_path = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\KetQua_Nen\Kvasir_BG20_YOLO26s_seg_TSVM_s5_w2\weights\best.pt"
    data_yaml = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Test_Mau\archive\data_bg20.yaml"

    val = SegmentationValidator(args=dict(model=ckpt_path, data=data_yaml, device="cpu", batch=2, imgsz=640, end2end=False, conf=0.001, workers=0))
    val.device = torch.device("cpu")
    val.args.workers = 0
    val.data = check_det_dataset(data_yaml, split="val")
    val.dataloader = val.get_dataloader(val.data["val"], batch_size=2)
    batch = next(iter(val.dataloader))
    batch = val.preprocess(batch)

    model = autobackend.AutoBackend(model=ckpt_path, device="cpu", fuse=False)
    val.init_metrics(model)
    head = model.model.model[-1]
    head.end2end = False
    model.end2end = False
    val.end2end = False
    val.names = model.names
    val.nc = len(model.names)

    print(f"model.end2end: {model.end2end}, head.end2end: {head.end2end}, val.end2end: {val.end2end}")

    preds = model(batch["img"])
    print(f"model output type: {type(preds)}")
    if isinstance(preds, (list, tuple)):
        for idx, item in enumerate(preds):
            print(f"  preds[{idx}] shape: {item.shape if hasattr(item, 'shape') else type(item)}")

    post_preds = val.postprocess(preds)
    print(f"post_preds len: {len(post_preds)}")
    for i, p in enumerate(post_preds):
        bb = p["bboxes"]
        mk = p["masks"]
        cf = p["conf"]
        print(f"  img {i}: bboxes={bb.shape}, masks={mk.shape}, max_conf={cf.max().item() if len(cf) else None}")

if __name__ == "__main__":
    main()
