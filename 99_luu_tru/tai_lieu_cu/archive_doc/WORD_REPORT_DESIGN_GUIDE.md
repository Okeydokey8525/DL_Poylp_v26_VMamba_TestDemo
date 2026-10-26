# WORD REPORT DESIGN GUIDE — HƯỚNG DẪN THIẾT KẾ BÁO CÁO WORD TỪ MARKDOWN

**SOURCE SCOPE:** `archive/` only. Every specification below is backed by a file that exists inside `archive/`. Where the archive does not prove a rule, this guide writes **`NOT SPECIFIED`** and does not invent one.

---

## 0. EVIDENCE BASIS FOR THIS GUIDE

| # | Source | Type | What it proves |
|---|---|---|---|
| E1 | `archive/doc/19_QUY_CHUAN_THIET_KE_WORD_LE_DUC_LUONG.md` | Specification doc | Design system: margins, font hierarchy, table/figure rules |
| E2 | `archive/doc/15_CAM_NANG_PHONG_CACH_WORD_VA_NGON_NGU_HOC_THUAT.md` | Style guide | Report structure, table/figure rules, academic phrasing templates |
| E3 | `archive/Bao_cao/CNTT_KLCN182_LeDucLuong.docx` | **Primary artifact** (`word/document.xml`, 402 paragraphs) | Shipped formatting: margins, fonts, sizes, indents, captions, chapter outline |
| E4 | `archive/Stracth/generate_final_word_report.py` (783 lines) | **Primary artifact** (code) | Executable recipe that produced E3 |
| E5 | `archive/Stracth/build_word_report_bg20_10seeds.py` | **Primary artifact** (code) | Second generator, same conventions |
| E6 | `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/06_reports/recommended_figures_for_thesis.md` | Audited report | Thesis-worthy figures and LaTeX metric table |
| E7 | `archive/Ket_Qua_V2/KQ_Nen_DX_10seed/reports/chart_template_mapping.md` | Stale inventory | Historical chart layout (superseded) |

**Precedence rule:** E3/E4/E5 (real artifact + code) beat E1/E2 (prose spec) when they disagree. See §3.3.

### 0.1 What may be reused, and what must NOT be copied

| Content | Reusable? | Reason |
|---|---|---|
| Page setup, fonts, sizes, indents, spacing (E3, E4) | **YES** | Verified directly in the shipped `.docx` XML |
| 6-chapter report skeleton (§1) | **YES** | Verified against the real outline extracted from E3 |
| Table / figure caption wording patterns (§6) | **YES** | Verified in E3 |
| Figure observation formula — "two-axis" commentary (§5) | **YES as structure** | Structure verified; any filled example must use real artifact values |
| LaTeX metric table in E6 | **YES** | Values match `full_comparison_mean_std.csv` exactly |
| Numeric example sentences in `doc/15` §2.1–§2.5 | **NO** | 6-fold-era values (1.3987, 4.39, 25.0 ms, 40 FPS) — `OUTDATED` per `archive/MARKDOWN_CLAIM_AUDIT.md` |
| `doc/15` §1.1 margins (left 3.00 cm, top/bottom 1.50 cm) | **NO** | Contradicted by the real `.docx` (`w:left="1984"` = 3.5 cm) |
| Claims from `doc/08`, 6-fold reports, or the stale 4-model efficiency draft | **NO** | `CONTRADICTED` / `UNVERIFIED` per the claim audit |
| `chart_template_mapping.md` §2 folder inventory | **NO** | `OUTDATED` — those folders no longer exist |

---

## 1. REPORT STRUCTURE

### 1.1 Canonical 6-chapter skeleton

Proven by the real `.docx` outline (`E3`) and mandated by `doc/15` §1.4. **`doc/15` explicitly forbids adding a 7th "weekly plan checklist" chapter.**

