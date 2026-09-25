# Employee Salary Analytics Dashboard

Ứng dụng Streamlit phân tích file CSV nhân viên do người dùng tải lên, cung cấp KPI, biểu đồ tương tác, bộ lọc dùng chung, tra cứu/xuất CSV và một mô hình hồi quy tuyến tính đơn biến minh họa mối liên hệ giữa số năm kinh nghiệm và mức lương. Dashboard chỉ hiện sau khi file được kiểm tra hợp lệ.

## Chức năng

- **Tổng quan:** tổng nhân viên, mean/median/min/max, histogram lương và cơ cấu phòng ban.
- **Phân tích lương:** so sánh mean/median theo phòng ban, chức danh, học vấn, địa điểm và box plot.
- **Kinh nghiệm:** Pearson correlation, hồi quy tuyến tính `Experience_Years → Salary`, R²/MAE/RMSE và residual plot.
- **Khám phá dữ liệu:** lọc, tìm theo ID/tên, chọn cột và tải đúng kết quả đang hiển thị.

## Cài đặt và chạy

Yêu cầu Python 3.11 trở lên.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Mở `http://localhost:8501` nếu trình duyệt không tự mở.

## Tải dữ liệu

Tại màn hình đầu, chọn một file CSV mã hóa UTF-8, phân tách bằng dấu phẩy. File cần có các cột `Employee_ID`, `Name`, `Age`, `Gender`, `Department`, `Job_Title`, `Experience_Years`, `Education_Level`, `Location`, `Salary`; các cột thêm sẽ không tham gia phân tích. Dữ liệu không được thiếu giá trị ở các cột bắt buộc; `Employee_ID` phải duy nhất. Bốn cột số cần là số nguyên, `Age` từ 15 đến 100, `Experience_Years` không âm và không lớn hơn `Age`, `Salary` phải dương.

Sau khi tải thành công, cả bốn trang dùng cùng dữ liệu trong phiên hiện tại. Có thể mở mục **Tải hoặc thay file CSV nhân viên** ở đầu trang để đổi file; khi đổi file, bộ lọc sẽ được đặt lại. Dữ liệu tải lên chỉ giữ trong phiên Streamlit, không ghi vào repository. File `data/Employers_data.csv` vẫn dùng cho script và kiểm thử, không tự hiển thị khi mở ứng dụng.

## Kiểm thử

```powershell
python -m pytest -q
python scripts/audit_data.py
python scripts/benchmark_core.py
```

Test bao phủ schema loader, luồng tải file, KPI chuẩn, filter kết hợp, nhóm tuổi/kinh nghiệm, biểu đồ, Pearson correlation, hồi quy tuyến tính, script audit/benchmark và bốn trang ứng dụng.

## Cấu trúc

```text
salary-dashboard/
├── app.py
├── data/Employers_data.csv
├── pages/
│   ├── 1_Overview.py
│   ├── 2_Salary_Analysis.py
│   ├── 3_Experience_Insights.py
│   └── 4_Data_Explorer.py
├── utils/
│   ├── charts.py
│   ├── config.py
│   ├── data_loader.py
│   ├── data_processing.py
│   ├── filters.py
│   ├── metrics.py
│   ├── modeling.py
│   └── ui.py
├── tests/
├── scripts/
│   ├── audit_data.py
│   └── benchmark_core.py
└── docs/
```

## Giới hạn sử dụng

- Đơn vị tiền tệ, kỳ trả lương, nguồn gốc và cách tạo dữ liệu chưa được xác thực.
- Mọi nhận xét chỉ mô tả bộ dữ liệu hiện tại, không đại diện cho thị trường lao động.
- Hồi quy tuyến tính là minh họa học thuật, không dùng để quyết định lương thực tế.
- CSV chứa tên và thuộc tính nhân viên; cần ẩn dữ liệu định danh trước khi công khai.
