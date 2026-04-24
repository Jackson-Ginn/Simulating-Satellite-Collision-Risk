import csv
from datetime import datetime

input_file = "EarthEnvironmentData_sorted.csv"

object_classes = [
    "Payload",
    "Payload Mission Related Object",
    "Payload Fragmentation Debris",
    "Payload Debris",
    "Rocket Body",
    "Rocket Mission Related Object",
    "Rocket Fragmentation Debris",
    "Rocket Debris",
    "Unknown",
]

epoch_years = list(range(1960, 2027, 2))


def parse_year(date_str):
    if not date_str:
        return None

    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).year
    except Exception:
        return None


# Create dictionary:
# {
#   "Payload": [0, 0, 0, ...],
#   "Rocket Body": [0, 0, 0, ...],
# }
counts_by_type = {
    obj_class: [0 for _ in epoch_years]
    for obj_class in object_classes
}


with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        obj_class = row["objectClass"]

        if obj_class not in counts_by_type:
            obj_class = "Unknown"

        launch_year = parse_year(row["firstEpoch"])
        reentry_year = parse_year(row["reentryEpoch"])

        if launch_year is None:
            continue

        for i, year in enumerate(epoch_years):
            launched = launch_year <= year

            if reentry_year is None:
                still_in_orbit = True
            else:
                still_in_orbit = year < reentry_year

            if launched and still_in_orbit:
                counts_by_type[obj_class][i] += 1


print("Years:")
print(epoch_years)

print("\nCounts by object type:")
for obj_class, counts in counts_by_type.items():
    print(obj_class)
    print(counts)


import csv

output_file = "orbit_counts_by_year.csv"

# Prepare header: Year + all object classes
header = ["Year"] + object_classes

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)

    # Each row = one year + counts for each object class
    for i, year in enumerate(epoch_years):
        row = [year]

        for obj_class in object_classes:
            row.append(counts_by_type[obj_class][i])

        writer.writerow(row)

print(f"Saved counts to {output_file}")