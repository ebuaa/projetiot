import requests
import json 

URL = "http://172.20.10.2:5000/api/releves"
DATA = {
    "humidite": 60,
    "temperature": 40,
    "pression": 1024,
}

DATA = json.dumps(DATA)
TYPE = "application/json"

response = requests.post(url=URL, data=DATA, headers={'Content-Type': TYPE})

print(response)