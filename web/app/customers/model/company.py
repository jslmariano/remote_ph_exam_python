import datetime

from app.main import mongo


class Companies(mongo.Document):
    company_id = mongo.StringField(required=True, max_length=256)
    company_name = mongo.StringField(required=True, max_length=256)

    def __repr__(self):
        return '<Companies(company_name={self.company_name!r})>'.format(self=self)

    def find_by_company_ids(company_ids=[]):
        if company_ids:
            return Companies.objects(company_id__in=company_ids)
        return Companies.objects()
