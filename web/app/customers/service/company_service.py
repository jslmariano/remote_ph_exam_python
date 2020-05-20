import csv
import pprint

from app.customers.model.company import Companies
from app.main import mongo

def get_all_companies():

    company_list = []
    for company in Companies.objects:
        company_dict = dict()
        company_dict['company_id'] = company.company_id
        company_dict['company_name'] = company.company_name
        company_list.append(company_dict)

    return company_list

def save_company(company_id, company_name):

    customer_model = Companies(company_id=company_id, company_name=company_name,)
    result = customer_model.save()

    pprint.pprint(result)
    return []

def save_company_from_csv():
    input_file = csv.DictReader(
        open("csv_test_datas/Test task - Mongo - customer_companies.csv")
    )

    inserted_count = 0
    for row in input_file:
        save_company(**row)
        inserted_count += 1

    message = "New {} companies".format(inserted_count)
    return {'message' : message}

def delete_all_companies():
    x = Companies.objects.delete()
    message = "Deleted {} companies".format(x)
    return {'message' : message}