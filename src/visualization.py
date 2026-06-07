import os
import matplotlib.pyplot as plt
from src.analysis import count_by_category, get_average_by_group, build_correlation_table


RISK_ORDER = ["Low Risk", "Moderate Risk", "High Risk"]


def create_risk_distribution_chart(rows, folder):
    counts = count_by_category(rows, "performance_risk_level")

    labels = []
    values = []

    for risk in RISK_ORDER:
        labels.append(risk)
        values.append(counts.get(risk, 0))

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title("Student Count by Performance Risk Level")
    plt.xlabel("Risk Level")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "01_risk_distribution.png"))
    plt.close()


def create_average_factors_chart(rows, folder):
    study_avg = get_average_by_group(rows, "performance_risk_level", "study_hours_daily")
    sleep_avg = get_average_by_group(rows, "performance_risk_level", "sleep_hours")
    stress_avg = get_average_by_group(rows, "performance_risk_level", "stress_level")

    labels = RISK_ORDER
    study_values = []
    sleep_values = []
    stress_values = []

    for risk in labels:
        study_values.append(study_avg.get(risk, 0))
        sleep_values.append(sleep_avg.get(risk, 0))
        stress_values.append(stress_avg.get(risk, 0))

    x_positions = list(range(len(labels)))
    width = 0.25

    left_positions = []
    middle_positions = []
    right_positions = []

    for x in x_positions:
        left_positions.append(x - width)
        middle_positions.append(x)
        right_positions.append(x + width)

    plt.figure(figsize=(9, 5))
    plt.bar(left_positions, study_values, width=width, label="Study Hours")
    plt.bar(middle_positions, sleep_values, width=width, label="Sleep Hours")
    plt.bar(right_positions, stress_values, width=width, label="Stress Level")
    plt.title("Average Study, Sleep, and Stress by Risk Level")
    plt.xlabel("Risk Level")
    plt.ylabel("Average Value")
    plt.xticks(x_positions, labels)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "02_average_factors_by_risk.png"))
    plt.close()


def create_correlation_heatmap(rows, folder):
    columns = [
        "study_hours_daily",
        "sleep_hours",
        "stress_level",
        "attendance_percentage",
        "daily_productivity",
        "cgpa_category"
    ]

    short_names = [
        "Study",
        "Sleep",
        "Stress",
        "Attendance",
        "Productivity",
        "CGPA"
    ]

    table = build_correlation_table(rows, columns)

    plt.figure(figsize=(8, 6))
    plt.imshow(table)
    plt.title("Correlation Heatmap of Selected Student Factors")
    plt.colorbar()
    plt.xticks(range(len(short_names)), short_names, rotation=45, ha="right")
    plt.yticks(range(len(short_names)), short_names)

    for i in range(len(table)):
        for j in range(len(table[i])):
            plt.text(j, i, str(round(table[i][j], 2)), ha="center", va="center")

    plt.tight_layout()
    plt.savefig(os.path.join(folder, "03_correlation_heatmap.png"))
    plt.close()


def create_all_charts(rows, folder):
    os.makedirs(folder, exist_ok=True)

    create_risk_distribution_chart(rows, folder)
    create_average_factors_chart(rows, folder)
    create_correlation_heatmap(rows, folder)
