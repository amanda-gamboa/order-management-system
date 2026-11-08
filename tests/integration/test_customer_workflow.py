from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select

from database import TestingSessionLocal
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse

INVALID_CUSTOMER_DATA = [
    ("first_name", "    "),
    ("last_name", 23),
    ("email", "invalid.email"),
    ("phone", "invalid-phone-number"),
    ("is_active", None),
]

INVALID_DATA_IDS = [
    "empty_first_name",
    "non_string_last_name",
    "invalid_email",
    "invalid_phone_number",
    "null_is_active",
]


# ------------- Customer Creation ----------------


def test_create_customer_with_valid_data(
    client: TestClient, valid_customer: CustomerCreate
):
    """Test successful customer creation."""

    payload = valid_customer.model_dump(mode="json")

    response = client.post("/customers/", json=payload)

    assert response.status_code == 201

    customer_response = CustomerResponse.model_validate(response.json())

    # Check response data
    assert customer_response.id is not None
    assert customer_response.first_name == valid_customer.first_name
    assert customer_response.last_name == valid_customer.last_name
    assert customer_response.email == valid_customer.email
    assert customer_response.phone == valid_customer.phone
    assert customer_response.created_at is not None
    assert customer_response.is_active == valid_customer.is_active

    # Check data persistence
    with TestingSessionLocal() as session:
        db_customer = session.get(Customer, customer_response.id)

        assert db_customer is not None
        assert db_customer.id == customer_response.id
        assert db_customer.first_name == customer_response.first_name
        assert db_customer.last_name == customer_response.last_name
        assert db_customer.email == customer_response.email
        assert db_customer.phone == customer_response.phone
        assert db_customer.created_at == customer_response.created_at
        assert db_customer.is_active == customer_response.is_active


@pytest.mark.parametrize("field, value", INVALID_CUSTOMER_DATA, ids=INVALID_DATA_IDS)
def test_create_customer_rejects_invalid_data(
    client: TestClient,
    valid_customer: CustomerCreate,
    field: str,
    value: Any,
):
    """Test rejection of invalid customer data."""

    payload = valid_customer.model_dump(mode="json")
    payload[field] = value

    response = client.post("/customers/", json=payload)

    assert response.status_code == 422


def test_create_customer_rejects_duplicate_email(
    client: TestClient,
    valid_customer: CustomerCreate,
):
    """Test customer creation with an existing email."""

    existing_customer = Customer(**valid_customer.model_dump())

    with TestingSessionLocal.begin() as session:
        session.add(existing_customer)

    payload = valid_customer.model_dump(mode="json")

    response = client.post("/customers/", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Customer data conflicts with an existing database record."
    )

    with TestingSessionLocal() as session:
        customer_count = session.scalar(select(func.count(Customer.id)))

        assert customer_count == 1


# ------------- Bulk Customer Creation ----------------


def test_create_customers_with_valid_data(
    client: TestClient, valid_customers: list[CustomerCreate]
):
    """Test successful creation of multiple customers."""

    payload = [customer.model_dump(mode="json") for customer in valid_customers]

    response = client.post("/customers/bulk", json=payload)

    assert response.status_code == 201

    customer_responses = [
        CustomerResponse.model_validate(customer) for customer in response.json()
    ]

    assert len(customer_responses) == len(valid_customers)

    # Check response data
    for customer_response, valid_customer in zip(customer_responses, valid_customers):
        assert customer_response.id is not None
        assert customer_response.first_name == valid_customer.first_name
        assert customer_response.last_name == valid_customer.last_name
        assert customer_response.email == valid_customer.email
        assert customer_response.phone == valid_customer.phone
        assert customer_response.created_at is not None
        assert customer_response.is_active == valid_customer.is_active

    # Check data persistence
    with TestingSessionLocal() as session:
        db_customers = session.scalars(
            select(Customer)
            .where(Customer.id.in_([customer.id for customer in customer_responses]))
            .order_by(Customer.id)
        ).all()

        assert len(db_customers) == len(customer_responses)

        for db_customer, customer_response in zip(db_customers, customer_responses):
            assert db_customer.id == customer_response.id
            assert db_customer.first_name == customer_response.first_name
            assert db_customer.last_name == customer_response.last_name
            assert db_customer.email == customer_response.email
            assert db_customer.phone == customer_response.phone
            assert db_customer.created_at == customer_response.created_at
            assert db_customer.is_active == customer_response.is_active


@pytest.mark.parametrize("field, value", INVALID_CUSTOMER_DATA, ids=INVALID_DATA_IDS)
def test_create_customers_rejects_invalid_data(
    client: TestClient,
    valid_customers: list[CustomerCreate],
    field: str,
    value: Any,
):
    """Test rejection of invalid customer data."""

    payload = [customer.model_dump(mode="json") for customer in valid_customers]
    payload[0][field] = value

    response = client.post("/customers/bulk", json=payload)

    assert response.status_code == 422


def test_create_customers_rejects_duplicate_email(
    client: TestClient,
    valid_customer: CustomerCreate,
    valid_customers: list[CustomerCreate],
):
    """Test bulk customer creation with an existing email."""

    existing_customer = Customer(**valid_customer.model_dump())

    with TestingSessionLocal.begin() as session:
        session.add(existing_customer)

    payload = [customer.model_dump(mode="json") for customer in valid_customers]
    payload[0]["email"] = valid_customer.email

    response = client.post("/customers/bulk", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Customer data conflicts with an existing database record."
    )

    with TestingSessionLocal() as session:
        customer_count = session.scalar(select(func.count(Customer.id)))

        assert customer_count == 1


def test_create_customers_rejects_empty_list(client: TestClient):
    """Test bulk customer creation with an empty list."""

    response = client.post("/customers/bulk", json=[])

    assert response.status_code == 400
    assert response.json()["detail"] == "Customer list is empty"
