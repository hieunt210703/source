from pathlib import Path

import pandas as pd
import streamlit as st

from utils.config import DATA_PATH, NUMERIC_COLUMNS, REQUIRED_COLUMNS, TEXT_COLUMNS


class DataValidationError(ValueError):
    """Raised when the input dataset does not satisfy the dashboard schema."""


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and normalize the fixed employee dataset without mutating input."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise DataValidationError(
            "Thiếu cột bắt buộc: " + ", ".join(missing_columns)
        )

    if df.empty:
        raise DataValidationError("File dữ liệu không có bản ghi.")

    clean = df.loc[:, REQUIRED_COLUMNS].copy()

    for column in TEXT_COLUMNS:
        clean[column] = clean[column].astype("string").str.strip()

    for column in NUMERIC_COLUMNS:
        converted = pd.to_numeric(clean[column], errors="coerce")
        invalid_count = int(converted.isna().sum() - clean[column].isna().sum())
        if invalid_count > 0:
            raise DataValidationError(
                f"Cột {column} có {invalid_count} giá trị không phải số."
            )
        clean[column] = converted

    null_counts = clean.isna().sum()
    columns_with_nulls = null_counts[null_counts > 0]
    if not columns_with_nulls.empty:
        details = ", ".join(
            f"{column}: {int(count)}" for column, count in columns_with_nulls.items()
        )
        raise DataValidationError(f"Dữ liệu có giá trị thiếu ({details}).")

    if clean["Employee_ID"].duplicated().any():
        duplicate_count = int(clean["Employee_ID"].duplicated().sum())
        raise DataValidationError(
            f"Employee_ID có {duplicate_count} giá trị trùng lặp."
        )

    invalid_rules = {
        "Age phải nằm trong khoảng 15-100": ~clean["Age"].between(15, 100),
        "Experience_Years không được âm": clean["Experience_Years"] < 0,
        "Experience_Years không được lớn hơn Age": clean["Experience_Years"]
        > clean["Age"],
        "Salary phải lớn hơn 0": clean["Salary"] <= 0,
    }
    violations = [
        f"{message} ({int(mask.sum())} dòng)"
        for message, mask in invalid_rules.items()
        if mask.any()
    ]
    if violations:
        raise DataValidationError("; ".join(violations))

    numeric_columns = list(NUMERIC_COLUMNS)
    clean.loc[:, numeric_columns] = clean.loc[:, numeric_columns].astype("int64")
    return clean


@st.cache_data(show_spinner=False)
def load_data(path: str | Path = DATA_PATH) -> pd.DataFrame:
    """Load and validate the configured CSV file."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise DataValidationError(f"Không tìm thấy file dữ liệu: {csv_path}")

    try:
        raw = pd.read_csv(csv_path)
    except (OSError, UnicodeError, pd.errors.ParserError) as error:
        raise DataValidationError(f"Không thể đọc file CSV: {error}") from error

    return validate_data(raw)
