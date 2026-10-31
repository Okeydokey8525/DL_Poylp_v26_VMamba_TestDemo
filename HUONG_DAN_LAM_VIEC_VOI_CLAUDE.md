# Hướng dẫn làm việc với Claude (bàn giao cho claude.ai)

Cập nhật 29/10/2026. Người dùng: **Lê Đức Lương** (sinh viên CNTT, HUIT; GitHub `Okeydokey8525`).

File này có ba mục đích:
1. Để Claude ở nơi khác (claude.ai, Claude Code phiên mới) hiểu **cách làm việc** của người dùng.
2. Làm nguồn để tạo **kỹ năng (skill)** và cập nhật **bộ nhớ (memory)** trên claude.ai.
3. Ghi lại **những việc đã làm** trong khóa luận, cùng trạng thái hiện tại.

Cách dùng trên claude.ai:
- Phần A và B: tạo hoặc cập nhật skill (mỗi khối ở mục B là một skill).
- Phần C: dán vào bộ nhớ hoặc phần hướng dẫn của Project.
- Phần D và E: tải lên làm tài liệu của Project khóa luận.

---

## A. Cách làm việc của người dùng (áp dụng lâu dài, mọi dự án)

### A1. Giao tiếp
- Luôn trả lời bằng **tiếng Việt**: rõ ràng, đi thẳng vào việc, câu ngắn.
- Người dùng thường nhắn bằng giọng nói chuyển thành chữ, nên có thể sai chính tả hoặc sai từ. Hãy đoán theo ngữ cảnh. Ví dụ: "study" là ablation study; "tempo" là template; "ghép word" là ghép file Word.
- Khi người dùng hỏi "là sao?", hãy giải thích bằng ví dụ cụ thể, không dùng thuật ngữ trừu tượng.
- Cuối mỗi đợt việc, tóm tắt **đã làm gì, còn gì, bước tiếp theo**.

### A2. Quy trình "lên kế hoạch trước, làm sau"
Với mọi việc lớn, làm theo bốn bước:
1. Rà soát và trình bày **kế hoạch chi tiết**.
2. Hỏi lại những điểm còn mơ hồ.
3. Chờ người dùng **xác nhận rõ ràng**, ví dụ "ok làm đi", "triển khai", "lưu đi".
4. Thực hiện, rồi báo cáo kết quả.

Một số câu cần hiểu đúng:
- "Chưa chỉnh gì", "đang hỏi đáp", "đang thảo luận", "chưa triển khai" nghĩa là **chỉ bàn**. Không sửa, tạo hay di chuyển file, và không gợi ý nút kiểu "làm luôn".
- Việc làm hàng loạt (nhiều slide, nhiều chương, nhiều hình): **làm mẫu 1–3 cái trước**, người dùng duyệt xong mới làm phần còn lại theo từng đợt.
- Thay đổi trên dịch vụ bên ngoài (Canva, Google Drive, Kaggle…): **cho xem trước, được duyệt mới lưu**.

### A3. Trung thực với số liệu
- **Không bịa số liệu.** Mọi con số phải truy được về file CSV hoặc script sinh ra nó. Chưa có bằng chứng thì ghi "chưa xác minh" hoặc để ô **[CHỜ KẾT QUẢ]**.
- Kết quả không có ý nghĩa thống kê thì viết "xu hướng", **không** viết "vượt trội" hay "cải thiện rõ rệt".
- Nêu rõ cả mặt kém. Ví dụ: TSVM chậm hơn, kém hơn trên một số bộ dữ liệu ngoài.
- Khi hai lần đo lệch nhau, ghi cả hai lần. Nói rõ nguyên nhân chưa xác minh, không chọn lần đo đẹp hơn.
- Kiểm tra chéo nhận định của người khác (bạn cùng nhóm, GPT, Gemini…) bằng bằng chứng gốc trước khi sửa. Ví dụ: bạn cùng nhóm cho rằng nhóm tự chia tập dữ liệu. Kiểm tra md5 cho thấy tập chia là do tác giả bộ dữ liệu cung cấp.

