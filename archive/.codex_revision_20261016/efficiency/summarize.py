from pathlib import Path
import csv,json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=next(p for p in Path(__file__).resolve().parents if (p/'ultralytics').is_dir() and (p/'Ket_Qua_V2').is_dir());O=R/'Ket_Qua_V2/KQ_Nen_DX_20seed_FP32/efficiency_benchmark'
meta=[json.loads((O/'raw'/f'{k}_environment.json').read_text(encoding='utf-8')) for k in ['baseline','tsvm']]
raw=[]
for k in ['baseline','tsvm']:
    raw+=list(csv.DictReader((O/'raw'/f'{k}_timings.csv').open(encoding='utf-8-sig')))
summary=[]
for m in meta:
    for mode in ['forward_only','predict_pipeline']:
        rr=[r for r in raw if r['model']==m['model'] and r['mode']==mode]
        vals=np.array([float(r['latency_ms']) for r in rr])
        assert len(vals)==100 and np.isfinite(vals).all() and (vals>0).all()
        s={'model':m['model'],'mode':mode,'n':len(vals),'mean_ms':vals.mean(),'sd_ms':vals.std(ddof=1),'p50_ms':np.percentile(vals,50),'p95_ms':np.percentile(vals,95),'p99_ms':np.percentile(vals,99),'min_ms':vals.min(),'max_ms':vals.max(),'serial_images_per_second':1000/vals.mean(),'parameters_unfused':m['parameters_unfused'],'params_M':m['parameters_unfused']/1e6,'checkpoint_MiB':m['checkpoint_bytes']/2**20,'fp32_parameter_MiB_unfused':m['fp32_parameter_bytes_unfused']/2**20,'sampled_process_RSS_MiB':m['rss_process_sample_max_bytes']/2**20,'sampled_process_RSS_delta_MiB':m['rss_delta_sample_max_bytes']/2**20,'GFLOPs':'','VRAM_MiB':''}
        if mode=='predict_pipeline':
            for col in ['preprocess_ms','inference_ms','postprocess_ms']:s['mean_'+col]=np.mean([float(r[col]) for r in rr])
            s['mean_unattributed_pipeline_overhead_ms']=s['mean_ms']-sum(s['mean_'+c] for c in ['preprocess_ms','inference_ms','postprocess_ms'])
            s['iterations_with_detections']=sum(int(r['detections'])>0 for r in rr)
        summary.append(s)
