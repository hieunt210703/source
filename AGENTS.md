# Quy tắc dự án Phân tích dữ liệu bằng Python

## Phạm vi và mục tiêu

- File này áp dụng cho toàn bộ thư mục hiện tại và mọi thư mục con.
- Xem các PDF trong `source/` và `source/Notes.txt` là tài liệu môn học gốc. Khi giải bài, viết notebook, script, báo cáo hoặc giải thích, phải bám theo mạch kiến thức của các tài liệu này.
- Mục tiêu mặc định là tạo ra một quy trình phân tích dữ liệu có thể chạy lại, giải thích được và đi từ câu hỏi thực tế đến kết luận có bằng chứng.
- Trả lời, chú thích code, tên biểu đồ và phần diễn giải bằng tiếng Việt, trừ tên API, thuật ngữ chuyên môn hoặc khi người dùng yêu cầu ngôn ngữ khác.
- Không bịa dữ liệu, kết quả thống kê, chỉ số mô hình hoặc kết luận. Nếu chưa chạy được dữ liệu thì phải nói rõ kết quả chỉ là kỳ vọng hoặc ví dụ minh họa.

## Bản đồ kiến thức nguồn

Sử dụng tài liệu theo trình tự sau:

1. `Bai_Giang_TH_01_Python_for_DA.pdf`: Python cơ sở, kiểu dữ liệu, toán tử, rẽ nhánh, vòng lặp, hàm, lambda, Series và DataFrame.
2. `Bai01_Gioi_thieu_PTDL-Nhap_Xuat_Bo_du_lieu.pdf`: đặt vấn đề, hiểu dữ liệu, thư viện, nhập/xuất và phân tích cơ bản.
3. `Bai02_Sap_xep_DL.pdf`: dữ liệu khuyết, định dạng, chuẩn hóa, chia khoảng và mã hóa biến phân loại.
4. `Bai03_Truc_quan.pdf`: nguyên tắc trực quan, kiến trúc Matplotlib và các phương thức `plot`.
5. `Bai04_Cong_cu_TQ.pdf`: line, area, histogram, bar, pie, box, scatter, waffle, word cloud và dashboard.
6. `Bai05_PT_Tham_do.pdf`: EDA, thống kê mô tả, tương quan, gom nhóm, heatmap và ANOVA.
7. `Bai06_Mo_hinh.pdf`: hồi quy tuyến tính đơn/đa biến, hồi quy đa thức, Pipeline, MSE và R².
8. `Bai07_Danh_gia_MH.pdf`: train/test, cross-validation, overfitting, underfitting, Ridge và tìm siêu tham số.
9. `Notes.txt`: URL bộ dữ liệu Bài 7, cấu hình hiển thị Pandas và danh sách 26 cột của bộ dữ liệu ô tô.

Tài liệu giảng dạy quyết định phạm vi và cách giải thích. Khi cú pháp trong slide đã lỗi thời, ưu tiên API hiện hành nhưng phải giữ nguyên ý nghĩa bài học.

## Quy trình chuẩn cho một bài phân tích

### 1. Đặt vấn đề

- Nêu câu hỏi cần trả lời, đối tượng phân tích, biến mục tiêu và đầu ra mong muốn trước khi viết mô hình.
- Phân biệt rõ bài toán mô tả, so sánh, kiểm định, dự báo hoặc trực quan.
- Với bộ dữ liệu ô tô, mục tiêu mặc định là giải thích hoặc dự đoán `price`; không tự chọn mục tiêu khác nếu đề bài không yêu cầu.

### 2. Nhập và hiểu dữ liệu

- Dùng Pandas để đọc đúng định dạng: `read_csv`, `read_excel`, `read_json`, `read_sql` hoặc `read_hdf`.
- Kiểm tra tối thiểu: nguồn dữ liệu, ý nghĩa mỗi hàng/cột, `shape`, `head`, `tail`, `info`, `dtypes`, số giá trị duy nhất, thống kê mô tả và số lượng giá trị khuyết.
- Phân biệt biến số, phân loại, thứ tự, ngày giờ, biến độc lập và biến phụ thuộc.
- Kiểm tra tên cột, index, đơn vị đo, miền giá trị, bản ghi trùng và các ký hiệu khuyết như `?`, `.`, chuỗi rỗng, `NA`, `N/A`, `None` hoặc giá trị quy ước riêng.
- Khi xuất dữ liệu trung gian, dùng phương thức `to_*` phù hợp và mặc định `index=False` nếu index không mang ý nghĩa nghiệp vụ.

### 3. Làm sạch và biến đổi

