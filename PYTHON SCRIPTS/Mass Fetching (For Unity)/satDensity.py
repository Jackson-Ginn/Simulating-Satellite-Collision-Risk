import requests
import time
import os
from get_token import get_token
import numpy as np
fileName = "satDensity"


def extractSatData(item):
    attributes = item.get("attributes", {})
    mass = attributes.get("mass")
    span = attributes.get("span")

    return mass, span

def checkDataStatus(item):   
    attributes = item.get("attributes", {})
    mass = attributes.get("mass")
    shape = attributes.get("shape")
    span = attributes.get("span")
    
    if mass != None and shape == "Sphere" and span != None:
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

def storeData(mass, radius):
    raw_data.append([mass, radius])


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
                mass, span = extractSatData(item)
                storeData(mass, span)
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

writeDataToFile(raw_data,"rawMassAndRadiusData","Satellite Mass, Satellite Radius")

# Get average density from raw data
totalDensity=0
densityArray=[]
for i in range(len(raw_data)-1):
    mass_i = float(raw_data[i+1][0])
    radius_i = float(raw_data[i+1][1])/2
    density_i = (3*mass_i)/(4*np.pi*radius_i**3)
    densityArray.append(density_i)


print(densityArray)
#avgDensity = densityArray.
#writeDataToFile(avgDensity,fileName,"Average Density")