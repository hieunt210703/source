"""Đo thời gian các bước lõi trên toàn bộ 10.000 bản ghi."""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path
from time import perf_counter
from typing import Callable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.config import DATA_PATH  # noqa: E402
from utils.data_loader import validate_data  # noqa: E402
from utils.data_processing import prepare_data  # noqa: E402
from utils.filters import FilterSpec, apply_filters  # noqa: E402
from utils.metrics import calculate_kpis  # noqa: E402
from utils.modeling import fit_simple_linear_regression  # noqa: E402


def _median_ms(action: Callable[[], object], repeats: int = 10) -> float:
    samples = []
    for _ in range(repeats):
        started = perf_counter()
        action()
        samples.append((perf_counter() - started) * 1_000)
    return round(statistics.median(samples), 3)


def run_benchmark() -> dict[str, int | float]:
    raw = pd.read_csv(DATA_PATH)
    data = validate_data(raw)
    prepared = prepare_data(data)
    representative_filter = FilterSpec(
        departments=("Engineering",),
        genders=("Female",),
    )

    return {
        "rows": len(data),
        "csv_read_and_validate_median_ms": _median_ms(
            lambda: validate_data(pd.read_csv(DATA_PATH))
        ),
        "prepare_data_median_ms": _median_ms(lambda: prepare_data(data)),
        "calculate_kpis_median_ms": _median_ms(lambda: calculate_kpis(prepared)),
        "combined_filter_median_ms": _median_ms(
            lambda: apply_filters(prepared, representative_filter)
        ),
        "linear_regression_median_ms": _median_ms(
            lambda: fit_simple_linear_regression(prepared), repeats=5
        ),
    }


def main() -> None:
    print(json.dumps(run_benchmark(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
