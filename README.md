# Order Management System

A backend order management API built with Python, FastAPI, Pydantic, SQLAlchemy, and MySQL. The project is designed to manage online orders for digital products, including customer management, product catalog, and order processing.

The application focuses on relational database integrity and a layered architecture. Its scope does not include physical inventory management, warehouse stock tracking, or shipping operations.

## Overview

The application separates HTTP endpoints, business logic, data access, request validation, and database models into distinct layers.

SQLAlchemy ORM models define the database structure, while relational constraints enforce data integrity at the database level.

Alembic manages database schema changes through version-controlled migrations.

The API is currently under development.

## Technologies

- **Python** — Core programming language.
- **FastAPI** — REST API development.
- **Pydantic** — Request validation and response schemas.
- **SQLAlchemy** — ORM and database interaction.
- **Alembic** — Database schema migrations.
- **MySQL** — Relational database.
- **pytest** — Unit and integration testing.
- **Docker** — Application containerization and multi-container development environment using Docker Compose.
- **Git and GitHub** — Version control and source code management.

## Architecture

The application follows a layered architecture that separates responsibilities across the following components.

```text
.
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   └── dependencies.py
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── main.py
│   └── product_types.py
├── docker/
│   └── mysql/
│       └── init/
│           └── init_test_db.sql
├── migrations/
│   ├── env.py
│   └── versions/
└── tests/
    ├── unit/
    └── integration/
```

### Component Responsibilities

- **API Endpoints:** Define HTTP routes and handle incoming requests.
- **Dependencies:** Provide shared dependencies, including database sessions.
- **Core:** Contains application configuration and database connection setup.
- **Models:** Define the database structure using SQLAlchemy ORM models.
- **Repositories:** Handle database access and persistence operations.
- **Schemas:** Validate request data and define response structures using Pydantic.
- **Services:** Coordinate business logic and data access.
- **Main Application:** Initializes the FastAPI application and registers its routers.
- **Product Types:** Defines the supported product types.
- **Unit Tests:** Test individual components in isolation.
- **Integration Tests:** Verify interactions between application components and the database.
- **Migrations:** Store version-controlled database schema migrations managed by Alembic.
- **Docker Configuration:** Defines the application and database containers, their configuration, networking, and persistent storage using Docker and Docker Compose.
- **Database Initialization:** Contains the MySQL initialization script used to create the dedicated testing database and grant the required permissions.

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

Represents a digital product available for inclusion in orders.

The model includes:

- Unique identifier.
- Name.
- Product type.
- Price.
- Creation timestamp.
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

The project can be run locally or through Docker.

For local execution, you will need:

- Python.
- MySQL.
- The dependencies listed in `requirements.txt`.

For Docker-based execution, you will need:

- Docker with Docker Compose.

Python and MySQL do not need to be installed locally when using Docker, as the application and database run inside containers.

## Installation and Setup

