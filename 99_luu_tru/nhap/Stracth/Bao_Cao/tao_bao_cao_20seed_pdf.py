"""Bao cao 20 seed (Baseline vs TSVM FP32) dang PDF, theo mau CNTT_KLCN182_LeDucLuong_formatThang.

    python archive/Stracth/Bao_Cao/tao_bao_cao_20seed_pdf.py

Noi dung giong ban Word CNTT_KLCN182_BaoCao_20Seed_FP32.docx; so lieu doc tu archive/Ket_Qua_V2/KQ_Nen_DX_20seed_FP32.
Dung HTML A4 roi in PDF bang Edge headless. Ghi archive/Bao_cao/CNTT_KLCN182_BaoCao_20Seed_FP32.pdf.
"""
import subprocess
import tempfile
from pathlib import Path

import matplotlib
import pandas as pd
from scipy import stats as sstats

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "Ket_Qua_V2" / "KQ_Nen_DX_20seed_FP32"
FIG = DATA / "figures"
OUT = ROOT / "Bao_cao" / "CNTT_KLCN182_BaoCao_20Seed_FP32.pdf"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
FONTS = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
NGAY = "TP. Hồ Chí Minh, ngày 13 tháng 10 năm 2026"

summ = pd.read_csv(DATA / "summary_20seeds_paired.csv").set_index("metric")
raw = pd.read_csv(DATA / "raw_20seeds_extracted_metrics.csv")
cm = pd.read_csv(DATA / "raw_20seeds_confusion_matrices.csv")
base = raw[raw.model == "Baseline"].set_index("seed").sort_index()
tsvm = raw[raw.model != "Baseline"].set_index("seed").sort_index()
cmb = cm[cm.model == "Baseline"].set_index("seed").sort_index()
cmt = cm[cm.model != "Baseline"].set_index("seed").sort_index()

m, loss = summ.loc["mask_map50_95"], summ.loc["val_seg_loss"]
wins, losses = int(m.tsvm_wins), int(m.baseline_wins)
sign_p = sstats.binomtest(wins, wins + losses).pvalue
sd_mask = (1 - m.tsvm_sd / m.baseline_sd) * 100
sd_loss = (1 - loss.tsvm_sd / loss.baseline_sd) * 100
loss_pct = -loss.delta / loss.baseline_mean * 100
gain = tsvm.mask_map50_95 - base.mask_map50_95
win_seeds = [int(s) for s in gain.index if gain[s] > 0]
fp_p = sstats.ttest_rel(cmt.FP, cmb.FP).pvalue
fp_fewer, fp_more = int((cmt.FP < cmb.FP).sum()), int((cmt.FP > cmb.FP).sum())
fp_rate = {k: v.FP / (v.TP + v.FP) * 100 for k, v in (("b", cmb), ("t", cmt))}
sens = {k: v.TP / 127 * 100 for k, v in (("b", cmb), ("t", cmt))}
low_b, low_t = int((base.mask_map50_95 < 0.71).sum()), int((tsvm.mask_map50_95 < 0.71).sum())


def p_(v, d=4):
    return f"<i>p</i> = {v:.{d}f}"


def num(v, d=4):
    return f"{v:+.{d}f}".replace("-", "−")


def B(t):
    return f'<b class="b">{t}</b>'


def R(t):
    return f'<b class="r">{t}</b>'


_tab, _fig = [0], [0]


def table(head, rows, align, caption, width=None, bold_last=False, head_rows=None):
    _tab[0] += 1
    style = f' style="width:{width}"' if width else ""
    thead = head_rows or "<tr>" + "".join(f'<th class="{a}">{h}</th>' for h, a in zip(head, align)) + "</tr>"
    body = ""
    for i, row in enumerate(rows):
        cls = ' class="last"' if bold_last and i == len(rows) - 1 else ""
        body += f"<tr{cls}>" + "".join(f'<td class="{a}">{c}</td>' for c, a in zip(row, align)) + "</tr>"
    return (f'<div class="tbl"><div class="cap"><b>Bảng {_tab[0]}.</b> {caption}</div>'
            f'<table{style}><thead>{thead}</thead><tbody>{body}</tbody></table></div>')


def plain_table(head, rows, align, width=None):
    style = f' style="width:{width}"' if width else ""
    th = "".join(f'<th class="{a}">{h}</th>' for h, a in zip(head, align))
    body = "".join("<tr>" + "".join(f'<td class="{a}">{c}</td>' for c, a in zip(row, align)) + "</tr>" for row in rows)
    return f'<div class="tbl"><table{style}><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def figure(name, width, caption):
    _fig[0] += 1
    return (f'<figure><img src="{(FIG / name).as_uri()}" style="width:{width}">'
            f'<figcaption><b>Hình {_fig[0]}.</b> {caption}</figcaption></figure>')


