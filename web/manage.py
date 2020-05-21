import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint_api
from app.main import create_app, db

from app.orders.model.orders import Orders

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint_api)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()

@manager.command
def load_csv():
    """
    This will load data from custom csv files to postgres and mongodb

    Files Should be :
        - web/csv_test_datas/Test task - Mongo - customer_companies.csv
        - web/csv_test_datas/Test task - Mongo - customers.csv
        - web/csv_test_datas/Test task - Postgres - deliveries.csv
        - web/csv_test_datas/Test task - Postgres - order_items.csv
        - web/csv_test_datas/Test task - Postgres - orders.csv
    """
    from app.customers.service.customer_service import save_customers_from_csv
    from app.customers.service.company_service import save_company_from_csv

    from app.orders.service.orders_service import OrderItemService
    from app.orders.service.orders_service import OrderService
    from app.orders.service.orders_service import OrderDeliveriesService

    # STart process
    print("Trying to load CSV to MongoDB")
    save_customers_from_csv()
    save_company_from_csv()
    print("Done loading csv to MongoDB")
    print("Trying to load CSV to PostgreSQL")
    OrderService().load_from_csv()
    OrderItemService().load_from_csv()
    OrderDeliveriesService().load_from_csv()
    print("Done loading csv to PostgreSQL")

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
