# Data dictionary

| Cột | Kiểu | Vai trò | Ghi chú |
|---|---|---|---|
| Employee_ID | int | Định danh | Duy nhất, dùng tra cứu |
| Name | string | Mô tả | Có thể trùng; dữ liệu định danh |
| Age | int | Biến số | Tuổi nhân viên |
| Gender | string | Phân loại | Male/Female trong dữ liệu hiện tại |
| Department | string | Phân loại | 6 phòng ban |
| Job_Title | string | Phân loại | 5 chức danh |
| Experience_Years | int | Biến số / predictor | Số năm kinh nghiệm |
| Education_Level | string | Phân loại | Bachelor/Master/PhD |
| Location | string | Phân loại | 5 địa điểm |
| Salary | int | Biến số / target | Đơn vị và kỳ lương chưa xác thực |

## Biến dẫn xuất

- `Experience_Group`: `0-2`, `3-5`, `6-10`, `11-20`, `21-30`, `31+`.
- `Age_Group`: `21-29`, `30-39`, `40-49`, `50-60`.

Hai biến dẫn xuất chỉ tồn tại trong bộ nhớ để phân tích; CSV nguồn không bị ghi đè.
