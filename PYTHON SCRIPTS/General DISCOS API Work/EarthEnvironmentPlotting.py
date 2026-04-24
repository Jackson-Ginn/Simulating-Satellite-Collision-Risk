import requests
import time
import os
from get_token import get_token
import numpy as np

fileName = "EarthEnvironmentData"

batch_size = 100
page = 1
URL = "https://discosweb.esoc.esa.int"
token = get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "DiscosWeb-Api-Version": "2",}
params={
    "page[size]": batch_size,
    "page[number]": page,
    "include":"objects"}


raw_data = []

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
epoch_years = []
yr = 1960
while yr <= 2026:
    epoch_years.append(yr)
    yr += 2

def getResponse(req):
    response = requests.get(
        f"{URL}/api{req}",
        headers=headers,
        params=params,
    )
    return response

def checkResponse(response):
    if response.status_code != 200:
        print(response.text)
        #input("Halt")
        return False
    else:
        print("Response Good")
        return True
    
reentry_raw = []
included_raw = []

while True:
    response = getResponse('/reentries')
    if checkResponse(response):
        reentryData = response.json().get("data", [])
        for item in reentryData:
            attributes = item.get("attributes", {})
            references = item.get("relationships", {}).get("objects", {}).get("data", [])
            id = references[0].get("id")
            reentryEpoch = attributes.get("epoch")

            reentry_raw.append([id, reentryEpoch])

        objData = response.json().get("included", [])
        for item in objData:
            attributes = item.get("attributes", {})
            id = item.get("id")
            satno = attributes.get("satno")

            included_raw.append([id, satno])
        
        if len(reentryData) < 100 or len(objData) < 100:
            break

        page += 1

assembled_data = []
for i in range(len(reentry_raw)):
    reID = reentry_raw[i][0]
    index = included_raw.index(reID)
    assembled_data.append([included_raw[index,1],reentry_raw[i,1]])

page = 1
object_raw = []
while True:
    response = getResponse('/objects')
    if checkResponse(response):
        data = response.json().get("data", [])
        for item in data:
            attributes = item.get("attributes", {})
            id = attributes.get("satno")
            firstEpoch = attributes.get("firstEpoch")
            objClass = attributes.get("objectClass")

            object_raw.append([id, firstEpoch, objClass])

        if len(data) < 100:
            break

        page += 1

final_data = []
for i in range(len(object_raw)):
    satno = object_raw[i][0]
    index = assembled_data.index(reID)
    final_data.append([assembled_data[index,1],object_raw[i,1]])