def bold_better(b, t, lower=False):
    sb, st = f"{b[0]:.4f} ± {b[1]:.4f}", f"{t[0]:.4f} ± {t[1]:.4f}"
    return (sb, f"<b>{st}</b>") if (t[0] < b[0] if lower else t[0] > b[0]) else (f"<b>{sb}</b>", st)


def lev(v):
    return f'<b class="b">{v:.3f}</b>' if v < 0.05 else f"{v:.3f}"


rows3 = []
for key, label in [("mask_map50_95", "Mask mAP@50-95"), ("mask_map50", "Mask mAP@50"), ("mask_precision", "Mask Precision"),
                   ("mask_recall", "Mask Recall"), ("box_map50_95", "Box mAP@50-95"), ("box_map50", "Box mAP@50"),
                   ("box_recall", "Box Recall"), ("val_seg_loss", "Val Seg Loss")]:
    x = summ.loc[key]
    sb, st = bold_better((x.baseline_mean, x.baseline_sd), (x.tsvm_mean, x.tsvm_sd), key == "val_seg_loss")
    rows3.append([label, sb, st, num(x.delta), f"{x.p_ttest:.4f}", lev(x.levene_p)])

rows4 = [[f"Seed {s}", int(base.loc[s].best_epoch), f"{base.loc[s].mask_map50_95:.4f}", int(tsvm.loc[s].best_epoch),
          f"{tsvm.loc[s].mask_map50_95:.4f}", num(gain[s])] for s in base.index]
head4 = ('<tr><th class="l">Seed</th><th class="c">Epoch tốt nhất<br>Baseline</th><th class="c">mAP@50-95<br>Baseline</th>'
         '<th class="c">Epoch tốt nhất<br>TSVM</th><th class="c">mAP@50-95<br>TSVM</th><th class="r">Δ</th></tr>')


def ms(s, d=1, unit=""):
    return f"{s.mean():.{d}f}{unit} ± {s.std(ddof=1):.{d}f}{unit}"


rows5 = [
    ["Phát hiện đúng (TP)", ms(cmb.TP), ms(cmt.TP), f"{num(cmt.TP.mean() - cmb.TP.mean(), 1)} ca"],
    ["Bỏ sót (FN)", ms(cmb.FN), ms(cmt.FN), f"{num(cmt.FN.mean() - cmb.FN.mean(), 1)} ca"],
    ["Báo động giả (FP)", ms(cmb.FP), ms(cmt.FP), f"{num(cmt.FP.mean() - cmb.FP.mean(), 1)} ca"],
    ["Độ nhạy", ms(sens["b"], 2, "%"), ms(sens["t"], 2, "%"), f"{num(sens['t'].mean() - sens['b'].mean(), 2)}%"],
    ["Tỷ lệ FP trên tổng dự đoán", ms(fp_rate["b"], 2, "%"), ms(fp_rate["t"], 2, "%"),
     f"{num(fp_rate['t'].mean() - fp_rate['b'].mean(), 2)}%"],
]


def font_face(family, file, weight="normal", style="normal"):
    return (f'@font-face {{ font-family: "{family}"; src: url("{(FONTS / file).as_uri()}"); '
            f"font-weight: {weight}; font-style: {style}; }}\n")


