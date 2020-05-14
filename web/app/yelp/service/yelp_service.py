import io
import os
import json
from urllib.parse import urlencode

import requests


YELP_DOMAIN = "https://api.yelp.com"
YELP_API_BUSINESS_SEARCH = "v3/businesses/search"
YELP_API_BUSINESS_REVIEWS = "v3/businesses/{}/reviews"

def business_search(term):

    filters = dict()
    # MANILA !!
    filters['latitude'] = '14.6091'
    filters['longitude'] = '121.0223'

    if term is not None:
        filters['term'] = str(term)

    yelp_credential = get_yelp_credential(
        os.path.abspath(os.getenv('YELP_CREDENTIALS', None))
    )

    payload = {}
    headers = {
      'Authorization': "Bearer {}".format(yelp_credential['api_key']),
    }

    url = get_formated_api(YELP_API_BUSINESS_SEARCH, filters)
    response = requests.request("GET", url,headers=headers, data = payload)

    return response.json()


def business_reviews(business_alias):

    yelp_credential = get_yelp_credential(
        os.path.abspath(os.getenv('YELP_CREDENTIALS', None))
    )

    payload = {}
    headers = {
      'Authorization': "Bearer {}".format(yelp_credential['api_key']),
    }

    url = get_formated_api(YELP_API_BUSINESS_REVIEWS.format(business_alias), {})
    response = requests.request("GET", url, headers=headers, data = payload)
    response_dict = response.json()

    # If theres reviews then we proceed to google vision api, little overhead
    # here though
    if "reviews" in response_dict:
        pass

    return response_dict

def get_formated_api(api_path, query_params):
    query_params = urlencode(query_params)
    return "{}/{}?{}".format(YELP_DOMAIN, api_path, query_params)

def get_yelp_credential(filename):
    with open(filename) as f_in:
       return(json.load(f_in))

