from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'fix_20261026'
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
    return h.hexdigest()
old=json.loads((ROOT/'audit_20261025_193105/root/source_before.json').read_text(encoding='utf-8'))
protected=[];bad=[]
for row in old:
    p=Path(row['path'])
    if p.suffix.lower() in {'.pt','.csv','.json','.png','.jpg','.jpeg','.txt'} and ('Ket_Qua_V2' in p.parts or p.suffix.lower()=='.pt'):
        protected.append(str(p))
        if not p.exists() or sha(p)!=row['sha256']:bad.append(str(p))
app=ROOT.parents[1]/'Ung_Dung/polypweb/polypweb'
snapshot=OUT/'integration/project'
source_mismatch=[];source_count=0
for p in (app/'src').rglob('*'):
    if p.is_file():
        source_count+=1;q=snapshot/p.relative_to(app)
        if not q.exists() or sha(p)!=sha(q):source_mismatch.append(str(p))
main=ROOT/'Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx'
alias=main.with_name(main.stem+'_MoRong_FP32.docx')
with zipfile.ZipFile(main) as a,zipfile.ZipFile(OUT/'backups'/main.name) as b:
    changed=[n for n in a.namelist() if a.read(n)!=b.read(n)]
result={'protected_files_checked':len(protected),'protected_files_changed':bad,'source_snapshot_files_checked':source_count,'source_snapshot_mismatches':source_mismatch,'word_sha256':sha(main),'word_alias_equal':sha(main)==sha(alias),'word_changed_zip_members':changed,'verified_render_pages':len(list((OUT/'word/rendered_verified').glob('page-*.png'))),'page_2_same_as_first_render':sha(OUT/'word/rendered/page-2.png')==sha(OUT/'word/rendered_verified/page-2.png')}
(OUT/'final_validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(result,indent=2,ensure_ascii=False))
assert not bad and not source_mismatch and result['word_alias_equal'] and changed==['word/document.xml']
manifest=OUT/'documentation/documentation_changes.json'
rows=json.loads(manifest.read_text(encoding='utf-8'))
for row in rows:row['after_sha256']=sha(row['path'])
manifest.write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
