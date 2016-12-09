import json
import requests
from datetime import date
from datetime import timedelta
from pprint import pprint

USING_CACHE = True

def flightperdate(fdate):
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
        "solutions": 5,
        "refundable": False
      }
    }
    try:
        response = requests.post(url, data=json.dumps(params), headers=headers)
        print response.status_code # error code is 403.
        flightdata = response.json()
        return flightdata
    except Exception:
        print "online data unavailable, Please try cached data."


def getFlightDict():
    today = date.today()
    a=1
    flightdict={}
    while a<15:
        fdate = today + timedelta(days=a)
        flightdict[fdate.isoformat()] = flightperdate(fdate)
        a=a+1
    return flightdict

flightdict = getFlightDict()
flightout = open('flightfile.txt', 'w')
json.dump(flightdict, flightout)
flightout.close()
