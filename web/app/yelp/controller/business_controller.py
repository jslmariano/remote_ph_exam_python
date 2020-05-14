from flask import request
from flask_restplus import Resource

from ..util.dto import BusinessDto
from ..service.google_vision_service import detect_faces_uri
from ..service.yelp_service import test_yelp

api = BusinessDto.api
_business = BusinessDto.business

@api.route('/')
class BusinessList(Resource):

    @api.doc('list_of_yelp_business')
    def get(self):
        """List all registered users"""
        return {'message': 'Hello, I am your backend'}


@api.route('/test')
class BusinessTest(Resource):

    @api.doc('just_a_test')
    def get(self):
        """List all registered users"""
        faces_emotions = detect_faces_uri()
        result = dict()
        result['message'] = 'Hello, I am your backend'
        result['faces_emotions'] = faces_emotions
        return result


@api.route('/yelp')
class BusinessYelp(Resource):

    @api.doc('test_yelp')
    def get(self):
        """List all registered users"""
        result = dict()
        result['message'] = 'Hello, I am your backend'
        result['test_yelp'] = test_yelp()
        return result

