"""Define the declarative base for SQLAlchemy models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models.

    Provides the shared declarative base used by SQLAlchemy
    to define and register the application's database models.
    """

    pass
