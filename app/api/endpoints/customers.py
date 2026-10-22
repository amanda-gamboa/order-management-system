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
    return create_customer(session, customer)


@router.post(
    "/bulk", status_code=status.HTTP_201_CREATED, response_model=list[CustomerResponse]
)
def create_customers_endpoint(
    customers: list[CustomerCreate], session: SessionDep
) -> list[CustomerResponse]:
    return create_customers(session, customers)
