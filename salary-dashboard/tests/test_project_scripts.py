from scripts.audit_data import build_audit_report
from scripts.benchmark_core import run_benchmark


def test_reproducible_audit_matches_documented_baseline() -> None:
    report = build_audit_report()
    assert report["rows"] == 10_000
    assert report["columns"] == 10
    assert report["missing_values"] == 0
    assert report["duplicate_employee_ids"] == 0
    assert report["salary_mean"] == 115_381.5
    assert report["salary_all_multiples_of_5000"] is True


def test_benchmark_covers_core_operations() -> None:
    result = run_benchmark()
    assert result["rows"] == 10_000
    assert result["csv_read_and_validate_median_ms"] > 0
    assert result["combined_filter_median_ms"] > 0
    assert result["linear_regression_median_ms"] > 0
