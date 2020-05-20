from app.main import db
import datetime


class Orders(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_name = db.Column(db.String(500))
    customer_id = db.Column(db.String(500))
    created_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<id: order_name: {}'.format(self.order_name)


class OrderItems(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer)
    price_per_unit = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    product = db.Column(db.String(500))

    def __repr__(self):
        return '<id: product: {}'.format(self.product)


class OrderDeliveries(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'order_deliveries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_item_id = db.Column(db.Integer)
    delivered_quantity = db.Column(db.Integer)
