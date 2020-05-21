import datetime

from app.main import mongo

class Customers(mongo.Document):
    user_id = mongo.StringField(required=True, max_length=256)
    login = mongo.StringField(required=True, max_length=256)
    name = mongo.StringField(required=True, max_length=256)
    company_id = mongo.StringField(required=True, max_length=256)
    password = mongo.StringField(required=True, max_length=256)
    credit_cards = mongo.StringField(required=True, max_length=512)

    def __repr__(self):
        return '<Customers(name={self.name!r})>'.format(self=self)

    def find_by_user_ids(user_ids=[]):
        if user_ids:
            return Customers.objects(user_id__in=user_ids)
        return Customers.objects()
