# Quality notes

## Hiệu năng

- Dataset 10.000 dòng phù hợp xử lý trong bộ nhớ.
- `st.cache_data` được dùng cho bước đọc/validate CSV.
- Các biểu đồ và mô hình chỉ tính lại khi trạng thái widget thay đổi.

## Trạng thái lỗi

- Loader trả thông báo tiếng Việt cho file thiếu, parse lỗi, thiếu schema, null, ID trùng hoặc miền số không hợp lệ.
- Tổ hợp filter rỗng có empty state thay vì biểu đồ lỗi.
- Hồi quy không chạy khi dưới 20 bản ghi hoặc không có biến thiên.

## An toàn dữ liệu

- Không có secret hoặc API key.
- `Name`, tuổi và lương là dữ liệu nhạy cảm; cảnh báo xuất hiện tại Data Explorer.
- File export chỉ chứa dataframe sau filter/search và các cột người dùng chọn.

## Thiết kế

Hai concept tại `docs/design/` là chuẩn tham chiếu. UI dùng nền trắng, text navy, cobalt/teal cho dữ liệu, amber dùng tiết chế, viền xám lạnh, radius 12px và không dùng ảnh raster làm giao diện.
