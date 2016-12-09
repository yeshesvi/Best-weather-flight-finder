from skyscanner.skyscanner import Flights
import requests
import json

flights_service = Flights('un441765848862889553535266199036')
result = flights_service.get_result(
    country='UK',
    currency='GBP',
    locale='en-GB',
    originplace='SIN-sky',
    destinationplace='KUL-sky',
    outbounddate='2017-05-28',
    inbounddate='2017-05-31',
    adults=1).parsed
print(result)

# response = requests.get('http://partners.api.skyscanner.net/apiservices/browsedates/v1.0/GB/GBP/en-GB/LON/JFK/2017-01/2017-01?apiKey=un441765848862889553535266199036')
# print json.loads(response.text)
