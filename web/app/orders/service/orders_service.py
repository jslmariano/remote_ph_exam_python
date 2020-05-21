import csv
import pprint
import json
from sqlalchemy import sql, select, func, or_

from app.main import db
from ..service.abstract_service import AbstractService
from app.orders.model.orders import Orders, OrderItems, OrderDeliveries
from app.customers.model.customer import Customers
from app.customers.model.company import Companies


def split_to_max(_records, max_per_record):

    # AVOIDING grpc_message : "Too many per request" error WORKAROUND
    # Break records into per N parts.,

    # using list comprehension
    return [_records[i:i + max_per_record] for i in range(0, len(_records), max_per_record)]


class OrderService(AbstractService):
    """docstring for OrderService"""

    def __init__(self):
        super(OrderService, self).__init__()
        self.session = db.session
        self.page_size = 5
        self.page = 0

        self.filters = {}

    def get_columns(self):
        _columns = list()
        _columns.append(Orders.id)
        _columns.append(Orders.order_name)
        _columns.append(Orders.customer_id)
        _columns.append(func.string_agg(OrderItems.product, ',').label('product_names'))
        _columns.append(func.to_char(Orders.created_at, 'Mon DDth, YYYY HH24:MI AM').label('order_date'))

        # Placeholder for missing columns for now
        _columns.append(Orders.id.label('customer_name'))
        _columns.append(Orders.id.label('customer_company'))
        return _columns

    def prepare_collection(self, term = None, start_date = None, end_date = None):
        _columns = self.get_columns()

        self.filters = dict()
        self.filters['term'] = term
        self.filters['start_date'] = start_date
        self.filters['end_date'] = end_date

        _query  = self.createQuery(Orders)
        _query = _query.join(OrderItems, OrderItems.order_id == Orders.id)

        if self.filters.get('start_date', None):
            _query = _query.filter(Orders.created_at  >= self.filters['start_date'])
        if self.filters.get('end_date', None):
            _query = _query.filter(
                Orders.created_at  <= "{0} 23:59:59".format(self.filters.get('end_date', None))
            )

        if self.filters['term']:
            product_names_column = self.getInstrumentByColumn(_columns, 'product_names')
            _query = _query.having(or_(
                    product_names_column.like("%{}%".format(self.filters['term'].strip())),
                    Orders.order_name.like("%{}%".format(self.filters['term'].strip()))
            ))

        # We only fetch ids for now for faster fetching
        _query = _query.with_entities(Orders.id)
        _query = _query.group_by(Orders.id)

        page_size = self.page_size
        page = self.page
        if page:
            page = (page - 1)

        _offset = (page * page_size)
        _query   = _query.offset(_offset)
        if page_size:
            _query   = _query.limit(page_size)
            pass

        # save query for use later
        self.setCurrentQuery(_query)
        result = dict()
        result['query'] = self.showQuery(_query, True)
        pprint.pprint(result['query'])
        result['order_ids'] = [r[0] for r in self.getCurrentIDS(Orders.id)]
        result['total_count'] = self.getCurrentCount(Orders.id)
        return result


    def get_orders(self, term = None, start_date = None, end_date = None):

        order_collection = self.prepare_collection(term, start_date, end_date)
        _columns = self.get_columns()
        # Select all results by id only for faster query
        _query = self.createQuery(Orders)
        _query = _query.join(OrderItems, OrderItems.order_id == Orders.id)
        _query = _query.filter(Orders.id.in_(order_collection['order_ids']))
        _query = _query.with_entities(*_columns)
        _query = _query.group_by(Orders.id)
        self.setCurrentQuery(_query)
        orders = self.result2list(_query)

        customers_ids = [r[0] for r in self.getCurrentIDS(Orders.customer_id)]
        customers = self.get_customers(customers_ids)

        company_ids = [customer['company_id'] for r, customer in customers.items()]
        companies = self.get_companies(company_ids)

        order_item_service = OrderItemService()
        order_items = order_item_service.get_order_items_additional(order_collection['order_ids'])
        grand_totals = list()

        # map additional totals to orders
        for x, order in enumerate(orders):
            _id = order['id']
            company_id  = customers[orders[x]['customer_id']]['company_id']
            orders[x]['customer_name'] = customers[orders[x]['customer_id']]['name']
            orders[x]['customer_company'] = companies[company_id]['company_name']
            if _id in order_items['items'].keys():
                _total_amount = order_items['items'][_id]['total_amount'] or 0
                _delivered_amount = order_items['items'][_id]['delivered_amount'] or 0
                orders[x]['total_amount'] = f"{_total_amount:,.2f}"
                orders[x]['delivered_amount'] = f"{_delivered_amount:,.2f}"
                grand_totals.append(_total_amount)

        try:
            result = dict()
            result['query'] = order_collection['query']
            result['order_ids'] = order_collection['order_ids']
            result['total_count'] = order_collection['total_count'] or 0
            result['items'] = orders
            result['order_items'] = order_items
            result['total_amount'] = f"{sum(grand_totals):,.2f}"
        except Exception as e:
            result['items'] = str(e)
            db.session.rollback()
        return result

    def get_customers(self, user_ids=[]):
        customers = Customers.find_by_user_ids(user_ids)
        customers_dicts = dict()
        for customer in customers:
            customers_dicts[customer.user_id] = dict(
                user_id=customer.user_id,
                name=customer.name,
                company_id=customer.company_id,
            )
        return customers_dicts

    def get_companies(self, company_ids=[]):
        companies = Companies.find_by_company_ids(company_ids)
        companies_dicts = dict()
        for company in companies:
            companies_dicts[company.company_id] = dict(
                company_id=company.company_id,
                company_name=company.company_name,
            )
        return companies_dicts

    def load_from_csv(self):
        print("Clearing out postgresql [orders]")
        self.truncate()

        # - web/csv_test_datas/Test task - Postgres - deliveries.csv
        # - web/csv_test_datas/Test task - Postgres - order_items.csv
        # - web/csv_test_datas/Test task - Postgres - orders.csv

        input_file = csv.DictReader(
            open("csv_test_datas/Test task - Postgres - orders.csv")
        )

        orders = list()
        max_per_record = 100000
        orders = [dict(**row) for row in input_file]
        _splits = split_to_max(orders, max_per_record)

        try:
            for _split in _splits:
                    db.engine.execute(
                        Orders.__table__.insert(),
                        _split
                    )
        except Exception as e:
            raise e

        message = "Done load orders from csv"
        print("Done loading csv to postgresql [orders]")
        return {'message' : message}

    def truncate(self):
        """
        @brief      Truncate out materials table

        @return     self
        """
        # get new instance of the table
        # intiate query
        session = self.createSession()
        # execute delete
        session.execute("TRUNCATE TABLE {0}".format('orders'))
        session.execute("SELECT setval('{0}_id_seq', 1);".format('orders'))

        try:
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise
        finally:
            session.close()


