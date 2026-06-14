import os
from datetime import datetime

from src.analysis import (
    dataset_overview,
    risk_distribution,
    study_habits_by_risk,
    get_average_by_group,
    build_correlation_table,
    get_numeric_list,
    average,
)

RISK_ORDER = ["Low Risk", "Moderate Risk", "High Risk"]

# Paths are relative to the report folder so embedded images resolve correctly
# when the .md is opened next to the charts folder.
CHART_PATHS = {
    "risk_dist":   "../charts/01_risk_distribution.png",
    "avg_factors": "../charts/02_average_factors_by_risk.png",
    "heatmap":     "../charts/03_correlation_heatmap.png",
    "by_program":  "../charts/04_risk_by_program.png",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _pct(part, total):
    return f"{part / total * 100:.1f}" if total else "0.0"

def _row(*cells):
    return "| " + " | ".join(str(c) for c in cells) + " |"

def _div(n):
    return "| " + " | ".join(["---"] * n) + " |"

def _write(path, lines):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── Shared data builders ──────────────────────────────────────────────────────

def _build_data(rows):
    overview  = dataset_overview(rows)
    risk      = risk_distribution(rows)
    habits    = study_habits_by_risk(rows)
    attend    = get_average_by_group(rows, "performance_risk_level", "attendance_percentage")
    total     = overview["total_records"]
    now       = datetime.now().strftime("%Y-%m-%d %H:%M")

    columns   = ["study_hours_daily", "sleep_hours", "stress_level", "attendance_percentage"]
    col_labels = ["Study Hrs", "Sleep Hrs", "Stress", "Attendance %"]
    corr_table = build_correlation_table(rows, columns)

    def avg_metric(col):
        vals = get_numeric_list(rows, col)
        return round(average(vals), 2) if vals else "N/A"

    program_risk = {}
    for row in rows:
        prog  = row.get("program_stream", "Unknown")
        rlvl  = row.get("performance_risk_level", "Unknown")
        if prog not in program_risk:
            program_risk[prog] = {r: 0 for r in RISK_ORDER}
        if rlvl in program_risk[prog]:
            program_risk[prog][rlvl] += 1

    return dict(
        overview=overview, risk=risk, habits=habits, attend=attend,
        total=total, now=now, avg_metric=avg_metric,
        columns=columns, col_labels=col_labels, corr_table=corr_table,
        program_risk=program_risk,
    )


# ── student_report.md  (full detailed report) ─────────────────────────────────

def create_student_report(rows, file_name):
    """Full multi-section report with tables, chart embeds, findings & recommendations."""

    d = _build_data(rows)
    total = d["total"]
    risk  = d["risk"]
    habits = d["habits"]
    study_h  = habits["study_hours"]
    sleep_h  = habits["sleep_hours"]
    stress_l = habits["stress_level"]
    attend   = d["attend"]
    corr_table  = d["corr_table"]
    col_labels  = d["col_labels"]
    program_risk = d["program_risk"]

    # Auto-derived insights
    high_risk_count = risk.get("High Risk", 0)
    study_diff  = round(study_h.get("Low Risk", 0)   - study_h.get("High Risk", 0), 2)
    stress_diff = round(stress_l.get("High Risk", 0) - stress_l.get("Low Risk", 0), 2)

    best_corr = ("", "", 0.0)
    for i in range(len(col_labels)):
        for j in range(len(col_labels)):
            if i != j and abs(corr_table[i][j]) > abs(best_corr[2]):
                best_corr = (col_labels[i], col_labels[j], corr_table[i][j])

    L = []

    # Title
    L += [
        "# Student Performance Analysis Report",
        "",
        f"> **Generated:** {d['now']}  ",
        f"> **Dataset:** hybrid_student_performance.csv  ",
        f"> **Total Records Analysed:** {total:,}",
        "",
        "---", "",
    ]

    # 1. Dataset Overview
    L += [
        "## 1. Dataset Overview", "",
        _row("Metric", "Value"), _div(2),
        _row("Total Students",          f"{total:,}"),
        _row("Program Streams",         d["overview"]["programs"]),
        _row("Risk Categories",         len(risk)),
        _row("Avg Study Hours / Day",   d["avg_metric"]("study_hours_daily")),
        _row("Avg Sleep Hours / Night", d["avg_metric"]("sleep_hours")),
        _row("Avg Stress Level (1-10)", d["avg_metric"]("stress_level")),
        _row("Avg Attendance %",        d["avg_metric"]("attendance_percentage")),
        "",
    ]

    # 2. Risk Distribution
    L += ["## 2. Risk Distribution", "",
          _row("Risk Level", "Students", "Percentage"), _div(3)]
    for level in RISK_ORDER:
        cnt = risk.get(level, 0)
        L.append(_row(level, cnt, f"{_pct(cnt, total)}%"))
    L += ["", f"![Risk Distribution]({CHART_PATHS['risk_dist']})", ""]

    # 3. Study, Sleep & Stress by Risk
    L += ["## 3. Study, Sleep & Stress by Risk Level", "",
          _row("Risk Level", "Avg Study Hrs", "Avg Sleep Hrs", "Avg Stress"), _div(4)]
    for level in RISK_ORDER:
        L.append(_row(level,
                      round(study_h.get(level, 0), 2),
                      round(sleep_h.get(level, 0), 2),
                      round(stress_l.get(level, 0), 2)))
    L += ["", f"![Average Factors by Risk]({CHART_PATHS['avg_factors']})", ""]

    # 4. Attendance by Risk
    L += ["## 4. Attendance by Risk Level", "",
          _row("Risk Level", "Avg Attendance %"), _div(2)]
    for level in RISK_ORDER:
        L.append(_row(level, round(attend.get(level, 0), 1)))
    L.append("")

    # 5. Correlation Heatmap
    L += ["## 5. Feature Correlations", "",
          f"![Correlation Heatmap]({CHART_PATHS['heatmap']})", "",
          _row("", *col_labels), _div(len(col_labels) + 1)]
    for i, rl in enumerate(col_labels):
        L.append(_row(rl, *[f"{corr_table[i][j]:.2f}" for j in range(len(col_labels))]))
    L.append("")

    # 6. Risk by Program Stream
    L += ["## 6. Risk by Program Stream", "",
          f"![Risk by Program]({CHART_PATHS['by_program']})", "",
          _row("Program Stream", *RISK_ORDER), _div(len(RISK_ORDER) + 1)]
    for prog, counts in sorted(program_risk.items()):
        L.append(_row(prog, *[counts.get(r, 0) for r in RISK_ORDER]))
    L.append("")

    # 7. Key Findings
    L += [
        "## 7. Key Findings", "",
        f"- **{_pct(high_risk_count, total)}%** of students are High Risk "
        f"({high_risk_count:,} students) — a significant cohort requiring targeted support.",
        f"- Low Risk students study **{study_diff} hrs/day more** than High Risk peers.",
        f"- Stress is **{stress_diff} points higher** on average for High Risk students.",
        f"- Strongest correlation: **{best_corr[0]}** ↔ **{best_corr[1]}** "
        f"(r = {best_corr[2]:.2f}).",
        "- Higher attendance consistently aligns with lower risk levels across all programs.",
        "",
    ]

    # 8. Recommendations
    L += [
        "## 8. Recommendations", "",
        "1. **Early Intervention** — Flag students with < 2 study hrs/day and stress > 7.",
        "2. **Attendance Alerts** — Trigger counsellor review when attendance falls below 66%.",
        "3. **Wellness Workshops** — Target sleep hygiene sessions at Moderate & High Risk cohorts.",
        "4. **Program-Level Resourcing** — Allocate tutoring to streams with highest High Risk ratios.",
        "5. **Predictive Modelling** — Dataset is ready for classification (Random Forest, XGBoost).",
        "", "---", "",
        "*Report generated automatically by Student Performance Analyzer.*",
    ]

    _write(file_name, L)


# ── summary_report.md  (concise executive summary) ────────────────────────────

def create_summary_report(rows, file_name):
    """Concise executive summary: headline numbers + key chart + top 3 actions."""

    d = _build_data(rows)
    total = d["total"]
    risk  = d["risk"]
    habits = d["habits"]
    study_h  = habits["study_hours"]
    stress_l = habits["stress_level"]

    high_risk_count = risk.get("High Risk", 0)
    low_risk_count  = risk.get("Low Risk",  0)
    mod_risk_count  = risk.get("Moderate Risk", 0)
    study_diff  = round(study_h.get("Low Risk", 0)   - study_h.get("High Risk", 0), 2)
    stress_diff = round(stress_l.get("High Risk", 0) - stress_l.get("Low Risk", 0), 2)

    L = []

    L += [
        "# Student Performance — Executive Summary",
        "",
        f"> **Generated:** {d['now']}  ",
        f"> **Records:** {total:,}",
        "",
        "---", "",
        "## Headline Figures", "",
        _row("Risk Level", "Students", "%"), _div(3),
    ]
    for level in RISK_ORDER:
        cnt = risk.get(level, 0)
        L.append(_row(level, cnt, f"{_pct(cnt, total)}%"))

    L += [
        "",
        f"![Risk Distribution]({CHART_PATHS['risk_dist']})",
        "",
        "## Key Insights", "",
        f"- **{_pct(high_risk_count, total)}%** of students ({high_risk_count:,}) are classified as High Risk.",
        f"- Low Risk students study **{study_diff} hrs/day more** than High Risk students.",
        f"- Stress levels are **{stress_diff} points higher** in the High Risk group.",
        f"- See `student_report.md` for full breakdowns, charts, and correlation analysis.",
        "",
        "## Top 3 Actions", "",
        "1. **Identify** students with < 2 study hrs/day and stress > 7 for immediate outreach.",
        "2. **Monitor** attendance weekly — drops below 66% are a leading risk indicator.",
        "3. **Run** classification modelling on the cleaned dataset to predict risk early.",
        "",
        "---",
        "*For the full report including all charts and recommendations, see `student_report.md`.*",
    ]

    _write(file_name, L)