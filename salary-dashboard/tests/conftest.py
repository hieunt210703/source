from pathlib import Path
import sys

import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Employee_ID": [1, 2, 3, 4, 5, 6],
            "Name": ["An", "Bình", "Chi", "Dũng", "Hà", "Lan"],
            "Age": [22, 27, 32, 38, 45, 52],
            "Gender": ["Female", "Male", "Female", "Male", "Female", "Female"],
            "Department": ["HR", "Engineering", "HR", "Finance", "Finance", "Engineering"],
            "Job_Title": ["Intern", "Engineer", "Analyst", "Manager", "Manager", "Executive"],
            "Experience_Years": [1, 4, 8, 15, 23, 31],
            "Education_Level": ["Bachelor", "Bachelor", "Master", "Master", "PhD", "PhD"],
            "Location": ["Austin", "Seattle", "Austin", "Chicago", "Chicago", "Seattle"],
            "Salary": [30_000, 70_000, 80_000, 120_000, 155_000, 200_000],
        }
    )
