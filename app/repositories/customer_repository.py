from sqlalchemy.orm import Session

from app.models.customer import Customer


def add_customers(session: Session, customers: list[Customer]) -> list[Customer]:
    session.add_all(customers)
    return customers
