import csv
import os

def load_csv(file_name):
    rows = []

    with open(file_name, "r", encoding="latin1", newline="") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames

        for row in reader:
            rows.append(row)

    return rows, headers


def clean_text(value):
    if value is None:
        return "Unknown"

    value = str(value).strip()
    value = value.replace("\x96", "-")
    value = value.replace("–", "-")

    if value == "":
        return "Unknown"

    return value


def calculate_risk_score(risk_level):
    mapping = {
        "Low Risk": 1,
        "Moderate Risk": 2,
        "High Risk": 3
    }

    return mapping.get(risk_level, 0)


def calculate_study_hours_score(study_hours):
    mapping = {
        "Less than 1 hour": 1,
        "1-2 hours": 2,
        "More than 2 hours": 3
    }

    return mapping.get(study_hours, 0)


def clean_rows(rows):
    cleaned_rows = []
    seen_ids = set()

    for row in rows:

        student_id = clean_text(row.get("student_id"))

        # Remove duplicate students
        if student_id in seen_ids:
            continue

        seen_ids.add(student_id)

        cleaned_row = {}

        for key, value in row.items():
            cleaned_row[key] = clean_text(value)

        # Create helper columns for analysis
        cleaned_row["risk_score"] = calculate_risk_score(
            cleaned_row.get("performance_risk_level")
        )

        cleaned_row["study_hours_score"] = calculate_study_hours_score(
            cleaned_row.get("study_hours_daily")
        )

        cleaned_rows.append(cleaned_row)

    return cleaned_rows


def save_cleaned_csv(rows, headers, file_name):

    headers = list(headers)

    if "risk_score" not in headers:
        headers.append("risk_score")

    if "study_hours_score" not in headers:
        headers.append("study_hours_score")

    folder = os.path.dirname(file_name)
    os.makedirs(folder, exist_ok=True)

    with open(file_name, "w", encoding="utf-8", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=headers)

        writer.writeheader()

        for row in rows:
            writer.writerow(row)


def load_clean_dataframe(file_name):
    """
    Optional helper for analysis.py.
    Loads cleaned CSV into pandas DataFrame.
    """

    return pd.read_csv(file_name)