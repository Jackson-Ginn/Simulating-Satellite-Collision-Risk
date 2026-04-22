import requests
import time
import os
from get_token import get_token
import numpy as np
import csv
import math

masses = []
with open("satellite_masses_2026-04-02.txt", "r") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        if i % 2 == 1:
            line = lines[i]
            mass = line[5:]
            try:
                if float(mass) == 450000 or float(mass) == 96000 or float(mass) == 20257 or float(mass) == 16000 or float(mass) == 13200:
                    continue
                
                masses.append(float(mass))
            except:
                continue
print(masses)
maxMass = max(masses)
print("Max Sat Mass:", maxMass)
fileName = "satDensity"

def writeDataToFile(data, file_name, header):
    with open(file_name + ".csv", "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for row in data:
            f.write(",".join(str(x) for x in row) + "\n")

# Calc density

totalDensity=0
densityArray=[]
massVolumeArray=[]
with open("rawMassAndDimensionData.csv", newline="") as f:
    lines = csv.reader(f)

    for line in lines:
        if line[0].strip() == "Shape":
            continue
        shape = line[0]
        mass = float(line[1])
        dimensions = line[2:]

        if mass > maxMass:
            continue

        if shape == "Sphere":
            r = float(dimensions[0])/2
            volume = 4/3 * math.pi * r**3
        if shape == "Cyl":
            r = float(dimensions[0])/2
            h = float(dimensions[1])
            volume = math.pi *r**2 * h
        if shape == "Box":
            h = float(dimensions[0])
            w = float(dimensions[1])
            d = float(dimensions[2])
            volume = h * w * d

        density = mass/volume
        massVolumeArray.append([mass,volume])
        densityArray.append(density)

print(densityArray)
avgDensity = sum(densityArray)/len(densityArray)
print("AVG DENSITY: ",avgDensity)
writeDataToFile(massVolumeArray,"satMassVolume","Mass, Volume")