CSS = (font_face("DVSerif", "DejaVuSerif.ttf") + font_face("DVSerif", "DejaVuSerif-Bold.ttf", "bold")
       + font_face("DVSerif", "DejaVuSerif-Italic.ttf", style="italic")
       + font_face("DVSerif", "DejaVuSerif-BoldItalic.ttf", "bold", "italic")
       + font_face("DVSans", "DejaVuSans.ttf") + font_face("DVSans", "DejaVuSans-Bold.ttf", "bold")) + """
@page { size: A4; margin: 19mm 21mm 20mm 21mm;
  @bottom-center { content: counter(page); font: 8.5pt "DVSerif"; color: #222; } }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "DVSerif", serif; font-size: 9.6pt; line-height: 1.5; color: #111; text-align: justify;
  margin: 0; background: #fff; }
p { margin: 0 0 4pt; }
.head { text-align: center; }
.uni { font: bold 8.6pt "DVSans"; color: #17325c; letter-spacing: .2pt; margin: 4pt 0 14pt; }
.title { font: bold 19pt/1.3 "DVSans"; color: #17325c; margin: 0 0 4pt; }
.topic { font-style: italic; font-size: 9.6pt; margin-bottom: 16pt; }
table.info { width: 100%; border-collapse: collapse; border-top: 1px solid #333; border-bottom: 1px solid #333;
  margin-bottom: 18pt; text-align: left; font-size: 8.9pt; }
table.info td { padding: 3pt 0; vertical-align: top; }
table.info td:first-child { font: bold 8.2pt "DVSans"; color: #17325c; width: 24%; padding-right: 8pt; vertical-align: bottom; }
h1 { font: bold 13pt "DVSans"; color: #17325c; border-bottom: .8px solid #6d7fa3; padding-bottom: 1pt;
  margin: 18pt 0 8pt; break-after: avoid; }
h1 .n { margin-right: 7pt; }
h2 { font: bold 9.2pt "DVSans"; color: #1f63a8; margin: 14pt 0 6pt; break-after: avoid; }
h2 .n { margin-right: 5pt; }
.b { color: #1f63a8; }
.r { color: #d04545; }
.tbl { margin: 8pt 0 12pt; break-inside: avoid; }
.cap, figcaption { font: 7.6pt/1.4 "DVSans"; color: #111; text-align: left; margin-bottom: 3pt; }
.cap b, figcaption b { color: #17325c; }
.tbl table { border-collapse: collapse; margin: 0 auto; border-top: 1px solid #333; border-bottom: 1px solid #333;
  font-size: 9pt; line-height: 1.35; }
.tbl th { font-weight: normal; padding: 4pt 7pt; border-bottom: .6px solid #333; vertical-align: bottom; }
.tbl td { padding: 1.6pt 7pt; vertical-align: top; }
.tbl tr:first-child td { padding-top: 4pt; }
.tbl tr:last-child td { padding-bottom: 4pt; }
.tbl tr.last td { border-top: .6px solid #333; font-weight: bold; padding-top: 4pt; }
.tbl tr.last td:first-child { font-weight: normal; }
.kq td:first-child, .kq th:first-child { font-weight: bold; }
.kq th:first-child { font-weight: bold; }
.l { text-align: left; } .r.t, td.r, th.r { text-align: right; } .c { text-align: center; } .j { text-align: justify; }
td.r, th.r { color: inherit; }
figure { margin: 8pt 0 10pt; text-align: center; break-inside: avoid; }
figure img { display: block; margin: 0 auto 6pt; }
.keep { break-inside: avoid; }
ul { margin: 2pt 0 6pt; padding-left: 15pt; }
li { margin-bottom: 4pt; }
.sign { text-align: right; margin-top: 20pt; line-height: 1.4; }
"""

# Bang "Ket qua chinh" va bang thong tin (khong danh so, giong mau)
kq_rows = [
    ["Mask mAP@50-95", f"TSVM đạt {m.tsvm_mean:.4f} so với {m.baseline_mean:.4f} của Baseline; chênh lệch trung bình "
                       f"{R('chưa đạt ý nghĩa thống kê')} ở mức 0.05 ({p_(m.p_ttest)})."],
    ["Độ ổn định", f"Độ lệch chuẩn của TSVM thấp hơn {sd_mask:.1f}%; khác biệt phương sai {B('có ý nghĩa thống kê')} "
                   f"(Levene {p_(m.levene_p, 3)})."],
    ["Mất mát phân đoạn kiểm định", f"TSVM thấp hơn {loss_pct:.2f}% ({p_(loss.p_ttest, 3)}); độ lệch chuẩn thấp hơn "
                                     f"{sd_loss:.1f}% (Levene {p_(loss.levene_p, 3)})."],
    ["Từng seed", f"TSVM đạt kết quả cao hơn ở {wins}/20 seed (kiểm định dấu {p_(sign_p)})."],
    ["Ma trận nhầm lẫn", f"TP và FN gần như trùng nhau; FP ít hơn {abs(cmt.FP.mean() - cmb.FP.mean()):.1f} nhưng "
                         f"{p_(fp_p, 2)}."],
    ["Chi phí CPU", f"Độ trễ forward của TSVM cao hơn khoảng {R('4.10 lần')} so với Baseline."],
]


def kq_table(rows):
    body = "".join(f'<tr><td class="l">{a}</td><td class="j">{b}</td></tr>' for a, b in rows)
    return (f'<div class="tbl kq"><table style="width:100%"><colgroup><col style="width:27%"><col></colgroup>'
            f'<thead><tr><th class="l">Kết quả</th><th class="l">Ý nghĩa</th></tr></thead><tbody>{body}</tbody></table></div>')


info = [
    ("Mã đề tài &amp; phân loại", "CNTT_KLCN182 – Khóa luận Cử nhân ngành CNTT, năm học 2026–2027"),
    ("Giảng viên hướng dẫn", "TS. Phùng Thế Bảo; email: baopt@huit.edu.vn"),
    ("Nhóm sinh viên thực hiện", "Lê Đức Lương – MSSV 2001230490 – Lớp 14DHTH09<br>Phùng Tuấn Huy – MSSV 2001230312 – Lớp 14DHTH13"
                                 "<br>Trần Mạnh Toàn – MSSV 2001230830 – Lớp 14DHTH09"),
    ("Nội dung trọng tâm", "So sánh Baseline và TSVM (checkpoint FP32) qua 20 seed; chất lượng phân đoạn, độ ổn định, "
                           "ma trận nhầm lẫn và chi phí suy luận CPU."),
    ("Ngày báo cáo", NGAY),
]
info_html = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in info)

