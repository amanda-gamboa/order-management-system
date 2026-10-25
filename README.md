# Order Management System

A backend order management API built with Python, FastAPI, Pydantic, SQLAlchemy, and MySQL. The project manages customers, products, and orders, with a focus on relational database integrity and a layered application architecture.

## Overview

The application separates HTTP endpoints, business logic, data access, request validation, and database models into distinct layers.

SQLAlchemy ORM models define the database structure, while relational constraints enforce data integrity at the database level.

The API is currently under development.

## Technologies

- **Python** — Core programming language.
- **FastAPI** — REST API development.
- **Pydantic** — Request validation and response schemas.
- **SQLAlchemy** — ORM and database interaction.
- **MySQL** — Relational database.
- **Git and GitHub** — Version control and source code management.

## Architecture

The application follows a layered architecture that separates responsibilities across the following components.

```text
app/
├── api/
│   ├── endpoints/
│   └── dependencies.py
├── core/
│   ├── config.py
│   └── database.py
├── models/
├── schemas/
├── repositories/
├── services/
├── init_db.py
└── main.py
```

### Layer Responsibilities

- **API Endpoints:** Define HTTP routes and handle incoming requests.
- **Dependencies:** Provide shared dependencies, including database sessions.
- **Core:** Contains application configuration and database connection setup.
- **Models:** Define the database structure using SQLAlchemy ORM models.
- **Schemas:** Validate request data and define response structures using Pydantic.
- **Repositories:** Handle database access and persistence operations.
- **Services:** Coordinate business logic and data access.
- **Database Initialization:** Creates database tables that do not already exist.
- **Main Application:** Initializes the FastAPI application and registers its routers.

This separation of responsibilities makes the application easier to maintain and extend.

## Database Design

The database uses a relational model consisting of four main entities.

### Customer

Represents a customer.

The model includes:
- Unique identifier.
- First and last name.
- Unique email address.
- Optional phone number.
- Creation timestamp.
- Active status.

### Product

Represents a product available for inclusion in orders.

The model includes:
- Unique identifier.
- Name.
- Product type.
- Price.
- Active status.

A database constraint prevents negative product prices.

### Order

Represents an order placed by a customer.

The model includes:
- Unique identifier.
- Customer reference.
- Creation timestamp.
- Subtotal.
- Discount.
- Total.

Each order references a customer through a foreign key. Database constraints enforce valid monetary values and the relationship between subtotal, discount, and total.

### OrderProduct

Represents a product included in an order.

The model includes:
- Order reference.
- Product reference.
- Quantity.
- Unit price at the time of purchase.

The combination of order and product identifiers forms a composite primary key, ensuring that each product appears at most once within an order.

Database constraints prevent invalid quantities and negative unit prices.

### Data Integrity

The database schema uses relational constraints and defaults to maintain data consistency, including:

- Primary keys.
- Foreign keys.
- Unique constraints.
- Check constraints.
- Default values for applicable fields.

These constraints enforce data integrity at the database level rather than relying exclusively on application-level validation.

## Requirements

To run the application locally, you will need:

- Python.
- MySQL.
- The dependencies listed in `requirements.txt`.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/amanda-gamboa/order-management-system
cd order-management-system
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Database Connection

Create an empty MySQL database for the application.

Configure the connection settings using the environment variables expected by the application. These settings are loaded from the `.env` file.

Use `.env.example` as a reference when configuring the environment.

### 5. Initialize the Database Tables

The application uses SQLAlchemy ORM models to define the database schema.

After creating the MySQL database and configuring the connection, run the following command from the repository root:

```bash
python -m app.init_db
```

This command creates the database tables that do not already exist, based on the registered SQLAlchemy models.

The MySQL database itself must exist before running this command.

This initialization procedure does not update existing tables when the models change.

### 6. Run the Application

From the repository root, start the development server:

```bash
uvicorn app.main:app --reload
```

Once the server is running, the interactive API documentation is available at:

http://127.0.0.1:8000/docs

## API Endpoints

The API currently supports customer creation.

### Customers

#### Create a Customer

Creates a new customer.

- **Method:** `POST`
- **Request Schema:** `CustomerCreate`
- **Success Status:** `201 Created`
- **Response Schema:** `CustomerResponse`

Pydantic validates the incoming request data before the service layer processes it.

The response includes the generated customer identifier and the fields defined by the response schema.

#### Create Multiple Customers

Creates multiple customers in a single request.

- **Method:** `POST`
- **Request Body:** A list of customer creation objects
- **Success Status:** `201 Created`
- **Response Schema:** A list of `CustomerResponse` objects

Pydantic validates the request data, and the service and repository layers coordinate the creation and persistence of the customers.

**Additional customer operations and product and order endpoints will be documented as they are implemented.**

## Testing

Automated tests using pytest are planned.

The test suite will cover implemented functionality, including request validation and database operations.

## Project Status

The project is under active development.

### Implemented

- Layered application architecture.
- SQLAlchemy database models and relational constraints.
- Database connection and environment configuration.
- Database table initialization.
- Pydantic request and response schemas for customer creation.
- Customer creation endpoint.
- Bulk customer creation endpoint.

### Planned

- Customer retrieval and update operations.
- Customer activation and deactivation.
- Product management endpoints.
- Order management endpoints.
- Automated testing with pytest.