class OrderItemService(AbstractService):
    """docstring for OrderItemService"""
    def __init__(self):
        super(OrderItemService, self).__init__()
        self.session = db.session

    def column_total_amount(self):
        return sql.expression.label(
            'total_amount', OrderItems.price_per_unit * OrderItems.quantity
        )

    def column_delivered_amount(self):
        return sql.expression.label(
            'delivered_amount', OrderItems.price_per_unit * OrderDeliveries.delivered_quantity
        )

    def get_columns(self):
        columns = list()
        # Main
        columns.append(OrderItems.id)
        columns.append(OrderItems.order_id)
        columns.append(OrderItems.price_per_unit)
        columns.append(OrderItems.quantity)
        columns.append(OrderItems.product)
        columns.append(self.column_total_amount())
        # Joined
        columns.append(OrderDeliveries.delivered_quantity)
        columns.append(self.column_delivered_amount())
        return columns

    def prepare_collection(self, order_ids):
        _query = self.createQuery(OrderItems)
        pprint.pprint(_query)
        _query = _query.filter(OrderItems.order_id.in_(order_ids))

        # We only fetch ids for now for faster fetching
        _query = _query.with_entities(OrderItems.id)

        # save query for use later
        self.setCurrentQuery(_query)
        result = dict()
        result['query'] = self.showQuery(_query, True)
        result['order_item_ids'] = [r[0] for r in self.getCurrentIDS(OrderItems.id)]
        return result

    def get_order_items_additional(self, order_ids, sum_totals = True):

        result = dict()
        order_item_collection = self.prepare_collection(order_ids)
        _columns = self.get_columns()

        # Select all results by id only for faster query
        _query = self.createQuery(OrderItems)
        _query = _query.outerjoin(OrderDeliveries, OrderDeliveries.order_item_id == OrderItems.id)
        _query = _query.filter(OrderItems.id.in_(order_item_collection['order_item_ids']))

        # If we nly need the sum total, we just sum it all
        if sum_totals:
            _columns = list()
            _columns.append(OrderItems.order_id)
            _columns.append(func.sum(self.column_total_amount()).label('total_amount'))
            _columns.append(func.sum(self.column_delivered_amount()).label('delivered_amount'))
            pass

        _query = _query.with_entities(*_columns)

        if sum_totals:
            _query = _query.group_by(OrderItems.order_id)


        self.setCurrentQuery(_query)

        order_items = self.result2dict(_query, 'order_id')

        try:
            result['collection'] = order_item_collection
            result['query'] = self.showQuery(_query, True)
            result['items'] = order_items
        except Exception as e:
            result['items'] = str(e)
            db.session.rollback()
        return result

    def load_from_csv(self):
        print("Clearing out postgresql [order_items]")
        self.truncate()

        # - web/csv_test_datas/Test task - Postgres - deliveries.csv
        # - web/csv_test_datas/Test task - Postgres - order_items.csv
        # - web/csv_test_datas/Test task - Postgres - order_items.csv

        input_file = csv.DictReader(
            open("csv_test_datas/Test task - Postgres - order_items.csv")
        )

        order_items = list()
        max_per_record = 100000
        str_to_none = lambda i : i or None
        order_items = [
            {k: str_to_none(v) for k, v in dict(**row).items()}
            for row in input_file
        ]
        _splits = split_to_max(order_items, max_per_record)

        error = None
        try:
            for _split in _splits:
                curr = _split
                db.engine.execute(
                    OrderItems.__table__.insert(),
                    _split
                )
        except Exception as e:
            error = (str(e))

        message = "Done load order items from csv"
        print("Done loading csv to postgresql [order_items]")
        return {'message' : _splits, "error" : error}

    def truncate(self):
        """
        @brief      Truncate out materials table

        @return     self
        """
        # get new instance of the table
        # intiate query
        session = self.createSession()
        # execute delete
        session.execute("TRUNCATE TABLE {0}".format('order_items'))
        session.execute("SELECT setval('{0}_id_seq', 1);".format('order_items'))

        try:
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise
        finally:
            session.close()


