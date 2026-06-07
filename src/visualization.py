import os
import matplotlib.pyplot as plt

from src.analysis import (
    count_by_category,
    get_average_by_group,
    build_correlation_table
)

RISK_ORDER = [
    "Low Risk",
    "Moderate Risk",
    "High Risk"
]


def create_risk_distribution_chart(rows, folder):

    counts = count_by_category(
        rows,
        "performance_risk_level"
    )

    labels = []
    values = []

    for risk in RISK_ORDER:
        labels.append(risk)
        values.append(counts.get(risk, 0))

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title("Risk Distribution")
    plt.tight_layout()

    plt.savefig(
        os.path.join(folder, "01_risk_distribution.png")
    )

    plt.close()


def create_average_factors_chart(rows, folder):

    study = get_average_by_group(
        rows,
        "performance_risk_level",
        "study_hours_daily"
    )

    labels = list(study.keys())
    values = list(study.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title("Average Study Hours by Risk Level")
    plt.tight_layout()

    plt.savefig(
        os.path.join(folder, "02_study_hours.png")
    )

    plt.close()


def create_correlation_heatmap(rows, folder):

    columns = [
        "study_hours_daily",
        "sleep_hours",
        "stress_level",
        "attendance_percentage"
    ]

    table = build_correlation_table(
        rows,
        columns
    )

    plt.figure(figsize=(7, 6))
    plt.imshow(table)
    plt.colorbar()
    plt.title("Correlation Heatmap")

    plt.savefig(
        os.path.join(folder, "03_correlation_heatmap.png")
    )

    plt.close()


def create_all_charts(rows, folder):

    os.makedirs(folder, exist_ok=True)

    create_risk_distribution_chart(rows, folder)
    create_average_factors_chart(rows, folder)
    create_correlation_heatmap(rows, folder)