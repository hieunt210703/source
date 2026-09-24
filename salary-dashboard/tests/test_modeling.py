import numpy as np
import pandas as pd
import pytest

from utils.config import DATA_PATH
from utils.data_loader import load_data
from utils.modeling import ModelingError, fit_simple_linear_regression, pearson_correlation


def test_simple_linear_regression_recovers_known_line() -> None:
    experience = np.arange(0, 50)
    data = pd.DataFrame(
        {
            "Experience_Years": experience,
            "Salary": 30_000 + 5_000 * experience,
        }
    )
    result = fit_simple_linear_regression(data)
    assert result.intercept == pytest.approx(30_000)
    assert result.coefficient == pytest.approx(5_000)
    assert result.train_r2 == pytest.approx(1.0)
    assert result.test_r2 == pytest.approx(1.0)
    assert result.mae == pytest.approx(0.0, abs=1e-8)
    assert result.rmse == pytest.approx(0.0, abs=1e-8)


def test_real_dataset_model_is_reproducible() -> None:
    data = load_data(DATA_PATH)
    first = fit_simple_linear_regression(data)
    second = fit_simple_linear_regression(data)
    assert first.intercept == pytest.approx(second.intercept)
    assert first.coefficient == pytest.approx(second.coefficient)
    assert first.test_r2 == pytest.approx(second.test_r2)
    assert first.test_r2 > 0.75


def test_real_dataset_pearson_result() -> None:
    data = load_data(DATA_PATH)
    coefficient, p_value = pearson_correlation(data)
    assert coefficient == pytest.approx(0.898025, abs=1e-6)
    assert p_value < 0.001


def test_model_rejects_too_few_rows() -> None:
    data = pd.DataFrame({"Experience_Years": [1, 2, 3], "Salary": [30_000, 40_000, 50_000]})
    with pytest.raises(ModelingError, match="ít nhất 20"):
        fit_simple_linear_regression(data)
