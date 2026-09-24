import streamlit as st

from utils.charts import comparison_bar, salary_boxplot
from utils.config import DIMENSION_LABELS
from utils.ui import (
    load_prepared_data,
    render_empty_state,
    render_header,
    render_page_heading,
    render_section_heading,
    render_sidebar_filters,
)


data = load_prepared_data()
_, filtered = render_sidebar_filters(data)
render_header("salary")
render_page_heading(
    "Phân tích lương",
    "So sánh trung bình, trung vị, cỡ mẫu và độ phân tán giữa các nhóm.",
    len(filtered),
    len(data),
)

if filtered.empty:
    render_empty_state()
    st.stop()

dimensions = ["Department", "Job_Title", "Education_Level", "Location"]
for index in range(0, len(dimensions), 2):
    columns = st.columns(2, gap="medium")
    for column, dimension in zip(columns, dimensions[index : index + 2], strict=False):
        with column:
            st.plotly_chart(
                comparison_bar(filtered, dimension),
                width="stretch",
                config={"displayModeBar": False},
            )

render_section_heading("Độ phân tán và ngoại lệ")
box_dimension = st.selectbox(
    "Chọn chiều phân nhóm cho box plot",
    dimensions,
    format_func=lambda value: DIMENSION_LABELS[value],
)
st.plotly_chart(
    salary_boxplot(filtered, box_dimension),
    width="stretch",
    config={"displayModeBar": False},
)
st.markdown(
    '<div class="analysis-note">Đường giữa hộp là trung vị; hộp thể hiện Q1–Q3. Điểm nằm ngoài râu hộp là ứng viên ngoại lệ theo từng nhóm, không tự động bị loại khỏi dữ liệu.</div>',
    unsafe_allow_html=True,
)
