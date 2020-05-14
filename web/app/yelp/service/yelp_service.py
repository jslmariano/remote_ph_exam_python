import io
import os
import json
import requests
from urllib.parse import urlencode

from ..service.google_vision_service import detect_faces_uri_multple

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

    user_image_urls = []

    # If theres reviews then we proceed to google vision api, little overhead
    # here though
    if "reviews" in response_dict:

        # Get all user image urls
        for review in response_dict['reviews']:
            # shift user.umage_url to parent level for easy lookup later
            image_url = review['user']['image_url']
            review['user_image_url'] = image_url
            user_image_urls.append(image_url)

        # Batch process image anotations, to avoid one by one request
        images_annotations = detect_faces_uri_multple(user_image_urls)

        # # Map all anotations to reviews
        for images_annotation in images_annotations:
            # REF :
            # https://www.geeksforgeeks.org/python-find-dictionary-matching-value-in-list/
            # Using next() + dictionary comprehension Find dictionary matching
            # value in list
            res = next((review for review in response_dict['reviews'] if review['user_image_url'] == images_annotation['from_url']), None)
            if res:
                res['images_annotation'] = images_annotation

    return response_dict


def scrape_reviews_api(business_alias, start = 0):

    payload = {}
    headers = {
        'X-Requested-By-React': 'true',
    }

    query_params = dict()
    query_params['start'] = start
    query_params['rl'] = 'en'
    query_params['sort_by'] = 'relevance_desc'
    # Somehow not needed for now
    # query_params['q'] = None

    query_params_encoded = urlencode(query_params)

    # https://www.yelp.com/biz/cqziEtN_g3P2pqxaD7Qj2g/review_feed?rl=en&sort_by=relevance_desc&q=&start=20
    url = "https://www.yelp.com/biz/{}/review_feed?{}".format(business_alias, query_params_encoded)
    response = requests.request("GET", url, headers=headers, data = payload)
    response_dict = response.json()

    user_image_urls = []

    # If theres reviews then we proceed to google vision api, little overhead
    # here though
    if "reviews" in response_dict:

        # Get all user image urls
        for review in response_dict['reviews']:
            # layout compatiblities
            review['user']['name'] = review['user']['altText']
            # shift user.umage_url to parent level for easy lookup later
            image_url = review['user']['src']
            # little modification to get the HD pic
            img_basename = os.path.basename(image_url)
            if img_basename == "user_60_square.png":
                # User has no photo
                review['user_image_url'] = None
                continue
            img_name, img_ext =  img_basename.split(".")
            new_img_basename = "o.{}".format(img_ext)
            image_url = image_url.replace(img_basename, new_img_basename)
            review['user_image_url'] = image_url
            user_image_urls.append(image_url)

        # Batch process image anotations, to avoid one by one request
        images_annotations = detect_faces_uri_multple(user_image_urls)

        # # Map all anotations to reviews
        for images_annotation in images_annotations:
            # REF :
            # https://www.geeksforgeeks.org/python-find-dictionary-matching-value-in-list/
            # Using next() + dictionary comprehension Find dictionary matching
            # value in list
            res = next((review for review in response_dict['reviews'] if review['user_image_url'] == images_annotation['from_url']), None)
            if res:
                res['images_annotation'] = images_annotation

    return response_dict

def scrape_reviews_page(business_id):
    return []

def get_formated_api(api_path, query_params):
    query_params = urlencode(query_params)
    return "{}/{}?{}".format(YELP_DOMAIN, api_path, query_params)

def get_yelp_credential(filename):
    with open(filename) as f_in:
       return(json.load(f_in))

