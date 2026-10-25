from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.customer_repository import add_customers
from app.schemas.customer import CustomerCreate


def create_customer(session: Session, customer: CustomerCreate) -> Customer:
    """Create a new customer.

    Convert validated customer data into a Customer model and coordinate
    its persistence through the repository.

    Args:
        session: SQLAlchemy session used for database operations.
        customer: Validated customer data.

    Returns:
        The newly created customer, with database-generated fields populated.
    """

    customer_model = Customer(**customer.model_dump())
    added_customers = add_customers(session, [customer_model])
    session.flush()
    return added_customers[0]


def create_customers(
    session: Session, customers: list[CustomerCreate]
) -> list[Customer]:
    """Create multiple customers.

    Convert validated customer data into Customer models and coordinate
    their persistence through the repository.

    Args:
        session: SQLAlchemy session used for database operations.
        customers: List of validated customer data.

    Returns:
        The newly created customers, with database-generated fields populated.

    Raises:
        ValueError: If the customer list is empty.
    """

    if not customers:
        raise ValueError("Customer list is empty")

    customer_models = [Customer(**customer.model_dump()) for customer in customers]
    added_customers = add_customers(session, customer_models)
    session.flush()

    return added_customers
