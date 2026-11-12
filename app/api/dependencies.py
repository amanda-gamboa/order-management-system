"""Provide shared dependencies for API endpoints."""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal


def get_session() -> Generator[Session, None, None]:
    """Provide a SQLAlchemy session with transaction management.

    Yields:
        A SQLAlchemy session for database operations.

    The transaction is committed if the operations succeed
    or rolled back if an exception occurs.
    """

    with SessionLocal.begin() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session, scope="function")]
