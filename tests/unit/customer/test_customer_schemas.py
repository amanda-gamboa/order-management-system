"""Test customer validation schemas."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse

# ------------- CustomerCreate ----------------


def test_customer_create_with_valid_data(valid_customer: CustomerCreate):
    """Verify CustomerCreate accepts valid customer data."""

    assert isinstance(valid_customer, CustomerCreate)
    assert valid_customer.first_name == "Laura"
    assert valid_customer.last_name == "Martínez"
    assert valid_customer.email == "laura.martinez@example.com"
    assert valid_customer.is_active is True
    assert valid_customer.phone is not None

    expected_phone = "34612345678"
    actual_phone = "".join(filter(str.isdigit, valid_customer.phone))
    assert actual_phone == expected_phone


def test_customer_create_without_optional_fields(
    customer_mandatory_data: dict[str, str],
):
    """Verify optional fields use their default values when omitted."""

    customer = CustomerCreate.model_validate(customer_mandatory_data)

    assert customer.phone is None
    assert customer.is_active is True


def test_customer_create_strips_whitespace_from_names(
    customer_mandatory_data: dict[str, str],
):
    """Verify leading and trailing whitespace is stripped from names."""

    data = customer_mandatory_data.copy()
    data["first_name"] = "  Laura  "
    data["last_name"] = "  Martínez  "

    customer = CustomerCreate.model_validate(data)

    assert customer.first_name == "Laura"
    assert customer.last_name == "Martínez"


@pytest.mark.parametrize(
    "field, value",
    [
        ("first_name", ""),
        ("first_name", "   "),
        ("last_name", ""),
        ("last_name", "   "),
    ],
    ids=[
        "first_name_empty",
        "first_name_whitespace",
        "last_name_empty",
        "last_name_whitespace",
    ],
)
def test_customer_create_rejects_blank_names(
    customer_mandatory_data: dict[str, str], field: str, value: str
):
    """Verify blank first and last names are rejected."""

    data = customer_mandatory_data.copy()
    data[field] = value

    with pytest.raises(ValidationError):
        CustomerCreate.model_validate(data)


def test_customer_create_rejects_phone_exceeding_max_length(
    customer_mandatory_data: dict[str, str],
):
    """Verify phone numbers exceeding the maximum length are rejected."""

    phone_number = "+1 650-253-0000 ext. 12345678901234567890"

    with pytest.raises(
        ValidationError, match="Phone number length must not be greater than 30"
    ):
        CustomerCreate(
            **customer_mandatory_data,
            phone=phone_number,
        )


# ------------- CustomerResponse ----------------


@pytest.mark.parametrize(
    "phone_value, expected_phone",
    [
        ("+34612345678", "34612345678"),
        (None, None),
    ],
    ids=[
        "with_valid_phone_number",
        "without_phone_number",
    ],
)
def test_customer_response_with_valid_data(
    customer_mandatory_data: dict[str, str],
    phone_value: str | None,
    expected_phone: str | None,
):
    """Verify CustomerResponse accepts customers with and without a phone number."""

    created_customer = Customer(
        id=1,
        **customer_mandatory_data,
        phone=phone_value,
        created_at=datetime.now(),
        is_active=True,
    )

    customer_response = CustomerResponse.model_validate(created_customer)

    assert isinstance(customer_response, CustomerResponse)
    assert customer_response.id == created_customer.id
    assert customer_response.first_name == created_customer.first_name
    assert customer_response.last_name == created_customer.last_name
    assert customer_response.email == created_customer.email
    assert customer_response.created_at == created_customer.created_at
    assert customer_response.is_active == created_customer.is_active

    if expected_phone is None:
        assert customer_response.phone is None
    else:
        assert customer_response.phone is not None
        actual_phone = "".join(filter(str.isdigit, customer_response.phone))
        assert actual_phone == expected_phone


def test_customer_response_without_id(customer_mandatory_data: dict[str, str]):
    """Verify CustomerResponse rejects a customer without an ID."""

    created_customer = Customer(
        **customer_mandatory_data,
        phone="+34612345678",
        created_at=datetime.now(),
        is_active=True,
    )

    with pytest.raises(ValidationError):
        CustomerResponse.model_validate(created_customer)
