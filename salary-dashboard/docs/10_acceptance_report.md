# Biên bản nghiệm thu MVP

**Ngày kiểm tra:** 24/09/2026  
**Phiên bản:** MVP sau deploy  
**Dữ liệu:** 10.000 dòng × 10 cột

## Kết quả acceptance

| ID | Kết quả | Bằng chứng |
|---|---|---|
| AC-01 | PASS | Loader validate schema; fixture file thiếu, thiếu cột và ID trùng |
| AC-02 | PASS | 10.000 dòng; mean 115.381,5; median 120.000; min 25.000; max 215.000 |
| AC-03 | PASS | Engineering giữ 1.683 bản ghi khi chuyển Overview → Salary → Explorer |
| AC-04 | PASS | Mọi page dùng `shared_filter_spec` và một dataframe sau lọc |
| AC-05 | PASS | Overview có 5 KPI, histogram và 2 biểu đồ phòng ban |
| AC-06 | PASS | Có so sánh phòng ban, chức danh, học vấn, địa điểm và box plot |
| AC-07 | PASS | Có Pearson, phương trình, R² train/test, MAE, RMSE và residual plot |
| AC-08 | PASS | CSV tải từ filter Engineering có 1.683 dòng, tất cả Department = Engineering |
| AC-09 | PASS | Empty state và lỗi file/schema/ID được xử lý có thông báo |
| AC-10 | PASS | Pytest, compile và kiểm thử trình duyệt đều hoàn tất |
| AC-11 | PASS | README có lệnh cài/chạy; người dùng xác nhận deploy thành công |
| AC-12 | PASS | `docs/08_findings.md` và báo cáo nêu số liệu, giới hạn và cảnh báo nhân quả |

## Kiểm thử trình duyệt

- Phương án: Microsoft Edge headless qua Playwright vì in-app Browser không có browser instance.
- Desktop: 1584 × 960.
- Mobile: 390 × 844.
- Console error: 0.
- Streamlit exception: 0.
- Điều hướng: 4/4 trang mở thành công.
- Filter xuyên trang: PASS.
- Reset filter: PASS.
- Export đúng tập đang lọc: PASS.

## Kiểm tra thiết kế

| Điểm đối chiếu | Concept | Bản chạy | Kết quả |
|---|---|---|---|
| App shell | Sidebar trái, top navigation | Giữ nguyên cấu trúc | Đạt |
| Palette | Navy, cobalt, teal, amber | Khớp token thiết kế | Đạt |
| KPI | 5 KPI một hàng desktop | 5 KPI, responsive xếp dọc mobile | Đạt |
| Chart container | Nền trắng, viền lạnh, radius nhỏ | Đồng nhất trên các trang | Đạt |
| Experience | Scatter + regression, nhóm kinh nghiệm, metric | Đủ thành phần và residual plot | Đạt |
| Responsive | Điều hướng gọn, nội dung không tràn | Kiểm tra 390 × 844 | Đạt |

Above-the-fold giữ nguyên tên dashboard, bốn nhãn điều hướng, tiêu đề trang và nhãn KPI. Bản chạy bổ sung mô tả trang, số bản ghi đang hiển thị và cảnh báo đơn vị chưa xác thực để phục vụ nghiệp vụ. Đây là các sai khác có chủ đích.

## Issue còn lại

Không có bug blocker hoặc critical. Rủi ro còn mở:

1. Chưa lưu URL deploy trong repository.
2. Chưa xác nhận CSV là dữ liệu giả lập; nếu app/repository public, cần cân nhắc ẩn danh `Name`.
3. Đơn vị và kỳ trả lương chưa được xác thực.

## Kết luận

MVP đạt 12/12 acceptance criteria. Hồi quy tuyến tính đơn biến được giữ đúng phạm vi; không bổ sung mô hình nâng cao. Phiên bản hiện tại đủ điều kiện demo và bàn giao với các giới hạn dữ liệu đã ghi rõ.
