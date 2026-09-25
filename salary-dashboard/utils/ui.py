from hashlib import sha256
from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.data_loader import load_uploaded_data
from utils.data_processing import prepare_data
from utils.filters import FilterSpec, apply_filters


STYLE_PATH = Path(__file__).resolve().parents[1] / "assets" / "dashboard.css"

NAV_ITEMS = (
    ("overview", "Tổng quan", "pages/1_Overview.py"),
    ("salary", "Phân tích lương", "pages/2_Salary_Analysis.py"),
    ("experience", "Kinh nghiệm", "pages/3_Experience_Insights.py"),
    ("explorer", "Khám phá dữ liệu", "pages/4_Data_Explorer.py"),
)

KPI_ICONS = {
    "Tổng nhân viên": ":material/groups:",
    "Lương trung bình": ":material/monetization_on:",
    "Trung vị": ":material/finance:",
    "Thấp nhất": ":material/south:",
    "Cao nhất": ":material/north:",
    "Pearson r": ":material/scatter_plot:",
    "p-value": ":material/function:",
    "R² train": ":material/model_training:",
    "R² test": ":material/check_circle:",
    "MAE": ":material/straighten:",
    "RMSE": ":material/analytics:",
}

CATEGORY_FILTER_KEYS = (
    "filter_departments",
    "filter_job_titles",
    "filter_education",
    "filter_locations",
    "filter_genders",
)
FILTER_STATE_KEYS = CATEGORY_FILTER_KEYS + (
    "filter_salary",
    "filter_experience",
)


def reset_filter_state(
    salary_range: tuple[int, int],
    experience_range: tuple[int, int],
) -> None:
    """Đưa widget và shared filter về giá trị mặc định trong callback."""
    for key in CATEGORY_FILTER_KEYS:
        st.session_state[key] = []
    st.session_state["filter_salary"] = salary_range
    st.session_state["filter_experience"] = experience_range
    st.session_state["shared_filter_spec"] = FilterSpec()


def clear_upload_state() -> None:
    """Bỏ dữ liệu phiên và bộ lọc khi file bị gỡ hoặc không hợp lệ."""
    keys = (
        *FILTER_STATE_KEYS,
        "shared_filter_spec",
        "uploaded_data",
        "uploaded_digest",
        "uploaded_filename",
    )
    for key in keys:
        st.session_state.pop(key, None)


def activate_uploaded_data(filename: str, contents: bytes) -> pd.DataFrame:
    """Kiểm tra file mới một lần và chia sẻ dữ liệu đã chuẩn bị giữa các trang."""
    digest = sha256(contents).hexdigest()
    if (
        digest != st.session_state.get("uploaded_digest")
        or "uploaded_data" not in st.session_state
    ):
        prepared = prepare_data(load_uploaded_data(contents))
        for key in (*FILTER_STATE_KEYS, "shared_filter_spec"):
            st.session_state.pop(key, None)
        st.session_state["uploaded_data"] = prepared
        st.session_state["uploaded_digest"] = digest
    st.session_state["uploaded_filename"] = filename
    return st.session_state["uploaded_data"]


def get_uploaded_data() -> pd.DataFrame:
    """Lấy dữ liệu đang dùng; trang con không tự đọc CSV mặc định."""
    data = st.session_state.get("uploaded_data")
    if data is None:
        st.info(
            "Hãy tải file CSV tại trang chính để bắt đầu phân tích.",
            icon=":material/upload_file:",
        )
        st.stop()
    return data


def inject_global_css() -> None:
    """Nạp phần CSS bố cục tối thiểu không thể biểu đạt bằng theme native."""
    css = STYLE_PATH.read_text(encoding="utf-8")
    st.html(f"<style>{css}</style>")


def render_header(active: str) -> None:
    with st.container(key="top_navigation"):
        columns = st.columns(
            [2.7, 1, 1.25, 1, 1.35],
            vertical_alignment="center",
            gap="small",
        )
        with columns[0]:
            st.html(
                """
                <div class="top-shell"><div class="brand">
                  <span class="brand-mark"><i></i><i></i><i></i></span>
                  <span>Phân tích lương nhân viên</span>
                </div></div>
                """
            )

        for column, (key, label, path) in zip(columns[1:], NAV_ITEMS, strict=True):
            with column:
                if key == active:
                    st.html(f'<div class="nav-active">{escape(label)}</div>')
                else:
                    st.page_link(path, label=label, width="stretch")

    st.html('<div class="top-divider"></div>')


def format_number(value: float | int | None, decimals: int = 0) -> str:
    if value is None or pd.isna(value):
        return "—"
    formatted = f"{value:,.{decimals}f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def format_pvalue(value: float) -> str:
    if value < 0.001:
        return "< 0,001"
    return format_number(value, 3)