### A4. An toàn và quyền
- **Git:** chỉ commit khi được đồng ý. Không push nếu chưa được yêu cầu. Nhánh làm việc của khóa luận là `Okeydokey`.
- **Bí mật:**
  - Không đọc, nhắc lại hay commit token, mật khẩu, tài khoản test.
  - Không đọc `Ung_Dung/polypweb/GhiChu.txt` (file này chứa tài khoản test).
  - Kaggle token do người dùng tự đặt vào `~/.kaggle/`.
- **Tải tệp** về máy: phải hỏi trước.
- Mỗi lần `kaggle kernels push`: phải hỏi trước.
- Không sửa dữ liệu gốc, checkpoint hay hiện vật kiểm toán. Di chuyển thư mục thì ghi vào `PATH_MAP`.
- File đề cương PDF của trường không đưa vào git.

### A5. Phong cách sản phẩm
- **Báo cáo**:
  - Mỗi chương một file markdown, sau đó ghép vào Word theo biểu mẫu của trường.
  - Viết mới để Turnitin trùng lặp dưới 30%.
  - Trích dẫn theo kiểu **IEEE**, đánh số theo thứ tự xuất hiện lần đầu.
  - Dùng **dấu phẩy thập phân** (0,7189) và dấu chấm phân cách hàng nghìn (1.040).
- **Hình**:
  - Phông mặc định của matplotlib.
  - Màu Okabe–Ito: đối chứng `#0072B2`, TSVM `#D55E00`, PraNet `#009E73`, U-Net `#CC79A7`.
  - Mỗi hình một biểu đồ, tối đa hai. Không dùng biểu đồ tròn hay rada, không xếp lưới 2×2.
  - Điểm từng seed vẽ thành hình riêng.
  - Thanh lỗi là ±1 SD.
  - Xuất PNG 300 dpi kèm PDF, có bản `vi/` và `en/`.
- **Slide**:
  - Phần kết quả: mỗi slide **một hình**, gần như không có chữ; lời nói đặt ở ghi chú.
  - Phần lý thuyết và dữ liệu: bố cục so le hình–chữ (zigzag) hoặc chỉ một hình.
  - Dùng mẫu (template) của trường.

### A6. Môi trường máy
- Windows 11, PowerShell và Git Bash. Laptop có GPU RTX 5050; tản nhiệt kém khi không có quạt, nên độ trễ đo được dao động.
- Python có GPU nằm ở `C:\venv_kl_gpu\Scripts\python.exe`. Đường dẫn được đặt ngắn vì Windows giới hạn 260 ký tự.
- Huấn luyện mô hình trên **Kaggle** (notebook). Máy cá nhân chỉ dùng để đánh giá, vẽ hình và đo hiệu năng.
- Công cụ người dùng hay dùng: Claude Code (desktop), claude.ai, Canva, Word, Kaggle, GitHub. Đôi khi dán kết quả từ GPT, Gemini, NotebookLM hoặc Antigravity để Claude kiểm chứng.
- Dự án khác ngoài khóa luận:
  - web/app Spring Boot, Next.js, FastAPI, Flutter;
  - PHP CodeIgniter cho `huyhoangmobile.vn` và `yeucodo.vn`.

---

## B. Bộ kỹ năng (skill) đề xuất

Mỗi khối dưới đây có thể dán thành một skill. Một số skill đã có trên claude.ai với tên tương tự (`thesis-polyp-report`, `ai-output-review`, `code-milestone-workflow`). Khi đó dùng nội dung bên dưới để **cập nhật** skill đó.

### B1. `thesis-polyp-report`: viết và rà soát khóa luận
**Dùng khi:** viết chương, rà số liệu, bảng, thống kê, trích dẫn, hình của khóa luận YOLO26-seg + VMamba.