doc = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Báo cáo 20 seed TSVM FP32</title>
<style>{CSS}</style></head><body>

<div class="head">
<div class="uni">TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP.HCM &nbsp;·&nbsp; KHOA CÔNG NGHỆ THÔNG TIN</div>
<div class="title">BÁO CÁO TIẾN ĐỘ<br>VÀ KẾT QUẢ THỰC NGHIỆM</div>
<div class="topic">Đề tài: Tích hợp Topology-Shape-aware VMamba vào YOLO26-seg<br>để phân đoạn polyp từ ảnh nội soi đại trực tràng</div>
</div>
<table class="info">{info_html}</table>

<h1><span class="n">1</span>Mục tiêu và kết quả chính</h1>
<p>Báo cáo so sánh YOLO26s-seg, gọi tắt là {B('Baseline')}, với mô hình tích hợp C2TSVMamba, gọi tắt là {B('TSVM')}.
Thực nghiệm sử dụng dữ liệu Kvasir_BG20 và 20 seed (0–19) cho mỗi mô hình. Checkpoint TSVM được lưu {B('FP32')} để tránh
lỗi tràn số FP16 của báo cáo trước.</p>
<h2>Kết quả chính</h2>
{kq_table(kq_rows)}
<h2>Các việc đã hoàn thành</h2>
<ul>
<li>Chuẩn hóa Kvasir_BG20 với 1.000 ảnh polyp và 200 ảnh nền không chứa polyp.</li>
<li>Hoàn thành 40 lượt huấn luyện: hai mô hình, mỗi mô hình 20 seed và 100 epoch.</li>
<li>Tổng hợp chỉ số tại epoch tốt nhất; kiểm định t theo cặp, Wilcoxon và Levene giữa hai mô hình.</li>
<li>Lưu checkpoint TSVM ở FP32 và kiểm tra lại ma trận nhầm lẫn của cả 40 lượt chạy.</li>
<li>Trình bày mười biểu đồ để so sánh ma trận nhầm lẫn, chất lượng phân đoạn và độ ổn định.</li>
<li>Đối chiếu số tham số, dung lượng trọng số và độ trễ suy luận trên CPU.</li>
</ul>

<h1 style="break-before:page"><span class="n">2</span>Mô hình và thiết lập thực nghiệm</h1>
<h2><span class="n">2.1</span>Dữ liệu Kvasir_BG20</h2>
<p>Ảnh nền được bổ sung để mô hình học phân biệt polyp với niêm mạc không có tổn thương. Tên BG20 thể hiện số ảnh nền bổ sung
bằng 20% số ảnh polyp; tỷ lệ ảnh nền trong toàn bộ dữ liệu là 16.67%.</p>
{table(["Tập dữ liệu", "Ảnh polyp", "Ảnh nền", "Tổng ảnh", "Số nhãn"],
       [["Huấn luyện", "880", "160", "1.040", "936"], ["Kiểm định", "120", "40", "160", "127"],
        ["Toàn bộ", "1.000", "200", "1.200", "1.063"]], "lrrrr", "Phân bố dữ liệu huấn luyện và kiểm định", bold_last=True)}
<h2><span class="n">2.2</span>Kiến trúc TSVM</h2>
<p>TSVM thay khối C2PSA tại tầng 10 của YOLO26s-seg bằng {B('C2TSVMamba')}. Khối đề xuất kết hợp quét không gian bốn hướng SS2D
với đặc trưng hình dạng, nhằm khai thác quan hệ giữa các vùng ảnh và hỗ trợ phân đoạn ranh giới polyp.</p>
<h2><span class="n">2.3</span>Tiền xử lý và tăng cường dữ liệu</h2>
<p>Ảnh đầu vào có kích thước 640 × 640 pixel. Mặt nạ được chuyển sang nhãn đa giác YOLO. Cấu hình tăng cường dữ liệu gồm lật ngang
0.5, co giãn 0.5 và Mosaic 1.0; Mosaic được tắt trong 10 epoch cuối.</p>
<h2><span class="n">2.4</span>Cấu hình huấn luyện</h2>
<p>Hai mô hình sử dụng cùng cấu hình huấn luyện và cùng các seed từ 0 đến 19. Một epoch là một lượt huấn luyện qua tập dữ liệu.</p>
<div class="kq">{table(["Tham số", "Thiết lập"], [
    ["Số seed", "20, từ 0 đến 19"], ["Kích thước ảnh", "640 × 640 pixel"], ["Batch", "8 ảnh"], ["Số epoch", "100"],
    ["Bộ tối ưu", "AdamW; weight_decay = 0.0005"], ["Tốc độ học", "lr0 = 0.001; lrf = 0.01; cos_lr = False"],
    ["Trọng số mất mát", "box = 7.5; seg = 7.5; cls = 0.5"],
    ["Chế độ tính toán", "deterministic = True; AMP = False; checkpoint TSVM lưu FP32"]],
    "ll", "Cấu hình huấn luyện chung", width="85%")}</div>

