# Kết quả phân tích ban đầu

Các kết quả sau được tính trên toàn bộ 10.000 bản ghi, chưa lọc.

## Tổng quan

- Salary: min `25.000`, max `215.000`, mean `115.381,5`, median `120.000`.
- Không có outlier toàn cục theo ngưỡng IQR.
- Salary chỉ có 39 mức, cách nhau 5.000; phân phối không phải biến liên tục mượt.

## So sánh nhóm

- Mean theo chức danh tăng rõ: Intern khoảng `35.802`, Analyst `69.478`, Engineer `99.273`, Manager `135.260`, Executive `183.415`.
- Mean theo học vấn: Bachelor khoảng `69.530`, Master `134.234`, PhD `152.137`.
- Mean theo địa điểm chỉ dao động khoảng `113.437–116.649`, nhỏ hơn nhiều so với chênh lệch chức danh.
- Chỉ có 15/30 tổ hợp Department × Job_Title và 10/15 tổ hợp Education × Job_Title. So sánh phòng ban/học vấn chịu ảnh hưởng bởi cơ cấu chức danh và chỉ được diễn giải mô tả.

## Kinh nghiệm và hồi quy tuyến tính

- Pearson `r = 0,898025`, `p < 0,001`.
- Phương trình trên tập train: `Salary = 59.480,83 + 4.513,90 × Experience_Years`.
- R² train: `0,806261`; R² test: `0,807168`.
- MAE test: `16.321,09`; RMSE test: `20.160,00`.

Mô hình giải thích khoảng 80,7% biến thiên lương trên test set của chính bộ dữ liệu này. Kết quả không chứng minh quan hệ nhân quả và không được dùng để quyết định lương thực tế.

## Tuổi và kinh nghiệm

- Age–Salary Pearson `r ≈ 0,928`.
- Age–Experience Pearson `r ≈ 0,982`.

Tuổi và kinh nghiệm gần như mang thông tin trùng nhau; không diễn giải chúng như hai tác nhân độc lập.
