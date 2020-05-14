import io
import os

import requests


YELP_DOMAIN = "https://api.yelp.com"
YELP_API_BUSINESS_SEARCH = "businesses/search"

def test_yelp():

    url = "https://api.yelp.com/v3/businesses/search?term=spiral&latitude=14.6091&longitude=121.0223"

    payload = {}
    headers = {
      'Authorization': 'Bearer dochXjYD-AT9mGVgd83tk9opUlJQ3ARfEPxX47puAfSSYn6KAQUFlsDRFGVeVgkJAXs_KKEwCCPv4xlZWfvM33REymKhBlScdrN2k9clCaTWssbEd3nQiYCzcT28XnYx',
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    return response.json()

def get_formated_api():
    return "{}/{}".format(YELP_DOMAIN, YELP_API_BUSINESS_SEARCH)