### Local Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/amanda-gamboa/order-management-system
cd order-management-system
```

#### 2. Create a Virtual Environment

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

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure the Database Connection

Create the application database in MySQL.

```sql
CREATE DATABASE order_management_db;
```

Create a `.env` file in the repository root using `.env.example` as a reference. Adjust the database connection values according to your local MySQL configuration.

#### 5. Apply Database Migrations

The project uses Alembic to manage database schema changes.

After creating the MySQL database and configuring the connection, run the following command from the repository root:

```bash
alembic upgrade head
```

This applies all pending migrations and brings the database schema up to the latest revision.

Alembic creates the tables and tracks the applied migration versions in the `alembic_version` table.

#### 6. Run the Application

From the repository root, start the development server:

```bash
uvicorn app.main:app --reload
```

Once the server is running, the interactive API documentation is available at:

http://127.0.0.1:8000/docs

### Docker Setup

#### 1. Configure Environment Variables

Create your local `.env` file from the example:

```bash
cp .env.example .env
```

Update the values in `.env` according to your environment.

The `.env` file contains local configuration and must not be committed to version control.

#### 2. Build and Start the Containers

```bash
docker compose up -d --build
```

This command builds the API image and starts the application and MySQL containers.

#### 3. Apply Database Migrations

Once the database is running, apply the migrations:

```bash
docker compose exec api alembic upgrade head
```

#### 4. Access the API Documentation

The interactive API documentation is available at:

http://localhost:8000/docs

### Docker Configuration

Docker Compose manages three services:

- **db:** Runs MySQL and stores database data in a volume.
- **api:** Runs the FastAPI application using Uvicorn with automatic reload enabled for development.
- **test:** Runs the test suite independently from the API service, using a dedicated testing database.

The MySQL service includes a health check to ensure the database is ready before dependent services start.

The database initialization script at `docker/mysql/init/init_test_db.sql` creates the testing database and grants the application user the required permissions.

MySQL initialization scripts are executed only when the database data directory is first initialized. Subsequent container restarts do not execute these scripts again.

## API Endpoints

The API currently supports customer and product creation, including bulk creation.

### Customers

#### Create a Customer

Creates a new customer.

- **Method:** `POST`
- **Endpoint:** `/customers/`
- **Request Schema:** `CustomerCreate`
- **Success Status:** `201 Created`
- **Response Schema:** `CustomerResponse`

Pydantic validates the incoming request data before the service layer processes it.

The response includes the generated customer identifier and other fields defined by the response schema.

#### Create Multiple Customers

Creates multiple customers in a single request.

- **Method:** `POST`
- **Endpoint:** `/customers/bulk`
- **Request Body:** A list of customer creation objects
- **Success Status:** `201 Created`
- **Response Schema:** A list of `CustomerResponse` objects

Pydantic validates the request data, and the service and repository layers coordinate the creation and persistence of the customers.

### Products

#### Create a Product

Creates a new digital product.

- **Method:** `POST`
- **Endpoint:** `/products/`
- **Request Schema:** `ProductCreate`
- **Success Status:** `201 Created`
- **Response Schema:** `ProductResponse`

Pydantic validates the incoming request data before the service layer processes it.

The response includes the generated product identifier and other fields defined by the response schema.

#### Create Multiple Products

Creates multiple digital products in a single request.

- **Method:** `POST`
- **Endpoint:** `/products/bulk`
- **Request Body:** A list of product creation objects
- **Success Status:** `201 Created`
- **Response Schema:** A list of `ProductResponse` objects

Pydantic validates each product in the request. The service and repository layers coordinate the creation and persistence of the products.

Empty bulk creation requests are rejected.

**Additional operations will be documented as they are implemented.**

## Testing

The project includes automated unit and integration tests using pytest.

The test suite currently covers customer and product schema validation, service logic, and API integration, including:

- Successful customer creation.
- Successful bulk customer creation.
- Successful product creation.
- Successful bulk product creation.
- Request data validation for customers and products.
- Product type normalization and validation.
- Product price validation.
- Duplicate email handling.
- Empty bulk creation requests.
- Database persistence and data integrity.

Integration tests use a dedicated test database to verify database operations without affecting the application database.

### Running Tests Locally

When running the tests without Docker, a dedicated testing database must be created manually in MySQL.

It must be different from the application database.

```sql
CREATE DATABASE test_order_management_db;
```

Make sure the test configuration points to `TEST_DB_NAME` rather than the application database before running the tests.

Run the test suite from the repository root:

```bash
python -m pytest -v
```

### Running Tests with Docker

Docker Compose provides a dedicated test service and initializes the testing database automatically when the MySQL data directory is first created.

Run the test suite with:

```bash
docker compose --profile test run --rm test
```

Both execution methods use a separate testing database to avoid affecting application data.

## Project Status

The project is under active development.

### Implemented

- Layered application architecture.
- SQLAlchemy database models and relational constraints.
- Database connection and environment configuration.
- Database schema migrations using Alembic.
- Pydantic request and response schemas for customer creation.
- Customer creation endpoint.
- Bulk customer creation endpoint.
- Pydantic request and response schemas for product creation.
- Product creation endpoint.
- Bulk product creation endpoint.
- Product type normalization and validation.
- Unit and integration tests for customer and product creation operations.
- Dockerfile and Docker Compose configuration.
- MySQL container with persistent data storage.
- Dedicated testing database initialization.
- Dockerized test execution.

### Planned

- Customer retrieval and update operations.
- Customer activation and deactivation.
- Product retrieval and update operations.
- Product activation and deactivation.
- Order management endpoints.