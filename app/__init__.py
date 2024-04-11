from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api

from .endpoints import *

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://mongoUser:dd74d6aecd2a6ebb0@localhost:27017/restaurant"
mongo = PyMongo(app)

# Flask-Restful API setup
api = Api(app)
api.add_resource(TablesEndpoints, '/api/tables', resource_class_kwargs={'mongo': mongo})
api.add_resource(TableIdEndpoints, '/api/tables/<table_id>', resource_class_kwargs={'mongo': mongo})
api.add_resource(CustomersEndpoints, '/api/customers', resource_class_kwargs={'mongo': mongo})
api.add_resource(CustomerIdEndpoints, '/api/customers/<customer_id>', resource_class_kwargs={'mongo': mongo})
api.add_resource(ReservationsEndpoints, '/api/reservations', resource_class_kwargs={'mongo': mongo})
api.add_resource(ReservationIdEndpoints, '/api/reservations/<reservation_id>', resource_class_kwargs={'mongo': mongo})
