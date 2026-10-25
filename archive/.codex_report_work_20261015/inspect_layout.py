from pathlib import Path
import sys
O=Path(__file__).parent;sys.path.insert(0,str(O/'packages'));sys.stdout.reconfigure(encoding='utf-8')
from docx import Document
from docx.oxml.ns import qn
import pymupdf
d=Document(O/'working_report.docx')
for i,p in enumerate(d.paragraphs[:42]):
    print(i,p.text[:95].replace('\n','|'),'sect',len(p._p.findall('.//'+qn('w:sectPr'))),'break',len(p._p.findall('.//'+qn('w:br'))))
pdf=pymupdf.open(O/'render_v2/working_report.pdf')
for i,p in enumerate(pdf):
    if i<16:print('PDF',i+1,len(p.get_text()),p.get_text()[:70].replace('\n',' | '))
for s in d.sections:print('SECTION',s._sectPr.xml[-1100:])
