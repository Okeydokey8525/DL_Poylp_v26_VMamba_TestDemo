from pathlib import Path
import json, re
from docx import Document
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
O=Path(__file__).parent
d=Document(O/'working_report.docx')
status={'api':'51 kiểm thử đạt','web':'261 kiểm thử đạt','mobile':'498 kiểm thử đạt'}
(O/'test_status.json').write_text(json.dumps(status,ensure_ascii=False),encoding='utf-8')
for t in d.tables:
    if [c.text for c in t.rows[0].cells]==['Nhóm kiểm tra','Phạm vi','Kết quả']:
        for row,txt in zip(t.rows[1:4],status.values()):
            cell=row.cells[2]
            runs=cell.paragraphs[0].runs
            runs[0].text=txt
            for r in runs[1:]:r.text=''
    if t.rows[0].cells[-1].text=='Δ' and len(t.columns)==4:
        widths=[4.2,4.3,4.3,2.2]
        for col,w in zip(t.columns,widths):col.width=Cm(w)
        for row in t.rows:
            for cell,w in zip(row.cells,widths):cell.width=Cm(w)
for i,p in enumerate(d.paragraphs):
    if re.match(r'^\[\d+\] ',p.text):p.alignment=WD_ALIGN_PARAGRAPH.LEFT
    if any(p.text.startswith(x) for x in ['Mã cơ bản:','Mã cải tiến:','YAML đề xuất:','Kết quả cơ bản:','Kết quả đề xuất:','Tổng hợp chính:','Notebook:','Tiền xử lý:']):p.alignment=WD_ALIGN_PARAGRAPH.LEFT
    if p.text.startswith('Hình 5.5 Trung bình'):
        prev=d.paragraphs[i-1]
        for inline in prev._p.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}inline'):
            ext=inline.find('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent')
            old_h=int(ext.get('cy'));new_h=old_h-int(Cm(.65));ratio=new_h/old_h
            ext.set('cx',str(round(int(ext.get('cx'))*ratio)));ext.set('cy',str(new_h))
            for e in inline.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm/{http://schemas.openxmlformats.org/drawingml/2006/main}ext'):
                e.set('cx',ext.get('cx'));e.set('cy',ext.get('cy'))
d.save(O/'working_report.docx')
print('Repaired test labels, numeric column width, reference alignment and figure 5.5 source placement.')
