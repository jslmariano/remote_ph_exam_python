from flask_restplus import Namespace, fields


class BusinessDto:
    api = Namespace('business', description='business related operations')
    business = api.model('business', {
    })
