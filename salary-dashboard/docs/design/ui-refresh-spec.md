# Đặc tả cải tiến UI/UX

## Phạm vi

- Giữ nguyên ứng dụng Python + Streamlit, bốn trang, dữ liệu, bộ lọc và toàn bộ logic phân tích.
- Dùng `overview-refresh-desktop.png` và `overview-refresh-mobile.png` làm chuẩn trực quan.
- Cải tiến theo hướng dashboard phân tích gọn, rõ thứ bậc và dễ dùng trên màn hình hẹp.

## Nội dung được khóa

- Thương hiệu: `Phân tích lương nhân viên`.
- Điều hướng: `Tổng quan`, `Phân tích lương`, `Kinh nghiệm`, `Khám phá dữ liệu`.
- Trang Tổng quan giữ năm KPI, histogram lương, donut phòng ban và biểu đồ lương trung bình theo phòng ban.
- Không tự thêm đơn vị tiền tệ, kết luận nhân quả, số liệu hoặc khu vực chức năng mới.

## Hệ thống thiết kế

| Token | Giá trị |
|---|---|
| Canvas | `#FFFFFF` |
| Sidebar/secondary surface | `#F4F7FB` |
| Text chính | `#07152F` |
| Text phụ | `#52647F` |
| Primary | `#1769E0` |
| Teal | `#079A92` |
| Amber | `#F4A621` |
| Border | `#D8E2EF` |
| Grid | `#E8EEF6` |
| Radius | 10–12 px |
| Typography | IBM Plex Sans, fallback sans-serif |

## Thành phần và hành vi

- Header desktop: logo chữ bên trái, bốn mục điều hướng trên cùng một hàng; trạng thái active dùng đường gạch cobalt.
- Header mobile: logo chiếm hàng đầu, điều hướng ở hàng thứ hai; nhãn được phép xuống dòng có kiểm soát.
- Sidebar: chỉ chứa bộ lọc toàn cục và nút reset; giới tính dùng lựa chọn dạng pills vì chỉ có ba giá trị.
- KPI: dùng `st.metric(border=True)` trong rail ngang. Desktop hiển thị đủ năm KPI; mobile cuộn ngang thay vì xếp năm thẻ dọc.
- Biểu đồ: tiêu đề nằm trong khung biểu đồ, nền trắng, viền lạnh 1 px, không dùng bóng đậm.
- Box plot: chọn chiều phân nhóm bằng segmented control để bốn lựa chọn luôn nhìn thấy.
- Trạng thái rỗng/lỗi dùng thành phần native của Streamlit với Material Symbols.

## Responsive

- Mốc chính: 900 px cho header và 640 px cho KPI/chart typography.
- Không thu nhỏ chữ dưới mức đọc được để nhồi nội dung.
- Các cặp biểu đồ tự xếp dọc theo hành vi responsive của `st.columns`.
- Sidebar dùng cơ chế đóng/mở native của Streamlit trên mobile.

## Icon

- Logo: ba cột màu code-native hiện có.
- KPI: `groups`, `monetization_on`, `finance`, `south`, `north`.
- Filter/reset/search/download/privacy: Material Symbols native của Streamlit.

## Sai khác có chủ đích với concept

- Không triển khai status bar điện thoại hoặc hamburger vẽ trong ảnh concept; dùng chrome/sidebar toggle native của trình duyệt và Streamlit.
- Không raster hóa bất kỳ chữ, số liệu, biểu đồ hay control nào từ concept.