1. Đọc `NGU_CANH_DU_AN.md` và `CLAUDE.md`. Số liệu lấy từ `00_tai_lieu_tong_quan/bang/*.csv`.
2. Bộ số chốt là **20 seed (0–19)**. Endpoint chính là mask mAP50–95 tại epoch cực đại. Dùng số ở mục D2.
3. Mỗi con số đưa vào chương phải ghi nguồn CSV. Ghi số đó vào `00_tai_lieu_tong_quan/12_TRUY_VET_SO_LIEU.md`.
4. Không suy diễn:
   - TN = 40 − FP;
   - Dice hay IoU từ mAP;
   - lợi ích topology (chỉ dùng số đã đo).
5. Văn phong: không viết "vượt trội". Chỉ endpoint chính được kết luận chắc chắn vì không hiệu chỉnh so sánh bội; các chỉ số phụ chỉ mang tính thăm dò.
6. Trích dẫn IEEE. Khi thêm tài liệu mới, đánh số lại theo thứ tự xuất hiện. Cập nhật `08_TAI_LIEU_THAM_KHAO.md` và bảng đối số `_KIEM_TRA/F_bang_doi_so_tai_lieu.csv`.
7. Viết xong chương thì cho một lượt phản biện kiểm tra số liệu và trích dẫn, ghi vào `_KIEM_TRA/`.
8. Đối chiếu với thang điểm (mục C, bộ nhớ "Đề cương và thang điểm") để không thiếu mục nào.

### B2. `stat-paired-seeds`: so sánh hai mô hình qua nhiều seed
**Dùng khi:** so sánh hai mô hình huấn luyện với cùng tập seed.

- Dùng kiểm định ghép cặp theo seed:
  - paired t-test, kèm Wilcoxon signed-rank;
  - khoảng tin cậy 95% của Δ;
  - Cohen's d_z;
  - số seed thắng / tổng số seed.
- Độ ổn định: Levene theo trung vị (Brown–Forsythe), ghi là kết quả thăm dò.
- Chọn **một endpoint chính** từ trước. Các chỉ số còn lại là phụ, không hiệu chỉnh so sánh bội nên chỉ mang tính tham khảo.
- Báo cáo đủ trung bình ± SD (ddof = 1), Δ, CI, p của cả hai kiểm định.
- Không chọn tập seed con cho đẹp số.

### B3. `gpu-latency-benchmark`: đo hiệu năng trung thực
**Dùng khi:** đo độ trễ hoặc FLOPs trên laptop.

- Cấu hình đo:
  - chỉ tính forward, batch 1, FP32, `cudnn.benchmark = False`;
  - khởi động 50 lần, đo 200 lần bằng CUDA event;
  - **5 vòng xen kẽ, đổi thứ tự mô hình mỗi vòng**.
- Trước mỗi khối đo, chờ GPU nguội dưới 55 °C. Ghi nhiệt độ và xung nhịp SM bằng `nvidia-smi`.
- Báo cáo các thống kê: trung vị, min, p10, tỉ lệ theo từng vòng. Ưu tiên **tỉ lệ giữa hai mô hình** hơn số ms tuyệt đối.
- Giữ kết quả các lần đo cũ (hậu tố `_lan1`). Ghi lệch giữa các phiên đo là "nguyên nhân chưa xác minh".
- Script mẫu: `00_tai_lieu_tong_quan/scripts/do_flops_gpu.py`.

### B4. `canva-slide-builder`: làm slide bảo vệ trên Canva
**Dùng khi:** chỉnh sửa thiết kế Canva qua MCP.

1. Mở bằng `resolve-shortlink`, sau đó `read-design` với `open_transaction`.
2. Sửa bằng `edit-design`, giữ giao dịch mở (keep_open). Gửi ảnh xem trước cho người dùng. **Chỉ commit sau khi được duyệt**; không duyệt thì cancel.
3. Lưu ý về công cụ:
   - Làm được: sửa chữ, định dạng, di chuyển, đổi kích thước, thêm chữ, thêm trang, đổi thứ tự trang, tải ảnh lên, ghi chú lời nói.
   - **Không làm được**: xóa trang, nhân bản trang. Người dùng tự làm hai việc này.
