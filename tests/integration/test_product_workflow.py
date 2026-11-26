"""Test product API integration."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from tests.integration.database import TestingSessionLocal

INVALID_PRODUCT_DATA = [
    ("name", "    "),
    ("product_type", "virus"),
    ("price", -15),
    ("is_active", None),
]

INVALID_DATA_IDS = [
    "empty_name",
    "unsupported_product_type",
    "negative_price",
    "null_is_active",
]


# ------------- Product Creation ----------------


def test_create_product_with_valid_data(
    client: TestClient, valid_product: ProductCreate
):
    """Verify successful product creation."""

    payload = valid_product.model_dump(mode="json")

    response = client.post("/products/", json=payload)

    assert response.status_code == 201

    product_response = ProductResponse.model_validate(response.json())

    # Verify response data
    assert product_response.id is not None
    assert product_response.name == valid_product.name
    assert product_response.product_type == valid_product.product_type
    assert product_response.price == valid_product.price
    assert product_response.created_at is not None
    assert product_response.is_active == valid_product.is_active

    # Verify data persistence
    with TestingSessionLocal() as session:
        db_product = session.get(Product, product_response.id)

        assert db_product is not None
        assert db_product.id == product_response.id
        assert db_product.name == product_response.name
        assert db_product.product_type == product_response.product_type
        assert db_product.price == product_response.price
        assert db_product.created_at == product_response.created_at
        assert db_product.is_active == product_response.is_active


@pytest.mark.parametrize("field, value", INVALID_PRODUCT_DATA, ids=INVALID_DATA_IDS)
def test_create_product_rejects_invalid_data(
    client: TestClient,
    valid_product: ProductCreate,
    field: str,
    value: str | int | None,
):
    """Verify rejection of invalid product data."""

    payload = valid_product.model_dump(mode="json")
    payload[field] = value

    response = client.post("/products/", json=payload)

    assert response.status_code == 422


# ------------- Bulk Product Creation ----------------


def test_create_products_with_valid_data(
    client: TestClient, valid_products: list[ProductCreate]
):
    """Verify successful creation of multiple products."""

    payload = [product.model_dump(mode="json") for product in valid_products]

    response = client.post("/products/bulk", json=payload)

    assert response.status_code == 201

    product_responses = [
        ProductResponse.model_validate(product) for product in response.json()
    ]

    assert len(product_responses) == len(valid_products)

    # Verify response data
    for product_response, valid_product in zip(product_responses, valid_products):
        assert product_response.id is not None
        assert product_response.name == valid_product.name
        assert product_response.product_type == valid_product.product_type
        assert product_response.price == valid_product.price
        assert product_response.created_at is not None
        assert product_response.is_active == valid_product.is_active

    # Verify data persistence
    with TestingSessionLocal() as session:
        db_products = session.scalars(
            select(Product)
            .where(Product.id.in_([product.id for product in product_responses]))
            .order_by(Product.id)
        ).all()

        assert len(db_products) == len(product_responses)

        for db_product, product_response in zip(db_products, product_responses):
            assert db_product.id == product_response.id
            assert db_product.name == product_response.name
            assert db_product.product_type == product_response.product_type
            assert db_product.price == product_response.price
            assert db_product.created_at == product_response.created_at
            assert db_product.is_active == product_response.is_active


@pytest.mark.parametrize("field, value", INVALID_PRODUCT_DATA, ids=INVALID_DATA_IDS)
def test_create_products_rejects_invalid_data(
    client: TestClient,
    valid_products: list[ProductCreate],
    field: str,
    value: str | int | None,
):
    """Verify rejection of invalid product data."""

    payload = [product.model_dump(mode="json") for product in valid_products]
    payload[0][field] = value

    response = client.post("/products/bulk", json=payload)

    assert response.status_code == 422


def test_create_products_rejects_empty_list(client: TestClient):
    """Verify bulk product creation rejects an empty list."""

    response = client.post("/products/bulk", json=[])

    assert response.status_code == 400
    assert response.json()["detail"] == "Product list is empty"