- Chuẩn hóa các ký hiệu khuyết về `NaN` trước khi thống kê hoặc xử lý.
- Chọn `dropna`, `fillna`, trung bình, trung vị, mode, `SimpleImputer` hoặc `KNNImputer` theo bản chất biến và phân phối; luôn giải thích lý do. Không mặc định coi số `0` là khuyết nếu chưa có căn cứ nghiệp vụ.
- Bản ghi thiếu biến mục tiêu thường được loại khỏi bài toán có giám sát. Với biến đầu vào, ưu tiên imputation trong Pipeline để tránh rò rỉ dữ liệu.
- Chuẩn hóa cách viết của cùng một giá trị phân loại, kiểu dữ liệu và đơn vị đo trước khi so sánh. Ví dụ chuyển mpg sang L/100 km phải nêu công thức và xử lý giá trị 0.
- Dùng `astype`, `to_numeric` hoặc `to_datetime` có kiểm soát; sau chuyển đổi phải kiểm tra số giá trị bị ép thành `NaN`.
- Chỉ chuẩn hóa thang đo khi thuật toán hoặc mục tiêu so sánh cần. Các cách trong môn học gồm:
  - scale theo cực đại: `x / x.max()`;
  - Min-Max: `(x - x.min()) / (x.max() - x.min())` hoặc `MinMaxScaler`;
  - Z-score: `(x - mean) / std` hoặc `StandardScaler`.
- Khi chia biến số thành nhóm, dùng mốc có ý nghĩa hoặc `pd.cut`; ghi rõ biên và nhãn nhóm.
- Mã hóa biến phân loại bằng one-hot cho biến không thứ tự; dùng ordinal mapping chỉ khi thứ tự thực sự có ý nghĩa. Tránh tạo bẫy giả về thứ tự từ integer encoding.
- Không ghi đè dữ liệu gốc nếu việc đó làm mất khả năng đối chiếu; giữ tên biến đổi rõ ràng hoặc dùng Pipeline.

### 4. Trực quan dữ liệu

- Mỗi biểu đồ phải trả lời một câu hỏi cụ thể và có tiêu đề, nhãn trục, đơn vị, chú giải khi cần; màu sắc và kích thước phải làm nổi bật thông điệp chính.
- Chọn biểu đồ theo mục đích:
  - line: xu hướng theo thời gian;
  - area: tổng tích lũy hoặc cơ cấu biến đổi theo thời gian;
  - histogram/KDE: phân phối của một biến số;
  - bar/barh: so sánh các nhóm tại một thời điểm hoặc sau tổng hợp;
  - pie/waffle: tỷ trọng với ít nhóm, tổng phải có ý nghĩa;
  - box plot: trung vị, IQR và ngoại lệ;
  - scatter/regression plot: quan hệ giữa hai biến số;
  - heatmap: ma trận tương quan hoặc bảng tổng hợp hai chiều;
  - word cloud: tần suất từ, chỉ dùng như trực quan bổ trợ;
  - dashboard: tổng quan nhiều chỉ số phục vụ quyết định.
- Không dùng pie chart khi có quá nhiều nhóm. Không dùng bar chart thay histogram cho dữ liệu liên tục chưa gom khoảng.
- Khi có nhiều biểu đồ, dùng bố cục nhất quán, `tight_layout()` và tránh chữ, nhãn hoặc chú giải chồng lấn.

### 5. Phân tích thăm dò và thống kê

- Với biến số, xem xét mean, median, mode, min, max, range, quartile, IQR, variance, standard deviation, coefficient of variation, skewness và kurtosis khi phù hợp.
- Nhận diện ngoại lệ theo ngữ cảnh và có thể dùng ngưỡng `Q1 - 1.5*IQR` và `Q3 + 1.5*IQR`; không tự động xóa ngoại lệ chỉ vì vượt ngưỡng.
- Dùng correlation cho mức độ liên hệ, không diễn giải thành quan hệ nhân quả và không suy luận bắc cầu.
- Với Pearson correlation, báo cả hệ số và p-value; đồng thời kiểm tra scatter plot, tính tuyến tính và ngoại lệ. Có thể dùng mốc định hướng từ bài giảng: `|r| < 0.3` rất yếu/không đáng kể, `0.3-0.5` yếu, `0.5-0.8` vừa, `0.8-1.0` mạnh.
- Dùng `groupby`, `value_counts`, `pivot`/`pivot_table` và heatmap để thăm dò biến phân loại.
- Dùng t-test cho hai nhóm hoặc one-way ANOVA cho từ ba nhóm trở lên khi giả định phù hợp. Với ANOVA, báo F-statistic, p-value, mức ý nghĩa `alpha` và kết luận theo ngữ cảnh; p-value nhỏ không tự chứng minh mức ảnh hưởng lớn.
- Chọn biến quan trọng dựa trên kết hợp hiểu biết nghiệp vụ, trực quan, thống kê và khả năng tổng quát hóa; không chỉ dựa vào một hệ số duy nhất.

