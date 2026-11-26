"""Test product validation schemas."""

from datetime import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.models.product import Product
from app.product_types import ProductType
from app.schemas.product import ProductCreate, ProductResponse

# ------------- ProductCreate ----------------


def test_product_create_with_valid_data(valid_product: ProductCreate):
    """Verify ProductCreate accepts valid product data."""

    assert isinstance(valid_product, ProductCreate)
    assert valid_product.name == "Python Programming Course"
    assert valid_product.product_type == ProductType.COURSE
    assert valid_product.price == Decimal("49.99")
    assert valid_product.is_active is True


def test_product_create_without_optional_active_status(
    product_mandatory_data: dict[str, str | Decimal],
):
    """Verify active status field uses its default value when omitted."""

    product = ProductCreate.model_validate(product_mandatory_data)

    assert product.is_active is True


def test_product_create_strips_whitespace_from_name(
    product_mandatory_data: dict[str, str | Decimal],
):
    """Verify leading and trailing whitespace is stripped from name."""

    data = product_mandatory_data.copy()
    data["name"] = "  Python Programming Course  "

    product = ProductCreate.model_validate(data)

    assert product.name == "Python Programming Course"


@pytest.mark.parametrize(
    "field, value",
    [
        ("name", ""),
        ("name", "   "),
        ("product_type", ""),
        ("product_type", "   "),
    ],
    ids=[
        "name_empty",
        "name_whitespace",
        "type_empty",
        "type_whitespace",
    ],
)
def test_product_create_rejects_blank_name_and_type(
    product_mandatory_data: dict[str, str | Decimal], field: str, value: str
):
    """Verify blank product names and types are rejected."""

    data = product_mandatory_data.copy()
    data[field] = value

    with pytest.raises(ValidationError):
        ProductCreate.model_validate(data)


@pytest.mark.parametrize(
    "value, expected_type",
    [
        (" audio ", ProductType.AUDIO),
        ("Membership", ProductType.MEMBERSHIP),
        ("video game", ProductType.VIDEO_GAME),
    ],
    ids=[
        "leading_and_trailing_whitespace",
        "uppercase_letter",
        "missing_underscore",
    ],
)
def test_product_create_normalizes_product_types(
    product_mandatory_data: dict[str, str | Decimal],
    value: str,
    expected_type: ProductType,
):
    """Verify product types are properly normalized."""

    data = product_mandatory_data.copy()
    data["product_type"] = value

    product = ProductCreate.model_validate(data)
    assert product.product_type is expected_type


def test_product_create_rejects_negative_price(
    product_mandatory_data: dict[str, str | Decimal],
):
    """Verify negative product price is rejected."""

    data = product_mandatory_data.copy()
    data["price"] = -15

    with pytest.raises(ValidationError):
        ProductCreate.model_validate(data)


# ------------- ProductResponse ----------------


def test_product_response_with_valid_data(
    product_mandatory_data: dict[str, str | Decimal],
):
    """Verify ProductResponse accepts valid product data."""

    created_product = Product(
        id=1,
        **product_mandatory_data,
        created_at=datetime.now(),
        is_active=True,
    )

    product_response = ProductResponse.model_validate(created_product)

    assert isinstance(product_response, ProductResponse)
    assert product_response.id == created_product.id
    assert product_response.name == created_product.name
    assert product_response.product_type == created_product.product_type
    assert product_response.price == created_product.price
    assert product_response.created_at == created_product.created_at
    assert product_response.is_active == created_product.is_active


def test_product_response_without_id(product_mandatory_data: dict[str, str | Decimal]):
    """Verify ProductResponse rejects a product without an ID."""

    created_product = Product(
        **product_mandatory_data,
        created_at=datetime.now(),
        is_active=True,
    )

    with pytest.raises(ValidationError):
        ProductResponse.model_validate(created_product)
