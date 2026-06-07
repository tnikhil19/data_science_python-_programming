from src.analysis import (
    dataset_overview,
    risk_distribution,
    study_habits_by_risk
)


def create_summary_report(rows, file_name):

    overview = dataset_overview(rows)
    risk = risk_distribution(rows)
    habits = study_habits_by_risk(rows)
    lines = []
    lines.append("# Student Performance Analysis Report")
    lines.append("")

    lines.append("## Dataset Overview")
    lines.append("")
    lines.append(
        f"- Total Records: {overview['total_records']}"
    )
    lines.append(
        f"- Programs: {overview['programs']}"
    )

    lines.append("")
    lines.append("## Risk Distribution")
    lines.append("")

    for level, count in risk.items():

        lines.append(
            f"- **{level}**: {count}"
        )

    lines.append("")
    lines.append("## Study Habits By Risk")
    lines.append("")

    for metric, values in habits.items():

        lines.append(
            f"### {metric.replace('_',' ').title()}"
        )

        for risk_level, value in values.items():

            lines.append(
                f"- {risk_level}: {round(value,2)}"
            )

        lines.append("")

    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(lines)
        )