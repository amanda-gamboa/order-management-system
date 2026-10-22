from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.customer_repository import add_customers
from app.schemas.customer import CustomerCreate


def create_customer(session: Session, customer: CustomerCreate) -> Customer:
    customer_model = Customer(**customer.model_dump())
    added_customers = add_customers(session, [customer_model])
    session.flush()
    return added_customers[0]


def create_customers(
    session: Session, customers: list[CustomerCreate]
) -> list[Customer]:
    if not customers:
        raise ValueError("Customer list is empty")

    customer_models = [Customer(**customer.model_dump()) for customer in customers]
    added_customers = add_customers(session, customer_models)
    session.flush()

    return added_customers
