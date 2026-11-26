"""Test product service operations."""

from unittest.mock import Mock

import pytest

from app.models.product import Product
from app.schemas.product import ProductCreate
from app.services.product_service import create_product, create_products

# ------------- create_product() ----------------


def test_create_product_with_valid_schema(
    session: Mock,
    mock_add_products: Mock,
    valid_product: ProductCreate,
):
    """Verify successful product creation with valid input data."""

    created_product = create_product(session, valid_product)

    mock_add_products.assert_called_once()

    # Verify the arguments passed to the mock
    # The product is wrapped in a list to meet the repository's input requirements.
    passed_session, passed_product_list = mock_add_products.call_args.args

    assert passed_session is session
    assert isinstance(passed_product_list, list)
    assert len(passed_product_list) == 1

    passed_product = passed_product_list[0]

    assert isinstance(passed_product, Product)

    # Verify the service return value
    assert isinstance(created_product, Product)
    assert created_product is passed_product

    assert created_product.name == valid_product.name
    assert created_product.product_type == valid_product.product_type
    assert created_product.price == valid_product.price
    assert created_product.is_active == valid_product.is_active


# ------------- create_products() ----------------


def test_create_products_with_valid_schemas(
    session: Mock,
    mock_add_products: Mock,
    valid_products: list[ProductCreate],
):
    """Verify successful bulk product creation with valid input data."""

    created_products = create_products(session, valid_products)

    mock_add_products.assert_called_once()

    # Verify the arguments passed to the mock
    passed_session, passed_products = mock_add_products.call_args.args

    assert passed_session is session
    assert isinstance(passed_products, list)
    assert len(passed_products) == len(valid_products)
    for passed_product in passed_products:
        assert isinstance(passed_product, Product)

    # Verify the service return value
    assert isinstance(created_products, list)
    assert created_products is passed_products
    for created_product in created_products:
        assert isinstance(created_product, Product)

    for created_product, valid_product in zip(created_products, valid_products):
        assert created_product.name == valid_product.name
        assert created_product.product_type == valid_product.product_type
        assert created_product.price == valid_product.price
        assert created_product.is_active == valid_product.is_active


def test_create_products_with_empty_list(session: Mock):
    """Verify that an empty product list raises ValueError."""

    with pytest.raises(ValueError, match="Product list is empty"):
        create_products(session, [])