| Ch. | Title (from E3) | Level-2 subsections (from E3) |
|---:|---|---|
| — | Title block + metadata table (§4.7) | — |
| 1 | `MỤC TIÊU VÀ NHIỆM VỤ BÁO CÁO TIẾN ĐỘ` | *(none in E3)* |
| 2 | `CẤU TRÚC MÔ HÌNH VÀ TIỀN XỬ LÝ DỮ LIỆU BG20` | 2.1 Vai trò tích hợp VMamba · 2.2 Bộ dữ liệu + nhãn rỗng · 2.3 Tiền xử lý & tăng cường · 2.4 Môi trường & siêu tham số tất định |
| 3 | `KẾT QUẢ ĐỊNH LƯỢNG ĐỐI CHỨNG QUA 10 SEED` | 3.1 Bảng tổng hợp · 3.2 Đối chiếng từng seed · 3.3 Paired t-test & co hẹp phương sai |
| 4 | `MA TRẬN NHẦM LẪN VÀ ĐÁNH GIÁ CHỈ SỐ LÂM SÀNG NỘI SOI` | *(none in E3)* |
| 5 | `HỆ THỐNG TRỰC QUAN HÓA THỰC NGHIỆM ĐA CHIỀU` | 5.1–5.12, one subsection per figure (verified: 12) |
| 6 | `ĐÁNH GIÁ CHI PHÍ TÍNH TOÁN VÀ TÍNH KHẢ THI TRIỂN KHAI THỜI GIAN THỰC` | *(none in E3)* |

Heading text is stored **UPPERCASE** at level 1 (`add_le_duc_luong_heading_1` calls `text.upper()` in E4).

### 1.2 Front matter order (E3)

1. Document title — `BÁO CÁO TIẾN ĐỘ THỰC NGHIỆM VÀ KẾT QUẢ NGHIÊN CỨU TUẦN`
2. Topic line — `Đề tài: Nghiên cứu phương pháp tích hợp Topology-Shape-aware VMamba vào mô hình YOLO26-seg trong phân đoạn polyp…`
3. Metadata table: Mã đề tài & Phân loại · Giảng viên hướng dẫn · Nhóm sinh viên thực hiện · Nội dung báo cáo trọng tâm
4. Chapter 1 … Chapter 6

---

## 2. HEADING HIERARCHY

Three levels only. Verified in E1 §3.1 and implemented in E4.

| Level | Pattern (from E3) | Size | Style | Alignment | Indent |
|---|---|---:|---|---|---|
| Title | — | 13.0 pt | UPPERCASE, BOLD | CENTER | 0 |
| Topic | — | 15.0 pt | BOLD ITALIC | CENTER | 0 |
---

## 3. PAGE SETUP, FONT, SPACING

### 3.1 Page setup — PROVEN from `word/document.xml` (E3)

```xml
<w:pgSz w:w="11906" w:h="16838"/>
<w:pgMar w:top="1417" w:right="1417" w:bottom="1417" w:left="1984"
         w:header="720" w:footer="720" w:gutter="0"/>
```

| Property | Value | twips | cm |
|---|---|---:|---:|
| Paper | A4 | 11906 × 16838 | 21.0 × 29.7 |
| Top margin | `w:top="1417"` | 1417 | **2.50** |
| Bottom margin | `w:bottom="1417"` | 1417 | **2.50** |
| Right margin | `w:right="1417"` | 1417 | **2.50** |
| **Left margin** | `w:left="1984"` | 1984 | **3.50** (binding gutter) |
| Header distance | `w:header="720"` | 720 | **1.27** |
| Footer distance | `w:footer="720"` | 720 | **1.27** |
| Printable width | 21.0 − 3.5 − 2.5 | — | **15.00** |

This matches `doc/19` §2 and the code in E4 lines 83–90 exactly.

### 3.2 Font and sizes — PROVEN (E3 font census)

`w:ascii` census of the whole document: **408 × `Times New Roman`, zero other fonts.** Single font confirmed.

| Component | Size | Style | Occurrences in E3 |
|---|---:|---|---:|
| Body / headings | 13.0 pt | see §2 | 94 |
| Figure & table captions | 12.0 pt | see §5–§6 | 18 |
| Topic title | 15.0 pt | BOLD ITALIC | 1 |
| Table cell text | 11.0 pt | Regular | 196 |
| Table cell text (secondary) | 10.5 pt | Regular | 99 |

Line/paragraph spacing: body `space_before = Pt(3.0)`, `space_after = Pt(3.0)`, `line_spacing = 1.25` (E4 lines 146–148).
Heading spacing in E4: `space_before = Pt(6.0)`, `space_after = Pt(4.0)`, H2 `Pt(5.0)/Pt(2.0)`, H3 `Pt(4.0)/Pt(2.0)`, all `line_spacing = 1.25`.
First-line indent: **720 twips = 1.27 cm** — exactly 30 occurrences in E3, all on body paragraphs (E4 line 145).

### 3.3 Known conflict — resolved by primary artifact

