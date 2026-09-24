import pytest

from utils.config import DATA_PATH
from utils.data_loader import load_data, validate_data
from utils.metrics import calculate_kpis, salary_summary_by


def test_full_dataset_kpis_match_project_plan() -> None:
    data = load_data(DATA_PATH)
    kpis = calculate_kpis(data)

    assert kpis["employee_count"] == 10_000
    assert kpis["average_salary"] == pytest.approx(115_381.5)
    assert kpis["median_salary"] == pytest.approx(120_000)
    assert kpis["minimum_salary"] == 25_000
    assert kpis["maximum_salary"] == 215_000


def test_empty_dataframe_kpis(sample_data) -> None:
    empty = validate_data(sample_data).iloc[0:0]
    kpis = calculate_kpis(empty)
    assert kpis["employee_count"] == 0
    assert kpis["average_salary"] is None


def test_salary_summary_reports_sample_size(sample_data) -> None:
    data = validate_data(sample_data)
    summary = salary_summary_by(data, "Department")
    assert set(summary.columns) == {"Department", "count", "mean", "median", "min", "max", "std"}
    assert int(summary["count"].sum()) == len(data)
