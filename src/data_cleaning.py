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

    value = value.strip()
    value = value.replace("\x96", "-")
    value = value.replace("–", "-")

    if value == "":
        return "Unknown"

    return value


def clean_rows(rows):
    cleaned_rows = []
    seen_ids = set()

    for row in rows:
        student_id = clean_text(row.get("student_id", ""))

        if student_id in seen_ids:
            continue

        seen_ids.add(student_id)

        new_row = {}
        for key, value in row.items():
            new_row[key] = clean_text(value)

        cleaned_rows.append(new_row)

    return cleaned_rows


def save_cleaned_csv(rows, headers, file_name):
    folder = os.path.dirname(file_name)
    os.makedirs(folder, exist_ok=True)

    with open(file_name, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        for row in rows:
            writer.writerow(row)
