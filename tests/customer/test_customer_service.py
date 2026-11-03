import pytest

from app.models.customer import Customer
from app.services.customer_service import create_customer, create_customers


def test_create_customer_with_valid_schema(session, mock_add_customers, valid_customer):
    created_customer = create_customer(session, valid_customer)

    mock_add_customers.assert_called_once()

    # Check the arguments passed to the mock
    # The customer is wrapped in a list to meet the repository's input requirements.
    passed_session, passed_customer_list = mock_add_customers.call_args.args

    assert passed_session is session
    assert isinstance(passed_customer_list, list)
    assert len(passed_customer_list) == 1

    passed_customer = passed_customer_list[0]

    assert isinstance(passed_customer, Customer)

    # Check the service return value

    assert isinstance(created_customer, Customer)
    assert created_customer is passed_customer

    assert created_customer.first_name == valid_customer.first_name
    assert created_customer.last_name == valid_customer.last_name
    assert created_customer.email == valid_customer.email
    assert created_customer.phone == valid_customer.phone
    assert created_customer.is_active == valid_customer.is_active


def test_create_customers_with_valid_schemas(
    session, mock_add_customers, valid_customers
):
    created_customers = create_customers(session, valid_customers)

    mock_add_customers.assert_called_once()

    # Check the arguments passed to the mock

    passed_session, passed_customers = mock_add_customers.call_args.args

    assert passed_session is session
    assert isinstance(passed_customers, list)
    assert len(passed_customers) == len(valid_customers)
    for passed_customer in passed_customers:
        assert isinstance(passed_customer, Customer)

    # Check the service return value
    assert isinstance(created_customers, list)
    assert created_customers is passed_customers
    for created_customer in created_customers:
        assert isinstance(created_customer, Customer)

    for created_customer, valid_customer in zip(created_customers, valid_customers):
        assert created_customer.first_name == valid_customer.first_name
        assert created_customer.last_name == valid_customer.last_name
        assert created_customer.email == valid_customer.email
        assert created_customer.phone == valid_customer.phone
        assert created_customer.is_active == valid_customer.is_active


def test_create_customers_with_empty_list(session):

    with pytest.raises(ValueError, match="Customer list is empty"):
        create_customers(session, [])