4. Chữ thêm mới mặc định cỡ 16px, cần đặt lại cỡ chữ. Ô tiêu đề có thể tự giãn hết chiều ngang, cần chỉnh lại.
5. Ảnh thu nhỏ trả về có thể là bản cũ trong bộ nhớ đệm. Xác minh bằng nội dung đọc lại, không dựa vào ảnh thu nhỏ.
6. Nếu người dùng không thấy thay đổi, có thể giao dịch chưa commit, hoặc trình duyệt cần tải lại (F5).
7. Làm theo đợt 5–8 slide. Kế hoạch slide nằm ở `06_bao_cao/slide/KE_HOACH_SLIDE.md`.

### B5. `ai-output-review`: kiểm chứng đầu ra của AI khác
**Dùng khi:** người dùng dán câu trả lời hoặc code từ GPT, Gemini, NotebookLM hay Antigravity, hoặc cần viết prompt giao việc cho Antigravity.

- Đối chiếu từng khẳng định với file hoặc số liệu gốc.
- Đánh dấu ✅ đúng / ❌ sai / ⚠️ chưa đủ bằng chứng, kèm đường dẫn bằng chứng.
- Khi viết prompt giao việc, nêu rõ: phạm vi file, quy tắc không bịa số, tiêu chí hoàn thành.

### B6. `code-milestone-workflow`: sửa code dự án web/app
**Dùng khi:** sửa các dự án Spring Boot, Next.js, FastAPI, Flutter, PHP CodeIgniter.

- Chia việc thành milestone. Hết mỗi milestone thì chạy hoặc kiểm tra, rồi báo **PASS/FAIL** kèm bằng chứng.
- Không đụng tới file chứa tài khoản hay bí mật. Không push khi chưa được phép.

---

## C. Bộ nhớ đề xuất (dán vào memory hoặc hướng dẫn của Project)

1. **Ngôn ngữ và phong cách:** tiếng Việt, ngắn gọn. Người dùng nhắn bằng giọng nói nên có thể sai chính tả; hiểu theo ngữ cảnh.
2. **Lên kế hoạch trước:** "chưa chỉnh gì / đang hỏi đáp" nghĩa là chỉ bàn. Việc lớn phải có kế hoạch, được duyệt, mới làm. Việc hàng loạt thì làm mẫu trước.
3. **Không bịa số liệu.** Không viết "vượt trội" khi p ≥ 0,05. Số liệu phải truy được về CSV.
4. **Git:** commit lên `Okeydokey` khi được đồng ý. Không push nếu chưa được yêu cầu.
5. **Bí mật:** không đọc hay đưa `GhiChu.txt` hoặc token vào git hay báo cáo. Tải tệp và `kaggle kernels push` phải hỏi trước.
6. **Khóa luận:**
   - HUIT CNTT_KLCN182, GVHD Phùng Thế Bảo.
   - Nhóm: Lê Đức Lương (2001230490), Phùng Tuấn Huy (2001230312), Trần Mạnh Toàn (2001230830).
   - Hạn nộp 08/11/2026.
   - Đề tài: tích hợp VMamba vào YOLO26-seg, phân đoạn polyp.
7. **Phạm vi khóa luận:**
   - So sánh Baseline YOLO26s-seg với TSVM FP32 (C2TSVMamba ở tầng 10), 20 seed.
   - PraNet và U-Net chỉ để so sánh.
   - AV, AVF, ITSVM là thử nghiệm, không đưa vào báo cáo.
8. **Dữ liệu:**
   - Kvasir-SEG lấy từ Kaggle (debeshjha1).
   - Tập chia 880/120 là **do tác giả bộ dữ liệu cung cấp** (đã kiểm md5).
   - BG20 bổ sung ảnh nền normal-cecum: train 1.040 ảnh, val 160 ảnh; không có tập test.
9. **Thang điểm bắt buộc có:**
   - độ đo Dice, IoU, P, R, F1, mAP50, mAP50–95, tốc độ suy luận, số tham số, FLOPs;
   - ablation;
   - triển khai trên dữ liệu thực tế;
   - lập kế hoạch và phân công;
   - ưu và nhược điểm của YOLO26-seg và VMamba, có ví dụ minh họa;
   - ứng dụng có so sánh hai mô hình.
