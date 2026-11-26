"""Provide shared fixtures for testing."""

from decimal import Decimal

import pytest

from app.schemas.customer import CustomerCreate
from app.schemas.product import ProductCreate

# CUSTOMER


@pytest.fixture
def valid_customer() -> CustomerCreate:
    """Provide a valid customer creation schema."""

    return CustomerCreate(
        first_name="Laura",
        last_name="Martínez",
        email="laura.martinez@example.com",
        phone="+34612345678",
        is_active=True,
    )


@pytest.fixture
def valid_customers() -> list[CustomerCreate]:
    """Provide multiple valid customer creation schemas."""

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
def customer_mandatory_data() -> dict[str, str]:
    """Provide the mandatory fields for customer creation."""

    return {
        "first_name": "Laura",
        "last_name": "Martínez",
        "email": "laura.martinez@example.com",
    }


# PRODUCT


@pytest.fixture
def valid_product() -> ProductCreate:
    """Provide a valid product creation schema."""

    return ProductCreate(
        name="Python Programming Course",
        product_type="course",
        price=Decimal("49.99"),
        is_active=True,
    )


@pytest.fixture
def valid_products() -> list[ProductCreate]:
    """Provide multiple valid product creation schemas."""

    return [
        ProductCreate(
            name="Python Programming Course",
            product_type="course",
            price=Decimal("49.99"),
            is_active=True,
        ),
        ProductCreate(
            name="Notion Project Planner",
            product_type="template",
            price=Decimal("0.00"),
            is_active=True,
        ),
        ProductCreate(
            name="Book Lovers Club",
            product_type="membership",
            price=Decimal("5.99"),
            is_active=False,
        ),
    ]


@pytest.fixture
def product_mandatory_data() -> dict[str, str | Decimal]:
    """Provide the mandatory fields for product creation."""

    return {
        "name": "Python Programming Course",
        "product_type": "course",
        "price": Decimal("49.99"),
    }
