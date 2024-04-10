from flask_restful import Resource, reqparse, inputs
from pymongo.errors import DuplicateKeyError

from .operations import *


class TablesEndpoints(Resource):
    def __init__(self, mongo):
        self.mongo = mongo

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('party_size', type=int, location='args')
        parser.add_argument('is_available', type=inputs.boolean, location='args')
        args = parser.parse_args()

        if args['party_size'] is None:
            party_size = 0
        else:
            party_size = args['party_size']

        try:
            return get_tables(self.mongo, party_size, args['is_available']), 200
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("table_number", type=str, required=True, help="table_number is required")
        parser.add_argument("capacity", type=int, required=True, help="capacity is required")
        args = parser.parse_args()

        try:
            create_table(self.mongo, table_number=args["table_number"], capacity=args["capacity"])
            return {"message": "New table created"}, 201
        except DuplicateKeyError:
            return {"error": "Duplicate table_number"}, 400
        except Exception as e:
            return {"error": str(e)}, 500


class TableIdEndpoints(Resource):
    def __init__(self, mongo):
        self.mongo = mongo

    def get(self, table_id):
        try:
            result = get_table_by_id(self.mongo, table_id)
            if result is None:
                return {"error": "Table not found"}, 404
            else:
                return result, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def put(self, table_id):
        parser = reqparse.RequestParser()
        parser.add_argument("table_number", type=int)
        parser.add_argument("capacity", type=int)
        parser.add_argument("is_available", type=inputs.boolean)
        args = parser.parse_args()

        try:
            existing_table = get_table_by_id(self.mongo, table_id)

            if existing_table:
                updates = {}
                if args["table_number"] is not None:
                    updates["table_number"] = args["table_number"]
                if args["capacity"] is not None:
                    updates["capacity"] = args["capacity"]
                if args["is_available"] is not None:
                    updates["is_available"] = args["is_available"]

                if update_table(self.mongo, table_id, updates):
                    return {"message": "Table updated successfully"}, 200
                else:
                    return {"error": "Failed to update table"}, 500

            else:
                return {"error": "Table not found"}, 404

        except DuplicateKeyError:
            return {"error": "Duplicate table_number"}, 400
        except Exception as e:
            return {"error": str(e)}, 500

    def delete(self, table_id):
        try:
            existing_table = get_table_by_id(self.mongo, table_id)
            if existing_table:
                if delete_table(self.mongo, table_id):
                    return {"message": "Table deleted successfully"}, 200
                else:
                    return {"error": "Failed to delete table"}, 500
            else:
                return {"error": "Table not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500


class CustomersEndpoints(Resource):
    def __init__(self, mongo):
        self.mongo = mongo

    def get(self):
        try:
            return get_customers(self.mongo), 200
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("customer_name", type=str, required=True, help="customer_name is required")
        parser.add_argument("customer_email", type=str, required=True, help="customer_email is required")
        parser.add_argument("customer_phone", type=str, required=True, help="customer_phone is required")
        args = parser.parse_args()

        try:
            create_customer(self.mongo, customer_name=args["customer_name"], customer_email=args["customer_email"],
                            customer_phone=args["customer_phone"])
            return {"message": "New customer created"}, 201
        except Exception as e:
            return {"error": str(e)}, 500


class CustomerIdEndpoints(Resource):
    def __init__(self, mongo):
        self.mongo = mongo

    def get(self, customer_id):
        try:
            result = get_customer_by_id(self.mongo, customer_id)
            if result is None:
                return {"error": "Customer not found"}, 404
            else:
                return result, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def put(self, customer_id):
        parser = reqparse.RequestParser()
        parser.add_argument("customer_name", type=str)
        parser.add_argument("customer_email", type=str)
        parser.add_argument("customer_phone", type=str)
        args = parser.parse_args()

        try:
            existing_customer = get_customer_by_id(self.mongo, customer_id)

            if existing_customer:
                updates = {}
                if args["customer_name"] is not None:
                    updates["customer_name"] = args["customer_name"]
                if args["customer_email"] is not None:
                    updates["customer_email"] = args["customer_email"]
                if args["customer_phone"] is not None:
                    updates["customer_phone"] = args["customer_phone"]

                if update_customer(self.mongo, customer_id, updates):
                    return {"message": "Customer updated successfully"}, 200
                else:
                    return {"error": "Failed to update customer"}, 500

            else:
                return {"error": "Customer not found"}, 404

        except Exception as e:
            return {"error": str(e)}, 500

    def delete(self, customer_id):
        try:
            existing_customer = get_customer_by_id(self.mongo, customer_id)
            if existing_customer:
                if delete_customer(self.mongo, customer_id):
                    return {"message": "Customer deleted successfully"}, 200
                else:
                    return {"error": "Failed to delete customer"}, 500
            else:
                return {"error": "Customer not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500


class ReservationsEndpoints(Resource):
    def __init__(self, mongo):
        self.mongo = mongo

    def get(self):
        try:
            return get_reservations(self.mongo), 200
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("customer_id", type=str, required=True, help="customer_id is required")
        parser.add_argument("table_id", type=str, required=True, help="table_id is required")
        parser.add_argument("datetime", type=str, required=True, help="datetime is required")
        parser.add_argument("party_size", type=int, required=True, help="party_size is required")
        args = parser.parse_args()

        try:
            create_reservation(self.mongo, customer_id=args["customer_id"], table_id=args["table_id"],
                               datetime=args["datetime"], party_size=args["party_size"])
            return {"message": "New reservation created"}, 201
        except Exception as e:
            return {"error": str(e)}, 500


class ReservationIdEndpoints(Resource):
    def __init__(self, mongo):
        self.mongo = mongo

    def get(self, reservation_id):
        try:
            result = get_reservation_by_id(self.mongo, reservation_id)
            if result is None:
                return {"error": "Reservation not found"}, 404
            else:
                return result, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def put(self, reservation_id):
        parser = reqparse.RequestParser()
        parser.add_argument("customer_id", type=str)
        parser.add_argument("table_id", type=str)
        parser.add_argument("datetime", type=str)
        parser.add_argument("party_size", type=int)
        args = parser.parse_args()

        try:
            existing_reservation = get_reservation_by_id(self.mongo, reservation_id)

            if existing_reservation:
                updates = {}
                if args["customer_id"] is not None:
                    updates["customer_id"] = args["customer_id"]
                if args["table_id"] is not None:
                    updates["table_id"] = args["table_id"]
                if args["datetime"] is not None:
                    updates["datetime"] = args["datetime"]
                if args["party_size"] is not None:
                    updates["party_size"] = args["party_size"]

                if update_reservation(self.mongo, reservation_id, updates):
                    return {"message": "Reservation updated successfully"}, 200
                else:
                    return {"error": "Failed to update reservation"}, 500

            else:
                return {"error": "Reservation not found"}, 404

        except Exception as e:
            return {"error": str(e)}, 500

    def delete(self, reservation_id):
        try:
            existing_reservation = get_reservation_by_id(self.mongo, reservation_id)
            if existing_reservation:
                if delete_reservation(self.mongo, reservation_id):
                    return {"message": "Reservation deleted successfully"}, 200
                else:
                    return {"error": "Failed to delete reservation"}, 500
            else:
                return {"error": "Reservation not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500
