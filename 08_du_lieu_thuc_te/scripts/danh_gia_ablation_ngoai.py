"""Chạy ba biến thể tách thành phần (ablation) trên dữ liệu ngoài, chỉ suy luận.

Mục đích: kiểm chứng (thăm dò) giả thuyết của phản biện II.1, "nhánh hình dạng quá khớp với Kvasir", bằng cách đo
tỉ lệ bỏ sót polyp của từng biến thể trên CVC-ClinicDB và CVC-ColonDB.
- Vmamba_only: chỉ nhánh SS2D, không có nhánh hình dạng.
- Shape_only: chỉ nhánh hình dạng, không có SS2D.
- No_guidance: cả hai nhánh, bỏ cổng.

Giao thức giống hệt danh_gia_du_lieu_ngoai.py (dùng lại hàm của script đó và của danh_gia_pixel.py):
imgsz 640, conf 0,25, iou 0,7, retina_masks=True, half=False; gộp mọi mặt nạ của ảnh thành một.

Kết quả từng lượt ghi vào ../bang/tung_luot_ablation/<bộ>_<biến thể>_s<seed>.csv (cùng cột với bang/tung_luot/).
Ghi riêng thư mục vì ablation chỉ có 10 seed; nếu ghi chung, summarize() của danh_gia_du_lieu_ngoai.py sẽ bỏ qua
bảng 20 seed. Chạy lại sẽ bỏ qua lượt đã có. Không tổng hợp ở đây (tổng hợp làm sau, không cần GPU).

Chạy (cần GPU, dữ liệu ở DoAnTotNghiepV4/Dataset/, checkpoint ở 03_ket_qua_huan_luyen/):
    C:\\venv_kl_gpu\\Scripts\\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_ablation_ngoai.py --kiem-tra   # chỉ kiểm tra file
    C:\\venv_kl_gpu\\Scripts\\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_ablation_ngoai.py --doi-chieu  # đối chiếu môi trường
    C:\\venv_kl_gpu\\Scripts\\python.exe 08_du_lieu_thuc_te/scripts/danh_gia_ablation_ngoai.py              # chạy đủ 3 × 10 × 2
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import pandas as pd
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import danh_gia_du_lieu_ngoai as ng  # noqa: E402  (load_set, SETS, dg)

dg = ng.dg
RUNS = ng.REPO / "03_ket_qua_huan_luyen"
OUT = ng.BANG / "tung_luot_ablation"

# Tên thư mục biến thể khác nhau giữa các máy (No_guidance hoặc Shape_VMamba_no_guidance): thử lần lượt.
VARIANTS = {
    "abl_vmamba_only": (["Vmamba_only"], "Kvasir_BG20_YOLO26s_seg_ABL_vmamba_only_s{s}_w2"),
    "abl_shape_only": (["Shape_only"], "Kvasir_BG20_YOLO26s_seg_ABL_shape_only_s{s}_w2"),
    "abl_no_guidance": (["No_guidance", "Shape_VMamba_no_guidance"],
                        "Kvasir_BG20_YOLO26s_seg_ABL_shape_vmamba_no_guidance_s{s}_w2"),
}


def weights(variant, s):
    dirs, run = VARIANTS[variant]
    for d in dirs:
        p = RUNS / d / run.format(s=s) / "weights" / "best.pt"
        if p.exists():
            return p
    return None


def kiem_tra(args):
    ok = True
    for v in args.variants:
        for s in args.seeds:
            p = weights(v, s)
            if p is None or p.stat().st_size < 1_000_000:
                print(f"THIẾU  {v} seed {s}")
                ok = False
    for key in args.sets:
        _, img_dir, mask_dir, n = ng.SETS[key]
        if not (img_dir.is_dir() and mask_dir.is_dir()):
            print(f"THIẾU  dữ liệu {key}: {img_dir}")
            ok = False
    print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "KHÔNG CÓ")
    ok = ok and torch.cuda.is_available()
    print("KIỂM TRA:", "ĐỦ, có thể chạy" if ok else "CHƯA ĐỦ, xem các dòng THIẾU ở trên")
    return ok


def doi_chieu(dev):
    """Chạy lại TSVM seed 0 trên CVC-ClinicDB, so với bang/tung_luot/ để chắc môi trường cho kết quả giống lần trước."""
    ref = ng.LUOT / "clinicdb_tsvm_s0.csv"
    w = dg.MODELS["tsvm"][1](0)
    if not (ref.exists() and w.exists()):
        print("Bỏ qua đối chiếu: thiếu", ref if not ref.exists() else w)
        return
    items = ng.load_set("clinicdb")
    preds = dg.predict_yolo(w, items, dev)
    old = pd.read_csv(ref, encoding="utf-8-sig").set_index("image").pred_px
    new = pd.Series({it["name"]: int(p.sum()) for it, p in zip(items, preds)})
    lech = (old.reindex(new.index) != new).sum()
    print(f"ĐỐI CHIẾU tsvm s0 clinicdb: {lech}/{len(new)} ảnh lệch số điểm ảnh dự đoán; "
          f"ảnh không dự đoán: cũ {int((old == 0).sum())}, mới {int((new == 0).sum())}")


def run(args, dev):
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    for key in args.sets:
        items = None
        for v in args.variants:
            for s in args.seeds:
                out = OUT / f"{key}_{v}_s{s}.csv"
                if out.exists():
                    continue
                w = weights(v, s)
                assert w is not None, f"thiếu checkpoint {v} seed {s}"
                if items is None:
                    items = ng.load_set(key)
                    print(f"[{key}] {len(items)} ảnh")
                t1 = time.time()
                preds = dg.predict_yolo(w, items, dev)
                torch.cuda.empty_cache()
                rows = []
                for it, pr in zip(items, preds):
                    tp, fp, fn = dg.counts(pr, it["gt"])
                    rows.append({"dataset": key, "model": v, "seed": s, "image": it["name"],
                                 "pred_px": int(pr.sum()), "gt_px": int(it["gt"].sum()), "tp": tp, "fp": fp, "fn": fn})
                pd.DataFrame(rows).to_csv(out, index=False, encoding="utf-8-sig")
                print(f"  {key:8s} {v:16s} seed {s}: {time.time() - t1:6.1f}s")
        del items
    print(f"Xong. Tổng thời gian: {(time.time() - t0) / 60:.1f} phút. Kết quả: {OUT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sets", nargs="*", default=["clinicdb", "colondb"], choices=list(ng.SETS))
    ap.add_argument("--variants", nargs="*", default=list(VARIANTS), choices=list(VARIANTS))
    ap.add_argument("--seeds", nargs="*", type=int, default=list(range(10)))
    ap.add_argument("--kiem-tra", action="store_true", help="chỉ kiểm tra checkpoint, dữ liệu, GPU rồi dừng")
    ap.add_argument("--doi-chieu", action="store_true", help="chạy lại TSVM seed 0 trên ClinicDB và so với kết quả cũ")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not kiem_tra(args) or args.kiem_tra:
        return
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    cleanup = dg.import_fork()
    try:
        if args.doi_chieu:
            doi_chieu("cuda:0")
        else:
            run(args, "cuda:0")
    finally:
        cleanup()


if __name__ == "__main__":
    main()
