# PROJECT PLAN — EMPLOYEE SALARY ANALYTICS DASHBOARD

> **Đề tài:** Xây dựng ứng dụng Dashboard phân tích và trực quan hóa dữ liệu lương nhân viên bằng Python  
> **Loại dự án:** Tiểu luận kết hợp ứng dụng web phân tích dữ liệu  
> **Trạng thái:** Planning — dùng checklist để cập nhật khi triển khai  
> **Nguyên tắc:** Không gắn thời gian cố định. Chỉ chuyển phase khi đáp ứng điều kiện hoàn thành (Definition of Done — DoD).

---

## 1. Tổng quan

### 1.1. Mục tiêu

Xây dựng một dashboard tương tác giúp người dùng khám phá bộ dữ liệu nhân viên, xem các chỉ số lương tổng quan, so sánh lương giữa các nhóm, tìm hiểu mối liên hệ giữa các thuộc tính và mức lương, minh họa hồi quy tuyến tính đơn giản, lọc dữ liệu và xuất kết quả.

**Đầu ra cuối cùng:** một ứng dụng Streamlit chạy được, source code có cấu trúc, bộ kiểm thử, tài liệu hướng dẫn và nội dung tổng kết phân tích để sử dụng trong bài tiểu luận.

### 1.2. Các câu hỏi phân tích

1. Quy mô dữ liệu và phân bố mức lương như thế nào?
2. Mức lương trung bình/trung vị khác nhau thế nào theo phòng ban và chức danh?
3. Phân bố lương khác nhau thế nào theo trình độ học vấn và địa điểm làm việc?
4. Số năm kinh nghiệm và độ tuổi có mối liên hệ như thế nào với lương?
5. Khi lọc một nhóm nhân viên cụ thể, các KPI, biểu đồ và bảng dữ liệu thay đổi ra sao?
6. Hồi quy tuyến tính đơn biến dùng số năm kinh nghiệm dự đoán lương đạt kết quả thế nào trên tập kiểm thử?

### 1.3. Phạm vi chức năng

| Trang | Nội dung trọng tâm |
|---|---|
| Overview | KPI tổng quan; phân bố lương; cơ cấu nhân viên theo phòng ban |
| Salary Analysis | So sánh lương theo phòng ban, chức danh, học vấn và địa điểm; xem độ phân tán |
| Experience Insights | Kinh nghiệm/tuổi so với lương; tương quan; hồi quy tuyến tính đơn biến |
| Data Explorer | Tìm kiếm, lọc, xem bảng và xuất CSV |

**Trong phạm vi:** đọc CSV cố định, kiểm tra dữ liệu, phân tích mô tả, biểu đồ tương tác, bộ lọc dùng chung, một mô hình hồi quy tuyến tính đơn biến `Experience_Years → Salary`, xử lý trạng thái rỗng/lỗi, kiểm thử và tài liệu.

**Ngoài phạm vi mặc định:** các mô hình khác ngoài hồi quy tuyến tính đơn biến nêu trên, dự đoán lương dùng cho quyết định thực tế, tối ưu siêu tham số, đăng nhập/phân quyền, chỉnh sửa dữ liệu, hệ thống upload nhiều định dạng, thu thập dữ liệu từ internet, MySQL, REST API riêng và dashboard thời gian thực. Chỉ bổ sung qua change request sau khi hoàn thành bản lõi.

### 1.4. Dữ liệu đầu vào đã kiểm tra

- File dữ liệu hiện dùng: `Employers_data.csv`.
- 10.000 dòng, 10 cột; chưa phát hiện giá trị null trong dữ liệu hiện tại; `Employee_ID` là duy nhất.
- Các cột: `Employee_ID`, `Name`, `Age`, `Gender`, `Department`, `Job_Title`, `Experience_Years`, `Education_Level`, `Location`, `Salary`.
- Giá trị đối chiếu ban đầu trên **toàn bộ dữ liệu, chưa lọc**: `Salary.min() = 25000`, `Salary.max() = 215000`, `Salary.mean() = 115381.5`, `Salary.median() = 120000`.
- Chưa có tài liệu xác thực đơn vị tiền tệ, kỳ trả lương, nguồn gốc và phương pháp thu thập/tạo dữ liệu. **Không tự ghi là USD/năm, không suy diễn đại diện thị trường lao động thực tế.**

### 1.5. Stack kỹ thuật mặc định

