"""Tạo lại bảng audit dữ liệu từ file CSV nguồn."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.config import DATA_PATH  # noqa: E402
from utils.data_loader import validate_data  # noqa: E402
from utils.data_processing import audit_data  # noqa: E402


def build_audit_report(path: str | Path = DATA_PATH) -> dict[str, int | float | bool]:
    """Đọc, validate và trả về các số liệu audit dùng trong tài liệu dự án."""
    raw = pd.read_csv(path)
    data = validate_data(raw)
    report = audit_data(data)
    report.update(
        {
            "unique_names": int(data["Name"].nunique()),
            "salary_levels": int(data["Salary"].nunique()),
            "salary_min": int(data["Salary"].min()),
            "salary_max": int(data["Salary"].max()),
            "salary_mean": float(data["Salary"].mean()),
            "salary_median": float(data["Salary"].median()),
            "salary_all_multiples_of_5000": bool((data["Salary"] % 5_000 == 0).all()),
            "non_positive_salary_rows": int((data["Salary"] <= 0).sum()),
            "experience_greater_than_age_rows": int(
                (data["Experience_Years"] > data["Age"]).sum()
            ),
        }
    )
    return report


def main() -> None:
    print(json.dumps(build_audit_report(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