def render_page_heading(title: str, description: str, current: int, total: int) -> None:
    st.html(
        f"""
        <div class="page-heading-row">
          <div class="page-heading">
            <h1>{escape(title)}</h1>
            <p>{escape(description)}</p>
          </div>
          <div class="record-count">Đang hiển thị <strong>{format_number(current)}</strong> / {format_number(total)} nhân viên</div>
        </div>
        """
    )


def render_kpi_cards(items: list[tuple[str, str]], compact: bool = False) -> None:
    """Hiển thị KPI bằng metric native trong rail ngang responsive."""
    key = "model_metric_rail" if compact else "kpi_rail"
    with st.container(horizontal=True, wrap=False, gap="small", key=key):
        for label, value in items:
            st.metric(
                label,
                value,
                border=True,
                icon=KPI_ICONS.get(label),
                width="stretch",
            )


def render_empty_state(message: str = "Không có dữ liệu phù hợp với bộ lọc hiện tại.") -> None:
    st.info(
        f"**Không có dữ liệu**\n\n{message}",
        icon=":material/filter_alt_off:",
    )


def render_section_heading(title: str) -> None:
    st.subheader(title)


def render_analysis_note(message: str) -> None:
    st.html(f'<div class="analysis-note">{escape(message)}</div>')


def render_model_equation(equation: str) -> None:
    with st.container(border=True, key="model_equation"):
        st.caption("PHƯƠNG TRÌNH TRÊN TẬP TRAIN")
        st.markdown(f"**:blue[{escape(equation)}]**")
        st.caption("Mô hình chỉ mang tính minh họa trên bộ dữ liệu hiện tại.")


def _sorted_values(df: pd.DataFrame, column: str) -> list[str]:
    return sorted(df[column].dropna().astype(str).unique().tolist())


def render_sidebar_filters(df: pd.DataFrame) -> tuple[FilterSpec, pd.DataFrame]:
    salary_min, salary_max = int(df["Salary"].min()), int(df["Salary"].max())
    experience_min = int(df["Experience_Years"].min())
    experience_max = int(df["Experience_Years"].max())

    with st.sidebar:
        st.header("Bộ lọc dữ liệu", icon=":material/tune:")
        st.caption("Thay đổi được áp dụng đồng thời trên cả bốn trang.")

        departments = st.multiselect(
            "Phòng ban",
            _sorted_values(df, "Department"),
            key="filter_departments",
            placeholder="Tất cả phòng ban",
        )
        job_titles = st.multiselect(
            "Chức danh",
            _sorted_values(df, "Job_Title"),
            key="filter_job_titles",
            placeholder="Tất cả chức danh",
        )
        education = st.multiselect(
            "Học vấn",
            _sorted_values(df, "Education_Level"),
            key="filter_education",
            placeholder="Tất cả trình độ",
        )
        locations = st.multiselect(
            "Địa điểm",
            _sorted_values(df, "Location"),
            key="filter_locations",
            placeholder="Tất cả địa điểm",
        )
        genders = st.pills(
            "Giới tính",
            _sorted_values(df, "Gender"),
            selection_mode="multi",
            key="filter_genders",
        )

        if salary_min == salary_max:
            st.caption(f"Khoảng lương: chỉ có {format_number(salary_min)}.")
            salary_range = (salary_min, salary_max)
        else:
            salary_range = st.slider(
                "Khoảng lương",
                min_value=salary_min,
                max_value=salary_max,
                step=5_000 if salary_max - salary_min >= 5_000 else 1,
                key="filter_salary",
                **(
                    {}
                    if "filter_salary" in st.session_state
                    else {"value": (salary_min, salary_max)}
                ),
            )
        if experience_min == experience_max:
            st.caption(f"Số năm kinh nghiệm: chỉ có {experience_min}.")
            experience_range = (experience_min, experience_max)
        else:
            experience_range = st.slider(
                "Số năm kinh nghiệm",
                min_value=experience_min,
                max_value=experience_max,
                key="filter_experience",
                **(
                    {}
                    if "filter_experience" in st.session_state
                    else {"value": (experience_min, experience_max)}
                ),
            )

        st.button(
            "Đặt lại bộ lọc",
            width="stretch",
            icon=":material/restart_alt:",
            on_click=reset_filter_state,
            args=((salary_min, salary_max), (experience_min, experience_max)),
        )

    spec = FilterSpec(
        departments=tuple(departments),
        job_titles=tuple(job_titles),
        education_levels=tuple(education),
        locations=tuple(locations),
        genders=tuple(genders or []),
        salary_range=salary_range,
        experience_range=experience_range,
    )
    filtered = apply_filters(df, spec)
    st.session_state["shared_filter_spec"] = spec

    with st.sidebar:
        st.caption(
            f":material/database: {format_number(len(filtered))} / "
            f"{format_number(len(df))} bản ghi phù hợp"
        )

    return spec, filtered
