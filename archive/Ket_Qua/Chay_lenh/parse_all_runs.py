import os
import glob
import pandas as pd
import yaml
import json

root = r"c:\LeDucLuong\HK VII\LuanCuNhan\DeepLearning\Ket_Qua"
results_info = []

for dirpath, dirnames, filenames in os.walk(root):
    if ".venv" in dirpath or "scratch" in dirpath:
        continue
    if "results.csv" in filenames:
        rel = os.path.relpath(dirpath, root)
        csv_path = os.path.join(dirpath, "results.csv")
        yaml_path = os.path.join(dirpath, "args.yaml")
        
        args = {}
        if os.path.exists(yaml_path):
            with open(yaml_path, "r", encoding="utf-8", errors="ignore") as f:
                try:
                    args = yaml.safe_load(f) or {}
                except:
                    pass
        
        try:
            df = pd.read_csv(csv_path)
            df.columns = [c.strip() for c in df.columns]
            num_epochs = len(df)
            
            mask_col = "metrics/mAP50-95(M)" if "metrics/mAP50-95(M)" in df.columns else None
            box_col = "metrics/mAP50-95(B)" if "metrics/mAP50-95(B)" in df.columns else None
            
            best_ep_idx = df[mask_col].idxmax() if mask_col else -1
            best_mask_row = df.iloc[best_ep_idx] if best_ep_idx != -1 else None
            
            last_row = df.iloc[-1]
            
            # Peak metrics across all epochs
            peak_metrics = {
                "box_p_max": float(df["metrics/precision(B)"].max()) if "metrics/precision(B)" in df else None,
                "box_r_max": float(df["metrics/recall(B)"].max()) if "metrics/recall(B)" in df else None,
                "box_map50_max": float(df["metrics/mAP50(B)"].max()) if "metrics/mAP50(B)" in df else None,
                "box_map5095_max": float(df["metrics/mAP50-95(B)"].max()) if "metrics/mAP50-95(B)" in df else None,
                "mask_p_max": float(df["metrics/precision(M)"].max()) if "metrics/precision(M)" in df else None,
                "mask_r_max": float(df["metrics/recall(M)"].max()) if "metrics/recall(M)" in df else None,
                "mask_map50_max": float(df["metrics/mAP50(M)"].max()) if "metrics/mAP50(M)" in df else None,
                "mask_map5095_max": float(df["metrics/mAP50-95(M)"].max()) if "metrics/mAP50-95(M)" in df else None,
            }
            
            # Epochs where peak occurred
            peak_epochs = {
                "box_p_max_ep": int(df["metrics/precision(B)"].idxmax() + 1) if "metrics/precision(B)" in df else None,
                "box_r_max_ep": int(df["metrics/recall(B)"].idxmax() + 1) if "metrics/recall(B)" in df else None,
                "box_map50_max_ep": int(df["metrics/mAP50(B)"].idxmax() + 1) if "metrics/mAP50(B)" in df else None,
                "box_map5095_max_ep": int(df["metrics/mAP50-95(B)"].idxmax() + 1) if "metrics/mAP50-95(B)" in df else None,
                "mask_p_max_ep": int(df["metrics/precision(M)"].idxmax() + 1) if "metrics/precision(M)" in df else None,
                "mask_r_max_ep": int(df["metrics/recall(M)"].idxmax() + 1) if "metrics/recall(M)" in df else None,
                "mask_map50_max_ep": int(df["metrics/mAP50(M)"].idxmax() + 1) if "metrics/mAP50(M)" in df else None,
                "mask_map5095_max_ep": int(df["metrics/mAP50-95(M)"].idxmax() + 1) if "metrics/mAP50-95(M)" in df else None,
            }
            
            best_epoch_num = int(best_mask_row["epoch"]) if best_mask_row is not None and "epoch" in best_mask_row else best_ep_idx + 1
            
            best_epoch_metrics = {
                "epoch": best_epoch_num,
                "box_p": float(best_mask_row["metrics/precision(B)"]) if "metrics/precision(B)" in best_mask_row else None,
                "box_r": float(best_mask_row["metrics/recall(B)"]) if "metrics/recall(B)" in best_mask_row else None,
                "box_map50": float(best_mask_row["metrics/mAP50(B)"]) if "metrics/mAP50(B)" in best_mask_row else None,
                "box_map5095": float(best_mask_row["metrics/mAP50-95(B)"]) if "metrics/mAP50-95(B)" in best_mask_row else None,
                "mask_p": float(best_mask_row["metrics/precision(M)"]) if "metrics/precision(M)" in best_mask_row else None,
                "mask_r": float(best_mask_row["metrics/recall(M)"]) if "metrics/recall(M)" in best_mask_row else None,
                "mask_map50": float(best_mask_row["metrics/mAP50(M)"]) if "metrics/mAP50(M)" in best_mask_row else None,
                "mask_map5095": float(best_mask_row["metrics/mAP50-95(M)"]) if "metrics/mAP50-95(M)" in best_mask_row else None,
                "train_box_loss": float(best_mask_row["train/box_loss"]) if "train/box_loss" in best_mask_row else None,
                "val_box_loss": float(best_mask_row["val/box_loss"]) if "val/box_loss" in best_mask_row else None,
                "train_seg_loss": float(best_mask_row["train/seg_loss"]) if "train/seg_loss" in best_mask_row else None,
                "val_seg_loss": float(best_mask_row["val/seg_loss"]) if "val/seg_loss" in best_mask_row else None,
                "train_cls_loss": float(best_mask_row["train/cls_loss"]) if "train/cls_loss" in best_mask_row else None,
                "val_cls_loss": float(best_mask_row["val/cls_loss"]) if "val/cls_loss" in best_mask_row else None,
            }
            
            final_epoch_metrics = {
                "epoch": int(last_row["epoch"]) if "epoch" in last_row else num_epochs,
                "box_p": float(last_row["metrics/precision(B)"]) if "metrics/precision(B)" in last_row else None,
                "box_r": float(last_row["metrics/recall(B)"]) if "metrics/recall(B)" in last_row else None,
                "box_map50": float(last_row["metrics/mAP50(B)"]) if "metrics/mAP50(B)" in last_row else None,
                "box_map5095": float(last_row["metrics/mAP50-95(B)"]) if "metrics/mAP50-95(B)" in last_row else None,
                "mask_p": float(last_row["metrics/precision(M)"]) if "metrics/precision(M)" in last_row else None,
                "mask_r": float(last_row["metrics/recall(M)"]) if "metrics/recall(M)" in last_row else None,
                "mask_map50": float(last_row["metrics/mAP50(M)"]) if "metrics/mAP50(M)" in last_row else None,
                "mask_map5095": float(last_row["metrics/mAP50-95(M)"]) if "metrics/mAP50-95(M)" in last_row else None,
                "train_box_loss": float(last_row["train/box_loss"]) if "train/box_loss" in last_row else None,
                "val_box_loss": float(last_row["val/box_loss"]) if "val/box_loss" in last_row else None,
                "train_seg_loss": float(last_row["train/seg_loss"]) if "train/seg_loss" in last_row else None,
                "val_seg_loss": float(last_row["val/seg_loss"]) if "val/seg_loss" in last_row else None,
                "train_cls_loss": float(last_row["train/cls_loss"]) if "train/cls_loss" in last_row else None,
                "val_cls_loss": float(last_row["val/cls_loss"]) if "val/cls_loss" in last_row else None,
            }
            
            results_info.append({
                "rel_path": rel,
                "model_arg": args.get("model", "N/A"),
                "data_arg": args.get("data", "N/A"),
                "epochs_arg": args.get("epochs", "N/A"),
                "batch_arg": args.get("batch", "N/A"),
                "imgsz_arg": args.get("imgsz", "N/A"),
                "seed_arg": args.get("seed", "N/A"),
                "optimizer_arg": args.get("optimizer", "N/A"),
                "lr0_arg": args.get("lr0", "N/A"),
                "epochs_run": num_epochs,
                "best_epoch": best_epoch_num,
                "peak_metrics": peak_metrics,
                "peak_epochs": peak_epochs,
                "best_epoch_metrics": best_epoch_metrics,
                "final_epoch_metrics": final_epoch_metrics,
            })
        except Exception as e:
            print(f"Error processing {csv_path}: {e}")

out_json = os.path.join(root, "all_runs_metrics.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(results_info, f, indent=2)

print(f"Successfully processed {len(results_info)} runs. Saved to {out_json}")
