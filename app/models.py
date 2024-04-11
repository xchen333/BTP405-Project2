import uuid


class Table:
    def __init__(self, table_number, capacity, is_available=True):
        self.table_id = str(uuid.uuid4())
        self.table_number = table_number
        self.capacity = capacity
        self.is_available = is_available

    def to_dict(self):
        return {
            "table_id": self.table_id,
            "table_number": self.table_number,
            "capacity": self.capacity,
            "is_available": self.is_available
        }


class Customer:
    def __init__(self, customer_name, customer_email, customer_phone):
        self.customer_id = str(uuid.uuid4())
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_phone = customer_phone

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "customer_phone": self.customer_phone
        }


class Reservation:
    def __init__(self, customer_id, table_id, datetime, party_size):
        self.reservation_id = str(uuid.uuid4())
        self.customer_id = customer_id
        self.table_id = table_id
        self.datetime = datetime
        self.party_size = party_size

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "table_id": self.table_id,
            "datetime": self.datetime,
            "party_size": self.party_size
        }