<h1><span class="n">3</span>Kết quả so sánh qua 20 seed</h1>
<p>Các chỉ số được lấy tại {B('epoch tốt nhất')} (Mask mAP@50-95 cao nhất) của từng lượt chạy. Giá trị trước và sau dấu ± lần lượt
là trung bình và độ lệch chuẩn; Δ là TSVM trừ Baseline. Cột <i>p</i> là kết quả kiểm định t theo cặp; <i>p</i> &lt; 0.05 được
dùng làm ngưỡng ý nghĩa thống kê. Cột Levene <i>p</i> kiểm định khác biệt độ phân tán giữa hai mô hình.</p>
<div class="kq">{plain_table(["Chỉ số", "Ý nghĩa"], [
    ["Mask", "Chỉ số phân đoạn mặt nạ."], ["Box", "Chỉ số phát hiện hộp bao."],
    ["Precision", "Độ chính xác của dự đoán."], ["Recall", "Khả năng phát hiện tổn thương."]], "ll", width="100%")}</div>
<h2><span class="n">3.1</span>Kết quả tổng hợp</h2>
{table(["Chỉ số", "Baseline", "TSVM", "Δ", "<i>p</i>", "Levene <i>p</i>"], rows3, "lcccrr",
       "So sánh các chỉ số chính qua 20 seed")}
<h2><span class="n">3.2</span>Kết quả từng seed</h2>
<p>TSVM đạt Mask mAP@50-95 cao hơn ở {wins}/20 seed: {", ".join(map(str, win_seeds[:-1]))} và {win_seeds[-1]}.
Bảng dưới dùng cùng chỉ số để đối chiếu từng cặp seed.</p>
{table([], rows4, "lccccr", "Mask mAP@50-95 tại epoch tốt nhất của từng seed", head_rows=head4)}
<h2><span class="n">3.3</span>Nhận xét và giới hạn thống kê</h2>
<p>TSVM {B('ổn định hơn rõ rệt')}, còn độ chính xác trung bình mới ở mức xu hướng. Độ lệch chuẩn Mask mAP@50-95 giảm từ
{m.baseline_sd:.4f} xuống {m.tsvm_sd:.4f}; kiểm định Levene cho {p_(m.levene_p, 3)}, nên mức giảm phân tán có ý nghĩa thống kê.
Mask mAP@50-95 tăng {m.delta:.4f} với {p_(m.p_ttest, 3)} (Wilcoxon {p_(m.p_wilcoxon, 3)}): gần ngưỡng nhưng
{R('chưa đủ bằng chứng')} ở mức 0.05.</p>
<p>Mất mát phân đoạn kiểm định giảm {loss_pct:.2f}%, từ {loss.baseline_mean:.4f} xuống {loss.tsvm_mean:.4f}
({p_(loss.p_ttest, 3)}); độ lệch chuẩn giảm {sd_loss:.1f}% (Levene {p_(loss.levene_p, 3)}). Các chỉ số còn lại có
<i>p</i> &gt; 0.2; Mask Recall gần như không đổi.</p>

<h1><span class="n">4</span>Ma trận nhầm lẫn và giới hạn dữ liệu</h1>
<p>Số liệu được đọc từ ảnh ma trận nhầm lẫn của 40 lượt chạy và đã kiểm tra chéo. Bảng chỉ dùng để mô tả, chưa dùng làm kết luận
lâm sàng.</p>
<p>Tập kiểm định gồm 120 ảnh polyp với 127 nhãn tổn thương và 40 ảnh nền. Số phát hiện đúng và bỏ sót được đếm theo nhãn tổn
thương; báo động giả (FP) được đếm theo dự đoán không khớp polyp nào. Hai mô hình gần như ngang nhau; TSVM có ít hơn
{abs(cmt.FP.mean() - cmb.FP.mean()):.1f} FP trung bình nhưng chênh lệch {R('không có ý nghĩa thống kê')} ({p_(fp_p, 2)}).</p>
{table(["Chỉ số", "Baseline", "TSVM", "Δ"], rows5, "lccr", "Tổng hợp số phát hiện đúng, bỏ sót và báo động giả")}
{figure("12_confusion_matrix_mean_comparison.png", "70%", "Ma trận nhầm lẫn trung bình 20 seed của Baseline, TSVM và chênh lệch giữa hai mô hình.")}
<p>Ma trận nhầm lẫn không cho thấy khác biệt đáng kể. Khả năng phát hiện polyp gần như trùng nhau (TP 0.87, FN 0.13 ở cả hai).
Tỷ lệ FP trên tổng dự đoán của TSVM thấp hơn nhẹ ({fp_rate['b'].mean() / 100:.3f} xuống {fp_rate['t'].mean() / 100:.3f}), nhưng
TSVM chỉ ít FP hơn ở {fp_fewer}/20 seed, nhiều hơn ở {fp_more}/20 seed, nên đây {R('chưa phải ưu thế')}. Ô TN để trống vì
Ultralytics không đếm ô nền–nền.</p>
<p><b>Giới hạn cần lưu ý:</b> với bài toán phân đoạn thực thể, Ultralytics không đếm ô nền–nền nên TN và độ đặc hiệu không xác
định; báo cáo không trình bày hai chỉ số này. FP là dự đoán không khớp với polyp nào, phần lớn do mô hình khoanh lệch polyp, nên
một polyp khoanh lệch thường bị tính cả FN lẫn FP. Vì vậy, tỷ lệ FP được tính trên tổng dự đoán (FP / (TP + FP)), không chia cho
40 ảnh nền. Kiểm tra riêng bằng code ở seed 1 cho thấy 0/40 ảnh nền bị báo nhầm.</p>
<p><b>Kiểm tra chéo:</b> với Baseline seed 0–9, số đọc được khớp hoàn toàn với bảng đã xác minh của báo cáo 10 seed. Với TSVM FP32,
cả 20 seed đều có TP + FN = 127 và tỷ lệ TP sát Box Recall (lệch ≤ 0.04); hiện tượng sai lệch ở seed 0, 5 và 8 của bản lưu FP16
không còn.</p>

