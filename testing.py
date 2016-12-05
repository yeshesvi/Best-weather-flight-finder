import json
import requests
from datetime import date
from pprint import pprint

fdate = date.today()
api_key = "AIzaSyB88DDPzNdz5bbUDSdSpLXE2nTgd0-bAj4"
url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
headers = {'content-type': 'application/json'}

params = {
  "request": {
    "slice": [
      {
        "origin": "DTW",
        "destination": "ORD",
        "date": fdate.isoformat()
      }
    ],
    "passengers": {
      "adultCount": 1
    },
    "solutions": 3,
    "refundable": False
  }
}
try:
    response = requests.post(url, data=json.dumps(params), headers=headers)
    flightdata = response.json()
    'error' not in flightdata.keys


except Exception:
    print "online data unavailable, or daily limit reached. Trying to find chache file."
    with open('flightfile.txt') as json_data:# This is to use the cache file instead of calling in data all the time.
        flightdata = json.load(json_data)

pprint(flightdata)
