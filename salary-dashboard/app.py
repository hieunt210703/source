import streamlit as st

from utils.ui import inject_global_css


st.set_page_config(
    page_title="Phân tích lương nhân viên",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
)
inject_global_css()

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
