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
    except (ValueError, TypeError):
        return None


def convert_range_to_number(value):

    if value is None:
        return None

    value = str(value)

    if value == "Unknown":
        return None

    value = value.replace("%", "")

    mappings = {
        "Less than 1 hour": 0.5,
        "1-2 hours": 1.5,
        "More than 2 hours": 2.5,
        "30-60 minutes": 0.75,
        "2-4 hours": 3.0,
        "4-6 hours": 5.0,
        "More than 6 hours": 7.0,
        "4-5": 4.5,
        "6-7": 6.5,
        "More than 8": 8.5,
        "Less than 50": 45.0,
        "50 - 65": 57.5,
        "66 - 75": 70.5,
        "76 - 85": 80.5,
        "More than 85": 90.0,
        "5.0 - 6.9": 5.95,
        "7.0 - 8.4": 7.7,
        "8.5 - 9.4": 8.95,
        "9.5 - 10.0": 9.75
    }

    for text, number in mappings.items():
        if text in value:
            return number

    return get_number(value)


def get_average_by_group(rows, group_column, value_column):

    totals = {}
    counts = {}

    for row in rows:

        group = row.get(group_column, "Unknown")
        value = convert_range_to_number(row.get(value_column))

        if value is None:
            continue

        if group not in totals:
            totals[group] = 0
            counts[group] = 0

        totals[group] += value
        counts[group] += 1

    averages = {}

    for group in totals:
        averages[group] = totals[group] / counts[group]

    return averages


def get_numeric_list(rows, column_name):

    values = []

    for row in rows:

        value = convert_range_to_number(
            row.get(column_name)
        )

        if value is not None:
            values.append(value)

    return values


def average(values):

    if not values:
        return 0

    return sum(values) / len(values)


def correlation(x_values, y_values):

    length = min(len(x_values), len(y_values))

    if length == 0:
        return 0

    x_values = x_values[:length]
    y_values = y_values[:length]

    x_avg = average(x_values)
    y_avg = average(y_values)

    numerator = 0
    denominator_x = 0
    denominator_y = 0

    for i in range(length):

        x_diff = x_values[i] - x_avg
        y_diff = y_values[i] - y_avg

        numerator += x_diff * y_diff
        denominator_x += x_diff ** 2
        denominator_y += y_diff ** 2

    denominator = (denominator_x * denominator_y) ** 0.5

    if denominator == 0:
        return 0

    return numerator / denominator


def build_correlation_table(rows, columns):

    table = []

    for col1 in columns:

        row_values = []

        for col2 in columns:

            value = correlation(
                get_numeric_list(rows, col1),
                get_numeric_list(rows, col2)
            )

            row_values.append(value)

        table.append(row_values)

    return table


def dataset_overview(rows):

    programs = set()

    for row in rows:
        programs.add(
            row.get("program_stream", "Unknown")
        )

    return {
        "total_records": len(rows),
        "programs": len(programs),
        "risk_levels": count_by_category(
            rows,
            "performance_risk_level"
        )
    }


def risk_distribution(rows):

    return count_by_category(
        rows,
        "performance_risk_level"
    )


def study_habits_by_risk(rows):

    return {
        "study_hours": get_average_by_group(
            rows,
            "performance_risk_level",
            "study_hours_daily"
        ),
        "sleep_hours": get_average_by_group(
            rows,
            "performance_risk_level",
            "sleep_hours"
        ),
        "stress_level": get_average_by_group(
            rows,
            "performance_risk_level",
            "stress_level"
        )
    }