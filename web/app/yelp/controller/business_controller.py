from flask import request
from flask_restplus import Resource

from ..util.dto import BusinessDto
from ..service.google_vision_service import detect_faces_uri, detect_faces_uri_multple
from ..service.yelp_service import business_search, business_reviews

api = BusinessDto.api
_business = BusinessDto.business

@api.route('/')
class BusinessList(Resource):

    @api.doc('list_of_yelp_business')
    def get(self):
        """List all registered users"""
        return {'message': 'Hello, I am your backend'}


@api.route('/face')
class BusinessTest(Resource):

    @api.doc('get_face_emotion_google_vision')
    def get(self):
        """List all registered users"""
        faces_emotions = detect_faces_uri()
        result = dict()
        result['message'] = 'Hello, I am your backend'
        result['faces_emotions'] = faces_emotions
        return result

@api.route('/multiple_faces')
class BusinessTest(Resource):

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
class BusinessSearch(Resource):

    @api.doc('yelp_business_search')
    def get(self):
        """List all registered users"""

        alias = request.args.get('alias')
        result = dict()
        result['message'] = 'Hello, I am your backend'
        result['business_reviews'] = business_reviews(alias)
        return result

