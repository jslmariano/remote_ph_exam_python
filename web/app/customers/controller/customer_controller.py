import copy

from flask import request
from flask_restplus import Resource

from ..util.dto import CustomerDto
from ..service.customer_service import *
from ..service.company_service import *
from app.orders.service.orders_service import OrderService

api = CustomerDto.api
_customer = CustomerDto.customer

@api.route('/')
class CustomerList(Resource):

    @api.doc('list_of_registered_customer')
    def get(self):
        """List all registered users"""
        return get_all_customers()


@api.route('/add')
class CustomerCsv(Resource):

    @api.doc('list_of_customers_in_csv')
    def get(self):
        """List all registered users"""
        customer_dict = dict()
        customer_dict['user_id']='josel'
        customer_dict['login']='josel'
        customer_dict['password']='josel'
        customer_dict['name']='josel'
        customer_dict['company_id']='1'
        customer_dict['credit_cards']= "[***3421]"
        return save_customer(**customer_dict)


@api.route('/csv')
class CustomerCsv(Resource):

    @api.doc('save_customers_from_csv')
    def get(self):
        """List all registered users"""
        return save_customers_from_csv()



@api.route('/orders')
class CustomerOrders(Resource):

    @api.doc('list_of_customer_orders')
    def get(self):
        """List all customer orders"""


        _limit = int(request.args.get('limit', 5))
        _page = int(request.args.get('page', 1))
        _term = request.args.get('term', None)
        _start_date = request.args.get('start_date', None)
        _end_date = request.args.get('end_date', None)

        # Filter null from javascript
        if _start_date == "null":
            _start_date = None
        if _end_date == "null":
            _end_date = None

        order_service = OrderService()
        order_service.page_size = _limit
        order_service.page = _page

        results = order_service.get_orders(_term, _start_date, _end_date)
        results['page'] = _page
        results['limit'] = _limit

        return results


@api.route('/test')
@api.doc(params={'id': 'An ID'})
class CustomerCsv(Resource):

    @api.doc('just_a_test')
    def get(self):
        """List all registered users"""

        test_datas = list()
        row_amounts = list()

        _row = dict()
        _row['customer_company'] = 'MAMBA'
        _row['customer_name'] = 'Edinburgh'
        _row['order_date'] = '2011/04/25'
        _row['delivered_amount'] = '61'
        _row['total_amount'] = '320'

        _limit = int(request.args.get('limit', 5))
        _page = int(request.args.get('page', 1))
        _term = request.args.get('term', None)
        _start_date = request.args.get('start_date', None)
        _end_date = request.args.get('end_date', None)


        _offest = _limit * (_page - 1)
        _max_to = _offest + _limit

        for x in range(_offest, _max_to):
            _item = copy.deepcopy(_row)
            _item['order_name'] = '# CLKA -{}'.format(x)
            _row_amount = int(_item['total_amount'])
            test_datas.append(_item)
            row_amounts.append(_row_amount)

        results = dict()
        results['total_amount'] = sum(row_amounts)
        results['total_count'] = _max_to * 10
        results['items'] = test_datas
        results['page'] = _page
        results['limit'] = _limit
        results['_term'] = _term
        results['_start_date'] = _start_date
        results['_end_date'] = _end_date
        results['message'] = 'Hello, I am your backend'
        return results


@api.route('/delete_all')
class CustomerDeleteAll(Resource):

    @api.doc('delete_all_customers_in_mongodb')
    def get(self):
        """List all registered users"""
        return delete_all_customer()

