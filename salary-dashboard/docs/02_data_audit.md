# Data audit

Nguồn kiểm tra: `data/Employers_data.csv`.

Tái tạo kết quả từ thư mục gốc dự án:

```powershell
python scripts/audit_data.py
```

| Kiểm tra | Kết quả |
|---|---:|
| Số dòng | 10.000 |
| Số cột | 10 |
| Giá trị thiếu | 0 |
| Dòng trùng hoàn toàn | 0 |
| Employee_ID trùng | 0 |
| Employee_ID duy nhất | Có |
| Salary min | 25.000 |
| Salary max | 215.000 |
| Salary mean | 115.381,5 |
| Salary median | 120.000 |

## Kiểm tra chất lượng bổ sung

- Không có lương không dương, tuổi ngoài 15–100 hoặc kinh nghiệm âm.
- Không có `Experience_Years > Age`.
- Chuỗi không có giá trị rỗng hoặc khoảng trắng thừa đầu/cuối.
- Có 9.868 tên duy nhất; tên không phải định danh. `Employee_ID` mới là khóa tra cứu duy nhất.
- Salary có 39 mức, đều là bội số của 5.000; dữ liệu có cấu trúc rời rạc và có khả năng được tổng hợp/sinh theo quy tắc.

## Rủi ro dữ liệu

Chưa xác thực đơn vị tiền tệ, kỳ trả lương, nguồn gốc và phương pháp thu thập. Không suy diễn kết quả thành kết luận về thị trường lao động hoặc quan hệ nhân quả.
