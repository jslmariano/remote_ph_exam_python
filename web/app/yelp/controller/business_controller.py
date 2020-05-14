from flask import request
from flask_restplus import Resource

from ..util.dto import BusinessDto
from ..service.google_vision_service import detect_faces_uri, detect_faces_uri_multple
from ..service.yelp_service import business_search
from ..service.yelp_service import business_reviews
from ..service.yelp_service import scrape_reviews_api
from ..service.yelp_service import scrape_reviews_page

api = BusinessDto.api
_business = BusinessDto.business

@api.route('/')
class BusinessIndex(Resource):

    @api.doc('home_message')
    def get(self):
        """List all registered users"""
        return {'message': 'Hello, I am your backend'}


@api.route('/face')
class BusinessFace(Resource):

    @api.doc('get_face_emotion_google_vision')
    def get(self):
        """List all registered users"""
        faces_emotions = detect_faces_uri()
        result = dict()
        result['message'] = 'Hello, I am your backend'
        result['faces_emotions'] = faces_emotions
        return result


@api.route('/multiple_faces')
class BusinessMultipleFaces(Resource):

    @api.doc('get_face_emotion_google_vision')
    def get(self):
        """List all registered users"""
        faces_emotions = detect_faces_uri_multple()
        result = dict()
        result['message'] = 'Hello, I am your backend'
        result['faces_emotions'] = faces_emotions
        return result


@api.route('/search')
class BusinessSearch(Resource):

    @api.doc('yelp_business_search')
    def get(self):
        """List all registered users"""

        term = request.args.get('term')
        result = dict()
        result['message'] = 'Hello, I am your backend'
        result['business_search'] = business_search(term)
        return result


@api.route('/reviews')
class BusinessReviews(Resource):

    @api.doc('yelp_business_reviews')
    def get(self):
        """List all registered users"""

        alias = request.args.get('alias')
        result = dict()
        result['message'] = 'Hello, I am your backend'
        result['business_reviews'] = business_reviews(alias)
        return result


@api.route('/scrape_reviews_api')
class BusinessScrapeReviewsApi(Resource):

    @api.doc('yelp_scrape_reviews_api')
    def get(self):
        """List all registered users"""

        business_id = request.args.get('business_id')
        result = dict()
        result['message'] = 'Hello, I am your backend'
        result['business_reviews'] = scrape_reviews_api(business_id)
        return result


@api.route('/scrape_reviews_page')
class BusinessScrapeReviewsPage(Resource):

    @api.doc('yelp_scrape_reviews_page')
    def get(self):
        """List all registered users"""

        business_id = request.args.get('business_id')
        result = dict()
        result['message'] = 'Hello, I am your backend'
        result['business_reviews'] = scrape_reviews_page(business_id)
        return result

