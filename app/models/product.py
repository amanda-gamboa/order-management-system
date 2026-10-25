from __future__ import annotations

from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Product(Base):
    """Represents a digital product in the catalog.

    Stores its name, type, current price and active status.
    """

    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint(
            "price >= 0",
            name="ck_products_price_nonnegative",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    product_type: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    order_products: Mapped[list["OrderProduct"]] = relationship(
        back_populates="product"
    )
