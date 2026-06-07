def count_by_category(rows, column_name):
    counts = {}

    for row in rows:
        value = row.get(column_name, "Unknown")

        if value not in counts:
            counts[value] = 0

        counts[value] += 1

    return counts


def get_number(value):
    try:
        return float(value)
    except ValueError:
        return None


def convert_range_to_number(value):
    value = value.replace("%", "")
    value = value.replace("Above", "More than")

    if value == "Unknown":
        return None

    if "Less than 1 hour" in value:
        return 0.5
    if "1-2 hours" in value:
        return 1.5
    if "More than 2 hours" in value:
        return 2.5

    if "30-60 minutes" in value:
        return 0.75

    if "2-4 hours" in value:
        return 3.0
    if "4-6 hours" in value:
        return 5.0
    if "More than 6 hours" in value:
        return 7.0

    if "4-5" in value:
        return 4.5
    if "6-7" in value:
        return 6.5
    if "More than 8" in value:
        return 8.5

    if "Less than 50" in value:
        return 45.0
    if "50 - 65" in value or "50-65" in value:
        return 57.5
    if "66 - 75" in value or "66-75" in value:
        return 70.5
    if "76 - 85" in value or "76-85" in value:
        return 80.5
    if "More than 85" in value:
        return 90.0

    if "5.0 - 6.9" in value or "5.0-6.9" in value:
        return 5.95
    if "7.0 - 8.4" in value or "7.0-8.4" in value:
        return 7.7
    if "8.5 - 9.4" in value or "8.5-9.4" in value:
        return 8.95
    if "9.5 - 10.0" in value or "9.5-10.0" in value:
        return 9.75

    return get_number(value)


def get_average_by_group(rows, group_column, value_column):
    totals = {}
    counts = {}

    for row in rows:
        group = row.get(group_column, "Unknown")
        number = convert_range_to_number(row.get(value_column, "Unknown"))

        if number is not None:
            if group not in totals:
                totals[group] = 0
                counts[group] = 0

            totals[group] += number
            counts[group] += 1

    averages = {}
    for group in totals:
        averages[group] = totals[group] / counts[group]

    return averages


def get_numeric_list(rows, column_name):
    values = []

    for row in rows:
        number = convert_range_to_number(row.get(column_name, "Unknown"))

        if number is not None:
            values.append(number)

    return values


def average(values):
    if len(values) == 0:
        return 0

    return sum(values) / len(values)


def correlation(list_one, list_two):
    length = min(len(list_one), len(list_two))

    if length == 0:
        return 0

    x_values = list_one[:length]
    y_values = list_two[:length]

    x_avg = average(x_values)
    y_avg = average(y_values)

    top = 0
    bottom_x = 0
    bottom_y = 0

    for i in range(length):
        x_difference = x_values[i] - x_avg
        y_difference = y_values[i] - y_avg

        top += x_difference * y_difference
        bottom_x += x_difference ** 2
        bottom_y += y_difference ** 2

    bottom = (bottom_x * bottom_y) ** 0.5

    if bottom == 0:
        return 0

    return top / bottom


def build_correlation_table(rows, columns):
    table = []

    for first_column in columns:
        row_values = []
        first_values = get_numeric_list(rows, first_column)

        for second_column in columns:
            second_values = get_numeric_list(rows, second_column)
            result = correlation(first_values, second_values)
            row_values.append(result)

        table.append(row_values)

    return table


def create_summary_report(rows, file_name):
    risk_counts = count_by_category(rows, "performance_risk_level")

    study_avg = get_average_by_group(rows, "performance_risk_level", "study_hours_daily")
    sleep_avg = get_average_by_group(rows, "performance_risk_level", "sleep_hours")
    stress_avg = get_average_by_group(rows, "performance_risk_level", "stress_level")
    attendance_avg = get_average_by_group(rows, "performance_risk_level", "attendance_percentage")

    lines = []
    lines.append("Student Performance Risk Analysis")
    lines.append("=================================")
    lines.append("")
    lines.append("Total cleaned records: " + str(len(rows)))
    lines.append("")

    lines.append("Analysis 1: Risk Level Distribution")
    for risk, count in risk_counts.items():
        lines.append("- " + risk + ": " + str(count))
    lines.append("")

    lines.append("Analysis 2: Average Factors by Risk Level")
    for risk in risk_counts:
        lines.append("Risk Level: " + risk)
        lines.append("  Average study hours: " + str(round(study_avg.get(risk, 0), 2)))
        lines.append("  Average sleep hours: " + str(round(sleep_avg.get(risk, 0), 2)))
        lines.append("  Average stress level: " + str(round(stress_avg.get(risk, 0), 2)))
        lines.append("  Average attendance percentage: " + str(round(attendance_avg.get(risk, 0), 2)))
    lines.append("")

    lines.append("Analysis 3: Relationship Check")
    columns = ["study_hours_daily", "sleep_hours", "stress_level", "attendance_percentage", "daily_productivity", "cgpa_category"]
    table = build_correlation_table(rows, columns)

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            text = columns[i] + " vs " + columns[j] + ": " + str(round(table[i][j], 2))
            lines.append("- " + text)

    lines.append("")
    lines.append("Main finding:")
    lines.append("Students with better study habits, higher attendance, and stronger routine indicators generally appear closer to lower risk levels. Stress and lack of consistency are useful factors to watch.")

    with open(file_name, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")