| Property | `doc/15` §1.1 | `doc/19` §2 | **`.docx` XML (authoritative)** |
|---|---|---|---|
| Left margin | 3.00 cm | 3.50 cm | **3.50 cm** |
| Top / Bottom | 1.50 cm | 2.50 cm | **2.50 cm** |
| Right | 2.00 cm | 2.50 cm | **2.50 cm** |
| Printable width | ~16.0 cm | 15.00 cm | **15.00 cm** |

⇒ **Use `doc/19` / the `.docx` values.** `doc/15` §1.1 is superseded for geometry. Image width limit is governed by 15.00 cm, not 15.80 cm (§5).

---

## 5. FIGURE / IMAGE RULES

From `doc/19` §5 and `doc/15` §1.7, verified against E3/E4.

1. **Never place a figure alone.** Every figure is a fixed triplet: image → caption → observation paragraph. (`doc/19` §5 calls this the single most important point of the style.)
2. **Alignment:** image centred (`WD_ALIGN_PARAGRAPH.CENTER`), `first_line_indent = None`, `space_before = Pt(6.0)`, `space_after = Pt(2.0)`.
3. **Width:** must fit the printable width. `doc/19` §5.1 says 14.50–15.80 cm and its checklist says `≤ 15.80 cm`, but §2 sets the printable width at **15.00 cm**. **Use ≤ 15.00 cm** so nothing crosses the right margin. `doc/15` §1.7 gives the same range but derives it from a 16.0 cm printable width, which is superseded.
4. **Aspect ratio:** preserve the source ratio — never distort.
5. **Caption:** directly **below** the image, centred, 12.0 pt, wording `Hình X. <description>`.
6. **Observation paragraph:** directly below the caption, JUSTIFY, first-line indent 1.27 cm, 13 pt.
7. Only use figures that exist on disk. Verified sets: 12 files in `Ket_Qua_V2/KQ_Nen_DX_10seed/figures/`, 16 PNGs in `05_charts/`, 15 PNGs in `efficiency_benchmark/figures/`. See `archive/15_CLAIM_FAMILIES_REVIEW.md` for which historical figures must not be reused.

### 5.1 The two-axis observation formula

`doc/19` §5.2 mandates that every figure observation analyse **two axes**:

1. **Deep-learning technical axis** — convergence behaviour over 100 epochs, inflection points, variance contraction, quantitative figures with `Mean ± Std` and `Δ`, and the architectural mechanism.
2. **Clinical endoscopy axis** — patient-protection effect (Recall / missed lesions), burden on the endoscopist (False Positive on normal mucosa, relevant because 20 % of images are background negatives), segmentation quality, and real-time feasibility.

**Constraint:** this formula governs *structure*, not licence. Any numeric statement inside an observation must still pass §7 and §11. In particular the ">30 FPS real-time" branch is **not currently supportable** — the only file-backed latency measurement is CPU `thop` timing at 5.00 / 1.22 FPS.

---

## 6. CAPTION AND NUMBERING CONVENTIONS

Verified wording taken from the shipped document (E3):

| Kind | Pattern | Position | Actual examples found in E3 |
|---|---|---|---|
| Table | `Bảng X: …` (colon) | **above** table | `Bảng 1: Thống kê chi tiết phân chia bộ dữ liệu chuẩn Kvasir_YOLO_SEG_BG20 (20% ảnh nền)`; `Bảng 3: … (Mean ± Std, Min/Max, p-value)`; `Bảng 6: So sánh chi phí tính toán, mức chiếm dụng bộ nhớ và tốc độ suy luận thời gian thực` |
| Figure | `Hình X. …` (period) | **below** image | `Hình 1. Biểu đồ cột đôi so sánh tổng thể 4 chỉ số phân vùng chính kèm thanh sai số ±1σ qua 10 seed`; `Hình 12. Biểu đồ cột nhóm so sánh số lượng ca tổn thương…` |

Rules:
- Numbering is **sequential per kind** (`Bảng 1…6`, `Hình 1…12` in the shipped report) and written **literally into the text** (no auto-field numbering in E3).
- Every figure caption is **followed by an observation paragraph** beginning `Hình X …` in the shipped document (e.g. `Hình 1 biểu diễn biểu đồ cột đôi so sánh…`). Preserve that pattern.
- Captions must not contain `chứng minh` or any significance claim — see §11.

---

## 7. FORMULA AND METRIC WRITING RULES

