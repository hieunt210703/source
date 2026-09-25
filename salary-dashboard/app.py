import streamlit as st

from utils.ui import inject_global_css, load_prepared_data, render_sidebar_filters


st.set_page_config(
    page_title="Phân tích lương nhân viên",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="auto",
)
inject_global_css()

# Sidebar được render tại entrypoint để widget có cùng identity trên mọi page.
# Các page chỉ đọc shared_filter_spec và áp dụng lên cùng dataset đã cache.
shared_data = load_prepared_data()
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
