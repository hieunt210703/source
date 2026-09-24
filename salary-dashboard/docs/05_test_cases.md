# Test cases

| Nhóm | Tình huống |
|---|---|
| Loader | CSV hợp lệ; thiếu file; thiếu cột; ID trùng |
| Processing | Nhóm kinh nghiệm và nhóm tuổi đúng biên |
| KPI | Full dataset; dataframe rỗng; tổng hợp theo nhóm |
| Filter | Không lọc; nhiều điều kiện; tổ hợp không có dữ liệu |
| Modeling | Đường tuyến tính hoàn hảo; dữ liệu thật; quá ít bản ghi |
| Charts | Tất cả chart builder trả về Plotly figure có dữ liệu |
| App | Trang mặc định chạy không có Streamlit exception |

Kiểm thử giao diện thủ công bổ sung: chuyển trang, thay bộ lọc, reset, empty state, search và CSV download.
