import pytest
from sqlalchemy.orm import Session
from unittest.mock import Mock, patch

from app.schemas.customer import CustomerCreate


@pytest.fixture
def valid_customer():
    return CustomerCreate(
        first_name="Laura",
        last_name="Martínez",
        email="laura.martinez@example.com",
        phone="+34612345678",
        is_active=True,
    )


@pytest.fixture
def valid_customers():
    return [
        CustomerCreate(
            first_name="Laura",
            last_name="Martínez",
            email="laura.martinez@example.com",
            phone="+34612345678",
            is_active=True,
        ),
        CustomerCreate(
            first_name="Diego",
            last_name="García",
            email="diego.garcia@example.com",
            phone="+34687654321",
            is_active=True,
        ),
        CustomerCreate(
            first_name="Sofía",
            last_name="López",
            email="sofia.lopez@example.com",
            phone=None,
            is_active=True,
        ),
    ]


@pytest.fixture
def customer_mandatory_data():
    return {
        "first_name": "Laura",
        "last_name": "Martínez",
        "email": "laura.martinez@example.com",
    }


@pytest.fixture
def session():
    return Mock(spec=Session)


@pytest.fixture
def mock_add_customers():
    with patch(
        "app.services.customer_service.add_customers",
        side_effect=lambda session, customers: customers,
    ) as mock_add_customers:
        yield mock_add_customers
