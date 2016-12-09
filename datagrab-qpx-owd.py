import requests
import json
import datetime
from datetime import timedelta, datetime, date
from pprint import pprint

fromcity = 'DTW'
tocity = 'ORD'

USING_CACHE = False

class Flights:
    numFlights = 0
    def __init__(self, fname, fnum, fprice, farrival, fduration):
        self.name = str(fname)+str(fnum)
        self.cost = fprice
        self.arrival = farrival
        self.duration = fduration
        Flights.numFlights+=1

#Code includes cache file to get data from QPX for 5 flights from DTW to ORD for one passenger on Dec 3


def flightperdate(fdate):
    api_key = "AIzaSyB88DDPzNdz5bbUDSdSpLXE2nTgd0-bAj4"
    url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
    headers = {'content-type': 'application/json'}

    params = {
      "request": {
        "slice": [
          {
            "origin": fromcity,
            "destination": tocity,
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
        # This is to use the cache file when live data is not available, only 5 flights TODO cache  a 20 flight journey
        USING_CACHE= True
        with open('flightfile.txt') as json_data:
            flightdata = json.load(json_data)
            json_data.close()

    listOfFlights = []
    def flightconstructor(flightdata):
        for foption in flightdata['trips']['tripOption']:
            listOfFlights.append(Flights(fprice=foption['saleTotal'],
                                         fduration=foption['slice'][0]['duration'],
                                         fname=foption['slice'][0]['segment'][0]['flight']['carrier'],
                                         fnum=foption['slice'][0]['segment'][0]['flight']['number'],
                                         farrival=foption['slice'][0]['segment'][0]['leg'][-1]['arrivalTime']))


    flightconstructor(flightdata)
    # print fdate
    # for f in listOfFlights:
    #     print f.name
    #     print f.cost
    #flight caching file printing Code
    # flightout = open('flightfile.txt', 'w')
    # json.dump(flightdata, flightout)
    # flightout.close()
    return listOfFlights

def getCityName(tocity):
    url_parameters = {'format':'json'}


    baseurl = 'http://services.faa.gov/airport/status/'
    airport = tocity

    # airport_response = requests.get(baseurl+airport, params =url_parameters)

    try:
        airport_response = requests.get(baseurl+airport, params =url_parameters)
        airport_data = json.loads(airport_response.text)
    except Exception:
        print "That didn't work"
        airport_data = {}

        airport_data['city'] = "Chicago" # TODO have a chache file with city names and airport codes


    return airport_data['city']

def getWeatherData():
    #get city name from airport Code
    city = getCityName(tocity)
    #Code to get data from openweathermap api for the destination city.
    # api.openweathermap.org/data/2.5/forecast/daily?q=London&mode=xml&units=metric&cnt=7
    try:
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?q={}&units=imperial&cnt=15&APPID=8579ca251c0a64d55baf34b3b588214b'.format(city))
        weatherdata = json.loads(r.text)
    except Exception:
        print "Online data unavailable, Trying chache data!"
        with open('weatherfile.txt') as json_data:
            weatherdata = json.load(json_data)
    return weatherdata

def getFlightDict():
    today = date.today()
    a=1
    flightdict={}
    while a<16:
        fdate = today + timedelta(days=a)
        flightdict[fdate] = flightperdate(fdate)
        a=a+1
    return flightdict

#### MAIN EXECUTION STARTS HERE ##########

#Flight dict is a dictionary that contains dates as keys and instances of the flights available as values
flightdict = getFlightDict()

#weatherdata contains weatherdata for the provided tocity's 15 day weather. It needs to be passed through class to parse it #TODO
weatherdata = getWeatherData()

if USING_CACHE:
    print "Hello, we are using cache files for one or more datasets as a result the result shown is for DTW to ORD as executed on DEC 3" #TODO update and fix this line
#### MANUAL TESTING CODE !! PLEASE IGNORE ######

# for i in flightdict.keys():
#     print i.isoformat()
#     for f in flightdict[i]:
#         print f.name
#     print "\n"*7

#caching weather results
# weatherout = open('weatherfile.txt', 'w')
# wdict = r.json()
# json.dump(wdict, weatherout)
# weatherout.close()
