import json

import pytest
from flask_pymongo import PyMongo

from app import app
from app.operations import *


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.extensions['mongo'] = PyMongo(app)
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_database_after_test(client):
    yield
    app.extensions['mongo'].db.tables.delete_many({})
    app.extensions['mongo'].db.customers.delete_many({})
    app.extensions['mongo'].db.reservations.delete_many({})


# Table
def test_get_tables(client):
    # Create some sample tables
    create_table(app.extensions['mongo'], table_number=1, capacity=4)
    create_table(app.extensions['mongo'], table_number=2, capacity=2)

    # Get all tables
    response = client.get('/api/tables')
    assert response.status_code == 200
    get_all_data = json.loads(response.data)
    assert len(get_all_data) == 2

    # Get a specific table
    query = '/api/tables/' + get_all_data[0]['table_id']
    response = client.get(query)
    assert response.status_code == 200
    get_one_data = json.loads(response.data)
    assert get_one_data == get_all_data[0]


def test_create_table(client):
    # Expecting success
    response = client.post('/api/tables', json={'table_number': '3', 'capacity': 4})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data == {'message': 'New table created'}

    # Expecting error due to duplicate table_number
    response = client.post('/api/tables', json={'table_number': '3', 'capacity': 4})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == {"error": "Duplicate table_number"}


def test_update_table(client):
    # Create some sample tables
    create_table(app.extensions['mongo'], table_number=1, capacity=4)
    create_table(app.extensions['mongo'], table_number=2, capacity=2)

    # Get the uuid of the first item
    table_id = json.loads(client.get('/api/tables').data)[0]['table_id']
    # Create query string
    query = '/api/tables/' + table_id

    # Expecting success
    response = client.put(query, json={'table_number': 3, 'capacity': 4})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"message": "Table updated successfully"}
    response = client.get(query)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['table_number'] == 3
    assert data['capacity'] == 4

    # Expecting error due to duplicate table_number
    response = client.put(query, json={'table_number': 2, 'capacity': 4})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == {"error": "Duplicate table_number"}

    # Expecting error due to invalid id
    response = client.put("/api/tables/invalid_id", json={'table_number': 3, 'capacity': 4})
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data == {"error": "Table not found"}


def test_delete_table(client):
    # Create some sample tables
    create_table(app.extensions['mongo'], table_number=1, capacity=4)
    create_table(app.extensions['mongo'], table_number=2, capacity=2)

    # Get the uuid of the first item
    table_id = json.loads(client.get('/api/tables').data)[0]['table_id']
    # Create query string
    query = '/api/tables/' + table_id

    # Expecting success
    response = client.delete(query)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"message": "Table deleted successfully"}
    response = client.get('/api/tables')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1

    # Expecting error due to invalid id
    response = client.delete("/api/tables/invalid_id")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data == {"error": "Table not found"}


# Customer
def test_get_customers(client):
    # Create some sample customers
    create_customer(app.extensions['mongo'], customer_name='Jane Smith', customer_email='jane.smith@example.com',
                    customer_phone='0987654321')
    create_customer(app.extensions['mongo'], customer_name='John Doe', customer_email='john.doe@example.com',
                    customer_phone='1234567890')

    # Get all customers
    response = client.get('/api/customers')
    assert response.status_code == 200
    get_all_data = json.loads(response.data)
    assert len(get_all_data) == 2

    # Get a specific customer
    query = '/api/customers/' + get_all_data[0]['customer_id']
    response = client.get(query)
    assert response.status_code == 200
    get_one_data = json.loads(response.data)
    assert get_one_data == get_all_data[0]


