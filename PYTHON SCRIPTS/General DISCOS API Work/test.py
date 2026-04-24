import requests
from get_token import get_token

URL = "https://discosweb.esoc.esa.int"
token = get_token()

headers = {
    "Authorization": f"Bearer {token}",
    "DiscosWeb-Api-Version": "2",
}

def get_json(path, params=None):
    r = requests.get(f"{URL}{path}", headers=headers, params=params)
    r.raise_for_status()
    return r.json()

# example: fetch one object
obj_doc = get_json("/api/objects")
print(obj_doc)
obj = obj_doc.get("attributes", {})
print(obj)
print("Object:", obj["id"], obj["attributes"]["name"])

# follow the relationship link to its reentry
reentry_path = obj["relationships"]["reentry"]["links"]["related"]
reentry_doc = get_json(reentry_path)
try:
    a = reentry_doc['data']['attributes']['epoch']
    a = a[:4]
except:
    a = '9999'
print(a)

