# Restaurant Booking System API

Welcome to the documentation for the Restaurant Booking System API. It uses mongoDB as the backend database and provides an nginx reverse proxy server. This API provides endpoints for managing tables, customers, and reservations in a restaurant booking system.

You can set up this project using `docker-compose`.

## Build and Run

### Reverse Proxy (Optional)

A Nginx reverse proxy is included with minimal configuration. By default, the proxy listens on `port 80`. Modify the `nginx.conf` file if needed. TLS is highly recommended for necessary security.

### docker-compose

To build the API server: `docker-compose build`

To run the API server: `docker-compose up -d`

## Usage

### Base URL
```
http://yourdomain.com/api
```

### Error Handling
The API returns standard HTTP response codes to indicate success or failure of the request. In case of errors, additional error messages are provided in the response body.

#### Response Codes
- `200 OK`: Request was successful.
- `201 Created`: Resource created successfully.
- `400 Bad Request`: Invalid request parameters or data.
- `401 Unauthorized`: Authentication required.
- `404 Not Found`: Resource not found.
- `500 Internal Server Error`: Server encountered an error while processing the request.

### Endpoints

#### Tables
- **GET /tables**: Retrieve all tables or filter by party size and availability.
- **POST /tables**: Create a new table.
- **GET /tables/{table_id}**: Retrieve details of a specific table by ID.
- **PUT /tables/{table_id}**: Update details of a specific table by ID.
- **DELETE /tables/{table_id}**: Delete a specific table by ID.

#### Customers
- **GET /customers**: Retrieve all customers.
- **POST /customers**: Create a new customer.
- **GET /customers/{customer_id}**: Retrieve details of a specific customer by ID.
- **PUT /customers/{customer_id}**: Update details of a specific customer by ID.
- **DELETE /customers/{customer_id}**: Delete a specific customer by ID.

#### Reservations
- **GET /reservations**: Retrieve all reservations.
- **POST /reservations**: Create a new reservation.
- **GET /reservations/{reservation_id}**: Retrieve details of a specific reservation by ID.
- **PUT /reservations/{reservation_id}**: Update details of a specific reservation by ID.
- **DELETE /reservations/{reservation_id}**: Delete a specific reservation by ID.

### Request Parameters

- **party_size**: (integer) Filter tables by minimum capacity required.
- **is_available**: (boolean) Filter tables by availability.
- **table_number**: (string) Table number.
- **capacity**: (integer) Table capacity.
- **customer_name**: (string) Customer's name.
- **customer_email**: (string) Customer's email address.
- **customer_phone**: (string) Customer's phone number.
- **datetime**: (string) Reservation date and time.
- **customer_id**: (string) ID of the customer associated with the reservation.
- **table_id**: (string) ID of the table associated with the reservation.
- **party_size**: (integer) Number of people in the reservation.

### Example Requests

#### Retrieve all tables
```
GET /tables
```

#### Create a new table
```
POST /tables
{
    "table_number": "T001",
    "capacity": 4
}
```

#### Update details of a specific table
```
PUT /tables/{table_id}
{
    "capacity": 6
}
```

#### Delete a specific table
```
DELETE /tables/{table_id}
```

#### Retrieve all customers
```
GET /customers
```

#### Create a new customer
```
POST /customers
{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "+1234567890"
}
```

#### Retrieve details of a specific customer
```
GET /customers/{customer_id}
```

#### Update details of a specific customer
```
PUT /customers/{customer_id}
{
    "customer_email": "new_email@example.com"
}
```

#### Delete a specific customer
```
DELETE /customers/{customer_id}
```

#### Retrieve all reservations
```
GET /reservations
```

#### Create a new reservation
```
POST /reservations
{
    "customer_id": "123456",
    "table_id": "789012",
    "datetime": "2024-04-15T18:00:00",
    "party_size": 4
}
```

#### Retrieve details of a specific reservation
```
GET /reservations/{reservation_id}
```

#### Update details of a specific reservation
```
PUT /reservations/{reservation_id}
{
    "party_size": 6
}
```

#### Delete a specific reservation
```
DELETE /reservations/{reservation_id}
```