import csv
import math

SKIP_MASSES = {450000, 96000, 20257, 16000, 13200}


def write_data_to_file(data, file_name, header):
    with open(file_name + ".csv", "w", encoding="utf-8", newline="") as f:
        f.write(header + "\n")
        for row in data:
            f.write(",".join(str(x) for x in row) + "\n")


masses = []
with open("satellite_masses_2026-04-02.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if i % 2 == 1:
            try:
                value = float(line[5:].strip())
                if value in SKIP_MASSES:
                    continue
                masses.append(value)
            except ValueError:
                continue

if not masses:
    raise ValueError("No valid masses found.")

print(masses)
max_mass = max(masses)
print("Max Sat Mass:", max_mass)

density_array = []
mass_volume_array = []

with open("rawMassAndDimensionData.csv", newline="", encoding="utf-8") as f:
    lines = csv.reader(f)

    for line in lines:
        if not line or line[0].strip() == "Shape":
            continue

        shape = line[0].strip()
        mass = float(line[1])
        dimensions = [float(x) for x in line[2:] if x.strip()]

        #if mass > max_mass:
        #    continue

        if shape == "Sphere":
            r = dimensions[0] / 2
            volume = 4 / 3 * math.pi * r**3
        elif shape == "Cyl":
            r = dimensions[0] / 2
            h = dimensions[1]
            volume = math.pi * r**2 * h
        elif shape == "Box":
            h, w, d = dimensions[:3]
            volume = h * w * d
        else:
            continue

        if volume > 4000:
            continue

        density = mass / volume
        mass_volume_array.append([mass, volume])
        density_array.append(density)

if not density_array:
    raise ValueError("No valid density values computed.")

print(density_array)
avg_density = sum(density_array) / len(density_array)
print("AVG DENSITY:", avg_density)

write_data_to_file(mass_volume_array, "satMassVolume2", "Mass, Volume")