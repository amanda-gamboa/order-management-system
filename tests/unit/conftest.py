"""Provide fixtures for unit tests."""

from collections.abc import Generator
from unittest.mock import Mock, patch

import pytest
from sqlalchemy.orm import Session


@pytest.fixture
def session() -> Mock:
    """Provide a mock database session."""

    return Mock(spec=Session)


@pytest.fixture
def mock_add_customers() -> Generator[Mock, None, None]:
    """Mock the customer repository function for unit testing."""

    with patch(
        "app.services.customer_service.add_customers",
        side_effect=lambda session, customers: customers,
    ) as mock_add_customers:
        yield mock_add_customers


@pytest.fixture
def mock_add_products() -> Generator[Mock, None, None]:
    """Mock the product repository function for unit testing."""

    with patch(
        "app.services.product_service.add_products",
        side_effect=lambda session, products: products,
    ) as mock_add_products:
        yield mock_add_products
