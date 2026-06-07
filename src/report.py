from src.analysis import (
    risk_distribution,
    study_habits_by_risk
)


def create_summary_report(rows, file_name):

    risk_counts = risk_distribution(rows)
    habits = study_habits_by_risk(rows)

    lines = []

    lines.append("# Student Performance Analysis Report")
    lines.append("")

    lines.append("## Risk Distribution")
    lines.append("")

    for risk, count in risk_counts.items():
        lines.append(f"- **{risk}**: {count}")

    lines.append("")
    lines.append("## Study Habits by Risk Level")
    lines.append("")

    for metric, values in habits.items():

        lines.append(f"### {metric.replace('_', ' ').title()}")

        for risk, value in values.items():
            lines.append(f"- **{risk}**: {round(value, 2)}")

        lines.append("")

    with open(file_name, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))