from flask import request
from flask_restplus import Resource

from ..util.dto import BusinessDto

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
        return {'message': 'Hello, I am your backend'}