10. **Chương 4** (dữ liệu) là bài của bạn cùng nhóm (bản v3). Chỉ đổi số mục và sửa lỗi sự thật, có ghi chú cho người biên tập.

---

## D. Những việc đã làm cùng nhau

### D1. Mốc thời gian

| Thời gian | Việc chính |
|---|---|
| 22–26/07 | Tích hợp VMamba vào YOLO26-seg, tạo tiện ích chuyển trọng số, lập 12 báo cáo kiểm toán baseline và tài liệu ban đầu. |
| 08–09 | Huấn luyện trên Kaggle. Thử nhiều biến thể (AV, AVF, ITSVM, TSVM). Chốt TSVM. |
| 29–30/09 | Sửa pipeline kết quả 10 seed: bỏ số viết cứng, sinh mọi số từ `results.csv`. Dọn các dataset không liên quan, chỉ giữ Baseline và TSVM. Viết báo cáo 10 seed đã kiểm toán. |
| 12/10 | Phát hiện **lỗi lưu checkpoint FP16 làm tràn BatchNorm tầng 10**. Vá fork để lưu float32. |
| 13/10 | Có kết quả 20 seed TSVM FP32. Viết báo cáo 20 seed, ma trận nhầm lẫn trung bình 20 seed. |
| 26/10 | Thêm notebook huấn luyện PraNet và U-Net (20 seed mỗi mô hình). |
| 25–26/10 | Kiểm toán toàn bộ (`07_kiem_toan_va_sua/`). Sắp xếp lại cây thư mục thành `00_…07_`, `99_luu_tru/`, kèm `PATH_MAP`. Viết `00_tai_lieu_tong_quan/`: 14 file md và `tinh_lai_so_lieu.py` tính lại mọi con số từ dữ liệu gốc. Xác minh 40 `results.csv` khớp 100%. |
| 26/10 | Vẽ lại toàn bộ hình theo quy cách mới (4 hình mẫu được duyệt trước). Đánh giá theo pixel 4 mô hình × 20 seed. |
| 27/10 | Điều tra bằng 4 sub-agent (dữ liệu, lý thuyết, ứng dụng, tài liệu tham khảo). Viết chương markdown. Xác minh nguồn tập chia dữ liệu (của tác giả). Đặt tạm báo cáo theo 10 seed. |
| 28/10 | **Chốt 20 seed**, dấu phẩy thập phân. Sửa Ch.4 từ 640 thành 672 cho khung validation. Thêm chỉ số topology (lỗi Betti), FLOPs và độ trễ GPU, dữ liệu ngoài (ClinicDB, ColonDB, ETIS, PolypGen). Thêm thiết kế ablation. |
| 28/10 | **Viết Chương 6** đầy đủ (mục ablation để trống). Chuyển Ch.4 sang bản v3 rút gọn. **Đánh số lại 76 tài liệu tham khảo** theo IEEE. |
| 28/10 | **Đo lại độ trễ GPU** có kiểm soát nhiệt độ (lần 2). Cập nhật `09_HIEU_NANG_TINH_TOAN.md` và Chương 6. |
| 28/10 | Lập kế hoạch slide bảo vệ (khoảng 62 slide). **Làm và lưu 3 slide mẫu trên Canva**: bìa, nội dung trình bày, lý do chọn đề tài, kèm ghi chú lời nói. |
| 29/10 | Ablation đủ 15 lượt, tính bảng 17/18, vẽ k01/k02, điền mục 6.6. Viết Kết luận, Phụ lục, trang đầu. Đối chiếu thang điểm. Mục 1.6 trong nước. |
| 30/10 | Đối chiếu PDF trong `TLTK/`, đối chứng 6 bài thu phí qua tóm tắt. **Ghép Word theo Biểu mẫu V3** bằng `06_bao_cao/ghep_word/ghep_word.py` (pandoc + docxcompose + Word). **Rút gọn tài liệu tham khảo 80 → 57**, có subagent kiểm tra chéo trước và sau khi sửa. |
| 31/10 | **Tách hai bản báo cáo:** bản đầy đủ 147 trang (tag `ban_day_du_147`) và bản rút gọn `md_bao_cao_rut_gon/` (thân 70 trang, 109 trang cả quyển, Phụ lục E–H). Làm mẫu Mở đầu, Ch.1, Kết luận cho chủ dự án duyệt trước, rồi nén Ch.2–6; script kiểm đánh số, tham chiếu, trích dẫn và số liệu; subagent phản biện. Sửa ở bản đầy đủ: mục 3.9–3.10 (ablation đã chạy), cú pháp 5 hình Ch.4. |

