import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict[str, float | int | None]:
    """Calculate the dashboard KPIs from the current filtered dataframe."""
    if df.empty:
        return {
            "employee_count": 0,
            "average_salary": None,
            "median_salary": None,
            "minimum_salary": None,
            "maximum_salary": None,
        }

    salary = df["Salary"]
    return {
        "employee_count": int(df["Employee_ID"].nunique()),
        "average_salary": float(salary.mean()),
        "median_salary": float(salary.median()),
        "minimum_salary": int(salary.min()),
        "maximum_salary": int(salary.max()),
    }


def salary_summary_by(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Summarize salary and sample size by one categorical dimension."""
    if df.empty:
        return pd.DataFrame(
            columns=[dimension, "count", "mean", "median", "min", "max", "std"]
        )

    summary = (
        df.groupby(dimension, observed=True)["Salary"]
        .agg(count="size", mean="mean", median="median", min="min", max="max", std="std")
        .reset_index()
        .sort_values("mean", ascending=False)
    )
    return summary
