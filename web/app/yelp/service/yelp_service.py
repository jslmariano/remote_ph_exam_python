# Built-ins
import io
import os
import json
import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
from contextlib import closing

# 3rd parties
from bs4 import BeautifulSoup

# Models
from ..service.google_vision_service import batch_detect_faces_uri

# YELP FUSION APIS
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
        images_annotations = batch_detect_faces_uri(user_image_urls)

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


def scrape_reviews_api(business_id, start = 0):

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

    url = "https://www.yelp.com/biz/{}/review_feed?{}".format(business_id, query_params_encoded)
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
            format_image_hd_link
            image_url = os.path.basename(image_url)
            review['user_image_url'] = image_url
            if image_url == "/images/No-image-found.jpg":
                # User has no photo
                continue
            user_image_urls.append(image_url)

        # Batch process image anotations, to avoid one by one request
        images_annotations = batch_detect_faces_uri(user_image_urls)

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


def scrape_reviews_page(business_alias):
    payload = {}
    headers = {
        'X-Requested-By-React': 'true',
    }

    url = "https://www.yelp.com/biz/{}".format(business_alias)
    print("requesting: {}".format(url))
    content = simple_get(url)

    if content is None:
        return []

    soup = BeautifulSoup(content, 'html.parser')
    review_user_images_elems = soup.select('ul img[class*=photo-box-img][srcset]')
    review_user_names_elems = soup.select('ul div[class*=user] a[href*="/user_details?userid"][rel]')

    review_lists = []
    user_image_urls = []

    # Map user avatar images
    total = 0
    for _elems in review_user_images_elems:
        image_url = format_image_hd_link(_elems['src'])
        image_dict = dict()
        image_dict['user_image_url'] = image_url
        review_lists.append(image_dict)
        total += 1
        if image_url == "/images/No-image-found.jpg":
            # User has no photo
            continue
        user_image_urls.append(image_url)

    # Map user names and ID
    total = 0
    for _elems in review_user_names_elems:
        _user_id = str(_elems['href']).replace('/user_details?userid=', '')
        review_lists[total]['user'] = dict()
        review_lists[total]['user']['name'] = _elems.text
        review_lists[total]['user']['id'] = _user_id
        total += 1

    if not total:
        return {'reviews' : review_lists}

    # Batch process image anotations, to avoid one by one request
    # images_annotations = batch_detect_faces_uri(user_image_urls)

    # # # Map all anotations to reviews
    # for images_annotation in images_annotations:
    #     # REF :
    #     # https://www.geeksforgeeks.org/python-find-dictionary-matching-value-in-list/
    #     # Using next() + dictionary comprehension Find dictionary matching
    #     # value in list
    #     res = next((review for review in review_lists if review['user_image_url'] == images_annotation['from_url']), None)
    #     if res:
    #         res['images_annotation'] = images_annotation

    return {'reviews' : user_image_urls}


def format_image_hd_link(image_url):
    img_basename = os.path.basename(image_url)
    if img_basename == "user_60_square.png":
        # User has no photo
        return "/images/No-image-found.jpg"

    img_name, img_ext =  img_basename.split(".")
    new_img_basename = "o.{}".format(img_ext)
    image_url = image_url.replace(img_basename, new_img_basename)
    return image_url


def get_formated_api(api_path, query_params):
    query_params = urlencode(query_params)
    return "{}/{}?{}".format(YELP_DOMAIN, api_path, query_params)


def get_yelp_credential(filename):
    with open(filename) as f_in:
       return(json.load(f_in))


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(requests.get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)