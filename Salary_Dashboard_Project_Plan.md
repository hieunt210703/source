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

**Status:** DONE  
**Phụ thuộc:** Không có.

- [x] Viết mục tiêu, đối tượng dùng và 6 câu hỏi phân tích chính.
- [x] Chốt 4 trang chức năng và danh sách ngoài phạm vi.
- [x] Lập danh sách KPI/biểu đồ mong muốn ở mức tên và mục đích.

**Đầu ra:** `docs/01_scope.md`.  
**DoD:** Có bảng phạm vi rõ ràng; mỗi chức năng đều gắn với ít nhất một câu hỏi phân tích.

#### Phase 01 — Audit dữ liệu gốc

**Status:** DONE  
**Phụ thuộc:** Phase 00.

- [x] Đọc CSV, kiểm tra số dòng/cột, tên cột, kiểu dữ liệu, null và duplicate ID.
- [x] Khảo sát các giá trị danh mục và khoảng giá trị số.
- [x] Ghi lại các bất thường/rủi ro cần theo dõi, không xóa bản ghi một cách mặc định.

**Đầu ra:** `docs/02_data_audit.md` và script/notebook audit có thể chạy lại.  
**DoD:** Có bảng audit tái tạo được từ CSV; số lượng bản ghi đầu vào được ghi nhận.

#### Phase 02 — Data dictionary và quy tắc tính toán

**Status:** DONE  
**Phụ thuộc:** Phase 01.

- [x] Mô tả ý nghĩa, kiểu dữ liệu và vai trò của 10 cột.
- [x] Chốt định nghĩa `employee_count`, `average_salary`, `median_salary`, `min_salary`, `max_salary`.
- [x] Chốt quy tắc hiển thị: đơn vị lương chưa xác thực; số thập phân; giá trị thiếu; mẫu số của tỷ lệ.

**Đầu ra:** `docs/03_data_dictionary.md`, `docs/04_metric_definitions.md`.  
**DoD:** KPI có công thức và phạm vi tính toán; không còn thuật ngữ mơ hồ trong giao diện.

### Nhóm B — Nền tảng xử lý dữ liệu

#### Phase 03 — Khởi tạo project

**Status:** DONE  
**Phụ thuộc:** Phase 00.

- [x] Tạo repository, virtual environment và `requirements.txt`.
- [x] Tạo cấu trúc `app.py`, `pages/`, `utils/`, `data/`, `tests/`, `docs/`.
- [x] Xây dựng trang Streamlit tối thiểu và xác nhận lệnh chạy hoạt động.

**Đầu ra:** project skeleton chạy được.  
**DoD:** Một người khác có thể cài dependency và mở trang app từ hướng dẫn ngắn.

#### Phase 04 — Module đọc và kiểm tra dữ liệu

**Status:** DONE  
**Phụ thuộc:** Phase 01, 03.

- [x] Viết `load_data()` đọc CSV từ đường dẫn cấu hình, không hard-code đường dẫn máy cá nhân.
- [x] Kiểm tra các cột bắt buộc và kiểu dữ liệu cơ bản; trả lỗi dễ hiểu nếu sai schema/file thiếu.
- [x] Kiểm tra ID trùng, giá trị số không hợp lệ và các bất thường cần cảnh báo.

**Đầu ra:** `utils/data_loader.py` và kiểm thử đầu vào cơ bản.  
**DoD:** Đọc được dữ liệu đúng schema; lỗi đầu vào không gây crash khó hiểu.

#### Phase 05 — Chuẩn hóa và bảo toàn dữ liệu

**Status:** DONE  
**Phụ thuộc:** Phase 04.

- [x] Xác định rõ quy tắc ép kiểu/chuẩn hóa text nếu cần.
- [x] Giữ dữ liệu nguồn bất biến; hàm xử lý trả về dataframe mới.
- [x] Ghi nhận số bản ghi bị loại hoặc thay đổi nếu phát sinh xử lý; không chỉnh sửa ngầm.

**Đầu ra:** `utils/data_processing.py` và ghi chú quy tắc xử lý.  
**DoD:** Input và output có thể đối chiếu; dữ liệu không bị mất im lặng.

#### Phase 06 — Xây dựng các hàm thống kê

