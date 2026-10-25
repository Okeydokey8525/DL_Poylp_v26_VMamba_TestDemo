from pathlib import Path
import re
O=Path(__file__).parent;c=(O/'report_content.md').read_text(encoding='utf-8')
c=re.sub(r'Hình 5\.(\d+)',lambda m:'Hình 5.'+str(int(m[1])+2) if int(m[1])>=14 else m[0],c)
new='''Các tệp results.csv của YOLO26 ghi val/seg_loss, val/box_loss, val/cls_loss, val/l1_loss và val/sem_loss. Chúng không có cột val/dfl_loss như một số biến thể YOLO trước. Giá trị val/sem_loss bằng 0 trên các lượt đã lưu được giữ đúng trong dữ liệu và đánh dấu không áp dụng cho kiểm định chênh lệch; không diễn giải số 0 đó như chất lượng phân đoạn hoàn hảo. Phân tích tập trung vào các thành phần đang có giá trị biến thiên thực tế.
@FIG pkg:05_charts/convergence/25_val_losses_mean_sd_epoch11_100|Hình 5.14 Các validation loss có biến thiên trong giai đoạn epoch 11 đến 100
Phóng lớn giai đoạn từ epoch 11 giúp quan sát xu hướng về cuối mà không bị các giá trị lớn ban đầu chi phối trục tung. Cả hai nhóm tiếp tục giảm các thành phần loss chính; các đường trung bình gần nhau và vùng SD giao nhau trên nhiều đoạn. Việc cắt bỏ 10 epoch đầu chỉ là cách biểu diễn bổ sung, không loại các epoch đó khỏi dữ liệu hoặc thay đổi quy tắc chọn mô hình.
@FIG pkg:05_charts/convergence/26_train_losses_mean_sd|Hình 5.15 Các thành phần train loss qua 100 epoch
Train loss và validation loss được tính trong những điều kiện đầu vào khác nhau: tập train có tăng cường dữ liệu, còn validation không dùng cùng phân bố tăng cường. Do đó, không lấy hai đường làm một thước đo hoàn toàn đồng nhất. Sự thay đổi train loss gần giai đoạn cuối phù hợp với thời điểm cấu hình tắt Mosaic, nhưng quan sát này không tách riêng tác động nhân quả của Mosaic khỏi các yếu tố tối ưu khác. Đánh giá overfitting cần xem đồng thời xu hướng hai tập và chất lượng dự đoán, thay vì chỉ dựa vào loss train thấp.
'''
c=c.replace('## 5.7 Ma trận nhầm lẫn và các sai số phát hiện',new+'\n## 5.7 Ma trận nhầm lẫn và các sai số phát hiện')
(O/'report_content.md').write_text(c,encoding='utf-8')
print('Added actual YOLO26 L1/semantic loss discussion and training/late-validation figures.')
