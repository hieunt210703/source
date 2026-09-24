from utils.charts import (
    age_group_bar,
    age_scatter,
    comparison_bar,
    department_donut,
    department_salary_bar,
    experience_group_bar,
    experience_scatter,
    residual_plot,
    salary_boxplot,
    salary_histogram,
)
from utils.data_loader import validate_data
from utils.data_processing import prepare_data
from utils.modeling import fit_simple_linear_regression


def test_all_chart_builders_return_figures(sample_data) -> None:
    data = prepare_data(validate_data(sample_data))
    model_data = data.loc[data.index.repeat(4)].reset_index(drop=True)
    model = fit_simple_linear_regression(model_data)
    figures = [
        salary_histogram(data),
        department_donut(data),
        department_salary_bar(data),
        comparison_bar(data, "Department"),
        salary_boxplot(data, "Department"),
        experience_scatter(model_data, model),
        experience_group_bar(data),
        residual_plot(model),
        age_scatter(data),
        age_group_bar(data),
    ]
    assert all(len(figure.data) > 0 for figure in figures)
