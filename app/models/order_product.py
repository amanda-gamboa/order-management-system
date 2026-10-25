from __future__ import annotations

from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class OrderProduct(Base):
    """Represents a product line within an order.

    Acts as an association table between Order and Product,
    recording the purchased quantity and the unit price at the time
    of purchase. The composite primary key ensures that each product
    appears at most once within an order.
    """

    __tablename__ = "order_products"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_order_products_quantity_positive",
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="ck_order_products_unit_price_nonnegative",
        ),
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        primary_key=True,
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        primary_key=True,
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    product: Mapped["Product"] = relationship(back_populates="order_products")
    order: Mapped["Order"] = relationship(back_populates="order_products")
