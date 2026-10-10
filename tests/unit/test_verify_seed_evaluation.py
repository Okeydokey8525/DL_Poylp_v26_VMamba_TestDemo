"""Checks for invalid evidence and image-level background counts, no ML runtime needed."""
import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/analysis/verify_seed_evaluation.py"
SPEC = importlib.util.spec_from_file_location("verify_seed_evaluation", SCRIPT)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class EvidenceTests(unittest.TestCase):
    def test_best_epoch_uses_mask_map5095_not_map50(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "results.csv"
            with path.open("w", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["epoch", "metrics/mAP50(M)", "metrics/mAP50-95(M)"])
                for epoch in range(1, 101):
                    writer.writerow([epoch, 0.95 if epoch == 97 else 0.9, 0.74 if epoch == 93 else 0.7])
            result = audit.best_csv(path)
            self.assertEqual(result["epoch"], 93)
            self.assertEqual(result["peak_mask_map50_epoch"], 97)
            with path.open("a") as handle:
                handle.write("101,0.9,0.7\n")
            with self.assertRaises(ValueError):
                audit.best_csv(path)

    def test_manifest_counts_instances_and_rejects_missing_background_label(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "images/val").mkdir(parents=True)
            (root / "labels/val").mkdir(parents=True)
            for index in range(160):
                (root / f"images/val/{index}.jpg").write_bytes(b"fixture image")
                polygon = "0 0.1 0.1 0.5 0.1 0.5 0.5\n"
                text = "" if index < 40 else polygon * (2 if index < 47 else 1)
                (root / f"labels/val/{index}.txt").write_text(text)
            result = audit.dataset_manifest(root)
            self.assertEqual(result["counts"], {"images": 160, "background_images": 40, "instances": 127})
            (root / "labels/val/0.txt").unlink()
            with self.assertRaisesRegex(ValueError, "Missing label"):
                audit.dataset_manifest(root)


if __name__ == "__main__":
    unittest.main()
