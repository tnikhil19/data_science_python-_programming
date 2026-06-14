import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from src.analysis import (
    count_by_category,
    get_average_by_group,
    build_correlation_table
)

RISK_ORDER  = ["Low Risk", "Moderate Risk", "High Risk"]
RISK_COLORS = ["#4CAF50", "#FF9800", "#F44336"]

CHART_STYLE = {
    "font.family":       "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "axes.grid.axis":    "y",
    "grid.alpha":        0.4,
    "grid.linestyle":    "--",
}


def apply_style():
    plt.rcParams.update(CHART_STYLE)


# ── Chart 01 ─────────────────────────────────────────────────────────────────

def create_risk_distribution_chart(rows, folder):
    """Colour-coded bar chart: student count per risk level."""
    apply_style()

    counts = count_by_category(rows, "performance_risk_level")
    labels = RISK_ORDER[:]
    values = [counts.get(r, 0) for r in RISK_ORDER]
    total  = sum(values)

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(labels, values, color=RISK_COLORS, width=0.5, zorder=3)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 5,
            str(val),
            ha="center", va="bottom", fontsize=12, fontweight="bold",
        )

    legend_patches = [
        mpatches.Patch(color=c, label=f"{r}  ({counts.get(r,0)/total*100:.1f}%)")
        for r, c in zip(RISK_ORDER, RISK_COLORS)
    ]
    ax.legend(handles=legend_patches, loc="upper right", fontsize=10)
    ax.set_title("Student Performance Risk Distribution", fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel("Risk Level",          fontsize=12, labelpad=8)
    ax.set_ylabel("Number of Students",  fontsize=12, labelpad=8)
    ax.set_ylim(0, max(values) * 1.15)

    plt.tight_layout()
    plt.savefig(os.path.join(folder, "01_risk_distribution.png"), dpi=150)
    plt.close()


# ── Chart 02 ─────────────────────────────────────────────────────────────────

def create_average_factors_chart(rows, folder):
    """
    Grouped bar chart matching the uploaded reference:
    Study Hours (blue) | Sleep Hours (orange) | Stress Level (green)
    Title: 'Average Study, Sleep, and Stress by Risk Level'
    """
    apply_style()

    metrics = {
        "Study Hours":  get_average_by_group(rows, "performance_risk_level", "study_hours_daily"),
        "Sleep Hours":  get_average_by_group(rows, "performance_risk_level", "sleep_hours"),
        "Stress Level": get_average_by_group(rows, "performance_risk_level", "stress_level"),
    }

    # Colours match the uploaded chart exactly
    metric_colors = ["#2196F3", "#FF9800", "#4CAF50"]

    x     = np.arange(len(RISK_ORDER))
    n     = len(metrics)
    width = 0.22

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (label, data) in enumerate(metrics.items()):
        vals   = [data.get(r, 0) for r in RISK_ORDER]
        offset = (i - n / 2 + 0.5) * width
        bars   = ax.bar(x + offset, vals, width, label=label,
                        color=metric_colors[i], zorder=3)

        for bar, val in zip(bars, vals):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05,
                f"{val:.2f}",
                ha="center", va="bottom", fontsize=8.5, fontweight="bold",
            )

    ax.set_title("Average Study, Sleep, and Stress by Risk Level",
                 fontsize=14, fontweight="bold", pad=14)
    ax.set_xlabel("Risk Level",   fontsize=12, labelpad=8)
    ax.set_ylabel("Average Value", fontsize=12, labelpad=8)
    ax.set_xticks(x)
    ax.set_xticklabels(RISK_ORDER, fontsize=11)
    ax.legend(fontsize=10, loc="upper right")
    ax.set_ylim(0, ax.get_ylim()[1] * 1.18)

    plt.tight_layout()
    plt.savefig(os.path.join(folder, "02_average_factors_by_risk.png"), dpi=150)
    plt.close()


# ── Chart 03 ─────────────────────────────────────────────────────────────────

def create_correlation_heatmap(rows, folder):
    """Annotated Pearson correlation heatmap."""
    apply_style()
    plt.rcParams["axes.grid"] = False

    columns = [
        "study_hours_daily",
        "sleep_hours",
        "stress_level",
        "attendance_percentage",
    ]
    labels = ["Study Hours", "Sleep Hours", "Stress Level", "Attendance %"]

    table = build_correlation_table(rows, columns)

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(table, cmap="RdYlGn", vmin=-1, vmax=1, aspect="auto")

    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Pearson Correlation", fontsize=11)

    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=10)
    ax.set_yticklabels(labels, fontsize=10)

    for i in range(len(labels)):
        for j in range(len(labels)):
            val        = table[i][j]
            text_color = "black" if abs(val) < 0.6 else "white"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=10, fontweight="bold", color=text_color)

    ax.set_title("Feature Correlation Heatmap", fontsize=15, fontweight="bold", pad=14)

    plt.tight_layout()
    plt.savefig(os.path.join(folder, "03_correlation_heatmap.png"), dpi=150)
    plt.close()


# ── Chart 04 ─────────────────────────────────────────────────────────────────

def create_risk_by_program_chart(rows, folder):
    """Stacked bar chart of risk levels across program streams."""
    apply_style()

    program_risk = {}
    for row in rows:
        program = row.get("program_stream", "Unknown")
        risk    = row.get("performance_risk_level", "Unknown")
        if program not in program_risk:
            program_risk[program] = {r: 0 for r in RISK_ORDER}
        if risk in program_risk[program]:
            program_risk[program][risk] += 1

    programs = sorted(program_risk.keys())
    bottoms  = [0] * len(programs)

    fig, ax = plt.subplots(figsize=(12, 6))

    for risk, color in zip(RISK_ORDER, RISK_COLORS):
        vals = [program_risk[p][risk] for p in programs]
        ax.bar(programs, vals, bottom=bottoms, label=risk, color=color, zorder=3)
        bottoms = [b + v for b, v in zip(bottoms, vals)]

    ax.set_title("Risk Level by Program Stream", fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel("Program Stream",       fontsize=12, labelpad=8)
    ax.set_ylabel("Number of Students",   fontsize=12, labelpad=8)
    ax.set_xticks(range(len(programs)))
    ax.set_xticklabels(programs, rotation=40, ha="right", fontsize=9)
    ax.legend(fontsize=10, loc="upper right")

    plt.tight_layout()
    plt.savefig(os.path.join(folder, "04_risk_by_program.png"), dpi=150)
    plt.close()


# ── Entry point ───────────────────────────────────────────────────────────────

def create_all_charts(rows, folder):
    os.makedirs(folder, exist_ok=True)
    create_risk_distribution_chart(rows, folder)
    create_average_factors_chart(rows, folder)
    create_correlation_heatmap(rows, folder)
    create_risk_by_program_chart(rows, folder)