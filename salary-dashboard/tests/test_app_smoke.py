import ast
import importlib
from pathlib import Path

from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_default_page_starts_without_streamlit_exception() -> None:
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=30).run()
    assert not app.exception


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
