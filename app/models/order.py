from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Order(Base):
    """
    Represents an order placed by a customer.
    Stores its creation date and financial totals.
    The discount field represents a monetary amount.
    """

    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint(
            "subtotal >= 0",
            name="ck_orders_subtotal_nonnegative",
        ),
        CheckConstraint(
            "discount >= 0",
            name="ck_orders_discount_nonnegative",
        ),
        CheckConstraint(
            "total >= 0",
            name="ck_orders_total_nonnegative",
        ),
        CheckConstraint(
            "discount <= subtotal",
            name="ck_orders_discount_not_exceed_subtotal",
        ),
        CheckConstraint(
            "total = subtotal - discount",
            name="ck_orders_total_matches_subtotal_minus_discount",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    discount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    customer: Mapped["Customer"] = relationship(back_populates="orders")
    order_products: Mapped[list["OrderProduct"]] = relationship(back_populates="order")
