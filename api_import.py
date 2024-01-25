import requests
import json 

URL = "http://172.20.10.2/api/releves"
DATA = {
    "humidite": 60,
    "temperature": 35,
    "pression": 1010,
}

DATA = json.dumps(DATA)
TYPE = "application/json"

response = requests.post(url=URL, data=DATA, headers={'Content-Type': TYPE})

print(response)