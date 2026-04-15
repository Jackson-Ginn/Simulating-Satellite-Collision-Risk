import requests
import time
import os
from get_token import get_token

URL = "https://discosweb.esoc.esa.int"
token = get_token()

headers = {
    "Authorization": f"Bearer {token}",
    "DiscosWeb-Api-Version": "2",
}

tle_file = "TLE Satellite Data 2026-04-02.txt"
output_file = "satellite_masses.txt"
counter_file = "batch_counter.txt"

batch_size = 100

# Read the TLE file
with open(tle_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Remove blank lines
clean_lines = []
for line in lines:
    line = line.strip()
    if line != "":
        clean_lines.append(line)

# Read 3-line TLEs
tle_satellites = []

i = 0
while i < len(clean_lines):
    if i + 2 >= len(clean_lines):
        break

    name_line = clean_lines[i]
    line1 = clean_lines[i + 1]
    line2 = clean_lines[i + 2]

    if line1.startswith("1 ") and line2.startswith("2 "):
        satno_text = line1[2:7].strip()

        try:
            satno = int(satno_text)

            tle_satellites.append({
                "name": name_line,
                "satno": satno
            })
        except:
            pass

        i = i + 3
    else:
        i = i + 1

print("Total satellites in TLE file:", len(tle_satellites))

# Work out which batch number to process this time
if os.path.exists(counter_file):
    with open(counter_file, "r", encoding="utf-8") as f:
        counter_text = f.read().strip()

    try:
        batch_number = int(counter_text)
    except:
        batch_number = 0
else:
    batch_number = 0

start_index = batch_number * batch_size
end_index = start_index + batch_size

batch_satellites = tle_satellites[start_index:end_index]

if len(batch_satellites) == 0:
    print("No more satellites left to process.")
    print("If you want to start again, delete", counter_file)
else:
    print("Processing batch number:", batch_number)
    print("Satellites", start_index, "to", end_index - 1)
    print("Number in this batch:", len(batch_satellites))

    # Build list of satnos for this batch
    satno_strings = []
    for sat in batch_satellites:
        satno_strings.append(str(sat["satno"]))

    satno_text = ",".join(satno_strings)

    # Request up to 100 satellites at once
    response = requests.get(
        f"{URL}/api/objects",
        headers=headers,
        params={
            "filter": f"in(satno,({satno_text}))",
            "page[size]": 100,
        },
    )

    mass_by_satno = {}

    if response.ok:
        doc = response.json()
        data = doc.get("data", [])

        print("Objects returned from API:", len(data))

        for item in data:
            attributes = item.get("attributes", {})
            satno = attributes.get("satno")
            mass = attributes.get("mass")

            if satno is not None:
                mass_by_satno[satno] = mass

        # Append this batch to the output file
        with open(output_file, "a", encoding="utf-8") as f:
            for sat in batch_satellites:
                name = sat["name"]
                satno = sat["satno"]

                if satno in mass_by_satno:
                    mass = mass_by_satno[satno]

                    if mass is None:
                        mass_text = "-1"
                    else:
                        mass_text = str(mass)
                else:
                    mass_text = "NOT_FOUND"

                # Format satno to always be 5 characters wide
                satno_text = f"{satno:05d}"

                # Write output
                f.write(name + "\n")
                f.write(satno_text + " " + mass_text + "\n")

                print(name)
                print(satno_text + " " + mass_text)

        # Increase counter so next run does the next batch
        with open(counter_file, "w", encoding="utf-8") as f:
            f.write(str(batch_number + 1))

        print("Batch finished.")
        print("Results appended to", output_file)
        print("Counter updated to", batch_number + 1)

    else:
        print("API error")
        print(response.text)