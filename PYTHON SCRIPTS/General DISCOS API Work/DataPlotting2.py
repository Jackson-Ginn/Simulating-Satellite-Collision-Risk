import requests
import time
import os
from get_token import get_token
import numpy as np

def extractSatData(item):
    attributes = item.get("attributes", {})
    epoch = attributes.get("firstEpoch")
    obj_class = attributes.get("objectClass")
    epoch_year = int(epoch[:4])
    return obj_class, epoch_year

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

def extractData(response):
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

def writeDataToFile(data,file_name):
    with open(file_name+".csv", "w", encoding="utf-8") as f:
        # Write header
        f.write("Epoch Year," + ",".join(object_classes) + "\n")
        # Write data rows
        for i in range(len(epoch_years)):
            row = [str(data[i][0])] + [str(data[i][j]) for j in range(1, len(object_classes)+1)]
            f.write(",".join(row) + "\n")

def checkResponse(response):
    if response.status_code != 200:
        print(response.text)
        input("Halt")
        return False
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

URL = "https://discosweb.esoc.esa.int"
token = get_token()

headers = {
    "Authorization": f"Bearer {token}",
    "DiscosWeb-Api-Version": "2",
}

batch_size = 100
page = 1
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


while True:
    # Request up to 100 satellites at once
    response = getResponse()

    if checkResponse(response):
        time.sleep(0.1)
        dataStatus()
        checkTotalDataAmount(n,s,total_data)

        data,data_amount = extractData(response)
        total_data += data_amount

        for item in data:
            if checkDataIntegrity(item) and checkSatStatus(item):
                obj_class, epoch_year = extractSatData(item)
                logData(epoch_year, obj_class)
                n += 1
            else:
                s += 1
        page += 1
        if data_amount < batch_size:
            break

writeDataToFile(data_array,"dataRearranged")