"""Initialize the application database."""

import app.models

from app.core.database import engine
from app.models.base import Base


def init_db() -> None:
    """Create database tables that do not already exist."""

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
