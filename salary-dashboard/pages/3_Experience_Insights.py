from html import escape

import streamlit as st

from utils.charts import (
    age_group_bar,
    age_scatter,
    experience_group_bar,
    experience_scatter,
    residual_plot,
)
from utils.filters import FilterSpec, apply_filters
from utils.modeling import ModelingError, fit_simple_linear_regression, pearson_correlation
from utils.ui import (
    format_number,
    format_pvalue,
    load_prepared_data,
    render_empty_state,
    render_header,
    render_kpi_cards,
    render_page_heading,
    render_section_heading,
)


data = load_prepared_data()
filtered = apply_filters(
    data,
    st.session_state.get("shared_filter_spec", FilterSpec()),
)
render_header("experience")
render_page_heading(
    "Kinh nghiệm và mức lương",
    "Khám phá mối liên hệ và đánh giá một hồi quy tuyến tính đơn biến trên tập kiểm thử.",
    len(filtered),
    len(data),
)

if filtered.empty:
    render_empty_state()
    st.stop()

model_result = None
pearson_result = None
model_error = None
try:
    pearson_result = pearson_correlation(filtered)
    model_result = fit_simple_linear_regression(filtered)
except ModelingError as error:
    model_error = str(error)

left, right = st.columns([1.35, 1], gap="medium")
with left:
    st.plotly_chart(
        experience_scatter(filtered, model_result),
        width="stretch",
        config={"displayModeBar": False},
    )
with right:
    st.plotly_chart(
        experience_group_bar(filtered),
        width="stretch",
        config={"displayModeBar": False},
    )

render_section_heading("Hồi quy tuyến tính đơn biến")
if model_error or model_result is None or pearson_result is None:
    st.warning(model_error or "Không thể xây dựng mô hình với bộ lọc hiện tại.", icon="⚠️")
else:
    pearson_r, p_value = pearson_result
    equation = (
        f"Salary = {format_number(model_result.intercept, 1)} "
        f"{'+' if model_result.coefficient >= 0 else '−'} "
        f"{format_number(abs(model_result.coefficient), 1)} × Experience_Years"
    )
    equation_column, metrics_column = st.columns([1.55, 3.45], gap="small")
    with equation_column:
        st.markdown(
            f"""
            <div class="equation-panel">
              <div class="eyeline">PHƯƠNG TRÌNH TRÊN TẬP TRAIN</div>
              <div class="equation">{escape(equation)}</div>
              <div class="subnote">Mô hình chỉ mang tính minh họa trên bộ dữ liệu hiện tại.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with metrics_column:
        render_kpi_cards(
            [
                ("Pearson r", format_number(pearson_r, 3)),
                ("p-value", format_pvalue(p_value)),
                ("R² train", format_number(model_result.train_r2, 3)),
                ("R² test", format_number(model_result.test_r2, 3)),
                ("MAE", format_number(model_result.mae)),
                ("RMSE", format_number(model_result.rmse)),
            ],
            compact=True,
        )
    st.plotly_chart(
        residual_plot(model_result),
        width="stretch",
        config={"displayModeBar": False},
    )
    st.markdown(
        '<div class="analysis-note">Mô hình được fit trên 80% dữ liệu và đánh giá trên 20% dữ liệu còn lại với <code>random_state=42</code>. Kết quả mô tả liên hệ tuyến tính, không chứng minh kinh nghiệm là nguyên nhân trực tiếp quyết định lương.</div>',
        unsafe_allow_html=True,
    )

render_section_heading("Độ tuổi và mức lương")
age_left, age_right = st.columns(2, gap="medium")
with age_left:
    st.plotly_chart(age_scatter(filtered), width="stretch", config={"displayModeBar": False})
with age_right:
    st.plotly_chart(age_group_bar(filtered), width="stretch", config={"displayModeBar": False})
st.caption("Tuổi và số năm kinh nghiệm có tương quan rất cao trong dữ liệu này; không diễn giải chúng như hai tác nhân độc lập.")
