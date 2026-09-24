# Kết quả kiểm thử

## Tự động

- Lệnh: `python -m pytest -q`
- Kết quả: **17 passed**.
- Compile: `python -m compileall -q app.py pages utils tests` thành công.

## Phạm vi đã xác nhận

- Schema và KPI khớp dữ liệu gốc.
- Filter kết hợp dùng đúng một dataframe chung.
- Hồi quy chia train/test tái lập với `random_state=42`.
- Pearson correlation và metric mô hình khớp kết quả kỳ vọng.
- Trang Streamlit mặc định không phát sinh exception trong smoke test.

## Trình duyệt

- Chạy app tại `http://127.0.0.1:8501` và kiểm tra bằng Microsoft Edge headless qua Playwright.
- Desktop: `1584 × 960`; mobile: `390 × 844`.
- Mở thành công cả 4 trang; không có Streamlit exception hay console error.
- Trang Kinh nghiệm hiển thị Pearson, phương trình hồi quy, R², MAE và RMSE.
- Tìm kiếm `Merle Ingram` tại Data Explorer trả đúng 1 bản ghi.
- Điều hướng mobile nằm trên một hàng gọn, nội dung dài xuống dòng và sidebar tự thu gọn.

In-app Browser không khả dụng trong môi trường kiểm thử (`iab` không có browser instance), nên dùng Edge headless làm phương án kiểm thử tương đương tại localhost.