def write_csv(path,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
write_csv(O/'tables/efficiency_summary.csv',summary)
write_csv(O/'raw/efficiency_raw_benchmark.csv',raw)
accuracy=list(csv.DictReader((R/'.codex_report_work_20261015/verified_statistics.csv').open()))
ap=next(r for r in accuracy if r['metric']=='mask_map50_95')
combined=[]
for i,m in enumerate(meta):
    s=next(s for s in summary if s['model']==m['model'] and s['mode']=='predict_pipeline').copy()
    pre='baseline' if i==0 else 'tsvm'
    s.update(mask_map50_95_20seed_mean=float(ap[pre+'_mean']),mask_map50_95_20seed_sd=float(ap[pre+'_sd']),accuracy_unit='20 training seeds, epoch selected by maximum mask AP',efficiency_unit='one seed-0 best.pt checkpoint,100 serial timing iterations')
    combined.append(s)
write_csv(O/'tables/accuracy_efficiency_summary.csv',combined)
names=['YOLO26s-seg','TSVM FP32'];colors=['#2878a5','#dd8452'];x=np.arange(2)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':120})
def save(name):
    plt.tight_layout();plt.savefig(O/'figures'/name,dpi=250,bbox_inches='tight');plt.close()
fig,ax=plt.subplots(figsize=(7.2,4.2))
for j,mode in enumerate(['forward_only','predict_pipeline']):
    ss=[s for s in summary if s['mode']==mode];pos=x+(j-.5)*.33
    bars=ax.bar(pos,[s['mean_ms'] for s in ss],.30,yerr=[s['sd_ms'] for s in ss],capsize=4,label=['Forward only','Predict pipeline'][j])
    ax.bar_label(bars,fmt='%.1f',padding=4)
ax.set(xticks=x,xticklabels=names,ylabel='Latency (ms)',title='CPU FP32: mean latency ± SD (100 iterations)');ax.legend();save('fig01_latency_mean.png')
fig,axes=plt.subplots(1,2,figsize=(10,4))
for ax,mode,title in zip(axes,['forward_only','predict_pipeline'],['Forward only','Predict pipeline']):
    vals=[[float(r['latency_ms']) for r in raw if r['model']==m['model'] and r['mode']==mode] for m in meta]
    ax.boxplot(vals,tick_labels=names,showfliers=True);ax.set(title=title,ylabel='Latency (ms)');ax.tick_params(axis='x',labelsize=9)
fig.suptitle('CPU latency distribution; timing repetitions are not training seeds');save('fig02_latency_distribution.png')
fig,ax=plt.subplots(figsize=(7.2,4.2))
for j,col in enumerate(['p50_ms','p95_ms','p99_ms']):
    bars=ax.bar(x+(j-1)*.25,[s[col] for s in combined],.23,label=col.split('_')[0].upper());ax.bar_label(bars,fmt='%.1f',padding=2,fontsize=8)
ax.set(xticks=x,xticklabels=names,ylabel='Latency (ms)',title='Predict pipeline latency percentiles');ax.legend();save('fig03_latency_percentiles.png')
fig,ax=plt.subplots(figsize=(7.2,4.2));bottom=np.zeros(2)
for col,label in [('mean_preprocess_ms','Preprocess'),('mean_inference_ms','Forward'),('mean_postprocess_ms','Postprocess'),('mean_unattributed_pipeline_overhead_ms','Other pipeline overhead')]:
    vals=np.array([s[col] for s in combined]);ax.bar(x,vals,bottom=bottom,label=label);bottom+=vals
ax.set(xticks=x,xticklabels=names,ylabel='Mean latency (ms)',title='Measured Ultralytics pipeline stages');ax.legend(fontsize=8,loc='upper left');save('fig04_pipeline_stages.png')
fig,axes=plt.subplots(1,2,figsize=(9,4))
for ax,col,title,unit in [(axes[0],'params_M','Architecture parameters','Million'),(axes[1],'fp32_parameter_MiB_unfused','FP32 parameter storage','MiB')]:
    bars=ax.bar(names,[s[col] for s in combined],color=colors);ax.bar_label(bars,fmt='%.2f',padding=3);ax.set(title=title,ylabel=unit);ax.set_ylim(0,max(s[col] for s in combined)*1.2)
save('fig05_parameters_fp32_memory.png')
fig,ax=plt.subplots(figsize=(7.2,4.2))
for j,col,label in [(0,'checkpoint_MiB','Checkpoint file'),(1,'fp32_parameter_MiB_unfused','FP32 parameters')]:
    bars=ax.bar(x+(j-.5)*.33,[s[col] for s in combined],.30,label=label);ax.bar_label(bars,fmt='%.2f',padding=3)
ax.set(xticks=x,xticklabels=names,ylabel='MiB (2^20 bytes)',title='Disk checkpoint size and FP32 parameter memory');ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.13),ncol=2);save('fig06_checkpoint_vs_parameter_bytes.png')
fig,ax=plt.subplots(figsize=(7.2,4.4))
for i,s in enumerate(combined):
    ax.errorbar(s['mean_ms'],s['mask_map50_95_20seed_mean'],yerr=s['mask_map50_95_20seed_sd'],fmt='o',color=colors[i],capsize=5,label=names[i],markersize=8)
