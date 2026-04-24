import csv
from datetime import datetime

input_file = "EarthEnvironmentData.csv"
output_file = "EarthEnvironmentData_sorted.csv"


def parse_date(date_str):
    """Safely parse ISO date strings; return None if invalid."""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        return None


# Load data
data = []
with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["parsed_firstEpoch"] = parse_date(row["firstEpoch"])
        data.append(row)


# Sort (oldest first, None values go last)
data.sort(
    key=lambda x: (
        x["parsed_firstEpoch"] is None,
        x["parsed_firstEpoch"]
    )
)


# Remove helper field before saving
for row in data:
    del row["parsed_firstEpoch"]


# Save sorted data
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["satno", "firstEpoch", "reentryEpoch", "objectClass"]
    )
    writer.writeheader()
    writer.writerows(data)


print(f"Sorted data saved to {output_file}")