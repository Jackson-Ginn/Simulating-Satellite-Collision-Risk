from pprint import pprint
import requests
from get_token import get_token

URL = 'https://discosweb.esoc.esa.int'
token = get_token()

response = requests.get(
    f'{URL}/api/reentries',
    headers={
        'Authorization': f'Bearer {token}',
        'DiscosWeb-Api-Version': '2',
    },
    params={
        'include': "objects",
        },
)

doc = response.json()
if response.ok:
    pprint(doc['data'])
else:
    pprint(doc['errors'])