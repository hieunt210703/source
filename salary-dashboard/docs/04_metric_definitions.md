# Định nghĩa thang đo

| Thang đo | Định nghĩa |
|---|---|
| Tổng nhân viên | `nunique(Employee_ID)` trên dataframe sau lọc |
| Lương trung bình | `mean(Salary)` trên dataframe sau lọc |
| Trung vị | `median(Salary)` trên dataframe sau lọc |
| Thấp nhất / Cao nhất | `min(Salary)` / `max(Salary)` |
| Cỡ mẫu nhóm | Số dòng của từng nhóm sau lọc |
| Pearson r | Tương quan tuyến tính giữa `Experience_Years` và `Salary` |
| p-value | p-value hai phía của Pearson correlation |
| R² train/test | Hệ số xác định trên tập train/test |
| MAE | Trung bình trị tuyệt đối sai số trên tập test |
| RMSE | Căn bậc hai của MSE trên tập test |

## Quy tắc mô hình

- Predictor: `Experience_Years`; target: `Salary`.
- Chia 80/20 bằng `train_test_split(random_state=42)`.
- Chỉ fit trên train, chỉ báo MAE/RMSE test từ dữ liệu chưa tham gia fit.
- Không fit nếu có dưới 20 bản ghi hoặc predictor/target không có biến thiên.
