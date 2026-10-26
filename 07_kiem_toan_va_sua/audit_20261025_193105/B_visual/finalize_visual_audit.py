"""Summarize persisted figure checks; no project source mutations."""
from pathlib import Path
import csv,json,hashlib,math,zipfile
O=Path(__file__).resolve().parent;R=O.parents[1];PKG=R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(name,rows):
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with (O/name).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inv=json.loads((O/'inventory.json').read_text(encoding='utf-8'))
repro=json.loads((O/'reproduction_pixel_comparison.json').read_text(encoding='utf-8'))
other=json.loads((O/'other_reproduction_pixel_comparison.json').read_text(encoding='utf-8'))
pixel={str(Path('Ket_Qua_V2/KQ_Nen_DX_20seed_FP32')/r['path']):r for r in repro}
pixel.update({r['path']:r for r in other})
cm=read(O/'cm_ocr_comparison.csv');curves=read(O/'raw_curve_digitization.csv')
cm_ids={r['id'] for r in cm};curve_ids={r['id'] for r in curves}
# Independent inputs behind the three Word-only quantitative figures.
work=R/'.codex_report_work_20261015';primary=read(O.parent/'A_numeric/independent_selected_metrics.csv');by={(r['model'],int(r['seed'])):r for r in primary}
raw_checks=[]
for r in read(work/'verified_raw.csv'):
    ref=by[r['model'],int(r['seed'])]
    for k,v in r.items():
        if k in {'model','run_path'}:continue
        if k in ref:raw_checks.append({'kind':'word_custom_raw','model':r['model'],'seed':r['seed'],'column':k,'expected':ref[k],'actual':v,'match':math.isclose(float(v),float(ref[k]),rel_tol=2e-11,abs_tol=2e-11)})
statby={r['metric']:r for r in read(O.parent/'A_numeric/independent_summary.csv')}
rename={'delta':'delta_tsvm_minus_baseline','ci_low':'delta_ci95_low','ci_high':'delta_ci95_high','p_ttest':'paired_t_p','p_wilcoxon':'wilcoxon_two_sided_p','levene_p':'levene_median_p','dz':'cohen_dz'}
for r in read(work/'verified_statistics.csv'):
    if r['metric'] not in statby:continue
    ref=statby[r['metric']]
    for k,v in r.items():
        kk=rename.get(k,k)
        if kk in ref and k!='metric' and v and ref[kk]:raw_checks.append({'kind':'word_custom_statistics','metric':r['metric'],'column':k,'expected':ref[kk],'actual':v,'match':math.isclose(float(v),float(ref[kk]),rel_tol=2e-11,abs_tol=2e-11)})
cached=json.loads((work/'curves.json').read_text(encoding='utf-8'));n_curve=0;curve_diff=[]
for m,items in cached.items():
    for seed,item in enumerate(items):
        p=R/by[m,seed]['run_path']/'results.csv';history=read(p)
        for k,vals in item.items():
            if k=='time':continue
            for epoch,val in enumerate(vals):
                n_curve+=1
                actual=float(next(v for key,v in history[epoch].items() if key.strip()==k))
                if not math.isclose(actual,float(val),rel_tol=2e-11,abs_tol=2e-11):curve_diff.append((m,seed,k,epoch+1))
write('word_custom_chart_numeric_checks.csv',raw_checks)
wordmap=[];coverage=[]
for r in inv:
    row={'figure_id':r['id'],'group':r['group'],'path':r['path'],'sha256':r['sha256'],'model':r['model'],'seed':r['seed']}
    if r['group']=='package':
        p=pixel.get(r['path'])
        row.update(overview='overview inspected in prior B phase; resumed corroboration of legacy original/reproduction',
                   quantitative='PIXEL_IDENTICAL_TO_ISOLATED_REPRODUCTION' if p and p['pixel_identical'] else 'LEGACY_SOURCE_AND_NUMERIC_LABEL_REVIEW; pixel reproduction differs',
                   precision_limit='pixel equality checks consistency with current generator; data independently checked by A')
    elif r['group']=='raw':
        row.update(overview='per-run contact-sheet overview; Baseline prior phase, TSVM resumed phase',
                   quantitative='CM_OCR_MATCH' if r['id'] in cm_ids else 'PLOT_DIGITIZED_APPROXIMATELY' if r['id'] in curve_ids else 'NOT_VERIFIED',
                   precision_limit='contact sheet is not full-resolution numeric inspection; OCR/digitization evidence stored separately')
    else:
        matches=[]
        for s in r['source'].split(';'):
            if not s:continue
            if '!' in s:
                file,member=s.split('!',1)
                with zipfile.ZipFile(R/file) as z:h=hashlib.sha256(z.read(member)).hexdigest()
            else:h=sha(R/s)
            matches.append(h==r['sha256'])
        status=bool(matches) and all(matches)
        row.update(overview='embedded content inspected; no full-document page-render sign-off',quantitative='EXACT_SOURCE_BYTES_MATCH' if status else 'SOURCE_MAPPING_UNRESOLVED',precision_limit='same image bytes do not prove caption, model provenance, or rendered page layout')
        wordmap.append({'figure_id':r['id'],'embedded_path':r['path'],'source':r['source'],'all_sources_same_hash':status,'caption_and_context':r['caption'],'word_crop':r.get('crop','{}'),'review':'caption/content mapping; quantitative sources A+B; qualitative checkpoint count E/root'})
    coverage.append(row)
write('coverage.csv',coverage);write('word_figure_mapping.csv',wordmap)
coverage_by_id={r['figure_id']:r for r in coverage}
for r in inv:
    c=coverage_by_id[r['id']]
    r['visual_status']=c['overview']
    r['numeric_status']=c['quantitative']
write('figure_inventory.csv',inv)
(O/'inventory.json').write_text(json.dumps(inv,ensure_ascii=False,indent=2),encoding='utf-8')
summary={'inventory':{g:sum(r['group']==g for r in inv) for g in ['package','raw','word']},
         'new_result_reproductions':len(repro),'new_result_pixel_identical':sum(r['pixel_identical'] for r in repro),
         'benchmark_reproductions':sum('efficiency_benchmark' in r['path'] for r in other),'benchmark_pixel_identical':sum(r['pixel_identical'] for r in other if 'efficiency_benchmark' in r['path']),
         'legacy_pixel_not_identical':sum(not r['pixel_identical'] for r in other if 'efficiency_benchmark' not in r['path']),
         'cm_checks':len(cm),'cm_statuses':{s:sum(r['status']==s for r in cm) for s in set(r['status'] for r in cm)},
         'digitized_curves':len(curves),'pr_curves':sum(bool(r.get('legend_minus_log')) for r in curves),
         'pr_legend_vs_fitness_log_max_abs':max(abs(float(r['legend_minus_log'])) for r in curves if r.get('legend_minus_log')),
         'pr_pixel_area_vs_legend_max_abs':max(abs(float(r['area_minus_legend'])) for r in curves if r.get('area_minus_legend')),
         'custom_word_numeric_checks':len(raw_checks),'custom_word_numeric_mismatches':sum(not r['match'] for r in raw_checks),
         'word_cached_curve_non_time_cells':n_curve,'word_cached_curve_mismatches':curve_diff,
         'word_source_mappings':len(wordmap),'word_source_hash_matches':sum(r['all_sources_same_hash'] for r in wordmap)}
(O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
