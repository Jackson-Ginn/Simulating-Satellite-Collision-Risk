import csv
import numpy as np
fileName = "satDensity"

raw_data  =[]
count = 0

with open('rawMassAndRadiusData.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        raw_data.append(row)

# Get average density from raw data
totalDensity=0
densityArray=[]
for i in range(len(raw_data)-1):
    mass_i = float(raw_data[i+1][0])
    radius_i = float(raw_data[i+1][1])/2
    density_i = (3*mass_i)/(4*np.pi*radius_i**3)
    densityArray.append(density_i)


avgDensity = sum(densityArray)/len(densityArray)

def writeDataToFile(data, file_name, header):
    with open(file_name + ".csv", "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for row in data:
            f.write(",".join(str(x) for x in row) + "\n")

writeDataToFile([[avgDensity]], fileName, "Average Density")