<h1><span class="n">5</span>Biểu đồ so sánh thực nghiệm</h1>
<p>Chín biểu đồ dưới đây được lấy từ thư mục KQ_Nen_DX_20seed_FP32/figures. Mỗi hình tập trung vào một khía cạnh của kết quả;
nhận xét chỉ giới hạn trong 20 seed đã khảo sát.</p>
<div class="keep"><h2><span class="n">5.1</span>Các chỉ số phân đoạn chính</h2>
{figure("01_overall_benchmark_barchart.png", "60%", "So sánh bốn chỉ số phân đoạn và độ lệch chuẩn qua 20 seed.")}</div>
<p>TSVM nhỉnh hơn ở Mask mAP@50-95 (+0.0043) và Precision (+0.0104); Mask mAP@50 và Recall gần như bằng nhau. Thanh sai số của
TSVM ngắn hơn ở cả bốn chỉ số, tức kết quả ít phụ thuộc seed hơn.</p>
<div class="keep"><h2><span class="n">5.2</span>Mất mát phân đoạn kiểm định</h2>
{figure("02_val_seg_loss_barchart.png", "42%", "Trung bình và độ lệch chuẩn của mất mát phân đoạn kiểm định.")}</div>
<p>Loss của TSVM thấp hơn {loss_pct:.2f}% và độ lệch chuẩn chỉ bằng khoảng một nửa ({loss.tsvm_sd:.4f} so với
{loss.baseline_sd:.4f}). Đây là tín hiệu tối ưu hóa ổn định hơn, dù chênh lệch trung bình {R('chưa đạt ý nghĩa thống kê')}.</p>
<div class="keep"><h2><span class="n">5.3</span>So sánh từng seed</h2>
{figure("03_seed_by_seed_barchart.png", "100%", "Mask mAP@50-95 của hai mô hình tại từng seed.")}</div>
<p>TSVM thắng {wins}/20 seed. Đáng chú ý hơn là mức đáy: seed thấp nhất của TSVM đạt {tsvm.mask_map50_95.min():.4f}
(seed {int(tsvm.mask_map50_95.idxmin())}), còn Baseline xuống {base.mask_map50_95.min():.4f} (seed {int(base.mask_map50_95.idxmin())}).</p>
<div class="keep"><h2><span class="n">5.4</span>Diễn biến hàm mất mát</h2>
{figure("04_convergence_loss_curves.png", "68%", "Diễn biến bốn hàm mất mát qua 100 epoch (trung bình ± 1 độ lệch chuẩn, 20 seed).")}</div>
<p>Hai mô hình hội tụ theo cùng một nhịp. Ở 10 epoch cuối, TSVM có mất mát phân đoạn kiểm định thấp hơn (1.260 so với 1.300)
nhưng mất mát phân loại kiểm định cao hơn (0.624 so với 0.609); vì vậy không dùng riêng các đường cong này để kết luận.</p>
<div class="keep"><h2><span class="n">5.5</span>Diễn biến chỉ số mAP</h2>
{figure("05_metric_curves_mAP.png", "100%", "Mask mAP@50-95 và Mask mAP@50 qua 100 epoch.")}</div>
<p>Hai đường trung bình gần như trùng nhau; TSVM cao hơn nhẹ ở Mask mAP@50-95 trong 10 epoch cuối (0.710 so với 0.706). Khác biệt
chính giữa hai mô hình nằm ở độ phân tán giữa các seed, không nằm ở tốc độ học.</p>
<div class="keep"><h2><span class="n">5.6</span>Tỷ lệ đạt kết quả cao hơn</h2>
{figure("07b_pie_head_to_head_winrate.png", "36%", f"Tỷ lệ thắng theo Mask mAP@50-95: TSVM {wins * 5}%, Baseline {losses * 5}%.")}</div>
<p>TSVM thắng {wins}/20 cặp seed, nhưng kiểm định dấu hai phía cho {p_(sign_p)}: tỷ lệ thắng {R('chưa đủ bằng chứng')} để kết
luận ưu thế. Cần đọc cùng mức chênh trung bình ở Bảng 3.</p>
<div class="keep"><h2><span class="n">5.7</span>Khoảng biến thiên qua các epoch</h2>
{figure("09_metric_stability_band_area.png", "62%", "Giá trị nhỏ nhất, lớn nhất và trung bình của Mask mAP@50-95.")}</div>
<p>Theo từng epoch, dải dao động của hai mô hình tương đương: TSVM hẹp hơn ở 53/100 epoch và độ rộng trung bình gần như bằng nhau
(+0.76%). Như vậy, ưu thế ổn định của TSVM thể hiện ở epoch tốt nhất, không phải suốt quá trình huấn luyện.</p>
<div class="keep"><h2><span class="n">5.8</span>Cân bằng giữa phát hiện và phân đoạn</h2>
{figure("10_radar_multiobjective_tradeoff.png", "42%", "Biểu đồ radar so sánh tám chỉ số Box và Mask.")}</div>
<p>TSVM cao hơn ở 7/8 trục nhưng mọi chênh lệch đều nhỏ (≤ 0.010); chỉ Mask Recall thấp hơn không đáng kể (−0.0004). Cải thiện
dàn đều, không có trục nào bứt phá.</p>
<div class="keep"><h2><span class="n">5.9</span>Phân bố kết quả giữa các seed</h2>
{figure("11_boxplot_variance_stability.png", "48%", "Phân bố Mask mAP@50-95 qua 20 seed.")}</div>
<p>Trung vị của TSVM là {tsvm.mask_map50_95.median():.4f}, cao hơn mức {base.mask_map50_95.median():.4f} của Baseline. Hộp của
TSVM hẹp hơn rõ rệt; số seed dưới 0.71 là {low_t} so với {low_b} của Baseline.</p>

