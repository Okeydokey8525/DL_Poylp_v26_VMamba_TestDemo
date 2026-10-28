"""Đo FLOPs và độ trễ GPU của YOLO26s-seg (đối chứng) và YOLO26s-seg + TSVM FP32, checkpoint seed 0.

- FLOPs: torch.utils.flop_counter.FlopCounterMode trên một lần forward ảnh 1×3×640×640 (FP32, sau khi gộp Conv-BN
  như khi suy luận). Bộ đếm này tính các phép conv, matmul/bmm/einsum; các phép theo phần tử (nhân, cộng, exp
  trong phép quét SS2D) không được tính, nên FLOPs của TSVM là cận dưới. Ghi kèm GFLOPs do Ultralytics báo
  (model.info, dùng thop nếu có) để đối chiếu.
- Độ trễ GPU: chỉ forward, batch 1, FP32, cudnn.benchmark tắt; khởi động 50 lần, đo 200 lần bằng CUDA event.
  Không gồm tiền xử lý và hậu xử lý. Đo xen kẽ hai mô hình 5 vòng. Trước mỗi khối đo, chờ GPU nguội xuống
  dưới COOL_C (tối đa COOL_MAX_S giây) và ghi nhiệt độ, xung nhịp trước/sau khối (nvidia-smi), vì GPU laptop
  hạ xung khi nóng (lần đo 28/10/2026 lúc máy không có quạt tản nhiệt bị ảnh hưởng rõ).

Kết quả: ../bang/16_flops_do_tre_gpu.csv (tổng hợp) và ../bang/16b_do_tre_gpu_tung_lan.csv (từng lần đo).

    C:\\venv_kl_gpu\\Scripts\\python.exe do_flops_gpu.py
"""
from __future__ import annotations

import platform
import subprocess
import sys
import time

import numpy as np
import pandas as pd
import torch
from torch.utils.flop_counter import FlopCounterMode

import danh_gia_pixel as dg

WARMUP, ITERS, ROUNDS = 50, 200, 5
COOL_C, COOL_MAX_S = 55, 180


def gpu_state():
    """(nhiệt độ °C, xung nhịp SM MHz) từ nvidia-smi; (nan, nan) nếu không đọc được."""
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu,clocks.sm", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=10).stdout.split(",")
        return float(out[0]), float(out[1])
    except Exception:
        return np.nan, np.nan


def cho_nguoi():
    """Chờ GPU nguội xuống dưới COOL_C, tối đa COOL_MAX_S giây. Trả về số giây đã chờ."""
    t0 = time.time()
    while time.time() - t0 < COOL_MAX_S and not gpu_state()[0] < COOL_C:
        time.sleep(5)
    return time.time() - t0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    assert torch.cuda.is_available(), "Cần GPU (chạy bằng C:\\venv_kl_gpu\\Scripts\\python.exe)"
    torch.backends.cudnn.benchmark = False
    cleanup = dg.import_fork()
    from ultralytics import YOLO
    from ultralytics.utils import LOGGER
    from ultralytics.utils.torch_utils import get_flops
    LOGGER.setLevel("ERROR")
    try:
        nets, info = {}, []
        for key in ("baseline", "tsvm"):
            yolo = YOLO(str(dg.MODELS[key][1](0)))
            n_param = sum(p.numel() for p in yolo.model.parameters())
            ul_gflops = get_flops(yolo.model, imgsz=640) or np.nan   # 0 khi không đếm được
            net = yolo.model.fuse().float().eval()
            x = torch.zeros(1, 3, 640, 640)
            with torch.inference_mode(), FlopCounterMode(display=False) as fc:
                net(x)
            info.append({"model": key, "params": n_param, "gflops_flopcounter": fc.get_total_flops() / 1e9,
                         "gflops_ultralytics": ul_gflops})
            nets[key] = net.cuda()
            print(f"{key}: {n_param:,} tham số, FlopCounter {fc.get_total_flops() / 1e9:.2f} GFLOPs, "
                  f"Ultralytics {ul_gflops} GFLOPs")

        x = torch.zeros(1, 3, 640, 640, device="cuda")
        rows, blocks = [], []
        with torch.inference_mode():
            for r in range(ROUNDS):
                # đổi thứ tự mỗi vòng để mô hình nào cũng có lúc được đo trước
                for key in (list(nets) if r % 2 == 0 else list(nets)[::-1]):
                    net = nets[key]
                    waited = cho_nguoi()
                    temp0, clk0 = gpu_state()
                    for _ in range(WARMUP):
                        net(x)
                    torch.cuda.synchronize()
                    for i in range(ITERS):
                        s, e = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
                        s.record()
                        net(x)
                        e.record()
                        torch.cuda.synchronize()
                        rows.append({"model": key, "round": r, "iteration": i, "latency_ms": s.elapsed_time(e)})
                    temp1, clk1 = gpu_state()
                    med = np.median([q["latency_ms"] for q in rows[-ITERS:]])
                    blocks.append({"model": key, "round": r, "cho_nguoi_s": round(waited), "nhiet_truoc": temp0,
                                   "nhiet_sau": temp1, "xung_truoc_mhz": clk0, "xung_sau_mhz": clk1, "median_ms": med})
                    print(f"vòng {r} {key}: chờ {waited:.0f}s, {temp0:.0f}→{temp1:.0f}°C, "
                          f"xung {clk0:.0f}→{clk1:.0f} MHz, trung vị {med:.2f} ms", flush=True)
        lat = pd.DataFrame(rows)
        pd.DataFrame(blocks).to_csv(dg.OUT / "16c_do_tre_gpu_nhiet_do.csv", index=False, encoding="utf-8-sig")
        dg.OUT.mkdir(exist_ok=True)
        lat.to_csv(dg.OUT / "16b_do_tre_gpu_tung_lan.csv", index=False, encoding="utf-8-sig")
        g = lat.groupby("model").latency_ms
        out = pd.DataFrame(info).set_index("model")
        out["gpu_ms_median"], out["gpu_ms_mean"] = g.median(), g.mean()
        out["gpu_ms_sd"], out["gpu_ms_p95"] = g.std(ddof=1), g.quantile(0.95)
        # GPU laptop hạ xung khi nóng: độ trễ tăng dần qua các vòng. Min và phân vị 10% ít bị ảnh hưởng nhất.
        out["gpu_ms_min"], out["gpu_ms_p10"] = g.min(), g.quantile(0.10)
        out["gpu_ms_median_vong0"] = lat[lat["round"] == 0].groupby("model").latency_ms.median()
        out["gpu"] = torch.cuda.get_device_name(0)
        out["torch"] = torch.__version__
        out["platform"] = platform.platform()
        out.reset_index().to_csv(dg.OUT / "16_flops_do_tre_gpu.csv", index=False, encoding="utf-8-sig")
        with pd.option_context("display.width", 200, "display.float_format", "{:.3f}".format):
            print(out.drop(columns=["platform"]).to_string())
        print(f"Tỉ lệ độ trễ GPU (TSVM / đối chứng, trung vị): {out.gpu_ms_median['tsvm'] / out.gpu_ms_median['baseline']:.2f}")
    finally:
        cleanup()


if __name__ == "__main__":
    main()
