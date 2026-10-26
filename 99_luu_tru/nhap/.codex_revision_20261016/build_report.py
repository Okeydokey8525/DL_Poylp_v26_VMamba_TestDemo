from pathlib import Path
import sys,json,re,copy,hashlib
from io import BytesIO
O=Path(__file__).parent;R=O.parent;sys.path.insert(0,str(R/'.codex_report_work_20261015/packages'))
import pandas as pd,numpy as np
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH,WD_BREAK
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

sys.stdout.reconfigure(encoding='utf-8')
original=R/'Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx'
retained=O/'original_report.docx'
src=retained if retained.exists() else original
doc=Document(src);body=doc.element.body
# Retain the reference styles, then rebuild overflowing cover text with the same identities.
for el in list(body):
    if el.tag!=qn('w:sectPr'):body.remove(el)
for p in doc.paragraphs:
    if p.text.strip()=='---':p._p.getparent().remove(p._p)
styles=doc.styles
for name,size,bold in [('Normal',13,False),('Heading 1',18,True),('Heading 2',14,True),('Heading 3',13,True),('Caption',12,False),('Title',18,True)]:
    st=styles[name];st.font.name='Times New Roman';st.font.size=Pt(size);st.font.bold=bold;st.font.color.rgb=RGBColor(0,0,0)
    st.element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'Times New Roman')
    f=st.paragraph_format;f.line_spacing=1.3;f.space_before=Pt(6);f.space_after=Pt(6)
    if name=='Normal':f.first_line_indent=Cm(.8);f.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
    if name.startswith('Heading'):f.keep_with_next=True;f.first_line_indent=Cm(0)
    if name=='Heading 1':f.alignment=WD_ALIGN_PARAGRAPH.CENTER;f.page_break_before=True;f.space_after=Pt(14)
for st in styles:
    for border in list(st.element.iter(qn('w:pBdr'))):border.getparent().remove(border)

def font(run,size=None,bold=None):
    run.font.name='Times New Roman';run.font.color.rgb=RGBColor(0,0,0)
    run._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'Times New Roman')
    if size:run.font.size=Pt(size)
    if bold is not None:run.bold=bold

def p(text='',style=None):
    out=doc.add_paragraph(text,style)
    for r in out.runs:font(r)
    return out

bookmarks=[];figures=[];tables=[];bookmark_counter=100
def mark(par,name):
    global bookmark_counter
    bookmark_counter+=1;s=OxmlElement('w:bookmarkStart');s.set(qn('w:id'),str(bookmark_counter));s.set(qn('w:name'),name)
    e=OxmlElement('w:bookmarkEnd');e.set(qn('w:id'),str(bookmark_counter));par._p.insert(0,s);par._p.append(e)

def heading(text,level=1):
    out=p(text.upper() if level in (1,2) else text,'Heading '+str(level));out.paragraph_format.first_line_indent=Cm(0)
    name=f'sec_{len(bookmarks)+1}';mark(out,name);bookmarks.append({'text':out.text,'bookmark':name,'level':level})
    return out

def caption(text,kind):
    out=p(text,'Caption');out.alignment=WD_ALIGN_PARAGRAPH.CENTER;out.paragraph_format.first_line_indent=Cm(0)
    if kind=='table':out.paragraph_format.keep_with_next=True
    name=f'{kind}_{bookmark_counter+1}';mark(out,name)
    (figures if kind=='figure' else tables).append({'text':text,'bookmark':name})
    return out

