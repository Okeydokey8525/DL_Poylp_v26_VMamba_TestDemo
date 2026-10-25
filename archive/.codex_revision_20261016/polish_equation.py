from pathlib import Path
from docx import Document
O=Path(__file__).parent;d=Document(O/'working_report.docx')
for p in d.paragraphs:
    if p.text.startswith('d_i = TSVM_i'):
        p.text='dᵢ = TSVMᵢ − Baselineᵢ\nKTC 95% = d̄ ± t(0,975; 19) × SD(d) / √20'
d.save(O/'working_report.docx')
print('Polished paired confidence interval notation.')
