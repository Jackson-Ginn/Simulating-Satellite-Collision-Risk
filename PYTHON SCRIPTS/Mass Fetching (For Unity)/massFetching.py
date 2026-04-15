import requests
import time
import os
from get_token import get_token
import numpy as np

tle_file = "TLE Satellite Data 2026-04-02.txt"
output_file = "satellite_masses.txt"
batch_size = 100

def extractSatData(item):
    attributes = item.get("attributes", {})
    satno = str(attributes.get("satno"))
    satno = satno.zfill(5)
    mass = attributes.get("mass")

    if mass is not None:
        mass = str(mass)
    else:
        mass = '-1'

    return satno, mass

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

def extractRawData(response):
    doc = response.json()
    data = doc.get("data", [])
    return data, len(data) 

def writeDataToFileCSV(data, file_name, header):
    with open(file_name + ".csv", "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for row in data:
            f.write(",".join(str(x) for x in row) + "\n")

def writeDataToFileLE(data,file_name, header):
    with open(file_name + ".txt", "w") as f:
        f.write(header+"\n")
        for i in range(len(data)):
            f.write(str(data[i])+"\n")

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

def checkTotalDataAmount(total_data):
    print("Total objects processed so far", total_data)

def storeData(array,data):
    for i in range(len(data)):
        array.append(data[i])

def TLEsatnoArray(tleData):
    NameSatnoArray = []
    for i in range(0, len(tleData), 3):
        name = tleData[i].strip()
        satno = tleData[i+1][2:7].strip()

        item = [str(name), str(satno)]
        NameSatnoArray.append(item)

    return NameSatnoArray

URL = "https://discosweb.esoc.esa.int"
token = get_token()

headers = {
    "Authorization": f"Bearer {token}",
    "DiscosWeb-Api-Version": "2",
}

####            __MAIN__            ####

# Get array with TLE name (for Unity) and satellite number, satno
input("Phase 1 Ready")
with open(tle_file, "r", encoding="utf-8") as f:
    tleData = f.readlines()
    TLEnameANDsatno = TLEsatnoArray(tleData)

for name, satno in TLEnameANDsatno:
    print(name)
    print(satno)

# Get array with satellite number, satno and mass from DISCOS
input("Phase 2 Ready")
page = 1;total_data=0
DISCOSsatnoANDmass= []
while True:
    # Request up to 100 satellites at once and give API 0.1s break
    time.sleep(0.1)
    response = getResponse(batch_size)

    if checkResponse(response):

        data, data_amount = extractRawData(response)
        total_data += data_amount

        checkTotalDataAmount(total_data)

        for item in data:
            satno, mass = extractSatData(item)
            toStore = [satno,mass]
            storeData(DISCOSsatnoANDmass,toStore)
        
        if data_amount < batch_size:
            break
        else:
            page+=1

writeDataToFileLE(DISCOSsatnoANDmass,"DISCOSsatnoANDmass","satno/mass")

input("Phase 3 Ready")
# Equate in file
fullData = []
for name,satno in TLEnameANDsatno:
    try:
        index = DISCOSsatnoANDmass.index(satno)
    except:
        index = -1

    if index !=-1:
        mass = DISCOSsatnoANDmass[index+1]

        toStore = [name,satno, mass]
        storeData(fullData, toStore)
        print(str(name)+" "+str(satno) + " found in TLE data, saving mass...")

    else:
        print(str(name)+" "+str(satno)+" not in TLE data...")

writeDataToFileLE(fullData,"fullData","name/satno/mass")