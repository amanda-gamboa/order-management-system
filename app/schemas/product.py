"""Define Pydantic schemas for product data validation."""

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.product_types import ProductType


class ProductCreate(BaseModel):
    """Validate product data submitted when creating a product.

    Ensures that the product name is not empty or composed only of whitespace,
    and normalizes the product type by stripping leading and trailing whitespace,
    converting it to lowercase, and replacing spaces with underscores.
    """

    name: str = Field(min_length=1, max_length=255)
    product_type: ProductType
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    is_active: bool = True

    @field_validator("name", mode="before")
    @classmethod
    def validate_and_strip_name(cls, value: Any) -> Any:
        if isinstance(value, str):
            value = value.strip()

            if not value:
                raise ValueError("This field cannot be empty or contain only spaces")

        return value

    @field_validator("product_type", mode="before")
    @classmethod
    def normalize_product_type(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip().lower().replace(" ", "_")
        return value


class ProductResponse(BaseModel):
    """Define the product data returned to the client.

    Includes database-generated fields, such as the product ID
    and creation timestamp.

    The model supports validation from object attributes, allowing
    Pydantic to construct the response directly from SQLAlchemy models.
    """

    id: int
    name: str
    product_type: ProductType
    price: Decimal
    created_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}
