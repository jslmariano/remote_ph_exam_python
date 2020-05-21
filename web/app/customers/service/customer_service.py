import csv
import pprint

from app.customers.model.customer import Customers
from app.main import mongo

def get_all_customers(user_ids = []):

    customer_list = []
    for customer in Customers.find_by_user_ids(user_ids):
        customer_dict = dict()
        customer_dict['user_id'] = customer.user_id
        customer_dict['login'] = customer.login
        customer_dict['name'] = customer.name
        customer_dict['company_id'] = customer.company_id
        customer_dict['password'] = customer.password
        customer_dict['credit_cards'] = customer.credit_cards
        customer_list.append(customer_dict)

    return customer_list

def save_customer(user_id, login, password,
                  name, company_id, credit_cards):

    customer_model = Customers(user_id=user_id, login=login,
                            password=password, name=name,
                            company_id=company_id, credit_cards=credit_cards,)
    result = customer_model.save()

    pprint.pprint(result)
    return []

def save_customers_from_csv():
    print("Clearing out mongodb [customers]")
    delete_all_customer()

    input_file = csv.DictReader(
        open("csv_test_datas/Test task - Mongo - customers.csv")
    )

    inserted_count = 0
    for row in input_file:
        save_customer(**row)
        inserted_count += 1

    message = "New {} customers".format(inserted_count)
    print("Done loading csv to mongodb [customers]")
    return {'message' : message}

def delete_all_customer():
    x = Customers.objects.delete()
    message = "Deleted {} customers".format(x)
    return {'message' : message}