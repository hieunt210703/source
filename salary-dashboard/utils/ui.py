from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.config import DATA_PATH
from utils.data_loader import DataValidationError, load_data
from utils.data_processing import prepare_data
from utils.filters import FilterSpec, apply_filters


NAV_ITEMS = (
    ("overview", "Tổng quan", "pages/1_Overview.py"),
    ("salary", "Phân tích lương", "pages/2_Salary_Analysis.py"),
    ("experience", "Kinh nghiệm", "pages/3_Experience_Insights.py"),
    ("explorer", "Khám phá dữ liệu", "pages/4_Data_Explorer.py"),
)

FILTER_KEYS = (
    "filter_departments",
    "filter_job_titles",
    "filter_education",
    "filter_locations",
    "filter_genders",
    "filter_salary",
    "filter_experience",
)


def inject_global_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --navy: #0B1739;
            --blue: #1769E0;
            --teal: #079A92;
            --amber: #F4A621;
            --muted: #5F6F89;
            --border: #DCE5F0;
            --surface: #FFFFFF;
            --canvas: #F7F9FC;
        }

        .stApp { background: var(--canvas); color: var(--navy); }
        [data-testid="stHeader"] { background: transparent; height: 0; }
        [data-testid="stToolbar"] { visibility: hidden; }
        [data-testid="stDecoration"] { display: none; }
        [data-testid="stMainBlockContainer"] {
            max-width: 1480px;
            padding: 0.3rem 2rem 3rem;
        }
        [data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid var(--border);
            min-width: 282px;
            max-width: 282px;
        }
        [data-testid="stSidebarContent"] { padding-top: 1rem; }
        [data-testid="stSidebar"] h2 {
            color: var(--navy);
            font-size: 1.15rem;
            letter-spacing: -0.01em;
        }
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] button {
            font-size: 0.86rem;
        }
        [data-baseweb="select"] > div,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextInput"] input {
            border-color: var(--border) !important;
            border-radius: 10px !important;
        }
        span[data-baseweb="tag"] { background: #EAF3FF !important; color: var(--blue) !important; }
        [data-testid="stSlider"] [role="slider"] { background: var(--blue); }

        .top-shell {
            display: flex;
            align-items: center;
            min-height: 48px;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.28rem;
            font-weight: 750;
            letter-spacing: -0.025em;
            color: var(--navy);
            white-space: nowrap;
        }
        .brand-mark {
            display: inline-flex;
            align-items: flex-end;
            gap: 3px;
            height: 24px;
        }
        .brand-mark i { width: 5px; border-radius: 2px 2px 0 0; display: block; }
        .brand-mark i:nth-child(1) { height: 12px; background: var(--blue); }
        .brand-mark i:nth-child(2) { height: 20px; background: var(--teal); }
        .brand-mark i:nth-child(3) { height: 25px; background: #64A8F6; }
        .top-divider { border-top: 1px solid var(--border); margin: 0.15rem -2rem 1.25rem; }

        div[data-testid="stPageLink"] a {
            color: var(--muted) !important;
            text-decoration: none !important;
            font-size: 0.92rem !important;
            font-weight: 600 !important;
            justify-content: center !important;
            border-radius: 0 !important;
            padding: 0.7rem 0.25rem !important;
            border-bottom: 2px solid transparent !important;
        }
        div[data-testid="stPageLink"] a:hover {
            color: var(--blue) !important;
            background: transparent !important;
            border-bottom-color: #B9D7FF !important;
        }
        .nav-active {
            color: var(--blue);
            font-size: 0.92rem;
            font-weight: 700;
            text-align: center;
            padding: 0.7rem 0.25rem;
            border-bottom: 2px solid var(--blue);
            white-space: nowrap;
        }

        .page-heading-row {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 24px;
            margin: 0.1rem 0 1.15rem;
        }
        .page-heading h1 {
            color: var(--navy);
            font-size: clamp(1.8rem, 2.7vw, 2.45rem);
            line-height: 1.08;
            letter-spacing: -0.035em;
            margin: 0;
        }
        .page-heading p { color: var(--muted); margin: 0.45rem 0 0; font-size: 0.92rem; }
        .record-count { color: var(--muted); font-size: 0.85rem; white-space: nowrap; padding-bottom: 0.25rem; }

        .kpi-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem 1.05rem 0.9rem;
            min-height: 108px;
        }
        .kpi-card .label { color: var(--muted); font-size: 0.83rem; font-weight: 600; }
        .kpi-card .value {
            color: var(--navy);
            display: block;
            font-size: clamp(1.42rem, 2vw, 2rem);
            line-height: 1.1;
            letter-spacing: -0.035em;
            font-weight: 760;
            margin-top: 0.62rem;
        }
        .kpi-card.compact { min-height: 104px; padding: 0.9rem 0.8rem 0.75rem; }
        .kpi-card.compact .label { font-size: 0.75rem; }
        .kpi-card.compact .value { font-size: clamp(1.28rem, 1.65vw, 1.65rem); }
        .analysis-note {
            background: #F0F7FF;
            border-left: 3px solid var(--blue);
            color: #304A6B;
            padding: 0.78rem 0.95rem;
            border-radius: 0 9px 9px 0;
            font-size: 0.86rem;
            margin: 0.2rem 0 1rem;
        }
        .equation-panel {
            border: 1px solid var(--border);
            border-radius: 12px;
            background: #F7FAFF;
            padding: 1rem 1.15rem;
            min-height: 108px;
        }
        .equation-panel .eyeline { color: var(--muted); font-size: 0.78rem; font-weight: 650; }
        .equation-panel .equation { color: var(--blue); font-size: 0.95rem; font-weight: 750; margin: 0.5rem 0; }
        .equation-panel .subnote { color: var(--muted); font-size: 0.78rem; }
        .empty-state {
            border: 1px dashed #B9C7D8;
            border-radius: 12px;
            background: #FFFFFF;
            padding: 3rem 1.5rem;
            text-align: center;
            color: var(--muted);
        }
        .empty-state strong { color: var(--navy); display: block; margin-bottom: 0.4rem; }
        .section-heading {
            color: var(--navy);
            font-size: 1.2rem;
            font-weight: 740;
            letter-spacing: -0.015em;
            margin: 1.2rem 0 0.55rem;
        }
        div[data-testid="stPlotlyChart"] {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
        }
        [data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
        .stButton > button, .stDownloadButton > button {
            border-radius: 10px;
            border-color: #B9C7D8;
            font-weight: 650;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            border-color: var(--blue);
            color: var(--blue);
        }
        @media (max-width: 900px) {
            [data-testid="stMainBlockContainer"] { padding: 0.75rem 1rem 2rem; }
            .brand > span:last-child { display: none; }
            .brand-mark { display: inline-flex; }
            .st-key-top_navigation [data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-wrap: nowrap !important;
                align-items: center !important;
                gap: 0.2rem !important;
            }
            .st-key-top_navigation [data-testid="stColumn"] {
                flex: 1 1 0 !important;
                width: auto !important;
                min-width: 0 !important;
            }
            .st-key-top_navigation [data-testid="stColumn"]:first-child {
                flex: 0 0 30px !important;
            }
            .st-key-top_navigation .top-shell { min-height: 42px; }
            div[data-testid="stPageLink"] a, .nav-active { font-size: 0.7rem !important; line-height: 1.1; }
            div[data-testid="stPageLink"] a, .nav-active {
                min-height: 50px;
                padding: 0.45rem 0.1rem !important;
                white-space: normal;
            }
            .st-key-top_navigation div[data-testid="stPageLink"] p {
                font-size: 0.66rem !important;
                line-height: 1.08 !important;
                overflow: visible !important;
                text-align: center !important;
                text-overflow: clip !important;
                white-space: normal !important;
            }
            .st-key-top_navigation .nav-active {
                align-items: center;
                display: flex;
                justify-content: center;
            }
            .page-heading-row { align-items: flex-start; flex-direction: column; gap: 8px; }
            .record-count { white-space: normal; }
            .top-divider { margin-left: -1rem; margin-right: -1rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(active: str) -> None:
    with st.container(key="top_navigation"):
        columns = st.columns([2.7, 1, 1.25, 1, 1.35], vertical_alignment="center", gap="small")
        with columns[0]:
            st.markdown(
                """
                <div class="top-shell"><div class="brand">
                  <span class="brand-mark"><i></i><i></i><i></i></span>
                  <span>Phân tích lương nhân viên</span>
                </div></div>
                """,
                unsafe_allow_html=True,
            )

        for column, (key, label, path) in zip(columns[1:], NAV_ITEMS, strict=True):
            with column:
                if key == active:
                    st.markdown(f'<div class="nav-active">{escape(label)}</div>', unsafe_allow_html=True)
                else:
                    st.page_link(path, label=label, width="stretch")

    st.markdown('<div class="top-divider"></div>', unsafe_allow_html=True)


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
    st.markdown(
        f"""
        <div class="page-heading-row">
          <div class="page-heading">
            <h1>{escape(title)}</h1>
            <p>{escape(description)}</p>
          </div>
          <div class="record-count">Đang hiển thị <strong>{format_number(current)}</strong> / {format_number(total)} nhân viên</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_cards(items: list[tuple[str, str]], compact: bool = False) -> None:
    columns = st.columns(len(items), gap="small")
    card_class = "kpi-card compact" if compact else "kpi-card"
    for column, (label, value) in zip(columns, items, strict=True):
        with column:
            st.markdown(
                f'<div class="{card_class}"><span class="label">{escape(label)}</span><span class="value">{escape(value)}</span></div>',
                unsafe_allow_html=True,
            )


def render_empty_state(message: str = "Không có dữ liệu phù hợp với bộ lọc hiện tại.") -> None:
    st.markdown(
        f'<div class="empty-state"><strong>Không có dữ liệu</strong>{escape(message)}</div>',
        unsafe_allow_html=True,
    )


def render_section_heading(title: str) -> None:
    st.markdown(f'<div class="section-heading">{escape(title)}</div>', unsafe_allow_html=True)


def load_prepared_data(path: str | Path = DATA_PATH) -> pd.DataFrame:
    try:
        return prepare_data(load_data(path))
    except DataValidationError as error:
        st.error(str(error), icon="🚫")
        st.stop()


def _sorted_values(df: pd.DataFrame, column: str) -> list[str]:
    return sorted(df[column].dropna().astype(str).unique().tolist())


def render_sidebar_filters(df: pd.DataFrame) -> tuple[FilterSpec, pd.DataFrame]:
    with st.sidebar:
        st.markdown("## Bộ lọc dữ liệu")
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
        genders = st.multiselect(
            "Giới tính",
            _sorted_values(df, "Gender"),
            key="filter_genders",
            placeholder="Tất cả giới tính",
        )

        salary_min, salary_max = int(df["Salary"].min()), int(df["Salary"].max())
        salary_range = st.slider(
            "Khoảng lương",
            min_value=salary_min,
            max_value=salary_max,
            value=(salary_min, salary_max),
            step=5_000,
            key="filter_salary",
        )
        experience_min = int(df["Experience_Years"].min())
        experience_max = int(df["Experience_Years"].max())
        experience_range = st.slider(
            "Số năm kinh nghiệm",
            min_value=experience_min,
            max_value=experience_max,
            value=(experience_min, experience_max),
            key="filter_experience",
        )

        if st.button("Đặt lại bộ lọc", width="stretch", icon=":material/restart_alt:"):
            for key in FILTER_KEYS:
                st.session_state.pop(key, None)
            st.rerun()

    spec = FilterSpec(
        departments=tuple(departments),
        job_titles=tuple(job_titles),
        education_levels=tuple(education),
        locations=tuple(locations),
        genders=tuple(genders),
        salary_range=salary_range,
        experience_range=experience_range,
    )
    return spec, apply_filters(df, spec)
