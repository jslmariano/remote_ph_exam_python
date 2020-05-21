# Flask
from flask_restplus import Namespace, fields

# Namespace
class BusinessDto:
    api = Namespace('business', description='business related operations')
    business = api.model('business', {
    })
