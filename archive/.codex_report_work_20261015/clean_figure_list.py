from pathlib import Path
import json,re
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as ET
O=Path(__file__).parent;nav=json.loads((O/'navigation.json').read_text(encoding='utf-8'))
bad=[e for e in nav['figures'] if e['text'].startswith('Hình 3.') and not re.match(r'^Hình 3\.\d+\.',e['text'])]
anchors={e['bookmark'] for e in bad};nav['figures']=[e for e in nav['figures'] if e['bookmark'] not in anchors]
path=O/'working_report.docx'
with ZipFile(path) as z:parts={i.filename:(i,z.read(i.filename)) for i in z.infolist()}
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};q=lambda t:'{'+ns['w']+'}'+t
r=ET.fromstring(parts['word/document.xml'][1]);removed=0
for p in list(r.findall('.//w:body/w:p',ns)):
    links=p.findall('w:hyperlink',ns)
    if any(x.get(q('anchor')) in anchors for x in links):p.getparent().remove(p);removed+=1
parts['word/document.xml']=(parts['word/document.xml'][0],ET.tostring(r,encoding='UTF-8',xml_declaration=True,standalone=True))
out=O/'clean_list.docx'
with ZipFile(out,'w',ZIP_DEFLATED) as z:
    for name,(info,data) in parts.items():z.writestr(info,data)
out.replace(path);(O/'navigation.json').write_text(json.dumps(nav,ensure_ascii=False,indent=2),encoding='utf-8')
print('Removed',removed,'narrative entries; actual figures:',len(nav['figures']))
