"""Consolidate verified literature evidence; original papers/report remain unchanged."""
from pathlib import Path
import csv, hashlib, json, re, unicodedata, sys
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
DATE='2026-10-25'

def writecsv(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

with (ROOT/'audit_20261025_193105/C_report/citation_inventory.csv').open(encoding='utf-8-sig') as f: refs=list(csv.DictReader(f))
with (OUT/'local_pdf_inventory.csv').open(encoding='utf-8-sig') as f: local=list(csv.DictReader(f))

# Evidence reviewed using official publisher/arXiv/docs pages and cached PDFs.
# metadata_status and support_status intentionally have separate meanings.
ev={
1:('VERIFIED','SUPPORTED_DATASET_DESCRIPTION','TLTK-01','https://link.springer.com/chapter/10.1007/978-3-030-37734-2_37','Springer MMM2020 pp451-462; arXiv1911.07069v1; local PDF sections3.1-3.3','2019 online date and conference year2020 both legitimate; local image statistics must be checked from data, not inferred from paper.'),
2:('VERIFIED','SUPPORTED_DATASET_DESCRIPTION','','https://doi.org/10.1145/3083187.3083212','Crossref primary DOI deposit cached metadata/CIT-002.json; Kvasir class description','Publisher page403/Simula502 in browser; exact dataset images/class counts belong local audit. Crossref title KVASIR plus subtitle matches full title.'),
3:('PAGE_EXISTS','INSUFFICIENT_SPLIT_PROVENANCE','','https://www.kaggle.com/datasets/debeshjha1/kvasirseg','Kaggle page exists; cached KAGGLE_FILES.json is one paginated listing with nextPageToken','Does not establish that authors supplied project train.txt/val.txt with880/120. Original Kvasir-SEG paper section4.2 uses80/10/10 for its experiment; this does not prove project split invalid.'),
4:('VERIFIED','SUPPORTED_FORMAT','','https://docs.ultralytics.com/datasets/segment/','Ultralytics YOLO format section: one row/object; normalized polygon; minimum3xy pairs','Live docs can differ from archived fork; runtime source/config remains authority for implementation.'),
5:('VERIFIED','SUPPORTED_SOFTWARE_ATTRIBUTION','','https://github.com/opencv/opencv/wiki/CiteOpenCV','Official OpenCV recommended BibTeX: Bradski2000 The OpenCV Library, Dr.Dobbs','General software citation does not specify exact cv2 behavior; add version-specific API docs for algorithm details.'),
6:('VERIFIED','SUPPORTED_METHOD_METADATA','','https://ieeexplore.ieee.org/document/4310076','IEEE metadata and cached Crossref/CIT-006:1979 volume9 issue1 pp62-66','Otsu attribution verified; exact reported thresholds5-8 require dataset recomputation, not paper support.'),
7:('VERIFIED','PARTIAL_CONCEPT_SUPPORT','','https://www.imageprocessingplace.com/DIP-4E/dip4e_main_page.htm','Authors companion site:4th edition Pearson ISBN9780133356724 copyright2018; morphology listed','No authorized full book available in supplied TLTK; exact page/formula for closing not inspected. New Pearson eText revision dates do not invalidate2018 print citation.'),
8:('VERIFIED','PARTIAL_METHOD_SUPPORT','','https://doi.org/10.1016/0734-189X(85)90016-7','Cached Crossref primary deposit CIT-008: Suzuki/Abe1985 volume30 issue1 pp32-46','Publisher fulltext403; metadata verified. Precise OpenCV implementation should cite findContours API/source; paper title does not validate TSVM topology claims.'),
9:('VERIFIED','SUPPORTED_METHOD_METADATA','','https://doi.org/10.3138/FM57-6770-U75U-7727','Publisher Cartographica metadata/abstract; cached Crossref CIT-009:Douglas/Peucker1973 volume10 issue2 pp112-122','Polygon simplification attribution supported; actual geometric fidelity after conversion requires direct evaluation.'),
10:('VERIFIED','SUPPORTED_METHOD','', 'https://arxiv.org/abs/2004.10934','YOLOv4 arXiv2020 authors Bochkovskiy/Wang/Liao; Mosaic augmentation source','Does not establish exact augmentation values used by this project; args.yaml does.'),
11:('VERIFIED','SUPPORTED_DOCUMENTATION','','https://docs.ultralytics.com/guides/yolo-data-augmentation/','Official augmentation guide: HSV, geometric and Mosaic settings','Docs are live; use code/version for actual pipeline and probabilities.'),
12:('VERIFIED','SUPPORTED_ARCHITECTURE','TLTK-05','https://arxiv.org/abs/1505.04597','U-Net authors/title2015 verified; local fulltext architecture section','Semantic segmentation background, not matched instance-AP benchmark.'),
13:('VERIFIED','SUPPORTED_ARCHITECTURE','TLTK-07','https://arxiv.org/abs/2006.11392','PraNet arXiv v4/MICCAI2020, reverse attention and decoder; local fulltext','Do not transfer its published scores to BG20.'),
14:('VERIFIED','SUPPORTED_ARCHITECTURE','TLTK-14','https://arxiv.org/abs/2312.00752','Gu/Dao2023 preprint; arXiv v2 revised2024, selective state spaces','Paper linear complexity refers its hardware-aware algorithm, not automatically custom O(LlogL) scan in project.'),
15:('VERIFIED','SUPPORTED_ARCHITECTURE','TLTK-15','https://arxiv.org/abs/2401.10166','VMamba arXiv v4, NeurIPS2024 spotlight; SS2D four routes','Project SS2D differs from full reference implementation; code/report already state missing out_norm/skipD.'),
16:('VERIFIED','SUPPORTED_DOCUMENTATION','TLTK-12','https://docs.ultralytics.com/models/yolo26/','Official YOLO26 docs and linked original paper arXiv2606.03748','Live docs mention broader training recipe. Project AdamW and exact Segment26 behavior must be attributed to saved args/fork8.4.127.'),
17:('VERIFIED','SUPPORTED_METHOD_AND_TABLE','TLTK-19','https://papers.miccai.org/miccai-2024/paper/0697_paper.pdf','MICCAI PDF p1 method; Table1 p6:Kvasir Dice.940 IoU.881; p6 protocol900+550,224px','Word T17R002 matches. Do not mix reviewer rebuttal or alternate-resolution numbers.'),
18:('VERIFIED','SUPPORTED_METHOD_AND_TABLE','downloaded/Topo-VM-UNetV2.pdf','https://arxiv.org/abs/2505.06210','arXivv1 p3-4 persistent homology/Topo-SDI; TableI p5:91.95%86.54%; sectionIII protocol900+550,256px','Word decimals.9195/.8654 correct. Five-seed averaged results in source; no same-protocol comparison to BG20.'),
19:('VERIFIED','SUPPORTED_METHOD_AND_TABLE','downloaded/CSG-Mamba.pdf','https://arxiv.org/abs/2608.14146','arXivv1 Table1 p9:mIoU.8677 Dice.9220; section4.1-4.2:800/100/100,256px,3seeds','Authors match; arXiv comments state accepted ICONIP2026. Calling accessed artifact preprint is defensible; may add acceptance status with date, not invent published DOI.'),
20:('VERIFIED','SUPPORTED_CLOSE_PRECEDENT','downloaded/MambaPSA.pdf','https://arxiv.org/abs/2607.12681','arXivv1 authors Chan etal; end-backbone C2PSA replacement and neck placement on PASCAL VOC','Word correctly avoids claiming first Mamba replacement of C2PSA in YOLO26.'),
21:('VERIFIED','SUPPORTED_CLOSE_PRECEDENT','downloaded/SAM-MaGuP.pdf','https://arxiv.org/abs/2507.01509','Dutta/Majhi/Nayak/Jha2025, boundary distillation and SAM Mamba adapter; MICCAI2025 official paper3165 entry','SAM-MaGuP is not the same paper as local TLTK-21 SAM-Mamba WACV2025. Add conference metadata if desired.'),
22:('VERIFIED','SUPPORTED_OPTIMIZER','','https://arxiv.org/abs/1711.05101','arXivv3 comments:ICLR2019; Loshchilov/Hutter; decoupled weight decay','2017 arXiv initial date and2019 conference citation are not inconsistent.'),
23:('VERIFIED','SUPPORTED_STATISTICAL_API','','https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html','SciPy1.18 docs:related paired samples; two-sided alternative; t statistic/CI','API documentation does not prove study assumptions or generalization; record installed version.'),
24:('VERIFIED','SUPPORTED_STATISTICAL_API','','https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html','SciPy1.18 docs:paired differences, symmetry about zero, zero/tie/method handling','Signed-rank test is not assumption-free; exact options/roundoff must be recorded.')}
rows=[]
for r in refs:
    n=int(r['word_reference_number']);m,s,l,u,e,lim=ev[n]
    rows.append({'citation_id':r['citation_id'],'word_reference_number':n,'word_location':r['paragraph_id'],'cited_word_ids':r['cited_word_ids'],
      'reference_text':r['reference_text'],'metadata_status':m,'claim_support_status':s,'local_match':l,'primary_url':u,'evidence_locator':e,'limitations':lim,'verified_on':DATE})
writecsv('reference_verification.csv',rows)

related=[
('RW01','MambaPSA','2026 arXiv v1','https://arxiv.org/abs/2607.12681','Object detection','YOLO26/C2PSA replacement; neck P3/P4/P5 study','PASCAL VOC2007+2012','Detection AP; CPU throughput','N/A for polyps','Very close integration location; differs task and shape branch','Already CIT-020','p1-2'),
('RW02','CSG-Mamba','2026 arXiv v1; comments acceptedICONIP2026','https://arxiv.org/abs/2608.14146','Semantic polyp segmentation','Convolutional bottleneck gating','Kvasir800/100/100; externalClinicDB/ColonDB','Dice,mIoU,HD95;3seeds','No BG20 negative-image protocol','Very close local/global gating motive; lacks YOLO instance head','Already CIT-019','sections3-5'),
('RW03','Topo-VM-UNetV2','2025 arXiv v1','https://arxiv.org/abs/2505.06210','Semantic polyp segmentation','Persistent-homology probability attention; Topo-SDI','Train900Kvasir+550ClinicDB; five public testsets','Dice/IoU/MAE;5seeds','Not BG20','Closest explicit topology comparator; project convolutional guidance has no persistent homology','Already CIT-018','sectionsII-III'),
('RW04','Polyp-Mamba','MICCAI2024','https://papers.miccai.org/miccai-2024/paper/0697_paper.pdf','Semantic polyp segmentation','Scale-aware semantics and global injection','900Kvasir+550ClinicDB;224px;5datasets','Dice/IoU and additional segmentation metrics','Not BG20','Useful multi-scale/global-local precedent; different backbone/head','Already CIT-017;TLTK-19','p1,sections2-3'),
('RW05','SAM-MaGuP','MICCAI2025/arXiv2507.01509','https://arxiv.org/abs/2507.01509','Generalized semantic polyp segmentation','SAM Mamba adapter and boundary distillation','Five datasets; fulltext cached','Pixel segmentation metrics; boundary mechanism','No same BG20 protocol established','Boundary supervision precedent; project has neither SAM nor distillation','Already CIT-021;notTLTK-21','p1,method'),
('RW06','PolyMamba','MICCAI2025','https://papers.miccai.org/miccai-2025/0704-Paper3872.html','Semantic polyp segmentation','Spatial-prior guidance and dual-gate frequency enhancement','Five polyp datasets','Semantic segmentation protocol; no AP comparison here','Not matched','Close guidance/local-frequency reasoning; explicit prior differs learned TSVM kernels','Present TLTK-20, absent mainWord refs;consider add','Abstract/method;localPDF'),
('RW07','Mamba YOLO','2024 arXiv v2','https://arxiv.org/abs/2406.05835','Object detection','ODMamba backbone and local multi-branch blocks','COCO','Object detection AP/latency','N/A','Broader YOLO-SSM predecessor, not YOLO26 polyp segmentation','Present TLTK-22, absent mainWord refs;optional','abstract/localPDF'),
('RW08','SAM-Mamba','WACV2025','https://openaccess.thecvf.com/content/WACV2025/papers/Dutta_SAM-Mamba_Mamba_Guided_SAM_Architecture_for_Generalized_Zero-Shot_Polyp_Segmentation_WACV_2025_paper.pdf','Generalized semantic polyp segmentation','SAM domain prior and Mamba channel interaction','Five polyp datasets;localPDF','Semantic segmentation;no matched AP ranking','Not matched','Related SAM predecessor; distinct from SAM-MaGuP','Present TLTK-21, absent mainWord refs;optional','localPDFfirstpage+method'),
('RW09','Hybrid Graph Mamba','MICCAI2025','https://papers.miccai.org/miccai-2025/paper/1195_paper.pdf','Semantic polyp segmentation','Graph/topological relationships with Mamba; boundary fusion','Five benchmark datasets','Segmentation metrics;not matched','Not matched','Useful distinction between explicit graph relations and directional kernels','New suggested source;primaryPDF verified','p1 abstract'),
('RW10','MambaPolyp','2026 publisher article','https://onlinelibrary.wiley.com/doi/10.1002/ima.70445','Semantic colorectal polyp segmentation','Long-range,multi-scale context,boundary enhancement','Abstract checked;protocol not fully reviewed','Not extracted for comparison','Unknown','Recent related lead only; needs fullmethod/protocol review before main comparison','New optional lead;abstract/metadata only','Publisherabstract;firstpublished8Sep2026')]
writecsv('related_work_matrix.csv',[dict(zip(['work_id','title','version','primary_url','task','mechanism','data_protocol','metrics','negative_image_protocol','relevance_difference','coverage','evidence_locator'],r)) for r in related])

issues=[
{'issue_id':'D-001','severity':'medium','status':'INSUFFICIENT_EVIDENCE','location':'Word P0363;CIT-003','title':'880/120 split attributed to dataset authors without provenance','evidence':'Original Kvasir-SEG PDF section4.2 p7 uses80/10/10 for its experiment; Kaggle cached listing is paginated and does not establish supplied project lists. Local lists establish membership, not authorship.','cause':'Provenance evidence not supplied; not proof local split is incorrect.','recommendation':'Describe project using existing880/120 lists; obtain exact release/version/downloadURL/hash supporting official authorship before retaining attribution.'},
{'issue_id':'D-002','severity':'medium','status':'CONFIRMED_INDEX_MISMATCH','location':'TLTK/MANIFEST.txt;currentWord reference list','title':'TLTK numbering and Word numbering identify different works','evidence':'TLTK[20]=PolyMamba, Word[20]=MambaPSA; TLTK[21]=SAM-Mamba, Word[21]=SAM-MaGuP. Six mainWord paper references have exact-work PDF counterparts among original24, plus a related YOLO26 paper accompanying docs reference16; four additional PDFs cached in audit.','cause':'Different bibliographic collections/version ordering; not necessarily an incorrect citation inside currentWord.','recommendation':'Use CIT stable IDs/title/DOI crosswalk; do not copy [n] from TLTK directly into currentWord.'},
{'issue_id':'D-003','severity':'low','status':'COVERAGE_RECOMMENDATION','location':'Word related work;TLTK-20','title':'Relevant existing PolyMamba paper not discussed in currentWord','evidence':'MICCAI2025 official page verifies spatial-prior guided Mamba and frequency gating; supplied TLTK-20 is same work.','cause':'Coverage choice; not proof existing bibliography inadequate overall.','recommendation':'Consider a concise comparison focused on guidance source and boundary-frequency mechanism, not unrelated performance ranking.'},
{'issue_id':'D-004','severity':'low','status':'PARTIAL_VERIFICATION','location':'CIT-007;CIT-008','title':'Exact source-page support incomplete for morphology/border-following references','evidence':'Book edition metadata verified on authors site; Suzuki/Abe metadata verified via primary Crossref deposit. Authorized fulltexts not in supplied TLTK; publisher403 for Suzuki.','cause':'Access/coverage limitation, not confirmed false reference.','recommendation':'Add precise lawful book pages or OpenCV official API/source documentation for implementation claims.'},
{'issue_id':'D-005','severity':'info','status':'NOT_ASSESSED','location':'Whole report;Turnitin','title':'Local source screening cannot determine Turnitin similarity threshold','evidence':'No school settings/report/submission history; source PDFs are largely English and Word is Vietnamese.','cause':'Database coverage, translation and exclusion settings outside local audit.','recommendation':'Use official Turnitin report on exact finalfile; keep citation/paraphrase review separate from similarity and AI writing indicators.'}]
writecsv('issues.csv',issues)

# Narrow, reproducible exact-overlap screening: no translation, no global corpus.
def tokens(s):return re.findall(r'\w+',unicodedata.normalize('NFKC',s).lower(),flags=re.UNICODE)
with (ROOT/'audit_20261025_193105/C_report/word_blocks.csv').open(encoding='utf-8-sig') as f: blocks=list(csv.DictReader(f))
textkey=next(k for k in blocks[0] if k in ['text','content'])
idkey=next(k for k in blocks[0] if k in ['id','block_id'])
body=[]
for r in blocks:
    bid=r[idkey]
    if bid.startswith('P') and bid[1:].isdigit() and int(bid[1:])>=733:continue
    ts=tokens(r[textkey])
    if len(ts)>=12:body.append((bid,r[textkey],ts))
sourcefiles=sorted((OUT/'local_text').glob('*.txt'));sourcegrams={}
for p in sourcefiles:
    ts=tokens(p.read_text(encoding='utf-8'));sourcegrams[p.stem]={tuple(ts[i:i+12]) for i in range(max(0,len(ts)-11))}
matches=[]
for bid,txt,ts in body:
    grams={tuple(ts[i:i+12]) for i in range(len(ts)-11)}
    for source,sg in sourcegrams.items():
        overlap=grams&sg
        if overlap:
            matches.append({'word_id':bid,'source_text':source,'distinct_12token_matches':len(overlap),'example':' '.join(next(iter(sorted(overlap)))),'interpretation':'Exact text match only; inspect attribution/context; no automatic plagiarism finding'})
if matches:writecsv('local_exact_overlap_candidates.csv',matches)
else:
    (OUT/'local_exact_overlap_candidates.csv').write_text('word_id,source_text,distinct_12token_matches,example,interpretation\n',encoding='utf-8-sig')
screen={'body_blocks_scanned':len(body),'source_texts_scanned':len(sourcefiles),'word_span':12,'matching_block_source_pairs':len(matches),'limitations':'Bibliography/appendix paragraphs P0733+ excluded; tables retained. Exact normalized contiguous token matching only. No translation/paraphrase/sourceInternet/prior submissions or Turnitin database. Not a similarity percentage.'}
(OUT/'local_overlap_scope.json').write_text(json.dumps(screen,ensure_ascii=False,indent=2),encoding='utf-8')

sources=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.suffix.lower() in {'.pdf','.txt','.json','.png'}:
        sources.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
for r in local:sources.append({'path':r['path'],'sha256':r['sha256'],'bytes':Path(r['path']).stat().st_size})
writecsv('source_manifest.csv',sources)
print('References',len(rows),'related',len(related),'issues',len(issues),'screen',screen)