| Thành phần | Lựa chọn |
|---|---|
| Ngôn ngữ và ứng dụng web | Python + Streamlit |
| Đọc/lọc/tổng hợp | Pandas |
| Tính toán bổ trợ | NumPy (khi cần) |
| Thống kê tương quan | SciPy |
| Hồi quy tuyến tính và đánh giá | scikit-learn |
| Biểu đồ | Plotly |
| Kiểm thử | pytest + kiểm thử giao diện thủ công |
| Dữ liệu | CSV nội bộ, chỉ đọc |
| Quản lý source | Git + `requirements.txt` |

**Kiến trúc:** một ứng dụng Streamlit nhiều trang, module xử lý dữ liệu độc lập với code UI; không có API/DB riêng ở phiên bản lõi.

---

## 2. Cách sử dụng kế hoạch

- Mỗi phase có **một mục tiêu nhỏ**, checklist, đầu ra và DoD riêng.
- Trạng thái dùng: `TODO` → `IN PROGRESS` → `BLOCKED` hoặc `DONE`. Ghi trạng thái vào dòng `Status` của phase.
- Nếu phát hiện bug, tạo issue và ghi phase liên quan; không âm thầm thay đổi phạm vi.
- Chỉ thực hiện phase phụ thuộc sau khi phần nền tảng liên quan đạt DoD; các phase độc lập có thể làm song song.
- Mỗi phase ưu tiên một commit hoặc pull request có thể kiểm tra được.
- Không bắt buộc làm toàn bộ nhiệm vụ của một nhóm lớn cùng lúc. **Làm xong từng phase rồi mới đánh dấu.**

### Quy tắc DoD chung

Một phase chỉ được coi là DONE nếu: (1) checklist đã hoàn tất; (2) đầu ra hiện diện trong source/tài liệu; (3) chạy được hoặc đã có bằng chứng kiểm thử phù hợp; (4) không có lỗi blocker thuộc phạm vi phase; (5) ghi lại quyết định/giả định mới phát sinh.

---

## 3. Roadmap theo phase

### Nhóm A — Định nghĩa bài toán và hiểu dữ liệu

#### Phase 00 — Chốt mục tiêu và phạm vi

**Status:** TODO  
**Phụ thuộc:** Không có.

- [ ] Viết mục tiêu, đối tượng dùng và 6 câu hỏi phân tích chính.
- [ ] Chốt 4 trang chức năng và danh sách ngoài phạm vi.
- [ ] Lập danh sách KPI/biểu đồ mong muốn ở mức tên và mục đích.

**Đầu ra:** `docs/01_scope.md`.  
**DoD:** Có bảng phạm vi rõ ràng; mỗi chức năng đều gắn với ít nhất một câu hỏi phân tích.

#### Phase 01 — Audit dữ liệu gốc

**Status:** TODO  
**Phụ thuộc:** Phase 00.

- [ ] Đọc CSV, kiểm tra số dòng/cột, tên cột, kiểu dữ liệu, null và duplicate ID.
- [ ] Khảo sát các giá trị danh mục và khoảng giá trị số.
- [ ] Ghi lại các bất thường/rủi ro cần theo dõi, không xóa bản ghi một cách mặc định.

**Đầu ra:** `docs/02_data_audit.md` và script/notebook audit có thể chạy lại.  
**DoD:** Có bảng audit tái tạo được từ CSV; số lượng bản ghi đầu vào được ghi nhận.

#### Phase 02 — Data dictionary và quy tắc tính toán

**Status:** TODO  
**Phụ thuộc:** Phase 01.

- [ ] Mô tả ý nghĩa, kiểu dữ liệu và vai trò của 10 cột.
- [ ] Chốt định nghĩa `employee_count`, `average_salary`, `median_salary`, `min_salary`, `max_salary`.
- [ ] Chốt quy tắc hiển thị: đơn vị lương chưa xác thực; số thập phân; giá trị thiếu; mẫu số của tỷ lệ.

**Đầu ra:** `docs/03_data_dictionary.md`, `docs/04_metric_definitions.md`.  
**DoD:** KPI có công thức và phạm vi tính toán; không còn thuật ngữ mơ hồ trong giao diện.

### Nhóm B — Nền tảng xử lý dữ liệu

#### Phase 03 — Khởi tạo project

**Status:** TODO  
**Phụ thuộc:** Phase 00.