### 6. Xây dựng mô hình

- Chỉ áp dụng phần này khi phạm vi bài toán có mô hình dự đoán hoặc người dùng yêu cầu. Bài toán thuần mô tả không bắt buộc phải thêm mô hình.
- Tách rõ `X` là đặc trưng và `y` là mục tiêu. Mọi bước học tham số từ dữ liệu như imputation, scaling, encoding và tạo polynomial features phải được fit chỉ trên tập train.
- Bắt đầu bằng mô hình cơ sở dễ giải thích. Chỉ tăng độ phức tạp khi mô hình cơ sở chưa đáp ứng câu hỏi và phạm vi dự án thực sự yêu cầu:
  1. hồi quy tuyến tính đơn biến;
  2. hồi quy tuyến tính đa biến;
  3. hồi quy đa thức khi quan hệ có độ cong;
  4. Ridge khi cần điều chuẩn và giảm overfitting/đa cộng tuyến.
- Dùng `Pipeline` và `ColumnTransformer` khi quy trình có nhiều bước học từ dữ liệu hoặc có cả cột số và phân loại; không bắt buộc cho một hồi quy tuyến tính đơn biến không có bước biến đổi.
- Với mô hình tuyến tính, khi cần giải thích phải báo intercept, coefficients, chiều ảnh hưởng và giới hạn diễn giải.
- Kiểm tra residual plot: phần dư nên phân tán ngẫu nhiên quanh 0; dạng cong, hình phễu hoặc xu hướng có hệ thống là dấu hiệu mô hình/giả định chưa phù hợp.
- Không tăng bậc đa thức hoặc số biến chỉ để cải thiện điểm train.

### 7. Đánh giá và tinh chỉnh

- Chỉ áp dụng các yêu cầu đánh giá mô hình khi phạm vi bài toán có xây dựng mô hình.
- Dùng `train_test_split` với `random_state` cố định và nêu rõ tỷ lệ train/test. Tỷ lệ 70/30 hoặc 80/20 đều hợp lệ nếu có lý do.
- So sánh hiệu suất train và test để phát hiện:
  - overfitting: train tốt nhưng test giảm rõ rệt;
  - underfitting: cả train và test đều kém;
  - good fit: hiệu suất đủ tốt và khoảng cách train-test hợp lý.
- Dùng k-fold cross-validation khi cần so sánh, chọn hoặc tinh chỉnh nhiều mô hình. Với một mô hình cơ sở đơn giản, một lần chia train/test cố định là đủ nếu báo rõ giới hạn đánh giá.
- Với hồi quy, tối thiểu xem xét MSE hoặc RMSE, MAE và R². MSE/RMSE/MAE càng thấp càng tốt; R² cao hơn thường tốt hơn nhưng có thể âm trên dữ liệu ngoài mẫu và không tự bảo đảm mô hình hợp lý.
- So sánh mô hình trên cùng cách chia dữ liệu hoặc cùng các fold. Không so sánh các chỉ số lấy từ các tập khác nhau như thể chúng tương đương.
- Nếu dùng Ridge hoặc mô hình có siêu tham số, chọn siêu tham số bằng cross-validation, `GridSearchCV` hoặc `RandomizedSearchCV`; không chọn dựa trên test set cuối cùng.
- Sau khi chốt quy trình và siêu tham số, chỉ đánh giá test set cuối một lần. Có thể fit lại mô hình cuối trên toàn bộ dữ liệu khi mục tiêu là triển khai, nhưng phải giữ nguyên kết quả đánh giá trước đó.

### 8. Kết luận và bàn giao

- Kết luận phải trả lời trực tiếp câu hỏi ban đầu, kèm số liệu hoặc biểu đồ làm bằng chứng.
- Nêu giới hạn: chất lượng và kích thước dữ liệu, missing values, ngoại lệ, giả định thống kê, khả năng thiên lệch và phạm vi tổng quát hóa.
- Khi tạo notebook/script, bảo đảm có thể chạy từ đầu đến cuối trong môi trường sạch: import đầy đủ, đường dẫn rõ ràng, seed cố định, không phụ thuộc vào trạng thái cell trước.
- Khi sửa hoặc tạo code, chạy kiểm tra phù hợp và báo chính xác phần đã kiểm tra; không tuyên bố thành công nếu chưa thực thi.

## Quy ước cho bộ dữ liệu trong môn học

### Bộ dữ liệu ô tô

