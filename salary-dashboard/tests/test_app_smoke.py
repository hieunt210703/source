from pathlib import Path

from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_default_page_starts_without_streamlit_exception() -> None:
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=30).run()
    assert not app.exception