- [ ] Tạo repository, virtual environment và `requirements.txt`.
- [ ] Tạo cấu trúc `app.py`, `pages/`, `utils/`, `data/`, `tests/`, `docs/`.
- [ ] Xây dựng trang Streamlit tối thiểu và xác nhận lệnh chạy hoạt động.

**Đầu ra:** project skeleton chạy được.  
**DoD:** Một người khác có thể cài dependency và mở trang app từ hướng dẫn ngắn.

#### Phase 04 — Module đọc và kiểm tra dữ liệu

**Status:** TODO  
**Phụ thuộc:** Phase 01, 03.

- [ ] Viết `load_data()` đọc CSV từ đường dẫn cấu hình, không hard-code đường dẫn máy cá nhân.
- [ ] Kiểm tra các cột bắt buộc và kiểu dữ liệu cơ bản; trả lỗi dễ hiểu nếu sai schema/file thiếu.
- [ ] Kiểm tra ID trùng, giá trị số không hợp lệ và các bất thường cần cảnh báo.

**Đầu ra:** `utils/data_loader.py` và kiểm thử đầu vào cơ bản.  
**DoD:** Đọc được dữ liệu đúng schema; lỗi đầu vào không gây crash khó hiểu.

#### Phase 05 — Chuẩn hóa và bảo toàn dữ liệu

**Status:** TODO  
**Phụ thuộc:** Phase 04.

- [ ] Xác định rõ quy tắc ép kiểu/chuẩn hóa text nếu cần.
- [ ] Giữ dữ liệu nguồn bất biến; hàm xử lý trả về dataframe mới.
- [ ] Ghi nhận số bản ghi bị loại hoặc thay đổi nếu phát sinh xử lý; không chỉnh sửa ngầm.

**Đầu ra:** `utils/data_processing.py` và ghi chú quy tắc xử lý.  
**DoD:** Input và output có thể đối chiếu; dữ liệu không bị mất im lặng.

#### Phase 06 — Xây dựng các hàm thống kê

**Status:** TODO  
**Phụ thuộc:** Phase 02, 05.

- [ ] Viết hàm KPI cơ bản cho một dataframe bất kỳ.
- [ ] Viết hàm tổng hợp theo một trường danh mục: số nhân viên, mean, median, min, max.
- [ ] Viết hàm tạo nhóm kinh nghiệm phục vụ biểu đồ (quy tắc nhóm phải ghi tài liệu).

**Đầu ra:** `utils/metrics.py`.  
**DoD:** Các hàm chạy độc lập với Streamlit và trả kết quả đúng trên mẫu dữ liệu kiểm thử.

#### Phase 07 — Bộ lọc dùng chung

**Status:** TODO  
**Phụ thuộc:** Phase 05, 06.

- [ ] Tạo hàm lọc theo phòng ban, chức danh, học vấn, địa điểm, khoảng lương và kinh nghiệm.
- [ ] Thiết kế filter state dùng chung giữa các trang; xác định hành vi mặc định và reset.
- [ ] Quy định KPI, biểu đồ, bảng và CSV đều dùng **cùng một dataframe đã lọc**.

**Đầu ra:** `utils/filters.py` và quy tắc filter trong tài liệu.  
**DoD:** Kết hợp nhiều bộ lọc hoạt động chính xác; reset trả về dữ liệu ban đầu.

### Nhóm C — Giao diện và phân tích

#### Phase 08 — App shell và điều hướng

**Status:** TODO  
**Phụ thuộc:** Phase 03, 07.

- [ ] Tạo 4 trang theo kiến trúc đã chốt và menu điều hướng.
- [ ] Tạo sidebar bộ lọc dùng chung và khu vực hiển thị số bản ghi sau lọc.
- [ ] Tạo bộ component/formatter dùng chung cho tiêu đề, số liệu và chú thích.

**Đầu ra:** điều hướng hoàn chỉnh, UI khung nhất quán.  
**DoD:** Chuyển trang không mất trạng thái filter ngoài ý muốn; chưa cần hoàn thiện tất cả biểu đồ.

#### Phase 09 — Overview: KPI

**Status:** TODO  
**Phụ thuộc:** Phase 06, 08.

- [ ] Hiển thị tổng nhân viên, lương trung bình, trung vị, thấp nhất và cao nhất.
- [ ] Format số nhất quán; gắn ghi chú đơn vị lương chưa xác thực.
- [ ] Kiểm tra KPI thay đổi theo bộ lọc và xử lý trường hợp không có bản ghi.