**Status:** DONE  
**Phụ thuộc:** Phase 02, 05.

- [x] Viết hàm KPI cơ bản cho một dataframe bất kỳ.
- [x] Viết hàm tổng hợp theo một trường danh mục: số nhân viên, mean, median, min, max.
- [x] Viết hàm tạo nhóm kinh nghiệm phục vụ biểu đồ (quy tắc nhóm phải ghi tài liệu).

**Đầu ra:** `utils/metrics.py`.  
**DoD:** Các hàm chạy độc lập với Streamlit và trả kết quả đúng trên mẫu dữ liệu kiểm thử.

#### Phase 07 — Bộ lọc dùng chung

**Status:** DONE  
**Phụ thuộc:** Phase 05, 06.

- [x] Tạo hàm lọc theo phòng ban, chức danh, học vấn, địa điểm, khoảng lương và kinh nghiệm.
- [x] Thiết kế filter state dùng chung giữa các trang; xác định hành vi mặc định và reset.
- [x] Quy định KPI, biểu đồ, bảng và CSV đều dùng **cùng một dataframe đã lọc**.

**Đầu ra:** `utils/filters.py` và quy tắc filter trong tài liệu.  
**DoD:** Kết hợp nhiều bộ lọc hoạt động chính xác; reset trả về dữ liệu ban đầu.

### Nhóm C — Giao diện và phân tích

#### Phase 08 — App shell và điều hướng

**Status:** DONE  
**Phụ thuộc:** Phase 03, 07.

- [x] Tạo 4 trang theo kiến trúc đã chốt và menu điều hướng.
- [x] Tạo sidebar bộ lọc dùng chung và khu vực hiển thị số bản ghi sau lọc.
- [x] Tạo bộ component/formatter dùng chung cho tiêu đề, số liệu và chú thích.

**Đầu ra:** điều hướng hoàn chỉnh, UI khung nhất quán.  
**DoD:** Chuyển trang không mất trạng thái filter ngoài ý muốn; chưa cần hoàn thiện tất cả biểu đồ.

#### Phase 09 — Overview: KPI

**Status:** DONE  
**Phụ thuộc:** Phase 06, 08.

- [x] Hiển thị tổng nhân viên, lương trung bình, trung vị, thấp nhất và cao nhất.
- [x] Format số nhất quán; gắn ghi chú đơn vị lương chưa xác thực.
- [x] Kiểm tra KPI thay đổi theo bộ lọc và xử lý trường hợp không có bản ghi.

**Đầu ra:** phần KPI của trang Overview.  
**DoD:** KPI đối chiếu đúng với kết quả Pandas cho full data và ít nhất hai nhóm đã lọc.

#### Phase 10 — Overview: biểu đồ tổng quan

**Status:** DONE  
**Phụ thuộc:** Phase 09.

- [x] Tạo histogram phân bố lương.
- [x] Tạo biểu đồ số lượng/tỷ trọng nhân viên theo phòng ban.
- [x] Tạo biểu đồ lương trung bình theo phòng ban kèm số lượng mẫu khi cần.

**Đầu ra:** trang Overview hoạt động đầy đủ.  
**DoD:** Cả ba biểu đồ nhận dataframe đã lọc; tiêu đề và nhãn trục rõ ràng.

#### Phase 11 — Salary Analysis: so sánh tổ chức

**Status:** DONE  
**Phụ thuộc:** Phase 06, 08.

- [x] Tạo biểu đồ so sánh mean/median salary theo phòng ban.
- [x] Tạo biểu đồ so sánh mean/median salary theo chức danh.
- [x] Hiển thị cỡ mẫu mỗi nhóm để tránh diễn giải nhóm quá ít bản ghi.

**Đầu ra:** hai biểu đồ đầu của Salary Analysis.  
**DoD:** Giá trị biểu đồ khớp hàm tổng hợp; filter toàn cục có hiệu lực.

#### Phase 12 — Salary Analysis: học vấn và địa điểm

**Status:** DONE  
**Phụ thuộc:** Phase 11.

- [x] Tạo biểu đồ lương theo trình độ học vấn.
- [x] Tạo biểu đồ lương theo địa điểm làm việc.
- [x] Bổ sung tùy chọn sắp xếp hoặc chuyển mean/median nếu UI còn đơn giản.

