import streamlit as st

from utils.charts import department_donut, department_salary_bar, salary_histogram
from utils.metrics import calculate_kpis
from utils.ui import (
    apply_shared_filters,
    format_number,
    load_prepared_data,
    render_empty_state,
    render_header,
    render_kpi_cards,
    render_page_heading,
)


data = load_prepared_data()
filtered = apply_shared_filters(data)
render_header("overview")
render_page_heading(
    "Tổng quan",
    "Theo dõi quy mô, phân bố và mặt bằng lương trên cùng tập dữ liệu đã lọc.",
    len(filtered),
    len(data),
)

if filtered.empty:
    render_empty_state()
    st.stop()

kpis = calculate_kpis(filtered)
render_kpi_cards(
    [
        ("Tổng nhân viên", format_number(kpis["employee_count"])),
        ("Lương trung bình", format_number(kpis["average_salary"], 1)),
        ("Trung vị", format_number(kpis["median_salary"])),
        ("Thấp nhất", format_number(kpis["minimum_salary"])),
        ("Cao nhất", format_number(kpis["maximum_salary"])),
    ]
)

st.caption("Đơn vị lương và kỳ trả lương chưa được xác thực trong dữ liệu nguồn.")
st.plotly_chart(salary_histogram(filtered), width="stretch", config={"displayModeBar": False})

left, right = st.columns([0.9, 1.1], gap="medium")
with left:
    st.plotly_chart(department_donut(filtered), width="stretch", config={"displayModeBar": False})
with right:
    st.plotly_chart(department_salary_bar(filtered), width="stretch", config={"displayModeBar": False})
