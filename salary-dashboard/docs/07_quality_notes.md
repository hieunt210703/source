# Quality notes

## Hiệu năng

- Dataset 10.000 dòng phù hợp xử lý trong bộ nhớ.
- File tải lên được kiểm tra một lần khi nội dung thay đổi và giữ trong `st.session_state` của phiên; CSV mẫu cho script/kiểm thử vẫn dùng `st.cache_data`.
- Các biểu đồ và mô hình chỉ tính lại khi trạng thái widget thay đổi.

Benchmark ngày 24/09/2026 trên môi trường phát triển hiện tại, lấy trung vị 10 lần chạy (hồi quy 5 lần):

| Tác vụ | Thời gian trung vị |
|---|---:|
| Đọc CSV và validate | 41,661 ms |
| Tạo nhóm phân tích | 2,514 ms |
| Tính KPI | 1,191 ms |
| Lọc Engineering + Female | 3,249 ms |
| Fit và đánh giá hồi quy | 25,177 ms |

Có thể tái chạy bằng `python scripts/benchmark_core.py`. Kết quả phụ thuộc phần cứng và tải hệ thống; các số trên chỉ là bằng chứng thực nghiệm cho bộ dữ liệu hiện tại, không phải SLA.

## Trạng thái lỗi

- Loader trả thông báo tiếng Việt cho file thiếu, parse lỗi, thiếu schema, null, ID trùng hoặc miền số không hợp lệ.
- Dashboard không hiển thị trước khi có CSV tải lên hợp lệ; đổi file đặt lại bộ lọc cũ.
- Tổ hợp filter rỗng có empty state thay vì biểu đồ lỗi.
- Hồi quy không chạy khi dưới 20 bản ghi hoặc không có biến thiên.

## An toàn dữ liệu

- Không có secret hoặc API key.
- `Name`, tuổi và lương là dữ liệu nhạy cảm; cảnh báo xuất hiện tại Data Explorer.
- File export chỉ chứa dataframe sau filter/search và các cột người dùng chọn.

## Thiết kế

Hai concept tại `docs/design/` là chuẩn tham chiếu. UI dùng nền trắng, text navy, cobalt/teal cho dữ liệu, amber dùng tiết chế, viền xám lạnh, radius 12px và không dùng ảnh raster làm giao diện.
