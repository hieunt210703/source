# Employee Salary Analytics Dashboard

Ứng dụng Streamlit phân tích bộ dữ liệu 10.000 nhân viên, cung cấp KPI, biểu đồ tương tác, bộ lọc dùng chung, tra cứu/xuất CSV và một mô hình hồi quy tuyến tính đơn biến minh họa mối liên hệ giữa số năm kinh nghiệm và mức lương.

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

## Kiểm thử

```powershell
python -m pytest -q
```

Test bao phủ schema loader, KPI chuẩn, filter kết hợp, nhóm tuổi/kinh nghiệm, biểu đồ, Pearson correlation, hồi quy tuyến tính và smoke test trang mặc định.

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
└── docs/
```

## Giới hạn sử dụng

- Đơn vị tiền tệ, kỳ trả lương, nguồn gốc và cách tạo dữ liệu chưa được xác thực.
- Mọi nhận xét chỉ mô tả bộ dữ liệu hiện tại, không đại diện cho thị trường lao động.
- Hồi quy tuyến tính là minh họa học thuật, không dùng để quyết định lương thực tế.
- CSV chứa tên và thuộc tính nhân viên; cần ẩn dữ liệu định danh trước khi công khai.
