import requests
import time
import os
from get_token import get_token
import numpy as np
fileName = "EarthEnvironmentData"


def extractSatData(item):
    attributes = item.get("attributes", {})
    start = attributes.get("firstEpoch")
    obj_class = attributes.get("objectClass")
    end = attributes.get("reEntryEpoch")

    print(item)

    id = attributes.get("satno")

    if end == None:
        end = '9999'

    print(id,end)

    start = int(start[:4])
    end = int(end[:4])

    input("Next")

    return obj_class, start, end

def logData(epoch_year, obj_class):
    i = epoch_years.index(epoch_year)
    j = object_classes.index(obj_class)+1
    data_array[i][j] += 1

def checkSatStatus(item):   
    attributes = item.get("attributes", {})
    reentry_epoch = attributes.get("reentryEpoch")
    predicted_decay_epoch = attributes.get("predictedDecay")
    if reentry_epoch is not None and predicted_decay_epoch is not None:
        reentry_year = int(reentry_epoch[:4])
        predicted_decay_year = int(predicted_decay_epoch[:4])
        if reentry_year < 2026 or predicted_decay_year < 2026:
            return False
    return True

def getResponse():
    response = requests.get(
        f"{URL}/api/objects",
        headers=headers,
        params={
            "page[size]": 100,
            "page[number]": page
        },
    )
    return response

def extractRawData(response):
    doc = response.json()
    data = doc.get("data", [])
    return data, len(data) 

def checkDataIntegrity(item):
    attributes = item.get("attributes", {})
    epoch = attributes.get("firstEpoch")
    obj_class = attributes.get("objectClass")
    if epoch is not None and obj_class is not None:
        epoch_year = int(epoch[:4])
        if epoch_year in epoch_years and obj_class in object_classes:
            return True

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

def storeData(obj_class, start, end):
    raw_data.append([obj_class, start, end])


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
    response = getResponse()

    if checkResponse(response):
        time.sleep(0.1)

        data,data_amount = extractRawData(response)
        total_data += data_amount

        for item in data:
            if checkDataIntegrity(item):
                obj_class, start_year, end_year = extractSatData(item)
                storeData(obj_class, start_year, end_year)
        page += 1
        if data_amount < batch_size:
            break

print(raw_data)
input("Halt")
# Put data from array into plotting format
writeDataToFile(raw_data,"rawData","Object Class,Start Year,End Year")
        
#for i in range(len(epoch_years)):
#    while


#writeDataToFile(data_array,fileName)