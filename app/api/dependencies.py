from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.core.database import SessionLocal


def get_session() -> Generator[Session]:
    with SessionLocal.begin() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session, scope="function")]
