from src.data_cleaning import load_csv, clean_rows, save_cleaned_csv
from src.analysis import create_summary_report
from src.visualization import create_all_charts


DATA_FILE = "data/hybrid_student_performance.csv"
CLEANED_FILE = "outputs/cleaned_student_data.csv"
REPORT_FILE = "outputs/summary_report.txt"
CHART_FOLDER = "outputs/charts"


def main():
    rows, headers = load_csv(DATA_FILE)
    cleaned_rows = clean_rows(rows)

    save_cleaned_csv(cleaned_rows, headers, CLEANED_FILE)
    create_summary_report(cleaned_rows, REPORT_FILE)
    create_all_charts(cleaned_rows, CHART_FOLDER)

    print("Project completed successfully.")
    print("Cleaned data saved to:", CLEANED_FILE)
    print("Summary report saved to:", REPORT_FILE)
    print("Charts saved to:", CHART_FOLDER)


if __name__ == "__main__":
    main()