### 7.1 Notation (verified in E3/E6)

| Quantity | Notation | Example from archive |
|---|---|---|
| Central tendency ± dispersion | `Mean ± Std` (σ) | `0.7246 ± 0.0078` |
| Per-metric difference | `Δ` (TSVM − Baseline) | `Δ = +0.0036` |
| Percent change | `%` | `+0.49 %` |
| p-value (paired t-test) | `p` | `p = 0.0908` |
| Variance ratio | `F = …` | `F = 2.75×` |

Metric families in the evidence: Mask mAP@50-95, Mask mAP@50, Mask Precision, Mask Recall, Box mAP@50-95, Box mAP@50, Box Precision, Box Recall, Val Seg/Box/Cls/L1 Loss, Best Epoch; plus FPS, GFLOPs and Params (M) for cost.

### 7.2 Mandatory accuracy rules for metrics

1. **Never round away a digit that carries meaning.** `doc/19` §7 checklist: *"Giữ nguyên 100% số liệu gốc… tuyệt đối không bịa số hay làm tròn sai lệch."*
2. **Always show dispersion** for any multi-seed figure (`Mean ± Std`), never a bare mean.
3. **A descriptive improvement is not a statistical claim.** Write "mean Mask mAP@50-95 is higher (0.7246 vs 0.7210, Δ = +0.0036, p = 0.3839)". Never "significantly improves". Verified: **no metric in the 10-seed study reaches p ≤ 0.05** — `full_comparison_mean_std.csv` has `statistically_significant_005 = False` on all 13 rows.
4. **Never invent a metric absent from the package.** No IoU / mIoU / Dice / F1 column exists in `raw_10seeds_extracted_metrics.csv` (21 fields).
5. **TN / Specificity must never be presented as measured.** It is reconstructed as `40 − FP` because `ConfusionMatrix.process_batch` never increments the background↔background cell.
6. **Dataset counts keep their units.** 160 validation *images* = 120 polyp images carrying **127 objects** + 40 background images. Never write "167 images".
### 3.4 Rules not specified by the archive

Line numbering, page-number format, header/footer text content, widow/orphan control, theme colours, and `styles.xml` contents beyond what is listed above ⇒ **`NOT SPECIFIED`**. Do not invent them. One helper does exist in E4 line 32: `set_cell_margins(cell, top=100, bottom=100, left=150, right=150)` — the only cell-padding evidence in the archive.

---

## 4. TABLE RULES

From `doc/19` §4 and `doc/15` §1.6, verified against the shipped document (7 tables, 6 `tblHeader`, 54 `cantSplit`).

1. **Caption placement: ABOVE the table.** Format `Bảng X: <description>`, 12.0 pt italic, left/justified, indent 0. Confirmed in E3: `Bảng 1: Thống kê chi tiết…` precedes the table.
2. **Header row:** light grey fill (`#F2F2F2` or `#F7F7F7`), **BOLD**, centred horizontally **and** vertically.
3. **Repeat header across pages:** set `<w:tblHeader/>`. **Prevent row splitting:** `<w:cantSplit/>`. Both present in the shipped file and set by E4.
4. **Cell alignment:** numeric data (mAP, Precision, Recall, Loss, FPS, p-value, parameters) → **CENTRE**. Text, model names, clinical interpretation → **LEFT** / justified.
5. **Measurement formatting:** values with dispersion are written `Mean ± Std`, e.g. `0.7246 ± 0.0078`.
6. **Borders:** thin horizontal rules, grey `#B0B0B0`, `0.5 pt` (`sz="4"`); vertical rules minimal or hidden. Metadata table borders `0.75 pt` (`sz="6"`), grey `#999999`/`#CCCCCC`.
7. **Metadata table:** 2 columns (~5.37 cm / ~9.63 cm); column 1 shaded `#F7F7F7` + BOLD 13 pt; column 2 unshaded, regular 13 pt.
8. Table cells have **no first-line indent** (0 cm).
| **H1** | `1. MỤC TIÊU…` | 13.0 pt | UPPERCASE, BOLD | JUSTIFY/LEFT | 0 |
| **H2** | `2.1. Vai trò…` | 13.0 pt | BOLD | JUSTIFY/LEFT | 0 |
| **H3** | `5.10.1. …` | 13.0 pt | BOLD ITALIC | JUSTIFY/LEFT | 0 |