**Đầu ra:** phần KPI của trang Overview.  
**DoD:** KPI đối chiếu đúng với kết quả Pandas cho full data và ít nhất hai nhóm đã lọc.

#### Phase 10 — Overview: biểu đồ tổng quan

**Status:** TODO  
**Phụ thuộc:** Phase 09.

- [ ] Tạo histogram phân bố lương.
- [ ] Tạo biểu đồ số lượng/tỷ trọng nhân viên theo phòng ban.
- [ ] Tạo biểu đồ lương trung bình theo phòng ban kèm số lượng mẫu khi cần.

**Đầu ra:** trang Overview hoạt động đầy đủ.  
**DoD:** Cả ba biểu đồ nhận dataframe đã lọc; tiêu đề và nhãn trục rõ ràng.

#### Phase 11 — Salary Analysis: so sánh tổ chức

**Status:** TODO  
**Phụ thuộc:** Phase 06, 08.

- [ ] Tạo biểu đồ so sánh mean/median salary theo phòng ban.
- [ ] Tạo biểu đồ so sánh mean/median salary theo chức danh.
- [ ] Hiển thị cỡ mẫu mỗi nhóm để tránh diễn giải nhóm quá ít bản ghi.

**Đầu ra:** hai biểu đồ đầu của Salary Analysis.  
**DoD:** Giá trị biểu đồ khớp hàm tổng hợp; filter toàn cục có hiệu lực.

#### Phase 12 — Salary Analysis: học vấn và địa điểm

**Status:** TODO  
**Phụ thuộc:** Phase 11.

- [ ] Tạo biểu đồ lương theo trình độ học vấn.
- [ ] Tạo biểu đồ lương theo địa điểm làm việc.
- [ ] Bổ sung tùy chọn sắp xếp hoặc chuyển mean/median nếu UI còn đơn giản.

**Đầu ra:** hoàn thiện các nhóm so sánh chính trên Salary Analysis.  
**DoD:** Có thể đọc được giá trị, nhóm và cỡ mẫu; không gọi chênh lệch là quan hệ nhân quả.

#### Phase 13 — Salary Analysis: độ phân tán

**Status:** TODO  
**Phụ thuộc:** Phase 11.

- [ ] Thêm box plot phân bố lương theo một chiều phân nhóm phù hợp.
- [ ] Viết chú thích ngắn giải thích median, tứ phân vị và outlier trên biểu đồ.
- [ ] Kiểm tra hiển thị khi bộ lọc chỉ còn một nhóm hoặc một vài bản ghi.

**Đầu ra:** biểu đồ phân bố/biến thiên lương.  
**DoD:** Biểu đồ không lỗi ở nhóm nhỏ và không đánh đồng mean với median.

#### Phase 14 — Experience Insights: kinh nghiệm

**Status:** TODO  
**Phụ thuộc:** Phase 06, 08.

- [ ] Tạo scatter plot `Experience_Years` so với `Salary`.
- [ ] Tạo biểu đồ mức lương theo nhóm kinh nghiệm đã định nghĩa.
- [ ] Tính/hiển thị Pearson correlation gồm hệ số và p-value nếu đủ dữ liệu biến thiên; nêu rõ đây là mô tả, không chứng minh nguyên nhân.
- [ ] Chia dữ liệu 80/20 với `random_state=42`, fit hồi quy tuyến tính đơn biến `Experience_Years → Salary` chỉ trên tập train.
- [ ] Hiển thị phương trình hồi quy, R² train/test, MAE và RMSE trên tập test cùng đường hồi quy.
- [ ] Nếu dữ liệu sau lọc quá ít hoặc không có biến thiên, không fit mô hình và hiển thị thông báo phù hợp.

**Đầu ra:** phần phân tích kinh nghiệm và mô hình hồi quy tuyến tính đơn biến.  
**DoD:** Biểu đồ, tương quan và mô hình dùng cùng dữ liệu sau lọc; mô hình không rò rỉ dữ liệu; chỉ số train/test tái lập được; xử lý trường hợp không đủ dữ liệu.

#### Phase 15 — Experience Insights: độ tuổi

**Status:** TODO  
**Phụ thuộc:** Phase 14.

- [ ] Tạo scatter plot `Age` so với `Salary`.
- [ ] Thêm cách phân nhóm tuổi minh bạch nếu cần so sánh rõ hơn.
- [ ] Viết ghi chú tránh suy luận tuổi/kinh nghiệm là nguyên nhân trực tiếp tạo ra mức lương.

