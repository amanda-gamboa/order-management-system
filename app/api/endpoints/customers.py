from fastapi import APIRouter, status

from app.schemas.customer import CustomerCreate, CustomerResponse
from app.api.dependencies import SessionDep
from app.services.customer_service import create_customer, create_customers

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CustomerResponse)
def create_customer_endpoint(
    customer: CustomerCreate, session: SessionDep
) -> CustomerResponse:
    """Create a new customer.

    Args:
        customer: Validated customer data provided in the request body.
        session: SQLAlchemy session used to persist the customer in the database.

    Returns:
        The newly created customer, including its ID and creation timestamp.
    """

    return create_customer(session, customer)


@router.post(
    "/bulk", status_code=status.HTTP_201_CREATED, response_model=list[CustomerResponse]
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
    """

    return create_customers(session, customers)