def table(title,headers,rows,widths=None):
    caption(title,'table')
    t=doc.add_table(rows=1,cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    if widths is None:widths=[15/len(headers)]*len(headers)
    for col,w in zip(t.columns,widths):col.width=Cm(w)
    for c,h in zip(t.rows[0].cells,headers):c.text=str(h)
    for row in rows:
        for c,v in zip(t.add_row().cells,row):c.text=str(v)
    pr=t._tbl.tblPr;b=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        x=OxmlElement('w:'+edge);x.set(qn('w:val'),'single');x.set(qn('w:sz'),'4');x.set(qn('w:color'),'D9D9D9');b.append(x)
    pr.append(b)
    for i,row in enumerate(t.rows):
        trpr=row._tr.get_or_add_trPr();trpr.append(OxmlElement('w:cantSplit'))
        if i==0:trpr.append(OxmlElement('w:tblHeader'))
        for j,c in enumerate(row.cells):
            c.width=Cm(widths[j]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tcpr=c._tc.get_or_add_tcPr();mar=OxmlElement('w:tcMar')
            for side,n in [('top',65),('bottom',65),('left',90),('right',90)]:
                x=OxmlElement('w:'+side);x.set(qn('w:w'),str(n));x.set(qn('w:type'),'dxa');mar.append(x)
            tcpr.append(mar)
            if i==0:
                sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E8EDF1');tcpr.append(sh)
            for cp in c.paragraphs:
                cp.paragraph_format.first_line_indent=Cm(0);cp.paragraph_format.line_spacing=1.3;cp.paragraph_format.space_before=Pt(0);cp.paragraph_format.space_after=Pt(0)
                cp.alignment=WD_ALIGN_PARAGRAPH.LEFT if j==0 else WD_ALIGN_PARAGRAPH.CENTER
                for r in cp.runs:font(r,12,i==0)
    p('').paragraph_format.space_after=Pt(0)
    return t

def fig(name,title):
    out=p();out.alignment=WD_ALIGN_PARAGRAPH.CENTER;out.paragraph_format.first_line_indent=Cm(0);out.paragraph_format.keep_with_next=True
    path=R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32'/f'{name[4:]}.png' if name.startswith('pkg:') else O/'figures'/f'{name}.png'
    out.add_run().add_picture(str(path),width=Cm(14.8));caption(title,'figure').paragraph_format.keep_with_next=True
    out=p('Nguồn: nhóm thực hiện từ mã nguồn hoặc số liệu của đề tài.');out.paragraph_format.first_line_indent=Cm(0);out.alignment=WD_ALIGN_PARAGRAPH.CENTER
    for r in out.runs:font(r,11)

def geometry(s):
    s.page_width=Cm(21);s.page_height=Cm(29.7);s.left_margin=Cm(3.5);s.right_margin=Cm(2.5);s.top_margin=Cm(2.5);s.bottom_margin=Cm(2.5);s.header_distance=Cm(1.27);s.footer_distance=Cm(1.27)

def numbering(s,fmt,start=1):
    s.footer.is_linked_to_previous=False
    for el in list(s.footer._element):s.footer._element.remove(el)
    for el in list(s._sectPr):
        if el.tag==qn('w:pgNumType'):s._sectPr.remove(el)
    el=OxmlElement('w:pgNumType');el.set(qn('w:fmt'),fmt);el.set(qn('w:start'),str(start));s._sectPr.append(el)
    fp=s.footer.add_paragraph();fp.alignment=WD_ALIGN_PARAGRAPH.CENTER;fp.paragraph_format.first_line_indent=Cm(0)
    f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');rr=OxmlElement('w:r');tt=OxmlElement('w:t');tt.text='1';rr.append(tt);f.append(rr);fp._p.append(f)

# Keep the reference cover content and logo while preventing overflow and blank pages.
cover=doc.sections[0];geometry(cover)
for n in range(2):
    if n:p().add_run().add_break(WD_BREAK.PAGE)
    def cover_line(text,size,bold=True,after=4,before=0):
        cp=p(text);cp.alignment=WD_ALIGN_PARAGRAPH.CENTER;pf=cp.paragraph_format;pf.first_line_indent=Cm(0);pf.line_spacing=1.15;pf.space_before=Pt(before);pf.space_after=Pt(after)
        for rr in cp.runs:font(rr,size,bold)
        return cp
    cover_line('BỘ CÔNG THƯƠNG',13)
    cover_line('TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG THÀNH PHỐ HỒ CHÍ MINH',13)
    cover_line('KHOA CÔNG NGHỆ THÔNG TIN',14,after=12)
    cp=cover_line('',13,after=12);cp.add_run().add_picture(str(O/'template_image_0.png'),width=Cm(2.6))
    cover_line('KHÓA LUẬN CỬ NHÂN',18,after=6)
    cover_line('NGÀNH CÔNG NGHỆ THÔNG TIN',14,after=4)
    cover_line('MÃ ĐỀ TÀI CNTT_KLCN182',13,after=20)
    cover_line('NGHIÊN CỨU PHƯƠNG PHÁP TÍCH HỢP VMAMBA\nVÀO MÔ HÌNH YOLO26-SEG TRONG PHÂN ĐOẠN\nPOLYP TỪ ẢNH NỘI SOI ĐẠI TRỰC TRÀNG',16,after=24)
    cover_line('Sinh viên thực hiện',13,after=6)
    for txt in ['LÊ ĐỨC LƯƠNG     MSSV 2001230490     Lớp 14DHTH09','PHÙNG TUẤN HUY   MSSV 2001230312     Lớp 14DHTH13','TRẦN MẠNH TOÀN   MSSV 2001230830     Lớp 14DHTH09']:cover_line(txt,12,bold=False,after=4)
    cover_line('Giảng viên hướng dẫn\nTS. PHÙNG THẾ BẢO',13,after=26,before=20)
    cover_line('TP. HỒ CHÍ MINH NĂM 2026',13,after=0)
front=doc.add_section(WD_SECTION.NEW_PAGE);geometry(front);numbering(front,'lowerRoman')
for s in list(doc.sections)[:-1]:
    s.footer.is_linked_to_previous=False
    for e in list(s.footer._element):s.footer._element.remove(e)

def front_title(text):
    out=p(text,'Title');out.alignment=WD_ALIGN_PARAGRAPH.CENTER;out.paragraph_format.first_line_indent=Cm(0);out.paragraph_format.space_after=Pt(18);return out

front_title('LỜI CẢM ƠN')
p('Nhóm sinh viên xin cảm ơn quý thầy cô Khoa Công nghệ Thông tin, Trường Đại học Công Thương Thành phố Hồ Chí Minh đã trang bị kiến thức và tạo điều kiện để nhóm thực hiện khóa luận. Nhóm xin cảm ơn TS. Phùng Thế Bảo đã hướng dẫn quá trình xác định vấn đề nghiên cứu, xây dựng mô hình và trình bày kết quả.')
p('Nhóm cũng xin cảm ơn các tác giả bộ dữ liệu Kvasir, Kvasir-SEG và cộng đồng phát triển mã nguồn mở Ultralytics, PyTorch, Mamba cùng các thư viện được sử dụng. Những nguồn tài nguyên này giúp nhóm xây dựng thực nghiệm và kiểm tra lại các kết quả của đề tài.')
p('Nhóm trân trọng các ý kiến góp ý nhằm hoàn thiện phương pháp đánh giá và sản phẩm ứng dụng. Những giới hạn của dữ liệu, thực nghiệm và triển khai được trình bày trong báo cáo để xác định phạm vi sử dụng của kết quả.')
out=p('Nhóm sinh viên thực hiện');out.alignment=WD_ALIGN_PARAGRAPH.RIGHT
p().add_run().add_break(WD_BREAK.PAGE);front_title('LỜI CAM ĐOAN')
p('Nhóm sinh viên cam đoan các kết quả thực nghiệm trong khóa luận được trình bày theo số liệu và cấu hình lưu trữ của đề tài. Những nội dung kế thừa, kết quả công bố và phần mềm sử dụng được dẫn nguồn. Nhóm phân biệt các phép đo đã thực hiện với các nội dung dự kiến phát triển, và chịu trách nhiệm về nội dung báo cáo.')
p('Các nhận xét không vượt quá phạm vi của tập dữ liệu và giao thức đánh giá. Báo cáo không xem sản phẩm minh họa như một thiết bị chẩn đoán, không gán các chỉ số chưa đo cho mô hình và không dùng các kết quả nghiên cứu cũ thay cho nhóm TSVM FP32 của thực nghiệm chính.')
p('Nhóm sinh viên thực hiện').alignment=WD_ALIGN_PARAGRAPH.RIGHT
for title in ['NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN','NHẬN XÉT CỦA GIẢNG VIÊN PHẢN BIỆN']:
    p().add_run().add_break(WD_BREAK.PAGE);front_title(title)
    for label in ['Nội dung và phương pháp nghiên cứu','Kết quả thực nghiệm và sản phẩm ứng dụng','Hình thức trình bày và nội dung cần hoàn thiện','Đánh giá và kết luận']:
        p(label)
        for _ in range(2):p('..............................................................................................................')
    p('Giảng viên nhận xét').alignment=WD_ALIGN_PARAGRAPH.RIGHT
    p('Ký và ghi rõ họ tên').alignment=WD_ALIGN_PARAGRAPH.RIGHT
p().add_run().add_break(WD_BREAK.PAGE);front_title('TÓM TẮT KHÓA LUẬN')
p('Khóa luận nghiên cứu phương pháp tích hợp Topology-Shape-aware VMamba vào YOLO26s-seg cho phân đoạn polyp từ ảnh nội soi đại trực tràng. Khối C2TSVMamba thay C2PSA tại tầng 10, kết hợp SS2D bốn hướng với nhánh hình dạng đa tỉ lệ và có hướng. Cổng guidance điều chỉnh đặc trưng trạng thái trước bước hợp nhất. Checkpoint mô hình cải tiến được lưu và suy luận bằng FP32 để bảo toàn biểu diễn số.')
p('Thực nghiệm sử dụng BG20 gồm 1.040 ảnh huấn luyện và 160 ảnh kiểm định, với 20 cặp seed và 100 epoch cho mỗi lượt. Tại epoch có mask mAP50–95 cao nhất của mỗi lượt, baseline đạt 0,718868 ± 0,011768 và TSVM FP32 đạt 0,723171 ± 0,007197. Chênh lệch trung bình là 0,004303; khoảng tin cậy 95% [−0,000228; 0,008834] chứa 0, paired t-test p = 0,0614. Kết quả cho thấy xu hướng tăng trung bình và giảm độ phân tán giữa seed nhưng chưa chứng minh ưu thế trung bình ở ngưỡng 0,05.')
p('Ứng dụng PolypVision cung cấp client Web Spring Boot và Flutter Mobile dùng chung FastAPI. Hai checkpoint thực nghiệm được tích hợp với định danh, mã băm và kiểm tra FP32. Kết luận giới hạn ở ảnh tĩnh và tập kiểm định đã dùng chọn mô hình; cần thêm kiểm thử ngoài, ablation và độ đo biên/topology.')
p('Từ khóa: phân đoạn polyp; YOLO26s-seg; VMamba; SS2D; TSVM; FP32; thực nghiệm nhiều seed.')
p().add_run().add_break(WD_BREAK.PAGE);front_title('ABSTRACT')
p('This thesis investigates the integration of a Topology-Shape-aware VMamba block into YOLO26s-seg for colorectal polyp instance segmentation. C2TSVMamba replaces the backbone C2PSA block at layer 10 and combines four-direction selective state-space scanning with multi-scale directional shape features. The improved model uses FP32 checkpoint storage and inference to preserve numerical fidelity.')
p('The BG20 dataset contains 1,040 training and 160 validation images. Forty training runs cover 20 paired seeds for two models, with 100 epochs per run. At each run’s maximum validation mask mAP50–95 epoch, baseline and TSVM FP32 achieve 0.718868 ± 0.011768 and 0.723171 ± 0.007197. The paired mean difference is 0.004303, with a 95% confidence interval of [−0.000228, 0.008834] and a paired t-test p-value of 0.0614. The observed mean improvement is therefore inconclusive at the 0.05 significance level.')
p('PolypVision integrates the experiment checkpoints through a shared FastAPI inference service for Spring Boot Web and Flutter Mobile clients. The study separates validation-history summaries, saved-checkpoint inference and published literature results. External testing, controlled ablation and boundary or topology measurements remain necessary before broader claims can be made.')

p().add_run().add_break(WD_BREAK.PAGE);front_title('MỤC LỤC');toc_anchor=p('TOC_PLACEHOLDER');mark(toc_anchor,'toc_start')
p().add_run().add_break(WD_BREAK.PAGE);front_title('DANH MỤC HÌNH');fig_anchor=p('FIG_LIST_PLACEHOLDER')
p().add_run().add_break(WD_BREAK.PAGE);front_title('DANH MỤC BẢNG');table_anchor=p('TABLE_LIST_PLACEHOLDER')
p().add_run().add_break(WD_BREAK.PAGE);front_title('DANH MỤC CHỮ VIẾT TẮT')
table('Các thuật ngữ dùng trong báo cáo',['Ký hiệu','Diễn giải'],[
('AI','Trí tuệ nhân tạo'),('API','Giao diện lập trình ứng dụng'),('BG20','Bổ sung 200 ảnh nền trên 1.000 ảnh polyp gốc'),('CNN','Mạng nơ-ron tích chập'),('SSM','Mô hình không gian trạng thái'),('SS2D','Quét chọn lọc hai chiều'),('TSVM','Topology-Shape-aware VMamba'),('FP16 và FP32','Số thực dấu phẩy động 16 bit và 32 bit'),('EMA','Trung bình trượt hàm mũ của trọng số'),('IoU','Phần giao trên phần hợp'),('Dice','Hệ số tương đồng Dice'),('AP và mAP','Diện tích đường precision–recall và trung bình AP'),('TP FP FN','Đúng dương tính, sai dương tính, sai âm tính'),('KTC','Khoảng tin cậy'),('SD','Độ lệch chuẩn mẫu'),('Seed','Hạt giống của bộ sinh số ngẫu nhiên'),('P3 P4 P5','Mức đặc trưng có stride 8, 16 và 32'),('FP32 checkpoint','Checkpoint giữ tensor dấu phẩy động ở float32')],[3.4,11.6])
tables.pop() # Abbreviation table is not a numbered research table.
mainsec=doc.add_section(WD_SECTION.NEW_PAGE);geometry(mainsec);numbering(mainsec,'decimal')

raw=pd.read_csv(O/'verified_raw.csv');stats=pd.read_csv(O/'verified_statistics.csv').set_index('metric');audit=json.loads((O/'verified_audit.json').read_text());migration=json.loads((O/'app_migration.json').read_text());smoke=json.loads((O/'smoke_results.json').read_text())
f=lambda x,n=4:f'{x:.{n}f}'.replace('.',',')
names={'mask_map50_95':'Mask mAP50–95','mask_map50':'Mask mAP50','mask_precision':'Mask Precision','mask_recall':'Mask Recall','box_map50_95':'Box mAP50–95','box_map50':'Box mAP50','box_precision':'Box Precision','box_recall':'Box Recall','val_seg_loss':'Val segmentation loss'}

def dynamic_table(key):
    if key=='related':table('Bảng 1.1 Đối chiếu các công trình gần với đề tài',['Công trình','Thành phần trọng tâm','Khác biệt của đề tài'],[
        ('Polyp-Mamba [17]','Ngữ nghĩa đa tỉ lệ và global injection','Tích hợp trong YOLO26s-seg'),('Topo-VM-UNetV2 [18]','Persistent homology và Topo-SDI','Guidance học từ convolution'),('CSG-Mamba [19]','Convolutional gate tại bottleneck','Nhánh đa hướng và cổng 1+G'),('MambaPSA [20]','Thay C2PSA trong YOLO26','Shape guidance cho polyp instance segmentation'),('SAM-MaGuP [21]','SAM và boundary distillation','Không sử dụng SAM hoặc boundary distillation')],[4.1,5.2,5.7])
    elif key=='layers':table('Bảng 2.1 Các mức đặc trưng của cấu hình small',['Vị trí','Stride','Kích thước với 640','Số kênh'],[('Backbone P3','8','80 × 80','256'),('Backbone P4','16','40 × 40','512'),('Backbone P5 và layer 10','32','20 × 20','512'),('Head P3 layer 16','8','80 × 80','128'),('Head P4 layer 19','16','40 × 40','256'),('Head P5 layer 22','32','20 × 20','512')],[5.5,2,4.7,2.8])
    elif key=='ablation':table('Bảng 2.2 Các chế độ hỗ trợ trong mã nguồn',['Chế độ','SS2D','Shape','Guidance'],[('topology_shape_vmamba','Có','Có','Có'),('vmamba_only','Có','Không','Không'),('shape_only','Không','Có','Không'),('shape_vmamba_no_guidance','Có','Có','Không')],[8,2.3,2.3,2.4])
    elif key=='training':table('Bảng 4.1 Cấu hình thống nhất của 40 lượt huấn luyện',['Tham số','Giá trị','Ý nghĩa'],[('Seed','0–19','20 seed cho mỗi kiến trúc'),('epochs / patience','100 / 100','100 epoch được lưu mỗi lượt'),('imgsz / batch','640 / 8','Cấu hình kích thước và lô'),('optimizer / lr0','AdamW / 0,001','Cùng thuật toán và tốc độ đầu'),('weight_decay','0,0005','Suy giảm trọng số'),('warmup_epochs','5','Giai đoạn khởi động'),('lrf / cos_lr','0,01 / False','Không bật cosine schedule'),('workers','2','Nạp dữ liệu'),('amp / deterministic','False / True','Tắt AMP và bật chế độ tất định'),('close_mosaic','10','Tắt Mosaic ở 10 epoch cuối'),('mask_ratio / overlap_mask','4 / True','Biểu diễn mặt nạ'),('Pretrained','yolo26s-seg.pt','Nạp trực tiếp hoặc nạp phần tương thích')],[5,4,6])
    elif key=='api':table('Bảng 4.2 Các endpoint chính của dịch vụ AI',['Endpoint','Client','Nội dung'],[('GET /health','Web','Trạng thái thiết bị và registry'),('POST /predict','Web','Ảnh, modelType, overlay và metadata'),('GET /api/v1/health','Mobile','Trạng thái và requestId'),('GET /api/v1/models','Mobile','Hai model key và ready'),('POST /api/v1/inference','Mobile','Ảnh và modelKey'),('POST /api/v1/comparison','Mobile','Cùng ảnh qua hai mô hình')],[6.5,2.1,6.4])
    elif key=='app_tests':
        status=json.loads((O/'test_status.json').read_text(encoding='utf-8')) if (O/'test_status.json').exists() else {}
        table('Bảng 4.3 Phạm vi kiểm tra ứng dụng sau chuyển mô hình',['Nhóm kiểm tra','Phạm vi','Kết quả'],[('FastAPI','Giao thức, lỗi, so sánh, đồng thời, RGB',status.get('api','Đã kiểm tra, xem biên bản kèm mã nguồn')),('Spring Boot','Dịch vụ, controller, phân quyền, hợp đồng API',status.get('web','Đã kiểm tra, xem biên bản kèm mã nguồn')),('Flutter','Mô hình dữ liệu, điều hướng, màn hình, hợp đồng',status.get('mobile','Đã kiểm tra, xem biên bản kèm mã nguồn')),('Checkpoint thật','Hai model seed 0, hai ảnh mỗi model','Nạp và dự đoán thành công'),('Kiểu số','Tensor mô hình sau nạp','Float32 và hữu hạn')],[3.8,7.2,4])
    elif key=='main_metrics':
        rows=[]
        for k in names:
            s=stats.loc[k];rows.append([names[k],f'{f(s.baseline_mean)} ± {f(s.baseline_sd)}',f'{f(s.tsvm_mean)} ± {f(s.tsvm_sd)}',f(s.delta)])
        table('Bảng 5.1 Kết quả tại epoch tối đa mask mAP50 95 của mỗi lượt',['Chỉ số','Baseline trung bình ± SD','TSVM FP32 trung bình ± SD','Δ'],rows,[4.2,4.3,4.3,2.2])
    elif key=='inference':
        rows=[]
        for k in ['mask_map50_95','mask_map50','mask_precision','mask_recall','box_map50_95','box_recall','val_seg_loss']:
            s=stats.loc[k];rows.append([names[k],f'[{f(s.ci_low)}; {f(s.ci_high)}]',f(s.p_ttest),f(s.p_wilcoxon)])
        table('Bảng 5.2 Khoảng tin cậy và kiểm định ghép cặp hai phía',['Chỉ số','KTC 95% của Δ','p t-test','p Wilcoxon'],rows,[4.2,5.2,2.8,2.8])
    elif key=='seed_results':
        rows=[]
        for s in range(20):
            a=raw[(raw.model=='Baseline')&(raw.seed==s)].iloc[0];b=raw[(raw.model=='TSVM')&(raw.seed==s)].iloc[0]
            rows.append([s,int(a.best_epoch),int(b.best_epoch),f(a.mask_map50_95,5),f(b.mask_map50_95,5),f(b.mask_map50_95-a.mask_map50_95,5)])
        table('Bảng 5.3 Kết quả mask mAP50 95 và epoch theo từng seed',['Seed','Epoch B','Epoch T','Baseline','TSVM FP32','Δ'],rows,[1.7,2.2,2.2,3.0,3.0,2.9])
    elif key=='confusion':
        cm=pd.read_csv(R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/raw_20seeds_confusion_matrices.csv');rows=[]
        for m,l in [('Baseline','Baseline'),('TSVM','TSVM FP32')]:
            x=cm[cm.model==m];rows.append([l]+[f'{f(x[k].mean(),2)} ± {f(x[k].std(ddof=1),2)}' for k in ['TP','FP','FN']])
        table('Bảng 5.5 Thống kê bổ sung từ ma trận phát hiện theo đối tượng',['Mô hình','TP','FP','FN'],rows,[4.2,3.6,3.6,3.6])
    elif key=='benchmark':
        bench=pd.read_csv(R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/efficiency_benchmark/tables/efficiency_summary.csv')
        rows=[]
        for mode,lab in [('forward_only','Forward'),('predict_pipeline','Pipeline')]:
            a=bench[(bench.model=='YOLO26s-seg')&(bench['mode']==mode)].iloc[0];z=bench[(bench.model=='YOLO26s-TSVM-FP32-seg')&(bench['mode']==mode)].iloc[0]
            rows.append([lab+' mean ± SD ms',f(a.mean_ms,2)+' ± '+f(a.sd_ms,2),f(z.mean_ms,2)+' ± '+f(z.sd_ms,2)])
            for k,label in [('p50_ms','p50 ms'),('p95_ms','p95 ms'),('p99_ms','p99 ms'),('serial_images_per_second','ảnh mỗi giây')]:rows.append([lab+' '+label,f(a[k],2),f(z[k],2)])
        table('Bảng 5.7 Kết quả benchmark CPU FP32 với 100 lượt đo mỗi chế độ',['Đại lượng','YOLO26s seg','TSVM FP32'],rows,[7,4,4])
    elif key=='ranges':
        rows=[]
        for m,label in [('Baseline','Baseline'),('TSVM','TSVM FP32')]:
            x=raw[raw.model==m]['mask_map50_95'];rows.append([label,f(x.min(),5),f(x.median(),5),f(x.max(),5),f(x.max()-x.min(),5)])
        table('Bảng 5.4 Phân bố mask mAP50 95 theo nhóm',['Mô hình','Min','Median','Max','Range'],rows,[4.2,2.7,2.7,2.7,2.7])
    elif key=='efficiency':
        table('Bảng 5.6 Quy mô hai checkpoint được tích hợp vào ứng dụng',['Đại lượng','YOLO26s seg','TSVM FP32'],[('Số tham số','11.434.463','12.254.688'),('Dung lượng tệp best.pt MiB',f(migration['checkpoints'][0]['bytes']/2**20,2),f(migration['checkpoints'][1]['bytes']/2**20,2)),('Seed minh họa','0','0'),('Kiểu suy luận','Float32','Float32'),('Benchmark CPU FP32','Đã đo tại Bảng 5.7','Đã đo tại Bảng 5.7'),('Bộ nhớ tham số FP32 MiB','43,62','46,75'),('Benchmark GPU','Chưa đo','Chưa đo')],[7,4,4])
    elif key=='literature_results':
        table('Bảng 5.8 Kết quả tham khảo do tác giả công bố trên Kvasir SEG',['Nguồn và mô hình','Dice','IoU','Giao thức tóm tắt'],[('Polyp-Mamba [17], Bảng 1','0,940','0,881','900 Kvasir + 550 ClinicDB train; ảnh 224'),('Topo-VM-UNetV2 [18], Bảng I','0,9195','0,8654','900 Kvasir + 550 ClinicDB train; ảnh 256'),('CSG-Mamba [19], Bảng 1','0,9220','0,8677','800/100/100 Kvasir; 3 seed; ảnh 256')],[5.3,1.7,1.7,6.3])
        p('Ghi chú: Polyp-Mamba lấy số ở bản PDF hội nghị, không trộn với biến thể độ phân giải khác trong phần phản hồi tác giả. Các kết quả này không cùng giao thức với BG20.')

def import_chapter3():
    source=Document(R/'Bao_cao/Tien_Xu_Ly_Du_Lieu.docx')
    for el in source.element.body:
        if el.tag==qn('w:sectPr'):continue
        if el.tag==qn('w:p'):
            sp=Paragraph(el,source);text=sp.text
            if text.startswith('TÀI LIỆU THAM KHẢO CỦA CHƯƠNG'):break
            if sp.style.name.startswith('Heading'):
                lev=int(sp.style.name[-1]);heading(text.replace('CHƯƠNG 3.','CHƯƠNG 3'),lev);continue
        new=copy.deepcopy(el)
        for blip in new.iter(qn('a:blip')):
            old=blip.get(qn('r:embed'))
            if old:
                part=source.part.related_parts[old];rid,_=doc.part.get_or_add_image(BytesIO(part.blob));blip.set(qn('r:embed'),rid)
        body.insert(len(body)-1,new)
        if new.tag==qn('w:p'):
            np_=Paragraph(new,doc)
            if re.match(r'^Hình 3\.\d+\.',np_.text):
                nm=f'figure_3_{len(figures)}';mark(np_,nm);figures.append({'text':np_.text,'bookmark':nm})
            if re.match(r'^Bảng 3\.\d+\.',np_.text):
                nm=f'table_3_{len(tables)}';mark(np_,nm);tables.append({'text':np_.text,'bookmark':nm})
            if 'mỗi lần chạy lại chương trình đều cho ra đúng' in np_.text:pass
            if 'Quy trình tiền xử lý của mô hình' in np_.text:
                np_.text='Khối TSVM xử lý đặc trưng bên trong mô hình sau khi ảnh đã được chuẩn hóa. Hai kiến trúc sử dụng cùng quy trình tiền xử lý để giảm nhiễu do dữ liệu; đánh giá tác động kiến trúc vẫn cần xem cùng khởi tạo, tiêu chí chọn mô hình và cách bảo toàn checkpoint FP32.'
            for r in np_.runs:font(r)

references=[
'D. Jha và cộng sự, “Kvasir-SEG: A Segmented Polyp Dataset,” MMM, 2020, tr. 451–462. DOI: 10.1007/978-3-030-37734-2_37. https://arxiv.org/abs/1911.07069',
'K. Pogorelov và cộng sự, “Kvasir: A Multi-Class Image Dataset for Computer Aided Gastrointestinal Disease Detection,” MMSys, 2017, tr. 164–169. DOI: 10.1145/3083187.3083212. https://datasets.simula.no/kvasir/',
'D. Jha, “Kvasir-SEG Data: Polyp segmentation & detection,” Kaggle. https://www.kaggle.com/datasets/debeshjha1/kvasirseg. Truy cập 15/10/2026.',
'Ultralytics, “Instance Segmentation Datasets Overview.” https://docs.ultralytics.com/datasets/segment/. Truy cập 15/10/2026.',
'G. Bradski, “The OpenCV Library,” Dr. Dobb’s Journal of Software Tools, 2000.',
'N. Otsu, “A Threshold Selection Method from Gray-Level Histograms,” IEEE Transactions on Systems, Man, and Cybernetics, 9(1), 1979, tr. 62–66. DOI: 10.1109/TSMC.1979.4310076.',
'R. C. Gonzalez và R. E. Woods, Digital Image Processing, ấn bản 4. Pearson, 2018.',
'S. Suzuki và K. Abe, “Topological Structural Analysis of Digitized Binary Images by Border Following,” Computer Vision, Graphics, and Image Processing, 30(1), 1985, tr. 32–46. DOI: 10.1016/0734-189X(85)90016-7.',
'D. H. Douglas và T. K. Peucker, “Algorithms for the Reduction of the Number of Points Required to Represent a Digitized Line or its Caricature,” Cartographica, 10(2), 1973, tr. 112–122. DOI: 10.3138/FM57-6770-U75U-7727.',
'A. Bochkovskiy, C.-Y. Wang và H.-Y. M. Liao, “YOLOv4: Optimal Speed and Accuracy of Object Detection,” 2020. https://arxiv.org/abs/2004.10934',
'Ultralytics, “Data Augmentation using Ultralytics YOLO.” https://docs.ultralytics.com/guides/yolo-data-augmentation/. Truy cập 15/10/2026.',
'O. Ronneberger, P. Fischer và T. Brox, “U-Net: Convolutional Networks for Biomedical Image Segmentation,” MICCAI, 2015. https://arxiv.org/abs/1505.04597',
'D.-P. Fan và cộng sự, “PraNet: Parallel Reverse Attention Network for Polyp Segmentation,” MICCAI, 2020. https://arxiv.org/abs/2006.11392',
'A. Gu và T. Dao, “Mamba: Linear-Time Sequence Modeling with Selective State Spaces,” 2023. https://arxiv.org/abs/2312.00752',
'Y. Liu và cộng sự, “VMamba: Visual State Space Model,” NeurIPS, 2024. https://arxiv.org/abs/2401.10166',
'Ultralytics, “Ultralytics YOLO26” và mã cấu hình Segment26 của fork 8.4.127 sử dụng trong đề tài. https://docs.ultralytics.com/models/yolo26/. Truy cập 15/10/2026.',
'Z. Xu và cộng sự, “Polyp-Mamba: Polyp Segmentation with Visual Mamba,” MICCAI, 2024. DOI: 10.1007/978-3-031-72111-3_48. https://papers.miccai.org/miccai-2024/paper/0697_paper.pdf',
'D. Adame và cộng sự, “Topo-VM-UNetV2: Encoding Topology into Vision Mamba UNet for Polyp Segmentation,” arXiv preprint, 2025. https://arxiv.org/abs/2505.06210',
'Y. Wang, J. Wu, J. Song và S. Ren, “CSG-Mamba: A Convolutional Scoring Gating Vision State Space Network for Endoscopic Polyp Segmentation,” arXiv preprint, 2026. https://arxiv.org/abs/2608.14146',
'S.-W. Chan và cộng sự, “MambaPSA: A Mamba-based Replacement for C2PSA in YOLO26,” arXiv preprint, 2026. https://arxiv.org/abs/2607.12681',
'T. K. Dutta, S. Majhi, D. R. Nayak và D. Jha, “Mamba Guided Boundary Prior Matters: A New Perspective for Generalized Polyp Segmentation,” 2025. https://arxiv.org/abs/2507.01509',
'I. Loshchilov và F. Hutter, “Decoupled Weight Decay Regularization,” ICLR, 2019. https://arxiv.org/abs/1711.05101',
'SciPy, “scipy.stats.ttest_rel.” https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html. Truy cập 15/10/2026.',
'SciPy, “scipy.stats.wilcoxon.” https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html. Truy cập 15/10/2026.'
]

def refs():
    heading('TÀI LIỆU THAM KHẢO')
    for i,r in enumerate(references,1):
        out=p(f'[{i}] {r}');out.paragraph_format.first_line_indent=Cm(-.7);out.paragraph_format.left_indent=Cm(.7)
        for rr in out.runs:font(rr,12)
        out.alignment=WD_ALIGN_PARAGRAPH.LEFT

def appendices():
    heading('PHỤ LỤC A NGUỒN SỐ LIỆU VÀ QUY TẮC TÁI LẬP')
    p('Các đường dẫn dưới đây được tính tương đối từ thư mục archive để tránh phụ thuộc máy cá nhân. Hai nhóm chính chỉ lấy seed 0–19. Không thay thế thư mục TSVM_FP32 bằng nhóm TSVM không có hậu tố FP32.')
    for t in ['Mã cơ bản: ultralytics/.','Mã cải tiến: ultralytics_Topology-Shape-aware_VMamba_FP32/.','YAML đề xuất: cfg/models/26/yolo26-seg-TopologyShapeVMamba.yaml trong mã cải tiến.','Kết quả cơ bản: Ket_Qua_V2/KetQua_Nen/YOLOv26s-seg/.','Kết quả đề xuất: Ket_Qua_V2/KetQua_Nen/Kvasir_BG20_YOLO26s_seg_TSVM_FP32/.','Tổng hợp chính: Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/.','Notebook: Cell Kaggle/kvasir-yolo26s-seg.ipynb và kvasir-yolo26s-seg-topology-shape-awar.ipynb.','Tiền xử lý: Stracth/Du_Lieu/convert_kvasir_to_yolo_seg.py và Bao_cao/Tien_Xu_Ly_Du_Lieu.docx.']:
        p(t).alignment=WD_ALIGN_PARAGRAPH.LEFT
    p('Thuật toán trích xuất: đọc results.csv, chuẩn hóa tên cột, chọn dòng đầu tiên đạt max metrics/mAP50-95(M), lấy các chỉ số khác trên cùng dòng, ghép hai kiến trúc theo seed và tính độ lệch chuẩn mẫu. best.pt không được tái định nghĩa bằng quy tắc max-mask này.')
    heading('PHỤ LỤC B ĐỐI CHIẾU EPOCH VÀ CHECKPOINT')
    rows=[[x['model'] if x['model']=='Baseline' else 'TSVM FP32',x['seed'],x['max_mask_epoch'],x['fitness_epoch']] for x in audit['runs']]
    table('Bảng B.1 Epoch chọn theo mask và theo fitness của 40 lượt',['Mô hình','Seed','Max mask','Max fitness'],rows,[5,2,4,4])
    heading('PHỤ LỤC C CẤU HÌNH VÀ KIỂM TRA ỨNG DỤNG')
    p('Ứng dụng nằm tại DeepLearning/Ung_Dung/polypweb. Thư mục polypweb/ai-service là FastAPI, polypweb là Spring Boot và app_polyp là Flutter. Tệp models/experiment_manifest.json trong dịch vụ AI xác định checkpoint mặc định của từng model key.')
    for item in migration['checkpoints']:
        p(item['model_key']+'; seed 0; '+item['file'])
        pp=p('SHA-256: '+item['sha256']);pp.paragraph_format.first_line_indent=Cm(0)
        for rr in pp.runs:font(rr,10)
    p('Để chạy dịch vụ AI, kích hoạt môi trường đã cài đúng dependencies, vào polypweb/ai-service và dùng python -m uvicorn main:app --host 127.0.0.1 --port 8000. Kiểm tra /health và /api/v1/models trước khi gửi ảnh. Với điện thoại thật, cấu hình host và AI_BASE_URL theo địa chỉ mạng truy cập được; không mặc định localhost của điện thoại là máy chủ.')
    p('Web được khởi chạy bằng Maven Wrapper trong thư mục polypweb sau khi cấu hình MongoDB và kho lưu ảnh. Mobile chạy trong app_polyp với flutter run --dart-define=AI_BASE_URL=http://địa_chỉ_máy_chủ:8000. Không đưa tài khoản, mật khẩu, khóa hoặc ảnh cá nhân vào tài liệu chia sẻ.')
    p('Để đổi checkpoint, dùng AI_BASELINE_MODEL_PATH và AI_VMAMBA_MODEL_PATH, đồng thời kiểm tra model key, kiến trúc C2TSVMamba, nhãn polyp, kiểu float32 và mã băm. Không nạp checkpoint Nano cũ dưới nhãn TSVM FP32 mới.')
    heading('PHỤ LỤC D KẾ HOẠCH THỰC NGHIỆM BỔ SUNG')
    table('Bảng D.1 Các phép kiểm cần bổ sung trước khi mở rộng kết luận',['Hạng mục','Thiết kế cần thực hiện','Đầu ra'],[('Đánh giá checkpoint','Validate best.pt trên cùng dữ liệu và cấu hình','JSON/CSV gắn SHA-256'),('Ablation','Bốn mode, cùng seed và pretrained policy','Mean SD và Δ ghép cặp'),('Độ đo điểm ảnh','Quy định hợp nhất instance và ảnh rỗng','Dice IoU Boundary F1 HD95'),('Topology','Định nghĩa lỗi liên thông và lỗ','Betti error hoặc phép đo phù hợp'),('Tập ngoài','Không fine-tune trên tập test','ClinicDB ColonDB ETIS'),('Ảnh nền','Âm tính đa nguồn và cấp ảnh','False-alarm rate theo ảnh'),('Tốc độ mở rộng','Đo GPU và tải ứng dụng sau benchmark CPU','Median p95 và thời gian toàn trình')],[3.6,7.5,3.9])
    p('Các hạng mục trên là kế hoạch kiểm chứng, không phải các kết quả đã được cộng vào báo cáo hiện tại. Thứ tự ưu tiên là xác nhận checkpoint, đánh giá ngoài, phân tích ablation rồi mới tối ưu triển khai.')

content=(O/'report_content.md').read_text(encoding='utf-8')
# Correct numbering of the compact published-results table.
# Table numbering follows the expanded chapter.
for line in content.splitlines():
    if not line.strip():continue
    if line.startswith('### '):heading(line[4:],3)
    elif line.startswith('## '):heading(line[3:],2)
    elif line.startswith('# '):heading(line[2:],1)
    elif line.startswith('@TABLE '):dynamic_table(line.split()[1])
    elif line.startswith('@FIG '):name,title=line[5:].split('|',1);fig(name,title)
    elif line.startswith('@EQ '):
        out=p(line[4:]);out.alignment=WD_ALIGN_PARAGRAPH.CENTER;out.paragraph_format.first_line_indent=Cm(0)
    elif line=='@IMPORT_CHAPTER3':import_chapter3()
    elif line=='@REFERENCES':refs()
    elif line=='@APPENDICES':appendices()
    else:p(line)

def nav(anchor,entries,kind):
    # Cached, linked TOC entries with PAGEREF fields; Word can update them on open.
    # Keep an actual TOC field around the cached entry list for full regeneration.
    parent=anchor._p.getparent();idx=parent.index(anchor._p);parent.remove(anchor._p)
    if kind=='toc':
        start=OxmlElement('w:p');rr=OxmlElement('w:r');fc=OxmlElement('w:fldChar');fc.set(qn('w:fldCharType'),'begin');rr.append(fc);start.append(rr)
        rr=OxmlElement('w:r');instr=OxmlElement('w:instrText');instr.set(qn('xml:space'),'preserve');instr.text=' TOC \\o "1-2" \\h \\z ';rr.append(instr);start.append(rr)
        rr=OxmlElement('w:r');sep=OxmlElement('w:fldChar');sep.set(qn('w:fldCharType'),'separate');rr.append(sep);start.append(rr);parent.insert(idx,start);idx+=1
    for item in entries:
        el=OxmlElement('w:p');pp=Paragraph(el,doc);pp.paragraph_format.first_line_indent=Cm(0);pp.paragraph_format.space_before=Pt(1);pp.paragraph_format.space_after=Pt(1);pp.paragraph_format.line_spacing=1.15
        if item.get('level')==2:pp.paragraph_format.left_indent=Cm(.4)
        tabs=pp.paragraph_format.tab_stops
        from docx.enum.text import WD_TAB_ALIGNMENT,WD_TAB_LEADER
        tabs.add_tab_stop(Cm(15),WD_TAB_ALIGNMENT.RIGHT,WD_TAB_LEADER.DOTS)
        link=OxmlElement('w:hyperlink');link.set(qn('w:anchor'),item['bookmark']);r=OxmlElement('w:r');t=OxmlElement('w:t');t.text=item['text'];r.append(t);link.append(r);el.append(link)
        rr=pp.add_run('\t');font(rr,12)
        field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGEREF '+item['bookmark']+' \\h');r=OxmlElement('w:r');t=OxmlElement('w:t');t.text='0';r.append(t);field.append(r);el.append(field)
        parent.insert(idx,el);idx+=1
    if kind=='toc':
        el=OxmlElement('w:p');rr=OxmlElement('w:r');fc=OxmlElement('w:fldChar');fc.set(qn('w:fldCharType'),'end');rr.append(fc);el.append(rr);parent.insert(idx,el)

nav(toc_anchor,[b for b in bookmarks if b['level']<=2],'toc');nav(fig_anchor,figures,'figure');nav(table_anchor,tables,'table')
# Normalize imported tables and constrain all body pictures to the text area.
for t in doc.tables:
    for row in t.rows:
        for c in row.cells:
            for cp in c.paragraphs:
                cp.paragraph_format.first_line_indent=Cm(0)
for shape in doc.inline_shapes:
    if shape.width>Cm(15):
        ratio=Cm(15)/shape.width;shape.width=Cm(15);shape.height=int(shape.height*ratio)
    if shape.height>Cm(10):
        ratio=Cm(10)/shape.height;shape.height=Cm(10);shape.width=int(shape.width*ratio)
for cp in doc.paragraphs:
    for border in list(cp._p.iter(qn('w:pBdr'))):border.getparent().remove(border)
    if cp._p.xpath('.//w:drawing'):
        cp.paragraph_format.keep_with_next=True
        cp.paragraph_format.space_before=Pt(6);cp.paragraph_format.space_after=Pt(3)
for section in doc.sections:geometry(section)
settings=doc.settings.element
for el in list(settings):
    if el.tag==qn('w:updateFields'):settings.remove(el)
update=OxmlElement('w:updateFields');update.set(qn('w:val'),'true');settings.append(update)
doc.core_properties.title='Nghiên cứu phương pháp tích hợp VMamba vào YOLO26 seg trong phân đoạn polyp'
doc.core_properties.author='Lê Đức Lương; Phùng Tuấn Huy; Trần Mạnh Toàn'
doc.core_properties.subject='YOLO26s seg và TSVM FP32 trên BG20 với 20 seed'
doc.core_properties.comments=''
out=O/'working_report.docx';doc.save(out)
(O/'navigation.json').write_text(json.dumps({'headings':bookmarks,'figures':figures,'tables':tables},ensure_ascii=False,indent=2),encoding='utf-8')
print('Created',out,'paragraphs',len(doc.paragraphs),'tables',len(doc.tables),'images',len(doc.inline_shapes),'sections',len(doc.sections))