**Đầu ra:** trang Experience Insights hoàn chỉnh.  
**DoD:** Các biểu đồ rõ nhãn, tương thích filter và có chú thích giới hạn diễn giải; mô hình chỉ là minh họa trên bộ dữ liệu hiện tại, không dùng để quyết định lương thực tế.

#### Phase 16 — Data Explorer: tra cứu

**Status:** TODO  
**Phụ thuộc:** Phase 07, 08.

- [ ] Hiển thị bảng dữ liệu sau lọc với các cột phù hợp.
- [ ] Bổ sung tìm kiếm theo `Employee_ID` hoặc `Name`.
- [ ] Hiển thị số dòng tìm được và thông báo nếu không có kết quả.

**Đầu ra:** trang tra cứu hoạt động.  
**DoD:** Tìm kiếm kết hợp được với filter; bảng không hiện dữ liệu ngoài điều kiện đã chọn.

#### Phase 17 — Data Explorer: xuất dữ liệu

**Status:** TODO  
**Phụ thuộc:** Phase 16.

- [ ] Thêm nút tải CSV của **kết quả đang lọc/tìm kiếm**.
- [ ] Định nghĩa thứ tự cột, tên file và encoding UTF-8 phù hợp.
- [ ] Kiểm tra số dòng/nội dung file tải về so với bảng hiện tại.

**Đầu ra:** tính năng download CSV.  
**DoD:** Không xuất nhầm full data khi đang lọc; xử lý kết quả rỗng có chủ đích.

### Nhóm D — Tính ổn định và chất lượng

#### Phase 18 — UX, trạng thái rỗng và lỗi

**Status:** TODO  
**Phụ thuộc:** Phase 09–17.

- [ ] Thống nhất format số, nhãn, màu, khoảng cách và chú thích trên 4 trang.
- [ ] Hiển thị empty state cho bộ lọc không có dữ liệu; không để biểu đồ/KPI lỗi hoặc gây hiểu sai.
- [ ] Hiển thị thông báo dễ hiểu khi file CSV không tồn tại, sai schema hoặc đọc thất bại.

**Đầu ra:** UI nhất quán và các trạng thái ngoại lệ đã xử lý.  
**DoD:** Có thể demo cả luồng thành công lẫn luồng lỗi có kiểm soát.

#### Phase 19 — Unit test cho logic dữ liệu

**Status:** TODO  
**Phụ thuộc:** Phase 04–07, 14.

- [ ] Test loader/schema và các tình huống dữ liệu lỗi bằng fixture nhỏ.
- [ ] Test KPI/tổng hợp: full data, nhóm đã lọc, dataframe rỗng và nhóm một bản ghi.
- [ ] Test filter kết hợp, reset và phân nhóm kinh nghiệm.
- [ ] Test hồi quy tuyến tính với split cố định, kiểm tra phương trình và các thang đo R², MAE, RMSE.

**Đầu ra:** thư mục `tests/` với các test tự động.  
**DoD:** `pytest` chạy thành công; phép tính không phụ thuộc thao tác thủ công trên UI.

#### Phase 20 — Kiểm thử tích hợp 4 trang

**Status:** TODO  
**Phụ thuộc:** Phase 18, 19.

- [ ] Kiểm tra flow mở app → đổi filter → chuyển trang → xem KPI/chart/table.
- [ ] Kiểm tra search và export; đối chiếu giá trị sau lọc giữa các thành phần.
- [ ] Lập danh sách bug, mức độ nghiêm trọng, kết quả retest và regression.

**Đầu ra:** `docs/05_test_cases.md`, `docs/06_test_results.md`.  
**DoD:** Các luồng chính PASS; không còn bug blocker/critical chưa xử lý.

#### Phase 21 — Hiệu năng và an toàn dữ liệu

**Status:** TODO  
**Phụ thuộc:** Phase 20.

- [ ] Dùng `st.cache_data` hợp lý cho đọc/tiền xử lý dữ liệu; tránh tính lại không cần thiết.
- [ ] Kiểm tra app với 10.000 dòng, thao tác filter và chuyển trang; ghi lại kết quả thực nghiệm thay vì tự đặt số liệu.
- [ ] Kiểm tra không commit secrets; quyết định cách chia sẻ dữ liệu có `Name` khi public repository/demo.