**Đầu ra:** hoàn thiện các nhóm so sánh chính trên Salary Analysis.  
**DoD:** Có thể đọc được giá trị, nhóm và cỡ mẫu; không gọi chênh lệch là quan hệ nhân quả.

#### Phase 13 — Salary Analysis: độ phân tán

**Status:** DONE  
**Phụ thuộc:** Phase 11.

- [x] Thêm box plot phân bố lương theo một chiều phân nhóm phù hợp.
- [x] Viết chú thích ngắn giải thích median, tứ phân vị và outlier trên biểu đồ.
- [x] Kiểm tra hiển thị khi bộ lọc chỉ còn một nhóm hoặc một vài bản ghi.

**Đầu ra:** biểu đồ phân bố/biến thiên lương.  
**DoD:** Biểu đồ không lỗi ở nhóm nhỏ và không đánh đồng mean với median.

#### Phase 14 — Experience Insights: kinh nghiệm

**Status:** DONE  
**Phụ thuộc:** Phase 06, 08.

- [x] Tạo scatter plot `Experience_Years` so với `Salary`.
- [x] Tạo biểu đồ mức lương theo nhóm kinh nghiệm đã định nghĩa.
- [x] Tính/hiển thị Pearson correlation gồm hệ số và p-value nếu đủ dữ liệu biến thiên; nêu rõ đây là mô tả, không chứng minh nguyên nhân.
- [x] Chia dữ liệu 80/20 với `random_state=42`, fit hồi quy tuyến tính đơn biến `Experience_Years → Salary` chỉ trên tập train.
- [x] Hiển thị phương trình hồi quy, R² train/test, MAE và RMSE trên tập test cùng đường hồi quy.
- [x] Nếu dữ liệu sau lọc quá ít hoặc không có biến thiên, không fit mô hình và hiển thị thông báo phù hợp.

**Đầu ra:** phần phân tích kinh nghiệm và mô hình hồi quy tuyến tính đơn biến.  
**DoD:** Biểu đồ, tương quan và mô hình dùng cùng dữ liệu sau lọc; mô hình không rò rỉ dữ liệu; chỉ số train/test tái lập được; xử lý trường hợp không đủ dữ liệu.

#### Phase 15 — Experience Insights: độ tuổi

**Status:** DONE  
**Phụ thuộc:** Phase 14.

- [x] Tạo scatter plot `Age` so với `Salary`.
- [x] Thêm cách phân nhóm tuổi minh bạch nếu cần so sánh rõ hơn.
- [x] Viết ghi chú tránh suy luận tuổi/kinh nghiệm là nguyên nhân trực tiếp tạo ra mức lương.

**Đầu ra:** trang Experience Insights hoàn chỉnh.  
**DoD:** Các biểu đồ rõ nhãn, tương thích filter và có chú thích giới hạn diễn giải; mô hình chỉ là minh họa trên bộ dữ liệu hiện tại, không dùng để quyết định lương thực tế.

#### Phase 16 — Data Explorer: tra cứu

**Status:** DONE  
**Phụ thuộc:** Phase 07, 08.

- [x] Hiển thị bảng dữ liệu sau lọc với các cột phù hợp.
- [x] Bổ sung tìm kiếm theo `Employee_ID` hoặc `Name`.
- [x] Hiển thị số dòng tìm được và thông báo nếu không có kết quả.

**Đầu ra:** trang tra cứu hoạt động.  
**DoD:** Tìm kiếm kết hợp được với filter; bảng không hiện dữ liệu ngoài điều kiện đã chọn.

#### Phase 17 — Data Explorer: xuất dữ liệu

**Status:** DONE  
**Phụ thuộc:** Phase 16.

- [x] Thêm nút tải CSV của **kết quả đang lọc/tìm kiếm**.
- [x] Định nghĩa thứ tự cột, tên file và encoding UTF-8 phù hợp.
- [x] Kiểm tra số dòng/nội dung file tải về so với bảng hiện tại.

**Đầu ra:** tính năng download CSV.  
**DoD:** Không xuất nhầm full data khi đang lọc; xử lý kết quả rỗng có chủ đích.

