import tkinter as tk
from tkinter import scrolledtext

from src.data_cleaning import (
    load_csv,
    clean_rows,
    save_cleaned_csv,
)

from src.analysis import (
    dataset_overview,
    risk_distribution,
    study_habits_by_risk,
)

from src.visualization import create_all_charts
from src.report import create_student_report, create_summary_report


# ── File / folder paths ───────────────────────────────────────────────────────
_BASE        = "data_science_python-_programming"

RAW_FILE     = f"{_BASE}/data/raw/hybrid_student_performance.csv"
CLEAN_FILE   = f"{_BASE}/data/processed/cleaned_student_performance.csv"
CHART_FOLDER = f"{_BASE}/outputs/charts"

# Reports live in their own folder, separate from charts
REPORT_FOLDER       = f"{_BASE}/outputs/report"
STUDENT_REPORT_FILE = f"{REPORT_FOLDER}/student_report.md"
SUMMARY_REPORT_FILE = f"{REPORT_FOLDER}/summary_report.md"


# ── GUI ───────────────────────────────────────────────────────────────────────

class StudentPerformanceGUI:

    def __init__(self):
        self.rows    = []
        self.headers = []

        self.root = tk.Tk()
        self.root.title("Student Performance Analyzer")
        self.root.geometry("900x640")

        buttons = [
            ("Load Dataset",          self.load_dataset),
            ("Clean Dataset",         self.clean_dataset),
            ("Dataset Overview",      self.show_overview),
            ("Risk Distribution",     self.show_risk_distribution),
            ("Study Habits by Risk",  self.show_study_habits),
            ("Generate Charts",       self.generate_charts),
            ("Generate Full Report",  self.generate_student_report),
            ("Generate Summary",      self.generate_summary_report),
            ("Generate Both Reports", self.generate_all_reports),
        ]

        for label, cmd in buttons:
            tk.Button(self.root, text=label, command=cmd).pack(fill="x")

        self.output = scrolledtext.ScrolledText(self.root, width=100, height=25)
        self.output.pack(fill="both", expand=True)

    # ── Output helper ─────────────────────────────────────────────────────────

    def write(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    # ── Buttons ───────────────────────────────────────────────────────────────

    def load_dataset(self):
        self.rows, self.headers = load_csv(RAW_FILE)
        self.write(f"Dataset loaded. Records: {len(self.rows)}")

    def clean_dataset(self):
        self.rows = clean_rows(self.rows)
        save_cleaned_csv(self.rows, self.headers, CLEAN_FILE)
        self.write(f"Dataset cleaned. Records: {len(self.rows)}")

    def show_overview(self):
        result = dataset_overview(self.rows)
        self.write("\nDATASET OVERVIEW")
        self.write(str(result))

    def show_risk_distribution(self):
        result = risk_distribution(self.rows)
        self.write("\nRISK DISTRIBUTION")
        for risk, count in result.items():
            self.write(f"  {risk}: {count}")

    def show_study_habits(self):
        result = study_habits_by_risk(self.rows)
        self.write("\nSTUDY HABITS BY RISK")
        for metric, values in result.items():
            self.write(f"\n  {metric}")
            for risk, value in values.items():
                self.write(f"    {risk}: {round(value, 2)}")

    def generate_charts(self):
        create_all_charts(self.rows, CHART_FOLDER)
        self.write(f"Charts saved to:  {CHART_FOLDER}/")

    def generate_student_report(self):
        create_student_report(self.rows, STUDENT_REPORT_FILE)
        self.write(f"Full report saved: {STUDENT_REPORT_FILE}")

    def generate_summary_report(self):
        create_summary_report(self.rows, SUMMARY_REPORT_FILE)
        self.write(f"Summary saved:     {SUMMARY_REPORT_FILE}")

    def generate_all_reports(self):
        create_student_report(self.rows, STUDENT_REPORT_FILE)
        create_summary_report(self.rows, SUMMARY_REPORT_FILE)
        self.write(f"Both reports saved to: {REPORT_FOLDER}/")
        self.write(f"  • student_report.md")
        self.write(f"  • summary_report.md")

    def run(self):
        self.root.mainloop()