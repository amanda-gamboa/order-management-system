import pytest
from pydantic import ValidationError
from datetime import datetime

from app.schemas.customer import CustomerCreate, CustomerResponse
from app.models.customer import Customer

# ------------- CustomerCreate ----------------


def test_customer_create_with_valid_data(valid_customer):
    customer = valid_customer

    assert isinstance(customer, CustomerCreate)
    assert customer.first_name == "Laura"
    assert customer.last_name == "Martínez"
    assert customer.email == "laura.martinez@example.com"
    assert customer.is_active is True

    expected_phone = "34612345678"
    actual_phone = "".join(filter(str.isdigit, customer.phone))
    assert actual_phone == expected_phone


def test_customer_create_without_optional_fields(customer_mandatory_data):
    customer = CustomerCreate(**customer_mandatory_data)

    assert customer.phone is None
    assert customer.is_active is True


def test_customer_create_strips_whitespace_from_names(customer_mandatory_data):
    data = customer_mandatory_data.copy()
    data["first_name"] = "  Laura  "
    data["last_name"] = "  Martínez  "

    customer = CustomerCreate(**data)

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
)
def test_customer_create_rejects_blank_names(customer_mandatory_data, field, value):
    data = customer_mandatory_data.copy()
    data[field] = value

    with pytest.raises(ValidationError):
        CustomerCreate(**data)


def test_customer_create_rejects_phone_exceeding_max_length(
    customer_mandatory_data,
):
    phone_number = "+123456789012345678901234567890123"

    with pytest.raises(ValidationError):
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
)
def test_customer_response_with_valid_data(
    customer_mandatory_data, phone_value, expected_phone
):
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
        actual_phone = "".join(filter(str.isdigit, customer_response.phone))
        assert actual_phone == expected_phone


def test_customer_response_without_id(customer_mandatory_data):
    created_customer = Customer(
        **customer_mandatory_data,
        phone="+34612345678",
        created_at=datetime.now(),
        is_active=True,
    )

    with pytest.raises(ValidationError):
        CustomerResponse.model_validate(created_customer)
