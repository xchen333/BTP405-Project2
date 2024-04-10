from .models import *


# Table
def create_table(mongo, table_number, capacity):
    new_table = Table(table_number, capacity)
    mongo.db.tables.insert_one(new_table.to_dict())


def get_tables(mongo, party_size=0, is_available=None):
    if is_available is None:
        tables = mongo.db.tables.find({
            'capacity': {'$gte': party_size},
        }, {'_id': 0})
    else:
        tables = mongo.db.tables.find({
            'capacity': {'$gte': party_size},
            'is_available': is_available
        }, {'_id': 0})
    all_tables = [table for table in tables]
    return all_tables


def get_table_by_id(mongo, table_id):
    return mongo.db.tables.find_one({'table_id': table_id}, {'_id': 0})


def update_table(mongo, table_id, updates):
    result = mongo.db.tables.update_one({'table_id': table_id}, {'$set': updates})
    if result.modified_count > 0:
        return True
    else:
        return False


def delete_table(mongo, table_id):
    result = mongo.db.tables.delete_one({'table_id': table_id})
    if result.deleted_count > 0:
        return True
    else:
        return False


# Customer
def create_customer(mongo, customer_name, customer_email, customer_phone):
    new_customer = Customer(customer_name, customer_email, customer_phone)
    mongo.db.customers.insert_one(new_customer.to_dict())


def get_customers(mongo):
    customers = mongo.db.customers.find({}, {'_id': 0})
    all_customers = [customer for customer in customers]
    return all_customers


def get_customer_by_id(mongo, customer_id):
    return mongo.db.customers.find_one({'customer_id': customer_id}, {'_id': 0})


def update_customer(mongo, customer_id, updates):
    result = mongo.db.customers.update_one({'customer_id': customer_id}, {'$set': updates})
    if result.modified_count > 0:
        return True
    else:
        return False


def delete_customer(mongo, customer_id):
    result = mongo.db.customers.delete_one({'customer_id': customer_id})
    if result.deleted_count > 0:
        return True
    else:
        return False


# Reservation
def create_reservation(mongo, customer_id, table_id, datetime, party_size):
    new_reservation = Reservation(customer_id, table_id, datetime, party_size)
    mongo.db.reservations.insert_one(new_reservation.to_dict())


def get_reservations(mongo):
    reservations = mongo.db.reservations.find({}, {'_id': 0})
    all_reservations = [reservation for reservation in reservations]
    return all_reservations


def get_reservation_by_id(mongo, reservation_id):
    return mongo.db.reservations.find_one({'reservation_id': reservation_id}, {'_id': 0})


def update_reservation(mongo, reservation_id, updates):
    result = mongo.db.reservations.update_one({'reservation_id': reservation_id}, {'$set': updates})
    if result.modified_count > 0:
        return True
    else:
        return False


def delete_reservation(mongo, reservation_id):
    result = mongo.db.reservations.delete_one({'reservation_id': reservation_id})
    if result.deleted_count > 0:
        return True
    else:
        return False