### Nhóm D — Tính ổn định và chất lượng

#### Phase 18 — UX, trạng thái rỗng và lỗi

**Status:** DONE  
**Phụ thuộc:** Phase 09–17.

- [x] Thống nhất format số, nhãn, màu, khoảng cách và chú thích trên 4 trang.
- [x] Hiển thị empty state cho bộ lọc không có dữ liệu; không để biểu đồ/KPI lỗi hoặc gây hiểu sai.
- [x] Hiển thị thông báo dễ hiểu khi file CSV không tồn tại, sai schema hoặc đọc thất bại.

**Đầu ra:** UI nhất quán và các trạng thái ngoại lệ đã xử lý.  
**DoD:** Có thể demo cả luồng thành công lẫn luồng lỗi có kiểm soát.

#### Phase 19 — Unit test cho logic dữ liệu

**Status:** DONE  
**Phụ thuộc:** Phase 04–07, 14.

- [x] Test loader/schema và các tình huống dữ liệu lỗi bằng fixture nhỏ.
- [x] Test KPI/tổng hợp: full data, nhóm đã lọc, dataframe rỗng và nhóm một bản ghi.
- [x] Test filter kết hợp, reset và phân nhóm kinh nghiệm.
- [x] Test hồi quy tuyến tính với split cố định, kiểm tra phương trình và các thang đo R², MAE, RMSE.

**Đầu ra:** thư mục `tests/` với các test tự động.  
**DoD:** `pytest` chạy thành công; phép tính không phụ thuộc thao tác thủ công trên UI.

#### Phase 20 — Kiểm thử tích hợp 4 trang

**Status:** DONE  
**Phụ thuộc:** Phase 18, 19.

- [x] Kiểm tra flow mở app → đổi filter → chuyển trang → xem KPI/chart/table.
- [x] Kiểm tra search và export; đối chiếu giá trị sau lọc giữa các thành phần.
- [x] Lập danh sách bug, mức độ nghiêm trọng, kết quả retest và regression.

**Đầu ra:** `docs/05_test_cases.md`, `docs/06_test_results.md`.  
**DoD:** Các luồng chính PASS; không còn bug blocker/critical chưa xử lý.

#### Phase 21 — Hiệu năng và an toàn dữ liệu

**Status:** DONE  
**Phụ thuộc:** Phase 20.

- [x] Dùng `st.cache_data` hợp lý cho đọc/tiền xử lý dữ liệu; tránh tính lại không cần thiết.
- [x] Kiểm tra app với 10.000 dòng, thao tác filter và chuyển trang; ghi lại kết quả thực nghiệm thay vì tự đặt số liệu.
- [x] Kiểm tra không commit secrets; quyết định cách chia sẻ dữ liệu có `Name` khi public repository/demo.

**Đầu ra:** `docs/07_quality_notes.md` và các chỉnh sửa cần thiết.  
**DoD:** Luồng chính đáp ứng được khi demo; rủi ro chia sẻ dữ liệu đã được đánh giá.

### Nhóm E — Kết quả nghiên cứu và bàn giao

#### Phase 22 — Tổng hợp insight và giới hạn nghiên cứu

**Status:** DONE  
**Phụ thuộc:** Phase 20.

- [x] Chọn các biểu đồ/KPI và kết quả hồi quy thể hiện câu trả lời cho 6 câu hỏi phân tích.
- [x] Viết nhận xét dựa trên số liệu thực tế đã kiểm tra; phân biệt mô tả và suy luận.
- [x] Nêu rõ các giới hạn: thiếu thời gian thu thập, đơn vị/kỳ lương chưa xác thực, nguồn gốc dữ liệu chưa xác minh, không suy diễn nhân quả.

**Đầu ra:** `docs/08_findings.md`.  
**DoD:** Mỗi kết luận đều truy ngược được về biểu đồ/bảng và điều kiện lọc.

#### Phase 23 — Tài liệu sử dụng và báo cáo

**Status:** DONE  
**Phụ thuộc:** Phase 21, 22.

