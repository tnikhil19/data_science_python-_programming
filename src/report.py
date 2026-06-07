from src.analysis import (
    risk_distribution,
    study_habits_by_risk
)


def create_summary_report(rows, file_name):

    risk_counts = risk_distribution(rows)
    habits = study_habits_by_risk(rows)

    lines = []

    lines.append("Student Performance Analysis Report")
    lines.append("=" * 40)
    lines.append("")

    lines.append("Risk Distribution")

    for risk, count in risk_counts.items():
        lines.append(f"{risk}: {count}")

    lines.append("")
    lines.append("Study Habits By Risk")

    for metric, values in habits.items():

        lines.append("")
        lines.append(metric)

        for risk, value in values.items():
            lines.append(
                f"{risk}: {round(value, 2)}"
            )

    with open(file_name, "w", encoding="utf-8") as file:

        for line in lines:
            file.write(line + "\n")