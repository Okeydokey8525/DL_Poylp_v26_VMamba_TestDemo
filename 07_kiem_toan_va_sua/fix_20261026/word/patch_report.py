"""Targeted OOXML edits preserving the original report's layout and media."""
from pathlib import Path
import hashlib,json,shutil,sys,zipfile
from lxml import etree as E

sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
MAIN=ROOT/'Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx'
ALIAS=ROOT/'Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong_MoRong_FP32.docx'
EXPECTED='2caaf8b42c299f3c73a0087654f8f7d3c2986a83b8878d713613e0c9e1ed0856'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(MAIN)==EXPECTED and sha(ALIAS)==EXPECTED,'Report changed since audit: review current version before editing.'
for p in [MAIN,ALIAS]:
    backup=ROOT/'fix_20261026/backups'/p.name
    if backup.exists():assert sha(backup)==EXPECTED
    else:shutil.copy2(p,backup)
with zipfile.ZipFile(MAIN) as z:
    members={item.filename:(item,z.read(item.filename)) for item in z.infolist()}
doc=E.fromstring(members['word/document.xml'][1]);pars=doc.findall('w:body/w:p',NS)
def text(node):return ''.join(t.text or '' for t in node.findall('.//w:t',NS))
changes=[]
replacements={
363:'Với dữ liệu Kvasir-SEG [1], [3], đề tài giữ cố định hai danh sách train.txt và val.txt gồm 880 ảnh huấn luyện và 120 ảnh kiểm định. Hai mô hình sử dụng cùng cách chia để phép đối chứng có cùng đầu vào. Các danh sách được lưu cùng dữ liệu của đề tài; nguồn phát hành riêng của hai tệp này chưa được xác minh. Kiểm tra tên tệp và SHA-256 không phát hiện ảnh trùng hoàn toàn giữa hai tập.',
447:'Kiểm tra độc lập trên bộ dữ liệu đang sử dụng cho thấy mỗi ảnh có đúng một tệp nhãn và không có nhãn thiếu ảnh. Toàn bộ 1.063 dòng nhãn thuộc lớp 0, có ít nhất ba đỉnh và tọa độ trong [0,1]. So sánh SHA-256 không phát hiện ảnh trùng hoàn toàn giữa tập huấn luyện và kiểm định. Khi tái chạy chuyển đổi trên 1.000 mặt nạ với OpenCV 4.12.0 và NumPy 2.2.6, có 999 tệp nhãn khớp từng ký tự; tệp còn lại khác một đỉnh 3 pixel trên mỗi trục, chưa xác định nguyên nhân. Các nhãn hiện hành được giữ nguyên. Việc chọn ảnh nền với seed 42 tái tạo đúng danh sách 200 ảnh. Kết quả xác nhận quy mô và cấu trúc dữ liệu; mức khớp tuyệt đối cần được kiểm tra cùng phiên bản môi trường.',
515:'Hai checkpoint seed 0 đã được nạp với đúng task segment và lớp polyp; các tensor dấu phẩy động trong mô hình sau tải là float32 và hữu hạn. Kiểm tra thực hiện dự đoán trên cùng một ảnh có polyp và một ảnh normal-cecum cho cả hai mô hình, với ngưỡng confidence 0,25. Trên ảnh polyp, Baseline trả một mặt nạ và TSVM FP32 trả hai mặt nạ. Cả hai không trả mặt nạ trên ảnh nền. Số mặt nạ không tự xác định dự đoán đúng hoặc sai khi chưa ghép với nhãn chuẩn.',
766:'BG20: Ket_Qua_V2/Data Prosessing/convert_kvasir_with_background_to_yolo_seg.py. Hướng dẫn tái lập: doc/28_HUONG_DAN_TAI_LAP_BG20_2026_10_26.md.'
}
for number,new in replacements.items():
    p=pars[number-1];old=text(p)
    assert not p.findall('.//w:drawing',NS) and not p.findall('.//w:fldChar',NS)
    nodes=p.findall('.//w:t',NS);assert nodes
    nodes[0].text=new
    for node in nodes[1:]:node.text=''
    changes.append({'location':f'P{number:04}','old':old,'new':new,'old_characters':len(old),'new_characters':len(new)})
row=doc.findall('w:body/w:tbl',NS)[2].findall('w:tr',NS)[2]
cells=row.findall('w:tc',NS)
assert [text(c) for c in cells]==['Backbone P4','16','40 × 40','512']
nodes=cells[3].findall('.//w:t',NS);nodes[0].text='256'
for n in nodes[1:]:n.text=''
changes.append({'location':'Bảng 2.1 / Backbone P4 / Channels','old':'512','new':'256'})
updated=E.tostring(doc,encoding='UTF-8',xml_declaration=True,standalone=True)
tmp=HERE/'report_patched.docx'
with zipfile.ZipFile(tmp,'w') as z:
    for name,(info,data) in members.items():z.writestr(info,updated if name=='word/document.xml' else data)
with zipfile.ZipFile(tmp) as z:
    for name,(info,data) in members.items():
        if name!='word/document.xml':assert z.read(name)==data,name
    check=E.fromstring(z.read('word/document.xml'))
    assert len(check.findall('w:body/w:p',NS))==len(pars)
    assert len(check.findall('w:body/w:tbl',NS))==19
shutil.copy2(tmp,MAIN);shutil.copy2(tmp,ALIAS)
(HERE/'changes.json').write_text(json.dumps({'before_sha256':EXPECTED,'after_sha256':sha(MAIN),'alias_sha256':sha(ALIAS),'unchanged_zip_members':len(members)-1,'changes':changes},ensure_ascii=False,indent=2),encoding='utf-8')
print('Updated main and matching FP32 alias; only word/document.xml changed; paragraphs',len(pars),'tables19; edits',len(changes))