- Dữ liệu gốc: `https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data`.
- Mô tả UCI: `https://archive.ics.uci.edu/dataset/10/automobile`.
- EDA: `https://raw.githubusercontent.com/datasethub/ds105/master/EDA_automobile.csv`.
- Phát triển mô hình:
  - `https://raw.githubusercontent.com/datasethub/ds105/master/Model_Dataset.csv`;
  - `https://raw.githubusercontent.com/datasethub/ds105/master/Model_Dataset_Lab.csv`.
- Đánh giá mô hình: `https://raw.githubusercontent.com/datasethub/ds105/master/Model-Evaluation-and-Refinement.csv`.
- Thứ tự 26 cột dữ liệu gốc:
  `symboling`, `normalized-losses`, `make`, `fuel-type`, `aspiration`, `num-of-doors`, `body-style`, `drive-wheels`, `engine-location`, `wheel-base`, `length`, `width`, `height`, `curb-weight`, `engine-type`, `num-of-cylinders`, `engine-size`, `fuel-system`, `bore`, `stroke`, `compression-ratio`, `horsepower`, `peak-rpm`, `city-mpg`, `highway-mpg`, `price`.
- Các đặc trưng được tài liệu xác định là ứng viên quan trọng cho `price` gồm `curb-weight`, `engine-size`, `length`, `width`, `horsepower`, `city-mpg`, `highway-mpg`, `wheel-base`, `bore` và `drive-wheels`. Phải xác minh lại trên dữ liệu thực tế trước khi kết luận.

### Bộ dữ liệu nhập cư Canada

- Dữ liệu: `https://github.com/datasethub/ds105/blob/master/Canada.xlsx`.
- Khi dùng theo bài giảng, đổi `OdName` thành `Country`, `AreaName` thành `Continent`, `RegName` thành `Region`; cân nhắc bỏ `AREA`, `REG`, `DEV`, `Type`, `Coverage` và giữ các cột năm cần phân tích.
- Trước khi tính tổng theo năm, chỉ chọn cột năm dạng số; không cộng nhầm mã vùng hoặc cột metadata.

## Chuẩn code và khả năng tương thích

- Ưu tiên Python, NumPy, Pandas, Matplotlib, Seaborn, SciPy, scikit-learn và Statsmodels theo đúng nhu cầu; không thêm thư viện nếu công cụ chuẩn đã giải quyết rõ ràng.
- Ưu tiên thao tác vector hóa của NumPy/Pandas cho dữ liệu bảng; dùng vòng lặp, comprehension, hàm hoặc lambda khi chúng làm ý định rõ hơn, không dùng `apply` nếu phép toán vector hóa đơn giản hơn.
- Đặt tên biến có nghĩa; tách bước tải dữ liệu, làm sạch, EDA, mô hình và đánh giá. Viết hàm cho logic được lặp lại.
- Tránh sửa DataFrame qua chained assignment; dùng `.loc` rõ ràng và cân nhắc `.copy()` khi tạo lát dữ liệu để sửa.
- Dùng API hiện hành thay cho cú pháp cũ trong slide:
  - dùng `.loc` và `.iloc`, không dùng `.ix`;
  - dùng `pd.set_option('display.max_colwidth', None)`, không dùng `-1`;
  - dùng `sns.histplot`, `sns.kdeplot` hoặc `sns.displot`, không dùng `sns.distplot`;
  - dùng `np.arange`, không dùng `np.arrange`;
  - với Dash mới, ưu tiên `app.run(...)` nếu phiên bản cài đặt không còn `app.run_server(...)`.
- Không hard-code kết quả tính toán từ slide. Luôn tính lại từ DataFrame đang dùng.
- Khi API, phiên bản thư viện hoặc nguồn trực tuyến có thể đã thay đổi, kiểm tra tài liệu chính thức hoặc phiên bản môi trường trước khi sửa cú pháp.

## Danh sách kiểm tra hoàn tất

Một bài phân tích chỉ được xem là hoàn tất khi:

- câu hỏi, dữ liệu, biến mục tiêu và phạm vi đã rõ;
- dữ liệu đã được kiểm tra kiểu, khuyết, trùng, miền giá trị và đơn vị;
- các quyết định làm sạch/biến đổi đều có lý do;
- biểu đồ đúng loại và có nhãn đầy đủ;
- kết luận thống kê không nhầm tương quan với nhân quả;
- nếu phạm vi có mô hình, quy trình mô hình không rò rỉ dữ liệu;
- nếu phạm vi có mô hình, mô hình được đánh giá ngoài mẫu và/hoặc bằng cross-validation;
- kết quả có thể tái lập và code chạy từ đầu đến cuối;
- kết luận trả lời đúng câu hỏi, có bằng chứng và nêu giới hạn.
