"""Đo độ trễ end-to-end của dịch vụ suy luận PolypVision qua HTTP thật.

Gửi lần lượt 160 ảnh val BG20 (120 polyp + 40 nền) tới endpoint /predict (đúng endpoint Spring Boot gọi) cho từng mô hình.
Mỗi yêu cầu ghi:
- client_ms: thời gian khứ hồi đo ở phía client (gửi multipart, chờ, nhận JSON có ảnh lớp phủ Base64);
- decode/infer/render/total_ms: thời gian từng bước phía máy chủ, đọc từ header Server-Timing.

Dịch vụ phải đang chạy (ví dụ uvicorn main:app --port 8010). Script chỉ đọc ảnh, không sửa dữ liệu.

Ví dụ:
    python do_tre_end_to_end.py --url http://127.0.0.1:8010 --nhan cpu
Kết quả: bang/19_do_tre_end_to_end_tung_anh.csv (từng yêu cầu) và bang/19_do_tre_end_to_end.csv (tóm tắt).
Chạy thêm lần khác (ví dụ --nhan gpu) thì kết quả được nối thêm, các dòng cùng nhãn được thay.
"""
import argparse
import csv
import json
import mimetypes
import platform
import statistics
import time
import urllib.request
import uuid
from datetime import datetime
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
ANH_VAL = GOC / "01_du_lieu" / "Kvasir_YOLO_SEG_BG20" / "images" / "val"
BANG = GOC / "00_tai_lieu_tong_quan" / "bang"
MO_HINH = ["YOLO26s-seg", "YOLO26s-TSVM-FP32-seg"]
COT_TUNG_ANH = ["nhan", "thiet_bi", "mo_hinh", "lan", "anh", "bytes", "client_ms",
                "decode_ms", "infer_ms", "render_ms", "total_ms", "detected"]


def multipart(duong_dan: Path, model_type: str) -> tuple[bytes, str]:
    ranh_gioi = f"----dotre-{uuid.uuid4().hex}"
    loai = mimetypes.guess_type(duong_dan.name)[0] or "image/jpeg"
    than = (
        f"--{ranh_gioi}\r\nContent-Disposition: form-data; name=\"modelType\"\r\n\r\n{model_type}\r\n"
        f"--{ranh_gioi}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{duong_dan.name}\"\r\n"
        f"Content-Type: {loai}\r\n\r\n"
    ).encode() + duong_dan.read_bytes() + f"\r\n--{ranh_gioi}--\r\n".encode()
    return than, f"multipart/form-data; boundary={ranh_gioi}"


def doc_server_timing(header: str | None) -> dict[str, float]:
    ket_qua = {}
    for phan in (header or "").split(","):
        if ";dur=" in phan:
            ten, gia_tri = phan.strip().split(";dur=")
            ket_qua[ten] = float(gia_tri)
    return ket_qua


def gui(url: str, duong_dan: Path, model_type: str) -> dict:
    than, loai = multipart(duong_dan, model_type)
    yeu_cau = urllib.request.Request(f"{url}/predict", data=than, headers={"Content-Type": loai})
    bat_dau = time.perf_counter()
    with urllib.request.urlopen(yeu_cau, timeout=300) as phan_hoi:
        noi_dung = phan_hoi.read()
        timing = doc_server_timing(phan_hoi.headers.get("Server-Timing"))
    client_ms = (time.perf_counter() - bat_dau) * 1000
    json_kq = json.loads(noi_dung)
    assert json_kq["modelType"] == model_type, json_kq["modelType"]
    return {"client_ms": client_ms, "bytes": len(than), "detected": json_kq["detected"],
            **{f"{k}_ms": timing.get(k) for k in ("decode", "infer", "render", "total")}}


def phan_vi(day: list[float], q: float) -> float:
    day = sorted(day)
    vi_tri = (len(day) - 1) * q
    duoi = int(vi_tri)
    tren = min(duoi + 1, len(day) - 1)
    return day[duoi] + (day[tren] - day[duoi]) * (vi_tri - duoi)