ax.set(xlabel='Seed-0 predict pipeline mean latency (ms)',ylabel='Mask mAP50–95 (20-seed mean ± SD)',title='Accuracy and CPU cost use different observation units');ax.legend();save('fig07_accuracy_latency_tradeoff.png')
fig,ax=plt.subplots(figsize=(7.2,4.2))
bars=ax.bar(names,[s['serial_images_per_second'] for s in combined],color=colors);ax.bar_label(bars,fmt='%.2f',padding=3)
ax.set(ylabel='Serial images/s = 1000 / mean latency',title='Predict pipeline serial throughput (CPU, batch 1)');ax.set_ylim(0,max(s['serial_images_per_second'] for s in combined)*1.2);save('fig08_serial_throughput.png')
fwd=[s for s in summary if s['mode']=='forward_only'];pipeline=combined
lines=['# Benchmark thực đo: YOLO26s-seg và TSVM FP32','',f"Thiết bị: {meta[0]['cpu_name']}; {meta[0]['physical_cpus']} lõi/{meta[0]['logical_cpus']} luồng logic; RAM {meta[0]['system_ram_bytes']/2**30:.2f} GiB. Windows; Python {meta[0]['python'].split()[0]}, PyTorch {meta[0]['torch']}, Ultralytics {meta[0]['ultralytics']}. CUDA khả dụng: {meta[0]['cuda_available']}.",'','## Giao thức và ranh giới đo','', '- Hai checkpoint seed 0 đúng cặp thực nghiệm 20 seed; SHA-256 và đường dẫn trong raw/*_environment.json. Không sử dụng checkpoint TSVM cũ không có FP32.','- CPU, float32, autocast tắt, 4 intra-op threads, 1 inter-op thread; batch 1, đầu vào chính xác 1×3×640×640; rect=False; conf=0.25, IoU=0.7, max_det=300. Trạng thái float32 và hữu hạn được kiểm tra trước đo.','- Mỗi mô hình chạy trong tiến trình Python riêng; baseline trước, TSVM sau. Mỗi chế độ 20 lượt warmup và 100 lượt đo bằng perf_counter_ns; torch.inference_mode; nhật ký không in trong vòng đo.','- Forward only: tensor float32 đã letterbox/chuẩn hóa từ ảnh polyp đầu tiên, tái sử dụng cùng tensor cho 100 lượt; chỉ model.forward, không gồm tiền/hậu xử lý. Đo sau khởi tạo predictor và Conv-BN fusion chuẩn.','- Predict pipeline: 20 ảnh validation cố định (10 polyp + 10 background theo tên sắp xếp), giải mã PIL RGB trước đo; lặp 5 chu kỳ. Bao gồm chuyển ảnh/letterbox/normalize, forward và hậu xử lý segmentation thật của Ultralytics. Không gồm đọc file, giải mã JPEG, HTTP, hàng đợi web, overlay, base64 hoặc trình duyệt.','- Các cột preprocess/inference/postprocess lấy từ result.speed thực tế, chỉ để mô tả thành phần. Chênh lệch với đồng hồ bao ngoài là chi phí pipeline còn lại; không gán tỷ lệ giả định cho backbone/head.','- Số tham số kiến trúc và bộ nhớ tham số float32 được đếm trước fusion. RSS là cực đại trong các mẫu RSS lấy ngoài vùng bấm giờ, không phải peak allocator hoặc riêng bộ nhớ mô hình. Hai quá trình nạp độc lập giúp hạn chế nhiễm từ mô hình trước nhưng cache/OS vẫn tác động.','', '## Kết quả','', '| Mô hình | Chế độ | Mean ± SD (ms) | P50 | P95 | P99 | ảnh/s nối tiếp |','|---|---|---:|---:|---:|---:|---:|']
for s in summary:lines.append(f"| {s['model']} | {s['mode']} | {s['mean_ms']:.2f} ± {s['sd_ms']:.2f} | {s['p50_ms']:.2f} | {s['p95_ms']:.2f} | {s['p99_ms']:.2f} | {s['serial_images_per_second']:.2f} |")
lines+=['','| Mô hình | Tham số (M) | File checkpoint (MiB) | Tham số FP32 (MiB) | RSS sampled (MiB) |','|---|---:|---:|---:|---:|']
for s in combined:lines.append(f"| {s['model']} | {s['params_M']:.6f} | {s['checkpoint_MiB']:.2f} | {s['fp32_parameter_MiB_unfused']:.2f} | {s['sampled_process_RSS_MiB']:.2f} |")
lines+=['','## Diễn giải và giới hạn','',f"- TSVM tăng tham số {(combined[1]['params_M']/combined[0]['params_M']-1)*100:.2f}%; latency forward gấp {fwd[1]['mean_ms']/fwd[0]['mean_ms']:.2f} lần, pipeline gấp {combined[1]['mean_ms']/combined[0]['mean_ms']:.2f} lần trong lần đo CPU này.",'- File baseline lưu tensor huấn luyện dạng FP16, nhưng cả hai mô hình đã được chuyển sang FP32 khi suy luận. Do đó không suy ra lượng RAM float32 chỉ từ dung lượng file best.pt. Các tensor FP16 gốc không có nghĩa benchmark dùng FP16.','- Không báo GFLOPs tổng vì chưa có quy tắc đếm được kiểm chứng cho custom parallel selective scan; số THOP chỉ đếm Conv/Linear sẽ thiếu phép toán. Không sao chép GFLOPs của TSVM cũ. VRAM: không áp dụng trong phiên CPU, không phải 0 MiB GPU.','- Đây là đo triển khai trên một máy, một seed, một thứ tự chạy; 100 lượt timing không phải 100 seed hoặc 100 mẫu độc lập để kiểm định ưu thế mô hình. OS, điện năng/nhiệt, nền Python và tác vụ khác có thể làm thay đổi độ trễ. Không suy rộng sang GPU hoặc hệ thống nội soi thời gian thực.','- Cột độ chính xác trong accuracy_efficiency_summary.csv dùng mean ± SD của 20 seed tại epoch cực đại mask AP, còn benchmark dùng seed-0 best.pt được chọn bởi box+mask fitness. Hai đại lượng giúp thảo luận đánh đổi tổng quát; không khẳng định AP cụ thể của checkpoint đo tốc độ hay Pareto có ý nghĩa thống kê.','- Không huấn luyện, không chỉnh checkpoint, không dùng ảnh validation để tối ưu tham số. Giải mã và các kiểm tra tensor/RSS nằm ngoài ranh giới bấm giờ.','', '## Tái lập','', 'Chạy hai tiến trình measure.py baseline và measure.py tsvm bằng venv ai-service, lần lượt; sau đó chạy summarize.py bằng bundled Python với numpy/matplotlib. Bản sao scripts nằm trong scripts/. Kiểm tra hash môi trường trước khi so sánh lại. Mọi mốc thời gian gốc được lưu trong raw/.']
lines=[line.replace('Conv-BN fusion chuẩn.', 'fusion chuẩn của Ultralytics (gộp Conv-BN và loại nhánh one2many khỏi đầu end-to-end).') for line in lines]
lines.insert(lines.index('## Diễn giải và giới hạn')+2,'- Không lấy hiệu mean của hai chế độ forward_only và predict_pipeline để suy ra chi phí tiền/hậu xử lý: forward dùng một tensor lặp lại, pipeline dùng 20 ảnh và chạy ở pha sau. Mean pipeline của TSVM nhỏ hơn forward khoảng 9.50 ms trong lần đo này do dữ liệu/cache/dao động thời gian; các thành phần pipeline phải đọc từ result.speed thực đo trong cùng lượt.')
lines=[line.replace('trong lần đo này do dữ liệu/cache/dao động thời gian', 'trong lần đo này; khác biệt có thể liên quan tới dữ liệu/cache/dao động thời gian').replace('sau đó chạy summarize.py bằng bundled Python', 'chạy verify_checkpoints.py bằng cùng venv để kiểm tra dtype lưu trữ, sau đó chạy summarize.py bằng bundled Python') for line in lines]
(O/'reports/benchmark_report.md').write_text('\n'.join(lines),encoding='utf-8')
audit={'raw_rows':len(raw),'groups':len(summary),'rows_per_group':100,'checkpoints_sha256_verified':all(hashlib.sha256(Path(m['checkpoint']).read_bytes()).hexdigest()==m['sha256'].lower() for m in meta),'matching_inputs':meta[0]['inputs']==meta[1]['inputs'],'matching_protocol':all(meta[0][k]==meta[1][k] for k in ['precision','device','threads','interop_threads','warmups_per_mode','measured_iterations_per_mode','batch','tensor_shape','rect','conf','iou','max_det']),'real_pipeline_detections':[s['iterations_with_detections'] for s in combined],'all_timings_finite_positive':True,'GFLOPs':'unavailable, unsupported custom scan counting','VRAM':'not applicable, CPU runtime','script_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')}}
assert audit['checkpoints_sha256_verified'] and audit['matching_inputs'] and audit['matching_protocol']
(O/'reports/benchmark_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
(O/'reports/benchmark_audit.md').write_text('# Kiểm tra benchmark\n\n'+f"- {len(raw)} dòng timing thật; 4 nhóm ×100, không NaN/vô hạn/độ trễ âm.\n- SHA-256 checkpoint khớp metadata.\n- Danh sách ảnh/hash và giao thức của hai mô hình trùng nhau.\n- Có kết quả hộp/mặt nạ hữu hạn từ pipeline thật.\n- Không tái dùng timing hoặc GFLOPs từ bộ 10 seed.\n- Đếm detection không dùng để suy ra AP/độ chính xác trên tập dữ liệu.\n- raw/*_environment.json có phiên bản, CPU, precision và RSS.\n",encoding='utf-8')
import shutil
(O/'scripts').mkdir(exist_ok=True)
for p in Path(__file__).parent.glob('*.py'):shutil.copy2(p,O/'scripts'/p.name)
(O/'README.md').write_text('# Efficiency benchmark FP32 riêng\n\nBắt đầu tại [báo cáo phương pháp và kết quả](reports/benchmark_report.md). raw/ chứa 400 lượt đo thực và môi trường; tables/ chứa bảng tổng hợp; figures/ có 8 biểu đồ; scripts/ có mã tái lập. Chỉ so sánh YOLO26s-seg và TSVM FP32 seed0.\n',encoding='utf-8')
print(json.dumps({'summary':summary,'audit':audit},ensure_ascii=False,indent=2))
