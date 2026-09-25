import streamlit as st

from utils.config import REQUIRED_COLUMNS
from utils.data_loader import DataValidationError
from utils.ui import (
    activate_uploaded_data,
    clear_upload_state,
    format_number,
    inject_global_css,
    render_sidebar_filters,
)


st.set_page_config(
    page_title="Phân tích lương nhân viên",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="auto",
)
inject_global_css()

if "uploaded_data" not in st.session_state:
    st.title("Phân tích lương nhân viên")
    st.caption("Tải file CSV nhân viên để xem các chỉ số, biểu đồ và bộ lọc.")

current_file = st.session_state.get("uploaded_filename")
with st.expander(
    "Tải hoặc thay file CSV nhân viên",
    expanded=current_file is None,
    icon=":material/upload_file:",
):
    uploaded_file = st.file_uploader(
        "Chọn file CSV",
        type="csv",
        key="employee_upload",
        help="File CSV mã hóa UTF-8, phân tách bằng dấu phẩy.",
    )
    st.caption("Cột bắt buộc: " + ", ".join(REQUIRED_COLUMNS) + ".")

if uploaded_file is None:
    if "uploaded_data" in st.session_state:
        clear_upload_state()
    st.info("Chọn file CSV hợp lệ để bắt đầu phân tích.", icon=":material/info:")
    st.stop()

try:
    shared_data = activate_uploaded_data(uploaded_file.name, uploaded_file.getvalue())
except DataValidationError as error:
    clear_upload_state()
    st.error(str(error), icon=":material/error:")
    st.stop()

st.caption(f"Đã tải {uploaded_file.name}: {format_number(len(shared_data))} bản ghi hợp lệ.")

# Widget bộ lọc ở entrypoint để giữ trạng thái khi chuyển giữa bốn trang.
render_sidebar_filters(shared_data)

navigation = st.navigation(
    [
        st.Page("pages/1_Overview.py", title="Tổng quan", default=True),
        st.Page("pages/2_Salary_Analysis.py", title="Phân tích lương"),
        st.Page("pages/3_Experience_Insights.py", title="Kinh nghiệm"),
        st.Page("pages/4_Data_Explorer.py", title="Khám phá dữ liệu"),
    ],
    position="hidden",
)
navigation.run()
