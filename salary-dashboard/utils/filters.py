from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class FilterSpec:
    departments: tuple[str, ...] = ()
    job_titles: tuple[str, ...] = ()
    education_levels: tuple[str, ...] = ()
    locations: tuple[str, ...] = ()
    genders: tuple[str, ...] = ()
    salary_range: tuple[int, int] | None = None
    experience_range: tuple[int, int] | None = None


FILTER_COLUMN_MAP = {
    "departments": "Department",
    "job_titles": "Job_Title",
    "education_levels": "Education_Level",
    "locations": "Location",
    "genders": "Gender",
}


def apply_filters(df: pd.DataFrame, spec: FilterSpec) -> pd.DataFrame:
    """Apply every active filter to one shared dataframe."""
    mask = pd.Series(True, index=df.index)

    for attribute, column in FILTER_COLUMN_MAP.items():
        selected = getattr(spec, attribute)
        if selected:
            mask &= df[column].isin(selected)

    if spec.salary_range is not None:
        mask &= df["Salary"].between(*spec.salary_range)

    if spec.experience_range is not None:
        mask &= df["Experience_Years"].between(*spec.experience_range)

    return df.loc[mask].copy()
