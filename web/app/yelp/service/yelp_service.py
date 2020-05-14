import io
import os
import json
from urllib.parse import urlencode

import requests


YELP_DOMAIN = "https://api.yelp.com"
YELP_API_BUSINESS_SEARCH = "v3/businesses/search"

def test_yelp():

    filters = dict()
    # MANILA !!
    filters['latitude'] = '14.6091'
    filters['longitude'] = '121.0223'

    filters['term'] = 'spiral'

    print(get_formated_api(filters))
    print(os.getenv('YELP_CREDENTIALS', None))
    print(get_yelp_credential(os.path.abspath(os.getenv('YELP_CREDENTIALS', None))))

    yelp_credential = get_yelp_credential(os.path.abspath(os.getenv('YELP_CREDENTIALS', None)))

    payload = {}
    headers = {
      'Authorization': "Bearer {}".format(yelp_credential['api_key']),
    }

    response = requests.request("GET", get_formated_api(filters), headers=headers, data = payload)

    return response.json()

def get_formated_api(query_params):
    query_params = urlencode(query_params)
    return "{}/{}?{}".format(YELP_DOMAIN, YELP_API_BUSINESS_SEARCH, query_params)

def get_yelp_credential(filename):
    with open(filename) as f_in:
       return(json.load(f_in))