class OrderDeliveriesService(AbstractService):
    """docstring for OrderDeliveriesService"""

    def __init__(self):
        super(OrderDeliveriesService, self).__init__()
        self.session = db.session

    def load_from_csv(self):
        print("Clearing out postgresql [order_deliveries]")
        self.truncate()

        # - web/csv_test_datas/Test task - Postgres - deliveries.csv
        # - web/csv_test_datas/Test task - Postgres - deliveries.csv
        # - web/csv_test_datas/Test task - Postgres - deliveries.csv

        input_file = csv.DictReader(
            open("csv_test_datas/Test task - Postgres - deliveries.csv")
        )

        order_deliveries = list()
        max_per_record = 100000
        str_to_none = lambda i : i or None
        order_deliveries = [
            {k: str_to_none(v) for k, v in dict(**row).items()}
            for row in input_file
        ]
        _splits = split_to_max(order_deliveries, max_per_record)

        error = None
        try:
            for _split in _splits:
                curr = _split
                db.engine.execute(
                    OrderDeliveries.__table__.insert(),
                    _split
                )
        except Exception as e:
            raise e

        message = "Done load order items from csv"
        print("Done loading csv to postgresql [order_deliveries]")
        return {'message' : _splits, "error" : error}

    def truncate(self):
        """
        @brief      Truncate out materials table

        @return     self
        """
        # get new instance of the table
        # intiate query
        session = self.createSession()
        # execute delete
        session.execute("TRUNCATE TABLE {0}".format('order_deliveries'))
        session.execute("SELECT setval('{0}_id_seq', 1);".format('order_deliveries'))

        try:
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise
        finally:
            session.close()
