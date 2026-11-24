"""Define API endpoints for product operations."""

from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import SessionDep
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import create_product, create_products

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponse,
)
def create_product_endpoint(
    session: SessionDep, product: ProductCreate
) -> ProductResponse:
    """Create a new product.

    Args:
        session: SQLAlchemy session used to persist the product in the database.
        product: Validated product data provided in the request body.

    Returns:
        The newly created product, including its ID and creation timestamp.

    """

    return create_product(session, product)


@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    response_model=list[ProductResponse],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Product list cannot be empty"},
    },
)
def create_products_endpoint(
    session: SessionDep, products: list[ProductCreate]
) -> list[ProductResponse]:
    """Create multiple products in a single request.

    Args:
        session: SQLAlchemy session used to persist the products in the database.
        products: Validated product data provided in the request body.

    Returns:
        A list of newly created products, including their IDs and creation timestamps.

    Raises:
        HTTPException: 400 if the product list is empty.
    """

    try:
        return create_products(session, products)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