def ghi_csv(duong_dan: Path, cot: list[str], dong_moi: list[dict], nhan: str) -> None:
    cu = []
    if duong_dan.exists():
        with open(duong_dan, encoding="utf-8-sig", newline="") as f:
            cu = [d for d in csv.DictReader(f) if d["nhan"] != nhan]
    with open(duong_dan, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cot)
        w.writeheader()
        w.writerows(cu + dong_moi)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8010")
    ap.add_argument("--nhan", required=True, help="nhãn lần đo, ví dụ cpu hoặc gpu")
    ap.add_argument("--khoi-dong", type=int, default=10, help="số yêu cầu khởi động mỗi mô hình (không ghi)")
    ap.add_argument("--lap", type=int, default=1, help="số lần lặp qua toàn bộ ảnh val")
    a = ap.parse_args()

    with urllib.request.urlopen(f"{a.url}/health", timeout=30) as r:
        suc_khoe = json.loads(r.read())
    thiet_bi = suc_khoe.get("device", "?")
    for m in MO_HINH:
        assert suc_khoe["models"][m]["status"] == "ready", (m, suc_khoe["models"][m])
    anh = sorted(p for p in ANH_VAL.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"})
    print(f"Thiết bị {thiet_bi}, {len(anh)} ảnh val, khởi động {a.khoi_dong}, lặp {a.lap}")

    tung_anh = []
    for m in MO_HINH:
        for p in anh[: a.khoi_dong]:
            gui(a.url, p, m)
        for lan in range(a.lap):
            for p in anh:
                kq = gui(a.url, p, m)
                tung_anh.append({"nhan": a.nhan, "thiet_bi": thiet_bi, "mo_hinh": m, "lan": lan,
                                 "anh": p.name, **kq})
        print(f"  xong {m}")

    tom_tat = []
    for m in MO_HINH:
        dong = [d for d in tung_anh if d["mo_hinh"] == m]
        ban_ghi = {"nhan": a.nhan, "thiet_bi": thiet_bi, "mo_hinh": m, "so_yeu_cau": len(dong)}
        for cot in ("client_ms", "decode_ms", "infer_ms", "render_ms", "total_ms"):
            gia_tri = [d[cot] for d in dong if d[cot] is not None]
            ban_ghi[f"{cot}_trung_vi"] = round(statistics.median(gia_tri), 2) if gia_tri else ""
            ban_ghi[f"{cot}_p95"] = round(phan_vi(gia_tri, 0.95), 2) if gia_tri else ""
            ban_ghi[f"{cot}_tb"] = round(statistics.fmean(gia_tri), 2) if gia_tri else ""
        tom_tat.append(ban_ghi)
    for b in tom_tat:
        b["ti_le_client_tsvm_tren_goc"] = ""
    tom_tat[1]["ti_le_client_tsvm_tren_goc"] = round(
        tom_tat[1]["client_ms_trung_vi"] / tom_tat[0]["client_ms_trung_vi"], 3)
    for b in tom_tat:
        b["may"] = f"{platform.processor()} | {platform.system()} {platform.release()}"
        b["ngay_do"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    for d in tung_anh:
        for k in ("client_ms", "decode_ms", "infer_ms", "render_ms", "total_ms"):
            if d[k] is not None:
                d[k] = round(d[k], 3)
    ghi_csv(BANG / "19_do_tre_end_to_end_tung_anh.csv", COT_TUNG_ANH, tung_anh, a.nhan)
    ghi_csv(BANG / "19_do_tre_end_to_end.csv", list(tom_tat[0].keys()), tom_tat, a.nhan)
    for b in tom_tat:
        print(f"{b['mo_hinh']}: client trung vị {b['client_ms_trung_vi']} ms (p95 {b['client_ms_p95']}), "
              f"suy luận {b['infer_ms_trung_vi']} ms, vẽ {b['render_ms_trung_vi']} ms, giải mã {b['decode_ms_trung_vi']} ms")
    print("Tỉ lệ client TSVM/gốc:", tom_tat[1]["ti_le_client_tsvm_tren_goc"])


if __name__ == "__main__":
    main()