Các commit gần nhất trên `Okeydokey` (chưa push):
- `17691da4`: chốt 20 seed.
- `20c595dc`: topology, FLOPs, dữ liệu ngoài.
- `32355bfd`: Chương 6, Ch.4 v3, đánh số lại tài liệu tham khảo.
- `2bd9bf2d`: đo lại độ trễ GPU.

### D2. Kết quả chính đã xác minh (20 seed, dùng trong báo cáo)

**Endpoint chính, mask mAP50–95 (Baseline so với TSVM):**

| Chỉ số | Giá trị |
|---|---|
| Baseline | 0,7189 ± 0,0118 |
| TSVM | 0,7232 ± 0,0072 |
| Δ | +0,0043 |
| CI 95% | [−0,0002; 0,0088] |
| p (paired t) | 0,061 |
| p (Wilcoxon) | 0,070 |
| Số seed TSVM cao hơn | 13/20 |
| d_z | 0,44 |

Kết luận: chưa có ý nghĩa thống kê, chỉ là xu hướng.

**Các kết quả khác:**
- **Độ ổn định:** SD của TSVM nhỏ hơn; Levene (Brown–Forsythe) p = 0,026, chỉ mang tính thăm dò.
- **Mask F1:** 0,8806 so với 0,8856; p = 0,259; 12/20 seed.
- **Chi phí tính toán:**
  - Tham số: 11.434.463 so với 12.254.688 (+7,17%).
  - Riêng tầng 10: 990.976 (C2PSA) so với 1.811.201 (C2TSVMamba).
  - Độ trễ CPU: 269,6 ms so với 577,4 ms (khoảng 2,1 lần).
  - Độ trễ GPU: TSVM chậm hơn khoảng 1,5–1,7 lần (lần 2: trung vị 26,33 ms so với 39,86 ms). Số ms tuyệt đối lệch giữa các phiên đo.

**Dữ liệu ngoài, Dice (Baseline / TSVM / PraNet / U-Net):**

| Bộ dữ liệu | Baseline | TSVM | PraNet | U-Net | Ghi chú |
|---|---:|---:|---:|---:|---|
| ClinicDB | 0,786 | 0,770 | 0,752 | 0,525 | TSVM kém hơn, p = 0,006 |
| ColonDB | 0,631 | 0,601 | 0,539 | 0,375 | TSVM kém hơn, p < 0,001 |
| ETIS | 0,535 | 0,529 | 0,466 | 0,284 | không khác biệt có ý nghĩa |
| PolypGen | 0,719 | 0,715 | 0,683 | 0,484 | không khác biệt có ý nghĩa |

Báo nhầm trên ảnh không có polyp của PolypGen: 13,3% / 10,8% / 22,6% / 69,3%. TSVM báo nhầm ít hơn Baseline, p = 0,011.

**Topology:** TSVM chỉ nhích hơn Baseline, không có ý nghĩa thống kê, và kém PraNet rõ rệt.

