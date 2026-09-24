from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "Employers_data.csv"

REQUIRED_COLUMNS = (
    "Employee_ID",
    "Name",
    "Age",
    "Gender",
    "Department",
    "Job_Title",
    "Experience_Years",
    "Education_Level",
    "Location",
    "Salary",
)

NUMERIC_COLUMNS = ("Employee_ID", "Age", "Experience_Years", "Salary")
TEXT_COLUMNS = (
    "Name",
    "Gender",
    "Department",
    "Job_Title",
    "Education_Level",
    "Location",
)

DIMENSION_LABELS = {
    "Department": "Phòng ban",
    "Job_Title": "Chức danh",
    "Education_Level": "Học vấn",
    "Location": "Địa điểm",
    "Gender": "Giới tính",
}

COLORS = {
    "navy": "#0B1739",
    "blue": "#1769E0",
    "blue_light": "#5FA8F5",
    "teal": "#079A92",
    "amber": "#F4A621",
    "green": "#76B947",
    "purple": "#6D5BD0",
    "gray": "#8A98AE",
    "border": "#DCE5F0",
    "grid": "#E9EFF6",
    "muted": "#5F6F89",
}

CHART_COLORS = [
    COLORS["blue"],
    COLORS["teal"],
    COLORS["blue_light"],
    COLORS["amber"],
    COLORS["purple"],
    COLORS["green"],
]
