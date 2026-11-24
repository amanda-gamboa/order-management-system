"""Implement business logic for product operations."""

from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product_repository import add_products
from app.schemas.product import ProductCreate


def create_product(session: Session, product: ProductCreate) -> Product:
    """Create a new product.

    Convert validated product data into a Product model and coordinate
    its persistence through the repository.

    Args:
        session: SQLAlchemy session used for database operations.
        product: Validated product data.

    Returns:
        The newly created product, with database-generated fields populated.
    """

    product_model = Product(**product.model_dump())

    # The product is wrapped in a list to meet the repository's input requirements.
    added_products = add_products(session, [product_model])

    session.flush()
    return added_products[0]


def create_products(
    session: Session, products: list[ProductCreate]
) -> list[Product]:
    """Create multiple products.

    Convert validated product data into Product models and coordinate
    their persistence through the repository.

    Args:
        session: SQLAlchemy session used for database operations.
        products: List of validated product data.

    Returns:
        The newly created products, with database-generated fields populated.

    Raises:
        ValueError: If the product list is empty.
    """

    if not products:
        raise ValueError("Product list is empty")

    product_models = [Product(**product.model_dump()) for product in products]
    added_products = add_products(session, product_models)
    session.flush()
    return added_products