> **Automatic TOC / outline levels:** `doc/15` §1.5 and `doc/19` §3.1 describe `outlineLvl` 0/1/2 and a `{ TOC \o "1-3" \h \z \u }` field. **The shipped `.docx` contains zero `pStyle` and zero TOC fields** (verified), and E4 builds headings with plain `add_paragraph()` + manual uppercase. The shipped report therefore uses **manual numbering, no automatic TOC**. Treat `outlineLvl`/TOC as an *optional enhancement*, not an existing feature.
---

## 8. RESULTS-PRESENTATION RULES

1. **Lead with the source.** Every quantitative statement must trace to a file under `archive/Ket_Qua_V2/`. Precedence: raw `results.csv` → derived CSVs (`01_raw_analysis`, `02_statistics`, `03_metrics`, `04_confusion_matrix`, `06_reports`) → narrative Markdown.
2. **Report both directions.** Several metrics favour Baseline (Mask mAP@50, Val Cls Loss). A results section listing only the favourable direction is an overclaim.
3. **Seed-level detail belongs in its own subsection** (`3.2` in E3), separate from the summary table (`3.1`).
4. **Statistically framed subsections (`3.3`) must state the test used** (paired t-test) and the minimum p-value.
5. **Cost/latency subsection (chapter 6) must name its hardware and method.** The only file-backed cost generation is `thop` profiling + CPU timing; VRAM is `N/A`. Do not present GPU numbers.
6. **Clinical-impact language is mandatory after each figure** (§5.1) but must stay proportional to the evidence — see §11.

---

## 9. CITATION AND REFERENCE RULES

**Finding: the archive contains no citation/reference standard.** The shipped `.docx` (E3) contains **zero** bibliography fields, **zero** `[1]`-style in-text citations and **zero** `numPr` numbered lists. Verified.

Therefore:
- Citation style, reference-list format, bibliography heading ⇒ **`NOT SPECIFIED`**.
- Dataset attribution: the archive names the dataset (`Kvasir-SEG`, `Kvasir_YOLO_SEG_BG20`) and the negative-image source (`normal-cecum` from Kvasir v2) inside body text only. Reproduce that as **plain body text**, not as a formal citation.
- The only external artefact present is `archive/Kvasir-SEG/Kvasir-SEG/1911.07069.pdf`. **No rule exists for citing it**; adding a citation style would be invention.

---

## 10. MARKDOWN → WORD CONVERSION RULES

### 10.1 Heading conversion

| Markdown | Word |
|---|---|
| `#` | 13.0 pt UPPERCASE BOLD, numbered `1.`, `2.` …, centred/justified, indent 0 |
| `##` | 13.0 pt BOLD, numbered `2.1.`, indent 0 |
| `###` | 13.0 pt BOLD ITALIC, numbered `5.10.1.`, indent 0 |

Uppercasing is applied programmatically (`text.upper()` in E4) for level 1.

### 10.2 Body conversion

- Every body paragraph: `alignment = JUSTIFY`, `first_line_indent = Cm(1.27)`, `space_before = Pt(3.0)`, `space_after = Pt(3.0)`, `line_spacing = 1.25`, 13.0 pt Times New Roman.
- **Never** emit blank paragraphs from repeated `Enter` / blank Markdown lines. Spacing is controlled exclusively by `space_before` / `space_after` (`doc/19` §1 principle 2).
- Markdown tables → Word tables using §4. First Markdown table row = header row.
- `![alt](path)` → image + `Hình X.` caption + observation paragraph (§5). Verify the image file exists before inserting.
- Math: `$...$` / LaTeX segments are kept as literal text in the shipped document; **no equation object** is created. Reproduce as-is.

### 10.3 Reference implementation

The archive ships working generators. Prefer adapting them over writing a new pipeline:

- `archive/Stracth/generate_final_word_report.py` — produced the current shipped `.docx`
- `archive/Stracth/build_word_report_bg20_10seeds.py`
- Helper functions in E4: `apply_le_duc_luong_page_setup()`, `add_le_duc_luong_heading_1()`, `add_le_duc_luong_body_paragraph()`, `add_le_duc_luong_figure_block()`

The figure helper implements exactly the image → caption → observation triplet required by §5.
---

## 11. CONTENT THAT MUST NOT BE INFERRED OR OVERSTATED

Hard prohibitions, derived from `archive/MARKDOWN_CLAIM_AUDIT.md` (56 `CONTRADICTED`, 8 `OUTDATED`, 12 `PROVENANCE_ISSUE`).

