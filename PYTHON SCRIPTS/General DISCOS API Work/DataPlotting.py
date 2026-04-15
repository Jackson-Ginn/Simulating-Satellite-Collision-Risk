import requests
import time
import os
from get_token import get_token
import numpy as np

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

URL = "https://discosweb.esoc.esa.int"
token = get_token()

headers = {
    "Authorization": f"Bearer {token}",
    "DiscosWeb-Api-Version": "2",
}

batch_size = 100

## --- Get satellite first epoch and object class from API ---

# Define object classes array
object_classes = [
    "Rocket Body",
    "Rocket Mission Related Object",
    "Rocket Fragmentation Debris",
    "Rocket Debris",
    "Payload",
    "Payload Mission Related Object",
    "Payload Fragmentation Debris",
    "Payload Debris",
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

# A check for whether all data is gathered or not
recieved_data = 100
total_data = 0
c=1;n=0
while recieved_data == 100:
# Request up to 100 satellites at once
    response = requests.get(
        f"{URL}/api/objects",
        headers=headers,
        params={
            "page[size]": 100,
            "page[number]": c
        },
    )

    if response.ok:
        
        doc = response.json()
        data = doc.get("data", [])

        # Check how many sats returned
        recieved_data = len(data)
        print("Call Number",c)
        print("Objects returned", recieved_data)
        total_data += recieved_data
        print("Total objects processed so far", total_data)

        # Get data from response
        for item in data:
            attributes = item.get("attributes", {})
            epoch1 = attributes.get("firstEpoch")
            reentry_epoch = attributes.get("reentryEpoch")
            predicted_decay_epoch = attributes.get("predictedDecay")
            reentry_year = reentry_epoch[:4] if reentry_epoch else None
            predicted_decay_year = predicted_decay_epoch[:4] if predicted_decay_epoch else None
            obj_class = attributes.get("objectClass")
            if epoch1 is not None and obj_class is not None:
                epoch_year = int(epoch1[:4])
                epoch_year = epoch_year - (epoch_year % 2)  # Round down to nearest even year
                if obj_class not in object_classes or epoch_year not in epoch_years or (epoch_year < 1960 or epoch_year > 2026):
                    #input("Total fuckup")
                    pass
                else:
                    if checkSatStatus(item):
                        logData(epoch_year, obj_class)
                        n += 1
                        print("Actual Data Points Gathered", n)
    else:
        print(response.text)
        input()
    # Wait between 100 API calls
    time.sleep(0.05) 
    c+=1

# Write data to file as CSV
with open("data.csv", "w", encoding="utf-8") as f:
    # Write header
    f.write("Epoch Year," + ",".join(object_classes) + "\n")
    # Write data rows
    for i in range(len(epoch_years)):
        row = [str(data_array[i][0])] + [str(data_array[i][j]) for j in range(1, len(object_classes)+1)]
        f.write(",".join(row) + "\n")