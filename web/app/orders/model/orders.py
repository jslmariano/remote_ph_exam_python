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
    order_id = db.Column(db.Integer, default=0, nullable=True)
    price_per_unit = db.Column(db.Float, default=0.00, nullable=True)
    quantity = db.Column(db.Integer, default=0, nullable=True)
    product = db.Column(db.String(500), default='', nullable=True)

    def __repr__(self):
        return '<id: product: {}'.format(self.product)


class OrderDeliveries(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'order_deliveries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_item_id = db.Column(db.Integer, default=0, nullable=True)
    delivered_quantity = db.Column(db.Integer, default=0, nullable=True)
