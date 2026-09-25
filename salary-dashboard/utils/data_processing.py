import numpy as np
import pandas as pd


EXPERIENCE_LABELS = ("0-2", "3-5", "6-10", "11-20", "21-30", "31+")
AGE_LABELS = ("15-20", "21-29", "30-39", "40-49", "50-60", "61-100")


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Add documented analysis groups to a copy of the validated dataset."""
    prepared = df.copy()
    prepared["Experience_Group"] = pd.cut(
        prepared["Experience_Years"],
        bins=[-1, 2, 5, 10, 20, 30, np.inf],
        labels=EXPERIENCE_LABELS,
        ordered=True,
    )
    prepared["Age_Group"] = pd.cut(
        prepared["Age"],
        bins=[14, 20, 29, 39, 49, 60, 100],
        labels=AGE_LABELS,
        include_lowest=True,
        ordered=True,
    )
    return prepared


def audit_data(df: pd.DataFrame) -> dict[str, int | bool]:
    """Return the compact quality checks used in project documentation."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_employee_ids": int(df["Employee_ID"].duplicated().sum()),
        "employee_id_unique": bool(df["Employee_ID"].is_unique),
    }
