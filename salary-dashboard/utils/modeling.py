from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


class ModelingError(ValueError):
    """Raised when the filtered data cannot support the requested model."""


@dataclass
class LinearModelResult:
    feature: str
    target: str
    intercept: float
    coefficient: float
    train_r2: float
    test_r2: float
    mae: float
    rmse: float
    line_x: np.ndarray
    line_y: np.ndarray
    test_actual: np.ndarray
    test_predicted: np.ndarray
    residuals: np.ndarray


def pearson_correlation(
    df: pd.DataFrame,
    feature: str = "Experience_Years",
    target: str = "Salary",
) -> tuple[float, float]:
    """Return Pearson r and p-value after validating sample variation."""
    clean = df[[feature, target]].dropna()
    if len(clean) < 3:
        raise ModelingError("Cần ít nhất 3 bản ghi để tính tương quan Pearson.")
    if clean[feature].nunique() < 2 or clean[target].nunique() < 2:
        raise ModelingError("Dữ liệu không có đủ biến thiên để tính tương quan.")

    result = stats.pearsonr(clean[feature], clean[target])
    return float(result.statistic), float(result.pvalue)


def fit_simple_linear_regression(
    df: pd.DataFrame,
    feature: str = "Experience_Years",
    target: str = "Salary",
    test_size: float = 0.2,
    random_state: int = 42,
    min_samples: int = 20,
) -> LinearModelResult:
    """Fit one reproducible, out-of-sample simple linear regression."""
    clean = df[[feature, target]].dropna().copy()
    if len(clean) < min_samples:
        raise ModelingError(
            f"Cần ít nhất {min_samples} bản ghi để fit mô hình; hiện có {len(clean)}."
        )
    if clean[feature].nunique() < 2 or clean[target].nunique() < 2:
        raise ModelingError("Dữ liệu không có đủ biến thiên để fit mô hình.")

    x = clean[[feature]].astype(float)
    y = clean[target].astype(float)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=test_size,
        random_state=random_state,
    )

    model = LinearRegression()
    model.fit(x_train, y_train)
    train_predicted = model.predict(x_train)
    test_predicted = model.predict(x_test)

    line_x = np.linspace(float(x[feature].min()), float(x[feature].max()), 100)
    line_y = model.predict(pd.DataFrame({feature: line_x}))

    return LinearModelResult(
        feature=feature,
        target=target,
        intercept=float(model.intercept_),
        coefficient=float(model.coef_[0]),
        train_r2=float(r2_score(y_train, train_predicted)),
        test_r2=float(r2_score(y_test, test_predicted)),
        mae=float(mean_absolute_error(y_test, test_predicted)),
        rmse=float(np.sqrt(mean_squared_error(y_test, test_predicted))),
        line_x=line_x,
        line_y=np.asarray(line_y),
        test_actual=y_test.to_numpy(),
        test_predicted=np.asarray(test_predicted),
        residuals=y_test.to_numpy() - np.asarray(test_predicted),
    )
