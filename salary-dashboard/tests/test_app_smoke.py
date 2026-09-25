import ast
import importlib
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pandas as pd

from streamlit.testing.v1 import AppTest

from utils.config import DATA_PATH


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_default_page_waits_for_uploaded_file() -> None:
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=30).run()
    assert not app.exception
    assert len(app.get("file_uploader")) == 1
    assert not app.metric
    assert not app.get("plotly_chart")


def _uploaded_file(name: str, contents: bytes) -> SimpleNamespace:
    return SimpleNamespace(name=name, getvalue=lambda: contents)


def test_valid_upload_opens_all_four_pages() -> None:
    uploaded = _uploaded_file("employees.csv", DATA_PATH.read_bytes())
    with patch("streamlit.file_uploader", return_value=uploaded):
        app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=30).run()

    assert not app.exception
    assert len(app.metric) == 5
    assert len(app.session_state["uploaded_data"]) == 10_000

    for page_path in (
        "pages/2_Salary_Analysis.py",
        "pages/3_Experience_Insights.py",
        "pages/4_Data_Explorer.py",
    ):
        app.switch_page(page_path).run()
        assert not app.exception, page_path


def test_replacing_upload_resets_filters_even_for_one_row(sample_data: pd.DataFrame) -> None:
    original = _uploaded_file("original.csv", DATA_PATH.read_bytes())
    replacement = _uploaded_file(
        "one_row.csv", sample_data.iloc[[0]].to_csv(index=False).encode("utf-8")
    )
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=30)

    with patch("streamlit.file_uploader", return_value=original):
        app.run()
        app.multiselect(key="filter_departments").set_value(["Engineering"]).run()
    assert app.session_state["shared_filter_spec"].departments == ("Engineering",)

    with patch("streamlit.file_uploader", return_value=replacement):
        app.run()
    assert not app.exception
    assert app.metric[0].value == "1"
    assert app.session_state["shared_filter_spec"].departments == ()


def test_invalid_upload_does_not_show_dashboard(sample_data: pd.DataFrame) -> None:
    missing_salary = sample_data.drop(columns=["Salary"])
    uploaded = _uploaded_file(
        "invalid.csv", missing_salary.to_csv(index=False).encode("utf-8")
    )
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=30)
    with patch(
        "streamlit.file_uploader",
        return_value=_uploaded_file("valid.csv", DATA_PATH.read_bytes()),
    ):
        app.run()
    assert len(app.metric) == 5

    with patch("streamlit.file_uploader", return_value=uploaded):
        app.run()

    assert not app.exception
    assert app.error
    assert not app.metric
    assert "uploaded_data" not in app.session_state


def test_all_page_internal_imports_are_available() -> None:
    page_paths = [
        "pages/1_Overview.py",
        "pages/2_Salary_Analysis.py",
        "pages/3_Experience_Insights.py",
        "pages/4_Data_Explorer.py",
    ]

    for page_path in page_paths:
        tree = ast.parse((PROJECT_ROOT / page_path).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or not node.module:
                continue
            if not node.module.startswith("utils."):
                continue

            module = importlib.import_module(node.module)
            missing_names = [
                alias.name for alias in node.names if not hasattr(module, alias.name)
            ]
            assert not missing_names, (
                f"{page_path} import tên không tồn tại từ {node.module}: "
                f"{missing_names}"
            )
