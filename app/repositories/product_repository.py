"""Handle product database persistence operations."""

from sqlalchemy.orm import Session

from app.models.product import Product


def add_products(session: Session, products: list[Product]) -> list[Product]:
    """Add multiple products to the SQLAlchemy session.

    Args:
        session: SQLAlchemy session to which the products are added.
        products: List of product instances to add.

    Returns:
        The list of products added to the session.
    """

    session.add_all(products)
    return products