### D3. Bài học và sự cố đáng nhớ
- **Checkpoint FP16** làm tràn số BatchNorm tầng 10. Cách khắc phục: vá fork để lưu float32. Đây là lý do có tên "TSVM FP32".
- **Số viết cứng trong báo cáo cũ** sai lệch với dữ liệu. Từ đó quy định mọi số phải sinh từ script.
- **Nhận định "nhóm tự chia dữ liệu"** là sai. Kiểm tra theo ba bước (script, nguồn đầu vào, thư mục thô) và so md5 cho thấy tập chia do tác giả cung cấp.
- **Độ trễ GPU trên laptop** phụ thuộc nhiệt độ và chế độ nguồn, nên báo tỉ lệ thay vì số ms tuyệt đối.
- **Canva:** thay đổi chỉ hiện ra sau khi commit giao dịch. Ảnh thu nhỏ có thể là bản cũ.
- **Windows:** đường dẫn dài hơn 260 ký tự làm cài đặt lỗi, nên venv đặt ở `C:\venv_kl_gpu`. Heredoc Bash dài dễ lỗi, nên ghi script ra file rồi chạy.

---

## E. Trạng thái hiện tại và việc còn lại (29/10/2026, hạn nộp 08/11)

| Hạng mục | Trạng thái |
|---|---|
| Trang đầu, Mở đầu, Ch.1–Ch.6, Kết luận, Phụ lục, Tài liệu tham khảo (md) | Đã viết đủ (29/10). Còn ô [ĐIỀN] (kế hoạch, phân công, học vị GVHD), [CHỤP HÌNH] và vài [CẦN KIỂM TRA]; nhóm tự xử lý sau khi ghép Word. Lời cảm ơn là bản nháp. |
| Ablation (`vmamba_only`, `shape_only`, `shape_vmamba_no_guidance`; seed 0–4) | Xong 29/10: 15/15 lượt, đã tính (`bang/17_*.csv`), vẽ k01/k02, điền mục 6.6. Cả ba biến thể thấp hơn bản đầy đủ, không có ý nghĩa thống kê. |
| Đối chiếu thang điểm | `_KIEM_TRA/G_doi_chieu_thang_diem.md` (29/10). |
| Ghép Word theo Biểu mẫu V3 của trường | Giai đoạn C, chờ chủ dự án duyệt nội dung trước. |
| Ảnh chụp ứng dụng PolypVision (Ch.5) | Người dùng tự chụp, chèn sau khi ghép Word. |
| Hình 4.5 | Đã sửa ô cuối (29/10), bản gốc giữ ở `h4_5_ban_goc.png`. |
| Slide Canva (thiết kế `DAHPtP9XqEY`) | Xong slide 1–3. Từ 29/10 **nhóm tự thiết kế** phần còn lại; sau đó Claude tham khảo cách thiết kế của nhóm để xây kỹ năng làm slide. |
| Turnitin, gửi GVHD | Dự kiến 04–05/11. |
| `06_bao_cao/slide/KE_HOACH_SLIDE.md` | Chưa commit. |

---

## F. Bản đồ tệp quan trọng

| Tệp | Vai trò |
|---|---|
| `CLAUDE.md`, `NGU_CANH_DU_AN.md` | Ngữ cảnh và quy tắc; đọc đầu tiên |
| `00_tai_lieu_tong_quan/` | Nguồn sự thật: 14 md, `bang/*.csv`, `scripts/` |
| `06_bao_cao/md_bao_cao/01…10_*.md` | Các chương báo cáo, bản đầy đủ |
| `06_bao_cao/md_bao_cao_rut_gon/` | Bản rút gọn (thân khoảng 70 trang) |
| `06_bao_cao/ghep_word/ghep_word.py` | Ghép Word/PDF theo Biểu mẫu V3 |
| `06_bao_cao/md_bao_cao/_KIEM_TRA/` | Ghi chú điều tra và phản biện, bảng đối số tài liệu tham khảo |
| `06_bao_cao/hinh/scripts/ve_hinh.py`, `ve_so_do.py` | Vẽ hình và sơ đồ |
| `06_bao_cao/slide/KE_HOACH_SLIDE.md` | Kế hoạch slide bảo vệ |
| `02_ma_nguon/ultralytics_TSVM_FP32/` | Fork Ultralytics có TSVM |
| `PATH_MAP.md` | Tra đường dẫn cũ sang đường dẫn mới |
