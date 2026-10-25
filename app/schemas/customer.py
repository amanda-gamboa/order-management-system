from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime


class CustomerCreate(BaseModel):
    """Validate customer data submitted when creating a customer.

    Ensures that first and last names are not empty or composed
    only of whitespace, and that phone numbers do not exceed the
    maximum length allowed by the database field.
    """

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(max_length=255)
    phone: PhoneNumber | None = None
    is_active: bool = True

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_empty_spaces(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field cannot be empty or contain only spaces")
        return value.strip()

    @field_validator("phone")
    @classmethod
    def validate_phone_length(cls, value: PhoneNumber | None) -> PhoneNumber | None:
        if value is not None and len(value) > 30:
            raise ValueError("Phone number length must not be greater than 30")
        return value


class CustomerResponse(BaseModel):
    """Define the customer data returned to the client.

    Includes database-generated fields, such as the customer ID
    and creation timestamp.

    The model supports validation from object attributes, allowing
    Pydantic to construct the response directly from SQLAlchemy models.
    """

    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: PhoneNumber | None
    created_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}
