from pathlib import Path

import pandas as pd
import pytest

from utils.config import DATA_PATH, REQUIRED_COLUMNS
from utils.data_loader import DataValidationError, load_data, load_uploaded_data, validate_data
from utils.data_processing import audit_data, prepare_data


def test_real_dataset_matches_verified_baseline() -> None:
    data = load_data(DATA_PATH)
    audit = audit_data(data)

    assert data.shape == (10_000, 10)
    assert list(data.columns) == list(REQUIRED_COLUMNS)
    assert audit["missing_values"] == 0
    assert audit["duplicate_rows"] == 0
    assert audit["duplicate_employee_ids"] == 0
    assert audit["employee_id_unique"] is True


def test_validate_data_rejects_missing_required_column(sample_data: pd.DataFrame) -> None:
    invalid = sample_data.drop(columns=["Salary"])
    with pytest.raises(DataValidationError, match="Thiếu cột bắt buộc"):
        validate_data(invalid)


def test_validate_data_rejects_duplicate_employee_id(sample_data: pd.DataFrame) -> None:
    invalid = sample_data.copy()
    invalid.loc[1, "Employee_ID"] = invalid.loc[0, "Employee_ID"]
    with pytest.raises(DataValidationError, match="trùng lặp"):
        validate_data(invalid)


def test_load_data_reports_missing_file(tmp_path: Path) -> None:
    with pytest.raises(DataValidationError, match="Không tìm thấy"):
        load_data(tmp_path / "missing.csv")


def test_uploaded_csv_is_validated(sample_data: pd.DataFrame) -> None:
    uploaded = load_uploaded_data(sample_data.to_csv(index=False).encode("utf-8-sig"))
    assert uploaded.shape == sample_data.shape
    assert list(uploaded.columns) == list(REQUIRED_COLUMNS)


def test_uploaded_csv_rejects_empty_file() -> None:
    with pytest.raises(DataValidationError, match="rỗng"):
        load_uploaded_data(b"")


def test_validate_data_rejects_blank_text_and_fractional_salary(sample_data: pd.DataFrame) -> None:
    blank_name = sample_data.copy()
    blank_name.loc[0, "Name"] = "   "
    with pytest.raises(DataValidationError, match="giá trị thiếu"):
        validate_data(blank_name)

    fractional_salary = sample_data.copy()
    fractional_salary["Salary"] = fractional_salary["Salary"].astype(float)
    fractional_salary.loc[0, "Salary"] = 30_000.5
    with pytest.raises(DataValidationError, match="số nguyên"):
        validate_data(fractional_salary)


def test_prepare_data_adds_documented_groups(sample_data: pd.DataFrame) -> None:
    prepared = prepare_data(validate_data(sample_data))
    assert prepared["Experience_Group"].astype(str).tolist() == [
        "0-2",
        "3-5",
        "6-10",
        "11-20",
        "21-30",
        "31+",
    ]
    assert prepared["Age_Group"].notna().all()


def test_prepare_data_covers_full_valid_age_range(sample_data: pd.DataFrame) -> None:
    age_edges = sample_data.copy()
    age_edges.loc[0, ["Age", "Experience_Years"]] = [15, 0]
    age_edges.loc[1, ["Age", "Experience_Years"]] = [100, 37]
    prepared = prepare_data(validate_data(age_edges))
    assert prepared["Age_Group"].astype(str).iloc[:2].tolist() == ["15-20", "61-100"]
