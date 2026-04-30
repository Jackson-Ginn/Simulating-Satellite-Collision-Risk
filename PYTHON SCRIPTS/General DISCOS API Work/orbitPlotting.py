import requests
from get_token import get_token

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
}
def getResponse(req):
    response = requests.get(
        f"{URL}/api{req}",
        headers=headers,
        params=params,
    )
    return response

data = getResponse('/destination-orbits').json().get("data", [])

for item in data:
    print(item)
    input("next")