<h1><span class="n">6</span>Chi phí tính toán và khả năng triển khai</h1>
<p>Hai mô hình được so sánh về số tham số, dung lượng trọng số và tốc độ suy luận trên CPU. Phép đo sử dụng trọng số của seed 0,
đầu vào 640 × 640 pixel, với 20 lượt khởi động và 100 lượt đo. Thời gian đo chưa bao gồm tiền xử lý và hậu xử lý. Kiến trúc không
đổi so với báo cáo 10 seed nên số liệu đo được giữ nguyên.</p>
{table(["Chỉ số", "Baseline", "TSVM", "Chênh lệch"], [
    ["Số tham số, triệu", "11.434", "12.255", "+0.821"], ["THOP, GMACs", "18.54", "18.86", "+0.32"],
    ["Trọng số FP16, MiB", "22.27", "23.86", "+1.59"], ["Độ trễ, ms/ảnh", "<b>200.12</b>", "821.27", "+621.15"],
    ["Tốc độ, FPS", "<b>5.00</b>", "1.22", "−3.78"], ["GPU VRAM", "chưa xác minh", "chưa xác minh", "chưa xác định"]],
    "lrrr", "Chi phí tài nguyên và tốc độ forward CPU")}
<p>Chi phí là điểm yếu chính: số tham số chỉ tăng 7.18% nhưng độ trễ forward CPU cao hơn khoảng {R('4.10 lần')}; số MAC do THOP
đếm chưa bao quát đầy đủ các phép scan. Khi lưu FP32, tệp trọng số TSVM khoảng 47 MiB (ước tính 4 byte mỗi tham số). Chưa có
phép đo trên GPU nên chưa thể kết luận về khả năng xử lý thời gian thực.</p>

