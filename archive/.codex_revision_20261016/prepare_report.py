from pathlib import Path
O=Path(__file__).parent
old=(O/'report_content.md').read_text(encoding='utf-8')
tail=old[old.index('# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN'):]
intro=(O/'content/expanded_intro_ch1_ch2_ch4.md').read_text(encoding='utf-8')
chapter5=(O/'chapter5.md').read_text(encoding='utf-8')
(O/'report_content.md').write_text(intro+'\n'+chapter5+'\n\n'+tail,encoding='utf-8')
b=(O/'build_report.py').read_text(encoding='utf-8')
b=b.replace("sys.path.insert(0,str(O/'packages'))", "sys.path.insert(0,str(R/'.codex_report_work_20261015/packages'))")
b=b.replace("[4.2,4.6,4.6,1.6]", "[4.2,4.3,4.3,2.2]")
b=b.replace("'Bảng 5.3 Kết quả", "'Bảng 5.3 Kết quả")
b=b.replace("'Bảng 5.4 Thống kê", "'Bảng 5.5 Thống kê")
b=b.replace("'Bảng 5.5 Quy mô", "'Bảng 5.6 Quy mô")
b=b.replace("'Bảng 5.6 Kết quả tham khảo", "'Bảng 5.8 Kết quả tham khảo")
b=b.replace("content=content.replace('Bảng 5.8','Bảng 5.6')", "# Table numbering follows the expanded chapter.")
b=b.replace("status=json.loads((O/'test_status.json').read_text())", "status=json.loads((O/'test_status.json').read_text(encoding='utf-8'))")
b=b.replace("out.add_run().add_picture(str(O/'figures'/f'{name}.png'),width=Cm(14.8));caption(title,'figure')", "path=R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32'/f'{name[4:]}.png' if name.startswith('pkg:') else O/'figures'/f'{name}.png'\n    out.add_run().add_picture(str(path),width=Cm(14.8));caption(title,'figure').paragraph_format.keep_with_next=True")
b=b.replace("font(rr,12)\n\ndef appendices", "font(rr,12)\n        out.alignment=WD_ALIGN_PARAGRAPH.LEFT\n\ndef appendices")
# All imported picture captions must belong to the correct navigation lists.
b=b.replace("if sp.style.name == 'Caption' and np_.text.startswith('Hình 3.'):", "if re.match(r'^Hình 3\\.\\d+\\.',np_.text):")
b=b.replace("if sp.style.name == 'Caption' and np_.text.startswith('Bảng 3.'):", "if re.match(r'^Bảng 3\\.\\d+\\.',np_.text):")
b=b.replace("elif key=='efficiency':", "elif key=='ranges':\n        rows=[]\n        for m,label in [('Baseline','Baseline'),('TSVM','TSVM FP32')]:\n            x=raw[raw.model==m]['mask_map50_95'];rows.append([label,f(x.min(),5),f(x.median(),5),f(x.max(),5),f(x.max()-x.min(),5)])\n        table('Bảng 5.4 Phân bố mask mAP50 95 theo nhóm',['Mô hình','Min','Median','Max','Range'],rows,[4.2,2.7,2.7,2.7,2.7])\n    elif key=='efficiency':")
# Left align long source paths, keep caption sources with their figures.
b=b.replace("p(t)\n    p('Thuật toán", "p(t).alignment=WD_ALIGN_PARAGRAPH.LEFT\n    p('Thuật toán")
(O/'build_report.py').write_text(b,encoding='utf-8')
(O/'artifact.md').write_text('Bản mở rộng ngày 16/10/2026 giữ quy cách A4 Times New Roman và mẫu bìa của báo cáo. Mở rộng thực chất Mở đầu, Chương 1, 2, 4 theo bản cũ đã đối chiếu; thay Chương 5 bằng phân tích 20 seed FP32 có hình từ bộ 01–07 mới và benchmark thực đo. Giữ nguồn, số liệu gốc và bản sao trước sửa. Không dùng TN dựng lại, không gán AP thành Dice, không tuyên bố topology hoặc hiệu quả lâm sàng khi chưa đo. Mọi trang phải được render và kiểm tra trước giao.',encoding='utf-8')
print('Prepared expanded manuscript:',len(intro),len(chapter5),len(tail),'characters')
