from sqlalchemy.orm import Session

from app.models.customer import Customer


def add_customers(session: Session, customers: list[Customer]) -> list[Customer]:
    """Add multiple customers to the SQLAlchemy session.

    Args:
        session: SQLAlchemy session to which the customers are added.
        customers: List of customer instances to add.

    Returns:
        The list of customers added to the session.
    """

    session.add_all(customers)
    return customers
