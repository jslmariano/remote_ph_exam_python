from flask import request
from flask_restplus import Resource

from ..util.dto import BusinessDto
from ..service.google_vision_service import test_google_vision

api = BusinessDto.api
_business = BusinessDto.business

@api.route('/')
class BusinessList(Resource):

    @api.doc('list_of_yelp_business')
    def get(self):
        """List all registered users"""
        return {'message': 'Hello, I am your backend'}


@api.route('/test')
class BusinessCsv(Resource):

    @api.doc('just_a_test')
    def get(self):
        """List all registered users"""
        test_google_vision()
        return {'message': 'Hello, I am your backend'}

