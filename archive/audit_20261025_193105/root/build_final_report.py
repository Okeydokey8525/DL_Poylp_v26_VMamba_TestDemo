"""Compile audit findings only; never modifies original project artifacts."""
from pathlib import Path
import csv,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')

HERE=Path(__file__).resolve().parent;OUT=HERE.parent;ROOT=OUT.parent
def link(label,p):return f'[{label}](<{Path(p).resolve().as_posix()}>)'
def evidence(p):return link(p,OUT/p)
validation=json.loads((HERE/'checkpoint_revalidation_summary.json').read_text())
integrity=json.loads((HERE/'source_after_check.json').read_text())
meta=json.loads((HERE/'checkpoint_metadata.json').read_text())
issues=[
('E-004','high','CONFIRMED_RUNTIME_FAILURE','Web /comparisons và /api/v1/comparisons','ComparisonHistorySearchRepository.java:50,143–153','HTML503/API500; Mongo40600 vì $facet lồng $facet','E_application/logs/comparison_diagnostic.log','Pipeline Mongo không hợp lệ; đã tái hiện bằng repository thật','Đưa data/count/invalidGroups về cùng một tầng facet hoặc tách query; sửa mapper; thêm test Mongo thật cho rỗng/có dữ liệu/filter/pagination'),
('E-002','medium','CONFIRMED_MISMATCH','Web trang kết quả TSVM','DiagnosisController.java:147–149','Tên TSVM nhưng badge BASELINE','E_application/screenshots/03_tsvm_result_badge.png','contains(vmamba) không khớp model key TSVM','Dùng enum/model key thống nhất; test HTML cho cả hai model; không đổi checkpoint'),
('E-003','medium','CONFIRMED_MISMATCH','Web kích thước ảnh','DiagnosisHistoryService.java:110','Ảnh621×530 bị hiển thị1280×720','E_application/screenshots/04_tsvm_maskcount_dimensions.png','Kích thước bị hard-code','Lưu width/height thật khi giải mã; xử lý bản ghi cũ không rõ kích thước có chủ đích'),
('E-001','low','CONFIRMED_MISMATCH','Web trang chủ','HomeController.java:18','Nêu YOLO26n/Nano dù registry và runtime dùng S','E_application/screenshots/02_home_stale_model.png','Chuỗi mô tả mô hình còn từ giai đoạn cũ','Lấy tên từ danh mục mô hình chung; xác nhận UI với runtime keys'),
('C-001','medium','CONFIRMED_MISMATCH','Word Bảng2.1 hàng Backbone P4','T03R003','512 kênh; thực tế256 sau scale s','root/checkpoint_inventory.json','Bảng mô tả chưa áp width multiplier0.5 đúng cho P4','Sửa giá trị thành256; so lại các kích thước với YAML/parser/checkpoint'),
('C-002','medium','CONFIRMED_MISMATCH','Word mục4.6 ví dụ polyp','P0515; alias E-006 và B-C002','Viết cả hai trả1mask; thực tế Baseline1,TSVM2','E_application/runtime/true_inference_smoke.json','Lời văn không khớp log lịch sử và suy luận thật tái hiện','Sửa số lượng đúng; không tự gán mask thứ2 là FP khi chưa ghép GT'),
('ROOT-001','low','REPRODUCTION_MISMATCH_CURRENT_ENV','Word mục3.7 và nhãn validation','P0447; ck2bxiswtxuw80838qkisqjwz.txt; alias B-003','999/1000 nhãn khớp từng ký tự;1nhãn khác1đỉnh khoảng3px, polygon IoU0.99981118','B_visual/dataset_label_crosscheck.json','Chưa xác định nguyên nhân; OpenCV4.12.0/numpy2.2.6 là môi trường đã thử; không chứng minh dữ liệu hỏng','Giữ nguyên nhãn hiện hành; ghi phiên bản,hash và kết quả tái lập có điều kiện; điều tra khác biệt trước khi sửa nhãn'),
('C-003/C-004','medium','CONFIRMED_REPRODUCIBILITY_GAP','Tái lập local/BG20 và phụ lụcA','data_bg20.yaml:2; WordP0766','Path local không tồn tại; phụ lục thiếu builder bổ sung ảnh nền','root/dataset_independent.json','Đường dẫn/mapping script theo layout cũ','Trỏ data tới Ket_Qua_V2/Kvasir_YOLO_SEG_BG20; mô tả builder BG20 và tham số nguồn hiện tại; không suy historicalKaggle sai'),
('C-005','high','CONFIRMED_DOCUMENT_DRIFT','Bản thảo Markdown báo cáo','Bao_cao/md viet bao cao/05...,06...,07...','Còn10seed,SGD,TN suy diễn,Dice/GPU speed chưa đo; khác Word mới','C_report/report.md','Các thế hệ tài liệu chưa được phân nhãn/đồng bộ','Đánh dấu historical hoặc đồng bộ có kiểm nguồn trước khi dùng builder tái sinh Word'),
('C-006','medium','CONFIRMED_DOCUMENT_DRIFT','Markdown kiến trúc','doc/01_KIEN_TRUC_TSVM_TANG_10.md:49,62,69','Gate G thay1+G; FFN3×3/GELU thay hai1×1; complexity không khớp triển khai','C_report/report.md','Sơ đồ và mô tả cũ không theo source hiện tại','Sửa theo code; phân biệt tensor work O(LlogL) với parallel depth O(logL)'),
('C-007','medium','CONFIRMED_DOCUMENT_DRIFT','Điểm vào tài liệu hiện trạng','doc/README.md; doc/CURRENT_PROJECT_STATUS.md','Ưu tiên10seed/CM cũ trong khi bộ hiện tại20seedFP32','C_report/report.md','Snapshot cũ vẫn mang tên current/nguồn ưu tiên','Thêm chỉ mục hiện trạng mới và giữ lịch sử đúng ngày; không đổi raw để khớp tài liệu'),
('A-01/A-02','medium','CONFIRMED_INVALID_INTERPRETATION','Legacy TN trong gói20seed','facts.json và raw_20seeds_confusion_matrices.csv','TN_reconstructed=40−FP đối tượng không phải TN ảnh','A_numeric/discrepancies.csv','Nhầm đơn vị đối tượng và ảnh; bảng mới đã loại trường này','Quarantine/deprecate trường legacy; không tính specificity; đánh giá riêng cấp ảnh nếu cần'),
('A-03','medium','CONFIRMED_MISMATCH','Legacy bảng thắng/thua loss','summary_20seeds_paired.csv dòng val_seg_loss','tsvm_wins6 theo chiều tăng; lower-is-better đúng14','A_numeric/independent_summary.csv','Tên wins dùng cùng chiều cho metric và loss','Dùng bảng mới có lower_is_better hoặc đổi nhãn higher/lower; không đổi rawloss'),
('D-001/C-008','medium','INSUFFICIENT_EVIDENCE','Nguồn gốc split880/120','WordP0363 citation[3]','Chưa chứng minh hai danh sách do nhóm tác giả dataset phát hành','D_literature/reference_verification.csv','Thiếu release/version/URL có chính train.txt và val.txt','Bổ sung snapshot/hash/source release hoặc mô tả trung tính danh sách đang sử dụng; không khẳng định split sai'),
('B-001','low','CONFIRMED_CONVENTION_DIFFERENCE','Hai hình hội tụ legacy','figures/04_convergence_loss_curves.png và05_metric_curves_mAP.png','ddof0 thay ddof1; band nhỏ hơn sampleSD khoảng2.532%','B_visual/report.md','Hai thế hệ script dùng khác quy ước SD','Ghi đúng quy ước hoặc dùng hình mới ddof1 nhất quán; không coi là rawdata sai'),
('B-002','low','INSUFFICIENT_EXACT_RENDER_PROVENANCE','11hình legacy','figures/','Không tái tạo pixel-identical; giá trị/nguồn được kiểm nhất quán','B_visual/other_reproduction_pixel_comparison.csv','Chưa xác nhận nguyên nhân khác renderer/phiên bản/style','Giữ nguồn/phiên bản/font và tách legacy; không suy hash ảnh khác là giả hay sai số'),
('D-002','info','INDEX_MAPPING_REQUIRED','Số tài liệu TLTK và Word','TLTK[20]/[21] khác Word[20]/[21]','Không thể ghép tài liệu chỉ theo số[n]','D_literature/reference_verification.csv','Hai danh mục được tổ chức theo thứ tự khác nhau','Dùng ID/DOI/tiêu đề ổn định; SAM-Mamba và SAM-MaGuP là hai nguồn khác nhau'),
('E-005','low','AMBIGUOUS_COPY','Copy trang chủ','templates/index.html:31','Câu không cần đăng nhập có thể bị hiểu là inference không cần tài khoản','E_application/report.md','Phạm vi demo tĩnh chưa rõ; không phải authbypass','Phân biệt demo công khai với inference/lịch sử cần đăng nhập'),
('ROOT-002','info','REVALIDATION_SENSITIVITY','P/R của checkpoint Baseline so CSV','root/checkpoint_all_metric_comparison.csv','AP khớp trong ngưỡng nhưng P/R một số run không tái tạo chính xác','root/checkpoint_revalidation_summary.json','Nguyên nhân riêng chưa chứng minh; serialization/precision/backend và điểm F1 có thể ảnh hưởng','Công bố cả sai khác P/R; không gộp PASS AP thành mọi metric khớp; đồng nhất chính sách lưu nếu thiết kế đối chứng mới'),
('ROOT-003','info','HISTORICAL_PROVENANCE_LIMIT','TSVM cũ và FP32','20seed×100epoch×23cột','44.000 ô non-time giống;2.000 ô time khác','A_numeric/lineage_numeric_columns_old_vs_fp32.csv','Phù hợp khả năng rerun tất định; không tự chứng minh hoặc phủ định rerun','Giữ log import/runtime/dataset/checkpoint hash; không cáo buộc từ việc trùng số'),
('D-004','info','PARTIAL_FULLTEXT_SUPPORT','Sách Gonzalez/Woods và Suzuki/Abe','Word[7]/[8]','Metadata xác nhận; chưa đủ fulltext hợp pháp để kiểm mọi locator','D_literature/report.md','Giới hạn truy cập toàn văn','Bổ sung locator từ bản hợp pháp và OpenCV API/source cho bước thực thi cụ thể'),
('D-005/C-011','info','TURNITIN_NOT_ASSESSED','Toàn báo cáo','Chưa có báo cáo/settingsTurnitin','Không thể kết luận đạt ngưỡng30%','D_literature/report.md','Thiếu phép kiểm thật với cấu hình trường và lịch sử nộp','Lấy báo cáo chính thức đúngfile/settings; không diễn giải sàng lọc cục bộ thành %Turnitin')
]
with (OUT/'ISSUES.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['id','severity','status','area','location','finding','evidence_relative_to_audit','cause_and_certainty','recommended_fix_and_retest']);w.writerows(issues)
status='HOÀN TẤT PHẠM VI ĐÃ KHAI BÁO' if validation['complete'] else 'ĐANG HOÀN TẤT ĐÁNH GIÁ CHECKPOINT'
counts={m:d['successful'] for m,d in validation['models'].items()}
vrows=[]
for m,d in validation['models'].items():
    ap=d['metrics']['metrics/mAP50-95(M)'];p=d['metrics']['metrics/precision(M)'];r=d['metrics']['metrics/recall(M)']
    vrows.append(f'|{m}|{d["successful"]}/20|{ap["actual_mean"]:.6f} ± {ap["actual_sample_sd"]:.6f}|{ap["max_abs_delta_to_csv"]:.8f}|{p["n_abs_delta_over_0_005"]}|{r["n_abs_delta_over_0_005"]}|')
secondary=validation.get('secondary_checkpoint_comparison')
secondary_text=(f'Đối chiếu phụ trên best.pt tái đánh giá: Δ mask AP={secondary["delta_mask_AP"]:.6f}, paired t p={secondary["paired_t_p"]:.6f}, CI95%=[{secondary["CI95"][0]:.6f}; {secondary["CI95"][1]:.6f}]. Đây là phân tích kiểm chứng phụ, không thay endpoint max-mask ban đầu và không phải test ngoài.' if secondary else 'Chưa tính so sánh ghép cặp checkpoint khi chưa đủ40 lượt đánh giá thành công.')
table='\n'.join(f'|{i}|{sev}|{area}|{finding}|' for i,sev,st,area,loc,finding,ev,cause,fix in issues if sev in {'high','medium'})
text=f'''# Kiểm toán kết quả TSVM FP32 và PolypVision

Đợt kiểm toán bắt đầu ngày25/10/2026. Trạng thái: **{status}**. Đây là báo cáo kiểm toán, không phải bản sửa luận văn hoặc mã nguồn.

Bản đối chiếu chính: {link('CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx',ROOT/'Bao_cao/CNTT_KLCN182_BaoCaoKhoaLuan_LeDucLuong.docx')}. SHA-256: `2caaf8b42c299f3c73a0087654f8f7d3c2986a83b8878d713613e0c9e1ed0856`.

## Kết luận tổng kiểm

Các phép tổng hợp thống kê chính của bộ20seed FP32 **khớp dữ liệu đang lưu**. Chưa phát hiện sai số số học trong36CSV đã kiểm; các con số chính trong Word khớp CSV. Có lỗi thật trong mô tả Word, tài liệu legacy, khả năng tái lập cục bộ và ứng dụng Web. Không thể đánh dấu toàn dự án là hoàn toàn đạt chỉ từ kết quả thống kê hoặc test unit pass.

Phán quyết phải tách bốn lớp: **nguồn hiện vật**, **phép tính**, **hình thể hiện**, **câu diễn giải/chạy thực tế**. CSV nhất quán không tự chứng minh nguồn phiên Kaggle; cùng hash không phải chứng nhận độc lập lịch sử huấn luyện. Không có bằng chứng từ cuộc kiểm toán này để cáo buộc giả số liệu.

## Phạm vi và kiểm tra chéo

|Phòng|Phần đã thực hiện|Bằng chứng chi tiết|
|---|---|---|
|A|40rawCSV,36CSV dẫn xuất/benchmark,13metric,epoch/statistics và lineage10/21/20seed|{evidence('A_numeric/report.md')}|
|B|46hình gói,400ảnh đường cong/CM,33ảnh nhúng Word;35PNG mới pixel-identical; mẫu10cặpGT/pred|{evidence('B_visual/report.md')}|
|C|783đoạn,19bảng,24mục tham khảo;357ô thống kê/epoch/timing;1.240trường cấu hình|{evidence('C_report/report.md')}|
|D|24mục tham khảo Word,24PDFTLTK,4PDF tải công khai;10công trình liên quan|{evidence('D_literature/report.md')}|
|E|Build/test cách ly; Web/FastAPI/Mongo thật, browser, inference, ownership/export/delete/persistence và AI-off|{evidence('E_application/report.md')}|
|Tổng kiểm|Tính lại t/CI bằng thư viện chuẩn; dataset/1.000mask;40checkpointdtype/metadata;AP tái đánh giá; kiểm nguồn/screenshot/paper độc lập|{evidence('root/checkpoint_revalidation_summary.json')}|

Số phép kiểm ô là phạm vi công việc, không phải số thí nghiệm độc lập hay xác suất không còn lỗi. 357ô Word là nhóm thống kê/epoch/timing; không có nghĩa mọi con số Word đều đúng (Bảng2.1 có lỗi P4).

Các phòng kiểm lần đầu độc lập, sau đó trao đổi chứng cứ. Tổng kiểm đã tự kiểm P4 từ checkpoint, log maskCount và suy luận Web, mã/source và screenshot badge/kích thước, pipeline Mongo lồng facet, bảng Polyp-Mamba từ ảnh PDF và các nguồn primary gần đề tài. Các alias cùng lỗi (C-002/E-006/B-C002) được gộp, không đếm thành ba lỗi.

Hai phòng bị gián đoạn giới hạn sử dụng và được tiếp tục từ đầu ra đã lưu; các nhiệm vụ còn thiếu không bị đánh dấu hoàn tất chỉ vì đã có file trung gian.

## Kết quả thống kê gốc

|Quy tắc|Baseline maskAP mean ± sampleSD|TSVMFP32|Δ|paired t p|
|---|---:|---:|---:|---:|
|Cực đại maskAP từng run|0,718868 ± 0,011768|0,723171 ± 0,007197|+0,004303|0,061431|
|Cực đại fitness box+mask từ CSV|0,717397 ± 0,012877|0,722199 ± 0,007527|+0,004802|0,061898|

Endpoint chính trong Word là hàng đầu. CI95% của Δ=[−0,000228;0,008834], chứa0; TSVM cao hơn13/20cặp và sampleSD thấp hơn khoảng38,85%. Chưa đủ bằng chứng ưu thế trung bình tại α0,05. Có16/40run khác epoch giữa hai quy tắc. Không đổi endpoint sau khi xem p. Tất cả seed dùng cùng validation đã tham gia chọn epoch; chưa phải patient-disjoint/external test.

Lineage được kiểm:240ô metric10seed khớp nguồn;20seedTSVM cũ/FP32 có44.000ô non-time giống và2.000ô time khác. Điều này có thể phù hợp rerun tất định khi bản vá chỉ đổi lưu checkpoint; cần log phiên để chứng thực lịch sử, không suy từ đó là gian lận.

## Kiểm checkpoint và đánh giá lại

40/40best.pt đọc được:20Baseline lưu tensorfloat16,20TSVM lưufloat32, không có tensor không hữu hạn. Seed và tên run trong40checkpoint đều khớp thư mục; embedded train_results khớp rawCSV trong phạm vi được lưu. Metadata nhất quán vẫn không tự chứng minh mọi thao tác lịch sử ngoài máy.

Dataset validation được sao chép vào vùng kiểm toán để tránh ghi cache lên nguồn.320tệp ảnh/nhãn của bản sao khớp byte với nguồn. Tái đánh giá dùng research fork8.4.127 đã vá, PyTorch2.6.0+cpu, batch16,rect=True,imgsz640,half=False,workers0. Đây là cách batching/resize tương ứng validator trong train, khác phép probe squarebatch4 ban đầu.

|Model|Đã tái đánh giá|MaskAP checkpoint mean ± SD|Max absΔAP với CSVfitness|Run có absΔmaskP>0,005|Run có absΔmaskR>0,005|
|---|---:|---:|---:|---:|---:|
{chr(10).join(vrows)}

Ngưỡng0,005 là tiêu chí đối chiếu AP đã khai báo, không phải chứng minh mọi metric giống chính xác. P/R của một số Baseline khác rõ hơn AP; bảng mọi sai khác được giữ tại {evidence('root/checkpoint_all_metric_comparison.csv')}. Không quy nguyên nhân chắc chắn cho FP16, backend hoặc điểm F1 nếu chưa có thí nghiệm cô lập. TSVM được đối chiếu riêng; không dùng PASS AP che sai khác P/R.

{secondary_text}

**Hiệu chỉnh phương pháp của chính kiểm toán:** probe đầu rect=False,batch4 trênBaseline0 cho AP lệch khoảng−0,00949; sau đối chiếu source và dùngrect=True,batch16, lệch còn−0,00124. Probe khác giao thức không được tính là lỗi checkpoint. Trường `threads=4` trong JSONL gốc là giá trị yêu cầu trước validator; CPU `select_device` đặt lại8, đã kiểm ở {evidence('root/thread_protocol_verification.json')}. Không dùng timing các lượt này làm benchmark vì còn tải cạnh tranh. Log gốc được giữ, không sửa cho đẹp.

## Dataset và tiền xử lý

Đã kiểm1.040ảnhtrain/1.040nhãn (160rỗng,936instances),160ảnhval/160nhãn (40rỗng,127instances). Không thiếu/orphanlabel, mọi nhãn class0, ít nhất3đỉnh và tọa độ hữu hạn trong[0,1]; không trùng ảnh hoàn toàn giữa train/val quaSHA256. Không có metadata bệnh nhân nên không chứng minh patient-disjoint hoặc không có near-duplicates.

Tái tạo1.000mask trong bộ nhớ cho Otsu5–8,1.206contour,loại143,giữ1.063; vertices mean333,1552→24,6369,range10–80. Cả200ảnh nền chọn seed42 khớp danh sách và byte ảnh. Có999nhãn khớp từng ký tự; một nhãnval khác một đỉnh khoảng3px vớiOpenCV4.12.0/numpy2.2.6. PhòngB tái hiện bằng chính hàm builder:27pixel raster khác, polygon-pairIoU0,99981118. Đây là khác biệt tái lập nhỏ trong môi trường thử, không chứng minh nhãn bị hỏng và không sửa nhãn trong cuộc kiểm toán. Xem {evidence('root/preprocessing_independent.json')} và {evidence('B_visual/dataset_label_crosscheck.json')}.

## Hình ảnh

27hình kết quả mới và8hình benchmark tái tạo giống từng pixel trong môi trường tái sinh. PhòngA kiểm dữ liệu độc lập để không dùng việc chạy lại cùng script làm chứng nhận duy nhất về số học. 40CM đếm và40CM chuẩn hóa có240ô số khớp và80ôTN trống.80PR có legendAP50 lệch fitness-log tối đa0,00125; digitization chỉ là xấp xỉ, không thay prediction arrays.

33/33image occurrences Word truy được nguồn;560ô số nguồn hình riêng Word và88.000giá trị non-time đường cong cached khớp raw/A. Chưa nghiệm thu toàn bộ97trang render Word; hash media khớp không bảo đảm mọi chi tiết bố cục trang không bị crop.

11hình legacy khác pixel khi tái sinh, chưa đủ căn cứ gọi sai số liệu. Hai hình legacy dùngpopulationSD(ddof0) khác sampleSD(ddof1) của gói mới. Mẫu10cặpGT/pred của hai model seeds0,5,8,18,19 dùng cùng16tile; đã thấy false-alarm/missing-overlay examples thông thường. Mẫu không chứng minh ưu thế tổng thể, không đếm thành160ảnh độc lập và không chứng nhận ngưỡng JPEG khi thiếu metadata.

## Báo cáo và ứng dụng

Word mới nhìn chung dùng đúng20cặp, gate1+G, FFN1×1, tensorworkO(LlogL), quy tắc epoch và giới hạn topology/Dice. Tuy nhiên phải sửa Bảng2.1 P4=256, ví dụTSVM2mask, và ràng buộc câu1.000nhãn exact-match theo bằng chứng môi trường. Tài liệu Markdown cũ có các phát biểu không còn hợp lệ; không dùng chúng để sinh lại Word trước khi đồng bộ.

Web khởi động và suy luận thật được;51pytest và261Java test pass không phát hiện pipeline Mongo thật bị cấm. Lịch sử so sánh đang lỗi; registry/inference thật vẫn đúng cặpS. Badge sai là lỗi view, không phải chứng minh nạp nhầm mô hình. Các server kiểm toán đã được dừng, dữ liệu kiểm thử riêng được giữ. Mobile chỉ đọc nguồn, chưa chạy hoặc xác nhận lại498test. Xem toàn bộtest/screenshot/cleanup tại {evidence('E_application/report.md')}.

## Tài liệu, tính mới và Turnitin

24mụcWord đã được đối chiếu:23metadata xác nhận; trangKaggle tồn tại nhưng chưa chứng minh tác giả phát hành split880/120. Ba dòngBảng5.8 khớp bảngPDF gốc và giao thức; không dùngDice/IoU của paper để xếp hạng trực tiếp với APBG20.

Đã lập ma trận10công trình gần. [MambaPSA](https://arxiv.org/abs/2607.12681) rất gần về thayC2PSA trongYOLO26; [PolyMamba](https://papers.miccai.org/miccai-2025/0704-Paper3872.html) là nguồn phù hợp spatial-prior/frequencyguidance đã có trongTLTK. Đóng góp phải mô tả ở thiết kế và thí nghiệm cụ thể; không khẳng định đầu tiên tuyệt đối. TLTK vàWord đánh số khác nhau, không copy số[n] giữa hai danh mục. Đề xuất có mục đích trong {evidence('D_literature/suggested_references.md')}.

Chưa có báo cáoTurnitin hoặc thiết lập trường/lịch sử nộp. Sàng lọc chuỗi khớp chính xác cục bộ không phát hiện dịch sát hoặc nguồn ngoài kho và **không quy đổi được thành phần trămTurnitin**. Không kết luận đạt ngưỡng30%, không upload lên dịch vụ ngoài, không có đánh giáAI-writing.

## Danh sách cần xử lý

CSV đầy đủ (gồm mức chắc chắn,nguyên nhân và khắc phục): {evidence('ISSUES.csv')}.

|ID|Mức|Khu vực|Phát hiện|
|---|---|---|---|
{table}

Các mục informational/thiếu bằng chứng trong CSV không được đếm chung thành lỗi đã xác nhận. Một lỗi được nhiều phòng tìm thấy đã được gộp alias.

## Thứ tự khắc phục đề xuất sau kiểm toán

1. Sửa lịch sử so sánh và test lại trênMongo thật; giữ kiểm ownership/pagination/filter.
2. Đồng nhất model identity trên UI, lưu kích thước thật và sửa mô tả Nano.
3. Sửa các câu/bảng Word được xác nhận sai, giữ kết luận thống kê có điều kiện; không chỉnh số để tạo p<0,05.
4. Sửa hướng dẫn local/BG20 và phân nhãn Markdown/legacyTN/winloss; giữ raw để truy vết.
5. Bổ sung provenance split và mapping tài liệu; lấy báo cáoTurnitin chính thức trước khi kết luận ngưỡng.

Không áp dụng các sửa đổi trên trong cuộc kiểm toán. Không train lại, không sửa checkpoint hoặc dữ liệu nguồn.

## Tính toàn vẹn và giới hạn

Manifest gốc có{integrity['checked']}tệp; kiểm lại thấy{len(integrity['changed_or_missing'])}tệp thay đổi hoặc mất: {evidence('root/source_after_check.json')}. Riêng phòngE kiểm174srcfiles không đổi. Bằng chứng mới nằm trong thư mục kiểm toán; không có nghĩa mọi tệp ngoài manifest đều đã được băm.

Chưa xác minh lại GPU lịch sử, patient-level leakage, test ngoài, đầy đủablation/topology, fullpageWordlayout, mobile runtime, mọi đường admin/load/production hoặc mọi ngưỡng CM từ prediction arrays. Những phần này không được ngầm ghi PASS. Báo cáo này hỗ trợ sửa sai và giới hạn phát biểu; không phải chứng nhận toàn bộ khóa luận đạt hay đã quaTurnitin.
'''
text=re.sub(r'(?<![A-Za-z_])(\d+)(?=(?:seed|rawCSV|CSV|metric|run|ảnh|nhãn|mục|dòng|bảng|checkpoint|best\.pt|model|đoạn|tệp|PDF|test|PNG|CM|PR|image|ô|mask|label|instances|tile|vertex|contour|hình|cặp|pixel|srcfiles))',r'\1 ',text)
for old,new in {'rawCSV':'CSV gốc','sampleSD':'SD mẫu','populationSD':'SD tổng thể','WordP':'Word P','Baseline0':'Baseline 0','TSVM2mask':'TSVM 2 mask','seedFP32':'seed FP32','CI95%':'CI 95%','α0,05':'α = 0,05','ngày25/10':'ngày 25/10','mean333':'mean 333','CPUfloat32':'CPU float32','tensorfloat16':'tensor float16','lưufloat32':'lưu float32','PyTorch2.6':'PyTorch 2.6','batch16':'batch 16','imgsz640':'imgsz 640','workers0':'workers 0','OpenCV4.12':'OpenCV 4.12','numpy2.2':'numpy 2.2','polygon-pairIoU0':'polygon-pair IoU 0','MambaPSA':'MambaPSA'}.items():
    text=text.replace(old,new)
for old,new in {
    'bộ20':'bộ 20','trong36':'trong 36','lineage10/21/20':'lineage 10/21/20','mẫu10':'mẫu 10','cặpGT':'cặp GT',
    '1.240trường':'1.240 trường','PDFTLTK':'PDF TLTK','10công':'10 công','checkpointdtype':'checkpoint dtype',
    'Bảng2.1':'Bảng 2.1','chứa0':'chứa 0','hơn13/20':'hơn 13/20','khoảng38':'khoảng 38','Có16/40':'Có 16/40',
    'kiểm:240':'kiểm: 240','metric10':'metric 10','seedTSVM':'seed TSVM','có44':'có 44','và2.000':'và 2.000',
    '20Baseline':'20 Baseline','20TSVM':'20 TSVM','trong40':'trong 40','.320 tệp':'. 320 tệp','fork8.':'fork 8.',
    'Ngưỡng0,':'Ngưỡng 0,','ngưỡng0,':'ngưỡng 0,','batch4':'batch 4','trênBaseline':'trên Baseline','dùngrect':'dùng rect',
    'lại8':'lại 8','kiểm1.':'kiểm 1.','ảnhtrain':'ảnh train','ảnhval':'ảnh val','160rỗng':'160 rỗng','40rỗng':'40 rỗng',
    'class0':'class 0','nhất3đỉnh':'nhất 3 đỉnh','trong[0,1]':'trong [0,1]','quaSHA256':'qua SHA-256',
    'Tái tạo1.':'Tái tạo 1.','Otsu5':'Otsu 5','loại143':'loại 143','giữ1.':'giữ 1.','range10':'range 10',
    'Cả200':'Cả 200','seed42':'seed 42','Có999':'Có 999','nhãnval':'nhãn val','khoảng3px':'khoảng 3 px',
    'vớiOpenCV':'với OpenCV','PhòngB':'Phòng B','PhòngA':'Phòng A','và8 hình':'và 8 hình','và40':'và 40',
    'có240':'có 240','và80':'và 80','ôTN':'ô TN','.80 PR':'. 80 PR','legendAP50':'legend AP50','đa0,':'đa 0,',
    'và88.':'và 88.','000giá trị':'000 giá trị','bộ97trang':'bộ 97 trang','dùngSD':'dùng SD',
    'seeds0,':'seeds 0,','cùng16':'cùng 16','thành160':'thành 160','đúng20':'đúng 20',
    'gate1+G':'gate 1+G','FFN1×1':'FFN 1×1','tensorworkO':'tensor work O','dụTSVM':'dụ TSVM','câu1.':'câu 1.',
    ';51pytest':'; 51 pytest','và261Java':'và 261 Java','cặpS':'cặp S','lại498':'lại 498','bộtest':'bộ test',
    '24mụcWord':'24 mục Word','23metadata':'23 metadata','split880/120':'split 880/120','Bảng5.8':'Bảng 5.8',
    'APBG20':'AP BG20','trận10 công':'trận 10 công','thayC2PSA':'thay C2PSA','trongYOLO26':'trong YOLO26',
    'ngưỡng30%':'ngưỡng 30%','TSVMFP32':'TSVM FP32','40raw':'40 raw','liên quan;':'liên quan;',
    'không train lại':'không train lại'
}.items():
    text=text.replace(old,new)
(OUT/'AUDIT_REPORT.md').write_text(text,encoding='utf-8')
print(status,counts,'issues',len(issues),'source_changed',len(integrity['changed_or_missing']))