**Đầu ra:** `docs/07_quality_notes.md` và các chỉnh sửa cần thiết.  
**DoD:** Luồng chính đáp ứng được khi demo; rủi ro chia sẻ dữ liệu đã được đánh giá.

### Nhóm E — Kết quả nghiên cứu và bàn giao

#### Phase 22 — Tổng hợp insight và giới hạn nghiên cứu

**Status:** TODO  
**Phụ thuộc:** Phase 20.

- [ ] Chọn các biểu đồ/KPI và kết quả hồi quy thể hiện câu trả lời cho 6 câu hỏi phân tích.
- [ ] Viết nhận xét dựa trên số liệu thực tế đã kiểm tra; phân biệt mô tả và suy luận.
- [ ] Nêu rõ các giới hạn: thiếu thời gian thu thập, đơn vị/kỳ lương chưa xác thực, nguồn gốc dữ liệu chưa xác minh, không suy diễn nhân quả.

**Đầu ra:** `docs/08_findings.md`.  
**DoD:** Mỗi kết luận đều truy ngược được về biểu đồ/bảng và điều kiện lọc.

#### Phase 23 — Tài liệu sử dụng và báo cáo

**Status:** TODO  
**Phụ thuộc:** Phase 21, 22.

- [ ] Viết README: môi trường, cách cài, lệnh chạy, cấu trúc thư mục và thao tác cơ bản.
- [ ] Hoàn thiện nội dung tiểu luận: bài toán → dữ liệu → phương pháp → thiết kế → triển khai → kiểm thử → kết quả → hạn chế.
- [ ] Chuẩn bị ảnh chụp giao diện, bảng KPI và minh họa luồng chức năng.

**Đầu ra:** `README.md` và bản thảo báo cáo.  
**DoD:** Người khác có thể dựng ứng dụng từ source và hiểu các kết quả đã trình bày.

#### Phase 24 — Nghiệm thu phiên bản lõi

**Status:** TODO  
**Phụ thuộc:** Phase 23.

- [ ] Chạy ứng dụng từ môi trường sạch theo README.
- [ ] Thực hiện checklist acceptance và lưu kết quả cuối cùng.
- [ ] Đóng gói source/tài liệu; ghi danh sách issue còn lại và backlog tương lai.

**Đầu ra:** bản bàn giao/demo của MVP.  
**DoD:** Tất cả acceptance criteria ở Mục 5 đạt; không còn bug blocker/critical.

---

## 4. Cấu trúc source mục tiêu

```text
salary-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── Employers_data.csv
├── pages/
│   ├── 1_Overview.py
│   ├── 2_Salary_Analysis.py
│   ├── 3_Experience_Insights.py
│   └── 4_Data_Explorer.py
├── utils/
│   ├── data_loader.py
│   ├── data_processing.py
│   ├── metrics.py
│   ├── filters.py
│   ├── modeling.py
│   └── charts.py
├── tests/
│   ├── test_data_loader.py
│   ├── test_metrics.py
│   ├── test_filters.py
│   └── test_modeling.py
└── docs/
    ├── 01_scope.md
    ├── 02_data_audit.md
    ├── 03_data_dictionary.md
    ├── 04_metric_definitions.md
    ├── 05_test_cases.md
    ├── 06_test_results.md
    ├── 07_quality_notes.md
    └── 08_findings.md
```

> Có thể tinh chỉnh tên file khi code thực tế. Không tạo module rỗng chỉ để khớp cây thư mục; ưu tiên cấu trúc rõ trách nhiệm.

## 5. Acceptance criteria — điều kiện nghiệm thu sản phẩm

