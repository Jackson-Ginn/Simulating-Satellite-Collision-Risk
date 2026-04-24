import requests
import time
import csv
from get_token import get_token

# Lord gpts effort

fileName = "EarthEnvironmentData"

batch_size = 100
URL = "https://discosweb.esoc.esa.int"

token = get_token()

headers = {
    "Authorization": f"Bearer {token}",
    "DiscosWeb-Api-Version": "2",
}

object_classes = [
    "Payload",
    "Payload Mission Related Object",
    "Payload Fragmentation Debris",
    "Payload Debris",
    "Rocket Body",
    "Rocket Mission Related Object",
    "Rocket Fragmentation Debris",
    "Rocket Debris",
    "Unknown",
]

epoch_years = list(range(1960, 2027, 2))


def get_response(endpoint, page, include=None):
    params = {
        "page[size]": batch_size,
        "page[number]": page,
    }

    if include:
        params["include"] = include

    response = requests.get(
        f"{URL}/api{endpoint}",
        headers=headers,
        params=params,
        timeout=30,
    )

    return response


def check_response(response):
    if response.status_code != 200:
        print("Request failed:")
        print(response.status_code)
        print(response.text)
        return False

    print("Response good")
    return True


def fetch_all(endpoint, include=None):
    page = 1
    all_data = []
    all_included = []

    while True:
        print(f"Fetching {endpoint}, page {page}")

        response = get_response(endpoint, page, include=include)

        if not check_response(response):
            break

        payload = response.json()
        data = payload.get("data", [])
        included = payload.get("included", [])

        all_data.extend(data)
        all_included.extend(included)

        if len(data) < batch_size:
            break

        page += 1

        # Be polite to the API
        time.sleep(0.2)

    return all_data, all_included


# -----------------------------
# Fetch reentry data
# -----------------------------

reentries, included_objects = fetch_all("/reentries", include="objects")

# Map DISCOs object id -> satno
object_id_to_satno = {}

for item in included_objects:
    obj_id = item.get("id")
    attributes = item.get("attributes", {})
    satno = attributes.get("satno")

    if obj_id is not None:
        object_id_to_satno[obj_id] = satno


# Build satno -> reentry epoch
satno_to_reentry_epoch = {}

for item in reentries:
    attributes = item.get("attributes", {})
    reentry_epoch = attributes.get("epoch")

    refs = (
        item.get("relationships", {})
        .get("objects", {})
        .get("data", [])
    )

    if not refs:
        continue

    obj_id = refs[0].get("id")
    satno = object_id_to_satno.get(obj_id)

    if satno is not None:
        satno_to_reentry_epoch[satno] = reentry_epoch


# -----------------------------
# Fetch object data
# -----------------------------

objects, _ = fetch_all("/objects")

final_data = []

for item in objects:
    attributes = item.get("attributes", {})

    satno = attributes.get("satno")
    first_epoch = attributes.get("firstEpoch")
    obj_class = attributes.get("objectClass")
    reentry_epoch = satno_to_reentry_epoch.get(satno)

    final_data.append({
        "satno": satno,
        "firstEpoch": first_epoch,
        "reentryEpoch": reentry_epoch,
        "objectClass": obj_class,
    })


# -----------------------------
# Save to CSV
# -----------------------------

output_file = f"{fileName}.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["satno", "firstEpoch", "reentryEpoch", "objectClass"]
    )

    writer.writeheader()
    writer.writerows(final_data)

print(f"Saved {len(final_data)} rows to {output_file}")