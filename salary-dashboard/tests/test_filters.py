from utils.data_loader import validate_data
from utils.filters import FilterSpec, apply_filters


def test_combined_filters_use_one_shared_dataframe(sample_data) -> None:
    data = validate_data(sample_data)
    spec = FilterSpec(
        departments=("Finance",),
        education_levels=("Master", "PhD"),
        salary_range=(100_000, 180_000),
        experience_range=(10, 30),
    )
    filtered = apply_filters(data, spec)
    assert filtered["Employee_ID"].tolist() == [4, 5]


def test_empty_selection_means_all_values(sample_data) -> None:
    data = validate_data(sample_data)
    filtered = apply_filters(data, FilterSpec())
    assert filtered.equals(data)


def test_impossible_filter_returns_empty_dataframe(sample_data) -> None:
    data = validate_data(sample_data)
    spec = FilterSpec(departments=("HR",), job_titles=("Executive",))
    assert apply_filters(data, spec).empty
