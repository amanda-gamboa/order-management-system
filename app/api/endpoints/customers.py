from fastapi import APIRouter, status, HTTPException
from sqlalchemy.exc import IntegrityError

from app.schemas.customer import CustomerCreate, CustomerResponse
from app.api.dependencies import SessionDep
from app.services.customer_service import create_customer, create_customers

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomerResponse,
    responses={
        status.HTTP_409_CONFLICT: {"description": "Customer data conflict"},
    },
)
def create_customer_endpoint(
    customer: CustomerCreate, session: SessionDep
) -> CustomerResponse:
    """Create a new customer.

    Args:
        customer: Validated customer data provided in the request body.
        session: SQLAlchemy session used to persist the customer in the database.

    Returns:
        The newly created customer, including its ID and creation timestamp.

    Raises:
        HTTPException: 409 if the customer data conflicts with an existing database record.
    """
    try:
        return create_customer(session, customer)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer data conflicts with an existing database record.",
        ) from exc


@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    response_model=list[CustomerResponse],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Customer list cannot be empty"},
        status.HTTP_409_CONFLICT: {"description": "Customer data conflict"},
    },
)
def create_customers_endpoint(
    customers: list[CustomerCreate], session: SessionDep
) -> list[CustomerResponse]:
    """Create multiple customers in a single request.

    Args:
        customers: Validated customer data provided in the request body.
        session: SQLAlchemy session used to persist the customers in the database.

    Returns:
        A list of newly created customers, including their IDs and creation timestamps.

    Raises:
        HTTPException: 400 if the customer list is empty.
        HTTPException: 409 if the customer data conflicts with an existing database record.
    """
    try:
        return create_customers(session, customers)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer data conflicts with an existing database record.",
        ) from exc
