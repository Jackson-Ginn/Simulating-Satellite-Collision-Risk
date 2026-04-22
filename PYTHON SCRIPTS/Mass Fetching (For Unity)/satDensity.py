import requests
import time
import os
from get_token import get_token
import numpy as np
import csv
import math
fileName = "satDensity"

def extractSatData(item):
    dimensions = []

    attributes = item.get("attributes", {})

    mass = attributes.get("mass")
    shape =attributes.get("shape")

    if shape == "Sphere":
        span = attributes.get("span")
        dimensions.append(span)
    elif shape == "Cyl":
        span = attributes.get("span")
        height = attributes.get("height")
        dimensions.append(span); dimensions.append(height)
    elif shape == "Box": 
        height = attributes.get("height")
        width = attributes.get("width")
        depth = attributes.get("depth")
        dimensions.append(height); dimensions.append(width); dimensions.append(depth)
    

    return shape, mass, dimensions

def checkDataStatus(item):   
    attributes = item.get("attributes", {})
    mass = attributes.get("mass")
    shape = attributes.get("shape")
    span = attributes.get("span")
    height = attributes.get("height")
    width = attributes.get("width")
    depth = attributes.get("depth")

    if mass != None:
        if shape == "Sphere" and span != None:
            return True
        elif shape == "Box" and height != None and width != None and depth != None:
            return True
        elif shape == "Cyl" and height != None and span != None:
            return True
    return False

def getResponse(batch_size):
    response = requests.get(
        f"{URL}/api/objects",
        headers=headers,
        params={
            "page[size]": batch_size,
            "page[number]": page
        },
    )
    return response

def extractData(response):
    doc = response.json()
    data = doc.get("data", [])
    return data, len(data) 

def writeDataToFile(data, file_name, header):
    with open(file_name + ".csv", "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for row in data:
            f.write(",".join(str(x) for x in row) + "\n")

def checkResponse(response):
    if response.status_code != 200:
        print(response.text)
        input("Halt")
        return False
    else:
        print("Response Good")
        return True

def dataStatus():
    print("Gathered Data Points:", n)
    print("Skipped Data Points:", s)

def checkTotalDataAmount(n,s,total_data):
    if n+s==total_data:
        print("Total objects processed so far", total_data)
    else:
        print("Total objects processed so far", total_data, "but gathered", n, "and skipped", s)
        input("Halt")

def storeData(shape, mass, dimensions):
    toAdd = []
    toAdd.append(shape); toAdd.append(mass)
    for item in dimensions:
        toAdd.append(item)
    raw_data.append(toAdd)


URL = "https://discosweb.esoc.esa.int"
token = get_token()

headers = {
    "Authorization": f"Bearer {token}",
    "DiscosWeb-Api-Version": "2",
}

batch_size = 100
page = 1
raw_data = []

n=0;s=0;total_data=0
## --- Get satellite first epoch and object class from API ---

# Define object classes array
object_classes = [
    "Payload",
    "Payload Mission Related Object",
    "Payload Fragmentation Debris",
    "Payload Debris",
    "Rocket Body",
    "Rocket Mission Related Object",
    "Rocket Fragmentation Debris",
    "Rocket Debris",
    "Unknown"]

# Define epoch years array to cover all epoch years
epoch_years = []
yr = 1960
while yr <= 2026:
    epoch_years.append(yr)
    yr += 2

# Define 2D array for epoch year and object class counts
data_array = np.zeros((len(epoch_years), len(object_classes)+1), dtype=int)
for i in range(len(epoch_years)):
    data_array[i][0] = epoch_years[i]

# Extract from API and put into array
while True:
    # Request up to 100 satellites at once
    response = getResponse(batch_size)

    if checkResponse(response):
        time.sleep(0.1)

        data,data_amount = extractData(response)
        total_data += data_amount

        for item in data:
            if checkDataStatus(item):
                shape, mass, dimensions = extractSatData(item)
                storeData(shape, mass, dimensions)
                n+=1
            else:
                s+=1
                pass

        page += 1
        if data_amount < batch_size:
            break
        dataStatus()
        checkTotalDataAmount(n,s,total_data)
print(raw_data)
input("Halt")

writeDataToFile(raw_data,"rawMassAndDimensionData","Shape, Mass, Dimensions")

# Calc density
totalDensity=0
densityArray=[]
with open("rawMassAndDimensionData.csv", newline="") as f:
    lines = csv.reader(f)

    for line in lines:
        if line[0].strip() == "Shape":
            continue
        shape = line[0]
        mass = float(line[1])
        dimensions = line[2:]

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
        densityArray.append(density)

print(densityArray)
avgDensity = sum(densityArray)/len(densityArray)
print("AVG DENSITY: ",avgDensity)
writeDataToFile(avgDensity,fileName,"Average Density")