def test_create_customer(client):
    # Expecting success
    response = client.post('/api/customers', json={
        'customer_name': 'Jane Smith',
        'customer_email': 'jane.smith@example.com',
        'customer_phone': '0987654321'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data == {'message': 'New customer created'}


def test_update_customer(client):
    # Create some sample customers
    create_customer(app.extensions['mongo'], customer_name='Jane Smith', customer_email='jane.smith@example.com',
                    customer_phone='0987654321')
    create_customer(app.extensions['mongo'], customer_name='John Doe', customer_email='john.doe@example.com',
                    customer_phone='1234567890')

    # Get the uuid of the first item
    customer_id = json.loads(client.get('/api/customers').data)[0]['customer_id']
    # Create query string
    query = '/api/customers/' + customer_id

    # Expecting success
    response = client.put(query, json={'customer_name': 'Sam Smith', 'customer_email': 'sam.smith@example.com',
                                       'customer_phone': '5555555555'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"message": "Customer updated successfully"}
    response = client.get(query)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['customer_name'] == 'Sam Smith'
    assert data['customer_email'] == 'sam.smith@example.com'
    assert data['customer_phone'] == '5555555555'

    # Expecting error due to invalid id
    response = client.put("/api/customers/invalid_id",
                          json={'customer_name': 'Sam Smith', 'customer_email': 'sam.smith@example.com',
                                'customer_phone': '5555555555'})
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data == {"error": "Customer not found"}


def test_delete_customer(client):
    # Create some sample customers
    create_customer(app.extensions['mongo'], customer_name='Jane Smith', customer_email='jane.smith@example.com',
                    customer_phone='0987654321')
    create_customer(app.extensions['mongo'], customer_name='John Doe', customer_email='john.doe@example.com',
                    customer_phone='1234567890')

    # Get the uuid of the first item
    customer_id = json.loads(client.get('/api/customers').data)[0]['customer_id']
    # Create query string
    query = '/api/customers/' + customer_id

    # Expecting success
    response = client.delete(query)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"message": "Customer deleted successfully"}
    response = client.get('/api/customers')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1

    # Expecting error due to invalid id
    response = client.delete("/api/customers/invalid_id")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data == {"error": "Customer not found"}


# Reservation
def test_get_reservations(client):
    # Create sample reservation
    create_customer(app.extensions['mongo'], customer_name='Jane Smith', customer_email='jane.smith@example.com',
                    customer_phone='0987654321')
    create_table(app.extensions['mongo'], table_number=1, capacity=4)

    customer_id = json.loads(client.get('/api/customers').data)[0]['customer_id']
    table_id = json.loads(client.get('/api/tables').data)[0]['table_id']

    create_reservation(app.extensions['mongo'], customer_id=customer_id, table_id=table_id,
                       datetime='2024-04-10T19:00:00', party_size=4)

    # Get all reservations
    response = client.get('/api/reservations')
    assert response.status_code == 200
    get_all_data = json.loads(response.data)
    assert len(get_all_data) == 1

    # Get a specific reservation
    query = '/api/reservations/' + get_all_data[0]['reservation_id']
    response = client.get(query)
    assert response.status_code == 200
    get_one_data = json.loads(response.data)
    assert get_one_data == get_all_data[0]


def test_create_reservations(client):
    # Expecting error due to unknown customer or table
    response = client.post('/api/reservations', json={
        "customer_id": "f2861e4f-41e9-4b92-932b-0772dd5e6bad",
        "table_id": "3cb1750d-7613-4cc4-9b58-3ab92bca45dc",
        "datetime": "2024-04-10T19:00:00",
        "party_size": 4
    })
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data == {'error': 'table_id or customer_id does not exist'}

    # Expecting success
    create_customer(app.extensions['mongo'], customer_name='Jane Smith', customer_email='jane.smith@example.com',
                    customer_phone='0987654321')
    create_table(app.extensions['mongo'], table_number=1, capacity=4)

    customer_id = json.loads(client.get('/api/customers').data)[0]['customer_id']
    table_id = json.loads(client.get('/api/tables').data)[0]['table_id']

    response = client.post('/api/reservations', json={
        "customer_id": customer_id,
        "table_id": table_id,
        "datetime": "2024-04-10T19:00:00",
        "party_size": 4
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data == {'message': 'New reservation created'}


def test_update_reservations(client):
    # Create sample reservation
    create_customer(app.extensions['mongo'], customer_name='Jane Smith', customer_email='jane.smith@example.com',
                    customer_phone='0987654321')
    create_table(app.extensions['mongo'], table_number=1, capacity=4)

    customer_id = json.loads(client.get('/api/customers').data)[0]['customer_id']
    table_id = json.loads(client.get('/api/tables').data)[0]['table_id']

    create_reservation(app.extensions['mongo'], customer_id=customer_id, table_id=table_id,
                       datetime='2024-04-10T19:00:00', party_size=4)

    # Get the uuid
    reservation_id = json.loads(client.get('/api/reservations').data)[0]['reservation_id']
    # Create query string
    query = '/api/reservations/' + reservation_id

    # Expecting success
    response = client.put(query, json={
        "datetime": "2023-04-21T18:00:00",
        "party_size": 5
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"message": "Reservation updated successfully"}
    response = client.get(query)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['datetime'] == '2023-04-21T18:00:00'
    assert data['party_size'] == 5

    # Expecting error due to invalid id
    response = client.put("/api/reservations/invalid_id", json={
        "datetime": "2023-04-21T18:00:00",
        "party_size": 5
    })
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data == {"error": "Reservation not found"}


def test_delete_reservations(client):
    # Create sample reservation
    create_customer(app.extensions['mongo'], customer_name='Jane Smith', customer_email='jane.smith@example.com',
                    customer_phone='0987654321')
    create_table(app.extensions['mongo'], table_number=1, capacity=4)

    customer_id = json.loads(client.get('/api/customers').data)[0]['customer_id']
    table_id = json.loads(client.get('/api/tables').data)[0]['table_id']

    create_reservation(app.extensions['mongo'], customer_id=customer_id, table_id=table_id,
                       datetime='2024-04-10T19:00:00', party_size=4)

    # Get the uuid
    reservation_id = json.loads(client.get('/api/reservations').data)[0]['reservation_id']
    # Create query string
    query = '/api/reservations/' + reservation_id

    # Expecting success
    response = client.delete(query)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"message": "Reservation deleted successfully"}
    response = client.get('/api/reservations')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 0

    # Expecting error due to invalid id
    response = client.delete("/api/reservations/invalid_id")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data == {"error": "Reservation not found"}
