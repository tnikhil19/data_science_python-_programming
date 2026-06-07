import tkinter as tk
from tkinter import scrolledtext

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


class StudentPerformanceGUI:

    def __init__(self):

        self.rows = []
        self.headers = []

        self.root = tk.Tk()
        self.root.title("Student Performance Analyzer")
        self.root.geometry("900x600")

        tk.Button(
            self.root,
            text="Load Dataset",
            command=self.load_dataset
        ).pack(fill="x")

        tk.Button(
            self.root,
            text="Clean Dataset",
            command=self.clean_dataset
        ).pack(fill="x")

        tk.Button(
            self.root,
            text="Dataset Overview",
            command=self.show_overview
        ).pack(fill="x")

        tk.Button(
            self.root,
            text="Risk Distribution",
            command=self.show_risk_distribution
        ).pack(fill="x")

        tk.Button(
            self.root,
            text="Study Habits by Risk",
            command=self.show_study_habits
        ).pack(fill="x")

        tk.Button(
            self.root,
            text="Generate Charts",
            command=self.generate_charts
        ).pack(fill="x")

        tk.Button(
            self.root,
            text="Generate Report",
            command=self.generate_report
        ).pack(fill="x")

        self.output = scrolledtext.ScrolledText(
            self.root,
            width=100,
            height=25
        )

        self.output.pack(fill="both", expand=True)

    def write(self, text):

        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def load_dataset(self):

        self.rows, self.headers = load_csv(RAW_FILE)

        self.write(
            f"Dataset loaded successfully. Records: {len(self.rows)}"
        )

    def clean_dataset(self):

        self.rows = clean_rows(self.rows)

        save_cleaned_csv(
            self.rows,
            self.headers,
            CLEAN_FILE
        )

        self.write(
            f"Dataset cleaned. Records: {len(self.rows)}"
        )

    def show_overview(self):

        result = dataset_overview(self.rows)

        self.write("\nDATASET OVERVIEW")
        self.write(str(result))

    def show_risk_distribution(self):

        result = risk_distribution(self.rows)

        self.write("\nRISK DISTRIBUTION")

        for risk, count in result.items():
            self.write(f"{risk}: {count}")

    def show_study_habits(self):

        result = study_habits_by_risk(self.rows)

        self.write("\nSTUDY HABITS")

        for metric, values in result.items():

            self.write(f"\n{metric}")

            for risk, value in values.items():

                self.write(
                    f"{risk}: {round(value, 2)}"
                )

    def generate_charts(self):

        create_all_charts(
            self.rows,
            CHART_FOLDER
        )

        self.write(
            "Charts created in outputs/charts"
        )

    def generate_report(self):

        create_summary_report(
            self.rows,
            REPORT_FILE
        )

        self.write(
            "Markdown report created."
        )

    def run(self):

        self.root.mainloop()