| ID | Tiêu chí kiểm tra | Cách xác nhận | Trạng thái |
|---|---|---|---|
| AC-01 | Đọc được file CSV đúng schema, có thông báo khi dữ liệu không hợp lệ | Chạy full data + fixture lỗi | TODO |
| AC-02 | KPI full data đối chiếu đúng: 10.000 dòng; mean 115381.5; min 25000; max 215000; median 120000 | Đối chiếu trực tiếp Pandas | TODO |
| AC-03 | Bộ lọc dùng chung trên cả 4 trang | Lọc 2 điều kiện, chuyển trang | TODO |
| AC-04 | KPI, chart và table dựa vào cùng tập dữ liệu sau lọc | Đối chiếu số bản ghi/kết quả nhóm | TODO |
| AC-05 | Overview có KPI, histogram và biểu đồ phòng ban | Demo chức năng | TODO |
| AC-06 | Salary Analysis có so sánh phòng ban, chức danh, học vấn, địa điểm và phân bố | Demo chức năng | TODO |
| AC-07 | Experience Insights có phân tích kinh nghiệm, tuổi, Pearson correlation và hồi quy tuyến tính `Experience_Years → Salary` với R², MAE, RMSE trên tập test | Demo chức năng + đối chiếu scikit-learn | TODO |
| AC-08 | Data Explorer tìm kiếm/lọc và xuất đúng CSV kết quả | So sánh file export và bảng | TODO |
| AC-09 | Data rỗng, file thiếu, schema sai không gây crash khó hiểu | Test các tình huống lỗi | TODO |
| AC-10 | Có test logic và kết quả kiểm thử tích hợp | Chạy pytest + biên bản test | TODO |
| AC-11 | README đủ để cài và chạy lại | Thử môi trường sạch | TODO |
| AC-12 | Có nhận xét số liệu cùng giới hạn nghiên cứu | Review nội dung báo cáo | TODO |

## 6. Mốc bàn giao theo năng lực, không theo ngày

| Milestone | Các phase | Chứng cứ hoàn thành |
|---|---|---|
| M1 — Problem & Data Ready | 00–02 | Scope, audit, metric dictionary |
| M2 — Data Engine Ready | 03–07 | Loader, processing, metrics, filter chạy được |
| M3 — Dashboard MVP | 08–10 | App shell + Overview hoàn chỉnh |
| M4 — Full Features | 11–17 | 4 trang và export hoạt động |
| M5 — Quality Gate | 18–21 | Empty/error states, tests, kiểm tra hiệu năng/an toàn dữ liệu |
| M6 — Handover | 22–24 | Findings, README, báo cáo, nghiệm thu |

## 7. Risk register và quyết định còn mở

| ID | Vấn đề/rủi ro | Cách xử lý mặc định |
|---|---|---|
| R-01 | Không rõ đơn vị tiền tệ và kỳ lương | Ghi `Salary`/`Salary (dataset units)`; không tự gắn `$` hoặc `/year` |
| R-02 | Không rõ nguồn gốc dữ liệu | Ghi hạn chế trong báo cáo; không khẳng định đại diện cho thị trường thực tế |
| R-03 | Lọc xong KPI, chart, CSV không đồng bộ | Mọi view sử dụng một `filtered_df` chung |
| R-04 | Nhóm có quá ít bản ghi gây diễn giải sai | Hiển thị cỡ mẫu; thận trọng khi so sánh |
| R-05 | Scatter plot dày điểm với 10.000 dòng | Điều chỉnh độ trong suốt/marker; không tùy tiện lấy mẫu khi chưa ghi chú |
| R-06 | CSV có tên cá nhân và thuộc tính nhân viên | Xem xét điều kiện chia sẻ; ẩn/giảm dữ liệu định danh trong ảnh demo công khai |
| R-07 | Phạm vi phát sinh thêm API/DB hoặc mô hình ngoài hồi quy tuyến tính đơn biến | Đưa vào backlog sau MVP, không làm đứt nhịp các phase lõi |

## 8. Backlog sau phiên bản lõi (không phải tiêu chí nghiệm thu)

- [ ] Bộ lọc nhiều lựa chọn với tùy chọn lưu preset.
- [ ] Cho người dùng upload CSV mới có cùng schema.
- [ ] Thêm biểu đồ tương tác chuyên sâu và so sánh hai nhóm được chọn.
- [ ] Tùy chọn ẩn các trường định danh khi export/chia sẻ.
- [ ] Tách FastAPI hoặc bổ sung database **chỉ khi** phát sinh nhu cầu dữ liệu/đối tượng sử dụng thực tế.

## 9. Nhật ký tiến độ / quyết định

| Ngày cập nhật | Phase | Trạng thái | Kết quả / blocker / quyết định | Người thực hiện |
|---|---|---|---|---|
| — | 00 | TODO | Khởi tạo kế hoạch | — |

---

**Điểm bắt đầu đề xuất:** Phase 00 → 01 → 02. Sau khi data dictionary và metric definitions ổn định, triển khai bộ xử lý dữ liệu trước khi đầu tư vào UI. Không dùng mốc thời gian để thay thế cho DoD.
