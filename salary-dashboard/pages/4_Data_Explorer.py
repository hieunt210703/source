import re

import streamlit as st

from utils.config import REQUIRED_COLUMNS
from utils.filters import FilterSpec, apply_filters
from utils.ui import (
    format_number,
    load_prepared_data,
    render_empty_state,
    render_header,
    render_page_heading,
)


data = load_prepared_data()
filtered = apply_filters(
    data,
    st.session_state.get("shared_filter_spec", FilterSpec()),
)
render_header("explorer")
render_page_heading(
    "Khám phá dữ liệu",
    "Tra cứu nhân viên, kiểm tra bản ghi và xuất đúng tập dữ liệu đang hiển thị.",
    len(filtered),
    len(data),
)

search_column, options_column = st.columns([1.15, 1.85], gap="medium")
with search_column:
    search = st.text_input(
        "Tìm theo Employee_ID hoặc Name",
        placeholder="Ví dụ: 1024 hoặc Nguyen",
        icon=":material/search:",
    ).strip()
with options_column:
    selected_columns = st.multiselect(
        "Cột hiển thị",
        list(REQUIRED_COLUMNS),
        default=list(REQUIRED_COLUMNS),
    )

result = filtered
if search:
    escaped_search = re.escape(search)
    id_matches = result["Employee_ID"].astype(str).str.contains(escaped_search, case=False, regex=True)
    name_matches = result["Name"].str.contains(escaped_search, case=False, regex=True, na=False)
    result = result.loc[id_matches | name_matches].copy()

if result.empty:
    render_empty_state("Không tìm thấy bản ghi phù hợp với bộ lọc hoặc từ khóa.")
    st.stop()

if not selected_columns:
    st.info("Hãy chọn ít nhất một cột để hiển thị.", icon="ℹ️")
    st.stop()

display = result.loc[:, selected_columns]
action_left, action_right = st.columns([3, 1], vertical_alignment="center")
with action_left:
    st.caption(f"Tìm thấy {format_number(len(display))} bản ghi. Tên có thể trùng; Employee_ID là định danh duy nhất.")
with action_right:
    st.download_button(
        "Tải CSV đang hiển thị",
        data=display.to_csv(index=False).encode("utf-8-sig"),
        file_name="salary_filtered.csv",
        mime="text/csv",
        width="stretch",
        icon=":material/download:",
    )

st.dataframe(
    display,
    width="stretch",
    hide_index=True,
    height=610,
    column_config={
        "Employee_ID": st.column_config.NumberColumn("Employee ID", format="%d"),
        "Age": st.column_config.NumberColumn("Tuổi", format="%d"),
        "Experience_Years": st.column_config.NumberColumn("Kinh nghiệm", format="%d năm"),
        "Salary": st.column_config.NumberColumn("Mức lương", format="localized"),
    },
)
st.warning(
    "Dữ liệu có tên cá nhân và thuộc tính lương. Cần xem xét ẩn định danh trước khi chia sẻ công khai.",
    icon="🔒",
)
