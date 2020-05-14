from flask_restplus import Api
from flask import Blueprint

# Import apidoc for monkey patching
from flask_restplus.apidoc import apidoc

URL_PREFIX = '/api'

# Make a global change setting the URL prefix for the swaggerui at the module level
apidoc.url_prefix = URL_PREFIX

# Main
from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns

# Work Order
from .workorder.controller.receiver_controller import api as wo_receiver_ns
from .redis.controller.queue_controller import api as queue_pipe_ns

# APIS
from .customers.controller.customer_controller import api as customer_ns
from .yelp.controller.business_controller import api as yelp_business_ns

blueprint_api = Blueprint('api', __name__, url_prefix=URL_PREFIX)
# blueprint_api = Blueprint('api', __name__)

api = Api(blueprint_api,
          title='FLASK API, MONGODB, POSTGRESQL, DOCKER COMPOSE',
          version='1.0',
          description='An api made from flask with mongodb and postgresql as data, build from docker compose',
          # doc='/api'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(wo_receiver_ns, path='/workorder/receiver')
api.add_namespace(queue_pipe_ns, path='/redis/queue')
api.add_namespace(customer_ns, path='/customer')
api.add_namespace(yelp_business_ns, path='/yelp/business')