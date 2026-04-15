def Break():
    input("Break")

import math
import numpy as np
# Open TLE file and read content
file = open("TLE Satellite Data2.txt", "r")
content = file.read()
file.close()

i = 0
# New content to store new data
newContent = ""
for line in content.splitlines():
    if i == 0:
        name = line.strip()
    elif i == 1:
        epoch = line.split()[3]
        epochYr = epoch[0:2]
        epochDay = epoch[2:]
    else:
        inc, RAAN, ecc, AoP, meanAnomaly, meanMotion = line.split()[2:8]
        ecc = "0." + ecc
        meanMotion = meanMotion[0:11]
    i+=1
    if i == 3:
        # Calculate semiMajor axis from mean motion
        meanMotion = float(meanMotion)
        mu = 3.986004418e14
        semiMaj = (mu * ((24*3600)/(meanMotion * 2 * math.pi)) ** 2) ** (1/3)
        semiMaj /= 1000
        newSat = name + "\n" + epochYr + " " + epochDay + "\n" + inc + " " + RAAN + " " + ecc + " " + AoP + " " + meanAnomaly + " " + str(meanMotion) + "\n" + str(semiMaj) + "\n"
        newContent = newContent + newSat
        i = 0
# Save new data in new file
file = open("Sorted Satellite Data.txt","w")
file.write(newContent)
file.close()

# Save just altitude values, same method
file = open("Sorted Satellite Data.txt","r")
content = file.read()
file.close()
i = 0
newContent = ""
for line in content.splitlines():
    i+=1
    if i == 4:
        altitude = line
        altitude = float(altitude) - 6371
        newContent = newContent + str(altitude) + "\n"
        i = 0

file = open("Altitudes.txt","w")
file.write(newContent)
file.close()

## --- STORING ALTITUDES COUNT IN ALTITUDE BANDS FOR HISTOGRAM ---
# Altitudes array to store altitudes for histogram
altitudes = []
# Open and read altitudes
file = open("Altitudes.txt","r")
content = file.read()
file.close()

# Store the altitudes in a 1D array
for line in content.splitlines():
    altitudes.append(float(line))

# Create 1D array to store altitude bands
altitudeBand = [0]
i=0
# Create altitude bands at designated width
barWidth = 5
while max(altitudeBand) < max(altitudes):
    if i == 0:
        altitudeBand[i] = int(min(altitudes)//barWidth * barWidth)
    else:
        altitudeBand.append(altitudeBand[i-1] + barWidth)
    i+=1

# Create empty 1D array of same size as altitude bands array
altitudeNum = [0]*len(altitudeBand)
# Sort altitudes for faster processing
altitudes = sorted(altitudes)

# Count number of each altitudes for each band
i=0
j=0
maxConsidered = 1500
while i < len(altitudes):
    if (altitudes[i] > altitudeBand[j]) & (altitudes[i] < altitudeBand[j+1]):
        altitudeNum[j] += 1
        i+=1
    else:
        j += 1
    if altitudeBand[j] > maxConsidered:
        break

# Remove any empty data beyond limit (there must be a bug, but at least this neatens the data up)
i = len(altitudeBand)
while i > 0:
    if altitudeNum[i-1] != 0:
        break
    else:
        altitudeNum.pop(i-1)
        altitudeBand.pop(i-1)
        i-=1

# Write into text file for MATLAB plotting
file = open("AltitudeBands2.csv", "w")
for i in range (len(altitudeBand)):
    toWrite = str(altitudeBand[i])
    file.write(str(toWrite + ","))

file.write("\n")
for i in range(len(altitudeNum)):
    toWrite = str(altitudeNum[i])
    file.write(toWrite + ",")

file.close()