- [x] Viết README: môi trường, cách cài, lệnh chạy, cấu trúc thư mục và thao tác cơ bản.
- [x] Hoàn thiện nội dung tiểu luận: bài toán → dữ liệu → phương pháp → thiết kế → triển khai → kiểm thử → kết quả → hạn chế.
- [x] Chuẩn bị ảnh chụp giao diện, bảng KPI và minh họa luồng chức năng.

**Đầu ra:** `README.md` và bản thảo báo cáo.  
**DoD:** Người khác có thể dựng ứng dụng từ source và hiểu các kết quả đã trình bày.

#### Phase 24 — Nghiệm thu phiên bản lõi

**Status:** DONE  
**Phụ thuộc:** Phase 23.

- [x] Chạy ứng dụng từ môi trường sạch theo README.
- [x] Thực hiện checklist acceptance và lưu kết quả cuối cùng.
- [x] Đóng gói source/tài liệu; ghi danh sách issue còn lại và backlog tương lai.

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
| AC-01 | Đọc được file CSV đúng schema, có thông báo khi dữ liệu không hợp lệ | Chạy full data + fixture lỗi | PASS |
| AC-02 | KPI full data đối chiếu đúng: 10.000 dòng; mean 115381.5; min 25000; max 215000; median 120000 | Đối chiếu trực tiếp Pandas | PASS |
| AC-03 | Bộ lọc dùng chung trên cả 4 trang | Lọc 2 điều kiện, chuyển trang | PASS |
| AC-04 | KPI, chart và table dựa vào cùng tập dữ liệu sau lọc | Đối chiếu số bản ghi/kết quả nhóm | PASS |
| AC-05 | Overview có KPI, histogram và biểu đồ phòng ban | Demo chức năng | PASS |
| AC-06 | Salary Analysis có so sánh phòng ban, chức danh, học vấn, địa điểm và phân bố | Demo chức năng | PASS |
| AC-07 | Experience Insights có phân tích kinh nghiệm, tuổi, Pearson correlation và hồi quy tuyến tính `Experience_Years → Salary` với R², MAE, RMSE trên tập test | Demo chức năng + đối chiếu scikit-learn | PASS |
| AC-08 | Data Explorer tìm kiếm/lọc và xuất đúng CSV kết quả | So sánh file export và bảng | PASS |
| AC-09 | Data rỗng, file thiếu, schema sai không gây crash khó hiểu | Test các tình huống lỗi | PASS |
| AC-10 | Có test logic và kết quả kiểm thử tích hợp | Chạy pytest + biên bản test | PASS |
| AC-11 | README đủ để cài và chạy lại | Thử môi trường sạch | PASS |
| AC-12 | Có nhận xét số liệu cùng giới hạn nghiên cứu | Review nội dung báo cáo | PASS |

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
| 24/09/2026 | 00–02 | DONE | Chốt scope; audit 10.000 × 10; hoàn thiện data dictionary và metric definitions | Codex |
| 24/09/2026 | 03–07 | DONE | Hoàn thiện project skeleton, loader, processing, metrics và shared filters | Codex |
| 24/09/2026 | 08–17 | DONE | Hoàn thiện 4 trang, Pearson correlation và hồi quy tuyến tính đơn biến | Codex |
| 24/09/2026 | 18–22 | DONE | Empty/error states, test, benchmark, quality notes và findings | Codex |
| 24/09/2026 | 07, 20 | DONE | Phát hiện filter mất khi chuyển page; chuyển sidebar lên entrypoint chung và retest filter/reset/export | Codex |
| 24/09/2026 | 23–24 | DONE | Thêm báo cáo, ảnh giao diện, biên bản nghiệm thu; 20 test PASS; người dùng xác nhận deploy thành công | Codex + người dùng |
| 24/09/2026 | 20, 24 | DONE | Hotfix ImportError trên Cloud: page dùng trực tiếp API ổn định từ `utils.filters`; kiểm tra 4/4 trang từ repository root | Codex |

---

**Trạng thái hiện tại:** MVP đã hoàn thành Phase 00–24 và đạt 12/12 acceptance criteria. Công việc tiếp theo chỉ lấy từ backlog sau phiên bản lõi khi có nhu cầu rõ ràng; ưu tiên xác nhận/ẩn danh dữ liệu trước khi chia sẻ công khai.