<h1><span class="n">7</span>Thay đổi so với báo cáo 10 seed và đối chiếu kết quả</h1>
<p>So với báo cáo 10 seed, nhóm mở rộng lên 20 seed cho mỗi mô hình và chuyển checkpoint TSVM sang lưu FP32. Bản lưu FP16 trước
đây làm tràn thống kê BatchNorm tại tầng 10, khiến ma trận nhầm lẫn của TSVM ở seed 0, 5 và 8 bị sai.</p>
<div class="kq">{table(["Nội dung", "Báo cáo 10 seed", "Báo cáo 20 seed"], [
    ["Số lượt chạy", "Hai mô hình, mỗi mô hình 10 seed; tổng 20 lượt", "Hai mô hình, mỗi mô hình 20 seed; tổng 40 lượt"],
    ["Lưu checkpoint TSVM", "FP16; thống kê BatchNorm tầng 10 bị tràn số", "FP32; không còn tràn số"],
    ["Dữ liệu", "Kvasir_BG20: 1.200 ảnh, 200 ảnh nền", "Giữ nguyên"],
    ["Mask mAP@50-95 Baseline", "0.7210 ± 0.0129", f"{m.baseline_mean:.4f} ± {m.baseline_sd:.4f}"],
    ["Mask mAP@50-95 TSVM", "0.7246 ± 0.0078", f"{m.tsvm_mean:.4f} ± {m.tsvm_sd:.4f}"],
    ["<i>p</i> của Mask mAP@50-95", "0.3839", f"{m.p_ttest:.4f}"],
    ["Ma trận nhầm lẫn", "Chưa dùng làm kết luận; TSVM seed 0, 5, 8 sai lệch", "Nhất quán ở cả 40 lượt; dùng để mô tả"]],
    "lll", "Những điều chỉnh chính so với báo cáo 10 seed", width="100%")}</div>
<p>Huấn luyện có tính tất định: chỉ số trong results.csv của TSVM FP32 tại seed 0–9 trùng với báo cáo 10 seed. Vì vậy, thay đổi
về kết quả đến từ 10 seed bổ sung chứ không do cách lưu checkpoint.</p>
<p>Khi thêm 10 seed, trung bình của cả hai mô hình giảm nhẹ nhưng chênh lệch vẫn nghiêng về TSVM (+0.0036 lên +{m.delta:.4f}),
và <i>p</i> giảm từ 0.384 xuống {m.p_ttest:.3f}.</p>

<h1><span class="n">8</span>Kết luận và giới hạn</h1>
<h2>Kết quả chính</h2>
{kq_table([
    ["Độ ổn định", f"Phương sai Mask mAP@50-95 của TSVM thấp hơn {B('có ý nghĩa thống kê')} (Levene {p_(m.levene_p, 3)}); "
                   f"độ lệch chuẩn val seg loss giảm {sd_loss:.1f}%."],
    ["Chất lượng phân đoạn", f"Mask mAP@50-95 tăng {m.delta:.4f} nhưng {R('chưa đạt ý nghĩa thống kê')} ở ngưỡng 0.05 "
                             f"({p_(m.p_ttest, 3)})."],
    ["Ma trận nhầm lẫn", f"TP, FN gần như trùng nhau; chênh lệch FP không có ý nghĩa ({p_(fp_p, 2)})."],
    ["Chi phí suy luận", "Tăng khoảng 7.18% số tham số, độ trễ forward CPU cao hơn khoảng 4.10 lần."],
    ["Checkpoint FP32", "Không còn tràn số BatchNorm; ma trận nhầm lẫn nhất quán ở cả 40 lượt chạy."],
])}
<h2>Giới hạn cần báo cáo</h2>
<ul>
<li>Mask mAP@50-95 có {p_(m.p_ttest, 3)}; {R('chưa đủ bằng chứng')} kết luận TSVM có trung bình cao hơn.</li>
<li>Tỷ lệ thắng {wins}/20 seed có {p_(sign_p)} (kiểm định dấu), chưa chứng tỏ ưu thế.</li>
<li>Ưu thế ổn định thể hiện ở epoch tốt nhất; dải dao động theo epoch chỉ hẹp hơn ở 53/100 epoch.</li>
<li>Epoch tốt nhất được chọn trên chính tập kiểm định; cần kiểm thử trên dữ liệu độc lập.</li>
<li>TN và độ đặc hiệu không xác định với phân đoạn thực thể; ma trận nhầm lẫn chỉ dùng để mô tả.</li>
<li>Số MAC do THOP đếm chưa bao quát đầy đủ các phép scan; chưa có phép đo toàn chuỗi trên GPU và GPU VRAM chưa xác minh,
nên chưa thể kết luận đáp ứng xử lý thời gian thực.</li>
</ul>
<h2>Bước tiếp theo</h2>
<p>Đo tốc độ toàn chuỗi trên GPU, kiểm thử trên dữ liệu độc lập và giảm độ trễ của khối SS2D trước khi xây dựng ứng dụng
thử nghiệm.</p>
<div class="sign"><i>{NGAY}</i><br><b>ĐẠI DIỆN NHÓM SINH VIÊN THỰC HIỆN</b><br>
<b>Lê Đức Lương — Phùng Tuấn Huy — Trần Mạnh Toàn</b></div>
</body></html>"""

if __name__ == "__main__":  # tao_bao_cao_20seed_word.py imports `doc` from here
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "bao_cao_20seed.html"
        page.write_text(doc, encoding="utf-8")
        subprocess.run([str(EDGE), "--headless", "--disable-gpu", f"--user-data-dir={Path(tmp) / 'edge'}",
                        "--no-pdf-header-footer", f"--print-to-pdf={OUT}", page.as_uri()], check=True, timeout=180)
    print("saved", OUT)