**Never write:**
- "chứng minh vượt trội", "significantly better", "vượt trội hoàn toàn", "best", "definitively", "hoàn toàn", "100 % chắc chắn" — no metric reaches p ≤ 0.05.
- "more stable" / "ổn định hơn" as a global claim — dispersion contracts on *some* metrics and not others; always name the metric.
- Any TN / Specificity value as a *measurement*; always label it `TN = 40 − FP` (reconstructed).
- "167 ảnh" or any conflation of 127 objects with 160 images.
- "47 runs", "4 models", "40 `results.csv`" — the archive holds 20 `results.csv` for 2 models.
- GPU cost/latency figures (11.55/12.16 M, 42.3/47.4 GFLOPs, 17.2/19.8 ms, 58.1/50.5 FPS, VRAM 1.42/1.68 GB) attributed to the efficiency CSV — that CSV contains 11.434/12.255 M, 18.54/18.86 GFLOPs, 200.12/821.27 ms, 5.00/1.22 FPS, VRAM `N/A`.
- P5 VMamba / ITS Mamba efficiency rows — no surviving artefact.
- Any figure, p-value or count copied from `doc/historical/**` — that directory is declared non-authoritative by its own manifest.
- IoU / mIoU / Dice / F1 values — not present in the package.

**Never infer a root cause.** Where the archive does not establish one, state `UNKNOWN`. Example: the cause of the TSVM s0 and s8 confusion-matrix PNG mismatches is `UNKNOWN`; only s5 has a proven mechanism (a separate `model.val()` run whose `confusion_matrix.png` was copied over the run-folder plot).

---

## 12. MARKING CONTENT THAT NEEDS VERIFICATION

Mark every unresolved point **inline** so a human reviewer sees it before it reaches the `.docx`. Use exactly these tokens:

| Token | Meaning | Applies to |
|---|---|---|
| `NEEDS VERIFICATION` | Claim has no artifact yet; must be checked before inclusion | unverified claims (30 in the ledger) |
| `NOT AVAILABLE` | Required information does not exist anywhere in the archive | e.g. citation style, week dates |
| `DERIVED` | Value was computed, not observed | TN = 40 − FP; all percentages and Δ |
| `OBSERVED` | Value read directly from an artifact | metrics, counts, config values |
| `INTERPRETATION` | Author's reading of the evidence | clinical commentary, mechanism discussion |
| `UNKNOWN` | Cause / root cause not established by the archive | s0 / s8 CM mismatch origin |

**Drafting protocol:** keep a running evidence index (statement → file → type) while writing, exactly as `archive/WEEKLY_REPORT_Ket_Qua_V2.md` §9 does. Any sentence that cannot be given an evidence-index row must be either removed or tagged `INTERPRETATION` with no numeric claim.

---

## 13. PRE-DELIVERY CHECKLIST

Derived from `doc/19` §7, plus checks added by this merge.

- [ ] Page: A4, left 3.50 cm, top/bottom/right 2.50 cm, header/footer 1.27 cm
- [ ] 100 % of text is Times New Roman (no Arial / Calibri anywhere)
- [ ] All body paragraphs and figure observations indented 1.27 cm
- [ ] All headings, table captions, figure captions and table cells at 0 cm indent
- [ ] No stray blank paragraphs; spacing via `space_before` / `space_after` only
- [ ] No image wider than 15.00 cm
- [ ] Every figure has caption **and** a two-axis observation paragraph
- [ ] Table captions above tables; figure captions below images
- [ ] Every multi-seed number carries `Mean ± Std`
- [ ] No p-value claimed as significant (verify against `statistically_significant_005`)
- [ ] Every number traced to a file under `archive/Ket_Qua_V2/`
- [ ] No 6-fold / `doc/historical/**` number reused
- [ ] Supervisor rendered **TS. Phùng Thế Bảo** (never "ThS.") — `doc/15` §1.4. Note: the archive is itself inconsistent here (`CONTRADICTED` — the 6-fold report uses "TS.", the 6-seed backup uses "ThS.")
- [ ] No 7th chapter added (`doc/15` §1.4 explicitly forbids it)
- [ ] Every unresolved point carries a §12 token

---

`SOURCE SCOPE = archive/ only`
`SPECS WITHOUT ARCHIVE EVIDENCE = NOT SPECIFIED (see §3.4, §9)`
`STATUS = COMPLETE`