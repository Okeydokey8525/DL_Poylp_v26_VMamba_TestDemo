from pathlib import Path
import zipfile, xml.etree.ElementTree as ET, csv, json, re, hashlib

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
DOC = ROOT / 'Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}
def txt(el):
    return ''.join(n.text or '' for n in el.iter() if n.tag in ('{'+NS['w']+'}t', '{'+NS['m']+'}t'))

with zipfile.ZipFile(DOC) as z:
    root = ET.fromstring(z.read('word/document.xml'))
    records=[]; refs=[]; equations=[]; pc=tc=0; section='frontmatter'
    for order, el in enumerate(root.find('w:body', NS), 1):
        if el.tag == '{'+NS['w']+'}p':
            pc+=1; text=txt(el); pid=f'P{pc:04d}'
            style=el.find('w:pPr/w:pStyle',NS)
            style='' if style is None else style.attrib.get('{'+NS['w']+'}val','')
            if re.match(r'^(CHƯƠNG [1-5] |KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN$|TÀI LIỆU THAM KHẢO$|PHỤ LỤC [A-D] )',text):
                section=text
            typ='paragraph'
            if re.match(r'^Hình\s+\d',text):typ='figure_caption'
            elif re.match(r'^Bảng\s+',text):typ='table_caption'
            elif re.match(r'^\[\d+\]',text):typ='reference'
            elif style.lower().startswith('heading'):typ='heading'
            math_count=len(el.findall('.//m:oMath',NS))
            rec={'id':pid,'body_order':order,'kind':typ,'section':section,'style':style,'text':text,'math_count':math_count,
                 'citation_numbers':','.join(re.findall(r'\[(\d+)\]',text))}
            records.append(rec)
            if math_count:equations.append(rec)
            if typ=='reference':
                n=re.match(r'^\[(\d+)\]',text).group(1)
                refs.append({'citation_id':f'CIT-{int(n):03d}','word_reference_number':n,'paragraph_id':pid,'reference_text':text,
                             'doi':';'.join(re.findall(r'10\.\d{4,9}/[^\s]+',text)),
                             'urls':';'.join(re.findall(r'https?://[^\s]+',text))})
        elif el.tag == '{'+NS['w']+'}tbl':
            tc+=1
            for ri,row in enumerate(el.findall('w:tr',NS),1):
                cells=[txt(c) for c in row.findall('w:tc',NS)]
                records.append({'id':f'T{tc:02d}R{ri:03d}','body_order':order,'kind':'table_row','section':section,
                                'style':'','text':' | '.join(cells),'math_count':len(row.findall('.//m:oMath',NS)),
                                'citation_numbers':','.join(re.findall(r'\[(\d+)\]',' '.join(cells)))})

def write_csv(name, data):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
write_csv('word_blocks.csv',records)
write_csv('citation_inventory.csv',refs)
if equations:write_csv('equations.csv',equations)
(OUT/'word_extracted.txt').write_text('\n'.join(f"{r['id']} [{r['kind']}] {r['text']}" for r in records),encoding='utf-8')
(OUT/'extraction_manifest.json').write_text(json.dumps({'document':str(DOC),'sha256':hashlib.sha256(DOC.read_bytes()).hexdigest(),
    'paragraphs':pc,'tables':tc,'table_rows':sum(r['kind']=='table_row' for r in records),'references':len(refs),
    'equation_paragraphs':len(equations),'method':'read-only OOXML extraction, w:t and m:t in document order; IDs tied to unchanged DOCX hash'},ensure_ascii=False,indent=2),encoding='utf-8')
print(pc,tc,len(refs),len(equations),DOC)
