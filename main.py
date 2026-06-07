from src.data_cleaning import (
    load_csv,
    clean_rows,
    save_cleaned_csv
)

from src.analysis import (
    dataset_overview,
    risk_distribution,
    study_habits_by_risk
)

from src.visualization import create_all_charts

from src.report import create_summary_report


RAW_FILE = "data_science_python-_programming/data/raw/hybrid_student_performance.csv"
CLEAN_FILE = "data_science_python-_programming/data/processed/cleaned_student_performance.csv"

CHART_FOLDER = "data_science_python-_programming/outputs/charts"
REPORT_FILE = "data_science_python-_programming/outputs/student_report.md"


def main():

    rows, headers = load_csv(RAW_FILE)

    cleaned_rows = clean_rows(rows)

    save_cleaned_csv(
        cleaned_rows,
        headers,
        CLEAN_FILE
    )

    print(dataset_overview(cleaned_rows))

    create_all_charts(
        cleaned_rows,
        CHART_FOLDER
    )

    create_summary_report(
        cleaned_rows,
        REPORT_FILE
    )

    print("Analysis completed successfully.")


if __name__ == "__main__":
    main()